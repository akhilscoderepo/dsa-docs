<!-- solutions-for: 01-arrays-core-operations -->
### Solutions For Cyclic Placement

#### Solution: [Build] Place 1..n (Author exercise)
<!-- id: ar-place-one-to-n -->

**Approach.** The method examines index `i` and reads the value `v = nums[i]`. The target slot of `v` is the index `v - 1`. When `nums[i]` is not yet at its target slot, the method swaps it there, and `i` stays still because a new, unexamined value now sits at `i`. When the value is already at its target slot, the method advances `i`.

Every swap places one value in its target slot, and the loop never moves a placed value again, so at most `n - 1` swaps happen. The input is a permutation, so no duplicate and no out-of-range value occurs. The harness asserts the final order on random permutations and counts the swaps to confirm the bound.

**Complexity.**

- **Time** is O(n), because there are at most `n - 1` swaps and `n` advances of `i`.
- **Space** is O(1), because the loop keeps `i`, `target` and a single temporary for the swap.

```java run
import java.util.Arrays;
import java.util.Random;

public final class PlaceOneToN {
    static int swaps;

    /**
     * Reorders a permutation of 1..n so that nums[i] == i + 1.
     * Time: O(n), because each swap places one value for good and i advances at most n times.
     * Space: O(1), because only scalars are stored.
     * Invariant: a value at its target slot is never moved again.
     */
    static void place(int[] nums) {
        // i is the index under examination; it starts at the left end.
        int i = 0;
        // The loop ends when i passes the last index; swaps keep i still, so the loop count is at most 2n.
        while (i < nums.length) {
            // The target slot of value v is v - 1.
            int target = nums[i] - 1;
            // A value away from its target slot is swapped there; the swap settles one value for good.
            if (nums[target] != nums[i]) {
                // Swap nums[i] with nums[target] through a temporary variable.
                int tmp = nums[i];
                nums[i] = nums[target];
                nums[target] = tmp;
                // Count the swaps so the harness can check the n - 1 bound.
                swaps++;
            } else {
                // The value is at its target slot, so i moves on.
                i++;
            }
        }
    }

    public static void main(String[] args) {
        // Checks Example 1 and Example 2.
        int[] a = {3, 1, 4, 2};
        place(a);
        if (!Arrays.equals(a, new int[] {1, 2, 3, 4})) throw new AssertionError("example 1");
        int[] b = {2, 1};
        place(b);
        if (!Arrays.equals(b, new int[] {1, 2})) throw new AssertionError("example 2");
        // Checks 3000 random permutations: the result is sorted, and the swap count stays below n.
        Random rnd = new Random(3);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(12);
            int[] x = new int[n];
            for (int i = 0; i < n; i++) x[i] = i + 1;
            // Shuffle the identity permutation.
            for (int i = n - 1; i > 0; i--) { int j = rnd.nextInt(i + 1); int tmp = x[i]; x[i] = x[j]; x[j] = tmp; }
            int[] expected = x.clone();
            Arrays.sort(expected);
            swaps = 0;
            place(x);
            if (!Arrays.equals(x, expected)) throw new AssertionError("not placed: " + Arrays.toString(x));
            if (swaps > n - 1) throw new AssertionError("more than n - 1 swaps");
        }
    }
}
```

#### Solution: [Vary] Missing Number (LeetCode 268)
<!-- id: ar-missing-number -->

**Approach.** The range runs from 0 to `n`, so the target slot of a value `v` is the index `v` itself. The value `n` has no target slot, because the last index is `n - 1`. The loop therefore swaps `nums[i]` into its target slot only when `nums[i] < n` and the target slot holds a different value, and otherwise advances `i`.

After placement, every value below `n` that is present sits at its own index. Exactly one value in `0..n` is absent. If it is below `n`, its index holds some other value, and the first index with `nums[i] != i` gives it. If every index holds its own number, the absent value is `n`. The harness compares the method with the sum formula `n(n + 1) / 2` minus the array sum on random inputs.

**Complexity.**

- **Time** is O(n), because the loop makes at most `n` swaps and at most `n` advances, and each pass costs constant work.
- **Space** is O(1), because the input array serves as the record and only `i` is added.

