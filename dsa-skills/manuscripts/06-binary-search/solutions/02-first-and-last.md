<!-- solutions-for: 06-first-and-last -->
### First And Last

#### Solution: [Build] First Occurrence (Author exercise)
<!-- id: bs-first-occurrence -->

**Approach.** Keep a closed interval and a candidate that starts at minus one. A middle value below the target moves `lo` up and one above it moves `hi` down. On equality, record the position and move `hi` to `mid - 1`, because any smaller index equal to the target must lie to the left. When the interval is empty the last recorded candidate is the leftmost occurrence. The check compares with a linear scan on random arrays with many repeats, and counts readings on an array of identical values to show that the method stays logarithmic.

**Complexity.** O(log n) time and O(1) extra space.

```java run
import java.util.Arrays;
import java.util.Random;

public final class FirstOccurrence {
    static int reads;

    static int firstOccurrence(int[] a, int target) {
        int lo = 0, hi = a.length - 1, candidate = -1;
        while (lo <= hi) {
            int mid = lo + (hi - lo) / 2;
            reads++;
            if (a[mid] < target) lo = mid + 1;
            else if (a[mid] > target) hi = mid - 1;
            else { candidate = mid; hi = mid - 1; }
        }
        return candidate;
    }
    static int scan(int[] a, int target) {
        for (int i = 0; i < a.length; i++) if (a[i] == target) return i;
        return -1;
    }

    public static void main(String[] args) {
        if (firstOccurrence(new int[] {2, 2, 5, 5, 5, 9}, 5) != 2) throw new AssertionError("example 1");
        if (firstOccurrence(new int[] {1, 3}, 4) != -1) throw new AssertionError("example 2");
        int[] same = new int[100000];
        Arrays.fill(same, 8);
        reads = 0;
        if (firstOccurrence(same, 8) != 0) throw new AssertionError("all equal");
        if (reads > 18) throw new AssertionError("too many readings: " + reads);
        Random rnd = new Random(611);
        for (int t = 0; t < 4000; t++) {
            int n = rnd.nextInt(14);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(6);
            Arrays.sort(a);
            for (int target = -1; target <= 6; target++) {
                if (firstOccurrence(a, target) != scan(a, target)) throw new AssertionError("differs on " + Arrays.toString(a) + " target " + target);
            }
        }
    }
}
```

#### Solution: [Vary] Last Occurrence (Author exercise)
<!-- id: bs-last-occurrence -->

**Approach.** The loop mirrors the first-occurrence search with the direction after a hit reversed: record the position and move `lo` to `mid + 1`, since a larger index equal to the target can only be to the right. The final candidate is the rightmost occurrence. The check compares with a backwards linear scan on random arrays with repeats and verifies the all-equal case.

**Complexity.** O(log n) time and O(1) extra space.

```java run
import java.util.Arrays;
import java.util.Random;

public final class LastOccurrence {
    static int lastOccurrence(int[] a, int target) {
        int lo = 0, hi = a.length - 1, candidate = -1;
        while (lo <= hi) {
            int mid = lo + (hi - lo) / 2;
            if (a[mid] < target) lo = mid + 1;
            else if (a[mid] > target) hi = mid - 1;
            else { candidate = mid; lo = mid + 1; }
        }
        return candidate;
    }
    static int backwardScan(int[] a, int target) {
        for (int i = a.length - 1; i >= 0; i--) if (a[i] == target) return i;
        return -1;
    }

    public static void main(String[] args) {
        if (lastOccurrence(new int[] {2, 2, 5, 5, 5, 9}, 5) != 4) throw new AssertionError("example 1");
        if (lastOccurrence(new int[] {6, 6, 6}, 6) != 2) throw new AssertionError("example 2");
        if (lastOccurrence(new int[0], 1) != -1) throw new AssertionError("empty array");
        Random rnd = new Random(612);
        for (int t = 0; t < 4000; t++) {
            int n = rnd.nextInt(14);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(6);
            Arrays.sort(a);
            for (int target = -1; target <= 6; target++) {
                if (lastOccurrence(a, target) != backwardScan(a, target)) throw new AssertionError("differs on " + Arrays.toString(a) + " target " + target);
            }
        }
    }
}
```

#### Solution: [Boundary] Find First and Last Position of Element in Sorted Array (LeetCode 34)
<!-- id: bs-search-range -->

