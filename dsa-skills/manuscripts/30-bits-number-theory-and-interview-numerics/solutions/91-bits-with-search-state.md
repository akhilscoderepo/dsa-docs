<!-- solutions-for: 91-bits-with-search-state -->
### Solutions For Bits With Search State

#### Solution: [Build] Subsets Listed By Size (LeetCode 78)
<!-- id: bt91-subsets-by-size -->

**Approach.** The solution reads every number from 0 to `2^n - 1` as one subset and emits the numbers grouped by bit count.

Bit `i` of a mask selects `nums[i]`, so the mask 5 for three items selects positions 0 and 2. An outer loop fixes the size, and an inner loop walks the masks in increasing order and keeps those whose `Integer.bitCount` equals the size. This produces sizes in ascending order and, inside one size, masks in ascending order, which is the required order. Each kept mask is expanded by testing bits 0 to `n - 1` in order, so the elements appear in index order. The invariant is that the list holds exactly the masks of smaller sizes, and of the current size below the current mask. For `n = 0` the only mask is 0, and the output is one empty list.

**Complexity.**

- **Time** is O(n * 2^n) for the size filter plus O(n * 2^n) to build the lists, because each of `n + 1` sizes scans `2^n` masks and each emitted list costs O(n).
- **Space** is O(n * 2^n) for the output, with O(1) extra working memory.

```java run
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public final class SubsetsBySize {
    /**
     * Returns all subsets ordered by size, then by mask value, with elements in index order.
     * Time: O(n * 2^n), n + 1 sizes each scanning 2^n masks plus the output cost.
     * Space: O(n * 2^n) for the output lists.
     * Invariant: all masks with smaller size, and smaller mask value at this size, are already emitted.
     */
    static List<List<Integer>> subsetsBySize(int[] nums) {
        int n = nums.length;
        List<List<Integer>> out = new ArrayList<>();
        // The outer loop fixes the subset size from 0 up to n.
        for (int size = 0; size <= n; size++) {
            // The inner loop walks every mask in increasing value, so ties follow mask order.
            for (int mask = 0; mask < (1 << n); mask++) {
                // Only masks with exactly this many set bits belong to the current size.
                if (Integer.bitCount(mask) != size) continue;
                List<Integer> subset = new ArrayList<>();
                // Bit i selects nums[i], and the loop order keeps elements in index order.
                for (int i = 0; i < n; i++) {
                    if ((mask & (1 << i)) != 0) subset.add(nums[i]);
                }
                out.add(subset);
            }
        }
        return out;
    }

    /** Oracle that builds subsets by include-or-exclude recursion and sorts by the stated key. */
    static List<List<Integer>> oracle(int[] nums) {
        List<int[]> all = new ArrayList<>();
        rec(nums, 0, new ArrayList<>(), all);
        // Sort key: size first, then the mask value rebuilt from the chosen indexes.
        all.sort((x, y) -> x.length != y.length ? Integer.compare(x.length, y.length) : Integer.compare(maskOf(x), maskOf(y)));
        List<List<Integer>> out = new ArrayList<>();
        for (int[] idx : all) {
            List<Integer> s = new ArrayList<>();
            for (int i : idx) s.add(nums[i]);
            out.add(s);
        }
        return out;
    }

    static void rec(int[] nums, int i, List<Integer> chosen, List<int[]> all) {
        if (i == nums.length) {
            all.add(chosen.stream().mapToInt(Integer::intValue).toArray());
            return;
        }
        rec(nums, i + 1, chosen, all);
        chosen.add(i);
        rec(nums, i + 1, chosen, all);
        chosen.remove(chosen.size() - 1);
    }

    static int maskOf(int[] idx) {
        int m = 0;
        for (int i : idx) m |= 1 << i;
        return m;
    }

    public static void main(String[] args) {
        // Example 1: three items, in the order of the masks 0, 1, 2, 4, 3, 5, 6, 7.
        List<List<Integer>> expected = List.of(List.of(), List.of(5), List.of(2), List.of(9),
                List.of(5, 2), List.of(5, 9), List.of(2, 9), List.of(5, 2, 9));
        if (!subsetsBySize(new int[]{5, 2, 9}).equals(expected)) throw new AssertionError("example 1");
        // Example 2: empty input gives one empty subset.
        if (!subsetsBySize(new int[0]).equals(List.of(List.of()))) throw new AssertionError("example 2");
        // The largest size has 2^12 lists in total.
        if (subsetsBySize(new int[12]).size() != 4096) throw new AssertionError("count");
        // Random distinct arrays with a fixed seed, against the recursion oracle.
        Random rnd = new Random(3101);
        for (int round = 0; round < 200; round++) {
            int n = rnd.nextInt(8);
            int[] nums = new int[n];
            for (int i = 0; i < n; i++) nums[i] = i * 7 - 20 + rnd.nextInt(5);
            if (!subsetsBySize(nums).equals(oracle(nums))) throw new AssertionError("round " + round);
        }
    }
}
```

