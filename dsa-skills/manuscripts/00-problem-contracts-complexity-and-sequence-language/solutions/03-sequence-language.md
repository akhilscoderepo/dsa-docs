<!-- solutions-for: 03-sequence-language -->
### Sequence Language

#### Solution: [Build] Classify [2,4] (Author exercise)
<!-- id: pc-classify-2-4 -->

**Approach.** Find the position of each candidate value in `[1,2,3,4]`. The value 2 sits at position 1 and the value 4 at position 3. The positions increase, so the original order is kept, which makes the candidate a subsequence. They are not consecutive, because position 2 is skipped, so it is not a subarray. Any selection of positions is a subset, so it is one as well. The code classifies by the position list, so each verdict is derived and not asserted from eyesight.

**Complexity.** O(n + m) time to locate the positions of `m` candidate values in an array of `n`, and O(m) space for the position list.

```java run
public final class ClassifyPositions {
    static int[] positionsOf(int[] nums, int[] cand) {
        int[] pos = new int[cand.length];
        for (int j = 0; j < cand.length; j++) {
            pos[j] = -1;
            for (int i = 0; i < nums.length; i++) if (nums[i] == cand[j]) { pos[j] = i; break; }
        }
        return pos;
    }
    static boolean noGaps(int[] pos) { for (int j = 1; j < pos.length; j++) if (pos[j] != pos[j - 1] + 1) return false; return true; }
    static boolean ordered(int[] pos) { for (int j = 1; j < pos.length; j++) if (pos[j] <= pos[j - 1]) return false; return true; }

    public static void main(String[] args) {
        int[] nums = {1, 2, 3, 4};
        int[] p = positionsOf(nums, new int[] {2, 4});
        if (p[0] != 1 || p[1] != 3) throw new AssertionError("positions");
        if (noGaps(p)) throw new AssertionError("[2,4] is not a subarray");
        if (!ordered(p)) throw new AssertionError("[2,4] is a subsequence");
        int[] q = positionsOf(nums, new int[] {2, 3});
        if (!noGaps(q) || !ordered(q)) throw new AssertionError("[2,3] is all three");
    }
}
```

#### Solution: [Vary] Order Matters (Author exercise)
<!-- id: pc-order-matters -->

**Approach.** The candidate `[4,2]` has positions 3 and then 1, so the positions fall. The no-gaps test fails, because a drop is not "one more than the previous position". The ordered test fails as well. Only the membership test passes, because both values occur in the array, which is all a subset needs. The one changed decision from `[2,4]` is therefore the direction of the positions.

**Complexity.** O(n + m) time and O(m) space, as in the previous exercise.

```java run
public final class OrderMatters {
    static int indexOf(int[] a, int v) { for (int i = 0; i < a.length; i++) if (a[i] == v) return i; return -1; }

    public static void main(String[] args) {
        int[] nums = {1, 2, 3, 4};
        int first = indexOf(nums, 4), second = indexOf(nums, 2);
        if (first != 3 || second != 1) throw new AssertionError("positions of 4 then 2");
        if (second >= first) throw new AssertionError("positions should fall, so the order is reversed");
        boolean member = indexOf(nums, 4) >= 0 && indexOf(nums, 2) >= 0;
        if (!member) throw new AssertionError("both values are members, so [4,2] is a subset");
        int whole = indexOf(nums, 1);
        if (whole != 0 || indexOf(nums, 4) != nums.length - 1) throw new AssertionError("the whole array spans every position");
    }
}
```

#### Solution: [Boundary] Empty Choice (Author exercise)
<!-- id: pc-empty-choice -->

**Approach.** The contract must say whether an empty block is legal, because its sum is 0 and 0 beats every sum on an all-negative array. With the non-empty requirement the best choice is the single largest reading, -3. With the empty choice allowed the best is to choose nothing, which gives 0. Both answers come from the same brute force, and the only difference is whether the starting best is the sum of nothing or the first block's sum.

**Complexity.** The brute force is O(n^2) time with a running sum per start, and O(1) space.

```java run
public final class EmptyChoice {
    static int bestBlock(int[] nums, boolean allowEmpty) {
        int best = allowEmpty ? 0 : Integer.MIN_VALUE;
        for (int start = 0; start < nums.length; start++) {
            int sum = 0;
            for (int end = start; end < nums.length; end++) {
                sum += nums[end];
                best = Math.max(best, sum);
            }
        }
        return best;
    }

    public static void main(String[] args) {
        int[] nums = {-8, -3, -6};
        if (bestBlock(nums, false) != -3) throw new AssertionError("non-empty answer");
        if (bestBlock(nums, true) != 0) throw new AssertionError("empty allowed answer");
        if (bestBlock(new int[] {2, -1, 3}, false) != bestBlock(new int[] {2, -1, 3}, true)) throw new AssertionError("a positive array does not expose the difference");
    }
}
```

#### Solution: [Recognize] Contiguous Maximum (Author exercise)
<!-- id: pc-contiguous-maximum -->

**Approach.** Every block of consecutive positions that contains both the 5 and the 4 also contains the -10 between them, so its sum is -1. The best block is the single value 5, giving 5. A subsequence may skip the -10, so it can take positions 0 and 2 for a sum of 9. The data and the objective are identical, and the position rule alone moves the answer from 5 to 9.

**Complexity.** Enumerating all blocks is O(n^2) and all subsequences is O(2^n) time, and both use O(1) extra space beyond the loops.

```java run
public final class ContiguousMaximum {
    static int bestSubarray(int[] a) {
        int best = Integer.MIN_VALUE;
        for (int l = 0; l < a.length; l++) { int s = 0; for (int r = l; r < a.length; r++) { s += a[r]; best = Math.max(best, s); } }
        return best;
    }
    static int bestSubsequence(int[] a) {
        int best = Integer.MIN_VALUE;
        for (int mask = 1; mask < (1 << a.length); mask++) {
            int s = 0;
            for (int i = 0; i < a.length; i++) if ((mask >> i & 1) == 1) s += a[i];
            best = Math.max(best, s);
        }
        return best;
    }

    public static void main(String[] args) {
        int[] nums = {5, -10, 4};
        if (bestSubarray(nums) != 5) throw new AssertionError("subarray answer");
        if (bestSubsequence(nums) != 9) throw new AssertionError("subsequence answer");
        int[] week = {2, -5, 3, 4};
        if (bestSubarray(week) != 7 || bestSubsequence(week) != 9) throw new AssertionError("the analyst's week");
    }
}
```
