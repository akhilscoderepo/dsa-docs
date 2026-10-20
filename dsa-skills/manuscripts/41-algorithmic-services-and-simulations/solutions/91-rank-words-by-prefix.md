<!-- solutions-for: 91-rank-words-by-prefix -->
### Solutions For Rank Words By Prefix

#### Solution: [Build] Prefix Maximum Under Overwrite (LeetCode 677)
<!-- id: sv-rank-prefix-max -->

**Approach.** A trie holds one number per node, and the number is the largest value among the keys below that node. The contract says an overwrite never lowers a value, so a node never needs to forget an old value. Its number only grows.

A put call walks the key's path. At each node it replaces the number with the larger of the old number and the new value. A max call walks the prefix and returns the number of the node it reaches, or -1 for a missing node.

The invariant is that every node's number equals the largest current value among the keys below it. A put raises one key, and every node on that key's path is exactly a node whose set of keys contains it, so the maximum of each of those nodes is repaired and no other node changes.

**Complexity.**

- **Time** is O(L) per put and per max, where L is the key or prefix length, because each step does one array lookup and one comparison.
- **Space** is O(total characters of the distinct keys), because each trie node stores one number.

```java run
import java.util.*;

public final class PrefixMaxSolution {
    static final class PrefixMax {
        private static final class Node {
            final Node[] next = new Node[26];
            int best = -1;                              // -1 means no key below this node
        }
        private final Node root = new Node();

        /**
         * Raises the maximum on every node of the key's path.
         * Time: O(L).
         * Space: O(L) for new nodes.
         * Invariant: each node holds the largest current value below it; values never fall.
         */
        void put(String key, int value) {
            Node cur = root;
            for (int i = 0; i < key.length(); i++) {
                int c = key.charAt(i) - 'a';
                // A missing child is created on the way down.
                if (cur.next[c] == null) cur.next[c] = new Node();
                cur = cur.next[c];
                // The larger of the old maximum and the new value stays.
                cur.best = Math.max(cur.best, value);
            }
        }

        /** Returns the largest value below the prefix, or -1; O(L) time, O(1) space. */
        int max(String prefix) {
            Node cur = root;
            // The walk stops early when a letter has no child.
            for (int i = 0; i < prefix.length() && cur != null; i++) cur = cur.next[prefix.charAt(i) - 'a'];
            return cur == null ? -1 : cur.best;
        }
    }

    public static void main(String[] args) {
        // Example 1 and Example 2 from the problem text.
        PrefixMax a = new PrefixMax();
        a.put("apple", 3); a.put("app", 5);
        if (a.max("ap") != 5) throw new AssertionError("e1 first");
        a.put("apple", 9);
        if (a.max("ap") != 9 || a.max("b") != -1) throw new AssertionError("e1 second");
        PrefixMax b = new PrefixMax();
        b.put("ab", 4); b.put("ab", 9);
        if (b.max("a") != 9) throw new AssertionError("e2 first");
        b.put("ac", 6);
        if (b.max("a") != 9 || b.max("ab") != 9) throw new AssertionError("e2 second");
        // Random calls with non-decreasing overwrites, checked against a scan of a plain map.
        Random rnd = new Random(4101);
        String[] keys = {"a", "ab", "abc", "b", "ba", "bb", "abb"};
        String[] prefixes = {"a", "ab", "abc", "b", "ba", "bc", "c"};
        for (int round = 0; round < 400; round++) {
            PrefixMax s = new PrefixMax();
            Map<String, Integer> ref = new HashMap<>();
            for (int op = 0; op < 80; op++) {
                if (rnd.nextBoolean()) {
                    String k = keys[rnd.nextInt(keys.length)];
                    int v = ref.getOrDefault(k, 0) + rnd.nextInt(3);   // an overwrite never lowers the value
                    ref.put(k, v);
                    s.put(k, v);
                } else {
                    String p = prefixes[rnd.nextInt(prefixes.length)];
                    int want = -1;
                    for (Map.Entry<String, Integer> e : ref.entrySet()) if (e.getKey().startsWith(p)) want = Math.max(want, e.getValue());
                    if (s.max(p) != want) throw new AssertionError("max " + p);
                }
            }
        }
    }
}
```

