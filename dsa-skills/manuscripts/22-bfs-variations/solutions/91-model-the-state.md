<!-- solutions-for: 22-bfs-variations -->
### Solutions For Modeling The State

#### Solution: [Build] Rot Everything And Name The Last Cell (LeetCode 994)
<!-- id: bv9-rot-last-cell -->

**Approach.**
The start set holds every rotten cell, and the state key is the cell id `r * cols + c`. The method marks each rotten cell and queues it before the first removal, so all sources sit in layer 0. One layer is one minute: the method reads `queue.size()` at the top of the loop and processes exactly that many cells before it counts a minute.

While a layer runs, the method records the smallest id among the cells that this layer newly rots. A layer that rots nothing does not count as a minute, so the final layer of the search, which finds no fresh orange, leaves `minutes` and `lastCell` alone. The invariant is that after each layer, `minutes` equals the number of layers that rotted at least one cell, and `lastCell` is the smallest id rotted in the latest such layer. The method finishes with a check of the `fresh` counter, because an orange that no search reached keeps the counter above zero and the answer becomes -1.

**Complexity.**
- **Time** is O(rows * cols), because each cell enters the queue at most once and tests four neighbors.
- **Space** is O(rows * cols), because the `visited` array and the queue each scale with the table.

```java run
import java.util.ArrayDeque;
import java.util.Arrays;
import java.util.Random;

public final class RotLastCell {
    /**
     * Returns {minutes, row, col} for the last cell to rot, or {-1, -1, -1} when a fresh orange never rots.
     * With no fresh orange at all, the result is {0, -1, -1}.
     * Time: O(rows * cols), because each cell is queued at most once.
     * Space: O(rows * cols), because of the visited array and the queue.
     * Invariant: after each layer, minutes counts layers that rotted a cell and lastCell is the smallest id of the latest such layer.
     */
    static int[] rotAll(int[][] grid) {
        int rows = grid.length, cols = grid[0].length;
        // One flag per cell id; a rotten cell is marked before it is queued.
        boolean[] visited = new boolean[rows * cols];
        ArrayDeque<Integer> queue = new ArrayDeque<>();
        int fresh = 0;
        // Scan every cell once to build the start set and to count the fresh oranges.
        for (int id = 0; id < rows * cols; id++) {
            int value = grid[id / cols][id % cols];
            // Every rotten cell starts in layer 0.
            if (value == 2) { visited[id] = true; queue.add(id); }
            // A fresh cell must be reached later, so it is counted.
            else if (value == 1) fresh++;
        }
        int minutes = 0, lastCell = -1;
        int[] dr = {1, -1, 0, 0}, dc = {0, 0, 1, -1};
        // Each pass of this loop handles one whole layer.
        while (!queue.isEmpty()) {
            // The queue size now is the size of the current layer, so cells added below wait for the next pass.
            int layerSize = queue.size();
            int firstNew = -1;
            for (int i = 0; i < layerSize; i++) {
                int cur = queue.poll();
                // Four side neighbors are the move rule of this contract.
                for (int k = 0; k < 4; k++) {
                    int nr = cur / cols + dr[k], nc = cur % cols + dc[k];
                    // Bounds check first.
                    if (nr < 0 || nr >= rows || nc < 0 || nc >= cols) continue;
                    int id = nr * cols + nc;
                    // Only an unreached fresh orange rots; empty cells and rotten cells are skipped.
                    if (grid[nr][nc] != 1 || visited[id]) continue;
                    // Mark when found, then queue.
                    visited[id] = true;
                    fresh--;
                    queue.add(id);
                    // Keep the smallest id rotted in this layer, which is the row-major first.
                    if (firstNew == -1 || id < firstNew) firstNew = id;
                }
            }
            // A layer that rotted nothing is not a minute.
            if (firstNew != -1) { minutes++; lastCell = firstNew; }
        }
        // A fresh orange that no search reached makes the task impossible.
        if (fresh > 0) return new int[] {-1, -1, -1};
        // No fresh orange at all means zero minutes and no last cell.
        if (lastCell == -1) return new int[] {0, -1, -1};
        return new int[] {minutes, lastCell / cols, lastCell % cols};
    }

    /** Oracle: simulates one minute at a time on a copy of the grid. */
    static int[] oracle(int[][] grid) {
        int rows = grid.length, cols = grid[0].length;
        int[][] g = new int[rows][];
        for (int r = 0; r < rows; r++) g[r] = grid[r].clone();
        int minutes = 0, lastCell = -1;
        while (true) {
            // Collect, in row-major order, every fresh orange that touches a rotten one now.
            int first = -1, count = 0;
            boolean[][] flip = new boolean[rows][cols];
            for (int r = 0; r < rows; r++) for (int c = 0; c < cols; c++) {
                if (g[r][c] != 1) continue;
                boolean near = (r > 0 && g[r - 1][c] == 2) || (r + 1 < rows && g[r + 1][c] == 2)
                        || (c > 0 && g[r][c - 1] == 2) || (c + 1 < cols && g[r][c + 1] == 2);
                if (near) { flip[r][c] = true; count++; if (first == -1) first = r * cols + c; }
            }
            if (count == 0) break;
            for (int r = 0; r < rows; r++) for (int c = 0; c < cols; c++) if (flip[r][c]) g[r][c] = 2;
            minutes++;
            lastCell = first;
        }
        for (int[] row : g) for (int v : row) if (v == 1) return new int[] {-1, -1, -1};
        if (lastCell == -1) return new int[] {0, -1, -1};
        return new int[] {minutes, lastCell / cols, lastCell % cols};
    }

    public static void main(String[] args) {
        // Example 1: one source, four minutes, and the last cell is the corner.
        if (!Arrays.equals(rotAll(new int[][] {{2, 1, 1}, {1, 1, 0}, {0, 1, 1}}), new int[] {4, 2, 2})) throw new AssertionError("example 1");
        // Example 2: two sources and a two-cell tie in the last minute; the row-major first cell wins.
        if (!Arrays.equals(rotAll(new int[][] {{2, 1, 0, 1}, {1, 1, 0, 1}, {0, 1, 1, 2}}), new int[] {2, 0, 3})) throw new AssertionError("example 2");
        // A fresh orange cut off by empty cells gives -1.
        if (!Arrays.equals(rotAll(new int[][] {{2, 1, 1}, {0, 1, 1}, {1, 0, 1}}), new int[] {-1, -1, -1})) throw new AssertionError("unreachable");
        // No fresh orange gives zero minutes and no cell, even with no rotten orange either.
        if (!Arrays.equals(rotAll(new int[][] {{0, 2}}), new int[] {0, -1, -1})) throw new AssertionError("no fresh");
        if (!Arrays.equals(rotAll(new int[][] {{0}}), new int[] {0, -1, -1})) throw new AssertionError("empty cell only");
        // A fresh orange with no rotten orange anywhere is unreachable.
        if (!Arrays.equals(rotAll(new int[][] {{1}}), new int[] {-1, -1, -1})) throw new AssertionError("no source");
        // The method must leave the input unchanged.
        int[][] keep = {{2, 1}, {1, 0}};
        rotAll(keep);
        if (!Arrays.deepEquals(keep, new int[][] {{2, 1}, {1, 0}})) throw new AssertionError("mutation");
        // Random tables against the minute-by-minute simulation.
        Random rnd = new Random(2201);
        for (int t = 0; t < 4000; t++) {
            int rows = 1 + rnd.nextInt(5), cols = 1 + rnd.nextInt(5);
            int[][] g = new int[rows][cols];
            for (int[] row : g) for (int j = 0; j < cols; j++) row[j] = rnd.nextInt(3);
            if (!Arrays.equals(rotAll(g), oracle(g))) throw new AssertionError("random " + t + " " + Arrays.deepToString(g));
        }
    }
}
```

