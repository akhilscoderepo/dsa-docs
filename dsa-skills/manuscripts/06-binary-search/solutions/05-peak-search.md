<!-- solutions-for: 06-peak-search -->
### Peak Search

#### Solution: [Build] Peak Index in a Mountain Array (LeetCode 852)
<!-- id: bs-mountain-peak -->

**Approach.** Keep a closed interval `[lo, hi]` that contains the summit. Compare `arr[mid]` with `arr[mid + 1]`. A rise means the summit is to the right, so `lo = mid + 1`. A fall means the summit is at `mid` or to its left, so `hi = mid`. The loop runs while `lo < hi`, so `mid + 1` is always inside the array, and the edges meet at the summit. The check builds random mountains and compares with a scan for the maximum.

**Complexity.** O(log n) time and O(1) extra space.

```java run
import java.util.Random;

public final class MountainPeak {
    static int peakIndex(int[] arr) {
        int lo = 0, hi = arr.length - 1;
        while (lo < hi) {
            int mid = lo + (hi - lo) / 2;
            if (arr[mid] < arr[mid + 1]) lo = mid + 1;
            else hi = mid;
        }
        return lo;
    }

    public static void main(String[] args) {
        if (peakIndex(new int[] {3, 6, 11, 8}) != 2) throw new AssertionError("example 1");
        if (peakIndex(new int[] {1, 2, 3, 4, 2, 1}) != 3) throw new AssertionError("example 2");
        Random rnd = new Random(651);
        for (int t = 0; t < 4000; t++) {
            int up = 1 + rnd.nextInt(8), down = 1 + rnd.nextInt(8);
            int[] arr = new int[up + down + 1];
            int v = rnd.nextInt(5);
            for (int i = 0; i <= up; i++) { arr[i] = v; v += 1 + rnd.nextInt(4); }
            v = arr[up];
            for (int i = 1; i <= down; i++) { v -= 1 + rnd.nextInt(3); arr[up + i] = v; }
            if (peakIndex(arr) != up) throw new AssertionError("wrong summit, expected " + up);
        }
    }
}
```

#### Solution: [Vary] Find Peak Element (LeetCode 162)
<!-- id: bs-find-peak-element -->

**Approach.** The same loop works when the array is not a mountain, with a weaker invariant: the interval always contains some peak. If `nums[mid] < nums[mid + 1]`, the sequence climbs, and since the position past the end counts as lower, a peak must appear somewhere to the right. If `nums[mid] > nums[mid + 1]`, then going left from `mid + 1` the sequence is falling, so either `mid` is a peak or the sequence climbs before it, and a peak lies at `mid` or earlier. The check accepts any index that is larger than both neighbors, treating the outside as negative infinity, on random arrays with distinct neighbors.

**Complexity.** O(log n) time and O(1) extra space.

```java run
import java.util.Random;

public final class FindPeakElement {
    static int findPeak(int[] nums) {
        int lo = 0, hi = nums.length - 1;
        while (lo < hi) {
            int mid = lo + (hi - lo) / 2;
            if (nums[mid] < nums[mid + 1]) lo = mid + 1;
            else hi = mid;
        }
        return lo;
    }
    static boolean isPeak(int[] a, int i) {
        boolean left = i == 0 || a[i - 1] < a[i];
        boolean right = i == a.length - 1 || a[i + 1] < a[i];
        return left && right;
    }

    public static void main(String[] args) {
        if (!isPeak(new int[] {1, 5, 2, 6, 3, 4}, findPeak(new int[] {1, 5, 2, 6, 3, 4}))) throw new AssertionError("example 1");
        if (findPeak(new int[] {9, 1}) != 0) throw new AssertionError("example 2");
        if (findPeak(new int[] {4}) != 0) throw new AssertionError("single element");
        Random rnd = new Random(652);
        for (int t = 0; t < 5000; t++) {
            int n = 1 + rnd.nextInt(12);
            int[] a = new int[n];
            a[0] = rnd.nextInt(10);
            for (int i = 1; i < n; i++) {
                int next;
                do { next = rnd.nextInt(10); } while (next == a[i - 1]);
                a[i] = next;
            }
            int p = findPeak(a);
            if (!isPeak(a, p)) throw new AssertionError("index " + p + " is not a peak");
        }
    }
}
```

#### Solution: [Boundary] Endpoint Peak (Author exercise)
<!-- id: bs-endpoint-peak -->

**Approach.** For a strictly increasing array, every comparison at `mid` finds a rise, so `lo` climbs until it reaches the last position, which is a peak because the position beyond the end counts as lower. For a strictly decreasing array every comparison finds a fall, so `hi` drops until it reaches 0, which is a peak because nothing precedes it. Arrays of length one return 0 without entering the loop, and for length two the only comparison is between positions 0 and 1. The program also instruments the reads to prove that the loop never touches an index outside the array.

**Complexity.** O(log n) time and O(1) extra space.

