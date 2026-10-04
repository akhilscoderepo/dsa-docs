<!-- solutions-for: 03-wildcard-branching -->
### Wildcard Branching

#### Solution: [Build] One Final Wildcard (Author exercise)
<!-- id: tn-final-wildcard -->

**Approach.** Insert the words into a trie with a flag. For a query, walk its letters except the last one along single edges. If the walk survives, the last character decides: a letter needs that one child to exist and be flagged, and a dot needs at least one flagged child. A query of one character walks nothing and is decided at the root. The oracle compares the query with every word of equal length square by square. The assertions compare the two on random inputs, and show that a dot cannot be used as an array index because `'.' - 'a'` is negative.

**Complexity.** O(L + 26) per query, since only the last step looks at all children.

```java run
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Random;
import java.util.Set;

public final class FinalWildcard {
    static final class Node {
        final Node[] next = new Node[26];
        boolean word;
    }

    static List<Boolean> solve(List<String> words, List<String> queries) {
        Node root = new Node();
        for (String w : words) {
            Node cur = root;
            for (char c : w.toCharArray()) {
                if (cur.next[c - 'a'] == null) cur.next[c - 'a'] = new Node();
                cur = cur.next[c - 'a'];
            }
            cur.word = true;
        }
        List<Boolean> out = new ArrayList<>();
        for (String q : queries) {
            Node cur = root;
            int last = q.length() - 1;
            for (int i = 0; i < last && cur != null; i++) cur = cur.next[q.charAt(i) - 'a'];
            boolean ok = false;
            if (cur != null) {
                char c = q.charAt(last);
                if (c == '.') {
                    for (Node child : cur.next) if (child != null && child.word) ok = true;
                } else {
                    Node child = cur.next[c - 'a'];
                    ok = child != null && child.word;
                }
            }
            out.add(ok);
        }
        return out;
    }

    static List<Boolean> oracle(List<String> words, List<String> queries) {
        List<Boolean> out = new ArrayList<>();
        for (String q : queries) {
            boolean ok = false;
            for (String w : words) {
                if (w.length() != q.length()) continue;
                boolean fits = true;
                for (int i = 0; i < q.length(); i++) if (q.charAt(i) != '.' && q.charAt(i) != w.charAt(i)) fits = false;
                if (fits) ok = true;
            }
            out.add(ok);
        }
        return out;
    }

    static String letters(Random rnd, int len) {
        StringBuilder sb = new StringBuilder();
        for (int j = 0; j < len; j++) sb.append((char) ('a' + rnd.nextInt(3)));
        return sb.toString();
    }

    public static void main(String[] args) {
        if (!solve(List.of("cat", "car", "cow"), List.of("ca.", "co.", "cx.", "ca")).equals(List.of(true, true, false, false))) throw new AssertionError("example 1");
        if (!solve(List.of("a"), List.of(".", "a", "b", "a.")).equals(List.of(true, true, false, false))) throw new AssertionError("example 2");
        if ('.' - 'a' != -51) throw new AssertionError("a dot maps to slot -51");
        Random rnd = new Random(18301);
        for (int t = 0; t < 5000; t++) {
            Set<String> pick = new HashSet<>();
            int n = rnd.nextInt(7);
            for (int k = 0; k < n; k++) pick.add(letters(rnd, 1 + rnd.nextInt(4)));
            List<String> words = new ArrayList<>(pick), queries = new ArrayList<>();
            for (int k = 0; k < 6; k++) {
                String q = letters(rnd, 1 + rnd.nextInt(4));
                if (rnd.nextBoolean()) q = q.substring(0, q.length() - 1) + ".";
                queries.add(q);
            }
            if (!solve(words, queries).equals(oracle(words, queries))) throw new AssertionError("differs on " + words + queries);
        }
    }
}
```

#### Solution: [Vary] Multiple Wildcards (Author exercise)
<!-- id: tn-multiple-wildcards -->

**Approach.** A recursive call takes a node, the pattern position and a builder holding the path so far. At a letter it follows the single edge, and at a dot it tries each existing child in alphabetical order, which is the order of the slots. A call that reaches the end of the pattern on a flagged node returns the path as a string, and any non-null result is passed straight up, so the first success stops the loop. Because slots are tried in increasing order and every word has the same length, the first success is the smallest matching word. The builder is extended before a child call and trimmed after it, so only the path travels. The oracle sorts the words and returns the first one that fits. The assertions compare the two on random inputs.

**Complexity.** O(total letters stored) per query in the worst case, and O(L) when the pattern has no dots.