#### Solution: [Vary] Distance To The Nearest Zero Around Walls (LeetCode 542)
<!-- id: bv9-nearest-zero-walls -->

**Approach.**
The start set holds every cell with value 0, each at distance 0, and the state key is again the cell id. Wall cells never enter the queue and never receive a distance, so the move rule gains one condition: a neighbor must hold 1 and must be unreached. The answer table starts filled with -1, and the same -1 serves as the `visited` flag, so a cell that no search reaches keeps -1 without an extra pass.

Because the queue holds layers in order, the first search to reach a cell reaches it by a shortest route that avoids walls. The invariant is that a cell with a distance value holds the length of a shortest wall-free route to some zero, and every queued cell has a final value. Wall cells and cells that no route reaches keep -1, which matches the contract.

**Complexity.**
- **Time** is O(rows * cols), because each cell is queued at most once and tests four neighbors.
- **Space** is O(rows * cols), because the answer table and the queue scale with the table.

```java run
import java.util.ArrayDeque;
import java.util.Arrays;
import java.util.Random;

public final class NearestZeroWalls {
    /**
     * Returns for each cell the length of a shortest side-neighbor route to a 0 cell that never enters a cell marked 2, or -1.
     * Time: O(rows * cols), because each cell is queued at most once.
     * Space: O(rows * cols), because of the result table and the queue.
     * Invariant: a cell with a value other than -1 holds its final distance, and every queued cell has such a value.
     */
    static int[][] nearestZero(int[][] grid) {
        int rows = grid.length, cols = grid[0].length;
        // The result doubles as the visited record, so -1 means unreached.
        int[][] dist = new int[rows][cols];
        for (int[] row : dist) Arrays.fill(row, -1);
        ArrayDeque<Integer> queue = new ArrayDeque<>();
        // Seed every zero cell at distance 0 before the first removal.
        for (int id = 0; id < rows * cols; id++) {
            if (grid[id / cols][id % cols] == 0) { dist[id / cols][id % cols] = 0; queue.add(id); }
        }
        int[] dr = {1, -1, 0, 0}, dc = {0, 0, 1, -1};
        // Each cell leaves the queue once, so the loop body runs at most rows * cols times.
        while (!queue.isEmpty()) {
            int cur = queue.poll();
            int r = cur / cols, c = cur % cols;
            for (int k = 0; k < 4; k++) {
                int nr = r + dr[k], nc = c + dc[k];
                // Bounds check first.
                if (nr < 0 || nr >= rows || nc < 0 || nc >= cols) continue;
                // Only an unreached cell with value 1 qualifies; walls and zeros are never entered.
                if (grid[nr][nc] != 1 || dist[nr][nc] != -1) continue;
                // The distance is final at discovery because the queue is in layer order.
                dist[nr][nc] = dist[r][c] + 1;
                queue.add(nr * cols + nc);
            }
        }
        return dist;
    }

    /** Oracle: relaxes every cell against its neighbors until no value changes. */
    static int[][] oracle(int[][] grid) {
        int rows = grid.length, cols = grid[0].length, inf = Integer.MAX_VALUE / 2;
        int[][] d = new int[rows][cols];
        for (int r = 0; r < rows; r++) for (int c = 0; c < cols; c++) d[r][c] = grid[r][c] == 0 ? 0 : inf;
        int[] dr = {1, -1, 0, 0}, dc = {0, 0, 1, -1};
        for (boolean changed = true; changed; ) {
            changed = false;
            for (int r = 0; r < rows; r++) for (int c = 0; c < cols; c++) {
                if (grid[r][c] != 1) continue;
                for (int k = 0; k < 4; k++) {
                    int nr = r + dr[k], nc = c + dc[k];
                    if (nr < 0 || nr >= rows || nc < 0 || nc >= cols || grid[nr][nc] == 2) continue;
                    if (d[nr][nc] + 1 < d[r][c]) { d[r][c] = d[nr][nc] + 1; changed = true; }
                }
            }
        }
        for (int r = 0; r < rows; r++) for (int c = 0; c < cols; c++) if (d[r][c] >= inf || grid[r][c] == 2) d[r][c] = -1;
        return d;
    }

    public static void main(String[] args) {
        // Example 1: a wall in the middle and one source in the corner.
        int[][] a = nearestZero(new int[][] {{1, 1, 1}, {1, 2, 1}, {1, 1, 0}});
        if (!Arrays.deepEquals(a, new int[][] {{4, 3, 2}, {3, -1, 1}, {2, 1, 0}})) throw new AssertionError("example 1");
        // Example 2: walls cut the only source off from every other cell.
        int[][] b = nearestZero(new int[][] {{1, 2, 0}, {2, 1, 2}, {1, 1, 2}});
        if (!Arrays.deepEquals(b, new int[][] {{-1, -1, 0}, {-1, -1, -1}, {-1, -1, -1}})) throw new AssertionError("example 2");
        // A table with no zero has no reachable source, so every cell is -1.
        if (!Arrays.deepEquals(nearestZero(new int[][] {{1, 1}}), new int[][] {{-1, -1}})) throw new AssertionError("no source");
        // A table that is all zeros gives all zeros.
        if (!Arrays.deepEquals(nearestZero(new int[][] {{0, 0}}), new int[][] {{0, 0}})) throw new AssertionError("all zero");
        // A wall forces a detour that is longer than the straight distance.
        if (!Arrays.deepEquals(nearestZero(new int[][] {{0, 2, 1}, {1, 1, 1}}), new int[][] {{0, -1, 4}, {1, 2, 3}})) throw new AssertionError("detour");
        // Random tables against the relaxation oracle.
        Random rnd = new Random(2202);
        for (int t = 0; t < 4000; t++) {
            int rows = 1 + rnd.nextInt(5), cols = 1 + rnd.nextInt(5);
            int[][] g = new int[rows][cols];
            for (int[] row : g) for (int j = 0; j < cols; j++) row[j] = rnd.nextInt(3);
            if (!Arrays.deepEquals(nearestZero(g), oracle(g))) throw new AssertionError("random " + t + " " + Arrays.deepToString(g));
        }
    }
}
```

