<!-- lesson-kind: combination -->
<!-- lesson-id: containers-and-api-state -->
## Containers And API State

<!-- stage: context -->
### Why A Fast Queue Refuses Good Requests

A notification service keeps at most 3 pending send requests in a fixed array. It refuses a request id that is already pending, so no user receives the same message twice. A reviewer writes a fast version that records the id in a hash set first and checks for a full array second. When the array is full, the call returns "full" but the id stays in the set. A slot frees up later, the caller retries the same id, and the service answers "duplicate" for an id that appears nowhere in the queue. The message is never sent.

Each method reads correctly when viewed alone. The defect appears only in a sequence of calls, and it comes from the order of two statements. The question of this lesson is how to choose the fields of a bounded queue with an index, and the order of writes inside each public method, so that both structures describe the same elements after every call, rejected calls included.

<!-- stage: contributions -->
### What The Earlier Lessons Contribute

The lesson Operation Traces supplied the habit of judging a class by its call sequence. A constructor and a list of calls produce a list of return values, and every call must leave a state that the next call can use. A rejected call is part of that sequence, so it needs a defined effect on the state.

The lesson Circular Buffers supplied the array with `head` and `size`, where the slot of the i-th element is `(head + i) % capacity`. The lesson Direct Stores supplied the hash set as a second collection that answers membership in constant expected time. This lesson joins the three ideas. The new work is a rule about which fields exist, which call may write them, and in what order, so that the array and the hash set always list the same elements.

<!-- stage: naive -->
### Keeping The Queue In A List

The direct design stores the pending ids in an `ArrayList`. The call `offer` scans the list with `contains` to detect a duplicate, and `poll` removes the element at position 0.

```java
final class NaiveJobQueue {
    private final java.util.ArrayList<Integer> pending = new java.util.ArrayList<>();
    private final int capacity;

    NaiveJobQueue(int capacity) { this.capacity = capacity; }

    // Returns 0 when accepted, 1 when the queue is full, 2 when the id is already pending.
    int offer(int id) {
        if (pending.contains(id)) return 2;           // linear scan of every pending id
        if (pending.size() == capacity) return 1;     // nothing was written yet, so rejection is safe
        pending.add(id);
        return 0;
    }

    // Returns the oldest id, or -1 when the queue is empty.
    int poll() {
        if (pending.isEmpty()) return -1;
        return pending.remove(0);                     // shifts every remaining element left by one
    }
}
```

With capacity 3, the calls `offer(7)`, `offer(9)`, `offer(7)`, `poll()` return 0, 0, 2 and 7. The answers are correct, and a rejected call changes nothing because all checks run before the only write. The cost sits in the two linear operations.

```predict
The queue has capacity 50,000 and is always full. A caller alternates `poll` and `offer` for 100,000 calls with ids that are never duplicates. About how many element moves or comparisons does the code above make?

Each `offer` scans all 50,000 pending ids with `contains` before it adds anything. Each `poll` shifts about 50,000 elements left by one position. So every call touches roughly 50,000 elements, and 100,000 calls cost about 5 * 10^9 operations. The correctness is fine, and the time is the problem.
```

<!-- stage: bottleneck -->
### Linear Work And Drifting Indexes

For capacity c, each call of the list version costs O(c) time. With c = 5 * 10^4 and 10^5 calls, that is about 5 * 10^9 steps for a task that needs one decision per call. The cost is easy to place. The duplicate check re-reads every pending id, and the removal at position 0 moves every pending id, although only one id left.

The obvious repair replaces the list with a ring array for order and a hash set for membership. That repair is fast, and it creates a second danger. The array and the set are now two separate records of one fact, namely which ids are pending. Any call that updates one of them, then returns early before updating the other, leaves them disagreeing. The service in the opening example failed in exactly this way.

A correct fix must meet three requirements. First, `offer` and `poll` must run in O(1) expected time. Second, the array and the set must list the same ids after every call that returns. Third, a rejected call must leave every field as it found it, so the caller can retry safely.

<!-- stage: insight -->
### One Window And One Index

#### The Live Window

<!-- names: live window, status code, atomicity -->

The ring array has capacity `c`, and two integers `head` and `size` describe the contents. The **live window** is the set of slots `(head + i) % c` for `i` from 0 to `size - 1`. A slot belongs to the queue exactly when it lies in the live window. Slots outside it hold stale values that no method reads.

