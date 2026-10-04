<!-- solutions-for: 11-trie-and-backtracking -->
### Trie And Backtracking

#### Solution: [Build] Trie-Guided Row Search (Author exercise)
<!-- id: bc-row-search -->

**Approach.** A trie is built from the words with the full word stored at its last node. The walk enters a tile only if the tile is unmarked and the cursor has a child for its letter, emits and clears the stored word at the new node, marks the tile, tries the left and right neighbours and restores the tile. In a row, a route that never reuses a tile can only run in one direction, because a turn would step back onto a marked tile, so a word is found exactly when it is a substring of the row or the reverse of one. The oracle uses that fact and shares no code with the trie. The harness compares the two on random rows and word lists over a three-letter alphabet and checks the examples, including the word read from right to left.

**Complexity.** The walk enters one tile per distinct beginning spelled by a monotone run, so it is bounded by the number of tiles times the longest word, plus building the trie in the total length of the words.

```java run
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Random;
import java.util.TreeSet;

public final class RowSearch {
    static final class Node {
        final Node[] next = new Node[26];
        String word;
    }

    static List<String> hunt(String row, String[] words) {
        Node root = new Node();
        for (String w : words) {
            Node cur = root;
            for (char ch : w.toCharArray()) {
                if (cur.next[ch - 'a'] == null) cur.next[ch - 'a'] = new Node();
                cur = cur.next[ch - 'a'];
            }
            cur.word = w;
        }
        char[] tiles = row.toCharArray();
        List<String> found = new ArrayList<>();
        for (int c = 0; c < tiles.length; c++) walk(tiles, c, root, found);
        Collections.sort(found);
        return found;
    }

    static void walk(char[] t, int c, Node parent, List<String> found) {
        if (c < 0 || c >= t.length) return;
        char saved = t[c];
        if (saved == '#') return;
        Node node = parent.next[saved - 'a'];
        if (node == null) return;
        if (node.word != null) { found.add(node.word); node.word = null; }
        t[c] = '#';
        walk(t, c - 1, node, found);
        walk(t, c + 1, node, found);
        t[c] = saved;
    }

    static List<String> oracle(String row, String[] words) {
        String rev = new StringBuilder(row).reverse().toString();
        TreeSet<String> set = new TreeSet<>();
        for (String w : words) if (row.contains(w) || rev.contains(w)) set.add(w);
        return new ArrayList<>(set);
    }

    public static void main(String[] args) {
        if (!hunt("oath", new String[] {"oat", "oath", "hat"}).equals(List.of("oat", "oath"))) throw new AssertionError("example 1");
        if (!hunt("tao", new String[] {"oat", "tao", "at"}).equals(List.of("at", "oat", "tao"))) throw new AssertionError("example 2");
        if (!hunt("a", new String[0]).isEmpty()) throw new AssertionError("no words");
        Random rnd = new Random(191101);
        for (int t = 0; t < 4000; t++) {
            StringBuilder rb = new StringBuilder();
            int n = 1 + rnd.nextInt(8);
            for (int i = 0; i < n; i++) rb.append((char) ('a' + rnd.nextInt(3)));
            int k = rnd.nextInt(9);
            String[] words = new String[k];
            for (int i = 0; i < k; i++) {
                StringBuilder wb = new StringBuilder();
                int len = 1 + rnd.nextInt(5);
                for (int j = 0; j < len; j++) wb.append((char) ('a' + rnd.nextInt(3)));
                words[i] = wb.toString();
            }
            String row = rb.toString();
            if (!hunt(row, words).equals(oracle(row, words))) throw new AssertionError("differs on " + row);
        }
    }
}
```

#### Solution: [Vary] Stop On Missing Trie Edge (Author exercise)
<!-- id: bc-missing-edge -->

**Approach.** The walk counts a tile entry at the moment the tile is unmarked and the cursor has a matching child, which is just before the tile is marked. Tiles whose letter has no edge are never counted, and neither are tiles already on the route. The result pairs the number of distinct words found with that count. The oracle counts the same quantity without a trie: every route in a row is a run in one direction, so it enumerates each start tile, each direction and each length, counts a single tile once, and counts the run when its spelling is a nonempty beginning of some word. The harness compares both on random inputs and asserts that the entry count is at most the count of a search that ignores the edge test.

**Complexity.** The entry count is the quantity being measured, and it is bounded by the number of tiles times the longest word.

