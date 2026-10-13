<!-- solutions-for: 03-ordered-maps-and-sets -->
### Solutions For Ordered Maps And Sets

#### Solution: [Build] Floor And Ceiling (Author exercise)
<!-- id: ord-floor-ceiling -->

**Approach.** The program loads the keys into a `TreeSet` and answers each query with two navigation calls.

The call `floor(q)` returns the greatest key at most `q`, and `ceiling(q)` returns the smallest key at least `q`. Each call descends one root-to-leaf path and remembers the last key that qualified. The invariant is that the remembered key is the best qualifying key among all nodes passed so far, and the subtree not entered cannot hold a better one. Both calls return `null` when no key qualifies, and the program maps `null` to -1 before it writes the pair. For keys `10, 20, 30, 40` and query 5, `floor` finds nothing and `ceiling` returns 10. The harness also checks the strict calls `lower` and `higher`, the empty-set behavior of `first`, and the live behavior of `headSet`.

**Complexity.**

- **Time** is O((n + q) log n), because each of the `n` insertions and `2q` navigation calls follows one path of height O(log n).
- **Space** is O(n), for the nodes of the tree.

```java run
import java.util.NoSuchElementException;
import java.util.Random;
import java.util.TreeSet;

public final class FloorCeilingCheck {
    /**
     * Returns one (floor, ceiling) pair per query, with -1 for a missing neighbor.
     * Time: O((n + q) log n), one tree path per insertion and per navigation call.
     * Space: O(n), one node per key.
     * Invariant: the remembered candidate is the best qualifying key on the path walked so far.
     */
    static int[][] nearest(int[] keys, int[] queries) {
        // The tree keeps keys ordered under natural integer order.
        TreeSet<Integer> set = new TreeSet<>();
        // Each insertion descends one path and relinks a few nodes.
        for (int k : keys) set.add(k);
        // One output pair per query.
        int[][] out = new int[queries.length][2];
        // Each query costs two descents.
        for (int i = 0; i < queries.length; i++) {
            // floor returns the greatest key <= q, or null when none exists.
            Integer f = set.floor(queries[i]);
            // ceiling returns the smallest key >= q, or null when none exists.
            Integer c = set.ceiling(queries[i]);
            // The null result is mapped to the sentinel -1 required by the problem.
            out[i][0] = f == null ? -1 : f;
            out[i][1] = c == null ? -1 : c;
        }
        // The pairs follow the query order.
        return out;
    }

    /** Linear-scan oracle with the same contract. */
    static int[][] brute(int[] keys, int[] queries) {
        // One pair per query.
        int[][] out = new int[queries.length][2];
        // Scan all keys for every query.
        for (int i = 0; i < queries.length; i++) {
            int f = -1, c = -1;
            for (int k : keys) {
                // A key at most q competes for the floor.
                if (k <= queries[i] && k > f) f = k;
                // A key at least q competes for the ceiling.
                if (k >= queries[i] && (c == -1 || k < c)) c = k;
            }
            out[i][0] = f;
            out[i][1] = c;
        }
        return out;
    }

    public static void main(String[] args) {
        // Checks Example 1 and Example 2.
        int[][] e1 = nearest(new int[]{10, 20, 30, 40}, new int[]{25, 20, 5, 45});
        int[][] w1 = {{20, 30}, {20, 20}, {-1, 10}, {40, -1}};
        if (!java.util.Arrays.deepEquals(e1, w1)) throw new AssertionError("example 1");
        int[][] e2 = nearest(new int[]{7}, new int[]{7, 8});
        if (!java.util.Arrays.deepEquals(e2, new int[][]{{7, 7}, {7, -1}})) throw new AssertionError("example 2");
        // Checks the Java claims: strict versus non-strict calls and null for a missing neighbor.
        TreeSet<Integer> s = new TreeSet<>(java.util.List.of(10, 20, 30));
        if (s.floor(20) != 20 || s.lower(20) != 10) throw new AssertionError("floor/lower");
        if (s.ceiling(20) != 20 || s.higher(20) != 30) throw new AssertionError("ceiling/higher");
        if (s.floor(5) != null || s.higher(30) != null) throw new AssertionError("null neighbor");
        if (s.first() != 10 || s.last() != 30) throw new AssertionError("first/last");
        // Checks that first() throws on an empty set while pollFirst() returns null.
        TreeSet<Integer> empty = new TreeSet<>();
        boolean threw = false;
        try { empty.first(); } catch (NoSuchElementException ex) { threw = true; }
        if (!threw || empty.pollFirst() != null) throw new AssertionError("empty set");
        // Checks that a null element is rejected by natural ordering.
        threw = false;
        try { empty.add(null); } catch (NullPointerException ex) { threw = true; }
        if (!threw) throw new AssertionError("null element");
        // Checks that headSet is a live view and rejects an out-of-range add.
        java.util.SortedSet<Integer> head = s.headSet(25);
        s.add(15);
        if (!head.contains(15) || head.size() != 3) throw new AssertionError("live view");
        threw = false;
        try { head.add(99); } catch (IllegalArgumentException ex) { threw = true; }
        if (!threw) throw new AssertionError("view range");
        // Checks the descending view order.
        if (!s.descendingSet().first().equals(30)) throw new AssertionError("descending");
        // Checks random inputs against the linear-scan oracle.
        Random rnd = new Random(3203);
        for (int round = 0; round < 400; round++) {
            int n = rnd.nextInt(15);
            java.util.LinkedHashSet<Integer> distinct = new java.util.LinkedHashSet<>();
            for (int i = 0; i < n; i++) distinct.add(rnd.nextInt(40));
            int[] keys = distinct.stream().mapToInt(Integer::intValue).toArray();
            int[] qs = new int[10];
            for (int i = 0; i < qs.length; i++) qs[i] = rnd.nextInt(45);
            if (!java.util.Arrays.deepEquals(nearest(keys, qs), brute(keys, qs))) throw new AssertionError("round " + round);
        }
    }
}
```

