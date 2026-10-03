<!-- solutions-for: 10-endpoint-ordering-contracts -->
### Endpoint Ordering Contracts

#### Solution: [Build] Order By Start Then End (Author exercise)
<!-- id: iv-order-start-end -->

**Approach.** The comparator compares the starts with `Integer.compare`, and only when they are equal compares the ends, so two intervals with the same start are ordered by the smaller end first. The tie rule matters because equal starts are common and an order that leaves them unspecified would let the result vary between runs of different sorting methods. The input must stay unchanged, so each row is cloned before sorting, since copying only the outer array would share the inner arrays with the caller. The oracle sorts by a single `long` key built from both endpoints and compares the results.

**Complexity.** O(n log n) time for the sort and O(n) extra space for the copies.

```java run
import java.util.Arrays;
import java.util.Random;

public final class OrderStartEnd {
    static int[][] orderByStartThenEnd(int[][] intervals) {
        int[][] copy = new int[intervals.length][];
        for (int i = 0; i < intervals.length; i++) copy[i] = intervals[i].clone();
        Arrays.sort(copy, (a, b) -> {
            int byStart = Integer.compare(a[0], b[0]);
            return byStart != 0 ? byStart : Integer.compare(a[1], b[1]);
        });
        return copy;
    }
    static int[][] oracle(int[][] intervals) {
        long[] keys = new long[intervals.length];
        for (int i = 0; i < intervals.length; i++) keys[i] = (long) (intervals[i][0] + 100) * 1000 + (intervals[i][1] + 100);
        Arrays.sort(keys);
        int[][] out = new int[keys.length][2];
        for (int i = 0; i < keys.length; i++) {
            out[i][0] = (int) (keys[i] / 1000) - 100;
            out[i][1] = (int) (keys[i] % 1000) - 100;
        }
        return out;
    }

    public static void main(String[] args) {
        int[][] ex = {{3, 5}, {1, 4}, {3, 4}, {1, 2}};
        if (!Arrays.deepEquals(orderByStartThenEnd(ex), new int[][] {{1, 2}, {1, 4}, {3, 4}, {3, 5}})) throw new AssertionError("example 1");
        if (!Arrays.deepEquals(orderByStartThenEnd(new int[][] {{2, 2}}), new int[][] {{2, 2}})) throw new AssertionError("example 2");
        if (!Arrays.deepEquals(ex, new int[][] {{3, 5}, {1, 4}, {3, 4}, {1, 2}})) throw new AssertionError("the input must not change");
        int[][] sorted = orderByStartThenEnd(ex);
        sorted[0][0] = 99;
        if (ex[3][0] != 1) throw new AssertionError("rows must be copied, not shared");
        if (orderByStartThenEnd(new int[0][]).length != 0) throw new AssertionError("empty input");
        Random rnd = new Random(10101);
        for (int t = 0; t < 3000; t++) {
            int n = rnd.nextInt(10);
            int[][] a = new int[n][2];
            for (int i = 0; i < n; i++) { int s = rnd.nextInt(8); a[i][0] = s; a[i][1] = s + rnd.nextInt(5); }
            if (!Arrays.deepEquals(orderByStartThenEnd(a), oracle(a))) throw new AssertionError("differs on " + Arrays.deepToString(a));
        }
    }
}
```

#### Solution: [Vary] Order By End Then Start (Author exercise)
<!-- id: iv-order-end-start -->

**Approach.** The comparator now compares the ends first and the starts only on equal ends. Sorting by end puts the interval that finishes first at the front, which is the order that supports selecting as many compatible intervals as possible, because choosing the earliest finish leaves the most room afterwards. It does not support merging, because a long interval that starts early and ends late is placed after shorter ones it overlaps, and a single pass that keeps only the last block cannot reconnect the earlier ones. The program checks the order against an oracle, and then shows a small input on which a merge scan over the end order produces more blocks than the true count.

**Complexity.** O(n log n) time for the sort and O(n) extra space for the copies.

