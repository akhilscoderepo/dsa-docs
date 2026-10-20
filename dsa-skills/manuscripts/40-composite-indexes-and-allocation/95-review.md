<!-- section: review -->
## Review

A price that changes in one structure only, a seat that two customers hold, and a failed withdrawal that still removes cash all pass small tests. The questions below span the eight lessons. Try them as the lessons end and after a few more days, and lock in an answer before you open the explanation.

### Check Your Recall

```quiz
{"id": "rq40-rev-record", "q": "Index 4 changes from holding 7 to holding 9, with a map and a sorted set of indexes per number. Which step comes first?", "options": ["Insert 9 into the new set.", "Remove index 4 from the set of number 7.", "Rebuild every set.", "Sort the map."], "answer": 1, "explain": "A sorted set finds an entry by its fields, so the old entry must leave while it still carries the old fields. The insertion follows."}
```

```quiz
{"id": "rq40-rev-order", "q": "Two players have equal scores and equal names. What keeps both inside a tree set?", "options": ["A comparator that stops at the name.", "A hash code on the score.", "A last comparison field that is unique, such as the id.", "A second tree set."], "answer": 2, "explain": "A tree set treats entries that compare equal as one entry. A unique last field makes the order total, so every live player keeps an entry."}
```

```quiz
{"id": "rq40-rev-partition", "q": "A release call arrives twice for the same seat. Which design stays correct?", "options": ["Check the held record first and ignore the second call.", "Push the seat into the free list both times.", "Sort the free list after each call.", "Count the releases."], "answer": 0, "explain": "The held record tells the class that the seat is already free. Without that check, the free structure holds the seat twice and hands it to two customers."}
```

```quiz
{"id": "rq40-rev-bucket", "q": "A key moves from count 3 to count 4 and was the only key at count 3. What must the call do with bucket 3?", "options": ["Keep it for later.", "Fill it with a placeholder.", "Merge it into bucket 4.", "Remove it, so no bucket is empty."], "answer": 3, "explain": "An empty bucket would make the minimum or maximum query read a group with no key. The call removes the bucket in the same step that empties it."}
```

```quiz
{"id": "rq40-rev-version", "q": "A job is cancelled and added again with the same priority. Why does a priority check fail to reject the old heap entry?", "options": ["The old entry shows the same priority as the new one.", "The heap sorts by id.", "The old entry has a larger id.", "Cancelled jobs never leave the heap."], "answer": 0, "explain": "The old and new entries look the same by priority. Only a version number or object identity tells the two apart."}
```

```quiz
{"id": "rq40-rev-plan", "q": "A withdrawal changes five counters and may fail at the end. Where should the counters change?", "options": ["Before the first check.", "After every check has passed.", "Inside a catch block.", "In a separate thread."], "answer": 1, "explain": "A plan that reads state and writes only local variables decides the verdict first. The commit then applies every change and cannot fail."}
```

```quiz
{"id": "rq40-rev-exits", "q": "A task can leave a class through an execute call for one user, an execute call for all users and a remove call. How many places should write the indexes?", "options": ["Three, one per call.", "One for each index.", "One shared helper.", "None, the garbage collector handles it."], "answer": 2, "explain": "Every exit must reach every index. A single helper makes that true by construction, and a missed index becomes impossible to write."}
```

```quiz
{"id": "rq40-rev-gap", "q": "A gap entry for seats 4 and 9 reaches the top of a heap. Seat 9 left the room. What does the neighbor check do?", "options": ["Returns the gap anyway.", "Marks seat 4 as free.", "Rebuilds the heap.", "Drops the entry, because the two seats are no longer neighbors."], "answer": 3, "explain": "A gap is current only when both seats are occupied and no occupied seat lies between them. Seat 9 is gone, so the entry is stale."}
```

```quiz
{"id": "rq40-rev-rank", "q": "A rank tracker returns the i-th best entry on its i-th get call. What does the set of returned entries hold?", "options": ["The newest i entries.", "The best i - 1 entries overall.", "A random sample.", "Every entry added so far."], "answer": 1, "explain": "The returned set holds exactly the entries ranked above the next answer. A new entry that beats its weakest member swaps places with it."}
```
