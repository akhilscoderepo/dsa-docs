<!-- lesson-kind: combination -->
<!-- lesson-id: trie-and-backtracking -->
## Trie And Backtracking

<!-- stage: context -->
### The Word Hunters Of Quarry Hill

The puzzle club of Quarry Hill meets on Thursdays around a tiled table, where a grid of letter tiles is laid out and the members hunt for words in it. A word counts when its letters can be read by stepping from tile to neighbouring tile, up, down, left or right, without lifting the same tile twice. Each week the club secretary hands out a list of several hundred target words and wants the members to report which of them are hidden in the grid.

The members used to take one word at a time and search the table for it. By the second hour they were tired, because every word that began with the letters `st`, and there were dozens, sent them off along the same few tile routes again, and a word that began with a letter found nowhere near its second letter still cost a long hunt. The secretary suspected that they were doing the same walking many times over.

<!-- stage: contributions -->
### What Each Structure Brings

Backtracking brings the walk across the board. It owns the current route, the marker on every tile that is in use, and the discipline of lifting each marker as the walk steps back. Without it there is no way to move from tile to tile without reusing one, and no way to try every route from a tile in turn.

The trie brings memory of the whole word list at once. The node reached by the letters on the current route stands for every listed word that begins with those letters, a missing edge means that none of them does, and a flag, or a stored word, at the node says that the route so far spells a listed word. Without the trie, each word has to be asked about separately.

Neither is enough alone. A trie with no walk has no tiles to read, and a walk with no trie knows only about one target at a time. The combination is recognised by a search over a board for many words whose answers depend on shared beginnings, and the question to ask at every tile is whether any word still begins with the route so far.

<!-- stage: naive -->
### One Full Search For Every Word

The direct method runs the single-word search of the previous lesson once for each target word. A word is reported when its search succeeds.

```java
final class OneByOne {
    static List<String> huntByWord(char[][] tiles, String[] targets) {
        List<String> found = new ArrayList<>();
        for (String word : targets) {
            if (exists(tiles, word)) found.add(word);
        }
        Collections.sort(found);
        return found;
    }

    private static boolean exists(char[][] tiles, String word) {
        boolean[][] used = new boolean[tiles.length][tiles[0].length];
        for (int r = 0; r < tiles.length; r++)
            for (int c = 0; c < tiles[0].length; c++)
                if (reads(tiles, word, 0, r, c, used)) return true;
        return false;
    }

    private static boolean reads(char[][] t, String w, int k, int r, int c, boolean[][] used) {
        if (r < 0 || c < 0 || r >= t.length || c >= t[0].length) return false;
        if (used[r][c] || t[r][c] != w.charAt(k)) return false;
        if (k == w.length() - 1) return true;
        used[r][c] = true;
        boolean ok = reads(t, w, k + 1, r + 1, c, used) || reads(t, w, k + 1, r - 1, c, used)
                  || reads(t, w, k + 1, r, c + 1, used) || reads(t, w, k + 1, r, c - 1, used);
        used[r][c] = false;
        return ok;
    }
}
```

The single-word search leaves its flags and the grid as it found them. The method is correct for any list, including a list with repeated words if each repeat is reported once, and it serves as the oracle for the faster hunt.

<!-- stage: bottleneck -->
### Shared Beginnings Are Walked Again

With W words of length up to L on a board of R by C tiles, every word pays for a search of its own, and a search can cost O(R * C * 3^L) steps in the worst case, so the whole hunt costs O(W * R * C * 3^L). Words that share a beginning, such as `star`, `start` and `stare`, send the walker over the identical routes for the letters `s`, `t`, `a`, `r` each time, and every one of those walks is repeated from scratch for the next word.

The method also has no way to tell the walker that a route is hopeless for all words at once. A route spelling `qz` is abandoned by each word separately, long after any single list lookup could have said that no word in the list begins with those letters. A hunt that carried the whole list along the route, and stopped the moment no word could continue, would walk each distinct beginning at most once.

