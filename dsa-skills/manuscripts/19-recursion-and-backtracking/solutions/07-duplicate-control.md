<!-- solutions-for: 07-duplicate-control -->
### Duplicate Control

#### Solution: [Build] Equal Sibling Choices (Author exercise)
<!-- id: bt-equal-siblings -->

**Approach.** The code builds the unskipped search tree for a sorted array and gathers the value lists recorded under the first pick at position `p` and under the first pick at `p - 1`. Under `p - 1` every later position, `p` included, is still on offer, while under `p` only the positions after it are, so the lists under `p` form a subset of those under `p - 1`, and the pair is always `[a, a]`. The harness checks the two examples, asserts `b == a` on random sorted arrays for every position with an equal left neighbour, and also confirms the converse that the subtree at `p - 1` is strictly larger, which is why the earlier sibling is the one to keep. An independent oracle builds both families with masks, using position sets rather than recursion.

**Complexity.** The subtrees together hold up to 2^n lists, so the check is exponential in n and fine for the small limit.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashSet;
import java.util.List;
import java.util.Random;
import java.util.Set;

public final class EqualSiblings {
    static void walk(int[] v, int start, List<Integer> path, List<List<Integer>> out) {
        out.add(new ArrayList<>(path));
        for (int i = start; i < v.length; i++) {
            path.add(v[i]);
            walk(v, i + 1, path, out);
            path.remove(path.size() - 1);
        }
    }

    static List<List<Integer>> below(int[] v, int p) {
        List<List<Integer>> out = new ArrayList<>();
        List<Integer> path = new ArrayList<>();
        path.add(v[p]);
        walk(v, p + 1, path, out);
        return out;
    }

    static int[] solve(int[] v, int p) {
        List<List<Integer>> a = below(v, p);
        Set<List<Integer>> b = new HashSet<>(below(v, p - 1));
        int shared = 0;
        for (List<Integer> l : a) if (b.contains(l)) shared++;
        return new int[] {a.size(), shared};
    }

    static int[] oracle(int[] v, int p) {
        int n = v.length;
        Set<List<Integer>> under = new HashSet<>();
        for (int m = 0; m < (1 << n); m++) {
            if ((m >> (p - 1) & 1) == 0 || (m & ((1 << (p - 1)) - 1)) != 0) continue;
            List<Integer> l = new ArrayList<>();
            for (int i = 0; i < n; i++) if ((m >> i & 1) == 1) l.add(v[i]);
            under.add(l);
        }
        int size = 0, shared = 0;
        for (int m = 0; m < (1 << n); m++) {
            if ((m >> p & 1) == 0 || (m & ((1 << p) - 1)) != 0) continue;
            List<Integer> l = new ArrayList<>();
            for (int i = 0; i < n; i++) if ((m >> i & 1) == 1) l.add(v[i]);
            size++;
            if (under.contains(l)) shared++;
        }
        return new int[] {size, shared};
    }

