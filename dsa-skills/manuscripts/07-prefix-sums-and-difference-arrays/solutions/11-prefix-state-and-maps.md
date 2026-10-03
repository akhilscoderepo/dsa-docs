<!-- solutions-for: 07-prefix-state-and-maps -->
### Prefix State And Maps

#### Solution: [Build] Subarray Sum Equals K (LeetCode 560)
<!-- id: ps-combo-subarray-sum-long -->

**Approach.** The running total is a `long`, since a hundred thousand entries near a billion pass the range of `int`, and the map is keyed by `Long`. The map is seeded with `0L`, the key of the empty prefix, so a stretch starting at the first entry is counted. For each entry the total is updated, the paired key `total - k` is looked up, the count found is added to the answer, and then the current total is recorded. A lookup with an `int` such as `get(0)` boxes an `Integer`, which never equals a stored `Long`, so it returns `null`, and the program asserts exactly that. The oracle tries every first and last entry with a `long` net change.

**Complexity.** One pass, linear expected time, and space proportional to the number of distinct totals.

```java run
import java.util.HashMap;
import java.util.Map;
import java.util.Random;

public final class ComboSubarraySumLong {
    static long subarraySum(int[] nums, long k) {
        Map<Long, Integer> seen = new HashMap<>();
        seen.put(0L, 1);
        long balance = 0, count = 0;
        for (int x : nums) {
            balance += x;
            count += seen.getOrDefault(balance - k, 0);
            seen.merge(balance, 1, Integer::sum);
        }
        return count;
    }
    static long oracle(int[] nums, long k) {
        long count = 0;
        for (int i = 0; i < nums.length; i++) {
            long net = 0;
            for (int j = i; j < nums.length; j++) {
                net += nums[j];
                if (net == k) count++;
            }
        }
        return count;
    }

    public static void main(String[] args) {
        if (subarraySum(new int[] {1000000000, 1000000000, -1000000000}, 1000000000L) != 3) throw new AssertionError("example 1");
        if (subarraySum(new int[] {5, -5, 5}, 0L) != 2) throw new AssertionError("example 2");
        Map<Long, Integer> probe = new HashMap<>();
        probe.put(0L, 1);
        if (probe.get(0) != null) throw new AssertionError("an Integer key never matches a Long key");
        if (probe.get(0L) == null) throw new AssertionError("a Long key matches");
        Random rnd = new Random(8101);
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(10);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = (rnd.nextInt(5) - 2) * 1000000000;
            long k = (rnd.nextInt(7) - 3) * 1000000000L;
            if (subarraySum(a, k) != oracle(a, k)) throw new AssertionError("differs for k=" + k);
        }
    }
}
```

#### Solution: [Vary] Contiguous Array (LeetCode 525)
<!-- id: ps-combo-contiguous-array-span -->

**Approach.** Each zero counts as minus one and each one as plus one, giving a running balance, and equal balances at two positions enclose a stretch with equal numbers of both. A table of the first index of each balance, seeded with zero at index minus one, gives the widest stretch ending at the current position. The best stretch is replaced only when a candidate is strictly longer. Scanning left to right with strict comparison keeps the earliest end among equal lengths, and equal lengths with earlier ends have earlier starts. The stretch starts one position after the stored index. The oracle examines every stretch and keeps the first longest one in order of start.

**Complexity.** One pass, linear expected time, and space proportional to the number of distinct balances.

```java run
import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;
import java.util.Random;

public final class ComboContiguousArraySpan {
    static int[] longestBalancedSpan(int[] nums) {
        Map<Integer, Integer> first = new HashMap<>();
        first.put(0, -1);
        int balance = 0, bestLen = 0, bestStart = -1, bestEnd = -1;
        for (int i = 0; i < nums.length; i++) {
            balance += nums[i] == 1 ? 1 : -1;
            Integer earlier = first.get(balance);
            if (earlier == null) first.put(balance, i);
            else if (i - earlier > bestLen) {
                bestLen = i - earlier;
                bestStart = earlier + 1;
                bestEnd = i;
            }
        }
        return new int[] {bestStart, bestEnd};
    }
    static int[] oracle(int[] nums) {
        int bestLen = 0, bestStart = -1, bestEnd = -1;
        for (int i = 0; i < nums.length; i++) {
            int bal = 0;
            for (int j = i; j < nums.length; j++) {
                bal += nums[j] == 1 ? 1 : -1;
                if (bal == 0 && j - i + 1 > bestLen) { bestLen = j - i + 1; bestStart = i; bestEnd = j; }
            }
        }
        return new int[] {bestStart, bestEnd};
    }

    public static void main(String[] args) {
        if (!Arrays.equals(longestBalancedSpan(new int[] {0, 1, 0, 0, 1, 1, 0}), new int[] {0, 5})) throw new AssertionError("example 1");
        if (!Arrays.equals(longestBalancedSpan(new int[] {1, 1, 1}), new int[] {-1, -1})) throw new AssertionError("example 2");
        Random rnd = new Random(8102);
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(12);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(2);
            int[] got = longestBalancedSpan(a), want = oracle(a);
            if (got[1] - got[0] != want[1] - want[0]) throw new AssertionError("length differs on " + Arrays.toString(a));
            if (got[0] != want[0] && got[0] != -1) {
                throw new AssertionError("start differs on " + Arrays.toString(a));
            }
        }
    }
}
```

