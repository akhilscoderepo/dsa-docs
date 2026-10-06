<!-- lesson-kind: standard -->
<!-- lesson-id: prefix-nodes -->
## Store Words By Shared Prefix

<!-- stage: context -->
### Why Every Keystroke Scans The Dictionary

A search box suggests product names while the user types. The program stores 200,000 names in a `HashSet<String>`. The user types `c`, then `ca`, then `car`, and after each keystroke the program must answer one question: does any stored name start with these letters?

A hash set answers whether one exact name is present, and it cannot answer this question. The program has to look at the names one by one. This lesson asks how a program stores words so that it answers a prefix question after reading only the letters of the prefix.

<!-- stage: naive -->
### Checking Every Stored Word

The direct plan keeps the words in a set. An exact query calls `contains`. A prefix query walks over all words and calls `startsWith` on each.

```java
static boolean hasPrefixByScan(Set<String> words, String prefix) {
    for (String w : words) {                          // visits every stored word
        if (w.startsWith(prefix)) return true;        // compares up to prefix.length() characters
    }
    return false;                                     // no word starts with the prefix
}
```

The method returns the right answer for every prefix, including the empty prefix. It repeats the same character comparisons for every keystroke, and it stores `car` and `cat` as two separate strings that both begin with `ca`.

<!-- stage: bottleneck -->
### Counting The Comparisons Per Keystroke

```predict
The set holds n = 200,000 words and the user types a prefix of 5 letters. Roughly how many character comparisons can one query make, and how many of them could the program have skipped?

A query that finds no match compares up to 5 characters against each of the 200,000 words, so about one million comparisons. Almost all of them test words that already failed on the first letter, so a program that stores the letters once could skip them.
```

A prefix query on the set costs O(n * m) time, where `n` is the number of words and `m` is the prefix length. The cost grows with the dictionary, although the answer depends only on the few words that share the prefix. A prefix typed one letter at a time pays this cost again after every keystroke.

The storage has the same flaw. Every word repeats the letters of its prefix, and the set cannot tell that `car` and `cat` agree on `ca`. The program needs one structure where words with the same prefix share the same stored letters.

<!-- stage: insight -->
### Letting Words Share One Path

A **prefix tree**, also called a trie, stores each distinct prefix once. The root represents the empty prefix. Each node has children, and each child is reached by one character. The characters on the path from the root to a node spell the prefix that the node represents.

#### One Node Per Prefix

The words `car` and `cat` both begin with `c` and `ca`. The tree has one node for `c` and one node for `ca`, and these two **shared nodes** serve both words. The tree then splits into the nodes for `car` and `cat`. A prefix query follows the letters of the prefix from the root. If an edge is missing, no stored word has this prefix. If the walk ends on a node, some stored word has this prefix, and the query read only `m` characters.

#### Marking Where A Word Ends

A node that lies on a path is not always a stored word. The word `car` passes through the node for `ca`, but `ca` is not a stored word. Each node therefore carries a **terminal flag**, which is true only when a stored word ends at this node. The path decides whether a prefix exists. The flag decides whether the prefix is also a whole word.

<!-- names: prefix tree, shared nodes, terminal flag -->

<!-- stage: variables -->
### The Pieces Of State

A node and a walk need four pieces of state, and only the node pieces survive between queries.

- **Children** map each character to the child node that the character selects.
- **Terminal flag** is true when a stored word ends at the node.
- **Pass count** is the number of inserted words whose path goes through the node, and the lesson uses it in the second exercise.
- **Current node** is the node reached after reading the first `i` characters of the word under test.

An insert changes the children and the pass counts along its path and sets the flag on its last node. A query changes nothing.

<!-- stage: trace -->
### Walking The Tree Letter By Letter

#### Inserting A Word That Shares A Prefix

The first trace inserts `cat` into a tree that already holds `car`. The pointer `i` marks the character under test, the variable `prefix` shows the prefix of the current node, and `nodes` counts the nodes below the root.

