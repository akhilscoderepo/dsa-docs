<!-- solutions-for: 05-query-planning -->
### Solutions For Query Planning

#### Solution: [Build] Range Frequency Queries (LeetCode 2080)
<!-- id: dq39-range-frequency -->

**Approach.** The constructor packs each pair of value and position into one `long` key, `value * 2^20 + position`, and sorts all keys. Equal values then form one block ordered by position, so the block of value `v` is the position index of `v`. A closed query `[left, right]` becomes the half-open key range from `v * 2^20 + left` up to but excluding `v * 2^20 + right + 1`. The count is the difference of two lower-bound searches over the whole key array. The shift of 20 bits exceeds the largest `right + 1`, which is at most 100,000, so one value's keys never overlap the next value's keys. The multiplication happens in `long` because the shift constant is a `long`, and the harness asserts that the largest key exceeds the `int` range. The harness checks both examples and thousands of random arrays against a direct scan.

**Complexity.**

- **Time** is O(n log n) for sorting in the constructor and O(log n) for each query. Each query runs two binary searches over `n` keys.
- **Space** is O(n) for the key array, and each query allocates nothing.

```java run
import java.util.Arrays;
import java.util.Random;

public final class RangeFrequencyQueries {
    /** Shift that separates the value part from the position part inside one sorted key. */
    private static final long SHIFT = 1L << 20;
    /** Sorted keys value * SHIFT + position; all positions of one value are adjacent and ascending. */
    private final long[] keys;

    /**
     * Builds the index once from the array.
     * Time: O(n log n) to sort n keys. Space: O(n) for the key array.
     * Invariant: keys is sorted, so equal values form one block ordered by position.
     */
    RangeFrequencyQueries(int[] arr) {
        // One key per array slot, so the index has exactly n entries.
        keys = new long[arr.length];
        // Pack each (value, position) pair; the multiplication runs in long because SHIFT is long.
        for (int i = 0; i < arr.length; i++) keys[i] = arr[i] * SHIFT + i;
        // Sorting groups equal values together and orders their positions ascending.
        Arrays.sort(keys);
    }

    /**
     * Returns the index of the first key that is at least target (keys.length when none is).
     * Time: O(log n). Space: O(1).
     * Invariant: every key before lo is below target and every key from hi on is at least target.
     */
    private int lowerBound(long target) {
        // The search range is the half-open interval [lo, hi).
        int lo = 0, hi = keys.length;
        // Each pass halves the range, which gives the logarithmic cost.
        while (lo < hi) {
            // The midpoint form avoids int overflow for large lengths.
            int mid = lo + (hi - lo) / 2;
            // A key below target proves the answer lies right of mid.
            if (keys[mid] < target) lo = mid + 1;
            // Otherwise mid is a candidate and the answer lies at mid or left of it.
            else hi = mid;
        }
        // lo equals hi, the first index whose key is not below target.
        return lo;
    }

    /**
     * Counts positions p with left <= p <= right (closed) where arr[p] == value.
     * Time: O(log n). Space: O(1).
     * Invariant: the answer is the number of keys in the half-open key range [value, left) to [value, right + 1).
     */
    int query(int left, int right, int value) {
        // The closed lower end becomes the first key of the block that can count.
        long from = value * SHIFT + left;
        // The closed upper end right becomes the half-open end right + 1.
        long to = value * SHIFT + right + 1;
        // Two searches give the block boundaries; their difference is the count.
        return lowerBound(to) - lowerBound(from);
    }

    static int brute(int[] a, int l, int r, int v) {
        // Oracle: scan the closed range directly.
        int c = 0;
        for (int i = l; i <= r; i++) if (a[i] == v) c++;
        return c;
    }

    public static void main(String[] args) {
        // Example 1 from the lesson text.
        RangeFrequencyQueries s = new RangeFrequencyQueries(new int[] {3, 1, 3, 2, 3, 1, 3});
        if (s.query(1, 5, 3) != 2) throw new AssertionError("example 1");
        // Example 2: a value that never occurs gives 0.
        if (s.query(0, 6, 9) != 0) throw new AssertionError("example 2");
        // The packed key of the largest value exceeds the int range, so long arithmetic is required.
        if (10_000 * SHIFT <= Integer.MAX_VALUE) throw new AssertionError("long range");
        // Random inputs compared with the scan oracle for every query.
        Random rnd = new Random(7);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(30);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = 1 + rnd.nextInt(5);
            RangeFrequencyQueries q = new RangeFrequencyQueries(a);
            for (int k = 0; k < 20; k++) {
                int l = rnd.nextInt(n), r = l + rnd.nextInt(n - l), v = 1 + rnd.nextInt(6);
                if (q.query(l, r, v) != brute(a, l, r, v)) throw new AssertionError("random mismatch");
            }
        }
    }
}
```

