<!-- lesson-kind: combination -->
<!-- lesson-id: look-up-prefixes -->
## Look Up Prefixes In A Dictionary

<!-- stage: context -->
### Why A Search Index Rereads Every Root

A search index shortens each word of a document to its root before it stores the word. The root list holds 10,000 entries such as `cat`, `bat` and `rat`. The word `cattle` becomes `cat`, and the word `rattled` becomes `rat`. A word with no root stays as it is.

The first version tests every root against every word. A document of 100,000 words then triggers a billion prefix tests, and the index build takes minutes. This lesson asks how a program finds the shortest root of a word after reading only the letters of the word that matter.

<!-- stage: contributions -->
### What The Tree And Index Each Add

Two earlier ideas combine here. The string index from the string chapters gives the program the next letter of a word in O(1) time. A loop with a position `i` reads `word.charAt(i)` and never builds a substring. The index also tells the program when the word ends, so the program never reads past it.

The prefix tree from this chapter gives the program everything it needs to know about the dictionary after `i` letters. One node stands for all dictionary words that share the first `i` letters, so the program never revisits a root that already disagrees with the word. The terminal flag says whether a root ends at this node. Neither idea answers the question alone. The index reads the word without knowing the dictionary, and the tree holds the dictionary without knowing which word to read.

<!-- stage: naive -->
### Testing Each Root For Each Word

The direct plan takes the roots as a list and tests every root against every word. It keeps the shortest root that is a prefix of the word.

```java
static String shortestRootByScan(List<String> roots, String word) {
    String best = null;
    for (String r : roots) {                                  // visits every root for every word
        if (word.startsWith(r) && (best == null || r.length() < best.length())) {
            best = r;                                         // keeps the shortest matching root so far
        }
    }
    return best == null ? word : best;                        // a word with no root stays unchanged
}
```

The method returns the correct replacement for every word. It reads the roots again for each word, and it keeps testing roots after the first letters of the word have already ruled them out.

<!-- stage: bottleneck -->
### Counting The Tests Per Document

```predict
The document has 100,000 words and the list has 10,000 roots. How many startsWith tests does the scan run, and how many of them could a program skip after reading the first letter of a word?

The scan runs 100,000 * 10,000 = 10^9 tests. After the first letter of a word, only the roots that start with this letter can match, which is a small fraction of the list, so the program could skip almost all of the tests.
```

The scan costs O(w * r * m) time for `w` words, `r` roots and `m` letters. The cost multiplies the size of the document by the size of the dictionary, although a word matches at most a few roots. A substring plus a hash set does not help, because it builds and hashes a substring for every prefix length of every word.

The program needs a structure where one pass over the letters of a word shows every root that is a prefix of it. The prefix tree supplies exactly that path.

<!-- stage: insight -->
### Letting The Word Drive The Walk

The program stores the roots in a prefix tree and reads the word through the **string index** `i`. After `i` letters the walk stands on one node, and that node represents the **candidate set**, which is all roots that agree with the first `i` letters of the word. The set is never built as a list. The node stands for it.

#### Stopping At The First Terminal

The walk checks the terminal flag after each letter. A flag means that a root ends here, and this root is a prefix of the word. Because the walk reads letters in order, the first flagged node is the **first terminal** and its root is the shortest one. The walk stops and returns the first `i` letters. Every deeper root is longer and cannot replace it.

#### Stopping At A Missing Edge

If the next letter has no edge, the candidate set becomes empty. No root can match, so the walk stops and the word stays unchanged. If the word ends before any flag appears, the same rule applies. The cost is at most the length of the word, and it does not depend on the number of roots.

<!-- names: string index, candidate set, first terminal -->

<!-- stage: variables -->
### The Pieces Of State

The combined state fits in four pieces.

- **Tree** holds all roots, built once before any word is read.
- **Position i** is the number of letters of the word that the walk has consumed.
- **Current node** is the tree node for the first `i` letters of the word.
- **Answer** is the shortest root, which equals the first `i` letters at the first flagged node.

Each step increases `i` by one and moves the current node to a child. The walk never moves back, and it never changes the tree.

<!-- stage: trace -->
### Following Two Words Through The Roots

#### A Word With A Root

