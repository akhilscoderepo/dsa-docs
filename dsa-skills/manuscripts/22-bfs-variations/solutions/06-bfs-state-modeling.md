<!-- solutions-for: 06-bfs-state-modeling -->
### BFS State Modeling

#### Solution: [Build] Rotting Oranges (LeetCode 994)
<!-- id: bs-rot-walls-untouched -->

**Approach.** Every rotten orange goes into the queue first, with time 0, and the count of fresh oranges is taken at the same moment. Taking a cell from the queue looks at its four side neighbours, and a neighbour is entered only if it is inside the grid, is fresh and has no time yet. Walls and empty cells fail the fresh test, so they stop the spread without any special case. Each discovery lowers the fresh count and raises the answer to the new time if that is larger, which means the minute counter can never run past the last real rot, and a grid where nothing rots reports 0 minutes. The oracle ignores queues: it gives every fresh cell an infinite time and repeats a pass over the grid, setting each fresh cell to one more than its smallest neighbouring time, until a pass changes nothing. The assertions replay both examples, compare 3000 random grids with all four cell kinds, and confirm that the input is left unchanged.

**Complexity.** One visit per cell with four neighbour checks each, so the time is O(rows * columns), and the time table and the queue use O(rows * columns) memory.

```java run
import java.util.ArrayDeque;
import java.util.Arrays;
import java.util.Random;

public final class RotWallsUntouched {
    static int[] solve(int[][] g) {
        int h = g.length, w = g[0].length, fresh = 0, minutes = 0;
        int[][] t = new int[h][w];
        ArrayDeque<int[]> q = new ArrayDeque<>();
        for (int r = 0; r < h; r++)
            for (int c = 0; c < w; c++) {
                t[r][c] = -1;
                if (g[r][c] == 2) { t[r][c] = 0; q.add(new int[]{r, c}); }
                if (g[r][c] == 1) fresh++;
            }
        int[] dr = {1, -1, 0, 0}, dc = {0, 0, 1, -1};
        while (!q.isEmpty()) {
            int[] cur = q.poll();
            for (int d = 0; d < 4; d++) {
                int a = cur[0] + dr[d], b = cur[1] + dc[d];
                if (a < 0 || a >= h || b < 0 || b >= w || g[a][b] != 1 || t[a][b] >= 0) continue;
                t[a][b] = t[cur[0]][cur[1]] + 1;
                minutes = Math.max(minutes, t[a][b]);
                fresh--;
                q.add(new int[]{a, b});
            }
        }
        return new int[]{minutes, fresh};
    }

    static int[] oracle(int[][] g) {
        int h = g.length, w = g[0].length, inf = 1 << 20;
        int[][] t = new int[h][w];
        for (int r = 0; r < h; r++)
            for (int c = 0; c < w; c++) t[r][c] = g[r][c] == 2 ? 0 : inf;
        int[] dr = {1, -1, 0, 0}, dc = {0, 0, 1, -1};
        boolean changed = true;
        while (changed) {
            changed = false;
            for (int r = 0; r < h; r++)
                for (int c = 0; c < w; c++) {
                    if (g[r][c] != 1) continue;
                    for (int d = 0; d < 4; d++) {
                        int a = r + dr[d], b = c + dc[d];
                        if (a < 0 || a >= h || b < 0 || b >= w || t[a][b] >= inf) continue;
                        if (t[a][b] + 1 < t[r][c]) { t[r][c] = t[a][b] + 1; changed = true; }
                    }
                }
        }
        int minutes = 0, left = 0;
        for (int r = 0; r < h; r++)
            for (int c = 0; c < w; c++) {
                if (g[r][c] != 1) continue;
                if (t[r][c] >= inf) left++; else minutes = Math.max(minutes, t[r][c]);
            }
        return new int[]{minutes, left};
    }

    public static void main(String[] args) {
        if (!Arrays.equals(solve(new int[][]{{2, 1, 1}, {1, 3, 1}, {0, 1, 1}}), new int[]{5, 0})) throw new AssertionError("example 1");
        if (!Arrays.equals(solve(new int[][]{{2, 3, 1}, {3, 3, 1}, {0, 1, 1}}), new int[]{0, 4})) throw new AssertionError("example 2");
        if (!Arrays.equals(solve(new int[][]{{1, 0, 1}}), new int[]{0, 2})) throw new AssertionError("no rotten orange");
        if (!Arrays.equals(solve(new int[][]{{0, 3}}), new int[]{0, 0})) throw new AssertionError("nothing to rot");
        Random rnd = new Random(22601);
        for (int t = 0; t < 3000; t++) {
            int h = 1 + rnd.nextInt(5), w = 1 + rnd.nextInt(5);
            int[][] g = new int[h][w];
            for (int[] row : g) for (int c = 0; c < w; c++) row[c] = new int[]{0, 1, 1, 1, 2, 3}[rnd.nextInt(6)];
            int[][] copy = new int[h][];
            for (int r = 0; r < h; r++) copy[r] = g[r].clone();
            int[] got = solve(g), want = oracle(g);
            if (!Arrays.equals(got, want)) throw new AssertionError("differs on " + Arrays.deepToString(g));
            if (!Arrays.deepEquals(copy, g)) throw new AssertionError("input changed");
        }
    }
}
```

