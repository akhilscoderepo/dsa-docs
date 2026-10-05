<!-- solutions-for: 07-prefix-sums-and-difference-arrays -->
### Solutions For Remainder Classes

#### Solution: [Build] Subarray Sums Divisible By K (LeetCode 974)
<!-- id: ps-divisible-974 -->

**Approach.**
A subarray sum is `prefix[b] - prefix[a]`, which is divisible by `k` exactly when both prefixes lie in the same remainder class. The loop converts each prefix to its class with `Math.floorMod`, so negative prefixes land in the range 0 to `k - 1`. It adds the number of earlier boundaries in that class and then records the current boundary. The array of counts starts with class 0 set to 1 for boundary 0. The invariant is that on arrival at boundary `b`, `freq[r]` counts the earlier boundaries in class `r`.

**Complexity.**
- **Time** is O(n), because each value costs one `floorMod`, one read and one write.
- **Space** is O(k) for the array of counts.

```java run
import java.util.Random;

public final class Divisible974 {
    /**
     * Counts non-empty subarrays with sum divisible by k.
     * Time: O(n), constant work per value.
     * Space: O(k) for the class counts.
     * Invariant: on arrival at boundary b, freq[r] counts boundaries a < b in class r.
     */
    static int count(int[] nums, int k) {
        int[] freq = new int[k];
        // Boundary 0 has prefix 0, which is in class 0.
        freq[0] = 1;
        long cur = 0;
        int count = 0;
        for (int v : nums) {
            cur += v;
            // floorMod keeps negative prefixes inside 0..k-1.
            int cls = (int) Math.floorMod(cur, (long) k);
            // Each earlier boundary in the same class closes a divisible subarray.
            count += freq[cls];
            // The record runs after the lookup.
            freq[cls]++;
        }
        return count;
    }

    public static void main(String[] args) {
        // The statement examples.
        if (count(new int[] {3, -1, 2, 4, -6, 1}, 4) != 5) throw new AssertionError("example 1");
        if (count(new int[] {5}, 9) != 0) throw new AssertionError("example 2");
        // The Java claim: % keeps the sign of the left operand, floorMod does not.
        if (-3 % 5 != -3) throw new AssertionError("raw remainder");
        if (Math.floorMod(-3, 5) != 2) throw new AssertionError("floorMod");
        // Random arrays with negative values against the double loop.
        Random rnd = new Random(21);
        for (int t = 0; t < 3000; t++) {
            int[] a = rnd.ints(1 + rnd.nextInt(12), -9, 10).toArray();
            int k = 2 + rnd.nextInt(6);
            int expect = 0;
            for (int i = 0; i < a.length; i++) {
                int s = 0;
                for (int j = i; j < a.length; j++) { s += a[j]; if (s % k == 0) expect++; }
            }
            if (count(a, k) != expect) throw new AssertionError("random");
        }
    }
}
```

#### Solution: [Vary] Continuous Subarray Sum (LeetCode 523)
<!-- id: ps-continuous-523 -->

**Approach.**
The loop stores the earliest index for each remainder class, with class 0 at index -1. When a class repeats at index `i`, the span from the stored index `p` has length `i - p`. The method returns true when that length is at least 2. It never overwrites an entry, so the stored index is the earliest and gives the longest span for that class. A repeat that gives length 1 is ignored, and the loop continues. The divisor can reach 2^31 - 1, so a hash map replaces the array, and the prefix is a `long`.

**Complexity.**
- **Time** is O(n) expected, because each value costs one hash operation.
- **Space** is O(min(n, k)) for the map, because it holds at most one entry per class and per boundary.

```java run
import java.util.HashMap;
import java.util.Random;

public final class Continuous523 {
    /**
     * Returns true when some subarray of length at least 2 has a sum that is a multiple of k.
     * Time: O(n) expected, one hash operation per value.
     * Space: O(min(n, k)) for the map of earliest indexes.
     * Invariant: first.get(c) is the smallest index at which the prefix class was c.
     */
    static boolean check(int[] nums, int k) {
        HashMap<Long, Integer> first = new HashMap<>();
        // Index -1 is the position before the first value, with prefix 0 in class 0.
        first.put(0L, -1);
        long cur = 0;
        for (int i = 0; i < nums.length; i++) {
            cur += nums[i];
            long cls = Math.floorMod(cur, (long) k);
            Integer p = first.get(cls);
            // A repeat at distance 2 or more gives a long enough subarray.
            if (p != null) {
                if (i - p >= 2) return true;
            } else {
                // A new class records its earliest index.
                first.put(cls, i);
            }
        }
        return false;
    }

    public static void main(String[] args) {
        // The statement examples.
        if (!check(new int[] {5, 0, 0}, 6)) throw new AssertionError("example 1");
        if (check(new int[] {1, 2, 3}, 7)) throw new AssertionError("example 2");
        // A single multiple of k is too short.
        if (check(new int[] {6}, 6)) throw new AssertionError("length rule");
        // A divisor above the int range of sums still works with long prefixes.
        if (!check(new int[] {2_000_000_000, 147_483_647}, Integer.MAX_VALUE)) throw new AssertionError("large k");
        // Random arrays against the double loop.
        Random rnd = new Random(22);
        for (int t = 0; t < 3000; t++) {
            int[] a = rnd.ints(1 + rnd.nextInt(10), 0, 10).toArray();
            int k = 1 + rnd.nextInt(8);
            boolean expect = false;
            for (int i = 0; i < a.length; i++) {
                long s = a[i];
                for (int j = i + 1; j < a.length; j++) { s += a[j]; if (s % k == 0) expect = true; }
            }
            if (check(a, k) != expect) throw new AssertionError("random");
        }
    }
}
```

