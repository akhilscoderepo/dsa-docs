<!-- solutions-for: 28-dynamic-programming-state-machines-and-sequences -->
### Solutions For Common Subsequences

#### Solution: [Build] LCS Of Short Prefixes (Author exercise)
<!-- id: cs-short-prefixes -->

**Approach.**
The table `dp` has `i + 1` rows and `j + 1` columns. Entry `dp[x][y]` is the longest common subsequence length of the first `x` characters of `a` and the first `y` characters of `b`. Row 0 and column 0 stay 0 because an empty prefix shares nothing. For `x` and `y` from 1, equal last characters give the diagonal entry plus 1, and different last characters give the larger of the entry above and the entry to the left.

The invariant is that every entry read by `(x, y)` has a smaller `x`, a smaller `y`, or both, so it is final when read. The method never looks at characters beyond index `i - 1` of `a` or `j - 1` of `b`.

**Complexity.**
- **Time** is O(i * j), because each of the `i * j` inner entries costs one comparison and at most two reads.
- **Space** is O(i * j) for the table, and the strings stay unchanged.

```java run
import java.util.*;

public final class CsShortPrefixes {
    /**
     * Returns the longest common subsequence length of a[0..i) and b[0..j).
     * Time: O(i * j). Space: O(i * j).
     * Invariant: each entry is final before a later entry reads it.
     */
    static int prefixLength(String a, String b, int i, int j) {
        // Java fills the new array with zeros, which sets row 0 and column 0 for empty prefixes.
        int[][] dp = new int[i + 1][j + 1];
        // Row x covers the first x characters of a.
        for (int x = 1; x <= i; x++) {
            // Column y covers the first y characters of b.
            for (int y = 1; y <= j; y++) {
                // Equal last characters extend the best answer of the diagonal entry.
                if (a.charAt(x - 1) == b.charAt(y - 1)) {
                    dp[x][y] = dp[x - 1][y - 1] + 1;
                } else {
                    // Different last characters drop one of them and keep the larger result.
                    dp[x][y] = Math.max(dp[x - 1][y], dp[x][y - 1]);
                }
            }
        }
        // The corner entry describes the requested prefix pair.
        return dp[i][j];
    }

    /** Oracle: tries every subsequence of the prefix of a and checks it against the prefix of b. */
    static int oracle(String a, String b, int i, int j) {
        int best = 0;
        for (int mask = 0; mask < (1 << i); mask++) {
            StringBuilder s = new StringBuilder();
            for (int k = 0; k < i; k++) if ((mask >> k & 1) == 1) s.append(a.charAt(k));
            int p = 0;
            for (int k = 0; k < j && p < s.length(); k++) if (b.charAt(k) == s.charAt(p)) p++;
            if (p == s.length()) best = Math.max(best, s.length());
        }
        return best;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (prefixLength("bacd", "acdb", 3, 4) != 2) throw new AssertionError("ex1");
        if (prefixLength("bacd", "acdb", 1, 2) != 0) throw new AssertionError("ex2");
        // Empty prefixes give 0, and the full strings give the lesson answer 3.
        if (prefixLength("bacd", "acdb", 0, 4) != 0) throw new AssertionError("empty i");
        if (prefixLength("bacd", "acdb", 4, 0) != 0) throw new AssertionError("empty j");
        if (prefixLength("bacd", "acdb", 4, 4) != 3) throw new AssertionError("full");
        // A new int array holds zeros, and String.charAt reads index i - 1 for a prefix of length i.
        int[][] fresh = new int[3][3];
        if (fresh[1][2] != 0) throw new AssertionError("zero fill");
        if ("ab".charAt(1) != 'b') throw new AssertionError("charAt");
        // Random prefixes against the subsequence oracle.
        Random rnd = new Random(2804);
        for (int t = 0; t < 2000; t++) {
            String a = word(rnd, rnd.nextInt(9));
            String b = word(rnd, rnd.nextInt(9));
            int i = rnd.nextInt(a.length() + 1);
            int j = rnd.nextInt(b.length() + 1);
            if (prefixLength(a, b, i, j) != oracle(a, b, i, j)) throw new AssertionError("random " + t);
        }
    }

    static String word(Random rnd, int len) {
        StringBuilder s = new StringBuilder();
        for (int k = 0; k < len; k++) s.append((char) ('a' + rnd.nextInt(3)));
        return s.toString();
    }
}
```

