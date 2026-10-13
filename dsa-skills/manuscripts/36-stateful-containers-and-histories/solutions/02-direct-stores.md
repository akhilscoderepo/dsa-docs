<!-- solutions-for: 02-direct-stores -->
### Solutions For Direct Slots

#### Solution: [Build] Boolean Direct Set (Author exercise)
<!-- id: sc-direct-boolean-set -->

**Approach.**
The class allocates one boolean per key of the domain, so key `k` owns array position `k` and no other position. An add reads the position first and writes `true` only when it was `false`, which gives the required report of a new key. A remove mirrors that rule. Every method first checks that the key lies inside the domain, because an unchecked index would either throw an unrelated array exception or, for a negative key, read the wrong position by accident.

The invariant is that `present[k]` is true exactly when key `k` is stored, and each call writes at most the single position that the key names. No call reads or writes a second position, so a repeated add or a removal of an absent key leaves the array unchanged.

**Complexity.**
- **Time** is O(1) per call, because each method reads or writes one array position after one range check.
- **Space** is O(D) for domain size `D`, because the array holds one boolean per possible key whether or not the key is stored.

```java run
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Random;
import java.util.Set;

public final class DirectSetBuild {
    /** Set over the keys 0..domain-1 with one boolean per key. Invariant: present[k] is true iff k is stored. */
    static final class DirectSet {
        // One entry per key of the domain; the key is its own index.
        private final boolean[] present;

        /**
         * Creates an empty set for the given domain size.
         * Time: O(D), because the array is zero-filled. Space: O(D).
         * Invariant: every entry starts false.
         */
        DirectSet(int domain) {
            // The allocation is the only linear-cost step of the class.
            present = new boolean[domain];
        }

        /**
         * Rejects keys outside the domain so that the array index is always valid.
         * Time: O(1). Space: O(1).
         * Invariant: afterwards 0 <= key < present.length.
         */
        private void check(int key) {
            // Both bounds are tested, because a negative key would otherwise raise an array exception with a different type.
            if (key < 0 || key >= present.length) throw new IllegalArgumentException("key " + key);
        }

        /**
         * Adds the key and reports whether it was absent.
         * Time: O(1). Space: O(1).
         * Invariant: only present[key] can change.
         */
        boolean add(int key) {
            // Validate before touching the array.
            check(key);
            // A stored key stays as it is, and the call reports that nothing was added.
            if (present[key]) return false;
            // The key owns this one position, so a single write stores it.
            present[key] = true;
            // The caller learns that the set grew.
            return true;
        }

        /**
         * Removes the key and reports whether it was present.
         * Time: O(1). Space: O(1).
         * Invariant: only present[key] can change.
         */
        boolean remove(int key) {
            // Validate before touching the array.
            check(key);
            // An absent key needs no write.
            if (!present[key]) return false;
            // Clearing the owned position removes the key.
            present[key] = false;
            // The caller learns that the set shrank.
            return true;
        }

        /**
         * Tests membership.
         * Time: O(1). Space: O(1).
         * Invariant: the call changes nothing.
         */
        boolean contains(int key) {
            // Validate, then read the single owned position.
            check(key);
            return present[key];
        }
    }

    /**
     * Applies one random call to both the direct set and the oracle and compares the results.
     * Time: O(1) per call. Space: O(1).
     * Invariant: after every call the two sets hold the same keys.
     */
    static void step(DirectSet s, Set<Integer> oracle, Random rnd, int domain) {
        // Keys range slightly past the domain so that the range check is exercised.
        int key = rnd.nextInt(domain + 3) - 1;
        int op = rnd.nextInt(3);
        boolean inside = key >= 0 && key < domain;
        try {
            // Each branch compares the answer of the direct set with the answer of java.util.HashSet.
            boolean got = op == 0 ? s.add(key) : op == 1 ? s.remove(key) : s.contains(key);
            if (!inside) throw new AssertionError("expected a throw for " + key);
            boolean want = op == 0 ? oracle.add(key) : op == 1 ? oracle.remove(key) : oracle.contains(key);
            if (got != want) throw new AssertionError("answer differs for op " + op + " key " + key);
        } catch (IllegalArgumentException e) {
            // Only out-of-domain keys may throw.
            if (inside) throw new AssertionError("unexpected throw for " + key);
        }
    }

    public static void main(String[] args) {
        // Example 1 from the exercise: duplicate add and absent remove.
        DirectSet a = new DirectSet(10);
        boolean[] got = {a.add(4), a.add(4), a.contains(4), a.remove(4), a.remove(4), a.contains(4)};
        boolean[] want = {true, false, true, true, false, false};
        for (int i = 0; i < want.length; i++) if (got[i] != want[i]) throw new AssertionError("example 1 call " + i);
        // Example 2: domain edges and the first key outside the domain.
        DirectSet b = new DirectSet(3);
        if (!b.add(0) || b.contains(2) || !b.add(2) || !b.remove(0) || b.contains(0)) throw new AssertionError("example 2");
        boolean threw = false;
        try { b.add(3); } catch (IllegalArgumentException e) { threw = true; }
        if (!threw) throw new AssertionError("add(3) must throw");
        // A negative key also throws, which a bare array access would report as a different exception type.
        threw = false;
        try { b.contains(-1); } catch (IllegalArgumentException e) { threw = true; }
        if (!threw) throw new AssertionError("negative key must throw");
        // List.remove(int) deletes by index while remove(Object) deletes by value, which is why the list version casts.
        List<Integer> list = new ArrayList<>(List.of(40, 7, 19));
        list.remove(1);
        if (!list.equals(List.of(40, 19))) throw new AssertionError("remove by index");
        list.remove((Integer) 19);
        if (!list.equals(List.of(40))) throw new AssertionError("remove by value");
        // Random sequences compared with the library set, over several domain sizes.
        Random rnd = new Random(3602L);
        for (int t = 0; t < 300; t++) {
            int domain = 1 + rnd.nextInt(12);
            DirectSet s = new DirectSet(domain);
            Set<Integer> oracle = new HashSet<>();
            for (int c = 0; c < 60; c++) step(s, oracle, rnd, domain);
        }
    }
}
```

