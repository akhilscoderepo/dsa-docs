<!-- solutions-for: 06-rotated-target -->
### Rotated Target

#### Solution: [Build] Search in Rotated Sorted Array (LeetCode 33)
<!-- id: bs-rotated-search -->

**Approach.** Compare the middle with the target first. Otherwise one half around the middle is sorted: if `nums[lo] <= nums[mid]` it is the left half, else the right half. A sorted half has its smallest value at one end and its largest at the other, so the target either lies strictly inside the range of the sorted half, and the search keeps that half, or it does not, and the search keeps the other half. The check rotates random sorted arrays by every amount and compares with a scan for every target near the values.

**Complexity.** O(log n) time and O(1) extra space.

```java run
import java.util.Random;
import java.util.TreeSet;

public final class RotatedSearch {
    static int search(int[] a, int target) {
        int lo = 0, hi = a.length - 1;
        while (lo <= hi) {
            int mid = lo + (hi - lo) / 2;
            if (a[mid] == target) return mid;
            if (a[lo] <= a[mid]) {
                if (a[lo] <= target && target < a[mid]) hi = mid - 1;
                else lo = mid + 1;
            } else {
                if (a[mid] < target && target <= a[hi]) lo = mid + 1;
                else hi = mid - 1;
            }
        }
        return -1;
    }
    static int scan(int[] a, int target) {
        for (int i = 0; i < a.length; i++) if (a[i] == target) return i;
        return -1;
    }

    public static void main(String[] args) {
        int[] ex = {9, 11, 15, 2, 4, 6};
        if (search(ex, 4) != 4) throw new AssertionError("example 1");
        if (search(ex, 7) != -1) throw new AssertionError("example 2");
        Random rnd = new Random(671);
        for (int t = 0; t < 3000; t++) {
            TreeSet<Integer> set = new TreeSet<>();
            int n = 1 + rnd.nextInt(10);
            while (set.size() < n) set.add(rnd.nextInt(40));
            int[] sorted = new int[n];
            int i = 0;
            for (int v : set) sorted[i++] = v;
            for (int k = 0; k < n; k++) {
                int[] a = new int[n];
                for (int j = 0; j < n; j++) a[(j + k) % n] = sorted[j];
                for (int target = -1; target <= 41; target++) {
                    if (search(a, target) != scan(a, target)) throw new AssertionError("rotation " + k + ", target " + target);
                }
            }
        }
    }
}
```

#### Solution: [Vary] Pivot Then Search (Author exercise)
<!-- id: bs-pivot-then-search -->

**Approach.** Phase one finds the rotation index with the comparison of the middle against the right end. That index splits the array into a left piece, ending just before it, and a right piece, starting at it, and both pieces are sorted. If the pivot is 0 the whole array is one sorted piece. Otherwise the target belongs to the left piece when it is at least `nums[0]`, and to the right piece when it is smaller, since every value in the left piece is at least the first element and every value in the right piece is below it. Phase two is an ordinary exact search over that piece. The check compares with a scan on every rotation of random arrays.

**Complexity.** O(log n) time, with two halving loops, and O(1) extra space.

