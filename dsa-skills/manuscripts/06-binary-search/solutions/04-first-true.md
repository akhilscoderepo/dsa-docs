<!-- solutions-for: 06-binary-search -->
### Solutions For The First True Value

#### Solution: [Build] First True Boolean (Author exercise)
<!-- id: bs-first-true-array -->

**Approach.**
The array is a run of `false` followed by a run of `true`, so the test `flags[mid]` is monotone. A `true` at `mid` keeps `mid` as a possible answer with `hi = mid`. A `false` at `mid` proves that every index up to `mid` is false, so `lo` moves to `mid + 1`. The search starts with `hi = flags.length`, which makes the length the answer for an array without a `true`. The invariant keeps the indexes below `lo` false and keeps index `hi` true or equal to the length.

**Complexity.**
- **Time** is O(log n), because the interval halves each step.
- **Space** is O(1), because the code stores only three indexes.

```java run
import java.util.Random;

public final class FirstTrueArray {
    /**
     * Returns the index of the first true, or flags.length when none exists.
     * Time: O(log n). Space: O(1).
     * Invariant: indexes below lo are false; index hi is true or equals flags.length.
     */
    static int firstTrue(boolean[] flags) {
        // hi starts at the length, the sentinel for "no true value".
        int lo = 0, hi = flags.length;
        while (lo < hi) {
            int mid = lo + (hi - lo) / 2;
            // A true value may be the first one, so hi keeps it.
            if (flags[mid]) hi = mid;
            // A false value proves that everything up to mid is false.
            else lo = mid + 1;
        }
        return lo;
    }

    public static void main(String[] args) {
        // The statement examples and the empty array.
        if (firstTrue(new boolean[] {false, false, true, true}) != 2) throw new AssertionError("example 1");
        if (firstTrue(new boolean[] {false, false, false}) != 3) throw new AssertionError("example 2");
        if (firstTrue(new boolean[0]) != 0) throw new AssertionError("empty");
        // A non-monotone array breaks the claim: false,true,false,true returns 3, not 1.
        if (firstTrue(new boolean[] {false, true, false, true}) != 3) throw new AssertionError("non-monotone behaviour");
        // Random monotone arrays against a linear scan.
        Random rnd = new Random(41);
        for (int t = 0; t < 3000; t++) {
            int n = rnd.nextInt(15), cut = rnd.nextInt(n + 1);
            boolean[] f = new boolean[n];
            for (int i = cut; i < n; i++) f[i] = true;
            if (firstTrue(f) != cut) throw new AssertionError("random " + n + " " + cut);
        }
    }
}
```

#### Solution: [Vary] First Bad Build Between Two Known Builds (LeetCode 278)
<!-- id: bs-bad-between -->

**Approach.**
The first failing build lies in `good + 1` to `bad`. The build `bad` is known to fail, so it acts as the sentinel upper end. The search runs on `[good + 1, bad)` and returns `lo`. If `lo` reaches `bad`, then every probed build passed and the answer is `bad`, which the search never calls. The invariant is that every build below `lo` passes and the build `hi` fails. The interval `[good + 1, bad)` has `bad - good - 1` positions. At most 31 calls suffice for any `int` range.

**Complexity.**
- **Time** is O(log(bad - good)) oracle calls, because the interval halves each step.
- **Space** is O(1), because the code stores only three integers.

```java run
import java.util.Random;
import java.util.function.IntPredicate;

public final class BadBetween {
    /**
     * Returns the first failing build in (good, bad]; never calls fails on good or bad.
     * Time: O(log(bad - good)) calls. Space: O(1).
     * Invariant: builds below lo pass; build hi fails (it is bad, or was probed and failed).
     */
    static int firstFailing(int good, int bad, IntPredicate fails) {
        // good passes, so the search starts at good + 1; bad fails, so it is the sentinel end.
        int lo = good + 1, hi = bad;
        while (lo < hi) {
            // The subtraction keeps the midpoint inside the int range.
            int mid = lo + (hi - lo) / 2;
            if (fails.test(mid)) hi = mid; else lo = mid + 1;
        }
        return lo;
    }

    public static void main(String[] args) {
        // The statement examples, with call counting and a guard on the known endpoints.
        int[] calls = {0};
        IntPredicate p = b -> { calls[0]++; return b >= 17; };
        if (firstFailing(10, 20, p) != 17) throw new AssertionError("example 1");
        calls[0] = 0;
        if (firstFailing(0, 1, b -> { throw new AssertionError("no call expected"); }) != 1) throw new AssertionError("example 2");
        // The largest range stays within 31 calls and never calls the endpoints.
        calls[0] = 0;
        int got = firstFailing(0, Integer.MAX_VALUE, b -> {
            calls[0]++;
            if (b == 0 || b == Integer.MAX_VALUE) throw new AssertionError("endpoint called");
            return b >= Integer.MAX_VALUE - 3;
        });
        if (got != Integer.MAX_VALUE - 3 || calls[0] > 31) throw new AssertionError("large range " + got + " " + calls[0]);
        // Random ranges against a linear scan.
        Random rnd = new Random(42);
        for (int t = 0; t < 3000; t++) {
            int good = rnd.nextInt(10), bad = good + 1 + rnd.nextInt(30), first = good + 1 + rnd.nextInt(bad - good);
            if (firstFailing(good, bad, b -> b >= first) != first) throw new AssertionError("random " + good + " " + bad + " " + first);
        }
    }
}
```

