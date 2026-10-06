<!-- solutions-for: 10-multilevel-flattening -->
### Solutions For Flattening

#### Solution: [Build] Splice One Child Chain (Author exercise)
<!-- id: ll-splice-one -->

**Approach.**
The method copies the old successor of `parent` into `succ` before any write. A walk along the child chain finds the child tail. Then four writes join the pieces. The write `parent.next = child` links the parent to the first child node, and `child.prev = parent` links back. The write `tail.next = succ` links the child tail to the old successor, and `succ.prev = tail` links back when `succ` exists. Last, `parent.child = null` clears the child field.

The invariant is that every node of the main list and of the child chain stays reachable from `parent` or from `succ` after each statement, and each `next` write has its matching `prev` write.

**Complexity.**
- **Time** is O(c), where `c` is the length of the child chain, because the walk to the child tail visits each child node once.
- **Space** is O(1), because the method stores three references.

```java run
import java.util.*;

public final class SpliceOne {
    static final class Node {
        int val;
        Node prev, next, child;
        Node(int val) { this.val = val; }
    }

    /**
     * Splices parent's child chain between parent and its old successor.
     * Time: O(c) for a child chain of c nodes, because one walk finds the child tail.
     * Space: O(1), because three references are stored.
     * Invariant: every node stays reachable, and each next write has a matching prev write.
     */
    static void spliceOne(Node parent) {
        Node child = parent.child;
        Node succ = parent.next;                      // saved before any write; may be null
        Node tail = child;
        // One walk reaches the last node of the child chain.
        while (tail.next != null) tail = tail.next;
        parent.next = child;                          // parent to the first child node
        child.prev = parent;                          // and back
        tail.next = succ;                             // child tail to the old successor
        if (succ != null) succ.prev = tail;           // and back, when a successor exists
        parent.child = null;                          // the child chain now belongs to the main list
    }


    static int counter;

    /** Builds a random chain; order receives the preorder values (a node, then its child chain). */
    static Node chain(Random rnd, int depth, List<Integer> order) {
        int len = 1 + rnd.nextInt(4);
        Node head = null, tail = null;
        // One node per turn; a child chain is built right after its parent is recorded.
        for (int i = 0; i < len; i++) {
            Node n = new Node(counter++);
            order.add(n.val);
            if (depth > 0 && rnd.nextInt(3) == 0) n.child = chain(rnd, depth - 1, order);
            if (head == null) head = n; else { tail.next = n; n.prev = tail; }
            tail = n;
        }
        return head;
    }

    /** Checks forward order, backward order, prev symmetry and cleared children. */
    static void verify(Node head, List<Integer> order, String tag) {
        List<Integer> fwd = new ArrayList<>();
        Node prev = null, last = null;
        // Forward walk: every prev link must name the node we just left.
        for (Node c = head; c != null; c = c.next) {
            if (c.child != null) throw new AssertionError(tag + " child left");
            if (c.prev != prev) throw new AssertionError(tag + " prev link of " + c.val);
            fwd.add(c.val);
            prev = c; last = c;
        }
        if (!fwd.equals(order)) throw new AssertionError(tag + " forward " + fwd + " vs " + order);
        List<Integer> bwd = new ArrayList<>();
        // Backward walk from the last node must give the same sequence reversed.
        for (Node c = last; c != null; c = c.prev) bwd.add(c.val);
        Collections.reverse(bwd);
        if (!bwd.equals(order)) throw new AssertionError(tag + " backward " + bwd);
    }

    /** Builds a chain from explicit values; children are attached by the caller. */
    static Node plain(int... vals) {
        Node head = null, tail = null;
        for (int v : vals) {
            Node n = new Node(v);
            if (head == null) head = n; else { tail.next = n; n.prev = tail; }
            tail = n;
        }
        return head;
    }

    static Node at(Node head, int val) {
        for (Node c = head; c != null; c = c.next) if (c.val == val) return c;
        throw new AssertionError("missing " + val);
    }

    public static void main(String[] args) {
        // Example 1: 1,2,3 with child 7,8 on the node 2 reads 1,2,7,8,3 in both directions.
        Node h = plain(1, 2, 3);
        at(h, 2).child = plain(7, 8);
        spliceOne(at(h, 2));
        verify(h, List.of(1, 2, 7, 8, 3), "ex1");
        // Example 2: the parent is the last node, so the old successor is null.
        h = plain(1, 2);
        at(h, 2).child = plain(5);
        spliceOne(at(h, 2));
        verify(h, List.of(1, 2, 5), "ex2");
        // Random main lists, parents and plain child chains must match the array order.
        Random rnd = new Random(91);
        for (int t = 0; t < 500; t++) {
            int n = 1 + rnd.nextInt(5), c = 1 + rnd.nextInt(4), p = rnd.nextInt(n);
            int[] mainVals = new int[n], childVals = new int[c];
            for (int i = 0; i < n; i++) mainVals[i] = i;
            for (int i = 0; i < c; i++) childVals[i] = 100 + i;
            List<Integer> order = new ArrayList<>();
            for (int i = 0; i <= p; i++) order.add(mainVals[i]);
            for (int v : childVals) order.add(v);
            for (int i = p + 1; i < n; i++) order.add(mainVals[i]);
            Node head = plain(mainVals);
            at(head, p).child = plain(childVals);
            spliceOne(at(head, p));
            verify(head, order, "random " + t);
        }
    }
}
```

