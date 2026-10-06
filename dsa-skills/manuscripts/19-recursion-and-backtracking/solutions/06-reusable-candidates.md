<!-- solutions-for: 06-reusable-candidates -->
### Solutions For Reusing A Value

#### Solution: [Build] Sum With Repeated Coins (Author exercise)
<!-- id: bt-sum-with-repeated-coins -->

**Approach.**
A call receives a start index, the remaining target and the shared path. A remaining target of 0 stores a copy of the path, which is the empty list when the target is 0 at the root. A negative remaining target returns without storing. Otherwise the loop runs from `start`, adds coin `i` and calls itself with the same start `i`, so coin `i` may repeat. The path lists indices that never decrease, so each multiset of coins appears once.

**Complexity.**
- **Time** is O(c^(t/m) * t/m) in the worst case, for `c` coins, target `t` and smallest coin `m`. The depth is at most `t / m`, and each call may try every coin.
- **Space** is O(t / m) for the path and the stack, plus the output.

```java run
import java.util.*;

public final class SumWithRepeatedCoins {
    /**
     * Returns every nondecreasing-index list of coins that adds up to target.
     * Time: O(c^(t/m) * t/m) worst case. Space: O(t/m) besides the output.
     * Invariant: remain equals target minus the sum of the path, and indices never decrease.
     */
    static List<List<Integer>> pay(int[] coins, int target) {
        List<List<Integer>> out = new ArrayList<>();
        go(0, target, coins, new ArrayList<>(), out);
        return out;
    }

    private static void go(int start, int remain, int[] coins, List<Integer> path, List<List<Integer>> out) {
        if (remain < 0) return;                              // the path overshoots the target
        if (remain == 0) { out.add(new ArrayList<>(path)); return; }   // exact sum: store a copy
        for (int i = start; i < coins.length; i++) {         // the same coin or a later one
            path.add(coins[i]);                              // choose coin i
            go(i, remain - coins[i], coins, path, out);      // same start: coin i stays available
            path.remove(path.size() - 1);                    // undo the choice
        }
    }

    /** Oracle: enumerate count vectors with a mixed-radix counter, then sort by the index list. */
    static List<List<Integer>> oracle(int[] c, int target) {
        int m = c.length; int[] cap = new int[m]; long total = 1;
        for (int i = 0; i < m; i++) { cap[i] = target / c[i] + 1; total *= cap[i]; }
        List<int[]> lists = new ArrayList<>();
        for (long code = 0; code < total; code++) {
            long x = code; int sum = 0; int[] cnt = new int[m];
            for (int i = 0; i < m; i++) { cnt[i] = (int) (x % cap[i]); x /= cap[i]; sum += cnt[i] * c[i]; }
            if (sum != target) continue;
            int len = 0; for (int v : cnt) len += v;
            int[] idx = new int[len]; int p = 0;
            for (int i = 0; i < m; i++) for (int j = 0; j < cnt[i]; j++) idx[p++] = i;
            lists.add(idx);
        }
        lists.sort(Arrays::compare);
        List<List<Integer>> out = new ArrayList<>();
        for (int[] idx : lists) { List<Integer> l = new ArrayList<>(); for (int i : idx) l.add(c[i]); out.add(l); }
        return out;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!pay(new int[] {1, 2}, 3).equals(List.of(List.of(1, 1, 1), List.of(1, 2)))) throw new AssertionError("ex1");
        if (!pay(new int[] {5}, 0).equals(List.of(List.of()))) throw new AssertionError("ex2");
        if (!pay(new int[] {5}, 3).isEmpty()) throw new AssertionError("empty result");
        // Random inputs must match the count-vector oracle in the same order.
        Random rnd = new Random(1961);
        for (int t = 0; t < 300; t++) {
            int m = 1 + rnd.nextInt(4);
            Set<Integer> s = new LinkedHashSet<>();
            while (s.size() < m) s.add(1 + rnd.nextInt(10));
            int[] c = s.stream().mapToInt(Integer::intValue).toArray();
            int target = rnd.nextInt(16);
            if (!pay(c, target).equals(oracle(c, target))) throw new AssertionError("random " + t);
        }
        // Ten cents with the coins 1, 2 and 3 has exactly 14 payments, and a restart at zero would give 274 lists.
        if (pay(new int[] {1, 2, 3}, 10).size() != 14) throw new AssertionError("ten cents");
        System.out.println("ok");
    }
}
```

#### Solution: [Vary] Combination Sum (LeetCode 39)
<!-- id: bt-combination-sum -->

**Approach.**
The method is the search of the previous solution applied to positive candidates in any order. A call with remaining target 0 stores a copy, and a negative remaining target returns. The loop passes the chosen index as the next start, so a candidate may repeat and a list never uses an earlier candidate after a later one. Because the start follows the input order, the values of each list follow the order of `candidates`. The remaining target is the only extra state, and the undo step removes the last entry by index.

**Complexity.**
- **Time** is O(c^(t/m) * t/m) in the worst case, because the depth is at most `t / m` for the smallest candidate `m`.
- **Space** is O(t / m) for the path and the stack, plus the output.

