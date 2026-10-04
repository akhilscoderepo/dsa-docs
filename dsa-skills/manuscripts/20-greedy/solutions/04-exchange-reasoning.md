<!-- solutions-for: 20-greedy -->
### Exchange Reasoning

#### Solution: [Build] Exchange Two Assignments (Author exercise)
<!-- id: gr-exchange-two-assignments -->

**Approach.** Find the party `p` with the smallest need and the room `s` with the smallest capacity that fits it, breaking ties by the lower index in both searches. If `s` does not exist, nothing changes. Otherwise give `s` to `p`. The party that held `s`, if any, takes the old room of `p`, which may be none. That old room fits the displaced party, because the old room fits `p`, so it is at least as large as `s`, and `s` fit the displaced party. The assertions check both examples. Every legal assignment of random small instances is then generated and exchanged, and each result must be legal, must not house fewer parties, must give `p` the room `s`, and must leave every party other than `p` and the displaced one unchanged.

**Complexity.** Finding `p`, `s` and the holder takes three linear scans, so the step costs O(n + m); the harness enumerates assignments exhaustively.

```java run
import java.util.Arrays;
import java.util.Random;

public final class ExchangeTwoAssignments {
    static int[] exchange(int[] need, int[] beds, int[] assign) {
        int[] out = assign.clone();
        if (need.length == 0) return out;
        int p = 0;
        for (int i = 1; i < need.length; i++) if (need[i] < need[p]) p = i;
        int s = -1;
        for (int r = 0; r < beds.length; r++) {
            if (beds[r] >= need[p] && (s == -1 || beds[r] < beds[s])) s = r;
        }
        if (s == -1) return out;
        int old = assign[p];
        if (old == s) return out;
        for (int q = 0; q < out.length; q++) if (out[q] == s) out[q] = old;
        out[p] = s;
        return out;
    }

    static boolean legal(int[] need, int[] beds, int[] assign) {
        boolean[] used = new boolean[beds.length];
        for (int i = 0; i < need.length; i++) {
            if (assign[i] == -1) continue;
            if (used[assign[i]] || beds[assign[i]] < need[i]) return false;
            used[assign[i]] = true;
        }
        return true;
    }

    static int housed(int[] a) {
        int c = 0;
        for (int v : a) if (v != -1) c++;
        return c;
    }

    static void forEachAssignment(int[] need, int[] beds, int idx, int[] cur, boolean[] used, java.util.function.Consumer<int[]> visit) {
        if (idx == need.length) { visit.accept(cur.clone()); return; }
        cur[idx] = -1;
        forEachAssignment(need, beds, idx + 1, cur, used, visit);
        for (int r = 0; r < beds.length; r++) {
            if (!used[r] && beds[r] >= need[idx]) {
                used[r] = true; cur[idx] = r;
                forEachAssignment(need, beds, idx + 1, cur, used, visit);
                used[r] = false; cur[idx] = -1;
            }
        }
    }

    public static void main(String[] args) {
        if (!Arrays.equals(exchange(new int[]{2, 5}, new int[]{9, 2, 6}, new int[]{0, 2}), new int[]{1, 2})) throw new AssertionError("example 1");
        if (!Arrays.equals(exchange(new int[]{3, 4}, new int[]{4, 3}, new int[]{0, 1}), new int[]{1, 0})) throw new AssertionError("example 2");
        int[] kept = {0, 2};
        exchange(new int[]{2, 5}, new int[]{9, 2, 6}, kept);
        if (!Arrays.equals(kept, new int[]{0, 2})) throw new AssertionError("input assignment was modified");
        if (!Arrays.equals(exchange(new int[]{9}, new int[]{3}, new int[]{-1}), new int[]{-1})) throw new AssertionError("no fitting room leaves it unchanged");

        Random rnd = new Random(2401);
        int[] checked = {0};
        for (int t = 0; t < 300; t++) {
            int n = 1 + rnd.nextInt(4), m = rnd.nextInt(5);
            int[] need = new int[n], beds = new int[m];
            for (int i = 0; i < n; i++) need[i] = 1 + rnd.nextInt(6);
            for (int i = 0; i < m; i++) beds[i] = 1 + rnd.nextInt(6);
            forEachAssignment(need, beds, 0, new int[n], new boolean[m], a -> {
                int[] b = exchange(need, beds, a);
                if (!legal(need, beds, b)) throw new AssertionError("exchange produced an illegal assignment");
                if (housed(b) < housed(a)) throw new AssertionError("exchange housed fewer parties");
                int p = 0;
                for (int i = 1; i < n; i++) if (need[i] < need[p]) p = i;
                int s = -1;
                for (int r = 0; r < m; r++) if (beds[r] >= need[p] && (s == -1 || beds[r] < beds[s])) s = r;
                if (s != -1 && b[p] != s) throw new AssertionError("the smallest party must hold the smallest fitting room");
                for (int i = 0; i < n; i++) if (i != p && b[i] != a[i] && a[i] != s) throw new AssertionError("an unrelated party changed");
                checked[0]++;
            });
        }
        if (checked[0] < 1000) throw new AssertionError("too few assignments were checked");
    }
}
```

