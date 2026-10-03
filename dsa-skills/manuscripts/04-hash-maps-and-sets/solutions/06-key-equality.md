<!-- solutions-for: 06-key-equality -->
### Key Equality

#### Solution: [Build] Count Coordinates (Author exercise)
<!-- id: hm-count-coordinates -->

**Approach.** Wrap each observation in a `Point` record and count with `merge`. Records generate `equals` and `hashCode` from their components, so equal coordinates share one entry. After counting, loop over the values and count the entries that reached two or more. The assertions first show why the record is needed: a map keyed by arrays holds one entry per observation, and a hand-written class that overrides only `equals` loses the match because equal objects get different hash codes. Then the method is compared with a brute-force pair count on random observations.

**Complexity.** Expected O(n) time and O(k) extra space for `k` distinct coordinates.

```java run
import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Random;
import java.util.Set;

public final class CountCoordinates {
    record Point(int row, int col) {}

    static final class EqualsOnly {
        final int id, tag;
        EqualsOnly(int id, int tag) { this.id = id; this.tag = tag; }
        @Override public boolean equals(Object o) { return o instanceof EqualsOnly e && e.id == id; }
        @Override public int hashCode() { return tag; }          // breaks the contract: equal ids, different hashes
    }

    static int repeatedCoordinates(int[][] observations) {
        Map<Point, Integer> count = new HashMap<>();
        for (int[] o : observations) count.merge(new Point(o[0], o[1]), 1, Integer::sum);
        int repeated = 0;
        for (int c : count.values()) if (c >= 2) repeated++;
        return repeated;
    }
    static int oracle(int[][] observations) {
        boolean[] counted = new boolean[observations.length];
        int repeated = 0;
        for (int i = 0; i < observations.length; i++) {
            if (counted[i]) continue;
            int same = 0;
            for (int j = 0; j < observations.length; j++)
                if (observations[j][0] == observations[i][0] && observations[j][1] == observations[i][1]) { same++; counted[j] = true; }
            if (same >= 2) repeated++;
        }
        return repeated;
    }

    public static void main(String[] args) {
        int[][] a = {{1, 2}, {3, 4}, {1, 2}, {1, 2}, {3, 4}, {0, 0}};
        if (repeatedCoordinates(a) != 2) throw new AssertionError("example 1");
        if (repeatedCoordinates(new int[][] {{1, 2}, {2, 1}}) != 0) throw new AssertionError("example 2");
        if (!new Point(4, 7).equals(new Point(4, 7)) || new Point(4, 7).hashCode() != new Point(4, 7).hashCode()) throw new AssertionError("records compare by components");
        Map<int[], Integer> byArray = new HashMap<>();
        for (int[] o : a) byArray.merge(o, 1, Integer::sum);
        if (byArray.size() != a.length) throw new AssertionError("an array key never merges equal contents");
        Set<EqualsOnly> broken = new HashSet<>();
        broken.add(new EqualsOnly(1, 10));
        if (broken.contains(new EqualsOnly(1, 20))) throw new AssertionError("equal keys with different hashes are not found");
        if (!new EqualsOnly(1, 10).equals(new EqualsOnly(1, 20))) throw new AssertionError("the two keys are equal");
        Random rnd = new Random(91);
        for (int t = 0; t < 3000; t++) {
            int[][] x = new int[rnd.nextInt(14)][];
            for (int i = 0; i < x.length; i++) x[i] = new int[] {rnd.nextInt(3), rnd.nextInt(3)};
            if (repeatedCoordinates(x) != oracle(x)) throw new AssertionError("disagrees with the pair count");
        }
    }
}
```

#### Solution: [Vary] Undirected Edge Key (Author exercise)
<!-- id: hm-undirected-edge-key -->

