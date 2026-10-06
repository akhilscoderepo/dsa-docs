<!-- lesson-kind: standard -->
<!-- lesson-id: multilevel-flattening -->
## Flatten Child Lists Into One List

<!-- stage: context -->
### Why The Up Arrow Jumps Backward

A file browser shows a folder as a doubly linked list of entries. Each entry has a `next` link, a `prev` link, and a `child` link that points to the first entry inside the folder. To support the arrow keys, the browser flattens the open folders into one list, so the down arrow follows `next` and the up arrow follows `prev`. After the first version of the flattening code, the down arrow walks through every entry in the right order. The up arrow from the first entry after a folder jumps to the folder's own name and skips every entry inside it.

The code set every `next` link correctly and left some `prev` links pointing at their old neighbors. A doubly linked list has two links per boundary, and a method that fixes one of them produces a list that works in one direction only. The question for this lesson is how to move a whole sub-list into the middle of another list while every link stays consistent.

<!-- stage: naive -->
### Collecting Every Node In An Array

The direct plan visits the entries in display order, stores them in an array, and then links the array from left to right in both directions.

```java
final class FlattenByArray {
    static final class Node {
        int val;
        Node prev, next, child;
        Node(int val) { this.val = val; }
    }

    static void collect(Node chain, List<Node> out) {
        for (Node c = chain; c != null; c = c.next) {
            out.add(c);                              // the entry comes first
            if (c.child != null) collect(c.child, out);   // then everything inside it
        }
    }

    static Node flatten(Node head) {
        List<Node> all = new ArrayList<>();
        collect(head, all);
        for (int i = 0; i < all.size(); i++) {
            Node c = all.get(i);
            c.child = null;                          // no folder remains open
            c.prev = (i == 0) ? null : all.get(i - 1);                  // both directions are rewritten
            c.next = (i + 1 == all.size()) ? null : all.get(i + 1);
        }
        return head;
    }
}
```

The method returns a correct list in both directions. It rewrites every link of every entry, including the links that were already right.

<!-- stage: bottleneck -->
### Counting The Extra Memory

```predict
The array method visits n entries. What extra memory does it need, and how deep can its recursion go when folders nest k levels?

The array holds all n entries, so it needs O(n) extra memory. The recursion goes k calls deep, so a very deep nesting can overflow the Java call stack.
```

The time is O(n), and no method can do better than visit each entry once. The extra memory is the problem. A list of one million entries needs an array of one million references, even though the method only needs to change a few links at each folder. The recursion adds one stack frame per level of nesting.

Most links are already correct. Only the boundaries around each folder's contents need rewiring: the link into the first entry inside, and the link out of the last one. A method that changes only those links needs no array.

<!-- stage: insight -->
### Splicing A Child Chain In Place

Call the list that starts at a node's `child` field its **child chain**. The method moves each child chain into the main list, directly after its parent. The result lists every node in **preorder**: a node comes first, then everything in its child chain, then the node's old successor.

#### Four Links Change At Each Splice

A splice touches four boundaries. The parent's `next` must point at the child chain's first node. That first node's `prev` must point back at the parent. The **child tail**, the last node of the child chain, must point at the parent's old successor. That successor's `prev` must point back at the child tail. A splice that writes only the two `next` links leaves the two `prev` links stale, which is the failure from the opening example.

<!-- names: child chain, child tail, preorder -->

#### Saving The Old Successor First

The write `parent.next = child` overwrites the only link to the old successor. The method therefore copies the old successor into a variable before any write. Then it finds the child tail with one walk along the child chain. The copy is `null` when the parent is the last node of its list. In that case the child tail becomes the last node, and the write `succ.prev = tail` must be skipped.

#### Reaching Nested Children

A child chain may contain nodes that have children of their own. The method does not need a special case. After a splice, the walk continues from the parent into the spliced nodes, because they now follow the parent in the main list. When the walk reaches a spliced node with a child, it splices again. Every node is visited once by the main walk and at most once by a tail search, so the whole method is O(n).

<!-- stage: variables -->
### The References Around One Splice

- **parent** holds the node whose `child` field is not `null`.
- **child** holds the first node of the child chain.
- **tail** holds the child tail, the last node of the child chain.
- **succ** holds the parent's old `next`, copied before any write, and it may be `null`.
- **prev**, **next** and **child** are the three link fields of every node.

<!-- stage: trace -->
### Splicing Once And Then Twice

In these traces, a pointer at the left of the cells or past their right end is `null`. In each step the variable `forward` reads the list from the head along `next`, and `backward` reads it from the last node along `prev`.

#### One Child Chain On Three Nodes

Take the main list `1, 2, 3`, where the node 2 has the child chain `7, 8`. The cells list the main nodes first and then the child nodes. The pointers `parent`, `tail` and `succ` mark the three nodes the splice uses.

