<!-- lesson-kind: standard -->
<!-- lesson-id: insert-and-search -->
## Insert And Search

<!-- stage: context -->
### The Sorting Room At The Harbour Post

At the harbour post office a clerk sorts parcels by the name of the destination town. Each town name arrives written on a label, and she reads it one letter at a time. Behind her stands a wall of pigeonholes. For the first letter there is a row of holes, one for each letter of the alphabet. Inside the hole for `p` hangs another row for the second letter, and so on. When a label reaches a hole that has nothing behind it, she hangs a fresh row there and carries on. When the label ends, she drops a small red token into the current hole, which says that a whole town stops here.

Later a courier asks about a town. The clerk reads the label letter by letter again. If she meets a hole with nothing behind it she answers no at once, and if she reaches the end she looks for the red token.

<!-- stage: naive -->
### Store Every Beginning As Its Own String

The direct method keeps two hash sets of strings, one for whole words and one for every beginning of every word. An insertion cuts the word into all of its beginnings and stores each one. An exact question looks in the first set, and a beginning question looks in the second.

```java
static void insert(String word, Set<String> words, Set<String> beginnings) {
    words.add(word);
    for (int k = 1; k <= word.length(); k++) {
        beginnings.add(word.substring(0, k));
    }
}
```

Both questions then cost one hash lookup, and the answers are right, since the second set holds exactly the nonempty beginnings that occur.

<!-- stage: bottleneck -->
### Copying Beginnings Costs Quadratic Text

Cutting a word of length L into L beginnings copies 1 + 2 + ... + L letters, so one insertion costs O(L^2) time and the stored text grows by the same amount. A word of two thousand letters stores about two million letters, though the word itself fills two thousand. Each lookup must also hash a string of up to L letters, so a question costs O(L) anyway, and nothing is gained for it.

The deeper waste is that the beginning `appl` is stored as a separate string beside `apple`, although it is just the first four letters of the longer one. Most of every copy repeats text that another copy already holds. A structure that adds one small piece for each new letter, and none when the letter is already there, would store a word in O(L) time and no more than L pieces.

<!-- stage: insight -->
### Walk One Letter At A Time

Hold a **walking cursor** that starts at the root. For each letter of the word, look at the **edge slot** for that letter in the node under the cursor. If the slot is empty, create a child node and place it in the slot, which happens only on insertion. If the slot is filled, nothing is created. Either way, move the cursor into the child. After i letters have been consumed, the cursor stands on the node that represents exactly the first i letters, so the cursor is a living record of how much of the word has been matched.

Insertion ends by flagging the node under the cursor, and a search ends by testing it. A beginning question stops at the same place and ignores the flag, and a failed slot on the way means no stored word has that beginning. This is why an exact question and a beginning question differ by a single test, and why a word that is a beginning of another word, such as `app` inside `apple`, needs no special case: the node for `app` carries its own flag, and having children changes nothing about it.

The slots must have a known size, which is the **domain size** of the characters that can occur. An array of 26 slots indexed by `letter - 'a'` is valid only when the contract promises lowercase English letters. Any other character needs a larger array with a mapping, or a map from characters to children.

The invariant is that after i letters the cursor stands on the node for the first i letters, so every created node is one that an inserted word needs.

<!-- names: walking cursor, edge slot, domain size -->

<!-- stage: variables -->
### Cursor, Slots And Flag

The `cur` variable is the cursor, set to the root before every operation and advanced once per letter. Each node holds `next`, an array of child references whose length is the domain size, and a boolean `word` that is set only by an insertion that ends at that node. The slot index is computed as `c - 'a'`, and it is only meaningful while `c` lies in the contract. The loop variable `i` counts the letters consumed. A question that meets a null slot stops with a failed walk, and the code must tell a failed walk apart from a walk that succeeded but sits on an unflagged node.

<!-- stage: trace -->
### A Word Inside A Longer Word

Both traces use a trie that already holds the word `app`. The first inserts `apple`. The pointer `i` marks the letter being consumed. The first three letters find filled slots, and the pass counts show that the route is shared with `app`. The fourth and fifth letters find empty slots, so two nodes are created, and the last step flags the node for `apple`.

