<!-- lesson-kind: standard -->
<!-- lesson-id: multilevel-flattening -->
## Multilevel Flattening

<!-- stage: context -->
### A Playlist With Nested Bonus Tracks

A radio station keeps its evening playlist as a chain of tracks. A disc jockey can step forward to the next track or backward to the one before it, so every track knows both of its neighbours. Some tracks carry a bonus set: a short playlist of its own that must be played immediately after the track and before the main playlist carries on. A bonus track can itself have a bonus set, and the nesting can go several levels deep.

The station wants one plain playlist, played in order, that the disc jockey can step through in either direction without ever meeting a bonus set. The bonus tracks have to be moved into place, and the station insists that the tracks are not copied, because each track holds a licensing record. What worries the producer is the order of the work. When a bonus set is moved into place, the track that came after the parent in the main playlist must not be forgotten, and the backward steps must stay correct, or the disc jockey will be taken to the wrong track on the way back.

<!-- stage: naive -->
### Collect In A List, Then Relink Everything

One approach is to visit the tracks in play order with a recursive walk, collect them in a list, and then link the list from front to back, setting both neighbours of every track and clearing every bonus reference.

```java
final class PlaylistByCollect {
    static final class Track {
        int id;
        Track prev, next, bonus;
        Track(int id) { this.id = id; }
    }

    static void collect(Track t, java.util.List<Track> out) {
        for (Track cur = t; cur != null; cur = cur.next) {
            out.add(cur);
            if (cur.bonus != null) collect(cur.bonus, out);
        }
    }

    static Track flatten(Track head) {
        java.util.List<Track> order = new java.util.ArrayList<>();
        collect(head, order);
        for (int i = 0; i < order.size(); i++) {
            Track t = order.get(i);
            t.bonus = null;
            t.prev = i == 0 ? null : order.get(i - 1);
            t.next = i + 1 < order.size() ? order.get(i + 1) : null;
        }
        return order.isEmpty() ? null : order.get(0);
    }
}
```

It is correct. Every track is placed once, both neighbours are set, and every bonus reference is cleared.

<!-- stage: bottleneck -->
### Memory, Recursion Depth And A Hidden Hazard

The list of tracks takes O(n) extra memory, and the recursive collection takes one stack frame per level of nesting. A playlist nested a hundred thousand levels deep, which is legal in the real data model, overflows the call stack long before the work is done. The rewiring pass also rewrites every link, including the ones that were already right, which is wasted effort when most tracks have no bonus set at all.

A better plan changes only the links that need to change. Where a track has a bonus set, only two connections are wrong: the parent must lead into the bonus set instead of its old successor, and the last track of the bonus set must lead into that old successor. Everything else in the chain is already correct. The danger is the order of the edits. As soon as the parent is pointed at the bonus set, its old successor is reachable only through the reference that was just overwritten, exactly as in the reversal lesson, and the backward links of the old successor still point at the parent. A plan that keeps both the old successor and the symmetry of the links needs a rule that holds at every moment.

<!-- stage: insight -->
### Defer The Successor And Keep Links Symmetric

Walk the playlist with one reference `cur` and process the tracks in the order they will be played. When `cur` has a bonus set, the track after it in its own chain is the **deferred successor**: it must be played after the whole bonus set, however deep, so it is pushed on a stack and the walk goes into the bonus set. The splice happens in a fixed **splice order**: first save or push the old successor, then link the parent forward to the bonus head, then link the bonus head back to the parent, then clear the parent's bonus reference. The walk continues forward through the bonus set, and when it reaches a track with no successor while the stack is not empty, it pops the deferred successor, links the track forward to it and the deferred successor back to the track, and continues from there.

<!-- names: deferred successor, splice order, symmetric links -->