```trace
{"cells":[1,2,3,7,8],"pointers":["parent","tail","succ"],"steps":[{"at":{"parent":1,"tail":-1,"succ":-1},"vars":{"forward":"1,2,3","backward":"3,2,1"},"note":"Start: the main list reads 1,2,3. The node 2 has the child chain 7,8, whose links are kept apart from the main list."},{"at":{"parent":1,"tail":-1,"succ":2},"vars":{"forward":"1,2,3","backward":"3,2,1"},"note":"succ copies parent.next, which is the node 3. This happens before any write."},{"at":{"parent":1,"tail":4,"succ":2},"vars":{"forward":"1,2,3","backward":"3,2,1"},"note":"The walk along the child chain stops on the node 8, the child tail."},{"at":{"parent":1,"tail":4,"succ":2},"vars":{"forward":"1,2,7,8","backward":"3,2,1"},"note":"parent.next now points at the node 7, and the node 7 points back at the node 2. The main list is cut after the node 8: forward reads 1,2,7,8 and the node 3 is held only by succ."},{"at":{"parent":1,"tail":4,"succ":2},"vars":{"forward":"1,2,7,8,3","backward":"3,8,7,2,1"},"note":"tail.next points at the node 3, and the node 3 points back at the node 8. Both directions now agree."}]}
```

After the four writes, `forward` reads `1, 2, 7, 8, 3` and `backward` reads `3, 8, 7, 2, 1`. The two directions agree, because both `prev` links changed together with the `next` links.

#### Two Levels Of Children

Now take the main list `1, 2, 3` where the node 2 has the child chain `7, 8, 9`, and the node 8 has the child chain `11, 12`. The walk moves along the main list and splices at each node that has a child.

```trace
{"cells":[1,2,3,7,8,9,11,12],"pointers":["curr","tail"],"steps":[{"at":{"curr":0,"tail":-1},"vars":{"forward":"1,2,3"},"note":"Start: the main list reads 1,2,3. The nodes 2 and 8 each have a child chain."},{"at":{"curr":1,"tail":5},"vars":{"forward":"1,2,7,8,9,3"},"note":"The node 2 has a child chain, so it is spliced in front of the node 3. The child tail is the node 9."},{"at":{"curr":4,"tail":7},"vars":{"forward":"1,2,7,8,11,12,9,3"},"note":"The node 8 has a child chain, so it is spliced in front of the node 9. The child tail is the node 12."},{"at":{"curr":-1,"tail":7},"vars":{"forward":"1,2,7,8,11,12,9,3"},"note":"The walk ends at null. Every child chain is spliced, and the list reads 1,2,7,8,11,12,9,3."}]}
```

The second splice happens at the node 8, which the first splice moved into the main list. The walk needs no special case for the nested child, because the node 8 is reached by the same walk.

<!-- stage: code -->
### Flattening In Code

```java
final class MultilevelFlatten {
    static final class Node {
        int val;
        Node prev, next, child;
        Node(int val) { this.val = val; }
    }

    static void splice(Node parent) {
        Node child = parent.child;
        Node succ = parent.next;                       // copied before any write, and may be null
        Node tail = child;
        while (tail.next != null) tail = tail.next;    // one walk finds the child tail
        parent.next = child;                           // parent to the first child node
        child.prev = parent;                           // the first child node back to the parent
        tail.next = succ;                              // the child tail to the old successor
        if (succ != null) succ.prev = tail;            // the successor back to the child tail, if one exists
        parent.child = null;                           // the folder is no longer a separate chain
    }

    static Node flatten(Node head) {
        for (Node curr = head; curr != null; curr = curr.next) {   // spliced nodes are reached by the same walk
            if (curr.child != null) splice(curr);
        }
        return head;
    }
}
```

The method `flatten` returns the same head, because the head's position never changes. The statement `if (succ != null)` is the only guard the splice needs, and it covers a child that belongs to the last node of a list.

- **Time** is O(n), because each node is reached once by the main walk and at most once by a tail search.
- **Space** is O(1), because the method stores four references and no collection.

<!-- stage: applicability -->
### Keeping Both Directions Consistent

#### Stating The Two-Way Rule

The invariant of every splice is that for each pair of neighbors, `a.next == b` holds exactly when `b.prev == a` holds. A splice that keeps this rule at the four boundaries leaves the list correct in both directions. After writing a splice, check each of the four writes against this rule.

#### Seeing The One-Direction Bug

The false friend of a flattening method is the list that looks right when read forward. A test that only reads along `next` passes while the `prev` links are wrong. A good check reads the list in both directions, and compares the two readings.

#### Using A Stack When The Order Changes

The splice needs the child tail, which costs one walk. A method that holds the old successors on an explicit stack avoids the tail search. The Vary exercise below uses the stack. A recursive method that returns the tail of each chain is the third form, and the Recognize exercise uses it.

<!-- stage: exercises -->
### Exercises

#### [Build] Splice One Child Chain (Author exercise)
<!-- id: ll-splice-one -->

**Prerequisites.** The four writes of one splice from this lesson.

