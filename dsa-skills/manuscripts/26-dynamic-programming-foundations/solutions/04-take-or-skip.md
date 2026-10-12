<!-- solutions-for: 26-dynamic-programming-foundations -->
### Solutions For Take Or Skip

#### Solution: [Build] Nonadjacent Sum (Author exercise)
<!-- id: dp-takeskip-nonadjacent-sum -->

**Approach.**
The method stores `best[i]`, the highest score of a legal selection that uses only the first `i` positions. The base entry `best[0]` is 0, which is the score of the empty selection. For each prefix length `i`, the skip case keeps `best[i - 1]`. The take case adds `value[i - 1]` to `best[i - 2]`, because using the last position forbids the position before it. For `i = 1` the take case adds to 0.

The invariant is that every legal selection within the first `i` positions is covered by exactly one case, so the larger case is the best score. The method writes only into its own table. An in-place variant that stored sums into the input would change the caller's array, and the test asserts that fact.

**Complexity.**
- **Time** is O(n), because each prefix length takes one comparison of two sums.
- **Space** is O(n) for the table, and the input array stays unchanged.

```java run
import java.util.*;

public final class DpTakeSkipNonadjacentSum {
    /**
     * Returns the largest sum over selections with no two adjacent positions.
     * Time: O(n). Space: O(n).
     * Invariant: best[i] is the highest score within the first i positions.
     */
    static int nonAdjacentBest(int[] value) {
        int n = value.length;
        // Java zero-fills the table, so best[0] is the empty-prefix score of 0.
        int[] best = new int[n + 1];
        // One iteration per prefix length costs O(n) in total.
        for (int i = 1; i <= n; i++) {
            // Skip case: the last position stays out, so the prefix of length i - 1 decides.
            int skip = best[i - 1];
            // Take case: the last position is used, so the position before it is forbidden.
            int take = value[i - 1] + (i >= 2 ? best[i - 2] : 0);
            // Every legal selection falls into one case, so the larger case is the best.
            best[i] = Math.max(skip, take);
        }
        // The full prefix covers the whole array.
        return best[n];
    }

    /** Variant that writes into its input, used only to show why the table is separate. */
    static int inPlace(int[] value) {
        for (int i = 1; i < value.length; i++) {
            value[i] = Math.max(value[i - 1], value[i] + (i >= 2 ? value[i - 2] : 0));
        }
        return value.length == 0 ? 0 : value[value.length - 1];
    }

    /** Oracle: tests every subset of positions and rejects subsets with adjacent members. */
    static int oracle(int[] value) {
        int n = value.length;
        int bestSum = 0;
        for (int mask = 0; mask < (1 << n); mask++) {
            // A mask has adjacent members exactly when it overlaps its own shift by one.
            if ((mask & (mask >> 1)) != 0) continue;
            int sum = 0;
            for (int i = 0; i < n; i++) if ((mask >> i & 1) == 1) sum += value[i];
            bestSum = Math.max(bestSum, sum);
        }
        return bestSum;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (nonAdjacentBest(new int[] {5, 8, 5}) != 10) throw new AssertionError("ex1");
        if (nonAdjacentBest(new int[] {3, 2, 7, 10}) != 13) throw new AssertionError("ex2");
        // The empty array and a single element.
        if (nonAdjacentBest(new int[] {}) != 0) throw new AssertionError("empty");
        if (nonAdjacentBest(new int[] {7}) != 7) throw new AssertionError("single");
        // The greedy pick of the naive section fails on the first example, and the alternating pick fails on 9,1,1,9.
        if (nonAdjacentBest(new int[] {9, 1, 1, 9}) != 18) throw new AssertionError("alternating");
        // Java fact: the in-place variant changes the caller's array.
        int[] shared = {5, 8, 5};
        int[] copy = shared.clone();
        inPlace(shared);
        if (Arrays.equals(shared, copy)) throw new AssertionError("in place should mutate");
        // The real method leaves the array unchanged.
        int[] safe = {5, 8, 5};
        nonAdjacentBest(safe);
        if (!Arrays.equals(safe, copy)) throw new AssertionError("mutated");
        // Random arrays against exhaustive subset search.
        Random rnd = new Random(2611);
        for (int t = 0; t < 4000; t++) {
            int[] v = new int[rnd.nextInt(13)];
            for (int i = 0; i < v.length; i++) v[i] = rnd.nextInt(30);
            if (nonAdjacentBest(v) != oracle(v)) throw new AssertionError("random " + t + " " + Arrays.toString(v));
        }
    }
}
```