#### Solution: [Vary] 01 Matrix (LeetCode 542)
<!-- id: bs-torus-nearest-zero -->

**Approach.** All zeros start in the queue at distance 0 and every other cell starts at -1, which doubles as the visited mark. A neighbour is found with `Math.floorMod(row + step, rows)` and the same for columns, so the position one step left of column 0 is the last column and the vertex is always a position inside the grid. A neighbour that still holds -1 gets the current distance plus one and joins the queue. A grid with no zero never enqueues anything and the table of -1 is returned unchanged. The oracle sets zeros to 0 and everything else to a large number, and repeats passes that lower each cell to its smallest wrapped neighbour plus one until nothing changes, with -1 written for cells that stayed large. The assertions check both examples, one-row and one-column grids where a wrapped neighbour is the cell itself or its twin, 3000 random grids, and three Java claims: `-1 % 5` is -1, `Math.floorMod(-1, 5)` is 4, and the false friend that tests bounds instead of wrapping gives a different table on the first example.

**Complexity.** Every cell is queued at most once and examines four neighbours, so the time is O(rows * columns) with the same amount of memory for the table and the queue.

```java run
import java.util.ArrayDeque;
import java.util.Arrays;
import java.util.Random;

public final class TorusNearestZero {
    static int[][] solve(int[][] g) {
        int h = g.length, w = g[0].length;
        int[][] dist = new int[h][w];
        ArrayDeque<int[]> q = new ArrayDeque<>();
        for (int r = 0; r < h; r++)
            for (int c = 0; c < w; c++) {
                dist[r][c] = -1;
                if (g[r][c] == 0) { dist[r][c] = 0; q.add(new int[]{r, c}); }
            }
        int[] dr = {1, -1, 0, 0}, dc = {0, 0, 1, -1};
        while (!q.isEmpty()) {
            int[] cur = q.poll();
            for (int d = 0; d < 4; d++) {
                int a = Math.floorMod(cur[0] + dr[d], h), b = Math.floorMod(cur[1] + dc[d], w);
                if (dist[a][b] != -1) continue;
                dist[a][b] = dist[cur[0]][cur[1]] + 1;
                q.add(new int[]{a, b});
            }
        }
        return dist;
    }

    static int[][] plainBounds(int[][] g) {
        int h = g.length, w = g[0].length;
        int[][] dist = new int[h][w];
        ArrayDeque<int[]> q = new ArrayDeque<>();
        for (int r = 0; r < h; r++)
            for (int c = 0; c < w; c++) {
                dist[r][c] = -1;
                if (g[r][c] == 0) { dist[r][c] = 0; q.add(new int[]{r, c}); }
            }
        int[] dr = {1, -1, 0, 0}, dc = {0, 0, 1, -1};
        while (!q.isEmpty()) {
            int[] cur = q.poll();
            for (int d = 0; d < 4; d++) {
                int a = cur[0] + dr[d], b = cur[1] + dc[d];
                if (a < 0 || a >= h || b < 0 || b >= w || dist[a][b] != -1) continue;
                dist[a][b] = dist[cur[0]][cur[1]] + 1;
                q.add(new int[]{a, b});
            }
        }
        return dist;
    }

    static int[][] oracle(int[][] g) {
        int h = g.length, w = g[0].length, inf = 1 << 20;
        int[][] d = new int[h][w];
        for (int r = 0; r < h; r++)
            for (int c = 0; c < w; c++) d[r][c] = g[r][c] == 0 ? 0 : inf;
        boolean changed = true;
        while (changed) {
            changed = false;
            for (int r = 0; r < h; r++)
                for (int c = 0; c < w; c++) {
                    int best = d[r][c];
                    best = Math.min(best, d[(r + 1) % h][c] + 1);
                    best = Math.min(best, d[(r + h - 1) % h][c] + 1);
                    best = Math.min(best, d[r][(c + 1) % w] + 1);
                    best = Math.min(best, d[r][(c + w - 1) % w] + 1);
                    if (best < d[r][c]) { d[r][c] = best; changed = true; }
                }
        }
        for (int r = 0; r < h; r++)
            for (int c = 0; c < w; c++) if (d[r][c] >= inf) d[r][c] = -1;
        return d;
    }

    public static void main(String[] args) {
        int[][] one = {{1, 1, 1, 1}, {0, 1, 1, 1}, {1, 1, 1, 1}};
        if (!Arrays.deepEquals(solve(one), new int[][]{{1, 2, 3, 2}, {0, 1, 2, 1}, {1, 2, 3, 2}})) throw new AssertionError("example 1");
        if (!Arrays.deepEquals(solve(new int[][]{{1, 1}, {1, 1}}), new int[][]{{-1, -1}, {-1, -1}})) throw new AssertionError("example 2");
        if (!Arrays.deepEquals(solve(new int[][]{{1, 1, 1, 0}}), new int[][]{{1, 2, 1, 0}})) throw new AssertionError("one row wraps");
        if (-1 % 5 != -1) throw new AssertionError("remainder keeps the sign of the dividend");
        if (Math.floorMod(-1, 5) != 4) throw new AssertionError("floorMod wraps");
        boolean threw = false;
        try {
            int[] row = new int[5];
            int ignored = row[(0 - 1) % 5];
        } catch (ArrayIndexOutOfBoundsException e) { threw = true; }
        if (!threw) throw new AssertionError("negative remainder index must fail");
        if (Arrays.deepEquals(plainBounds(one), solve(one))) throw new AssertionError("false friend must differ");
        Random rnd = new Random(22602);
        for (int t = 0; t < 3000; t++) {
            int h = 1 + rnd.nextInt(5), w = 1 + rnd.nextInt(5);
            int[][] g = new int[h][w];
            int zeroChance = rnd.nextInt(4) == 0 ? 0 : 1 + rnd.nextInt(4);
            for (int[] row : g) for (int c = 0; c < w; c++) row[c] = zeroChance == 0 || rnd.nextInt(5) >= zeroChance ? 1 : 0;
            if (!Arrays.deepEquals(solve(g), oracle(g))) throw new AssertionError("differs on " + Arrays.deepToString(g));
        }
    }
}
```

