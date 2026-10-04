<!-- solutions-for: 06-binary-search -->
### Solutions For Peak Search

#### Solution: [Build] Peak Index In A Mountain Array (LeetCode 852)
<!-- id: bs-mountain-852 -->

**Approach.**
The array rises strictly to its top and then falls strictly. At `mid`, the comparison of `arr[mid]` with `arr[mid + 1]` says which side holds the top. A smaller value means the data still rises, so the top lies right of `mid` and `lo` becomes `mid + 1`. A larger value means the data falls, so the top is at `mid` or left of it and `hi` becomes `mid`. The invariant is that the top lies inside `[lo, hi]`. The loop ends with one index, the top. The test checks the result against a scan for the maximum.

**Complexity.**
- **Time** is O(log n), because each step halves the interval and reads two neighbors.
- **Space** is O(1), because the code stores only three indexes.

```java run
import java.util.Random;

public final class MountainPeak852 {
    /**
     * Returns the index of the top of a mountain array.
     * Time: O(log n). Space: O(1).
     * Invariant: the top lies inside [lo, hi].
     */
    static int peakIndex(int[] arr) {
        int lo = 0, hi = arr.length - 1;
        // The loop stops when one index remains.
        while (lo < hi) {
            // mid < hi here, so mid + 1 is inside the array.
            int mid = lo + (hi - lo) / 2;
            // A rising pair means the top lies to the right of mid.
            if (arr[mid] < arr[mid + 1]) lo = mid + 1;
            // A falling pair means the top is at mid or to its left.
            else hi = mid;
        }
        return lo;
    }

    public static void main(String[] args) {
        // The statement examples.
        if (peakIndex(new int[] {1, 3, 6, 9, 7, 4, 2}) != 3) throw new AssertionError("example 1");
        if (peakIndex(new int[] {2, 10, 30, 40, 5}) != 3) throw new AssertionError("example 2");
        // Random mountains against a scan for the maximum.
        Random rnd = new Random(51);
        for (int t = 0; t < 3000; t++) {
            int up = 1 + rnd.nextInt(8), down = 1 + rnd.nextInt(8), v = rnd.nextInt(5);
            int[] a = new int[up + down + 1];
            for (int i = 0; i <= up; i++) a[i] = v += 1 + rnd.nextInt(4);
            for (int i = up + 1; i < a.length; i++) a[i] = v -= 1 + rnd.nextInt(4);
            if (peakIndex(a) != up) throw new AssertionError("random top " + up);
        }
    }
}
```

#### Solution: [Vary] Find Peak Element (LeetCode 162)
<!-- id: bs-peak-162 -->

**Approach.**
The array may hold several peaks, and the rule returns one of them. Walking right from `mid + 1` along a rise ends at a peak or at the last index. The last index counts as a peak, because its missing right neighbor is treated as smaller. The mirror argument covers the falling case. The invariant is that a peak lies inside `[lo, hi]`, and it needs only that neighbors differ. The test verifies the peak definition for the returned index, and shows that an array with equal neighbors can have no strict peak.

**Complexity.**
- **Time** is O(log n), because each step halves the interval.
- **Space** is O(1), because only three indexes are stored.

```java run
import java.util.Random;

public final class FindPeak162 {
    /**
     * Returns the index of any strict peak in an array whose adjacent values differ.
     * Time: O(log n). Space: O(1).
     * Invariant: a peak lies inside [lo, hi].
     */
    static int findPeak(int[] nums) {
        int lo = 0, hi = nums.length - 1;
        while (lo < hi) {
            int mid = lo + (hi - lo) / 2;
            // Rising: a peak exists to the right, ending at the last index at the latest.
            if (nums[mid] < nums[mid + 1]) lo = mid + 1;
            // Falling: a peak exists at mid or to its left.
            else hi = mid;
        }
        return lo;
    }

    /** True when index i is larger than every neighbor that exists. */
    static boolean isPeak(int[] a, int i) {
        return (i == 0 || a[i - 1] < a[i]) && (i == a.length - 1 || a[i + 1] < a[i]);
    }

    public static void main(String[] args) {
        // The statement examples.
        int r = findPeak(new int[] {1, 5, 2, 4, 6, 3, 0});
        if (r != 1 && r != 4) throw new AssertionError("example 1");
        if (findPeak(new int[] {7}) != 0) throw new AssertionError("example 2");
        // Equal neighbors: the array has no strict peak, so the returned index is not one.
        int[] flat = {1, 2, 2, 2, 1};
        if (isPeak(flat, findPeak(flat))) throw new AssertionError("a plateau cannot give a strict peak");
        // Random arrays with distinct neighbors: the result satisfies the peak definition.
        Random rnd = new Random(52);
        for (int t = 0; t < 3000; t++) {
            int[] a = new int[1 + rnd.nextInt(15)];
            for (int i = 0; i < a.length; i++) {
                do a[i] = rnd.nextInt(10); while (i > 0 && a[i] == a[i - 1]);
            }
            if (!isPeak(a, findPeak(a))) throw new AssertionError("random " + java.util.Arrays.toString(a));
        }
    }
}
```

#### Solution: [Boundary] Endpoint Peak (Author exercise)
<!-- id: bs-endpoint-peak -->

**Approach.**
In a strictly increasing array, every step finds a rising pair, so `lo` moves right each time and stops at the last index, whose missing right neighbor counts as smaller. The loop never reads `nums[mid + 1]` outside the array, because `mid < hi <= nums.length - 1`. In a strictly decreasing array, every step finds a falling pair, so `hi` moves to `mid` each time and the search stops at index 0. The invariant is the same as before. The test traces both shapes and checks that no read goes out of range.

