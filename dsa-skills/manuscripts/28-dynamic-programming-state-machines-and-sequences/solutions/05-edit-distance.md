<!-- solutions-for: 28-dynamic-programming-state-machines-and-sequences -->
### Solutions For Edit Distance

#### Solution: [Build] Insert Or Delete Only (Author exercise)
<!-- id: ed-insert-delete-only -->

**Approach.**
The table cell `dp[i][j]` holds the fewest insertions and deletions that turn the first `i` characters of `s` into the first `j` characters of `t`. Column 0 holds `i` deletions and row 0 holds `j` insertions. When the last characters are equal, the cell copies its diagonal neighbor. When they differ, no replacement exists, so the cell adds one to the smaller of the cell above, which stands for a deletion, and the cell on the left, which stands for an insertion.

Each cell reads only cells in an earlier row or an earlier column, so a row-by-row fill makes every read final. The answer is the corner cell.

**Complexity.**
- **Time** is O(m * n), because each of the (m + 1) * (n + 1) cells does at most three reads.
- **Space** is O(m * n) for the table, and the strings are immutable.

```java run
import java.util.*;

public final class EdInsertDeleteOnly {
    /**
     * Returns the fewest insertions and deletions that turn s into t.
     * Time: O(m * n). Space: O(m * n).
     * Invariant: dp[i][j] is exact for the prefixes of lengths i and j, and every read points to a finished cell.
     */
    static int insertDelete(String s, String t) {
        int m = s.length(), n = t.length();
        // One extra row and column hold the empty prefixes.
        int[][] dp = new int[m + 1][n + 1];
        // Turning i characters into nothing takes i deletions.
        for (int i = 0; i <= m; i++) dp[i][0] = i;
        // Building j characters from nothing takes j insertions.
        for (int j = 0; j <= n; j++) dp[0][j] = j;
        // Rows run from top to bottom, so the row above is final.
        for (int i = 1; i <= m; i++) {
            // Columns run left to right, so the left cell is final.
            for (int j = 1; j <= n; j++) {
                if (s.charAt(i - 1) == t.charAt(j - 1)) {
                    // Equal last characters stay paired at no cost.
                    dp[i][j] = dp[i - 1][j - 1];
                } else {
                    // Without replacement, only a deletion or an insertion remains.
                    dp[i][j] = 1 + Math.min(dp[i - 1][j], dp[i][j - 1]);
                }
            }
        }
        // The corner covers both whole strings.
        return dp[m][n];
    }

    /** Oracle: m + n minus twice the longest common subsequence, found by plain recursion. */
    static int oracle(String s, String t) {
        return s.length() + t.length() - 2 * lcs(s, t);
    }

    static int lcs(String a, String b) {
        if (a.isEmpty() || b.isEmpty()) return 0;
        if (a.charAt(0) == b.charAt(0)) return 1 + lcs(a.substring(1), b.substring(1));
        return Math.max(lcs(a.substring(1), b), lcs(a, b.substring(1)));
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (insertDelete("sea", "eat") != 2) throw new AssertionError("ex1");
        if (insertDelete("abc", "xyz") != 6) throw new AssertionError("ex2");
        // Empty strings give the other length, and two empty strings give 0.
        if (insertDelete("", "") != 0) throw new AssertionError("both empty");
        if (insertDelete("abc", "") != 3 || insertDelete("", "ab") != 2) throw new AssertionError("one empty");
        // Replacement is not allowed, so one changed letter costs 2.
        if (insertDelete("cat", "cut") != 2) throw new AssertionError("no replace");
        // Random strings against the oracle.
        Random rnd = new Random(2805);
        for (int tr = 0; tr < 2000; tr++) {
            StringBuilder a = new StringBuilder(), b = new StringBuilder();
            for (int i = rnd.nextInt(8); i > 0; i--) a.append((char) ('a' + rnd.nextInt(3)));
            for (int i = rnd.nextInt(8); i > 0; i--) b.append((char) ('a' + rnd.nextInt(3)));
            if (insertDelete(a.toString(), b.toString()) != oracle(a.toString(), b.toString())) throw new AssertionError("random " + tr);
        }
    }
}
```

#### Solution: [Vary] Edit Distance (LeetCode 72)
<!-- id: ed-edit-distance -->

**Approach.**
The table keeps the meaning of the previous exercise, and the mismatch case gains a third read. Equal last characters copy the diagonal neighbor. Different last characters take one plus the smallest of the diagonal neighbor, which stands for a replacement, the cell above, which stands for a deletion, and the cell on the left, which stands for an insertion.

Every optimal script handles the last character of the source prefix in exactly one of those ways, so the minimum over the three covers all scripts. Row `i` reads only row `i - 1` and its own left cell, so the solution also shows a version with two rows of length `n + 1`, and the main method asserts that both versions agree.

