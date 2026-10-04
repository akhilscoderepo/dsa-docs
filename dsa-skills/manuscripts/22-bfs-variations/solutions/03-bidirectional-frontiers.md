<!-- solutions-for: 03-bidirectional-frontiers -->
### Bidirectional Frontiers

#### Solution: [Build] Two-Ended Integer Search (Author exercise)
<!-- id: bv-two-ended-integer -->

**Approach.** Two distance arrays of size `cap + 1` hold the two tables, with -1 for unreached, and each side keeps a list for its current layer. Every round expands whole layers of the thinner side, with ties going to the start side, and while a neighbor is being generated it is first looked up in the opposite table, and then in the side's own table. A hit returns the expanded value's distance plus one plus the stored distance. The four neighbors come from a helper that doubles only when `x <= cap / 2`. The oracle never searches by layers. It sets every distance to infinity except the start and relaxes all moves over all values until nothing improves, which is a fixpoint of the shortest-distance equations, for random caps from 1 to 40. The assertions also cover the lesson's claims: a variant that declares a meeting only when the two current layers share a value fails on start 3 and target 4, where the answer is 1, such a variant is wrong on many random inputs while the real method never is, and `2 * x` overflows to a negative `int` at 1.1 billion while `x <= cap / 2` stays correct.

**Complexity.** Both searches stop at about half the answer's depth, so the number of values touched is roughly twice what one search to that radius would touch, instead of the full-radius count. Memory is O(cap) for the two arrays, and a single call also costs O(cap) to initialise them.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

public final class TwoEndedIntegerSolution {
    static int[] moves(int x, int cap) {
        int[] out = new int[4];
        int k = 0;
        if (x + 1 <= cap) out[k++] = x + 1;
        if (x - 1 >= 1) out[k++] = x - 1;
        if (x <= cap / 2) out[k++] = 2 * x;
        if (x % 2 == 0) out[k++] = x / 2;
        return Arrays.copyOf(out, k);
    }

    static int solve(int start, int target, int cap) {
        if (start == target) return 0;
        int[] fromStart = new int[cap + 1], fromTarget = new int[cap + 1];
        Arrays.fill(fromStart, -1);
        Arrays.fill(fromTarget, -1);
        fromStart[start] = 0;
        fromTarget[target] = 0;
        List<Integer> layerS = new ArrayList<>(List.of(start));
        List<Integer> layerT = new ArrayList<>(List.of(target));
        while (!layerS.isEmpty() && !layerT.isEmpty()) {
            boolean growStart = layerS.size() <= layerT.size();
            List<Integer> layer = growStart ? layerS : layerT;
            int[] mine = growStart ? fromStart : fromTarget;
            int[] other = growStart ? fromTarget : fromStart;
            List<Integer> fresh = new ArrayList<>();
            for (int cur : layer) {
                for (int next : moves(cur, cap)) {
                    if (other[next] >= 0) return mine[cur] + 1 + other[next];
                    if (mine[next] >= 0) continue;
                    mine[next] = mine[cur] + 1;
                    fresh.add(next);
                }
            }
            if (growStart) layerS = fresh; else layerT = fresh;
        }
        return -1;
    }

    static int oracle(int start, int target, int cap) {
        int inf = Integer.MAX_VALUE / 2;
        int[] best = new int[cap + 1];
        Arrays.fill(best, inf);
        best[start] = 0;
        boolean changed = true;
        while (changed) {
            changed = false;
            for (int x = 1; x <= cap; x++) {
                if (best[x] >= inf) continue;
                for (int y : moves(x, cap)) {
                    if (best[x] + 1 < best[y]) { best[y] = best[x] + 1; changed = true; }
                }
            }
        }
        return best[target] >= inf ? -1 : best[target];
    }

