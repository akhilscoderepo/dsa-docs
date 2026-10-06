<!-- solutions-for: 91-look-up-prefixes-in-a-dictionary -->
### Solutions For Looking Up Prefixes

#### Solution: [Build] Implement Trie (LeetCode 208)
<!-- id: tr-combo-longest-stored-prefix -->

**Approach.**
The class keeps a root node with a map of children and a terminal flag. The methods `insert`, `search` and `startsWith` follow the edges of the string, as in the first lesson. The new method `longestMatch` walks the query and counts the edges it follows. A missing edge ends the walk and returns the count, and it does not fail the call. The root counts as depth 0, so a query with no shared first letter returns 0, and a query that is a full prefix of a stored word returns its own length.

After `k` followed edges the walk stands on a node whose path equals the first `k` characters of the query.

**Complexity.**
- **Time** is O(m) per call for a string of `m` characters.
- **Space** is O(L) for the letters of all inserted words.

```java run
import java.util.*;

public final class ComboLongestStoredPrefix {
    static final class Trie {
        private static final class Node { final Map<Character, Node> next = new HashMap<>(); boolean terminal; }
        private final Node root = new Node();

        /** Inserts a word. Time: O(m). Space: O(m). */
        void insert(String word) {
            Node cur = root;
            for (int i = 0; i < word.length(); i++) cur = cur.next.computeIfAbsent(word.charAt(i), c -> new Node());
            cur.terminal = true;
        }

        private Node walk(String s) {
            Node cur = root;
            for (int i = 0; i < s.length() && cur != null; i++) cur = cur.next.get(s.charAt(i));
            return cur;
        }

        /** Returns true when the exact word is stored. Time: O(m). Space: O(1). */
        boolean search(String word) { Node n = walk(word); return n != null && n.terminal; }

        /** Returns true when a stored word starts with prefix. Time: O(m). Space: O(1). */
        boolean startsWith(String prefix) { return walk(prefix) != null; }

        /** Returns the length of the longest prefix of query that prefixes a stored word. Time: O(m). Space: O(1). */
        int longestMatch(String query) {
            Node cur = root;
            int k = 0;
            while (k < query.length()) {                           // one edge per matched character
                Node next = cur.next.get(query.charAt(k));
                if (next == null) break;                           // a missing edge ends the walk without failing
                cur = next;
                k++;
            }
            return k;
        }
    }

    public static void main(String[] args) {
        // Example 1: the query plant shares four letters with planet.
        Trie t = new Trie();
        t.insert("planet");
        if (t.longestMatch("plant") != 4 || t.longestMatch("zoo") != 0) throw new AssertionError("ex1");
        // Example 2: abc is not a prefix of ab, yet the longest match is 2.
        Trie u = new Trie();
        u.insert("ab");
        if (u.startsWith("abc") || u.longestMatch("abc") != 2) throw new AssertionError("ex2");
        // A full word returns its own length, and an empty tree returns 0.
        if (t.longestMatch("planet") != 6 || new Trie().longestMatch("a") != 0) throw new AssertionError("edges");
        // Random operations must match a scan over the stored words.
        Random rnd = new Random(1861);
        for (int r = 0; r < 200; r++) {
            Trie x = new Trie();
            List<String> list = new ArrayList<>();
            for (int op = 0; op < 20; op++) {
                String s = "a" + word(rnd);
                if (rnd.nextBoolean()) { x.insert(s); list.add(s); }
                int expect = 0;
                for (String w : list) {
                    int k = 0;
                    while (k < w.length() && k < s.length() && w.charAt(k) == s.charAt(k)) k++;
                    expect = Math.max(expect, k);
                }
                if (x.longestMatch(s) != expect) throw new AssertionError("random " + r);
            }
        }
    }

    static String word(Random r) {
        StringBuilder sb = new StringBuilder();
        for (int j = r.nextInt(5); j > 0; j--) sb.append((char) ('a' + r.nextInt(2)));
        return sb.toString();
    }
}
```

#### Solution: [Vary] Design Add and Search Words Data Structure (LeetCode 211)
<!-- id: tr-combo-smallest-match -->

**Approach.**
The class stores words in a tree with 26 child slots in each node. The method `smallestMatch` runs a depth-first search that builds the matched word in a `StringBuilder`. A letter of the pattern follows one slot. A dot loops over the slots in alphabetical order. The first call that reaches the end of the pattern on a flagged node returns the word at once. All matching words have the pattern length, so the lexicographic order equals the order of the letters from left to right, and the search visits the smaller letter first. The search removes the last letter from the builder after a failed child. That undo restores only the traversal state, and the tree stays unchanged.

The first successful path in alphabetical order is the lexicographically smallest matching word.

**Complexity.**
- **Time** is O(m) for `addWord`. For `smallestMatch` it is O(m) without dots and at most O(N * m) with dots, where each path copy costs O(m).
- **Space** is O(26 * N) for the nodes plus O(m) for the recursion and the builder.

