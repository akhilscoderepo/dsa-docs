<!-- solutions-for: 02-insert-and-search -->
### Insert And Search

#### Solution: [Build] Insert Lowercase Words (Author exercise)
<!-- id: tn-insert-lowercase -->

**Approach.** Walk the word with a cursor and create a child only at an empty slot, counting the creations. The count for a word then equals its length minus the number of leading letters that already had a route. The oracle keeps a set of all beginnings seen so far as plain strings, and the new nodes of a word are the beginnings of it that the set did not yet contain. The assertions compare the two on random words over a two-letter alphabet, which repeat often, and they also show the hazard stated in the lesson: a capital letter maps to a negative slot and fails with an `ArrayIndexOutOfBoundsException`.

**Complexity.** O(L) time per word, and at most L new nodes.

```java run
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Random;
import java.util.Set;

public final class InsertLowercase {
    static final class Node {
        final Node[] next = new Node[26];
    }

    static List<Integer> solve(List<String> words) {
        Node root = new Node();
        List<Integer> out = new ArrayList<>();
        for (String w : words) {
            Node cur = root;
            int made = 0;
            for (int i = 0; i < w.length(); i++) {
                int slot = w.charAt(i) - 'a';
                if (cur.next[slot] == null) { cur.next[slot] = new Node(); made++; }
                cur = cur.next[slot];
            }
            out.add(made);
        }
        return out;
    }

    static List<Integer> oracle(List<String> words) {
        Set<String> seen = new HashSet<>();
        List<Integer> out = new ArrayList<>();
        for (String w : words) {
            int made = 0;
            for (int k = 1; k <= w.length(); k++) if (seen.add(w.substring(0, k))) made++;
            out.add(made);
        }
        return out;
    }

    public static void main(String[] args) {
        if (!solve(List.of("car", "cart", "cat", "car")).equals(List.of(3, 1, 1, 0))) throw new AssertionError("example 1");
        if (!solve(List.of("b", "ba", "bad", "b")).equals(List.of(1, 1, 1, 0))) throw new AssertionError("example 2");
        if (!solve(List.of()).isEmpty()) throw new AssertionError("no words");
        if ('A' - 'a' != -32) throw new AssertionError("a capital gives slot -32");
        boolean failed = false;
        try { solve(List.of("Ab")); } catch (ArrayIndexOutOfBoundsException e) { failed = true; }
        if (!failed) throw new AssertionError("a capital letter must fall outside the 26 slots");
        Random rnd = new Random(18201);
        for (int t = 0; t < 5000; t++) {
            List<String> words = new ArrayList<>();
            int n = rnd.nextInt(10);
            for (int k = 0; k < n; k++) {
                StringBuilder sb = new StringBuilder();
                int len = 1 + rnd.nextInt(5);
                for (int j = 0; j < len; j++) sb.append((char) ('a' + rnd.nextInt(2)));
                words.add(sb.toString());
            }
            if (!solve(words).equals(oracle(words))) throw new AssertionError("differs on " + words);
        }
    }
}
```

#### Solution: [Vary] Search Versus StartsWith (Author exercise)
<!-- id: tn-search-versus-starts -->

**Approach.** After inserting every word, each probe is walked from the root. A missing slot gives 0. A successful walk gives 2 when the node is flagged and 1 when it is not, so the flag is read only after the walk has succeeded. The oracle uses a set of words and tests each probe with `contains` and with `startsWith` over the set, then combines the two answers into the code. The assertions compare on random inputs and check that the unflagged node of a shared route gives 1.

**Complexity.** O(total letters of words and probes) time.