    static int layersMustMatch(int start, int target, int cap) {
        if (start == target) return 0;
        boolean[] seenS = new boolean[cap + 1], seenT = new boolean[cap + 1];
        seenS[start] = true;
        seenT[target] = true;
        List<Integer> layerS = new ArrayList<>(List.of(start));
        List<Integer> layerT = new ArrayList<>(List.of(target));
        int round = 0;
        while (!layerS.isEmpty() && !layerT.isEmpty()) {
            round++;
            List<Integer> freshS = new ArrayList<>(), freshT = new ArrayList<>();
            for (int cur : layerS) for (int next : moves(cur, cap)) if (!seenS[next]) { seenS[next] = true; freshS.add(next); }
            for (int cur : layerT) for (int next : moves(cur, cap)) if (!seenT[next]) { seenT[next] = true; freshT.add(next); }
            for (int v : freshS) if (freshT.contains(v)) return 2 * round;
            layerS = freshS;
            layerT = freshT;
        }
        return -1;
    }

    public static void main(String[] args) {
        if (solve(3, 11, 11) != 4) throw new AssertionError("example 1");
        if (solve(1, 37, 37) != 7) throw new AssertionError("example 2");
        if (solve(3, 11, 1000) != 3) throw new AssertionError("a larger cap shortens the route");
        if (solve(9, 9, 20) != 0) throw new AssertionError("equal ends");
        if (solve(1, 999999, 1000000) != solve(999999, 1, 1000000)) throw new AssertionError("moves are reversible, so distance is symmetric");
        if (layersMustMatch(3, 4, 10) == 1 || solve(3, 4, 10) != 1)
            throw new AssertionError("layer-equality rule must miss the crossing edge");
        Random rnd = new Random(22301);
        int wrongFriend = 0;
        for (int t = 0; t < 3000; t++) {
            int cap = 1 + rnd.nextInt(40);
            int s = 1 + rnd.nextInt(cap), g = 1 + rnd.nextInt(cap);
            int want = oracle(s, g, cap);
            if (solve(s, g, cap) != want) throw new AssertionError("random " + t);
            if (layersMustMatch(s, g, cap) != want) wrongFriend++;
        }
        if (wrongFriend == 0) throw new AssertionError("the false friend should fail somewhere");
        int x = 1_100_000_000;
        if (2 * x >= 0) throw new AssertionError("doubling should overflow");
        if (x <= Integer.MAX_VALUE / 2) throw new AssertionError("guard should reject x");
        if (!(1_000_000 <= Integer.MAX_VALUE / 2)) throw new AssertionError("guard should accept small x");
    }
}
```

#### Solution: [Vary] Detect A Crossing Neighbor (Author exercise)
<!-- id: bv-crossing-neighbor -->

**Approach.** Build the forward adjacency from the arcs, and build a second adjacency from the same arcs with every pair flipped, which the sink side walks. The two distance arrays stay separate. Each round expands the thinner layer, and for every generated neighbor the opposite table is tested before the side's own table, returning the sum of the two distances and the connecting arc. Equal ends return 0 first. The oracle is Floyd-Warshall over all pairs on random directed graphs of at most eight nodes, with self-loops and parallel arcs included. The assertions also check that treating the arcs as undirected turns example 2 from -1 into 3, which is why the reversed adjacency is needed, and that a layers-must-be-equal variant answers -1 on example 1 although the route exists.

**Complexity.** Roughly the work of two searches to half the depth, so on branching graphs it is far below a full one-directional sweep, and no worse than O(n + m) for n nodes and m arcs. The two adjacency structures take O(n + m) memory between them.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

public final class CrossingNeighborSolution {
    static int[][] adjacency(int n, int[][] arcs, boolean flip) {
        int[] count = new int[n];
        for (int[] a : arcs) count[flip ? a[1] : a[0]]++;
        int[][] adj = new int[n][];
        for (int i = 0; i < n; i++) adj[i] = new int[count[i]];
        int[] fill = new int[n];
        for (int[] a : arcs) {
            int from = flip ? a[1] : a[0], to = flip ? a[0] : a[1];
            adj[from][fill[from]++] = to;
        }
        return adj;
    }

    static int solve(int n, int[][] arcs, int source, int sink) {
        if (source == sink) return 0;
        int[][] forward = adjacency(n, arcs, false), backward = adjacency(n, arcs, true);
        int[] distS = new int[n], distT = new int[n];
        Arrays.fill(distS, -1);
        Arrays.fill(distT, -1);
        distS[source] = 0;
        distT[sink] = 0;
        List<Integer> layerS = new ArrayList<>(List.of(source));
        List<Integer> layerT = new ArrayList<>(List.of(sink));
        while (!layerS.isEmpty() && !layerT.isEmpty()) {
            boolean growSource = layerS.size() <= layerT.size();
            List<Integer> layer = growSource ? layerS : layerT;
            int[][] adj = growSource ? forward : backward;
            int[] mine = growSource ? distS : distT;
            int[] other = growSource ? distT : distS;
            List<Integer> fresh = new ArrayList<>();
            for (int cur : layer) {
                for (int next : adj[cur]) {
                    if (other[next] >= 0) return mine[cur] + 1 + other[next];
                    if (mine[next] >= 0) continue;
                    mine[next] = mine[cur] + 1;
                    fresh.add(next);
                }
            }
            if (growSource) layerS = fresh; else layerT = fresh;
        }
        return -1;
    }

    static int oracle(int n, int[][] arcs, int source, int sink) {
        int inf = 1_000_000;
        int[][] d = new int[n][n];
        for (int[] row : d) Arrays.fill(row, inf);
        for (int i = 0; i < n; i++) d[i][i] = 0;
        for (int[] a : arcs) d[a[0]][a[1]] = Math.min(d[a[0]][a[1]], a[0] == a[1] ? 0 : 1);
        for (int k = 0; k < n; k++)
            for (int i = 0; i < n; i++)
                for (int j = 0; j < n; j++)
                    if (d[i][k] + d[k][j] < d[i][j]) d[i][j] = d[i][k] + d[k][j];
        return d[source][sink] >= inf ? -1 : d[source][sink];
    }

    static int layersMustMatch(int n, int[][] arcs, int source, int sink) {
        if (source == sink) return 0;
        int[][] forward = adjacency(n, arcs, false), backward = adjacency(n, arcs, true);
        boolean[] seenS = new boolean[n], seenT = new boolean[n];
        seenS[source] = true;
        seenT[sink] = true;
        List<Integer> layerS = new ArrayList<>(List.of(source));
        List<Integer> layerT = new ArrayList<>(List.of(sink));
        int round = 0;
        while (!layerS.isEmpty() && !layerT.isEmpty()) {
            round++;
            List<Integer> freshS = new ArrayList<>(), freshT = new ArrayList<>();
            for (int cur : layerS) for (int next : forward[cur]) if (!seenS[next]) { seenS[next] = true; freshS.add(next); }
            for (int cur : layerT) for (int next : backward[cur]) if (!seenT[next]) { seenT[next] = true; freshT.add(next); }
            for (int v : freshS) if (freshT.contains(v)) return 2 * round;
            layerS = freshS;
            layerT = freshT;
        }
        return -1;
    }

    public static void main(String[] args) {
        int[][] ex1 = {{0, 1}, {1, 2}, {2, 3}, {0, 4}};
        if (solve(5, ex1, 0, 3) != 3) throw new AssertionError("example 1");
        int[][] ex2 = {{1, 0}, {1, 2}, {2, 3}};
        if (solve(4, ex2, 0, 3) != -1) throw new AssertionError("example 2");
        int[][] both = new int[ex2.length * 2][];
        for (int i = 0; i < ex2.length; i++) { both[2 * i] = ex2[i]; both[2 * i + 1] = new int[] {ex2[i][1], ex2[i][0]}; }
        if (solve(4, both, 0, 3) != 3) throw new AssertionError("undirected reading differs");
        if (layersMustMatch(5, ex1, 0, 3) != -1) throw new AssertionError("layer-equality rule should miss example 1");
        if (solve(1, new int[0][], 0, 0) != 0) throw new AssertionError("single node");
        Random rnd = new Random(22302);
        int missed = 0;
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(8), m = rnd.nextInt(15);
            int[][] arcs = new int[m][];
            for (int i = 0; i < m; i++) arcs[i] = new int[] {rnd.nextInt(n), rnd.nextInt(n)};
            int s = rnd.nextInt(n), g = rnd.nextInt(n);
            int want = oracle(n, arcs, s, g);
            if (solve(n, arcs, s, g) != want) throw new AssertionError("random " + t);
            if (layersMustMatch(n, arcs, s, g) != want) missed++;
        }
        if (missed == 0) throw new AssertionError("false friend should fail on some graph");
    }
}
```

