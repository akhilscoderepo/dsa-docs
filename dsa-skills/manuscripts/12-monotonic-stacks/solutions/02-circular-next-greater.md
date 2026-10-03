<!-- solutions-for: 02-circular-next-greater -->
### Circular Next Greater

#### Solution: [Build] Circular Successor Indices (Author exercise)
<!-- id: ms-circular-successors -->

**Approach.** The position reached after `step` moves from `start` is `(start + step) % n`, and the walker takes `step` from 1 to `n - 1`, so the last position listed is the one just before `start`. No doubled array is needed, because the remainder performs the wrap. The assertions check the two examples, compare with a method that really builds a doubled array and slices it, and record the Java fact that a negative left operand keeps its sign in `%`, which is why a backward step must add `n` first.

**Complexity.** O(n) time to list the `n - 1` positions and O(n) space for the output, with O(1) extra space.

```java run
import java.util.Arrays;

public final class CircularSuccessors {
    static int[] successors(int n, int start) {
        int[] order = new int[n - 1];
        for (int step = 1; step < n; step++) order[step - 1] = (start + step) % n;
        return order;
    }
    static int[] oracle(int n, int start) {
        int[] doubled = new int[2 * n];
        for (int i = 0; i < 2 * n; i++) doubled[i] = i % n;
        return Arrays.copyOfRange(doubled, start + 1, start + n);
    }

    public static void main(String[] args) {
        if (!Arrays.equals(successors(5, 3), new int[]{4, 0, 1, 2})) throw new AssertionError("example 1");
        if (successors(1, 0).length != 0) throw new AssertionError("example 2");
        if (-1 % 5 != -1) throw new AssertionError("a negative left operand keeps its sign in %");
        if ((-1 + 5) % 5 != 4) throw new AssertionError("adding n before the remainder wraps backward");
        for (int n = 1; n <= 12; n++)
            for (int s = 0; s < n; s++)
                if (!Arrays.equals(successors(n, s), oracle(n, s))) throw new AssertionError("disagrees with the doubled array for n=" + n + " start=" + s);
    }
}
```

#### Solution: [Vary] Virtual Double Scan (Author exercise)
<!-- id: ms-virtual-double-scan -->

**Approach.** Walk virtual indices `j` from 0 to `2n - 1` and read `a[j % n]`. Pop each stack top that the current value strictly exceeds, and store `j` as its answer, which may be at least `n`. Push the real position only while `j < n`. The answer for a position is the smallest virtual index after it that qualifies, because pops happen in increasing `j`. The assertions compare with a method that scans virtual indices literally for every position, and show that pushing during the second lap makes positions appear twice on the stack.

**Complexity.** O(n) time and O(n) extra space, with no doubled array.

```java run
import java.util.ArrayDeque;
import java.util.Arrays;
import java.util.Random;

public final class VirtualDoubleScan {
    static int[] resolvingVirtualIndex(int[] a, boolean pushOnSecondLap, int[] maxDepth) {
        int n = a.length;
        int[] answer = new int[n];
        Arrays.fill(answer, -1);
        ArrayDeque<Integer> stack = new ArrayDeque<>();
        for (int j = 0; j < 2 * n; j++) {
            int p = j % n;
            while (!stack.isEmpty() && a[p] > a[stack.peekLast()]) {
                int top = stack.removeLast();
                if (answer[top] == -1) answer[top] = j;
            }
            if (j < n || pushOnSecondLap) stack.addLast(p);
            if (maxDepth != null) maxDepth[0] = Math.max(maxDepth[0], stack.size());
        }
        return answer;
    }
    static int[] oracle(int[] a) {
        int n = a.length;
        int[] r = new int[n];
        for (int i = 0; i < n; i++) {
            r[i] = -1;
            for (int j = i + 1; j < 2 * n; j++) if (a[j % n] > a[i]) { r[i] = j; break; }
        }
        return r;
    }

    public static void main(String[] args) {
        if (!Arrays.equals(resolvingVirtualIndex(new int[]{3, 8, 4, 1, 2}, false, null), new int[]{1, -1, 6, 4, 5})) throw new AssertionError("example 1");
        if (!Arrays.equals(resolvingVirtualIndex(new int[]{2, 1}, false, null), new int[]{-1, 2})) throw new AssertionError("example 2");
        int[] depth = {0};
        resolvingVirtualIndex(new int[]{9, 8, 7, 6}, false, depth);
        if (depth[0] != 4) throw new AssertionError("with first-lap pushes only the stack never exceeds n entries");
        depth[0] = 0;
        resolvingVirtualIndex(new int[]{9, 8, 7, 6}, true, depth);
        if (depth[0] <= 4) throw new AssertionError("pushing on the second lap puts positions on the stack twice");
        Random rnd = new Random(1212);
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(12);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(6);
            if (!Arrays.equals(resolvingVirtualIndex(a, false, null), oracle(a))) throw new AssertionError("disagrees with the literal virtual scan on " + Arrays.toString(a));
        }
    }
}
```

#### Solution: [Boundary] All Equal Circular Array (Author exercise)
<!-- id: ms-all-equal-circular -->

**Approach.** Use the strict comparison through both laps. When every value is equal, no value exceeds any waiting top, so nothing is popped and every position keeps -1, and since pushes happen only in the first lap the stack ends with exactly `n` positions. The same reasoning holds for a ring of one value. The assertions check both examples, count the waiting positions after the scan to confirm that no position was resolved, and compare with the walk-around method on random rings that use only two values so that ties are everywhere.

