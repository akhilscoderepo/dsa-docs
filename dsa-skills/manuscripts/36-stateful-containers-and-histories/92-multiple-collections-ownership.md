<!-- lesson-kind: combination -->
<!-- lesson-id: multiple-collections-ownership -->
## Multiple Collections Ownership

<!-- stage: context -->
### Why Two Callers Receive One Session Id

A chat server hands each new connection the smallest unused session id, so a client table can be a plain array. When a connection closes, the server returns its id for reuse. A network retry then delivers the close message for session 3 twice. The server puts the id 3 into its reuse queue two times. The next two connections both receive id 3, and they now read and overwrite the same slot of the client table. Nothing crashes, and every call returns a plausible number, so the fault shows up only later as messages delivered to the wrong person.

The question of this lesson is how a class can hand out the smallest free id quickly, reject a repeated return of the same id, and prove that each id is in exactly one place at all times.

<!-- stage: contributions -->
### What The Earlier Chapters Contribute

The chapter on heaps and priority queues supplied `PriorityQueue`, which removes its smallest element in O(log k) time for k stored elements. It cannot answer the question whether a given element is stored, except by scanning all k elements. The chapter on ordered data supplied `TreeSet`, which keeps elements in sorted order and answers membership, insertion and removal of the smallest element in O(log k) time. The chapter on hash maps and sets supplied `HashSet`, which answers membership in expected O(1) time but has no order.

The chapter on design problems supplied the habit of writing down which fields describe one logical state and which method owns each change. This lesson applies that habit to a new situation. Two collections store overlapping facts about the same ids, so one method must update both and never leave them disagreeing between calls.

<!-- stage: naive -->
### Reusing Ids With One Queue

The direct design keeps a counter `next` for ids that were never handed out and a `PriorityQueue` of ids that callers gave back. Allocation takes the smallest queue entry when one exists and otherwise takes `next` and increases it. Release adds the id to the queue.

```java
final class NaivePool {
    private final int capacity;
    private int next = 0;
    private final java.util.PriorityQueue<Integer> back = new java.util.PriorityQueue<>();

    NaivePool(int capacity) { this.capacity = capacity; }

    // Returns the smallest reusable id, a fresh id, or -1 when all ids are in use.
    int allocate() {
        if (!back.isEmpty()) return back.poll();           // the smallest given-back id comes out first
        if (next < capacity) return next++;                // otherwise take a never-used id
        return -1;
    }

    // Gives an id back to the pool; the code trusts the caller.
    void release(int id) { back.add(id); }
}
```

With capacity 4, the calls `allocate`, `allocate`, `allocate`, `release(1)`, `allocate` return 0, 1, 2 and then 1. For callers that behave, the answers are correct and each call costs O(log k).

```predict
With capacity 4, the calls are allocate, allocate, release(1), release(1), allocate, allocate. What do the last two calls return, and what does the pool believe about id 1?

Both of the last two calls return 1. The queue holds two copies of 1 after the repeated release, and each allocation removes one copy. Two callers now own id 1, yet the pool believes that it handed out id 1 once and has the id fully accounted for. The queue stores order but not a fact about which ids it already contains.
```

<!-- stage: bottleneck -->
### Order Without Membership Costs O(n)

The queue gives the right order for allocation, but it gives no cheap answer to the question that release needs: is this id already waiting in the queue? Calling `contains` on a `PriorityQueue` scans its array, so each release costs O(k) for k waiting ids. A pool with 10^5 ids and 10^5 releases then performs about 10^10 element comparisons in the worst case.

The check has a second gap that no scan of the queue closes. A release of an id that was never handed out, such as id 3 when `next` is 2, passes the scan because the queue does not contain it. The pool then hands out id 3 twice, once from the queue and once when `next` reaches 3.

A correct design must therefore decide three things in about O(log k) time. It must tell whether an id is waiting for reuse. It must tell whether an id was ever handed out. It must keep both answers consistent with the order structure after every call, including calls that fail.

<!-- stage: insight -->
### Every Id Has One State

#### Three States For Every Id

<!-- names: frontier, returned set, stale entry -->

Every id from 0 to capacity - 1 is in exactly one of three states. A never-issued id has not been handed out since the pool was created. An allocated id belongs to a caller. A returned id was handed out earlier, was given back, and waits for reuse. Each state needs a store that answers its own questions quickly.