Two rules define the whole representation. First, every queued id sits in exactly one slot of the live window. Second, the hash set holds one entry for each id in the live window and no other entry. The field `size` is necessary because `head` and the next write position are equal both for an empty queue and for a full one.

#### Public Calls Restore The Representation

Inside one call the array and the set change one after the other, so for a short moment they disagree. That moment is allowed only inside a method body. Every public method must end with both rules true again, on every return path, including early returns.

The practical consequence is an order of statements. A method first reads state and runs every check that can reject the call. Only after the last check passes does it write, and the writes contain no further return. The array write, the `size` update and the set update then happen together, and a later method never sees one without the others.

#### Rejected Calls Change Nothing

A method reports its outcome with a **status code**, an integer that the contract defines for each case. In this lesson 0 means accepted, 1 means full and 2 means duplicate. When two rejections apply to the same call, the contract names which one wins. In this lesson the duplicate check comes first.

A call has **atomicity** when it either completes all of its writes or makes none of them. A rejected call makes none. The next call therefore starts in the same state as if the rejected call had never happened. The observable behavior of the class is then fully described by the status codes and returned values of the call sequence, and the call sequence is the unit that a test checks.

<!-- stage: variables -->
### Fields And Their Roles

The queue of pending ids uses these fields. Together they represent one logical state, and no method may change one of them without keeping the rest consistent.

- **slots** is an int array of length `capacity`, and only the live window holds meaningful values.
- **head** is the index of the oldest element, from 0 to `capacity - 1`.
- **size** is the number of queued ids, from 0 to `capacity`.
- **queued** is a hash set that contains exactly the ids in the live window.
- **tail** is a local value `(head + size) % capacity` computed when needed, never stored, so that it cannot drift.

Ids are non-negative integers, and the value -1 means that `poll` found an empty queue.

<!-- stage: trace -->
### Following Calls Through Both Collections

#### A Correct Sequence With Wraparound

The queue has capacity 3. The pointer `head` marks the oldest slot, and the pointer `next` marks the slot that the next accepted `offer` writes. The first two offers fill slots 0 and 1. The third call repeats id 7, so the duplicate check rejects it before any write, and the fields stay as they were.

The offer of 4 fills slot 2, so `size` is 3 and `next` wraps back to slot 0. At that moment `head` and `next` are both 0, the same pair of values as in an empty queue, and only `size` tells the two cases apart. The offer of 5 returns status 1 and writes nothing. After `poll` returns 7, the offer of 5 succeeds and writes slot 0, which holds the stale value 7 until that moment. The last offer of 7 succeeds again, because `poll` removed 7 from the set.

```trace
{"cells":["0","1","2"],"pointers":["head","next"],"steps":[{"at":{"head":0,"next":0},"vars":{"slots":"[-,-,-]","size":0,"index":"{}","result":"start"},"note":"Start: every slot is empty, and the index is empty."},{"at":{"head":0,"next":1},"vars":{"slots":"[7,-,-]","size":1,"index":"{7}","result":0},"note":"offer(7) returns 0, accepted. The id enters slot 0, size becomes 1, and the index gains 7."},{"at":{"head":0,"next":2},"vars":{"slots":"[7,9,-]","size":2,"index":"{7,9}","result":0},"note":"offer(9) returns 0, accepted. The id enters slot 1, size becomes 2, and the index gains 9."},{"at":{"head":0,"next":2},"vars":{"slots":"[7,9,-]","size":2,"index":"{7,9}","result":2},"note":"offer(7) returns 2, duplicate. No field changed."},{"at":{"head":0,"next":0},"vars":{"slots":"[7,9,4]","size":3,"index":"{4,7,9}","result":0},"note":"offer(4) returns 0, accepted. The id enters slot 2, size becomes 3, and the index gains 4."},{"at":{"head":0,"next":0},"vars":{"slots":"[7,9,4]","size":3,"index":"{4,7,9}","result":1},"note":"offer(5) returns 1, full. No field changed."},{"at":{"head":1,"next":0},"vars":{"slots":"[7,9,4]","size":2,"index":"{4,9}","result":7},"note":"poll() returns 7. The head moves to slot 1, size becomes 2, and the index drops 7."},{"at":{"head":1,"next":1},"vars":{"slots":"[5,9,4]","size":3,"index":"{4,5,9}","result":0},"note":"offer(5) returns 0, accepted. The id enters slot 0, size becomes 3, and the index gains 5."},{"at":{"head":2,"next":1},"vars":{"slots":"[5,9,4]","size":2,"index":"{4,5}","result":9},"note":"poll() returns 9. The head moves to slot 2, size becomes 2, and the index drops 9."},{"at":{"head":2,"next":2},"vars":{"slots":"[5,7,4]","size":3,"index":"{4,5,7}","result":0},"note":"offer(7) returns 0, accepted. The id enters slot 1, size becomes 3, and the index gains 7."}]}
```

