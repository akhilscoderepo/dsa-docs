<!-- solutions-for: 04-word-break-trie-search -->
### Solutions For Cutting A String Into Words

#### Solution: [Build] Dictionary Ends From One Index (Author exercise)
<!-- id: tr-dictionary-ends-from-index -->

**Approach.**
The method builds a tree of the dictionary and walks it from position `from`. It reads one letter per step and stops at the first missing edge, which is a dead end. A terminal node after reading the letter at position `i` records the end position `i + 1`. The walk goes in increasing position order, so the list is already sorted. No substring is built, and the walk never reads more letters than the longest word.

After reading `k` letters the node represents `s[from..from + k)`, and the recorded ends are exactly the words among those prefixes.

**Complexity.**
- **Time** is O(L + min(n, W)), where `L` is the total length of the dictionary, `W` the longest word and `n` the string length.
- **Space** is O(26 * N) for the nodes plus O(W) for the result.

```java run
import java.util.*;

public final class DictionaryEnds {
    private static final class Node { final Node[] child = new Node[26]; boolean terminal; }

    /**
     * Returns every end position e such that s[from..e) is a dictionary word.
     * Time: O(L + min(n, W)). Space: O(26 * N + W).
     * Invariant: after k letters the node stands for s[from..from+k).
     */
    static int[] ends(String[] dict, String s, int from) {
        Node root = new Node();
        for (String w : dict) {
            Node cur = root;
            for (int i = 0; i < w.length(); i++) {
                int c = w.charAt(i) - 'a';
                if (cur.child[c] == null) cur.child[c] = new Node();
                cur = cur.child[c];
            }
            cur.terminal = true;
        }
        List<Integer> out = new ArrayList<>();
        Node cur = root;
        for (int i = from; i < s.length(); i++) {                  // one letter per step, no substring
            cur = cur.child[s.charAt(i) - 'a'];
            if (cur == null) break;                                // dead end: no word extends these letters
            if (cur.terminal) out.add(i + 1);                      // a word ends after letter i
        }
        int[] r = new int[out.size()];
        for (int i = 0; i < r.length; i++) r[i] = out.get(i);
        return r;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        String[] d = {"cat", "cats", "and", "sand"};
        if (!Arrays.equals(ends(d, "catsand", 0), new int[] {3, 4})) throw new AssertionError("ex1");
        if (ends(d, "catsand", 5).length != 0) throw new AssertionError("ex2");
        // Starting at the string length returns no end.
        if (ends(d, "cat", 3).length != 0) throw new AssertionError("at end");
        // Random inputs must match the substring test against a set.
        Random rnd = new Random(1841);
        for (int t = 0; t < 400; t++) {
            String[] w = new String[rnd.nextInt(6)];
            Set<String> set = new HashSet<>();
            for (int i = 0; i < w.length; i++) { w[i] = word(rnd, 1); set.add(w[i]); }
            String s = word(rnd, 0) + word(rnd, 0);
            int from = rnd.nextInt(s.length() + 1);
            List<Integer> expect = new ArrayList<>();
            for (int e = from + 1; e <= s.length(); e++) if (set.contains(s.substring(from, e))) expect.add(e);
            int[] got = ends(w, s, from);
            if (got.length != expect.size()) throw new AssertionError("random " + t);
            for (int i = 0; i < got.length; i++) if (got[i] != expect.get(i)) throw new AssertionError("random " + t);
        }
    }

    static String word(Random r, int min) {
        StringBuilder sb = new StringBuilder();
        for (int j = min + r.nextInt(4); j > 0; j--) sb.append((char) ('a' + r.nextInt(2)));
        return sb.toString();
    }
}
```

#### Solution: [Vary] One Valid Segmentation On Short Input (Author exercise)
<!-- id: tr-one-valid-segmentation -->

