<!-- lesson-kind: standard -->
<!-- lesson-id: prefix-nodes -->
## Prefix Nodes

<!-- stage: context -->
### The Catalogue Drawers Of Cedar Library

Cedar Library keeps a wooden catalogue of the words its readers have asked about. One drawer holds the cards for every word beginning with the same letter, and inside a drawer, small dividers split the cards again by the second letter, then the third. The clerk asks the cabinet two kinds of questions all day. Has this exact word ever been requested? And is there any requested word that begins with these letters, so that a reader typing `ca` can be shown suggestions?

The words `car`, `cart`, `card` and `care` crowd together, and the clerk can see that the letters `c`, `a`, `r` are the same on all four cards. She would like the cabinet itself to remember that shared beginning once, instead of every card repeating it.

<!-- stage: naive -->
### Keep A Flat Pile Of Cards

The direct method keeps every requested word in one flat list. An exact question compares the asked word against each card. A beginning question checks each card to see whether it starts with the asked letters, and stops at the first card that does.

```java
static boolean anyStartsWith(List<String> cards, String letters) {
    for (String card : cards) {
        if (card.startsWith(letters)) return true;
    }
    return false;
}
```

The method is easy to trust, because it follows the question word for word, and it answers correctly for any collection of cards whatever the order. A hash set would speed up the exact question, yet the beginning question would still need this scan.

<!-- stage: bottleneck -->
### Every Query Rereads Shared Letters

With n cards of average length L, one beginning question costs O(n * L) in the worst case, which happens whenever the answer is no or the matching card sits near the end. Ten thousand questions against a hundred thousand cards of length ten can mean ten billion letter comparisons. The expensive part is not the cards that fail on their first letter. It is the large crowd of cards that share a long beginning, since `c`, `a`, `r` is compared again for `car`, `cart`, `card` and `care`, and again for the next question.

A flat pile also cannot tell the clerk anything about a beginning as a thing in its own right. `ca` is not stored anywhere, so every question about it must be rebuilt from the cards. A structure that stores each beginning once could answer by walking one letter at a time, at a cost of O(L) per question, whatever the number of cards.

<!-- stage: insight -->
### One Node For Every Beginning

Give every distinct beginning that occurs in the collection exactly one **prefix node**. The empty beginning is the root. The node for `ca` is reached from the root by the edge `c` and then the edge `a`, so the route of edges from the root spells the beginning the node stands for, and two different routes can never reach the same node. Words that share a beginning share the first part of their route, which is the whole saving.

A card exists for `car` only if the route `c`, `a`, `r` ends at a node that was marked on purpose. That mark is the **terminal flag**, and it is separate from the existence of the node. The node for `ca` exists because `car` passes through it, yet no word `ca` was stored, so its terminal flag stays false. An exact question must find the node and read the flag. A beginning question only needs the node to exist.

A third piece of state, the **pass count**, records how many inserted words went through the node. A node with a pass count above zero is exactly a beginning of some stored word, which gives the beginning question a second way to be answered and gives counting questions their answer for free.

The invariant is that the route from the root to any node spells exactly one beginning, and the flag of that node records whether that beginning was itself stored as a word.

<!-- names: prefix node, terminal flag, pass count -->

<!-- stage: variables -->
### Root, Children, Flag And Count

The `root` is created once and stands for the empty beginning. Each node owns `children`, a map from a character to the next node, which changes only when an insertion needs an edge that is missing. A boolean `terminal` is set once, at the node where an inserted word ends. An integer `pass` goes up by one at every node an insertion touches, including the root, so `root.pass` equals the number of insertions. A walker variable `cur` starts at the root and moves one edge per character.

<!-- stage: trace -->
### Two Words Sharing A Beginning

The first trace inserts `car` into an empty trie. The pointer `i` marks the letter being consumed, and the last step sits one past the final letter, where the word ends and its flag is set. The count `nodes` includes the root. Every letter finds no edge, so each step creates a node and moves onto it.

