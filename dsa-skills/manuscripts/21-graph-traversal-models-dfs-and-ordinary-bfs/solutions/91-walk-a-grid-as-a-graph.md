<!-- solutions-for: 91-walk-a-grid-as-a-graph -->
### Solutions For Walking A Grid

#### Solution: [Build] Protected Fill With A Count (LeetCode 733)
<!-- id: gt-fill-protected -->

**Approach.**
The neighbor rule changes, and the traversal stays the same. A candidate joins the patch when it lies inside the table, is new to the search and holds a color other than `protect`. Because `protect != color`, a recolored pixel still passes the rule, so the `visited` array is the only thing that stops the search from returning to it. The method marks a pixel when it enters the frontier.

The invariant is that every queued pixel is in bounds, marked and not protected. The count grows only when a dequeued pixel holds a color different from `color`, because the problem counts changed pixels and not patch pixels. A protected source returns 0 before any queuing.

**Complexity.**
- **Time** is O(rows * cols), because each pixel is queued at most once and tests four candidates.
- **Space** is O(rows * cols), because `visited` and the frontier scale with the table.

```java run
import java.util.ArrayDeque;
import java.util.Arrays;
import java.util.Random;

public final class ProtectedFill {
    /**
     * Recolors the patch reachable from (sr, sc) through pixels that are not protect, and returns how many pixels changed.
     * Time: O(rows * cols), because each pixel is queued at most once.
     * Space: O(rows * cols), because of the visited array and the frontier.
     * Invariant: every queued pixel is in bounds, visited and not protected.
     */
    static int fillAvoiding(int[][] image, int sr, int sc, int color, int protect) {
        int rows = image.length, cols = image[0].length;
        // A protected source gives an empty patch, so nothing changes.
        if (image[sr][sc] == protect) return 0;
        // Recolored pixels remain eligible, so only this array prevents revisits.
        boolean[] visited = new boolean[rows * cols];
        ArrayDeque<Integer> frontier = new ArrayDeque<>();
        // Mark the source before it enters the frontier.
        visited[sr * cols + sc] = true;
        frontier.add(sr * cols + sc);
        int changed = 0;
        // Each pixel leaves the frontier once, so the loop body runs at most rows * cols times.
        while (!frontier.isEmpty()) {
            int cur = frontier.poll();
            int r = cur / cols, c = cur % cols;
            // Count a pixel only when its value really changes.
            if (image[r][c] != color) { image[r][c] = color; changed++; }
            // Candidate neighbors in four side directions.
            int[] dr = {1, -1, 0, 0}, dc = {0, 0, 1, -1};
            for (int k = 0; k < 4; k++) {
                int nr = r + dr[k], nc = c + dc[k];
                // Bounds check first.
                if (nr < 0 || nr >= rows || nc < 0 || nc >= cols) continue;
                // The eligibility rule of this contract: any color except protect.
                if (image[nr][nc] == protect || visited[nr * cols + nc]) continue;
                // Mark when found, then queue.
                visited[nr * cols + nc] = true;
                frontier.add(nr * cols + nc);
            }
        }
        return changed;
    }

    /** Oracle: grows the patch by repeated sweeps until no pixel joins. */
    static int oracle(int[][] image, int sr, int sc, int color, int protect) {
        int rows = image.length, cols = image[0].length;
        if (image[sr][sc] == protect) return 0;
        boolean[][] in = new boolean[rows][cols];
        in[sr][sc] = true;
        for (boolean grew = true; grew; ) {
            grew = false;
            for (int r = 0; r < rows; r++) for (int c = 0; c < cols; c++) {
                if (in[r][c] || image[r][c] == protect) continue;
                if ((r > 0 && in[r - 1][c]) || (r + 1 < rows && in[r + 1][c]) || (c > 0 && in[r][c - 1]) || (c + 1 < cols && in[r][c + 1])) { in[r][c] = true; grew = true; }
            }
        }
        int n = 0;
        for (int r = 0; r < rows; r++) for (int c = 0; c < cols; c++) if (in[r][c]) { if (image[r][c] != color) n++; image[r][c] = color; }
        return n;
    }

    public static void main(String[] args) {
        // Example 1: six pixels change, and the pixel already holding 7 adds nothing to the count.
        int[][] a = {{1, 7, 5}, {2, 5, 1}, {1, 2, 2}};
        if (fillAvoiding(a, 0, 0, 7, 5) != 6) throw new AssertionError("example 1 count");
        if (!Arrays.deepEquals(a, new int[][] {{7, 7, 5}, {7, 5, 7}, {7, 7, 7}})) throw new AssertionError("example 1 image");
        // Example 2: a protected source changes nothing.
        int[][] b = {{4, 5}, {5, 4}};
        if (fillAvoiding(b, 0, 1, 6, 5) != 0 || !Arrays.deepEquals(b, new int[][] {{4, 5}, {5, 4}})) throw new AssertionError("example 2");
        // The diagonal pixel is not a neighbor, so only the source changes.
        int[][] c = {{4, 5}, {5, 4}};
        if (fillAvoiding(c, 0, 0, 6, 5) != 1 || c[1][1] != 4) throw new AssertionError("diagonal");
        // Random tests against the sweep oracle; protect and color always differ.
        Random rnd = new Random(21);
        for (int t = 0; t < 3000; t++) {
            int rows = 1 + rnd.nextInt(6), cols = 1 + rnd.nextInt(6);
            int[][] img = new int[rows][cols];
            for (int[] row : img) for (int j = 0; j < cols; j++) row[j] = rnd.nextInt(4);
            int protect = rnd.nextInt(4), color = (protect + 1 + rnd.nextInt(3)) % 4;
            int sr = rnd.nextInt(rows), sc = rnd.nextInt(cols);
            int[][] x = new int[rows][], y = new int[rows][];
            for (int r = 0; r < rows; r++) { x[r] = img[r].clone(); y[r] = img[r].clone(); }
            int got = fillAvoiding(x, sr, sc, color, protect), want = oracle(y, sr, sc, color, protect);
            if (got != want || !Arrays.deepEquals(x, y)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Vary] Islands With Diagonal Contact (LeetCode 200)
<!-- id: gt-island-diagonal -->

**Approach.**
Only the direction table changes. The table lists eight steps, the four side steps and the four corner steps, so a cell touches up to eight others. The start loop scans cells in row-major order, and each unvisited land cell begins one search and adds 1 to `islands`. The search shares one `visited` array with all later searches.

The invariant is that after the scan passes a cell, the cell is water or visited. The table is a parameter, so the same method also counts with four steps, and the test in `main` uses that to show that the answers differ on a map with diagonal contact.

**Complexity.**
- **Time** is O(rows * cols * s), where `s` is the number of steps in the table, which is 8 here, so O(rows * cols).
- **Space** is O(rows * cols), because `visited` has one flag per cell and the frontier holds ids.

```java run
import java.util.ArrayDeque;
import java.util.HashSet;
import java.util.Random;