#### Solution: [Vary] Ordered Frequency Map (Author exercise)
<!-- id: ord-frequency-map -->

**Approach.** A `TreeMap` from value to count keeps the values in order while the counts change.

An add operation calls `merge`, which creates the entry or raises its count with one search. A remove operation looks up the count. When the count is 1, the program deletes the entry, and otherwise it stores the count minus one. The invariant is that every key in the map has a count of at least 1. Deleting at count 0 is necessary, because a key that stays with count 0 would still appear in iteration and in `firstKey`. The harness shows that effect with a `put(k, 0)`. Iterating the map yields the pairs in increasing key order with no extra sort.

**Complexity.**

- **Time** is O(m log d) for `m` operations and `d` distinct values, since each operation does one or two tree searches, and the final iteration costs O(d).
- **Space** is O(d), one entry per distinct value with a positive count.

```java run
import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;
import java.util.NoSuchElementException;
import java.util.Random;
import java.util.TreeMap;

public final class FrequencyMapCheck {
    /**
     * Applies add and remove operations and returns (value, count) pairs in increasing value order.
     * Time: O(m log d) for m operations and d distinct values, plus O(d) to read the result.
     * Space: O(d), one entry per value with a positive count.
     * Invariant: every key stored in the map has a count of at least 1.
     */
    static int[][] apply(int[][] ops) {
        // The tree orders values and holds one count per value.
        TreeMap<Integer, Integer> counts = new TreeMap<>();
        // One iteration per operation.
        for (int[] op : ops) {
            if (op[0] == 1) {
                // Add: create the entry with 1 or raise the count, using one search.
                counts.merge(op[1], 1, Integer::sum);
            } else {
                // Remove: read the current count with one search.
                Integer c = counts.get(op[1]);
                // An absent value is ignored.
                if (c == null) continue;
                // A count of 1 would become 0, so the entry is deleted to keep the invariant.
                if (c == 1) counts.remove(op[1]);
                // Otherwise the count drops by one.
                else counts.put(op[1], c - 1);
            }
        }
        // Iteration in key order produces the pairs without sorting.
        int[][] out = new int[counts.size()][2];
        int i = 0;
        for (Map.Entry<Integer, Integer> e : counts.entrySet()) {
            // Each entry becomes one (value, count) pair.
            out[i][0] = e.getKey();
            out[i][1] = e.getValue();
            i++;
        }
        return out;
    }

    /** Oracle that counts in a hash map and sorts the distinct values at the end. */
    static int[][] brute(int[][] ops) {
        // The hash map has no order, so ordering happens at the end.
        HashMap<Integer, Integer> m = new HashMap<>();
        for (int[] op : ops) {
            int cur = m.getOrDefault(op[1], 0);
            // Add raises the count, and remove lowers it only when it is positive.
            if (op[0] == 1) m.put(op[1], cur + 1);
            else if (cur > 0) m.put(op[1], cur - 1);
        }
        // Keep only positive counts and sort the values.
        int[] vals = m.entrySet().stream().filter(e -> e.getValue() > 0).mapToInt(Map.Entry::getKey).sorted().toArray();
        int[][] out = new int[vals.length][2];
        for (int i = 0; i < vals.length; i++) {
            out[i][0] = vals[i];
            out[i][1] = m.get(vals[i]);
        }
        return out;
    }

    public static void main(String[] args) {
        // Checks Example 1 and Example 2.
        int[][] e1 = apply(new int[][]{{1, 5}, {1, 3}, {1, 5}, {1, 9}, {2, 3}, {2, 5}});
        if (!Arrays.deepEquals(e1, new int[][]{{5, 1}, {9, 1}})) throw new AssertionError("example 1");
        int[][] e2 = apply(new int[][]{{1, 4}, {2, 7}, {1, 4}, {2, 4}, {2, 4}, {2, 4}});
        if (e2.length != 0) throw new AssertionError("example 2");
        // Checks the Java claims: a zero-count entry stays visible, firstKey throws, firstEntry returns null.
        TreeMap<Integer, Integer> t = new TreeMap<>();
        t.put(3, 0);
        if (t.firstKey() != 3) throw new AssertionError("zero count stays");
        t.remove(3);
        boolean threw = false;
        try { t.firstKey(); } catch (NoSuchElementException ex) { threw = true; }
        if (!threw || t.firstEntry() != null) throw new AssertionError("empty map");
        // Checks that subMap is a live view of the map.
        t.put(1, 1); t.put(5, 1); t.put(9, 1);
        Map<Integer, Integer> view = t.subMap(2, true, 9, true);
        t.put(7, 4);
        if (view.size() != 3 || view.get(7) != 4) throw new AssertionError("live subMap");
        // Checks random operation lists against the hash-map oracle.
        Random rnd = new Random(3204);
        for (int round = 0; round < 400; round++) {
            int m = rnd.nextInt(30);
            int[][] ops = new int[m][2];
            for (int i = 0; i < m; i++) {
                ops[i][0] = 1 + rnd.nextInt(2);
                ops[i][1] = rnd.nextInt(7) - 3;
            }
            if (!Arrays.deepEquals(apply(ops), brute(ops))) throw new AssertionError("round " + round);
        }
    }
}
```

