<!-- lesson-kind: standard -->
<!-- lesson-id: wildcard-branching -->
## Match Words With Wildcards

<!-- stage: context -->
### Why A Blank Letter Slows The Search

A word-game helper holds a dictionary and answers patterns such as `c.t`, where the dot stands for any one letter. The program found `cat` and `cot` for this pattern and then received `c...e.`, which has four blanks. The player waits, because the program compares the pattern with every word in the dictionary.

A pattern with no blanks is cheap in a prefix tree, because each letter picks one edge. A blank breaks that rule. This lesson asks where a search must look at more than one child and where it can still follow one.

<!-- stage: naive -->
### Comparing The Pattern With Every Word

The direct plan keeps all words in a list. A query compares the pattern with each word of the same length, one character at a time.

```java
static boolean matchesByScan(List<String> words, String pattern) {
    for (String w : words) {
        if (w.length() != pattern.length()) continue;          // a match needs the same length
        boolean ok = true;
        for (int i = 0; i < w.length() && ok; i++) {
            ok = pattern.charAt(i) == '.' || pattern.charAt(i) == w.charAt(i);   // a dot accepts any letter
        }
        if (ok) return true;                                   // the first matching word ends the scan
    }
    return false;
}
```

The method is correct for every pattern. It reads each word again for every query, even when the first letter of the pattern is `c` and most words start with other letters.

<!-- stage: bottleneck -->
### Counting The Words That Cannot Match

```predict
The list holds 100,000 words of length 6, and the pattern is `cat...` with three fixed letters at the start. How many words can the scan skip safely, and how does the scan know?

Only the words that start with `cat` can match, and the scan has no way to find them without reading each word. A prefix tree finds them after reading three letters, because the path of `cat` leads only to those words.
```

A query on the list costs O(n * m) time for `n` words of length `m`. The scan treats a fixed letter and a blank alike, so it never uses the fixed letters to exclude words. The information that rules out a word is exactly the prefix that all candidates share, and the prefix tree stores that prefix once.

The tree keeps this benefit only if the search follows one edge at each fixed letter. It must look at several edges only where the pattern has a blank.

<!-- stage: insight -->
### Splitting The Search At Each Blank

The search is a recursive function of two values: a node and a position `i` in the pattern. The call represents every stored word that agrees with the first `i` characters of the pattern. It asks whether the rest of the pattern matches below the node.

#### Fixed Letters Use One Edge

When the pattern holds a letter at position `i`, only one child can continue a match. The call moves along that **single edge**. If the edge is missing, no stored word agrees with the prefix, and the call returns false without looking at any other child.

#### Blanks Try Every Child

When the pattern holds a dot at position `i`, every child of the node can continue a match. The call must **fan out** and call itself once for each child that exists, with position `i + 1`. These calls explore different words, so they do not repeat each other's work.

#### Stopping Early And Ending Exactly

The search can **short-circuit**. As soon as one child call returns true, the parent returns true and skips the remaining children. After the last pattern character the call returns the terminal flag of the node, because a match needs a word that ends exactly there. A pattern shorter than the word reaches a node with a false flag, and a pattern longer than the word runs out of children.

<!-- names: single edge, fan out, short-circuit -->

<!-- stage: variables -->
### The Pieces Of State

One recursive call carries three values, and the tree stays unchanged.

- **Node** is the position in the tree that represents the first `i` characters of the pattern.
- **Position i** is the index of the next pattern character to match.
- **Pattern character** is a letter that selects one child, or a dot that selects every child.
- **Terminal flag** is read only when `i` equals the pattern length.

A call to a child differs only in its node and in `i + 1`. The call writes nothing to the tree, so nothing needs to be undone when a call returns false.

<!-- stage: trace -->
### Following The Search Through Branches

#### A Blank That Needs Two Tries

The first trace searches `c.t` in a tree that holds `cap` and `cot`. The pointer `i` marks the position in the pattern, `node` shows the prefix of the current node, and `calls` counts the recursive calls so far.

The letter `c` has one edge. The dot at position 1 tries the children in alphabetical order. The child `a` leads to the node `ca`, where the letter `t` has no edge, so this branch fails. The search returns to position 1 and tries the child `o`. The node `co` has an edge for `t`, and the last node holds a flag, so the search returns true.