#### Solution: [Vary] Count Near Words Within A Budget (LeetCode 676)
<!-- id: sv-rank-near-words -->

**Approach.** The trie stores each distinct dictionary word and marks its last node as a word end. A query runs a depth-first search that carries the position in the query and the remaining budget. At each node the search tries every child. A child whose letter equals the query letter costs nothing. Any other child costs one unit and is skipped when the budget is zero. When the position reaches the query length, the search counts one if the node ends a word.

Each dictionary word has exactly one path in the trie, so the search reaches it at most once and a repeated word is counted once. Words of a different length never reach a word end at the right depth, so the length rule needs no extra check.

The invariant is that the search at a node with position p and budget b counts the word ends below it whose letters from position p differ from the query in at most b places.

**Complexity.**

- **Time** is O(25^d * L^(d+1)) per query in the worst case, where d is the budget, at most 2. The search branches into at most 25 wrong letters at each of at most d mismatching positions, and it spends O(L) steps on each branch. The trie size also bounds it.
- **Space** is O(L) for the recursion, plus O(S) for the trie with S nodes.

```java run
import java.util.*;

public final class NearWordsSolution {
    static final class NearDictionary {
        private static final class Node {
            final Node[] next = new Node[26];
            boolean end;
        }
        private final Node root = new Node();

        NearDictionary(String[] words) {
            for (String w : words) {
                Node cur = root;
                for (int i = 0; i < w.length(); i++) {
                    int c = w.charAt(i) - 'a';
                    if (cur.next[c] == null) cur.next[c] = new Node();
                    cur = cur.next[c];
                }
                // A repeated word marks the same node, so it counts once.
                cur.end = true;
            }
        }

        /**
         * Counts the word ends reachable with at most the remaining budget of mismatches.
         * Time: O(25^d * L^(d+1)) in the worst case.
         * Space: O(L) recursion.
         * Invariant: the result counts words below node that match q from pos with at most budget differences.
         */
        private int dfs(Node node, String q, int pos, int budget) {
            // The end of the query counts the node only when a word ends here.
            if (pos == q.length()) return node.end ? 1 : 0;
            int total = 0;
            int want = q.charAt(pos) - 'a';
            for (int c = 0; c < 26; c++) {
                Node child = node.next[c];
                if (child == null) continue;
                // A matching letter is free; any other letter spends one unit of budget.
                int cost = c == want ? 0 : 1;
                if (cost <= budget) total += dfs(child, q, pos + 1, budget - cost);
            }
            return total;
        }

        int countWithin(String query, int d) { return dfs(root, query, 0, d); }
    }

    public static void main(String[] args) {
        // Example 1 and Example 2 from the problem text.
        NearDictionary a = new NearDictionary(new String[] {"hello", "hallo", "hullo", "help", "hello"});
        if (a.countWithin("hello", 0) != 1 || a.countWithin("hello", 1) != 3 || a.countWithin("hxllo", 1) != 3) throw new AssertionError("e1");
        NearDictionary b = new NearDictionary(new String[] {"abc", "abd", "xyz"});
        if (b.countWithin("abz", 1) != 2 || b.countWithin("abz", 2) != 3) throw new AssertionError("e2");
        // Random dictionaries checked against a Hamming distance scan.
        Random rnd = new Random(4102);
        for (int round = 0; round < 500; round++) {
            int n = 1 + rnd.nextInt(8);
            String[] words = new String[n];
            for (int i = 0; i < n; i++) words[i] = rand(rnd, 1 + rnd.nextInt(4));
            NearDictionary s = new NearDictionary(words);
            Set<String> distinct = new HashSet<>(Arrays.asList(words));
            for (int q = 0; q < 20; q++) {
                String query = rand(rnd, 1 + rnd.nextInt(4));
                int d = rnd.nextInt(3), want = 0;
                for (String w : distinct) {
                    if (w.length() != query.length()) continue;
                    int diff = 0;
                    for (int i = 0; i < w.length(); i++) if (w.charAt(i) != query.charAt(i)) diff++;
                    if (diff <= d) want++;
                }
                if (s.countWithin(query, d) != want) throw new AssertionError("count " + query + " " + d);
            }
        }
    }

    private static String rand(Random rnd, int len) {
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < len; i++) sb.append((char) ('a' + rnd.nextInt(3)));
        return sb.toString();
    }
}
```