#### Solution: [Boundary] Shortest Path in Binary Matrix (LeetCode 1091)
<!-- id: bs-diagonal-cells-on-shortest -->

**Approach.** If either end is blocked the answer is `[-1, 0]` at once. Otherwise one sweep starts at the top-left cell and another starts at the bottom-right cell, each over open cells with eight directions, and each cell records its distance in cells with the start cell counting 1. If the far corner was not reached, the answer is again `[-1, 0]`. Otherwise the length is the far corner's distance from the first sweep, and a cell lies on some shortest path exactly when its two distances add up to the length plus one, since the cell itself is counted by both. The count of such cells is the second number. A 1 by 1 open grid gives `[1, 1]`. The oracle builds a Floyd-Warshall table of steps between all open cells and counts the cells whose steps from the start and to the end sum to the shortest number of steps. The assertions replay the examples, compare 3000 random grids, and check the false friend, which follows one parent per cell back from the end and so counts only 6 cells in the first example where 10 are right.

**Complexity.** Two sweeps with eight neighbour checks per cell give O(n^2) time for an n by n grid, and the two distance tables use O(n^2) memory.

```java run
import java.util.ArrayDeque;
import java.util.Arrays;
import java.util.Random;

public final class DiagonalShortestCells {
    static int[][] sweep(int[][] g, int sr, int sc) {
        int n = g.length;
        int[][] dist = new int[n][n];
        for (int[] row : dist) Arrays.fill(row, -1);
        dist[sr][sc] = 1;
        ArrayDeque<int[]> q = new ArrayDeque<>();
        q.add(new int[]{sr, sc});
        while (!q.isEmpty()) {
            int[] cur = q.poll();
            for (int dr = -1; dr <= 1; dr++)
                for (int dc = -1; dc <= 1; dc++) {
                    int a = cur[0] + dr, b = cur[1] + dc;
                    if ((dr == 0 && dc == 0) || a < 0 || a >= n || b < 0 || b >= n) continue;
                    if (g[a][b] != 0 || dist[a][b] != -1) continue;
                    dist[a][b] = dist[cur[0]][cur[1]] + 1;
                    q.add(new int[]{a, b});
                }
        }
        return dist;
    }

    static int[] solve(int[][] g) {
        int n = g.length;
        if (g[0][0] != 0 || g[n - 1][n - 1] != 0) return new int[]{-1, 0};
        int[][] from = sweep(g, 0, 0), to = sweep(g, n - 1, n - 1);
        int len = from[n - 1][n - 1];
        if (len == -1) return new int[]{-1, 0};
        int cells = 0;
        for (int r = 0; r < n; r++)
            for (int c = 0; c < n; c++)
                if (from[r][c] != -1 && to[r][c] != -1 && from[r][c] + to[r][c] == len + 1) cells++;
        return new int[]{len, cells};
    }

    static int[] oneParentTrace(int[][] g) {
        int n = g.length;
        if (g[0][0] != 0 || g[n - 1][n - 1] != 0) return new int[]{-1, 0};
        int[][] from = sweep(g, 0, 0);
        if (from[n - 1][n - 1] == -1) return new int[]{-1, 0};
        int r = n - 1, c = n - 1, cells = 1;
        while (from[r][c] > 1) {
            boolean moved = false;
            for (int dr = -1; dr <= 1 && !moved; dr++)
                for (int dc = -1; dc <= 1 && !moved; dc++) {
                    int a = r + dr, b = c + dc;
                    if ((dr == 0 && dc == 0) || a < 0 || a >= n || b < 0 || b >= n) continue;
                    if (from[a][b] == from[r][c] - 1) { r = a; c = b; moved = true; }
                }
            cells++;
        }
        return new int[]{from[n - 1][n - 1], cells};
    }

    static int[] oracle(int[][] g) {
        int n = g.length, inf = 1 << 20, m = n * n;
        if (g[0][0] != 0 || g[n - 1][n - 1] != 0) return new int[]{-1, 0};
        int[][] d = new int[m][m];
        for (int i = 0; i < m; i++) {
            Arrays.fill(d[i], inf);
            d[i][i] = 0;
        }
        for (int i = 0; i < m; i++)
            for (int j = 0; j < m; j++) {
                int r1 = i / n, c1 = i % n, r2 = j / n, c2 = j % n;
                boolean near = i != j && Math.abs(r1 - r2) <= 1 && Math.abs(c1 - c2) <= 1;
                if (near && g[r1][c1] == 0 && g[r2][c2] == 0) d[i][j] = 1;
            }
        for (int k = 0; k < m; k++)
            for (int i = 0; i < m; i++)
                for (int j = 0; j < m; j++) d[i][j] = Math.min(d[i][j], d[i][k] + d[k][j]);
        int end = m - 1;
        if (d[0][end] >= inf) return new int[]{-1, 0};
        int cells = 0;
        for (int v = 0; v < m; v++) if (d[0][v] + d[v][end] == d[0][end]) cells++;
        return new int[]{d[0][end] + 1, cells};
    }

    public static void main(String[] args) {
        int[][] ring = {{0, 0, 0, 0}, {0, 1, 1, 0}, {0, 1, 1, 0}, {0, 0, 0, 0}};
        if (!Arrays.equals(solve(ring), new int[]{6, 10})) throw new AssertionError("example 1");
        if (!Arrays.equals(solve(new int[][]{{0, 0}, {0, 1}}), new int[]{-1, 0})) throw new AssertionError("example 2");
        if (!Arrays.equals(solve(new int[][]{{0}}), new int[]{1, 1})) throw new AssertionError("single open cell");
        if (!Arrays.equals(solve(new int[][]{{1}}), new int[]{-1, 0})) throw new AssertionError("single blocked cell");
        if (!Arrays.equals(solve(new int[][]{{0, 1}, {1, 0}}), new int[]{2, 2})) throw new AssertionError("diagonal step");
        if (!Arrays.equals(oneParentTrace(ring), new int[]{6, 6})) throw new AssertionError("false friend counts one path");
        Random rnd = new Random(22603);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(5);
            int[][] g = new int[n][n];
            int pct = 10 + rnd.nextInt(50);
            for (int[] row : g) for (int c = 0; c < n; c++) row[c] = rnd.nextInt(100) < pct ? 1 : 0;
            if (!Arrays.equals(solve(g), oracle(g))) throw new AssertionError("differs on " + Arrays.deepToString(g));
        }
    }
}
```

