<!-- solutions-for: 04-hash-maps-and-sets -->
### Solutions For Runs In A Set

#### Solution: [Build] Start Of The Longest Run (LeetCode 128)
<!-- id: hm-longest-run-start -->

**Approach.**
The method builds a set of the distinct values. It visits each value once and applies the predecessor test. When `x - 1` is in the set, the value lies inside a run that its start covers, and the loop skips it. A value without a predecessor starts a run, and the successor walk counts the length. A run replaces the best one when it is longer, or equally long with a smaller start. The invariant is that every run is walked exactly once from its start. The walks together cost one step per distinct value. The guards at `Integer.MIN_VALUE` and `Integer.MAX_VALUE` stop the arithmetic from wrapping, and the harness asserts both the wrap and the silent `Long` lookup from the lesson.

**Complexity.**
- **Time** is O(n) on average, because the set takes n insertions and the walks visit each distinct value once.
- **Space** is O(n) for the set of distinct values.

```java run
import java.util.*;

public final class LongestRunStart {
    /**
     * Returns {start, length} of the longest run, the smallest start on ties, {0, 0} when empty.
     * Time: O(n) expected. Space: O(n).
     * Invariant: each run is walked once, from its start.
     */
    static int[] longestRun(int[] nums) {
        Set<Integer> all = new HashSet<>();
        for (int x : nums) all.add(x);
        int bestStart = 0, bestLen = 0;
        // The loop visits each distinct value once, in no promised order.
        for (int x : all) {
            // A present predecessor means a walk from an earlier start covers x.
            if (x != Integer.MIN_VALUE && all.contains(x - 1)) continue;
            int len = 1;
            // The walk stops at the end of the run, or before the int range wraps.
            while (x + len != Integer.MIN_VALUE && all.contains(x + len)) len++;
            // A longer run wins; an equal run wins only with a smaller start.
            if (len > bestLen || (len == bestLen && x < bestStart)) {
                bestLen = len;
                bestStart = x;
            }
        }
        return new int[] {bestStart, bestLen};
    }

    public static void main(String[] args) {
        // The statement examples, the empty array and the lesson trace input.
        if (!Arrays.equals(longestRun(new int[] {20, 5, 21, 6, 22, 7, 8}), new int[] {5, 4})) throw new AssertionError("example 1");
        if (!Arrays.equals(longestRun(new int[] {9, 2, 3, 10}), new int[] {2, 2})) throw new AssertionError("example 2");
        if (!Arrays.equals(longestRun(new int[0]), new int[] {0, 0})) throw new AssertionError("empty");
        if (!Arrays.equals(longestRun(new int[] {50, 12, 13, 49, 11, 51, 52, 14}), new int[] {11, 4})) throw new AssertionError("trace tie");
        // Range ends: a run at the top of int and a run at the bottom.
        if (!Arrays.equals(longestRun(new int[] {Integer.MAX_VALUE - 1, Integer.MAX_VALUE}), new int[] {Integer.MAX_VALUE - 1, 2})) throw new AssertionError("top");
        if (!Arrays.equals(longestRun(new int[] {Integer.MIN_VALUE, Integer.MIN_VALUE + 1}), new int[] {Integer.MIN_VALUE, 2})) throw new AssertionError("bottom");
        // Java facts from the lesson.
        Set<Integer> probe = new HashSet<>(List.of(5));
        if (probe.contains(4 + 1L)) throw new AssertionError("a Long never matches an Integer");
        if (!probe.contains(4 + 1)) throw new AssertionError("int lookup");
        if (Integer.MIN_VALUE - 1 != Integer.MAX_VALUE) throw new AssertionError("wrap");
        // Random arrays are checked against a sort-based oracle.
        Random rnd = new Random(56);
        for (int t = 0; t < 600; t++) {
            int[] a = new int[rnd.nextInt(12)];
            for (int k = 0; k < a.length; k++) a[k] = rnd.nextInt(16) - 5;
            int[] s = a.clone();
            Arrays.sort(s);
            int bestStart = 0, bestLen = 0, i = 0;
            while (i < s.length) {
                int j = i;
                while (j + 1 < s.length && (s[j + 1] == s[j] || s[j + 1] == s[j] + 1)) j++;
                int len = s[j] - s[i] + 1;
                if (len > bestLen) { bestLen = len; bestStart = s[i]; }
                i = j + 1;
            }
            if (!Arrays.equals(longestRun(a), new int[] {bestStart, bestLen})) throw new AssertionError(Arrays.toString(a));
        }
    }
}
```

