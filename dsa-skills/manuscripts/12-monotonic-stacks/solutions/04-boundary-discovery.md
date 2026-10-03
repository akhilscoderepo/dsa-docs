<!-- solutions-for: 04-boundary-discovery -->
### Boundary Discovery

#### Solution: [Build] Previous Smaller Index (Author exercise)
<!-- id: ms-previous-smaller-index -->

**Approach.** Scan left to right and, for each index, remove every stack top whose value is at least the current value. A removed index can never again be the nearest strictly smaller index for a later position, because the current index is closer and not larger. After the removals the top, if present, is the answer, and an empty stack gives -1. The assertions compare with the outward walk on random arrays, check the examples, and confirm that the stack heights strictly increase from bottom to top after every step, which is why equal values must be removed.

**Complexity.** O(n) time, as the pushes and removals are each bounded by n, and O(n) extra space.

```java run
import java.util.ArrayDeque;
import java.util.Arrays;
import java.util.Random;

public final class PreviousSmallerIndex {
    static int[] previousSmaller(int[] a) {
        int n = a.length;
        int[] p = new int[n];
        ArrayDeque<Integer> stack = new ArrayDeque<>();
        for (int j = 0; j < n; j++) {
            while (!stack.isEmpty() && a[stack.peekLast()] >= a[j]) stack.removeLast();
            p[j] = stack.isEmpty() ? -1 : stack.peekLast();
            stack.addLast(j);
            int prev = Integer.MIN_VALUE;
            boolean first = true;
            for (int idx : stack) {
                if (!first && a[idx] <= prev) throw new AssertionError("stack heights must strictly increase");
                prev = a[idx];
                first = false;
            }
        }
        return p;
    }
    static int[] oracle(int[] a) {
        int[] p = new int[a.length];
        for (int i = 0; i < a.length; i++) {
            int k = i - 1;
            while (k >= 0 && a[k] >= a[i]) k--;
            p[i] = k;
        }
        return p;
    }

    public static void main(String[] args) {
        if (!Arrays.equals(previousSmaller(new int[]{3, 5, 4, 6, 2, 7}), new int[]{-1, 0, 0, 2, -1, 4})) throw new AssertionError("example 1");
        if (!Arrays.equals(previousSmaller(new int[]{2, 2, 2}), new int[]{-1, -1, -1})) throw new AssertionError("example 2");
        Random rnd = new Random(1401);
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(14);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(7) - 3;
            if (!Arrays.equals(previousSmaller(a), oracle(a))) throw new AssertionError("disagrees with the outward walk on " + Arrays.toString(a));
        }
    }
}
```

#### Solution: [Vary] Next Smaller Index (Author exercise)
<!-- id: ms-next-smaller-index -->

**Approach.** Fill the answer with `n`, then scan left to right with a stack of waiting indices. When the current value is strictly smaller than the top, that top's next smaller index is the current index, so write it and remove the top. Equal values do not pop. Indices never removed keep `n`, which points just past the array. The assertions compare with a forward walk on random arrays and check that a plain scan with a default of -1 would hide the difference between "no wall" and index -1 when the answer feeds a width formula.

**Complexity.** O(n) time and O(n) extra space.

```java run
import java.util.ArrayDeque;
import java.util.Arrays;
import java.util.Random;

public final class NextSmallerIndex {
    static int[] nextSmaller(int[] a) {
        int n = a.length;
        int[] q = new int[n];
        Arrays.fill(q, n);
        ArrayDeque<Integer> stack = new ArrayDeque<>();
        for (int j = 0; j < n; j++) {
            while (!stack.isEmpty() && a[j] < a[stack.peekLast()]) q[stack.removeLast()] = j;
            stack.addLast(j);
        }
        return q;
    }
    static int[] oracle(int[] a) {
        int n = a.length;
        int[] q = new int[n];
        for (int i = 0; i < n; i++) {
            int j = i + 1;
            while (j < n && a[j] >= a[i]) j++;
            q[i] = j;
        }
        return q;
    }

    public static void main(String[] args) {
        if (!Arrays.equals(nextSmaller(new int[]{4, 6, 5, 2, 7, 1}), new int[]{3, 2, 3, 5, 5, 6})) throw new AssertionError("example 1");
        if (!Arrays.equals(nextSmaller(new int[]{1, 2, 3}), new int[]{3, 3, 3})) throw new AssertionError("example 2");
        int[] a = {5, 1, 4};
        int width0 = nextSmaller(a)[2] - (-1) - 1;
        if (width0 != 3) throw new AssertionError("the sentinel n makes the width of a wall-less index reach the end");
        Random rnd = new Random(1402);
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(14);
            int[] arr = new int[n];
            for (int i = 0; i < n; i++) arr[i] = rnd.nextInt(7) - 3;
            if (!Arrays.equals(nextSmaller(arr), oracle(arr))) throw new AssertionError("disagrees with the forward walk on " + Arrays.toString(arr));
        }
    }
}
```

#### Solution: [Boundary] No Boundary (Author exercise)
<!-- id: ms-no-boundary -->

**Approach.** Compute the left wall with a forward scan that removes values at least as large as the current one and reads the surviving top, and compute the right wall with a forward scan that resolves on a strictly smaller value. Use -1 for a missing left wall and `n` for a missing right wall, so that `right - left - 1` counts the elements strictly between the walls without a special case. The assertions check both examples, compare with the outward walk on random arrays, and verify the identity that the width equals the count of elements strictly between the walls, all of which are at least `a[i]`.