#### Solution: [Boundary] Prefix And Suffix Filter (LeetCode 745)
<!-- id: sv-rank-affix-filter -->

**Approach.** Each word is inserted into one trie once for every suffix start, including the empty suffix. The inserted key is the suffix, then the separator `{`, then the whole word. The separator is the character after `z`, so the alphabet has 27 letters. The query key is the query suffix, the separator and the query prefix. One walk of that key checks both constraints, because the key begins with a suffix of the word and then continues with the word itself from its first letter.

Every node on an inserted key stores the largest index of any word whose key passes through it. Words arrive in index order, so each new index is at least as large as any stored index, and an overwrite is enough. A repeated word therefore replaces its earlier index. The empty prefix or the empty suffix needs no special case.

The invariant is that a node's value is the largest index among the words with a key that starts with the path to the node.

**Complexity.**

- **Time** is O(L^2) per word at construction and O(L) per query, where L is the word length. Each word inserts L + 1 keys of length at most 2L + 1.
- **Space** is O(n * L^2) trie nodes in the worst case, since each word contributes L + 1 keys of length O(L).

```java run
import java.util.*;

public final class AffixFilterSolution {
    static final class WordFilter {
        private static final class Node {
            final Node[] next = new Node[27];
            int best = -1;
        }
        private final Node root = new Node();

        WordFilter(String[] words) {
            for (int i = 0; i < words.length; i++) {
                String w = words[i];
                // One key per suffix start; the empty suffix is included.
                for (int s = 0; s <= w.length(); s++) {
                    String key = w.substring(s) + "{" + w;
                    Node cur = root;
                    for (int k = 0; k < key.length(); k++) {
                        int c = key.charAt(k) - 'a';
                        if (cur.next[c] == null) cur.next[c] = new Node();
                        cur = cur.next[c];
                        // Later words have larger indexes, so the overwrite keeps the maximum.
                        cur.best = i;
                    }
                }
            }
        }

        /** Returns the largest index of a word with the prefix and the suffix, or -1; O(L) time, O(1) space. */
        int f(String prefix, String suffix) {
            String key = suffix + "{" + prefix;
            Node cur = root;
            // A missing child means no word has both parts.
            for (int k = 0; k < key.length() && cur != null; k++) cur = cur.next[key.charAt(k) - 'a'];
            return cur == null ? -1 : cur.best;
        }
    }

    public static void main(String[] args) {
        // Example 1 and Example 2 from the problem text.
        WordFilter a = new WordFilter(new String[] {"apple", "ample", "maple"});
        if (a.f("a", "e") != 1 || a.f("ap", "le") != 0 || a.f("m", "e") != 2 || a.f("z", "e") != -1) throw new AssertionError("e1");
        WordFilter b = new WordFilter(new String[] {"bob", "bob", "bo"});
        if (b.f("bo", "b") != 1 || b.f("bo", "o") != 2 || b.f("", "b") != 1) throw new AssertionError("e2");
        // Random words checked against a scan from the last index.
        Random rnd = new Random(4103);
        for (int round = 0; round < 500; round++) {
            int n = 1 + rnd.nextInt(7);
            String[] words = new String[n];
            for (int i = 0; i < n; i++) words[i] = rand(rnd, 1 + rnd.nextInt(4));
            WordFilter s = new WordFilter(words);
            for (int q = 0; q < 20; q++) {
                String p = rand(rnd, rnd.nextInt(4)), x = rand(rnd, rnd.nextInt(4));
                int want = -1;
                for (int i = n - 1; i >= 0 && want == -1; i--) if (words[i].startsWith(p) && words[i].endsWith(x)) want = i;
                if (s.f(p, x) != want) throw new AssertionError("f " + p + " " + x);
            }
        }
    }

    private static String rand(Random rnd, int len) {
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < len; i++) sb.append((char) ('a' + rnd.nextInt(3)));
        return sb.toString();
    }
}
```

