<!-- solutions-for: 01-meet-in-middle -->
### Solutions For Meet In Middle

#### Solution: [Build] Half Subset Sums (Author exercise)
<!-- id: mm35-half-subset-sums -->

**Approach.**
The result array starts with one entry, the empty sum 0. For each element `x` the method copies the current entries into the next block of the same array, adding `x` to each copy. The entry count doubles with every element, so after `k` elements the array holds `2^k` sums, one per subset of the first `k` positions. The method adds in `long`, so values near 10^9 cannot wrap. A final sort puts the sums in order. The invariant is that after each element the filled prefix of the array holds exactly one sum per subset of the elements seen so far.

The program compares the method with a mask-based enumeration on random arrays that include negative values and repeats. It also checks that two ints near 2^31 overflow in `int` arithmetic and not in `long`, which is why the sums are `long`.

**Complexity.**
- **Time** is O(2^n * n) with the sort, because the doubling writes 2^n entries and the sort compares them in n * 2^n steps.
- **Space** is O(2^n) for the result array.

```java run
import java.util.Arrays;
import java.util.Random;

public final class HalfSubsetSumsBuild {
    /**
     * Returns all subset sums of a in non-decreasing order.
     * Time: O(2^n * n). Space: O(2^n).
     * Invariant: after element k the first 2^k entries hold one sum per subset of a[0..k-1].
     */
    static long[] subsetSums(int[] a) {
        long[] s = new long[1 << a.length];
        int size = 1; // the empty subset gives the sum 0
        for (int k = 0; k < a.length; k++) {
            // copy every sum into the next block and add a[k], so each old subset gains a twin that takes a[k]
            for (int j = 0; j < size; j++) s[size + j] = s[j] + a[k];
            size *= 2; // the count of subsets doubles with each element
        }
        Arrays.sort(s); // sorted order is the output contract
        return s;
    }

    static long[] oracle(int[] a) {
        long[] r = new long[1 << a.length];
        for (int mask = 0; mask < r.length; mask++) {
            long sum = 0;
            for (int k = 0; k < a.length; k++) if ((mask >> k & 1) == 1) sum += a[k];
            r[mask] = sum;
        }
        Arrays.sort(r);
        return r;
    }

    public static void main(String[] args) {
        // the two examples from the problem text
        if (!Arrays.equals(subsetSums(new int[]{3, 3}), new long[]{0, 3, 3, 6})) throw new AssertionError("ex1");
        if (!Arrays.equals(subsetSums(new int[]{4, -2, 5}), new long[]{-2, 0, 2, 3, 4, 5, 7, 9})) throw new AssertionError("ex2");
        // the empty array has exactly one subset
        if (!Arrays.equals(subsetSums(new int[0]), new long[]{0})) throw new AssertionError("empty");
        // int addition wraps near 2^31, long addition does not
        int wrapped = 2_000_000_000 + 2_000_000_000;
        if (wrapped >= 0 || (long) 2_000_000_000 + 2_000_000_000 != 4_000_000_000L) throw new AssertionError("overflow claim");
        // random arrays with negatives and repeats agree with the mask oracle
        Random rnd = new Random(35);
        for (int t = 0; t < 400; t++) {
            int[] a = new int[rnd.nextInt(11)];
            for (int i = 0; i < a.length; i++) a[i] = rnd.nextInt(7) - 3;
            if (!Arrays.equals(subsetSums(a), oracle(a))) throw new AssertionError("random " + Arrays.toString(a));
        }
        System.out.println("ok");
    }
}
```

#### Solution: [Vary] Closest Pair Of Half Sums (Author exercise)
<!-- id: mm35-closest-pair-half-sums -->

**Approach.**
The method lists every sum of `left` and every sum of `right`. It sorts the second list. For each sum `s` of the first list it computes the complement `target - s` and runs a lower-bound binary search for the first entry at or above the complement. The entry found and the entry before it are the only two candidates, because every other entry is farther from the complement. The method keeps the smallest distance seen. An empty array contributes the single sum 0, so empty picks are covered. The invariant is that after each first-list sum the variable `best` equals the minimum distance over all pairs that use a first-list sum seen so far.

The program checks the method against a double loop over both lists on random inputs, including targets far outside the reachable range and empty arrays.

**Complexity.**
- **Time** is O(2^a * a + 2^b * b + 2^a * b) for arrays of lengths `a` and `b`, which is the build plus one binary search per first-list sum.
- **Space** is O(2^a + 2^b) for the two lists.

