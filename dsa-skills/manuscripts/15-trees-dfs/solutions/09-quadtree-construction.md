<!-- solutions-for: 09-quadtree-construction -->
### Solutions For Splitting A Grid

#### Solution: [Build] Uniform Region Test (Author exercise)
<!-- id: qt-uniform -->

**Approach.**
The method reads the cell at the top-left corner of the region and compares every other cell of the region with it. The first cell that differs ends the scan and returns `false`. If the scan reaches the last cell, every cell agreed, and the method returns `true`. The invariant is that at the start of each comparison, all cells already read are equal to the first cell.

A check of the four corners would not be enough. Two corners can agree while a cell between them differs, and the section below confirms this with a grid.

**Complexity.**
- **Time** is O(size^2) in the worst case, because a uniform region is read cell by cell, and a mixed region may stop earlier.
- **Space** is O(1), because the method keeps a few integers.

```java run
import java.util.*;

public final class UniformTest {
    /**
     * Tells whether every cell of the region equals its top-left cell.
     * Time: O(size^2) worst case.
     * Space: O(1).
     * Invariant: all cells read so far equal the first cell.
     */
    static boolean uniform(int[][] g, int r, int c, int size) {
        int first = g[r][c];                                     // the value that every cell must equal
        for (int i = r; i < r + size; i++) {                     // visit the rows of the region
            for (int j = c; j < c + size; j++) {                 // visit the cells of one row
                if (g[i][j] != first) return false;              // one difference ends the test
            }
        }
        return true;                                             // no cell differed
    }

    static boolean cornersOnly(int[][] g, int r, int c, int size) {
        int e = r + size - 1, f = c + size - 1;
        return g[r][c] == g[r][f] && g[r][c] == g[e][c] && g[r][c] == g[e][f];
    }

    public static void main(String[] args) {
        int[][] a = {{1, 1, 0, 0}, {1, 1, 0, 0}, {1, 1, 1, 1}, {1, 1, 1, 1}};
        int[][] b = {{0, 0, 1, 1}, {0, 0, 1, 0}, {1, 1, 1, 1}, {1, 1, 1, 1}};
        // Example 1: the top-left quadrant of the first grid is all 1.
        if (!uniform(a, 0, 0, 2)) throw new AssertionError("ex1");
        // Example 2: the top-right quadrant of the second grid has a 0 in its last cell.
        if (uniform(b, 0, 2, 2)) throw new AssertionError("ex2");
        // A region of size 1 is always uniform.
        if (!uniform(b, 3, 3, 1)) throw new AssertionError("single cell");
        // The four corners can agree while a cell between them differs.
        int[][] hole = {{1, 1, 1, 1}, {1, 0, 1, 1}, {1, 1, 1, 1}, {1, 1, 1, 1}};
        if (!cornersOnly(hole, 0, 0, 4) || uniform(hole, 0, 0, 4)) throw new AssertionError("corners");
        // Random regions must match a count of cells equal to the first cell.
        Random rnd = new Random(33);
        for (int t = 0; t < 800; t++) {
            int n = 1 << rnd.nextInt(4);
            int[][] g = new int[n][n];
            for (int[] row : g) for (int j = 0; j < n; j++) row[j] = rnd.nextInt(6) == 0 ? 1 : 0;
            int size = 1 << rnd.nextInt(Integer.numberOfTrailingZeros(n) + 1);
            int r = rnd.nextInt(n - size + 1), c = rnd.nextInt(n - size + 1);
            int same = 0;
            for (int i = r; i < r + size; i++) for (int j = c; j < c + size; j++) if (g[i][j] == g[r][c]) same++;
            if (uniform(g, r, c, size) != (same == size * size)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Vary] Split Four Quadrants (Author exercise)
<!-- id: qt-split -->

**Approach.**
The side of each quadrant is `size / 2`, and the division is exact because the side is even. The top-left quadrant keeps the corner `(r, c)`. The top-right quadrant adds `half` to the column. The bottom-left quadrant adds `half` to the row. The bottom-right quadrant adds `half` to both. The four squares do not overlap and together cover exactly `size * size` cells. Each quadrant has `half * half` cells, and four of them add up to the whole.

**Complexity.**
- **Time** is O(1), because the method computes four triples.
- **Space** is O(1), because the output has a fixed size.

```java run
import java.util.*;

