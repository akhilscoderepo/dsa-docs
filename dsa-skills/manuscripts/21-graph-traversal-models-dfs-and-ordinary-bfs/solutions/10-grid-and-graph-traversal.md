<!-- solutions-for: 10-grid-and-graph-traversal -->
### Grid And Graph Traversal

#### Solution: [Build] Flood Fill On A Ring (LeetCode 733)
<!-- id: gg-ring-flood-fill -->

**Approach.** Return 0 at once when the new colour equals the starting colour, since nothing may change. Otherwise decode the start into a cell id, push it with its mark, and pop ids from an array stack. The row shift is bounds-checked and the column shift is wrapped with `(nc + cols) % cols`, then a neighbour is pushed only if it is unmarked and has the starting colour. The marks now name exactly the reached cells, so one pass over the mark table recolours them and counts them. The oracle never uses a stack. It repeats a sweep that adds any same-coloured cell standing beside a reached cell, with `Math.floorMod` for the wrap, until a sweep adds nothing. The assertions replay both examples, compare the grid and the count on random rings of one to five columns, and check three claims from the lesson: `-1 % 4` is `-1` in Java, the stack never holds more ids than there are cells because of the mark at push, and a ring of two columns counts the cell on its far side once, although both horizontal moves reach it.

**Complexity.** Every cell is pushed at most once and tried from four directions, so time is O(R * C), and the mark table and stack take O(R * C) space.

```java run
import java.util.Arrays;
import java.util.Random;

public final class RingFloodFillSolution {
    private static final int[] DR = {0, 1, 0, -1};
    private static final int[] DC = {1, 0, -1, 0};
    static int deepest = 0;

    static int solve(int[][] img, int sr, int sc, int color) {
        int rows = img.length, cols = img[0].length, tone = img[sr][sc];
        if (tone == color) return 0;
        boolean[] owned = new boolean[rows * cols];
        int[] stack = new int[rows * cols];
        int top = 0;
        stack[top++] = sr * cols + sc;
        owned[sr * cols + sc] = true;
        while (top > 0) {
            deepest = Math.max(deepest, top);
            int id = stack[--top];
            int r = id / cols, c = id % cols;
            for (int d = 0; d < 4; d++) {
                int nr = r + DR[d];
                int nc = (c + DC[d] + cols) % cols;
                if (nr < 0 || nr >= rows) continue;
                int next = nr * cols + nc;
                if (owned[next] || img[nr][nc] != tone) continue;
                owned[next] = true;
                stack[top++] = next;
            }
        }
        int changed = 0;
        for (int id = 0; id < owned.length; id++) {
            if (owned[id]) { img[id / cols][id % cols] = color; changed++; }
        }
        return changed;
    }

    static int oracle(int[][] img, int sr, int sc, int color) {
        int rows = img.length, cols = img[0].length, tone = img[sr][sc];
        if (tone == color) return 0;
        boolean[][] reach = new boolean[rows][cols];
        reach[sr][sc] = true;
        boolean grew = true;
        while (grew) {
            grew = false;
            for (int r = rows - 1; r >= 0; r--) {
                for (int c = cols - 1; c >= 0; c--) {
                    if (reach[r][c] || img[r][c] != tone) continue;
                    boolean beside = (r > 0 && reach[r - 1][c]) || (r + 1 < rows && reach[r + 1][c])
                            || reach[r][Math.floorMod(c + 1, cols)] || reach[r][Math.floorMod(c - 1, cols)];
                    if (beside) { reach[r][c] = true; grew = true; }
                }
            }
        }
        int n = 0;
        for (int r = 0; r < rows; r++) for (int c = 0; c < cols; c++) if (reach[r][c]) { img[r][c] = color; n++; }
        return n;
    }

    static int[][] copy(int[][] a) {
        int[][] b = new int[a.length][];
        for (int i = 0; i < a.length; i++) b[i] = a[i].clone();
        return b;
    }

    public static void main(String[] args) {
        int[][] a = {{3, 3, 1, 3}, {1, 2, 1, 1}, {3, 1, 1, 3}};
        if (solve(a, 0, 0, 7) != 3 || !Arrays.deepToString(a).equals("[[7, 7, 1, 7], [1, 2, 1, 1], [3, 1, 1, 3]]"))
            throw new AssertionError("example 1");
        int[][] b = {{4, 0, 4}, {0, 0, 0}};
        if (solve(b, 0, 0, 9) != 2 || !Arrays.deepToString(b).equals("[[9, 0, 9], [0, 0, 0]]"))
            throw new AssertionError("example 2");
        int[][] same = {{5, 5}, {5, 1}};
        if (solve(same, 0, 0, 5) != 0 || !Arrays.deepToString(same).equals("[[5, 5], [5, 1]]"))
            throw new AssertionError("same colour changes nothing");
        if ((-1 % 4) != -1 || Math.floorMod(-1, 4) != 3 || (-1 + 4) % 4 != 3)
            throw new AssertionError("remainder keeps the sign of its left side");
        int[][] two = {{1, 1}};
        if (solve(two, 0, 0, 2) != 2) throw new AssertionError("two columns count each cell once");
        Random rnd = new Random(21101);
        for (int t = 0; t < 6000; t++) {
            int rows = 1 + rnd.nextInt(5), cols = 1 + rnd.nextInt(5);
            int[][] g = new int[rows][cols];
            for (int[] row : g) for (int c = 0; c < cols; c++) row[c] = rnd.nextInt(3);
            int sr = rnd.nextInt(rows), sc = rnd.nextInt(cols), color = rnd.nextInt(4);
            int[][] x = copy(g), y = copy(g);
            int nx = solve(x, sr, sc, color), ny = oracle(y, sr, sc, color);
            if (nx != ny || !Arrays.deepEquals(x, y)) throw new AssertionError("differs on " + Arrays.deepToString(g));
        }
        if (deepest > 25) throw new AssertionError("stack deeper than the cell count");
    }
}
```

