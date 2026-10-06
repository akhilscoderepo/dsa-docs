<!-- solutions-for: 03-subsets -->
### Solutions For Listing Every Subset

#### Solution: [Build] Subsets Of Two Values (Author exercise)
<!-- id: bt-subsets-of-two-values -->

**Approach.**
A call receives a start index and a shared path. It stores a copy of the path at once, because every path of increasing indices is a complete subset. Then it loops over the indices from `start` to the end, adds the value, calls itself with the next index as the start and removes the value. For two values the root stores the empty subset and tries two children. The child for index 0 stores `[nums[0]]` and has one child of its own, and the child for index 1 stores `[nums[1]]` and has none. The path holds the values chosen at indices below `start`.

**Complexity.**
- **Time** is O(1) for two values, and in general O(n * 2^n), because each of the 2^n calls copies at most n values.
- **Space** is O(n) for the path and the stack, plus the output.

```java run
import java.util.*;

public final class SubsetsOfTwoValues {
    /**
     * Returns the subsets of nums in the order in which the calls begin.
     * Time: O(n * 2^n). Space: O(n) besides the output.
     * Invariant: the path holds values at increasing indices, all below the current start.
     */
    static List<List<Integer>> subsets(int[] nums) {
        List<List<Integer>> out = new ArrayList<>();
        go(0, nums, new ArrayList<>(), out);
        return out;
    }

    private static void go(int start, int[] nums, List<Integer> path, List<List<Integer>> out) {
        out.add(new ArrayList<>(path));                  // store a copy when the call begins
        for (int i = start; i < nums.length; i++) {      // only indices at or after start
            path.add(nums[i]);                           // choose index i
            go(i + 1, nums, path, out);                  // the child may only use later indices
            path.remove(path.size() - 1);                // undo the choice by index
        }
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!subsets(new int[] {5, 7}).equals(List.of(List.of(), List.of(5), List.of(5, 7), List.of(7)))) throw new AssertionError("ex1");
        if (!subsets(new int[] {9}).equals(List.of(List.of(), List.of(9)))) throw new AssertionError("ex2");
        if (!subsets(new int[] {}).equals(List.of(List.of()))) throw new AssertionError("empty");
        // Every length up to 2 must give 2^n subsets that match a mask enumeration.
        Random rnd = new Random(1921);
        for (int t = 0; t < 100; t++) {
            int n = rnd.nextInt(3);
            int[] a = new int[n]; for (int i = 0; i < n; i++) a[i] = i * 10 + rnd.nextInt(10) - 100;
            List<List<Integer>> got = subsets(a);
            if (got.size() != (1 << n)) throw new AssertionError("size");
            Set<List<Integer>> seen = new HashSet<>(got);
            if (seen.size() != got.size()) throw new AssertionError("repeat");
        }
        System.out.println("ok");
    }
}
```

#### Solution: [Vary] Subsets (LeetCode 78)
<!-- id: bt-subsets-start-index -->

**Approach.**
The search is the one of the previous solution, applied to up to ten values. Each call stores its path on entry and loops over indices from `start`. Choosing index `i` passes `i + 1` as the next start, so each subset appears as one increasing list of indices and no subset appears twice. The result lists a parent before its children and visits the children in increasing index order, which gives the entry order. For `[1, 2, 3]`, the call for `[1]` stores `[1, 2]`, then `[1, 2, 3]`, then `[1, 3]`, before the root tries index 1.

**Complexity.**
- **Time** is O(n * 2^n), because the search makes 2^n calls and each copies up to n values.
- **Space** is O(n) for the path and the stack, plus the output.