#### Solution: [Vary] Swap To Earlier Finish (Author exercise)
<!-- id: gr-swap-to-earlier-finish -->

**Approach.** Find `g`, the interval that ends earliest overall, and `f`, the schedule member that ends earliest. If they are the same, only sort the indexes. Otherwise remove `f` and insert `g`. The new interval cannot clash with the other members, since each of them starts at or after the end of `f`, and `f` ends no earlier than `g`. The assertions check both examples. Every conflict-free subset of random small calendars is then exchanged, and the result must be conflict-free, must keep the size, and must contain `g`. Applied to a largest subset, the result is again a largest subset.

**Complexity.** Two scans and a sort of the schedule give O(n + k log k) for k scheduled intervals; the harness enumerates all subsets.

```java run
import java.util.Arrays;
import java.util.Random;

public final class SwapToEarlierFinish {
    static int[] swap(int[][] iv, int[] schedule) {
        if (schedule.length == 0) return schedule.clone();
        int g = 0;
        for (int i = 1; i < iv.length; i++) if (iv[i][1] < iv[g][1]) g = i;
        int f = schedule[0];
        for (int idx : schedule) {
            if (iv[idx][1] < iv[f][1] || (iv[idx][1] == iv[f][1] && idx < f)) f = idx;
        }
        Integer[] boxed = new Integer[schedule.length];
        for (int i = 0; i < boxed.length; i++) boxed[i] = schedule[i] == f ? g : schedule[i];
        Arrays.sort(boxed, (a, b) -> iv[a][0] != iv[b][0] ? Integer.compare(iv[a][0], iv[b][0]) : Integer.compare(iv[a][1], iv[b][1]));
        int[] out = new int[boxed.length];
        for (int i = 0; i < out.length; i++) out[i] = boxed[i];
        return out;
    }

    static boolean conflictFree(int[][] iv, int[] set) {
        for (int i = 0; i < set.length; i++)
            for (int j = i + 1; j < set.length; j++)
                if (set[i] == set[j] || (iv[set[i]][0] < iv[set[j]][1] && iv[set[j]][0] < iv[set[i]][1])) return false;
        return true;
    }

    public static void main(String[] args) {
        int[][] a = {{0, 6}, {1, 3}, {4, 8}, {6, 9}};
        if (!Arrays.equals(swap(a, new int[]{0, 3}), new int[]{1, 3})) throw new AssertionError("example 1");
        int[][] b = {{0, 2}, {2, 5}, {3, 4}};
        if (!Arrays.equals(swap(b, new int[]{0, 1}), new int[]{0, 1})) throw new AssertionError("example 2");
        if (swap(a, new int[0]).length != 0) throw new AssertionError("an empty schedule stays empty");

        Random rnd = new Random(2402);
        int checked = 0;
        for (int t = 0; t < 600; t++) {
            int n = 1 + rnd.nextInt(8);
            int[][] iv = new int[n][];
            for (int i = 0; i < n; i++) {
                int s = rnd.nextInt(10);
                iv[i] = new int[]{s, s + 1 + rnd.nextInt(5)};
            }
            int g = 0;
            for (int i = 1; i < n; i++) if (iv[i][1] < iv[g][1]) g = i;
            int bestSize = 0;
            for (int mask = 0; mask < (1 << n); mask++) {
                int[] set = new int[Integer.bitCount(mask)];
                for (int i = 0, k = 0; i < n; i++) if ((mask >> i & 1) == 1) set[k++] = i;
                if (conflictFree(iv, set)) bestSize = Math.max(bestSize, set.length);
            }
            for (int mask = 1; mask < (1 << n); mask++) {
                int[] set = new int[Integer.bitCount(mask)];
                for (int i = 0, k = 0; i < n; i++) if ((mask >> i & 1) == 1) set[k++] = i;
                if (!conflictFree(iv, set)) continue;
                int[] out = swap(iv, set);
                if (out.length != set.length) throw new AssertionError("size changed");
                if (!conflictFree(iv, out)) throw new AssertionError("swap produced a clash on " + Arrays.deepToString(iv));
                boolean has = false;
                for (int v : out) if (v == g) has = true;
                if (!has) throw new AssertionError("the earliest finish must be in the result");
                if (set.length == bestSize && out.length != bestSize) throw new AssertionError("a best schedule got worse");
                checked++;
            }
        }
        if (checked < 1000) throw new AssertionError("too few schedules were checked");
    }
}
```

