<!-- lesson-kind: standard -->
<!-- lesson-id: circular-buffers -->
## Circular Buffers

<!-- stage: context -->
### Why Removing The Oldest Item Stalls

A network driver keeps the most recent 4096 incoming packets in one array and hands them to the application oldest first. Packets arrive thousands of times per second, and the application removes the oldest packet each time it is ready. The first version of the driver removes the oldest packet by moving every other packet one position to the left. Under load the driver spends most of its time copying packets instead of delivering them.

The same shape appears in a keyboard input queue, a log viewer that retains the last thousand lines, and a rate limiter that remembers recent requests. In each case the capacity is fixed, items leave in the order they arrived, and memory must not grow. This lesson asks one question. How can a fixed array behave as a first-in first-out queue so that adding and removing each cost constant time, with no copying?

<!-- stage: naive -->
### Keeping The Oldest Item At Index 0

The direct design keeps the oldest item at index 0 and the newest at index `count - 1`. Adding an item writes at `count`. Removing an item returns index 0 and moves every later item one position to the left, so the invariant "oldest at index 0" holds again.

```java
final class ShiftingQueue {
    private final int[] items;
    private int count;

    ShiftingQueue(int capacity) { items = new int[capacity]; }

    boolean offer(int v) {
        if (count == items.length) return false;
        items[count++] = v;
        return true;
    }

    int poll() {
        if (count == 0) return -1;
        int v = items[0];
        for (int i = 1; i < count; i++) items[i - 1] = items[i];
        count--;
        return v;
    }
}
```

A second idea avoids the copying. The queue keeps a start index that moves right after each removal. That version never copies, but it can no longer add items after `capacity` removals, even when the queue is nearly empty, because the free positions on the left are never reused.

<!-- stage: bottleneck -->
### Counting The Copies And The Stranded Space

```predict
A queue holds 100 000 items. A program removes one item and adds one item, and repeats this 1 000 000 times. About how many item copies does the shifting version make?

About 10^11 copies. Each removal moves the 99 999 remaining items, and 1 000 000 removals multiply that by 99 999. The adds cost one write each, so the removals decide the total.
```

For a queue holding `n` items, each removal in the shifting version costs O(n) time. A million removals on a full queue of 100 000 items therefore cost about 10^11 item moves, while the useful work is 2 000 000 reads and writes. Memory stays at O(n), so time is the only problem.

The start-index version fixes the time and breaks the space. Its removal costs O(1), but the used region slides to the right end of the array, and the positions it has already left stay empty and unreachable. The array behaves as if it were consumed once.

Both failures have the same cause. The design ties the oldest item to a fixed array position or ties free space to one end of the array. A correct design must let the used region start at any index and continue from the end of the array back to index 0.

<!-- stage: insight -->
### Letting The Used Region Wrap Around

#### Two Numbers Locate Every Item

<!-- names: head, size, wraparound -->

Let `cap` be the array length. Store the array index of the oldest item in an int named `head`, and store the number of items currently held in an int named `size`. The queue contents are then the array positions `head`, `head + 1`, up to `head + size - 1`, where every position is taken modulo `cap`.

The modulo step is called **wraparound**. An index that would reach `cap` continues at index 0 instead. The next free position for an add is `(head + size) % cap`, and a removal advances `head` to `(head + 1) % cap`. Neither operation moves any item, so both cost O(1).

#### Why Size Replaces The End Index

A common alternative stores a `tail` index, the position of the next write, instead of `size`. That choice has a defect. When `head` equals `tail`, the queue could be empty or completely full, because both states make the two indices meet. Code then needs a spare unused slot or an extra flag to tell them apart.

The `size` field removes the ambiguity. The queue is empty exactly when `size == 0` and full exactly when `size == cap`. The write position is computed from `head` and `size` and never stored, so it cannot disagree with them.

#### The Invariant

