<!-- solutions-for: 05-increasing-start-combinations -->
### Solutions For Choosing K Values

#### Solution: [Build] Choose Two From Four (Author exercise)
<!-- id: bt-choose-two-from-four -->

**Approach.**
A call receives a start index and the shared path. When the path holds two values, the call stores a copy and returns. Otherwise it loops from `start` to the last index, adds the value, calls itself with the next index as the start and removes the value. The next start rises past the chosen index, so each pair of indices appears once, in increasing order. The root tries four first choices. The first three have children that store pairs, and the last has a child with no index left.

**Complexity.**
- **Time** is O(1) for four values, with 10 choices and 6 copies; in general it is O(k * C(n, k)).
- **Space** is O(1) for four values, and O(k) in general besides the output.

```java run
import java.util.*;

public final class ChooseTwoFromFour {
    /**
     * Returns the six pairs of four values, in increasing index order.
     * Time: O(1) for four values. Space: O(1) besides the output.
     * Invariant: the path lists increasing indices, and each child starts one past the last chosen index.
     */
    static List<List<Integer>> pairs(int[] nums) {
        List<List<Integer>> out = new ArrayList<>();
        go(0, nums, new ArrayList<>(), out);
        return out;
    }

    private static void go(int start, int[] nums, List<Integer> path, List<List<Integer>> out) {
        if (path.size() == 2) { out.add(new ArrayList<>(path)); return; }   // two values: store a copy and stop
        for (int i = start; i < nums.length; i++) {          // only indices at or after start
            path.add(nums[i]);                               // choose index i
            go(i + 1, nums, path, out);                      // the child starts one past i
            path.remove(path.size() - 1);                    // undo the choice
        }
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!pairs(new int[] {1, 2, 3, 4}).equals(List.of(List.of(1, 2), List.of(1, 3), List.of(1, 4), List.of(2, 3), List.of(2, 4), List.of(3, 4)))) throw new AssertionError("ex1");
        if (!pairs(new int[] {9, 0, 5, 2}).equals(List.of(List.of(9, 0), List.of(9, 5), List.of(9, 2), List.of(0, 5), List.of(0, 2), List.of(5, 2)))) throw new AssertionError("ex2");
        // Random quadruples must match nested loops over index pairs.
        Random rnd = new Random(1941);
        for (int t = 0; t < 200; t++) {
            Set<Integer> s = new LinkedHashSet<>();
            while (s.size() < 4) s.add(rnd.nextInt(201) - 100);
            int[] a = s.stream().mapToInt(Integer::intValue).toArray();
            List<List<Integer>> want = new ArrayList<>();
            for (int x = 0; x < 4; x++) for (int y = x + 1; y < 4; y++) want.add(List.of(a[x], a[y]));
            if (!pairs(a).equals(want)) throw new AssertionError("random " + t);
        }
        System.out.println("ok");
    }
}
```

#### Solution: [Vary] Combinations (LeetCode 77)
<!-- id: bt-combinations-n-choose-k -->

**Approach.**
The values are the numbers `1` to `n`, so the call at start `s` tries the numbers from `s` upward, and it needs no array. A call with `k` numbers on the path stores a copy and returns. Each child starts one number higher than the number just chosen, so every list is increasing and appears once. For `k = 0`, the root already has the target size and stores the empty list. The loop ends at the last useful number `n - (k - size) + 1`, which avoids calls that cannot finish.

**Complexity.**
- **Time** is O(k * C(n, k)), because the search stores C(n, k) lists and copies k numbers each, and every call extends to a result.
- **Space** is O(k) for the path and the stack, plus the output.

