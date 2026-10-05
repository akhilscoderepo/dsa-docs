<!-- solutions-for: 08-two-pointers -->
### Solutions For Splitting An Array In Three

#### Solution: [Build] Partition 0,1,2 (Author exercise)
<!-- id: tp-partition-012 -->

**Approach.**
The scan keeps `low`, `mid` and `high`, and it inspects `nums[mid]`. A 0 swaps with the slot at `low`, and both `low` and `mid` advance. A 1 stays, and `mid` advances. A 2 swaps with the slot at `high`, and `high` moves back while `mid` waits. When the loop ends, `low` is the number of zeros, `mid - low` is the number of ones, and `n - (high + 1)` is the number of twos. The invariant is that slots before `low` hold 0, slots from `low` to `mid - 1` hold 1, and slots after `high` hold 2.

**Complexity.**
- **Time** is O(n), because each iteration shrinks the unresolved range by one slot.
- **Space** is O(1), because the method swaps inside the input and returns three counts.

```java run
import java.util.Arrays;
import java.util.Random;

public final class Partition012 {
    /**
     * Groups 0, 1, 2 in place and returns the three counts.
     * Time: O(n).
     * Space: O(1) beyond the three returned counts.
     * Invariant: nums[0..low-1] are 0, nums[low..mid-1] are 1, nums[high+1..] are 2.
     */
    static int[] partition(int[] nums) {
        int low = 0, mid = 0, high = nums.length - 1;
        // The unresolved range [mid, high] shrinks by one slot per iteration.
        while (mid <= high) {
            if (nums[mid] == 0) {
                // A zero joins the first region; the value from low is a known one, so mid advances.
                int t = nums[low]; nums[low] = nums[mid]; nums[mid] = t;
                low++;
                mid++;
            } else if (nums[mid] == 1) {
                // A one already sits in the middle region.
                mid++;
            } else {
                // A two joins the last region; the value from high is unread, so mid waits.
                int t = nums[mid]; nums[mid] = nums[high]; nums[high] = t;
                high--;
            }
        }
        // The region sizes follow from the final boundaries.
        return new int[] {low, mid - low, nums.length - (high + 1)};
    }

    public static void main(String[] args) {
        // The statement examples.
        int[] a = {1, 2, 0, 1};
        if (!Arrays.equals(partition(a), new int[] {1, 2, 1}) || !Arrays.equals(a, new int[] {0, 1, 1, 2})) throw new AssertionError("example 1");
        if (!Arrays.equals(partition(new int[0]), new int[] {0, 0, 0})) throw new AssertionError("example 2");
        // Random arrays against counting and sorting.
        Random rnd = new Random(41);
        for (int t = 0; t < 4000; t++) {
            int[] x = rnd.ints(rnd.nextInt(12), 0, 3).toArray();
            int[] expect = x.clone();
            Arrays.sort(expect);
            int[] counts = new int[3];
            for (int v : x) counts[v]++;
            int[] y = x.clone();
            if (!Arrays.equals(partition(y), counts) || !Arrays.equals(y, expect)) throw new AssertionError("random");
        }
    }
}
```

#### Solution: [Vary] Sort Colors (LeetCode 75)
<!-- id: tp-sort-colors -->

**Approach.**
The formal problem uses the same three groups, so the same scan solves it. The method swaps a 0 with the slot at `low`, leaves a 1, and swaps a 2 with the slot at `high`. The slot that arrives from `high` is unread, so `mid` does not advance after that swap. The loop condition is `mid <= high`, because the slot at `high` is still unresolved. The invariant is that the slots before `low` hold 0, the slots from `low` to `mid - 1` hold 1, and the slots after `high` hold 2.

**Complexity.**
- **Time** is O(n), because the scan makes one pass and each iteration settles one slot.
- **Space** is O(1), because the method keeps three indexes.

