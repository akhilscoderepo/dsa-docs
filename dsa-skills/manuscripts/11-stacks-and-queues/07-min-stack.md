<!-- lesson-kind: standard -->
<!-- lesson-id: min-stack -->
## Track The Minimum In A Stack

<!-- stage: context -->
### A Monitor That Slows As It Fills

A monitor tracks the open calls of a running program. When a call starts, the monitor pushes the number of bytes that the call allocated onto a stack. When the call ends, the monitor pops that number. After every event the monitor must show the smallest byte count among the calls that are still open. A scan answers that question by reading every open call. A deeply recursive program with many thousands of open calls makes every event cost many thousands of reads.

The stack operations themselves are fast. Pushing and popping at one end costs O(1) each. The slow part is the question about the smallest value. The lesson answers one question. How can a stack return its current minimum in constant time after every push and every pop?

<!-- stage: naive -->
### Scan The Stack On Every Question

The direct approach keeps a normal `ArrayDeque` stack and answers each minimum question by reading every value that is currently on the stack.

```java
static int minByScan(ArrayDeque<Integer> stack) {
    int best = Integer.MAX_VALUE;
    for (int v : stack) {
        best = Math.min(best, v);
    }
    return best;
}
```

The method is correct. It always reflects the stack after the latest push or pop, because it reads the stack itself and keeps no copy. A stack that holds 5, 3 and 7 from bottom to top returns 3. After the 7 is popped, the call still returns 3. After the 3 is popped as well, the call returns 5, because the scan sees only what remains.

<!-- stage: bottleneck -->
### The Scan Rereads Settled Answers

```predict
A stack already holds 100000 values. The program then pushes 100000 more values and calls the scan once after each push. About how many values does the scan read in total?

About 1.5 x 10^10 reads. The call after push k reads 100000 + k values, and the sum over 100000 pushes is 100000 x 100000 + 100000 x 100001 / 2.
```

The scan costs O(n) for a stack of size `n`. A program that asks `q` questions on a stack of that size pays O(n * q) in total. The cost grows with the product, so doubling both the stack and the number of questions multiplies the work by four.

Most of that work repeats earlier work. Before a push, the scan already established the minimum of every value below the new one. The next scan reads those same values again and reaches the same conclusion about them. The values below the top do not change while they stay on the stack. Only the single new value is new information, yet the scan reads everything.

<!-- stage: insight -->
### Store The Answer Next To Each Value

The values below the top never change, so their minimum never changes either. The stack can save that answer once and read it later.

<!-- names: prefix minimum, value-min pair, helper stack -->

#### Each Depth Has A Fixed Prefix Minimum

Number the stack positions from the bottom. The **prefix minimum** at position `k` is the smallest value among positions 1 through `k`. A push at position `k` does not touch positions below it. So the prefix minimum at position `k` equals the smaller of the new value and the prefix minimum at position `k - 1`. A pop removes position `k` together with its answer, and the prefix minimum of the new top is already stored there. The invariant is that every position holds the correct prefix minimum for exactly the values at or below it.

#### One Value-Min Pair Per Position

The simplest way to store the answer is a **value-min pair**. Each stack entry holds the value and the prefix minimum at its position. A push builds the pair from the value and the minimum of the current top, or from the value alone when the stack is empty. The `top` operation reads the value of the top pair. The `getMin` operation reads the minimum of the top pair. Every operation touches only the top entry, so each costs O(1) in the worst case.

#### A Helper Stack Saves Space

The pair repeats the same minimum at many positions. A **helper stack** stores a minimum only when a new one appears. A pushed value goes onto the helper stack when it is less than or equal to the current minimum. A popped value leaves the helper stack when it equals the helper's top. The comparison must be less than or equal, so a duplicate of the minimum gets its own entry. Without it, popping one copy of the minimum would delete the answer while another copy remains.

<!-- stage: variables -->
### What Each Stack Entry Stores

The structure tracks three pieces of state.

