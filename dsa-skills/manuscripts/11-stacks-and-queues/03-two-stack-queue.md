<!-- lesson-kind: standard -->
<!-- lesson-id: two-stack-queue -->
## Build A Queue From Two Stacks

<!-- stage: context -->
### A Job Runner With Only A Stack

A firmware library gives a developer one container for pending jobs, and that container is a stack. The runner must start jobs in the order they arrive. The developer calls `push` for each new job and `pop` to pick the next one. The `pop` call returns the job that arrived last, so a burst of new jobs keeps pushing the first job further down. The first job never starts while new jobs keep coming.

The runner needs a first-in first-out queue, and the library offers only last-in first-out access. The developer may create more than one stack. How do two stacks produce the arrival order, and how many element moves does each call cost?

<!-- stage: naive -->
### Dig Out The Bottom Element Each Time

The direct idea keeps all jobs in one stack. To remove the oldest job, the code pops every job into a second stack, pops the last one, and pushes the others back.

```java
final class SlowQueue {
    private final java.util.ArrayDeque<Integer> main = new java.util.ArrayDeque<>();
    private final java.util.ArrayDeque<Integer> spare = new java.util.ArrayDeque<>();

    void enqueue(int v) { main.push(v); }

    int dequeue() {
        while (main.size() > 1) spare.push(main.pop());
        int oldest = main.pop();
        while (!spare.isEmpty()) main.push(spare.pop());
        return oldest;
    }
}
```

This code is correct. With the jobs 4, 7 and 9 enqueued in that order, `dequeue` returns 4, then 7, then 9. Every `dequeue` on a queue of `k` jobs pops `k - 1` jobs out and pushes `k - 1` jobs back.

<!-- stage: bottleneck -->
### Every Removal Walks The Whole Stack

```predict
A queue receives 5 jobs and then serves all 5. The slow queue above counts one move per `push` onto `spare` and one move per `push` back onto `main`. How many moves does it make in total?

It makes 20 moves. Serving a queue of size k costs 2(k - 1) moves, and the sizes 5, 4, 3, 2, 1 give 8 + 6 + 4 + 2 + 0 = 20. For n jobs the total is n(n - 1).
```

The slow queue makes 2(k - 1) moves for a queue of size `k`, so one `dequeue` costs O(n) time. Serving `n` jobs costs n(n - 1) moves in total, which is O(n^2). For 100,000 jobs that is about ten billion moves.

Most of that work repeats. The first `dequeue` reverses the order of the whole stack and the code immediately reverses it back. The second `dequeue` starts by reversing the same jobs again. The code needs to keep the reversed order instead of undoing it.

<!-- stage: insight -->
### Keep The Reversed Order And Reuse It

Popping all values from one stack onto a second stack reverses their order. After a **reversal**, the value that arrived first lies on top of the second stack. That top value is exactly the next value a queue must return. So the second stack already holds the answer to `dequeue`, as long as the code leaves it alone.

#### Two Stacks With Two Roles

Use a stack named `in` for arrivals and a stack named `out` for departures. The call `enqueue` pushes onto `in`. The call `dequeue` pops from `out`. The values in `out` stay in arrival order from top to bottom, and every value in `in` arrived after every value in `out`.

<!-- names: transfer, amortized, reversal -->

#### Transfer Only When Out Is Empty

When `out` is empty and a call needs a value, the code runs a **transfer**. It pops every value from `in` and pushes it onto `out`. The transfer happens only when `out` is empty. If `out` still held values, pushing more onto it would place newer values above older ones and break the order.

#### Each Value Moves At Most Twice

A value is pushed onto `in` once, moves to `out` once, and is popped from `out` once. That bounds the work per value by a constant. The cost per call is **amortized** O(1), which means the total cost of any sequence of `m` calls is O(m), even though one `dequeue` that triggers a transfer costs O(n).

<!-- stage: variables -->
### What The Two Stacks Hold

The queue keeps two stacks and no other state.

- **in** is the stack that receives every `enqueue`, and its top is the newest value.
- **out** is the stack that serves `dequeue` and `peek`, and its top is the oldest value in the whole queue.
- **size** is `in.size() + out.size()`, and it is zero exactly when both stacks are empty.
- **moves** is a count of values pushed from `in` onto `out`, and it never exceeds the number of `enqueue` calls.

The stack `in` changes on every `enqueue` and empties on every transfer. The stack `out` changes only when a transfer refills it or a `dequeue` pops it.

<!-- stage: trace -->
### Following Values Between The Stacks

#### Arrivals Followed By Removals

The first trace enqueues 4, 7 and 9 and then dequeues three times. Stack contents are listed from bottom to top. The pointer `next` counts how many of the cells have been enqueued.

The three enqueues fill `in` with 4, 7, 9. The first `dequeue` finds `out` empty, so it moves 9, 7 and 4 in that order, and `out` holds 9, 7, 4 with 4 on top. The call returns 4. The next two calls pop 7 and 9 directly, with no further moves.

