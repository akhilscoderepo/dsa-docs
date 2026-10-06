<!-- solutions-for: 11-stacks-and-queues -->
### Solutions For Level Processing

#### Solution: [Build] Process Queue In Batches (Author exercise)
<!-- id: sq-process-in-batches -->

**Approach.**
The method places the start items in an `ArrayDeque`. Each outer iteration reads `queue.size()` once into `levelSize`. At that moment the queue holds exactly one level, because every item of the next level is appended only while the current level is polled. The inner loop polls `levelSize` items, records them in a row and appends their children behind them. The invariant is that the queue holds one complete level at the top of every outer iteration. A `null` marker is not an option, because `ArrayDeque` rejects `null` with a `NullPointerException`.

**Complexity.**
- **Time** is O(n), because each item is polled once and each child is appended once.
- **Space** is O(w) extra for the widest level w, plus O(n) for the returned rows.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.Random;

public final class ProcessInBatches {
    /**
     * Groups items into levels of a first-in first-out traversal.
     * Time: O(n), one poll and one append per item.
     * Space: O(w) for the queue plus O(n) for the output.
     * Invariant: the queue holds exactly one level at the top of each outer iteration.
     */
    static int[][] levels(int[] start, int[][] children) {
        List<int[]> result = new ArrayList<>();
        ArrayDeque<Integer> queue = new ArrayDeque<>();
        // The start items form level 0.
        for (int s : start) queue.offer(s);
        // The outer loop runs once per level.
        while (!queue.isEmpty()) {
            // The size is read once, so appends during the inner loop cannot change it.
            int levelSize = queue.size();
            int[] row = new int[levelSize];
            // The inner loop polls exactly the items that were queued when the level began.
            for (int k = 0; k < levelSize; k++) {
                int id = queue.poll();
                row[k] = id;
                // Children join the back of the queue and belong to the next level.
                for (int c : children[id]) queue.offer(c);
            }
            result.add(row);
        }
        return result.toArray(new int[0][]);
    }

    /** Builds a random forest: each attached id is a start item or a child of an earlier attached id. */
    static void generate(Random rnd, int[][] outChildren, int[][] outStart) {
        int n = outChildren.length;
        List<Integer> ids = new ArrayList<>();
        for (int i = 0; i < n; i++) ids.add(i);
        // A shuffled id order makes parents and children unrelated to numeric order.
        Collections.shuffle(ids, rnd);
        List<List<Integer>> kids = new ArrayList<>();
        for (int i = 0; i < n; i++) kids.add(new ArrayList<>());
        List<Integer> starts = new ArrayList<>();
        List<Integer> attached = new ArrayList<>();
        for (int id : ids) {
            int pick = rnd.nextInt(6);
            // One in six ids stays out of every list, so some items are never added.
            if (pick == 0) continue;
            // A start item has no parent; the first attached id must be one.
            if (attached.isEmpty() || pick == 1) starts.add(id);
            else kids.get(attached.get(rnd.nextInt(attached.size()))).add(id);
            attached.add(id);
        }
        for (int i = 0; i < n; i++) {
            outChildren[i] = new int[kids.get(i).size()];
            for (int j = 0; j < outChildren[i].length; j++) outChildren[i][j] = kids.get(i).get(j);
        }
        int[] s = new int[starts.size()];
        for (int i = 0; i < s.length; i++) s[i] = starts.get(i);
        outStart[0] = s;
    }

    /** Reference: record each depth, then regroup by scanning the processing order once per level. */
    static int[][] oracle(int[] start, int[][] children) {
        int[] depth = new int[children.length];
        List<Integer> order = new ArrayList<>();
        ArrayDeque<Integer> queue = new ArrayDeque<>();
        for (int s : start) queue.offer(s);
        while (!queue.isEmpty()) {
            int id = queue.poll();
            order.add(id);
            for (int c : children[id]) { depth[c] = depth[id] + 1; queue.offer(c); }
        }
        int count = 0;
        for (int id : order) count = Math.max(count, depth[id] + 1);
        int[][] res = new int[count][];
        for (int d = 0; d < count; d++) {
            List<Integer> row = new ArrayList<>();
            for (int id : order) if (depth[id] == d) row.add(id);
            res[d] = row.stream().mapToInt(Integer::intValue).toArray();
        }
        return res;
    }

