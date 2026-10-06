<!-- solutions-for: 03-wildcard-branching -->
### Solutions For Matching Words With Wildcards

#### Solution: [Build] One Final Wildcard (Author exercise)
<!-- id: tr-one-final-wildcard -->

**Approach.**
The method builds a tree of the words. If the pattern ends with a dot, the walk follows the letters of the pattern before the dot along single edges and stops with false at a missing edge. At the last node the method checks every child for a true flag, because the dot may match any letter. If the pattern has no dot, the method reads the flag of the node after the last letter. The length rule holds because the walk consumes the whole pattern and the answer is read exactly there.

After `i` letters the walk stands on the node whose prefix equals the first `i` letters of the pattern.

**Complexity.**
- **Time** is O(L + m + 26), where `L` is the total length of the words and `m` the pattern length.
- **Space** is O(26 * N) for the nodes.

```java run
import java.util.*;

public final class OneFinalWildcard {
    private static final class Node { final Node[] child = new Node[26]; boolean terminal; }

    /**
     * Returns true when some word matches a pattern with at most one final dot.
     * Time: O(L + m). Space: O(26 * N).
     * Invariant: after i letters the walk stands on the node of the first i pattern letters.
     */
    static boolean matches(String[] words, String pattern) {
        Node root = new Node();
        for (String w : words) {
            Node cur = root;
            for (int i = 0; i < w.length(); i++) {
                int s = w.charAt(i) - 'a';
                if (cur.child[s] == null) cur.child[s] = new Node();
                cur = cur.child[s];
            }
            cur.terminal = true;
        }
        boolean dot = pattern.endsWith(".");
        int letters = dot ? pattern.length() - 1 : pattern.length();
        Node cur = root;
        for (int i = 0; i < letters && cur != null; i++) cur = cur.child[pattern.charAt(i) - 'a'];   // one edge per letter
        if (cur == null) return false;                             // a missing edge rules out every word
        if (!dot) return cur.terminal;                             // no dot: the word must end here
        for (Node next : cur.child) if (next != null && next.terminal) return true;   // the dot tries each child once
        return false;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!matches(new String[] {"bad", "dad"}, "da.")) throw new AssertionError("ex1");
        if (matches(new String[] {"tea", "ten"}, "te")) throw new AssertionError("ex2");
        // A lone dot needs a word of length one, and the empty pattern needs the empty word.
        if (!matches(new String[] {"a"}, ".") || matches(new String[] {"ab"}, ".") || !matches(new String[] {""}, "")) throw new AssertionError("edges");
        // Random inputs must match a direct comparison.
        Random rnd = new Random(1821);
        for (int t = 0; t < 400; t++) {
            String[] w = new String[rnd.nextInt(6)];
            for (int i = 0; i < w.length; i++) w[i] = word(rnd);
            String p = word(rnd) + (rnd.nextBoolean() ? "." : "");
            boolean expect = false;
            for (String x : w) if (fits(x, p)) expect = true;
            if (matches(w, p) != expect) throw new AssertionError("random " + t);
        }
    }

    static boolean fits(String w, String p) {
        if (w.length() != p.length()) return false;
        for (int i = 0; i < w.length(); i++) if (p.charAt(i) != '.' && p.charAt(i) != w.charAt(i)) return false;
        return true;
    }

    static String word(Random r) {
        StringBuilder sb = new StringBuilder();
        for (int j = r.nextInt(4); j > 0; j--) sb.append((char) ('a' + r.nextInt(3)));
        return sb.toString();
    }
}
```

#### Solution: [Vary] Multiple Wildcards (Author exercise)
<!-- id: tr-multiple-wildcards -->

**Approach.**
The method builds the tree and answers each pattern with a recursive call on a node and a position. A letter follows one edge and a missing edge returns false. A dot calls itself on every existing child and returns true at the first child that succeeds. After the last position the call returns the flag of its node. The calls change no state of the tree, so a failed branch needs no undo.

A call for node `v` and position `i` returns true exactly when some word below `v` matches the pattern from position `i` onward.

**Complexity.**
- **Time** is O(L + Q * N) in the worst case, because each pair of a node and a position is visited at most once and a pattern of only dots can visit the whole tree. A pattern without dots costs O(m).
- **Space** is O(26 * N) for the nodes plus O(m) for the recursion stack.