- **main stack** holds every pushed value in push order, and `pop` and `top` read it.
- **prefix minimum** is the smallest value from the bottom up to one position, and it changes only when that position is created.
- **helper stack** holds the distinct minimum levels, with one extra entry for each duplicate, and its top equals the current minimum.

The value-min pair design merges the first two items into one entry. The helper stack design keeps them apart and stores the prefix minimum only where it changes.

<!-- stage: trace -->
### Following Pushes And Pops

#### Value-Min Pairs Over Four Pushes

The first trace pushes the values 5, 3, 7 and 3 in this order, and then pops all four. The cells are the pushed values, and the pointer `in` marks the value being pushed. During the pops the pointer rests past the last cell. Each step lists the stack from bottom to top as pairs of value and prefix minimum.

The push of 3 stores the pair 3 with minimum 3, because 3 is smaller than 5. The push of 7 stores minimum 3, copied from the pair below. The second push of 3 stores minimum 3 again. Each pop then restores the answer of the pair underneath without any scan. After the third pop, the top pair is again 5 with minimum 5.

```trace
{"cells":[5,3,7,3],"pointers":["in"],"steps":[{"at":{"in":0},"vars":{"pairs":"[5/5]","min":5},"note":"push(5) stores the pair 5 with minimum 5."},{"at":{"in":1},"vars":{"pairs":"[5/5, 3/3]","min":3},"note":"push(3) stores the pair 3 with minimum 3."},{"at":{"in":2},"vars":{"pairs":"[5/5, 3/3, 7/3]","min":3},"note":"push(7) stores the pair 7 with minimum 3."},{"at":{"in":3},"vars":{"pairs":"[5/5, 3/3, 7/3, 3/3]","min":3},"note":"push(3) stores the pair 3 with minimum 3."},{"at":{"in":4},"vars":{"pairs":"[5/5, 3/3, 7/3]","min":3},"note":"pop() returns 3 and the minimum reads 3 from the pair below."},{"at":{"in":4},"vars":{"pairs":"[5/5, 3/3]","min":3},"note":"pop() returns 7 and the minimum reads 3 from the pair below."},{"at":{"in":4},"vars":{"pairs":"[5/5]","min":5},"note":"pop() returns 3 and the minimum reads 5 from the pair below."},{"at":{"in":4},"vars":{"pairs":"[]","min":"none"},"note":"pop() returns 5 and the stack is empty."}]}
```

#### Helper Stack With Duplicate Minima

The second trace pushes 4, 2, 2 and 6. It shows the main stack and the helper stack side by side. The second 2 equals the current minimum, so it enters the helper stack as well. The 6 stays out of the helper stack.

The pops show why the equality matters. Popping 6 changes only the main stack. Popping the first 2 removes one helper entry, and the minimum is still 2 because the other entry remains. Popping the second 2 removes the last entry for 2, and the minimum becomes 4.

```trace
{"cells":[4,2,2,6],"pointers":["in"],"steps":[{"at":{"in":0},"vars":{"main":"[4]","helper":"[4]","min":4},"note":"push(4) also enters the helper stack."},{"at":{"in":1},"vars":{"main":"[4, 2]","helper":"[4, 2]","min":2},"note":"push(2) also enters the helper stack."},{"at":{"in":2},"vars":{"main":"[4, 2, 2]","helper":"[4, 2, 2]","min":2},"note":"push(2) also enters the helper stack."},{"at":{"in":3},"vars":{"main":"[4, 2, 2, 6]","helper":"[4, 2, 2]","min":2},"note":"push(6) stays out of the helper stack."},{"at":{"in":4},"vars":{"main":"[4, 2, 2]","helper":"[4, 2, 2]","min":2},"note":"pop() returns 6 and leaves the helper stack unchanged."},{"at":{"in":4},"vars":{"main":"[4, 2]","helper":"[4, 2]","min":2},"note":"pop() returns 2 and removes one helper entry."},{"at":{"in":4},"vars":{"main":"[4]","helper":"[4]","min":4},"note":"pop() returns 2 and removes one helper entry."},{"at":{"in":4},"vars":{"main":"[]","helper":"[]","min":"none"},"note":"pop() returns 4 and removes one helper entry."}]}
```