```java run
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashSet;
import java.util.List;
import java.util.Random;
import java.util.Set;

public final class MultipleWildcards {
    static final class Node {
        final Node[] next = new Node[26];
        boolean word;
    }

    static String dfs(Node node, String pattern, int pos, StringBuilder path) {
        if (pos == pattern.length()) return node.word ? path.toString() : null;
        char c = pattern.charAt(pos);
        for (int slot = 0; slot < 26; slot++) {
            if (node.next[slot] == null) continue;
            if (c != '.' && c - 'a' != slot) continue;
            path.append((char) ('a' + slot));
            String got = dfs(node.next[slot], pattern, pos + 1, path);
            path.setLength(path.length() - 1);
            if (got != null) return got;
        }
        return null;
    }

    static List<String> solve(List<String> words, List<String> queries) {
        Node root = new Node();
        for (String w : words) {
            Node cur = root;
            for (char c : w.toCharArray()) {
                if (cur.next[c - 'a'] == null) cur.next[c - 'a'] = new Node();
                cur = cur.next[c - 'a'];
            }
            cur.word = true;
        }
        List<String> out = new ArrayList<>();
        for (String q : queries) {
            String got = dfs(root, q, 0, new StringBuilder());
            out.add(got == null ? "" : got);
        }
        return out;
    }

    static boolean fits(String q, String w) {
        if (q.length() != w.length()) return false;
        for (int i = 0; i < q.length(); i++) if (q.charAt(i) != '.' && q.charAt(i) != w.charAt(i)) return false;
        return true;
    }

    static List<String> oracle(List<String> words, List<String> queries) {
        List<String> sorted = new ArrayList<>(words);
        Collections.sort(sorted);
        List<String> out = new ArrayList<>();
        for (String q : queries) {
            String best = "";
            for (String w : sorted) if (fits(q, w)) { best = w; break; }
            out.add(best);
        }
        return out;
    }

    static String text(Random rnd, int len, boolean dots) {
        StringBuilder sb = new StringBuilder();
        for (int j = 0; j < len; j++) sb.append(dots && rnd.nextInt(3) == 0 ? '.' : (char) ('a' + rnd.nextInt(3)));
        return sb.toString();
    }

    public static void main(String[] args) {
        List<String> a = solve(List.of("bad", "bed", "bid", "cod"), List.of("b.d", ".o.", "...", "b..."));
        if (!a.equals(List.of("bad", "cod", "bad", ""))) throw new AssertionError("example 1 " + a);
        if (!solve(List.of("zz", "za", "az"), List.of(".z", "z.", "..")).equals(List.of("az", "za", "az"))) throw new AssertionError("example 2");
        Random rnd = new Random(18302);
        for (int t = 0; t < 5000; t++) {
            Set<String> pick = new HashSet<>();
            int n = rnd.nextInt(8);
            for (int k = 0; k < n; k++) pick.add(text(rnd, 1 + rnd.nextInt(4), false));
            List<String> words = new ArrayList<>(pick), queries = new ArrayList<>();
            for (int k = 0; k < 6; k++) queries.add(text(rnd, 1 + rnd.nextInt(4), true));
            if (!solve(words, queries).equals(oracle(words, queries))) throw new AssertionError("differs on " + words + queries);
        }
    }
}
```

#### Solution: [Boundary] Wildcard At Root And Missing Length (Author exercise)
<!-- id: tn-wildcard-root-length -->

**Approach.** The call returns a count instead of a boolean. At the end of the pattern it returns 1 for a flagged node and 0 otherwise, which is what rejects a longer word that only begins like the pattern, and a pattern longer than any word simply runs out of edges and returns 0. At a letter it follows one edge, and at a dot it adds the counts of all existing children, with no early stop, since every match must be counted. Since words are distinct, each match is counted once. The oracle tests every word with a length check and a square by square comparison. The assertions compare the two on random inputs that include all-dot patterns and patterns longer than every word.

**Complexity.** O(total letters stored) per pattern in the worst case.

```java run
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Random;
import java.util.Set;

public final class WildcardRootLength {
    static final class Node {
        final Node[] next = new Node[26];
        boolean word;
    }

    static int count(Node node, String pattern, int pos) {
        if (pos == pattern.length()) return node.word ? 1 : 0;
        char c = pattern.charAt(pos);
        int total = 0;
        if (c == '.') {
            for (Node child : node.next) if (child != null) total += count(child, pattern, pos + 1);
        } else if (node.next[c - 'a'] != null) {
            total = count(node.next[c - 'a'], pattern, pos + 1);
        }
        return total;
    }

    static List<Integer> solve(List<String> words, List<String> patterns) {
        Node root = new Node();
        for (String w : words) {
            Node cur = root;
            for (char c : w.toCharArray()) {
                if (cur.next[c - 'a'] == null) cur.next[c - 'a'] = new Node();
                cur = cur.next[c - 'a'];
            }
            cur.word = true;
        }
        List<Integer> out = new ArrayList<>();
        for (String p : patterns) out.add(count(root, p, 0));
        return out;
    }

    static List<Integer> oracle(List<String> words, List<String> patterns) {
        List<Integer> out = new ArrayList<>();
        for (String p : patterns) {
            int c = 0;
            for (String w : words) {
                if (w.length() != p.length()) continue;
                boolean ok = true;
                for (int i = 0; i < p.length(); i++) if (p.charAt(i) != '.' && p.charAt(i) != w.charAt(i)) ok = false;
                if (ok) c++;
            }
            out.add(c);
        }
        return out;
    }

    static String text(Random rnd, int len, boolean dots) {
        StringBuilder sb = new StringBuilder();
        for (int j = 0; j < len; j++) sb.append(dots && rnd.nextInt(2) == 0 ? '.' : (char) ('a' + rnd.nextInt(2)));
        return sb.toString();
    }

    public static void main(String[] args) {
        if (!solve(List.of("ab", "abc", "b"), List.of(".", "..", "...", "....", ".b")).equals(List.of(1, 1, 1, 0, 1))) throw new AssertionError("example 1");
        if (!solve(List.of("aa", "ab", "ba"), List.of("..", "a.", ".a", "a", "b.")).equals(List.of(3, 2, 2, 0, 1))) throw new AssertionError("example 2");
        if (!solve(List.of(), List.of("...")).equals(List.of(0))) throw new AssertionError("empty dictionary");
        Random rnd = new Random(18303);
        for (int t = 0; t < 5000; t++) {
            Set<String> pick = new HashSet<>();
            int n = rnd.nextInt(8);
            for (int k = 0; k < n; k++) pick.add(text(rnd, 1 + rnd.nextInt(4), false));
            List<String> words = new ArrayList<>(pick), patterns = new ArrayList<>();
            for (int k = 0; k < 6; k++) patterns.add(text(rnd, 1 + rnd.nextInt(5), true));
            if (!solve(words, patterns).equals(oracle(words, patterns))) throw new AssertionError("differs on " + words + patterns);
        }
    }
}
```