The never-issued ids form a contiguous range, because allocation takes them in increasing order. One integer, the **frontier**, stores that whole range: every id at or above the frontier is never issued, and every id below it has been issued at least once. The returned ids are scattered below the frontier, so they need a real collection.

#### Order In One Collection, Membership In Another

A `PriorityQueue` of returned ids supplies the smallest one in O(log k) time. A hash-based **returned set** holds the same ids and answers the question whether a given id waits for reuse in expected O(1) time. The queue serves allocation, and the set serves validation.

An allocated id is defined by absence. An id below the frontier that is not in the returned set must be allocated. This definition means that the pool needs no third collection, and it means that the two stores plus the frontier decide the state of every id.

#### The Policy For A Stale Entry

A **stale entry** is an element that one collection still holds although the other collection has already dropped it. The queue cannot remove an arbitrary element cheaply, so a design must pick a policy and state it. The eager policy never creates a stale entry. Every method changes the queue and the set together, so both always hold the same ids. The lazy policy lets a stale entry stay and discards it when it reaches the front. The eager policy is correct here because allocation removes from the front of both stores, and release adds to both.

The invariant has three parts. The queue and the set contain identical ids. Every one of those ids is below the frontier. No id appears twice in either one. A release that would break a part is rejected before any field changes, so a rejected call leaves the pool unchanged.

<!-- stage: variables -->
### Fields That Describe One Pool

The pool uses five fields, and every public method reads or changes them together.

- **capacity** is the number of ids, fixed at construction, so valid ids run from 0 to `capacity - 1`.
- **frontier** is the smallest never-issued id, from 0 to `capacity`.
- **returnedHeap** is a `PriorityQueue<Integer>` that holds the returned ids in increasing order.
- **returnedSet** is a `HashSet<Integer>` that holds the same ids and answers membership.
- **state(id)** is a derived answer: never-issued when `id >= frontier`, returned when `returnedSet` contains it, allocated otherwise.

The state of an id is never stored as a field, because a stored copy could disagree with the stores above. Only the frontier and the two collections hold information, and the answer for one id is computed from them in expected O(1) time.

<!-- stage: trace -->
### Following Ids Through Two Pools

#### Allocation And A Rejected Return

The first pool has capacity 4. The pointer `op` marks the current call, and the variables show the frontier and the returned ids. The first three calls take never-issued ids 0, 1 and 2, so the frontier rises to 3 and both stores stay empty. The call `release(1)` adds 1 to the heap and to the set. A second `release(1)` finds 1 in the set, so the pool rejects it and changes nothing. The call `release(0)` adds 0. The next allocation takes the smallest returned id, 0, from the heap and the set at once. The following allocation takes 1. The last allocation finds both stores empty, so it takes the frontier id 3.

```trace
{"cells":["alloc","alloc","alloc","release(1)","release(1)","release(0)","alloc","alloc","alloc"],"pointers":["op"],"steps":[{"at":{"op":-1},"vars":{"frontier":0,"returned":"[]","result":"-"},"note":"Start: no id has been issued, and both stores are empty."},{"at":{"op":0},"vars":{"frontier":1,"returned":"[]","result":"0"},"note":"Both stores are empty, so allocate issues the frontier id 0 and the frontier rises to 1."},{"at":{"op":1},"vars":{"frontier":2,"returned":"[]","result":"1"},"note":"Both stores are empty, so allocate issues the frontier id 1 and the frontier rises to 2."},{"at":{"op":2},"vars":{"frontier":3,"returned":"[]","result":"2"},"note":"Both stores are empty, so allocate issues the frontier id 2 and the frontier rises to 3."},{"at":{"op":3},"vars":{"frontier":3,"returned":"[1]","result":"ok"},"note":"Id 1 is below the frontier and not in the set, so it is allocated. The call adds it to the heap and the set."},{"at":{"op":4},"vars":{"frontier":3,"returned":"[1]","result":"rejected"},"note":"Id 1 is already in the set, so the pool rejects the call and changes nothing."},{"at":{"op":5},"vars":{"frontier":3,"returned":"[0,1]","result":"ok"},"note":"Id 0 is below the frontier and not in the set, so it is allocated. The call adds it to the heap and the set."},{"at":{"op":6},"vars":{"frontier":3,"returned":"[1]","result":"0"},"note":"allocate takes the smallest returned id, 0, from the heap and the set together."},{"at":{"op":7},"vars":{"frontier":3,"returned":"[]","result":"1"},"note":"allocate takes the smallest returned id, 1, from the heap and the set together."},{"at":{"op":8},"vars":{"frontier":4,"returned":"[]","result":"3"},"note":"Both stores are empty, so allocate issues the frontier id 3 and the frontier rises to 4."}]}
```

