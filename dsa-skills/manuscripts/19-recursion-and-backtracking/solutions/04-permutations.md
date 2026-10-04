<!-- solutions-for: 04-permutations -->
### Permutations

#### Solution: [Build] Permute Three Distinct Values (Author exercise)
<!-- id: bt-permute-three -->

**Approach.** Each call fills the chair equal to the current path length, offers the indexes 0 to n - 1, skips the marked ones, and marks, appends, recurses, removes and unmarks the same index. The arrangement is stored when the path is full. The harness also shows why the code stage copies with a loop: `Arrays.asList` on an `int[]` yields a one-element list. The oracle is the odometer of the naive stage, counting through all n^n index sequences and keeping those without a repeat, which visits them in exactly the order the search finds them, so the two lists must be equal and not merely the same set.

**Complexity.** There are n! leaves and O(n) copying per leaf, so O(n * n!) time, and a stack of n frames.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

public final class PermuteThree {
    static void place(int[] g, boolean[] used, List<Integer> path, List<List<Integer>> out) {
        if (path.size() == g.length) {
            out.add(new ArrayList<>(path));
            return;
        }
        for (int i = 0; i < g.length; i++) {
            if (used[i]) continue;
            used[i] = true;
            path.add(g[i]);
            place(g, used, path, out);
            path.remove(path.size() - 1);
            used[i] = false;
        }
    }

    static List<List<Integer>> seatings(int[] g) {
        List<List<Integer>> out = new ArrayList<>();
        boolean[] used = new boolean[g.length];
        place(g, used, new ArrayList<>(), out);
        for (boolean u : used) if (u) throw new AssertionError("marks must be clear on exit");
        return out;
    }

    static List<List<Integer>> oracle(int[] g) {
        int n = g.length;
        List<List<Integer>> kept = new ArrayList<>();
        int[] pick = new int[n];
        while (true) {
            boolean[] seen = new boolean[n];
            boolean ok = true;
            for (int c = 0; c < n && ok; c++) {
                if (seen[pick[c]]) ok = false; else seen[pick[c]] = true;
            }
            if (ok) {
                List<Integer> s = new ArrayList<>();
                for (int c = 0; c < n; c++) s.add(g[pick[c]]);
                kept.add(s);
            }
            int c = n - 1;
            while (c >= 0 && pick[c] == n - 1) pick[c--] = 0;
            if (c < 0) break;
            pick[c]++;
        }
        return kept;
    }

