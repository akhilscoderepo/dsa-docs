<!-- solutions-for: 08-sorting-and-two-pointers -->
### Sorting And Two Pointers

#### Solution: [Build] Two Sum II (LeetCode 167)
<!-- id: tp-pair-original-indices -->

**Approach.** Build an index order, an array of boxed slot numbers, and sort it by the value each slot holds, using `Integer.compare` so large values cannot overflow a subtraction. Run the opposite-end window over that order, computing each sum as a `long` before comparing it with the target. A small sum drops the left end and a large one drops the right end. On a hit, return the two original slot numbers with the smaller first. Because only the index order is sorted, the array handed in is never modified, and the check asserts this by comparing it with a saved copy. The oracle tries all pairs, and the check requires that the returned pair is valid whenever the oracle finds one and is minus one twice otherwise. A counter shows that the window loop runs at most n steps after the sort.

**Complexity.** The sort dominates at O(n log n) time, the window adds O(n), and the index order takes O(n) extra space.

```java run
import java.util.Arrays;
import java.util.Random;

public final class PairOriginalIndices {
    static int windowSteps;

    static int[] pairByOriginalIndex(int[] nums, int target) {
        Integer[] order = new Integer[nums.length];
        for (int k = 0; k < order.length; k++) order[k] = k;
        Arrays.sort(order, (x, y) -> Integer.compare(nums[x], nums[y]));
        int lo = 0, hi = order.length - 1;
        while (lo < hi) {
            windowSteps++;
            long sum = (long) nums[order[lo]] + nums[order[hi]];
            if (sum == target) {
                int p = order[lo], q = order[hi];
                return new int[] {Math.min(p, q), Math.max(p, q)};
            }
            if (sum < target) lo++; else hi--;
        }
        return new int[] {-1, -1};
    }

    static boolean exists(int[] nums, int target) {
        for (int a = 0; a < nums.length; a++)
            for (int b = a + 1; b < nums.length; b++)
                if ((long) nums[a] + nums[b] == target) return true;
        return false;
    }

    public static void main(String[] args) {
        int[] one = {8, 3, 11, 5, 2, 9};
        if (!Arrays.equals(pairByOriginalIndex(one, 17), new int[] {0, 5})) throw new AssertionError("example 1");
        if (!Arrays.equals(pairByOriginalIndex(new int[] {4, 4, 9}, 8), new int[] {0, 1})) throw new AssertionError("example 2");
        if (!Arrays.equals(one, new int[] {8, 3, 11, 5, 2, 9})) throw new AssertionError("input was modified");
        if (!Arrays.equals(pairByOriginalIndex(new int[] {Integer.MAX_VALUE, Integer.MAX_VALUE}, -2), new int[] {-1, -1})) throw new AssertionError("overflow gave a false hit");
        if (!Arrays.equals(pairByOriginalIndex(new int[0], 0), new int[] {-1, -1})) throw new AssertionError("empty");
        if (!Arrays.equals(pairByOriginalIndex(new int[] {5}, 10), new int[] {-1, -1})) throw new AssertionError("one element");
        Random rnd = new Random(8101);
        for (int t = 0; t < 4000; t++) {
            int n = rnd.nextInt(10);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) {
                int pick = rnd.nextInt(12);
                a[i] = pick == 0 ? Integer.MAX_VALUE : pick == 1 ? Integer.MIN_VALUE : rnd.nextInt(9) - 4;
            }
            int[] copy = a.clone();
            int target = rnd.nextInt(5) == 0 ? Integer.MAX_VALUE : rnd.nextInt(15) - 7;
            windowSteps = 0;
            int[] got = pairByOriginalIndex(a, target);
            if (!Arrays.equals(a, copy)) throw new AssertionError("mutated " + Arrays.toString(copy));
            if (windowSteps > Math.max(0, n - 1)) throw new AssertionError("window loop exceeded n steps");
            if (exists(a, target)) {
                if (got[0] < 0 || got[0] >= got[1] || got[1] >= n || (long) a[got[0]] + a[got[1]] != target)
                    throw new AssertionError("invalid pair " + Arrays.toString(got) + " for " + Arrays.toString(a) + " target " + target);
            } else if (!Arrays.equals(got, new int[] {-1, -1})) throw new AssertionError("expected none for " + Arrays.toString(a));
        }
    }
}
```

#### Solution: [Vary] 3Sum (LeetCode 15)
<!-- id: tp-count-zero-triplets -->

