<!-- solutions-for: 12-monotonic-stacks -->
### Solutions For Both Boundaries

#### Solution: [Build] Previous Smaller Index (Author exercise)
<!-- id: ms-previous-smaller-index -->

**Approach.**
The stack holds indices whose values strictly increase from bottom to top. Each new value pops the tops that are not smaller than it. A popped top can never be the nearest smaller value of the new index or of any later index, because the new index is nearer and its value is at most the popped value. Equal tops must pop, since an equal value is not smaller. After the pops, the top is the nearest earlier index with a strictly smaller value, and an empty stack means none exists.

**Complexity.**
- **Time** is O(n), because the loop pushes each index once and pops it at most once.
- **Space** is O(n), because an increasing input keeps every index on the stack.

```java run
import java.util.ArrayDeque;
import java.util.Arrays;
import java.util.Deque;
import java.util.Random;

public final class PreviousSmaller {
    /**
     * Returns the previous strictly smaller index for every position, or -1.
     * Time: O(n). Space: O(n).
     * Invariant: stack values strictly increase from bottom to top.
     */
    static int[] solve(int[] nums) {
        int[] left = new int[nums.length];
        Deque<Integer> stack = new ArrayDeque<>();
        // One left-to-right pass reads each value once.
        for (int i = 0; i < nums.length; i++) {
            // Greater or equal tops cannot be a strictly smaller boundary.
            while (!stack.isEmpty() && nums[stack.peek()] >= nums[i]) stack.pop();
            // The surviving top is the nearest smaller index, or -1 when empty.
            left[i] = stack.isEmpty() ? -1 : stack.peek();
            stack.push(i);
        }
        return left;
    }

    /** Reference: walk left from every index. */
    static int[] oracle(int[] nums) {
        int[] r = new int[nums.length];
        for (int i = 0; i < nums.length; i++) {
            int j = i - 1;
            while (j >= 0 && nums[j] >= nums[i]) j--;
            r[i] = j;
        }
        return r;
    }

    public static void main(String[] args) {
        // Example 1 and Example 2 from the exercise text.
        if (!Arrays.equals(solve(new int[] {5, 2, 6, 3, 4, 1}), new int[] {-1, -1, 1, 1, 3, -1})) throw new AssertionError("example 1");
        if (!Arrays.equals(solve(new int[] {4, 4, 4}), new int[] {-1, -1, -1})) throw new AssertionError("example 2");
        // Random arrays with repeated values must match the oracle.
        Random rnd = new Random(53);
        for (int t = 0; t < 3000; t++) {
            int[] a = new int[1 + rnd.nextInt(12)];
            for (int i = 0; i < a.length; i++) a[i] = rnd.nextInt(5);
            if (!Arrays.equals(solve(a), oracle(a))) throw new AssertionError(Arrays.toString(a));
        }
        System.out.println("ok");
    }
}
```

#### Solution: [Vary] Next Smaller Index (Author exercise)
<!-- id: ms-next-smaller-index -->

**Approach.**
The stack holds indices whose values never decrease from bottom to top. A new value `nums[i]` is the first smaller value after every top whose value is strictly greater, so the loop pops those tops and writes `i` as their answer. Equal tops stay, because an equal value does not resolve them. The loop stops at the first top that is not greater, and every index below it is not greater either. Indices left at the end keep `-1`.

**Complexity.**
- **Time** is O(n), because the loop pushes each index once and pops it at most once.
- **Space** is O(n), because a non-decreasing input keeps every index on the stack.

