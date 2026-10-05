<!-- solutions-for: 08-two-pointers -->
### Solutions For Scanning After Fixed Values

#### Solution: [Build] 3Sum (LeetCode 15)
<!-- id: tp-three-sum-count -->

**Approach.**
The method sorts a copy of the input. The outer loop fixes the first value at index `i`, and the remaining target is `target - nums[i]`. The pair scan runs on the indexes after `i`. When the two ends sum to the remaining target and hold different values, the scan measures the run of the left value and the run of the right value, and it adds the product of the lengths. When both ends hold the same value, every value between them is equal, and the block of `m` values holds `m * (m - 1) / 2` index pairs. The invariant is that `count` equals the number of triples whose first index is before `i`.

**Complexity.**
- **Time** is O(n^2), because the sort costs O(n log n) and each of at most `n` fixed values triggers one O(n) pair scan.
- **Space** is O(n) for the sorted copy.

```java run
import java.util.Arrays;
import java.util.Random;

public final class ThreeSumCount15 {
    /**
     * Counts index triples i < j < k whose values sum to target.
     * Time: O(n^2).
     * Space: O(n) for the sorted copy.
     * Invariant: count equals the number of matching triples with first index before i.
     */
    static long countTriples(int[] input, long target) {
        int[] a = input.clone();
        Arrays.sort(a);
        long count = 0;
        // Each fixed index starts one pair scan over the later indexes.
        for (int i = 0; i + 2 < a.length; i++) {
            long rem = target - a[i];
            int left = i + 1, right = a.length - 1;
            while (left < right) {
                long sum = (long) a[left] + a[right];
                if (sum < rem) left++;
                else if (sum > rem) right--;
                else if (a[left] == a[right]) {
                    // Every value from left to right is equal, so all pairs inside the block match.
                    long m = right - left + 1;
                    count += m * (m - 1) / 2;
                    break;
                } else {
                    // Different end values: each copy on the left pairs with each copy on the right.
                    int x = a[left], y = a[right];
                    long runX = 0, runY = 0;
                    while (left <= right && a[left] == x) { left++; runX++; }
                    while (right >= left && a[right] == y) { right--; runY++; }
                    count += runX * runY;
                }
            }
        }
        return count;
    }

    public static void main(String[] args) {
        // The statement examples.
        if (countTriples(new int[] {-1, 0, 1, 2, -1, -4}, 0) != 3) throw new AssertionError("example 1");
        if (countTriples(new int[] {0, 0, 0, 0}, 0) != 4) throw new AssertionError("example 2");
        // The empty array and two values give zero.
        if (countTriples(new int[0], 0) != 0 || countTriples(new int[] {1, 2}, 3) != 0) throw new AssertionError("short");
        // Random arrays against three nested loops.
        Random rnd = new Random(61);
        for (int t = 0; t < 3000; t++) {
            int[] a = rnd.ints(rnd.nextInt(12), -4, 5).toArray();
            long target = rnd.nextInt(9) - 4;
            long expect = 0;
            for (int i = 0; i < a.length; i++) for (int j = i + 1; j < a.length; j++) for (int k = j + 1; k < a.length; k++) if (a[i] + a[j] + a[k] == target) expect++;
            if (countTriples(a, target) != expect) throw new AssertionError("random " + Arrays.toString(a));
        }
    }
}
```

#### Solution: [Vary] 3Sum Closest (LeetCode 16)
<!-- id: tp-three-sum-closest -->

**Approach.**
The method sorts a copy, fixes one value, and runs the pair scan on the later indexes. At each step it compares the three-value total with the target. A total that is closer than the best one, or equally close and smaller, becomes the best. A total below the target moves `left` right, a total above it moves `right` left, and a total equal to the target returns at once because no total is closer. The invariant is that `best` is the closest total among all combinations the scan has passed.

**Complexity.**
- **Time** is O(n^2), because the sort costs O(n log n) and each fixed value costs one O(n) scan.
- **Space** is O(n) for the sorted copy.

