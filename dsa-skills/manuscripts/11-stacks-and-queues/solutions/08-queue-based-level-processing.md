<!-- solutions-for: 08-queue-based-level-processing -->
### Queue-Based Level Processing

#### Solution: [Build] Process Queue In Batches (Author exercise)
<!-- id: sq-process-in-batches -->

**Approach.** Put item 0 in a queue. While the queue is nonempty, read its size once, remove exactly that many items into a list, and append each removed item's children to the queue. The list is the batch, and the queue behind it holds the next batch. The size is captured before the inner loop, because the inner loop changes the live size. The assertions compare with a distance-array method that computes each item's round and groups the items by round in index order, comparing each batch as a sorted list, on random forests where every item appears in at most one list.

**Complexity.** O(n + e) time and O(width) extra space for the queue.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

public final class ProcessInBatches {
    static List<List<Integer>> batches(int[][] children) {
        List<List<Integer>> out = new ArrayList<>();
        ArrayDeque<Integer> queue = new ArrayDeque<>();
        queue.addLast(0);
        while (!queue.isEmpty()) {
            int size = queue.size();
            List<Integer> batch = new ArrayList<>();
            for (int k = 0; k < size; k++) {
                int item = queue.removeFirst();
                batch.add(item);
                for (int c : children[item]) queue.addLast(c);
            }
            out.add(batch);
        }
        return out;
    }
    static List<List<Integer>> byDistance(int[][] children) {
        int n = children.length;
        int[] round = new int[n];
        Arrays.fill(round, -1);
        round[0] = 0;
        boolean changed = true;
        while (changed) {
            changed = false;
            for (int i = 0; i < n; i++) {
                if (round[i] < 0) continue;
                for (int c : children[i]) if (round[c] < 0) { round[c] = round[i] + 1; changed = true; }
            }
        }
        int maxRound = 0;
        for (int r : round) maxRound = Math.max(maxRound, r);
        List<List<Integer>> out = new ArrayList<>();
        for (int r = 0; r <= maxRound; r++) {
            List<Integer> level = new ArrayList<>();
            for (int i = 0; i < n; i++) if (round[i] == r) level.add(i);
            out.add(level);
        }
        return out;
    }
    static int[][] randomForest(Random rnd, int n) {
        List<List<Integer>> lists = new ArrayList<>();
        for (int i = 0; i < n; i++) lists.add(new ArrayList<>());
        for (int i = 1; i < n; i++) if (rnd.nextInt(5) != 0) lists.get(rnd.nextInt(i)).add(i);
        int[][] c = new int[n][];
        for (int i = 0; i < n; i++) c[i] = lists.get(i).stream().mapToInt(Integer::intValue).toArray();
        return c;
    }

