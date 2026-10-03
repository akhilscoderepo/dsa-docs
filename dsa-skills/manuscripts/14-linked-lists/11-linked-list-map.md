<!-- lesson-kind: combination -->
<!-- lesson-id: linked-list-map -->
## Linked List Map

<!-- stage: context -->
### Duplicating A Museum Catalogue

A museum keeps its exhibits in a catalogue, and the entries are chained in tour order: each entry names the next entry on the tour. Every entry also carries a cross-reference to a related exhibit, and that related exhibit can be any entry in the catalogue, earlier or later, or the entry itself, or none. A touring show is about to leave, and the curator needs a complete duplicate of the catalogue to travel with it.

The duplicate has to be a catalogue of its own. When someone follows a cross-reference in the travelling copy, they must land on another entry of the travelling copy, never on an entry of the original, since the original stays at home and may be changed. The curator's assistant can copy one entry at a time, and the copy of an entry has the same title. What troubles the assistant is the cross-references: when an entry is copied, the copy of the related exhibit may not exist yet.

<!-- stage: contributions -->
### What Each Structure Brings

The linked list brings the order and the identity of the entries. Following the tour links visits every entry exactly once, and each entry is a distinct object that can be told apart from all others, however many entries share a title. This is what makes the next references of the copy easy: they follow the same order. By itself the list cannot answer the question that the cross-references ask, which is where the copy of an arbitrary entry lives. Finding it means walking the copy from the start, and doing that for every entry costs a walk each.

The hash map brings direct lookup. Given an original entry, it returns the copy of that entry in one step, whatever the position. By itself it has no order and no source of the entries to put into it, so something has to enumerate the originals, which is the job of the list. A map keyed by title also fails when titles repeat, so the key must be the entry itself.

The recognition cue is a structure in which nodes hold arbitrary references to other nodes, and a duplicate must reproduce the same shape using only its own nodes.

<!-- stage: naive -->
### Find Each Target By Counting Steps

A method that uses only the list finds each cross-reference target by counting how many steps it is from the first entry, then walks the same number of steps in the copy.

```java
final class CatalogueByCounting {
    static final class Entry {
        int title;
        Entry next, related;
        Entry(int title) { this.title = title; }
    }

    static Entry copy(Entry head) {
        Entry copyHead = null, copyTail = null;
        for (Entry e = head; e != null; e = e.next) {
            Entry c = new Entry(e.title);
            if (copyHead == null) copyHead = c; else copyTail.next = c;
            copyTail = c;
        }
        Entry original = head, duplicate = copyHead;
        while (original != null) {
            if (original.related != null) {
                int steps = 0;
                for (Entry e = head; e != original.related; e = e.next) steps++;
                Entry target = copyHead;
                for (int i = 0; i < steps; i++) target = target.next;
                duplicate.related = target;
            }
            original = original.next;
            duplicate = duplicate.next;
        }
        return copyHead;
    }
}
```

It is correct. The duplicate has the same titles in the same order, and every cross-reference points inside the duplicate.

<!-- stage: bottleneck -->
### A Walk For Every Cross-Reference

For each entry with a cross-reference the code walks from the head to find the target's position and then walks the copy to the same position, so a single cross-reference costs up to 2n steps. With n entries the total is O(n^2). A catalogue of a hundred thousand entries needs on the order of ten billion steps, where one pass over the catalogue should be enough.

The waste comes from forgetting what has already been seen. Every entry was visited when the copy was made, and at that moment its copy was created, so the pair of an original and its copy was known and then thrown away. If that pair had been recorded, the cross-reference would be a single lookup, and the problem of copies that do not exist yet would disappear if all copies were made before any cross-reference is wired. The remaining design question is the key: titles repeat, so any structure keyed by title confuses different entries, and the key has to be the identity of the original entry.

<!-- stage: insight -->
### Clone First, Wire Second

The combined state is an **identity map** from each original node to its clone, together with two passes over the list. The key is the node object itself, compared by reference, so two nodes with equal values are two keys. In the first pass, walk the originals in order, create a clone holding the same value for each one, and put the pair in the map. Nothing is linked yet. In the second pass, the **two-pass wiring**, walk the originals again and for each node `o` set `clone(o).next` to `map.get(o.next)` and `clone(o).random` to `map.get(o.random)`, leaving a reference null when the original's is null.

<!-- names: identity map, two-pass wiring, clone-first rule -->