```java run
import java.util.*;

public final class MultipleWildcards {
    private static final class Node { final Node[] child = new Node[26]; boolean terminal; }

    /**
     * Answers each pattern.
     * Time: O(L + Q * N) worst case. Space: O(26 * N + m).
     * Invariant: match(v, i) is true iff some word below v matches the pattern from position i.
     */
    static boolean[] answer(String[] words, String[] patterns) {
        Node root = new Node();
        for (String w : words) {
            Node cur = root;
            for (int i = 0; i < w.length(); i++) {
                int s = w.charAt(i) - 'a';
                if (cur.child[s] == null) cur.child[s] = new Node();
                cur = cur.child[s];
            }
            cur.terminal = true;
        }
        boolean[] out = new boolean[patterns.length];
        for (int j = 0; j < patterns.length; j++) out[j] = match(root, patterns[j], 0);
        return out;
    }

    private static boolean match(Node node, String p, int i) {
        if (i == p.length()) return node.terminal;                 // the pattern ended, so the word must end
        char c = p.charAt(i);
        if (c != '.') {
            Node next = node.child[c - 'a'];                       // a letter follows one edge
            return next != null && match(next, p, i + 1);
        }
        for (Node next : node.child) {                             // a dot tries each existing child
            if (next != null && match(next, p, i + 1)) return true;   // the first success stops the loop
        }
        return false;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!Arrays.equals(answer(new String[] {"cap", "cot"}, new String[] {"c.t", "c.p", "..."}), new boolean[] {true, true, true})) throw new AssertionError("ex1");
        if (!Arrays.equals(answer(new String[] {"ab"}, new String[] {".b", "a..", "b."}), new boolean[] {true, false, false})) throw new AssertionError("ex2");
        // Random inputs must match a direct comparison with every word.
        Random rnd = new Random(1822);
        for (int t = 0; t < 400; t++) {
            String[] w = new String[rnd.nextInt(6)];
            for (int i = 0; i < w.length; i++) w[i] = word(rnd, false);
            String[] p = new String[rnd.nextInt(6)];
            for (int i = 0; i < p.length; i++) p[i] = word(rnd, true);
            boolean[] expect = new boolean[p.length];
            for (int j = 0; j < p.length; j++) for (String x : w) if (fits(x, p[j])) expect[j] = true;
            if (!Arrays.equals(answer(w, p), expect)) throw new AssertionError("random " + t);
        }
    }

    static boolean fits(String w, String p) {
        if (w.length() != p.length()) return false;
        for (int i = 0; i < w.length(); i++) if (p.charAt(i) != '.' && p.charAt(i) != w.charAt(i)) return false;
        return true;
    }

    static String word(Random r, boolean dots) {
        StringBuilder sb = new StringBuilder();
        for (int j = r.nextInt(5); j > 0; j--) sb.append(dots && r.nextInt(3) == 0 ? '.' : (char) ('a' + r.nextInt(3)));
        return sb.toString();
    }
}
```

#### Solution: [Boundary] Wildcard At Root And Missing Length (Author exercise)
<!-- id: tr-wildcard-root-length -->

**Approach.**
The tree stores each distinct word once, so equal entries share one flagged node. A recursive call returns the number of flagged nodes that match the pattern from its position. At a letter the call follows one edge. At a dot it adds the results of all existing children and never stops early, because the answer is a count. After the last position it returns 1 for a flagged node and 0 otherwise, which enforces the length rule. A pattern that starts with a dot begins the same recursion at the root, so no special case exists. The empty pattern returns the flag of the root, which is true only for the empty word.

Each distinct matching word ends at exactly one flagged node, and different words end at different nodes, so no word is counted twice.

**Complexity.**
- **Time** is O(L + Q * N) in the worst case, because a pattern of only dots can visit every node once.
- **Space** is O(26 * N) for the nodes plus O(m) for the recursion stack.

```java run
import java.util.*;

public final class WildcardRootLength {
    private static final class Node { final Node[] child = new Node[26]; boolean terminal; }

    /**
     * Counts distinct words that match each pattern exactly.
     * Time: O(L + Q * N) worst case. Space: O(26 * N + m).
     * Invariant: count(v, i) is the number of distinct words below v that match the pattern from position i.
     */
    static int[] counts(String[] words, String[] patterns) {
        Node root = new Node();
        for (String w : words) {
            Node cur = root;
            for (int i = 0; i < w.length(); i++) {
                int s = w.charAt(i) - 'a';
                if (cur.child[s] == null) cur.child[s] = new Node();
                cur = cur.child[s];
            }
            cur.terminal = true;                                   // equal words share one flagged node
        }
        int[] out = new int[patterns.length];
        for (int j = 0; j < patterns.length; j++) out[j] = count(root, patterns[j], 0);
        return out;
    }

    private static int count(Node node, String p, int i) {
        if (i == p.length()) return node.terminal ? 1 : 0;         // the word must end exactly at the pattern end
        char c = p.charAt(i);
        if (c != '.') {
            Node next = node.child[c - 'a'];
            return next == null ? 0 : count(next, p, i + 1);
        }
        int sum = 0;
        for (Node next : node.child) if (next != null) sum += count(next, p, i + 1);   // a count never stops early
        return sum;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!Arrays.equals(counts(new String[] {"ab", "abc", "ab"}, new String[] {"..", "...", ".", "", "a.c"}), new int[] {1, 1, 0, 0, 1}))
            throw new AssertionError("ex1");
        if (!Arrays.equals(counts(new String[] {"", "z"}, new String[] {"", "."}), new int[] {1, 1})) throw new AssertionError("ex2");
        // Random inputs must match a count over the distinct words.
        Random rnd = new Random(1823);
        for (int t = 0; t < 400; t++) {
            String[] w = new String[rnd.nextInt(7)];
            for (int i = 0; i < w.length; i++) w[i] = word(rnd, false);
            String[] p = new String[rnd.nextInt(6)];
            for (int i = 0; i < p.length; i++) p[i] = word(rnd, true);
            int[] expect = new int[p.length];
            Set<String> distinct = new HashSet<>(Arrays.asList(w));
            for (int j = 0; j < p.length; j++) for (String x : distinct) if (fits(x, p[j])) expect[j]++;
            if (!Arrays.equals(counts(w, p), expect)) throw new AssertionError("random " + t);
        }
    }

    static boolean fits(String w, String p) {
        if (w.length() != p.length()) return false;
        for (int i = 0; i < w.length(); i++) if (p.charAt(i) != '.' && p.charAt(i) != w.charAt(i)) return false;
        return true;
    }

    static String word(Random r, boolean dots) {
        StringBuilder sb = new StringBuilder();
        for (int j = r.nextInt(5); j > 0; j--) sb.append(dots && r.nextInt(3) == 0 ? '.' : (char) ('a' + r.nextInt(3)));
        return sb.toString();
    }
}
```

