<!-- solutions-for: 08-proof-based-pruning -->
### Proof-Based Pruning

#### Solution: [Build] Positive Remaining Sum (Author exercise)
<!-- id: bt-positive-budget -->

**Approach.** Each call counts itself and loops from `start`, leaving at the first value above the remaining budget, which is justified because the values are positive and ascending. A call is entered only when its load already fits, so every call is one counted subset and `calls` must equal `count`, a property the harness asserts on every random input. A second version without the exit enters every branch and checks the budget only at the end, and its call count is exactly 2^n, which shows what the proof saves. The oracle weighs every mask.

**Complexity.** The number of calls equals the number of subsets within the budget, which is at most 2^n and often far smaller, with a copy-free count and a stack of up to n frames.

```java run
import java.util.Arrays;
import java.util.Random;

public final class PositiveBudget {
    static long calls;

    static long count(int[] v, int start, long room) {
        calls++;
        long total = 1;
        for (int i = start; i < v.length; i++) {
            if (v[i] > room) break;
            total += count(v, i + 1, room - v[i]);
        }
        return total;
    }

    static long countUnpruned(int[] v, int start, long used, long budget) {
        calls++;
        long total = used <= budget ? 1 : 0;
        for (int i = start; i < v.length; i++) total += countUnpruned(v, i + 1, used + v[i], budget);
        return total;
    }

    static long[] solve(int[] v, int budget) {
        calls = 0;
        long c = count(v, 0, budget);
        return new long[] {c, calls};
    }

    static long oracle(int[] v, int budget) {
        long c = 0;
        for (int m = 0; m < (1 << v.length); m++) {
            long s = 0;
            for (int i = 0; i < v.length; i++) if ((m >> i & 1) == 1) s += v[i];
            if (s <= budget) c++;
        }
        return c;
    }

    public static void main(String[] args) {
        if (!Arrays.equals(solve(new int[] {2, 3, 4}, 6), new long[] {6, 6})) throw new AssertionError("example 1");
        if (!Arrays.equals(solve(new int[] {5, 6}, 4), new long[] {1, 1})) throw new AssertionError("example 2");
        if (!Arrays.equals(solve(new int[0], 0), new long[] {1, 1})) throw new AssertionError("no values");
        Random rnd = new Random(19801);
        for (int t = 0; t < 3000; t++) {
            int n = rnd.nextInt(13);
            int[] v = new int[n];
            for (int i = 0; i < n; i++) v[i] = 1 + rnd.nextInt(30);
            Arrays.sort(v);
            int budget = rnd.nextInt(61);
            long[] got = solve(v, budget);
            if (got[0] != oracle(v, budget)) throw new AssertionError("count differs, budget " + budget);
            if (got[0] != got[1]) throw new AssertionError("every call entered must be one counted subset");
            calls = 0;
            if (countUnpruned(v, 0, 0, budget) != got[0]) throw new AssertionError("unpruned count differs");
            if (calls != (1L << n)) throw new AssertionError("the unpruned search enters 2^n calls");
        }
    }
}
```

#### Solution: [Vary] Remaining-Slots Bound (Author exercise)
<!-- id: bt-nonadjacent-slots -->

**Approach.** After a pick at position `i` the next pick must be at `i + 2` or later, so a call that needs `need` more picks has to find room for them and for the `need - 1` gaps between them, which is `2 * need - 1` positions. The loop therefore stops at `n - (2 * need - 1)`. The harness counts dead calls, meaning calls that return no result, and asserts there are none with this bound, which is the property that makes the bound a proof and not a guess. A looser bound, the end of the row, produces dead calls on the first example's shape. The oracle takes the masks with `k` set bits and no two adjacent bits and sorts the position lists.

**Complexity.** Each call leads to at least one answer, so the work is within a factor of k of the number of answers, which is C(n - k + 1, k).

