<!-- solutions-for: 07-remainder-classes -->
### Remainder Classes

#### Solution: [Build] Subarray Sums Divisible by K (LeetCode 974)
<!-- id: ps-sums-divisible-k -->

**Approach.** The sum of a stretch is the difference of two running totals, and it is divisible by `k` exactly when the two totals leave the same remainder. Normalizing each running total with `Math.floorMod` gives a class from zero to `k - 1`, so an array of `k` counters is enough. At each position the answer grows by the counter of the current class, which is the number of earlier totals in that class, and then the counter is incremented. The counter of class zero starts at one, standing for the empty start. The oracle sums every stretch and tests divisibility.

**Complexity.** One pass, linear time, and an array of `k` counters.

```java run
import java.util.Random;

public final class SumsDivisibleK {
    static int subarraysDivByK(int[] nums, int k) {
        int[] seen = new int[k];
        seen[0] = 1;
        int total = 0, count = 0;
        for (int x : nums) {
            total += x;
            int cls = Math.floorMod(total, k);
            count += seen[cls];
            seen[cls]++;
        }
        return count;
    }
    static int oracle(int[] nums, int k) {
        int count = 0;
        for (int i = 0; i < nums.length; i++) {
            int s = 0;
            for (int j = i; j < nums.length; j++) {
                s += nums[j];
                if (s % k == 0) count++;
            }
        }
        return count;
    }

    public static void main(String[] args) {
        if (subarraysDivByK(new int[] {4, 5, 0, -2, -3, 1}, 5) != 7) throw new AssertionError("example 1");
        if (subarraysDivByK(new int[] {5}, 9) != 0) throw new AssertionError("example 2");
        if (subarraysDivByK(new int[] {9}, 9) != 1) throw new AssertionError("a single multiple");
        Random rnd = new Random(7601);
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(12);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(21) - 10;
            int k = 2 + rnd.nextInt(8);
            if (subarraysDivByK(a, k) != oracle(a, k)) throw new AssertionError("differs for k=" + k);
        }
    }
}
```

#### Solution: [Vary] Continuous Subarray Sum (LeetCode 523)
<!-- id: ps-continuous-subarray-sum -->

**Approach.** Two running totals in the same class enclose a stretch whose sum is a multiple of `k`, and the stretch has at least two numbers exactly when the indices of the two totals differ by at least two. The table keeps the first index of each class, so a repeated class is compared with the earliest possible partner, which gives the widest gap. Keeping the latest index instead could reject a valid pair. Class zero starts at index minus one, so the stretch beginning at the first number is considered, and a gap of exactly one is skipped without replacing the stored index. The total is a `long`, because the sum of many large values leaves the range of `int`. The oracle tests every stretch of at least two numbers.

**Complexity.** One pass, linear expected time, and a map with at most `k` entries.

```java run
import java.util.HashMap;
import java.util.Map;
import java.util.Random;

public final class ContinuousSubarraySum {
    static boolean checkSubarraySum(int[] nums, int k) {
        Map<Integer, Integer> firstAt = new HashMap<>();
        firstAt.put(0, -1);
        long total = 0;
        for (int i = 0; i < nums.length; i++) {
            total += nums[i];
            int cls = (int) Math.floorMod(total, (long) k);
            Integer earlier = firstAt.get(cls);
            if (earlier == null) firstAt.put(cls, i);
            else if (i - earlier >= 2) return true;
        }
        return false;
    }
    static boolean oracle(int[] nums, int k) {
        for (int i = 0; i < nums.length; i++) {
            long s = nums[i];
            for (int j = i + 1; j < nums.length; j++) {
                s += nums[j];
                if (s % k == 0) return true;
            }
        }
        return false;
    }

    public static void main(String[] args) {
        if (!checkSubarraySum(new int[] {23, 2, 4, 6, 7}, 6)) throw new AssertionError("example 1");
        if (checkSubarraySum(new int[] {23, 2, 6, 4, 7}, 13)) throw new AssertionError("example 2");
        if (!checkSubarraySum(new int[] {5, 0, 0}, 3)) throw new AssertionError("two zeros form a stretch");
        if (checkSubarraySum(new int[] {0}, 1)) throw new AssertionError("a single value is too short");
        if (!checkSubarraySum(new int[] {2000000000, 2000000000}, 2000000000)) throw new AssertionError("total beyond int");
        Random rnd = new Random(7602);
        for (int t = 0; t < 5000; t++) {
            int n = 1 + rnd.nextInt(9);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(12);
            int k = 1 + rnd.nextInt(9);
            if (checkSubarraySum(a, k) != oracle(a, k)) throw new AssertionError("differs for k=" + k + " on " + java.util.Arrays.toString(a));
        }
    }
}
```