At every moment between public calls, `0 <= head < cap` and `0 <= size <= cap`. The live positions are `(head + i) % cap` for `i` from 0 to `size - 1`. Because `size <= cap`, these positions are all different, so each live item has exactly one position and no position holds two items.

A deque adds symmetric rules. Adding at the front first moves `head` to `(head - 1 + cap) % cap`, and the added `cap` keeps the value non-negative because Java's `%` returns a negative result for a negative left operand. The newest item sits at `(head + size - 1) % cap`.

<!-- stage: variables -->
### Fields That Describe One Queue

A circular buffer is fully described by four values, and only three of them are stored.

- **slots** is the fixed array that holds the items; its length is the capacity.
- **head** is the array index of the oldest item, kept between 0 and `cap - 1`.
- **size** is the number of live items, kept between 0 and `cap`.
- **next** is the write position `(head + size) % cap`; it is computed on demand and never stored.

The state invariant is that the live items occupy exactly the positions `(head + i) % cap` for `i` from 0 to `size - 1`. Every public method reads these fields at its start and leaves them satisfying the invariant at its end, including when it rejects a call.

<!-- stage: trace -->
### Tracing Wraparound On Four Slots

#### Queue Of Capacity Four

Take a queue with `cap = 4`. The trace below shows the slot indexes as cells and uses two pointers: `head` marks the oldest item and `next` marks the write position. The variable `slots` lists the contents, and an underscore marks a position that no live index reaches.

The first four adds fill slots 0 to 3 in order, and `next` then equals `head`, which is why `size` is needed to see that the queue is full. The fifth add is rejected and changes nothing. A removal returns 10 from slot 0, moves `head` to 1 and leaves `next` at 0. The next add of 50 lands in slot 0, so the written item wraps to the front of the array while `head` stays at 1. Two more removals return 20 and 30, and `head` moves to 3.

```trace
{"cells":["0","1","2","3"],"pointers":["head","next"],"steps":[{"at":{"head":0,"next":0},"vars":{"slots":"_,_,_,_","size":0},"note":"The buffer is empty: size is 0, head is 0, and the write position next is (0 + 0) % 4 = 0."},{"at":{"head":0,"next":1},"vars":{"slots":"10,_,_,_","size":1},"note":"offer(10) writes slot 0, the position (head + size) % 4 computed before the add, and size becomes 1."},{"at":{"head":0,"next":2},"vars":{"slots":"10,20,_,_","size":2},"note":"offer(20) writes slot 1, the position (head + size) % 4 computed before the add, and size becomes 2."},{"at":{"head":0,"next":3},"vars":{"slots":"10,20,30,_","size":3},"note":"offer(30) writes slot 2, the position (head + size) % 4 computed before the add, and size becomes 3."},{"at":{"head":0,"next":0},"vars":{"slots":"10,20,30,40","size":4},"note":"offer(40) writes slot 3, the position (head + size) % 4 computed before the add, and size becomes 4."},{"at":{"head":0,"next":0},"vars":{"slots":"10,20,30,40","size":4},"note":"offer(50) is rejected because size equals the capacity 4. head, size and every slot stay as they were; here next equals head, so only size shows that the buffer is full."},{"at":{"head":1,"next":0},"vars":{"slots":"_,20,30,40","size":3},"note":"poll() returns 10 from slot 0, moves head to (head + 1) % 4 = 1 and lowers size to 3. No item is copied."},{"at":{"head":1,"next":1},"vars":{"slots":"50,20,30,40","size":4},"note":"offer(50) writes slot 0, the position (head + size) % 4 computed before the add, and size becomes 4. The position wrapped past the end of the array to slot 0."},{"at":{"head":2,"next":1},"vars":{"slots":"50,_,30,40","size":3},"note":"poll() returns 20 from slot 1, moves head to (head + 1) % 4 = 2 and lowers size to 3. No item is copied."},{"at":{"head":3,"next":1},"vars":{"slots":"50,_,_,40","size":2},"note":"poll() returns 30 from slot 2, moves head to (head + 1) % 4 = 3 and lowers size to 2. No item is copied."}]}
```

