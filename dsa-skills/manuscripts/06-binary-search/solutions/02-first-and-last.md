<!-- solutions-for: 06-binary-search -->
### Solutions For First Or Last Match

#### Solution: [Build] First Occurrence (Author exercise)
<!-- id: bs-first-occurrence -->

**Approach.**
A match at `mid` is only a candidate. The search stores `mid` as the candidate and discards the right half, because a smaller matching index can only lie on the left. A smaller entry moves `lo` right, and a larger entry moves `hi` left. The invariant is that the smallest matching index is either the stored candidate or inside `[lo, hi]`. The loop ends on an empty interval, so the candidate is the answer, and `-1` means no entry matched.

**Complexity.**
- **Time** is O(log n), because every step removes `mid` and at least half of the interval, also on a match.
- **Space** is O(1), because the code stores only the bounds and the candidate.

```java run
import java.util.Arrays;
import java.util.Random;

public final class FirstOccurrence {
    /**
     * Returns the smallest index holding target in a non-decreasing array, or -1.
     * Time: O(log n), because the interval shrinks by at least half each step.
     * Space: O(1), because only three indexes are stored.
     * Invariant: the smallest matching index equals candidate or lies in [lo, hi].
     */
    static int first(int[] nums, int target) {
        // candidate starts at -1, the answer for "no match".
        int lo = 0, hi = nums.length - 1, candidate = -1;
        // The loop runs while the interval holds a possible better match.
        while (lo <= hi) {
            int mid = lo + (hi - lo) / 2;
            // A match is stored, then the search moves left to look for an earlier one.
            if (nums[mid] == target) { candidate = mid; hi = mid - 1; }
            // A smaller middle value discards indexes lo..mid.
            else if (nums[mid] < target) lo = mid + 1;
            // A larger middle value discards indexes mid..hi.
            else hi = mid - 1;
        }
        return candidate;
    }

    public static void main(String[] args) {
        // The statement examples and the empty array.
        if (first(new int[] {5, 7, 7, 7, 7, 9}, 7) != 1) throw new AssertionError("example 1");
        if (first(new int[] {2, 2, 2, 2}, 3) != -1) throw new AssertionError("example 2");
        if (first(new int[0], 1) != -1) throw new AssertionError("empty");
        // An all-equal array returns index 0.
        if (first(new int[] {4, 4, 4, 4, 4}, 4) != 0) throw new AssertionError("all equal");
        // The library may return any matching index, so it is not a first-match tool.
        int[] same = new int[100];
        int any = Arrays.binarySearch(same, 0);
        if (any < 0 || any == 0) throw new AssertionError("library should pick the middle here, not index 0");
        // Random arrays with many duplicates against a linear scan.
        Random rnd = new Random(21);
        for (int t = 0; t < 3000; t++) {
            int[] a = rnd.ints(rnd.nextInt(14), 0, 6).sorted().toArray();
            int target = rnd.nextInt(8) - 1, expect = -1;
            for (int i = a.length - 1; i >= 0; i--) if (a[i] == target) expect = i;
            if (first(a, target) != expect) throw new AssertionError("random " + Arrays.toString(a) + " " + target);
        }
    }
}
```

#### Solution: [Vary] Last Occurrence (Author exercise)
<!-- id: bs-last-occurrence -->

**Approach.**
The method mirrors the first-occurrence search. A match at `mid` becomes the candidate and `lo` moves to `mid + 1`. A larger matching index can only lie on the right. The other two branches stay the same. The invariant is that the largest matching index equals the candidate or lies in `[lo, hi]`.

**Complexity.**
- **Time** is O(log n), because each step removes `mid` and at least half of the interval.
- **Space** is O(1), because only the bounds and the candidate are stored.

```java run
import java.util.Arrays;
import java.util.Random;

public final class LastOccurrence {
    /**
     * Returns the largest index holding target in a non-decreasing array, or -1.
     * Time: O(log n), because the interval shrinks by at least half each step.
     * Space: O(1), because only three indexes are stored.
     * Invariant: the largest matching index equals candidate or lies in [lo, hi].
     */
    static int last(int[] nums, int target) {
        int lo = 0, hi = nums.length - 1, candidate = -1;
        // The loop runs while a better match may remain.
        while (lo <= hi) {
            int mid = lo + (hi - lo) / 2;
            // A match is stored, then the search moves right for a later one.
            if (nums[mid] == target) { candidate = mid; lo = mid + 1; }
            else if (nums[mid] < target) lo = mid + 1;
            else hi = mid - 1;
        }
        return candidate;
    }

    public static void main(String[] args) {
        // The statement examples.
        if (last(new int[] {4, 7, 7, 7, 9, 9, 9}, 7) != 3) throw new AssertionError("example 1");
        if (last(new int[] {1, 1, 1, 1}, 1) != 3) throw new AssertionError("example 2");
        if (last(new int[0], 5) != -1) throw new AssertionError("empty");
        // Random arrays with many duplicates against a linear scan.
        Random rnd = new Random(22);
        for (int t = 0; t < 3000; t++) {
            int[] a = rnd.ints(rnd.nextInt(14), 0, 6).sorted().toArray();
            int target = rnd.nextInt(8) - 1, expect = -1;
            for (int i = 0; i < a.length; i++) if (a[i] == target) expect = i;
            if (last(a, target) != expect) throw new AssertionError("random " + Arrays.toString(a) + " " + target);
        }
    }
}
```

#### Solution: [Boundary] First And Last Position (LeetCode 34)
<!-- id: bs-range-34 -->