```java run
import java.util.*;

public final class SubsetsStartIndex {
    /**
     * Returns every subset of nums in call-entry order.
     * Time: O(n * 2^n). Space: O(n) besides the output.
     * Invariant: the path lists the chosen values at increasing indices, and the next choice uses an index at or after start.
     */
    static List<List<Integer>> subsets(int[] nums) {
        List<List<Integer>> out = new ArrayList<>();
        go(0, nums, new ArrayList<>(), out);
        return out;
    }

    private static void go(int start, int[] nums, List<Integer> path, List<List<Integer>> out) {
        out.add(new ArrayList<>(path));                  // record on entry
        for (int i = start; i < nums.length; i++) {      // later indices only
            path.add(nums[i]);                           // choose
            go(i + 1, nums, path, out);                  // explore with a larger start
            path.remove(path.size() - 1);                // undo
        }
    }

    /** Oracle: the subsets in entry order equal the masks sorted by the lexicographic order of their index lists. */
    static List<List<Integer>> oracle(int[] a) {
        int n = a.length;
        List<int[]> idx = new ArrayList<>();
        for (int mask = 0; mask < (1 << n); mask++) {
            int[] list = new int[Integer.bitCount(mask)]; int p = 0;
            for (int i = 0; i < n; i++) if ((mask >> i & 1) == 1) list[p++] = i;
            idx.add(list);
        }
        idx.sort(Arrays::compare);                       // a prefix sorts before its extensions
        List<List<Integer>> out = new ArrayList<>();
        for (int[] l : idx) { List<Integer> s = new ArrayList<>(); for (int i : l) s.add(a[i]); out.add(s); }
        return out;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!subsets(new int[] {1, 2, 3}).equals(List.of(List.of(), List.of(1), List.of(1, 2), List.of(1, 2, 3), List.of(1, 3), List.of(2), List.of(2, 3), List.of(3)))) throw new AssertionError("ex1");
        if (!subsets(new int[] {4, 0}).equals(List.of(List.of(), List.of(4), List.of(4, 0), List.of(0)))) throw new AssertionError("ex2");
        // Random inputs must match the sorted index lists.
        Random rnd = new Random(1922);
        for (int t = 0; t < 300; t++) {
            int n = rnd.nextInt(9);
            Set<Integer> set = new LinkedHashSet<>();
            while (set.size() < n) set.add(rnd.nextInt(21) - 10);
            int[] a = set.stream().mapToInt(Integer::intValue).toArray();
            List<List<Integer>> got = subsets(a);
            if (!got.equals(oracle(a))) throw new AssertionError("random " + t);
            if (got.size() != (1 << n)) throw new AssertionError("count " + t);
        }
        // The input must stay unchanged.
        int[] keep = {2, 9, 4}; subsets(keep);
        if (!Arrays.equals(keep, new int[] {2, 9, 4})) throw new AssertionError("mutation");
        System.out.println("ok");
    }
}
```

#### Solution: [Boundary] Empty Input (Author exercise)
<!-- id: bt-subsets-empty-input -->

**Approach.**
The search keeps the shared path and a running sum. Each call checks its own path first, because every path is a complete subset, and it stores a copy when the sum equals `target`. For an empty `nums`, the root call is the only call, its path is empty and its sum is 0. The result holds the empty list when `target` is 0 and no list when it is not. Negative values allow a sum to leave the target and return to it, so the search must not stop when the sum exceeds `target`. It visits all 2^n paths.

**Complexity.**
- **Time** is O(n * 2^n), because the search makes 2^n calls and each match copies up to n values.
- **Space** is O(n) for the path and the stack, plus the output.

```java run
import java.util.*;

public final class SubsetsEmptyInput {
    /**
     * Returns the subsets of nums that add up to target, in call-entry order.
     * Time: O(n * 2^n). Space: O(n) besides the output.
     * Invariant: sum equals the total of the values in the path.
     */
    static List<List<Integer>> withSum(int[] nums, int target) {
        List<List<Integer>> out = new ArrayList<>();
        go(0, 0, nums, target, new ArrayList<>(), out);
        return out;
    }

    private static void go(int start, int sum, int[] nums, int target, List<Integer> path, List<List<Integer>> out) {
        if (sum == target) out.add(new ArrayList<>(path));      // the empty path counts when target is 0
        for (int i = start; i < nums.length; i++) {             // no early stop, because values may be negative
            path.add(nums[i]);                                  // choose index i
            go(i + 1, sum + nums[i], nums, target, path, out);  // the child sees the larger sum
            path.remove(path.size() - 1);                       // undo the choice
        }
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!withSum(new int[] {}, 0).equals(List.of(List.of()))) throw new AssertionError("ex1");
        if (!withSum(new int[] {1, 2, 3}, 3).equals(List.of(List.of(1, 2), List.of(3)))) throw new AssertionError("ex2");
        if (!withSum(new int[] {}, 1).isEmpty()) throw new AssertionError("empty result");
        // A negative value lets the sum leave the target and return, so [5, -5] and the empty set both reach 0.
        if (!withSum(new int[] {5, -5}, 0).equals(List.of(List.of(), List.of(5, -5)))) throw new AssertionError("negative");
        // Random inputs must match a mask enumeration filtered by sum, after sorting both sides.
        Random rnd = new Random(1923);
        for (int t = 0; t < 300; t++) {
            int n = rnd.nextInt(9);
            Set<Integer> set = new LinkedHashSet<>();
            while (set.size() < n) set.add(rnd.nextInt(41) - 20);
            int[] a = set.stream().mapToInt(Integer::intValue).toArray();
            int target = rnd.nextInt(41) - 20;
            Set<List<Integer>> want = new HashSet<>();
            for (int mask = 0; mask < (1 << n); mask++) {
                List<Integer> s = new ArrayList<>(); int sum = 0;
                for (int i = 0; i < n; i++) if ((mask >> i & 1) == 1) { s.add(a[i]); sum += a[i]; }
                if (sum == target) want.add(s);
            }
            List<List<Integer>> got = withSum(a, target);
            if (!new HashSet<>(got).equals(want) || got.size() != want.size()) throw new AssertionError("random " + t);
        }
        System.out.println("ok");
    }
}
```

