<!-- solutions-for: 04-permutations -->
### Solutions For Listing Every Ordering

#### Solution: [Build] Permute Three Distinct Values (Author exercise)
<!-- id: bt-permute-three -->

**Approach.**
The call at depth `d` fills output position `d`. It loops over the indices 0 to 2 and skips every index whose mark is true, because an earlier position holds that index. For a free index, it sets the mark, adds the value and calls itself. After the call it removes the last value and clears the same mark. At depth 3 the path holds one ordering, and the call stores a copy. The invariant is that at depth `d`, exactly `d` marks are true and they belong to the indices on the path.

**Complexity.**
- **Time** is O(1) for exactly three values, with 15 choices and 6 copies; in general it is O(n * n!).
- **Space** is O(1) for three values, and O(n) in general besides the output.

```java run
import java.util.*;

public final class PermuteThree {
    /**
     * Returns the six orderings of three distinct values.
     * Time: O(1) for three values. Space: O(1) besides the output.
     * Invariant: at depth d, d marks are true, one for each index on the path.
     */
    static List<List<Integer>> orderings(int[] nums) {
        List<List<Integer>> out = new ArrayList<>();
        go(nums, new boolean[3], new ArrayList<>(), out);
        return out;
    }

    private static void go(int[] nums, boolean[] used, List<Integer> path, List<List<Integer>> out) {
        if (path.size() == 3) { out.add(new ArrayList<>(path)); return; }   // full path: store a copy
        for (int i = 0; i < 3; i++) {                        // any index may fill this position
            if (used[i]) continue;                           // an earlier position holds this index
            used[i] = true; path.add(nums[i]);               // choose: mark the index and add its value
            go(nums, used, path, out);                       // explore the later positions
            path.remove(path.size() - 1); used[i] = false;   // restore both pieces of state
        }
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!orderings(new int[] {1, 2, 3}).equals(List.of(List.of(1, 2, 3), List.of(1, 3, 2), List.of(2, 1, 3), List.of(2, 3, 1), List.of(3, 1, 2), List.of(3, 2, 1)))) throw new AssertionError("ex1");
        if (!orderings(new int[] {7, -1, 4}).equals(List.of(List.of(7, -1, 4), List.of(7, 4, -1), List.of(-1, 7, 4), List.of(-1, 4, 7), List.of(4, 7, -1), List.of(4, -1, 7)))) throw new AssertionError("ex2");
        // Random triples must match nested loops over the indices.
        Random rnd = new Random(1931);
        for (int t = 0; t < 200; t++) {
            int[] a = new int[3];
            Set<Integer> s = new LinkedHashSet<>();
            while (s.size() < 3) s.add(rnd.nextInt(201) - 100);
            int p = 0; for (int v : s) a[p++] = v;
            List<List<Integer>> want = new ArrayList<>();
            for (int x = 0; x < 3; x++) for (int y = 0; y < 3; y++) for (int z = 0; z < 3; z++)
                if (x != y && y != z && x != z) want.add(List.of(a[x], a[y], a[z]));
            if (!orderings(a).equals(want)) throw new AssertionError("random " + t);
        }
        System.out.println("ok");
    }
}
```

#### Solution: [Vary] Permutations (LeetCode 46)
<!-- id: bt-permutations-used-array -->

**Approach.**
The search of the previous solution works for any length when the base case uses `nums.length`. A call fills position `depth`, loops over all indices from low to high and skips marked indices. After each branch the call removes the last path entry and clears the mark. An empty array reaches the base case at the root, so the result holds one empty list. The swap version is a second correct method, and the code below checks that it lists the same set of orderings.

**Complexity.**
- **Time** is O(n * n!), because the tree has about e * n! calls and each of the n! leaves copies n values.
- **Space** is O(n) for the path, the marks and the stack, plus the output.

