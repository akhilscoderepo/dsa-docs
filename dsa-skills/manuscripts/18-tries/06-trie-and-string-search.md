<!-- lesson-kind: combination -->
<!-- lesson-id: trie-and-string-search -->
## Trie And String Search

<!-- stage: context -->
### The Telegraph Office Of Pine Ridge

The telegraph office of Pine Ridge charges by the letter, so the clerks shorten messages with a book of approved roots. When a word in a telegram begins with an approved root, the clerk writes only the root. Long words such as `cattle` and `cattery` both become `cat`. A word with no approved root in front of it is sent whole. The same book also feeds a small game that the clerks play in the evening. Given the book as a list of words, they look for the longest word that can be built one letter at a time, so that every shorter beginning of it is also in the book.

Every telegram holds hundreds of words, and the book holds thousands of roots. A clerk reads each telegram word letter by letter and asks the book about its beginnings, and she has noticed that the book keeps being consulted about the same beginnings over and over.

<!-- stage: contributions -->
### What Each Structure Brings

The string brings an order of reading. A word is consumed one letter at a time from the left, and the letters already consumed are exactly the beginning that the next question is about, so the text hands over the next symbol and a clear place to stop, which is its own end.

The trie brings memory of candidates. The node reached after some letters stands for every stored word that begins with those letters, and an edge that is missing rules out all of them at once. It also records which beginnings are themselves words, through the flag.

Neither is enough alone. A string with no structure behind it must ask about every stored word, and a trie with no text to read has no question to follow. The recognition cue for the combination is a question about the beginnings of a text, such as the shortest stored beginning or the stored beginnings that are words themselves, where the answer is decided by the first flag met or the first missing edge.

<!-- stage: naive -->
### Test Every Root Against Every Word

The direct method takes each word of the telegram and tests every root in the book to see whether the word begins with it, keeping the shortest root that does. A word with no matching root stays as it is.

```java
static String shorten(String word, List<String> roots) {
    String best = null;
    for (String root : roots) {
        if (word.startsWith(root) && (best == null || root.length() < best.length())) best = root;
    }
    return best == null ? word : best;
}
```

The method answers correctly for any book of roots, including a book where one root begins another, since it compares each root separately and keeps the shortest that fits.

<!-- stage: bottleneck -->
### Unrelated Roots Are Compared Again

For a telegram of w words, a book of r roots and words of length up to L, the method costs O(w * r * L), because every word is compared with every root. Two hundred thousand words against ten thousand roots is two billion comparisons before any letter is counted. Nearly all of them are wasted. A word that begins with `ca` has nothing to do with the roots that begin with `b`, yet each of those roots is tested and rejected, and each root that shares a beginning with the word repeats the same letter comparisons that its neighbours already made.

The longest buildable word shows the same waste in another form. Testing each word by looking up all of its beginnings costs O(L) hash lookups of strings of growing length, which is O(L^2) letters per word. What is wanted is to read each word once, one letter at a time, against a structure that already knows which beginnings are roots, at a cost of O(L) per word.

<!-- stage: insight -->
### Read The Text Against The Trie

Put the roots into a trie, and let a cursor start at the root of the trie while a loop reads the word from the left. After i letters the cursor stands on the node for the **consumed prefix**, the first i letters of the word, and that node stands for all roots that begin with it. A missing edge means no root begins with the consumed prefix, so reading further is pointless. A flagged node means the consumed prefix is itself a root.

What the walk does at a flagged node is the **stop rule**, and it is the only thing that changes between problems. To shorten a word, stop at the first flagged node and return the consumed prefix, since the first flag met is the shortest root. If the walk ends by a missing edge or by the end of the word with no flag seen, the word has no root and is kept whole. To answer an exact or beginning question, as in the first rungs of the ladder, the stop rule is the flag test at the end. With a pattern containing blanks, the stop rule is the same, and the single change is that the walk fans out at a blank.

The longest buildable word uses a **terminal-only descent**. A word is buildable only if every shorter beginning is a word, so the search may enter a child only when that child's own flag is set. Any node reached this way has an unbroken chain of flags above it, and the deepest such node, with ties broken alphabetically, is the answer.

The invariant is that the cursor always stands on the node for the consumed prefix, so one pass over the text answers every beginning question about it.

<!-- names: consumed prefix, stop rule, terminal-only descent -->

<!-- stage: variables -->
### Cursor, Depth And Best Word

For shortening, `node` is the cursor, `i` counts the consumed letters, and the returned piece is `word.substring(0, i)` taken only when the flag is met. For the buildable word, a depth-first call holds `node` and a `StringBuilder path` that spells the consumed prefix, extended before the child call and trimmed after it. The variable `best` holds the longest word found so far as a string, and it is replaced only when a path is strictly longer, which is enough for the alphabetical tie rule when children are visited in order. For a wildcard search with a cost report, `visited` counts the nodes entered.

