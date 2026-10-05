<!-- lesson-kind: combination -->
<!-- lesson-id: prefix-state-maps -->
## Count And Measure Spans With Maps

<!-- stage: context -->
### Three Reports From One Map

An analytics team keeps a stream of signed amounts and answers three questions about it. How many stretches add up to a threshold? What is the longest stretch with equal credits and debits? How many stretches add up to a multiple of a divisor? Each report builds a `HashMap` that maps a running total to a number, and the three programs look almost alike.

The first report is correct. The second prints a count where the question asks for a length. The third undercounts as soon as some amounts are negative. These are two kinds of defect, and each one traces back to a choice inside the map. All three reports use the same map idea, so the defects have to come from two choices inside it. The problem is to decide what the map keys mean and what the map values remember.

<!-- stage: contributions -->
### What The Prefix And The Map Add

A running total from the start of the array fixes a position with a single number. The total at boundary `b` is the sum of the first `b` values, and the sum of any window is the difference of two such totals. The prefix idea contributes this reduction, from a question about windows to a question about pairs of earlier and later boundaries. It does not say how to find the matching earlier boundary without a loop.

A hash map answers that second question. It looks up a key in expected constant time, and it stores one value per key, so it can hold a count or a position. The map contributes the fast match. It does not say which quantity should be the key, and it does not say which value answers the question. The combination needs both parts. The prefix reduces a window to a pair of boundaries with a computable key, and the map finds the earlier partner.

<!-- stage: naive -->
### Checking Every Window For Each End

The direct method answers one of the three reports with two nested loops. For every end index it tries every start and counts the windows that end there and add up to `k`.

```java
static int[] endingCountsSlow(int[] nums, long k) {
    int[] out = new int[nums.length];
    for (int end = 0; end < nums.length; end++) {
        long sum = 0;
        for (int start = end; start >= 0; start--) {
            sum += nums[start];
            if (sum == k) out[end]++;
        }
    }
    return out;
}
```

For `[3, 1, 0, 4, -4, 4]` and `k = 4`, the method returns `[0, 1, 1, 2, 1, 3]`. The window `[3, 1]` ends at index 1. The window `[3, 1, 0]` ends at index 2, and the windows `[4]` and `[0, 4]` end at index 3.

```predict
The stream holds 40,000 amounts. How many (start, end) pairs does `endingCountsSlow` check?

It checks 40,000 * 40,001 / 2 = 800,020,000 pairs. Every end loops back over all earlier starts, so the cost is O(n^2).
```

<!-- stage: bottleneck -->
### The Loops Ignore What A Pair Needs

The method costs O(n^2) because it tests each pair of boundaries separately. The test for a pair is a comparison of two totals, and the later total is known when the end is fixed. The loop searches for earlier totals that match, one start after another, and it repeats that search at every end.

A map from totals to what they mean would turn the search into one lookup. The map needs a key that makes a pair match exactly when the window is valid, and it needs a value that holds whatever the report asks for. If the key is chosen wrongly, the lookup finds the wrong partners. If the value is chosen wrongly, the answer has the wrong meaning, such as a count in place of a length.

<!-- stage: insight -->
### Choose The Key, Then Choose The Value

Every prefix-and-map solution answers two questions before it writes a loop. The first fixes what two boundaries must share to form a valid window. The second fixes what the map remembers about each shared value.

#### The State Behind The Key

A **boundary state** is a value computed from the prefix up to one boundary, such that two boundaries with related states enclose a valid window. For a sum equal to `k`, the state is the raw total, and the partner of total `t` has total `t - k`. For a balance, the state is the running balance, and the partner has the same balance. For divisibility, the state is the normalized remainder `Math.floorMod(total, k)`, and the partner has the same remainder. Several parts can combine into one key, as in the second exercise below, which tracks two differences at once.

#### What The Map Stores

A **frequency map** stores how many earlier boundaries have a state. It answers how many windows exist, because every earlier boundary with the partner state starts one window. An **earliest-index map** stores the first position of each state and never overwrites it. It answers how long a window can be, because the earliest partner gives the longest window for a fixed end. The same keys serve both maps, and only the value differs.