**Approach.** Run the leftmost search, and if it returns minus one, return the pair of minus ones without a second search. Otherwise run the rightmost search and return both positions. For an array of identical values equal to the target, the first search keeps moving left and the second keeps moving right, so each takes a logarithmic number of readings, and the pair spans the whole array. The check compares with a scan for the first and last matching index on random arrays, and counts readings on a long run.

**Complexity.** O(log n) time and O(1) extra space.

```java run
import java.util.Arrays;
import java.util.Random;

public final class SearchRange {
    static int reads;

    static int bound(int[] a, int target, boolean wantFirst) {
        int lo = 0, hi = a.length - 1, candidate = -1;
        while (lo <= hi) {
            int mid = lo + (hi - lo) / 2;
            reads++;
            if (a[mid] < target) lo = mid + 1;
            else if (a[mid] > target) hi = mid - 1;
            else { candidate = mid; if (wantFirst) hi = mid - 1; else lo = mid + 1; }
        }
        return candidate;
    }
    static int[] searchRange(int[] a, int target) {
        int first = bound(a, target, true);
        if (first == -1) return new int[] {-1, -1};
        return new int[] {first, bound(a, target, false)};
    }
    static int[] scan(int[] a, int target) {
        int first = -1, last = -1;
        for (int i = 0; i < a.length; i++) if (a[i] == target) { if (first == -1) first = i; last = i; }
        return new int[] {first, last};
    }

    public static void main(String[] args) {
        if (!Arrays.equals(searchRange(new int[] {3, 3, 3, 3}, 3), new int[] {0, 3})) throw new AssertionError("example 1");
        if (!Arrays.equals(searchRange(new int[] {1, 2, 4}, 3), new int[] {-1, -1})) throw new AssertionError("example 2");
        int[] same = new int[50000];
        Arrays.fill(same, 4);
        reads = 0;
        if (!Arrays.equals(searchRange(same, 4), new int[] {0, 49999})) throw new AssertionError("whole-array run");
        if (reads > 34) throw new AssertionError("a long run must not cost a walk: " + reads);
        Random rnd = new Random(613);
        for (int t = 0; t < 4000; t++) {
            int n = rnd.nextInt(14);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(5);
            Arrays.sort(a);
            for (int target = -1; target <= 5; target++) {
                if (!Arrays.equals(searchRange(a, target), scan(a, target))) throw new AssertionError("differs on " + Arrays.toString(a) + " target " + target);
            }
        }
    }
}
```

#### Solution: [Recognize] First Bad Version (LeetCode 278)
<!-- id: bs-first-bad-version -->

**Approach.** The predicate is monotone, so a bad version proves that every later version is bad and a good version proves that every earlier one is good. Keep a closed interval over versions and a candidate that starts at `n`. On a bad version record it and move `hi` to `mid - 1`, and on a good version move `lo` to `mid + 1`. Each predicate call halves the interval, so the number of calls is at most the number of binary digits of `n`. The test counts calls for every first-bad position of small `n`, and for large `n` with a predicate defined by a threshold.

**Complexity.** O(log n) predicate calls and O(1) extra space.

```java run
import java.util.function.IntPredicate;

public final class FirstBadVersion {
    static int calls;

    static int firstBadVersion(int n, IntPredicate isBad) {
        int lo = 1, hi = n, candidate = n;
        while (lo <= hi) {
            int mid = lo + (hi - lo) / 2;
            calls++;
            if (isBad.test(mid)) { candidate = mid; hi = mid - 1; }
            else lo = mid + 1;
        }
        return candidate;
    }

    public static void main(String[] args) {
        if (firstBadVersion(10, v -> v >= 4) != 4) throw new AssertionError("example 1");
        if (firstBadVersion(1, v -> v >= 1) != 1) throw new AssertionError("example 2");
        for (int n = 1; n <= 200; n++) {
            for (int bad = 1; bad <= n; bad++) {
                final int threshold = bad;
                calls = 0;
                if (firstBadVersion(n, v -> v >= threshold) != bad) throw new AssertionError("wrong answer for n=" + n + " bad=" + bad);
                int digits = 32 - Integer.numberOfLeadingZeros(n);
                if (calls > digits) throw new AssertionError("too many calls: " + calls + " for n=" + n);
            }
        }
        int n = 2_000_000_000, threshold = 1_999_999_999;
        calls = 0;
        if (firstBadVersion(n, v -> v >= threshold) != threshold) throw new AssertionError("large n");
        if (calls > 31) throw new AssertionError("large n needs at most 31 calls: " + calls);
    }
}
```
