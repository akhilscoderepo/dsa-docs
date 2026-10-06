<!-- solutions-for: 12-monotonic-stacks -->
### Solutions For Finding The Next Greater Value

#### Solution: [Build] Next Greater Value (Author exercise)
<!-- id: ms-next-greater-value -->

**Approach.**
The scan keeps a stack of indices whose answers are still missing. Reading `nums[i]`, the loop pops every top index whose value is smaller. It writes `nums[i]` as the answer of each popped index, because `i` is the first position after that index with a larger value. The loop stops at the first top that is not smaller. The invariant is that the values behind the stack indices never increase from bottom to top, so no index below the stopping point can be smaller than `nums[i]`. The loop then pushes index `i`, and the indices left at the end keep `-1`.

**Complexity.**
- **Time** is O(n), because the loop pushes each index once and pops it at most once.
- **Space** is O(n) for the stack and the answer array, and the stack alone reaches n on a non-increasing input.

```java run
import java.util.ArrayDeque;
import java.util.Arrays;
import java.util.Deque;
import java.util.Random;

public final class NextGreaterValue {
    /**
     * Returns the first strictly greater later value for every index, or -1.
     * Time: O(n), each index is pushed once and popped at most once.
     * Space: O(n) for the stack.
     * Invariant: values at stack indices never increase from bottom to top.
     */
    static int[] solve(int[] nums) {
        int[] ans = new int[nums.length];
        // Every answer starts at -1 and changes only when an index resolves.
        Arrays.fill(ans, -1);
        Deque<Integer> stack = new ArrayDeque<>();
        // One left-to-right pass reads each value exactly once.
        for (int i = 0; i < nums.length; i++) {
            // The condition pops while the top value is strictly smaller, so ties stay.
            while (!stack.isEmpty() && nums[stack.peek()] < nums[i]) {
                // Index i is the first greater position for the popped index.
                ans[stack.pop()] = nums[i];
            }
            // The new index waits for its own answer.
            stack.push(i);
        }
        return ans;
    }

    /** Reference: scan to the right from every index. */
    static int[] oracle(int[] nums) {
        int[] ans = new int[nums.length];
        for (int i = 0; i < nums.length; i++) {
            ans[i] = -1;
            for (int j = i + 1; j < nums.length; j++) {
                if (nums[j] > nums[i]) { ans[i] = nums[j]; break; }
            }
        }
        return ans;
    }

    public static void main(String[] args) {
        // Example 1 and Example 2 from the exercise text.
        if (!Arrays.equals(solve(new int[] {6, 2, 4, 3, 9, 5, 7}), new int[] {9, 4, 9, 9, -1, 7, -1})) throw new AssertionError("example 1");
        if (!Arrays.equals(solve(new int[] {5, 4, 3, 2, 1}), new int[] {-1, -1, -1, -1, -1})) throw new AssertionError("example 2");
        // Ties stay unresolved, and the input array is not modified.
        int[] tie = {3, 3, 3};
        if (!Arrays.equals(solve(tie), new int[] {-1, -1, -1}) || !Arrays.equals(tie, new int[] {3, 3, 3})) throw new AssertionError("ties");
        // Random arrays with many repeated values must match the oracle.
        Random rnd = new Random(7);
        for (int t = 0; t < 3000; t++) {
            int[] a = new int[rnd.nextInt(12)];
            for (int i = 0; i < a.length; i++) a[i] = rnd.nextInt(6);
            if (!Arrays.equals(solve(a), oracle(a))) throw new AssertionError(Arrays.toString(a));
        }
        System.out.println("ok");
    }
}
```

#### Solution: [Vary] Daily Temperatures (LeetCode 739)
<!-- id: ms-daily-temperatures -->

**Approach.**
The loop is the same as in the previous solution, but the stack must hold indices because the output is a difference of positions. When day `d` pops index `e`, the first higher reading after `e` is on day `d`, so the waiting time is `d - e`. Days that never pop keep the default `0`, which matches the required no-answer marker. The invariant is the same: the readings at stack indices never increase from bottom to top.

**Complexity.**
- **Time** is O(n), because each day enters and leaves the stack at most once.
- **Space** is O(n), for the output array plus a stack that holds up to n days.

