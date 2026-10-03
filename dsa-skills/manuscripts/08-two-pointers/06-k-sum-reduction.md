<!-- lesson-kind: standard -->
<!-- lesson-id: k-sum-reduction -->
## K-Sum Reduction

<!-- stage: context -->
### A Ferry And Its Deck Rating

A small ferry takes exactly three crates per crossing. Its deck is rated for one exact total weight, because the harbour master wants the boat to ride level and the ballast tanks are tuned for that figure. A pile of crates waits on the quay, and a ledger lists the weight of every crate in the order in which it was delivered, so the list is in no useful order at all.

Each morning the harbour master asks the same question: is there any group of three crates in the pile whose weights add up to the rating? On some mornings the answer is no, and then she wants to know the nearest total she can get, so that she can top up with sand. The pile holds thousands of crates, and a few weigh nearly as much as the boat can carry alone.

<!-- stage: naive -->
### Weigh Every Group Of Three

The first plan is to take every group of three crates from the ledger and compare its total with the rating.

```java
static boolean hasTripleByTrial(int[] weights, long rating) {
    for (int a = 0; a < weights.length; a++)
        for (int b = a + 1; b < weights.length; b++)
            for (int c = b + 1; c < weights.length; c++)
                if ((long) weights[a] + weights[b] + weights[c] == rating) return true;
    return false;
}
```

It leaves the ledger untouched and it answers correctly for short piles and for piles with no match. The total is added in `long`, so very heavy crates cannot spoil the comparison.

<!-- stage: bottleneck -->
### Every Pair Searches The Pile Again

The three loops examine about n cubed over six groups, which is O(n^3). A pile of two thousand crates means over a billion weighings, and each one is made on a ledger whose order says nothing about where a partner might be. After the first crate is picked, the loops ask a smaller question for every second crate: is there a third crate that completes the total? The answer to that question never uses what the earlier pairs learned, so the work is repeated for each pair.

The smaller question has structure that the ledger hides. Once a crate is picked, the other two must add up to a known number, and if the weights were sorted, a pair that is too light can be improved only by a heavier left crate and a pair that is too heavy only by a lighter right crate. One sweep from both ends of the sorted row could settle every pair for that pick at once, and it would cost O(n) instead of O(n^2).

<!-- stage: insight -->
### Pick One, Then Ask A Smaller Question

Sort a copy of the weights. Choosing the crate at position `i` turns the question "do three crates reach the rating" into "do two crates among those to the right of `i` reach the rating minus this weight". That is a **reduction**: the number of crates still to choose falls from three to two, and the figure to reach falls by the weight just chosen. The new figure is the **remaining target**, and it can be an arbitrary `long`, even when every weight fits into an `int`.

The two-crate question is the **base case**. On a sorted row it is answered by a sweep from both ends, because a pair that is too light can only be improved by moving the left end right, and a pair that is too heavy only by moving the right end left. Nothing else is ever needed, so each choice of `i` costs one linear sweep and the whole search costs O(n^2).

The same step works for any count of crates. With four crates to choose, pick one, reduce to three crates and a smaller target, pick another, and arrive at the pair sweep. Each level starts its candidates just to the right of the previous pick, so a group of crates is examined in sorted order once and never under another name. The invariant of a call is that its answer equals the answer to the question about its own range, count and remaining target, and the answer of a nested call is exactly what the call above is waiting for.

<!-- names: reduction, remaining target, base case -->

The shape is not tied to an exact total. If no exact answer exists, the sweep can instead remember the total that is nearest to the target and still move by the same rule, since the comparison that decides the direction is the same.

<!-- stage: variables -->
### Count, Start, Target And Best

`k` is the number of crates that still have to be chosen, and `from` is the first position of the row that may be chosen. `remaining` is a `long` equal to the rating minus the weights already picked, so it can pass the `int` limits in either direction. `lo` and `hi` are the two ends of the final sweep, and the sum of that pair is computed in `long` as well. For the nearest-total variant, `best` holds the total closest to the rating found so far, and it is replaced only by a strictly closer total. The caller's array is never written, because the sorting happens on a copy.

