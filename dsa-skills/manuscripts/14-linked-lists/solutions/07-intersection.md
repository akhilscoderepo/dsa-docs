<!-- solutions-for: 07-intersection -->
### Intersection

#### Solution: [Build] Compare Node Identity (Author exercise)
<!-- id: ll-compare-identity -->

**Approach.** Build the shared nodes once and link them behind the private nodes of each list, so that the two lists end in the very same node objects. Put every node of the second list into an identity-based set, and count the nodes of the first list that are in it, which is the identity count. For the value count, put the values of the second list into an ordinary set and count the nodes of the first list whose value is in it. The two counts differ exactly when different nodes hold equal values. The assertions compare the identity count with the length of the shared part, and show a case where the value count is larger.

**Complexity.** O(n + m) time and O(m) extra space for the sets, which is acceptable here because the exercise asks for a count and not for constant space.

```java run
import java.util.HashSet;
import java.util.IdentityHashMap;
import java.util.Random;
import java.util.Set;

public final class CompareIdentity {
    static final class Node {
        int value;
        Node next;
        Node(int value) { this.value = value; }
    }
    static Node chain(int[] values, Node tail) {
        Node head = tail;
        for (int i = values.length - 1; i >= 0; i--) {
            Node n = new Node(values[i]);
            n.next = head;
            head = n;
        }
        return head;
    }
    static int[] counts(int[] a, int[] b, int[] shared) {
        Node tail = chain(shared, null);
        Node headA = chain(a, tail), headB = chain(b, tail);
        IdentityHashMap<Node, Boolean> inB = new IdentityHashMap<>();
        Set<Integer> valuesB = new HashSet<>();
        for (Node cur = headB; cur != null; cur = cur.next) { inB.put(cur, true); valuesB.add(cur.value); }
        int identity = 0, byValue = 0;
        for (Node cur = headA; cur != null; cur = cur.next) {
            if (inB.containsKey(cur)) identity++;
            if (valuesB.contains(cur.value)) byValue++;
        }
        return new int[]{identity, byValue};
    }

    public static void main(String[] args) {
        if (!java.util.Arrays.equals(counts(new int[]{1, 2}, new int[]{1, 5}, new int[]{8, 9}), new int[]{2, 3})) throw new AssertionError("example 1");
        if (!java.util.Arrays.equals(counts(new int[]{3}, new int[]{3}, new int[]{}), new int[]{0, 1})) throw new AssertionError("example 2");
        Random rnd = new Random(1425);
        for (int t = 0; t < 4000; t++) {
            int[] a = new int[rnd.nextInt(5)], b = new int[rnd.nextInt(5)], s = new int[rnd.nextInt(5)];
            for (int i = 0; i < a.length; i++) a[i] = rnd.nextInt(4);
            for (int i = 0; i < b.length; i++) b[i] = rnd.nextInt(4);
            for (int i = 0; i < s.length; i++) s[i] = rnd.nextInt(4);
            int[] got = counts(a, b, s);
            if (got[0] != s.length) throw new AssertionError("identity matches must equal the shared length");
            if (got[1] < got[0]) throw new AssertionError("value matches can never be fewer than identity matches");
        }
    }
}
```

#### Solution: [Vary] Align By Length (Author exercise)
<!-- id: ll-align-by-length -->

**Approach.** Count the nodes of both lists. Advance the pointer of the longer list by the difference of the lengths, so that both pointers are the same distance from the end. Then move both pointers together until they are the same node, which happens at the first shared node, or when both become null if there is none. The answer holds the two lengths and the value at the stopping node, or -1 for null. The assertions compare with a nested-loop search for the first node of the first list that is also in the second list.

**Complexity.** O(n + m) time and O(1) extra space.

