<!-- solutions-for: 06-exact-search -->
### Exact Search

#### Solution: [Build] Binary Search (LeetCode 704)
<!-- id: bs-binary-search -->

**Approach.** Keep a closed interval `[lo, hi]` of positions that may hold the target, initially the whole array. Read `mid = lo + (hi - lo) / 2`. On equality return `mid`. If the value is smaller than the target, every position up to `mid` is too small, so set `lo = mid + 1`. If it is larger, set `hi = mid - 1`. When `lo > hi`, the interval is empty and the target is absent. The check compares with a linear scan on random strictly increasing arrays, for every value in and around the range, and shows that the shorter midpoint formula overflows for large positions while the safe one does not.

**Complexity.** O(log n) time and O(1) extra space.

```java run
import java.util.Random;
import java.util.TreeSet;

public final class BinarySearchExact {
    static int search(int[] a, int target) {
        int lo = 0, hi = a.length - 1;
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
        if (search(new int[] {4, 8, 15, 16, 23, 42}, 16) != 3) throw new AssertionError("example 1");
        if (search(new int[] {7}, 3) != -1) throw new AssertionError("example 2");
        int lo = 1_500_000_000, hi = 2_000_000_000;
        if ((lo + hi) / 2 >= 0) throw new AssertionError("the unsafe midpoint should have overflowed to a negative number");
        int safe = lo + (hi - lo) / 2;
        if (safe < lo || safe > hi) throw new AssertionError("the safe midpoint stays inside the interval");
        Random rnd = new Random(601);
        for (int t = 0; t < 3000; t++) {
            TreeSet<Integer> set = new TreeSet<>();
            int n = 1 + rnd.nextInt(12);
            while (set.size() < n) set.add(rnd.nextInt(40) - 20);
            int[] a = new int[n];
            int k = 0;
            for (int v : set) a[k++] = v;
            for (int target = -22; target <= 22; target++) {
                if (search(a, target) != scan(a, target)) throw new AssertionError("differs from the scan for target " + target);
            }
        }
    }
}
```

#### Solution: [Vary] Descending Search (Author exercise)
<!-- id: bs-descending-search -->

**Approach.** The loop has the same shape, with the two moves exchanged. If the middle value is larger than the target, then in a descending array the target can only be to the right, so `lo = mid + 1`; if it is smaller, the target can only be to the left, so `hi = mid - 1`. The array is not copied or reversed. The empty array gives `hi = -1`, so the loop body never runs and the answer is minus one. The check compares with a linear scan on random strictly decreasing arrays, including the empty one.

**Complexity.** O(log n) time and O(1) extra space.

```java run
import java.util.Random;
import java.util.TreeSet;

public final class DescendingSearch {
    static int searchDescending(int[] a, int target) {
        int lo = 0, hi = a.length - 1;
        while (lo <= hi) {
            int mid = lo + (hi - lo) / 2;
            if (a[mid] == target) return mid;
            if (a[mid] > target) lo = mid + 1;
            else hi = mid - 1;
        }
        return -1;
    }
    static int scan(int[] a, int target) {
        for (int i = 0; i < a.length; i++) if (a[i] == target) return i;
        return -1;
    }

    public static void main(String[] args) {
        if (searchDescending(new int[] {90, 70, 50, 30, 10}, 30) != 3) throw new AssertionError("example 1");
        if (searchDescending(new int[] {9, 4, 1}, 5) != -1) throw new AssertionError("example 2");
        if (searchDescending(new int[0], 1) != -1) throw new AssertionError("empty array");
        if (searchDescending(new int[] {Integer.MAX_VALUE, 0, Integer.MIN_VALUE}, Integer.MIN_VALUE) != 2) throw new AssertionError("extremes");
        Random rnd = new Random(602);
        for (int t = 0; t < 3000; t++) {
            TreeSet<Integer> set = new TreeSet<>();
            int n = rnd.nextInt(12);
            while (set.size() < n) set.add(rnd.nextInt(40) - 20);
            int[] a = new int[n];
            int k = 0;
            for (int v : set.descendingSet()) a[k++] = v;
            for (int target = -22; target <= 22; target++) {
                if (searchDescending(a, target) != scan(a, target)) throw new AssertionError("differs for target " + target);
            }
        }
    }
}
```

#### Solution: [Boundary] Two Elements (Author exercise)
<!-- id: bs-two-elements -->

