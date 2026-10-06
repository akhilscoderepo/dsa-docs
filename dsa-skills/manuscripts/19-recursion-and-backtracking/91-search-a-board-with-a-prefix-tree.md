<!-- lesson-kind: combination -->
<!-- lesson-id: board-prefix-tree -->
## Search A Board With A Prefix Tree

<!-- stage: context -->
### Why The Word Game Needs Minutes

A word game lists every dictionary word that appears on a 4 by 4 letter board. The dictionary holds 10,000 words. The first version runs one board search for each word, and the board search tries every cell as a start. Words such as `stone`, `stones` and `stoned` begin with the same five letters. The program walks the same path of cells for `stone` once for each of those words, and a busy round of the game needs minutes.

The program can see the shared start before the search begins. This lesson asks how one search over the board follows all dictionary words at once. It also asks how the search stops a path as soon as no word begins with the letters spelled so far.

<!-- stage: contributions -->
### What The Search And Tree Each Add

Two earlier ideas combine here. The board search from the lesson on marking cells owns the current path. It marks each cell that the path enters, tries the touching cells and clears the mark on the way out. A path of cells therefore never uses a cell twice, and every sibling branch starts from the same marks. The search alone knows nothing about the dictionary, so it needs a target letter for each step.

The prefix tree from the chapter on tries represents every prefix of every dictionary word. A node stands for the letters spelled so far, and an edge exists only when some word continues with that letter. A missing edge proves that no word begins with the current path. The tree alone cannot move across a board, because it has no notion of touching cells or of cells in use. Independent word searches repeat the same prefixes, and a tree without a path search never reads the board.

<!-- stage: naive -->
### Running One Board Search For Each Word

The direct plan keeps the dictionary as a list. For each word, it calls the board search of the lesson on marking cells and collects the words that the search finds.

```java
static List<String> wordByWord(char[][] board, List<String> words, java.util.function.BiPredicate<char[][], String> exists) {
    List<String> found = new ArrayList<>();
    for (String w : words) {                            // one complete board search for each word
        if (exists.test(board, w)) found.add(w);        // the board search marks cells and restores them, as before
    }
    return found;
}
```

The method returns every word that appears on the board, because each word gets a complete search. It repeats the walk of a shared prefix once for every word that starts with it.

<!-- stage: bottleneck -->
### Counting The Walks Of One Prefix

```predict
The dictionary holds 5,000 words that begin with the same three letters, and the board has 5 paths that spell those three letters. How many times does the word-by-word plan walk those paths for the first three letters, and how many times does a search that follows all words together walk them?

The word-by-word plan walks the 5 paths once for each of the 5,000 words, so it makes 25,000 path walks over the first three letters. A search that follows all words together walks the 5 paths once, which is 5 walks.
```

The word-by-word plan costs O(W * R * C * 3^L) time for `W` words of up to `L` letters on a board of `R` rows and `C` columns. The factor `W` appears because each word repeats every shared prefix. It also keeps exploring paths such as `qz` that no dictionary word can use, since each search only knows its own word.

A single search needs to know, at each cell, which dictionary words are still possible. Those words are exactly the words below one node of a prefix tree, so the search can carry that node as its state.

<!-- stage: insight -->
### Carrying The Tree Node Along The Path

#### Moving The Node With The Path

The **node state** is the prefix tree node that spells the letters of the cells on the current path. The call at a cell reads the letter of the cell and looks up the child of the node for that letter. The call then marks the cell and passes the child to each touching cell. The node and the marked cells always agree: the node spells exactly the letters of the marked cells, in path order. The invariant is that on exit of a call, the marks and the node match the state at entry.

#### Stopping At A Missing Edge

A **missing edge** is a null child for the letter of the cell. It proves that no dictionary word begins with the path plus this letter. The call returns at once, before it marks the cell or visits any neighbour. This single test replaces the target letter of the single-word search, and it prunes the whole subtree below the cell. Branches that no word can use cost one lookup.

