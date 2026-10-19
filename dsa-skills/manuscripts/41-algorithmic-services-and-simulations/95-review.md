<!-- section: review -->
## Review

A board scan that grows with the board, a trie that adds an overwritten value twice, and a transfer that debits one account before it finds the other missing all pass small tests. The nine questions below follow the nine lessons. Answer from memory first, then open the explanation, and repeat after a few days.

### Check Your Recall

```quiz
{"id": "rq41-rev-board", "q": "A 5 by 5 game keeps one counter per row, column and diagonal. How many counters does a move at the center update?", "options": ["Two.", "Three.", "Five.", "Four."], "answer": 3, "explain": "The center cell lies on its row, its column and both diagonals. That gives four counters, and each update costs O(1)."}
```

```quiz
{"id": "rq41-rev-path", "q": "A service creates the path /a/b/c while only /a exists. What should the create call do?", "options": ["Create b and c as well.", "Return failure and change nothing.", "Create c under a.", "Replace /a."], "answer": 1, "explain": "A node needs an existing parent. The parent /a/b is missing, so the call fails before it writes anything."}
```

```quiz
{"id": "rq41-rev-dependency", "q": "Cell A1 changes, and B1 reads A1 while C1 reads B1. In what order does the sheet recompute?", "options": ["C1, then B1.", "Any order.", "B1 only.", "B1, then C1."], "answer": 3, "explain": "C1 reads the cached value of B1, so B1 must be fresh first. A dependents search, reversed after finishing, gives that order."}
```

```quiz
{"id": "rq41-rev-feed", "q": "A feed returns the 10 newest posts from followed accounts. When must a muted account be removed from consideration?", "options": ["After the 10 posts are chosen.", "Before the heap receives its first entry.", "After sorting the output.", "Only when the account posts again."], "answer": 1, "explain": "A filter that runs after truncation can leave fewer than 10 posts although more eligible posts exist. Visibility comes first."}
```

```quiz
{"id": "rq41-rev-ledger", "q": "A transfer debits the sender and then finds that the receiver does not exist. Which design avoids the half-applied state?", "options": ["Credit the sender back in a catch block.", "Run the transfer twice.", "Test both accounts before any balance changes.", "Lock the sender."], "answer": 2, "explain": "A check block writes nothing, so a failure leaves the object as it was. The commit block then runs with no failure path."}
```

```quiz
{"id": "rq41-rev-trie", "q": "The key apple holds value 3 and is overwritten with value 5. What does each prefix node on its path add?", "options": ["Plus 2.", "Plus 5.", "Plus 3.", "Minus 3."], "answer": 0, "explain": "The delta is the new value minus the old value, which is 2. Adding 5 would count the old contribution a second time."}
```

```quiz
{"id": "rq41-rev-lifecycle", "q": "A task was cancelled, and its entry still sits in a heap. What lets the heap answer the next-task query correctly?", "options": ["Rebuilding the heap each call.", "Storing priorities only.", "Never cancelling a task.", "Checking the status table when the entry reaches the top."], "answer": 3, "explain": "A heap cannot remove an arbitrary entry cheaply. The status table is authoritative, so a top entry that it rejects is discarded."}
```

```quiz
{"id": "rq41-rev-ranked", "q": "Word counts are 5 for go, 5 for gone and 4 for gold. Which two words does the top list of prefix go keep first and second?", "options": ["gold, then go.", "gone, then go.", "go, then gone.", "go, then gold."], "answer": 2, "explain": "The higher count comes first, and equal counts break ties with the smaller word. So go precedes gone, and gold follows with a lower count."}
```

```quiz
{"id": "rq41-rev-writer", "q": "Three public calls each change a record that feeds four indexes. How many places should update the indexes?", "options": ["One private writer.", "Three, one per call.", "Four, one per index.", "Twelve."], "answer": 0, "explain": "A single writer takes the old and the new record and repairs every index. A call cannot skip an index that it never touches directly."}
```
