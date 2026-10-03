<!-- solutions-for: 09-quadtree-construction -->
### Quadtree Construction

#### Solution: [Build] Uniform Region Test (Author exercise)
<!-- id: tr-uniform-region -->

**Approach.** Read the first cell of the region, then loop over its rows and columns and return false at the first cell that differs, and true if the loop ends. The loop bounds are `top` to `top + side - 1` for rows and `left` to `left + side - 1` for columns, which stay inside the region and never touch its neighbours. The oracle collects the cells of the region into a set and asks whether the set has one element. The assertions compare the two on random grids and random regions, using regions that are aligned squares of every side, and check that a region of side one is always uniform.

**Complexity.** O(side squared) time in the worst case, and O(1) space.

```java run
import java.util.HashSet;
import java.util.Random;
import java.util.Set;

public final class UniformRegion {
    static boolean uniform(int[][] grid, int top, int left, int side) {
        int first = grid[top][left];
        for (int r = top; r < top + side; r++) {
            for (int c = left; c < left + side; c++) {
                if (grid[r][c] != first) return false;
            }
        }
        return true;
    }

    static boolean oracle(int[][] grid, int top, int left, int side) {
        Set<Integer> seen = new HashSet<>();
        for (int r = 0; r < side; r++) for (int c = 0; c < side; c++) seen.add(grid[top + r][left + c]);
        return seen.size() == 1;
    }

    static void paint(int[][] g, int top, int left, int side, Random rnd) {
        if (side == 1 || rnd.nextInt(3) == 0) {
            int v = rnd.nextInt(2);
            for (int r = top; r < top + side; r++) for (int c = left; c < left + side; c++) g[r][c] = v;
            return;
        }
        int h = side / 2;
        paint(g, top, left, h, rnd);
        paint(g, top, left + h, h, rnd);
        paint(g, top + h, left, h, rnd);
        paint(g, top + h, left + h, h, rnd);
    }

    public static void main(String[] args) {
        int[][] g = {{1, 1}, {1, 0}};
        if (!uniform(g, 0, 0, 1)) throw new AssertionError("example 1");
        if (uniform(g, 0, 0, 2)) throw new AssertionError("example 2");
        Random rnd = new Random(15901);
        for (int t = 0; t < 4000; t++) {
            int side = 1 << rnd.nextInt(5);
            int[][] grid = new int[side][side];
            paint(grid, 0, 0, side, rnd);
            for (int s = 1; s <= side; s *= 2) {
                int top = rnd.nextInt(side / s) * s, left = rnd.nextInt(side / s) * s;
                boolean got = uniform(grid, top, left, s);
                if (got != oracle(grid, top, left, s)) throw new AssertionError("differs at " + top + "," + left + " side " + s);
                if (s == 1 && !got) throw new AssertionError("one cell is always uniform");
            }
        }
    }
}
```

#### Solution: [Vary] Split Four Quadrants (Author exercise)
<!-- id: tr-split-quadrants -->

**Approach.** Let `half` be the side divided by two. The four children have side `half` and start at `(top, left)`, `(top, left + half)`, `(top + half, left)` and `(top + half, left + half)`, in the order top-left, top-right, bottom-left, bottom-right. The division is exact because the side is even. The oracle marks cells instead of reading formulas: it creates a count array for the parent's cells, adds one for every cell of every child, and requires that every cell of the parent was counted exactly once and that no child cell falls outside the parent. It also checks the order by finding which parent corner each child contains. The assertions run this for every even power-of-two side and random offsets.

**Complexity.** Constant time for the split itself, and O(side squared) for the oracle.

