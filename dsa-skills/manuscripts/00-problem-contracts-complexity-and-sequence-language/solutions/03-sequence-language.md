<!-- solutions-for: 03-sequence-language -->
### Sequence Language

#### Solution: [Build] Classify [2,4] (Author exercise)
<!-- id: pc-classify-2-4 -->

**Approach.** First, find the position of each candidate value in `[1,2,3,4]`. The value 2 sits at position 1 and the value 4 at position 3. Second, test whether the positions strictly increase. They do (1 then 3), so the original order is kept and the candidate is a subsequence. Third, test whether each position is exactly one more than the previous. Position 2 is skipped, so the test fails and the candidate is not a subarray. Fourth, check membership. Both values occur in `nums`, so the candidate is a subset. The code derives each verdict from the position list, so no verdict rests on how the values look. The invariant is that every verdict reads only the positions.

**Complexity.** Time: O(n * m) in this brute-force code, because each of the `m` candidate values scans up to `n` positions of the array. Keeping a value-to-position map would reduce this to O(n + m). Space: O(m), because the position array holds one entry per candidate value.

```java run
public final class ClassifyPositions {
    /**
     * Returns the position of each candidate value in nums, or -1 if a value is absent.
     * Time: O(n * m), because each of m candidate values scans up to n positions.
     * Space: O(m), because the result holds one position per candidate value.
     */
    static int[] positionsOf(int[] nums, int[] cand) {
        // One slot per candidate value: this array is the only extra memory.
        int[] pos = new int[cand.length];
        // Outer loop runs m times, one search per candidate value.
        for (int j = 0; j < cand.length; j++) {
            // -1 marks "not found", so a missing value cannot pass for position 0.
            pos[j] = -1;
            // Inner scan costs up to n steps; the break stops at the first match (values are distinct).
            for (int i = 0; i < nums.length; i++) if (nums[i] == cand[j]) { pos[j] = i; break; }
        }
        // Callers read verdicts from these positions only.
        return pos;
    }
    /**
     * Tests whether the positions are consecutive, which is the subarray rule.
     * Time: O(m), because one pass compares each position with its predecessor.
     * Space: O(1), because only the loop index is stored.
     */
    // Each position must be exactly one more than the previous; any gap or drop fails the test.
    static boolean noGaps(int[] pos) { for (int j = 1; j < pos.length; j++) if (pos[j] != pos[j - 1] + 1) return false; return true; }
    /**
     * Tests whether the positions strictly increase, which is the subsequence rule.
     * Time: O(m), because one pass compares neighbours.
     * Space: O(1), because only the loop index is stored.
     */
    // Gaps are allowed, so only a position that fails to grow breaks the order.
    static boolean ordered(int[] pos) { for (int j = 1; j < pos.length; j++) if (pos[j] <= pos[j - 1]) return false; return true; }

    public static void main(String[] args) {
        int[] nums = {1, 2, 3, 4};
        // Positions of [2,4] must be 1 and 3.
        int[] p = positionsOf(nums, new int[] {2, 4});
        if (p[0] != 1 || p[1] != 3) throw new AssertionError("positions");
        // Position 2 is skipped, so [2,4] is not a subarray but is a subsequence.
        if (noGaps(p)) throw new AssertionError("[2,4] is not a subarray");
        if (!ordered(p)) throw new AssertionError("[2,4] is a subsequence");
        // Consecutive positions make [2,3] pass both tests.
        int[] q = positionsOf(nums, new int[] {2, 3});
        if (!noGaps(q) || !ordered(q)) throw new AssertionError("[2,3] is all three");
    }
}
```

#### Solution: [Vary] Order Matters (Author exercise)
<!-- id: pc-order-matters -->

**Approach.** First, find the positions of `[4,2]`. They are 3 and then 1, so the positions fall. Second, apply the no-gaps test. A drop is not "one more than the previous position", so the test fails and the candidate is not a subarray. Third, apply the ordered test. The positions do not increase, so the candidate is not a subsequence. Fourth, apply the membership test. Both values occur in the array, and a subset needs nothing more, so the candidate is a subset. The decision that differs from `[2,4]` is the direction of the positions. The invariant is that a subset test ignores positions, while the other two tests use them.