#### Solution: [Vary] Design HashSet (LeetCode 705)
<!-- id: sc-bucketed-hash-set -->

**Approach.**
The set keeps an array of bucket heads and a hash function `key % B`. Every key belongs to the one chain that the function names, and the chain stores nodes in arrival order with new nodes at the head. The add method first searches only that chain, so a stored key is never inserted twice. The remove method walks the same chain with a `prev` reference. When the match is the head, the array entry moves to the next node. Otherwise the previous node skips the match.

The invariant is that every stored key appears in exactly one node, inside the chain of bucket `key % B`, and no chain holds a repeated key. Two keys that collide only share a chain, so removing one leaves the other reachable, which the tests below check with a tiny bucket count that forces many collisions. The memory depends on `B` and on the number of stored keys, not on the key range.

**Complexity.**
- **Time** is O(1 + n / B) expected per call and O(n) in the worst case, because a call walks one chain whose length averages `n / B`.
- **Space** is O(B + n), because the array has `B` entries and each stored key owns one node.

```java run
import java.util.HashSet;
import java.util.Random;
import java.util.Set;

public final class BucketSetVary {
    /** Chained set over non-negative int keys. Invariant: key k appears once, in the chain of bucket k % B. */
    static final class MyHashSet {
        // One chain node holds one key and the reference to the next node.
        private static final class Node {
            final int key;
            Node next;
            Node(int key, Node next) { this.key = key; this.next = next; }
        }

        // buckets[b] is the head of chain b, or null for an empty chain.
        private final Node[] buckets;

        /**
         * Creates an empty set with the given number of buckets.
         * Time: O(B). Space: O(B).
         * Invariant: every chain starts empty.
         */
        MyHashSet(int bucketCount) {
            buckets = new Node[bucketCount];
        }

        /**
         * Maps a key to its only bucket.
         * Time: O(1). Space: O(1).
         * Invariant: equal keys always return the same index, and the index is in 0..B-1 for non-negative keys.
         */
        private int bucketOf(int key) {
            // The remainder is deterministic, so the key always returns to this bucket.
            return key % buckets.length;
        }

        /**
         * Tests membership by walking one chain.
         * Time: O(1 + n / B) expected, O(n) worst case. Space: O(1).
         * Invariant: only the chain of bucketOf(key) is read.
         */
        boolean contains(int key) {
            // Start at the head of the owning chain and move node by node.
            for (Node n = buckets[bucketOf(key)]; n != null; n = n.next) {
                // Keys compare by value, because two different keys can share this chain.
                if (n.key == key) return true;
            }
            // The chain ended without a match, and no other bucket can hold the key.
            return false;
        }

        /**
         * Adds the key unless it is stored.
         * Time: O(1 + n / B) expected. Space: O(1) extra, one node when the key is new.
         * Invariant: no chain holds a repeated key afterwards.
         */
        void add(int key) {
            // The search also guards against duplicates.
            if (contains(key)) return;
            int b = bucketOf(key);
            // The new node points at the old head and then becomes the head, so the old chain stays intact.
            buckets[b] = new Node(key, buckets[b]);
        }

        /**
         * Removes the key if it is stored.
         * Time: O(1 + n / B) expected. Space: O(1).
         * Invariant: only the chain of bucketOf(key) can change, and only by dropping one node.
         */
        void remove(int key) {
            int b = bucketOf(key);
            // prev trails the current node so the walk can unlink it.
            Node prev = null;
            for (Node n = buckets[b]; n != null; prev = n, n = n.next) {
                // Skip nodes that hold other keys of this bucket.
                if (n.key != key) continue;
                // A head match moves the array entry; any other match is skipped by the previous node.
                if (prev == null) buckets[b] = n.next; else prev.next = n.next;
                // The key is unique in the chain, so the walk ends here.
                return;
            }
        }
    }

    public static void main(String[] args) {
        // Example 1: add, query, remove, query.
        MyHashSet s = new MyHashSet(769);
        s.add(5); s.add(9);
        if (!s.contains(5) || s.contains(6)) throw new AssertionError("example 1 before remove");
        s.remove(5);
        if (s.contains(5)) throw new AssertionError("example 1 after remove");
        // Example 2: 3 and 772 collide with 769 buckets, and removing the older one keeps the other reachable.
        if (3 % 769 != 772 % 769) throw new AssertionError("hash function");
        MyHashSet c = new MyHashSet(769);
        c.add(3); c.add(772); c.remove(3);
        if (!c.contains(772) || c.contains(3)) throw new AssertionError("example 2");
        // Removing a head, a middle and a tail node of one chain in turn, with a single bucket.
        MyHashSet one = new MyHashSet(1);
        for (int k = 1; k <= 4; k++) one.add(k);
        one.remove(4); one.remove(2); one.remove(1);
        if (one.contains(4) || one.contains(2) || one.contains(1) || !one.contains(3)) throw new AssertionError("chain positions");
        // Random comparison with the library set; tiny bucket counts force heavy collisions.
        Random rnd = new Random(3605L);
        for (int t = 0; t < 400; t++) {
            int buckets = 1 + rnd.nextInt(5);
            MyHashSet mine = new MyHashSet(buckets);
            Set<Integer> oracle = new HashSet<>();
            for (int c2 = 0; c2 < 80; c2++) {
                // Keys include the maximum value 10^6 and small values that share buckets.
                int key = rnd.nextInt(3) == 0 ? 1_000_000 - rnd.nextInt(3) : rnd.nextInt(12);
                int op = rnd.nextInt(3);
                if (op == 0) { mine.add(key); oracle.add(key); }
                else if (op == 1) { mine.remove(key); oracle.remove(key); }
                else if (mine.contains(key) != oracle.contains(key)) throw new AssertionError("contains " + key);
            }
        }
    }
}
```