```java run
import java.util.Random;

public final class AlignByLength {
    static final class Node {
        int value;
        Node next;
        Node(int value) { this.value = value; }
    }
    static Node chain(int[] values, Node tail) {
        Node head = tail;
        for (int i = values.length - 1; i >= 0; i--) {
            Node n = new Node(values[i]);
            n.next = head;
            head = n;
        }
        return head;
    }
    static int length(Node head) {
        int n = 0;
        for (Node cur = head; cur != null; cur = cur.next) n++;
        return n;
    }
    static int[] align(Node headA, Node headB) {
        int lenA = length(headA), lenB = length(headB);
        Node a = headA, b = headB;
        for (int i = lenA; i > lenB; i--) a = a.next;
        for (int i = lenB; i > lenA; i--) b = b.next;
        while (a != b) {
            a = a.next;
            b = b.next;
        }
        return new int[]{lenA, lenB, a == null ? -1 : a.value};
    }
    static int nested(Node headA, Node headB) {
        for (Node a = headA; a != null; a = a.next)
            for (Node b = headB; b != null; b = b.next)
                if (a == b) return a.value;
        return -1;
    }

    public static void main(String[] args) {
        Node tail = chain(new int[]{8, 4, 5}, null);
        if (!java.util.Arrays.equals(align(chain(new int[]{4, 1}, tail), chain(new int[]{5, 6, 1}, tail)), new int[]{5, 6, 8})) throw new AssertionError("example 1");
        if (!java.util.Arrays.equals(align(chain(new int[]{1}, null), chain(new int[]{2, 3}, null)), new int[]{1, 2, -1})) throw new AssertionError("example 2");
        Random rnd = new Random(1426);
        for (int t = 0; t < 5000; t++) {
            int[] a = new int[rnd.nextInt(6)], b = new int[rnd.nextInt(6)], s = new int[rnd.nextInt(5)];
            for (int i = 0; i < a.length; i++) a[i] = rnd.nextInt(4);
            for (int i = 0; i < b.length; i++) b[i] = rnd.nextInt(4);
            for (int i = 0; i < s.length; i++) s[i] = rnd.nextInt(4);
            Node sharedTail = chain(s, null);
            Node headA = chain(a, sharedTail), headB = chain(b, sharedTail);
            int[] got = align(headA, headB);
            if (got[0] != a.length + s.length || got[1] != b.length + s.length) throw new AssertionError("lengths are wrong");
            if (got[2] != nested(headA, headB)) throw new AssertionError("disagrees with the nested search");
        }
    }
}
```

#### Solution: [Boundary] No Intersection And Shared Head (Author exercise)
<!-- id: ll-switch-rounds -->

**Approach.** Start `pa` and `pb` at the two heads and, while they are different, move each one step, sending a null pointer to the other list's head. Count the rounds in which this happens. If both heads are the same node the loop body never runs and the count is 0. If there is no shared node, both pointers become null in the same round, and the equality of two nulls ends the loop. The result records whether the stopping node is real. The assertions compare with a path-based oracle: the pointer `pa` visits the nodes of its own list, then a null, then the nodes of the other list, and `pb` does the same in the opposite order, so the answer is the first index at which the two sequences agree.

**Complexity.** O(n + m) time and O(1) extra space.

```java run
import java.util.Random;

public final class SwitchRounds {
    static final class Node {
        int id;
        Node next;
        Node(int id) { this.id = id; }
    }
    static int nextId;
    static Node chain(int count, Node tail) {
        Node head = tail;
        for (int i = 0; i < count; i++) {
            Node n = new Node(nextId++);
            n.next = head;
            head = n;
        }
        return head;
    }
    static int[] walk(Node headA, Node headB) {
        Node pa = headA, pb = headB;
        int rounds = 0;
        while (pa != pb) {
            pa = pa == null ? headB : pa.next;
            pb = pb == null ? headA : pb.next;
            rounds++;
        }
        return new int[]{pa == null ? 0 : 1, rounds};
    }
    static int[] oracle(Node headA, Node headB) {
        java.util.List<Integer> seqA = new java.util.ArrayList<>(), seqB = new java.util.ArrayList<>();
        for (Node c = headA; c != null; c = c.next) seqA.add(c.id);
        seqA.add(-1);
        for (Node c = headB; c != null; c = c.next) seqA.add(c.id);
        seqA.add(-1);
        for (Node c = headB; c != null; c = c.next) seqB.add(c.id);
        seqB.add(-1);
        for (Node c = headA; c != null; c = c.next) seqB.add(c.id);
        seqB.add(-1);
        for (int k = 0; k < seqA.size(); k++)
            if (seqA.get(k).equals(seqB.get(k))) return new int[]{seqA.get(k) == -1 ? 0 : 1, k};
        throw new AssertionError("the sequences must agree at the final null");
    }

    public static void main(String[] args) {
        nextId = 0;
        if (!java.util.Arrays.equals(walk(chain(2, null), chain(1, null)), new int[]{0, 4})) throw new AssertionError("example 1");
        nextId = 0;
        Node shared = chain(2, null);
        if (!java.util.Arrays.equals(walk(shared, shared), new int[]{1, 0})) throw new AssertionError("example 2");
        if (!java.util.Arrays.equals(walk(null, null), new int[]{0, 0})) throw new AssertionError("both empty");
        Random rnd = new Random(1427);
        for (int t = 0; t < 6000; t++) {
            nextId = 0;
            Node sharedTail = chain(rnd.nextInt(4), null);
            Node headA = chain(rnd.nextInt(5), sharedTail), headB = chain(rnd.nextInt(5), sharedTail);
            if (!java.util.Arrays.equals(walk(headA, headB), oracle(headA, headB))) throw new AssertionError("disagrees with the path oracle");
        }
    }
}
```