```java run
import java.util.*;

public final class CombinationsNChooseK {
    /**
     * Returns all lists of k numbers from 1..n in increasing order, in search order.
     * Time: O(k * C(n, k)). Space: O(k) besides the output.
     * Invariant: the path is increasing and can still grow to k numbers.
     */
    static List<List<Integer>> combine(int n, int k) {
        List<List<Integer>> out = new ArrayList<>();
        go(1, n, k, new ArrayList<>(), out);
        return out;
    }

    private static void go(int start, int n, int k, List<Integer> path, List<List<Integer>> out) {
        if (path.size() == k) { out.add(new ArrayList<>(path)); return; }   // target size reached
        int last = n - (k - path.size()) + 1;                // highest number that can still finish
        for (int v = start; v <= last; v++) {                // numbers above last leave too few numbers
            path.add(v);                                     // choose v
            go(v + 1, n, k, path, out);                      // the child starts one above v
            path.remove(path.size() - 1);                    // undo the choice
        }
    }

    static long binom(int n, int k) { long r = 1; for (int i = 1; i <= k; i++) r = r * (n - k + i) / i; return r; }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!combine(4, 3).equals(List.of(List.of(1, 2, 3), List.of(1, 2, 4), List.of(1, 3, 4), List.of(2, 3, 4)))) throw new AssertionError("ex1");
        if (!combine(3, 0).equals(List.of(List.of()))) throw new AssertionError("ex2");
        // Every n and k in range must give the binomial count, increasing lists and lexicographic order.
        for (int n = 1; n <= 12; n++) for (int k = 0; k <= n; k++) {
            List<List<Integer>> got = combine(n, k);
            if (got.size() != binom(n, k)) throw new AssertionError("count " + n + "," + k);
            for (int j = 0; j < got.size(); j++) {
                List<Integer> l = got.get(j);
                for (int i = 1; i < l.size(); i++) if (l.get(i) <= l.get(i - 1)) throw new AssertionError("increasing");
                if (j > 0 && compare(got.get(j - 1), l) >= 0) throw new AssertionError("order " + n + "," + k);
            }
        }
        System.out.println("ok");
    }

    static int compare(List<Integer> a, List<Integer> b) {
        for (int i = 0; i < Math.min(a.size(), b.size()); i++) if (!a.get(i).equals(b.get(i))) return a.get(i) - b.get(i);
        return a.size() - b.size();
    }
}
```

#### Solution: [Boundary] Insufficient Remaining Values (Author exercise)
<!-- id: bt-insufficient-remaining -->

**Approach.**
The method runs the search of the previous solution and counts each call, including the root. A call with a full path counts itself and stops. Otherwise its loop runs up to the last useful number `n - (k - size) + 1`. When `k` exceeds `n`, the last useful number at the root is below 1, so the loop has no iteration and the search makes the root call only. For `k = 0`, the root has the target size and counts once. A prefix of `j` numbers makes a call exactly when it can still extend to `k` numbers. The calls of all prefix lengths add up to C(n + 1, k) when `k <= n`.

**Complexity.**
- **Time** is O(C(n + 1, k)), because the search makes that many calls and each call costs O(1) outside the copies, which this method skips.
- **Space** is O(k) for the stack and the size counter.

```java run
import java.util.*;

public final class InsufficientRemaining {
    private static long calls;

    /**
     * Returns the number of calls of the combination search with the early loop end, root included.
     * Time: O(C(n + 1, k)). Space: O(k) stack frames.
     * Invariant: every call that has a loop iteration reaches at least one stored result.
     */
    static long countCalls(int n, int k) {
        calls = 0;
        go(1, n, k, 0);
        return calls;
    }

    private static void go(int start, int n, int k, int size) {
        calls++;                                             // every entry counts as one call
        if (size == k) return;                               // target size: nothing more to choose
        int last = n - (k - size) + 1;                       // highest number that can still finish
        for (int v = start; v <= last; v++) go(v + 1, n, k, size + 1);   // each child path is one number longer
    }

    static long binom(int n, int k) { if (k < 0 || k > n) return 0; long r = 1; for (int i = 1; i <= k; i++) r = r * (n - k + i) / i; return r; }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (countCalls(4, 2) != 10) throw new AssertionError("ex1");
        if (countCalls(3, 5) != 1) throw new AssertionError("ex2");
        if (countCalls(0, 0) != 1) throw new AssertionError("empty range");
        // The closed form: C(n + 1, k) calls when k <= n, and one call otherwise.
        for (int n = 0; n <= 14; n++) for (int k = 0; k <= 18; k++) {
            long want = k <= n ? binom(n + 1, k) : 1;
            if (countCalls(n, k) != want) throw new AssertionError("n=" + n + " k=" + k + " got " + countCalls(n, k) + " want " + want);
        }
        // Without the early end, the same search makes more calls for n = 4 and k = 2.
        calls = 0; plain(1, 4, 2, 0);
        if (calls != 11) throw new AssertionError("plain calls " + calls);
        System.out.println("ok");
    }

    private static void plain(int start, int n, int k, int size) {
        calls++;
        if (size == k) return;
        for (int v = start; v <= n; v++) plain(v + 1, n, k, size + 1);
    }
}
```