**Complexity.** Time: O(n), because each `indexOf` call scans the array of `n` values at most once, and the code makes a constant number of calls. Space: O(1), because the code stores only a few integers.

```java run
public final class OrderMatters {
    /**
     * Returns the first position of v in a, or -1 if v is absent.
     * Time: O(n), because the scan may visit every element once.
     * Space: O(1), because only the loop index is stored.
     */
    // Scan left to right; the first match is the position, and -1 means "absent".
    static int indexOf(int[] a, int v) { for (int i = 0; i < a.length; i++) if (a[i] == v) return i; return -1; }

    public static void main(String[] args) {
        int[] nums = {1, 2, 3, 4};
        // Look up the positions of 4 and then 2, in the order the candidate lists them.
        int first = indexOf(nums, 4), second = indexOf(nums, 2);
        if (first != 3 || second != 1) throw new AssertionError("positions of 4 then 2");
        // The second position is smaller, so the order is reversed and the subsequence test fails.
        if (second >= first) throw new AssertionError("positions should fall, so the order is reversed");
        // Membership alone decides the subset verdict.
        boolean member = indexOf(nums, 4) >= 0 && indexOf(nums, 2) >= 0;
        if (!member) throw new AssertionError("both values are members, so [4,2] is a subset");
        // The whole array [1,2,3,4] starts at position 0 and ends at the last position, so it passes all three.
        int whole = indexOf(nums, 1);
        if (whole != 0 || indexOf(nums, 4) != nums.length - 1) throw new AssertionError("the whole array spans every position");
    }
}
```

#### Solution: [Boundary] Empty Choice (Author exercise)
<!-- id: pc-empty-choice -->

**Approach.** First, read the specification. It must say whether the empty subarray is legal, because its sum is 0 and 0 beats every sum on an all-negative array. Second, start `best` from the right value. With the non-empty requirement, `best` starts at `Integer.MIN_VALUE`, so the first block sum replaces it. With the empty choice allowed, `best` starts at 0, the sum of nothing. Third, try every start position. For each start, extend the end one step at a time and keep a running sum, so each block sum costs one addition. Fourth, after each extension, keep the larger of `best` and the block sum. For `[-8,-3,-6]` the non-empty answer is -3, the best single value. The empty-allowed answer is 0. The invariant is that `best` always holds the maximum over the legal blocks seen so far.

**Complexity.** Time: O(n^2), because the two nested loops visit every start and end pair once, and a running sum makes each block cost O(1). Space: O(1), because the code stores only `best`, `sum` and the loop indexes.

```java run
public final class EmptyChoice {
    /**
     * Returns the maximum subarray sum, with or without the empty subarray.
     * Time: O(n^2), because every (start, end) pair is visited once with an O(1) update.
     * Space: O(1), because only best, sum and two indexes are stored.
     * Invariant: best is the maximum over all legal blocks seen so far.
     */
    static int bestBlock(int[] nums, boolean allowEmpty) {
        // Starting at 0 models "choose nothing"; MIN_VALUE means every legal block must replace it.
        int best = allowEmpty ? 0 : Integer.MIN_VALUE;
        // Each start position begins a new family of blocks; this loop runs n times.
        for (int start = 0; start < nums.length; start++) {
            // Reset the running sum so it covers exactly the block [start, end].
            int sum = 0;
            // Extend the block one position at a time; together with the outer loop this costs O(n^2).
            for (int end = start; end < nums.length; end++) {
                // Add one value instead of re-summing the block, so each step costs O(1).
                sum += nums[end];
                // Keep the larger sum, which maintains the invariant.
                best = Math.max(best, sum);
            }
        }
        // best covers every non-empty block, plus the empty one when allowed.
        return best;
    }

    public static void main(String[] args) {
        int[] nums = {-8, -3, -6};
        // All-negative input: the non-empty answer is the largest single value, and the empty-allowed answer is 0.
        if (bestBlock(nums, false) != -3) throw new AssertionError("non-empty answer");
        if (bestBlock(nums, true) != 0) throw new AssertionError("empty allowed answer");
        // A positive array gives the same answer under both specifications.
        if (bestBlock(new int[] {2, -1, 3}, false) != bestBlock(new int[] {2, -1, 3}, true)) throw new AssertionError("a positive array does not expose the difference");
    }
}
```

