<!-- solutions-for: 28-dynamic-programming-state-machines-and-sequences -->
### Solutions For Increasing Subsequences

#### Solution: [Build] LIS Ending At I (Author exercise)
<!-- id: is-ending-at-i -->

**Approach.**
Entry `dp[i]` is the length of the longest strictly increasing subsequence whose last element is `nums[i]`. Each entry starts at 1, because the element alone is a valid subsequence. The inner loop then visits every earlier index `j`. When `nums[j]` is smaller than `nums[i]`, any subsequence that ends at `j` can take `nums[i]` as its next element, so the candidate is `dp[j] + 1`. The entry keeps the largest candidate.

The invariant is that every entry below `i` is final when index `i` starts, so each candidate reads a finished value. Equal values give no candidate, which enforces the strict rule. The test compares every entry with a subset enumeration on random arrays.

**Complexity.**
- **Time** is O(n^2), because index `i` compares with `i` earlier indexes and the sum of those counts is about n^2 / 2.
- **Space** is O(n) for the result array, and the input array stays unchanged.

```java run
import java.util.*;

public final class IsEndingAtI {
    /**
     * Returns, for each index, the longest strictly increasing subsequence length that ends there.
     * Time: O(n^2). Space: O(n).
     * Invariant: dp[0..i-1] are final when index i is computed.
     */
    static int[] endingAt(int[] nums) {
        // One entry per index, so memory is O(n).
        int[] dp = new int[nums.length];
        for (int i = 0; i < nums.length; i++) {
            // The element alone is a subsequence of length 1.
            dp[i] = 1;
            // Every earlier index is a possible previous element, so this loop costs O(i).
            for (int j = 0; j < i; j++) {
                // Only a strictly smaller earlier value can extend, so equal values never count.
                if (nums[j] < nums[i] && dp[j] + 1 > dp[i]) dp[i] = dp[j] + 1;
            }
        }
        // The finished table is the result.
        return dp;
    }

    /** Oracle: the longest strictly increasing subsequence ending at index i, by subset enumeration. */
    static int oracle(int[] a, int end) {
        int best = 0;
        // Each mask selects the earlier elements to keep, and the element at end is always last.
        for (int mask = 0; mask < (1 << end); mask++) {
            int prev = Integer.MIN_VALUE;
            boolean first = true;
            int len = 0;
            boolean ok = true;
            for (int k = 0; k < end && ok; k++) {
                if ((mask >> k & 1) == 0) continue;
                if (!first && a[k] <= prev) ok = false;
                prev = a[k];
                first = false;
                len++;
            }
            if (ok && (first || prev < a[end])) best = Math.max(best, len + 1);
        }
        return best;
    }

    public static void main(String[] args) {
        // The worked examples.
        if (!Arrays.equals(endingAt(new int[] {3, 1, 4, 1, 5, 9, 2, 6}), new int[] {1, 1, 2, 1, 3, 4, 2, 4})) throw new AssertionError("ex1");
        if (!Arrays.equals(endingAt(new int[] {4, 4, 4}), new int[] {1, 1, 1})) throw new AssertionError("ex2");
        // The empty array gives an empty result.
        if (endingAt(new int[0]).length != 0) throw new AssertionError("empty");
        // The input array stays unchanged.
        int[] in = {2, 1, 3};
        endingAt(in);
        if (!Arrays.equals(in, new int[] {2, 1, 3})) throw new AssertionError("mutated");
        // Random arrays against the subset oracle.
        Random rnd = new Random(2803);
        for (int t = 0; t < 2000; t++) {
            int n = rnd.nextInt(11);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(8) - 3;
            int[] got = endingAt(a);
            for (int i = 0; i < n; i++) {
                if (got[i] != oracle(a, i)) throw new AssertionError("random " + t + " index " + i);
            }
        }
    }
}
```

#### Solution: [Vary] Longest Increasing Subsequence (LeetCode 300)
<!-- id: is-quadratic-length -->

**Approach.**
The answer is the largest entry of the table from the previous exercise, because the best subsequence can end at any index. The method fills `dp[i]` with 1 plus the largest `dp[j]` over earlier indexes `j` that hold a smaller value, and it keeps a running maximum. An empty array never enters the loop, so the maximum stays 0.

The invariant is that `best` always equals the largest finished entry among indexes below the current one. A strictly increasing subsequence has distinct values in rising order, so an equal value never extends, and an array of equal values gives 1. The test checks the result against subset enumeration.

**Complexity.**
- **Time** is O(n^2), because the two nested loops compare every pair of indexes once.
- **Space** is O(n) for the table, and the input array stays unchanged.