#### Solution: [Recognize] Word Ladder (LeetCode 127)
<!-- id: bs-ladder-count -->

**Approach.** The search runs one layer at a time. For each word of the current layer it tries every one-letter change, and a candidate that is in the list and was not finalized in an earlier layer is added to this layer's parent lists, with the current word as one more parent. Words are marked final only when the layer ends, so a candidate reached by two words of the same layer keeps both parents. The search stops after the layer in which the target appears. The ways to each word are then the sum of the ways of its parents, taken in layer order, with 1 for the start word, and the answer is the ways of the target, or 0 when it never appears or is not in the list. The layer count also gives the ladder length in words, and the solution asserts that a bidirectional search from both ends, which expands the smaller side and stops when the two sides touch, finds the same length. The oracle shares no code with the search: it builds a Floyd-Warshall table over the start word and the list, then counts ladders by a pass over words in order of their distance from the start, adding up the counts of neighbours that are exactly one step closer. The assertions replay both examples, compare 3000 random registries over a three-letter alphabet, and check the false friend that marks words on discovery, which keeps only the first parent and returns 1 on the second example where 2 is right. They also check that `Integer.MAX_VALUE + 1` becomes negative, which is why the counts are held in `long`.

**Complexity.** Each word is expanded once with 26 * L candidate strings of length L, so the time is O(V * L * L * 26) counting the cost of building and hashing each candidate, and the parent lists add at most one entry per pair of adjacent words, within O(V * L * 26) memory.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.HashSet;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Random;
import java.util.Set;

