<!-- solutions-for: 27-dynamic-programming-capacity-and-partition-patterns -->
### Solutions For Target Sum

#### Solution: [Build] Derive The Subset Equation (Author exercise)
<!-- id: cap-tgt-derive-equation -->

**Approach.**
Let P be the sum of the elements with a plus sign and N the sum of those with a minus sign. A target is reached when P - N = target, and the total satisfies P + N = total. Adding the two equations gives 2P = total + target. So the plus group must sum to `(total + target) / 2`, and that value must be a whole number between 0 and `total`.

The method checks the range first, with `|target| <= total`, because that test also guarantees `total + target >= 0`. It then checks that `total + target` is even and returns the half. The total is a `long`, so large inputs cannot overflow. No table is needed, and the invariant is the pair of equations that tie P and N to the total and the target.

**Complexity.**
- **Time** is O(n), because the method sums the elements once.
- **Space** is O(1), and the input array stays unchanged.

```java run
import java.util.*;

public final class CapTgtDeriveEquation {
    /**
     * Returns the required plus-group sum, or -1 when no assignment can reach target.
     * Time: O(n). Space: O(1).
     * Invariant: P + N = total and P - N = target, so P = (total + target) / 2.
     */
    static long plusGroupSum(int[] nums, int target) {
        long total = 0;
        for (int x : nums) total += x;
        // Range test first: it also makes total + target nonnegative for the parity test.
        if (Math.abs((long) target) > total) return -1;
        // An odd total + target has no whole-number half.
        if ((total + target) % 2 != 0) return -1;
        return (total + target) / 2;
    }

    /** Oracle: tries every sign assignment and reports the plus-group sum of the first match. */
    static long oracle(int[] nums, int target) {
        int n = nums.length;
        for (int mask = 0; mask < (1 << n); mask++) {
            int signed = 0, plus = 0;
            for (int i = 0; i < n; i++) {
                if ((mask >> i & 1) == 1) { signed += nums[i]; plus += nums[i]; }
                else signed -= nums[i];
            }
            if (signed == target) return plus;
        }
        return -1;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (plusGroupSum(new int[] {1, 2, 3, 4}, 2) != 6) throw new AssertionError("ex1");
        if (plusGroupSum(new int[] {2, 3}, 2) != -1) throw new AssertionError("ex2");
        // A target beyond the total is rejected by the range test, in both signs.
        if (plusGroupSum(new int[] {1, 2}, 4) != -1 || plusGroupSum(new int[] {1, 2}, -4) != -1) throw new AssertionError("range");
        // The empty array has total 0, so only target 0 passes and its plus group is 0.
        if (plusGroupSum(new int[] {}, 0) != 0 || plusGroupSum(new int[] {}, 2) != -1) throw new AssertionError("empty");
        // Java fact: % keeps the sign of the left side, so a negative odd number gives -1.
        if ((-3) % 2 != -1) throw new AssertionError("negative remainder");
        // Random inputs: a valid derived sum exists exactly when some assignment reaches the target.
        Random rnd = new Random(2714);
        for (int t = 0; t < 3000; t++) {
            int[] a = new int[rnd.nextInt(9)];
            for (int i = 0; i < a.length; i++) a[i] = rnd.nextInt(8);
            int target = rnd.nextInt(41) - 20;
            boolean reachable = oracle(a, target) != -1;
            long got = plusGroupSum(a, target);
            // The derived sum is necessary, and when an assignment exists its plus group has that sum.
            if (reachable && got != oracle(a, target)) throw new AssertionError("sum " + t);
            if (!reachable && got != -1) {
                // A valid derived sum without an assignment is allowed: the derivation is necessary, not sufficient.
                if (got < 0) throw new AssertionError("negative " + t);
            }
        }
    }
}
```

#### Solution: [Vary] Count Derived Subsets (Author exercise)
<!-- id: cap-tgt-count-subsets -->

**Approach.**
The table `ways[s]` counts the subsets of the processed elements whose sum is `s`. The table starts with `ways[0]` equal to 1 for the empty subset. For each element `x`, the loop visits sums from the goal down to `x` and adds `ways[s - x]` to `ways[s]`. The descending order makes `ways[s - x]` describe the elements before `x`, so each element joins a subset at most once.

At every point, `ways[s]` counts the subsets of the processed elements that sum to `s`. The answer is `ways[goal]`. The counts are `long` values, and the base entry is 1 because the empty subset is a subset.

**Complexity.**
- **Time** is O(n * goal), because each element updates up to `goal` entries.
- **Space** is O(goal) for the count array, and the input array stays unchanged.