#### The Same Calls With The Wrong Order

The second trace uses the version that adds the id to the set before it checks for a full array. After three offers the queue holds 5, 6 and 7. The offer of 8 returns status 1, yet the set now contains 8, so the set holds an entry for an id outside the live window. The `poll` returns 5 and frees a slot. The retry of 8 returns status 2, although 8 is not queued, and a correct queue would return 0. The disagreement began at one call and surfaced two calls later, which is why a call sequence is the right unit of checking.

```trace
{"cells":["0","1","2"],"pointers":["head","next"],"steps":[{"at":{"head":0,"next":0},"vars":{"slots":"[-,-,-]","size":0,"index":"{}","result":"start"},"note":"Start: every slot is empty, and the index is empty."},{"at":{"head":0,"next":1},"vars":{"slots":"[5,-,-]","size":1,"index":"{5}","result":0},"note":"offer(5) returns 0, accepted. The id enters slot 0, size becomes 1, and the index gains 5."},{"at":{"head":0,"next":2},"vars":{"slots":"[5,6,-]","size":2,"index":"{5,6}","result":0},"note":"offer(6) returns 0, accepted. The id enters slot 1, size becomes 2, and the index gains 6."},{"at":{"head":0,"next":0},"vars":{"slots":"[5,6,7]","size":3,"index":"{5,6,7}","result":0},"note":"offer(7) returns 0, accepted. The id enters slot 2, size becomes 3, and the index gains 7."},{"at":{"head":0,"next":0},"vars":{"slots":"[5,6,7]","size":3,"index":"{5,6,7,8}","result":1},"note":"offer(8) returns 1, full. The set already gained 8 before the full check, so the index no longer matches the live window."},{"at":{"head":1,"next":0},"vars":{"slots":"[5,6,7]","size":2,"index":"{6,7,8}","result":5},"note":"poll() returns 5. The head moves to slot 1, size becomes 2, and the index drops 5."},{"at":{"head":1,"next":0},"vars":{"slots":"[5,6,7]","size":2,"index":"{6,7,8}","result":2},"note":"offer(8) returns 2, duplicate. The id 8 is not queued, so this answer is wrong: a correct queue accepts it."}]}
```

<!-- stage: code -->
### Ring Array With A Hash Index

#### The Queue Class

The constants name the status codes, so callers never compare against bare numbers. The method `offer` performs both checks before its first write. The method `poll` reads the oldest id first and then updates the three fields that depend on it.

```java
final class JobQueue {
    static final int OK = 0, FULL = 1, DUPLICATE = 2;
    private final int[] slots;
    private int head, size;
    private final java.util.HashSet<Integer> queued = new java.util.HashSet<>();

    JobQueue(int capacity) { slots = new int[capacity]; }

    // Returns a status code; a non-zero code means no field changed.
    int offer(int id) {
        if (queued.contains(id)) return DUPLICATE;          // the duplicate check wins over the full check
        if (size == slots.length) return FULL;
        slots[(head + size) % slots.length] = id;           // tail slot, one past the live window
        size++;
        queued.add(id);                                     // the set gains exactly the id that the array gained
        return OK;
    }

    // Returns the oldest id, or -1 when the queue is empty.
    int poll() {
        if (size == 0) return -1;
        int id = slots[head];
        head = (head + 1) % slots.length;                   // the old slot leaves the live window
        size--;
        queued.remove(id);                                  // the set loses exactly the id that left
        return id;
    }
}
```

#### Cost And Java Details

- **offer** costs O(1) expected time, because the hash lookup, the array write and the set insert are constant on average.
- **poll** costs O(1) expected time, because the head moves by one and the set removes one entry.
- **Memory** is O(c) for the array and the set, and it does not grow with the number of calls.

The expression `(head + size) % slots.length` never overflows for realistic capacities, because both operands are below the capacity. The set stores `Integer` objects, so `queued.remove(id)` with an `int` argument chooses the overload that removes an element. A `List<Integer>` would instead treat the same `int` as an index.