#### Solution: [Vary] Longest Common Subsequence (LeetCode 1143)
<!-- id: cs-longest-common-subsequence -->

**Approach.**
The full table has one row for each prefix length of `text1` and one column for each prefix length of `text2`. The loops visit rows from top to bottom and columns from left to right. An equal pair of last characters reads the diagonal entry and adds 1. A different pair reads the entries above and to the left and keeps the larger.

The invariant is that entry `(i, j)` is final when the loops finish it, and its three inputs were finished earlier. The answer is the bottom-right entry. Each text has at least one character here, but the code also handles an empty text, because a loop with no iterations leaves the zeros.

**Complexity.**
- **Time** is O(m * n) for strings of length m and n, because each entry costs constant work.
- **Space** is O(m * n) for the table, and the strings stay unchanged.

```java run
import java.util.*;

public final class CsLongestCommonSubsequence {
    /**
     * Returns the length of the longest common subsequence of two strings.
     * Time: O(m * n). Space: O(m * n).
     * Invariant: entry (i, j) is final once its row pass reaches column j.
     */
    static int lcs(String text1, String text2) {
        // m and n are the string lengths, so the table has (m + 1) * (n + 1) entries.
        int m = text1.length();
        int n = text2.length();
        int[][] dp = new int[m + 1][n + 1];
        // Rows run over the prefix lengths of text1, which costs m passes.
        for (int i = 1; i <= m; i++) {
            // Columns run over the prefix lengths of text2, which costs n steps per row.
            for (int j = 1; j <= n; j++) {
                // Equal last characters join the diagonal subsequence.
                if (text1.charAt(i - 1) == text2.charAt(j - 1)) {
                    dp[i][j] = dp[i - 1][j - 1] + 1;
                } else {
                    // Otherwise one last character is unused, so the better neighbour wins.
                    dp[i][j] = Math.max(dp[i - 1][j], dp[i][j - 1]);
                }
            }
        }
        // The corner entry covers both full strings.
        return dp[m][n];
    }

    /** Oracle: tries every subsequence of a and tests it as a subsequence of b. */
    static int oracle(String a, String b) {
        int best = 0;
        for (int mask = 0; mask < (1 << a.length()); mask++) {
            StringBuilder s = new StringBuilder();
            for (int k = 0; k < a.length(); k++) if ((mask >> k & 1) == 1) s.append(a.charAt(k));
            int p = 0;
            for (int k = 0; k < b.length() && p < s.length(); k++) if (b.charAt(k) == s.charAt(p)) p++;
            if (p == s.length()) best = Math.max(best, s.length());
        }
        return best;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (lcs("abcd", "xaybzc") != 3) throw new AssertionError("ex1");
        if (lcs("programming", "gaming") != 6) throw new AssertionError("ex2");
        // The lesson pair, no shared character, equal strings and reversed order.
        if (lcs("bacd", "acdb") != 3) throw new AssertionError("lesson");
        if (lcs("ab", "cd") != 0) throw new AssertionError("disjoint");
        if (lcs("abc", "abc") != 3) throw new AssertionError("equal");
        if (lcs("ab", "ba") != 1) throw new AssertionError("reversed");
        // An empty text gives 0.
        if (lcs("", "abc") != 0) throw new AssertionError("empty");
        // Strings are immutable, so the inputs stay the same objects with the same content.
        String s = "abc";
        lcs(s, "bca");
        if (!s.equals("abc")) throw new AssertionError("mutated");
        // Random inputs against the subsequence oracle.
        Random rnd = new Random(2814);
        for (int t = 0; t < 2000; t++) {
            String a = word(rnd, rnd.nextInt(10));
            String b = word(rnd, rnd.nextInt(10));
            if (lcs(a, b) != oracle(a, b)) throw new AssertionError("random " + t);
        }
    }

    static String word(Random rnd, int len) {
        StringBuilder s = new StringBuilder();
        for (int k = 0; k < len; k++) s.append((char) ('a' + rnd.nextInt(3)));
        return s.toString();
    }
}
```