#### Solution: [Recognize] Combination Sum III (LeetCode 216)
<!-- id: bt-combination-sum-three -->

**Approach.**
The digits `1` to `9` form the candidate range, and a path is increasing, so each digit appears at most once and each set of digits appears once. The call keeps a remaining sum, which starts at `n` and falls by each chosen digit. A call stores a copy when the path holds `k` digits and the remaining sum is 0. A full path with a nonzero remaining sum stores nothing. The loop starts at `start` and may stop early when a digit exceeds the remaining sum, because every later digit is larger and the digits are positive. The loop also ends at the last useful digit `9 - (k - size) + 1`.

**Complexity.**
- **Time** is O(k * C(9, k)), because at most C(9, k) increasing lists exist and each costs O(k) to copy.
- **Space** is O(k) for the path and the stack, plus the output.

```java run
import java.util.*;

public final class CombinationSumThree {
    /**
     * Returns the increasing lists of k digits from 1..9 that add up to n, in search order.
     * Time: O(k * C(9, k)). Space: O(k) besides the output.
     * Invariant: remain equals n minus the sum of the path.
     */
    static List<List<Integer>> combos(int k, int n) {
        List<List<Integer>> out = new ArrayList<>();
        go(1, k, n, new ArrayList<>(), out);
        return out;
    }

    private static void go(int start, int k, int remain, List<Integer> path, List<List<Integer>> out) {
        if (path.size() == k) {                              // target size: the remaining sum decides
            if (remain == 0) out.add(new ArrayList<>(path));
            return;
        }
        int last = 9 - (k - path.size()) + 1;                // highest digit that can still finish
        for (int d = start; d <= last && d <= remain; d++) { // a digit above the remaining sum overshoots
            path.add(d);                                     // choose digit d
            go(d + 1, k, remain - d, path, out);             // a larger start and a smaller remaining sum
            path.remove(path.size() - 1);                    // undo the choice
        }
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!combos(2, 5).equals(List.of(List.of(1, 4), List.of(2, 3)))) throw new AssertionError("ex1");
        if (!combos(4, 1).isEmpty()) throw new AssertionError("ex2");
        // Every k and n in range must match a mask enumeration over the nine digits, in order.
        for (int k = 1; k <= 9; k++) for (int n = 1; n <= 60; n++) {
            List<List<Integer>> want = new ArrayList<>();
            for (int mask = 0; mask < 512; mask++) {
                if (Integer.bitCount(mask) != k) continue;
                List<Integer> l = new ArrayList<>(); int sum = 0;
                for (int d = 1; d <= 9; d++) if ((mask >> (d - 1) & 1) == 1) { l.add(d); sum += d; }
                if (sum == n) want.add(l);
            }
            want.sort((x, y) -> { for (int i = 0; i < x.size(); i++) if (!x.get(i).equals(y.get(i))) return x.get(i) - y.get(i); return 0; });
            if (!combos(k, n).equals(want)) throw new AssertionError("k=" + k + " n=" + n);
        }
        // A known case: the three digits that sum to 9 are three lists.
        if (combos(3, 9).size() != 3) throw new AssertionError("k=3 n=9");
        System.out.println("ok");
    }
}
```
