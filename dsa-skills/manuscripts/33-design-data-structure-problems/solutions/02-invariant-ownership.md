<!-- solutions-for: 02-invariant-ownership -->
### Solutions For Keeping Fields Consistent

#### Solution: [Build] Size Ownership (Author exercise)
<!-- id: ds-size-ownership -->

**Approach.**

The public operations validate first and then call a helper. `insertAt` accepts an index in `0..size` while the array has room, so it rejects everything else before any write. Its helper `openGap` shifts the values from the end down to the index one slot to the right and then increments `size`. `removeAt` accepts an index in `0..size-1`, reads the value, and calls `closeGap`, which shifts the later values one slot left and decrements `size`.

The invariant is that `data[0..size-1]` holds the stored values in order. Only the two helpers write `size`, so each successful call changes it exactly once, and a rejected call never reaches a helper. The harness counts writes through a field `sizeWrites` and compares it with the number of successful calls.

**Complexity.**

- **Time** is O(n) per insert or removal, because the helpers shift up to `size` values, and O(1) for `add` at the end.
- **Space** is O(1) beyond the fixed array, because each call keeps a few integer locals.

```java run
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public final class SizeOwnership {
    static final class IntSeq {
        private final int[] data;
        private int size;
        int sizeWrites;   // counts every write to size, so the harness can check "exactly once"

        IntSeq(int capacity) { data = new int[capacity]; }

        /**
         * Shifts data[index..size-1] one slot right and grows size; the only insertion owner.
         * Time: O(size). Space: O(1). Invariant: data[0..size-1] stays contiguous.
         */
        private void openGap(int index) {
            // Walk from the end so each value moves before its slot is overwritten.
            for (int i = size; i > index; i--) data[i] = data[i - 1];
            // The count changes here and nowhere else on the insertion path.
            size++;
            sizeWrites++;
        }

        /**
         * Shifts data[index+1..size-1] one slot left and shrinks size; the only removal owner.
         * Time: O(size). Space: O(1). Invariant: data[0..size-1] stays contiguous.
         */
        private void closeGap(int index) {
            // Walk forward so each value moves into a slot that is already free.
            for (int i = index; i < size - 1; i++) data[i] = data[i + 1];
            size--;
            sizeWrites++;
        }

        /** Inserts v at index. Time: O(size). Space: O(1). Rejects before any write. */
        boolean insertAt(int index, int v) {
            // Precheck: bad index or full array, so a rejected call never reaches the owner.
            if (index < 0 || index > size || size == data.length) return false;
            openGap(index);
            // The slot is free now, so the value lands without losing a neighbour.
            data[index] = v;
            return true;
        }

        /** Appends v. Time: O(1). Space: O(1). */
        boolean add(int v) { return insertAt(size, v); }

        /** Removes and returns the value at index, or -1 when rejected. Time: O(size). Space: O(1). */
        int removeAt(int index) {
            // Precheck before the first read of data.
            if (index < 0 || index >= size) return -1;
            int v = data[index];
            closeGap(index);
            return v;
        }

        int size() { return size; }
        int get(int i) { return data[i]; }
    }

    public static void main(String[] args) {
        // Example 1: three adds succeed, the fourth is rejected, then removeAt(0) returns 5.
        IntSeq s = new IntSeq(3);
        if (!s.add(5) || !s.add(6) || !s.add(7)) throw new AssertionError("adds");
        if (s.add(8) || s.size() != 3) throw new AssertionError("full add must be rejected");
        if (s.removeAt(0) != 5 || s.size() != 2) throw new AssertionError("removeAt");
        // Example 2: middle insert and an invalid removal.
        IntSeq t = new IntSeq(3);
        t.add(5); t.add(6);
        if (!t.insertAt(1, 9) || t.size() != 3 || t.get(0) != 5 || t.get(1) != 9 || t.get(2) != 6) throw new AssertionError("insertAt");
        if (t.removeAt(5) != -1 || t.size() != 3) throw new AssertionError("invalid removal");
        // Random operation scripts against a plain ArrayList model.
        Random rnd = new Random(3302);
        for (int round = 0; round < 200; round++) {
            int cap = 1 + rnd.nextInt(8);
            IntSeq seq = new IntSeq(cap);
            List<Integer> model = new ArrayList<>();
            int successes = 0;
            for (int step = 0; step < 200; step++) {
                int kind = rnd.nextInt(3);
                int idx = rnd.nextInt(cap + 3) - 1;
                int v = rnd.nextInt(100);
                if (kind == 0) {
                    // Model accepts the insert only for a valid index on a non-full list.
                    boolean ok = idx >= 0 && idx <= model.size() && model.size() < cap;
                    if (ok) { model.add(idx, v); successes++; }
                    if (seq.insertAt(idx, v) != ok) throw new AssertionError("insert result");
                } else if (kind == 1) {
                    boolean ok = model.size() < cap;
                    if (ok) { model.add(v); successes++; }
                    if (seq.add(v) != ok) throw new AssertionError("add result");
                } else {
                    boolean ok = idx >= 0 && idx < model.size();
                    int expected = ok ? model.remove(idx) : -1;
                    if (ok) successes++;
                    if (seq.removeAt(idx) != expected) throw new AssertionError("remove result");
                }
                // Contents, size and the exactly-once write count must match after every call.
                if (seq.size() != model.size()) throw new AssertionError("size");
                for (int i = 0; i < model.size(); i++) if (seq.get(i) != model.get(i)) throw new AssertionError("content");
                if (seq.sizeWrites != successes) throw new AssertionError("size written once per success");
            }
        }
    }
}
```

