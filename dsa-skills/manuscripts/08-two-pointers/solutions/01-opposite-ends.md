<!-- solutions-for: 08-two-pointers -->
### Solutions For Scanning From Both Ends

#### Solution: [Build] Two Sum II, Input Array Is Sorted (LeetCode 167)
<!-- id: tp-two-sum-sorted -->

**Approach.**
The scan starts with `left` at the first index and `right` at the last. When the sum is below the target, every pair that uses `left` has a sum no larger than the current one, so `left` moves right. When the sum is above the target, `right` moves left for the mirror reason. The invariant is that the unique answer lies inside the range from `left` to `right`. The method returns the match with both indexes shifted by one.

**Complexity.**
- **Time** is O(n), because each iteration moves one pointer and the pointers never move back.
- **Space** is O(1), because the scan keeps only two indexes and one sum.

```java run
import java.util.Arrays;
import java.util.Random;

public final class TwoSumSorted167 {
    /**
     * Returns the 1-based indexes of the unique pair that sums to target.
     * Time: O(n), each step discards one index.
     * Space: O(1).
     * Invariant: the answer pair lies inside [left, right].
     */
    static int[] twoSum(int[] numbers, int target) {
        // The range starts as the whole array.
        int left = 0, right = numbers.length - 1;
        // Two different indexes are needed, so the loop ends when they meet.
        while (left < right) {
            // The sum of the two ends decides which index to discard.
            int sum = numbers[left] + numbers[right];
            // A match is the unique answer, reported with 1-based indexes.
            if (sum == target) return new int[] {left + 1, right + 1};
            // Too small: every pair that uses left is at most this sum.
            if (sum < target) left++;
            // Too large: every pair that uses right is at least this sum.
            else right--;
        }
        // The statement guarantees a pair, so this line is not reached for valid input.
        return new int[] {-1, -1};
    }

    public static void main(String[] args) {
        // The statement examples.
        if (!Arrays.equals(twoSum(new int[] {2, 5, 9, 12, 20}, 21), new int[] {3, 4})) throw new AssertionError("example 1");
        if (!Arrays.equals(twoSum(new int[] {-4, -1, 0, 3}, -4), new int[] {1, 3})) throw new AssertionError("example 2");
        // Random sorted arrays with one planted pair, checked against all pairs.
        Random rnd = new Random(11);
        for (int t = 0; t < 3000; t++) {
            int n = 2 + rnd.nextInt(8);
            int[] a = rnd.ints(n, -20, 21).sorted().toArray();
            int i = rnd.nextInt(n - 1), j = i + 1 + rnd.nextInt(n - 1 - i);
            int target = a[i] + a[j];
            int count = 0;
            int[] expect = null;
            for (int x = 0; x < n; x++) for (int y = x + 1; y < n; y++) if (a[x] + a[y] == target) { count++; expect = new int[] {x + 1, y + 1}; }
            // The scan is only specified when the pair is unique.
            if (count != 1) continue;
            if (!Arrays.equals(twoSum(a, target), expect)) throw new AssertionError("random " + Arrays.toString(a));
        }
    }
}
```

#### Solution: [Vary] Closest Pair Sum (Author exercise)
<!-- id: tp-closest-pair-sum -->

**Approach.**
The same scan runs, but a match no longer ends it. At each step the method compares the current sum with the best sum by absolute difference and keeps the closer one. A tie keeps the smaller sum. The pointer moves by the same rule as before: a sum below the target discards `left`, and a sum above or equal to the target discards `right`. A sum equal to the target has difference 0 and ends the scan at once. The invariant is that the best pair overall is either recorded in `best` or still lies inside the range.

**Complexity.**
- **Time** is O(n), because the scan makes at most `n - 1` moves.
- **Space** is O(1), because it stores two indexes and the best sum.

```java run
import java.util.Random;

public final class ClosestPairSum {
    /**
     * Returns the pair sum closest to target, preferring the smaller sum on a tie.
     * Time: O(n).
     * Space: O(1).
     * Invariant: every pair outside [left, right] has a sum no closer than best.
     */
    static long closest(int[] nums, int target) {
        int left = 0, right = nums.length - 1;
        // Start with the first legal pair.
        long best = (long) nums[left] + nums[right];
        // Each iteration tests one sum and discards one index.
        while (left < right) {
            long sum = (long) nums[left] + nums[right];
            long dSum = Math.abs(sum - target), dBest = Math.abs(best - target);
            // A strictly closer sum, or an equally close smaller sum, replaces the best.
            if (dSum < dBest || (dSum == dBest && sum < best)) best = sum;
            // An exact match cannot be beaten.
            if (sum == target) return sum;
            // Below the target: left cannot give a closer sum than this one with any index before right.
            if (sum < target) left++;
            else right--;
        }
        return best;
    }

    public static void main(String[] args) {
        // The statement examples, including the tie.
        if (closest(new int[] {1, 4, 9, 16}, 12) != 13) throw new AssertionError("example 1");
        if (closest(new int[] {1, 5, 7}, 7) != 6) throw new AssertionError("example 2");
        // Extreme values keep the sum exact in a long.
        if (closest(new int[] {1_000_000_000, 1_000_000_000}, 0) != 2_000_000_000L) throw new AssertionError("overflow");
        // Random sorted arrays against all pairs.
        Random rnd = new Random(12);
        for (int t = 0; t < 4000; t++) {
            int n = 2 + rnd.nextInt(8);
            int[] a = rnd.ints(n, -15, 16).sorted().toArray();
            int target = rnd.nextInt(41) - 20;
            long best = Long.MAX_VALUE;
            for (int x = 0; x < n; x++) for (int y = x + 1; y < n; y++) {
                long s = a[x] + a[y];
                if (best == Long.MAX_VALUE || Math.abs(s - target) < Math.abs(best - target) || (Math.abs(s - target) == Math.abs(best - target) && s < best)) best = s;
            }
            if (closest(a, target) != best) throw new AssertionError("random");
        }
    }
}
```

