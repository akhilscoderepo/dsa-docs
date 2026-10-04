<!-- solutions-for: 05-sorting-and-java-comparators -->
### Solutions For Safe Comparison

#### Solution: [Build] Sort An Array (LeetCode 912)
<!-- id: so-sort-array -->

**Approach.**
The method copies the input and sorts the copy with a merge sort that makes its order decision through `Integer.compare`. The recursion splits a range in halves, sorts each half, and merges them. The invariant of the merge is that the output prefix holds the smallest values of both halves in nondecreasing order. The merge takes from the left half on a tie, so equal values keep their order. The harness asserts that the subtraction rule gives a wrong sign for the extreme pair, which is the failure that the lesson describes.

**Complexity.**
- **Time** is O(n log n), because the recursion has about log n levels and each level merges n values with one comparison per moved value.
- **Space** is O(n), because the merge writes into one buffer of length n next to the copy.

```java run
import java.util.*;

public final class SortArray {
    /**
     * Returns a sorted copy of nums.
     * Time: O(n log n). Space: O(n).
     * Invariant: after merge(lo, mid, hi), a[lo..hi) is nondecreasing.
     */
    static int[] sortArray(int[] nums) {
        // The copy keeps the caller's array unchanged.
        int[] a = Arrays.copyOf(nums, nums.length);
        sort(a, new int[a.length], 0, a.length);
        return a;
    }

    static void sort(int[] a, int[] buf, int lo, int hi) {
        // A range of length 0 or 1 is sorted already.
        if (hi - lo < 2) return;
        int mid = (lo + hi) >>> 1;
        sort(a, buf, lo, mid);
        sort(a, buf, mid, hi);
        int i = lo, j = mid, k = lo;
        // Each iteration moves one value to buf, so the loop runs hi - lo times.
        while (i < mid || j < hi) {
            // Take from the left on a tie so that equal values keep their order.
            if (j >= hi || (i < mid && Integer.compare(a[i], a[j]) <= 0)) buf[k++] = a[i++];
            else buf[k++] = a[j++];
        }
        // Copying the range back costs hi - lo writes.
        System.arraycopy(buf, lo, a, lo, hi - lo);
    }

    public static void main(String[] args) {
        // The statement examples and the empty array.
        if (!Arrays.equals(sortArray(new int[] {5, -3, 9, -3, 0}), new int[] {-3, -3, 0, 5, 9})) throw new AssertionError("example 1");
        if (!Arrays.equals(sortArray(new int[] {Integer.MAX_VALUE, Integer.MIN_VALUE, 0}), new int[] {Integer.MIN_VALUE, 0, Integer.MAX_VALUE})) throw new AssertionError("example 2");
        if (sortArray(new int[0]).length != 0) throw new AssertionError("empty");
        // The input array keeps its contents.
        int[] in = {3, 1, 2};
        sortArray(in);
        if (!Arrays.equals(in, new int[] {3, 1, 2})) throw new AssertionError("input mutated");
        // Java fact from the lesson: subtraction wraps for the extreme pair, so its sign is wrong.
        if (!(2000000000 - -2000000000 < 0)) throw new AssertionError("subtraction wraps");
        if (Integer.compare(2000000000, -2000000000) <= 0) throw new AssertionError("compare sign");
        // Random arrays with extreme values are checked against Arrays.sort.
        Random rnd = new Random(51);
        int[] pool = {Integer.MIN_VALUE, Integer.MAX_VALUE, 0, -1, 1, 7, 7};
        for (int t = 0; t < 500; t++) {
            int[] a = new int[rnd.nextInt(12)];
            for (int k = 0; k < a.length; k++) a[k] = rnd.nextBoolean() ? pool[rnd.nextInt(pool.length)] : rnd.nextInt(20) - 10;
            int[] expect = a.clone();
            Arrays.sort(expect);
            if (!Arrays.equals(sortArray(a), expect)) throw new AssertionError(Arrays.toString(a));
        }
    }
}
```

#### Solution: [Vary] Sort Boxed Integers In Descending Order (Author exercise)
<!-- id: so-descending-boxed -->

