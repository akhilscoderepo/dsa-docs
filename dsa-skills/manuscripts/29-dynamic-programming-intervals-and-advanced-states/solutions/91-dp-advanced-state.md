<!-- solutions-for: 29-dynamic-programming-intervals-and-advanced-states -->
### Solutions For DP With Advanced State

#### Solution: [Build] Palindromic Subsequence In Query Ranges (LeetCode 516)
<!-- id: dp29-range-palindrome-queries -->

**Approach.**
The table `dp[l][r]` holds the longest palindromic subsequence length of `s[l..r]`. A single character gives 1. When the two end characters match, both join the subsequence and the inner range `l + 1 .. r - 1` supplies the rest, so the entry is the inner value plus 2. When they differ, at least one end is unused, so the entry is the larger of the range without the left end and the range without the right end. If the inner range is empty, its entry is a cell that was never written and still holds 0.

Rows run from the last start index down to 0 and columns run upward from `l`, so each entry reads only shorter ranges that are already final. Every query then reads one cell. The invariant is that `dp[l][r]` describes exactly the substring `s[l..r]` and nothing else.

**Complexity.**
- **Time** is O(n^2 + q) for n characters and q queries, because the table has about n^2 / 2 entries with constant work each and a query is one read.
- **Space** is O(n^2) for the table, plus O(q) for the answers.

```java run
import java.util.*;

public final class Dp29RangePalindromeQueries {
    /**
     * Answers each query with the longest palindromic subsequence length of s[l..r].
     * Time: O(n^2 + q). Space: O(n^2 + q).
     * Invariant: dp[l][r] is final and describes exactly s[l..r] when a longer range reads it.
     */
    static int[] answer(String s, int[][] queries) {
        // n is the number of characters.
        int n = s.length();
        // Row n and the cells below the diagonal stay 0, which covers empty inner ranges.
        int[][] dp = new int[n + 1][n];
        // Start indexes run from the right so that dp[l + 1][...] is final first.
        for (int l = n - 1; l >= 0; l--) {
            // A single character is a palindrome of length 1.
            dp[l][l] = 1;
            // Ends move apart one position at a time, and each range reads shorter ranges only.
            for (int r = l + 1; r < n; r++) {
                if (s.charAt(l) == s.charAt(r)) {
                    // Equal ends join the subsequence around the inner range.
                    dp[l][r] = dp[l + 1][r - 1] + 2;
                } else {
                    // Different ends mean one end is unused, so keep the larger shorter range.
                    dp[l][r] = Math.max(dp[l + 1][r], dp[l][r - 1]);
                }
            }
        }
        // Each query is one table read.
        int[] out = new int[queries.length];
        for (int q = 0; q < queries.length; q++) out[q] = dp[queries[q][0]][queries[q][1]];
        return out;
    }

    /** Oracle: tries every subset of the characters in the range and keeps the longest palindrome. */
    static int oracle(String s, int l, int r) {
        int len = r - l + 1;
        int best = 0;
        for (int mask = 1; mask < (1 << len); mask++) {
            StringBuilder t = new StringBuilder();
            for (int k = 0; k < len; k++) if ((mask >> k & 1) == 1) t.append(s.charAt(l + k));
            if (t.toString().contentEquals(new StringBuilder(t).reverse()) && t.length() > best) best = t.length();
        }
        return best;
    }

    public static void main(String[] args) {
        // Both examples of the exercise.
        if (!Arrays.equals(answer("xabcbayz", new int[][]{{0, 7}, {1, 5}, {2, 2}, {6, 7}}), new int[]{5, 5, 1, 1})) throw new AssertionError("ex1");
        if (!Arrays.equals(answer("cbbdcb", new int[][]{{0, 5}, {1, 4}}), new int[]{4, 2})) throw new AssertionError("ex2");
        // A one-character string, equal pair and unequal pair at the edges.
        if (answer("a", new int[][]{{0, 0}})[0] != 1) throw new AssertionError("single");
        if (answer("aa", new int[][]{{0, 1}})[0] != 2) throw new AssertionError("pair");
        if (answer("ab", new int[][]{{0, 1}})[0] != 1) throw new AssertionError("different pair");
        // A new int array holds zeros, so the empty inner range of an equal pair reads 0.
        int[][] fresh = new int[3][2];
        if (fresh[2][1] != 0) throw new AssertionError("zero fill");
        // Strings are immutable, so the call leaves the input equal to its copy.
        String keep = new String("abcba");
        answer(keep, new int[][]{{0, 4}});
        if (!keep.equals("abcba")) throw new AssertionError("immutable");
        // Random strings and random ranges against the subset oracle.
        Random rnd = new Random(2901);
        for (int t = 0; t < 400; t++) {
            int n = 1 + rnd.nextInt(10);
            StringBuilder b = new StringBuilder();
            for (int i = 0; i < n; i++) b.append((char) ('a' + rnd.nextInt(3)));
            String s = b.toString();
            int[][] qs = new int[5][2];
            for (int[] q : qs) {
                q[0] = rnd.nextInt(n);
                q[1] = q[0] + rnd.nextInt(n - q[0]);
            }
            int[] got = answer(s, qs);
            for (int i = 0; i < qs.length; i++) {
                if (got[i] != oracle(s, qs[i][0], qs[i][1])) throw new AssertionError("random " + t);
            }
        }
    }
}
```

