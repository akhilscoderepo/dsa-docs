<!-- solutions-for: 06-rotated-minimum -->
### Rotated Minimum

#### Solution: [Build] Find Minimum in Rotated Sorted Array (LeetCode 153)
<!-- id: bs-rotated-minimum -->

**Approach.** Keep a closed interval that contains the smallest element. Compare `nums[mid]` with `nums[hi]`. If the middle is larger, it lies in the first ascending stretch, so the drop and the minimum are strictly to the right and `lo = mid + 1`. If the middle is smaller, it is in the last stretch, so the minimum is at `mid` or earlier and `hi = mid`. With distinct values equality never occurs while `mid < hi`. The check rotates random sorted arrays by every amount and compares with the minimum found by scanning.

**Complexity.** O(log n) time and O(1) extra space.

```java run
import java.util.Random;
import java.util.TreeSet;

public final class RotatedMinimum {
    static int findMin(int[] a) {
        int lo = 0, hi = a.length - 1;
        while (lo < hi) {
            int mid = lo + (hi - lo) / 2;
            if (a[mid] > a[hi]) lo = mid + 1;
            else hi = mid;
        }
        return a[lo];
    }
    static int[] rotate(int[] sorted, int k) {
        int n = sorted.length;
        int[] out = new int[n];
        for (int i = 0; i < n; i++) out[(i + k) % n] = sorted[i];
        return out;
    }

    public static void main(String[] args) {
        if (findMin(new int[] {9, 11, 15, 2, 4, 6}) != 2) throw new AssertionError("example 1");
        if (findMin(new int[] {3, 5, 8}) != 3) throw new AssertionError("example 2");
        Random rnd = new Random(661);
        for (int t = 0; t < 3000; t++) {
            TreeSet<Integer> set = new TreeSet<>();
            int n = 1 + rnd.nextInt(12);
            while (set.size() < n) set.add(rnd.nextInt(60) - 30);
            int[] sorted = new int[n];
            int i = 0;
            for (int v : set) sorted[i++] = v;
            for (int k = 0; k < n; k++) {
                int[] rotated = rotate(sorted, k);
                if (findMin(rotated) != sorted[0]) throw new AssertionError("wrong minimum for rotation " + k);
            }
        }
    }
}
```

#### Solution: [Vary] Rotation Count (Author exercise)
<!-- id: bs-rotation-count -->

**Approach.** The loop is the same as for the minimum value, but the answer is the final `lo`. If the array was sorted and then rotated right by `k` places, the smallest element moved from index 0 to index `k`, so the index of the minimum is the rotation count. A full rotation by the array length is indistinguishable from none and counts as zero. The check rotates random sorted arrays by each amount and requires the returned count to equal that amount.

**Complexity.** O(log n) time and O(1) extra space.

```java run
import java.util.Random;
import java.util.TreeSet;

public final class RotationCount {
    static int rotationCount(int[] a) {
        int lo = 0, hi = a.length - 1;
        while (lo < hi) {
            int mid = lo + (hi - lo) / 2;
            if (a[mid] > a[hi]) lo = mid + 1;
            else hi = mid;
        }
        return lo;
    }

    public static void main(String[] args) {
        if (rotationCount(new int[] {9, 11, 15, 2, 4, 6}) != 3) throw new AssertionError("example 1");
        if (rotationCount(new int[] {3, 5, 8}) != 0) throw new AssertionError("example 2");
        Random rnd = new Random(662);
        for (int t = 0; t < 3000; t++) {
            TreeSet<Integer> set = new TreeSet<>();
            int n = 1 + rnd.nextInt(12);
            while (set.size() < n) set.add(rnd.nextInt(60) - 30);
            int[] sorted = new int[n];
            int i = 0;
            for (int v : set) sorted[i++] = v;
            for (int k = 0; k < n; k++) {
                int[] rotated = new int[n];
                for (int j = 0; j < n; j++) rotated[(j + k) % n] = sorted[j];
                if (rotationCount(rotated) != k) throw new AssertionError("rotation " + k + " of " + n + " reported as " + rotationCount(rotated));
            }
        }
    }
}
```

#### Solution: [Boundary] Two Values (Author exercise)
<!-- id: bs-two-values -->

**Approach.** For two elements `lo = 0`, `hi = 1`, and `mid = 0`, so the middle equals the left edge. For `[2, 1]` the comparison finds 2 larger than 1, so `lo = 1` and the edges meet at index 1. For `[1, 2]` it finds 1 smaller than 2, so `hi = 0` and the edges meet at index 0. In both cases one comparison ends the loop, and neither update can repeat the same interval, because `lo = mid + 1` and `hi = mid` with `mid < hi` both shrink it. A one-element array never enters the loop. The program records each triple and also checks that the interval size strictly decreases for every rotation of arrays up to length eight.

