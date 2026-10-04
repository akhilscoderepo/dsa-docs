<!-- solutions-for: 06-binary-search -->
### Solutions For Where A Value Belongs

#### Solution: [Build] Search Insert Position (LeetCode 35)
<!-- id: bs-insert-35 -->

**Approach.**
The answer is the first index whose value is at least the target. The search uses the half-open interval `[lo, hi)` with `hi = nums.length`, so the end of the array is a legal answer. A value smaller than the target moves `lo` to `mid + 1`. Any other value keeps `mid` as a possible answer with `hi = mid`. The invariant is that every index below `lo` holds a smaller value and every index from `hi` on holds a value that is at least the target. The loop ends with `lo == hi`, and that index is both the position of the target when it occurs and its insertion place otherwise.

**Complexity.**
- **Time** is O(log n), because each step removes at least half of the interval.
- **Space** is O(1), because the code stores only `lo`, `hi` and `mid`.

```java run
import java.util.Arrays;
import java.util.Random;

public final class SearchInsert35 {
    /**
     * Returns the first index whose value is at least target, or nums.length.
     * Time: O(log n), because the interval halves each step.
     * Space: O(1), because only three indexes are stored.
     * Invariant: indexes below lo are smaller than target; indexes from hi on are not.
     */
    static int searchInsert(int[] nums, int target) {
        // hi starts at the length, so "after the last value" is a legal answer.
        int lo = 0, hi = nums.length;
        // The loop runs while the half-open interval [lo, hi) is not empty.
        while (lo < hi) {
            int mid = lo + (hi - lo) / 2;
            // A smaller value puts mid and everything before it on the left part.
            if (nums[mid] < target) lo = mid + 1;
            // Otherwise mid may be the answer, so hi keeps it.
            else hi = mid;
        }
        // lo == hi, and that index is the answer.
        return lo;
    }

    /** Closed-interval loop with hi = mid, run under an iteration cap to show that it never ends. */
    static boolean closedStyleStalls(int[] nums, int target) {
        int lo = 0, hi = nums.length - 1, steps = 0;
        while (lo <= hi) {
            if (++steps > 100) return true;
            int mid = lo + (hi - lo) / 2;
            if (nums[mid] < target) lo = mid + 1; else hi = mid;
        }
        return false;
    }

    public static void main(String[] args) {
        // The statement examples and the empty array.
        if (searchInsert(new int[] {2, 4, 7, 10}, 7) != 2) throw new AssertionError("example 1");
        if (searchInsert(new int[] {2, 4, 7, 10}, 5) != 2) throw new AssertionError("example 2");
        if (searchInsert(new int[0], 3) != 0) throw new AssertionError("empty");
        // Targets below and above every value reach both ends of the legal range.
        if (searchInsert(new int[] {2, 4}, 1) != 0 || searchInsert(new int[] {2, 4}, 9) != 2) throw new AssertionError("ends");
        // The claim about the closed interval: hi = mid stalls on {5} with target 5.
        if (!closedStyleStalls(new int[] {5}, 5)) throw new AssertionError("closed style should stall");
        // Random arrays against a linear scan.
        Random rnd = new Random(31);
        for (int t = 0; t < 3000; t++) {
            int[] a = rnd.ints(rnd.nextInt(12), -15, 15).distinct().sorted().toArray();
            int target = rnd.nextInt(34) - 17, expect = a.length;
            for (int i = a.length - 1; i >= 0; i--) if (a[i] >= target) expect = i;
            if (searchInsert(a, target) != expect) throw new AssertionError("random " + Arrays.toString(a) + " " + target);
        }
    }
}
```

#### Solution: [Vary] Upper Bound (Author exercise)
<!-- id: bs-upper-bound -->

**Approach.**
The upper bound changes one test. A value that is less than or equal to the target belongs to the left part, so `nums[mid] <= target` moves `lo` to `mid + 1`. A greater value keeps `mid` with `hi = mid`. The invariant is that indexes below `lo` hold values at most the target and indexes from `hi` on hold larger values. With duplicates, the loop skips the whole group of equal entries and stops just after it.

**Complexity.**
- **Time** is O(log n), because the interval halves each step.
- **Space** is O(1), because only three indexes are stored.

```java run
import java.util.Arrays;
import java.util.Random;

public final class UpperBound {
    /**
     * Returns the first index whose value is strictly greater than target, or nums.length.
     * Time: O(log n). Space: O(1).
     * Invariant: indexes below lo hold values at most target; indexes from hi on hold larger values.
     */
    static int upperBound(int[] nums, int target) {
        int lo = 0, hi = nums.length;
        // The loop runs while [lo, hi) is not empty.
        while (lo < hi) {
            int mid = lo + (hi - lo) / 2;
            // An equal value still belongs to the left part, so it is skipped.
            if (nums[mid] <= target) lo = mid + 1;
            else hi = mid;
        }
        return lo;
    }

    public static void main(String[] args) {
        // The statement examples.
        if (upperBound(new int[] {2, 4, 4, 4, 9, 9}, 4) != 4) throw new AssertionError("example 1");
        if (upperBound(new int[] {1, 2, 3}, 3) != 3) throw new AssertionError("example 2");
        // The library finds some index of 4 and not the bound, so it cannot replace this loop.
        int[] a = {2, 4, 4, 4, 9, 9};
        int any = Arrays.binarySearch(a, 4);
        if (any < 1 || any > 3) throw new AssertionError("library returns some index of 4");
        // Random arrays with duplicates against a linear scan.
        Random rnd = new Random(32);
        for (int t = 0; t < 3000; t++) {
            int[] b = rnd.ints(rnd.nextInt(14), 0, 6).sorted().toArray();
            int target = rnd.nextInt(9) - 1, expect = b.length;
            for (int i = b.length - 1; i >= 0; i--) if (b[i] > target) expect = i;
            if (upperBound(b, target) != expect) throw new AssertionError("random " + Arrays.toString(b) + " " + target);
        }
    }
}
```