public final class DiagonalIslands {
    static final int[][] FOUR = {{1, 0}, {-1, 0}, {0, 1}, {0, -1}};
    static final int[][] EIGHT = {{1, 0}, {-1, 0}, {0, 1}, {0, -1}, {1, 1}, {1, -1}, {-1, 1}, {-1, -1}};

    /**
     * Counts islands of land cells whose neighbors are given by dirs.
     * Time: O(rows * cols * dirs.length), because each cell is queued once and tests every step.
     * Space: O(rows * cols), because of the visited array.
     * Invariant: after the scan passes a cell, the cell is water or visited.
     */
    static int countIslands(int[][] grid, int[][] dirs) {
        int rows = grid.length, cols = grid[0].length, islands = 0;
        // One array for all searches, so no region is walked twice.
        boolean[] visited = new boolean[rows * cols];
        // The start loop: one pass over every cell id.
        for (int start = 0; start < rows * cols; start++) {
            // Skip water and land that an earlier search reached.
            if (grid[start / cols][start % cols] == 0 || visited[start]) continue;
            // A new island begins here.
            islands++;
            ArrayDeque<Integer> frontier = new ArrayDeque<>();
            visited[start] = true;
            frontier.add(start);
            while (!frontier.isEmpty()) {
                int cur = frontier.poll();
                // Every step of the table is a candidate, four or eight of them.
                for (int[] d : dirs) {
                    int nr = cur / cols + d[0], nc = cur % cols + d[1];
                    // Bounds check first.
                    if (nr < 0 || nr >= rows || nc < 0 || nc >= cols) continue;
                    // Land that is new to the search joins the island.
                    if (grid[nr][nc] == 1 && !visited[nr * cols + nc]) {
                        visited[nr * cols + nc] = true;
                        frontier.add(nr * cols + nc);
                    }
                }
            }
        }
        return islands;
    }