```java run
import java.util.*;

public final class PermutationsUsedArray {
    /**
     * Returns all orderings of distinct values, trying indices from low to high at each depth.
     * Time: O(n * n!). Space: O(n) besides the output.
     * Invariant: the path holds depth values, and used marks exactly their indices.
     */
    static List<List<Integer>> permute(int[] nums) {
        List<List<Integer>> out = new ArrayList<>();
        go(nums, new boolean[nums.length], new ArrayList<>(), out);
        return out;
    }

    private static void go(int[] nums, boolean[] used, List<Integer> path, List<List<Integer>> out) {
        if (path.size() == nums.length) { out.add(new ArrayList<>(path)); return; }   // all positions filled
        for (int i = 0; i < nums.length; i++) {              // low to high gives a fixed order
            if (used[i]) continue;                           // skip indices on the path
            used[i] = true; path.add(nums[i]);               // choose
            go(nums, used, path, out);                       // explore
            path.remove(path.size() - 1); used[i] = false;   // undo both pieces of state
        }
    }

    /** The in-place swap version, used here only as a second method for comparison. */
    static void swapGo(int[] a, int d, List<List<Integer>> out) {
        if (d == a.length) { List<Integer> l = new ArrayList<>(); for (int v : a) l.add(v); out.add(l); return; }
        for (int i = d; i < a.length; i++) {
            int t = a[d]; a[d] = a[i]; a[i] = t;             // place a[i] at position d
            swapGo(a, d + 1, out);
            t = a[d]; a[d] = a[i]; a[i] = t;                 // swap back to restore the array
        }
    }

    static long factorial(int n) { return n <= 1 ? 1 : n * factorial(n - 1); }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!permute(new int[] {0, 1}).equals(List.of(List.of(0, 1), List.of(1, 0)))) throw new AssertionError("ex1");
        if (!permute(new int[] {}).equals(List.of(List.of()))) throw new AssertionError("ex2");
        // Random inputs: count, uniqueness, first and last ordering, and agreement with the swap version.
        Random rnd = new Random(1932);
        for (int t = 0; t < 100; t++) {
            int n = rnd.nextInt(7);
            Set<Integer> s = new LinkedHashSet<>();
            while (s.size() < n) s.add(rnd.nextInt(21) - 10);
            int[] a = s.stream().mapToInt(Integer::intValue).toArray();
            int[] copy = a.clone();
            List<List<Integer>> got = permute(a);
            if (got.size() != factorial(n)) throw new AssertionError("count " + t);
            if (new HashSet<>(got).size() != got.size()) throw new AssertionError("repeat " + t);
            if (n > 0) {
                List<Integer> rev = new ArrayList<>(); for (int i = n - 1; i >= 0; i--) rev.add(a[i]);
                List<Integer> fwd = new ArrayList<>(); for (int v : a) fwd.add(v);
                if (!got.get(0).equals(fwd) || !got.get(got.size() - 1).equals(rev)) throw new AssertionError("ends " + t);
            }
            List<List<Integer>> sw = new ArrayList<>(); swapGo(a.clone(), 0, sw);
            if (!new HashSet<>(sw).equals(new HashSet<>(got))) throw new AssertionError("swap " + t);
            if (!Arrays.equals(a, copy)) throw new AssertionError("mutation " + t);
        }
        System.out.println("ok");
    }
}
```

#### Solution: [Boundary] Restore Used State (Author exercise)
<!-- id: bt-restore-used-state -->

**Approach.**
The search stops at depth `k`, when the path holds `k` values and some indices are still free. Here a missing mark restoration shows up at once, because the unused indices of one branch are the free choices of its sibling. Each call tries every unmarked index, sets its mark, adds its value and calls itself. After the return it removes the last entry and clears the same mark. For `k = 0`, the root call already has depth 0 and stores the empty list. For `k` above the length, the loop runs out of free indices before the depth reaches `k`, and the result stays empty.

**Complexity.**
- **Time** is O(k * n!/(n-k)!), because the tree has about n!/(n-k)! leaves and each copies k values.
- **Space** is O(n) for the marks, the path and the stack, plus the output.

```java run
import java.util.*;

public final class RestoreUsedState {
    /**
     * Returns every list of k values from different indices, low to high at each depth.
     * Time: O(k * n!/(n-k)!). Space: O(n) besides the output.
     * Invariant: at depth d, the marks are true exactly for the d indices on the path.
     */
    static List<List<Integer>> arrange(int[] nums, int k) {
        List<List<Integer>> out = new ArrayList<>();
        go(nums, k, new boolean[nums.length], new ArrayList<>(), out);
        return out;
    }

    private static void go(int[] nums, int k, boolean[] used, List<Integer> path, List<List<Integer>> out) {
        if (path.size() == k) { out.add(new ArrayList<>(path)); return; }   // stop at depth k, before all indices are used
        for (int i = 0; i < nums.length; i++) {
            if (used[i]) continue;                           // skip indices on the path
            used[i] = true; path.add(nums[i]);               // choose
            go(nums, k, used, path, out);                    // explore
            path.remove(path.size() - 1); used[i] = false;   // clear exactly the mark that this call set
        }
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!arrange(new int[] {1, 2, 3}, 2).equals(List.of(List.of(1, 2), List.of(1, 3), List.of(2, 1), List.of(2, 3), List.of(3, 1), List.of(3, 2)))) throw new AssertionError("ex1");
        if (!arrange(new int[] {5}, 0).equals(List.of(List.of()))) throw new AssertionError("ex2");
        if (!arrange(new int[] {5}, 2).isEmpty()) throw new AssertionError("k above length");
        if (!arrange(new int[] {}, 0).equals(List.of(List.of()))) throw new AssertionError("empty input");
        // Random inputs must match an iterative enumeration of index tuples in lexicographic order.
        Random rnd = new Random(1933);
        for (int t = 0; t < 200; t++) {
            int n = rnd.nextInt(6);
            Set<Integer> s = new LinkedHashSet<>();
            while (s.size() < n) s.add(rnd.nextInt(21) - 10);
            int[] a = s.stream().mapToInt(Integer::intValue).toArray();
            int k = rnd.nextInt(5);
            List<List<Integer>> want = new ArrayList<>();
            int total = 1; for (int i = 0; i < k; i++) total *= Math.max(n, 1);
            for (int code = 0; code < total && n > 0; code++) {
                int c = code; int[] ix = new int[k];
                for (int i = k - 1; i >= 0; i--) { ix[i] = c % n; c /= n; }
                Set<Integer> distinct = new HashSet<>(); List<Integer> tuple = new ArrayList<>();
                for (int i : ix) { distinct.add(i); tuple.add(a[i]); }
                if (distinct.size() == k) want.add(tuple);
            }
            if (n == 0 && k == 0) want.add(new ArrayList<>());
            if (!arrange(a, k).equals(want)) throw new AssertionError("random " + t);
        }
        System.out.println("ok");
    }
}
```