**Approach.**
The method calls the `Arrays.sort` overload that takes a comparator and passes the arguments of `Integer.compare` in reverse order. Swapping the arguments reverses the ranking and cannot overflow, while negating a result fails for `Integer.MIN_VALUE`. The invariant after the call is that every adjacent pair `values[i]`, `values[i + 1]` satisfies `values[i] >= values[i + 1]`. The harness asserts through reflection that no overload of `Arrays.sort` accepts both an `int[]` and a comparator.

**Complexity.**
- **Time** is O(n log n), because the library sort makes that many comparisons and each takes constant time.
- **Space** is O(n) for the working buffer that the object sort uses in the worst case.

```java run
import java.util.*;

public final class DescendingBoxed {
    /**
     * Sorts values in place, largest first.
     * Time: O(n log n). Space: O(n) worst case for the library buffer.
     * Invariant: after the call, values[i] >= values[i + 1] for every adjacent pair.
     */
    static void sortDescending(Integer[] values) {
        // Swapped arguments reverse the ranking without arithmetic on the values.
        Arrays.sort(values, (a, b) -> Integer.compare(b, a));
    }

    public static void main(String[] args) throws Exception {
        // The statement examples.
        Integer[] e1 = {3, 9, 1, 9};
        sortDescending(e1);
        if (!Arrays.equals(e1, new Integer[] {9, 9, 3, 1})) throw new AssertionError("example 1");
        Integer[] e2 = {Integer.MIN_VALUE, Integer.MAX_VALUE};
        sortDescending(e2);
        if (!Arrays.equals(e2, new Integer[] {Integer.MAX_VALUE, Integer.MIN_VALUE})) throw new AssertionError("example 2");
        // Java fact from the lesson: no overload takes int[] together with a comparator.
        boolean found = false;
        for (var m : Arrays.class.getMethods()) {
            if (m.getName().equals("sort") && m.getParameterCount() >= 2
                    && m.getParameterTypes()[0] == int[].class
                    && Arrays.asList(m.getParameterTypes()).contains(Comparator.class)) found = true;
        }
        if (found) throw new AssertionError("int[] comparator overload");
        // Java fact from the lesson: negating the minimum value returns the minimum value.
        if (-Integer.MIN_VALUE != Integer.MIN_VALUE) throw new AssertionError("negation");
        // Random arrays are checked against a sort and reverse.
        Random rnd = new Random(52);
        for (int t = 0; t < 500; t++) {
            Integer[] a = new Integer[rnd.nextInt(10)];
            for (int k = 0; k < a.length; k++) a[k] = rnd.nextInt(5) == 0 ? Integer.MIN_VALUE : rnd.nextInt(9) - 4;
            Integer[] expect = a.clone();
            Arrays.sort(expect);
            Collections.reverse(Arrays.asList(expect));
            sortDescending(a);
            if (!Arrays.equals(a, expect)) throw new AssertionError(Arrays.toString(a));
        }
    }
}
```

#### Solution: [Boundary] Extreme Comparator (Author exercise)
<!-- id: so-extreme-comparator -->

**Approach.**
The method uses the comparison operators `<` and `>` and maps their results to -1, 0 and 1. Comparison operators read the two values and never form a difference, so no pair can wrap. The invariant is that the result is the sign of the mathematical difference for every pair. The harness checks all nine pairs of the three extreme values and shows that the subtraction rule disagrees on the pair of `Integer.MIN_VALUE` and `Integer.MAX_VALUE`.

**Complexity.**
- **Time** is O(1), because the method makes at most two comparisons.
- **Space** is O(1), because the method stores no extra values.