#### Solution: [Vary] Palindrome Cuts With Minimum Piece Length (LeetCode 132)
<!-- id: dp29-cuts-min-piece-length -->

**Approach.**
The first table `pal[i][j]` is true when `s[i..j]` is a palindrome. Equal end characters make the range a palindrome when the inner range is empty, has one character or is itself a palindrome. The second table `pieces[j]` is the fewest pieces that cover the first `j` characters, with a large marker for a prefix that cannot be covered. The empty prefix needs 0 pieces. For each `j`, the loop tries each start `i` of the last piece and accepts it when `pal[i][j - 1]` is true and the piece length `j - i` is at least `minLen` and `pieces[i]` is reachable.

The answer is `pieces[n] - 1`, which counts cuts and not pieces, or -1 when the marker remains. The invariant is that `pieces[j]` is final when a longer prefix reads it, and the palindrome table is complete before the prefix loop starts.

**Complexity.**
- **Time** is O(n^2), because the palindrome table and the prefix loop each visit about n^2 / 2 pairs with constant work.
- **Space** is O(n^2) for the palindrome table and O(n) for the prefix array.

```java run
import java.util.*;

public final class Dp29CutsMinPieceLength {
    /**
     * Returns the fewest cuts so every piece is a palindrome of at least minLen characters, or -1.
     * Time: O(n^2). Space: O(n^2).
     * Invariant: pieces[j] is final before any longer prefix reads it.
     */
    static int minCuts(String s, int minLen) {
        // n is the number of characters.
        int n = s.length();
        // pal[i][j] is true when s[i..j] is a palindrome.
        boolean[][] pal = new boolean[n][n];
        // Start indexes run from the right so that the inner range is final first.
        for (int i = n - 1; i >= 0; i--) {
            for (int j = i; j < n; j++) {
                // Equal ends make a palindrome when the inner range is short or already a palindrome.
                pal[i][j] = s.charAt(i) == s.charAt(j) && (j - i < 2 || pal[i + 1][j - 1]);
            }
        }
        // INF marks a prefix that has no valid cover.
        final int INF = Integer.MAX_VALUE / 2;
        int[] pieces = new int[n + 1];
        // The empty prefix needs 0 pieces.
        Arrays.fill(pieces, INF);
        pieces[0] = 0;
        // j is the prefix length, and the last piece is s[i..j - 1].
        for (int j = 1; j <= n; j++) {
            for (int i = 0; i < j; i++) {
                // The piece must be long enough, a palindrome, and attach to a reachable prefix.
                if (j - i >= minLen && pal[i][j - 1] && pieces[i] < INF) {
                    pieces[j] = Math.min(pieces[j], pieces[i] + 1);
                }
            }
        }
        // A cover of p pieces uses p - 1 cuts.
        return pieces[n] >= INF ? -1 : pieces[n] - 1;
    }

    /** Oracle: tries every subset of the n - 1 gaps as cuts. */
    static int oracle(String s, int minLen) {
        int n = s.length();
        int best = -1;
        for (int mask = 0; mask < (1 << (n - 1)); mask++) {
            int start = 0;
            boolean ok = true;
            int cuts = Integer.bitCount(mask);
            for (int i = 0; i < n && ok; i++) {
                // A piece ends at index i when a cut follows it or the string ends.
                if (i == n - 1 || (mask >> i & 1) == 1) {
                    String piece = s.substring(start, i + 1);
                    ok = piece.length() >= minLen && piece.contentEquals(new StringBuilder(piece).reverse());
                    start = i + 1;
                }
            }
            if (ok && (best < 0 || cuts < best)) best = cuts;
        }
        return best;
    }

    public static void main(String[] args) {
        // The examples of the exercise, including the impossible case.
        if (minCuts("aaacbcaa", 2) != 2) throw new AssertionError("ex1");
        if (minCuts("aaacbcaa", 1) != 1) throw new AssertionError("ex1 floor 1");
        if (minCuts("abacabb", 2) != -1) throw new AssertionError("ex2");
        // A whole palindrome needs 0 cuts, and a single character fails a floor of 2.
        if (minCuts("racecar", 1) != 0) throw new AssertionError("whole");
        if (minCuts("a", 1) != 0) throw new AssertionError("single");
        if (minCuts("a", 1 + 1) != -1) throw new AssertionError("single floor");
        // Integer.MAX_VALUE / 2 plus 1 does not overflow, so INF can be extended safely.
        if (Integer.MAX_VALUE / 2 + 1 < 0) throw new AssertionError("overflow");
        // Random strings and floors against the cut-subset oracle.
        Random rnd = new Random(2902);
        for (int t = 0; t < 1500; t++) {
            int n = 1 + rnd.nextInt(10);
            StringBuilder b = new StringBuilder();
            for (int i = 0; i < n; i++) b.append((char) ('a' + rnd.nextInt(2)));
            String s = b.toString();
            int floor = 1 + rnd.nextInt(n);
            if (minCuts(s, floor) != oracle(s, floor)) throw new AssertionError("random " + t + " " + s + " " + floor);
        }
    }
}
```

