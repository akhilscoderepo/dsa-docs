<!-- solutions-for: 08-two-pointers -->
### Solutions For Sums In Sorted Arrays

#### Solution: [Build] Two Sum II With Original Positions (LeetCode 167)
<!-- id: tp-sorted-rows-pair -->

**Approach.**
Each value is packed with its position into one `long`, with the value in the high 32 bits. Sorting the packed keys orders the entries by value, and the position travels inside the key. The opposite-end scan then runs on the decoded values of the sorted copy. At a match, the low 32 bits of the two keys give the original positions, and the method returns them in increasing order. The position is never negative, so it never changes the sign of the key. The invariant is that every matching pair has both keys inside the range from `left` to `right`.

**Complexity.**
- **Time** is O(n log n), because the sort dominates and the scan adds O(n).
- **Space** is O(n) for the array of packed keys.

```java run
import java.util.Arrays;
import java.util.Random;

public final class SortedRowsPair {
    /**
     * Returns the original positions {i, j} with i < j of two values that sum to target, or {-1, -1}.
     * Time: O(n log n).
     * Space: O(n).
     * Invariant: every matching pair has both packed keys inside [left, right].
     */
    static int[] pairRows(int[] nums, long target) {
        long[] keys = new long[nums.length];
        // The value goes into the high bits and the position into the low bits.
        for (int i = 0; i < nums.length; i++) keys[i] = ((long) nums[i] << 32) | i;
        // Sorting a long[] orders by value first and position second, with no boxing.
        Arrays.sort(keys);
        int left = 0, right = keys.length - 1;
        while (left < right) {
            // The shifts decode the values, and the long cast keeps the sum exact.
            long sum = (long) (int) (keys[left] >> 32) + (int) (keys[right] >> 32);
            if (sum == target) {
                // The low 32 bits are the original positions.
                int a = (int) keys[left], b = (int) keys[right];
                return new int[] {Math.min(a, b), Math.max(a, b)};
            }
            // The usual elimination on the sorted values.
            if (sum < target) left++;
            else right--;
        }
        return new int[] {-1, -1};
    }

    public static void main(String[] args) {
        // The statement examples.
        if (!Arrays.equals(pairRows(new int[] {8, 3, 12, 5}, 13), new int[] {0, 3})) throw new AssertionError("example 1");
        if (!Arrays.equals(pairRows(new int[] {3, 3}, 6), new int[] {0, 1})) throw new AssertionError("example 2");
        // Negative values keep their order in the packed key.
        if (!Arrays.equals(pairRows(new int[] {5, -7, 2, -3}, -10), new int[] {1, 3})) throw new AssertionError("negative");
        // The empty array and one value.
        if (!Arrays.equals(pairRows(new int[0], 0), new int[] {-1, -1})) throw new AssertionError("empty");
        // Random arrays: any returned pair must be valid, and none is returned only when no pair exists.
        Random rnd = new Random(81);
        for (int t = 0; t < 4000; t++) {
            int[] a = rnd.ints(rnd.nextInt(9), -6, 7).toArray();
            long target = rnd.nextInt(15) - 7;
            boolean exists = false;
            for (int i = 0; i < a.length; i++) for (int j = i + 1; j < a.length; j++) if (a[i] + a[j] == target) exists = true;
            int[] got = pairRows(a, target);
            if (exists) {
                if (got[0] < 0 || got[0] >= got[1] || got[1] >= a.length || (long) a[got[0]] + a[got[1]] != target) throw new AssertionError("invalid pair");
            } else if (got[0] != -1 || got[1] != -1) throw new AssertionError("false match");
        }
    }
}
```

#### Solution: [Vary] 3Sum With Original Positions (LeetCode 15)
<!-- id: tp-sorted-rows-triple -->

**Approach.**
The method packs and sorts the keys once. The outer loop fixes the key at index `i`, and the remaining target is `target - value(i)`. The pair scan runs on the keys after `i` and returns at the first match. The three original positions come from the low 32 bits of the three keys, and the method sorts them before it returns. If every fixed key fails, the method returns an empty array. The invariant is that every triple whose smallest sorted index is below `i` has already been tested.

**Complexity.**
- **Time** is O(n^2), because the sort costs O(n log n) and each of at most `n` fixed keys triggers one O(n) pair scan.
- **Space** is O(n) for the packed keys.