```java run
public final class ExtremeComparator {
    /**
     * Returns -1, 0 or 1 for a compared with b.
     * Time: O(1). Space: O(1).
     * Invariant: the result equals the sign of the true difference a - b.
     */
    static int sign(int a, int b) {
        // The operators never produce a difference, so nothing wraps.
        if (a < b) return -1;
        if (a > b) return 1;
        // Neither operator held, so the values are equal.
        return 0;
    }

    public static void main(String[] args) {
        // The statement examples.
        if (sign(Integer.MIN_VALUE, Integer.MAX_VALUE) != -1) throw new AssertionError("example 1");
        if (sign(Integer.MAX_VALUE, Integer.MAX_VALUE) != 0) throw new AssertionError("example 2");
        // All pairs of the extreme values are checked against long arithmetic, which cannot wrap here.
        int[] pool = {Integer.MIN_VALUE, -1, 0, 1, Integer.MAX_VALUE};
        for (int a : pool) {
            for (int b : pool) {
                long diff = (long) a - b;
                int expect = diff < 0 ? -1 : (diff > 0 ? 1 : 0);
                if (sign(a, b) != expect) throw new AssertionError(a + " " + b);
            }
        }
        // Java facts from the lesson: subtraction gives the wrong sign for this pair.
        if (Integer.signum(Integer.MIN_VALUE - Integer.MAX_VALUE) != 1) throw new AssertionError("subtraction wraps");
        if (Integer.signum(Integer.compare(Integer.MIN_VALUE, Integer.MAX_VALUE)) != -1) throw new AssertionError("compare");
    }
}
```

#### Solution: [Recognize] Largest Number (LeetCode 179)
<!-- id: so-largest-number -->

**Approach.**
The method turns each value into a string and sorts the strings with a comparator that puts `x` before `y` when `x + y` is larger than `y + x`. Both concatenations have the same length, so comparing them as strings equals comparing them as numbers. The relation is a total order, because it equals the numeric order of the concatenation, which is transitive. After the sort, no adjacent pair can gain by swapping, and the concatenation is maximal. An all-zero input produces a string that starts with `0`, so the method returns `"0"` in that case.

**Complexity.**
- **Time** is O(n log n * L), where L is the length of the longest decimal string, because each of the O(n log n) comparisons builds and compares strings of length up to 2L.
- **Space** is O(n * L) for the strings.

```java run
import java.util.*;

public final class LargestNumber {
    /**
     * Returns the largest number formed by concatenating all values.
     * Time: O(n log n * L). Space: O(n * L).
     * Invariant: after the sort, for every adjacent pair x, y the string x + y >= y + x.
     */
    static String largestNumber(int[] nums) {
        String[] s = new String[nums.length];
        for (int i = 0; i < nums.length; i++) s[i] = Integer.toString(nums[i]);
        // The larger concatenation decides which string goes first.
        Arrays.sort(s, (x, y) -> (y + x).compareTo(x + y));
        // A leading zero means that every value is zero.
        if (s[0].equals("0")) return "0";
        StringBuilder sb = new StringBuilder();
        for (String t : s) sb.append(t);
        return sb.toString();
    }

    /** Oracle: tries every permutation and keeps the largest string of equal length. */
    static String brute(int[] nums) {
        String[] best = {""};
        permute(nums, 0, best);
        return best[0].startsWith("0") ? "0" : best[0];
    }

    static void permute(int[] a, int k, String[] best) {
        if (k == a.length) {
            StringBuilder sb = new StringBuilder();
            for (int v : a) sb.append(v);
            String t = sb.toString();
            if (best[0].isEmpty() || t.compareTo(best[0]) > 0) best[0] = t;
            return;
        }
        for (int i = k; i < a.length; i++) {
            int tmp = a[k]; a[k] = a[i]; a[i] = tmp;
            permute(a, k + 1, best);
            tmp = a[k]; a[k] = a[i]; a[i] = tmp;
        }
    }

    public static void main(String[] args) {
        // The statement examples.
        if (!largestNumber(new int[] {3, 30, 34, 5, 9}).equals("9534330")) throw new AssertionError("example 1");
        if (!largestNumber(new int[] {0, 0}).equals("0")) throw new AssertionError("example 2");
        // Java fact from the lesson: numeric order and concatenation order disagree.
        if (!(("3" + "30").compareTo("30" + "3") > 0)) throw new AssertionError("concatenation order");
        // Random arrays are checked against the permutation oracle.
        Random rnd = new Random(53);
        for (int t = 0; t < 400; t++) {
            int[] a = new int[1 + rnd.nextInt(5)];
            for (int k = 0; k < a.length; k++) a[k] = rnd.nextInt(4) == 0 ? 0 : rnd.nextInt(130);
            String expect = brute(a.clone());
            if (!largestNumber(a).equals(expect)) throw new AssertionError(Arrays.toString(a));
        }
    }
}
```