#### Solution: [Boundary] Subarray Sums Divisible by K (LeetCode 974)
<!-- id: ps-combo-divisible-large-k -->

**Approach.** A modulus of up to a billion rules out an array of `k` counters, so the counts live in a map from the normalized remainder to the number of earlier prefixes with that remainder, seeded with remainder zero once. For each entry the running total, held in a `long`, is reduced with `Math.floorMod`, the count already stored under that remainder is added to the answer, and then it is incremented. The answer is a `long`, because a hundred thousand zeros with any modulus give a hundred thousand and one equal remainders and about five billion pairs, which cannot be held in an `int`. The oracle tests the sum of every stretch with `long` arithmetic.

**Complexity.** One pass, linear expected time, and a map with at most n + 1 entries.

```java run
import java.util.HashMap;
import java.util.Map;
import java.util.Random;

public final class ComboDivisibleLargeK {
    static long divisibleStretches(int[] nums, int k) {
        Map<Integer, Integer> seen = new HashMap<>();
        seen.put(0, 1);
        long total = 0, count = 0;
        for (int x : nums) {
            total += x;
            int cls = (int) Math.floorMod(total, (long) k);
            count += seen.getOrDefault(cls, 0);
            seen.merge(cls, 1, Integer::sum);
        }
        return count;
    }
    static long oracle(int[] nums, int k) {
        long count = 0;
        for (int i = 0; i < nums.length; i++) {
            long s = 0;
            for (int j = i; j < nums.length; j++) {
                s += nums[j];
                if (s % k == 0) count++;
            }
        }
        return count;
    }

    public static void main(String[] args) {
        if (divisibleStretches(new int[] {4, 5, 0, -2, -3, 1}, 5) != 7) throw new AssertionError("example 1");
        if (divisibleStretches(new int[100000], 1000000000) != 5000050000L) throw new AssertionError("example 2");
        if (5000050000L <= Integer.MAX_VALUE) throw new AssertionError("the count must not fit in an int");
        Random rnd = new Random(8103);
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(12);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(2000000001) - 1000000000;
            int k = rnd.nextBoolean() ? 1 + rnd.nextInt(10) : 1 + rnd.nextInt(1000000000);
            if (divisibleStretches(a, k) != oracle(a, k)) throw new AssertionError("differs for k=" + k);
        }
    }
}
```

#### Solution: [Recognize] Continuous Subarray Sum (LeetCode 523)
<!-- id: ps-combo-continuous-pair -->

**Approach.** A stretch of at least two numbers has a sum divisible by `k` exactly when two prefix totals with the same remainder lie at least two positions apart. The table keeps the first index of each remainder, seeded with zero at index minus one, and a repeated remainder with a gap of at least two ends the scan. The first such position is the smallest possible end, because positions are visited in increasing order. For that end, the stored first index is the smallest start, and the stretch begins one position after it. A gap of exactly one is skipped, and the stored index is not replaced. The oracle tries every stretch in order of end and then start.

**Complexity.** One pass, linear expected time, and a map with at most `k` entries.

```java run
import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;
import java.util.Random;

public final class ComboContinuousPair {
    static int[] earliestGoodPair(int[] nums, int k) {
        Map<Integer, Integer> first = new HashMap<>();
        first.put(0, -1);
        long total = 0;
        for (int i = 0; i < nums.length; i++) {
            total += nums[i];
            int cls = (int) Math.floorMod(total, (long) k);
            Integer earlier = first.get(cls);
            if (earlier == null) first.put(cls, i);
            else if (i - earlier >= 2) return new int[] {earlier + 1, i};
        }
        return new int[] {-1, -1};
    }
    static int[] oracle(int[] nums, int k) {
        for (int end = 1; end < nums.length; end++) {
            for (int start = 0; start < end; start++) {
                long s = 0;
                for (int t = start; t <= end; t++) s += nums[t];
                if (s % k == 0) return new int[] {start, end};
            }
        }
        return new int[] {-1, -1};
    }

    public static void main(String[] args) {
        if (!Arrays.equals(earliestGoodPair(new int[] {23, 2, 4, 6, 7}, 6), new int[] {1, 2})) throw new AssertionError("example 1");
        if (!Arrays.equals(earliestGoodPair(new int[] {23, 2, 6, 4, 7}, 13), new int[] {-1, -1})) throw new AssertionError("example 2");
        if (!Arrays.equals(earliestGoodPair(new int[] {0, 0}, 5), new int[] {0, 1})) throw new AssertionError("two zeros");
        Random rnd = new Random(8104);
        for (int t = 0; t < 5000; t++) {
            int n = 1 + rnd.nextInt(9);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(15);
            int k = 1 + rnd.nextInt(9);
            int[] got = earliestGoodPair(a, k), want = oracle(a, k);
            if (got[1] != want[1]) throw new AssertionError("end differs for k=" + k + " on " + Arrays.toString(a));
            if (got[0] < 0 != want[0] < 0) throw new AssertionError("presence differs");
            if (got[0] >= 0) {
                long s = 0;
                for (int q = got[0]; q <= got[1]; q++) s += a[q];
                if (s % k != 0 || got[1] - got[0] < 1) throw new AssertionError("reported stretch is not valid");
            }
        }
    }
}
```