#### Order Of Lookup And Seed

At each boundary the loop reads the partner state first and records the current state second. A record before the lookup lets a boundary pair with itself. The map starts with the state of boundary 0, which is the empty prefix. The frequency map holds count 1 for it, and the earliest-index map holds index -1.

<!-- names: boundary state, frequency map, earliest-index map -->

<!-- stage: variables -->
### Five Names And Their Roles

Every solution in this lesson follows the same five roles. The code uses shorter names such as `first`, `p`, `out` and `best` for them.

- **cur** is the running total through the current value and has type `long`.
- **state** is the key that the current boundary contributes, such as `cur`, a balance or a normalized remainder.
- **partner** is the key that an earlier boundary must have, computed from `state`.
- **seen** is the map from a state to a count or to the earliest index.
- **answer** is the number of windows or the longest length found so far.

The loop computes `state` and `partner`, reads `seen` at `partner`, updates `answer`, and then records `state` in `seen`. Only the key rule and the value rule differ between problems.

<!-- stage: trace -->
### One Count And One Remainder Count

#### Counting Windows That End At Each Index

The input is `[3, 1, 0, 4, -4, 4]` and `k = 4`. The frequency map holds how many earlier boundaries have each total, and the partner of total `t` is `t - 4`. Index 3 finds two windows, because the total 8 has the partners 4 twice. The output list grows with each step and ends as `[0, 1, 1, 2, 1, 3]`.

```trace
{"cells":[3,1,0,4,-4,4],"pointers":["i"],"steps":[{"at":{"i":-1},"vars":{"seen":"{0=1}","out":"[]"},"note":"The map starts with the total 0 once, for boundary 0."},{"at":{"i":0},"vars":{"cur":"3","partner":"-1","seen":"{0=1, 3=1}","out":"[0]"},"note":"Total 3 has partner -1, which occurs 0 times. So 0 windows end at index 0."},{"at":{"i":1},"vars":{"cur":"4","partner":"0","seen":"{0=1, 3=1, 4=1}","out":"[0, 1]"},"note":"Total 4 has partner 0, which occurs 1 time. So 1 window end at index 1."},{"at":{"i":2},"vars":{"cur":"4","partner":"0","seen":"{0=1, 3=1, 4=2}","out":"[0, 1, 1]"},"note":"Total 4 has partner 0, which occurs 1 time. So 1 window end at index 2."},{"at":{"i":3},"vars":{"cur":"8","partner":"4","seen":"{0=1, 3=1, 4=2, 8=1}","out":"[0, 1, 1, 2]"},"note":"Total 8 has partner 4, which occurs 2 times. So 2 windows end at index 3."},{"at":{"i":4},"vars":{"cur":"4","partner":"0","seen":"{0=1, 3=1, 4=3, 8=1}","out":"[0, 1, 1, 2, 1]"},"note":"Total 4 has partner 0, which occurs 1 time. So 1 window end at index 4."},{"at":{"i":5},"vars":{"cur":"8","partner":"4","seen":"{0=1, 3=1, 4=3, 8=2}","out":"[0, 1, 1, 2, 1, 3]"},"note":"Total 8 has partner 4, which occurs 3 times. So 3 windows end at index 5."}]}
```

#### Counting Windows By Remainder With A Target

The input is `[2, -1, 3, -3, 4]`, the divisor is 3 and the wanted remainder is 1. The state is `Math.floorMod(cur, 3)`, and the partner is `Math.floorMod(cur - 1, 3)`. Negative totals still give classes from 0 to 2. The loop finds 6 windows whose sum leaves remainder 1.

