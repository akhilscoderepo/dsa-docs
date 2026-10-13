<!-- solutions-for: 29-dynamic-programming-intervals-and-advanced-states -->
### Solutions For Interval DP

#### Solution: [Build] Best Split Of A Short Interval (Author exercise)
<!-- id: dp29-short-interval-split -->

**Approach.**
The method builds prefix sums over the whole array, so the sum of any interval comes from two reads. It then fills `dp[x][y]` only for `l <= x <= y <= r`, by increasing interval length. A one-piece interval keeps the value 0 that Java writes into a new array. A longer interval takes the minimum of `dp[x][k] + dp[k + 1][y]` over every split point `k`, and adds the interval sum.

The invariant is that `dp[x][y]` describes exactly the pieces `x` through `y`, and it reads only intervals that are strictly shorter and lie inside `[l, r]`. Pieces outside the range never enter a read, so they never change the answer.

**Complexity.**
- **Time** is O(L^3) for L = r - l + 1, because there are O(L^2) intervals and each tries up to L split points.
- **Space** is O(n + L^2) for the prefix sums and the table, and the input array stays unchanged.

```java run
import java.util.*;

public final class IntervalShortSplit {
    /**
     * Returns the least cost to merge a[l..r] into one piece.
     * Time: O(L^3) with L = r - l + 1. Space: O(n + L^2).
     * Invariant: dp[x][y] reads only shorter intervals, which are final.
     */
    static int rangeMergeCost(int[] a, int l, int r) {
        // prefix[i] is the sum of the first i sizes, so an interval sum costs two reads.
        int[] prefix = new int[a.length + 1];
        // One pass builds all prefix sums in O(n).
        for (int i = 0; i < a.length; i++) prefix[i + 1] = prefix[i] + a[i];
        // The table is indexed by absolute positions; Java fills it with zeros, which is right for one-piece intervals.
        int[][] dp = new int[a.length][a.length];
        // The outer loop runs over interval length, so shorter intervals are final first.
        for (int len = 2; len <= r - l + 1; len++) {
            // The first index slides so that the interval stays inside [l, r].
            for (int x = l; x + len - 1 <= r; x++) {
                int y = x + len - 1;
                // best starts above any real cost, so the first split replaces it.
                int best = Integer.MAX_VALUE;
                // Each split point joins a left interval and a right interval.
                for (int k = x; k < y; k++) {
                    // The two parts are independent, so their best costs add.
                    best = Math.min(best, dp[x][k] + dp[k + 1][y]);
                }
                // The last merge always copies the whole interval once.
                dp[x][y] = best + prefix[y + 1] - prefix[x];
            }
        }
        // The entry for the full range holds the answer.
        return dp[l][r];
    }

    /** Oracle: tries every pair of neighbours to merge next, with no table. */
    static int oracle(List<Integer> pieces) {
        if (pieces.size() < 2) return 0;
        int best = Integer.MAX_VALUE;
        for (int i = 0; i + 1 < pieces.size(); i++) {
            List<Integer> next = new ArrayList<>(pieces);
            int sum = next.get(i) + next.get(i + 1);
            next.set(i, sum);
            next.remove(i + 1);
            best = Math.min(best, sum + oracle(next));
        }
        return best;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (rangeMergeCost(new int[]{9, 7, 8, 8}, 1, 3) != 38) throw new AssertionError("ex1");
        if (rangeMergeCost(new int[]{4, 1, 3, 5}, 0, 2) != 12) throw new AssertionError("ex2");
        // The lesson array over its full range gives 64.
        if (rangeMergeCost(new int[]{9, 7, 8, 8}, 0, 3) != 64) throw new AssertionError("lesson");
        // A one-piece range costs 0, and a two-piece range costs the sum.
        if (rangeMergeCost(new int[]{5, 6, 7}, 1, 1) != 0) throw new AssertionError("single");
        if (rangeMergeCost(new int[]{5, 6, 7}, 1, 2) != 13) throw new AssertionError("pair");
        // A new Java int array holds zeros, which the base intervals rely on.
        int[][] fresh = new int[3][3];
        if (fresh[1][1] != 0 || fresh[0][2] != 0) throw new AssertionError("zero fill");
        // The input array is not changed by the call.
        int[] keep = {2, 9, 4, 4};
        int[] copy = keep.clone();
        rangeMergeCost(keep, 0, 3);
        if (!Arrays.equals(keep, copy)) throw new AssertionError("mutated");
        // Random subranges against the oracle that tries every neighbour pair.
        Random rnd = new Random(2901);
        for (int t = 0; t < 1500; t++) {
            int n = 1 + rnd.nextInt(7);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(10);
            int l = rnd.nextInt(n);
            int r = l + rnd.nextInt(n - l);
            List<Integer> sub = new ArrayList<>();
            for (int i = l; i <= r; i++) sub.add(a[i]);
            if (rangeMergeCost(a, l, r) != oracle(sub)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Vary] Matrix Chain Cost (Author exercise)
<!-- id: dp29-matrix-chain-cost -->

**Approach.**
Matrix `i` has shape `dims[i] x dims[i + 1]`. For the matrices `l` through `r`, split after `k` means the left product has shape `dims[l] x dims[k + 1]` and the right product has shape `dims[k + 1] x dims[r + 1]`. The last multiplication therefore costs `dims[l] * dims[k + 1] * dims[r + 1]`. The entry `dp[l][r]` is the minimum over `k` of the two part costs plus that product.

The last multiplication cost depends on `k`, so it moves inside the minimum, unlike the interval sum in the lesson. The invariant is unchanged: `dp[l][r]` reads only shorter intervals. A single matrix needs no multiplication, so its entry is 0.

**Complexity.**
- **Time** is O(n^3), because O(n^2) intervals each try up to n split points at constant cost.
- **Space** is O(n^2) for the table, and `dims` stays unchanged.

```java run
import java.util.*;

