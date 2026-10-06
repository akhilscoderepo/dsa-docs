<!-- lesson-kind: standard -->
<!-- lesson-id: insert-and-search -->
## Insert And Look Up Words

<!-- stage: context -->
### Why The Tree Crashes On Capital Letters

A signup form stores banned usernames in a prefix tree. Each node holds an array of 26 child references, one for each lowercase letter. The program inserts `admin` and `root` and works. A user then types `Admin` with a capital letter, and the program throws `ArrayIndexOutOfBoundsException`, because `'A' - 'a'` equals -32.

The crash comes from how the program turns a character into a child position and from what it assumes about the input. This lesson asks how an insert and a search move through the tree one character at a time, and what the program must state about the characters before it uses an array.

<!-- stage: naive -->
### Copying The Rest Of The Word

The direct plan writes the insert as a recursion on the remaining word. Each call takes the first character and passes the rest of the word to the child.

```java
static final class Node {
    final Map<Character, Node> next = new HashMap<>();   // one map per node
    boolean terminal;
}

static void insertByCopy(Node node, String rest) {
    if (rest.isEmpty()) { node.terminal = true; return; }            // the word ends at this node
    Node child = node.next.computeIfAbsent(rest.charAt(0), c -> new Node());
    insertByCopy(child, rest.substring(1));                          // copies the remaining characters
}
```

The method inserts every word correctly. Each call copies the rest of the word, and each node allocates a map, even when the node has one child.

<!-- stage: bottleneck -->
### Measuring The Copies And The Memory

```predict
A word has m = 1,000 characters. About how many characters do all the substring copies in one insert move, and how much memory does the tree allocate for one new node?

The calls copy 999, then 998, then 997 characters, and so on, about m * m / 2 = 500,000 characters in total. Each new node also allocates a map object, and the map stores boxed characters, so a node costs far more than one reference.
```

The copies make one insert cost O(m^2) time, although the walk itself needs only O(m). The recursion has no reason to build new strings. It needs to know which character comes next, and an integer position in the original word already says that.

The maps add a second cost. A hash map allocates a table and boxes each key, so a node with one child pays for storage that a small fixed array avoids. When the alphabet is known and small, a fixed array reaches the child by arithmetic and needs no lookup structure.

<!-- stage: insight -->
### Walking With An Index Into The Word

The insert and the search keep a **character index** `i` into the original word. After `i` characters, the current node represents `word[0..i)`, which is the prefix of length `i`. Both operations loop over `i` from 0 to the word length and never build a new string.

#### Choosing The Next Edge

When the contract says that every character is a lowercase English letter, each node holds a **child array** of 26 slots. The character `c` selects the slot at the **index offset** `c - 'a'`, so `'a'` maps to 0 and `'z'` maps to 25. An empty slot holds `null`. The insert creates a node when the slot is empty. The search stops with failure when the slot is empty, because no stored word has this prefix.

#### Stating The Alphabet

The array version is correct only inside its contract. A character outside `'a'` to `'z'` gives an offset that is negative or above 25. The program must either state that such input never occurs or check each character before it uses the offset. A map keyed by `Character` removes the assumption, and it costs more memory.

<!-- names: character index, child array, index offset -->

<!-- stage: variables -->
### The Pieces Of State

One loop and one node type hold all state.

- **Index i** is the number of characters of the word that the walk has consumed.
- **Current node** is the node that represents the first `i` characters.
- **Slot** is the position `word.charAt(i) - 'a'` inside the child array of the current node.
- **Terminal flag** is true when a stored word ends at the node, and only an exact search reads it.

The index grows by one at every step. The current node changes to the child in the slot, or the operation ends when the slot is empty and the operation is a search.

<!-- stage: trace -->
### Following The Index Through A Word

#### Inserting A Longer Word

The first trace inserts `apple` into a tree that already holds `app`. The pointer `i` marks the character under test, `slot` shows the array position, and `created` counts the nodes that the insert has created so far.

The first three characters reach existing nodes, so `created` stays 0. The character `l` finds an empty slot, and the insert creates a node. The character `e` does the same, and the last node receives the terminal flag. The node for `app` keeps its own flag, so the two words stay distinct.