#### Solution: [Vary] Shared By Three Arrays (LeetCode 349)
<!-- id: hm-shared-by-three -->

**Approach.**
The method puts the values of `b` and `c` into two sets. It then scans `a` from left to right. A value joins the answer when both sets hold it and a third set shows that the answer has not reported it. Each value of `a` costs at most three set operations, and the scan order of `a` gives the order of first occurrence. The invariant is that after index `i`, the answer holds the values of `a[0..i]` that occur in `b` and in `c`, once each.

**Complexity.**
- **Time** is O(n + m + p) on average for array lengths n, m and p, because each array is read once with expected constant-time set operations.
- **Space** is O(n + m + p), because the three sets and the answer hold at most that many values.

```java run
import java.util.*;

public final class SharedByThree {
    /**
     * Returns the values present in a, b and c, once each, in first-occurrence order of a.
     * Time: O(n + m + p) expected. Space: O(n + m + p).
     * Invariant: after index i, out holds the values of a[0..i] present in b and c, once each.
     */
    static int[] sharedByThree(int[] a, int[] b, int[] c) {
        Set<Integer> inB = new HashSet<>(), inC = new HashSet<>();
        for (int y : b) inB.add(y);
        for (int z : c) inC.add(z);
        Set<Integer> reported = new HashSet<>();
        List<Integer> out = new ArrayList<>();
        // One scan of a; each value needs two tests and one report check.
        for (int x : a) {
            if (inB.contains(x) && inC.contains(x) && reported.add(x)) {
                out.add(x);
            }
        }
        int[] res = new int[out.size()];
        for (int k = 0; k < res.length; k++) res[k] = out.get(k);
        return res;
    }

    public static void main(String[] args) {
        // The statement examples.
        if (!Arrays.equals(sharedByThree(new int[] {5, 1, 5, 2, 9}, new int[] {2, 5, 7, 5}, new int[] {5, 2, 2}), new int[] {5, 2})) throw new AssertionError("example 1");
        if (sharedByThree(new int[] {1, 2}, new int[] {3}, new int[] {1}).length != 0) throw new AssertionError("example 2");
        if (sharedByThree(new int[0], new int[0], new int[0]).length != 0) throw new AssertionError("all empty");
        // Random arrays are checked against a triple-scan oracle.
        Random rnd = new Random(57);
        for (int t = 0; t < 500; t++) {
            int[][] arr = new int[3][];
            for (int q = 0; q < 3; q++) {
                arr[q] = new int[rnd.nextInt(8)];
                for (int k = 0; k < arr[q].length; k++) arr[q][k] = rnd.nextInt(6);
            }
            List<Integer> expect = new ArrayList<>();
            for (int x : arr[0]) {
                boolean b = false, c = false;
                for (int y : arr[1]) if (y == x) b = true;
                for (int z : arr[2]) if (z == x) c = true;
                if (b && c && !expect.contains(x)) expect.add(x);
            }
            int[] got = sharedByThree(arr[0], arr[1], arr[2]);
            if (got.length != expect.size()) throw new AssertionError("size");
            for (int k = 0; k < got.length; k++) if (got[k] != expect.get(k)) throw new AssertionError("order");
        }
    }
}
```

#### Solution: [Boundary] Duplicate Starts (Author exercise)
<!-- id: hm-duplicate-starts -->

**Approach.**
The number of runs equals the number of run starts, because each run has exactly one start. The method inserts all values into a set first, so a repeated value collapses to one element. It then counts the elements `x` whose predecessor `x - 1` is absent. A loop over the array would count a repeated start once for each copy, which gives a larger result, so the loop reads the set. The invariant is that `count` holds the number of starts among the elements read so far. The harness runs the array-loop variant on the first example to show the larger result.

**Complexity.**
- **Time** is O(n) on average, because the set takes n insertions and the count makes one test per distinct value.
- **Space** is O(n) for the set.

