<!-- solutions-for: 08-k-sum-reduction -->
### K-Sum Reduction

#### Solution: [Build] 3Sum (LeetCode 15)
<!-- id: tp-triple-exists -->

**Approach.** Sort a copy of the array. A recursive method owns a count `k`, a start position and a remaining target. With `k` above two it picks each position in turn, from the start onward, and asks the same question about the suffix after it with `k - 1` and the target minus the picked value. With `k` equal to two it sweeps from both ends of the suffix. The caller's array is cloned before sorting, so it comes back unchanged, and the target arithmetic is in `long`. The check compares with a subset enumeration for pair, triple and quad counts on random arrays, shows that sums at the `int` limits are handled, counts sweep reads against the quadratic bound for three values, and records the deepest recursion level to show that it never passes `k`.

**Complexity.** For three values, O(n log n) to sort and O(n^2) for the sweeps, with O(n) for the copy and O(k) for the recursion stack.

```java run
import java.util.*;

public final class TripleExists {
    static long sweepReads;
    static int deepest;

    static boolean search(int[] row, int start, int k, long need, int level) {
        deepest = Math.max(deepest, level);
        if (k == 2) {
            int a = start, b = row.length - 1;
            while (a < b) {
                sweepReads++;
                long pair = (long) row[a] + row[b];
                if (pair == need) return true;
                if (pair < need) a++; else b--;
            }
            return false;
        }
        for (int pick = start; pick + k <= row.length; pick++)
            if (search(row, pick + 1, k - 1, need - row[pick], level + 1)) return true;
        return false;
    }

    static boolean anyGroup(int[] nums, int k, long target) {
        int[] copy = nums.clone();
        Arrays.sort(copy);
        return search(copy, 0, k, target, 1);
    }

    static boolean oracle(int[] nums, int k, long target) {
        for (int mask = 0; mask < (1 << nums.length); mask++) {
            if (Integer.bitCount(mask) != k) continue;
            long sum = 0;
            for (int i = 0; i < nums.length; i++) if ((mask >> i & 1) == 1) sum += nums[i];
            if (sum == target) return true;
        }
        return false;
    }

    public static void main(String[] args) {
        int[] ex = {8, -3, 5, 11, 2, -6};
        if (!anyGroup(ex, 3, 10)) throw new AssertionError("example 1");
        if (anyGroup(ex, 3, 40)) throw new AssertionError("example 2");
        if (!oracle(ex, 3, 10) || oracle(ex, 3, 40)) throw new AssertionError("oracle disagrees on the examples");
        if (!Arrays.equals(ex, new int[] {8, -3, 5, 11, 2, -6})) throw new AssertionError("input was modified");
        if (anyGroup(new int[0], 3, 0) || anyGroup(new int[] {4, 4}, 3, 12)) throw new AssertionError("too few elements");
        if (!anyGroup(new int[] {4, 4, 4}, 3, 12)) throw new AssertionError("exactly three elements");
        int[] extremes = {Integer.MAX_VALUE, Integer.MAX_VALUE, Integer.MAX_VALUE};
        if (!anyGroup(extremes, 3, 3L * Integer.MAX_VALUE)) throw new AssertionError("long arithmetic at the limit");
        if (anyGroup(extremes, 3, 3L * Integer.MAX_VALUE - 1)) throw new AssertionError("one below the limit");
        if (Integer.MAX_VALUE + Integer.MAX_VALUE + Integer.MAX_VALUE != 2147483645) throw new AssertionError("int addition wraps to a different number");
        Random rnd = new Random(861);
        for (int t = 0; t < 3000; t++) {
            int n = rnd.nextInt(10);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = switch (rnd.nextInt(4)) { case 0 -> Integer.MAX_VALUE; case 1 -> Integer.MIN_VALUE; default -> rnd.nextInt(9) - 4; };
            int[] before = a.clone();
            for (int k = 2; k <= 4; k++) {
                long target = rnd.nextInt(3) == 0 ? (long) k * Integer.MAX_VALUE - rnd.nextInt(3) : rnd.nextInt(17) - 8;
                deepest = 0;
                if (anyGroup(a, k, target) != oracle(a, k, target)) throw new AssertionError("differs on " + Arrays.toString(a) + " k=" + k + " target " + target);
                if (deepest > k - 1) throw new AssertionError("recursion level " + deepest);
            }
            if (!Arrays.equals(a, before)) throw new AssertionError("input was modified");
        }
        for (int n : new int[] {50, 200, 800}) {
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = 10 * i;
            sweepReads = 0;
            if (anyGroup(a, 3, -1)) throw new AssertionError("unreachable target");
            if (sweepReads > (long) n * n) throw new AssertionError("more than quadratic: " + sweepReads);
        }
    }
}
```