#### Solution: [Vary] Majority Element In Subarray (LeetCode 1157)
<!-- id: dq39-subarray-majority -->

**Approach.** A segment tree stores at each node a survivor pair of a candidate and a count, merged so that equal candidates add and different candidates cancel. If a strict majority of the node range exists, it is the survivor, which is the invariant. A query merges the survivors of the O(log n) nodes that cover the range and obtains one suspect. The suspect is only a suspect, so the code counts it exactly with two binary searches on its sorted position list and returns it only when the count reaches `threshold`. The contract `2 * threshold > length` means any qualifying value is a strict majority, so a failed verification proves that no value qualifies. The harness checks three examples and random arrays with thresholds drawn from the allowed range.

**Complexity.**

- **Time** is O(n) for the build and O(log n) per query, because the walk touches O(log n) nodes and verification runs two binary searches.
- **Space** is O(n) for the tree and the position lists.

```java run
import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;
import java.util.Random;

public final class MajorityChecker {
    /** Number of leaves, a power of two that is at least n. */
    private final int size;
    /** Segment tree node candidate (Boyer-Moore survivor) and its surviving count. */
    private final int[] cand, cnt;
    /** Ascending positions of each value. */
    private final Map<Integer, int[]> where = new HashMap<>();

    /**
     * Builds the candidate tree and the position lists.
     * Time: O(n). Space: O(n).
     * Invariant: each node holds a survivor pair; if a strict majority of the node range exists, it is the survivor.
     */
    MajorityChecker(int[] arr) {
        // Round the leaf count up to a power of two so the bottom-up layout works.
        int s = 1;
        while (s < arr.length) s <<= 1;
        size = s;
        cand = new int[2 * s];
        cnt = new int[2 * s];
        // Each leaf is its own survivor with count one; padding leaves keep count zero.
        for (int i = 0; i < arr.length; i++) { cand[s + i] = arr[i]; cnt[s + i] = 1; }
        // Each parent merges its two children, which costs O(1) per node.
        for (int v = s - 1; v >= 1; v--) merge(v, cand[2 * v], cnt[2 * v], cand[2 * v + 1], cnt[2 * v + 1]);
        // Count occurrences of every value to size the position lists exactly.
        Map<Integer, Integer> freq = new HashMap<>();
        for (int x : arr) freq.merge(x, 1, Integer::sum);
        // Allocate each list, then fill it in index order so it stays ascending.
        for (Map.Entry<Integer, Integer> e : freq.entrySet()) where.put(e.getKey(), new int[e.getValue()]);
        Map<Integer, Integer> fill = new HashMap<>();
        for (int i = 0; i < arr.length; i++) {
            int k = fill.merge(arr[i], 1, Integer::sum) - 1;
            where.get(arr[i])[k] = i;
        }
    }

    /** Writes the survivor of two survivor pairs into node v. Equal candidates add, different ones cancel. */
    private void merge(int v, int a, int ac, int b, int bc) {
        // Equal candidates add their counts.
        if (a == b) { cand[v] = a; cnt[v] = ac + bc; }
        // Different candidates cancel one for one, and the larger count keeps its candidate.
        else if (ac >= bc) { cand[v] = a; cnt[v] = ac - bc; }
        else { cand[v] = b; cnt[v] = bc - ac; }
    }

    /** Counts entries of a sorted list that fall in the closed range [l, r]. Time: O(log n). Space: O(1). */
    private static int countIn(int[] p, int l, int r) {
        // Entries below l and entries above r are both excluded by two lower bounds.
        return lower(p, r + 1) - lower(p, l);
    }

    /** First index in p whose entry is at least x. Invariant: entries before lo are below x. */
    private static int lower(int[] p, int x) {
        // Half-open search range [lo, hi).
        int lo = 0, hi = p.length;
        while (lo < hi) {
            int mid = lo + (hi - lo) / 2;
            if (p[mid] < x) lo = mid + 1; else hi = mid;
        }
        return lo;
    }

    /**
     * Returns a value occurring at least threshold times in positions left..right (closed), or -1.
     * Contract: 2 * threshold > right - left + 1.
     * Time: O(log n) for the tree walk plus O(log n) for verification. Space: O(1).
     * Invariant: the survivor of the range is the only value that can reach a strict majority.
     */
    int query(int left, int right, int threshold) {
        // Accumulated survivor of the walked nodes.
        int ac = 0, acc = 0;
        // Bottom-up walk over the half-open leaf range [l, r).
        int l = left + size, r = right + size + 1;
        while (l < r) {
            // A right child at the left border is taken whole, then the border moves right.
            if ((l & 1) == 1) { int[] m = join(ac, acc, cand[l], cnt[l]); ac = m[0]; acc = m[1]; l++; }
            // A left child at the right border is taken whole after the border moves left.
            if ((r & 1) == 1) { --r; int[] m = join(ac, acc, cand[r], cnt[r]); ac = m[0]; acc = m[1]; }
            l >>= 1; r >>= 1;
        }
        // Survivor count zero means no value can be a strict majority.
        if (acc == 0) return -1;
        int[] p = where.get(ac);
        // Verification: the survivor is only a suspect until its real count reaches the threshold.
        return p != null && countIn(p, left, right) >= threshold ? ac : -1;
    }

    private static int[] join(int a, int ac, int b, int bc) {
        if (a == b) return new int[] {a, ac + bc};
        return ac >= bc ? new int[] {a, ac - bc} : new int[] {b, bc - ac};
    }

    static int brute(int[] a, int l, int r, int t) {
        // Oracle: count every value in the range with a map.
        Map<Integer, Integer> m = new HashMap<>();
        for (int i = l; i <= r; i++) m.merge(a[i], 1, Integer::sum);
        for (Map.Entry<Integer, Integer> e : m.entrySet()) if (e.getValue() >= t) return e.getKey();
        return -1;
    }

    public static void main(String[] args) {
        // Examples from the exercise text.
        MajorityChecker c = new MajorityChecker(new int[] {1, 1, 2, 2, 1, 1});
        if (c.query(0, 5, 4) != 1) throw new AssertionError("example 1");
        if (c.query(0, 3, 3) != -1) throw new AssertionError("example 2");
        if (c.query(2, 3, 2) != 2) throw new AssertionError("example 3");
        // Random inputs, thresholds restricted to the contract 2 * t > length.
        Random rnd = new Random(11);
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(25);
            int[] a = new int[n];
            int range = 1 + rnd.nextInt(4);
            for (int i = 0; i < n; i++) a[i] = 1 + rnd.nextInt(range);
            MajorityChecker q = new MajorityChecker(a);
            for (int k = 0; k < 20; k++) {
                int l = rnd.nextInt(n), r = l + rnd.nextInt(n - l), len = r - l + 1;
                int th = len / 2 + 1 + rnd.nextInt(len - len / 2);
                if (q.query(l, r, th) != brute(a, l, r, th)) throw new AssertionError("random mismatch " + Arrays.toString(a));
            }
        }
    }
}
```