```trace
{"cells":[4,7,9],"pointers":["next"],"steps":[{"at":{"next":1},"vars":{"in":"[4]","out":"[]","moves":0},"note":"enqueue(4) pushes 4 onto in."},{"at":{"next":2},"vars":{"in":"[4, 7]","out":"[]","moves":0},"note":"enqueue(7) pushes 7 onto in."},{"at":{"next":3},"vars":{"in":"[4, 7, 9]","out":"[]","moves":0},"note":"enqueue(9) pushes 9 onto in."},{"at":{"next":3},"vars":{"in":"[]","out":"[9, 7]","moves":3},"note":"out is empty, so 3 value(s) move from in to out. dequeue() pops 4 from out."},{"at":{"next":3},"vars":{"in":"[]","out":"[9]","moves":3},"note":"dequeue() pops 7 from out."},{"at":{"next":3},"vars":{"in":"[]","out":"[]","moves":3},"note":"dequeue() pops 9 from out."}]}
```

#### Arrivals Between Removals

The second trace enqueues 4, 7 and 9, calls `dequeue`, enqueues 2, and then calls `dequeue` three more times. The value 2 lands in `in` while `out` still holds 9 and 7. The second and third `dequeue` calls pop 7 and then 9 without a transfer, so 2 stays behind 9. The last `dequeue` finds `out` empty and moves 2 across, and it returns 2 as the newest value.

```trace
{"cells":[4,7,9,2],"pointers":["next"],"steps":[{"at":{"next":1},"vars":{"in":"[4]","out":"[]","moves":0},"note":"enqueue(4) pushes 4 onto in."},{"at":{"next":2},"vars":{"in":"[4, 7]","out":"[]","moves":0},"note":"enqueue(7) pushes 7 onto in."},{"at":{"next":3},"vars":{"in":"[4, 7, 9]","out":"[]","moves":0},"note":"enqueue(9) pushes 9 onto in."},{"at":{"next":3},"vars":{"in":"[]","out":"[9, 7]","moves":3},"note":"out is empty, so 3 value(s) move from in to out. dequeue() pops 4 from out."},{"at":{"next":4},"vars":{"in":"[2]","out":"[9, 7]","moves":3},"note":"enqueue(2) pushes 2 onto in."},{"at":{"next":4},"vars":{"in":"[2]","out":"[9]","moves":3},"note":"dequeue() pops 7 from out."},{"at":{"next":4},"vars":{"in":"[2]","out":"[]","moves":3},"note":"dequeue() pops 9 from out."},{"at":{"next":4},"vars":{"in":"[]","out":"[]","moves":4},"note":"out is empty, so 1 value(s) move from in to out. dequeue() pops 2 from out."}]}
```

<!-- stage: code -->
### Writing The Two Stack Queue

#### The Class

The class below keeps `in` and `out` as `ArrayDeque` stacks. The private method `shift` runs the transfer and runs only when `out` is empty. A call on an empty queue throws `NoSuchElementException`, which is the behavior of `ArrayDeque.pop` itself.

```java
final class TwoStackQueue {
    private final java.util.ArrayDeque<Integer> in = new java.util.ArrayDeque<>();
    private final java.util.ArrayDeque<Integer> out = new java.util.ArrayDeque<>();

    void enqueue(int v) { in.push(v); }

    private void shift() {
        if (!out.isEmpty()) return;
        while (!in.isEmpty()) out.push(in.pop());
    }

    int dequeue() { shift(); return out.pop(); }

    int peek() { shift(); return out.peek(); }

    boolean isEmpty() { return in.isEmpty() && out.isEmpty(); }
}
```

#### The Cost

Each value is pushed twice and popped twice over its lifetime, once on `in` and once on `out`. A sequence of `m` calls runs in O(m) time. The two stacks together hold at most `n` values, so the space is O(n). In `peek`, the call `out.peek()` returns `null` on empty `out`, and unboxing that value into `int` throws `NullPointerException` instead of `NoSuchElementException`. The exercises state which failure to use.

<!-- stage: applicability -->
### Deciding When Two Stacks Are Enough

#### The Invariant To Protect

The invariant is that `out` holds the oldest values in arrival order and `in` holds newer values, so every value in `in` arrived after every value in `out`. The only operation that can break it is a transfer onto a nonempty `out`. A review of any two-stack queue starts with that one condition.

#### False Friend And Limits

Moving everything between the stacks on every call is a false friend. It returns correct values, so tests pass, but each call costs O(n) and a long run costs O(n^2). Another false friend is a monotonic queue, which also holds values in a deque. A monotonic queue discards dominated values, while this queue keeps every value, so it is plain first-in first-out emulation.

Use two stacks when the platform offers only stack operations. Do not use them when a single call must finish within a hard time bound. One `dequeue` still costs O(n) when it triggers a transfer. An `ArrayDeque` used directly as a queue has amortized O(1) calls for each operation without any transfer, and it is the better choice whenever Java is available.

<!-- stage: exercises -->
### Exercises

