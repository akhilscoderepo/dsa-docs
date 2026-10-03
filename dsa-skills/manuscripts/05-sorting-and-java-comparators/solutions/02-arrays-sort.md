<!-- solutions-for: 05-arrays-sort -->
### Arrays Sort

#### Solution: [Build] Sort A Primitive Copy (Author exercise)
<!-- id: so-primitive-copy -->

**Approach.** Copy first with `Arrays.copyOf`, then sort the copy and return it. The argument is never touched, so any other reference to it still sees the original order. The test confirms that the returned array is a different object, that it equals a brute-force sorted version, and that the argument is unchanged, on random arrays that include repeats and the type's extreme values.

**Complexity.** Sorting costs O(n log n) time; the copy needs O(n) extra space.

```java run
import java.util.Arrays;
import java.util.Random;

public final class PrimitiveCopy {
    static int[] sortedCopy(int[] nums) {
        int[] out = Arrays.copyOf(nums, nums.length);
        Arrays.sort(out);
        return out;
    }
    static int[] insertionOracle(int[] nums) {
        int[] a = new int[nums.length];
        int size = 0;
        for (int x : nums) {
            int j = size++;
            while (j > 0 && a[j - 1] > x) { a[j] = a[j - 1]; j--; }
            a[j] = x;
        }
        return a;
    }

    public static void main(String[] args) {
        int[] ex = {6, 2, 9, 2};
        int[] got = sortedCopy(ex);
        if (!Arrays.equals(got, new int[] {2, 2, 6, 9})) throw new AssertionError("example 1");
        if (!Arrays.equals(ex, new int[] {6, 2, 9, 2})) throw new AssertionError("argument changed");
        if (got == ex) throw new AssertionError("must be a different array");
        if (sortedCopy(new int[0]).length != 0) throw new AssertionError("example 2");
        Random rnd = new Random(511);
        for (int t = 0; t < 3000; t++) {
            int n = rnd.nextInt(20);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) {
                int pick = rnd.nextInt(8);
                a[i] = pick == 0 ? Integer.MIN_VALUE : pick == 1 ? Integer.MAX_VALUE : rnd.nextInt(9) - 4;
            }
            int[] keep = a.clone();
            int[] r = sortedCopy(a);
            if (!Arrays.equals(a, keep)) throw new AssertionError("the argument was mutated");
            if (!Arrays.equals(r, insertionOracle(a))) throw new AssertionError("wrong order for " + Arrays.toString(keep));
        }
    }
}
```

#### Solution: [Vary] Sort A Subrange (Author exercise)
<!-- id: so-subrange -->

**Approach.** The library call `Arrays.sort(a, from, to)` orders the positions from `from` up to but not including `to`, so the slice length is `to - from`. Clone the input, apply the call, and return the clone. The test compares with an oracle that extracts the slice, sorts it by insertion and writes it back, over every legal pair of bounds on random arrays. It also confirms that a reversed pair and a pair beyond the end both raise exceptions, and that an empty slice leaves the array unchanged.

**Complexity.** O(k log k) time for a slice of length k, plus O(n) for the clone.

```java run
import java.util.Arrays;
import java.util.Random;

public final class SubrangeSort {
    /** Sorts positions from (inclusive) to to (exclusive) of a copy. */
    static int[] sortSlice(int[] nums, int from, int to) {
        int[] out = nums.clone();
        Arrays.sort(out, from, to);
        return out;
    }
    static int[] oracle(int[] nums, int from, int to) {
        int[] out = nums.clone();
        for (int i = from + 1; i < to; i++) {
            int x = out[i], j = i - 1;
            while (j >= from && out[j] > x) { out[j + 1] = out[j]; j--; }
            out[j + 1] = x;
        }
        return out;
    }

    public static void main(String[] args) {
        if (!Arrays.equals(sortSlice(new int[] {9, 4, 7, 1, 8, 2}, 1, 5), new int[] {9, 1, 4, 7, 8, 2})) throw new AssertionError("example 1");
        if (!Arrays.equals(sortSlice(new int[] {3, 2, 1}, 2, 2), new int[] {3, 2, 1})) throw new AssertionError("example 2");
        boolean reversed = false, beyond = false;
        try { sortSlice(new int[] {1, 2, 3}, 2, 1); } catch (IllegalArgumentException e) { reversed = true; }
        try { sortSlice(new int[] {1, 2, 3}, 0, 4); } catch (ArrayIndexOutOfBoundsException e) { beyond = true; }
        if (!reversed) throw new AssertionError("from > to must throw IllegalArgumentException");
        if (!beyond) throw new AssertionError("to beyond the array must throw ArrayIndexOutOfBoundsException");
        Random rnd = new Random(512);
        for (int t = 0; t < 3000; t++) {
            int n = rnd.nextInt(10);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(7) - 3;
            for (int from = 0; from <= n; from++) {
                for (int to = from; to <= n; to++) {
                    if (!Arrays.equals(sortSlice(a, from, to), oracle(a, from, to))) throw new AssertionError("slice differs: " + Arrays.toString(a) + " " + from + " " + to);
                }
            }
        }
    }
}
```

