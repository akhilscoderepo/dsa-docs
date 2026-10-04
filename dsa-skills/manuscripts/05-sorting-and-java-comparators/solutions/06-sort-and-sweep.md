<!-- solutions-for: 05-sorting-and-java-comparators -->
### Solutions For Sorted Sweeps

#### Solution: [Build] Squares Of A Sorted Array (LeetCode 977)
<!-- id: so-sorted-squares -->

**Approach.**
The method squares each value into a new array and sorts that array. Squaring reverses the order of the negative values, so the squares are not sorted even when the input is. The sort restores the order. The invariant after the sort is that every adjacent pair of squares is nondecreasing and the multiset of squares is unchanged. A later chapter replaces the sort with a method that merges from both ends.

**Complexity.**
- **Time** is O(n log n), because the squaring pass costs O(n) and the sort dominates.
- **Space** is O(n) for the array of squares.

```java run
import java.util.*;

public final class SortedSquares {
    /**
     * Returns the squares of nums in nondecreasing order.
     * Time: O(n log n). Space: O(n).
     * Invariant: after the sort, adjacent squares are nondecreasing.
     */
    static int[] sortedSquares(int[] nums) {
        int[] out = new int[nums.length];
        // The squaring pass visits each value once.
        for (int i = 0; i < nums.length; i++) out[i] = nums[i] * nums[i];
        // Squaring flips the order of negative values, so the sort restores the order.
        Arrays.sort(out);
        return out;
    }

    public static void main(String[] args) {
        // The statement examples and the empty input.
        if (!Arrays.equals(sortedSquares(new int[] {-6, -2, 0, 3}), new int[] {0, 4, 9, 36})) throw new AssertionError("example 1");
        if (!Arrays.equals(sortedSquares(new int[] {-5, -5, 1}), new int[] {1, 25, 25})) throw new AssertionError("example 2");
        if (sortedSquares(new int[0]).length != 0) throw new AssertionError("empty");
        // Java fact from the lesson: squaring a sorted input can leave the output unsorted.
        int[] raw = {-6, -2, 0, 3};
        for (int i = 0; i < raw.length; i++) raw[i] *= raw[i];
        if (Arrays.equals(raw, new int[] {0, 4, 9, 36})) throw new AssertionError("squares are already sorted");
        // Random sorted inputs are checked against an oracle that picks the smallest remaining square each time.
        Random rnd = new Random(101);
        for (int t = 0; t < 500; t++) {
            int[] a = new int[rnd.nextInt(10)];
            for (int k = 0; k < a.length; k++) a[k] = rnd.nextInt(21) - 10;
            Arrays.sort(a);
            boolean[] used = new boolean[a.length];
            int[] expect = new int[a.length];
            for (int pos = 0; pos < a.length; pos++) {
                int best = -1;
                for (int k = 0; k < a.length; k++) if (!used[k] && (best < 0 || a[k] * a[k] < a[best] * a[best])) best = k;
                used[best] = true;
                expect[pos] = a[best] * a[best];
            }
            if (!Arrays.equals(sortedSquares(a), expect)) throw new AssertionError(Arrays.toString(a));
        }
    }
}
```

#### Solution: [Vary] Queue Reconstruction By Height (LeetCode 406)
<!-- id: so-queue-or-none -->

**Approach.**
The method sorts the people by height descending and `k` ascending. It then inserts each person at index `k`. When `k` is larger than the current list size, no position can satisfy the count, and the method returns an empty array at once. After all insertions, the method checks every person against the final queue, because a repeated pair, such as two people with the same height and count, passes the insertion step and still fails the count. The invariant during insertion is that every person already in the list has the correct count within the list, and the check at the end confirms the property for the whole queue.

**Complexity.**
- **Time** is O(n^2), because each insertion shifts up to n elements and the final check compares every pair.
- **Space** is O(n) for the list.