#### Solution: [Boundary] Burst Balloons With Given Outer Values (LeetCode 312)
<!-- id: dp29-burst-outer-values -->

**Approach.**
The method copies `nums` into an array `a` of length `n + 2` with `leftEdge` at index 0 and `rightEdge` at index `n + 1`. Entry `dp[l][r]` is the best total for bursting every balloon strictly between `l` and `r` while positions `l` and `r` stay. The balloon `k` burst last inside the range has neighbours `a[l]` and `a[r]`, so it earns `a[l] * a[k] * a[r]`. Before that, the balloons between `l` and `k` and between `k` and `r` were burst independently, which gives `dp[l][k] + dp[k][r]`.

Ranges with a larger gap read only ranges with a smaller gap, so the loops run by increasing gap. Ranges with gap 1 hold no balloon and stay 0. With an empty array the gap loop does not run, and the answer is 0. The edges are separate from the values, so an edge of 0 makes every product at that side 0 without any special case.

**Complexity.**
- **Time** is O(n^3), because O(n^2) ranges try up to n last balloons each.
- **Space** is O(n^2) for the table.

```java run
import java.util.*;

public final class Dp29BurstOuterValues {
    /**
     * Returns the largest total from bursting every balloon, with the given outside values.
     * Time: O(n^3). Space: O(n^2).
     * Invariant: dp[l][r] is final before any wider range reads it.
     */
    static int maxCoins(int[] nums, int leftEdge, int rightEdge) {
        // n is the number of balloons, and the copy leaves the input unchanged.
        int n = nums.length;
        int[] a = new int[n + 2];
        // The two edge cells hold the outside values.
        a[0] = leftEdge;
        a[n + 1] = rightEdge;
        for (int i = 0; i < n; i++) a[i + 1] = nums[i];
        int[][] dp = new int[n + 2][n + 2];
        // The gap r - l grows, so both parts of a split are final when read.
        for (int gap = 2; gap <= n + 1; gap++) {
            for (int l = 0; l + gap <= n + 1; l++) {
                int r = l + gap;
                // k is the balloon burst last inside (l, r), so its neighbours are a[l] and a[r].
                for (int k = l + 1; k < r; k++) {
                    int total = a[l] * a[k] * a[r] + dp[l][k] + dp[k][r];
                    if (total > dp[l][r]) dp[l][r] = total;
                }
            }
        }
        // The widest range spans both edges.
        return dp[0][n + 1];
    }

    /** Oracle: tries every burst order with recursion on the remaining balloons. */
    static int oracle(List<Integer> rest, int left, int right) {
        if (rest.isEmpty()) return 0;
        int best = 0;
        for (int i = 0; i < rest.size(); i++) {
            int l = i == 0 ? left : rest.get(i - 1);
            int r = i == rest.size() - 1 ? right : rest.get(i + 1);
            List<Integer> next = new ArrayList<>(rest);
            next.remove(i);
            best = Math.max(best, l * rest.get(i) * r + oracle(next, left, right));
        }
        return best;
    }

    public static void main(String[] args) {
        // The examples of the exercise.
        if (maxCoins(new int[]{2, 4, 3}, 5, 2) != 130) throw new AssertionError("ex1");
        if (maxCoins(new int[]{2, 4, 3}, 0, 0) != 24) throw new AssertionError("ex2");
        // The empty array gives 0, and one balloon earns edge * value * edge.
        if (maxCoins(new int[]{}, 5, 5) != 0) throw new AssertionError("empty");
        if (maxCoins(new int[]{7}, 3, 4) != 84) throw new AssertionError("single");
        // The input array stays unchanged.
        int[] keep = {2, 4, 3};
        maxCoins(keep, 1, 1);
        if (!Arrays.equals(keep, new int[]{2, 4, 3})) throw new AssertionError("input changed");
        // The largest allowed total stays inside int range: 300 balloons of 100 with edges of 100.
        long bound = 300L * 100 * 100 * 100;
        if (bound > Integer.MAX_VALUE) throw new AssertionError("overflow bound");
        // Random arrays and edges against the order oracle.
        Random rnd = new Random(2903);
        for (int t = 0; t < 600; t++) {
            int n = rnd.nextInt(7);
            int[] v = new int[n];
            List<Integer> list = new ArrayList<>();
            for (int i = 0; i < n; i++) {
                v[i] = rnd.nextInt(6);
                list.add(v[i]);
            }
            int le = rnd.nextInt(6);
            int re = rnd.nextInt(6);
            if (maxCoins(v, le, re) != oracle(list, le, re)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Recognize] Largest Number Of Equal Sum Groups (LeetCode 698)
<!-- id: dp29-equal-sum-groups -->

**Approach.**
For a fixed group count `k`, the total must divide by `k`, and the share `target = total / k` must be at least the largest entry. The search then walks over subsets. Entry `fill[mask]` is the sum of the used items modulo `target` when the used items can be arranged into complete groups plus one open group, and -1 otherwise. The empty set has fill 0. From a reachable mask, adding an unused item is allowed when the open group stays at or below `target`. The new fill is the sum modulo `target`, so a closed group wraps to 0.

The fill of the open group depends only on the sum of the mask, so the search never records which group holds which item. That removes the symmetric work of trying equal groups in different orders. The set of all items works when `fill[full] == 0`. The method tries `k` from the item count down to 2, returns the first that works, and returns 1 otherwise. The invariant is that `fill[mask]` is final before a larger mask reads it, because adding a bit always raises the mask value.

**Complexity.**
- **Time** is O(d * 2^n * n) for n items and d divisors of the total that reach the search, because each mask tries each unused item.
- **Space** is O(2^n) for the fill array, reused for each divisor.

```java run
import java.util.*;

