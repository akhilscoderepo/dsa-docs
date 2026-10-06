<!-- solutions-for: 22-bfs-variations -->
### Solutions For Generated States

#### Solution: [Build] Combination-Lock States (Author exercise)
<!-- id: bv4-lock-neighbors -->

**Approach.**
The method copies the code into a `char[]` and visits the wheels from left to right. For each wheel it writes the digit one higher, modulo 10, and records the new string. It then writes the digit one lower, which it computes as the digit plus 9 modulo 10 so that the remainder never goes negative, and records that string. After both turns it restores the original digit, so the next wheel starts from the unchanged code.

The invariant is that at the start of each wheel iteration the array equals the input code. Each wheel contributes exactly two strings, and the two differ because 1 and 9 are different modulo 10. The result therefore holds `2 * w` strings, and no two are equal. The harness also asserts the Java fact that `%` on a negative int is negative, which is why the method uses `+ 9`.

**Complexity.**
- **Time** is O(w^2), because each of the `2w` results is a new string of length `w`.
- **Space** is O(w^2) for the result list, plus O(w) for the working array.

```java run
import java.util.*;

public final class LockNeighbors {
    /**
     * Returns every code one turn away, wheel by wheel, up before down.
     * Time: O(w^2). Space: O(w^2).
     * Invariant: before each wheel is handled, the array equals the input code.
     */
    static List<String> neighbors(String code) {
        // The result holds exactly 2 * w strings.
        List<String> result = new ArrayList<>();
        // A copy lets each wheel change without touching the input string.
        char[] digits = code.toCharArray();
        // Each wheel is handled once, so the loop runs w times.
        for (int wheel = 0; wheel < digits.length; wheel++) {
            // Remember the digit so it can be restored after both turns.
            char original = digits[wheel];
            // Turn up: 9 wraps to 0 through the remainder.
            digits[wheel] = (char) ('0' + (original - '0' + 1) % 10);
            result.add(new String(digits));
            // Turn down: adding 9 avoids a negative remainder at digit 0.
            digits[wheel] = (char) ('0' + (original - '0' + 9) % 10);
            result.add(new String(digits));
            // Restore the digit so the next wheel starts from the input code.
            digits[wheel] = original;
        }
        // The caller receives a list that never aliases the working array.
        return result;
    }

    /** Brute force: scan all codes of the same length and keep those that differ from the input by one cyclic step in one wheel. */
    static Set<String> oracle(String code) {
        int w = code.length();
        int total = 1;
        for (int i = 0; i < w; i++) total *= 10;
        Set<String> out = new HashSet<>();
        for (int v = 0; v < total; v++) {
            String s = String.format("%0" + w + "d", v);
            int diff = 0;
            boolean ok = true;
            for (int i = 0; i < w; i++) {
                int d = (s.charAt(i) - code.charAt(i) + 10) % 10;
                if (d != 0) { diff++; if (d != 1 && d != 9) ok = false; }
            }
            if (diff == 1 && ok) out.add(s);
        }
        return out;
    }

    public static void main(String[] args) {
        // The two examples of the exercise, including the order of the results.
        if (!neighbors("1209").equals(List.of("2209", "0209", "1309", "1109", "1219", "1299", "1200", "1208"))) throw new AssertionError("ex1");
        if (!neighbors("9").equals(List.of("0", "8"))) throw new AssertionError("ex2");
        // Java fact: % on a negative int is negative, so the down turn needs + 9.
        if (-1 % 10 != -1) throw new AssertionError("negative remainder");
        // Java fact: a char[] has identity equality, so two arrays with equal digits are different set entries.
        Set<char[]> arrays = new HashSet<>();
        arrays.add("12".toCharArray());
        if (arrays.contains("12".toCharArray())) throw new AssertionError("array identity");
        // Random codes must match the brute force as sets, with the correct size and no duplicates.
        Random rnd = new Random(2204);
        for (int t = 0; t < 400; t++) {
            int w = 1 + rnd.nextInt(4);
            StringBuilder sb = new StringBuilder();
            for (int i = 0; i < w; i++) sb.append(rnd.nextInt(10));
            String code = sb.toString();
            List<String> got = neighbors(code);
            if (got.size() != 2 * w || new HashSet<>(got).size() != 2 * w) throw new AssertionError("size " + code);
            if (!new HashSet<>(got).equals(oracle(code))) throw new AssertionError("random " + code);
        }
    }
}
```

