<!-- solutions-for: 02-insert-and-search -->
### Solutions For Inserting And Looking Up Words

#### Solution: [Build] Insert Lowercase Words (Author exercise)
<!-- id: tr-insert-lowercase-words -->

**Approach.**
The method keeps one tree with 26 child slots in each node. For each word it walks the characters with an index. A non-null slot moves the walk down, and a null slot creates a node and counts it. The empty word walks nothing and creates nothing. An equal word finds every slot filled, so its count is 0. The walk never builds a substring.

Before the insert of word `j`, the tree holds exactly the nodes of the prefixes of `words[0..j)`.

**Complexity.**
- **Time** is O(L), where `L` is the total length of the words, because each character costs one slot read.
- **Space** is O(26 * N) for the `N` created nodes, which is O(L) with a constant of 26.

```java run
import java.util.*;

public final class InsertLowercaseWords {
    private static final class Node { final Node[] child = new Node[26]; }

    /**
     * Returns the number of nodes created by each insert.
     * Time: O(L). Space: O(26 * N).
     * Invariant: before insert j the tree holds the nodes of every prefix of words[0..j).
     */
    static int[] created(String[] words) {
        Node root = new Node();
        int[] out = new int[words.length];
        for (int j = 0; j < words.length; j++) {
            Node cur = root;
            for (int i = 0; i < words[j].length(); i++) {          // one step per character
                int s = words[j].charAt(i) - 'a';                  // offset in 0..25 for lowercase input
                if (cur.child[s] == null) {                        // an empty slot costs one node
                    cur.child[s] = new Node();
                    out[j]++;
                }
                cur = cur.child[s];                                // descend one level
            }
        }
        return out;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!Arrays.equals(created(new String[] {"car", "cat", "car", "ca"}), new int[] {3, 1, 0, 0})) throw new AssertionError("ex1");
        if (!Arrays.equals(created(new String[] {"b", "", "ba"}), new int[] {1, 0, 1})) throw new AssertionError("ex2");
        // Random inputs must match a set of seen prefixes.
        Random rnd = new Random(1811);
        for (int t = 0; t < 400; t++) {
            String[] w = new String[rnd.nextInt(8)];
            for (int i = 0; i < w.length; i++) w[i] = word(rnd);
            Set<String> seen = new HashSet<>();
            int[] expect = new int[w.length];
            for (int j = 0; j < w.length; j++)
                for (int k = 1; k <= w[j].length(); k++) if (seen.add(w[j].substring(0, k))) expect[j]++;
            if (!Arrays.equals(created(w), expect)) throw new AssertionError("random " + t);
        }
    }

    static String word(Random r) {
        StringBuilder sb = new StringBuilder();
        for (int j = r.nextInt(5); j > 0; j--) sb.append((char) ('a' + r.nextInt(3)));
        return sb.toString();
    }
}
```

#### Solution: [Vary] Search Versus StartsWith (Author exercise)
<!-- id: tr-search-versus-starts-with -->

**Approach.**
The method inserts every word into one tree and flags the last node. For each query it walks the characters and stops with false at the first null slot. After a full walk, an exact query returns the flag of the node, and a prefix query returns true. The two modes differ only in the last line, so one walk serves both. The empty prefix needs at least one stored entry.

A walk that survives `i` characters sits on the node of a real prefix of some entry.

**Complexity.**
- **Time** is O(L + Q) for the total lengths of the entries and the queries.
- **Space** is O(26 * N) for the nodes.

