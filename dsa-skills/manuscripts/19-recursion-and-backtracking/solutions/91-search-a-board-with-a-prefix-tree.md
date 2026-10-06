<!-- solutions-for: 91-search-a-board-with-a-prefix-tree -->
### Solutions For Searching With A Prefix Tree

#### Solution: [Build] Trie-Guided Row Search (Author exercise)
<!-- id: bt-trie-row-search -->

**Approach.**
The method builds a prefix tree in which the node of each word stores the word. A call at cell `i` rejects a cell outside the row or with a mark. It moves the node to the child for the letter of the cell and returns when the child is missing. When the new node stores a word, the call adds the word to the result. Then it sets the mark, calls itself for the left neighbour and then for the right neighbour, and clears the mark. The tree keeps its words, so every path that spells a word reports it, and a path of one letter reports a word of one letter. The node always spells the letters of the marked cells in path order.

**Complexity.**
- **Time** is O(T + n * L) for a tree of `T` letters, a row of `n` cells and words of up to `L` letters. A path on a row extends one way, and the node ends it after at most `L` letters.
- **Space** is O(T) for the tree plus O(n) for the marks and the stack.

```java run
import java.util.*;

public final class TrieRowSearch {
    private static final class Node { final Node[] next = new Node[26]; String word; }

    /**
     * Returns the word of each path on the row that spells a dictionary word, start cells from left to right.
     * Time: O(T + n * L). Space: O(T + n).
     * Invariant: the node spells the letters of the marked cells, in path order.
     */
    static List<String> search(String row, String[] words) {
        Node root = new Node();
        for (String w : words) {
            Node cur = root;
            for (int i = 0; i < w.length(); i++) {
                int s = w.charAt(i) - 'a';
                if (cur.next[s] == null) cur.next[s] = new Node();
                cur = cur.next[s];
            }
            cur.word = w;                                    // the node of a word stores the word
        }
        List<String> out = new ArrayList<>();
        boolean[] on = new boolean[row.length()];
        for (int i = 0; i < row.length(); i++) go(row, i, root, on, out);
        return out;
    }

    private static void go(String row, int i, Node parent, boolean[] on, List<String> out) {
        if (i < 0 || i >= row.length() || on[i]) return;     // outside the row or already on the path
        Node node = parent.next[row.charAt(i) - 'a'];        // move the node by the letter of this cell
        if (node == null) return;                            // missing edge: no word has this prefix
        if (node.word != null) out.add(node.word);           // the path spells a dictionary word
        on[i] = true;                                        // choose: mark the cell
        go(row, i - 1, node, on, out);                       // the left neighbour first
        go(row, i + 1, node, on, out);                       // then the right neighbour
        on[i] = false;                                       // undo: clear the mark
    }

    /** Oracle: for each start, list the one-letter path, then the left chain, then the right chain, and test each string. */
    static List<String> oracle(String row, String[] words) {
        Set<String> dict = new HashSet<>(Arrays.asList(words));
        List<String> out = new ArrayList<>();
        int n = row.length();
        for (int s = 0; s < n; s++) {
            if (dict.contains(row.substring(s, s + 1))) out.add(row.substring(s, s + 1));
            StringBuilder left = new StringBuilder().append(row.charAt(s));
            for (int i = s - 1; i >= 0; i--) { left.append(row.charAt(i)); if (dict.contains(left.toString())) out.add(left.toString()); }
            StringBuilder right = new StringBuilder().append(row.charAt(s));
            for (int i = s + 1; i < n; i++) { right.append(row.charAt(i)); if (dict.contains(right.toString())) out.add(right.toString()); }
        }
        return out;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!search("aba", new String[] {"ab", "aba"}).equals(List.of("ab", "aba", "ab", "aba"))) throw new AssertionError("ex1");
        if (!search("x", new String[] {"x"}).equals(List.of("x"))) throw new AssertionError("ex2");
        if (!search("ab", new String[] {}).isEmpty()) throw new AssertionError("empty dictionary");
        // Random rows and dictionaries must match the oracle, including repeated words.
        Random rnd = new Random(2011);
        for (int t = 0; t < 500; t++) {
            StringBuilder sb = new StringBuilder();
            for (int i = 0, n = 1 + rnd.nextInt(8); i < n; i++) sb.append((char) ('a' + rnd.nextInt(2)));
            String[] w = new String[rnd.nextInt(8)];
            for (int i = 0; i < w.length; i++) { StringBuilder x = new StringBuilder(); for (int j = 0, m = 1 + rnd.nextInt(4); j < m; j++) x.append((char) ('a' + rnd.nextInt(2))); w[i] = x.toString(); }
            if (!search(sb.toString(), w).equals(oracle(sb.toString(), w))) throw new AssertionError("random " + t);
        }
        System.out.println("ok");
    }
}
```