#### Solution: [Vary] Repeated Windows Of Chosen Length (LeetCode 187)
<!-- id: bt91-repeated-windows -->

**Approach.** The solution encodes each window as a `long` mask and counts masks in a hash map.

Each letter takes two bits through the codes A=0, C=1, G=2 and T=3. A window of `k` letters then uses `2k` bits. The update shifts the old mask left by two, adds the new code and cuts the result with `full`, which holds `2k` one-bits. The cut removes the letter that has left the window. For `k` up to 31 the mask needs up to 62 bits, so `long` is required, and `full` is built as `(1L << (2 * k)) - 1`. With an `int`, the shift count 32 wraps to 0 for `k = 16`, so `full` would be wrong. Two windows have the same mask exactly when they have the same text. A map records the count of each mask and the first start of each mask, and the answer lists the texts of masks with a count of at least 2 in text order. When the string is shorter than `k`, no window completes and the answer is empty.

**Complexity.**

- **Time** is O(N + d * k + d log d), where `N` is the length of `s` and `d` is the number of distinct repeated windows, because the scan does O(1) work per letter and the output needs the texts and a sort.
- **Space** is O(N) for the two maps, since each holds at most one entry per window.

```java run
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Random;
import java.util.TreeSet;

public final class RepeatedWindows {
    /**
     * Returns the distinct length-k windows of s that occur at least twice, in text order.
     * Time: O(N + d*k + d log d) for N letters and d repeated windows.
     * Space: O(N) for the count and first-start maps.
     * Invariant: window holds the codes of the last min(i + 1, k) letters in its low bits.
     */
    static List<String> repeatedWindows(String s, int k) {
        Map<Long, Integer> count = new HashMap<>();
        Map<Long, Integer> firstStart = new HashMap<>();
        // 2k one-bits, built in long so that k up to 31 stays inside 62 bits.
        long full = (1L << (2 * k)) - 1;
        long window = 0;
        // One pass keeps a rolling mask of the latest letters.
        for (int i = 0; i < s.length(); i++) {
            // Shift in two bits for the new letter, then cut the letter that left the window.
            window = ((window << 2) | "ACGT".indexOf(s.charAt(i))) & full;
            // A complete window exists from index k - 1 onward.
            if (i >= k - 1) {
                count.merge(window, 1, Integer::sum);
                firstStart.putIfAbsent(window, i - k + 1);
            }
        }
        // A tree set sorts the texts and removes nothing, since masks are unique per text.
        TreeSet<String> sorted = new TreeSet<>();
        for (Map.Entry<Long, Integer> e : count.entrySet()) {
            if (e.getValue() >= 2) {
                int start = firstStart.get(e.getKey());
                sorted.add(s.substring(start, start + k));
            }
        }
        return new ArrayList<>(sorted);
    }

    /** Oracle that counts substrings directly. */
    static List<String> oracle(String s, int k) {
        Map<String, Integer> count = new HashMap<>();
        for (int i = 0; i + k <= s.length(); i++) count.merge(s.substring(i, i + k), 1, Integer::sum);
        TreeSet<String> out = new TreeSet<>();
        for (Map.Entry<String, Integer> e : count.entrySet()) if (e.getValue() >= 2) out.add(e.getKey());
        return new ArrayList<>(out);
    }

    public static void main(String[] args) {
        // Example 1: overlapping repeats with k = 4.
        List<String> e1 = List.of("CCGG", "CGGT", "GGTT", "GTTC", "TCCG", "TTCC");
        if (!repeatedWindows("CCGGTTCCGGTTCCGGA", 4).equals(e1)) throw new AssertionError("example 1");
        // Example 2: forty copies of A with k = 31 needs 62 mask bits.
        if (!repeatedWindows("A".repeat(40), 31).equals(List.of("A".repeat(31)))) throw new AssertionError("example 2");
        // Windows longer than the string, and an empty string, give empty results.
        if (!repeatedWindows("ACG", 5).isEmpty() || !repeatedWindows("", 3).isEmpty()) throw new AssertionError("short");
        // An int-width mask would fail at k = 16, so a window of 16 must still work.
        if (!repeatedWindows("T".repeat(20), 16).equals(List.of("T".repeat(16)))) throw new AssertionError("k 16");
        // Random strings over the alphabet, every k from 1 to 31, against the substring oracle.
        Random rnd = new Random(3102);
        for (int round = 0; round < 300; round++) {
            int len = rnd.nextInt(60);
            StringBuilder sb = new StringBuilder();
            int alphabet = 1 + rnd.nextInt(4);
            for (int i = 0; i < len; i++) sb.append("ACGT".charAt(rnd.nextInt(alphabet)));
            int k = 1 + rnd.nextInt(31);
            if (!repeatedWindows(sb.toString(), k).equals(oracle(sb.toString(), k))) throw new AssertionError("round " + round);
        }
    }
}
```

