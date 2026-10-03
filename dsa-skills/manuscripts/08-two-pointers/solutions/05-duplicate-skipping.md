<!-- solutions-for: 08-duplicate-skipping -->
### Duplicate Skipping

#### Solution: [Build] Unique Pairs (Author exercise)
<!-- id: tp-unique-pairs -->

**Approach.** Two pointers start at the ends of the sorted array. A sum below the target pushes the left pointer up and a larger sum pulls the right pointer down. On a match the pair is appended first, and only then are both pointers moved past every position that holds the value just used, so the pair cannot be rebuilt from a twin. The input is promised sorted, so the method reads it and never writes it. The check counts pointer moves to confirm the bound of 2n, compares with a brute force over all position pairs on random arrays with heavy repetition, includes values at the `int` limits where the pair sum needs `long`, and confirms that the input array is unchanged.

**Complexity.** Linear time in the array length, since the pointers only approach each other, and constant extra space besides the output.

```java run
import java.util.*;

public final class UniquePairs {
    static int moves;

    static List<int[]> uniquePairs(int[] nums, long target) {
        List<int[]> out = new ArrayList<>();
        int lo = 0, hi = nums.length - 1;
        while (lo < hi) {
            long total = (long) nums[lo] + nums[hi];
            if (total == target) {
                out.add(new int[] {nums[lo], nums[hi]});
                int x = nums[lo], y = nums[hi];
                while (lo < hi && nums[lo] == x) { lo++; moves++; }
                while (lo < hi && nums[hi] == y) { hi--; moves++; }
            } else if (total < target) { lo++; moves++; }
            else { hi--; moves++; }
        }
        return out;
    }

    static List<List<Integer>> oracle(int[] nums, long target) {
        TreeSet<List<Integer>> found = new TreeSet<>((p, q) -> p.get(0) != q.get(0).intValue() ? Integer.compare(p.get(0), q.get(0)) : Integer.compare(p.get(1), q.get(1)));
        for (int i = 0; i < nums.length; i++)
            for (int j = i + 1; j < nums.length; j++)
                if ((long) nums[i] + nums[j] == target) found.add(List.of(Math.min(nums[i], nums[j]), Math.max(nums[i], nums[j])));
        return new ArrayList<>(found);
    }

    static List<List<Integer>> asLists(List<int[]> pairs) {
        List<List<Integer>> out = new ArrayList<>();
        for (int[] p : pairs) out.add(List.of(p[0], p[1]));
        return out;
    }

    public static void main(String[] args) {
        if (!asLists(uniquePairs(new int[] {1, 1, 2, 3, 3, 4, 5, 5}, 6)).equals(List.of(List.of(1, 5), List.of(2, 4), List.of(3, 3)))) throw new AssertionError("example 1");
        if (!asLists(uniquePairs(new int[] {2, 2, 2, 2}, 4)).equals(List.of(List.of(2, 2)))) throw new AssertionError("example 2");
        if (!uniquePairs(new int[0], 0).isEmpty()) throw new AssertionError("empty");
        if (!uniquePairs(new int[] {5}, 10).isEmpty()) throw new AssertionError("one element cannot pair with itself");
        int[] extremes = {Integer.MAX_VALUE, Integer.MAX_VALUE};
        if (!asLists(uniquePairs(extremes, 2L * Integer.MAX_VALUE)).equals(List.of(List.of(Integer.MAX_VALUE, Integer.MAX_VALUE)))) throw new AssertionError("long sum at the limit");
        if (Integer.MAX_VALUE + Integer.MAX_VALUE >= 0) throw new AssertionError("int addition should wrap here");
        Random rnd = new Random(851);
        for (int t = 0; t < 4000; t++) {
            int n = rnd.nextInt(13);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(7) - 3;
            Arrays.sort(a);
            int[] before = a.clone();
            long target = rnd.nextInt(13) - 6;
            moves = 0;
            List<List<Integer>> got = asLists(uniquePairs(a, target));
            if (!got.equals(oracle(a, target))) throw new AssertionError("differs on " + Arrays.toString(a) + " target " + target);
            if (!Arrays.equals(a, before)) throw new AssertionError("input was modified");
            if (moves > 2 * n) throw new AssertionError("too many moves " + moves + " for n=" + n);
        }
        int[] big = new int[100000];
        Arrays.fill(big, 4);
        moves = 0;
        if (uniquePairs(big, 8).size() != 1) throw new AssertionError("all equal");
        if (moves > 2 * big.length) throw new AssertionError("linear bound " + moves);
    }
}
```