public final class SplitRegion {
    /**
     * Returns the four quadrants of a region with even side.
     * Time: O(1).
     * Space: O(1).
     * Invariant: the quadrants tile the region without overlap.
     */
    static int[][] quadrants(int r, int c, int size) {
        int half = size / 2;                                     // the side of every quadrant
        return new int[][] {
            {r, c, half},                                        // top-left keeps the corner
            {r, c + half, half},                                 // top-right moves right by half
            {r + half, c, half},                                 // bottom-left moves down by half
            {r + half, c + half, half}                           // bottom-right moves both ways
        };
    }

    public static void main(String[] args) {
        // Example 1: the region (0, 0, 4).
        if (!Arrays.deepEquals(quadrants(0, 0, 4), new int[][] {{0, 0, 2}, {0, 2, 2}, {2, 0, 2}, {2, 2, 2}})) throw new AssertionError("ex1");
        // Example 2: the region (4, 2, 2).
        if (!Arrays.deepEquals(quadrants(4, 2, 2), new int[][] {{4, 2, 1}, {4, 3, 1}, {5, 2, 1}, {5, 3, 1}})) throw new AssertionError("ex2");
        // Odd sides do not tile: a side of 3 covers only 4 of 9 cells.
        int[][] odd = quadrants(0, 0, 3);
        int covered = 0;
        for (int[] q : odd) covered += q[2] * q[2];
        if (covered != 4) throw new AssertionError("odd side");
        // Random even regions: each cell of the region lies in exactly one quadrant.
        Random rnd = new Random(34);
        for (int t = 0; t < 800; t++) {
            int size = 2 * (1 + rnd.nextInt(8));
            int r = rnd.nextInt(20), c = rnd.nextInt(20);
            int[][] q = quadrants(r, c, size);
            int[][] hits = new int[size][size];
            for (int[] part : q) {
                if (part[2] != size / 2) throw new AssertionError("side " + t);
                for (int i = part[0]; i < part[0] + part[2]; i++)
                    for (int j = part[1]; j < part[1] + part[2]; j++) hits[i - r][j - c]++;
            }
            for (int[] row : hits) for (int h : row) if (h != 1) throw new AssertionError("tiling " + t);
        }
    }
}
```

#### Solution: [Boundary] One Cell (Author exercise)
<!-- id: qt-leaf-count -->

**Approach.**
The call tests the region before it cuts. A uniform region counts as one leaf. A mixed region is cut into four quadrants, and the call returns the sum of the four leaf counts. A region of side 1 is always uniform, so the recursion never asks for a quadrant of a single cell, and the value `size / 2 = 0` never appears. The invariant is that every call owns a region of side at least 1.

**Complexity.**
- **Time** is O(n^2 log n), because each level scans at most n^2 cells and there are about log n levels.
- **Space** is O(log n) for the stack.

```java run
import java.util.*;

public final class LeafCountQuad {
    /**
     * Counts the leaves of the quadtree of a region.
     * Time: O(n^2 log n).
     * Space: O(log n).
     * Invariant: every call owns a region of side at least 1.
     */
    static int leaves(int[][] g, int r, int c, int size) {
        int first = g[r][c];
        boolean same = true;
        for (int i = r; i < r + size && same; i++)               // scan the rows of the region
            for (int j = c; j < c + size; j++)
                if (g[i][j] != first) { same = false; break; }   // a different cell ends the scan
        if (same) return 1;                                      // a uniform region is one leaf, even for one cell
        int h = size / 2;                                        // a mixed region has side at least 2
        return leaves(g, r, c, h) + leaves(g, r, c + h, h)
             + leaves(g, r + h, c, h) + leaves(g, r + h, c + h, h);
    }

