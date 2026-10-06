<!-- section: review -->
## Review

Come back to this page after the lessons and again a few days later. Each question describes a situation and leaves out the lesson name. Choose an answer before you open the explanation.

### Recognition Questions

```quiz
{"id": "sq-rev-null-deque", "q": "A program calls `deque.addLast(null)` on an `ArrayDeque`. What happens?", "options": ["The call throws NullPointerException", "The call adds the null and returns false", "The call adds the null at the front", "The call ignores the null silently"], "answer": 0, "explain": "ArrayDeque rejects null because `poll` returns null to mean that the deque is empty. A stored null would make that signal ambiguous."}
```

```quiz
{"id": "sq-rev-fifo-turns", "q": "A task needs three turns. After each turn that is not the last, where does the simulation put it?", "options": ["On top of the stack of waiting tasks", "At the back of the queue", "At the front of the queue", "Nowhere, since the turn finished"], "answer": 1, "explain": "The task joins the back so every task that arrived earlier gets its turn first. Putting it at the front would let one task take every turn while the others wait."}
```

```quiz
{"id": "sq-rev-two-stack-cost", "q": "A queue built from an input stack and an output stack runs n pushes and then n removals. What is the total cost of the removals?", "options": ["O(n^2), because each removal moves everything", "O(log n), because the stacks halve the work", "O(n), because each item moves once", "O(1), because the output stack is already full"], "answer": 2, "explain": "The first removal moves all n items to the output stack once. Later removals only pop from it. Each item is pushed twice and popped twice in total, so the cost is O(n)."}
```

```quiz
{"id": "sq-rev-bfs-first", "q": "A search moves between floors with fixed steps, each press costing one. Why does a queue reach the target by the fewest presses?", "options": ["It skips floors that it already saw", "It always picks the floor closest to the target", "It tries the up button before the down button", "It finishes all routes of k presses before any route of k plus 1"], "answer": 3, "explain": "The queue serves older entries first, so every floor reached by k presses leaves before any floor reached by k plus 1. The first time the target comes out, no shorter route exists."}
```

```quiz
{"id": "sq-rev-bracket-count", "q": "The text `[1, {2]}` has one of each of the four bracket symbols. Why does it still fail?", "options": ["The closing `]` meets an unfinished `{` on top of the stack", "The counts of the two pairs differ", "The text does not start with an opening symbol", "The closing symbols come after the opening symbols"], "answer": 0, "explain": "Equal counts do not give the right pairing. The most recent unfinished opening is `{`, and `]` cannot close it, so the scan reports a mismatch at that point."}
```

```quiz
{"id": "sq-rev-saved-total", "q": "A scan sums the numbers directly inside each array of `[1, [2, 9], 4]`. What does it do when it reads the inner `[`?", "options": ["Resets the total to 0 and forgets the 1", "Pushes the current total and starts a fresh total", "Adds the inner numbers to the same total", "Skips the inner array until the outer one ends"], "answer": 1, "explain": "The total 1 belongs to the outer array and must survive. The scan stores it on the stack, counts the inner numbers from 0 and restores the stored 1 at the closing bracket."}
```

```quiz
{"id": "sq-rev-min-pop", "q": "Each entry of a stack holds a value and the minimum of everything below it and itself. After a pop, where does the new minimum come from?", "options": ["From a scan of the remaining entries", "From the popped entry", "From the entry that is now on top", "From the first entry pushed"], "answer": 2, "explain": "The entry on top stores the minimum of its own prefix, and that prefix is exactly what remains after the pop. No rescan is needed, so the question costs O(1)."}
```

```quiz
{"id": "sq-rev-level-size", "q": "A loop must print the pages of each click depth on its own line. What does it read before each pass over a level?", "options": ["The size of the queue at that moment", "The depth stored in each page", "The number of links on the first page", "The total number of pages"], "answer": 0, "explain": "At the start of a level the queue holds exactly that level. Reading the size then and removing that many items drains one level. Items added during the pass wait for the next one."}
```

```quiz
{"id": "sq-rev-decode-digits", "q": "A decoder reads `12[a]` and repeats the letter twice. What did it get wrong?", "options": ["It pushed the count before the bracket", "It treated each digit as a full count and did not join digits into one number", "It popped the text too early", "It ignored the closing bracket"], "answer": 1, "explain": "The count is built as number = number * 10 + digit while digits arrive. Using only the last digit gives 2, not 12."}
```

```quiz
{"id": "sq-rev-calc-delay", "q": "A calculator keeps a pending operator and reads `7 + 12 * 3` from left to right. When does it apply the `+` that sits before the 12?", "options": ["Right after the 7 is read", "When the 12 is complete, at the `*`", "When the whole text ends", "After the 3 is read, together with the `*`"], "answer": 1, "explain": "A pending operator applies as soon as the number after it is complete. The `+` pushes 12 as a new term when the scan reaches the `*`. The `*` then becomes pending, and when the 3 is complete it multiplies the top term 12 into 36."}
```

```quiz
{"id": "sq-rev-postfix-order", "q": "A postfix engine reads `8 3 -`. The first pop returns 3 and the second returns 8. Which expression gives the answer?", "options": ["first pop minus second pop", "second pop minus first pop", "the larger minus the smaller", "the absolute difference"], "answer": 1, "explain": "The operand written first is deeper in the stack, so it comes out second. The result is the second pop minus the first pop, which gives 5. The reverse order gives -5."}
```

```quiz
{"id": "sq-rev-checked-pop", "q": "A path reader sees `..` while its stack of folder names is empty at the root. What does the contract say the reader does before any pop?", "options": ["It pops anyway and catches the exception", "It checks that the stack is not empty and otherwise keeps the root", "It clears the stack and starts again", "It adds a new folder named `..`"], "answer": 1, "explain": "A pop on an empty stack throws or returns null, depending on the call. The reader checks the size first, and the contract decides that a move above the root stays at the root."}
```
