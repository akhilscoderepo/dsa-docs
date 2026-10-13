<!-- lesson-kind: standard -->
<!-- lesson-id: split-containers -->
## Split Containers

<!-- stage: context -->
### Why Middle Inserts Slow A Queue

A music player keeps an up-next list. Listeners add a song to the front, add one in the middle, or append one at the back. The player also removes songs from all three places as the listener skips and reorders. With a few hundred songs this feels instant. A shared playlist of one hundred thousand songs with a stream of such edits makes every edit visibly slower than the last, even though each edit touches only one position.

Plain queues and deques serve the two ends well and cannot reach the middle without walking to it. A list reaches the middle by index and pays to shift everything behind it. The lesson asks one question. How can a structure serve the front, the middle and the back of a sequence, each in constant time?

<!-- stage: naive -->
### Keeping Everything In One List

The direct design stores the sequence in one `ArrayList`. The middle of a list of size `s` sits at a computable index, so each call is one list operation. A push inserts at index 0, at index `s / 2` or at the end. A pop removes the element at index 0, at index `(s - 1) / 2` or at the last index.

```java
static void pushFront(List<Integer> q, int v) { q.add(0, v); }
static void pushMiddle(List<Integer> q, int v) { q.add(q.size() / 2, v); }
static int popMiddle(List<Integer> q) { return q.isEmpty() ? -1 : q.remove((q.size() - 1) / 2); }
```

The code is short and always correct, and it needs no extra memory. The rule for an even size is part of the contract: the removed middle is the frontmost of the two middle elements, at index `(s - 1) / 2`.

<!-- stage: bottleneck -->
### Counting The Shifted Elements

```predict
A list receives 100 000 calls to `pushFront`, starting empty. About how many element moves does the list perform in total, and does `ArrayDeque` fix the middle calls?

About 5 billion moves, because the call that meets a list of size `s` shifts `s` elements, and the sizes run from 0 to 99 999. `ArrayDeque` makes `pushFront` constant time, but it has no insert or remove at an index, so a middle call would walk half of the elements.
```

Inserting at index `i` of an `ArrayList` of size `s` moves the `s - i` elements behind it. A front call moves all `s` elements, and a middle call moves about `s / 2`. Each call therefore costs O(s), and `q` calls cost O(q * s), which is quadratic when the list grows with the calls.

A linked list removes the shifting and adds a different cost, because reaching index `s / 2` means walking `s / 2` links. Both designs pay a linear price for the middle. The shifted elements are not the real waste. The real waste is that the structure forgets where the middle is after every call. A design that remembers the middle position and moves it by one place per call would avoid both prices.

<!-- stage: insight -->
### Two Containers Share The Sequence

#### Cut The Sequence At The Middle

Store the sequence as two deques placed end to end. The first deque holds the **left half**, and the second holds the **right half**. Read left to right, the left half followed by the right half is the logical sequence. The place where the two meet is the **boundary**, and it is the middle of the sequence.

<!-- names: halves, boundary, rebalance -->

For a sequence of size `s`, the left half holds exactly `s / 2` elements (integer division) and the right half holds the rest. The two halves therefore differ in size by at most one, and the right half is the larger one when `s` is odd. With this rule, the front of the sequence is the first element of the left half, the back is the last element of the right half, and the middle sits at the boundary. Every end of interest is an end of a deque.

#### Move One Element To Rebalance

Each push or pop changes the size by one, so the rule `left = s / 2` can break by one element only. A **rebalance** moves one element across the boundary. If the left half is longer than the right half, its last element moves to the front of the right half. If the right half has two more elements than the left half, its first element moves to the back of the left half. The order of the logical sequence does not change, because the element stays next to the boundary on both sides of the move.

A middle push inserts at index `s / 2`, which is the end of the left half. A middle pop removes index `(s - 1) / 2`. For an even `s` that is the last element of the left half, and for an odd `s` it is the first element of the right half. Each call is one deque operation plus at most one rebalance move, so each call costs O(1).

