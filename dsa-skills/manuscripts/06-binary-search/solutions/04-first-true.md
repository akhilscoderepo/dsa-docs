<!-- solutions-for: 06-first-true -->
### First True

#### Solution: [Build] First True Boolean (Author exercise)
<!-- id: bs-first-true-boolean -->

**Approach.** Keep a half-open interval `[lo, hi)` with `hi = n`. A true value at `mid` means the first true position is at `mid` or earlier, so `hi = mid`. A false value proves that `mid` and everything before it are false, so `lo = mid + 1`. When the edges meet, that position is the first true value, or `n` when none exists. The check builds every monotone array of lengths up to ten and compares with a linear scan.

**Complexity.** O(log n) time and O(1) extra space.

```java run
public final class FirstTrueBoolean {
    static int firstTrue(boolean[] flags) {
        int lo = 0, hi = flags.length;
        while (lo < hi) {
            int mid = lo + (hi - lo) / 2;
            if (flags[mid]) hi = mid;
            else lo = mid + 1;
        }
        return lo;
    }

    public static void main(String[] args) {
        if (firstTrue(new boolean[] {false, false, true, true}) != 2) throw new AssertionError("example 1");
        if (firstTrue(new boolean[] {true}) != 0) throw new AssertionError("example 2");
        for (int n = 1; n <= 10; n++) {
            for (int flip = 0; flip <= n; flip++) {
                boolean[] f = new boolean[n];
                for (int i = flip; i < n; i++) f[i] = true;
                int expected = n;
                for (int i = 0; i < n; i++) if (f[i]) { expected = i; break; }
                if (firstTrue(f) != expected) throw new AssertionError("flip at " + flip + " of " + n);
            }
        }
    }
}
```

#### Solution: [Vary] First Bad Version (LeetCode 278)
<!-- id: bs-first-bad-version-halfopen -->

**Approach.** The contract guarantees that version `n` is bad, so `n` is a legitimate possible answer without being tested. Keep `[lo, hi)` as `[1, n)` plus that guaranteed answer: loop while `lo < hi`, test `mid`, set `hi = mid` on a bad version and `lo = mid + 1` on a good one. At the end `lo == hi` is the first bad version. Every call halves the number of candidates, so at most `ceil(log2 n)` calls are made. The check counts calls for every first-bad position of every `n` up to 300 and for a huge `n`.

**Complexity.** O(log n) calls to the predicate and O(1) extra space.

```java run
import java.util.function.IntPredicate;

public final class FirstBadVersionHalfOpen {
    static int calls;

    static int firstBadVersion(int n, IntPredicate isBad) {
        int lo = 1, hi = n;
        while (lo < hi) {
            int mid = lo + (hi - lo) / 2;
            calls++;
            if (isBad.test(mid)) hi = mid;
            else lo = mid + 1;
        }
        return lo;
    }
    static int ceilLog2(int n) { return n <= 1 ? 0 : 32 - Integer.numberOfLeadingZeros(n - 1); }

    public static void main(String[] args) {
        calls = 0;
        if (firstBadVersion(100, v -> v >= 37) != 37) throw new AssertionError("example 1");
        calls = 0;
        if (firstBadVersion(2, v -> v >= 2) != 2) throw new AssertionError("example 2");
        for (int n = 1; n <= 300; n++) {
            for (int bad = 1; bad <= n; bad++) {
                final int b = bad;
                calls = 0;
                if (firstBadVersion(n, v -> v >= b) != bad) throw new AssertionError("wrong for n=" + n + " bad=" + bad);
                if (calls > ceilLog2(n)) throw new AssertionError("too many calls for n=" + n + ": " + calls);
            }
        }
        calls = 0;
        int n = 2_000_000_000, b = 1_234_567_890;
        if (firstBadVersion(n, v -> v >= b) != b) throw new AssertionError("large n");
        if (calls > 31) throw new AssertionError("calls on large n: " + calls);
    }
}
```

#### Solution: [Boundary] No True Value (Author exercise)
<!-- id: bs-no-true-value -->

