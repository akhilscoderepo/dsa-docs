<!-- section: review -->
## Review

Come back to this page after the lessons and again a few days later. Each question describes a situation and leaves out the lesson name. Choose an answer before you open the explanation.

### Recognition Questions

```quiz
{"id": "hp-rev-iteration-order", "q": "A default `PriorityQueue<Integer>` receives 5, 3, 8, 1 and 4 in that order. A program prints the queue with `toString`. What appears?", "options": ["[1, 3, 4, 5, 8]", "[1, 3, 8, 5, 4]", "[5, 3, 8, 1, 4]", "[8, 5, 4, 3, 1]"], "answer": 1, "explain": "The queue prints its array. The array keeps heap order, where each parent is at most its children, and it is not sorted. Repeated polls return 1, 3, 4, 5, 8."}
```

```quiz
{"id": "hp-rev-negation", "q": "A program fakes a largest-first queue by storing the negative of each value. Which input breaks it?", "options": ["A value of 0", "An array with duplicates", "The value Integer.MIN_VALUE", "An array with one element"], "answer": 2, "explain": "Negating Integer.MIN_VALUE gives Integer.MIN_VALUE again, because +2^31 does not fit in an int. The value then leaves first although it is the smallest."}
```

```quiz
{"id": "hp-rev-top-k-order", "q": "A program keeps the 3 largest values of a stream in a queue trimmed to 3 values. Which order must the queue use?", "options": ["Smallest value first, so the root is the weakest kept value", "Largest value first, so the root is the best value", "Insertion order", "Any order, because the queue is small"], "answer": 0, "explain": "A new candidate competes with the weakest kept value, so that value must sit at the root. A largest-first queue trimmed to 3 values keeps the 3 smallest values."}
```

```quiz
{"id": "hp-rev-merge-size", "q": "A merge reads 200 sorted files with 10 million values in total. What is the largest number of entries the queue holds at one time?", "options": ["10,000,000", "100,000", "2", "200"], "answer": 3, "explain": "The queue holds at most one entry for each file that still has unread values. That is at most 200 entries, so each operation costs O(log 200)."}
```

```quiz
{"id": "hp-rev-idle-jump", "q": "A scheduler has an empty queue, and the next task is released at time 1,000,000. What should the loop do?", "options": ["Increase the clock by one until the release time", "Set the clock to the release time and add that task", "Stop the loop", "Poll the queue and return null"], "answer": 1, "explain": "Nothing can run before that release time, so the clock jumps to it. Increasing the clock one unit at a time costs a million steps for no gain."}
```

```quiz
{"id": "hp-rev-remove-cost", "q": "A queue holds n entries. What does one call to `remove(Object)` cost?", "options": ["O(1)", "O(log n)", "O(n)", "O(n log n)"], "answer": 2, "explain": "The method searches the array from the front with equals, which costs O(n). Only the repair of the heap after the removal costs O(log n)."}
```

```quiz
{"id": "hp-rev-median-sizes", "q": "A tracker has seen 7 values and follows the rules of the two halves. How many values does each half hold?", "options": ["Lower 4 and upper 3", "Lower 3 and upper 4", "Lower 7 and upper 0", "Lower 3 and upper 3"], "answer": 0, "explain": "The lower half holds the same count as the upper half or one more. For 7 values that gives 4 and 3, and the root of the lower half is the median."}
```

```quiz
{"id": "hp-rev-closed-reuse", "q": "Two closed intervals [1,3] and [3,5] arrive in start order. The earliest finish is 3 and the next start is 3. May the second interval reuse the first group?", "options": ["Yes, because 3 is at most 3", "No, because both contain the point 3", "Yes, because the intervals are sorted", "Only when the groups have the same size"], "answer": 1, "explain": "Closed intervals include both endpoints, so these two share the point 3. The reuse test must be strict, an earliest finish below the next start."}
```

```quiz
{"id": "hp-rev-stale-root", "q": "A queue holds an old entry for a task whose priority was edited. The old entry reaches the root. What does the program do before it uses the root?", "options": ["Return it, because it is the smallest", "Compare its version with the newest version and discard it when they differ", "Rebuild the whole queue", "Call contains on the queue"], "answer": 1, "explain": "A root with an out-of-date version describes a state that no longer holds. The program polls and discards it, then checks the next root."}
```

```quiz
{"id": "hp-rev-equal-priority", "q": "A comparator orders tasks by duration only, and two tasks have equal durations. What does the queue promise about their removal order?", "options": ["The earlier input comes first", "The smaller index comes first", "The one inserted last comes first", "Nothing, the order depends on the array layout"], "answer": 3, "explain": "A heap gives no rule for ties. A tie-break on a unique field such as the index makes the order the same on every run."}
```
