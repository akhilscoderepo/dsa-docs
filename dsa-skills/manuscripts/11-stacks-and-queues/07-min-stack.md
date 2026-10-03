<!-- lesson-kind: standard -->
<!-- lesson-id: min-stack -->
## Min Stack

<!-- stage: context -->
### The Cold Store Logbook

A cold store keeps a logbook of temperature readings in the order they were taken, and the clerk treats the logbook like a stack: a new reading is written on top, and when a reading is found to be a sensor glitch, the clerk crosses out the most recent entry, which removes it. At any moment the inspector may walk in and ask a single question: what is the coldest reading still standing in the logbook? The clerk must answer at once, because the inspector will not wait while the whole book is read.

Readings are written and crossed out thousands of times a day, and the inspector asks often. Some readings repeat, and the coldest value can be written twice. The clerk worries that crossing out one of two equal coldest readings will somehow make the coldest value disappear from the answer.

<!-- stage: naive -->
### Read The Whole Book For Each Question

The direct method keeps the readings in an ordinary stack and, whenever the inspector asks, reads through every reading in the stack and reports the smallest.

```java
static int coldestByScan(ArrayDeque<Integer> readings) {
    int coldest = Integer.MAX_VALUE;
    for (int r : readings) coldest = Math.min(coldest, r);
    return coldest;
}
```

It is correct, because the answer is the minimum over exactly the readings that are currently standing, and the loop examines all of them.

<!-- stage: bottleneck -->
### The Question Costs The Whole Book

With n readings standing, one question reads n values, which is O(n). An inspector who asks m times in a day causes O(n m) reading work, and a book of a hundred thousand entries asked ten thousand times means a billion value reads. The operations that write and cross out are constant time, so the questions have become the whole cost of the system, although the requirement is that every operation, the question included, should answer in constant time.

Most of that work repeats earlier work. Between two questions only a few entries changed, yet the scan reads everything again. The coldest reading of the book is the smaller of two things: the newest reading, and the coldest of everything below it. The coldest of everything below it was already true at the moment the newest reading was written, so if it is written down beside the reading at that time, the question becomes a single lookup at the top.

<!-- stage: insight -->
### Store The Answer Beside The Entry

When a reading is pushed, the coldest value of the stack as it will be after the push is known immediately: it is the smaller of the new reading and the **paired minimum** of the entry below, or the new reading itself on an empty stack. Store that value with the entry. Then the top entry always carries the coldest value of the whole stack, and the question is one read of the top, without any scan. Crossing out the top entry removes its pair, and the entry underneath still carries the coldest value for exactly the readings that remain, because that value was computed when it was on top and nothing below it has changed.

The invariant is that every depth of the stack carries enough information to recover the minimum of exactly the prefix of the stack that ends at that depth. Pushes and pops preserve it, because a push adds one new prefix and a pop discards the longest one, and the shorter prefixes are untouched.

A cheaper layout keeps the readings in one stack and the record in a second, the **minimum stack**, which gets a new entry only when the reading is a new coldest value. The **equal-value rule** decides the boundary: the reading goes onto the minimum stack when it is smaller than or equal to the current minimum. With a strict comparison, the second of two equal coldest readings would not be recorded, and crossing out one of them would remove the only record of the cold value while the other reading is still standing. The comparison with equality keeps one record for each standing copy.

<!-- names: paired minimum, minimum stack, equal-value rule -->

A heap would answer the same question for any removal order, but a stack only removes its newest entry, so the answer for each prefix can be fixed once, with no further structure.

<!-- stage: variables -->
### Pairs, Or Two Stacks In Step

The first layout stores each entry as a pair of the reading and the coldest value at that depth, so `top[1]` answers the question and the stack grows by one pair per push. The second layout keeps `values` for readings and `mins` for the record, and a pop from `values` also pops `mins` exactly when the removed reading equals the top of `mins`. Both layouts answer in constant time and use O(n) space, and the second can use less when readings only rarely set a new coldest value. Readings are `int` values and comparisons use the primitive operators, so boxed equality is never needed.

<!-- stage: trace -->
### Writing, Asking And Crossing Out

The first trace uses the paired layout. The cells hold the script, and `op` points at the step being run. After the readings 5, 3 and 7 the top pair is 7 with coldest 3, so the question answers 3 at once. Crossing out the 7 exposes the pair 3 with coldest 3, and crossing out the 3 exposes 5 with coldest 5, which is what a rescan would also have found.

