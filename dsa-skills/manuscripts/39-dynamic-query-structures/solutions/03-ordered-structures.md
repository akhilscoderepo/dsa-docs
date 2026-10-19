<!-- solutions-for: 03-ordered-structures -->
### Solutions For Ordered Structures

#### Solution: [Build] Layered Linked Search (Author exercise)
<!-- id: dq39-layered-linked-search -->

**Approach.**
The constructor links every key into the levels given by its height rule. Index `i` reaches `numberOfTrailingZeros(i + 1) + 1` levels. About half the nodes stay on level 0 only, and a quarter reach level 1. A `last` array holds the newest node of each level, so appending in ascending order keeps every level sorted without a second pass.

The query keeps one cursor that starts at the head. On each level from the top down, it moves right while the next key is at most `x`, then drops. The cursor key stays at most `x` and the next node on the current level stays above `x`. After level 0 the cursor sits on the largest key not above `x`, or on the head, which reports `-1`. The harness checks the level count against the bit length of `n` and compares every query with a linear scan. It also asserts at most two comparisons per level.

**Complexity.**

- **Time** is O(log n) per query, because each level costs at most one advance and one failed comparison. Construction is O(n).
- **Space** is O(n) for the links, because the heights sum to about 2n. A query uses O(1) extra space.

```java run
public final class LayeredLinkedSearch {
    /** One node of the layered structure; next[l] is the successor on level l. */
    private static final class Node {
        final int index;   // position of the key in the sorted array, -1 for the head
        final int key;     // stored key, unused for the head
        final Node[] next; // one forward link per level the node belongs to
        Node(int index, int key, int levels) {
            this.index = index;
            this.key = key;
            this.next = new Node[levels];
        }
    }

    private final Node head;
    private final int levels;
    long comparisons;

    /**
     * Builds the layers over strictly ascending keys; index i joins trailingZeros(i + 1) + 1 levels.
     * Time: O(n), because each node is linked on an average of two levels.
     * Space: O(n), because the links total about 2n.
     * Invariant: on every level the nodes appear in ascending key order.
     */
    LayeredLinkedSearch(int[] keys) {
        // The top level count is the bit length of n, which is 1 + floor(log2 n).
        int top = Math.max(1, 32 - Integer.numberOfLeadingZeros(keys.length));
        levels = top;
        // The head belongs to every level so each search can start at any level.
        head = new Node(-1, 0, top);
        // last[l] is the most recently linked node on level l.
        Node[] last = new Node[top];
        java.util.Arrays.fill(last, head);
        // Visit keys in ascending order so every level list stays sorted.
        for (int i = 0; i < keys.length; i++) {
            // Height rule: odd positions of (i + 1) reach level 0 only, multiples of 2^k reach level k.
            int h = Integer.numberOfTrailingZeros(i + 1) + 1;
            Node node = new Node(i, keys[i], h);
            // Append the node to the tail of each level it belongs to.
            for (int l = 0; l < h; l++) {
                last[l].next[l] = node;
                last[l] = node;
            }
        }
    }

    int levelCount() {
        return levels;
    }

    /**
     * Returns the index of the largest key that is at most x (closed comparison), or -1 if none.
     * Time: O(log n), because each level advances at most once before dropping.
     * Space: O(1), because only one cursor is kept.
     * Invariant: cur.key <= x always holds, and the node after cur on the current level exceeds x.
     */
    int floorIndex(long x) {
        // Start at the head so the cursor is a valid "no key yet" position.
        Node cur = head;
        // Scan from the sparsest level down to the full list.
        for (int l = levels - 1; l >= 0; l--) {
            // Advance while the next key on this level still fits under x.
            while (cur.next[l] != null) {
                comparisons++;
                if (cur.next[l].key > x) break;
                cur = cur.next[l];
            }
        }
        // The cursor rests on the answer, or on the head when every key exceeds x.
        return cur.index;
    }

    public static void main(String[] args) {
        // Fixed example from the lesson: floor of 31 is index 5, floor of 2 is none.
        int[] fixed = {3, 7, 12, 18, 25, 31, 40, 52};
        LayeredLinkedSearch s = new LayeredLinkedSearch(fixed);
        if (s.floorIndex(31) != 5) throw new AssertionError("floor 31");
        if (s.floorIndex(2) != -1) throw new AssertionError("floor 2");
        if (s.floorIndex(1000) != 7) throw new AssertionError("floor 1000");
        if (s.levelCount() != 4) throw new AssertionError("levels of 8 keys");
        // Random inputs against a linear scan oracle.
        java.util.Random rnd = new java.util.Random(7);
        for (int t = 0; t < 300; t++) {
            int n = rnd.nextInt(40);
            java.util.TreeSet<Integer> set = new java.util.TreeSet<>();
            while (set.size() < n) set.add(rnd.nextInt(200) - 100);
            int[] keys = set.stream().mapToInt(Integer::intValue).toArray();
            LayeredLinkedSearch ls = new LayeredLinkedSearch(keys);
            if (ls.levelCount() != Math.max(1, 32 - Integer.numberOfLeadingZeros(n))) throw new AssertionError("level count");
            for (int q = -110; q <= 110; q++) {
                int expect = -1;
                for (int i = 0; i < n; i++) if (keys[i] <= q) expect = i;
                long before = ls.comparisons;
                if (ls.floorIndex(q) != expect) throw new AssertionError("floor " + q);
                // Each level costs at most one advance plus one failed comparison.
                if (ls.comparisons - before > 2L * ls.levelCount()) throw new AssertionError("too many steps");
            }
        }
    }
}
```