#### Writable Stacks With Stale Entries

The second trace uses a related shape. Several stacks of capacity 2 grow to the right, and a `TreeSet` named `writable` lists the stack indexes that may accept a push. The policy there is lazy. A stack that becomes full stays in the set until a later push looks at the front of the set, sees the full stack and discards the entry. The pointer `op` marks the current call.

The first two pushes fill stack 0, and its index stays in the set although the stack is full. The third push finds that stale entry at the front and discards it, then opens stack 1. The fourth push fills stack 1, and its entry stays. The call `popAtStack(0)` removes the top value of stack 0 and adds index 0 to the set, which now holds indexes 0 and 1. The next push finds index 0 at the front, accepts it because the stack has room, and fills it again. The push after that finds index 0 full and discards it, finds index 1 full and discards it as well, and then opens a new stack 2.

```trace
{"cells":["push(1)","push(2)","push(3)","push(4)","popAt(0)","push(5)","push(6)"],"pointers":["op"],"steps":[{"at":{"op":-1},"vars":{"writable":"[]","stacks":0},"note":"Start: there are no stacks and the set is empty."},{"at":{"op":0},"vars":{"writable":"[0]","stacks":1},"note":"push(1): The front entry is valid, so the push opens stack 0."},{"at":{"op":1},"vars":{"writable":"[0]","stacks":1},"note":"push(2): The front entry is valid, so the push accepts stack 0."},{"at":{"op":2},"vars":{"writable":"[1]","stacks":2},"note":"push(3): It discards the stale entry 0, then the push opens stack 1."},{"at":{"op":3},"vars":{"writable":"[1]","stacks":2},"note":"push(4): The front entry is valid, so the push accepts stack 1."},{"at":{"op":4},"vars":{"writable":"[0,1]","stacks":2},"note":"popAtStack(0) returns 2 and adds index 0 to the set; a present index stays once."},{"at":{"op":5},"vars":{"writable":"[0,1]","stacks":2},"note":"push(5): The front entry is valid, so the push accepts stack 0."},{"at":{"op":6},"vars":{"writable":"[2]","stacks":3},"note":"push(6): It discards the stale entries 0 and 1, then the push opens stack 2."}]}
```

<!-- stage: code -->
### Writing The Pool In Java

#### Allocate And Release With Two Owners

Two private helpers own every change to the stores, and the public methods call only those helpers. This keeps the heap and the set from drifting apart. The method `state` follows the definition of the three states from the insight stage.

```java
final class IdPool {
    static final int NEVER_ISSUED = 0, ALLOCATED = 1, RETURNED = 2;
    private final int capacity;
    private int frontier = 0;
    private final java.util.PriorityQueue<Integer> returnedHeap = new java.util.PriorityQueue<>();
    private final java.util.Set<Integer> returnedSet = new java.util.HashSet<>();

    IdPool(int capacity) { this.capacity = capacity; }

    private void putReturned(int id) { returnedHeap.add(id); returnedSet.add(id); }   // the only way an id enters the stores

    private int takeReturned() {
        int id = returnedHeap.poll();                      // the smallest returned id, removed in O(log k)
        returnedSet.remove(id);                            // keeps the set equal to the heap
        return id;
    }

    // The state of an id, derived from the frontier and the returned set.
    int state(int id) {
        if (id < 0 || id >= capacity) throw new IllegalArgumentException("id out of range: " + id);
        if (id >= frontier) return NEVER_ISSUED;           // the frontier covers a whole range with one integer
        return returnedSet.contains(id) ? RETURNED : ALLOCATED;
    }

    // Returns the smallest available id, or -1 when every id is allocated.
    int allocate() {
        if (!returnedHeap.isEmpty()) return takeReturned();    // a returned id is always below the frontier
        if (frontier < capacity) return frontier++;            // otherwise issue the next never-issued id
        return -1;
    }

    // Gives an allocated id back; any other state is a caller error and changes nothing.
    void release(int id) {
        if (state(id) != ALLOCATED) throw new IllegalStateException("id is not allocated: " + id);
        putReturned(id);
    }
}
```

#### Cost And Java Details