```trace
{"cells":["push 5","push 3","push 7","min","pop","pop","min"],"pointers":["op"],"steps":[{"at":{"op":0},"vars":{"pairs":"[(5,5)]","answers":"[]"},"note":"The reading 5 is pushed with the coldest value 5, which is the smaller of 5 and the pair below."},{"at":{"op":1},"vars":{"pairs":"[(5,5),(3,3)]","answers":"[]"},"note":"The reading 3 is pushed with the coldest value 3, which is the smaller of 3 and the pair below."},{"at":{"op":2},"vars":{"pairs":"[(5,5),(3,3),(7,3)]","answers":"[]"},"note":"The reading 7 is pushed with the coldest value 3, which is the smaller of 7 and the pair below."},{"at":{"op":3},"vars":{"pairs":"[(5,5),(3,3),(7,3)]","answers":"[3]"},"note":"The question reads the top pair and answers 3 without scanning."},{"at":{"op":4},"vars":{"pairs":"[(5,5),(3,3)]","answers":"[3]"},"note":"The top pair with reading 7 is crossed out, and the pair below now carries the coldest value of what remains."},{"at":{"op":5},"vars":{"pairs":"[(5,5)]","answers":"[3]"},"note":"The top pair with reading 3 is crossed out, and the pair below now carries the coldest value of what remains."},{"at":{"op":6},"vars":{"pairs":"[(5,5)]","answers":"[3,5]"},"note":"The question reads the top pair and answers 5 without scanning."}]}
```

The second trace uses the two-stack layout with repeated readings. The reading 4 is written twice and both copies are recorded, because the rule records equal values. Look at the second crossing out: it removes one 4, the record keeps the other, and the question still answers 4. A strict comparison would have lost the record at exactly this step.

```trace
{"cells":["push 4","push 4","push 2","pop","pop","min"],"pointers":["op"],"steps":[{"at":{"op":0},"vars":{"values":"[4]","mins":"[4]"},"note":"The reading 4 is at most the current minimum, so it is recorded on the minimum stack as well."},{"at":{"op":1},"vars":{"values":"[4,4]","mins":"[4,4]"},"note":"The reading 4 is at most the current minimum, so it is recorded on the minimum stack as well."},{"at":{"op":2},"vars":{"values":"[4,4,2]","mins":"[4,4,2]"},"note":"The reading 2 is at most the current minimum, so it is recorded on the minimum stack as well."},{"at":{"op":3},"vars":{"values":"[4,4]","mins":"[4,4]"},"note":"The reading 2 equals the top of the minimum stack, so its record is removed too."},{"at":{"op":4},"vars":{"values":"[4]","mins":"[4]"},"note":"The reading 4 is crossed out and its record is removed, but the other copy of 4 is still standing and still recorded, so the minimum stack keeps one entry."},{"at":{"op":5},"vars":{"values":"[4]","mins":"[4]"},"note":"The question reads the top of the minimum stack and answers 4."}]}
```

<!-- stage: code -->
### A Stack That Knows Its Minimum

```java
static final class MinStack {
    private final ArrayDeque<int[]> pairs = new ArrayDeque<>();

    void push(int x) {
        int below = pairs.isEmpty() ? x : pairs.peekLast()[1];
        pairs.addLast(new int[] {x, Math.min(x, below)});
    }

    int pop() { return pairs.removeLast()[0]; }

    int top() { return pairs.peekLast()[0]; }

    int getMin() { return pairs.peekLast()[1]; }
}

static final class TwoStackMin {
    private final ArrayDeque<Integer> values = new ArrayDeque<>();
    private final ArrayDeque<Integer> mins = new ArrayDeque<>();

    void push(int x) {
        values.addLast(x);
        if (mins.isEmpty() || x <= mins.peekLast()) mins.addLast(x);
    }

    int pop() {
        int x = values.removeLast();
        if (x == mins.peekLast()) mins.removeLast();
        return x;
    }

    int getMin() { return mins.peekLast(); }
}
```

Every operation touches at most two deque entries, so each one is O(1) in the worst case and not only on average, and the space is O(n). The pair version spends one extra integer per entry, while the two-stack version spends extra only when a new minimum arrives.

<!-- stage: applicability -->
### When A Stack Must Know Its Extreme

Use this when a stack must also report its current minimum or maximum in constant time, as in undo histories, expression evaluation with running bounds, and monitoring logs. The invariant is that each depth carries what is needed to recover the answer for exactly that prefix.

A false friend is scanning for the minimum on demand, which breaks the constant-time contract. A second false friend is a single variable holding the minimum, which cannot recover the previous minimum after a pop. A third is the strict comparison in the two-stack layout, which loses a duplicate minimum.

