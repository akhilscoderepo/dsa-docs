<!-- solutions-for: 91-map-and-linked-list -->
### Solutions For Map And Linked List

#### Solution: [Build] Detach And Reinsert (Author exercise)
<!-- id: ds-detach-reinsert -->

**Approach.** The method builds one doubly linked list between two sentinels and a map from key to node. The map hands over the exact node of `k`, so no scan is needed. The detach connects the old predecessor and the old successor to each other. The insert connects the node to the head sentinel and to the old first node, and it fixes the old first node's `prev` and the head's `next`. Those are the four neighbour links. The invariant is that for every real node `n`, `n.prev.next == n` and `n.next.prev == n`. A forward walk and a backward walk then give the same keys in opposite orders, and the method asserts this after the move. A node already at the hot end is detached and reinserted without harm, and a node at the cold end works because the tail sentinel plays the successor.

**Complexity.**

- **Time** is O(n) for building the list and O(1) for the move itself, because the detach and insert make a constant number of writes.
- **Space** is O(n) for the nodes and the map, which the input size already requires.

```java run
import java.util.*;

public final class DetachReinsert {
    private static final class Node {
        final int key;
        Node prev, next;
        Node(int key) { this.key = key; }
    }

    /**
     * Moves the node of k directly after the head sentinel and returns the keys head to tail.
     * Time: O(n) to build, O(1) for the move. Space: O(n) for nodes and the map.
     * Invariant: for every node n, n.prev.next == n and n.next.prev == n.
     */
    static int[] moveToFront(int[] keys, int k) {
        // Two sentinels make every real node have a real prev and next.
        Node head = new Node(-1), tail = new Node(-1);
        head.next = tail;
        tail.prev = head;
        Map<Integer, Node> index = new HashMap<>();
        // Build the list by appending each key before the tail sentinel.
        for (int key : keys) {
            Node n = new Node(key);
            n.prev = tail.prev;
            n.next = tail;
            tail.prev.next = n;
            tail.prev = n;
            index.put(key, n);
        }
        // The map returns the exact node, so no scan happens.
        Node n = index.get(k);
        // Detach: the old predecessor and the old successor link to each other (two writes).
        n.prev.next = n.next;
        n.next.prev = n.prev;
        // Insert: link the node to the head and to the old first node (four more writes in total).
        n.prev = head;
        n.next = head.next;
        head.next.prev = n;
        head.next = n;
        // Walk both directions and prove that every link agrees.
        int[] forward = new int[keys.length];
        int i = 0;
        for (Node cur = head.next; cur != tail; cur = cur.next) {
            if (cur.prev.next != cur || cur.next.prev != cur) throw new AssertionError("link mismatch");
            forward[i++] = cur.key;
        }
        if (i != keys.length) throw new AssertionError("forward length");
        int j = keys.length;
        for (Node cur = tail.prev; cur != head; cur = cur.prev) {
            if (j == 0 || forward[--j] != cur.key) throw new AssertionError("backward is not the reverse");
        }
        if (j != 0) throw new AssertionError("backward length");
        return forward;
    }

    /** Oracle: remove from an ArrayList and insert at index 0. */
    static int[] oracle(int[] keys, int k) {
        List<Integer> list = new ArrayList<>();
        for (int x : keys) list.add(x);
        list.remove(Integer.valueOf(k));
        list.add(0, k);
        int[] out = new int[list.size()];
        for (int i = 0; i < out.length; i++) out[i] = list.get(i);
        return out;
    }

    public static void main(String[] args) {
        // The two examples from the problem, recomputed here.
        if (!Arrays.equals(moveToFront(new int[] {4, 7, 1, 9}, 1), new int[] {1, 4, 7, 9})) throw new AssertionError("example 1");
        if (!Arrays.equals(moveToFront(new int[] {4, 7, 1, 9}, 9), new int[] {9, 4, 7, 1})) throw new AssertionError("example 2");
        // Boundary shapes: one node, and the key already at the hot end.
        if (!Arrays.equals(moveToFront(new int[] {5}, 5), new int[] {5})) throw new AssertionError("single node");
        if (!Arrays.equals(moveToFront(new int[] {4, 7}, 4), new int[] {4, 7})) throw new AssertionError("already first");
        // Random check against the list oracle with a fixed seed.
        Random rnd = new Random(33091);
        for (int t = 0; t < 2000; t++) {
            int n = 1 + rnd.nextInt(12);
            List<Integer> pool = new ArrayList<>();
            for (int i = 0; i < 40; i++) pool.add(i);
            Collections.shuffle(pool, rnd);
            int[] keys = new int[n];
            for (int i = 0; i < n; i++) keys[i] = pool.get(i);
            int k = keys[rnd.nextInt(n)];
            if (!Arrays.equals(moveToFront(keys, k), oracle(keys, k))) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Vary] LRU Cache With Resize (LeetCode 146)
<!-- id: ds-lru-resize -->

**Approach.** The cache keeps a map from key to node and a doubly linked list between two sentinels, with the hottest node next to the head. Two private methods, `detach` and `insertFront`, make every link change. A get or an update detaches the node and reinserts it at the hot end. A put of a new key first evicts `tail.prev` when the size equals the capacity, then inserts the new node. The new `resize` stores the new capacity and then repeats the same eviction step while the size exceeds it, appending each evicted key to the result. Eviction order is therefore coldest first. The combined invariant holds after every step: the map keys equal the list nodes, and the list length equals the map size. With capacity 0, a put returns at once, so the cache stays empty.

**Complexity.**

- **Time** is O(1) average for get and put, and O(e + 1) for a resize that evicts e keys, since each eviction is one detach and one map removal.
- **Space** is O(capacity) for the nodes and the map, and O(e) for the returned array.

```java run
import java.util.*;