```java run
import java.util.Arrays;
import java.util.Random;

public final class ClosestPairHalfSumsVary {
    static long[] sums(int[] a) {
        long[] s = new long[1 << a.length];
        int size = 1;
        for (int k = 0; k < a.length; k++) {
            for (int j = 0; j < size; j++) s[size + j] = s[j] + a[k];
            size *= 2;
        }
        return s;
    }

    /**
     * Smallest |sumLeft + sumRight - target| over all pairs of subsets.
     * Time: O(2^a * a + 2^b * b + 2^a * b). Space: O(2^a + 2^b).
     * Invariant: best is the minimum distance over the first-list sums handled so far.
     */
    static long closestPair(int[] left, int[] right, long target) {
        long[] ls = sums(left);
        long[] rs = sums(right);
        Arrays.sort(rs); // the lookup needs sorted order
        long best = Long.MAX_VALUE;
        for (long s : ls) {
            long need = target - s; // complement of the first-list sum
            int lo = 0, hi = rs.length;
            while (lo < hi) { // lower bound: first index with rs[idx] >= need
                int m = (lo + hi) >>> 1;
                if (rs[m] < need) lo = m + 1; else hi = m;
            }
            if (lo < rs.length) best = Math.min(best, Math.abs(rs[lo] - need)); // nearest from above
            if (lo > 0) best = Math.min(best, Math.abs(need - rs[lo - 1]));     // nearest from below
        }
        return best;
    }

    static long oracle(int[] left, int[] right, long target) {
        long best = Long.MAX_VALUE;
        for (long x : sums(left)) for (long y : sums(right)) best = Math.min(best, Math.abs(x + y - target));
        return best;
    }

    public static void main(String[] args) {
        // the two examples from the problem text
        if (closestPair(new int[]{5, 10}, new int[]{3, 6}, 14) != 0) throw new AssertionError("ex1");
        if (closestPair(new int[]{7, 2}, new int[]{4, -9}, 20) != 7) throw new AssertionError("ex2");
        // both arrays empty: the only total is 0
        if (closestPair(new int[0], new int[0], -5) != 5) throw new AssertionError("both empty");
        // random inputs, including targets far from every reachable total
        Random rnd = new Random(36);
        for (int t = 0; t < 500; t++) {
            int[] l = new int[rnd.nextInt(7)], r = new int[rnd.nextInt(7)];
            for (int i = 0; i < l.length; i++) l[i] = rnd.nextInt(41) - 20;
            for (int i = 0; i < r.length; i++) r[i] = rnd.nextInt(41) - 20;
            long target = rnd.nextInt(400) - 200;
            if (closestPair(l, r, target) != oracle(l, r, target)) throw new AssertionError("random");
        }
        System.out.println("ok");
    }
}
```

#### Solution: [Boundary] Duplicates And Long Sums (Author exercise)
<!-- id: mm35-duplicates-long-sums -->

**Approach.**
The method counts pairs of half subsets whose sums add to `target`. It builds the sums of the first half and the sorted sums of the second half. For each first-half sum it needs the number of second-half entries equal to the complement. Two lower-bound searches give that number: the first index at or above the complement and the first index above it. Their difference is the count of equal entries. Adding the counts over all first-half sums gives the answer. Equal sums stay in the lists as separate entries, so two subsets with the same values count twice. The invariant is that `total` holds the number of matching subsets whose first-half part has a sum already handled.

The program compares the method with a mask enumeration on arrays full of zeros, repeats and negatives, and runs the large-value example that overflows `int` arithmetic.

**Complexity.**
- **Time** is O(2^(n/2) * n), because the build and sort dominate and each lookup is two binary searches.
- **Space** is O(2^(n/2)) for the two lists.

```java run
import java.util.Arrays;
import java.util.Random;

public final class DuplicatesLongSumsBoundary {
    static long[] sums(int[] a, int from, int to) {
        long[] s = new long[1 << (to - from)];
        int size = 1;
        for (int k = from; k < to; k++) {
            for (int j = 0; j < size; j++) s[size + j] = s[j] + a[k];
            size *= 2;
        }
        return s;
    }

    /** First index in sorted r whose value is at least v. */
    static int lowerBound(long[] r, long v) {
        int lo = 0, hi = r.length;
        while (lo < hi) {
            int m = (lo + hi) >>> 1;
            if (r[m] < v) lo = m + 1; else hi = m;
        }
        return lo;
    }

    /**
     * Counts subsets of positions with sum equal to target.
     * Time: O(2^(n/2) * n). Space: O(2^(n/2)).
     * Invariant: total counts matching subsets whose first-half part was already handled.
     */
    static long countSubsets(int[] a, long target) {
        int mid = a.length / 2;
        long[] left = sums(a, 0, mid);
        long[] right = sums(a, mid, a.length);
        Arrays.sort(right); // equal sums become neighbours
        long total = 0;
        for (long s : left) {
            long need = target - s; // the second-half sum that completes the target
            // the run of entries equal to need starts at lowerBound(need) and ends before lowerBound(need + 1)
            total += lowerBound(right, need + 1) - lowerBound(right, need);
        }
        return total;
    }

    static long oracle(int[] a, long target) {
        long c = 0;
        for (int mask = 0; mask < (1 << a.length); mask++) {
            long sum = 0;
            for (int k = 0; k < a.length; k++) if ((mask >> k & 1) == 1) sum += a[k];
            if (sum == target) c++;
        }
        return c;
    }

    public static void main(String[] args) {
        // the two examples from the problem text
        if (countSubsets(new int[]{1, 1, 1}, 2) != 3) throw new AssertionError("ex1");
        if (countSubsets(new int[]{1_000_000_000, 1_000_000_000, 1_000_000_000, 1_000_000_000}, 3_000_000_000L) != 4) throw new AssertionError("ex2");
        // zeros double the count of every sum, and the empty array has one subset with sum 0
        if (countSubsets(new int[]{0, 0}, 0) != 4) throw new AssertionError("zeros");
        if (countSubsets(new int[0], 0) != 1) throw new AssertionError("empty");
        // random arrays with many repeats and negatives
        Random rnd = new Random(37);
        for (int t = 0; t < 500; t++) {
            int[] a = new int[rnd.nextInt(13)];
            for (int i = 0; i < a.length; i++) a[i] = rnd.nextInt(5) - 2;
            long target = rnd.nextInt(7) - 3;
            if (countSubsets(a, target) != oracle(a, target)) throw new AssertionError("random " + Arrays.toString(a));
        }
        System.out.println("ok");
    }
}
```

