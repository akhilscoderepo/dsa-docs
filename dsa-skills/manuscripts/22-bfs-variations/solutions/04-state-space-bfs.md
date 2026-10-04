<!-- solutions-for: 04-state-space-bfs -->
### State-Space BFS

#### Solution: [Build] Combination-Lock States (Author exercise)
<!-- id: bv-lock-neighbors -->

**Approach.** Copy the string into a `char[]`, and for each wheel save the digit, write the lowered digit, record a string, write the raised digit, record a string, and put the saved digit back. The wrap is done with `(digit + 9) % 10` for down and `(digit + 1) % 10` for up, so no branch is needed. The oracle ignores wheels entirely: it lists every digit string of the same length and keeps those that differ from the input in exactly one position by plus or minus one modulo ten, then compares the two answers as sets and checks the stated order separately by recomputing each entry from its index. The assertions also confirm three Java claims from the lesson: `charAt(i) + 1` has type `int`, two equal strings built separately are `equals` but not `==`, and forgetting to restore the wheel corrupts every later neighbor.

**Complexity.** The routine writes 2W strings of W characters for W wheels, so it takes O(W^2) time and O(W^2) memory for the output, which is at most 36 characters per string for the largest allowed lock.

```java run
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Random;
import java.util.Set;

public final class LockStatesSolution {
    static List<String> solve(String state) {
        List<String> out = new ArrayList<>(2 * state.length());
        char[] wheels = state.toCharArray();
        for (int i = 0; i < wheels.length; i++) {
            char keep = wheels[i];
            wheels[i] = (char) ('0' + (keep - '0' + 9) % 10);
            out.add(new String(wheels));
            wheels[i] = (char) ('0' + (keep - '0' + 1) % 10);
            out.add(new String(wheels));
            wheels[i] = keep;
        }
        return out;
    }

    static List<String> withoutRestore(String state) {
        List<String> out = new ArrayList<>();
        char[] wheels = state.toCharArray();
        for (int i = 0; i < wheels.length; i++) {
            char keep = wheels[i];
            wheels[i] = (char) ('0' + (keep - '0' + 9) % 10);
            out.add(new String(wheels));
            wheels[i] = (char) ('0' + (keep - '0' + 1) % 10);
            out.add(new String(wheels));
        }
        return out;
    }

    static Set<String> oracle(String state) {
        int w = state.length(), total = 1;
        for (int i = 0; i < w; i++) total *= 10;
        Set<String> out = new HashSet<>();
        for (int v = 0; v < total; v++) {
            String cand = String.format("%0" + w + "d", v);
            int diff = 0;
            boolean ok = true;
            for (int i = 0; i < w; i++) {
                int a = state.charAt(i) - '0', b = cand.charAt(i) - '0';
                if (a == b) continue;
                diff++;
                if ((a + 1) % 10 != b && (b + 1) % 10 != a) ok = false;
            }
            if (ok && diff == 1) out.add(cand);
        }
        return out;
    }

    public static void main(String[] args) {
        if (!solve("042").equals(List.of("942", "142", "032", "052", "041", "043")))
            throw new AssertionError("example 1");
        if (!solve("90").equals(List.of("80", "00", "99", "91"))) throw new AssertionError("example 2");
        if (!solve("0").equals(List.of("9", "1"))) throw new AssertionError("one wheel");
        Object plus = "4".charAt(0) + 1;
        if (!(plus instanceof Integer) || (Integer) plus != 53) throw new AssertionError("char plus int is int");
        String built = new String("0042");
        if (built == "0042" || !built.equals("0042")) throw new AssertionError("identity versus equals");
        if (withoutRestore("042").equals(solve("042"))) throw new AssertionError("missing restore must corrupt");
        Random rnd = new Random(22401);
        for (int t = 0; t < 600; t++) {
            int w = 1 + rnd.nextInt(4);
            StringBuilder sb = new StringBuilder();
            for (int i = 0; i < w; i++) sb.append((char) ('0' + rnd.nextInt(10)));
            String s = sb.toString();
            String before = s;
            List<String> got = solve(s);
            if (!s.equals(before)) throw new AssertionError("input changed");
            if (got.size() != 2 * w || new HashSet<>(got).size() != 2 * w) throw new AssertionError("size " + s);
            if (!new HashSet<>(got).equals(oracle(s))) throw new AssertionError("set " + s);
            for (int i = 0; i < w; i++) {
                int d = s.charAt(i) - '0';
                String down = s.substring(0, i) + (d + 9) % 10 + s.substring(i + 1);
                String up = s.substring(0, i) + (d + 1) % 10 + s.substring(i + 1);
                if (!got.get(2 * i).equals(down) || !got.get(2 * i + 1).equals(up))
                    throw new AssertionError("order " + s + " wheel " + i);
            }
        }
    }
}
```

