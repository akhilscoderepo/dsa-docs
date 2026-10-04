<!-- solutions-for: 05-sorting-and-java-comparators -->
### Solutions For Sorting A Primitive Array

#### Solution: [Build] Sort A Primitive Copy (Author exercise)
<!-- id: so-sorted-copy -->

**Approach.**
The method builds an independent copy with `Arrays.copyOf` and sorts the copy, so the caller's array is never written. The invariant after the sort is that every adjacent pair of the copy is nondecreasing and the copy holds the same multiset of values as `nums`. The harness asserts that the input keeps its order, that the answer is a different object, and that the sort call returns nothing that code could chain.

**Complexity.**
- **Time** is O(n log n), because the copy costs O(n) and the library sort dominates.
- **Space** is O(n), because the copy holds every value next to the original.

```java run
import java.util.*;

public final class SortedCopy {
    /**
     * Returns an ascending copy of nums and leaves nums unchanged.
     * Time: O(n log n). Space: O(n).
     * Invariant: the result is nondecreasing and holds the same values as nums.
     */
    static int[] sortedCopy(int[] nums) {
        // The copy is the only array that the sort writes to.
        int[] copy = Arrays.copyOf(nums, nums.length);
        Arrays.sort(copy);
        return copy;
    }

    public static void main(String[] args) throws Exception {
        // The statement examples, including the unchanged input.
        int[] in = {9, 2, 7, 2};
        int[] out = sortedCopy(in);
        if (!Arrays.equals(out, new int[] {2, 2, 7, 9})) throw new AssertionError("example 1");
        if (!Arrays.equals(in, new int[] {9, 2, 7, 2})) throw new AssertionError("input mutated");
        if (out == in) throw new AssertionError("same object");
        if (sortedCopy(new int[0]).length != 0) throw new AssertionError("example 2");
        // Java fact from the lesson: Arrays.sort on an int[] returns void.
        if (Arrays.class.getMethod("sort", int[].class).getReturnType() != void.class) throw new AssertionError("return type");
        // Random arrays are checked against a counting oracle for the same multiset and the order.
        Random rnd = new Random(61);
        for (int t = 0; t < 500; t++) {
            int[] a = new int[rnd.nextInt(12)];
            for (int k = 0; k < a.length; k++) a[k] = rnd.nextInt(9) - 4;
            int[] snapshot = a.clone();
            int[] r = sortedCopy(a);
            if (!Arrays.equals(a, snapshot)) throw new AssertionError("mutated");
            for (int k = 1; k < r.length; k++) if (r[k - 1] > r[k]) throw new AssertionError("order");
            int[] counts = new int[9];
            for (int v : a) counts[v + 4]++;
            for (int v : r) counts[v + 4]--;
            for (int c : counts) if (c != 0) throw new AssertionError("multiset");
        }
    }
}
```

#### Solution: [Vary] Sort A Subrange (Author exercise)
<!-- id: so-sort-subrange -->

**Approach.**
The method passes both bounds to `Arrays.sort(nums, from, to)`, which sorts the half-open range and leaves every other position alone. The invariant is that positions outside `[from, to)` hold their original values, and the range is nondecreasing. The harness asserts the exception types that the library throws for `from > to` and for bounds outside the array.

**Complexity.**
- **Time** is O(k log k) for a range of length k = to - from, because the sort touches only that range.
- **Space** is O(1) extra for the call itself, apart from any working space of the library.

```java run
import java.util.*;

public final class SortSubrange {
    /**
     * Sorts nums[from..to) ascending in place.
     * Time: O(k log k) for k = to - from. Space: O(1) beyond the library.
     * Invariant: positions outside [from, to) keep their values.
     */
    static void sortRange(int[] nums, int from, int to) {
        // The library sorts only the half-open range and checks the bounds itself.
        Arrays.sort(nums, from, to);
    }

    public static void main(String[] args) {
        // The statement examples.
        int[] a = {8, 6, 4, 2, 0};
        sortRange(a, 1, 4);
        if (!Arrays.equals(a, new int[] {8, 2, 4, 6, 0})) throw new AssertionError("example 1");
        boolean threw = false;
        try { sortRange(new int[] {5, 1}, 2, 1); } catch (IllegalArgumentException e) { threw = true; }
        if (!threw) throw new AssertionError("example 2");
        // Java facts from the lesson: an empty range changes nothing, bounds outside the array throw.
        int[] b = {3, 2, 1};
        sortRange(b, 1, 1);
        if (!Arrays.equals(b, new int[] {3, 2, 1})) throw new AssertionError("empty range");
        threw = false;
        try { sortRange(new int[3], 0, 4); } catch (ArrayIndexOutOfBoundsException e) { threw = true; }
        if (!threw) throw new AssertionError("to past the end");
        threw = false;
        try { sortRange(new int[3], -1, 2); } catch (ArrayIndexOutOfBoundsException e) { threw = true; }
        if (!threw) throw new AssertionError("negative from");
        // Random ranges are checked against a copy that sorts the slice by hand.
        Random rnd = new Random(62);
        for (int t = 0; t < 500; t++) {
            int n = rnd.nextInt(10);
            int[] x = new int[n];
            for (int k = 0; k < n; k++) x[k] = rnd.nextInt(7) - 3;
            int from = rnd.nextInt(n + 1), to = from + rnd.nextInt(n - from + 1);
            int[] expect = x.clone();
            int[] slice = Arrays.copyOfRange(x, from, to);
            Arrays.sort(slice);
            System.arraycopy(slice, 0, expect, from, slice.length);
            sortRange(x, from, to);
            if (!Arrays.equals(x, expect)) throw new AssertionError(Arrays.toString(x));
        }
    }
}
```

