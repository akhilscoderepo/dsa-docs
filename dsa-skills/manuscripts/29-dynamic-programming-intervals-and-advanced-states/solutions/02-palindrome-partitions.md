<!-- solutions-for: 29-dynamic-programming-intervals-and-advanced-states -->
### Solutions For Palindrome Partitions

#### Solution: [Build] Palindrome Table (Author exercise)
<!-- id: dp29-pp-palindrome-table -->

**Approach.**
The table `pal` has one row and one column for each index of `s`. Entry `pal[i][j]` is true when the substring from `i` to `j` is a palindrome. A substring of one or two characters needs only equal end characters. A longer substring needs equal end characters and a true entry for the inner interval, `pal[i + 1][j - 1]`. The method visits `i` from the last index down to 0 and `j` from `i` upward, so the inner entry is final when the outer entry reads it. The method counts the true entries as it sets them.

The invariant is that every entry read by `(i, j)` belongs to a row below `i` or to the same row and was set earlier. An empty string has no rows, so the count stays 0.

**Complexity.**
- **Time** is O(n^2), because the loops visit n * (n + 1) / 2 entries and each costs constant work.
- **Space** is O(n^2) for the boolean table, and the string stays unchanged.

```java run
import java.util.*;

public final class PpPalindromeTable {
    /**
     * Counts the index pairs (i, j) whose substring is a palindrome.
     * Time: O(n^2). Space: O(n^2).
     * Invariant: pal[i + 1][j - 1] is final before pal[i][j] reads it.
     */
    static int countPalindromes(String s) {
        // n is the string length, and the table has n rows and n columns.
        int n = s.length();
        boolean[][] pal = new boolean[n][n];
        int count = 0;
        // Rows run from the last index upward, so the row below is complete.
        for (int i = n - 1; i >= 0; i--) {
            // Columns start at i, because a substring needs i <= j.
            for (int j = i; j < n; j++) {
                // A substring of length 1 or 2 has an empty inner interval.
                boolean innerOk = j - i < 2 || pal[i + 1][j - 1];
                // Equal end characters and a valid inner interval make a palindrome.
                pal[i][j] = s.charAt(i) == s.charAt(j) && innerOk;
                // Each true entry adds one to the count.
                if (pal[i][j]) count++;
            }
        }
        // The count covers every pair with i <= j.
        return count;
    }

    /** Oracle: reverses every substring and compares it with the original. */
    static int oracle(String s) {
        int count = 0;
        for (int i = 0; i < s.length(); i++) {
            for (int j = i; j < s.length(); j++) {
                String t = s.substring(i, j + 1);
                if (new StringBuilder(t).reverse().toString().equals(t)) count++;
            }
        }
        return count;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (countPalindromes("aaba") != 6) throw new AssertionError("ex1");
        if (countPalindromes("abcba") != 7) throw new AssertionError("ex2");
        // The empty string, one character, equal characters and distinct characters.
        if (countPalindromes("") != 0) throw new AssertionError("empty");
        if (countPalindromes("a") != 1) throw new AssertionError("single");
        if (countPalindromes("aaaa") != 10) throw new AssertionError("equal");
        if (countPalindromes("abcd") != 4) throw new AssertionError("distinct");
        // A new boolean array holds false, and substring excludes its end index.
        boolean[][] fresh = new boolean[2][2];
        if (fresh[0][1]) throw new AssertionError("false fill");
        if (!"abc".substring(0, 2).equals("ab")) throw new AssertionError("substring");
        // Strings are immutable, so the input keeps its content.
        String s = "abba";
        countPalindromes(s);
        if (!s.equals("abba")) throw new AssertionError("mutated");
        // Random strings against the reversal oracle.
        Random rnd = new Random(2921);
        for (int t = 0; t < 2000; t++) {
            String w = word(rnd, rnd.nextInt(12), 3);
            if (countPalindromes(w) != oracle(w)) throw new AssertionError("random " + t);
        }
    }

    static String word(Random rnd, int len, int alphabet) {
        StringBuilder s = new StringBuilder();
        for (int k = 0; k < len; k++) s.append((char) ('a' + rnd.nextInt(alphabet)));
        return s.toString();
    }
}
```

#### Solution: [Vary] Minimum Valid Prefix Pieces (Author exercise)
<!-- id: dp29-pp-valid-prefix-pieces -->

