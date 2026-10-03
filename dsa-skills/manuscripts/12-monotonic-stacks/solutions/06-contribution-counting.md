<!-- solutions-for: 06-contribution-counting -->
### Contribution Counting

#### Solution: [Build] Count Subarrays Owned By One Index (Author exercise)
<!-- id: ms-count-owned-one-index -->

**Approach.** A subarray `[s, e]` belongs to the index when it contains it and stays strictly between the walls. The start can be any of `left + 1, ..., i`, which is `i - left` values, and the end can be any of `i, ..., right - 1`, which is `right - i` values. The two choices are independent, so the count is their product. The product is computed after widening to `long`. The assertions check both examples, compare with a loop that enumerates every pair `(s, e)`, and show that an `int` product of two moderately large distances wraps around.

**Complexity.** O(1) time and space for the formula, against O(n^2) for the enumeration used as the oracle.

```java run
import java.util.Random;

public final class CountOwnedOneIndex {
    static long owned(int left, int i, int right) {
        return (long) (i - left) * (right - i);
    }
    static long oracle(int left, int i, int right) {
        long count = 0;
        for (int s = left + 1; s <= i; s++)
            for (int e = i; e < right; e++) count++;
        return count;
    }

    public static void main(String[] args) {
        if (owned(-1, 2, 5) != 9) throw new AssertionError("example 1");
        if (owned(2, 3, 4) != 1) throw new AssertionError("example 2");
        int distance = 50001;
        if (distance * distance == (long) distance * distance) throw new AssertionError("the int product of two large distances should wrap");
        if (owned(-1, 50000, 100001) != 50001L * 50001L) throw new AssertionError("the long product keeps the full count");
        Random rnd = new Random(1601);
        for (int t = 0; t < 3000; t++) {
            int left = rnd.nextInt(10) - 1;
            int i = left + 1 + rnd.nextInt(8);
            int right = i + 1 + rnd.nextInt(8);
            if (owned(left, i, right) != oracle(left, i, right)) throw new AssertionError("disagrees with the enumeration for " + left + "," + i + "," + right);
        }
    }
}
```

#### Solution: [Vary] Sum Owned Minimum Contributions (Author exercise)
<!-- id: ms-sum-owned-contributions -->

**Approach.** Each index contributes its value times the number of subarrays it owns, so the answer is the sum of `a[i] * (i - left[i]) * (right[i] - i)`. The count is widened to `long` before it meets the value. The assertions check both examples and test random arrays by computing the walls with the strict-left, non-strict-right comparisons and comparing the weighted sum with the sum of the minimum of every subarray, which also confirms the ownership proof the formula relies on.

**Complexity.** O(n) time and O(1) extra space once the walls are given.

```java run
import java.util.Random;

public final class SumOwnedContributions {
    static long weighted(int[] a, int[] left, int[] right) {
        long sum = 0;
        for (int i = 0; i < a.length; i++) sum += (long) a[i] * (long) (i - left[i]) * (right[i] - i);
        return sum;
    }
    static long bruteMinimums(int[] a) {
        long sum = 0;
        for (int lo = 0; lo < a.length; lo++) {
            int min = Integer.MAX_VALUE;
            for (int hi = lo; hi < a.length; hi++) { min = Math.min(min, a[hi]); sum += min; }
        }
        return sum;
    }

    public static void main(String[] args) {
        if (weighted(new int[]{3, 1, 2, 4}, new int[]{-1, -1, 1, 2}, new int[]{1, 4, 4, 4}) != 17) throw new AssertionError("example 1");
        if (weighted(new int[]{2, 2}, new int[]{-1, -1}, new int[]{1, 2}) != 6) throw new AssertionError("example 2");
        Random rnd = new Random(1602);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(12);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = 1 + rnd.nextInt(4);
            int[] left = new int[n];
            int[] right = new int[n];
            for (int i = 0; i < n; i++) {
                int l = i - 1;
                while (l >= 0 && !(a[l] < a[i])) l--;
                int r = i + 1;
                while (r < n && !(a[r] <= a[i])) r++;
                left[i] = l;
                right[i] = r;
            }
            if (weighted(a, left, right) != bruteMinimums(a)) throw new AssertionError("weighted sum differs from the brute force on " + java.util.Arrays.toString(a));
        }
    }
}
```

#### Solution: [Boundary] Negative And Repeated Values (Author exercise)
<!-- id: ms-negative-repeated-values -->

**Approach.** The ownership proof does not depend on the sign of the values, because it only compares them, so the same walls give the same counts for negative and repeated values. The arithmetic is where care is needed: the count is widened to `long` and reduced first, the product with a possibly negative value is reduced again, and Java's `%` leaves a negative remainder for a negative left operand, so the final value is normalized with one more addition of the modulus. The assertions check the examples, state the sign behaviour of `%` directly, and compare with a brute force that reduces its sum with the same normalization.

**Complexity.** O(n) time and O(n) extra space.

