<!-- solutions-for: 22-bfs-variations -->
### Solutions For Search From Both Ends

#### Solution: [Build] Two-Ended Integer Search (Author exercise)
<!-- id: bv3-two-ended-integer -->

**Approach.**
The method keeps one map from value to distance for each side, `distStart` and `distTarget`, and one frontier list for each side. Each round compares the two frontier sizes and expands the smaller one completely. For every generated value `next`, the method looks `next` up in the opposite map before it stores anything. A hit returns the sum `own.get(cur) + 1 + far`.

The invariant is that before a round, no sequence of `dS + dT` moves or fewer connects the two ends. Here `dS` and `dT` are the depths of the two frontiers. Every hit therefore pairs a state of the current layer with a state at the full opposite depth, and the first hit is the minimum. The code asserts the Java facts it relies on: `Map.get` returns `null` for a missing key, and integer division by 2 of an even number is exact.

**Complexity.**
- **Time** is O(b^(d/2)) with `b = 4` moves per value, and never more than O(limit), because each value enters a map at most once.
- **Space** is O(b^(d/2)) for the two maps and frontiers, bounded by O(limit).

```java run
import java.util.*;

public final class TwoEndedIntegerSearch {
    /** Lists the values reachable from x in one move that stay inside 1..limit. */
    static int[] neighbors(int x, int limit) {
        // At most four moves exist: plus one, minus one, double and halve.
        int[] buffer = new int[4];
        int count = 0;
        // Each candidate is kept only when it lies inside the allowed range.
        if (x + 1 <= limit) buffer[count++] = x + 1;
        if (x - 1 >= 1) buffer[count++] = x - 1;
        if (2L * x <= limit) buffer[count++] = 2 * x;
        // Halving is a move only for even values.
        if (x % 2 == 0) buffer[count++] = x / 2;
        return Arrays.copyOf(buffer, count);
    }

    /**
     * Returns the minimum number of moves from start to target inside 1..limit.
     * Time: O(b^(d/2)), at most O(limit). Space: O(b^(d/2)), at most O(limit).
     * Invariant: no path of length dS + dT or less exists before a round starts.
     */
    static int minMoves(int start, int target, int limit) {
        // Equal ends need no search.
        if (start == target) return 0;
        // Each side owns a distance map, so a value can hold two different distances.
        Map<Integer, Integer> distStart = new HashMap<>();
        Map<Integer, Integer> distTarget = new HashMap<>();
        distStart.put(start, 0);
        distTarget.put(target, 0);
        List<Integer> frontierStart = new ArrayList<>(List.of(start));
        List<Integer> frontierTarget = new ArrayList<>(List.of(target));
        // The loop stops when a side has no value left to expand.
        while (!frontierStart.isEmpty() && !frontierTarget.isEmpty()) {
            // Expanding the smaller frontier keeps the work of the round small.
            boolean fromStart = frontierStart.size() <= frontierTarget.size();
            List<Integer> frontier = fromStart ? frontierStart : frontierTarget;
            Map<Integer, Integer> own = fromStart ? distStart : distTarget;
            Map<Integer, Integer> other = fromStart ? distTarget : distStart;
            List<Integer> nextFrontier = new ArrayList<>();
            // The whole layer is expanded, so all lookups meet complete opposite layers.
            for (int cur : frontier) {
                for (int next : neighbors(cur, limit)) {
                    // The meeting test runs on the generated value, before it is stored.
                    Integer far = other.get(next);
                    if (far != null) return own.get(cur) + 1 + far;
                    // A value already known to this side is skipped.
                    if (own.containsKey(next)) continue;
                    own.put(next, own.get(cur) + 1);
                    nextFrontier.add(next);
                }
            }
            // The new layer becomes the frontier of the side that was expanded.
            if (fromStart) frontierStart = nextFrontier; else frontierTarget = nextFrontier;
        }
        // Unreachable in this exercise, but the failure value keeps the method total.
        return -1;
    }

    /** Brute force: ordinary breadth-first search from the start only. */
    static int oneSided(int start, int target, int limit) {
        int[] dist = new int[limit + 1];
        Arrays.fill(dist, -1);
        ArrayDeque<Integer> queue = new ArrayDeque<>();
        dist[start] = 0;
        queue.add(start);
        while (!queue.isEmpty()) {
            int cur = queue.poll();
            if (cur == target) return dist[cur];
            for (int next : neighbors(cur, limit)) {
                if (dist[next] != -1) continue;
                dist[next] = dist[cur] + 1;
                queue.add(next);
            }
        }
        return -1;
    }

    public static void main(String[] args) {
        // Example 1 has an odd distance, so the two maps never share a value.
        if (minMoves(3, 29, 40) != 5) throw new AssertionError("ex1");
        // Example 2 is a long search where the doubling moves matter.
        if (minMoves(1, 1000, 1000) != 12) throw new AssertionError("ex2");
        // Equal ends return 0 before any search.
        if (minMoves(7, 7, 10) != 0) throw new AssertionError("equal");
        // Java facts used above: a missing key reads as null, and halving an even value is exact.
        if (new HashMap<Integer, Integer>().get(5) != null) throw new AssertionError("null get");
        if (2 * (46 / 2) != 46) throw new AssertionError("even halving");
        // Every move is reversible, which the problem statement promises.
        for (int x = 1; x <= 60; x++) {
            for (int y : neighbors(x, 60)) {
                boolean back = false;
                for (int z : neighbors(y, 60)) if (z == x) back = true;
                if (!back) throw new AssertionError("reverse " + x + " " + y);
            }
        }
        // Random inputs must match the one-sided search exactly.
        Random rnd = new Random(2203);
        for (int t = 0; t < 3000; t++) {
            int limit = 1 + rnd.nextInt(200);
            int s = 1 + rnd.nextInt(limit), g = 1 + rnd.nextInt(limit);
            int want = oneSided(s, g, limit);
            int got = minMoves(s, g, limit);
            if (want != got) throw new AssertionError(s + " " + g + " " + limit + " want " + want + " got " + got);
        }
    }
}
```