#### Solution: [Boundary] Smallest Shortest Path In A Binary Matrix (LeetCode 1091)
<!-- id: bv9-smallest-shortest-path -->

**Approach.**
The method searches from the target and not from the start. The start set holds the bottom right cell at distance 0, and the search fills `toEnd`, the shortest eight-direction distance from each open cell to the target. The state key is the cell id, and a blocked cell never receives a distance, so a blocked endpoint gives an unreachable start or an immediate empty answer.

After the search, the method walks forward from the top left cell. At each cell it tries the eight steps in the fixed order and takes the first neighbor whose `toEnd` equals the current value minus one. Such a neighbor lies on some shortest path, so taking the earliest step in the order yields the lexicographically smallest shortest path. The invariant is that the walk stands on a cell with `toEnd = d` after `length - 1 - d` steps, and every step lowers the value by exactly one. The walk stops at the target, whose value is 0.

**Complexity.**
- **Time** is O(rows * cols), because the search queues each open cell once with eight tests, and the walk visits one cell per path length.
- **Space** is O(rows * cols), because `toEnd` and the queue scale with the table, and the path is no longer than the cell count.

```java run
import java.util.ArrayDeque;
import java.util.Arrays;
import java.util.Random;

public final class SmallestShortestPath {
    /** The fixed direction order: row-major order of the eight steps. */
    static final int[][] ORDER = {{-1, -1}, {-1, 0}, {-1, 1}, {0, -1}, {0, 1}, {1, -1}, {1, 0}, {1, 1}};

    /**
     * Returns the cells {row, col} of the lexicographically smallest shortest path, or an empty array.
     * Time: O(rows * cols), because one search and one walk each touch a cell at most once.
     * Space: O(rows * cols), because of the distance table and the queue.
     * Invariant: the walk stands on a cell whose distance to the target drops by one at every step.
     */
    static int[][] smallestPath(int[][] grid) {
        int rows = grid.length, cols = grid[0].length;
        // A blocked endpoint leaves no path at all.
        if (grid[0][0] != 0 || grid[rows - 1][cols - 1] != 0) return new int[0][];
        // toEnd doubles as the visited record, so -1 means unreached.
        int[] toEnd = new int[rows * cols];
        Arrays.fill(toEnd, -1);
        ArrayDeque<Integer> queue = new ArrayDeque<>();
        // The start set is the target alone, at distance 0.
        toEnd[rows * cols - 1] = 0;
        queue.add(rows * cols - 1);
        // Each open cell leaves the queue once, with eight candidate steps.
        while (!queue.isEmpty()) {
            int cur = queue.poll();
            for (int[] d : ORDER) {
                int nr = cur / cols + d[0], nc = cur % cols + d[1];
                // Bounds check first.
                if (nr < 0 || nr >= rows || nc < 0 || nc >= cols) continue;
                // Only an open, unreached cell joins the layer.
                if (grid[nr][nc] != 0 || toEnd[nr * cols + nc] != -1) continue;
                toEnd[nr * cols + nc] = toEnd[cur] + 1;
                queue.add(nr * cols + nc);
            }
        }
        // If the search never reached the top left cell, no path exists.
        if (toEnd[0] == -1) return new int[0][];
        // The path holds toEnd[0] + 1 cells, from the start to the target.
        int[][] path = new int[toEnd[0] + 1][];
        int cur = 0;
        for (int i = 0; i < path.length; i++) {
            path[i] = new int[] {cur / cols, cur % cols};
            // The last cell is the target, so there is no next step.
            if (i == path.length - 1) break;
            // The first step in the fixed order that lowers the distance by one is the smallest choice.
            for (int[] d : ORDER) {
                int nr = cur / cols + d[0], nc = cur % cols + d[1];
                if (nr < 0 || nr >= rows || nc < 0 || nc >= cols) continue;
                if (toEnd[nr * cols + nc] == toEnd[cur] - 1) { cur = nr * cols + nc; break; }
            }
        }
        return path;
    }

    /** Oracle: finds the length by a search from the start, then tries paths of exactly that length in the fixed order. */
    static int[][] oracle(int[][] grid) {
        int rows = grid.length, cols = grid[0].length;
        if (grid[0][0] != 0 || grid[rows - 1][cols - 1] != 0) return new int[0][];
        int[][] dist = new int[rows][cols];
        for (int[] row : dist) Arrays.fill(row, -1);
        ArrayDeque<int[]> q = new ArrayDeque<>();
        dist[0][0] = 0;
        q.add(new int[] {0, 0});
        while (!q.isEmpty()) {
            int[] p = q.poll();
            for (int[] d : ORDER) {
                int nr = p[0] + d[0], nc = p[1] + d[1];
                if (nr < 0 || nr >= rows || nc < 0 || nc >= cols || grid[nr][nc] != 0 || dist[nr][nc] != -1) continue;
                dist[nr][nc] = dist[p[0]][p[1]] + 1;
                q.add(new int[] {nr, nc});
            }
        }
        if (dist[rows - 1][cols - 1] == -1) return new int[0][];
        int[][] path = new int[dist[rows - 1][cols - 1] + 1][];
        boolean[][] used = new boolean[rows][cols];
        if (!dfs(grid, 0, 0, 0, path, used)) throw new AssertionError("oracle found no path");
        return path;
    }

    /** Depth-first search that fills path in direction order and stops at the first complete path. */
    static boolean dfs(int[][] grid, int r, int c, int index, int[][] path, boolean[][] used) {
        path[index] = new int[] {r, c};
        if (index == path.length - 1) return r == grid.length - 1 && c == grid[0].length - 1;
        used[r][c] = true;
        for (int[] d : ORDER) {
            int nr = r + d[0], nc = c + d[1];
            if (nr < 0 || nr >= grid.length || nc < 0 || nc >= grid[0].length || grid[nr][nc] != 0 || used[nr][nc]) continue;
            if (dfs(grid, nr, nc, index + 1, path, used)) { used[r][c] = false; return true; }
        }
        used[r][c] = false;
        return false;
    }

    public static void main(String[] args) {
        // Example 1: a six-cell path where the first choice is to step right.
        int[][] a = smallestPath(new int[][] {{0, 0, 1, 0}, {1, 1, 0, 0}, {0, 0, 1, 1}, {1, 0, 0, 0}});
        if (!Arrays.deepEquals(a, new int[][] {{0, 0}, {0, 1}, {1, 2}, {2, 1}, {3, 2}, {3, 3}})) throw new AssertionError("example 1");
        // Example 2: several shortest paths tie, and the fixed order picks the one that goes right before it goes down.
        int[][] b = smallestPath(new int[][] {{0, 0, 0}, {0, 1, 0}, {0, 0, 0}});
        if (!Arrays.deepEquals(b, new int[][] {{0, 0}, {0, 1}, {1, 2}, {2, 2}})) throw new AssertionError("example 2");
        // A single open cell is both the start and the target.
        if (!Arrays.deepEquals(smallestPath(new int[][] {{0}}), new int[][] {{0, 0}})) throw new AssertionError("single open");
        // A single blocked cell has no path.
        if (smallestPath(new int[][] {{1}}).length != 0) throw new AssertionError("single blocked");
        // A blocked target and a blocked start each give an empty result.
        if (smallestPath(new int[][] {{0, 0}, {0, 1}}).length != 0) throw new AssertionError("blocked target");
        if (smallestPath(new int[][] {{1, 0}, {0, 0}}).length != 0) throw new AssertionError("blocked start");
        // Walls that cut the start off from the target give an empty result.
        if (smallestPath(new int[][] {{0, 1, 0}, {1, 1, 0}, {0, 0, 0}}).length != 0) throw new AssertionError("cut off");
        // Random tables against the exhaustive ordered search.
        Random rnd = new Random(2203);
        for (int t = 0; t < 4000; t++) {
            int rows = 1 + rnd.nextInt(5), cols = 1 + rnd.nextInt(5);
            int[][] g = new int[rows][cols];
            for (int[] row : g) for (int j = 0; j < cols; j++) row[j] = rnd.nextInt(10) < 3 ? 1 : 0;
            if (!Arrays.deepEquals(smallestPath(g), oracle(g))) throw new AssertionError("random " + t + " " + Arrays.deepToString(g));
        }
    }
}
```

