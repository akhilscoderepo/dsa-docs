<!-- solutions-for: 04-hash-maps-and-sets -->
### Solutions For Remembered Positions

#### Solution: [Build] Two Sum (LeetCode 1)
<!-- id: hm-two-sum -->

**Approach.**
The loop computes the complement `target - nums[i]` and looks it up in a map from value to position before it stores `nums[i]`. A hit returns the stored position and `i`. The lookup comes first so that a value never pairs with its own position, and so that the array `[5, 5]` with target 10 finds two different 5s. The invariant states that before index `i` is processed, the map holds the values of `nums[0..i-1]`. The method therefore finds any pair that ends at `i` at that index. The harness asserts that the store-first variant breaks on `[5, 5]`, that `put` returns the previous value, and that the subtraction stays inside `int` for values within one billion.

**Complexity.**
- **Time** is O(n) on average, because the loop makes one lookup and one store of expected constant time per index.
- **Space** is O(n), because the map can hold one entry per value.

```java run
import java.util.*;

public final class TwoSumMap {
    /**
     * Returns the indexes of the one pair that adds to target.
     * Time: O(n) expected. Space: O(n).
     * Invariant: before index i, at maps each value of nums[0..i-1] to a position of that value.
     */
    static int[] twoSum(int[] nums, int target) {
        Map<Integer, Integer> at = new HashMap<>();
        // One iteration per position, so n iterations.
        for (int i = 0; i < nums.length; i++) {
            int complement = target - nums[i];
            // get returns null for a missing value, so the result is an Integer.
            Integer j = at.get(complement);
            if (j != null) {
                return new int[] {j, i};
            }
            // The store follows the lookup, so a value never pairs with itself.
            at.put(nums[i], i);
        }
        return new int[] {-1, -1};
    }

    /** The mistake: store first, then look up. */
    static int[] storeFirst(int[] nums, int target) {
        Map<Integer, Integer> at = new HashMap<>();
        for (int i = 0; i < nums.length; i++) {
            at.put(nums[i], i);
            Integer j = at.get(target - nums[i]);
            if (j != null) return new int[] {j, i};
        }
        return new int[] {-1, -1};
    }

    /** Lesson code: the pairwise method, kept as the oracle. */
    static int[] naive(int[] nums, int target) {
        for (int i = 0; i < nums.length; i++)
            for (int j = i + 1; j < nums.length; j++)
                if (nums[i] + nums[j] == target) return new int[] {i, j};
        return new int[] {-1, -1};
    }

    public static void main(String[] args) {
        // The statement examples and the lesson trace.
        if (!Arrays.equals(twoSum(new int[] {6, 2, 9, 4}, 10), new int[] {0, 3})) throw new AssertionError("example 1");
        if (!Arrays.equals(twoSum(new int[] {5, 5}, 10), new int[] {0, 1})) throw new AssertionError("example 2");
        if (!Arrays.equals(twoSum(new int[] {8, 2, 11, 3}, 14), new int[] {2, 3})) throw new AssertionError("lesson");
        // The store-first variant pairs a value with itself.
        if (!Arrays.equals(storeFirst(new int[] {5, 5}, 10), new int[] {0, 0})) throw new AssertionError("store first");
        // Java facts: put returns the previous value, and the subtraction wraps outside the stated range.
        Map<Integer, Integer> m = new HashMap<>();
        if (m.put(1, 10) != null || m.put(1, 20) != 10) throw new AssertionError("put return");
        if (Integer.MAX_VALUE - (-1) >= 0) throw new AssertionError("wrap");
        if (1_000_000_000 - (-1_000_000_000) != 2_000_000_000) throw new AssertionError("bounded range");
        // Random arrays with one planted pair are checked against the pairwise oracle on the first match.
        Random rnd = new Random(48);
        for (int t = 0; t < 600; t++) {
            int[] a = new int[2 + rnd.nextInt(8)];
            for (int k = 0; k < a.length; k++) a[k] = rnd.nextInt(21) - 10;
            int target = rnd.nextInt(21) - 10;
            int[] got = twoSum(a, target), want = naive(a, target);
            if (want[0] == -1 ? got[0] != -1 : a[got[0]] + a[got[1]] != target || got[0] >= got[1]) throw new AssertionError(Arrays.toString(a) + " " + target);
        }
    }
}
```