#### Solution: [Vary] 3Sum (LeetCode 15)
<!-- id: tp-three-sum-all -->

**Approach.** Sort the array in place, which the contract allows, so that equal numbers form runs. The outer loop chooses a position and skips it when it holds the same number as the position just before it, because that earlier twin has already run its whole hunt. The pair scan then starts one position to the right of the chosen one, so a twin of the chosen number is still available as a partner. A match is recorded before both pointers leave their runs. The check sorts a copy to prove that the method really leaves the input sorted, compares with a brute force over every position triple that stores sorted trios in a tree set, verifies that the output has no repeat and is in lexicographic order, and uses numbers near a billion so that `int` addition would wrap. It also shows why boxed integers must not be compared with `==`.

**Complexity.** O(n log n) to sort plus O(n^2) for the sweeps, and the output list is the only memory used beyond the sort.

```java run
import java.util.*;

public final class ThreeSumAll {
    static List<List<Integer>> threeSum(int[] nums) {
        Arrays.sort(nums);
        List<List<Integer>> answer = new ArrayList<>();
        for (int p = 0; p + 2 < nums.length; p++) {
            if (p > 0 && nums[p] == nums[p - 1]) continue;
            int l = p + 1, r = nums.length - 1;
            while (l < r) {
                long total = (long) nums[p] + nums[l] + nums[r];
                if (total > 0) r--;
                else if (total < 0) l++;
                else {
                    answer.add(Arrays.asList(nums[p], nums[l], nums[r]));
                    int lv = nums[l], rv = nums[r];
                    do { l++; } while (l < r && nums[l] == lv);
                    do { r--; } while (l < r && nums[r] == rv);
                }
            }
        }
        return answer;
    }

    static int compareLists(List<Integer> a, List<Integer> b) {
        for (int i = 0; i < a.size(); i++) {
            int c = Integer.compare(a.get(i), b.get(i));
            if (c != 0) return c;
        }
        return 0;
    }

    static List<List<Integer>> oracle(int[] nums) {
        TreeSet<List<Integer>> found = new TreeSet<>(ThreeSumAll::compareLists);
        for (int i = 0; i < nums.length; i++)
            for (int j = i + 1; j < nums.length; j++)
                for (int k = j + 1; k < nums.length; k++)
                    if ((long) nums[i] + nums[j] + nums[k] == 0) {
                        int[] t = {nums[i], nums[j], nums[k]};
                        Arrays.sort(t);
                        found.add(List.of(t[0], t[1], t[2]));
                    }
        return new ArrayList<>(found);
    }

    static void check(int[] original) {
        int[] work = original.clone();
        List<List<Integer>> got = threeSum(work);
        int[] sortedCopy = original.clone();
        Arrays.sort(sortedCopy);
        if (!Arrays.equals(work, sortedCopy)) throw new AssertionError("input should be left sorted");
        List<List<Integer>> want = oracle(original);
        if (!got.equals(want)) throw new AssertionError("differs on " + Arrays.toString(original) + ": " + got + " vs " + want);
        for (int i = 1; i < got.size(); i++)
            if (compareLists(got.get(i - 1), got.get(i)) >= 0) throw new AssertionError("repeat or disorder on " + Arrays.toString(original));
    }

    public static void main(String[] args) {
        if (!threeSum(new int[] {-4, 2, -2, 0, 2, 0, -2, 4}).equals(List.of(List.of(-4, 0, 4), List.of(-4, 2, 2), List.of(-2, -2, 4), List.of(-2, 0, 2)))) throw new AssertionError("example 1");
        if (!threeSum(new int[] {3, -1, -1, -1, 2}).equals(List.of(List.of(-1, -1, 2)))) throw new AssertionError("example 2");
        check(new int[0]);
        check(new int[] {0});
        check(new int[] {0, 0});
        check(new int[] {0, 0, 0});
        check(new int[] {1_000_000_000, 1_000_000_000, -2_000_000_000});
        check(new int[] {1_000_000_000, 1_000_000_000, 1_000_000_000});
        if (1_000_000_000 + 1_000_000_000 + 1_000_000_000 >= 0) throw new AssertionError("int sum should wrap negative");
        Integer boxedA = 1000, boxedB = 1000;
        if (boxedA == boxedB) throw new AssertionError("boxed values outside the small cache are distinct objects");
        if (!boxedA.equals(boxedB)) throw new AssertionError("equals compares the numbers");
        Random rnd = new Random(852);
        for (int t = 0; t < 3000; t++) {
            int n = rnd.nextInt(12);
            int range = 1 + rnd.nextInt(6);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(2 * range + 1) - range;
            check(a);
        }
    }
}
```