```java run
import java.util.ArrayDeque;
import java.util.Arrays;
import java.util.Deque;
import java.util.Random;

public final class NextSmaller {
    /**
     * Returns the next strictly smaller index for every position, or -1.
     * Time: O(n). Space: O(n).
     * Invariant: stack values never decrease from bottom to top.
     */
    static int[] solve(int[] nums) {
        int[] right = new int[nums.length];
        // The default -1 stays for indices that never resolve.
        Arrays.fill(right, -1);
        Deque<Integer> stack = new ArrayDeque<>();
        for (int i = 0; i < nums.length; i++) {
            // Only strictly greater tops resolve, so equal values keep waiting.
            while (!stack.isEmpty() && nums[stack.peek()] > nums[i]) right[stack.pop()] = i;
            stack.push(i);
        }
        return right;
    }

    /** Reference: walk right from every index. */
    static int[] oracle(int[] nums) {
        int[] r = new int[nums.length];
        for (int i = 0; i < nums.length; i++) {
            r[i] = -1;
            for (int j = i + 1; j < nums.length; j++) {
                if (nums[j] < nums[i]) { r[i] = j; break; }
            }
        }
        return r;
    }

    public static void main(String[] args) {
        // Example 1 and Example 2 from the exercise text.
        if (!Arrays.equals(solve(new int[] {5, 2, 6, 3, 4, 1}), new int[] {1, 5, 3, 5, 5, -1})) throw new AssertionError("example 1");
        if (!Arrays.equals(solve(new int[] {3, 3, 1, 3}), new int[] {2, 2, -1, -1})) throw new AssertionError("example 2");
        // Random arrays with repeated values must match the oracle.
        Random rnd = new Random(59);
        for (int t = 0; t < 3000; t++) {
            int[] a = new int[1 + rnd.nextInt(12)];
            for (int i = 0; i < a.length; i++) a[i] = rnd.nextInt(5);
            if (!Arrays.equals(solve(a), oracle(a))) throw new AssertionError(Arrays.toString(a));
        }
        System.out.println("ok");
    }
}
```

#### Solution: [Boundary] No Boundary (Author exercise)
<!-- id: ms-no-boundary -->

**Approach.**
Two scans produce the two sides. The left scan reads the surviving top after popping greater or equal tops, and it writes `-1` when the stack is empty. The right scan resolves tops at the pop, with the default `n` placed in every entry beforehand, so indices that never resolve already hold the sentinel. The pair for each index is `{left[i], right[i]}`. Each sentinel lies one slot outside the array, so an index with no smaller value on either side gets `{-1, n}`. The invariants are the same as in the two earlier solutions.

**Complexity.**
- **Time** is O(n), because each scan pushes every index once and pops it at most once.
- **Space** is O(n), for the stack and the two answer arrays.

```java run
import java.util.ArrayDeque;
import java.util.Arrays;
import java.util.Deque;
import java.util.Random;

public final class NoBoundary {
    /**
     * Returns {previous smaller index or -1, next smaller index or n} for every position.
     * Time: O(n). Space: O(n).
     * Invariant: the left stack strictly increases, the right stack never decreases.
     */
    static int[][] solve(int[] nums) {
        int n = nums.length;
        int[] left = new int[n];
        int[] right = new int[n];
        // The sentinel n is the default for every right boundary.
        Arrays.fill(right, n);
        Deque<Integer> stack = new ArrayDeque<>();
        // The left scan reads the surviving top after popping greater or equal values.
        for (int i = 0; i < n; i++) {
            while (!stack.isEmpty() && nums[stack.peek()] >= nums[i]) stack.pop();
            left[i] = stack.isEmpty() ? -1 : stack.peek();
            stack.push(i);
        }
        stack.clear();
        // The right scan writes at the pop, and only strictly greater tops resolve.
        for (int i = 0; i < n; i++) {
            while (!stack.isEmpty() && nums[stack.peek()] > nums[i]) right[stack.pop()] = i;
            stack.push(i);
        }
        int[][] out = new int[n][];
        for (int i = 0; i < n; i++) out[i] = new int[] {left[i], right[i]};
        return out;
    }

    /** Reference: walk both ways from every index. */
    static int[][] oracle(int[] nums) {
        int n = nums.length;
        int[][] r = new int[n][];
        for (int i = 0; i < n; i++) {
            int l = i - 1;
            while (l >= 0 && nums[l] >= nums[i]) l--;
            int h = i + 1;
            while (h < n && nums[h] >= nums[i]) h++;
            r[i] = new int[] {l, h};
        }
        return r;
    }

    public static void main(String[] args) {
        // Example 1 and Example 2 from the exercise text.
        if (!Arrays.deepEquals(solve(new int[] {1, 2, 3}), new int[][] {{-1, 3}, {0, 3}, {1, 3}})) throw new AssertionError("example 1");
        if (!Arrays.deepEquals(solve(new int[] {3, 3}), new int[][] {{-1, 2}, {-1, 2}})) throw new AssertionError("example 2");
        // Random arrays with repeated values must match the oracle.
        Random rnd = new Random(61);
        for (int t = 0; t < 3000; t++) {
            int[] a = new int[1 + rnd.nextInt(12)];
            for (int i = 0; i < a.length; i++) a[i] = rnd.nextInt(4);
            if (!Arrays.deepEquals(solve(a), oracle(a))) throw new AssertionError(Arrays.toString(a));
        }
        System.out.println("ok");
    }
}
```