    /** Oracle: propagates the smallest id over eight-direction contact until stable, then counts labels. */
    static int oracle(int[][] grid) {
        int rows = grid.length, cols = grid[0].length;
        int[] label = new int[rows * cols];
        for (int i = 0; i < label.length; i++) label[i] = i;
        for (boolean changed = true; changed; ) {
            changed = false;
            for (int r = 0; r < rows; r++) for (int c = 0; c < cols; c++) {
                if (grid[r][c] == 0) continue;
                for (int dr = -1; dr <= 1; dr++) for (int dc = -1; dc <= 1; dc++) {
                    int nr = r + dr, nc = c + dc;
                    if ((dr == 0 && dc == 0) || nr < 0 || nr >= rows || nc < 0 || nc >= cols || grid[nr][nc] == 0) continue;
                    int m = Math.min(label[r * cols + c], label[nr * cols + nc]);
                    if (label[r * cols + c] != m) { label[r * cols + c] = m; changed = true; }
                    if (label[nr * cols + nc] != m) { label[nr * cols + nc] = m; changed = true; }
                }
            }
        }
        HashSet<Integer> roots = new HashSet<>();
        for (int r = 0; r < rows; r++) for (int c = 0; c < cols; c++) if (grid[r][c] == 1) roots.add(label[r * cols + c]);
        return roots.size();
    }