```java run
import java.util.ArrayDeque;
import java.util.Arrays;
import java.util.Deque;
import java.util.Random;

public final class DailyTemperatures {
    /**
     * Returns the days to wait for a strictly higher reading, or 0.
     * Time: O(n). Space: O(n).
     * Invariant: readings at stack indices never increase from bottom to top.
     */
    static int[] solve(int[] temps) {
        // Default 0 already encodes "no warmer day".
        int[] wait = new int[temps.length];
        Deque<Integer> stack = new ArrayDeque<>();
        // The loop variable is the candidate resolving day.
        for (int day = 0; day < temps.length; day++) {
            // Pop every earlier day that this reading beats strictly.
            while (!stack.isEmpty() && temps[stack.peek()] < temps[day]) {
                int earlier = stack.pop();
                // The distance exists only because the stack stores indices.
                wait[earlier] = day - earlier;
            }
            // The current day waits for a higher reading.
            stack.push(day);
        }
        return wait;
    }

    /** Reference: scan forward from every day. */
    static int[] oracle(int[] t) {
        int[] r = new int[t.length];
        for (int i = 0; i < t.length; i++) {
            for (int j = i + 1; j < t.length; j++) {
                if (t[j] > t[i]) { r[i] = j - i; break; }
            }
        }
        return r;
    }

    public static void main(String[] args) {
        // Example 1 and Example 2 from the exercise text.
        if (!Arrays.equals(solve(new int[] {71, 70, 75, 70, 69, 72, 80, 68}), new int[] {2, 1, 4, 2, 1, 1, 0, 0})) throw new AssertionError("example 1");
        if (!Arrays.equals(solve(new int[] {60, 60, 61, 59, 62}), new int[] {2, 1, 2, 1, 0})) throw new AssertionError("example 2");
        // Random readings in the allowed range must match the oracle.
        Random rnd = new Random(11);
        for (int t = 0; t < 3000; t++) {
            int[] a = new int[1 + rnd.nextInt(15)];
            for (int i = 0; i < a.length; i++) a[i] = 30 + rnd.nextInt(6);
            if (!Arrays.equals(solve(a), oracle(a))) throw new AssertionError(Arrays.toString(a));
        }
        System.out.println("ok");
    }
}
```

#### Solution: [Boundary] Equal Values Stay Unresolved (Author exercise)
<!-- id: ms-equal-values-stay-unresolved -->

**Approach.**
An index is open exactly when it is never popped, so the answer is the stack size after the last value. The pop condition must be strictly smaller. With a non-strict comparison, an equal later value would pop the earlier index and report it as closed, which contradicts the definition. The strict comparison also keeps equal values side by side on the stack, and the invariant that values never increase from bottom to top still holds. An empty array skips the loop and returns `0`.

**Complexity.**
- **Time** is O(n), because the loop pushes every index once and pops it at most once.
- **Space** is O(n), because an all-equal array keeps every index on the stack.

```java run
import java.util.ArrayDeque;
import java.util.Deque;
import java.util.Random;

public final class OpenIndices {
    /**
     * Counts indices with no strictly greater value after them.
     * Time: O(n). Space: O(n).
     * Invariant: stack values never increase from bottom to top, ties included.
     */
    static int solve(int[] nums) {
        Deque<Integer> stack = new ArrayDeque<>();
        // The loop reads each value once, so an empty array skips it.
        for (int i = 0; i < nums.length; i++) {
            // Strict comparison keeps equal values on the stack.
            while (!stack.isEmpty() && nums[stack.peek()] < nums[i]) stack.pop();
            stack.push(i);
        }
        // Whatever remains was never beaten by a later value.
        return stack.size();
    }

    /** Reference: check every later value for every index. */
    static int oracle(int[] nums) {
        int open = 0;
        for (int i = 0; i < nums.length; i++) {
            boolean beaten = false;
            for (int j = i + 1; j < nums.length; j++) if (nums[j] > nums[i]) beaten = true;
            if (!beaten) open++;
        }
        return open;
    }

    public static void main(String[] args) {
        // Example 1 and Example 2 from the exercise text.
        if (solve(new int[] {2, 2, 3, 3, 1}) != 3) throw new AssertionError("example 1");
        if (solve(new int[] {5, 5, 5, 5}) != 4) throw new AssertionError("example 2");
        // Empty input has no open index.
        if (solve(new int[0]) != 0) throw new AssertionError("empty");
        // Random arrays with heavy repetition must match the oracle.
        Random rnd = new Random(13);
        for (int t = 0; t < 3000; t++) {
            int[] a = new int[rnd.nextInt(12)];
            for (int i = 0; i < a.length; i++) a[i] = rnd.nextInt(4) - 2;
            if (solve(a) != oracle(a)) throw new AssertionError("random");
        }
        System.out.println("ok");
    }
}
```

