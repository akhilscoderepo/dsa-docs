<!-- solutions-for: 07-duplicate-control -->
### Solutions For Skipping Equal Values

#### Solution: [Build] Equal Sibling Choices (Author exercise)
<!-- id: bt-equal-sibling-choices -->

**Approach.**
Both runs share one search and differ in one flag. A call adds one to the counter when it begins, then loops over the indices from `start`. In the second run, the loop skips index `i` when `i > start` and `nums[i] == nums[i - 1]`. The first copy of a value in a loop starts the only subtree for that value, and the other copies would repeat it. The first run counts 2^n calls for n values. The second run counts one call for each different subset, because every call stores one different list.

**Complexity.**
- **Time** is O(2^n) for the first run and O(m * n) for the second, where `m` is the number of different subsets.
- **Space** is O(n) for the stack.

```java run
import java.util.*;

public final class EqualSiblingChoices {
    private static long calls;

    /**
     * Returns the call counts of the plain search and of the search with the same-level check.
     * Time: O(2^n). Space: O(n) stack frames.
     * Invariant: with the check, no call starts two subtrees with the same value.
     */
    static long[] counts(int[] nums) {
        calls = 0; go(0, nums, false); long plain = calls;
        calls = 0; go(0, nums, true); long skipped = calls;
        return new long[] {plain, skipped};
    }

    private static void go(int start, int[] a, boolean skip) {
        calls++;                                             // each entry counts once
        for (int i = start; i < a.length; i++) {
            if (skip && i > start && a[i] == a[i - 1]) continue;   // an equal sibling already started this subtree
            go(i + 1, a, skip);                              // the child starts one past i
        }
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!Arrays.equals(counts(new int[] {1, 2, 2}), new long[] {8, 6})) throw new AssertionError("ex1");
        if (!Arrays.equals(counts(new int[] {3, 3, 3, 3}), new long[] {16, 5})) throw new AssertionError("ex2");
        if (!Arrays.equals(counts(new int[] {}), new long[] {1, 1})) throw new AssertionError("empty");
        // Random sorted inputs: the plain count is 2^n and the skip count is the product of (count + 1).
        Random rnd = new Random(1971);
        for (int t = 0; t < 300; t++) {
            int[] a = new int[rnd.nextInt(13)];
            for (int i = 0; i < a.length; i++) a[i] = rnd.nextInt(6) - 3;
            Arrays.sort(a);
            Map<Integer, Integer> cnt = new HashMap<>();
            for (int v : a) cnt.merge(v, 1, Integer::sum);
            long want = 1; for (int c : cnt.values()) want *= c + 1;
            long[] got = counts(a);
            if (got[0] != (1L << a.length) || got[1] != want) throw new AssertionError("random " + t);
        }
        System.out.println("ok");
    }
}
```

#### Solution: [Vary] Subsets II (LeetCode 90)
<!-- id: bt-subsets-two-skip -->

**Approach.**
The method sorts a copy of `nums`, so equal values sit side by side and the caller's array keeps its order. The search stores the path when a call begins, then loops from `start`. The loop skips an index with `i > start` and `a[i] == a[i - 1]`. In that case, index `i - 1` was a choice of the same loop and has started the same subtree. When `i == start`, the left neighbour sits on the path, so the choice is allowed. This is why a list may hold two copies of one value. The result holds each different subset once, in the order in which the calls begin.

**Complexity.**
- **Time** is O(n log n + n * m), where `m` is the number of different subsets, because each call stores one list of up to n values.
- **Space** is O(n) for the copy, the path and the stack, plus the output.