**Complexity.**
- **Time** is O(m * n), because every cell does a constant number of reads.
- **Space** is O(m * n) for the full table, and the rolling version needs only O(n) memory.

```java run
import java.util.*;

public final class EdEditDistance {
    /**
     * Returns the edit distance with insert, delete and replace.
     * Time: O(m * n). Space: O(m * n).
     * Invariant: dp[i][j] is the exact distance between the prefixes of lengths i and j.
     */
    static int editDistance(String s, String t) {
        int m = s.length(), n = t.length();
        // The extra row and column describe the empty prefixes.
        int[][] dp = new int[m + 1][n + 1];
        // A source prefix of length i needs i deletions to become empty.
        for (int i = 0; i <= m; i++) dp[i][0] = i;
        // An empty source needs j insertions to reach a target prefix of length j.
        for (int j = 0; j <= n; j++) dp[0][j] = j;
        // Rows increase, so the row above is final when it is read.
        for (int i = 1; i <= m; i++) {
            // Columns increase, so the left cell is final when it is read.
            for (int j = 1; j <= n; j++) {
                if (s.charAt(i - 1) == t.charAt(j - 1)) {
                    // A match keeps the diagonal value without an extra edit.
                    dp[i][j] = dp[i - 1][j - 1];
                } else {
                    // Replace reads the diagonal, delete reads above, insert reads left.
                    dp[i][j] = 1 + Math.min(dp[i - 1][j - 1], Math.min(dp[i - 1][j], dp[i][j - 1]));
                }
            }
        }
        // The corner cell is the distance between the whole strings.
        return dp[m][n];
    }

    /**
     * Returns the same distance with two rows of length n + 1.
     * Time: O(m * n). Space: O(n).
     * Invariant: prev holds row i - 1 and cur holds row i up to column j.
     */
    static int rolling(String s, String t) {
        int m = s.length(), n = t.length();
        // prev starts as row 0, which holds the insertion counts.
        int[] prev = new int[n + 1];
        int[] cur = new int[n + 1];
        for (int j = 0; j <= n; j++) prev[j] = j;
        // Each source character produces one new row.
        for (int i = 1; i <= m; i++) {
            // Column 0 of row i is i deletions.
            cur[0] = i;
            for (int j = 1; j <= n; j++) {
                if (s.charAt(i - 1) == t.charAt(j - 1)) {
                    // The diagonal value sits at prev[j - 1].
                    cur[j] = prev[j - 1];
                } else {
                    // Above is prev[j], left is cur[j - 1], diagonal is prev[j - 1].
                    cur[j] = 1 + Math.min(prev[j - 1], Math.min(prev[j], cur[j - 1]));
                }
            }
            // Swap the arrays so the finished row becomes the previous row.
            int[] tmp = prev;
            prev = cur;
            cur = tmp;
        }
        // After the last swap, prev holds row m.
        return prev[n];
    }

    /** Oracle: plain recursion over the first characters of both strings. */
    static int oracle(String a, String b) {
        if (a.isEmpty()) return b.length();
        if (b.isEmpty()) return a.length();
        if (a.charAt(0) == b.charAt(0)) return oracle(a.substring(1), b.substring(1));
        return 1 + Math.min(oracle(a.substring(1), b.substring(1)),
                Math.min(oracle(a.substring(1), b), oracle(a, b.substring(1))));
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (editDistance("kitten", "sitting") != 3) throw new AssertionError("ex1");
        if (editDistance("monday", "mundane") != 3) throw new AssertionError("ex2");
        // Deleting the first character fixes the case that position matching gets wrong.
        if (editDistance("abc", "bc") != 1) throw new AssertionError("shift");
        // Equal strings cost 0, and two empty strings cost 0.
        if (editDistance("same", "same") != 0 || editDistance("", "") != 0) throw new AssertionError("zero");
        // Random strings against the oracle, and the rolling version against the table.
        Random rnd = new Random(2806);
        for (int tr = 0; tr < 2000; tr++) {
            StringBuilder a = new StringBuilder(), b = new StringBuilder();
            for (int i = rnd.nextInt(8); i > 0; i--) a.append((char) ('a' + rnd.nextInt(3)));
            for (int i = rnd.nextInt(8); i > 0; i--) b.append((char) ('a' + rnd.nextInt(3)));
            int expected = oracle(a.toString(), b.toString());
            if (editDistance(a.toString(), b.toString()) != expected) throw new AssertionError("table " + tr);
            if (rolling(a.toString(), b.toString()) != expected) throw new AssertionError("rolling " + tr);
        }
    }
}
```

#### Solution: [Boundary] Empty String (Author exercise)
<!-- id: ed-empty-string -->