#### Solution: [Recognize] One Shortest Word Sequence (LeetCode 127)
<!-- id: bv9-word-sequence -->

**Approach.**
The state key is the word itself, mapped to an id through a `HashMap`. The move rule generates keys instead of reading them from a table: for each position it replaces the letter with each of the 26 lowercase letters and looks the result up in the map. A word that the map does not hold is not a valid next word. The start set is the begin word alone, and the method adds it to the map when the list lacks it.

The search is plain BFS with a `parent` array. When a word first enters the queue, the method stores the word that discovered it. Because layers are in order, the first discovery of the end word comes from a shortest sequence. The method then follows `parent` from the end word back to the begin word and reverses the result. The invariant is that every queued word has a recorded parent whose layer is one lower. A meet-in-the-middle search would give the same answer with a smaller frontier, but plain BFS with parents is enough here. An end word that the list lacks returns an empty list before any search.

**Complexity.**
- **Time** is O(n * L * 26 * L), because each of the `n` words generates `26 * L` candidates and each candidate costs O(L) to hash.
- **Space** is O(n * L), because the map, the `parent` array and the queue hold at most `n + 1` words of length `L`.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Random;

public final class WordSequence {
    /**
     * Returns one shortest sequence from begin to end, or an empty list.
     * Time: O(n * L * 26 * L), because each word tries 26 letters at each of L positions and hashes a word of length L.
     * Space: O(n * L), because of the id map, the parent array and the queue.
     * Invariant: every queued word has a parent that sits exactly one layer closer to the begin word.
     */
    static List<String> shortestSequence(String begin, String end, List<String> words) {
        // The end word must be in the list; otherwise no sequence exists.
        if (!words.contains(end)) return new ArrayList<>();
        // Assign one id to every distinct word, including the begin word.
        HashMap<String, Integer> idOf = new HashMap<>();
        List<String> byId = new ArrayList<>();
        for (String w : words) if (!idOf.containsKey(w)) { idOf.put(w, byId.size()); byId.add(w); }
        if (!idOf.containsKey(begin)) { idOf.put(begin, byId.size()); byId.add(begin); }
        // parent[id] is -1 for an unreached word and the discovering word otherwise.
        int[] parent = new int[byId.size()];
        Arrays.fill(parent, -1);
        int startId = idOf.get(begin), endId = idOf.get(end);
        ArrayDeque<Integer> queue = new ArrayDeque<>();
        // The begin word is its own parent, which also marks it as reached.
        parent[startId] = startId;
        queue.add(startId);
        // Each word leaves the queue once.
        while (!queue.isEmpty() && parent[endId] == -1) {
            int cur = queue.poll();
            char[] letters = byId.get(cur).toCharArray();
            // Generate every word that differs from cur in exactly one position.
            for (int pos = 0; pos < letters.length; pos++) {
                char original = letters[pos];
                for (char ch = 'a'; ch <= 'z'; ch++) {
                    // A candidate equal to cur is not a move.
                    if (ch == original) continue;
                    letters[pos] = ch;
                    Integer next = idOf.get(new String(letters));
                    // A word outside the list, or one reached earlier, is skipped.
                    if (next == null || parent[next] != -1) continue;
                    // Mark when found, then queue.
                    parent[next] = cur;
                    queue.add(next);
                }
                // Restore the letter before the next position.
                letters[pos] = original;
            }
        }
        // If the end word was never reached, no sequence exists.
        if (parent[endId] == -1) return new ArrayList<>();
        // Follow the parents from the end word back to the begin word.
        List<String> result = new ArrayList<>();
        for (int id = endId; ; id = parent[id]) {
            result.add(byId.get(id));
            if (id == startId) break;
        }
        // The walk ran backward, so reverse it.
        Collections.reverse(result);
        return result;
    }