<!-- stage: applicability -->
### When The Composed API Applies

#### Recognizing The Pattern

Look for a class with a fixed capacity, a front and back discipline, and a second question that the array alone cannot answer fast: is this id present, how many entries have this key, or what is the oldest entry. Look also for a phrase such as "return false and leave the state unchanged". The invariant to state is that every queued element sits in one live slot and one index entry, and every public method restores that pair before it returns.

#### The Nearest False Friend

The false friend is to know the queue API and to assume that the fields follow from it. A reader who can call a queue still has to decide whether `tail` is stored, which field separates full from empty, and which write comes first. A class with correct individual methods can fail on a sequence, as the opening example shows. A second false friend is to add a second collection without a rule for which method owns each write, because two owners drift apart.

#### When Not To Use It

Do not build the ring and the set by hand when the capacity is unbounded or when memory for removals does not matter. A `LinkedHashSet` already keeps insertion order and membership in one object, and `iterator().next()` reads the oldest element. The hand-built version earns its place when the capacity is fixed, when the array must not allocate per call, or when the contract needs an index by position as well as by value.

<!-- stage: exercises -->
### Exercises

#### [Build] Bounded Queue Contract (Author exercise)
<!-- id: cs-bounded-queue-contract -->

**Prerequisites.** The lesson Circular Buffers. This exercise changes the policy for a full queue: a full `offer` evicts the oldest element and does not reject.

**Problem.** Design a class `BoundedQueue` with a constructor `BoundedQueue(int capacity)`. The method `int offer(int v)` appends `v` at the back. When the queue already holds `capacity` elements, it first removes the oldest element and returns that element, and otherwise it returns -1. The method `int poll()` removes and returns the oldest element, or returns -1 when the queue is empty. The method `int size()` returns the number of elements. The method `int at(int i)` returns the i-th oldest element, counting from 0, or -1 when `i` is outside `0..size-1`. Store only `slots`, `head` and `size`.

**Constraints.** These limits apply:
- **Capacity** satisfies `1 <= capacity <= 10^5`.
- **Values** are `int` values from 0 to 10^9, so -1 is never a stored value.
- **Calls** number at most 10^5 in one sequence.
- **Mutation** is limited to `offer` and `poll`; `size` and `at` change nothing.

**Example 1.** Input capacity 3 and the calls `offer(4)`, `offer(5)`, `offer(6)`, `offer(7)`, `at(0)`, `poll()`, `offer(8)`, `offer(9)`, output `-1, -1, -1, 4, 5, 5, -1, 6`.

**Example 2.** Input capacity 1 and the calls `offer(2)`, `offer(3)`, `poll()`, `poll()`, `size()`, output `-1, 2, 3, -1, 0`.

**Hint.** When the queue is full, which slot holds the oldest element, and which slot receives the new one after `head` moves?

**Changed decision.** A full queue no longer rejects. The oldest slot is overwritten in place, `head` advances in the same call, and `size` stays at capacity.

#### [Vary] Circular Queue With Status Codes (LeetCode 622)
<!-- id: cs-circular-queue-status -->

**Prerequisites.** The first exercise above. This exercise changes the contract of LeetCode 622: calls return integer status codes, and a method exposes the live window.

**Problem.** Design a class `StatusQueue` with a constructor `StatusQueue(int k)` for capacity `k`. The method `int enQueue(int v)` returns 0 after appending `v`, or 1 when the queue is full. The method `int deQueue()` returns 0 after removing the front, or 1 when the queue is empty. The methods `int front()` and `int rear()` return the oldest and newest element, or -1 when the queue is empty. The methods `boolean isEmpty()` and `boolean isFull()` report the state. The method `int[] snapshot()` returns the elements from front to back. A call that returns 1 changes no field.

**Constraints.** These limits apply:
- **Capacity** satisfies `1 <= k <= 1000`.
- **Values** satisfy `0 <= v <= 1000`.
- **Calls** number at most 3000 in one sequence.
- **Return** value of `snapshot` is a new array of length `size`.

**Example 1.** Input capacity 3 and the calls `enQueue(1)`, `enQueue(2)`, `enQueue(3)`, `enQueue(4)`, `rear()`, `isFull()`, `deQueue()`, `enQueue(4)`, `snapshot()`, output `0, 0, 0, 1, 3, true, 0, 0, [2, 3, 4]`.