```java run
import java.util.*;

public final class IsQuadraticLength {
    /**
     * Returns the length of the longest strictly increasing subsequence.
     * Time: O(n^2). Space: O(n).
     * Invariant: best is the maximum of the finished entries dp[0..i-1].
     */
    static int lis(int[] nums) {
        // One entry per index.
        int[] dp = new int[nums.length];
        // An empty array keeps best at 0.
        int best = 0;
        for (int i = 0; i < nums.length; i++) {
            // The element alone has length 1.
            dp[i] = 1;
            // Compare with every earlier index, which costs O(i).
            for (int j = 0; j < i; j++) {
                // A strictly smaller earlier value can be extended by nums[i].
                if (nums[j] < nums[i] && dp[j] + 1 > dp[i]) dp[i] = dp[j] + 1;
            }
            // The best subsequence may end at any index, so keep the maximum.
            best = Math.max(best, dp[i]);
        }
        return best;
    }

    /** Oracle: tries every subset of indexes. */
    static int oracle(int[] a) {
        int n = a.length;
        int best = 0;
        for (int mask = 0; mask < (1 << n); mask++) {
            int prev = Integer.MIN_VALUE;
            int len = 0;
            boolean ok = true;
            for (int k = 0; k < n && ok; k++) {
                if ((mask >> k & 1) == 0) continue;
                if (len > 0 && a[k] <= prev) ok = false;
                prev = a[k];
                len++;
            }
            if (ok) best = Math.max(best, len);
        }
        return best;
    }

    public static void main(String[] args) {
        // The worked examples.
        if (lis(new int[] {0, 8, 4, 12, 2, 10, 6, 14}) != 4) throw new AssertionError("ex1");
        if (lis(new int[] {7, 7, 7, 7}) != 1) throw new AssertionError("ex2");
        // The opening readings: the adjacent-run count is 2 while the true answer is 4.
        if (lis(new int[] {5, 1, 6, 2, 7, 3, 8}) != 4) throw new AssertionError("readings");
        // Empty and decreasing arrays.
        if (lis(new int[0]) != 0) throw new AssertionError("empty");
        if (lis(new int[] {5, 4, 3}) != 1) throw new AssertionError("decreasing");
        // The input array stays unchanged.
        int[] in = {2, 1, 3};
        lis(in);
        if (!Arrays.equals(in, new int[] {2, 1, 3})) throw new AssertionError("mutated");
        // Random arrays against the subset oracle.
        Random rnd = new Random(2804);
        for (int t = 0; t < 3000; t++) {
            int n = rnd.nextInt(13);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(10) - 4;
            if (lis(a) != oracle(a)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Boundary] Duplicates (Author exercise)
<!-- id: is-duplicates -->

**Approach.**
The method keeps two sorted arrays of tails, one for each rule. For the strict rule, each value `x` goes to the lower bound, which is the first position whose tail is at least `x`. An equal tail sits at that position, so the value replaces it and the size does not grow. For the non-decreasing rule, each value goes to the upper bound, which is the first position whose tail is larger than `x`. An equal tail stays, and the value lands after it, so the size grows.

The invariant is that each array is sorted and `tails[L - 1]` is the smallest possible last element for length `L` under its rule. The search is a binary search over the used part of the array. The test compares both lengths with subset enumeration, including arrays with many equal values.

**Complexity.**
- **Time** is O(n log n), because each element costs two binary searches over at most n entries.
- **Space** is O(n) for the two tail arrays, and the input array stays unchanged.

```java run
import java.util.*;

public final class IsDuplicates {
    /**
     * Returns {strict length, non-decreasing length} of the longest subsequences.
     * Time: O(n log n). Space: O(n).
     * Invariant: each tails array is sorted and holds the smallest last element for every length.
     */
    static int[] lengths(int[] nums) {
        // Two tail arrays, one for each comparison rule.
        int[] strict = new int[nums.length];
        int[] loose = new int[nums.length];
        int sizeStrict = 0;
        int sizeLoose = 0;
        for (int x : nums) {
            // Lower bound: first tail >= x, so an equal tail is replaced.
            int lo = 0;
            int hi = sizeStrict;
            // Each search halves the range, so it costs O(log n).
            while (lo < hi) {
                int mid = (lo + hi) >>> 1;
                if (strict[mid] < x) lo = mid + 1;
                else hi = mid;
            }
            strict[lo] = x;
            // Appending at the end is the only way the strict length grows.
            if (lo == sizeStrict) sizeStrict++;
            // Upper bound: first tail > x, so an equal tail stays and the value lands after it.
            lo = 0;
            hi = sizeLoose;
            while (lo < hi) {
                int mid = (lo + hi) >>> 1;
                if (loose[mid] <= x) lo = mid + 1;
                else hi = mid;
            }
            loose[lo] = x;
            if (lo == sizeLoose) sizeLoose++;
        }
        return new int[] {sizeStrict, sizeLoose};
    }

    /** Oracle: tries every subset, with a flag for the strict rule. */
    static int oracle(int[] a, boolean strict) {
        int n = a.length;
        int best = 0;
        for (int mask = 0; mask < (1 << n); mask++) {
            int prev = 0;
            int len = 0;
            boolean ok = true;
            for (int k = 0; k < n && ok; k++) {
                if ((mask >> k & 1) == 0) continue;
                if (len > 0 && (strict ? a[k] <= prev : a[k] < prev)) ok = false;
                prev = a[k];
                len++;
            }
            if (ok) best = Math.max(best, len);
        }
        return best;
    }