<!-- stage: insight -->
### Walk The Board And The Trie Together

Let the walk through the board carry a **trie cursor**, the node of the trie that stands for the letters on the current route. At the start of a route the cursor is the root. Stepping onto a tile reads its letter, and the cursor must move to the child with that letter. The board path and the trie path are the same string, read from two structures at once.

When the cursor has no child for the tile's letter, the **missing-edge cut** applies: no listed word begins with the route plus this letter, so the walk does not step onto the tile at all, and no marker is placed. One failed lookup abandons every word that would have followed. Each distinct beginning of the word list is therefore walked at most once from each tile where it can occur, and the cost no longer carries a factor of the number of words.

A word is found when the cursor reaches a node that stores a word. The same node can be reached by many routes, for example when the grid holds several copies of the same letters, so the rule is **one-time emission**: record the word and clear it from the node at that moment. Only the stored word is cleared, never the node, because longer words may pass through it and the route must continue. A later route that reaches the node finds nothing stored and emits nothing, so every word appears once however many routes spell it.

The board side keeps its own discipline. The tile is marked before the neighbours are tried and restored after all of them have been tried, whatever was found below.

The invariant is that the cursor always equals the trie node for exactly the letters on the marked board path, and on return both the cursor of the caller and the board markers are as they were on entry.

<!-- names: trie cursor, missing-edge cut, one-time emission -->

<!-- stage: variables -->
### Tile, Cursor, Mark And Found List

The pair `r` and `c` is the tile the call is about to enter. The `parent` is the cursor of the caller, and the `node` obtained from it by the tile's letter is the new cursor, which exists only if the edge does. The letter kept in `saved` is the tile's original letter, replaced by `#` during exploration and put back afterwards. The `word` field of a trie node holds the complete target word at the node where that word ends, and it is set to nothing at the moment it is emitted. The `found` list receives each word once, and it is sorted at the end so that the answer does not depend on the order in which tiles were tried.

<!-- stage: trace -->
### Hunting In A Row Of Four Tiles

The first trace hunts for `oat`, `oath` and `hat` in a single row of tiles reading `o`, `a`, `t`, `h`, where a step goes to the tile on the left or right and a tile may not be used twice. The pointer `cell` is the tile being entered. The variable `prefix` is the route spelled so far, which is also the cursor's node, and `found` holds the words emitted. Watch the walk starting on the last tile, where the letter `h` is a valid beginning but `t` is not its continuation.