```java run
import java.util.ArrayList;
import java.util.List;

public final class NonadjacentSlots {
    static int dead;

    static int pick(int n, int k, int start, boolean tight, List<Integer> path, List<List<Integer>> out) {
        int need = k - path.size();
        if (need == 0) {
            out.add(new ArrayList<>(path));
            return 1;
        }
        int hi = tight ? n - (2 * need - 1) : n - 1;
        int found = 0;
        for (int i = start; i <= hi; i++) {
            path.add(i);
            found += pick(n, k, i + 2, tight, path, out);
            path.remove(path.size() - 1);
        }
        if (found == 0) dead++;
        return found;
    }

    static List<List<Integer>> solve(int n, int k, boolean tight) {
        dead = 0;
        List<List<Integer>> out = new ArrayList<>();
        pick(n, k, 0, tight, new ArrayList<>(), out);
        return out;
    }

    static List<List<Integer>> oracle(int n, int k) {
        List<List<Integer>> out = new ArrayList<>();
        for (int m = 0; m < (1 << n); m++) {
            if (Integer.bitCount(m) != k || (m & (m >> 1)) != 0) continue;
            List<Integer> s = new ArrayList<>();
            for (int i = 0; i < n; i++) if ((m >> i & 1) == 1) s.add(i);
            out.add(s);
        }
        out.sort((a, b) -> {
            for (int i = 0; i < Math.min(a.size(), b.size()); i++) if (!a.get(i).equals(b.get(i))) return a.get(i) - b.get(i);
            return a.size() - b.size();
        });
        return out;
    }

    public static void main(String[] args) {
        List<List<Integer>> one = List.of(List.of(0, 2), List.of(0, 3), List.of(0, 4), List.of(1, 3), List.of(1, 4), List.of(2, 4));
        if (!solve(5, 2, true).equals(one)) throw new AssertionError("example 1");
        if (!solve(4, 3, true).isEmpty()) throw new AssertionError("example 2");
        List<List<Integer>> zero = solve(6, 0, true);
        if (zero.size() != 1 || !zero.get(0).isEmpty()) throw new AssertionError("k = 0");
        boolean looseHadDead = false;
        for (int n = 1; n <= 12; n++) {
            for (int k = 0; k <= 8; k++) {
                List<List<Integer>> got = solve(n, k, true);
                int deadTight = dead;
                if (!got.equals(oracle(n, k))) throw new AssertionError("differs at n=" + n + ", k=" + k);
                if (k > 0 && n >= 2 * k - 1 && deadTight != 0) throw new AssertionError("a tight bound must never enter a dead call");
                List<List<Integer>> loose = solve(n, k, false);
                if (!loose.equals(got)) throw new AssertionError("the loose bound finds the same answers");
                if (k >= 2 && dead > 0) looseHadDead = true;
            }
        }
        if (!looseHadDead) throw new AssertionError("a loose bound must enter dead calls somewhere");
    }
}
```

#### Solution: [Boundary] Negative Values Break Sum Pruning (Author exercise)
<!-- id: bt-negative-breaks-prune -->

**Approach.** The search decides each position as taken or left. Before deciding position `i` it checks the sum still needed against the lowest and highest sums the unused positions can give, which are the totals of their negative and of their positive values. If the need lies outside that interval, nothing below can reach the target, so the branch is abandoned, and at the end of the row the interval is just zero, so a surviving call counts one. Sums use `long`. The harness also runs the rule that stops when the partial sum exceeds the target and asserts it counts too few on both examples, and it confirms the overflow fact that motivates `long`. The oracle weighs all masks.

**Complexity.** At most 2^(n+1) - 1 calls, and typically far fewer, since out-of-range needs are cut at once.

