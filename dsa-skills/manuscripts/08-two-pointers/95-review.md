<!-- section: review -->
## Review

Return to this section after the lessons and again after a few days. The scenarios avoid naming the technique, so decide which two positions, which promise and which safe move each situation calls for before reading the options. They test recognition and prediction, which the guided exercises cannot.

### Recognition Questions

```quiz
{"id":"tp-rev-sorted-pair","q":"A sorted array is scanned from both ends and the pair sum is larger than the target. Which move is safe?","options":["Move the left pointer right.","Move the right pointer left.","Move both pointers inward.","Stop, since no pair exists."],"answer":1,"explain":"The right value is paired with the smallest remaining left value already, so every pair that uses it is at least as large. It can be discarded."}
```

```quiz
{"id":"tp-rev-write-prefix","q":"In a read and write scan, what does the written prefix promise?","options":["It holds the original first values.","It already satisfies the final contract for the input read so far.","It is sorted.","It has no duplicates in every problem."],"answer":1,"explain":"The write pointer marks the length of finished output. Each problem decides what finished means, and the prefix always meets that meaning."}
```

```quiz
{"id":"tp-rev-partition-order","q":"A task asks to put all even numbers before all odd numbers and does not care about internal order. Which design uses the fewest writes?","options":["Stable compaction into a new array.","Swapping misplaced values from opposite regions.","Sorting with a comparator.","A hash map from parity to list."],"answer":1,"explain":"Two regions without an order promise let a misplaced pair trade places once, instead of shifting everything between them."}
```

```quiz
{"id":"tp-rev-mid-after-swap","q":"In a three-way partition, the middle value is swapped with the high pointer. Why must the middle pointer stay?","options":["The swapped-in value is unresolved.","The high pointer has moved past it.","The low region has grown.","The swap changed the length."],"answer":0,"explain":"The value that arrives from the unresolved end has not been classified yet, so it must be inspected before the middle pointer advances."}
```

```quiz
{"id":"tp-rev-skip-order","q":"When is it safe to skip a repeated value in a sorted search for distinct combinations?","options":["Before the first copy is processed.","Only after one representative has been fully processed.","Never, because duplicates are valid.","Only when the array is unsorted."],"answer":1,"explain":"Skipping first can discard the only copy of a valid answer. A representative must be handled, and then equal copies add nothing new."}
```

```quiz
{"id":"tp-rev-long-sum","q":"Four values near the int maximum are added in a four-sum search. What prevents a wrong comparison?","options":["Sorting the array first.","Computing the sum in long.","Skipping equal values.","Using fewer pointers."],"answer":1,"explain":"The int sum can wrap negative and compare wrongly. A long sum cannot overflow with four int terms."}
```

```quiz
{"id":"tp-rev-floyd-entry","q":"In Floyd's cycle method, why do two pointers moving one step each, one starting at the origin and one at the meeting point, meet at the cycle entry?","options":["They always meet at index zero.","The distance from the origin to the entry equals the distance from the meeting point onward to the entry, modulo the cycle length.","The fast pointer catches the slow one again.","Both pointers run the same number of laps."],"answer":1,"explain":"At the first meeting the fast pointer has travelled twice as far as the slow one. That makes the tail length equal to the remaining walk to the entry modulo the cycle."}
```

```quiz
{"id":"tp-rev-sorted-needed","q":"Which situation does NOT allow the sorted pair scan from both ends?","options":["A sorted array and an exact target.","A sorted array and the closest sum.","An unsorted array with no promise.","A sorted array with repeated values."],"answer":2,"explain":"Without order, moving an endpoint is a guess, because nothing proves that the discarded value cannot take part in a better pair."}
```

```quiz
{"id":"tp-rev-string-rates","q":"Is Subsequence uses two pointers over two strings. What distinguishes it from a palindrome check?","options":["It needs sorting.","Both pointers travel left to right at different rates.","It uses a hash map.","It allows one deletion."],"answer":1,"explain":"The pointers do not converge. One advances on every step and the other only on a match, so the palindrome movement rule does not apply."}
```

```quiz
{"id":"tp-rev-readonly","q":"A task promises the array must not be modified. Which technique is ruled out for finding a duplicate?","options":["Floyd's cycle walk.","Sorting a copy.","Negating values to mark visits.","A hash set."],"answer":2,"explain":"Marking visits by changing signs writes into the input. The cycle walk only reads, so it respects the promise."}
```