**Complexity.** O(n) time and O(n) extra space for the two arrays and the stack.

```java run
import java.util.ArrayDeque;
import java.util.Arrays;
import java.util.Random;

public final class NoBoundary {
    static int[][] walls(int[] a) {
        int n = a.length;
        int[][] w = new int[n][2];
        ArrayDeque<Integer> stack = new ArrayDeque<>();
        for (int j = 0; j < n; j++) {
            while (!stack.isEmpty() && a[stack.peekLast()] >= a[j]) stack.removeLast();
            w[j][0] = stack.isEmpty() ? -1 : stack.peekLast();
            stack.addLast(j);
        }
        stack.clear();
        for (int j = 0; j < n; j++) w[j][1] = n;
        for (int j = 0; j < n; j++) {
            while (!stack.isEmpty() && a[j] < a[stack.peekLast()]) w[stack.removeLast()][1] = j;
            stack.addLast(j);
        }
        return w;
    }
    static int[][] oracle(int[] a) {
        int n = a.length;
        int[][] w = new int[n][2];
        for (int i = 0; i < n; i++) {
            int l = i - 1;
            while (l >= 0 && a[l] >= a[i]) l--;
            int r = i + 1;
            while (r < n && a[r] >= a[i]) r++;
            w[i][0] = l;
            w[i][1] = r;
        }
        return w;
    }

    public static void main(String[] args) {
        if (!Arrays.deepEquals(walls(new int[]{1, 2, 3}), new int[][]{{-1, 3}, {0, 3}, {1, 3}})) throw new AssertionError("example 1");
        if (!Arrays.deepEquals(walls(new int[]{3, 2, 1}), new int[][]{{-1, 1}, {-1, 2}, {-1, 3}})) throw new AssertionError("example 2");
        Random rnd = new Random(1403);
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(14);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(6) - 2;
            int[][] got = walls(a);
            if (!Arrays.deepEquals(got, oracle(a))) throw new AssertionError("disagrees with the outward walk on " + Arrays.toString(a));
            for (int i = 0; i < n; i++) {
                int width = got[i][1] - got[i][0] - 1;
                int count = 0;
                for (int k = got[i][0] + 1; k < got[i][1]; k++) {
                    if (a[k] < a[i]) throw new AssertionError("an element between the walls is smaller");
                    count++;
                }
                if (count != width) throw new AssertionError("width must count the elements between the walls");
            }
        }
    }
}
```

#### Solution: [Recognize] Widest Region Where Each Value Is Minimum (Author exercise)
<!-- id: ms-widest-minimum-region -->

**Approach.** Find both walls with strict comparisons, as in the previous solutions, and return `right - left - 1` for each index. The region for an index is every element between the walls, all of which are at least `a[i]`, and it is the longest such contiguous stretch because each wall is the nearest strictly smaller element. Equal values lie inside the region, which is why the all-equal example gives the full length for each element. The assertions compare with a brute force that tries every subarray containing the index, and confirm the examples.

**Complexity.** O(n) time and O(n) extra space, against O(n^3) for the brute force.

```java run
import java.util.ArrayDeque;
import java.util.Arrays;
import java.util.Random;

public final class WidestMinimumRegion {
    static int[] widest(int[] a) {
        int n = a.length;
        int[] left = new int[n];
        int[] right = new int[n];
        Arrays.fill(right, n);
        ArrayDeque<Integer> stack = new ArrayDeque<>();
        for (int j = 0; j < n; j++) {
            while (!stack.isEmpty() && a[stack.peekLast()] >= a[j]) stack.removeLast();
            left[j] = stack.isEmpty() ? -1 : stack.peekLast();
            stack.addLast(j);
        }
        stack.clear();
        for (int j = 0; j < n; j++) {
            while (!stack.isEmpty() && a[j] < a[stack.peekLast()]) right[stack.removeLast()] = j;
            stack.addLast(j);
        }
        int[] width = new int[n];
        for (int i = 0; i < n; i++) width[i] = right[i] - left[i] - 1;
        return width;
    }
    static int[] oracle(int[] a) {
        int n = a.length;
        int[] best = new int[n];
        for (int lo = 0; lo < n; lo++)
            for (int hi = lo; hi < n; hi++) {
                for (int i = lo; i <= hi; i++) {
                    boolean minimal = true;
                    for (int k = lo; k <= hi; k++) if (a[k] < a[i]) minimal = false;
                    if (minimal) best[i] = Math.max(best[i], hi - lo + 1);
                }
            }
        return best;
    }

    public static void main(String[] args) {
        if (!Arrays.equals(widest(new int[]{2, 1, 5, 6, 2, 3}), new int[]{1, 6, 2, 1, 4, 1})) throw new AssertionError("example 1");
        if (!Arrays.equals(widest(new int[]{4, 4, 4}), new int[]{3, 3, 3})) throw new AssertionError("example 2");
        Random rnd = new Random(1404);
        for (int t = 0; t < 1500; t++) {
            int n = 1 + rnd.nextInt(9);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = 1 + rnd.nextInt(5);
            if (!Arrays.equals(widest(a), oracle(a))) throw new AssertionError("disagrees with the brute force on " + Arrays.toString(a));
        }
    }
}
```