#### Solution: [Recognize] Widest Region Where Each Value Is Minimum (Author exercise)
<!-- id: ms-widest-minimum-region -->

**Approach.**
The region of index `i` extends until the nearest strictly smaller value on each side, because every value inside must be at least `nums[i]`. Two scans find those boundaries. The width is `right[i] - left[i] - 1`, the number of positions strictly between the boundary indices, and the sentinels `-1` and `n` make the same formula valid at the array ends. Equal values never end a region, which matches the strict boundaries. The invariants are the same as in the earlier solutions.

**Complexity.**
- **Time** is O(n), because each scan pushes every index once and pops it at most once.
- **Space** is O(n), for the stack and the two boundary arrays.

```java run
import java.util.ArrayDeque;
import java.util.Arrays;
import java.util.Deque;
import java.util.Random;

public final class WidestMinimumRegion {
    /**
     * Returns the length of the longest range around each index with all values at least nums[i].
     * Time: O(n). Space: O(n).
     * Invariant: boundaries are strictly smaller, so ties stay inside the region.
     */
    static int[] solve(int[] nums) {
        int n = nums.length;
        int[] left = new int[n];
        int[] right = new int[n];
        Arrays.fill(right, n);
        Deque<Integer> stack = new ArrayDeque<>();
        // The left scan gives each index its nearest strictly smaller predecessor.
        for (int i = 0; i < n; i++) {
            while (!stack.isEmpty() && nums[stack.peek()] >= nums[i]) stack.pop();
            left[i] = stack.isEmpty() ? -1 : stack.peek();
            stack.push(i);
        }
        stack.clear();
        // The right scan resolves each index at the first strictly smaller successor.
        for (int i = 0; i < n; i++) {
            while (!stack.isEmpty() && nums[stack.peek()] > nums[i]) right[stack.pop()] = i;
            stack.push(i);
        }
        int[] width = new int[n];
        // The sentinels let one formula cover the array ends.
        for (int i = 0; i < n; i++) width[i] = right[i] - left[i] - 1;
        return width;
    }

    /** Reference: grow the range one index at a time in both directions. */
    static int[] oracle(int[] nums) {
        int n = nums.length;
        int[] r = new int[n];
        for (int i = 0; i < n; i++) {
            int lo = i;
            int hi = i;
            while (lo > 0 && nums[lo - 1] >= nums[i]) lo--;
            while (hi < n - 1 && nums[hi + 1] >= nums[i]) hi++;
            r[i] = hi - lo + 1;
        }
        return r;
    }

    public static void main(String[] args) {
        // Example 1 and Example 2 from the exercise text.
        if (!Arrays.equals(solve(new int[] {4, 2, 5, 5, 3, 6}), new int[] {1, 6, 2, 2, 4, 1})) throw new AssertionError("example 1");
        if (!Arrays.equals(solve(new int[] {3, 1, 2, 2, 5}), new int[] {1, 5, 3, 3, 1})) throw new AssertionError("example 2");
        // Random arrays with repeated values must match the oracle.
        Random rnd = new Random(67);
        for (int t = 0; t < 3000; t++) {
            int[] a = new int[1 + rnd.nextInt(14)];
            for (int i = 0; i < a.length; i++) a[i] = rnd.nextInt(5);
            if (!Arrays.equals(solve(a), oracle(a))) throw new AssertionError(Arrays.toString(a));
        }
        System.out.println("ok");
    }
}
```