#### Solution: [Boundary] Empty, Singleton, And Extreme Values (Author exercise)
<!-- id: so-empty-single-extreme -->

**Approach.** Sort a clone with `Arrays.sort`, then verify with a neighbor check that uses `>`. An array of length zero or one has no adjacent pairs, so the check returns true without running its loop. A check written as `a[i] - a[i - 1] >= 0` is wrong at the extremes: for the sorted pair of `Integer.MIN_VALUE` then `Integer.MAX_VALUE` the subtraction wraps to a negative number, so the wrong check rejects a correct order. The program asserts both facts and runs every array of length up to five built from three extreme-ish values.

**Complexity.** O(n log n) time for the sort and O(n) for the check, with O(n) extra space for the clone.

```java run
import java.util.Arrays;

public final class EmptySingleExtreme {
    static int[] sorted(int[] a) { int[] c = a.clone(); Arrays.sort(c); return c; }
    static boolean safeSorted(int[] a) {
        for (int i = 1; i < a.length; i++) if (a[i - 1] > a[i]) return false;
        return true;
    }
    static boolean subtractionSorted(int[] a) {
        for (int i = 1; i < a.length; i++) if (a[i] - a[i - 1] < 0) return false;
        return true;
    }

    public static void main(String[] args) {
        if (!Arrays.equals(sorted(new int[] {Integer.MAX_VALUE, 0, Integer.MIN_VALUE}), new int[] {Integer.MIN_VALUE, 0, Integer.MAX_VALUE})) throw new AssertionError("example 1");
        if (!safeSorted(sorted(new int[0]))) throw new AssertionError("example 2");
        if (!safeSorted(new int[] {42})) throw new AssertionError("a singleton is sorted");
        int[] pair = {Integer.MIN_VALUE, Integer.MAX_VALUE};
        if (!safeSorted(pair)) throw new AssertionError("the safe check accepts the sorted extreme pair");
        if (subtractionSorted(pair)) throw new AssertionError("the subtraction check wrongly rejects it");
        int[] alphabet = {Integer.MIN_VALUE, 0, Integer.MAX_VALUE};
        for (int len = 0; len <= 5; len++) {
            int total = 1;
            for (int i = 0; i < len; i++) total *= 3;
            for (int code = 0; code < total; code++) {
                int[] a = new int[len];
                int c = code;
                for (int i = 0; i < len; i++) { a[i] = alphabet[c % 3]; c /= 3; }
                int[] s = sorted(a);
                if (!safeSorted(s)) throw new AssertionError("not sorted: " + Arrays.toString(s));
                long sumBefore = 0, sumAfter = 0;
                for (int x : a) sumBefore += x;
                for (int x : s) sumAfter += x;
                if (sumBefore != sumAfter || s.length != a.length) throw new AssertionError("sort changed the multiset");
            }
        }
    }
}
```

#### Solution: [Recognize] Contains Duplicate (LeetCode 217)
<!-- id: so-contains-duplicate-sorted -->

**Approach.** Because the contract allows reordering the argument, sort it directly. Equal values then occupy one contiguous run, so a repeat exists exactly when some adjacent pair is equal, and the scan stops at the first such pair. The check compares the answer with an all-pairs oracle on random arrays with small and with huge values, and confirms that the argument really is left in sorted order afterwards, which is the price of the in-place contract.

**Complexity.** O(n log n) time dominated by the sort, and O(1) extra space beyond what the sort uses.

```java run
import java.util.Arrays;
import java.util.Random;

public final class ContainsDuplicateSorted {
    static boolean containsDuplicate(int[] nums) {
        Arrays.sort(nums);                       // contract: the argument may be reordered
        for (int i = 1; i < nums.length; i++) {
            if (nums[i] == nums[i - 1]) return true;
        }
        return false;
    }
    static boolean oracle(int[] nums) {
        for (int i = 0; i < nums.length; i++)
            for (int j = i + 1; j < nums.length; j++)
                if (nums[i] == nums[j]) return true;
        return false;
    }

    public static void main(String[] args) {
        if (!containsDuplicate(new int[] {7, 3, 8, 3})) throw new AssertionError("example 1");
        if (containsDuplicate(new int[] {4, 9, 1, 6})) throw new AssertionError("example 2");
        if (containsDuplicate(new int[] {5})) throw new AssertionError("a single value has no repeat");
        if (!containsDuplicate(new int[] {1000000000, -1000000000, 1000000000})) throw new AssertionError("large values");
        Random rnd = new Random(513);
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(12);
            int range = rnd.nextBoolean() ? 6 : 1000000;
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(range) - range / 2;
            int[] copy = a.clone();
            boolean got = containsDuplicate(a);
            if (got != oracle(copy)) throw new AssertionError("disagrees with the pair oracle on " + Arrays.toString(copy));
            for (int i = 1; i < a.length; i++) if (a[i - 1] > a[i]) throw new AssertionError("the argument should end up sorted");
        }
    }
}
```
