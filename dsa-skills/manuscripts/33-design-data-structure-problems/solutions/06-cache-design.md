<!-- solutions-for: 06-cache-design -->
### Solutions For Evicting Cache Entries

#### Solution: [Build] Move Node To Front (Author exercise)
<!-- id: ds-move-to-front -->

**Approach.**

The list owns two sentinel nodes, `head` and `tail`, that never hold a key. Because they always exist, every real node has a non-null `prev` and `next`, and no operation tests for null. The invariant is that following `next` from `head` reaches `tail`, and following `prev` from `tail` reaches `head`, and both walks visit the same real nodes in opposite order.

`moveToFront` runs two steps in a fixed order. The detach step makes the node's `prev` and `next` neighbors point at each other, which uses all four links around the node. The reinsert step then links the node between `head` and `head.next`, which again rewrites four links. Detaching first and inserting second also handles a node that is already first, because the detach step leaves it isolated and the insert step puts it back in the same place. The operation `removeLast` detaches `tail.prev`, so the least recent key leaves in constant time.

**Complexity.**

- **Time** is O(1) per operation, because each operation rewrites a fixed number of links and never walks the list.
- **Space** is O(1) auxiliary per operation, because only the nodes themselves exist and no operation allocates more than one node.

```java run
import java.util.*;

public final class FrontList {
    /** One list node. The key is fixed; the two links change as the node moves. */
    static final class Node {
        final int key;
        Node prev, next;
        Node(int key) { this.key = key; }
    }

    // The sentinels never hold data, so real nodes always have two non-null neighbors.
    private final Node head = new Node(-1);
    private final Node tail = new Node(-1);
    private int size;

    FrontList() {
        // An empty list is head linked to tail in both directions.
        head.next = tail;
        tail.prev = head;
    }

    /**
     * Creates a node for key at the front and returns it.
     * Time: O(1). Space: O(1). Invariant: forward and backward walks agree.
     */
    Node addFront(int key) {
        Node node = new Node(key);
        insertAfterHead(node);
        size++;
        return node;
    }

    /**
     * Moves a node that is currently in this list to the front.
     * Time: O(1), eight link writes at most. Space: O(1).
     * Invariant: the node appears exactly once after the call.
     */
    void moveToFront(Node node) {
        // Detach first so the old neighbors stop pointing at the node.
        detach(node);
        // Reinsert second; this also works when the node was already first.
        insertAfterHead(node);
    }

    /** Removes and returns the key at the back. Time: O(1). Space: O(1). */
    int removeLast() {
        // An empty list has no back node to remove.
        if (size == 0) throw new NoSuchElementException("empty list");
        Node last = tail.prev;
        detach(last);
        size--;
        return last.key;
    }

    private void detach(Node n) {
        // The two neighbors now point at each other; the node's own links are overwritten on reinsert.
        n.prev.next = n.next;
        n.next.prev = n.prev;
    }

    private void insertAfterHead(Node n) {
        // Link the node to its new neighbors first, then link the neighbors back to it.
        n.prev = head;
        n.next = head.next;
        head.next.prev = n;
        head.next = n;
    }

    List<Integer> frontToBack() {
        List<Integer> out = new ArrayList<>();
        // Follow next links until the tail sentinel is reached.
        for (Node n = head.next; n != tail; n = n.next) out.add(n.key);
        return out;
    }

    List<Integer> backToFront() {
        List<Integer> out = new ArrayList<>();
        // Follow prev links until the head sentinel is reached.
        for (Node n = tail.prev; n != head; n = n.prev) out.add(n.key);
        return out;
    }

    public static void main(String[] args) {
        // Example 1: three adds, move the oldest to the front, then remove the back.
        FrontList list = new FrontList();
        Node one = list.addFront(1);
        list.addFront(2);
        Node three = list.addFront(3);
        if (!list.frontToBack().equals(List.of(3, 2, 1))) throw new AssertionError("after adds");
        list.moveToFront(one);
        if (!list.frontToBack().equals(List.of(1, 3, 2))) throw new AssertionError("after move");
        if (list.removeLast() != 2) throw new AssertionError("removeLast");
        // Example 2: moving the node that is already first changes nothing.
        list.moveToFront(one);
        if (!list.frontToBack().equals(List.of(1, 3))) throw new AssertionError("first node move");
        if (!list.backToFront().equals(List.of(3, 1))) throw new AssertionError("backward walk");
        // Removing from an empty list fails loudly.
        FrontList empty = new FrontList();
        try { empty.removeLast(); throw new AssertionError("expected failure"); } catch (NoSuchElementException expected) { }

        // Random operations against an ArrayList model that stores the front at index 0.
        Random rnd = new Random(3306);
        for (int round = 0; round < 200; round++) {
            FrontList real = new FrontList();
            List<Integer> model = new ArrayList<>();
            Map<Integer, Node> nodes = new HashMap<>();
            int nextKey = 0;
            for (int step = 0; step < 150; step++) {
                int op = rnd.nextInt(3);
                if (op == 0 && model.size() < 12) {
                    // Add a fresh key at the front in both structures.
                    nodes.put(nextKey, real.addFront(nextKey));
                    model.add(0, nextKey++);
                } else if (op == 1 && !model.isEmpty()) {
                    // Move a random present key to the front in both structures.
                    int key = model.get(rnd.nextInt(model.size()));
                    real.moveToFront(nodes.get(key));
                    model.remove(Integer.valueOf(key));
                    model.add(0, key);
                } else if (op == 2 && !model.isEmpty()) {
                    // Remove from the back in both structures.
                    int expected = model.remove(model.size() - 1);
                    if (real.removeLast() != expected) throw new AssertionError("removeLast mismatch");
                    nodes.remove(expected);
                }
                // Both walks must match the model, and the backward walk must be its reverse.
                if (!real.frontToBack().equals(model)) throw new AssertionError("forward mismatch");
                List<Integer> reversed = new ArrayList<>(model);
                Collections.reverse(reversed);
                if (!real.backToFront().equals(reversed)) throw new AssertionError("backward mismatch");
            }
        }
    }
}
```