#### Solution: [Vary] Stop On Missing Trie Edge (Author exercise)
<!-- id: bt-stop-on-missing-edge -->

**Approach.**
The method builds the prefix tree and starts a call at every cell. A call returns when the cell is outside the board, carries a mark or has no tree child for its letter. The missing child is the pruning test, and it runs before the call sets any mark. When the new node stores a word, the call stores the result in a local variable and still clears nothing, because it has set no mark yet. Otherwise it sets the mark, tries the four neighbours with `||`, clears the mark and returns the stored result. A success returns up through the calls, and each call clears its own mark on the way. The board is read only, so it keeps its letters.

**Complexity.**
- **Time** is O(T + R * C * 3^L), where `T` is the number of letters in the dictionary and `L` is the longest word.
- **Space** is O(T + R * C) for the tree and the marks, plus O(L) for the stack.

```java run
import java.util.*;

public final class StopOnMissingEdge {
    private static final class Node { final Node[] next = new Node[26]; boolean end; }

    /**
     * Returns true when at least one word appears on the board.
     * Time: O(T + R * C * 3^L). Space: O(T + R * C).
     * Invariant: the node spells the marked cells in path order, and each call clears the mark that it set.
     */
    static boolean any(String[] board, String[] words) {
        Node root = new Node();
        for (String w : words) {
            Node cur = root;
            for (int i = 0; i < w.length(); i++) {
                int s = w.charAt(i) - 'a';
                if (cur.next[s] == null) cur.next[s] = new Node();
                cur = cur.next[s];
            }
            cur.end = true;
        }
        boolean[][] on = new boolean[board.length][board[0].length()];
        for (int r = 0; r < board.length; r++)
            for (int c = 0; c < board[0].length(); c++)
                if (go(board, r, c, root, on)) return true;
        return false;
    }

    private static boolean go(String[] b, int r, int c, Node parent, boolean[][] on) {
        if (r < 0 || c < 0 || r >= b.length || c >= b[0].length() || on[r][c]) return false;   // outside or in use
        Node node = parent.next[b[r].charAt(c) - 'a'];
        if (node == null) return false;                      // missing edge: stop before any mark
        if (node.end) return true;                           // a word is spelled: nothing was marked in this call
        on[r][c] = true;                                     // choose: mark the cell
        boolean found = go(b, r - 1, c, node, on) || go(b, r + 1, c, node, on)
                     || go(b, r, c - 1, node, on) || go(b, r, c + 1, node, on);
        on[r][c] = false;                                    // undo: clear the mark before the return
        return found;
    }

    /** Oracle: one independent search per word with a letter index. */
    static boolean oracle(String[] board, String[] words) {
        for (String w : words) {
            boolean[][] on = new boolean[board.length][board[0].length()];
            for (int r = 0; r < board.length; r++) for (int c = 0; c < board[0].length(); c++) if (single(board, w, r, c, 0, on)) return true;
        }
        return false;
    }

    private static boolean single(String[] b, String w, int r, int c, int k, boolean[][] on) {
        if (r < 0 || c < 0 || r >= b.length || c >= b[0].length() || on[r][c] || b[r].charAt(c) != w.charAt(k)) return false;
        if (k == w.length() - 1) return true;
        on[r][c] = true;
        boolean f = single(b, w, r - 1, c, k + 1, on) || single(b, w, r + 1, c, k + 1, on) || single(b, w, r, c - 1, k + 1, on) || single(b, w, r, c + 1, k + 1, on);
        on[r][c] = false;
        return f;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        String[] board = {"ab", "cd"};
        if (!any(board, new String[] {"abdc", "zz"})) throw new AssertionError("ex1");
        if (any(board, new String[] {"zz", "abcd"})) throw new AssertionError("ex2");
        if (any(board, new String[] {})) throw new AssertionError("empty dictionary");
        // Random boards and dictionaries must match the independent word searches.
        Random rnd = new Random(2012);
        for (int t = 0; t < 500; t++) {
            int R = 1 + rnd.nextInt(3), C = 1 + rnd.nextInt(3);
            String[] b = new String[R];
            for (int i = 0; i < R; i++) { StringBuilder sb = new StringBuilder(); for (int j = 0; j < C; j++) sb.append((char) ('a' + rnd.nextInt(2))); b[i] = sb.toString(); }
            String[] w = new String[rnd.nextInt(6)];
            for (int i = 0; i < w.length; i++) { StringBuilder x = new StringBuilder(); for (int j = 0, m = 1 + rnd.nextInt(5); j < m; j++) x.append((char) ('a' + rnd.nextInt(2))); w[i] = x.toString(); }
            if (any(b, w) != oracle(b, w)) throw new AssertionError("random " + t);
        }
        System.out.println("ok");
    }
}
```