#### Solution: [Vary] Open The Lock (LeetCode 752)
<!-- id: bv4-open-the-lock -->

**Approach.**
The method treats a four-digit string as a state and generates its eight neighbors on demand. It puts the dead codes into the `seen` set first, so one `add` call tests a code for both reasons. If adding `"0000"` fails, the start is dead and the result is -1. The search then processes the queue one full pass at a time. The counter `turns` grows after each pass, so every code in a pass shares the same turn count.

The invariant is that every code in `seen` is either dead or was generated at its smallest possible turn count, and the queue holds the codes of one pass followed by the next. The first time a code is taken from the queue equal to the target, `turns` is minimal. When the queue empties, no allowed code leads to the target, so the method returns -1. The dead set also blocks the target, which gives -1 when the target is dead.

**Complexity.**
- **Time** is O(R * w), because each reachable code is generated once and costs `w` work per neighbor string.
- **Space** is O(R * w) for the set and the queue, bounded by 10,000 codes of four digits.

```java run
import java.util.*;

public final class OpenTheLock {
    /**
     * Returns the fewest turns from "0000" to target that avoid every dead code, or -1.
     * Time: O(R * w). Space: O(R * w).
     * Invariant: each code in seen is dead or was first generated at its smallest turn count.
     */
    static int openLock(String[] deadends, String target) {
        // Dead codes start in the seen set, so they are never enqueued.
        Set<String> seen = new HashSet<>(Arrays.asList(deadends));
        ArrayDeque<String> queue = new ArrayDeque<>();
        // add returns false when the start is dead.
        if (!seen.add("0000")) return -1;
        queue.add("0000");
        // Each pass over the queue is one more turn.
        for (int turns = 0; !queue.isEmpty(); turns++) {
            // The pass length is fixed before the loop, so new codes wait for the next pass.
            for (int count = queue.size(); count > 0; count--) {
                String current = queue.poll();
                // The first dequeue of the target happens at the minimum turn count.
                if (current.equals(target)) return turns;
                // Each neighbor is generated from the rule, not read from a stored graph.
                for (String next : neighbors(current)) {
                    // add tests and marks in one call, so each code is enqueued once.
                    if (seen.add(next)) queue.add(next);
                }
            }
        }
        // The queue emptied without reaching the target.
        return -1;
    }

    /** Generates the eight one-turn codes of a code. */
    static List<String> neighbors(String code) {
        List<String> result = new ArrayList<>();
        char[] digits = code.toCharArray();
        for (int wheel = 0; wheel < digits.length; wheel++) {
            char original = digits[wheel];
            digits[wheel] = (char) ('0' + (original - '0' + 1) % 10);
            result.add(new String(digits));
            digits[wheel] = (char) ('0' + (original - '0' + 9) % 10);
            result.add(new String(digits));
            digits[wheel] = original;
        }
        return result;
    }

    /** Brute force: relax distances over all codes until nothing changes, using no queue. */
    static int oracle(String[] deadends, String target, int w) {
        int total = 1;
        for (int i = 0; i < w; i++) total *= 10;
        Set<String> dead = new HashSet<>(Arrays.asList(deadends));
        int inf = Integer.MAX_VALUE / 2;
        int[] dist = new int[total];
        Arrays.fill(dist, inf);
        String zero = "0".repeat(w);
        if (dead.contains(zero)) return -1;
        dist[0] = 0;
        boolean changed = true;
        while (changed) {
            changed = false;
            for (int v = 0; v < total; v++) {
                if (dist[v] >= inf) continue;
                for (String n : neighbors(String.format("%0" + w + "d", v))) {
                    if (dead.contains(n)) continue;
                    int id = Integer.parseInt(n);
                    if (dist[v] + 1 < dist[id]) { dist[id] = dist[v] + 1; changed = true; }
                }
            }
        }
        int d = dist[Integer.parseInt(target)];
        return dead.contains(target) || d >= inf ? -1 : d;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (openLock(new String[] {"0010", "0001", "1100"}, "0021") != 5) throw new AssertionError("ex1");
        String[] ring = {"1000", "9000", "0100", "0900", "0010", "0090", "0001", "0009"};
        if (openLock(ring, "5555") != -1) throw new AssertionError("ex2");
        // Boundary cases: dead start, dead target, and target equal to the start.
        if (openLock(new String[] {"0000"}, "0001") != -1) throw new AssertionError("dead start");
        if (openLock(new String[] {"0001"}, "0001") != -1) throw new AssertionError("dead target");
        if (openLock(new String[0], "0000") != 0) throw new AssertionError("start is target");
        // Wrap-around makes 9000 one turn away from the start.
        if (openLock(new String[0], "9000") != 1) throw new AssertionError("wrap");
        // Random three-wheel locks must match the relaxation oracle; the method works for any length through the start string.
        Random rnd = new Random(2205);
        for (int t = 0; t < 150; t++) {
            int w = 3;
            int k = rnd.nextInt(120);
            String[] dead = new String[k];
            for (int i = 0; i < k; i++) dead[i] = String.format("%03d", rnd.nextInt(1000));
            String target = String.format("%03d", rnd.nextInt(1000));
            if (openLock3(dead, target) != oracle(dead, target, w)) throw new AssertionError("random " + t);
        }
    }

    /** Runs the same search for three wheels by padding to the generic start code. */
    static int openLock3(String[] deadends, String target) {
        Set<String> seen = new HashSet<>(Arrays.asList(deadends));
        ArrayDeque<String> queue = new ArrayDeque<>();
        if (!seen.add("000")) return -1;
        queue.add("000");
        for (int turns = 0; !queue.isEmpty(); turns++) {
            for (int count = queue.size(); count > 0; count--) {
                String current = queue.poll();
                if (current.equals(target)) return turns;
                for (String next : neighbors(current)) if (seen.add(next)) queue.add(next);
            }
        }
        return -1;
    }
}
```

