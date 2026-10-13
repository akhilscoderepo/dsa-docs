<!-- solutions-for: 28-dynamic-programming-state-machines-and-sequences -->
### Solutions For Palindromic Sequences

#### Solution: [Build] Length One And Two (Author exercise)
<!-- id: ps-length-one-and-two -->

**Approach.**
The table has `n` rows and `n` columns, and entry `[left][right]` describes the interval from `left` to `right`. An interval with one character is a palindrome by itself, so its entry is 1. An interval with two characters stores 2 when the characters match, because both form a palindrome. When they differ, only one of them can stay, so the entry is the larger of the two single-character entries, which is 1.

The method visits only intervals of length 1 and 2 and leaves every other entry at 0. The invariant is that each stored entry equals the true longest palindromic subsequence of its interval. These entries read no inner interval, so they are the base cases that every longer interval relies on.

**Complexity.**
- **Time** is O(n) for the loop over start positions, plus O(n^2) to allocate the zero-filled table.
- **Space** is O(n^2) for the returned table, and `s` stays unchanged.

```java run
import java.util.*;

public final class PsLengthOneAndTwo {
    /**
     * Returns a table whose length-1 and length-2 intervals hold their best palindromic subsequence.
     * Time: O(n^2) including allocation. Space: O(n^2).
     * Invariant: every nonzero entry equals the true answer for its interval.
     */
    static int[][] baseCases(String s) {
        int n = s.length();
        // Java allocates the table with every entry 0, which costs n * n.
        int[][] dp = new int[n][n];
        // One pass over the start positions fills both base lengths.
        for (int left = 0; left < n; left++) {
            // A single character is a palindrome of length 1.
            dp[left][left] = 1;
            // A pair exists only when a next character is present.
            if (left + 1 < n) {
                // Matching characters keep both, and different characters keep one.
                dp[left][left + 1] = s.charAt(left) == s.charAt(left + 1) ? 2 : 1;
            }
        }
        // The table is returned with every longer interval still 0.
        return dp;
    }

    /** Oracle: tests every subset of the interval for a palindrome. */
    static int oracle(String s, int left, int right) {
        int len = right - left + 1;
        int best = 0;
        for (int mask = 0; mask < (1 << len); mask++) {
            StringBuilder sb = new StringBuilder();
            for (int i = 0; i < len; i++) if ((mask >> i & 1) == 1) sb.append(s.charAt(left + i));
            String t = sb.toString();
            if (t.equals(sb.reverse().toString())) best = Math.max(best, t.length());
        }
        return best;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!Arrays.deepEquals(baseCases("aab"), new int[][] {{1, 2, 0}, {0, 1, 1}, {0, 0, 1}})) throw new AssertionError("ex1");
        if (!Arrays.deepEquals(baseCases("z"), new int[][] {{1}})) throw new AssertionError("ex2");
        // The empty string returns an empty array.
        if (baseCases("").length != 0) throw new AssertionError("empty");
        // Random strings against the subset oracle, with zeros outside lengths 1 and 2.
        Random rnd = new Random(2806);
        for (int t = 0; t < 1000; t++) {
            int n = rnd.nextInt(9);
            StringBuilder sb = new StringBuilder();
            for (int i = 0; i < n; i++) sb.append((char) ('a' + rnd.nextInt(3)));
            String s = sb.toString();
            int[][] dp = baseCases(s);
            for (int l = 0; l < n; l++) {
                for (int r = 0; r < n; r++) {
                    int expected = (r >= l && r - l <= 1) ? oracle(s, l, r) : 0;
                    if (dp[l][r] != expected) throw new AssertionError("random " + t + " " + l + " " + r);
                }
            }
        }
    }
}
```

#### Solution: [Vary] Longest Palindromic Subsequence (LeetCode 516)
<!-- id: ps-longest-palindromic-subsequence -->

**Approach.**
Entry `dp[left][right]` is the longest palindromic subsequence inside the closed interval from `left` to `right`. A single character stores 1. When the two endpoints are equal, some best subsequence keeps both, so the entry is the inner entry plus 2, with an empty inner range counted as 0. When the endpoints differ, at least one is skipped, and the entry is the larger of the two entries that drop one endpoint.

Every entry reads only shorter intervals, so the loops run over increasing length and, inside one length, over increasing `left`. The invariant is that every interval shorter than the current length is final. The answer is the entry for the whole string. The recursion from the lesson makes 15 calls on `abcd`, and the test counts them.

**Complexity.**
- **Time** is O(n^2), because the table has n * (n + 1) / 2 intervals and each takes at most two reads.
- **Space** is O(n^2) for the table, and `s` stays unchanged.