**Approach.** Sort a clone, so the caller's array is unchanged, and walk a fixed anchor from left to right. The anchor loop stops at the first positive value, and an anchor equal to the one before it is skipped before any pointer is set. For each anchor the window runs over the positions after it. A negative sum raises `lo`, a positive sum lowers `hi`, and a zero sum adds one to the count, then moves `lo` past every copy of its value and `hi` past every copy of its own, in that order and each bounded by `lo < hi`. A counter adds one for every pointer move, and the check asserts that it is below `n * n` on an input of 2000 distinct values and on random ones. The oracle collects the sorted value triples of all position triples into a set and compares its size.

**Complexity.** Sorting is O(n log n) and the anchor loop with its windows is O(n^2) time, with O(n) space for the sorted clone.

```java run
import java.util.Arrays;
import java.util.HashSet;
import java.util.Random;
import java.util.Set;

public final class CountZeroTriplets {
    static long moves;

    static int countZeroTriples(int[] nums) {
        int[] a = nums.clone();
        Arrays.sort(a);
        int count = 0;
        for (int anchor = 0; anchor + 2 < a.length && a[anchor] <= 0; anchor++) {
            if (anchor > 0 && a[anchor] == a[anchor - 1]) continue;
            int lo = anchor + 1, hi = a.length - 1;
            while (lo < hi) {
                long sum = (long) a[anchor] + a[lo] + a[hi];
                if (sum < 0) { lo++; moves++; }
                else if (sum > 0) { hi--; moves++; }
                else {
                    count++;
                    int left = a[lo], right = a[hi];
                    while (lo < hi && a[lo] == left) { lo++; moves++; }
                    while (lo < hi && a[hi] == right) { hi--; moves++; }
                }
            }
        }
        return count;
    }

    static int oracle(int[] a) {
        Set<String> seen = new HashSet<>();
        for (int i = 0; i < a.length; i++)
            for (int j = i + 1; j < a.length; j++)
                for (int k = j + 1; k < a.length; k++)
                    if ((long) a[i] + a[j] + a[k] == 0) {
                        int[] v = {a[i], a[j], a[k]};
                        Arrays.sort(v);
                        seen.add(Arrays.toString(v));
                    }
        return seen.size();
    }

    public static void main(String[] args) {
        int[] one = {-2, 0, 1, 1, 2, -2};
        if (countZeroTriples(one) != 2) throw new AssertionError("example 1");
        if (!Arrays.equals(one, new int[] {-2, 0, 1, 1, 2, -2})) throw new AssertionError("input was modified");
        if (countZeroTriples(new int[] {0, 0, 0, 0}) != 1) throw new AssertionError("example 2");
        if (countZeroTriples(new int[0]) != 0 || countZeroTriples(new int[] {0}) != 0 || countZeroTriples(new int[] {0, 0}) != 0)
            throw new AssertionError("short arrays");
        if (countZeroTriples(new int[] {1, 2, 3}) != 0) throw new AssertionError("all positive");
        int n = 2000;
        int[] big = new int[n];
        for (int i = 0; i < n; i++) big[i] = i - 1000;
        moves = 0;
        countZeroTriples(big);
        if (moves > (long) n * n) throw new AssertionError("moves " + moves);
        Random rnd = new Random(8102);
        for (int t = 0; t < 4000; t++) {
            int len = rnd.nextInt(12);
            int[] a = new int[len];
            for (int i = 0; i < len; i++) a[i] = rnd.nextInt(9) - 4;
            int[] copy = a.clone();
            moves = 0;
            int got = countZeroTriples(a);
            if (got != oracle(a)) throw new AssertionError("differs on " + Arrays.toString(copy));
            if (!Arrays.equals(a, copy)) throw new AssertionError("mutated");
            if (moves > (long) len * len) throw new AssertionError("quadratic bound broken");
        }
    }
}
```

#### Solution: [Boundary] 3Sum Closest (LeetCode 16)
<!-- id: tp-closest-sum-tie-smaller -->

**Approach.** Sort a clone and seed the best sum with the first three values, so a row of exactly three entries is already settled. For each anchor, run the window over the positions after it and compare each sum with the best by gap. The best is replaced when the new gap is smaller, or equal with a smaller sum. The loop does not need a special exit at an exact hit, since a gap of zero is never replaced by a larger one. Move `lo` when the sum is below the target and `hi` otherwise. The gap uses `long` arithmetic, since three `int` values near the limits reach beyond the `int` range and the target may too. The oracle checks all position triples, and the check includes the all-large example and the tie example.

**Complexity.** O(n^2) time after the O(n log n) sort, and O(n) space for the clone.