#### Solution: [Boundary] Forbidden Start And Target (Author exercise)
<!-- id: bv4-forbidden-endpoints -->

**Approach.**
The method stores a code as an `int`, so a `boolean[]` of size 10^w replaces the hash set. It first marks every forbidden code in that array. Then it rejects the two endpoints before any search: a forbidden `start` or a forbidden `target` returns -1, and only after both checks does equal `start` and `target` return 0. This order makes the contract explicit, and the equality shortcut never skips a forbidden code.

The search keeps the distance in an `int[]`. It takes a code from the queue, reads each wheel digit with division and remainder by a power of ten, and builds the two neighbors by arithmetic. A neighbor that is marked is skipped. Otherwise it is marked, gets distance plus one and joins the queue. The invariant is that a marked code is forbidden or has its final distance. The method returns the distance of `target` when it is discovered, and -1 if the queue empties.

**Complexity.**
- **Time** is O(10^w * w) in the worst case, because each code is processed once and has `2w` neighbors.
- **Space** is O(10^w) for the marks, the distances and the queue.

```java run
import java.util.*;

public final class ForbiddenEndpoints {
    /**
     * Returns the fewest turns from start to target avoiding forbidden codes, or -1.
     * Time: O(10^w * w). Space: O(10^w).
     * Invariant: a marked code is forbidden or already holds its final distance.
     */
    static int minTurns(String start, String target, String[] forbidden) {
        // The number of wheels fixes the size of the code space.
        int w = start.length();
        int space = 1;
        for (int i = 0; i < w; i++) space *= 10;
        // Forbidden codes are marked before any search, as if they were visited.
        boolean[] marked = new boolean[space];
        for (String f : forbidden) marked[Integer.parseInt(f)] = true;
        int s = Integer.parseInt(start);
        int t = Integer.parseInt(target);
        // A forbidden endpoint decides the answer before equality is considered.
        if (marked[s] || marked[t]) return -1;
        // Equal and allowed endpoints need no turn.
        if (s == t) return 0;
        // Distance array and queue hold only the codes that the search generates.
        int[] dist = new int[space];
        Arrays.fill(dist, -1);
        ArrayDeque<Integer> queue = new ArrayDeque<>();
        marked[s] = true;
        dist[s] = 0;
        queue.add(s);
        // Each code is taken from the queue at most once.
        while (!queue.isEmpty()) {
            int current = queue.poll();
            // Power is the place value of the wheel, so division reads that digit.
            for (int power = 1; power < space; power *= 10) {
                int digit = current / power % 10;
                int base = current - digit * power;
                // Two neighbors per wheel: one digit up and one digit down, both with wrap-around.
                for (int step : new int[] {1, 9}) {
                    int next = base + (digit + step) % 10 * power;
                    // A marked code is forbidden or already discovered.
                    if (marked[next]) continue;
                    marked[next] = true;
                    dist[next] = dist[current] + 1;
                    // The first discovery of the target is its minimum distance.
                    if (next == t) return dist[next];
                    queue.add(next);
                }
            }
        }
        // The target is cut off by forbidden codes.
        return -1;
    }

    /** Brute force: repeat relaxation over every code and both neighbors until stable. */
    static int oracle(String start, String target, String[] forbidden) {
        int w = start.length();
        int space = 1;
        for (int i = 0; i < w; i++) space *= 10;
        Set<Integer> bad = new HashSet<>();
        for (String f : forbidden) bad.add(Integer.parseInt(f));
        int s = Integer.parseInt(start), t = Integer.parseInt(target);
        if (bad.contains(s) || bad.contains(t)) return -1;
        int inf = 1 << 28;
        int[] d = new int[space];
        Arrays.fill(d, inf);
        d[s] = 0;
        for (boolean ch = true; ch; ) {
            ch = false;
            for (int v = 0; v < space; v++) {
                if (d[v] >= inf) continue;
                for (int u = 0; u < space; u++) {
                    if (bad.contains(u) || d[u] <= d[v] + 1) continue;
                    // u is one turn from v when exactly one wheel differs by one cyclic step.
                    int diff = 0; boolean ok = true; int a = v, b = u;
                    for (int i = 0; i < w; i++, a /= 10, b /= 10) {
                        int x = (b % 10 - a % 10 + 10) % 10;
                        if (x != 0) { diff++; if (x != 1 && x != 9) ok = false; }
                    }
                    if (diff == 1 && ok) { d[u] = d[v] + 1; ch = true; }
                }
            }
        }
        return d[t] >= inf ? -1 : d[t];
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (minTurns("5", "5", new String[] {"5"}) != -1) throw new AssertionError("ex1");
        if (minTurns("3", "3", new String[] {"2", "4"}) != 0) throw new AssertionError("ex2");
        // A single wheel blocked on both sides cannot be left.
        if (minTurns("0", "5", new String[] {"1", "9"}) != -1) throw new AssertionError("ring");
        // Forbidden target with a different start.
        if (minTurns("0", "5", new String[] {"5"}) != -1) throw new AssertionError("target forbidden");
        // Java fact: a code with leading zeros parses to a smaller int, so the string "007" and the int 7 name the same code.
        if (Integer.parseInt("007") != 7) throw new AssertionError("leading zeros");
        // Random locks with one to three wheels must match the oracle.
        Random rnd = new Random(2206);
        for (int t = 0; t < 300; t++) {
            int w = 1 + rnd.nextInt(3);
            int space = (int) Math.pow(10, w);
            String fmt = "%0" + w + "d";
            String start = String.format(fmt, rnd.nextInt(space));
            String target = String.format(fmt, rnd.nextInt(space));
            int k = rnd.nextInt(Math.max(1, space / 2));
            String[] forb = new String[k];
            for (int i = 0; i < k; i++) forb[i] = String.format(fmt, rnd.nextInt(space));
            if (minTurns(start, target, forb) != oracle(start, target, forb)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Recognize] Shortest Path in Binary Matrix (LeetCode 1091)
<!-- id: bv4-shortest-path-binary-matrix -->

**Approach.**
The state is the coordinate pair, packed as `row * n + col` in one `int`. No other fact changes the legal moves, because every free cell allows the same eight steps, so the pair is a complete encoding. The method returns -1 when either endpoint is blocked. It then marks the start, counts it as one cell and runs a pass-by-pass search, where each pass adds one cell to the path length.

For each cell taken from the queue, the method tries the eight offsets and skips offsets outside the grid, blocked cells and cells already marked. The method records marks in a separate `boolean` array, so the input grid stays unchanged. The invariant is that each marked cell was reached by a path of the smallest possible cell count, which equals the pass number. The method returns the pass count when it takes the cell `(n-1,n-1)` from the queue and returns -1 when the queue empties.

**Complexity.**
- **Time** is O(n^2), because each cell enters the queue once and tries eight offsets.
- **Space** is O(n^2) for the copy of the grid and the queue.

```java run
import java.util.*;

