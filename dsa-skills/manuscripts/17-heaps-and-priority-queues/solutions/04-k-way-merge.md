<!-- solutions-for: 04-k-way-merge -->
### Solutions For Merging Many Sorted Inputs

#### Solution: [Build] Merge Three Sorted Arrays (Author exercise)
<!-- id: hp-merge-three -->

**Approach.**
The queue holds one entry per array, and each entry stores the value, the array number and the position in that array. The code offers the first value of each non-empty array. Each poll returns the smallest unread value over all three arrays, because every array is sorted and its next value is its smallest. After the poll, the code offers the next value of the same array when one exists. The loop ends when the queue is empty, which happens exactly when all arrays are read.

Before each poll, every array that still has unread values owns exactly one queue entry.

**Complexity.**
- **Time** is O(N), because the queue holds at most three entries, so each of the N values costs a constant number of steps.
- **Space** is O(1) extra beyond the output, because the queue holds at most three entries.

```java run
import java.util.*;

public final class MergeThree {
    /**
     * Merges three sorted arrays with a queue of at most three entries.
     * Time: O(N) for N total values. Space: O(1) beyond the output.
     * Invariant: every array with unread values owns one queue entry.
     */
    static int[] merge(int[] a, int[] b, int[] c) {
        int[][] src = {a, b, c};
        PriorityQueue<int[]> queue = new PriorityQueue<>((x, y) -> Integer.compare(x[0], y[0]));
        // One entry per non-empty array: value, array number, position.
        for (int s = 0; s < 3; s++) if (src[s].length > 0) queue.offer(new int[] {src[s][0], s, 0});
        int[] out = new int[a.length + b.length + c.length];
        int w = 0;
        while (!queue.isEmpty()) {
            int[] top = queue.poll();
            // The polled value is the smallest unread value over all arrays.
            out[w++] = top[0];
            int next = top[2] + 1;
            // Refill only from the array that just lost its entry.
            if (next < src[top[1]].length) queue.offer(new int[] {src[top[1]][next], top[1], next});
        }
        return out;
    }

    public static void main(String[] args) {
        // Examples from the exercise.
        if (!Arrays.equals(merge(new int[] {1, 4, 9}, new int[] {2, 3}, new int[] {0, 8}), new int[] {0, 1, 2, 3, 4, 8, 9})) throw new AssertionError("ex1");
        if (!Arrays.equals(merge(new int[] {5}, new int[] {5}, new int[] {5}), new int[] {5, 5, 5})) throw new AssertionError("ex2");
        // Three empty arrays give an empty result.
        if (merge(new int[0], new int[0], new int[0]).length != 0) throw new AssertionError("empty");
        // Random sorted inputs must match concatenate-and-sort.
        Random rnd = new Random(1731);
        for (int t = 0; t < 300; t++) {
            int[][] in = new int[3][];
            List<Integer> all = new ArrayList<>();
            for (int s = 0; s < 3; s++) {
                in[s] = new int[rnd.nextInt(8)];
                for (int i = 0; i < in[s].length; i++) in[s][i] = rnd.nextInt(10);
                Arrays.sort(in[s]);
                for (int v : in[s]) all.add(v);
            }
            Collections.sort(all);
            int[] got = merge(in[0], in[1], in[2]);
            if (got.length != all.size()) throw new AssertionError("length " + t);
            for (int i = 0; i < got.length; i++) if (got[i] != all.get(i)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Vary] Merge k Sorted Lists (LeetCode 23)
<!-- id: hp-merge-k-lists -->

**Approach.**
The queue stores nodes ordered by `val`. The code offers each non-null head. Each poll returns the node with the smallest value among the current heads, and the code links it after the tail of the output list. The polled node's own `next` reference is its successor, and the code offers it when it is not null. A dummy head node removes the special case for the first output node. The method reuses the input nodes and changes only their `next` fields.

Before each poll, every list with unlinked nodes owns exactly one queue entry, its first unlinked node.

**Complexity.**
- **Time** is O(N log k), because each of the N nodes costs one poll and at most one offer on a queue of at most `k` entries.
- **Space** is O(k), because the queue holds at most one node per list.

```java run
import java.util.*;

public final class MergeKLists {
    static final class ListNode {
        int val;
        ListNode next;
        ListNode(int val) { this.val = val; }
    }