**Approach.**
The method runs one search per bound. A single helper takes a flag that chooses which side a match discards, so the two searches share all other code. If the first search returns `-1`, no entry matches and the method returns `[-1,-1]` at once, so the second search cannot produce a half-filled pair. For an array of one repeated value the first search ends at index 0 and the second at the last index. The invariant of each search is the one from the previous two exercises.

**Complexity.**
- **Time** is O(log n), because the method runs two searches of O(log n) each.
- **Space** is O(1), because the result array has fixed size 2.

```java run
import java.util.Arrays;
import java.util.Random;

public final class FirstAndLastPosition {
    /**
     * Returns the first or last index of target, chosen by wantFirst, or -1.
     * Time: O(log n). Space: O(1).
     * Invariant: the wanted extreme equals candidate or lies in [lo, hi].
     */
    static int bound(int[] nums, int target, boolean wantFirst) {
        int lo = 0, hi = nums.length - 1, candidate = -1;
        while (lo <= hi) {
            int mid = lo + (hi - lo) / 2;
            if (nums[mid] == target) {
                // Store the match, then discard the side that cannot beat it.
                candidate = mid;
                if (wantFirst) hi = mid - 1; else lo = mid + 1;
            } else if (nums[mid] < target) lo = mid + 1;
            else hi = mid - 1;
        }
        return candidate;
    }

    /**
     * Returns {first, last} or {-1, -1}.
     * Time: O(log n), two searches. Space: O(1), a pair of fixed size.
     */
    static int[] range(int[] nums, int target) {
        // The first search decides whether any entry matches.
        int first = bound(nums, target, true);
        // An absent target must return a complete pair of -1 values.
        if (first == -1) return new int[] {-1, -1};
        // The second search finds the right end of the same group.
        return new int[] {first, bound(nums, target, false)};
    }

    public static void main(String[] args) {
        // The statement examples.
        if (!Arrays.equals(range(new int[] {3, 3, 3, 3}, 3), new int[] {0, 3})) throw new AssertionError("example 1");
        if (!Arrays.equals(range(new int[] {1, 4, 4, 6}, 5), new int[] {-1, -1})) throw new AssertionError("example 2");
        if (!Arrays.equals(range(new int[0], 5), new int[] {-1, -1})) throw new AssertionError("empty");
        // The group size follows from the pair.
        int[] r = range(new int[] {1, 4, 4, 4, 6}, 4);
        if (r[1] - r[0] + 1 != 3) throw new AssertionError("count");
        // Random arrays against a scan, including absent targets.
        Random rnd = new Random(23);
        for (int t = 0; t < 3000; t++) {
            int[] a = rnd.ints(rnd.nextInt(14), 0, 6).sorted().toArray();
            int target = rnd.nextInt(8) - 1, f = -1, l = -1;
            for (int i = 0; i < a.length; i++) if (a[i] == target) { if (f == -1) f = i; l = i; }
            if (!Arrays.equals(range(a, target), new int[] {f, l})) throw new AssertionError("random " + Arrays.toString(a) + " " + target);
        }
    }
}
```

#### Solution: [Recognize] First Bad Version (LeetCode 278)
<!-- id: bs-first-bad -->

**Approach.**
The oracle `isBad` is monotone, so a bad version at `mid` is a candidate and every later version is bad too. The search stores the candidate and moves `hi` to `mid - 1`. A good version at `mid` rules out all versions up to `mid`, so `lo` moves to `mid + 1`. The invariant is that the first bad version equals the candidate or lies in `[lo, hi]`. The bounds are `long` values here so that `n` near `2^31 - 1` cannot overflow, and the midpoint uses the subtraction form. The test counts oracle calls and checks the limit of 32.

**Complexity.**
- **Time** is O(log n), because the interval halves each step and the oracle is called once per step.
- **Space** is O(1), because only the bounds and the candidate are stored.

```java run
import java.util.Random;
import java.util.function.LongPredicate;

public final class FirstBadVersion {
    /**
     * Returns the smallest version v in 1..n with isBad(v) true.
     * Time: O(log n) oracle calls. Space: O(1).
     * Invariant: the first bad version equals candidate or lies in [lo, hi].
     */
    static long firstBad(long n, LongPredicate isBad) {
        long lo = 1, hi = n, candidate = -1;
        // The loop runs while an earlier bad version may remain.
        while (lo <= hi) {
            // The subtraction form is safe for any bounds.
            long mid = lo + (hi - lo) / 2;
            // A bad version is a candidate; search the left side for an earlier one.
            if (isBad.test(mid)) { candidate = mid; hi = mid - 1; }
            // A good version rules out everything up to mid.
            else lo = mid + 1;
        }
        return candidate;
    }

    public static void main(String[] args) {
        // The statement examples.
        if (firstBad(9, v -> v >= 6) != 6) throw new AssertionError("example 1");
        if (firstBad(1, v -> v >= 1) != 1) throw new AssertionError("example 2");
        // The call limit of 32 holds for the largest n, and the answer is the last version.
        long big = Integer.MAX_VALUE;
        int[] calls = {0};
        long got = firstBad(big, v -> { calls[0]++; return v >= big; });
        if (got != big || calls[0] > 32) throw new AssertionError("large n " + got + " calls " + calls[0]);
        // The sum of two large bounds does not fit in an int, which is why the midpoint subtracts.
        int a = Integer.MAX_VALUE - 5, b = Integer.MAX_VALUE;
        if ((a + b) / 2 >= 0) throw new AssertionError("int sum should wrap");
        // Random thresholds against a linear scan.
        Random rnd = new Random(24);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(40), bad = 1 + rnd.nextInt(n);
            if (firstBad(n, v -> v >= bad) != bad) throw new AssertionError("random " + n + " " + bad);
        }
    }
}
```