#### Solution: [Vary] Stack Of Deferred Successors (Author exercise)
<!-- id: ll-deferred-stack -->

**Approach.**
One walk moves a reference `curr` along the list. When `curr` has a child, the method pushes `curr.next` on the stack if it is not `null`, links `curr` to its child in both directions, and clears the child field. When `curr` is the last node of its chain and the stack is not empty, the method pops a saved successor and links `curr` to it in both directions. The walk then continues with `curr.next`. Because a chain ends at `null` before the saved successor is restored, the saved nodes come back in last-in first-out order, which matches the nesting.

The invariant is that the stack holds, from bottom to top, the successors of the open parents, so the node on top is the next node after the chain that the walk is in. The method also records the largest stack size.

**Complexity.**
- **Time** is O(n), because each node is visited once and each push and pop is O(1).
- **Space** is O(d), where `d` is the nesting depth, because the stack holds at most one saved successor per open parent.

```java run
import java.util.*;

public final class DeferredStack {
    static final class Node {
        int val;
        Node prev, next, child;
        Node(int val) { this.val = val; }
    }

    static int maxDeferred;                           // largest stack size of the last call

    /**
     * Flattens with an explicit stack of deferred successors and returns the head.
     * Time: O(n), because each node is visited once.
     * Space: O(d) for nesting depth d, because the stack holds one successor per open parent.
     * Invariant: the stack top is the node that follows the chain the walk is in.
     */
    static Node flattenWithStack(Node head) {
        Deque<Node> stack = new ArrayDeque<>();
        maxDeferred = 0;
        Node curr = head;
        // Each turn visits one node, so the loop makes n turns.
        while (curr != null) {
            if (curr.child != null) {
                // Defer the old successor; a null successor needs no entry.
                if (curr.next != null) { stack.push(curr.next); maxDeferred = Math.max(maxDeferred, stack.size()); }
                curr.next = curr.child;               // descend into the child chain
                curr.child.prev = curr;
                curr.child = null;
            }
            // At the end of a chain, resume at the most recently deferred successor.
            if (curr.next == null && !stack.isEmpty()) {
                Node resume = stack.pop();
                curr.next = resume;
                resume.prev = curr;
            }
            curr = curr.next;
        }
        return head;
    }


    static int counter;

    /** Builds a random chain; order receives the preorder values (a node, then its child chain). */
    static Node chain(Random rnd, int depth, List<Integer> order) {
        int len = 1 + rnd.nextInt(4);
        Node head = null, tail = null;
        // One node per turn; a child chain is built right after its parent is recorded.
        for (int i = 0; i < len; i++) {
            Node n = new Node(counter++);
            order.add(n.val);
            if (depth > 0 && rnd.nextInt(3) == 0) n.child = chain(rnd, depth - 1, order);
            if (head == null) head = n; else { tail.next = n; n.prev = tail; }
            tail = n;
        }
        return head;
    }

    /** Checks forward order, backward order, prev symmetry and cleared children. */
    static void verify(Node head, List<Integer> order, String tag) {
        List<Integer> fwd = new ArrayList<>();
        Node prev = null, last = null;
        // Forward walk: every prev link must name the node we just left.
        for (Node c = head; c != null; c = c.next) {
            if (c.child != null) throw new AssertionError(tag + " child left");
            if (c.prev != prev) throw new AssertionError(tag + " prev link of " + c.val);
            fwd.add(c.val);
            prev = c; last = c;
        }
        if (!fwd.equals(order)) throw new AssertionError(tag + " forward " + fwd + " vs " + order);
        List<Integer> bwd = new ArrayList<>();
        // Backward walk from the last node must give the same sequence reversed.
        for (Node c = last; c != null; c = c.prev) bwd.add(c.val);
        Collections.reverse(bwd);
        if (!bwd.equals(order)) throw new AssertionError(tag + " backward " + bwd);
    }

    /** Builds a chain from explicit values; children are attached by the caller. */
    static Node plain(int... vals) {
        Node head = null, tail = null;
        for (int v : vals) {
            Node n = new Node(v);
            if (head == null) head = n; else { tail.next = n; n.prev = tail; }
            tail = n;
        }
        return head;
    }

    static Node at(Node head, int val) {
        for (Node c = head; c != null; c = c.next) if (c.val == val) return c;
        throw new AssertionError("missing " + val);
    }

    public static void main(String[] args) {
        // Example 1: one level of nesting needs a stack of size 1.
        Node h = plain(1, 2, 3);
        at(h, 2).child = plain(7, 8);
        flattenWithStack(h);
        verify(h, List.of(1, 2, 7, 8, 3), "ex1");
        if (maxDeferred != 1) throw new AssertionError("ex1 stack " + maxDeferred);
        // Example 2: two nested levels need a stack of size 2.
        h = plain(1, 2, 3);
        at(h, 2).child = plain(7, 8, 9);
        at(at(h, 2).child, 8).child = plain(11, 12);
        flattenWithStack(h);
        verify(h, List.of(1, 2, 7, 8, 11, 12, 9, 3), "ex2");
        if (maxDeferred != 2) throw new AssertionError("ex2 stack " + maxDeferred);
        // The empty list returns null with a stack of size 0.
        if (flattenWithStack(null) != null || maxDeferred != 0) throw new AssertionError("empty");
        // Random multilevel lists must match the preorder oracle.
        Random rnd = new Random(92);
        for (int t = 0; t < 1000; t++) {
            List<Integer> order = new ArrayList<>();
            Node head = chain(rnd, 3, order);
            verify(flattenWithStack(head), order, "random " + t);
        }
    }
}
```

