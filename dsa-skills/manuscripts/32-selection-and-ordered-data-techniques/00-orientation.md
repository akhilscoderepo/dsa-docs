<!-- section: orientation -->
## Orientation

A monitoring service stores a million response times and must report the median every minute. Sorting the whole list each time wastes work, because only one position of the sorted order is needed. A pricing service also asks for the nearest cheaper offer to a given price while offers come and go. Both services need an answer about order without paying for a full sort.

### Prerequisites

You should know arrays and swapping two cells, sorting with comparators, recursion on an index range, and the merge step of merge sort. You should know that a `TreeMap` keeps keys sorted. The lessons explain the exact methods when they first matter.

### The Four Lessons

Each lesson answers one question about order.

- **Quickselect** finds the value of one sorted position by partitioning and then following only the side that holds the target position.
- **Partition Invariants** shows which index ranges a partition loop guarantees at every step, including the three-way form for repeated values.
- **Ordered Maps And Sets** uses `TreeMap` and `TreeSet` to find the nearest key below or above a value in O(log n) time while keys change.
- **Merge Counting** counts pairs of positions that violate an order while merge sort combines two sorted halves.

### The Closing Lesson

**Partition And Selection** joins Quickselect, Partition Invariants and Merge Counting. A partition places one value at its final position, and selection uses that proof to skip a whole side. Its four exercises select a rank with its position range, select the closest points with ties, count smaller values to the right within a distance, and count pairs with a scaled threshold.

### How To Work Through Each Lesson

A lesson opens with a realistic failure and a direct program that is too slow or wrong. You predict its cost before the explanation appears. Later parts say which value the method keeps between steps, list the variables, follow two traces, show the code and say when the idea stops fitting. Four exercises close each lesson, and each has a hint and a solution you can open after your own attempt.

### What You Can Do After This Chapter

You can decide when one rank is enough and a full sort is not needed. You can write a partition loop whose index boundaries you can state before the first swap. You can pick a sorted collection for nearest-key questions and count order violations in O(n log n) time.
