<!-- solutions-for: 04-exchange-reasoning -->
### Solutions For Exchange Reasoning

#### Solution: [Build] Exchange Two Assignments (Author exercise)
<!-- id: gr-exchange-two-assignments -->

**Approach.**
The method finds `r` with a scan, because the supplies are sorted. It then performs the three cases of the exchange step. When demand 0 already uses `r`, nothing changes. When another demand `e` holds `r`, demand 0 takes `r` and `e` takes the supply that demand 0 held, which is valid because that supply is at least `supplies[r]` and `e` fits in `supplies[r]`, as does demand 0 earlier. When `e` held `r` and demand 0 was unserved, `e` becomes unserved, so the count stays equal. When nobody holds `r`, demand 0 takes it. Every case keeps the plan valid and the served count no lower.

After the step, the plan is valid, serves at least as many demands, and demand 0 uses supply `r`.

**Complexity.**
- **Time** is O(n + m), because one scan finds `r` and one scan finds the holder of `r`.
- **Space** is O(1) extra, because the method edits the plan in place.

```java run
import java.util.*;

public final class ExchangeTwoAssignments {
    /**
     * Applies one exchange step and returns the plan.
     * Time: O(n + m). Space: O(1) extra.
     * Invariant: the plan stays valid and serves no fewer demands than before.
     */
    static int[] exchange(int[] demands, int[] supplies, int[] plan) {
        int r = -1;
        for (int j = 0; j < supplies.length; j++) {                   // smallest sufficient supply
            if (supplies[j] >= demands[0]) { r = j; break; }
        }
        if (r < 0 || plan[0] == r) return plan;                       // nothing to exchange
        int holder = -1;
        for (int k = 1; k < plan.length; k++) if (plan[k] == r) holder = k; // who uses supply r
        if (holder >= 0) plan[holder] = plan[0];                      // pass the old supply on, possibly -1
        plan[0] = r;                                                  // demand 0 takes the smallest sufficient supply
        return plan;
    }

    static boolean valid(int[] d, int[] s, int[] plan) {
        boolean[] used = new boolean[s.length];
        for (int k = 0; k < plan.length; k++) {
            if (plan[k] < 0) continue;
            if (used[plan[k]] || s[plan[k]] < d[k]) return false;
            used[plan[k]] = true;
        }
        return true;
    }

    static int served(int[] plan) { int c = 0; for (int x : plan) if (x >= 0) c++; return c; }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!Arrays.equals(exchange(new int[] {3, 5}, new int[] {4, 6, 9}, new int[] {2, 1}), new int[] {0, 1})) throw new AssertionError("ex1");
        if (!Arrays.equals(exchange(new int[] {3, 5}, new int[] {5, 6}, new int[] {-1, 0}), new int[] {0, -1})) throw new AssertionError("ex2");
        // No sufficient supply leaves the plan unchanged.
        if (!Arrays.equals(exchange(new int[] {9}, new int[] {1, 2}, new int[] {-1}), new int[] {-1})) throw new AssertionError("none");
        // Random valid plans must stay valid, serve no fewer demands, and give demand 0 the supply r.
        Random rnd = new Random(2031);
        for (int t = 0; t < 800; t++) {
            int[] d = new int[1 + rnd.nextInt(4)], s = new int[rnd.nextInt(5)];
            for (int k = 0; k < d.length; k++) d[k] = 1 + rnd.nextInt(8);
            for (int k = 0; k < s.length; k++) s[k] = 1 + rnd.nextInt(8);
            Arrays.sort(d); Arrays.sort(s);
            int[] plan = new int[d.length]; Arrays.fill(plan, -1);
            boolean[] used = new boolean[s.length];
            for (int k = 0; k < d.length; k++) {                      // build a random valid plan
                if (rnd.nextBoolean()) continue;
                List<Integer> ok = new ArrayList<>();
                for (int j = 0; j < s.length; j++) if (!used[j] && s[j] >= d[k]) ok.add(j);
                if (!ok.isEmpty()) { plan[k] = ok.get(rnd.nextInt(ok.size())); used[plan[k]] = true; }
            }
            int before = served(plan);
            int[] after = exchange(d, s, plan.clone());
            int r = -1;
            for (int j = 0; j < s.length; j++) if (s[j] >= d[0]) { r = j; break; }
            if (!valid(d, s, after) || served(after) < before) throw new AssertionError("random " + t);
            if (r >= 0 && after[0] != r) throw new AssertionError("pick " + t);
        }
    }
}
```

#### Solution: [Vary] Swap To Earlier Finish (Author exercise)
<!-- id: gr-swap-to-earlier-finish -->

**Approach.**
The method compares the end of `chosen` with the end of the first interval. A later end is rejected at once, because the interval would then reach into the second interval. For an equal or earlier end, the method builds the new schedule and checks only the pair of the new first interval and the second interval, because every other pair is unchanged and was valid before. Since `chosen` ends no later than the old first interval, which ended no later than the start of the second, the check always passes and the method returns the new schedule.

After the call, the result is a valid schedule of the same size whose first interval ends no later than before.

