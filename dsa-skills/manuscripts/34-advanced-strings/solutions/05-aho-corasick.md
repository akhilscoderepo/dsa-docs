<!-- solutions-for: 05-aho-corasick -->
### Solutions For Matching Many Patterns

#### Solution: [Build] Trie Failure Links (Author exercise)
<!-- id: as-trie-failure-links -->

**Approach.**
The code inserts the patterns into a trie whose absent edges hold -1, so nodes receive numbers in creation order. A queue then visits nodes in level order, starting with the children of the root, whose failure link is the root. When the loop dequeues a node `v`, every shallower node already has a finished table row. For each letter `c`, a missing child of `v` copies the entry `go[fail[v]][c]`. A real child `u` gets the failure link `go[fail[v]][c]`, which is the node reached by the longest proper suffix of `u` that is still a trie prefix.

The invariant is that a dequeued node has a correct failure link and that every row of a shallower node is complete. That is why each lookup in `go[fail[v]]` reads a finished row. The harness also asserts two Java facts used by the code: a new `int` array is filled with zeros, and `'c' - 'a'` is the `int` 2.

**Complexity.**
- **Time** is O(L * 26), because the fill touches every one of the `L + 1` rows once per letter, where `L` is the total pattern length.
- **Space** is O(L * 26), because the table has `L + 1` rows of 26 entries, and the queue holds at most one entry per node.

```java run
import java.util.*;

public class AcFailLinks {
    /**
     * Returns the failure link of every trie node, with nodes numbered in creation order.
     * Time: O(L * 26), one table-row fill per node.
     * Space: O(L * 26), the dense table dominates.
     * Invariant: a dequeued node has a correct link, and all shallower rows are complete.
     */
    static int[] failLinks(String[] patterns) {
        // Upper bound on node count: one node per inserted character plus the root.
        int cap = 1;
        for (String p : patterns) cap += p.length();
        // Each row holds the 26 transitions; -1 marks an edge that does not exist yet.
        int[][] go = new int[cap][26];
        for (int[] row : go) Arrays.fill(row, -1);
        int nodes = 1;
        // Insert each pattern; a new node takes the next unused number.
        for (String p : patterns) {
            int v = 0;
            for (int k = 0; k < p.length(); k++) {
                // The letter offset is already an int, so it indexes the row directly.
                int c = p.charAt(k) - 'a';
                // Create the child only when the edge is absent; creation order fixes the numbering.
                if (go[v][c] == -1) go[v][c] = nodes++;
                v = go[v][c];
            }
        }
        // Zero-filled by Java, so every link starts at the root until the loop sets it.
        int[] fail = new int[nodes];
        int[] queue = new int[nodes];
        int head = 0, tail = 0;
        // Depth-1 nodes keep link 0 and enter the queue; missing root edges loop to the root.
        for (int c = 0; c < 26; c++) {
            int u = go[0][c];
            if (u == -1) go[0][c] = 0; else queue[tail++] = u;
        }
        // Level order: a node leaves the queue only after all shallower nodes did.
        while (head < tail) {
            int v = queue[head++];
            for (int c = 0; c < 26; c++) {
                int u = go[v][c];
                // Missing child: borrow the transition of the fallback node, whose row is complete.
                if (u == -1) go[v][c] = go[fail[v]][c];
                // Real child: its link is where the fallback node would go on the same letter.
                else { fail[u] = go[fail[v]][c]; queue[tail++] = u; }
            }
        }
        return fail;
    }

    /**
     * Oracle: finds each link by comparing node strings, using substring allocation freely.
     * Time: O(L^3) in the worst case, which is acceptable for tiny inputs.
     * Space: O(L^2) for the node strings.
     * Invariant: the link is the longest proper suffix of the node string that is a node string.
     */
    static int[] oracle(String[] patterns) {
        // Map every trie prefix to its creation number; the empty string is the root.
        LinkedHashMap<String, Integer> id = new LinkedHashMap<>();
        id.put("", 0);
        for (String p : patterns)
            for (int len = 1; len <= p.length(); len++)
                id.putIfAbsent(p.substring(0, len), id.size());
        int[] fail = new int[id.size()];
        // Try suffixes from longest to shortest and keep the first that is a node.
        for (Map.Entry<String, Integer> e : id.entrySet()) {
            String s = e.getKey();
            for (int from = 1; from < s.length(); from++) {
                Integer hit = id.get(s.substring(from));
                if (hit != null) { fail[e.getValue()] = hit; break; }
            }
        }
        return fail;
    }

    public static void main(String[] args) {
        // Java facts the method relies on: zero-filled arrays and int letter offsets.
        int[] zeros = new int[3];
        if (zeros[2] != 0 || ('c' - 'a') != 2) throw new AssertionError("java facts");
        // Fixed examples from the exercise.
        if (!Arrays.equals(failLinks(new String[] {"he", "she", "his", "hers"}), new int[] {0, 0, 0, 0, 1, 2, 0, 3, 0, 3}))
            throw new AssertionError("example 1");
        if (!Arrays.equals(failLinks(new String[] {"abab", "baba"}), new int[] {0, 0, 5, 6, 7, 0, 1, 2, 3}))
            throw new AssertionError("example 2");
        // Random patterns over a small alphabet create many suffix relations.
        Random rnd = new Random(34051);
        for (int t = 0; t < 3000; t++) {
            LinkedHashSet<String> set = new LinkedHashSet<>();
            int k = 1 + rnd.nextInt(5);
            for (int j = 0; j < k; j++) {
                StringBuilder sb = new StringBuilder();
                int len = 1 + rnd.nextInt(6);
                for (int x = 0; x < len; x++) sb.append((char) ('a' + rnd.nextInt(3)));
                set.add(sb.toString());
            }
            String[] pats = set.toArray(new String[0]);
            // The fast version must match the substring-based oracle.
            if (!Arrays.equals(failLinks(pats), oracle(pats))) throw new AssertionError("mismatch " + Arrays.toString(pats));
        }
    }
}
```