#### Solution: [Boundary] Child At Tail And Nested Child (Author exercise)
<!-- id: ll-child-edges -->

**Approach.**
The walk visits each node of the main list in order. At a node with a child, the method saves the old successor, finds the child tail, links the parent to the child chain in both directions, and links the child tail to the saved successor. The back link from the successor is written only when the successor exists, which covers a child chain that belongs to the last node of a list. After the splice, the walk moves to `curr.next`, which is the first child node, so a nested child is spliced when the walk reaches the node that owns it.

The invariant is that every node before `curr` is flattened and has no child, and every node from `curr` on is reachable through `next`, so no node is skipped or visited twice.

**Complexity.**
- **Time** is O(n), because each node is reached once by the walk and at most once by a tail search.
- **Space** is O(1), because the method stores four references.

```java run
import java.util.*;

public final class ChildEdges {
    static final class Node {
        int val;
        Node prev, next, child;
        Node(int val) { this.val = val; }
    }

    /**
     * Flattens in place and returns the head.
     * Time: O(n), because each node is walked once and searched for a tail at most once.
     * Space: O(1), because four references are stored.
     * Invariant: nodes before curr are flat, and nodes from curr stay reachable through next.
     */
    static Node flattenInPlace(Node head) {
        Node curr = head;
        // Spliced nodes follow curr, so nested children are met by the same walk.
        while (curr != null) {
            if (curr.child != null) {
                Node child = curr.child, succ = curr.next;   // succ is null when curr ends its chain
                Node tail = child;
                while (tail.next != null) tail = tail.next;  // find the child tail
                curr.next = child; child.prev = curr; curr.child = null;
                tail.next = succ;
                if (succ != null) succ.prev = tail;          // skipped when no successor exists
            }
            curr = curr.next;
        }
        return head;
    }


    static int counter;

    /** Builds a random chain; order receives the preorder values (a node, then its child chain). */
    static Node chain(Random rnd, int depth, List<Integer> order) {
        int len = 1 + rnd.nextInt(4);
        Node head = null, tail = null;
        // One node per turn; a child chain is built right after its parent is recorded.
        for (int i = 0; i < len; i++) {
            Node n = new Node(counter++);
            order.add(n.val);
            if (depth > 0 && rnd.nextInt(3) == 0) n.child = chain(rnd, depth - 1, order);
            if (head == null) head = n; else { tail.next = n; n.prev = tail; }
            tail = n;
        }
        return head;
    }

    /** Checks forward order, backward order, prev symmetry and cleared children. */
    static void verify(Node head, List<Integer> order, String tag) {
        List<Integer> fwd = new ArrayList<>();
        Node prev = null, last = null;
        // Forward walk: every prev link must name the node we just left.
        for (Node c = head; c != null; c = c.next) {
            if (c.child != null) throw new AssertionError(tag + " child left");
            if (c.prev != prev) throw new AssertionError(tag + " prev link of " + c.val);
            fwd.add(c.val);
            prev = c; last = c;
        }
        if (!fwd.equals(order)) throw new AssertionError(tag + " forward " + fwd + " vs " + order);
        List<Integer> bwd = new ArrayList<>();
        // Backward walk from the last node must give the same sequence reversed.
        for (Node c = last; c != null; c = c.prev) bwd.add(c.val);
        Collections.reverse(bwd);
        if (!bwd.equals(order)) throw new AssertionError(tag + " backward " + bwd);
    }

    /** Builds a chain from explicit values; children are attached by the caller. */
    static Node plain(int... vals) {
        Node head = null, tail = null;
        for (int v : vals) {
            Node n = new Node(v);
            if (head == null) head = n; else { tail.next = n; n.prev = tail; }
            tail = n;
        }
        return head;
    }

    static Node at(Node head, int val) {
        for (Node c = head; c != null; c = c.next) if (c.val == val) return c;
        throw new AssertionError("missing " + val);
    }

    public static void main(String[] args) {
        // Example 1: the child belongs to the last node, so the child tail ends the list.
        Node h = plain(1, 2);
        at(h, 2).child = plain(5, 6);
        flattenInPlace(h);
        verify(h, List.of(1, 2, 5, 6), "ex1");
        if (at(h, 6).next != null) throw new AssertionError("tail next");
        // Example 2: a child chain that holds one node with its own child.
        h = plain(1);
        h.child = plain(2);
        h.child.child = plain(3);
        flattenInPlace(h);
        verify(h, List.of(1, 2, 3), "ex2");
        // The empty list returns null.
        if (flattenInPlace(null) != null) throw new AssertionError("empty");
        // Random multilevel lists, up to four levels, must match the preorder oracle.
        Random rnd = new Random(93);
        for (int t = 0; t < 1000; t++) {
            List<Integer> order = new ArrayList<>();
            Node head = chain(rnd, 4, order);
            verify(flattenInPlace(head), order, "random " + t);
        }
    }
}
```