    public static void main(String[] args) {
        if (!batches(new int[][] {{1, 2}, {3}, {}, {}}).equals(List.of(List.of(0), List.of(1, 2), List.of(3)))) throw new AssertionError("example 1");
        if (!batches(new int[][] {{}}).equals(List.of(List.of(0)))) throw new AssertionError("example 2");
        ArrayDeque<Integer> q = new ArrayDeque<>();
        q.addLast(1);
        int before = q.size();
        q.addLast(2);
        if (q.size() == before) throw new AssertionError("the live size grows while the queue is filled");
        Random rnd = new Random(11801);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(14);
            int[][] c = randomForest(rnd, n);
            List<List<Integer>> got = batches(c);
            List<List<Integer>> want = byDistance(c);
            if (got.size() != want.size()) throw new AssertionError("round count differs on " + Arrays.deepToString(c));
            for (int r = 0; r < got.size(); r++) {
                List<Integer> sortedBatch = new ArrayList<>(got.get(r));
                java.util.Collections.sort(sortedBatch);
                if (!sortedBatch.equals(want.get(r))) throw new AssertionError("round " + r + " differs on " + Arrays.deepToString(c));
            }
        }
    }
}
```

#### Solution: [Vary] Count Levels To First Target (Author exercise)
<!-- id: sq-levels-to-target -->

**Approach.** Run the batch loop and increase a round counter only after a captured batch has been fully processed. When the target is removed, the counter equals the number of completed batches before its own, which is its distance from item 0. If the queue empties first, the target is not reachable and the answer is -1. The assertions compare with a plain parent-chain walk: build a parent array from the lists and count steps up from the target to item 0, with the unreachable case when the walk ends elsewhere.

**Complexity.** O(n + e) time and O(width) extra space.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public final class LevelsToTarget {
    static int levels(int[][] children, int target) {
        ArrayDeque<Integer> queue = new ArrayDeque<>();
        queue.addLast(0);
        int round = 0;
        while (!queue.isEmpty()) {
            int size = queue.size();
            for (int k = 0; k < size; k++) {
                int item = queue.removeFirst();
                if (item == target) return round;
                for (int c : children[item]) queue.addLast(c);
            }
            round++;
        }
        return -1;
    }
    static int viaParents(int[][] children, int target) {
        int n = children.length;
        int[] parent = new int[n];
        java.util.Arrays.fill(parent, -1);
        for (int i = 0; i < n; i++) for (int c : children[i]) parent[c] = i;
        int steps = 0, x = target;
        while (x != 0) {
            if (parent[x] == -1) return -1;
            x = parent[x];
            steps++;
        }
        return steps;
    }
    static int[][] randomForest(Random rnd, int n) {
        List<List<Integer>> lists = new ArrayList<>();
        for (int i = 0; i < n; i++) lists.add(new ArrayList<>());
        for (int i = 1; i < n; i++) if (rnd.nextInt(4) != 0) lists.get(rnd.nextInt(i)).add(i);
        int[][] c = new int[n][];
        for (int i = 0; i < n; i++) c[i] = lists.get(i).stream().mapToInt(Integer::intValue).toArray();
        return c;
    }

    public static void main(String[] args) {
        if (levels(new int[][] {{1, 2}, {3}, {}, {}}, 3) != 2) throw new AssertionError("example 1");
        if (levels(new int[][] {{1}, {}, {}}, 2) != -1) throw new AssertionError("example 2");
        if (levels(new int[][] {{}}, 0) != 0) throw new AssertionError("item 0 is at distance zero");
        Random rnd = new Random(11802);
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(14);
            int[][] c = randomForest(rnd, n);
            int target = rnd.nextInt(n);
            if (levels(c, target) != viaParents(c, target)) throw new AssertionError("differs for target " + target);
        }
    }
}
```

#### Solution: [Boundary] Expanding Queue (Author exercise)
<!-- id: sq-expanding-queue -->

**Approach.** Start the queue with item 0, which exists only when n is positive. Read the size once per round, remove that many items, and append `2x + 1` and `2x + 2` when they are below n. Record the captured size as the batch size. Appending raises the live size, so a loop bounded by the live size would run into the next batch, and the assertions run that faulty loop and show that it reports different sizes. The correct sizes are compared with a closed form: level k holds the indices from 2^k - 1 up to 2^(k + 1) - 2, clipped to n.