```java run
import java.util.*;

public final class CombinationSum {
    /**
     * Returns every list of candidates, in input order, that adds up to target; candidates may repeat.
     * Time: O(c^(t/m) * t/m) worst case. Space: O(t/m) besides the output.
     * Invariant: remain is target minus the sum of the path, and each choice uses an index at or above the last one.
     */
    static List<List<Integer>> combinationSum(int[] candidates, int target) {
        List<List<Integer>> out = new ArrayList<>();
        go(0, target, candidates, new ArrayList<>(), out);
        return out;
    }

    private static void go(int start, int remain, int[] cand, List<Integer> path, List<List<Integer>> out) {
        if (remain < 0) return;                              // overshoot
        if (remain == 0) { out.add(new ArrayList<>(path)); return; }   // exact sum
        for (int i = start; i < cand.length; i++) {          // same candidate or later
            path.add(cand[i]);                               // choose
            go(i, remain - cand[i], cand, path, out);        // same start allows reuse
            path.remove(path.size() - 1);                    // undo
        }
    }

    /** Oracle: dynamic table of lists by amount, built from the last candidate backwards, independent of the search. */
    static Set<List<Integer>> oracle(int[] cand, int target) {
        List<List<List<Integer>>> table = new ArrayList<>();
        for (int a = 0; a <= target; a++) table.add(new ArrayList<>());
        table.get(0).add(new ArrayList<>());
        for (int c : cand)                                   // candidate by candidate, so each multiset appears once
            for (int a = c; a <= target; a++)
                for (List<Integer> base : table.get(a - c)) { List<Integer> l = new ArrayList<>(base); l.add(c); table.get(a).add(l); }
        return new HashSet<>(table.get(target));
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!combinationSum(new int[] {2, 3, 6, 7}, 7).equals(List.of(List.of(2, 2, 3), List.of(7)))) throw new AssertionError("ex1");
        if (!combinationSum(new int[] {3, 5}, 2).isEmpty()) throw new AssertionError("ex2");
        // Random unsorted candidates: the set of lists must match the table oracle, and the lists must have no repeats.
        Random rnd = new Random(1962);
        for (int t = 0; t < 300; t++) {
            int m = 1 + rnd.nextInt(5);
            Set<Integer> s = new LinkedHashSet<>();
            while (s.size() < m) s.add(2 + rnd.nextInt(14));
            int[] c = s.stream().mapToInt(Integer::intValue).toArray();
            int target = 1 + rnd.nextInt(30);
            List<List<Integer>> got = combinationSum(c, target);
            Set<List<Integer>> want = oracle(c, target);
            if (!new HashSet<>(got).equals(want) || got.size() != want.size()) throw new AssertionError("random " + t);
        }
        // The input must stay unchanged.
        int[] keep = {7, 2, 5}; combinationSum(keep, 14);
        if (!Arrays.equals(keep, new int[] {7, 2, 5})) throw new AssertionError("mutation");
        System.out.println("ok");
    }
}
```

#### Solution: [Boundary] Candidate Larger Than Remainder (Author exercise)
<!-- id: bt-candidate-larger-than-remainder -->

**Approach.**
The candidates are positive and strictly increasing. When one candidate exceeds the remaining target, every later candidate is larger still, so it also exceeds the remaining target. The loop therefore stops at the first such candidate with `break`, and this loses no payment. The counter adds one for every entry into the search, including the root and the calls that reach remaining target 0. On unsorted input, a `break` at a large candidate would skip a smaller candidate after it. The stop rule therefore needs the sorted order. For target 0, the root call stores the empty list and makes no loop call.

**Complexity.**
- **Time** is O(number of calls), which is at most c^(t/m) and usually far fewer than without the stop rule.
- **Space** is O(t / m) for the stack.