The first trace replaces `cattle`, with the roots `cat`, `bat` and `rat`. The pointer `i` marks the letter under test, and `node` shows the prefix of the current node.

The letters `c` and `a` follow edges. The letter `t` leads to a node with a true flag, so the walk stops after three letters and returns `cat`. The letters `tle` stay unread.

#### A Word Without A Root

The second trace replaces `carb`, with the roots `cat` and `cart`. The letters `c`, `a` and `r` follow edges, and none of these nodes has a flag. The letter `b` has no edge below `car`, so the candidate set is empty. The walk stops, and the word `carb` stays unchanged.

#### Stepping Through Both Words

```trace
{"cells":["c","a","t","t","l","e"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"node":"c"},"note":"The letter c has an edge, so the walk moves to the node c. The flag is false."},{"at":{"i":1},"vars":{"node":"ca"},"note":"The letter a has an edge, so the walk moves to the node ca. The flag is false."},{"at":{"i":2},"vars":{"node":"cat"},"note":"The letter t has an edge, so the walk moves to the node cat. The node has a true flag, so the walk stops and returns the root cat."}]}
```

```trace
{"cells":["c","a","r","b"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"node":"c"},"note":"The letter c has an edge, so the walk moves to the node c. The flag is false."},{"at":{"i":1},"vars":{"node":"ca"},"note":"The letter a has an edge, so the walk moves to the node ca. The flag is false."},{"at":{"i":2},"vars":{"node":"car"},"note":"The letter r has an edge, so the walk moves to the node car. The flag is false."},{"at":{"i":3},"vars":{"node":"car"},"note":"The node car has no edge for b, so the candidate set is empty. The word stays unchanged."}]}
```

<!-- stage: code -->
### Writing The Replacement In Java

#### The Walk With An Early Stop

The class stores the roots with a map in each node, so any character is allowed. The method `rootOf` returns the shortest root of a word, or the word itself.

```java
final class RootReplacer {
    private static final class Node {
        final Map<Character, Node> next = new HashMap<>();
        boolean terminal;                              // true when a root ends at this node
    }

    private final Node root = new Node();

    RootReplacer(List<String> roots) {
        for (String r : roots) {
            Node cur = root;
            for (int i = 0; i < r.length(); i++) cur = cur.next.computeIfAbsent(r.charAt(i), c -> new Node());
            cur.terminal = true;
        }
    }

    String rootOf(String word) {
        Node cur = root;
        for (int i = 0; i < word.length(); i++) {      // the word drives the walk, one letter per step
            cur = cur.next.get(word.charAt(i));
            if (cur == null) return word;              // no root agrees with these letters
            if (cur.terminal) return word.substring(0, i + 1);   // the first flag is the shortest root
        }
        return word;                                   // the word ended inside a root
    }
}
```

#### Cost Of One Word

The walk reads at most `m` letters for a word of length `m`, and it stops earlier at a root or a missing edge. A document of `w` words costs O(w * m) time after the tree is built, and the cost does not grow with the number of roots. The tree needs O(total length of roots) memory.

<!-- stage: applicability -->
### Recognizing A Prefix Lookup

#### Spotting The Pattern

The cue is a dictionary of strings and a stream of query strings, where the answer depends on which dictionary strings are prefixes of a query, or which have the query as a prefix. The invariant is that after `i` letters the current node stands for exactly the dictionary strings that agree with the first `i` letters of the query.

#### Finding The False Friend

The false friend is the hash set of roots tested on every prefix of the word. It builds a substring of each length and hashes it, so it costs O(m^2) for one word, and the tree needs only O(m). A second false friend is a loop that does not stop at the first flagged node. It returns the longest root, and the task asks for the shortest.

#### Recognizing The No-Go Cases

The tree does not fit when the dictionary changes rarely and only exact lookups occur, because a hash set is smaller and simpler. It also does not fit when queries are not read from the left, for example when roots are suffixes, unless the program stores the reversed words.

<!-- stage: exercises -->
### Exercises

#### [Build] Implement Trie (LeetCode 208)
<!-- id: tr-combo-longest-stored-prefix -->

**Prerequisites.** The first two lessons of this chapter.

**Problem.** Design a class with `insert(word)`, `search(word)`, `startsWith(prefix)` and `longestMatch(query)`. The method `longestMatch` returns the largest `k` such that the first `k` characters of `query` form a prefix of some inserted word. A query that shares no first character returns 0.