```java run
import java.util.*;

public final class QueueOrNone {
    /**
     * Rebuilds the queue, or returns an empty array when no queue exists.
     * Time: O(n^2). Space: O(n).
     * Invariant: before the final check, each person in the list has the correct count within the list.
     */
    static int[][] reconstruct(int[][] people) {
        int[][] sorted = people.clone();
        Arrays.sort(sorted, (p, q) -> p[0] != q[0] ? Integer.compare(q[0], p[0]) : Integer.compare(p[1], q[1]));
        List<int[]> queue = new ArrayList<>();
        for (int[] person : sorted) {
            // A count beyond the list size has no position, so no valid queue exists.
            if (person[1] > queue.size()) return new int[0][];
            queue.add(person[1], person);
        }
        int[][] out = queue.toArray(new int[0][]);
        // The final check rejects inputs that the insertion step cannot detect.
        return valid(out) ? out : new int[0][];
    }

    static boolean valid(int[][] q) {
        for (int i = 0; i < q.length; i++) {
            int c = 0;
            for (int j = 0; j < i; j++) if (q[j][0] >= q[i][0]) c++;
            if (c != q[i][1]) return false;
        }
        return true;
    }

    static boolean exists(int[][] a, int k) {
        if (k == a.length) return valid(a);
        for (int i = k; i < a.length; i++) {
            int[] t = a[k]; a[k] = a[i]; a[i] = t;
            boolean ok = exists(a, k + 1);
            t = a[k]; a[k] = a[i]; a[i] = t;
            if (ok) return true;
        }
        return false;
    }

    public static void main(String[] args) {
        // The statement examples and the empty input.
        if (!Arrays.deepEquals(reconstruct(new int[][] {{5, 1}, {9, 0}, {5, 0}}), new int[][] {{5, 0}, {5, 1}, {9, 0}})) throw new AssertionError("example 1");
        if (reconstruct(new int[][] {{4, 0}, {4, 0}}).length != 0) throw new AssertionError("example 2");
        if (reconstruct(new int[0][]).length != 0) throw new AssertionError("empty");
        if (reconstruct(new int[][] {{3, 1000000}}).length != 0) throw new AssertionError("count past the list");
        // Random inputs, valid and invalid, are checked against an exhaustive search over all permutations.
        Random rnd = new Random(102);
        for (int t = 0; t < 600; t++) {
            int n = 1 + rnd.nextInt(5);
            int[][] in = new int[n][];
            for (int i = 0; i < n; i++) in[i] = new int[] {rnd.nextInt(4), rnd.nextInt(n)};
            int[][] out = reconstruct(in);
            boolean possible = exists(in.clone(), 0);
            if (possible != (out.length == in.length)) throw new AssertionError("existence mismatch");
            if (possible && !valid(out)) throw new AssertionError("invalid answer");
        }
    }
}
```

#### Solution: [Boundary] A Long Run Of Equal Values (Author exercise)
<!-- id: so-frontier-max -->

**Approach.**
The method sorts a copy and sweeps it with a `long` frontier, which is the smallest slot that no earlier value holds. Each value takes the larger of itself and the frontier, and the frontier becomes that value plus one. The largest final value is the last taken value, which is `frontier - 1` after the sweep. Because the frontier is stored as a `long`, a run of `Integer.MAX_VALUE` values passes the `int` range without wrapping. The invariant after index `i` is that the taken values are distinct, each is at least its original value, and the frontier is one more than the largest of them.

**Complexity.**
- **Time** is O(n log n), because the sort dominates the linear sweep.
- **Space** is O(n) for the sorted copy.