public final class LruResize {
    private static final class Node {
        final int key;
        int value;
        Node prev, next;
        Node(int key, int value) { this.key = key; this.value = value; }
    }

    private final Map<Integer, Node> index = new HashMap<>();
    private final Node head = new Node(0, 0);
    private final Node tail = new Node(0, 0);
    private int capacity;

    LruResize(int capacity) {
        this.capacity = capacity;
        head.next = tail;
        tail.prev = head;
    }

    /** Detaches n from the list. Time: O(1). Space: O(1). Invariant: neighbours link to each other. */
    private void detach(Node n) {
        // The old predecessor and successor now point at each other.
        n.prev.next = n.next;
        n.next.prev = n.prev;
    }

    /** Inserts n after the head sentinel. Time: O(1). Space: O(1). */
    private void insertFront(Node n) {
        // Four writes: n.prev, n.next, the old first node's prev, and the head's next.
        n.prev = head;
        n.next = head.next;
        head.next.prev = n;
        head.next = n;
    }

    /** Removes the coldest node and returns its key. Time: O(1) average. */
    private int evictCold() {
        Node cold = tail.prev;
        detach(cold);
        // The stored key makes the map removal O(1).
        index.remove(cold.key);
        return cold.key;
    }

    int get(int key) {
        Node n = index.get(key);
        // A miss changes nothing.
        if (n == null) return -1;
        // A hit moves the exact node to the hot end.
        detach(n);
        insertFront(n);
        return n.value;
    }

    void put(int key, int value) {
        // Capacity 0 stores nothing.
        if (capacity == 0) return;
        Node n = index.get(key);
        if (n != null) {
            // An update counts as a use.
            n.value = value;
            detach(n);
            insertFront(n);
            return;
        }
        // A new key at full size evicts silently.
        if (index.size() == capacity) evictCold();
        n = new Node(key, value);
        index.put(key, n);
        insertFront(n);
    }

    /** Sets the capacity and evicts coldest first until the size fits. Time: O(e + 1). */
    int[] resize(int newCapacity) {
        capacity = newCapacity;
        List<Integer> out = new ArrayList<>();
        // Each pass is one eviction, so the loop costs O(e).
        while (index.size() > capacity) out.add(evictCold());
        int[] r = new int[out.size()];
        for (int i = 0; i < r.length; i++) r[i] = out.get(i);
        return r;
    }

    int size() { return index.size(); }

    /** Verifies the combined invariant and returns the keys hot to cold. */
    int[] checkAndKeys() {
        List<Integer> fwd = new ArrayList<>();
        for (Node c = head.next; c != tail; c = c.next) {
            if (c.prev.next != c || c.next.prev != c) throw new AssertionError("links");
            if (index.get(c.key) != c) throw new AssertionError("map does not own this node");
            fwd.add(c.key);
        }
        if (fwd.size() != index.size()) throw new AssertionError("length differs from map size");
        int[] r = new int[fwd.size()];
        for (int i = 0; i < r.length; i++) r[i] = fwd.get(i);
        return r;
    }