#### Solution: [Vary] Detect A Crossing Neighbor (Author exercise)
<!-- id: bv3-crossing-neighbor -->

**Approach.**
The method numbers each cell `r * cols + c` and keeps two `int` arrays filled with -1, one for each side. Each round expands the smaller frontier by one complete layer. When a free neighbor cell has a value of zero or more in the opposite array, the two searches have connected. The method returns the sum of the three parts.

The test runs before the neighbor is written into the own array. This is what finds an odd distance, because two adjacent frontier cells belong to different searches and no cell holds a value in both arrays. The invariant is that every cell with a value in `distStart` has its exact distance from the start, and the same holds for `distTarget`. A new `int[]` holds zeros, so the code asserts that `Arrays.fill` is needed before -1 can mean unseen.

**Complexity.**
- **Time** is O(R * C) in the worst case, because each cell receives a value from each side at most once. It is smaller when the endpoints are close.
- **Space** is O(R * C) for the two arrays, plus the two frontier lists.

```java run
import java.util.*;

public final class CrossingNeighbor {
    /**
     * Returns the fewest moves between two free cells, or -1 when none exists.
     * Time: O(R * C). Space: O(R * C).
     * Invariant: each filled entry holds the exact distance from its own origin.
     */
    static int fewestMoves(int[][] grid, int sr, int sc, int tr, int tc) {
        int rows = grid.length, cols = grid[0].length;
        int startCell = sr * cols + sc, targetCell = tr * cols + tc;
        // The same cell on both ends needs no search.
        if (startCell == targetCell) return 0;
        // The value -1 marks a cell that this side has not reached.
        int[] distStart = new int[rows * cols];
        int[] distTarget = new int[rows * cols];
        Arrays.fill(distStart, -1);
        Arrays.fill(distTarget, -1);
        distStart[startCell] = 0;
        distTarget[targetCell] = 0;
        List<Integer> frontierStart = new ArrayList<>(List.of(startCell));
        List<Integer> frontierTarget = new ArrayList<>(List.of(targetCell));
        int[] dr = {1, -1, 0, 0};
        int[] dc = {0, 0, 1, -1};
        // Both sides need a non-empty frontier; an empty one means that side is enclosed.
        while (!frontierStart.isEmpty() && !frontierTarget.isEmpty()) {
            // The smaller frontier is expanded as a whole layer.
            boolean fromStart = frontierStart.size() <= frontierTarget.size();
            List<Integer> frontier = fromStart ? frontierStart : frontierTarget;
            int[] own = fromStart ? distStart : distTarget;
            int[] other = fromStart ? distTarget : distStart;
            List<Integer> nextFrontier = new ArrayList<>();
            for (int cur : frontier) {
                int r = cur / cols, c = cur % cols;
                // Each cell has four candidate neighbors.
                for (int k = 0; k < 4; k++) {
                    int nr = r + dr[k], nc = c + dc[k];
                    // Cells outside the grid and wall cells are not moves.
                    if (nr < 0 || nr >= rows || nc < 0 || nc >= cols || grid[nr][nc] == 1) continue;
                    int next = nr * cols + nc;
                    // The test uses the generated neighbor, so adjacent frontiers of the two sides connect.
                    if (other[next] >= 0) return own[cur] + 1 + other[next];
                    if (own[next] >= 0) continue;
                    own[next] = own[cur] + 1;
                    nextFrontier.add(next);
                }
            }
            if (fromStart) frontierStart = nextFrontier; else frontierTarget = nextFrontier;
        }
        // One side ran out of cells, so no path exists.
        return -1;
    }

    /** Brute force: breadth-first search from the start cell only. */
    static int oneSided(int[][] grid, int sr, int sc, int tr, int tc) {
        int rows = grid.length, cols = grid[0].length;
        int[][] dist = new int[rows][cols];
        for (int[] row : dist) Arrays.fill(row, -1);
        ArrayDeque<int[]> queue = new ArrayDeque<>();
        dist[sr][sc] = 0;
        queue.add(new int[] {sr, sc});
        int[] dr = {1, -1, 0, 0}, dc = {0, 0, 1, -1};
        while (!queue.isEmpty()) {
            int[] cur = queue.poll();
            for (int k = 0; k < 4; k++) {
                int nr = cur[0] + dr[k], nc = cur[1] + dc[k];
                if (nr < 0 || nr >= rows || nc < 0 || nc >= cols || grid[nr][nc] == 1 || dist[nr][nc] != -1) continue;
                dist[nr][nc] = dist[cur[0]][cur[1]] + 1;
                queue.add(new int[] {nr, nc});
            }
        }
        return dist[tr][tc];
    }

    public static void main(String[] args) {
        // Example 1 has an odd distance around a wall.
        int[][] g1 = {{0, 0, 0, 0}, {1, 1, 0, 1}, {0, 0, 0, 0}};
        if (fewestMoves(g1, 0, 0, 2, 3) != 5) throw new AssertionError("ex1");
        // Example 2 encloses the target, so the answer is -1.
        int[][] g2 = {{0, 1, 0}, {1, 0, 1}, {0, 1, 0}};
        if (fewestMoves(g2, 0, 0, 1, 1) != -1) throw new AssertionError("ex2");
        // Adjacent cells connect through one generated neighbor, and equal cells return 0.
        if (fewestMoves(g1, 0, 0, 0, 1) != 1) throw new AssertionError("adjacent");
        if (fewestMoves(g1, 0, 0, 0, 0) != 0) throw new AssertionError("equal");
        // A new int array holds zeros, which is why the code fills -1 explicitly.
        int[] fresh = new int[3];
        if (fresh[0] != 0 || fresh[2] != 0) throw new AssertionError("zeros");
        // Random grids must match the one-sided search.
        Random rnd = new Random(2231);
        for (int t = 0; t < 3000; t++) {
            int rows = 1 + rnd.nextInt(6), cols = 1 + rnd.nextInt(6);
            int[][] grid = new int[rows][cols];
            for (int[] row : grid) for (int c = 0; c < cols; c++) row[c] = rnd.nextInt(10) < 3 ? 1 : 0;
            int sr = rnd.nextInt(rows), sc = rnd.nextInt(cols), tr = rnd.nextInt(rows), tc = rnd.nextInt(cols);
            grid[sr][sc] = 0;
            grid[tr][tc] = 0;
            int want = oneSided(grid, sr, sc, tr, tc);
            int got = fewestMoves(grid, sr, sc, tr, tc);
            if (want != got) throw new AssertionError(Arrays.deepToString(grid) + " want " + want + " got " + got);
        }
    }
}
```

