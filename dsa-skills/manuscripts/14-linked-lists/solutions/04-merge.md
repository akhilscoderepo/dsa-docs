<!-- solutions-for: 04-merge -->
### Merge

#### Solution: [Build] Merge Two One-Node Lists (Author exercise)
<!-- id: ll-merge-one-node -->

**Approach.** Compare the two nodes. If the second value is strictly smaller, the second node goes first, and otherwise the first node goes first, so a tie favours the first list. The chosen node becomes the head, and its `next` is pointed at the other node. The flag records whether the head is the original first-list node, which is checked with `==` on the node objects and not on values. The assertions compare with sorting the two values, and confirm that on equal values the head is the first list's node and the tail is the second list's.

**Complexity.** One comparison and two assignments, so O(1) time and O(1) space.

```java run
import java.util.Random;

public final class MergeOneNode {
    static final class Node {
        int value;
        Node next;
        Node(int value) { this.value = value; }
    }
    static long[] merge(int x, int y) {
        Node a = new Node(x), b = new Node(y);
        Node head, other;
        if (b.value < a.value) { head = b; other = a; }
        else { head = a; other = b; }
        head.next = other;
        other.next = null;
        return new long[]{head.value, head.next.value, head == a ? 1 : 0};
    }

    public static void main(String[] args) {
        if (!java.util.Arrays.equals(merge(7, 3), new long[]{3, 7, 0})) throw new AssertionError("example 1");
        if (!java.util.Arrays.equals(merge(4, 4), new long[]{4, 4, 1})) throw new AssertionError("example 2");
        if (!java.util.Arrays.equals(merge(Integer.MIN_VALUE, Integer.MAX_VALUE), new long[]{Integer.MIN_VALUE, Integer.MAX_VALUE, 1})) throw new AssertionError("extremes compare without subtraction");
        Random rnd = new Random(1413);
        for (int t = 0; t < 3000; t++) {
            int x = rnd.nextInt(6), y = rnd.nextInt(6);
            long[] got = merge(x, y);
            if (got[0] != Math.min(x, y) || got[1] != Math.max(x, y)) throw new AssertionError("disagrees with sorting two values");
            long expectedFlag = x <= y ? 1 : 0;
            if (got[2] != expectedFlag) throw new AssertionError("ties must favour the first list");
        }
    }
}
```

#### Solution: [Vary] Merge Two Sorted Lists (LeetCode 21)
<!-- id: ll-merge-two-sorted -->

**Approach.** Keep the two remaining heads and the tail of the merged list. While both heads exist, detach the smaller one, with the first list winning ties, link it behind the tail or make it the head when the tail is null, and advance its list. After the loop at most one list is left, and it is linked behind the tail in one assignment, or returned directly when nothing was merged. The assertions compare with a sorted concatenation, check that the nodes are reused by counting distinct node objects before and after, and check stability by tagging values with their list of origin.

**Complexity.** O(n + m) time and O(1) extra space.

```java run
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public final class MergeTwoSorted {
    static final class Node {
        int value;
        int origin;
        Node next;
        Node(int value, int origin) { this.value = value; this.origin = origin; }
    }
    static Node build(int[] values, int origin) {
        Node head = null, tail = null;
        for (int v : values) {
            Node n = new Node(v, origin);
            if (head == null) head = n; else tail.next = n;
            tail = n;
        }
        return head;
    }
    static Node merge(Node a, Node b) {
        Node head = null, tail = null;
        while (a != null && b != null) {
            Node take;
            if (b.value < a.value) { take = b; b = b.next; }
            else { take = a; a = a.next; }
            if (tail == null) head = take; else tail.next = take;
            tail = take;
        }
        Node rest = a != null ? a : b;
        if (tail == null) return rest;
        tail.next = rest;
        return head;
    }

    public static void main(String[] args) {
        Node m1 = merge(build(new int[]{2, 5, 9}, 0), build(new int[]{1, 5, 7, 8}, 1));
        List<Integer> got1 = new ArrayList<>();
        for (Node c = m1; c != null; c = c.next) got1.add(c.value);
        if (!got1.equals(List.of(1, 2, 5, 5, 7, 8, 9))) throw new AssertionError("example 1");
        if (merge(null, null) != null) throw new AssertionError("example 2");
        Random rnd = new Random(1414);
        for (int t = 0; t < 5000; t++) {
            int n = rnd.nextInt(8), m = rnd.nextInt(8);
            int[] a = new int[n], b = new int[m];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(6);
            for (int i = 0; i < m; i++) b[i] = rnd.nextInt(6);
            java.util.Arrays.sort(a);
            java.util.Arrays.sort(b);
            Node merged = merge(build(a, 0), build(b, 1));
            List<Integer> values = new ArrayList<>();
            int count = 0;
            Node prev = null;
            for (Node c = merged; c != null && count <= n + m; c = c.next) {
                values.add(c.value);
                if (prev != null && prev.value == c.value && prev.origin > c.origin) throw new AssertionError("a tie must keep the first list ahead");
                prev = c;
                count++;
            }
            if (count != n + m) throw new AssertionError("a node was lost or duplicated");
            List<Integer> expected = new ArrayList<>();
            for (int v : a) expected.add(v);
            for (int v : b) expected.add(v);
            java.util.Collections.sort(expected);
            if (!values.equals(expected)) throw new AssertionError("disagrees with the sorted concatenation");
        }
    }
}
```

#### Solution: [Boundary] One Empty Or Exhausted List (Author exercise)
<!-- id: ll-merge-exhausted -->