#### Solution: [Vary] Design Skiplist (LeetCode 1206)
<!-- id: dq39-design-skiplist -->

**Approach.**
The skiplist keeps a head with sixteen links and one node per stored copy. A shared `descend` method walks from the highest used level and records in an update array the last node whose key is below the target. All three operations use that array. Search checks whether the level 0 successor has the target key. Add splices a new node of the supplied height after the update entries. Erase takes the first copy at level 0 and unlinks it from every level it occupies.

The first copy is the right node on every level, because it is the first node at or above the target everywhere it appears. Duplicates of unequal height are therefore safe: the unlinked node is always the first one, and the others stay in place. The height comes from an injected supplier. The harness runs seeded coin flips, a constant height of one that degenerates into a chain, and an out-of-range height that clamps to sixteen. Each stream is compared with a counting `TreeMap`, and the node count is compared after every call.

**Complexity.**

- **Time** is O(log n) expected per call with random heights, because each level holds about half the nodes of the one below. A degenerate height source gives O(n).
- **Space** is O(n) for the nodes, plus O(1) per call for the update array of sixteen entries.

```java run
import java.util.function.IntSupplier;

public final class Skiplist {
    private static final int MAX = 16;

    /** A node holds one key copy; duplicates are separate nodes. */
    private static final class Node {
        final int key;
        final Node[] next;
        Node(int key, int levels) {
            this.key = key;
            this.next = new Node[levels];
        }
    }

    private final Node head = new Node(0, MAX);
    private final IntSupplier levelSource;
    private int top = 1; // number of levels currently in use

    /** The supplier returns how many levels a new node joins; it is clamped to 1..16. */
    Skiplist(IntSupplier levelSource) {
        this.levelSource = levelSource;
    }

    /** Standard source: each extra level has probability one half. */
    static IntSupplier coinFlips(long seed) {
        java.util.Random rnd = new java.util.Random(seed);
        return () -> {
            int h = 1;
            while (h < MAX && rnd.nextBoolean()) h++;
            return h;
        };
    }

    /**
     * Fills update[l] with the last node on level l whose key is below target (strict comparison).
     * Time: O(log n) expected. Space: O(1) besides the array.
     * Invariant: cur.key < target, and the next node on level l has key >= target.
     */
    private Node descend(int target, Node[] update) {
        // Start from the head at the highest level in use.
        Node cur = head;
        for (int l = top - 1; l >= 0; l--) {
            // Move right while the next key is still strictly smaller than target.
            while (cur.next[l] != null && cur.next[l].key < target) cur = cur.next[l];
            // Remember the last node below target for this level.
            update[l] = cur;
        }
        // The level-0 successor is the first key that is >= target.
        return cur.next[0];
    }

    /**
     * Reports whether at least one copy of num exists.
     * Time: O(log n) expected. Space: O(1).
     */
    boolean search(int num) {
        Node found = descend(num, new Node[MAX]);
        // The first node at or above num matches only when the key is equal.
        return found != null && found.key == num;
    }

    /**
     * Inserts one more copy of num.
     * Time: O(log n) expected. Space: O(1) expected for the new node's links.
     * Invariant: every level list stays sorted and each level list is a subsequence of level 0.
     */
    void add(int num) {
        Node[] update = new Node[MAX];
        // Levels above top are served by the head, so fill them before the descent.
        java.util.Arrays.fill(update, head);
        descend(num, update);
        // Ask the level source and clamp its answer to the allowed range.
        int h = Math.max(1, Math.min(MAX, levelSource.getAsInt()));
        Node node = new Node(num, h);
        // Splice the new node after update[l] on each of its levels.
        for (int l = 0; l < h; l++) {
            node.next[l] = update[l].next[l];
            update[l].next[l] = node;
        }
        // Grow the number of levels in use if the node is taller than before.
        top = Math.max(top, h);
    }

    /**
     * Removes exactly one copy of num and reports whether a copy existed.
     * Time: O(log n) expected. Space: O(1).
     */
    boolean erase(int num) {
        Node[] update = new Node[MAX];
        Node target = descend(num, update);
        // Missing key: nothing changes.
        if (target == null || target.key != num) return false;
        // Unlink the first copy on every level it occupies.
        for (int l = 0; l < target.next.length; l++) {
            update[l].next[l] = target.next[l];
        }
        // Lower the used level count while the highest level is empty.
        while (top > 1 && head.next[top - 1] == null) top--;
        return true;
    }

    /** Counts level-0 nodes; used by the harness to compare sizes. */
    int size() {
        int n = 0;
        for (Node c = head.next[0]; c != null; c = c.next[0]) n++;
        return n;
    }

    public static void main(String[] args) {
        // Fixed scenario with duplicates.
        Skiplist s = new Skiplist(coinFlips(1));
        s.add(1); s.add(2); s.add(3);
        if (s.search(0)) throw new AssertionError("0 absent");
        s.add(4);
        if (!s.search(1)) throw new AssertionError("1 present");
        if (s.erase(0)) throw new AssertionError("erase 0");
        if (!s.erase(1)) throw new AssertionError("erase 1");
        if (s.search(1)) throw new AssertionError("1 gone");
        s.add(5); s.add(5);
        if (!s.erase(5) || !s.search(5)) throw new AssertionError("one copy of 5 remains");
        if (!s.erase(5) || s.search(5)) throw new AssertionError("both copies of 5 gone");
        // Second fixed scenario: the final erase of a missing key reports false.
        Skiplist d = new Skiplist(coinFlips(2));
        d.add(5); d.add(5);
        if (!d.erase(5) || !d.search(5) || !d.erase(5) || d.search(5) || d.erase(5)) throw new AssertionError("duplicate scenario");
        // Random operation streams against a counting map, under three level sources.
        for (int mode = 0; mode < 3; mode++) {
            for (int seed = 0; seed < 60; seed++) {
                final int m = mode;
                IntSupplier src = m == 0 ? coinFlips(seed) : m == 1 ? () -> 1 : () -> 99;
                Skiplist sl = new Skiplist(src);
                java.util.TreeMap<Integer, Integer> oracle = new java.util.TreeMap<>();
                java.util.Random rnd = new java.util.Random(seed * 31L + m);
                int total = 0;
                for (int op = 0; op < 300; op++) {
                    int v = rnd.nextInt(15);
                    int kind = rnd.nextInt(3);
                    if (kind == 0) {
                        sl.add(v);
                        oracle.merge(v, 1, Integer::sum);
                        total++;
                    } else if (kind == 1) {
                        boolean exp = oracle.containsKey(v);
                        if (sl.erase(v) != exp) throw new AssertionError("erase " + v);
                        if (exp) {
                            total--;
                            if (oracle.merge(v, -1, Integer::sum) == 0) oracle.remove(v);
                        }
                    } else if (sl.search(v) != oracle.containsKey(v)) {
                        throw new AssertionError("search " + v);
                    }
                    if (sl.size() != total) throw new AssertionError("size");
                }
            }
        }
    }
}
```

