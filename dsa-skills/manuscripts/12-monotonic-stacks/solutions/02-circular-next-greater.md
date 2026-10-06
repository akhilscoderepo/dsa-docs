<!-- solutions-for: 12-monotonic-stacks -->
### Solutions For The Circular Scan

#### Solution: [Build] Circular Successor Indices (Author exercise)
<!-- id: ms-circular-successor-index -->

**Approach.**
The k-th slot after `s` has index `(s + k) % n`. The loop takes `k` from `1` through `n - 1`, which visits every other slot exactly once and never returns to `s`. The first slot with a strictly greater value ends the walk, so the loop returns its index. The invariant is that all slots visited before the current `k` hold values not greater than `nums[s]`. Reaching the end of the loop proves that no slot qualifies, and the method returns `-1`.

**Complexity.**
- **Time** is O(n), because the walk visits at most `n - 1` slots.
- **Space** is O(1), because the method keeps only the loop counter and the current index.

```java run
import java.util.Random;

public final class CircularSuccessor {
    /**
     * Returns the first slot after s in circular order with a strictly greater value, or -1.
     * Time: O(n). Space: O(1).
     * Invariant: slots visited before step k are all at most nums[s].
     */
    static int solve(int[] nums, int s) {
        int n = nums.length;
        // At most n - 1 steps keep the walk from reaching slot s again.
        for (int k = 1; k < n; k++) {
            // The modulus wraps the slot index from n - 1 back to 0.
            int j = (s + k) % n;
            // A strictly greater value ends the walk with the nearest slot in ring order.
            if (nums[j] > nums[s]) return j;
        }
        // No visited slot was greater.
        return -1;
    }

    /** Reference: copy the ring into a list of 2n slots and search after position s. */
    static int oracle(int[] nums, int s) {
        int n = nums.length;
        int[] twice = new int[2 * n];
        for (int p = 0; p < 2 * n; p++) twice[p] = nums[p % n];
        for (int p = s + 1; p < s + n; p++) if (twice[p] > nums[s]) return p % n;
        return -1;
    }

    public static void main(String[] args) {
        // Example 1 and Example 2 from the exercise text.
        if (solve(new int[] {3, 8, 4, 1, 2}, 2) != 1) throw new AssertionError("example 1");
        if (solve(new int[] {7, 7, 7, 7}, 0) != -1) throw new AssertionError("example 2");
        // A single slot never answers itself.
        if (solve(new int[] {5}, 0) != -1) throw new AssertionError("single slot");
        // Random rings and starts must match the oracle.
        Random rnd = new Random(21);
        for (int t = 0; t < 3000; t++) {
            int[] a = new int[1 + rnd.nextInt(10)];
            for (int i = 0; i < a.length; i++) a[i] = rnd.nextInt(5);
            int s = rnd.nextInt(a.length);
            if (solve(a, s) != oracle(a, s)) throw new AssertionError("random");
        }
        System.out.println("ok");
    }
}
```

#### Solution: [Vary] Virtual Double Scan (Author exercise)
<!-- id: ms-virtual-double-scan -->

**Approach.**
The scan reads virtual positions `p` from `0` to `2n - 1` and maps each one to the real index `p % n`. Real indices are pushed only while `p < n`, so each index waits on the stack once. A read at position `p` pops every top index `t` whose value is smaller, and the steps for `t` equal `p - t`. The distance is correct because `t < n <= p` or `t < p` in the first pass, and the first resolving position is the nearest one in ring order. The invariant is that stack values never increase from bottom to top. Indices that never pop keep the default `0`.

**Complexity.**
- **Time** is O(n), because there are `2n` reads and each index pops at most once.
- **Space** is O(n), for the stack and the output.

