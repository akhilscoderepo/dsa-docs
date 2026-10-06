<!-- lesson-kind: combination -->
<!-- lesson-id: copy-a-list-with-random-links -->
## Copy A List With Random Links

<!-- stage: context -->
### Why The Snapshot Changes With The Document

A document editor stores an outline as a list of nodes. Each node has a `next` link to the following item and a `related` link to any other item, which the editor shows as a cross-reference. The undo feature takes a snapshot of the outline before each edit. The first version of the snapshot code walks the list, makes a new node for each item, and copies the `related` field by plain assignment. The snapshot looks right. Then the user edits an item, and the cross-references inside the old snapshot change too, because every `related` link in the snapshot still points at a node of the live outline.

A snapshot must share nothing with the live outline. Each link of the snapshot must point at a node of the snapshot. The `next` links follow the list order, so they are easy to rebuild. The `related` links point anywhere, and the program needs to find the snapshot node that stands for any original node.

<!-- stage: contributions -->
### What Each Earlier Idea Adds

Two earlier ideas combine in this lesson, and each supplies one half. The linked list lessons of this chapter supply the order and the identity of the nodes. A walk along `next` reaches every node exactly once, and a node reference names one particular node even when another node holds the same value. The list alone cannot answer a question about an arbitrary link, because the only way to reach a node from a random link is a walk from the head.

The hash map lessons of Chapter 04 supply the lookup. A map answers "what is stored for this key" in constant time on average. If the key is the original node, the stored value can be the copy of that node. The map alone cannot say in which order to build the copies or how many nodes exist, and the list supplies exactly that. Together they give a copy in which every link lands on the right node, and neither idea needs the other half's work done by a slower method.

<!-- stage: naive -->
### Finding Each Target By Walking

The direct plan builds the copies in list order first. For each random link, it walks the original list from the head to count the position of the target, and then walks the copies by the same count.

```java
final class CopyByPosition {
    static final class Node {
        int val;
        Node next, random;
        Node(int val) { this.val = val; }
    }

    static Node copy(Node head) {
        Node copyHead = null, copyTail = null;
        for (Node c = head; c != null; c = c.next) {         // pass 1 builds the copies in list order
            Node n = new Node(c.val);
            if (copyHead == null) copyHead = n; else copyTail.next = n;
            copyTail = n;
        }
        Node o = head, k = copyHead;
        while (o != null) {                                  // pass 2 sets each random link by position
            if (o.random != null) {
                int pos = 0;
                for (Node s = head; s != o.random; s = s.next) pos++;   // walk to the target in the original
                Node t = copyHead;
                for (int i = 0; i < pos; i++) t = t.next;            // walk the same distance in the copy
                k.random = t;
            }
            o = o.next; k = k.next;
        }
        return copyHead;
    }
}
```

The method returns a list whose links all stay inside the new nodes. Its `random` links match the original by position.

<!-- stage: bottleneck -->
### Counting The Walks

```predict
The list has n nodes and every node has a random link. In the worst case, how many hops do the position walks take in total, and which of those hops does the program already know the answer to?

Each random link can cost up to n hops in the original and up to n hops in the copy, so the walks cost O(n^2) in total. The program already visited every node once in the first pass, so the hops repeat work that a stored answer would avoid.
```

For a list of 100,000 nodes, the position walks can take about twenty billion hops. The time is wasted because the first pass saw every original node and created its copy, and then forgot the pairing. A second pass has to rediscover the pairing for each link, and the only tool it has is a walk.

The pairing "this original node, that copy" is a function from nodes to nodes. A hash map stores such a function, so the program can save the pairing in the first pass and read it in the second.

<!-- stage: insight -->
### Pairing Each Node With Its Copy

A **deep copy** of a list makes one new node for each original node, and every link of every new node points at a new node or is `null`. No new node shares a link with an original node. Building a deep copy needs two facts about each node: its copy, and the copies of the nodes its links point at.

#### Saving The Pairing In An Identity Map

An **identity map** is a hash map whose keys are compared by object identity and not by value. The first pass walks the original list and puts one entry in the map for each node, with the original node as the key and a new node holding the same value as the entry's value. After this pass, every original node has exactly one copy, and the map answers "which copy belongs to this node" in constant time.

<!-- names: deep copy, identity map, second pass -->

#### Wiring The Links In The Second Pass

The **second pass** walks the original list again. For each original node, it looks up the copy of the node, the copy of the node's `next` target, and the copy of its `random` target. It assigns the two links of the copy. A `null` link has no copy, so the lookup of `null` yields `null`, and the link stays `null`. The pass does not need to know the order of the targets, because every copy already exists.

#### Why Two Passes Are Needed

A random link may point forward to a node that has no copy yet. A single pass that wired links as it went would find the target missing. Creating every copy first guarantees that every lookup in the second pass succeeds. The map holds each original node once, so a node that many random links point at still gets one copy, and a link that points at its own node maps to its own copy.

<!-- stage: variables -->
### The State Of The Two Passes

