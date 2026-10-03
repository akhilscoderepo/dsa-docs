<!-- lesson-kind: standard -->
<!-- lesson-id: endpoint-ordering-contracts -->
## Endpoint Ordering Contracts

<!-- stage: context -->
### A Scheduler With Index Cards

A conference scheduler has a shoebox of index cards. Each card has two numbers written on it, the minute a talk starts and the minute it ends, and the cards are in no particular order. Rooms are scarce, so the scheduler wants to know how many separate blocks of continuous activity the day contains: stretches of time during which at least one talk is running, with a quiet gap before the next block begins. Two talks that share even a single minute belong to the same block.

She tries to settle this by picking up a card and checking it against every other card to see whether the two share a minute. The shoebox holds hundreds of cards, and after every merge of two cards she has to start checking again, because the merged card may now reach talks that the original cards did not.

<!-- stage: naive -->
### Merge Any Two Cards That Touch

The direct approach is to keep merging any two cards that share a minute, and to stop when no pair does.

```java
static int blocksByMerging(int[][] cards) {
    List<int[]> list = new ArrayList<>();
    for (int[] c : cards) list.add(new int[] {c[0], c[1]});
    boolean changed = true;
    while (changed) {
        changed = false;
        for (int i = 0; i < list.size() && !changed; i++) {
            for (int j = i + 1; j < list.size() && !changed; j++) {
                int[] a = list.get(i), b = list.get(j);
                if (a[0] <= b[1] && b[0] <= a[1]) {
                    a[0] = Math.min(a[0], b[0]);
                    a[1] = Math.max(a[1], b[1]);
                    list.remove(j);
                    changed = true;
                }
            }
        }
    }
    return list.size();
}
```

When the loop stops, no two remaining cards share a minute, so the number of cards left is the number of blocks.

<!-- stage: bottleneck -->
### Every Pair Is Checked After Every Merge

One round of the double loop compares up to n squared over two pairs, and a merge restarts the search, so the worst case is O(n^3) comparisons. Even a single round is O(n^2), which is too slow for a hundred thousand cards. The cards are compared with many others that are nowhere near them in time.

The waste comes from having no order. If the cards lay in a row sorted by start minute, then whether the next card shares a minute with the cards before it would depend only on how far the previous blocks reach. Everything earlier than the block currently being grown has already ended, or it would have been absorbed. One number, the furthest minute reached so far, would be enough to decide about each new card, so one pass over the sorted cards costs O(n), and the sort itself costs O(n log n).

<!-- stage: insight -->
### Sort By Start, Remember One End

An ordering is a contract: it says what comes first, and it says what happens when two items tie. The most useful order for blocks of activity is **lexicographic order** on the pair, comparing starts first and breaking a tie by comparing ends. Once the cards are in that order, the invariant is that every card already processed begins no later than the card now in hand, so the only processed card that can still touch the new one is the block that reaches furthest. If the new card begins within that block, it joins it and may push the block's end further. If it begins after the block ends, no later card can reach back to it, since every later card begins even later, and the block is finished.

Sorting by end is a different contract, with different uses. It answers questions about which talk finishes first, and it supports selection problems. It does not support merging, because a long card that starts early but ends late appears after short cards that it should have absorbed, so the scan has already closed blocks that the later card reconnects. A **tie rule** says what to do for equal starts or equal ends, and it must be stated, since two cards with the same start are not interchangeable once ends matter.

<!-- names: lexicographic order, tie rule, safe comparison -->

In Java the comparison itself needs a **safe comparison**. A comparator written as `a[0] - b[0]` is tempting and wrong: the difference of two `int` values can overflow, giving a result with the wrong sign, and a sort that uses it may order the cards incorrectly or even throw. `Integer.compare(a[0], b[0])` has no such risk and returns the sign directly. A comparator for a pair then reads: compare starts, and if equal, compare ends.

<!-- stage: variables -->
### Cards, Order And The Reach So Far

`cards` is an array of two-number arrays, and sorting it by a comparator reorders the references, not the numbers. `reach` is the furthest end among the cards in the block being grown, and it is only meaningful after the first card has set it. `blocks` counts finished or started blocks. For each card after the first, the decision compares `card[0]` with `reach` under the endpoint contract: a start that does not pass `reach` joins the block, and a start that does pass it opens a new block. The comparator is chosen before anything else, since every later decision depends on it.