#### Solution: [Vary] Contains Duplicate II (LeetCode 219)
<!-- id: hm-nearby-duplicate -->

**Approach.**
The map stores, for each value, its most recent position. At index `i`, a stored position `p` for the same value gives the smallest gap `i - p` among all earlier equal values. One comparison with `k` then decides the pair. After the comparison, the entry is overwritten with `i`, because a later equal value is closer to `i` than to `p`. The invariant is that the map holds the latest position of every value in `nums[0..i-1]`. With `k = 0`, the gap of a repeat is at least 1, so the answer is false.

**Complexity.**
- **Time** is O(n) on average, because each index makes one lookup and one store.
- **Space** is O(n), because the map holds up to n distinct values.

```java run
import java.util.*;

public final class NearbyDuplicate {
    /**
     * Reports whether two equal values lie at most k positions apart.
     * Time: O(n) expected. Space: O(n).
     * Invariant: last holds the latest position of every value in nums[0..i-1].
     */
    static boolean nearbyDuplicate(int[] nums, int k) {
        Map<Integer, Integer> last = new HashMap<>();
        // One iteration per position.
        for (int i = 0; i < nums.length; i++) {
            Integer p = last.get(nums[i]);
            // The latest earlier position gives the smallest gap for this value.
            if (p != null && i - p <= k) {
                return true;
            }
            // Overwrite: later equal values are closer to the newest position.
            last.put(nums[i], i);
        }
        return false;
    }

    public static void main(String[] args) {
        // The statement examples, the lesson trace and the zero limit.
        if (nearbyDuplicate(new int[] {7, 2, 7}, 1)) throw new AssertionError("example 1");
        if (!nearbyDuplicate(new int[] {7, 2, 7}, 2)) throw new AssertionError("example 2");
        if (!nearbyDuplicate(new int[] {5, 1, 5, 5}, 1)) throw new AssertionError("lesson trace");
        if (nearbyDuplicate(new int[] {4, 4}, 0)) throw new AssertionError("k = 0");
        if (nearbyDuplicate(new int[0], 3)) throw new AssertionError("empty");
        // Random arrays are checked against a pairwise oracle.
        Random rnd = new Random(49);
        for (int t = 0; t < 600; t++) {
            int[] a = new int[rnd.nextInt(10)];
            for (int q = 0; q < a.length; q++) a[q] = rnd.nextInt(5);
            int k = rnd.nextInt(5);
            boolean expect = false;
            for (int i = 0; i < a.length; i++)
                for (int j = i + 1; j < a.length; j++)
                    if (a[i] == a[j] && j - i <= k) expect = true;
            if (nearbyDuplicate(a, k) != expect) throw new AssertionError(Arrays.toString(a) + " " + k);
        }
    }
}
```

#### Solution: [Boundary] First Index Wins (Author exercise)
<!-- id: hm-first-index-wins -->

**Approach.**
The build loop stores a value only when the map does not hold it yet, so each value keeps the smallest index. Each query then needs one lookup, and `getOrDefault(query, -1)` returns -1 for a value that does not occur. A build loop that always calls `put` would keep the largest index, which answers a different question. The invariant is that after index `i`, each value of `nums[0..i]` maps to its smallest index.

**Complexity.**
- **Time** is O(n + q) on average for n values and q queries, because the build and the queries each use expected constant-time operations.
- **Space** is O(d) for d distinct values of `nums`, plus the answer of length q.