#### Reporting A Word Once

A node that ends a dictionary word stores the word. When a path arrives at that node, the search reports the word. Several paths can reach the same node, and each would report the word again. The **emit once** rule clears the stored word of the node after the first report, so later paths find an empty slot and report nothing. The call keeps searching below the node after the report, because a longer word may continue from it.

<!-- names: node state, missing edge, emit once -->

<!-- stage: variables -->
### The Pieces Of State

Five pieces of state describe a call.

- **Cell** is the pair of a row and a column that the call tries to enter.
- **Node** is the prefix tree node that spells the path before this cell.
- **Path marks** are one boolean flag for each cell, true for the cells of the active calls.
- **Stored word** is the dictionary word that ends at a node, or `null` when no word ends there or the search has reported it.
- **Found** is the list of words that the search has reported so far.

Entering a cell moves the node to the child for the letter, sets the mark, reports the stored word and visits the neighbours. The call clears the mark before it returns.

<!-- stage: trace -->
### Following The Node Along A Row

#### Searching The Row Aba

The first trace searches the row `aba` for the dictionary `ab` and `aba`, without the emit-once rule, so each path reports its word. Moves go to the touching cell on the left or on the right. The pointer `cell` marks the cell that the step enters. The variable `node` shows the letters that the node spells, and `found` counts the reports so far.

The search starts at cell 0 and enters the node `a`. Cell 1 holds `b`, and the node `ab` stores a word, so the search reports `ab`. Cell 2 holds `a` and leads to the node `aba`, which reports `aba`. The start at cell 1 finds no edge for `b` below the root, so the call returns at once. The start at cell 2 enters `a`, then reaches cell 1 and reports `ab` again, and then reaches cell 0 and reports `aba` again. The trace ends with 4 reports.

#### Reporting Each Word Once

The second trace repeats the start at cell 2 with the emit-once rule in force. The start at cell 0 reported both words, so their stored slots are empty. The path enters the nodes `a`, `ab` and `aba` and reports nothing. The list of found words keeps its 2 entries.

#### Stepping Through Both Runs

```trace
{"cells":["a","b","a"],"pointers":["cell"],"steps":[{"at":{"cell":0},"vars":{"node":"a","found":0},"note":"The call at cell 0 moves the node to a."},{"at":{"cell":1},"vars":{"node":"ab","found":1},"note":"The call at cell 1 moves the node to ab. The node stores ab, so the search reports it."},{"at":{"cell":2},"vars":{"node":"aba","found":2},"note":"The call at cell 2 moves the node to aba. The node stores aba, so the search reports it."},{"at":{"cell":1},"vars":{"node":"root","found":2},"note":"The letter b has no edge below the node root, so no word begins with b. The call returns before it marks the cell."},{"at":{"cell":2},"vars":{"node":"a","found":2},"note":"The call at cell 2 moves the node to a."},{"at":{"cell":1},"vars":{"node":"ab","found":3},"note":"The call at cell 1 moves the node to ab. The node stores ab, so the search reports it."},{"at":{"cell":0},"vars":{"node":"aba","found":4},"note":"The call at cell 0 moves the node to aba. The node stores aba, so the search reports it."}]}
```

```trace
{"cells":["a","b","a"],"pointers":["cell"],"steps":[{"at":{"cell":2},"vars":{"node":"a","found":2},"note":"The call at cell 2 moves the node to a."},{"at":{"cell":1},"vars":{"node":"ab","found":2},"note":"The call at cell 1 moves the node to ab. The slot of ab is empty after its first report, so nothing is reported."},{"at":{"cell":0},"vars":{"node":"aba","found":2},"note":"The call at cell 0 moves the node to aba. The slot of aba is empty after its first report, so nothing is reported."}]}
```

<!-- stage: code -->
### Writing The Combined Search In Java

#### The Tree And The Board Search Together

