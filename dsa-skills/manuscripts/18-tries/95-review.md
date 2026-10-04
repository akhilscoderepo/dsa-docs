<!-- section: review -->
## Review

Return to this section once the lessons are finished and again after some days. The scenarios do not name the technique, so decide what a node stands for and what a missing edge means before you read the options. The questions test prediction and recognition, which the guided exercises do not.

### Recognition Questions

```quiz
{"id": "tn-rev-flag-versus-node", "q": "Only the word apple has been inserted into a trie. What do an exact search for app and a beginning test for app answer?", "options": ["Both answer yes, since the node for app exists.", "Exact search answers no and the beginning test answers yes.", "Exact search answers yes and the beginning test answers no.", "Both answer no, since app was never inserted."], "answer": 1, "explain": "The node for app exists because apple passes through it, but its flag was never set. Only the exact search reads the flag."}
```

```quiz
{"id": "tn-rev-domain-contract", "q": "A trie node uses an array of 26 slots indexed by letter minus a. What happens when a capital letter is inserted?", "options": ["It is treated as the lowercase letter.", "It is stored in slot 0.", "It is silently skipped.", "It gets a negative index and the access fails."], "answer": 3, "explain": "A capital letter has a smaller code than a, so the index is negative. A larger table or a map is needed when the contract allows other characters."}
```

```quiz
{"id": "tn-rev-count-nodes", "q": "A set of distinct words is inserted into an empty trie. How many nodes other than the root does it contain?", "options": ["The number of words.", "The total number of letters in all words.", "The number of distinct nonempty beginnings of the words.", "Twenty-six times the number of words."], "answer": 2, "explain": "Each node stands for exactly one beginning, and a beginning shared by several words has only one node."}
```

```quiz
{"id": "tn-rev-wildcard-letters", "q": "In a pattern search, the search reaches a written letter in the pattern. How many children of the current node can it follow?", "options": ["Every child, because any might lead to a match.", "Exactly two.", "At most one, the child for that letter.", "None, until it reaches a blank."], "answer": 2, "explain": "A written letter selects one edge. Only a blank square gives the search a reason to follow several children."}
```

```quiz
{"id": "tn-rev-pattern-end", "q": "A pattern search has used up all pattern squares at a node whose flag is not set. What should it answer?", "options": ["Yes, because the beginning exists.", "No, because the pattern is only a beginning of a longer word.", "Yes if the node has children.", "It depends on the number of blanks."], "answer": 1, "explain": "A match must end on a stored word. A node without a flag means the pattern is a beginning, not a word of the same length."}
```

```quiz
{"id": "tn-rev-word-break-state", "q": "Plain recursion that cuts a long string into dictionary words becomes exponentially slow on some inputs. What is the repeated work?", "options": ["Building the trie for every call.", "Comparing words of different lengths.", "Reading the string from the right.", "Answering the question for the same start index again after reaching it by a different route."], "answer": 3, "explain": "The only state is the start index, so there are at most n + 1 different questions, but many routes reach the same one."}
```

```quiz
{"id": "tn-rev-terminal-branch", "q": "In a word-break search, from which trie nodes may a new piece of the segmentation begin?", "options": ["Only nodes whose flag is set.", "Every node on the route.", "Only leaf nodes.", "Only the root."], "answer": 0, "explain": "A gap may be placed only after a complete dictionary word, so the walk continues the recursion from flagged nodes, and it keeps reading past them for longer words."}
```

```quiz
{"id": "tn-rev-opposite-bit", "q": "Looking for the number that gives the largest exclusive or with x, the walk is at a bit where x has a 1 and the child for 0 exists. What should it do?", "options": ["Follow the child for 1, which agrees with x.", "Follow whichever child has more numbers below it.", "Follow the child for 0, the opposite branch.", "Stop, because the result is already settled."], "answer": 2, "explain": "A one in this position of the result outweighs every choice in lower bits, and it requires the bit to differ from the bit of x."}
```

```quiz
{"id": "tn-rev-sign-bit", "q": "Which choice keeps a binary trie correct when the input may contain negative 32-bit integers and the result is read as unsigned?", "options": ["Start at bit 30 and ignore the sign.", "Start at bit 31, shift with an unsigned shift, and keep the result in a long.", "Take absolute values first.", "Use 26 slots per node."], "answer": 1, "explain": "The sign bit is the top bit of the unsigned reading, so it must be an ordinary level of the trie. The unsigned shift avoids smearing it into lower bits."}
```

```quiz
{"id": "tn-rev-stop-rule", "q": "To replace a word by its shortest root, a cursor walks the word through a trie of roots. When should it stop?", "options": ["At the last flagged node it meets.", "At the end of the word.", "Only at a node with no children.", "At the first flagged node it meets."], "answer": 3, "explain": "The first flag met belongs to the shortest beginning that is a root. If no flag is met before a missing edge or the end, the word stays whole."}
```

```quiz
{"id": "tn-rev-buildable", "q": "A word counts only if every shorter beginning of it is also in the list. How does the trie search enforce that?", "options": ["It enters a child only when that child is flagged.", "It sorts the words by length first.", "It checks every beginning in a hash set.", "It counts the pass count of every node."], "answer": 0, "explain": "A node reached through flagged children has an unbroken chain of words above it, and one unflagged child cuts off every longer word below it."}
```

```quiz
{"id": "tn-rev-false-friend", "q": "What separates a binary trie from a character trie when both are used for search?", "options": ["The binary trie never stores a flag.", "A binary trie needs a hash map per node.", "The binary search follows the branch that disagrees with the query, the character search the branch that agrees.", "Nothing, the two are the same search."], "answer": 2, "explain": "The shape is the same, but the edges are digits and the goal is a large exclusive or, so the greedy choice is the opposite bit."}
```
