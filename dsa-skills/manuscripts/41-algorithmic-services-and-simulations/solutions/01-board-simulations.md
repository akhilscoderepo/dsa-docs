<!-- solutions-for: 01-board-simulations -->
### Solutions For Move Pieces On A Board

#### Solution: [Build] Design Tic-Tac-Toe (LeetCode 348)
<!-- id: sv-board-tictactoe -->

**Approach.** An owner array of bytes is the authoritative record of the marks. Four derived values summarize it: a signed sum for each row, a signed sum for each column, and one sum for each diagonal. Player 1 adds 1 and player 2 adds -1, so a line holds n marks of one player exactly when its sum has absolute value n.

A move first validates the game state, the coordinates and the cell, and it returns -1 without a write when any check fails. Only then does it store the owner, raise the mark count and update the at most four sums that contain the cell. The winner field is set once and blocks every later move.

The invariant is that each sum equals the signed number of marks on its line, and a rejected move writes none of the fields.

**Complexity.**

- **Time** per call is O(1), since a move touches at most four sums.
- **Space** is O(n^2) for the owner array plus O(n) for the sums.

```java run
import java.util.*;

public final class TicTacToeSolution {
    static final class Board {
        private final int n;
        private final byte[] owner;                                // authoritative marks
        private final int[] rowSum, colSum;                         // derived sums per row and column
        private int diagSum, antiSum, marks, winner;

        Board(int n) {
            this.n = n;
            this.owner = new byte[n * n];
            this.rowSum = new int[n];
            this.colSum = new int[n];
        }

        /**
         * Places a mark or rejects the move.
         * Time: O(1).
         * Space: O(1).
         * Invariant: every check runs before the first write.
         */
        int move(int row, int col, int player) {
            // A finished game rejects every move.
            if (winner != 0) return -1;
            // Coordinates outside the grid are illegal.
            if (row < 0 || col < 0 || row >= n || col >= n) return -1;
            // A taken cell is illegal.
            if (owner[row * n + col] != 0) return -1;
            int d = player == 1 ? 1 : -1;
            // All checks passed, so the writes below cannot be partial.
            owner[row * n + col] = (byte) player;
            marks++;
            rowSum[row] += d;
            colSum[col] += d;
            if (row == col) diagSum += d;
            if (row + col == n - 1) antiSum += d;
            // Only the four sums that contain the cell can have reached n in absolute value.
            if (Math.abs(rowSum[row]) == n || Math.abs(colSum[col]) == n
                    || (row == col && Math.abs(diagSum) == n)
                    || (row + col == n - 1 && Math.abs(antiSum) == n)) winner = player;
            return winner;
        }

        int filled() { return marks; }
    }

    /** Brute force: stores the grid and scans every line after each legal move. */
    static final class Oracle {
        final int n; final int[][] g; int marks; boolean over;
        Oracle(int n) { this.n = n; g = new int[n][n]; }
        int move(int r, int c, int p) {
            if (over || r < 0 || c < 0 || r >= n || c >= n || g[r][c] != 0) return -1;
            g[r][c] = p; marks++;
            for (int q = 1; q <= 2; q++) {
                boolean d = true, a = true;
                for (int i = 0; i < n; i++) {
                    boolean rf = true, cf = true;
                    for (int j = 0; j < n; j++) { if (g[i][j] != q) rf = false; if (g[j][i] != q) cf = false; }
                    if (rf || cf) { over = true; return q; }
                    if (g[i][i] != q) d = false;
                    if (g[i][n - 1 - i] != q) a = false;
                }
                if (d || a) { over = true; return q; }
            }
            return 0;
        }
    }

    public static void main(String[] args) {
        // Example 1 from the problem text.
        Board b = new Board(3);
        int[][] e1 = {{0, 0, 1, 0}, {0, 0, 2, -1}, {1, 1, 1, 0}, {2, 2, 1, 1}, {0, 1, 2, -1}};
        for (int[] m : e1) if (b.move(m[0], m[1], m[2]) != m[3]) throw new AssertionError("example 1");
        if (b.filled() != 3) throw new AssertionError("example 1 filled");
        // Example 2 includes a coordinate outside the grid.
        b = new Board(2);
        int[][] e2 = {{0, 0, 1, 0}, {2, 0, 1, -1}, {1, 1, 2, 0}, {0, 1, 2, 2}};
        for (int[] m : e2) if (b.move(m[0], m[1], m[2]) != m[3]) throw new AssertionError("example 2");
        if (b.filled() != 3) throw new AssertionError("example 2 filled");
        // Random games, including out-of-range and repeated cells, against the scanning oracle.
        Random rnd = new Random(348);
        for (int round = 0; round < 2000; round++) {
            int n = 1 + rnd.nextInt(5);
            Board s = new Board(n);
            Oracle o = new Oracle(n);
            for (int op = 0; op < 30; op++) {
                int r = rnd.nextInt(n + 2) - 1, c = rnd.nextInt(n + 2) - 1, p = 1 + rnd.nextInt(2);
                if (s.move(r, c, p) != o.move(r, c, p)) throw new AssertionError("move mismatch");
                if (s.filled() != o.marks) throw new AssertionError("filled mismatch");
            }
        }
    }
}
```