```trace
{"cells":["o","a","t","h"],"pointers":["cell"],"steps":[{"at":{"cell":0},"vars":{"prefix":"o","found":"none"},"note":"The tile 0 is entered, and the cursor moves to the node for o."},{"at":{"cell":1},"vars":{"prefix":"oa","found":"none"},"note":"The tile 1 is entered, and the cursor moves to the node for oa."},{"at":{"cell":0},"vars":{"prefix":"oa","found":"none"},"note":"The tile 0 holding o is already on the route, so the walk may not return to it."},{"at":{"cell":2},"vars":{"prefix":"oat","found":"oat"},"note":"The tile 2 is entered, and the cursor moves to the node for oat. That node stores the word oat, so it is emitted and cleared from the node."},{"at":{"cell":1},"vars":{"prefix":"oat","found":"oat"},"note":"The tile 1 holding a is already on the route, so the walk may not return to it."},{"at":{"cell":3},"vars":{"prefix":"oath","found":"oat,oath"},"note":"The tile 3 is entered, and the cursor moves to the node for oath. That node stores the word oath, so it is emitted and cleared from the node."},{"at":{"cell":2},"vars":{"prefix":"oath","found":"oat,oath"},"note":"The tile 2 holding t is already on the route, so the walk may not return to it."},{"at":{"cell":3},"vars":{"prefix":"oath","found":"oat,oath"},"note":"Both neighbours of tile 3 have been tried, so its marker is lifted and the cursor goes back to oat."},{"at":{"cell":2},"vars":{"prefix":"oat","found":"oat,oath"},"note":"Both neighbours of tile 2 have been tried, so its marker is lifted and the cursor goes back to oa."},{"at":{"cell":1},"vars":{"prefix":"oa","found":"oat,oath"},"note":"Both neighbours of tile 1 have been tried, so its marker is lifted and the cursor goes back to o."},{"at":{"cell":0},"vars":{"prefix":"o","found":"oat,oath"},"note":"Both neighbours of tile 0 have been tried, so its marker is lifted and the cursor goes back to the root."},{"at":{"cell":1},"vars":{"prefix":"root","found":"oat,oath"},"note":"The cursor at the root has no child for the letter a, so no listed word continues this way and the tile is not entered."},{"at":{"cell":2},"vars":{"prefix":"root","found":"oat,oath"},"note":"The cursor at the root has no child for the letter t, so no listed word continues this way and the tile is not entered."},{"at":{"cell":3},"vars":{"prefix":"h","found":"oat,oath"},"note":"The tile 3 is entered, and the cursor moves to the node for h."},{"at":{"cell":2},"vars":{"prefix":"h","found":"oat,oath"},"note":"The cursor at h has no child for the letter t, so no listed word continues this way and the tile is not entered."},{"at":{"cell":3},"vars":{"prefix":"h","found":"oat,oath"},"note":"Both neighbours of tile 3 have been tried, so its marker is lifted and the cursor goes back to the root."}]}
```

The second trace hunts for the word `aa` in a row of three tiles that all read `a`. Several routes spell it. The variable `found` shows that the word is recorded the first time a route reaches its node and never again, and that the routes keep walking after the emission, since a longer word could still pass through the same node.

```trace
{"cells":["a","a","a"],"pointers":["cell"],"steps":[{"at":{"cell":0},"vars":{"prefix":"a","found":"none"},"note":"The tile 0 is entered, and the cursor moves to the node for a."},{"at":{"cell":1},"vars":{"prefix":"aa","found":"aa"},"note":"The tile 1 is entered, and the cursor moves to the node for aa. That node stores the word aa, so it is emitted and cleared from the node."},{"at":{"cell":0},"vars":{"prefix":"aa","found":"aa"},"note":"The tile 0 holding a is already on the route, so the walk may not return to it."},{"at":{"cell":2},"vars":{"prefix":"aa","found":"aa"},"note":"The cursor at aa has no child for the letter a, so no listed word continues this way and the tile is not entered."},{"at":{"cell":1},"vars":{"prefix":"aa","found":"aa"},"note":"Both neighbours of tile 1 have been tried, so its marker is lifted and the cursor goes back to a."},{"at":{"cell":0},"vars":{"prefix":"a","found":"aa"},"note":"Both neighbours of tile 0 have been tried, so its marker is lifted and the cursor goes back to the root."},{"at":{"cell":1},"vars":{"prefix":"a","found":"aa"},"note":"The tile 1 is entered, and the cursor moves to the node for a."},{"at":{"cell":0},"vars":{"prefix":"aa","found":"aa"},"note":"The tile 0 is entered, and the cursor moves to the node for aa."},{"at":{"cell":1},"vars":{"prefix":"aa","found":"aa"},"note":"The tile 1 holding a is already on the route, so the walk may not return to it."},{"at":{"cell":0},"vars":{"prefix":"aa","found":"aa"},"note":"Both neighbours of tile 0 have been tried, so its marker is lifted and the cursor goes back to a."},{"at":{"cell":2},"vars":{"prefix":"aa","found":"aa"},"note":"The tile 2 is entered, and the cursor moves to the node for aa."},{"at":{"cell":1},"vars":{"prefix":"aa","found":"aa"},"note":"The tile 1 holding a is already on the route, so the walk may not return to it."},{"at":{"cell":2},"vars":{"prefix":"aa","found":"aa"},"note":"Both neighbours of tile 2 have been tried, so its marker is lifted and the cursor goes back to a."},{"at":{"cell":1},"vars":{"prefix":"a","found":"aa"},"note":"Both neighbours of tile 1 have been tried, so its marker is lifted and the cursor goes back to the root."},{"at":{"cell":2},"vars":{"prefix":"a","found":"aa"},"note":"The tile 2 is entered, and the cursor moves to the node for a."},{"at":{"cell":1},"vars":{"prefix":"aa","found":"aa"},"note":"The tile 1 is entered, and the cursor moves to the node for aa."},{"at":{"cell":0},"vars":{"prefix":"aa","found":"aa"},"note":"The cursor at aa has no child for the letter a, so no listed word continues this way and the tile is not entered."},{"at":{"cell":2},"vars":{"prefix":"aa","found":"aa"},"note":"The tile 2 holding a is already on the route, so the walk may not return to it."},{"at":{"cell":1},"vars":{"prefix":"aa","found":"aa"},"note":"Both neighbours of tile 1 have been tried, so its marker is lifted and the cursor goes back to a."},{"at":{"cell":2},"vars":{"prefix":"a","found":"aa"},"note":"Both neighbours of tile 2 have been tried, so its marker is lifted and the cursor goes back to the root."}]}
```