    public static void main(String[] args) {
        List<List<Integer>> one = List.of(List.of(1, 2, 3), List.of(1, 3, 2), List.of(2, 1, 3), List.of(2, 3, 1), List.of(3, 1, 2), List.of(3, 2, 1));
        if (!seatings(new int[] {1, 2, 3}).equals(one)) throw new AssertionError("example 1");
        List<List<Integer>> two = List.of(List.of(9, -4, 0), List.of(9, 0, -4), List.of(-4, 9, 0), List.of(-4, 0, 9), List.of(0, 9, -4), List.of(0, -4, 9));
        if (!seatings(new int[] {9, -4, 0}).equals(two)) throw new AssertionError("example 2");
        if (Arrays.asList(new int[] {1, 2}).size() != 1) throw new AssertionError("Arrays.asList on an int[] holds one element");
        Random rnd = new Random(19401);
        for (int t = 0; t < 1500; t++) {
            int n = rnd.nextInt(6);
            int[] g = new int[n];
            for (int i = 0; i < n; i++) g[i] = i * 7 - 20 + rnd.nextInt(5);
            if (!seatings(g).equals(oracle(g))) throw new AssertionError("differs on length " + n);
        }
    }
}
```

#### Solution: [Vary] Permutations By Swapping (LeetCode 46)
<!-- id: bt-permute-swaps -->

**Approach.** The call for `pos` loops `j` from `pos` to the end, swaps `pos` and `j`, recurses on `pos + 1`, and swaps the same pair back, so the prefix of the array is the path and the suffix is the unused pile. A copy of the array is stored at `pos == n`. The order of results differs from the marks version, so the first two examples are checked literally. The harness then compares the swap results, as sorted lists, with the marks version on random inputs, checks that there are n! results with no repeats, and checks that the array is back in its original order afterwards. A variant that forgets the second swap is run and must produce a wrong answer for three values.

**Complexity.** The leaves number n!, each costing an O(n) copy, so the time is O(n * n!) and the stack holds n frames.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashSet;
import java.util.List;
import java.util.Random;
import java.util.Set;

public final class PermuteSwaps {
    static void go(int[] a, int pos, boolean swapBack, List<List<Integer>> out) {
        if (pos == a.length) {
            List<Integer> copy = new ArrayList<>();
            for (int v : a) copy.add(v);
            out.add(copy);
            return;
        }
        for (int j = pos; j < a.length; j++) {
            int t = a[pos]; a[pos] = a[j]; a[j] = t;
            go(a, pos + 1, swapBack, out);
            if (swapBack) { t = a[pos]; a[pos] = a[j]; a[j] = t; }
        }
    }

    static List<List<Integer>> arrangements(int[] nums, boolean swapBack) {
        List<List<Integer>> out = new ArrayList<>();
        go(nums, 0, swapBack, out);
        return out;
    }

    static void marks(int[] g, boolean[] used, List<Integer> path, List<List<Integer>> out) {
        if (path.size() == g.length) { out.add(new ArrayList<>(path)); return; }
        for (int i = 0; i < g.length; i++) {
            if (used[i]) continue;
            used[i] = true; path.add(g[i]);
            marks(g, used, path, out);
            path.remove(path.size() - 1); used[i] = false;
        }
    }

    static int cmp(List<Integer> a, List<Integer> b) {
        for (int i = 0; i < Math.min(a.size(), b.size()); i++) if (!a.get(i).equals(b.get(i))) return a.get(i) - b.get(i);
        return a.size() - b.size();
    }

    public static void main(String[] args) {
        List<List<Integer>> one = List.of(List.of(1, 2, 3), List.of(1, 3, 2), List.of(2, 1, 3), List.of(2, 3, 1), List.of(3, 2, 1), List.of(3, 1, 2));
        if (!arrangements(new int[] {1, 2, 3}, true).equals(one)) throw new AssertionError("example 1");
        if (!arrangements(new int[] {8}, true).equals(List.of(List.of(8)))) throw new AssertionError("example 2");
        if (!arrangements(new int[0], true).equals(List.of(List.of()))) throw new AssertionError("empty input gives one empty arrangement");
        List<List<Integer>> wrong = arrangements(new int[] {1, 2, 3}, false);
        Set<List<Integer>> distinctWrong = new HashSet<>(wrong);
        if (distinctWrong.size() == 6) throw new AssertionError("without the second swap the search must lose arrangements");
        int[] fact = {1, 1, 2, 6, 24, 120, 720, 5040, 40320};
        Random rnd = new Random(19402);
        for (int t = 0; t < 1500; t++) {
            int n = rnd.nextInt(7);
            int[] nums = new int[n];
            for (int i = 0; i < n; i++) nums[i] = i * 5 - 20 + rnd.nextInt(3);
            int[] before = nums.clone();
            List<List<Integer>> got = arrangements(nums, true);
            if (!Arrays.equals(nums, before)) throw new AssertionError("array must be restored");
            if (got.size() != fact[n] || new HashSet<>(got).size() != fact[n]) throw new AssertionError("count or repeats at n=" + n);
            List<List<Integer>> ref = new ArrayList<>();
            marks(nums, new boolean[n], new ArrayList<>(), ref);
            got.sort(PermuteSwaps::cmp);
            ref.sort(PermuteSwaps::cmp);
            if (!got.equals(ref)) throw new AssertionError("different family at n=" + n);
        }
    }
}
```

#### Solution: [Boundary] Restore Used State (Author exercise)
<!-- id: bt-restore-used -->

**Approach.** The search is the used-marks search with the stopping depth set to `r`. When `r` is 0 the path is already full at the first call, which returns one empty selection, and when `r` exceeds the number of values the path can never reach `r` and nothing is stored. Every call clears the index it set, so the marks are all false on exit, which the harness asserts after each run. A careless variant clears the flag at the current depth rather than at the index it set, and the harness shows that it returns a different answer for three values and `r = 2`. The oracle is an odometer of r digits over the values that keeps the sequences with no repeated index.

**Complexity.** There are n! / (n - r)! selections, each an O(r) copy, and the stack is r frames deep.

```java run
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public final class RestoreUsed {
    static void go(int[] v, int r, boolean[] used, List<Integer> path, boolean careless, List<List<Integer>> out) {
        if (path.size() == r) {
            out.add(new ArrayList<>(path));
            return;
        }
        for (int i = 0; i < v.length; i++) {
            if (used[i]) continue;
            used[i] = true;
            path.add(v[i]);
            go(v, r, used, path, careless, out);
            path.remove(path.size() - 1);
            if (careless) used[path.size()] = false; else used[i] = false;
        }
    }

    static List<List<Integer>> select(int[] v, int r, boolean careless, boolean[] usedOut) {
        List<List<Integer>> out = new ArrayList<>();
        go(v, r, usedOut, new ArrayList<>(), careless, out);
        return out;
    }

    static List<List<Integer>> oracle(int[] v, int r) {
        int n = v.length;
        List<List<Integer>> out = new ArrayList<>();
        int[] pick = new int[r];
        if (r > 0 && n == 0) return out;
        while (true) {
            boolean ok = true;
            for (int a = 0; a < r && ok; a++) for (int b = a + 1; b < r; b++) if (pick[a] == pick[b]) { ok = false; break; }
            if (ok) {
                List<Integer> s = new ArrayList<>();
                for (int a = 0; a < r; a++) s.add(v[pick[a]]);
                out.add(s);
            }
            int c = r - 1;
            while (c >= 0 && pick[c] == n - 1) pick[c--] = 0;
            if (c < 0) break;
            pick[c]++;
        }
        return out;
    }

    public static void main(String[] args) {
        List<List<Integer>> one = List.of(List.of(1, 2), List.of(1, 3), List.of(2, 1), List.of(2, 3), List.of(3, 1), List.of(3, 2));
        if (!select(new int[] {1, 2, 3}, 2, false, new boolean[3]).equals(one)) throw new AssertionError("example 1");
        if (!select(new int[] {7, 8}, 3, false, new boolean[2]).isEmpty()) throw new AssertionError("example 2");
        List<List<Integer>> zero = select(new int[] {7, 8}, 0, false, new boolean[2]);
        if (zero.size() != 1 || !zero.get(0).isEmpty()) throw new AssertionError("r = 0 gives one empty selection");
        if (select(new int[] {1, 2, 3}, 2, true, new boolean[3]).equals(one)) throw new AssertionError("clearing the wrong flag must change the answer");
        Random rnd = new Random(19403);
        for (int t = 0; t < 1500; t++) {
            int n = rnd.nextInt(5);
            int r = rnd.nextInt(6);
            int[] v = new int[n];
            for (int i = 0; i < n; i++) v[i] = i * 6 - 10 + rnd.nextInt(4);
            boolean[] used = new boolean[n];
            List<List<Integer>> got = select(v, r, false, used);
            for (boolean u : used) if (u) throw new AssertionError("a mark leaked at n=" + n + ", r=" + r);
            if (!got.equals(oracle(v, r))) throw new AssertionError("differs at n=" + n + ", r=" + r);
        }
    }
}
```

