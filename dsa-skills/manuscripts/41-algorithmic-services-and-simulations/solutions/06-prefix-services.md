<!-- solutions-for: 06-prefix-services -->
### Solutions For Prefix Services

#### Solution: [Build] Map Sum Pairs (LeetCode 677)
<!-- id: sv-prefix-map-sum -->

**Approach.** A hash map from key to value is the authoritative state. The trie is a derived index in which each node holds the sum of the values of all live keys under its prefix. An insert reads the earlier value from the map, stores the new value and computes the difference between them. It then walks the key once and adds that difference to every node on the path, creating missing nodes on the way.

A sum call walks the prefix and returns the number on the last node, or 0 when a child is missing. The invariant is that every node equals the sum of the map values of the keys under its prefix. An overwrite keeps that equality because the node already contains the old value, and only the difference is added.

**Complexity.**

- **Time** is O(p) for an insert or a sum with a key or prefix of length p, because each call visits one node per character.
- **Space** is O(L) for the trie, where L is the total length of the distinct keys, plus O(n) for the map.

```java run
import java.util.*;

public final class MapSumSolution {
    static final class MapSum {
        private static final class Node {
            final Node[] next = new Node[26];
            long sum;
        }
        private final Node root = new Node();
        private final Map<String, Integer> value = new HashMap<>();   // authoritative key -> value

        /**
         * Stores a value and returns the earlier one, or -1 for a new key.
         * Time: O(p).
         * Space: O(p) for new nodes.
         * Invariant: each node sum equals the map values under its prefix.
         */
        int insert(String key, int val) {
            Integer old = value.put(key, val);
            // Only the difference reaches the nodes, because they already hold the old value.
            long delta = (long) val - (old == null ? 0 : old);
            Node cur = root;
            for (int i = 0; i < key.length(); i++) {
                int c = key.charAt(i) - 'a';
                // Create the child on first use so the path exists for the whole key.
                if (cur.next[c] == null) cur.next[c] = new Node();
                cur = cur.next[c];
                cur.sum += delta;
            }
            return old == null ? -1 : old;
        }

        /**
         * Returns the sum of values of keys under the prefix.
         * Time: O(p).
         * Space: O(1).
         * Invariant: a missing child means no live key has this prefix.
         */
        long sum(String prefix) {
            Node cur = root;
            // Follow the prefix and stop early when no key continues that way.
            for (int i = 0; i < prefix.length(); i++) {
                cur = cur.next[prefix.charAt(i) - 'a'];
                if (cur == null) return 0;
            }
            return cur.sum;
        }
    }

    public static void main(String[] args) {
        // Example 1 and Example 2 from the problem text.
        MapSum m = new MapSum();
        if (m.insert("apple", 3) != -1 || m.insert("app", 2) != -1) throw new AssertionError("e1 insert");
        if (m.sum("ap") != 5) throw new AssertionError("e1 sum");
        MapSum n = new MapSum();
        if (n.insert("apple", 3) != -1 || n.insert("apple", 5) != 3 || n.insert("app", 2) != -1) throw new AssertionError("e2 insert");
        if (n.sum("app") != 7) throw new AssertionError("e2 sum");
        // Random calls checked against a full scan of a reference map.
        Random rnd = new Random(677);
        for (int round = 0; round < 300; round++) {
            MapSum s = new MapSum();
            Map<String, Integer> ref = new HashMap<>();
            for (int op = 0; op < 80; op++) {
                String w = word(rnd, 1 + rnd.nextInt(4));
                if (rnd.nextBoolean()) {
                    int v = 1 + rnd.nextInt(1000);
                    Integer old = ref.put(w, v);
                    if (s.insert(w, v) != (old == null ? -1 : old)) throw new AssertionError("returned old value");
                } else {
                    long want = 0;
                    for (Map.Entry<String, Integer> e : ref.entrySet()) if (e.getKey().startsWith(w)) want += e.getValue();
                    if (s.sum(w) != want) throw new AssertionError("sum " + w);
                }
            }
        }
    }

    static String word(Random rnd, int len) {
        StringBuilder b = new StringBuilder();
        for (int i = 0; i < len; i++) b.append((char) ('a' + rnd.nextInt(3)));
        return b.toString();
    }
}
```

