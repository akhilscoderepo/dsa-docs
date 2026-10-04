<!-- solutions-for: 03-subsets -->
### Subsets

#### Solution: [Build] Subsets Of Two Values (Author exercise)
<!-- id: bt-two-values -->

**Approach.** The call at index 0 first recurses with the value left out, then appends it, recurses again and removes it, and the call at index 1 does the same, so the four leaves are reached in the order leave-leave, leave-take, take-leave, take-take. A leaf stores a copy of the path. The code works for any array length, which lets the harness check it against an oracle that counts masks upward and reads the highest bit as the first value, since leaving a value out first corresponds to a zero bit in that position. The two given examples are asserted as well, including the value zero, which must appear as the subset holding a zero and not be confused with the empty subset.

**Complexity.** Four leaves for two values and, in general, 2^n leaves of O(n) copying each, with a stack of n frames.

```java run
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public final class TwoValues {
    static void settle(int[] nums, int index, List<Integer> path, List<List<Integer>> out) {
        if (index == nums.length) {
            out.add(new ArrayList<>(path));
            return;
        }
        settle(nums, index + 1, path, out);
        path.add(nums[index]);
        settle(nums, index + 1, path, out);
        path.remove(path.size() - 1);
    }

    static List<List<Integer>> subsets(int[] nums) {
        List<List<Integer>> out = new ArrayList<>();
        settle(nums, 0, new ArrayList<>(), out);
        return out;
    }

    static List<List<Integer>> oracle(int[] nums) {
        int n = nums.length;
        List<List<Integer>> out = new ArrayList<>();
        for (int m = 0; m < (1 << n); m++) {
            List<Integer> s = new ArrayList<>();
            for (int i = 0; i < n; i++) if ((m >> (n - 1 - i) & 1) == 1) s.add(nums[i]);
            out.add(s);
        }
        return out;
    }

    public static void main(String[] args) {
        if (!subsets(new int[] {4, 7}).equals(List.of(List.of(), List.of(7), List.of(4), List.of(4, 7)))) throw new AssertionError("example 1");
        if (!subsets(new int[] {-1, 0}).equals(List.of(List.of(), List.of(0), List.of(-1), List.of(-1, 0)))) throw new AssertionError("example 2");
        Random rnd = new Random(19301);
        for (int t = 0; t < 3000; t++) {
            int n = rnd.nextInt(7);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(201) - 100;
            if (!subsets(a).equals(oracle(a))) throw new AssertionError("differs on length " + n);
        }
    }
}
```

#### Solution: [Vary] Subsets In Arrival Order (LeetCode 78)
<!-- id: bt-preorder-subsets -->

**Approach.** Each call records a copy of the path before doing anything else, then loops `i` from `start` to the end, appends `nums[i]`, recurses with `i + 1` and removes the element. The order of the card is the order of arrival, which equals sorting the subsets by their index lists, shorter prefix first. The oracle therefore builds all subsets from masks, turns each into the ascending list of its indexes and sorts those lists, sharing no code with the recursion. The harness compares the two on random arrays and checks that the first recorded subset is the empty one.

**Complexity.** There are 2^n nodes, each copied once at O(n), for O(n * 2^n) time and n stack frames.