#### Solution: [Vary] Design Snake Game (LeetCode 353)
<!-- id: sv-board-snake -->

**Approach.** The body deque holds the cells from head to tail and is the authoritative state. A bit set indexed by `row * width + col` is derived from it and answers whether a cell is taken. The call also keeps the number of eaten food cells, which is both the score and the index of the visible food.

A move computes the new head cell and rejects it when it leaves the grid. It then decides whether the cell holds the visible food. A cell in the occupancy set blocks the move, except that the tail cell does not block a move that does not eat, because that move releases the tail before the head enters. When the move is blocked the game is over and the deque and the set stay as they were. Otherwise a non-eating move removes the tail from both structures, and every legal move adds the head to both.

The invariant is that the occupancy set holds exactly the cells of the body deque after each accepted move, and a rejected move writes nothing except the game-over flag.

**Complexity.**

- **Time** per call is O(1), since a move runs a fixed number of deque and bit set operations.
- **Space** is O(width * height + F) for the bit set and the F food cells, plus O(L) for a body of length L.

```java run
import java.util.*;

public final class SnakeSolution {
    static final class Snake {
        private final int width, height;
        private final int[][] food;
        private final ArrayDeque<Integer> body = new ArrayDeque<>();   // head first, tail last
        private final BitSet occupancySet = new BitSet();              // derived from the deque
        private int eaten;
        private boolean over;

        Snake(int width, int height, int[][] food) {
            this.width = width; this.height = height; this.food = food;
            body.addFirst(0);
            occupancySet.set(0);
        }

        /**
         * Moves the head one cell and returns the score, or -1 when the game is over.
         * Time: O(1).
         * Space: O(1).
         * Invariant: occupancySet equals the cells of body after each accepted move.
         */
        int move(char direction) {
            // A finished game rejects every move.
            if (over) return -1;
            int head = body.peekFirst();
            int r = head / width, c = head % width;
            switch (direction) {
                case 'U' -> r--;
                case 'D' -> r++;
                case 'L' -> c--;
                default -> c++;
            }
            // Leaving the grid ends the game before any write.
            if (r < 0 || c < 0 || r >= height || c >= width) { over = true; return -1; }
            int cell = r * width + c;
            boolean eats = eaten < food.length && food[eaten][0] == r && food[eaten][1] == c;
            int tail = body.peekLast();
            // The tail cell is free for a move that does not eat, so only other body cells block.
            if (occupancySet.get(cell) && (eats || cell != tail)) { over = true; return -1; }
            if (eats) {
                // Growth keeps the tail and reveals the next food.
                eaten++;
            } else {
                // The tail leaves both structures before the head enters.
                body.pollLast();
                occupancySet.clear(tail);
            }
            body.addFirst(cell);
            occupancySet.set(cell);
            return eaten;
        }

        boolean consistent() {
            BitSet check = new BitSet();
            for (int cell : body) check.set(cell);
            return check.equals(occupancySet);
        }
    }

    /** Brute force: a list of cells, tail removed first, then a linear search for the head. */
    static final class Oracle {
        final int w, h; final int[][] food; final ArrayList<int[]> body = new ArrayList<>(); int eaten; boolean over;
        Oracle(int w, int h, int[][] food) { this.w = w; this.h = h; this.food = food; body.add(new int[] {0, 0}); }
        int move(char d) {
            if (over) return -1;
            int[] hd = body.get(body.size() - 1);
            int r = hd[0] + (d == 'U' ? -1 : d == 'D' ? 1 : 0), c = hd[1] + (d == 'L' ? -1 : d == 'R' ? 1 : 0);
            if (r < 0 || c < 0 || r >= h || c >= w) { over = true; return -1; }
            boolean eat = eaten < food.length && food[eaten][0] == r && food[eaten][1] == c;
            if (!eat) body.remove(0);
            for (int[] b : body) if (b[0] == r && b[1] == c) { over = true; return -1; }
            body.add(new int[] {r, c});
            if (eat) eaten++;
            return eaten;
        }
    }

    public static void main(String[] args) {
        // Example 1: the last move hits a middle segment.
        Snake s = new Snake(3, 3, new int[][] {{0, 1}, {1, 1}, {1, 0}});
        int[] want1 = {1, 2, 3, 3, -1};
        String m1 = "RDLUD";
        for (int i = 0; i < 5; i++) if (s.move(m1.charAt(i)) != want1[i]) throw new AssertionError("example 1 at " + i);
        // Example 2: the head keeps entering the cell the tail just left.
        s = new Snake(2, 2, new int[][] {{0, 1}, {1, 1}, {1, 0}});
        int[] want2 = {1, 2, 3, 3, 3};
        String m2 = "RDLUR";
        for (int i = 0; i < 5; i++) if (s.move(m2.charAt(i)) != want2[i]) throw new AssertionError("example 2 at " + i);
        // Random grids, food lists and moves against the list-based oracle.
        Random rnd = new Random(353);
        String dirs = "UDLR";
        for (int round = 0; round < 3000; round++) {
            int w = 1 + rnd.nextInt(5), h = 1 + rnd.nextInt(5);
            List<Integer> cells = new ArrayList<>();
            for (int i = 0; i < w * h; i++) cells.add(i);
            Collections.shuffle(cells, rnd);
            int fc = rnd.nextInt(Math.min(8, w * h) + 1);
            int[][] food = new int[fc][];
            for (int i = 0; i < fc; i++) food[i] = new int[] {cells.get(i) / w, cells.get(i) % w};
            Snake a = new Snake(w, h, food);
            Oracle o = new Oracle(w, h, food);
            for (int op = 0; op < 40; op++) {
                char d = dirs.charAt(rnd.nextInt(4));
                if (a.move(d) != o.move(d)) throw new AssertionError("move mismatch");
                if (!a.consistent()) throw new AssertionError("occupancy set drift");
            }
        }
    }
}
```