#### Solution: [Boundary] Empty, Singleton, And Extreme Values (Author exercise)
<!-- id: so-sorted-gap -->

**Approach.**
The method returns 0 for fewer than two values, sorts a copy, and scans adjacent pairs. Each difference is computed as `(long) copy[i] - copy[i - 1]`, so the cast happens before the subtraction and nothing wraps. The invariant after index `i` is that `best` holds the largest gap among the first `i + 1` sorted values. The harness shows that the same difference computed in `int` wraps for the extreme pair.

**Complexity.**
- **Time** is O(n log n), because the sort dominates the linear scan.
- **Space** is O(n), because of the sorted copy.

```java run
import java.util.*;

public final class SortedGap {
    /**
     * Returns the largest gap between adjacent values of the sorted array.
     * Time: O(n log n). Space: O(n).
     * Invariant: after index i, best is the largest gap among copy[0..i].
     */
    static long largestGap(int[] nums) {
        // Fewer than two values have no adjacent pair.
        if (nums.length < 2) return 0;
        int[] copy = Arrays.copyOf(nums, nums.length);
        Arrays.sort(copy);
        long best = 0;
        // The scan visits n - 1 adjacent pairs.
        for (int i = 1; i < copy.length; i++) {
            // The cast to long comes first, so the subtraction cannot wrap.
            best = Math.max(best, (long) copy[i] - copy[i - 1]);
        }
        return best;
    }

    public static void main(String[] args) {
        // The statement examples and the small inputs.
        if (largestGap(new int[] {3, 9, 4}) != 5) throw new AssertionError("example 1");
        if (largestGap(new int[] {Integer.MIN_VALUE, Integer.MAX_VALUE}) != 4294967295L) throw new AssertionError("example 2");
        if (largestGap(new int[0]) != 0 || largestGap(new int[] {7}) != 0) throw new AssertionError("fewer than two");
        // Java fact from the lesson: the same difference in int arithmetic wraps.
        if (Integer.MAX_VALUE - Integer.MIN_VALUE != -1) throw new AssertionError("int wrap");
        // Random arrays with extreme values are checked against an all-pairs oracle.
        Random rnd = new Random(63);
        int[] pool = {Integer.MIN_VALUE, Integer.MAX_VALUE, 0, 1, -1, 5};
        for (int t = 0; t < 500; t++) {
            int[] a = new int[rnd.nextInt(8)];
            for (int k = 0; k < a.length; k++) a[k] = pool[rnd.nextInt(pool.length)];
            long expect = 0;
            for (int x : a) {
                for (int y : a) {
                    if (y > x) {
                        boolean between = false;
                        for (int z : a) if (z > x && z < y) between = true;
                        if (!between) expect = Math.max(expect, (long) y - x);
                    }
                }
            }
            if (largestGap(a) != expect) throw new AssertionError(Arrays.toString(a));
        }
    }
}
```

#### Solution: [Recognize] Smallest Repeated Value (LeetCode 217)
<!-- id: so-smallest-repeat -->

**Approach.**
The method sorts a copy and scans adjacent pairs from the left. Equal values form one contiguous run, so the first pair of equal neighbors belongs to the smallest value that repeats. Any smaller repeated value would have produced an earlier equal pair. The invariant at index `i` is that the values `copy[0..i - 1]` are all distinct from their right neighbors, so none of them repeats. The method returns the boxed value, or `null` when the scan ends.

**Complexity.**
- **Time** is O(n log n), because the sort dominates the linear scan.
- **Space** is O(n), because of the sorted copy.

```java run
import java.util.*;

public final class SmallestRepeat {
    /**
     * Returns the smallest value that occurs at least twice, or null.
     * Time: O(n log n). Space: O(n).
     * Invariant: before index i, no value of copy[0..i - 1] equals its right neighbor.
     */
    static Integer smallestRepeat(int[] nums) {
        int[] copy = Arrays.copyOf(nums, nums.length);
        Arrays.sort(copy);
        // The scan checks n - 1 adjacent pairs.
        for (int i = 1; i < copy.length; i++) {
            // The first equal pair is the smallest repeated value, because equal values are adjacent.
            if (copy[i] == copy[i - 1]) return copy[i];
        }
        // No adjacent pair was equal, so every value is distinct.
        return null;
    }

    public static void main(String[] args) {
        // The statement examples and the empty array.
        if (smallestRepeat(new int[] {7, 3, 7, 3, 9}) != 3) throw new AssertionError("example 1");
        if (smallestRepeat(new int[] {4, -4, 0}) != null) throw new AssertionError("example 2");
        if (smallestRepeat(new int[0]) != null) throw new AssertionError("empty");
        // Random arrays are checked against a counting oracle.
        Random rnd = new Random(64);
        for (int t = 0; t < 500; t++) {
            int[] a = new int[rnd.nextInt(10)];
            for (int k = 0; k < a.length; k++) a[k] = rnd.nextInt(12) - 6;
            Integer expect = null;
            for (int x : a) {
                int c = 0;
                for (int y : a) if (x == y) c++;
                if (c >= 2 && (expect == null || x < expect)) expect = x;
            }
            Integer got = smallestRepeat(a);
            if (!Objects.equals(got, expect)) throw new AssertionError(Arrays.toString(a));
        }
    }
}
```
