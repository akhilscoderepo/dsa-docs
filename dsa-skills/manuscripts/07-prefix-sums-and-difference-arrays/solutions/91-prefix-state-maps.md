<!-- solutions-for: 07-prefix-sums-and-difference-arrays -->
### Solutions For Prefix State And Maps

#### Solution: [Build] Subarray Sum Equals K (LeetCode 560)
<!-- id: psm-ending-counts -->

**Approach.**
A window that ends at index `i` and has sum `k` pairs the boundary after `i` with an earlier boundary whose total is `cur - k`. The frequency map holds the totals of the earlier boundaries, so the lookup of `cur - k` returns the number of such windows at once. The loop stores that number at `out[i]` and then records `cur`. The map starts with the total 0 mapped to 1 for boundary 0, so windows that begin at index 0 are found. Reading before recording keeps the empty window out of the count.

**Complexity.**
- **Time** is O(n) expected, because each value costs one lookup and one update in a hash map.
- **Space** is O(n) for the map and the output.

```java run
import java.util.Arrays;
import java.util.HashMap;
import java.util.Random;

public final class EndingCounts {
    /**
     * Returns out[i] = the number of subarrays ending at index i with sum k.
     * Time: O(n) expected, one lookup and one update per value.
     * Space: O(n) for the frequency map and the output.
     * Invariant: at index i, seen holds the totals of boundaries 0..i with their counts.
     */
    static int[] endingCounts(int[] nums, int k) {
        HashMap<Long, Integer> seen = new HashMap<>();
        // The seed is boundary 0 with the empty total.
        seen.put(0L, 1);
        int[] out = new int[nums.length];
        long cur = 0;
        for (int i = 0; i < nums.length; i++) {
            cur += nums[i];
            // The partner total cur - k gives the windows that end here.
            out[i] = seen.getOrDefault(cur - k, 0);
            // The record follows the lookup, so a window is never empty.
            seen.merge(cur, 1, Integer::sum);
        }
        return out;
    }

    public static void main(String[] args) {
        // The statement examples.
        if (!Arrays.equals(endingCounts(new int[] {3, 1, 0, 4, -4, 4}, 4), new int[] {0, 1, 1, 2, 1, 3})) throw new AssertionError("example 1");
        if (!Arrays.equals(endingCounts(new int[] {1, 1, 1}, 2), new int[] {0, 1, 1})) throw new AssertionError("example 2");
        // Random arrays against the double loop, per end index.
        Random rnd = new Random(41);
        for (int t = 0; t < 3000; t++) {
            int[] a = rnd.ints(1 + rnd.nextInt(10), -4, 5).toArray();
            int k = rnd.nextInt(9) - 4;
            int[] got = endingCounts(a, k);
            for (int end = 0; end < a.length; end++) {
                int c = 0, s = 0;
                for (int start = end; start >= 0; start--) { s += a[start]; if (s == k) c++; }
                if (got[end] != c) throw new AssertionError("random");
            }
        }
    }
}
```

#### Solution: [Vary] Contiguous Array (LeetCode 525)
<!-- id: psm-three-kinds -->

**Approach.**
Let `d1` be the count of 1 minus the count of 0 in the prefix, and `d2` the count of 2 minus the count of 0. A window has equal counts of all three values exactly when both differences have the same value at its two boundaries. The pair `(d1, d2)` is the boundary state. Both parts lie between `-n` and `n`, so the pair encodes into one `long` as `(d1 + n) * (2n + 1) + (d2 + n)`. The earliest-index map stores the first position of each pair, starting with the pair `(0, 0)` at index -1, and a repeat gives the longest window for that end.

**Complexity.**
- **Time** is O(n) expected, because each value costs one hash lookup and at most one insert.
- **Space** is O(n) for the map.

```java run
import java.util.HashMap;
import java.util.Random;

public final class ThreeKinds {
    /**
     * Returns the longest subarray with equal counts of 0, 1 and 2.
     * Time: O(n) expected, one hash operation per value.
     * Space: O(n) for the map of earliest indexes.
     * Invariant: first.get(key) is the smallest index at which the pair (d1, d2) was seen.
     */
    static int longest(int[] nums) {
        int n = nums.length;
        HashMap<Long, Integer> first = new HashMap<>();
        // The pair (0, 0) encodes to n * (2n + 1) + n and stands for the empty prefix at index -1.
        first.put((long) n * (2L * n + 1) + n, -1);
        int d1 = 0, d2 = 0, best = 0;
        for (int i = 0; i < n; i++) {
            // A one raises d1, a two raises d2, and a zero lowers both differences.
            if (nums[i] == 0) { d1--; d2--; }
            else if (nums[i] == 1) d1++;
            else d2++;
            // Each part lies in [-n, n], so the encoding is unique.
            long key = (long) (d1 + n) * (2L * n + 1) + (d2 + n);
            Integer p = first.get(key);
            // A repeat measures the window from the earliest boundary with the same pair.
            if (p != null) best = Math.max(best, i - p);
            else first.put(key, i);
        }
        return best;
    }

    public static void main(String[] args) {
        // The statement examples.
        if (longest(new int[] {0, 0, 1, 2, 1, 0}) != 3) throw new AssertionError("example 1");
        if (longest(new int[] {2, 2}) != 0) throw new AssertionError("example 2");
        // Random arrays against the double loop.
        Random rnd = new Random(42);
        for (int t = 0; t < 3000; t++) {
            int[] a = rnd.ints(1 + rnd.nextInt(14), 0, 3).toArray();
            int expect = 0;
            for (int i = 0; i < a.length; i++) {
                int[] c = new int[3];
                for (int j = i; j < a.length; j++) {
                    c[a[j]]++;
                    if (c[0] == c[1] && c[1] == c[2]) expect = Math.max(expect, j - i + 1);
                }
            }
            if (longest(a) != expect) throw new AssertionError("random");
        }
    }
}
```