#### Searching A Missing Word

The second trace searches `apx` in the tree that holds `app` and `apple`. The walk follows `a` and `p`, and the character `x` selects slot 23, which is empty. The search stops at once and returns false. It reads three characters and never looks at the rest of the tree.

#### Stepping Through Both Walks

```trace
{"cells":["a","p","p","l","e"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"slot":0,"created":0},"note":"The slot 0 for a holds a node, so the insert moves into the node for a."},{"at":{"i":1},"vars":{"slot":15,"created":0},"note":"The slot 15 for p holds a node, so the insert moves into the node for ap."},{"at":{"i":2},"vars":{"slot":15,"created":0},"note":"The slot 15 for p holds a node, so the insert moves into the node for app."},{"at":{"i":3},"vars":{"slot":11,"created":1},"note":"The slot 11 for l is empty, so the insert creates the node for appl."},{"at":{"i":4},"vars":{"slot":4,"created":2},"note":"The slot 4 for e is empty, so the insert creates the node for apple. The word ends here, so the terminal flag becomes true."}]}
```

```trace
{"cells":["a","p","x"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"slot":0,"found":"yes"},"note":"The slot 0 for a holds a node, so the search moves into the node for a."},{"at":{"i":1},"vars":{"slot":15,"found":"yes"},"note":"The slot 15 for p holds a node, so the search moves into the node for ap."},{"at":{"i":2},"vars":{"slot":23,"found":"no"},"note":"The slot 23 for x is empty, so no stored word starts with apx. The search returns false and reads no more characters."}]}
```

<!-- stage: code -->
### Writing The Walk In Java

#### The Insert And The Search

The class below assumes that every character is a lowercase English letter. The helper `slot` reports the offset, and the public methods read it for each character.

```java
final class LowerTrie {
    private static final class Node {
        final Node[] child = new Node[26];             // one slot for each letter, null when absent
        boolean terminal;                              // true when a stored word ends here
    }

    private final Node root = new Node();

    private static int slot(char c) { return c - 'a'; }   // 'a' maps to 0 and 'z' maps to 25

    void insert(String word) {
        Node cur = root;
        for (int i = 0; i < word.length(); i++) {      // one step per character, no substring
            int s = slot(word.charAt(i));
            if (cur.child[s] == null) cur.child[s] = new Node();   // create only a missing edge
            cur = cur.child[s];
        }
        cur.terminal = true;                           // the last node marks the word end
    }

    boolean search(String word) {
        Node cur = root;
        for (int i = 0; i < word.length() && cur != null; i++) cur = cur.child[slot(word.charAt(i))];
        return cur != null && cur.terminal;            // exact words need the flag
    }

    boolean startsWith(String prefix) {
        Node cur = root;
        for (int i = 0; i < prefix.length() && cur != null; i++) cur = cur.child[slot(prefix.charAt(i))];
        return cur != null;                            // a prefix needs only the path
    }
}
```

#### Cost Of The Array

Each operation costs O(m) time for a string of `m` characters, with no copies. Each node holds 26 references even when it has one child. The tree uses O(26 * N) memory for `N` nodes, which is O(N) with a large constant.

<!-- stage: applicability -->
### Recognizing A Character-By-Character Walk

#### Spotting The Pattern

The cue is an operation that reads one character at a time and either creates a missing edge or fails when the edge is absent. The invariant is that after `i` characters the current node represents the first `i` characters of the word.

#### Finding The False Friend

The false friend is the string-copying recursion of the naive plan. It looks like the same walk, and it costs O(m^2) because every call builds a new string. A second false friend is the array applied to arbitrary text. It looks faster than a map, and it fails on the first character outside its alphabet.

#### Recognizing The No-Go Cases

The array does not fit when the alphabet is large or unknown, such as Unicode text, because each node would need thousands of slots. It does not fit when most nodes have one child, because 25 of the 26 slots then waste memory. A map per node fits those cases.

<!-- stage: exercises -->
### Exercises

#### [Build] Insert Lowercase Words (Author exercise)
<!-- id: tr-insert-lowercase-words -->

**Prerequisites.** The previous lesson and the index walk of this lesson.