#### Solution: [Vary] Islands With A Diagonal Flag (LeetCode 200)
<!-- id: gg-island-count-flag -->

**Approach.** The scan walks ids in reading order and starts a search at each land cell that nobody owns. The search is the same stack loop for both contracts, and the flag only chooses how many entries of the shift tables are used, four or eight, where the first four are the straight moves. The shared mark table is allocated once outside the scan. The oracle labels every land cell with its own id and repeatedly lowers each label to the smallest label among the neighbours allowed by the flag, until nothing changes, and then counts the distinct labels. The assertions replay both examples with the flag set both ways on the same grids, check that the input strings are untouched, and verify on random grids that allowing diagonals never produces more islands than the straight contract.

**Complexity.** Each cell is pushed once and tried from at most eight directions, so the time is O(R * C) for both settings, and the marks and the stack use O(R * C) memory.

```java run
import java.util.HashSet;
import java.util.Random;
import java.util.Set;

public final class IslandFlagSolution {
    private static final int[] DR = {-1, 0, 1, 0, -1, -1, 1, 1};
    private static final int[] DC = {0, 1, 0, -1, -1, 1, 1, -1};

    static int solve(String[] grid, boolean diagonal) {
        int rows = grid.length, cols = grid[0].length(), moves = diagonal ? 8 : 4;
        boolean[] owned = new boolean[rows * cols];
        int[] stack = new int[rows * cols];
        int islands = 0;
        for (int start = 0; start < rows * cols; start++) {
            if (owned[start] || grid[start / cols].charAt(start % cols) != '1') continue;
            islands++;
            int top = 0;
            stack[top++] = start;
            owned[start] = true;
            while (top > 0) {
                int id = stack[--top];
                int r = id / cols, c = id % cols;
                for (int d = 0; d < moves; d++) {
                    int nr = r + DR[d], nc = c + DC[d];
                    if (nr < 0 || nr >= rows || nc < 0 || nc >= cols) continue;
                    int next = nr * cols + nc;
                    if (owned[next] || grid[nr].charAt(nc) != '1') continue;
                    owned[next] = true;
                    stack[top++] = next;
                }
            }
        }
        return islands;
    }

    static int oracle(String[] grid, boolean diagonal) {
        int rows = grid.length, cols = grid[0].length();
        int[] label = new int[rows * cols];
        for (int i = 0; i < label.length; i++) label[i] = i;
        boolean moved = true;
        while (moved) {
            moved = false;
            for (int i = 0; i < label.length; i++) {
                if (grid[i / cols].charAt(i % cols) != '1') continue;
                for (int j = 0; j < label.length; j++) {
                    if (grid[j / cols].charAt(j % cols) != '1') continue;
                    int dr = Math.abs(i / cols - j / cols), dc = Math.abs(i % cols - j % cols);
                    boolean touch = (dr + dc == 1) || (diagonal && dr == 1 && dc == 1);
                    if (touch && label[j] < label[i]) { label[i] = label[j]; moved = true; }
                }
            }
        }
        Set<Integer> kinds = new HashSet<>();
        for (int i = 0; i < label.length; i++) if (grid[i / cols].charAt(i % cols) == '1') kinds.add(label[i]);
        return kinds.size();
    }

    public static void main(String[] args) {
        String[] a = {"10010", "01100", "00001", "10010"};
        if (solve(a, true) != 3 || solve(a, false) != 6) throw new AssertionError("example 1 both flags");
        String[] b = {"0110", "1001", "0110"};
        if (solve(b, false) != 4 || solve(b, true) != 1) throw new AssertionError("example 2 both flags");
        String[] none = {"000"};
        if (solve(none, true) != 0 || solve(none, false) != 0) throw new AssertionError("no land");
        Random rnd = new Random(21102);
        for (int t = 0; t < 4000; t++) {
            int rows = 1 + rnd.nextInt(6), cols = 1 + rnd.nextInt(6);
            String[] g = new String[rows];
            for (int r = 0; r < rows; r++) {
                StringBuilder sb = new StringBuilder();
                for (int c = 0; c < cols; c++) sb.append(rnd.nextInt(5) < 2 ? '1' : '0');
                g[r] = sb.toString();
            }
            String[] before = g.clone();
            int straight = solve(g, false), diag = solve(g, true);
            if (straight != oracle(g, false)) throw new AssertionError("four-way differs");
            if (diag != oracle(g, true)) throw new AssertionError("eight-way differs");
            if (diag > straight) throw new AssertionError("diagonals cannot split an island");
            if (!java.util.Arrays.equals(before, g)) throw new AssertionError("grid changed");
        }
    }
}
```