#### Solution: [Recognize] Autocomplete With Recency Ties (LeetCode 642)
<!-- id: sv-rank-autocomplete -->

**Approach.** A hash map from sentence text to an immutable entry of count, last-use stamp and text is the record that decides. A trie is the derived view. Every node on a sentence's path, including the root, holds a tree set of the entries of all sentences below it. The set orders by higher count, then by larger stamp, then by smaller text. The text makes the order total, so removing an entry never removes a different one.

A commit builds a new entry with the count raised by one and the next stamp. It calls one helper that walks the path, removes the old entry from each node, and inserts the new entry. A retract call builds a lowered entry that keeps the old stamp, or none when the count reaches zero, and calls the same helper. A missing sentence returns `false` before any write. Nodes are never deleted, so the pointer to the current node stays valid.

A type call moves the current-node pointer by one child, and it becomes null when the child is missing. It reads the first three entries of that node's set. A tree set cannot be repaired in place, because the entry fields are the comparator fields. So the code removes the exact old entry before it inserts a new one.

The invariant is that every node's set holds the current entry of every stored sentence below its prefix, and no stale entry.

**Complexity.**

- **Time** is O(L log n) per commit and retract, where L is the sentence length, and O(1) per typed character, since it moves one link and reads three entries.
- **Space** is O(n * L), because each sentence has one entry in each of its at most L + 1 node sets.

