<!-- solutions-for: 09-sliding-window -->
### Solutions For Fixed-Size Windows

#### Solution: [Build] Sums Of Every K-Block (Author exercise)
<!-- id: sw-block-sums -->

**Approach.**
The method adds the first `k` values to build the first running sum. Then it moves `right` across the remaining indexes. At each index it adds `nums[right]`, which enters the window, and subtracts `nums[right - k]`, which leaves it. The invariant is that, after each update, `sum` equals the total of `nums[right - k + 1 .. right]`, so the method stores it at index `right - k + 1` of the output.

**Complexity.**
- **Time** is O(n), because each index is added once and subtracted at most once.
- **Space** is O(1) beyond the output array, because the method keeps one running sum and two indexes.

```java run
import java.util.Random;

public final class BlockSums {
    /**
     * Returns the sum of every length-k block of nums.
     * Time: O(n), because each index enters the sum once and leaves it at most once.
     * Space: O(1) beyond the output, because only the running sum is stored.
     * Invariant: after each update, sum equals nums[right - k + 1 .. right].
     */
    static long[] blockSums(int[] nums, int k) {
        // Running sum of the current window, as long so large inputs cannot overflow.
        long sum = 0;
        // Fill loop: k additions build the first window.
        for (int right = 0; right < k; right++) sum += nums[right];
        // One output entry per window start, which is n - k + 1 entries.
        long[] out = new long[nums.length - k + 1];
        // The first window ends at index k - 1, so its total belongs at index 0.
        out[0] = sum;
        // Slide loop: each step moves the window one index to the right.
        for (int right = k; right < nums.length; right++) {
            // The value at right enters the window.
            sum += nums[right];
            // The value at right - k leaves the window.
            sum -= nums[right - k];
            // The window now starts at right - k + 1.
            out[right - k + 1] = sum;
        }
        // The caller receives all totals in order of the window start.
        return out;
    }

    /** Brute force oracle: adds k values for every start, in O(n * k). */
    static long[] oracle(int[] nums, int k) {
        long[] out = new long[nums.length - k + 1];
        for (int s = 0; s < out.length; s++) for (int i = s; i < s + k; i++) out[s] += nums[i];
        return out;
    }

    public static void main(String[] args) {
        // Example 1 from the problem statement.
        long[] ex = blockSums(new int[] {4, 2, 7, 1, 3, 5}, 3);
        if (!java.util.Arrays.equals(ex, new long[] {13, 10, 11, 9})) throw new AssertionError("example 1");
        // Example 2: k = 1 returns the values themselves.
        if (!java.util.Arrays.equals(blockSums(new int[] {-5, 5}, 1), new long[] {-5, 5})) throw new AssertionError("example 2");
        // Random inputs agree with the oracle, including k equal to the length.
        Random rnd = new Random(1);
        for (int t = 0; t < 2000; t++) {
            int n = 1 + rnd.nextInt(12), k = 1 + rnd.nextInt(n);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(21) - 10;
            int[] copy = a.clone();
            if (!java.util.Arrays.equals(blockSums(a, k), oracle(a, k))) throw new AssertionError("random " + t);
            // The method never mutates its input.
            if (!java.util.Arrays.equals(a, copy)) throw new AssertionError("mutation");
        }
    }
}
```

#### Solution: [Vary] Maximum Average Subarray I (LeetCode 643)
<!-- id: sw-max-average -->

**Approach.**
The averages of two blocks compare in the same order as their sums, because both blocks have the same size `k`. The method therefore keeps the largest integer sum and divides once at the end. The best sum starts as the first window's sum and not as 0, because a start of 0 beats every negative sum and returns a wrong maximum. The invariant is that `best` equals the largest total among the windows already visited.

**Complexity.**
- **Time** is O(n), because the method makes one pass with two updates per index.
- **Space** is O(1), because it stores a running sum and a best sum.

