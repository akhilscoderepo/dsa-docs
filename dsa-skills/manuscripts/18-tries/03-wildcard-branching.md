<!-- lesson-kind: standard -->
<!-- lesson-id: wildcard-branching -->
## Wildcard Branching

<!-- stage: context -->
### The Crossword Helper Of Mill Street

Every Sunday the Mill Street newsagent sells a crossword booklet, and every Sunday customers lean over the counter asking for help. A customer reads out a pattern such as `b.d`, meaning a three letter word whose first letter is `b` and last is `d`, with the middle square still blank. The newsagent keeps a pocket dictionary and wants to say quickly whether any word fits the pattern, and she does not care which one.

Some patterns are nearly full of letters and fit at most a handful of words. Others, such as `...`, are blank everywhere and fit a great many. She has noticed that the blank squares are the only places where she has any real choice, and that every letter the customer has written narrows the dictionary at once.

<!-- stage: naive -->
### Compare The Pattern With Every Word

The direct method takes each word of the right length from the pocket dictionary and compares it with the pattern square by square. A square matches when the pattern has a blank there or when the two letters agree. The first word that matches ends the search.

```java
static boolean fits(String pattern, String word) {
    if (pattern.length() != word.length()) return false;
    for (int i = 0; i < pattern.length(); i++) {
        if (pattern.charAt(i) != '.' && pattern.charAt(i) != word.charAt(i)) return false;
    }
    return true;
}

static boolean anyFits(String pattern, List<String> dictionary) {
    for (String word : dictionary) if (fits(pattern, word)) return true;
    return false;
}
```

It is correct for any dictionary, and short patterns that match early finish quickly.

<!-- stage: bottleneck -->
### Letters Are Ignored Until Compared

A pattern with no match makes the method read the whole dictionary, so one question costs O(n * L) for n words of length L, and ten thousand patterns against a hundred thousand words is a huge number of comparisons. The waste is plain when the pattern begins with `qz`: every word that does not begin with `qz` is still compared, one letter at a time, though the first two letters have already ruled it out for all of them at once.

The comparison cannot share its effort between words, because each word is a separate string. Words that start alike are compared against the same pattern letters again and again. A structure that groups words by their beginnings would let one comparison of `q` dismiss the whole group. Only at a blank square would the search need to look at several groups, and then only at the groups that exist, at a cost bounded by the nodes of the structure.

<!-- stage: insight -->
### Branch Only At The Blank Squares

Store the words in a trie and let a recursive call take a node and a position in the pattern. The call stands for every stored word whose beginning agrees with the pattern squares consumed so far, so the whole set of candidates is held in a single node. At a written letter, the call performs a **literal step**: it looks at one edge only and either follows it or reports failure. Nothing is lost by ignoring the other children, because no word through them can match that letter.

At a blank square, the call performs a **wildcard fan-out**: it makes one independent recursive call for each existing child, since any child could lead to a match. The calls do not share state beyond the node and the position, so each can be judged alone, and the call succeeds when any of them does. As soon as one succeeds, the remaining children are skipped, which is the **short-circuit** that keeps a yes answer cheap.

When the position reaches the end of the pattern, the call succeeds only if the node is flagged as a word. Reaching the end on an unflagged node means the pattern is a beginning of a longer word, which does not fit, and a word that ended earlier never gets this far because the walk has no edge left to follow.

The invariant is that a call at position i represents exactly the stored words that agree with the first i squares of the pattern.

<!-- names: literal step, wildcard fan-out, short-circuit -->

<!-- stage: variables -->
### Node, Position And Child Loop

A call takes `node`, the trie node reached after consuming `pos` squares, and `pos`, the index of the next pattern square. Only these two change from one call to the next, and neither is shared, so there is nothing to undo. `c` is the square under examination, and the test `c == '.'` is made before `c - 'a'` is used as an index, since the blank has no slot. The loop over the 26 slots of a node skips null entries. A boolean result travels upward, and the call returns at the first true.

<!-- stage: trace -->
### One Branch Then Many Branches

The first trace searches the pattern `b.d` in a trie holding `bad`, `bed`, `bid` and `cod`. The pointer `i` marks the pattern square a call is working on. The first square is a written letter, so only the edge `b` is followed and the `c` branch is never looked at. The second square is blank, so the call tries its children in alphabetical order, and the first child already leads to a flagged `bad`, which ends the search.