#### Solution: [Boundary] Start Equals Target (Author exercise)
<!-- id: bv-start-equals-target -->

**Approach.** The first line returns 0 when the two ends coincide, before any array is allocated or any edge is read. Otherwise the method builds an undirected adjacency, keeps one distance array per side, and runs the thinner-layer search with the crossing test at generation time. A self-loop is harmless because the node's own entry sits in its own side's table and the opposite table does not hold it. The oracle is an ordinary one-directional BFS over the same adjacency. The assertions confirm that equal ends return 0 even when the edge array is `null`, which shows that nothing was read, that a single merged table which treats any visited node as a meeting wrongly answers 1 on example 2 where the true answer is -1, and that results match the oracle on random multigraphs.

**Complexity.** Two half-depth searches cost on the order of 2 * b^(d/2) node visits on a graph of branching b, and never more than O(n + m) for n nodes and m edges. Building the adjacency also takes O(n + m) time and space.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

public final class StartEqualsTargetSolution {
    static int[][] adjacency(int n, int[][] edges) {
        int[] count = new int[n];
        for (int[] e : edges) { count[e[0]]++; count[e[1]]++; }
        int[][] adj = new int[n][];
        for (int i = 0; i < n; i++) adj[i] = new int[count[i]];
        int[] fill = new int[n];
        for (int[] e : edges) { adj[e[0]][fill[e[0]]++] = e[1]; adj[e[1]][fill[e[1]]++] = e[0]; }
        return adj;
    }

