<!-- solutions-for: 07-prefix-sums-and-difference-arrays -->
### Solutions For Counting With A Frequency Map

#### Solution: [Build] Subarray Sum Equals K (LeetCode 560)
<!-- id: ps-subarray-sum-560 -->

**Approach.**
A subarray from boundary `a` to boundary `b` has sum `prefix[b] - prefix[a]`, so it equals `k` exactly when `prefix[a] = prefix[b] - k`. The loop keeps the running prefix and a frequency map of the prefix values of earlier boundaries. At each step it adds the count stored under `cur - k` and only then records `cur`. The map starts with the seed 0 mapped to 1, which stands for boundary 0 and lets subarrays that begin at index 0 match. The invariant is that, before the lookup at boundary `b`, the map holds the frequencies of `prefix[0..b-1]`.

**Complexity.**
- **Time** is O(n) expected, because each value costs one lookup and one update in a hash map.
- **Space** is O(n), because the map holds at most n + 1 distinct prefix values.

```java run
import java.util.HashMap;
import java.util.Random;

public final class SubarraySum560 {
    /**
     * Counts non-empty subarrays with sum k.
     * Time: O(n) expected, one hash lookup and one update per value.
     * Space: O(n) for the frequency map.
     * Invariant: before the lookup at boundary b, seen holds the frequencies of prefix[0..b-1].
     */
    static int count(int[] nums, int k) {
        HashMap<Long, Integer> seen = new HashMap<>();
        // The seed stands for boundary 0, whose prefix is the empty sum.
        seen.put(0L, 1);
        long cur = 0;
        int count = 0;
        for (int v : nums) {
            // The prefix extends by one value.
            cur += v;
            // The lookup counts earlier boundaries with prefix cur - k, and it runs before the record.
            count += seen.getOrDefault(cur - k, 0);
            // The record adds the current boundary for later positions.
            seen.merge(cur, 1, Integer::sum);
        }
        return count;
    }

    public static void main(String[] args) {
        // The statement examples.
        if (count(new int[] {3, 4, 7, 2, -3, 1, 4, 2}, 7) != 4) throw new AssertionError("example 1");
        if (count(new int[] {1, 2, 3}, 3) != 2) throw new AssertionError("example 2");
        // Without the seed, subarrays that start at index 0 would be missed.
        if (count(new int[] {5}, 5) != 1) throw new AssertionError("seed");
        // Random arrays against the double loop.
        Random rnd = new Random(13);
        for (int t = 0; t < 3000; t++) {
            int[] a = rnd.ints(1 + rnd.nextInt(10), -4, 5).toArray();
            int k = rnd.nextInt(9) - 4;
            int expect = 0;
            for (int i = 0; i < a.length; i++) {
                int s = 0;
                for (int j = i; j < a.length; j++) { s += a[j]; if (s == k) expect++; }
            }
            if (count(a, k) != expect) throw new AssertionError("random");
        }
    }
}
```

#### Solution: [Vary] Binary Subarrays With Sum (LeetCode 930)
<!-- id: ps-binary-subarrays-930 -->

**Approach.**
The method is the same count with a different value domain. The prefix sum never decreases, because every value is 0 or 1, so a zero repeats the previous prefix and raises that key's count. An array can then have many boundaries with one prefix value, and each of them is a valid start for a later end. Since the prefix takes at most `n + 1` values, a plain `int` array of counts replaces the hash map. The index `cur - goal` is read only when it is not negative.

**Complexity.**
- **Time** is O(n), because each value costs one array read and one array write.
- **Space** is O(n) for the array of counts.

```java run
import java.util.Random;

public final class BinarySubarrays930 {
    /**
     * Counts non-empty subarrays of a binary array with sum goal.
     * Time: O(n), one array lookup and one update per value.
     * Space: O(n) for the count array indexed by prefix value.
     * Invariant: before the lookup at boundary b, freq[p] counts earlier boundaries with prefix p.
     */
    static int count(int[] nums, int goal) {
        // The prefix is between 0 and n, so an array indexed by prefix replaces the map.
        int[] freq = new int[nums.length + 1];
        // The seed counts boundary 0 with prefix 0.
        freq[0] = 1;
        int cur = 0, count = 0;
        for (int v : nums) {
            cur += v;
            // A negative key can never match, so the lookup is guarded.
            if (cur - goal >= 0) count += freq[cur - goal];
            // Record the current boundary after the lookup.
            freq[cur]++;
        }
        return count;
    }

    public static void main(String[] args) {
        // The statement examples.
        if (count(new int[] {0, 1, 1, 0, 1}, 2) != 5) throw new AssertionError("example 1");
        if (count(new int[] {0, 0, 1, 0, 0}, 1) != 9) throw new AssertionError("example 2");
        // A goal of zero counts every run of zeros.
        if (count(new int[] {0, 0, 0, 0, 0}, 0) != 15) throw new AssertionError("zeros");
        // Random binary arrays against the double loop.
        Random rnd = new Random(14);
        for (int t = 0; t < 3000; t++) {
            int[] a = rnd.ints(1 + rnd.nextInt(12), 0, 2).toArray();
            int goal = rnd.nextInt(a.length + 1);
            int expect = 0;
            for (int i = 0; i < a.length; i++) {
                int s = 0;
                for (int j = i; j < a.length; j++) { s += a[j]; if (s == goal) expect++; }
            }
            if (count(a, goal) != expect) throw new AssertionError("random");
        }
    }
}
```