**Problem.** Given an array `words` of lowercase strings, insert them in the given order into an empty tree that stores 26 child slots in each node. Return an array where position `j` holds the number of nodes that the insert of `words[j]` created.

**Constraints.** The limits are:
- **Count** is `0 <= words.length <= 10^4`.
- **Length** of each word is `0 <= length <= 50`.
- **Characters** are lowercase English letters only.
- **Mutation** does not occur; `words` keeps its order.

**Example 1.** Input `words = ["car","cat","car","ca"]`, output `[3,1,0,0]`.

**Example 2.** Input `words = ["b","","ba"]`, output `[1,0,1]`.

**Hint.** Which characters of the word find a non-null slot? What does the empty word do to the tree?

**Changed decision.** The array replaces the map, and the method reports the created nodes of each insert.

#### [Vary] Search Versus StartsWith (Author exercise)
<!-- id: tr-search-versus-starts-with -->

**Prerequisites.** The previous exercise.

**Problem.** Given arrays `words` and `queries` of lowercase strings and an array `exact` of booleans with the same length as `queries`, return a boolean array. Position `j` is true when `exact[j]` is true and `queries[j]` equals an entry of `words`, or when `exact[j]` is false and some entry of `words` starts with `queries[j]`.

**Constraints.** The limits are:
- **Count** is `0 <= words.length, queries.length <= 10^4`.
- **Length** of each string is `0 <= length <= 50`.
- **Characters** are lowercase English letters only.
- **Mutation** does not occur; the arrays keep their contents.

**Example 1.** Input `words = ["app","apple"]`, `queries = ["app","ap","apple","apples"]`, `exact = [true,true,false,false]`, output `[true,false,true,false]`.

**Example 2.** Input `words = ["a"]`, `queries = ["","a"]`, `exact = [false,true]`, output `[true,true]`.

**Hint.** Which of the two modes reads the terminal flag? What does the empty query reach in each mode?

**Changed decision.** The terminal flag matters only for the exact mode.

#### [Boundary] Word Is Prefix Of Another (Author exercise)
<!-- id: tr-word-is-prefix-of-another -->

**Prerequisites.** The two exercises above.

**Problem.** Given an array `words` and a string `query`, return the number of distinct entries of `words` that are a prefix of `query`. A string is a prefix of itself, and the empty string is a prefix of every string. Entries that appear twice count once.

**Constraints.** The limits are:
- **Count** is `0 <= words.length <= 10^4`.
- **Length** of each string is `0 <= length <= 50`.
- **Characters** are lowercase English letters only.
- **Mutation** does not occur; `words` keeps its order.

**Example 1.** Input `words = ["a","app","apple","app"]` and `query = "applesauce"`, output 3.

**Example 2.** Input `words = ["","b"]` and `query = "a"`, output 1.

**Hint.** Which nodes on the walk of the query carry a true flag? What happens when the walk of the query ends early?

**Changed decision.** The method counts flags along the path and does not look at the final node alone.

#### [Recognize] Implement Trie (LeetCode 208)
<!-- id: tr-implement-trie-array -->

**Prerequisites.** The previous three exercises.

**Problem.** Design a class over the alphabet `'a'` to `'z'` with `insert(word)`, `search(word)` and `startsWith(prefix)`. The method `insert` returns true when the word was not stored before, and false when it was. A string that holds any other character makes `insert` throw `IllegalArgumentException` and leave the tree unchanged. The same string makes `search` and `startsWith` return false.

**Constraints.** The limits are:
- **Length** of each string is `1 <= length <= 2000`.
- **Characters** may be any `char` value, and only `'a'` to `'z'` are valid.
- **Calls** number at most `3 * 10^4` in total.
- **Storage** uses an array of 26 slots in each node.

**Example 1.** Input calls `insert("dog")`, `insert("dog")`, `search("do")`, `startsWith("do")`, output `true`, `false`, `false`, `true`.

**Example 2.** Input calls `insert("Dog")`, `search("Dog")`, output an exception and then `false`, and the tree stays empty.

**Hint.** When must the program check every character of an insert? What state could a partial insert leave behind?

**Changed decision.** The array forces a domain check, and the check must run before the first node is created.