**Complexity.** O(n) time and O(n) space in the worst case for the queue.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public final class ExpandingQueue {
    static int[] sizes(int n) {
        List<Integer> out = new ArrayList<>();
        ArrayDeque<Integer> queue = new ArrayDeque<>();
        if (n > 0) queue.addLast(0);
        while (!queue.isEmpty()) {
            int size = queue.size();
            out.add(size);
            for (int k = 0; k < size; k++) {
                int x = queue.removeFirst();
                if (2 * x + 1 < n) queue.addLast(2 * x + 1);
                if (2 * x + 2 < n) queue.addLast(2 * x + 2);
            }
        }
        return out.stream().mapToInt(Integer::intValue).toArray();
    }
    static int[] faulty(int n) {
        List<Integer> out = new ArrayList<>();
        ArrayDeque<Integer> queue = new ArrayDeque<>();
        if (n > 0) queue.addLast(0);
        while (!queue.isEmpty()) {
            int count = 0;
            for (int k = 0; k < queue.size(); k++) {
                int x = queue.removeFirst();
                count++;
                if (2 * x + 1 < n) queue.addLast(2 * x + 1);
                if (2 * x + 2 < n) queue.addLast(2 * x + 2);
            }
            out.add(count);
        }
        return out.stream().mapToInt(Integer::intValue).toArray();
    }
    static int[] closedForm(int n) {
        List<Integer> out = new ArrayList<>();
        for (long lo = 0, width = 1; lo < n; lo += width, width *= 2) out.add((int) Math.min(width, n - lo));
        return out.stream().mapToInt(Integer::intValue).toArray();
    }

    public static void main(String[] args) {
        if (!Arrays.equals(sizes(7), new int[] {1, 2, 4})) throw new AssertionError("example 1");
        if (!Arrays.equals(sizes(10), new int[] {1, 2, 4, 3})) throw new AssertionError("example 2");
        if (sizes(0).length != 0) throw new AssertionError("no items");
        if (Arrays.equals(faulty(7), sizes(7))) throw new AssertionError("a live-size loop reports different batches");
        for (int n = 0; n <= 3000; n++) {
            if (!Arrays.equals(sizes(n), closedForm(n))) throw new AssertionError("differs at n=" + n);
        }
    }
}
```

#### Solution: [Recognize] Alternate Level Output (Author exercise)
<!-- id: sq-alternate-level-output -->

**Approach.** Run the captured-size batch loop with ordinary first-in-first-out removal and children appended in list order. After a batch is complete, reverse the reported list when the batch index is odd. The queue is never reordered, so the next batch is discovered in the same order as without the reversal. Reversing the queue instead would change which children are discovered first and break the next batch. The assertions compare with a method that computes each item's round by a distance array, groups by round in discovery order, and reverses the odd rounds, and they show that a deque reversed at the odd rounds gives a different answer on a wide forest.

**Complexity.** O(n + e) time and O(width) extra space.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.Random;

public final class AlternateLevelOutput {
    static List<List<Integer>> zigzag(int[][] children) {
        List<List<Integer>> out = new ArrayList<>();
        ArrayDeque<Integer> queue = new ArrayDeque<>();
        queue.addLast(0);
        int index = 0;
        while (!queue.isEmpty()) {
            int size = queue.size();
            List<Integer> batch = new ArrayList<>();
            for (int k = 0; k < size; k++) {
                int item = queue.removeFirst();
                batch.add(item);
                for (int c : children[item]) queue.addLast(c);
            }
            if (index % 2 == 1) Collections.reverse(batch);
            out.add(batch);
            index++;
        }
        return out;
    }
    static List<List<Integer>> reorderingQueue(int[][] children) {
        List<List<Integer>> out = new ArrayList<>();
        ArrayDeque<Integer> queue = new ArrayDeque<>();
        queue.addLast(0);
        int index = 0;
        while (!queue.isEmpty()) {
            int size = queue.size();
            List<Integer> batch = new ArrayList<>();
            for (int k = 0; k < size; k++) {
                int item = index % 2 == 1 ? queue.removeLast() : queue.removeFirst();
                batch.add(item);
                for (int c : children[item]) queue.addLast(c);
            }
            out.add(batch);
            index++;
        }
        return out;
    }
    static List<List<Integer>> viaRounds(int[][] children) {
        int n = children.length;
        int[] round = new int[n];
        Arrays.fill(round, -1);
        round[0] = 0;
        List<Integer> order = new ArrayList<>();
        order.add(0);
        for (int head = 0; head < order.size(); head++) {
            int x = order.get(head);
            for (int c : children[x]) { round[c] = round[x] + 1; order.add(c); }
        }
        int maxRound = round[order.get(order.size() - 1)];
        List<List<Integer>> out = new ArrayList<>();
        for (int r = 0; r <= maxRound; r++) {
            List<Integer> level = new ArrayList<>();
            for (int x : order) if (round[x] == r) level.add(x);
            if (r % 2 == 1) Collections.reverse(level);
            out.add(level);
        }
        return out;
    }
    static int[][] randomForest(Random rnd, int n) {
        List<List<Integer>> lists = new ArrayList<>();
        for (int i = 0; i < n; i++) lists.add(new ArrayList<>());
        for (int i = 1; i < n; i++) lists.get(rnd.nextInt(i)).add(i);
        int[][] c = new int[n][];
        for (int i = 0; i < n; i++) c[i] = lists.get(i).stream().mapToInt(Integer::intValue).toArray();
        return c;
    }

    public static void main(String[] args) {
        if (!zigzag(new int[][] {{1, 2}, {3, 4}, {5}, {}, {}, {}}).equals(List.of(List.of(0), List.of(2, 1), List.of(3, 4, 5)))) throw new AssertionError("example 1");
        if (!zigzag(new int[][] {{}}).equals(List.of(List.of(0)))) throw new AssertionError("example 2");
        boolean differs = false;
        Random rnd = new Random(11803);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(14);
            int[][] c = randomForest(rnd, n);
            if (!zigzag(c).equals(viaRounds(c))) throw new AssertionError("differs on " + Arrays.deepToString(c));
            if (!zigzag(c).equals(reorderingQueue(c))) differs = true;
        }
        if (!differs) throw new AssertionError("reordering the queue itself must change some answers");
    }
}
```
