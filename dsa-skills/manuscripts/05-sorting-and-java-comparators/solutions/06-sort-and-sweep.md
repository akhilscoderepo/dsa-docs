<!-- solutions-for: 05-sort-and-sweep -->
### Sort And Sweep

#### Solution: [Build] Squares of a Sorted Array (LeetCode 977)
<!-- id: so-sorted-squares -->

**Approach.** Square every element, then sort the result. Squaring maps the negative side onto large positive values, so the squares are not in order even though the input is, and the sort restores the order. The check compares with an independent two-pointer merge from both ends, which is the linear method that a later chapter develops, and also asserts that the output length matches and that every output is non-negative. Values up to 10000 square to at most 100 million, which fits in an `int`.

**Complexity.** O(n log n) time and O(n) extra space.

```java run
import java.util.Arrays;
import java.util.Random;

public final class SortedSquares {
    static int[] sortedSquares(int[] nums) {
        int[] out = new int[nums.length];
        for (int i = 0; i < nums.length; i++) out[i] = nums[i] * nums[i];
        Arrays.sort(out);
        return out;
    }
    static int[] twoEnds(int[] nums) {
        int[] out = new int[nums.length];
        int lo = 0, hi = nums.length - 1;
        for (int k = nums.length - 1; k >= 0; k--) {
            int a = nums[lo] * nums[lo], b = nums[hi] * nums[hi];
            if (a > b) { out[k] = a; lo++; } else { out[k] = b; hi--; }
        }
        return out;
    }

    public static void main(String[] args) {
        if (!Arrays.equals(sortedSquares(new int[] {-6, -2, 1, 5}), new int[] {1, 4, 25, 36})) throw new AssertionError("example 1");
        if (!Arrays.equals(sortedSquares(new int[] {-3, -3, 0}), new int[] {0, 9, 9})) throw new AssertionError("example 2");
        if (!Arrays.equals(sortedSquares(new int[] {-10000, 10000}), new int[] {100000000, 100000000})) throw new AssertionError("largest squares fit in an int");
        Random rnd = new Random(551);
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(12);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(21) - 10;
            Arrays.sort(a);
            int[] got = sortedSquares(a);
            if (!Arrays.equals(got, twoEnds(a))) throw new AssertionError("differs from the two-ends oracle on " + Arrays.toString(a));
            if (got[0] < 0) throw new AssertionError("squares are non-negative");
        }
    }
}
```

#### Solution: [Vary] Queue Reconstruction by Height (LeetCode 406)
<!-- id: so-queue-free-slots -->

**Approach.** Sort the rows by height ascending and, among equal heights, by count descending. Process them in that order and put each person into the empty position that has exactly `count` empty positions before it. Everyone processed later is at least as tall, and among equals has a smaller count, so every empty position before the chosen one will be filled by someone who counts toward this person, and nobody who counts is placed behind. The test builds random valid queues and requires that the method reproduces the original queue exactly.

**Complexity.** O(n log n) for the sort and O(n^2) for the slot scans, with O(n) extra space.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.Random;

public final class QueueFreeSlots {
    static int[][] rebuild(int[][] people) {
        int[][] order = people.clone();
        Arrays.sort(order, (p, q) -> p[0] != q[0] ? Integer.compare(p[0], q[0]) : Integer.compare(q[1], p[1]));
        int[][] line = new int[order.length][];
        for (int[] p : order) {
            int empty = -1, at = 0;
            while (true) {
                if (line[at] == null && ++empty == p[1]) break;
                at++;
            }
            line[at] = p;
        }
        return line;
    }

    public static void main(String[] args) {
        int[][] ex1 = rebuild(new int[][] {{2, 4}, {6, 0}, {3, 2}, {3, 0}, {4, 2}, {5, 0}});
        if (!Arrays.deepEquals(ex1, new int[][] {{3, 0}, {5, 0}, {3, 2}, {6, 0}, {2, 4}, {4, 2}})) throw new AssertionError("example 1");
        if (!Arrays.deepEquals(rebuild(new int[][] {{9, 0}, {4, 1}, {9, 1}}), new int[][] {{9, 0}, {4, 1}, {9, 1}})) throw new AssertionError("example 2");
        Random rnd = new Random(552);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(8);
            int[][] queue = new int[n][];
            for (int i = 0; i < n; i++) {
                int h = 1 + rnd.nextInt(5), taller = 0;
                for (int j = 0; j < i; j++) if (queue[j][0] >= h) taller++;
                queue[i] = new int[] {h, taller};
            }
            List<int[]> shuffled = new ArrayList<>(Arrays.asList(queue));
            Collections.shuffle(shuffled, rnd);
            int[][] got = rebuild(shuffled.toArray(new int[0][]));
            if (!Arrays.deepEquals(got, queue)) throw new AssertionError("not the original queue: " + Arrays.deepToString(got) + " vs " + Arrays.deepToString(queue));
        }
    }
}
```

#### Solution: [Boundary] A Long Run of Equal Values (Author exercise)
<!-- id: so-long-equal-run -->

**Approach.** Sort a copy and sweep with a `long` named `next`, the smallest value that is still unused. Each element is raised to `max(value, next)`, the increase is added to a `long` total, and `next` becomes the placed value plus one. For a run of k equal values the increases are 0, 1, up to k minus 1, so the total is k(k-1)/2, which for one hundred thousand equals 4999950000 and is above `Integer.MAX_VALUE`. The program asserts the closed form for several run lengths, shows that an `int` accumulator would have wrapped, and compares the sweep with an exhaustive search over all increase vectors on tiny arrays.

**Complexity.** O(n log n) time for the sort and O(n) for the sweep, with O(n) extra space for the copy.

```java run
import java.util.Arrays;
import java.util.Random;

