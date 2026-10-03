<!-- solutions-for: 07-prefix-construction -->
### Prefix Construction

#### Solution: [Build] Running Sum of 1d Array (LeetCode 1480)
<!-- id: ps-running-sum -->

**Approach.** Position `i` of the answer is position `i - 1` of the answer plus `nums[i]`, so one variable holding the total so far is enough. The loop adds the next value, stores the total, and moves on. Because the limits keep every total within about a billion, an `int` total is safe here, and the input array is only read. The oracle recomputes each position by adding from the start, and the program also checks that the input is unchanged.

**Complexity.** One pass, so linear time in the length, with the output array as the only extra space.

```java run
import java.util.Arrays;
import java.util.Random;

public final class RunningSum {
    static int[] runningSum(int[] nums) {
        int[] out = new int[nums.length];
        int total = 0;
        for (int i = 0; i < nums.length; i++) {
            total += nums[i];
            out[i] = total;
        }
        return out;
    }
    static int[] oracle(int[] nums) {
        int[] out = new int[nums.length];
        for (int i = 0; i < nums.length; i++) {
            int s = 0;
            for (int j = 0; j <= i; j++) s += nums[j];
            out[i] = s;
        }
        return out;
    }

    public static void main(String[] args) {
        if (!Arrays.equals(runningSum(new int[] {2, 5, -1, 4}), new int[] {2, 7, 6, 10})) throw new AssertionError("example 1");
        if (!Arrays.equals(runningSum(new int[] {7, 7, 7}), new int[] {7, 14, 21})) throw new AssertionError("example 2");
        int[] keep = {3, -4, 9};
        int[] copy = keep.clone();
        runningSum(keep);
        if (!Arrays.equals(keep, copy)) throw new AssertionError("the input must not change");
        Random rnd = new Random(7101);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(12);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(2001) - 1000;
            if (!Arrays.equals(runningSum(a), oracle(a))) throw new AssertionError("differs on " + Arrays.toString(a));
        }
    }
}
```

#### Solution: [Vary] Find Pivot Index (LeetCode 724)
<!-- id: ps-pivot-index -->

**Approach.** For a position `i`, the sum to the right equals the grand total minus the sum to the left minus `nums[i]`, so nothing needs to be stored besides the grand total and a running left sum. The first pass computes the total in a `long`. The second pass tests each position in order, and returns the first one whose two sides are equal, then adds the current value to the left sum. Testing before adding is what keeps the current value out of both sides, and the order of the scan makes the answer the leftmost one. The oracle sums both sides directly for each position.

**Complexity.** Two passes and O(1) extra space.

```java run
import java.util.Random;

public final class PivotIndex {
    static int pivotIndex(int[] nums) {
        long total = 0;
        for (int x : nums) total += x;
        long left = 0;
        for (int i = 0; i < nums.length; i++) {
            if (left == total - left - nums[i]) return i;
            left += nums[i];
        }
        return -1;
    }
    static int oracle(int[] nums) {
        for (int i = 0; i < nums.length; i++) {
            long l = 0, r = 0;
            for (int j = 0; j < i; j++) l += nums[j];
            for (int j = i + 1; j < nums.length; j++) r += nums[j];
            if (l == r) return i;
        }
        return -1;
    }

    public static void main(String[] args) {
        if (pivotIndex(new int[] {2, -1, 8, 4, 2, 2, 5}) != 3) throw new AssertionError("example 1");
        if (pivotIndex(new int[] {3, 3}) != -1) throw new AssertionError("example 2");
        if (pivotIndex(new int[] {5}) != 0) throw new AssertionError("a single value is a pivot");
        if (pivotIndex(new int[] {0, 4, -4}) != 0) throw new AssertionError("an empty left side counts as zero");
        Random rnd = new Random(7102);
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(9);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(7) - 3;
            if (pivotIndex(a) != oracle(a)) throw new AssertionError("differs at n=" + n);
        }
    }
}
```

#### Solution: [Boundary] Empty Prefix (Author exercise)
<!-- id: ps-empty-prefix -->