#### Solution: [Recognize] Closest Subsequence Sum (LeetCode 1755)
<!-- id: mm35-closest-subsequence-sum -->

**Approach.**
A limit of 40 on the length rules out the 2^40 enumeration and rules in two enumerations of 2^20. The order of a subsequence never changes its sum, so the problem is the closest-subset-sum question and position order does not matter. The method splits `nums` in the middle, lists both half sums, sorts the second list and looks up the complement of every first-half sum by binary search. The answer is the smallest distance. The invariant is that the pair of half sums stands for each subsequence exactly once.

The program compares the method with a mask enumeration on random arrays of length up to 14 with negative values. It also confirms that 40 values of 10^7 stay inside `int` but that 40 values near 10^9 would not, which is why the lesson sums in `long`.

**Complexity.**
- **Time** is O(2^(n/2) * n).
- **Space** is O(2^(n/2)).

```java run
import java.util.Arrays;
import java.util.Random;

public final class ClosestSubsequenceSumRecognize {
    static long[] sums(int[] a, int from, int to) {
        long[] s = new long[1 << (to - from)];
        int size = 1;
        for (int k = from; k < to; k++) {
            for (int j = 0; j < size; j++) s[size + j] = s[j] + a[k];
            size *= 2;
        }
        return s;
    }

    /**
     * Minimum |sum - goal| over all subsequences of nums.
     * Time: O(2^(n/2) * n). Space: O(2^(n/2)).
     * Invariant: each subsequence maps to exactly one pair (first-half sum, second-half sum).
     */
    static int minAbsDifference(int[] nums, int goal) {
        int mid = nums.length / 2;
        long[] left = sums(nums, 0, mid);
        long[] right = sums(nums, mid, nums.length);
        Arrays.sort(right); // required by the lower-bound search
        long best = Long.MAX_VALUE;
        for (long s : left) {
            long need = (long) goal - s; // complement
            int lo = 0, hi = right.length;
            while (lo < hi) {
                int m = (lo + hi) >>> 1;
                if (right[m] < need) lo = m + 1; else hi = m;
            }
            if (lo < right.length) best = Math.min(best, Math.abs(right[lo] - need));
            if (lo > 0) best = Math.min(best, Math.abs(need - right[lo - 1]));
        }
        return (int) best; // the answer is at most |goal| + 40 * 10^7, which fits in int
    }

    static int oracle(int[] a, int goal) {
        long best = Long.MAX_VALUE;
        for (int mask = 0; mask < (1 << a.length); mask++) {
            long sum = 0;
            for (int k = 0; k < a.length; k++) if ((mask >> k & 1) == 1) sum += a[k];
            best = Math.min(best, Math.abs(sum - goal));
        }
        return (int) best;
    }

    public static void main(String[] args) {
        // the two examples from the problem text
        if (minAbsDifference(new int[]{4, -3, 8, 1}, 10) != 0) throw new AssertionError("ex1");
        if (minAbsDifference(new int[]{3, 8}, -20) != 20) throw new AssertionError("ex2");
        // 40 values of 10^7 fit in int, while 40 values of 10^9 would not
        long small = 40L * 10_000_000, big = 40L * 1_000_000_000;
        if (small > Integer.MAX_VALUE || big <= Integer.MAX_VALUE) throw new AssertionError("range claim");
        // random arrays with negative values and goals on both sides
        Random rnd = new Random(38);
        for (int t = 0; t < 500; t++) {
            int[] a = new int[1 + rnd.nextInt(14)];
            for (int i = 0; i < a.length; i++) a[i] = rnd.nextInt(61) - 30;
            int goal = rnd.nextInt(301) - 150;
            if (minAbsDifference(a, goal) != oracle(a, goal)) throw new AssertionError("random " + Arrays.toString(a));
        }
        System.out.println("ok");
    }
}
```
