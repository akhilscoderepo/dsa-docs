<!-- solutions-for: 01-call-state -->
### Solutions For Shrinking Each Call

#### Solution: [Build] Sum A Prefix (Author exercise)
<!-- id: bt-sum-a-prefix -->

**Approach.**
The contract says that `prefix(a, k)` returns the sum of `a[0..k)`. The base case is `k == 0`, where the range is empty and the sum is 0. For `k > 0`, the sum equals `a[k - 1]` plus the sum of the first `k - 1` values, which the contract of the next call provides. Each call passes `k - 1`, so the state moves toward 0 by one in each call, and the chain ends after `k` calls.

**Complexity.**
- **Time** is O(k), because the chain holds k + 1 calls and each call does constant work.
- **Space** is O(k) for the stack frames, and the method allocates no array.

```java run
import java.util.*;

public final class SumAPrefix {
    /**
     * Returns the sum of the first k values of a.
     * Time: O(k). Space: O(k) stack frames.
     * Invariant: each call returns the sum of a[0..k) for its own k, and k falls by one per call.
     */
    static long prefix(int[] a, int k) {
        if (k == 0) return 0;                          // base case: the empty range sums to 0
        return a[k - 1] + prefix(a, k - 1);            // the last value of the range plus the contract of k - 1
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (prefix(new int[] {4, 1, 3, 5}, 3) != 8) throw new AssertionError("ex1");
        if (prefix(new int[] {7, -2}, 0) != 0) throw new AssertionError("ex2");
        // Random arrays must match a plain loop.
        Random rnd = new Random(1901);
        for (int t = 0; t < 500; t++) {
            int[] a = new int[rnd.nextInt(40)];
            for (int i = 0; i < a.length; i++) a[i] = rnd.nextInt(2001) - 1000;
            int k = rnd.nextInt(a.length + 1);
            long want = 0;
            for (int i = 0; i < k; i++) want += a[i];
            if (prefix(a, k) != want) throw new AssertionError("random " + t);
        }
        // A call with k = 0 must not read the array, so a null array is safe.
        if (prefix(null, 0) != 0) throw new AssertionError("base case reads nothing");
        System.out.println("ok");
    }
}
```

#### Solution: [Vary] Pow(x, n) (LeetCode 50)
<!-- id: bt-pow-halving -->

**Approach.**
The contract says that `pow(x, n)` returns x^n for `n >= 0`. The base case is `n == 0`, which returns 1. For `n > 0`, the call asks the contract for `n / 2`, which is strictly smaller than `n`. Squaring that answer gives `x^(2 * (n / 2))`. When `n` is odd, `n` equals `2 * (n / 2) + 1`, so the method multiplies the square by one more `x`. The invariant is that every call returns x^n for its own exponent.

**Complexity.**
- **Time** is O(log n), because each call halves the exponent and the chain ends after about 31 calls for an `int`.
- **Space** is O(log n) for the stack frames, and each frame holds one `double`.

```java run
import java.util.*;

public final class PowHalving {
    /**
     * Returns x raised to the power n for n >= 0.
     * Time: O(log n). Space: O(log n) stack frames.
     * Invariant: each call returns x^n for its own n, and n halves in every call.
     */
    static double pow(double x, int n) {
        if (n == 0) return 1.0;                        // base case: the empty product is 1
        double half = pow(x, n / 2);                   // n / 2 < n for every n > 0, so the chain ends
        return (n % 2 == 0) ? half * half : half * half * x;   // an odd exponent adds one factor of x
    }

    static int depth(int n) { return n == 0 ? 1 : 1 + depth(n / 2); }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (pow(2, 10) != 1024.0) throw new AssertionError("ex1");
        if (pow(0, 0) != 1.0) throw new AssertionError("ex2");
        // Random inputs must match a plain loop within a relative error.
        Random rnd = new Random(1902);
        for (int t = 0; t < 500; t++) {
            double x = (rnd.nextInt(41) - 20) / 10.0;
            int n = rnd.nextInt(30);
            double want = 1.0;
            for (int i = 0; i < n; i++) want *= x;
            double got = pow(x, n);
            if (Math.abs(got - want) > 1e-9 * Math.max(1.0, Math.abs(want))) throw new AssertionError("random " + t);
        }
        // The deepest exponent needs 32 calls, which supports the logarithmic claim.
        if (depth(Integer.MAX_VALUE) != 32) throw new AssertionError("depth " + depth(Integer.MAX_VALUE));
        // Integer division truncates toward zero, so n / 2 is smaller than n for every positive n.
        for (int n = 1; n <= 1000; n++) if (n / 2 >= n) throw new AssertionError("shrink " + n);
        System.out.println("ok");
    }
}
```

#### Solution: [Boundary] Zero And Negative Exponents (Author exercise)
<!-- id: bt-negative-exponents -->

**Approach.**
In `int` arithmetic, `-Integer.MIN_VALUE` equals `Integer.MIN_VALUE`, so a negation before widening keeps the number negative and breaks the contract. The method converts `n` to a `long` first and negates after that, so `-(long) n` holds the correct positive value 2^31. The helper computes the power of a non-negative `long` exponent by halving. A negative exponent then returns the reciprocal of the helper result. The invariant is that the helper always receives an exponent that is zero or positive.

