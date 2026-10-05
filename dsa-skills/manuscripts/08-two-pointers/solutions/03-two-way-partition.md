<!-- solutions-for: 08-two-pointers -->
### Solutions For Splitting An Array In Two

#### Solution: [Build] Sort Array By Parity (LeetCode 905)
<!-- id: tp-sort-by-parity -->

**Approach.**
The scan keeps an unresolved range between `left` and `right`. An even value at `left` is already in the first region, so `left` moves. An odd value at `right` is already in the second region, so `right` moves. When `left` holds an odd value and `right` holds an even value, both are misplaced, and one swap fixes both. The invariant is that every index before `left` holds an even value and every index after `right` holds an odd value. The parity test is `x % 2 == 0`, because `-3 % 2` is `-1` in Java and a test for `== 1` would treat negative odd values as even.

**Complexity.**
- **Time** is O(n), because each iteration shrinks the unresolved range by at least one index.
- **Space** is O(1), because the method swaps inside the input array.

```java run
import java.util.Arrays;
import java.util.Random;

public final class SortByParity905 {
    /**
     * Rearranges nums so that all even values precede all odd values.
     * Time: O(n).
     * Space: O(1).
     * Invariant: indexes before left are even, indexes after right are odd.
     */
    static int[] sortByParity(int[] nums) {
        int left = 0, right = nums.length - 1;
        // The unresolved range [left, right] shrinks every iteration.
        while (left < right) {
            // An even value at left already belongs to the first region.
            if (nums[left] % 2 == 0) left++;
            // An odd value at right already belongs to the second region.
            else if (nums[right] % 2 != 0) right--;
            // Both ends are misplaced, so one swap fixes two values.
            else {
                int tmp = nums[left];
                nums[left] = nums[right];
                nums[right] = tmp;
                left++;
                right--;
            }
        }
        return nums;
    }

    static boolean valid(int[] before, int[] after) {
        // The result must contain the same values.
        int[] a = before.clone(), b = after.clone();
        Arrays.sort(a);
        Arrays.sort(b);
        if (!Arrays.equals(a, b)) return false;
        // After the first odd value, no even value may appear.
        boolean seenOdd = false;
        for (int x : after) {
            if (x % 2 != 0) seenOdd = true;
            else if (seenOdd) return false;
        }
        return true;
    }

    public static void main(String[] args) {
        // Java gives a negative remainder for negative odd values, so the test must be != 0.
        if (-3 % 2 != -1) throw new AssertionError("remainder");
        // The statement examples.
        if (!Arrays.equals(sortByParity(new int[] {5, 2, 8, 3}), new int[] {8, 2, 5, 3})) throw new AssertionError("example 1");
        if (!Arrays.equals(sortByParity(new int[] {-1, -4}), new int[] {-4, -1})) throw new AssertionError("example 2");
        // The empty array.
        if (sortByParity(new int[0]).length != 0) throw new AssertionError("empty");
        // Random arrays with negative values against the validity check.
        Random rnd = new Random(31);
        for (int t = 0; t < 4000; t++) {
            int[] x = rnd.ints(rnd.nextInt(10), -6, 7).toArray();
            int[] y = x.clone();
            if (!valid(x, sortByParity(y))) throw new AssertionError("random " + Arrays.toString(x));
        }
    }
}
```

#### Solution: [Vary] Partition Around Pivot (Author exercise)
<!-- id: tp-partition-pivot -->

**Approach.**
The scan index `i` visits every slot once, and the boundary `store` is the first slot of the second region. A value below `pivot` swaps with the value at `store`, and then `store` advances. A value that is not below `pivot` leaves `store` unchanged. The invariant is that slots before `store` hold values below `pivot`, slots from `store` up to `i` hold values not below `pivot`, and slots from `i` on are unread. The method returns `store`, which is the count of values below `pivot`.

**Complexity.**
- **Time** is O(n), because one pass makes one comparison per slot and at most one swap.
- **Space** is O(1), because the method swaps inside the input array.

```java run
import java.util.Arrays;
import java.util.Random;

public final class PartitionPivot {
    /**
     * Moves values below pivot to the front and returns how many there are.
     * Time: O(n).
     * Space: O(1).
     * Invariant: nums[0..store-1] < pivot and nums[store..i-1] >= pivot.
     */
    static int partition(int[] nums, int pivot) {
        int store = 0;
        // i reads each slot once, so the loop costs n steps.
        for (int i = 0; i < nums.length; i++) {
            // A value below pivot joins the first region at store.
            if (nums[i] < pivot) {
                int tmp = nums[store];
                nums[store] = nums[i];
                nums[i] = tmp;
                store++;
            }
        }
        return store;
    }

    public static void main(String[] args) {
        // The statement examples.
        int[] a = {7, 2, 9, 3, 5, 1};
        int k = partition(a, 5);
        int[] firstThree = Arrays.copyOf(a, 3);
        Arrays.sort(firstThree);
        if (k != 3 || !Arrays.equals(firstThree, new int[] {1, 2, 3})) throw new AssertionError("example 1");
        if (partition(new int[] {6, 6}, 6) != 0) throw new AssertionError("example 2");
        // The empty array.
        if (partition(new int[0], 0) != 0) throw new AssertionError("empty");
        // Random arrays against a count and a region check.
        Random rnd = new Random(32);
        for (int t = 0; t < 4000; t++) {
            int[] x = rnd.ints(rnd.nextInt(10), -5, 6).toArray();
            int pivot = rnd.nextInt(11) - 5;
            int expectK = (int) Arrays.stream(x).filter(v -> v < pivot).count();
            int[] y = x.clone();
            int got = partition(y, pivot);
            if (got != expectK) throw new AssertionError("count");
            for (int i = 0; i < y.length; i++) if ((i < got) != (y[i] < pivot)) throw new AssertionError("region");
            int[] s1 = x.clone(), s2 = y.clone();
            Arrays.sort(s1);
            Arrays.sort(s2);
            if (!Arrays.equals(s1, s2)) throw new AssertionError("values");
        }
    }
}
```