<!-- stage: trace -->
### Shortening And Building

The first trace shortens the word `battery` against the roots `bat` and `cat`. The pointer `i` marks the letter being consumed. The first two letters follow edges without a flag. The third letter reaches a flagged node, and the stop rule ends the walk there, so the remaining letters `tery` are never read and the word is replaced by its first three letters.

```trace
{"cells":["b","a","t","t","e","r","y"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"node":"b","flag":"unset"},"note":"The node for b exists but is not flagged, so the walk continues."},{"at":{"i":1},"vars":{"node":"ba","flag":"unset"},"note":"The node for ba exists but is not flagged, so the walk continues."},{"at":{"i":2},"vars":{"node":"bat","flag":"set"},"note":"The node for bat is flagged, so the stop rule fires: the shortest root is bat, and the letters after position 2 are never read."}]}
```

The second trace finds the longest buildable word in the sorted list shown in the cells. The pointer `w` marks the word whose node is entered. Children are entered only when flagged, in alphabetical order, so the words `xy` and `xyz`, whose first letter `x` is not itself a word, are never reached. The best word changes only when a strictly longer one is found, so `abd` does not replace `abc`.

```trace
{"cells":["a","ab","abc","abd","b","bd","xy","xyz"],"pointers":["w"],"steps":[{"at":{"w":0},"vars":{"best":"a","len":1},"note":"The node for a is flagged and entered, and a is longer than the best so far, so it becomes the best."},{"at":{"w":1},"vars":{"best":"ab","len":2},"note":"The node for ab is flagged and entered, and ab is longer than the best so far, so it becomes the best."},{"at":{"w":2},"vars":{"best":"abc","len":3},"note":"The node for abc is flagged and entered, and abc is longer than the best so far, so it becomes the best."},{"at":{"w":3},"vars":{"best":"abc","len":3},"note":"The node for abd is flagged and entered, but abd is not longer than the best word abc, so the best stays."},{"at":{"w":4},"vars":{"best":"abc","len":3},"note":"The node for b is flagged and entered, but b is not longer than the best word abc, so the best stays."},{"at":{"w":5},"vars":{"best":"abc","len":3},"note":"The node for bd is flagged and entered, but bd is not longer than the best word abc, so the best stays."}]}
```

<!-- stage: code -->
### Shorten Words And Find The Longest Buildable

```java
final class RootBook {
    private static final class Node {
        final Node[] next = new Node[26];
        boolean root;
    }

    private final Node top = new Node();
    private String best = "";

    void addRoot(String word) {
        Node cur = top;
        for (int i = 0; i < word.length(); i++) {
            int e = word.charAt(i) - 'a';
            if (cur.next[e] == null) cur.next[e] = new Node();
            cur = cur.next[e];
        }
        cur.root = true;
    }

    String shorten(String word) {
        Node cur = top;
        for (int i = 0; i < word.length(); i++) {
            cur = cur.next[word.charAt(i) - 'a'];
            if (cur == null) return word;
            if (cur.root) return word.substring(0, i + 1);
        }
        return word;
    }

    String longestBuildable() {
        best = "";
        build(top, new StringBuilder());
        return best;
    }

    private void build(Node node, StringBuilder path) {
        for (int e = 0; e < 26; e++) {
            Node child = node.next[e];
            if (child == null || !child.root) continue;
            path.append((char) ('a' + e));
            if (path.length() > best.length()) best = path.toString();
            build(child, path);
            path.setLength(path.length() - 1);
        }
    }
}
```

Shortening costs O(L) per word, and the whole telegram costs O(total letters) after the book is stored in O(total root letters). The buildable search visits each flagged node at most once, so it costs O(number of nodes) time and O(depth) stack, with the copy of the best string made only when a strictly longer path is found.

<!-- stage: applicability -->
### Reading Text Against A Dictionary

Use this combination when text is read from the left against a fixed list and the decision depends on the first flag, the last flag or the chain of flags along the way: stemming words to approved roots, finding the shortest abbreviation, checking that a word can be built up one letter at a time, and autocompletion that follows the typed letters. The invariant is that the cursor is always the node of the consumed prefix, and all decisions are made from that node.

The first false friend is the scan over the whole list for each word, which is correct and repeats unrelated comparisons. The second is to check each beginning of a word as a separate substring against a hash set, which is also correct and costs a quadratic number of letters per word. A third looks tempting but belongs elsewhere: searching a letter grid for many words at once also uses a trie, yet the path through the grid must be chosen, explored and then undone, and that state is taught in Chapter 19 and not here.

