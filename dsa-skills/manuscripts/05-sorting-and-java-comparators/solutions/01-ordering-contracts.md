<!-- solutions-for: 05-ordering-contracts -->
### Ordering Contracts

#### Solution: [Build] Sort an Array (LeetCode 912)
<!-- id: so-sort-an-array -->

**Approach.** The required order is nondecreasing, and equal values may appear in either order because they cannot be told apart. Clone the argument, sort the clone with `Arrays.sort`, and return it, so the caller's array is untouched. The check compares against a selection-sort oracle on random arrays and also asserts that the input array still holds its original contents after the call.

**Complexity.** O(n log n) time and O(n) extra space for the copy.

```java run
import java.util.Arrays;
import java.util.Random;

public final class SortAnArray {
    static int[] sortArray(int[] nums) {
        int[] copy = nums.clone();
        Arrays.sort(copy);
        return copy;
    }
    static int[] oracle(int[] nums) {
        int[] a = nums.clone();
        for (int i = 0; i < a.length; i++) {
            int m = i;
            for (int j = i + 1; j < a.length; j++) if (a[j] < a[m]) m = j;
            int t = a[i]; a[i] = a[m]; a[m] = t;
        }
        return a;
    }

    public static void main(String[] args) {
        if (!Arrays.equals(sortArray(new int[] {5, 2, 3, 1}), new int[] {1, 2, 3, 5})) throw new AssertionError("example 1");
        if (!Arrays.equals(sortArray(new int[] {4, -1, 4, 0, -1}), new int[] {-1, -1, 0, 4, 4})) throw new AssertionError("example 2");
        if (sortArray(new int[] {7}).length != 1) throw new AssertionError("singleton");
        Random rnd = new Random(501);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(30);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(41) - 20;
            int[] before = a.clone();
            int[] got = sortArray(a);
            if (!Arrays.equals(got, oracle(a))) throw new AssertionError("differs from the selection-sort oracle: " + Arrays.toString(before));
            if (!Arrays.equals(a, before)) throw new AssertionError("the caller's array was mutated");
        }
    }
}
```

#### Solution: [Vary] Sort Boxed Integers in Descending Order (Author exercise)
<!-- id: so-boxed-descending -->

**Approach.** A comparator that returns `Integer.compare(y, x)` reverses the natural order, because it swaps the roles of the two arguments. It is applied to an `Integer[]`, since the comparator overloads of `Arrays.sort` take an object array. The program scans the public `sort` methods by reflection to show that none accepts an `int[]` together with a `Comparator`, and it checks the result against a brute-force oracle that repeatedly extracts the maximum, including arrays that hold both extreme ints.

**Complexity.** O(n log n) time and O(1) extra space beyond the boxed array.

```java run
import java.lang.reflect.Method;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Comparator;
import java.util.List;
import java.util.Random;

public final class BoxedDescending {
    static void sortDescending(Integer[] values) {
        Arrays.sort(values, (x, y) -> Integer.compare(y, x));
    }
    static Integer[] oracle(Integer[] values) {
        List<Integer> pool = new ArrayList<>(Arrays.asList(values));
        Integer[] out = new Integer[values.length];
        for (int i = 0; i < out.length; i++) {
            int best = 0;
            for (int j = 1; j < pool.size(); j++) if (pool.get(j) > pool.get(best)) best = j;
            out[i] = pool.remove(best);
        }
        return out;
    }

    public static void main(String[] args) {
        Integer[] a = {3, 9, 1, 9};
        sortDescending(a);
        if (!Arrays.equals(a, new Integer[] {9, 9, 3, 1})) throw new AssertionError("example 1");
        Integer[] b = {-5, 0, 7};
        sortDescending(b);
        if (!Arrays.equals(b, new Integer[] {7, 0, -5})) throw new AssertionError("example 2");
        Integer[] empty = {};
        sortDescending(empty);
        boolean primitiveWithComparator = false, objectWithComparator = false;
        for (Method m : Arrays.class.getMethods()) {
            if (!m.getName().equals("sort")) continue;
            Class<?>[] p = m.getParameterTypes();
            if (p.length == 2 && p[1] == Comparator.class) {
                if (p[0] == int[].class) primitiveWithComparator = true;
                if (p[0] == Object[].class) objectWithComparator = true;
            }
        }
        if (primitiveWithComparator) throw new AssertionError("int[] must have no comparator overload");
        if (!objectWithComparator) throw new AssertionError("Object[] has a comparator overload");
        Integer[] edge = {Integer.MIN_VALUE, Integer.MAX_VALUE, 0, -1};
        sortDescending(edge);
        if (!Arrays.equals(edge, new Integer[] {Integer.MAX_VALUE, 0, -1, Integer.MIN_VALUE})) throw new AssertionError("extremes");
        Random rnd = new Random(502);
        for (int t = 0; t < 3000; t++) {
            int n = rnd.nextInt(15);
            Integer[] v = new Integer[n];
            for (int i = 0; i < n; i++) v[i] = rnd.nextInt(5) == 0 ? (rnd.nextBoolean() ? Integer.MAX_VALUE : Integer.MIN_VALUE) : rnd.nextInt(11) - 5;
            Integer[] expected = oracle(v);
            sortDescending(v);
            if (!Arrays.equals(v, expected)) throw new AssertionError("differs from the oracle: " + Arrays.toString(expected));
        }
    }
}
```

#### Solution: [Boundary] Extreme Comparator (Author exercise)
<!-- id: so-extreme-comparator -->

**Approach.** The safe comparator is `Integer.compare`, which returns the sign without computing a difference. The unsafe one, `a - b`, wraps when the true difference exceeds 32 bits. For the pair of the minimum and the maximum, the true difference is about minus 4.29 billion, which wraps to positive 1, so the unsafe comparator ranks the minimum after the maximum. The program tries all six arrangements of the three values and shows the safe result is always minimum, zero, maximum. It then confirms by brute force over a grid of extreme-ish values that the unsafe sign disagrees with the true sign for exactly those pairs whose difference overflows.

