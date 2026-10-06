<!-- section: review -->
## Review

Return to this page after the lessons, and again after a few days. Each question describes a situation without naming the lesson. Choose an answer before you open the explanation.

### Recognition Questions

```quiz
{"id": "tr-rev-path-flag", "q": "A prefix tree holds the words car and cat only. A program calls search(\"ca\") and startsWith(\"ca\"). What do the two calls return?", "options": ["true and true", "false and false", "true and false", "false and true"], "answer": 3, "explain": "The node for ca exists, because both words pass through it, so startsWith returns true. No word ends at that node, so its flag is false and search returns false."}
```

```quiz
{"id": "tr-rev-array-domain", "q": "A node stores children in an array of 26 slots and indexes it with c - 'a'. A user submits the word Hat with a capital letter. What happens at the first letter?", "options": ["The program reads slot 7 and continues", "The offset is negative, so the program throws an index error", "The program treats the letter as a lowercase h", "The program skips the letter"], "answer": 1, "explain": "The code of H is 72 and the code of a is 97, so the offset is -25. Java throws an ArrayIndexOutOfBoundsException. A map, or a check before the first insert, avoids it."}
```

```quiz
{"id": "tr-rev-wildcard-edges", "q": "A search reads the pattern b.d in a tree of lowercase words. At which positions does the search look at more than one child?", "options": ["At every position", "At the first position only", "At the last position only", "At the dot only"], "answer": 3, "explain": "A letter selects one edge, so the search follows it or stops. Only a dot accepts any letter, so only there the search loops over the children."}
```

```quiz
{"id": "tr-rev-repeated-start", "q": "A recursion cuts the string aaaa...ab with the dictionary a and aa and takes a very long time. What causes the slowdown?", "options": ["The tree walk reads too many letters at each call", "Different sequences of cuts reach the same start index, and each visit repeats the search", "The dictionary words are too short for a tree", "The recursion uses too many substrings"], "answer": 1, "explain": "The cut sequences a,a and aa both reach index 2, and the number of sequences grows with the length. Each visit searches the same suffix again. Remembering results, taught in Chapter 26, removes the repeats."}
```

```quiz
{"id": "tr-rev-opposite-bit", "q": "A walk looks for the best XOR partner of x. At bit 12 the bit of x is 1, and the tree has both children at this node. Which child does the walk take?", "options": ["The child 1, because it equals the bit of x", "The child 0, because a differing bit puts a 1 in the result", "Either child, because lower bits decide", "The child with more numbers below it"], "answer": 1, "explain": "A result bit of 1 at bit 12 beats every combination of lower bits, so the walk takes the child whose bit differs from the bit of x."}
```

```quiz
{"id": "tr-rev-first-flag", "q": "The roots are car and cart, and the word is carts. The task asks for the shortest root that is a prefix of the word. What does the walk return?", "options": ["cart, because the walk reads every letter", "carts, because no root equals the word", "car, because the walk stops at the first flagged node", "An empty string"], "answer": 2, "explain": "The node for car already has a flag, and every deeper root is longer. The walk stops there and returns car."}
```

```quiz
{"id": "tr-rev-built-word", "q": "A search for the longest word whose every prefix is also in the list enters children of the tree. Which children may it enter?", "options": ["Every child that exists", "Only children whose own flag is true", "Only the first child in each node", "Only children below the deepest flagged node"], "answer": 1, "explain": "A path through a node without a flag means a prefix of the word is missing from the list. The search must enter only flagged children, so every node on the path is a word."}
```
