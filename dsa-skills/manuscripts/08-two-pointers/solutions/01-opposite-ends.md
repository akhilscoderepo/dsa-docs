<!-- solutions-for: 08-opposite-ends -->
### Opposite Ends

#### Solution: [Build] Two Sum II Input Array Is Sorted (LeetCode 167)
<!-- id: tp-two-sum-sorted -->

**Approach.** Put `left` at the first entry and `right` at the last. A sum below the target proves that `left` is short with every remaining partner, so it moves up. A sum above the target proves that `right` is too dear with every remaining partner, so it moves down. Because exactly one pair exists, the loop returns it, and each step shrinks the range by one, so the number of steps is at most n - 1. The check compares with a double loop on random sorted arrays that are built to hold exactly one pair, confirms the step bound, and asserts the input is never modified.

**Complexity.** Linear time in the array length and no extra memory beyond two indices.

```java run
import java.util.Arrays;
import java.util.Random;

public final class TwoSumSorted {
    static int steps;

    static int[] twoSum(int[] numbers, int target) {
        int left = 0, right = numbers.length - 1;
        while (left < right) {
            steps++;
            long sum = (long) numbers[left] + numbers[right];
            if (sum == target) return new int[] {left + 1, right + 1};
            if (sum < target) left++; else right--;
        }
        return new int[] {-1, -1};
    }
    static int pairCount(int[] a, int target) {
        int c = 0;
        for (int i = 0; i < a.length; i++) for (int j = i + 1; j < a.length; j++) if ((long) a[i] + a[j] == target) c++;
        return c;
    }
    static int[] bruteForce(int[] a, int target) {
        for (int i = 0; i < a.length; i++) for (int j = i + 1; j < a.length; j++) if ((long) a[i] + a[j] == target) return new int[] {i + 1, j + 1};
        return new int[] {-1, -1};
    }

    public static void main(String[] args) {
        if (!Arrays.equals(twoSum(new int[] {2, 7, 11, 15}, 18), new int[] {2, 3})) throw new AssertionError("example 1");
        if (!Arrays.equals(twoSum(new int[] {-3, 0, 4, 4, 9}, 8), new int[] {3, 4})) throw new AssertionError("example 2");
        Random rnd = new Random(801);
        int checked = 0;
        for (int t = 0; t < 6000; t++) {
            int n = 2 + rnd.nextInt(10);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(21) - 10;
            if (t % 7 == 0) Arrays.fill(a, 3);
            Arrays.sort(a);
            int[] copy = a.clone();
            int target = rnd.nextInt(41) - 20;
            if (pairCount(a, target) != 1) {
                continue;   // outside the promise of exactly one pair
            }
            steps = 0;
            int[] got = twoSum(a, target);
            if (!Arrays.equals(got, bruteForce(a, target))) throw new AssertionError("differs on " + Arrays.toString(a) + " target " + target);
            if (steps > n - 1) throw new AssertionError("more than n - 1 steps");
            if (!Arrays.equals(a, copy)) throw new AssertionError("input was modified");
            checked++;
        }
        if (checked < 300) throw new AssertionError("too few unique-pair cases: " + checked);
    }
}
```

#### Solution: [Vary] Closest Pair Sum (Author exercise)
<!-- id: tp-closest-pair-sum -->

**Approach.** The same discard rule applies, but a pair that misses the target is not an answer to return, so the scan records the distance of every pair it inspects before moving an end. A sum that is short moves `left` and a sum that is long moves `right`. The smallest distance over the inspected pairs equals the smallest over all pairs, because every discarded end could only have produced pairs no closer than the one just inspected. The check compares with a double loop on random sorted arrays, including values near the `int` limits where an `int` sum would wrap.

**Complexity.** A single pass of at most n - 1 pair inspections, with constant extra memory.