#### Solution: [Vary] LRU Cache With Peek (LeetCode 146)
<!-- id: ds-lru-peek-contract -->

**Approach.**

The state is a map from key to node and a doubly linked list with two sentinels, ordered from most recent at the front to least recent at the back. The invariant is that the map holds exactly the keys in the list, each once, and the list order is the order of last refresh. The operations `get` and an overwriting `put` both detach the node and reinsert it at the front, so they refresh. The operation `peek` reads the node's value and touches no link, so it does not refresh. That one difference is the changed contract, and it makes the order observable through `keysByRecency`.

A `put` of a new key first checks `index.size() == capacity`. If the cache is full, it detaches `tail.prev`, which is the least recent node, and removes that key from the map before inserting the new node. The eviction happens before the insert, so the map never holds more than `capacity` keys.

The main method also checks the library shortcut. A `LinkedHashMap` built with access order and a `removeEldestEntry` override matches the same random script, which shows that the shortcut honors this contract for `get` and `put` only. It has no operation that reads without refreshing the order. The main method also shows why a key class needs `equals` and `hashCode`.

**Complexity.**

- **Time** is O(1) expected per operation, because a hash lookup plus a fixed number of link writes does all the work; `keysByRecency` is O(size) because it reports every key.
- **Space** is O(capacity), because the map and the list each hold at most `capacity` entries.