#### Solution: [Boundary] Empty Prefix (Author exercise)
<!-- id: cs-empty-prefix -->

**Approach.**
The table has `a.length() + 1` rows and `b.length() + 1` columns. Row 0 and column 0 describe an empty prefix, so each of those entries is 0 and the method counts them without any comparison. The loops then fill the remaining entries with the usual rule, and the method counts each entry that equals 0.

The invariant is that every entry is final before it is counted. With an empty string, the inner loops never run, so every entry is a zero-row or zero-column entry, and the count is the full table size. Counting only the interior would miss these entries.

**Complexity.**
- **Time** is O(m * n) for lengths m and n, because the table has (m + 1) * (n + 1) entries and each costs constant work.
- **Space** is O(m * n) for the table, and the strings stay unchanged.

```java run
import java.util.*;

public final class CsEmptyPrefix {
    /**
     * Counts prefix pairs whose longest common subsequence has length 0.
     * Time: O(m * n). Space: O(m * n).
     * Invariant: every entry is final before the count reads it.
     */
    static int zeroPairs(String a, String b) {
        int m = a.length();
        int n = b.length();
        // The new table holds zeros, which is the correct value for row 0 and column 0.
        int[][] dp = new int[m + 1][n + 1];
        // Rows from 1 skip the zero row.
        for (int i = 1; i <= m; i++) {
            // Columns from 1 skip the zero column.
            for (int j = 1; j <= n; j++) {
                // Equal last characters extend the diagonal entry, others keep the better neighbour.
                dp[i][j] = a.charAt(i - 1) == b.charAt(j - 1)
                        ? dp[i - 1][j - 1] + 1
                        : Math.max(dp[i - 1][j], dp[i][j - 1]);
            }
        }
        int zeros = 0;
        // The count visits every entry, including row 0 and column 0.
        for (int i = 0; i <= m; i++) {
            for (int j = 0; j <= n; j++) {
                // An entry equal to 0 is a prefix pair with no shared character.
                if (dp[i][j] == 0) zeros++;
            }
        }
        // The total is returned as an int.
        return zeros;
    }

    /** Oracle: for each prefix pair, tries every subsequence of the a prefix and checks the b prefix. */
    static int oracle(String a, String b) {
        int zeros = 0;
        for (int i = 0; i <= a.length(); i++) {
            for (int j = 0; j <= b.length(); j++) {
                boolean shared = false;
                // A common subsequence of length 1 exists exactly when some character appears in both prefixes.
                for (int x = 0; x < i && !shared; x++) {
                    for (int y = 0; y < j; y++) if (a.charAt(x) == b.charAt(y)) shared = true;
                }
                if (!shared) zeros++;
            }
        }
        return zeros;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (zeroPairs("", "abc") != 4) throw new AssertionError("ex1");
        if (zeroPairs("ab", "ba") != 6) throw new AssertionError("ex2");
        // Both strings empty give one pair, and disjoint strings give every pair.
        if (zeroPairs("", "") != 1) throw new AssertionError("both empty");
        if (zeroPairs("ab", "cd") != 9) throw new AssertionError("disjoint");
        // Equal single characters leave only the zero row and column.
        if (zeroPairs("a", "a") != 3) throw new AssertionError("single");
        // Random inputs against the direct oracle.
        Random rnd = new Random(2824);
        for (int t = 0; t < 2000; t++) {
            String a = word(rnd, rnd.nextInt(8));
            String b = word(rnd, rnd.nextInt(8));
            if (zeroPairs(a, b) != oracle(a, b)) throw new AssertionError("random " + t);
        }
    }

    static String word(Random rnd, int len) {
        StringBuilder s = new StringBuilder();
        for (int k = 0; k < len; k++) s.append((char) ('a' + rnd.nextInt(4)));
        return s.toString();
    }
}
```