**Complexity.**
- **Time** is O(log |n|), because the helper halves the exponent in each call.
- **Space** is O(log |n|) for the stack frames, and the widening adds one `long`.

```java run
import java.util.*;

public final class NegativeExponents {
    /**
     * Returns x raised to the power n for x != 0 and any int n.
     * Time: O(log |n|). Space: O(log |n|) stack frames.
     * Invariant: the helper receives an exponent of at least 0, and the exponent halves in every call.
     */
    static double pow(double x, int n) {
        long e = n;                                    // widen first so the next negation cannot wrap
        return e >= 0 ? helper(x, e) : 1.0 / helper(x, -e);   // a negative exponent means the reciprocal
    }

    private static double helper(double x, long e) {
        if (e == 0) return 1.0;                        // base case: the exponent 0 gives 1
        double half = helper(x, e / 2);                // e / 2 is strictly smaller for e > 0
        return (e % 2 == 0) ? half * half : half * half * x;   // an odd exponent adds one factor
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (pow(2, -3) != 0.125) throw new AssertionError("ex1");
        if (pow(1, Integer.MIN_VALUE) != 1.0) throw new AssertionError("ex2");
        // The Java claim: negating Integer.MIN_VALUE in int arithmetic leaves it negative.
        if (-Integer.MIN_VALUE != Integer.MIN_VALUE) throw new AssertionError("int negation");
        // Widening first gives the true positive value.
        if (-(long) Integer.MIN_VALUE != 2147483648L) throw new AssertionError("long negation");
        // Random exponents must match a reciprocal of a plain loop.
        Random rnd = new Random(1903);
        for (int t = 0; t < 500; t++) {
            double x = (rnd.nextInt(16) + 5) / 10.0;
            int n = rnd.nextInt(41) - 20;
            double want = 1.0;
            for (int i = 0; i < Math.abs(n); i++) want *= x;
            if (n < 0) want = 1.0 / want;
            double got = pow(x, n);
            if (Math.abs(got - want) > 1e-9 * Math.max(1.0, Math.abs(want))) throw new AssertionError("random " + t);
        }
        // A base below 1 underflows to 0 at the most negative exponent from the other side.
        if (pow(0.5, Integer.MIN_VALUE) != Double.POSITIVE_INFINITY) throw new AssertionError("overflow");
        if (pow(2, Integer.MIN_VALUE) != 0.0) throw new AssertionError("underflow");
        System.out.println("ok");
    }
}
```

#### Solution: [Recognize] Recursive String Reversal By Range (Author exercise)
<!-- id: bt-reverse-by-range -->

**Approach.**
The contract says that `rev(s, lo, hi)` reverses the values at positions `lo` to `hi`. The base case is `lo >= hi`, because a range with zero or one value is already reversed. Otherwise the call swaps `s[lo]` and `s[hi]`, which puts both values at their final positions. Then it asks the contract to reverse the inner range `lo + 1` to `hi - 1`. The range loses two positions per call, so the chain ends after about half of the length. The method copies nothing and creates no substring.

**Complexity.**
- **Time** is O(n), because the chain holds about n / 2 calls and each call swaps once.
- **Space** is O(n) for the stack frames, and the heap holds no extra array.

```java run
import java.util.*;

public final class ReverseByRange {
    /**
     * Reverses s[lo..hi] in place.
     * Time: O(hi - lo). Space: O(hi - lo) stack frames.
     * Invariant: before each call, the positions outside lo..hi already hold their final values.
     */
    static void rev(char[] s, int lo, int hi) {
        if (lo >= hi) return;                          // base case: zero or one value needs no swap
        char t = s[lo]; s[lo] = s[hi]; s[hi] = t;      // both ends reach their final positions
        rev(s, lo + 1, hi - 1);                        // the inner range is two positions shorter
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        char[] a = {'a', 'b', 'c', 'd'}; rev(a, 0, a.length - 1);
        if (!Arrays.equals(a, new char[] {'d', 'c', 'b', 'a'})) throw new AssertionError("ex1");
        char[] b = {'x'}; rev(b, 0, 0);
        if (!Arrays.equals(b, new char[] {'x'})) throw new AssertionError("ex2");
        // The empty array has hi = -1 and must stay empty.
        char[] e = {}; rev(e, 0, -1);
        if (e.length != 0) throw new AssertionError("empty");
        // Random arrays must match a reversed copy.
        Random rnd = new Random(1904);
        for (int t = 0; t < 500; t++) {
            char[] s = new char[rnd.nextInt(30)];
            for (int i = 0; i < s.length; i++) s[i] = (char) ('a' + rnd.nextInt(26));
            char[] want = new char[s.length];
            for (int i = 0; i < s.length; i++) want[i] = s[s.length - 1 - i];
            rev(s, 0, s.length - 1);
            if (!Arrays.equals(s, want)) throw new AssertionError("random " + t);
        }
        System.out.println("ok");
    }
}
```