```trace
{"cells":["b",".","d"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"prefix":"","calls":1},"note":"The square is the letter b, so only the edge b is followed from the root."},{"at":{"i":1},"vars":{"prefix":"b","calls":2},"note":"The square is blank, so every child of b is a candidate: a, e, i in that order."},{"at":{"i":2},"vars":{"prefix":"ba","calls":3},"note":"The square is the letter d, so only the edge d is followed from ba."},{"at":{"i":3},"vars":{"prefix":"bad","calls":4},"note":"The pattern is used up at bad, and its flag is set, so this call answers yes."}]}
```

The second trace searches `.ad` in a trie holding `bat`, `cad`, `dad` and `cot`. The blank at the start fans out over `b`, `c` and `d`. The first child fails at its last letter, because `bat` ends in `t`, and the search backs up and tries the next sibling. Notice that the failure of one branch costs only that branch, and that the call count in the table grows with every branch entered.

```trace
{"cells":[".","a","d"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"prefix":"","calls":1},"note":"The square is blank, so every child of the root is a candidate: b, c, d in that order."},{"at":{"i":1},"vars":{"prefix":"b","calls":2},"note":"The square is the letter a, so only the edge a is followed from b."},{"at":{"i":2},"vars":{"prefix":"ba","calls":3},"note":"The square is the letter d, and ba has no edge d, so this call answers no without looking at any sibling."},{"at":{"i":1},"vars":{"prefix":"c","calls":4},"note":"The square is the letter a, so only the edge a is followed from c."},{"at":{"i":2},"vars":{"prefix":"ca","calls":5},"note":"The square is the letter d, so only the edge d is followed from ca."},{"at":{"i":3},"vars":{"prefix":"cad","calls":6},"note":"The pattern is used up at cad, and its flag is set, so this call answers yes."}]}
```

<!-- stage: code -->
### Dictionary With Dot Patterns

```java
final class DotDictionary {
    private static final class Node {
        final Node[] next = new Node[26];
        boolean word;
    }

    private final Node root = new Node();

    void add(String word) {
        Node cur = root;
        for (int i = 0; i < word.length(); i++) {
            int slot = word.charAt(i) - 'a';
            if (cur.next[slot] == null) cur.next[slot] = new Node();
            cur = cur.next[slot];
        }
        cur.word = true;
    }

    boolean search(String pattern) {
        return dfs(root, pattern, 0);
    }

    private boolean dfs(Node node, String pattern, int pos) {
        if (pos == pattern.length()) return node.word;
        char c = pattern.charAt(pos);
        if (c != '.') {
            Node child = node.next[c - 'a'];
            return child != null && dfs(child, pattern, pos + 1);
        }
        for (Node child : node.next) {
            if (child != null && dfs(child, pattern, pos + 1)) return true;
        }
        return false;
    }
}
```

A pattern with no blanks follows one route, so it costs O(L). With blanks, the work is bounded by the number of nodes of the trie that agree with the pattern prefix at each position, which never exceeds the total number of nodes, so a question costs at most O(total letters stored).

<!-- stage: applicability -->
### When Some Squares Are Free

Use this search when stored words are matched against patterns where most squares are fixed and a few may take any value: crossword and word-game helpers, search boxes that allow a placeholder, and routing rules with a wildcard segment. The invariant is that a call at position i stands for the stored words that agree with the first i squares, so a fixed square can never lead to more than one child.

The false friend is branching at every square. Looping over all children at a written letter gives the right answer and turns a narrow search into a walk of the whole trie, with a cost that is the number of nodes instead of the pattern length. The wildcard is the only reason to leave a single edge. A second false friend is accepting at the end of the pattern without the flag, which would let `ba` match when only `bad` was stored.

The method has a no-go case. If almost every square is blank, the search visits most of the trie whatever the layout, and a scan over the words of the right length can be simpler and as fast. In Java, `'.' - 'a'` is a negative number, so the blank must be tested before the index is computed. Since the recursion is as deep as the pattern is long, a pattern of a few thousand squares is safe.

<!-- stage: exercises -->
### Exercises