    /** Oracle: a plain list of {key, value}, hot end at index 0. */
    static final class Model {
        final List<int[]> list = new ArrayList<>();
        int capacity;
        Model(int capacity) { this.capacity = capacity; }
        int find(int key) {
            for (int i = 0; i < list.size(); i++) if (list.get(i)[0] == key) return i;
            return -1;
        }
        int get(int key) {
            int i = find(key);
            if (i < 0) return -1;
            int[] e = list.remove(i);
            list.add(0, e);
            return e[1];
        }
        void put(int key, int value) {
            if (capacity == 0) return;
            int i = find(key);
            if (i >= 0) list.remove(i);
            else if (list.size() == capacity) list.remove(list.size() - 1);
            list.add(0, new int[] {key, value});
        }
        int[] resize(int c) {
            capacity = c;
            List<Integer> out = new ArrayList<>();
            while (list.size() > capacity) out.add(list.remove(list.size() - 1)[0]);
            int[] r = new int[out.size()];
            for (int i = 0; i < r.length; i++) r[i] = out.get(i);
            return r;
        }
    }

    public static void main(String[] args) {
        // Example 1 from the problem.
        LruResize a = new LruResize(3);
        a.put(1, 10); a.put(2, 20); a.put(3, 30);
        if (a.get(1) != 10) throw new AssertionError("e1 get");
        if (!Arrays.equals(a.resize(1), new int[] {2, 3})) throw new AssertionError("e1 resize");
        if (a.get(2) != -1 || a.get(1) != 10) throw new AssertionError("e1 after");
        // Example 2 from the problem.
        LruResize b = new LruResize(2);
        b.put(5, 50); b.put(6, 60);
        if (b.get(5) != 50) throw new AssertionError("e2 get");
        if (!Arrays.equals(b.resize(0), new int[] {6, 5})) throw new AssertionError("e2 resize");
        b.put(7, 70);
        if (b.get(5) != -1 || b.get(7) != -1 || b.size() != 0) throw new AssertionError("e2 after");
        // Growing the capacity evicts nothing.
        if (b.resize(4).length != 0) throw new AssertionError("grow");
        // Random scripts compared with the list model, with a fixed seed.
        Random rnd = new Random(33092);
        for (int t = 0; t < 400; t++) {
            int cap = 1 + rnd.nextInt(5);
            LruResize c = new LruResize(cap);
            Model m = new Model(cap);
            for (int s = 0; s < 200; s++) {
                int op = rnd.nextInt(10);
                int k = rnd.nextInt(8);
                if (op < 4) {
                    if (c.get(k) != m.get(k)) throw new AssertionError("get " + t + " " + s);
                } else if (op < 8) {
                    int v = rnd.nextInt(100);
                    c.put(k, v);
                    m.put(k, v);
                } else {
                    int nc = rnd.nextInt(6);
                    if (!Arrays.equals(c.resize(nc), m.resize(nc))) throw new AssertionError("resize " + t + " " + s);
                }
                int[] keys = c.checkAndKeys();
                if (keys.length != m.list.size()) throw new AssertionError("size");
                for (int i = 0; i < keys.length; i++) if (keys[i] != m.list.get(i)[0]) throw new AssertionError("order");
            }
        }
    }
}
```

#### Solution: [Boundary] Repeated Get And Capacity One (Author exercise)
<!-- id: ds-repeated-get-capacity-one -->

**Approach.** The solution reuses the map and sentinel list and adds a checker that runs after every operation. The checker walks forward from the head and counts each node, stopping at the tail sentinel, then walks backward from the tail and requires the reverse sequence. It also requires that the map holds each walked node under its own key, that no key repeats, and that the walk length equals the map size. A repeated get detaches a node and inserts it at the same place, and the checker shows that the node still appears once. With capacity 1, the only real node sits between both sentinels, so `head.next` and `tail.prev` are the same node. The resize to 0 then evicts that node and leaves the sentinels pointing at each other. The invariant is the combined one: map keys and list nodes are the same set, once each.

**Complexity.**

- **Time** is O(1) average per operation, plus O(size) for each walk, which only the checker pays.
- **Space** is O(size) for the nodes, the map and the sets used by the checker.

```java run
import java.util.*;