#### Solution: [Boundary] Subarray Sums Divisible By K (LeetCode 974)
<!-- id: psm-target-remainder -->

**Approach.**
A window from boundary `a` to boundary `b` leaves remainder `r` when `prefix[b] - prefix[a] ≡ r (mod k)`. That is the same as `prefix[a] ≡ prefix[b] - r (mod k)`. The state of a boundary is `Math.floorMod(cur, k)`, and its partner class is `Math.floorMod(cur - r, k)`. The call normalizes both the negative totals and the shift by `r`, so the keys lie between 0 and `k - 1`. An array of counts indexed by class replaces the map, and boundary 0 starts class 0 with count 1. The count has type `long`, because up to `n * (n + 1) / 2` windows can match.

**Complexity.**
- **Time** is O(n), because each value costs two `floorMod` calls and one array update.
- **Space** is O(k) for the array of counts.

```java run
import java.util.Random;

public final class TargetRemainder {
    /**
     * Counts non-empty subarrays whose sum leaves remainder r modulo k.
     * Time: O(n), constant work per value.
     * Space: O(k) for the class counts.
     * Invariant: at each boundary, freq[c] counts earlier boundaries whose total is in class c.
     */
    static long count(int[] nums, int k, int r) {
        long[] freq = new long[k];
        // Boundary 0 has total 0, which is in class 0.
        freq[0] = 1;
        long cur = 0, count = 0;
        for (int v : nums) {
            cur += v;
            // The partner class is the class of cur - r, normalized into 0..k-1.
            int partner = (int) Math.floorMod(cur - r, (long) k);
            count += freq[partner];
            // The record uses the class of cur itself and follows the lookup.
            freq[(int) Math.floorMod(cur, (long) k)]++;
        }
        return count;
    }

    public static void main(String[] args) {
        // The statement examples.
        if (count(new int[] {3, -1, 2, 4, -6, 1}, 4, 1) != 4) throw new AssertionError("example 1");
        if (count(new int[] {5}, 3, -1) != 1) throw new AssertionError("example 2");
        // With r = 0 the count matches the divisible-sum count.
        if (count(new int[] {3, -1, 2, 4, -6, 1}, 4, 0) != 5) throw new AssertionError("r zero");
        // Random arrays with negative values and unnormalized r against the double loop.
        Random rnd = new Random(43);
        for (int t = 0; t < 3000; t++) {
            int[] a = rnd.ints(1 + rnd.nextInt(10), -9, 10).toArray();
            int k = 2 + rnd.nextInt(6), r = rnd.nextInt(41) - 20;
            long expect = 0;
            for (int i = 0; i < a.length; i++) {
                long s = 0;
                for (int j = i; j < a.length; j++) { s += a[j]; if (Math.floorMod(s - r, k) == 0) expect++; }
            }
            if (count(a, k, r) != expect) throw new AssertionError("random");
        }
    }
}
```

#### Solution: [Recognize] Continuous Subarray Sum (LeetCode 523)
<!-- id: psm-min-length -->

**Approach.**
The earliest-index map stores the first boundary of each remainder class, with class 0 at index -1. At index `i` the current class either repeats or is new. A repeat with stored index `p` gives a window of length `i - p`. That window is the longest one for this end and this class. The method returns true when its length is at least `minLen`. A shorter repeat does not end the search, because a later end can reach a longer window from the same stored index. A new class records its index. The prefix is a `long` and uses `Math.floorMod` for negative totals.

**Complexity.**
- **Time** is O(n) expected, because each value costs one hash operation.
- **Space** is O(min(n, k)) for the map.

```java run
import java.util.HashMap;
import java.util.Random;

public final class MinLength {
    /**
     * Returns true when some subarray of length at least minLen has a sum divisible by k.
     * Time: O(n) expected, one hash operation per value.
     * Space: O(min(n, k)) for the map of earliest indexes.
     * Invariant: first.get(c) is the smallest index at which the prefix class was c.
     */
    static boolean check(int[] nums, int k, int minLen) {
        HashMap<Long, Integer> first = new HashMap<>();
        // Index -1 is the empty prefix, which is in class 0.
        first.put(0L, -1);
        long cur = 0;
        for (int i = 0; i < nums.length; i++) {
            cur += nums[i];
            long cls = Math.floorMod(cur, (long) k);
            Integer p = first.get(cls);
            if (p != null) {
                // The earliest boundary gives the longest window, so a failed length rules out this index only.
                if (i - p >= minLen) return true;
            } else {
                first.put(cls, i);
            }
        }
        return false;
    }

    public static void main(String[] args) {
        // The statement examples.
        if (check(new int[] {5, 0, 0}, 6, 3)) throw new AssertionError("example 1");
        if (!check(new int[] {4, 2, 6, 0, 1}, 6, 4)) throw new AssertionError("example 2");
        // A shorter minimum accepts the first example.
        if (!check(new int[] {5, 0, 0}, 6, 2)) throw new AssertionError("min length 2");
        // Random arrays with negative values against the double loop.
        Random rnd = new Random(44);
        for (int t = 0; t < 3000; t++) {
            int[] a = rnd.ints(1 + rnd.nextInt(10), -9, 10).toArray();
            int k = 1 + rnd.nextInt(7), minLen = 1 + rnd.nextInt(a.length);
            boolean expect = false;
            for (int i = 0; i < a.length; i++) {
                long s = 0;
                for (int j = i; j < a.length; j++) { s += a[j]; if (j - i + 1 >= minLen && s % k == 0) expect = true; }
            }
            if (check(a, k, minLen) != expect) throw new AssertionError("random");
        }
    }
}
```