    /** True when the two words have the same length and differ in exactly one position. */
    static boolean oneApart(String a, String b) {
        if (a.length() != b.length()) return false;
        int diff = 0;
        for (int i = 0; i < a.length(); i++) if (a.charAt(i) != b.charAt(i)) diff++;
        return diff == 1;
    }

    /** Oracle: computes all-pairs distances with Floyd-Warshall, then checks the returned sequence against them. */
    static void check(String begin, String end, List<String> words, List<String> got) {
        List<String> nodes = new ArrayList<>(new HashSet<>(words));
        if (!nodes.contains(begin)) nodes.add(begin);
        int n = nodes.size(), inf = 1000;
        int[][] d = new int[n][n];
        for (int i = 0; i < n; i++) for (int j = 0; j < n; j++) d[i][j] = i == j ? 0 : oneApart(nodes.get(i), nodes.get(j)) ? 1 : inf;
        for (int k = 0; k < n; k++) for (int i = 0; i < n; i++) for (int j = 0; j < n; j++) d[i][j] = Math.min(d[i][j], d[i][k] + d[k][j]);
        boolean endInList = words.contains(end);
        int want = endInList ? d[nodes.indexOf(begin)][nodes.indexOf(end)] : inf;
        if (want >= inf) {
            if (!got.isEmpty()) throw new AssertionError("expected empty");
            return;
        }
        if (got.size() != want + 1) throw new AssertionError("wrong length " + got);
        if (!got.get(0).equals(begin) || !got.get(got.size() - 1).equals(end)) throw new AssertionError("wrong ends " + got);
        for (int i = 1; i < got.size(); i++) {
            if (!oneApart(got.get(i - 1), got.get(i))) throw new AssertionError("bad step " + got);
            if (!words.contains(got.get(i))) throw new AssertionError("word outside list " + got);
        }
    }