```trace
{"cells":["a","p","p","l","e"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"nodes":4,"pass":2,"made":"no"},"note":"The letter a already has an edge, so the walk moves onto the existing node for a and its pass count rises to 2."},{"at":{"i":1},"vars":{"nodes":4,"pass":2,"made":"no"},"note":"The letter p already has an edge, so the walk moves onto the existing node for ap and its pass count rises to 2."},{"at":{"i":2},"vars":{"nodes":4,"pass":2,"made":"no"},"note":"The letter p already has an edge, so the walk moves onto the existing node for app and its pass count rises to 2."},{"at":{"i":3},"vars":{"nodes":5,"pass":1,"made":"yes"},"note":"The letter l has no edge yet, so a new node is made for the beginning appl and the walk moves onto it."},{"at":{"i":4},"vars":{"nodes":6,"pass":1,"made":"yes"},"note":"The letter e has no edge yet, so a new node is made for the beginning apple and the walk moves onto it."},{"at":{"i":5},"vars":{"nodes":6,"pass":1,"made":"no"},"note":"The word apple ends here, so the flag of this node is set and the trie holds 6 nodes with the root."}]}
```

The second trace asks an exact question about `appl` on the grown trie, which holds `app` and `apple`. The walk succeeds on every letter, since `appl` is a beginning of `apple`. The verdict step then reads the flag at the node for `appl`, finds it unset, and answers no. A beginning question would have answered yes at the same place.

```trace
{"cells":["a","p","p","l"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"flag":"unset","found":"yes"},"note":"The letter a has an edge, so the cursor moves onto the node for a."},{"at":{"i":1},"vars":{"flag":"unset","found":"yes"},"note":"The letter p has an edge, so the cursor moves onto the node for ap."},{"at":{"i":2},"vars":{"flag":"set","found":"yes"},"note":"The letter p has an edge, so the cursor moves onto the node for app."},{"at":{"i":3},"vars":{"flag":"unset","found":"yes"},"note":"The letter l has an edge, so the cursor moves onto the node for appl."},{"at":{"i":4},"vars":{"flag":"unset","found":"yes"},"note":"Every letter was matched, and the flag of the node for appl is unset, so an exact question answers no."}]}
```

<!-- stage: code -->
### Array Children For Lowercase Words

```java
final class LowerTrie {
    private static final class Node {
        final Node[] next = new Node[26];
        boolean word;
    }

    private final Node root = new Node();
    private int created;

    int insert(String word) {
        int before = created;
        Node cur = root;
        for (int i = 0; i < word.length(); i++) {
            int slot = word.charAt(i) - 'a';
            if (cur.next[slot] == null) {
                cur.next[slot] = new Node();
                created++;
            }
            cur = cur.next[slot];
        }
        cur.word = true;
        return created - before;
    }

    private Node reach(String letters) {
        Node cur = root;
        for (int i = 0; i < letters.length() && cur != null; i++) {
            cur = cur.next[letters.charAt(i) - 'a'];
        }
        return cur;
    }

    boolean search(String word) {
        Node end = reach(word);
        return end != null && end.word;
    }

    boolean startsWith(String letters) {
        return reach(letters) != null;
    }
}
```

Insertion returns the number of nodes it had to create, which is zero for a word already stored. Every operation visits one node per letter, so the time is O(L), and the space is O(26 * nodes) references, since each node carries a full array.

<!-- stage: applicability -->
### Character By Character Operations

Use this walk when an operation consumes its input one character at a time and either creates the missing step or fails at it: dictionary loading, validating that a code is on a list, and phone keypad lookups. The invariant is that the cursor always stands on the node for the letters consumed so far, so nothing needs to be rechecked.

One false friend is the sorted array of words with binary search. It answers exact questions in O(L log n) and can locate a beginning, yet inserting a new word shifts the array, and it stores every shared beginning again. Another is the idea that a node with no children must be a word, which is wrong whenever words are inserted in an order such as `apple` and then `app`, since the node for `app` has children and is flagged anyway.