```java run
import java.util.*;

public final class PsLongestPalindromicSubsequence {
    /**
     * Returns the length of the longest palindromic subsequence of s.
     * Time: O(n^2). Space: O(n^2).
     * Invariant: all intervals shorter than the current length are final.
     */
    static int longest(String s) {
        int n = s.length();
        // The table has one entry for each pair of ends, which costs n * n memory.
        int[][] dp = new int[n][n];
        // Length is the outer loop so that shorter intervals finish first.
        for (int length = 1; length <= n; length++) {
            // Left runs over every start whose interval fits in the string.
            for (int left = 0; left + length - 1 < n; left++) {
                // Right is fixed by left and length.
                int right = left + length - 1;
                if (length == 1) {
                    // One character is a palindrome of length 1.
                    dp[left][right] = 1;
                } else if (s.charAt(left) == s.charAt(right)) {
                    // Equal endpoints add 2 to the inner interval, which is empty for length 2.
                    int inner = length == 2 ? 0 : dp[left + 1][right - 1];
                    dp[left][right] = inner + 2;
                } else {
                    // Different endpoints skip one end, and the better skip wins.
                    dp[left][right] = Math.max(dp[left + 1][right], dp[left][right - 1]);
                }
            }
        }
        // The whole string is the interval from 0 to n - 1, and the empty string returns 0.
        return n == 0 ? 0 : dp[0][n - 1];
    }

    static int calls;

    /** The lesson's recursion, with a call counter. */
    static int slow(String s, int left, int right) {
        calls++;
        if (left > right) return 0;
        if (left == right) return 1;
        if (s.charAt(left) == s.charAt(right)) return 2 + slow(s, left + 1, right - 1);
        return Math.max(slow(s, left + 1, right), slow(s, left, right - 1));
    }

    /** Oracle: tests every subset of characters for a palindrome. */
    static int oracle(String s) {
        int n = s.length();
        int best = 0;
        for (int mask = 0; mask < (1 << n); mask++) {
            StringBuilder sb = new StringBuilder();
            for (int i = 0; i < n; i++) if ((mask >> i & 1) == 1) sb.append(s.charAt(i));
            String t = sb.toString();
            if (t.equals(sb.reverse().toString())) best = Math.max(best, t.length());
        }
        return best;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (longest("bbbab") != 4) throw new AssertionError("ex1");
        if (longest("cbbd") != 2) throw new AssertionError("ex2");
        // The longest palindromic substring of bbbab is bbb, shorter than the subsequence bbbb.
        if (longest("bbbab") <= 3) throw new AssertionError("substring false friend");
        // The recursion makes 15 calls on abcd and 2^n - 1 calls for n distinct letters.
        calls = 0;
        slow("abcd", 0, 3);
        if (calls != 15) throw new AssertionError("calls");
        // Small cases: one character, one repeated letter, and the empty string.
        if (longest("q") != 1) throw new AssertionError("one");
        if (longest("aaaa") != 4) throw new AssertionError("repeat");
        if (longest("") != 0) throw new AssertionError("empty");
        // Random strings against the subset oracle and the recursion.
        Random rnd = new Random(2816);
        for (int t = 0; t < 1500; t++) {
            int n = rnd.nextInt(13);
            StringBuilder sb = new StringBuilder();
            for (int i = 0; i < n; i++) sb.append((char) ('a' + rnd.nextInt(3)));
            String s = sb.toString();
            if (longest(s) != oracle(s)) throw new AssertionError("random " + t);
            if (n > 0 && longest(s) != slow(s, 0, n - 1)) throw new AssertionError("slow " + t);
        }
    }
}
```

#### Solution: [Boundary] Fill By Increasing Length (Author exercise)
<!-- id: ps-fill-by-increasing-length -->

**Approach.**
In the fill order, every interval of length L comes after all intervals shorter than L. A string of length `n` has `n - len + 1` intervals of length `len`, so the intervals shorter than the target length `L` occupy the first sum of `n - len + 1` for `len` from 1 to `L - 1` positions. Inside length `L`, the intervals are ordered by `left`, so the target sits `left` positions after that block.

The invariant is that the position of an interval is larger than the position of every interval it reads, because each read is a strictly shorter interval. The test builds the list explicitly and checks both the position formula and that property.

**Complexity.**
- **Time** is O(L), because the loop adds one term for each shorter length.
- **Space** is O(1), since the method keeps one running total.

