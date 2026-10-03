<!-- solutions-for: 07-range-queries -->
### Range Queries

#### Solution: [Build] Range Sum Query - Immutable (LeetCode 303)
<!-- id: ps-range-immutable -->

**Approach.** The constructor builds a table with one more slot than the array, where slot `i` holds the sum of the first `i` values. A request for positions `left` through `right` is the table at `right + 1` minus the table at `left`, since every value before `left` is counted in both slots and cancels. No request touches the array again. The oracle adds the values of each stretch directly, and the program also checks the two examples and a stretch with a single value.

**Complexity.** Setup is O(n) time and n + 1 slots of space, and each request is O(1).

```java run
import java.util.Random;

public final class RangeImmutable {
    static final class NumArray {
        private final long[] prefix;
        NumArray(int[] nums) {
            prefix = new long[nums.length + 1];
            for (int i = 0; i < nums.length; i++) prefix[i + 1] = prefix[i] + nums[i];
        }
        int sumRange(int left, int right) { return (int) (prefix[right + 1] - prefix[left]); }
    }

    public static void main(String[] args) {
        NumArray na = new NumArray(new int[] {4, -3, 6, 2, 8});
        if (na.sumRange(1, 3) != 5) throw new AssertionError("example 1");
        if (na.sumRange(0, 4) != 17) throw new AssertionError("example 2");
        if (na.sumRange(2, 2) != 6) throw new AssertionError("a single value");
        Random rnd = new Random(7201);
        for (int t = 0; t < 2000; t++) {
            int n = 1 + rnd.nextInt(10);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(200001) - 100000;
            NumArray x = new NumArray(a);
            for (int l = 0; l < n; l++)
                for (int r = l; r < n; r++) {
                    int s = 0;
                    for (int k = l; k <= r; k++) s += a[k];
                    if (x.sumRange(l, r) != s) throw new AssertionError("differs for " + l + "," + r);
                }
        }
    }
}
```

#### Solution: [Vary] Half-Open Query (Author exercise)
<!-- id: ps-half-open-query -->

**Approach.** When the right end is excluded, the values before it are all the values in the first `right` positions, which is slot `right` of the table. The values before `left` are slot `left`. The answer is `prefix[right] - prefix[left]`, with no shift, and the right end may equal the length of the array, since the table has a slot for it. A request with equal ends reads the same slot twice and returns zero, which is the right answer for an empty stretch and needs no branch. The program compares both conventions on every pair of ends against a direct sum.

**Complexity.** O(n) setup and O(1) per request.

```java run
import java.util.Random;

public final class HalfOpenQuery {
    static long[] build(int[] a) {
        long[] p = new long[a.length + 1];
        for (int i = 0; i < a.length; i++) p[i + 1] = p[i] + a[i];
        return p;
    }
    static long halfOpen(long[] p, int left, int right) { return p[right] - p[left]; }
    static long inclusive(long[] p, int left, int right) { return p[right + 1] - p[left]; }

    public static void main(String[] args) {
        long[] p = build(new int[] {4, -3, 6, 2, 8});
        if (halfOpen(p, 1, 4) != 5) throw new AssertionError("example 1");
        if (halfOpen(p, 3, 3) != 0) throw new AssertionError("example 2");
        if (halfOpen(p, 0, 5) != 17) throw new AssertionError("right end equal to the length");
        Random rnd = new Random(7202);
        for (int t = 0; t < 2000; t++) {
            int n = 1 + rnd.nextInt(10);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(2001) - 1000;
            long[] q = build(a);
            for (int l = 0; l <= n; l++)
                for (int r = l; r <= n; r++) {
                    long s = 0;
                    for (int k = l; k < r; k++) s += a[k];
                    if (halfOpen(q, l, r) != s) throw new AssertionError("half-open differs for " + l + "," + r);
                    if (r > l && inclusive(q, l, r - 1) != s) throw new AssertionError("conventions disagree for " + l + "," + r);
                }
        }
    }
}
```

#### Solution: [Boundary] Whole Array (Author exercise)
<!-- id: ps-whole-array -->

