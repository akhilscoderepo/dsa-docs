<!-- solutions-for: 06-integer-answers -->
### Integer Answers

#### Solution: [Build] Koko Eating Bananas (LeetCode 875)
<!-- id: bs-koko-speed -->

**Approach.** A speed that finishes in time makes every faster speed finish in time, because the hours needed never increase with speed. The candidates run from 1 to the largest pile, and the largest pile is always feasible since each pile then takes one hour. Search for the smallest feasible speed: test `mid` by summing `ceil(pile / mid)` over the piles in a `long`, set `hi = mid` if the total is within `h`, and `lo = mid + 1` otherwise. The oracle tries every speed from 1 upward on random small inputs.

**Complexity.** O(n log M) time for n piles and largest pile M, and O(1) extra space.

```java run
import java.util.Random;

public final class KokoSpeed {
    static int minEatingSpeed(int[] piles, int h) {
        int lo = 1, hi = 0;
        for (int p : piles) hi = Math.max(hi, p);
        while (lo < hi) {
            int mid = lo + (hi - lo) / 2;
            long hours = 0;
            for (int p : piles) hours += (p + mid - 1) / mid;
            if (hours <= h) hi = mid;
            else lo = mid + 1;
        }
        return lo;
    }
    static int oracle(int[] piles, int h) {
        for (int s = 1; ; s++) {
            long hours = 0;
            for (int p : piles) hours += (p + s - 1) / s;
            if (hours <= h) return s;
        }
    }

    public static void main(String[] args) {
        if (minEatingSpeed(new int[] {5, 9, 14, 20}, 9) != 7) throw new AssertionError("example 1");
        if (minEatingSpeed(new int[] {4, 4, 4}, 3) != 4) throw new AssertionError("example 2");
        if (minEatingSpeed(new int[] {1000000000}, 2) != 500000000) throw new AssertionError("large pile");
        Random rnd = new Random(681);
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(6);
            int[] piles = new int[n];
            for (int i = 0; i < n; i++) piles[i] = 1 + rnd.nextInt(30);
            int h = n + rnd.nextInt(30);
            if (minEatingSpeed(piles, h) != oracle(piles, h)) throw new AssertionError("differs for h=" + h);
        }
    }
}
```

#### Solution: [Vary] Capacity To Ship Packages Within D Days (LeetCode 1011)
<!-- id: bs-ship-capacity -->

**Approach.** A capacity that ships everything in time also works for any larger capacity. The answer is at least the heaviest package, since a package cannot be split, and at most the total weight, which ships everything in one day. For a given capacity, load packages in order and start a new day whenever the next one would overflow; the number of days used is the fewest possible for that capacity. Search the smallest capacity whose day count is within `days`. The oracle tries every capacity from the heaviest package upward.

**Complexity.** O(n log W) time for total weight W, and O(1) extra space.

```java run
import java.util.Random;

public final class ShipCapacity {
    static int daysNeeded(int[] weights, int capacity) {
        int used = 1, load = 0;
        for (int w : weights) {
            if (load + w > capacity) { used++; load = 0; }
            load += w;
        }
        return used;
    }
    static int shipWithinDays(int[] weights, int days) {
        int lo = 0, hi = 0;
        for (int w : weights) { lo = Math.max(lo, w); hi += w; }
        while (lo < hi) {
            int mid = lo + (hi - lo) / 2;
            if (daysNeeded(weights, mid) <= days) hi = mid;
            else lo = mid + 1;
        }
        return lo;
    }
    static int oracle(int[] weights, int days) {
        int heaviest = 0;
        for (int w : weights) heaviest = Math.max(heaviest, w);
        for (int c = heaviest; ; c++) if (daysNeeded(weights, c) <= days) return c;
    }

    public static void main(String[] args) {
        if (shipWithinDays(new int[] {4, 8, 3, 9, 6, 5}, 3) != 12) throw new AssertionError("example 1");
        if (shipWithinDays(new int[] {2, 2, 2}, 3) != 2) throw new AssertionError("example 2");
        Random rnd = new Random(682);
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(8);
            int[] w = new int[n];
            for (int i = 0; i < n; i++) w[i] = 1 + rnd.nextInt(20);
            int days = 1 + rnd.nextInt(n);
            if (shipWithinDays(w, days) != oracle(w, days)) throw new AssertionError("differs for days=" + days);
        }
    }
}
```

#### Solution: [Boundary] Minimum Number of Days to Make m Bouquets (LeetCode 1482)
<!-- id: bs-bouquet-days -->

**Approach.** If `m * k` exceeds the number of flowers, no day can work, so return minus one before any search, computing the product as a `long`. Otherwise the latest bloom day is feasible, because every flower has bloomed and the flowers suffice. If a day is feasible, any later day is too. For a candidate day, scan the flowers keeping a run of bloomed ones, count a bouquet and reset when the run reaches `k`, and reset the run at an unbloomed flower. Search the earliest feasible day between the earliest and latest bloom days. The oracle tests each distinct bloom day in increasing order.