public final class Dp29EqualSumGroups {
    /**
     * Returns the largest k so nums splits into k non-empty groups of equal sum.
     * Time: O(d * 2^n * n). Space: O(2^n).
     * Invariant: fill[mask] depends on the mask alone and is final before a larger mask reads it.
     */
    static int largestGroupCount(int[] nums) {
        // n is the item count and total is the sum of all items.
        int n = nums.length;
        int total = 0;
        int max = 0;
        for (int v : nums) {
            total += v;
            max = Math.max(max, v);
        }
        // fill is reused across divisors; its size is 2^n.
        int[] fill = new int[1 << n];
        // Try the largest group count first, so the first success is the answer.
        for (int k = n; k >= 2; k--) {
            // The total must divide into k shares, and no item may exceed a share.
            if (total % k != 0 || total / k < max) continue;
            int target = total / k;
            Arrays.fill(fill, -1);
            fill[0] = 0;
            // Masks grow with each added bit, so a mask is final before any superset reads it.
            for (int mask = 0; mask < (1 << n); mask++) {
                if (fill[mask] < 0) continue;
                for (int i = 0; i < n; i++) {
                    // Skip items already used.
                    if ((mask >> i & 1) == 1) continue;
                    // The open group must stay within the target.
                    if (fill[mask] + nums[i] > target) continue;
                    // The modulo wraps a completed group to 0.
                    fill[mask | 1 << i] = (fill[mask] + nums[i]) % target;
                }
            }
            // A reachable full mask with fill 0 means every group closed exactly.
            if (fill[(1 << n) - 1] == 0) return k;
        }
        // One group holding every item always works.
        return 1;
    }

