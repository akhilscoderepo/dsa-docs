<!-- solutions-for: 06-binary-search -->
### Solutions For A Target After Rotation

#### Solution: [Build] Search In Rotated Sorted Array (LeetCode 33)
<!-- id: bs-rotated-search-33 -->

**Approach.**
A cut at `mid` leaves at least one half without the restart point, and that half is ascending. The comparison `nums[lo] <= nums[mid]` names the left half as sorted, and its failure names the right half. A range test on the sorted half then decides. If the target lies between the end values of the sorted half, the search keeps that half, and otherwise it keeps the other half. Each update drops `mid`, which was already compared. The invariant keeps a present target inside `[lo, hi]`, so an empty interval proves absence. The test needs `<=` for a two-index interval, where `mid` coincides with `lo`.

**Complexity.**
- **Time** is O(log n), because each step removes `mid` and at least half of the interval.
- **Space** is O(1), because the code stores only three indexes.

```java run
import java.util.Arrays;
import java.util.Random;

public final class RotatedSearch33 {
    /**
     * Returns the index of target in a rotated ascending array of distinct values, or -1.
     * Time: O(log n). Space: O(1).
     * Invariant: if target occurs in nums, its index lies in [lo, hi].
     */
    static int search(int[] nums, int target) {
        int lo = 0, hi = nums.length - 1;
        while (lo <= hi) {
            int mid = lo + (hi - lo) / 2;
            // Equality ends the search before any half is chosen.
            if (nums[mid] == target) return mid;
            // The left half is ascending when its first value does not exceed the middle value.
            if (nums[lo] <= nums[mid]) {
                // Range test on the sorted left half: keep it only if the target lies inside.
                if (nums[lo] <= target && target < nums[mid]) hi = mid - 1; else lo = mid + 1;
            } else {
                // Otherwise the right half is ascending; keep it only if the target lies inside.
                if (nums[mid] < target && target <= nums[hi]) lo = mid + 1; else hi = mid - 1;
            }
        }
        return -1;
    }

    public static void main(String[] args) {
        int[] a = {9, 11, 14, 2, 4, 6};
        // The statement examples and the empty array.
        if (search(a, 4) != 4) throw new AssertionError("example 1");
        if (search(a, 5) != -1) throw new AssertionError("example 2");
        if (search(new int[0], 1) != -1) throw new AssertionError("empty");
        // The plain search of the first lesson can miss: on [6,7,9,1,2,3,4] it never finds 7.
        int[] w = {6, 7, 9, 1, 2, 3, 4};
        if (Arrays.binarySearch(w, 7) >= 0) throw new AssertionError("plain search should miss 7 here");
        if (search(w, 7) != 1) throw new AssertionError("rotated search finds 7");
        // Random rotations, with present and absent targets, against a scan.
        Random rnd = new Random(71);
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(14), k = rnd.nextInt(n), v = 0;
            int[] s = new int[n], r = new int[n];
            for (int i = 0; i < n; i++) s[i] = v += 1 + rnd.nextInt(3);
            for (int i = 0; i < n; i++) r[i] = s[(i - k + n) % n];
            int target = rnd.nextInt(v + 3), expect = -1;
            for (int i = 0; i < n; i++) if (r[i] == target) expect = i;
            if (search(r, target) != expect) throw new AssertionError("random " + Arrays.toString(r) + " " + target);
        }
    }
}
```

#### Solution: [Vary] Pivot Then Search (Author exercise)
<!-- id: bs-pivot-then-search -->

**Approach.**
The first phase finds the minimum index `p` with the right endpoint rule from the previous lesson. The array is then two ascending runs, `[0, p - 1]` and `[p, n - 1]`, or one run when `p` is 0. Every value of the left run is at least `nums[0]` and every value of the right run is smaller, so the comparison `target >= nums[0]` picks the run that can hold the target. The second phase is the exact search of the first lesson on that run, with indexes taken from `nums`. The invariant of phase one is that the minimum index lies in `[lo, hi]`, and the invariant of phase two is that the target lies in its own `[l, h]`.

**Complexity.**
- **Time** is O(log n), because two searches of O(log n) run one after the other.
- **Space** is O(1), because the code stores a few indexes.