```java run
import java.util.Arrays;
import java.util.Random;

public final class ClosestSumTie {
    static long closestSum(int[] nums, long target) {
        int[] a = nums.clone();
        Arrays.sort(a);
        long best = (long) a[0] + a[1] + a[2];
        for (int anchor = 0; anchor + 2 < a.length; anchor++) {
            int lo = anchor + 1, hi = a.length - 1;
            while (lo < hi) {
                long sum = (long) a[anchor] + a[lo] + a[hi];
                long gap = Math.abs(sum - target), bestGap = Math.abs(best - target);
                if (gap < bestGap || (gap == bestGap && sum < best)) best = sum;
                if (sum < target) lo++; else hi--;
            }
        }
        return best;
    }

    static long oracle(int[] a, long target) {
        boolean have = false;
        long best = 0;
        for (int i = 0; i < a.length; i++)
            for (int j = i + 1; j < a.length; j++)
                for (int k = j + 1; k < a.length; k++) {
                    long sum = (long) a[i] + a[j] + a[k];
                    if (!have || Math.abs(sum - target) < Math.abs(best - target)
                            || (Math.abs(sum - target) == Math.abs(best - target) && sum < best)) {
                        best = sum;
                        have = true;
                    }
                }
        return best;
    }

    public static void main(String[] args) {
        int[] three = {2000000000, 2000000000, 2000000000};
        if (closestSum(three, 0) != 6000000000L) throw new AssertionError("example 1");
        if (closestSum(new int[] {1, 2, 4, 8}, 9) != 7) throw new AssertionError("example 2 tie must pick the smaller sum");
        if (closestSum(new int[] {1, 2, 4, 8}, 10) != 11) throw new AssertionError("a clear winner on the larger side");
        if (closestSum(new int[] {Integer.MIN_VALUE, Integer.MIN_VALUE, Integer.MIN_VALUE}, 0) != 3L * Integer.MIN_VALUE)
            throw new AssertionError("negative extreme");
        if (closestSum(new int[] {5, 5, 5, 5}, 15) != 15) throw new AssertionError("all equal exact");
        Random rnd = new Random(8103);
        for (int t = 0; t < 4000; t++) {
            int n = 3 + rnd.nextInt(7);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) {
                int pick = rnd.nextInt(10);
                a[i] = pick == 0 ? Integer.MAX_VALUE : pick == 1 ? Integer.MIN_VALUE : rnd.nextInt(11) - 5;
            }
            int[] copy = a.clone();
            long target = rnd.nextInt(4) == 0 ? (rnd.nextBoolean() ? 6000000000L : -6000000000L) : rnd.nextInt(31) - 15;
            if (closestSum(a, target) != oracle(a, target)) throw new AssertionError("differs on " + Arrays.toString(a) + " target " + target);
            if (!Arrays.equals(a, copy)) throw new AssertionError("mutated");
        }
    }
}
```

#### Solution: [Recognize] 4Sum (LeetCode 18)
<!-- id: tp-quads-pruned -->

**Approach.** Sort a clone. Two nested anchors, `i` and `j`, each skip a value equal to the one before it at the same depth, which is `i` against `i - 1` and `j` against `j - 1` only when `j` is past its first position. Then the window over the rest finds the pairs, skipping copies after a hit exactly as in the triple search. The pruning tests use `long` sums of the four smallest values after the anchor and of the anchor plus the three largest values overall. If the smallest reachable sum already exceeds the target, the loop at that depth can end, since every later anchor only raises it. If the largest reachable sum is still below the target, the anchor is skipped. The check runs the same method with pruning off and on, asserts both equal each other and a brute-force set on random input with duplicates and extremes, asserts that the input is unchanged, and shows that pruning does fewer pointer moves on a larger input.

**Complexity.** O(n^3) time in the worst case with or without pruning, which pruning only improves in practice, and O(n) space for the clone and the output.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Comparator;
import java.util.HashSet;
import java.util.List;
import java.util.Random;
import java.util.Set;

public final class QuadsPruned {
    static long moves;