#### Solution: [Boundary] Start Equals Target (Author exercise)
<!-- id: bv3-start-equals-target -->

**Approach.**
The method answers the equal case first, because the minimum edge count from a vertex to itself is 0. Without that line, both arrays hold the same vertex at 0. The second round then generates a neighbor that the opposite array holds at distance 1, and the method returns 2 for any vertex that has a neighbor. After that, the method builds `adj`, creates two separate distance arrays, and runs rounds from queues of each side.

A round uses `queue.size()` as the layer width, so vertices added during the round wait for the next one. Each side expands the queue with fewer vertices. When a side has no vertex left, the two origins are in different components, and the method returns -1. The invariant is that each array holds exact distances from its own origin for every discovered vertex. The code asserts that `ArrayDeque.poll` returns `null` on an empty queue, which is why the loop checks `isEmpty` first.

**Complexity.**
- **Time** is O(V + E), because each vertex enters each side at most once and each adjacency entry is read at most twice.
- **Space** is O(V + E) for `adj`, plus O(V) for the two arrays and two queues.

```java run
import java.util.*;

public final class StartEqualsTarget {
    /**
     * Returns the fewest edges between start and target, 0 if equal, or -1 if no path exists.
     * Time: O(V + E). Space: O(V + E).
     * Invariant: each array holds exact distances from its own origin for discovered vertices.
     */
    static int edgeCount(int n, int[][] edges, int start, int target) {
        // The answer for equal ends is known before anything is built.
        if (start == target) return 0;
        List<List<Integer>> adj = new ArrayList<>();
        for (int v = 0; v < n; v++) adj.add(new ArrayList<>());
        // Each undirected edge is stored in both directions.
        for (int[] e : edges) { adj.get(e[0]).add(e[1]); adj.get(e[1]).add(e[0]); }
        // Two arrays keep the origins logically distinct.
        int[] fromStart = new int[n];
        int[] fromTarget = new int[n];
        Arrays.fill(fromStart, -1);
        Arrays.fill(fromTarget, -1);
        ArrayDeque<Integer> startQueue = new ArrayDeque<>();
        ArrayDeque<Integer> targetQueue = new ArrayDeque<>();
        fromStart[start] = 0;
        fromTarget[target] = 0;
        startQueue.add(start);
        targetQueue.add(target);
        // The search ends when a side cannot grow any more.
        while (!startQueue.isEmpty() && !targetQueue.isEmpty()) {
            // The side with fewer queued vertices takes the next round.
            boolean useStart = startQueue.size() <= targetQueue.size();
            ArrayDeque<Integer> queue = useStart ? startQueue : targetQueue;
            int[] own = useStart ? fromStart : fromTarget;
            int[] other = useStart ? fromTarget : fromStart;
            // The width is fixed before the round, so the round expands one whole layer.
            int width = queue.size();
            for (int i = 0; i < width; i++) {
                int cur = queue.poll();
                for (int next : adj.get(cur)) {
                    // A generated vertex that the other side holds ends the search.
                    if (other[next] >= 0) return own[cur] + 1 + other[next];
                    if (own[next] >= 0) continue;
                    own[next] = own[cur] + 1;
                    queue.add(next);
                }
            }
        }
        // A side with no queued vertex means the origins lie in different components.
        return -1;
    }

    /** Brute force: breadth-first search from the start only. */
    static int oneSided(int n, int[][] edges, int start, int target) {
        List<List<Integer>> adj = new ArrayList<>();
        for (int v = 0; v < n; v++) adj.add(new ArrayList<>());
        for (int[] e : edges) { adj.get(e[0]).add(e[1]); adj.get(e[1]).add(e[0]); }
        int[] dist = new int[n];
        Arrays.fill(dist, -1);
        ArrayDeque<Integer> queue = new ArrayDeque<>();
        dist[start] = 0;
        queue.add(start);
        while (!queue.isEmpty()) {
            int cur = queue.poll();
            for (int next : adj.get(cur)) {
                if (dist[next] != -1) continue;
                dist[next] = dist[cur] + 1;
                queue.add(next);
            }
        }
        return dist[target];
    }

    public static void main(String[] args) {
        // Example 1 is an isolated vertex asked about itself.
        if (edgeCount(3, new int[][] {{0, 1}}, 2, 2) != 0) throw new AssertionError("ex1");
        // Example 2 has the two origins in different components.
        if (edgeCount(5, new int[][] {{0, 1}, {1, 2}, {3, 4}}, 0, 4) != -1) throw new AssertionError("ex2");
        // A single edge has an odd distance and connects through one generated neighbor.
        if (edgeCount(2, new int[][] {{0, 1}}, 0, 1) != 1) throw new AssertionError("one edge");
        // Java fact used above: poll on an empty deque returns null.
        if (new ArrayDeque<Integer>().poll() != null) throw new AssertionError("poll null");
        // Random graphs, including equal and unreachable pairs, must match the one-sided search.
        Random rnd = new Random(2247);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(9);
            List<int[]> es = new ArrayList<>();
            for (int a = 0; a < n; a++) for (int b = a + 1; b < n; b++) if (rnd.nextInt(4) == 0) es.add(new int[] {a, b});
            Collections.shuffle(es, rnd);
            int[][] arr = es.toArray(new int[0][]);
            int s = rnd.nextInt(n), g = rnd.nextInt(n);
            int want = oneSided(n, arr, s, g);
            int got = edgeCount(n, arr, s, g);
            if (want != got) throw new AssertionError(n + " " + s + " " + g + " want " + want + " got " + got);
        }
    }
}
```

