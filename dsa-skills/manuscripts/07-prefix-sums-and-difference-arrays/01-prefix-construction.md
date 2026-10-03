<!-- lesson-kind: standard -->
<!-- lesson-id: prefix-construction -->
## Prefix Construction

<!-- stage: context -->
### A Cashier's Running Total

A cashier rings up a long list of purchases for a customer, and the till prints the amount of each item on a paper tape. At the end of the afternoon the shop owner wants to ask questions of the tape: how much had the customer spent when the fifth item was scanned, and was the spending past a certain limit by the twelfth? Some prices are negative, because returned items are credited.

The owner could add up the first five amounts on a calculator, then the first twelve, then the first three, and so on for each question. A better cashier writes, next to each amount, the total of everything printed so far. After that, "how much by the fifth item" is read straight off the fifth line, and nobody has to add anything again.

<!-- stage: naive -->
### Add The Items Again For Each Question

The direct approach answers each question by adding the first few items from the top of the tape.

```java
static long spentAfter(int[] amounts, int items) {
    long total = 0;
    for (int i = 0; i < items; i++) {
        total += amounts[i];
    }
    return total;
}
```

It is correct for any number of items between zero and the length of the tape, and a request for zero items correctly gives zero.

<!-- stage: bottleneck -->
### The Same Additions Over And Over

A question about the first k items costs O(k), and a list of q questions about a tape of n items costs O(q n) in the worst case. With a hundred thousand items and a hundred thousand questions, the loop performs about ten billion additions. Most of them repeat work: the total of the first twelve items starts with the total of the first five, which an earlier question already computed.

Each total is the previous total plus one more item. The answers form a chain, and the chain can be produced in a single pass over the tape, in O(n) time, by remembering the total so far and adding the next amount. Once the chain is stored, any question about "the first k items" is one lookup.

<!-- stage: insight -->
### Store The Total Up To Each Position

A **prefix sum** is the total of everything before a position. It is stored in an array of length `n + 1`, where `prefix[i]` is the sum of the first `i` values, so `prefix[0]` is the sum of nothing, which is zero. The extra leading slot is a **sentinel**: a value placed so that no question needs a special case. Every entry after it follows one rule, `prefix[i + 1] = prefix[i] + a[i]`, which is the whole algorithm.

With the sentinel, the invariant is easy to state: after processing `i` values, `prefix[i]` is exactly the sum of `a[0]` to `a[i - 1]`. A running total with no sentinel stores the sum through each position instead, and then an empty prefix has nowhere to live, so a question about zero items needs a special case. The sentinel convention removes that case, and the same convention keeps range formulas simple in later lessons.

<!-- names: prefix sum, sentinel, running total -->

The same array also answers other questions at once. A position where the amount to the left equals the amount to the right can be found from the **running total** alone: if the grand total is `T` and the sum before position `i` is `L`, the sum after it is `T - L - a[i]`, so no second array is needed. In every case the work is one pass to build the chain, and then constant work per question.

<!-- stage: variables -->
### The Array, The Total And The Slot

`a` is the input and stays unchanged. `prefix` has one more slot than `a`, and `prefix[0]` is zero. `total` is the running total while the chain is built, and it is held in a `long` because many `int` values can add up to more than an `int` can hold. `i` is the position of the amount being added, and the slot written is `i + 1`. For a pivot question, `left` is the sum before the current position and the sum to the right is computed from the grand total instead of being stored.

<!-- stage: trace -->
### Building The Chain, Then Using It

The first trace builds the chain for the amounts 4, -2, 5, 3, -6, 1. The row of cells holds the amounts, and the variables carry the running total. The step to study is the fifth: the amount is negative, so the total goes down, which shows that a prefix sum does not have to grow.

```trace
{"cells":["4","-2","5","3","-6","1"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"amount":4,"total":4},"note":"Add 4 to the total, which becomes 4, and write it into slot 1."},{"at":{"i":1},"vars":{"amount":-2,"total":2},"note":"Add -2 to the total, which becomes 2, and write it into slot 2."},{"at":{"i":2},"vars":{"amount":5,"total":7},"note":"Add 5 to the total, which becomes 7, and write it into slot 3."},{"at":{"i":3},"vars":{"amount":3,"total":10},"note":"Add 3 to the total, which becomes 10, and write it into slot 4."},{"at":{"i":4},"vars":{"amount":-6,"total":4},"note":"Add -6 to the total, which becomes 4, and write it into slot 5."},{"at":{"i":5},"vars":{"amount":1,"total":5},"note":"Add 1 to the total, which becomes 5, and write it into slot 6."}]}
```

The second trace looks for a pivot, a position whose left sum equals its right sum, in 2, -1, 8, 4, 2, 2, 5. The grand total is 22. The step to study is the fourth: the sum to the left is 9, the amount is 4, and the sum to the right is 22 - 9 - 4 = 9, so the position is a pivot.

```trace
{"cells":["2","-1","8","4","2","2","5"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"left":0,"amount":2,"right":20},"note":"The left sum is 0 and the right sum is 20, which differ, so add 2 to the left sum and move on."},{"at":{"i":1},"vars":{"left":2,"amount":-1,"right":21},"note":"The left sum is 2 and the right sum is 21, which differ, so add -1 to the left sum and move on."},{"at":{"i":2},"vars":{"left":1,"amount":8,"right":13},"note":"The left sum is 1 and the right sum is 13, which differ, so add 8 to the left sum and move on."},{"at":{"i":3},"vars":{"left":9,"amount":4,"right":9},"note":"The left sum is 9, the amount is 4, and the right sum is 22 - 9 - 4 = 9, so position 3 is a pivot."}]}
```