#### Solution: [Vary] Multi-Pattern Scan (Author exercise)
<!-- id: as-multi-pattern-scan -->

**Approach.**
This solution marks absent edges with 0, which is safe during insertion because no edge ever points back to the root. It records the pattern index at each terminal node, then fills the failure links and the output links in one level-order pass. The output link of a node `v` is the fallback node `fail[v]` when a pattern ends there, and otherwise the output link of `fail[v]`. The scan advances one table lookup per text character and then walks the output links from the current node, adding one to the count of each pattern it visits.

The invariant is that after reading `text[0..i]` the state is the node of the longest suffix that is a trie prefix, so every pattern ending at `i` lies on the chain formed by the state and its output links. Overlapping occurrences need no special handling, because the state never resets after a match.

**Complexity.**
- **Time** is O(L * 26 + n + z), because the build fills the table, each text character costs one lookup, and each output link followed counts one occurrence, where `z` is the total number of occurrences.
- **Space** is O(L * 26), because the table dominates, and the counts take one entry per pattern.

```java run
import java.util.*;

public class AcMultiScan {
    /**
     * Counts the occurrences of every pattern in the text, overlaps included.
     * Time: O(L * 26 + n + z) for total pattern length L, text length n and z occurrences.
     * Space: O(L * 26) for the table plus O(k) for the counts.
     * Invariant: the state is the longest suffix of the text read so far that is a trie prefix.
     */
    static int[] countMatches(String[] patterns, String text) {
        int cap = 1;
        for (String p : patterns) cap += p.length();
        // Zero means "no edge" during insertion, because no edge ever leads back to the root.
        int[][] go = new int[cap][26];
        int[] id = new int[cap];
        // -1 means no pattern ends at the node.
        Arrays.fill(id, -1);
        int nodes = 1;
        for (int k = 0; k < patterns.length; k++) {
            int v = 0;
            for (int j = 0; j < patterns[k].length(); j++) {
                int c = patterns[k].charAt(j) - 'a';
                // An absent edge reads 0; allocate the next node number for it.
                if (go[v][c] == 0) go[v][c] = nodes++;
                v = go[v][c];
            }
            // Remember which pattern ends at this node.
            id[v] = k;
        }
        int[] fail = new int[nodes];
        int[] link = new int[nodes];
        ArrayDeque<Integer> queue = new ArrayDeque<>();
        // Children of the root fall back to the root and start the level order.
        for (int c = 0; c < 26; c++) if (go[0][c] != 0) queue.add(go[0][c]);
        while (!queue.isEmpty()) {
            int v = queue.poll();
            int f = fail[v];
            // The nearest pattern end on the fallback chain: the fallback itself, or its own nearest.
            link[v] = id[f] >= 0 ? f : link[f];
            for (int c = 0; c < 26; c++) {
                int u = go[v][c];
                // Row v still holds only real children, so 0 here means the edge is absent.
                if (u == 0) go[v][c] = go[f][c];
                else { fail[u] = go[f][c]; queue.add(u); }
            }
        }
        int[] counts = new int[patterns.length];
        int state = 0;
        // One lookup per text character: the table already contains the fallback.
        for (int i = 0; i < text.length(); i++) {
            state = go[state][text.charAt(i) - 'a'];
            // Walk the node itself if it ends a pattern, then each output link; every step is one match.
            for (int m = id[state] >= 0 ? state : link[state]; m != 0; m = link[m]) counts[id[m]]++;
        }
        return counts;
    }

    /**
     * Oracle: tests every pattern at every start position with regionMatches.
     * Time: O(n * L). Space: O(k).
     * Invariant: counts[k] equals the number of starts where patterns[k] matches.
     */
    static int[] oracle(String[] patterns, String text) {
        int[] counts = new int[patterns.length];
        for (int k = 0; k < patterns.length; k++)
            for (int s = 0; s + patterns[k].length() <= text.length(); s++)
                if (text.regionMatches(s, patterns[k], 0, patterns[k].length())) counts[k]++;
        return counts;
    }

    public static void main(String[] args) {
        // Fixed examples from the exercise.
        if (!Arrays.equals(countMatches(new String[] {"he", "she", "his", "hers"}, "ushers"), new int[] {1, 1, 0, 1}))
            throw new AssertionError("example 1");
        if (!Arrays.equals(countMatches(new String[] {"a", "aa"}, "aaaa"), new int[] {4, 3}))
            throw new AssertionError("example 2");
        // An empty text reports nothing.
        if (!Arrays.equals(countMatches(new String[] {"a"}, ""), new int[] {0})) throw new AssertionError("empty text");
        // Random patterns and texts over {a, b, c} produce many overlaps and nested patterns.
        Random rnd = new Random(34052);
        for (int t = 0; t < 3000; t++) {
            LinkedHashSet<String> set = new LinkedHashSet<>();
            int k = 1 + rnd.nextInt(5);
            for (int j = 0; j < k; j++) {
                StringBuilder sb = new StringBuilder();
                int len = 1 + rnd.nextInt(4);
                for (int x = 0; x < len; x++) sb.append((char) ('a' + rnd.nextInt(3)));
                set.add(sb.toString());
            }
            String[] pats = set.toArray(new String[0]);
            StringBuilder tx = new StringBuilder();
            int n = rnd.nextInt(30);
            for (int x = 0; x < n; x++) tx.append((char) ('a' + rnd.nextInt(3)));
            // The automaton must agree with the per-pattern oracle.
            if (!Arrays.equals(countMatches(pats, tx.toString()), oracle(pats, tx.toString())))
                throw new AssertionError("mismatch " + Arrays.toString(pats) + " " + tx);
        }
    }
}
```