- **map** holds one entry per original node, with the original node as the key and its copy as the value.
- **curr** holds the original node under inspection in either pass.
- **copy** holds the copy of `curr`, which is `map.get(curr)`.
- **copy.next** and **copy.random** are set in the second pass from `map.get(curr.next)` and `map.get(curr.random)`.
- **n** is the number of original nodes and the final size of `map`.

<!-- stage: trace -->
### Two Passes On Three Nodes

Here `null` is a pointer that sits outside the cells.

#### Copying A Plain Case

Take the list `5, 8, 2`. The `random` link of the node 5 points at the node 2, the node 8 has a `null` random link, and the node 2 points at the node 5. The pointer `curr` marks the original node under inspection. The variable `map` counts entries, and `links` shows the links of the copies as positions.

```trace
{"cells":[5,8,2],"pointers":["curr"],"steps":[{"at":{"curr":0},"vars":{"map":0,"links":"none"},"note":"Start: the map is empty, and curr is the first original node."},{"at":{"curr":1},"vars":{"map":1,"links":"none"},"note":"First pass: a new node for the original node 5 is stored in the map. The map holds 1 entries."},{"at":{"curr":2},"vars":{"map":2,"links":"none"},"note":"First pass: a new node for the original node 8 is stored in the map. The map holds 2 entries."},{"at":{"curr":-1},"vars":{"map":3,"links":"none"},"note":"First pass: a new node for the original node 2 is stored in the map. The map holds 3 entries."},{"at":{"curr":0},"vars":{"map":3,"links":"0:next=1,random=2"},"note":"Second pass at the node 5: next becomes the copy of the node 8, and random becomes the copy of the node 2. Every lookup finds an entry."},{"at":{"curr":1},"vars":{"map":3,"links":"0:next=1,random=2 1:next=2,random=null"},"note":"Second pass at the node 8: next becomes the copy of the node 2, and random becomes null. Every lookup finds an entry."},{"at":{"curr":2},"vars":{"map":3,"links":"0:next=1,random=2 1:next=2,random=null 2:next=null,random=0"},"note":"Second pass at the node 2: next becomes null, and random becomes the copy of the node 5. Every lookup finds an entry."}]}
```

The first three steps create the copies, one entry per original node. The next three steps wire the links, and every lookup finds an entry because the first pass finished.

#### Copying Self And Shared Targets

Now take the list `4, 6, 9`. The node 4 points at itself, and the nodes 6 and 9 both point at the node 9. The map still holds one entry per node.

```trace
{"cells":[4,6,9],"pointers":["curr"],"steps":[{"at":{"curr":0},"vars":{"map":0,"links":"none"},"note":"Start: the map is empty, and curr is the first original node."},{"at":{"curr":1},"vars":{"map":1,"links":"none"},"note":"First pass: a new node for the original node 4 is stored in the map. The map holds 1 entries."},{"at":{"curr":2},"vars":{"map":2,"links":"none"},"note":"First pass: a new node for the original node 6 is stored in the map. The map holds 2 entries."},{"at":{"curr":-1},"vars":{"map":3,"links":"none"},"note":"First pass: a new node for the original node 9 is stored in the map. The map holds 3 entries."},{"at":{"curr":0},"vars":{"map":3,"links":"0:next=1,random=0"},"note":"Second pass at the node 4: next becomes the copy of the node 6, and random becomes the copy of the node 4. Every lookup finds an entry."},{"at":{"curr":1},"vars":{"map":3,"links":"0:next=1,random=0 1:next=2,random=2"},"note":"Second pass at the node 6: next becomes the copy of the node 9, and random becomes the copy of the node 9. Every lookup finds an entry."},{"at":{"curr":2},"vars":{"map":3,"links":"0:next=1,random=0 1:next=2,random=2 2:next=null,random=2"},"note":"Second pass at the node 9: next becomes null, and random becomes the copy of the node 9. Every lookup finds an entry. The node 9 is the target of two random links and still has one copy."}]}
```

The node 9 is the target of two random links, and it has one copy. The node 4 points at itself, and its copy points at itself.

<!-- stage: code -->
### Copying In Code

```java
final class RandomListCopy {
    static final class Node {
        int val;
        Node next, random;
        Node(int val) { this.val = val; }
    }

    static Node copyRandomList(Node head) {
        Map<Node, Node> copyOf = new HashMap<>();       // original node to its copy
        for (Node c = head; c != null; c = c.next) {    // first pass: one copy per original node
            copyOf.put(c, new Node(c.val));
        }
        for (Node c = head; c != null; c = c.next) {    // second pass: wire the links of each copy
            Node k = copyOf.get(c);
            k.next = copyOf.get(c.next);                // get(null) returns null, so the end stays null
            k.random = copyOf.get(c.random);
        }
        return copyOf.get(head);                        // null for the empty list
    }
}
```

The class `Node` does not override `equals` or `hashCode`, so `HashMap` compares nodes by identity, which is the rule this lesson needs. A `Node` that compares by value would merge two nodes with equal values into one key, and the method would lose a copy.

- **Time** is O(n), because each pass makes one hop and one map operation per node.
- **Space** is O(n), because the map holds one entry per node and the copies hold n new nodes.

<!-- stage: applicability -->
### Using The Pairing Rule