#### Deque Of Capacity Three

The second trace uses a deque with `cap = 3`. An add at the front moves `head` backward, and from index 0 that move lands on index 2 because of the added `cap`. After the three adds of 1, 2 and 3, the logical order is 2, 1, 3, but the array holds `[1, 3, 2]`. A removal at the front then returns 2 and moves `head` to index 0, and the rear read computes index `(0 + 2 - 1) % 3 = 1`.

```trace
{"cells":["0","1","2"],"pointers":["head","next"],"steps":[{"at":{"head":0,"next":0},"vars":{"slots":"_,_,_","size":0},"note":"The deque is empty: size is 0, head is 0 and next is 0."},{"at":{"head":0,"next":1},"vars":{"slots":"1,_,_","size":1},"note":"insertLast(1) writes slot (head + size) % 3 = 0 and size becomes 1."},{"at":{"head":2,"next":1},"vars":{"slots":"1,_,2","size":2},"note":"insertFront(2) moves head from 0 to (head - 1 + 3) % 3 = 2, writes slot 2 and size becomes 2."},{"at":{"head":2,"next":2},"vars":{"slots":"1,3,2","size":3},"note":"insertLast(3) writes slot (head + size) % 3 = 1 and size becomes 3."},{"at":{"head":0,"next":2},"vars":{"slots":"1,3,_","size":2},"note":"deleteFront() returns 2 from slot 2, moves head to 0 and lowers size to 2."},{"at":{"head":0,"next":2},"vars":{"slots":"1,3,_","size":2},"note":"getRear() reads slot (head + size - 1) % 3 = 1, which holds 3. No field changes."}]}
```

<!-- stage: code -->
### Writing The Queue With Two Fields

#### The Class

The class below stores `slots`, `head` and `size` and nothing else. Both methods compute positions with the modulo rule, and neither method copies an item. The return value -1 marks a rejected removal because the stored values are non-negative.

```java
final class IntRing {
    private final int[] slots;
    private int head;
    private int size;

    IntRing(int capacity) { slots = new int[capacity]; }

    // Adds v at the write position (head + size) % capacity; false when full.
    boolean offer(int v) {
        if (size == slots.length) return false;
        slots[(head + size) % slots.length] = v;
        size++;
        return true;
    }

    // Removes and returns the oldest value; -1 when empty.
    int poll() {
        if (size == 0) return -1;
        int v = slots[head];
        head = (head + 1) % slots.length;
        size--;
        return v;
    }
}
```

#### Cost And Java Details

- **offer** costs O(1) time and no extra space, because it writes one slot.
- **poll** costs O(1) time and no extra space, because it reads one slot and moves one index.
- **Memory** is O(cap) for the whole life of the queue, and it never grows.

The contract requires a capacity of at least 1, because the remainder operator with a divisor of 0 throws an `ArithmeticException` for ints. When the stored values are objects, a removal should also clear its slot so the array does not keep a stale reference.

<!-- stage: applicability -->
### When A Fixed Ring Fits

#### Recognizing The Pattern

Use a circular buffer when the capacity is fixed, items leave in arrival order, and the operations are add at the back and remove at the front, with a deque also allowing both ends. The statement often says "design a queue of size k", "keep only the last k items", or "drop the oldest when full". The state to name before coding is the invariant: the live positions are `(head + i) % cap` for `i < size`, and every method restores that statement before it returns.

Harder problems wrap more indexes around the same ring. A router that stores packets in arrival order and drops the oldest when memory is full still has this ring at its center, and it adds a set for duplicate checks and per-destination lists for counting.

#### Two False Friends

The pair of indices `head` and `tail` is a false friend. It looks like a complete description, yet equal values mean both empty and full, so correct code adds a spare slot or a flag and the bug returns when one branch forgets it.

The library class `ArrayDeque` is a second false friend. It uses the same wrapped array internally, yet it grows without limit and never rejects an add, so it cannot enforce a capacity by itself.