#### Solution: [Boundary] Best Disjoint Word Pair (LeetCode 318)
<!-- id: bt91-best-word-pair -->

**Approach.** The solution turns each word into a 26-bit letter mask and compares masks pairwise.

A word with letters `a` to `z` becomes the integer whose bit `c - 'a'` is set for each letter that occurs. Two words share a letter exactly when the `&` of their masks is nonzero, so a zero `&` accepts the pair. The product of the two lengths is computed after casting one length to `long`, because lengths up to 100,000 give a product of 10^10, which an `int` would wrap. A pair replaces the best only if its product is strictly larger. Since the loops visit pairs in increasing `i` and then increasing `j`, the first pair to reach the maximum stays, which implements the tie rule. When no pair is disjoint, the initial values `{0, -1, -1}` are returned.

**Complexity.**

- **Time** is O(T + n^2), where `T` is the total number of letters, because building the masks reads each letter once and the pair loop does a constant test for each of the `n(n-1)/2` pairs.
- **Space** is O(n) for the mask array.

```java run
import java.util.Random;

public final class BestWordPair {
    /**
     * Returns {best product, i, j} for the best disjoint pair, or {0, -1, -1}.
     * Time: O(T + n^2) for T letters in total and n words.
     * Space: O(n) for the letter masks.
     * Invariant: best is the largest product among disjoint pairs examined so far, with the earliest indexes.
     */
    static long[] bestWordPair(String[] words) {
        int n = words.length;
        int[] letters = new int[n];
        // One pass over each word sets one bit for each distinct letter.
        for (int i = 0; i < n; i++) {
            for (int p = 0; p < words[i].length(); p++) letters[i] |= 1 << (words[i].charAt(p) - 'a');
        }
        long best = 0;
        int bi = -1, bj = -1;
        // Pairs are visited in increasing i, then increasing j.
        for (int i = 0; i < n; i++) {
            for (int j = i + 1; j < n; j++) {
                // A shared letter leaves a nonzero AND, so the pair is rejected.
                if ((letters[i] & letters[j]) != 0) continue;
                // Widen one factor first, because two lengths can multiply past int.
                long product = (long) words[i].length() * words[j].length();
                // A strict comparison keeps the earliest pair on a tie.
                if (product > best) { best = product; bi = i; bj = j; }
            }
        }
        return new long[]{best, bi, bj};
    }

    /** Oracle that compares letters with boolean tables instead of masks. */
    static long[] oracle(String[] words) {
        long best = 0;
        int bi = -1, bj = -1;
        for (int i = 0; i < words.length; i++) {
            for (int j = i + 1; j < words.length; j++) {
                boolean[] seen = new boolean[26];
                for (char c : words[i].toCharArray()) seen[c - 'a'] = true;
                boolean shared = false;
                for (char c : words[j].toCharArray()) if (seen[c - 'a']) shared = true;
                if (shared) continue;
                long product = (long) words[i].length() * words[j].length();
                if (product > best) { best = product; bi = i; bj = j; }
            }
        }
        return new long[]{best, bi, bj};
    }

    public static void main(String[] args) {
        // Example 1: five words with one best disjoint pair.
        String[] w1 = {"abcd", "ab", "xyz", "mnopq", "cde"};
        if (!java.util.Arrays.equals(bestWordPair(w1), new long[]{20, 0, 3})) throw new AssertionError("example 1");
        // Example 2: two long words, where the product needs a long.
        String[] w2 = {"a".repeat(100_000), "b".repeat(100_000)};
        if (!java.util.Arrays.equals(bestWordPair(w2), new long[]{10_000_000_000L, 0, 1})) throw new AssertionError("example 2");
        // No disjoint pair, and fewer than two words.
        if (!java.util.Arrays.equals(bestWordPair(new String[]{"ab", "ba", "ab"}), new long[]{0, -1, -1})) throw new AssertionError("none");
        if (!java.util.Arrays.equals(bestWordPair(new String[0]), new long[]{0, -1, -1})) throw new AssertionError("empty");
        // Ties keep the earliest pair.
        if (!java.util.Arrays.equals(bestWordPair(new String[]{"ab", "cd", "ef"}), new long[]{4, 0, 1})) throw new AssertionError("tie");
        // Random small alphabets with a fixed seed, against the table oracle.
        Random rnd = new Random(3103);
        for (int round = 0; round < 500; round++) {
            int n = rnd.nextInt(8);
            String[] words = new String[n];
            for (int i = 0; i < n; i++) {
                StringBuilder sb = new StringBuilder();
                int len = 1 + rnd.nextInt(6);
                for (int p = 0; p < len; p++) sb.append((char) ('a' + rnd.nextInt(7)));
                words[i] = sb.toString();
            }
            if (!java.util.Arrays.equals(bestWordPair(words), oracle(words))) throw new AssertionError("round " + round);
        }
    }
}
```