The **clone-first rule** is what makes the second pass safe: every clone exists before any link is written, so each lookup finds a clone, whatever the target's position, including the node itself, an earlier node or a later one. The invariant after the first pass is that the map has exactly one entry per original and no clone has any link. The invariant after the second pass is that, for every original `o`, each reference of `clone(o)` is the clone of the node that `o` refers to, and so no reference of a clone leads back to an original.

Each pass is linear and each lookup takes constant expected time, so the cost is O(n) time and O(n) extra space for the map, and the clones themselves are the output.

<!-- stage: variables -->
### Map, Originals And Clones

The map is keyed by original node and holds the clone as the value. A `HashMap<Node, Node>` works when the node class does not override `equals` and `hashCode`, because then the default identity semantics apply, and an `IdentityHashMap` is the safe choice when it might. A lookup of a null reference must not be passed to the map as if it were a node; the code tests for null first and leaves the clone's reference null. The head of the copy is `map.get(head)` for a non-empty list, and null for an empty one. With two arbitrary references per node, the second pass simply makes two lookups.

<!-- stage: trace -->
### Four Entries, Then Repeated Titles

Take four entries with titles `5, 9, 2, 6`, where the cross-references point from node 0 to node 2, from node 1 to node 0, from node 3 to itself, and node 2 has none. In the first pass, a clone is made for each node and the map grows to four pairs, with no links set. In the second pass, node 0's clone gets a next reference to the clone of node 1 and a cross-reference to the clone of node 2, which was created in the first pass and exists although it comes later. Node 1's clone points back to the clone of node 0. Node 2's cross-reference stays null. Node 3's clone points to itself, and its next is null.

A second run uses the titles `7, 7, 3, 7` with cross-references `3, 2, 1, 0`. Three of the four entries share a title, so a map keyed by title would hold only two keys after the first pass, and the second pass would send entries 1 and 0 to the clone of the last entry titled 7. The identity map holds four keys, and each cross-reference lands on exactly the right clone.

```trace
{"cells":[5,9,2,6],"pointers":["orig","target"],"steps":[{"at":{"orig":0,"target":-1},"vars":{"pass":"first","map_size":1},"note":"First pass: a new clone holding 5 is created for original node 0, and the identity map now records 1 original-to-clone pair(s). No links are set yet."},{"at":{"orig":1,"target":-1},"vars":{"pass":"first","map_size":2},"note":"First pass: a new clone holding 9 is created for original node 1, and the identity map now records 2 original-to-clone pair(s). No links are set yet."},{"at":{"orig":2,"target":-1},"vars":{"pass":"first","map_size":3},"note":"First pass: a new clone holding 2 is created for original node 2, and the identity map now records 3 original-to-clone pair(s). No links are set yet."},{"at":{"orig":3,"target":-1},"vars":{"pass":"first","map_size":4},"note":"First pass: a new clone holding 6 is created for original node 3, and the identity map now records 4 original-to-clone pair(s). No links are set yet."},{"at":{"orig":0,"target":2},"vars":{"pass":"second","random_so_far":"[2]"},"note":"Second pass: for original node 0 holding 5, its next is the clone of node 1, and its random is the clone of node 2. Each target is found with one map lookup."},{"at":{"orig":1,"target":0},"vars":{"pass":"second","random_so_far":"[2,0]"},"note":"Second pass: for original node 1 holding 9, its next is the clone of node 2, and its random is the clone of node 0. Each target is found with one map lookup."},{"at":{"orig":2,"target":-1},"vars":{"pass":"second","random_so_far":"[2,0,-1]"},"note":"Second pass: for original node 2 holding 2, its next is the clone of node 3, and its random stays null. Each target is found with one map lookup."},{"at":{"orig":3,"target":3},"vars":{"pass":"second","random_so_far":"[2,0,-1,3]"},"note":"Second pass: for original node 3 holding 6, its next is null, and its random is the clone of node 3, which is the clone itself. Each target is found with one map lookup."}]}
```