```java run
import java.util.Random;

public final class MaxAverage {
    /**
     * Returns the largest average over blocks of length exactly k.
     * Time: O(n), one pass with a constant update per index.
     * Space: O(1), two long variables.
     * Invariant: best is the largest window sum seen so far.
     */
    static double maxAverage(int[] nums, int k) {
        // Running sum of the first window.
        long sum = 0;
        for (int i = 0; i < k; i++) sum += nums[i];
        // The first window is the only candidate so far, so it is the best so far.
        long best = sum;
        // Slide loop: one entering value and one leaving value per step.
        for (int right = k; right < nums.length; right++) {
            // Update the sum by the two changed members.
            sum += nums[right] - nums[right - k];
            // Keep the larger total; comparing sums avoids a division per window.
            if (sum > best) best = sum;
        }
        // Divide once; the cast makes this a floating-point division.
        return (double) best / k;
    }

    /** Oracle: computes the average of every block directly. */
    static double oracle(int[] a, int k) {
        double best = -1e18;
        for (int s = 0; s + k <= a.length; s++) {
            long t = 0;
            for (int i = s; i < s + k; i++) t += a[i];
            best = Math.max(best, (double) t / k);
        }
        return best;
    }

    public static void main(String[] args) {
        // Example 1: the best block is [-2, 6] with average 2.0.
        if (Math.abs(maxAverage(new int[] {3, -1, 4, -2, 6}, 2) - 2.0) > 1e-9) throw new AssertionError("example 1");
        // Example 2: all sums are negative, and the best is -5.5.
        if (Math.abs(maxAverage(new int[] {-3, -8, -5}, 2) + 5.5) > 1e-9) throw new AssertionError("example 2");
        // Random inputs, including all-negative arrays, agree with the oracle.
        Random rnd = new Random(2);
        for (int t = 0; t < 2000; t++) {
            int n = 1 + rnd.nextInt(12), k = 1 + rnd.nextInt(n), lo = -20, hi = t % 2 == 0 ? -1 : 20;
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = lo + rnd.nextInt(hi - lo + 1);
            if (Math.abs(maxAverage(a, k) - oracle(a, k)) > 1e-9) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Boundary] Whole-Array Window (Author exercise)
<!-- id: sw-whole-array -->

**Approach.**
The method first checks the contract. A value of `k` below 1 or above `nums.length` makes the window impossible, so the method throws `IllegalArgumentException` and does not return an invented number. After the check, the first window covers indexes `0..k-1`. When `k == nums.length`, the slide loop does not run, and the first sum is the answer. The invariant of the loop is the same as before, and the check guarantees that the first fill never reads past the array.

**Complexity.**
- **Time** is O(n), because the method makes at most one fill pass and one slide pass.
- **Space** is O(1), because it keeps a running sum and a best sum.

```java run
import java.util.Random;

public final class WholeArrayWindow {
    /**
     * Returns the largest sum over blocks of length exactly k, or throws if k is illegal.
     * Time: O(n), a fill pass plus a slide pass.
     * Space: O(1), two long variables.
     * Invariant: sum equals the current window, and best the largest sum so far.
     */
    static long maxBlockSum(int[] nums, int k) {
        // The contract check comes first, so no later line reads outside the array.
        if (k < 1 || k > nums.length) throw new IllegalArgumentException("k out of range: " + k);
        // Fill loop builds the first window; it reads indexes 0..k-1 only.
        long sum = 0;
        for (int i = 0; i < k; i++) sum += nums[i];
        // With k == nums.length, this is the only window.
        long best = sum;
        // The slide loop body runs nums.length - k times, which is zero for a whole-array window.
        for (int right = k; right < nums.length; right++) {
            // Enter nums[right], leave nums[right - k].
            sum += nums[right] - nums[right - k];
            // Track the largest total seen.
            best = Math.max(best, sum);
        }
        // Return the best total.
        return best;
    }

    /** Oracle that tries every start. */
    static long oracle(int[] a, int k) {
        long best = Long.MIN_VALUE;
        for (int s = 0; s + k <= a.length; s++) {
            long t = 0;
            for (int i = s; i < s + k; i++) t += a[i];
            best = Math.max(best, t);
        }
        return best;
    }

