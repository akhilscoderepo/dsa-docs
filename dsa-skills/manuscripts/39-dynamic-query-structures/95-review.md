<!-- section: review -->
## Review

A prefix sum that ignores a correction, two touching ranges that stay split, and a division by a multiplier of zero all pass small tests. The questions below cover all eight lessons. Try them after the lessons and again after a few days, and commit to an answer before opening the explanation.

### Check Your Recall

```quiz
{"id": "rq39-rev-mutable", "q": "A Fenwick tree must change one value. Which entries change?", "options": ["Only the entry at that position.", "Every entry that owns a range containing that position.", "Every entry in the tree.", "No entry, because queries subtract."], "answer": 1, "explain": "Each entry sums the range it owns, so the entries whose range contains the position change by the same delta."}
```

```quiz
{"id": "rq39-rev-halfopen", "q": "Ranges [2,5) and [5,8) are stored. What does a half-open merge rule do?", "options": ["Keeps them apart because 5 is shared.", "Merges them into [2,8), because the end of one equals the start of the next.", "Deletes the second one.", "Rejects the insert."], "answer": 1, "explain": "With half-open ranges no integer lies in both, so touching ranges merge into one without a gap."}
```

```quiz
{"id": "rq39-rev-skip", "q": "What makes a skip list search fast?", "options": ["Every level holds all keys.", "Upper levels hold fewer keys, so a search skips long stretches.", "The keys are hashed.", "Levels are rebuilt on every query."], "answer": 1, "explain": "Promotion keeps each higher level sparser, so a search drops down only after it cannot move forward."}
```

```quiz
{"id": "rq39-rev-zero", "q": "Why can a pending multiplier of zero not be divided out?", "options": ["Zero is an even number.", "Zero has no modular inverse.", "Zero overflows a long.", "Zero changes the modulus."], "answer": 1, "explain": "Dividing needs an inverse, and zero has none, so the design resets the pending pair instead."}
```

```quiz
{"id": "rq39-rev-ratio", "q": "One update arrives for every hundred queries. Which cost matters most?", "options": ["Update cost.", "Query cost.", "Neither.", "Constructor memory only."], "answer": 1, "explain": "The update-to-query ratio tells which side to make cheap, and here it is the query side."}
```

```quiz
{"id": "rq39-rev-stale", "q": "A cached index was built before a new edge arrived. What must the next query do?", "options": ["Use it anyway.", "Rebuild or repair it first when the edge can change the answer.", "Return zero.", "Ignore the edge."], "answer": 1, "explain": "A stale index answers for an older graph, so a query that follows an effective update must refresh it."}
```