```java run
import java.util.Arrays;
import java.util.Random;

public final class SortedRowsTriple {
    /**
     * Returns the original positions {i, j, k} of one triple that sums to target, or an empty array.
     * Time: O(n^2).
     * Space: O(n).
     * Invariant: every triple whose smallest sorted index is below i has been tested.
     */
    static int[] tripleRows(int[] nums, long target) {
        int n = nums.length;
        long[] keys = new long[n];
        for (int i = 0; i < n; i++) keys[i] = ((long) nums[i] << 32) | i;
        Arrays.sort(keys);
        // Each fixed key starts a pair scan over the later keys.
        for (int i = 0; i + 2 < n; i++) {
            long rem = target - (int) (keys[i] >> 32);
            int left = i + 1, right = n - 1;
            while (left < right) {
                long sum = (long) (int) (keys[left] >> 32) + (int) (keys[right] >> 32);
                if (sum == rem) {
                    // Decode the three original positions and order them.
                    int[] rows = {(int) keys[i], (int) keys[left], (int) keys[right]};
                    Arrays.sort(rows);
                    return rows;
                }
                if (sum < rem) left++;
                else right--;
            }
        }
        return new int[0];
    }

    public static void main(String[] args) {
        // The statement examples.
        if (!Arrays.equals(tripleRows(new int[] {9, 2, -5, 3, 1}, 0), new int[] {1, 2, 3})) throw new AssertionError("example 1");
        if (tripleRows(new int[] {4, 1, 5}, 20).length != 0) throw new AssertionError("example 2");
        // Fewer than three values.
        if (tripleRows(new int[] {1, 2}, 3).length != 0) throw new AssertionError("short");
        // Random arrays: a valid triple is returned exactly when one exists.
        Random rnd = new Random(82);
        for (int t = 0; t < 4000; t++) {
            int[] a = rnd.ints(rnd.nextInt(9), -5, 6).toArray();
            long target = rnd.nextInt(11) - 5;
            boolean exists = false;
            for (int i = 0; i < a.length; i++) for (int j = i + 1; j < a.length; j++) for (int k = j + 1; k < a.length; k++) if (a[i] + a[j] + a[k] == target) exists = true;
            int[] got = tripleRows(a, target);
            if (!exists) { if (got.length != 0) throw new AssertionError("false match"); continue; }
            if (got.length != 3 || got[0] >= got[1] || got[1] >= got[2] || got[2] >= a.length) throw new AssertionError("shape");
            if ((long) a[got[0]] + a[got[1]] + a[got[2]] != target) throw new AssertionError("sum");
        }
    }
}
```

#### Solution: [Boundary] 3Sum Closest With Original Positions (LeetCode 16)
<!-- id: tp-sorted-rows-closest -->

**Approach.**
The method sorts packed keys and runs the pair scan under each fixed key, as in the previous solution. At each step it compares the total with the target. A total that is closer than the best total, or equally close and smaller, becomes the best, and the method stores the three keys of that triple. The scan moves `left` right when the total is below the target and `right` left otherwise. When the best total reaches distance 0, the method returns at once. The final answer decodes the stored keys into positions in increasing order. The invariant is that the stored triple has the closest total among all triples the scan has passed.

**Complexity.**
- **Time** is O(n^2), because the sort costs O(n log n) and each fixed key costs one O(n) scan.
- **Space** is O(n) for the packed keys.

```java run
import java.util.Arrays;
import java.util.Random;

public final class SortedRowsClosest {
    /**
     * Returns original positions {i, j, k} of a triple whose sum is closest to target.
     * Time: O(n^2).
     * Space: O(n).
     * Invariant: best is the closest total, smaller on a tie, among the triples passed by the scan.
     */
    static int[] closestRows(int[] nums, long target) {
        int n = nums.length;
        long[] keys = new long[n];
        for (int i = 0; i < n; i++) keys[i] = ((long) nums[i] << 32) | i;
        Arrays.sort(keys);
        // The first three sorted keys form a legal starting candidate.
        long best = (long) (int) (keys[0] >> 32) + (int) (keys[1] >> 32) + (int) (keys[2] >> 32);
        int[] rows = {(int) keys[0], (int) keys[1], (int) keys[2]};
        for (int i = 0; i + 2 < n; i++) {
            int left = i + 1, right = n - 1;
            while (left < right) {
                long sum = (long) (int) (keys[i] >> 32) + (int) (keys[left] >> 32) + (int) (keys[right] >> 32);
                long dSum = Math.abs(sum - target), dBest = Math.abs(best - target);
                // A closer total, or an equally close smaller total, replaces the candidate.
                if (dSum < dBest || (dSum == dBest && sum < best)) {
                    best = sum;
                    rows = new int[] {(int) keys[i], (int) keys[left], (int) keys[right]};
                }
                // An exact match cannot be beaten.
                if (sum == target) { Arrays.sort(rows); return rows; }
                if (sum < target) left++;
                else right--;
            }
        }
        Arrays.sort(rows);
        return rows;
    }

    public static void main(String[] args) {
        // The statement examples.
        if (!Arrays.equals(closestRows(new int[] {10, 2, 7, 4, 15}, 20), new int[] {0, 1, 2})) throw new AssertionError("example 1");
        int[] r = closestRows(new int[] {1, 1, 1, 1}, 5);
        if (r.length != 3 || r[0] >= r[1] || r[1] >= r[2]) throw new AssertionError("example 2");
        // Random arrays: the sum of the returned positions equals the best sum of the brute force.
        Random rnd = new Random(83);
        for (int t = 0; t < 4000; t++) {
            int[] a = rnd.ints(3 + rnd.nextInt(7), -8, 9).toArray();
            long target = rnd.nextInt(41) - 20;
            long best = Long.MAX_VALUE;
            for (int i = 0; i < a.length; i++) for (int j = i + 1; j < a.length; j++) for (int k = j + 1; k < a.length; k++) {
                long s = a[i] + a[j] + a[k];
                if (best == Long.MAX_VALUE || Math.abs(s - target) < Math.abs(best - target) || (Math.abs(s - target) == Math.abs(best - target) && s < best)) best = s;
            }
            int[] got = closestRows(a, target);
            if (got.length != 3 || got[0] >= got[1] || got[1] >= got[2]) throw new AssertionError("shape");
            if ((long) a[got[0]] + a[got[1]] + a[got[2]] != best) throw new AssertionError("sum " + Arrays.toString(a));
        }
    }
}
```