    public static void main(String[] args) {
        // Example 1: a window equal to the whole array returns the whole sum.
        if (maxBlockSum(new int[] {2, -7, 4}, 3) != -1) throw new AssertionError("example 1");
        // Example 2: k above the length throws, and so do k = 0 and a negative k.
        for (int bad : new int[] {4, 0, -1}) {
            boolean threw = false;
            try { maxBlockSum(new int[] {2, -7, 4}, bad); } catch (IllegalArgumentException e) { threw = true; }
            if (!threw) throw new AssertionError("no exception for k = " + bad);
        }
        // Random legal inputs agree with the oracle.
        Random rnd = new Random(3);
        for (int t = 0; t < 2000; t++) {
            int n = 1 + rnd.nextInt(10), k = 1 + rnd.nextInt(n);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(41) - 30;
            if (maxBlockSum(a, k) != oracle(a, k)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Recognize] Maximum Number Of Vowels In A Substring Of Given Length (LeetCode 1456)
<!-- id: sw-max-vowels -->

**Approach.**
The window state is the number of vowels inside `s[left..right]`. A character that enters adds 1 when it is a vowel and 0 otherwise. A character that leaves subtracts the same amount. The method builds the first count over `s[0..k-1]`, slides across the rest of the string, and keeps the largest count. The method never creates a substring, because the indexes alone describe the window. The invariant is that `count` equals the number of vowels in the current window.

**Complexity.**
- **Time** is O(n), because each character enters once and leaves at most once, and the vowel test costs O(1).
- **Space** is O(1), because the method stores two integers.

```java run
import java.util.Random;

public final class MaxVowels {
    /** Contribution of one character to the count. */
    static int v(char c) { return "aeiou".indexOf(c) >= 0 ? 1 : 0; }

    /**
     * Returns the largest vowel count over substrings of length exactly k.
     * Time: O(n), one fill pass and one slide pass with a constant vowel test.
     * Space: O(1), two integers and no substring.
     * Invariant: count equals the number of vowels in s[right - k + 1 .. right].
     */
    static int maxVowels(String s, int k) {
        // Count of vowels in the first window.
        int count = 0;
        for (int i = 0; i < k; i++) count += v(s.charAt(i));
        // The first window is the best so far.
        int best = count;
        // Slide loop: one entering character and one leaving character per step.
        for (int right = k; right < s.length(); right++) {
            // Entering character adds 1 or 0; leaving character subtracts 1 or 0.
            count += v(s.charAt(right)) - v(s.charAt(right - k));
            // Keep the larger count.
            if (count > best) best = count;
        }
        // Return the largest count.
        return best;
    }

    /** Oracle: counts the vowels of every substring directly with substring(). */
    static int oracle(String s, int k) {
        int best = 0;
        for (int st = 0; st + k <= s.length(); st++) {
            int c = 0;
            for (char ch : s.substring(st, st + k).toCharArray()) c += v(ch);
            best = Math.max(best, c);
        }
        return best;
    }

    public static void main(String[] args) {
        // Example 1: the substring "iii" holds three vowels.
        if (maxVowels("abciiidef", 3) != 3) throw new AssertionError("example 1");
        // Example 2: a string with no vowel returns 0.
        if (maxVowels("rhythm", 2) != 0) throw new AssertionError("example 2");
        // Random strings over a small alphabet agree with the oracle.
        Random rnd = new Random(4);
        String alpha = "abeiz";
        for (int t = 0; t < 2000; t++) {
            int n = 1 + rnd.nextInt(14), k = 1 + rnd.nextInt(n);
            StringBuilder sb = new StringBuilder();
            for (int i = 0; i < n; i++) sb.append(alpha.charAt(rnd.nextInt(alpha.length())));
            if (maxVowels(sb.toString(), k) != oracle(sb.toString(), k)) throw new AssertionError("random " + t);
        }
    }
}
```
