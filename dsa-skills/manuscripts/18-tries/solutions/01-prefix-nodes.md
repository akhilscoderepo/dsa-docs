<!-- solutions-for: 01-prefix-nodes -->
### Prefix Nodes

#### Solution: [Build] Store Shared Prefixes (Author exercise)
<!-- id: tn-shared-prefixes -->

**Approach.** Insert the words one by one into a trie whose nodes hold a pass count, and create a node only when an edge is missing. After all insertions, `nodes` is the number of created nodes and `shared` is the number of non-root nodes with a pass count of at least two, because the words are distinct and each insertion adds one to every node on its own route. The oracle never builds a trie. It collects the set of all nonempty beginnings of all words, which is the node total, and for each beginning counts how many words start with it, which is the pass count. The assertions compare the two on random word lists over a small alphabet, and also check that `computeIfAbsent` leaves an existing child untouched.

**Complexity.** O(total letters) time, and O(total letters) space for the nodes.

```java run
import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Random;
import java.util.Set;

public final class SharedPrefixes {
    static final class Node {
        final Map<Character, Node> children = new HashMap<>();
        int pass;
    }

    static int[] solve(List<String> words) {
        Node root = new Node();
        int nodes = 0;
        for (String w : words) {
            Node cur = root;
            for (int i = 0; i < w.length(); i++) {
                Node next = cur.children.get(w.charAt(i));
                if (next == null) { next = new Node(); cur.children.put(w.charAt(i), next); nodes++; }
                cur = next;
                cur.pass++;
            }
        }
        int shared = 0;
        List<Node> pile = new ArrayList<>(root.children.values());
        while (!pile.isEmpty()) {
            Node n = pile.remove(pile.size() - 1);
            if (n.pass >= 2) shared++;
            pile.addAll(n.children.values());
        }
        return new int[] {nodes, shared};
    }

    static int[] oracle(List<String> words) {
        Set<String> beginnings = new HashSet<>();
        for (String w : words) for (int k = 1; k <= w.length(); k++) beginnings.add(w.substring(0, k));
        int shared = 0;
        for (String b : beginnings) {
            int c = 0;
            for (String w : words) if (w.startsWith(b)) c++;
            if (c >= 2) shared++;
        }
        return new int[] {beginnings.size(), shared};
    }

    static void same(int[] a, int[] b, String what) {
        if (a[0] != b[0] || a[1] != b[1]) throw new AssertionError(what + ": " + a[0] + "," + a[1] + " vs " + b[0] + "," + b[1]);
    }

    public static void main(String[] args) {
        same(solve(List.of("car", "cat")), new int[] {4, 2}, "example 1");
        same(solve(List.of("dog", "do", "dot")), new int[] {4, 2}, "example 2");
        same(solve(List.of()), new int[] {0, 0}, "no words");
        Map<Character, Node> kids = new HashMap<>();
        Node first = new Node();
        kids.computeIfAbsent('a', c -> first);
        if (kids.computeIfAbsent('a', c -> new Node()) != first) throw new AssertionError("computeIfAbsent replaced a child");
        Random rnd = new Random(18101);
        for (int t = 0; t < 4000; t++) {
            Set<String> pick = new HashSet<>();
            int n = rnd.nextInt(8);
            for (int k = 0; k < n; k++) {
                StringBuilder sb = new StringBuilder();
                int len = 1 + rnd.nextInt(5);
                for (int j = 0; j < len; j++) sb.append((char) ('a' + rnd.nextInt(3)));
                pick.add(sb.toString());
            }
            List<String> words = new ArrayList<>(pick);
            same(solve(words), oracle(words), "random " + words);
        }
    }
}
```

#### Solution: [Vary] Prefix Count (Author exercise)
<!-- id: tn-prefix-count -->

**Approach.** Every insertion adds one to the pass count of each node on its route, root included, and a `count` command walks its letters and returns the pass count where it stops, or zero when an edge is missing. Duplicates need no special rule, because a repeated word walks the same route and adds again. The oracle keeps the list of all inserted words and counts those with `startsWith`. The assertions compare the two on random scripts with a three-letter alphabet, and check that the root's pass count equals the number of insertions.

**Complexity.** O(L) per command for a string of length L.

