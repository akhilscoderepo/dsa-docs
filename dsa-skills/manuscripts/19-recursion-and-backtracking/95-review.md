<!-- section: review -->
## Review

Come back to this page after the lessons and again after a few days. Each question describes a situation and does not name its lesson. Choose an answer before you open the explanation.

### Recognition Questions

```quiz
{"id": "bt-rev-call-state", "q": "A method sum(a, i) returns a[i] + sum(a, i) when i < a.length, and 0 otherwise. A program calls sum(a, 0) on an array of three values. What happens?", "options": ["It returns the sum of the three values", "It returns a[0] three times", "It fails with a StackOverflowError, because the argument i never changes", "It returns 0, because the base case runs first"], "answer": 2, "explain": "The recursive call passes the same i, so no call moves toward the base case. The chain of calls grows until the stack overflows. A strictly smaller state, such as i + 1, ends the chain."}
```

```quiz
{"id": "bt-rev-store-reference", "q": "A search adds the shared list path to the output with out.add(path) and removes the last entry of path after each branch. What do the stored lists hold when the search ends?", "options": ["Every finished path, unchanged", "The same list object stored many times, and it is empty after the last removal", "Only the first finished path", "A compile error appears, because a list cannot hold lists"], "answer": 1, "explain": "The method add stores a reference and makes no copy. Every stored entry is the one list that the search keeps editing, and the undo steps empty it. The leaf must store new ArrayList<>(path)."}
```

```quiz
{"id": "bt-rev-subset-calls", "q": "A subset search receives a start index and stores a copy of its path at the beginning of every call. How many calls does it make on an array of 5 distinct values, counting the first call?", "options": ["5", "10", "25", "32"], "answer": 3, "explain": "Each call stores exactly one different subset, and an array of 5 values has 2^5 = 32 subsets. The tree has no call without a result."}
```

```quiz
{"id": "bt-rev-used-mark", "q": "An ordering search sets used[i] to true before a branch and removes the last path entry after it, but it never sets used[i] back to false. How many orderings does it store for three distinct values?", "options": ["6", "3", "1", "0"], "answer": 2, "explain": "The first branch fills all three positions and stores one ordering. After the returns, every mark is still true, so no loop finds a free index and the search ends with a single ordering."}
```

```quiz
{"id": "bt-rev-last-useful", "q": "A search chooses 3 values from the indices 0 to 5 with a start index, and every loop runs to the last index. Which choices at the first level start calls that cannot reach 3 values?", "options": ["The choices at indices 4 and 5", "The choices at index 5 only", "The choices at indices 0 and 1", "No choice, because every call reaches 3 values"], "answer": 0, "explain": "A choice at index 4 leaves only index 5 for two more values, and a choice at index 5 leaves none. Both calls end with too few values. Index 3 leaves indices 4 and 5, which is enough."}
```

```quiz
{"id": "bt-rev-same-start", "q": "A search lists the lists of coins 2 and 3 that add up to 6, but each call passes i + 1 to its child. Which lists does it find?", "options": ["Only [2, 2, 2]", "None of them, because a coin can no longer repeat", "Only [3, 3]", "Both [2, 2, 2] and [3, 3]"], "answer": 1, "explain": "Both answers repeat a coin, and the next start i + 1 forbids the repeat. After the coin 2 the child may only use the coin 3 and the sum stops at 5. The child must receive the same start i."}
```

```quiz
{"id": "bt-rev-left-neighbour", "q": "A sorted array is [1, 2, 2, 2]. A subset search skips index i when i > 0 and a[i] == a[i - 1]. How many lists does it store, counting the empty list?", "options": ["4", "6", "8", "16"], "answer": 0, "explain": "The check removes every second copy of a value even at a deeper level, so only [], [1], [1, 2] and [2] remain. The check i > start keeps the 8 different subsets."}
```

```quiz
{"id": "bt-rev-unsafe-prune", "q": "A search for subsets with sum 10 stops a branch as soon as its sum exceeds 10. The input is [8, 7, -5]. Which statement is true?", "options": ["The rule is safe, because sums only grow", "The rule is safe, because the array is short", "The rule is unsafe only for arrays that are not sorted", "The rule is unsafe, because the branch 8, 7 passes 10 and the value -5 brings it back to 10"], "answer": 3, "explain": "The rule needs positive values, since only then every later choice raises the sum. The negative value lets the total return to 10, so the skip would lose the subset [8, 7, -5]."}
```

```quiz
{"id": "bt-rev-empty-suffix", "q": "A cutting search stores its path whenever the path is not empty and does not wait for the start position to reach the length. What does it store for the string abc, besides the four full cuts?", "options": ["Nothing else", "Partial lists such as [a], [a, b] and [ab], which do not cover the whole string", "The two cuts that end with c", "The string abc once more"], "answer": 1, "explain": "A path with fewer letters than the string leaves a suffix uncut. Only the empty suffix, at start position 3, proves that the fields cover every letter."}
```

```quiz
{"id": "bt-rev-mark-leak", "q": "A program shares one grid of marks between the searches of several words. A call returns true from inside its loop, and it has not cleared its mark. What can go wrong?", "options": ["The next word finds some cells blocked, so it may be reported missing", "The program throws an exception on the next call", "The board letters change", "Nothing, because a true result ends the program"], "answer": 0, "explain": "A mark that stays blocks the cell for every later path. The call must store its result, clear the mark and then return, so that the grid returns to its entry state on every exit."}
```

```quiz
{"id": "bt-rev-missing-edge", "q": "A board search carries a prefix tree node. At a cell, the child of the node for the letter of the cell is missing. What should the call do?", "options": ["Return at once, before it marks the cell", "Mark the cell and try the neighbours in case another word fits", "Clear the node and continue", "Report the path so far as a word"], "answer": 0, "explain": "A missing child proves that no dictionary word begins with the path plus this letter. Every longer path fails too, so the call returns without a mark to clear."}
```