#### Solution: [Recognize] Design Add and Search Words Data Structure (LeetCode 211)
<!-- id: tr-add-search-words -->

**Approach.**
The class stores words in a tree with 26 slots in each node. The method `addWord` creates missing nodes and flags the last node. The method `search` starts a recursion at the root. A letter follows one edge. A dot loops over the existing children and returns true at the first success. A search reads the tree and writes nothing, so alternating adds and searches stay correct. A query longer than every stored word runs out of children and returns false.

The tree always holds exactly the prefixes of the added words, so a search reflects every earlier add and no earlier search.

**Complexity.**
- **Time** is O(m) for `addWord`, and for `search` it is O(m) without dots and at most O(N) with dots.
- **Space** is O(26 * N) for the nodes plus O(m) for the recursion stack.

```java run
import java.util.*;

public final class AddSearchWords {
    static final class WordDictionary {
        private static final class Node { final Node[] child = new Node[26]; boolean terminal; }
        private final Node root = new Node();

        /** Adds a word. Time: O(m). Space: O(m). */
        void addWord(String word) {
            Node cur = root;
            for (int i = 0; i < word.length(); i++) {
                int s = word.charAt(i) - 'a';
                if (cur.child[s] == null) cur.child[s] = new Node();
                cur = cur.child[s];
            }
            cur.terminal = true;
        }

        /** Returns true when an added word matches the query. Time: O(m) to O(N). Space: O(m). */
        boolean search(String word) { return match(root, word, 0); }

        private boolean match(Node node, String p, int i) {
            if (i == p.length()) return node.terminal;             // a match needs a word that ends here
            char c = p.charAt(i);
            if (c != '.') {
                Node next = node.child[c - 'a'];
                return next != null && match(next, p, i + 1);
            }
            for (Node next : node.child) if (next != null && match(next, p, i + 1)) return true;
            return false;
        }
    }

    public static void main(String[] args) {
        // Example 1 of the exercise.
        WordDictionary d = new WordDictionary();
        d.addWord("bad");
        d.addWord("mad");
        if (d.search("pad") || !d.search("b..")) throw new AssertionError("ex1");
        // Example 2: an add after a failed search must be visible.
        WordDictionary e = new WordDictionary();
        if (e.search("a")) throw new AssertionError("ex2a");
        e.addWord("a");
        if (!e.search(".")) throw new AssertionError("ex2b");
        // A query longer than every stored word fails.
        if (d.search("bad.") || d.search("..")) throw new AssertionError("length");
        // Random interleaved calls must match a scan over a list of words.
        Random rnd = new Random(1824);
        for (int r = 0; r < 200; r++) {
            WordDictionary x = new WordDictionary();
            List<String> list = new ArrayList<>();
            for (int op = 0; op < 30; op++) {
                if (rnd.nextBoolean()) { String w = word(rnd, false); if (!w.isEmpty()) { x.addWord(w); list.add(w); } }
                else {
                    String p = word(rnd, true);
                    if (p.isEmpty()) continue;
                    boolean expect = false;
                    for (String w : list) if (fits(w, p)) expect = true;
                    if (x.search(p) != expect) throw new AssertionError("random " + r);
                }
            }
        }
    }

    static boolean fits(String w, String p) {
        if (w.length() != p.length()) return false;
        for (int i = 0; i < w.length(); i++) if (p.charAt(i) != '.' && p.charAt(i) != w.charAt(i)) return false;
        return true;
    }

    static String word(Random r, boolean dots) {
        StringBuilder sb = new StringBuilder();
        for (int j = r.nextInt(5); j > 0; j--) sb.append(dots && r.nextInt(3) == 0 ? '.' : (char) ('a' + r.nextInt(3)));
        return sb.toString();
    }
}
```
