<!-- solutions-for: 01-next-greater-or-smaller -->
### Next Greater Or Smaller

#### Solution: [Build] Next Greater Value (Author exercise)
<!-- id: ms-next-greater-value -->

**Approach.** Scan left to right with a stack of positions whose values never increase from bottom to top. For each new value, pop every top that it strictly exceeds and write the new value as that top's answer, then push the new position. Positions left on the stack at the end keep -1. The assertions compare the stack scan with the forward-walking method on random arrays, check the stated invariant that stack values never increase after every step, and count pushes and pops to confirm that each position takes one push and at most one pop.

**Complexity.** O(n) time, because pushes and pops are each at most n in total, and O(n) extra space for the stack and the answer.

```java run
import java.util.ArrayDeque;
import java.util.Arrays;
import java.util.Random;

public final class NextGreaterValue {
    static long pushes, pops;
    static int[] nextGreaterValue(int[] a) {
        int n = a.length;
        int[] answer = new int[n];
        Arrays.fill(answer, -1);
        ArrayDeque<Integer> stack = new ArrayDeque<>();
        for (int j = 0; j < n; j++) {
            while (!stack.isEmpty() && a[j] > a[stack.peekLast()]) {
                answer[stack.removeLast()] = a[j];
                pops++;
            }
            stack.addLast(j);
            pushes++;
            int prev = Integer.MAX_VALUE;
            for (int idx : stack) {
                if (a[idx] > prev) throw new AssertionError("stack values must never increase from bottom to top");
                prev = a[idx];
            }
        }
        return answer;
    }
    static int[] oracle(int[] a) {
        int[] r = new int[a.length];
        for (int i = 0; i < a.length; i++) {
            r[i] = -1;
            for (int j = i + 1; j < a.length; j++) if (a[j] > a[i]) { r[i] = a[j]; break; }
        }
        return r;
    }

    public static void main(String[] args) {
        if (!Arrays.equals(nextGreaterValue(new int[]{2, 7, 3, 5, 4, 6, 8}), new int[]{7, 8, 5, 6, 6, 8, -1})) throw new AssertionError("example 1");
        if (!Arrays.equals(nextGreaterValue(new int[]{5, 4, 3}), new int[]{-1, -1, -1})) throw new AssertionError("example 2");
        if (!Arrays.equals(nextGreaterValue(new int[]{2, 7, 3, 9}), new int[]{7, 9, 9, -1})) throw new AssertionError("first greater, not the global maximum");
        Random rnd = new Random(1201);
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(14);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(8);
            pushes = 0; pops = 0;
            int[] got = nextGreaterValue(a);
            if (!Arrays.equals(got, oracle(a))) throw new AssertionError("disagrees with the forward walk on " + Arrays.toString(a));
            if (pushes != n || pops > pushes) throw new AssertionError("each position takes one push and at most one pop");
        }
    }
}
```

#### Solution: [Vary] Daily Temperatures (LeetCode 739)
<!-- id: ms-daily-temperatures -->

**Approach.** The scan is unchanged, but the answer is no longer the value that resolves a position. It is the distance `j - top`, so the stack must keep positions, and the answer array starts at 0 for the days that never see a warmer one. A value stored in the stack could not give a distance, and storing positions costs nothing extra. The assertions check both examples, compare with a forward walk on random readings, and confirm that readings which only fall leave every entry at 0.

**Complexity.** O(n) time and O(n) extra space.

```java run
import java.util.ArrayDeque;
import java.util.Arrays;
import java.util.Random;

public final class DailyTemperatures {
    static int[] dailyTemperatures(int[] t) {
        int[] answer = new int[t.length];
        ArrayDeque<Integer> stack = new ArrayDeque<>();
        for (int j = 0; j < t.length; j++) {
            while (!stack.isEmpty() && t[j] > t[stack.peekLast()]) {
                int top = stack.removeLast();
                answer[top] = j - top;
            }
            stack.addLast(j);
        }
        return answer;
    }
    static int[] oracle(int[] t) {
        int[] r = new int[t.length];
        for (int i = 0; i < t.length; i++)
            for (int j = i + 1; j < t.length; j++) if (t[j] > t[i]) { r[i] = j - i; break; }
        return r;
    }

    public static void main(String[] args) {
        if (!Arrays.equals(dailyTemperatures(new int[]{71, 69, 72, 65, 80, 75, 70}), new int[]{2, 1, 2, 1, 0, 0, 0})) throw new AssertionError("example 1");
        if (!Arrays.equals(dailyTemperatures(new int[]{90, 80, 70, 85}), new int[]{0, 2, 1, 0})) throw new AssertionError("example 2");
        if (!Arrays.equals(dailyTemperatures(new int[]{50, 40, 30, 20}), new int[]{0, 0, 0, 0})) throw new AssertionError("falling readings");
        Random rnd = new Random(1202);
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(14);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = 30 + rnd.nextInt(6);
            if (!Arrays.equals(dailyTemperatures(a), oracle(a))) throw new AssertionError("disagrees with the forward walk on " + Arrays.toString(a));
        }
    }
}
```

#### Solution: [Boundary] Equal Values Stay Unresolved (Author exercise)
<!-- id: ms-equal-stays-unresolved -->