```java run
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Random;
import java.util.Set;

public final class SearchVersusStarts {
    static final class Node {
        final Node[] next = new Node[26];
        boolean word;
    }

    static List<Integer> solve(List<String> words, List<String> probes) {
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
        for (String p : probes) {
            Node cur = root;
            for (int i = 0; i < p.length() && cur != null; i++) cur = cur.next[p.charAt(i) - 'a'];
            out.add(cur == null ? 0 : cur.word ? 2 : 1);
        }
        return out;
    }

    static List<Integer> oracle(List<String> words, List<String> probes) {
        Set<String> set = new HashSet<>(words);
        List<Integer> out = new ArrayList<>();
        for (String p : probes) {
            if (set.contains(p)) { out.add(2); continue; }
            boolean begins = false;
            for (String w : set) if (w.startsWith(p)) begins = true;
            out.add(begins ? 1 : 0);
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
        List<Integer> a = solve(List.of("tea", "ten", "to"), List.of("te", "tea", "tee", "t", "toe"));
        if (!a.equals(List.of(1, 2, 0, 1, 0))) throw new AssertionError("example 1");
        if (!solve(List.of("a"), List.of("a", "ab", "b")).equals(List.of(2, 0, 0))) throw new AssertionError("example 2");
        if (!solve(List.of(), List.of("a")).equals(List.of(0))) throw new AssertionError("empty trie");
        Random rnd = new Random(18202);
        for (int t = 0; t < 5000; t++) {
            List<String> words = new ArrayList<>(), probes = new ArrayList<>();
            int n = rnd.nextInt(7), m = 1 + rnd.nextInt(7);
            for (int k = 0; k < n; k++) words.add(word(rnd));
            for (int k = 0; k < m; k++) probes.add(word(rnd));
            if (!solve(words, probes).equals(oracle(words, probes))) throw new AssertionError("differs on " + words + probes);
        }
    }
}
```

#### Solution: [Boundary] Word Is Prefix Of Another (Author exercise)
<!-- id: tn-word-is-prefix -->

**Approach.** Insert every word, then walk each word again and report it when its final node has at least one child. Since the words are distinct and nonempty, a child below the final node means some other word extends it, so the word is a proper beginning of another. The answer does not depend on insertion order, which the assertions test by shuffling. The oracle compares every ordered pair with `startsWith` and inequality.

**Complexity.** O(total letters) time, and O(total letters) nodes.

```java run
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashSet;
import java.util.List;
import java.util.Random;
import java.util.Set;

public final class WordIsPrefix {
    static final class Node {
        final Node[] next = new Node[26];
        boolean hasChild;
    }

    static List<String> solve(List<String> words) {
        Node root = new Node();
        for (String w : words) {
            Node cur = root;
            for (char c : w.toCharArray()) {
                cur.hasChild = true;
                if (cur.next[c - 'a'] == null) cur.next[c - 'a'] = new Node();
                cur = cur.next[c - 'a'];
            }
        }
        List<String> out = new ArrayList<>();
        for (String w : words) {
            Node cur = root;
            for (char c : w.toCharArray()) cur = cur.next[c - 'a'];
            if (cur.hasChild) out.add(w);
        }
        return out;
    }

    static List<String> oracle(List<String> words) {
        List<String> out = new ArrayList<>();
        for (String w : words) {
            for (String other : words) {
                if (!other.equals(w) && other.startsWith(w)) { out.add(w); break; }
            }
        }
        return out;
    }

    public static void main(String[] args) {
        if (!solve(List.of("apple", "app", "ape")).equals(List.of("app"))) throw new AssertionError("example 1");
        if (!solve(List.of("a", "ab", "abc", "b", "zebra")).equals(List.of("a", "ab"))) throw new AssertionError("example 2");
        if (!solve(List.of()).isEmpty()) throw new AssertionError("no words");
        Random rnd = new Random(18203);
        for (int t = 0; t < 5000; t++) {
            Set<String> pick = new HashSet<>();
            int n = rnd.nextInt(9);
            for (int k = 0; k < n; k++) {
                StringBuilder sb = new StringBuilder();
                int len = 1 + rnd.nextInt(4);
                for (int j = 0; j < len; j++) sb.append((char) ('a' + rnd.nextInt(2)));
                pick.add(sb.toString());
            }
            List<String> words = new ArrayList<>(pick);
            Collections.shuffle(words, rnd);
            if (!solve(words).equals(oracle(words))) throw new AssertionError("differs on " + words);
        }
    }
}
```

#### Solution: [Recognize] Implement Trie (LeetCode 208)
<!-- id: tn-trie-domain-contract -->