**Approach.** Start `hi` at the array length, which stands for "no true value". While `lo < hi`, the midpoint satisfies `lo <= mid < hi <= n`, so it is always a valid index and the array is never read at `n`. An all-false array pushes `lo` up to `n`, which is returned as the sentinel, and an empty array never enters the loop and returns 0. The program wraps the flags in an accessor that throws on an out-of-range read, and checks the all-false and empty cases against a linear scan.

**Complexity.** O(log n) time and O(1) extra space.

```java run
public final class NoTrueValue {
    static int firstTrue(boolean[] flags) {
        int lo = 0, hi = flags.length;
        while (lo < hi) {
            int mid = lo + (hi - lo) / 2;
            if (flags[mid]) hi = mid;
            else lo = mid + 1;
        }
        return lo;
    }
    static int firstTrueChecked(int n, int flip) {
        int lo = 0, hi = n;
        while (lo < hi) {
            int mid = lo + (hi - lo) / 2;
            if (mid < 0 || mid >= n) throw new AssertionError("read outside the array at " + mid);
            if (mid >= flip) hi = mid;
            else lo = mid + 1;
        }
        return lo;
    }

    public static void main(String[] args) {
        if (firstTrue(new boolean[] {false, false, false}) != 3) throw new AssertionError("example 1");
        if (firstTrue(new boolean[0]) != 0) throw new AssertionError("example 2");
        for (int n = 0; n <= 40; n++) {
            for (int flip = 0; flip <= n; flip++) {
                if (firstTrueChecked(n, flip) != flip) throw new AssertionError("n=" + n + " flip=" + flip);
            }
        }
        boolean[] allFalse = new boolean[100000];
        if (firstTrue(allFalse) != 100000) throw new AssertionError("a long all-false array");
    }
}
```

#### Solution: [Recognize] Kth Missing Positive Number (LeetCode 1539)
<!-- id: bs-kth-missing-positive -->

**Approach.** In a sorted array of distinct positive integers, the number of positive values missing before `arr[i]` is `arr[i] - (i + 1)`, and that count never decreases as `i` grows, so "at least k values are missing before position `i`" is a monotone predicate. Find the first position where it holds with a half-open search. The final `lo` is how many array values come before the k-th missing number, so the answer is `lo + k`, including when `lo` equals the array length. The oracle counts upward from 1, skipping values present in a set.

**Complexity.** O(log n) time and O(1) extra space.

```java run
import java.util.HashSet;
import java.util.Random;
import java.util.Set;
import java.util.TreeSet;

public final class KthMissingPositive {
    static int findKthPositive(int[] arr, int k) {
        int lo = 0, hi = arr.length;
        while (lo < hi) {
            int mid = lo + (hi - lo) / 2;
            if (arr[mid] - (mid + 1) >= k) hi = mid;
            else lo = mid + 1;
        }
        return lo + k;
    }
    static int oracle(int[] arr, int k) {
        Set<Integer> present = new HashSet<>();
        for (int v : arr) present.add(v);
        int seen = 0, x = 0;
        while (seen < k) { x++; if (!present.contains(x)) seen++; }
        return x;
    }

    public static void main(String[] args) {
        if (findKthPositive(new int[] {2, 3, 4, 7, 11}, 5) != 9) throw new AssertionError("example 1");
        if (findKthPositive(new int[] {1, 2, 3, 4}, 2) != 6) throw new AssertionError("example 2");
        Random rnd = new Random(641);
        for (int t = 0; t < 4000; t++) {
            TreeSet<Integer> set = new TreeSet<>();
            int n = 1 + rnd.nextInt(8);
            while (set.size() < n) set.add(1 + rnd.nextInt(20));
            int[] arr = new int[n];
            int i = 0;
            for (int v : set) arr[i++] = v;
            for (int k = 1; k <= 25; k++) {
                if (findKthPositive(arr, k) != oracle(arr, k)) throw new AssertionError("differs for k=" + k);
            }
        }
    }
}
```
