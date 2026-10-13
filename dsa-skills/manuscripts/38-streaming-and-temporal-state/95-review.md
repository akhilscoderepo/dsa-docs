<!-- section: review -->
## Review

A window that disagrees with its spec at one instant, a heap root that was corrected away, and a shuffle that hands out its own array all pass short tests. The questions below cover all nine lessons. Try them after the lessons and again after a few days, and commit to an answer before opening the explanation.

### Recognition Questions

```quiz
{"id": "rq38-rev-boundary", "q": "A window covers the last 60 seconds and a call arrives at time 100. A record has time 40. Under the half-open range (t-60, t], what happens to it?", "options": ["It still counts, because 100 - 40 = 60 is not more than 60.", "It is expired, because the range excludes the instant 40.", "It counts only if the stream is correctable.", "It counts once and is then deleted."], "answer": 1, "explain": "The range (40, 100] excludes 40. Under the inclusive range [40, 100] the same record would count, so the contract must say which range applies."}
```

```quiz
{"id": "rq38-rev-stream-kind", "q": "Which question must you answer before choosing the data structure for a stream API?", "options": ["Whether the stream is append-only, correctable or expiring.", "Whether the values are even or odd.", "Whether Java or Python is used.", "Whether the answers are printed."], "answer": 0, "explain": "The kind of stream decides whether old state can be dropped, replaced or only hidden, and that decides the structure."}
```

```quiz
{"id": "rq38-rev-lazy-expiry", "q": "A token map cleans expired entries only when a method runs. Which rule keeps counting correct?", "options": ["Count every entry in the map.", "Purge or skip entries with expiry at or before now before counting.", "Purge only at midnight.", "Count only the newest entry."], "answer": 1, "explain": "A query must never expose expired state. Lazy cleanup is safe only when the query filters or purges first."}
```

```quiz
{"id": "rq38-rev-prefix-zero", "q": "A product-of-last-k stream stores prefix products. Why does a zero break division?", "options": ["Zero is negative.", "Zero changes the type to double.", "The product of the newest k values divides by a stored prefix, and a prefix of zero cannot be divided by.", "Zero makes the queue empty."], "answer": 2, "explain": "Dividing by a zero prefix is undefined. Clearing the stored history at a zero keeps every later division valid, and a query that reaches the zero returns 0."}
```

```quiz
{"id": "rq38-rev-heap-roots", "q": "A lazy heap stores (score, id) records after corrections. What must hold before its root is used?", "options": ["The root must be the largest id.", "The heap must be rebuilt.", "The root must be a duplicate.", "The map must still hold that id with that exact score."], "answer": 3, "explain": "Stale records stay in the heap after a correction. A root is trusted only after the map confirms it is current."}
```

```quiz
{"id": "rq38-rev-count-of-counts", "q": "A frequency tracker keeps value counts and a tally of counts. A value drops from count 1 to 0. What happens to the tally?", "options": ["The entry for count 1 decreases and no entry for count 0 is created.", "The entry for count 0 increases.", "The tally is rebuilt from scratch.", "The tally keeps the old entry."], "answer": 0, "explain": "Count 0 means the value is absent, so no tally entry represents it. Leaving the old entry would make a later query report a value that is gone."}
```

```quiz
{"id": "rq38-rev-sparse-buckets", "q": "A query asks for counts per hour over a range of ten years. Which approach avoids work proportional to the whole range?", "options": ["Allocate an array for every hour.", "Sort all events on each query.", "Store only non-empty buckets and report zero for missing ones.", "Refuse long ranges."], "answer": 2, "explain": "The cost should follow the number of events and buckets asked for, not the length of time covered."}
```

```quiz
{"id": "rq38-rev-shuffle-alias", "q": "A shuffle class returns its internal array from reset(). What can go wrong?", "options": ["Nothing, because arrays are immutable.", "The caller changes the array and corrupts the stored original.", "The shuffle becomes biased toward zero.", "The array doubles in size."], "answer": 1, "explain": "Arrays are mutable. Returning copies keeps the stored original unchanged by caller edits."}
```

```quiz
{"id": "rq38-rev-ordered-region", "q": "Why does the median structure keep the two halves balanced after every insert?", "options": ["So the heaps use less memory.", "So values print in order.", "So the roots of the two halves are always the middle values.", "So duplicates are rejected."], "answer": 2, "explain": "The median is read from the roots only when the sizes differ by at most one and every lower value is at most every upper value."}
```