#### Solution: [Boundary] Duplicate Key Policy (Author exercise)
<!-- id: dq39-duplicate-key-policy -->

**Approach.**
The policy stores one node per distinct key and a `long` count in it. Add either raises the count of an existing node or creates a node with the injected height. Remove-one lowers the count and unlinks the node only when the count reaches zero. Remove-all unlinks at once and returns the old count. This keeps the invariant that every node on level 0 holds a positive count, so a search never reaches a key that has no copies.

The boundary cases are the counts and the totals. A single add can contribute three billion copies, so two adds already exceed the `int` range, which is why `times`, `count` and `size` are `long`. The harness checks a total of 4,000,000,001, the node removal on the last copy and absent-key results. It also compares random streams with a `TreeMap` under three height sources.

**Complexity.**

- **Time** is O(log n) expected per call, because each call is one descent plus constant relinking.
- **Space** is O(d) for d distinct keys, because duplicates cost no extra nodes.

```java run
import java.util.function.IntSupplier;

public final class CountedSkiplist {
    private static final int MAX = 16;

    /** One node per distinct key; count is the multiplicity. */
    private static final class Node {
        final int key;
        long count;
        final Node[] next;
        Node(int key, long count, int levels) {
            this.key = key;
            this.count = count;
            this.next = new Node[levels];
        }
    }

    private final Node head = new Node(0, 0, MAX);
    private final IntSupplier levelSource;
    private int top = 1;
    private long total; // sum of all multiplicities

    CountedSkiplist(IntSupplier levelSource) {
        this.levelSource = levelSource;
    }

    /**
     * Records the last node below key on every level and returns the first node at or above key.
     * Time: O(log n) expected. Space: O(1).
     * Invariant: update[l].key < key (strict) and update[l].next[l] is null or has key >= key.
     */
    private Node find(int key, Node[] update) {
        Node cur = head;
        // Walk from the highest used level down to level 0.
        for (int l = top - 1; l >= 0; l--) {
            // Advance while the next distinct key is smaller than the target.
            while (cur.next[l] != null && cur.next[l].key < key) cur = cur.next[l];
            update[l] = cur;
        }
        return cur.next[0];
    }

    /** Detaches a node from every level it occupies. */
    private void unlink(Node node, Node[] update) {
        // Each update[l] points at this node on the levels the node occupies.
        for (int l = 0; l < node.next.length; l++) update[l].next[l] = node.next[l];
        // Shrink the used level count when the top levels become empty.
        while (top > 1 && head.next[top - 1] == null) top--;
    }

    /**
     * Adds times copies of key (times >= 1).
     * Time: O(log n) expected. Space: O(1) amortized, one node per new distinct key.
     */
    void add(int key, long times) {
        Node[] update = new Node[MAX];
        java.util.Arrays.fill(update, head);
        Node at = find(key, update);
        total += times;
        // Existing key: raise the multiplicity and keep the node.
        if (at != null && at.key == key) {
            at.count += times;
            return;
        }
        // New key: create one node and splice it into its levels.
        int h = Math.max(1, Math.min(MAX, levelSource.getAsInt()));
        Node node = new Node(key, times, h);
        for (int l = 0; l < h; l++) {
            node.next[l] = update[l].next[l];
            update[l].next[l] = node;
        }
        top = Math.max(top, h);
    }

    /** Removes one copy; returns false when the key is absent. Time: O(log n) expected. Space: O(1). */
    boolean eraseOne(int key) {
        Node[] update = new Node[MAX];
        Node at = find(key, update);
        // Absent key: nothing to remove.
        if (at == null || at.key != key) return false;
        total--;
        at.count--;
        // The last copy removes the node itself so the structure holds only present keys.
        if (at.count == 0) unlink(at, update);
        return true;
    }

    /** Removes every copy and returns how many were removed. Time: O(log n) expected. Space: O(1). */
    long eraseAll(int key) {
        Node[] update = new Node[MAX];
        Node at = find(key, update);
        if (at == null || at.key != key) return 0;
        long removed = at.count;
        total -= removed;
        unlink(at, update);
        return removed;
    }

    long count(int key) {
        Node at = find(key, new Node[MAX]);
        return at != null && at.key == key ? at.count : 0;
    }

    long size() {
        return total;
    }

    /** Counts distinct keys by walking level 0; harness only. */
    int distinct() {
        int n = 0;
        for (Node c = head.next[0]; c != null; c = c.next[0]) n++;
        return n;
    }

    public static void main(String[] args) {
        // Fixed example: bulk additions that overflow an int total.
        CountedSkiplist s = new CountedSkiplist(() -> 3);
        s.add(5, 2_000_000_000L);
        s.add(5, 2_000_000_000L);
        s.add(9, 1);
        if (s.size() != 4_000_000_001L) throw new AssertionError("long total");
        if (s.count(5) != 4_000_000_000L) throw new AssertionError("count above int range");
        if (!s.eraseOne(9) || s.count(9) != 0 || s.distinct() != 1) throw new AssertionError("last copy removes node");
        if (s.eraseOne(9) || s.eraseAll(9) != 0) throw new AssertionError("absent key");
        if (s.eraseAll(5) != 4_000_000_000L || s.size() != 0 || s.distinct() != 0) throw new AssertionError("erase all");
        // Examples 1 and 2 of the exercise.
        CountedSkiplist a = new CountedSkiplist(() -> 2);
        a.add(7, 3); a.add(7, 2);
        if (a.count(7) != 5 || !a.eraseOne(7) || a.count(7) != 4 || a.eraseAll(7) != 4 || a.count(7) != 0 || a.size() != 0) throw new AssertionError("example 1");
        a.add(4, 2); a.add(9, 1);
        if (!a.eraseOne(9) || a.size() != 2 || a.eraseAll(9) != 0 || !a.eraseOne(4) || a.size() != 1) throw new AssertionError("example 2");
        // Random streams against a TreeMap oracle under several level sources.
        for (int mode = 0; mode < 3; mode++) {
            for (int seed = 0; seed < 60; seed++) {
                final int m = mode;
                java.util.Random coin = new java.util.Random(seed);
                IntSupplier src = m == 0 ? () -> { int h = 1; while (h < MAX && coin.nextBoolean()) h++; return h; }
                        : m == 1 ? () -> 1 : () -> MAX;
                CountedSkiplist c = new CountedSkiplist(src);
                java.util.TreeMap<Integer, Long> oracle = new java.util.TreeMap<>();
                java.util.Random rnd = new java.util.Random(seed * 17L + m);
                for (int op = 0; op < 300; op++) {
                    int v = rnd.nextInt(12);
                    int kind = rnd.nextInt(4);
                    long have = oracle.getOrDefault(v, 0L);
                    if (kind == 0) {
                        long times = 1 + rnd.nextInt(3) * 1_000_000_000L;
                        c.add(v, times);
                        oracle.put(v, have + times);
                    } else if (kind == 1) {
                        if (c.eraseOne(v) != (have > 0)) throw new AssertionError("eraseOne");
                        if (have > 1) oracle.put(v, have - 1); else oracle.remove(v);
                    } else if (kind == 2) {
                        if (c.eraseAll(v) != have) throw new AssertionError("eraseAll");
                        oracle.remove(v);
                    } else if (c.count(v) != have) {
                        throw new AssertionError("count");
                    }
                    long sum = 0;
                    for (long x : oracle.values()) sum += x;
                    if (c.size() != sum || c.distinct() != oracle.size()) throw new AssertionError("totals");
                }
            }
        }
    }
}
```

