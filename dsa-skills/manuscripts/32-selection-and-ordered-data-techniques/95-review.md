<!-- section: review -->
## Review

A dashboard sorts a million samples to read the median, a lookup scans every price to find the next higher one, and a ranking job compares every pair of scores to count inversions. The questions below cover the four lessons and the closing lesson. Decide each answer before you open the explanation, and return to this page after a few days.

### Recognition Questions

```quiz
{"id": "rq32-rev-quickselect-side", "q": "After a partition, the pivot sits at index 6 in a zero-based array, and the target position is index 3. Which range does quickselect search next?", "options": ["Indices 0 to 5", "Indices 7 to the end", "The whole array again", "Only index 6"], "answer": 0, "explain": "Every value left of index 6 is not greater than the pivot, and index 3 is less than 6, so the target lies in indices 0 to 5."}
```

```quiz
{"id": "rq32-rev-three-way", "q": "A partition on the values 4, 4, 4, 4 with pivot 4 uses a two-way split that sends equal values to one side. What risk does that create?", "options": ["Each call may shrink the range by only one value, giving O(n^2) time", "The pivot may be lost", "The array may be sorted wrongly", "No risk exists"], "answer": 0, "explain": "All equal values land on one side, so the next range shrinks by one. A three-way split removes the whole run of equal values at once."}
```

```quiz
{"id": "rq32-rev-treemap-floor", "q": "A TreeMap holds the keys 10, 20 and 30. What does floorKey(25) return?", "options": ["20", "30", "25", "null"], "answer": 0, "explain": "floorKey returns the greatest key that is less than or equal to its argument. That key is 20."}
```

```quiz
{"id": "rq32-rev-merge-count", "q": "Two sorted halves are [2, 5, 9] and [1, 3]. While merging, how many pairs of a left value greater than a right value does the merge count?", "options": ["5", "2", "6", "3"], "answer": 0, "explain": "The value 1 is below 2, 5 and 9, which gives 3 pairs. The value 3 is below 5 and 9, which gives 2 more. The total is 5." }
```

```quiz
{"id": "rq32-rev-overflow", "q": "A pair test compares a[i] > 2 * a[j] for int values near 2^31 - 1. Why does the code use long?", "options": ["2 * a[j] can exceed the int range and wrap to a negative number", "long is faster than int", "int cannot compare two values", "The array must hold long values"], "answer": 0, "explain": "Doubling a large int overflows the 32-bit range. A long holds the exact product."}
```

### Fixing A Wrong Answer

Open the lesson whose topic the question covers, such as Quickselect, Ordered Maps And Sets or Merge Counting, and reread its variables list and applicability part. Then rerun its first trace by hand on a smaller input.