#### Solution: [Boundary] One Empty Region (Author exercise)
<!-- id: tp-one-empty-region -->

**Approach.**
The method runs the opposite-end scan and counts each swap. When every value is even, `left` walks across the array and `right` never moves. When every value is odd, `right` walks down and `left` never moves, because the odd value at `left` sends the test to the `right` branch. Both cases end with the pointers met and no swap. A swap happens only when `nums[left]` is odd and `nums[right]` is even, so the count equals the number of such pairs the scan meets.

**Complexity.**
- **Time** is O(n), because every iteration shrinks the unresolved range.
- **Space** is O(1), because the method keeps two indexes and a counter.

```java run
import java.util.Random;

public final class OneEmptyRegion {
    /**
     * Partitions even values first and returns the number of swaps.
     * Time: O(n).
     * Space: O(1).
     * Invariant: indexes before left are even, indexes after right are odd.
     */
    static int swapCount(int[] nums) {
        int left = 0, right = nums.length - 1, swaps = 0;
        while (left < right) {
            // Only misplaced values at both ends cause a swap.
            if (nums[left] % 2 == 0) left++;
            else if (nums[right] % 2 != 0) right--;
            else {
                int tmp = nums[left];
                nums[left] = nums[right];
                nums[right] = tmp;
                swaps++;
                left++;
                right--;
            }
        }
        return swaps;
    }

    public static void main(String[] args) {
        // The statement examples.
        if (swapCount(new int[] {2, 4, 6}) != 0) throw new AssertionError("all even");
        if (swapCount(new int[] {1, 3}) != 0) throw new AssertionError("all odd");
        // The empty array and a mixed array.
        if (swapCount(new int[0]) != 0) throw new AssertionError("empty");
        if (swapCount(new int[] {1, 2}) != 1) throw new AssertionError("mixed");
        // Random arrays: the count never exceeds the number of odd values in the even region.
        Random rnd = new Random(33);
        for (int t = 0; t < 4000; t++) {
            int[] x = rnd.ints(rnd.nextInt(10), -4, 5).toArray();
            int evens = 0;
            for (int v : x) if (v % 2 == 0) evens++;
            int misplaced = 0;
            for (int i = 0; i < evens; i++) if (x[i] % 2 != 0) misplaced++;
            if (swapCount(x.clone()) != misplaced) throw new AssertionError("random");
        }
    }
}
```

#### Solution: [Recognize] Sort Array By Parity II (LeetCode 922)
<!-- id: tp-parity-two -->

**Approach.**
The even slots are the indexes `0, 2, 4, ...` and the odd slots are `1, 3, 5, ...`. The pointer `even` walks the even slots and stops at a slot that holds an odd value. The pointer `odd` walks the odd slots and stops at a slot that holds an even value. The two stopped slots hold values of the opposite parity, so one swap fixes both. The counts of even and odd values are equal, so the two pointers run out together. The invariant is that every even slot before `even` holds an even value and every odd slot before `odd` holds an odd value.

**Complexity.**
- **Time** is O(n), because each pointer moves forward by two and never moves back.
- **Space** is O(1), because the method swaps inside the input array.

```java run
import java.util.Arrays;
import java.util.Random;

public final class ParityTwo922 {
    /**
     * Places even values at even indexes and odd values at odd indexes.
     * Time: O(n).
     * Space: O(1).
     * Invariant: even slots before even and odd slots before odd already hold the right parity.
     */
    static int[] sortArrayByParityII(int[] nums) {
        int odd = 1;
        // even visits slots 0, 2, 4, ..., so the loop makes n / 2 outer steps.
        for (int even = 0; even < nums.length; even += 2) {
            // An odd value in an even slot needs a partner.
            if (nums[even] % 2 != 0) {
                // odd skips the odd slots that already hold odd values.
                while (nums[odd] % 2 != 0) odd += 2;
                // The partner is an even value in an odd slot, so the swap fixes both slots.
                int tmp = nums[even];
                nums[even] = nums[odd];
                nums[odd] = tmp;
            }
        }
        return nums;
    }

    public static void main(String[] args) {
        // The statement examples.
        if (!Arrays.equals(sortArrayByParityII(new int[] {4, 1, 2, 3}), new int[] {4, 1, 2, 3})) throw new AssertionError("example 1");
        int[] b = sortArrayByParityII(new int[] {3, 2, 1, 4});
        for (int i = 0; i < b.length; i++) if (b[i] % 2 != i % 2) throw new AssertionError("example 2");
        // Random balanced arrays against the index-parity rule and the multiset.
        Random rnd = new Random(34);
        for (int t = 0; t < 4000; t++) {
            int half = 1 + rnd.nextInt(5);
            int[] x = new int[2 * half];
            for (int i = 0; i < half; i++) { x[i] = 2 * rnd.nextInt(10); x[half + i] = 2 * rnd.nextInt(10) + 1; }
            for (int i = x.length - 1; i > 0; i--) { int j = rnd.nextInt(i + 1); int tmp = x[i]; x[i] = x[j]; x[j] = tmp; }
            int[] y = sortArrayByParityII(x.clone());
            for (int i = 0; i < y.length; i++) if (y[i] % 2 != i % 2) throw new AssertionError("parity");
            int[] s1 = x.clone(), s2 = y.clone();
            Arrays.sort(s1);
            Arrays.sort(s2);
            if (!Arrays.equals(s1, s2)) throw new AssertionError("values");
        }
    }
}
```