#### Solution: [Recognize] Subsets II Count (LeetCode 90)
<!-- id: bt-subsets-distinct-count -->

**Approach.**
Two subsets are equal when their sorted value lists are equal, so the method sorts a copy of `nums` and searches with a start index. Each path is then already sorted, and the method stores the path in a `HashSet<List<Integer>>`, which keeps one copy of every distinct list. The answer is the size of the set. The search still visits the repeated index sets, so equal values cost extra calls. A later lesson removes those calls by skipping equal siblings. The method sorts a copy and leaves the caller's array unchanged.

**Complexity.**
- **Time** is O(n * 2^n), because the search makes 2^n calls and each hashes and copies a list of up to n values.
- **Space** is O(n * 2^n) in the worst case for the set, plus O(n) for the path and the stack.

```java run
import java.util.*;

public final class SubsetsDistinctCount {
    /**
     * Returns the number of different subsets of nums, treating equal values as interchangeable.
     * Time: O(n * 2^n). Space: O(n * 2^n) for the set.
     * Invariant: the path is sorted, so equal subsets give equal lists.
     */
    static int distinct(int[] nums) {
        int[] a = nums.clone();                            // sort a copy so the caller's array keeps its order
        Arrays.sort(a);
        Set<List<Integer>> seen = new HashSet<>();
        go(0, a, new ArrayList<>(), seen);
        return seen.size();
    }

    private static void go(int start, int[] a, List<Integer> path, Set<List<Integer>> seen) {
        seen.add(new ArrayList<>(path));                   // the set drops lists that already appeared
        for (int i = start; i < a.length; i++) {           // increasing indices keep each list sorted
            path.add(a[i]);                                // choose index i
            go(i + 1, a, path, seen);                      // explore the later indices
            path.remove(path.size() - 1);                  // undo the choice
        }
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (distinct(new int[] {1, 2, 2}) != 6) throw new AssertionError("ex1");
        if (distinct(new int[] {3, 3, 3}) != 4) throw new AssertionError("ex2");
        if (distinct(new int[] {}) != 1) throw new AssertionError("empty");
        // Random inputs must match a product formula over value counts: the product of (count + 1).
        Random rnd = new Random(1924);
        for (int t = 0; t < 400; t++) {
            int[] a = new int[rnd.nextInt(11)];
            for (int i = 0; i < a.length; i++) a[i] = rnd.nextInt(5) - 2;
            Map<Integer, Integer> cnt = new HashMap<>();
            for (int v : a) cnt.merge(v, 1, Integer::sum);
            int want = 1; for (int c : cnt.values()) want *= c + 1;
            int[] copy = a.clone();
            if (distinct(a) != want) throw new AssertionError("random " + t);
            if (!Arrays.equals(a, copy)) throw new AssertionError("mutation " + t);
        }
        // The Java claim: equal lists have equal hash codes, so a HashSet of lists detects repeats.
        if (!new ArrayList<>(List.of(1, 2)).equals(List.of(1, 2)) || new ArrayList<>(List.of(1, 2)).hashCode() != List.of(1, 2).hashCode()) throw new AssertionError("list equality");
        System.out.println("ok");
    }
}
```