#### Solution: [Boundary] No True Value (Author exercise)
<!-- id: bs-no-true -->

**Approach.**
The search counts every oracle call and starts with `hi = n`. When every probed position is false, `lo` moves up until it equals `n`, so the sentinel appears without a special case. When `n == 0`, the loop condition `lo < hi` is false at once, and the method makes no call. The call count is at most `floor(log2(n)) + 1`, because each call halves the interval. The invariant is that every position below `lo` is false and position `hi` is true or equals `n`.

**Complexity.**
- **Time** is O(log n), because each oracle call halves the interval.
- **Space** is O(1), because the result pair has fixed size.

```java run
import java.util.Random;
import java.util.function.IntPredicate;

public final class NoTrueValue {
    /**
     * Returns {first true position or n, number of oracle calls}.
     * Time: O(log n). Space: O(1).
     * Invariant: positions below lo are false; position hi is true or equals n.
     */
    static int[] firstTrue(int n, IntPredicate isTrue) {
        int lo = 0, hi = n, calls = 0;
        // n == 0 skips the loop, so no call is made.
        while (lo < hi) {
            int mid = lo + (hi - lo) / 2;
            calls++;
            if (isTrue.test(mid)) hi = mid; else lo = mid + 1;
        }
        return new int[] {lo, calls};
    }

    public static void main(String[] args) {
        // The statement examples: five false positions give the sentinel after 2 calls.
        int[] r = firstTrue(5, i -> false);
        if (r[0] != 5 || r[1] != 2) throw new AssertionError("example 1");
        int[] z = firstTrue(0, i -> { throw new AssertionError("no call expected"); });
        if (z[0] != 0 || z[1] != 0) throw new AssertionError("example 2");
        // A huge range stays within the call limit.
        int[] big = firstTrue(1_000_000_000, i -> false);
        if (big[0] != 1_000_000_000 || big[1] > 30) throw new AssertionError("large n " + big[1]);
        // Random monotone oracles: the answer matches and calls stay within floor(log2(n)) + 1.
        Random rnd = new Random(43);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(200), cut = rnd.nextInt(n + 1);
            int[] got = firstTrue(n, i -> i >= cut);
            if (got[0] != cut || got[1] > 32 - Integer.numberOfLeadingZeros(n)) throw new AssertionError("random " + n + " " + cut);
        }
    }
}
```

#### Solution: [Recognize] Kth Missing Positive Number (LeetCode 1539)
<!-- id: bs-kth-missing -->

**Approach.**
Below the value `arr[i]` lie `arr[i] - 1` positive integers, and `i` of them are array values. The count of missing numbers below `arr[i]` is therefore `arr[i] - (i + 1)`. This count never decreases as `i` grows, because the values are distinct and ascending. The predicate "at least `k` numbers are missing below `arr[i]`" is therefore monotone. The search finds the first index `lo` that satisfies it, with `lo = arr.length` when none does. Exactly `lo` array values lie below the answer, so the answer is `lo + k`. The invariant is that every index below `lo` has fewer than `k` missing numbers below its value.

**Complexity.**
- **Time** is O(log n), because the predicate takes O(1) per probe and the interval halves each step.
- **Space** is O(1), because the code stores only three indexes.

```java run
import java.util.Random;

public final class KthMissing1539 {
    /**
     * Returns the k-th positive integer missing from the ascending distinct array arr.
     * Time: O(log n). Space: O(1).
     * Invariant: indexes below lo have fewer than k missing numbers below their value.
     */
    static int findKthPositive(int[] arr, int k) {
        int lo = 0, hi = arr.length;
        while (lo < hi) {
            int mid = lo + (hi - lo) / 2;
            // arr[mid] - (mid + 1) counts the missing numbers below arr[mid]; it never decreases.
            if (arr[mid] - (mid + 1) >= k) hi = mid; else lo = mid + 1;
        }
        // lo array values lie below the answer, so the answer is lo + k.
        return lo + k;
    }

    public static void main(String[] args) {
        // The statement examples.
        if (findKthPositive(new int[] {2, 3, 4, 7, 11}, 5) != 9) throw new AssertionError("example 1");
        if (findKthPositive(new int[] {4, 5, 6}, 2) != 2) throw new AssertionError("example 2");
        // The missing counts never decrease on a sample array.
        int[] s = {2, 3, 4, 7, 11};
        for (int i = 1; i < s.length; i++) if (s[i] - (i + 1) < s[i - 1] - i) throw new AssertionError("count decreased");
        // Random arrays against counting missing numbers one by one.
        Random rnd = new Random(44);
        for (int t = 0; t < 3000; t++) {
            int[] a = rnd.ints(1 + rnd.nextInt(10), 1, 30).distinct().sorted().toArray();
            int k = 1 + rnd.nextInt(30), seen = 0, v = 0, i = 0;
            while (seen < k) { v++; if (i < a.length && a[i] == v) i++; else seen++; }
            if (findKthPositive(a, k) != v) throw new AssertionError("random " + java.util.Arrays.toString(a) + " " + k);
        }
    }
}
```
