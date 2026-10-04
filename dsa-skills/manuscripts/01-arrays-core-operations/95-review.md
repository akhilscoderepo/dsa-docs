<!-- section: review -->
## Review

Return to this page after the lessons and again after a few days. Each question describes a situation and hides the lesson name. Commit to an answer before you read the options.

### Recognition Questions

```quiz
{"id":"ar-rev-scan-exit","q":"A method must return the index of the last even number in an array. How should the loop behave after it finds an even number?","options":["Return the index at once, because the match is final.","Record the index and continue, because a later position may match.","Stop the loop and return -1.","Sort the array and read the final cell."],"answer":1,"explain":"Only the first match is final in a first-match search. A last-match search must examine every position and overwrite the stored index on each match."}
```

```quiz
{"id":"ar-rev-initial","q":"A method finds the largest value of an array that holds only negative integers. Which starting value for the maximum is correct?","options":["0","Integer.MAX_VALUE","nums[0], with the loop starting at index 1","-1"],"answer":2,"explain":"Zero and -1 both exceed some legal inputs, so they can be returned although they are not in the array. The first element is a real member, which makes the promise about the examined prefix true from the start."}
```

```quiz
{"id":"ar-rev-gain","q":"For prices [7, 2, 5, 1, 6], what is the best profit from one buy followed by a later sell?","options":["4","5","3","6"],"answer":1,"explain":"The running minimum reaches 1 at index 3, and the price 6 at index 4 gives 6 - 1 = 5. The value 4 comes from buying at 2 and selling at 6, which is smaller."}
```

```quiz
{"id":"ar-rev-compact","q":"During in-place removal of all zeros from the array, what does the return value `write` tell the caller?","options":["The index of the last zero.","The number of valid values in the prefix, which is the only part with a defined meaning.","The number of zeros removed.","The new length of the Java array."],"answer":1,"explain":"The method returns the count of kept values. The array length never changes, and the cells from `write` onward still hold old values."}
```

```quiz
{"id":"ar-rev-dedup","q":"In a sorted array, the scan compares `nums[read]` with `nums[write - 1]`. Why does comparing with the last written value work?","options":["Because equal values are always adjacent, so the last kept value is the only possible duplicate.","Because the array is unsorted after compaction.","Because the write index can pass the read index.","Because the comparison replaces the sort."],"answer":0,"explain":"In sorted order, every copy of a value sits inside one run. A value that equals the last kept value belongs to the run already represented."}
```

```quiz
{"id":"ar-rev-frequency","q":"The input holds 1,000,000 exam scores, and every score is an integer from 0 to 100. Which plan has the lowest cost?","options":["Sort the scores, then count runs.","Allocate an array of 101 counters and increment `count[score]` for each score.","Compare every pair of scores.","Store the scores in a list and call `contains` for each one."],"answer":1,"explain":"The domain is small and bounded, so the value is its own index. The method runs in O(n) time and O(1) extra space, because 101 slots do not depend on n."}
```

```quiz
{"id":"ar-rev-majority","q":"The cancellation scan ends with candidate 4 on the array [4, 1, 4, 2, 3]. What must the method do next?","options":["Return 4, because the scan found it.","Return 4 only after a second pass counts it, because no majority may exist.","Return the last value.","Run the scan again from the right."],"answer":1,"explain":"The scan guarantees the candidate only when a majority exists. Here 4 occurs twice in five positions, which is not more than half, so the verification count rejects it."}
```

```quiz
{"id":"ar-rev-cyclic","q":"A cyclic placement loop swaps `nums[i]` with `nums[nums[i] - 1]` and finds equal values in both cells. What goes wrong without a guard?","options":["The array becomes sorted.","The loop repeats the same swap forever.","The loop skips the next index.","The method returns early."],"answer":1,"explain":"A swap of two equal values changes nothing, and the pointer does not advance after a swap. The loop would repeat the same state without end, so the guard must advance the pointer."}
```

```quiz
{"id":"ar-rev-sign","q":"A sign-marking scan reads a cell that an earlier step already made negative. Which expression gives the value that the cell stands for?","options":["nums[i]","Math.abs(nums[i])","-nums[i] - 1","nums[i] * nums[i]"],"answer":1,"explain":"A mark changes only the sign, so the magnitude still names the number. Using the raw negative value as an index would point before the array."}
```

```quiz
{"id":"ar-rev-kadane","q":"For nums = [2, -5, 3, 4], what is `bestEndingHere` after index 3?","options":["7","4","3","4 + 3 - 5 + 2 = 4"],"answer":0,"explain":"After index 1 the value is -3, so index 2 starts fresh at 3. Then 3 + 4 = 7 at index 3. The answer 4 would drop the earlier positive part."}
```

```quiz
{"id":"ar-rev-product","q":"A scan keeps the largest and the smallest product ending at each index. Why does the smallest product matter when the next value is negative?","options":["A negative value reverses the order, so the smallest product becomes the largest.","A negative value resets both products to zero.","The smallest product is always the answer.","It replaces the need to read the next value."],"answer":0,"explain":"Multiplying by a negative number maps the smallest product to the largest candidate. Dropping the minimum would miss pairs of negatives."}
```

```quiz
{"id":"ar-rev-circular","q":"For a circular array whose values are all negative, the formula `totalSum - minimumOrdinary` gives 0. What should the method return?","options":["0, because the formula gave it.","The ordinary maximum, which is the largest single value.","The total sum.","The most negative value."],"answer":1,"explain":"The whole array was the smallest ordinary subarray, so the leftover is empty. An empty subarray is not allowed, and the ordinary maximum is the correct answer."}
```

### Recall Exercises

Close this page and write each answer from memory, then check it against the lessons. State the invariant of an accumulator that counts matches, and say what it claims before the first element. Write the compaction loop with its read index and write index, and explain why the write index never passes the read index. Explain in two sentences why a count array needs a range check. Describe the update step that turns Kadane's algorithm into the product version, and name the case that forces the second variable.