#### Solution: [Recognize] Shortest Walk Ending At A Node (LeetCode 847)
<!-- id: bt91-walk-ends-at-target -->

**Approach.** The solution runs breadth-first search over states made of a node and a mask of nodes seen.

A state packs into `(node << n) | mask`. Every node starts as its own state at distance 0, because the walk may begin anywhere. A move along an edge to `next` produces the state with node `next` and mask `mask | (1 << next)`. The search marks a state visited when it first enters the queue, so each of the at most `n * 2^n` states is expanded once. Breadth-first order guarantees that the first time the state `(t, full)` leaves the queue, its distance is the smallest. The goal is one specific node together with the full mask, so a state with the full mask at another node does not end the search. A node may be entered again, since it pairs with a larger mask each time. A single-node graph starts at the goal, and the answer is 0.

**Complexity.**

- **Time** is O(2^n * (n + E)), because each of the `n * 2^n` states scans the edges of its node, and the edge scans total `2^n` times the sum of the degrees `2E`.
- **Space** is O(n * 2^n) for the distance array and the queue.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

public final class WalkEndsAtTarget {
    /**
     * Returns the fewest edges of a walk that visits every node and ends at t, or -1.
     * Time: O(2^n * (n + E)) over n * 2^n states.
     * Space: O(n * 2^n) for dist and the queue.
     * Invariant: dist[state] is final when state first enters the queue, because the queue is in distance order.
     */
    static int shortestWalkEndingAt(int[][] graph, int t) {
        int n = graph.length;
        int full = (1 << n) - 1;
        // One slot per (node, mask), and -1 marks an unvisited state.
        int[] dist = new int[n << n];
        Arrays.fill(dist, -1);
        int[] queue = new int[n << n];
        int head = 0, tail = 0;
        // The walk may start at any node, so every node begins as a level-0 state.
        for (int s = 0; s < n; s++) {
            int state = (s << n) | (1 << s);
            dist[state] = 0;
            queue[tail++] = state;
        }
        // The goal is the node t together with the full mask.
        int goal = (t << n) | full;
        // Each state is dequeued once, so the loop runs at most n * 2^n times.
        while (head < tail) {
            int state = queue[head++];
            // The goal state leaves the queue at its smallest distance.
            if (state == goal) return dist[state];
            int node = state >> n;
            int mask = state & full;
            // Every edge adds the next node to the mask.
            for (int next : graph[node]) {
                int nextState = (next << n) | (mask | (1 << next));
                // A state seen before already has a distance that is no larger.
                if (dist[nextState] == -1) {
                    dist[nextState] = dist[state] + 1;
                    queue[tail++] = nextState;
                }
            }
        }
        return -1;
    }

