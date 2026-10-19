<!-- section: review -->
## Review

A prefix sum that ignores a correction, two touching ranges that stay split, and a division by a multiplier of zero all pass small tests. The ten questions below cover all eight lessons. Try them after the lessons and again after a few days, and commit to an answer before opening the explanation.

### Check Your Recall

```quiz
{"id": "rq39-rev-mutable", "q": "A Fenwick tree must change one value. Which entries change?", "options": ["Only the entry at that position.", "Every entry in the tree.", "Every entry that owns a range containing that position.", "No entry, because queries subtract."], "answer": 2, "explain": "Each entry sums the range it owns, so the entries whose range contains the position change by the same delta."}
```

```quiz
{"id": "rq39-rev-plan", "q": "A fixed array answers 100,000 range-frequency queries known in advance. What does a sorted position list per value allow?", "options": ["A full scan of the range for every query.", "One hash lookup that ignores the range.", "A rebuild of the list after every query.", "Two binary searches over one list per query."], "answer": 3, "explain": "The positions of one value are sorted, so the count inside [left, right] is the difference of two binary search results."}
```

```quiz
{"id": "rq39-rev-halfopen", "q": "Ranges [2,5) and [5,8) are stored. What does a half-open merge rule do?", "options": ["Merges them into [2,8), because the end of one equals the start of the next.", "Keeps them apart because 5 is shared.", "Deletes the second one.", "Rejects the insert."], "answer": 0, "explain": "Touching ranges merge because the end of one equals the start of the next. Half-open means 5 belongs only to [5,8), so there is no gap and no overlap, and the result is one range [2,8)."}
```

```quiz
{"id": "rq39-rev-skip", "q": "What makes a skip list search fast?", "options": ["Every level holds all keys.", "The keys are hashed.", "Levels are rebuilt on every query.", "Upper levels hold fewer keys, so a search skips long stretches."], "answer": 3, "explain": "Promotion keeps each higher level sparser, so a search drops down only after it cannot move forward."}
```

```quiz
{"id": "rq39-rev-zero", "q": "Why can a pending multiplier of zero not be divided out?", "options": ["Zero is an even number.", "Zero has no modular inverse.", "Zero overflows a long.", "Zero changes the modulus."], "answer": 1, "explain": "Dividing needs an inverse, and zero has none, so the design resets the pending pair instead."}
```

```quiz
{"id": "rq39-rev-pair", "q": "The pending pair is (1, 0). The call addAll(3) runs, then multAll(2). What is the pair?", "options": ["(2, 6)", "(2, 3)", "(3, 2)", "(1, 6)"], "answer": 0, "explain": "addAll(3) gives (1, 3). The later multiplier scales both parts, so the pair becomes (2, 6)."}
```

```quiz
{"id": "rq39-rev-runs", "q": "Offsets reach 10^18 and ranges are added and removed. Which state answers coverage questions after a few merges?", "options": ["A boolean array with one cell per offset.", "A sorted map of disjoint runs keyed by start.", "A list of every call, sorted again per query.", "A hash set that holds every covered point."], "answer": 1, "explain": "The map stores one entry per run, and a floor lookup on the start finds the one run that can contain or touch a new range."}
```

```quiz
{"id": "rq39-rev-lift", "q": "A binary lifting table is built once. How many table jumps find the 25th ancestor of a node?", "options": ["25 jumps, one per level.", "One jump, because 25 is stored.", "Three jumps, one per set bit of 25.", "Five jumps, one per bit position."], "answer": 2, "explain": "25 is 11001 in binary, so jumps of 16, 8 and 1 levels reach the ancestor after the constructor has paid for the table."}
```

```quiz
{"id": "rq39-rev-ratio", "q": "One update arrives for every hundred queries. Which cost matters most?", "options": ["Update cost.", "Neither.", "Constructor memory only.", "Query cost."], "answer": 3, "explain": "The update-to-query ratio tells which side to make cheap, and here it is the query side."}
```

```quiz
{"id": "rq39-rev-stale", "q": "A cached index was built before a new edge arrived. What must the next query do?", "options": ["Use it anyway.", "Return zero.", "Rebuild or repair it first when the edge can change the answer.", "Ignore the edge."], "answer": 2, "explain": "A stale index answers for an older graph, so a query that follows an effective update must refresh it."}
```