```java run
import java.util.ArrayDeque;
import java.util.Arrays;
import java.util.Deque;
import java.util.Random;

public final class VirtualDoubleScan {
    /**
     * Returns the circular steps to the first strictly greater slot, or 0.
     * Time: O(n). Space: O(n).
     * Invariant: stack values never increase from bottom to top.
     */
    static int[] solve(int[] nums) {
        int n = nums.length;
        int[] steps = new int[n];
        Deque<Integer> stack = new ArrayDeque<>();
        // Two passes of virtual positions, with no second array.
        for (int p = 0; p < 2 * n; p++) {
            int i = p % n;
            // A strictly greater read resolves the top index at distance p - top.
            while (!stack.isEmpty() && nums[stack.peek()] < nums[i]) {
                int t = stack.pop();
                steps[t] = p - t;
            }
            // Only the first pass pushes, so each real index waits once.
            if (p < n) stack.push(i);
        }
        return steps;
    }

    /** Reference: walk the ring from every slot. */
    static int[] oracle(int[] nums) {
        int n = nums.length;
        int[] r = new int[n];
        for (int i = 0; i < n; i++) {
            for (int k = 1; k < n; k++) {
                if (nums[(i + k) % n] > nums[i]) { r[i] = k; break; }
            }
        }
        return r;
    }

    public static void main(String[] args) {
        // Example 1 and Example 2 from the exercise text.
        if (!Arrays.equals(solve(new int[] {3, 8, 4, 1, 2}), new int[] {1, 0, 4, 1, 1})) throw new AssertionError("example 1");
        if (!Arrays.equals(solve(new int[] {1, 2, 3, 2, 1}), new int[] {1, 1, 0, 4, 2})) throw new AssertionError("example 2");
        // Random rings with repeated values must match the oracle.
        Random rnd = new Random(23);
        for (int t = 0; t < 3000; t++) {
            int[] a = new int[1 + rnd.nextInt(12)];
            for (int i = 0; i < a.length; i++) a[i] = rnd.nextInt(5);
            if (!Arrays.equals(solve(a), oracle(a))) throw new AssertionError(Arrays.toString(a));
        }
        System.out.println("ok");
    }
}
```

#### Solution: [Boundary] All Equal Circular Array (Author exercise)
<!-- id: ms-all-equal-circular -->

**Approach.**
The same two-pass scan applies, and the strict comparison carries the whole edge case. Position `i + n` reads a value equal to `nums[i]`, so it cannot resolve index `i`. An all-equal array therefore never pops and every answer stays `-1`. A one-slot array pushes index 0 in the first pass and reads the same value in the second pass, which pops nothing. The invariant is unchanged: stack values never increase from bottom to top, and equal values sit side by side. The harness also checks that pushing during both passes gives identical answers, so the second-pass push is only wasted work.

**Complexity.**
- **Time** is O(n), because the scan makes `2n` reads and pops each index at most once.
- **Space** is O(n), because an all-equal array keeps every index on the stack.

```java run
import java.util.ArrayDeque;
import java.util.Arrays;
import java.util.Deque;
import java.util.Random;

public final class AllEqualRing {
    /**
     * Returns the first strictly greater value in circular order, or -1.
     * Time: O(n). Space: O(n).
     * Invariant: stack values never increase from bottom to top.
     */
    static int[] solve(int[] nums, boolean pushBothPasses) {
        int n = nums.length;
        int[] ans = new int[n];
        // Every answer starts at -1 and changes only on a strict resolution.
        Arrays.fill(ans, -1);
        Deque<Integer> stack = new ArrayDeque<>();
        for (int p = 0; p < 2 * n; p++) {
            int i = p % n;
            // Strict comparison keeps ties on the stack and off the answers.
            while (!stack.isEmpty() && nums[stack.peek()] < nums[i]) ans[stack.pop()] = nums[i];
            // The normal solution pushes only in the first pass.
            if (p < n || pushBothPasses) stack.push(i);
        }
        return ans;
    }

    /** Reference: walk the ring from every slot. */
    static int[] oracle(int[] nums) {
        int n = nums.length;
        int[] r = new int[n];
        for (int i = 0; i < n; i++) {
            r[i] = -1;
            for (int k = 1; k < n; k++) {
                if (nums[(i + k) % n] > nums[i]) { r[i] = nums[(i + k) % n]; break; }
            }
        }
        return r;
    }

    public static void main(String[] args) {
        // Example 1 and Example 2 from the exercise text.
        if (!Arrays.equals(solve(new int[] {7, 7, 7, 7}, false), new int[] {-1, -1, -1, -1})) throw new AssertionError("example 1");
        if (!Arrays.equals(solve(new int[] {2, 2, 5, 2}, false), new int[] {5, 5, -1, 5})) throw new AssertionError("example 2");
        // A single slot returns -1.
        if (!Arrays.equals(solve(new int[] {4}, false), new int[] {-1})) throw new AssertionError("single");
        // Random rings, including many ties, must match the oracle and the push-always variant.
        Random rnd = new Random(29);
        for (int t = 0; t < 3000; t++) {
            int[] a = new int[1 + rnd.nextInt(10)];
            for (int i = 0; i < a.length; i++) a[i] = rnd.nextInt(3);
            int[] expect = oracle(a);
            if (!Arrays.equals(solve(a, false), expect)) throw new AssertionError("first pass push " + Arrays.toString(a));
            if (!Arrays.equals(solve(a, true), expect)) throw new AssertionError("both passes push " + Arrays.toString(a));
        }
        System.out.println("ok");
    }
}
```

