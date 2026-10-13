<!-- section: review -->
## Review

A search that skips a subset boundary, a pick that favours the last item, and a guess that is 3 percent too high all pass short tests. The questions below cover all eight lessons. Try them after the lessons and again after a few days, and commit to an answer before opening the explanation.

### Check Your Recall

```quiz
{"id": "rq35-rev-half-limit", "q": "A statement allows 40 items, each taken or left, and asks for the sum closest to a target. Which method fits the limit?", "options": ["Enumerate all 2^40 subsets.", "Enumerate the sums of each half and search for complements.", "Sort the items and use two pointers.", "Use a table indexed by the total."], "answer": 1, "explain": "Two lists of about a million sums are practical, while 2^40 checks are not. The table fails because the totals can be huge."}
```

```quiz
{"id": "rq35-rev-multiplicity", "q": "Why must the half-sum lists keep equal sums as separate entries when counting subsets?", "options": ["Two different subsets can have the same sum, and each one counts.", "Equal sums make the list shorter.", "The sort needs distinct keys.", "Equal sums are always zero."], "answer": 0, "explain": "The answer counts position sets. Dropping duplicates would undercount subsets whose values coincide."}
```

```quiz
{"id": "rq35-rev-f-value", "q": "In A*, which value orders the queue?", "options": ["The cost so far g alone.", "The guess h alone.", "The sum g + h.", "The number of edges used."], "answer": 2, "explain": "With h = 0 the sum equals g and the search is Dijkstra's algorithm. Using h alone gives greedy best-first search, which loses exactness."}
```

```quiz
{"id": "rq35-rev-stale-pop", "q": "A queue entry pops with a cost larger than the recorded cost of its cell. What should the search do?", "options": ["Expand the cell again.", "Return the cost.", "Skip the entry.", "Stop the search."], "answer": 2, "explain": "A cheaper cost was recorded after the entry was pushed, so the entry is stale and carries no new information."}
```

```quiz
{"id": "rq35-rev-reservoir-chance", "q": "In a one-item reservoir, what is the chance that the t-th item replaces the held item?", "options": ["1/2 for every item.", "1/t.", "1/(t-1).", "t/n for a stream of length n."], "answer": 1, "explain": "The chance 1/t makes every item seen so far equally likely to be held, and it needs no knowledge of the final length."}
```

```quiz
{"id": "rq35-rev-ticket-boundary", "q": "The weights are 2, 5 and 3, and tickets run from 1 to 10. Which index owns ticket 7?", "options": ["Index 1.", "Index 0.", "Index 2.", "No index."], "answer": 0, "explain": "The prefix totals are 2, 7 and 10. The first prefix total at least 7 belongs to index 1, so the boundary ticket stays with the earlier index."}
```

```quiz
{"id": "rq35-rev-polar-bias", "q": "Why does a uniform distance and a uniform angle give too many points near the center of a circle?", "options": ["Rings near the wall have more area but receive the same share of points as rings near the center.", "The angle is not uniform.", "The generator repeats values.", "Cosine is larger near zero."], "answer": 0, "explain": "Equal distance steps are not equal areas. A ring at distance d has area proportional to d, so the center is crowded."}
```

```quiz
{"id": "rq35-rev-random-pivot", "q": "Why does a uniformly random pivot protect quickselect from sorted input?", "options": ["Sorted input becomes unsorted.", "The partition becomes unnecessary.", "The worst case disappears.", "The pivot lands in the middle half with probability one half whatever the order is."], "answer": 3, "explain": "The chance of a good split depends on the draw, not on the input order. The worst case remains possible but becomes unlikely."}
```

```quiz
{"id": "rq35-rev-eligible-total", "q": "A pick must be fair among the items that qualify. What must the denominator of each chance be?", "options": ["The total weight of the qualifying items.", "The number of all items in the catalog.", "The weight of the heaviest item.", "The length of the longest run of non-qualifying items."], "answer": 0, "explain": "Each qualifying item needs chance weight divided by the eligible total. Any other denominator moves probability to the wrong items."}
```

```quiz
{"id": "rq35-rev-admissible-test", "q": "How can a program test whether a guess never exceeds the true remaining cost?", "options": ["Run the search once and compare costs.", "Check that the guess is positive.", "Sort the guesses.", "Run Dijkstra on the reversed graph from the goal and compare every vertex."], "answer": 3, "explain": "The reversed run gives the exact remaining cost of every vertex. The test is one comparison per vertex."}
```

```quiz
{"id": "rq35-rev-reopen", "q": "A guess is admissible but not consistent. What must the search do when a cheaper entry arrives for a cell that was already expanded?", "options": ["Expand the cell again.", "Ignore it.", "Return an error.", "Add the cost to the old one."], "answer": 0, "explain": "Reopening keeps the answer exact for an admissible guess. Ignoring the cheaper entry can return a longer route."}
```