```java run
import java.util.Arrays;
import java.util.Random;
import java.util.TreeSet;

public final class MissingEdge {
    static final class Node {
        final Node[] next = new Node[26];
        String word;
    }

    static long entered;

    static long[] solve(String row, String[] words) {
        Node root = new Node();
        for (String w : words) {
            Node cur = root;
            for (char ch : w.toCharArray()) {
                if (cur.next[ch - 'a'] == null) cur.next[ch - 'a'] = new Node();
                cur = cur.next[ch - 'a'];
            }
            cur.word = w;
        }
        char[] tiles = row.toCharArray();
        entered = 0;
        TreeSet<String> found = new TreeSet<>();
        for (int c = 0; c < tiles.length; c++) walk(tiles, c, root, found);
        return new long[] {found.size(), entered};
    }

    static void walk(char[] t, int c, Node parent, TreeSet<String> found) {
        if (c < 0 || c >= t.length) return;
        char saved = t[c];
        if (saved == '#') return;
        Node node = parent.next[saved - 'a'];
        if (node == null) return;
        entered++;
        if (node.word != null) { found.add(node.word); node.word = null; }
        t[c] = '#';
        walk(t, c - 1, node, found);
        walk(t, c + 1, node, found);
        t[c] = saved;
    }

    static boolean isPrefix(String s, String[] words) {
        for (String w : words) if (w.startsWith(s)) return true;
        return false;
    }

    static long[] oracle(String row, String[] words) {
        int n = row.length();
        long count = 0;
        for (int s = 0; s < n; s++) {
            if (isPrefix(row.substring(s, s + 1), words)) count++;
            for (int len = 2; s + len <= n; len++) {
                if (isPrefix(row.substring(s, s + len), words)) count++;
            }
            for (int len = 2; s - len + 1 >= 0; len++) {
                StringBuilder sb = new StringBuilder();
                for (int i = 0; i < len; i++) sb.append(row.charAt(s - i));
                if (isPrefix(sb.toString(), words)) count++;
            }
        }
        TreeSet<String> found = new TreeSet<>();
        String rev = new StringBuilder(row).reverse().toString();
        for (String w : words) if (row.contains(w) || rev.contains(w)) found.add(w);
        return new long[] {found.size(), count};
    }

    public static void main(String[] args) {
        if (!Arrays.equals(solve("oath", new String[] {"oat", "oath", "hat"}), new long[] {2, 5})) throw new AssertionError("example 1");
        if (!Arrays.equals(solve("xyz", new String[] {"abc"}), new long[] {0, 0})) throw new AssertionError("example 2");
        Random rnd = new Random(191102);
        for (int t = 0; t < 4000; t++) {
            StringBuilder rb = new StringBuilder();
            int n = 1 + rnd.nextInt(8);
            for (int i = 0; i < n; i++) rb.append((char) ('a' + rnd.nextInt(3)));
            int k = rnd.nextInt(9);
            String[] words = new String[k];
            for (int i = 0; i < k; i++) {
                StringBuilder wb = new StringBuilder();
                int len = 1 + rnd.nextInt(5);
                for (int j = 0; j < len; j++) wb.append((char) ('a' + rnd.nextInt(3)));
                words[i] = wb.toString();
            }
            String row = rb.toString();
            long[] a = solve(row, words), b = oracle(row, words);
            if (!Arrays.equals(a, b)) throw new AssertionError("differs on " + row + " " + Arrays.toString(a) + " vs " + Arrays.toString(b));
        }
    }
}
```

#### Solution: [Boundary] Shared Prefix And Duplicate Discovery (Author exercise)
<!-- id: bc-duplicate-discovery -->

**Approach.** The trie stores each distinct word once, so a repeated word in the list simply writes the same field again. Emission adds the word to the answer and sets the field to nothing, while the node stays in place, so a second route that reaches it adds nothing and a longer word that passes through it can still be reached by routes that arrive later. The harness runs two careless variants. One never clears the stored word and asserts that it reports repeats on the first example. The other detaches the node from its parent at emission, and the harness asserts that on the row `yxyz` with the words `xy` and `xyz` it loses `xyz`, because the route that goes left to a dead end emits `xy` first and the route that goes right then finds the edge gone. The oracle tests each distinct word as a substring of the row or its reverse.

**Complexity.** The same as the plain trie walk, plus a constant per emission.