```java run
import java.util.Arrays;
import java.util.Random;

public final class OrderEndStart {
    static int[][] orderByEndThenStart(int[][] intervals) {
        int[][] copy = new int[intervals.length][];
        for (int i = 0; i < intervals.length; i++) copy[i] = intervals[i].clone();
        Arrays.sort(copy, (a, b) -> {
            int byEnd = Integer.compare(a[1], b[1]);
            return byEnd != 0 ? byEnd : Integer.compare(a[0], b[0]);
        });
        return copy;
    }
    static boolean ordered(int[][] a) {
        for (int i = 1; i < a.length; i++) {
            if (a[i - 1][1] > a[i][1]) return false;
            if (a[i - 1][1] == a[i][1] && a[i - 1][0] > a[i][0]) return false;
        }
        return true;
    }
    static int blocksAfterEndOrder(int[][] intervals) {
        int[][] s = orderByEndThenStart(intervals);
        int blocks = 1, reach = s[0][1];
        for (int i = 1; i < s.length; i++) {
            if (s[i][0] <= reach) reach = Math.max(reach, s[i][1]);
            else { blocks++; reach = s[i][1]; }
        }
        return blocks;
    }
    static int trueBlocks(int[][] intervals) {
        int[][] s = intervals.clone();
        Arrays.sort(s, (a, b) -> Integer.compare(a[0], b[0]));
        int blocks = 1, reach = s[0][1];
        for (int i = 1; i < s.length; i++) {
            if (s[i][0] <= reach) reach = Math.max(reach, s[i][1]);
            else { blocks++; reach = s[i][1]; }
        }
        return blocks;
    }

    public static void main(String[] args) {
        if (!Arrays.deepEquals(orderByEndThenStart(new int[][] {{1, 10}, {2, 3}, {2, 5}, {0, 3}}), new int[][] {{0, 3}, {2, 3}, {2, 5}, {1, 10}})) throw new AssertionError("example 1");
        if (!Arrays.deepEquals(orderByEndThenStart(new int[][] {{5, 6}, {1, 6}, {3, 6}}), new int[][] {{1, 6}, {3, 6}, {5, 6}})) throw new AssertionError("example 2");
        int[][] trap = {{1, 2}, {5, 6}, {0, 10}};
        if (trueBlocks(trap) != 1 || blocksAfterEndOrder(trap) != 2) throw new AssertionError("end order cannot be used for merging");
        Random rnd = new Random(10102);
        for (int t = 0; t < 3000; t++) {
            int n = rnd.nextInt(10);
            int[][] a = new int[n][2];
            for (int i = 0; i < n; i++) { int s = rnd.nextInt(8); a[i][0] = s; a[i][1] = s + rnd.nextInt(5); }
            int[][] sorted = orderByEndThenStart(a);
            if (!ordered(sorted) || sorted.length != n) throw new AssertionError("not ordered: " + Arrays.deepToString(a));
        }
    }
}
```

#### Solution: [Boundary] Equal And Extreme Endpoints (Author exercise)
<!-- id: iv-extreme-endpoints -->

**Approach.** A comparator written as `a[0] - b[0]` computes a difference that can leave the range of `int`: `2147483647 - (-2147483648)` wraps to minus one, so the larger start compares as smaller. `Integer.compare` returns the sign directly and never subtracts, so it is correct for every pair of `int` values, and equal endpoints compare as equal. The program asserts the wrapped difference, checks that the subtraction comparator and `Integer.compare` disagree on the extreme pair, sorts with the safe comparator, and checks the result against a sort of `long` keys on random inputs that include the extremes.

**Complexity.** O(n log n) time for the sort and O(n) extra space for the copies.

```java run
import java.util.Arrays;
import java.util.Random;

public final class ExtremeEndpoints {
    static int[][] sortSafe(int[][] intervals) {
        int[][] copy = new int[intervals.length][];
        for (int i = 0; i < intervals.length; i++) copy[i] = intervals[i].clone();
        Arrays.sort(copy, (a, b) -> {
            int byStart = Integer.compare(a[0], b[0]);
            return byStart != 0 ? byStart : Integer.compare(a[1], b[1]);
        });
        return copy;
    }
    static int[][] oracle(int[][] intervals) {
        long[][] wide = new long[intervals.length][];
        for (int i = 0; i < intervals.length; i++) wide[i] = new long[] {intervals[i][0], intervals[i][1]};
        Arrays.sort(wide, (a, b) -> a[0] != b[0] ? Long.compare(a[0], b[0]) : Long.compare(a[1], b[1]));
        int[][] out = new int[wide.length][];
        for (int i = 0; i < wide.length; i++) out[i] = new int[] {(int) wide[i][0], (int) wide[i][1]};
        return out;
    }

    public static void main(String[] args) {
        int[][] ex1 = {{Integer.MAX_VALUE, Integer.MAX_VALUE}, {Integer.MIN_VALUE, Integer.MIN_VALUE}, {0, 0}};
        int[][] want1 = {{Integer.MIN_VALUE, Integer.MIN_VALUE}, {0, 0}, {Integer.MAX_VALUE, Integer.MAX_VALUE}};
        if (!Arrays.deepEquals(sortSafe(ex1), want1)) throw new AssertionError("example 1");
        if (!Arrays.deepEquals(sortSafe(new int[][] {{1, 2}, {1, 2}}), new int[][] {{1, 2}, {1, 2}})) throw new AssertionError("example 2");
        if (Integer.MAX_VALUE - Integer.MIN_VALUE != -1) throw new AssertionError("the difference wraps to minus one");
        int bySubtraction = Integer.MAX_VALUE - Integer.MIN_VALUE;
        if (Integer.signum(bySubtraction) == Integer.signum(Integer.compare(Integer.MAX_VALUE, Integer.MIN_VALUE))) throw new AssertionError("subtraction should give the wrong sign");
        Random rnd = new Random(10103);
        int[] pool = {Integer.MIN_VALUE, Integer.MIN_VALUE + 1, -1, 0, 1, Integer.MAX_VALUE - 1, Integer.MAX_VALUE};
        for (int t = 0; t < 3000; t++) {
            int n = rnd.nextInt(9);
            int[][] a = new int[n][2];
            for (int i = 0; i < n; i++) {
                int x = pool[rnd.nextInt(pool.length)], y = pool[rnd.nextInt(pool.length)];
                a[i][0] = Math.min(x, y);
                a[i][1] = Math.max(x, y);
            }
            if (!Arrays.deepEquals(sortSafe(a), oracle(a))) throw new AssertionError("differs on " + Arrays.deepToString(a));
        }
    }
}
```