```java run
import java.util.*;

public final class PsFillByIncreasingLength {
    /**
     * Returns the position of interval (left, right) in the increasing-length fill order.
     * Time: O(right - left). Space: O(1).
     * Invariant: the count skips exactly the intervals that are shorter than the target.
     */
    static int position(int n, int left, int right) {
        // Length of the target interval.
        int target = right - left + 1;
        int before = 0;
        // Each shorter length contributes all of its n - len + 1 intervals.
        for (int len = 1; len < target; len++) {
            before += n - len + 1;
        }
        // Inside the target length, the intervals are ordered by left.
        return before + left;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (position(5, 1, 2) != 6) throw new AssertionError("ex1");
        if (position(5, 0, 4) != 14) throw new AssertionError("ex2");
        // The first interval has position 0, and the last one has position n(n+1)/2 - 1.
        if (position(1, 0, 0) != 0) throw new AssertionError("single");
        if (position(1000, 0, 999) != 1000 * 1001 / 2 - 1) throw new AssertionError("last");
        // For every n up to 30, the formula matches an explicit list and every read comes earlier.
        for (int n = 1; n <= 30; n++) {
            List<int[]> order = new ArrayList<>();
            for (int len = 1; len <= n; len++) for (int l = 0; l + len - 1 < n; l++) order.add(new int[] {l, l + len - 1});
            for (int i = 0; i < order.size(); i++) {
                int l = order.get(i)[0];
                int r = order.get(i)[1];
                if (position(n, l, r) != i) throw new AssertionError("position " + n + " " + l + " " + r);
                // The three intervals that an entry reads must have smaller positions.
                if (r > l) {
                    if (position(n, l + 1, r) >= i || position(n, l, r - 1) >= i) throw new AssertionError("order");
                    if (r - l >= 2 && position(n, l + 1, r - 1) >= i) throw new AssertionError("inner");
                }
            }
        }
    }
}
```

#### Solution: [Recognize] Minimum Insertion Steps To Make A String Palindrome (LeetCode 1312)
<!-- id: ps-minimum-insertions-palindrome -->

**Approach.**
Characters of `s` that are never moved keep their order, so they form a subsequence that must already be a palindrome in the result. Every other character needs one inserted partner on the opposite side. The cost is therefore `n` minus the length of the kept palindrome, and keeping the longest one gives the smallest cost.

The method computes that longest palindromic subsequence with the interval table from the lesson, filled by increasing length, and returns `n` minus its value. The invariant is that each entry is final before a longer interval reads it. The test compares the result with a separate recurrence that counts insertions directly.

**Complexity.**
- **Time** is O(n^2), because the table has n * (n + 1) / 2 intervals with at most two reads each.
- **Space** is O(n^2) for the table, and `s` stays unchanged.

```java run
import java.util.*;

public final class PsMinimumInsertionsPalindrome {
    /**
     * Returns the fewest insertions that make s a palindrome.
     * Time: O(n^2). Space: O(n^2).
     * Invariant: dp entries of shorter intervals are final before longer ones are read.
     */
    static int minInsertions(String s) {
        int n = s.length();
        // The table holds the longest palindromic subsequence of each interval.
        int[][] dp = new int[n][n];
        // Increasing length guarantees the inner intervals are ready.
        for (int length = 1; length <= n; length++) {
            for (int left = 0; left + length - 1 < n; left++) {
                int right = left + length - 1;
                if (length == 1) {
                    // A single character needs no partner.
                    dp[left][right] = 1;
                } else if (s.charAt(left) == s.charAt(right)) {
                    // Matching ends extend the inner palindrome by 2.
                    dp[left][right] = (length == 2 ? 0 : dp[left + 1][right - 1]) + 2;
                } else {
                    // Mismatched ends skip the better end.
                    dp[left][right] = Math.max(dp[left + 1][right], dp[left][right - 1]);
                }
            }
        }
        // Every character outside the kept palindrome needs one inserted partner.
        return n - dp[0][n - 1];
    }

    /** Oracle: a direct recurrence on insertions, memoised by interval. */
    static int direct(String s, int left, int right, int[][] memo) {
        if (left >= right) return 0;
        if (memo[left][right] >= 0) return memo[left][right];
        int result;
        if (s.charAt(left) == s.charAt(right)) {
            result = direct(s, left + 1, right - 1, memo);
        } else {
            result = 1 + Math.min(direct(s, left + 1, right, memo), direct(s, left, right - 1, memo));
        }
        memo[left][right] = result;
        return result;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (minInsertions("zzazz") != 0) throw new AssertionError("ex1");
        if (minInsertions("mbadm") != 2) throw new AssertionError("ex2");
        // One character needs no insertion, and two different characters need one.
        if (minInsertions("q") != 0) throw new AssertionError("one");
        if (minInsertions("qr") != 1) throw new AssertionError("two");
        // Random strings against the direct insertion recurrence.
        Random rnd = new Random(2826);
        for (int t = 0; t < 2000; t++) {
            int n = 1 + rnd.nextInt(14);
            StringBuilder sb = new StringBuilder();
            for (int i = 0; i < n; i++) sb.append((char) ('a' + rnd.nextInt(4)));
            String s = sb.toString();
            int[][] memo = new int[n][n];
            for (int[] row : memo) Arrays.fill(row, -1);
            if (minInsertions(s) != direct(s, 0, n - 1, memo)) throw new AssertionError("random " + t);
        }
    }
}
```