#### Solution: [Recognize] Ordered Multiset API (Author exercise)
<!-- id: dq39-ordered-multiset-api -->

**Approach.**
The recognition step is that both nearest-key queries are the same descent. Lower asks for the last key below `x`. Floor asks for the last key below `x + 1`, computed as a `long` so the largest `int` key does not overflow. One half-open limit method therefore serves both, and the other operations use it too.

Nodes live in parallel arrays addressed by slot index, with slot 0 as the head and 0 also meaning no successor. Removed slots go onto a free stack, so capacity bounds the distinct keys alive at once and not the total ever inserted. Add raises a count or splices a slot after the update entries. Remove-one lowers a count and recycles the slot on the last copy. The harness compares floor, lower and count with `TreeMap` results after every call under three height sources. A capacity of twelve keys forces slot reuse, and one check uses the maximum `int` key.

**Complexity.**

- **Time** is O(log n) expected per call, because every operation is one descent over the levels.
- **Space** is O(capacity) for the arrays, which hold sixteen links per slot.

```java run
import java.util.function.IntSupplier;

public final class OrderedMultiset {
    private static final int MAX = 16;
    private final int[] key;      // key[i] is the value stored in slot i
    private final int[] count;    // count[i] is its multiplicity
    private final int[] levels;   // levels[i] is how many levels slot i occupies
    private final int[] link;     // link[i * MAX + l] is the next slot on level l, 0 means none
    private final int[] freeStack;
    private int freeTop;
    private int top = 1;
    private final IntSupplier levelSource;

    /** Slot 0 is the head; slots 1..capacity hold distinct keys. */
    OrderedMultiset(int capacity, IntSupplier levelSource) {
        this.levelSource = levelSource;
        key = new int[capacity + 1];
        count = new int[capacity + 1];
        levels = new int[capacity + 1];
        link = new int[(capacity + 1) * MAX];
        freeStack = new int[capacity];
        // Push slots so that slot 1 is handed out first.
        for (int i = 0; i < capacity; i++) freeStack[i] = capacity - i;
        freeTop = capacity;
        levels[0] = MAX;
    }

    /**
     * Returns the last slot whose key is below limit (half-open range of keys [-inf, limit)) and fills update.
     * Time: O(log n) expected. Space: O(1).
     * Invariant: key[cur] < limit, and the next slot on level l is 0 or has key >= limit.
     */
    private int lastBelow(long limit, int[] update) {
        int cur = 0;
        // Descend from the highest used level.
        for (int l = top - 1; l >= 0; l--) {
            // Slot 0 means no successor; any other slot is compared by key.
            while (link[cur * MAX + l] != 0 && key[link[cur * MAX + l]] < limit) cur = link[cur * MAX + l];
            if (update != null) update[l] = cur;
        }
        return cur;
    }

    /** Adds one copy of x. Time: O(log n) expected. Space: O(1). */
    void add(int x) {
        int[] update = new int[MAX]; // all zero, which is the head
        int pred = lastBelow(x, update);
        int nxt = link[pred * MAX];
        // Same key already stored: raise its count.
        if (nxt != 0 && key[nxt] == x) {
            count[nxt]++;
            return;
        }
        // Capacity is the number of distinct keys the caller promised.
        if (freeTop == 0) throw new IllegalStateException("capacity exceeded");
        int slot = freeStack[--freeTop];
        int h = Math.max(1, Math.min(MAX, levelSource.getAsInt()));
        key[slot] = x;
        count[slot] = 1;
        levels[slot] = h;
        // Splice the slot after update[l] on each of its levels.
        for (int l = 0; l < h; l++) {
            link[slot * MAX + l] = link[update[l] * MAX + l];
            link[update[l] * MAX + l] = slot;
        }
        top = Math.max(top, h);
    }

    /** Removes one copy of x; false when absent. Time: O(log n) expected. Space: O(1). */
    boolean removeOne(int x) {
        int[] update = new int[MAX];
        int pred = lastBelow(x, update);
        int slot = link[pred * MAX];
        if (slot == 0 || key[slot] != x) return false;
        // More copies remain: only the count changes.
        if (--count[slot] > 0) return true;
        // Last copy: detach the slot from its levels and recycle it.
        for (int l = 0; l < levels[slot]; l++) link[update[l] * MAX + l] = link[slot * MAX + l];
        freeStack[freeTop++] = slot;
        while (top > 1 && link[top - 1] == 0) top--;
        return true;
    }

    int count(int x) {
        int slot = link[lastBelow(x, null) * MAX];
        return slot != 0 && key[slot] == x ? count[slot] : 0;
    }

    /** Largest stored key strictly below x, or -1. Uses the half-open range [-inf, x). */
    int lower(int x) {
        int s = lastBelow(x, null);
        return s == 0 ? -1 : key[s];
    }

    /** Largest stored key at most x, or -1. Uses the half-open range [-inf, x + 1), with x + 1 computed as long. */
    int floor(int x) {
        int s = lastBelow(x + 1L, null);
        return s == 0 ? -1 : key[s];
    }

    public static void main(String[] args) {
        // Fixed example: floor includes equal keys, lower excludes them.
        OrderedMultiset m = new OrderedMultiset(8, () -> 2);
        m.add(10); m.add(10); m.add(30);
        if (m.floor(10) != 10 || m.lower(10) != -1) throw new AssertionError("equal key handling");
        if (m.floor(29) != 10 || m.lower(31) != 30) throw new AssertionError("between keys");
        if (m.count(10) != 2) throw new AssertionError("count 10");
        if (!m.removeOne(10) || m.floor(10) != 10) throw new AssertionError("one copy remains");
        if (!m.removeOne(10) || m.floor(10) != -1) throw new AssertionError("key gone");
        if (m.removeOne(10)) throw new AssertionError("absent");
        // Second example of the exercise.
        OrderedMultiset b = new OrderedMultiset(4, () -> 1);
        b.add(5); b.add(8);
        if (!b.removeOne(8) || b.floor(100) != 5 || b.lower(5) != -1 || b.floor(4) != -1) throw new AssertionError("example 2");
        // The largest allowed key must not overflow when floor adds one.
        m.add(Integer.MAX_VALUE);
        if (m.floor(Integer.MAX_VALUE) != Integer.MAX_VALUE) throw new AssertionError("max key");
        // Random streams against TreeMap, with slot recycling under small capacity.
        for (int mode = 0; mode < 3; mode++) {
            for (int seed = 0; seed < 60; seed++) {
                java.util.Random coin = new java.util.Random(seed);
                final int md = mode;
                IntSupplier src = md == 0 ? () -> { int h = 1; while (h < MAX && coin.nextBoolean()) h++; return h; }
                        : md == 1 ? () -> 1 : () -> MAX;
                OrderedMultiset om = new OrderedMultiset(12, src);
                java.util.TreeMap<Integer, Integer> oracle = new java.util.TreeMap<>();
                java.util.Random rnd = new java.util.Random(seed * 13L + md);
                for (int op = 0; op < 400; op++) {
                    int v = rnd.nextInt(12);
                    int kind = rnd.nextInt(4);
                    if (kind == 0) {
                        om.add(v);
                        oracle.merge(v, 1, Integer::sum);
                    } else if (kind == 1) {
                        boolean exp = oracle.containsKey(v);
                        if (om.removeOne(v) != exp) throw new AssertionError("remove");
                        if (exp && oracle.merge(v, -1, Integer::sum) == 0) oracle.remove(v);
                    }
                    Integer f = oracle.floorKey(v), lo = oracle.lowerKey(v);
                    if (om.floor(v) != (f == null ? -1 : f)) throw new AssertionError("floor " + v);
                    if (om.lower(v) != (lo == null ? -1 : lo)) throw new AssertionError("lower " + v);
                    if (om.count(v) != oracle.getOrDefault(v, 0)) throw new AssertionError("count");
                }
            }
        }
    }
}
```