#### Solution: [Boundary] No Majority Exists (Author exercise)
<!-- id: dq39-no-majority -->

**Approach.** For each bit position the constructor stores prefix counts of entries that have that bit set. For a range, a bit joins the candidate when more than half of the entries carry it. If a strict majority value exists, every one of its set bits appears in more than half the range. Every bit it lacks appears in at most half, so the candidate equals that value. When no majority exists, the candidate is some other number that may even be absent from the array. The query counts the candidate exactly through its position list and requires `2 * count > length`. That rule rejects the input `[1, 2, 3]`, where the candidate is 3 with count one. It also rejects an exact tie. The harness asserts the plausible candidate, the rejection, the tie, the `Arrays.binarySearch` insertion code used by the helper, and random arrays against a counting oracle.

**Complexity.**

- **Time** is O(n * 15) for the build and O(15 + log n) per query, because one query reads 15 prefix pairs and runs two binary searches.
- **Space** is O(n * 15) for the prefix tables plus O(n) for the position lists.

```java run
import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;
import java.util.Random;

public final class NoMajorityExists {
    private static final int BITS = 15;
    /** ones[b][i] counts entries among the first i that have bit b set. */
    private final int[][] ones;
    /** Ascending positions of each value. */
    private final Map<Integer, int[]> where = new HashMap<>();

    /**
     * Builds bit prefix counts and position lists.
     * Time: O(n * BITS). Space: O(n * BITS).
     * Invariant: ones[b][i] equals the number of set bits b among arr[0..i-1].
     */
    NoMajorityExists(int[] arr) {
        ones = new int[BITS][arr.length + 1];
        // One prefix pass per bit; each cell extends the previous prefix by one entry.
        for (int b = 0; b < BITS; b++)
            for (int i = 0; i < arr.length; i++) ones[b][i + 1] = ones[b][i] + ((arr[i] >> b) & 1);
        // Collect the positions of each value in index order.
        Map<Integer, Integer> freq = new HashMap<>();
        for (int x : arr) freq.merge(x, 1, Integer::sum);
        for (Map.Entry<Integer, Integer> e : freq.entrySet()) where.put(e.getKey(), new int[e.getValue()]);
        Map<Integer, Integer> fill = new HashMap<>();
        for (int i = 0; i < arr.length; i++) where.get(arr[i])[fill.merge(arr[i], 1, Integer::sum) - 1] = i;
    }

    /**
     * Builds the only value that could be a strict majority of positions left..right (closed).
     * Time: O(BITS). Space: O(1).
     * Invariant: if a strict majority value exists, each of its bits is set in more than half the range.
     */
    int candidate(int left, int right) {
        // Length of the closed range, kept as an int because it is at most n.
        int len = right - left + 1;
        int c = 0;
        for (int b = 0; b < BITS; b++) {
            // Number of entries with bit b set inside the range, from two prefix reads.
            int set = ones[b][right + 1] - ones[b][left];
            // The bit joins the candidate only when a strict majority of entries carry it.
            if (2 * set > len) c |= 1 << b;
        }
        return c;
    }

    /**
     * Returns the value occurring strictly more than half the range, or -1 when none does.
     * Time: O(BITS + log n). Space: O(1).
     * Invariant: the candidate is verified by its real count, so a plausible but wrong value never escapes.
     */
    int query(int left, int right) {
        int c = candidate(left, right);
        int[] p = where.get(c);
        // A candidate that never occurs in the array has no position list.
        if (p == null) return -1;
        // Real count of c inside the closed range, from two lower bounds.
        int count = insertion(p, right + 1) - insertion(p, left);
        // Strict majority means twice the count exceeds the length.
        return 2 * count > right - left + 1 ? c : -1;
    }

    /** Index of the first entry at least x; binarySearch gives a negative insertion code when absent. */
    private static int insertion(int[] p, int x) {
        int i = Arrays.binarySearch(p, x);
        // Positions are distinct, so a hit is the unique first entry and a miss decodes to -(i) - 1.
        return i >= 0 ? i : -i - 1;
    }

    static int brute(int[] a, int l, int r) {
        Map<Integer, Integer> m = new HashMap<>();
        for (int i = l; i <= r; i++) m.merge(a[i], 1, Integer::sum);
        for (Map.Entry<Integer, Integer> e : m.entrySet()) if (2 * e.getValue() > r - l + 1) return e.getKey();
        return -1;
    }

    public static void main(String[] args) {
        // Plausible but insufficient candidate: bits of 1, 2, 3 produce 3, which occurs once in three slots.
        NoMajorityExists s = new NoMajorityExists(new int[] {1, 2, 3});
        if (s.candidate(0, 2) != 3) throw new AssertionError("candidate");
        if (s.query(0, 2) != -1) throw new AssertionError("rejected");
        // An exact half is not more than half.
        NoMajorityExists t = new NoMajorityExists(new int[] {5, 5, 6, 6});
        if (t.query(0, 3) != -1) throw new AssertionError("tie");
        // A real majority passes verification.
        if (t.query(0, 2) != 5) throw new AssertionError("majority");
        // Arrays.binarySearch returns -(insertion point) - 1 for a missing key.
        if (Arrays.binarySearch(new int[] {2, 4}, 3) != -2) throw new AssertionError("binarySearch code");
        // Random inputs against the counting oracle.
        Random rnd = new Random(5);
        for (int k = 0; k < 4000; k++) {
            int n = 1 + rnd.nextInt(25);
            int[] a = new int[n];
            int range = 1 + rnd.nextInt(5);
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(range + 1) * 3;
            NoMajorityExists q = new NoMajorityExists(a);
            for (int j = 0; j < 20; j++) {
                int l = rnd.nextInt(n), r = l + rnd.nextInt(n - l);
                if (q.query(l, r) != brute(a, l, r)) throw new AssertionError("random mismatch " + Arrays.toString(a));
            }
        }
    }
}
```