public final class IntervalMatrixChain {
    /**
     * Returns the least scalar multiplications for the chain described by dims.
     * Time: O(n^3). Space: O(n^2).
     * Invariant: dp[l][r] reads only shorter intervals, which are final.
     */
    static int chainCost(int[] dims) {
        // n matrices need n + 1 dimensions.
        int n = dims.length - 1;
        // Zero or one matrix needs no multiplication.
        if (n < 2) return 0;
        // dp[l][r] is the least cost for matrices l through r; Java zeroes the single-matrix entries.
        int[][] dp = new int[n][n];
        // Interval length runs outward so shorter chains are final first.
        for (int len = 2; len <= n; len++) {
            // The first matrix slides across the valid starts, which costs n - len + 1 steps.
            for (int l = 0; l + len <= n; l++) {
                int r = l + len - 1;
                int best = Integer.MAX_VALUE;
                // The split point k decides the shapes of both products.
                for (int k = l; k < r; k++) {
                    // The last multiplication costs rows of the left, the shared size and columns of the right.
                    int cost = dp[l][k] + dp[k + 1][r] + dims[l] * dims[k + 1] * dims[r + 1];
                    // Keep the cheapest split.
                    best = Math.min(best, cost);
                }
                dp[l][r] = best;
            }
        }
        // The whole chain is the interval from 0 to n - 1.
        return dp[0][n - 1];
    }

