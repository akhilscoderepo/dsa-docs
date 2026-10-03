<!-- solutions-for: 05-sliding-maximum -->
### Sliding Maximum

#### Solution: [Build] Maximum Of One Moving Window (Author exercise)
<!-- id: dq-maximum-one-window -->

**Approach.** For each right edge do the four moves in order: remove expired indices from the front, remove dominated indices from the back, append the new index, and read the front once the window is complete. Only the last read is returned. Reading before the first two moves would return an expired or dominated value, which the assertions demonstrate on a case where the front is stale before expiry. The assertions check both examples and compare with a direct scan of the last window on random arrays.

**Complexity.** O(n) time and O(k) memory.

```java run
import java.util.ArrayDeque;
import java.util.Random;

public final class MaximumOneWindow {
    static int lastWindowMax(int[] a, int k) {
        ArrayDeque<Integer> d = new ArrayDeque<>();
        int answer = Integer.MIN_VALUE;
        for (int right = 0; right < a.length; right++) {
            while (!d.isEmpty() && d.peekFirst() <= right - k) d.removeFirst();
            while (!d.isEmpty() && a[d.peekLast()] < a[right]) d.removeLast();
            d.addLast(right);
            if (right >= k - 1) answer = a[d.peekFirst()];
        }
        return answer;
    }
    static int staleReadBeforeExpiry(int[] a, int k, int right) {
        ArrayDeque<Integer> d = new ArrayDeque<>();
        for (int r = 0; r <= right; r++) {
            if (r == right) return a[d.peekFirst()];
            while (!d.isEmpty() && d.peekFirst() <= r - k) d.removeFirst();
            while (!d.isEmpty() && a[d.peekLast()] < a[r]) d.removeLast();
            d.addLast(r);
        }
        throw new AssertionError("unreachable");
    }

    public static void main(String[] args) {
        if (lastWindowMax(new int[]{9, 4, 7, 1, 6, 3, 5}, 4) != 6) throw new AssertionError("example 1");
        if (lastWindowMax(new int[]{2}, 1) != 2) throw new AssertionError("example 2");
        int[] a = {9, 1, 1, 1};
        if (staleReadBeforeExpiry(a, 3, 3) != 9) throw new AssertionError("before expiry the front still holds the old 9");
        if (lastWindowMax(a, 3) != 1) throw new AssertionError("after expiry the answer is 1");
        Random rnd = new Random(1341);
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(16);
            int[] arr = new int[n];
            for (int i = 0; i < n; i++) arr[i] = rnd.nextInt(8) - 3;
            int k = 1 + rnd.nextInt(n);
            int expected = Integer.MIN_VALUE;
            for (int j = n - k; j < n; j++) expected = Math.max(expected, arr[j]);
            if (lastWindowMax(arr, k) != expected) throw new AssertionError("disagrees with the scan on " + java.util.Arrays.toString(arr) + " k=" + k);
        }
    }
}
```

#### Solution: [Vary] Return Maximum Indices (Author exercise)
<!-- id: dq-return-maximum-indices -->

**Approach.** The deque already holds indices, so the answer for a window is the front itself and not the value read through it. With strictly smaller removal, equal values stay in arrival order, so among equal maxima the earliest sits at the front, which gives the smallest index. A deque of values could return the maximum but not where it was. The assertions check both examples, compare with a scan that reports the smallest index of the maximum, and confirm that the replace-equals policy returns the largest index instead, so the policy is what decides the reported position.

**Complexity.** O(n) time and O(k) memory.