```java run
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Random;
import java.util.Set;

public final class PreorderSubsets {
    static void collect(int[] nums, int start, List<Integer> path, List<List<Integer>> out) {
        out.add(new ArrayList<>(path));
        for (int i = start; i < nums.length; i++) {
            path.add(nums[i]);
            collect(nums, i + 1, path, out);
            path.remove(path.size() - 1);
        }
    }

    static List<List<Integer>> subsets(int[] nums) {
        List<List<Integer>> out = new ArrayList<>();
        collect(nums, 0, new ArrayList<>(), out);
        return out;
    }

    static int cmp(List<Integer> a, List<Integer> b) {
        for (int i = 0; i < Math.min(a.size(), b.size()); i++) if (!a.get(i).equals(b.get(i))) return a.get(i) - b.get(i);
        return a.size() - b.size();
    }

    static List<List<Integer>> oracle(int[] nums) {
        int n = nums.length;
        List<List<Integer>> idx = new ArrayList<>();
        for (int m = 0; m < (1 << n); m++) {
            List<Integer> s = new ArrayList<>();
            for (int i = 0; i < n; i++) if ((m >> i & 1) == 1) s.add(i);
            idx.add(s);
        }
        idx.sort(PreorderSubsets::cmp);
        List<List<Integer>> out = new ArrayList<>();
        for (List<Integer> s : idx) {
            List<Integer> vals = new ArrayList<>();
            for (int i : s) vals.add(nums[i]);
            out.add(vals);
        }
        return out;
    }

    public static void main(String[] args) {
        List<List<Integer>> want = List.of(List.of(), List.of(1), List.of(1, 2), List.of(1, 2, 3), List.of(1, 3), List.of(2), List.of(2, 3), List.of(3));
        if (!subsets(new int[] {1, 2, 3}).equals(want)) throw new AssertionError("example 1");
        if (!subsets(new int[] {4, 9}).equals(List.of(List.of(), List.of(4), List.of(4, 9), List.of(9)))) throw new AssertionError("example 2");
        Random rnd = new Random(19302);
        for (int t = 0; t < 2000; t++) {
            int n = rnd.nextInt(9);
            Set<Integer> used = new HashSet<>();
            int[] a = new int[n];
            for (int i = 0; i < n; i++) {
                int v;
                do { v = rnd.nextInt(21) - 10; } while (!used.add(v));
                a[i] = v;
            }
            List<List<Integer>> got = subsets(a);
            if (!got.equals(oracle(a))) throw new AssertionError("differs on length " + n);
            if (!got.get(0).isEmpty() || got.size() != (1 << n)) throw new AssertionError("first record or size wrong");
        }
    }
}
```

#### Solution: [Boundary] Empty Input (Author exercise)
<!-- id: bt-empty-input -->

**Approach.** The search carries the running sum, records a copy of the path whenever the sum equals the target, and never abandons a path on a partial sum, because values may be negative and a sum above the target can still come back down. The empty array reaches only the root, whose sum is zero, so a target of zero returns a list holding one empty list and any other target returns an empty list. The harness runs a careless variant that stops when the sum exceeds the target, and asserts that it loses an answer on the second example, which is exactly what the hint warns about. The oracle filters all masks by sum and sorts them into arrival order.

**Complexity.** All 2^n nodes are visited since no branch can be ruled out, at O(n) copying per answer.

```java run
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Random;
import java.util.Set;

public final class EmptyInputSums {
    static void go(int[] nums, int start, int sum, int t, boolean prune, List<Integer> path, List<List<Integer>> out) {
        if (sum == t) out.add(new ArrayList<>(path));
        for (int i = start; i < nums.length; i++) {
            if (prune && sum + nums[i] > t) continue;
            path.add(nums[i]);
            go(nums, i + 1, sum + nums[i], t, prune, path, out);
            path.remove(path.size() - 1);
        }
    }

    static List<List<Integer>> solve(int[] nums, int t, boolean prune) {
        List<List<Integer>> out = new ArrayList<>();
        go(nums, 0, 0, t, prune, new ArrayList<>(), out);
        return out;
    }

    static List<List<Integer>> oracle(int[] nums, int t) {
        int n = nums.length;
        List<List<Integer>> idx = new ArrayList<>();
        for (int m = 0; m < (1 << n); m++) {
            List<Integer> s = new ArrayList<>();
            int sum = 0;
            for (int i = 0; i < n; i++) if ((m >> i & 1) == 1) { s.add(i); sum += nums[i]; }
            if (sum == t) idx.add(s);
        }
        idx.sort((a, b) -> {
            for (int i = 0; i < Math.min(a.size(), b.size()); i++) if (!a.get(i).equals(b.get(i))) return a.get(i) - b.get(i);
            return a.size() - b.size();
        });
        List<List<Integer>> out = new ArrayList<>();
        for (List<Integer> s : idx) {
            List<Integer> vals = new ArrayList<>();
            for (int i : s) vals.add(nums[i]);
            out.add(vals);
        }
        return out;
    }

    public static void main(String[] args) {
        List<List<Integer>> a = solve(new int[0], 0, false);
        if (a.size() != 1 || !a.get(0).isEmpty()) throw new AssertionError("example 1");
        if (!solve(new int[0], 5, false).isEmpty()) throw new AssertionError("empty array with target 5");
        int[] second = {3, -3, 5};
        if (!solve(second, 0, false).equals(List.of(List.of(), List.of(3, -3)))) throw new AssertionError("example 2");
        if (solve(second, 0, true).equals(solve(second, 0, false))) throw new AssertionError("pruning on the running sum should lose [3, -3]");
        Random rnd = new Random(19303);
        for (int t = 0; t < 3000; t++) {
            int n = rnd.nextInt(9);
            Set<Integer> used = new HashSet<>();
            int[] nums = new int[n];
            for (int i = 0; i < n; i++) {
                int v;
                do { v = rnd.nextInt(41) - 20; } while (!used.add(v));
                nums[i] = v;
            }
            int target = rnd.nextInt(21) - 10;
            if (!solve(nums, target, false).equals(oracle(nums, target))) throw new AssertionError("differs on length " + n);
        }
    }
}
```