    public static void main(String[] args) {
        // Example 1 and Example 2 from the exercise text.
        int[][] r1 = levels(new int[] {0, 1}, new int[][] {{2}, {3, 4}, {}, {5}, {}, {}});
        if (!Arrays.deepEquals(r1, new int[][] {{0, 1}, {2, 3, 4}, {5}})) throw new AssertionError("example 1");
        if (levels(new int[] {}, new int[][] {{}}).length != 0) throw new AssertionError("example 2");
        // The lesson claims that ArrayDeque rejects null, so a null marker cannot work.
        boolean rejected = false;
        try { new ArrayDeque<Integer>().offer(null); } catch (NullPointerException e) { rejected = true; }
        if (!rejected) throw new AssertionError("null contract");
        // Random forests agree with the record-depth-then-regroup reference.
        Random rnd = new Random(1181);
        for (int t = 0; t < 3000; t++) {
            int n = rnd.nextInt(14);
            int[][] ch = new int[n][];
            int[][] st = new int[1][];
            generate(rnd, ch, st);
            if (!Arrays.deepEquals(levels(st[0], ch), oracle(st[0], ch))) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Vary] Count Levels To First Target (Author exercise)
<!-- id: sq-levels-to-target -->

**Approach.**
The method runs the same two loops and keeps a `distance` counter that starts at 0. Inside the inner loop, it returns `distance` as soon as a polled item equals the target. After the inner loop ends, the whole level has been processed without a hit, so `distance` increases by 1. When the queue empties first, the target never appeared and the method returns -1. The invariant is that `distance` equals the number of levels that were fully processed before the current one.

**Complexity.**
- **Time** is O(n), because each item is polled at most once.
- **Space** is O(w) for the widest level w, because only the queue grows.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.Random;

public final class LevelsToTarget {
    /**
     * Returns the number of complete levels before the level that holds the target, or -1.
     * Time: O(n), each item is polled at most once.
     * Space: O(w) for the widest level.
     * Invariant: distance counts the levels fully processed before the current one.
     */
    static int distance(int[] start, int[][] children, int target) {
        ArrayDeque<Integer> queue = new ArrayDeque<>();
        for (int s : start) queue.offer(s);
        int distance = 0;
        // The outer loop runs once per level.
        while (!queue.isEmpty()) {
            int levelSize = queue.size();
            // The inner loop covers exactly the current level.
            for (int k = 0; k < levelSize; k++) {
                int id = queue.poll();
                // A hit inside the level returns the count of finished levels.
                if (id == target) return distance;
                for (int c : children[id]) queue.offer(c);
            }
            // The level had no hit, so one more level is finished.
            distance++;
        }
        // The queue emptied before the target appeared.
        return -1;
    }

    /** Builds a random forest: each attached id is a start item or a child of an earlier attached id. */
    static void generate(Random rnd, int[][] outChildren, int[][] outStart) {
        int n = outChildren.length;
        List<Integer> ids = new ArrayList<>();
        for (int i = 0; i < n; i++) ids.add(i);
        // A shuffled id order makes parents and children unrelated to numeric order.
        Collections.shuffle(ids, rnd);
        List<List<Integer>> kids = new ArrayList<>();
        for (int i = 0; i < n; i++) kids.add(new ArrayList<>());
        List<Integer> starts = new ArrayList<>();
        List<Integer> attached = new ArrayList<>();
        for (int id : ids) {
            int pick = rnd.nextInt(6);
            // One in six ids stays out of every list, so some items are never added.
            if (pick == 0) continue;
            // A start item has no parent; the first attached id must be one.
            if (attached.isEmpty() || pick == 1) starts.add(id);
            else kids.get(attached.get(rnd.nextInt(attached.size()))).add(id);
            attached.add(id);
        }
        for (int i = 0; i < n; i++) {
            outChildren[i] = new int[kids.get(i).size()];
            for (int j = 0; j < outChildren[i].length; j++) outChildren[i][j] = kids.get(i).get(j);
        }
        int[] s = new int[starts.size()];
        for (int i = 0; i < s.length; i++) s[i] = starts.get(i);
        outStart[0] = s;
    }

    /** Reference: record each depth, then regroup by scanning the processing order once per level. */
    static int[][] oracle(int[] start, int[][] children) {
        int[] depth = new int[children.length];
        List<Integer> order = new ArrayList<>();
        ArrayDeque<Integer> queue = new ArrayDeque<>();
        for (int s : start) queue.offer(s);
        while (!queue.isEmpty()) {
            int id = queue.poll();
            order.add(id);
            for (int c : children[id]) { depth[c] = depth[id] + 1; queue.offer(c); }
        }
        int count = 0;
        for (int id : order) count = Math.max(count, depth[id] + 1);
        int[][] res = new int[count][];
        for (int d = 0; d < count; d++) {
            List<Integer> row = new ArrayList<>();
            for (int id : order) if (depth[id] == d) row.add(id);
            res[d] = row.stream().mapToInt(Integer::intValue).toArray();
        }
        return res;
    }

    public static void main(String[] args) {
        // Example 1: the target 4 sits in the fourth level, after three finished levels.
        if (distance(new int[] {0}, new int[][] {{1, 2}, {3}, {}, {4}, {}}, 4) != 3) throw new AssertionError("example 1");
        // Example 2: item 2 is never added, so the answer is -1.
        if (distance(new int[] {0}, new int[][] {{1}, {}, {}}, 2) != -1) throw new AssertionError("example 2");
        // A target in the starting queue gives 0.
        if (distance(new int[] {0, 1}, new int[][] {{2}, {}, {}}, 1) != 0) throw new AssertionError("start level");
        // Random forests agree with the level index found in the regrouped reference.
        Random rnd = new Random(1182);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(14);
            int[][] ch = new int[n][];
            int[][] st = new int[1][];
            generate(rnd, ch, st);
            int target = rnd.nextInt(n);
            int[][] ref = oracle(st[0], ch);
            int expected = -1;
            // The expected answer is the index of the first reference row that contains the target.
            for (int d = 0; d < ref.length && expected < 0; d++) {
                for (int id : ref[d]) if (id == target) expected = d;
            }
            if (distance(st[0], ch, target) != expected) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Boundary] Expanding Queue (Author exercise)
<!-- id: sq-expanding-queue -->

**Approach.**
The method captures `levelSize = queue.size()` before polling and uses that fixed value as the inner loop bound. Each processed item appends all its children, so `queue.size()` can be much larger than `levelSize` before the level ends. Those extra items sit behind the unprocessed items of the level, so they wait for the next outer iteration. The invariant is that the count recorded for a level equals the queue size at the moment that level began. A loop bound that reads `queue.size()` on every check mixes levels, which the harness shows on Example 1.

**Complexity.**
- **Time** is O(n), because each item is polled once and each append happens once, whatever the fan-out.
- **Space** is O(n) in the worst case, because one item can append up to n - 1 children.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.Random;

public final class ExpandingQueue {
    /**
     * Returns the number of items processed in each level.
     * Time: O(n), one poll and one append per item.
     * Space: O(n), the queue can hold a whole wide level.
     * Invariant: sizes[d] is the queue size when level d began.
     */
    static int[] levelSizes(int[] start, int[][] children) {
        List<Integer> sizes = new ArrayList<>();
        ArrayDeque<Integer> queue = new ArrayDeque<>();
        for (int s : start) queue.offer(s);
        // The outer loop runs once per level.
        while (!queue.isEmpty()) {
            // The size is captured before any append of this level can change it.
            int levelSize = queue.size();
            sizes.add(levelSize);
            // The loop bound is the captured value, not the live queue size.
            for (int k = 0; k < levelSize; k++) {
                int id = queue.poll();
                for (int c : children[id]) queue.offer(c);
            }
        }
        return sizes.stream().mapToInt(Integer::intValue).toArray();
    }

    /** Faulty version that reads the live size in the loop condition. */
    static int[] faultySizes(int[] start, int[][] children) {
        List<Integer> sizes = new ArrayList<>();
        ArrayDeque<Integer> queue = new ArrayDeque<>();
        for (int s : start) queue.offer(s);
        while (!queue.isEmpty()) {
            int count = 0;
            // The live size changes on every poll and every append.
            for (int k = 0; k < queue.size(); k++) {
                int id = queue.poll();
                count++;
                for (int c : children[id]) queue.offer(c);
            }
            sizes.add(count);
        }
        return sizes.stream().mapToInt(Integer::intValue).toArray();
    }

    /** Builds a random forest: each attached id is a start item or a child of an earlier attached id. */
    static void generate(Random rnd, int[][] outChildren, int[][] outStart) {
        int n = outChildren.length;
        List<Integer> ids = new ArrayList<>();
        for (int i = 0; i < n; i++) ids.add(i);
        // A shuffled id order makes parents and children unrelated to numeric order.
        Collections.shuffle(ids, rnd);
        List<List<Integer>> kids = new ArrayList<>();
        for (int i = 0; i < n; i++) kids.add(new ArrayList<>());
        List<Integer> starts = new ArrayList<>();
        List<Integer> attached = new ArrayList<>();
        for (int id : ids) {
            int pick = rnd.nextInt(6);
            // One in six ids stays out of every list, so some items are never added.
            if (pick == 0) continue;
            // A start item has no parent; the first attached id must be one.
            if (attached.isEmpty() || pick == 1) starts.add(id);
            else kids.get(attached.get(rnd.nextInt(attached.size()))).add(id);
            attached.add(id);
        }
        for (int i = 0; i < n; i++) {
            outChildren[i] = new int[kids.get(i).size()];
            for (int j = 0; j < outChildren[i].length; j++) outChildren[i][j] = kids.get(i).get(j);
        }
        int[] s = new int[starts.size()];
        for (int i = 0; i < s.length; i++) s[i] = starts.get(i);
        outStart[0] = s;
    }

    /** Reference: record each depth, then regroup by scanning the processing order once per level. */
    static int[][] oracle(int[] start, int[][] children) {
        int[] depth = new int[children.length];
        List<Integer> order = new ArrayList<>();
        ArrayDeque<Integer> queue = new ArrayDeque<>();
        for (int s : start) queue.offer(s);
        while (!queue.isEmpty()) {
            int id = queue.poll();
            order.add(id);
            for (int c : children[id]) { depth[c] = depth[id] + 1; queue.offer(c); }
        }
        int count = 0;
        for (int id : order) count = Math.max(count, depth[id] + 1);
        int[][] res = new int[count][];
        for (int d = 0; d < count; d++) {
            List<Integer> row = new ArrayList<>();
            for (int id : order) if (depth[id] == d) row.add(id);
            res[d] = row.stream().mapToInt(Integer::intValue).toArray();
        }
        return res;
    }

    public static void main(String[] args) {
        // Example 1: one item expands to four, which expand to three.
        int[][] ch1 = {{1, 2, 3, 4}, {5}, {}, {6, 7}, {}, {}, {}, {}};
        if (!Arrays.equals(levelSizes(new int[] {0}, ch1), new int[] {1, 4, 3})) throw new AssertionError("example 1");
        // Example 2: two start items and no children make one level of size 2.
        if (!Arrays.equals(levelSizes(new int[] {0, 1}, new int[][] {{}, {}}), new int[] {2})) throw new AssertionError("example 2");
        // Empty input gives an empty array.
        if (levelSizes(new int[] {}, new int[][] {}).length != 0) throw new AssertionError("empty");
        // The live-size loop mixes levels on Example 1, so it differs from the correct answer.
        if (Arrays.equals(faultySizes(new int[] {0}, ch1), new int[] {1, 4, 3})) throw new AssertionError("faulty loop should differ");
        // A fan-out of 1000 from one item gives levels of size 1 and 1000.
        int[][] wide = new int[1001][];
        wide[0] = new int[1000];
        for (int i = 0; i < 1000; i++) { wide[0][i] = i + 1; wide[i + 1] = new int[0]; }
        if (!Arrays.equals(levelSizes(new int[] {0}, wide), new int[] {1, 1000})) throw new AssertionError("wide");
        // Random forests agree with the row lengths of the regrouped reference.
        Random rnd = new Random(1183);
        for (int t = 0; t < 3000; t++) {
            int n = rnd.nextInt(14);
            int[][] ch = new int[n][];
            int[][] st = new int[1][];
            generate(rnd, ch, st);
            int[][] ref = oracle(st[0], ch);
            int[] expected = new int[ref.length];
            for (int d = 0; d < ref.length; d++) expected[d] = ref[d].length;
            if (!Arrays.equals(levelSizes(st[0], ch), expected)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Recognize] Alternate Level Output (Author exercise)
<!-- id: sq-alternate-levels -->

**Approach.**
The method polls each level in plain first-in first-out order into a row, so the queue keeps the true discovery order. After the inner loop finishes, it reverses the finished row when its index in the result is odd and then stores the row. The reversal acts on the output list only, and the queue never sees it, so the children of the next level still appear in discovery order. The invariant is that the queue order is independent of the order of reported rows.

**Complexity.**
- **Time** is O(n), because each item is polled once and each odd row is reversed once, which costs its length.
- **Space** is O(w) for the queue plus O(n) for the returned rows.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.Random;

public final class AlternateLevels {
    /**
     * Returns levels, with every odd-numbered level reversed in the report only.
     * Time: O(n), polling plus one reversal per odd row.
     * Space: O(w) for the queue plus O(n) for the output.
     * Invariant: the queue order never depends on the reported order of a row.
     */
    static int[][] levels(int[] start, int[][] children) {
        List<int[]> result = new ArrayList<>();
        ArrayDeque<Integer> queue = new ArrayDeque<>();
        for (int s : start) queue.offer(s);
        // The outer loop runs once per level.
        while (!queue.isEmpty()) {
            int levelSize = queue.size();
            int[] row = new int[levelSize];
            // Polling keeps first-in first-out order, and the row records that order.
            for (int k = 0; k < levelSize; k++) {
                int id = queue.poll();
                row[k] = id;
                for (int c : children[id]) queue.offer(c);
            }
            // Only the finished row is reversed, after every child has been appended.
            if (result.size() % 2 == 1) {
                for (int i = 0, j = row.length - 1; i < j; i++, j--) {
                    int tmp = row[i]; row[i] = row[j]; row[j] = tmp;
                }
            }
            result.add(row);
        }
        return result.toArray(new int[0][]);
    }

    /** Builds a random forest: each attached id is a start item or a child of an earlier attached id. */
    static void generate(Random rnd, int[][] outChildren, int[][] outStart) {
        int n = outChildren.length;
        List<Integer> ids = new ArrayList<>();
        for (int i = 0; i < n; i++) ids.add(i);
        // A shuffled id order makes parents and children unrelated to numeric order.
        Collections.shuffle(ids, rnd);
        List<List<Integer>> kids = new ArrayList<>();
        for (int i = 0; i < n; i++) kids.add(new ArrayList<>());
        List<Integer> starts = new ArrayList<>();
        List<Integer> attached = new ArrayList<>();
        for (int id : ids) {
            int pick = rnd.nextInt(6);
            // One in six ids stays out of every list, so some items are never added.
            if (pick == 0) continue;
            // A start item has no parent; the first attached id must be one.
            if (attached.isEmpty() || pick == 1) starts.add(id);
            else kids.get(attached.get(rnd.nextInt(attached.size()))).add(id);
            attached.add(id);
        }
        for (int i = 0; i < n; i++) {
            outChildren[i] = new int[kids.get(i).size()];
            for (int j = 0; j < outChildren[i].length; j++) outChildren[i][j] = kids.get(i).get(j);
        }
        int[] s = new int[starts.size()];
        for (int i = 0; i < s.length; i++) s[i] = starts.get(i);
        outStart[0] = s;
    }

    /** Reference: record each depth, then regroup by scanning the processing order once per level. */
    static int[][] oracle(int[] start, int[][] children) {
        int[] depth = new int[children.length];
        List<Integer> order = new ArrayList<>();
        ArrayDeque<Integer> queue = new ArrayDeque<>();
        for (int s : start) queue.offer(s);
        while (!queue.isEmpty()) {
            int id = queue.poll();
            order.add(id);
            for (int c : children[id]) { depth[c] = depth[id] + 1; queue.offer(c); }
        }
        int count = 0;
        for (int id : order) count = Math.max(count, depth[id] + 1);
        int[][] res = new int[count][];
        for (int d = 0; d < count; d++) {
            List<Integer> row = new ArrayList<>();
            for (int id : order) if (depth[id] == d) row.add(id);
            res[d] = row.stream().mapToInt(Integer::intValue).toArray();
        }
        return res;
    }

    public static void main(String[] args) {
        // Example 1 from the exercise text.
        int[][] ch1 = {{1, 2}, {3, 4}, {5}, {6, 7}, {8}, {}, {}, {}, {}};
        if (!Arrays.deepEquals(levels(new int[] {0}, ch1), new int[][] {{0}, {2, 1}, {3, 4, 5}, {8, 7, 6}})) throw new AssertionError("example 1");
        // Example 2 from the exercise text.
        int[][] ch2 = {{2, 3}, {4}, {}, {5}, {}, {}};
        if (!Arrays.deepEquals(levels(new int[] {0, 1}, ch2), new int[][] {{0, 1}, {4, 3, 2}, {5}})) throw new AssertionError("example 2");
        // Empty input gives no rows.
        if (levels(new int[] {}, new int[][] {}).length != 0) throw new AssertionError("empty");
        // Random forests agree with the reference rows, reversed at odd positions.
        Random rnd = new Random(1184);
        for (int t = 0; t < 3000; t++) {
            int n = rnd.nextInt(14);
            int[][] ch = new int[n][];
            int[][] st = new int[1][];
            generate(rnd, ch, st);
            int[][] ref = oracle(st[0], ch);
            for (int d = 1; d < ref.length; d += 2) {
                int[] copy = ref[d].clone();
                for (int i = 0; i < copy.length; i++) ref[d][i] = copy[copy.length - 1 - i];
            }
            if (!Arrays.deepEquals(levels(st[0], ch), ref)) throw new AssertionError("random " + t);
        }
    }
}
```