```java run
import java.util.*;

public final class SubsetsTwoSkip {
    /**
     * Returns every different subset of nums, in call-entry order over the sorted copy.
     * Time: O(n log n + n * m). Space: O(n) besides the output.
     * Invariant: no call starts two subtrees with the same value, and a path may repeat a value across depths.
     */
    static List<List<Integer>> subsetsWithDup(int[] nums) {
        int[] a = nums.clone();                              // sort a copy to keep the caller's order
        Arrays.sort(a);
        List<List<Integer>> out = new ArrayList<>();
        go(0, a, new ArrayList<>(), out);
        return out;
    }

    private static void go(int start, int[] a, List<Integer> path, List<List<Integer>> out) {
        out.add(new ArrayList<>(path));                      // record on entry
        for (int i = start; i < a.length; i++) {
            if (i > start && a[i] == a[i - 1]) continue;     // same-level check: skip the equal sibling
            path.add(a[i]);                                  // choose index i
            go(i + 1, a, path, out);                         // explore the later indices
            path.remove(path.size() - 1);                    // undo the choice
        }
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!subsetsWithDup(new int[] {4, 4, 1, 4}).equals(List.of(List.of(), List.of(1), List.of(1, 4), List.of(1, 4, 4), List.of(1, 4, 4, 4), List.of(4), List.of(4, 4), List.of(4, 4, 4)))) throw new AssertionError("ex1");
        if (!subsetsWithDup(new int[] {0}).equals(List.of(List.of(), List.of(0)))) throw new AssertionError("ex2");
        // Random inputs must match the set of sorted mask subsets, with no repeat in the output.
        Random rnd = new Random(1972);
        for (int t = 0; t < 300; t++) {
            int[] a = new int[rnd.nextInt(10)];
            for (int i = 0; i < a.length; i++) a[i] = rnd.nextInt(5) - 2;
            int[] copy = a.clone();
            int[] s = a.clone(); Arrays.sort(s);
            Set<List<Integer>> want = new HashSet<>();
            for (int mask = 0; mask < (1 << s.length); mask++) {
                List<Integer> l = new ArrayList<>();
                for (int i = 0; i < s.length; i++) if ((mask >> i & 1) == 1) l.add(s[i]);
                want.add(l);
            }
            List<List<Integer>> got = subsetsWithDup(a);
            if (got.size() != want.size() || !new HashSet<>(got).equals(want)) throw new AssertionError("random " + t);
            if (!Arrays.equals(a, copy)) throw new AssertionError("mutation " + t);
        }
        // The Java claim: == on boxed values compares references, so equal Integer objects above 127 can differ.
        Integer p = Integer.valueOf(1000), q = Integer.valueOf(1000);
        if (p == q || !p.equals(q)) throw new AssertionError("boxed comparison");
        System.out.println("ok");
    }
}
```

#### Solution: [Boundary] Equal Values At Different Depths (Author exercise)
<!-- id: bt-equal-values-different-depths -->

**Approach.**
The search is the sorted search with the same-level check, and it stores a path when the path holds exactly `m` copies of `v`. The skip compares `i` with `start`, so the second copy of `v` can still enter a path at the next depth. If the check compared `i` with 0, a call for the path `[2]` would skip the second 2, and `[2, 2]` would never appear. The method counts copies of `v` with a running counter, and the undo step lowers the counter when it removes a copy. Because the filter looks only at the count, every stored list that holds two or more copies of `v` depends on the correct comparison.

**Complexity.**
- **Time** is O(n * m), where `m` is the number of different subsets, because each call may copy a path of up to n values.
- **Space** is O(n) for the path and the stack, plus the output.

```java run
import java.util.*;

public final class EqualValuesDifferentDepths {
    /**
     * Returns every different subset of sorted nums that holds v exactly m times.
     * Time: O(n * m). Space: O(n) besides the output.
     * Invariant: copies equals the number of entries of the path that are equal to v.
     */
    static List<List<Integer>> withCopies(int[] nums, int v, int m) {
        List<List<Integer>> out = new ArrayList<>();
        go(0, nums, v, m, 0, new ArrayList<>(), out, true);
        return out;
    }

    static List<List<Integer>> wrongCheck(int[] nums, int v, int m) {
        List<List<Integer>> out = new ArrayList<>();
        go(0, nums, v, m, 0, new ArrayList<>(), out, false);
        return out;
    }

    private static void go(int start, int[] a, int v, int m, int copies, List<Integer> path, List<List<Integer>> out, boolean right) {
        if (copies == m) out.add(new ArrayList<>(path));     // the filter looks only at the count of v
        for (int i = start; i < a.length; i++) {
            int limit = right ? start : 0;                   // the right check compares with start, the wrong one with 0
            if (i > limit && a[i] == a[i - 1]) continue;     // skip the equal sibling
            path.add(a[i]);                                  // choose index i
            go(i + 1, a, v, m, copies + (a[i] == v ? 1 : 0), path, out, right);
            path.remove(path.size() - 1);                    // undo the choice
        }
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!withCopies(new int[] {2, 2, 3}, 2, 2).equals(List.of(List.of(2, 2), List.of(2, 2, 3)))) throw new AssertionError("ex1");
        if (!withCopies(new int[] {1, 1}, 1, 0).equals(List.of(List.of()))) throw new AssertionError("ex2");
        if (!withCopies(new int[] {1}, 7, 1).isEmpty()) throw new AssertionError("absent value");
        // The wrong check loses the lists with two copies.
        if (!wrongCheck(new int[] {2, 2, 3}, 2, 2).isEmpty()) throw new AssertionError("wrong check should lose them");
        // Random sorted inputs must match a mask enumeration filtered by the count of v.
        Random rnd = new Random(1973);
        for (int t = 0; t < 300; t++) {
            int[] a = new int[rnd.nextInt(10)];
            for (int i = 0; i < a.length; i++) a[i] = rnd.nextInt(4) - 1;
            Arrays.sort(a);
            int v = rnd.nextInt(5) - 2, m = rnd.nextInt(4);
            Set<List<Integer>> want = new HashSet<>();
            for (int mask = 0; mask < (1 << a.length); mask++) {
                List<Integer> l = new ArrayList<>(); int c = 0;
                for (int i = 0; i < a.length; i++) if ((mask >> i & 1) == 1) { l.add(a[i]); if (a[i] == v) c++; }
                if (c == m) want.add(l);
            }
            List<List<Integer>> got = withCopies(a, v, m);
            if (got.size() != want.size() || !new HashSet<>(got).equals(want)) throw new AssertionError("random " + t);
        }
        System.out.println("ok");
    }
}
```