```trace
{"cells":[7,7,3,7],"pointers":["orig","target"],"steps":[{"at":{"orig":0,"target":-1},"vars":{"pass":"first","identity_map":1,"value_map":1},"note":"First pass: a clone is made for original node 0 holding 7. The identity map holds 1 pairs. A map keyed by value would hold only 1, since equal values collapse into one key."},{"at":{"orig":1,"target":-1},"vars":{"pass":"first","identity_map":2,"value_map":1},"note":"First pass: a clone is made for original node 1 holding 7. The identity map holds 2 pairs. A map keyed by value would hold only 1, since equal values collapse into one key."},{"at":{"orig":2,"target":-1},"vars":{"pass":"first","identity_map":3,"value_map":2},"note":"First pass: a clone is made for original node 2 holding 3. The identity map holds 3 pairs. A map keyed by value would hold only 2, since equal values collapse into one key."},{"at":{"orig":3,"target":-1},"vars":{"pass":"first","identity_map":4,"value_map":2},"note":"First pass: a clone is made for original node 3 holding 7. The identity map holds 4 pairs. A map keyed by value would hold only 2, since equal values collapse into one key."},{"at":{"orig":0,"target":3},"vars":{"pass":"second","target_node":3},"note":"Second pass: original node 0 points at node 3, holding 7. The identity map returns the clone of node 3 exactly. A value-keyed map would return the clone of the last node holding 7, which is correct only when that last node is node 3."},{"at":{"orig":1,"target":2},"vars":{"pass":"second","target_node":2},"note":"Second pass: original node 1 points at node 2, holding 3. The identity map returns the clone of node 2 exactly. A value-keyed map would return the clone of the last node holding 3, which is correct only when that last node is node 2."},{"at":{"orig":2,"target":1},"vars":{"pass":"second","target_node":1},"note":"Second pass: original node 2 points at node 1, holding 7. The identity map returns the clone of node 1 exactly. A value-keyed map would return the clone of the last node holding 7, which is correct only when that last node is node 1."},{"at":{"orig":3,"target":0},"vars":{"pass":"second","target_node":0},"note":"Second pass: original node 3 points at node 0, holding 7. The identity map returns the clone of node 0 exactly. A value-keyed map would return the clone of the last node holding 7, which is correct only when that last node is node 0."}]}
```

<!-- stage: code -->
### Clone With One Or Two Random References

```java
final class CloneCode {
    static final class Node {
        int value;
        Node next, random;
        Node(int value) { this.value = value; }
    }

    static Node copyList(Node head) {
        if (head == null) return null;
        java.util.IdentityHashMap<Node, Node> clone = new java.util.IdentityHashMap<>();
        for (Node o = head; o != null; o = o.next) clone.put(o, new Node(o.value));
        for (Node o = head; o != null; o = o.next) {
            Node c = clone.get(o);
            c.next = o.next == null ? null : clone.get(o.next);
            c.random = o.random == null ? null : clone.get(o.random);
        }
        return clone.get(head);
    }

    static final class Wide {
        int value;
        Wide next, a, b;
        Wide(int value) { this.value = value; }
    }

    static Wide copyWide(Wide head) {
        if (head == null) return null;
        java.util.IdentityHashMap<Wide, Wide> clone = new java.util.IdentityHashMap<>();
        for (Wide o = head; o != null; o = o.next) clone.put(o, new Wide(o.value));
        for (Wide o = head; o != null; o = o.next) {
            Wide c = clone.get(o);
            c.next = o.next == null ? null : clone.get(o.next);
            c.a = o.a == null ? null : clone.get(o.a);
            c.b = o.b == null ? null : clone.get(o.b);
        }
        return clone.get(head);
    }
}
```

Each method makes two linear passes with constant-time lookups, so both take O(n) time and use O(n) space for the map. The second method differs from the first only by one more reference per node, because the invariant of the map does not depend on how many references a node has.

<!-- stage: applicability -->
### When References Point Anywhere

Use an identity map whenever a structure of nodes must be duplicated, or when each node must be paired with a counterpart, and the nodes refer to each other in ways that follow no simple order: random pointers, parent links, graph neighbours, or references to earlier nodes. The invariant is that every clone exists before any link is written, and every link of a clone is the lookup of the matching original link.

The false friend is a map keyed by value. It works on data with distinct values and quietly miswires data with repeated values, so a test on small distinct numbers passes. A second false friend is cloning while wiring, with a single pass that creates a clone only when it is first needed, which works until a reference points to a node that has not been visited yet and then needs bookkeeping for half-built clones. A third is sharing: wiring a clone to an original node by mistake produces a copy that looks right and mutates the original.