<!-- stage: variables -->
### State Kept In The Two Halves

The structure keeps two fields and no counters, because `ArrayDeque.size()` already reports each length in constant time.

- **left** is the deque that holds the first `s / 2` elements, in sequence order.
- **right** is the deque that holds the last `s - s / 2` elements, in sequence order.
- **s** is the total size, equal to `left.size() + right.size()`.
- **boundary** is the index `left.size()`, the first index that belongs to the right half.

The state invariant is that `right.size() - left.size()` is 0 or 1 after every public call returns. During a call the difference can be off by one for a moment, and only the private rebalance method repairs it. No public method moves elements between the halves on its own, which keeps that repair in one place.

<!-- stage: trace -->
### Tracing Inserts And Removals

#### Building A Sequence From Both Ends

The first trace starts from an empty sequence and applies `pushBack(10)`, `pushBack(20)`, `pushFront(5)`, `pushMiddle(15)` and `pushMiddle(25)`. The cells show the final sequence, and the pointer `b` is the boundary at each step, so it counts the elements in the left half. The variable `seq` lists the sequence at that step.

The first `pushBack(10)` puts 10 in the right half, and the right half may hold one more element than the left half, so no move follows. The call `pushBack(20)` makes the right half two elements longer, so 10 moves to the left half. The call `pushFront(5)` makes the left half longer than the right half, so 10 moves back. Then `pushMiddle(15)` adds to the end of the left half and leaves both halves with two elements. The last call `pushMiddle(25)` makes the left half longer, and 25 crosses the boundary. The sequence ends as 5, 15, 25, 10, 20.

```trace
{"cells":["5","15","25","10","20"],"pointers":["b"],"steps":[{"at":{"b":0},"vars":{"seq":"","left":0,"right":0},"note":"Both halves are empty, so the boundary b is 0."},{"at":{"b":0},"vars":{"seq":"10","left":0,"right":1},"note":"pushBack(10) inserts 10; the sequence is now 10."},{"at":{"b":0},"vars":{"seq":"10,20","left":0,"right":2},"note":"pushBack(20) inserts 20; the sequence is now 10,20."},{"at":{"b":1},"vars":{"seq":"10,20","left":1,"right":1},"note":"The right half is two elements longer, so 10 moves from the front of the right half to the end of the left half."},{"at":{"b":2},"vars":{"seq":"5,10,20","left":2,"right":1},"note":"pushFront(5) inserts 5; the sequence is now 5,10,20."},{"at":{"b":1},"vars":{"seq":"5,10,20","left":1,"right":2},"note":"The left half is longer, so 10 moves from the end of the left half to the front of the right half."},{"at":{"b":2},"vars":{"seq":"5,15,10,20","left":2,"right":2},"note":"pushMiddle(15) inserts 15; the sequence is now 5,15,10,20."},{"at":{"b":3},"vars":{"seq":"5,15,25,10,20","left":3,"right":2},"note":"pushMiddle(25) inserts 25; the sequence is now 5,15,25,10,20."},{"at":{"b":2},"vars":{"seq":"5,15,25,10,20","left":2,"right":3},"note":"The left half is longer, so 25 moves from the end of the left half to the front of the right half."}]}
```

#### Removing From The Front, Middle And Back

The second trace starts from the sequence 1 to 6, with 1, 2, 3 in the left half and 4, 5, 6 in the right half. It applies `popFront` twice, then `popMiddle`, `popBack` and `popMiddle` twice. The cells show the starting sequence, and `b` is the boundary.

The first `popFront` removes 1, and the sizes 2 and 3 already satisfy the rule. The second `popFront` removes 2 and leaves one element on the left, so 4 moves across. The call `popMiddle` sees an even size, so it removes the last element of the left half, which is 4. The call `popBack` removes 6. The next `popMiddle` meets an even size again and removes 3, which empties the left half. The last `popMiddle` meets size one and takes the first element of the right half, 5. A pop from the right half is always possible while the sequence is non-empty, because that half is never smaller than the left half.