**Complexity.** O(log n) time and O(1) extra space; at most one comparison for two elements.

```java run
import java.util.ArrayList;
import java.util.List;

public final class TwoValuesTrace {
    static List<int[]> steps = new ArrayList<>();

    static int findMinIndex(int[] a) {
        steps.clear();
        int lo = 0, hi = a.length - 1;
        while (lo < hi) {
            int mid = lo + (hi - lo) / 2;
            steps.add(new int[] {lo, hi, mid});
            if (a[mid] > a[hi]) lo = mid + 1;
            else hi = mid;
        }
        return lo;
    }

    public static void main(String[] args) {
        if (findMinIndex(new int[] {2, 1}) != 1 || steps.size() != 1 || steps.get(0)[2] != 0) throw new AssertionError("example 1");
        if (findMinIndex(new int[] {1, 2}) != 0 || steps.size() != 1 || steps.get(0)[2] != 0) throw new AssertionError("example 2");
        if (findMinIndex(new int[] {5}) != 0 || !steps.isEmpty()) throw new AssertionError("one element");
        for (int n = 2; n <= 8; n++) {
            for (int k = 0; k < n; k++) {
                int[] a = new int[n];
                for (int i = 0; i < n; i++) a[(i + k) % n] = i;
                int idx = findMinIndex(a);
                if (idx != k) throw new AssertionError("n=" + n + " k=" + k);
                int previous = Integer.MAX_VALUE;
                for (int[] s : steps) {
                    int size = s[1] - s[0] + 1;
                    if (size >= previous) throw new AssertionError("the interval did not shrink");
                    previous = size;
                    if (s[2] >= s[1]) throw new AssertionError("mid must stay below hi");
                }
            }
        }
    }
}
```

#### Solution: [Recognize] Find Minimum in Rotated Sorted Array II (LeetCode 154)
<!-- id: bs-rotated-minimum-repeats -->

**Approach.** Compare `nums[mid]` with `nums[hi]`. A larger middle means the minimum is to the right, so `lo = mid + 1`. A smaller middle means the minimum is at `mid` or before, so `hi = mid`. When they are equal, the middle gives no information about which stretch it is in, but the value at `hi` also appears at `mid`, so the minimum value is still present in `[lo, hi - 1]` and `hi` can be decreased by one safely. That step removes a single element, so a long run of equal values forces about n steps. The program counts the steps on an array of 4000 ones with a single zero second from the front and compares the answer with a scan on random rotated arrays with repeats.

**Complexity.** O(log n) when the equal case is rare and O(n) in the worst case, with O(1) extra space.

```java run
import java.util.Arrays;
import java.util.Random;

public final class RotatedMinimumRepeats {
    static int steps;

    static int findMin(int[] a) {
        int lo = 0, hi = a.length - 1;
        while (lo < hi) {
            steps++;
            int mid = lo + (hi - lo) / 2;
            if (a[mid] > a[hi]) lo = mid + 1;
            else if (a[mid] < a[hi]) hi = mid;
            else hi--;
        }
        return a[lo];
    }

    public static void main(String[] args) {
        if (findMin(new int[] {2, 2, 2, 0, 1, 2}) != 0) throw new AssertionError("example 1");
        if (findMin(new int[] {1, 1, 1}) != 1) throw new AssertionError("example 2");
        Random rnd = new Random(664);
        for (int t = 0; t < 5000; t++) {
            int n = 1 + rnd.nextInt(12);
            int[] sorted = new int[n];
            for (int i = 0; i < n; i++) sorted[i] = rnd.nextInt(4);
            Arrays.sort(sorted);
            int k = rnd.nextInt(n);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[(i + k) % n] = sorted[i];
            int expected = Integer.MAX_VALUE;
            for (int v : a) expected = Math.min(expected, v);
            if (findMin(a) != expected) throw new AssertionError("wrong minimum on " + Arrays.toString(a));
        }
        int n = 4000;
        int[] hidden = new int[n];
        Arrays.fill(hidden, 1);
        hidden[1] = 0;
        steps = 0;
        if (findMin(hidden) != 0) throw new AssertionError("hidden zero");
        if (steps < n / 2) throw new AssertionError("the worst case should be linear, got " + steps);
    }
}
```