```java run
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public final class PrefixCount {
    static final class Trie {
        final Trie[] next = new Trie[26];
        int pass;
    }

    static List<Integer> run(List<String> commands, Trie root) {
        List<Integer> out = new ArrayList<>();
        for (String cmd : commands) {
            int colon = cmd.indexOf(':');
            String op = cmd.substring(0, colon), s = cmd.substring(colon + 1);
            Trie cur = root;
            if (op.equals("insert")) {
                cur.pass++;
                for (char c : s.toCharArray()) {
                    if (cur.next[c - 'a'] == null) cur.next[c - 'a'] = new Trie();
                    cur = cur.next[c - 'a'];
                    cur.pass++;
                }
            } else {
                for (int i = 0; i < s.length() && cur != null; i++) cur = cur.next[s.charAt(i) - 'a'];
                out.add(cur == null ? 0 : cur.pass);
            }
        }
        return out;
    }

    static List<Integer> oracle(List<String> commands) {
        List<String> stored = new ArrayList<>();
        List<Integer> out = new ArrayList<>();
        for (String cmd : commands) {
            int colon = cmd.indexOf(':');
            String op = cmd.substring(0, colon), s = cmd.substring(colon + 1);
            if (op.equals("insert")) stored.add(s);
            else {
                int c = 0;
                for (String w : stored) if (w.startsWith(s)) c++;
                out.add(c);
            }
        }
        return out;
    }

    static String word(Random rnd) {
        StringBuilder sb = new StringBuilder();
        int len = 1 + rnd.nextInt(4);
        for (int j = 0; j < len; j++) sb.append((char) ('a' + rnd.nextInt(3)));
        return sb.toString();
    }

    public static void main(String[] args) {
        List<String> one = List.of("insert:apple", "insert:apply", "insert:ape", "count:ap", "count:app", "count:b");
        if (!run(one, new Trie()).equals(List.of(3, 2, 0))) throw new AssertionError("example 1");
        List<String> two = List.of("insert:a", "insert:a", "count:a", "count:ab");
        if (!run(two, new Trie()).equals(List.of(2, 0))) throw new AssertionError("example 2");
        if (!run(List.of(), new Trie()).isEmpty()) throw new AssertionError("empty script");
        Random rnd = new Random(18102);
        for (int t = 0; t < 4000; t++) {
            List<String> cmds = new ArrayList<>();
            int inserts = 0;
            int n = rnd.nextInt(14);
            for (int k = 0; k < n; k++) {
                if (rnd.nextBoolean()) { cmds.add("insert:" + word(rnd)); inserts++; }
                else cmds.add("count:" + word(rnd));
            }
            Trie root = new Trie();
            if (!run(cmds, root).equals(oracle(cmds))) throw new AssertionError("differs on " + cmds);
            if (root.pass != inserts) throw new AssertionError("root pass must equal insertions");
        }
    }
}
```

#### Solution: [Boundary] Empty Word And Prefix-Only Node (Author exercise)
<!-- id: tn-empty-and-prefix-only -->

**Approach.** The root exists from the start, so its existence says nothing. A `prefix` command walks its letters and answers true only when the node reached has a positive pass count, which makes the empty beginning true exactly when something has been inserted. A `search` command also needs the terminal flag at the node reached, and an inserted empty word sets the flag on the root itself. The oracle keeps a set of inserted words and checks `startsWith` over it, so it has no notion of nodes. The assertions compare the two on random scripts that include empty strings, and check the two examples plus the case of a node that exists only because a longer word passes through it.

**Complexity.** O(L) per command for a string of length L.

```java run
import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Random;
import java.util.Set;

public final class EmptyAndPrefixOnly {
    static final class Node {
        final Map<Character, Node> kids = new HashMap<>();
        boolean flag;
        int pass;
    }

    static List<Boolean> run(List<String> commands) {
        Node root = new Node();
        List<Boolean> out = new ArrayList<>();
        for (String cmd : commands) {
            int colon = cmd.indexOf(':');
            String op = cmd.substring(0, colon), s = cmd.substring(colon + 1);
            if (op.equals("insert")) {
                Node cur = root;
                cur.pass++;
                for (char c : s.toCharArray()) {
                    cur = cur.kids.computeIfAbsent(c, k -> new Node());
                    cur.pass++;
                }
                cur.flag = true;
            } else {
                Node cur = root;
                for (int i = 0; i < s.length() && cur != null; i++) cur = cur.kids.get(s.charAt(i));
                if (op.equals("search")) out.add(cur != null && cur.flag);
                else out.add(cur != null && cur.pass > 0);
            }
        }
        return out;
    }

    static List<Boolean> oracle(List<String> commands) {
        Set<String> words = new HashSet<>();
        List<Boolean> out = new ArrayList<>();
        for (String cmd : commands) {
            int colon = cmd.indexOf(':');
            String op = cmd.substring(0, colon), s = cmd.substring(colon + 1);
            if (op.equals("insert")) words.add(s);
            else if (op.equals("search")) out.add(words.contains(s));
            else {
                boolean any = false;
                for (String w : words) if (w.startsWith(s)) any = true;
                out.add(any);
            }
        }
        return out;
    }

    static String piece(Random rnd) {
        StringBuilder sb = new StringBuilder();
        int len = rnd.nextInt(4);
        for (int j = 0; j < len; j++) sb.append((char) ('a' + rnd.nextInt(2)));
        return sb.toString();
    }

    public static void main(String[] args) {
        List<String> one = List.of("prefix:", "search:", "insert:", "search:", "prefix:", "search:x");
        if (!run(one).equals(List.of(false, false, true, true, false))) throw new AssertionError("example 1");
        List<String> two = List.of("insert:car", "prefix:", "search:", "prefix:ca", "search:ca", "search:car");
        if (!run(two).equals(List.of(true, false, true, false, true))) throw new AssertionError("example 2");
        if (run(List.of("insert:ab", "search:a")).equals(List.of(true))) throw new AssertionError("a node on a longer route is not a word");
        Random rnd = new Random(18103);
        String[] ops = {"insert", "search", "prefix"};
        for (int t = 0; t < 5000; t++) {
            List<String> cmds = new ArrayList<>();
            int n = rnd.nextInt(12);
            for (int k = 0; k < n; k++) cmds.add(ops[rnd.nextInt(3)] + ":" + piece(rnd));
            if (!run(cmds).equals(oracle(cmds))) throw new AssertionError("differs on " + cmds);
        }
    }
}
```

