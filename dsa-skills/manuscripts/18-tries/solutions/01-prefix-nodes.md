<!-- solutions-for: 01-prefix-nodes -->
### Solutions For Storing Shared Prefixes

#### Solution: [Build] Store Shared Prefixes (Author exercise)
<!-- id: tr-store-shared-prefixes -->

**Approach.**
The method inserts each word letter by letter and counts every child that it has to create. A letter whose edge already exists reuses the node, so a shared prefix adds nothing the second time. The count after all inserts equals the number of distinct nonempty prefixes. An equal word walks existing edges only and adds zero nodes.

Before each insert the tree has one node per distinct nonempty prefix of the earlier words.

**Complexity.**
- **Time** is O(L), where `L` is the total length of all words, because each letter costs one map lookup and at most one creation.
- **Space** is O(L), because the tree has at most one node per letter.

```java run
import java.util.*;

public final class StoreSharedPrefixes {
    /**
     * Returns the number of nodes below the root after inserting all words.
     * Time: O(L) for L total letters. Space: O(L).
     * Invariant: before each insert the tree has one node per distinct nonempty prefix inserted so far.
     */
    static int countNodes(String[] words) {
        final class Node { final Map<Character, Node> next = new HashMap<>(); }
        Node root = new Node();
        int created = 0;
        for (String w : words) {                                   // one insert per word
            Node cur = root;
            for (int i = 0; i < w.length(); i++) {                 // one step per letter
                Node child = cur.next.get(w.charAt(i));            // look up the edge
                if (child == null) {                               // a missing edge costs one new node
                    child = new Node();
                    cur.next.put(w.charAt(i), child);
                    created++;
                }
                cur = child;                                       // move down one level
            }
        }
        return created;                                            // one node per distinct nonempty prefix
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (countNodes(new String[] {"car", "cat"}) != 4) throw new AssertionError("ex1");
        if (countNodes(new String[] {"a", "a", "ab"}) != 2) throw new AssertionError("ex2");
        // No words, or only the empty word, create no nodes.
        if (countNodes(new String[0]) != 0 || countNodes(new String[] {"", ""}) != 0) throw new AssertionError("empty");
        // Random words must match a set of all distinct nonempty prefixes.
        Random rnd = new Random(1801);
        for (int t = 0; t < 400; t++) {
            String[] w = new String[rnd.nextInt(8)];
            Set<String> prefixes = new HashSet<>();
            for (int i = 0; i < w.length; i++) {
                StringBuilder sb = new StringBuilder();
                for (int j = rnd.nextInt(5); j > 0; j--) sb.append((char) ('a' + rnd.nextInt(3)));
                w[i] = sb.toString();
                for (int k = 1; k <= w[i].length(); k++) prefixes.add(w[i].substring(0, k));
            }
            if (countNodes(w) != prefixes.size()) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Vary] Prefix Count (Author exercise)
<!-- id: tr-prefix-count -->

**Approach.**
Each node stores a pass count. An insert increments the count of every node on its path, so the count of a node equals the number of inserted words that start with the prefix of that node. A query walks the letters of the prefix and returns the count of the last node, or 0 when an edge is missing. The empty prefix stays at the root, and the root count equals the number of inserted words, so the method adds one to a separate total for every insert, including the empty word.

The pass count of a node equals the number of inserted entries whose first letters spell the prefix of the node.

**Complexity.**
- **Time** is O(L + Q), where `L` is the total length of `words` and `Q` the total length of `prefixes`.
- **Space** is O(L), because the tree has at most one node per inserted letter.

```java run
import java.util.*;

public final class PrefixCount {
    private static final class Node {
        final Map<Character, Node> next = new HashMap<>();
        int pass;
    }