#### Solution: [Boundary] Suffix Pattern Matches (Author exercise)
<!-- id: as-suffix-pattern-matches -->

**Approach.**
When one pattern is a suffix of another, reaching the longer pattern's node also completes the shorter one, yet the shorter pattern's node is not the current state. The fix is to store at each node the number of patterns that end there or on its failure chain. The value of a node is one if a pattern ends exactly there, plus the value of its failure link. The level-order loop computes it when the node is dequeued, because the failure link is shallower and already has its value.

With that value the scan needs no chain walk. After each text character the answer for that position is the value of the current state. The invariant is that `inherited[v]` equals the number of patterns that are suffixes of the string of `v`, so the entry at index `i` counts exactly the patterns that finish at `i`. For `a`, `aa` and `aaa` the node `aaa` has value 3, because the two shorter patterns are suffixes of it.

**Complexity.**
- **Time** is O(L * 26 + n), because the build fills the table once and the scan does one lookup and one read per text character.
- **Space** is O(L * 26 + n), because of the table and the answer array of length `n`.

```java run
import java.util.*;

public class AcSuffixMatches {
    /**
     * For each text index, counts the patterns that finish at that index.
     * Time: O(L * 26 + n), one table lookup per text letter.
     * Space: O(L * 26 + n) for the table and the answer.
     * Invariant: inherited[v] counts the patterns that are suffixes of the string of node v.
     */
    static int[] endCounts(String[] patterns, String text) {
        int cap = 1;
        for (String p : patterns) cap += p.length();
        int[][] go = new int[cap][26];
        // own[v] is 1 when a pattern ends exactly at v.
        int[] own = new int[cap];
        int nodes = 1;
        for (String p : patterns) {
            int v = 0;
            for (int j = 0; j < p.length(); j++) {
                int c = p.charAt(j) - 'a';
                // Zero is the absent marker while inserting.
                if (go[v][c] == 0) go[v][c] = nodes++;
                v = go[v][c];
            }
            own[v] = 1;
        }
        int[] fail = new int[nodes];
        // inherited[v] = own[v] + inherited[fail[v]], filled in level order.
        int[] inherited = new int[nodes];
        int[] queue = new int[nodes];
        int head = 0, tail = 0;
        for (int c = 0; c < 26; c++) if (go[0][c] != 0) queue[tail++] = go[0][c];
        while (head < tail) {
            int v = queue[head++];
            int f = fail[v];
            // The failure link is shallower, so its inherited count is final already.
            inherited[v] = own[v] + inherited[f];
            for (int c = 0; c < 26; c++) {
                int u = go[v][c];
                if (u == 0) go[v][c] = go[f][c];
                else { fail[u] = go[f][c]; queue[tail++] = u; }
            }
        }
        int[] ends = new int[text.length()];
        int state = 0;
        // Scan once; the answer at index i is read from the state alone.
        for (int i = 0; i < text.length(); i++) {
            state = go[state][text.charAt(i) - 'a'];
            ends[i] = inherited[state];
        }
        return ends;
    }

    /**
     * Oracle: counts, for each index, the patterns whose last character lands there.
     * Time: O(n * L). Space: O(n).
     * Invariant: ends[i] counts patterns p with text[i - |p| + 1 .. i] equal to p.
     */
    static int[] oracle(String[] patterns, String text) {
        int[] ends = new int[text.length()];
        for (String p : patterns)
            for (int s = 0; s + p.length() <= text.length(); s++)
                if (text.regionMatches(s, p, 0, p.length())) ends[s + p.length() - 1]++;
        return ends;
    }

    public static void main(String[] args) {
        // Fixed examples from the exercise.
        if (!Arrays.equals(endCounts(new String[] {"he", "she", "hers"}, "ushers"), new int[] {0, 0, 0, 2, 0, 1}))
            throw new AssertionError("example 1");
        if (!Arrays.equals(endCounts(new String[] {"a", "aa", "aaa"}, "aaaa"), new int[] {1, 2, 3, 3}))
            throw new AssertionError("example 2");
        // Random patterns over {a, b} make suffix patterns common.
        Random rnd = new Random(34053);
        for (int t = 0; t < 3000; t++) {
            LinkedHashSet<String> set = new LinkedHashSet<>();
            int k = 1 + rnd.nextInt(6);
            for (int j = 0; j < k; j++) {
                StringBuilder sb = new StringBuilder();
                int len = 1 + rnd.nextInt(4);
                for (int x = 0; x < len; x++) sb.append((char) ('a' + rnd.nextInt(2)));
                set.add(sb.toString());
            }
            String[] pats = set.toArray(new String[0]);
            StringBuilder tx = new StringBuilder();
            int n = rnd.nextInt(25);
            for (int x = 0; x < n; x++) tx.append((char) ('a' + rnd.nextInt(2)));
            // The inherited counts must match the position-by-position oracle.
            if (!Arrays.equals(endCounts(pats, tx.toString()), oracle(pats, tx.toString())))
                throw new AssertionError("mismatch " + Arrays.toString(pats) + " " + tx);
        }
    }
}
```