**Approach.**
The method builds the tree and recurses on a start index. A call at the string length returns an empty list, which means that the cutting is complete. Otherwise the call walks the tree from `from` and tries each cut point in increasing order. The first cut point whose recursive call succeeds gives the answer, and the call prepends the word before it. Trying cut points in increasing order makes the first word the shortest possible, and the same rule applies to the rest. A call that finds no successful cut point returns null. The recursion may reach the same start index many times, so it suits short strings, and Chapter 26 shows how to remember results.

A call at `from` returns a cutting of `s[from..]` with the shortest first word, or null when none exists.

**Complexity.**
- **Time** is exponential in `n` in the worst case, because the same start index can be reached by many cut sequences. A call itself costs O(min(n, W)).
- **Space** is O(26 * N) for the nodes plus O(n) for the recursion depth.

```java run
import java.util.*;

public final class OneValidSegmentation {
    private static final class Node { final Node[] child = new Node[26]; boolean terminal; }

    private static Node build(String[] dict) {
        Node root = new Node();
        for (String w : dict) {
            Node cur = root;
            for (int i = 0; i < w.length(); i++) {
                int c = w.charAt(i) - 'a';
                if (cur.child[c] == null) cur.child[c] = new Node();
                cur = cur.child[c];
            }
            cur.terminal = true;
        }
        return root;
    }

    /**
     * Returns the cutting with the shortest first word at every step, or null.
     * Time: exponential worst case. Space: O(26 * N + n).
     * Invariant: cut(from) returns a cutting of s[from..] or null when none exists.
     */
    static String[] segment(String[] dict, String s) {
        List<String> r = cut(build(dict), s, 0);
        return r == null ? null : r.toArray(new String[0]);
    }

    private static List<String> cut(Node root, String s, int from) {
        if (from == s.length()) return new ArrayList<>();          // the string ended at a cut point
        Node cur = root;
        for (int i = from; i < s.length(); i++) {                  // cut points in increasing order
            cur = cur.child[s.charAt(i) - 'a'];
            if (cur == null) break;                                // dead end
            if (cur.terminal) {
                List<String> rest = cut(root, s, i + 1);           // continue after this word
                if (rest != null) { rest.add(0, s.substring(from, i + 1)); return rest; }
            }
        }
        return null;                                               // no cut point reaches the end
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!Arrays.equals(segment(new String[] {"cat", "cats", "and", "sand", "dog"}, "catsanddog"), new String[] {"cat", "sand", "dog"})) throw new AssertionError("ex1");
        if (segment(new String[] {"a", "aa"}, "aaab") != null) throw new AssertionError("ex2");
        // Random inputs must match the best cutting found by trying all cuttings.
        Random rnd = new Random(1842);
        for (int t = 0; t < 400; t++) {
            String[] w = new String[rnd.nextInt(5)];
            Set<String> set = new HashSet<>();
            for (int i = 0; i < w.length; i++) { w[i] = word(rnd, 1); set.add(w[i]); }
            String s = word(rnd, 1) + word(rnd, 0);
            List<List<String>> all = new ArrayList<>();
            all(set, s, 0, new ArrayList<>(), all);
            List<String> best = null;
            for (List<String> c : all) if (best == null || before(c, best)) best = c;
            String[] got = segment(w, s);
            if (best == null ? got != null : (got == null || !Arrays.equals(got, best.toArray(new String[0])))) throw new AssertionError("random " + t);
        }
    }

    // Lists the word lengths in order and compares them, so the shorter first word wins.
    static boolean before(List<String> a, List<String> b) {
        for (int i = 0; i < Math.min(a.size(), b.size()); i++) {
            if (a.get(i).length() != b.get(i).length()) return a.get(i).length() < b.get(i).length();
        }
        return a.size() < b.size();
    }

    static void all(Set<String> set, String s, int from, List<String> cur, List<List<String>> out) {
        if (from == s.length()) { out.add(new ArrayList<>(cur)); return; }
        for (int e = from + 1; e <= s.length(); e++) {
            if (set.contains(s.substring(from, e))) { cur.add(s.substring(from, e)); all(set, s, e, cur, out); cur.remove(cur.size() - 1); }
        }
    }

    static String word(Random r, int min) {
        StringBuilder sb = new StringBuilder();
        for (int j = min + r.nextInt(4); j > 0; j--) sb.append((char) ('a' + r.nextInt(2)));
        return sb.toString();
    }
}
```