**Constraints.** The limits are:
- **Length** of each string is `1 <= length <= 2000`.
- **Characters** are lowercase English letters.
- **Calls** number at most `3 * 10^4` in total.
- **Mutation** does not occur; the input strings stay unchanged.

**Example 1.** Input calls `insert("planet")`, `longestMatch("plant")`, `longestMatch("zoo")`, output `4` and `0` for the two queries.

**Example 2.** Input calls `insert("ab")`, `startsWith("abc")`, `longestMatch("abc")`, output `false` and `2`.

**Hint.** Where does the walk of a query stop? How does this differ from the walk of `startsWith`?

**Changed decision.** A fourth method reports how deep a query goes, and a missing edge ends the walk without failing the call.

#### [Vary] Design Add and Search Words Data Structure (LeetCode 211)
<!-- id: tr-combo-smallest-match -->

**Prerequisites.** The previous exercise and the wildcard lesson.

**Problem.** Design a class with `addWord(word)` and `smallestMatch(pattern)`. The pattern holds lowercase letters and dots, and a dot matches any single letter. The method returns the lexicographically smallest added word that matches the pattern, or the empty string when no added word matches.

**Constraints.** The limits are:
- **Length** of each word or pattern is `1 <= length <= 25`.
- **Words** hold lowercase letters only.
- **Dots** may appear in any positions of a pattern.
- **Calls** number at most `10^4` in total.

**Example 1.** Input calls `addWord("mad")`, `addWord("bad")`, `addWord("bud")`, `smallestMatch(".ad")`, `smallestMatch("b.d")`, output `"bad"` and `"bad"`.

**Example 2.** Input calls `addWord("dog")`, `smallestMatch("do")`, `smallestMatch("d..")`, output `""` and `"dog"`.

**Hint.** In which order must the search try the children? What does the first success mean for the answer?

**Changed decision.** The search returns the word and not a boolean, and it tries the children in alphabetical order.

#### [Boundary] Replace Words (LeetCode 648)
<!-- id: tr-combo-replace-words -->

**Prerequisites.** The previous two exercises.

**Problem.** Given an array `roots` of nonempty lowercase strings and a sentence of words separated by single spaces, replace every word with the shortest root that is a prefix of it. A word with no root as a prefix stays unchanged. Return the new sentence with the same spaces.

**Constraints.** The limits are:
- **Roots** number `0 <= roots.length <= 1000`, with lengths from 1 to 100.
- **Sentence** has length `1 <= length <= 10^6`, with words of lowercase letters separated by single spaces.
- **Spaces** do not appear at the start or the end of the sentence.
- **Mutation** does not occur; the inputs keep their contents.

**Example 1.** Input `roots = ["cat","bat","rat"]` and `sentence = "the cattle was rattled by the battery"`, output `"the cat was rat by the bat"`.

**Example 2.** Input `roots = ["car","cart"]` and `sentence = "carbon carts"`, output `"car car"`.

**Hint.** What does the walk do at the first flagged node? What does the program return when a word ends before any flag?

**Changed decision.** The walk stops at the first terminal node, and a word without a root keeps its own letters.

#### [Recognize] Longest Word in Dictionary (LeetCode 720)
<!-- id: tr-combo-longest-built-word -->

**Prerequisites.** The three exercises above.

**Problem.** From an array `words` of lowercase strings, return the longest string `w` in `words` such that every nonempty prefix of `w` is also in `words`. When several strings have the longest length, return the lexicographically smallest one. Return the empty string when `words` is empty.

**Constraints.** The limits are:
- **Count** is `0 <= words.length <= 1000`.
- **Length** of each word is `1 <= length <= 30`.
- **Characters** are lowercase English letters.
- **Mutation** does not occur; `words` keeps its order.

**Example 1.** Input `words = ["w","wo","wor","worl","world","wom"]`, output `"world"`.

**Example 2.** Input `words = ["a","banana","app","appl","ap","apply","apple"]`, output `"apple"`.

**Hint.** Which nodes may the walk enter? How does the visiting order decide between two words of equal length?

**Changed decision.** The walk enters only children whose own flag is true, and ties go to the alphabetically earlier word.