#### Solution: [Recognize] Next Greater Element I (LeetCode 496)
<!-- id: ms-next-greater-element-one -->

**Approach.**
The query array adds nothing to the scan, because every question is about a position in `nums2`. One stack pass over `nums2` stores the next greater value for each value in a `HashMap`. The values are distinct, so a value names exactly one position and the map has no collisions. Each entry of `nums1` then reads its stored answer, or `-1` when the value never resolved. The invariant is the same stack order as in the earlier solutions.

**Complexity.**
- **Time** is O(m + n) for `m = nums1.length` and `n = nums2.length`, with one stack pass and one map lookup per query.
- **Space** is O(n) for the map and the stack.

```java run
import java.util.ArrayDeque;
import java.util.Arrays;
import java.util.Deque;
import java.util.HashMap;
import java.util.Map;
import java.util.Random;

public final class NextGreaterSubset {
    /**
     * Answers the next greater value in nums2 for every value of nums1.
     * Time: O(m + n). Space: O(n).
     * Invariant: values at stack indices never increase from bottom to top.
     */
    static int[] solve(int[] nums1, int[] nums2) {
        // The map links a value of nums2 to its next greater value.
        Map<Integer, Integer> next = new HashMap<>();
        Deque<Integer> stack = new ArrayDeque<>();
        // One pass over the reference array resolves every position.
        for (int i = 0; i < nums2.length; i++) {
            while (!stack.isEmpty() && nums2[stack.peek()] < nums2[i]) {
                // The popped value gets the current value as its answer.
                next.put(nums2[stack.pop()], nums2[i]);
            }
            stack.push(i);
        }
        int[] ans = new int[nums1.length];
        // Each query is a map lookup, with -1 for values that never resolved.
        for (int k = 0; k < nums1.length; k++) ans[k] = next.getOrDefault(nums1[k], -1);
        return ans;
    }

    /** Reference: locate each value in nums2 and scan to its right. */
    static int[] oracle(int[] nums1, int[] nums2) {
        int[] ans = new int[nums1.length];
        for (int k = 0; k < nums1.length; k++) {
            int pos = 0;
            while (nums2[pos] != nums1[k]) pos++;
            ans[k] = -1;
            for (int j = pos + 1; j < nums2.length; j++) {
                if (nums2[j] > nums1[k]) { ans[k] = nums2[j]; break; }
            }
        }
        return ans;
    }

    public static void main(String[] args) {
        // Example 1 and Example 2 from the exercise text.
        if (!Arrays.equals(solve(new int[] {3, 5}, new int[] {5, 2, 3, 8, 4}), new int[] {8, 8})) throw new AssertionError("example 1");
        if (!Arrays.equals(solve(new int[] {9, 1}, new int[] {1, 9, 4, 7}), new int[] {-1, 9})) throw new AssertionError("example 2");
        // Random permutations with random subsets must match the oracle.
        Random rnd = new Random(17);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(10);
            Integer[] boxed = new Integer[n];
            for (int i = 0; i < n; i++) boxed[i] = i * 3;
            java.util.Collections.shuffle(Arrays.asList(boxed), rnd);
            int[] nums2 = new int[n];
            for (int i = 0; i < n; i++) nums2[i] = boxed[i];
            int m = 1 + rnd.nextInt(n);
            int[] nums1 = new int[m];
            for (int i = 0; i < m; i++) nums1[i] = nums2[i];
            if (!Arrays.equals(solve(nums1, nums2), oracle(nums1, nums2))) throw new AssertionError("random");
        }
        System.out.println("ok");
    }
}
```