#### When Not To Use It

Do not use a fixed ring when the capacity is unknown, because growing it means copying live items into a new array in order. Do not use it when items leave from the middle, since the live positions would no longer form one run. Do not use it when removal order depends on priority and not on arrival.

<!-- stage: exercises -->
### Exercises

#### [Build] Ring Buffer (Author exercise)
<!-- id: sc-ring-buffer -->

**Prerequisites.** The head, size and wraparound rules from this lesson.

**Problem.** Implement a class `RingBuffer` with a fixed capacity. The constructor `RingBuffer(int capacity)` creates an empty buffer. The method `boolean offer(int v)` appends `v` at the back and returns `true`, or returns `false` and changes nothing when the buffer already holds `capacity` values. The method `int poll()` removes and returns the oldest value, or returns -1 when the buffer is empty. The method `int peek()` returns the oldest value without removing it, or -1 when empty. The method `int size()` returns the number of stored values.

**Constraints.** The limits are:
- **Capacity** is `1 <= capacity <= 1000`.
- **Values** are integers in `0..10^9`, so -1 never collides with a stored value.
- **Calls** number at most 5000 per buffer.
- **Storage** is one array of length `capacity` allocated in the constructor.

**Example 1.** Input: capacity 2 and the calls `offer(5)`, `offer(6)`, `offer(7)`, `poll()`, `offer(7)`, `poll()`, `poll()`, `poll()`. Output: `true, true, false, 5, true, 6, 7, -1`.

**Example 2.** Input: capacity 3 and the calls `offer(1)`, `offer(2)`, `offer(3)`, `poll()`, `poll()`, `offer(4)`, `offer(5)`, `peek()`, `size()`. Output: `true, true, true, 1, 2, true, true, 3, 3`.

**Hint.** Which two stored numbers locate the oldest value and the next free position, and what keeps both inside the array?

**Changed decision.** Basic case: the oldest value is located by a stored `head`, so removal moves an index and copies nothing.

#### [Vary] Design Circular Queue (LeetCode 622)
<!-- id: sc-circular-queue -->

**Prerequisites.** The Ring Buffer exercise above.

**Problem.** Implement `MyCircularQueue` with the constructor `MyCircularQueue(int k)`, which creates an empty queue of capacity `k`. The method `boolean enQueue(int value)` appends `value` and returns `true`, or returns `false` when the queue is full. The method `boolean deQueue()` removes the front value and returns `true`, or returns `false` when the queue is empty. The methods `int Front()` and `int Rear()` return the oldest and the newest value, or -1 when the queue is empty. The query `boolean isEmpty()` tells whether the queue holds no value, and `boolean isFull()` tells whether it holds `k` values.

**Constraints.** The limits are:
- **Capacity** is `1 <= k <= 1000`.
- **Values** are integers in `0..1000`.
- **Calls** number at most 3000 in total.
- **Empty reads** return -1 from `Front` and `Rear`.

**Example 1.** Input: capacity 3 and the calls `enQueue(7)`, `enQueue(8)`, `Front()`, `Rear()`, `deQueue()`, `deQueue()`, `deQueue()`, `Front()`, `Rear()`, `isEmpty()`. Output: `true, true, 7, 8, true, true, false, -1, -1, true`.

**Example 2.** Input: capacity 2 and the calls `enQueue(4)`, `enQueue(9)`, `enQueue(1)`, `deQueue()`, `enQueue(1)`, `Front()`, `Rear()`, `isFull()`. Output: `true, true, false, true, true, 9, 1, true`.

**Hint.** Which position holds the newest value when `size` is positive, and which condition on `size` replaces any comparison of two indices?

**Changed decision.** The output changes from one removal method to the full set of six queries, so `Rear` needs the position `(head + size - 1) % k`.

#### [Boundary] Design Circular Deque (LeetCode 641)
<!-- id: sc-circular-deque -->

**Prerequisites.** The Design Circular Queue exercise above.

