<!-- solutions-for: 04-k-way-merge -->
### K-Way Merge

#### Solution: [Build] Merge Three Sorted Arrays (Author exercise)
<!-- id: hp-merge-three-arrays -->

**Approach.** Offer the first element of each non-empty array as `{value, array, position}`. Then poll the smallest entry, write its value, and offer the next element of the same array if there is one. Because every array is sorted, the smallest front is the smallest unwritten value. The harness runs both examples, tracks the largest number of entries the frontier ever holds and requires it to stay at three or below, and sets that against a load-everything variant whose heap reaches the full input size on the same data. Random inputs are judged against a sorted concatenation.

**Complexity.** Each of the n values causes one poll and at most one offer on a heap of at most three entries, so the merge takes O(n) time here and O(1) memory beyond the output. For `k` sources the same code costs O(n log k).

```java run
import java.util.Arrays;
import java.util.Comparator;
import java.util.PriorityQueue;
import java.util.Random;

public final class MergeThreeArrays {
    static int peakFrontier;

    static int[] merge(int[] a, int[] b, int[] c) {
        int[][] src = {a, b, c};
        PriorityQueue<int[]> frontier = new PriorityQueue<>(
            Comparator.<int[]>comparingInt(e -> e[0]).thenComparingInt(e -> e[1]));
        int total = 0;
        for (int s = 0; s < 3; s++) {
            total += src[s].length;
            if (src[s].length > 0) frontier.offer(new int[]{src[s][0], s, 0});
        }
        peakFrontier = frontier.size();
        int[] out = new int[total];
        for (int i = 0; i < total; i++) {
            int[] head = frontier.poll();
            out[i] = head[0];
            int next = head[2] + 1;
            if (next < src[head[1]].length) frontier.offer(new int[]{src[head[1]][next], head[1], next});
            peakFrontier = Math.max(peakFrontier, frontier.size());
        }
        return out;
    }

    static int loadEverythingPeak(int[] a, int[] b, int[] c) {
        PriorityQueue<Integer> all = new PriorityQueue<>();
        for (int v : a) all.offer(v);
        for (int v : b) all.offer(v);
        for (int v : c) all.offer(v);
        return all.size();
    }

    static int[] sortedConcat(int[] a, int[] b, int[] c) {
        int[] all = new int[a.length + b.length + c.length];
        System.arraycopy(a, 0, all, 0, a.length);
        System.arraycopy(b, 0, all, a.length, b.length);
        System.arraycopy(c, 0, all, a.length + b.length, c.length);
        Arrays.sort(all);
        return all;
    }

    static int[] sortedRandom(Random rnd, int len) {
        int[] x = new int[len];
        for (int i = 0; i < len; i++) x[i] = rnd.nextInt(15) - 7;
        Arrays.sort(x);
        return x;
    }

    public static void main(String[] args) {
        if (!Arrays.equals(merge(new int[]{1, 5, 9}, new int[]{2, 6}, new int[]{0, 3, 10}), new int[]{0, 1, 2, 3, 5, 6, 9, 10})) throw new AssertionError("example 1");
        if (peakFrontier > 3) throw new AssertionError("frontier holds at most one entry per array");
        if (loadEverythingPeak(new int[]{1, 5, 9}, new int[]{2, 6}, new int[]{0, 3, 10}) != 8) throw new AssertionError("the load-everything heap holds all 8 values");
        if (!Arrays.equals(merge(new int[]{4}, new int[]{4}, new int[]{4, 4}), new int[]{4, 4, 4, 4})) throw new AssertionError("example 2");
        Random rnd = new Random(1741);
        for (int t = 0; t < 4000; t++) {
            int[] a = sortedRandom(rnd, rnd.nextInt(8));
            int[] b = sortedRandom(rnd, rnd.nextInt(8));
            int[] c = sortedRandom(rnd, rnd.nextInt(8));
            if (a.length + b.length + c.length == 0) continue;
            if (!Arrays.equals(merge(a, b, c), sortedConcat(a, b, c))) throw new AssertionError("wrong merge of " + Arrays.toString(a) + Arrays.toString(b) + Arrays.toString(c));
            if (peakFrontier > 3) throw new AssertionError("frontier grew past three entries");
        }
    }
}
```

#### Solution: [Vary] Merge k Sorted Lists (LeetCode 23)
<!-- id: hp-merge-k-lists -->

**Approach.** Put the head node of every non-empty list into a queue ordered by `node.val`. Poll the smallest node, append it to the tail of the result with a dummy head, and offer `node.next` if it exists. The successor is found through the node itself, so no position is stored. The merged list reuses the original node objects, which the harness proves with an identity set. It also shows that a `PriorityQueue<ListNode>` built without a comparator fails with a `ClassCastException` on its second offer, since the node class has no natural order. Both examples and random lists are checked against a sorted concatenation of the values.

**Complexity.** There are N nodes in total, and each costs one poll and at most one offer on a queue of at most k nodes, so the time is O(N log k) and the extra memory is O(k).

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.IdentityHashMap;
import java.util.PriorityQueue;
import java.util.Random;