#### Stating What The Map Guarantees

The invariant of the method is that after the first pass the map holds exactly one copy for each original node, and no copy is created again in the second pass. State this before coding, and check each link of the copy against it. A lookup that returns `null` for a non-null link means the first pass missed a node.

#### Avoiding Shared Links

The false friend of this lesson is the plain assignment `copy.random = original.random`. It compiles, and it produces a list that looks right, but its links point into the original list. A test that edits the original and reads the copy catches it. A second false friend is a map keyed by value, such as `Map<Integer, Node>`, which merges nodes with equal values.

#### Counting The Cost

The map costs O(n) extra memory. If a statement forbids extra memory, another technique places each copy between its original and the next original, and it needs no map. That technique is not part of this lesson, because the map version states the pairing directly and is easier to check.

<!-- stage: exercises -->
### Exercises

#### [Build] Original-To-Clone Map (Author exercise)
<!-- id: ll-copy-map -->

**Prerequisites.** The identity map and the first pass of this lesson.

**Problem.** Given the head of a list in which each node has a `next` link and a `random` link, build a map from each original node to a new node that holds the same value and has `null` for both links. Return the number of entries in the map and the new node that belongs to the head. Two original nodes with equal values must get two different new nodes.

**Constraints.** The limits are:
- **Length** is between 0 and 1000 nodes.
- **Values** satisfy `-10^4 <= val <= 10^4`, and values may repeat.
- **Answer** is an entry count and a node reference.
- **Mutation** does not occur; the original list is unchanged.

**Example 1.** Input `5, 8, 2` with any random links, output 3 entries and a new node holding 5.

**Example 2.** Input `7, 7` with any random links, output 2 entries and two different new nodes, both holding 7.

**Hint.** What must the key of the map be so that two equal values stay apart? What does the map hold for the empty list?

**Changed decision.** The map pairs nodes by identity, and the first pass creates every copy.

#### [Vary] Copy List with Random Pointer (LeetCode 138)
<!-- id: ll-copy-random -->

**Prerequisites.** The exercise above.

**Problem.** Given the head of a list in which each node has a `next` link and a `random` link to any node of the list or `null`, return a deep copy. The copy has exactly `n` new nodes. Every `next` and `random` link of a new node points at a new node or is `null`, and the links match the original by position. Use a second pass to wire both links through the map.

**Constraints.** The limits are:
- **Length** is between 0 and 1000 nodes.
- **Values** satisfy `-10^4 <= val <= 10^4`, and values may repeat.
- **Answer** is the head of the copy, or `null` for the empty list.
- **Mutation** does not occur; no link of the original changes.

**Example 1.** Input values `5, 8, 2` with `random` positions 2, none and 0, output a copy with the same values and random positions.

**Example 2.** Input values `3, 3` with `random` positions 1 and 0, output a copy where the two new nodes point at each other.

**Hint.** Which pass can create a copy for a node that a later random link points at? What does `map.get(null)` return?

**Changed decision.** The second pass wires both links by lookup instead of by position.

#### [Boundary] Null, Self, And Shared Random Targets (Author exercise)
<!-- id: ll-copy-edges -->

**Prerequisites.** The two exercises above.

**Problem.** Deep copy the list as in the previous exercise, and also return the number of new nodes that the method allocates in total. The count must equal `n`, even when a `random` link is `null`, points at its own node, or points at a node that other links also target. A method that allocates a second copy for a repeated target fails this requirement.

**Constraints.** The limits are:
- **Length** is between 0 and 1000 nodes.
- **Values** satisfy `-10^4 <= val <= 10^4`.
- **Answer** is the head of the copy and an allocation count.
- **Mutation** does not occur.

**Example 1.** Input values `4, 6, 9` with `random` positions 0, 2 and 2, output a copy with those random positions and 3 allocations.

**Example 2.** Input values `1` with `random` position none, output a one-node copy and 1 allocation.

**Hint.** When does the method allocate a node? Can a lookup in the second pass allocate one?

**Changed decision.** Allocation moves to the first pass only, so repeated targets never get a second copy.

#### [Recognize] Two Arbitrary References (Author exercise)
<!-- id: ll-copy-two-random -->

**Prerequisites.** All three exercises above.

**Problem.** Each node has a value, a `next` link, and two further links `randomA` and `randomB`, each pointing at any node of the list or `null`. Return a deep copy in which the three links of every new node point at new nodes or are `null`, and match the original by position. Reuse the one identity map for all three links.

**Constraints.** The limits are:
- **Length** is between 0 and 1000 nodes.
- **Values** satisfy `-10^4 <= val <= 10^4`, and values may repeat.
- **Answer** is the head of the copy, or `null` for the empty list.
- **Mutation** does not occur.

**Example 1.** Input values `1, 2, 3` with `randomA` positions 2, 0 and none, and `randomB` positions 1, 1 and 2, output a copy with the same positions.

**Example 2.** Input values `9, 9` with both references pointing at the second node in each node, output a copy where all four references point at the second new node.

**Hint.** Does a third link change what the first pass does? Which lines of the second pass grow?

**Changed decision.** The same map serves a third link, and only the second pass grows by one line.
