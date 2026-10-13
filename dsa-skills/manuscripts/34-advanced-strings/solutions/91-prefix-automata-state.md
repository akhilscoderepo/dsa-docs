<!-- solutions-for: 91-prefix-automata-state -->
### Solutions For Stream Matching With Failure Links

#### Solution: [Build] Every Start Of A Pattern (LeetCode 28)
<!-- id: as-all-starts-automaton -->

**Approach.**
The pattern defines states 0 to `m`, where state `k` means that the last `k` characters read equal `pattern[0..k-1]`. The array `fail` is built first. Each text character is then one transition: while the next pattern character `pattern[k]` differs from the text character, the state drops to `fail[k - 1]`, and when the characters agree the state rises by one. State `m` has no next pattern character. The transition from it therefore starts with a fall to `fail[m - 1]`, which keeps the longest end of the text that can still begin another occurrence. This fall is what lets overlapping occurrences appear, and a scan that returned at state `m` could report only the first.

The invariant is that after reading `text[0..i]` the state is the length of the longest prefix of the pattern that is a suffix of that text, except that a full match is reported before the fall. A match ending at `i` is reported as start `i - m + 1`, in increasing order because `i` only grows.

**Complexity.**
- **Time** is O(n + m), because the state rises at most once per text character and every fallback lowers it, so fallbacks never exceed `n`.
- **Space** is O(m + z), because `fail` has one entry per pattern character and the answer holds z start indices.