In Java, use `x <= mins.peekLast()` so that the unboxed comparison includes equality, and compare the popped value with the top of the minimum stack by unboxing, since `Integer` objects should not be compared with `==` beyond the small cached range. Keep pop and getMin behind the nonempty contract of the problem, or check `isEmpty()` before them.

<!-- stage: exercises -->
### Exercises

#### [Build] Value-Min Pairs (Author exercise)
<!-- id: sq-value-min-pairs -->

**Prerequisites.** The Nested Structure lesson.

**Problem.** A script is an array of integers: a nonnegative value pushes it, -1 pops the top, and -2 asks for the minimum of the stack. Return the answers to all -2 commands in order. Push each value together with the minimum of the stack after the push. Every pop and every question finds a nonempty stack.

**Constraints.** 0 <= script.length <= 100000 and each value is -2, -1, or between 0 and 1000000000.

**Example 1.** Input `script = [5, 3, 7, -2, -1, -2, -1, -2]`, output `[3, 3, 5]`.

**Example 2.** Input `script = [9, -2]`, output `[9]`.

**Hint.** What is the minimum of the stack immediately after a push, in terms of the new value and the entry below?

**Changed decision.** First rung: the minimum is computed once at push time and travels with the entry.

#### [Vary] Two-Stack Minimum (Author exercise)
<!-- id: sq-two-stack-minimum -->

**Prerequisites.** The Value-Min Pairs rung.

**Problem.** Run the same kind of script using a second stack that records minimums: a pushed value goes onto it when it is smaller than or equal to the current minimum, and a pop removes from it when the popped value equals its top. Return the answers to all -2 commands, followed by the final size of the minimum stack as the last element.

**Constraints.** 0 <= script.length <= 100000 and each value is -2, -1, or between 0 and 1000000000. Every pop and question finds a nonempty stack.

**Example 1.** Input `script = [4, 4, 2, -2]`, output `[2, 3]`.

**Example 2.** Input `script = [5, 6, 7, -2]`, output `[5, 1]`.

**Hint.** When does a pushed value need a record? What does the second stack look like after pushing 5, 6 and 7?

**Changed decision.** The record lives in a separate stack that grows only on new or equal minimums, so the final size of that stack depends on the equality rule.

#### [Boundary] Duplicate Minima (Author exercise)
<!-- id: sq-duplicate-minima -->

**Prerequisites.** The Two-Stack Minimum rung.

**Problem.** The script also has the command -3, which reports the top value without removing it. Run the script with the two-stack layout and return, in order, the value removed by every pop, the top reported by every -3, and the minimum reported by every -2. Pushing the same minimum twice and then popping once must not lose it.

**Constraints.** 0 <= script.length <= 100000, each value is -3, -2, -1, or between 0 and 1000000000, and every pop, top and question finds a nonempty stack.

**Example 1.** Input `script = [2, 2, -1, -2]`, output `[2, 2]`.

**Example 2.** Input `script = [3, 1, 1, 4, -1, -1, -2, -3]`, output `[4, 1, 1, 1]`.

**Hint.** After the second copy of the minimum is popped, is the first copy still recorded?

**Changed decision.** Duplicate minimums each keep their own record, so a pop of one copy leaves the other copy answering the question.

#### [Recognize] Min Stack (LeetCode 155)
<!-- id: sq-min-stack -->

**Prerequisites.** The Duplicate Minima rung.

**Problem.** Design a stack that supports `push`, `pop`, `top` and `getMin`, each in constant worst-case time. The input is a list of command strings, and the output has one string per command: a dash for `push x` and `pop`, and the value for `top` and `getMin`. Every `pop`, `top` and `getMin` finds a nonempty stack.

**Constraints.** 1 <= commands.length <= 100000 and every pushed value fits in a signed 32-bit integer, including the extremes.

**Example 1.** Input `commands = ["push 6", "push 2", "getMin", "pop", "top", "getMin"]`, output `["-", "-", "2", "-", "6", "6"]`.

**Example 2.** Input `commands = ["push -2147483648", "push 5", "getMin", "pop", "getMin"]`, output `["-", "-", "-2147483648", "-", "-2147483648"]`.

**Hint.** What is the smallest value an `int` can hold? If a design saves space by storing differences between a value and the minimum, what happens to the difference of two extreme values?

**Changed decision.** The full interface must be constant time in the worst case, including values at the extremes of `int`, so a design that encodes differences in `int` is unsafe and the stored values must be exact.