    static int solve(int n, int[][] edges, int a, int b) {
        if (a == b) return 0;
        int[][] adj = adjacency(n, edges);
        int[] distA = new int[n], distB = new int[n];
        Arrays.fill(distA, -1);
        Arrays.fill(distB, -1);
        distA[a] = 0;
        distB[b] = 0;
        List<Integer> layerA = new ArrayList<>(List.of(a));
        List<Integer> layerB = new ArrayList<>(List.of(b));
        while (!layerA.isEmpty() && !layerB.isEmpty()) {
            boolean growA = layerA.size() <= layerB.size();
            List<Integer> layer = growA ? layerA : layerB;
            int[] mine = growA ? distA : distB;
            int[] other = growA ? distB : distA;
            List<Integer> fresh = new ArrayList<>();
            for (int cur : layer) {
                for (int next : adj[cur]) {
                    if (other[next] >= 0) return mine[cur] + 1 + other[next];
                    if (mine[next] >= 0) continue;
                    mine[next] = mine[cur] + 1;
                    fresh.add(next);
                }
            }
            if (growA) layerA = fresh; else layerB = fresh;
        }
        return -1;
    }

    static int oracle(int n, int[][] edges, int a, int b) {
        int[][] adj = adjacency(n, edges);
        int[] dist = new int[n];
        Arrays.fill(dist, -1);
        dist[a] = 0;
        ArrayDeque<Integer> line = new ArrayDeque<>();
        line.add(a);
        while (!line.isEmpty()) {
            int cur = line.poll();
            for (int next : adj[cur]) {
                if (dist[next] >= 0) continue;
                dist[next] = dist[cur] + 1;
                line.add(next);
            }
        }
        return dist[b];
    }