```java run
import java.util.*;

public final class CapTgtCountSubsets {
    /**
     * Returns how many index subsets of nums sum to exactly goal.
     * Time: O(n * goal). Space: O(goal).
     * Invariant: ways[s] counts subsets of the processed elements that sum to s.
     */
    static long countSubsets(int[] nums, int goal) {
        long[] ways = new long[goal + 1];
        // The empty subset is one subset with sum 0.
        ways[0] = 1;
        for (int x : nums) {
            // Descending sums keep ways[s - x] at the state before x.
            for (int s = goal; s >= x; s--) {
                ways[s] += ways[s - x];
            }
        }
        return ways[goal];
    }

    /** Oracle: tests every subset. */
    static long oracle(int[] nums, int goal) {
        long count = 0;
        for (int mask = 0; mask < (1 << nums.length); mask++) {
            int sum = 0;
            for (int i = 0; i < nums.length; i++) if ((mask >> i & 1) == 1) sum += nums[i];
            if (sum == goal) count++;
        }
        return count;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (countSubsets(new int[] {1, 2, 3, 4, 5}, 5) != 3) throw new AssertionError("ex1");
        if (countSubsets(new int[] {2, 2, 2}, 4) != 3) throw new AssertionError("ex2");
        // Goal 0 counts the empty subset only, and an empty array has one subset.
        if (countSubsets(new int[] {1, 2}, 0) != 1 || countSubsets(new int[] {}, 0) != 1) throw new AssertionError("empty subset");
        // Equal elements count by index: ten equal ones give 252 subsets of size five.
        int[] ones = new int[10];
        Arrays.fill(ones, 1);
        if (countSubsets(ones, 5) != 252) throw new AssertionError("by index");
        // The input array stays unchanged.
        int[] nums = {3, 1, 2};
        int[] copy = nums.clone();
        countSubsets(nums, 3);
        if (!Arrays.equals(nums, copy)) throw new AssertionError("mutated");
        // Random inputs against the subset oracle.
        Random rnd = new Random(2715);
        for (int t = 0; t < 3000; t++) {
            int[] a = new int[rnd.nextInt(12)];
            for (int i = 0; i < a.length; i++) a[i] = 1 + rnd.nextInt(9);
            int goal = rnd.nextInt(40);
            if (countSubsets(a, goal) != oracle(a, goal)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Boundary] Zero Values And Parity (Author exercise)
<!-- id: cap-tgt-zeros-and-parity -->

**Approach.**
A zero can take either sign without changing the signed sum, so every zero doubles the number of assignments. The method counts the zeros, sets them aside, and solves the problem for the positive elements. It then multiplies the result by 2 for each zero, using `1L << zeros`. At most 60 elements keep the shift below 63 bits, so the product stays a `long`.

For the positive elements, the method sums them into `total` and rejects the target if `|target| > total` or if `total + target` is odd. Otherwise it counts the subsets whose sum is `(total + target) / 2` with the descending count table. The invariant is that after each element, `ways[s]` counts the subsets of the processed positive elements with sum `s`. An empty array with target 0 gives total 0, goal 0 and one subset, so the result is 1.

**Complexity.**
- **Time** is O(n * goal), because each positive element updates up to `goal` entries.
- **Space** is O(goal) for the count array, and the input array stays unchanged.

```java run
import java.util.*;

public final class CapTgtZerosAndParity {
    /**
     * Returns the number of sign assignments with signed sum target, with zeros allowed.
     * Time: O(n * goal). Space: O(goal).
     * Invariant: ways[s] counts subsets of the processed positive elements that sum to s.
     */
    static long countWithZeros(int[] nums, int target) {
        long total = 0;
        int zeros = 0;
        for (int x : nums) {
            total += x;
            if (x == 0) zeros++;
        }
        // Range test first, then parity, so the parity test never sees a negative number.
        if (Math.abs((long) target) > total || (total + target) % 2 != 0) return 0;
        int goal = (int) ((total + target) / 2);
        long[] ways = new long[goal + 1];
        ways[0] = 1;
        for (int x : nums) {
            // Zeros are set aside and counted by the multiplier below.
            if (x == 0) continue;
            for (int s = goal; s >= x; s--) ways[s] += ways[s - x];
        }
        // Each zero can take either sign, so the count doubles per zero.
        return ways[goal] * (1L << zeros);
    }