```java run
import java.util.*;

public final class ComboSmallestMatch {
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

        /** Returns the smallest matching word or the empty string. Time: O(N * m) worst case. Space: O(m). */
        String smallestMatch(String pattern) {
            StringBuilder path = new StringBuilder();
            return find(root, pattern, 0, path) ? path.toString() : "";
        }

        private boolean find(Node node, String p, int i, StringBuilder path) {
            if (i == p.length()) return node.terminal;             // a match needs a word that ends here
            char c = p.charAt(i);
            int from = c == '.' ? 0 : c - 'a';
            int to = c == '.' ? 25 : c - 'a';
            for (int s = from; s <= to; s++) {                     // alphabetical order gives the smallest word first
                if (node.child[s] == null) continue;
                path.append((char) ('a' + s));
                if (find(node.child[s], p, i + 1, path)) return true;
                path.setLength(path.length() - 1);                 // undo the traversal state only, never the tree
            }
            return false;
        }
    }

    public static void main(String[] args) {
        // Example 1 of the exercise.
        WordDictionary d = new WordDictionary();
        d.addWord("mad");
        d.addWord("bad");
        d.addWord("bud");
        if (!d.smallestMatch(".ad").equals("bad") || !d.smallestMatch("b.d").equals("bad")) throw new AssertionError("ex1");
        // Example 2: a shorter query does not match a longer word.
        WordDictionary e = new WordDictionary();
        e.addWord("dog");
        if (!e.smallestMatch("do").isEmpty() || !e.smallestMatch("d..").equals("dog")) throw new AssertionError("ex2");
        // A failed search leaves the tree unchanged.
        if (!e.smallestMatch("x..").isEmpty() || !e.smallestMatch("...").equals("dog")) throw new AssertionError("undo");
        // Random interleaved calls must match a sorted scan.
        Random rnd = new Random(1862);
        for (int r = 0; r < 200; r++) {
            WordDictionary x = new WordDictionary();
            TreeSet<String> set = new TreeSet<>();
            for (int op = 0; op < 25; op++) {
                if (rnd.nextBoolean()) { String w = word(rnd, false); if (!w.isEmpty()) { x.addWord(w); set.add(w); } }
                else {
                    String p = word(rnd, true);
                    if (p.isEmpty()) continue;
                    String expect = "";
                    for (String w : set) if (fits(w, p)) { expect = w; break; }
                    if (!x.smallestMatch(p).equals(expect)) throw new AssertionError("random " + r);
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

#### Solution: [Boundary] Replace Words (LeetCode 648)
<!-- id: tr-combo-replace-words -->

**Approach.**
The method stores the roots in a tree with a terminal flag. It splits the sentence at spaces and replaces each word by the result of one walk. The walk reads the letters of the word and follows edges. A missing edge returns the word unchanged. The first flagged node returns the letters read so far, and that is the shortest root because the walk reads letters in order and stops at once. A word that ends before any flag also stays unchanged. The method joins the results with single spaces.

At each step the current node stands for all roots that agree with the letters read, and the first flagged node gives the shortest root.

**Complexity.**
- **Time** is O(R + S), where `R` is the total length of the roots and `S` the length of the sentence, because each word costs at most its own length.
- **Space** is O(R) for the tree plus O(S) for the output.

```java run
import java.util.*;

public final class ComboReplaceWords {
    private static final class Node { final Node[] child = new Node[26]; boolean terminal; }