```java run
import java.util.Arrays;
import java.util.Random;

public final class AllStartsAutomaton {
    // Counts fallbacks so that main can check the amortized bound.
    static int fallbacks;

    /**
     * Returns the border length of every prefix of pat; pat is non-empty.
     * Time: O(m), because the state rises at most once per character.
     * Space: O(m), because the result has one entry per character.
     * Invariant: before iteration i, k equals fail[i - 1].
     */
    static int[] failArray(String pat) {
        // One entry per pattern character; entry 0 stays 0 because a single character has no proper prefix.
        int[] fail = new int[pat.length()];
        // k is the length of the border of the prefix read so far.
        int k = 0;
        // Position 0 needs no work, so the loop starts at 1.
        for (int i = 1; i < pat.length(); i++) {
            // A mismatch moves k to the next shorter border of the same prefix.
            while (k > 0 && pat.charAt(i) != pat.charAt(k)) k = fail[k - 1];
            // A match extends the border by one character.
            if (pat.charAt(i) == pat.charAt(k)) k++;
            // Record the border length for position i.
            fail[i] = k;
        }
        // The caller reads fallback targets from this array.
        return fail;
    }

    /**
     * Returns every start index of pat in text, overlaps included, in increasing order.
     * Time: O(n + m), because the text index never moves back and fallbacks are paid by earlier growth.
     * Space: O(m + z), because of the fail array and the z reported starts.
     * Invariant: after reading text[0..i], k is the longest pattern prefix that is a suffix of the text read.
     */
    static int[] allStarts(String text, String pat) {
        // Pattern table built once; its cost is O(m).
        int[] fail = failArray(pat);
        // Matches cannot exceed the number of text positions, so this buffer is large enough.
        int[] starts = new int[text.length()];
        // found counts reported starts; k is the match state.
        int found = 0, k = 0;
        // The text index only moves forward, which bounds the scan to n iterations.
        for (int i = 0; i < text.length(); i++) {
            // Fall back while the next pattern character rejects the text character.
            while (k > 0 && pat.charAt(k) != text.charAt(i)) { k = fail[k - 1]; fallbacks++; }
            // An agreeing character extends the match by one.
            if (pat.charAt(k) == text.charAt(i)) k++;
            // A full match ends at i, so it starts at i - m + 1.
            if (k == pat.length()) {
                starts[found++] = i - pat.length() + 1;
                // The match state has no next character; fall to the longest border so overlaps continue.
                k = fail[k - 1];
                fallbacks++;
            }
        }
        // Trim the buffer to the reported matches.
        return Arrays.copyOf(starts, found);
    }

    /**
     * Brute-force oracle that tests every start position.
     * Time: O(n * m), because each start compares up to m characters.
     * Space: O(z), because only the result is stored.
     * Invariant: start s is reported exactly when the m characters from s equal pat.
     */
    static int[] oracle(String text, String pat) {
        // Collect starts in a list because the count is unknown.
        java.util.List<Integer> out = new java.util.ArrayList<>();
        // Every start with enough room for the pattern is tested.
        for (int s = 0; s + pat.length() <= text.length(); s++) {
            // regionMatches compares in place without allocating a substring.
            if (text.regionMatches(s, pat, 0, pat.length())) out.add(s);
        }
        // Convert the list to the contract's int array.
        return out.stream().mapToInt(Integer::intValue).toArray();
    }

    public static void main(String[] args) {
        // Overlapping occurrences from the exercise.
        if (!Arrays.equals(allStarts("abababa", "aba"), new int[] {0, 2, 4})) throw new AssertionError("abababa");
        // The hostile all-equal case reports every position after the third.
        if (!Arrays.equals(allStarts("aaaaaa", "aaa"), new int[] {0, 1, 2, 3})) throw new AssertionError("aaaaaa");
        // A pattern longer than the text yields an empty array.
        if (allStarts("aab", "aabaab").length != 0) throw new AssertionError("longer pattern");
        // An empty text yields an empty array.
        if (allStarts("", "a").length != 0) throw new AssertionError("empty text");
        // A pattern of length one is its own match state with no fallback beyond the root.
        if (!Arrays.equals(allStarts("abca", "a"), new int[] {0, 3})) throw new AssertionError("length one");
        // Random comparison with the oracle; the seed makes any failure reproducible.
        Random rnd = new Random(3491L);
        for (int t = 0; t < 4000; t++) {
            // Small alphabets create many overlaps and fallbacks.
            int alpha = 1 + rnd.nextInt(3);
            StringBuilder tx = new StringBuilder(), pt = new StringBuilder();
            for (int i = rnd.nextInt(25); i > 0; i--) tx.append((char) ('a' + rnd.nextInt(alpha)));
            for (int i = 1 + rnd.nextInt(5); i > 0; i--) pt.append((char) ('a' + rnd.nextInt(alpha)));
            // Reset the counter so each case is bounded on its own.
            fallbacks = 0;
            int[] got = allStarts(tx.toString(), pt.toString());
            if (!Arrays.equals(got, oracle(tx.toString(), pt.toString()))) throw new AssertionError("mismatch " + tx + " / " + pt);
            // The amortized bound: fallbacks never exceed the text length.
            if (fallbacks > tx.length()) throw new AssertionError("too many fallbacks");
        }
    }
}
```

#### Solution: [Vary] Smallest Repeating Unit (LeetCode 459)
<!-- id: as-smallest-repeating-unit -->

**Approach.**
The array `fail` gives `b = fail[n - 1]`, the length of the longest proper prefix of `s` that is also a suffix. A border of length `b` means that `s[i] == s[i + (n - b)]` for every valid index, so `p = n - b` is the smallest shift under which the string agrees with itself, which is its smallest period. When `p` divides `n`, the string is the first `p` characters repeated `n / p` times, and no smaller length can work because a smaller valid unit would be a smaller period. When `p` does not divide `n`, no proper unit exists. A proper unit `u` that divides `n` is also a period with `u <= n / 2`, and then `p + u <= n`, so the periodicity lemma of Fine and Wilf makes `p` divide `u`, which would make `p` divide `n`.

When the border is 0, the formula gives `p = n`, and `n` divides `n`, so the same line returns `n`. The invariant is that `p` is the smallest period of the whole string, because the border chain lists all periods.

**Complexity.**
- **Time** is O(n), because building `fail` is linear and the final test is one remainder.
- **Space** is O(n), because `fail` has one entry per character.