    public static void main(String[] args) {
        // The worked examples.
        if (!Arrays.equals(lengths(new int[] {2, 2, 3, 3, 1, 3}), new int[] {2, 5})) throw new AssertionError("ex1");
        if (!Arrays.equals(lengths(new int[] {5, 4, 3}), new int[] {1, 1})) throw new AssertionError("ex2");
        // Empty input and all-equal input.
        if (!Arrays.equals(lengths(new int[0]), new int[] {0, 0})) throw new AssertionError("empty");
        if (!Arrays.equals(lengths(new int[] {7, 7, 7}), new int[] {1, 3})) throw new AssertionError("equal");
        // The input array stays unchanged.
        int[] in = {2, 2, 1};
        lengths(in);
        if (!Arrays.equals(in, new int[] {2, 2, 1})) throw new AssertionError("mutated");
        // Random arrays with a small value range, so equal values are common.
        Random rnd = new Random(2805);
        for (int t = 0; t < 3000; t++) {
            int n = rnd.nextInt(13);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(5) - 2;
            int[] got = lengths(a);
            if (got[0] != oracle(a, true) || got[1] != oracle(a, false)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Recognize] Prefix Lengths In O(n log n) (LeetCode 300)
<!-- id: is-prefix-lengths -->

**Approach.**
With n up to 200,000 the quadratic table needs about 2 * 10^10 comparisons, so the method keeps the sorted smallest tails. For each value `x`, a binary search finds the lower bound among the used entries. The value replaces the tail there, or it extends the array when every tail is smaller. After each element, the number of used entries is the longest strictly increasing subsequence length of that prefix, and the method stores it in the result.

The invariant is that after element `k`, the array holds the smallest possible last element for every length in the first `k + 1` elements. The array itself is not a subsequence of the input, only its size is used. The test compares every prefix length with subset enumeration.

**Complexity.**
- **Time** is O(n log n), because each element needs one binary search over at most n entries.
- **Space** is O(n) for the tails and the result, and the input array stays unchanged.

```java run
import java.util.*;

public final class IsPrefixLengths {
    /**
     * Returns the longest strictly increasing subsequence length for every prefix.
     * Time: O(n log n). Space: O(n).
     * Invariant: after element k, tails[L-1] is the smallest last element for length L in the prefix.
     */
    static int[] prefixLengths(int[] nums) {
        int[] tails = new int[nums.length];
        int[] result = new int[nums.length];
        int size = 0;
        for (int i = 0; i < nums.length; i++) {
            int x = nums[i];
            int lo = 0;
            int hi = size;
            // Binary search for the first tail >= x, which costs O(log n).
            while (lo < hi) {
                int mid = (lo + hi) >>> 1;
                if (tails[mid] < x) lo = mid + 1;
                else hi = mid;
            }
            // Replace the tail, or extend when every tail is smaller.
            tails[lo] = x;
            if (lo == size) size++;
            // The size is the answer for this prefix.
            result[i] = size;
        }
        return result;
    }

    /** Oracle: tries every subset of the first k elements. */
    static int oracle(int[] a, int k) {
        int best = 0;
        for (int mask = 0; mask < (1 << k); mask++) {
            int prev = 0;
            int len = 0;
            boolean ok = true;
            for (int p = 0; p < k && ok; p++) {
                if ((mask >> p & 1) == 0) continue;
                if (len > 0 && a[p] <= prev) ok = false;
                prev = a[p];
                len++;
            }
            if (ok) best = Math.max(best, len);
        }
        return best;
    }

    public static void main(String[] args) {
        // The worked examples.
        if (!Arrays.equals(prefixLengths(new int[] {3, 1, 2, 1, 5, 4, 6}), new int[] {1, 1, 2, 2, 3, 3, 4})) throw new AssertionError("ex1");
        if (!Arrays.equals(prefixLengths(new int[] {5, 4, 3, 2}), new int[] {1, 1, 1, 1})) throw new AssertionError("ex2");
        // The empty array gives an empty result.
        if (prefixLengths(new int[0]).length != 0) throw new AssertionError("empty");
        // The input array stays unchanged.
        int[] in = {2, 1, 3};
        prefixLengths(in);
        if (!Arrays.equals(in, new int[] {2, 1, 3})) throw new AssertionError("mutated");
        // A large sorted input finishes quickly and ends at length n.
        int[] big = new int[200000];
        for (int i = 0; i < big.length; i++) big[i] = i - 100000;
        if (prefixLengths(big)[big.length - 1] != big.length) throw new AssertionError("large");
        // Random arrays against the subset oracle.
        Random rnd = new Random(2806);
        for (int t = 0; t < 2000; t++) {
            int n = rnd.nextInt(12);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(10) - 4;
            int[] got = prefixLengths(a);
            for (int k = 1; k <= n; k++) {
                if (got[k - 1] != oracle(a, k)) throw new AssertionError("random " + t + " prefix " + k);
            }
        }
    }
}
```