#### Solution: [Vary] Implement Magic Dictionary (LeetCode 676)
<!-- id: sv-prefix-magic-dictionary -->

**Approach.** The build call creates a fresh root, so a later build discards the earlier dictionary. Each stored word marks its last node as the end of a word. A search is a depth-first walk that carries the node, the index in the query and a flag that tells whether the one change is already used.

At each index the walk always follows the child that matches the query letter. While the flag is unset, it also tries each other child and sets the flag on that branch. At the end of the query the walk accepts only a node that ends a word and only when the flag is set, so an exact match without a change is rejected. The invariant is that a walk with the flag set has followed the query on every index except one.

**Complexity.**

- **Time** is O(26 * L * L) per search for a query of length L, because each of the L positions may branch to 25 children and each branch then follows at most L letters.
- **Space** is O(T) for the trie over T total dictionary letters, plus O(L) for the recursion.

```java run
import java.util.*;

public final class MagicDictionarySolution {
    static final class MagicDictionary {
        private static final class Node {
            final Node[] next = new Node[26];
            boolean end;
        }
        private Node root = new Node();

        /** Replaces the dictionary; Time O(total letters); Space O(total letters); invariant: only the new words are stored. */
        void buildDict(String[] words) {
            root = new Node();
            for (String w : words) {
                Node cur = root;
                for (int i = 0; i < w.length(); i++) {
                    int c = w.charAt(i) - 'a';
                    if (cur.next[c] == null) cur.next[c] = new Node();
                    cur = cur.next[c];
                }
                cur.end = true;
            }
        }

        boolean search(String word) { return dfs(root, word, 0, false); }

        /**
         * Walks the query and may leave it once.
         * Time: O(26 * L * L).
         * Space: O(L) recursion.
         * Invariant: when used is true, exactly one earlier index differed from the query.
         */
        private boolean dfs(Node node, String w, int i, boolean used) {
            // At the end the word must exist and the one change must have happened.
            if (i == w.length()) return used && node.end;
            int want = w.charAt(i) - 'a';
            for (int c = 0; c < 26; c++) {
                Node nx = node.next[c];
                if (nx == null) continue;
                // The matching child keeps the flag as it is.
                if (c == want) { if (dfs(nx, w, i + 1, used)) return true; }
                // A different child spends the one allowed change.
                else if (!used && dfs(nx, w, i + 1, true)) return true;
            }
            return false;
        }
    }

    public static void main(String[] args) {
        // Example 1 and Example 2 from the problem text.
        MagicDictionary d = new MagicDictionary();
        d.buildDict(new String[] {"hello", "leetcode"});
        if (d.search("hello") || !d.search("hhllo") || d.search("hell")) throw new AssertionError("e1");
        d.buildDict(new String[] {"abc", "abd"});
        if (!d.search("abc") || d.search("xyz")) throw new AssertionError("e2 first");
        d.buildDict(new String[] {"zzz"});
        if (d.search("abc")) throw new AssertionError("e2 rebuild");
        // Random dictionaries checked against a pairwise count of differing positions.
        Random rnd = new Random(676);
        for (int round = 0; round < 400; round++) {
            String[] words = new String[rnd.nextInt(7)];
            for (int i = 0; i < words.length; i++) words[i] = word(rnd, 1 + rnd.nextInt(4));
            MagicDictionary m = new MagicDictionary();
            m.buildDict(words);
            for (int q = 0; q < 30; q++) {
                String w = word(rnd, 1 + rnd.nextInt(4));
                boolean want = false;
                for (String x : words) {
                    if (x.length() != w.length()) continue;
                    int diff = 0;
                    for (int i = 0; i < w.length(); i++) if (x.charAt(i) != w.charAt(i)) diff++;
                    if (diff == 1) want = true;
                }
                if (m.search(w) != want) throw new AssertionError("search " + w + " in " + Arrays.toString(words));
            }
        }
    }

    static String word(Random rnd, int len) {
        StringBuilder b = new StringBuilder();
        for (int i = 0; i < len; i++) b.append((char) ('a' + rnd.nextInt(3)));
        return b.toString();
    }
}
```