#### Solution: [Boundary] Two Values (Author exercise)
<!-- id: tp-two-values -->

**Approach.**
The loop condition `left < right` keeps the two indexes different, so a single value never pairs with itself. Two equal values at different indexes are allowed, so `[3, 3]` with target 6 returns `true`. An empty array and a one-element array never enter the loop and return `false`. The invariant is that any valid pair lies inside the range from `left` to `right`.

**Complexity.**
- **Time** is O(n), because the pointers move toward each other one step per iteration.
- **Space** is O(1), because the method keeps two indexes.

```java run
import java.util.Random;

public final class TwoValues {
    /**
     * Returns true when two different indexes hold values that sum to target.
     * Time: O(n).
     * Space: O(1).
     * Invariant: every valid pair lies inside [left, right].
     */
    static boolean hasPair(int[] nums, long target) {
        int left = 0, right = nums.length - 1;
        // The strict comparison forbids pairing an index with itself.
        while (left < right) {
            long sum = (long) nums[left] + nums[right];
            // A match proves a pair of different indexes exists.
            if (sum == target) return true;
            // Discard the index that cannot reach the target.
            if (sum < target) left++;
            else right--;
        }
        // The range holds fewer than two indexes.
        return false;
    }

    public static void main(String[] args) {
        // The statement examples.
        if (!hasPair(new int[] {3, 3}, 6)) throw new AssertionError("equal values");
        if (hasPair(new int[] {3, 5, 8}, 6)) throw new AssertionError("absent");
        // A single value cannot pair with itself, and the empty array has no pair.
        if (hasPair(new int[] {3}, 6)) throw new AssertionError("single");
        if (hasPair(new int[0], 0)) throw new AssertionError("empty");
        // Random sorted arrays against all pairs.
        Random rnd = new Random(13);
        for (int t = 0; t < 4000; t++) {
            int[] a = rnd.ints(rnd.nextInt(8), -6, 7).sorted().toArray();
            long target = rnd.nextInt(17) - 8;
            boolean expect = false;
            for (int x = 0; x < a.length; x++) for (int y = x + 1; y < a.length; y++) if (a[x] + a[y] == target) expect = true;
            if (hasPair(a, target) != expect) throw new AssertionError("random");
        }
    }
}
```

#### Solution: [Recognize] Container With Most Water (LeetCode 11)
<!-- id: tp-container-water -->

**Approach.**
The area of a pair is bounded by its shorter wall, and the width shrinks by one at each move. Fix the pair at the two ends. Moving the pointer at the taller wall keeps the same shorter wall and reduces the width, so the new area cannot be larger. That shows the shorter wall's index belongs to no better pair, and the scan discards it. The invariant is that the best pair of the whole array is either already recorded or lies inside the range.

**Complexity.**
- **Time** is O(n), because each step discards one index.
- **Space** is O(1), because the method keeps two indexes and the best area.

```java run
import java.util.Random;

public final class ContainerWater11 {
    /**
     * Returns the largest min(height[i], height[j]) * (j - i) over i < j.
     * Time: O(n).
     * Space: O(1).
     * Invariant: every pair that uses a discarded index has an area no larger than best.
     */
    static long maxArea(int[] height) {
        int left = 0, right = height.length - 1;
        long best = 0;
        // Each iteration evaluates one pair and discards one index.
        while (left < right) {
            long area = (long) Math.min(height[left], height[right]) * (right - left);
            // Keep the maximum area seen.
            best = Math.max(best, area);
            // The shorter wall limits every pair that keeps it, and those pairs are narrower.
            if (height[left] <= height[right]) left++;
            else right--;
        }
        return best;
    }

    public static void main(String[] args) {
        // The statement examples.
        if (maxArea(new int[] {3, 9, 2, 8, 1}) != 16) throw new AssertionError("example 1");
        if (maxArea(new int[] {5, 5}) != 5) throw new AssertionError("example 2");
        // Random unsorted arrays against all pairs.
        Random rnd = new Random(14);
        for (int t = 0; t < 4000; t++) {
            int[] h = rnd.ints(2 + rnd.nextInt(8), 0, 12).toArray();
            long expect = 0;
            for (int i = 0; i < h.length; i++) for (int j = i + 1; j < h.length; j++) expect = Math.max(expect, (long) Math.min(h[i], h[j]) * (j - i));
            if (maxArea(h) != expect) throw new AssertionError("random");
        }
    }
}
```