The array of 26 slots is a contract, not a default. A capital letter gives a negative index, and a digit or a hyphen gives an index outside the array, so input from outside a lowercase contract must either be rejected with a clear error or use a larger table or a map. The array also costs 26 references per node even when a node has one child, which is why a map can use less memory for a sparse dictionary.

<!-- stage: exercises -->
### Exercises

#### [Build] Insert Lowercase Words (Author exercise)
<!-- id: tn-insert-lowercase -->

**Prerequisites.** The prefix node lesson and its route idea.

**Problem.** Insert the given lowercase words into an initially empty trie, in order, and report for each insertion how many new nodes it had to create. A word already present creates none.

**Constraints.** 0 <= words.length <= 1000 and each word has 1 to 30 lowercase letters. Words may repeat.

**Example 1.** Input `words = ["car", "cart", "cat", "car"]`, output `[3, 1, 1, 0]`.

**Example 2.** Input `words = ["b", "ba", "bad", "b"]`, output `[1, 1, 1, 0]`.

**Hint.** At which letters does the cursor find an empty slot, and what is created there?

**Changed decision.** A node is added only at an empty slot, so the count for a word equals its length minus the length of the longest route that already existed.

#### [Vary] Search Versus StartsWith (Author exercise)
<!-- id: tn-search-versus-starts -->

**Prerequisites.** The Insert Lowercase Words rung and the flag at a node.

**Problem.** After inserting a list of lowercase words, answer a list of probes. For each probe return 2 if it is exactly an inserted word, 1 if it is a beginning of some inserted word but not itself a word, and 0 otherwise.

**Constraints.** 0 <= words.length <= 1000, 0 <= probes.length <= 1000, and every string has 1 to 20 lowercase letters.

**Example 1.** Input `words = ["tea", "ten", "to"]`, `probes = ["te", "tea", "tee", "t", "toe"]`, output `[1, 2, 0, 1, 0]`.

**Example 2.** Input `words = ["a"]`, `probes = ["a", "ab", "b"]`, output `[2, 0, 0]`.

**Hint.** What is different between a walk that fails and a walk that succeeds on an unflagged node?

**Changed decision.** The flag is consulted only after a successful walk, and it separates the codes 2 and 1.

#### [Boundary] Word Is Prefix Of Another (Author exercise)
<!-- id: tn-word-is-prefix -->

**Prerequisites.** The Search Versus StartsWith rung.

**Problem.** Given distinct lowercase words in any order, return those words that are a proper beginning of at least one other word in the list, keeping the input order. Insert all the words first and then judge each word from its own node.

**Constraints.** 0 <= words.length <= 1000, each word has 1 to 20 lowercase letters, and all words are different.

**Example 1.** Input `words = ["apple", "app", "ape"]`, output `["app"]`.

**Example 2.** Input `words = ["a", "ab", "abc", "b", "zebra"]`, output `["a", "ab"]`.

**Hint.** Insert order does not change the trie, so what must be true of the node of a word if some longer word passes through it?

**Changed decision.** A flagged node that has a child is a word that is also a route, and it is detected after all insertions, not by the order of arrival.

#### [Recognize] Implement Trie (LeetCode 208)
<!-- id: tn-trie-domain-contract -->

**Prerequisites.** The Word Is Prefix Of Another rung and the domain size.

**Problem.** Implement the three operations insert, exact search and beginning test over strings made of the lowercase letters `a` to `z` and the digits `0` to `9`, which is a domain of 36 characters. Run a script of commands `insert:w`, `search:w` and `startsWith:p`. Return the answers of the last two kinds as 1 or 0, in order, and append the final count of nodes other than the root as the last number.

**Constraints.** Up to 2000 commands and every string has 1 to 50 characters from the domain.

**Example 1.** Input `commands = ["insert:ab1", "search:ab", "startsWith:ab", "search:ab1", "insert:b2", "startsWith:b"]`, output `[0, 1, 1, 1, 5]`.

**Example 2.** Input `commands = ["search:7", "insert:7", "search:7", "startsWith:77"]`, output `[0, 1, 0, 1]`.

**Hint.** What index does a digit get, and how many slots does a node need?

**Changed decision.** The slot array has 36 entries and a mapping function replaces `c - 'a'`, so the contract of the character domain is written into one line.
