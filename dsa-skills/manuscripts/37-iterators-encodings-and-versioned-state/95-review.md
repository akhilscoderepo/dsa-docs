<!-- section: review -->
## Review

An iterator that moves when it only looks, a codec that gives two lists the same text, and a version query that reads the wrong state all pass short tests. The questions below cover all eight lessons. Try them after the lessons and again after a few days, and commit to an answer before opening the explanation.

### Recognition Questions

```quiz
{"id": "rq37-rev-peek-moves", "q": "A wrapper stores the next value in a field when `peek()` runs. What must `next()` do when that field is filled?", "options": ["Read a fresh value from the source and drop the field.", "Throw, because the value was already seen.", "Return the stored value and clear the field.", "Return the stored value and keep the field."], "answer": 2, "explain": "The stored value is the next element. Returning it and clearing the field consumes it once, and the source is not read a second time."}
```

```quiz
{"id": "rq37-rev-exhausted", "q": "An iterator is exhausted and a caller invokes `next()`. Which rule keeps the class predictable?", "options": ["Throw `NoSuchElementException` and leave the logical state unchanged.", "Return a default value such as -1 on some paths and throw on others.", "Retry the source until a value appears.", "Reset the cursor to the start."], "answer": 0, "explain": "One stated rule on every path is the contract. A throw that changes no logical state lets the caller call again and get the same answer."}
```

```quiz
{"id": "rq37-rev-lazy-flatten", "q": "A nested list may be 100,000 levels deep. Why does a recursive eager flatten fail the iterator contract?", "options": ["It returns elements in the wrong order.", "It cannot handle empty lists.", "It needs a hash map.", "It reads the whole input before the first `next()` and can overflow the call stack."], "answer": 3, "explain": "A lazy iterator holds only the unfinished cursors on a heap stack. Eager recursion costs memory up front and depth equal to the nesting."}
```

```quiz
{"id": "rq37-rev-run-skip", "q": "An RLE iterator has counts up to 10^9 and thousands of runs. What does `skip(n)` use to skip n elements?", "options": ["A loop that consumes one element at a time.", "Subtraction on the current run's remaining count, run by run.", "Binary search over a flattened array.", "A copy of the encoded array."], "answer": 1, "explain": "Each run is consumed in one step by subtracting its remaining count, so the cost depends on the number of runs touched and not on n."}
```

```quiz
{"id": "rq37-rev-codec-ambiguity", "q": "Strings are joined with a comma into one encoded string. Why can decoding fail?", "options": ["Commas are too slow.", "Java strings cannot hold commas.", "A string may contain a comma, so two different lists can share one encoding.", "Decoding needs the original count."], "answer": 2, "explain": "A codec must be injective. A length prefix before each body marks the boundary, so a comma inside a body cannot be mistaken for a separator."}
```

```quiz
{"id": "rq37-rev-null-markers", "q": "A preorder tree codec writes only node values. Why do two different trees collide?", "options": ["Missing children leave no trace, so different shapes give the same value list.", "Preorder is not a traversal.", "Values may repeat.", "Decoding needs the postorder."], "answer": 0, "explain": "A marker for each missing child records the shape. With markers, the decoder knows when a subtree ends."}
```

```quiz
{"id": "rq37-rev-version-floor", "q": "A snapshot array records pairs `(snapId, value)` per cell. How does `get(index, snapId)` find the value?", "options": ["Scan from the first pair to the last.", "Copy the array at each snapshot.", "Return the latest pair.", "Binary search for the last pair whose id is at most `snapId`."], "answer": 3, "explain": "Pairs are sorted by id, so the greatest id not above the query is the value in force at that version. If none exists, the cell kept its starting value."}
```

```quiz
{"id": "rq37-rev-query-object", "q": "A class answers many `frequency(left, right, value)` queries on one array. Where should the work go?", "options": ["Into each query, scanning the range.", "Into the constructor, which stores a sorted index list per value for binary search.", "Into a recursive call per element.", "Into a static counter."], "answer": 1, "explain": "The constructor spends O(n) once, and each query binary searches two positions in the value's list. Repeated queries then cost O(log n)."}
```

```quiz
{"id": "rq37-rev-frontier", "q": "A complete-tree inserter keeps a queue of nodes that still have a free child slot. After it adds a child, what happens to the parent?", "options": ["It always leaves the queue.", "It leaves the queue only when both child slots are full.", "It moves to the back of the queue.", "It is never stored again."], "answer": 1, "explain": "The first node in the queue is the parent that gets the next child. It leaves the queue once its second child is attached, so the queue head is always the next insertion point."}
```

```quiz
{"id": "rq37-rev-prev-next", "q": "A bidirectional tree iterator supports `next` and `prev`. Why keep the values already produced?", "options": ["The tree cannot be walked a second time.", "Moving back must return values already seen, and re-walking a lazy stack cannot go backward.", "Sorting needs them.", "They make `hasNext` faster."], "answer": 1, "explain": "A forward-only stack walk discards visited nodes. Keeping produced values lets `prev` step back and lets a later `next` replay them in the same order."}
```

```quiz
{"id": "rq37-rev-shared-grammar", "q": "Why must a tree decoder read the same token grammar that the encoder wrote?", "options": ["Decoding must stop at exactly the tokens of one tree, so shape markers and order must match.", "Decoders run faster that way.", "The tree has to be sorted.", "Java requires it."], "answer": 0, "explain": "The decoder consumes tokens in the encoder's order and ends when the markers close the root's subtrees, so any change in grammar breaks the rebuild."}
```