The class below builds the prefix tree, then runs one search from every cell. The node moves with the path, and the marks come back on exit.

```java
final class BoardTrie {
    private static final class Node {
        final Node[] next = new Node[26];               // one child for each lowercase letter
        String word;                                    // the word that ends here, or null
    }

    static List<String> findWords(char[][] board, String[] words) {
        Node root = new Node();
        for (String w : words) {                        // build the tree: one path for each word
            Node cur = root;
            for (int i = 0; i < w.length(); i++) {
                int s = w.charAt(i) - 'a';              // the input holds lowercase letters only
                if (cur.next[s] == null) cur.next[s] = new Node();
                cur = cur.next[s];
            }
            cur.word = w;                               // a repeated word writes the same value again
        }
        List<String> found = new ArrayList<>();
        boolean[][] on = new boolean[board.length][board[0].length];
        for (int r = 0; r < board.length; r++)
            for (int c = 0; c < board[0].length; c++) go(board, r, c, root, on, found);   // every cell may start a word
        return found;
    }

    private static void go(char[][] b, int r, int c, Node parent, boolean[][] on, List<String> found) {
        if (r < 0 || c < 0 || r >= b.length || c >= b[0].length || on[r][c]) return;   // outside or in use
        Node node = parent.next[b[r][c] - 'a'];         // move the node by the letter of this cell
        if (node == null) return;                       // missing edge: no word has this prefix
        if (node.word != null) { found.add(node.word); node.word = null; }   // emit once, then clear the slot
        on[r][c] = true;                                // choose: mark the cell
        go(b, r - 1, c, node, on, found); go(b, r + 1, c, node, on, found);
        go(b, r, c - 1, node, on, found); go(b, r, c + 1, node, on, found);
        on[r][c] = false;                               // undo: clear the mark on every exit
    }
}
```

#### Cost Of The Search

The tree takes O(T) time and memory for `T` letters in the dictionary, with 26 slots for each node. The search makes at most 4 * 3^(L-1) calls from each start cell, and it never makes a call below a missing edge. The total time is O(R * C * 3^L) and does not depend on the number of words, except through the shape of the tree. The marks use O(R * C) memory.

<!-- stage: applicability -->
### Recognizing A Dictionary Search On A Board

#### Spotting The Pattern

The cue is a board or grid, many target words, and a path that may not reuse a cell. The combined invariant is that the node spells the marked cells and both return to their earlier state when the call exits.

#### Finding The False Friend

The false friend is a tree walk without marks. It lets a path enter one cell twice and reports words that the board cannot spell. A second false friend is a board search that loops over the words, which walks every shared prefix again. A third is a report without the emit-once rule, which returns the same word for each path that spells it.

#### Recognizing The No-Go Cases

The combination does not fit when the dictionary is tiny, because one search per word costs less than building a tree. It does not fit when the targets are patterns with wildcards, since an edge may then match several letters. A board with unbounded repeated cells needs a graph search and not a path search.

<!-- stage: exercises -->
### Exercises

#### [Build] Trie-Guided Row Search (Author exercise)
<!-- id: bt-trie-row-search -->

**Prerequisites.** The node state and the marks of this lesson.

**Problem.** The string `row` is a board with one row of lowercase letters, and `words` is an array of lowercase words. A path starts at any cell and moves to the touching cell on the left or on the right, and no cell appears twice. Build a prefix tree of `words` and search with it. Each time a path spells a dictionary word, add the word to the result. This exercise does not clear the stored word, so a word repeats once for each path. The search starts at the cells from left to right and tries the left neighbour before the right one.

**Constraints.** The limits are:
- **Row** has `1 <= row.length() <= 12` lowercase letters.
- **Words** satisfy `0 <= words.length <= 20`, and each word has `1 <= length <= 12` letters.
- **Result** holds a word once for each path that spells it.
- **Mutation** does not occur; `row` and `words` keep their contents.