```trace
{"cells":["1","2","3","4","5","6"],"pointers":["b"],"steps":[{"at":{"b":3},"vars":{"seq":"1,2,3,4,5,6","left":3,"right":3},"note":"Start: left half 1,2,3 and right half 4,5,6, so the boundary b is 3."},{"at":{"b":2},"vars":{"seq":"2,3,4,5,6","left":2,"right":3},"note":"popFront returns 1. The sizes already satisfy the rule."},{"at":{"b":2},"vars":{"seq":"3,4,5,6","left":2,"right":2},"note":"popFront returns 2. The sizes now differ by two, so one element crosses the boundary."},{"at":{"b":1},"vars":{"seq":"3,5,6","left":1,"right":2},"note":"popMiddle returns 4. The sizes already satisfy the rule."},{"at":{"b":1},"vars":{"seq":"3,5","left":1,"right":1},"note":"popBack returns 6. The sizes already satisfy the rule."},{"at":{"b":0},"vars":{"seq":"5","left":0,"right":1},"note":"popMiddle returns 3. The sizes already satisfy the rule."},{"at":{"b":0},"vars":{"seq":"","left":0,"right":0},"note":"popMiddle returns 5. The sizes already satisfy the rule."}]}
```

<!-- stage: code -->
### Implementing The Six Calls

#### The Class With One Rebalance Method

The code below keeps the two halves in `ArrayDeque` fields. The private method `shiftBoundary` performs the rebalance from the insight, and every public method calls it last. The names `leftHalf` and `rightHalf` mean the left half and the right half.

```java
final class SplitQueue {
    private final Deque<Integer> leftHalf = new ArrayDeque<>();
    private final Deque<Integer> rightHalf = new ArrayDeque<>();

    // The only method that moves an element between the halves.
    private void shiftBoundary() {
        if (leftHalf.size() > rightHalf.size()) rightHalf.addFirst(leftHalf.removeLast());
        else if (rightHalf.size() > leftHalf.size() + 1) leftHalf.addLast(rightHalf.removeFirst());
    }

    void pushFront(int v)  { leftHalf.addFirst(v); shiftBoundary(); }
    void pushMiddle(int v) { leftHalf.addLast(v);  shiftBoundary(); }
    void pushBack(int v)   { rightHalf.addLast(v); shiftBoundary(); }

    int popFront() {
        if (rightHalf.isEmpty()) return -1;
        int v = leftHalf.isEmpty() ? rightHalf.removeFirst() : leftHalf.removeFirst();
        shiftBoundary();
        return v;
    }

    int popMiddle() {
        if (rightHalf.isEmpty()) return -1;
        int v = leftHalf.size() == rightHalf.size() ? leftHalf.removeLast() : rightHalf.removeFirst();
        shiftBoundary();
        return v;
    }

    int popBack() {
        if (rightHalf.isEmpty()) return -1;
        int v = rightHalf.removeLast();
        shiftBoundary();
        return v;
    }
}
```

#### Cost And Java Details

- **Every call** costs O(1) time, because it makes one or two deque operations and at most one move.
- **Memory** is O(n) for the elements and O(1) beyond them.

The empty test in every pop reads only `rightHalf`. That is enough because the invariant keeps `rightHalf` at least as long as `leftHalf`, so it is empty only when the whole sequence is empty. The methods `removeFirst` and `removeLast` throw `NoSuchElementException` on an empty deque, so the guard must run before them.

<!-- stage: applicability -->
### When To Split A Sequence

#### Recognizing The Pattern

Use two containers when the operations name several fixed logical positions, such as the front, the middle and the back, and each call changes the size by one. The cue is a statement that asks for a push or pop "in the middle" at constant cost. Before writing code, state the invariant in words: the left half holds `s / 2` elements, the sequence is the left half followed by the right half, and one private method restores that after each call. Then decide which middle a pop removes when the size is even, and write that choice into a test.