**Approach.** For `[1, 3]` the first middle is position 0, because `0 + (1 - 0) / 2` is 0. Target 1 is found at once. Target 3 sends `lo` to 1, and the second reading at position 1 finds it. Target 2 sends `lo` to 1, and the second reading finds 3, which is too large, so `hi` becomes 0 and the interval is empty. Progress is guaranteed because each reading removes the middle position, and the program records the interval size before each reading to show that it strictly decreases. It then repeats the same check on every array of length one to eight.

**Complexity.** O(log n) readings; for two elements at most two readings.

```java run
import java.util.ArrayList;
import java.util.List;

public final class TwoElementsTrace {
    static List<Integer> sizes = new ArrayList<>();

    static int search(int[] a, int target) {
        sizes.clear();
        int lo = 0, hi = a.length - 1;
        while (lo <= hi) {
            sizes.add(hi - lo + 1);
            int mid = lo + (hi - lo) / 2;
            if (a[mid] == target) return mid;
            if (a[mid] < target) lo = mid + 1;
            else hi = mid - 1;
        }
        return -1;
    }
    static void strictlyShrinking() {
        for (int i = 1; i < sizes.size(); i++) if (sizes.get(i) >= sizes.get(i - 1)) throw new AssertionError("interval did not shrink: " + sizes);
    }

    public static void main(String[] args) {
        int[] a = {1, 3};
        if (search(a, 1) != 0 || !sizes.equals(List.of(2))) throw new AssertionError("target 1: " + sizes);
        if (search(a, 3) != 1 || !sizes.equals(List.of(2, 1))) throw new AssertionError("target 3: " + sizes);
        if (search(a, 2) != -1 || !sizes.equals(List.of(2, 1))) throw new AssertionError("target 2: " + sizes);
        strictlyShrinking();
        for (int n = 1; n <= 8; n++) {
            int[] arr = new int[n];
            for (int i = 0; i < n; i++) arr[i] = 2 * i + 1;
            for (int target = 0; target <= 2 * n + 1; target++) {
                search(arr, target);
                strictlyShrinking();
                int bound = 32 - Integer.numberOfLeadingZeros(n);
                if (sizes.size() > bound) throw new AssertionError("more readings than floor(log2 n) + 1 for n = " + n);
            }
        }
    }
}
```

#### Solution: [Recognize] Search a 2D Matrix (LeetCode 74)
<!-- id: bs-search-matrix-virtual -->

**Approach.** Because every row is sorted and each row starts above the end of the previous one, reading the matrix row by row gives one sorted sequence of rows times columns values. Run the ordinary closed-interval search over virtual positions from 0 to `rows * cols - 1`, and convert a middle position `p` to the row `p / cols` and the column `p % cols` only when its value is needed. The position is kept in a `long`. The check builds random matrices from a sorted sequence of distinct values and compares with a nested scan, for every target near the values.

**Complexity.** O(log(rows times cols)) time and O(1) extra space.

```java run
import java.util.Random;
import java.util.TreeSet;

public final class SearchMatrixVirtual {
    static boolean searchMatrix(int[][] m, int target) {
        int rows = m.length;
        if (rows == 0) return false;
        int cols = m[0].length;
        long lo = 0, hi = (long) rows * cols - 1;
        while (lo <= hi) {
            long mid = lo + (hi - lo) / 2;
            int v = m[(int) (mid / cols)][(int) (mid % cols)];
            if (v == target) return true;
            if (v < target) lo = mid + 1;
            else hi = mid - 1;
        }
        return false;
    }
    static boolean scan(int[][] m, int target) {
        for (int[] row : m) for (int v : row) if (v == target) return true;
        return false;
    }

    public static void main(String[] args) {
        int[][] ex = {{2, 4, 6}, {8, 10, 12}};
        if (!searchMatrix(ex, 10)) throw new AssertionError("example 1");
        if (searchMatrix(ex, 7)) throw new AssertionError("example 2");
        if (searchMatrix(new int[0][], 1)) throw new AssertionError("no rows");
        Random rnd = new Random(603);
        for (int t = 0; t < 2000; t++) {
            int rows = 1 + rnd.nextInt(5), cols = 1 + rnd.nextInt(5);
            TreeSet<Integer> set = new TreeSet<>();
            while (set.size() < rows * cols) set.add(rnd.nextInt(100));
            int[][] m = new int[rows][cols];
            int k = 0;
            for (int v : set) { m[k / cols][k % cols] = v; k++; }
            for (int target = -1; target <= 101; target++) {
                if (searchMatrix(m, target) != scan(m, target)) throw new AssertionError("differs for target " + target);
            }
        }
    }
}
```