    /**
     * Replaces each word with its shortest root prefix, or leaves it unchanged.
     * Time: O(R + S). Space: O(R + S).
     * Invariant: the walk stands on the node of the letters read, which stands for all roots that agree with them.
     */
    static String replace(String[] roots, String sentence) {
        Node root = new Node();
        for (String r : roots) {
            Node cur = root;
            for (int i = 0; i < r.length(); i++) {
                int s = r.charAt(i) - 'a';
                if (cur.child[s] == null) cur.child[s] = new Node();
                cur = cur.child[s];
            }
            cur.terminal = true;
        }
        StringBuilder out = new StringBuilder();
        for (String w : sentence.split(" ")) {
            if (out.length() > 0) out.append(' ');                 // single spaces between words
            Node cur = root;
            String result = w;
            for (int i = 0; i < w.length(); i++) {
                cur = cur.child[w.charAt(i) - 'a'];
                if (cur == null) break;                            // no root agrees, so the word stays
                if (cur.terminal) { result = w.substring(0, i + 1); break; }   // the first flag is the shortest root
            }
            out.append(result);
        }
        return out.toString();
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!replace(new String[] {"cat", "bat", "rat"}, "the cattle was rattled by the battery").equals("the cat was rat by the bat")) throw new AssertionError("ex1");
        if (!replace(new String[] {"car", "cart"}, "carbon carts").equals("car car")) throw new AssertionError("ex2");
        // No roots leaves the sentence unchanged, and a word shorter than every root stays.
        if (!replace(new String[0], "a bc").equals("a bc") || !replace(new String[] {"abc"}, "ab").equals("ab")) throw new AssertionError("edges");
        // Random inputs must match a scan of all roots.
        Random rnd = new Random(1863);
        for (int t = 0; t < 400; t++) {
            String[] roots = new String[rnd.nextInt(5)];
            for (int i = 0; i < roots.length; i++) roots[i] = word(rnd, 1);
            StringBuilder sb = new StringBuilder();
            StringBuilder exp = new StringBuilder();
            for (int k = 1 + rnd.nextInt(4); k > 0; k--) {
                String w = word(rnd, 1);
                String best = w;
                for (String r : roots) if (w.startsWith(r) && (best.equals(w) || r.length() < best.length()) && r.length() <= w.length()) best = r;
                if (sb.length() > 0) { sb.append(' '); exp.append(' '); }
                sb.append(w);
                exp.append(best);
            }
            if (!replace(roots, sb.toString()).equals(exp.toString())) throw new AssertionError("random " + t);
        }
    }

    static String word(Random r, int min) {
        StringBuilder sb = new StringBuilder();
        for (int j = min + r.nextInt(4); j > 0; j--) sb.append((char) ('a' + r.nextInt(2)));
        return sb.toString();
    }
}
```

#### Solution: [Recognize] Longest Word in Dictionary (LeetCode 720)
<!-- id: tr-combo-longest-built-word -->

**Approach.**
The method stores all words in a tree with a terminal flag. It then runs a depth-first search from the root that enters a child only when that child carries a flag. A path made of flagged nodes spells a word whose every nonempty prefix is also a stored word. The search visits the children in alphabetical order and keeps the best word. A word replaces the best only when it is strictly longer. Equal lengths keep the earlier word, and the earlier word in this order is the lexicographically smaller one. The root has no letter, so an empty input returns the empty string.

Every visited node has a flagged path from the root, and the search visits those nodes in alphabetical preorder.

**Complexity.**
- **Time** is O(L) for the total length `L` of the words, because each node is built once and visited at most once.
- **Space** is O(26 * N) for the nodes plus O(depth) for the recursion and the path.

```java run
import java.util.*;

public final class ComboLongestBuiltWord {
    private static final class Node { final Node[] child = new Node[26]; boolean terminal; }

    private static String best;

    /**
     * Returns the longest word whose every prefix is stored, smallest lexicographically on ties.
     * Time: O(L). Space: O(26 * N + depth).
     * Invariant: the search enters only flagged nodes, so every visited path is a chain of stored words.
     */
    static String longest(String[] words) {
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
        best = "";
        dfs(root, new StringBuilder());
        return best;
    }

    private static void dfs(Node node, StringBuilder path) {
        for (int s = 0; s < 26; s++) {                             // alphabetical order makes earlier words smaller
            Node next = node.child[s];
            if (next == null || !next.terminal) continue;          // a missing prefix word blocks this branch
            path.append((char) ('a' + s));
            if (path.length() > best.length()) best = path.toString();   // strictly longer only, so ties keep the earlier word
            dfs(next, path);
            path.setLength(path.length() - 1);                     // undo the traversal state only
        }
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!longest(new String[] {"w", "wo", "wor", "worl", "world", "wom"}).equals("world")) throw new AssertionError("ex1");
        if (!longest(new String[] {"a", "banana", "app", "appl", "ap", "apply", "apple"}).equals("apple")) throw new AssertionError("ex2");
        // An empty list, and words with no one-letter start, return the empty string.
        if (!longest(new String[0]).isEmpty() || !longest(new String[] {"ab", "abc"}).isEmpty()) throw new AssertionError("empty");
        // Random inputs must match a set-based check of every prefix.
        Random rnd = new Random(1864);
        for (int t = 0; t < 400; t++) {
            String[] w = new String[rnd.nextInt(8)];
            Set<String> set = new HashSet<>();
            for (int i = 0; i < w.length; i++) { w[i] = word(rnd); set.add(w[i]); }
            String expect = "";
            for (String x : set) {
                boolean ok = true;
                for (int k = 1; k <= x.length(); k++) if (!set.contains(x.substring(0, k))) ok = false;
                if (ok && (x.length() > expect.length() || (x.length() == expect.length() && x.compareTo(expect) < 0))) expect = x;
            }
            if (!longest(w).equals(expect)) throw new AssertionError("random " + t);
        }
    }

    static String word(Random r) {
        StringBuilder sb = new StringBuilder();
        for (int j = 1 + r.nextInt(4); j > 0; j--) sb.append((char) ('a' + r.nextInt(2)));
        return sb.toString();
    }
}
```