**Approach.**
The edges of the table carry the whole answer when one string is empty. Cell `dp[i][0]` is `i`, because the only way to turn `i` characters into nothing is `i` deletions. Cell `dp[0][j]` is `j`, because the only way to build `j` characters from nothing is `j` insertions. The loops over interior cells never run when `m` or `n` is 0, so the corner is an edge cell, and the method returns the other length. Two empty strings give a 1 by 1 table with the value 0.

Setting the edges before the loops is what keeps the interior reads inside the table, since cell `(1, 1)` reads row 0 and column 0.

**Complexity.**
- **Time** is O(m * n) for the interior and O(m + n) for the edges, which is O(max(m, n)) when a string is empty.
- **Space** is O(m * n) for the table, which shrinks to O(max(m, n)) with an empty string.

```java run
import java.util.*;

public final class EdEmptyString {
    /**
     * Returns the edit distance, where either string may be empty.
     * Time: O(m * n + m + n). Space: O((m + 1) * (n + 1)).
     * Invariant: column 0 holds row indexes, row 0 holds column indexes, and the interior reads them.
     */
    static int distance(String s, String t) {
        int m = s.length(), n = t.length();
        // The table always has at least one row and one column.
        int[][] dp = new int[m + 1][n + 1];
        // Column 0 costs i deletions; the loop runs m + 1 times.
        for (int i = 0; i <= m; i++) dp[i][0] = i;
        // Row 0 costs j insertions; the loop runs n + 1 times.
        for (int j = 0; j <= n; j++) dp[0][j] = j;
        // The interior loops run zero times when m or n is 0.
        for (int i = 1; i <= m; i++) {
            for (int j = 1; j <= n; j++) {
                // The cell either copies a match or adds one edit to the best neighbor.
                int best = Math.min(dp[i - 1][j - 1] + (s.charAt(i - 1) == t.charAt(j - 1) ? 0 : 1),
                        Math.min(dp[i - 1][j] + 1, dp[i][j - 1] + 1));
                dp[i][j] = best;
            }
        }
        // For an empty string, this corner is an edge cell.
        return dp[m][n];
    }

    /** Oracle: plain recursion over the first characters of both strings. */
    static int oracle(String a, String b) {
        if (a.isEmpty()) return b.length();
        if (b.isEmpty()) return a.length();
        if (a.charAt(0) == b.charAt(0)) return oracle(a.substring(1), b.substring(1));
        return 1 + Math.min(oracle(a.substring(1), b.substring(1)),
                Math.min(oracle(a.substring(1), b), oracle(a, b.substring(1))));
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (distance("", "abc") != 3) throw new AssertionError("ex1");
        if (distance("abcd", "") != 4) throw new AssertionError("ex2");
        // Two empty strings return 0 without an out-of-range read.
        if (distance("", "") != 0) throw new AssertionError("both empty");
        // An empty string equals the other length for many lengths.
        for (int k = 0; k <= 20; k++) {
            String x = "z".repeat(k);
            if (distance("", x) != k || distance(x, "") != k) throw new AssertionError("length " + k);
        }
        // Random strings, including empty ones, against the oracle.
        Random rnd = new Random(2807);
        for (int tr = 0; tr < 2000; tr++) {
            StringBuilder a = new StringBuilder(), b = new StringBuilder();
            for (int i = rnd.nextInt(7); i > 0; i--) a.append((char) ('a' + rnd.nextInt(3)));
            for (int i = rnd.nextInt(7); i > 0; i--) b.append((char) ('a' + rnd.nextInt(3)));
            if (distance(a.toString(), b.toString()) != oracle(a.toString(), b.toString())) throw new AssertionError("random " + tr);
        }
    }
}
```

#### Solution: [Recognize] Reconstruct Operations (Author exercise)
<!-- id: ed-reconstruct-operations -->

**Approach.**
The method first builds the same table as the edit distance. The table stores counts only, so the method then walks from cell `(m, n)` back to `(0, 0)` and asks which neighbor explains the stored value. If the last characters are equal and the cell equals its diagonal neighbor, the step is `M`. Otherwise, if the cell equals the diagonal neighbor plus one, the step is `R`. Otherwise, if the cell equals the cell above plus one, the step is `D`, and the last remaining case is `I`. Each step moves to the neighbor that explains it, and the letters collect in reverse order.

The invariant is that the value of the current cell equals the number of non-`M` letters still to emit. Each step emits one letter and lowers that number by the cost of the letter, so the walk ends at `(0, 0)` with a script of exactly `dp[m][n]` edits. The fixed order of checks makes the answer unique.

**Complexity.**
- **Time** is O(m * n) for the table and O(m + n) for the walk, because each step lowers `i`, `j` or both.
- **Space** is O(m * n) for the table, because the walk needs interior cells, plus O(m + n) for the script.