#### Solution: [Recognize] Intersection of Two Linked Lists (LeetCode 160)
<!-- id: ll-intersection-lists -->

**Approach.** Walk two pointers, one from each head. When a pointer reaches the end of its list it continues from the head of the other list. Each pointer then covers its own list followed by the other list's private part before reaching the shared nodes, so both have walked the same total number of nodes when they first coincide. They coincide on the first shared node, or in null together if the lists do not meet. The answer is the value at that node, or -1. The assertions compare with a nested identity search, including lists that share a whole list, one empty list, and lists with equal values but no shared node.

**Complexity.** O(n + m) time and O(1) extra space.

```java run
import java.util.Random;

public final class IntersectionLists {
    static final class Node {
        int value;
        Node next;
        Node(int value) { this.value = value; }
    }
    static Node chain(int[] values, Node tail) {
        Node head = tail;
        for (int i = values.length - 1; i >= 0; i--) {
            Node n = new Node(values[i]);
            n.next = head;
            head = n;
        }
        return head;
    }
    static int firstShared(Node headA, Node headB) {
        Node pa = headA, pb = headB;
        while (pa != pb) {
            pa = pa == null ? headB : pa.next;
            pb = pb == null ? headA : pb.next;
        }
        return pa == null ? -1 : pa.value;
    }
    static int nested(Node headA, Node headB) {
        for (Node a = headA; a != null; a = a.next)
            for (Node b = headB; b != null; b = b.next)
                if (a == b) return a.value;
        return -1;
    }

    public static void main(String[] args) {
        Node tail = chain(new int[]{8, 4, 5}, null);
        if (firstShared(chain(new int[]{4, 1, 3}, tail), chain(new int[]{6, 5}, tail)) != 8) throw new AssertionError("example 1");
        if (firstShared(chain(new int[]{2, 6, 4}, null), chain(new int[]{1, 5}, null)) != -1) throw new AssertionError("example 2");
        Node same = chain(new int[]{3, 3}, null);
        if (firstShared(same, same) != 3) throw new AssertionError("the same list twice");
        if (firstShared(chain(new int[]{5, 5}, null), chain(new int[]{5, 5}, null)) != -1) throw new AssertionError("equal values without shared nodes");
        Random rnd = new Random(1428);
        for (int t = 0; t < 6000; t++) {
            int[] a = new int[rnd.nextInt(6)], b = new int[rnd.nextInt(6)], s = new int[rnd.nextInt(5)];
            for (int i = 0; i < a.length; i++) a[i] = 1 + rnd.nextInt(3);
            for (int i = 0; i < b.length; i++) b[i] = 1 + rnd.nextInt(3);
            for (int i = 0; i < s.length; i++) s[i] = 1 + rnd.nextInt(3);
            Node sharedTail = chain(s, null);
            Node headA = chain(a, sharedTail), headB = chain(b, sharedTail);
            if (firstShared(headA, headB) != nested(headA, headB)) throw new AssertionError("disagrees with the nested search");
        }
    }
}
```
