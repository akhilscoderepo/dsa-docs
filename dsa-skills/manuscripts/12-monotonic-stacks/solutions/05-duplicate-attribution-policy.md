<!-- solutions-for: 05-duplicate-attribution-policy -->
### Duplicate-Attribution Policy

#### Solution: [Build] Two Equal Minima Ownership (Author exercise)
<!-- id: ms-two-equal-minima -->

**Approach.** For each starting index, extend the end one step at a time and keep the owner as the last index that has held the running minimum, which means the owner moves to the new end whenever the new value is smaller than or equal to the owner's value. Each extension adds one to the owner's count. A stretch containing two equal minima therefore goes to the later one, and every stretch is counted once. The assertions check both examples, check that the counts add up to `n * (n + 1) / 2`, and compare with a second method that fixes both ends and searches the stretch for its last minimum.

**Complexity.** O(n^2) time and O(n) extra space, which is what this first rung allows.

```java run
import java.util.Arrays;
import java.util.Random;

public final class TwoEqualMinima {
    static long[] owned(int[] a) {
        int n = a.length;
        long[] owned = new long[n];
        for (int start = 0; start < n; start++) {
            int owner = start;
            for (int end = start; end < n; end++) {
                if (a[end] <= a[owner]) owner = end;
                owned[owner]++;
            }
        }
        return owned;
    }
    static long[] oracle(int[] a) {
        int n = a.length;
        long[] owned = new long[n];
        for (int lo = 0; lo < n; lo++)
            for (int hi = lo; hi < n; hi++) {
                int min = Integer.MAX_VALUE;
                for (int k = lo; k <= hi; k++) min = Math.min(min, a[k]);
                int last = -1;
                for (int k = lo; k <= hi; k++) if (a[k] == min) last = k;
                owned[last]++;
            }
        return owned;
    }

    public static void main(String[] args) {
        if (!Arrays.equals(owned(new int[]{2, 2}), new long[]{1, 2})) throw new AssertionError("example 1");
        if (!Arrays.equals(owned(new int[]{3, 1, 3, 1}), new long[]{1, 4, 1, 4})) throw new AssertionError("example 2");
        Random rnd = new Random(1501);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(10);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(4);
            long[] got = owned(a);
            if (!Arrays.equals(got, oracle(a))) throw new AssertionError("disagrees with the search method on " + Arrays.toString(a));
            long sum = Arrays.stream(got).sum();
            if (sum != (long) n * (n + 1) / 2) throw new AssertionError("every subarray must have exactly one owner");
        }
    }
}
```

#### Solution: [Vary] Strict Left, Non-Strict Right (Author exercise)
<!-- id: ms-strict-left-nonstrict-right -->

**Approach.** Run one forward scan that removes every stack top whose value is at least the current value. A removed index meets a later value that is smaller or equal, so the current index is its right wall. After the removals, the top is strictly smaller than the current value, so it is the left wall. Indices never removed keep the right sentinel `n`, and an empty stack gives the left sentinel -1. The assertions compare with an outward walk that applies the two comparisons literally, on arrays with many ties, and check both examples.

**Complexity.** O(n) time and O(n) extra space.

```java run
import java.util.ArrayDeque;
import java.util.Arrays;
import java.util.Random;

public final class StrictLeftNonStrictRight {
    static int[][] walls(int[] a) {
        int n = a.length;
        int[][] w = new int[n][2];
        for (int i = 0; i < n; i++) w[i][1] = n;
        ArrayDeque<Integer> stack = new ArrayDeque<>();
        for (int j = 0; j < n; j++) {
            while (!stack.isEmpty() && a[stack.peekLast()] >= a[j]) w[stack.removeLast()][1] = j;
            w[j][0] = stack.isEmpty() ? -1 : stack.peekLast();
            stack.addLast(j);
        }
        return w;
    }
    static int[][] oracle(int[] a) {
        int n = a.length;
        int[][] w = new int[n][2];
        for (int i = 0; i < n; i++) {
            int l = i - 1;
            while (l >= 0 && !(a[l] < a[i])) l--;
            int r = i + 1;
            while (r < n && !(a[r] <= a[i])) r++;
            w[i][0] = l;
            w[i][1] = r;
        }
        return w;
    }

    public static void main(String[] args) {
        if (!Arrays.deepEquals(walls(new int[]{3, 1, 3, 1}), new int[][]{{-1, 1}, {-1, 3}, {1, 3}, {-1, 4}})) throw new AssertionError("example 1");
        if (!Arrays.deepEquals(walls(new int[]{2, 2, 1, 2}), new int[][]{{-1, 1}, {-1, 2}, {-1, 4}, {2, 4}})) throw new AssertionError("example 2");
        Random rnd = new Random(1502);
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(14);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(4);
            if (!Arrays.deepEquals(walls(a), oracle(a))) throw new AssertionError("disagrees with the outward walk on " + Arrays.toString(a));
        }
    }
}
```

#### Solution: [Boundary] All Equal Array (Author exercise)
<!-- id: ms-all-equal-ownership -->

**Approach.** Compute the walls under each convention by an outward walk, which keeps the comparisons visible, and sum `(i - left) * (right - i)` in `long` arithmetic. Under both strict walls, equal values extend over each other, so ties are counted more than once; under both non-strict walls, equal values stop each other, so stretches with ties are lost; only the asymmetric rule gives `n * (n + 1) / 2`. The assertions check the examples, check that the asymmetric total equals `n * (n + 1) / 2` on random arrays, that the two symmetric totals bracket it, and that for arrays of distinct values all three totals coincide.