public final class LadderCount {
    static long lastLength;

    static List<String> neighbours(String s, Set<String> known) {
        List<String> out = new ArrayList<>();
        char[] t = s.toCharArray();
        for (int i = 0; i < t.length; i++) {
            char keep = t[i];
            for (char x = 'a'; x <= 'z'; x++) {
                if (x == keep) continue;
                t[i] = x;
                String n = new String(t);
                if (known.contains(n)) out.add(n);
            }
            t[i] = keep;
        }
        return out;
    }

    static long solve(String start, String target, List<String> list, boolean markEarly) {
        Set<String> known = new HashSet<>(list);
        lastLength = 0;
        if (!known.contains(target)) return 0;
        Map<String, Long> ways = new HashMap<>();
        Set<String> sealed = new HashSet<>();
        ways.put(start, 1L);
        sealed.add(start);
        List<String> layer = List.of(start);
        int words = 1;
        while (!layer.isEmpty() && !ways.containsKey(target)) {
            Map<String, List<String>> parents = new LinkedHashMap<>();
            Set<String> early = new HashSet<>();
            for (String s : layer)
                for (String n : neighbours(s, known)) {
                    if (sealed.contains(n)) continue;
                    if (markEarly && !early.add(n)) continue;
                    parents.computeIfAbsent(n, k -> new ArrayList<>()).add(s);
                }
            for (Map.Entry<String, List<String>> e : parents.entrySet()) {
                long sum = 0;
                for (String p : e.getValue()) sum += ways.get(p);
                ways.put(e.getKey(), sum);
            }
            sealed.addAll(parents.keySet());
            layer = new ArrayList<>(parents.keySet());
            words++;
        }
        if (!ways.containsKey(target)) return 0;
        lastLength = words;
        return ways.get(target);
    }