The letters `c` and `a` already have edges, so the insert reuses both nodes and creates nothing. The letter `t` has no edge below `ca`, so the insert creates one node and sets its flag, because the word ends there. The tree grows by one node for a word of three letters.

#### Querying A Prefix That Is Not A Word

The second trace queries `car` in the tree that holds `card` and `care`. The walk reaches the node for `car` after three steps. A prefix query returns true, because the node exists. An exact query returns false, because the flag of this node is false.

#### Stepping Through Both Walks

```trace
{"cells":["c","a","t"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"prefix":"c","nodes":3},"note":"The node for c already exists, so the insert reuses it and creates nothing."},{"at":{"i":1},"vars":{"prefix":"ca","nodes":3},"note":"The node for ca already exists, so the insert reuses it and creates nothing."},{"at":{"i":2},"vars":{"prefix":"cat","nodes":4},"note":"The node for cat is missing, so the insert creates it. The word ends here, so the terminal flag becomes true."}]}
```

```trace
{"cells":["c","a","r"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"prefix":"c","flag":"false"},"note":"The edge c exists, so the walk reaches the node for c."},{"at":{"i":1},"vars":{"prefix":"ca","flag":"false"},"note":"The edge a exists, so the walk reaches the node for ca."},{"at":{"i":2},"vars":{"prefix":"car","flag":"false"},"note":"The edge r exists, so the walk reaches the node for car. The node exists, so startsWith returns true. The terminal flag is false, so search returns false."}]}
```

<!-- stage: code -->
### Writing The Tree In Java

#### The Node And The Insert

Each node stores its children in a `HashMap<Character, Node>`, so any character is allowed. The insert walks from the root and creates a child only when the edge is missing.

```java
final class PrefixTree {
    private static final class Node {
        final Map<Character, Node> next = new HashMap<>();   // child selected by one character
        boolean terminal;                                    // true when a stored word ends here
        int pass;                                            // inserted words through this node
    }

    private final Node root = new Node();

    void insert(String word) {
        Node cur = root;
        for (int i = 0; i < word.length(); i++) {            // one step per character
            cur = cur.next.computeIfAbsent(word.charAt(i), c -> new Node());  // create only a missing child
            cur.pass++;                                      // this word passes through the child
        }
        cur.terminal = true;                                 // the last node marks the word end
    }

    private Node walk(String s) {
        Node cur = root;
        for (int i = 0; i < s.length() && cur != null; i++) {
            cur = cur.next.get(s.charAt(i));                 // null when the edge is missing
        }
        return cur;                                          // the node for s, or null
    }

    boolean search(String word) { Node n = walk(word); return n != null && n.terminal; }
    boolean startsWith(String prefix) { return walk(prefix) != null; }
}
```

#### Cost Of One Operation

An insert, a search and a prefix query each visit at most one node per character. Each costs O(m) time for a word of `m` characters, and the cost does not depend on how many words are stored. The tree uses O(total characters) memory in the worst case, and shared prefixes reduce it.

<!-- stage: applicability -->
### Recognizing A Prefix Question

#### Spotting The Pattern

The cue is a set of strings where many share a start and the program asks again and again whether some string begins with given letters. The invariant is that the path from the root spells exactly one prefix, and the terminal flag is separate from the existence of that path.

#### Finding The False Friend

The false friend is the hash set. It answers whole-word membership in O(m) expected time, and the tree matches it. The set cannot answer a prefix question without a scan, because it stores no information about the prefixes of a word.

A second false friend is a sorted array with binary search. It also answers a prefix question, in O(m log n), and it needs no nodes. It cannot add words cheaply, and the tree adds a word in O(m).

#### Recognizing The No-Go Cases

The tree does not fit when the program asks only whole-word membership, because a hash set uses less memory. It also does not fit when words share almost no prefixes and the alphabet is large, because each node then holds a map for a single child.

<!-- stage: exercises -->
### Exercises

#### [Build] Store Shared Prefixes (Author exercise)
<!-- id: tr-store-shared-prefixes -->

**Prerequisites.** The prefix tree and the insert of this lesson.