<!-- stage: trace -->
### Walking Sorted Cards, Then Unsorted Ones

The first trace scans the cards 1 to 3, 2 to 6, 8 to 10 and 15 to 18, already in start order. The row of cells is the cards, and the variables show the furthest end so far and the block count. Study the second step: the card starting at 2 begins before the reach of 3, so it joins the first block and pushes the reach to 6.

```trace
{"cells":["1-3","2-6","8-10","15-18"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"reach":3,"blocks":1},"note":"The first card 1 to 3 opens a block, so the reach is 3 and there is 1 block."},{"at":{"i":1},"vars":{"reach":6,"blocks":1},"note":"The card starts at 2, not past the reach, so it joins the block and the reach becomes 6."},{"at":{"i":2},"vars":{"reach":10,"blocks":2},"note":"The card starts at 8, past the reach, so a new block opens and the count is 2."},{"at":{"i":3},"vars":{"reach":18,"blocks":3},"note":"The card starts at 15, past the reach, so a new block opens and the count is 3."}]}
```

The second trace scans three cards sorted by end instead: 1 to 2, 5 to 6 and 0 to 10, which together form a single block. Watch the third step: the card from 0 to 10 begins before the reach of 6 and merges with the last block only, so the first block 1 to 2 is never reconnected and the count is wrong.

```trace
{"cells":["1-2","5-6","0-10"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"reach":2,"blocks":1},"note":"The first card 1 to 2 opens a block, so the reach is 2 and there is 1 block."},{"at":{"i":1},"vars":{"reach":6,"blocks":2},"note":"The card starts at 5, past the reach of 2, so a new block opens and the count is 2."},{"at":{"i":2},"vars":{"reach":10,"blocks":2},"note":"The card starts at 0, not past the reach of 6, so it merges with the last block only. The count stays 2, but the true answer is 1."}]}
```

<!-- stage: code -->
### Sort With A Contract, Then Scan

```java
static int[][] orderByStartThenEnd(int[][] intervals) {
    int[][] copy = new int[intervals.length][];
    for (int i = 0; i < intervals.length; i++) copy[i] = intervals[i].clone();
    Arrays.sort(copy, (a, b) -> {
        int byStart = Integer.compare(a[0], b[0]);
        return byStart != 0 ? byStart : Integer.compare(a[1], b[1]);
    });
    return copy;
}

static int[][] orderByEndThenStart(int[][] intervals) {
    int[][] copy = new int[intervals.length][];
    for (int i = 0; i < intervals.length; i++) copy[i] = intervals[i].clone();
    Arrays.sort(copy, (a, b) -> {
        int byEnd = Integer.compare(a[1], b[1]);
        return byEnd != 0 ? byEnd : Integer.compare(a[0], b[0]);
    });
    return copy;
}

static int countBlocks(int[][] intervals) {
    if (intervals.length == 0) return 0;
    int[][] sorted = orderByStartThenEnd(intervals);
    int blocks = 1;
    long reach = sorted[0][1];
    for (int i = 1; i < sorted.length; i++) {
        if (sorted[i][0] <= reach) reach = Math.max(reach, sorted[i][1]);
        else {
            blocks++;
            reach = sorted[i][1];
        }
    }
    return blocks;
}
```

Sorting costs O(n log n) and the scan costs O(n), so the total is O(n log n) time. The copies cost O(n) extra space, and they keep the caller's array in its original order.

<!-- stage: applicability -->
### When Order Decides Overlap

Reach for an explicit order when many records describe ranges and the decision about each record depends on the ranges before it. State the order as a contract before sorting: which endpoint comes first and how ties break. The invariant is that everything already processed is ordered before everything unprocessed, so one summary of the processed part is enough.

A false friend is sorting by end whenever the problem mentions ranges. That order serves selection of compatible items, and it fails for merging. Another false friend is a comparator that returns a boolean-like difference, which breaks at the extremes of `int`. A third is sorting a shared array in place when the caller expects the original order back, since the sort mutates the argument.