#### Solution: [Boundary] All Equal (Author exercise)
<!-- id: tp-all-equal -->

**Approach.** Handle the array as a single run at both levels. For zeros, the outer loop starts one hunt at position 0: the pair scan finds the first trio at once, then each pointer skips the run and the scan ends because the pointers meet. Every later outer position holds the same number as the one before it, so each costs a single comparison and no scan. For a nonzero repeated value the pair scan moves one pointer per step and finds nothing. The method counts every advance of the outer index and both pointers. The check feeds arrays of every length up to 300 filled with one value, confirms the answer and the bound of 4n, and compares with a brute force on random arrays that contain long runs.

**Complexity.** At most about 2n advances on an all-equal array and O(n^2) in general, with the output as the only extra memory.

```java run
import java.util.*;

public final class AllEqualRun {
    static long advances;

    static List<List<Integer>> triples(int[] nums) {
        int[] s = nums.clone();
        Arrays.sort(s);
        List<List<Integer>> res = new ArrayList<>();
        for (int c = 0; c + 2 < s.length; c++, advances++) {
            if (c > 0 && s[c] == s[c - 1]) continue;
            int left = c + 1, right = s.length - 1;
            while (left < right) {
                long total = (long) s[c] + s[left] + s[right];
                if (total < 0) { left++; advances++; }
                else if (total > 0) { right--; advances++; }
                else {
                    res.add(List.of(s[c], s[left], s[right]));
                    int a = s[left], b = s[right];
                    while (left < right && s[left] == a) { left++; advances++; }
                    while (left < right && s[right] == b) { right--; advances++; }
                }
            }
        }
        return res;
    }

    static List<List<Integer>> oracle(int[] nums) {
        Set<List<Integer>> found = new HashSet<>();
        for (int i = 0; i < nums.length; i++)
            for (int j = i + 1; j < nums.length; j++)
                for (int k = j + 1; k < nums.length; k++)
                    if ((long) nums[i] + nums[j] + nums[k] == 0) {
                        int[] t = {nums[i], nums[j], nums[k]};
                        Arrays.sort(t);
                        found.add(List.of(t[0], t[1], t[2]));
                    }
        List<List<Integer>> list = new ArrayList<>(found);
        list.sort((x, y) -> { for (int i = 0; i < 3; i++) { int c = Integer.compare(x.get(i), y.get(i)); if (c != 0) return c; } return 0; });
        return list;
    }

    public static void main(String[] args) {
        if (!triples(new int[] {0, 0, 0, 0}).equals(List.of(List.of(0, 0, 0)))) throw new AssertionError("example 1");
        if (!triples(new int[] {7, 7, 7, 7, 7}).isEmpty()) throw new AssertionError("example 2");
        for (int n = 0; n <= 300; n++) {
            for (int value : new int[] {0, 7, -7}) {
                int[] a = new int[n];
                Arrays.fill(a, value);
                advances = 0;
                List<List<Integer>> got = triples(a);
                boolean expectTrio = value == 0 && n >= 3;
                if (got.size() != (expectTrio ? 1 : 0)) throw new AssertionError("count for n=" + n + " value=" + value);
                if (advances > 4L * n) throw new AssertionError("too many advances " + advances + " for n=" + n);
            }
        }
        Random rnd = new Random(853);
        for (int t = 0; t < 3000; t++) {
            int n = rnd.nextInt(12);
            int[] a = new int[n];
            int base = rnd.nextInt(3) - 1;
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(4) == 0 ? rnd.nextInt(5) - 2 : base;
            int[] before = a.clone();
            if (!triples(a).equals(oracle(a))) throw new AssertionError("differs on " + Arrays.toString(a));
            if (!Arrays.equals(a, before)) throw new AssertionError("this version sorts a copy and must not touch the input");
        }
    }
}
```

#### Solution: [Recognize] 4Sum (LeetCode 18)
<!-- id: tp-four-sum-all -->