```java run
import java.util.Arrays;
import java.util.Random;

public final class ClosestPairSum {
    static long closestGap(int[] numbers, long target) {
        int left = 0, right = numbers.length - 1;
        long best = Long.MAX_VALUE;
        while (left < right) {
            long sum = (long) numbers[left] + numbers[right];
            best = Math.min(best, Math.abs(sum - target));
            if (sum < target) left++;
            else if (sum > target) right--;
            else return 0;
        }
        return best;
    }
    static long brute(int[] a, long target) {
        long best = Long.MAX_VALUE;
        for (int i = 0; i < a.length; i++) for (int j = i + 1; j < a.length; j++) best = Math.min(best, Math.abs((long) a[i] + a[j] - target));
        return best;
    }

    public static void main(String[] args) {
        if (closestGap(new int[] {1, 4, 9, 16}, 12) != 1) throw new AssertionError("example 1");
        if (closestGap(new int[] {-5, -1, 5}, 0) != 0) throw new AssertionError("example 2");
        if (closestGap(new int[] {Integer.MAX_VALUE, Integer.MAX_VALUE}, Integer.MIN_VALUE) != 2L * Integer.MAX_VALUE - Integer.MIN_VALUE)
            throw new AssertionError("long arithmetic needed");
        Random rnd = new Random(802);
        for (int t = 0; t < 5000; t++) {
            int n = 2 + rnd.nextInt(9);
            int[] a = new int[n];
            int mode = t % 4;
            for (int i = 0; i < n; i++) {
                if (mode == 0) a[i] = rnd.nextInt(15) - 7;
                else if (mode == 1) a[i] = rnd.nextBoolean() ? Integer.MAX_VALUE - rnd.nextInt(4) : Integer.MIN_VALUE + rnd.nextInt(4);
                else if (mode == 2) a[i] = 5;
                else a[i] = rnd.nextInt();
            }
            Arrays.sort(a);
            long target = mode == 1 || mode == 3 ? rnd.nextInt() : rnd.nextInt(41) - 20;
            if (closestGap(a, target) != brute(a, target)) throw new AssertionError("differs on " + Arrays.toString(a) + " target " + target);
        }
    }
}
```

#### Solution: [Boundary] Two Values (Author exercise)
<!-- id: tp-two-values -->

**Approach.** Run the scan with the condition `left < right`. For an empty or one-element array that condition is false at once, so the answer is false without a special branch, and two equal neighbours are found because they sit at different positions. The sum is computed in `long`, so two copies of the largest `int` cannot wrap around and appear to match a negative target. The check compares with a double loop on random arrays that include the empty array, single values, all-equal arrays and the extreme values, and it shows that `int` addition would have given a wrong answer on one of the extreme cases.

**Complexity.** Linear time in the array length, constant extra memory.

```java run
import java.util.Arrays;
import java.util.Random;

public final class TwoValues {
    static boolean hasPair(int[] numbers, long target) {
        int left = 0, right = numbers.length - 1;
        while (left < right) {
            long sum = (long) numbers[left] + numbers[right];
            if (sum == target) return true;
            if (sum < target) left++; else right--;
        }
        return false;
    }
    static boolean wrappingPair(int[] numbers, long target) {
        int left = 0, right = numbers.length - 1;
        while (left < right) {
            int sum = numbers[left] + numbers[right];
            if (sum == target) return true;
            if (sum < target) left++; else right--;
        }
        return false;
    }
    static boolean brute(int[] a, long target) {
        for (int i = 0; i < a.length; i++) for (int j = i + 1; j < a.length; j++) if ((long) a[i] + a[j] == target) return true;
        return false;
    }

    public static void main(String[] args) {
        if (!hasPair(new int[] {5, 5}, 10)) throw new AssertionError("example 1");
        if (hasPair(new int[] {7}, 14)) throw new AssertionError("example 2");
        if (hasPair(new int[0], 0)) throw new AssertionError("empty array");
        int[] big = {Integer.MAX_VALUE, Integer.MAX_VALUE};
        if (hasPair(big, -2)) throw new AssertionError("long arithmetic must not wrap");
        if (!wrappingPair(big, -2)) throw new AssertionError("int arithmetic wraps to -2, the hazard this exercise warns about");
        Random rnd = new Random(803);
        int[] pool = {Integer.MIN_VALUE, Integer.MIN_VALUE + 1, -3, 0, 4, 4, Integer.MAX_VALUE - 1, Integer.MAX_VALUE};
        for (int t = 0; t < 6000; t++) {
            int n = rnd.nextInt(7);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = t % 3 == 0 ? pool[rnd.nextInt(pool.length)] : rnd.nextInt(9) - 4;
            if (t % 11 == 0 && n > 0) Arrays.fill(a, a[0]);
            Arrays.sort(a);
            long target;
            if (t % 3 == 0) {
                long[] picks = {-2, -1, 0, 1, 4, 8, Integer.MAX_VALUE, 2L * Integer.MAX_VALUE, 2L * Integer.MIN_VALUE, rnd.nextInt()};
                target = picks[rnd.nextInt(picks.length)];
            } else target = rnd.nextInt(21) - 10;
            if (hasPair(a, target) != brute(a, target)) throw new AssertionError("differs on " + Arrays.toString(a) + " target " + target);
        }
    }
}
```