<!-- stage: code -->
### One Pass Builds The Chain

```java
static long[] buildPrefix(int[] a) {
    long[] prefix = new long[a.length + 1];
    for (int i = 0; i < a.length; i++) {
        prefix[i + 1] = prefix[i] + a[i];
    }
    return prefix;
}

static int[] runningSum(int[] a) {
    int[] out = new int[a.length];
    int total = 0;
    for (int i = 0; i < a.length; i++) {
        total += a[i];
        out[i] = total;
    }
    return out;
}

static int pivotIndex(int[] a) {
    long total = 0;
    for (int x : a) total += x;
    long left = 0;
    for (int i = 0; i < a.length; i++) {
        if (left == total - left - a[i]) return i;
        left += a[i];
    }
    return -1;
}
```

Building takes one pass over the n values and uses n + 1 slots of space, and the pivot search takes two passes and O(1) space beyond the input. The running sum may use `int` only when the contract promises the total fits, as in its exercise below.

<!-- stage: applicability -->
### When Earlier Totals Get Reused

Reach for prefix sums when many questions ask for the total of everything before a position, or when a single answer compares what lies before a position with what lies after it. The invariant is the chain rule: the value stored at slot `i` is the sum of the first `i` values, and each slot is computed from the one before it.

One false friend is the plain loop that re-adds from the start for every question, which looks harmless for one question and ruins a batch of them. Another is a running total that stores the sum through each position without a sentinel, which forces an extra branch for the empty prefix and invites an off-by-one when ranges arrive in the next lesson. A third is a prefix of the wrong kind: the total of a window that slides is not a prefix at all.

In Java, decide the type of the stored total before writing the loop. Use `long` when the maximum value times the length can pass the range of `int`, and say in a comment why that bound holds. Allocate `n + 1` slots, not `n`, so that index zero is the empty prefix, and never read `a[i - 1]` before checking that `i` is at least one.

<!-- stage: exercises -->
### Exercises

#### [Build] Running Sum of 1d Array (LeetCode 1480)
<!-- id: ps-running-sum -->

**Prerequisites.** Loops over arrays from Chapter 01 and the idea of a running total.

**Problem.** Given an integer array, return an array of the same length in which position `i` holds the sum of the original values from position zero through position `i`. The input array must not be changed.

**Constraints.** 1 <= nums.length <= 1000 and -1000000 <= nums[i] <= 1000000, so every running total fits in an `int`.

**Example 1.** Input `nums = [2, 5, -1, 4]`, output `[2, 7, 6, 10]`.

**Example 2.** Input `nums = [7, 7, 7]`, output `[7, 14, 21]`.

**Hint.** What does each output position need besides its own input value? Can you keep that in one variable?

**Changed decision.** First rung: the answer is built left to right, and each position reuses the total of the one before it.

#### [Vary] Find Pivot Index (LeetCode 724)
<!-- id: ps-pivot-index -->

**Prerequisites.** The Running Sum exercise above.

**Problem.** Return the leftmost index whose left sum equals its right sum, where the sum of an empty side is zero and the value at the index itself belongs to neither side. Return minus one if no index qualifies.

**Constraints.** 1 <= nums.length <= 10000 and -1000 <= nums[i] <= 1000.

**Example 1.** Input `nums = [2, -1, 8, 4, 2, 2, 5]`, output 3.

**Example 2.** Input `nums = [3, 3]`, output -1.

**Hint.** If you know the grand total and the sum so far, what is the sum on the other side? Why can the first position be a pivot?

**Changed decision.** The question compares two sides of a position, so only the running total and the grand total are needed, and no array of sums is stored.

#### [Boundary] Empty Prefix (Author exercise)
<!-- id: ps-empty-prefix -->

**Prerequisites.** The two exercises above.

**Problem.** Write `buildPrefix` and a function `sumOfFirst(prefix, count)` that returns the sum of the first `count` values for any `count` from zero to the length. An empty array must produce a prefix with one slot, a count of zero must return zero, and values near the top of the `int` range must not overflow.

**Constraints.** 0 <= nums.length <= 100000 and any `int` values, including 2147483647.

**Example 1.** Input `nums = []`, output a prefix `[0]` and `sumOfFirst(prefix, 0) = 0`.

**Example 2.** Input `nums = [2000000000, 2000000000]`, output `sumOfFirst(prefix, 2) = 4000000000`.

**Hint.** Which slot of the prefix stands for no values? What type must the slots have?

**Changed decision.** The empty prefix is a real answer, so the array has one more slot than the input and the slots are `long`.

#### [Recognize] Prefix Averages (Author exercise)
<!-- id: ps-prefix-averages -->

**Prerequisites.** All three exercises above.

**Problem.** For each position `i`, return the average of the first `i + 1` values as a `double`. The division must use the number of values in the prefix, not the position of the last value, and the sum must not overflow.

**Constraints.** 1 <= nums.length <= 100000 and -1000000000 <= nums[i] <= 1000000000.

**Example 1.** Input `nums = [4, 6, 2]`, output `[4.0, 5.0, 4.0]`.

**Example 2.** Input `nums = [1000000000, 1000000000, 1000000000]`, output `[1.0E9, 1.0E9, 1.0E9]`.

**Hint.** Which running total do you already have at position `i`? What is the count of values it covers?

**Changed decision.** The stored total is combined with a count, so the type of the sum and the divisor are chosen on purpose.