```java run
import java.util.Arrays;
import java.util.Random;

public final class ThreeSumClosest16 {
    /**
     * Returns the three-value sum closest to target, smaller on a tie.
     * Time: O(n^2).
     * Space: O(n).
     * Invariant: best is the closest total among the combinations already passed by the scan.
     */
    static long closest(int[] input, int target) {
        int[] a = input.clone();
        Arrays.sort(a);
        // The first three values form a legal starting candidate.
        long best = (long) a[0] + a[1] + a[2];
        for (int i = 0; i + 2 < a.length; i++) {
            int left = i + 1, right = a.length - 1;
            while (left < right) {
                long sum = (long) a[i] + a[left] + a[right];
                long dSum = Math.abs(sum - target), dBest = Math.abs(best - target);
                // Closer wins; on equal distance the smaller total wins.
                if (dSum < dBest || (dSum == dBest && sum < best)) best = sum;
                // An exact match cannot be beaten.
                if (sum == target) return sum;
                // The comparison with the target decides which pointer moves.
                if (sum < target) left++;
                else right--;
            }
        }
        return best;
    }

    public static void main(String[] args) {
        // The statement examples, including the tie.
        if (closest(new int[] {-4, -1, 1, 2}, 1) != 2) throw new AssertionError("example 1");
        if (closest(new int[] {1, 3, 5, 7}, 10) != 9) throw new AssertionError("example 2");
        // Random arrays against three nested loops.
        Random rnd = new Random(62);
        for (int t = 0; t < 3000; t++) {
            int[] a = rnd.ints(3 + rnd.nextInt(8), -6, 7).toArray();
            int target = rnd.nextInt(31) - 15;
            long best = Long.MAX_VALUE;
            for (int i = 0; i < a.length; i++) for (int j = i + 1; j < a.length; j++) for (int k = j + 1; k < a.length; k++) {
                long s = a[i] + a[j] + a[k];
                if (best == Long.MAX_VALUE || Math.abs(s - target) < Math.abs(best - target) || (Math.abs(s - target) == Math.abs(best - target) && s < best)) best = s;
            }
            if (closest(a, target) != best) throw new AssertionError("random " + Arrays.toString(a));
        }
    }
}
```

#### Solution: [Boundary] Overflowing Sum (Author exercise)
<!-- id: tp-overflowing-sum -->

**Approach.**
Three values near `2^31` add to a number that does not fit in `int`, and Java wraps without an error. The sum `2147483647 + 2147483647 + 2` is 4294967296 as a `long`, and it wraps to 0 as an `int`. A target of 0 would then match by mistake. The method widens the first operand to `long`, so every later addition in the expression runs as `long` arithmetic. The scan fixes one value and runs the pair scan on the rest, with the remaining target as a `long`. The invariant is that every triple that sums to the target lies at the fixed index or after it.

**Complexity.**
- **Time** is O(n^2), because each fixed value triggers one O(n) pair scan on the sorted input.
- **Space** is O(1), because the method works on the given sorted array and keeps indexes and sums.

```java run
import java.util.Random;

public final class OverflowingSum {
    /**
     * Returns true when three values at different indexes of a sorted array sum to target.
     * Time: O(n^2).
     * Space: O(1).
     * Invariant: every matching triple has its first index at or after i.
     */
    static boolean hasTriple(int[] a, long target) {
        for (int i = 0; i + 2 < a.length; i++) {
            // The remaining target is a long, so no step wraps.
            long rem = target - a[i];
            int left = i + 1, right = a.length - 1;
            while (left < right) {
                long sum = (long) a[left] + a[right];
                if (sum == rem) return true;
                if (sum < rem) left++;
                else right--;
            }
        }
        return false;
    }

    public static void main(String[] args) {
        int max = Integer.MAX_VALUE;
        // The int sum wraps to 0, which is why a long is needed.
        int wrapped = max + max + 2;
        if (wrapped != 0) throw new AssertionError("wrap");
        // The statement examples.
        if (hasTriple(new int[] {2, max, max}, 0)) throw new AssertionError("example 1");
        if (!hasTriple(new int[] {max, max, max}, 6_442_450_941L)) throw new AssertionError("example 2");
        // The empty array and two values.
        if (hasTriple(new int[0], 0) || hasTriple(new int[] {1, 2}, 3)) throw new AssertionError("short");
        // Random extreme arrays against three nested loops in long arithmetic.
        Random rnd = new Random(63);
        for (int t = 0; t < 3000; t++) {
            int[] a = new int[rnd.nextInt(8)];
            for (int i = 0; i < a.length; i++) a[i] = rnd.nextBoolean() ? max - rnd.nextInt(3) : Integer.MIN_VALUE + rnd.nextInt(3);
            java.util.Arrays.sort(a);
            long target = rnd.nextBoolean() ? 3L * max - rnd.nextInt(4) : -3L * 2147483648L + rnd.nextInt(4);
            boolean expect = false;
            for (int i = 0; i < a.length; i++) for (int j = i + 1; j < a.length; j++) for (int k = j + 1; k < a.length; k++) if ((long) a[i] + a[j] + a[k] == target) expect = true;
            if (hasTriple(a, target) != expect) throw new AssertionError("random");
        }
    }
}
```