```java run
import java.util.*;

public final class RecencyCache {
    private static final class Node {
        int key, value;
        Node prev, next;
    }

    private final int capacity;
    private final Map<Integer, Node> index = new HashMap<>();
    // Sentinels hold no data; head.next is the most recent node and tail.prev the least recent.
    private final Node head = new Node();
    private final Node tail = new Node();

    RecencyCache(int capacity) {
        // A cache of zero entries is outside this contract.
        if (capacity < 1) throw new IllegalArgumentException("capacity must be at least 1");
        this.capacity = capacity;
        head.next = tail;
        tail.prev = head;
    }

    private void unlink(Node n) {
        // Connect the two neighbors to each other.
        n.prev.next = n.next;
        n.next.prev = n.prev;
    }

    private void linkFront(Node n) {
        // Place the node directly after head and repair both neighbors.
        n.prev = head;
        n.next = head.next;
        head.next.prev = n;
        head.next = n;
    }

    /**
     * Returns the value and refreshes the key, or -1 when absent.
     * Time: O(1) expected. Space: O(1). Invariant: the list holds exactly the map's keys.
     */
    int get(int key) {
        Node n = index.get(key);
        // A miss changes nothing.
        if (n == null) return -1;
        // A hit moves the node to the front.
        unlink(n);
        linkFront(n);
        return n.value;
    }

    /** Returns the value without refreshing, or -1 when absent. Time: O(1) expected. Space: O(1). */
    int peek(int key) {
        Node n = index.get(key);
        // No link is touched, so the order stays the same.
        return n == null ? -1 : n.value;
    }

    /**
     * Stores the value and refreshes the key; evicts the least recent key when a new key arrives at capacity.
     * Time: O(1) expected. Space: O(1).
     */
    void put(int key, int value) {
        Node n = index.get(key);
        if (n != null) {
            // Overwrite keeps the node, replaces the value and refreshes the order.
            n.value = value;
            unlink(n);
            linkFront(n);
            return;
        }
        if (index.size() == capacity) {
            // Evict the back node first, so the map never exceeds capacity.
            Node victim = tail.prev;
            unlink(victim);
            index.remove(victim.key);
        }
        n = new Node();
        n.key = key;
        n.value = value;
        index.put(key, n);
        linkFront(n);
    }

    /** Lists keys with the most recent first. Time: O(size). Space: O(size) for the result. */
    List<Integer> keysByRecency() {
        List<Integer> out = new ArrayList<>();
        // Walk from the front sentinel to the back sentinel.
        for (Node n = head.next; n != tail; n = n.next) out.add(n.key);
        return out;
    }

    /** Library shortcut: access-ordered LinkedHashMap that drops the eldest entry after an insert. */
    static final class Shortcut extends LinkedHashMap<Integer, Integer> {
        private final int limit;
        Shortcut(int limit) {
            // The third constructor argument true selects access order instead of insertion order.
            super(16, 0.75f, true);
            this.limit = limit;
        }
        @Override
        protected boolean removeEldestEntry(Map.Entry<Integer, Integer> eldest) {
            return size() > limit;
        }
    }

    /** Key class with no equals or hashCode, so lookup uses object identity. */
    static final class RawKey {
        final int id;
        RawKey(int id) { this.id = id; }
    }

    record ValueKey(int id) { }

    public static void main(String[] args) {
        // Example 1: get refreshes, so key 2 is evicted when key 3 arrives.
        RecencyCache a = new RecencyCache(2);
        a.put(1, 10);
        a.put(2, 20);
        if (a.get(1) != 10) throw new AssertionError("get value");
        a.put(3, 30);
        if (!a.keysByRecency().equals(List.of(3, 1))) throw new AssertionError("example 1 order");
        if (a.peek(2) != -1) throw new AssertionError("evicted key");
        // Example 2: peek does not refresh, so key 1 is evicted even though it was just read.
        RecencyCache b = new RecencyCache(2);
        b.put(1, 10);
        b.put(2, 20);
        if (b.peek(1) != 10) throw new AssertionError("peek value");
        b.put(3, 30);
        if (!b.keysByRecency().equals(List.of(3, 2))) throw new AssertionError("example 2 order");
        // Overwriting refreshes: key 2 moves ahead of key 3.
        b.put(2, 25);
        if (!b.keysByRecency().equals(List.of(2, 3)) || b.peek(2) != 25) throw new AssertionError("overwrite refresh");

        // The shortcut matches the contract for get and put: access order refreshes on get, containsKey does not.
        Shortcut s = new Shortcut(2);
        s.put(1, 10);
        s.put(2, 20);
        s.containsKey(1);
        s.put(3, 30);
        if (s.containsKey(1)) throw new AssertionError("containsKey must not refresh");
        s.clear();
        s.put(1, 10);
        s.put(2, 20);
        s.get(1);
        s.put(3, 30);
        if (s.containsKey(2) || !s.containsKey(1)) throw new AssertionError("get must refresh");
        // A get during iteration of an access-ordered map is a structural change.
        Shortcut it = new Shortcut(5);
        it.put(1, 1);
        it.put(2, 2);
        it.put(3, 3);
        try {
            for (int k : it.keySet()) it.get(1);
            throw new AssertionError("expected ConcurrentModificationException");
        } catch (ConcurrentModificationException expected) { }
        // Keys without equals and hashCode miss; a record key hits.
        Map<Object, Integer> keyed = new HashMap<>();
        keyed.put(new RawKey(1), 1);
        if (keyed.get(new RawKey(1)) != null) throw new AssertionError("identity lookup");
        keyed.put(new ValueKey(1), 2);
        if (keyed.get(new ValueKey(1)) != 2) throw new AssertionError("value lookup");

        // Random scripts against a list model whose index 0 is the most recent entry.
        Random rnd = new Random(1460);
        for (int round = 0; round < 300; round++) {
            int cap = 1 + rnd.nextInt(4);
            RecencyCache real = new RecencyCache(cap);
            Shortcut lib = new Shortcut(cap);
            List<int[]> model = new ArrayList<>();
            for (int step = 0; step < 120; step++) {
                int key = rnd.nextInt(7);
                int op = rnd.nextInt(3);
                int at = -1;
                // Find the key in the model by scanning, which is the slow but obviously right way.
                for (int i = 0; i < model.size(); i++) if (model.get(i)[0] == key) at = i;
                if (op == 0) {
                    int expected = at < 0 ? -1 : model.get(at)[1];
                    if (real.get(key) != expected) throw new AssertionError("get mismatch");
                    Integer got = lib.get(key);
                    if ((got == null ? -1 : got) != expected) throw new AssertionError("shortcut get mismatch");
                    // A hit moves the entry to index 0.
                    if (at >= 0) model.add(0, model.remove(at));
                } else if (op == 1) {
                    int value = rnd.nextInt(100);
                    real.put(key, value);
                    lib.put(key, value);
                    if (at >= 0) model.remove(at);
                    // A new key at capacity removes the last entry first.
                    else if (model.size() == cap) model.remove(model.size() - 1);
                    model.add(0, new int[] {key, value});
                } else {
                    int expected = at < 0 ? -1 : model.get(at)[1];
                    if (real.peek(key) != expected) throw new AssertionError("peek mismatch");
                }
                // The observable order must match after every operation.
                List<Integer> want = new ArrayList<>();
                for (int[] e : model) want.add(e[0]);
                if (!real.keysByRecency().equals(want)) throw new AssertionError("order mismatch");
                List<Integer> libKeys = new ArrayList<>(lib.keySet());
                Collections.reverse(libKeys);
                if (!libKeys.equals(want)) throw new AssertionError("shortcut order mismatch");
            }
        }
    }
}
```