#### Solution: [Recognize] Delete Operation For Two Strings (LeetCode 583)
<!-- id: cs-delete-operation -->

**Approach.**
After the deletions, both strings equal one shared string `s`. That string is a subsequence of each input, because deletions keep the order of the remaining characters. A longer `s` means fewer deletions, so the best `s` is a longest common subsequence. The deletions then remove `word1.length() - L` characters from the first string and `word2.length() - L` from the second, where L is the common subsequence length.

The method computes L with the prefix-pair table and returns the two lengths added together minus 2 * L. The invariant of the table is that each entry is final before a later entry reads it. The oracle in the test tries every pair of kept character sets and does not use this formula.

**Complexity.**
- **Time** is O(m * n), because the table dominates and the final formula costs constant work.
- **Space** is O(m * n) for the table, and the strings stay unchanged.

```java run
import java.util.*;

public final class CsDeleteOperation {
    /**
     * Returns the fewest single-character deletions that make two strings equal.
     * Time: O(m * n). Space: O(m * n).
     * Invariant: each table entry is final before a later entry reads it.
     */
    static int minDeletions(String word1, String word2) {
        int m = word1.length();
        int n = word2.length();
        // Zeros in row 0 and column 0 stand for empty prefixes.
        int[][] dp = new int[m + 1][n + 1];
        // Rows cover prefixes of word1.
        for (int i = 1; i <= m; i++) {
            // Columns cover prefixes of word2.
            for (int j = 1; j <= n; j++) {
                // Equal last characters extend the diagonal entry, others keep the better neighbour.
                if (word1.charAt(i - 1) == word2.charAt(j - 1)) {
                    dp[i][j] = dp[i - 1][j - 1] + 1;
                } else {
                    dp[i][j] = Math.max(dp[i - 1][j], dp[i][j - 1]);
                }
            }
        }
        // Everything outside the common subsequence is deleted from one side or the other.
        return m + n - 2 * dp[m][n];
    }

    /** Oracle: tries every pair of kept character sets and keeps the equal pairs with the most characters. */
    static int oracle(String a, String b) {
        int best = Integer.MAX_VALUE;
        for (int ma = 0; ma < (1 << a.length()); ma++) {
            String sa = pick(a, ma);
            for (int mb = 0; mb < (1 << b.length()); mb++) {
                if (sa.equals(pick(b, mb))) {
                    best = Math.min(best, a.length() - sa.length() + b.length() - sa.length());
                }
            }
        }
        return best;
    }

    static String pick(String s, int mask) {
        StringBuilder r = new StringBuilder();
        for (int k = 0; k < s.length(); k++) if ((mask >> k & 1) == 1) r.append(s.charAt(k));
        return r.toString();
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (minDeletions("bacd", "acdb") != 2) throw new AssertionError("ex1");
        if (minDeletions("kitten", "sitting") != 5) throw new AssertionError("ex2");
        // Equal strings need none, disjoint strings delete everything, and empty strings are allowed.
        if (minDeletions("abc", "abc") != 0) throw new AssertionError("equal");
        if (minDeletions("ab", "cd") != 4) throw new AssertionError("disjoint");
        if (minDeletions("x", "") != 1) throw new AssertionError("one empty");
        if (minDeletions("", "") != 0) throw new AssertionError("both empty");
        // Random inputs against the pair-of-subsets oracle.
        Random rnd = new Random(2834);
        for (int t = 0; t < 800; t++) {
            String a = word(rnd, rnd.nextInt(7));
            String b = word(rnd, rnd.nextInt(7));
            if (minDeletions(a, b) != oracle(a, b)) throw new AssertionError("random " + t);
        }
    }

    static String word(Random rnd, int len) {
        StringBuilder s = new StringBuilder();
        for (int k = 0; k < len; k++) s.append((char) ('a' + rnd.nextInt(3)));
        return s.toString();
    }
}
```