public final class BinaryMatrixPath {
    /**
     * Returns the cell count of the shortest eight-direction clear path, or -1.
     * Time: O(n^2). Space: O(n^2).
     * Invariant: a marked cell was reached by a path with the smallest possible cell count.
     */
    static int shortestPathBinaryMatrix(int[][] grid) {
        int n = grid.length;
        // Blocked endpoints leave no clear path.
        if (grid[0][0] == 1 || grid[n - 1][n - 1] == 1) return -1;
        // A separate mark array keeps the caller's grid unchanged.
        boolean[] marked = new boolean[n * n];
        ArrayDeque<Integer> queue = new ArrayDeque<>();
        marked[0] = true;
        queue.add(0);
        // length counts the cells on the path to every cell in the current pass.
        for (int length = 1; !queue.isEmpty(); length++) {
            // The pass size is fixed first, so new cells wait for the next pass.
            for (int count = queue.size(); count > 0; count--) {
                int packed = queue.poll();
                int row = packed / n, col = packed % n;
                // The first dequeue of the goal happens at the minimum length.
                if (row == n - 1 && col == n - 1) return length;
                // Eight offsets generate the neighbors of the coordinate state.
                for (int dr = -1; dr <= 1; dr++) {
                    for (int dc = -1; dc <= 1; dc++) {
                        int r = row + dr, c = col + dc;
                        // Skip cells outside the grid.
                        if (r < 0 || r >= n || c < 0 || c >= n) continue;
                        // Skip blocked cells and cells that were generated before.
                        if (grid[r][c] == 1 || marked[r * n + c]) continue;
                        marked[r * n + c] = true;
                        queue.add(r * n + c);
                    }
                }
            }
        }
        // The queue emptied before the goal was reached.
        return -1;
    }