**Approach.** The domain has 36 characters, so each node holds 36 slots and one function maps a character to its slot: letters to 0 to 25 and digits to 26 to 35. The three operations are the usual walk with a flag, and a counter increments whenever a node is created. The answers are written as 1 or 0 and the node count is appended at the end. The oracle keeps a set of words and the set of every beginning of every word as strings, so its node count is the size of the beginning set. The assertions replay the examples, check that the mapping is a bijection onto 0 to 35, and compare random scripts over a small mixed alphabet.

**Complexity.** O(L) per command, and O(36 * nodes) references.

```java run
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Random;
import java.util.Set;

public final class TrieDomainContract {
    static int slot(char c) {
        if (c >= 'a' && c <= 'z') return c - 'a';
        if (c >= '0' && c <= '9') return 26 + (c - '0');
        throw new IllegalArgumentException("outside the 36 character domain: " + c);
    }

    static final class Node {
        final Node[] next = new Node[36];
        boolean word;
    }

    static List<Integer> solve(List<String> commands) {
        Node root = new Node();
        int nodes = 0;
        List<Integer> out = new ArrayList<>();
        for (String cmd : commands) {
            int colon = cmd.indexOf(':');
            String op = cmd.substring(0, colon), s = cmd.substring(colon + 1);
            Node cur = root;
            if (op.equals("insert")) {
                for (char c : s.toCharArray()) {
                    if (cur.next[slot(c)] == null) { cur.next[slot(c)] = new Node(); nodes++; }
                    cur = cur.next[slot(c)];
                }
                cur.word = true;
            } else {
                for (int i = 0; i < s.length() && cur != null; i++) cur = cur.next[slot(s.charAt(i))];
                out.add(cur != null && (op.equals("startsWith") || cur.word) ? 1 : 0);
            }
        }
        out.add(nodes);
        return out;
    }

    static List<Integer> oracle(List<String> commands) {
        Set<String> words = new HashSet<>(), begins = new HashSet<>();
        List<Integer> out = new ArrayList<>();
        for (String cmd : commands) {
            int colon = cmd.indexOf(':');
            String op = cmd.substring(0, colon), s = cmd.substring(colon + 1);
            if (op.equals("insert")) {
                words.add(s);
                for (int k = 1; k <= s.length(); k++) begins.add(s.substring(0, k));
            } else if (op.equals("search")) out.add(words.contains(s) ? 1 : 0);
            else out.add(begins.contains(s) ? 1 : 0);
        }
        out.add(begins.size());
        return out;
    }

    public static void main(String[] args) {
        List<String> one = List.of("insert:ab1", "search:ab", "startsWith:ab", "search:ab1", "insert:b2", "startsWith:b");
        if (!solve(one).equals(List.of(0, 1, 1, 1, 5))) throw new AssertionError("example 1");
        List<String> two = List.of("search:7", "insert:7", "search:7", "startsWith:77");
        if (!solve(two).equals(List.of(0, 1, 0, 1))) throw new AssertionError("example 2");
        Set<Integer> used = new HashSet<>();
        for (char c = 'a'; c <= 'z'; c++) used.add(slot(c));
        for (char c = '0'; c <= '9'; c++) used.add(slot(c));
        if (used.size() != 36 || !used.contains(0) || !used.contains(35)) throw new AssertionError("slots must cover 0..35 exactly once");
        boolean rejected = false;
        try { slot('A'); } catch (IllegalArgumentException e) { rejected = true; }
        if (!rejected) throw new AssertionError("a capital is outside the contract");
        Random rnd = new Random(18204);
        String[] ops = {"insert", "search", "startsWith"};
        String alphabet = "ab12";
        for (int t = 0; t < 5000; t++) {
            List<String> cmds = new ArrayList<>();
            int n = rnd.nextInt(12);
            for (int k = 0; k < n; k++) {
                StringBuilder sb = new StringBuilder();
                int len = 1 + rnd.nextInt(4);
                for (int j = 0; j < len; j++) sb.append(alphabet.charAt(rnd.nextInt(alphabet.length())));
                cmds.add(ops[rnd.nextInt(3)] + ":" + sb);
            }
            if (!solve(cmds).equals(oracle(cmds))) throw new AssertionError("differs on " + cmds);
        }
    }
}
```