```java run
import java.util.Arrays;
import java.util.Random;

public final class SplitQuadrants {
    static int[][] split(int top, int left, int side) {
        int half = side / 2;
        return new int[][] {
            {top, left, half},
            {top, left + half, half},
            {top + half, left, half},
            {top + half, left + half, half}
        };
    }

    static void check(int top, int left, int side) {
        int[][] kids = split(top, left, side);
        int[][] count = new int[side][side];
        for (int[] k : kids) {
            for (int r = k[0]; r < k[0] + k[2]; r++) {
                for (int c = k[1]; c < k[1] + k[2]; c++) {
                    int rr = r - top, cc = c - left;
                    if (rr < 0 || cc < 0 || rr >= side || cc >= side) throw new AssertionError("child cell outside the parent");
                    count[rr][cc]++;
                }
            }
        }
        for (int[] row : count) for (int v : row) if (v != 1) throw new AssertionError("every cell is covered exactly once, saw " + v);
        int[][] corners = {{top, left}, {top, left + side - 1}, {top + side - 1, left}, {top + side - 1, left + side - 1}};
        for (int i = 0; i < 4; i++) {
            int[] k = kids[i];
            boolean inside = corners[i][0] >= k[0] && corners[i][0] < k[0] + k[2] && corners[i][1] >= k[1] && corners[i][1] < k[1] + k[2];
            if (!inside) throw new AssertionError("child " + i + " holds the wrong corner of the parent");
        }
    }

    public static void main(String[] args) {
        if (!Arrays.deepEquals(split(0, 0, 4), new int[][] {{0, 0, 2}, {0, 2, 2}, {2, 0, 2}, {2, 2, 2}})) throw new AssertionError("example 1");
        if (!Arrays.deepEquals(split(2, 4, 2), new int[][] {{2, 4, 1}, {2, 5, 1}, {3, 4, 1}, {3, 5, 1}})) throw new AssertionError("example 2");
        Random rnd = new Random(15902);
        for (int s = 2; s <= 64; s *= 2) {
            for (int t = 0; t < 40; t++) check(rnd.nextInt(1001), rnd.nextInt(1001), s);
        }
        if (1 / 2 != 0) throw new AssertionError("integer division of a side of one gives zero");
    }
}
```

#### Solution: [Boundary] One Cell (Author exercise)
<!-- id: tr-one-cell -->

**Approach.** A call returns one node when its block is uniform, which includes every block of side one, and otherwise returns one plus the counts of its four quadrant calls. Since a side-one block is uniform by itself, the recursion never divides a single cell and never reaches a side of zero. The oracle follows the naive route: it builds the full tree down to single tiles and then merges bottom-up, collapsing four equal leaves into one, and counts the nodes that remain. The assertions compare the two counts on random grids, and also count the nodes the full tree creates for an all-equal grid of side 64 to show the saving.

**Complexity.** O(N log n) time for N cells at worst, and O(log n) stack.

```java run
import java.util.Random;

public final class OneCell {
    static int count(int[][] g, int top, int left, int side) {
        int first = g[top][left];
        boolean same = true;
        for (int r = top; r < top + side && same; r++)
            for (int c = left; c < left + side; c++)
                if (g[r][c] != first) { same = false; break; }
        if (same) return 1;
        int h = side / 2;
        return 1 + count(g, top, left, h) + count(g, top, left + h, h)
                 + count(g, top + h, left, h) + count(g, top + h, left + h, h);
    }

    static int fullNodes;

    static int[] collapse(int[][] g, int top, int left, int side) {
        fullNodes++;
        if (side == 1) return new int[] {g[top][left], 1};
        int h = side / 2;
        int[] a = collapse(g, top, left, h), b = collapse(g, top, left + h, h);
        int[] c = collapse(g, top + h, left, h), d = collapse(g, top + h, left + h, h);
        boolean leaves = a[1] == 1 && b[1] == 1 && c[1] == 1 && d[1] == 1;
        if (leaves && a[0] == b[0] && b[0] == c[0] && c[0] == d[0]) return new int[] {a[0], 1};
        return new int[] {-1, 1 + a[1] + b[1] + c[1] + d[1]};
    }

    static void paint(int[][] g, int top, int left, int side, Random rnd) {
        if (side == 1 || rnd.nextInt(3) == 0) {
            int v = rnd.nextInt(2);
            for (int r = top; r < top + side; r++) for (int c = left; c < left + side; c++) g[r][c] = v;
            return;
        }
        int h = side / 2;
        paint(g, top, left, h, rnd);
        paint(g, top, left + h, h, rnd);
        paint(g, top + h, left, h, rnd);
        paint(g, top + h, left + h, h, rnd);
    }

    public static void main(String[] args) {
        if (count(new int[][] {{1}}, 0, 0, 1) != 1) throw new AssertionError("example 1");
        if (count(new int[][] {{1, 0}, {0, 1}}, 0, 0, 2) != 5) throw new AssertionError("example 2");
        if (count(new int[][] {{1, 1}, {1, 1}}, 0, 0, 2) != 1) throw new AssertionError("a uniform grid is one leaf");
        Random rnd = new Random(15903);
        for (int t = 0; t < 4000; t++) {
            int side = 1 << rnd.nextInt(5);
            int[][] g = new int[side][side];
            paint(g, 0, 0, side, rnd);
            if (rnd.nextInt(4) == 0) g[rnd.nextInt(side)][rnd.nextInt(side)] ^= 1;
            int want = collapse(g, 0, 0, side)[1];
            if (count(g, 0, 0, side) != want) throw new AssertionError("differs at side " + side);
        }
        int[][] flat = new int[64][64];
        fullNodes = 0;
        collapse(flat, 0, 0, 64);
        if (fullNodes != 5461) throw new AssertionError("the full tree allocates every level: " + fullNodes);
        if (count(flat, 0, 0, 64) != 1) throw new AssertionError("the compressed tree of a flat floor is one node");
    }
}
```