<!-- stage: code -->
### The Cursor Moves With The Walk

```java
final class WordHunt {
    private static final class Node {
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

    private static void walk(char[][] t, int r, int c, Node parent, List<String> found) {
        if (r < 0 || c < 0 || r >= t.length || c >= t[0].length) return;
        char saved = t[r][c];
        if (saved == '#') return;                        // tile is on the route
        Node node = parent.next[saved - 'a'];
        if (node == null) return;                        // missing-edge cut
        if (node.word != null) { found.add(node.word); node.word = null; }  // one-time emission
        t[r][c] = '#';
        walk(t, r + 1, c, node, found);
        walk(t, r - 1, c, node, found);
        walk(t, r, c + 1, node, found);
        walk(t, r, c - 1, node, found);
        t[r][c] = saved;                                 // restore
    }
}
```

The test for `#` must come before the lookup, because `'#' - 'a'` is a negative number and would index outside the array of children. The trie holds each word once, so repeated targets collapse into one stored word. The cost is bounded by the number of distinct beginnings that can be spelled along routes of the grid, which is far below the cost of one search per word, and the stack is as deep as the longest word.

<!-- stage: applicability -->
### Many Words, One Board

Use the combined walk when a board or grid is searched for many words, or for any family of strings that share beginnings, and the answer is which of them appear. Boggle-style puzzles, crossword fill checks and the search of a word list through a grid of letters all fit. The invariant to hold is that the cursor spells exactly what the marked path spells, so every step has to move both together.

The nearest false friend is the pair of structures used separately: running the single-word search once per target, which is correct and repeats every shared beginning, or building the trie and then searching it as if it were a list, with no walk over the board. A second false friend is clearing the trie node and not only the stored word on emission, which cuts off longer words that pass through the same node and silently drops them from the answer.

Do not use the trie when there is a single target, since the plain search of the previous lesson is simpler, or when the list is tiny. Keep the alphabet in mind, because the array of children assumes lowercase letters and the marker character must lie outside the alphabet. Memoising repeated sub-searches of this kind needs a precise definition of equal states, and that belongs to the dynamic-programming chapters, so this lesson does not attempt it.

<!-- stage: exercises -->
### Exercises

#### [Build] Trie-Guided Row Search (Author exercise)
<!-- id: bc-row-search -->

**Prerequisites.** The trie with a stored word at each word-ending node, and the mark-and-restore walk of the board lesson.

**Problem.** A row of lowercase letters and a list of words are given. A word is found when its letters can be read by starting on any tile and stepping to the tile immediately left or right, never using a tile twice in one reading. Carry a trie cursor along the walk and report each found word, in alphabetical order.