**Complexity.** O(1) for the fixed three values; the grid check is O(k^2) for k probe values.

```java run
import java.util.Arrays;
import java.util.Comparator;

public final class ExtremeComparator {
    static final Comparator<Integer> SAFE = (a, b) -> Integer.compare(a, b);
    static final Comparator<Integer> UNSAFE = (a, b) -> a - b;

    static void permute(Integer[] a, int k, java.util.List<Integer[]> out) {
        if (k == a.length) { out.add(a.clone()); return; }
        for (int i = k; i < a.length; i++) {
            Integer t = a[k]; a[k] = a[i]; a[i] = t;
            permute(a, k + 1, out);
            t = a[k]; a[k] = a[i]; a[i] = t;
        }
    }

    public static void main(String[] args) {
        Integer[] want = {Integer.MIN_VALUE, 0, Integer.MAX_VALUE};
        java.util.List<Integer[]> all = new java.util.ArrayList<>();
        permute(new Integer[] {Integer.MIN_VALUE, 0, Integer.MAX_VALUE}, 0, all);
        if (all.size() != 6) throw new AssertionError("six arrangements");
        for (Integer[] p : all) {
            Arrays.sort(p, SAFE);
            if (!Arrays.equals(p, want)) throw new AssertionError("safe compare failed on " + Arrays.toString(p));
        }
        if (Integer.MIN_VALUE - Integer.MAX_VALUE != 1) throw new AssertionError("the difference wraps to 1");
        if (UNSAFE.compare(Integer.MIN_VALUE, Integer.MAX_VALUE) <= 0) throw new AssertionError("subtraction claims MIN is not smaller than MAX");
        if (SAFE.compare(Integer.MIN_VALUE, Integer.MAX_VALUE) >= 0) throw new AssertionError("safe compare says MIN is smaller");
        int[] probes = {Integer.MIN_VALUE, Integer.MIN_VALUE + 1, -1, 0, 1, Integer.MAX_VALUE - 1, Integer.MAX_VALUE};
        for (int x : probes) {
            for (int y : probes) {
                long trueDiff = (long) x - (long) y;
                boolean overflows = trueDiff > Integer.MAX_VALUE || trueDiff < Integer.MIN_VALUE;
                boolean signWrong = Integer.signum(x - y) != Long.signum(trueDiff);
                if (signWrong != overflows) throw new AssertionError("the sign is wrong exactly when the difference overflows: " + x + "," + y);
                if (Integer.signum(SAFE.compare(x, y)) != Long.signum(trueDiff)) throw new AssertionError("safe compare wrong on " + x + "," + y);
            }
        }
    }
}
```

#### Solution: [Recognize] Largest Number (LeetCode 179)
<!-- id: so-largest-number -->

**Approach.** Numeric order fails because 8 is larger than 81 as a number, yet `"881"` beats `"818"`. Sort the decimal strings so that `x` precedes `y` when `x + y` is lexicographically larger than `y + x`. Because the two concatenations have equal length, string comparison and numeric comparison agree. After sorting, a leading `"0"` means every piece is zero and the answer is `"0"`. The oracle tries every permutation for up to six pieces and keeps the lexicographically largest joined string, which is also the numerically largest because all permutations have the same length.

**Complexity.** O(n log n) comparisons, each over strings of at most 20 characters, so O(n log n) time with the bound on number length; O(n) extra space.

```java run
import java.util.Arrays;
import java.util.Random;

public final class LargestNumber {
    static String largestNumber(int[] nums) {
        String[] parts = new String[nums.length];
        for (int i = 0; i < nums.length; i++) parts[i] = Integer.toString(nums[i]);
        Arrays.sort(parts, (x, y) -> (y + x).compareTo(x + y));
        if (parts[0].equals("0")) return "0";
        return String.join("", parts);
    }
    static String best;
    static void permute(String[] p, int k) {
        if (k == p.length) {
            String s = String.join("", p);
            if (best == null || s.compareTo(best) > 0) best = s;
            return;
        }
        for (int i = k; i < p.length; i++) {
            String t = p[k]; p[k] = p[i]; p[i] = t;
            permute(p, k + 1);
            t = p[k]; p[k] = p[i]; p[i] = t;
        }
    }
    static String oracle(int[] nums) {
        String[] p = new String[nums.length];
        for (int i = 0; i < p.length; i++) p[i] = Integer.toString(nums[i]);
        best = null;
        permute(p, 0);
        return best.charAt(0) == '0' ? "0" : best;
    }

    public static void main(String[] args) {
        if (!largestNumber(new int[] {8, 81, 80}).equals("88180")) throw new AssertionError("example 1");
        if (!largestNumber(new int[] {0, 0, 0}).equals("0")) throw new AssertionError("example 2");
        if (!largestNumber(new int[] {3, 30, 34, 5, 9}).equals("9534330")) throw new AssertionError("the classic case");
        if (!largestNumber(new int[] {1000000000, 999999999}).equals("9999999991000000000")) throw new AssertionError("large pieces");
        if (!largestNumber(new int[] {7}).equals("7")) throw new AssertionError("single piece");
        Random rnd = new Random(503);
        int[] pool = {0, 1, 2, 3, 9, 10, 11, 12, 30, 34, 90, 91, 100, 121, 129, 999};
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(6);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = pool[rnd.nextInt(pool.length)];
            if (!largestNumber(a).equals(oracle(a))) throw new AssertionError("disagrees with the permutation oracle on " + Arrays.toString(a));
        }
    }
}
```