**Problem.** Given an array `words` of lowercase strings, insert every word into an empty prefix tree and return the number of nodes below the root. A node exists once for each distinct nonempty prefix of the words. Equal words create the nodes only once.

**Constraints.** The limits are:
- **Count** is `0 <= words.length <= 10^4`.
- **Length** of each word is `0 <= length <= 50`.
- **Characters** are lowercase English letters.
- **Mutation** does not occur; `words` keeps its order.

**Example 1.** Input `words = ["car","cat"]`, output 4.

**Example 2.** Input `words = ["a","a","ab"]`, output 2.

**Hint.** Which letters of a new word already have an edge? What changes in the node count when an edge is missing?

**Changed decision.** The method counts the created nodes and does not answer queries.

#### [Vary] Prefix Count (Author exercise)
<!-- id: tr-prefix-count -->

**Prerequisites.** The previous exercise.

**Problem.** Given an array `words` of lowercase strings and an array `prefixes`, return an array where position `j` holds the number of entries of `words` that start with `prefixes[j]`. An entry that appears twice counts twice. The empty prefix counts every entry.

**Constraints.** The limits are:
- **Count** is `0 <= words.length, prefixes.length <= 10^4`.
- **Length** of each string is `0 <= length <= 50`.
- **Characters** are lowercase English letters.
- **Mutation** does not occur; both arrays keep their order.

**Example 1.** Input `words = ["car","cat","cart","dog"]` and `prefixes = ["ca","car","d","x"]`, output `[3,2,1,0]`.

**Example 2.** Input `words = ["ab","ab"]` and `prefixes = ["","ab","abc"]`, output `[2,2,0]`.

**Hint.** How many inserted words go through a node? Where does a word with length 0 leave its trace?

**Changed decision.** Each node stores a count, and the terminal flag is not read.

#### [Boundary] Empty Word And Prefix-Only Node (Author exercise)
<!-- id: tr-empty-word-prefix-only -->

**Prerequisites.** The two exercises above.

**Problem.** Given an array `words` and an array `queries`, return for each query one status. The status is 2 when the query equals an entry of `words`, 1 when the query is not an entry but some entry starts with it, and 0 otherwise. The empty string is an entry only when `words` contains it. With no entries at all, every query has status 0.

**Constraints.** The limits are:
- **Count** is `0 <= words.length, queries.length <= 10^4`.
- **Length** of each string is `0 <= length <= 50`.
- **Characters** are lowercase English letters.
- **Mutation** does not occur; both arrays keep their order.

**Example 1.** Input `words = ["app","apple"]` and `queries = ["ap","app","apple","applez"]`, output `[1,2,2,0]`.

**Example 2.** Input `words = ["x"]` and `queries = ["","x","y"]`, output `[1,2,0]`.

**Hint.** Which node does the empty query reach? When can a node exist while its flag is false?

**Changed decision.** The method reads the path and the flag as two separate facts.

#### [Recognize] Implement Trie (LeetCode 208)
<!-- id: tr-implement-trie-map -->

**Prerequisites.** The previous three exercises.

**Problem.** Design a class with `insert(word)`, `search(word)` and `startsWith(prefix)`. The method `search` returns true only when the exact word was inserted before. The method `startsWith` returns true when an inserted word begins with the prefix. Strings may hold any `char`, so the class stores its children in a map.

**Constraints.** The limits are:
- **Length** of each string is `1 <= length <= 2000`.
- **Characters** are any `char` values, such as uppercase letters or digits.
- **Calls** number at most `3 * 10^4` in total.
- **Mutation** does not occur; the input strings stay unchanged.

**Example 1.** Input calls `insert("Go")`, `search("G")`, `startsWith("G")`, `search("Go")`, output `false`, `true`, `true` for the last three calls.

**Example 2.** Input calls `search("a")` and `startsWith("a")` on an empty tree, output `false` and `false`.

**Hint.** What does a query that stops on a node with a false flag report for each of the two methods?

**Changed decision.** Children live in a map, so the lowercase assumption of an array does not apply.