**Approach.** The prefix array has one more slot than the input, and slot zero is the sum of no values, so an empty input produces an array with the single value zero. A request for the sum of the first `count` values reads slot `count`, which is valid for every count from zero to the length, and no branch is needed for zero. The slots are `long`, because two values near two billion add to more than an `int` can hold. The program shows both cases, and a second version with an `int` accumulator that wraps on the large example, to show what the `long` protects against.

**Complexity.** O(n) to build and O(1) per request, with n + 1 slots of space.

```java run
import java.util.Random;

public final class EmptyPrefix {
    static long[] buildPrefix(int[] nums) {
        long[] prefix = new long[nums.length + 1];
        for (int i = 0; i < nums.length; i++) prefix[i + 1] = prefix[i] + nums[i];
        return prefix;
    }
    static long sumOfFirst(long[] prefix, int count) { return prefix[count]; }
    static int[] wrappedPrefix(int[] nums) {
        int[] prefix = new int[nums.length + 1];
        for (int i = 0; i < nums.length; i++) prefix[i + 1] = prefix[i] + nums[i];
        return prefix;
    }

    public static void main(String[] args) {
        long[] empty = buildPrefix(new int[0]);
        if (empty.length != 1 || sumOfFirst(empty, 0) != 0) throw new AssertionError("example 1");
        int[] big = {2000000000, 2000000000};
        long[] p = buildPrefix(big);
        if (sumOfFirst(p, 2) != 4000000000L) throw new AssertionError("example 2");
        if (wrappedPrefix(big)[2] == 4000000000L) throw new AssertionError("an int accumulator should have wrapped");
        if (sumOfFirst(buildPrefix(new int[] {Integer.MAX_VALUE}), 1) != 2147483647L) throw new AssertionError("largest single value");
        Random rnd = new Random(7103);
        for (int t = 0; t < 2000; t++) {
            int n = rnd.nextInt(8);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt();
            long[] pre = buildPrefix(a);
            for (int c = 0; c <= n; c++) {
                long s = 0;
                for (int i = 0; i < c; i++) s += a[i];
                if (sumOfFirst(pre, c) != s) throw new AssertionError("differs at count " + c);
            }
        }
    }
}
```

#### Solution: [Recognize] Prefix Averages (Author exercise)
<!-- id: ps-prefix-averages -->

**Approach.** The average of the first `i + 1` values is the running total through position `i` divided by `i + 1`, the number of values in the prefix. The total is held in a `long`, since the total of many values near a billion can reach a hundred trillion, and the division is done as `double` division so that the fraction survives. The oracle recomputes each prefix sum from scratch with a `long` accumulator, and the program checks that dividing by `i` instead of `i + 1` would be wrong for the first example.

**Complexity.** One pass, linear time, and the output array as the only extra space.

```java run
import java.util.Random;

public final class PrefixAverages {
    static double[] prefixAverages(int[] nums) {
        double[] out = new double[nums.length];
        long total = 0;
        for (int i = 0; i < nums.length; i++) {
            total += nums[i];
            out[i] = (double) total / (i + 1);
        }
        return out;
    }
    static double[] oracle(int[] nums) {
        double[] out = new double[nums.length];
        for (int i = 0; i < nums.length; i++) {
            long s = 0;
            for (int j = 0; j <= i; j++) s += nums[j];
            out[i] = s / (double) (i + 1);
        }
        return out;
    }

    public static void main(String[] args) {
        double[] one = prefixAverages(new int[] {4, 6, 2});
        if (one[0] != 4.0 || one[1] != 5.0 || one[2] != 4.0) throw new AssertionError("example 1");
        double[] two = prefixAverages(new int[] {1000000000, 1000000000, 1000000000});
        for (double d : two) if (d != 1.0E9) throw new AssertionError("example 2");
        if (10.0 / 1 == one[1]) throw new AssertionError("dividing by the position would be wrong");
        Random rnd = new Random(7104);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(10);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(2000000001) - 1000000000;
            double[] x = prefixAverages(a), y = oracle(a);
            for (int i = 0; i < n; i++) if (x[i] != y[i]) throw new AssertionError("differs at " + i);
        }
    }
}
```