#### Solution: [Boundary] Implement Trie II (LeetCode 1804)
<!-- id: sv-prefix-trie-counts -->

**Approach.** Every node stores a pass count, which is the number of stored copies that go through it, and an end count, which is the number of copies that end there. Insert raises the pass count on each node of the path and raises the end count on the last node. A count call walks the string and reads one of the two numbers.

Erase is a multi-field change, so it validates first. It walks the word and returns `false` when a node is missing or when the end count on the last node is 0. A word that is only a prefix of other words therefore cannot be erased. After that check, a second walk lowers every pass count on the path and the end count on the last node. When a pass count reaches 0 the parent drops the whole child, because no copy lives below it. The invariant is that a pass count equals the end counts in its subtree, and no node with a pass count of 0 stays linked.

**Complexity.**

- **Time** is O(p) for each call with a string of length p, because validation and update are two walks of the same path.
- **Space** is O(L) for the nodes of the live words, since erase frees nodes with a pass count of 0.

```java run
import java.util.*;

public final class TrieCountsSolution {
    static final class TrieCounts {
        private static final class Node {
            final Node[] next = new Node[26];
            int pass, end;
        }
        private final Node root = new Node();

        /** Adds one copy; Time O(p); Space O(p); invariant: pass counts rise on the whole path together. */
        void insert(String word) {
            Node cur = root;
            for (int i = 0; i < word.length(); i++) {
                int c = word.charAt(i) - 'a';
                if (cur.next[c] == null) cur.next[c] = new Node();
                cur = cur.next[c];
                cur.pass++;
            }
            cur.end++;
        }

        // Walks to the node of a string, or returns null when no stored word continues that way; O(p) time, O(1) space.
        private Node find(String s) {
            Node cur = root;
            for (int i = 0; i < s.length() && cur != null; i++) cur = cur.next[s.charAt(i) - 'a'];
            return cur;
        }

        int countEqual(String word) { Node n = find(word); return n == null ? 0 : n.end; }

        int countPrefix(String prefix) { Node n = find(prefix); return n == null ? 0 : n.pass; }

        /**
         * Removes one copy, or changes nothing.
         * Time: O(p).
         * Space: O(1).
         * Invariant: validation finishes before the first count changes.
         */
        boolean erase(String word) {
            // Validate on the read-only walk, because a prefix without an end count is not a word.
            if (countEqual(word) == 0) return false;
            Node parent = root;
            for (int i = 0; i < word.length(); i++) {
                int c = word.charAt(i) - 'a';
                Node child = parent.next[c];
                // The pass count drops once for each node on the path.
                if (--child.pass == 0) { parent.next[c] = null; return true; }
                parent = child;
            }
            // The end count drops on the last node when it stays linked.
            parent.end--;
            return true;
        }
    }

    public static void main(String[] args) {
        // Example 1 and Example 2 from the problem text.
        TrieCounts t = new TrieCounts();
        t.insert("apple"); t.insert("apple"); t.insert("app");
        if (t.countEqual("apple") != 2 || t.countPrefix("app") != 3) throw new AssertionError("e1 counts");
        if (!t.erase("apple") || t.countPrefix("app") != 2) throw new AssertionError("e1 erase");
        TrieCounts u = new TrieCounts();
        u.insert("cat");
        if (u.erase("car") || u.erase("ca") || u.countPrefix("ca") != 1) throw new AssertionError("e2 failed erases");
        if (!u.erase("cat") || u.erase("cat") || u.countPrefix("c") != 0) throw new AssertionError("e2 last");
        // Random calls checked against a multiset and a scan for prefixes.
        Random rnd = new Random(1804);
        for (int round = 0; round < 300; round++) {
            TrieCounts s = new TrieCounts();
            Map<String, Integer> ref = new HashMap<>();
            for (int op = 0; op < 100; op++) {
                String w = word(rnd, 1 + rnd.nextInt(4));
                switch (rnd.nextInt(4)) {
                    case 0 -> { s.insert(w); ref.merge(w, 1, Integer::sum); }
                    case 1 -> {
                        boolean want = ref.getOrDefault(w, 0) > 0;
                        if (s.erase(w) != want) throw new AssertionError("erase result " + w);
                        if (want) ref.merge(w, -1, Integer::sum);
                    }
                    case 2 -> { if (s.countEqual(w) != ref.getOrDefault(w, 0)) throw new AssertionError("equal " + w); }
                    default -> {
                        int want = 0;
                        for (Map.Entry<String, Integer> e : ref.entrySet()) if (e.getKey().startsWith(w)) want += e.getValue();
                        if (s.countPrefix(w) != want) throw new AssertionError("prefix " + w);
                    }
                }
            }
        }
    }

    static String word(Random rnd, int len) {
        StringBuilder b = new StringBuilder();
        for (int i = 0; i < len; i++) b.append((char) ('a' + rnd.nextInt(3)));
        return b.toString();
    }
}
```