#### Solution: [Boundary] Zero Target (Author exercise)
<!-- id: ps-zero-target -->

**Approach.**
A subarray has sum 0 exactly when its two boundaries have equal prefix values. If a value occurred `m` times before the current boundary, then `m` subarrays end here, so the answer adds the stored count and not 1. A set would add at most 1 per step and undercount. The lookup must run before the record. A lookup after the record would match each boundary with itself and count `n` empty subarrays. The count uses `long`, because `n = 10^5` gives up to 5,000,050,000 candidate pairs.

**Complexity.**
- **Time** is O(n) expected, because each value costs one lookup and one update.
- **Space** is O(n) for the frequency map.

```java run
import java.util.HashMap;
import java.util.HashSet;
import java.util.Random;

public final class ZeroTarget {
    /**
     * Counts non-empty subarrays with sum 0.
     * Time: O(n) expected, one hash operation pair per value.
     * Space: O(n) for the frequency map.
     * Invariant: before the lookup at boundary b, seen holds the frequencies of prefix[0..b-1].
     */
    static long count(int[] nums) {
        HashMap<Long, Integer> seen = new HashMap<>();
        // The seed counts boundary 0.
        seen.put(0L, 1);
        long cur = 0, count = 0;
        for (int v : nums) {
            cur += v;
            // Each earlier boundary with the same prefix starts a zero-sum subarray here.
            count += seen.getOrDefault(cur, 0);
            // Record after the lookup, so a boundary never pairs with itself.
            seen.merge(cur, 1, Integer::sum);
        }
        return count;
    }

    /** The wrong version: a set remembers only presence. */
    static long countWithSet(int[] nums) {
        HashSet<Long> seen = new HashSet<>();
        seen.add(0L);
        long cur = 0, count = 0;
        for (int v : nums) {
            cur += v;
            if (seen.contains(cur)) count++;
            seen.add(cur);
        }
        return count;
    }

    public static void main(String[] args) {
        // The statement examples.
        if (count(new int[] {1, -1, 1, -1}) != 4) throw new AssertionError("example 1");
        if (count(new int[] {2, 3}) != 0) throw new AssertionError("example 2");
        // The set version undercounts on repeated prefixes, which is the claim of the lesson.
        if (countWithSet(new int[] {1, -1, 1, -1}) == 4) throw new AssertionError("set should undercount");
        // The count passes the int range for 100,000 zeros: n * (n + 1) / 2.
        long big = count(new int[100_000]);
        if (big != 100_000L * 100_001L / 2) throw new AssertionError("large count");
        // Random arrays against the double loop.
        Random rnd = new Random(15);
        for (int t = 0; t < 3000; t++) {
            int[] a = rnd.ints(1 + rnd.nextInt(12), -2, 3).toArray();
            long expect = 0;
            for (int i = 0; i < a.length; i++) {
                long s = 0;
                for (int j = i; j < a.length; j++) { s += a[j]; if (s == 0) expect++; }
            }
            if (count(a) != expect) throw new AssertionError("random");
        }
    }
}
```

#### Solution: [Recognize] Count Number Of Nice Subarrays (LeetCode 1248)
<!-- id: ps-nice-subarrays-1248 -->

**Approach.**
A conversion maps each value to `v & 1`, which is 1 for an odd value and 0 for an even one. The sum of a subarray of converted values equals its number of odd values, so the task becomes counting subarrays with sum `k`. The count of odd values before each position is a prefix that grows by at most 1, so an array of counts indexed by that prefix is enough. The seed counts boundary 0.

**Complexity.**
- **Time** is O(n), because each value costs one conversion, one lookup and one update.
- **Space** is O(n) for the array of counts.

```java run
import java.util.Random;

public final class NiceSubarrays1248 {
    /**
     * Counts subarrays with exactly k odd values.
     * Time: O(n), one array lookup and one update per value.
     * Space: O(n) for the count array indexed by the number of odd values so far.
     * Invariant: before the lookup at boundary b, freq[p] counts earlier boundaries with p odd values before them.
     */
    static long count(int[] nums, int k) {
        long[] freq = new long[nums.length + 1];
        // The seed counts boundary 0 with zero odd values before it.
        freq[0] = 1;
        int odds = 0;
        long count = 0;
        for (int v : nums) {
            // The conversion adds 1 for an odd value and 0 otherwise.
            odds += v & 1;
            // Earlier boundaries with odds - k odd values start a window with exactly k.
            if (odds - k >= 0) count += freq[odds - k];
            freq[odds]++;
        }
        return count;
    }

    public static void main(String[] args) {
        // The statement examples.
        if (count(new int[] {2, 1, 2, 2, 1, 2, 1}, 2) != 7) throw new AssertionError("example 1");
        if (count(new int[] {1, 3, 5}, 2) != 2) throw new AssertionError("example 2");
        // Random arrays against the double loop.
        Random rnd = new Random(16);
        for (int t = 0; t < 3000; t++) {
            int[] a = rnd.ints(1 + rnd.nextInt(12), 1, 10).toArray();
            int k = 1 + rnd.nextInt(a.length);
            long expect = 0;
            for (int i = 0; i < a.length; i++) {
                int odd = 0;
                for (int j = i; j < a.length; j++) { odd += a[j] % 2; if (odd == k) expect++; }
            }
            if (count(a, k) != expect) throw new AssertionError("random");
        }
    }
}
```
