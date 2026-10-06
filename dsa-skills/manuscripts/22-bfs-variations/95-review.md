<!-- section: review -->
## Review

A spread simulator ages every cell one minute per cell, and a lock solver walks through a forbidden code. Each failure matches a question below. Return to this page after the lessons, and again after a few days. Each question describes a situation and hides the lesson name.

### Recognition Questions

```quiz
{"id": "bv-rev-sources", "q": "A grid has 3 rotten oranges. A program runs one search from each and keeps the smallest time per cell. What does a single search do better?", "options": ["Put all 3 oranges in the queue at distance 0 and run once", "Run the 3 searches in parallel threads", "Sort the oranges first", "Use depth-first search"], "answer": 0, "explain": "With all sources at distance 0, the first discovery of a cell is its distance to the nearest source, and each cell is dequeued once."}
```

```quiz
{"id": "bv-rev-layer", "q": "A queue holds 4 vertices at distance 2. A program adds 1 to the minute counter after each removal. What is wrong?", "options": ["Nothing, each removal takes a minute", "The four vertices spread at the same time, so the counter should rise once for the whole group", "The queue should be a stack", "The counter should start at 1"], "answer": 1, "explain": "Capturing the queue size at the start of a round lets the program process exactly one distance group and then add 1."}
```

```quiz
{"id": "bv-rev-meet", "q": "Two searches grow from start and target. When can the program add their two distances into an answer?", "options": ["Only when both queue fronts hold the same vertex", "When a newly generated state already sits in the other side's map", "After both queues are empty", "When both sides have the same size"], "answer": 1, "explain": "A crossing edge joins two different vertices, so the test must run while generating neighbors, not when fronts are compared."}
```

```quiz
{"id": "bv-rev-key", "q": "A maze has doors that need keys. The visited array records only the cell. Which answer can it produce?", "options": ["A shorter path than the true one", "No path although one exists", "A correct path always", "A crash"], "answer": 1, "explain": "A cell reached without the key marks the cell seen, so the later visit with the key is dropped even though it opens new moves."}
```

```quiz
{"id": "bv-rev-dominance", "q": "A search reaches cell c with 1 break left at distance 5, and later with 3 breaks left at distance 6. Does the first state dominate the second?", "options": ["Yes, because it arrived earlier", "No, because the later state keeps more resource and may reach cells the first cannot", "Yes, because distance matters more", "Only on a 1-D grid"], "answer": 1, "explain": "Dominance needs equal or smaller distance and at least as much resource. Here the second state has more resource, so it stays."}
```

```quiz
{"id": "bv-rev-model", "q": "A task asks for the shortest word sequence, not only its length. Which of the four modeling choices changes?", "options": ["The start set", "What the search stores per state, which now includes a parent", "The meaning of a layer", "Nothing changes"], "answer": 1, "explain": "The state key stays the word, and the program stores each word's parent so the sequence can be rebuilt after the search."}
```
