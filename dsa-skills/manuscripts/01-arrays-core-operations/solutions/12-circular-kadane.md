<!-- solutions-for: 12-circular-kadane -->
### Circular Kadane

#### Solution: [Build] Maximum Sum Circular Subarray (LeetCode 918)
<!-- id: ar-maximum-circular-subarray -->

**Approach.** One pass keeps the total and the extend-or-restart states for both the maximum and the minimum straight stretch. A wrapping stretch is the total minus an excluded straight block, so the best wrap is the total minus the minimum straight block. The answer is the larger of that and the ordinary maximum, except that an all-negative array returns the ordinary maximum, because the wrap candidate would then be the empty stretch. The assertions compare with the enumeration over every start and length on random rings, including all-negative ones.

**Complexity.** O(n) time and O(1) extra space.

```java run
import java.util.Random;

public final class MaximumCircularSubarray {
    static int maxCircular(int[] nums) {
        int total = nums[0];
        int maxEnd = nums[0], maxBest = nums[0];
        int minEnd = nums[0], minBest = nums[0];
        for (int i = 1; i < nums.length; i++) {
            int x = nums[i];
            total += x;
            maxEnd = Math.max(x, maxEnd + x);
            maxBest = Math.max(maxBest, maxEnd);
            minEnd = Math.min(x, minEnd + x);
            minBest = Math.min(minBest, minEnd);
        }
        if (maxBest < 0) return maxBest;
        return Math.max(maxBest, total - minBest);
    }
    static int oracle(int[] nums) {
        int n = nums.length, best = Integer.MIN_VALUE;
        for (int s = 0; s < n; s++) {
            int sum = 0;
            for (int len = 1; len <= n; len++) { sum += nums[(s + len - 1) % n]; best = Math.max(best, sum); }
        }
        return best;
    }

    public static void main(String[] args) {
        if (maxCircular(new int[] {4, -5, 3, -1, 4}) != 10) throw new AssertionError("example 1");
        if (maxCircular(new int[] {2, -1, 2, -6, 1}) != 4) throw new AssertionError("example 2");
        Random rnd = new Random(81);
        for (int t = 0; t < 6000; t++) {
            int[] a = new int[1 + rnd.nextInt(10)];
            int shift = rnd.nextInt(3) == 0 ? 8 : 0;           // sometimes force mostly negative arrays
            for (int i = 0; i < a.length; i++) a[i] = rnd.nextInt(21) - 10 - shift;
            if (maxCircular(a) != oracle(a)) throw new AssertionError("disagrees with enumeration");
        }
    }
}
```

#### Solution: [Vary] Circular Minimum (Author exercise)
<!-- id: ar-circular-minimum -->

**Approach.** The mirror argument: a wrapping minimum is the total minus the largest straight block. The block cannot be the whole array, because then the remainder is empty. That happens exactly when the ordinary maximum equals the total and is positive, as for an all-positive array, where the answer is the ordinary minimum. Otherwise the answer is the smaller of the ordinary minimum and the total minus the ordinary maximum. The assertions compare with the enumeration over every start and length on random rings.

**Complexity.** O(n) time and O(1) extra space.

```java run
import java.util.Random;

public final class CircularMinimum {
    static int minCircular(int[] nums) {
        int total = nums[0];
        int maxEnd = nums[0], maxBest = nums[0];
        int minEnd = nums[0], minBest = nums[0];
        for (int i = 1; i < nums.length; i++) {
            int x = nums[i];
            total += x;
            maxEnd = Math.max(x, maxEnd + x);
            maxBest = Math.max(maxBest, maxEnd);
            minEnd = Math.min(x, minEnd + x);
            minBest = Math.min(minBest, minEnd);
        }
        if (maxBest == total && maxBest > 0) return minBest;
        if (maxBest == total) return Math.min(minBest, total - maxBest);
        return Math.min(minBest, total - maxBest);
    }
    static int oracle(int[] nums) {
        int n = nums.length, best = Integer.MAX_VALUE;
        for (int s = 0; s < n; s++) {
            int sum = 0;
            for (int len = 1; len <= n; len++) { sum += nums[(s + len - 1) % n]; best = Math.min(best, sum); }
        }
        return best;
    }

    public static void main(String[] args) {
        if (minCircular(new int[] {-5, 2, 3, -4}) != -9) throw new AssertionError("example 1");
        if (minCircular(new int[] {3, 1, 2}) != 1) throw new AssertionError("example 2");
        Random rnd = new Random(82);
        for (int t = 0; t < 6000; t++) {
            int[] a = new int[1 + rnd.nextInt(10)];
            int shift = rnd.nextInt(3) == 0 ? 8 : 0;
            for (int i = 0; i < a.length; i++) a[i] = rnd.nextInt(21) - 10 + shift;
            if (minCircular(a) != oracle(a)) throw new AssertionError("disagrees with enumeration");
        }
    }
}
```

#### Solution: [Boundary] All Negative (Author exercise)
<!-- id: ar-circular-all-negative -->

**Approach.** When every value is negative, the smallest straight block is the whole array, so the total minus that block is zero, which describes an empty stretch. The unguarded formula would therefore return zero, a value no non-empty stretch can reach. The guard returns the ordinary maximum, the largest single element, whenever that maximum is negative. The assertions compute the unguarded answer to show the wrong zero, then the guarded one, then compare the guarded one with the largest element on random all-negative arrays.