#### Solution: [Boundary] Design HashMap (LeetCode 706)
<!-- id: sc-map-absent-update -->

**Approach.**
The map uses the same array of chains as the set, but each node also stores a value. The private `find` method returns the node for a key or `null`, so the code separates "no node" from "a node whose value is 0". A put calls `find` first. When a node exists, the call overwrites that node's value and leaves the chain shape alone. When no node exists, the call links a new node at the head. A get returns `-1` only when `find` returns `null`, and a stored 0 is returned as 0.

The invariant is that each key has at most one node and that node sits in the chain of its own bucket. A second put never creates a second node, so a later remove deletes the only copy and a later get cannot see an old value. The `size` field changes only when a node is created or unlinked, and the tests compare it with the library map after every call.

**Complexity.**
- **Time** is O(1 + n / B) expected per call and O(n) in the worst case, because every call walks one chain.
- **Space** is O(B + n), because the array has `B` entries and each stored pair owns one node.

```java run
import java.util.HashMap;
import java.util.Map;
import java.util.Random;

public final class HashMapBoundary {
    /** Chained map from non-negative int keys to non-negative int values. Invariant: one node per stored key, in bucket key % B. */
    static final class MyHashMap {
        // A node holds the key, its current value and the next node of the chain.
        private static final class Node {
            final int key;
            int value;
            Node next;
            Node(int key, int value, Node next) { this.key = key; this.value = value; this.next = next; }
        }

        // buckets[b] is the head of chain b.
        private final Node[] buckets;
        // size counts nodes and changes only when a node is created or unlinked.
        private int size;

        /**
         * Creates an empty map with the given number of buckets.
         * Time: O(B). Space: O(B).
         * Invariant: size is 0 and every chain is empty.
         */
        MyHashMap(int bucketCount) {
            buckets = new Node[bucketCount];
        }

        /**
         * Finds the node of a key.
         * Time: O(1 + n / B) expected. Space: O(1).
         * Invariant: returns null exactly when the key is absent, whatever values are stored.
         */
        private Node find(int key) {
            // Walk only the chain of the key's bucket.
            for (Node n = buckets[key % buckets.length]; n != null; n = n.next) {
                // Compare by key value; a node with value 0 is still a node.
                if (n.key == key) return n;
            }
            // The chain ended, so the key has no node.
            return null;
        }

        /**
         * Stores a pair, replacing the value of an existing key in place.
         * Time: O(1 + n / B) expected. Space: O(1) extra, one node when the key is new.
         * Invariant: the key has exactly one node afterwards.
         */
        void put(int key, int value) {
            Node n = find(key);
            // An existing node is updated in place, so size and chain shape stay the same.
            if (n != null) { n.value = value; return; }
            int b = key % buckets.length;
            // A new node becomes the chain head, and size grows with it.
            buckets[b] = new Node(key, value, buckets[b]);
            size++;
        }

        /**
         * Reads a value.
         * Time: O(1 + n / B) expected. Space: O(1).
         * Invariant: the result is -1 only when the key is absent, because stored values are never negative.
         */
        int get(int key) {
            Node n = find(key);
            // Only a missing node maps to -1; a stored 0 is returned as 0.
            return n == null ? -1 : n.value;
        }

        /**
         * Removes a pair if it exists.
         * Time: O(1 + n / B) expected. Space: O(1).
         * Invariant: size drops by one exactly when a node is unlinked.
         */
        void remove(int key) {
            int b = key % buckets.length;
            // prev trails the walk so the matching node can be skipped.
            Node prev = null;
            for (Node n = buckets[b]; n != null; prev = n, n = n.next) {
                // Ignore other keys that share this bucket.
                if (n.key != key) continue;
                // Unlink at the head or in the middle of the chain.
                if (prev == null) buckets[b] = n.next; else prev.next = n.next;
                size--;
                return;
            }
        }

        /** Returns the number of stored pairs. Time: O(1). Space: O(1). Invariant: equals the number of nodes in all chains. */
        int size() { return size; }
    }

    public static void main(String[] args) {
        // Example 1: a stored 0 differs from an absent key, and a second put changes the value.
        MyHashMap m = new MyHashMap(769);
        m.put(2, 0);
        if (m.get(2) != 0 || m.get(5) != -1) throw new AssertionError("absent versus zero");
        m.put(2, 7);
        if (m.get(2) != 7 || m.size() != 1) throw new AssertionError("update in place");
        m.remove(2);
        if (m.get(2) != -1 || m.size() != 0) throw new AssertionError("after remove");
        // Example 2: 1 and 770 share a bucket; updating 1 and removing 1 leave 770 intact.
        if (1 % 769 != 770 % 769) throw new AssertionError("hash function");
        MyHashMap c = new MyHashMap(769);
        c.put(1, 1); c.put(770, 5); c.put(1, 9);
        if (c.get(770) != 5 || c.get(1) != 9 || c.size() != 2) throw new AssertionError("example 2 before remove");
        c.remove(1);
        if (c.get(770) != 5 || c.get(1) != -1) throw new AssertionError("example 2 after remove");
        // Removing an absent key changes nothing.
        c.remove(1);
        if (c.size() != 1) throw new AssertionError("remove absent");
        // Random comparison with the library map; few buckets force collisions and many updates of one key.
        Random rnd = new Random(3606L);
        for (int t = 0; t < 400; t++) {
            MyHashMap mine = new MyHashMap(1 + rnd.nextInt(5));
            Map<Integer, Integer> oracle = new HashMap<>();
            for (int i = 0; i < 80; i++) {
                int key = rnd.nextInt(4) == 0 ? 1_000_000 - rnd.nextInt(2) : rnd.nextInt(10);
                int op = rnd.nextInt(3);
                // Values include 0 and the maximum 10^6.
                int value = rnd.nextInt(3) == 0 ? 0 : rnd.nextInt(1_000_001);
                if (op == 0) { mine.put(key, value); oracle.put(key, value); }
                else if (op == 1) { mine.remove(key); oracle.remove(key); }
                else if (mine.get(key) != oracle.getOrDefault(key, -1)) throw new AssertionError("get " + key);
                if (mine.size() != oracle.size()) throw new AssertionError("size");
            }
        }
    }
}
```