#### Solution: [Boundary] Find A Counterexample (Author exercise)
<!-- id: gr-find-counterexample -->

**Approach.** List every span with endpoints from 0 to `maxCoord`, in lexicographic order. For each size from 1 to 6, walk the combinations of that size in lexicographic order, skip any combination whose lengths are not all different, and run shortest-first against the earliest-finish rule, which is known to be best. The first combination where shortest-first takes fewer intervals is returned. The assertions check both examples, confirm that the earliest-finish rule agrees with an exhaustive subset search on the returned set, and check that shortest-first never beats the best answer on any distinct-length combination in the range.

**Complexity.** For maxCoord = 7 there are 28 spans, so the search looks at fewer than 600000 combinations, each judged in near-linear time; the work is bounded by the constants in the constraints.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public final class FindCounterexample {
    static int shortestFirst(int[][] set) {
        Integer[] order = new Integer[set.length];
        for (int i = 0; i < order.length; i++) order[i] = i;
        Arrays.sort(order, (x, y) -> {
            int lx = set[x][1] - set[x][0], ly = set[y][1] - set[y][0];
            return lx != ly ? Integer.compare(lx, ly) : Integer.compare(set[x][0], set[y][0]);
        });
        List<int[]> kept = new ArrayList<>();
        for (int idx : order) {
            int[] a = set[idx];
            boolean clash = false;
            for (int[] k : kept) if (a[0] < k[1] && k[0] < a[1]) clash = true;
            if (!clash) kept.add(a);
        }
        return kept.size();
    }

    static int earliestFinish(int[][] set) {
        int[][] s = set.clone();
        Arrays.sort(s, (x, y) -> Integer.compare(x[1], y[1]));
        int kept = 0, free = Integer.MIN_VALUE;
        for (int[] a : s) if (a[0] >= free) { kept++; free = a[1]; }
        return kept;
    }

    static int bruteBest(int[][] set) {
        int n = set.length, best = 0;
        for (int mask = 0; mask < (1 << n); mask++) {
            boolean ok = true;
            for (int i = 0; i < n && ok; i++) for (int j = i + 1; j < n && ok; j++)
                if ((mask >> i & 1) == 1 && (mask >> j & 1) == 1 && set[i][0] < set[j][1] && set[j][0] < set[i][1]) ok = false;
            if (ok) best = Math.max(best, Integer.bitCount(mask));
        }
        return best;
    }

    static boolean distinctLengths(int[][] set) {
        for (int i = 0; i < set.length; i++)
            for (int j = i + 1; j < set.length; j++)
                if (set[i][1] - set[i][0] == set[j][1] - set[j][0]) return false;
        return true;
    }

    static int[][] pool(int maxCoord) {
        List<int[]> list = new ArrayList<>();
        for (int a = 0; a <= maxCoord; a++) for (int b = a + 1; b <= maxCoord; b++) list.add(new int[]{a, b});
        return list.toArray(new int[0][]);
    }

    static int[][] found;
    static boolean verifyAll;

    static void walk(int[][] pool, int size, int from, int[][] cur, int depth) {
        if (found != null && !verifyAll) return;
        if (depth == size) {
            if (!distinctLengths(cur)) return;
            int sf = shortestFirst(cur);
            if (verifyAll && sf > earliestFinish(cur)) throw new AssertionError("shortest-first cannot beat the best answer");
            if (sf < earliestFinish(cur) && found == null) {
                found = new int[size][];
                for (int i = 0; i < size; i++) found[i] = cur[i].clone();
            }
            return;
        }
        for (int i = from; i < pool.length; i++) {
            cur[depth] = pool[i];
            walk(pool, size, i + 1, cur, depth + 1);
            if (found != null && !verifyAll) return;
        }
    }

    static int[][] search(int maxCoord, boolean verify) {
        found = null;
        verifyAll = verify;
        int[][] pool = pool(maxCoord);
        for (int size = 1; size <= 6 && (found == null || verify); size++) walk(pool, size, 0, new int[size][], 0);
        return found == null ? new int[0][] : found;
    }

    public static void main(String[] args) {
        int[][] ex1 = search(7, false);
        if (!Arrays.deepEquals(ex1, new int[][]{{0, 3}, {2, 4}, {3, 7}})) throw new AssertionError("example 1: " + Arrays.deepToString(ex1));
        if (search(6, false).length != 0) throw new AssertionError("example 2");
        if (shortestFirst(ex1) != 1 || earliestFinish(ex1) != 2 || bruteBest(ex1) != 2) throw new AssertionError("counts on the counterexample");
        if (search(4, false).length != 0) throw new AssertionError("a tiny range has no counterexample");
        int[][] check = search(6, true);
        if (check.length != 0) throw new AssertionError("verification pass must also find nothing in range 6");
        int[][][] samples = {{{0, 3}, {3, 7}}, {{0, 2}, {1, 4}, {5, 6}}, {{0, 5}, {1, 2}, {2, 4}}};
        for (int[][] s : samples) if (earliestFinish(s) != bruteBest(s)) throw new AssertionError("earliest finish must be best");
    }
}
```

#### Solution: [Recognize] Present A Greedy Proof (Author exercise)
<!-- id: gr-present-greedy-proof -->

**Approach.** Locate the first position `k` that holds a job with the smallest duration, and swap it with position 0. The swap cannot hurt: with `n` jobs, a job in position `i` (counting from 0) contributes its duration `n - i` times, so trading a longer job at position 0 for a shorter job at position `k` changes the total by exactly the duration difference multiplied by `k`, which is not positive. The permutation property is preserved, and what remains is a sequence of `n - 1` jobs. The returned numbers are the total before, the total after, and the total of the tail. The assertions check the examples, the identity that the total after equals `n` times the first duration plus the tail total, the difference formula, and that repeating the step on the tail reaches the minimum over all permutations on random inputs.

**Complexity.** One step scans the jobs once and sums them three times, so it costs O(n); the harness tries all permutations of at most seven jobs.

```java run
import java.util.Arrays;
import java.util.Random;