```java run
import java.util.Random;

public final class MissingNumber {
    /**
     * Returns the value in 0..n that is absent from nums.
     * Time: O(n), because each swap settles one value and i advances at most n times.
     * Space: O(1), because the input array is reused as the record.
     * Invariant: a value v below n at index v is never moved again.
     */
    static int missingNumber(int[] nums) {
        // n is both the array length and the one value without a target slot.
        int n = nums.length;
        // i is the index under examination.
        int i = 0;
        // The loop ends after at most n swaps and n advances.
        while (i < n) {
            // The target slot of value v is v itself, and the value n has none.
            int v = nums[i];
            // Swap only when v has a target slot and that slot holds a different value.
            if (v < n && nums[v] != v) {
                // Put v in its target slot; the displaced value lands at i and is examined next.
                nums[i] = nums[v];
                nums[v] = v;
            } else {
                // The value is settled or is n, so i moves on.
                i++;
            }
        }
        // The first index holding the wrong number is the absent value.
        for (int k = 0; k < n; k++) if (nums[k] != k) return k;
        // Every index holds its own number, so the absent value is n.
        return n;
    }

    public static void main(String[] args) {
        // Checks Example 1 and Example 2.
        if (missingNumber(new int[] {1, 4, 0, 2}) != 3) throw new AssertionError("example 1");
        if (missingNumber(new int[] {0, 1, 2}) != 3) throw new AssertionError("example 2");
        // Checks the case where the absent value is 0.
        if (missingNumber(new int[] {1}) != 0) throw new AssertionError("absent zero");
        // Checks 3000 random inputs against the sum formula.
        Random rnd = new Random(8);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(12);
            // Build 0..n, remove one random value, and shuffle the rest.
            int absent = rnd.nextInt(n + 1);
            int[] x = new int[n];
            int p = 0;
            for (int v = 0; v <= n; v++) if (v != absent) x[p++] = v;
            for (int i = n - 1; i > 0; i--) { int j = rnd.nextInt(i + 1); int tmp = x[i]; x[i] = x[j]; x[j] = tmp; }
            // The oracle is the expected sum minus the actual sum.
            int sum = 0;
            for (int v : x) sum += v;
            int want = n * (n + 1) / 2 - sum;
            if (want != absent) throw new AssertionError("oracle disagrees with construction");
            if (missingNumber(x) != want) throw new AssertionError("mismatch on random input");
        }
    }
}
```

#### Solution: [Boundary] Duplicate Slot (Author exercise)
<!-- id: ar-duplicate-slot -->

**Approach.** The method runs the placement loop with the duplicate guard `nums[target] != nums[i]`. When the target slot already holds the same value, a copy is settled there, so swapping would exchange two equal values and change nothing. The guard makes the loop advance instead.

Without the guard, the loop repeats the same swap on any array with a duplicate, such as `[1, 1]` at index 1. The harness shows this with a step cap on an unguarded version. After the guarded loop ends, each value from 1 to `n` that appears in the input sits at its own index. Every other index is wrong, so the answer is `n` minus the number of distinct values. The harness checks that formula and that the multiset of values stays unchanged.

**Complexity.**

- **Time** is O(n), because the guard keeps the swap count at most `n`, and the final count loop adds `n` more steps.
- **Space** is O(1), because the loop keeps a few integers and no copy of the array.

```java run
import java.util.Arrays;
import java.util.HashSet;
import java.util.Random;
import java.util.Set;

public final class DuplicateSlot {
    /**
     * Places values 1..n with the duplicate guard and counts the wrong indices.
     * Time: O(n), because each swap settles one value and i advances at most n times.
     * Space: O(1), because only scalars are stored.
     * Invariant: a value at its target slot never moves again.
     */
    static int misplacedAfterPlacement(int[] nums) {
        // i is the index under examination.
        int i = 0;
        // The loop ends after at most n swaps and n advances.
        while (i < nums.length) {
            // The target slot of value v is v - 1, valid because values lie in 1..n.
            int target = nums[i] - 1;
            // The guard: swap only when the target slot holds a different value.
            if (nums[target] != nums[i]) {
                // Swap nums[i] into its target slot.
                int tmp = nums[i];
                nums[i] = nums[target];
                nums[target] = tmp;
            } else {
                // The value is settled, or a copy is already settled; i moves on.
                i++;
            }
        }
        // Count the indices that hold the wrong number.
        int wrong = 0;
        for (int k = 0; k < nums.length; k++) if (nums[k] != k + 1) wrong++;
        return wrong;
    }

    /**
     * Placement without the guard, with a step cap so the harness can observe the endless loop.
     * Returns true when the loop finishes within the cap.
     */
    static boolean finishesWithoutGuard(int[] nums, int cap) {
        int i = 0, steps = 0;
        // Each pass is one swap or one advance; the cap stops an endless loop.
        while (i < nums.length) {
            if (++steps > cap) return false;
            int target = nums[i] - 1;
            // Without the guard, any value away from index target is swapped, even a duplicate.
            if (target != i) {
                int tmp = nums[i];
                nums[i] = nums[target];
                nums[target] = tmp;
            } else {
                i++;
            }
        }
        return true;
    }

    public static void main(String[] args) {
        // Checks Example 1 and Example 2.
        if (misplacedAfterPlacement(new int[] {3, 1, 3, 4, 2}) != 1) throw new AssertionError("example 1");
        if (misplacedAfterPlacement(new int[] {2, 2, 2}) != 2) throw new AssertionError("example 2");
        // Checks the claim that the loop without the guard never ends on an array with a duplicate.
        if (finishesWithoutGuard(new int[] {1, 1}, 1000)) throw new AssertionError("unguarded loop must not finish");
        // Checks 5000 random arrays: the formula n minus distinct values, and an unchanged multiset.
        Random rnd = new Random(13);
        for (int t = 0; t < 5000; t++) {
            int n = 1 + rnd.nextInt(10);
            int[] x = new int[n];
            Set<Integer> distinct = new HashSet<>();
            for (int i = 0; i < n; i++) { x[i] = 1 + rnd.nextInt(n); distinct.add(x[i]); }
            int[] sortedBefore = x.clone();
            Arrays.sort(sortedBefore);
            int got = misplacedAfterPlacement(x);
            if (got != n - distinct.size()) throw new AssertionError("formula mismatch");
            int[] sortedAfter = x.clone();
            Arrays.sort(sortedAfter);
            if (!Arrays.equals(sortedBefore, sortedAfter)) throw new AssertionError("values changed");
        }
    }
}
```