#### Solution: [Vary] 3Sum Closest (LeetCode 16)
<!-- id: tp-closest-total -->

**Approach.** Sort a copy and pick each position `i` that still leaves two positions to its right. For each pick the sweep keeps the distance of the best total so far in a variable, and updates it only when a total is strictly closer. A total below the target moves the left end up and a total above it moves the right end down, which is the same decision as in the exact version because only that move can bring the total nearer. An exact hit ends everything at once. The check enumerates every triple of positions to find the true minimum distance, confirms that the returned value is a total that some triple really produces, confirms that the input stays as given, and uses values at the `int` limits where an `int` sum would be wrong.

**Complexity.** O(n log n) to sort plus O(n^2) for the sweeps, and O(n) for the copy.

```java run
import java.util.*;

public final class NearestTotal {
    static long nearest(int[] nums, long target) {
        int[] s = nums.clone();
        Arrays.sort(s);
        long answer = (long) s[0] + s[1] + s[2];
        long gap = Math.abs(answer - target);
        for (int i = 0; i + 2 < s.length; i++) {
            int lo = i + 1, hi = s.length - 1;
            while (lo < hi) {
                long total = (long) s[i] + s[lo] + s[hi];
                long d = Math.abs(total - target);
                if (d < gap) { gap = d; answer = total; }
                if (d == 0) return total;
                if (total < target) lo++; else hi--;
            }
        }
        return answer;
    }

    static void check(int[] nums, long target) {
        int[] before = nums.clone();
        long got = nearest(nums, target);
        long bestGap = Long.MAX_VALUE;
        boolean achievable = false;
        for (int a = 0; a < nums.length; a++)
            for (int b = a + 1; b < nums.length; b++)
                for (int c = b + 1; c < nums.length; c++) {
                    long total = (long) nums[a] + nums[b] + nums[c];
                    bestGap = Math.min(bestGap, Math.abs(total - target));
                    if (total == got) achievable = true;
                }
        if (!achievable) throw new AssertionError("no triple produces " + got);
        if (Math.abs(got - target) != bestGap) throw new AssertionError("not nearest on " + Arrays.toString(nums) + " target " + target + ": " + got);
        if (!Arrays.equals(nums, before)) throw new AssertionError("input was modified");
    }

    public static void main(String[] args) {
        if (nearest(new int[] {14, -6, 3, 9, -2, 7}, 29) != 30) throw new AssertionError("example 1");
        if (nearest(new int[] {5, 5, 5}, 0) != 15) throw new AssertionError("example 2");
        check(new int[] {14, -6, 3, 9, -2, 7}, 29);
        check(new int[] {Integer.MAX_VALUE, Integer.MAX_VALUE, Integer.MAX_VALUE}, 0);
        check(new int[] {Integer.MIN_VALUE, Integer.MIN_VALUE, Integer.MIN_VALUE, Integer.MAX_VALUE}, 5);
        check(new int[] {0, 0, 0}, 0);
        check(new int[] {1, 1, 1, 1}, -7);
        Random rnd = new Random(862);
        for (int t = 0; t < 4000; t++) {
            int n = 3 + rnd.nextInt(8);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = switch (rnd.nextInt(5)) { case 0 -> Integer.MAX_VALUE; case 1 -> Integer.MIN_VALUE; default -> rnd.nextInt(41) - 20; };
            long target = rnd.nextInt(4) == 0 ? (rnd.nextBoolean() ? 3L * Integer.MAX_VALUE : 3L * Integer.MIN_VALUE) + rnd.nextInt(5) : rnd.nextInt(121) - 60;
            check(a, target);
        }
    }
}
```