#### Solution: [Recognize] 4Sum (LeetCode 18)
<!-- id: tp-four-sum-count -->

**Approach.**
Two nested loops fix the first two values of each quadruple on a sorted copy. The remaining target is the original target minus both fixed values, and every operation is a `long` operation. The pair scan then counts the matching index pairs in the indexes after the second fixed value. Matching ends with different values add the product of the run lengths, and a block of equal values adds `m * (m - 1) / 2`. The invariant is that the count equals the number of quadruples whose first two indexes come before the current fixed pair.

**Complexity.**
- **Time** is O(n^3), because two fixed loops each cost O(n) and the pair scan costs O(n).
- **Space** is O(n) for the sorted copy.

```java run
import java.util.Arrays;
import java.util.Random;

public final class FourSumCount18 {
    /**
     * Counts index quadruples i < j < k < l whose values sum to target.
     * Time: O(n^3).
     * Space: O(n).
     * Invariant: count equals the number of matching quadruples whose first two indexes precede (i, j).
     */
    static long countQuadruples(int[] input, long target) {
        int[] a = input.clone();
        Arrays.sort(a);
        int n = a.length;
        long count = 0;
        for (int i = 0; i + 3 < n; i++) {
            for (int j = i + 1; j + 2 < n; j++) {
                long rem = target - a[i] - a[j];
                int left = j + 1, right = n - 1;
                while (left < right) {
                    long sum = (long) a[left] + a[right];
                    if (sum < rem) left++;
                    else if (sum > rem) right--;
                    else if (a[left] == a[right]) {
                        // One block of equal values holds all remaining pairs.
                        long m = right - left + 1;
                        count += m * (m - 1) / 2;
                        break;
                    } else {
                        // Count the runs at both ends and multiply their lengths.
                        int x = a[left], y = a[right];
                        long runX = 0, runY = 0;
                        while (left <= right && a[left] == x) { left++; runX++; }
                        while (right >= left && a[right] == y) { right--; runY++; }
                        count += runX * runY;
                    }
                }
            }
        }
        return count;
    }

    public static void main(String[] args) {
        // The statement examples.
        if (countQuadruples(new int[] {1, 0, -1, 0, -2, 2}, 0) != 3) throw new AssertionError("example 1");
        if (countQuadruples(new int[] {2, 2, 2, 2, 2}, 8) != 5) throw new AssertionError("example 2");
        // Large values stay exact in long arithmetic.
        if (countQuadruples(new int[] {1_000_000_000, 1_000_000_000, 1_000_000_000, 1_000_000_000}, 4_000_000_000L) != 1) throw new AssertionError("large");
        // Random arrays against four nested loops.
        Random rnd = new Random(64);
        for (int t = 0; t < 2000; t++) {
            int[] a = rnd.ints(rnd.nextInt(10), -3, 4).toArray();
            long target = rnd.nextInt(7) - 3;
            long expect = 0;
            for (int i = 0; i < a.length; i++) for (int j = i + 1; j < a.length; j++) for (int k = j + 1; k < a.length; k++) for (int l = k + 1; l < a.length; l++) if (a[i] + a[j] + a[k] + a[l] == target) expect++;
            if (countQuadruples(a, target) != expect) throw new AssertionError("random " + Arrays.toString(a));
        }
    }
}
```