public final class LongEqualRun {
    static long minTotal(int[] nums) {
        int[] a = nums.clone();
        Arrays.sort(a);
        long total = 0, next = 0;
        for (int v : a) {
            long placed = Math.max(v, next);
            total += placed - v;
            next = placed + 1;
        }
        return total;
    }
    static long best;
    static void search(int[] a, int i, boolean[] used, long cost, int limit) {
        if (cost >= best) return;
        if (i == a.length) { best = cost; return; }
        for (int v = a[i]; v <= limit; v++) {
            if (used[v]) continue;
            used[v] = true;
            search(a, i + 1, used, cost + (v - a[i]), limit);
            used[v] = false;
        }
    }
    static long exhaustive(int[] a) {
        best = Long.MAX_VALUE;
        search(a, 0, new boolean[16], 0, 15);
        return best;
    }

    public static void main(String[] args) {
        if (minTotal(new int[] {5, 5, 5, 5}) != 6) throw new AssertionError("example 1");
        int[] zeros = new int[100000];
        long big = minTotal(zeros);
        if (big != 4999950000L) throw new AssertionError("example 2");
        if (big <= Integer.MAX_VALUE) throw new AssertionError("the answer must exceed the int range");
        int wrapped = 0;
        for (int i = 0; i < 100000; i++) wrapped += i;
        if (wrapped == big) throw new AssertionError("an int accumulator would have wrapped");
        for (int k = 0; k <= 50; k++) {
            int[] run = new int[k];
            Arrays.fill(run, 7);
            if (minTotal(run) != (long) k * (k - 1) / 2) throw new AssertionError("closed form fails for k = " + k);
        }
        if (minTotal(new int[0]) != 0) throw new AssertionError("empty array");
        Random rnd = new Random(553);
        for (int t = 0; t < 400; t++) {
            int n = 1 + rnd.nextInt(5);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(5);
            if (minTotal(a) != exhaustive(a)) throw new AssertionError("differs from the exhaustive search on " + Arrays.toString(a));
        }
    }
}
```

#### Solution: [Recognize] Minimum Increment to Make Array Unique (LeetCode 945)
<!-- id: so-minimum-increment-unique -->

**Approach.** Sort a copy, then carry the frontier, the last finalized value. An element not above the frontier is raised to frontier plus one, and an element above it stays as it is. The cost of each element is its final value minus its request, summed into a `long`. The oracle is the slow bumping method with a hash set, which checks one number at a time and does not depend on the sorted order, and the two must agree on random arrays that include long runs of equal values and sparse values.

**Complexity.** O(n log n) time and O(n) extra space for the sorted copy; the bumping oracle is O(n^2) in the worst case.

```java run
import java.util.Arrays;
import java.util.HashSet;
import java.util.Random;
import java.util.Set;

public final class MinimumIncrementUnique {
    static long minIncrementForUnique(int[] nums) {
        int[] a = nums.clone();
        Arrays.sort(a);
        long cost = 0, frontier = Long.MIN_VALUE;
        for (int x : a) {
            long placed = Math.max(x, frontier + 1);
            cost += placed - x;
            frontier = placed;
        }
        return cost;
    }
    static long bumping(int[] requests) {
        Set<Integer> taken = new HashSet<>();
        long moves = 0;
        for (int want : requests) {
            int got = want;
            while (taken.contains(got)) { got++; moves++; }
            taken.add(got);
        }
        return moves;
    }

    public static void main(String[] args) {
        if (minIncrementForUnique(new int[] {3, 2, 1, 2, 1, 7}) != 6) throw new AssertionError("example 1");
        if (minIncrementForUnique(new int[] {4, 9, 20}) != 0) throw new AssertionError("example 2");
        if (minIncrementForUnique(new int[] {0}) != 0) throw new AssertionError("single element");
        Random rnd = new Random(554);
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(16);
            int range = 1 + rnd.nextInt(8);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(range);
            int[] copy = a.clone();
            if (minIncrementForUnique(a) != bumping(copy)) throw new AssertionError("differs from the bumping oracle on " + Arrays.toString(copy));
            if (!Arrays.equals(a, copy)) throw new AssertionError("the argument must not be modified");
        }
    }
}
```