```trace
{"cells":[2,-1,3,-3,4],"pointers":["i"],"steps":[{"at":{"i":-1},"vars":{"seen":"{0=1}","count":"0"},"note":"The map starts with class 0 once, for boundary 0."},{"at":{"i":0},"vars":{"cur":"2","state":"2","partner":"1","seen":"{0=1, 2=1}","count":"0"},"note":"Total 2 has class 2 and partner class 1. The partner occurs 0 times, so the count becomes 0."},{"at":{"i":1},"vars":{"cur":"1","state":"1","partner":"0","seen":"{0=1, 1=1, 2=1}","count":"1"},"note":"Total 1 has class 1 and partner class 0. The partner occurs 1 time, so the count becomes 1."},{"at":{"i":2},"vars":{"cur":"4","state":"1","partner":"0","seen":"{0=1, 1=2, 2=1}","count":"2"},"note":"Total 4 has class 1 and partner class 0. The partner occurs 1 time, so the count becomes 2."},{"at":{"i":3},"vars":{"cur":"1","state":"1","partner":"0","seen":"{0=1, 1=3, 2=1}","count":"3"},"note":"Total 1 has class 1 and partner class 0. The partner occurs 1 time, so the count becomes 3."},{"at":{"i":4},"vars":{"cur":"5","state":"2","partner":"1","seen":"{0=1, 1=3, 2=2}","count":"6"},"note":"Total 5 has class 2 and partner class 1. The partner occurs 3 times, so the count becomes 6."}]}
```

<!-- stage: code -->
### Two Maps That Share A Key

```java
static int[] endingCounts(int[] nums, long k) {
    java.util.HashMap<Long, Integer> seen = new java.util.HashMap<>();
    seen.put(0L, 1);
    int[] out = new int[nums.length];
    long cur = 0;
    for (int i = 0; i < nums.length; i++) {
        cur += nums[i];
        out[i] = seen.getOrDefault(cur - k, 0);
        seen.merge(cur, 1, Integer::sum);
    }
    return out;
}

static int longestWithSum(int[] nums, long k) {
    java.util.HashMap<Long, Integer> first = new java.util.HashMap<>();
    first.put(0L, -1);
    long cur = 0;
    int best = 0;
    for (int i = 0; i < nums.length; i++) {
        cur += nums[i];
        Integer p = first.get(cur - k);
        if (p != null) best = Math.max(best, i - p);
        first.putIfAbsent(cur, i);
    }
    return best;
}
```

Both methods read `cur - k` before they record `cur`. The first stores counts and merges new counts into existing entries. The second stores positions and uses `putIfAbsent`, so the entry for a state never moves to a later index. A `Long` key compares by value, and a `long` prefix does not overflow for the sizes in the exercises.

<!-- stage: applicability -->
### When The Map Needs A Careful Key

#### The Invariant

The invariant is that at each boundary `b`, the map holds the states of boundaries `0` through `b - 1`, each with a count or its earliest index. A window ending at `b` is valid exactly when an earlier boundary has the partner state. The lookup then returns the count of such windows or the longest of them.

#### The False Friend

The false friend is a map that is correct for one report and reused for another. A frequency map answers how many windows exist, and it cannot tell the longest one. An earliest-index map answers the longest window, and it cannot count them. A raw `%` key matches the true remainder only for non-negative totals. Each of these looks right on small positive tests and fails on a stream with ties or negative amounts.

#### Conditions That Break The Fit

The condition of a valid window must reduce to a relation between two boundary states that a hash lookup can test, such as equality or a fixed difference. A condition like a window sum below a bound is an inequality, and a map cannot find all matching boundaries for it. The values may be negative, and the idea still holds. The method needs memory proportional to the number of distinct states.

<!-- stage: exercises -->
### Exercises

#### [Build] Subarray Sum Equals K (LeetCode 560)
<!-- id: psm-ending-counts -->

**Prerequisites.** The frequency map of this lesson and the lesson on counting windows with a target sum.

**Problem.** Take an integer array `nums` and an integer `k`. Return an array `out` of the same length where `out[i]` is the number of contiguous subarrays that end at index `i` and have sum `k`. This contract differs from LeetCode 560, which asks only for the total number.

**Constraints.** The limits are:
- **Length** is `1 <= nums.length <= 2 * 10^4`.
- **Values** are `int` values with `-1000 <= nums[i] <= 1000`.
- **Target** satisfies `-10^7 <= k <= 10^7`.
- **Return type** is `int[]` with `out[i] <= i + 1`.

**Example 1.** Input `nums = [3,1,0,4,-4,4]` and `k = 4`, output `[0,1,1,2,1,3]`.