public final class MergeKLists {
    static final class ListNode {
        int val;
        ListNode next;
        ListNode(int val) { this.val = val; }
    }

    static ListNode build(int[] values, ArrayList<ListNode> registry) {
        ListNode dummy = new ListNode(0), tail = dummy;
        for (int v : values) {
            tail.next = new ListNode(v);
            tail = tail.next;
            registry.add(tail);
        }
        return dummy.next;
    }

    static ListNode merge(ListNode[] lists) {
        PriorityQueue<ListNode> frontier = new PriorityQueue<>((x, y) -> Integer.compare(x.val, y.val));
        for (ListNode head : lists) if (head != null) frontier.offer(head);
        ListNode dummy = new ListNode(0), tail = dummy;
        while (!frontier.isEmpty()) {
            ListNode node = frontier.poll();
            tail.next = node;
            tail = node;
            if (node.next != null) frontier.offer(node.next);
        }
        tail.next = null;
        return dummy.next;
    }

    static int[] toArray(ListNode head) {
        ArrayList<Integer> out = new ArrayList<>();
        for (ListNode n = head; n != null; n = n.next) out.add(n.val);
        int[] r = new int[out.size()];
        for (int i = 0; i < r.length; i++) r[i] = out.get(i);
        return r;
    }

    static int[] run(int[][] lists, ArrayList<ListNode> registry) {
        ListNode[] heads = new ListNode[lists.length];
        for (int i = 0; i < lists.length; i++) heads[i] = build(lists[i], registry);
        return toArray(merge(heads));
    }

    public static void main(String[] args) {
        if (!Arrays.equals(run(new int[][]{{2, 5}, {1, 6, 8}, {3}}, new ArrayList<>()), new int[]{1, 2, 3, 5, 6, 8})) throw new AssertionError("example 1");
        if (run(new int[][]{{}}, new ArrayList<>()).length != 0) throw new AssertionError("example 2");
        if (merge(new ListNode[0]) != null) throw new AssertionError("no lists gives an empty result");
        try {
            PriorityQueue<ListNode> raw = new PriorityQueue<>();
            raw.offer(new ListNode(1));
            raw.offer(new ListNode(2));
            throw new AssertionError("nodes without an order must not be comparable");
        } catch (ClassCastException expected) { }
        Random rnd = new Random(1742);
        for (int t = 0; t < 3000; t++) {
            int k = rnd.nextInt(6);
            int[][] lists = new int[k][];
            ArrayList<Integer> all = new ArrayList<>();
            for (int i = 0; i < k; i++) {
                int[] x = new int[rnd.nextInt(6)];
                for (int j = 0; j < x.length; j++) x[j] = rnd.nextInt(11) - 5;
                Arrays.sort(x);
                lists[i] = x;
                for (int v : x) all.add(v);
            }
            Collections.sort(all);
            ArrayList<ListNode> registry = new ArrayList<>();
            ListNode[] heads = new ListNode[k];
            for (int i = 0; i < k; i++) heads[i] = build(lists[i], registry);
            ListNode merged = merge(heads);
            int[] got = toArray(merged);
            for (int i = 0; i < got.length; i++) if (got[i] != all.get(i)) throw new AssertionError("wrong order for " + Arrays.deepToString(lists));
            if (got.length != all.size()) throw new AssertionError("wrong length for " + Arrays.deepToString(lists));
            IdentityHashMap<ListNode, Boolean> original = new IdentityHashMap<>();
            for (ListNode n : registry) original.put(n, true);
            for (ListNode n = merged; n != null; n = n.next) if (!original.containsKey(n)) throw new AssertionError("a node was copied instead of reused");
        }
    }
}
```

#### Solution: [Boundary] Empty Sources And Equal Heads (Author exercise)
<!-- id: hp-empty-sources-equal-heads -->

**Approach.** Offer an entry for a source only when it has at least one value, so empty sources never reach the heap and cannot cause a failed poll. The comparator orders by value and then by source index, which makes equal heads leave in source order, and a source whose next value equals its previous one keeps its turn, because its successor again ties and again wins on the index. The method records the source index of each poll. Since every source is nondecreasing, the expected emission order is the same as sorting all triples of value, source and position, and the random test uses that sort as its oracle. Both examples are asserted, including one in which three heads tie at 2.

**Complexity.** The cost is O(N log k) time for N values over k sources, with O(k) memory for the frontier and the O(N) result.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Comparator;
import java.util.PriorityQueue;
import java.util.Random;

public final class EmptySourcesEqualHeads {
    static int[] emissionOrder(int[][] sources) {
        PriorityQueue<int[]> frontier = new PriorityQueue<>(
            Comparator.<int[]>comparingInt(e -> e[0]).thenComparingInt(e -> e[1]));
        int total = 0;
        for (int s = 0; s < sources.length; s++) {
            total += sources[s].length;
            if (sources[s].length > 0) frontier.offer(new int[]{sources[s][0], s, 0});
        }
        int[] order = new int[total];
        for (int i = 0; i < total; i++) {
            int[] head = frontier.poll();
            order[i] = head[1];
            int next = head[2] + 1;
            if (next < sources[head[1]].length) frontier.offer(new int[]{sources[head[1]][next], head[1], next});
        }
        return order;
    }

    static int[] bySortingTriples(int[][] sources) {
        ArrayList<int[]> all = new ArrayList<>();
        for (int s = 0; s < sources.length; s++)
            for (int p = 0; p < sources[s].length; p++) all.add(new int[]{sources[s][p], s, p});
        all.sort(Comparator.<int[]>comparingInt(e -> e[0]).thenComparingInt(e -> e[1]).thenComparingInt(e -> e[2]));
        int[] out = new int[all.size()];
        for (int i = 0; i < out.length; i++) out[i] = all.get(i)[1];
        return out;
    }

    public static void main(String[] args) {
        if (!Arrays.equals(emissionOrder(new int[][]{{}, {5, 5}, {5}, {}}), new int[]{1, 1, 2})) throw new AssertionError("example 1");
        if (!Arrays.equals(emissionOrder(new int[][]{{2}, {1, 2}, {2}}), new int[]{1, 0, 1, 2})) throw new AssertionError("example 2");
        if (emissionOrder(new int[][]{{}, {}}).length != 0) throw new AssertionError("all sources empty");
        Random rnd = new Random(1743);
        for (int t = 0; t < 4000; t++) {
            int k = 1 + rnd.nextInt(6);
            int[][] sources = new int[k][];
            for (int s = 0; s < k; s++) {
                int[] x = new int[rnd.nextInt(5)];
                for (int j = 0; j < x.length; j++) x[j] = rnd.nextInt(4);
                Arrays.sort(x);
                sources[s] = x;
            }
            if (!Arrays.equals(emissionOrder(sources), bySortingTriples(sources))) throw new AssertionError("emission order differs for " + Arrays.deepToString(sources));
        }
    }
}
```