#### Solution: [Recognize] Design Add and Search Words Data Structure (LeetCode 211)
<!-- id: tn-add-search-words -->

**Approach.** The dictionary class owns a trie and exposes `add` and `search`. Search is the recursive call over a node and a position: at the end it returns the flag, at a letter it follows one edge, and at a dot it returns true as soon as any child succeeds. The script runner splits each command at the first colon. The oracle stores the words in a list and tests a pattern against each word of equal length. The assertions replay both examples and then compare random scripts, which mix adds and searches so the dictionary grows between questions.

**Complexity.** O(L) to add, and at most O(total letters stored) per search, which is O(L) when there is no dot.

```java run
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public final class AddSearchWords {
    static final class WordDictionary {
        private static final class Node {
            final Node[] next = new Node[26];
            boolean word;
        }

        private final Node root = new Node();

        void add(String w) {
            Node cur = root;
            for (int i = 0; i < w.length(); i++) {
                int s = w.charAt(i) - 'a';
                if (cur.next[s] == null) cur.next[s] = new Node();
                cur = cur.next[s];
            }
            cur.word = true;
        }

        boolean search(String p) {
            return go(root, p, 0);
        }

        private boolean go(Node node, String p, int pos) {
            if (pos == p.length()) return node.word;
            char c = p.charAt(pos);
            if (c != '.') return node.next[c - 'a'] != null && go(node.next[c - 'a'], p, pos + 1);
            for (Node child : node.next) if (child != null && go(child, p, pos + 1)) return true;
            return false;
        }
    }

    static List<Boolean> run(List<String> commands) {
        WordDictionary dict = new WordDictionary();
        List<Boolean> out = new ArrayList<>();
        for (String cmd : commands) {
            int colon = cmd.indexOf(':');
            String op = cmd.substring(0, colon), s = cmd.substring(colon + 1);
            if (op.equals("add")) dict.add(s);
            else out.add(dict.search(s));
        }
        return out;
    }

    static List<Boolean> oracle(List<String> commands) {
        List<String> words = new ArrayList<>();
        List<Boolean> out = new ArrayList<>();
        for (String cmd : commands) {
            int colon = cmd.indexOf(':');
            String op = cmd.substring(0, colon), s = cmd.substring(colon + 1);
            if (op.equals("add")) { words.add(s); continue; }
            boolean any = false;
            for (String w : words) {
                if (w.length() != s.length()) continue;
                boolean ok = true;
                for (int i = 0; i < s.length(); i++) if (s.charAt(i) != '.' && s.charAt(i) != w.charAt(i)) ok = false;
                if (ok) any = true;
            }
            out.add(any);
        }
        return out;
    }

    public static void main(String[] args) {
        List<String> one = List.of("add:tin", "add:ton", "search:t.n", "search:tun", "search:..n", "search:t.");
        if (!run(one).equals(List.of(true, false, true, false))) throw new AssertionError("example 1");
        List<String> two = List.of("add:a", "search:.", "search:a.", "search:b");
        if (!run(two).equals(List.of(true, false, false))) throw new AssertionError("example 2");
        Random rnd = new Random(18304);
        for (int t = 0; t < 5000; t++) {
            List<String> cmds = new ArrayList<>();
            int n = rnd.nextInt(14);
            for (int k = 0; k < n; k++) {
                boolean add = rnd.nextBoolean();
                StringBuilder sb = new StringBuilder();
                int len = 1 + rnd.nextInt(4);
                for (int j = 0; j < len; j++) sb.append(!add && rnd.nextInt(3) == 0 ? '.' : (char) ('a' + rnd.nextInt(3)));
                cmds.add((add ? "add:" : "search:") + sb);
            }
            if (!run(cmds).equals(oracle(cmds))) throw new AssertionError("differs on " + cmds);
        }
    }
}
```