**Approach.** A request starting at position zero reads slot zero, which is the sentinel and holds zero, so nothing before the first value is read. A request ending at position `n - 1` reads slot `n`, the final slot of the table, which exists because the table has `n + 1` entries. Both ends of the array therefore need no branch. The totals can reach `n` times a billion, so the table holds `long` values, and the program shows that an `int` table wraps on the first example. The oracle sums the stretch directly with a `long` accumulator.

**Complexity.** O(n) setup and O(1) per request.

```java run
import java.util.Random;

public final class WholeArray {
    static long[] build(int[] a) {
        long[] p = new long[a.length + 1];
        for (int i = 0; i < a.length; i++) p[i + 1] = p[i] + a[i];
        return p;
    }
    static long query(long[] p, int left, int right) { return p[right + 1] - p[left]; }
    static int[] wrappedTable(int[] a) {
        int[] p = new int[a.length + 1];
        for (int i = 0; i < a.length; i++) p[i + 1] = p[i] + a[i];
        return p;
    }

    public static void main(String[] args) {
        int[] big = {1000000000, 1000000000, 1000000000};
        long[] p = build(big);
        if (query(p, 0, 2) != 3000000000L) throw new AssertionError("example 1");
        if (wrappedTable(big)[3] == 3000000000L) throw new AssertionError("an int table should wrap");
        if (query(build(new int[] {5}), 0, 0) != 5) throw new AssertionError("example 2");
        if (p[0] != 0) throw new AssertionError("the sentinel must be zero");
        Random rnd = new Random(7203);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(8);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(2000000001) - 1000000000;
            long[] q = build(a);
            long total = 0;
            for (int x : a) total += x;
            if (query(q, 0, n - 1) != total) throw new AssertionError("whole array differs");
            if (query(q, 0, 0) != a[0]) throw new AssertionError("first value differs");
            if (query(q, n - 1, n - 1) != a[n - 1]) throw new AssertionError("last value differs");
        }
    }
}
```

#### Solution: [Recognize] XOR Queries of a Subarray (LeetCode 1310)
<!-- id: ps-xor-queries-intro -->

**Approach.** The table stores, in slot `i`, the XOR of the first `i` values, with slot zero holding zero because XOR with zero changes nothing. XOR of any value with itself is zero, so XOR of slot `right + 1` with slot `left` leaves exactly the values from `left` through `right`: the early part appears in both slots and cancels. XOR plays the role of subtraction because it is its own inverse. The oracle XORs the stretch value by value for each request.

**Complexity.** O(n) setup and O(1) per request, with n + 1 slots of space.

```java run
import java.util.Arrays;
import java.util.Random;

public final class XorQueriesIntro {
    static int[] xorQueries(int[] arr, int[][] queries) {
        int[] prefix = new int[arr.length + 1];
        for (int i = 0; i < arr.length; i++) prefix[i + 1] = prefix[i] ^ arr[i];
        int[] out = new int[queries.length];
        for (int i = 0; i < queries.length; i++) out[i] = prefix[queries[i][1] + 1] ^ prefix[queries[i][0]];
        return out;
    }
    static int[] oracle(int[] arr, int[][] queries) {
        int[] out = new int[queries.length];
        for (int i = 0; i < queries.length; i++) {
            int x = 0;
            for (int k = queries[i][0]; k <= queries[i][1]; k++) x ^= arr[k];
            out[i] = x;
        }
        return out;
    }

    public static void main(String[] args) {
        int[] arr = {6, 2, 7, 4};
        if (xorQueries(arr, new int[][] {{1, 3}})[0] != 1) throw new AssertionError("example 1");
        if (xorQueries(arr, new int[][] {{0, 0}})[0] != 6) throw new AssertionError("example 2");
        if (xorQueries(arr, new int[][] {{0, 3}})[0] != (6 ^ 2 ^ 7 ^ 4)) throw new AssertionError("whole array");
        Random rnd = new Random(7204);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(10);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(1000000001);
            int q = 1 + rnd.nextInt(6);
            int[][] qs = new int[q][2];
            for (int i = 0; i < q; i++) { int l = rnd.nextInt(n); int r = l + rnd.nextInt(n - l); qs[i][0] = l; qs[i][1] = r; }
            if (!Arrays.equals(xorQueries(a, qs), oracle(a, qs))) throw new AssertionError("differs on " + Arrays.toString(a));
        }
    }
}
```