#### Solution: [Vary] Open The Lock (LeetCode 752)
<!-- id: bv-open-lock -->

**Approach.** The vertices are digit strings, and the generator from the Build rung supplies the edges. If `"0000"` is itself listed, the answer is -1 straight away. Otherwise the search advances one whole layer at a time, with a counter that goes up once per layer, and marks a string in the seen set the moment it is queued, so the earliest arrival is also the shortest. The listed settings are loaded into the same seen set up front, which gives one gate instead of two. The oracle relaxes distances over all 10^w settings until nothing changes, which has no queue at all, and the two agree on random locks of one to three wheels with random listed settings, plus a few full four-wheel locks. The fixed asserts cover both examples, a listed start, a listed target and an unreachable target boxed in by listed neighbors.

**Complexity.** Each of at most 10,000 settings is queued once and expands into eight neighbors of four characters each, so the work is O(10^W * W) in general and about a third of a million character operations for four wheels, plus O(D) to load D listed settings.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashSet;
import java.util.List;
import java.util.Random;
import java.util.Set;

public final class OpenLockSolution {
    static List<String> around(String s) {
        List<String> out = new ArrayList<>();
        for (int i = 0; i < s.length(); i++) {
            int d = s.charAt(i) - '0';
            out.add(s.substring(0, i) + (d + 9) % 10 + s.substring(i + 1));
            out.add(s.substring(0, i) + (d + 1) % 10 + s.substring(i + 1));
        }
        return out;
    }

    static int solve(String[] deadends, String target) {
        String start = "0".repeat(target.length());
        Set<String> seen = new HashSet<>(Arrays.asList(deadends));
        if (seen.contains(start)) return -1;
        ArrayDeque<String> layer = new ArrayDeque<>();
        layer.add(start);
        seen.add(start);
        int turns = 0;
        while (!layer.isEmpty()) {
            for (int left = layer.size(); left > 0; left--) {
                String cur = layer.poll();
                if (cur.equals(target)) return turns;
                for (String next : around(cur)) {
                    if (seen.add(next)) layer.add(next);
                }
            }
            turns++;
        }
        return -1;
    }

    static int oracle(String[] deadends, String target) {
        int w = target.length(), total = 1;
        for (int i = 0; i < w; i++) total *= 10;
        boolean[] bad = new boolean[total];
        for (String d : deadends) bad[Integer.parseInt(d)] = true;
        int inf = Integer.MAX_VALUE / 2, goal = Integer.parseInt(target);
        if (bad[0] || bad[goal]) return -1;
        int[] dist = new int[total];
        Arrays.fill(dist, inf);
        dist[0] = 0;
        boolean moved = true;
        while (moved) {
            moved = false;
            for (int v = total - 1; v >= 0; v--) {
                if (bad[v]) continue;
                String s = String.format("%0" + w + "d", v);
                for (String n : around(s)) {
                    int u = Integer.parseInt(n);
                    if (!bad[u] && dist[u] + 1 < dist[v]) { dist[v] = dist[u] + 1; moved = true; }
                }
            }
        }
        return dist[goal] >= inf ? -1 : dist[goal];
    }