    // Oracle: build the full tree of cells, then merge four equal sibling leaves bottom-up.
    static int[] merged(int[][] g, int r, int c, int size) {     // returns {isLeaf, value, leafCount}
        if (size == 1) return new int[] {1, g[r][c], 1};
        int h = size / 2;
        int[][] k = {merged(g, r, c, h), merged(g, r, c + h, h), merged(g, r + h, c, h), merged(g, r + h, c + h, h)};
        boolean allLeaf = true, allSame = true;
        for (int[] x : k) { allLeaf &= x[0] == 1; allSame &= x[1] == k[0][1]; }
        if (allLeaf && allSame) return new int[] {1, k[0][1], 1};
        return new int[] {0, 0, k[0][2] + k[1][2] + k[2][2] + k[3][2]};
    }

    public static void main(String[] args) {
        // Example 1: a single cell is one leaf.
        if (leaves(new int[][] {{1}}, 0, 0, 1) != 1) throw new AssertionError("ex1");
        // Example 2: a checker of side 2 has four leaves.
        if (leaves(new int[][] {{0, 1}, {1, 0}}, 0, 0, 2) != 4) throw new AssertionError("ex2");
        // A uniform grid of side 8 is one leaf.
        int[][] blank = new int[8][8];
        if (leaves(blank, 0, 0, 8) != 1) throw new AssertionError("blank");
        // Random grids with side up to 16 must match the bottom-up merge.
        Random rnd = new Random(35);
        for (int t = 0; t < 800; t++) {
            int n = 1 << rnd.nextInt(5);
            int[][] g = new int[n][n];
            int p = 1 + rnd.nextInt(5);
            for (int[] row : g) for (int j = 0; j < n; j++) row[j] = rnd.nextInt(12) < p ? 1 : 0;
            if (leaves(g, 0, 0, n) != merged(g, 0, 0, n)[2]) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Recognize] Construct Quad Tree (LeetCode 427)
<!-- id: qt-construct -->

**Approach.**
A call owns a region and first tests whether every cell equals the top-left cell. A uniform region returns one leaf with that value. A mixed region is cut at `half = size / 2`. The call builds an internal node. Its four children come from the four quadrants, in the order top-left, top-right, bottom-left, bottom-right. Each call returns the node for exactly its region. The test before the cut guarantees that no internal node has four equal leaf children.

The checks below also confirm two claims of the lesson. Cutting before testing creates 85 nodes for a blank grid of side 8. Integer division loses cells for a side that is not a power of two.

**Complexity.**
- **Time** is O(n^2 log n), because each level scans at most n^2 cells and there are about log n levels.
- **Space** is O(log n) for the stack, plus the tree, whose size is at most about 4/3 of the number of cells.

```java run
import java.util.*;

public final class ConstructQuad {
    static final class Node {
        boolean val;
        boolean isLeaf;
        Node topLeft, topRight, bottomLeft, bottomRight;
        Node(boolean val, boolean isLeaf) { this.val = val; this.isLeaf = isLeaf; }
    }

    /**
     * Builds the quadtree of a square grid.
     * Time: O(n^2 log n).
     * Space: O(log n) for the stack, plus the tree.
     * Invariant: each call returns the node for exactly its region.
     */
    static Node build(int[][] g, int r, int c, int size) {
        int first = g[r][c];
        boolean same = true;
        for (int i = r; i < r + size && same; i++)               // scan the rows of the region
            for (int j = c; j < c + size; j++)
                if (g[i][j] != first) { same = false; break; }   // a different cell ends the scan
        if (same) return new Node(first == 1, true);             // one leaf for the whole region
        int h = size / 2;                                        // the side of each quadrant
        Node n = new Node(true, false);                          // an internal node
        n.topLeft = build(g, r, c, h);
        n.topRight = build(g, r, c + h, h);
        n.bottomLeft = build(g, r + h, c, h);
        n.bottomRight = build(g, r + h, c + h, h);
        return n;
    }

    static int cutFirstNodes;                                    // counts nodes of the cut-first method

    static void cutFirst(int[][] g, int r, int c, int size) {
        cutFirstNodes++;
        if (size == 1) return;
        int h = size / 2;
        cutFirst(g, r, c, h);
        cutFirst(g, r, c + h, h);
        cutFirst(g, r + h, c, h);
        cutFirst(g, r + h, c + h, h);
    }

    // Oracle: the value of every cell is read back from the tree, and no internal node may have four equal leaves.
    static int read(Node n, int r, int c, int size, int qr, int qc) {
        if (n.isLeaf) return n.val ? 1 : 0;
        int h = size / 2;
        if (qr < r + h) return qc < c + h ? read(n.topLeft, r, c, h, qr, qc) : read(n.topRight, r, c + h, h, qr, qc);
        return qc < c + h ? read(n.bottomLeft, r + h, c, h, qr, qc) : read(n.bottomRight, r + h, c + h, h, qr, qc);
    }

    static boolean minimal(Node n) {
        if (n.isLeaf) return true;
        Node[] k = {n.topLeft, n.topRight, n.bottomLeft, n.bottomRight};
        boolean fourEqual = true;
        for (Node x : k) fourEqual &= x.isLeaf && x.val == k[0].val;
        if (fourEqual) return false;                             // such a node should have been one leaf
        for (Node x : k) if (!minimal(x)) return false;
        return true;
    }

    public static void main(String[] args) {
        // Example 1: the second grid of the lesson.
        int[][] g = {{0, 0, 1, 1}, {0, 0, 1, 0}, {1, 1, 1, 1}, {1, 1, 1, 1}};
        Node r = build(g, 0, 0, 4);
        if (r.isLeaf || !r.topLeft.isLeaf || r.topLeft.val || r.topRight.isLeaf) throw new AssertionError("ex1 top");
        Node tr = r.topRight;
        if (!tr.topLeft.val || !tr.topRight.val || !tr.bottomLeft.val || tr.bottomRight.val) throw new AssertionError("ex1 cells");
        if (!r.bottomLeft.isLeaf || !r.bottomLeft.val || !r.bottomRight.isLeaf || !r.bottomRight.val) throw new AssertionError("ex1 bottom");
        // Example 2: a blank 2 by 2 grid is a single leaf.
        Node z = build(new int[][] {{0, 0}, {0, 0}}, 0, 0, 2);
        if (!z.isLeaf || z.val) throw new AssertionError("ex2");
        // Cutting before testing creates 85 nodes for a blank grid of side 8.
        cutFirstNodes = 0;
        cutFirst(new int[8][8], 0, 0, 8);
        if (cutFirstNodes != 85) throw new AssertionError("cut first");
        // Integer division loses cells for a side of 3: the four quadrants cover 4 of 9 cells.
        if (4 * (3 / 2) * (3 / 2) != 4) throw new AssertionError("odd side");
        // Random grids: every cell reads back correctly, and no node can be merged further.
        Random rnd = new Random(36);
        for (int t = 0; t < 800; t++) {
            int n = 1 << rnd.nextInt(5);
            int[][] a = new int[n][n];
            int p = 1 + rnd.nextInt(5);
            for (int[] row : a) for (int j = 0; j < n; j++) row[j] = rnd.nextInt(12) < p ? 1 : 0;
            Node x = build(a, 0, 0, n);
            if (!minimal(x)) throw new AssertionError("minimal " + t);
            for (int i = 0; i < n; i++) for (int j = 0; j < n; j++)
                if (read(x, 0, 0, n, i, j) != a[i][j]) throw new AssertionError("cell " + t);
        }
    }
}
```
