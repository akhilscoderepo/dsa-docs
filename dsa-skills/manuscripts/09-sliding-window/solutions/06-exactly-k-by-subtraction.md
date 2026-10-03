<!-- solutions-for: 09-exactly-k-by-subtraction -->
### Exactly-K By Subtraction

#### Solution: [Build] Exactly One Odd Number (Author exercise)
<!-- id: sw-exactly-one-odd -->

**Approach.** Write one helper that counts the subarrays holding at most a given number of odd values, using a window whose left edge only moves right, and adding `right - left + 1` for each right edge. The answer is the helper at limit one minus the helper at limit zero, since the subarrays with at most one odd value split into those with none and those with exactly one. The check compares with a cubic scan on random arrays that include negative odd values, asserts that the input is not changed, and runs an array of one hundred thousand even numbers to show that the count of subarrays needs `long`, because it exceeds the largest `int`.

**Complexity.** Two passes, each moving each edge at most n times, so O(n) time and O(1) extra space.

```java run
import java.util.Arrays;
import java.util.Random;

public final class ExactlyOneOdd {
    static long atMost(int[] a, int limit) {
        long total = 0;
        int left = 0, odd = 0;
        for (int right = 0; right < a.length; right++) {
            odd += a[right] & 1;
            while (odd > limit) odd -= a[left++] & 1;
            total += right - left + 1;
        }
        return total;
    }

    static long exactlyOne(int[] a) {
        return atMost(a, 1) - atMost(a, 0);
    }

    static long brute(int[] a) {
        long c = 0;
        for (int s = 0; s < a.length; s++) {
            int odd = 0;
            for (int e = s; e < a.length; e++) {
                if (a[e] % 2 != 0) odd++;
                if (odd == 1) c++;
            }
        }
        return c;
    }

    public static void main(String[] args) {
        if (exactlyOne(new int[] {2, 3, 4, 6, 5}) != 9) throw new AssertionError("example 1");
        if (exactlyOne(new int[] {8, 8, 8}) != 0) throw new AssertionError("example 2");
        if (exactlyOne(new int[0]) != 0) throw new AssertionError("empty");
        if (exactlyOne(new int[] {-3}) != 1) throw new AssertionError("negative odd");
        int[] evens = new int[100000];
        Arrays.fill(evens, 2);
        long all = atMost(evens, 0);
        if (all != 100000L * 100001L / 2) throw new AssertionError("long total");
        if (all <= Integer.MAX_VALUE) throw new AssertionError("should exceed int");
        Random rnd = new Random(911);
        for (int t = 0; t < 3000; t++) {
            int n = rnd.nextInt(13);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(7) - 3;
            int[] copy = a.clone();
            if (exactlyOne(a) != brute(a)) throw new AssertionError("differs on " + Arrays.toString(a));
            if (!Arrays.equals(a, copy)) throw new AssertionError("input changed");
        }
    }
}
```

#### Solution: [Vary] Count Number of Nice Subarrays (LeetCode 1248)
<!-- id: sw-nice-subarrays -->

**Approach.** Pass the limit as a parameter. The helper keeps `odd` as the number of odd values inside the window and shrinks while it is above the limit, subtracting one for each odd value that leaves. The number of nice subarrays is the helper at `k` minus the helper at `k - 1`. The check compares with a brute force on random positive arrays for every k from one up to the length, counts the left and right moves in both passes to show that each edge moves at most n times per pass, and checks both examples.

**Complexity.** Each pass moves `right` n times and `left` at most n times, so the total is at most 4n edge moves, with O(1) extra space.

```java run
import java.util.Random;
import java.util.Arrays;

public final class NiceSubarrays {
    static int moves;

    static long upTo(int[] nums, int limit) {
        long sum = 0;
        int lo = 0, odds = 0;
        for (int hi = 0; hi < nums.length; hi++) {
            moves++;
            odds += nums[hi] % 2;
            while (odds > limit) {
                odds -= nums[lo] % 2;
                lo++;
                moves++;
            }
            sum += hi - lo + 1;
        }
        return sum;
    }

    static long nice(int[] nums, int k) {
        return upTo(nums, k) - upTo(nums, k - 1);
    }

    static long brute(int[] a, int k) {
        long c = 0;
        for (int s = 0; s < a.length; s++)
            for (int e = s; e < a.length; e++) {
                int odd = 0;
                for (int i = s; i <= e; i++) odd += a[i] % 2;
                if (odd == k) c++;
            }
        return c;
    }

    public static void main(String[] args) {
        if (nice(new int[] {1, 2, 2, 1, 3, 2}, 2) != 7) throw new AssertionError("example 1");
        if (nice(new int[] {4, 6, 8}, 1) != 0) throw new AssertionError("example 2");
        if (nice(new int[] {5}, 1) != 1) throw new AssertionError("single odd");
        Random rnd = new Random(912);
        for (int t = 0; t < 2500; t++) {
            int n = 1 + rnd.nextInt(11);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = 1 + rnd.nextInt(6);
            for (int k = 1; k <= n; k++) {
                moves = 0;
                long got = nice(a, k);
                if (got != brute(a, k)) throw new AssertionError("differs on " + Arrays.toString(a) + " k " + k);
                if (moves > 4 * n) throw new AssertionError("too many moves " + moves);
            }
        }
    }
}
```