**Approach.** Before inserting an edge, order its endpoints with the smaller first, so `(5, 4)` and `(4, 5)` become the same record. A loop `(3, 3)` is unchanged by the ordering and is its own key. The set size is the number of distinct edges. Without the normalisation, `[[1, 2], [2, 1]]` would count as two edges, and the assertions show that. The oracle compares every pair of edges for equality in either direction and counts the edges that have no equal predecessor, and the assertions agree on random edge lists.

**Complexity.** Expected O(n) time and O(k) extra space for `k` distinct edges.

```java run
import java.util.HashSet;
import java.util.Random;
import java.util.Set;

public final class UndirectedEdgeKey {
    record Pair(int from, int to) {}

    static int distinctUndirectedEdges(int[][] edges) {
        Set<Pair> seen = new HashSet<>();
        for (int[] e : edges) seen.add(new Pair(Math.min(e[0], e[1]), Math.max(e[0], e[1])));
        return seen.size();
    }
    static int unnormalised(int[][] edges) {
        Set<Pair> seen = new HashSet<>();
        for (int[] e : edges) seen.add(new Pair(e[0], e[1]));
        return seen.size();
    }
    static boolean sameEdge(int[] p, int[] q) {
        return (p[0] == q[0] && p[1] == q[1]) || (p[0] == q[1] && p[1] == q[0]);
    }
    static int oracle(int[][] edges) {
        int distinct = 0;
        for (int i = 0; i < edges.length; i++) {
            boolean earlier = false;
            for (int j = 0; j < i; j++) if (sameEdge(edges[i], edges[j])) { earlier = true; break; }
            if (!earlier) distinct++;
        }
        return distinct;
    }

    public static void main(String[] args) {
        if (distinctUndirectedEdges(new int[][] {{1, 2}, {2, 1}, {3, 3}, {2, 3}}) != 3) throw new AssertionError("example 1");
        if (distinctUndirectedEdges(new int[][] {{5, 4}, {4, 5}, {5, 4}}) != 1) throw new AssertionError("example 2");
        if (unnormalised(new int[][] {{1, 2}, {2, 1}}) != 2) throw new AssertionError("without normalising the two spellings differ");
        if (distinctUndirectedEdges(new int[][] {}) != 0) throw new AssertionError("no edges");
        Random rnd = new Random(92);
        for (int t = 0; t < 4000; t++) {
            int[][] x = new int[rnd.nextInt(12)][];
            for (int i = 0; i < x.length; i++) x[i] = new int[] {rnd.nextInt(4), rnd.nextInt(4)};
            if (distinctUndirectedEdges(x) != oracle(x)) throw new AssertionError("disagrees with the pair comparison");
        }
    }
}
```

#### Solution: [Boundary] Mutable-Key Failure (Author exercise)
<!-- id: hm-mutable-key-failure -->

**Approach.** The entry is filed in the bucket chosen by the hash code at insertion time, which is `start` for a class whose hash code is its field. After the field changes, a lookup computes the new hash code and searches the bucket for `changed`, which does not contain the entry, so `containsKey` reports false. Scanning `entrySet()` visits the stored nodes directly and still finds the entry, and `size()` still reports 1. Restoring the field makes the lookup succeed again. With `changed` equal to `start` nothing moves. The assertions check each of these statements on a plain map and compare the output with a calculation of the bucket for the small table.

**Complexity.** O(1) for the probe, and the map holds a single entry.