#### Solution: [Recognize] Stream of Characters (LeetCode 1032)
<!-- id: as-stream-of-characters -->

**Approach.**
The class builds the automaton once in its constructor and keeps one `int` field `state` between calls. A call to `query` moves the state by one table lookup and returns a precomputed boolean for the new node. The boolean for a node is true when a word ends at the node or when the boolean of its failure link is true. The level-order loop computes it when the node is dequeued, because the failure link is shallower. This single boolean per node is the compact form of the output links, since the problem asks only whether some word matches and not which one.

The invariant is that after each call `state` is the node of the longest suffix of the stream that is a prefix of some word. A word is a suffix of the stream exactly when its node lies on the failure chain of `state`, so the boolean answers the question. The stream itself is never stored, so memory does not grow with the number of calls.

**Complexity.**
- **Time** is O(L * 26) for construction and O(1) per `query`, because a query is one table lookup and one array read.
- **Space** is O(L * 26), because the table dominates, and the stream is not stored.

```java run
import java.util.*;

public class AcStreamRecognize {
    /** Answers whether some word is a suffix of the stream appended so far. */
    static final class StreamChecker {
        private final int[][] go;
        private final boolean[] hit;
        private int state;

        /**
         * Builds the automaton over the words.
         * Time: O(L * 26). Space: O(L * 26).
         * Invariant: hit[v] is true when some word is a suffix of the string of node v.
         */
        StreamChecker(String[] words) {
            int cap = 1;
            for (String w : words) cap += w.length();
            go = new int[cap][26];
            boolean[] ends = new boolean[cap];
            int nodes = 1;
            for (String w : words) {
                int v = 0;
                for (int j = 0; j < w.length(); j++) {
                    int c = w.charAt(j) - 'a';
                    // Zero marks an absent edge until the level-order fill.
                    if (go[v][c] == 0) go[v][c] = nodes++;
                    v = go[v][c];
                }
                ends[v] = true;
            }
            hit = new boolean[nodes];
            int[] fail = new int[nodes];
            int[] queue = new int[nodes];
            int head = 0, tail = 0;
            for (int c = 0; c < 26; c++) if (go[0][c] != 0) queue[tail++] = go[0][c];
            while (head < tail) {
                int v = queue[head++];
                int f = fail[v];
                // A word ends here, or one ends on the fallback chain.
                hit[v] = ends[v] || hit[f];
                for (int c = 0; c < 26; c++) {
                    int u = go[v][c];
                    if (u == 0) go[v][c] = go[f][c];
                    else { fail[u] = go[f][c]; queue[tail++] = u; }
                }
            }
        }

        /**
         * Appends one letter and reports whether some word is now a suffix of the stream.
         * Time: O(1), one lookup. Space: O(1).
         * Invariant: state is the longest suffix of the stream that is a prefix of some word.
         */
        boolean query(char letter) {
            // One lookup moves the state; the table already holds the fallback.
            state = go[state][letter - 'a'];
            // The precomputed flag covers the whole failure chain.
            return hit[state];
        }
    }

    /**
     * Oracle: keeps the whole stream and tests endsWith for every word.
     * Time: O(L) per call. Space: O(stream length).
     * Invariant: the answer is true exactly when some word is a suffix of the stream.
     */
    static boolean oracleQuery(StringBuilder stream, String[] words, char letter) {
        stream.append(letter);
        for (String w : words) if (stream.length() >= w.length() && stream.substring(stream.length() - w.length()).equals(w)) return true;
        return false;
    }

    public static void main(String[] args) {
        // Example 1 from the exercise.
        StreamChecker a = new StreamChecker(new String[] {"rat", "at", "tea"});
        boolean[] want1 = {false, false, true, false, true};
        String q1 = "ratea";
        for (int i = 0; i < 5; i++) if (a.query(q1.charAt(i)) != want1[i]) throw new AssertionError("example 1 at " + i);
        // Example 2: the third query is true only through the inherited word bc.
        StreamChecker b = new StreamChecker(new String[] {"abcd", "bc"});
        boolean[] want2 = {false, false, true, true, false};
        String q2 = "abcdc";
        for (int i = 0; i < 5; i++) if (b.query(q2.charAt(i)) != want2[i]) throw new AssertionError("example 2 at " + i);
        // Random words and streams over {a, b, c}; state must persist across many calls.
        Random rnd = new Random(34054);
        for (int t = 0; t < 2000; t++) {
            LinkedHashSet<String> set = new LinkedHashSet<>();
            int k = 1 + rnd.nextInt(5);
            for (int j = 0; j < k; j++) {
                StringBuilder sb = new StringBuilder();
                int len = 1 + rnd.nextInt(4);
                for (int x = 0; x < len; x++) sb.append((char) ('a' + rnd.nextInt(3)));
                set.add(sb.toString());
            }
            String[] words = set.toArray(new String[0]);
            StreamChecker sc = new StreamChecker(words);
            StringBuilder stream = new StringBuilder();
            for (int x = 0; x < 40; x++) {
                char ch = (char) ('a' + rnd.nextInt(3));
                // Each answer must equal the endsWith oracle on the full stream.
                if (sc.query(ch) != oracleQuery(stream, words, ch)) throw new AssertionError("mismatch " + Arrays.toString(words) + " at " + x);
            }
        }
    }
}
```