    static int oneSharedTable(int n, int[][] edges, int a, int b) {
        int[][] adj = adjacency(n, edges);
        int[] owner = new int[n], dist = new int[n];
        owner[a] = 1;
        owner[b] = 2;
        List<Integer> layerA = new ArrayList<>(List.of(a));
        List<Integer> layerB = new ArrayList<>(List.of(b));
        while (!layerA.isEmpty() && !layerB.isEmpty()) {
            boolean growA = layerA.size() <= layerB.size();
            List<Integer> layer = growA ? layerA : layerB;
            List<Integer> fresh = new ArrayList<>();
            for (int cur : layer) {
                for (int next : adj[cur]) {
                    if (owner[next] != 0) return dist[cur] + 1 + dist[next];
                    owner[next] = growA ? 1 : 2;
                    dist[next] = dist[cur] + 1;
                    fresh.add(next);
                }
            }
            if (growA) layerA = fresh; else layerB = fresh;
        }
        return -1;
    }

    public static void main(String[] args) {
        if (solve(3, new int[][] {{2, 2}}, 2, 2) != 0) throw new AssertionError("example 1");
        int[][] ex2 = {{0, 0}, {0, 1}, {0, 1}};
        if (solve(3, ex2, 0, 2) != -1) throw new AssertionError("example 2");
        if (solve(1, null, 0, 0) != 0) throw new AssertionError("equal ends must return before reading edges");
        if (oneSharedTable(3, ex2, 0, 2) == -1) throw new AssertionError("shared table should be fooled by the loop");
        Random rnd = new Random(22303);
        for (int t = 0; t < 5000; t++) {
            int n = 1 + rnd.nextInt(9), m = rnd.nextInt(16);
            int[][] edges = new int[m][];
            for (int i = 0; i < m; i++) edges[i] = new int[] {rnd.nextInt(n), rnd.nextInt(n)};
            int a = rnd.nextInt(n), b = rnd.nextInt(n);
            if (solve(n, edges, a, b) != oracle(n, edges, a, b)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Recognize] Word Ladder (LeetCode 127)
<!-- id: bv-word-ladder -->

**Approach.** Words are nodes and two words are neighbors when they differ in one position, but neighbors are generated, not stored: for each position the method tries the 25 other letters and keeps candidates that are in a hash set of the list. If `endWord` is missing from the set the answer is 0. Otherwise it keeps two maps from word to distance, one per end, and each round expands the whole layer of the smaller side. A candidate is looked up in the opposite map first, so the begin word is found even though it need not be in the list, and a hit returns the two distances plus one edge, plus one more because the answer counts words. The oracle is a one-directional BFS over the begin word plus the list, comparing every pair of words letter by letter. The assertions run it on random words of length 3 over three letters, and they confirm the Java hazard that a `String` built from a `char[]` equals the literal but is a different object, so `==` would fail.

**Complexity.** Candidate generation costs O(L * 26) hash lookups of length L per expanded word, so the whole search is O(N * L^2 * 26) in the worst case for N list words, and usually far less because each side stops near half the depth. The two maps and the hash set hold O(N) words.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Random;
import java.util.Set;

public final class WordLadderSolution {
    static int solve(String beginWord, String endWord, List<String> wordList) {
        Set<String> allowed = new HashSet<>(wordList);
        if (!allowed.contains(endWord)) return 0;
        Map<String, Integer> fromBegin = new HashMap<>(), fromEnd = new HashMap<>();
        fromBegin.put(beginWord, 0);
        fromEnd.put(endWord, 0);
        List<String> layerB = new ArrayList<>(List.of(beginWord));
        List<String> layerE = new ArrayList<>(List.of(endWord));
        while (!layerB.isEmpty() && !layerE.isEmpty()) {
            boolean growBegin = layerB.size() <= layerE.size();
            List<String> layer = growBegin ? layerB : layerE;
            Map<String, Integer> mine = growBegin ? fromBegin : fromEnd;
            Map<String, Integer> other = growBegin ? fromEnd : fromBegin;
            List<String> fresh = new ArrayList<>();
            for (String cur : layer) {
                char[] chars = cur.toCharArray();
                for (int i = 0; i < chars.length; i++) {
                    char original = chars[i];
                    for (char ch = 'a'; ch <= 'z'; ch++) {
                        if (ch == original) continue;
                        chars[i] = ch;
                        String cand = new String(chars);
                        if (other.containsKey(cand)) return mine.get(cur) + 1 + other.get(cand) + 1;
                        if (!allowed.contains(cand) || mine.containsKey(cand)) continue;
                        mine.put(cand, mine.get(cur) + 1);
                        fresh.add(cand);
                    }
                    chars[i] = original;
                }
            }
            if (growBegin) layerB = fresh; else layerE = fresh;
        }
        return 0;
    }

    static boolean oneApart(String x, String y) {
        int diff = 0;
        for (int i = 0; i < x.length(); i++) if (x.charAt(i) != y.charAt(i)) diff++;
        return diff == 1;
    }

    static int oracle(String beginWord, String endWord, List<String> wordList) {
        if (!wordList.contains(endWord)) return 0;
        List<String> nodes = new ArrayList<>();
        nodes.add(beginWord);
        for (String w : wordList) if (!w.equals(beginWord)) nodes.add(w);
        int[] dist = new int[nodes.size()];
        java.util.Arrays.fill(dist, -1);
        dist[0] = 0;
        ArrayDeque<Integer> line = new ArrayDeque<>();
        line.add(0);
        while (!line.isEmpty()) {
            int cur = line.poll();
            for (int next = 0; next < nodes.size(); next++) {
                if (dist[next] >= 0 || !oneApart(nodes.get(cur), nodes.get(next))) continue;
                dist[next] = dist[cur] + 1;
                line.add(next);
            }
        }
        int at = nodes.indexOf(endWord);
        return dist[at] < 0 ? 0 : dist[at] + 1;
    }

    public static void main(String[] args) {
        List<String> ex = List.of("cord", "card", "ward", "warm", "word", "wold");
        if (solve("cold", "warm", ex) != 5) throw new AssertionError("example 1");
        List<String> noEnd = List.of("cord", "card", "ward", "word", "wold");
        if (solve("cold", "warm", noEnd) != 0) throw new AssertionError("example 2");
        String built = new String(new char[] {'c', 'a', 't'});
        if (!built.equals("cat")) throw new AssertionError("equals");
        if (built == "cat") throw new AssertionError("a new String is a different object");
        Random rnd = new Random(22304);
        List<String> universe = new ArrayList<>();
        for (char a = 'a'; a <= 'c'; a++) for (char b = 'a'; b <= 'c'; b++) for (char c = 'a'; c <= 'c'; c++)
            universe.add("" + a + b + c);
        int found = 0;
        for (int t = 0; t < 4000; t++) {
            List<String> pool = new ArrayList<>(universe);
            Collections.shuffle(pool, rnd);
            int size = 1 + rnd.nextInt(14);
            List<String> list = new ArrayList<>(pool.subList(0, size));
            String end = rnd.nextInt(5) < 4 ? list.get(rnd.nextInt(size)) : pool.get(26);
            String begin = universe.get(rnd.nextInt(27));
            if (begin.equals(end)) continue;
            int want = oracle(begin, end, list);
            if (solve(begin, end, list) != want) throw new AssertionError("random " + t);
            if (want > 0) found++;
        }
        if (found < 200) throw new AssertionError("tests should include many reachable cases");
    }
}
```