**Example 2.** Input `nums = [1,1,1]` and `k = 2`, output `[0,1,1]`.

**Hint.** The count at index `i` is the map value of the partner key `cur - k`, read before `cur` is recorded. Store the value in `out[i]` and not in a running total.

**Changed decision.** The answer is reported per end index, so the lookup result is stored at each step and not accumulated.

#### [Vary] Contiguous Array (LeetCode 525)
<!-- id: psm-three-kinds -->

**Prerequisites.** The first exercise above and the lesson on balanced spans.

**Problem.** Given an array `nums` whose values are 0, 1 or 2, return the length of the longest contiguous subarray that contains as many 0 as 1 and as many 1 as 2. Return 0 when no non-empty subarray qualifies. This contract differs from LeetCode 525, which has two kinds of values.

**Constraints.** The limits are:
- **Length** is `1 <= nums.length <= 10^5`.
- **Values** are 0, 1 or 2.
- **State** is the pair of the 1 count minus the 0 count and the 2 count minus the 0 count.
- **Return value** is the length.

**Example 1.** Input `nums = [0,0,1,2,1,0]`, output 3.

**Example 2.** Input `nums = [2,2]`, output 0.

**Hint.** Two windows have equal counts of all three kinds when both differences return to the same pair. Combine the pair into one `long` key such as `(d1 + n) * (2n + 1) + (d2 + n)`.

**Changed decision.** The state grows from one balance to a pair of balances, so the key needs an encoding while the earliest-index idea stays.

#### [Boundary] Subarray Sums Divisible By K (LeetCode 974)
<!-- id: psm-target-remainder -->

**Prerequisites.** The first exercise above and the lesson on remainder classes.

**Problem.** Given an integer array `nums`, an integer `k` and an integer `r`, count the non-empty contiguous subarrays whose sum leaves remainder `r` when divided by `k`. Two integers leave the same remainder when their difference is divisible by `k`, and `r` may be negative or at least `k`. This contract differs from LeetCode 974, which fixes `r = 0`.

**Constraints.** The limits are:
- **Length** is `1 <= nums.length <= 3 * 10^4`.
- **Values** are `int` values with `-10^4 <= nums[i] <= 10^4`.
- **Divisor** satisfies `2 <= k <= 10^4`, and `r` satisfies `|r| <= 10^5`.
- **Return type** is `long`.

**Example 1.** Input `nums = [3,-1,2,4,-6,1]`, `k = 4` and `r = 1`, output 4.

**Example 2.** Input `nums = [5]`, `k = 3` and `r = -1`, output 1.

**Hint.** A window leaves remainder `r` when its two boundaries satisfy `state - partner ≡ r (mod k)`. Which normalized key does the partner have, and why must `r` be normalized too?

**Changed decision.** The wanted remainder is arbitrary, so the partner key shifts by `r`, and both the shift and the key need normalization.

#### [Recognize] Continuous Subarray Sum (LeetCode 523)
<!-- id: psm-min-length -->

**Prerequisites.** All exercises above.

**Problem.** Given an integer array `nums`, an integer `k` and an integer `minLen`, return `true` when some contiguous subarray of length at least `minLen` has a sum that is a multiple of `k`. Zero is a multiple of `k`. This contract differs from LeetCode 523, which fixes `minLen = 2` and uses non-negative values.

**Constraints.** The limits are:
- **Length** is `1 <= nums.length <= 10^5`.
- **Values** are `int` values with `|nums[i]| <= 10^9`.
- **Divisor** satisfies `1 <= k <= 10^9`, and `1 <= minLen <= nums.length`.
- **Return type** is `boolean`.

**Example 1.** Input `nums = [5,0,0]`, `k = 6` and `minLen = 3`, output `false`.

**Example 2.** Input `nums = [4,2,6,0,1]`, `k = 6` and `minLen = 4`, output `true`.

**Hint.** The earliest boundary in a class gives the longest window for the current end. A window of length `i - first` qualifies when that length is at least `minLen`.

**Changed decision.** The length rule becomes a parameter, so the map keeps positions and the check compares the span with `minLen`.
