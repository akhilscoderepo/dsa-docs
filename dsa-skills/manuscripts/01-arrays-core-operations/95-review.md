<!-- section: review -->
## Review

Come back to this section once the lessons are done, and once more after a few days. Each question describes a situation without naming the technique, so commit to an answer before looking at the options. The questions test recognition and prediction, which a guided ladder of exercises cannot.

### Recognition Questions

```quiz
{"id":"ar-rev-frequency","q":"A log holds up to 100,000 user ids, each between 1 and 1,000,000,000, and you must count how often each id appears. Which statement is right?","options":["A frequency array of size 100,001 is enough.","A frequency array indexed by id needs about a billion slots, so the bounded-domain promise is missing.","A frequency array works if the ids are first made negative.","A frequency array works only if the log is sorted."],"answer":1,"explain":"A frequency array needs one slot per possible value, and the problem does not promise a small range. A hash map from a later chapter counts arbitrary keys at a memory cost proportional to the distinct ids."}
```

```quiz
{"id":"ar-rev-sorted-dedup","q":"The sorted-deduplication loop, which compares each element with the last kept value, is run on [4, 9, 4, 9]. What happens?","options":["It returns 2 with the prefix [4, 9].","It keeps all four elements, because equal values are not adjacent.","It throws an exception on the second 4.","It returns 3 with the prefix [4, 9, 4]."],"answer":1,"explain":"Each element differs from the last kept value, so every element is admitted. The loop needs equal values to be neighbors, and unsorted data breaks that promise without any error."}
```

```quiz
{"id":"ar-rev-majority","q":"The majority vote is run on [1, 2, 3] and ends with the candidate 3. What should you conclude?","options":["3 is the majority element.","No majority exists, and that is known without further work.","3 is only a candidate, and a counting pass is needed to learn that it is not a majority.","The vote must have a bug, because the survivor should be 1."],"answer":2,"explain":"The ritual always ends with some candidate. Only a majority that exists is guaranteed to survive, so without the guarantee a second pass must count the candidate."}
```

```quiz
{"id":"ar-rev-placement-duplicates","q":"In cyclic placement, the loop swaps nums[i] into slot nums[i] - 1 while nums[i] != i + 1. On [2, 2] it never finishes. What is the repair?","options":["Use if instead of while.","Stop swapping when nums[i] equals nums[nums[i] - 1].","Sort the array first.","Swap in the other direction."],"answer":1,"explain":"Swapping two equal values changes nothing, so the loop spins. Comparing the cursor's value with the value in its home slot detects the duplicate and stops."}
```

```quiz
{"id":"ar-rev-sign-read","q":"During sign marking on values in 1..n, the cursor reaches a slot that an earlier step made negative. What must the code do before using the slot's value as an index?","options":["Use the value directly, since negative indices wrap around in Java.","Take the absolute value, because a negative number minus one is not a valid index.","Skip the slot, because it carries no information.","Reset the slot to positive."],"answer":1,"explain":"Marking only changes the sign, so the magnitude is still the original value. Java does not wrap negative indices, and resetting the sign would erase the record."}
```

```quiz
{"id":"ar-rev-kadane-negative","q":"A Kadane implementation starts both the ending state and the best at 0 instead of at the first element. On [-8, -3, -6] it returns 0. What went wrong?","options":["Nothing, 0 is the largest possible sum.","It allowed an empty stretch, but the contract demands a non-empty one, so the answer should be -3.","The array has no valid answer.","It should have returned -8, the first element."],"answer":1,"explain":"A zero start lets the empty stretch win whenever every value is negative. Starting from the first element protects the non-empty contract and yields the largest single value."}
```

```quiz
{"id":"ar-rev-product","q":"For the maximum product subarray, why does a single running best-ending product fail on [2, -1, 3, -2, 2]?","options":["Products overflow before the end.","A negative factor can turn the worst earlier product into the best, so the minimum must be kept too.","The zero case breaks it, and this array has a zero.","Multiplication is not associative."],"answer":1,"explain":"At the factor -2 the best answer comes from the earlier product -6, which a method that kept only the largest would have discarded. Keeping the maximum and the minimum, and swapping them on a negative, solves it."}
```

```quiz
{"id":"ar-rev-circular","q":"For a circular array, the wrapping maximum is computed as the total minus the minimum straight subarray. For [-3, -2, -3] this formula gives 0. What does that mean?","options":["The answer is 0.","The excluded block is the whole array, so the wrap candidate is empty and the answer is the ordinary maximum, -2.","The array must be rotated first.","The minimum subarray was computed wrongly."],"answer":1,"explain":"When every value is negative, the smallest straight block is the entire array and nothing is left to wrap. The guard returns the ordinary maximum, which is the largest single element."}
```

```quiz
{"id":"ar-rev-gain-vs-kadane","q":"An array of daily price changes is given, and you want the best sum of consecutive days. A teammate suggests the running-minimum scan used for stock gain. Why is that the wrong tool?","options":["It is too slow for long arrays.","It chooses two positions and reports a difference of prices, while this objective is a sum over a contiguous block, which needs the ending state.","It cannot handle negative numbers.","It only works on sorted data."],"answer":1,"explain":"The best-gain scan answers a buy-and-sell question on prices. Daily changes are already differences, and the sum of a block calls for the extend-or-restart recurrence."}
```

```quiz
{"id":"ar-rev-compaction","q":"After an in-place removal that returns k, a caller reads the whole array. Which part of the array is meaningful, if the contract says nothing more?","options":["All n elements.","Only the first k elements.","Only the last k elements.","Only the elements that were not removed, wherever they are."],"answer":1,"explain":"The returned count defines the valid prefix, and the slots after it are unspecified unless the contract says otherwise. The write index tells you where the prefix ends."}
```