    /**
     * Returns, for each prefix, how many entries of words start with it.
     * Time: O(L + Q). Space: O(L).
     * Invariant: pass of a node equals the entries whose first letters spell the node's prefix.
     */
    static int[] countPrefixes(String[] words, String[] prefixes) {
        Node root = new Node();
        for (String w : words) {
            root.pass++;                                           // the empty prefix matches every entry
            Node cur = root;
            for (int i = 0; i < w.length(); i++) {                 // one step per letter
                cur = cur.next.computeIfAbsent(w.charAt(i), c -> new Node());
                cur.pass++;                                        // this entry passes through the node
            }
        }
        int[] out = new int[prefixes.length];
        for (int j = 0; j < prefixes.length; j++) {                // one walk per query
            Node cur = root;
            for (int i = 0; i < prefixes[j].length() && cur != null; i++) {
                cur = cur.next.get(prefixes[j].charAt(i));         // null when the edge is missing
            }
            out[j] = cur == null ? 0 : cur.pass;                   // a missing path means no entry matches
        }
        return out;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!Arrays.equals(countPrefixes(new String[] {"car", "cat", "cart", "dog"}, new String[] {"ca", "car", "d", "x"}), new int[] {3, 2, 1, 0}))
            throw new AssertionError("ex1");
        if (!Arrays.equals(countPrefixes(new String[] {"ab", "ab"}, new String[] {"", "ab", "abc"}), new int[] {2, 2, 0}))
            throw new AssertionError("ex2");
        // Random inputs must match a direct startsWith count.
        Random rnd = new Random(1802);
        for (int t = 0; t < 400; t++) {
            String[] w = new String[rnd.nextInt(8)];
            String[] q = new String[rnd.nextInt(8)];
            for (int i = 0; i < w.length; i++) w[i] = rnd(rnd);
            for (int i = 0; i < q.length; i++) q[i] = rnd(rnd);
            int[] expect = new int[q.length];
            for (int j = 0; j < q.length; j++) for (String x : w) if (x.startsWith(q[j])) expect[j]++;
            if (!Arrays.equals(countPrefixes(w, q), expect)) throw new AssertionError("random " + t);
        }
    }

    static String rnd(Random r) {
        StringBuilder sb = new StringBuilder();
        for (int j = r.nextInt(4); j > 0; j--) sb.append((char) ('a' + r.nextInt(2)));
        return sb.toString();
    }
}
```

#### Solution: [Boundary] Empty Word And Prefix-Only Node (Author exercise)
<!-- id: tr-empty-word-prefix-only -->

**Approach.**
The tree stores a terminal flag on every node, and the root has a flag as well. Inserting the empty word sets the flag of the root and creates no node. A query walks its letters. A missing edge gives status 0. A node with a true flag gives status 2. A node with a false flag gives status 1 only when the node is a real prefix, which means it is not the root or the tree holds at least one word. The empty query on a tree without words ends on the root with a false flag and an empty tree, so the method returns 0.

The invariant is that a node with a false flag still has a stored word below it, except for the root of a tree with no words.

**Complexity.**
- **Time** is O(L + Q) for the total lengths of the entries and the queries.
- **Space** is O(L) for the nodes.

```java run
import java.util.*;

public final class EmptyWordPrefixOnly {
    private static final class Node {
        final Map<Character, Node> next = new HashMap<>();
        boolean terminal;
    }