```java run
import java.util.Arrays;
import java.util.Random;

public final class SortColors75 {
    /**
     * Sorts an array of 0, 1 and 2 in place in one pass.
     * Time: O(n).
     * Space: O(1).
     * Invariant: slots before low are 0, slots in [low, mid) are 1, slots after high are 2.
     */
    static void sortColors(int[] nums) {
        int low = 0, mid = 0, high = nums.length - 1;
        // The loop includes mid == high, because that slot is unresolved.
        while (mid <= high) {
            int v = nums[mid];
            if (v == 0) {
                // Swap with low; the displaced value was a settled one, so both advance.
                nums[mid] = nums[low];
                nums[low] = 0;
                low++;
                mid++;
            } else if (v == 1) {
                mid++;
            } else {
                // Swap with high; the arriving value is unread, so mid stays.
                nums[mid] = nums[high];
                nums[high] = 2;
                high--;
            }
        }
    }

    /** The buggy variant that advances mid after the swap with high. */
    static void buggy(int[] nums) {
        int low = 0, mid = 0, high = nums.length - 1;
        while (mid <= high) {
            int v = nums[mid];
            if (v == 0) { nums[mid] = nums[low]; nums[low] = 0; low++; mid++; }
            else if (v == 1) mid++;
            else { nums[mid] = nums[high]; nums[high] = 2; high--; mid++; }
        }
    }

    public static void main(String[] args) {
        // The statement examples.
        int[] a = {2, 1, 0, 2, 1};
        sortColors(a);
        if (!Arrays.equals(a, new int[] {0, 1, 1, 2, 2})) throw new AssertionError("example 1");
        int[] b = {1};
        sortColors(b);
        if (!Arrays.equals(b, new int[] {1})) throw new AssertionError("example 2");
        // The variant that advances mid after the high swap fails on this input.
        int[] c = {1, 2, 0};
        buggy(c);
        if (Arrays.equals(c, new int[] {0, 1, 2})) throw new AssertionError("the buggy variant should fail");
        // Random arrays against Arrays.sort.
        Random rnd = new Random(42);
        for (int t = 0; t < 4000; t++) {
            int[] x = rnd.ints(1 + rnd.nextInt(12), 0, 3).toArray();
            int[] expect = x.clone();
            Arrays.sort(expect);
            sortColors(x);
            if (!Arrays.equals(x, expect)) throw new AssertionError("random");
        }
    }
}
```

#### Solution: [Boundary] Reinspect Swapped High (Author exercise)
<!-- id: tp-reinspect-high -->

**Approach.**
The method runs the three-way scan and counts one iteration per inspection of `nums[mid]`. A swap with `high` leaves `mid` in place, so the arriving value is inspected in the next iteration and adds one more iteration. A 1 and a 0 advance `mid`. Each iteration shrinks the unresolved range by one slot, and the swap with `high` shrinks it from the right end. The count therefore equals the number of values, because every slot is inspected exactly once as the range shrinks. A value that comes from `high` is a different slot, not a repeat of the same one.

**Complexity.**
- **Time** is O(n), because the loop runs once per slot.
- **Space** is O(1), because the method keeps three indexes and a counter.

```java run
import java.util.Random;

public final class ReinspectHigh {
    /**
     * Runs the three-way scan and returns the number of loop iterations.
     * Time: O(n).
     * Space: O(1).
     * Invariant: each iteration settles one slot, so the unresolved range shrinks by one.
     */
    static int iterations(int[] nums) {
        int low = 0, mid = 0, high = nums.length - 1, count = 0;
        while (mid <= high) {
            // One inspection of nums[mid] per iteration.
            count++;
            if (nums[mid] == 0) {
                int t = nums[low]; nums[low] = nums[mid]; nums[mid] = t;
                low++;
                mid++;
            } else if (nums[mid] == 1) {
                mid++;
            } else {
                // The arriving value is unread, so mid stays for the next iteration.
                int t = nums[mid]; nums[mid] = nums[high]; nums[high] = t;
                high--;
            }
        }
        return count;
    }

    public static void main(String[] args) {
        // The statement examples.
        if (iterations(new int[] {2, 0}) != 2) throw new AssertionError("example 1");
        if (iterations(new int[] {1, 2, 0}) != 3) throw new AssertionError("example 2");
        // The empty array runs no iteration.
        if (iterations(new int[0]) != 0) throw new AssertionError("empty");
        // Each iteration settles one slot, so the count equals the length for every input.
        Random rnd = new Random(43);
        for (int t = 0; t < 4000; t++) {
            int[] x = rnd.ints(rnd.nextInt(12), 0, 3).toArray();
            if (iterations(x.clone()) != x.length) throw new AssertionError("random");
        }
    }
}
```