public final class RepeatedGetCapacityOne {
    private static final class Node {
        final int key;
        int value;
        Node prev, next;
        Node(int key, int value) { this.key = key; this.value = value; }
    }

    private final Map<Integer, Node> index = new HashMap<>();
    private final Node head = new Node(-1, 0);
    private final Node tail = new Node(-1, 0);
    private int capacity;

    RepeatedGetCapacityOne(int capacity) {
        this.capacity = capacity;
        head.next = tail;
        tail.prev = head;
    }

    private void detach(Node n) {
        // Connect the old neighbours to each other.
        n.prev.next = n.next;
        n.next.prev = n.prev;
    }

    private void insertFront(Node n) {
        // Link the node to the head and to the old first node.
        n.prev = head;
        n.next = head.next;
        head.next.prev = n;
        head.next = n;
    }

    private void evictCold() {
        Node cold = tail.prev;
        detach(cold);
        index.remove(cold.key);
    }

    /** Time: O(1) average. Space: O(1). Invariant: the hit node is linked exactly once afterwards. */
    int get(int key) {
        Node n = index.get(key);
        if (n == null) return -1;
        detach(n);
        insertFront(n);
        return n.value;
    }

    void put(int key, int value) {
        if (capacity == 0) return;
        Node n = index.get(key);
        if (n != null) {
            n.value = value;
            detach(n);
            insertFront(n);
            return;
        }
        if (index.size() == capacity) evictCold();
        n = new Node(key, value);
        index.put(key, n);
        insertFront(n);
    }

    void resize(int newCapacity) {
        capacity = newCapacity;
        // Evict coldest first until the size fits.
        while (index.size() > capacity) evictCold();
    }

    /** Walks both ways, proves one appearance per node, and returns the forward keys. Time: O(size). */
    int[] verify() {
        List<Node> fwd = new ArrayList<>();
        Set<Node> seen = Collections.newSetFromMap(new IdentityHashMap<>());
        for (Node c = head.next; c != tail; c = c.next) {
            // A repeated node would loop forever, so cap the walk at size + 1 steps.
            if (!seen.add(c)) throw new AssertionError("node appears twice forward");
            if (fwd.size() > index.size()) throw new AssertionError("forward walk too long");
            fwd.add(c);
        }
        List<Node> back = new ArrayList<>();
        for (Node c = tail.prev; c != head; c = c.prev) {
            if (back.size() > index.size()) throw new AssertionError("backward walk too long");
            back.add(c);
        }
        if (fwd.size() != index.size() || back.size() != index.size()) throw new AssertionError("walk length");
        Collections.reverse(back);
        for (int i = 0; i < fwd.size(); i++) {
            if (fwd.get(i) != back.get(i)) throw new AssertionError("backward is not the reverse");
            if (index.get(fwd.get(i).key) != fwd.get(i)) throw new AssertionError("map and list differ");
        }
        int[] r = new int[fwd.size()];
        for (int i = 0; i < r.length; i++) r[i] = fwd.get(i).key;
        return r;
    }

    /** Runs the script, verifying after every operation, and returns the final forward keys. */
    static int[] finalKeys(int capacity, int[][] ops) {
        RepeatedGetCapacityOne c = new RepeatedGetCapacityOne(capacity);
        for (int[] op : ops) {
            if (op[0] == 0) c.get(op[1]);
            else if (op[0] == 1) c.put(op[1], op[2]);
            else c.resize(op[1]);
            // One check per operation.
            c.verify();
        }
        return c.verify();
    }

    /** Oracle: list model with hot end at index 0 that returns the keys only. */
    static int[] oracle(int capacity, int[][] ops) {
        List<int[]> list = new ArrayList<>();
        int cap = capacity;
        for (int[] op : ops) {
            int idx = -1;
            if (op[0] != 2) for (int i = 0; i < list.size(); i++) if (list.get(i)[0] == op[1]) idx = i;
            if (op[0] == 0) {
                if (idx >= 0) list.add(0, list.remove(idx));
            } else if (op[0] == 1) {
                if (cap == 0) continue;
                if (idx >= 0) list.remove(idx);
                else if (list.size() == cap) list.remove(list.size() - 1);
                list.add(0, new int[] {op[1], op[2]});
            } else {
                cap = op[1];
                while (list.size() > cap) list.remove(list.size() - 1);
            }
        }
        int[] r = new int[list.size()];
        for (int i = 0; i < r.length; i++) r[i] = list.get(i)[0];
        return r;
    }