#### Solution: [Recognize] Permutations With Equal Values (LeetCode 47)
<!-- id: bt-permutations-equal -->

**Approach.** A sorted copy puts equal values side by side. At each depth an index is skipped when it is marked, or when its value equals that of the previous index and the previous index is not marked, which means the previous equal value was offered at this same depth and already explored. When the previous equal index is marked it is sitting on the path at a shallower depth, so the current one is a second copy and must stay available. The harness runs an over-eager rule that skips whenever the value equals the previous value, and asserts it loses the arrangement `[1, 1, 2]`. The oracle permutes all indexes, removes repeats with a set, and sorts lexicographically, which is arrival order for an ascending offer.

**Complexity.** At most n! leaves at O(n) per copy, so O(n * n!) in the worst case of distinct values, and fewer when values repeat.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashSet;
import java.util.List;
import java.util.Random;
import java.util.Set;

public final class PermutationsEqual {
    static void go(int[] a, boolean[] used, List<Integer> path, boolean eager, List<List<Integer>> out) {
        if (path.size() == a.length) {
            out.add(new ArrayList<>(path));
            return;
        }
        for (int i = 0; i < a.length; i++) {
            if (used[i]) continue;
            if (i > 0 && a[i] == a[i - 1] && (eager || !used[i - 1])) continue;
            used[i] = true;
            path.add(a[i]);
            go(a, used, path, eager, out);
            path.remove(path.size() - 1);
            used[i] = false;
        }
    }

    static List<List<Integer>> distinct(int[] nums, boolean eager) {
        int[] a = nums.clone();
        Arrays.sort(a);
        List<List<Integer>> out = new ArrayList<>();
        go(a, new boolean[a.length], new ArrayList<>(), eager, out);
        return out;
    }

    static void all(int[] a, boolean[] used, List<Integer> path, Set<List<Integer>> out) {
        if (path.size() == a.length) { out.add(new ArrayList<>(path)); return; }
        for (int i = 0; i < a.length; i++) {
            if (used[i]) continue;
            used[i] = true; path.add(a[i]);
            all(a, used, path, out);
            path.remove(path.size() - 1); used[i] = false;
        }
    }

    static List<List<Integer>> oracle(int[] nums) {
        Set<List<Integer>> seen = new HashSet<>();
        all(nums, new boolean[nums.length], new ArrayList<>(), seen);
        List<List<Integer>> out = new ArrayList<>(seen);
        out.sort((x, y) -> {
            for (int i = 0; i < x.size(); i++) if (!x.get(i).equals(y.get(i))) return x.get(i) - y.get(i);
            return 0;
        });
        return out;
    }

    public static void main(String[] args) {
        if (!distinct(new int[] {1, 1, 2}, false).equals(List.of(List.of(1, 1, 2), List.of(1, 2, 1), List.of(2, 1, 1)))) throw new AssertionError("example 1");
        List<List<Integer>> two = List.of(List.of(1, 2, 2, 2), List.of(2, 1, 2, 2), List.of(2, 2, 1, 2), List.of(2, 2, 2, 1));
        if (!distinct(new int[] {2, 2, 1, 2}, false).equals(two)) throw new AssertionError("example 2");
        if (distinct(new int[] {1, 1, 2}, true).contains(List.of(1, 1, 2))) throw new AssertionError("the eager rule must lose [1, 1, 2]");
        if (!distinct(new int[0], false).equals(List.of(List.of()))) throw new AssertionError("empty input");
        Random rnd = new Random(19404);
        for (int t = 0; t < 2000; t++) {
            int n = rnd.nextInt(7);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(4) - 1;
            if (!distinct(a, false).equals(oracle(a))) throw new AssertionError("differs on " + Arrays.toString(a));
        }
    }
}
```
