<!-- section: review -->
## Review

Return to this section after the lessons and again after a few days. The scenarios avoid naming the technique, so decide what the window holds, what makes it valid and what repairs it before reading the options. They test recognition and prediction, which the guided exercises cannot.

### Recognition Questions

```quiz
{"id":"sw-rev-fixed-slide","q":"A fixed window of length k slides one step. What does the update do?","options":["Recompute the whole sum.","Add the entering item and subtract the leaving item.","Sort the window.","Subtract the first item only."],"answer":1,"explain":"The window changes by one item at each end, so the summary changes by those two items and the work per step is constant."}
```

```quiz
{"id":"sw-rev-fixed-frequency","q":"A pattern is aab. Why is a set of letters the wrong summary for a window match?","options":["Sets are slower.","A set cannot hold the letter twice, so it cannot represent multiplicity.","Sets need sorting.","Sets drop the order."],"answer":1,"explain":"A match needs two copies of a. Only counts can represent how many copies are present."}
```

```quiz
{"id":"sw-rev-longest-shrink","q":"In a longest-valid window, one new right item breaks the rule. What may be needed?","options":["Restart at the right edge.","Move the left edge several times until the window is valid again.","Ignore the item.","Double the window."],"answer":1,"explain":"One entering item can require many leaving items before the window is valid again, so shrinking is a loop."}
```

```quiz
{"id":"sw-rev-cover-record","q":"In a minimum cover window, when is the best length recorded?","options":["While the window is invalid.","Whenever the window covers the demand, before the left edge moves on.","Only at the end.","After the right edge has reached the end."],"answer":1,"explain":"Each covering window is a candidate. The shrink loop then tries to find a shorter one while the demand stays met."}
```

```quiz
{"id":"sw-rev-atmost-distinct","q":"A map counts values in the window. What must happen when a count falls to zero?","options":["Nothing.","The key is removed so the size of the map equals the number of distinct values.","The window is reset.","The right edge moves back."],"answer":1,"explain":"The distinct count is the size of the map only if keys with zero count are removed."}
```

```quiz
{"id":"sw-rev-exactly-k","q":"How is the number of stretches with exactly k odd values obtained?","options":["atMost(k) + atMost(k-1)","atMost(k) - atMost(k-1)","atMost(k) * 2","atMost(k-1) - atMost(k)"],"answer":1,"explain":"A stretch with at most k and not at most k-1 has exactly k. The difference counts exactly those."}
```

```quiz
{"id":"sw-rev-stale-max","q":"In the replacement budget window, the tracked maximum frequency is never lowered. Why is the answer still right?","options":["The maximum is always exact.","A stale maximum cannot make the window longer than the best length ever proved reachable.","The window is reset.","The budget is ignored."],"answer":1,"explain":"The window only grows when a new true maximum appears, so a stale value never inflates the best length."}
```

```quiz
{"id":"sw-rev-count-valid","q":"Counting all subarrays with sum below k over positive values: for a right edge, how many valid stretches end there?","options":["Always one.","The window length after the shrink.","The distance to the array start.","k."],"answer":1,"explain":"Every start from the left edge to the right edge gives a valid stretch, so the count added is the current length."}
```

```quiz
{"id":"sw-rev-nonshrink","q":"A non-shrinking policy moves the left edge by at most one per step. What is the loss?","options":["The answer is wrong.","The window can be invalid in between, so only its length, not its content, is meaningful.","It needs sorting.","It uses more memory."],"answer":1,"explain":"The policy keeps the window length at the best seen, which is enough for the length answer, but the window content may not satisfy the rule."}
```

```quiz
{"id":"sw-rev-negative","q":"A task asks for the shortest stretch with sum at least k and values can be negative. Why can the usual window fail?","options":["Negative values need long.","Shrinking from the left no longer makes the sum smaller in a controlled way, so validity is not monotone.","The array must be sorted.","Windows need a map."],"answer":1,"explain":"With negatives, adding an item can lower the sum and removing one can raise it, so the repair argument of the window no longer holds."}
```