#### Solution: [Boundary] Walking Robot Simulation II (LeetCode 2069)
<!-- id: sv-board-robot -->

**Approach.** The robot visits only the cells on the edge of the rectangle, and those cells form a loop of 2 * (width + height) - 4 cells. The solution stores one loop index, numbered from the start corner along the bottom edge, and one flag that records whether any step happened. A call to `step(num)` adds `num` modulo the cycle length to the index, and it sets the flag only when `num` is positive.

The position follows from the index by four ranges, one for each side. The direction follows from the same ranges: East on the bottom side, North on the right side, West on the top side and South on the left side. Index 0 is special. The robot faces East there before any step, and South once it has taken a step, because it arrives at the start corner by walking down the left side.

The invariant is that the loop index equals the total number of steps modulo the cycle length, so the position and the direction match a step-by-step simulation.

**Complexity.**

- **Time** per call is O(1), since the update is one addition and one remainder.
- **Space** is O(1), because the state is the index, the flag and the grid size.

```java run
import java.util.*;

public final class RobotSolution {
    static final class Robot {
        private final int w, h, cycle;
        private int index;
        private boolean moved;

        Robot(int width, int height) {
            this.w = width; this.h = height;
            this.cycle = 2 * (width + height) - 4;
        }

        /**
         * Advances the robot along the edge loop.
         * Time: O(1).
         * Space: O(1).
         * Invariant: index equals the step total modulo the cycle length.
         */
        void step(int num) {
            // Zero steps change nothing, including the moved flag.
            if (num == 0) return;
            moved = true;
            // The long sum prevents overflow for num near 10^9.
            index = (int) (((long) index + num) % cycle);
        }

        int[] getPos() {
            // Bottom side, indices 0 to w - 1.
            if (index < w) return new int[] {index, 0};
            // Right side, indices w to w + h - 2.
            if (index < w + h - 1) return new int[] {w - 1, index - (w - 1)};
            // Top side, indices w + h - 1 to 2w + h - 3.
            if (index < 2 * w + h - 2) return new int[] {w - 1 - (index - (w + h - 2)), h - 1};
            // Left side, the remaining indices.
            return new int[] {0, h - 1 - (index - (2 * w + h - 3))};
        }

        String getDir() {
            // The start corner has two directions, chosen by the moved flag.
            if (index == 0) return moved ? "South" : "East";
            if (index < w) return "East";
            if (index < w + h - 1) return "North";
            if (index < 2 * w + h - 2) return "West";
            return "South";
        }
    }

    /** Brute force: one cell at a time with the turn rule from the problem text. */
    static final class Oracle {
        final int w, h; int x, y, d;
        static final int[] DX = {1, 0, -1, 0}, DY = {0, 1, 0, -1};
        static final String[] NAME = {"East", "North", "West", "South"};
        Oracle(int w, int h) { this.w = w; this.h = h; }
        void step(int num) {
            for (int i = 0; i < num; i++) {
                int nx = x + DX[d], ny = y + DY[d];
                if (nx < 0 || ny < 0 || nx >= w || ny >= h) { d = (d + 1) % 4; nx = x + DX[d]; ny = y + DY[d]; }
                x = nx; y = ny;
            }
        }
    }

    public static void main(String[] args) {
        // Example 1 from the problem text.
        Robot r = new Robot(6, 3);
        r.step(2); r.step(2);
        if (!Arrays.equals(r.getPos(), new int[] {4, 0}) || !r.getDir().equals("East")) throw new AssertionError("example 1a");
        r.step(2); r.step(1); r.step(4);
        if (!Arrays.equals(r.getPos(), new int[] {1, 2}) || !r.getDir().equals("West")) throw new AssertionError("example 1b");
        // Example 2: the start corner before any step, after step(0) and after one full loop.
        r = new Robot(2, 2);
        if (!r.getDir().equals("East")) throw new AssertionError("example 2a");
        r.step(0);
        if (!r.getDir().equals("East")) throw new AssertionError("example 2b");
        r.step(4);
        if (!Arrays.equals(r.getPos(), new int[] {0, 0}) || !r.getDir().equals("South")) throw new AssertionError("example 2c");
        // A very large step count must match the loop arithmetic, checked by reducing to the cycle by hand.
        Robot big = new Robot(5, 4), small = new Robot(5, 4);
        big.step(1_000_000_000);
        small.step((int) (1_000_000_000L % 14));
        if (!Arrays.equals(big.getPos(), small.getPos()) || !big.getDir().equals(small.getDir())) throw new AssertionError("large step");
        // Random sizes and step sequences against the step-by-step oracle.
        Random rnd = new Random(2069);
        for (int round = 0; round < 3000; round++) {
            int w = 2 + rnd.nextInt(6), h = 2 + rnd.nextInt(6);
            Robot a = new Robot(w, h);
            Oracle o = new Oracle(w, h);
            for (int op = 0; op < 20; op++) {
                int num = rnd.nextInt(4) == 0 ? 0 : rnd.nextInt(3 * (w + h));
                a.step(num); o.step(num);
                int[] p = a.getPos();
                if (p[0] != o.x || p[1] != o.y) throw new AssertionError("position mismatch");
                if (!a.getDir().equals(Oracle.NAME[o.d])) throw new AssertionError("direction mismatch");
            }
        }
    }
}
```