**Constraints.** The row has 1 to 8 tiles, the list has 0 to 8 words, and each word has 1 to 8 lowercase letters.

**Example 1.** Input `row = "oath"`, `words = ["oat", "oath", "hat"]`, output `["oat", "oath"]`.

**Example 2.** Input `row = "tao"`, `words = ["oat", "tao", "at"]`, output `["at", "oat", "tao"]`.

**Hint.** Where on the row does a route that reads `oat` from right to left begin, and which letters does the cursor consume along the way?

**Changed decision.** The state of the walk is a trie node, not an index into one word, and a word is reported at the node that stores it.

#### [Vary] Stop On Missing Trie Edge (Author exercise)
<!-- id: bc-missing-edge -->

**Prerequisites.** The Trie-Guided Row Search rung.

**Problem.** Run the same row search and return `[found, entered]`, where `found` is the number of distinct words found and `entered` is the number of times the walk steps onto a tile, which happens only when the tile is unmarked and the cursor has a child for its letter. A tile whose letter has no edge is never entered.

**Constraints.** The row has 1 to 8 tiles, the list has 0 to 8 words, and each word has 1 to 8 lowercase letters.

**Example 1.** Input `row = "oath"`, `words = ["oat", "oath", "hat"]`, output `[2, 5]`.

**Example 2.** Input `row = "xyz"`, `words = ["abc"]`, output `[0, 0]`.

**Hint.** From which tiles does the walk begin when no word starts with the tile's letter, and how many tiles does it enter from them?

**Changed decision.** A missing edge ends a route before the tile is entered, so impossible prefixes cost one failed lookup and no marker.

#### [Boundary] Shared Prefix And Duplicate Discovery (Author exercise)
<!-- id: bc-duplicate-discovery -->

**Prerequisites.** The Stop On Missing Trie Edge rung.

**Problem.** Run the row search again, but the list may contain the same word twice, and several different routes may spell the same word. Report every found word exactly once, in alphabetical order, by clearing the stored word at the node when it is first emitted and never clearing the node itself.

**Constraints.** The row has 1 to 8 tiles, the list has 0 to 10 words with repeats allowed, and each word has 1 to 8 lowercase letters.

**Example 1.** Input `row = "aaa"`, `words = ["aa", "a", "aaa"]`, output `["a", "aa", "aaa"]`.

**Example 2.** Input `row = "ab"`, `words = ["ab", "ba", "ab"]`, output `["ab", "ba"]`.

**Hint.** If the node were removed from its parent at the first emission, what would happen to a longer word that passes through it?

**Changed decision.** Emission clears only the stored word, so a node can be reached again by another route without a second report.

#### [Recognize] Word Search II (LeetCode 212)
<!-- id: bc-word-search-two -->

**Prerequisites.** The Shared Prefix And Duplicate Discovery rung, and the four-direction walk of the board lesson.

**Problem.** Given a board of lowercase letters and a list of words, return every word that can be traced through the board by stepping to a tile directly above, below, left or right, without using a tile twice in one trace, listed in alphabetical order. Search all words together with a trie.

**Constraints.** The board has 1 to 5 rows and 1 to 5 columns, and the list has 1 to 12 words of 1 to 8 lowercase letters each.

**Example 1.** Input `board = ["cat", "oxe", "dgs"]`, `words = ["cod", "cat", "tex", "sea", "dog", "xxx"]`, output `["cat", "cod", "tex"]`.

**Example 2.** Input `board = ["aa"]`, `words = ["aaa", "a"]`, output `["a"]`.

**Hint.** Which of the earlier rungs already contains the cursor and the emission rule, and what changes when a tile has four neighbours instead of two?

**Changed decision.** The two-neighbour step of the row becomes four neighbours with a restored marker, while the cursor and the emission rule stay as they were.