    /**
     * Merges sorted lists by relinking the existing nodes.
     * Time: O(N log k). Space: O(k).
     * Invariant: every list with unlinked nodes owns one queue entry.
     */
    static ListNode mergeKLists(ListNode[] lists) {
        PriorityQueue<ListNode> queue = new PriorityQueue<>((x, y) -> Integer.compare(x.val, y.val));
        // Null heads are empty lists and get no entry.
        for (ListNode head : lists) if (head != null) queue.offer(head);
        ListNode dummy = new ListNode(0), tail = dummy;
        while (!queue.isEmpty()) {
            ListNode node = queue.poll();
            // Link the smallest current node, then advance to its successor.
            tail.next = node;
            tail = node;
            if (node.next != null) queue.offer(node.next);
        }
        // The last node may still point into its old list, so cut it.
        tail.next = null;
        return dummy.next;
    }

    static ListNode build(int... vals) {
        ListNode dummy = new ListNode(0), t = dummy;
        for (int v : vals) { t.next = new ListNode(v); t = t.next; }
        return dummy.next;
    }

    static List<Integer> toList(ListNode h) {
        List<Integer> out = new ArrayList<>();
        for (; h != null; h = h.next) out.add(h.val);
        return out;
    }

    public static void main(String[] args) {
        // Example 1 and Example 2 from the exercise.
        ListNode merged = mergeKLists(new ListNode[] {build(2, 5, 8), build(1, 5), build(3)});
        if (!toList(merged).equals(List.of(1, 2, 3, 5, 5, 8))) throw new AssertionError("ex1");
        if (mergeKLists(new ListNode[0]) != null) throw new AssertionError("ex2");
        // Null heads only give an empty result.
        if (mergeKLists(new ListNode[] {null, null}) != null) throw new AssertionError("nulls");
        // Random inputs must match concatenate-and-sort, and every input node must be reused.
        Random rnd = new Random(1732);
        for (int t = 0; t < 300; t++) {
            ListNode[] in = new ListNode[rnd.nextInt(6)];
            List<Integer> all = new ArrayList<>();
            Set<ListNode> nodes = Collections.newSetFromMap(new IdentityHashMap<>());
            for (int s = 0; s < in.length; s++) {
                int[] v = new int[rnd.nextInt(6)];
                for (int i = 0; i < v.length; i++) v[i] = rnd.nextInt(8);
                Arrays.sort(v);
                in[s] = build(v);
                for (ListNode n = in[s]; n != null; n = n.next) { nodes.add(n); all.add(n.val); }
            }
            Collections.sort(all);
            ListNode out = mergeKLists(in);
            if (!toList(out).equals(all)) throw new AssertionError("random " + t);
            for (ListNode n = out; n != null; n = n.next) if (!nodes.contains(n)) throw new AssertionError("new node " + t);
        }
    }
}
```

#### Solution: [Boundary] Empty Sources And Equal Heads (Author exercise)
<!-- id: hp-empty-equal-heads -->

**Approach.**
The code gives an entry only to non-empty sources, so an empty source never enters the queue and never causes an index error. The comparator reads the value first. On equal values it reads the source index, so the smaller source leaves first. Each poll records the source index of the polled entry, and then the code offers the next value of that source. A source with equal values in a row keeps winning ties against larger source indexes. This is why the example output starts with 0 and then switches to 2.

Each source with unread values owns exactly one entry, and the queue orders entries by value and then by source index.

**Complexity.**
- **Time** is O(N log k), because each of the N values costs one poll and at most one offer on a queue of at most `k` entries.
- **Space** is O(k) beyond the output, because the queue holds one entry per non-empty source.

```java run
import java.util.*;

public final class EmptyEqualHeads {
    /**
     * Returns the source index of each merged value, ties resolved by the smaller source index.
     * Time: O(N log k). Space: O(k) beyond the output.
     * Invariant: the queue holds one entry per source that still has unread values.
     */
    static int[] sourceOrder(int[][] sources) {
        PriorityQueue<int[]> queue = new PriorityQueue<>((a, b) ->
            a[0] != b[0] ? Integer.compare(a[0], b[0]) : Integer.compare(a[1], b[1]));
        int total = 0;
        for (int s = 0; s < sources.length; s++) {
            total += sources[s].length;
            // Empty sources are skipped, so no entry reads position 0 of an empty array.
            if (sources[s].length > 0) queue.offer(new int[] {sources[s][0], s, 0});
        }
        int[] labels = new int[total];
        int w = 0;
        while (!queue.isEmpty()) {
            int[] top = queue.poll();
            // Record which source supplied this output value.
            labels[w++] = top[1];
            int next = top[2] + 1;
            if (next < sources[top[1]].length) queue.offer(new int[] {sources[top[1]][next], top[1], next});
        }
        return labels;
    }