#### A Pattern That Is Too Long

The second trace searches `ca..` in a tree that holds only `cat`. The first dot reaches the node `cat`. The second dot needs a child, and the node has none, so the search returns false. A pattern must match the length of the word exactly.

#### Stepping Through Both Searches

```trace
{"cells":["c",".","t"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"node":"c","calls":1},"note":"The letter c has an edge, so the search moves to the node c."},{"at":{"i":1},"vars":{"node":"ca","calls":2},"note":"The dot tries the child a, which leads to the node ca."},{"at":{"i":2},"vars":{"node":"ca","calls":3},"note":"The node ca has no edge for t, so this branch returns false."},{"at":{"i":1},"vars":{"node":"co","calls":3},"note":"The dot tries the child o, which leads to the node co."},{"at":{"i":2},"vars":{"node":"cot","calls":4},"note":"The letter t has an edge, so the search moves to the node cot. The pattern ends on a node with a true flag, so the search returns true."}]}
```

```trace
{"cells":["c","a",".","."],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"node":"c","calls":1},"note":"The letter c has an edge, so the search moves to the node c."},{"at":{"i":1},"vars":{"node":"ca","calls":2},"note":"The letter a has an edge, so the search moves to the node ca."},{"at":{"i":2},"vars":{"node":"cat","calls":3},"note":"The dot tries the child t, which leads to the node cat."},{"at":{"i":3},"vars":{"node":"cat","calls":4},"note":"The dot needs a child, but the node cat has none, so the search returns false."}]}
```

<!-- stage: code -->
### Writing The Search In Java

#### The Recursive Match

The class stores lowercase words with a 26-slot array in each node. The method `match` handles a letter with one slot and a dot with a loop over the slots.

```java
final class WildTrie {
    private static final class Node {
        final Node[] child = new Node[26];             // one slot for each lowercase letter
        boolean terminal;                              // true when a stored word ends here
    }

    private final Node root = new Node();

    void add(String word) {
        Node cur = root;
        for (int i = 0; i < word.length(); i++) {
            int s = word.charAt(i) - 'a';
            if (cur.child[s] == null) cur.child[s] = new Node();
            cur = cur.child[s];
        }
        cur.terminal = true;
    }

    boolean search(String pattern) { return match(root, pattern, 0); }

    private boolean match(Node node, String p, int i) {
        if (i == p.length()) return node.terminal;                 // the pattern ended, so the word must end here
        char c = p.charAt(i);
        if (c != '.') {
            Node next = node.child[c - 'a'];                       // a letter follows one edge
            return next != null && match(next, p, i + 1);
        }
        for (Node next : node.child) {                             // a dot tries every existing child
            if (next != null && match(next, p, i + 1)) return true;   // the first success ends the search
        }
        return false;                                              // no child continued the match
    }
}
```

#### Cost Of One Search

The tree is never changed, so no step undoes anything. Each pair of a node and a position is visited at most once, because a node at depth `i` has only one path from the root. A search costs O(m) when the pattern has no dot, and it costs at most O(N) for a tree with `N` nodes when blanks fan out. The recursion needs O(m) stack space.

<!-- stage: applicability -->
### Recognizing A Pattern With Blanks

#### Spotting The Pattern

The cue is a query where most characters select one edge and a few characters accept any child. The invariant is that a call for a node and position `i` represents every stored word that agrees with the first `i` characters of the pattern.

#### Finding The False Friend

The false friend is a search that fans out at every character, including fixed letters. It returns the same answers, and it turns a narrow walk into a traversal of the whole tree. A second false friend is the regular expression engine applied to each stored word, which brings back the scan of the whole list.

#### Recognizing The No-Go Cases

The recursion does not fit when the pattern may contain a wildcard that matches any number of letters, such as `*`, because one position then explains many lengths and the same pair of node and position can repeat through different paths. It also does not fit when the word list is small, because the scan is simpler.

<!-- stage: exercises -->
### Exercises

#### [Build] One Final Wildcard (Author exercise)
<!-- id: tr-one-final-wildcard -->

**Prerequisites.** The prefix tree walk of the previous lessons.