#### Solution: [Recognize] Design Search Autocomplete System (LeetCode 642)
<!-- id: sv-prefix-autocomplete -->

**Approach.** A hash map from sentence to count is the authoritative state. Each trie node keeps only the set of sentences that pass through it, which is derived state. A sentence enters the sets once, when it first appears, and later count changes touch only the map. The typed text lives in a string builder, and a cursor holds the current node, or null when no stored sentence starts with the typed text.

A letter or space extends the typed text and moves the cursor one edge. While the cursor is null it stays null, so every further character returns an empty list until the next `#`. Otherwise the call copies the node's set, sorts it by the count read from the map and then by `compareTo`, and returns the first three. A `#` adds one to the count of the typed text, links a new sentence into the trie when needed, clears the typed text and resets the cursor. The sort comparator reads counts from the map and never from objects inside the sets, so no key of an ordered structure changes in place.

The review note is that the sort costs O(m log m) for m matching sentences. A cache of the best three sentences on each node would give O(p) per character, but it needs an update on every count change along the path. The transfer prompt asks only for the correct order, and the simpler sort is enough here.

**Complexity.**

- **Time** is O(m log m) per character for m sentences under the typed text, and O(p) per `#` for a sentence of length p.
- **Space** is O(L) for the nodes and sets, where L is the total length of the distinct sentences, plus the length of the typed text.