#### Solution: [Boundary] Negative Values (Author exercise)
<!-- id: ps-negative-values -->

**Approach.** In Java, `%` takes the sign of the dividend, so a negative running total gives a negative remainder, and the same class reached from a positive total gets a different key. Used as an array index, a negative remainder throws; used as a map key, it splits one class into two and misses pairs. `Math.floorMod` always returns a value from zero to `k - 1` for a positive `k`, and the table is then correct. The running total is a `long` because the values go up to a billion. The program runs the normalized version against an oracle, shows that `%` gives -2 for the total -2 with `k` equal to 3, and shows that an array indexed with that remainder throws.

**Complexity.** One pass, linear time, and an array of `k` counters.

```java run
import java.util.Random;

public final class NegativeValues {
    static int count(int[] nums, int k) {
        int[] seen = new int[k];
        seen[0] = 1;
        long total = 0;
        int count = 0;
        for (int x : nums) {
            total += x;
            int cls = (int) Math.floorMod(total, (long) k);
            count += seen[cls];
            seen[cls]++;
        }
        return count;
    }
    static int withPercent(int[] nums, int k) {
        int[] seen = new int[k];
        seen[0] = 1;
        long total = 0;
        int count = 0;
        for (int x : nums) {
            total += x;
            int cls = (int) (total % k);
            count += seen[cls];
            seen[cls]++;
        }
        return count;
    }
    static int oracle(int[] nums, int k) {
        int count = 0;
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
        if (count(new int[] {-3, 1, 2, -4}, 3) != 3) throw new AssertionError("example 1");
        if (count(new int[] {-1, -1, 2}, 3) != 1) throw new AssertionError("example 2");
        if (-2 % 3 != -2 || Math.floorMod(-2, 3) != 1) throw new AssertionError("Java remainder rules");
        boolean threw = false;
        try { withPercent(new int[] {-3, 1, 2, -4}, 3); } catch (ArrayIndexOutOfBoundsException e) { threw = true; }
        if (!threw) throw new AssertionError("a negative remainder should fail as an index");
        Random rnd = new Random(7603);
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(12);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(2000000001) - 1000000000;
            int k = 2 + rnd.nextInt(9);
            if (count(a, k) != oracle(a, k)) throw new AssertionError("differs for k=" + k);
        }
    }
}
```

#### Solution: [Recognize] Longest Divisible Span (Author exercise)
<!-- id: ps-longest-divisible-span -->

**Approach.** The question asks for a length, so the table keeps the first index at which each class occurred, and a repeated class gives the candidate length as the difference of indices. Class zero starts at index minus one, so a stretch from the first number counts. Because `k` can be as large as a billion, an array of counters is not an option, and a map holds only the classes that occur. The total is a `long`, and the class is taken with `floorMod`. The oracle checks the sum of every stretch.

**Complexity.** One pass, linear expected time, and a map with at most n + 1 entries.

```java run
import java.util.HashMap;
import java.util.Map;
import java.util.Random;

public final class LongestDivisibleSpan {
    static int longestDivisibleSpan(int[] nums, int k) {
        Map<Integer, Integer> firstAt = new HashMap<>();
        firstAt.put(0, -1);
        long total = 0;
        int best = 0;
        for (int i = 0; i < nums.length; i++) {
            total += nums[i];
            int cls = (int) Math.floorMod(total, (long) k);
            Integer earlier = firstAt.get(cls);
            if (earlier == null) firstAt.put(cls, i);
            else best = Math.max(best, i - earlier);
        }
        return best;
    }
    static int oracle(int[] nums, int k) {
        int best = 0;
        for (int i = 0; i < nums.length; i++) {
            long s = 0;
            for (int j = i; j < nums.length; j++) {
                s += nums[j];
                if (s % k == 0) best = Math.max(best, j - i + 1);
            }
        }
        return best;
    }

    public static void main(String[] args) {
        if (longestDivisibleSpan(new int[] {3, 1, 4, 1, 5}, 5) != 3) throw new AssertionError("example 1");
        if (longestDivisibleSpan(new int[] {1, 2}, 5) != 0) throw new AssertionError("example 2");
        if (longestDivisibleSpan(new int[] {1000000000, 1000000000, 1000000000}, 1000000000) != 3) throw new AssertionError("large k");
        Random rnd = new Random(7604);
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(12);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(41) - 20;
            int k = 2 + rnd.nextInt(10);
            if (longestDivisibleSpan(a, k) != oracle(a, k)) throw new AssertionError("differs for k=" + k);
        }
    }
}
```
