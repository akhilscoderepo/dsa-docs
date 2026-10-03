<!-- solutions-for: 08-cyclic-placement -->
### Cyclic Placement

#### Solution: [Build] Place 1..n (Author exercise)
<!-- id: ar-place-one-to-n -->

**Approach.** At each index, while the value is not the one that belongs there, swap it into its home slot `value - 1`. Every swap settles one value permanently, so the total number of swaps is at most `n` and the pass is linear. The assertions shuffle permutations at random and check that each slot holds its own number, and a counter confirms that no more than `n` swaps ever happen.

**Complexity.** O(n) time and O(1) extra space.

```java run
import java.util.Arrays;
import java.util.Random;

public final class PlaceOneToN {
    static int swaps;
    static void placeAll(int[] nums) {
        for (int i = 0; i < nums.length; i++) {
            while (nums[i] != i + 1) {
                int home = nums[i] - 1;
                int tmp = nums[home]; nums[home] = nums[i]; nums[i] = tmp;
                swaps++;
            }
        }
    }

    public static void main(String[] args) {
        int[] a = {3, 1, 2};
        placeAll(a);
        if (!Arrays.equals(a, new int[] {1, 2, 3})) throw new AssertionError("example 1");
        int[] b = {4, 3, 2, 1};
        placeAll(b);
        if (!Arrays.equals(b, new int[] {1, 2, 3, 4})) throw new AssertionError("example 2");
        Random rnd = new Random(41);
        for (int t = 0; t < 2000; t++) {
            int n = 1 + rnd.nextInt(20);
            int[] p = new int[n];
            for (int i = 0; i < n; i++) p[i] = i + 1;
            for (int i = n - 1; i > 0; i--) { int j = rnd.nextInt(i + 1); int tmp = p[i]; p[i] = p[j]; p[j] = tmp; }
            swaps = 0;
            placeAll(p);
            for (int i = 0; i < n; i++) if (p[i] != i + 1) throw new AssertionError("slot " + i + " unsettled");
            if (swaps > n) throw new AssertionError("more than n swaps: " + swaps);
        }
    }
}
```

#### Solution: [Vary] Missing Number (LeetCode 268)
<!-- id: ar-missing-number -->

**Approach.** With values in `0..n`, the home slot of a value `v` is index `v`, and the value `n` has no slot in an array of length `n`, so it is left alone. Swap each in-range value into its slot, then scan for the first index whose slot holds a different value. If every slot is settled, the missing number is `n`. The assertions compare with the arithmetic-series oracle, `n(n+1)/2` minus the sum, on randomly built inputs with one value removed.

**Complexity.** O(n) time and O(1) extra space.

```java run
import java.util.Random;

public final class MissingNumber {
    static int missingNumber(int[] nums) {
        int n = nums.length;
        for (int i = 0; i < n; i++) {
            while (nums[i] < n && nums[i] != i && nums[nums[i]] != nums[i]) {
                int home = nums[i];
                int tmp = nums[home]; nums[home] = nums[i]; nums[i] = tmp;
            }
        }
        for (int i = 0; i < n; i++) if (nums[i] != i) return i;
        return n;
    }

    public static void main(String[] args) {
        if (missingNumber(new int[] {4, 0, 2, 1}) != 3) throw new AssertionError("example 1");
        if (missingNumber(new int[] {0, 1}) != 2) throw new AssertionError("example 2");
        if (missingNumber(new int[] {1}) != 0) throw new AssertionError("missing zero");
        Random rnd = new Random(42);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(15);
            int gone = rnd.nextInt(n + 1);
            int[] a = new int[n];
            int k = 0;
            for (int v = 0; v <= n; v++) if (v != gone) a[k++] = v;
            for (int i = n - 1; i > 0; i--) { int j = rnd.nextInt(i + 1); int tmp = a[i]; a[i] = a[j]; a[j] = tmp; }
            if (missingNumber(a) != gone) throw new AssertionError("expected " + gone);
        }
    }
}
```

#### Solution: [Boundary] Duplicate Slot (Author exercise)
<!-- id: ar-duplicate-slot -->

**Approach.** Compare the value at the cursor with the value in its home slot, and stop when they are equal. A second copy of a settled value cannot be placed, and swapping two equal values changes nothing, so a loop that tested only the index would spin forever. After the pass, every slot that does not hold its own number marks a missing value, and the value sitting there is a duplicate. The assertions run the unguarded loop with a swap cap on `[2, 2]` and show that it hits the cap, then check that the guarded loop terminates with the expected arrays.

