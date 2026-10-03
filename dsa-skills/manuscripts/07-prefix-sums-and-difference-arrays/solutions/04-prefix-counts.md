<!-- solutions-for: 07-prefix-counts -->
### Prefix Counts

#### Solution: [Build] Subarray Sum Equals K (LeetCode 560)
<!-- id: ps-subarray-sum-k -->

**Approach.** A stretch ending at the current day has total `k` exactly when the balance before its first day equals the current balance minus `k`. A map from balance to the number of days that ended with it answers how many such starting points exist. The map starts with balance zero seen once, which stands for the moment before the first day. For each value, the balance is updated, the complement is looked up and added to the count, and only then is the current balance recorded, so a day is never paired with itself. The oracle tries every first and last day.

**Complexity.** A single scan with constant expected cost per value, so linear expected time, and space proportional to the number of distinct balances.

```java run
import java.util.HashMap;
import java.util.Map;
import java.util.Random;

public final class SubarraySumK {
    static int subarraySum(int[] nums, int k) {
        Map<Integer, Integer> seen = new HashMap<>();
        seen.put(0, 1);
        int balance = 0, count = 0;
        for (int x : nums) {
            balance += x;
            count += seen.getOrDefault(balance - k, 0);
            seen.merge(balance, 1, Integer::sum);
        }
        return count;
    }
    static int oracle(int[] nums, int k) {
        int count = 0;
        for (int i = 0; i < nums.length; i++) {
            int s = 0;
            for (int j = i; j < nums.length; j++) {
                s += nums[j];
                if (s == k) count++;
            }
        }
        return count;
    }

    public static void main(String[] args) {
        if (subarraySum(new int[] {3, 4, 7, 2, -3, 1, 4, 2}, 7) != 4) throw new AssertionError("example 1");
        if (subarraySum(new int[] {1, -1, 0}, 0) != 3) throw new AssertionError("example 2");
        if (subarraySum(new int[] {5}, 5) != 1) throw new AssertionError("the seeded zero counts a stretch from the start");
        Random rnd = new Random(7401);
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(12);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(9) - 4;
            int k = rnd.nextInt(11) - 5;
            if (subarraySum(a, k) != oracle(a, k)) throw new AssertionError("differs for k=" + k);
        }
    }
}
```

#### Solution: [Vary] Binary Subarrays With Sum (LeetCode 930)
<!-- id: ps-binary-subarrays-sum -->

**Approach.** The running total of a zero-and-one array never exceeds the length, so an array of counts indexed by the balance replaces the map, with slot zero starting at one. The complement `balance - goal` is negative while the balance is below the goal, and then no earlier balance can match, so the lookup is skipped by a guard instead of reading a negative index. After the lookup the balance is recorded. The oracle checks every stretch directly.

**Complexity.** One pass, linear time, and an array of n + 1 counts.

```java run
import java.util.Random;

public final class BinarySubarraysSum {
    static int numSubarrays(int[] nums, int goal) {
        int[] seen = new int[nums.length + 1];
        seen[0] = 1;
        int balance = 0, count = 0;
        for (int x : nums) {
            balance += x;
            if (balance >= goal) count += seen[balance - goal];
            seen[balance]++;
        }
        return count;
    }
    static int oracle(int[] nums, int goal) {
        int count = 0;
        for (int i = 0; i < nums.length; i++) {
            int s = 0;
            for (int j = i; j < nums.length; j++) {
                s += nums[j];
                if (s == goal) count++;
            }
        }
        return count;
    }

    public static void main(String[] args) {
        if (numSubarrays(new int[] {1, 0, 1, 0, 1}, 2) != 4) throw new AssertionError("example 1");
        if (numSubarrays(new int[] {0, 0, 0, 0, 0}, 0) != 15) throw new AssertionError("example 2");
        if (numSubarrays(new int[] {1}, 2) != 0) throw new AssertionError("goal above any total");
        Random rnd = new Random(7402);
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(14);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(2);
            int goal = rnd.nextInt(n + 1);
            if (numSubarrays(a, goal) != oracle(a, goal)) throw new AssertionError("differs for goal=" + goal);
        }
    }
}
```

#### Solution: [Boundary] Zero Target (Author exercise)
<!-- id: ps-zero-target -->