- **allocate** costs O(log k) time when a returned id exists and O(1) time otherwise, for k returned ids.
- **release** costs O(log k) time for the heap insertion, plus expected O(1) time for the set.
- **Space** is O(k) for the two stores, and k never exceeds `frontier`.

The set operation `returnedSet.remove(id)` takes an `int` that Java boxes to an `Integer`, which is the intended overload for a `Set`. The same call on a `List<Integer>` would remove by position, which is a different and silent behavior. The method `poll` returns an `Integer`, and unboxing it cannot fail because the code checks `isEmpty` first.

<!-- stage: applicability -->
### When Two Collections Must Agree

#### Recognizing The Pattern

Look for a class that needs the next resource by an order, such as smallest id, lowest free slot or leftmost stack with room, and also needs to answer a question about a named resource, such as whether this id is free or whether this return is legal. One collection answers the first need, and a different one answers the second. The invariant is that each resource appears in exactly one state, and every collection that mentions it agrees about that state after each public call.

#### The Nearest False Friend

The false friend is the priority queue alone. It returns the right smallest element and passes every test with well-behaved callers, yet it accepts a repeated return and stores the id twice. A scan with `contains` repairs correctness and costs O(k) per call. A second false friend is a boolean array of capacity length. It rejects repeated returns, but it finds the smallest free id by scanning, which costs O(n) per allocation when the free ids lie far to the right.

#### Choosing Eager Or Lazy Cleanup

Choose eager removal when every removal happens at the front of the ordered collection, as in this pool. Choose lazy removal when an element can lose its meaning while it sits in the middle of the ordered collection, as with a stack index that becomes full. Lazy cleanup is safe only when every use of the front element first checks that it is still valid. Do not use either policy when ids are not integers from a bounded range, because the frontier then has no meaning, and a map from resource to state is simpler.

<!-- stage: exercises -->
### Exercises

#### [Build] Reusable-ID Pool (Author exercise)
<!-- id: mco-reusable-id-pool -->

**Prerequisites.** The lesson stages above. This exercise has no LeetCode counterpart.

**Problem.** Design a class `IdPool`. Its constructor takes `capacity`, and the valid ids are the integers from 0 to `capacity - 1`. The method `allocate()` returns the smallest id that is not currently allocated, or -1 when all ids are allocated. The method `release(id)` makes an allocated id available again. It throws `IllegalArgumentException` for an id outside the valid range, and `IllegalStateException` when the id is not allocated. A call that throws leaves the pool unchanged. The method `state(id)` returns 0 for never-issued, 1 for allocated and 2 for returned.

**Constraints.** The limits are:
- **Capacity** satisfies `1 <= capacity <= 10^5`.
- **Calls** number at most 2 * 10^5.
- **Smallest** is by numeric value of the id.
- **Return** value of `allocate` is an `int`, and -1 means that no id is available.

**Example 1.** Input `capacity = 3` and four calls of `allocate()`, output `0, 1, 2, -1`.

**Example 2.** Input `capacity = 5`, three calls of `allocate()`, then `release(1)`, `release(0)` and `release(1)`, then three calls of `allocate()`. The output is `0, 1, 2`, then no output for the first two releases, then `IllegalStateException` for the third, then `0, 1, 3`.

**Hint.** If the heap and the set must hold the same ids after every call, which two lines of code change them together?

**Changed decision.** A release now validates against a derived state before it touches any collection, so repeated and never-issued ids are rejected.

#### [Vary] Smallest Number In Infinite Set (LeetCode 2336)
<!-- id: mco-infinite-set-treeset -->

**Prerequisites.** The first exercise above. This exercise changes the contract of LeetCode 2336: it adds a count of removed values, and it stores the returned values in a `TreeSet`.

**Problem.** Design a class `InfiniteSet` that starts with all positive integers. The method `popSmallest()` removes and returns the smallest value in the set. The method `addBack(num)` inserts `num` into the set when `num` was removed earlier, and does nothing otherwise. The method `removedCount()` returns how many positive integers are currently removed from the set. Keep the never-popped range in one integer `frontier`, and keep only the values below it that were added back in a `TreeSet`.

**Constraints.** The limits are:
- **Value** `num` satisfies `1 <= num <= 1000`.
- **Calls** number at most 1000.
- **Return** value of `popSmallest` and `removedCount` is an `int`.
- **Ignored** calls include `addBack` of a value at or above the frontier, and `addBack` of a value already in the set.

