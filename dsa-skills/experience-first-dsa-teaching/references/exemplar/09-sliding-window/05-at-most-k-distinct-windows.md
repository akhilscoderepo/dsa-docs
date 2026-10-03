<!-- lesson-kind: standard -->
<!-- lesson-id: at-most-k-distinct-windows -->
## At-Most-K Distinct Windows

<!-- stage: context -->
### The Two-Badge Shift

A warehouse door scanner logs the badge number of whoever passes through. A supervisor is reviewing one night's log and asks a staffing question: what is the longest stretch of consecutive scans in which at most two different people used the door? The same person may badge in a hundred times and that counts as one. Only the number of different badges matters.

The condition is a budget on variety. Repeating a value costs nothing, and the first appearance of a new value spends one unit of the budget. Fruit pickers who carry two baskets, playlists limited to a few genres, and a text with at most `k` different letters all have this shape, and in each of them the question is how long a stretch can be before the budget is exceeded.

<!-- stage: naive -->
### Extend Until The Budget Breaks

From each starting scan, keep walking right while remembering which badges have appeared in a set, and stop when a third different badge shows up. Record how far that start got.

```java
static int longestWithAtMostKBruteForce(int[] scans, int k) {
    int best = 0;
    for (int start = 0; start < scans.length; start++) {
        Set<Integer> seen = new HashSet<>();
        for (int end = start; end < scans.length; end++) {
            seen.add(scans[end]);
            if (seen.size() > k) break;
            best = Math.max(best, end - start + 1);
        }
    }
    return best;
}
```

The code is easy to trust, and it gives the right answer on every input.

<!-- stage: bottleneck -->
### A New Set For Every Start

Every start builds a brand-new set and re-reads the same scans that the previous start read. If the whole night used only two badges, no start ever breaks, and start `i` walks `n - i` scans, which makes the total about `n^2 / 2`. A night of 100,000 scans costs five billion set insertions, each of which hashes a boxed `Integer`.

The method costs O(n^2) time, and the set is thrown away and rebuilt every time. The information we need from one start is almost identical to what the next start needs, because the two stretches differ by a single scan at the left.

<!-- stage: insight -->
### Count Each Value

A set remembers that a value appeared but not how many times, and that is exactly what the left edge needs. When the leftmost scan is dropped, we must know whether another copy of that badge is still inside. If one is, the number of distinct badges does not change. If it was the last copy, the badge disappears and the distinct count falls by one.

So we keep a **count map**: a map from each value in the window to the number of times it occurs there. The number of keys in the map is the number of distinct values, and that is the quantity the budget limits. A window whose distinct count is at most `k` is valid. Taking in a value increases its count and may add a key. Dropping a value decreases its count and removes the key only when the count reaches zero.

<!-- names: count map, distinct-count budget -->

This is the same longest-valid pattern from earlier in the chapter, with a different violation counter. The **distinct-count budget** is the number of different values we can afford, and the window repairs itself from the left whenever the map has more keys than the budget allows. The monotonicity check passes, since removing elements from a valid window can only lower the number of distinct values, never raise it. That is why the left edge never has to move backward.

One consequence is easy to overlook. A single arrival can push the distinct count only from `k` to `k + 1`, but repairing may take many removals, because the leftmost values may be repeats whose copies keep their keys alive. The loop continues until a key actually disappears.

<!-- stage: variables -->
### Four Variables

The map `count` holds a positive count for every value currently inside the window and no entries for any other value. That is the invariant that makes `count.size()` trustworthy. The indices `left` and `right` bound the window, and `best` records the longest valid window measured so far. The budget `k` is an input and does not change. Nothing else needs to be stored.

<!-- stage: trace -->
### One Run Through

Take the scans `[1, 2, 1, 3, 3, 2, 2, 4]` with a budget of two distinct badges. The first three scans, 1, 2 and 1, fit inside the budget, and the window grows to length 3.

At index 3 the badge 3 arrives, which makes three distinct values and exceeds the budget. The repair starts at the left. Dropping the leftmost scan removes one copy of badge 1, but another copy of 1 sits at index 2, so the key stays and the distinct count is still three. Dropping the next scan removes the only copy of badge 2, and now the key disappears. The window covers indices 2 and 3, holding 1 and 3. Two removals were needed for one arrival, and the first of them did not help at all.

Badge 3 arrives again at index 4, and the window `1, 3, 3` stays valid. At index 5 badge 2 arrives and the budget is exceeded again. The leftmost scan, at index 2, is the only copy of 1, so one removal is enough. The window now holds `3, 3, 2`.

Index 6 brings a second 2. The stretch `3, 3, 2, 2` is the longest valid one so far, with four scans and two distinct badges. A newcomer then walks in at index 7, badge 4, and the repair has to shed both copies of badge 3 before that key finally vanishes. Nothing longer than four ever appears, so four is the answer.