```java run
import java.util.*;

public final class SearchVersusStartsWith {
    private static final class Node { final Node[] child = new Node[26]; boolean terminal; }

    /**
     * Answers each query in its own mode.
     * Time: O(L + Q). Space: O(26 * N).
     * Invariant: a walk that survives i characters sits on a node whose prefix starts some entry.
     */
    static boolean[] answer(String[] words, String[] queries, boolean[] exact) {
        Node root = new Node();
        for (String w : words) {
            Node cur = root;
            for (int i = 0; i < w.length(); i++) {
                int s = w.charAt(i) - 'a';
                if (cur.child[s] == null) cur.child[s] = new Node();
                cur = cur.child[s];
            }
            cur.terminal = true;                                   // the flag matters only for exact queries
        }
        boolean[] out = new boolean[queries.length];
        for (int j = 0; j < queries.length; j++) {
            Node cur = root;
            for (int i = 0; i < queries[j].length() && cur != null; i++) cur = cur.child[queries[j].charAt(i) - 'a'];
            // A missing node fails both modes. The exact mode reads the flag, and the prefix mode needs a stored entry.
            out[j] = cur != null && (exact[j] ? cur.terminal : (cur != root || words.length > 0));
        }
        return out;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!Arrays.equals(answer(new String[] {"app", "apple"}, new String[] {"app", "ap", "apple", "apples"}, new boolean[] {true, true, false, false}),
                new boolean[] {true, false, true, false})) throw new AssertionError("ex1");
        if (!Arrays.equals(answer(new String[] {"a"}, new String[] {"", "a"}, new boolean[] {false, true}), new boolean[] {true, true}))
            throw new AssertionError("ex2");
        // An empty word list makes the empty prefix query false and the exact query false.
        if (answer(new String[0], new String[] {""}, new boolean[] {false})[0]) throw new AssertionError("empty list");
        // Random inputs must match direct comparisons.
        Random rnd = new Random(1812);
        for (int t = 0; t < 400; t++) {
            String[] w = new String[rnd.nextInt(6)];
            String[] q = new String[rnd.nextInt(8)];
            boolean[] ex = new boolean[q.length];
            for (int i = 0; i < w.length; i++) w[i] = word(rnd);
            for (int i = 0; i < q.length; i++) { q[i] = word(rnd); ex[i] = rnd.nextBoolean(); }
            boolean[] expect = new boolean[q.length];
            for (int j = 0; j < q.length; j++)
                for (String x : w) if (ex[j] ? x.equals(q[j]) : x.startsWith(q[j])) expect[j] = true;
            if (!Arrays.equals(answer(w, q, ex), expect)) throw new AssertionError("random " + t);
        }
    }

    static String word(Random r) {
        StringBuilder sb = new StringBuilder();
        for (int j = r.nextInt(5); j > 0; j--) sb.append((char) ('a' + r.nextInt(3)));
        return sb.toString();
    }
}
```

#### Solution: [Boundary] Word Is Prefix Of Another (Author exercise)
<!-- id: tr-word-is-prefix-of-another -->

**Approach.**
The method stores all words with a flag on the last node. It then walks the query character by character and counts every flagged node it passes, starting with the root, because the root flag marks the empty word. When a slot is null, the walk ends, and no deeper entry can be a prefix. The count of flags along the path equals the number of distinct entries that are prefixes of the query. A repeated entry sets the same flag again, so it counts once.

At step `i` the count equals the number of distinct entries of length at most `i` that are prefixes of the query.

**Complexity.**
- **Time** is O(L + m), where `m` is the length of the query.
- **Space** is O(26 * N) for the nodes.

```java run
import java.util.*;

public final class WordIsPrefixOfAnother {
    private static final class Node { final Node[] child = new Node[26]; boolean terminal; }

    /**
     * Counts distinct entries that are prefixes of the query.
     * Time: O(L + m). Space: O(26 * N).
     * Invariant: after step i the count holds the distinct entries of length at most i that prefix the query.
     */
    static int prefixesOf(String[] words, String query) {
        Node root = new Node();
        for (String w : words) {
            Node cur = root;
            for (int i = 0; i < w.length(); i++) {
                int s = w.charAt(i) - 'a';
                if (cur.child[s] == null) cur.child[s] = new Node();
                cur = cur.child[s];
            }
            cur.terminal = true;                                   // equal entries set the same flag
        }
        int count = 0;
        Node cur = root;
        for (int i = 0; cur != null; i++) {
            if (cur.terminal) count++;                             // an entry ends on this path node
            if (i == query.length()) break;                        // the query has no more characters
            cur = cur.child[query.charAt(i) - 'a'];                // null ends the walk
        }
        return count;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (prefixesOf(new String[] {"a", "app", "apple", "app"}, "applesauce") != 3) throw new AssertionError("ex1");
        if (prefixesOf(new String[] {"", "b"}, "a") != 1) throw new AssertionError("ex2");
        // An empty query matches only the empty entry.
        if (prefixesOf(new String[] {"", "a"}, "") != 1 || prefixesOf(new String[] {"a"}, "") != 0) throw new AssertionError("empty query");
        // Random inputs must match a set of entries compared with startsWith.
        Random rnd = new Random(1813);
        for (int t = 0; t < 400; t++) {
            String[] w = new String[rnd.nextInt(7)];
            for (int i = 0; i < w.length; i++) w[i] = word(rnd);
            String q = word(rnd) + word(rnd);
            int expect = 0;
            for (String x : new HashSet<>(Arrays.asList(w))) if (q.startsWith(x)) expect++;
            if (prefixesOf(w, q) != expect) throw new AssertionError("random " + t);
        }
    }

    static String word(Random r) {
        StringBuilder sb = new StringBuilder();
        for (int j = r.nextInt(5); j > 0; j--) sb.append((char) ('a' + r.nextInt(3)));
        return sb.toString();
    }
}
```