```trace
{"cells":["c","a","r"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"nodes":2,"pass":1,"made":"yes"},"note":"The letter c has no edge yet, so a new node is made for the beginning c and the walk moves onto it."},{"at":{"i":1},"vars":{"nodes":3,"pass":1,"made":"yes"},"note":"The letter a has no edge yet, so a new node is made for the beginning ca and the walk moves onto it."},{"at":{"i":2},"vars":{"nodes":4,"pass":1,"made":"yes"},"note":"The letter r has no edge yet, so a new node is made for the beginning car and the walk moves onto it."},{"at":{"i":3},"vars":{"nodes":4,"pass":1,"made":"no"},"note":"The word car ends here, so the flag of this node is set and the trie holds 4 nodes with the root."}]}
```

The second trace inserts `cat` into the trie that already holds `car`. Watch the first two steps, which find the edges `c` and `a` waiting and only move along them, with the pass count of the reached node going up. Only the third letter has no edge, so a single new node is made, and the node total grows by one instead of three.

```trace
{"cells":["c","a","t"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"nodes":4,"pass":2,"made":"no"},"note":"The letter c already has an edge, so the walk moves onto the existing node for c and its pass count rises to 2."},{"at":{"i":1},"vars":{"nodes":4,"pass":2,"made":"no"},"note":"The letter a already has an edge, so the walk moves onto the existing node for ca and its pass count rises to 2."},{"at":{"i":2},"vars":{"nodes":5,"pass":1,"made":"yes"},"note":"The letter t has no edge yet, so a new node is made for the beginning cat and the walk moves onto it."},{"at":{"i":3},"vars":{"nodes":5,"pass":1,"made":"no"},"note":"The word cat ends here, so the flag of this node is set and the trie holds 5 nodes with the root."}]}
```

<!-- stage: code -->
### A Trie With Flags And Counts

```java
final class PrefixTrie {
    static final class Node {
        final Map<Character, Node> children = new HashMap<>();
        boolean terminal;
        int pass;
    }

    private final Node root = new Node();

    void insert(String word) {
        Node cur = root;
        cur.pass++;
        for (int i = 0; i < word.length(); i++) {
            cur = cur.children.computeIfAbsent(word.charAt(i), c -> new Node());
            cur.pass++;
        }
        cur.terminal = true;
    }

    private Node walk(String letters) {
        Node cur = root;
        for (int i = 0; i < letters.length() && cur != null; i++) {
            cur = cur.children.get(letters.charAt(i));
        }
        return cur;
    }

    boolean contains(String word) {
        Node end = walk(word);
        return end != null && end.terminal;
    }

    int countBeginningWith(String letters) {
        Node end = walk(letters);
        return end == null ? 0 : end.pass;
    }
}
```

The children are stored in a map keyed by `Character`, so the structure works for any characters. Insertion and every question walk one edge per letter, which is O(L) time for a word of length L, and the whole structure holds at most one node per distinct beginning.

<!-- stage: applicability -->
### Repeated Beginnings And Beginning Questions

Reach for prefix nodes when many strings share beginnings and the questions are about beginnings: autocomplete lists, spell checkers that prune on a dead beginning, routing tables keyed by address prefixes, and dictionaries probed letter by letter. The invariant to keep in sight is that one route spells one beginning, and a word exists only where the flag says so.

The nearest false friend is the hash set of words. It answers whole-word membership in expected constant time, but it cannot answer whether any word begins with `ca`, because `ca` was never stored. Storing every beginning of every word in a second set repairs the answer and costs L entries per word, with no sharing and no counts. A second false friend is treating a node's existence as a stored word, which makes `ca` look like a word as soon as `car` is inserted.

There is no benefit when strings share few beginnings and only whole-word lookups are needed, since the nodes then cost more memory than a set. In Java, a `HashMap<Character, Node>` per node is heavy, so the memory is much larger than the text itself. Use `computeIfAbsent` to create an edge only when it is missing, so an existing subtree is never replaced.

<!-- stage: exercises -->
### Exercises

#### [Build] Store Shared Prefixes (Author exercise)
<!-- id: tn-shared-prefixes -->