```java run
import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

public final class MutableKeyFailure {
    static final class Key {
        int x;
        Key(int x) { this.x = x; }
        @Override public boolean equals(Object o) { return o instanceof Key k && k.x == x; }
        @Override public int hashCode() { return x; }
    }

    static boolean[] probe(int start, int changed) {
        Map<Key, Integer> map = new HashMap<>();
        Key k = new Key(start);
        map.put(k, 1);
        k.x = changed;
        boolean found = map.containsKey(k);
        boolean scanned = false;
        for (Map.Entry<Key, Integer> e : map.entrySet()) if (e.getKey() == k) scanned = true;
        return new boolean[] {found, scanned};
    }

    public static void main(String[] args) {
        if (!Arrays.equals(probe(3, 8), new boolean[] {false, true})) throw new AssertionError("example 1");
        if (!Arrays.equals(probe(3, 3), new boolean[] {true, true})) throw new AssertionError("example 2");
        Map<Key, Integer> map = new HashMap<>();
        Key k = new Key(5);
        map.put(k, 1);
        k.x = 9;
        if (map.size() != 1) throw new AssertionError("the entry still counts toward the size");
        if (map.get(k) != null) throw new AssertionError("lookup by the changed key fails");
        if (map.containsKey(new Key(5))) throw new AssertionError("a fresh key with the old value is not equal to the stored key now");
        k.x = 5;
        if (map.get(k) == null || map.get(k) != 1) throw new AssertionError("restoring the field makes the entry reachable again");
        for (int s = 0; s < 16; s++)
            for (int c = 0; c < 16; c++)
                if (probe(s, c)[0] != (s == c)) throw new AssertionError("a changed hash code must hide the entry in a table of 16 buckets: " + s + " " + c);
    }
}
```

#### Solution: [Recognize] Count Directed Transitions (Author exercise)
<!-- id: hm-directed-transitions -->

**Approach.** Read consecutive pairs and use an immutable `Pair(from, to)` record as the key of a frequency map, keeping the fields in the order they were read so direction is part of the identity. `merge` returns the new count, which updates the running maximum. With the undirected normalisation from the previous exercise, `[4, 9, 4]` would give 2, and the assertions show the difference. The oracle counts, for each position, how many positions hold the same consecutive pair, and the assertions agree on random sequences.

**Complexity.** Expected O(n) time and O(k) extra space for `k` distinct transitions.

```java run
import java.util.HashMap;
import java.util.Map;
import java.util.Random;

public final class DirectedTransitions {
    record Pair(int from, int to) {}

    static int mostRepeatedTransition(int[] states) {
        Map<Pair, Integer> count = new HashMap<>();
        int best = 0;
        for (int i = 0; i + 1 < states.length; i++) {
            best = Math.max(best, count.merge(new Pair(states[i], states[i + 1]), 1, Integer::sum));
        }
        return best;
    }
    static int undirected(int[] states) {
        Map<Pair, Integer> count = new HashMap<>();
        int best = 0;
        for (int i = 0; i + 1 < states.length; i++) {
            int a = states[i], b = states[i + 1];
            best = Math.max(best, count.merge(new Pair(Math.min(a, b), Math.max(a, b)), 1, Integer::sum));
        }
        return best;
    }
    static int oracle(int[] states) {
        int best = 0;
        for (int i = 0; i + 1 < states.length; i++) {
            int same = 0;
            for (int j = 0; j + 1 < states.length; j++)
                if (states[j] == states[i] && states[j + 1] == states[i + 1]) same++;
            best = Math.max(best, same);
        }
        return best;
    }

    public static void main(String[] args) {
        if (mostRepeatedTransition(new int[] {1, 2, 1, 3, 1, 2}) != 2) throw new AssertionError("example 1");
        if (mostRepeatedTransition(new int[] {4, 9, 4}) != 1) throw new AssertionError("example 2");
        if (undirected(new int[] {4, 9, 4}) != 2) throw new AssertionError("normalising would merge the two directions");
        if (mostRepeatedTransition(new int[] {7}) != 0 || mostRepeatedTransition(new int[] {}) != 0) throw new AssertionError("no transitions");
        Random rnd = new Random(93);
        for (int t = 0; t < 4000; t++) {
            int[] x = new int[rnd.nextInt(14)];
            for (int i = 0; i < x.length; i++) x[i] = rnd.nextInt(3);
            if (mostRepeatedTransition(x) != oracle(x)) throw new AssertionError("disagrees with the position count");
        }
    }
}
```