    public static void main(String[] args) {
        // Example 1: capacity one with repeated gets, then a resize to zero.
        int[][] e1 = {{1, 1, 10}, {0, 1}, {0, 1}, {0, 1}, {1, 2, 20}};
        if (!Arrays.equals(finalKeys(1, e1), new int[] {2})) throw new AssertionError("e1");
        int[][] e1b = {{1, 1, 10}, {0, 1}, {0, 1}, {0, 1}, {1, 2, 20}, {2, 0}};
        if (finalKeys(1, e1b).length != 0) throw new AssertionError("e1 resize to zero");
        // Example 2: three keys and three repeated gets of the oldest.
        int[][] e2 = {{1, 1, 1}, {1, 2, 2}, {1, 3, 3}, {0, 1}, {0, 1}, {0, 1}};
        if (!Arrays.equals(finalKeys(3, e2), new int[] {1, 3, 2})) throw new AssertionError("e2");
        // Random scripts compared with the list model, with a fixed seed.
        Random rnd = new Random(33093);
        for (int t = 0; t < 600; t++) {
            int cap = 1 + rnd.nextInt(4);
            int len = rnd.nextInt(60);
            int[][] ops = new int[len][];
            for (int i = 0; i < len; i++) {
                int op = rnd.nextInt(10);
                if (op < 5) ops[i] = new int[] {0, rnd.nextInt(6)};
                else if (op < 9) ops[i] = new int[] {1, rnd.nextInt(6), rnd.nextInt(50)};
                else ops[i] = new int[] {2, rnd.nextInt(5)};
            }
            if (!Arrays.equals(finalKeys(cap, ops), oracle(cap, ops))) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Recognize] LFU Cache With Eviction Log (LeetCode 460)
<!-- id: ds-lfu-evicted-sequence -->

**Approach.** This is the same ownership as before with one list for each use count. A map from key to node finds the node. A second map from use count to a doubly linked list holds the nodes with that count, hottest first. The state also holds `minCount`, the smallest count that has a node. A touch detaches the node from its count list, raises its count by one, and inserts it at the hot end of the next count list. If the old list is now empty and it was the minimum list, `minCount` moves up by one. A new key arrives with count 1 and sets `minCount` to 1. When the cache is full, the victim is the cold end of the `minCount` list, which is the least recently used node among the least frequently used. The key is added to the log, removed from the map and detached from its list. The combined invariant is that each node sits in the list for its own count, and the map keys equal the union of all list nodes.

**Complexity.**

- **Time** is O(1) average per operation, since each operation does a few map lookups and a constant number of pointer writes.
- **Space** is O(capacity) for the nodes, the maps and the count lists, plus O(e) for the log.

```java run
import java.util.*;

public final class LfuLog {
    private static final class Node {
        final int key;
        int value, count = 1;
        Node prev, next;
        Node(int key, int value) { this.key = key; this.value = value; }
    }

    /** Doubly linked list of nodes with one use count, hottest next to head. */
    private static final class Chain {
        final Node head = new Node(-1, 0), tail = new Node(-1, 0);
        int size;
        Chain() { head.next = tail; tail.prev = head; }
        void addFront(Node n) {
            n.prev = head;
            n.next = head.next;
            head.next.prev = n;
            head.next = n;
            size++;
        }
        void remove(Node n) {
            n.prev.next = n.next;
            n.next.prev = n.prev;
            size--;
        }
    }

    private final Map<Integer, Node> index = new HashMap<>();
    private final Map<Integer, Chain> byCount = new HashMap<>();
    private final List<Integer> log = new ArrayList<>();
    private final int capacity;
    private int minCount;

    LfuLog(int capacity) { this.capacity = capacity; }

    /** Moves n to the list of the next count. Time: O(1) average. Space: O(1) average. */
    private void touch(Node n) {
        Chain old = byCount.get(n.count);
        old.remove(n);
        // The minimum list may have just emptied, so the minimum count rises with the node.
        if (old.size == 0) {
            byCount.remove(n.count);
            if (minCount == n.count) minCount++;
        }
        n.count++;
        byCount.computeIfAbsent(n.count, c -> new Chain()).addFront(n);
    }

    int get(int key) {
        Node n = index.get(key);
        if (n == null) return -1;
        touch(n);
        return n.value;
    }

    void put(int key, int value) {
        Node n = index.get(key);
        if (n != null) {
            // An update counts as a use.
            n.value = value;
            touch(n);
            return;
        }
        if (index.size() == capacity) {
            // The victim is the coldest node of the smallest count.
            Chain low = byCount.get(minCount);
            Node victim = low.tail.prev;
            low.remove(victim);
            if (low.size == 0) byCount.remove(minCount);
            index.remove(victim.key);
            log.add(victim.key);
        }
        n = new Node(key, value);
        index.put(key, n);
        byCount.computeIfAbsent(1, c -> new Chain()).addFront(n);
        minCount = 1;
    }

    /** Runs the script and returns the log of evicted keys in eviction order. */
    static int[] evicted(int capacity, int[][] ops) {
        LfuLog c = new LfuLog(capacity);
        for (int[] op : ops) {
            if (op[0] == 0) c.get(op[1]);
            else c.put(op[1], op[2]);
        }
        int[] r = new int[c.log.size()];
        for (int i = 0; i < r.length; i++) r[i] = c.log.get(i);
        return r;
    }

    /** Oracle: entries {key, value, count, tick}; evict the smallest count, then the smallest tick. */
    static int[] oracle(int capacity, int[][] ops) {
        List<int[]> list = new ArrayList<>();
        List<Integer> out = new ArrayList<>();
        int tick = 0;
        for (int[] op : ops) {
            tick++;
            int[] hit = null;
            for (int[] e : list) if (e[0] == op[1]) hit = e;
            if (op[0] == 0) {
                if (hit != null) { hit[2]++; hit[3] = tick; }
            } else if (hit != null) {
                hit[1] = op[2]; hit[2]++; hit[3] = tick;
            } else {
                if (list.size() == capacity) {
                    int[] victim = list.get(0);
                    for (int[] e : list) if (e[2] < victim[2] || (e[2] == victim[2] && e[3] < victim[3])) victim = e;
                    list.remove(victim);
                    out.add(victim[0]);
                }
                list.add(new int[] {op[1], op[2], 1, tick});
            }
        }
        int[] r = new int[out.size()];
        for (int i = 0; i < r.length; i++) r[i] = out.get(i);
        return r;
    }

    public static void main(String[] args) {
        // Example 1: key 2 goes first, then the tie between keys 1 and 3 goes to the older one.
        int[][] e1 = {{1, 1, 1}, {1, 2, 2}, {0, 1}, {1, 3, 3}, {0, 3}, {1, 4, 4}};
        if (!Arrays.equals(evicted(2, e1), new int[] {2, 1})) throw new AssertionError("e1");
        // Example 2: an update raises the count of key 1.
        int[][] e2 = {{1, 1, 1}, {1, 2, 2}, {1, 1, 5}, {1, 3, 3}};
        if (!Arrays.equals(evicted(2, e2), new int[] {2})) throw new AssertionError("e2");
        // Capacity one evicts the previous key every time.
        int[][] e3 = {{1, 1, 1}, {1, 2, 2}, {1, 3, 3}};
        if (!Arrays.equals(evicted(1, e3), new int[] {1, 2})) throw new AssertionError("capacity one");
        // Random scripts compared with the list model, with a fixed seed.
        Random rnd = new Random(33094);
        for (int t = 0; t < 800; t++) {
            int cap = 1 + rnd.nextInt(4);
            int len = rnd.nextInt(80);
            int[][] ops = new int[len][];
            for (int i = 0; i < len; i++) {
                if (rnd.nextInt(10) < 4) ops[i] = new int[] {0, rnd.nextInt(7)};
                else ops[i] = new int[] {1, rnd.nextInt(7), rnd.nextInt(50)};
            }
            if (!Arrays.equals(evicted(cap, ops), oracle(cap, ops))) throw new AssertionError("random " + t);
        }
    }
}
```