#### Solution: [Recognize] Combination Sum II (LeetCode 40)
<!-- id: bt-combination-sum-two -->

**Approach.**
The method sorts a copy of `candidates` and searches with a start index, a remaining target and the same-level check. A call stores a copy when the remaining target is 0. A call chooses index `i` and passes `i + 1`, so each index serves at most once. The loop skips an equal sibling with `i > start && a[i] == a[i - 1]`. It also stops at the first candidate above the remaining target. The array is sorted and all values are positive, so later candidates are larger still. This stop loses nothing. The two checks together give each different list once, and a list may still hold two copies of a value that the array holds twice.

**Complexity.**
- **Time** is O(n * m) plus O(n log n) for the sort, where `m` counts the calls that keep a nonnegative remaining target.
- **Space** is O(n) for the copy, the path and the stack, plus the output.

```java run
import java.util.*;

public final class CombinationSumTwo {
    /**
     * Returns every different list of candidates, each index used once, that adds up to target.
     * Time: O(n log n + n * m). Space: O(n) besides the output.
     * Invariant: remain is target minus the sum of the path, and no call starts two subtrees with the same value.
     */
    static List<List<Integer>> combinationSum2(int[] candidates, int target) {
        int[] a = candidates.clone();                        // sort a copy to keep the caller's order
        Arrays.sort(a);
        List<List<Integer>> out = new ArrayList<>();
        go(0, target, a, new ArrayList<>(), out);
        return out;
    }

    private static void go(int start, int remain, int[] a, List<Integer> path, List<List<Integer>> out) {
        if (remain == 0) { out.add(new ArrayList<>(path)); return; }   // exact sum: store a copy
        for (int i = start; i < a.length; i++) {
            if (a[i] > remain) break;                        // sorted and positive: later values are larger still
            if (i > start && a[i] == a[i - 1]) continue;     // same-level check
            path.add(a[i]);                                  // choose index i
            go(i + 1, remain - a[i], a, path, out);          // each index serves once
            path.remove(path.size() - 1);                    // undo the choice
        }
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!combinationSum2(new int[] {3, 1, 3, 2, 2}, 5).equals(List.of(List.of(1, 2, 2), List.of(2, 3)))) throw new AssertionError("ex1");
        if (!combinationSum2(new int[] {2, 2, 2}, 4).equals(List.of(List.of(2, 2)))) throw new AssertionError("ex2");
        // Random inputs must match the set of sorted mask subsets with the right sum.
        Random rnd = new Random(1974);
        for (int t = 0; t < 300; t++) {
            int[] a = new int[1 + rnd.nextInt(11)];
            for (int i = 0; i < a.length; i++) a[i] = 1 + rnd.nextInt(6);
            int target = 1 + rnd.nextInt(20);
            int[] copy = a.clone();
            int[] s = a.clone(); Arrays.sort(s);
            Set<List<Integer>> want = new HashSet<>();
            for (int mask = 1; mask < (1 << s.length); mask++) {
                List<Integer> l = new ArrayList<>(); int sum = 0;
                for (int i = 0; i < s.length; i++) if ((mask >> i & 1) == 1) { l.add(s[i]); sum += s[i]; }
                if (sum == target) want.add(l);
            }
            List<List<Integer>> got = combinationSum2(a, target);
            if (got.size() != want.size() || !new HashSet<>(got).equals(want)) throw new AssertionError("random " + t);
            if (!Arrays.equals(a, copy)) throw new AssertionError("mutation " + t);
        }
        System.out.println("ok");
    }
}
```