```java run
import java.util.*;

public final class FrontierMax {
    /**
     * Returns the largest value after the fewest increments that make all values distinct.
     * Time: O(n log n). Space: O(n).
     * Invariant: after index i, frontier is one more than the largest taken value.
     */
    static long largestAfterDistinct(int[] nums) {
        // The empty array has no largest value, and the contract returns 0.
        if (nums.length == 0) return 0;
        int[] sorted = Arrays.copyOf(nums, nums.length);
        Arrays.sort(sorted);
        long frontier = Long.MIN_VALUE;
        // The sweep makes one decision per value.
        for (int v : sorted) {
            long taken = Math.max(v, frontier);
            frontier = taken + 1;
        }
        return frontier - 1;
    }

    /** Oracle: linear probing with a set, which gives the same set of final values for any order. */
    static long brute(int[] nums) {
        if (nums.length == 0) return 0;
        Set<Long> used = new HashSet<>();
        long max = Long.MIN_VALUE;
        for (int v : nums) {
            long c = v;
            while (!used.add(c)) c++;
            max = Math.max(max, c);
        }
        return max;
    }

    public static void main(String[] args) {
        // The statement examples and the empty input.
        if (largestAfterDistinct(new int[] {7, 7, 1}) != 8) throw new AssertionError("example 1");
        if (largestAfterDistinct(new int[] {Integer.MAX_VALUE, Integer.MAX_VALUE, Integer.MAX_VALUE}) != 2147483649L) throw new AssertionError("example 2");
        if (largestAfterDistinct(new int[0]) != 0) throw new AssertionError("empty");
        // A long run of equal values passes the int range in the sum of moves, so the oracle and the sweep must agree on it.
        int[] run = new int[2000];
        Arrays.fill(run, Integer.MAX_VALUE - 10);
        if (largestAfterDistinct(run) != (long) Integer.MAX_VALUE - 10 + 1999) throw new AssertionError("long run");
        // Random inputs with values near the limit are checked against the probing oracle.
        Random rnd = new Random(103);
        for (int t = 0; t < 500; t++) {
            int[] a = new int[rnd.nextInt(10)];
            for (int k = 0; k < a.length; k++) a[k] = rnd.nextBoolean() ? Integer.MAX_VALUE - rnd.nextInt(3) : rnd.nextInt(4) - 2;
            if (largestAfterDistinct(a) != brute(a)) throw new AssertionError(Arrays.toString(a));
        }
    }
}
```

#### Solution: [Recognize] Minimum Increment To Make Array Unique (LeetCode 945)
<!-- id: so-min-increment -->

**Approach.**
The method sorts a copy and sweeps it with a `long` frontier. Each value takes the larger of itself and the frontier, the cost grows by the difference, and the frontier becomes the taken value plus one. In sorted order, a value below the frontier collides with a taken slot, and the smallest free slot is the frontier itself. A larger slot would raise the frontier and cost more later, so the smallest slot is a safe move. The invariant after index `i` is that `moves` is the minimum cost for the first `i + 1` sorted values. The harness checks the method against the probing oracle of the lesson.

**Complexity.**
- **Time** is O(n log n), because the sort dominates the linear sweep.
- **Space** is O(n) for the sorted copy.

```java run
import java.util.*;

public final class MinIncrement {
    /**
     * Returns the minimum number of +1 moves that make all values distinct.
     * Time: O(n log n). Space: O(n).
     * Invariant: after index i, moves is the minimum cost for the first i + 1 sorted values.
     */
    static long minIncrements(int[] nums) {
        int[] sorted = Arrays.copyOf(nums, nums.length);
        Arrays.sort(sorted);
        long frontier = Long.MIN_VALUE;
        long moves = 0;
        // One decision per value, in sorted order.
        for (int v : sorted) {
            // A value below the frontier moves up to the frontier.
            long taken = Math.max(v, frontier);
            moves += taken - v;
            frontier = taken + 1;
        }
        return moves;
    }

    /** Lesson code: probing with a set, kept as the oracle. */
    static long brute(int[] nums) {
        Set<Long> used = new HashSet<>();
        long moves = 0;
        for (int v : nums) {
            long c = v;
            while (!used.add(c)) { c++; moves++; }
        }
        return moves;
    }

    public static void main(String[] args) {
        // The statement examples and the empty input.
        if (minIncrements(new int[] {5, 2, 5, 5}) != 3) throw new AssertionError("example 1");
        if (minIncrements(new int[] {0, 0, 0, 0, 10}) != 6) throw new AssertionError("example 2");
        if (minIncrements(new int[0]) != 0) throw new AssertionError("empty");
        // A run of 100000 equal values needs more moves than int holds, so the counter must be long.
        int[] run = new int[100000];
        if (minIncrements(run) != 4999950000L) throw new AssertionError("long run");
        // Random inputs are checked against the probing oracle.
        Random rnd = new Random(104);
        for (int t = 0; t < 500; t++) {
            int[] a = new int[rnd.nextInt(12)];
            for (int k = 0; k < a.length; k++) a[k] = rnd.nextInt(6);
            if (minIncrements(a) != brute(a)) throw new AssertionError(Arrays.toString(a));
        }
    }
}
```