```java run
import java.util.Arrays;
import java.util.Random;

public final class PivotThenSearch {
    /**
     * Returns the index of target, or -1, by finding the minimum first.
     * Time: O(log n). Space: O(1).
     * Invariant: phase one keeps the minimum index in [lo, hi]; phase two keeps the target in [l, h].
     */
    static int search(int[] nums, int target) {
        int n = nums.length, lo = 0, hi = n - 1;
        // Phase one: locate the minimum with the right endpoint comparison.
        while (lo < hi) {
            int mid = lo + (hi - lo) / 2;
            if (nums[mid] > nums[hi]) lo = mid + 1; else hi = mid;
        }
        int p = lo;
        // Choose the run: the whole array when p == 0, otherwise the left run if target >= nums[0].
        int l, h;
        if (p == 0) { l = 0; h = n - 1; }
        else if (target >= nums[0]) { l = 0; h = p - 1; }
        else { l = p; h = n - 1; }
        // Phase two: exact search on the chosen ascending run.
        while (l <= h) {
            int mid = l + (h - l) / 2;
            if (nums[mid] == target) return mid;
            if (nums[mid] < target) l = mid + 1; else h = mid - 1;
        }
        return -1;
    }

    public static void main(String[] args) {
        int[] a = {9, 11, 14, 2, 4, 6};
        // The statement examples.
        if (search(a, 11) != 1) throw new AssertionError("example 1");
        if (search(a, 2) != 3) throw new AssertionError("example 2");
        // An unrotated array uses the whole range.
        if (search(new int[] {1, 3, 5}, 5) != 2) throw new AssertionError("unrotated");
        // Random rotations against a scan.
        Random rnd = new Random(72);
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(14), k = rnd.nextInt(n), v = 0;
            int[] s = new int[n], r = new int[n];
            for (int i = 0; i < n; i++) s[i] = v += 1 + rnd.nextInt(3);
            for (int i = 0; i < n; i++) r[i] = s[(i - k + n) % n];
            int target = rnd.nextInt(v + 3), expect = -1;
            for (int i = 0; i < n; i++) if (r[i] == target) expect = i;
            if (search(r, target) != expect) throw new AssertionError("random " + Arrays.toString(r) + " " + target);
        }
    }
}
```

#### Solution: [Boundary] Search With Duplicates (LeetCode 81)
<!-- id: bs-rotated-search-81 -->

**Approach.**
With repeated values, `nums[lo] <= nums[mid]` no longer proves that the left half is ascending. When `nums[lo]`, `nums[mid]` and `nums[hi]` are all equal, no half is proved sorted. The value at `mid` is not the target, so equal copies at `lo` and `hi` are not the target either, and both ends are dropped. Other cases keep the rule of the distinct-value search, with `<` and `<=` adjusted so equal values stay on the safe side. The invariant keeps a present target inside `[lo, hi]`. An array of equal values forces about `n / 2` iterations, so the worst case is O(n).

**Complexity.**
- **Time** is O(log n) when few values repeat and O(n) in the worst case, because a three-way tie removes only two indexes.
- **Space** is O(1), because the code stores only three indexes.

```java run
import java.util.Arrays;
import java.util.Random;

public final class RotatedSearch81 {
    static int iterations;

    /**
     * Returns true when target occurs in a rotated non-decreasing array.
     * Time: O(log n) typical, O(n) worst case. Space: O(1).
     * Invariant: if target occurs in nums, some occurrence lies in [lo, hi].
     */
    static boolean search(int[] nums, int target) {
        int lo = 0, hi = nums.length - 1;
        iterations = 0;
        while (lo <= hi) {
            iterations++;
            int mid = lo + (hi - lo) / 2;
            if (nums[mid] == target) return true;
            // A three-way tie proves nothing; both ends differ from the target, so drop them.
            if (nums[lo] == nums[mid] && nums[mid] == nums[hi]) { lo++; hi--; }
            // The left half is ascending here.
            else if (nums[lo] <= nums[mid]) {
                if (nums[lo] <= target && target < nums[mid]) hi = mid - 1; else lo = mid + 1;
            // Otherwise the right half is ascending.
            } else {
                if (nums[mid] < target && target <= nums[hi]) lo = mid + 1; else hi = mid - 1;
            }
        }
        return false;
    }

    public static void main(String[] args) {
        // The statement examples.
        if (!search(new int[] {1, 0, 1, 1, 1}, 0)) throw new AssertionError("example 1");
        if (search(new int[] {2, 2, 2, 3, 2, 2}, 4)) throw new AssertionError("example 2");
        // The worst case is linear: equal values with an absent target take about n / 2 iterations.
        int[] same = new int[1000];
        Arrays.fill(same, 7);
        search(same, 8);
        if (iterations != 500) throw new AssertionError("iterations " + iterations);
        // Random rotations with many duplicates against a scan.
        Random rnd = new Random(73);
        for (int t = 0; t < 5000; t++) {
            int n = 1 + rnd.nextInt(14), k = rnd.nextInt(n);
            int[] s = rnd.ints(n, 0, 5).sorted().toArray(), r = new int[n];
            for (int i = 0; i < n; i++) r[i] = s[(i - k + n) % n];
            int target = rnd.nextInt(7) - 1;
            boolean expect = false;
            for (int x : r) if (x == target) expect = true;
            if (search(r, target) != expect) throw new AssertionError("random " + Arrays.toString(r) + " " + target);
        }
    }
}
```