    /** Oracle: tries every sign assignment. */
    static long oracle(int[] nums, int target) {
        long count = 0;
        for (int mask = 0; mask < (1 << nums.length); mask++) {
            int sum = 0;
            for (int i = 0; i < nums.length; i++) sum += (mask >> i & 1) == 1 ? nums[i] : -nums[i];
            if (sum == target) count++;
        }
        return count;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (countWithZeros(new int[] {0, 0, 1}, 1) != 4) throw new AssertionError("ex1");
        if (countWithZeros(new int[] {1, 2}, 0) != 0) throw new AssertionError("ex2");
        // An empty array with target 0 has one assignment, and the same array with target 1 has none.
        if (countWithZeros(new int[] {}, 0) != 1 || countWithZeros(new int[] {}, 1) != 0) throw new AssertionError("empty");
        // Sixty zeros give 2^60 assignments, which still fits in a long.
        int[] zeros = new int[60];
        if (countWithZeros(zeros, 0) != (1L << 60)) throw new AssertionError("sixty zeros");
        // The input array stays unchanged.
        int[] nums = {0, 3, 0, 1};
        int[] copy = nums.clone();
        countWithZeros(nums, 2);
        if (!Arrays.equals(nums, copy)) throw new AssertionError("mutated");
        // Random inputs with many zeros against the assignment oracle.
        Random rnd = new Random(2716);
        for (int t = 0; t < 3000; t++) {
            int[] a = new int[rnd.nextInt(11)];
            for (int i = 0; i < a.length; i++) a[i] = rnd.nextInt(3) == 0 ? 0 : rnd.nextInt(8);
            int target = rnd.nextInt(31) - 15;
            if (countWithZeros(a, target) != oracle(a, target)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Recognize] Target Sum (LeetCode 494)
<!-- id: cap-tgt-signed-expressions -->

**Approach.**
The plus group sum must be `(total + target) / 2`, as derived in the lesson, so the problem is a count of subsets with that sum. The method first rejects a target beyond the total in absolute value and a target whose parity differs from the total. Otherwise it builds the count table up to the goal and returns the last entry as an `int`.

The inner loop runs from the goal down to `x`, which keeps each element in a subset at most once. When `x` is 0 the loop covers every sum and each entry doubles, which gives the right count for zeros without a special case. Each entry keeps its meaning throughout: `ways[s]` is the number of subsets of the elements added so far with sum `s`.

**Complexity.**
- **Time** is O(n * goal), because each element updates up to `goal` entries.
- **Space** is O(goal) for the count array, and the input array stays unchanged.

```java run
import java.util.*;

public final class CapTgtSignedExpressions {
    /**
     * Returns the number of sign assignments whose signed sum equals target.
     * Time: O(n * goal). Space: O(goal).
     * Invariant: ways[s] counts subsets of the processed elements that sum to s.
     */
    static int findTargetWays(int[] nums, int target) {
        int total = 0;
        for (int x : nums) total += x;
        // The range test also keeps total + target nonnegative for the parity test.
        if (Math.abs(target) > total || (total + target) % 2 != 0) return 0;
        int goal = (total + target) / 2;
        int[] ways = new int[goal + 1];
        // The empty subset is one subset with sum 0.
        ways[0] = 1;
        for (int x : nums) {
            // Descending sums keep ways[s - x] at the state before x, and x = 0 doubles every entry.
            for (int s = goal; s >= x; s--) ways[s] += ways[s - x];
        }
        return ways[goal];
    }

    /** Oracle: the map over signed running sums from the naive section. */
    static int oracle(int[] nums, int target) {
        Map<Integer, Integer> ways = new HashMap<>();
        ways.put(0, 1);
        for (int x : nums) {
            Map<Integer, Integer> next = new HashMap<>();
            for (Map.Entry<Integer, Integer> e : ways.entrySet()) {
                next.merge(e.getKey() + x, e.getValue(), Integer::sum);
                next.merge(e.getKey() - x, e.getValue(), Integer::sum);
            }
            ways = next;
        }
        return ways.getOrDefault(target, 0);
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (findTargetWays(new int[] {2, 3, 5, 1}, 1) != 2) throw new AssertionError("ex1");
        if (findTargetWays(new int[] {4, 1, 3}, 9) != 0) throw new AssertionError("ex2");
        // A single element reaches only plus or minus itself.
        if (findTargetWays(new int[] {5}, 5) != 1 || findTargetWays(new int[] {5}, -5) != 1 || findTargetWays(new int[] {5}, 0) != 0) throw new AssertionError("single");
        // The five-ones example of the lesson.
        if (findTargetWays(new int[] {1, 1, 1, 1, 1}, 3) != 5) throw new AssertionError("ones");
        // The input array stays unchanged.
        int[] nums = {1, 0, 2};
        int[] copy = nums.clone();
        findTargetWays(nums, 1);
        if (!Arrays.equals(nums, copy)) throw new AssertionError("mutated");
        // Random inputs, including negative targets and zeros, against the signed-sum map.
        Random rnd = new Random(2717);
        for (int t = 0; t < 3000; t++) {
            int[] a = new int[1 + rnd.nextInt(10)];
            for (int i = 0; i < a.length; i++) a[i] = rnd.nextInt(9);
            int target = rnd.nextInt(41) - 20;
            if (findTargetWays(a, target) != oracle(a, target)) throw new AssertionError("random " + t);
        }
    }
}
```