#### Solution: [Boundary] Capacity One And Repeated Get (Author exercise)
<!-- id: ds-capacity-one-repeated-get -->

**Approach.**

This version stores the links in `int` arrays instead of node objects. Slots `0` to `capacity - 1` hold entries, and two extra slots, `head` and `tail`, serve as sentinels. The map takes a key to its slot. The invariant is that every occupied slot appears exactly once on the forward walk from `head` and exactly once on the backward walk from `tail`, and both walks have length `size`.

Repeated `get` of the same key is safe because the refresh is detach followed by insert, and detaching a slot always leaves it unlinked before the insert links it again. A refresh that only inserted would add a second link to the same slot and create a cycle. At capacity one the only slot is both the first and the last, so `tail`'s previous slot is that slot. The eviction path detaches it, removes its key from the map, and reuses the same slot for the new key. An overwrite of the stored key never reaches the eviction path, so it keeps size one.

The methods `forwardCount` and `backwardCount` walk each direction and stop with an exception when they pass `capacity` links, so a broken cycle fails the check and cannot loop forever.

**Complexity.**

- **Time** is O(1) expected for `get` and `put`, because the map lookup and the link writes are constant; the two count methods are O(size) and exist for checking.
- **Space** is O(capacity), because the four `int` arrays and the map all have at most `capacity` entries.