#### Solution: [Boundary] Missing Neighbor And Comparator Equality (Author exercise)
<!-- id: ord-comparator-equality -->

**Approach.** A `TreeSet` built with a case-insensitive comparator treats two spellings as one key.

The comparator `String.CASE_INSENSITIVE_ORDER` returns 0 for words that differ only in case. The set therefore ignores a second insertion of the same key, and the first spelling stays. For a query, `lower(query)` returns the greatest stored word whose key is strictly smaller, and the comparator also decides what smaller means. When no stored key is smaller, `lower` returns `null`, and the program writes `none`. The invariant is that the set stays ordered under one comparator that is never changed, and that no stored element is mutated. The harness asserts that `add` returns false for the repeated key, that `equals` still says the spellings differ, that `BigDecimal` values `1.0` and `1.00` merge in a `TreeSet` but not in a `HashSet`, and that mutating a stored key hides it from `contains`.

**Complexity.**

- **Time** is O((n + q) log n) comparisons, and each comparison costs O(L) for words of length `L`, which is at most 10 here.
- **Space** is O(n), for the nodes of the stored keys.

```java run
import java.math.BigDecimal;
import java.util.HashSet;
import java.util.Random;
import java.util.TreeSet;

public final class ComparatorEqualityCheck {
    /**
     * Returns, per query, the stored word with the greatest key strictly below the query key, or "none".
     * Time: O((n + q) L log n) for words of length L.
     * Space: O(n), one node per distinct key.
     * Invariant: the tree is ordered under one fixed comparator and no stored element changes.
     */
    static String[] lowerWords(String[] words, String[] queries) {
        // Keys that differ only in case compare as equal under this comparator.
        TreeSet<String> set = new TreeSet<>(String.CASE_INSENSITIVE_ORDER);
        // add ignores a word whose key is already present, so the first spelling stays.
        for (String w : words) set.add(w);
        // One answer per query.
        String[] out = new String[queries.length];
        for (int i = 0; i < queries.length; i++) {
            // lower returns the greatest strictly smaller element, or null when none exists.
            String r = set.lower(queries[i]);
            // The null result becomes the required text.
            out[i] = r == null ? "none" : r;
        }
        return out;
    }

    /** Oracle that keeps first spellings in a list and scans for the best smaller key. */
    static String[] brute(String[] words, String[] queries) {
        java.util.ArrayList<String> kept = new java.util.ArrayList<>();
        // Keep a word only when no kept word has the same lower-case text.
        for (String w : words) {
            boolean seen = false;
            for (String k : kept) if (k.toLowerCase().equals(w.toLowerCase())) seen = true;
            if (!seen) kept.add(w);
        }
        String[] out = new String[queries.length];
        for (int i = 0; i < queries.length; i++) {
            String best = null;
            for (String k : kept) {
                // A candidate must be strictly smaller than the query in lower-case order.
                if (k.toLowerCase().compareTo(queries[i].toLowerCase()) < 0
                        && (best == null || k.toLowerCase().compareTo(best.toLowerCase()) > 0)) best = k;
            }
            out[i] = best == null ? "none" : best;
        }
        return out;
    }

    public static void main(String[] args) {
        // Checks Example 1 and Example 2.
        String[] e1 = lowerWords(new String[]{"Pear", "apple", "APPLE", "banana"}, new String[]{"BANANA", "Apple", "zebra"});
        if (!java.util.Arrays.equals(e1, new String[]{"apple", "none", "Pear"})) throw new AssertionError("example 1");
        String[] e2 = lowerWords(new String[]{"b", "B", "a"}, new String[]{"B", "A", "c"});
        if (!java.util.Arrays.equals(e2, new String[]{"a", "none", "b"})) throw new AssertionError("example 2");
        // Checks that the comparator, and not equals, decides key identity.
        TreeSet<String> ci = new TreeSet<>(String.CASE_INSENSITIVE_ORDER);
        ci.add("apple");
        if (ci.add("APPLE") || ci.size() != 1 || !ci.contains("Apple")) throw new AssertionError("comparator identity");
        if ("Apple".equals("apple")) throw new AssertionError("equals differs");
        // Checks a comparator that is not consistent with equals: BigDecimal 1.0 and 1.00.
        BigDecimal a = new BigDecimal("1.0"), b = new BigDecimal("1.00");
        if (a.equals(b) || a.compareTo(b) != 0) throw new AssertionError("bigdecimal contract");
        TreeSet<BigDecimal> tree = new TreeSet<>(java.util.List.of(a, b));
        HashSet<BigDecimal> hash = new HashSet<>(java.util.List.of(a, b));
        if (tree.size() != 1 || hash.size() != 2) throw new AssertionError("merge versus keep both");
        // Checks the key mutation hazard: changing a stored key hides it from searches.
        int[] x = {5}, y = {10}, z = {15};
        TreeSet<int[]> byFirst = new TreeSet<>((p, q) -> Integer.compare(p[0], q[0]));
        byFirst.add(x); byFirst.add(y); byFirst.add(z);
        x[0] = 50;
        if (byFirst.contains(new int[]{50}) || byFirst.contains(new int[]{5}) || byFirst.size() != 3) throw new AssertionError("mutation hazard");
        // Checks that a natural-order TreeMap rejects a null key.
        boolean threw = false;
        try { new java.util.TreeMap<String, Integer>().put(null, 1); } catch (NullPointerException ex) { threw = true; }
        if (!threw) throw new AssertionError("null key");
        // Checks random inputs against the oracle.
        Random rnd = new Random(3205);
        String letters = "abcABC";
        for (int round = 0; round < 400; round++) {
            String[] ws = new String[rnd.nextInt(10)];
            String[] qs = new String[8];
            for (int i = 0; i < ws.length; i++) ws[i] = word(rnd, letters);
            for (int i = 0; i < qs.length; i++) qs[i] = word(rnd, letters);
            if (!java.util.Arrays.equals(lowerWords(ws, qs), brute(ws, qs))) throw new AssertionError("round " + round);
        }
    }

    /** Builds a random word of length 1 to 3 over the given letters. */
    static String word(Random rnd, String letters) {
        StringBuilder sb = new StringBuilder();
        int len = 1 + rnd.nextInt(3);
        for (int i = 0; i < len; i++) sb.append(letters.charAt(rnd.nextInt(letters.length())));
        return sb.toString();
    }
}
```