```java run
import java.util.ArrayDeque;
import java.util.Arrays;
import java.util.Random;

public final class ReturnMaximumIndices {
    static int[] maxIndices(int[] a, int k, boolean replaceEquals) {
        int[] out = new int[a.length - k + 1];
        ArrayDeque<Integer> d = new ArrayDeque<>();
        for (int right = 0; right < a.length; right++) {
            while (!d.isEmpty() && d.peekFirst() <= right - k) d.removeFirst();
            while (!d.isEmpty() && (replaceEquals ? a[d.peekLast()] <= a[right] : a[d.peekLast()] < a[right])) d.removeLast();
            d.addLast(right);
            if (right >= k - 1) out[right - k + 1] = d.peekFirst();
        }
        return out;
    }
    static int[] scan(int[] a, int k, boolean smallest) {
        int[] out = new int[a.length - k + 1];
        for (int s = 0; s + k <= a.length; s++) {
            int best = s;
            for (int j = s + 1; j < s + k; j++) if (smallest ? a[j] > a[best] : a[j] >= a[best]) best = j;
            out[s] = best;
        }
        return out;
    }

    public static void main(String[] args) {
        if (!Arrays.equals(maxIndices(new int[]{3, 5, 5, 2, 5}, 3, false), new int[]{1, 1, 2})) throw new AssertionError("example 1");
        if (!Arrays.equals(maxIndices(new int[]{7, 7, 7}, 2, false), new int[]{0, 1})) throw new AssertionError("example 2");
        Random rnd = new Random(1342);
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(16);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(4);
            int k = 1 + rnd.nextInt(n);
            if (!Arrays.equals(maxIndices(a, k, false), scan(a, k, true))) throw new AssertionError("keep equals gives the smallest index on " + Arrays.toString(a) + " k=" + k);
            if (!Arrays.equals(maxIndices(a, k, true), scan(a, k, false))) throw new AssertionError("replace equals gives the largest index on " + Arrays.toString(a) + " k=" + k);
        }
    }
}
```

#### Solution: [Boundary] Increasing, Decreasing, And Equal Arrays (Author exercise)
<!-- id: dq-increasing-decreasing-equal -->

**Approach.** Run the window deque and count the pops at each end and the peak size. An increasing array makes every arrival remove the whole deque from the back, so the peak is 1 and there are `n - 1` back removals, and nothing ever expires because the deque holds only the newest index, except when `k = 1`, where expiry empties the deque first and the back loop has nothing left to remove. A decreasing array removes nothing from the back, fills the deque to `k` and expires the front once per step after the first window, which gives `n - k` front removals. An array of equal values behaves like a decreasing one when equals are kept. The assertions check the examples, the closed forms for the three shapes on random sizes, and compare the peak with `k` as an upper bound on random arrays.

**Complexity.** O(n) time and O(k) memory.

```java run
import java.util.ArrayDeque;
import java.util.Arrays;
import java.util.Random;

public final class IncreasingDecreasingEqual {
    static int[] profile(int[] a, int k) {
        int peak = 0, back = 0, front = 0;
        ArrayDeque<Integer> d = new ArrayDeque<>();
        for (int right = 0; right < a.length; right++) {
            while (!d.isEmpty() && d.peekFirst() <= right - k) { d.removeFirst(); front++; }
            while (!d.isEmpty() && a[d.peekLast()] < a[right]) { d.removeLast(); back++; }
            d.addLast(right);
            peak = Math.max(peak, d.size());
        }
        return new int[]{peak, back, front};
    }

    public static void main(String[] args) {
        if (!Arrays.equals(profile(new int[]{2, 2, 2, 2, 2}, 3), new int[]{3, 0, 2})) throw new AssertionError("example 1");
        if (!Arrays.equals(profile(new int[]{5, 4, 3, 2, 1}, 3), new int[]{3, 0, 2})) throw new AssertionError("example 2");
        if (!Arrays.equals(profile(new int[]{1, 2, 3, 4, 5}, 3), new int[]{1, 4, 0})) throw new AssertionError("increasing array");
        Random rnd = new Random(1343);
        for (int t = 0; t < 3000; t++) {
            int n = 2 + rnd.nextInt(30);
            int k = 1 + rnd.nextInt(n);
            int[] inc = new int[n], dec = new int[n], eq = new int[n];
            for (int i = 0; i < n; i++) { inc[i] = i; dec[i] = n - i; eq[i] = 4; }
            int[] incWant = k == 1 ? new int[]{1, 0, n - 1} : new int[]{1, n - 1, 0};
            if (!Arrays.equals(profile(inc, k), incWant)) throw new AssertionError("increasing shape n=" + n + " k=" + k);
            if (!Arrays.equals(profile(dec, k), new int[]{k, 0, n - k})) throw new AssertionError("decreasing shape n=" + n + " k=" + k);
            if (!Arrays.equals(profile(eq, k), new int[]{k, 0, n - k})) throw new AssertionError("equal shape n=" + n + " k=" + k);
            int[] r = new int[n];
            for (int i = 0; i < n; i++) r[i] = rnd.nextInt(5);
            if (profile(r, k)[0] > k) throw new AssertionError("the deque never holds more than k indices");
        }
    }
}
```

