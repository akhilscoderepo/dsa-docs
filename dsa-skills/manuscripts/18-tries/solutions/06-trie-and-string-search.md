<!-- solutions-for: 06-trie-and-string-search -->
### Trie And String Search

#### Solution: [Build] Implement Trie (LeetCode 208)
<!-- id: ts-trie-distinct-words -->

**Approach.** Each node holds a flag and `under`, the number of different stored words at or below the node. Insertion first walks the word and creates missing nodes. If the final node was not flagged, the word is new, so the flag is set and a second walk adds one to `under` on every node of the route, root included. A repeated word finds the flag already set and changes nothing. `search` needs the node and its flag, `startsWith` needs the node to have a positive `under`, which keeps the empty trie from answering yes for the empty prefix, and `distinct` returns `under` of the node or 0 for a missing route. The empty prefix stops at the root, whose `under` is the number of stored words. The oracle keeps a hash set of the words and counts with `startsWith` over the set. The assertions replay the examples and compare random scripts over a three-letter alphabet with many repeated words.

**Complexity.** O(L) per command for a string of length L.

```java run
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Random;
import java.util.Set;

public final class TrieDistinctWords {
    static final class Node {
        final Node[] next = new Node[26];
        boolean flag;
        int under;
    }

    static Node reach(Node root, String s) {
        Node cur = root;
        for (int i = 0; i < s.length() && cur != null; i++) cur = cur.next[s.charAt(i) - 'a'];
        return cur;
    }

    static List<Integer> run(List<String> commands) {
        Node root = new Node();
        List<Integer> out = new ArrayList<>();
        for (String cmd : commands) {
            int colon = cmd.indexOf(':');
            String op = cmd.substring(0, colon), s = cmd.substring(colon + 1);
            switch (op) {
                case "insert" -> {
                    Node cur = root;
                    for (char c : s.toCharArray()) {
                        if (cur.next[c - 'a'] == null) cur.next[c - 'a'] = new Node();
                        cur = cur.next[c - 'a'];
                    }
                    if (!cur.flag) {
                        cur.flag = true;
                        Node walk = root;
                        walk.under++;
                        for (char c : s.toCharArray()) { walk = walk.next[c - 'a']; walk.under++; }
                    }
                }
                case "search" -> { Node n = reach(root, s); out.add(n != null && n.flag ? 1 : 0); }
                case "startsWith" -> { Node n = reach(root, s); out.add(n != null && n.under > 0 ? 1 : 0); }
                default -> { Node n = reach(root, s); out.add(n == null ? 0 : n.under); }
            }
        }
        return out;
    }

    static List<Integer> oracle(List<String> commands) {
        Set<String> words = new HashSet<>();
        List<Integer> out = new ArrayList<>();
        for (String cmd : commands) {
            int colon = cmd.indexOf(':');
            String op = cmd.substring(0, colon), s = cmd.substring(colon + 1);
            if (op.equals("insert")) { words.add(s); continue; }
            int c = 0;
            for (String w : words) if (w.startsWith(s)) c++;
            if (op.equals("search")) out.add(words.contains(s) ? 1 : 0);
            else if (op.equals("startsWith")) out.add(c > 0 ? 1 : 0);
            else out.add(c);
        }
        return out;
    }

    static String text(Random rnd, int min, int max) {
        StringBuilder sb = new StringBuilder();
        int len = min + rnd.nextInt(max - min + 1);
        for (int j = 0; j < len; j++) sb.append((char) ('a' + rnd.nextInt(3)));
        return sb.toString();
    }

    public static void main(String[] args) {
        List<String> one = List.of("insert:car", "insert:car", "insert:cart", "distinct:ca", "search:ca", "startsWith:ca", "distinct:cars");
        if (!run(one).equals(List.of(2, 0, 1, 0))) throw new AssertionError("example 1");
        List<String> two = List.of("insert:ab", "insert:ab", "insert:b", "distinct:", "distinct:b", "startsWith:abc");
        if (!run(two).equals(List.of(2, 1, 0))) throw new AssertionError("example 2");
        if (!run(List.of("startsWith:", "distinct:")).equals(List.of(0, 0))) throw new AssertionError("empty trie has no words");
        Random rnd = new Random(18601);
        String[] ops = {"insert", "insert", "search", "startsWith", "distinct"};
        for (int t = 0; t < 5000; t++) {
            List<String> cmds = new ArrayList<>();
            int n = rnd.nextInt(14);
            for (int k = 0; k < n; k++) {
                String op = ops[rnd.nextInt(ops.length)];
                boolean maybeEmpty = op.equals("startsWith") || op.equals("distinct");
                cmds.add(op + ":" + text(rnd, maybeEmpty ? 0 : 1, 3));
            }
            if (!run(cmds).equals(oracle(cmds))) throw new AssertionError("differs on " + cmds);
        }
    }
}
```

