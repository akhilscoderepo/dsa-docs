<!-- section: review -->
## Review

Return to this section once the lessons are done and again a few days later. The scenarios avoid naming the technique, so decide first what the heap holds, what its root promises, and what has to happen when that promise goes stale, and only then read the options. These questions test recall and recognition, which the guided exercises cannot.

### Recognition Questions

```quiz
{"id":"hp-rev-peek-promise","q":"A default Java PriorityQueue<Integer> holds 7, 3, 9, 1. What does peek() promise?","options":["The largest value, 9.","The value that was inserted first, 7.","The smallest value, 1, and nothing about the order of the rest.","The values in sorted order from the front."],"answer":2,"explain":"The default queue is a min-heap, so only the root is guaranteed to be extreme, and the remaining entries are only known to be no better than their parents."}
```

```quiz
{"id":"hp-rev-iteration","q":"A program prints every element of a PriorityQueue with a for-each loop and expects a sorted list. What is wrong?","options":["The loop removes the elements.","The loop walks the backing array, which is only partly ordered.","The loop skips the root.","The loop throws on equal values."],"answer":1,"explain":"Iteration reads the array from index 0, and a heap array satisfies only the parent-child rule, so sorted output needs repeated poll calls."}
```

```quiz
{"id":"hp-rev-negation","q":"Why is storing negated integers a risky way to get a max-first queue?","options":["Negation is slower than comparison.","The negation of the smallest int is itself, so it would be treated as the largest.","Negative numbers cannot be stored in a heap.","The queue refuses to reorder after negation."],"answer":1,"explain":"There is no positive counterpart of Integer.MIN_VALUE in 32 bits, so a comparator that compares through Integer.compare is the safe form."}
```

```quiz
{"id":"hp-rev-topk-heap","q":"To keep the five largest values of a long stream, which heap should hold them, and what is its root?","options":["A max-heap, and the root is the largest value.","A min-heap, and the root is the weakest of the five.","A max-heap of all values, and the root is the fifth.","A min-heap of all values, and the root is the largest."],"answer":1,"explain":"The item to find quickly is the one to drop next, which is the smallest of the retained values, so a min-heap capped at five exposes it."}
```

```quiz
{"id":"hp-rev-merge-size","q":"A merge of k sorted lists with a frontier heap never holds more than how many entries?","options":["One per value in all lists.","One per source that still has values.","Exactly two.","Half of the values."],"answer":1,"explain":"Each source contributes only its current front, so the heap size is bounded by the number of sources and not by the number of values."}
```

```quiz
{"id":"hp-rev-admit-ties","q":"A scheduler jumps its clock to the next release time. Why must it admit every task released at that time before choosing one?","options":["To keep the heap sorted.","A shorter task released at the same moment could otherwise be skipped.","The clock would run backward.","Admission is cheaper in a batch."],"answer":1,"explain":"The invariant says the ready heap holds exactly the executable tasks, and leaving one tied task outside could make the root the wrong choice."}
```

```quiz
{"id":"hp-rev-stale-loop","q":"After several removals are recorded in a pending-count map, the root of the heap may be stale. How should it be cleaned before use?","options":["With one if statement.","By calling contains on the heap.","With a loop that discards stale roots until a live one or an empty heap.","By rebuilding the heap each time."],"answer":2,"explain":"Several stale entries can sit at the top together, so the cleanup repeats until the root agrees with the companion state."}
```

```quiz
{"id":"hp-rev-logical-size","q":"A structure with delayed deletion reports its size. Which number is correct?","options":["The heap's size(), since it counts everything inside.","A separate live counter updated when an item is added or logically removed.","The size of the pending map.","The number of polls so far."],"answer":1,"explain":"Stale entries remain in the heap until they reach the root, so only a counter maintained at edit time describes the logical contents."}
```

```quiz
{"id":"hp-rev-median-invariant","q":"In a two-heap running median, which statement must hold after every insertion?","options":["Both heaps are min-heaps of equal size.","Every lower value is at most every upper value, and the sizes differ by at most one.","The lower heap holds all negative values.","The upper heap is always the larger one."],"answer":1,"explain":"The order between the halves puts the middle at the two roots, and the size rule decides whether the median is one root or the average of two."}
```

```quiz
{"id":"hp-rev-closed-tie","q":"Two closed intervals [1, 3] and [3, 6] are placed with an end heap. When may the second one reuse the first one's resource?","options":["Whenever the root is at most its start.","Only if the root is strictly less than its start.","Never, since they are sorted.","Only if their lengths are equal."],"answer":1,"explain":"Closed intervals that share an endpoint overlap, so reuse needs a strict comparison, while half-open intervals would allow at most."}
```