<!-- stage: trace -->
### One Pick And One Sweep

The first trace asks whether any three weights in the sorted row 2, 5, 7, 8, 11, 14, 20 reach 26. The pick of 2 leaves a remaining target of 24, and its sweep fails after five steps. Study the step where `i` becomes position 1: the pick is 5, the remaining target is 21, and a sweep from the far end finds the pair 7 and 14, which settles the whole question.

```trace
{"cells":[2,5,7,8,11,14,20],"pointers":["i","lo","hi"],"steps":[{"at":{"i":0,"lo":1,"hi":6},"vars":{"remaining":24,"pair":25},"note":"Pick 2, remaining target 24. Pair 5 + 20 = 25, too heavy, so hi becomes 5."},{"at":{"i":0,"lo":1,"hi":5},"vars":{"remaining":24,"pair":19},"note":"Pick 2, remaining target 24. Pair 5 + 14 = 19, too light, so lo becomes 2."},{"at":{"i":0,"lo":2,"hi":5},"vars":{"remaining":24,"pair":21},"note":"Pick 2, remaining target 24. Pair 7 + 14 = 21, too light, so lo becomes 3."},{"at":{"i":0,"lo":3,"hi":5},"vars":{"remaining":24,"pair":22},"note":"Pick 2, remaining target 24. Pair 8 + 14 = 22, too light, so lo becomes 4."},{"at":{"i":0,"lo":4,"hi":5},"vars":{"remaining":24,"pair":25},"note":"Pick 2, remaining target 24. Pair 11 + 14 = 25, too heavy, so hi becomes 4."},{"at":{"i":1,"lo":2,"hi":6},"vars":{"remaining":21,"pair":27},"note":"Pick 5, remaining target 21. Pair 7 + 20 = 27, too heavy, so hi becomes 5."},{"at":{"i":1,"lo":2,"hi":5},"vars":{"remaining":21,"pair":21},"note":"Pick 5, remaining target 21. Pair 7 + 14 = 21, which equals it, so three weights reach 26."}]}
```

The second trace looks for the total nearest to 1 in the shorter row minus 9, minus 4, 0, 3, 8, 12. It never finds an exact match, so every step keeps the best total so far. The step to study is the one that first reaches total 2, because it replaces an earlier best of minus 1 that was equally close on the other side; the next best is chosen only when it is strictly closer. After that step no later pick improves on it.

```trace
{"cells":[-9,-4,0,3,8,12],"pointers":["i","lo","hi"],"steps":[{"at":{"i":0,"lo":1,"hi":5},"vars":{"total":-1,"best":-1},"note":"-9 + -4 + 12 = -1, below the target 1. New best -1, replacing -13. lo becomes 2."},{"at":{"i":0,"lo":2,"hi":5},"vars":{"total":3,"best":-1},"note":"-9 + 0 + 12 = 3, above the target 1. Best stays -1. hi becomes 4."},{"at":{"i":0,"lo":2,"hi":4},"vars":{"total":-1,"best":-1},"note":"-9 + 0 + 8 = -1, below the target 1. Best stays -1. lo becomes 3."},{"at":{"i":0,"lo":3,"hi":4},"vars":{"total":2,"best":2},"note":"-9 + 3 + 8 = 2, above the target 1. New best 2, replacing -1. hi becomes 3."},{"at":{"i":1,"lo":2,"hi":5},"vars":{"total":8,"best":2},"note":"-4 + 0 + 12 = 8, above the target 1. Best stays 2. hi becomes 4."},{"at":{"i":1,"lo":2,"hi":4},"vars":{"total":4,"best":2},"note":"-4 + 0 + 8 = 4, above the target 1. Best stays 2. hi becomes 3."},{"at":{"i":1,"lo":2,"hi":3},"vars":{"total":-1,"best":2},"note":"-4 + 0 + 3 = -1, below the target 1. Best stays 2. lo becomes 3."},{"at":{"i":2,"lo":3,"hi":5},"vars":{"total":15,"best":2},"note":"0 + 3 + 12 = 15, above the target 1. Best stays 2. hi becomes 4."},{"at":{"i":2,"lo":3,"hi":4},"vars":{"total":11,"best":2},"note":"0 + 3 + 8 = 11, above the target 1. Best stays 2. hi becomes 3."},{"at":{"i":3,"lo":4,"hi":5},"vars":{"total":23,"best":2},"note":"3 + 8 + 12 = 23, above the target 1. Best stays 2. hi becomes 4."}]}
```