**Complexity.** O(n^2) for the outward walks used to display the three conventions, and the single-scan version of the previous exercise gives the asymmetric total in O(n).

```java run
import java.util.Arrays;
import java.util.Random;

public final class AllEqualOwnership {
    static long total(int[] a, boolean leftStrict, boolean rightStrict) {
        int n = a.length;
        long sum = 0;
        for (int i = 0; i < n; i++) {
            int l = i - 1;
            while (l >= 0 && !(leftStrict ? a[l] < a[i] : a[l] <= a[i])) l--;
            int r = i + 1;
            while (r < n && !(rightStrict ? a[r] < a[i] : a[r] <= a[i])) r++;
            sum += (long) (i - l) * (r - i);
        }
        return sum;
    }
    static long[] totals(int[] a) {
        return new long[]{total(a, true, true), total(a, false, false), total(a, true, false)};
    }

    public static void main(String[] args) {
        if (!Arrays.equals(totals(new int[]{5, 5, 5}), new long[]{10, 3, 6})) throw new AssertionError("example 1");
        if (!Arrays.equals(totals(new int[]{4}), new long[]{1, 1, 1})) throw new AssertionError("example 2");
        Random rnd = new Random(1503);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(12);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(4);
            long[] tt = totals(a);
            long all = (long) n * (n + 1) / 2;
            if (tt[2] != all) throw new AssertionError("the asymmetric rule must give n(n+1)/2 on " + Arrays.toString(a));
            if (tt[0] < all || tt[1] > all) throw new AssertionError("both strict never undercounts and both non-strict never overcounts");
        }
        for (int t = 0; t < 500; t++) {
            int n = 1 + rnd.nextInt(10);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = i * 3 + 1;
            for (int i = n - 1; i > 0; i--) { int k = rnd.nextInt(i + 1); int tmp = a[i]; a[i] = a[k]; a[k] = tmp; }
            long[] tt = totals(a);
            if (tt[0] != tt[1] || tt[1] != tt[2]) throw new AssertionError("distinct values need no tie rule");
        }
    }
}
```

#### Solution: [Recognize] Sum of Subarray Minimums (LeetCode 907)
<!-- id: ms-sum-minimums-convention -->

**Approach.** State the rule first: each subarray belongs to the last index that holds its minimum, so the left wall is the nearest earlier strictly smaller index and the right wall is the nearest later index that is smaller or equal. One forward scan removing tops that are at least the current value supplies both walls. Index `i` owns `(i - left) * (right - i)` subarrays, its contribution to the sum is that count times `arr[i]`, and the count total is the second number of the answer. The assertions compare with a brute force over all subarrays, check that the count equals `n * (n + 1) / 2`, and show that the mirror rule, which gives ties to the earlier index and uses a flipped comparison, produces the same sum.

**Complexity.** O(n) time and O(n) extra space, with `long` arithmetic before the modulus.

```java run
import java.util.ArrayDeque;
import java.util.Arrays;
import java.util.Random;

public final class SumMinimumsConvention {
    static final long MOD = 1_000_000_007L;
    static long[] solve(int[] arr, boolean laterOwns) {
        int n = arr.length;
        int[] left = new int[n];
        int[] right = new int[n];
        Arrays.fill(right, n);
        ArrayDeque<Integer> stack = new ArrayDeque<>();
        for (int j = 0; j < n; j++) {
            while (!stack.isEmpty() && (laterOwns ? arr[stack.peekLast()] >= arr[j] : arr[stack.peekLast()] > arr[j])) right[stack.removeLast()] = j;
            left[j] = stack.isEmpty() ? -1 : stack.peekLast();
            stack.addLast(j);
        }
        long sum = 0, count = 0;
        for (int i = 0; i < n; i++) {
            long owned = (long) (i - left[i]) * (right[i] - i);
            count += owned;
            sum = (sum + owned % MOD * arr[i]) % MOD;
        }
        return new long[]{sum, count};
    }
    static long oracleSum(int[] arr) {
        long sum = 0;
        for (int lo = 0; lo < arr.length; lo++) {
            int min = Integer.MAX_VALUE;
            for (int hi = lo; hi < arr.length; hi++) { min = Math.min(min, arr[hi]); sum += min; }
        }
        return sum % MOD;
    }

    public static void main(String[] args) {
        if (!Arrays.equals(solve(new int[]{3, 1, 2, 4}, true), new long[]{17, 10})) throw new AssertionError("example 1");
        if (!Arrays.equals(solve(new int[]{1, 2, 1, 2, 1}, true), new long[]{17, 15})) throw new AssertionError("example 2");
        Random rnd = new Random(1504);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(14);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = 1 + rnd.nextInt(4);
            long[] later = solve(a, true);
            long[] earlier = solve(a, false);
            if (later[0] != oracleSum(a)) throw new AssertionError("disagrees with the brute force on " + Arrays.toString(a));
            if (later[1] != (long) n * (n + 1) / 2 || earlier[1] != later[1]) throw new AssertionError("both conventions must own every subarray once");
            if (later[0] != earlier[0]) throw new AssertionError("the mirror convention changes the owner but not the sum");
        }
    }
}
```