```java run
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Random;
import java.util.TreeSet;

public final class DuplicateDiscovery {
    static final class Node {
        final Node[] next = new Node[26];
        String word;
    }

    static List<String> hunt(String row, String[] words, int mode) {
        Node root = new Node();
        for (String w : words) {
            Node cur = root;
            for (char ch : w.toCharArray()) {
                if (cur.next[ch - 'a'] == null) cur.next[ch - 'a'] = new Node();
                cur = cur.next[ch - 'a'];
            }
            cur.word = w;
        }
        char[] tiles = row.toCharArray();
        List<String> found = new ArrayList<>();
        for (int c = 0; c < tiles.length; c++) walk(tiles, c, root, found, mode);
        Collections.sort(found);
        return found;
    }

    // mode 0: clear the stored word; mode 1: never clear; mode 2: detach the node from its parent
    static void walk(char[] t, int c, Node parent, List<String> found, int mode) {
        if (c < 0 || c >= t.length) return;
        char saved = t[c];
        if (saved == '#') return;
        Node node = parent.next[saved - 'a'];
        if (node == null) return;
        if (node.word != null) {
            found.add(node.word);
            if (mode == 0) node.word = null;
            if (mode == 2) parent.next[saved - 'a'] = null;
        }
        t[c] = '#';
        walk(t, c - 1, node, found, mode);
        walk(t, c + 1, node, found, mode);
        t[c] = saved;
    }

    static List<String> oracle(String row, String[] words) {
        String rev = new StringBuilder(row).reverse().toString();
        TreeSet<String> set = new TreeSet<>();
        for (String w : words) if (row.contains(w) || rev.contains(w)) set.add(w);
        return new ArrayList<>(set);
    }

    public static void main(String[] args) {
        if (!hunt("aaa", new String[] {"aa", "a", "aaa"}, 0).equals(List.of("a", "aa", "aaa"))) throw new AssertionError("example 1");
        if (!hunt("ab", new String[] {"ab", "ba", "ab"}, 0).equals(List.of("ab", "ba"))) throw new AssertionError("example 2");
        if (hunt("aaa", new String[] {"aa", "a", "aaa"}, 1).size() <= 3) throw new AssertionError("never clearing must report repeats");
        List<String> lost = hunt("yxyz", new String[] {"xy", "xyz"}, 2);
        if (lost.contains("xyz")) throw new AssertionError("detaching the node must lose xyz");
        if (!hunt("yxyz", new String[] {"xy", "xyz"}, 0).equals(List.of("xy", "xyz"))) throw new AssertionError("clearing the word keeps xyz");
        Random rnd = new Random(191103);
        for (int t = 0; t < 4000; t++) {
            StringBuilder rb = new StringBuilder();
            int n = 1 + rnd.nextInt(8);
            for (int i = 0; i < n; i++) rb.append((char) ('a' + rnd.nextInt(2)));
            int k = rnd.nextInt(11);
            String[] words = new String[k];
            for (int i = 0; i < k; i++) {
                StringBuilder wb = new StringBuilder();
                int len = 1 + rnd.nextInt(4);
                for (int j = 0; j < len; j++) wb.append((char) ('a' + rnd.nextInt(2)));
                words[i] = wb.toString();
            }
            String row = rb.toString();
            if (!hunt(row, words, 0).equals(oracle(row, words))) throw new AssertionError("differs on " + row);
        }
    }
}
```

#### Solution: [Recognize] Word Search II (LeetCode 212)
<!-- id: bc-word-search-two -->

**Approach.** The trie holds the target words, each at its last node. Every tile is tried as a start. A call returns at once when the tile is out of the board, is marked, or has a letter the cursor has no edge for. Otherwise it emits and clears the node's word, marks the tile with `#`, tries four neighbours with the new cursor, and restores the letter, so the board is unchanged when the hunt ends, which the harness checks. The test for the marker comes before the index into the children, and the harness asserts the arithmetic that makes the order matter: `'#' - 'a'` is negative and indexing with it throws. The oracle runs the single-word search with a fresh flag grid for each word, as in the naive stage, and sorts the words found.

**Complexity.** The walk is bounded by the distinct beginnings that can be spelled on the board, far fewer than one search per word, and the stack is as deep as the longest word.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.Random;
import java.util.TreeSet;

public final class WordSearchTwo {
    static final class Node {
        final Node[] next = new Node[26];
        String word;
    }