The invariant is that the tracks before `cur` are in final order with **symmetric links**, meaning that for every pair of neighbours `a.next == b` exactly when `b.prev == a`, that no bonus reference remains before `cur`, and that every unplayed suffix is reachable either from `cur` or from a node on the stack. Updating only forward links would leave a playlist that plays correctly in one direction and is broken when stepped backward.

Each track is pushed and popped at most once and visited once, so the cost is O(n) time, and the stack holds at most one entry per level of nesting at any time.

<!-- stage: variables -->
### Walker, Stack And The Four Links

The walker `cur` moves along `next`. The stack holds the deferred successors, and its depth is bounded by the nesting depth. A splice touches four references: the parent's `next` and `bonus`, and the bonus head's `prev`, and later the end track's `next` with the deferred successor's `prev`. The old successor may be null, because the parent may be the last track of its chain, and then nothing is pushed. An empty playlist has a null head, and the function returns null. The bonus reference must be set to null after splicing, or the structure keeps a second route to the same tracks.

<!-- stage: trace -->
### Two Levels And A Single Splice

Take the playlist `1, 2, 3` in which track 2 has a bonus set `4, 5, 7`, and track 5 has a bonus set `6`. The walker passes track 1 and reaches track 2. Track 2 has a bonus set, so its successor, holding 3, is pushed, and track 2 is linked forward to track 4. The walker moves through 4 and reaches 5, which has a bonus set, so its successor, holding 7, is pushed, and track 5 is linked to track 6. Track 6 has no successor and the stack is not empty, so 7 is popped and linked after 6. Track 7 also has no successor, so 3 is popped and linked after 7. Track 3 ends the walk, and the playlist reads 1, 2, 4, 5, 6, 7, 3.

A second run splices one bonus set into the chain `1, 2, 3, 4` without a stack. The parent is track 2 and its bonus set is `7, 8`. The old successor, track 3, is saved. The last bonus track 8 is linked forward to track 3 and track 3 is linked back to track 8, and only then the parent is linked to the bonus head and the bonus head back to the parent. Forward the playlist reads 1, 2, 7, 8, 3, 4, and backward from the end it reads 4, 3, 8, 7, 2, 1.

```trace
{"cells":[1,2,3,4,5,7,6],"pointers":["cur"],"steps":[{"at":{"cur":0},"vars":{"stack":"[]","flat_so_far":"1,2,3"},"note":"The walker is on the node holding 1. There is no child, so the walker follows the next link."},{"at":{"cur":1},"vars":{"stack":"[3]","flat_so_far":"1,2,4,5,7"},"note":"The walker is on the node holding 2. It has a child chain, so its successor, holding 3, is pushed onto the stack of deferred successors. The child head, holding 4, now follows it, and the child reference is cleared."},{"at":{"cur":3},"vars":{"stack":"[3]","flat_so_far":"1,2,4,5,7"},"note":"The walker is on the node holding 4. There is no child, so the walker follows the next link."},{"at":{"cur":4},"vars":{"stack":"[3,7]","flat_so_far":"1,2,4,5,6"},"note":"The walker is on the node holding 5. It has a child chain, so its successor, holding 7, is pushed onto the stack of deferred successors. The child head, holding 6, now follows it, and the child reference is cleared."},{"at":{"cur":6},"vars":{"stack":"[3]","flat_so_far":"1,2,4,5,6,7"},"note":"The walker is on the node holding 6. This chain has ended, so the deferred successor holding 7 is popped and linked after it."},{"at":{"cur":5},"vars":{"stack":"[]","flat_so_far":"1,2,4,5,6,7,3"},"note":"The walker is on the node holding 7. This chain has ended, so the deferred successor holding 3 is popped and linked after it."},{"at":{"cur":2},"vars":{"stack":"[]","flat_so_far":"1,2,4,5,6,7,3"},"note":"The walker is on the node holding 3. There is no child, no successor and nothing deferred, so the walk is complete."}]}
```