**Problem.** A doubly linked list has `prev` and `next` links. A node `parent` has a non-null `child`, which is the first node of a plain doubly linked chain. No node of the child chain has a child. Replace the link structure so that the whole child chain sits between `parent` and the old successor of `parent`, with all `prev` and `next` links consistent, and set `parent.child` to `null`.

**Constraints.** The limits are:
- **Main list** has between 1 and 100 nodes, and `parent` is one of them.
- **Child chain** has between 1 and 100 nodes with no children of their own.
- **Values** satisfy `-10^4 <= val <= 10^4`.
- **Mutation** changes link fields only and allocates no node.

**Example 1.** Input main list `1, 2, 3`, `parent` at the node 2 and the child chain `7, 8`, output `1, 2, 7, 8, 3` read forward and `3, 8, 7, 2, 1` read backward.

**Example 2.** Input main list `1, 2`, `parent` at the node 2 and the child chain `5`, output `1, 2, 5` in both directions.

**Hint.** Which node must be saved before `parent.next` changes? What does the child tail point at when the parent is the last node?

**Changed decision.** One child chain moves into the main list, and four boundaries need rewriting.

#### [Vary] Stack Of Deferred Successors (Author exercise)
<!-- id: ll-deferred-stack -->

**Prerequisites.** The exercise above.

**Problem.** The nodes of a multilevel doubly linked list have `prev`, `next` and `child` links, and a child chain may have children of its own. Flatten the list with an explicit stack and no tail search. When a node has a child and a non-null `next`, push that `next` onto the stack, link the node to its child, and continue in the child chain. When a chain ends and the stack is not empty, pop a node and link the last node of the chain to it. Return the head and the largest number of nodes the stack held at one moment.

**Constraints.** The limits are:
- **Length** is between 0 and 1000 nodes in all, including nested chains.
- **Values** are distinct `int` values.
- **Answer** is the head and an `int` count.
- **Mutation** changes link fields only, and every `child` ends as `null`.

**Example 1.** Input main list `1, 2, 3` with the child chain `7, 8` on the node 2, output `1, 2, 7, 8, 3` and the largest stack size 1.

**Example 2.** Input main list `1, 2, 3` with the child chain `7, 8, 9` on the node 2 and the chain `11, 12` on the node 8, output `1, 2, 7, 8, 11, 12, 9, 3` and the largest stack size 2.

**Hint.** What does the stack hold after the first descent in Example 2? Which node is pushed at the second descent?

**Changed decision.** The old successor waits on a stack instead of in a local variable.

#### [Boundary] Child At Tail And Nested Child (Author exercise)
<!-- id: ll-child-edges -->

**Prerequisites.** The two exercises above.

**Problem.** Flatten a multilevel doubly linked list in place, and make the method correct for two special shapes. In the first, a node that has a child is the last node of its chain, so its old successor is `null`. In the second, a child chain has a node with a child of its own. After the call every node has `child` equal to `null`, every `prev` and `next` pair agrees, and the list reads in preorder.

**Constraints.** The limits are:
- **Length** is between 0 and 1000 nodes in all.
- **Values** are distinct `int` values.
- **Answer** is the head of the flattened list, or `null` for the empty list.
- **Mutation** changes link fields only.

**Example 1.** Input main list `1, 2` with the child chain `5, 6` on the node 2, output `1, 2, 5, 6`, and the node 6 has `next` equal to `null`.

**Example 2.** Input main list `1` with the child chain `2` on the node 1 and the child chain `3` on the node 2, output `1, 2, 3`.

**Hint.** What must the splice skip when the old successor is `null`? Which node does the walk reach after a splice?

**Changed decision.** A null saved successor removes one write, and a nested child needs no extra case.

#### [Recognize] Flatten a Multilevel Doubly Linked List (LeetCode 430)
<!-- id: ll-flatten-430 -->

**Prerequisites.** All three exercises above.

**Problem.** Given the head of a multilevel doubly linked list, where each node has `prev`, `next` and `child` links and a child chain may have children of its own, flatten the list so that all nodes appear in a single-level doubly linked list. A node comes before its child chain, and the child chain comes before the node's old successor. Set every `child` to `null` and return the head. A recursive method that returns the last node of each flattened chain is allowed.

**Constraints.** The limits are:
- **Length** is between 0 and 1000 nodes in all.
- **Values** satisfy `1 <= val <= 10^5`.
- **Answer** is the head of the flattened list.
- **Mutation** changes link fields only.

**Example 1.** Input main list `1, 2, 3, 4` with the child chain `5, 6` on the node 2 and the child chain `7` on the node 6, output `1, 2, 5, 6, 7, 3, 4`.

**Example 2.** Input main list `1, 2` with the child chain `3` on the node 1, output `1, 3, 2`.

**Hint.** What does the recursive call on a child chain return? Which two links must the parent set around that chain?

**Changed decision.** The method returns the last node of each chain instead of searching for it.