```java run
import java.util.*;

public final class CandidateLargerThanRemainder {
    private static long calls;

    /**
     * Returns the number of calls of the reuse search with the stop rule, root included.
     * Time: O(calls). Space: O(t/m) stack frames.
     * Invariant: every candidate after the stopping point exceeds the remaining target.
     */
    static long countCalls(int[] cand, int target) {
        calls = 0;
        go(0, target, cand, true);
        return calls;
    }

    private static void go(int start, int remain, int[] cand, boolean stop) {
        calls++;                                             // each entry counts once
        if (remain == 0) return;                             // an exact sum needs no loop
        for (int i = start; i < cand.length; i++) {
            if (cand[i] > remain) { if (stop) break; else continue; }   // sorted input: all later candidates are larger
            go(i, remain - cand[i], cand, stop);             // same start allows reuse
        }
    }

    /** Counts the solutions of the same search, to show that the stop rule keeps every payment. */
    static int solutions(int[] cand, int start, int remain, boolean stop) {
        if (remain == 0) return 1;
        int total = 0;
        for (int i = start; i < cand.length; i++) {
            if (cand[i] > remain) { if (stop) break; else continue; }
            total += solutions(cand, i, remain - cand[i], stop);
        }
        return total;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (countCalls(new int[] {2, 3, 6, 7}, 7) != 10) throw new AssertionError("ex1 " + countCalls(new int[] {2, 3, 6, 7}, 7));
        if (countCalls(new int[] {4}, 3) != 1) throw new AssertionError("ex2");
        if (countCalls(new int[] {2}, 0) != 1) throw new AssertionError("target 0");
        // Random sorted inputs: the stop rule and the skip rule find the same number of payments.
        Random rnd = new Random(1963);
        for (int t = 0; t < 300; t++) {
            int m = 1 + rnd.nextInt(6);
            TreeSet<Integer> s = new TreeSet<>();
            while (s.size() < m) s.add(1 + rnd.nextInt(30));
            int[] c = s.stream().mapToInt(Integer::intValue).toArray();
            int target = rnd.nextInt(31);
            if (solutions(c, 0, target, true) != solutions(c, 0, target, false)) throw new AssertionError("stop loses payments " + t);
        }
        // On unsorted input the stop rule loses a payment: for target 4, the candidate 5 stops the loop before the 2 is tried.
        if (solutions(new int[] {5, 2, 3}, 0, 4, true) != 0) throw new AssertionError("unsorted stop");
        if (solutions(new int[] {5, 2, 3}, 0, 4, false) != 1) throw new AssertionError("unsorted skip");
        System.out.println("ok");
    }
}
```

#### Solution: [Recognize] Fixed-Length Reusable Sum (Author exercise)
<!-- id: bt-fixed-length-reusable-sum -->

**Approach.**
The search of the previous solutions gains one more state value, the number of choices still allowed. A call with no choice left stores a copy when the remaining sum is 0 and returns. Otherwise the loop runs from `start`, chooses candidate `i`, and calls itself with the same start, the smaller sum and one fewer choice. The reuse rule stays the same, so the path stays nondecreasing. A call whose remaining sum is negative returns at once. The path never grows beyond `k` values, so the depth is at most `k`.

**Complexity.**
- **Time** is O(c^k * k), because the depth is at most `k` and each call may try every candidate.
- **Space** is O(k) for the path and the stack, plus the output.

```java run
import java.util.*;

public final class FixedLengthReusableSum {
    /**
     * Returns every nondecreasing-index list of exactly k candidates that adds up to target.
     * Time: O(c^k * k). Space: O(k) besides the output.
     * Invariant: path.size() + left equals k, and remain is target minus the sum of the path.
     */
    static List<List<Integer>> lists(int[] cand, int target, int k) {
        List<List<Integer>> out = new ArrayList<>();
        go(0, target, k, cand, new ArrayList<>(), out);
        return out;
    }

    private static void go(int start, int remain, int left, int[] cand, List<Integer> path, List<List<Integer>> out) {
        if (remain < 0) return;                              // the sum overshoots
        if (left == 0) {                                     // no choices remain
            if (remain == 0) out.add(new ArrayList<>(path)); // store only an exact sum
            return;
        }
        for (int i = start; i < cand.length; i++) {          // same candidate or later
            path.add(cand[i]);                               // choose
            go(i, remain - cand[i], left - 1, cand, path, out);   // reuse allowed, one choice fewer
            path.remove(path.size() - 1);                    // undo
        }
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!lists(new int[] {1, 2, 3}, 5, 3).equals(List.of(List.of(1, 1, 3), List.of(1, 2, 2)))) throw new AssertionError("ex1");
        if (!lists(new int[] {4, 6}, 10, 3).isEmpty()) throw new AssertionError("ex2");
        // Random inputs must match an enumeration of all index tuples, filtered to nondecreasing tuples.
        Random rnd = new Random(1964);
        for (int t = 0; t < 300; t++) {
            int m = 1 + rnd.nextInt(4);
            Set<Integer> s = new LinkedHashSet<>();
            while (s.size() < m) s.add(1 + rnd.nextInt(12));
            int[] c = s.stream().mapToInt(Integer::intValue).toArray();
            int k = 1 + rnd.nextInt(5), target = 1 + rnd.nextInt(30);
            List<List<Integer>> want = new ArrayList<>();
            int total = 1; for (int i = 0; i < k; i++) total *= m;
            for (int code = 0; code < total; code++) {
                int x = code; int[] ix = new int[k];
                for (int i = k - 1; i >= 0; i--) { ix[i] = x % m; x /= m; }
                boolean ok = true; int sum = 0;
                for (int i = 0; i < k; i++) { sum += c[ix[i]]; if (i > 0 && ix[i] < ix[i - 1]) ok = false; }
                if (!ok || sum != target) continue;
                List<Integer> l = new ArrayList<>(); for (int i : ix) l.add(c[i]);
                want.add(l);
            }
            if (!lists(c, target, k).equals(want)) throw new AssertionError("random " + t);
        }
        // A path with remaining sum 0 and choices left is not a result: sum 4 with k = 3 over [2] has no list.
        if (!lists(new int[] {2}, 4, 3).isEmpty()) throw new AssertionError("short path");
        System.out.println("ok");
    }
}
```