```java run
import java.util.Random;
import java.util.TreeSet;

public final class PivotThenSearch {
    static int pivotThenSearch(int[] a, int target) {
        int lo = 0, hi = a.length - 1;
        while (lo < hi) {
            int mid = lo + (hi - lo) / 2;
            if (a[mid] > a[hi]) lo = mid + 1;
            else hi = mid;
        }
        int pivot = lo;
        if (pivot == 0) { lo = 0; hi = a.length - 1; }
        else if (target >= a[0]) { lo = 0; hi = pivot - 1; }
        else { lo = pivot; hi = a.length - 1; }
        while (lo <= hi) {
            int mid = lo + (hi - lo) / 2;
            if (a[mid] == target) return mid;
            if (a[mid] < target) lo = mid + 1;
            else hi = mid - 1;
        }
        return -1;
    }
    static int scan(int[] a, int target) {
        for (int i = 0; i < a.length; i++) if (a[i] == target) return i;
        return -1;
    }

    public static void main(String[] args) {
        if (pivotThenSearch(new int[] {9, 11, 15, 2, 4, 6}, 11) != 1) throw new AssertionError("example 1");
        if (pivotThenSearch(new int[] {5, 6, 1, 2, 3}, 1) != 2) throw new AssertionError("example 2");
        if (pivotThenSearch(new int[] {4}, 4) != 0 || pivotThenSearch(new int[] {4}, 5) != -1) throw new AssertionError("single element");
        Random rnd = new Random(672);
        for (int t = 0; t < 3000; t++) {
            TreeSet<Integer> set = new TreeSet<>();
            int n = 1 + rnd.nextInt(10);
            while (set.size() < n) set.add(rnd.nextInt(40));
            int[] sorted = new int[n];
            int i = 0;
            for (int v : set) sorted[i++] = v;
            for (int k = 0; k < n; k++) {
                int[] a = new int[n];
                for (int j = 0; j < n; j++) a[(j + k) % n] = sorted[j];
                for (int target = -1; target <= 41; target++) {
                    if (pivotThenSearch(a, target) != scan(a, target)) throw new AssertionError("rotation " + k + ", target " + target);
                }
            }
        }
    }
}
```

#### Solution: [Boundary] Search in Rotated Sorted Array II (LeetCode 81)
<!-- id: bs-rotated-search-repeats -->

**Approach.** Check the middle against the target first. If the first, middle and last values are all equal and the middle is not the target, then neither end can be the target either, so both ends are dropped and the invariant holds, though only two positions are removed. Otherwise one half is provably sorted by `nums[lo] <= nums[mid]`, and the range test chooses the half as in the distinct-value search. The worst case is linear, for example an array of equal values with a smaller one hidden and a target that is absent. The program counts steps on a long array of ones, and compares with a scan on random rotated arrays that contain many repeats.

**Complexity.** O(log n) when equal samples are rare and O(n) in the worst case, with O(1) extra space.

```java run
import java.util.Arrays;
import java.util.Random;

public final class RotatedSearchRepeats {
    static int steps;

    static boolean search(int[] a, int target) {
        int lo = 0, hi = a.length - 1;
        while (lo <= hi) {
            steps++;
            int mid = lo + (hi - lo) / 2;
            if (a[mid] == target) return true;
            if (a[lo] == a[mid] && a[mid] == a[hi]) { lo++; hi--; }
            else if (a[lo] <= a[mid]) {
                if (a[lo] <= target && target < a[mid]) hi = mid - 1;
                else lo = mid + 1;
            } else {
                if (a[mid] < target && target <= a[hi]) lo = mid + 1;
                else hi = mid - 1;
            }
        }
        return false;
    }
    static boolean scan(int[] a, int target) {
        for (int v : a) if (v == target) return true;
        return false;
    }

    public static void main(String[] args) {
        if (!search(new int[] {1, 0, 1, 1, 1}, 0)) throw new AssertionError("example 1");
        if (search(new int[] {3, 3, 3, 1, 3}, 2)) throw new AssertionError("example 2");
        Random rnd = new Random(673);
        for (int t = 0; t < 6000; t++) {
            int n = 1 + rnd.nextInt(12);
            int[] sorted = new int[n];
            for (int i = 0; i < n; i++) sorted[i] = rnd.nextInt(4);
            Arrays.sort(sorted);
            int k = rnd.nextInt(n);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[(i + k) % n] = sorted[i];
            for (int target = -1; target <= 4; target++) {
                if (search(a, target) != scan(a, target)) throw new AssertionError("differs on " + Arrays.toString(a) + " target " + target);
            }
        }
        int[] hidden = new int[4000];
        Arrays.fill(hidden, 1);
        hidden[1] = 0;
        steps = 0;
        if (search(hidden, 2)) throw new AssertionError("absent target");
        if (steps < 1000) throw new AssertionError("the worst case should be linear, got " + steps);
    }
}
```