**Prerequisites.** The idea of a node that stands for one beginning.

**Problem.** Distinct lowercase words are inserted into an empty trie in the given order. Return `[nodes, shared]`, where `nodes` counts the nodes other than the root and `shared` counts those non-root nodes that lie on the routes of at least two of the words.

**Constraints.** 0 <= words.length <= 500, each word has 1 to 20 lowercase letters, and no word repeats.

**Example 1.** Input `words = ["car", "cat"]`, output `[4, 2]`.

**Example 2.** Input `words = ["dog", "do", "dot"]`, output `[4, 2]`.

**Hint.** Which letters of the second word find an edge already waiting, and what happens at a word that ends in the middle of another route?

**Changed decision.** A node is created only when the walk meets a missing edge, so the node total is the number of distinct nonempty beginnings.

#### [Vary] Prefix Count (Author exercise)
<!-- id: tn-prefix-count -->

**Prerequisites.** The Store Shared Prefixes rung and the idea of a pass count.

**Problem.** A script of commands is run on an initially empty trie. The command `insert:w` adds the word `w`, and inserting the same word twice counts it twice. The command `count:p` reports how many insertions so far were of a word that begins with `p`. Return the answers of the `count` commands in order.

**Constraints.** 0 <= commands.length <= 2000, and every word and every beginning has 1 to 12 lowercase letters.

**Example 1.** Input `commands = ["insert:apple", "insert:apply", "insert:ape", "count:ap", "count:app", "count:b"]`, output `[3, 2, 0]`.

**Example 2.** Input `commands = ["insert:a", "insert:a", "count:a", "count:ab"]`, output `[2, 0]`.

**Hint.** Which nodes does one insertion touch, and what must a missing route report?

**Changed decision.** Instead of reading a flag, the answer is the pass count of the node where the question ends, and zero when the route is missing.

#### [Boundary] Empty Word And Prefix-Only Node (Author exercise)
<!-- id: tn-empty-and-prefix-only -->

**Prerequisites.** The Prefix Count rung and the separation of flag from existence.

**Problem.** Run a script on an empty trie with the commands `insert:w`, `search:w` and `prefix:p`, where `w` and `p` may be empty. A `search` is true only if exactly that word was inserted. A `prefix` is true only if some inserted word begins with `p`, so on a trie with no words even the empty `p` gives false. Return the results of the `search` and `prefix` commands in order.

**Constraints.** 0 <= commands.length <= 2000, and each word or beginning has 0 to 10 lowercase letters.

**Example 1.** Input `commands = ["prefix:", "search:", "insert:", "search:", "prefix:", "search:x"]`, output `[false, false, true, true, false]`.

**Example 2.** Input `commands = ["insert:car", "prefix:", "search:", "prefix:ca", "search:ca", "search:car"]`, output `[true, false, true, false, true]`.

**Hint.** Is the root a stored word merely because it exists, and which number tells whether any word passed through it?

**Changed decision.** Existence of a node is judged by its pass count, never by the node object, and only the terminal flag decides an exact answer.

#### [Recognize] Implement Trie (LeetCode 208)
<!-- id: tn-implement-trie -->

**Prerequisites.** The Empty Word And Prefix-Only Node rung.

**Problem.** Support three operations on a collection of lowercase words: add a word, ask whether a word was added exactly, and ask whether any added word begins with a given string. Run a script of the commands `insert:w`, `search:w` and `startsWith:p`, and return the results of the last two kinds in order.

**Constraints.** Up to 3000 commands, and every string has 1 to 2000 lowercase letters.

**Example 1.** Input `commands = ["insert:apple", "search:apple", "search:app", "startsWith:app", "insert:app", "search:app"]`, output `[true, false, true, true]`.

**Example 2.** Input `commands = ["insert:ab", "startsWith:b", "search:abc", "startsWith:ab"]`, output `[false, false, true]`.

**Hint.** Which of the three commands needs the flag, and which only needs the route to exist?

**Changed decision.** Exact and beginning questions walk the same route and differ only in whether the final node must be flagged.