#### Solution: [Vary] Design Add and Search Words Data Structure (LeetCode 211)
<!-- id: ts-wildcard-search-cost -->

**Approach.** The recursive call takes a node and a position and increments a counter each time it enters a child node. At a letter it follows the one edge if it exists, and entering that child counts once. At a dot it loops over the slots in alphabetical order, enters each existing child and returns true on the first success, so later children are never entered. At the end of the pattern the answer is the flag. A missing edge counts nothing. The answer is checked against a plain scan of the word list, which does not use the trie. The visited count is checked against a second implementation of the same rule over a set of all beginnings kept as strings, where a child exists when the longer string is in the set. The assertions compare both on random inputs, and check that a pattern without dots never visits more nodes than its length.

**Complexity.** O(total letters stored) per pattern in the worst case, and O(L) without dots.

```java run
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Random;
import java.util.Set;

public final class WildcardSearchCost {
    static final class Node {
        final Node[] next = new Node[26];
        boolean word;
    }

    static int visited;

    static boolean go(Node node, String p, int pos) {
        if (pos == p.length()) return node.word;
        char c = p.charAt(pos);
        for (int e = 0; e < 26; e++) {
            Node child = node.next[e];
            if (child == null || (c != '.' && c - 'a' != e)) continue;
            visited++;
            if (go(child, p, pos + 1)) return true;
        }
        return false;
    }

    static List<int[]> solve(List<String> words, List<String> patterns) {
        Node root = new Node();
        for (String w : words) {
            Node cur = root;
            for (char c : w.toCharArray()) {
                if (cur.next[c - 'a'] == null) cur.next[c - 'a'] = new Node();
                cur = cur.next[c - 'a'];
            }
            cur.word = true;
        }
        List<int[]> out = new ArrayList<>();
        for (String p : patterns) {
            visited = 0;
            boolean ok = go(root, p, 0);
            out.add(new int[] {ok ? 1 : 0, visited});
        }
        return out;
    }

    static int oVisited;

    static boolean oGo(String prefix, String p, int pos, Set<String> begins, Set<String> words) {
        if (pos == p.length()) return words.contains(prefix);
        for (char ch = 'a'; ch <= 'z'; ch++) {
            if (p.charAt(pos) != '.' && p.charAt(pos) != ch) continue;
            if (!begins.contains(prefix + ch)) continue;
            oVisited++;
            if (oGo(prefix + ch, p, pos + 1, begins, words)) return true;
        }
        return false;
    }

    static boolean scan(List<String> words, String p) {
        for (String w : words) {
            if (w.length() != p.length()) continue;
            boolean ok = true;
            for (int i = 0; i < p.length(); i++) if (p.charAt(i) != '.' && p.charAt(i) != w.charAt(i)) ok = false;
            if (ok) return true;
        }
        return false;
    }

    static String text(Random rnd, int len, boolean dots) {
        StringBuilder sb = new StringBuilder();
        for (int j = 0; j < len; j++) sb.append(dots && rnd.nextInt(3) == 0 ? '.' : (char) ('a' + rnd.nextInt(3)));
        return sb.toString();
    }

    public static void main(String[] args) {
        List<int[]> a = solve(List.of("tin", "ton", "tan", "tex"), List.of("t.n", "t.z", "x.n", "..x"));
        String got = a.stream().map(r -> r[0] + "," + r[1]).toList().toString();
        if (!got.equals("[1,3, 0,5, 0,0, 1,4]")) throw new AssertionError("example 1 " + got);
        got = solve(List.of("a"), List.of(".", "a", "b", "..")).stream().map(r -> r[0] + "," + r[1]).toList().toString();
        if (!got.equals("[1,1, 1,1, 0,0, 0,1]")) throw new AssertionError("example 2 " + got);
        Random rnd = new Random(18602);
        for (int t = 0; t < 5000; t++) {
            Set<String> pick = new HashSet<>();
            int n = rnd.nextInt(7);
            for (int k = 0; k < n; k++) pick.add(text(rnd, 1 + rnd.nextInt(4), false));
            List<String> words = new ArrayList<>(pick), patterns = new ArrayList<>();
            for (int k = 0; k < 6; k++) patterns.add(text(rnd, 1 + rnd.nextInt(4), true));
            Set<String> begins = new HashSet<>();
            for (String w : words) for (int k = 1; k <= w.length(); k++) begins.add(w.substring(0, k));
            List<int[]> res = solve(words, patterns);
            for (int k = 0; k < patterns.size(); k++) {
                String p = patterns.get(k);
                oVisited = 0;
                boolean ok = oGo("", p, 0, begins, pick);
                if (res.get(k)[0] != (ok ? 1 : 0) || res.get(k)[1] != oVisited) throw new AssertionError("differs on " + words + p);
                if (res.get(k)[0] != (scan(words, p) ? 1 : 0)) throw new AssertionError("answer differs from the scan on " + words + p);
                if (p.indexOf('.') < 0 && res.get(k)[1] > p.length()) throw new AssertionError("no dots means one route");
            }
        }
    }
}
```