**Example 2.** Input capacity 1 and the calls `deQueue()`, `enQueue(9)`, `front()`, `rear()`, `deQueue()`, `isEmpty()`, `front()`, output `1, 0, 9, 9, 0, true, -1`.

**Hint.** If the class stores only `head` and `size`, how does it compute the slot of the newest element?

**Changed decision.** Rejections become explicit status codes, and `snapshot` reads the live window so that a caller can compare the state with a model after every call.

#### [Boundary] Deque Of Capacity One With A Call Log (LeetCode 641)
<!-- id: cs-deque-capacity-one-log -->

**Prerequisites.** The second exercise above. This exercise changes the contract of LeetCode 641: the class records one character per mutating call, and the capacity may be 1.

**Problem.** Design a class `LoggedDeque` with a constructor `LoggedDeque(int k)`. The methods `boolean insertFront(int v)`, `boolean insertLast(int v)`, `boolean deleteFront()` and `boolean deleteLast()` return true when they change the deque and false otherwise. The methods `int getFront()` and `int getRear()` return -1 when the deque is empty. The method `String log()` returns one character for each mutating call so far, in call order: `A` for an accepted call and `R` for a rejected call. A rejected call changes the log and no other field.

**Constraints.** These limits apply:
- **Capacity** satisfies `1 <= k <= 1000`.
- **Values** satisfy `0 <= v <= 1000`.
- **Calls** number at most 2000 in one sequence.
- **Read methods** `getFront`, `getRear` and `log` add no character to the log.

**Example 1.** Input capacity 1 and the calls `insertFront(5)`, `insertLast(6)`, `getRear()`, `deleteLast()`, `deleteFront()`, `log()`, output `true, false, 5, true, false, "ARAR"`.

**Example 2.** Input capacity 2 and the calls `insertLast(1)`, `insertFront(2)`, `insertFront(3)`, `getFront()`, `getRear()`, `deleteLast()`, `insertLast(4)`, `getRear()`, `log()`, output `true, true, false, 2, 1, true, true, 4, "AARAA"`.

**Hint.** In a deque of capacity one, the front slot and the rear slot are the same slot. Which formula for each end still gives that slot?

**Changed decision.** Both ends write, so `insertFront` moves `head` backward with wraparound and `insertLast` writes past the live window. The log makes each rejected call observable.

#### [Recognize] Implement Router (LeetCode 3508)
<!-- id: cs-router-expiry-index -->

**Prerequisites.** The first three exercises above and the lesson Direct Stores. This exercise adds a packet identity set and a destination index to a ring that evicts its oldest packet.

**Problem.** Design a class `Router` with a constructor `Router(int memoryLimit)`. The method `boolean addPacket(int source, int destination, int timestamp)` rejects a packet whose three values equal a stored packet, returning false. Otherwise it removes the oldest stored packet when the router holds `memoryLimit` packets, stores the new packet, and returns true. The method `int[] forwardPacket()` removes and returns `[source, destination, timestamp]` of the oldest packet, or an empty array. The method `int getCount(int destination, int startTime, int endTime)` counts stored packets for that destination with `startTime <= timestamp <= endTime`.

**Constraints.** These limits apply:
- **Memory limit** satisfies `2 <= memoryLimit <= 10^5`.
- **Source and destination** satisfy `1 <= value <= 2 * 10^5`.
- **Timestamps** satisfy `1 <= timestamp <= 10^9` and never decrease across `addPacket` calls.
- **Calls** number at most 10^5, and `startTime <= endTime`.

**Example 1.** Input memory limit 3 and the calls `addPacket(1,4,10)`, `addPacket(2,4,10)`, `addPacket(1,4,10)`, `addPacket(3,5,12)`, `addPacket(2,5,13)`, `forwardPacket()`, `getCount(4,10,10)`, `getCount(5,12,13)`, output `true, true, false, true, true, [2,4,10], 0, 2`.

**Example 2.** Input memory limit 2 and the calls `addPacket(7,1,5)`, `addPacket(8,1,6)`, `getCount(1,5,6)`, `addPacket(9,1,6)`, `getCount(1,5,6)`, `getCount(1,5,5)`, output `true, true, 2, true, 2, 0`.

**Hint.** Which of the three structures must change when the oldest packet leaves, and in which order should `addPacket` check for a duplicate and evict?

**Changed decision.** Three collections now describe one packet set. The duplicate check runs before the eviction, because a rejected call may not evict anything.