The method has no advantage when the book is tiny or each word is looked up once, since building the trie costs as much as the scan it replaces. In Java, a word shorter than every root simply ends with no flag and is returned whole, a case that has to be tested. Wrapping the answer in a `StringBuilder` for a sentence of many words avoids building a quadratic number of intermediate strings.

<!-- stage: exercises -->
### Exercises

#### [Build] Implement Trie (LeetCode 208)
<!-- id: ts-trie-distinct-words -->

**Prerequisites.** The prefix node and insert and search lessons.

**Problem.** Support four commands on lowercase words: `insert:w` adds a word, and inserting a word that is already stored changes nothing, `search:w` asks for an exact word, `startsWith:p` asks whether any stored word begins with `p`, and `distinct:p` reports how many different stored words begin with `p`. The prefix of a `startsWith` or `distinct` command may be empty. Return an integer for every command except `insert`, where 1 means true and 0 means false.

**Constraints.** Up to 3000 commands, every word has 1 to 20 letters, and every prefix has 0 to 20 letters.

**Example 1.** Input `commands = ["insert:car", "insert:car", "insert:cart", "distinct:ca", "search:ca", "startsWith:ca", "distinct:cars"]`, output `[2, 0, 1, 0]`.

**Example 2.** Input `commands = ["insert:ab", "insert:ab", "insert:b", "distinct:", "distinct:b", "startsWith:abc"]`, output `[2, 1, 0]`.

**Hint.** Should a repeated word change any number stored on its route, and which moment tells you that a word is new?

**Changed decision.** The count under a node is raised only when the flag at the end of a route is newly set, so duplicates do not count twice, unlike a pass count.

#### [Vary] Design Add and Search Words Data Structure (LeetCode 211)
<!-- id: ts-wildcard-search-cost -->

**Prerequisites.** The Build rung and the wildcard branching lesson.

**Problem.** Store distinct lowercase words in a trie. For each pattern, which may contain dots that match any one letter, return `[answer, visited]`. The answer is 1 if some stored word matches the pattern exactly in length and 0 otherwise. The count `visited` is the number of trie nodes entered other than the root, when the search tries the children of a dot in alphabetical order and stops at the first success.

**Constraints.** 0 <= words.length <= 500, 0 <= patterns.length <= 500, and each string has 1 to 12 characters.

**Example 1.** Input `words = ["tin", "ton", "tan", "tex"]`, `patterns = ["t.n", "t.z", "x.n", "..x"]`, output `[[1, 3], [0, 5], [0, 0], [1, 4]]`.

**Example 2.** Input `words = ["a"]`, `patterns = [".", "a", "b", ".."]`, output `[[1, 1], [1, 1], [0, 0], [0, 1]]`.

**Hint.** Where does the search branch, and which node counts as entered when a letter has no edge?

**Changed decision.** The call reports its own cost as well as its answer, which shows that only the dots widen the search.

#### [Boundary] Replace Words (LeetCode 648)
<!-- id: ts-replace-words -->

**Prerequisites.** The Vary rung and the stop rule at the first flag.

**Problem.** A list of root words and a sentence of lowercase words separated by single spaces are given. Replace every word that has a root as a beginning by the shortest such root, and keep every other word whole. A root longer than the word, or one that only shares the first letters, does not apply.

**Constraints.** 0 <= roots.length <= 1000, each root has 1 to 20 letters, and the sentence has 1 to 500 words of 1 to 30 letters each.

**Example 1.** Input `roots = ["ab", "abc", "x"]`, `sentence = "abcd abx xyz zzz ab a"`, output `"ab ab x zzz ab a"`.

**Example 2.** Input `roots = ["bat", "cab"]`, `sentence = "batman cabin ba tab"`, output `"bat cab ba tab"`.

**Hint.** What does the walk return when the word ends before any flag, and when an edge is missing?

**Changed decision.** The walk stops at the first flag instead of the last, and it returns the word itself when no flag is met.

#### [Recognize] Longest Word in Dictionary (LeetCode 720)
<!-- id: ts-longest-buildable -->

**Prerequisites.** The Replace Words rung.

**Problem.** For a list of lowercase words, return the longest word of which every nonempty beginning is also in the list, including the word itself. If several have the same length, return the alphabetically smallest. If no word qualifies, return the empty string.

**Constraints.** 1 <= words.length <= 1000 and each word has 1 to 30 letters. Words may repeat.

**Example 1.** Input `words = ["ab", "a", "abc", "b", "bd", "abd", "bde"]`, output `"abc"`.

**Example 2.** Input `words = ["xyz", "xy"]`, output `""`.

**Hint.** From a node, into which children may the search go, and when does a longer word replace the best one?

**Changed decision.** The search enters a child only if the child is itself flagged, so a gap in the chain of flags cuts off everything below it.