#### Solution: [Boundary] Shared Prefix And Duplicate Discovery (Author exercise)
<!-- id: bt-shared-prefix-duplicates -->

**Approach.**
The method uses the row search of the first exercise and adds the emit-once rule. When a path reaches a node that stores a word, the call adds the word to the result and sets the stored word to `null`. A later path that reaches the same node finds `null` and reports nothing, so each word appears once, even when `words` lists it several times. The call then continues below the node, because the word may be the prefix of a longer word such as `ab` inside `aba`. The tree keeps all its nodes, so clearing the slot changes only what the search reports and not where it goes. The result keeps the order of the first reports.

**Complexity.**
- **Time** is O(T + n * L) for a tree of `T` letters and a row of `n` cells.
- **Space** is O(T + n) for the tree, the marks and the stack.

```java run
import java.util.*;

public final class SharedPrefixDuplicates {
    private static final class Node { final Node[] next = new Node[26]; String word; }

    /**
     * Returns each dictionary word that a path on the row spells, once, in the order of the first report.
     * Time: O(T + n * L). Space: O(T + n).
     * Invariant: a node reports its word at most once, and the search continues below every node.
     */
    static List<String> unique(String row, String[] words) {
        Node root = new Node();
        for (String w : words) {
            Node cur = root;
            for (int i = 0; i < w.length(); i++) {
                int s = w.charAt(i) - 'a';
                if (cur.next[s] == null) cur.next[s] = new Node();
                cur = cur.next[s];
            }
            cur.word = w;
        }
        List<String> out = new ArrayList<>();
        boolean[] on = new boolean[row.length()];
        for (int i = 0; i < row.length(); i++) go(row, i, root, on, out);
        return out;
    }

    private static void go(String row, int i, Node parent, boolean[] on, List<String> out) {
        if (i < 0 || i >= row.length() || on[i]) return;
        Node node = parent.next[row.charAt(i) - 'a'];
        if (node == null) return;                            // missing edge: no word has this prefix
        if (node.word != null) { out.add(node.word); node.word = null; }   // emit once: clear the slot after the report
        on[i] = true;                                        // choose: mark the cell
        go(row, i - 1, node, on, out);
        go(row, i + 1, node, on, out);                       // the search continues below a node that ended a word
        on[i] = false;                                       // undo: clear the mark
    }

    /** Oracle: every contiguous or reversed contiguous slice of the row, tested against a set, in first-report order. */
    static List<String> oracle(String row, String[] words) {
        Set<String> dict = new HashSet<>(Arrays.asList(words));
        LinkedHashSet<String> out = new LinkedHashSet<>();
        int n = row.length();
        for (int s = 0; s < n; s++) {
            if (dict.contains(row.substring(s, s + 1))) out.add(row.substring(s, s + 1));
            StringBuilder left = new StringBuilder().append(row.charAt(s));
            for (int i = s - 1; i >= 0; i--) { left.append(row.charAt(i)); if (dict.contains(left.toString())) out.add(left.toString()); }
            StringBuilder right = new StringBuilder().append(row.charAt(s));
            for (int i = s + 1; i < n; i++) { right.append(row.charAt(i)); if (dict.contains(right.toString())) out.add(right.toString()); }
        }
        return new ArrayList<>(out);
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!unique("aba", new String[] {"ab", "aba", "ab"}).equals(List.of("ab", "aba"))) throw new AssertionError("ex1");
        if (!unique("ab", new String[] {"ba"}).equals(List.of("ba"))) throw new AssertionError("ex2");
        // A word that is a prefix of another word must not stop the search below its node.
        if (!unique("abab", new String[] {"a", "ab", "abab"}).containsAll(List.of("a", "ab", "abab"))) throw new AssertionError("prefix words");
        // Random inputs must match the oracle in order.
        Random rnd = new Random(2013);
        for (int t = 0; t < 500; t++) {
            StringBuilder sb = new StringBuilder();
            for (int i = 0, n = 1 + rnd.nextInt(8); i < n; i++) sb.append((char) ('a' + rnd.nextInt(2)));
            String[] w = new String[rnd.nextInt(8)];
            for (int i = 0; i < w.length; i++) { StringBuilder x = new StringBuilder(); for (int j = 0, m = 1 + rnd.nextInt(4); j < m; j++) x.append((char) ('a' + rnd.nextInt(2))); w[i] = x.toString(); }
            if (!unique(sb.toString(), w).equals(oracle(sb.toString(), w))) throw new AssertionError("random " + t);
        }
        System.out.println("ok");
    }
}
```