<!-- stage: code -->
### Exact Total And Nearest Total

```java
static boolean hasKSum(int[] sorted, int from, int k, long remaining) {
    if (k == 2) {
        int lo = from, hi = sorted.length - 1;
        while (lo < hi) {
            long pair = (long) sorted[lo] + sorted[hi];
            if (pair == remaining) return true;
            if (pair < remaining) lo++; else hi--;
        }
        return false;
    }
    for (int i = from; i + k <= sorted.length; i++)
        if (hasKSum(sorted, i + 1, k - 1, remaining - sorted[i])) return true;
    return false;
}

static boolean anyTripleReaches(int[] weights, long rating) {
    int[] copy = weights.clone();
    Arrays.sort(copy);
    return hasKSum(copy, 0, 3, rating);
}

static long nearestTripleTotal(int[] weights, long rating) {
    int[] copy = weights.clone();
    Arrays.sort(copy);
    long best = (long) copy[0] + copy[1] + copy[2];
    for (int i = 0; i + 2 < copy.length; i++) {
        int lo = i + 1, hi = copy.length - 1;
        while (lo < hi) {
            long total = (long) copy[i] + copy[lo] + copy[hi];
            if (Math.abs(total - rating) < Math.abs(best - rating)) best = total;
            if (total == rating) return total;
            if (total < rating) lo++; else hi--;
        }
    }
    return best;
}
```

Sorting is O(n log n), and each level of the recursion multiplies the work by at most n until the final sweep, so a call with `k` crates costs O(n^(k-1)) after the sort, which is quadratic for three crates. The recursion is at most `k` levels deep, so its stack use is O(k), and the copy adds O(n). The bound `i + k <= sorted.length` stops a level when too few crates remain to complete the group.

<!-- stage: applicability -->
### When A Total Can Be Chased

Think of this reduction when a question asks for a fixed count of values with a given total, the values can be sorted, and the caller does not care about their original order. If the count is two, a single sweep is enough. If it is three or four, peel off leading choices until two remain. The invariant to say aloud before coding is that each call owns a count, a start position and a remaining target, and that a pick lowers the count by one and the target by the picked value.

A false friend is the hash-set version of pair search. It also answers the pair question in linear time, but it spends memory, it has no sorted order to prune with, and it gives no guidance for the nearest-total variant. Another false friend is the sorted order itself: sorting loses original positions, so if the question asks for indices, a sort of a copy must remember them. A third is a count of values that is large, where the exponent grows with every level and a different method is needed.

In Java, add every sum in `long`, since three or four `int` values can pass the limit and wrap into a wrong sign that still compares plausibly. Compute the remaining target as `long` too, because subtracting a negative `int` from a large target also overflows an `int`. Clone the array before sorting unless the contract says the caller's array may be reordered.

<!-- stage: exercises -->
### Exercises

#### [Build] 3Sum (LeetCode 15)
<!-- id: tp-triple-exists -->

**Prerequisites.** The pair sweep on a sorted row, and the notion of a remaining target.

**Problem.** Given an unsorted array of integers and a `long` target, decide whether any three elements at distinct positions add up to the target. The caller's array must come back unchanged, so sort a copy.