#### Solution: [Recognize] Explain Both Strategies (Author exercise)
<!-- id: bs-explain-both-strategies -->

**Approach.** The one-pass search discards half of the interval per step. Its proof obligation is that at least one half around the middle is sorted, which holds for any rotation of a strictly increasing array, and that a target outside the range of the sorted half cannot be inside it. The pivot method makes two obligations: the right-end comparison finds the rotation index, and the target belongs to the left piece exactly when it is at least the first element. Both are O(log n) for distinct values, and the pivot method does about twice the number of halvings. The program implements both with a counted array, checks that they agree on every rotation and target of random arrays, and checks that the reads of each stay within small multiples of the number of halvings.

**Complexity.** O(log n) time and O(1) extra space for each strategy; the pivot method makes roughly two searches' worth of reads.

```java run
import java.util.Random;
import java.util.TreeSet;

public final class ExplainBothStrategies {
    static final class Counted {
        final int[] data;
        int reads;
        Counted(int[] data) { this.data = data; }
        int at(int i) { reads++; return data[i]; }
        int length() { return data.length; }
    }

    static int onePass(Counted a, int target) {
        int lo = 0, hi = a.length() - 1;
        while (lo <= hi) {
            int mid = lo + (hi - lo) / 2;
            int m = a.at(mid);
            if (m == target) return mid;
            if (a.at(lo) <= m) {
                if (a.at(lo) <= target && target < m) hi = mid - 1;
                else lo = mid + 1;
            } else {
                if (m < target && target <= a.at(hi)) lo = mid + 1;
                else hi = mid - 1;
            }
        }
        return -1;
    }
    static int pivotThenSearch(Counted a, int target) {
        int lo = 0, hi = a.length() - 1;
        while (lo < hi) {
            int mid = lo + (hi - lo) / 2;
            if (a.at(mid) > a.at(hi)) lo = mid + 1;
            else hi = mid;
        }
        int pivot = lo;
        if (pivot == 0) { lo = 0; hi = a.length() - 1; }
        else if (target >= a.at(0)) { lo = 0; hi = pivot - 1; }
        else { lo = pivot; hi = a.length() - 1; }
        while (lo <= hi) {
            int mid = lo + (hi - lo) / 2;
            int m = a.at(mid);
            if (m == target) return mid;
            if (m < target) lo = mid + 1;
            else hi = mid - 1;
        }
        return -1;
    }

    public static void main(String[] args) {
        int[] ex = {9, 11, 15, 2, 4, 6};
        if (onePass(new Counted(ex), 15) != 2 || pivotThenSearch(new Counted(ex), 15) != 2) throw new AssertionError("example 1");
        if (onePass(new Counted(ex), 1) != -1 || pivotThenSearch(new Counted(ex), 1) != -1) throw new AssertionError("example 2");
        Random rnd = new Random(674);
        for (int t = 0; t < 1500; t++) {
            TreeSet<Integer> set = new TreeSet<>();
            int n = 1 + rnd.nextInt(30);
            while (set.size() < n) set.add(rnd.nextInt(100));
            int[] sorted = new int[n];
            int i = 0;
            for (int v : set) sorted[i++] = v;
            int k = rnd.nextInt(n);
            int[] a = new int[n];
            for (int j = 0; j < n; j++) a[(j + k) % n] = sorted[j];
            int halvings = 32 - Integer.numberOfLeadingZeros(n);
            for (int target = -1; target <= 101; target++) {
                Counted c1 = new Counted(a), c2 = new Counted(a);
                int r1 = onePass(c1, target), r2 = pivotThenSearch(c2, target);
                if (r1 != r2) throw new AssertionError("strategies disagree, target " + target);
                if (c1.reads > 4 * halvings + 4) throw new AssertionError("one-pass reads: " + c1.reads);
                if (c2.reads > 6 * halvings + 6) throw new AssertionError("pivot reads: " + c2.reads);
            }
        }
    }
}
```