#### Solution: [Vary] House Robber With Minimum Spacing (LeetCode 198)
<!-- id: dp-takeskip-spaced-houses -->

**Approach.**
The table keeps the same meaning: `best[i]` is the highest score within the first `i` positions. Only the take case changes. Using position `i - 1` forbids every position closer than `gap`, which are the positions `i - gap` through `i - 2`. So the remaining selection lies in the prefix of length `i - gap`. When `i - gap` is negative, no earlier position exists, and the rest contributes 0.

With `gap` equal to 2, the take case reads `best[i - 2]` and the method equals the nonadjacent version. With `gap` equal to 1, the take case reads `best[i - 1]`, which allows adjacent positions and sums every value. The invariant is the same as before: both cases together cover each legal selection within the prefix.

**Complexity.**
- **Time** is O(n), because each prefix length does one comparison and one table read.
- **Space** is O(n) for the table; the input array stays unchanged.

```java run
import java.util.*;

public final class DpTakeSkipSpacedPickups {
    /**
     * Returns the largest sum over selections whose positions differ pairwise by at least gap.
     * Time: O(n). Space: O(n).
     * Invariant: best[i] is the highest score within the first i positions.
     */
    static int spaced(int[] value, int gap) {
        int n = value.length;
        // best[0] is 0 for the empty prefix.
        int[] best = new int[n + 1];
        // One iteration per prefix length costs O(n) in total.
        for (int i = 1; i <= n; i++) {
            // Skip case: the last position stays out.
            int skip = best[i - 1];
            // Take case: only the prefix of length i - gap is compatible, and a negative length means no earlier position.
            int take = value[i - 1] + (i - gap >= 0 ? best[i - gap] : 0);
            // The larger case is the best score for this prefix.
            best[i] = Math.max(skip, take);
        }
        // The full prefix covers the whole array.
        return best[n];
    }

    /** Oracle: tests every subset and rejects subsets with two positions closer than gap. */
    static int oracle(int[] value, int gap) {
        int n = value.length;
        int bestSum = 0;
        for (int mask = 0; mask < (1 << n); mask++) {
            boolean legal = true;
            int last = -gap;
            int sum = 0;
            for (int i = 0; i < n && legal; i++) {
                if ((mask >> i & 1) == 0) continue;
                // Two chosen positions must differ by at least gap.
                if (i - last < gap) legal = false;
                last = i;
                sum += value[i];
            }
            if (legal) bestSum = Math.max(bestSum, sum);
        }
        return bestSum;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (spaced(new int[] {6, 1, 5, 7, 2}, 3) != 13) throw new AssertionError("ex1");
        if (spaced(new int[] {3, 8, 1}, 5) != 8) throw new AssertionError("ex2");
        // A gap of 1 sums every value, and a gap of 2 matches the nonadjacent rule.
        if (spaced(new int[] {4, 0, 9, 2}, 1) != 15) throw new AssertionError("gap1");
        if (spaced(new int[] {5, 8, 5}, 2) != 10) throw new AssertionError("gap2");
        if (spaced(new int[] {}, 4) != 0) throw new AssertionError("empty");
        // The input array is read only.
        int[] v0 = {2, 4, 6};
        int[] copy = v0.clone();
        spaced(v0, 2);
        if (!Arrays.equals(v0, copy)) throw new AssertionError("mutated");
        // Random arrays and gaps against exhaustive subset search, including gaps larger than the array.
        Random rnd = new Random(2612);
        for (int t = 0; t < 4000; t++) {
            int[] v = new int[rnd.nextInt(12)];
            for (int i = 0; i < v.length; i++) v[i] = rnd.nextInt(25);
            int gap = 1 + rnd.nextInt(14);
            if (spaced(v, gap) != oracle(v, gap)) throw new AssertionError("random " + t + " " + Arrays.toString(v) + " gap " + gap);
        }
    }
}
```

#### Solution: [Boundary] All Zero And Singleton (Author exercise)
<!-- id: dp-takeskip-zero-singleton -->