#### Solution: [Recognize] First Missing Positive (LeetCode 41)
<!-- id: ar-first-missing-positive -->

**Approach.** The answer lies between 1 and `n + 1`, because `n` cells can hold at most `n` different positive values. The cue is a value with one intended index together with permission to reorder. The method places every value from 1 to `n` at its target slot, and the duplicate guard and a range test keep the loop safe. Values at most 0, above `n`, or duplicated never block progress, because the loop advances past them.

After placement, the first index `k` with `nums[k] != k + 1` shows that `k + 1` never appeared, so the method returns `k + 1`. When every index holds its own number, the values 1 to `n` all appear and the method returns `n + 1`. The harness compares the method with a set-based oracle on random arrays that include negatives, zeros, duplicates and large values.

**Complexity.**

- **Time** is O(n), because swaps settle at most `n` values, the advances of `i` number at most `n`, and the final scan reads `n` cells.
- **Space** is O(1), because only `i`, `k` and a temporary value are stored beside the reordered input.

```java run
import java.util.HashSet;
import java.util.Random;
import java.util.Set;

public final class FirstMissingPositive {
    /**
     * Returns the smallest positive integer absent from nums, reordering nums in place.
     * Time: O(n), because each swap settles one value and i advances at most n times.
     * Space: O(1), because the input array is reused as the record.
     * Invariant: a value in 1..n at its target slot is never moved again.
     */
    static int firstMissingPositive(int[] nums) {
        int n = nums.length;
        // i is the index under examination.
        int i = 0;
        // The loop ends after at most n swaps and n advances.
        while (i < n) {
            // The target slot of value v is v - 1 when v lies in 1..n.
            int target = nums[i] - 1;
            // Range test first, so nums[target] is read only for a valid index.
            boolean hasTarget = target >= 0 && target < n;
            // Swap only when the value has a target slot and that slot holds a different value.
            if (hasTarget && nums[target] != nums[i]) {
                // Swap nums[i] into its target slot.
                int tmp = nums[i];
                nums[i] = nums[target];
                nums[target] = tmp;
            } else {
                // Settled, out of range or duplicate: i moves on.
                i++;
            }
        }
        // The first index with the wrong number reveals the smallest missing positive.
        for (int k = 0; k < n; k++) if (nums[k] != k + 1) return k + 1;
        // Every value from 1 to n is present, so the answer is n + 1.
        return n + 1;
    }

    /**
     * Oracle: a hash set of all values, which uses O(n) space.
     * Time: O(n). Space: O(n).
     */
    static int oracle(int[] nums) {
        // Store every value, then test 1, 2, 3, ... until one is absent.
        Set<Integer> seen = new HashSet<>();
        for (int v : nums) seen.add(v);
        int want = 1;
        while (seen.contains(want)) want++;
        return want;
    }

    public static void main(String[] args) {
        // Checks Example 1 and Example 2.
        if (firstMissingPositive(new int[] {2, 5, -3, 1, 0}) != 3) throw new AssertionError("example 1");
        if (firstMissingPositive(new int[] {6, 6, 1, 1, 1}) != 2) throw new AssertionError("example 2");
        // Checks a full permutation and an array with no positive value.
        if (firstMissingPositive(new int[] {3, 1, 2}) != 4) throw new AssertionError("permutation");
        if (firstMissingPositive(new int[] {-5, 0}) != 1) throw new AssertionError("no positives");
        // Checks the extreme values that make index arithmetic risky.
        if (firstMissingPositive(new int[] {Integer.MAX_VALUE, Integer.MIN_VALUE, 1}) != 2) throw new AssertionError("extreme values");
        // Checks 8000 random arrays against the set oracle.
        Random rnd = new Random(17);
        for (int t = 0; t < 8000; t++) {
            int[] x = new int[1 + rnd.nextInt(10)];
            for (int i = 0; i < x.length; i++) x[i] = rnd.nextInt(16) - 4;
            int want = oracle(x);
            if (firstMissingPositive(x) != want) throw new AssertionError("mismatch on random input");
        }
    }
}
```