#### Solution: [Boundary] Prefix Exists But Word Does Not (Author exercise)
<!-- id: tr-prefix-exists-no-word -->

**Approach.**
The method builds the tree and starts one walk at each position `i`. The walk reads letters while edges exist. It remembers whether it read at least one letter and whether it passed a terminal node. A walk that read a letter and never saw a terminal node counts as stuck. The case where the string ends in the middle of a word is stuck as well, because the loop leaves without a terminal node. A walk that reads zero letters, because the first letter has no edge at the root, does not count.

A walk counts exactly when its path is a prefix of some dictionary word and no node on that path is terminal.

**Complexity.**
- **Time** is O(L + n * W), because each of the `n` walks reads at most `W` letters.
- **Space** is O(26 * N) for the nodes.

```java run
import java.util.*;

public final class PrefixExistsNoWord {
    private static final class Node { final Node[] child = new Node[26]; boolean terminal; }

    /**
     * Counts positions whose walk reads a letter and never meets a terminal node.
     * Time: O(L + n * W). Space: O(26 * N).
     * Invariant: a walk counts iff its path is a word prefix and no node on it is terminal.
     */
    static int stuck(String[] dict, String s) {
        Node root = new Node();
        for (String w : dict) {
            Node cur = root;
            for (int i = 0; i < w.length(); i++) {
                int c = w.charAt(i) - 'a';
                if (cur.child[c] == null) cur.child[c] = new Node();
                cur = cur.child[c];
            }
            cur.terminal = true;
        }
        int count = 0;
        for (int i = 0; i < s.length(); i++) {                     // one walk per position
            Node cur = root;
            int read = 0;
            boolean sawWord = false;
            for (int j = i; j < s.length(); j++) {
                cur = cur.child[s.charAt(j) - 'a'];
                if (cur == null) break;                            // dead end
                read++;
                if (cur.terminal) sawWord = true;                  // a cut point exists at this position
            }
            if (read > 0 && !sawWord) count++;                     // a prefix matched, but no word did
        }
        return count;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (stuck(new String[] {"cats"}, "catcat") != 2) throw new AssertionError("ex1");
        if (stuck(new String[] {"apple", "pen"}, "applepen") != 2) throw new AssertionError("ex2");
        // An empty string has no positions, and a string that ends inside a word counts that position.
        if (stuck(new String[] {"ab"}, "") != 0 || stuck(new String[] {"ab"}, "a") != 1) throw new AssertionError("edges");
        // Random inputs must match a direct startsWith comparison.
        Random rnd = new Random(1843);
        for (int t = 0; t < 400; t++) {
            String[] w = new String[rnd.nextInt(5)];
            for (int i = 0; i < w.length; i++) w[i] = word(rnd, 1);
            String s = word(rnd, 0) + word(rnd, 0);
            int expect = 0;
            for (int i = 0; i < s.length(); i++) {
                boolean prefix = false, word = false;
                for (String x : w) {
                    if (x.startsWith(s.substring(i, i + 1))) {
                        // x begins with the first letter, so a walk reads at least one letter.
                        prefix = true;
                    }
                    if (s.startsWith(x, i)) word = true;
                }
                if (prefix && !word) expect++;
            }
            if (stuck(w, s) != expect) throw new AssertionError("random " + t);
        }
    }

    static String word(Random r, int min) {
        StringBuilder sb = new StringBuilder();
        for (int j = min + r.nextInt(4); j > 0; j--) sb.append((char) ('a' + r.nextInt(2)));
        return sb.toString();
    }
}
```

#### Solution: [Recognize] Explain Trie-Based Word Break State (Author exercise)
<!-- id: tr-word-break-state-count -->