**Problem.** The input is an array `words` of lowercase strings and a string `pattern`. Return true when some entry of `words` matches the pattern. The pattern has lowercase letters and may end with one dot. The dot matches exactly one letter. A match needs the same length as the pattern.

**Constraints.** The limits are:
- **Count** is `0 <= words.length <= 10^4`.
- **Length** of each string is `0 <= length <= 50`.
- **Pattern** holds lowercase letters, with at most one dot and only as its last character.
- **Mutation** does not occur; `words` keeps its order.

**Example 1.** Input `words = ["bad","dad"]` and `pattern = "da."`, output `true`.

**Example 2.** Input `words = ["tea","ten"]` and `pattern = "te"`, output `false`.

**Hint.** What does the walk do for every character before the dot? Which node holds the answer after the last letter?

**Changed decision.** A loop over the children happens once, at the last position, and needs no recursion.

#### [Vary] Multiple Wildcards (Author exercise)
<!-- id: tr-multiple-wildcards -->

**Prerequisites.** The previous exercise.

**Problem.** The inputs are `words`, an array of lowercase strings, and an array `patterns`. Return a boolean array. Position `j` is true when some entry of `words` matches `patterns[j]`. A pattern holds lowercase letters and dots, and a dot matches exactly one letter anywhere in the pattern.

**Constraints.** The limits are:
- **Count** is `0 <= words.length, patterns.length <= 10^4`.
- **Length** of each string is `0 <= length <= 50`.
- **Pattern** holds lowercase letters and dots, in any positions.
- **Mutation** does not occur; both arrays keep their contents.

**Example 1.** Input `words = ["cap","cot"]` and `patterns = ["c.t","c.p","..."]`, output `[true,true,true]`.

**Example 2.** Input `words = ["ab"]` and `patterns = [".b","a..","b."]`, output `[true,false,false]`.

**Hint.** Which children must the call try at a dot? When may the loop over the children stop?

**Changed decision.** Each dot spawns independent calls, and the first success ends the loop.

#### [Boundary] Wildcard At Root And Missing Length (Author exercise)
<!-- id: tr-wildcard-root-length -->

**Prerequisites.** The two exercises above.

**Problem.** Given an array `words` of lowercase strings and an array `patterns` that hold lowercase letters and dots, return for each pattern the number of distinct entries of `words` that match it. A word matches only when its length equals the length of the pattern. The empty pattern matches only the empty string.

**Constraints.** The limits are:
- **Count** is `0 <= words.length, patterns.length <= 10^3`.
- **Length** of each string is `0 <= length <= 20`.
- **Pattern** may start with a dot, may consist only of dots, or may be empty.
- **Mutation** does not occur; both arrays keep their contents.

**Example 1.** Input `words = ["ab","abc","ab"]` and `patterns = ["..","...",".","","a.c"]`, output `[1,1,0,0,1]`.

**Example 2.** Input `words = ["","z"]` and `patterns = ["","."]`, output `[1,1]`.

**Hint.** Which node does a pattern with a dot at position 0 start from? How do you count each distinct word only once?

**Changed decision.** The method counts every match, so no call may stop early, and the tree stores each word once.

#### [Recognize] Design Add and Search Words Data Structure (LeetCode 211)
<!-- id: tr-add-search-words -->

**Prerequisites.** The previous three exercises.

**Problem.** Design a class with `addWord(word)` and `search(word)`. The method `search` returns true when a word added so far matches the query. The query holds lowercase letters and dots, and a dot matches any single letter. Calls to `addWord` and `search` may alternate in any order.

**Constraints.** The limits are:
- **Length** of each word or query is `1 <= length <= 25`.
- **Words** passed to `addWord` hold lowercase letters only.
- **Dots** appear at most 2 times in each query.
- **Calls** number at most `10^4` in total.

**Example 1.** Input calls `addWord("bad")`, `addWord("mad")`, `search("pad")`, `search("b..")`, output `false`, `true` for the two searches.

**Example 2.** Input calls `search("a")` on an empty structure and then `addWord("a")`, `search(".")`, output `false` and then `true`.

**Hint.** What must a search return for a query that is longer than every stored word? Does an earlier search change the stored words?

**Changed decision.** Adds and searches interleave, so the tree must stay correct after every call.
