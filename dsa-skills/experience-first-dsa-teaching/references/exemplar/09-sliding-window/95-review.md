<!-- section: review -->
## Review

Use this section after you have finished the ladders, and again a few days later. It tests recognition, prediction and rebuilding, which are the three things an interview asks of you and a ladder of guided exercises does not.

### Recognition Questions

Each question describes a situation without naming the technique. Decide before you open the options.

```quiz
{"id":"sw-rev-exact-odds","q":"All values are positive integers. You must count the contiguous subarrays containing exactly three odd numbers. Which approach gives O(n) time?","options":["One window that always holds exactly three odd numbers and counts its size.","Count subarrays with at most three odd numbers, count those with at most two, and subtract.","Sort the array and count pairs of positions.","Slide a fixed window of length three."],"answer":1,"explain":"An exact count has no unique left boundary, because removing a leading even number keeps the count exact. The at-most counts are monotone, so each is a plain window, and the difference isolates the exact case."}
```

```quiz
{"id":"sw-rev-shortest-sum","q":"For an array of positive integers, you want the shortest subarray whose sum is at least a target. Where in the loop do you record the length?","options":["After the repair loop, as in the longest-valid pattern.","Inside the shrink loop, before removing the leftmost value, while the window still meets the target.","Only once at the end of the array.","Before the new value is added."],"answer":1,"explain":"The goal is the shortest valid window, so the window shrinks while it is valid and the length is recorded before each removal, because the removal may be the one that breaks validity."}
```

```quiz
{"id":"sw-rev-signature","q":"A task asks whether any block of exactly k letters is a rearrangement of a given word. Why is a running sum of letter codes not enough?","options":["The sum overflows an int for every input.","Different multisets of letters can produce the same sum, so the summary is too weak.","Sums cannot be updated when a value leaves the window.","The window length is not fixed."],"answer":1,"explain":"A single number cannot tell two different multisets apart. The summary has to be a table of counts, the frequency signature, so that equality of tables means equality of contents."}
```

```quiz
{"id":"sw-rev-while-if","q":"Which statement about replacing the repair `while` with an `if` is correct?","options":["It is a safe optimization for every window problem because both loops run in O(n).","It is never correct, because one arrival can need several removals.","It can be correct for a longest-length question when validity is monotone and the test covers the whole window or comes with a proof, but not for questions that use the boundaries.","It is correct whenever the code checks only the count of the arriving element."],"answer":2,"explain":"The non-shrinking form keeps only a candidate length, so it needs an exact whole-window test or a proof, and it cannot support counting windows or reporting the best stretch. A check on the arriving element alone fails on inputs such as abba."}
```

```quiz
{"id":"sw-rev-zero-key","q":"A distinct-count window keeps a HashMap of counts but never removes a key whose count reaches zero. What goes wrong?","options":["The map throws an exception on the next lookup.","map.size() overstates the number of distinct values in the window, so the window shrinks too much and the answer is too small.","The counts become negative.","Nothing, because a zero count is ignored by size()."],"answer":1,"explain":"size() counts keys, not positive counts. A stale zero entry makes the budget look exceeded, so the loop shrinks more than it should and the reported length is too short, with no error message."}
```

```quiz
{"id":"sw-rev-negative-sum","q":"You must count subarrays whose sum is below k, and the array may contain negative numbers. Why does the count-all window fail?","options":["The count can overflow an int.","Removing a value from the left can raise the sum, so the valid starts are not an unbroken block ending at the right edge.","The window cannot become empty.","Negative numbers cannot be stored in a window."],"answer":1,"explain":"The addition of right - left + 1 relies on validity being monotone when a prefix is removed. With negatives that fails, and the problem needs a different tool such as prefix sums with an ordered structure."}
```

### Prediction Questions

```quiz
{"id":"sw-rev-stale-max","q":"In the replacement-budget window, the stored maximum is raised on arrival and never lowered. After a departure it may exceed the true dominant count of the window. What does the reported length still guarantee?","options":["The current window is valid.","Some window of that length can be made uniform with at most k replacements.","The reported length equals the current window length minus k.","The best window starts at left."],"answer":1,"explain":"A length of stored maximum plus k is reached only after a real window had that dominant count, so the length is achievable, even though the current window may not be. That is why the method returns a length and cannot return the window."}
```

```quiz
{"id":"sw-rev-overshoot","q":"An arriving letter pushes its count above its requirement. How should the status counter treat that slot in a permutation check, and in a cover check?","options":["Bad in both.","Good in both.","Bad for the permutation check, fine for the cover check.","Fine for the permutation check, bad for the cover check."],"answer":2,"explain":"A permutation needs equality, so an overshoot breaks it. A cover needs at least the requirement, so surplus copies are allowed and the window may still pass."}
```

### Rebuild Checks

Close the lesson and the editor, and write each of these from a blank page, with a timer of fifteen minutes each. Then compare with the lesson and note which line you got wrong.

First, write the minimum-cover window for a requirement string over arbitrary characters. Your answer must state the invariant that the outstanding count is zero exactly when the window covers, record the boundaries before each removal, and build the substring once. Second, write the exactly-K counter for distinct values, including the budget of minus one, and say why the guard for that budget is needed. Third, write the replacement-budget window with a stored maximum, and write the two sentences that justify why it cannot report a length that no window can reach.

### The Review Loop

After three or four chapters, return here with one problem you have not seen, one you previously failed, and one that you explain aloud without an editor. For each, record the recognition cue you missed, the invariant you failed to maintain, or the boundary that caused the bug, and review the decision rather than the final code.