#### Solution: [Recognize] Implement Trie (LeetCode 208)
<!-- id: tn-implement-trie -->

**Approach.** One trie answers all three commands. `insert` creates the missing edges along the word and flags the last node. `search` and `startsWith` share one walk helper that returns the node reached or null, and they differ only in the final test: the flag for `search`, and bare existence for `startsWith`. Existence is safe here because an inserted word is never empty, so every node other than the root lies on the route of some stored word. The oracle holds the words in a hash set and scans for `startsWith`. The assertions replay the two examples and then random scripts over a three-letter alphabet, which produce many words that are beginnings of other words.

**Complexity.** O(L) per command, with at most one node per distinct nonempty beginning.

```java run
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Random;
import java.util.Set;

public final class ImplementTrie {
    static final class Trie {
        private final Trie[] next = new Trie[26];
        private boolean word;

        void insert(String w) {
            Trie cur = this;
            for (int i = 0; i < w.length(); i++) {
                int e = w.charAt(i) - 'a';
                if (cur.next[e] == null) cur.next[e] = new Trie();
                cur = cur.next[e];
            }
            cur.word = true;
        }

        private Trie reach(String s) {
            Trie cur = this;
            for (int i = 0; i < s.length() && cur != null; i++) cur = cur.next[s.charAt(i) - 'a'];
            return cur;
        }

        boolean search(String w) {
            Trie end = reach(w);
            return end != null && end.word;
        }

        boolean startsWith(String p) {
            return reach(p) != null;
        }
    }

    static List<Boolean> run(List<String> commands) {
        Trie trie = new Trie();
        List<Boolean> out = new ArrayList<>();
        for (String cmd : commands) {
            int colon = cmd.indexOf(':');
            String op = cmd.substring(0, colon), s = cmd.substring(colon + 1);
            switch (op) {
                case "insert" -> trie.insert(s);
                case "search" -> out.add(trie.search(s));
                default -> out.add(trie.startsWith(s));
            }
        }
        return out;
    }

    static List<Boolean> oracle(List<String> commands) {
        Set<String> words = new HashSet<>();
        List<Boolean> out = new ArrayList<>();
        for (String cmd : commands) {
            int colon = cmd.indexOf(':');
            String op = cmd.substring(0, colon), s = cmd.substring(colon + 1);
            if (op.equals("insert")) words.add(s);
            else if (op.equals("search")) out.add(words.contains(s));
            else {
                boolean any = false;
                for (String w : words) if (w.startsWith(s)) any = true;
                out.add(any);
            }
        }
        return out;
    }

    public static void main(String[] args) {
        List<String> one = List.of("insert:apple", "search:apple", "search:app", "startsWith:app", "insert:app", "search:app");
        if (!run(one).equals(List.of(true, false, true, true))) throw new AssertionError("example 1");
        List<String> two = List.of("insert:ab", "startsWith:b", "search:abc", "startsWith:ab");
        if (!run(two).equals(List.of(false, false, true))) throw new AssertionError("example 2");
        Random rnd = new Random(18104);
        String[] ops = {"insert", "search", "startsWith"};
        for (int t = 0; t < 5000; t++) {
            List<String> cmds = new ArrayList<>();
            int n = rnd.nextInt(14);
            for (int k = 0; k < n; k++) {
                StringBuilder sb = new StringBuilder();
                int len = 1 + rnd.nextInt(4);
                for (int j = 0; j < len; j++) sb.append((char) ('a' + rnd.nextInt(3)));
                cmds.add(ops[rnd.nextInt(3)] + ":" + sb);
            }
            if (!run(cmds).equals(oracle(cmds))) throw new AssertionError("differs on " + cmds);
        }
    }
}
```