    public static void main(String[] args) {
        // Examples from the exercise.
        if (!Arrays.equals(sourceOrder(new int[][] {{1, 3}, {}, {1, 2}}), new int[] {0, 2, 2, 0})) throw new AssertionError("ex1");
        if (sourceOrder(new int[][] {{}, {}}).length != 0) throw new AssertionError("ex2");
        if (sourceOrder(new int[0][]).length != 0) throw new AssertionError("no sources");
        // Random sources must match a stable sort of (value, source index, position) tuples.
        Random rnd = new Random(1733);
        for (int t = 0; t < 400; t++) {
            int[][] in = new int[rnd.nextInt(6)][];
            List<int[]> all = new ArrayList<>();
            for (int s = 0; s < in.length; s++) {
                in[s] = new int[rnd.nextInt(6)];
                for (int i = 0; i < in[s].length; i++) in[s][i] = rnd.nextInt(4);
                Arrays.sort(in[s]);
                for (int i = 0; i < in[s].length; i++) all.add(new int[] {in[s][i], s, i});
            }
            all.sort((x, y) -> x[0] != y[0] ? Integer.compare(x[0], y[0]) : x[1] != y[1] ? Integer.compare(x[1], y[1]) : Integer.compare(x[2], y[2]));
            int[] got = sourceOrder(in);
            for (int i = 0; i < got.length; i++) if (got[i] != all.get(i)[1]) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Recognize] Kth Smallest Element in a Sorted Matrix (LeetCode 378)
<!-- id: hp-kth-smallest-matrix -->

**Approach.**
Each row is a sorted stream, so the queue holds one entry per row, with the first value of each row at the start. The code polls `k` times. Each poll returns the smallest value not yet taken, and the code offers the next value of the same row. The kth polled value is the answer, so the code stops without reading the rest of the matrix. The column order is not needed for correctness, because each row alone is sorted.

After `j` polls, the `j` polled values are the `j` smallest, and each row with unread values owns one entry.

**Complexity.**
- **Time** is O(n + k log n), because the first row of entries costs O(n) to offer and each of the `k` polls costs O(log n).
- **Space** is O(n), because the queue holds one entry per row.

```java run
import java.util.*;

public final class KthSmallestMatrix {
    /**
     * Returns the kth smallest value of a matrix whose rows are sorted.
     * Time: O(n + k log n). Space: O(n).
     * Invariant: after j polls, the polled values are the j smallest.
     */
    static int kthSmallest(int[][] matrix, int k) {
        PriorityQueue<int[]> queue = new PriorityQueue<>((a, b) -> Integer.compare(a[0], b[0]));
        // Each row contributes its first value: value, row, column.
        for (int r = 0; r < matrix.length; r++) queue.offer(new int[] {matrix[r][0], r, 0});
        int last = 0;
        // Exactly k polls; the last polled value is the kth smallest.
        for (int i = 0; i < k; i++) {
            int[] top = queue.poll();
            last = top[0];
            // The successor is the next value in the same row.
            if (top[2] + 1 < matrix[top[1]].length) queue.offer(new int[] {matrix[top[1]][top[2] + 1], top[1], top[2] + 1});
        }
        return last;
    }

    public static void main(String[] args) {
        // Examples from the exercise.
        if (kthSmallest(new int[][] {{2, 3, 7}, {4, 6, 8}, {5, 9, 10}}, 5) != 6) throw new AssertionError("ex1");
        if (kthSmallest(new int[][] {{4}}, 1) != 4) throw new AssertionError("ex2");
        // Duplicates count separately: the 2nd smallest of [[1,1],[1,2]] is 1.
        if (kthSmallest(new int[][] {{1, 1}, {1, 2}}, 2) != 1) throw new AssertionError("duplicates");
        // Random matrices with sorted rows and columns must match sorting all values.
        Random rnd = new Random(1734);
        for (int t = 0; t < 300; t++) {
            int n = 1 + rnd.nextInt(5);
            int[][] m = new int[n][n];
            // Cell value = row-wise running sum, so rows and columns both rise.
            for (int r = 0; r < n; r++) for (int c = 0; c < n; c++) {
                int up = r > 0 ? m[r - 1][c] : 0, left = c > 0 ? m[r][c - 1] : 0;
                m[r][c] = Math.max(up, left) + rnd.nextInt(3);
            }
            List<Integer> all = new ArrayList<>();
            for (int[] row : m) for (int v : row) all.add(v);
            Collections.sort(all);
            int k = 1 + rnd.nextInt(n * n);
            if (kthSmallest(m, k) != all.get(k - 1)) throw new AssertionError("random " + t);
        }
    }
}
```