    public static void main(String[] args) {
        if (solve(new String[] {"0100", "1000", "0010"}, "1230") != 8) throw new AssertionError("example 1");
        if (solve(new String[] {"1000", "9000", "2000"}, "3000") != 5) throw new AssertionError("example 2");
        if (solve(new String[] {"0000"}, "0001") != -1) throw new AssertionError("listed start");
        if (solve(new String[] {"0202"}, "0202") != -1) throw new AssertionError("listed target");
        String[] boxed = {"1000", "9000", "0100", "0900", "0010", "0090", "0001", "0009"};
        if (solve(boxed, "5555") != -1) throw new AssertionError("boxed in");
        Random rnd = new Random(22402);
        for (int t = 0; t < 500; t++) {
            int w = 1 + rnd.nextInt(3), total = 1;
            for (int i = 0; i < w; i++) total *= 10;
            int count = 1 + rnd.nextInt(Math.max(1, total / 2));
            Set<String> dead = new HashSet<>();
            for (int i = 0; i < count; i++) dead.add(String.format("%0" + w + "d", rnd.nextInt(total)));
            String target = String.format("%0" + w + "d", 1 + rnd.nextInt(total - 1 > 0 ? total - 1 : 1));
            String[] arr = dead.toArray(new String[0]);
            if (solve(arr, target) != oracle(arr, target)) throw new AssertionError("random " + t);
        }
        for (int t = 0; t < 12; t++) {
            Set<String> dead = new HashSet<>();
            for (int i = 0; i < 2500; i++) dead.add(String.format("%04d", rnd.nextInt(10000)));
            String target = String.format("%04d", 1 + rnd.nextInt(9999));
            String[] arr = dead.toArray(new String[0]);
            if (solve(arr, target) != oracle(arr, target)) throw new AssertionError("four wheels " + t);
        }
    }
}
```

#### Solution: [Boundary] Forbidden Start And Target (Author exercise)
<!-- id: bv-forbidden-ends -->

**Approach.** Settle the three contract cases before the queue exists: a forbidden start returns -1 even if it equals the target, a forbidden target returns -1, and an allowed start equal to the target returns 0. After that the search is ordinary, but this version encodes a setting as one `int` whose decimal digits are the wheels, using `10^p` as the place value of wheel `p`, and keeps a `boolean[]` of size 10^W instead of a set of strings. That is a different encoding that holds exactly the same facts, so the visited table is still complete. The oracle relaxes distances to a fixpoint on lists of up to three wheels with a heavy share of forbidden entries, so the edge cases appear constantly, and the assertions cover both examples and the three contract cases by name.

**Complexity.** Every setting is queued at most once and tries 2W neighbors, giving O(10^W * W) time, and the visited table and queue use O(10^W) memory, which is one million booleans at the six-wheel limit.

```java run
import java.util.ArrayDeque;
import java.util.Arrays;
import java.util.Random;

public final class ForbiddenEndsSolution {
    static int solve(String start, String target, String[] forbidden) {
        int w = start.length(), total = 1;
        for (int i = 0; i < w; i++) total *= 10;
        boolean[] barred = new boolean[total];
        for (String f : forbidden) barred[Integer.parseInt(f)] = true;
        int from = Integer.parseInt(start), goal = Integer.parseInt(target);
        if (barred[from] || barred[goal]) return -1;
        if (from == goal) return 0;
        boolean[] seen = new boolean[total];
        seen[from] = true;
        ArrayDeque<Integer> frontier = new ArrayDeque<>();
        frontier.add(from);
        int clicks = 0;
        while (!frontier.isEmpty()) {
            clicks++;
            for (int left = frontier.size(); left > 0; left--) {
                int cur = frontier.poll();
                int place = 1;
                for (int p = 0; p < w; p++, place *= 10) {
                    int digit = cur / place % 10;
                    int base = cur - digit * place;
                    for (int step : new int[] {9, 1}) {
                        int next = base + (digit + step) % 10 * place;
                        if (barred[next] || seen[next]) continue;
                        if (next == goal) return clicks;
                        seen[next] = true;
                        frontier.add(next);
                    }
                }
            }
        }
        return -1;
    }

