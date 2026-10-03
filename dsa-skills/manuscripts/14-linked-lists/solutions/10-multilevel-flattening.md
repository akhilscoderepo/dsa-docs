<!-- solutions-for: 10-multilevel-flattening -->
### Multilevel Flattening

#### Solution: [Build] Splice One Child Chain (Author exercise)
<!-- id: ll-splice-one-child -->

**Approach.** Build the main chain with both `prev` and `next` links, build the child chain the same way, and attach its head to the parent's `child` field. To splice, save the parent's old successor, walk to the tail of the child chain, link that tail forward to the saved node and the saved node back to the tail, and only then link the parent forward to the child head and the child head back to the parent, clearing the child reference. If the parent has no successor, the saved node is null and the tail simply ends the chain. The assertions compare the forward order with list insertion, and walk back from the last node to confirm that the `prev` links give the exact reverse.

**Complexity.** O(m + c) time for a main chain of length m and a child chain of length c, and O(1) extra space.

```java run
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public final class SpliceOneChild {
    static final class Node {
        int value;
        Node prev, next, child;
        Node(int value) { this.value = value; }
    }
    static Node chain(int[] values) {
        Node head = null, tail = null;
        for (int v : values) {
            Node n = new Node(v);
            if (head == null) head = n;
            else { tail.next = n; n.prev = tail; }
            tail = n;
        }
        return head;
    }
    static void splice(Node parent) {
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
    static List<Integer> forward(Node head) {
        List<Integer> out = new ArrayList<>();
        for (Node c = head; c != null; c = c.next) out.add(c.value);
        return out;
    }
    static List<Integer> backwardFromEnd(Node head) {
        Node last = head;
        while (last.next != null) last = last.next;
        List<Integer> out = new ArrayList<>();
        for (Node c = last; c != null; c = c.prev) out.add(c.value);
        return out;
    }
    static Node run(int[] main, int p, int[] child) {
        Node head = chain(main);
        Node parent = head;
        for (int i = 0; i < p; i++) parent = parent.next;
        parent.child = chain(child);
        splice(parent);
        return head;
    }

    public static void main(String[] args) {
        if (!forward(run(new int[]{1, 2, 3, 4}, 1, new int[]{7, 8})).equals(List.of(1, 2, 7, 8, 3, 4))) throw new AssertionError("example 1");
        if (!forward(run(new int[]{5}, 0, new int[]{6})).equals(List.of(5, 6))) throw new AssertionError("example 2");
        Random rnd = new Random(1437);
        for (int t = 0; t < 4000; t++) {
            int m = 1 + rnd.nextInt(8), c = 1 + rnd.nextInt(6);
            int[] main = new int[m], child = new int[c];
            for (int i = 0; i < m; i++) main[i] = rnd.nextInt(100);
            for (int i = 0; i < c; i++) child[i] = rnd.nextInt(100);
            int p = rnd.nextInt(m);
            List<Integer> expected = new ArrayList<>();
            for (int v : main) expected.add(v);
            List<Integer> insert = new ArrayList<>();
            for (int v : child) insert.add(v);
            expected.addAll(p + 1, insert);
            Node head = run(main, p, child);
            if (!forward(head).equals(expected)) throw new AssertionError("forward order is wrong");
            List<Integer> reversed = new ArrayList<>(expected);
            java.util.Collections.reverse(reversed);
            if (!backwardFromEnd(head).equals(reversed)) throw new AssertionError("back links are wrong");
        }
    }
}
```

#### Solution: [Vary] Stack Of Deferred Successors (Author exercise)
<!-- id: ll-deferred-stack -->

**Approach.** Parse the text into nodes, with each parenthesised group attached to the node before it. Then walk with a cursor. When the cursor has a child, push its successor if it has one, link the cursor forward to the child and the child back to the cursor, and clear the child reference. When the cursor has no child and no successor and the stack is not empty, pop a successor and link it after the cursor. Track the largest stack size. The oracle computes the preorder by recursion, and computes the largest depth by counting, for each node with a child, the ancestors that still have a successor waiting, which is the number of entries the stack would hold at that moment.

