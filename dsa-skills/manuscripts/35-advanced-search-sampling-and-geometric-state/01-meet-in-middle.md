<!-- lesson-kind: standard -->
<!-- lesson-id: meet-in-middle -->
## Meet In Middle

<!-- stage: context -->
### Forty Items And One Budget

A shopping app lets a customer pick any of 40 add-on items so that the total price lands as close as possible to a gift-card balance. A test with 12 items answers instantly. The same code on 40 items runs for the whole afternoon and the test never finishes. Each item is either in the order or out of it, so 40 items allow about 1.1 trillion different orders. No loop can look at that many totals in a normal request.

The problem is not unusual. Subset-sum questions with 30 to 44 items show up in interview rounds and in budget tools. The numbers are too large for one pass over all choices and too small to justify heavy machinery. This lesson asks one question. Can the work shrink from "all choices of 40 items" to something a laptop finishes in under a second, without losing the exact answer?

<!-- stage: naive -->
### Try Every Subset Directly

The direct method treats each subset as a bit pattern. A counter `mask` runs from 0 to `2^n - 1`, and bit `k` of the counter says whether item `k` is in the order. For every pattern the method adds up the chosen items and compares the total with the target. The code keeps the total in a `long`, because 40 prices near a billion overflow an `int`.

```java
final class NaiveClosest {
    static long closest(int[] a, long target) {
        int n = a.length;
        long best = Long.MAX_VALUE;
        for (long mask = 0; mask < (1L << n); mask++) {
            long sum = 0;
            for (int k = 0; k < n; k++) {
                if ((mask >> k & 1) == 1) sum += a[k];   // item k is in this subset
            }
            best = Math.min(best, Math.abs(sum - target));
        }
        return best;
    }
}
```

The method is correct and easy to check. For `n = 20` it makes about a million patterns and finishes at once. A different attempt would try dynamic programming over the total, as in the knapsack lessons, but prices up to a billion make the table of totals far too large.

```predict
Suppose the machine checks one pattern per nanosecond and ignores the inner loop. About how long does the loop take for n = 40? Now cut the 40 items into two groups of 20 and write down every subset total of each group separately. How many totals do you write down in all?

The loop needs 2^40, about 1.1 x 10^12, checks. At one per nanosecond that is roughly 1100 seconds, and the inner loop of 40 steps makes it far worse. Two groups of 20 produce 2^20, about one million, totals each, so about two million totals in all. Two million is a number that fits in memory and in a fraction of a second.
```

<!-- stage: bottleneck -->
### Recomputing Totals For Every Pair

The loop costs O(2^n * n) time and O(1) extra space. The `2^n` factor is the real problem. Look at what happens inside it. Take two patterns that agree on the first 20 items and differ only on the last 20. The loop adds up the same first 20 items for both patterns, then adds different last items. Across all patterns, the same 2^20 partial totals of the first group are rebuilt 2^20 times each.

The patterns also have a structure that the loop ignores. Choosing a subset of 40 items is the same as choosing a subset of the first 20 and, independently, a subset of the last 20. The final total is the sum of two numbers, one from each side, and the choices on the two sides never interact. The loop pairs every first-group choice with every last-group choice one at a time, and that pairing is where the 2^40 comes from.

Pairing is not necessary. If the loop fixes one first-group total `s` and wants the total closest to `target`, it needs one value from the last group that is closest to `target - s`. Finding the closest value to a given number in a list is a search question, and a sorted list answers it quickly. So the requirement is a way to write each group's totals once and look up the best partner for each.

<!-- stage: insight -->
### Split In Two And Search

<!-- names: halves, complement, unique split -->

#### Two Halves With One Rule

The method cuts the array at `mid = n / 2` into two **halves**: positions `0` to `mid - 1`, and positions `mid` to `n - 1`. Every subset of the array has a **unique split**: the part inside the first half and the part inside the second half. No position belongs to both halves, so no subset is split in two ways, and the two parts together give the whole subset back. The map from subsets of the array to pairs (first-half subset, second-half subset) is one to one and covers every pair.