#### Solution: [Recognize] Flatten a Multilevel Doubly Linked List (LeetCode 430)
<!-- id: ll-flatten-430 -->

**Approach.**
The method `flattenChain(node)` flattens the chain that starts at `node` and returns its last node. It walks the chain. At a node with a child, it flattens the child chain first with a recursive call that returns the child's last node. Then it links the parent to the child chain, links the child's last node to the saved successor when one exists, and clears the child field. The returned last node is the last node of the child chain when the final node of the chain had a child, and that final node otherwise.

The invariant is that each recursive call returns the last node of a fully flattened chain, so the caller never searches for a tail. The recursion goes as deep as the nesting, which the constraints bound by 1000 nodes.

**Complexity.**
- **Time** is O(n), because each node is visited once.
- **Space** is O(d), where `d` is the nesting depth, because the call stack holds one frame per open child chain.

```java run
import java.util.*;

public final class Flatten430 {
    static final class Node {
        int val;
        Node prev, next, child;
        Node(int val) { this.val = val; }
    }

    /**
     * Flattens the chain starting at node and returns its last node.
     * Time: O(n), because each node is visited once.
     * Space: O(d) for nesting depth d, because the call stack holds one frame per open child chain.
     * Invariant: each call returns the last node of a flat chain.
     */
    static Node flattenChain(Node node) {
        Node curr = node, last = node;
        // The walk saves each successor before it rewires the links of curr.
        while (curr != null) {
            Node succ = curr.next;
            if (curr.child != null) {
                Node childLast = flattenChain(curr.child);   // the child chain is already flat
                curr.next = curr.child; curr.child.prev = curr;
                if (succ != null) { childLast.next = succ; succ.prev = childLast; }
                curr.child = null;
                last = childLast;                     // the chain now ends at the child's last node, unless succ continues it
            } else {
                last = curr;
            }
            curr = succ;
        }
        return last;
    }

    static Node flatten(Node head) {
        if (head != null) flattenChain(head);
        return head;
    }


    static int counter;

    /** Builds a random chain; order receives the preorder values (a node, then its child chain). */
    static Node chain(Random rnd, int depth, List<Integer> order) {
        int len = 1 + rnd.nextInt(4);
        Node head = null, tail = null;
        // One node per turn; a child chain is built right after its parent is recorded.
        for (int i = 0; i < len; i++) {
            Node n = new Node(counter++);
            order.add(n.val);
            if (depth > 0 && rnd.nextInt(3) == 0) n.child = chain(rnd, depth - 1, order);
            if (head == null) head = n; else { tail.next = n; n.prev = tail; }
            tail = n;
        }
        return head;
    }

    /** Checks forward order, backward order, prev symmetry and cleared children. */
    static void verify(Node head, List<Integer> order, String tag) {
        List<Integer> fwd = new ArrayList<>();
        Node prev = null, last = null;
        // Forward walk: every prev link must name the node we just left.
        for (Node c = head; c != null; c = c.next) {
            if (c.child != null) throw new AssertionError(tag + " child left");
            if (c.prev != prev) throw new AssertionError(tag + " prev link of " + c.val);
            fwd.add(c.val);
            prev = c; last = c;
        }
        if (!fwd.equals(order)) throw new AssertionError(tag + " forward " + fwd + " vs " + order);
        List<Integer> bwd = new ArrayList<>();
        // Backward walk from the last node must give the same sequence reversed.
        for (Node c = last; c != null; c = c.prev) bwd.add(c.val);
        Collections.reverse(bwd);
        if (!bwd.equals(order)) throw new AssertionError(tag + " backward " + bwd);
    }

    /** Builds a chain from explicit values; children are attached by the caller. */
    static Node plain(int... vals) {
        Node head = null, tail = null;
        for (int v : vals) {
            Node n = new Node(v);
            if (head == null) head = n; else { tail.next = n; n.prev = tail; }
            tail = n;
        }
        return head;
    }

    static Node at(Node head, int val) {
        for (Node c = head; c != null; c = c.next) if (c.val == val) return c;
        throw new AssertionError("missing " + val);
    }

    public static void main(String[] args) {
        // Example 1: nested children on the nodes 2 and 6.
        Node h = plain(1, 2, 3, 4);
        at(h, 2).child = plain(5, 6);
        at(at(h, 2).child, 6).child = plain(7);
        flatten(h);
        verify(h, List.of(1, 2, 5, 6, 7, 3, 4), "ex1");
        // Example 2: a child on the first node.
        h = plain(1, 2);
        h.child = plain(3);
        flatten(h);
        verify(h, List.of(1, 3, 2), "ex2");
        // The empty list returns null.
        if (flatten(null) != null) throw new AssertionError("empty");
        // Random multilevel lists must match the preorder oracle.
        Random rnd = new Random(94);
        for (int t = 0; t < 1000; t++) {
            List<Integer> order = new ArrayList<>();
            Node head = chain(rnd, 4, order);
            verify(flatten(head), order, "random " + t);
        }
    }
}
```