#### [Build] One Final Wildcard (Author exercise)
<!-- id: tn-final-wildcard -->

**Prerequisites.** The insert and search lesson and its slot arrays.

**Problem.** Store a list of lowercase words. Each query is a lowercase string whose last character may be a dot, which stands for any single letter, and no other character is a dot. Return for each query whether some stored word matches it exactly, with the same length.

**Constraints.** 0 <= words.length <= 1000, 0 <= queries.length <= 1000, and every string has 1 to 20 characters.

**Example 1.** Input `words = ["cat", "car", "cow"]`, `queries = ["ca.", "co.", "cx.", "ca"]`, output `[true, true, false, false]`.

**Example 2.** Input `words = ["a"]`, `queries = [".", "a", "b", "a."]`, output `[true, true, false, false]`.

**Hint.** Walk the letters as usual, and at the last character look at every child of the node instead of one.

**Changed decision.** Only at the final character does the walk look at more than one child, and the flag decides each of those children.

#### [Vary] Multiple Wildcards (Author exercise)
<!-- id: tn-multiple-wildcards -->

**Prerequisites.** The One Final Wildcard rung and the recursive call over a node and a position.

**Problem.** Store distinct lowercase words. Each query may contain dots anywhere. Return for each query the alphabetically smallest stored word that matches it exactly in length, or the empty string if no word matches. Visit the children of a node in alphabetical order and stop at the first success.

**Constraints.** 0 <= words.length <= 1000, 0 <= queries.length <= 1000, and every string has 1 to 15 characters.

**Example 1.** Input `words = ["bad", "bed", "bid", "cod"]`, `queries = ["b.d", ".o.", "...", "b..."]`, output `["bad", "cod", "bad", ""]`.

**Example 2.** Input `words = ["zz", "za", "az"]`, `queries = [".z", "z.", ".."]`, output `["az", "za", "az"]`.

**Hint.** Which child is tried first at a blank, and what does the first success tell you about the word spelled by the path?

**Changed decision.** The call returns the word found instead of a boolean, and alphabetical order of the fan-out makes the first success the smallest word.

#### [Boundary] Wildcard At Root And Missing Length (Author exercise)
<!-- id: tn-wildcard-root-length -->

**Prerequisites.** The Multiple Wildcards rung and the end-of-pattern test.

**Problem.** Store distinct lowercase words. For each pattern, which may be all dots or start with a dot, return how many stored words match it. A word matches only if it has the same length as the pattern and agrees on every written letter. A longer word that merely begins like the pattern does not match.

**Constraints.** 0 <= words.length <= 1000, 0 <= patterns.length <= 1000, every string has 1 to 12 characters, and all words are different.

**Example 1.** Input `words = ["ab", "abc", "b"]`, `patterns = [".", "..", "...", "....", ".b"]`, output `[1, 1, 1, 0, 1]`.

**Example 2.** Input `words = ["aa", "ab", "ba"]`, `patterns = ["..", "a.", ".a", "a", "b."]`, output `[3, 2, 2, 0, 1]`.

**Hint.** What must be true of a node when the pattern is used up, and does the search still count the branches after one success?

**Changed decision.** The call adds up the results of all children instead of stopping at the first success, and counts only flagged nodes at exactly the pattern length.

#### [Recognize] Design Add and Search Words Data Structure (LeetCode 211)
<!-- id: tn-add-search-words -->

**Prerequisites.** The Wildcard At Root And Missing Length rung.

**Problem.** Design a dictionary that adds lowercase words and answers search commands whose pattern may contain dots. Run a script of the commands `add:w` and `search:p`, and return the answers of the search commands in order, each true when some added word matches the pattern letter for letter in the same length.

**Constraints.** Up to 3000 commands, and each word or pattern has 1 to 25 characters. Patterns contain only lowercase letters and dots.

**Example 1.** Input `commands = ["add:tin", "add:ton", "search:t.n", "search:tun", "search:..n", "search:t."]`, output `[true, false, true, false]`.

**Example 2.** Input `commands = ["add:a", "search:.", "search:a.", "search:b"]`, output `[true, false, false]`.

**Hint.** Which squares allow only one child, and which allow all of them?

**Changed decision.** A literal square follows a single edge and a dot loops over the existing children, so a fixed letter never widens the search.