#### Solution: [Vary] Sentinel List Links (Author exercise)
<!-- id: ds-sentinel-links -->

**Approach.**

Two sentinels remove every special case for the first and last real node, because each real node always has a neighbour on both sides. `detach` joins the neighbours of a node, and `attachAfter` splices a node between a position and that position's successor. Each helper also adjusts `size`, so the count has one owner per direction.

Every public operation becomes a short composition. `addFirst` attaches after the head, `addLast` attaches after `tail.prev`, and the two removals detach `head.next` or `tail.prev`. `moveToFront` detaches the node and attaches it after the head, so it needs no link code of its own. The invariant is that walking forward from the head and backward from the tail visits the same nodes, and `size` equals their count.

**Complexity.**

- **Time** is O(1) per operation, because each one performs a fixed number of pointer writes through the helpers.
- **Space** is O(1) extra per call, and the list itself stores one node per value.

```java run
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public final class SentinelLinks {
    static final class Node {
        int val; Node prev, next;
    }

    static final class Chain {
        final Node head = new Node(), tail = new Node();
        private int size;

        Chain() { head.next = tail; tail.prev = head; }

        /** Unlinks n from its neighbours. Time: O(1). Space: O(1). The only code that removes links. */
        private void detach(Node n) {
            // Join the two neighbours around n.
            n.prev.next = n.next;
            n.next.prev = n.prev;
            n.prev = null; n.next = null;
            size--;
        }

        /** Links n directly after at. Time: O(1). Space: O(1). The only code that adds links. */
        private void attachAfter(Node at, Node n) {
            // Point n at both neighbours first, then point the neighbours at n.
            n.prev = at; n.next = at.next;
            at.next.prev = n;
            at.next = n;
            size++;
        }

        Node addFirst(int v) { Node n = new Node(); n.val = v; attachAfter(head, n); return n; }
        Node addLast(int v) { Node n = new Node(); n.val = v; attachAfter(tail.prev, n); return n; }

        int removeFirst() {
            // Empty list: head.next is the tail sentinel, so reject before detaching.
            if (size == 0) return -1;
            Node n = head.next; detach(n); return n.val;
        }

        int removeLast() {
            if (size == 0) return -1;
            Node n = tail.prev; detach(n); return n.val;
        }

        void remove(Node n) { detach(n); }

        /** Moves n to the front using only the two helpers. Time: O(1). Space: O(1). */
        void moveToFront(Node n) { detach(n); attachAfter(head, n); }

        int size() { return size; }

        Node nodeAt(int i) { Node n = head.next; while (i-- > 0) n = n.next; return n; }

        /** Reads the list forward and checks the backward walk and size agree. */
        List<Integer> toList() {
            List<Integer> fwd = new ArrayList<>();
            for (Node n = head.next; n != tail; n = n.next) fwd.add(n.val);
            List<Integer> back = new ArrayList<>();
            for (Node n = tail.prev; n != head; n = n.prev) back.add(0, n.val);
            if (!fwd.equals(back)) throw new AssertionError("forward and backward walks differ");
            if (fwd.size() != size) throw new AssertionError("size differs from node count");
            return fwd;
        }
    }

    public static void main(String[] args) {
        // Example 1: build [1,2,3], move 3 to the front, remove the last value.
        Chain c = new Chain();
        c.addLast(1); c.addLast(2); Node three = c.addLast(3);
        if (!c.toList().equals(List.of(1, 2, 3))) throw new AssertionError("build");
        c.moveToFront(three);
        if (!c.toList().equals(List.of(3, 1, 2))) throw new AssertionError("moveToFront");
        if (c.removeLast() != 2 || !c.toList().equals(List.of(3, 1))) throw new AssertionError("removeLast");
        // Example 2: empty list removal leaves the sentinels linked to each other.
        Chain e = new Chain();
        if (e.removeFirst() != -1 || e.head.next != e.tail || e.tail.prev != e.head) throw new AssertionError("empty");
        // Random operation scripts against an ArrayList model.
        Random rnd = new Random(3303);
        for (int round = 0; round < 200; round++) {
            Chain ch = new Chain();
            List<Integer> model = new ArrayList<>();
            for (int step = 0; step < 200; step++) {
                int kind = rnd.nextInt(6);
                int v = rnd.nextInt(1000);
                if (kind == 0) { ch.addFirst(v); model.add(0, v); }
                else if (kind == 1) { ch.addLast(v); model.add(v); }
                else if (kind == 2) {
                    int expected = model.isEmpty() ? -1 : model.remove(0);
                    if (ch.removeFirst() != expected) throw new AssertionError("removeFirst");
                } else if (kind == 3) {
                    int expected = model.isEmpty() ? -1 : model.remove(model.size() - 1);
                    if (ch.removeLast() != expected) throw new AssertionError("removeLast");
                } else if (!model.isEmpty()) {
                    int i = rnd.nextInt(model.size());
                    if (kind == 4) { ch.moveToFront(ch.nodeAt(i)); model.add(0, model.remove(i)); }
                    else { ch.remove(ch.nodeAt(i)); model.remove(i); }
                }
                // After every call the list must match the model and keep both walks consistent.
                if (!ch.toList().equals(model)) throw new AssertionError("list differs from model");
            }
        }
    }
}
```