#### Solution: [Boundary] Replace Words (LeetCode 648)
<!-- id: ts-replace-words -->

**Approach.** Store the roots in a trie with a flag. For each word of the sentence, a cursor walks its letters. A missing edge ends the walk and the word stays whole. The first flagged node ends the walk and the word becomes the prefix read so far, which is the shortest root because every shorter beginning was seen unflagged. A word that ends before any flag also stays whole, so a root longer than the word never applies. The answers are joined with single spaces through a `StringBuilder`. The oracle tests every root against every word with `startsWith` and keeps the shortest. The assertions compare the two on random sentences and root lists, and check that a word shorter than the only root is kept.

**Complexity.** O(total root letters + total sentence letters).

```java run
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Random;
import java.util.Set;

public final class ReplaceWords {
    static final class Node {
        final Node[] next = new Node[26];
        boolean root;
    }

    static String solve(List<String> roots, String sentence) {
        Node top = new Node();
        for (String r : roots) {
            Node cur = top;
            for (char c : r.toCharArray()) {
                if (cur.next[c - 'a'] == null) cur.next[c - 'a'] = new Node();
                cur = cur.next[c - 'a'];
            }
            cur.root = true;
        }
        StringBuilder out = new StringBuilder();
        for (String word : sentence.split(" ")) {
            String piece = word;
            Node cur = top;
            for (int i = 0; i < word.length(); i++) {
                cur = cur.next[word.charAt(i) - 'a'];
                if (cur == null) break;
                if (cur.root) { piece = word.substring(0, i + 1); break; }
            }
            if (out.length() > 0) out.append(' ');
            out.append(piece);
        }
        return out.toString();
    }

    static String oracle(List<String> roots, String sentence) {
        List<String> parts = new ArrayList<>();
        for (String word : sentence.split(" ")) {
            String best = word;
            for (String r : roots) if (word.startsWith(r) && (best == word || r.length() < best.length())) best = r;
            parts.add(best);
        }
        return String.join(" ", parts);
    }

    static String text(Random rnd, int min, int max) {
        StringBuilder sb = new StringBuilder();
        int len = min + rnd.nextInt(max - min + 1);
        for (int j = 0; j < len; j++) sb.append((char) ('a' + rnd.nextInt(3)));
        return sb.toString();
    }

    public static void main(String[] args) {
        if (!solve(List.of("ab", "abc", "x"), "abcd abx xyz zzz ab a").equals("ab ab x zzz ab a")) throw new AssertionError("example 1");
        if (!solve(List.of("bat", "cab"), "batman cabin ba tab").equals("bat cab ba tab")) throw new AssertionError("example 2");
        if (!solve(List.of("abc"), "ab").equals("ab")) throw new AssertionError("a word shorter than the root stays");
        if (!solve(List.of(), "x y").equals("x y")) throw new AssertionError("no roots");
        Random rnd = new Random(18603);
        for (int t = 0; t < 5000; t++) {
            Set<String> pick = new HashSet<>();
            int n = rnd.nextInt(6);
            for (int k = 0; k < n; k++) pick.add(text(rnd, 1, 3));
            List<String> roots = new ArrayList<>(pick), words = new ArrayList<>();
            int m = 1 + rnd.nextInt(6);
            for (int k = 0; k < m; k++) words.add(text(rnd, 1, 5));
            String sentence = String.join(" ", words);
            if (!solve(roots, sentence).equals(oracle(roots, sentence))) throw new AssertionError("differs on " + roots + sentence);
        }
    }
}
```