**Complexity.** O(n) time and O(n) extra space.

```java run
import java.util.ArrayDeque;
import java.util.Arrays;
import java.util.Random;

public final class AllEqualCircular {
    static int waiting;
    static int[] nextGreaterCircular(int[] a) {
        int n = a.length;
        int[] answer = new int[n];
        Arrays.fill(answer, -1);
        ArrayDeque<Integer> stack = new ArrayDeque<>();
        for (int j = 0; j < 2 * n; j++) {
            int p = j % n;
            while (!stack.isEmpty() && a[p] > a[stack.peekLast()]) answer[stack.removeLast()] = a[p];
            if (j < n) stack.addLast(p);
        }
        waiting = stack.size();
        return answer;
    }
    static int[] oracle(int[] a) {
        int n = a.length;
        int[] r = new int[n];
        for (int i = 0; i < n; i++) {
            r[i] = -1;
            for (int step = 1; step < n; step++) if (a[(i + step) % n] > a[i]) { r[i] = a[(i + step) % n]; break; }
        }
        return r;
    }

    public static void main(String[] args) {
        if (!Arrays.equals(nextGreaterCircular(new int[]{7, 7, 7, 7}), new int[]{-1, -1, -1, -1})) throw new AssertionError("example 1");
        if (waiting != 4) throw new AssertionError("all four positions stay on the stack");
        if (!Arrays.equals(nextGreaterCircular(new int[]{5}), new int[]{-1})) throw new AssertionError("example 2");
        if (waiting != 1) throw new AssertionError("a single position stays waiting");
        Random rnd = new Random(1213);
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(12);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(2);
            if (!Arrays.equals(nextGreaterCircular(a), oracle(a))) throw new AssertionError("disagrees with the walk-around method on " + Arrays.toString(a));
        }
    }
}
```

#### Solution: [Recognize] Next Greater Element II (LeetCode 503)
<!-- id: ms-next-greater-element-ii -->

**Approach.** This is the virtual double lap with the unresolved stack: iterate `j` from 0 to `2n - 1`, read `nums[j % n]`, pop and answer every top that the value strictly exceeds, and push only during the first lap. The assertions check the examples, compare with the walk-around method on random rings with negative values, show that the doubled-array alternative gives the same answers, and confirm the one-lap claim from the lesson: it is right when the largest value stands last and wrong for `[3, 8, 4, 1, 2]`.

**Complexity.** O(n) time and O(n) extra space.

```java run
import java.util.ArrayDeque;
import java.util.Arrays;
import java.util.Random;

public final class NextGreaterElementTwo {
    static int[] nextGreaterElements(int[] nums, int laps) {
        int n = nums.length;
        int[] answer = new int[n];
        Arrays.fill(answer, -1);
        ArrayDeque<Integer> stack = new ArrayDeque<>();
        for (int j = 0; j < laps * n; j++) {
            int p = j % n;
            while (!stack.isEmpty() && nums[p] > nums[stack.peekLast()]) answer[stack.removeLast()] = nums[p];
            if (j < n) stack.addLast(p);
        }
        return answer;
    }
    static int[] oracle(int[] a) {
        int n = a.length;
        int[] r = new int[n];
        for (int i = 0; i < n; i++) {
            r[i] = -1;
            for (int step = 1; step < n; step++) if (a[(i + step) % n] > a[i]) { r[i] = a[(i + step) % n]; break; }
        }
        return r;
    }
    static int[] viaDoubledArray(int[] a) {
        int n = a.length;
        int[] d = new int[2 * n];
        for (int i = 0; i < 2 * n; i++) d[i] = a[i % n];
        int[] r = new int[n];
        for (int i = 0; i < n; i++) {
            r[i] = -1;
            for (int j = i + 1; j < i + n; j++) if (d[j] > d[i]) { r[i] = d[j]; break; }
        }
        return r;
    }

    public static void main(String[] args) {
        if (!Arrays.equals(nextGreaterElements(new int[]{1, 2, 1}, 2), new int[]{2, -1, 2})) throw new AssertionError("example 1");
        if (!Arrays.equals(nextGreaterElements(new int[]{5, 4, 3, 2, 1}, 2), new int[]{-1, 5, 5, 5, 5})) throw new AssertionError("example 2");
        if (!Arrays.equals(nextGreaterElements(new int[]{1, 3, 2, 9}, 1), nextGreaterElements(new int[]{1, 3, 2, 9}, 2))) throw new AssertionError("one lap suffices when the maximum stands last");
        if (Arrays.equals(nextGreaterElements(new int[]{3, 8, 4, 1, 2}, 1), nextGreaterElements(new int[]{3, 8, 4, 1, 2}, 2))) throw new AssertionError("one lap is wrong for 3, 8, 4, 1, 2");
        Random rnd = new Random(1214);
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(12);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(7) - 3;
            int[] got = nextGreaterElements(a, 2);
            if (!Arrays.equals(got, oracle(a))) throw new AssertionError("disagrees with the walk-around method on " + Arrays.toString(a));
            if (!Arrays.equals(got, viaDoubledArray(a))) throw new AssertionError("disagrees with the doubled array on " + Arrays.toString(a));
        }
    }
}
```