    static int oracle(String start, String target, String[] forbidden) {
        int w = start.length(), total = 1;
        for (int i = 0; i < w; i++) total *= 10;
        boolean[] bad = new boolean[total];
        for (String f : forbidden) bad[Integer.parseInt(f)] = true;
        int from = Integer.parseInt(start), goal = Integer.parseInt(target), inf = Integer.MAX_VALUE / 2;
        if (bad[from] || bad[goal]) return -1;
        int[] dist = new int[total];
        Arrays.fill(dist, inf);
        dist[from] = 0;
        boolean moved = true;
        while (moved) {
            moved = false;
            for (int v = 0; v < total; v++) {
                if (bad[v]) continue;
                String s = String.format("%0" + w + "d", v);
                for (int i = 0; i < w; i++) {
                    int d = s.charAt(i) - '0';
                    for (int step : new int[] {9, 1}) {
                        String n = s.substring(0, i) + (d + step) % 10 + s.substring(i + 1);
                        int u = Integer.parseInt(n);
                        if (!bad[u] && dist[u] + 1 < dist[v]) { dist[v] = dist[u] + 1; moved = true; }
                    }
                }
            }
        }
        return dist[goal] >= inf ? -1 : dist[goal];
    }

    public static void main(String[] args) {
        if (solve("55", "55", new String[] {"55"}) != -1) throw new AssertionError("example 1");
        if (solve("7", "3", new String[] {"4", "6"}) != 6) throw new AssertionError("example 2");
        if (solve("123", "123", new String[0]) != 0) throw new AssertionError("equal and allowed");
        if (solve("123", "124", new String[] {"124"}) != -1) throw new AssertionError("forbidden target");
        if (solve("000", "000", new String[] {"000"}) != -1) throw new AssertionError("forbidden start equals target");
        if (solve("0000", "0009", new String[] {"0001", "0002"}) != 1) throw new AssertionError("wrap is one click");
        Random rnd = new Random(22403);
        for (int t = 0; t < 1500; t++) {
            int w = 1 + rnd.nextInt(3), total = 1;
            for (int i = 0; i < w; i++) total *= 10;
            int count = rnd.nextInt(Math.max(1, total * 6 / 10));
            String[] arr = new String[count];
            for (int i = 0; i < count; i++) arr[i] = String.format("%0" + w + "d", rnd.nextInt(total));
            String a = String.format("%0" + w + "d", rnd.nextInt(total));
            String b = rnd.nextInt(8) == 0 ? a : String.format("%0" + w + "d", rnd.nextInt(total));
            if (solve(a, b, arr) != oracle(a, b, arr)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Recognize] Shortest Path In Binary Matrix (LeetCode 1091)
<!-- id: bv-binary-matrix-count -->

**Approach.** The state is just the cell, since the eight moves never depend on the route taken, so a flat cell code is a complete encoding. The search keeps two tables, `len` for the layer a cell was first reached in and `ways` for the number of shortest routes into it. A neighbor that is new gets its length and a zero count; then, whenever its length equals the current cell's length plus one, the current cell's count is added to it, which covers the first parent and every later parent in the same layer. A cell expanded later has its count final, because all of its parents sit in the previous layer and every one of them was expanded earlier. The oracle shares nothing with this: Floyd-Warshall gives the shortest length between the corners, and the count is the entry of the adjacency matrix raised to that power, since a walk with the minimum number of moves cannot repeat a cell. The assertions also run the counting rule that only looks at first arrivals and require it to disagree with the oracle on a fixed grid, and they run the key-door corridor from the applicability stage, where marking only the cell fails and marking cell plus key succeeds.

**Complexity.** There are n squared cells and each looks at eight neighbors, so time is O(n^2) and the two tables and queue use O(n^2) memory. The count is exact because `long` holds it for every grid in the stated limit.

```java run
import java.util.ArrayDeque;
import java.util.Arrays;
import java.util.Random;

public final class BinaryMatrixCountSolution {
    static long[] solve(int[][] grid) {
        int n = grid.length;
        if (grid[0][0] == 1 || grid[n - 1][n - 1] == 1) return new long[] {-1, 0};
        int[] len = new int[n * n];
        long[] ways = new long[n * n];
        ArrayDeque<Integer> line = new ArrayDeque<>();
        len[0] = 1;
        ways[0] = 1;
        line.add(0);
        while (!line.isEmpty()) {
            int cur = line.poll();
            int r = cur / n, c = cur % n;
            for (int dr = -1; dr <= 1; dr++) {
                for (int dc = -1; dc <= 1; dc++) {
                    int nr = r + dr, nc = c + dc;
                    if ((dr == 0 && dc == 0) || nr < 0 || nr >= n || nc < 0 || nc >= n) continue;
                    if (grid[nr][nc] == 1) continue;
                    int nx = nr * n + nc;
                    if (len[nx] == 0) {
                        len[nx] = len[cur] + 1;
                        line.add(nx);
                    }
                    if (len[nx] == len[cur] + 1) ways[nx] += ways[cur];
                }
            }
        }
        int goal = n * n - 1;
        return len[goal] == 0 ? new long[] {-1, 0} : new long[] {len[goal], ways[goal]};
    }

    static long[] firstArrivalOnly(int[][] grid) {
        int n = grid.length;
        if (grid[0][0] == 1 || grid[n - 1][n - 1] == 1) return new long[] {-1, 0};
        int[] len = new int[n * n];
        long[] ways = new long[n * n];
        ArrayDeque<Integer> line = new ArrayDeque<>();
        len[0] = 1;
        ways[0] = 1;
        line.add(0);
        while (!line.isEmpty()) {
            int cur = line.poll();
            int r = cur / n, c = cur % n;
            for (int dr = -1; dr <= 1; dr++) {
                for (int dc = -1; dc <= 1; dc++) {
                    int nr = r + dr, nc = c + dc;
                    if ((dr == 0 && dc == 0) || nr < 0 || nr >= n || nc < 0 || nc >= n) continue;
                    if (grid[nr][nc] == 1 || len[nr * n + nc] != 0) continue;
                    len[nr * n + nc] = len[cur] + 1;
                    ways[nr * n + nc] = ways[cur];
                    line.add(nr * n + nc);
                }
            }
        }
        int goal = n * n - 1;
        return len[goal] == 0 ? new long[] {-1, 0} : new long[] {len[goal], ways[goal]};
    }

    static long[] oracle(int[][] grid) {
        int n = grid.length, v = n * n, inf = 1_000_000;
        if (grid[0][0] == 1 || grid[n - 1][n - 1] == 1) return new long[] {-1, 0};
        long[][] adj = new long[v][v];
        int[][] d = new int[v][v];
        for (int[] row : d) Arrays.fill(row, inf);
        for (int a = 0; a < v; a++) {
            if (grid[a / n][a % n] == 1) continue;
            d[a][a] = 0;
            for (int b = 0; b < v; b++) {
                if (a == b || grid[b / n][b % n] == 1) continue;
                if (Math.abs(a / n - b / n) <= 1 && Math.abs(a % n - b % n) <= 1) { adj[a][b] = 1; d[a][b] = 1; }
            }
        }
        for (int k = 0; k < v; k++)
            for (int i = 0; i < v; i++)
                for (int j = 0; j < v; j++)
                    if (d[i][k] + d[k][j] < d[i][j]) d[i][j] = d[i][k] + d[k][j];
        int moves = d[0][v - 1];
        if (moves >= inf) return new long[] {-1, 0};
        long[][] pow = new long[v][v];
        for (int i = 0; i < v; i++) pow[i][i] = 1;
        for (int step = 0; step < moves; step++) {
            long[][] next = new long[v][v];
            for (int i = 0; i < v; i++)
                for (int k = 0; k < v; k++) {
                    if (pow[i][k] == 0) continue;
                    for (int j = 0; j < v; j++) next[i][j] += pow[i][k] * adj[k][j];
                }
            pow = next;
        }
        return new long[] {moves + 1, pow[0][v - 1]};
    }

    // key-door corridor: 'S' start, 'T' target, 'D' door, 'K' key, '.' floor
    static int corridor(String row, boolean trackKey) {
        int s = row.indexOf('S'), n = row.length();
        int[][] dist = new int[n][2];
        for (int[] x : dist) Arrays.fill(x, -1);
        ArrayDeque<int[]> q = new ArrayDeque<>();
        dist[s][0] = 0;
        q.add(new int[] {s, 0});
        while (!q.isEmpty()) {
            int[] cur = q.poll();
            int pos = cur[0], key = cur[1];
            if (row.charAt(pos) == 'T') return dist[pos][key];
            for (int step = -1; step <= 1; step += 2) {
                int np = pos + step;
                if (np < 0 || np >= n) continue;
                char ch = row.charAt(np);
                if (ch == 'D' && key == 0) continue;
                int nk = (ch == 'K') ? 1 : key;
                int slot = trackKey ? nk : 0;
                if (!trackKey && dist[np][0] != -1) continue;
                if (trackKey && dist[np][slot] != -1) continue;
                dist[np][slot] = dist[pos][trackKey ? key : 0] + 1;
                q.add(new int[] {np, trackKey ? nk : (ch == 'K' ? 1 : key)});
            }
        }
        return -1;
    }

    static int[][] randomGrid(Random rnd, int n, int percent) {
        int[][] g = new int[n][n];
        for (int r = 0; r < n; r++)
            for (int c = 0; c < n; c++) g[r][c] = rnd.nextInt(100) < percent ? 1 : 0;
        return g;
    }

    public static void main(String[] args) {
        int[][] e1 = {{0, 0, 0}, {0, 1, 0}, {0, 0, 0}};
        int[][] e2 = {{0, 0, 1, 0}, {0, 0, 0, 0}, {1, 0, 1, 0}, {0, 0, 0, 0}};
        if (!Arrays.equals(solve(e1), new long[] {4, 2})) throw new AssertionError("example 1");
        if (!Arrays.equals(solve(e2), new long[] {5, 4})) throw new AssertionError("example 2");
        if (!Arrays.equals(solve(new int[][] {{0}}), new long[] {1, 1})) throw new AssertionError("one cell");
        if (!Arrays.equals(solve(new int[][] {{1}}), new long[] {-1, 0})) throw new AssertionError("blocked one cell");
        if (!Arrays.equals(solve(new int[][] {{0, 0}, {0, 1}}), new long[] {-1, 0})) throw new AssertionError("blocked end");
        if (!Arrays.equals(solve(new int[][] {{0, 1}, {1, 0}}), new long[] {2, 1})) throw new AssertionError("diagonal only");
        if (Arrays.equals(firstArrivalOnly(e1), oracle(e1))) throw new AssertionError("false friend must fail on e1");
        if (Arrays.equals(firstArrivalOnly(e2), oracle(e2))) throw new AssertionError("false friend must fail on e2");
        if (corridor("TD.S.K", true) != 7) throw new AssertionError("cell plus key");
        if (corridor("TD.S.K", false) != -1) throw new AssertionError("cell only must fail");
        Random rnd = new Random(22404);
        int multi = 0;
        for (int t = 0; t < 1500; t++) {
            int n = 1 + rnd.nextInt(t < 1300 ? 4 : 5);
            int[][] g = randomGrid(rnd, n, 15 + rnd.nextInt(30));
            if (rnd.nextInt(6) > 0) { g[0][0] = 0; g[n - 1][n - 1] = 0; }
            int[][] copy = new int[n][];
            for (int r = 0; r < n; r++) copy[r] = g[r].clone();
            long[] got = solve(g), want = oracle(g);
            if (!Arrays.equals(got, want)) throw new AssertionError("random " + t + Arrays.toString(got) + Arrays.toString(want));
            if (!Arrays.deepEquals(copy, g)) throw new AssertionError("grid modified");
            if (got[1] > 1) multi++;
        }
        if (multi < 30) throw new AssertionError("random grids rarely had several shortest paths: " + multi);
    }
}
```