```java run
import java.util.*;

public final class SlotCache {
    private final int capacity;
    private final int[] keyAt, valueAt, before, after;
    private final Map<Integer, Integer> slotOf = new HashMap<>();
    // head and tail are slot numbers just past the data slots.
    private final int head, tail;
    private int size;

    SlotCache(int capacity) {
        if (capacity < 1) throw new IllegalArgumentException("capacity must be at least 1");
        this.capacity = capacity;
        keyAt = new int[capacity];
        valueAt = new int[capacity];
        before = new int[capacity + 2];
        after = new int[capacity + 2];
        head = capacity;
        tail = capacity + 1;
        // An empty list links the two sentinels to each other.
        after[head] = tail;
        before[tail] = head;
    }

    private void cut(int s) {
        // Neighbors skip the slot; its own links are rewritten on the next insert.
        after[before[s]] = after[s];
        before[after[s]] = before[s];
    }

    private void putFirst(int s) {
        // Four writes place slot s directly after head.
        before[s] = head;
        after[s] = after[head];
        before[after[head]] = s;
        after[head] = s;
    }

    /**
     * Returns the value and refreshes the key, or -1 when absent.
     * Time: O(1) expected. Space: O(1). Invariant: each slot is linked exactly once.
     */
    int get(int key) {
        Integer s = slotOf.get(key);
        if (s == null) return -1;
        // Detach then insert: skipping the detach would link the slot twice.
        cut(s);
        putFirst(s);
        return valueAt[s];
    }

    /**
     * Stores or overwrites a value; at capacity a new key reuses the slot of the least recent entry.
     * Time: O(1) expected. Space: O(1).
     */
    void put(int key, int value) {
        Integer existing = slotOf.get(key);
        if (existing != null) {
            // Overwrite keeps the slot and refreshes the order.
            valueAt[existing] = value;
            cut(existing);
            putFirst(existing);
            return;
        }
        int s;
        if (size < capacity) {
            // A free slot exists, so take the next unused number.
            s = size++;
        } else {
            // The cache is full: the slot just before tail holds the least recent key.
            s = before[tail];
            cut(s);
            slotOf.remove(keyAt[s]);
        }
        keyAt[s] = key;
        valueAt[s] = value;
        slotOf.put(key, s);
        putFirst(s);
    }

    int size() { return size; }

    /** Counts slots reachable forward from head; fails if a walk exceeds capacity links. */
    int forwardCount() {
        int count = 0;
        for (int s = after[head]; s != tail; s = after[s]) {
            if (++count > capacity) throw new IllegalStateException("cycle or duplicate link");
        }
        return count;
    }

    /** Counts slots reachable backward from tail; fails if a walk exceeds capacity links. */
    int backwardCount() {
        int count = 0;
        for (int s = before[tail]; s != head; s = before[s]) {
            if (++count > capacity) throw new IllegalStateException("cycle or duplicate link");
        }
        return count;
    }

    private static void check(SlotCache c, int expectedSize) {
        // The map, both walks and the size field must agree.
        if (c.size() != expectedSize || c.forwardCount() != expectedSize || c.backwardCount() != expectedSize) {
            throw new AssertionError("link count mismatch");
        }
    }

    public static void main(String[] args) {
        // Example 1: capacity one, repeated get, then a second key evicts the first.
        SlotCache one = new SlotCache(1);
        one.put(5, 50);
        if (one.get(5) != 50 || one.get(5) != 50) throw new AssertionError("repeated get");
        check(one, 1);
        one.put(6, 60);
        if (one.get(5) != -1 || one.get(6) != 60) throw new AssertionError("eviction at capacity one");
        check(one, 1);
        // Example 2: overwriting the only key keeps one link and does not evict.
        SlotCache two = new SlotCache(1);
        two.put(5, 50);
        two.put(5, 51);
        if (two.get(5) != 51) throw new AssertionError("overwrite value");
        check(two, 1);

        // Random scripts mostly made of get, against a model that stamps each touch with a counter.
        Random rnd = new Random(5301);
        for (int round = 0; round < 400; round++) {
            int cap = 1 + rnd.nextInt(3);
            SlotCache real = new SlotCache(cap);
            Map<Integer, Integer> values = new HashMap<>();
            Map<Integer, Long> stamp = new HashMap<>();
            long clock = 0;
            for (int step = 0; step < 150; step++) {
                int key = rnd.nextInt(cap + 2);
                if (rnd.nextInt(4) != 0) {
                    // A get returns the stored value or -1 and refreshes the stamp on a hit.
                    int expected = values.getOrDefault(key, -1);
                    if (real.get(key) != expected) throw new AssertionError("get mismatch");
                    if (expected != -1) stamp.put(key, ++clock);
                } else {
                    int value = rnd.nextInt(100);
                    real.put(key, value);
                    if (!values.containsKey(key) && values.size() == cap) {
                        // Evict the key with the smallest stamp.
                        int oldest = -1;
                        long best = Long.MAX_VALUE;
                        for (Map.Entry<Integer, Long> e : stamp.entrySet()) {
                            if (e.getValue() < best) { best = e.getValue(); oldest = e.getKey(); }
                        }
                        values.remove(oldest);
                        stamp.remove(oldest);
                    }
                    values.put(key, value);
                    stamp.put(key, ++clock);
                }
                check(real, values.size());
            }
        }
    }
}
```