The consequence is a total that adds up in two pieces. If the first-half part has sum `s` and the second-half part has sum `t`, the subset sum is `s + t`. The method lists all `2^mid` sums of the first half and all `2^(n - mid)` sums of the second half. Each list builds by doubling. It starts as `[0]`, and for each element `x` it appends a copy of the list shifted by `x`.

#### Looking Up The Complement

Fix one first-half sum `s`. The best partner is the second-half sum `t` that makes `s + t` closest to `target`. That means `t` should be closest to the **complement** `target - s`. The method sorts the second-half sums once. For each `s` a binary search finds the first sum at or above the complement, and the sum just before it. The closer of those two neighbours is the best partner for `s`. Taking the smallest distance over all `s` gives the answer.

#### What The Cost Becomes

Building both lists costs O(2^(n/2)) time. Sorting one list costs O(2^(n/2) * n). Each of the `2^(n/2)` lookups costs O(n). The total is O(2^(n/2) * n) time and O(2^(n/2)) space. For `n = 40` that is about a million entries per list instead of a trillion patterns.

The invariant is this: the pairs (first-half sum, second-half sum) stand for every subset exactly once, and for each first-half sum the lookup returns the best second-half sum.

<!-- stage: variables -->
### Lists, Midpoint And Best Distance

The code keeps six names, and each one is set in a known place.

- **mid** is `n / 2`. It is the first position of the second half.
- **left** is the array of all first-half sums, with `2^mid` entries.
- **right** is the sorted array of all second-half sums, with `2^(n - mid)` entries.
- **target** is the goal total, stored as a `long`.
- **need** is the complement `target - s` for the current first-half sum `s`. It changes once per loop step.
- **best** is the smallest distance found so far. It starts at `Long.MAX_VALUE` and only decreases.

The lists contain the empty sum 0, because each half may contribute no item. Equal sums stay in the lists as separate entries, because two different subsets can produce the same total.

<!-- stage: trace -->
### Tracing The Two Steps

#### Building Half Sums By Doubling

The first trace builds the sums of the half `3 5 2`. The pointer `i` marks the element being added. At the start the list holds only the empty sum 0. Adding 3 copies the list shifted by 3 and gives `0 3`. Adding 5 doubles the list again and gives `0 3 5 8`. Adding 2 doubles it a third time and gives eight sums, `0 3 5 8 2 5 7 10`. Two different subsets, `{5}` and `{3, 2}`, both have the sum 5, and the list keeps both copies. Sorting at the end gives `0 2 3 5 5 7 8 10`.

```trace
{"cells":[3,5,2],"pointers":["i"],"steps":[{"at":{"i":-1},"vars":{"sums":"0"},"note":"Start: the list holds only the empty sum 0."},{"at":{"i":0},"vars":{"element":3,"count":2,"sums":"0 3"},"note":"Add 3 to a shifted copy of the list. The list now has 2 sums."},{"at":{"i":1},"vars":{"element":5,"count":4,"sums":"0 3 5 8"},"note":"Add 5 to a shifted copy of the list. The list now has 4 sums."},{"at":{"i":2},"vars":{"element":2,"count":8,"sums":"0 3 5 8 2 5 7 10"},"note":"Add 2 to a shifted copy of the list. The list now has 8 sums."},{"at":{"i":3},"vars":{"count":8,"sums":"0 2 3 5 5 7 8 10"},"note":"Sort the list. Both copies of the sum 5 stay in the list."}]}
```

#### Searching For The Complement

The second trace searches the sorted second-half list `0 4 7 11 15` for the complement 8. The pointers `lo`, `mid` and `hi` bound the search. The search looks for the first entry at or above 8. It ends at index 3, where the value is 11. The entry before it, 7, is also a candidate. The distances are 3 for 11 and 1 for 7, so the best partner is 7 and the subset total misses the target by 1.