#### Solution: [Recognize] Three-Way Pivot Partition (Author exercise)
<!-- id: tp-three-way-pivot -->

**Approach.**
The method replaces the group numbers with comparisons against `pivot`. A value below `pivot` swaps with the slot at `low`, and both `low` and `mid` advance. A value equal to `pivot` advances `mid`. A value above `pivot` swaps with the slot at `high`, and `mid` waits. When the loop ends, `low` is the first index of the equal region, and `mid` is the first index of the greater region. The invariant is that slots before `low` are below `pivot`, slots from `low` to `mid - 1` equal `pivot`, and slots after `high` are above `pivot`. When no value equals `pivot`, the equal region is empty, so the two returned indexes are the same.

**Complexity.**
- **Time** is O(n), because each iteration settles one slot.
- **Space** is O(1), because the method keeps three indexes and returns two.

```java run
import java.util.Arrays;
import java.util.Random;

public final class ThreeWayPivot {
    /**
     * Partitions around pivot and returns {first index equal to pivot, first index above pivot}.
     * Time: O(n).
     * Space: O(1).
     * Invariant: [0, low) < pivot, [low, mid) == pivot, (high, n) > pivot.
     */
    static int[] partition(int[] nums, int pivot) {
        int low = 0, mid = 0, high = nums.length - 1;
        while (mid <= high) {
            if (nums[mid] < pivot) {
                // A smaller value joins the first region; the swapped value is known to equal pivot.
                int t = nums[low]; nums[low] = nums[mid]; nums[mid] = t;
                low++;
                mid++;
            } else if (nums[mid] == pivot) {
                mid++;
            } else {
                // A larger value joins the last region; the arriving value is unread.
                int t = nums[mid]; nums[mid] = nums[high]; nums[high] = t;
                high--;
            }
        }
        // After the loop mid equals high + 1, which is the start of the last region.
        return new int[] {low, mid};
    }

    public static void main(String[] args) {
        // The statement examples.
        int[] a = {7, 5, 2, 9, 5, 1};
        if (!Arrays.equals(partition(a, 5), new int[] {2, 4})) throw new AssertionError("example 1");
        if (!Arrays.equals(partition(new int[] {4, 8}, 6), new int[] {1, 1})) throw new AssertionError("example 2");
        // The empty array.
        if (!Arrays.equals(partition(new int[0], 3), new int[] {0, 0})) throw new AssertionError("empty");
        // Random arrays against the region check.
        Random rnd = new Random(44);
        for (int t = 0; t < 4000; t++) {
            int[] x = rnd.ints(rnd.nextInt(12), -4, 5).toArray();
            int pivot = rnd.nextInt(9) - 4;
            int less = 0, equal = 0;
            for (int v : x) { if (v < pivot) less++; else if (v == pivot) equal++; }
            int[] y = x.clone();
            int[] got = partition(y, pivot);
            if (got[0] != less || got[1] != less + equal) throw new AssertionError("boundaries");
            for (int i = 0; i < y.length; i++) {
                int want = i < less ? -1 : (i < less + equal ? 0 : 1);
                if (Integer.compare(y[i], pivot) != want) throw new AssertionError("region");
            }
            int[] s1 = x.clone(), s2 = y.clone();
            Arrays.sort(s1);
            Arrays.sort(s2);
            if (!Arrays.equals(s1, s2)) throw new AssertionError("values");
        }
    }
}
```