public final class PresentGreedyProof {
    static long total(int[] d, int[] order, int from) {
        long clock = 0, sum = 0;
        for (int i = from; i < order.length; i++) { clock += d[order[i]]; sum += clock; }
        return sum;
    }

    static long[] step(int[] d, int[] order) {
        int k = 0;
        for (int i = 1; i < order.length; i++) if (d[order[i]] < d[order[k]]) k = i;
        int[] after = order.clone();
        int tmp = after[0]; after[0] = after[k]; after[k] = tmp;
        return new long[]{total(d, order, 0), total(d, after, 0), total(d, after, 1)};
    }

    static long bruteMin(int[] d, int[] order, int idx) {
        if (idx == order.length) return total(d, order, 0);
        long best = Long.MAX_VALUE;
        for (int i = idx; i < order.length; i++) {
            int t = order[idx]; order[idx] = order[i]; order[i] = t;
            best = Math.min(best, bruteMin(d, order, idx + 1));
            t = order[idx]; order[idx] = order[i]; order[i] = t;
        }
        return best;
    }

    public static void main(String[] args) {
        if (!Arrays.equals(step(new int[]{5, 2, 8, 1}, new int[]{0, 1, 2, 3}), new long[]{43, 31, 27})) throw new AssertionError("example 1");
        if (!Arrays.equals(step(new int[]{3, 3, 3}, new int[]{2, 0, 1}), new long[]{18, 18, 9})) throw new AssertionError("example 2");
        long big = 1_000_000_000L;
        long[] huge = step(new int[]{1000000000, 1000000000, 1}, new int[]{0, 1, 2});
        if (huge[0] != big + 2 * big + (2 * big + 1)) throw new AssertionError("a total above the int range needs long");
        if (huge[0] <= Integer.MAX_VALUE) throw new AssertionError("the total must exceed the int range");

        Random rnd = new Random(2404);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(7);
            int[] d = new int[n];
            for (int i = 0; i < n; i++) d[i] = rnd.nextInt(3) == 0 ? 1 + rnd.nextInt(1000000000) : 1 + rnd.nextInt(9);
            Integer[] boxed = new Integer[n];
            for (int i = 0; i < n; i++) boxed[i] = i;
            java.util.Collections.shuffle(Arrays.asList(boxed), rnd);
            int[] order = new int[n];
            for (int i = 0; i < n; i++) order[i] = boxed[i];
            long[] r = step(d, order);
            if (r[1] > r[0]) throw new AssertionError("the swap made the total worse");
            int k = 0;
            for (int i = 1; i < n; i++) if (d[order[i]] < d[order[k]]) k = i;
            long gain = (long) (d[order[0]] - d[order[k]]) * k;
            if (r[0] - r[1] != gain) throw new AssertionError("difference formula fails");
            int[] after = order.clone();
            int tmp = after[0]; after[0] = after[k]; after[k] = tmp;
            if (r[1] != (long) n * d[after[0]] + r[2]) throw new AssertionError("identity with the remainder fails");
            int[] cur = order.clone();
            for (int i = 0; i < n; i++) {
                int best = i;
                for (int j = i + 1; j < n; j++) if (d[cur[j]] < d[cur[best]]) best = j;
                int x = cur[i]; cur[i] = cur[best]; cur[best] = x;
            }
            if (total(d, cur, 0) != bruteMin(d, order.clone(), 0)) throw new AssertionError("repeating the exchange must reach the minimum");
        }
    }
}
```