    static List<List<Integer>> fourSum(int[] nums, int target, boolean prune) {
        int[] a = nums.clone();
        Arrays.sort(a);
        int n = a.length;
        List<List<Integer>> out = new ArrayList<>();
        for (int i = 0; i + 3 < n; i++) {
            if (i > 0 && a[i] == a[i - 1]) continue;
            if (prune) {
                if ((long) a[i] + a[i + 1] + a[i + 2] + a[i + 3] > target) break;
                if ((long) a[i] + a[n - 3] + a[n - 2] + a[n - 1] < target) continue;
            }
            for (int j = i + 1; j + 2 < n; j++) {
                if (j > i + 1 && a[j] == a[j - 1]) continue;
                if (prune) {
                    if ((long) a[i] + a[j] + a[j + 1] + a[j + 2] > target) break;
                    if ((long) a[i] + a[j] + a[n - 2] + a[n - 1] < target) continue;
                }
                int lo = j + 1, hi = n - 1;
                while (lo < hi) {
                    long sum = (long) a[i] + a[j] + a[lo] + a[hi];
                    if (sum < target) { lo++; moves++; }
                    else if (sum > target) { hi--; moves++; }
                    else {
                        out.add(List.of(a[i], a[j], a[lo], a[hi]));
                        int left = a[lo], right = a[hi];
                        while (lo < hi && a[lo] == left) { lo++; moves++; }
                        while (lo < hi && a[hi] == right) { hi--; moves++; }
                    }
                }
            }
        }
        return out;
    }

    static List<List<Integer>> oracle(int[] a, long target) {
        Set<List<Integer>> seen = new HashSet<>();
        int n = a.length;
        for (int i = 0; i < n; i++)
            for (int j = i + 1; j < n; j++)
                for (int k = j + 1; k < n; k++)
                    for (int m = k + 1; m < n; m++)
                        if ((long) a[i] + a[j] + a[k] + a[m] == target) {
                            int[] v = {a[i], a[j], a[k], a[m]};
                            Arrays.sort(v);
                            seen.add(List.of(v[0], v[1], v[2], v[3]));
                        }
        List<List<Integer>> list = new ArrayList<>(seen);
        list.sort(Comparator.<List<Integer>>comparingInt(l -> l.get(0)).thenComparingInt(l -> l.get(1))
                .thenComparingInt(l -> l.get(2)).thenComparingInt(l -> l.get(3)));
        return list;
    }

    public static void main(String[] args) {
        int[] one = {3, 0, 1, 2, 1, 2, 0};
        List<List<Integer>> expected = List.of(List.of(0, 1, 2, 3), List.of(1, 1, 2, 2));
        if (!fourSum(one, 6, true).equals(expected)) throw new AssertionError("example 1 pruned");
        if (!fourSum(one, 6, false).equals(expected)) throw new AssertionError("example 1 plain");
        if (!Arrays.equals(one, new int[] {3, 0, 1, 2, 1, 2, 0})) throw new AssertionError("input was modified");
        int[] huge = {1000000000, 1000000000, 1000000000, 1000000000};
        if (!fourSum(huge, -294967296, true).isEmpty()) throw new AssertionError("example 2 overflowed");
        if (!fourSum(huge, -294967296, false).isEmpty()) throw new AssertionError("example 2 plain overflowed");
        if ((huge[0] + huge[1] + huge[2] + huge[3]) != -294967296) throw new AssertionError("int sum should wrap to the example target");
        if (fourSum(new int[] {5, 5, 5, 5}, 20, true).size() != 1) throw new AssertionError("all equal");
        if (!fourSum(new int[] {1, 2, 3}, 6, true).isEmpty() || !fourSum(new int[0], 0, true).isEmpty()) throw new AssertionError("short");
        Random rnd = new Random(8104);
        for (int t = 0; t < 4000; t++) {
            int n = rnd.nextInt(11);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) {
                int pick = rnd.nextInt(12);
                a[i] = pick == 0 ? Integer.MAX_VALUE : pick == 1 ? Integer.MIN_VALUE : rnd.nextInt(7) - 3;
            }
            int[] copy = a.clone();
            int target = rnd.nextInt(6) == 0 ? Integer.MAX_VALUE : rnd.nextInt(13) - 6;
            List<List<Integer>> plain = fourSum(a, target, false);
            List<List<Integer>> pruned = fourSum(a, target, true);
            if (!plain.equals(pruned)) throw new AssertionError("pruning changed the result on " + Arrays.toString(copy));
            if (!pruned.equals(oracle(a, target))) throw new AssertionError("differs from oracle on " + Arrays.toString(copy));
            if (!Arrays.equals(a, copy)) throw new AssertionError("mutated");
        }
        int[] many = new int[120];
        for (int i = 0; i < many.length; i++) many[i] = i * 3 - 100;
        moves = 0;
        fourSum(many, -500, false);
        long plainMoves = moves;
        moves = 0;
        fourSum(many, -500, true);
        if (moves >= plainMoves) throw new AssertionError("pruning saved nothing: " + moves + " vs " + plainMoves);
    }
}
```
