<!-- section: orientation -->
## Orientation

Many problems about words keep asking about their beginnings. Does some stored word start with these letters, what completes them, which stored word is the shortest beginning of this one? A trie answers all of these by storing each beginning once, as a node that is reached by a route of edges from the root, and by keeping a separate mark for the beginnings that are words in their own right. The chapter builds that structure, makes it search with blanks, uses it to cut a string into dictionary words, and then reuses the same idea with bits in place of letters to maximise an exclusive or.

### What To Bring

You should be comfortable with arrays of references, with recursion over a position, and with the habit from earlier chapters of naming what a variable means before using it. Hash maps and sets from Chapter 04 are the baseline that a trie is compared with. The string indexing of Chapter 03 supplies the letter-by-letter reading, and the bit operations used in the last lesson are explained when they appear. Backtracking is not assumed, because it belongs to Chapter 19.

### The Six Lessons

The first lesson defines the prefix node and separates the flag that marks a word from the existence of a node. The second turns that into insertion and search over a fixed set of characters, and states what happens when the input leaves that set. The third searches patterns in which a blank matches any letter, branching only at the blanks. The fourth cuts a string into dictionary words and shows honestly where plain recursion becomes too slow. The fifth stores integers as paths of bits and finds the best partner for an exclusive or. The sixth combines the trie with reading a text, for shortening words to roots and for building the longest word one letter at a time.

### How To Work Through A Lesson

Each lesson opens with a short scene and a plain method that is right but slow. Try to say which work is repeated before you read the insight. When you follow a trace, say aloud which node the cursor stands on and what the flag at that node says. For each exercise decide first what a missing edge means, then what the end of the input means, and only then write code. Every solution file is run against a slower method on random inputs, so a surprising answer is worth tracing by hand.

### Leaving The Chapter

You should be able to say what one node stands for, why a node can exist without being a word, and how many characters a node can have as children. You should be able to explain why a search with blanks does not branch at written letters, why a word-break search needs more than recursion at scale, and why a maximum exclusive or can be settled one bit at a time. The review questions are scenarios, and they repay a second attempt after a few days.