#### Solution: [Recognize] Explain Both Strategies (Author exercise)
<!-- id: bs-compare-strategies -->

**Approach.**
Both strategies are written once with a counter in each loop. The one-pass search needs one loop of at most `floor(log2(n)) + 1` iterations. The two-phase method needs the minimum search, at most `floor(log2(n))` iterations, and then an exact search over a run of at most `n` values. Its total is therefore larger by a constant factor of about two. The proof obligations differ. The one-pass search must prove at each step that the range test discards only a half that cannot hold the target, and it relies on the sorted half. The two-phase method proves the right endpoint rule once and the run choice `target >= nums[0]` once. The test checks that both strategies agree on the answer, and that their step counts stay within the stated bounds.

**Complexity.**
- **Time** is O(log n) for both strategies, because each loop halves its interval.
- **Space** is O(1), because only a few indexes and counters are stored.

```java run
import java.util.Arrays;
import java.util.Random;

public final class CompareStrategies {
    /**
     * Returns {index, iterations} for the one-pass search.
     * Time: O(log n). Space: O(1). Invariant: the target lies in [lo, hi] if present.
     */
    static int[] onePass(int[] nums, int target) {
        int lo = 0, hi = nums.length - 1, it = 0;
        while (lo <= hi) {
            it++;
            int mid = lo + (hi - lo) / 2;
            if (nums[mid] == target) return new int[] {mid, it};
            if (nums[lo] <= nums[mid]) {
                if (nums[lo] <= target && target < nums[mid]) hi = mid - 1; else lo = mid + 1;
            } else {
                if (nums[mid] < target && target <= nums[hi]) lo = mid + 1; else hi = mid - 1;
            }
        }
        return new int[] {-1, it};
    }

    /**
     * Returns {index, iterations} for the minimum search followed by an exact search.
     * Time: O(log n). Space: O(1). Invariant: phase one keeps the minimum in [lo, hi].
     */
    static int[] twoPhase(int[] nums, int target) {
        int n = nums.length, lo = 0, hi = n - 1, it = 0;
        while (lo < hi) {
            it++;
            int mid = lo + (hi - lo) / 2;
            if (nums[mid] > nums[hi]) lo = mid + 1; else hi = mid;
        }
        int p = lo, l, h;
        if (p == 0) { l = 0; h = n - 1; } else if (target >= nums[0]) { l = 0; h = p - 1; } else { l = p; h = n - 1; }
        while (l <= h) {
            it++;
            int mid = l + (h - l) / 2;
            if (nums[mid] == target) return new int[] {mid, it};
            if (nums[mid] < target) l = mid + 1; else h = mid - 1;
        }
        return new int[] {-1, it};
    }

    public static void main(String[] args) {
        int[] a = {9, 11, 14, 2, 4, 6};
        // The statement examples as [onePass, twoPhase] counts.
        if (onePass(a, 4)[1] != 2 || twoPhase(a, 4)[1] != 4) throw new AssertionError("example 1");
        if (onePass(a, 5)[1] != 3 || twoPhase(a, 5)[1] != 5) throw new AssertionError("example 2");
        // Random rotations: both strategies agree and stay within logarithmic bounds.
        Random rnd = new Random(74);
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(60), k = rnd.nextInt(n), v = 0;
            int[] s = new int[n], r = new int[n];
            for (int i = 0; i < n; i++) s[i] = v += 1 + rnd.nextInt(3);
            for (int i = 0; i < n; i++) r[i] = s[(i - k + n) % n];
            int target = rnd.nextInt(v + 3);
            int[] x = onePass(r, target), y = twoPhase(r, target);
            if (x[0] != y[0]) throw new AssertionError("disagree " + Arrays.toString(r) + " " + target);
            int bound = 32 - Integer.numberOfLeadingZeros(n);
            if (x[1] > bound || y[1] > 2 * bound) throw new AssertionError("bounds " + x[1] + " " + y[1]);
        }
    }
}
```