#### Solution: [Boundary] Report On The Largest Island (LeetCode 695)
<!-- id: gg-largest-island-report -->

**Approach.** The outer scan starts a search at each unowned land cell, and the search returns how many cells it claimed. Three numbers ride along. When a size beats the best, the best becomes that size, the tie count resets to 1, and the first id becomes the start of that search. When a size equals the best, only the tie count grows, so the first id stays with the earlier island. A grid with no land keeps the initial `[0, 0, -1]`. Because the scan runs in reading order, the cell that starts an island is also its smallest id, and the solution checks that by tracking the minimum claimed id of every search. The oracle lowers labels to a fixpoint as the previous solution does, then counts cells per final label, so the first largest island is the one with the smallest label. The assertions replay both examples and the empty grid, and compare random grids against the oracle.

**Complexity.** The scan and the searches together visit each cell a constant number of times, so time is O(R * C) and memory is O(R * C).

```java run
import java.util.Arrays;
import java.util.Random;
import java.util.TreeMap;

public final class LargestIslandReportSolution {
    private static final int[] DR = {1, 0, -1, 0};
    private static final int[] DC = {0, -1, 0, 1};

    static int[] solve(String[] grid) {
        int rows = grid.length, cols = grid[0].length();
        boolean[] owned = new boolean[rows * cols];
        int[] stack = new int[rows * cols];
        int area = 0, ties = 0, firstId = -1;
        for (int start = 0; start < rows * cols; start++) {
            if (owned[start] || grid[start / cols].charAt(start % cols) != '1') continue;
            int top = 0, size = 0, smallest = start;
            stack[top++] = start;
            owned[start] = true;
            while (top > 0) {
                int id = stack[--top];
                size++;
                smallest = Math.min(smallest, id);
                int r = id / cols, c = id % cols;
                for (int d = 0; d < 4; d++) {
                    int nr = r + DR[d], nc = c + DC[d];
                    if (nr < 0 || nr >= rows || nc < 0 || nc >= cols) continue;
                    int next = nr * cols + nc;
                    if (owned[next] || grid[nr].charAt(nc) != '1') continue;
                    owned[next] = true;
                    stack[top++] = next;
                }
            }
            if (smallest != start) throw new AssertionError("a reading-order start is its island's smallest id");
            if (size > area) { area = size; ties = 1; firstId = start; }
            else if (size == area) ties++;
        }
        return new int[]{area, ties, firstId};
    }

    static int[] oracle(String[] grid) {
        int rows = grid.length, cols = grid[0].length(), n = rows * cols;
        int[] label = new int[n];
        for (int i = 0; i < n; i++) label[i] = i;
        boolean moved = true;
        while (moved) {
            moved = false;
            for (int i = 0; i < n; i++) {
                if (grid[i / cols].charAt(i % cols) != '1') continue;
                int r = i / cols, c = i % cols;
                for (int d = 0; d < 4; d++) {
                    int nr = r - DR[d], nc = c + DC[d];
                    if (nr < 0 || nr >= rows || nc < 0 || nc >= cols || grid[nr].charAt(nc) != '1') continue;
                    int j = nr * cols + nc;
                    if (label[j] < label[i]) { label[i] = label[j]; moved = true; }
                }
            }
        }
        TreeMap<Integer, Integer> sizes = new TreeMap<>();
        for (int i = 0; i < n; i++) if (grid[i / cols].charAt(i % cols) == '1') sizes.merge(label[i], 1, Integer::sum);
        int area = 0, ties = 0, first = -1;
        for (var e : sizes.entrySet()) {
            if (e.getValue() > area) { area = e.getValue(); ties = 1; first = e.getKey(); }
            else if (e.getValue() == area) ties++;
        }
        return new int[]{area, ties, first};
    }

    public static void main(String[] args) {
        if (!Arrays.equals(solve(new String[]{"1100", "0011", "1001"}), new int[]{3, 1, 6})) throw new AssertionError("example 1");
        if (!Arrays.equals(solve(new String[]{"1011", "0010", "1001", "1100"}), new int[]{3, 2, 2})) throw new AssertionError("example 2");
        if (!Arrays.equals(solve(new String[]{"0000"}), new int[]{0, 0, -1})) throw new AssertionError("no land");
        Random rnd = new Random(21103);
        for (int t = 0; t < 5000; t++) {
            int rows = 1 + rnd.nextInt(6), cols = 1 + rnd.nextInt(6);
            String[] g = new String[rows];
            for (int r = 0; r < rows; r++) {
                StringBuilder sb = new StringBuilder();
                for (int c = 0; c < cols; c++) sb.append(rnd.nextInt(5) < 2 ? '1' : '0');
                g[r] = sb.toString();
            }
            if (!Arrays.equals(solve(g), oracle(g))) throw new AssertionError("differs on " + Arrays.toString(g));
        }
    }
}
```