The same idea covers a second family of problems that look different. A set of bounded stacks needs the leftmost stack with free space, and the rightmost stack with an element. Each of the two questions, which stack is writable and which stack holds an element, needs its own ordered index, and the two indexes must stay consistent after every call.

#### The False Friend

A single `ArrayDeque` looks sufficient, because it serves both ends in constant time. It is a false friend. The `Deque` interface has no access by index, so reaching the middle means iterating over half of the elements. A doubly linked list with a pointer to the middle node also works, but every end call must also move that pointer, and the even-size rule must be applied in each of six methods. Two deques keep that rule in one method.

#### When Not To Use It

Do not split when the operations insert at arbitrary indexes, because the boundary then needs to jump far, and an order-statistic tree or a rope serves that case. Do not split when only the two ends are used, since one `ArrayDeque` is simpler. Do not split when the calls must run from several threads, because a move between the halves is two operations that another thread could observe half-finished.

<!-- stage: exercises -->
### Exercises

#### [Build] Balanced Two-Deque Sequence (Author exercise)
<!-- id: sc-split-balanced-sequence -->

**Prerequisites.** The left half, the right half and the single rebalance move from this lesson.

**Problem.** Implement a class `BalancedSequence` that stores a sequence of integers in two deques, `left` followed by `right`. It supports `pushFront(v)`, which inserts `v` before every element, and `pushBack(v)`, which inserts `v` after every element. The method `sizes()` returns the array `{left.size(), right.size()}`, and `toArray()` returns the whole sequence in order. After every call, `right.size() - left.size()` must be 0 or 1.

**Constraints.** The limits are:
- **Calls** number at most 10^5, and `v` is any `int`.
- **Empty sequence** returns `{0, 0}` from `sizes()` and an empty array from `toArray()`.
- **Balance** holds after each call, not only at the end.
- **Values** `v` are stored as given, with duplicates allowed.

**Example 1.** Input calls `pushBack(1)`, `pushBack(2)`, `pushFront(0)`, `pushBack(3)`. Output `toArray()` is `[0,1,2,3]` and `sizes()` is `[2,2]`.

**Example 2.** Input calls `pushFront(7)`, `pushFront(6)`, `pushBack(8)`, `pushBack(9)`, `pushBack(10)`. Output `toArray()` is `[6,7,8,9,10]` and `sizes()` is `[2,3]`. The right half holds the extra element.

**Hint.** After one insertion the sizes are off by one. Which end of which deque crosses the boundary to repair each of the two kinds of imbalance?

**Changed decision.** Basic case: the sequence is split at the middle once, and each end insertion triggers at most one rebalance move.

#### [Vary] Design Front Middle Back Queue (LeetCode 1670)
<!-- id: sc-split-front-middle-back -->

**Prerequisites.** The Balanced Two-Deque Sequence exercise above.

**Problem.** Implement a queue with six operations. The calls `pushFront(val)`, `pushMiddle(val)` and `pushBack(val)` insert `val` at index 0, at index `size / 2` and at index `size`. The calls `popFront()`, `popMiddle()` and `popBack()` remove and return the element at index 0, at index `(size - 1) / 2` and at index `size - 1`. Each pop returns -1 when the queue is empty. When the size is even, `popMiddle` removes the frontmost of the two middle elements.

**Constraints.** The limits are:
- **Calls** number at most 1000, and `1 <= val <= 10^9`.
- **Empty queue** returns -1 from every pop.
- **Even size** removes the element at index `size / 2 - 1` in `popMiddle`.
- **Insertion** at the middle uses index `size / 2` before the insertion.

**Example 1.** Input calls `pushFront(1)`, `pushBack(2)`, `pushBack(3)`, `pushMiddle(4)`, `pushMiddle(5)` build `[1,4,5,2,3]`. Then `popMiddle`, `popMiddle`, `popFront`, `popBack`, `popMiddle`, `popMiddle` give the output `5, 4, 1, 3, 2, -1`.