    /** Oracle: all-pairs shortest paths, then every visiting order that ends at t. */
    static int oracle(int[][] graph, int t) {
        int n = graph.length, inf = 1_000_000;
        int[][] d = new int[n][n];
        for (int[] row : d) Arrays.fill(row, inf);
        for (int i = 0; i < n; i++) {
            d[i][i] = 0;
            for (int j : graph[i]) d[i][j] = 1;
        }
        // Floyd-Warshall closes the distances.
        for (int k = 0; k < n; k++)
            for (int i = 0; i < n; i++)
                for (int j = 0; j < n; j++) d[i][j] = Math.min(d[i][j], d[i][k] + d[k][j]);
        List<Integer> others = new ArrayList<>();
        for (int v = 0; v < n; v++) if (v != t) others.add(v);
        if (others.isEmpty()) return 0;
        int[] best = {inf};
        permute(others, 0, t, d, best);
        return best[0] >= inf ? -1 : best[0];
    }

    static void permute(List<Integer> list, int k, int t, int[][] d, int[] best) {
        if (k == list.size()) {
            int cost = 0;
            for (int i = 0; i + 1 < list.size(); i++) cost += d[list.get(i)][list.get(i + 1)];
            cost += d[list.get(list.size() - 1)][t];
            best[0] = Math.min(best[0], cost);
            return;
        }
        for (int i = k; i < list.size(); i++) {
            java.util.Collections.swap(list, k, i);
            permute(list, k + 1, t, d, best);
            java.util.Collections.swap(list, k, i);
        }
    }

    static int[][] randomConnected(Random rnd, int n) {
        boolean[][] adj = new boolean[n][n];
        // A random tree guarantees connectivity.
        for (int v = 1; v < n; v++) {
            int u = rnd.nextInt(v);
            adj[u][v] = adj[v][u] = true;
        }
        // Extra edges add cycles.
        for (int e = rnd.nextInt(n + 1); e > 0; e--) {
            int u = rnd.nextInt(n), v = rnd.nextInt(n);
            if (u != v) adj[u][v] = adj[v][u] = true;
        }
        int[][] g = new int[n][];
        for (int i = 0; i < n; i++) {
            List<Integer> nb = new ArrayList<>();
            for (int j = 0; j < n; j++) if (adj[i][j]) nb.add(j);
            g[i] = nb.stream().mapToInt(Integer::intValue).toArray();
        }
        return g;
    }

    public static void main(String[] args) {
        // Example 1: the triangle with a tail, for two different end nodes.
        int[][] g1 = {{1, 2}, {0, 2}, {0, 1, 3}, {2}};
        if (shortestWalkEndingAt(g1, 3) != 3 || shortestWalkEndingAt(g1, 2) != 4) throw new AssertionError("example 1");
        // Example 2: a path, and a one-node graph.
        int[][] g2 = {{1}, {0, 2}, {1, 3}, {2}};
        if (shortestWalkEndingAt(g2, 1) != 4) throw new AssertionError("example 2a");
        if (shortestWalkEndingAt(new int[][]{{}}, 0) != 0) throw new AssertionError("example 2b");
        // The largest allowed size must finish: a path of twelve nodes.
        int[][] path = new int[12][];
        for (int i = 0; i < 12; i++) {
            if (i == 0) path[i] = new int[]{1};
            else if (i == 11) path[i] = new int[]{10};
            else path[i] = new int[]{i - 1, i + 1};
        }
        if (shortestWalkEndingAt(path, 11) != 11) throw new AssertionError("path end");
        // Random connected graphs of up to seven nodes against the permutation oracle.
        Random rnd = new Random(3104);
        for (int round = 0; round < 300; round++) {
            int n = 1 + rnd.nextInt(7);
            int[][] g = randomConnected(rnd, n);
            int t = rnd.nextInt(n);
            if (shortestWalkEndingAt(g, t) != oracle(g, t)) throw new AssertionError("round " + round);
        }
    }
}
```