    public static void main(String[] args) {
        if (!Arrays.equals(solve(new int[] {1, 2, 2}, 2), new int[] {1, 1})) throw new AssertionError("example 1");
        if (!Arrays.equals(solve(new int[] {3, 3, 3, 5}, 1), new int[] {4, 4})) throw new AssertionError("example 2");
        Random rnd = new Random(19701);
        int checked = 0;
        for (int t = 0; t < 3000; t++) {
            int n = 2 + rnd.nextInt(7);
            int[] v = new int[n];
            for (int i = 0; i < n; i++) v[i] = rnd.nextInt(4) - 1;
            Arrays.sort(v);
            for (int p = 1; p < n; p++) {
                if (v[p] != v[p - 1]) continue;
                int[] got = solve(v, p);
                if (!Arrays.equals(got, oracle(v, p))) throw new AssertionError("differs at p=" + p);
                if (got[0] != got[1]) throw new AssertionError("the later sibling must add nothing new");
                if (below(v, p - 1).size() <= got[0]) throw new AssertionError("the earlier sibling reaches strictly more");
                checked++;
            }
        }
        if (checked == 0) throw new AssertionError("no equal neighbours were tested");
    }
}
```

#### Solution: [Vary] Fixed-Size Distinct Subsets (LeetCode 90)
<!-- id: bt-distinct-size-k -->

**Approach.** The search sorts a copy and applies the test `i > start && vals[i] == vals[i - 1]` inside the loop. It records a copy of the path only when the path has `k` values and does not loop any further at that size. This is the same skip as in the plain distinct-subsets search, with a different recording rule, and the harness proves it by filtering the plain search's output by size and comparing. The oracle takes all masks of the sorted copy with exactly `k` bits, collects value lists in a set, and sorts them lexicographically. A size above the array length gives an empty answer, and an unsorted input is used throughout.

**Complexity.** One node per distinct selection of size up to k, each costing at most a k-element copy, plus the sort.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashSet;
import java.util.List;
import java.util.Random;
import java.util.Set;

public final class DistinctSizeK {
    static void walk(int[] v, int start, int k, List<Integer> path, List<List<Integer>> out) {
        if (path.size() == k) {
            out.add(new ArrayList<>(path));
            return;
        }
        for (int i = start; i < v.length; i++) {
            if (i > start && v[i] == v[i - 1]) continue;
            path.add(v[i]);
            walk(v, i + 1, k, path, out);
            path.remove(path.size() - 1);
        }
    }

    static List<List<Integer>> solve(int[] nums, int k) {
        int[] v = nums.clone();
        Arrays.sort(v);
        List<List<Integer>> out = new ArrayList<>();
        walk(v, 0, k, new ArrayList<>(), out);
        return out;
    }

    static void plain(int[] v, int start, List<Integer> path, List<List<Integer>> out) {
        out.add(new ArrayList<>(path));
        for (int i = start; i < v.length; i++) {
            if (i > start && v[i] == v[i - 1]) continue;
            path.add(v[i]);
            plain(v, i + 1, path, out);
            path.remove(path.size() - 1);
        }
    }

    static int cmp(List<Integer> a, List<Integer> b) {
        for (int i = 0; i < Math.min(a.size(), b.size()); i++) if (!a.get(i).equals(b.get(i))) return a.get(i) - b.get(i);
        return a.size() - b.size();
    }

    static List<List<Integer>> oracle(int[] nums, int k) {
        int[] v = nums.clone();
        Arrays.sort(v);
        int n = v.length;
        Set<List<Integer>> seen = new HashSet<>();
        for (int m = 0; m < (1 << n); m++) {
            if (Integer.bitCount(m) != k) continue;
            List<Integer> l = new ArrayList<>();
            for (int i = 0; i < n; i++) if ((m >> i & 1) == 1) l.add(v[i]);
            seen.add(l);
        }
        List<List<Integer>> out = new ArrayList<>(seen);
        out.sort(DistinctSizeK::cmp);
        return out;
    }

    public static void main(String[] args) {
        if (!solve(new int[] {1, 2, 2}, 2).equals(List.of(List.of(1, 2), List.of(2, 2)))) throw new AssertionError("example 1");
        if (!solve(new int[] {4, 4, 4}, 2).equals(List.of(List.of(4, 4)))) throw new AssertionError("example 2");
        if (!solve(new int[] {1, 1}, 3).isEmpty()) throw new AssertionError("size above the length");
        Random rnd = new Random(19702);
        for (int t = 0; t < 3000; t++) {
            int n = rnd.nextInt(8);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(5) - 2;
            int k = rnd.nextInt(10);
            List<List<Integer>> got = solve(a, k);
            if (!got.equals(oracle(a, k))) throw new AssertionError("differs for k=" + k);
            int[] sorted = a.clone();
            Arrays.sort(sorted);
            List<List<Integer>> all = new ArrayList<>();
            plain(sorted, 0, new ArrayList<>(), all);
            List<List<Integer>> filtered = new ArrayList<>();
            for (List<Integer> l : all) if (l.size() == k) filtered.add(l);
            if (!filtered.equals(got)) throw new AssertionError("filtering the plain search must agree");
        }
    }
}
```

#### Solution: [Boundary] Equal Values At Different Depths (Author exercise)
<!-- id: bt-equal-depths -->

**Approach.** The search is the distinct-subsets walk with the skip test against `start`, and an answer is a path in which some value occurs twice or more, which is checked by comparing neighbours in the sorted path. The second copy of a value is reached one call deeper, at `start` equal to the position after the first copy, where the skip test is not applied, so pairs such as two fives survive. The harness runs a variant with the test `i > 0` and asserts that it loses `[2, 2]` for the first example, and it compares both with an oracle based on masks and a set. It also shows the boxing trap behind the code stage's warning, since two equal `Integer` values above 127 are different objects, while small values are cached.

**Complexity.** One node per distinct subset, each with a copy of at most n values, so the time is proportional to the number of distinct subsets times n.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashSet;
import java.util.List;
import java.util.Random;
import java.util.Set;

public final class EqualDepths {
    static void walk(int[] v, int start, boolean overSkip, List<Integer> path, List<List<Integer>> out) {
        boolean twice = false;
        for (int j = 1; j < path.size(); j++) if (path.get(j).equals(path.get(j - 1))) twice = true;
        if (twice) out.add(new ArrayList<>(path));
        for (int i = start; i < v.length; i++) {
            if (overSkip ? (i > 0 && v[i] == v[i - 1]) : (i > start && v[i] == v[i - 1])) continue;
            path.add(v[i]);
            walk(v, i + 1, overSkip, path, out);
            path.remove(path.size() - 1);
        }
    }

    static List<List<Integer>> solve(int[] nums, boolean overSkip) {
        int[] v = nums.clone();
        Arrays.sort(v);
        List<List<Integer>> out = new ArrayList<>();
        walk(v, 0, overSkip, new ArrayList<>(), out);
        return out;
    }