    /**
     * Returns 2 for a stored word, 1 for a prefix of a stored word, 0 otherwise.
     * Time: O(L + Q). Space: O(L).
     * Invariant: every non-root node with a false flag has a flagged node in its subtree.
     */
    static int[] status(String[] words, String[] queries) {
        Node root = new Node();
        for (String w : words) {
            Node cur = root;
            for (int i = 0; i < w.length(); i++) cur = cur.next.computeIfAbsent(w.charAt(i), c -> new Node());
            cur.terminal = true;                                   // the empty word flags the root itself
        }
        boolean anyWord = words.length > 0;                        // a root with no words is not a prefix
        int[] out = new int[queries.length];
        for (int j = 0; j < queries.length; j++) {
            Node cur = root;
            for (int i = 0; i < queries[j].length() && cur != null; i++) cur = cur.next.get(queries[j].charAt(i));
            if (cur == null) out[j] = 0;                           // the path breaks
            else if (cur.terminal) out[j] = 2;                     // a stored word ends here
            else out[j] = anyWord ? 1 : 0;                         // a path node without a flag is a prefix
        }
        return out;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!Arrays.equals(status(new String[] {"app", "apple"}, new String[] {"ap", "app", "apple", "applez"}), new int[] {1, 2, 2, 0}))
            throw new AssertionError("ex1");
        if (!Arrays.equals(status(new String[] {"x"}, new String[] {"", "x", "y"}), new int[] {1, 2, 0}))
            throw new AssertionError("ex2");
        // The empty word makes the empty query a word, and an empty tree gives 0.
        if (status(new String[] {""}, new String[] {""})[0] != 2) throw new AssertionError("empty word");
        if (status(new String[0], new String[] {"", "a"})[0] != 0) throw new AssertionError("empty tree");
        // Random inputs must match a direct comparison.
        Random rnd = new Random(1803);
        for (int t = 0; t < 400; t++) {
            String[] w = new String[rnd.nextInt(6)];
            String[] q = new String[rnd.nextInt(8)];
            for (int i = 0; i < w.length; i++) w[i] = rnd(rnd);
            for (int i = 0; i < q.length; i++) q[i] = rnd(rnd);
            int[] expect = new int[q.length];
            for (int j = 0; j < q.length; j++) {
                for (String x : w) {
                    if (x.equals(q[j])) expect[j] = 2;
                    else if (x.startsWith(q[j]) && expect[j] == 0) expect[j] = 1;
                }
            }
            if (!Arrays.equals(status(w, q), expect)) throw new AssertionError("random " + t);
        }
    }

    static String rnd(Random r) {
        StringBuilder sb = new StringBuilder();
        for (int j = r.nextInt(4); j > 0; j--) sb.append((char) ('a' + r.nextInt(2)));
        return sb.toString();
    }
}
```

#### Solution: [Recognize] Implement Trie (LeetCode 208)
<!-- id: tr-implement-trie-map -->

**Approach.**
The class keeps a root node. Each node has a `HashMap<Character, Node>` and a terminal flag. The method `insert` creates missing children along the word and flags the last node. A shared helper walks a string and returns the node it reaches, or null. The method `search` returns true when the node exists and its flag is true. The method `startsWith` returns true when the node exists. A map allows any `char`, so the class makes no assumption about the alphabet.

A node exists exactly when it is the prefix of some inserted word.

**Complexity.**
- **Time** is O(m) per call for a string of `m` characters, because each call visits one node per character.
- **Space** is O(L) for the stored letters of all inserted words.

```java run
import java.util.*;

public final class ImplementTrieMap {
    private static final class Node {
        final Map<Character, Node> next = new HashMap<>();
        boolean terminal;
    }

    static final class Trie {
        private final Node root = new Node();

        /** Inserts a word. Time: O(m). Space: O(m). Invariant: a node exists iff it is a prefix of an inserted word. */
        void insert(String word) {
            Node cur = root;
            for (int i = 0; i < word.length(); i++) {              // one step per character
                cur = cur.next.computeIfAbsent(word.charAt(i), c -> new Node());
            }
            cur.terminal = true;                                   // mark the word end
        }

        private Node walk(String s) {
            Node cur = root;
            for (int i = 0; i < s.length() && cur != null; i++) cur = cur.next.get(s.charAt(i));
            return cur;                                            // null when a prefix is absent
        }

        /** Returns true when the exact word was inserted. Time: O(m). Space: O(1). */
        boolean search(String word) { Node n = walk(word); return n != null && n.terminal; }

        /** Returns true when an inserted word starts with prefix. Time: O(m). Space: O(1). */
        boolean startsWith(String prefix) { return walk(prefix) != null; }
    }

    public static void main(String[] args) {
        // Example 1: a prefix is not a word, and the word itself is found.
        Trie t = new Trie();
        t.insert("Go");
        if (t.search("G") || !t.startsWith("G") || !t.search("Go")) throw new AssertionError("ex1");
        // Example 2: an empty tree answers false twice.
        Trie e = new Trie();
        if (e.search("a") || e.startsWith("a")) throw new AssertionError("ex2");
        // Characters other than lowercase letters work because the children live in a map.
        t.insert("a9_");
        if (!t.search("a9_") || !t.startsWith("a9")) throw new AssertionError("any char");
        // Random operations must match a set and a startsWith scan.
        Random rnd = new Random(1804);
        for (int r = 0; r < 200; r++) {
            Trie x = new Trie();
            Set<String> set = new HashSet<>();
            for (int op = 0; op < 30; op++) {
                String s = "a" + rnd(rnd);                  // the contract allows only nonempty strings
                if (rnd.nextBoolean()) { x.insert(s); set.add(s); }
                boolean any = false;
                for (String w : set) if (w.startsWith(s)) any = true;
                if (x.search(s) != set.contains(s) || x.startsWith(s) != any) throw new AssertionError("random " + r);
            }
        }
    }

    static String rnd(Random r) {
        StringBuilder sb = new StringBuilder();
        for (int j = r.nextInt(4); j > 0; j--) sb.append((char) ('a' + r.nextInt(2)));
        return sb.toString();
    }
}
```
