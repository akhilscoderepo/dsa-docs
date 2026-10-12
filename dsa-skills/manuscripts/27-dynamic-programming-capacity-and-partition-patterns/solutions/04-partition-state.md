<!-- solutions-for: 27-dynamic-programming-capacity-and-partition-patterns -->
### Solutions For Partition State

#### Solution: [Build] Reachable Subset Sums (Author exercise)
<!-- id: cap-part-reachable-sums -->

**Approach.**
The table has one boolean for every sum from 0 to the total of all elements, and only `reach[0]` starts true for the empty subset. Each element `x` sets `reach[s]` for every sum `s` whose predecessor `s - x` was reachable before `x` was added. The loop visits sums from the total down to `x`, so the predecessor still describes the earlier elements and no element is counted twice.

At every step, `reach[s]` is true exactly for sums of subsets of the processed elements. The count of distinct subset sums is the number of true entries in the final table, and the empty array gives 1.

**Complexity.**
- **Time** is O(n * total), because each element updates up to `total` entries.
- **Space** is O(total) for the boolean array, and the input array stays unchanged.

```java run
import java.util.*;

public final class CapPartReachableSums {
    /**
     * Returns the number of distinct subset sums, including the empty sum 0.
     * Time: O(n * total). Space: O(total).
     * Invariant: reach[s] is true exactly for sums of subsets of the processed elements.
     */
    static int countSums(int[] nums) {
        int total = 0;
        for (int x : nums) total += x;
        boolean[] reach = new boolean[total + 1];
        // The empty subset sums to 0.
        reach[0] = true;
        for (int x : nums) {
            // Descending sums keep reach[s - x] at the state before x.
            for (int s = total; s >= x; s--) {
                if (reach[s - x]) reach[s] = true;
            }
        }
        // Count the sums that some subset reaches.
        int count = 0;
        for (boolean flag : reach) if (flag) count++;
        return count;
    }

    /** Oracle: collects the sum of every subset in a set. */
    static int oracle(int[] nums) {
        Set<Integer> seen = new HashSet<>();
        for (int mask = 0; mask < (1 << nums.length); mask++) {
            int sum = 0;
            for (int i = 0; i < nums.length; i++) if ((mask >> i & 1) == 1) sum += nums[i];
            seen.add(sum);
        }
        return seen.size();
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (countSums(new int[] {1, 2, 2}) != 6) throw new AssertionError("ex1");
        if (countSums(new int[] {5, 5}) != 3) throw new AssertionError("ex2");
        // The empty array has exactly the empty sum.
        if (countSums(new int[] {}) != 1) throw new AssertionError("empty");
        // The input array stays unchanged.
        int[] nums = {4, 1, 3};
        int[] copy = nums.clone();
        countSums(nums);
        if (!Arrays.equals(nums, copy)) throw new AssertionError("mutated");
        // Random inputs against the subset oracle.
        Random rnd = new Random(2710);
        for (int t = 0; t < 3000; t++) {
            int[] a = new int[rnd.nextInt(11)];
            for (int i = 0; i < a.length; i++) a[i] = 1 + rnd.nextInt(12);
            if (countSums(a) != oracle(a)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Vary] Smallest Equal Group (LeetCode 416)
<!-- id: cap-part-smallest-group -->

**Approach.**
An odd total has no equal split, so the method returns -1 at once. For an even total, each group of an equal split sums to the target `total / 2`, so the smallest group has the fewest elements among subsets that sum to the target. The table `fewest[s]` holds the fewest elements of a subset that sums to `s`, with the marker `n + 1` for sums that no subset reaches and `fewest[0] = 0`.

For each element `x`, the loop visits sums from the target down to `x` and keeps the smaller of `fewest[s]` and `fewest[s - x] + 1`. The descending order makes `fewest[s - x]` describe the elements before `x`. The invariant is that `fewest[s]` is exact for the processed elements. The answer is `fewest[target]` or -1 when it holds the marker.

**Complexity.**
- **Time** is O(n * target), because each element updates up to `target` entries.
- **Space** is O(target) for the count array, and the input array stays unchanged.

```java run
import java.util.*;

public final class CapPartSmallestGroup {
    /**
     * Returns the fewest elements of a group in an equal split, or -1 when no equal split exists.
     * Time: O(n * target). Space: O(target).
     * Invariant: fewest[s] is the fewest elements of a subset of the processed elements that sums to s.
     */
    static int smallestGroup(int[] nums) {
        int total = 0;
        for (int x : nums) total += x;
        // An odd total cannot be halved into integers.
        if (total % 2 != 0) return -1;
        int target = total / 2;
        int n = nums.length;
        // The marker n + 1 is larger than any real element count.
        int[] fewest = new int[target + 1];
        Arrays.fill(fewest, n + 1);
        // The empty subset has 0 elements and sums to 0.
        fewest[0] = 0;
        for (int x : nums) {
            // Descending sums keep fewest[s - x] at the state before x.
            for (int s = target; s >= x; s--) {
                // Adding x to the best subset for s - x gives a candidate with one more element.
                if (fewest[s - x] + 1 < fewest[s]) fewest[s] = fewest[s - x] + 1;
            }
        }
        // The marker means no subset reaches the target.
        return fewest[target] > n ? -1 : fewest[target];
    }