**Problem.** Implement `MyCircularDeque` with the constructor `MyCircularDeque(int k)` for capacity `k`. The methods `boolean insertFront(int value)` and `boolean insertLast(int value)` add at the front or at the back and return `false` when the deque is full. The methods `boolean deleteFront()` and `boolean deleteLast()` remove from the front or the back and return `false` when the deque is empty. The methods `int getFront()` and `int getRear()` return the front or the back value, or -1 when empty. The queries `isEmpty()` and `isFull()` return a `boolean` that states whether the deque holds zero values or `k` values.

**Constraints.** The limits are:
- **Capacity** is `1 <= k <= 1000`, and capacity 1 is a legal and tested case.
- **Values** are integers in `0..1000`.
- **Calls** number at most 2000 in total.
- **Empty reads** return -1.

**Example 1.** Input: capacity 1 and the calls `insertFront(5)`, `insertLast(6)`, `getFront()`, `getRear()`, `isFull()`, `deleteLast()`, `isEmpty()`, `insertLast(6)`, `getFront()`, `deleteFront()`, `deleteFront()`. Output: `true, false, 5, 5, true, true, true, true, 6, true, false`.

**Example 2.** Input: capacity 3 and the calls `insertLast(1)`, `insertFront(2)`, `insertFront(3)`, `insertLast(4)`, `getFront()`, `getRear()`, `deleteLast()`, `insertLast(9)`, `getRear()`, `getFront()`. Output: `true, true, true, false, 3, 1, true, true, 9, 3`.

**Hint.** Which expression moves `head` back by one without a negative result, and what does that expression evaluate to when the capacity is 1?

**Changed decision.** The queue becomes a deque, so removal and insertion happen at both ends, and `head` moves backward by `(head - 1 + k) % k` on a front insertion.

#### [Recognize] Implement Router (LeetCode 3508)
<!-- id: sc-implement-router -->

**Prerequisites.** The Design Circular Deque exercise above.

**Problem.** Implement `Router` with the constructor `Router(int memoryLimit)`, which stores at most `memoryLimit` packets. A packet is the triple (`source`, `destination`, `timestamp`). The method `boolean addPacket(int source, int destination, int timestamp)` returns `false` and changes nothing when an identical triple is stored. Otherwise it removes the oldest packet first when the router is full, stores the new packet and returns `true`. The method `int[] forwardPacket()` removes the oldest packet and returns `[source, destination, timestamp]`, or returns an empty array when none is stored. The method `int getCount(int destination, int startTime, int endTime)` counts the stored packets with that destination and a timestamp in `[startTime, endTime]`.

**Constraints.** The limits are:
- **Memory limit** is `2 <= memoryLimit <= 10^5`.
- **Fields** satisfy `1 <= source, destination <= 2 * 10^5` and `1 <= timestamp <= 10^9`.
- **Order** requires that the `timestamp` of each `addPacket` call is at least that of the previous `addPacket` call.
- **Queries** satisfy `startTime <= endTime`, and the calls number at most `10^5`.

**Example 1.** Input: memory limit 3 and the calls `addPacket(1,4,10)`, `addPacket(2,4,11)`, `addPacket(1,4,10)`, `addPacket(3,5,12)`, `addPacket(4,4,13)`, `getCount(4,10,13)`, then four calls of `forwardPacket()`. Output: `true, true, false, true, true, 2, [2,4,11], [3,5,12], [4,4,13], []`.

**Example 2.** Input: memory limit 2 and the calls `addPacket(1,1,5)`, `addPacket(2,1,5)`, `addPacket(3,2,5)`, `addPacket(1,1,5)`, `getCount(1,5,5)`. Output: `true, true, true, true, 1`. The packet (1,1,5) is accepted the second time because eviction removed it from the router.

**Hint.** The ring decides which packet leaves. Which two extra indexes must be updated at that same moment so that duplicate checks and counts stay correct?

**Changed decision.** Each stored item gains an identity and a destination, so every eviction or forward must update the identity set and the destination list in the same call.
