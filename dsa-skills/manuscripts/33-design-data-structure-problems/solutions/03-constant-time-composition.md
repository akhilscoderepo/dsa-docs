<!-- solutions-for: 03-constant-time-composition -->
### Solutions For Paired Structures

#### Solution: [Build] Map To List Node (Author exercise)
<!-- id: ds-map-list-node -->

**Approach.**

The map stores the node of every key, so `detach` finds the node in O(1) on average and never walks the list. The invariant is that the map contains the keys reachable from the head and no others, and that the `next` and `prev` links agree with each other. Detaching a node rewrites the link of its previous neighbor, or the head when there is none. It then rewrites the link of its next neighbor, or the tail when there is none. The method returns the key of the next neighbor, which makes the rewritten link observable. The detached key leaves the map in the same call. Iterating over `nodeOf.keySet()` while detaching throws `ConcurrentModificationException`, so any loop over keys works on a copy.

**Complexity.**

- **Time** is O(1) on average for `append` and `detach`, because each does a constant number of hash lookups and link writes.
- **Space** is O(n) for n live keys, because each key owns one node and one map entry.

```java run
import java.util.ArrayList;
import java.util.ConcurrentModificationException;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Random;

public final class MapToListNode {
    private static final class Node {
        final int key;
        Node prev, next;
        Node(int key) { this.key = key; }
    }

    private final Map<Integer, Node> nodeOf = new HashMap<>();
    private Node head, tail;

    /**
     * Adds the key at the tail; returns false when it already exists.
     * Time: O(1) average. Space: O(1) for one node and one map entry.
     * Invariant: nodeOf holds exactly the keys reachable from head.
     */
    boolean append(int key) {
        // A present key must not get a second node, or the map would lose the first one.
        if (nodeOf.containsKey(key)) return false;
        Node n = new Node(key);
        // The new node points back at the old tail.
        n.prev = tail;
        // An empty list makes the node the head; otherwise the old tail links forward to it.
        if (tail == null) head = n; else tail.next = n;
        tail = n;
        // Record the node so a later detach finds it without walking.
        nodeOf.put(key, n);
        return true;
    }

    /**
     * Unlinks the node of the key; returns the key after it, or -1 when it was the tail.
     * Time: O(1) average. Space: O(1).
     * Invariant: after the call, the neighbors of the removed node link to each other.
     */
    int detach(int key) {
        // Removing the entry from the map is the O(1) lookup that replaces a walk.
        Node n = nodeOf.remove(key);
        if (n == null) throw new IllegalArgumentException("absent key " + key);
        // The previous side: the head moves forward when there is no previous node.
        if (n.prev == null) head = n.next; else n.prev.next = n.next;
        // The next side: the tail moves back when there is no next node.
        if (n.next == null) tail = n.prev; else n.next.prev = n.prev;
        // The returned key shows which neighbor now follows the gap.
        return n.next == null ? -1 : n.next.key;
    }

    /** Returns the keys from head to tail. Time: O(n). Space: O(n) for the result. */
    List<Integer> order() {
        List<Integer> out = new ArrayList<>();
        // Walk forward through next links; the loop visits each live node once.
        for (Node n = head; n != null; n = n.next) out.add(n.key);
        return out;
    }

    /** Returns the keys from tail to head. Time: O(n). Space: O(n) for the result. */
    List<Integer> orderBackward() {
        List<Integer> out = new ArrayList<>();
        // Walk backward through prev links to prove both link directions agree.
        for (Node n = tail; n != null; n = n.prev) out.add(0, n.key);
        return out;
    }

    int mapSize() { return nodeOf.size(); }

    public static void main(String[] args) {
        // Example 1: detach from the middle returns the next key.
        MapToListNode a = new MapToListNode();
        for (int k : new int[] {5, 9, 2, 7}) a.append(k);
        if (a.detach(9) != 2) throw new AssertionError("example 1 return");
        if (!a.order().equals(List.of(5, 2, 7))) throw new AssertionError("example 1 order");
        // Example 2: a single node leaves the list empty, and the list still accepts appends.
        MapToListNode b = new MapToListNode();
        b.append(4);
        if (b.detach(4) != -1) throw new AssertionError("example 2 return");
        if (!b.order().isEmpty()) throw new AssertionError("example 2 empty");
        b.append(6);
        if (!b.order().equals(List.of(6))) throw new AssertionError("example 2 reuse");
        // Duplicates are rejected and an absent key throws.
        if (a.append(5)) throw new AssertionError("duplicate append");
        boolean threw = false;
        try { a.detach(1234); } catch (IllegalArgumentException e) { threw = true; }
        if (!threw) throw new AssertionError("absent key");
        // Java claim: removing from a map while iterating its keys throws.
        Map<Integer, Integer> m = new HashMap<>(Map.of(1, 1, 2, 2, 3, 3));
        boolean cme = false;
        try { for (int k : m.keySet()) m.remove(k); } catch (ConcurrentModificationException e) { cme = true; }
        if (!cme) throw new AssertionError("map mutation during iteration must throw");
        // Random replay against a plain list model.
        Random rnd = new Random(33);
        MapToListNode s = new MapToListNode();
        List<Integer> model = new ArrayList<>();
        for (int step = 0; step < 20000; step++) {
            if (model.isEmpty() || rnd.nextInt(100) < 55) {
                int k = rnd.nextInt(300);
                boolean expect = !model.contains(k);
                if (s.append(k) != expect) throw new AssertionError("append flag");
                if (expect) model.add(k);
            } else {
                int k = model.get(rnd.nextInt(model.size()));
                int at = model.indexOf(k);
                int expectNext = at == model.size() - 1 ? -1 : model.get(at + 1);
                if (s.detach(k) != expectNext) throw new AssertionError("detach return");
                model.remove(at);
            }
            if (!s.order().equals(model) || !s.orderBackward().equals(model)) throw new AssertionError("order");
            if (s.mapSize() != model.size()) throw new AssertionError("map size");
        }
    }
}
```