```java run
import java.util.*;

public final class EdReconstructOperations {
    /**
     * Returns an optimal script of M, R, D and I letters read from left to right.
     * Time: O(m * n). Space: O(m * n).
     * Invariant: dp[i][j] equals the number of edit letters still needed for the prefixes of lengths i and j.
     */
    static String script(String s, String t) {
        int m = s.length(), n = t.length();
        // The extra row and column describe the empty prefixes.
        int[][] dp = new int[m + 1][n + 1];
        for (int i = 0; i <= m; i++) dp[i][0] = i;
        for (int j = 0; j <= n; j++) dp[0][j] = j;
        // Each interior cell copies a match or adds one to the best neighbor.
        for (int i = 1; i <= m; i++) {
            for (int j = 1; j <= n; j++) {
                if (s.charAt(i - 1) == t.charAt(j - 1)) {
                    dp[i][j] = dp[i - 1][j - 1];
                } else {
                    dp[i][j] = 1 + Math.min(dp[i - 1][j - 1], Math.min(dp[i - 1][j], dp[i][j - 1]));
                }
            }
        }
        // The walk collects letters from the end, so a builder is reversed later.
        StringBuilder out = new StringBuilder();
        int i = m, j = n;
        // Each pass lowers i, j or both, so the loop runs at most m + n times.
        while (i > 0 || j > 0) {
            if (i > 0 && j > 0 && s.charAt(i - 1) == t.charAt(j - 1) && dp[i][j] == dp[i - 1][j - 1]) {
                // The cell copied its diagonal neighbor, so the pair matches.
                out.append('M');
                i--;
                j--;
            } else if (i > 0 && j > 0 && dp[i][j] == dp[i - 1][j - 1] + 1) {
                // The diagonal neighbor explains the cell with one replacement.
                out.append('R');
                i--;
                j--;
            } else if (i > 0 && dp[i][j] == dp[i - 1][j] + 1) {
                // The cell above explains the cell with one deletion.
                out.append('D');
                i--;
            } else {
                // The last remaining explanation is the cell on the left, an insertion.
                out.append('I');
                j--;
            }
        }
        // The letters were collected from the end, so reverse them.
        return out.reverse().toString();
    }

    /** Oracle: plain recursion for the distance. */
    static int oracle(String a, String b) {
        if (a.isEmpty()) return b.length();
        if (b.isEmpty()) return a.length();
        if (a.charAt(0) == b.charAt(0)) return oracle(a.substring(1), b.substring(1));
        return 1 + Math.min(oracle(a.substring(1), b.substring(1)),
                Math.min(oracle(a.substring(1), b), oracle(a, b.substring(1))));
    }

    /** Applies the script to s and returns the string it produces, or null when a letter is invalid. */
    static String apply(String s, String t, String script) {
        StringBuilder res = new StringBuilder();
        int i = 0, j = 0;
        for (char c : script.toCharArray()) {
            if (c == 'M') {
                // A match needs equal characters at both cursors.
                if (i >= s.length() || j >= t.length() || s.charAt(i) != t.charAt(j)) return null;
                res.append(s.charAt(i));
                i++;
                j++;
            } else if (c == 'R') {
                if (i >= s.length() || j >= t.length()) return null;
                res.append(t.charAt(j));
                i++;
                j++;
            } else if (c == 'D') {
                if (i >= s.length()) return null;
                i++;
            } else {
                if (j >= t.length()) return null;
                res.append(t.charAt(j));
                j++;
            }
        }
        // Both strings must be fully consumed.
        return i == s.length() && j == t.length() ? res.toString() : null;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!script("cat", "cut").equals("MRM")) throw new AssertionError("ex1");
        if (!script("ab", "b").equals("DM")) throw new AssertionError("ex2");
        // Empty inputs give only insertions or only deletions.
        if (!script("", "").equals("") || !script("", "ab").equals("II") || !script("ab", "").equals("DD")) throw new AssertionError("empty");
        // Random strings: the script is valid, optimal, and at least as long as the longer input.
        Random rnd = new Random(2808);
        for (int tr = 0; tr < 2000; tr++) {
            StringBuilder a = new StringBuilder(), b = new StringBuilder();
            for (int i = rnd.nextInt(8); i > 0; i--) a.append((char) ('a' + rnd.nextInt(3)));
            for (int i = rnd.nextInt(8); i > 0; i--) b.append((char) ('a' + rnd.nextInt(3)));
            String s = a.toString(), t = b.toString();
            String sc = script(s, t);
            if (!t.equals(apply(s, t, sc))) throw new AssertionError("invalid " + tr);
            int edits = 0;
            for (char c : sc.toCharArray()) if (c != 'M') edits++;
            if (edits != oracle(s, t)) throw new AssertionError("not optimal " + tr);
            if (sc.length() < Math.max(s.length(), t.length())) throw new AssertionError("short " + tr);
        }
    }
}
```