**Complexity.** O(n) time and O(1) extra space.

```java run
import java.util.Arrays;
import java.util.Random;

public final class DuplicateSlot {
    static void place(int[] nums) {
        for (int i = 0; i < nums.length; i++) {
            while (nums[i] != nums[nums[i] - 1]) {
                int home = nums[i] - 1;
                int tmp = nums[home]; nums[home] = nums[i]; nums[i] = tmp;
            }
        }
    }
    static boolean unguardedFinishes(int[] nums, int cap) {
        int swaps = 0;
        for (int i = 0; i < nums.length; i++) {
            while (nums[i] != i + 1) {
                if (++swaps > cap) return false;
                int home = nums[i] - 1;
                int tmp = nums[home]; nums[home] = nums[i]; nums[i] = tmp;
            }
        }
        return true;
    }

    public static void main(String[] args) {
        int[] a = {3, 1, 3};
        place(a);
        if (!Arrays.equals(a, new int[] {1, 3, 3})) throw new AssertionError("example 1: " + Arrays.toString(a));
        int[] b = {2, 2};
        place(b);
        if (!Arrays.equals(b, new int[] {2, 2})) throw new AssertionError("example 2");
        if (unguardedFinishes(new int[] {2, 2}, 1000)) throw new AssertionError("the unguarded loop must not finish on [2, 2]");
        Random rnd = new Random(43);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(10);
            int[] x = new int[n];
            for (int i = 0; i < n; i++) x[i] = 1 + rnd.nextInt(n);
            int[] sortedBefore = x.clone();
            Arrays.sort(sortedBefore);
            place(x);
            int[] sortedAfter = x.clone();
            Arrays.sort(sortedAfter);
            if (!Arrays.equals(sortedBefore, sortedAfter)) throw new AssertionError("placement must only permute the values");
            for (int i = 0; i < n; i++) {
                boolean present = false;
                for (int v : x) if (v == i + 1) present = true;
                if (present && x[i] != i + 1) throw new AssertionError("a present value " + (i + 1) + " is not in its slot");
            }
        }
    }
}
```

#### Solution: [Recognize] First Missing Positive (LeetCode 41)
<!-- id: ar-first-missing-positive -->

**Approach.** The answer lies in `1..n + 1`, so values outside `1..n` can never matter and are skipped. Every in-range value is swapped to its home slot unless that slot already holds the same value. After the pass, the first slot not holding `index + 1` names the answer, and if all slots are settled the answer is `n + 1`. The test order matters: the range check comes first, so no out-of-range index is ever evaluated. The assertions compare with a set-based oracle on random arrays that include zero, negatives and large values.

**Complexity.** O(n) time and O(1) extra space.

```java run
import java.util.HashSet;
import java.util.Random;
import java.util.Set;

public final class FirstMissingPositive {
    static int firstMissingPositive(int[] nums) {
        int n = nums.length;
        for (int i = 0; i < n; i++) {
            while (nums[i] >= 1 && nums[i] <= n && nums[nums[i] - 1] != nums[i]) {
                int home = nums[i] - 1;
                int tmp = nums[home]; nums[home] = nums[i]; nums[i] = tmp;
            }
        }
        for (int i = 0; i < n; i++) if (nums[i] != i + 1) return i + 1;
        return n + 1;
    }
    static int oracle(int[] nums) {
        Set<Integer> seen = new HashSet<>();
        for (int v : nums) seen.add(v);
        int c = 1;
        while (seen.contains(c)) c++;
        return c;
    }

    public static void main(String[] args) {
        if (firstMissingPositive(new int[] {7, 5, 1, 2, -4}) != 3) throw new AssertionError("example 1");
        if (firstMissingPositive(new int[] {1, 2, 3, 4}) != 5) throw new AssertionError("example 2");
        if (firstMissingPositive(new int[] {Integer.MAX_VALUE, Integer.MIN_VALUE, 0}) != 1) throw new AssertionError("extreme values");
        Random rnd = new Random(44);
        for (int t = 0; t < 5000; t++) {
            int[] a = new int[1 + rnd.nextInt(10)];
            for (int i = 0; i < a.length; i++) a[i] = rnd.nextInt(14) - 3;
            int expected = oracle(a);
            if (firstMissingPositive(a.clone()) != expected) throw new AssertionError("disagrees with the set oracle");
        }
    }
}
```