#### [Build] Enqueue And One Dequeue (Author exercise)
<!-- id: sq-enqueue-one-dequeue -->

**Prerequisites.** The roles of `in` and `out` and the transfer in this lesson.

**Problem.** A stack `in` starts empty and receives the values of the array `values` in order, so the last value is on top. Move every value from `in` onto a stack `out` by popping `in` and pushing `out`. Then pop one value from `out`. Return an array with the popped value first, followed by the remaining values of `out` from top to bottom.

**Constraints.** The limits are:
- **Length** is `1 <= values.length <= 10^4`.
- **Values** are `int` values and may repeat.
- **Return** is an `int[]` of the same length as `values`.
- **Mutation** is not allowed; the input array stays unchanged.

**Example 1.** Input `[5,8,2]`, output `[5,8,2]`. The first value is on top of `out` after the transfer.

**Example 2.** Input `[3,3,9,1]`, output `[3,3,9,1]`.

**Hint.** What order does a pop from `in` followed by a push onto `out` give? Which value ends on top?

**Changed decision.** The code builds both stacks explicitly and observes the order instead of copying the input.

#### [Vary] Interleaved Queue Calls (Author exercise)
<!-- id: sq-interleaved-queue-calls -->

**Prerequisites.** The exercise above and the rule that a transfer needs an empty `out`.

**Problem.** A queue starts empty. The array `ops` lists calls in order. A row `{1, v}` enqueues the value `v`. A row `{0}` dequeues the oldest value. Return the dequeued values in the order of the calls. Implement the queue with two stacks and transfer only when `out` is empty.

**Constraints.** The limits are:
- **Length** is `0 <= ops.length <= 10^5`.
- **Values** are `int` values `v` with `0 <= v <= 10^9`.
- **Validity** means the queue is nonempty at every dequeue row.
- **Return** is an `int[]` with one entry per dequeue row.

**Example 1.** Input `[[1,4],[1,7],[0],[1,2],[0],[0]]`, output `[4,7,2]`.

**Example 2.** Input `[[1,6],[0],[1,1],[1,5],[0],[0]]`, output `[6,1,5]`.

**Hint.** When `out` is nonempty and a new value arrives, which stack receives it? Which value must stay on top of `out`?

**Changed decision.** New values arrive while `out` holds older values, and the code must leave `out` untouched.

#### [Boundary] Empty Queue API (Author exercise)
<!-- id: sq-empty-queue-api -->

**Prerequisites.** The two exercises above.

**Problem.** A two-stack queue stores non-negative integers. The array `ops` lists calls in order. A row `{1, v}` enqueues `v`. A row `{2}` dequeues the oldest value. A row `{3}` returns the oldest value without removing it. Return one result per row `{2}` or `{3}`. When the queue is empty at such a row, the result is `-1` and the queue stays unchanged.

**Constraints.** The limits are:
- **Length** is `0 <= ops.length <= 10^5`.
- **Values** are `int` values `v` with `0 <= v <= 10^9`.
- **Empty calls** are allowed and give `-1`.
- **Return** is an `int[]`, empty when no row asks for a value.

**Example 1.** Input `[[2],[1,8],[3],[2],[3]]`, output `[-1,8,8,-1]`.

**Example 2.** Input `[[1,5],[1,6],[3],[3],[2],[2],[2]]`, output `[5,5,5,6,-1]`.

**Hint.** Where can the oldest value sit when `out` is empty but `in` is not? Which stack must a peek read after the empty check?

**Changed decision.** Empty calls return a sentinel, and a peek must not change which stack holds the oldest value.

#### [Recognize] Implement Queue Using Stacks (LeetCode 232)
<!-- id: sq-implement-queue-stacks -->

**Prerequisites.** All three exercises above.

**Problem.** Implement a first-in first-out queue that supports `push(x)`, `pop()`, `peek()` and `empty()` using only stack operations on two stacks. The array `ops` lists calls in order: `{0, x}` is `push(x)`, `{1}` is `pop()`, `{2}` is `peek()` and `{3}` is `empty()`. Return one result per row `{1}`, `{2}` or `{3}`. A `pop` or `peek` returns the value, and `empty` returns 1 when the queue is empty and 0 otherwise. Each value must move from `in` to `out` at most once.

**Constraints.** The limits are:
- **Length** is `0 <= ops.length <= 10^5`.
- **Values** are `int` values `x` with `1 <= x <= 100`.
- **Validity** means the queue is nonempty at every `pop` and `peek` row.
- **Return** is an `int[]` with one entry per `pop`, `peek` and `empty` row.

**Example 1.** Input `[[0,3],[0,8],[2],[1],[3],[1],[3]]`, output `[3,3,0,8,1]`.

**Example 2.** Input `[[3],[0,6],[0,2],[1],[0,9],[1],[1],[3]]`, output `[1,6,2,9,1]`.

**Hint.** Count the pushes onto `out` over the whole run. Which call performs them, and when?

**Changed decision.** The full API appears together, and the solution proves the move count stays at most the number of pushes.