```java run
import java.util.*;

public final class DuplicateStarts {
    /**
     * Counts maximal runs of consecutive values.
     * Time: O(n) expected. Space: O(n).
     * Invariant: count equals the number of starts among the distinct values read so far.
     */
    static int countRuns(int[] nums) {
        Set<Integer> all = new HashSet<>();
        for (int x : nums) all.add(x);
        int count = 0;
        // The loop reads the set, so a repeated value is tested once.
        for (int x : all) {
            if (x == Integer.MIN_VALUE || !all.contains(x - 1)) count++;
        }
        return count;
    }

    /** The mistake: the loop reads the array, so a repeated start counts more than once. */
    static int countOverArray(int[] nums) {
        Set<Integer> all = new HashSet<>();
        for (int x : nums) all.add(x);
        int count = 0;
        for (int x : nums) if (x == Integer.MIN_VALUE || !all.contains(x - 1)) count++;
        return count;
    }

    public static void main(String[] args) {
        // The statement examples.
        if (countRuns(new int[] {1, 1, 2, 5, 5, 5, 9}) != 3) throw new AssertionError("example 1");
        if (countRuns(new int[0]) != 0) throw new AssertionError("example 2");
        // The array loop overcounts the repeated starts.
        if (countOverArray(new int[] {1, 1, 2, 5, 5, 5, 9}) != 6) throw new AssertionError("array loop");
        // A repeated minimum value is a start too.
        if (countRuns(new int[] {Integer.MIN_VALUE, Integer.MIN_VALUE, Integer.MAX_VALUE}) != 2) throw new AssertionError("range ends");
        // Random arrays are checked against a sort-based oracle.
        Random rnd = new Random(58);
        for (int t = 0; t < 600; t++) {
            int[] a = new int[rnd.nextInt(12)];
            for (int k = 0; k < a.length; k++) a[k] = rnd.nextInt(14) - 4;
            int[] s = a.clone();
            Arrays.sort(s);
            int runs = 0;
            for (int k = 0; k < s.length; k++) if (k == 0 || s[k] > s[k - 1] + 1) runs++;
            if (countRuns(a) != runs) throw new AssertionError(Arrays.toString(a));
        }
    }
}
```

#### Solution: [Recognize] Generator Period (LeetCode 202)
<!-- id: hm-generator-period -->

**Approach.**
The next state depends only on the current state, so once a state repeats, the whole sequence repeats forever. The method stores each visited state in a set and stops when `add` reports a state that the set already holds. The size of the set is then the number of distinct states, including the seed. The invariant is that the set holds every state visited before the current one. The state space has 10000 values, so the loop runs at most 10001 times. The product `s * s` stays below `10^8`, so `int` arithmetic does not overflow.

**Complexity.**
- **Time** is O(1) in the input, because the loop visits at most 10000 distinct states, which is a constant bound.
- **Space** is O(1) in the input for the same reason, at most 10000 stored states.

```java run
import java.util.*;

public final class GeneratorPeriod {
    /**
     * Counts distinct states visited from seed until a state repeats.
     * Time: O(10000) worst case. Space: O(10000).
     * Invariant: seen holds every state visited before the current one.
     */
    static int distinctStates(int seed) {
        Set<Integer> seen = new HashSet<>();
        int s = seed;
        // add returns false at the first repeated state.
        while (seen.add(s)) {
            s = next(s);
        }
        return seen.size();
    }

    static int next(int s) {
        return (s * s / 100) % 10000;
    }

    public static void main(String[] args) {
        // The statement examples.
        if (distinctStates(0) != 1) throw new AssertionError("example 1");
        if (distinctStates(1234) != 57) throw new AssertionError("example 2");
        // The product stays inside int for every state.
        if (9999 * 9999 <= 0) throw new AssertionError("overflow");
        // Every seed is checked against a boolean-array oracle that tracks visited states.
        for (int seed = 0; seed <= 9999; seed++) {
            boolean[] visited = new boolean[10000];
            int s = seed, count = 0;
            while (!visited[s]) { visited[s] = true; count++; s = next(s); }
            if (distinctStates(seed) != count) throw new AssertionError("seed " + seed);
        }
    }
}
```
