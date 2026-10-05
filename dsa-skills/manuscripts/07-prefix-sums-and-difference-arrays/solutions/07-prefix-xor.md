<!-- solutions-for: 07-prefix-sums-and-difference-arrays -->
### Solutions For Running XOR

#### Solution: [Build] XOR Queries Of A Subarray (LeetCode 1310)
<!-- id: ps-xor-half-open -->

**Approach.**
Entry `px[i]` of the stored array is the XOR of the first `i` values. One pass fills it from the rule `px[i + 1] = px[i] ^ arr[i]`, starting from `px[0] = 0`. A window that leaves out its end index covers `arr[start]` through `arr[end - 1]`, so its XOR is `px[end] ^ px[start]`. The first `start` values appear in both entries and cancel, because `x ^ x` is 0. An empty window reads one entry twice and returns 0 without a branch.

**Complexity.**
- **Time** is O(n + q), because the build costs n XOR operations and each query costs one.
- **Space** is O(n) for the array `px`.

```java run
import java.util.Arrays;
import java.util.Random;

public final class XorHalfOpen {
    /**
     * Returns the XOR of each window arr[start..end-1].
     * Time: O(n + q), one build and one XOR per query.
     * Space: O(n) for the prefix XOR array.
     * Invariant: px[i] is the XOR of the first i values, with px[0] = 0.
     */
    static int[] answer(int[] arr, int[][] queries) {
        int[] px = new int[arr.length + 1];
        // Each entry extends the previous XOR by one value.
        for (int i = 0; i < arr.length; i++) px[i + 1] = px[i] ^ arr[i];
        int[] out = new int[queries.length];
        for (int q = 0; q < queries.length; q++) {
            // The end index is excluded, so both indexes name entries of px directly.
            out[q] = px[queries[q][1]] ^ px[queries[q][0]];
        }
        return out;
    }

    public static void main(String[] args) {
        // The statement examples.
        if (!Arrays.equals(answer(new int[] {5, 1, 7, 2, 6}, new int[][] {{1, 4}, {0, 5}, {2, 2}}), new int[] {4, 7, 0})) throw new AssertionError("example 1");
        if (!Arrays.equals(answer(new int[] {9}, new int[][] {{0, 1}, {1, 1}}), new int[] {9, 0})) throw new AssertionError("example 2");
        // The properties that the approach uses.
        for (int x : new int[] {0, 1, 123456789, Integer.MAX_VALUE}) {
            if ((x ^ 0) != x || (x ^ x) != 0) throw new AssertionError("xor properties");
        }
        // The empty array accepts only the empty window.
        if (answer(new int[0], new int[][] {{0, 0}})[0] != 0) throw new AssertionError("empty array");
        // Random arrays against a loop over each window.
        Random rnd = new Random(25);
        for (int t = 0; t < 3000; t++) {
            int n = rnd.nextInt(10);
            int[] arr = rnd.ints(n, 0, 1_000_000_001).toArray();
            int s = rnd.nextInt(n + 1), e = s + rnd.nextInt(n - s + 1);
            int expect = 0;
            for (int i = s; i < e; i++) expect ^= arr[i];
            if (answer(arr, new int[][] {{s, e}})[0] != expect) throw new AssertionError("random");
        }
    }
}
```

#### Solution: [Vary] Count XOR K (Author exercise)
<!-- id: ps-count-xor-k -->

**Approach.**
A range from boundary `a` to boundary `b` has XOR `px[b] ^ px[a]`, and that equals `k` exactly when `px[a] = px[b] ^ k`. XOR with `k` twice returns the original value, so the rearrangement is valid. The loop keeps a frequency map of the prefix XOR values of earlier boundaries. At each step it adds the count under `cur ^ k` and then records `cur`. The map starts with 0 mapped to 1 for boundary 0. The count has type `long`, because up to `n * (n + 1) / 2` ranges can match.

**Complexity.**
- **Time** is O(n) expected, because each value costs one lookup and one update.
- **Space** is O(n) for the map.

```java run
import java.util.HashMap;
import java.util.Random;

public final class CountXorK {
    /**
     * Counts non-empty subarrays with XOR equal to k.
     * Time: O(n) expected, one hash lookup and one update per value.
     * Space: O(n) for the frequency map.
     * Invariant: on arrival at boundary b, seen holds the frequencies of px[0..b-1].
     */
    static long count(int[] arr, int k) {
        HashMap<Integer, Integer> seen = new HashMap<>();
        // The seed stands for boundary 0, whose prefix XOR is 0.
        seen.put(0, 1);
        int cur = 0;
        long count = 0;
        for (int v : arr) {
            cur ^= v;
            // The earlier prefix that pairs with cur has the value cur ^ k.
            count += seen.getOrDefault(cur ^ k, 0);
            // The record runs after the lookup, so the empty range is not counted.
            seen.merge(cur, 1, Integer::sum);
        }
        return count;
    }

    public static void main(String[] args) {
        // The statement examples.
        if (count(new int[] {4, 2, 2, 6, 4}, 6) != 4) throw new AssertionError("example 1");
        if (count(new int[] {3, 3, 3}, 3) != 4) throw new AssertionError("example 2");
        // A single value equal to k is counted through the seed.
        if (count(new int[] {5}, 5) != 1) throw new AssertionError("seed");
        // Random arrays against the double loop.
        Random rnd = new Random(26);
        for (int t = 0; t < 3000; t++) {
            int[] a = rnd.ints(1 + rnd.nextInt(12), 0, 8).toArray();
            int k = rnd.nextInt(8);
            long expect = 0;
            for (int i = 0; i < a.length; i++) {
                int x = 0;
                for (int j = i; j < a.length; j++) { x ^= a[j]; if (x == k) expect++; }
            }
            if (count(a, k) != expect) throw new AssertionError("random");
        }
    }
}
```

