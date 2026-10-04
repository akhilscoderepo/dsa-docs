<!-- section: review -->
## Review

Return to this section after the lessons and again a few days later. The scenarios avoid naming the technique, so decide what the call state is and what must be undone before you read the options. The questions test prediction and recognition, which the guided exercises do not.

### Recognition Questions

```quiz
{"id": "bt-rev-shrinking-extreme", "q": "A power method takes an int exponent and, for a negative one, negates it to get a positive count. Which input defeats the negation?", "options": ["An exponent of zero.", "An exponent of minus one.", "The largest positive int.", "The most negative int, which stays negative when negated."], "answer": 3, "explain": "Negating the most negative int returns the same negative number, so the shrinking number never becomes a valid positive count. Widening to long before negating avoids it."}
```

```quiz
{"id": "bt-rev-missing-undo", "q": "A search appends a choice to one shared list, recurses, and returns without removing the choice. What do the later sibling branches see?", "options": ["The same list they would have seen with the removal.", "The choices of earlier branches still on the list, as if they had been made here.", "An empty list at every depth.", "A copy of the list as it was on entry."], "answer": 1, "explain": "Without the removal the list keeps growing, so each sibling starts from a path that includes decisions that belong to a finished branch."}
```

```quiz
{"id": "bt-rev-empty-subsets", "q": "What should a subset generator return for an empty input array?", "options": ["An empty list of results.", "A list holding one empty subset.", "A list holding the single value zero.", "An exception, since there is nothing to choose."], "answer": 1, "explain": "The empty subset is a valid selection of nothing, so the result has exactly one entry, and that entry is itself empty."}
```

```quiz
{"id": "bt-rev-mark-same-index", "q": "A search for arrangements marks index i as used before recursing. Why must the same index i be cleared on the way back?", "options": ["Clearing by value would also work, so it does not matter.", "Clearing any index is enough, because all marks look alike.", "The marks belong to input positions, so another index would free the wrong position or leave one blocked.", "The mark is cleared automatically when the call returns."], "answer": 2, "explain": "Each mark stands for one input occurrence. Clearing a different index leaves the set one still marked and frees one that is on the path."}
```

```quiz
{"id": "bt-rev-start-argument", "q": "A search for sets of five items records every ordering of every set. Which change removes the repeats?", "options": ["Pass i + 1 as the start of the next call and loop from it.", "Sort each result after it is found.", "Stop the search at depth four.", "Clear the used marks only at the end."], "answer": 0, "explain": "A start index that moves just beyond the last pick gives every set one spelling, in increasing order, so no ordering is generated twice."}
```

```quiz
{"id": "bt-rev-same-position", "q": "A coin search passes i, not i + 1, to its recursive call. What does that single change allow?", "options": ["Coins to be used in any order.", "A coin to be picked again, while earlier coins stay excluded.", "Negative coins.", "Skipping the base case."], "answer": 1, "explain": "The call may pay the same coin again but never an earlier one, so each handful is reached once, in list order, with repeats allowed."}
```

```quiz
{"id": "bt-rev-skip-condition", "q": "The values are sorted and some are equal. Which test skips a duplicate branch without losing a valid answer that uses two equal values?", "options": ["i > 0 and the value equals the value before it.", "The value equals any value already on the path.", "i > start and the value equals the value before it.", "The value was used anywhere earlier in the search."], "answer": 2, "explain": "Only the later of two equal siblings in the same loop is redundant. At i equal to start the earlier equal value sits higher on the path, so taking this one makes a legitimate second copy."}
```

```quiz
{"id": "bt-rev-unsafe-prune", "q": "A search for subsets with an exact sum abandons a branch once the running sum passes the target. For which inputs is that rule unsafe?", "options": ["Inputs that contain negative values.", "Inputs that are sorted.", "Inputs with a target of zero only.", "Inputs longer than ten values."], "answer": 0, "explain": "A negative value can bring a sum that is too high back down, so the premise that the sum never decreases fails and real answers are cut off."}
```

```quiz
{"id": "bt-rev-record-moment", "q": "A search cuts a string into pieces that each pass a test. When should it record the path as a complete partition?", "options": ["When the loop over endings finds no acceptable piece.", "When the path holds at least two pieces.", "When the last piece accepted is the longest so far.", "When the start has reached the length of the string."], "answer": 3, "explain": "Only a start equal to the length means that every position has been covered. A path that stops early has left a scrap uncut."}
```

```quiz
{"id": "bt-rev-restore-on-success", "q": "A grid search marks a cell in place and returns true the moment one neighbour succeeds, before restoring the cell. What goes wrong?", "options": ["Nothing, since a found word ends the program.", "The recursion no longer stops.", "Later searches on the same grid meet leftover markers and may miss routes that exist.", "The word is reported twice."], "answer": 2, "explain": "The marker stays on the board after the call returns, so every later start cell sees a changed grid. The outcome should be stored, the cell restored, and only then returned."}
```

```quiz
{"id": "bt-rev-missing-child", "q": "In a board search guided by a trie, the walk reaches a tile whose letter has no child at the cursor. What should it do?", "options": ["Enter the tile and mark it, then stop at the next tile.", "Restart the search from the root of the trie at that tile.", "Remove the cursor node from the trie.", "Not enter the tile at all, since no listed word continues that way."], "answer": 3, "explain": "A missing edge proves that no listed word begins with the route plus this letter, so the tile is not entered and no marker is placed."}
```

```quiz
{"id": "bt-rev-emission-clears-word", "q": "When a trie-guided walk emits a word, why does it clear the word stored at the node and not remove the node?", "options": ["Longer words may pass through the node and later routes still need it.", "Removing nodes is slower than clearing a field.", "The trie would otherwise forget the alphabet.", "A node cannot be removed once it has been entered."], "answer": 0, "explain": "The node may lie on the route of a longer listed word, so only the stored word is cleared, which stops a second report without cutting off continuations."}
```