#### Solution: [Recognize] Merge Intervals (LeetCode 56)
<!-- id: iv-merge-count -->

**Approach.** After sorting by start, every interval already processed begins no later than the current one, so the only processed interval that can still touch it is the block with the furthest reach. The scan keeps that one number. If the current start does not pass the reach, the interval joins the block and the reach becomes the larger of the two ends. If it passes the reach, no later interval can reconnect to it, because every later start is even larger, so a new block opens. Touching endpoints share a point, so a start equal to the reach joins the block. The oracle merges any two touching intervals repeatedly until none remain, and the program shows that an end order gives a wrong count on a small input.

**Complexity.** O(n log n) time for the sort and O(1) extra space for the scan, plus the sorted copy.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

public final class MergeCount {
    static int countBlocks(int[][] intervals) {
        if (intervals.length == 0) return 0;
        int[][] sorted = intervals.clone();
        Arrays.sort(sorted, (a, b) -> Integer.compare(a[0], b[0]));
        int blocks = 1;
        long reach = sorted[0][1];
        for (int i = 1; i < sorted.length; i++) {
            if (sorted[i][0] <= reach) reach = Math.max(reach, sorted[i][1]);
            else { blocks++; reach = sorted[i][1]; }
        }
        return blocks;
    }
    static int blocksByEnd(int[][] intervals) {
        int[][] sorted = intervals.clone();
        Arrays.sort(sorted, (a, b) -> Integer.compare(a[1], b[1]));
        int blocks = 1, reach = sorted[0][1];
        for (int i = 1; i < sorted.length; i++) {
            if (sorted[i][0] <= reach) reach = Math.max(reach, sorted[i][1]);
            else { blocks++; reach = sorted[i][1]; }
        }
        return blocks;
    }
    static int oracle(int[][] intervals) {
        List<int[]> list = new ArrayList<>();
        for (int[] c : intervals) list.add(new int[] {c[0], c[1]});
        boolean changed = true;
        while (changed) {
            changed = false;
            for (int i = 0; i < list.size() && !changed; i++)
                for (int j = i + 1; j < list.size() && !changed; j++) {
                    int[] a = list.get(i), b = list.get(j);
                    if (a[0] <= b[1] && b[0] <= a[1]) {
                        a[0] = Math.min(a[0], b[0]);
                        a[1] = Math.max(a[1], b[1]);
                        list.remove(j);
                        changed = true;
                    }
                }
        }
        return list.size();
    }

    public static void main(String[] args) {
        if (countBlocks(new int[][] {{1, 3}, {2, 6}, {8, 10}, {15, 18}}) != 3) throw new AssertionError("example 1");
        if (countBlocks(new int[][] {{1, 4}, {4, 5}}) != 1) throw new AssertionError("example 2");
        int[][] trap = {{1, 2}, {5, 6}, {0, 10}};
        if (countBlocks(trap) != 1 || blocksByEnd(trap) == 1) throw new AssertionError("end order must fail on the trap");
        Random rnd = new Random(10104);
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(9);
            int[][] a = new int[n][2];
            for (int i = 0; i < n; i++) { int s = rnd.nextInt(20); a[i][0] = s; a[i][1] = s + rnd.nextInt(5); }
            if (countBlocks(a) != oracle(a)) throw new AssertionError("differs on " + Arrays.deepToString(a));
        }
    }
}
```