**Constraints.** 0 <= nums.length <= 3000, any `int` values, and any `long` target. No list of triples is built, and the answer must come in O(n^2) time.

**Example 1.** Input `nums = [8, -3, 5, 11, 2, -6], target = 10`, output `true`.

**Example 2.** Input `nums = [8, -3, 5, 11, 2, -6], target = 40`, output `false`.

**Hint.** Which value does the pair sweep have to reach after one element is picked? Why must the sweep start just to the right of the picked position and not at the front of the row?

**Changed decision.** The answer is a yes or no, so there is no duplicate policy to write, and the input is promised to stay untouched, which moves the sort onto a copy.

#### [Vary] 3Sum Closest (LeetCode 16)
<!-- id: tp-closest-total -->

**Prerequisites.** The existence exercise above.

**Problem.** Given an array of at least three integers and a `long` target, return the sum of three elements at distinct positions that is nearest to the target. When two sums are equally near, either may be returned.

**Constraints.** 3 <= nums.length <= 1000 and any `int` values. Compute totals in `long` and sort a copy, so the caller's array stays as it was.

**Example 1.** Input `nums = [14, -6, 3, 9, -2, 7], target = 29`, output 30.

**Example 2.** Input `nums = [5, 5, 5], target = 0`, output 15.

**Hint.** Which comparison tells a sweep which end to move when no total is exact? When may a sweep stop early?

**Changed decision.** The goal is no longer a match but the smallest distance, so a best total is carried through every sweep and replaced only by a strictly closer one.

#### [Boundary] Overflowing Sum (Author exercise)
<!-- id: tp-overflow-sum -->

**Prerequisites.** The closest-total exercise above.

**Problem.** Given an array of integers that may sit at the limits of `int` and a `long` limit, return the largest sum of three elements at distinct positions that does not exceed the limit. If the array has fewer than three elements, or every triple sum exceeds the limit, return `Long.MIN_VALUE`.

**Constraints.** 0 <= nums.length <= 2000, any `int` values including both extremes, and any `long` limit. Every addition and every subtraction that touches a total must be done in `long`.

**Example 1.** Input `nums = [2147483647, 2147483647, 2147483647, -5, 10], limit = 4294967289`, output 4294967289.

**Example 2.** Input `nums = [2147483647, 2147483647, 2147483647], limit = 6442450940`, output `-9223372036854775808`.

**Hint.** For a picked element, which pair is the heaviest one that still fits under the remaining limit, and how does one sweep find it? Where would a plain `int` addition go wrong?

**Changed decision.** The comparison is an inequality against a remaining limit that lies far outside the `int` range, so a sweep that is correct on small numbers breaks silently in `int` arithmetic.

#### [Recognize] 4Sum (LeetCode 18)
<!-- id: tp-four-sum-count -->

**Prerequisites.** The overflow exercise above, and the duplicate-skipping lesson.

**Problem.** Given an array of integers near the limits of `int` and a `long` target, return how many distinct quadruplets of values add up to the target. Two quadruplets are the same when they hold the same values, whatever the positions. The input array must stay unchanged.

**Constraints.** 0 <= nums.length <= 400, any `int` values including both extremes, and any `long` target. Count in `long`, reduce two picks to a pair sweep, and aim at O(n^3) time.

**Example 1.** Input `nums = [-2147483648, 2147483647, -2147483648, 2147483647, 0, -1, 1], target = -2`, output 2.

**Example 2.** Input `nums = [2147483647, 2147483647, 2147483647, 2147483647, 2147483647], target = 8589934588`, output 1.

**Hint.** Which two levels of choice need the duplicate policy, and what does the sweep do right after it counts a match? Which expression needs `long` first, the sum or the remaining target?

**Changed decision.** Two picks are made before the sweep and the output is a count, so each match adds one to the count and then leaves both runs, and every intermediate target stays in `long`.