#### Solution: [Recognize] Clone A Patch Of Nodes (LeetCode 133)
<!-- id: gg-clone-cell-graph -->

**Approach.** The harness first builds one node object per nonzero digit and links each cell to its up, right, down and left neighbours in that order. The copying routine then sees only node objects. Its marks are an `IdentityHashMap` from original node to copy, written when a node is discovered and before it is expanded, and an explicit stack replaces the grid stack. Each popped original has its neighbour list walked, a missing copy is created and queued, and the copy of the neighbour is appended to the copy of the popped node. The answer is read off the copy alone, by a second identity-keyed walk that counts nodes and list entries, followed by the values of the start copy's neighbours. The oracle uses the grid and label propagation instead of objects: component size, twice the number of touching nonzero pairs inside the component, and the digits found around the start cell in the stated order. The assertions replay both examples, confirm that no copied node is an original object, that `Node` has no value-based `equals`, and that a map keyed by value would keep one entry for the all-fours grid where the identity map keeps four.

**Complexity.** Every node is copied once and every neighbour entry is wired once, giving O(V + E) time with O(V) memory for the map and the stack, where V is at most 144 here.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Deque;
import java.util.HashMap;
import java.util.IdentityHashMap;
import java.util.List;
import java.util.Map;
import java.util.Random;

public final class CloneCellGraphSolution {
    static final class Node {
        final int val;
        final List<Node> neighbors = new ArrayList<>();
        Node(int val) { this.val = val; }
    }

    private static final int[] DR = {-1, 0, 1, 0};
    private static final int[] DC = {0, 1, 0, -1};

    static Node cloneFrom(Node start) {
        Map<Node, Node> twin = new IdentityHashMap<>();
        Deque<Node> stack = new ArrayDeque<>();
        twin.put(start, new Node(start.val));
        stack.push(start);
        while (!stack.isEmpty()) {
            Node cur = stack.pop();
            Node mine = twin.get(cur);
            for (Node nb : cur.neighbors) {
                Node copy = twin.get(nb);
                if (copy == null) {
                    copy = new Node(nb.val);
                    twin.put(nb, copy);
                    stack.push(nb);
                }
                mine.neighbors.add(copy);
            }
        }
        return twin.get(start);
    }

    static Node[] build(int[][] grid) {
        int rows = grid.length, cols = grid[0].length;
        Node[] nodes = new Node[rows * cols];
        for (int i = 0; i < nodes.length; i++) if (grid[i / cols][i % cols] != 0) nodes[i] = new Node(grid[i / cols][i % cols]);
        for (int i = 0; i < nodes.length; i++) {
            if (nodes[i] == null) continue;
            for (int d = 0; d < 4; d++) {
                int nr = i / cols + DR[d], nc = i % cols + DC[d];
                if (nr >= 0 && nr < rows && nc >= 0 && nc < cols && nodes[nr * cols + nc] != null) nodes[i].neighbors.add(nodes[nr * cols + nc]);
            }
        }
        return nodes;
    }