#### Solution: [Recognize] Subsets With Equal Values (LeetCode 90)
<!-- id: bt-subsets-with-equals -->

**Approach.** A copy of the input is sorted so that equal values are adjacent, and the original array is left alone, which the harness checks. Inside the increasing-start loop an element is skipped when `i > start` and it equals the element before it, so among equal siblings only the first is taken, while the same value can still be taken again one level deeper. The oracle takes every mask over the sorted copy, puts the resulting value lists into a set to remove repeats, and sorts them lexicographically, which equals arrival order. The harness also confirms that without the skip the search lists 2^n entries, so the repeats are real.

**Complexity.** At most 2^n nodes, each copied at O(n), so O(n * 2^n) time, plus O(n log n) for the sort.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashSet;
import java.util.List;
import java.util.Random;
import java.util.Set;

public final class SubsetsWithEquals {
    static void collect(int[] nums, int start, boolean skip, List<Integer> path, List<List<Integer>> out) {
        out.add(new ArrayList<>(path));
        for (int i = start; i < nums.length; i++) {
            if (skip && i > start && nums[i] == nums[i - 1]) continue;
            path.add(nums[i]);
            collect(nums, i + 1, skip, path, out);
            path.remove(path.size() - 1);
        }
    }

    static List<List<Integer>> distinctSubsets(int[] nums, boolean skip) {
        int[] sorted = nums.clone();
        Arrays.sort(sorted);
        List<List<Integer>> out = new ArrayList<>();
        collect(sorted, 0, skip, new ArrayList<>(), out);
        return out;
    }

    static List<List<Integer>> oracle(int[] nums) {
        int[] sorted = nums.clone();
        Arrays.sort(sorted);
        int n = sorted.length;
        Set<List<Integer>> seen = new HashSet<>();
        for (int m = 0; m < (1 << n); m++) {
            List<Integer> s = new ArrayList<>();
            for (int i = 0; i < n; i++) if ((m >> i & 1) == 1) s.add(sorted[i]);
            seen.add(s);
        }
        List<List<Integer>> out = new ArrayList<>(seen);
        out.sort((a, b) -> {
            for (int i = 0; i < Math.min(a.size(), b.size()); i++) if (!a.get(i).equals(b.get(i))) return a.get(i) - b.get(i);
            return a.size() - b.size();
        });
        return out;
    }

    public static void main(String[] args) {
        List<List<Integer>> one = List.of(List.of(), List.of(1), List.of(1, 2), List.of(1, 2, 2), List.of(2), List.of(2, 2));
        if (!distinctSubsets(new int[] {1, 2, 2}, true).equals(one)) throw new AssertionError("example 1");
        List<List<Integer>> two = List.of(List.of(), List.of(1), List.of(1, 4), List.of(1, 4, 4), List.of(1, 4, 4, 4), List.of(4), List.of(4, 4), List.of(4, 4, 4));
        if (!distinctSubsets(new int[] {4, 1, 4, 4}, true).equals(two)) throw new AssertionError("example 2");
        int[] original = {3, 1, 2};
        distinctSubsets(original, true);
        if (!Arrays.equals(original, new int[] {3, 1, 2})) throw new AssertionError("the caller's array must stay unsorted");
        int[] sortedInPlace = {3, 1, 2};
        Arrays.sort(sortedInPlace);
        if (Arrays.equals(sortedInPlace, new int[] {3, 1, 2})) throw new AssertionError("Arrays.sort changes the array it is given");
        Random rnd = new Random(19304);
        for (int t = 0; t < 3000; t++) {
            int n = rnd.nextInt(9);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(5) - 2;
            if (!distinctSubsets(a, true).equals(oracle(a))) throw new AssertionError("differs on " + Arrays.toString(a));
            if (distinctSubsets(a, false).size() != (1 << n)) throw new AssertionError("without the skip every mask appears");
        }
    }
}
```