#### Solution: [Recognize] Next Greater Element II (LeetCode 503)
<!-- id: ms-next-greater-element-two -->

**Approach.**
The cue is a successor that wraps, so the scan covers `2n` virtual positions and pushes real indices only in the first pass. An index left on the stack after the first pass has no greater value to its right. The second pass lets those indices meet the values that precede them in the array. The answers are written as values at the pop, with `-1` as the default. The invariant is that stack values never increase from bottom to top, which lets each read stop as soon as one top survives.

**Complexity.**
- **Time** is O(n), because the loop makes `2n` reads and each index pops at most once.
- **Space** is O(n), for the stack and the answer array.

```java run
import java.util.ArrayDeque;
import java.util.Arrays;
import java.util.Deque;
import java.util.Random;

public final class NextGreaterTwo {
    /**
     * Returns the next greater element in circular order for every slot.
     * Time: O(n). Space: O(n).
     * Invariant: stack values never increase from bottom to top.
     */
    static int[] nextGreaterElements(int[] nums) {
        int n = nums.length;
        int[] ans = new int[n];
        Arrays.fill(ans, -1);
        Deque<Integer> stack = new ArrayDeque<>();
        // The virtual position p covers the array twice.
        for (int p = 0; p < 2 * n; p++) {
            int i = p % n;
            // The current read resolves every smaller top.
            while (!stack.isEmpty() && nums[stack.peek()] < nums[i]) ans[stack.pop()] = nums[i];
            // Pushing in the first pass only keeps each slot on the stack once.
            if (p < n) stack.push(i);
        }
        return ans;
    }

    /** Reference: walk the ring from every slot. */
    static int[] oracle(int[] nums) {
        int n = nums.length;
        int[] r = new int[n];
        for (int i = 0; i < n; i++) {
            r[i] = -1;
            for (int k = 1; k < n; k++) {
                if (nums[(i + k) % n] > nums[i]) { r[i] = nums[(i + k) % n]; break; }
            }
        }
        return r;
    }

    public static void main(String[] args) {
        // Example 1 and Example 2 from the exercise text.
        if (!Arrays.equals(nextGreaterElements(new int[] {6, 2, 9, 4, 4}), new int[] {9, 9, -1, 6, 6})) throw new AssertionError("example 1");
        if (!Arrays.equals(nextGreaterElements(new int[] {5, -3, 0, 5, -3}), new int[] {-1, 0, 5, -1, 5})) throw new AssertionError("example 2");
        // Random rings with negative and repeated values must match the oracle.
        Random rnd = new Random(31);
        for (int t = 0; t < 3000; t++) {
            int[] a = new int[1 + rnd.nextInt(12)];
            for (int i = 0; i < a.length; i++) a[i] = rnd.nextInt(7) - 3;
            if (!Arrays.equals(nextGreaterElements(a), oracle(a))) throw new AssertionError(Arrays.toString(a));
        }
        System.out.println("ok");
    }
}
```