```java run
import java.util.*;

public final class AutocompleteSolution {
    static final class Autocomplete {
        private record Entry(int count, int stamp, String text) {}
        private static final Comparator<Entry> ORDER = (a, b) -> {
            if (a.count() != b.count()) return Integer.compare(b.count(), a.count());
            if (a.stamp() != b.stamp()) return Integer.compare(b.stamp(), a.stamp());
            return a.text().compareTo(b.text());
        };
        private static final class Node {
            final Map<Character, Node> next = new HashMap<>();
            final TreeSet<Entry> ranked = new TreeSet<>(ORDER);
        }
        private final Map<String, Entry> byText = new HashMap<>();
        private final Node root = new Node();
        private final StringBuilder typed = new StringBuilder();
        private Node cur = root;
        private int clock;

        /**
         * Replaces the old entry of a sentence by a new one on the whole path.
         * Time: O(L log n).
         * Space: O(L) for new nodes.
         * Invariant: the old entry leaves a node before the new entry enters it.
         */
        private void swap(String text, Entry old, Entry fresh) {
            Node n = root;
            for (int i = 0; i <= text.length(); i++) {
                // The exact old entry is removed first, so the comparator fields never change inside a set.
                if (old != null) n.ranked.remove(old);
                if (fresh != null) n.ranked.add(fresh);
                if (i < text.length()) {
                    final Character ch = text.charAt(i);
                    n = n.next.computeIfAbsent(ch, k -> new Node());
                }
            }
        }

        /** Appends a character or commits the text; O(1) per character, O(L log n) per commit. */
        List<String> type(char c) {
            if (c == '#') {
                String text = typed.toString();
                Entry old = byText.get(text);
                // A commit raises the count and stamps the entry with a fresh clock value.
                Entry fresh = new Entry(old == null ? 1 : old.count() + 1, ++clock, text);
                swap(text, old, fresh);
                byText.put(text, fresh);
                typed.setLength(0);
                cur = root;
                return List.of();
            }
            typed.append(c);
            cur = cur == null ? null : cur.next.get(c);
            List<String> out = new ArrayList<>();
            if (cur != null) for (Entry e : cur.ranked) { if (out.size() == 3) break; out.add(e.text()); }
            return out;
        }

        /** Removes one use of a sentence; O(L log n) time, O(1) extra space. */
        boolean retract(String sentence) {
            Entry old = byText.get(sentence);
            // The precondition is checked before any structure changes.
            if (old == null) return false;
            if (old.count() == 1) {
                swap(sentence, old, null);
                byText.remove(sentence);
            } else {
                Entry fresh = new Entry(old.count() - 1, old.stamp(), sentence);
                swap(sentence, old, fresh);
                byText.put(sentence, fresh);
            }
            return true;
        }
    }

    private static List<String> feed(Autocomplete a, String s) {
        List<String> last = List.of();
        for (char c : s.toCharArray()) last = a.type(c);
        return last;
    }

    public static void main(String[] args) {
        // Example 1 and Example 2 from the problem text.
        Autocomplete a = new Autocomplete();
        feed(a, "go#"); feed(a, "gone#"); feed(a, "go#"); feed(a, "ga#");
        if (!a.type('g').equals(List.of("go", "ga", "gone"))) throw new AssertionError("e1 g");
        if (!a.type('o').equals(List.of("go", "gone"))) throw new AssertionError("e1 o");
        if (!a.type('#').isEmpty()) throw new AssertionError("e1 #");
        Autocomplete b = new Autocomplete();
        feed(b, "ab#"); feed(b, "ab#"); feed(b, "ac#");
        if (!b.retract("ab") || !b.type('a').equals(List.of("ac", "ab"))) throw new AssertionError("e2 first");
        if (!b.retract("ab") || b.retract("zz") || !b.type('c').equals(List.of("ac"))) throw new AssertionError("e2 second");
        // Random streams checked against a sort of all stored sentences.
        Random rnd = new Random(4104);
        String[] pool = {"a", "b", "ab", "ba", "aa", "abb"};
        for (int round = 0; round < 400; round++) {
            Autocomplete s = new Autocomplete();
            Map<String, int[]> ref = new HashMap<>();
            StringBuilder typed = new StringBuilder();
            int clock = 0;
            for (int op = 0; op < 120; op++) {
                int t = rnd.nextInt(5);
                if (t == 0) {
                    String r = pool[rnd.nextInt(pool.length)];
                    int[] e = ref.get(r);
                    boolean want = e != null;
                    if (want && --e[0] == 0) ref.remove(r);
                    if (s.retract(r) != want) throw new AssertionError("retract");
                } else {
                    char c = t == 1 && typed.length() > 0 ? '#' : (char) ('a' + rnd.nextInt(2));
                    List<String> got = s.type(c);
                    List<String> want = new ArrayList<>();
                    if (c == '#') {
                        int[] e = ref.computeIfAbsent(typed.toString(), k -> new int[] {0, 0});
                        e[0]++;
                        e[1] = ++clock;
                        typed.setLength(0);
                    } else {
                        typed.append(c);
                        List<String> hits = new ArrayList<>();
                        for (String k : ref.keySet()) if (k.startsWith(typed.toString())) hits.add(k);
                        hits.sort((x, y) -> {
                            int[] ex = ref.get(x), ey = ref.get(y);
                            if (ex[0] != ey[0]) return Integer.compare(ey[0], ex[0]);
                            if (ex[1] != ey[1]) return Integer.compare(ey[1], ex[1]);
                            return x.compareTo(y);
                        });
                        want = hits.subList(0, Math.min(3, hits.size()));
                    }
                    if (!got.equals(want)) throw new AssertionError("type " + c + " " + got + " " + want);
                }
            }
        }
    }
}
```