```java run
import java.util.ArrayDeque;
import java.util.Random;

public final class NegativeRepeatedValues {
    static final long MOD = 1_000_000_007L;
    static long sumOfMinimums(int[] a) {
        int n = a.length;
        long total = 0;
        ArrayDeque<Integer> stack = new ArrayDeque<>();
        for (int j = 0; j <= n; j++) {
            int current = (j == n) ? Integer.MIN_VALUE : a[j];
            while (!stack.isEmpty() && a[stack.peekLast()] >= current) {
                int t = stack.removeLast();
                int left = stack.isEmpty() ? -1 : stack.peekLast();
                long owned = (long) (t - left) * (j - t);
                total = (total + (owned % MOD) * a[t]) % MOD;
            }
            if (j < n) stack.addLast(j);
        }
        return ((total % MOD) + MOD) % MOD;
    }
    static long oracle(int[] a) {
        long sum = 0;
        for (int lo = 0; lo < a.length; lo++) {
            int min = Integer.MAX_VALUE;
            for (int hi = lo; hi < a.length; hi++) { min = Math.min(min, a[hi]); sum += min; }
        }
        return ((sum % MOD) + MOD) % MOD;
    }

    public static void main(String[] args) {
        if (-3L % MOD != -3L) throw new AssertionError("a negative left operand keeps its sign in %");
        if (sumOfMinimums(new int[]{-1, 2, -1}) != 1000000004L) throw new AssertionError("example 1");
        if (sumOfMinimums(new int[]{-5, -5}) != 999999992L) throw new AssertionError("example 2");
        Random rnd = new Random(1603);
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(14);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(7) - 4;
            if (sumOfMinimums(a) != oracle(a)) throw new AssertionError("disagrees with the brute force on " + java.util.Arrays.toString(a));
        }
    }
}
```

#### Solution: [Recognize] Sum of Subarray Minimums (LeetCode 907)
<!-- id: ms-sum-minimums-stack -->

**Approach.** One forward scan keeps a stack of indices with a flush step at `j = n`. When index `j` removes index `t`, the right wall of `t` is `j` and its left wall is the new top, or -1, so `t` owns `(t - left) * (j - t)` subarrays and is priced immediately, with the product widened to `long` and reduced before it is multiplied by the value. The removal test is "at least", which is the one-strict, one-non-strict rule. The assertions check the examples, compare with the brute force on random small arrays, and for arrays of 100,000 values up to a billion compare against a version that stores explicit wall arrays and sums with `BigInteger`, so any overflow in the single-pass version would show.

**Complexity.** O(n) time and O(n) extra space.

```java run
import java.math.BigInteger;
import java.util.ArrayDeque;
import java.util.Random;

public final class SumMinimumsStack {
    static final long MOD = 1_000_000_007L;
    static long sumSubarrayMins(int[] arr) {
        int n = arr.length;
        long total = 0;
        ArrayDeque<Integer> stack = new ArrayDeque<>();
        for (int j = 0; j <= n; j++) {
            int current = (j == n) ? Integer.MIN_VALUE : arr[j];
            while (!stack.isEmpty() && arr[stack.peekLast()] >= current) {
                int t = stack.removeLast();
                int left = stack.isEmpty() ? -1 : stack.peekLast();
                long owned = (long) (t - left) * (j - t);
                total = (total + (owned % MOD) * arr[t]) % MOD;
            }
            if (j < n) stack.addLast(j);
        }
        return total;
    }
    static long bruteForce(int[] a) {
        long sum = 0;
        for (int lo = 0; lo < a.length; lo++) {
            int min = Integer.MAX_VALUE;
            for (int hi = lo; hi < a.length; hi++) { min = Math.min(min, a[hi]); sum = (sum + min) % MOD; }
        }
        return sum;
    }
    static long withArraysAndBigInteger(int[] a) {
        int n = a.length;
        int[] left = new int[n];
        int[] right = new int[n];
        ArrayDeque<Integer> st = new ArrayDeque<>();
        for (int i = 0; i < n; i++) {
            while (!st.isEmpty() && a[st.peekLast()] >= a[i]) st.removeLast();
            left[i] = st.isEmpty() ? -1 : st.peekLast();
            st.addLast(i);
        }
        st.clear();
        for (int i = n - 1; i >= 0; i--) {
            while (!st.isEmpty() && a[st.peekLast()] > a[i]) st.removeLast();
            right[i] = st.isEmpty() ? n : st.peekLast();
            st.addLast(i);
        }
        BigInteger sum = BigInteger.ZERO;
        for (int i = 0; i < n; i++)
            sum = sum.add(BigInteger.valueOf(a[i]).multiply(BigInteger.valueOf((long) (i - left[i]) * (right[i] - i))));
        return sum.mod(BigInteger.valueOf(MOD)).longValue();
    }

    public static void main(String[] args) {
        if (sumSubarrayMins(new int[]{2, 9, 3, 3}) != 32) throw new AssertionError("example 1");
        if (sumSubarrayMins(new int[]{4, 4, 4, 4}) != 40) throw new AssertionError("example 2");
        Random rnd = new Random(1604);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(14);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = 1 + rnd.nextInt(5);
            if (sumSubarrayMins(a) != bruteForce(a)) throw new AssertionError("disagrees with the brute force on " + java.util.Arrays.toString(a));
        }
        int[] big = new int[100000];
        for (int i = 0; i < big.length; i++) big[i] = 1 + rnd.nextInt(1_000_000_000);
        if (sumSubarrayMins(big) != withArraysAndBigInteger(big)) throw new AssertionError("overflow in the large case");
        int[] same = new int[100000];
        java.util.Arrays.fill(same, 1_000_000_000);
        if (sumSubarrayMins(same) != withArraysAndBigInteger(same)) throw new AssertionError("overflow when all values are equal");
    }
}
```