#### Solution: [Boundary] Overflowing Sum (Author exercise)
<!-- id: tp-overflow-sum -->

**Approach.** Sort a copy. For each pick, the remaining limit is the limit minus the picked value, held in a `long` because it can lie far outside the `int` range. The sweep looks for the heaviest pair that fits under that remaining limit: when a pair fits, it is a candidate, and the only way to find a heavier one is to move the left end up, and when it does not fit, the right end must come down. A candidate total is the pick plus the pair, again in `long`. If nothing ever fits, the method returns `Long.MIN_VALUE`. The check shows with plain arithmetic that three limit values wrap in `int`, compares with a brute force over all triples, and covers the cases of fewer than three elements and of a limit below every total.

**Complexity.** O(n log n) for the sort and O(n^2) for the sweeps, with an O(n) copy.

```java run
import java.util.*;

public final class OverflowingSum {
    static long largestUnder(int[] nums, long limit) {
        if (nums.length < 3) return Long.MIN_VALUE;
        int[] s = nums.clone();
        Arrays.sort(s);
        long best = Long.MIN_VALUE;
        for (int i = 0; i + 2 < s.length; i++) {
            long room = limit - s[i];
            int left = i + 1, right = s.length - 1;
            while (left < right) {
                long pair = (long) s[left] + s[right];
                if (pair <= room) {
                    best = Math.max(best, s[i] + pair);
                    left++;
                } else right--;
            }
        }
        return best;
    }

    static long oracle(int[] nums, long limit) {
        long best = Long.MIN_VALUE;
        for (int a = 0; a < nums.length; a++)
            for (int b = a + 1; b < nums.length; b++)
                for (int c = b + 1; c < nums.length; c++) {
                    long total = (long) nums[a] + nums[b] + nums[c];
                    if (total <= limit && total > best) best = total;
                }
        return best;
    }

    public static void main(String[] args) {
        int max = Integer.MAX_VALUE;
        if (largestUnder(new int[] {max, max, max, -5, 10}, 4294967289L) != 4294967289L) throw new AssertionError("example 1");
        if (largestUnder(new int[] {max, max, max}, 6442450940L) != Long.MIN_VALUE) throw new AssertionError("example 2");
        if (max + max >= 0 || (long) max + max + max != 6442450941L) throw new AssertionError("int sum wraps while the long sum is exact");
        if (max - (-5) >= 0) throw new AssertionError("subtracting a negative int can wrap too");
        if (largestUnder(new int[0], 0) != Long.MIN_VALUE || largestUnder(new int[] {1, 2}, 100) != Long.MIN_VALUE) throw new AssertionError("fewer than three");
        if (largestUnder(new int[] {1, 2, 3}, 5) != Long.MIN_VALUE) throw new AssertionError("limit below the only total");
        if (largestUnder(new int[] {1, 2, 3}, 6) != 6) throw new AssertionError("limit equal to the only total");
        int[] mix = {max, Integer.MIN_VALUE, 7, max, 0};
        int[] before = mix.clone();
        largestUnder(mix, 0);
        if (!Arrays.equals(mix, before)) throw new AssertionError("input was modified");
        Random rnd = new Random(863);
        for (int t = 0; t < 4000; t++) {
            int n = rnd.nextInt(9);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = switch (rnd.nextInt(5)) { case 0 -> max; case 1 -> Integer.MIN_VALUE; case 2 -> max - 1; default -> rnd.nextInt(7) - 3; };
            long limit = switch (rnd.nextInt(3)) { case 0 -> 3L * max - rnd.nextInt(4); case 1 -> 2L * Integer.MIN_VALUE + rnd.nextInt(4); default -> rnd.nextInt(15) - 7; };
            if (largestUnder(a, limit) != oracle(a, limit)) throw new AssertionError("differs on " + Arrays.toString(a) + " limit " + limit);
        }
    }
}
```