**Complexity.**
- **Time** is O(log n), because the interval halves each step.
- **Space** is O(1), because only three indexes are stored.

```java run
import java.util.Random;

public final class EndpointPeak {
    /**
     * Returns the index of a peak; ends count as peaks when they beat their one neighbor.
     * Time: O(log n). Space: O(1).
     * Invariant: a peak lies inside [lo, hi].
     */
    static int findPeak(int[] nums) {
        int lo = 0, hi = nums.length - 1;
        while (lo < hi) {
            int mid = lo + (hi - lo) / 2;
            // mid < hi <= length - 1, so this read stays inside the array.
            if (nums[mid] < nums[mid + 1]) lo = mid + 1; else hi = mid;
        }
        return lo;
    }

    public static void main(String[] args) {
        // The statement examples.
        if (findPeak(new int[] {1, 2, 3, 4}) != 3) throw new AssertionError("increasing");
        if (findPeak(new int[] {4, 3, 2, 1}) != 0) throw new AssertionError("decreasing");
        if (findPeak(new int[] {9}) != 0) throw new AssertionError("single value");
        // Longer monotone arrays keep the same result at both ends.
        Random rnd = new Random(53);
        for (int t = 0; t < 2000; t++) {
            int n = 1 + rnd.nextInt(40);
            int[] up = new int[n], down = new int[n];
            for (int i = 0; i < n; i++) { up[i] = i * 3; down[i] = (n - i) * 3; }
            if (findPeak(up) != n - 1 || findPeak(down) != 0) throw new AssertionError("monotone " + n);
        }
    }
}
```

#### Solution: [Recognize] Find In Mountain Array (LeetCode 1095)
<!-- id: bs-find-in-mountain -->

**Approach.**
The search runs three times. The first run finds the top with the slope rule, using two `get` calls per step. The second run is an ascending exact search on `[0, top]`. If it finds the target, that index is the smallest one, because the left side comes before the right side. Otherwise the third run is a descending exact search on `[top + 1, n - 1]`. Each run is logarithmic, so the total stays near `4 * (floor(log2(n)) + 1)` calls, which is below 100 for `n <= 10^4`. The invariant of each run is the one of its own lesson.

**Complexity.**
- **Time** is O(log n) calls to `get`, because three logarithmic searches run one after another.
- **Space** is O(1), because the code stores only a few indexes.

```java run
import java.util.Random;

public final class FindInMountain1095 {
    /** The hidden array; every get call is counted. */
    static final class Mountain {
        final int[] v; int calls = 0;
        Mountain(int[] v) { this.v = v; }
        int length() { return v.length; }
        int get(int i) { calls++; return v[i]; }
    }

    /**
     * Returns the smallest index holding target, or -1.
     * Time: O(log n) get calls. Space: O(1).
     * Invariant: each phase keeps the wanted index inside its own interval.
     */
    static int find(Mountain m, int target) {
        int n = m.length();
        // Phase 1: find the top with the slope rule.
        int lo = 0, hi = n - 1;
        while (lo < hi) {
            int mid = lo + (hi - lo) / 2;
            if (m.get(mid) < m.get(mid + 1)) lo = mid + 1; else hi = mid;
        }
        int top = lo;
        // Phase 2: ascending exact search on [0, top]; a hit here is the smallest index.
        lo = 0; hi = top;
        while (lo <= hi) {
            int mid = lo + (hi - lo) / 2, x = m.get(mid);
            if (x == target) return mid;
            if (x < target) lo = mid + 1; else hi = mid - 1;
        }
        // Phase 3: descending exact search on [top + 1, n - 1].
        lo = top + 1; hi = n - 1;
        while (lo <= hi) {
            int mid = lo + (hi - lo) / 2, x = m.get(mid);
            if (x == target) return mid;
            if (x < target) hi = mid - 1; else lo = mid + 1;
        }
        return -1;
    }

    public static void main(String[] args) {
        int[] data = {1, 5, 9, 12, 10, 7, 2};
        // The statement examples.
        if (find(new Mountain(data), 7) != 5) throw new AssertionError("example 1");
        if (find(new Mountain(data), 4) != -1) throw new AssertionError("example 2");
        // A value on both sides must return the left index.
        if (find(new Mountain(new int[] {1, 5, 9, 5, 1}), 5) != 1) throw new AssertionError("both sides");
        // Random mountains: the answer matches a scan and calls stay within 100 for n up to 10^4.
        Random rnd = new Random(54);
        for (int t = 0; t < 300; t++) {
            int up = 1 + rnd.nextInt(5000), down = 1 + rnd.nextInt(5000);
            int[] a = new int[up + down + 1];
            int v = 0;
            for (int i = 0; i <= up; i++) a[i] = v += 1 + rnd.nextInt(3);
            for (int i = up + 1; i < a.length; i++) a[i] = v -= 1 + rnd.nextInt(3);
            int target = a[rnd.nextInt(a.length)] + (rnd.nextBoolean() ? 0 : 1);
            int expect = -1;
            for (int i = a.length - 1; i >= 0; i--) if (a[i] == target) expect = i;
            Mountain m = new Mountain(a);
            if (find(m, target) != expect) throw new AssertionError("random " + target);
            if (m.calls > 100) throw new AssertionError("calls " + m.calls);
        }
    }
}
```