```trace
{"cells":[1,2,1,3,3,2,2,4],"pointers":["left","right"],"steps":[{"at":{"left":0,"right":0},"vars":{"distinct":1,"best":0},"note":"Take in index 0 (value 1). A new value joins, so the distinct count rises."},{"at":{"left":0,"right":0},"vars":{"distinct":1,"best":1},"note":"Measure: the window holds 1 values, so best is 1."},{"at":{"left":0,"right":1},"vars":{"distinct":2,"best":1},"note":"Take in index 1 (value 2). A new value joins, so the distinct count rises."},{"at":{"left":0,"right":1},"vars":{"distinct":2,"best":2},"note":"Measure: the window holds 2 values, so best is 2."},{"at":{"left":0,"right":2},"vars":{"distinct":2,"best":2},"note":"Take in index 2 (value 1)."},{"at":{"left":0,"right":2},"vars":{"distinct":2,"best":3},"note":"Measure: the window holds 3 values, so best is 3."},{"at":{"left":0,"right":3},"vars":{"distinct":3,"best":3},"note":"Take in index 3 (value 3). A new value joins, so the distinct count rises. It exceeds the budget, so the window must be repaired."},{"at":{"left":1,"right":3},"vars":{"distinct":3,"best":3},"note":"Remove index 0 (value 1) from the left. Other copies remain, so the map keeps it."},{"at":{"left":2,"right":3},"vars":{"distinct":2,"best":3},"note":"Remove index 1 (value 2) from the left. That was its last copy, so the value leaves the map. The window is valid again."},{"at":{"left":2,"right":3},"vars":{"distinct":2,"best":3},"note":"Measure: the window holds 2 values, so best is 3."},{"at":{"left":2,"right":4},"vars":{"distinct":2,"best":3},"note":"Take in index 4 (value 3)."},{"at":{"left":2,"right":4},"vars":{"distinct":2,"best":3},"note":"Measure: the window holds 3 values, so best is 3."},{"at":{"left":2,"right":5},"vars":{"distinct":3,"best":3},"note":"Take in index 5 (value 2). A new value joins, so the distinct count rises. It exceeds the budget, so the window must be repaired."},{"at":{"left":3,"right":5},"vars":{"distinct":2,"best":3},"note":"Remove index 2 (value 1) from the left. That was its last copy, so the value leaves the map. The window is valid again."},{"at":{"left":3,"right":5},"vars":{"distinct":2,"best":3},"note":"Measure: the window holds 3 values, so best is 3."},{"at":{"left":3,"right":6},"vars":{"distinct":2,"best":3},"note":"Take in index 6 (value 2)."},{"at":{"left":3,"right":6},"vars":{"distinct":2,"best":4},"note":"Measure: the window holds 4 values, so best is 4."},{"at":{"left":3,"right":7},"vars":{"distinct":3,"best":4},"note":"Take in index 7 (value 4). A new value joins, so the distinct count rises. It exceeds the budget, so the window must be repaired."},{"at":{"left":4,"right":7},"vars":{"distinct":3,"best":4},"note":"Remove index 3 (value 3) from the left. Other copies remain, so the map keeps it."},{"at":{"left":5,"right":7},"vars":{"distinct":2,"best":4},"note":"Remove index 4 (value 3) from the left. That was its last copy, so the value leaves the map. The window is valid again."},{"at":{"left":5,"right":7},"vars":{"distinct":2,"best":4},"note":"Measure: the window holds 3 values, so best is 4."}]}
```

<!-- stage: code -->
### The Java Blueprint

```java
static int longestWithAtMostK(int[] scans, int k) {
    if (k <= 0) return 0;                       // contract: a zero budget allows no value at all
    Map<Integer, Integer> count = new HashMap<>();
    int left = 0, best = 0;
    for (int right = 0; right < scans.length; right++) {
        count.merge(scans[right], 1, Integer::sum);
        while (count.size() > k) {
            int out = scans[left];
            int remaining = count.merge(out, -1, Integer::sum);
            if (remaining == 0) count.remove(out);   // without this, size() overstates the distinct count
            left++;
        }
        best = Math.max(best, right - left + 1);
    }
    return best;
}
```

The line that removes the key at zero is the whole technique in miniature. If a count of zero stays in the map, `count.size()` keeps counting a value that is no longer in the window, the budget looks exceeded when it is not, and the answer comes out too short. No exception is thrown, so the bug is silent. The `merge` call is a compact way to update a boxed count, and it returns the new value, which is what the zero check needs. Comparing boxed integers with `==` is a separate trap that this code avoids by comparing the returned value to a literal `0`.

The repair loop never rewinds, so the whole scan costs O(n) time, with O(k) extra space because the map never holds more than `k + 1` keys. When the values are small known integers or lowercase letters, a plain `int[]` plus a separate integer for the distinct count is faster and avoids boxing. The count for a value then moves from zero to one when the distinct count increases, and from one to zero when it decreases.

<!-- stage: applicability -->
### When It Applies