#### Solution: [Boundary] Failed Mutation (Author exercise)
<!-- id: ds-failed-mutation -->

**Approach.**

The method checks the index and then fullness, and it throws before it writes anything. Only after both tests pass does it shift the values, store the new one, and update `size` and `modCount`. A thrown call therefore touches no field, and the caller can catch the exception and keep using the object.

The harness also includes a flawed variant that increments `size` first and then tests the capacity. Java keeps that increment after the exception leaves the method, so the flawed list reports a size larger than its capacity. The random check takes a snapshot of `size`, `modCount` and every array slot before each call and compares it after each rejected call.

**Complexity.**

- **Time** is O(n) for a successful insert, because it shifts up to `size` values, and O(1) for a rejected call.
- **Space** is O(1) extra, and a rejected call allocates nothing.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

public final class FailedMutation {
    static final class Bounded {
        final int[] data;
        int size, modCount;

        Bounded(int capacity) { data = new int[capacity]; }

        /**
         * Inserts v at index; throws before any write when the call is illegal.
         * Time: O(size) on success, O(1) on rejection. Space: O(1).
         * Invariant: a thrown call leaves size, modCount and data unchanged.
         */
        void insertAt(int index, int v) {
            // Precheck 1: index range, tested first by contract.
            if (index < 0 || index > size) throw new IndexOutOfBoundsException("index " + index);
            // Precheck 2: capacity, tested before the first write.
            if (size == data.length) throw new IllegalStateException("full");
            // All writes happen below this line.
            for (int i = size; i > index; i--) data[i] = data[i - 1];
            data[index] = v;
            size++;
            modCount++;
        }
    }

    /** The hazard: the count changes before the test, and Java does not undo it on a throw. */
    static final class Flawed {
        final int[] data;
        int size;

        Flawed(int capacity) { data = new int[capacity]; }

        void insertAt(int index, int v) {
            size++;
            if (size > data.length) throw new IllegalStateException("full");
            for (int i = size - 1; i > index; i--) data[i] = data[i - 1];
            data[index] = v;
        }
    }