#### Solution: [Boundary] Empty Prefix (Author exercise)
<!-- id: ps-xor-empty-prefix -->

**Approach.**
A range has XOR 0 exactly when its two boundaries have equal prefix XOR values. The map stores the earliest index of each value, with 0 at index -1 for the empty prefix. That entry is the only partner for a range that starts at index 0, so without it the whole array would never match. A repeat at index `i` with stored index `p` gives a range of length `i - p`. The entry is never overwritten, so that length is the longest for its value.

**Complexity.**
- **Time** is O(n) expected, because each value costs one hash operation.
- **Space** is O(n) for the map of earliest indexes.

```java run
import java.util.HashMap;
import java.util.Random;

public final class XorEmptyPrefix {
    /**
     * Returns the length of the longest non-empty subarray with XOR 0, or 0.
     * Time: O(n) expected, one hash operation per value.
     * Space: O(n) for the map of earliest indexes.
     * Invariant: first.get(v) is the smallest index at which the prefix XOR was v.
     */
    static int longestZero(int[] arr) {
        HashMap<Integer, Integer> first = new HashMap<>();
        // Index -1 is the position before the first value, with prefix XOR 0.
        first.put(0, -1);
        int cur = 0, best = 0;
        for (int i = 0; i < arr.length; i++) {
            cur ^= arr[i];
            Integer p = first.get(cur);
            // A repeat measures the range from the earliest boundary with this value.
            if (p != null) best = Math.max(best, i - p);
            // A new value records its earliest index.
            else first.put(cur, i);
        }
        return best;
    }

    public static void main(String[] args) {
        // The statement examples.
        if (longestZero(new int[] {1, 2, 3}) != 3) throw new AssertionError("example 1");
        if (longestZero(new int[] {4, 5}) != 0) throw new AssertionError("example 2");
        // Random arrays against the double loop.
        Random rnd = new Random(27);
        for (int t = 0; t < 3000; t++) {
            int[] a = rnd.ints(1 + rnd.nextInt(12), 0, 8).toArray();
            int expect = 0;
            for (int i = 0; i < a.length; i++) {
                int x = 0;
                for (int j = i; j < a.length; j++) { x ^= a[j]; if (x == 0) expect = Math.max(expect, j - i + 1); }
            }
            if (longestZero(a) != expect) throw new AssertionError("random");
        }
    }
}
```

#### Solution: [Recognize] Count Triplets With Equal XOR (LeetCode 1442)
<!-- id: ps-triplets-1442 -->

**Approach.**
Let `a = XOR(arr[i..j-1])` and `b = XOR(arr[j..k])`. The two are equal exactly when `a ^ b = 0`, and `a ^ b` is the XOR of `arr[i..k]`. That range has XOR 0 exactly when `px[i] = px[k + 1]`. For every such pair `(i, k)` with `i < k`, each `j` from `i + 1` to `k` gives a valid triplet, so the pair adds `k - i` triplets. The loop tests every pair of boundaries, which suits the limit of 300 values.

**Complexity.**
- **Time** is O(n^2), because the loops test every pair of boundaries once.
- **Space** is O(n) for the prefix XOR array.

```java run
import java.util.Random;

public final class Triplets1442 {
    /**
     * Counts triplets (i, j, k) with XOR(arr[i..j-1]) == XOR(arr[j..k]).
     * Time: O(n^2), one test per pair of boundaries.
     * Space: O(n) for the prefix XOR array.
     * Invariant: px[i] == px[k + 1] exactly when XOR(arr[i..k]) is 0.
     */
    static int count(int[] arr) {
        int n = arr.length;
        int[] px = new int[n + 1];
        for (int i = 0; i < n; i++) px[i + 1] = px[i] ^ arr[i];
        int count = 0;
        // Each pair of boundaries (i, k + 1) is tested once.
        for (int i = 0; i < n; i++) {
            for (int k = i + 1; k < n; k++) {
                // Equal prefix values mean the range i..k has XOR 0.
                if (px[i] == px[k + 1]) {
                    // Every split point j in i + 1..k gives one triplet.
                    count += k - i;
                }
            }
        }
        return count;
    }

    public static void main(String[] args) {
        // The statement examples.
        if (count(new int[] {5, 1, 4, 0, 4, 1}) != 11) throw new AssertionError("example 1");
        if (count(new int[] {9, 9, 9}) != 2) throw new AssertionError("example 2");
        // A pair has no zero-XOR range of length at least 2 unless both values match.
        if (count(new int[] {3, 7}) != 0) throw new AssertionError("pair");
        // Random arrays against the triple loop.
        Random rnd = new Random(28);
        for (int t = 0; t < 2000; t++) {
            int[] a = rnd.ints(1 + rnd.nextInt(9), 1, 6).toArray();
            int expect = 0;
            for (int i = 0; i < a.length; i++)
                for (int j = i + 1; j < a.length; j++)
                    for (int k = j; k < a.length; k++) {
                        int l = 0, r = 0;
                        for (int x = i; x < j; x++) l ^= a[x];
                        for (int x = j; x <= k; x++) r ^= a[x];
                        if (l == r) expect++;
                    }
            if (count(a) != expect) throw new AssertionError("random");
        }
    }
}
```