#### Solution: [Recognize] Kth Smallest Element in a Sorted Matrix (LeetCode 378)
<!-- id: hp-kth-smallest-matrix -->

**Approach.** Treat each row as a sorted source. Offer the first entry of each of the first `min(n, k)` rows, since the first element of any later row has at least `k` values no larger than it, namely the first elements of the rows above, and so it cannot be among the first `k` smallest. Then poll `k` times, offering the successor in the row after each poll, and return the value of the last poll. The loop never exhausts the matrix, so most entries are never touched. The harness asserts both examples and the number of polls, and it builds random matrices from sorted row offsets plus sorted column offsets, which guarantees sorted rows and columns, and checks the answer on each against a full sort.

**Complexity.** The setup costs O(min(n, k) log n) and the loop costs O(k log n), so the total time is O(k log n) up to the setup, with at most n entries in the heap.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.Comparator;
import java.util.PriorityQueue;
import java.util.Random;

public final class KthSmallestMatrix {
    static int polls;

    static int kthSmallest(int[][] matrix, int k) {
        int n = matrix.length;
        PriorityQueue<int[]> frontier = new PriorityQueue<>(
            Comparator.<int[]>comparingInt(e -> e[0]).thenComparingInt(e -> e[1]));
        for (int r = 0; r < Math.min(n, k); r++) frontier.offer(new int[]{matrix[r][0], r, 0});
        polls = 0;
        int answer = 0;
        for (int i = 0; i < k; i++) {
            int[] head = frontier.poll();
            polls++;
            answer = head[0];
            int next = head[2] + 1;
            if (next < n) frontier.offer(new int[]{matrix[head[1]][next], head[1], next});
        }
        return answer;
    }

    public static void main(String[] args) {
        if (kthSmallest(new int[][]{{1, 4, 8}, {2, 5, 9}, {3, 6, 12}}, 5) != 5) throw new AssertionError("example 1");
        if (polls != 5) throw new AssertionError("exactly k polls, got " + polls);
        if (kthSmallest(new int[][]{{2, 2}, {2, 3}}, 3) != 2) throw new AssertionError("example 2");
        if (kthSmallest(new int[][]{{7}}, 1) != 7) throw new AssertionError("single cell");
        Random rnd = new Random(1744);
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(6);
            int[] rowBase = new int[n], colBase = new int[n];
            for (int i = 0; i < n; i++) { rowBase[i] = rnd.nextInt(10); colBase[i] = rnd.nextInt(10); }
            Arrays.sort(rowBase);
            Arrays.sort(colBase);
            int[][] m = new int[n][n];
            ArrayList<Integer> all = new ArrayList<>();
            for (int i = 0; i < n; i++) for (int j = 0; j < n; j++) { m[i][j] = rowBase[i] + colBase[j]; all.add(m[i][j]); }
            Collections.sort(all);
            int k = 1 + rnd.nextInt(n * n);
            if (kthSmallest(m, k) != all.get(k - 1)) throw new AssertionError("wrong answer for k=" + k + " on " + Arrays.deepToString(m));
            if (polls != k) throw new AssertionError("poll count must equal k");
        }
    }
}
```