```trace
{"cells":[1,2,3,4,7,8],"pointers":["parent","childHead","childTail","saved"],"steps":[{"at":{"parent":1,"childHead":4,"childTail":5,"saved":-1},"vars":{"forward":"1,2,3,4","backward":"4,3,2,1"},"note":"The parent holds 2 and has a child chain 7, 8. The main chain reads 1, 2, 3, 4 in both directions."},{"at":{"parent":1,"childHead":4,"childTail":5,"saved":2},"vars":{"forward":"1,2,3,4","backward":"4,3,2,1"},"note":"The parent's old successor, the node holding 3, is saved before any link changes."},{"at":{"parent":1,"childHead":4,"childTail":5,"saved":2},"vars":{"forward":"1,2,3,4","backward":"4,3,8,7"},"note":"The child tail is linked forward to the saved node and the saved node is linked back to the child tail. The main chain does not show the child yet, but the saved node's back link already reads 8."},{"at":{"parent":1,"childHead":4,"childTail":5,"saved":2},"vars":{"forward":"1,2,7,8,3,4","backward":"4,3,8,7,2,1"},"note":"The parent is linked forward to the child head and the child head back to the parent, and the child reference is cleared. Forward the list reads 1, 2, 7, 8, 3, 4, and backward from the end it reads 4, 3, 8, 7, 2, 1."}]}
```

<!-- stage: code -->
### Splice And Walk With A Stack

```java
final class FlattenCode {
    static final class Node {
        int value;
        Node prev, next, child;
        Node(int value) { this.value = value; }
    }

    static void spliceChild(Node parent) {
        Node childHead = parent.child;
        Node childTail = childHead;
        while (childTail.next != null) childTail = childTail.next;
        Node saved = parent.next;
        childTail.next = saved;
        if (saved != null) saved.prev = childTail;
        parent.next = childHead;
        childHead.prev = parent;
        parent.child = null;
    }

    static Node flatten(Node head) {
        java.util.ArrayDeque<Node> deferred = new java.util.ArrayDeque<>();
        Node cur = head;
        while (cur != null) {
            if (cur.child != null) {
                if (cur.next != null) deferred.addLast(cur.next);
                cur.next = cur.child;
                cur.next.prev = cur;
                cur.child = null;
            } else if (cur.next == null && !deferred.isEmpty()) {
                cur.next = deferred.removeLast();
                cur.next.prev = cur;
            }
            cur = cur.next;
        }
        return head;
    }
}
```

The stack-based walk visits every node once and pushes at most one entry per node with a child, so it is O(n) time. The extra space is the stack, bounded by the nesting depth. The single splice walks to the end of the child chain, which is linear in the size of that chain.

<!-- stage: applicability -->
### When Nodes Hide Further Chains

Reach for the deferred successor whenever a node may carry a nested structure that must be placed before the rest of its own chain, as in flattening nested lists, expanding macros, or walking a tree in preorder with a stack. The invariant is that everything behind the walker is final with symmetric links, and every suffix still to be placed is held either by the walker or on the stack, so that no node can be lost between steps.

The false friend is the forward-only repair. A flatten that sets only `next` produces a list that prints correctly and walks wrongly backward, which a one-directional test never reveals. A second false friend is forgetting to clear the child reference, which leaves nodes with two routes and makes later traversals duplicate them. A third is overwriting `parent.next` before the old successor is saved, which loses everything behind the parent.

Do not use the stack for structures that may share nodes between levels, since a node reachable twice would be placed twice. Prefer the single-splice form when nesting is shallow and the child chains are short, and the stack when the nesting is deep or the child chains are long. In Java, an explicit `ArrayDeque` avoids the stack overflow that a recursive version risks on deep nesting.

<!-- stage: exercises -->
### Exercises

#### [Build] Splice One Child Chain (Author exercise)
<!-- id: ll-splice-one-child -->

**Prerequisites.** The reverse and fixed-gap lessons of this chapter, which showed why the order of link edits matters.