<!-- stage: code -->
### Two Working Designs In Java

#### Pairs Stored In One Stack

The first class keeps one `ArrayDeque` of two-element arrays. Index 0 holds the value and index 1 holds the prefix minimum.

```java
final class PairMinStack {
    private final ArrayDeque<int[]> entries = new ArrayDeque<>();

    void push(int v) {
        int lowest = entries.isEmpty() ? v : Math.min(v, entries.peek()[1]);
        entries.push(new int[] {v, lowest});
    }
    int pop() { return entries.pop()[0]; }
    int top() { return entries.peek()[0]; }
    int getMin() { return entries.peek()[1]; }
}
```

#### Values And A Helper Stack

The second class keeps two stacks of boxed `Integer` values. In `v == mins.peek()`, the variable `v` is a primitive `int`, so Java unboxes `mins.peek()` and the `==` test is numeric, whichever side `v` is on. Comparing two `Integer` objects with `==` would compare object identity, and equal values above 127 can be different objects.

```java
final class HelperMinStack {
    private final ArrayDeque<Integer> main = new ArrayDeque<>();
    private final ArrayDeque<Integer> mins = new ArrayDeque<>();

    void push(int v) {
        main.push(v);
        if (mins.isEmpty() || v <= mins.peek()) mins.push(v);
    }
    int pop() {
        int v = main.pop();
        if (v == mins.peek()) mins.pop();
        return v;
    }
    int top() { return main.peek(); }
    int getMin() { return mins.peek(); }
}
```

Both classes run each operation in O(1) worst-case time. The pair version uses O(n) extra space always. The helper version uses O(n) extra space in the worst case, which happens when the values are pushed in non-increasing order. Both rely on the caller never calling `pop`, `top` or `getMin` on an empty stack.

<!-- stage: applicability -->
### When Saved Prefix Answers Apply

#### The Operation Contract Decides

The method applies when a stack must answer an aggregate question over all of its current values, in constant time, after any push or pop. The invariant is that each position stores the aggregate of the values at or below it. The aggregate must combine one new value with the stored answer in constant time. Minimum and maximum qualify. A sum also qualifies, and so does a count of values that satisfy a test.

#### Two False Friends

A single field `currentMin` is a false friend. It works after pushes, and it breaks on the first pop of the minimum, because the second smallest value is gone. A scan on demand, as in the opening code, is the other false friend. It returns correct answers and violates the constant-time contract.

A sorted tree such as `TreeMap` also looks like a fit. It supports minimum queries, but each operation costs O(log n), and it is not needed when removal happens only at the top.

#### When It Does Not Apply

Removal from the top is what makes the stored answers safe. A queue removes the oldest value, which sits under every newer prefix. The stored prefix minimums become wrong there, and a queue needs a different invariant. A question about the median or the k-th smallest value cannot combine one value with one stored number either.

<!-- stage: exercises -->
### Exercises

#### [Build] Value-Min Pairs (Author exercise)
<!-- id: sq-value-min-pairs -->

**Prerequisites.** The value-min pair design in this lesson.

**Problem.** A stack starts empty and supports four operations given as integer arrays. The array `{0, x}` pushes `x`. The array `{1}` pops the top value. The array `{2}` reads the top value without removing it. The array `{3}` reads the smallest value on the stack without removing anything. Process the operations in order and return the results of the `{2}` and `{3}` operations, in order. Store each pushed value together with the smallest value at or below it.

**Constraints.** The limits are:
- **Length** is `1 <= ops.length <= 10^5`.
- **Values** are `int` values in `x`.
- **Validity** means no pop, read or minimum operation runs on an empty stack.
- **Return** is an `int[]` and is empty when no read operation occurs.

**Example 1.** Input `[[0,5],[0,3],[0,7],[3],[1],[1],[3],[2]]`, output `[3,5,5]`.