#### Solution: [Recognize] Word Ladder (LeetCode 127)
<!-- id: bv3-word-ladder -->

**Approach.**
The method returns 0 at once when `endWord` is not in the list, because the last word of a sequence must belong to it. Otherwise it keeps a map from word to distance for each side, with `beginWord` at 0 in the first map and `endWord` at 0 in the second. A neighbor of a word is a string that differs in one position and belongs to the word set. The method generates it by trying all 26 letters at each position.

Each round expands the smaller frontier by a whole layer and tests every generated neighbor against the opposite map. A hit returns the number of moves plus 1, because a sequence has one more word than it has moves. The invariant is that no sequence with `dS + dT` moves or fewer exists before a round, so the first hit is minimal. The code asserts that `String.charAt` indexes from 0 and that `HashSet.contains` compares by content.

**Complexity.**
- **Time** is O(W * L * 26) in the worst case for `W` words of length `L`, and it is far smaller when the two layers connect early.
- **Space** is O(W * L) for the word set, the two maps and the frontiers.

```java run
import java.util.*;

public final class WordLadder {
    /**
     * Returns the number of words in the shortest sequence, or 0 if none exists.
     * Time: O(W * L * 26). Space: O(W * L).
     * Invariant: no sequence of dS + dT moves or fewer exists before a round starts.
     */
    static int ladderLength(String beginWord, String endWord, List<String> wordList) {
        Set<String> words = new HashSet<>(wordList);
        // The last word of a sequence must belong to the list.
        if (!words.contains(endWord)) return 0;
        Map<String, Integer> distBegin = new HashMap<>();
        Map<String, Integer> distEnd = new HashMap<>();
        distBegin.put(beginWord, 0);
        distEnd.put(endWord, 0);
        List<String> frontierBegin = new ArrayList<>(List.of(beginWord));
        List<String> frontierEnd = new ArrayList<>(List.of(endWord));
        // A side with no frontier cannot reach the other side any more.
        while (!frontierBegin.isEmpty() && !frontierEnd.isEmpty()) {
            // The smaller frontier is expanded completely.
            boolean fromBegin = frontierBegin.size() <= frontierEnd.size();
            List<String> frontier = fromBegin ? frontierBegin : frontierEnd;
            Map<String, Integer> own = fromBegin ? distBegin : distEnd;
            Map<String, Integer> other = fromBegin ? distEnd : distBegin;
            List<String> nextFrontier = new ArrayList<>();
            for (String cur : frontier) {
                char[] chars = cur.toCharArray();
                // Each position is changed to every other letter in turn.
                for (int i = 0; i < chars.length; i++) {
                    char original = chars[i];
                    for (char ch = 'a'; ch <= 'z'; ch++) {
                        if (ch == original) continue;
                        chars[i] = ch;
                        String next = new String(chars);
                        // Only dictionary words are legal states.
                        if (!words.contains(next)) continue;
                        // The meeting test runs on the generated word; words count one more than moves.
                        Integer far = other.get(next);
                        if (far != null) return own.get(cur) + 1 + far + 1;
                        if (own.containsKey(next)) continue;
                        own.put(next, own.get(cur) + 1);
                        nextFrontier.add(next);
                    }
                    // The position is restored before the next position is changed.
                    chars[i] = original;
                }
            }
            if (fromBegin) frontierBegin = nextFrontier; else frontierEnd = nextFrontier;
        }
        return 0;
    }

    /** Brute force: breadth-first search from beginWord only. */
    static int oneSided(String beginWord, String endWord, List<String> wordList) {
        Set<String> words = new HashSet<>(wordList);
        Map<String, Integer> dist = new HashMap<>();
        ArrayDeque<String> queue = new ArrayDeque<>();
        dist.put(beginWord, 1);
        queue.add(beginWord);
        while (!queue.isEmpty()) {
            String cur = queue.poll();
            if (cur.equals(endWord)) return dist.get(cur);
            for (String w : words) {
                int diff = 0;
                for (int i = 0; i < w.length(); i++) if (w.charAt(i) != cur.charAt(i)) diff++;
                if (diff == 1 && !dist.containsKey(w)) { dist.put(w, dist.get(cur) + 1); queue.add(w); }
            }
        }
        return 0;
    }

    public static void main(String[] args) {
        // Example 1 is a five-word sequence with an odd move count.
        if (ladderLength("cold", "warm", List.of("cord", "card", "ward", "warm", "word", "wood", "worm")) != 5) throw new AssertionError("ex1");
        // Example 2 has no end word in the list.
        if (ladderLength("cat", "dog", List.of("cot", "cog", "dot", "dig")) != 0) throw new AssertionError("ex2");
        // Java facts used above: charAt starts at 0, and a set compares strings by content.
        if ("abc".charAt(0) != 'a') throw new AssertionError("charAt");
        if (!new HashSet<>(List.of("ab")).contains(new String(new char[] {'a', 'b'}))) throw new AssertionError("content");
        // Random dictionaries over a small alphabet must match the one-sided search.
        Random rnd = new Random(2259);
        for (int t = 0; t < 3000; t++) {
            int len = 1 + rnd.nextInt(4);
            int size = 1 + rnd.nextInt(12);
            Set<String> set = new LinkedHashSet<>();
            for (int i = 0; i < size; i++) set.add(randomWord(rnd, len));
            List<String> list = new ArrayList<>(set);
            String begin = randomWord(rnd, len), end = rnd.nextInt(4) == 0 ? randomWord(rnd, len) : list.get(rnd.nextInt(list.size()));
            if (begin.equals(end)) continue;
            int want = oneSided(begin, end, list);
            // The brute force counts the end word only when it is a listed word.
            if (!set.contains(end)) want = 0;
            int got = ladderLength(begin, end, list);
            if (want != got) throw new AssertionError(begin + " " + end + " " + list + " want " + want + " got " + got);
        }
    }

    /** Builds a random word from the letters a, b and c. */
    static String randomWord(Random rnd, int len) {
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < len; i++) sb.append((char) ('a' + rnd.nextInt(3)));
        return sb.toString();
    }
}
```