    /** Oracle: assigns every item to a group index with plain recursion for each k. */
    static boolean oracleSplit(int[] nums, int idx, int[] load, int target) {
        if (idx == nums.length) {
            for (int x : load) if (x != target) return false;
            return true;
        }
        for (int g = 0; g < load.length; g++) {
            load[g] += nums[idx];
            boolean ok = oracleSplit(nums, idx + 1, load, target);
            load[g] -= nums[idx];
            if (ok) return true;
        }
        return false;
    }

    static int oracle(int[] nums) {
        int total = Arrays.stream(nums).sum();
        for (int k = nums.length; k >= 1; k--) {
            if (total % k == 0 && oracleSplit(nums, 0, new int[k], total / k)) return k;
        }
        return 1;
    }

    public static void main(String[] args) {
        // The examples of the exercise.
        if (largestGroupCount(new int[]{1, 2, 3, 4, 5, 6}) != 3) throw new AssertionError("ex1");
        if (largestGroupCount(new int[]{7, 7, 2, 2, 3, 3}) != 2) throw new AssertionError("ex2");
        // One item, equal items and a total with no usable divisor.
        if (largestGroupCount(new int[]{5}) != 1) throw new AssertionError("single");
        if (largestGroupCount(new int[]{3, 3, 3, 3}) != 4) throw new AssertionError("equal");
        if (largestGroupCount(new int[]{1, 2, 4}) != 1) throw new AssertionError("prime total");
        // Operator precedence: 1 << n is evaluated before the bitwise or in mask | 1 << i.
        if ((5 | 1 << 1) != 7) throw new AssertionError("precedence");
        // Random arrays against the assignment oracle.
        Random rnd = new Random(2904);
        for (int t = 0; t < 400; t++) {
            int n = 1 + rnd.nextInt(7);
            int[] v = new int[n];
            for (int i = 0; i < n; i++) v[i] = 1 + rnd.nextInt(5);
            int[] copy = v.clone();
            if (largestGroupCount(v) != oracle(copy)) throw new AssertionError("random " + t + " " + Arrays.toString(v));
            if (!Arrays.equals(v, copy)) throw new AssertionError("input changed");
        }
    }
}
```
