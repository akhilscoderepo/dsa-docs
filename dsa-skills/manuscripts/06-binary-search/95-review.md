<!-- section: review -->
## Review

Return to this section after the lessons and again after a few days. The scenarios avoid naming the technique, so decide what interval, question or tool each situation calls for before you read the options. They test recognition and prediction, which the guided exercises cannot.

### Recognition Questions

```quiz
{"id":"bs-rev-midpoint","q":"A search over int positions computes mid as (lo + hi) / 2 on an array with about two billion elements. What can go wrong?","options":["It is always off by one.","The sum lo + hi can pass the range of int and wrap negative, so mid becomes an invalid index.","It makes the loop skip the last element only.","Nothing, since indices are never that large in practice."],"answer":1,"explain":"Adding two large ints can exceed 32 bits and wrap. Writing lo + (hi - lo) / 2 never forms a sum larger than hi."}
```

```quiz
{"id":"bs-rev-closed-loop","q":"In a closed interval search with lo <= hi, the code sets hi = mid after a comparison that was not a hit. What happens on a two-element interval?","options":["It returns the right answer faster.","It throws an exception.","It may loop forever, because hi never shrinks below mid.","It skips the left element."],"answer":2,"explain":"With lo and hi adjacent, mid equals lo, so hi = mid changes nothing. A closed interval must exclude the probed position with mid - 1 or mid + 1."}
```

```quiz
{"id":"bs-rev-first-hit","q":"An array has many copies of the target and a search stops at the first position that equals it. Which request does that answer correctly?","options":["Whether the target exists.","The index of the first copy.","The index of the last copy.","The number of copies."],"answer":0,"explain":"A hit proves presence only. For a boundary the hit is a candidate, and the search continues toward the side that was asked for."}
```

```quiz
{"id":"bs-rev-bounds","q":"For a sorted array and a target larger than every element, what do the lower bound and the upper bound return?","options":["Both return minus one.","Lower returns zero and upper returns the length.","They throw an exception.","Both return the length of the array."],"answer":3,"explain":"The first position with a value at least the target and the first with a value above it both fall one past the end, so the return value n is a legal answer."}
```

```quiz
{"id":"bs-rev-predicate","q":"Which situation is a valid use of the first-true search?","options":["A yes-or-no question over positions in which every no comes before every yes.","A question whose answers alternate along the positions.","Any array, since sorting is not required.","A question that depends on the previous answer."],"answer":0,"explain":"The halving is safe only when the answers form one stretch of no followed by one stretch of yes. Alternating answers give no safe half to drop."}
```

```quiz
{"id":"bs-rev-peak","q":"In the peak search over a mountain array, the comparison a[mid] < a[mid + 1] holds. Where is a peak?","options":["At or to the left of mid.","At or to the right of mid + 1.","Only at mid.","Nowhere, so the array is invalid."],"answer":1,"explain":"A rising step means the climb continues to the right, so a peak exists at mid + 1 or beyond and the left part can be dropped."}
```

```quiz
{"id":"bs-rev-rotated-min","q":"In the search for the minimum of a rotated array of distinct values, a[mid] > a[hi]. What follows?","options":["The minimum is at mid.","The minimum is to the left of mid.","The minimum is to the right of mid.","The array is not rotated."],"answer":2,"explain":"If the middle is larger than the right end, the drop from large to small lies between them, so the minimum is in the right part."}
```

```quiz
{"id":"bs-rev-duplicates","q":"A rotated array may contain duplicates and a[mid] == a[hi]. What is the safe move for the minimum search?","options":["Discard the right half.","Discard the left half.","Return a[mid].","Shrink the right end by one, accepting a linear worst case."],"answer":3,"explain":"Equal values hide which side holds the drop. Stepping hi down by one never loses the minimum, though many equal values make the worst case O(n)."}
```

```quiz
{"id":"bs-rev-answer-space","q":"A search over speeds from 1 to the largest pile calls a check that uses a sum of ceilings. Why keep that sum in a long?","options":["Because long is faster than int.","The total of the per-item costs can pass the range of int even when each cost fits.","Because int cannot hold a ceiling.","Because the speeds are decimals."],"answer":1,"explain":"A large candidate count times many items can exceed 32 bits. The check must not wrap before it is compared with the limit."}
```

```quiz
{"id":"bs-rev-epsilon","q":"A real-valued bisection loops while hi - lo > 1e-12, and the answer is near one billion. What is the risk?","options":["The loop ends too early.","The answer is always exact.","Doubles near one billion are spaced further apart than 1e-12, so the width may never get below it and the loop may not end.","The midpoint becomes negative."],"answer":2,"explain":"When lo and hi are neighbours among doubles, the midpoint equals one of them, and the width cannot shrink. A fixed round count always ends."}
```

```quiz
{"id":"bs-rev-time-lookup","q":"A time-based store needs the value of a key at a given moment. Which design answers in O(log m) per read for a key with m changes?","options":["A map from key to the latest value only.","One list of all changes of all keys, scanned for the key.","A map from key to a list of changes in order of time, searched for the first change after the moment.","A map from time to value shared by all keys."],"answer":2,"explain":"The map selects the key's own sorted list, and the upper-bound search finds the boundary. Keeping only the latest value loses the past."}
```

```quiz
{"id":"bs-rev-matrix","q":"A matrix has sorted rows and sorted columns, but the first value of a row can be smaller than the last value of the row above. Which method is valid?","options":["Binary search over the virtual index in reading order.","Searching only the first column.","Searching only the last row.","Walking from the top right corner, discarding a row or a column per step."],"answer":3,"explain":"Reading order is not increasing here, so the virtual line has no safe half. The corner walk uses the two sorted directions instead."}
```