Use an at-most-`k`-distinct window when the question limits how many different values a contiguous range may contain and asks for its longest length. The invariant to state is that `count` has a positive entry for exactly the values in `left..right`, so `count.size()` is the distinct count, and after the repair loop it is at most `k`.

The false friend is the frequency-signature window, which demands that the counts match a target exactly. Here only the number of keys matters, and any values are allowed. A second false friend is the set. A set cannot say whether dropping a scan removes the last copy, so it forces a rebuild and brings back the quadratic method. The count map is what lets the left edge move one step at a time.

Do not confuse this with the next lesson's question. This lesson asks for the longest window with at most `k` distinct values. A problem that asks for the number of subarrays with exactly `k` distinct values is not monotone in the same way, and it is solved by subtracting two at-most counts.

Check the edge budgets. A budget of zero allows no values at all, and without a guard the loop would try to repair an empty window forever or drive a count negative. A budget larger than the number of distinct values never triggers a repair, so the answer is the whole input. State both in the contract.

<!-- stage: exercises -->
### Exercises

#### [Build] Longest Segment With One Distinct Value (Author exercise)
<!-- id: sw-one-distinct-value -->

**Prerequisites.** The longest-valid lesson for the repair loop; this lesson for distinct counting.

**Problem.** Given an integer array, return the length of the longest contiguous segment in which all values are equal. Solve it with a window that tracks one active value and how many times it appears, not by comparing neighbors only.

**Constraints.** 0 <= nums.length <= 10^5 and -10^9 <= nums[i] <= 10^9. Target O(n) time and O(1) extra space.

**Example 1.** Input `nums = [4, 4, 2, 2, 2, 4]`, output `3`, from the run of three 2s.

**Example 2.** Input `nums = []`, output `0`, because an empty array has no segment.

**Hint.** When a different value arrives, how much of the window must be discarded, and what does the single active key become?

**Changed decision.** First rung of the ladder: the distinct budget is one, so the map degenerates to one key and one count.

#### [Vary] Fruit Into Baskets (LeetCode 904)
<!-- id: sw-fruit-into-baskets -->

**Prerequisites.** The exercise above.

**Problem.** Trees stand in a row and tree `i` bears fruit of type `fruits[i]`. You carry two baskets, and each basket can hold only one type of fruit, in any quantity. You choose a starting tree, then walk right taking one fruit from every tree, and you must stop at the first tree whose type fits neither basket. Return the most fruit you can collect.

**Constraints.** 1 <= fruits.length <= 10^5 and 0 <= fruits[i] < fruits.length. Target O(n) time.

**Example 1.** Input `fruits = [4, 4, 5, 4, 6, 6]`, output `4`, from the first four trees.

**Example 2.** Input `fruits = [0, 3, 2, 3, 3, 2]`, output `5`, from the last five trees. Starting at the first tree would stop after two.

**Hint.** What is the longest stretch with at most two types of fruit, and what happens to the map when the left edge drops a tree whose type still appears later in the stretch?

**Changed decision.** The budget becomes two, so the map may hold two keys and repair must keep dropping until a key actually vanishes.

#### [Boundary] K Is Zero (Author exercise)
<!-- id: sw-k-is-zero -->

**Prerequisites.** The two exercises above.

**Problem.** Given an integer array `nums` and an integer `k`, return the length of the longest contiguous segment containing at most `k` distinct values. The value `k` may be zero. A segment with zero distinct values is the empty segment.

**Constraints.** 0 <= nums.length <= 10^5, 0 <= k <= 10^5, and -10^9 <= nums[i] <= 10^9. Target O(n) time.

**Example 1.** Input `nums = [1, 2]`, `k = 0`, output `0`. No value is allowed, so no segment qualifies.

**Example 2.** Input `nums = [5, 5, 5]`, `k = 3`, output `3`. The budget exceeds the distinct count, so the repair loop never runs.

**Hint.** If the budget is zero, what would the repair loop do after the first arrival, and why must the contract be handled before the loop rather than inside it?

**Changed decision.** The budget sits at both extremes, zero and larger than the data, so the guard and the never-repair path are exercised.

#### [Recognize] Longest Substring With At Most K Distinct Characters (Author exercise)
<!-- id: sw-at-most-k-characters -->

**Prerequisites.** The three exercises above.

**Problem.** Return the length of the longest substring of the string `s` that contains at most `k` distinct characters, where `k` is a non-negative integer.

**Constraints.** 0 <= s.length <= 5 * 10^4, 0 <= k <= 50, and `s` consists of ASCII characters. Target O(n) time.

**Example 1.** Input `s = "eceba"`, `k = 2`, output `3`, from the substring `"ece"`.

**Example 2.** Input `s = "aa"`, `k = 1`, output `2`.

**Hint.** The values are now characters. Which structure replaces the boxed map when the character domain is small and known?

**Changed decision.** The domain moves from integers to characters, so a fixed-size table and a separate distinct counter can replace the map.