    public static void main(String[] args) {
        // Example 1: the only shortest sequence has five words.
        List<String> w1 = Arrays.asList("cord", "card", "ward", "warm", "wore");
        List<String> r1 = shortestSequence("cold", "warm", w1);
        if (!r1.equals(Arrays.asList("cold", "cord", "card", "ward", "warm"))) throw new AssertionError("example 1");
        // Example 2: the end word is in the list but no chain reaches it.
        if (!shortestSequence("hat", "cog", Arrays.asList("hot", "dot", "cog")).isEmpty()) throw new AssertionError("example 2");
        // An end word outside the list gives an empty list.
        if (!shortestSequence("hit", "hot", Arrays.asList("hat", "hug")).isEmpty()) throw new AssertionError("end missing");
        // A begin word that is also in the list does not change the answer.
        if (shortestSequence("hit", "hot", Arrays.asList("hit", "hot")).size() != 2) throw new AssertionError("begin in list");
        // A sequence of two words has one step.
        if (!shortestSequence("a", "b", Arrays.asList("b")).equals(Arrays.asList("a", "b"))) throw new AssertionError("one letter");
        // Random lists over a three-letter alphabet against the Floyd-Warshall oracle.
        Random rnd = new Random(2204);
        for (int t = 0; t < 4000; t++) {
            int len = 1 + rnd.nextInt(3);
            String begin = randomWord(rnd, len), end = randomWord(rnd, len);
            while (end.equals(begin)) end = randomWord(rnd, len);
            List<String> words = new ArrayList<>();
            for (int i = rnd.nextInt(9); i > 0; i--) words.add(randomWord(rnd, len));
            check(begin, end, words, shortestSequence(begin, end, words));
        }
    }

    /** Builds a random word of the given length over the letters a to c. */
    static String randomWord(Random rnd, int len) {
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < len; i++) sb.append((char) ('a' + rnd.nextInt(3)));
        return sb.toString();
    }
}
```