In Java, use `Integer.compare` on each endpoint, never subtraction, and write the tie rule as the second comparison. Sort a copy when the contract keeps the input unchanged, and clone each row, since copying the outer array alone shares the inner arrays. Hold the running reach in a `long` if endpoints can be near the limits of `int`, so that nothing is added to them.

<!-- stage: exercises -->
### Exercises

#### [Build] Order By Start Then End (Author exercise)
<!-- id: iv-order-start-end -->

**Prerequisites.** Sorting with comparators from Chapter 05, and arrays of arrays.

**Problem.** Return a new array of the same intervals sorted by start, with ties broken by the smaller end first. The original array and its rows must not be changed. Explain in a comment why the tie rule is part of the contract.

**Constraints.** 0 <= intervals.length <= 100000 and every interval has two integers with start <= end.

**Example 1.** Input `intervals = [[3, 5], [1, 4], [3, 4], [1, 2]]`, output `[[1, 2], [1, 4], [3, 4], [3, 5]]`.

**Example 2.** Input `intervals = [[2, 2]]`, output `[[2, 2]]`.

**Hint.** What does the comparator return when two starts are equal? Why must each row be copied?

**Changed decision.** First rung: the order of intervals becomes an explicit comparator with a stated tie rule.

#### [Vary] Order By End Then Start (Author exercise)
<!-- id: iv-order-end-start -->

**Prerequisites.** The Order By Start Then End exercise above.

**Problem.** Return a new array of the intervals sorted by end, with ties broken by the smaller start first. Then state in a comment which decision this order enables, namely choosing the interval that finishes first, and why it does not enable merging.

**Constraints.** 0 <= intervals.length <= 100000 and every interval has two integers with start <= end.

**Example 1.** Input `intervals = [[1, 10], [2, 3], [2, 5], [0, 3]]`, output `[[0, 3], [2, 3], [2, 5], [1, 10]]`.

**Example 2.** Input `intervals = [[5, 6], [1, 6], [3, 6]]`, output `[[1, 6], [3, 6], [5, 6]]`.

**Hint.** Which endpoint is compared first now? What stays the same in the code?

**Changed decision.** The primary key moves from the start to the end, which changes which later decision the sorted order supports.

#### [Boundary] Equal And Extreme Endpoints (Author exercise)
<!-- id: iv-extreme-endpoints -->

**Prerequisites.** The two exercises above.

**Problem.** Sort intervals whose endpoints include the smallest and largest `int` values, and intervals with equal starts and equal ends, using `Integer.compare`. Show an input on which a comparator based on subtraction gives the wrong order, and check the result against a sort by `long` values.

**Constraints.** 1 <= intervals.length <= 100000 and endpoints are any `int` values with start <= end.

**Example 1.** Input `intervals = [[2147483647, 2147483647], [-2147483648, -2147483648], [0, 0]]`, output `[[-2147483648, -2147483648], [0, 0], [2147483647, 2147483647]]`.

**Example 2.** Input `intervals = [[1, 2], [1, 2]]`, output `[[1, 2], [1, 2]]`.

**Hint.** What is `2147483647 - (-2147483648)` in `int` arithmetic? What does `Integer.compare` return instead?

**Changed decision.** The endpoints reach the limits of `int`, so the comparison must never compute a difference.

#### [Recognize] Merge Intervals (LeetCode 56)
<!-- id: iv-merge-count -->

**Prerequisites.** All three exercises above.

**Problem.** Given closed intervals in any order, return how many intervals remain after every pair that shares at least one point has been merged, repeatedly, until none do. Choose the order that makes one pass enough, and explain why only the furthest reach so far matters.

**Constraints.** 1 <= intervals.length <= 10000 and 0 <= start <= end <= 10000.

**Example 1.** Input `intervals = [[1, 3], [2, 6], [8, 10], [15, 18]]`, output 3.

**Example 2.** Input `intervals = [[1, 4], [4, 5]]`, output 1.

**Hint.** Which order guarantees that every earlier interval begins no later than the current one? What would go wrong if the intervals were ordered by end?

**Changed decision.** The order is chosen for a purpose: start order lets a single number, the furthest reach, summarize everything already seen.