```java run
import java.util.*;

public final class FirstIndexWins {
    /**
     * Answers each query with the smallest index of the value in nums, or -1.
     * Time: O(n + q) expected. Space: O(d) plus the answer.
     * Invariant: after index i, first maps each value of nums[0..i] to its smallest index.
     */
    static int[] firstIndexes(int[] nums, int[] queries) {
        Map<Integer, Integer> first = new HashMap<>();
        // putIfAbsent keeps the earliest position, because later equal values find the key present.
        for (int i = 0; i < nums.length; i++) {
            first.putIfAbsent(nums[i], i);
        }
        int[] out = new int[queries.length];
        // One lookup per query.
        for (int q = 0; q < queries.length; q++) {
            out[q] = first.getOrDefault(queries[q], -1);
        }
        return out;
    }

    /** The mistake: always overwrite, which keeps the last index. */
    static int[] lastIndexes(int[] nums, int[] queries) {
        Map<Integer, Integer> last = new HashMap<>();
        for (int i = 0; i < nums.length; i++) last.put(nums[i], i);
        int[] out = new int[queries.length];
        for (int q = 0; q < queries.length; q++) out[q] = last.getOrDefault(queries[q], -1);
        return out;
    }

    public static void main(String[] args) {
        // The statement examples.
        if (!Arrays.equals(firstIndexes(new int[] {4, 6, 4, 6, 6}, new int[] {6, 4, 9}), new int[] {1, 0, -1})) throw new AssertionError("example 1");
        if (!Arrays.equals(firstIndexes(new int[0], new int[] {3}), new int[] {-1})) throw new AssertionError("example 2");
        // Overwriting gives a different answer on the first example.
        if (!Arrays.equals(lastIndexes(new int[] {4, 6, 4, 6, 6}, new int[] {6, 4, 9}), new int[] {4, 2, -1})) throw new AssertionError("overwrite variant");
        // Random arrays are checked against indexOf-style scans.
        Random rnd = new Random(50);
        for (int t = 0; t < 500; t++) {
            int[] a = new int[rnd.nextInt(10)], q = new int[rnd.nextInt(6)];
            for (int k = 0; k < a.length; k++) a[k] = rnd.nextInt(6);
            for (int k = 0; k < q.length; k++) q[k] = rnd.nextInt(7);
            int[] got = firstIndexes(a, q);
            for (int k = 0; k < q.length; k++) {
                int want = -1;
                for (int i = a.length - 1; i >= 0; i--) if (a[i] == q[k]) want = i;
                if (got[k] != want) throw new AssertionError("trial " + t);
            }
        }
    }
}
```

#### Solution: [Recognize] Widest Equal-Value Pair (Author exercise)
<!-- id: hm-widest-pair -->

**Approach.**
For a fixed right index `j`, the widest pair uses the smallest earlier index of the same value, which is its first position. The map therefore stores the first position of each value and never overwrites it. At each index, a stored first position `p` gives the candidate `j - p`, and the answer is the largest candidate. The invariant is that the map holds the first position of every value in `nums[0..j-1]`, and `best` holds the widest gap among pairs that end before `j`.

**Complexity.**
- **Time** is O(n) on average, because each index does one lookup and at most one store.
- **Space** is O(d) for d distinct values.

```java run
import java.util.*;

public final class WidestPair {
    /**
     * Returns the largest j - i over equal pairs i < j, or 0.
     * Time: O(n) expected. Space: O(d).
     * Invariant: first holds the first position of every value in nums[0..j-1].
     */
    static int widestPair(int[] nums) {
        Map<Integer, Integer> first = new HashMap<>();
        int best = 0;
        // One iteration per index j.
        for (int j = 0; j < nums.length; j++) {
            Integer p = first.get(nums[j]);
            if (p == null) {
                // The first sighting is stored and never replaced.
                first.put(nums[j], j);
            } else {
                // The earliest position gives the widest gap for this right end.
                best = Math.max(best, j - p);
            }
        }
        return best;
    }

    public static void main(String[] args) {
        // The statement examples and the empty array.
        if (widestPair(new int[] {3, 1, 4, 1, 5, 3}) != 5) throw new AssertionError("example 1");
        if (widestPair(new int[] {1, 2, 3}) != 0) throw new AssertionError("example 2");
        if (widestPair(new int[0]) != 0) throw new AssertionError("empty");
        // Random arrays are checked against a pairwise oracle.
        Random rnd = new Random(51);
        for (int t = 0; t < 600; t++) {
            int[] a = new int[rnd.nextInt(10)];
            for (int k = 0; k < a.length; k++) a[k] = rnd.nextInt(6);
            int expect = 0;
            for (int i = 0; i < a.length; i++)
                for (int j = i + 1; j < a.length; j++)
                    if (a[i] == a[j]) expect = Math.max(expect, j - i);
            if (widestPair(a) != expect) throw new AssertionError(Arrays.toString(a));
        }
    }
}
```