**Example 1.** Input is three calls of `popSmallest()`, then `addBack(2)`, `addBack(2)`, `addBack(7)`, then two calls of `popSmallest()`, then `removedCount()`. The output is `1, 2, 3`, then `2, 4`, then `4`. The second `addBack(2)` and the call `addBack(7)` change nothing.

**Example 2.** Input is `popSmallest()`, `addBack(1)`, `removedCount()`, `popSmallest()`, `removedCount()`. The output is `1`, then `0`, then `1`, then `1`.

**Hint.** Which comparison with the frontier tells whether `num` was ever removed, and which return value of `TreeSet.add` tells whether the removed count changes?

**Changed decision.** A `TreeSet` replaces the heap, so one `add` call both ignores duplicates and reports whether the value was new. The count of removed values is a fourth field that must equal `frontier - 1 - addedBack.size()` after every call.

#### [Boundary] Design Phone Directory (LeetCode 379)
<!-- id: mco-phone-directory-free-list -->

**Prerequisites.** The first exercise above. This exercise changes the contract of LeetCode 379: `release` reports whether it freed a number, and the free numbers form a linked list inside an `int` array.

**Problem.** Design a class `PhoneDirectory`. Its constructor takes `maxNumbers`, and the valid numbers run from 0 to `maxNumbers - 1`, all free at the start. The method `get()` removes any free number and returns it, or returns -1 when none is free. The method `check(number)` returns true when the number is in range and free. The method `release(number)` returns true when it changed an allocated number to free, and false for a number that is out of range or already free. Store the free numbers as a linked list in one `int[] next`, where one reserved value marks an allocated number.

**Constraints.** The limits are:
- **maxNumbers** satisfies `1 <= maxNumbers <= 10^4`.
- **Calls** number at most 2 * 10^4.
- **Number** arguments are any `int`, including negative values and values at or above `maxNumbers`.
- **Order** of the numbers returned by `get` is unspecified.

**Example 1.** Input `maxNumbers = 3` and the calls `get()`, `get()`, `release(0)`, `release(0)`, `get()`, `get()`, `get()`. The output is `0, 1, true, false, 0, 2, -1`.

**Example 2.** Input `maxNumbers = 2` and the calls `release(1)`, `check(1)`, `release(5)`, `get()`, `check(0)`. The output is `false, true, false, 0, false`. Number 1 is already free, so its release returns false.

**Hint.** If `next[n]` holds one reserved value exactly when `n` is allocated, how does `release` reject a second return without any extra collection?

**Changed decision.** The release result is now a boolean, so a repeated release is a normal answer and not an error. One array stores both ownership and the list order, so no second collection exists to disagree.

#### [Recognize] Dinner Plate Stacks (LeetCode 1172)
<!-- id: mco-dinner-plates-writable -->

**Prerequisites.** The first exercise above and the lazy cleanup policy from the applicability stage. This exercise keeps the contract of LeetCode 1172.

**Problem.** Design a class `DinnerPlates`. Its constructor takes `capacity`, the maximum number of values per stack, and there is an unbounded row of stacks numbered from 0. The method `push(val)` places `val` on the leftmost stack that is not full. The method `pop()` removes and returns the top value of the rightmost non-empty stack, or returns -1 when every stack is empty. The method `popAtStack(index)` removes and returns the top value of stack `index`, or returns -1 when that stack is empty or does not exist.

**Constraints.** The limits are:
- **capacity** satisfies `1 <= capacity <= 2 * 10^4`.
- **Values** satisfy `1 <= val <= 2 * 10^4`.
- **index** satisfies `0 <= index <= 10^5`.
- **Calls** number at most 2 * 10^5.

**Example 1.** Input `capacity = 2`, pushes of `1, 2, 3, 4, 5`, then `popAtStack(0)`, `push(6)`, `pop()`, `pop()`. The pushes build `[1,2]`, `[3,4]` and `[5]`. The output of the last four calls is `2`, nothing, `5`, `4`.

**Example 2.** Input `capacity = 1`, pushes of `7` and `8`, then `popAtStack(0)`, `popAtStack(0)`, `push(9)`, `pop()`. The pushes build `[7]` and `[8]`. The output of the last four calls is `7`, `-1`, nothing, `8`.

**Hint.** If a set of stack indexes may contain a full stack, which check must `push` run on the smallest index before it uses it?

**Changed decision.** The writable set may hold entries for full stacks and for removed stacks. Every use of its smallest entry first validates the stack and discards the entry when it is invalid.