**Complexity.** O(n log D) time for the range D of bloom days, and O(1) extra space.

```java run
import java.util.Random;
import java.util.TreeSet;

public final class BouquetDays {
    static int bouquets(int[] bloom, int day, int k) {
        int count = 0, run = 0;
        for (int d : bloom) {
            if (d <= day) { if (++run == k) { count++; run = 0; } }
            else run = 0;
        }
        return count;
    }
    static int minDays(int[] bloom, int m, int k) {
        if ((long) m * k > bloom.length) return -1;
        int lo = Integer.MAX_VALUE, hi = 0;
        for (int d : bloom) { lo = Math.min(lo, d); hi = Math.max(hi, d); }
        while (lo < hi) {
            int mid = lo + (hi - lo) / 2;
            if (bouquets(bloom, mid, k) >= m) hi = mid;
            else lo = mid + 1;
        }
        return lo;
    }
    static int oracle(int[] bloom, int m, int k) {
        if ((long) m * k > bloom.length) return -1;
        TreeSet<Integer> days = new TreeSet<>();
        for (int d : bloom) days.add(d);
        for (int d : days) if (bouquets(bloom, d, k) >= m) return d;
        throw new AssertionError("a feasible day must exist");
    }

    public static void main(String[] args) {
        if (minDays(new int[] {4, 9, 2, 9, 9, 3, 9}, 2, 2) != 9) throw new AssertionError("example 1");
        if (minDays(new int[] {4, 9, 2, 9, 9, 3, 9}, 3, 3) != -1) throw new AssertionError("example 2");
        if (minDays(new int[] {5}, 1000000, 1000000) != -1) throw new AssertionError("the product exceeds int");
        Random rnd = new Random(683);
        for (int t = 0; t < 5000; t++) {
            int n = 1 + rnd.nextInt(10);
            int[] bloom = new int[n];
            for (int i = 0; i < n; i++) bloom[i] = 1 + rnd.nextInt(12);
            int m = 1 + rnd.nextInt(4), k = 1 + rnd.nextInt(4);
            if (minDays(bloom, m, k) != oracle(bloom, m, k)) throw new AssertionError("differs for m=" + m + " k=" + k);
        }
    }
}
```

#### Solution: [Recognize] Split Array Largest Sum (LeetCode 410)
<!-- id: bs-split-array-largest-sum -->

**Approach.** The answer lies between the largest element, since some part contains it, and the total sum, which is the answer for one part. For an allowed maximum sum `limit`, cut greedily: extend the current part while the running sum stays within the limit, and start a new part when it would not. Greedy cutting uses the fewest parts for that limit, and if it needs at most `k` parts the limit is feasible, because a part can always be split further when `k` is larger. A larger limit never needs more parts, so feasibility is monotone. The oracle is a dynamic program over prefixes that computes the best split directly, without a search over sums.

**Complexity.** O(n log S) time for total sum S, and O(1) extra space.

```java run
import java.util.Arrays;
import java.util.Random;

public final class SplitArrayLargestSum {
    static int splitArray(int[] nums, int parts) {
        int lo = 0, hi = 0;
        for (int x : nums) { lo = Math.max(lo, x); hi += x; }
        while (lo < hi) {
            int mid = lo + (hi - lo) / 2;
            int used = 1, sum = 0;
            for (int x : nums) {
                if (sum + x > mid) { used++; sum = 0; }
                sum += x;
            }
            if (used <= parts) hi = mid;
            else lo = mid + 1;
        }
        return lo;
    }
    static int dp(int[] nums, int k) {
        int n = nums.length;
        int[] prefix = new int[n + 1];
        for (int i = 0; i < n; i++) prefix[i + 1] = prefix[i] + nums[i];
        int[][] best = new int[k + 1][n + 1];
        for (int[] row : best) Arrays.fill(row, Integer.MAX_VALUE);
        best[0][0] = 0;
        for (int j = 1; j <= k; j++)
            for (int i = j; i <= n; i++)
                for (int cut = j - 1; cut < i; cut++)
                    if (best[j - 1][cut] != Integer.MAX_VALUE)
                        best[j][i] = Math.min(best[j][i], Math.max(best[j - 1][cut], prefix[i] - prefix[cut]));
        return best[k][n];
    }

    public static void main(String[] args) {
        if (splitArray(new int[] {3, 9, 1, 4, 6, 2}, 3) != 12) throw new AssertionError("example 1");
        if (splitArray(new int[] {5, 5}, 1) != 10) throw new AssertionError("example 2");
        if (splitArray(new int[] {0, 0, 0}, 2) != 0) throw new AssertionError("all zeros");
        Random rnd = new Random(684);
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(8);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(15);
            int k = 1 + rnd.nextInt(n);
            if (splitArray(a, k) != dp(a, k)) throw new AssertionError("differs on " + Arrays.toString(a) + " k=" + k);
        }
    }
}
```