#### Solution: [Recognize] Edge Length Limited Paths II (LeetCode 1724)
<!-- id: dq39-limited-paths-online -->

**Approach.** The offline task sorts queries by `limit`, unions every edge strictly below the limit and checks whether `p` and `q` share a root. That plan needs every query before the first answer, so an online API cannot use it. The online plan builds a minimum spanning forest with Kruskal's algorithm. The invariant is that the heaviest edge on the forest path between two vertices is the smallest possible heaviest edge over all paths between them. Binary lifting tables store the ancestor and the heaviest edge for each jump of 2^k steps. A query answers false when the roots differ and otherwise lifts both endpoints to their meeting point while tracking the heaviest edge. The answer is true exactly when that edge is strictly below `limit`. The solution also contains the offline method, and the harness compares online answers, offline answers and a rebuild-from-scratch oracle on random graphs with parallel edges and self-loops.

**Complexity.**

- **Time** is O(E log E) for sorting edges plus O(n log n) for the tables, and O(log n) per query because each lift uses at most log n jumps.
- **Space** is O(n log n) for the two lifting tables, plus O(E) for the sorted copy of the edge list during construction.

```java run
import java.util.ArrayDeque;
import java.util.Arrays;
import java.util.Comparator;
import java.util.Random;

public final class EdgeLimitedPathsOnline {
    private final int[][] up, mx;
    private final int[] depth, root;
    private final int log;

    private static int find(int[] d, int x) {
        // Path halving keeps the trees shallow; each step points x at its grandparent.
        while (d[x] != x) { d[x] = d[d[x]]; x = d[x]; }
        return x;
    }

    /**
     * Builds the minimum spanning forest, then binary lifting tables of ancestors and heaviest edges.
     * Time: O(E log E + n log n). Space: O(n log n).
     * Invariant: p and q are joined by edges all below limit exactly when the forest path between them has maximum edge below limit.
     */
    EdgeLimitedPathsOnline(int n, int[][] edges) {
        // Kruskal order: ascending weight, compared without subtraction.
        int[][] sorted = edges.clone();
        Arrays.sort(sorted, Comparator.comparingInt(e -> e[2]));
        int[] dsu = new int[n];
        for (int i = 0; i < n; i++) dsu[i] = i;
        // Forest adjacency as linked arrays: head per vertex, next/to/w per directed half-edge.
        int[] head = new int[n], nxt = new int[2 * n], to = new int[2 * n], w = new int[2 * n];
        Arrays.fill(head, -1);
        int h = 0;
        for (int[] e : sorted) {
            int a = find(dsu, e[0]), b = find(dsu, e[1]);
            // An edge between two different components joins the forest; otherwise a lighter path already exists.
            if (a != b) {
                dsu[a] = b;
                to[h] = e[1]; w[h] = e[2]; nxt[h] = head[e[0]]; head[e[0]] = h++;
                to[h] = e[0]; w[h] = e[2]; nxt[h] = head[e[1]]; head[e[1]] = h++;
            }
        }
        // Smallest table height with 2^log >= n, at least 1.
        int lg = 1;
        while ((1 << lg) < n) lg++;
        log = lg;
        up = new int[lg][n];
        mx = new int[lg][n];
        depth = new int[n];
        root = new int[n];
        boolean[] seen = new boolean[n];
        // Breadth-first walk from each unseen vertex roots one tree per component.
        for (int s = 0; s < n; s++) {
            if (seen[s]) continue;
            ArrayDeque<Integer> dq = new ArrayDeque<>();
            dq.add(s); seen[s] = true; up[0][s] = s; mx[0][s] = 0; root[s] = s;
            while (!dq.isEmpty()) {
                int u = dq.poll();
                for (int e = head[u]; e != -1; e = nxt[e]) {
                    int v = to[e];
                    if (seen[v]) continue;
                    seen[v] = true; root[v] = s; depth[v] = depth[u] + 1;
                    up[0][v] = u; mx[0][v] = w[e];
                    dq.add(v);
                }
            }
        }
        // Level k jumps 2^k parents and keeps the heaviest edge on that jump.
        for (int k = 1; k < lg; k++)
            for (int v = 0; v < n; v++) {
                int mid = up[k - 1][v];
                up[k][v] = up[k - 1][mid];
                mx[k][v] = Math.max(mx[k - 1][v], mx[k - 1][mid]);
            }
    }

    /**
     * Returns true when some path from p to q uses only edges with weight strictly below limit.
     * Time: O(log n) per call. Space: O(1).
     * Invariant: best is the heaviest edge seen on the climb so far.
     */
    boolean query(int p, int q, int limit) {
        // Different trees mean no path exists at all.
        if (root[p] != root[q]) return false;
        int best = 0;
        int u = p, v = q;
        // Lift the deeper endpoint to the depth of the other one.
        if (depth[u] < depth[v]) { int t = u; u = v; v = t; }
        int diff = depth[u] - depth[v];
        for (int k = 0; k < log; k++)
            if (((diff >> k) & 1) == 1) { best = Math.max(best, mx[k][u]); u = up[k][u]; }
        if (u != v) {
            // Lift both endpoints while their ancestors differ, so they stop just below the meeting vertex.
            for (int k = log - 1; k >= 0; k--)
                if (up[k][u] != up[k][v]) {
                    best = Math.max(best, Math.max(mx[k][u], mx[k][v]));
                    u = up[k][u]; v = up[k][v];
                }
            // One last edge on each side reaches the meeting vertex.
            best = Math.max(best, Math.max(mx[0][u], mx[0][v]));
        }
        // The minimum possible heaviest edge over all p-q paths is best; the strict bound compares against limit.
        return best < limit;
    }

    /** Offline contrast: sorts the queries by limit and grows a union-find; needs every query in advance. */
    static boolean[] offline(int n, int[][] edges, int[][] queries) {
        int[][] es = edges.clone();
        Arrays.sort(es, Comparator.comparingInt(e -> e[2]));
        Integer[] order = new Integer[queries.length];
        for (int i = 0; i < order.length; i++) order[i] = i;
        Arrays.sort(order, Comparator.comparingInt(i -> queries[i][2]));
        int[] d = new int[n];
        for (int i = 0; i < n; i++) d[i] = i;
        boolean[] ans = new boolean[queries.length];
        int ptr = 0;
        for (int qi : order) {
            // Union exactly the edges strictly below this query's limit.
            while (ptr < es.length && es[ptr][2] < queries[qi][2]) {
                d[find(d, es[ptr][0])] = find(d, es[ptr][1]);
                ptr++;
            }
            ans[qi] = find(d, queries[qi][0]) == find(d, queries[qi][1]);
        }
        return ans;
    }

    static boolean brute(int n, int[][] edges, int p, int q, int limit) {
        // Oracle: rebuild a union-find from only the edges below limit.
        int[] d = new int[n];
        for (int i = 0; i < n; i++) d[i] = i;
        for (int[] e : edges) if (e[2] < limit) d[find(d, e[0])] = find(d, e[1]);
        return find(d, p) == find(d, q);
    }

    public static void main(String[] args) {
        // Example: path 0-1 (weight 2), 1-2 (weight 4), plus a heavy shortcut 0-2 (weight 9).
        int[][] ex = {{0, 1, 2}, {1, 2, 4}, {0, 2, 9}};
        EdgeLimitedPathsOnline s = new EdgeLimitedPathsOnline(4, ex);
        if (!s.query(0, 2, 5)) throw new AssertionError("example 1");
        if (s.query(0, 2, 4)) throw new AssertionError("strict bound");
        if (s.query(0, 3, 100)) throw new AssertionError("isolated vertex");
        // Random graphs, with duplicate edges and self-loops allowed, against the oracle and the offline method.
        Random rnd = new Random(3);
        for (int t = 0; t < 1500; t++) {
            int n = 1 + rnd.nextInt(9), m = rnd.nextInt(15);
            int[][] edges = new int[m][];
            for (int i = 0; i < m; i++) edges[i] = new int[] {rnd.nextInt(n), rnd.nextInt(n), 1 + rnd.nextInt(8)};
            EdgeLimitedPathsOnline g = new EdgeLimitedPathsOnline(n, edges);
            int qn = 15;
            int[][] qs = new int[qn][];
            for (int i = 0; i < qn; i++) qs[i] = new int[] {rnd.nextInt(n), rnd.nextInt(n), 1 + rnd.nextInt(10)};
            boolean[] off = offline(n, edges, qs);
            for (int i = 0; i < qn; i++) {
                boolean want = brute(n, edges, qs[i][0], qs[i][1], qs[i][2]);
                if (g.query(qs[i][0], qs[i][1], qs[i][2]) != want) throw new AssertionError("online mismatch");
                if (off[i] != want) throw new AssertionError("offline mismatch");
            }
        }
    }
}
```