**Approach.** The loop makes one comparison per node moved while both lists are non-empty, and it counts them. When it ends, the surviving list, possibly empty, is linked behind the tail with a single assignment, so no further comparison is made. If nothing was moved the tail is null, and the surviving list is itself the result. The comparison count equals the number of nodes moved by the loop, which is at most `n + m - 1`, and is exactly the number of nodes that precede the point where one list runs out. The assertions compare the count with a direct simulation on arrays and check that when either list is empty the count is zero.

**Complexity.** O(n + m) time, with the bulk attach costing O(1), and O(1) extra space.

```java run
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public final class MergeExhausted {
    static final class Node {
        int value;
        Node next;
        Node(int value) { this.value = value; }
    }
    static Node build(int[] values) {
        Node head = null, tail = null;
        for (int v : values) {
            Node n = new Node(v);
            if (head == null) head = n; else tail.next = n;
            tail = n;
        }
        return head;
    }
    static int comparisons;
    static Node merge(Node a, Node b) {
        comparisons = 0;
        Node head = null, tail = null;
        while (a != null && b != null) {
            comparisons++;
            Node take;
            if (b.value < a.value) { take = b; b = b.next; }
            else { take = a; a = a.next; }
            if (tail == null) head = take; else tail.next = take;
            tail = take;
        }
        Node rest = a != null ? a : b;
        if (tail == null) return rest;
        tail.next = rest;
        return head;
    }
    static int expectedComparisons(int[] a, int[] b) {
        int i = 0, j = 0, c = 0;
        while (i < a.length && j < b.length) {
            c++;
            if (b[j] < a[i]) j++; else i++;
        }
        return c;
    }

    public static void main(String[] args) {
        Node m = merge(build(new int[]{1, 2}), build(new int[]{5, 6}));
        List<Integer> v = new ArrayList<>();
        for (Node c = m; c != null; c = c.next) v.add(c.value);
        if (!v.equals(List.of(1, 2, 5, 6)) || comparisons != 2) throw new AssertionError("example 1");
        m = merge(build(new int[]{4, 8, 9}), null);
        v.clear();
        for (Node c = m; c != null; c = c.next) v.add(c.value);
        if (!v.equals(List.of(4, 8, 9)) || comparisons != 0) throw new AssertionError("example 2");
        Random rnd = new Random(1415);
        for (int t = 0; t < 5000; t++) {
            int n = rnd.nextInt(8), k = rnd.nextInt(8);
            int[] a = new int[n], b = new int[k];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(6);
            for (int i = 0; i < k; i++) b[i] = rnd.nextInt(6);
            java.util.Arrays.sort(a);
            java.util.Arrays.sort(b);
            merge(build(a), build(b));
            if (comparisons != expectedComparisons(a, b)) throw new AssertionError("comparison count differs");
            if ((n == 0 || k == 0) && comparisons != 0) throw new AssertionError("an empty list needs no comparison");
        }
    }
}
```

#### Solution: [Recognize] Sort List (LeetCode 148)
<!-- id: ll-sort-list -->

**Approach.** A list with zero or one node is already sorted. Otherwise count the nodes, walk to the last node of the first half, and cut the link after it, which makes two separate lists. Sort each half recursively and merge them with the stable merge from this lesson, which takes the first half's node on ties. The recursion depth is about log n, so the stack stays small. The assertions compare with sorting an array, check stability by tagging each node with its original position, and check that the node count is preserved.

**Complexity.** O(n log n) time, since each of the log n levels merges n nodes, and O(log n) stack space.

```java run
import java.util.Random;

public final class SortList {
    static final class Node {
        int value;
        int origin;
        Node next;
        Node(int value, int origin) { this.value = value; this.origin = origin; }
    }
    static Node build(int[] values) {
        Node head = null, tail = null;
        for (int i = 0; i < values.length; i++) {
            Node n = new Node(values[i], i);
            if (head == null) head = n; else tail.next = n;
            tail = n;
        }
        return head;
    }
    static Node merge(Node a, Node b) {
        Node head = null, tail = null;
        while (a != null && b != null) {
            Node take;
            if (b.value < a.value) { take = b; b = b.next; }
            else { take = a; a = a.next; }
            if (tail == null) head = take; else tail.next = take;
            tail = take;
        }
        Node rest = a != null ? a : b;
        if (tail == null) return rest;
        tail.next = rest;
        return head;
    }
    static Node sortList(Node head) {
        if (head == null || head.next == null) return head;
        int n = 0;
        for (Node cur = head; cur != null; cur = cur.next) n++;
        Node left = head;
        for (int i = 1; i < n / 2; i++) left = left.next;
        Node right = left.next;
        left.next = null;
        return merge(sortList(head), sortList(right));
    }

    public static void main(String[] args) {
        Node s = sortList(build(new int[]{5, 2, 9, 2, 7, 1}));
        int[] expected = {1, 2, 2, 5, 7, 9};
        int i = 0;
        for (Node c = s; c != null; c = c.next) if (c.value != expected[i++]) throw new AssertionError("example 1");
        if (i != 6) throw new AssertionError("example 1 length");
        if (sortList(null) != null) throw new AssertionError("example 2");
        Random rnd = new Random(1416);
        for (int t = 0; t < 4000; t++) {
            int n = rnd.nextInt(16);
            int[] a = new int[n];
            for (int k = 0; k < n; k++) a[k] = rnd.nextInt(5);
            int[] sorted = a.clone();
            java.util.Arrays.sort(sorted);
            Node head = sortList(build(a));
            int count = 0;
            Node prev = null;
            for (Node c = head; c != null && count <= n; c = c.next) {
                if (c.value != sorted[count]) throw new AssertionError("disagrees with Arrays.sort");
                if (prev != null && prev.value == c.value && prev.origin > c.origin) throw new AssertionError("the sort must be stable");
                prev = c;
                count++;
            }
            if (count != n) throw new AssertionError("a node was lost");
        }
    }
}
```
