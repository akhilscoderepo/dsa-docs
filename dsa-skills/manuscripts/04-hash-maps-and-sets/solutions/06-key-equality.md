<!-- solutions-for: 04-hash-maps-and-sets -->
### Solutions For Record Keys

#### Solution: [Build] Count Coordinates (Author exercise)
<!-- id: hm-count-coordinates -->

**Approach.**
The key is `record Point(int row, int col)`, whose generated `equals` and `hashCode` use both components. Each order becomes a new `Point`, and `merge` raises the count of the equal stored point, so two orders at one cell reach one entry. The invariant is that after order `i`, `counts.get(p)` equals the number of orders among `0..i` at the cell `p`. The harness asserts the Java facts of the lesson. Two arrays with equal contents are different map keys. Two equal records are one key with equal hash codes. A `Map<int[], Integer>` produces a count of 1 for each order, which is the failure from the opening.

**Complexity.**
- **Time** is O(n) on average, because each order costs one record creation and one map operation.
- **Space** is O(d) for d distinct cells.

```java run
import java.util.*;

public final class CountCoordinates {
    record Point(int row, int col) {}

    /**
     * Returns the largest number of equal pairs in orders.
     * Time: O(n) expected. Space: O(d).
     * Invariant: after order i, counts.get(p) is the number of orders in 0..i at cell p.
     */
    static int busiestCell(int[][] orders) {
        Map<Point, Integer> counts = new HashMap<>();
        int best = 0;
        // One iteration per order.
        for (int[] order : orders) {
            // The record gives logical equality, so equal cells find one entry.
            int now = counts.merge(new Point(order[0], order[1]), 1, Integer::sum);
            best = Math.max(best, now);
        }
        return best;
    }

    /** The mistake: the key is the int[] itself. */
    static int busiestWithArrayKeys(int[][] orders) {
        Map<int[], Integer> counts = new HashMap<>();
        int best = 0;
        for (int[] order : orders) best = Math.max(best, counts.merge(order, 1, Integer::sum));
        return best;
    }

    public static void main(String[] args) {
        // The statement examples, the empty array and the lesson input.
        if (busiestCell(new int[][] {{4, 4}, {4, 5}, {5, 4}, {4, 4}}) != 2) throw new AssertionError("example 1");
        if (busiestCell(new int[][] {{0, 1}, {1, 0}}) != 1) throw new AssertionError("example 2");
        if (busiestCell(new int[0][]) != 0) throw new AssertionError("empty");
        if (busiestCell(new int[][] {{1, 2}, {0, 0}, {1, 2}, {2, 1}, {1, 2}}) != 3) throw new AssertionError("lesson input");
        // Java facts: arrays compare by identity, records by components.
        int[] a = {1, 2}, b = {1, 2};
        if (a.equals(b)) throw new AssertionError("array equals is identity");
        if (busiestWithArrayKeys(new int[][] {{1, 2}, {1, 2}, {1, 2}}) != 1) throw new AssertionError("array keys count 1");
        if (!new Point(1, 2).equals(new Point(1, 2))) throw new AssertionError("record equals");
        if (new Point(1, 2).hashCode() != new Point(1, 2).hashCode()) throw new AssertionError("record hash contract");
        Map<int[], Integer> m = new HashMap<>();
        m.put(a, 1);
        if (m.get(b) != null) throw new AssertionError("lookup by another array");
        // Random inputs are checked against the list-scan method from the lesson.
        Random rnd = new Random(59);
        for (int t = 0; t < 500; t++) {
            int[][] o = new int[rnd.nextInt(12)][];
            for (int k = 0; k < o.length; k++) o[k] = new int[] {rnd.nextInt(3) - 1, rnd.nextInt(3) - 1};
            int best = 0;
            for (int i = 0; i < o.length; i++) {
                int c = 0;
                for (int j = 0; j < o.length; j++) if (o[i][0] == o[j][0] && o[i][1] == o[j][1]) c++;
                best = Math.max(best, c);
            }
            if (busiestCell(o) != best) throw new AssertionError("trial " + t);
        }
    }
}
```

#### Solution: [Vary] Undirected Edge Key (Author exercise)
<!-- id: hm-undirected-edge -->

**Approach.**
The connection `(a, b)` equals `(b, a)`, so the key must not depend on the order of the two ends. Before each insertion the method puts the smaller node first, then adds the record `Edge(lo, hi)` to a set. The set size is the number of distinct connections. The invariant is that after edge `i`, the set holds one normalized key for each distinct connection among the first `i + 1` edges. A self-loop `(7, 7)` normalizes to itself.

**Complexity.**
- **Time** is O(n) on average, because each edge costs one comparison, one record and one set operation.
- **Space** is O(d) for d distinct connections.