**Example 2.** Input `[[0,4],[0,9],[0,2],[3],[1],[3],[2]]`, output `[2,4,9]`.

**Hint.** Compute the smaller of the new value and the minimum stored in the entry below. What does the entry below hold after a pop?

**Changed decision.** The answer for each position is computed once, at push time.

#### [Vary] Two-Stack Minimum (Author exercise)
<!-- id: sq-two-stack-minimum -->

**Prerequisites.** The exercise above and the helper stack design in this lesson.

**Problem.** Use the same operation format as the previous exercise, with the operations `{0, x}` and `{1}` only. The minimum is kept in a second stack. A pushed value goes onto the second stack exactly when it is less than or equal to the current minimum, or when the second stack is empty. A popped value leaves the second stack exactly when it equals the second stack's top. After all operations, return the number of entries left on the second stack.

**Constraints.** The limits are:
- **Length** is `1 <= ops.length <= 10^5`.
- **Values** are `int` values in `x`, including equal values.
- **Validity** means no pop runs on an empty stack.
- **Return** is an `int`.

**Example 1.** Input `[[0,5],[0,3],[0,7],[0,3],[0,8],[0,1],[1],[1],[1]]`, output 2.

**Example 2.** Input `[[0,4],[0,2],[0,6],[0,1]]`, output 3.

**Hint.** Track both stacks together. Which pops change the second stack, and which leave it alone?

**Changed decision.** The minimum is stored only where it changes, so the extra space depends on the input order.

#### [Boundary] Duplicate Minima (Author exercise)
<!-- id: sq-duplicate-minima -->

**Prerequisites.** The two exercises above.

**Problem.** A stack supports `{0, x}` to push `x` and `{1}` to pop the top value. After every operation, report the smallest value on the stack, or `Integer.MAX_VALUE` when the stack is empty. Return one report per operation, in order. Several pushed values can be equal to the minimum, and popping one copy must leave the minimum unchanged while another copy remains.

**Constraints.** The limits are:
- **Length** is `1 <= ops.length <= 10^5`.
- **Values** are `int` values with `-10^9 <= x <= 10^9`.
- **Validity** means no pop runs on an empty stack.
- **Return** is an `int[]` with one entry per operation.

**Example 1.** Input `[[0,2],[0,2],[0,5],[1],[1],[1]]`, output `[2,2,2,2,2,2147483647]`.

**Example 2.** Input `[[0,7],[0,7],[1],[0,3],[1],[1]]`, output `[7,7,7,3,7,2147483647]`.

**Hint.** Remove a minimum entry only when the popped value equals it. Which comparison keeps a second copy of the minimum alive?

**Changed decision.** An empty stack reports a sentinel, and equal minimum values each keep their own record.

#### [Recognize] Min Stack (LeetCode 155)
<!-- id: sq-leetcode-min-stack -->

**Prerequisites.** The three exercises above.

**Problem.** Design a class `MinStack` with `push(int val)`, `pop()`, `top()` and `getMin()`. The method `top` returns the newest value, and `getMin` returns the smallest value currently stored. Every method must run in constant time in the worst case.

**Constraints.** The limits are:
- **Calls** total at most `3 * 10^4`.
- **Values** are `int` values, including `Integer.MIN_VALUE` and `Integer.MAX_VALUE`.
- **Validity** means `pop`, `top` and `getMin` run only on a non-empty stack.
- **Cost** per call is O(1) in the worst case, not amortized.

**Example 1.** Input calls `push(-2)`, `push(0)`, `push(-3)`, `getMin()`, `pop()`, `top()`, `getMin()`, output `[-3,0,-2]` for the three read calls.

**Example 2.** Input calls `push(2)`, `push(1)`, `push(1)`, `pop()`, `getMin()`, output `[1]` for the one read call.

**Hint.** The same minimum can appear at many depths. Which stored information survives a pop of one copy?

**Changed decision.** The contract names worst-case time, which rules out any scan and any rebuild.
