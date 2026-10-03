<!-- solutions-for: 06-lower-and-upper-bounds -->
### Lower And Upper Bounds

#### Solution: [Build] Search Insert Position (LeetCode 35)
<!-- id: bs-search-insert -->

**Approach.** The positions in a sorted array split into a prefix of values smaller than the target and a suffix of values at least as large, and the answer is the first position of the suffix. Use a half-open interval `[lo, hi)` with `hi = n`. If the value at `mid` is smaller than the target, the answer is to its right, so `lo = mid + 1`. Otherwise `mid` may be the answer, so `hi = mid`. The loop ends with `lo == hi`, which is the answer, possibly `n`. The check compares with a linear walk on random arrays and targets around the values.

**Complexity.** O(log n) time and O(1) extra space.

```java run
import java.util.Random;
import java.util.TreeSet;

public final class SearchInsertPosition {
    static int searchInsert(int[] a, int target) {
        int lo = 0, hi = a.length;
        while (lo < hi) {
            int mid = lo + (hi - lo) / 2;
            if (a[mid] < target) lo = mid + 1;
            else hi = mid;
        }
        return lo;
    }
    static int walk(int[] a, int target) {
        int i = 0;
        while (i < a.length && a[i] < target) i++;
        return i;
    }

    public static void main(String[] args) {
        if (searchInsert(new int[] {2, 4, 7, 9}, 7) != 2) throw new AssertionError("example 1");
        if (searchInsert(new int[] {2, 4, 7, 9}, 5) != 2) throw new AssertionError("example 2");
        if (searchInsert(new int[] {2, 4, 7, 9}, 10) != 4) throw new AssertionError("past the end");
        if (searchInsert(new int[0], 3) != 0) throw new AssertionError("empty array");
        Random rnd = new Random(621);
        for (int t = 0; t < 3000; t++) {
            TreeSet<Integer> set = new TreeSet<>();
            int n = rnd.nextInt(10);
            while (set.size() < n) set.add(rnd.nextInt(30) - 15);
            int[] a = new int[n];
            int k = 0;
            for (int v : set) a[k++] = v;
            for (int target = -17; target <= 17; target++) {
                if (searchInsert(a, target) != walk(a, target)) throw new AssertionError("differs for target " + target);
            }
        }
    }
}
```

#### Solution: [Vary] Upper Bound (Author exercise)
<!-- id: bs-upper-bound -->

**Approach.** The loop is the lower-bound loop with a different predicate: a value less than or equal to the target is still before the answer, so `lo = mid + 1`, and a larger value may be the answer, so `hi = mid`. The result is the first position behind every copy of the target. The number of copies is the upper bound minus the lower bound, and the check compares both bounds and the count with a linear scan on random arrays with many repeats.

**Complexity.** O(log n) time and O(1) extra space.

```java run
import java.util.Arrays;
import java.util.Random;

public final class UpperBound {
    static int lowerBound(int[] a, int target) {
        int lo = 0, hi = a.length;
        while (lo < hi) {
            int mid = lo + (hi - lo) / 2;
            if (a[mid] < target) lo = mid + 1;
            else hi = mid;
        }
        return lo;
    }
    static int upperBound(int[] a, int target) {
        int lo = 0, hi = a.length;
        while (lo < hi) {
            int mid = lo + (hi - lo) / 2;
            if (a[mid] <= target) lo = mid + 1;
            else hi = mid;
        }
        return lo;
    }

    public static void main(String[] args) {
        int[] ex = {1, 2, 2, 2, 5};
        if (upperBound(ex, 2) != 4 || upperBound(ex, 2) - lowerBound(ex, 2) != 3) throw new AssertionError("example 1");
        if (upperBound(ex, 0) != 0) throw new AssertionError("example 2");
        Random rnd = new Random(622);
        for (int t = 0; t < 4000; t++) {
            int n = rnd.nextInt(14);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(6);
            Arrays.sort(a);
            for (int target = -1; target <= 6; target++) {
                int greater = 0, less = 0, equal = 0;
                for (int v : a) { if (v > target) greater++; else if (v < target) less++; else equal++; }
                if (upperBound(a, target) != n - greater) throw new AssertionError("upper bound differs on " + Arrays.toString(a) + " target " + target);
                if (lowerBound(a, target) != less) throw new AssertionError("lower bound differs");
                if (upperBound(a, target) - lowerBound(a, target) != equal) throw new AssertionError("copy count differs");
            }
        }
    }
}
```

#### Solution: [Boundary] Outside Range (Author exercise)
<!-- id: bs-outside-range -->

**Approach.** When the target is smaller than every element, every position fails the "before the target" predicate, so `hi` keeps moving down to 0 and both bounds return 0. When the target is larger than every element, every position is before the target, so `lo` moves up to `n` and both bounds return `n`, which is why `hi` starts at the length and not at the last index. An empty array has `lo == hi == 0` from the start, so the loop body never runs. The program checks these cases with the extreme integers as targets, and requires that the two bounds coincide whenever the target is absent.