```trace
{"cells":[0,4,7,11,15],"pointers":["lo","mid","hi"],"steps":[{"at":{"lo":0,"mid":-1,"hi":5},"vars":{"need":8},"note":"Start: search the whole list for the first sum at or above 8."},{"at":{"lo":3,"mid":2,"hi":5},"vars":{"need":8,"value":7},"note":"7 is below 8, so lo moves to 3."},{"at":{"lo":3,"mid":4,"hi":4},"vars":{"need":8,"value":15},"note":"15 is at or above 8, so hi moves to 4."},{"at":{"lo":3,"mid":3,"hi":3},"vars":{"need":8,"value":11},"note":"11 is at or above 8, so hi moves to 3."},{"at":{"lo":3,"mid":3,"hi":3},"vars":{"need":8,"above":"11 (distance 3)","below":"7 (distance 1)"},"note":"The search ends at index 3. The neighbours 11 and 7 are at distance 3 and 1, so the best miss is 1."}]}
```

<!-- stage: code -->
### Closest Sum With Two Lists

#### Building And Searching

The method `halfSums` builds the sums of positions `from` to `to - 1` by doubling. The method `closest` sorts the second list and runs a lower-bound binary search for each first-half sum.

```java
final class MeetInMiddle {
    static long[] halfSums(int[] a, int from, int to) {
        long[] s = new long[1 << (to - from)];
        int size = 1;                                   // the empty subset gives sum 0
        for (int k = from; k < to; k++) {
            for (int j = 0; j < size; j++) s[size + j] = s[j] + a[k];   // copy shifted by a[k]
            size *= 2;                                  // the list doubles with each element
        }
        return s;
    }

    static long closest(int[] a, long target) {
        int mid = a.length / 2;
        long[] left = halfSums(a, 0, mid);
        long[] right = halfSums(a, mid, a.length);
        java.util.Arrays.sort(right);                   // binary search needs sorted order
        long best = Long.MAX_VALUE;
        for (long s : left) {
            long need = target - s;                     // the complement of this first-half sum
            int lo = 0, hi = right.length;              // find the first index with right[idx] >= need
            while (lo < hi) {
                int m = (lo + hi) >>> 1;
                if (right[m] < need) lo = m + 1; else hi = m;
            }
            if (lo < right.length) best = Math.min(best, Math.abs(right[lo] - need));
            if (lo > 0) best = Math.min(best, Math.abs(need - right[lo - 1]));
        }
        return best;
    }
}
```

#### Cost

- **halfSums** costs O(2^k) time and space for `k` elements.
- **closest** costs O(2^(n/2) * n) time and O(2^(n/2)) space.
- **Memory** for `n = 40` is two arrays of about a million `long` values, near 16 MB.

<!-- stage: applicability -->
### When Splitting In Half Applies

#### Recognizing The Pattern

Use this method when the statement lets each item be taken or left, when `n` is between about 30 and 44, and when the objective is a sum of per-item contributions. The limits are the cue. A limit of `n <= 20` allows plain enumeration and a limit near 100 or more points to a different tool. The invariant to protect is that each full choice maps to exactly one pair of half choices.

#### False Friends

A knapsack table is a false friend when values are small. It runs in O(n * W) time, and it beats this method when the total `W` is a few thousand. A greedy choice of the largest item that still fits is another false friend, because subset sum has no greedy rule that stays exact. Two pointers over a sorted array look like pairing, but they pair two elements, not two subsets.

#### When The Method Does Not Apply

If the objective does not split into a sum, as in a product with sign changes or a cost that depends on neighbouring picks across the middle, the halves interact and the pair lookup is wrong. If `n` is 60 or more, `2^30` entries per list no longer fit in memory, so the method is a no-go.

<!-- stage: exercises -->
### Exercises

#### [Build] Half Subset Sums (Author exercise)
<!-- id: mm35-half-subset-sums -->

**Prerequisites.** The doubling construction from this lesson.

**Problem.** Write `long[] subsetSums(int[] a)`. The method returns every subset sum of `a` in increasing order. There is one entry for each subset of positions, so the result has `2^a.length` entries. The empty subset contributes the sum 0.