#### Solution: [Recognize] 4Sum (LeetCode 18)
<!-- id: tp-four-sum-count -->

**Approach.** Sort a copy and make two picks, each with its own backward comparison, so that a pick is skipped only when it equals the pick just before it at the same level. The second pick starts right after the first, which is why its comparison uses `second > first + 1`. The remaining target after two picks is computed in `long`, and the final sweep reads two values from both ends. A match adds one to a `long` counter and then moves both ends past their runs of equal values, so a quadruplet of values is counted once. The check compares with a brute force that stores sorted quadruplets in a set, uses values at both `int` limits and targets built from real quadruplet sums, checks the two examples, and confirms that the input array is not changed.

**Complexity.** O(n log n) for the sort and O(n^3) for the picks and sweeps, with an O(n) copy.

```java run
import java.util.*;

public final class QuadrupleCount {
    static long countQuads(int[] nums, long target) {
        int[] s = nums.clone();
        Arrays.sort(s);
        int n = s.length;
        long count = 0;
        for (int first = 0; first + 3 < n; first++) {
            if (first > 0 && s[first] == s[first - 1]) continue;
            for (int second = first + 1; second + 2 < n; second++) {
                if (second > first + 1 && s[second] == s[second - 1]) continue;
                long need = target - s[first] - s[second];
                int lo = second + 1, hi = n - 1;
                while (lo < hi) {
                    long pair = (long) s[lo] + s[hi];
                    if (pair < need) lo++;
                    else if (pair > need) hi--;
                    else {
                        count++;
                        int lv = s[lo], hv = s[hi];
                        while (lo < hi && s[lo] == lv) lo++;
                        while (lo < hi && s[hi] == hv) hi--;
                    }
                }
            }
        }
        return count;
    }

    static long oracle(int[] nums, long target) {
        Set<List<Integer>> seen = new HashSet<>();
        int n = nums.length;
        for (int a = 0; a < n; a++)
            for (int b = a + 1; b < n; b++)
                for (int c = b + 1; c < n; c++)
                    for (int d = c + 1; d < n; d++)
                        if ((long) nums[a] + nums[b] + nums[c] + nums[d] == target) {
                            int[] q = {nums[a], nums[b], nums[c], nums[d]};
                            Arrays.sort(q);
                            seen.add(List.of(q[0], q[1], q[2], q[3]));
                        }
        return seen.size();
    }

    public static void main(String[] args) {
        int max = Integer.MAX_VALUE, min = Integer.MIN_VALUE;
        int[] ex1 = {min, max, min, max, 0, -1, 1};
        int[] keep = ex1.clone();
        if (countQuads(ex1, -2) != 2) throw new AssertionError("example 1");
        if (oracle(ex1, -2) != 2) throw new AssertionError("oracle on example 1");
        if (!Arrays.equals(ex1, keep)) throw new AssertionError("input was modified");
        if (countQuads(new int[] {max, max, max, max, max}, 8589934588L) != 1) throw new AssertionError("example 2");
        if (4L * max != 8589934588L) throw new AssertionError("the target in example 2 is four times the limit");
        if (max + max + max + max != -4) throw new AssertionError("an int sum of four limits wraps to minus four");
        if (countQuads(new int[0], 0) != 0 || countQuads(new int[] {1, 2, 3}, 6) != 0) throw new AssertionError("fewer than four");
        if (countQuads(new int[] {0, 0, 0, 0}, 0) != 1) throw new AssertionError("all equal");
        Random rnd = new Random(864);
        int[] pool = {min, min + 1, -1, 0, 1, max - 1, max};
        for (int t = 0; t < 4000; t++) {
            int n = rnd.nextInt(10);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = pool[rnd.nextInt(pool.length)];
            long target;
            if (n >= 4 && rnd.nextBoolean()) {
                target = 0;
                for (int j = 0; j < 4; j++) target += a[rnd.nextInt(n)];
            } else target = rnd.nextInt(9) - 4;
            if (countQuads(a, target) != oracle(a, target)) throw new AssertionError("differs on " + Arrays.toString(a) + " target " + target);
        }
    }
}
```