#### Solution: [Recognize] Word Search II (LeetCode 212)
<!-- id: bt-word-search-two -->

**Approach.**
The method builds the prefix tree once and searches from every cell. A call returns when its cell lies outside the board, carries a mark or has no tree child for its letter. A node that stores a word reports it and clears the slot, so a word that several paths spell appears once. The call sets the mark, explores the four neighbours with the child node and clears the mark. The tree node and the marks return to their earlier state on exit, because the node is an argument and the call clears its own mark. The method sorts the result at the end, because the order of discovery depends on the search.

**Complexity.**
- **Time** is O(T + R * C * 3^L + k log k) for `k` found words, because the search never enters a call below a missing edge.
- **Space** is O(T + R * C) for the tree and the marks, plus O(L) for the stack.

```java run
import java.util.*;

public final class WordSearchTwo {
    private static final class Node { final Node[] next = new Node[26]; String word; }
    private static long trieCalls, baseCalls;

    /**
     * Returns every dictionary word that a path on the board spells, each once, sorted.
     * Time: O(T + R * C * 3^L + k log k). Space: O(T + R * C).
     * Invariant: the node spells the marked cells in path order, and both return to their entry state on exit.
     */
    static List<String> find(String[] board, String[] words) {
        Node root = new Node();
        for (String w : words) {
            Node cur = root;
            for (int i = 0; i < w.length(); i++) {
                int s = w.charAt(i) - 'a';
                if (cur.next[s] == null) cur.next[s] = new Node();
                cur = cur.next[s];
            }
            cur.word = w;
        }
        List<String> out = new ArrayList<>();
        boolean[][] on = new boolean[board.length][board[0].length()];
        for (int r = 0; r < board.length; r++)
            for (int c = 0; c < board[0].length(); c++) go(board, r, c, root, on, out);
        Collections.sort(out);
        return out;
    }

    private static void go(String[] b, int r, int c, Node parent, boolean[][] on, List<String> out) {
        trieCalls++;
        if (r < 0 || c < 0 || r >= b.length || c >= b[0].length() || on[r][c]) return;   // outside or in use
        Node node = parent.next[b[r].charAt(c) - 'a'];
        if (node == null) return;                            // missing edge: no word has this prefix
        if (node.word != null) { out.add(node.word); node.word = null; }   // emit once
        on[r][c] = true;                                     // choose: mark the cell
        go(b, r - 1, c, node, on, out); go(b, r + 1, c, node, on, out);
        go(b, r, c - 1, node, on, out); go(b, r, c + 1, node, on, out);
        on[r][c] = false;                                    // undo: clear the mark
    }

    /** Oracle: one independent letter-index search per word, deduplicated and sorted. */
    static List<String> oracle(String[] board, String[] words) {
        TreeSet<String> out = new TreeSet<>();
        for (String w : words) {
            boolean[][] on = new boolean[board.length][board[0].length()];
            for (int r = 0; r < board.length; r++) for (int c = 0; c < board[0].length(); c++) if (single(board, w, r, c, 0, on)) out.add(w);
        }
        return new ArrayList<>(out);
    }

    private static boolean single(String[] b, String w, int r, int c, int k, boolean[][] on) {
        baseCalls++;
        if (r < 0 || c < 0 || r >= b.length || c >= b[0].length() || on[r][c] || b[r].charAt(c) != w.charAt(k)) return false;
        if (k == w.length() - 1) return true;
        on[r][c] = true;
        boolean f = single(b, w, r - 1, c, k + 1, on) || single(b, w, r + 1, c, k + 1, on) || single(b, w, r, c - 1, k + 1, on) || single(b, w, r, c + 1, k + 1, on);
        on[r][c] = false;
        return f;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        String[] board = {"ab", "cd"};
        if (!find(board, new String[] {"abdc", "acd", "bad", "ca"}).equals(List.of("abdc", "acd", "ca"))) throw new AssertionError("ex1");
        if (!find(board, new String[] {"xy"}).isEmpty()) throw new AssertionError("ex2");
        if (!find(board, new String[] {"ca", "ca"}).equals(List.of("ca"))) throw new AssertionError("duplicate words");
        // The Java claim: a mark written as '#' gives a negative array index, which throws.
        try { int[] probe = new int[26]; int x = probe['#' - 'a']; throw new AssertionError("no exception " + x); }
        catch (ArrayIndexOutOfBoundsException expected) { /* '#' - 'a' is -62 */ }
        // Random boards and dictionaries must match the independent searches.
        Random rnd = new Random(2014);
        for (int t = 0; t < 400; t++) {
            int R = 1 + rnd.nextInt(3), C = 1 + rnd.nextInt(4);
            String[] b = new String[R];
            for (int i = 0; i < R; i++) { StringBuilder sb = new StringBuilder(); for (int j = 0; j < C; j++) sb.append((char) ('a' + rnd.nextInt(3))); b[i] = sb.toString(); }
            String[] w = new String[rnd.nextInt(10)];
            for (int i = 0; i < w.length; i++) { StringBuilder x = new StringBuilder(); for (int j = 0, m = 1 + rnd.nextInt(5); j < m; j++) x.append((char) ('a' + rnd.nextInt(3))); w[i] = x.toString(); }
            String[] copy = b.clone();
            if (!find(b, w).equals(oracle(b, w))) throw new AssertionError("random " + t);
            if (!Arrays.equals(b, copy)) throw new AssertionError("board changed " + t);
        }
        // The cost claim: many words with a shared prefix make fewer calls in one tree search than in separate searches.
        String[] grid = {"aaaa", "aaaa", "aaaa"};
        List<String> ws = new ArrayList<>();
        for (int mask = 0; mask < 32; mask++) { StringBuilder sb = new StringBuilder("aaaa"); sb.append((mask & 1) == 0 ? 'a' : 'b'); sb.append((mask & 2) == 0 ? 'a' : 'b'); ws.add(sb.toString()); }
        trieCalls = 0; baseCalls = 0;
        find(grid, ws.toArray(new String[0])); oracle(grid, ws.toArray(new String[0]));
        if (trieCalls >= baseCalls) throw new AssertionError("tree search should make fewer calls: " + trieCalls + " vs " + baseCalls);
        System.out.println("ok");
    }
}
```