**Constraints.** The limits are:
- **Length** of `a` is from 0 to 20.
- **Values** are `int` values from -10^9 to 10^9, possibly equal or negative.
- **Result** is a new array that is sorted in non-decreasing order.
- **Sums** use `long` arithmetic.

**Example 1.** Input `a = [3, 3]`, output `[0, 3, 3, 6]`.

**Example 2.** Input `a = [4, -2, 5]`, output `[-2, 0, 2, 3, 4, 5, 7, 9]`.

**Hint.** How long is the result after each element, and what does the new half of the array hold?

**Changed decision.** Basic case: build the sums for one array, with no target and no search.

#### [Vary] Closest Pair Of Half Sums (Author exercise)
<!-- id: mm35-closest-pair-half-sums -->

**Prerequisites.** The Half Subset Sums exercise above. This exercise adds a second array and a target.

**Problem.** Write `long closestPair(int[] left, int[] right, long target)`. Pick one subset of `left` and one subset of `right`, either possibly empty. Let `total` be the sum of the two subsets together. Return the smallest value of `|total - target|` over all such picks.

**Constraints.** The limits are:
- **Lengths** of both arrays are from 0 to 20.
- **Values** are `int` values from -10^9 to 10^9.
- **Target** is a `long` from -10^15 to 10^15.
- **Mutation** is not allowed on the inputs.

**Example 1.** Input `left = [5, 10]`, `right = [3, 6]`, `target = 14`, output `0`, because 5 and 3 + 6 give 14.

**Example 2.** Input `left = [7, 2]`, `right = [4, -9]`, `target = 20`, output `7`, because the best total is 13.

**Hint.** Which of the two lists needs to be sorted, and how many neighbours of the complement must be checked?

**Changed decision.** The split of the array is given by the input, and the objective is a distance to a target.

#### [Boundary] Duplicates And Long Sums (Author exercise)
<!-- id: mm35-duplicates-long-sums -->

**Prerequisites.** The Closest Pair Of Half Sums exercise above. This exercise changes the goal from a distance to an exact count and keeps every equal sum.

**Problem.** Write `long countSubsets(int[] a, long target)`. The method counts the subsets of positions of `a` whose sum equals `target`. Two subsets are different when their position sets are different, even if their values are equal. The empty subset counts when `target` is 0.

**Constraints.** The limits are:
- **Length** of `a` is from 0 to 40.
- **Values** are `int` values from -10^9 to 10^9, and they may repeat or equal 0.
- **Target** is a `long`.
- **Result** fits in a `long`.

**Example 1.** Input `a = [1, 1, 1]`, `target = 2`, output `3`.

**Example 2.** Input `a = [1000000000, 1000000000, 1000000000, 1000000000]`, `target = 3000000000`, output `4`.

**Hint.** When the lookup finds one equal sum, how many equal sums sit next to it in the sorted list?

**Changed decision.** The lookup returns how many partners match exactly, not which partner is nearest, and the code must keep multiplicity.

#### [Recognize] Closest Subsequence Sum (LeetCode 1755)
<!-- id: mm35-closest-subsequence-sum -->

**Prerequisites.** The Duplicates And Long Sums exercise above.

**Problem.** Given an integer array `nums` and an integer `goal`, choose a subsequence of `nums`, which is any set of positions kept in their original order and possibly empty. Return the minimum possible value of `|sum - goal|`, where `sum` is the sum of the chosen elements.

**Constraints.** The limits are:
- **Length** of `nums` is from 1 to 40.
- **Values** are integers from -10^7 to 10^7.
- **Goal** is an integer from -10^9 to 10^9.

**Example 1.** Input `nums = [4, -3, 8, 1]`, `goal = 10`, output `0`.

**Example 2.** Input `nums = [3, 8]`, `goal = -20`, output `20`.

**Hint.** Which limit on `nums.length` tells you that a plain enumeration of all subsequences is out of reach, and what would two enumerations of half the size give?

**Changed decision.** The statement hides the split. The reader must see that the length limit of 40 asks for two half enumerations.