**Example 2.** Input calls `pushFront(1)`, `pushBack(2)`, `pushMiddle(3)`, `pushMiddle(4)` build `[1,4,3,2]`. Then `popMiddle`, `popBack`, `popFront`, `popMiddle` give the output `4, 2, 1, 3`. The first pop removes 4, the frontmost of the two middle elements.

**Hint.** Which half ends at index `size / 2` before a middle push, and which half holds the element at index `(size - 1) / 2` for each parity of the size?

**Changed decision.** The contract adds three removals and a fixed choice of middle for even sizes, so the middle moves in both directions.

#### [Boundary] Oscillating Empty Halves (Author exercise)
<!-- id: sc-split-oscillating -->

**Prerequisites.** The Design Front Middle Back Queue exercise above.

**Problem.** A sequence starts empty. The array `ops` lists operations in order: a positive value `v` inserts `v` at index `size / 2`, and the value 0 removes the element at index `(size - 1) / 2`. Return an array of the removed values in the order of removal, using -1 for a removal from an empty sequence. Keep the sequence in two deques whose sizes differ by at most one after every operation, including when the sequence becomes empty and refills.

**Constraints.** The limits are:
- **Operations** number at most 10^5, and `1 <= v <= 10^9`.
- **Empty input** returns an empty array.
- **Removal from empty** appends -1 and changes no state.
- **Balance** holds after each operation, including at size 0 and size 1.

**Example 1.** Input `ops = [1,2,0,0,0,3,0]`, output `[2,1,-1,3]`. The sequence after the first two inserts is `[2,1]`, and it empties and refills once.

**Example 2.** Input `ops = [1,2,3,4,0,0,0,0,0]`, output `[4,3,2,1,-1]`. The sequence `[2,4,3,1]` shrinks one middle element at a time.

**Hint.** At size 1 the left half is empty. Which half supplies the middle, and what does the next insertion see when both halves are empty?

**Changed decision.** The workload shifts from growth to repeated removal at the boundary, so the empty and single-element states are visited many times.

#### [Recognize] Dinner Plate Stacks (LeetCode 1172)
<!-- id: sc-split-dinner-plates -->

**Prerequisites.** The Oscillating Empty Halves exercise above.

**Problem.** Implement `DinnerPlates(capacity)`, an unbounded row of stacks numbered from 0, each holding at most `capacity` values. The call `push(val)` places `val` on the stack with the smallest index that is not full. The call `pop()` removes and returns the top value of the stack with the largest index that is not empty, or -1 when all stacks are empty. The call `popAtStack(index)` removes and returns the top value of stack `index`, or -1 when that stack is empty or `index` is beyond every stack used so far.

**Constraints.** The limits are:
- **Capacity** is `1 <= capacity <= 2 * 10^4`.
- **Values** satisfy `1 <= val <= 2 * 10^4`.
- **Index** satisfies `0 <= index <= 10^5`.
- **Calls** number at most 2 * 10^5.

**Example 1.** Input `capacity = 2` and pushes of 1 to 5, which build `[1,2]`, `[3,4]`, `[5]`. The call `popAtStack(0)` returns 2, then `push(20)` and `push(21)` fill stack 0 and stack 2. The calls `pop`, `popAtStack(1)`, `pop`, `pop`, `pop`, `pop` give the output `21, 4, 5, 3, 20, 1`.

**Example 2.** Input `capacity = 1` and pushes of 7 and 8, which build `[7]`, `[8]`. The call `popAtStack(0)` returns 7, and `push(9)` refills stack 0. Then `popAtStack(5)`, `pop`, `pop`, `pop` give the output `-1, 8, 9, -1`.

**Hint.** Which index must a push find, and which must a pop find? State the order of each index set and how an entry leaves it before choosing a `TreeSet` or a `PriorityQueue`.

**Changed decision.** There is no single middle. Two ordered positions, the leftmost writable stack and the rightmost non-empty stack, play the role of the boundary.