**Complexity.**
- **Time** is O(n) for the copy, and the check itself is O(1).
- **Space** is O(n) for the new array.

```java run
import java.util.*;

public final class SwapToEarlierFinish {
    /**
     * Returns the schedule with the first interval replaced, or the original.
     * Time: O(n). Space: O(n).
     * Invariant: the returned schedule has no overlap and the same size.
     */
    static int[][] swap(int[][] schedule, int[] chosen) {
        if (chosen[1] > schedule[0][1]) return schedule;              // later end: not an exchange
        int[][] changed = schedule.clone();                           // never mutate the input
        changed[0] = chosen;
        if (changed.length > 1 && changed[1][0] < chosen[1]) return schedule; // overlap check of the one new pair
        return changed;
    }

    static boolean valid(int[][] s) {
        for (int k = 1; k < s.length; k++) if (s[k][0] < s[k - 1][1]) return false;
        return true;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!Arrays.deepEquals(swap(new int[][] {{2, 5}, {6, 9}}, new int[] {1, 3}), new int[][] {{1, 3}, {6, 9}})) throw new AssertionError("ex1");
        if (!Arrays.deepEquals(swap(new int[][] {{2, 5}, {6, 9}}, new int[] {1, 7}), new int[][] {{2, 5}, {6, 9}})) throw new AssertionError("ex2");
        // Equal ends are allowed, and the input array is not changed.
        int[][] in = {{2, 5}, {5, 9}};
        if (!Arrays.deepEquals(swap(in, new int[] {0, 5}), new int[][] {{0, 5}, {5, 9}}) || in[0][0] != 2) throw new AssertionError("equal end");
        // Random valid schedules: the result is valid, has equal size, and its first end never grows.
        Random rnd = new Random(2032);
        for (int t = 0; t < 800; t++) {
            int[][] s = new int[1 + rnd.nextInt(5)][];
            int at = rnd.nextInt(5);
            for (int k = 0; k < s.length; k++) { int a = at + rnd.nextInt(3), b = a + 1 + rnd.nextInt(3); s[k] = new int[] {a, b}; at = b; }
            int a = rnd.nextInt(10) - 2, c[] = {a, a + 1 + rnd.nextInt(8)};
            int[][] r = swap(s, c);
            if (!valid(r) || r.length != s.length || r[0][1] > s[0][1]) throw new AssertionError("random " + t);
            boolean should = c[1] <= s[0][1];
            if (should != (r[0] == c)) throw new AssertionError("rule " + t);
        }
    }
}
```

#### Solution: [Boundary] Find A Counterexample (Author exercise)
<!-- id: gr-find-a-counterexample -->

**Approach.**
The method runs the shortest-first rule as stated and counts the accepted intervals. It also computes the largest set with the end-order scan, which the lesson proved correct. The input is a counterexample exactly when the rule's count is smaller. The rule can never exceed the optimum, because it builds a valid set. The boundary cases are an empty input, where both counts are 0, and ties in length, which the tie rule fixes.

After each call, the two counts describe a valid set and a largest valid set.

**Complexity.**
- **Time** is O(n^2), because the rule tests each interval against the accepted ones, and the scan adds O(n log n).
- **Space** is O(n) for the sorted copies and the accepted list.

```java run
import java.util.*;

public final class FindACounterexample {
    /**
     * Returns true when shortest-first accepts fewer intervals than the optimum.
     * Time: O(n^2). Space: O(n).
     * Invariant: both counts come from valid sets, and the end-order count is the optimum.
     */
    static boolean fails(int[][] iv) {
        int[][] byLen = iv.clone();
        Arrays.sort(byLen, (a, b) -> a[1] - a[0] != b[1] - b[0] ? Integer.compare(a[1] - a[0], b[1] - b[0]) : Integer.compare(a[0], b[0])); // length, then start
        List<int[]> kept = new ArrayList<>();
        for (int[] m : byLen) {                                       // the rule under test
            boolean clash = false;
            for (int[] k : kept) if (m[0] < k[1] && k[0] < m[1]) clash = true;
            if (!clash) kept.add(m);
        }
        int[][] byEnd = iv.clone();
        Arrays.sort(byEnd, (a, b) -> Integer.compare(a[1], b[1]));    // the proven rule
        int best = 0, lastEnd = Integer.MIN_VALUE;
        for (int[] m : byEnd) if (m[0] >= lastEnd) { best++; lastEnd = m[1]; }
        return kept.size() < best;
    }

    static int brute(int[][] m) {
        int best = 0;
        for (int mask = 0; mask < (1 << m.length); mask++) {
            boolean ok = true;
            for (int a = 0; a < m.length && ok; a++) {
                if ((mask >> a & 1) == 0) continue;
                for (int b = a + 1; b < m.length; b++) if ((mask >> b & 1) != 0 && m[a][0] < m[b][1] && m[b][0] < m[a][1]) { ok = false; break; }
            }
            if (ok) best = Math.max(best, Integer.bitCount(mask));
        }
        return best;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!fails(new int[][] {{0, 4}, {3, 5}, {4, 8}})) throw new AssertionError("ex1");
        if (fails(new int[][] {{1, 2}, {3, 4}})) throw new AssertionError("ex2");
        if (fails(new int[0][])) throw new AssertionError("empty");
        // Random inputs: the optimum used by the method must equal exhaustive search, so fails() is exact.
        Random rnd = new Random(2033);
        int found = 0;
        for (int t = 0; t < 1500; t++) {
            int[][] m = new int[rnd.nextInt(8)][];
            for (int k = 0; k < m.length; k++) { int s = rnd.nextInt(10); m[k] = new int[] {s, s + 1 + rnd.nextInt(6)}; }
            int[][] byEnd = m.clone();
            Arrays.sort(byEnd, (a, b) -> Integer.compare(a[1], b[1]));
            int best = 0, last = Integer.MIN_VALUE;
            for (int[] x : byEnd) if (x[0] >= last) { best++; last = x[1]; }
            if (best != brute(m)) throw new AssertionError("optimum " + t);
            if (fails(m)) found++;
        }
        if (found == 0) throw new AssertionError("no counterexample appeared");
    }
}
```