**Approach.**
The method fills the palindrome table first. It then defines `pieces[end]` as the fewest valid pieces that cover the first `end` characters, with `pieces[0] = 0`. For each `end`, it tries every `start` below `end`. A start is allowed when the piece `s[start..end - 1]` is a palindrome, has at least `k` characters, and `pieces[start]` is reachable. Unreachable prefixes hold a large sentinel, and the transition skips them. A reachable value plus 1 never overflows, because the method adds 1 only to reachable values.

The invariant is that `pieces[start]` is final before `pieces[end]` reads it, and the sentinel marks exactly the prefixes with no valid split. The method returns -1 when `pieces[n]` is still the sentinel.

**Complexity.**
- **Time** is O(n^2), because the table fill and the prefix loops each visit O(n^2) pairs.
- **Space** is O(n^2) for the table plus O(n) for `pieces`.

```java run
import java.util.*;

public final class PpValidPrefixPieces {
    /**
     * Returns the fewest palindromic pieces of length at least k, or -1 if no split exists.
     * Time: O(n^2). Space: O(n^2).
     * Invariant: pieces[start] is final before pieces[end] reads it.
     */
    static int minPieces(String s, int k) {
        int n = s.length();
        boolean[][] pal = new boolean[n][n];
        // Rows run upward so the inner interval is final when read.
        for (int i = n - 1; i >= 0; i--) {
            for (int j = i; j < n; j++) {
                pal[i][j] = s.charAt(i) == s.charAt(j) && (j - i < 2 || pal[i + 1][j - 1]);
            }
        }
        // The sentinel marks a prefix that no valid split reaches.
        final int unreachable = Integer.MAX_VALUE;
        int[] pieces = new int[n + 1];
        Arrays.fill(pieces, unreachable);
        // The empty prefix needs 0 pieces.
        pieces[0] = 0;
        // end is the prefix length, so each pass finishes one entry.
        for (int end = 1; end <= n; end++) {
            // start is the first index of the last piece.
            for (int start = 0; start < end; start++) {
                // The piece must be long enough, a palindrome, and attached to a reachable prefix.
                if (end - start >= k && pal[start][end - 1] && pieces[start] != unreachable) {
                    pieces[end] = Math.min(pieces[end], pieces[start] + 1);
                }
            }
        }
        // An untouched sentinel means no split exists.
        return pieces[n] == unreachable ? -1 : pieces[n];
    }

    /** Oracle: tries every set of cut positions and checks each piece directly. */
    static int oracle(String s, int k) {
        int n = s.length();
        int best = -1;
        for (int mask = 0; mask < (1 << (n - 1)); mask++) {
            int start = 0;
            int count = 0;
            boolean valid = true;
            for (int p = 0; p < n && valid; p++) {
                if (p == n - 1 || ((mask >> p) & 1) == 1) {
                    String t = s.substring(start, p + 1);
                    if (t.length() < k || !new StringBuilder(t).reverse().toString().equals(t)) valid = false;
                    count++;
                    start = p + 1;
                }
            }
            if (valid && (best == -1 || count < best)) best = count;
        }
        return best;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (minPieces("aabbcc", 2) != 3) throw new AssertionError("ex1");
        if (minPieces("racecarbob", 3) != 2) throw new AssertionError("ex2");
        // A limit that no split can meet, and a limit of 1 that reduces to the plain count.
        if (minPieces("aabbcc", 3) != -1) throw new AssertionError("impossible");
        if (minPieces("aaba", 1) != 2) throw new AssertionError("k one");
        if (minPieces("abcba", 5) != 1) throw new AssertionError("whole string");
        // Adding 1 to Integer.MAX_VALUE overflows to a negative number, which is why the sentinel is skipped.
        if (Integer.MAX_VALUE + 1 >= 0) throw new AssertionError("overflow");
        // Random inputs against the cut-set oracle.
        Random rnd = new Random(2922);
        for (int t = 0; t < 2000; t++) {
            String w = word(rnd, 1 + rnd.nextInt(11), 2);
            int k = 1 + rnd.nextInt(w.length());
            if (minPieces(w, k) != oracle(w, k)) throw new AssertionError("random " + t + " " + w + " " + k);
        }
    }

    static String word(Random rnd, int len, int alphabet) {
        StringBuilder s = new StringBuilder();
        for (int k = 0; k < len; k++) s.append((char) ('a' + rnd.nextInt(alphabet)));
        return s.toString();
    }
}
```

#### Solution: [Boundary] Empty Prefix And Whole Palindrome (Author exercise)
<!-- id: dp29-pp-empty-prefix -->