    /** Oracle: tests every subset and keeps the smallest one that sums to half. */
    static int oracle(int[] nums) {
        int total = 0;
        for (int x : nums) total += x;
        int best = -1;
        for (int mask = 0; mask < (1 << nums.length); mask++) {
            int sum = 0;
            for (int i = 0; i < nums.length; i++) if ((mask >> i & 1) == 1) sum += nums[i];
            if (sum * 2 == total) {
                int size = Integer.bitCount(mask);
                if (best == -1 || size < best) best = size;
            }
        }
        return best;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (smallestGroup(new int[] {4, 6, 5, 3, 2}) != 2) throw new AssertionError("ex1");
        if (smallestGroup(new int[] {3, 5, 9, 2}) != -1) throw new AssertionError("ex2");
        // One large element can form the smaller group alone.
        if (smallestGroup(new int[] {1, 1, 1, 1, 4}) != 1) throw new AssertionError("one big");
        // The input array stays unchanged.
        int[] nums = {4, 6, 5, 3, 2};
        int[] copy = nums.clone();
        smallestGroup(nums);
        if (!Arrays.equals(nums, copy)) throw new AssertionError("mutated");
        // Random inputs against the subset oracle.
        Random rnd = new Random(2711);
        for (int t = 0; t < 3000; t++) {
            int[] a = new int[1 + rnd.nextInt(11)];
            for (int i = 0; i < a.length; i++) a[i] = 1 + rnd.nextInt(10);
            if (smallestGroup(a) != oracle(a)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Boundary] Odd Total And Large Target (Author exercise)
<!-- id: cap-part-odd-and-large -->

**Approach.**
The method decides as much as it can before it allocates anything. It sums the elements into a `long`, because elements up to 10^9 can push the total past the `int` range. An odd total returns 0 immediately. For an even total, the target is `total / 2`, and the table would need `target + 1` entries. If that number exceeds `cellBudget`, the method returns 3 without building the table.

Only then does the method allocate a boolean array of length `target + 1`, which is at most `cellBudget` and so fits in an `int`. It runs the descending subset-sum update and returns 1 when `reach[target]` is true and 2 otherwise. The flags keep their usual meaning, so each true entry names a sum that some subset of the processed elements reaches.

**Complexity.**
- **Time** is O(n) for the checks and O(n * target) for the table, and the table runs only when the target fits the budget.
- **Space** is O(min(target, cellBudget)) because the budget check precedes the allocation.

```java run
import java.util.*;

public final class CapPartOddAndLarge {
    /**
     * Returns 0 for an odd total, 3 when the table exceeds the budget, 1 for an equal split and 2 otherwise.
     * Time: O(n * target). Space: O(min(target, cellBudget)).
     * Invariant: reach[s] is true exactly for sums of subsets of the processed elements.
     */
    static int status(int[] nums, int cellBudget) {
        // A long total cannot overflow for 100 elements up to 10^9.
        long total = 0;
        for (int x : nums) total += x;
        // Parity decides first and costs no memory.
        if (total % 2 != 0) return 0;
        long target = total / 2;
        // The budget check comes before the allocation, so a huge target never allocates.
        if (target + 1 > cellBudget) return 3;
        boolean[] reach = new boolean[(int) target + 1];
        // The empty subset sums to 0.
        reach[0] = true;
        for (int x : nums) {
            // An element above the target cannot enter the loop.
            for (int s = (int) target; s >= x; s--) {
                if (reach[s - x]) reach[s] = true;
            }
        }
        // One group sums to the target exactly when the target is reachable.
        return reach[(int) target] ? 1 : 2;
    }

    /** Oracle: parity, budget, then subset enumeration. */
    static int oracle(int[] nums, int cellBudget) {
        long total = 0;
        for (int x : nums) total += x;
        if (total % 2 != 0) return 0;
        if (total / 2 + 1 > cellBudget) return 3;
        for (int mask = 0; mask < (1 << nums.length); mask++) {
            long sum = 0;
            for (int i = 0; i < nums.length; i++) if ((mask >> i & 1) == 1) sum += nums[i];
            if (sum * 2 == total) return 1;
        }
        return 2;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (status(new int[] {1, 2, 4}, 100) != 0) throw new AssertionError("ex1");
        if (status(new int[] {5, 5, 10}, 5) != 3) throw new AssertionError("ex2");
        // Large elements: the long total is 3 * 10^9 and the budget check refuses the table.
        if (status(new int[] {1_000_000_000, 1_000_000_000, 1_000_000_000, 1_000_000_000}, 1_000_000) != 3) throw new AssertionError("large");
        // Java fact: the same sum in an int becomes negative, which would make the target negative.
        int wrapped = 1_000_000_000 + 1_000_000_000 + 1_000_000_000;
        if (wrapped >= 0) throw new AssertionError("int should overflow");
        // The input array stays unchanged.
        int[] nums = {3, 1, 4};
        int[] copy = nums.clone();
        status(nums, 50);
        if (!Arrays.equals(nums, copy)) throw new AssertionError("mutated");
        // Random inputs against the oracle, with budgets that sometimes refuse the table.
        Random rnd = new Random(2712);
        for (int t = 0; t < 3000; t++) {
            int[] a = new int[1 + rnd.nextInt(10)];
            for (int i = 0; i < a.length; i++) a[i] = 1 + rnd.nextInt(10);
            int budget = 1 + rnd.nextInt(40);
            if (status(a, budget) != oracle(a, budget)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Recognize] Last Stone Weight II (LeetCode 1049)
<!-- id: cap-part-last-stone -->

**Approach.**
Every sequence of smashes leaves one stone whose weight is a signed sum of the original weights, with a plus sign or a minus sign on each stone. The stones with plus signs form one group and the stones with minus signs form the other, so the final weight is the absolute difference of two group sums. Any split into two groups can also be reached by some order of smashes, so the answer is the smallest possible difference of two group sums.

If one group sums to `s`, the other sums to `total - s`, and the difference is `total - 2s` for `s <= total / 2`. The smallest difference comes from the largest reachable `s` that is at most `total / 2`. The method builds the one-use reachable-sum table up to `total / 2`, finds the largest true entry, and returns `total - 2 * s`. The flag table keeps the meaning from the earlier solutions in this lesson.

**Complexity.**
- **Time** is O(n * total), because each stone updates up to `total / 2` entries and the search scans the table once.
- **Space** is O(total) for the boolean array, and the input array stays unchanged.

```java run
import java.util.*;

public final class CapPartLastStone {
    /**
     * Returns the smallest possible weight of the remaining stone, or 0 when none remains.
     * Time: O(n * total). Space: O(total).
     * Invariant: reach[s] is true exactly for sums of subsets of the processed stones.
     */
    static int lastStone(int[] stones) {
        int total = 0;
        for (int x : stones) total += x;
        int half = total / 2;
        boolean[] reach = new boolean[half + 1];
        // The empty subset sums to 0.
        reach[0] = true;
        for (int x : stones) {
            // Descending sums use each stone once.
            for (int s = half; s >= x; s--) {
                if (reach[s - x]) reach[s] = true;
            }
        }
        // The largest reachable sum at most half gives the smallest difference.
        int best = 0;
        for (int s = half; s >= 0; s--) {
            if (reach[s]) {
                best = s;
                break;
            }
        }
        return total - 2 * best;
    }

    /** Oracle: simulates the smashing game over every pair of stones. */
    static int oracle(List<Integer> stones) {
        if (stones.size() <= 1) return stones.isEmpty() ? 0 : stones.get(0);
        int best = Integer.MAX_VALUE;
        for (int i = 0; i < stones.size(); i++) {
            for (int j = i + 1; j < stones.size(); j++) {
                List<Integer> rest = new ArrayList<>();
                for (int k = 0; k < stones.size(); k++) if (k != i && k != j) rest.add(stones.get(k));
                int diff = Math.abs(stones.get(i) - stones.get(j));
                if (diff > 0) rest.add(diff);
                best = Math.min(best, oracle(rest));
            }
        }
        return best;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (lastStone(new int[] {10, 4, 3, 1}) != 2) throw new AssertionError("ex1");
        if (lastStone(new int[] {6, 11, 4, 9}) != 0) throw new AssertionError("ex2");
        // One stone remains as it is.
        if (lastStone(new int[] {17}) != 17) throw new AssertionError("single");
        // The input array stays unchanged.
        int[] stones = {10, 4, 3, 1};
        int[] copy = stones.clone();
        lastStone(stones);
        if (!Arrays.equals(stones, copy)) throw new AssertionError("mutated");
        // Random inputs against the game simulation.
        Random rnd = new Random(2713);
        for (int t = 0; t < 600; t++) {
            int n = 1 + rnd.nextInt(6);
            int[] a = new int[n];
            List<Integer> list = new ArrayList<>();
            for (int i = 0; i < n; i++) {
                a[i] = 1 + rnd.nextInt(12);
                list.add(a[i]);
            }
            if (lastStone(a) != oracle(list)) throw new AssertionError("random " + t);
        }
    }
}
```