#### Solution: [Recognize] Construct Quad Tree (LeetCode 427)
<!-- id: tr-construct-quad-tree -->

**Approach.** Each call owns a block given by top, left and side. It tests the block for a single value, returns a leaf node holding it when the block is uniform, and otherwise creates an internal node with four children built from the four quadrants in the order top-left, top-right, bottom-left and bottom-right. The node tree is then written in preorder, with the value for a leaf and parentheses around the four child strings for an internal node. The oracle builds the full tree down to single cells and merges four equal leaves bottom-up. The assertions compare the two serialisations on random grids and count how many nodes each builder creates for a flat floor, which is one for the top-down builder.

**Complexity.** O(N log n) time at worst for N cells, and O(log n) stack plus the nodes of the answer.

```java run
import java.util.Random;

public final class ConstructQuadTree {
    static final class Quad {
        final int val;
        final Quad[] kids;
        Quad(int val, Quad[] kids) { this.val = val; this.kids = kids; }
        boolean leaf() { return kids == null; }
    }

    static int created;

    static boolean uniform(int[][] g, int top, int left, int side) {
        int first = g[top][left];
        for (int r = top; r < top + side; r++)
            for (int c = left; c < left + side; c++)
                if (g[r][c] != first) return false;
        return true;
    }

    static Quad build(int[][] g, int top, int left, int side) {
        if (uniform(g, top, left, side)) { created++; return new Quad(g[top][left], null); }
        int h = side / 2;
        Quad[] kids = {
            build(g, top, left, h), build(g, top, left + h, h),
            build(g, top + h, left, h), build(g, top + h, left + h, h)
        };
        created++;
        return new Quad(-1, kids);
    }

    static Quad fullThenMerge(int[][] g, int top, int left, int side) {
        created++;
        if (side == 1) return new Quad(g[top][left], null);
        int h = side / 2;
        Quad a = fullThenMerge(g, top, left, h), b = fullThenMerge(g, top, left + h, h);
        Quad c = fullThenMerge(g, top + h, left, h), d = fullThenMerge(g, top + h, left + h, h);
        if (a.leaf() && b.leaf() && c.leaf() && d.leaf() && a.val == b.val && b.val == c.val && c.val == d.val) return new Quad(a.val, null);
        return new Quad(-1, new Quad[] {a, b, c, d});
    }

    static String write(Quad q) {
        if (q.leaf()) return String.valueOf(q.val);
        StringBuilder sb = new StringBuilder("(");
        for (Quad k : q.kids) sb.append(write(k));
        return sb.append(')').toString();
    }

    static void paint(int[][] g, int top, int left, int side, Random rnd) {
        if (side == 1 || rnd.nextInt(3) == 0) {
            int v = rnd.nextInt(2);
            for (int r = top; r < top + side; r++) for (int c = left; c < left + side; c++) g[r][c] = v;
            return;
        }
        int h = side / 2;
        paint(g, top, left, h, rnd);
        paint(g, top, left + h, h, rnd);
        paint(g, top + h, left, h, rnd);
        paint(g, top + h, left + h, h, rnd);
    }

    public static void main(String[] args) {
        if (!write(build(new int[][] {{1, 1}, {1, 1}}, 0, 0, 2)).equals("1")) throw new AssertionError("example 1");
        if (!write(build(new int[][] {{1, 0}, {1, 1}}, 0, 0, 2)).equals("(1011)")) throw new AssertionError("example 2");
        Random rnd = new Random(15904);
        for (int t = 0; t < 4000; t++) {
            int side = 1 << rnd.nextInt(5);
            int[][] g = new int[side][side];
            paint(g, 0, 0, side, rnd);
            if (rnd.nextInt(3) == 0) g[rnd.nextInt(side)][rnd.nextInt(side)] ^= 1;
            String got = write(build(g, 0, 0, side));
            String want = write(fullThenMerge(g, 0, 0, side));
            if (!got.equals(want)) throw new AssertionError("differs at side " + side + ": " + got + " against " + want);
        }
        int[][] flat = new int[64][64];
        created = 0;
        build(flat, 0, 0, 64);
        if (created != 1) throw new AssertionError("a flat floor is one node, built " + created);
        created = 0;
        fullThenMerge(flat, 0, 0, 64);
        if (created != 5461) throw new AssertionError("the full tree creates every node first: " + created);
    }
}
```