**Approach.** Sort in place and open two levels of choice, each with its own backward comparison: the first position skips when it equals the position before it, and the second position, which starts right after the first, skips when it equals the position before it but only if that earlier position is itself inside the second level, so the test is `q > p + 1`. The pair scan covers the rest of the row, records a match before moving, and then leaves both runs. Using `p + 1` as the guard is what keeps a quadruple such as 2, 2, 2, 2 alive, because the second 2 is the representative of its own level. The check compares with a brute force over all position quadruples, tests the sorted-order and no-repeat properties of the output, and uses sums that stay in `long`.

**Complexity.** O(n^3) after the sort, which costs O(n log n), with only the output list as extra memory.

```java run
import java.util.*;

public final class FourSumAll {
    static List<List<Integer>> fourSum(int[] nums, long target) {
        Arrays.sort(nums);
        int n = nums.length;
        List<List<Integer>> out = new ArrayList<>();
        for (int p = 0; p + 3 < n; p++) {
            if (p > 0 && nums[p] == nums[p - 1]) continue;
            for (int q = p + 1; q + 2 < n; q++) {
                if (q > p + 1 && nums[q] == nums[q - 1]) continue;
                int l = q + 1, r = n - 1;
                while (l < r) {
                    long total = (long) nums[p] + nums[q] + nums[l] + nums[r];
                    if (total < target) l++;
                    else if (total > target) r--;
                    else {
                        out.add(List.of(nums[p], nums[q], nums[l], nums[r]));
                        int lv = nums[l], rv = nums[r];
                        while (l < r && nums[l] == lv) l++;
                        while (l < r && nums[r] == rv) r--;
                    }
                }
            }
        }
        return out;
    }

    static int cmp(List<Integer> a, List<Integer> b) {
        for (int i = 0; i < a.size(); i++) {
            int c = Integer.compare(a.get(i), b.get(i));
            if (c != 0) return c;
        }
        return 0;
    }

    static List<List<Integer>> oracle(int[] nums, long target) {
        TreeSet<List<Integer>> found = new TreeSet<>(FourSumAll::cmp);
        int n = nums.length;
        for (int a = 0; a < n; a++)
            for (int b = a + 1; b < n; b++)
                for (int c = b + 1; c < n; c++)
                    for (int d = c + 1; d < n; d++)
                        if ((long) nums[a] + nums[b] + nums[c] + nums[d] == target) {
                            int[] t = {nums[a], nums[b], nums[c], nums[d]};
                            Arrays.sort(t);
                            found.add(List.of(t[0], t[1], t[2], t[3]));
                        }
        return new ArrayList<>(found);
    }

    static void check(int[] original, long target) {
        int[] work = original.clone();
        List<List<Integer>> got = fourSum(work, target);
        List<List<Integer>> want = oracle(original, target);
        if (!got.equals(want)) throw new AssertionError("differs on " + Arrays.toString(original) + " target " + target + ": " + got + " vs " + want);
        for (int i = 1; i < got.size(); i++)
            if (cmp(got.get(i - 1), got.get(i)) >= 0) throw new AssertionError("repeat or disorder");
    }

    public static void main(String[] args) {
        if (!fourSum(new int[] {3, 1, 1, 1, 0, 2, 2, -1}, 5).equals(List.of(List.of(-1, 1, 2, 3), List.of(0, 1, 1, 3), List.of(0, 1, 2, 2), List.of(1, 1, 1, 2)))) throw new AssertionError("example 1");
        if (!fourSum(new int[] {2, 2, 2, 2, 2}, 8).equals(List.of(List.of(2, 2, 2, 2)))) throw new AssertionError("example 2");
        check(new int[0], 0);
        check(new int[] {4}, 4);
        check(new int[] {1, 1, 1}, 3);
        check(new int[] {0, 0, 0, 0}, 0);
        check(new int[] {-1000, 1000, 1000, -1000, 0, 0}, 0);
        int[] sample = {5, 3, 5, 3, 1};
        int[] untouched = sample.clone();
        fourSum(sample, 16);
        Arrays.sort(untouched);
        if (!Arrays.equals(sample, untouched)) throw new AssertionError("the contract allows sorting in place and the method does it");
        Random rnd = new Random(854);
        for (int t = 0; t < 4000; t++) {
            int n = rnd.nextInt(11);
            int range = 1 + rnd.nextInt(4);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(2 * range + 1) - range;
            check(a, rnd.nextInt(4 * range + 1) - 2 * range);
        }
    }
}
```