#### Solution: [Recognize] Permutations II (LeetCode 47)
<!-- id: bt-permutations-equal-values -->

**Approach.**
The search of the previous solutions lists an ordering once for every way to assign equal values to indices, which repeats results. Two equal values at one depth build the same subtree, so each call keeps a `HashSet<Integer>` named `tried` for the values it has already placed at its own depth. A call skips an index whose value is in `tried`. The set belongs to one call, so equal values still fill different depths of one path, and `[1, 1, 2]` remains reachable. Each call tries the first free index of every value, so the result lists each ordering at the first place where the plain search reaches it.

**Complexity.**
- **Time** is O(n * m), where `m` is the number of different orderings, because each call adds a set check per index and each leaf copies n values.
- **Space** is O(n) for the marks, the path, the stack and the sets, plus the output.

```java run
import java.util.*;

public final class PermutationsEqualValues {
    /**
     * Returns every different ordering of nums, first-reached order of the index search.
     * Time: O(n * m) for m different orderings. Space: O(n) besides the output.
     * Invariant: within one call, each value fills the position at most once.
     */
    static List<List<Integer>> unique(int[] nums) {
        List<List<Integer>> out = new ArrayList<>();
        go(nums, new boolean[nums.length], new ArrayList<>(), out);
        return out;
    }

    private static void go(int[] nums, boolean[] used, List<Integer> path, List<List<Integer>> out) {
        if (path.size() == nums.length) { out.add(new ArrayList<>(path)); return; }
        Set<Integer> tried = new HashSet<>();                // values this call has already placed at this depth
        for (int i = 0; i < nums.length; i++) {
            if (used[i] || !tried.add(nums[i])) continue;    // add returns false for a value that was tried before
            used[i] = true; path.add(nums[i]);               // choose
            go(nums, used, path, out);                       // explore
            path.remove(path.size() - 1); used[i] = false;   // undo both pieces of state
        }
    }

    private static void plain(int[] a, boolean[] used, List<Integer> path, List<List<Integer>> out) {
        if (path.size() == a.length) { out.add(new ArrayList<>(path)); return; }
        for (int i = 0; i < a.length; i++) {
            if (used[i]) continue;
            used[i] = true; path.add(a[i]);
            plain(a, used, path, out);
            path.remove(path.size() - 1); used[i] = false;
        }
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!unique(new int[] {1, 1, 2}).equals(List.of(List.of(1, 1, 2), List.of(1, 2, 1), List.of(2, 1, 1)))) throw new AssertionError("ex1");
        if (!unique(new int[] {2, 2}).equals(List.of(List.of(2, 2)))) throw new AssertionError("ex2");
        if (!unique(new int[] {}).equals(List.of(List.of()))) throw new AssertionError("empty");
        // The Java claim: Set.add returns false when the value is already present.
        Set<Integer> probe = new HashSet<>(); if (!probe.add(4) || probe.add(4)) throw new AssertionError("add result");
        // Random inputs must match the plain search with later repeats dropped.
        Random rnd = new Random(1934);
        for (int t = 0; t < 300; t++) {
            int[] a = new int[rnd.nextInt(7)];
            for (int i = 0; i < a.length; i++) a[i] = rnd.nextInt(4) - 2;
            int[] copy = a.clone();
            List<List<Integer>> all = new ArrayList<>(); plain(a, new boolean[a.length], new ArrayList<>(), all);
            List<List<Integer>> want = new ArrayList<>(new LinkedHashSet<>(all));
            if (!unique(a).equals(want)) throw new AssertionError("random " + t);
            if (!Arrays.equals(a, copy)) throw new AssertionError("mutation " + t);
        }
        System.out.println("ok");
    }
}
```