#### Solution: [Recognize] Design Linked List (LeetCode 707)
<!-- id: sc-list-head-tail-size -->

**Approach.**
The list is a singly linked chain with three owning fields: `head` for the first node, `tail` for the last node and `size` for the node count. Positions replace hash keys, so a walk of `index - 1` steps finds the node before the position. Insertion at index 0 changes `head`, insertion at index `size` changes `tail`, and a middle insertion changes neither. Deletion mirrors that table. Removing index 0 moves `head`, removing the last node moves `tail` back to its predecessor, and removing the only node sets both to `null`.

The invariant is that `size` equals the number of nodes reachable from `head`, `tail` is the last of them, and `head` and `tail` are both `null` exactly when `size` is 0. Every public call restores that statement before it returns, and the test calls a checker after every operation. Invalid indexes return before any field changes, so a rejected call leaves the list as it was.

**Complexity.**
- **Time** is O(1) for `addAtHead` and `addAtTail`, and O(n) for `get`, `addAtIndex` and `deleteAtIndex`, because those three walk up to `n` nodes.
- **Space** is O(n), because each stored value owns one node and the three fields add O(1).

```java run
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public final class ListOwnership {
    /** Singly linked list. Invariant: size counts the nodes after head, tail is the last node, and head is null iff size is 0. */
    static final class MyLinkedList {
        // A node holds one value and the reference to its successor.
        private static final class Node {
            final int val;
            Node next;
            Node(int val) { this.val = val; }
        }

        private Node head, tail;
        private int size;

        /**
         * Returns the node at a valid position.
         * Time: O(index). Space: O(1).
         * Invariant: the caller has checked 0 <= index < size.
         */
        private Node nodeAt(int index) {
            Node n = head;
            // Each step moves one node along the chain, which is the source of the linear cost.
            for (int i = 0; i < index; i++) n = n.next;
            return n;
        }

        /**
         * Reads the value at a position.
         * Time: O(index). Space: O(1).
         * Invariant: the call changes nothing.
         */
        int get(int index) {
            // An invalid position reports -1 before any walk.
            if (index < 0 || index >= size) return -1;
            return nodeAt(index).val;
        }

        /**
         * Inserts a value at the front.
         * Time: O(1). Space: O(1).
         * Invariant: head, tail and size agree again on return.
         */
        void addAtHead(int val) {
            Node n = new Node(val);
            // The new node points at the old first node, which is null for an empty list.
            n.next = head;
            head = n;
            // An empty list makes the new node the last node as well.
            if (size == 0) tail = n;
            size++;
        }

        /**
         * Inserts a value at the back.
         * Time: O(1). Space: O(1).
         * Invariant: head, tail and size agree again on return.
         */
        void addAtTail(int val) {
            Node n = new Node(val);
            // An empty list has no last node to link from, so the new node is both ends.
            if (size == 0) head = n; else tail.next = n;
            tail = n;
            size++;
        }

        /**
         * Inserts a value so that it occupies the given position.
         * Time: O(index). Space: O(1).
         * Invariant: an invalid index changes no field.
         */
        void addAtIndex(int index, int val) {
            // Positions after the end and negative positions are ignored.
            if (index < 0 || index > size) return;
            // The two ends have their own methods because they update head or tail.
            if (index == 0) { addAtHead(val); return; }
            if (index == size) { addAtTail(val); return; }
            // A middle insertion links after the predecessor and changes neither head nor tail.
            Node prev = nodeAt(index - 1);
            Node n = new Node(val);
            n.next = prev.next;
            prev.next = n;
            size++;
        }

        /**
         * Removes the node at a position.
         * Time: O(index). Space: O(1).
         * Invariant: an invalid index changes no field, and the last removal clears head and tail together.
         */
        void deleteAtIndex(int index) {
            // Invalid positions are ignored.
            if (index < 0 || index >= size) return;
            if (index == 0) {
                // The second node, or null, becomes the first.
                head = head.next;
                // Deleting the only node leaves no last node.
                if (size == 1) tail = null;
            } else {
                Node prev = nodeAt(index - 1);
                Node gone = prev.next;
                // The predecessor skips the removed node.
                prev.next = gone.next;
                // Deleting the last node moves tail back to the predecessor.
                if (gone == tail) tail = prev;
            }
            size--;
        }

        /**
         * Checks the ownership invariant by walking the whole chain.
         * Time: O(n). Space: O(1).
         * Invariant: it reports a mismatch of size, head or tail and changes nothing.
         */
        void checkOwnership() {
            int count = 0;
            Node last = null;
            // Count reachable nodes and remember the final one.
            for (Node n = head; n != null; n = n.next) { count++; last = n; }
            if (count != size) throw new AssertionError("size " + size + " but " + count + " nodes");
            if (last != tail) throw new AssertionError("tail does not point at the last node");
            if ((head == null) != (size == 0)) throw new AssertionError("head and size disagree");
        }
    }

    public static void main(String[] args) {
        // Example 1: ends and a middle insertion, then a delete and a new tail.
        MyLinkedList a = new MyLinkedList();
        a.addAtHead(4); a.addAtTail(8); a.addAtIndex(1, 6);
        if (a.get(0) != 4 || a.get(1) != 6 || a.get(2) != 8) throw new AssertionError("example 1 list");
        a.deleteAtIndex(2);
        a.addAtTail(3);
        if (a.get(2) != 3 || a.get(1) != 6) throw new AssertionError("example 1 tail after delete");
        a.checkOwnership();
        // Example 2: invalid insert on an empty list, then emptying the list and appending again.
        MyLinkedList b = new MyLinkedList();
        b.addAtIndex(1, 5);
        if (b.get(0) != -1) throw new AssertionError("ignored insert");
        b.addAtIndex(0, 5);
        b.deleteAtIndex(0);
        b.checkOwnership();
        b.addAtTail(2);
        if (b.get(0) != 2) throw new AssertionError("append after emptying");
        b.checkOwnership();
        // Negative indexes are ignored by every indexed method.
        b.addAtIndex(-1, 9); b.deleteAtIndex(-1);
        if (b.get(-1) != -1 || b.get(0) != 2) throw new AssertionError("negative index");
        // Random comparison with ArrayList, checking the three fields after every call.
        Random rnd = new Random(3607L);
        for (int t = 0; t < 600; t++) {
            MyLinkedList mine = new MyLinkedList();
            List<Integer> oracle = new ArrayList<>();
            for (int i = 0; i < 60; i++) {
                int op = rnd.nextInt(5);
                // Indexes run from -1 to size + 1 so that both invalid sides occur.
                int idx = rnd.nextInt(oracle.size() + 3) - 1;
                int val = rnd.nextInt(1001);
                if (op == 0) { mine.addAtHead(val); oracle.add(0, val); }
                else if (op == 1) { mine.addAtTail(val); oracle.add(val); }
                else if (op == 2) { mine.addAtIndex(idx, val); if (idx >= 0 && idx <= oracle.size()) oracle.add(idx, val); }
                else if (op == 3) { mine.deleteAtIndex(idx); if (idx >= 0 && idx < oracle.size()) oracle.remove(idx); }
                else {
                    int want = idx >= 0 && idx < oracle.size() ? oracle.get(idx) : -1;
                    if (mine.get(idx) != want) throw new AssertionError("get " + idx);
                }
                mine.checkOwnership();
                if (mine.size != oracle.size()) throw new AssertionError("size");
            }
        }
    }
}
```