**Example 1.** Input `row = "aba"`, `words = ["ab","aba"]`, output `["ab","aba","ab","aba"]`.

**Example 2.** Input `row = "x"`, `words = ["x"]`, output `["x"]`.

**Hint.** Which node does the call pass to a neighbour? Which two cells does a path starting at the last cell of `aba` visit?

**Changed decision.** A prefix tree node replaces the letter index, and a path reports a word whenever its node ends one.

#### [Vary] Stop On Missing Trie Edge (Author exercise)
<!-- id: bt-stop-on-missing-edge -->

**Prerequisites.** The previous exercise and the board search of the lesson on marking cells.

**Problem.** The strings of `board` are the rows of a letter grid, and `words` lists lowercase words. Return true when at least one word appears on the grid. A path moves to a touching cell above, below, left or right and does not reuse a cell. Search with a prefix tree node in place of the letter index. A missing edge ends a call at once, and the first word that a path spells ends the whole search.

**Constraints.** The limits are:
- **Board** has `1 <= rows, columns <= 5` lowercase letters.
- **Words** satisfy `0 <= words.length <= 20`, and each word has `1 <= length <= 10` letters.
- **Return** is a boolean, false when `words` is empty.
- **Mutation** does not occur; the board keeps its letters after the call.

**Example 1.** Input `board = ["ab","cd"]`, `words = ["abdc","zz"]`, output true.

**Example 2.** Input `board = ["ab","cd"]`, `words = ["zz","abcd"]`, output false.

**Hint.** When does a call return before it marks a cell? What must the call restore before it returns true?

**Changed decision.** The search asks whether any word exists, so it stops at the first report and still clears every mark on the way out.

#### [Boundary] Shared Prefix And Duplicate Discovery (Author exercise)
<!-- id: bt-shared-prefix-duplicates -->

**Prerequisites.** The two exercises above.

**Problem.** Use the row board and the moves of the first exercise. Return each dictionary word that some path spells exactly once, in the order of the first report. A word may be a prefix of another word, and `words` may list the same word several times. The search must continue below a node after it reports the word of that node.

**Constraints.** The limits are:
- **Row** has `1 <= row.length() <= 12` lowercase letters.
- **Words** satisfy `0 <= words.length <= 20`, may repeat, and each word has `1 <= length <= 12` letters.
- **Result** holds each found word once.
- **Order** follows the first report of each word.

**Example 1.** Input `row = "aba"`, `words = ["ab","aba","ab"]`, output `["ab","aba"]`.

**Example 2.** Input `row = "ab"`, `words = ["ba"]`, output `["ba"]`.

**Hint.** What does the node of `ab` hold after the first report? Why must the search continue below that node?

**Changed decision.** The search clears the stored word after the first report and does not stop at a node that ends a word.

#### [Recognize] Word Search II (LeetCode 212)
<!-- id: bt-word-search-two -->

**Prerequisites.** The previous three exercises.

**Problem.** The array `board` holds rows of lowercase letters, and `words` is an array of lowercase words. Return every word that appears on the board, where a path moves to a touching cell above, below, left or right and does not reuse a cell. Each word appears once in the result, and the result is in lexicographic order. The list `words` may hold the same word several times.

**Constraints.** The limits are:
- **Board** has `1 <= rows, columns <= 5` lowercase letters.
- **Words** satisfy `0 <= words.length <= 30`, and each word has `1 <= length <= 10` letters.
- **Result** holds each found word once, in lexicographic order.
- **Mutation** does not occur; the board keeps its letters after the call.

**Example 1.** Input `board = ["ab","cd"]`, `words = ["abdc","acd","bad","ca"]`, output `["abdc","acd","ca"]`.

**Example 2.** Input `board = ["ab","cd"]`, `words = ["xy"]`, output `[]`.

**Hint.** Which node holds a word that two different paths can spell? Which two states must the call restore on exit?

**Changed decision.** The board has four directions, and the tree and the marks both return to their earlier state when a call exits.