```java run
import java.util.Random;

public final class SmallestRepeatingUnit {
    /**
     * Returns the border length of the whole string, using a running border value.
     * Time: O(n), because the border rises at most once per character.
     * Space: O(n), because the table of border lengths has n entries.
     * Invariant: before iteration i, k is the border length of s[0..i-1].
     */
    static int wholeBorder(String s) {
        // Table of border lengths per prefix.
        int[] fail = new int[s.length()];
        // k is the current border length.
        int k = 0;
        // Each position extends or shortens the border of the previous prefix.
        for (int i = 1; i < s.length(); i++) {
            // Shorten the border until the next character agrees or the border is empty.
            while (k > 0 && s.charAt(i) != s.charAt(k)) k = fail[k - 1];
            // Extend by one when the characters agree.
            if (s.charAt(i) == s.charAt(k)) k++;
            // Store the border for prefix i.
            fail[i] = k;
        }
        // The last entry is the border of the whole string.
        return fail[s.length() - 1];
    }

    /**
     * Returns the smallest u that divides n with s equal to u-character blocks repeated, or n if none is smaller.
     * Time: O(n), because of the border computation.
     * Space: O(n), because of the border table.
     * Invariant: p = n - border is the smallest period of s.
     */
    static int smallestUnit(String s) {
        // Length of the string.
        int n = s.length();
        // The gap between the string and its longest border is the smallest period.
        int p = n - wholeBorder(s);
        // A period that divides n tiles the string; otherwise the whole string is the only unit.
        return n % p == 0 ? p : n;
    }

    /**
     * Brute-force oracle that tests every divisor length.
     * Time: O(n^2), because each of up to n lengths checks n characters.
     * Space: O(1), because only counters are used.
     * Invariant: the first divisor u whose blocks all agree is the smallest valid one.
     */
    static int oracle(String s) {
        // Lengths are tried from 1 upward, so the first success is the smallest.
        for (int u = 1; u < s.length(); u++) {
            // Only divisors of n can tile the string exactly.
            if (s.length() % u != 0) continue;
            // ok stays true while every character equals the one u positions earlier.
            boolean ok = true;
            for (int i = u; i < s.length() && ok; i++) ok = s.charAt(i) == s.charAt(i - u);
            // The first tiling length is returned.
            if (ok) return u;
        }
        // No proper unit exists, so the whole string is the unit.
        return s.length();
    }

    public static void main(String[] args) {
        // Worked examples from the exercise.
        if (smallestUnit("abcabcabc") != 3) throw new AssertionError("abcabcabc");
        // The border 3 leaves gap 2, which does not divide 5, so the answer is the full length.
        if (smallestUnit("ababa") != 5) throw new AssertionError("ababa");
        // A single character is its own unit.
        if (smallestUnit("a") != 1) throw new AssertionError("a");
        // All-equal text has unit 1.
        if (smallestUnit("aaaaaa") != 1) throw new AssertionError("aaaaaa");
        // Random comparison with the oracle; the seed makes any failure reproducible.
        Random rnd = new Random(3492L);
        for (int t = 0; t < 5000; t++) {
            // Short blocks repeated a random number of times produce many true cases.
            int alpha = 1 + rnd.nextInt(2);
            StringBuilder block = new StringBuilder();
            for (int i = 1 + rnd.nextInt(4); i > 0; i--) block.append((char) ('a' + rnd.nextInt(alpha)));
            StringBuilder s = new StringBuilder();
            for (int r = 1 + rnd.nextInt(4); r > 0; r--) s.append(block);
            // Sometimes append one stray character to build near-miss cases.
            if (rnd.nextInt(3) == 0) s.append((char) ('a' + rnd.nextInt(alpha)));
            if (smallestUnit(s.toString()) != oracle(s.toString())) throw new AssertionError("mismatch " + s);
        }
    }
}
```

#### Solution: [Boundary] Borders And Repeats Of Every Prefix (LeetCode 1392)
<!-- id: as-prefix-border-lengths -->

**Approach.**
The string is matched against itself. The state `k` is the border of the prefix read so far, and each new character `s[i]` is one transition of the machine built from the earlier entries. While `s[k]` differs from `s[i]`, the state falls to `fail[k - 1]`. When the characters agree, the state rises to `k + 1`. Row 0 stores that state for index `i`. The state is always at most `i`, because the transition reads `s[i]` against a position `k` that is still before `i`, so the border is strictly shorter than the prefix.