**Problem.** A doubly linked chain is given by its values `main`, and one node of it, at position `p`, has a child chain given by `child`. Splice the child chain between that node and its old successor, keeping both `prev` and `next` links correct, and return the values of the result read forward.

**Constraints.** 1 <= main.length, child.length <= 10^5, 0 <= p < main.length and -10^9 <= value <= 10^9.

**Example 1.** Input `main = [1, 2, 3, 4]`, `p = 1`, `child = [7, 8]`, output `[1, 2, 7, 8, 3, 4]`.

**Example 2.** Input `main = [5]`, `p = 0`, `child = [6]`, output `[5, 6]`.

**Hint.** Which node must be saved first? What does the child tail point to when the parent has no successor?

**Changed decision.** First rung: the old successor is saved, the child tail is linked to it with its back link, and only then is the parent linked to the child head.

#### [Vary] Stack Of Deferred Successors (Author exercise)
<!-- id: ll-deferred-stack -->

**Prerequisites.** The Splice One Child Chain exercise above.

**Problem.** A multilevel list is written as text: values separated by spaces, and a child chain is a parenthesised group that belongs to the node written just before it. For example `1 2 (4 5 (6) 7) 3`. Flatten it with a stack of deferred successors, and return `[values, maxDepth]`, where `values` is the flattened order and `maxDepth` is the largest number of nodes the stack held at one time.

**Constraints.** At most 10^5 nodes, nesting depth at most 10^4 and -10^9 <= value <= 10^9. A group never appears before the first node.

**Example 1.** Input `1 2 (4 5 (6) 7) 3`, output `[[1, 2, 4, 5, 6, 7, 3], 2]`.

**Example 2.** Input `5 (6)`, output `[[5, 6], 0]`.

**Hint.** When is nothing pushed? When a node ends its chain, how does the walker know whether to pop?

**Changed decision.** The old successor is deferred on a stack instead of being reattached at once, and the walker pops it when a chain ends.

#### [Boundary] Child At Tail And Nested Child (Author exercise)
<!-- id: ll-flatten-back-links -->

**Prerequisites.** The two exercises above.

**Problem.** For the same text format, flatten the list and return the value of the previous node of every node, in flattened order, using -1 for the first node. The result shows whether the backward links are correct. Use only values that are distinct.

**Constraints.** At most 10^5 nodes, all values distinct and 0 <= value <= 10^9.

**Example 1.** Input `1 2 (4 5) 3`, output `[-1, 1, 2, 4, 5]`, since the flattened order is 1, 2, 4, 5, 3.

**Example 2.** Input `7 (8 (9))`, output `[-1, 7, 8]`.

**Hint.** Which node is the previous node of the successor after a child chain ends? What changes when the child chain belongs to the last node of its own chain?

**Changed decision.** The back link of every node is part of the output, so a flatten that repairs only forward links fails the tests.

#### [Recognize] Flatten a Multilevel Doubly Linked List (LeetCode 430)
<!-- id: ll-flatten-multilevel -->

**Prerequisites.** All three exercises above.

**Problem.** A doubly linked list has nodes with `prev`, `next` and `child` references, where a child is the head of another doubly linked list of the same kind. Flatten the list so that every node appears in depth-first preorder, with the child chain placed right after its parent, all `child` references set to null, and both `prev` and `next` correct. Return the flattened values. The input uses the text format of the previous exercises.

**Constraints.** At most 1000 nodes, 1 <= value <= 10^5.

**Example 1.** Input `3 6 (9 2) 5 (4 (8) 1)`, output `[3, 6, 9, 2, 5, 4, 8, 1]`.

**Example 2.** Input `1 (2 (3))`, output `[1, 2, 3]`.

**Hint.** Where does the successor of a parent go while its child chain is placed? After flattening, what must every `child` reference be?

**Changed decision.** Both directions and the child references are repaired, and the output must be the depth-first preorder of the whole structure.