**Approach.**
Each table entry holds a pair: the highest score within the first `i` positions and the smallest count of positions that reach it. The base pair is (0, 0) for the empty prefix. The skip case copies the pair of the prefix of length `i - 1`. The take case adds `value[i - 1]` to the sum of the prefix of length `i - 2`, adds 1 to its count, and treats a missing prefix as (0, 0).

The method chooses the take pair only when its sum is larger, or when the sums tie and its count is smaller. The ordering is compatible with the addition of one position, so the best pair of a prefix comes from the best pairs of shorter prefixes. A zero value never wins a tie, since it raises the count without raising the sum. A negative value never wins, because the skip pair is larger. So an array with no positive values returns (0, 0).

**Complexity.**
- **Time** is O(n), because each prefix length compares two pairs in constant time.
- **Space** is O(n) for two int arrays, and the input array stays unchanged.

```java run
import java.util.*;

public final class DpTakeSkipZeroSingleton {
    /**
     * Returns {largest sum, fewest positions reaching it} over selections with no adjacent positions.
     * Time: O(n). Space: O(n).
     * Invariant: sum[i] and cnt[i] hold the best pair within the first i positions.
     */
    static int[] bestPair(int[] value) {
        int n = value.length;
        // The empty prefix gives the pair (0, 0), which Java zero-fill provides.
        int[] sum = new int[n + 1];
        int[] cnt = new int[n + 1];
        // One iteration per prefix length costs O(n) in total.
        for (int i = 1; i <= n; i++) {
            // Skip case: copy the pair of the shorter prefix.
            int skipSum = sum[i - 1];
            int skipCnt = cnt[i - 1];
            // Take case: add the last position to the pair two prefixes back, or to (0, 0) for the first prefix.
            int takeSum = value[i - 1] + (i >= 2 ? sum[i - 2] : 0);
            int takeCnt = 1 + (i >= 2 ? cnt[i - 2] : 0);
            // Taking wins only with a larger sum, or with an equal sum and fewer positions.
            if (takeSum > skipSum || (takeSum == skipSum && takeCnt < skipCnt)) {
                sum[i] = takeSum;
                cnt[i] = takeCnt;
            } else {
                sum[i] = skipSum;
                cnt[i] = skipCnt;
            }
        }
        // The full prefix covers the whole array.
        return new int[] {sum[n], cnt[n]};
    }

    /** Oracle: tests every subset, keeping the largest sum and then the smallest size. */
    static int[] oracle(int[] value) {
        int n = value.length;
        int bestSum = 0;
        int bestCnt = 0;
        for (int mask = 0; mask < (1 << n); mask++) {
            if ((mask & (mask >> 1)) != 0) continue;
            int sum = 0;
            int cnt = 0;
            for (int i = 0; i < n; i++) {
                if ((mask >> i & 1) == 1) {
                    sum += value[i];
                    cnt++;
                }
            }
            if (sum > bestSum || (sum == bestSum && cnt < bestCnt)) {
                bestSum = sum;
                bestCnt = cnt;
            }
        }
        return new int[] {bestSum, bestCnt};
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!Arrays.equals(bestPair(new int[] {0, 0, 0}), new int[] {0, 0})) throw new AssertionError("ex1");
        if (!Arrays.equals(bestPair(new int[] {2, 0, -4, 2, 0}), new int[] {4, 2})) throw new AssertionError("ex2");
        // Empty array, singletons of each sign, and an all-negative array keep the empty choice.
        if (!Arrays.equals(bestPair(new int[] {}), new int[] {0, 0})) throw new AssertionError("empty");
        if (!Arrays.equals(bestPair(new int[] {7}), new int[] {7, 1})) throw new AssertionError("single positive");
        if (!Arrays.equals(bestPair(new int[] {-7}), new int[] {0, 0})) throw new AssertionError("single negative");
        if (!Arrays.equals(bestPair(new int[] {-3, -1, -8}), new int[] {0, 0})) throw new AssertionError("negatives");
        // The input array is read only.
        int[] v0 = {1, -2, 3};
        int[] copy = v0.clone();
        bestPair(v0);
        if (!Arrays.equals(v0, copy)) throw new AssertionError("mutated");
        // Random arrays with zeros and negatives against exhaustive subset search.
        Random rnd = new Random(2613);
        for (int t = 0; t < 5000; t++) {
            int[] v = new int[rnd.nextInt(13)];
            for (int i = 0; i < v.length; i++) v[i] = rnd.nextInt(9) - 4;
            if (!Arrays.equals(bestPair(v), oracle(v))) throw new AssertionError("random " + t + " " + Arrays.toString(v));
        }
    }
}
```