#### Solution: [Recognize] Layered Counts In A Cube (LeetCode 3391)
<!-- id: sv-board-layers -->

**Approach.** A flat boolean array of n^3 cells is the authoritative matrix. A count array holds the number of ones in each layer, and it is derived from the matrix. An ordered set holds one key for each layer, built from the count and the layer index, so the last key names the layer with the most ones and, among equal counts, the largest index.

An update first reads the cell. A call whose request matches the stored value returns `false` and writes nothing. Otherwise it removes the layer's current key from the ordered set, changes the cell and the count, and inserts the new key. The remove must come first, because the key is derived from the count and a key that changes while it sits in the set breaks the ordering.

The invariant is that the ordered set holds exactly one key for each layer and that key matches the layer's current count.

**Complexity.**

- **Time** is O(log n) per update, because it does one removal and one insertion in a tree set of n keys, and `largestLayer` is O(log n) for reading the last key.
- **Space** is O(n^3) for the matrix plus O(n) for the counts and keys.

```java run
import java.util.*;

public final class LayersSolution {
    static final class Cube {
        private final int n;
        private final boolean[] cell;                              // authoritative matrix
        private final int[] ones;                                  // derived count per layer
        private final TreeSet<Long> ranking = new TreeSet<>();     // derived keys: count and layer index

        Cube(int n) {
            this.n = n;
            this.cell = new boolean[n * n * n];
            this.ones = new int[n];
            for (int x = 0; x < n; x++) ranking.add(key(0, x));
        }

        private static long key(int count, int x) { return ((long) count << 8) | x; }

        // Moves one layer to a new count; the old key leaves the set before the count changes.
        private void shift(int x, int delta) {
            ranking.remove(key(ones[x], x));
            ones[x] += delta;
            ranking.add(key(ones[x], x));
        }

        /**
         * Sets one cell to 1.
         * Time: O(log n).
         * Space: O(1).
         * Invariant: a repeated call returns before the index is touched.
         */
        boolean setCell(int x, int y, int z) {
            int i = (x * n + y) * n + z;
            // The value already matches, so nothing changes.
            if (cell[i]) return false;
            cell[i] = true;
            shift(x, 1);
            return true;
        }

        /** Sets one cell to 0 with the same checks; O(log n) time and O(1) space. */
        boolean unsetCell(int x, int y, int z) {
            int i = (x * n + y) * n + z;
            if (!cell[i]) return false;
            cell[i] = false;
            shift(x, -1);
            return true;
        }

        /** Reads the last key; O(log n) time; the largest key has the most ones and then the largest index. */
        int largestLayer() { return (int) (ranking.last() & 255); }

        boolean consistent() {
            int[] c = new int[n];
            for (int x = 0; x < n; x++) for (int k = 0; k < n * n; k++) if (cell[x * n * n + k]) c[x]++;
            TreeSet<Long> want = new TreeSet<>();
            for (int x = 0; x < n; x++) want.add(key(c[x], x));
            return Arrays.equals(c, ones) && want.equals(ranking);
        }
    }

    public static void main(String[] args) {
        // Example 1 from the problem text.
        Cube c = new Cube(3);
        if (c.largestLayer() != 2) throw new AssertionError("e1 0");
        if (!c.setCell(0, 0, 0) || c.largestLayer() != 0) throw new AssertionError("e1 1");
        if (c.setCell(0, 0, 0)) throw new AssertionError("e1 repeated set");
        if (!c.setCell(2, 1, 1) || c.largestLayer() != 2) throw new AssertionError("e1 tie");
        if (!c.unsetCell(2, 1, 1) || c.largestLayer() != 0) throw new AssertionError("e1 unset");
        if (c.unsetCell(0, 1, 1)) throw new AssertionError("e1 unset zero");
        // Example 2 from the problem text.
        c = new Cube(2);
        if (!c.setCell(1, 0, 0) || !c.setCell(1, 1, 1) || !c.setCell(0, 0, 0)) throw new AssertionError("e2 set");
        if (c.largestLayer() != 1) throw new AssertionError("e2 a");
        if (!c.unsetCell(1, 0, 0) || !c.unsetCell(1, 1, 1) || c.largestLayer() != 0) throw new AssertionError("e2 b");
        if (!c.unsetCell(0, 0, 0) || c.largestLayer() != 1) throw new AssertionError("e2 c");
        // Random updates against a scan of a plain 3D array.
        Random rnd = new Random(3391);
        for (int round = 0; round < 500; round++) {
            int n = 1 + rnd.nextInt(5);
            Cube s = new Cube(n);
            boolean[][][] g = new boolean[n][n][n];
            for (int op = 0; op < 60; op++) {
                int x = rnd.nextInt(n), y = rnd.nextInt(n), z = rnd.nextInt(n);
                int kind = rnd.nextInt(3);
                if (kind == 0) { boolean ch = !g[x][y][z]; g[x][y][z] = true; if (s.setCell(x, y, z) != ch) throw new AssertionError("set result"); }
                else if (kind == 1) { boolean ch = g[x][y][z]; g[x][y][z] = false; if (s.unsetCell(x, y, z) != ch) throw new AssertionError("unset result"); }
                int best = 0, bestCount = -1;
                for (int a = 0; a < n; a++) {
                    int cnt = 0;
                    for (int b = 0; b < n; b++) for (int d = 0; d < n; d++) if (g[a][b][d]) cnt++;
                    if (cnt >= bestCount) { bestCount = cnt; best = a; }
                }
                if (s.largestLayer() != best) throw new AssertionError("largest mismatch");
                if (!s.consistent()) throw new AssertionError("index drift");
            }
        }
    }
}
```