```java run
public final class EndpointPeak {
    static int findPeak(int[] a) {
        int lo = 0, hi = a.length - 1;
        while (lo < hi) {
            int mid = lo + (hi - lo) / 2;
            if (mid < 0 || mid + 1 >= a.length) throw new AssertionError("read out of range at " + mid);
            if (a[mid] < a[mid + 1]) lo = mid + 1;
            else hi = mid;
        }
        return lo;
    }

    public static void main(String[] args) {
        if (findPeak(new int[] {1, 2, 3, 4, 5}) != 4) throw new AssertionError("example 1");
        if (findPeak(new int[] {5, 4, 3, 2, 1}) != 0) throw new AssertionError("example 2");
        if (findPeak(new int[] {7}) != 0) throw new AssertionError("length one");
        if (findPeak(new int[] {1, 2}) != 1) throw new AssertionError("length two rising");
        if (findPeak(new int[] {2, 1}) != 0) throw new AssertionError("length two falling");
        for (int n = 1; n <= 60; n++) {
            int[] up = new int[n], down = new int[n];
            for (int i = 0; i < n; i++) { up[i] = i; down[i] = n - i; }
            if (findPeak(up) != n - 1) throw new AssertionError("increasing, n=" + n);
            if (findPeak(down) != 0) throw new AssertionError("decreasing, n=" + n);
        }
    }
}
```

#### Solution: [Recognize] Find in Mountain Array (LeetCode 1095)
<!-- id: bs-find-in-mountain -->

**Approach.** First locate the summit by comparing `get(mid)` with `get(mid + 1)`. Then run an ordinary closed-interval search on the rising part from index 0 to the summit. If the target is not found there, run the reversed-comparison search on the falling part after the summit. Searching the rising part first returns the smaller index when the target appears on both sides. Each loop halves its interval, so the total number of `get` calls is about four times the number of halvings, well under the limit of 100 for lengths up to 10000. The wrapper counts calls, and the check compares with a linear scan on random mountains.

**Complexity.** O(log n) calls to `get` and O(1) extra space.

```java run
import java.util.Random;
import java.util.TreeSet;

public final class FindInMountain {
    static final class MountainArray {
        final int[] data;
        int calls;
        MountainArray(int[] data) { this.data = data; }
        int get(int i) { calls++; return data[i]; }
        int length() { return data.length; }
    }

    static int findInMountain(MountainArray m, int target) {
        int n = m.length(), lo = 0, hi = n - 1;
        while (lo < hi) {
            int mid = lo + (hi - lo) / 2;
            if (m.get(mid) < m.get(mid + 1)) lo = mid + 1;
            else hi = mid;
        }
        int peak = lo;
        lo = 0; hi = peak;
        while (lo <= hi) {
            int mid = lo + (hi - lo) / 2, v = m.get(mid);
            if (v == target) return mid;
            if (v < target) lo = mid + 1; else hi = mid - 1;
        }
        lo = peak + 1; hi = n - 1;
        while (lo <= hi) {
            int mid = lo + (hi - lo) / 2, v = m.get(mid);
            if (v == target) return mid;
            if (v > target) lo = mid + 1; else hi = mid - 1;
        }
        return -1;
    }
    static int scan(int[] a, int target) {
        for (int i = 0; i < a.length; i++) if (a[i] == target) return i;
        return -1;
    }

    public static void main(String[] args) {
        int[] ex = {1, 3, 6, 9, 12, 10, 7, 4, 2};
        if (findInMountain(new MountainArray(ex), 6) != 2) throw new AssertionError("example 1");
        if (findInMountain(new MountainArray(ex), 5) != -1) throw new AssertionError("example 2");
        if (findInMountain(new MountainArray(ex), 7) != 6) throw new AssertionError("falling side");
        Random rnd = new Random(653);
        for (int t = 0; t < 3000; t++) {
            TreeSet<Integer> left = new TreeSet<>(), right = new TreeSet<>();
            int up = 1 + rnd.nextInt(8), down = 1 + rnd.nextInt(8);
            while (left.size() < up) left.add(rnd.nextInt(30));
            while (right.size() < down) right.add(rnd.nextInt(30));
            int top = 31;
            int[] a = new int[up + down + 1];
            int k = 0;
            for (int v : left) a[k++] = v;
            a[k++] = top;
            for (int v : right.descendingSet()) a[k++] = v;
            for (int target = -1; target <= 31; target++) {
                MountainArray m = new MountainArray(a);
                if (findInMountain(m, target) != scan(a, target)) throw new AssertionError("differs for target " + target);
            }
        }
        int[] big = new int[10000];
        for (int i = 0; i < 5000; i++) big[i] = i;
        for (int i = 5000; i < 10000; i++) big[i] = 10000 - i - 2;
        for (int target : new int[] {0, 4999, 2500, 1, 4998, -1}) {
            MountainArray m = new MountainArray(big);
            int got = findInMountain(m, target);
            if (got != scan(big, target)) throw new AssertionError("large mountain, target " + target);
            if (m.calls > 100) throw new AssertionError("more than 100 calls: " + m.calls);
        }
    }
}
```