    public static void main(String[] args) {
        // Example 1: a full list rejects a valid index and keeps every field.
        Bounded b = new Bounded(2);
        b.insertAt(0, 5); b.insertAt(0, 4);
        int mods = b.modCount;
        try { b.insertAt(0, 9); throw new AssertionError("must throw"); } catch (IllegalStateException expected) { }
        if (b.size != 2 || b.modCount != mods || b.data[0] != 4 || b.data[1] != 5) throw new AssertionError("full rejection changed state");
        // Example 2: an index beyond size throws the other exception type.
        Bounded c = new Bounded(3);
        c.insertAt(0, 5); c.insertAt(0, 4);
        try { c.insertAt(4, 9); throw new AssertionError("must throw"); } catch (IndexOutOfBoundsException expected) { }
        if (c.size != 2 || c.data[2] != 0) throw new AssertionError("index rejection changed state");
        // The flawed variant keeps its increment after the exception, so size exceeds capacity.
        Flawed f = new Flawed(1);
        f.insertAt(0, 7);
        try { f.insertAt(0, 8); throw new AssertionError("must throw"); } catch (IllegalStateException expected) { }
        if (f.size != 2) throw new AssertionError("flawed size must show the half-finished update");
        // Random scripts: valid and invalid calls against an ArrayList model with snapshots.
        Random rnd = new Random(3304);
        for (int round = 0; round < 300; round++) {
            int cap = 1 + rnd.nextInt(6);
            Bounded list = new Bounded(cap);
            List<Integer> model = new ArrayList<>();
            for (int step = 0; step < 100; step++) {
                int idx = rnd.nextInt(cap + 4) - 1;
                int v = rnd.nextInt(100);
                int sizeBefore = list.size, modsBefore = list.modCount;
                int[] dataBefore = list.data.clone();
                boolean badIndex = idx < 0 || idx > model.size();
                boolean full = model.size() == cap;
                try {
                    list.insertAt(idx, v);
                    if (badIndex || full) throw new AssertionError("should have thrown");
                    model.add(idx, v);
                } catch (IndexOutOfBoundsException ex) {
                    if (!badIndex) throw new AssertionError("wrong exception");
                    // Rejected: every field must equal its snapshot.
                    if (list.size != sizeBefore || list.modCount != modsBefore || !Arrays.equals(list.data, dataBefore)) throw new AssertionError("state changed");
                } catch (IllegalStateException ex) {
                    if (badIndex || !full) throw new AssertionError("wrong exception");
                    if (list.size != sizeBefore || list.modCount != modsBefore || !Arrays.equals(list.data, dataBefore)) throw new AssertionError("state changed");
                }
                // The accepted contents must always match the model.
                if (list.size != model.size()) throw new AssertionError("size");
                for (int i = 0; i < model.size(); i++) if (list.data[i] != model.get(i)) throw new AssertionError("content");
            }
        }
    }
}
```

#### Solution: [Recognize] LC 146 LRU Cache (LeetCode 146)
<!-- id: ds-lru-evicted-key -->

**Approach.**

The map finds a node by key, and the doubly linked list orders the nodes from most to least recently used. Two private helpers own every change. `attach` puts a node right after the head sentinel and registers its key in the map. `detach` unlinks a node and removes its key from the map. The map size and the list length therefore change together, and the harness asserts that they match after every call.

`get` detaches and re-attaches the node, which refreshes its position. `put` on an existing key updates the value and refreshes the node the same way. `put` on a new key first checks `map.size() == capacity`. When the cache is full, it detaches `tail.prev`, which is the least recently used node, and remembers its key as the return value. Only then does it attach the new node, so the cache never exceeds its capacity.

**Complexity.**

- **Time** is O(1) average per call, because each call does a fixed number of hash operations and pointer writes.
- **Space** is O(capacity), since the map and the list store one entry per cached key, up to the limit.

```java run
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Random;

public final class LruEvictedKey {
    static final class Node {
        final int key; int val; Node prev, next;
        Node(int key, int val) { this.key = key; this.val = val; }
    }

    static final class Cache {
        private final int capacity;
        private final Map<Integer, Node> map = new HashMap<>();
        private final Node head = new Node(-1, -1), tail = new Node(-1, -1);