**Complexity.** O(n) time and O(1) extra space.

```java run
import java.util.Random;

public final class CircularAllNegative {
    static int unguarded(int[] nums) {
        int total = nums[0], maxEnd = nums[0], maxBest = nums[0], minEnd = nums[0], minBest = nums[0];
        for (int i = 1; i < nums.length; i++) {
            int x = nums[i];
            total += x;
            maxEnd = Math.max(x, maxEnd + x); maxBest = Math.max(maxBest, maxEnd);
            minEnd = Math.min(x, minEnd + x); minBest = Math.min(minBest, minEnd);
        }
        return Math.max(maxBest, total - minBest);
    }
    static int guarded(int[] nums) {
        int total = nums[0], maxEnd = nums[0], maxBest = nums[0], minEnd = nums[0], minBest = nums[0];
        for (int i = 1; i < nums.length; i++) {
            int x = nums[i];
            total += x;
            maxEnd = Math.max(x, maxEnd + x); maxBest = Math.max(maxBest, maxEnd);
            minEnd = Math.min(x, minEnd + x); minBest = Math.min(minBest, minEnd);
        }
        if (maxBest < 0) return maxBest;
        return Math.max(maxBest, total - minBest);
    }

    public static void main(String[] args) {
        if (unguarded(new int[] {-3, -2, -3}) != 0) throw new AssertionError("the wrap candidate is an empty stretch worth zero");
        if (guarded(new int[] {-3, -2, -3}) != -2) throw new AssertionError("example 1");
        if (guarded(new int[] {-7}) != -7) throw new AssertionError("example 2");
        Random rnd = new Random(83);
        for (int t = 0; t < 3000; t++) {
            int[] a = new int[1 + rnd.nextInt(10)];
            int max = Integer.MIN_VALUE;
            for (int i = 0; i < a.length; i++) { a[i] = -1 - rnd.nextInt(40); max = Math.max(max, a[i]); }
            if (guarded(a) != max) throw new AssertionError("the answer must be the largest element");
        }
    }
}
```

#### Solution: [Recognize] Circular Maximum With A Proof (LeetCode 918)
<!-- id: ar-circular-proof -->

**Approach.** The proof in two sentences: a wrapping stretch starting at index `s` with length `len` greater than `n - s` covers the indices from `s` to the end and from zero to `s + len - n - 1`, so the indices left out run from `s + len - n` up to `s - 1`, one contiguous block. That block is non-empty when `len < n` and it cannot touch index 0 or the last index, because the stretch covers both ends. So the wrapping sum is the total minus one straight middle block, and the maximum over all wraps is the total minus the minimum straight block. The code implements the formula. The assertions verify the structural claim on every wrapping choice of random rings, and also compare the formula with enumeration.

**Complexity.** O(n) time and O(1) extra space for the method, and O(n^2) for the checking harness.

```java run
import java.util.Random;

public final class CircularProof {
    static int maxCircular(int[] nums) {
        int total = nums[0], maxEnd = nums[0], maxBest = nums[0], minEnd = nums[0], minBest = nums[0];
        for (int i = 1; i < nums.length; i++) {
            int x = nums[i];
            total += x;
            maxEnd = Math.max(x, maxEnd + x); maxBest = Math.max(maxBest, maxEnd);
            minEnd = Math.min(x, minEnd + x); minBest = Math.min(minBest, minEnd);
        }
        if (maxBest < 0) return maxBest;
        return Math.max(maxBest, total - minBest);
    }
    static int oracle(int[] nums) {
        int n = nums.length, best = Integer.MIN_VALUE;
        for (int s = 0; s < n; s++) {
            int sum = 0;
            for (int len = 1; len <= n; len++) { sum += nums[(s + len - 1) % n]; best = Math.max(best, sum); }
        }
        return best;
    }

    public static void main(String[] args) {
        if (maxCircular(new int[] {7, -3, -4, 6}) != 13) throw new AssertionError("example 1");
        if (maxCircular(new int[] {-1, -2}) != -1) throw new AssertionError("example 2");
        Random rnd = new Random(84);
        for (int t = 0; t < 3000; t++) {
            int n = 2 + rnd.nextInt(9);
            int[] a = new int[n];
            int total = 0;
            for (int i = 0; i < n; i++) { a[i] = rnd.nextInt(21) - 10; total += a[i]; }
            for (int s = 0; s < n; s++) {
                for (int len = 1; len < n; len++) {
                    if (s + len <= n) continue;                       // straight choice, not a wrap
                    boolean[] covered = new boolean[n];
                    int sum = 0;
                    for (int k = 0; k < len; k++) { covered[(s + k) % n] = true; sum += a[(s + k) % n]; }
                    int first = -1, last = -1, count = 0;
                    for (int i = 0; i < n; i++) if (!covered[i]) { if (first < 0) first = i; last = i; count++; }
                    if (count != n - len) throw new AssertionError("excluded count");
                    if (last - first + 1 != count) throw new AssertionError("excluded indices must be one block");
                    if (first == 0 || last == n - 1) throw new AssertionError("excluded block must be strictly inside");
                    int excluded = 0;
                    for (int i = first; i <= last; i++) excluded += a[i];
                    if (sum != total - excluded) throw new AssertionError("wrap sum equals total minus excluded block");
                }
            }
            if (maxCircular(a) != oracle(a)) throw new AssertionError("disagrees with enumeration");
        }
    }
}
```