**Complexity.** O(n) time and O(d) extra space for nesting depth d.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public final class DeferredStack {
    static final class Node {
        int value;
        Node prev, next, child;
        Node(int value) { this.value = value; }
    }
    static String[] tok;
    static int pos;
    static Node parseChain() {
        Node head = null, tail = null;
        while (pos < tok.length && !tok[pos].equals(")")) {
            if (tok[pos].equals("(")) {
                pos++;
                tail.child = parseChain();
                pos++;
            } else {
                Node n = new Node(Integer.parseInt(tok[pos++]));
                if (head == null) head = n;
                else { tail.next = n; n.prev = tail; }
                tail = n;
            }
        }
        return head;
    }
    static Node parse(String s) {
        tok = s.replace("(", " ( ").replace(")", " ) ").trim().split("\\s+");
        pos = 0;
        return parseChain();
    }
    static int maxDepth;
    static List<Integer> flatten(Node head) {
        ArrayDeque<Node> deferred = new ArrayDeque<>();
        maxDepth = 0;
        Node cur = head;
        while (cur != null) {
            if (cur.child != null) {
                if (cur.next != null) deferred.addLast(cur.next);
                maxDepth = Math.max(maxDepth, deferred.size());
                cur.next = cur.child;
                cur.next.prev = cur;
                cur.child = null;
            } else if (cur.next == null && !deferred.isEmpty()) {
                cur.next = deferred.removeLast();
                cur.next.prev = cur;
            }
            cur = cur.next;
        }
        List<Integer> out = new ArrayList<>();
        for (Node c = head; c != null; c = c.next) out.add(c.value);
        return out;
    }
    static void preorder(Node chain, List<Integer> out) {
        for (Node c = chain; c != null; c = c.next) {
            out.add(c.value);
            if (c.child != null) preorder(c.child, out);
        }
    }
    static int oracleDepth(Node chain, int pending) {
        int best = pending;
        for (Node c = chain; c != null; c = c.next)
            if (c.child != null) best = Math.max(best, oracleDepth(c.child, pending + (c.next != null ? 1 : 0)));
        return best;
    }
    static String randomText(Random rnd, int budget, int[] counter, int depth) {
        StringBuilder sb = new StringBuilder();
        int len = 1 + rnd.nextInt(3);
        for (int i = 0; i < len && counter[0] < budget; i++) {
            sb.append(counter[0]++).append(' ');
            if (depth < 3 && counter[0] < budget && rnd.nextInt(3) == 0) {
                sb.append("( ").append(randomText(rnd, budget, counter, depth + 1)).append(") ");
            }
        }
        return sb.toString();
    }

    public static void main(String[] args) {
        Node a = parse("1 2 (4 5 (6) 7) 3");
        List<Integer> got = flatten(a);
        if (!got.equals(List.of(1, 2, 4, 5, 6, 7, 3)) || maxDepth != 2) throw new AssertionError("example 1");
        Node b = parse("5 (6)");
        got = flatten(b);
        if (!got.equals(List.of(5, 6)) || maxDepth != 0) throw new AssertionError("example 2");
        Random rnd = new Random(1438);
        for (int t = 0; t < 3000; t++) {
            String text = randomText(rnd, 1 + rnd.nextInt(12), new int[]{0}, 0).trim();
            Node head = parse(text);
            List<Integer> expected = new ArrayList<>();
            preorder(head, expected);
            int expectedDepth = oracleDepth(head, 0);
            List<Integer> flat = flatten(head);
            if (!flat.equals(expected)) throw new AssertionError("wrong order for: " + text);
            if (maxDepth != expectedDepth) throw new AssertionError("wrong depth for: " + text + " got " + maxDepth + " expected " + expectedDepth);
        }
    }
}
```

#### Solution: [Boundary] Child At Tail And Nested Child (Author exercise)
<!-- id: ll-flatten-back-links -->

**Approach.** Flatten with the stack of deferred successors, setting both `next` and `prev` at every splice and at every pop. After the walk, read the `prev` link of every node in the flattened order, using -1 for the null link of the first node. A child chain at the tail of its own chain has no successor to defer, so nothing is pushed and the walk ends with an empty stack, which is also checked. A nested child pushes a second entry, and when the inner chain ends its deferred successor is popped and linked back to the inner tail. The oracle is the preorder of the structure: in a correct flatten, the previous node of each node is simply the node before it in that order.

**Complexity.** O(n) time and O(d) extra space for nesting depth d.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public final class FlattenBackLinks {
    static final class Node {
        int value;
        Node prev, next, child;
        Node(int value) { this.value = value; }
    }
    static String[] tok;
    static int pos;
    static Node parseChain() {
        Node head = null, tail = null;
        while (pos < tok.length && !tok[pos].equals(")")) {
            if (tok[pos].equals("(")) {
                pos++;
                tail.child = parseChain();
                pos++;
            } else {
                Node n = new Node(Integer.parseInt(tok[pos++]));
                if (head == null) head = n;
                else { tail.next = n; n.prev = tail; }
                tail = n;
            }
        }
        return head;
    }
    static Node parse(String s) {
        tok = s.replace("(", " ( ").replace(")", " ) ").trim().split("\\s+");
        pos = 0;
        return parseChain();
    }
    static List<Integer> backValues(Node head) {
        ArrayDeque<Node> deferred = new ArrayDeque<>();
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
        if (!deferred.isEmpty()) throw new AssertionError("the stack must be empty at the end");
        List<Integer> out = new ArrayList<>();
        for (Node c = head; c != null; c = c.next) out.add(c.prev == null ? -1 : c.prev.value);
        return out;
    }
    static void preorder(Node chain, List<Integer> out) {
        for (Node c = chain; c != null; c = c.next) {
            out.add(c.value);
            if (c.child != null) preorder(c.child, out);
        }
    }
    static String randomText(Random rnd, int budget, int[] counter, int depth) {
        StringBuilder sb = new StringBuilder();
        int len = 1 + rnd.nextInt(3);
        for (int i = 0; i < len && counter[0] < budget; i++) {
            sb.append(counter[0]++).append(' ');
            if (depth < 3 && counter[0] < budget && rnd.nextInt(3) == 0) {
                sb.append("( ").append(randomText(rnd, budget, counter, depth + 1)).append(") ");
            }
        }
        return sb.toString();
    }

    public static void main(String[] args) {
        if (!backValues(parse("1 2 (4 5) 3")).equals(List.of(-1, 1, 2, 4, 5))) throw new AssertionError("example 1");
        if (!backValues(parse("7 (8 (9))")).equals(List.of(-1, 7, 8))) throw new AssertionError("example 2");
        Random rnd = new Random(1439);
        for (int t = 0; t < 3000; t++) {
            String text = randomText(rnd, 1 + rnd.nextInt(14), new int[]{0}, 0).trim();
            List<Integer> order = new ArrayList<>();
            preorder(parse(text), order);
            List<Integer> expected = new ArrayList<>();
            expected.add(-1);
            for (int i = 0; i + 1 < order.size(); i++) expected.add(order.get(i));
            if (!backValues(parse(text)).equals(expected)) throw new AssertionError("wrong back links for: " + text);
        }
    }
}
```