```java run
import java.util.*;

public final class AutocompleteSolution {
    static final class Autocomplete {
        private static final class Node {
            final Map<Character, Node> next = new HashMap<>();
            final Set<String> through = new HashSet<>();     // derived: sentences under this prefix
        }
        private final Node root = new Node();
        private final Map<String, Integer> count = new HashMap<>();   // authoritative sentence -> count
        private final StringBuilder typed = new StringBuilder();
        private Node cur = root;                              // null once the typed text matches nothing

        Autocomplete(String[] sentences, int[] times) {
            for (int i = 0; i < sentences.length; i++) add(sentences[i], times[i]);
        }

        // Adds to the count and links a sentence into the trie on its first appearance; O(p) time, O(p) space.
        private void add(String s, int times) {
            boolean fresh = !count.containsKey(s);
            count.merge(s, times, Integer::sum);
            if (!fresh) return;
            Node n = root;
            for (int i = 0; i < s.length(); i++) {
                n = n.next.computeIfAbsent(s.charAt(i), k -> new Node());
                n.through.add(s);
            }
        }

        /**
         * Handles one typed character.
         * Time: O(m log m) for a letter, O(p) for the end mark.
         * Space: O(m).
         * Invariant: the cursor is the node of the typed text, or null when no sentence matches.
         */
        List<String> input(char c) {
            if (c == '#') {
                // An empty typed text changes nothing, otherwise the text becomes one more use.
                if (typed.length() > 0) add(typed.toString(), 1);
                typed.setLength(0);
                cur = root;
                return List.of();
            }
            typed.append(c);
            // A null cursor stays null, so a dead prefix cannot match again.
            if (cur != null) cur = cur.next.get(c);
            if (cur == null) return List.of();
            List<String> cand = new ArrayList<>(cur.through);
            // Counts come from the map at sort time, so the order is never stale.
            cand.sort((a, b) -> {
                int byCount = Integer.compare(count.get(b), count.get(a));
                return byCount != 0 ? byCount : a.compareTo(b);
            });
            return new ArrayList<>(cand.subList(0, Math.min(3, cand.size())));
        }
    }

    public static void main(String[] args) {
        // Example 1 and Example 2 from the problem text.
        String[] start = {"i love you", "island", "iroman", "i love leetcode"};
        int[] times = {5, 3, 2, 2};
        Autocomplete a = new Autocomplete(start, times);
        if (!a.input('i').equals(List.of("i love you", "island", "i love leetcode"))) throw new AssertionError("e1 i");
        if (!a.input(' ').equals(List.of("i love you", "i love leetcode"))) throw new AssertionError("e1 space");
        if (!a.input('a').isEmpty() || !a.input('#').isEmpty()) throw new AssertionError("e1 end");
        a.input('i');
        if (!a.input(' ').equals(List.of("i love you", "i love leetcode", "i a"))) throw new AssertionError("e2 last");
        // Random calls checked against a full scan with the same sort rule.
        Random rnd = new Random(642);
        char[] alpha = {'a', 'b', ' '};
        for (int round = 0; round < 300; round++) {
            int k = rnd.nextInt(5);
            String[] ss = new String[k];
            int[] tt = new int[k];
            Map<String, Integer> ref = new HashMap<>();
            for (int i = 0; i < k; i++) {
                ss[i] = text(rnd, alpha, 1 + rnd.nextInt(4));
                tt[i] = 1 + rnd.nextInt(4);
                ref.merge(ss[i], tt[i], Integer::sum);
            }
            Autocomplete s = new Autocomplete(ss, tt);
            StringBuilder typed = new StringBuilder();
            for (int op = 0; op < 60; op++) {
                char c = rnd.nextInt(5) == 0 ? '#' : alpha[rnd.nextInt(3)];
                List<String> got = s.input(c);
                if (c == '#') {
                    if (typed.length() > 0) ref.merge(typed.toString(), 1, Integer::sum);
                    typed.setLength(0);
                    if (!got.isEmpty()) throw new AssertionError("end mark returns empty");
                    continue;
                }
                typed.append(c);
                List<String> want = new ArrayList<>();
                for (String x : ref.keySet()) if (x.startsWith(typed.toString())) want.add(x);
                want.sort((x, y) -> ref.get(x).equals(ref.get(y)) ? x.compareTo(y) : ref.get(y) - ref.get(x));
                if (want.size() > 3) want = new ArrayList<>(want.subList(0, 3));
                if (!got.equals(want)) throw new AssertionError("typed [" + typed + "] got " + got + " want " + want);
            }
        }
    }

    static String text(Random rnd, char[] alpha, int len) {
        StringBuilder b = new StringBuilder();
        for (int i = 0; i < len; i++) b.append(alpha[rnd.nextInt(3)]);
        return b.toString();
    }
}
```
