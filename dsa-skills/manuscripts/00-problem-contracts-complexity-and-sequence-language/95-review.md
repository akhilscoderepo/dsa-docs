<!-- section: review -->
## Review

Use this section after you finish the lessons, and again a few days later. The questions describe situations without naming the lesson topic, so decide before you open the options. They test recognition and prediction. The guided exercises do not test those.

### Recognition Questions

```quiz
{"id":"pc-rev-budget","q":"A problem allows n up to 200,000 and asks for the count of pairs with a given difference. A colleague proposes checking every pair. What does the input constraint imply?","options":["Fine, because the sample has only six values.","Too slow: about 2 * 10^10 pair checks is far past a limit of about 10^8 basic operations.","Fine, because pairs are checked with simple subtraction.","Too slow only if the values are negative."],"answer":1,"explain":"The count of pairs is n * (n - 1) / 2, which at n = 200,000 is about 2 * 10^10. The sample size is irrelevant, and the cost of each comparison does not change the time complexity class."}
```

```quiz
{"id":"pc-rev-mutation","q":"A method must return the elements of nums greater than 10, and the statement says the caller keeps using nums afterward. Which design is correct?","options":["Overwrite nums in place and return the new length.","Allocate and return a new array, leaving nums unchanged.","Sort nums first, then overwrite the prefix.","Set the unwanted slots to zero in place."],"answer":1,"explain":"The statement forbids visible changes to the input, so an in-place rewrite breaks the interface even though it is faster. Allocating the result costs O(n) space and respects the specification."}
```

```quiz
{"id":"pc-rev-sequence","q":"For nums = [3, 1, 4, 1, 5], the candidate [3, 4, 5] is which of the following?","options":["A subarray, a subsequence and a subset.","A subsequence and a subset, but not a subarray.","Only a subset.","None of the three."],"answer":1,"explain":"The positions of 3, 4 and 5 are 0, 2 and 4. They increase, so the order is kept. They skip positions 1 and 3, so the block is not contiguous."}
```

```quiz
{"id":"pc-rev-guarantee","q":"A statement promises that the array is non-empty. Which first line of a maximum-finding method matches the promise?","options":["if (nums.length == 0) return 0; int best = 0;","int best = nums[0];","int best = Integer.MAX_VALUE;","int best = -1;"],"answer":1,"explain":"The first element is a real member of the input, so it is a valid initial value. Zero and -1 assume every element exceeds those values. The empty guard defines a behavior the statement never asks for."}
```

```quiz
{"id":"pc-rev-cost","q":"Method A scans an array twice in sequence. Method B scans it once but, for each element, scans the elements after it. Which statement is correct?","options":["Both are O(n^2) because each has two loops.","A is O(n) and B is O(n^2).","A is O(n^2) and B is O(n).","Both are O(n) because each loop is a single scan."],"answer":1,"explain":"Sequential loops add, so A costs 2n. Nested loops multiply, so B costs about n^2 / 2. Counting executions of the inner statement settles it."}
```

```quiz
{"id":"pc-rev-amortized","q":"A growable array doubles its capacity when full. Which claim about append is accurate?","options":["Every append is O(1) in the worst case.","Appends are O(1) amortized, although one append can cost O(n).","Appends are O(n) amortized because of the copying.","Appends are O(log n) amortized."],"answer":1,"explain":"Each doubling copies as many elements as the appends since the previous doubling added, so the total is linear in the number of appends. A single call can still take O(n)."}
```

```quiz
{"id":"pc-rev-dryrun","q":"Your method returns the longest run of equal values. Which single input best tests its initialization?","options":["A random array of 100,000 values.","A single-element array.","An array sorted in descending order.","An array with a negative first value."],"answer":1,"explain":"With one element the loop body never runs, so the result comes entirely from the initial values of the variables. Random data rarely reaches that case."}
```

```quiz
{"id":"pc-rev-java","q":"Which line inside a loop over n items can silently make the loop quadratic?","options":["total += list.get(i);","list.remove(0);","builder.append(ch);","count++;"],"answer":1,"explain":"Removing at index 0 of an ArrayList shifts every later element, so each call costs O(n). The other lines are constant or amortized constant per call."}
```

### Recall Exercises

Close this page and answer from memory, then check against the lessons. State the preconditions, postconditions and mutation rules for a problem of your choice in five lines. Write the loop that counts the steps of a nested loop whose inner index starts one past the outer index, and give its closed form. Explain in two sentences why a doubling array has amortized constant append cost, using either the aggregate method or the accounting method. Name three Java calls whose time complexity or meaning surprises people in a loop. State the lower-cost alternative for each.