    static List<Integer> solve(int[][] grid, int sr, int sc, boolean[] sharedFlag) {
        int cols = grid[0].length;
        Node[] nodes = build(grid);
        Node copy = cloneFrom(nodes[sr * cols + sc]);
        Map<Node, Boolean> original = new IdentityHashMap<>();
        for (Node n : nodes) if (n != null) original.put(n, true);
        Map<Node, Boolean> seen = new IdentityHashMap<>();
        Deque<Node> queue = new ArrayDeque<>();
        seen.put(copy, true);
        queue.add(copy);
        int entries = 0;
        while (!queue.isEmpty()) {
            Node cur = queue.poll();
            if (original.containsKey(cur)) sharedFlag[0] = true;
            entries += cur.neighbors.size();
            for (Node nb : cur.neighbors) if (seen.put(nb, true) == null) queue.add(nb);
        }
        List<Integer> out = new ArrayList<>(List.of(seen.size(), entries));
        for (Node nb : copy.neighbors) out.add(nb.val);
        return out;
    }

    static List<Integer> oracle(int[][] grid, int sr, int sc) {
        int rows = grid.length, cols = grid[0].length;
        boolean[][] in = new boolean[rows][cols];
        in[sr][sc] = true;
        boolean grew = true;
        while (grew) {
            grew = false;
            for (int r = 0; r < rows; r++) for (int c = 0; c < cols; c++) {
                if (in[r][c] || grid[r][c] == 0) continue;
                for (int d = 0; d < 4; d++) {
                    int nr = r + DR[d], nc = c + DC[d];
                    if (nr >= 0 && nr < rows && nc >= 0 && nc < cols && in[nr][nc]) { in[r][c] = true; grew = true; break; }
                }
            }
        }
        int nodes = 0, entries = 0;
        for (int r = 0; r < rows; r++) for (int c = 0; c < cols; c++) {
            if (!in[r][c]) continue;
            nodes++;
            for (int d = 0; d < 4; d++) {
                int nr = r + DR[d], nc = c + DC[d];
                if (nr >= 0 && nr < rows && nc >= 0 && nc < cols && grid[nr][nc] != 0) entries++;
            }
        }
        List<Integer> out = new ArrayList<>(List.of(nodes, entries));
        for (int d = 0; d < 4; d++) {
            int nr = sr + DR[d], nc = sc + DC[d];
            if (nr >= 0 && nr < rows && nc >= 0 && nc < cols && grid[nr][nc] != 0) out.add(grid[nr][nc]);
        }
        return out;
    }

    public static void main(String[] args) {
        boolean[] shared = {false};
        int[][] a = {{2, 2, 0}, {0, 2, 5}, {7, 0, 2}};
        if (!solve(a, 0, 1, shared).equals(List.of(5, 8, 2, 2))) throw new AssertionError("example 1");
        int[][] b = {{4, 4}, {4, 4}};
        if (!solve(b, 0, 0, shared).equals(List.of(4, 8, 4, 4))) throw new AssertionError("example 2");
        if (!solve(new int[][]{{1, 0, 1}}, 0, 2, shared).equals(List.of(1, 0))) throw new AssertionError("lone node");
        if (new Node(4).equals(new Node(4))) throw new AssertionError("Node must not compare by value");
        Map<Integer, Node> byValue = new HashMap<>();
        Map<Node, Node> byObject = new IdentityHashMap<>();
        for (Node n : build(b)) { byValue.put(n.val, n); byObject.put(n, n); }
        if (byValue.size() != 1 || byObject.size() != 4) throw new AssertionError("value keys fuse equal nodes");
        Random rnd = new Random(21104);
        for (int t = 0; t < 4000; t++) {
            int rows = 1 + rnd.nextInt(5), cols = 1 + rnd.nextInt(5);
            int[][] g = new int[rows][cols];
            for (int[] row : g) for (int c = 0; c < cols; c++) row[c] = rnd.nextInt(3) == 0 ? 0 : 1 + rnd.nextInt(2);
            int sr = rnd.nextInt(rows), sc = rnd.nextInt(cols);
            if (g[sr][sc] == 0) continue;
            if (!solve(g, sr, sc, shared).equals(oracle(g, sr, sc))) throw new AssertionError("differs on " + Arrays.deepToString(g));
        }
        if (shared[0]) throw new AssertionError("a copied node is an original object");
    }
}
```