#### Solution: [Recognize] Longest Word in Dictionary (LeetCode 720)
<!-- id: ts-longest-buildable -->

**Approach.** Insert all words and flag their end nodes. Then run a depth-first search from the root that enters a child only if the child is flagged, visiting slots in alphabetical order, with a builder that spells the path. Every node entered has a chain of flagged nodes above it, so its path is a buildable word. The best string is replaced only when the path is strictly longer, and since alphabetical order visits smaller words first, the first word of the maximum length wins ties. If no first letter is a word, nothing is entered and the answer is the empty string. The oracle puts the words in a set, checks every beginning of every word as a string, and picks the longest and then the smallest. The assertions compare the two on random lists with many repeated and nested words.

**Complexity.** O(total letters) to build and O(number of nodes) to search.

```java run
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Random;
import java.util.Set;

public final class LongestBuildable {
    static final class Node {
        final Node[] next = new Node[26];
        boolean flag;
    }

    static String best;

    static void dfs(Node node, StringBuilder path) {
        for (int e = 0; e < 26; e++) {
            Node child = node.next[e];
            if (child == null || !child.flag) continue;
            path.append((char) ('a' + e));
            if (path.length() > best.length()) best = path.toString();
            dfs(child, path);
            path.setLength(path.length() - 1);
        }
    }

    static String solve(List<String> words) {
        Node root = new Node();
        for (String w : words) {
            Node cur = root;
            for (char c : w.toCharArray()) {
                if (cur.next[c - 'a'] == null) cur.next[c - 'a'] = new Node();
                cur = cur.next[c - 'a'];
            }
            cur.flag = true;
        }
        best = "";
        dfs(root, new StringBuilder());
        return best;
    }

    static String oracle(List<String> words) {
        Set<String> set = new HashSet<>(words);
        String best = "";
        for (String w : set) {
            boolean ok = true;
            for (int k = 1; k <= w.length(); k++) if (!set.contains(w.substring(0, k))) ok = false;
            if (ok && (w.length() > best.length() || (w.length() == best.length() && w.compareTo(best) < 0))) best = w;
        }
        return best;
    }

    public static void main(String[] args) {
        if (!solve(List.of("ab", "a", "abc", "b", "bd", "abd", "bde")).equals("abc")) throw new AssertionError("example 1");
        if (!solve(List.of("xyz", "xy")).equals("")) throw new AssertionError("example 2");
        if (!solve(List.of("a", "a", "a")).equals("a")) throw new AssertionError("repeated words");
        Random rnd = new Random(18604);
        for (int t = 0; t < 5000; t++) {
            List<String> words = new ArrayList<>();
            int n = 1 + rnd.nextInt(10);
            for (int k = 0; k < n; k++) {
                StringBuilder sb = new StringBuilder();
                int len = 1 + rnd.nextInt(4);
                for (int j = 0; j < len; j++) sb.append((char) ('a' + rnd.nextInt(2)));
                words.add(sb.toString());
            }
            if (!solve(words).equals(oracle(words))) throw new AssertionError("differs on " + words);
        }
    }
}
```