```java run
import java.util.*;

public final class UndirectedEdgeKey {
    record Edge(int lo, int hi) {}

    /**
     * Counts distinct undirected connections.
     * Time: O(n) expected. Space: O(d).
     * Invariant: after edge i, seen holds one normalized Edge per distinct connection in edges[0..i].
     */
    static int distinctEdges(int[][] edges) {
        Set<Edge> seen = new HashSet<>();
        // One iteration per edge.
        for (int[] e : edges) {
            // The smaller node goes first, so (a, b) and (b, a) build the same key.
            seen.add(new Edge(Math.min(e[0], e[1]), Math.max(e[0], e[1])));
        }
        return seen.size();
    }

    public static void main(String[] args) {
        // The statement examples and the lesson input.
        if (distinctEdges(new int[][] {{1, 2}, {2, 1}, {2, 3}, {3, 2}, {1, 2}}) != 2) throw new AssertionError("example 1");
        if (distinctEdges(new int[][] {{7, 7}, {7, 7}}) != 1) throw new AssertionError("example 2");
        if (distinctEdges(new int[0][]) != 0) throw new AssertionError("empty");
        if (distinctEdges(new int[][] {{3, 1}, {1, 3}, {2, 5}, {5, 2}, {3, 1}}) != 2) throw new AssertionError("lesson input");
        // Without normalization the two directions would be two keys.
        Set<Edge> raw = new HashSet<>(List.of(new Edge(3, 1), new Edge(1, 3)));
        if (raw.size() != 2) throw new AssertionError("directions differ without normalization");
        // Extreme node values.
        if (distinctEdges(new int[][] {{1_000_000_000, -1_000_000_000}, {-1_000_000_000, 1_000_000_000}}) != 1) throw new AssertionError("extremes");
        // Random inputs are checked against a sorted-pair string oracle.
        Random rnd = new Random(60);
        for (int t = 0; t < 500; t++) {
            int[][] e = new int[rnd.nextInt(10)][];
            for (int k = 0; k < e.length; k++) e[k] = new int[] {rnd.nextInt(4), rnd.nextInt(4)};
            Set<String> oracle = new HashSet<>();
            for (int[] p : e) oracle.add(Math.min(p[0], p[1]) + "|" + Math.max(p[0], p[1]));
            if (distinctEdges(e) != oracle.size()) throw new AssertionError("trial " + t);
        }
    }
}
```

#### Solution: [Boundary] Mutable-Key Failure (Author exercise)
<!-- id: hm-mutable-key -->

**Approach.**
The walker edits one `int[2]` in place, so the set must never receive that array. An array compares by identity, so inserting the same array after each move leaves one entry. Inserting a clone gives one entry per move, since every clone is a different object. The correct method builds a fresh `Point(row, col)` from the current numbers after each move and inserts it. The record is immutable, so later moves cannot change a stored key. The invariant is that the set holds one immutable key for each distinct position occupied so far. The harness also shows the lesson's claim about a mutable class. On JDK 21, after a key field changes, the set no longer finds the key. The Javadoc of `Set` leaves this case unspecified, so the assertion reports what the JDK does and not a guarantee.

**Complexity.**
- **Time** is O(n) on average for n moves, because each move updates the array and makes one set operation.
- **Space** is O(d) for d distinct positions.