#### Solution: [Boundary] Empty At-Most Budget (Author exercise)
<!-- id: sw-empty-budget -->

**Approach.** The identity needs the at-most count for `k - 1`, which for k equal to zero is a limit of minus one. No subarray has a negative number of odd values, so the true count is zero, and the helper returns it before the loop starts. Without that guard, the shrink loop would keep running because the odd count, even when zero, is above minus one, and `left` would move past the end of the array. The check runs the unguarded loop on a nonempty array and expects an `ArrayIndexOutOfBoundsException`, then compares the guarded version with a brute force for k from zero to six on random arrays, including empty and all-even arrays.

**Complexity.** Two linear passes, so O(n) time and constant extra space, and the guarded call adds no work at all.

```java run
import java.util.Arrays;
import java.util.Random;

public final class EmptyBudget {
    static long guarded(int[] a, int limit) {
        if (limit < 0) return 0;
        return loop(a, limit);
    }

    static long loop(int[] a, int limit) {
        long total = 0;
        int left = 0, odd = 0;
        for (int right = 0; right < a.length; right++) {
            odd += a[right] & 1;
            while (odd > limit) odd -= a[left++] & 1;
            total += right - left + 1;
        }
        return total;
    }

    static long exactly(int[] a, int k) {
        return guarded(a, k) - guarded(a, k - 1);
    }

    static long brute(int[] a, int k) {
        long c = 0;
        for (int s = 0; s < a.length; s++) {
            int odd = 0;
            for (int e = s; e < a.length; e++) {
                odd += a[e] & 1;
                if (odd == k) c++;
            }
        }
        return c;
    }

    public static void main(String[] args) {
        if (exactly(new int[] {2, 4, 1, 6}, 0) != 4) throw new AssertionError("example 1");
        if (exactly(new int[] {1, 1}, 3) != 0) throw new AssertionError("example 2");
        if (guarded(new int[] {1, 2, 3}, -1) != 0) throw new AssertionError("minus one is zero");
        boolean threw = false;
        try {
            loop(new int[] {2}, -1);
        } catch (ArrayIndexOutOfBoundsException expected) {
            threw = true;
        }
        if (!threw) throw new AssertionError("unguarded loop should run off the array");
        if (exactly(new int[0], 0) != 0) throw new AssertionError("empty");
        if (exactly(new int[] {8, 8, 8, 8}, 0) != 10) throw new AssertionError("all even");
        Random rnd = new Random(913);
        for (int t = 0; t < 3000; t++) {
            int n = rnd.nextInt(13);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(9) - 4;
            for (int k = 0; k <= 6; k++) {
                if (exactly(a, k) != brute(a, k)) throw new AssertionError("differs on " + Arrays.toString(a) + " k " + k);
            }
        }
    }
}
```

#### Solution: [Recognize] Subarrays with K Different Integers (LeetCode 992)
<!-- id: sw-k-different-integers -->

**Approach.** The property is now the number of different values. Build the helper around a map from value to count, shrink while the map holds more keys than the limit, delete a key the moment its count reaches zero, and add `right - left + 1` for each right edge. The answer is the helper at `k` minus the helper at `k - 1`. The check compares with a brute force that builds a set for every subarray, asserts that the map size equals the number of different values in the window at every step, which fails if a zero count is left behind, and checks both examples.

**Complexity.** Two passes with at most 2n map updates each, so expected O(n) time and O(k) extra space.

```java run
import java.util.*;

public final class KDifferent {
    static long upTo(int[] a, int limit) {
        long total = 0;
        Map<Integer, Integer> counts = new HashMap<>();
        int left = 0;
        for (int right = 0; right < a.length; right++) {
            counts.merge(a[right], 1, Integer::sum);
            while (counts.size() > limit) {
                int v = a[left++];
                if (counts.merge(v, -1, Integer::sum) == 0) counts.remove(v);
            }
            Set<Integer> real = new HashSet<>();
            for (int i = left; i <= right; i++) real.add(a[i]);
            if (real.size() != counts.size()) throw new AssertionError("size drifted");
            total += right - left + 1;
        }
        return total;
    }

    static long exactly(int[] a, int k) {
        return upTo(a, k) - upTo(a, k - 1);
    }

    static long brute(int[] a, int k) {
        long c = 0;
        for (int s = 0; s < a.length; s++)
            for (int e = s; e < a.length; e++) {
                Set<Integer> kinds = new HashSet<>();
                for (int i = s; i <= e; i++) kinds.add(a[i]);
                if (kinds.size() == k) c++;
            }
        return c;
    }

    public static void main(String[] args) {
        if (exactly(new int[] {3, 1, 3, 2, 2}, 2) != 5) throw new AssertionError("example 1");
        if (exactly(new int[] {5, 5, 5}, 2) != 0) throw new AssertionError("example 2");
        if (exactly(new int[] {7}, 1) != 1) throw new AssertionError("single");
        if (exactly(new int[] {4, 4, 4}, 1) != 6) throw new AssertionError("all equal");
        Random rnd = new Random(914);
        for (int t = 0; t < 2500; t++) {
            int n = 1 + rnd.nextInt(11);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = 1 + rnd.nextInt(Math.min(n, 4));
            for (int k = 1; k <= n; k++) {
                if (exactly(a, k) != brute(a, k)) throw new AssertionError("differs on " + Arrays.toString(a) + " k " + k);
            }
        }
    }
}
```