#### Solution: [Vary] Map To Array Index (Author exercise)
<!-- id: ds-map-array-index -->

**Approach.**

The caller names a position, so the removed key comes straight from the array and the map is not needed to find it. The map matters only for the key that moves. The method copies the final key into position `i`, so the removal costs O(1) instead of a shift of the tail. The moved key now sits at position `i`, so `put(last, i)` repairs its entry. The removed key's entry is deleted after that, which also handles the case where `i` is the final position. The array then drops its final slot using the index form of `remove`. The returned value is the moved key, or -1 when the removed key was the final one.

**Complexity.**

- **Time** is O(1) on average, because the method does one array read, one array write, two map updates and one tail removal.
- **Space** is O(n) for n keys, because the array and the map each hold one record per key.

```java run
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Random;

public final class MapToArrayIndex {
    private final List<Integer> keys = new ArrayList<>();
    private final Map<Integer, Integer> slots = new HashMap<>();

    /**
     * Appends the key; returns false when it exists.
     * Time: O(1) amortized. Space: O(1) per key.
     * Invariant: slots.get(k) equals the position of k in keys.
     */
    boolean add(int key) {
        if (slots.containsKey(key)) return false;
        // Record the slot before the append, because the slot equals the old size.
        slots.put(key, keys.size());
        keys.add(key);
        return true;
    }

    /**
     * Removes the key at position i by moving the final key into it; returns the moved key or -1.
     * Time: O(1) average. Space: O(1).
     * Invariant: after the call, every remaining key maps to its true position.
     */
    int removeAt(int i) {
        // Reject positions outside the live range before touching any state.
        if (i < 0 || i >= keys.size()) throw new IndexOutOfBoundsException("position " + i);
        int removed = keys.get(i);
        int lastPos = keys.size() - 1;
        int last = keys.get(lastPos);
        // Overwrite the freed slot with the final key; no tail shift happens.
        keys.set(i, last);
        // Repair the moved key first, so its entry names the new position.
        slots.put(last, i);
        // Delete the removed key last; when removed equals last this drops the repair write.
        slots.remove(removed);
        // The int argument removes by position, which is O(1) at the end of the list.
        keys.remove(lastPos);
        return removed == last ? -1 : last;
    }

    /** Returns the position of the key, or -1 when absent. Time: O(1) average. Space: O(1). */
    int slotOf(int key) {
        Integer s = slots.get(key);
        return s == null ? -1 : s;
    }

    List<Integer> keys() { return keys; }

    public static void main(String[] args) {
        // Example 1: removing position 1 moves the final key 25 into it.
        MapToArrayIndex a = new MapToArrayIndex();
        for (int k : new int[] {30, 11, 64, 25}) a.add(k);
        if (a.removeAt(1) != 25) throw new AssertionError("example 1 return");
        if (!a.keys().equals(List.of(30, 25, 64))) throw new AssertionError("example 1 keys");
        if (a.slotOf(25) != 1 || a.slotOf(11) != -1) throw new AssertionError("example 1 slots");
        // Example 2: a single key leaves the structure empty and reusable.
        MapToArrayIndex b = new MapToArrayIndex();
        b.add(30);
        if (b.removeAt(0) != -1 || !b.keys().isEmpty()) throw new AssertionError("example 2");
        if (!b.add(30)) throw new AssertionError("example 2 reuse");
        // Out-of-range positions throw.
        boolean threw = false;
        try { b.removeAt(1); } catch (IndexOutOfBoundsException e) { threw = true; }
        if (!threw) throw new AssertionError("range check");
        // Random replay against a list model that shifts on removal and then swaps by hand.
        Random rnd = new Random(34);
        MapToArrayIndex s = new MapToArrayIndex();
        List<Integer> model = new ArrayList<>();
        for (int step = 0; step < 20000; step++) {
            if (model.isEmpty() || rnd.nextInt(100) < 55) {
                int k = rnd.nextInt(400);
                boolean expect = !model.contains(k);
                if (s.add(k) != expect) throw new AssertionError("add flag");
                if (expect) model.add(k);
            } else {
                int i = rnd.nextInt(model.size());
                int fin = model.remove(model.size() - 1);
                int expect = -1;
                if (i < model.size()) { model.set(i, fin); expect = fin; }
                if (s.removeAt(i) != expect) throw new AssertionError("removeAt return");
            }
            if (!s.keys().equals(model)) throw new AssertionError("keys");
            for (int p = 0; p < model.size(); p++)
                if (s.slotOf(model.get(p)) != p) throw new AssertionError("slot of " + model.get(p));
            if (s.slots.size() != model.size()) throw new AssertionError("stale map entry");
        }
    }
}
```