#### Solution: [Recognize] Sliding Window Maximum (LeetCode 239)
<!-- id: dq-sliding-window-maximum -->

**Approach.** Run the four-step turn for every right edge and write the front's value to slot `right - k + 1` once the first window is complete. The deque holds in-window indices with non-increasing values, so the front is the window maximum. The assertions check the examples, compare with the brute-force scan on random arrays including negative values, compare with a `PriorityQueue` that deletes stale entries lazily, which is the heap alternative named in the lesson, and verify the claim about values-only deques: expiring by comparing the departing value works while equals are kept, and fails when equals are replaced.

**Complexity.** O(n) time and O(k) extra memory, against O(n k) for the scan and O(n log k) for the heap.

```java run
import java.util.ArrayDeque;
import java.util.Arrays;
import java.util.PriorityQueue;
import java.util.Random;

public final class SlidingWindowMaximum {
    static int[] maxSlidingWindow(int[] nums, int k) {
        int n = nums.length;
        int[] out = new int[n - k + 1];
        ArrayDeque<Integer> d = new ArrayDeque<>();
        for (int right = 0; right < n; right++) {
            while (!d.isEmpty() && d.peekFirst() <= right - k) d.removeFirst();
            while (!d.isEmpty() && nums[d.peekLast()] < nums[right]) d.removeLast();
            d.addLast(right);
            if (right >= k - 1) out[right - k + 1] = nums[d.peekFirst()];
        }
        return out;
    }
    static int[] brute(int[] a, int k) {
        int[] out = new int[a.length - k + 1];
        for (int s = 0; s + k <= a.length; s++) {
            int m = Integer.MIN_VALUE;
            for (int j = s; j < s + k; j++) m = Math.max(m, a[j]);
            out[s] = m;
        }
        return out;
    }
    static int[] heap(int[] a, int k) {
        int[] out = new int[a.length - k + 1];
        PriorityQueue<int[]> pq = new PriorityQueue<>((x, y) -> y[0] - x[0]);
        for (int right = 0; right < a.length; right++) {
            pq.add(new int[]{a[right], right});
            while (pq.peek()[1] <= right - k) pq.poll();
            if (right >= k - 1) out[right - k + 1] = pq.peek()[0];
        }
        return out;
    }
    static int[] valuesOnly(int[] a, int k, boolean replaceEquals) {
        int[] out = new int[a.length - k + 1];
        ArrayDeque<Integer> d = new ArrayDeque<>();
        for (int right = 0; right < a.length; right++) {
            if (right >= k && !d.isEmpty() && d.peekFirst() == a[right - k]) d.removeFirst();
            while (!d.isEmpty() && (replaceEquals ? d.peekLast() <= a[right] : d.peekLast() < a[right])) d.removeLast();
            d.addLast(a[right]);
            if (right >= k - 1) out[right - k + 1] = d.peekFirst();
        }
        return out;
    }

    public static void main(String[] args) {
        if (!Arrays.equals(maxSlidingWindow(new int[]{8, 3, 5, 9, 2, 7, 7, 1}, 3), new int[]{8, 9, 9, 9, 7, 7})) throw new AssertionError("example 1");
        if (!Arrays.equals(maxSlidingWindow(new int[]{1, 5, 2}, 3), new int[]{5})) throw new AssertionError("example 2");
        Random rnd = new Random(1344);
        boolean replaceFailed = false;
        for (int t = 0; t < 5000; t++) {
            int n = 1 + rnd.nextInt(16);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(5) - 2;
            int k = 1 + rnd.nextInt(n);
            int[] want = brute(a, k);
            if (!Arrays.equals(maxSlidingWindow(a, k), want)) throw new AssertionError("deque disagrees on " + Arrays.toString(a) + " k=" + k);
            if (!Arrays.equals(heap(a, k), want)) throw new AssertionError("heap disagrees on " + Arrays.toString(a));
            if (!Arrays.equals(valuesOnly(a, k, false), want)) throw new AssertionError("values-only with equals kept must work");
            if (!Arrays.equals(valuesOnly(a, k, true), want)) replaceFailed = true;
        }
        if (!replaceFailed) throw new AssertionError("values-only with replace-equals should fail somewhere");
    }
}
```
