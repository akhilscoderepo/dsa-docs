<!-- section: review -->
## Review

A leaderboard recomputes a range total on every request, a calendar scans every booking to find the busiest minute and a counter allocates an array for timestamps near two billion. The questions below cover the five lessons and the two closing lessons. Return to this page after the lessons and again after a few days. Each question describes a situation, so decide the answer before you open the explanation.

### Recognition Questions

```quiz
{"id": "rq31-rev-fenwick-low-bit", "q": "A Fenwick tree stores node 12, and 12 in binary is 1100. Which positions does node 12 cover?", "options": ["Positions 9 to 12, a block of length 4", "Positions 1 to 12", "Only position 12", "Positions 12 to 16"], "answer": 0, "explain": "The block length equals the lowest set bit, and 12 & -12 equals 4, so node 12 covers positions 9 to 12."}
```

```quiz
{"id": "rq31-rev-segment-identity", "q": "A segment tree for range sums receives a query that does not overlap a node's interval. What should that node return?", "options": ["The node's stored sum", "The value of its left child", "-1", "0, the identity of addition"], "answer": 3, "explain": "A node outside the query contributes nothing. The identity of the operator leaves the combined result unchanged, which is 0 for sums."}
```

```quiz
{"id": "rq31-rev-lazy-tag", "q": "A lazy tree adds 5 to every position of a node covering 4 positions. By how much does the stored node sum change, and what is saved for the children?", "options": ["The sum rises by 5, and nothing is saved", "The sum rises by 20, and a pending add of 5 is saved", "The sum rises by 20, and the children change immediately", "The sum rises by 4, and a pending add of 20 is saved"], "answer": 1, "explain": "Each of the 4 positions gains 5, so the node sum gains 4 * 5 = 20. The pending add of 5 is applied to the children when a later call descends."}
```

```quiz
{"id": "rq31-rev-compress-ranks", "q": "The values 900000, -7, 900000 and 15 are compressed to dense ranks starting at 1. What are the ranks in input order?", "options": ["3, 1, 3, 2", "3, 1, 4, 2", "1, 2, 1, 3", "2, 0, 2, 1"], "answer": 0, "explain": "The distinct sorted values are -7, 15 and 900000, which get ranks 1, 2 and 3. Equal values share one rank, so the input maps to 3, 1, 3, 2."}
```

```quiz
{"id": "rq31-rev-sweep-grouping", "q": "Trips take 2 passengers from stop 1 to stop 5 and 3 passengers from stop 5 to stop 8, with half-open trips [pick-up, drop-off). Is the peak load 5 at stop 5?", "options": ["Yes, both trips are active at stop 5", "Yes, because pick-ups run before drop-offs", "No, the first trip ended before stop 5 and the peak is 3", "No, the peak is 2"], "answer": 2, "explain": "A half-open trip stops counting at its drop-off stop. The first trip releases its 2 passengers at stop 5 before the second boards, so the load never exceeds 3."}
```

```quiz
{"id": "rq31-rev-sweep-ordered-state", "q": "A skyline sweep reaches a coordinate where one building ends and another of equal height starts. How many output points does that coordinate add?", "options": ["One point at the new height", "Two points at the same height", "None, because the highest active height does not change", "One point at height 0"], "answer": 2, "explain": "The output records only changes of the highest active height. The equal height keeps the maximum the same, so no point is added."}
```

```quiz
{"id": "rq31-rev-compress-fenwick", "q": "In a Fenwick tree over ranks 1 to m, which call counts the inserted values with a rank strictly below r?", "options": ["prefix(r)", "prefix(r - 1)", "prefix(m) - prefix(r - 1)", "add(r, 1)"], "answer": 1, "explain": "prefix(k) sums ranks 1 to k. Ranks strictly below r are 1 to r - 1, so the query is prefix(r - 1)."}
```

### Fixing A Wrong Answer

Open the lesson that the question names and reread its variables list and its applicability part. Then rerun its first trace by hand on a smaller input.