#### Solution: [Recognize] Implement Trie (LeetCode 208)
<!-- id: tr-implement-trie-array -->

**Approach.**
The class stores 26 child slots in each node. The method `insert` first scans the whole word and throws when any character lies outside `'a'` to `'z'`. This check runs before the first node is created, so a rejected word leaves no partial path behind. The walk then creates missing nodes and counts them. The method returns true when the flag was false before the insert, which means the word is new. The methods `search` and `startsWith` return false at the first invalid character, and otherwise they walk the slots exactly as in the previous exercises.

The invariant is that every node in the tree is the prefix of some inserted word, because an insert either completes or never starts.

**Complexity.**
- **Time** is O(m) per call, because one pass checks the characters and one pass walks them.
- **Space** is O(26 * N) for the nodes, which is O(L) with a constant of 26.

```java run
import java.util.*;

public final class ImplementTrieArray {
    private static final class Node { final Node[] child = new Node[26]; boolean terminal; }

    static final class Trie {
        private final Node root = new Node();

        private static boolean valid(String s) {
            for (int i = 0; i < s.length(); i++) if (s.charAt(i) < 'a' || s.charAt(i) > 'z') return false;
            return true;
        }

        /** Inserts a word; returns true when the word is new. Time: O(m). Space: O(m). */
        boolean insert(String word) {
            if (!valid(word)) throw new IllegalArgumentException("outside a-z");   // check before any node exists
            Node cur = root;
            for (int i = 0; i < word.length(); i++) {
                int s = word.charAt(i) - 'a';
                if (cur.child[s] == null) cur.child[s] = new Node();
                cur = cur.child[s];
            }
            boolean fresh = !cur.terminal;                         // false when the word was stored before
            cur.terminal = true;
            return fresh;
        }

        private Node walk(String s) {
            if (!valid(s)) return null;                            // an invalid character never matches
            Node cur = root;
            for (int i = 0; i < s.length() && cur != null; i++) cur = cur.child[s.charAt(i) - 'a'];
            return cur;
        }

        /** Returns true when the exact word is stored. Time: O(m). Space: O(1). */
        boolean search(String word) { Node n = walk(word); return n != null && n.terminal; }

        /** Returns true when a stored word starts with prefix. Time: O(m). Space: O(1). */
        boolean startsWith(String prefix) { return walk(prefix) != null; }

        int nodes() { return count(root) - 1; }

        private int count(Node n) {
            int c = 1;
            for (Node ch : n.child) if (ch != null) c += count(ch);
            return c;
        }
    }

    public static void main(String[] args) {
        // Example 1: the second insert of the same word returns false.
        Trie t = new Trie();
        if (!t.insert("dog") || t.insert("dog") || t.search("do") || !t.startsWith("do")) throw new AssertionError("ex1");
        // Example 2: an invalid word throws, leaves no nodes and fails both queries.
        Trie e = new Trie();
        boolean threw = false;
        try { e.insert("Dog"); } catch (IllegalArgumentException x) { threw = true; }
        if (!threw || e.nodes() != 0 || e.search("Dog") || e.startsWith("Dog")) throw new AssertionError("ex2");
        // A word whose bad character comes last must leave no partial path.
        try { e.insert("dogs!"); } catch (IllegalArgumentException x) { threw = true; }
        if (e.nodes() != 0) throw new AssertionError("partial insert");
        // Random operations must match a set and a startsWith scan.
        Random rnd = new Random(1814);
        for (int r = 0; r < 200; r++) {
            Trie x = new Trie();
            Set<String> set = new HashSet<>();
            for (int op = 0; op < 30; op++) {
                String s = "a" + word(rnd);
                if (rnd.nextBoolean()) {
                    boolean fresh = x.insert(s);                  // true exactly when the word was absent
                    if (fresh == set.contains(s)) throw new AssertionError("fresh " + r);
                    set.add(s);
                }
                boolean any = false;
                for (String w : set) if (w.startsWith(s)) any = true;
                if (x.search(s) != set.contains(s) || x.startsWith(s) != any) throw new AssertionError("query " + r);
            }
        }
    }

    static String word(Random r) {
        StringBuilder sb = new StringBuilder();
        for (int j = r.nextInt(5); j > 0; j--) sb.append((char) ('a' + r.nextInt(3)));
        return sb.toString();
    }
}
```