    static List<String> hunt(char[][] tiles, String[] targets) {
        Node root = new Node();
        for (String w : targets) {
            Node cur = root;
            for (char ch : w.toCharArray()) {
                if (cur.next[ch - 'a'] == null) cur.next[ch - 'a'] = new Node();
                cur = cur.next[ch - 'a'];
            }
            cur.word = w;
        }
        List<String> found = new ArrayList<>();
        for (int r = 0; r < tiles.length; r++)
            for (int c = 0; c < tiles[0].length; c++)
                walk(tiles, r, c, root, found);
        Collections.sort(found);
        return found;
    }

    static void walk(char[][] t, int r, int c, Node parent, List<String> found) {
        if (r < 0 || c < 0 || r >= t.length || c >= t[0].length) return;
        char saved = t[r][c];
        if (saved == '#') return;
        Node node = parent.next[saved - 'a'];
        if (node == null) return;
        if (node.word != null) { found.add(node.word); node.word = null; }
        t[r][c] = '#';
        walk(t, r + 1, c, node, found);
        walk(t, r - 1, c, node, found);
        walk(t, r, c + 1, node, found);
        walk(t, r, c - 1, node, found);
        t[r][c] = saved;
    }

    static boolean viaCopies(String[] stones, String word) {
        int rows = stones.length, cols = stones[0].length();
        for (int r = 0; r < rows; r++)
            for (int c = 0; c < cols; c++)
                if (spell(stones, word, r, c, 0, new boolean[rows][cols])) return true;
        return false;
    }

    static boolean spell(String[] s, String w, int r, int c, int k, boolean[][] used) {
        if (r < 0 || c < 0 || r >= s.length || c >= s[0].length()) return false;
        if (used[r][c] || s[r].charAt(c) != w.charAt(k)) return false;
        if (k == w.length() - 1) return true;
        boolean[][] next = new boolean[used.length][];
        for (int i = 0; i < used.length; i++) next[i] = used[i].clone();
        next[r][c] = true;
        int[][] d = {{1, 0}, {-1, 0}, {0, 1}, {0, -1}};
        for (int[] x : d) if (spell(s, w, r + x[0], c + x[1], k + 1, next)) return true;
        return false;
    }

    static char[][] grid(String[] rows) {
        char[][] g = new char[rows.length][];
        for (int i = 0; i < rows.length; i++) g[i] = rows[i].toCharArray();
        return g;
    }

    public static void main(String[] args) {
        String[] b1 = {"cat", "oxe", "dgs"};
        List<String> one = hunt(grid(b1), new String[] {"cod", "cat", "tex", "sea", "dog", "xxx"});
        if (!one.equals(List.of("cat", "cod", "tex"))) throw new AssertionError("example 1: " + one);
        if (!hunt(grid(new String[] {"aa"}), new String[] {"aaa", "a"}).equals(List.of("a"))) throw new AssertionError("example 2");
        if (('#' - 'a') >= 0) throw new AssertionError("the marker would give a negative index");
        boolean threw = false;
        try {
            Object[] probe = new Object[26];
            probe['#' - 'a'] = null;
        } catch (ArrayIndexOutOfBoundsException e) {
            threw = true;
        }
        if (!threw) throw new AssertionError("indexing with the marker must throw");
        Random rnd = new Random(191104);
        for (int t = 0; t < 3000; t++) {
            int rows = 1 + rnd.nextInt(4), cols = 1 + rnd.nextInt(4);
            String[] g = new String[rows];
            for (int i = 0; i < rows; i++) {
                StringBuilder sb = new StringBuilder();
                for (int j = 0; j < cols; j++) sb.append((char) ('a' + rnd.nextInt(3)));
                g[i] = sb.toString();
            }
            int k = 1 + rnd.nextInt(8);
            String[] words = new String[k];
            for (int i = 0; i < k; i++) {
                StringBuilder wb = new StringBuilder();
                int len = 1 + rnd.nextInt(6);
                for (int j = 0; j < len; j++) wb.append((char) ('a' + rnd.nextInt(3)));
                words[i] = wb.toString();
            }
            char[][] board = grid(g);
            List<String> got = hunt(board, words);
            if (!Arrays.deepEquals(board, grid(g))) throw new AssertionError("the board must be unchanged");
            TreeSet<String> want = new TreeSet<>();
            for (String w : words) if (viaCopies(g, w)) want.add(w);
            if (!got.equals(new ArrayList<>(want))) throw new AssertionError("differs on " + String.join("|", g) + " " + Arrays.toString(words));
        }
    }
}
```