Row 1 reads only the finished border. A prefix of length `len = i + 1` with border `b` has the period `p = len - b`. The prefix is a repeat exactly when `b > 0` and `len % p == 0`. When `b` is 0 the period equals `len`, so there is no shorter unit. When `p` does not divide `len`, no other length can work, because every period of the prefix is at least `p` and a unit length must divide `len`. Index 0 has border 0, so both rows hold 0 there and the loop does not run for a string of length one. The invariant is that before iteration `i`, the value `k` equals `fail[i - 1]`.

**Complexity.**
- **Time** is O(n), because `k` rises by at most 1 per index, each fallback lowers it by at least 1, and the flag is one remainder test per index.
- **Space** is O(n), because the two rows have one entry per index.

```java run
import java.util.Arrays;
import java.util.Random;

public final class PrefixBorderLengths {
    /**
     * Returns row 0 with the longest proper border of every prefix and row 1 with the repeat flag of every prefix.
     * Time: O(n), by the amortized rise and fall of k.
     * Space: O(n), because both rows have n entries.
     * Invariant: before iteration i, k equals out[0][i - 1].
     */
    static int[][] bordersAndRepeats(String s) {
        // Row 0 holds borders and row 1 holds repeat flags; entry 0 of both is 0.
        int[][] out = new int[2][s.length()];
        // k starts at the border of the first prefix.
        int k = 0;
        // The loop is skipped for a string of length one.
        for (int i = 1; i < s.length(); i++) {
            // Fall to shorter borders while the next character disagrees.
            while (k > 0 && s.charAt(k) != s.charAt(i)) k = out[0][k - 1];
            // Rise by one when the characters agree; k stays at most i because s.charAt(k) is read before i.
            if (s.charAt(k) == s.charAt(i)) k++;
            // Store the border for the prefix ending at i.
            out[0][i] = k;
            // The period is the prefix length minus the border; it divides the length only for a repeat.
            int len = i + 1;
            if (k > 0 && len % (len - k) == 0) out[1][i] = 1;
        }
        // The caller reads both rows from this array.
        return out;
    }

    /**
     * Brute-force oracle that tests every proper length and every unit length for every prefix.
     * Time: O(n^3), because of three nested loops.
     * Space: O(n), because of the result.
     * Invariant: the first matching border tried from the longest is the maximum.
     */
    static int[][] oracle(String s) {
        // Result rows.
        int[][] out = new int[2][s.length()];
        // Each prefix s[0..i] is handled alone.
        for (int i = 0; i < s.length(); i++) {
            // Proper border lengths run from i down to 1.
            for (int len = i; len >= 1; len--) {
                // The prefix and the suffix of this length must agree.
                if (s.regionMatches(0, s, i + 1 - len, len)) { out[0][i] = len; break; }
            }
            // A unit length u below the prefix length that divides it and rebuilds the prefix proves a repeat.
            for (int u = 1; u <= i; u++) {
                if ((i + 1) % u != 0) continue;
                boolean same = true;
                for (int j = u; j <= i; j++) if (s.charAt(j) != s.charAt(j - u)) { same = false; break; }
                if (same) { out[1][i] = 1; break; }
            }
        }
        // Compared with the fast answer in main.
        return out;
    }

    public static void main(String[] args) {
        // Worked examples from the exercise.
        if (!Arrays.deepEquals(bordersAndRepeats("ababab"), new int[][] {{0, 0, 1, 2, 3, 4}, {0, 0, 0, 1, 0, 1}})) throw new AssertionError("ababab");
        // A border that does not divide the length is not a repeat.
        if (!Arrays.deepEquals(bordersAndRepeats("abcab"), new int[][] {{0, 0, 0, 1, 2}, {0, 0, 0, 0, 0}})) throw new AssertionError("abcab");
        // All-equal text: every prefix after the first is a repeat of one letter.
        if (!Arrays.deepEquals(bordersAndRepeats("aaaa"), new int[][] {{0, 1, 2, 3}, {0, 1, 1, 1}})) throw new AssertionError("aaaa");
        // Length one gives a zero in both rows.
        if (!Arrays.deepEquals(bordersAndRepeats("a"), new int[][] {{0}, {0}})) throw new AssertionError("a");
        // Random comparison with the oracle; the seed makes any failure reproducible.
        Random rnd = new Random(3493L);
        for (int t = 0; t < 4000; t++) {
            // Small alphabets create many borders and repeats.
            int alpha = 1 + rnd.nextInt(3);
            StringBuilder sb = new StringBuilder();
            for (int i = 1 + rnd.nextInt(14); i > 0; i--) sb.append((char) ('a' + rnd.nextInt(alpha)));
            String s = sb.toString();
            int[][] got = bordersAndRepeats(s);
            if (!Arrays.deepEquals(got, oracle(s))) throw new AssertionError("mismatch " + s);
            // Every border is proper: strictly shorter than its prefix.
            for (int i = 0; i < s.length(); i++) if (got[0][i] > i) throw new AssertionError("not proper " + s);
        }
    }
}
```