**Approach.** With a target of zero, the complement equals the balance, so a stretch has total zero exactly when two equal balances enclose it. If a balance has occurred c times before, then c different stretches end on the current day, which is why the table must count occurrences and not merely record them. The lookup comes before the record, so the current balance is not paired with itself, and the seeded zero accounts for stretches starting at the first day. The set version, which can only say that some earlier balance matched, adds at most one per day, and the program shows that it differs on the two examples and always gives a result no larger than the true count.

**Complexity.** One pass, linear expected time, and space proportional to the number of distinct balances.

```java run
import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Random;
import java.util.Set;

public final class ZeroTarget {
    static int zeroSumStretches(int[] nums) {
        Map<Integer, Integer> seen = new HashMap<>();
        seen.put(0, 1);
        int balance = 0, count = 0;
        for (int x : nums) {
            balance += x;
            count += seen.getOrDefault(balance, 0);
            seen.merge(balance, 1, Integer::sum);
        }
        return count;
    }
    static int withASet(int[] nums) {
        Set<Integer> seen = new HashSet<>();
        seen.add(0);
        int balance = 0, count = 0;
        for (int x : nums) {
            balance += x;
            if (seen.contains(balance)) count++;
            seen.add(balance);
        }
        return count;
    }
    static int oracle(int[] nums) {
        int count = 0;
        for (int i = 0; i < nums.length; i++) {
            int s = 0;
            for (int j = i; j < nums.length; j++) {
                s += nums[j];
                if (s == 0) count++;
            }
        }
        return count;
    }

    public static void main(String[] args) {
        if (zeroSumStretches(new int[] {0, 0, 0}) != 6) throw new AssertionError("example 1");
        if (zeroSumStretches(new int[] {2, -2, 2, -2}) != 4) throw new AssertionError("example 2");
        if (withASet(new int[] {0, 0, 0}) == 6) throw new AssertionError("a set should undercount the first example");
        if (withASet(new int[] {2, -2, 2, -2}) == 4) throw new AssertionError("a set should undercount the second example");
        Random rnd = new Random(7403);
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(12);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(5) - 2;
            int want = oracle(a);
            if (zeroSumStretches(a) != want) throw new AssertionError("count differs");
            if (withASet(a) > want) throw new AssertionError("a set can never exceed the true count");
        }
    }
}
```

#### Solution: [Recognize] Count Number of Nice Subarrays (LeetCode 1248)
<!-- id: ps-nice-subarrays -->

**Approach.** Replacing every value by its parity, one for odd and zero for even, turns the question into counting stretches whose sum equals `k`, which is the binary case of the previous exercises. The running total is the number of odd values seen so far, and it cannot exceed the length, so an array of counts indexed by it works. For each position, add the number of earlier totals equal to the current total minus `k`, then record the current total. The oracle counts the odd values in each stretch directly.

**Complexity.** One pass, linear time, and an array of n + 1 counts.

```java run
import java.util.Random;

public final class NiceSubarrays {
    static int numberOfSubarrays(int[] nums, int k) {
        int[] seen = new int[nums.length + 1];
        seen[0] = 1;
        int odds = 0, count = 0;
        for (int x : nums) {
            odds += x & 1;
            if (odds >= k) count += seen[odds - k];
            seen[odds]++;
        }
        return count;
    }
    static int oracle(int[] nums, int k) {
        int count = 0;
        for (int i = 0; i < nums.length; i++) {
            int odds = 0;
            for (int j = i; j < nums.length; j++) {
                if (nums[j] % 2 != 0) odds++;
                if (odds == k) count++;
            }
        }
        return count;
    }

    public static void main(String[] args) {
        if (numberOfSubarrays(new int[] {1, 1, 2, 1, 1}, 3) != 2) throw new AssertionError("example 1");
        if (numberOfSubarrays(new int[] {2, 4, 6}, 1) != 0) throw new AssertionError("example 2");
        if (numberOfSubarrays(new int[] {2, 2, 2, 1, 2, 2, 1, 2, 2, 2}, 2) != 16) throw new AssertionError("evens around two odds");
        Random rnd = new Random(7404);
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(14);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = 1 + rnd.nextInt(9);
            int k = 1 + rnd.nextInt(n);
            if (numberOfSubarrays(a, k) != oracle(a, k)) throw new AssertionError("differs for k=" + k);
        }
    }
}
```