#### Solution: [Boundary] Remove Last Element (Author exercise)
<!-- id: ds-remove-last-slot -->

**Approach.**

The invariant is that the map contains one entry per stored key, and each entry names the true position. A removal by swap with last moves the final key onto the freed slot. When the removed key is the final key, the move copies the key onto itself. The moved key and the removed key are then the same key, so the order of the two map updates decides the result. Repairing first and deleting second leaves the key out of the map, which is correct. Deleting first and repairing second writes the removed key back, and the map keeps an entry for a position that no longer exists. The solution below holds both orders in one class so the assertions can compare them. The faulty order passes every case where the removed key is not last, which is why a test must cover the last position directly.

**Complexity.**

- **Time** is O(1) on average, because each removal does a constant number of map and list operations.
- **Space** is O(n) for n keys, because the list and the map each hold one record per key.

```java run
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Random;

public final class RemoveLastElement {
    private final List<Integer> keys = new ArrayList<>();
    private final Map<Integer, Integer> slots = new HashMap<>();

    boolean add(int key) {
        if (slots.containsKey(key)) return false;
        slots.put(key, keys.size());
        keys.add(key);
        return true;
    }

    /**
     * Removes the key by moving the final key into its slot; returns false when absent.
     * Time: O(1) average. Space: O(1).
     * Invariant: slots has one correct entry per key and no other entry.
     */
    boolean removeKey(int key) {
        Integer slot = slots.get(key);
        // An absent key changes nothing.
        if (slot == null) return false;
        int last = keys.get(keys.size() - 1);
        // Move the final key into the freed slot; when key equals last this writes it onto itself.
        keys.set(slot, last);
        // Repair first, then delete: the delete must be the final write to the map.
        slots.put(last, slot);
        slots.remove(key);
        keys.remove(keys.size() - 1);
        return true;
    }

    /** Faulty order kept for comparison: it deletes first, so removing the final key leaves a stale entry. */
    boolean removeKeyFaulty(int key) {
        Integer slot = slots.get(key);
        if (slot == null) return false;
        int last = keys.get(keys.size() - 1);
        keys.set(slot, last);
        slots.remove(key);
        // When key equals last, this write puts the removed key back into the map.
        slots.put(last, slot);
        keys.remove(keys.size() - 1);
        return true;
    }

    int slotOf(int key) {
        Integer s = slots.get(key);
        return s == null ? -1 : s;
    }

    int size() { return keys.size(); }
    int mapSize() { return slots.size(); }
    List<Integer> keys() { return keys; }

    public static void main(String[] args) {
        // Example 1: removing the final key leaves no stale entry.
        RemoveLastElement a = new RemoveLastElement();
        for (int k : new int[] {8, 3, 6}) a.add(k);
        if (!a.removeKey(6) || !a.keys().equals(List.of(8, 3))) throw new AssertionError("example 1 keys");
        if (a.slotOf(6) != -1 || a.mapSize() != 2) throw new AssertionError("example 1 map");
        // Example 2: a middle removal moves 6 into slot 1, and an absent key returns false.
        RemoveLastElement b = new RemoveLastElement();
        for (int k : new int[] {8, 3, 6}) b.add(k);
        b.removeKey(3);
        if (!b.keys().equals(List.of(8, 6)) || b.slotOf(6) != 1 || b.mapSize() != 2) throw new AssertionError("example 2");
        if (b.removeKey(9)) throw new AssertionError("absent key");
        // The faulty order keeps an entry for the removed final key.
        RemoveLastElement f = new RemoveLastElement();
        for (int k : new int[] {8, 3, 6}) f.add(k);
        f.removeKeyFaulty(6);
        if (f.mapSize() != 3 || f.size() != 2) throw new AssertionError("faulty order must leave a stale entry");
        // The faulty order is correct when the removed key is not last, so only a last-slot test exposes it.
        RemoveLastElement g = new RemoveLastElement();
        for (int k : new int[] {8, 3, 6}) g.add(k);
        g.removeKeyFaulty(8);
        if (g.mapSize() != g.size()) throw new AssertionError("middle removal is fine in both orders");
        // Random replay against a list model; the map size must equal the list size after every call.
        Random rnd = new Random(35);
        RemoveLastElement s = new RemoveLastElement();
        List<Integer> model = new ArrayList<>();
        for (int step = 0; step < 20000; step++) {
            int k = rnd.nextInt(60);
            if (rnd.nextInt(100) < 50) {
                boolean expect = !model.contains(k);
                if (s.add(k) != expect) throw new AssertionError("add flag");
                if (expect) model.add(k);
            } else {
                int at = model.indexOf(k);
                if (s.removeKey(k) != (at >= 0)) throw new AssertionError("remove flag");
                if (at >= 0) {
                    int fin = model.remove(model.size() - 1);
                    if (at < model.size()) model.set(at, fin);
                }
            }
            if (!s.keys().equals(model) || s.mapSize() != s.size()) throw new AssertionError("state");
            for (int p = 0; p < model.size(); p++)
                if (s.slotOf(model.get(p)) != p) throw new AssertionError("slot");
        }
    }
}
```