#### Solution: [Recognize] Count Words Ending Here (LeetCode 1032)
<!-- id: as-count-words-ending-here -->

**Approach.**
The words are inserted into a trie, so each node stands for one prefix of some word. A level-order pass computes, for every node, a failure target (the node of its longest proper suffix that is also a node), and fills every missing edge with the edge of the failure target. After this pass each node has a transition for all 26 letters. The pass also adds the count of the failure target to the count of the node itself. The target is shallower, so its count is already final when the node is processed, and each node then holds the number of words that end at it or at some node on its failure chain.

The class keeps one integer `state`, the current node. A call to `query` replaces `state` with `go[state][letter]` and returns `hits[state]`. The stream is never stored. The invariant is that after each call, `state` is the node of the longest suffix of the stream that is a prefix of some word, so the words ending at the newest letter are exactly the words on its failure chain.

**Complexity.**
- **Time** is O(L * 26) to build for total word length L, and O(1) for each `query`, because a query is one table read and one array read.
- **Space** is O(L * 26), because the table has up to L + 1 rows of 26 entries, and each query adds no memory.

```java run
import java.util.ArrayList;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Random;

public final class StreamWordCounter {
    /** Counts the words that end at each streamed letter. */
    static final class WordCounter {
        private static final int ALPHABET = 26;
        private final int[][] go;
        private final int[] hits;
        // state is the only value kept between calls.
        private int state = 0;

        /**
         * Builds the automaton from distinct non-empty words.
         * Time: O(L * 26), because each of up to L + 1 rows is filled once.
         * Space: O(L * 26), because of the transition table.
         * Invariant: after the level-order pass, hits[v] counts the words ending at v or on its failure chain.
         */
        WordCounter(String[] words) {
            // The node count is at most one plus the total word length.
            int cap = 1;
            for (String w : words) cap += w.length();
            // Each row holds the next node for every letter.
            go = new int[cap][ALPHABET];
            hits = new int[cap];
            // fail[v] is the node of the longest proper suffix of v that is also a node.
            int[] fail = new int[cap];
            // real[v * 26 + c] marks genuine trie edges, since 0 is also the root.
            boolean[] real = new boolean[cap * ALPHABET];
            // nodes is the next free node number; the root is node 0.
            int nodes = 1;
            // Insert each word by walking or creating one node per letter.
            for (String w : words) {
                int v = 0;
                for (int j = 0; j < w.length(); j++) {
                    int c = w.charAt(j) - 'a';
                    // A missing edge creates the next node.
                    if (!real[v * ALPHABET + c]) { real[v * ALPHABET + c] = true; go[v][c] = nodes++; }
                    v = go[v][c];
                }
                // One more word ends at this node.
                hits[v]++;
            }
            // The queue visits nodes by depth, so every failure target is finished before its dependents.
            int[] queue = new int[nodes];
            int head = 0, tail = 0;
            // Root children have the root as failure target and need no count change.
            for (int c = 0; c < ALPHABET; c++) if (real[c]) queue[tail++] = go[0][c];
            // Each dequeued node finalizes its count and completes its row.
            while (head < tail) {
                int v = queue[head++];
                // The target is shallower, so its count is final; add the words it ends.
                hits[v] += hits[fail[v]];
                for (int c = 0; c < ALPHABET; c++) {
                    int u = go[v][c];
                    if (real[v * ALPHABET + c]) {
                        // The child's failure target is reached by following the target of v on the same letter.
                        fail[u] = go[fail[v]][c];
                        queue[tail++] = u;
                    } else {
                        // A missing edge takes the result of the failure target, which is already complete.
                        go[v][c] = go[fail[v]][c];
                    }
                }
            }
        }

        /**
         * Consumes one letter and returns how many words end at it.
         * Time: O(1), because of one table read.
         * Space: O(1), because the stream is not stored.
         * Invariant: state is the longest suffix of the stream that is a prefix of some word.
         */
        int query(char letter) {
            // One transition replaces any search through earlier letters.
            state = go[state][letter - 'a'];
            // The stored count already includes words on the failure chain.
            return hits[state];
        }
    }

    /**
     * Brute-force oracle that keeps the whole stream and tests every word.
     * Time: O(q * L) over q queries, because each query tests all words.
     * Space: O(q), because the stream is stored.
     * Invariant: a word counts exactly when the stream ends with it.
     */
    static int[] oracle(String[] words, String stream) {
        // One answer per query.
        int[] out = new int[stream.length()];
        for (int i = 0; i < stream.length(); i++) {
            // Prefix of the stream up to and including letter i.
            String seen = stream.substring(0, i + 1);
            for (String w : words) if (seen.endsWith(w)) out[i]++;
        }
        // Compared with the automaton in main.
        return out;
    }

    static int[] run(String[] words, String stream) {
        // A fresh automaton per scenario.
        WordCounter wc = new WordCounter(words);
        int[] out = new int[stream.length()];
        // The state persists across the calls inside this loop.
        for (int i = 0; i < stream.length(); i++) out[i] = wc.query(stream.charAt(i));
        return out;
    }

    public static void main(String[] args) {
        // Character subtraction has type int, which is why it indexes the table directly.
        Object diff = 'd' - 'a';
        if (!(diff instanceof Integer) || (Integer) diff != 3) throw new AssertionError("char arithmetic");
        // First worked example: bc and c are inherited through failure links.
        if (!java.util.Arrays.equals(run(new String[] {"cd", "abc", "bc", "c"}, "abcd"), new int[] {0, 0, 3, 1})) throw new AssertionError("ex1");
        // Hostile example: nested suffixes give growing counts.
        if (!java.util.Arrays.equals(run(new String[] {"a", "aa", "aaa"}, "aaaa"), new int[] {1, 2, 3, 3})) throw new AssertionError("ex2");
        // A single one-letter word reports every matching letter and no other.
        if (!java.util.Arrays.equals(run(new String[] {"b"}, "abb"), new int[] {0, 1, 1})) throw new AssertionError("single");
        // Random comparison with the oracle; the seed makes any failure reproducible.
        Random rnd = new Random(3494L);
        for (int t = 0; t < 3000; t++) {
            int alpha = 1 + rnd.nextInt(3);
            // A set keeps the words distinct, as the contract requires.
            LinkedHashSet<String> set = new LinkedHashSet<>();
            for (int k = 1 + rnd.nextInt(5); k > 0; k--) {
                StringBuilder w = new StringBuilder();
                for (int i = 1 + rnd.nextInt(4); i > 0; i--) w.append((char) ('a' + rnd.nextInt(alpha)));
                set.add(w.toString());
            }
            String[] words = set.toArray(new String[0]);
            StringBuilder sb = new StringBuilder();
            for (int i = rnd.nextInt(30); i > 0; i--) sb.append((char) ('a' + rnd.nextInt(alpha)));
            if (!java.util.Arrays.equals(run(words, sb.toString()), oracle(words, sb.toString()))) throw new AssertionError("mismatch " + set + " / " + sb);
        }
    }
}
```