#### Solution: [Recognize] Flatten a Multilevel Doubly Linked List (LeetCode 430)
<!-- id: ll-flatten-multilevel -->

**Approach.** Walk the structure in play order with an explicit stack of deferred successors. A node with a child pushes its own successor, if there is one, becomes linked forward to the child head and backward from it, and loses its child reference. A node that ends its chain pops the top deferred successor and links to it in both directions. After the walk every node is on one chain, in depth-first preorder, with symmetric links and no child reference. An explicit stack is used because a recursive version overflows the call stack on deep nesting, which the assertions demonstrate with a structure of 200000 levels. The assertions compare with a recursive preorder on small random structures, check that every child reference is null, and check the back links.

**Complexity.** O(n) time and O(d) extra space for nesting depth d.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public final class FlattenMultilevel {
    static final class Node {
        int value;
        Node prev, next, child;
        Node(int value) { this.value = value; }
    }
    static String[] tok;
    static int pos;
    static Node parseChain() {
        Node head = null, tail = null;
        while (pos < tok.length && !tok[pos].equals(")")) {
            if (tok[pos].equals("(")) {
                pos++;
                tail.child = parseChain();
                pos++;
            } else {
                Node n = new Node(Integer.parseInt(tok[pos++]));
                if (head == null) head = n;
                else { tail.next = n; n.prev = tail; }
                tail = n;
            }
        }
        return head;
    }
    static Node parse(String s) {
        tok = s.replace("(", " ( ").replace(")", " ) ").trim().split("\\s+");
        pos = 0;
        return parseChain();
    }
    static Node flatten(Node head) {
        ArrayDeque<Node> deferred = new ArrayDeque<>();
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
    static void preorder(Node chain, List<Integer> out) {
        for (Node c = chain; c != null; c = c.next) {
            out.add(c.value);
            if (c.child != null) preorder(c.child, out);
        }
    }
    static int collectDepth(Node t) {
        int count = 0;
        for (Node cur = t; cur != null; cur = cur.next) {
            count++;
            if (cur.child != null) count += collectDepth(cur.child);
        }
        return count;
    }
    static List<Integer> values(Node head) {
        List<Integer> out = new ArrayList<>();
        for (Node c = head; c != null; c = c.next) out.add(c.value);
        return out;
    }
    static void checkStructure(Node head, int expectedCount) {
        int n = 0;
        Node last = null;
        for (Node c = head; c != null; c = c.next) {
            if (c.child != null) throw new AssertionError("a child reference remains");
            if (c.next != null && c.next.prev != c) throw new AssertionError("links are not symmetric");
            last = c;
            n++;
        }
        if (n != expectedCount) throw new AssertionError("a node was lost");
        int back = 0;
        for (Node c = last; c != null; c = c.prev) back++;
        if (back != n) throw new AssertionError("walking back visits a different number of nodes");
    }
    static String randomText(Random rnd, int budget, int[] counter, int depth) {
        StringBuilder sb = new StringBuilder();
        int len = 1 + rnd.nextInt(3);
        for (int i = 0; i < len && counter[0] < budget; i++) {
            sb.append(1 + counter[0]++).append(' ');
            if (depth < 3 && counter[0] < budget && rnd.nextInt(3) == 0) {
                sb.append("( ").append(randomText(rnd, budget, counter, depth + 1)).append(") ");
            }
        }
        return sb.toString();
    }

    public static void main(String[] args) {
        Node a = flatten(parse("3 6 (9 2) 5 (4 (8) 1)"));
        if (!values(a).equals(List.of(3, 6, 9, 2, 5, 4, 8, 1))) throw new AssertionError("example 1");
        checkStructure(a, 8);
        Node b = flatten(parse("1 (2 (3))"));
        if (!values(b).equals(List.of(1, 2, 3))) throw new AssertionError("example 2");
        checkStructure(b, 3);
        Random rnd = new Random(1440);
        for (int t = 0; t < 3000; t++) {
            String text = randomText(rnd, 1 + rnd.nextInt(14), new int[]{0}, 0).trim();
            Node head = parse(text);
            List<Integer> expected = new ArrayList<>();
            preorder(head, expected);
            Node flat = flatten(head);
            if (!values(flat).equals(expected)) throw new AssertionError("wrong order for: " + text);
            checkStructure(flat, expected.size());
        }
        int levels = 200000;
        Node deepHead = new Node(0);
        Node holder = deepHead;
        for (int i = 1; i < levels; i++) {
            Node n = new Node(i);
            holder.child = n;
            holder = n;
        }
        Node flatDeep = flatten(deepHead);
        checkStructure(flatDeep, levels);
        Node deepAgain = new Node(0);
        holder = deepAgain;
        for (int i = 1; i < levels; i++) {
            Node n = new Node(i);
            holder.child = n;
            holder = n;
        }
        boolean overflowed = false;
        try { collectDepth(deepAgain); }
        catch (StackOverflowError expected) { overflowed = true; }
        if (!overflowed) throw new AssertionError("a recursive walk should overflow the stack at this depth");
    }
}
```