```java run
import java.util.*;

public final class MutableKeyFailure {
    record Point(int row, int col) {}

    /** A mutable key class with equality on both fields, used only to show the failure. */
    static final class Cell {
        int row, col;
        Cell(int row, int col) { this.row = row; this.col = col; }
        @Override public boolean equals(Object o) { return o instanceof Cell c && c.row == row && c.col == col; }
        @Override public int hashCode() { return 31 * row + col; }
    }

    /**
     * Counts distinct positions occupied, start included.
     * Time: O(n) expected. Space: O(d).
     * Invariant: seen holds one immutable key for each position occupied so far.
     */
    static int distinctPositions(String moves) {
        int[] pos = {0, 0};
        Set<Point> seen = new HashSet<>();
        seen.add(new Point(pos[0], pos[1]));
        // One iteration per move.
        for (int i = 0; i < moves.length(); i++) {
            char c = moves.charAt(i);
            if (c == 'U') pos[0]++;
            else if (c == 'D') pos[0]--;
            else if (c == 'R') pos[1]++;
            else pos[1]--;
            // A fresh record copies the numbers, so later edits of pos cannot reach the stored key.
            seen.add(new Point(pos[0], pos[1]));
        }
        return seen.size();
    }

    /** The mistake: the walker's own array goes into the set. */
    static int insertsTheArray(String moves) {
        int[] pos = {0, 0};
        Set<int[]> seen = new HashSet<>();
        seen.add(pos);
        for (int i = 0; i < moves.length(); i++) {
            char c = moves.charAt(i);
            if (c == 'U') pos[0]++; else if (c == 'D') pos[0]--; else if (c == 'R') pos[1]++; else pos[1]--;
            seen.add(pos);
        }
        return seen.size();
    }

    /** The second mistake: a clone is a new object, and arrays compare by identity. */
    static int insertsClones(String moves) {
        int[] pos = {0, 0};
        Set<int[]> seen = new HashSet<>();
        seen.add(pos.clone());
        for (int i = 0; i < moves.length(); i++) {
            char c = moves.charAt(i);
            if (c == 'U') pos[0]++; else if (c == 'D') pos[0]--; else if (c == 'R') pos[1]++; else pos[1]--;
            seen.add(pos.clone());
        }
        return seen.size();
    }

    public static void main(String[] args) {
        // The statement examples.
        if (distinctPositions("RULD") != 4) throw new AssertionError("example 1");
        if (distinctPositions("") != 1) throw new AssertionError("example 2");
        // The array mistakes: one entry, then one entry per move.
        if (insertsTheArray("RULD") != 1) throw new AssertionError("same array twice");
        if (insertsClones("RULD") != 5) throw new AssertionError("clones never match");
        // A mutable key stops being found after a field changes, on this JDK.
        Set<Cell> cells = new HashSet<>();
        Cell k = new Cell(1, 1);
        cells.add(k);
        if (!cells.contains(k)) throw new AssertionError("found before the change");
        k.row = 2;
        if (cells.contains(k) || cells.contains(new Cell(1, 1))) throw new AssertionError("entry should be lost on this JDK");
        if (cells.size() != 1) throw new AssertionError("the entry still occupies space");
        // Random move strings are checked against a visited-grid oracle.
        Random rnd = new Random(61);
        for (int t = 0; t < 500; t++) {
            StringBuilder sb = new StringBuilder();
            int len = rnd.nextInt(14);
            for (int j = 0; j < len; j++) sb.append("UDLR".charAt(rnd.nextInt(4)));
            boolean[][] grid = new boolean[41][41];
            int r = 20, c = 20, count = 1;
            grid[r][c] = true;
            for (char ch : sb.toString().toCharArray()) {
                if (ch == 'U') r++; else if (ch == 'D') r--; else if (ch == 'R') c++; else c--;
                if (!grid[r][c]) { grid[r][c] = true; count++; }
            }
            if (distinctPositions(sb.toString()) != count) throw new AssertionError(sb.toString());
        }
    }
}
```

#### Solution: [Recognize] Count Directed Transitions (Author exercise)
<!-- id: hm-directed-transitions -->

**Approach.**
A transition is an ordered pair of neighbors, so the key keeps its order and the record `Pair(from, to)` serves as the key. The loop reads each index `i` from 0 to `n - 2`, and `merge` counts the transition `(states[i], states[i + 1])`. The pair `(a, b)` and the pair `(b, a)` are different records, so they stay different entries, unlike the undirected edges of the previous exercise. The invariant is that after index `i`, each entry equals the occurrences of its transition among the first `i + 1` neighbor pairs.

**Complexity.**
- **Time** is O(n) on average, because each neighbor pair costs one record and one map operation.
- **Space** is O(d) for d distinct transitions.

```java run
import java.util.*;

public final class DirectedTransitions {
    record Pair(int from, int to) {}

    /**
     * Returns the largest count of one ordered transition between neighbors.
     * Time: O(n) expected. Space: O(d).
     * Invariant: after index i, counts.get(p) is the number of neighbor pairs among the first i + 1 equal to p.
     */
    static int busiestTransition(int[] states) {
        Map<Pair, Integer> counts = new HashMap<>();
        int best = 0;
        // The loop stops one before the end, because each pair needs a right neighbor.
        for (int i = 0; i + 1 < states.length; i++) {
            // The order of the record fields keeps (a, b) apart from (b, a).
            best = Math.max(best, counts.merge(new Pair(states[i], states[i + 1]), 1, Integer::sum));
        }
        return best;
    }

    public static void main(String[] args) {
        // The statement examples and the empty array.
        if (busiestTransition(new int[] {1, 2, 1, 2, 2, 1}) != 2) throw new AssertionError("example 1");
        if (busiestTransition(new int[] {5}) != 0) throw new AssertionError("example 2");
        if (busiestTransition(new int[0]) != 0) throw new AssertionError("empty");
        // Opposite directions stay separate: the pair (1, 2) occurs once and the pair (2, 1) occurs once.
        if (busiestTransition(new int[] {1, 2, 1}) != 1) throw new AssertionError("directions are separate");
        // Random arrays are checked against a quadratic oracle.
        Random rnd = new Random(62);
        for (int t = 0; t < 600; t++) {
            int[] s = new int[rnd.nextInt(10)];
            for (int k = 0; k < s.length; k++) s[k] = rnd.nextInt(3);
            int expect = 0;
            for (int i = 0; i + 1 < s.length; i++) {
                int c = 0;
                for (int j = 0; j + 1 < s.length; j++) if (s[i] == s[j] && s[i + 1] == s[j + 1]) c++;
                expect = Math.max(expect, c);
            }
            if (busiestTransition(s) != expect) throw new AssertionError(Arrays.toString(s));
        }
    }
}
```