#### Solution: [Recognize] 4Sum Not Above A Target (LeetCode 18)
<!-- id: tp-sorted-rows-four -->

**Approach.**
A sorted copy and two nested loops fix the first two values of each four-value combination. For each fixed pair it needs the largest pair sum among the later indexes that does not exceed the remaining target. The pair scan moves `left` right when the pair sum fits under the remaining target, because a larger left value can give a larger sum that may still fit. It moves `right` left when the pair sum exceeds the remaining target. A pair sum that fits updates the best total. Every sum is a `long`, because four values near `10^9` exceed the `int` range. The invariant is that `best` is the largest fitting sum among the combinations that the scan has passed.

**Complexity.**
- **Time** is O(n^3), because two fixed loops cost O(n^2) and the pair scan costs O(n).
- **Space** is O(n) for the sorted copy.

```java run
import java.util.Arrays;
import java.util.Random;

public final class FourNotAbove {
    /**
     * Returns the largest sum of four values not above target, or -1 when none exists.
     * Time: O(n^3).
     * Space: O(n).
     * Invariant: best is the largest sum not above target among the combinations passed.
     */
    static long largestUnder(int[] input, long target) {
        int[] a = input.clone();
        Arrays.sort(a);
        int n = a.length;
        long best = -1;
        for (int i = 0; i + 3 < n; i++) {
            for (int j = i + 1; j + 2 < n; j++) {
                long rem = target - a[i] - a[j];
                int left = j + 1, right = n - 1;
                while (left < right) {
                    long pair = (long) a[left] + a[right];
                    if (pair <= rem) {
                        // The pair fits, so it is a candidate, and a larger left value may fit better.
                        best = Math.max(best, (long) a[i] + a[j] + pair);
                        left++;
                    } else {
                        // The pair is too large, and a smaller right value is the only way to shrink it.
                        right--;
                    }
                }
            }
        }
        return best;
    }

    public static void main(String[] args) {
        // The statement examples.
        if (largestUnder(new int[] {7, 3, 2, 9, 4}, 20) != 18) throw new AssertionError("example 1");
        if (largestUnder(new int[] {5, 5, 5, 5}, 19) != -1) throw new AssertionError("example 2");
        // Large values stay exact.
        int big = 1_000_000_000;
        if (largestUnder(new int[] {big, big, big, big}, 4L * big) != 4L * big) throw new AssertionError("large");
        // Fewer than four values.
        if (largestUnder(new int[] {1, 2, 3}, 100) != -1) throw new AssertionError("short");
        // Random arrays against four nested loops.
        Random rnd = new Random(84);
        for (int t = 0; t < 3000; t++) {
            int[] a = rnd.ints(rnd.nextInt(9), 1, 10).toArray();
            long target = rnd.nextInt(40);
            long expect = -1;
            for (int i = 0; i < a.length; i++) for (int j = i + 1; j < a.length; j++) for (int k = j + 1; k < a.length; k++) for (int l = k + 1; l < a.length; l++) {
                long s = a[i] + a[j] + a[k] + a[l];
                if (s <= target) expect = Math.max(expect, s);
            }
            if (largestUnder(a, target) != expect) throw new AssertionError("random " + Arrays.toString(a));
        }
    }
}
```