#### Solution: [Recognize] Container With Most Water (LeetCode 11)
<!-- id: tp-container-water -->

**Approach.** The area of a pair is the width times the shorter wall. Start with the widest pair. For any pair with the shorter wall at `left`, every other pair that keeps `left` has a smaller width and a height capped by that same wall, so none of them can beat the pair just measured, and `left` can be discarded. The symmetric argument discards `right` when it is the shorter wall. Ties may discard either end. The scan therefore measures at most n - 1 pairs, and the answer is held in a `long` because width times height can exceed the `int` range. The check compares with a double loop on random heights, counts the measured pairs, and includes huge heights to prove the `long` is needed.

**Complexity.** Pointers move inward exactly once per measurement, giving a linear number of steps and constant extra memory.

```java run
import java.util.Random;

public final class ContainerWater {
    static int measured;

    static long maxWater(int[] height) {
        int left = 0, right = height.length - 1;
        long best = 0;
        while (left < right) {
            measured++;
            long area = (long) (right - left) * Math.min(height[left], height[right]);
            best = Math.max(best, area);
            if (height[left] <= height[right]) left++; else right--;
        }
        return best;
    }
    static long brute(int[] h) {
        long best = 0;
        for (int i = 0; i < h.length; i++) for (int j = i + 1; j < h.length; j++) best = Math.max(best, (long) (j - i) * Math.min(h[i], h[j]));
        return best;
    }

    public static void main(String[] args) {
        if (maxWater(new int[] {3, 9, 2, 6, 4}) != 12) throw new AssertionError("example 1");
        if (maxWater(new int[] {5, 5, 5}) != 10) throw new AssertionError("example 2");
        int[] huge = new int[50001];
        java.util.Arrays.fill(huge, 1_000_000_000);
        long want = 50000L * 1_000_000_000L;
        if (want <= Integer.MAX_VALUE) throw new AssertionError("test must exceed int");
        measured = 0;
        if (maxWater(huge) != want) throw new AssertionError("huge heights");
        if (measured != huge.length - 1) throw new AssertionError("pair count");
        Random rnd = new Random(804);
        for (int t = 0; t < 6000; t++) {
            int n = 2 + rnd.nextInt(10);
            int[] h = new int[n];
            for (int i = 0; i < n; i++) h[i] = t % 5 == 0 ? 4 : rnd.nextInt(t % 2 == 0 ? 8 : 1000);
            measured = 0;
            long got = maxWater(h);
            if (got != brute(h)) throw new AssertionError("differs on " + java.util.Arrays.toString(h));
            if (measured != n - 1) throw new AssertionError("each step discards one wall, so exactly n - 1 pairs are measured");
        }
    }
}
```