#### Solution: [Recognize] House Robber II (LeetCode 213)
<!-- id: dp-takeskip-circular-houses -->

**Approach.**
In a circle, house 0 and house `n - 1` are neighbours, so a legal selection never contains both. Every legal selection therefore avoids house 0, or avoids house `n - 1`, or avoids both. The method runs the straight-line table on the range from house 1 to house `n - 1`, and again on the range from house 0 to house `n - 2`. It returns the larger result. Each range is an ordinary line, because the ends of a range are not adjacent.

A single house is a special case, since both ranges would be empty and the house has no neighbour. The method returns `nums[0]` for `n` equal to 1. The straight-line helper receives bounds and reads the original array, so no copy is made. The invariant of the helper is the same prefix statement as in the build exercise, applied to the chosen range.

**Complexity.**
- **Time** is O(n), because the method makes two linear passes.
- **Space** is O(n) for each table, and the input array stays unchanged.

```java run
import java.util.*;

public final class DpTakeSkipCircularHouses {
    /**
     * Returns the largest sum over selections in a circle with no two adjacent houses.
     * Time: O(n). Space: O(n).
     * Invariant: each straight-line pass returns the best score of its range.
     */
    static int rob(int[] nums) {
        int n = nums.length;
        // A single house has no neighbour, and both ranges below would be empty.
        if (n == 1) return nums[0];
        // Either house 0 is unused or house n - 1 is unused, so two straight ranges cover every case.
        return Math.max(line(nums, 1, n - 1), line(nums, 0, n - 2));
    }

    /** Returns the best nonadjacent sum over nums[from..to], inclusive, using a prefix table. */
    static int line(int[] nums, int from, int to) {
        int len = to - from + 1;
        int[] best = new int[len + 1];
        // One iteration per prefix length of the range costs O(n).
        for (int i = 1; i <= len; i++) {
            // Skip case keeps the shorter prefix.
            int skip = best[i - 1];
            // Take case adds the range element to the prefix two back.
            int take = nums[from + i - 1] + (i >= 2 ? best[i - 2] : 0);
            // The larger case is the best score for the prefix.
            best[i] = Math.max(skip, take);
        }
        return best[len];
    }

    /** Oracle: tests every subset of the circle and rejects circular neighbours. */
    static int oracle(int[] nums) {
        int n = nums.length;
        int bestSum = 0;
        for (int mask = 0; mask < (1 << n); mask++) {
            boolean legal = true;
            int sum = 0;
            for (int i = 0; i < n; i++) {
                if ((mask >> i & 1) == 0) continue;
                sum += nums[i];
                int next = (i + 1) % n;
                // A house is adjacent to the next one, wrapping around the circle, unless the circle has one house.
                if (next != i && (mask >> next & 1) == 1) legal = false;
            }
            if (legal) bestSum = Math.max(bestSum, sum);
        }
        return bestSum;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (rob(new int[] {4, 9, 4}) != 9) throw new AssertionError("ex1");
        if (rob(new int[] {5, 1, 1, 5}) != 6) throw new AssertionError("ex2");
        // One house and two houses.
        if (rob(new int[] {6}) != 6) throw new AssertionError("single");
        if (rob(new int[] {3, 8}) != 8) throw new AssertionError("pair");
        // The input array is read only.
        int[] v0 = {2, 7, 9, 3};
        int[] copy = v0.clone();
        rob(v0);
        if (!Arrays.equals(v0, copy)) throw new AssertionError("mutated");
        // Random circles against exhaustive subset search.
        Random rnd = new Random(2614);
        for (int t = 0; t < 4000; t++) {
            int[] v = new int[1 + rnd.nextInt(12)];
            for (int i = 0; i < v.length; i++) v[i] = rnd.nextInt(30);
            if (rob(v) != oracle(v)) throw new AssertionError("random " + t + " " + Arrays.toString(v));
        }
    }
}
```