**Approach.** Pop only while the current value is strictly greater than the top, and write the current index as the answer. With a strict test a tie leaves the earlier index waiting, which is correct because an equal value does not hide anybody, and the stack still never increases from bottom to top. The assertions show that popping on `>=` gives a different and wrong answer on the examples, and compare the strict version with a forward walk on arrays drawn from a tiny value range so that ties are frequent.

**Complexity.** O(n) time and O(n) extra space.

```java run
import java.util.ArrayDeque;
import java.util.Arrays;
import java.util.Random;

public final class EqualStaysUnresolved {
    static int[] nextGreaterIndex(int[] a, boolean strict) {
        int[] answer = new int[a.length];
        Arrays.fill(answer, -1);
        ArrayDeque<Integer> stack = new ArrayDeque<>();
        for (int j = 0; j < a.length; j++) {
            while (!stack.isEmpty() && (strict ? a[j] > a[stack.peekLast()] : a[j] >= a[stack.peekLast()])) {
                answer[stack.removeLast()] = j;
            }
            stack.addLast(j);
        }
        return answer;
    }
    static int[] oracle(int[] a) {
        int[] r = new int[a.length];
        for (int i = 0; i < a.length; i++) {
            r[i] = -1;
            for (int j = i + 1; j < a.length; j++) if (a[j] > a[i]) { r[i] = j; break; }
        }
        return r;
    }

    public static void main(String[] args) {
        if (!Arrays.equals(nextGreaterIndex(new int[]{4, 4, 5, 4}, true), new int[]{2, 2, -1, -1})) throw new AssertionError("example 1");
        if (!Arrays.equals(nextGreaterIndex(new int[]{3, 3, 3}, true), new int[]{-1, -1, -1})) throw new AssertionError("example 2");
        if (!Arrays.equals(nextGreaterIndex(new int[]{3, 3, 3}, false), new int[]{1, 2, -1})) throw new AssertionError("popping on equality resolves ties, which is wrong here");
        Random rnd = new Random(1203);
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(14);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(3) - 1;
            if (!Arrays.equals(nextGreaterIndex(a, true), oracle(a))) throw new AssertionError("disagrees with the forward walk on " + Arrays.toString(a));
        }
    }
}
```

#### Solution: [Recognize] Next Greater Element I (LeetCode 496)
<!-- id: ms-next-greater-element-i -->

**Approach.** The queries only matter through their positions in `reference`, so run the stack scan once over `reference` and store each resolved result in a map from the value to its next greater value. Positions that never resolve are not written, and the lookup falls back to -1 with `getOrDefault`. Values are distinct, so a value is a safe key. The assertions check the examples, compare against a method that finds each query's position and walks right, and use random permutations and random query subsets.

**Complexity.** O(r + q) time for `r` reference values and `q` queries, and O(r) extra space for the stack and the map.

```java run
import java.util.ArrayDeque;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Random;

public final class NextGreaterElementOne {
    static int[] nextGreaterElement(int[] queries, int[] reference) {
        HashMap<Integer, Integer> next = new HashMap<>();
        ArrayDeque<Integer> stack = new ArrayDeque<>();
        for (int j = 0; j < reference.length; j++) {
            while (!stack.isEmpty() && reference[j] > reference[stack.peekLast()]) {
                next.put(reference[stack.removeLast()], reference[j]);
            }
            stack.addLast(j);
        }
        int[] out = new int[queries.length];
        for (int i = 0; i < queries.length; i++) out[i] = next.getOrDefault(queries[i], -1);
        return out;
    }
    static int[] oracle(int[] queries, int[] reference) {
        int[] out = new int[queries.length];
        for (int i = 0; i < queries.length; i++) {
            int pos = 0;
            while (reference[pos] != queries[i]) pos++;
            out[i] = -1;
            for (int j = pos + 1; j < reference.length; j++) if (reference[j] > queries[i]) { out[i] = reference[j]; break; }
        }
        return out;
    }

    public static void main(String[] args) {
        if (!Arrays.equals(nextGreaterElement(new int[]{4, 1, 2}, new int[]{1, 3, 4, 2}), new int[]{-1, 3, -1})) throw new AssertionError("example 1");
        if (!Arrays.equals(nextGreaterElement(new int[]{2, 4}, new int[]{1, 2, 3, 4}), new int[]{3, -1})) throw new AssertionError("example 2");
        Random rnd = new Random(1204);
        for (int t = 0; t < 3000; t++) {
            int r = 1 + rnd.nextInt(10);
            int[] ref = new int[r];
            for (int i = 0; i < r; i++) ref[i] = i * 3 + 1;
            for (int i = r - 1; i > 0; i--) { int k = rnd.nextInt(i + 1); int tmp = ref[i]; ref[i] = ref[k]; ref[k] = tmp; }
            int q = 1 + rnd.nextInt(r);
            int[] qs = new int[q];
            for (int i = 0; i < q; i++) qs[i] = ref[rnd.nextInt(r)];
            if (!Arrays.equals(nextGreaterElement(qs, ref), oracle(qs, ref))) throw new AssertionError("disagrees with the position walk on " + Arrays.toString(ref));
        }
    }
}
```