Do not use a map when a trick that interleaves clones with originals in the list can avoid the extra memory, though that trick is harder to read and to get right. In Java, avoid a `HashMap` keyed by objects whose `equals` compares values, test for null before calling `get`, and remember that the map holds the only record of the pairing.

<!-- stage: exercises -->
### Exercises

#### [Build] Original-To-Clone Map (Author exercise)
<!-- id: llm-original-clone-map -->

**Prerequisites.** The node invariants lesson, and the hash maps chapter, where keys and equality were studied.

**Problem.** A linked list is given by its values, which may repeat. Create one clone for every node and build two maps: one keyed by the original node object, and one keyed by the node's value. Return `[identityMapSize, valueMapSize]`.

**Constraints.** 0 <= n <= 10^5 and -10^9 <= value <= 10^9.

**Example 1.** Input `values = [7, 7, 3, 7]`, output `[4, 2]`.

**Example 2.** Input `values = []`, output `[0, 0]`.

**Hint.** Which key distinguishes two nodes that hold the same value? What does `put` do when the key is already present?

**Changed decision.** First rung: the key is the original node itself, so every node gets its own entry, and the value-keyed map is built only to show how many entries are lost.

#### [Vary] Copy List with Random Pointer (LeetCode 138)
<!-- id: llm-copy-random-list -->

**Prerequisites.** The Original-To-Clone Map exercise above.

**Problem.** A linked list is given by its values together with an array `random`, where `random[i]` is the index of the node that node `i` points to as its random target, or -1 for none. Build a deep copy, and return a list of pairs `[value, randomIndex]` read from the copy, where `randomIndex` is the index in the copy of the node that the copied node points to. No node of the copy may refer to a node of the original.

**Constraints.** 0 <= n <= 1000, -10^4 <= value <= 10^4 and -1 <= random[i] < n.

**Example 1.** Input `values = [5, 9, 2, 6]`, `random = [2, 0, -1, 3]`, output `[[5, 2], [9, 0], [2, -1], [6, 3]]`.

**Example 2.** Input `values = [4]`, `random = [-1]`, output `[[4, -1]]`.

**Hint.** Why must every clone exist before any random link is written? How is a null random target handled?

**Changed decision.** The clones are created in a first pass and wired in a second one, so a random target that comes later in the list is already available.

#### [Boundary] Null, Self, And Shared Random Targets (Author exercise)
<!-- id: llm-null-self-shared -->

**Prerequisites.** The two exercises above.

**Problem.** For the same input encoding, clone the list and report on the clone: `[nullCount, selfCount, sharedTargets]`, where `nullCount` is the number of clone nodes whose random reference is null, `selfCount` the number whose random reference is the node itself, and `sharedTargets` the number of clone nodes that are the random target of two or more clone nodes.

**Constraints.** 0 <= n <= 10^5 and -1 <= random[i] < n. Each target must be cloned only once.

**Example 1.** Input `values = [1, 2, 3, 4]`, `random = [-1, 1, 2, 2]`, output `[1, 2, 1]`.

**Example 2.** Input `values = [8]`, `random = [0]`, output `[0, 1, 0]`.

**Hint.** What does a lookup return for a self reference? How can you tell that two clones share a target, with identity and not with values?

**Changed decision.** The three reference cases are read from the clone, not from the encoding, so any lookup that created a second clone for a shared target would be caught.

#### [Recognize] Two Arbitrary References (Author exercise)
<!-- id: llm-two-references -->

**Prerequisites.** All three exercises above.

**Problem.** Each node has a value, a `next` reference and two arbitrary references `a` and `b`. The list is given by `values` and arrays `a` and `b` of target indices, with -1 for none. Clone the list and return triples `[value, aIndex, bIndex]` read from the clone, where each index is a position in the clone.

**Constraints.** 0 <= n <= 10^5, -10^9 <= value <= 10^9 and -1 <= a[i], b[i] < n.

**Example 1.** Input `values = [3, 5, 8]`, `a = [2, -1, 0]`, `b = [1, 1, -1]`, output `[[3, 2, 1], [5, -1, 1], [8, 0, -1]]`.

**Example 2.** Input `values = [6, 6]`, `a = [1, 0]`, `b = [0, 1]`, output `[[6, 1, 0], [6, 0, 1]]`.

**Hint.** Does the number of references change what the map must hold? What would a map keyed by value do in the second example?

**Changed decision.** A second arbitrary reference adds one more lookup in the wiring pass, and the identity map and the two-pass order stay exactly as they were.