    static List<List<Integer>> oracle(int[] nums) {
        int[] v = nums.clone();
        Arrays.sort(v);
        int n = v.length;
        Set<List<Integer>> seen = new HashSet<>();
        for (int m = 0; m < (1 << n); m++) {
            List<Integer> l = new ArrayList<>();
            for (int i = 0; i < n; i++) if ((m >> i & 1) == 1) l.add(v[i]);
            boolean rep = false;
            for (int j = 1; j < l.size(); j++) if (l.get(j).equals(l.get(j - 1))) rep = true;
            if (rep) seen.add(l);
        }
        List<List<Integer>> out = new ArrayList<>(seen);
        out.sort((a, b) -> {
            for (int i = 0; i < Math.min(a.size(), b.size()); i++) if (!a.get(i).equals(b.get(i))) return a.get(i) - b.get(i);
            return a.size() - b.size();
        });
        return out;
    }

    public static void main(String[] args) {
        if (!solve(new int[] {1, 2, 2}, false).equals(List.of(List.of(1, 2, 2), List.of(2, 2)))) throw new AssertionError("example 1");
        if (!solve(new int[] {5, 5, 5}, false).equals(List.of(List.of(5, 5), List.of(5, 5, 5)))) throw new AssertionError("example 2");
        if (!solve(new int[] {1, 2, 2}, true).isEmpty()) throw new AssertionError("skipping every repeated value loses every pair");
        if (Integer.valueOf(1000) == Integer.valueOf(1000)) throw new AssertionError("boxed values beyond the cache are different objects");
        if (Integer.valueOf(100) != Integer.valueOf(100)) throw new AssertionError("small boxed values are cached");
        Random rnd = new Random(19703);
        for (int t = 0; t < 3000; t++) {
            int n = rnd.nextInt(9);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = 1 + rnd.nextInt(4) * 333;
            if (!solve(a, false).equals(oracle(a))) throw new AssertionError("differs on " + Arrays.toString(a));
        }
    }
}
```

#### Solution: [Recognize] Combination Sum II (LeetCode 40)
<!-- id: bt-combination-sum-two -->

**Approach.** After sorting a copy, the loop starts at `start`, leaves at the first candidate larger than the remaining target, which is valid because the values are ascending and positive, skips an equal sibling with `i > start`, and recurses with `i + 1` and the reduced target. A path is stored when the target reaches zero. The harness runs a version without the sibling skip and asserts it lists a repeated combination for the second example, then compares the real search with an oracle that takes every mask of the sorted copy, filters by sum, removes repeats with a set and sorts.

**Complexity.** The nodes are bounded by the distinct partial combinations whose sum stays within the target, and each answer costs a copy.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashSet;
import java.util.List;
import java.util.Random;
import java.util.Set;

public final class CombinationSumTwo {
    static void go(int[] v, int start, int left, boolean skip, List<Integer> path, List<List<Integer>> out) {
        if (left == 0) {
            out.add(new ArrayList<>(path));
            return;
        }
        for (int i = start; i < v.length; i++) {
            if (v[i] > left) break;
            if (skip && i > start && v[i] == v[i - 1]) continue;
            path.add(v[i]);
            go(v, i + 1, left - v[i], skip, path, out);
            path.remove(path.size() - 1);
        }
    }

    static List<List<Integer>> solve(int[] c, int target, boolean skip) {
        int[] v = c.clone();
        Arrays.sort(v);
        List<List<Integer>> out = new ArrayList<>();
        go(v, 0, target, skip, new ArrayList<>(), out);
        return out;
    }

    static List<List<Integer>> oracle(int[] c, int target) {
        int[] v = c.clone();
        Arrays.sort(v);
        int n = v.length;
        Set<List<Integer>> seen = new HashSet<>();
        for (int m = 1; m < (1 << n); m++) {
            int sum = 0;
            List<Integer> l = new ArrayList<>();
            for (int i = 0; i < n; i++) if ((m >> i & 1) == 1) { l.add(v[i]); sum += v[i]; }
            if (sum == target) seen.add(l);
        }
        List<List<Integer>> out = new ArrayList<>(seen);
        out.sort((a, b) -> {
            for (int i = 0; i < Math.min(a.size(), b.size()); i++) if (!a.get(i).equals(b.get(i))) return a.get(i) - b.get(i);
            return a.size() - b.size();
        });
        return out;
    }

    public static void main(String[] args) {
        List<List<Integer>> one = List.of(List.of(1, 1, 4), List.of(1, 2, 3), List.of(2, 4), List.of(3, 3));
        if (!solve(new int[] {3, 1, 2, 3, 1, 4}, 6, true).equals(one)) throw new AssertionError("example 1");
        if (!solve(new int[] {2, 2, 2}, 4, true).equals(List.of(List.of(2, 2)))) throw new AssertionError("example 2");
        if (solve(new int[] {2, 2, 2}, 4, false).size() != 3) throw new AssertionError("without the skip the pair is listed three times");
        Random rnd = new Random(19704);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(10);
            int[] c = new int[n];
            for (int i = 0; i < n; i++) c[i] = 1 + rnd.nextInt(6);
            int target = 1 + rnd.nextInt(30);
            if (!solve(c, target, true).equals(oracle(c, target))) throw new AssertionError("differs for target " + target);
        }
    }
}
```