    static int bidirectional(String start, String target, List<String> list) {
        Set<String> known = new HashSet<>(list);
        if (!known.contains(target)) return 0;
        Set<String> a = new HashSet<>(List.of(start)), z = new HashSet<>(List.of(target));
        Set<String> seen = new HashSet<>(a);
        seen.addAll(z);
        int len = 1;
        while (!a.isEmpty() && !z.isEmpty()) {
            if (a.size() > z.size()) { Set<String> tmp = a; a = z; z = tmp; }
            Set<String> next = new HashSet<>();
            for (String s : a) {
                char[] t = s.toCharArray();
                for (int i = 0; i < t.length; i++) {
                    char keep = t[i];
                    for (char x = 'a'; x <= 'z'; x++) {
                        if (x == keep) continue;
                        t[i] = x;
                        String n = new String(t);
                        if (z.contains(n)) return len + 1;
                        if (known.contains(n) && seen.add(n)) next.add(n);
                    }
                    t[i] = keep;
                }
            }
            a = next;
            len++;
        }
        return 0;
    }

    static boolean oneApart(String x, String y) {
        int diff = 0;
        for (int i = 0; i < x.length(); i++) if (x.charAt(i) != y.charAt(i)) diff++;
        return diff == 1;
    }

    static long[] oracle(String start, String target, List<String> list) {
        if (!list.contains(target)) return new long[]{0, 0};
        List<String> nodes = new ArrayList<>();
        nodes.add(start);
        for (String w : list) if (!w.equals(start)) nodes.add(w);
        int m = nodes.size(), inf = 1 << 20;
        int[][] d = new int[m][m];
        for (int i = 0; i < m; i++)
            for (int j = 0; j < m; j++) d[i][j] = i == j ? 0 : (oneApart(nodes.get(i), nodes.get(j)) ? 1 : inf);
        for (int k = 0; k < m; k++)
            for (int i = 0; i < m; i++)
                for (int j = 0; j < m; j++) d[i][j] = Math.min(d[i][j], d[i][k] + d[k][j]);
        int goal = nodes.indexOf(target);
        if (d[0][goal] >= inf) return new long[]{0, 0};
        long[] count = new long[m];
        count[0] = 1;
        for (int step = 1; step <= d[0][goal]; step++)
            for (int v = 0; v < m; v++) {
                if (d[0][v] != step) continue;
                for (int u = 0; u < m; u++) if (d[0][u] == step - 1 && d[u][v] == 1) count[v] += count[u];
            }
        return new long[]{count[goal], d[0][goal] + 1};
    }

    public static void main(String[] args) {
        List<String> reg = List.of("pat", "pet", "pot", "rot", "ret", "ren", "pen", "ten");
        if (solve("rat", "pen", reg, false) != 3) throw new AssertionError("example 1");
        if (lastLength != 4 || bidirectional("rat", "pen", reg) != 4) throw new AssertionError("length of example 1");
        List<String> two = List.of("ab", "ba", "bb");
        if (solve("aa", "bb", two, false) != 2) throw new AssertionError("example 2");
        if (solve("aa", "bb", two, true) != 1) throw new AssertionError("false friend keeps only the first parent");
        if (solve("aa", "bb", List.of("ab", "ba"), false) != 0) throw new AssertionError("target missing from list");
        if (solve("aa", "cc", List.of("ab", "cc"), false) != 0) throw new AssertionError("no ladder");
        if (Integer.MAX_VALUE + 1 >= 0) throw new AssertionError("int overflow wraps negative");
        Random rnd = new Random(22604);
        for (int t = 0; t < 3000; t++) {
            int len = 2 + rnd.nextInt(2);
            List<String> pool = new ArrayList<>();
            int total = len == 2 ? 9 : 27;
            for (int i = 0; i < total; i++) {
                StringBuilder sb = new StringBuilder();
                int v = i;
                for (int k = 0; k < len; k++) { sb.append((char) ('a' + v % 3)); v /= 3; }
                pool.add(sb.toString());
            }
            List<String> list = new ArrayList<>();
            for (String w : pool) if (rnd.nextInt(100) < 55) list.add(w);
            String start = pool.get(rnd.nextInt(total)), target = pool.get(rnd.nextInt(total));
            if (start.equals(target)) continue;
            long got = solve(start, target, list, false);
            long[] want = oracle(start, target, list);
            if (got != want[0]) throw new AssertionError("count differs on " + start + " " + target + " " + list);
            if (got > 0 && lastLength != want[1]) throw new AssertionError("layer length differs");
            if (bidirectional(start, target, list) != (got > 0 ? want[1] : 0)) throw new AssertionError("bidirectional length differs on " + start + " " + target + " " + list);
        }
    }
}
```