    public static void main(String[] args) {
        // Example 1: two islands with diagonal contact, and four islands without it.
        int[][] g1 = {{1, 0, 0, 1}, {0, 1, 0, 0}, {0, 0, 1, 1}};
        if (countIslands(g1, EIGHT) != 2) throw new AssertionError("example 1");
        if (countIslands(g1, FOUR) != 4) throw new AssertionError("four-direction answer differs");
        // Example 2: the three cells in the top left join through a corner.
        if (countIslands(new int[][] {{1, 1, 0}, {0, 0, 1}, {1, 0, 0}}, EIGHT) != 2) throw new AssertionError("example 2");
        // No land gives 0.
        if (countIslands(new int[][] {{0, 0}}, EIGHT) != 0) throw new AssertionError("no land");
        // Random tests against the label oracle.
        Random rnd = new Random(8);
        for (int t = 0; t < 3000; t++) {
            int rows = 1 + rnd.nextInt(7), cols = 1 + rnd.nextInt(7);
            int[][] m = new int[rows][cols];
            for (int[] row : m) for (int j = 0; j < cols; j++) row[j] = rnd.nextInt(100) < 40 ? 1 : 0;
            if (countIslands(m, EIGHT) != oracle(m)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Boundary] Smallest Island And Its First Cell (LeetCode 695)
<!-- id: gt-smallest-island -->

**Approach.**
The start loop scans cells in row-major order, so the first cell of an island that the scan meets is that island's first cell. Each such cell begins a search, and the search returns the island's area. The method keeps `bestArea` and the start cell of the best island.

A new island replaces the best only when its area is strictly smaller. A tie therefore leaves the earlier island in place, and the earlier island has the earlier first cell. The invariant is that `bestArea` is the smallest area among islands started so far, with the earliest first cell among equals. The method uses a `visited` array and leaves `grid` unchanged.

**Complexity.**
- **Time** is O(rows * cols), because each cell is scanned once and queued at most once.
- **Space** is O(rows * cols), because of the `visited` array and the frontier.

```java run
import java.util.ArrayDeque;
import java.util.Arrays;
import java.util.Random;

public final class SmallestIsland {
    /**
     * Returns {area, row, col} of the smallest island, ties to the earliest first cell, or {0, -1, -1}.
     * Time: O(rows * cols), because each cell is queued at most once.
     * Space: O(rows * cols), because of the visited array and the frontier.
     * Invariant: bestArea is the smallest area among islands started so far.
     */
    static int[] smallest(int[][] grid) {
        int rows = grid.length, cols = grid[0].length;
        boolean[] visited = new boolean[rows * cols];
        // Zero means that no island has been found yet.
        int bestArea = 0, bestRow = -1, bestCol = -1;
        for (int start = 0; start < rows * cols; start++) {
            // Skip water and cells of islands that were measured already.
            if (grid[start / cols][start % cols] == 0 || visited[start]) continue;
            // The scan order guarantees that this cell is the first cell of its island.
            ArrayDeque<Integer> frontier = new ArrayDeque<>();
            visited[start] = true;
            frontier.add(start);
            int area = 0;
            while (!frontier.isEmpty()) {
                int cur = frontier.poll();
                area++;
                int r = cur / cols, c = cur % cols;
                int[][] around = {{r + 1, c}, {r - 1, c}, {r, c + 1}, {r, c - 1}};
                for (int[] a : around) {
                    if (a[0] < 0 || a[0] >= rows || a[1] < 0 || a[1] >= cols) continue;
                    if (grid[a[0]][a[1]] == 1 && !visited[a[0] * cols + a[1]]) {
                        visited[a[0] * cols + a[1]] = true;
                        frontier.add(a[0] * cols + a[1]);
                    }
                }
            }
            // Strictly smaller replaces; an equal area keeps the earlier first cell.
            if (bestArea == 0 || area < bestArea) { bestArea = area; bestRow = start / cols; bestCol = start % cols; }
        }
        return new int[] {bestArea, bestRow, bestCol};
    }

    /** Oracle: labels cells by repeated sweeps, then picks the smallest (area, first id) pair. */
    static int[] oracle(int[][] grid) {
        int rows = grid.length, cols = grid[0].length;
        int[] label = new int[rows * cols];
        for (int i = 0; i < label.length; i++) label[i] = i;
        for (boolean changed = true; changed; ) {
            changed = false;
            for (int r = 0; r < rows; r++) for (int c = 0; c < cols; c++) {
                if (grid[r][c] == 0) continue;
                int[][] nbs = {{r + 1, c}, {r, c + 1}};
                for (int[] n : nbs) {
                    if (n[0] >= rows || n[1] >= cols || grid[n[0]][n[1]] == 0) continue;
                    int m = Math.min(label[r * cols + c], label[n[0] * cols + n[1]]);
                    if (label[r * cols + c] != m || label[n[0] * cols + n[1]] != m) { label[r * cols + c] = m; label[n[0] * cols + n[1]] = m; changed = true; }
                }
            }
        }
        int[] size = new int[rows * cols];
        for (int r = 0; r < rows; r++) for (int c = 0; c < cols; c++) if (grid[r][c] == 1) size[label[r * cols + c]]++;
        int bestId = -1;
        // The label of an island is its smallest id, which is its first cell in row-major order.
        for (int id = 0; id < size.length; id++) if (size[id] > 0 && (bestId < 0 || size[id] < size[bestId])) bestId = id;
        return bestId < 0 ? new int[] {0, -1, -1} : new int[] {size[bestId], bestId / cols, bestId % cols};
    }

    public static void main(String[] args) {
        // Example 1: area 1, and the first one-cell island in row-major order is at row 1, column 3.
        int[][] g = {{1, 1, 0, 0}, {1, 0, 0, 1}, {0, 0, 0, 0}, {1, 0, 1, 1}};
        if (!Arrays.equals(smallest(g), new int[] {1, 1, 3})) throw new AssertionError("example 1");
        // Example 2: both islands have area 3, so the left one wins.
        if (!Arrays.equals(smallest(new int[][] {{1, 0, 1}, {1, 0, 1}, {1, 0, 1}}), new int[] {3, 0, 0})) throw new AssertionError("example 2");
        // No land gives the sentinel result.
        if (!Arrays.equals(smallest(new int[][] {{0, 0}, {0, 0}}), new int[] {0, -1, -1})) throw new AssertionError("no land");
        // The grid stays unchanged after the call.
        if (!Arrays.deepEquals(g, new int[][] {{1, 1, 0, 0}, {1, 0, 0, 1}, {0, 0, 0, 0}, {1, 0, 1, 1}})) throw new AssertionError("grid mutated");
        // Random tests against the label oracle.
        Random rnd = new Random(34);
        for (int t = 0; t < 3000; t++) {
            int rows = 1 + rnd.nextInt(7), cols = 1 + rnd.nextInt(7);
            int[][] m = new int[rows][cols];
            for (int[] row : m) for (int j = 0; j < cols; j++) row[j] = rnd.nextInt(100) < 45 ? 1 : 0;
            if (!Arrays.equals(smallest(m), oracle(m))) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Recognize] Clone A Graph Built From Land (LeetCode 133)
<!-- id: gt-clone-land -->

**Approach.**
The method builds the original graph with one `Node` for each land cell, adding the neighbors in the order up, left, right, down. It then finds the first land cell in row-major order and copies the component of that node. The copy uses a `HashMap` from original node to copy. The map is the `visited` record, because a node counts as found once it is a key, and its value is the copy that later edges link to.

The walk creates a copy when it first finds a node, queues the original, and links the copy of the current node to the copy of each neighbor. The invariant is that every node in the frontier already has a copy in the map. The map relies on `Node` keeping the default `equals`, which compares identity, so two nodes with equal values stay distinct keys.

**Complexity.**
- **Time** is O(V + E) for the copy, where V counts nodes of the component and E counts its edges, because each node is copied once and each edge is linked once. Building the graph costs O(rows * cols).
- **Space** is O(V) for the map and the frontier, plus the O(V + E) memory of the copy itself.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.HashSet;
import java.util.IdentityHashMap;
import java.util.List;
import java.util.Random;
import java.util.Set;

public final class CloneLand {
    /** A land cell as an object; no equals override, so map keys compare by identity. */
    static final class Node {
        final int val;
        final List<Node> neighbors = new ArrayList<>();
        Node(int val) { this.val = val; }
    }

    /**
     * Builds one node per land cell with neighbors in the order up, left, right, down; water cells give null.
     * Time: O(rows * cols). Space: O(rows * cols).
     */
    static Node[] build(int[][] grid) {
        int rows = grid.length, cols = grid[0].length;
        Node[] nodes = new Node[rows * cols];
        // Create nodes first, so a neighbor can be linked before its own row is processed.
        for (int id = 0; id < rows * cols; id++) if (grid[id / cols][id % cols] == 1) nodes[id] = new Node(id);
        // Offsets in the required order: up, left, right, down.
        int[][] order = {{-1, 0}, {0, -1}, {0, 1}, {1, 0}};
        for (int id = 0; id < rows * cols; id++) {
            if (nodes[id] == null) continue;
            for (int[] o : order) {
                int nr = id / cols + o[0], nc = id % cols + o[1];
                // Bounds check, then water check, then link.
                if (nr >= 0 && nr < rows && nc >= 0 && nc < cols && nodes[nr * cols + nc] != null) nodes[id].neighbors.add(nodes[nr * cols + nc]);
            }
        }
        return nodes;
    }

    /**
     * Copies the component of first by breadth-first search with an identity map from original to copy.
     * Time: O(V + E). Space: O(V) for the map and the frontier.
     * Invariant: every node in the frontier already has a copy in the map.
     */
    static Node copyComponent(Node first) {
        // The map is both the visited record and the store of copies.
        HashMap<Node, Node> copies = new HashMap<>();
        ArrayDeque<Node> frontier = new ArrayDeque<>();
        // Mark the first node by creating its copy before queuing it.
        copies.put(first, new Node(first.val));
        frontier.add(first);
        while (!frontier.isEmpty()) {
            Node cur = frontier.poll();
            // Each edge is read once from its source node.
            for (Node nb : cur.neighbors) {
                // A node that is not a key has never been found, so it gets a copy and joins the frontier.
                if (!copies.containsKey(nb)) { copies.put(nb, new Node(nb.val)); frontier.add(nb); }
                // Link copy to copy, which keeps the neighbor order of the original.
                copies.get(cur).neighbors.add(copies.get(nb));
            }
        }
        return copies.get(first);
    }

    /** Returns a deep copy of the island that holds the first land cell, or null when there is no land. */
    static Node cloneFirstIsland(int[][] grid) {
        Node[] nodes = build(grid);
        // Row-major order is the order of the ids, so the first non-null entry is the first land cell.
        for (Node n : nodes) if (n != null) return copyComponent(n);
        return null;
    }

    /** Lists the component of start as "val:[neighbor vals]" pairs sorted by val, collecting nodes by identity. */
    static String listing(Node start) {
        if (start == null) return "null";
        Set<Node> seen = java.util.Collections.newSetFromMap(new IdentityHashMap<>());
        ArrayDeque<Node> q = new ArrayDeque<>();
        seen.add(start);
        q.add(start);
        List<Node> all = new ArrayList<>();
        while (!q.isEmpty()) {
            Node cur = q.poll();
            all.add(cur);
            for (Node nb : cur.neighbors) if (seen.add(nb)) q.add(nb);
        }
        all.sort((x, y) -> Integer.compare(x.val, y.val));
        StringBuilder sb = new StringBuilder();
        for (Node n : all) {
            List<Integer> vals = new ArrayList<>();
            for (Node nb : n.neighbors) vals.add(nb.val);
            sb.append(n.val).append(':').append(vals).append(' ');
        }
        return sb.toString().trim();
    }

    /** Oracle: labels cells by repeated sweeps, then writes the expected listing straight from the grid. */
    static String oracle(int[][] grid) {
        int rows = grid.length, cols = grid[0].length;
        int first = -1;
        for (int id = 0; id < rows * cols && first < 0; id++) if (grid[id / cols][id % cols] == 1) first = id;
        if (first < 0) return "null";
        boolean[] in = new boolean[rows * cols];
        in[first] = true;
        for (boolean grew = true; grew; ) {
            grew = false;
            for (int id = 0; id < rows * cols; id++) {
                if (in[id] || grid[id / cols][id % cols] == 0) continue;
                int r = id / cols, c = id % cols;
                if ((r > 0 && in[id - cols]) || (r + 1 < rows && in[id + cols]) || (c > 0 && in[id - 1]) || (c + 1 < cols && in[id + 1])) { in[id] = true; grew = true; }
            }
        }
        StringBuilder sb = new StringBuilder();
        for (int id = 0; id < rows * cols; id++) {
            if (!in[id]) continue;
            int r = id / cols, c = id % cols;
            List<Integer> vals = new ArrayList<>();
            if (r > 0 && grid[r - 1][c] == 1) vals.add(id - cols);
            if (c > 0 && grid[r][c - 1] == 1) vals.add(id - 1);
            if (c + 1 < cols && grid[r][c + 1] == 1) vals.add(id + 1);
            if (r + 1 < rows && grid[r + 1][c] == 1) vals.add(id + cols);
            sb.append(id).append(':').append(vals).append(' ');
        }
        return sb.toString().trim();
    }

    public static void main(String[] args) {
        // Example 1: only the island of cell 0 is copied; cells 6 and 8 are other islands.
        if (!listing(cloneFirstIsland(new int[][] {{1, 1, 0}, {0, 1, 0}, {1, 0, 1}})).equals("0:[1] 1:[0, 4] 4:[1]")) throw new AssertionError("example 1");
        // Example 2: a full 2 by 2 block has a cycle of four nodes.
        if (!listing(cloneFirstIsland(new int[][] {{1, 1}, {1, 1}})).equals("0:[1, 2] 1:[0, 3] 2:[0, 3] 3:[1, 2]")) throw new AssertionError("example 2");
        // No land gives null.
        if (cloneFirstIsland(new int[][] {{0}}) != null) throw new AssertionError("no land");
        // Node keeps the default equals, so two nodes with one value are different keys, as the prose says.
        if (new Node(1).equals(new Node(1))) throw new AssertionError("default equals is identity");
        // The copy shares no node with the original graph.
        int[][] g = {{1, 1}, {1, 1}};
        Node[] original = build(g);
        Node copy = copyComponent(original[0]);
        Set<Node> originals = java.util.Collections.newSetFromMap(new IdentityHashMap<>());
        originals.addAll(Arrays.asList(original));
        ArrayDeque<Node> q = new ArrayDeque<>();
        Set<Node> seen = java.util.Collections.newSetFromMap(new IdentityHashMap<>());
        seen.add(copy);
        q.add(copy);
        while (!q.isEmpty()) {
            Node cur = q.poll();
            if (originals.contains(cur)) throw new AssertionError("copy shares a node");
            for (Node nb : cur.neighbors) if (seen.add(nb)) q.add(nb);
        }
        if (seen.size() != 4) throw new AssertionError("copy size");
        // Random tests against the grid oracle.
        Random rnd = new Random(55);
        for (int t = 0; t < 3000; t++) {
            int rows = 1 + rnd.nextInt(6), cols = 1 + rnd.nextInt(6);
            int[][] m = new int[rows][cols];
            for (int[] row : m) for (int j = 0; j < cols; j++) row[j] = rnd.nextInt(100) < 55 ? 1 : 0;
            if (!listing(cloneFirstIsland(m)).equals(oracle(m))) throw new AssertionError("random " + t);
        }
    }
}
```