#### Solution: [Recognize] Contiguous Maximum (Author exercise)
<!-- id: pc-contiguous-maximum -->

**Approach.** First, list the blocks of consecutive positions that contain both the 5 and the 4. Only one exists, the whole array, and it also contains the -10 between them, so its sum is -1. Second, compare the other blocks: `[5]` gives 5, `[-10]` gives -10, `[4]` gives 4, and `[5,-10]` gives -5. The best subarray sum is therefore 5. Third, enumerate subsequences with a bit mask. Bit `i` of the mask says whether position `i` is chosen, so positions 0 and 2 give 9 and skip the -10. The best subsequence sum is therefore 9. The data and the objective are identical, so the position rule alone moves the answer from 5 to 9. The invariant in each function is that `best` holds the maximum over the candidates examined so far.

**Complexity.** Time: O(n^2) for the subarray function, because it visits each start and end pair once. Time: O(2^n * n) for the subsequence function, because it tests `2^n` masks and sums up to `n` values for each. Space: O(1) for both, because each keeps only `best`, a sum, and loop indexes.

```java run
public final class ContiguousMaximum {
    /**
     * Returns the maximum sum over all non-empty subarrays.
     * Time: O(n^2), because each (l, r) pair is visited once with an O(1) update.
     * Space: O(1), because only best, s and two indexes are stored.
     * Invariant: best is the maximum sum over the blocks visited so far.
     */
    static int bestSubarray(int[] a) {
        // MIN_VALUE is replaced by the first block sum, which keeps the result non-empty.
        int best = Integer.MIN_VALUE;
        // l is the left end of the block; the loop runs n times.
        for (int l = 0; l < a.length; l++) { int s = 0;
            // Extending r one step adds one value, so the running sum s costs O(1) per block.
            for (int r = l; r < a.length; r++) { s += a[r]; best = Math.max(best, s); } }
        return best;
    }
    /**
     * Returns the maximum sum over all non-empty subsequences.
     * Time: O(2^n * n), because there are 2^n masks and each is summed in O(n).
     * Space: O(1), because only best, s and two indexes are stored.
     * Invariant: best is the maximum sum over the masks visited so far.
     */
    static int bestSubsequence(int[] a) {
        // Same starting value as above, so the result is also non-empty.
        int best = Integer.MIN_VALUE;
        // Mask 0 is the empty selection, so start at 1; each mask picks one set of positions.
        for (int mask = 1; mask < (1 << a.length); mask++) {
            // Sum only the positions whose bit is set in the mask.
            int s = 0;
            // This inner loop costs O(n) per mask, which gives the factor n.
            for (int i = 0; i < a.length; i++) if ((mask >> i & 1) == 1) s += a[i];
            // Keep the larger sum, which maintains the invariant.
            best = Math.max(best, s);
        }
        return best;
    }

    public static void main(String[] args) {
        int[] nums = {5, -10, 4};
        // The two position rules give 5 for subarrays and 9 for subsequences on the same data.
        if (bestSubarray(nums) != 5) throw new AssertionError("subarray answer");
        if (bestSubsequence(nums) != 9) throw new AssertionError("subsequence answer");
        // A second array shows the gap again: 7 for subarrays, 9 for subsequences.
        int[] week = {2, -5, 3, 4};
        if (bestSubarray(week) != 7 || bestSubsequence(week) != 9) throw new AssertionError("the analyst's week");
    }
}
```