#### Solution: [Recognize] LFU Cache With Frequency Query (LeetCode 460)
<!-- id: ds-lfu-frequency-ties -->

**Approach.**

The state has three parts. A map takes each key to its value and its use count. A second map takes each count to an insertion-ordered set of the keys with that count, and each set serves as the list for its bucket. An integer `minFreq` names the smallest count that has a non-empty bucket. The invariant is that every stored key sits in exactly one bucket, the bucket matching its count, and `minFreq` is the smallest count of any stored key.

The helper `touch` moves a key from bucket `f` to bucket `f + 1` and puts it at the end of the new bucket, which makes it the most recent key there. If bucket `f` becomes empty and `f` equals `minFreq`, then `minFreq` becomes `f + 1`, because the key that just moved is the only candidate for a new minimum. Both `get` and an overwriting `put` call `touch`. A new key always enters bucket 1 and sets `minFreq` to 1, which is correct after the eviction because the new key is the smallest count of any entry. At capacity, the victim is the first key of the `minFreq` bucket, which is the least recent among the keys with the smallest count. The operation `frequency` only reads the map, so it changes nothing. With capacity 0, `put` returns before touching any state, so `get` returns -1 and `frequency` returns 0.

The count is an `int`, and the main method shows that `Integer.MAX_VALUE + 1` wraps negative. The constraints cap the script at 200000 operations, so no count can reach that limit.

**Complexity.**

- **Time** is O(1) expected per operation, because a bucket lookup, a set removal, a set insertion and the first-element read each take constant time.
- **Space** is O(capacity), because each stored key owns one entry and one bucket slot.