#### Solution: [Recognize] My Calendar I (LeetCode 729)
<!-- id: ord-calendar-booking -->

**Approach.** Accepted bookings never overlap, so only the two neighbors of a new start can conflict with it.

The program stores each accepted booking in a `TreeMap` from start to end. For a new range, `floorEntry(start)` gives the booking with the greatest start at most the new start. That booking overlaps when its end is greater than the new start. The call `ceilingKey(start)` gives the booking with the smallest start at least the new start, and that booking overlaps when its start is below the new end. Any other stored booking lies entirely before the floor booking or after the ceiling booking, because the stored ranges are disjoint and sorted by start. The invariant is that the stored ranges stay pairwise disjoint. A booking with the same start as the new one is found by `floorEntry`, and its end exceeds the start, so the call is rejected.

**Complexity.**

- **Time** is O(log n) per call, since one insertion and two navigation calls follow tree paths.
- **Space** is O(n), one entry per accepted booking.

```java run
import java.util.ArrayList;
import java.util.Map;
import java.util.Random;
import java.util.TreeMap;

public final class CalendarCheck {
    private final TreeMap<Integer, Integer> booked = new TreeMap<>();

    /**
     * Books [start, end) when it shares no time with an accepted booking.
     * Time: O(log n), three tree paths.
     * Space: O(1) extra per call, plus one stored entry when accepted.
     * Invariant: the stored ranges are pairwise disjoint, so only the two nearest starts can conflict.
     */
    boolean book(int start, int end) {
        // The booking with the greatest start at most the new start.
        Map.Entry<Integer, Integer> before = booked.floorEntry(start);
        // It conflicts when it still runs after the new start.
        if (before != null && before.getValue() > start) return false;
        // The booking with the smallest start at least the new start.
        Integer after = booked.ceilingKey(start);
        // It conflicts when it begins before the new range ends.
        if (after != null && after < end) return false;
        // No neighbor conflicts, so the range is stored and the invariant holds.
        booked.put(start, end);
        return true;
    }

    /** Oracle that compares the new range with every accepted range. */
    static final class Brute {
        final ArrayList<int[]> list = new ArrayList<>();

        boolean book(int start, int end) {
            // Two half-open ranges overlap when each starts before the other ends.
            for (int[] r : list) if (start < r[1] && r[0] < end) return false;
            list.add(new int[]{start, end});
            return true;
        }
    }

    public static void main(String[] args) {
        // Checks Example 1.
        CalendarCheck c1 = new CalendarCheck();
        if (!c1.book(10, 20) || c1.book(15, 25) || !c1.book(20, 30)) throw new AssertionError("example 1");
        // Checks Example 2, which includes touching ranges and an overlap with two bookings.
        CalendarCheck c2 = new CalendarCheck();
        if (!c2.book(5, 10) || !c2.book(0, 5) || c2.book(0, 6) || !c2.book(10, 11)) throw new AssertionError("example 2");
        // Checks the Java claims about navigation on the map used by the solution.
        TreeMap<Integer, Integer> m = new TreeMap<>();
        if (m.floorEntry(3) != null || m.ceilingKey(3) != null) throw new AssertionError("empty map neighbors");
        m.put(5, 9);
        if (m.floorEntry(5).getValue() != 9 || m.ceilingKey(5) != 5) throw new AssertionError("equal start");
        // Checks random call sequences against the oracle.
        Random rnd = new Random(3206);
        for (int round = 0; round < 400; round++) {
            CalendarCheck fast = new CalendarCheck();
            Brute slow = new Brute();
            for (int call = 0; call < 25; call++) {
                int s = rnd.nextInt(40);
                int e = s + 1 + rnd.nextInt(8);
                if (fast.book(s, e) != slow.book(s, e)) throw new AssertionError("round " + round + " call " + call);
            }
        }
    }
}
```