    /** Oracle: multiplies any adjacent pair next, using shape lists and no table. */
    static int oracle(List<Integer> d) {
        if (d.size() < 3) return 0;
        int best = Integer.MAX_VALUE;
        for (int i = 1; i + 1 < d.size(); i++) {
            // Multiplying the matrices around dimension i removes that dimension.
            int cost = d.get(i - 1) * d.get(i) * d.get(i + 1);
            List<Integer> next = new ArrayList<>(d);
            next.remove(i);
            best = Math.min(best, cost + oracle(next));
        }
        return best;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (chainCost(new int[]{10, 30, 5, 60}) != 4500) throw new AssertionError("ex1");
        if (chainCost(new int[]{3, 8, 2, 9, 4}) != 144) throw new AssertionError("ex2");
        // One matrix and one dimension pair give 0, and two matrices give one product.
        if (chainCost(new int[]{7, 2}) != 0) throw new AssertionError("single");
        if (chainCost(new int[]{4, 5, 6}) != 120) throw new AssertionError("pair");
        // A single dimension is legal input and describes no matrix.
        if (chainCost(new int[]{6}) != 0) throw new AssertionError("none");
        // The input array is not changed by the call.
        int[] keep = {5, 2, 8, 3};
        int[] copy = keep.clone();
        chainCost(keep);
        if (!Arrays.equals(keep, copy)) throw new AssertionError("mutated");
        // Random chains against the oracle that tries every adjacent product.
        Random rnd = new Random(2902);
        for (int t = 0; t < 1500; t++) {
            int len = 1 + rnd.nextInt(8);
            int[] d = new int[len];
            List<Integer> list = new ArrayList<>();
            for (int i = 0; i < len; i++) {
                d[i] = 1 + rnd.nextInt(9);
                list.add(d[i]);
            }
            if (chainCost(d) != oracle(list)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Boundary] Empty And Singleton Intervals (Author exercise)
<!-- id: dp29-empty-singleton -->

**Approach.**
An interval of length 0 or 1 has no merge to perform, so the method returns 0 for `a.length < 2` before it allocates any table. This also protects the final read `dp[0][n - 1]`, which would use index -1 for an empty array. For longer arrays the method uses the standard table, with prefix sums of length `n + 1` and entries filled by increasing interval length.

The invariant is that every base entry is 0 when a longer interval reads it, and no read touches an entry of equal or greater length. The neutral value is correct because adding a one-piece interval to a split contributes no copying.

**Complexity.**
- **Time** is O(n^3) for n pieces, and O(1) when n is 0 or 1.
- **Space** is O(n^2) for the table, and the input array stays unchanged.

```java run
import java.util.*;

public final class IntervalEmptySingleton {
    /**
     * Returns the least merge cost of the whole array, and 0 for fewer than two pieces.
     * Time: O(n^3), or O(1) below two pieces. Space: O(n^2).
     * Invariant: base entries are 0 before any longer interval reads them.
     */
    static int wholeCost(int[] a) {
        int n = a.length;
        // With no merge to make, the neutral cost is 0 and the table is never built.
        if (n < 2) return 0;
        // prefix has n + 1 entries, so prefix[0] = 0 covers an interval that starts at index 0.
        int[] prefix = new int[n + 1];
        for (int i = 0; i < n; i++) prefix[i + 1] = prefix[i] + a[i];
        // Java zeroes the diagonal, which holds the one-piece intervals.
        int[][] dp = new int[n][n];
        // Length 2 is the first length that needs a merge.
        for (int len = 2; len <= n; len++) {
            for (int l = 0; l + len <= n; l++) {
                int r = l + len - 1;
                int best = Integer.MAX_VALUE;
                // Every split point reads two shorter intervals.
                for (int k = l; k < r; k++) best = Math.min(best, dp[l][k] + dp[k + 1][r]);
                // Add the interval sum for the last merge.
                dp[l][r] = best + prefix[r + 1] - prefix[l];
            }
        }
        // The corner interval is the whole array.
        return dp[0][n - 1];
    }

    /** Oracle: tries every neighbour pair as the next merge. */
    static int oracle(List<Integer> pieces) {
        if (pieces.size() < 2) return 0;
        int best = Integer.MAX_VALUE;
        for (int i = 0; i + 1 < pieces.size(); i++) {
            List<Integer> next = new ArrayList<>(pieces);
            int sum = next.get(i) + next.get(i + 1);
            next.set(i, sum);
            next.remove(i + 1);
            best = Math.min(best, sum + oracle(next));
        }
        return best;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (wholeCost(new int[]{}) != 0) throw new AssertionError("ex1");
        if (wholeCost(new int[]{3, 1, 2}) != 9) throw new AssertionError("ex2");
        // One piece costs 0, two pieces cost their sum, and zeros cost 0.
        if (wholeCost(new int[]{7}) != 0) throw new AssertionError("single");
        if (wholeCost(new int[]{5, 5}) != 10) throw new AssertionError("pair");
        if (wholeCost(new int[]{0, 0, 0}) != 0) throw new AssertionError("zeros");
        // The lesson array returns 64, which the cheapest first rule misses.
        if (wholeCost(new int[]{9, 7, 8, 8}) != 64) throw new AssertionError("lesson");
        // A Java array of length 0 is legal and has length 0, so the guard is reachable.
        if (new int[0].length != 0) throw new AssertionError("length");
        // The input array is not changed by the call.
        int[] keep = {4, 4, 1};
        int[] copy = keep.clone();
        wholeCost(keep);
        if (!Arrays.equals(keep, copy)) throw new AssertionError("mutated");
        // Random arrays, including empty ones, against the oracle.
        Random rnd = new Random(2903);
        for (int t = 0; t < 1500; t++) {
            int n = rnd.nextInt(8);
            int[] a = new int[n];
            List<Integer> list = new ArrayList<>();
            for (int i = 0; i < n; i++) {
                a[i] = rnd.nextInt(10);
                list.add(a[i]);
            }
            if (wholeCost(a) != oracle(list)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Recognize] Burst Balloons (LeetCode 312)
<!-- id: dp29-burst-balloons -->

**Approach.**
Choosing the first balloon to burst fails, because its removal changes the neighbours of the others and the two sides depend on each other. Choosing the last balloon removed in an open interval fixes this. The method pads the values with a 1 on each side, so `v[0] = 1` and `v[n + 1] = 1`. The entry `dp[l][r]` is the most coins from bursting every balloon strictly between positions `l` and `r`.

If balloon `k` bursts last in that open interval, its neighbours at that moment are `v[l]` and `v[r]`, because everything else between them is gone. The two sides `(l, k)` and `(k, r)` then never affect each other. So `dp[l][r]` is the maximum over `k` of `dp[l][k] + dp[k][r] + v[l] * v[k] * v[r]`. An open interval with no balloon inside, where `r = l + 1`, is worth 0.

The invariant is that `dp[l][r]` reads only open intervals that are strictly shorter. The answer is `dp[0][n + 1]`.

**Complexity.**
- **Time** is O(n^3), because O(n^2) open intervals each try up to n last balloons.
- **Space** is O(n^2) for the table and O(n) for the padded array, and `nums` stays unchanged.

```java run
import java.util.*;

public final class IntervalBurstBalloons {
    /**
     * Returns the most coins from bursting every balloon.
     * Time: O(n^3). Space: O(n^2).
     * Invariant: dp[l][r] covers the balloons strictly between l and r and reads shorter gaps.
     */
    static int maxCoins(int[] nums) {
        int n = nums.length;
        // The padded array has a boundary value 1 at both ends, so a missing neighbour counts as 1.
        int[] v = new int[n + 2];
        v[0] = 1;
        v[n + 1] = 1;
        // Copy the values into the middle so the input array stays unchanged.
        for (int i = 0; i < n; i++) v[i + 1] = nums[i];
        // Java zeroes the table, which is right for an empty gap with r = l + 1.
        int[][] dp = new int[n + 2][n + 2];
        // gap is r - l, and gap 2 is the first gap with a balloon inside.
        for (int gap = 2; gap <= n + 1; gap++) {
            // l slides so that r stays within the padded array.
            for (int l = 0; l + gap <= n + 1; l++) {
                int r = l + gap;
                int best = 0;
                // k is the balloon that bursts last inside the open gap.
                for (int k = l + 1; k < r; k++) {
                    // At that moment its neighbours are the gap boundaries v[l] and v[r].
                    int coins = dp[l][k] + dp[k][r] + v[l] * v[k] * v[r];
                    // Keep the largest total.
                    if (coins > best) best = coins;
                }
                dp[l][r] = best;
            }
        }
        // The widest gap holds every real balloon.
        return dp[0][n + 1];
    }

    /** Oracle: tries every burst order by removing one balloon at a time. */
    static int oracle(List<Integer> balloons) {
        int best = 0;
        for (int i = 0; i < balloons.size(); i++) {
            int left = i == 0 ? 1 : balloons.get(i - 1);
            int right = i + 1 == balloons.size() ? 1 : balloons.get(i + 1);
            List<Integer> next = new ArrayList<>(balloons);
            int value = next.remove(i);
            best = Math.max(best, left * value * right + oracle(next));
        }
        return best;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (maxCoins(new int[]{2, 4, 3}) != 33) throw new AssertionError("ex1");
        if (maxCoins(new int[]{5, 1, 6, 2}) != 105) throw new AssertionError("ex2");
        // The empty array earns 0, and one balloon earns its own value.
        if (maxCoins(new int[]{}) != 0) throw new AssertionError("empty");
        if (maxCoins(new int[]{9}) != 9) throw new AssertionError("single");
        // Zero values are legal and earn nothing when they are the product.
        if (maxCoins(new int[]{0, 0}) != 0) throw new AssertionError("zeros");
        // The input array is not changed by the call.
        int[] keep = {3, 1, 5, 8};
        int[] copy = keep.clone();
        maxCoins(keep);
        if (!Arrays.equals(keep, copy)) throw new AssertionError("mutated");
        // Random arrays against the oracle that tries every burst order.
        Random rnd = new Random(2904);
        for (int t = 0; t < 1500; t++) {
            int n = rnd.nextInt(8);
            int[] a = new int[n];
            List<Integer> list = new ArrayList<>();
            for (int i = 0; i < n; i++) {
                a[i] = rnd.nextInt(10);
                list.add(a[i]);
            }
            if (maxCoins(a) != oracle(list)) throw new AssertionError("random " + t);
        }
    }
}
```