**Complexity.** O(log n) time and O(1) extra space.

```java run
import java.util.Arrays;
import java.util.Random;

public final class OutsideRange {
    static int lowerBound(int[] a, int target) {
        int lo = 0, hi = a.length;
        while (lo < hi) { int mid = lo + (hi - lo) / 2; if (a[mid] < target) lo = mid + 1; else hi = mid; }
        return lo;
    }
    static int upperBound(int[] a, int target) {
        int lo = 0, hi = a.length;
        while (lo < hi) { int mid = lo + (hi - lo) / 2; if (a[mid] <= target) lo = mid + 1; else hi = mid; }
        return lo;
    }

    public static void main(String[] args) {
        int[] a = {5, 6, 7};
        if (lowerBound(a, 1) != 0 || upperBound(a, 1) != 0) throw new AssertionError("example 1");
        if (lowerBound(a, 9) != 3 || upperBound(a, 9) != 3) throw new AssertionError("example 2");
        if (lowerBound(a, Integer.MIN_VALUE) != 0 || upperBound(a, Integer.MIN_VALUE) != 0) throw new AssertionError("minimum target");
        if (lowerBound(a, Integer.MAX_VALUE) != 3 || upperBound(a, Integer.MAX_VALUE) != 3) throw new AssertionError("maximum target");
        int[] empty = {};
        if (lowerBound(empty, 4) != 0 || upperBound(empty, 4) != 0) throw new AssertionError("empty array");
        int[] extremes = {Integer.MIN_VALUE, Integer.MAX_VALUE};
        if (upperBound(extremes, Integer.MAX_VALUE) != 2) throw new AssertionError("the maximum value is itself in the array");
        if (lowerBound(extremes, Integer.MIN_VALUE) != 0) throw new AssertionError("the minimum value is itself in the array");
        Random rnd = new Random(623);
        for (int t = 0; t < 3000; t++) {
            int n = rnd.nextInt(8);
            int[] arr = new int[n];
            for (int i = 0; i < n; i++) arr[i] = 2 * rnd.nextInt(6);
            Arrays.sort(arr);
            for (int target = -1; target <= 11; target += 2) {
                if (lowerBound(arr, target) != upperBound(arr, target)) throw new AssertionError("bounds must agree for an absent target");
            }
        }
    }
}
```

#### Solution: [Recognize] Find Smallest Letter Greater Than Target (LeetCode 744)
<!-- id: bs-next-greatest-letter -->

**Approach.** The first letter strictly greater than the target is the upper bound of the target in the letter array. A letter that is at most the target is still before the answer, so `lo = mid + 1`; a larger one may be the answer, so `hi = mid`. If the final position equals the array length, no letter is greater and the contract says to return the first letter, which is applied after the loop. The oracle scans the letters for the smallest strictly greater one and falls back to the first letter, and the two agree for every target from `a` to `z`.

**Complexity.** O(log n) time and O(1) extra space.

```java run
import java.util.Arrays;
import java.util.Random;

public final class NextGreatestLetter {
    static char nextGreatestLetter(char[] letters, char target) {
        int lo = 0, hi = letters.length;
        while (lo < hi) {
            int mid = lo + (hi - lo) / 2;
            if (letters[mid] <= target) lo = mid + 1;
            else hi = mid;
        }
        return lo == letters.length ? letters[0] : letters[lo];
    }
    static char scan(char[] letters, char target) {
        char best = 0;
        for (char c : letters) if (c > target && (best == 0 || c < best)) best = c;
        return best == 0 ? letters[0] : best;
    }

    public static void main(String[] args) {
        char[] ex = {'d', 'h', 'h', 'm', 't'};
        if (nextGreatestLetter(ex, 'h') != 'm') throw new AssertionError("example 1");
        if (nextGreatestLetter(ex, 'z') != 'd') throw new AssertionError("example 2");
        if (nextGreatestLetter(ex, 't') != 'd') throw new AssertionError("the largest letter wraps");
        if (nextGreatestLetter(ex, 'a') != 'd') throw new AssertionError("a target below all letters");
        Random rnd = new Random(624);
        for (int t = 0; t < 3000; t++) {
            int n = 2 + rnd.nextInt(8);
            char[] letters = new char[n];
            for (int i = 0; i < n; i++) letters[i] = (char) ('a' + rnd.nextInt(8));
            Arrays.sort(letters);
            if (letters[0] == letters[n - 1]) continue;
            for (char target = 'a'; target <= 'z'; target++) {
                if (nextGreatestLetter(letters, target) != scan(letters, target)) throw new AssertionError("differs on " + new String(letters) + " target " + target);
            }
        }
    }
}
```