**Approach.**
The state of one call is its start index, because the rest of the work depends only on the suffix that begins there. The method runs the plain recursion with the tree walk and counts every call, including the call at the string length. It stores the start index of each call in a set. The first returned number is the number of calls, and the second is the size of the set. When the first number exceeds the second, some call repeats a state that an earlier call already searched. Memoization, which Chapter 26 teaches, would run each start index once, so the calls would drop to the second number.

The set of start indices holds each different state once, and the counter holds one entry for each call.

**Complexity.**
- **Time** is exponential in `n` in the worst case, and each call costs O(min(n, W)) for the walk.
- **Space** is O(26 * N) for the nodes plus O(n) for the recursion depth and the set.

```java run
import java.util.*;

public final class WordBreakStateCount {
    private static final class Node { final Node[] child = new Node[26]; boolean terminal; }

    private static int calls;
    private static Set<Integer> starts;

    /**
     * Returns {total calls, different start indices} of the plain recursion.
     * Time: exponential worst case. Space: O(26 * N + n).
     * Invariant: the state of a call is its start index, and calls beyond the different starts are repeats.
     */
    static int[] measure(String[] dict, String s) {
        Node root = new Node();
        for (String w : dict) {
            Node cur = root;
            for (int i = 0; i < w.length(); i++) {
                int c = w.charAt(i) - 'a';
                if (cur.child[c] == null) cur.child[c] = new Node();
                cur = cur.child[c];
            }
            cur.terminal = true;
        }
        calls = 0;
        starts = new HashSet<>();
        run(root, s, 0);
        return new int[] {calls, starts.size()};
    }

    private static void run(Node root, String s, int from) {
        calls++;                                                   // every call counts, repeats included
        starts.add(from);                                          // the set keeps each state once
        Node cur = root;
        for (int i = from; i < s.length(); i++) {                  // walk the dictionary words at from
            cur = cur.child[s.charAt(i) - 'a'];
            if (cur == null) break;                                // dead end
            if (cur.terminal) run(root, s, i + 1);                 // a call for every cut point, never stopping early
        }
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!Arrays.equals(measure(new String[] {"a", "aa"}, "aaab"), new int[] {7, 4})) throw new AssertionError("ex1");
        if (!Arrays.equals(measure(new String[] {"ab"}, "abab"), new int[] {3, 3})) throw new AssertionError("ex2");
        // Repeats grow quickly: the calls on a run of a's with a dictionary of a and aa follow Fibonacci numbers.
        int[] r = measure(new String[] {"a", "aa"}, "aaaaaaaaaaaaaaaaaaab");
        if (r[0] <= 2 * r[1]) throw new AssertionError("repeats must dominate");
        // Random inputs must match a set-based recursion with substrings.
        Random rnd = new Random(1844);
        for (int t = 0; t < 300; t++) {
            String[] w = new String[rnd.nextInt(4)];
            Set<String> set = new HashSet<>();
            for (int i = 0; i < w.length; i++) { w[i] = word(rnd, 1); set.add(w[i]); }
            String s = word(rnd, 1) + word(rnd, 0) + word(rnd, 0);
            int[] expectCalls = new int[1];
            Set<Integer> st = new HashSet<>();
            slow(set, s, 0, expectCalls, st);
            if (!Arrays.equals(measure(w, s), new int[] {expectCalls[0], st.size()})) throw new AssertionError("random " + t);
        }
    }

    static void slow(Set<String> set, String s, int from, int[] calls, Set<Integer> st) {
        calls[0]++;
        st.add(from);
        for (int e = from + 1; e <= s.length(); e++) if (set.contains(s.substring(from, e))) slow(set, s, e, calls, st);
    }

    static String word(Random r, int min) {
        StringBuilder sb = new StringBuilder();
        for (int j = min + r.nextInt(3); j > 0; j--) sb.append((char) ('a' + r.nextInt(2)));
        return sb.toString();
    }
}
```