```java run
import java.util.Random;

public final class NegativeBreaksPrune {
    static long solve(int[] v, long target) {
        int n = v.length;
        long[] low = new long[n + 1], high = new long[n + 1];
        for (int i = n - 1; i >= 0; i--) {
            low[i] = low[i + 1] + Math.min(0, v[i]);
            high[i] = high[i + 1] + Math.max(0, v[i]);
        }
        return go(v, 0, target, low, high);
    }

    static long go(int[] v, int i, long need, long[] low, long[] high) {
        if (need < low[i] || need > high[i]) return 0;
        if (i == v.length) return 1;
        return go(v, i + 1, need, low, high) + go(v, i + 1, need - v[i], low, high);
    }

    static long careless(int[] v, int i, long sum, long target) {
        if (sum > target) return 0;
        if (i == v.length) return sum == target ? 1 : 0;
        return careless(v, i + 1, sum, target) + careless(v, i + 1, sum + v[i], target);
    }

    static long oracle(int[] v, long target) {
        long c = 0;
        for (int m = 0; m < (1 << v.length); m++) {
            long s = 0;
            for (int i = 0; i < v.length; i++) if ((m >> i & 1) == 1) s += v[i];
            if (s == target) c++;
        }
        return c;
    }

    public static void main(String[] args) {
        if (solve(new int[] {5, -5}, 0) != 2) throw new AssertionError("example 1");
        if (solve(new int[] {3, -2, 4, -1}, 2) != 2) throw new AssertionError("example 2");
        if (careless(new int[] {5, -5}, 0, 0, 0) == 2) throw new AssertionError("the careless rule must miss [5, -5]");
        if (careless(new int[] {3, -2, 4, -1}, 0, 0, 2) == 2) throw new AssertionError("the careless rule must miss [3, -1]");
        if (solve(new int[0], 0) != 1 || solve(new int[0], 4) != 0) throw new AssertionError("empty input");
        if (Integer.MAX_VALUE + 1 != Integer.MIN_VALUE) throw new AssertionError("int sums wrap around");
        Random rnd = new Random(19802);
        for (int t = 0; t < 4000; t++) {
            int n = rnd.nextInt(13);
            int[] v = new int[n];
            for (int i = 0; i < n; i++) v[i] = rnd.nextInt(19) - 9;
            int target = rnd.nextInt(61) - 30;
            if (solve(v, target) != oracle(v, target)) throw new AssertionError("differs for target " + target);
        }
    }
}
```

#### Solution: [Recognize] N-Queens Rejections (LeetCode 51)
<!-- id: bt-queens-rejected -->

**Approach.** Rows are filled from the top and each row tries its columns from left to right. Three boolean arrays record occupied columns, and the two kinds of diagonal, indexed by `row + col` and by `row - col + n - 1`. A square is refused and counted when any of the three is set. Otherwise the three flags are set, the next row is filled, and the same three flags are cleared. A conflict between two queens cannot be repaired by later rows, because queens are never moved, which is what makes the refusal a proof and not a guess. The oracle redoes the search while checking conflicts by scanning every earlier queen, so it shares no flags with the solution. Known counts of 1, 0, 0, 2, 10, 4, 40 and 92 solutions for boards 1 to 8 are asserted too.

**Complexity.** Exponential in n in the worst case, and well below n^n in practice, since conflicting squares are refused before any deeper row is visited.

```java run
public final class QueensRejected {
    static long solutions, rejected;

    static void place(int n, int row, boolean[] col, boolean[] d1, boolean[] d2) {
        if (row == n) {
            solutions++;
            return;
        }
        for (int c = 0; c < n; c++) {
            if (col[c] || d1[row + c] || d2[row - c + n - 1]) {
                rejected++;
                continue;
            }
            col[c] = d1[row + c] = d2[row - c + n - 1] = true;
            place(n, row + 1, col, d1, d2);
            col[c] = d1[row + c] = d2[row - c + n - 1] = false;
        }
    }

    static long[] solve(int n) {
        solutions = 0;
        rejected = 0;
        place(n, 0, new boolean[n], new boolean[2 * n], new boolean[2 * n]);
        return new long[] {solutions, rejected};
    }

    static long oSol, oRej;

    static void scan(int n, int row, int[] at) {
        if (row == n) {
            oSol++;
            return;
        }
        for (int c = 0; c < n; c++) {
            boolean clash = false;
            for (int r = 0; r < row; r++) {
                if (at[r] == c || Math.abs(at[r] - c) == row - r) { clash = true; break; }
            }
            if (clash) {
                oRej++;
                continue;
            }
            at[row] = c;
            scan(n, row + 1, at);
        }
    }

    static long[] oracle(int n) {
        oSol = 0;
        oRej = 0;
        scan(n, 0, new int[n]);
        return new long[] {oSol, oRej};
    }

    public static void main(String[] args) {
        long[] four = solve(4), three = solve(3);
        if (four[0] != 2 || four[1] != 44) throw new AssertionError("example 1: " + four[0] + "," + four[1]);
        if (three[0] != 0 || three[1] != 13) throw new AssertionError("example 2: " + three[0] + "," + three[1]);
        long[] known = {1, 0, 0, 2, 10, 4, 40, 92};
        for (int n = 1; n <= 8; n++) {
            long[] a = solve(n), b = oracle(n);
            if (a[0] != b[0] || a[1] != b[1]) throw new AssertionError("differs at n=" + n);
            if (a[0] != known[n - 1]) throw new AssertionError("known solution count at n=" + n);
        }
    }
}
```