#### Solution: [Boundary] Negative Values (Author exercise)
<!-- id: ps-negative-remainders -->

**Approach.**
The method keeps a `long` running sum and stores `Math.floorMod(sum, k)` after each value. The first entry is 0 for the empty prefix. The call returns a value from 0 to `k - 1` for positive `k`, so negative sums map to the class of the equal remainder, for example -3 with `k = 5` gives 2. The raw operator `%` would return -3 and break the range. The cast to `int` is safe, because the result is below `k`, which is at most 10^9.

**Complexity.**
- **Time** is O(n), because each value costs one addition and one `floorMod`.
- **Space** is O(n) for the returned array.

```java run
import java.util.Arrays;
import java.util.Random;

public final class NegativeRemainders {
    /**
     * Returns the class number of every prefix sum, with the empty prefix first.
     * Time: O(n), constant work per value.
     * Space: O(n) for the result.
     * Invariant: out[i] equals floorMod of the sum of the first i values.
     */
    static int[] classes(int[] nums, int k) {
        int[] out = new int[nums.length + 1];
        long cur = 0;
        for (int i = 0; i < nums.length; i++) {
            cur += nums[i];
            // floorMod maps the sum to 0..k-1, whatever its sign.
            out[i + 1] = (int) Math.floorMod(cur, (long) k);
        }
        return out;
    }

    public static void main(String[] args) {
        // The statement examples.
        if (!Arrays.equals(classes(new int[] {-3, -2}, 5), new int[] {0, 2, 0})) throw new AssertionError("example 1");
        if (!Arrays.equals(classes(new int[] {7, -8, 1}, 3), new int[] {0, 1, 2, 0})) throw new AssertionError("example 2");
        // The raw operator gives a negative class for the prefix -1 and k = 3.
        if (-1 % 3 != -1 || Math.floorMod(-1, 3) != 2) throw new AssertionError("operator difference");
        // The empty array has only the empty prefix.
        if (!Arrays.equals(classes(new int[0], 4), new int[] {0})) throw new AssertionError("empty");
        // Random arrays: every entry is in range and matches a BigInteger remainder.
        Random rnd = new Random(23);
        for (int t = 0; t < 2000; t++) {
            int[] a = rnd.ints(rnd.nextInt(10), -1_000_000_000, 1_000_000_000).toArray();
            int k = 1 + rnd.nextInt(1_000_000_000);
            int[] got = classes(a, k);
            java.math.BigInteger sum = java.math.BigInteger.ZERO;
            for (int i = 0; i < a.length; i++) {
                sum = sum.add(java.math.BigInteger.valueOf(a[i]));
                int expect = sum.mod(java.math.BigInteger.valueOf(k)).intValue();
                if (got[i + 1] != expect || got[i + 1] < 0 || got[i + 1] >= k) throw new AssertionError("random");
            }
        }
    }
}
```

#### Solution: [Recognize] Longest Divisible Span (Author exercise)
<!-- id: ps-divisible-span -->

**Approach.**
A span is divisible when its two boundaries share a class, and the longest span for a class starts at its earliest boundary. The map stores the first index per class, with class 0 at index -1. At each index the loop computes the class with `Math.floorMod`, measures `i - first` on a repeat and stores the index on a miss. The map value is a position and not a count, which is the change from the counting version. The prefix is a `long`, and the divisor can reach 10^9.

**Complexity.**
- **Time** is O(n) expected, because each value costs one hash operation.
- **Space** is O(min(n, k)) for the map.

```java run
import java.util.HashMap;
import java.util.Random;

public final class DivisibleSpan {
    /**
     * Returns the length of the longest subarray with sum divisible by k, or 0.
     * Time: O(n) expected, one hash operation per value.
     * Space: O(min(n, k)) for the map of earliest indexes.
     * Invariant: first.get(c) is the smallest index at which the prefix class was c.
     */
    static int longest(int[] nums, int k) {
        HashMap<Long, Integer> first = new HashMap<>();
        first.put(0L, -1);
        long cur = 0;
        int best = 0;
        for (int i = 0; i < nums.length; i++) {
            cur += nums[i];
            long cls = Math.floorMod(cur, (long) k);
            Integer p = first.get(cls);
            // A repeat measures the span from the earliest boundary in the class.
            if (p != null) best = Math.max(best, i - p);
            // A new class records its earliest index.
            else first.put(cls, i);
        }
        return best;
    }

    public static void main(String[] args) {
        // The statement examples.
        if (longest(new int[] {2, -2, 5}, 5) != 3) throw new AssertionError("example 1");
        if (longest(new int[] {1, 2, 3}, 4) != 0) throw new AssertionError("example 2");
        // Random arrays with negative values against the double loop.
        Random rnd = new Random(24);
        for (int t = 0; t < 3000; t++) {
            int[] a = rnd.ints(1 + rnd.nextInt(12), -9, 10).toArray();
            int k = 1 + rnd.nextInt(7);
            int expect = 0;
            for (int i = 0; i < a.length; i++) {
                long s = 0;
                for (int j = i; j < a.length; j++) { s += a[j]; if (s % k == 0) expect = Math.max(expect, j - i + 1); }
            }
            if (longest(a, k) != expect) throw new AssertionError("random");
        }
    }
}
```