#### Solution: [Recognize] Present A Greedy Proof (Author exercise)
<!-- id: gr-present-a-greedy-proof -->

**Approach.**
For rule 1 the exchange argument of the lesson proves the answer is always true. Take any largest set `S`. If the pick `a` is in `S`, nothing changes. Otherwise the first interval `b` of `S` in end order ends no earlier than `a`, so replacing `b` with `a` keeps every later interval valid and keeps the size. Rules 2 and 3 fail this argument. The pick of rule 2 can end very late and overlap many intervals, and the pick of rule 3 can sit between two long intervals, so the replacement removes more than it adds. The method does not rely on a proof for those rules. It applies the definition: it finds the pick by the stated order, enumerates all subsets to find the largest size, and checks whether some largest subset contains the pick.

After the call, the answer equals the existence of a largest set that contains the pick.

**Complexity.**
- **Time** is O(2^n * n^2), because the method tests every subset against every pair, which the limit of 12 intervals allows.
- **Space** is O(1) extra, because the method keeps counters.

```java run
import java.util.*;

public final class PresentAGreedyProof {
    /**
     * Returns true when the pick of the rule belongs to at least one largest compatible set.
     * Time: O(2^n * n^2). Space: O(1) extra.
     * Invariant: best is the largest valid subset size seen, and withPick is the largest size among subsets containing the pick.
     */
    static boolean pickIsSafe(int[][] iv, int rule) {
        int pick = 0;
        for (int i = 1; i < iv.length; i++) {                         // choose by the stated order
            if (better(iv, i, pick, rule)) pick = i;
        }
        int best = 0, withPick = -1;
        for (int mask = 0; mask < (1 << iv.length); mask++) {         // every subset
            boolean ok = true;
            for (int a = 0; a < iv.length && ok; a++) {
                if ((mask >> a & 1) == 0) continue;
                for (int b = a + 1; b < iv.length; b++) if ((mask >> b & 1) != 0 && iv[a][0] < iv[b][1] && iv[b][0] < iv[a][1]) { ok = false; break; }
            }
            if (!ok) continue;
            int size = Integer.bitCount(mask);
            best = Math.max(best, size);
            if ((mask >> pick & 1) != 0) withPick = Math.max(withPick, size);
        }
        return withPick == best;                                      // some largest set contains the pick
    }

    static boolean better(int[][] iv, int x, int y, int rule) {
        int[] a = iv[x], b = iv[y];
        int ka = rule == 1 ? a[1] : rule == 2 ? a[0] : a[1] - a[0];
        int kb = rule == 1 ? b[1] : rule == 2 ? b[0] : b[1] - b[0];
        if (ka != kb) return ka < kb;
        if (rule == 2 && a[1] != b[1]) return a[1] < b[1];            // rule 2: tie by end
        if (a[0] != b[0]) return a[0] < b[0];                         // otherwise tie by start
        return false;                                                 // equal: the earlier position stays
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!pickIsSafe(new int[][] {{0, 4}, {3, 5}, {4, 8}}, 1)) throw new AssertionError("ex1");
        if (pickIsSafe(new int[][] {{0, 4}, {3, 5}, {4, 8}}, 3)) throw new AssertionError("ex2");
        // The proof of rule 1: it is always safe on random inputs.
        Random rnd = new Random(2034);
        boolean sawUnsafe = false;
        for (int t = 0; t < 600; t++) {
            int[][] m = new int[1 + rnd.nextInt(8)][];
            for (int k = 0; k < m.length; k++) { int s = rnd.nextInt(10); m[k] = new int[] {s, s + 1 + rnd.nextInt(6)}; }
            if (!pickIsSafe(m, 1)) throw new AssertionError("rule 1 failed " + t);
            if (!pickIsSafe(m, 2) || !pickIsSafe(m, 3)) sawUnsafe = true;
        }
        if (!sawUnsafe) throw new AssertionError("rules 2 and 3 never failed");
    }
}
```