#### Solution: [Recognize] Insert Delete GetRandom O(1) With Positions (LeetCode 380)
<!-- id: ds-indexed-set-contract -->

**Approach.**

The contract needs membership, insertion, removal and position reads, all in O(1). A hash map answers membership and finds a value's position. A list answers `getAt` and supports append and tail removal. Every value in the list has exactly one map entry that names its position, and that fact is the invariant. Insertion records the position before the append. Removal looks up the position, copies the final value into it, repairs the moved value's entry and then deletes the removed value's entry. That order keeps the map correct when the removed value is last. The return value of `remove` is the moved value, or -1 when the value was absent or last, so a wrong repair shows up in later `getAt` calls. Slots read from the map are boxed `Integer` objects, and `==` on two boxed values above 127 compares object identity, so the code unboxes to `int` before any comparison.

**Complexity.**

- **Time** is O(1) on average for every operation, because each does a constant number of hash and list operations at the tail or at one position.
- **Space** is O(n) for n values, because the list and the map each hold one record per value.

```java run
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Random;

public final class IndexedSet {
    private final List<Integer> values = new ArrayList<>();
    private final Map<Integer, Integer> slotOf = new HashMap<>();

    /**
     * Adds v at the next free position; returns false when present.
     * Time: O(1) amortized. Space: O(1) per value.
     * Invariant: slotOf.get(v) equals the position of v in values.
     */
    boolean insert(int v) {
        // A present value keeps its position and its entry.
        if (slotOf.containsKey(v)) return false;
        // The new position equals the size before the append.
        slotOf.put(v, values.size());
        values.add(v);
        return true;
    }

    /**
     * Deletes v and returns the value that moved into its position, or -1 when none moved.
     * Time: O(1) average. Space: O(1).
     * Invariant: after the call, every remaining value maps to its true position.
     */
    int remove(int v) {
        Integer boxed = slotOf.get(v);
        // Absent values change nothing and move nothing.
        if (boxed == null) return -1;
        // Unbox once so no later comparison uses object identity.
        int slot = boxed;
        int last = values.get(values.size() - 1);
        // Swap with last: the final value fills the freed position.
        values.set(slot, last);
        // Repair the moved value's entry, then delete the removed value's entry.
        slotOf.put(last, slot);
        slotOf.remove(v);
        // The int argument drops the final position without searching.
        values.remove(values.size() - 1);
        return last == v ? -1 : last;
    }

    /** Returns the value at position i. Time: O(1). Space: O(1). */
    int getAt(int i) {
        if (i < 0 || i >= values.size()) throw new IndexOutOfBoundsException("position " + i);
        return values.get(i);
    }

    int size() { return values.size(); }

    public static void main(String[] args) {
        // Example 1: removing 5 moves the final value 9 into position 1.
        IndexedSet a = new IndexedSet();
        for (int v : new int[] {12, 5, 30, 9}) a.insert(v);
        if (a.remove(5) != 9 || a.getAt(1) != 9 || a.size() != 3) throw new AssertionError("example 1");
        // Example 2: a duplicate insert, a last-position removal and an absent removal.
        IndexedSet b = new IndexedSet();
        b.insert(7);
        b.insert(2);
        if (b.insert(7)) throw new AssertionError("duplicate");
        if (b.remove(2) != -1) throw new AssertionError("last removal");
        if (b.remove(99) != -1) throw new AssertionError("absent removal");
        if (b.getAt(0) != 7 || b.size() != 1) throw new AssertionError("example 2 state");
        // Out-of-range reads throw.
        boolean threw = false;
        try { b.getAt(1); } catch (IndexOutOfBoundsException e) { threw = true; }
        if (!threw) throw new AssertionError("range check");
        // Java claim: boxed Integers above 127 are not guaranteed identical, so == is unsafe; equals is safe.
        Integer x = Integer.valueOf(127), y = Integer.valueOf(127);
        Integer p = Integer.valueOf(1000), q = Integer.valueOf(1000);
        if (x != y) throw new AssertionError("small boxed values are cached");
        if (p == q) throw new AssertionError("large boxed values are separate objects");
        if (!p.equals(q)) throw new AssertionError("equals compares values");
        // Random replay against a list model; values above 127 exercise the boxed comparison.
        Random rnd = new Random(36);
        IndexedSet s = new IndexedSet();
        List<Integer> model = new ArrayList<>();
        for (int step = 0; step < 20000; step++) {
            int v = rnd.nextInt(600);
            if (rnd.nextInt(100) < 50) {
                boolean expect = !model.contains(v);
                if (s.insert(v) != expect) throw new AssertionError("insert flag");
                if (expect) model.add(v);
            } else {
                int at = model.indexOf(v);
                int expect = -1;
                if (at >= 0) {
                    int fin = model.remove(model.size() - 1);
                    if (at < model.size()) { model.set(at, fin); expect = fin; }
                }
                if (s.remove(v) != expect) throw new AssertionError("remove return");
            }
            if (s.size() != model.size()) throw new AssertionError("size");
            for (int i = 0; i < model.size(); i++)
                if (s.getAt(i) != model.get(i)) throw new AssertionError("getAt " + i);
        }
    }
}
```