    /** Brute force: repeated relaxation of path lengths over all cells until stable. */
    static int oracle(int[][] grid) {
        int n = grid.length;
        if (grid[0][0] == 1 || grid[n - 1][n - 1] == 1) return -1;
        int inf = 1 << 28;
        int[][] d = new int[n][n];
        for (int[] row : d) Arrays.fill(row, inf);
        d[0][0] = 1;
        for (boolean ch = true; ch; ) {
            ch = false;
            for (int r = 0; r < n; r++) for (int c = 0; c < n; c++) {
                if (grid[r][c] == 1) continue;
                for (int a = -1; a <= 1; a++) for (int b = -1; b <= 1; b++) {
                    int x = r + a, y = c + b;
                    if (x < 0 || y < 0 || x >= n || y >= n || grid[x][y] == 1) continue;
                    if (d[x][y] + 1 < d[r][c]) { d[r][c] = d[x][y] + 1; ch = true; }
                }
            }
        }
        return d[n - 1][n - 1] >= inf ? -1 : d[n - 1][n - 1];
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (shortestPathBinaryMatrix(new int[][] {{0, 0, 1, 0}, {1, 0, 1, 0}, {1, 1, 0, 0}, {0, 0, 1, 0}}) != 4) throw new AssertionError("ex1");
        if (shortestPathBinaryMatrix(new int[][] {{1, 0}, {0, 0}}) != -1) throw new AssertionError("ex2");
        // A single free cell has a path of one cell, and a single blocked cell has none.
        if (shortestPathBinaryMatrix(new int[][] {{0}}) != 1) throw new AssertionError("single free");
        if (shortestPathBinaryMatrix(new int[][] {{1}}) != -1) throw new AssertionError("single blocked");
        // Diagonal moves allow a two-cell path across a checkerboard corner.
        if (shortestPathBinaryMatrix(new int[][] {{0, 1}, {1, 0}}) != 2) throw new AssertionError("diagonal");
        // The input grid is not modified.
        int[][] keep = {{0, 0}, {0, 0}};
        shortestPathBinaryMatrix(keep);
        if (!Arrays.deepEquals(keep, new int[][] {{0, 0}, {0, 0}})) throw new AssertionError("mutation");
        // Random grids from one to six cells wide must match the oracle.
        Random rnd = new Random(2208);
        for (int t = 0; t < 500; t++) {
            int n = 1 + rnd.nextInt(6);
            int[][] g = new int[n][n];
            for (int[] row : g) for (int c = 0; c < n; c++) row[c] = rnd.nextInt(3) == 0 ? 1 : 0;
            if (shortestPathBinaryMatrix(g) != oracle(g)) throw new AssertionError("random " + t);
        }
    }
}
```