        Cache(int capacity) { this.capacity = capacity; head.next = tail; tail.prev = head; }

        /** Unlinks n and removes its key from the map. Time: O(1) average. Space: O(1). */
        private void detach(Node n) {
            n.prev.next = n.next;
            n.next.prev = n.prev;
            map.remove(n.key);
        }

        /** Links n after the head and registers its key. Time: O(1) average. Space: O(1). */
        private void attach(Node n) {
            n.prev = head; n.next = head.next;
            head.next.prev = n;
            head.next = n;
            map.put(n.key, n);
        }

        int get(int key) {
            Node n = map.get(key);
            // Absent key: nothing to refresh.
            if (n == null) return -1;
            detach(n); attach(n);
            return n.val;
        }

        /** Stores the pair; returns the evicted key or -1. Time: O(1) average. Space: O(1). */
        int put(int key, int val) {
            Node n = map.get(key);
            if (n != null) {
                // Update in place and refresh recency; no eviction for an existing key.
                n.val = val;
                detach(n); attach(n);
                return -1;
            }
            int evicted = -1;
            // Full cache: the node before the tail sentinel is least recently used.
            if (map.size() == capacity) {
                Node lru = tail.prev;
                detach(lru);
                evicted = lru.key;
            }
            attach(new Node(key, val));
            return evicted;
        }

        int mapSize() { return map.size(); }

        int listLength() { int c = 0; for (Node n = head.next; n != tail; n = n.next) c++; return c; }
    }

    /** Naive model: a recency-ordered list of {key, value}, most recent first. */
    static final class Model {
        final int capacity; final List<int[]> items = new ArrayList<>();
        Model(int capacity) { this.capacity = capacity; }
        int indexOf(int key) { for (int i = 0; i < items.size(); i++) if (items.get(i)[0] == key) return i; return -1; }
        int get(int key) {
            int i = indexOf(key);
            if (i < 0) return -1;
            int[] e = items.remove(i); items.add(0, e);
            return e[1];
        }
        int put(int key, int val) {
            int i = indexOf(key);
            if (i >= 0) { items.remove(i); items.add(0, new int[] {key, val}); return -1; }
            int evicted = -1;
            if (items.size() == capacity) evicted = items.remove(items.size() - 1)[0];
            items.add(0, new int[] {key, val});
            return evicted;
        }
    }

    public static void main(String[] args) {
        // Example 1: capacity 3 with a get, an eviction of 6, an update and an eviction of 5.
        Cache c = new Cache(3);
        if (c.put(5, 50) != -1 || c.put(6, 60) != -1 || c.put(7, 70) != -1) throw new AssertionError("fill");
        if (c.get(5) != 50) throw new AssertionError("get 5");
        if (c.put(8, 80) != 6) throw new AssertionError("evict 6");
        if (c.put(7, 71) != -1) throw new AssertionError("update");
        if (c.put(9, 90) != 5) throw new AssertionError("evict 5");
        if (c.mapSize() != c.listLength()) throw new AssertionError("map and list sizes");
        // Example 2: capacity 1.
        Cache d = new Cache(1);
        if (d.put(1, 1) != -1 || d.put(2, 2) != 1 || d.put(2, 3) != -1) throw new AssertionError("capacity one puts");
        if (d.get(1) != -1 || d.get(2) != 3) throw new AssertionError("capacity one gets");
        // Random scripts: results and the map/list size match after every call.
        Random rnd = new Random(3305);
        for (int round = 0; round < 300; round++) {
            int cap = 1 + rnd.nextInt(5);
            Cache cache = new Cache(cap);
            Model model = new Model(cap);
            for (int step = 0; step < 200; step++) {
                int key = rnd.nextInt(9), val = rnd.nextInt(1000);
                if (rnd.nextBoolean()) {
                    if (cache.put(key, val) != model.put(key, val)) throw new AssertionError("put result");
                } else {
                    if (cache.get(key) != model.get(key)) throw new AssertionError("get result");
                }
                // The synchronization invariant: map entries, list nodes and the model agree.
                if (cache.mapSize() != cache.listLength()) throw new AssertionError("map size differs from list length");
                if (cache.mapSize() != model.items.size()) throw new AssertionError("size differs from model");
            }
        }
    }
}
```