```java run
import java.util.*;

public final class FrequencyCache {
    private static final class Entry {
        int value;
        int count = 1;
        Entry(int value) { this.value = value; }
    }

    private final int capacity;
    private final Map<Integer, Entry> entries = new HashMap<>();
    // Each bucket keeps keys in insertion order, so the first key is the least recent one.
    private final Map<Integer, LinkedHashSet<Integer>> buckets = new HashMap<>();
    private int minFreq;

    FrequencyCache(int capacity) {
        if (capacity < 0) throw new IllegalArgumentException("capacity must not be negative");
        this.capacity = capacity;
    }

    private void touch(int key, Entry e) {
        LinkedHashSet<Integer> old = buckets.get(e.count);
        old.remove(key);
        if (old.isEmpty()) {
            // The old bucket is gone; if it was the minimum, the moved key defines the new minimum.
            buckets.remove(e.count);
            if (minFreq == e.count) minFreq++;
        }
        e.count++;
        // Adding to the end makes the key the most recent one in its new bucket.
        buckets.computeIfAbsent(e.count, f -> new LinkedHashSet<>()).add(key);
    }

    /**
     * Returns the value and counts one use, or -1 when absent.
     * Time: O(1) expected. Space: O(1). Invariant: each key sits in the bucket of its count.
     */
    int get(int key) {
        Entry e = entries.get(key);
        if (e == null) return -1;
        touch(key, e);
        return e.value;
    }

    /**
     * Stores a value; an existing key counts one use, a new key at capacity evicts first.
     * Time: O(1) expected. Space: O(1).
     */
    void put(int key, int value) {
        // Capacity 0 is accepted and ignored.
        if (capacity == 0) return;
        Entry e = entries.get(key);
        if (e != null) {
            e.value = value;
            touch(key, e);
            return;
        }
        if (entries.size() == capacity) {
            // The victim is the first key of the smallest-count bucket.
            LinkedHashSet<Integer> lowest = buckets.get(minFreq);
            int victim = lowest.iterator().next();
            lowest.remove(victim);
            if (lowest.isEmpty()) buckets.remove(minFreq);
            entries.remove(victim);
        }
        entries.put(key, new Entry(value));
        buckets.computeIfAbsent(1, f -> new LinkedHashSet<>()).add(key);
        // The new key has count 1, which is now the smallest count.
        minFreq = 1;
    }

    /** Returns the use count of key, or 0 when absent; reading it counts no use. Time: O(1). Space: O(1). */
    int frequency(int key) {
        Entry e = entries.get(key);
        return e == null ? 0 : e.count;
    }

    public static void main(String[] args) {
        // Example 1: key 1 is used twice, so the single-use key 2 is evicted.
        FrequencyCache a = new FrequencyCache(2);
        a.put(1, 10);
        a.put(2, 20);
        if (a.get(1) != 10) throw new AssertionError("get value");
        a.put(3, 30);
        if (a.frequency(1) != 2 || a.frequency(2) != 0 || a.frequency(3) != 1) throw new AssertionError("example 1");
        // Example 2: keys 1 and 2 both reach count 2, and key 2 was used first, so key 2 is evicted.
        FrequencyCache b = new FrequencyCache(2);
        b.put(1, 10);
        b.put(2, 20);
        b.get(2);
        b.get(1);
        b.put(3, 30);
        if (b.get(2) != -1 || b.get(1) != 10) throw new AssertionError("example 2 tie");
        // Capacity 0 accepts every operation and stores nothing.
        FrequencyCache zero = new FrequencyCache(0);
        zero.put(1, 10);
        if (zero.get(1) != -1 || zero.frequency(1) != 0) throw new AssertionError("capacity 0");
        // The count is an int that wraps past its maximum, which the operation limit prevents.
        if (Integer.MAX_VALUE + 1 >= 0) throw new AssertionError("int wrap");

        // Random scripts against a list model that scans for the smallest count, then the oldest touch.
        Random rnd = new Random(4601);
        for (int round = 0; round < 400; round++) {
            int cap = rnd.nextInt(4);
            FrequencyCache real = new FrequencyCache(cap);
            List<long[]> model = new ArrayList<>();
            long clock = 0;
            for (int step = 0; step < 120; step++) {
                int key = rnd.nextInt(6);
                int op = rnd.nextInt(3);
                int at = -1;
                for (int i = 0; i < model.size(); i++) if (model.get(i)[0] == key) at = i;
                if (op == 0) {
                    long expected = at < 0 ? -1 : model.get(at)[1];
                    if (real.get(key) != expected) throw new AssertionError("get mismatch");
                    if (at >= 0) { model.get(at)[2]++; model.get(at)[3] = ++clock; }
                } else if (op == 1) {
                    int value = rnd.nextInt(100);
                    real.put(key, value);
                    if (cap == 0) continue;
                    if (at >= 0) {
                        model.get(at)[1] = value;
                        model.get(at)[2]++;
                        model.get(at)[3] = ++clock;
                    } else {
                        if (model.size() == cap) {
                            // Evict the smallest count, breaking ties by the oldest touch.
                            int worst = 0;
                            for (int i = 1; i < model.size(); i++) {
                                long[] x = model.get(i), y = model.get(worst);
                                if (x[2] < y[2] || (x[2] == y[2] && x[3] < y[3])) worst = i;
                            }
                            model.remove(worst);
                        }
                        model.add(new long[] {key, value, 1, ++clock});
                    }
                } else {
                    long expected = at < 0 ? 0 : model.get(at)[2];
                    if (real.frequency(key) != expected) throw new AssertionError("frequency mismatch");
                }
                // After every operation all six keys must report the model's count.
                for (int k = 0; k < 6; k++) {
                    long want = 0;
                    for (long[] e : model) if (e[0] == k) want = e[2];
                    if (real.frequency(k) != want) throw new AssertionError("count mismatch");
                }
            }
        }
    }
}
```