**Approach.**
The method fills the palindrome table, then fills `pieces[end]` for every prefix length, with `pieces[0] = 0`. The cut count of a prefix is `pieces[end] - 1`, except for the empty prefix, where the subtraction would give -1. The method therefore writes 0 into `r[0]` directly and writes `pieces[end] - 1` for each `end` from 1. A palindromic prefix has `pieces[end] = 1`, which gives 0 cuts.

The invariant is that `r[end]` reads only a finished `pieces[end]`, and that the guard covers exactly the one prefix with zero pieces. An empty string returns the array `[0]`.

**Complexity.**
- **Time** is O(n^2), because the table fill and the prefix loops each visit O(n^2) pairs.
- **Space** is O(n^2) for the table, and the result has n + 1 entries.

```java run
import java.util.*;

public final class PpEmptyPrefix {
    /**
     * Returns the fewest palindrome cuts for every prefix length from 0 to n.
     * Time: O(n^2). Space: O(n^2).
     * Invariant: r[end] is read from a finished pieces[end], and r[0] is fixed at 0.
     */
    static int[] cutsPerPrefix(String s) {
        int n = s.length();
        boolean[][] pal = new boolean[n][n];
        // Rows run upward so the inner interval is final when read.
        for (int i = n - 1; i >= 0; i--) {
            for (int j = i; j < n; j++) {
                pal[i][j] = s.charAt(i) == s.charAt(j) && (j - i < 2 || pal[i + 1][j - 1]);
            }
        }
        int[] pieces = new int[n + 1];
        int[] r = new int[n + 1];
        // The empty prefix keeps pieces 0 and cuts 0, so no subtraction runs for it.
        for (int end = 1; end <= n; end++) {
            pieces[end] = Integer.MAX_VALUE;
            // Each start gives a candidate last piece.
            for (int start = 0; start < end; start++) {
                if (pal[start][end - 1] && pieces[start] + 1 < pieces[end]) pieces[end] = pieces[start] + 1;
            }
            // p pieces use p - 1 cuts, which is valid because end >= 1 gives pieces[end] >= 1.
            r[end] = pieces[end] - 1;
        }
        return r;
    }

    /** Oracle: for each prefix, tries every set of cut positions with direct palindrome checks. */
    static int[] oracle(String s) {
        int[] r = new int[s.length() + 1];
        for (int e = 1; e <= s.length(); e++) {
            String p = s.substring(0, e);
            int best = e - 1;
            for (int mask = 0; mask < (1 << (e - 1)); mask++) {
                int start = 0;
                int cuts = 0;
                boolean valid = true;
                for (int q = 0; q < e && valid; q++) {
                    if (q == e - 1 || ((mask >> q) & 1) == 1) {
                        String t = p.substring(start, q + 1);
                        if (!new StringBuilder(t).reverse().toString().equals(t)) valid = false;
                        if (q < e - 1) cuts++;
                        start = q + 1;
                    }
                }
                if (valid) best = Math.min(best, cuts);
            }
            r[e] = best;
        }
        return r;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!Arrays.equals(cutsPerPrefix(""), new int[] {0})) throw new AssertionError("ex1");
        if (!Arrays.equals(cutsPerPrefix("abcba"), new int[] {0, 0, 1, 2, 1, 0})) throw new AssertionError("ex2");
        // A whole palindrome ends with 0, and distinct characters grow by one per prefix.
        if (cutsPerPrefix("aaaa")[4] != 0) throw new AssertionError("whole");
        if (!Arrays.equals(cutsPerPrefix("abcd"), new int[] {0, 0, 1, 2, 3})) throw new AssertionError("distinct");
        // A new int array holds zeros, so entry 0 of a one-character result is 0 and entry 1 is 0.
        int[] z = new int[3];
        if (z[2] != 0) throw new AssertionError("zero fill");
        if (cutsPerPrefix("a")[0] != 0) throw new AssertionError("entry zero");
        // Random strings against the cut-set oracle.
        Random rnd = new Random(2923);
        for (int t = 0; t < 1500; t++) {
            String w = word(rnd, rnd.nextInt(11), 3);
            if (!Arrays.equals(cutsPerPrefix(w), oracle(w))) throw new AssertionError("random " + t + " " + w);
        }
    }

    static String word(Random rnd, int len, int alphabet) {
        StringBuilder s = new StringBuilder();
        for (int k = 0; k < len; k++) s.append((char) ('a' + rnd.nextInt(alphabet)));
        return s.toString();
    }
}
```