#### Solution: [Boundary] Outside Range (Author exercise)
<!-- id: bs-outside-range -->

**Approach.**
A helper takes a flag that selects the keep test, `<` for the lower bound and `<=` for the upper bound. A target below every value fails the keep test at every probed index, so `hi` collapses to 0 and both bounds are 0. A target above every value passes the keep test at every probed index, so `lo` grows to `nums.length` and both bounds equal the length. The invariant of the half-open interval makes these ends reachable without a special case. The pair always satisfies `lower <= upper`, because the upper keep test accepts every index that the lower keep test accepts.

**Complexity.**
- **Time** is O(log n), because the method runs two searches of O(log n) each.
- **Space** is O(1), because the pair has fixed size.

```java run
import java.util.Arrays;
import java.util.Random;

public final class OutsideRange {
    /**
     * Returns the lower bound, or the upper bound when strict is true.
     * Time: O(log n). Space: O(1).
     * Invariant: indexes below lo pass the keep test; indexes from hi on fail it.
     */
    static int bound(int[] nums, int target, boolean strict) {
        int lo = 0, hi = nums.length;
        while (lo < hi) {
            int mid = lo + (hi - lo) / 2;
            // The flag chooses between "value <= target" and "value < target".
            boolean keep = strict ? nums[mid] <= target : nums[mid] < target;
            if (keep) lo = mid + 1; else hi = mid;
        }
        return lo;
    }

    /** Returns {lower, upper}. Time: O(log n). Space: O(1). */
    static int[] bounds(int[] nums, int target) {
        return new int[] {bound(nums, target, false), bound(nums, target, true)};
    }

    public static void main(String[] args) {
        // The statement examples at both ends of the legal range.
        if (!Arrays.equals(bounds(new int[] {2, 4, 4, 7}, 1), new int[] {0, 0})) throw new AssertionError("below");
        if (!Arrays.equals(bounds(new int[] {2, 4, 4, 7}, 9), new int[] {4, 4})) throw new AssertionError("above");
        // An inside target gives the group size as upper - lower.
        int[] r = bounds(new int[] {2, 4, 4, 7}, 4);
        if (r[0] != 1 || r[1] != 3) throw new AssertionError("group");
        // The count of values in the closed range [a, b] equals upper(b) - lower(a).
        int[] data = {1, 2, 2, 5, 5, 5, 8};
        if (bound(data, 5, true) - bound(data, 2, false) != 5) throw new AssertionError("range count");
        // Random arrays against a linear scan, with targets outside the data.
        Random rnd = new Random(33);
        for (int t = 0; t < 3000; t++) {
            int[] a = rnd.ints(rnd.nextInt(14), 0, 6).sorted().toArray();
            int target = rnd.nextInt(10) - 2, lo = 0, up = 0;
            for (int x : a) { if (x < target) lo++; if (x <= target) up++; }
            int[] got = bounds(a, target);
            if (got[0] != lo || got[1] != up || got[0] > got[1]) throw new AssertionError("random " + Arrays.toString(a) + " " + target);
        }
    }
}
```

#### Solution: [Recognize] Smallest Letter Greater Than Target (LeetCode 744)
<!-- id: bs-next-letter-744 -->

**Approach.**
The wanted letter sits at the upper bound of the target, the first index with a strictly greater letter. The half-open search finds that index with `hi = letters.length`. When the bound equals the array length, no letter is greater, and the contract returns the first letter. The expression `idx % letters.length` applies that wraparound in one place and leaves other indexes unchanged. The invariant is the upper bound invariant: indexes below `lo` hold letters at most the target.

**Complexity.**
- **Time** is O(log n), because the search halves the interval each step.
- **Space** is O(1), because the code stores only three indexes.

```java run
import java.util.Random;

public final class NextLetter744 {
    /**
     * Returns the smallest letter greater than target, wrapping to letters[0].
     * Time: O(log n). Space: O(1).
     * Invariant: indexes below lo hold letters at most target.
     */
    static char nextGreatest(char[] letters, char target) {
        int lo = 0, hi = letters.length;
        // Upper-bound search: equal letters belong to the left part.
        while (lo < hi) {
            int mid = lo + (hi - lo) / 2;
            if (letters[mid] <= target) lo = mid + 1; else hi = mid;
        }
        // The modulo maps the end-of-array result to index 0, as the contract says.
        return letters[lo % letters.length];
    }

    public static void main(String[] args) {
        char[] s = {'d', 'f', 'f', 'k'};
        // The statement examples.
        if (nextGreatest(s, 'f') != 'k') throw new AssertionError("example 1");
        if (nextGreatest(s, 'k') != 'd') throw new AssertionError("example 2");
        // A target below every letter returns the first letter without wrapping.
        if (nextGreatest(s, 'a') != 'd') throw new AssertionError("below");
        // Random sorted letter arrays against a linear scan.
        Random rnd = new Random(34);
        for (int t = 0; t < 3000; t++) {
            char[] a = new char[2 + rnd.nextInt(8)];
            for (int i = 0; i < a.length; i++) a[i] = (char) ('a' + rnd.nextInt(8));
            java.util.Arrays.sort(a);
            if (a[0] == a[a.length - 1]) continue;
            char target = (char) ('a' + rnd.nextInt(10));
            char expect = a[0];
            for (int i = a.length - 1; i >= 0; i--) if (a[i] > target) expect = a[i];
            if (nextGreatest(a, target) != expect) throw new AssertionError("random " + new String(a) + " " + target);
        }
    }
}
```