#### Solution: [Recognize] Palindrome Partitioning II (LeetCode 132)
<!-- id: dp29-pp-min-cuts -->

**Approach.**
The method keeps only `cuts`, where `cuts[e]` is the fewest cuts for the first `e` characters, with `cuts[0] = -1` so that a prefix that is one whole palindrome costs `-1 + 1 = 0`. Each entry starts at its worst case, `e - 1`. Instead of a boolean table, the method grows a palindrome from every center. For an odd center `c` it starts at `l = r = c`, and for an even center it starts at `l = c`, `r = c + 1`. Each palindrome `s[l..r]` offers `cuts[l] + 1` to `cuts[r + 1]`, and the method keeps the smaller value.

The invariant is that `cuts[l]` is final when a palindrome starting at `l` reads it. Every palindrome that ends at index `l - 1` has a center left of `c`, so the earlier centers already updated `cuts[l]`. The answer is `cuts[n]`.

**Complexity.**
- **Time** is O(n^2), because each of the 2n - 1 centers grows over at most n characters.
- **Space** is O(n) for the `cuts` array, with no boolean table.

```java run
import java.util.*;

public final class PpMinCuts {
    /**
     * Returns the fewest cuts that split s into palindromes.
     * Time: O(n^2). Space: O(n).
     * Invariant: cuts[l] is final before a palindrome that starts at l uses it.
     */
    static int minCut(String s) {
        int n = s.length();
        int[] cuts = new int[n + 1];
        // Prefix length e needs at most e - 1 cuts, and the empty prefix holds -1.
        for (int e = 0; e <= n; e++) cuts[e] = e - 1;
        // Centers run from left to right, so earlier centers finish first.
        for (int c = 0; c < n; c++) {
            // Odd length: the palindrome grows around the single character c.
            for (int l = c, r = c; l >= 0 && r < n && s.charAt(l) == s.charAt(r); l--, r++) {
                // The palindrome s[l..r] ends the prefix of length r + 1 after the prefix of length l.
                cuts[r + 1] = Math.min(cuts[r + 1], cuts[l] + 1);
            }
            // Even length: the palindrome grows around the gap between c and c + 1.
            for (int l = c, r = c + 1; l >= 0 && r < n && s.charAt(l) == s.charAt(r); l--, r++) {
                cuts[r + 1] = Math.min(cuts[r + 1], cuts[l] + 1);
            }
        }
        // The last entry covers the whole string.
        return cuts[n];
    }

    /** Oracle: tries every set of cut positions and checks each piece directly. */
    static int oracle(String s) {
        int n = s.length();
        int best = n - 1;
        for (int mask = 0; mask < (1 << (n - 1)); mask++) {
            int start = 0;
            int cuts = 0;
            boolean valid = true;
            for (int q = 0; q < n && valid; q++) {
                if (q == n - 1 || ((mask >> q) & 1) == 1) {
                    String t = s.substring(start, q + 1);
                    if (!new StringBuilder(t).reverse().toString().equals(t)) valid = false;
                    if (q < n - 1) cuts++;
                    start = q + 1;
                }
            }
            if (valid) best = Math.min(best, cuts);
        }
        return best;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (minCut("abbab") != 1) throw new AssertionError("ex1");
        if (minCut("cabbad") != 2) throw new AssertionError("ex2");
        // One character, a whole palindrome, distinct characters and the lesson string.
        if (minCut("a") != 0) throw new AssertionError("single");
        if (minCut("abcba") != 0) throw new AssertionError("whole");
        if (minCut("abcd") != 3) throw new AssertionError("distinct");
        if (minCut("aaba") != 1) throw new AssertionError("lesson");
        // A long string of equal characters finishes without a cut and without a table.
        if (minCut("a".repeat(2000)) != 0) throw new AssertionError("long");
        // Random strings against the cut-set oracle.
        Random rnd = new Random(2924);
        for (int t = 0; t < 2000; t++) {
            String w = word(rnd, 1 + rnd.nextInt(12), 3);
            if (minCut(w) != oracle(w)) throw new AssertionError("random " + t + " " + w);
        }
    }

    static String word(Random rnd, int len, int alphabet) {
        StringBuilder s = new StringBuilder();
        for (int k = 0; k < len; k++) s.append((char) ('a' + rnd.nextInt(alphabet)));
        return s.toString();
    }
}
```
