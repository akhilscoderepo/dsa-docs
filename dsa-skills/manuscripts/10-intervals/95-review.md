<!-- section: review -->
## Review

Return to this page after the lessons and again after a few days. Each question describes a situation and hides the name of the lesson. Pick an answer before you open the explanation.

### Recognition Questions

```quiz
{"id": "iv-rev-sort-key", "q": "A scan must merge overlapping closed intervals using one comparison with the last merged interval. Which sort key makes that comparison enough?", "options": ["Start", "End", "Length", "Arrival order"], "answer": 0, "explain": "With starts in order, every later start is at least the last start, so only the largest end seen so far can reach it. Sorting by end breaks this, because a long interval with a late end comes last and meets several earlier ones."}
```

```quiz
{"id": "iv-rev-subtraction", "q": "A comparator returns `a[0] - b[0]`. What can go wrong?", "options": ["Nothing, because the sort only needs the sign", "The sort becomes unstable", "The comparator ignores equal starts", "The subtraction can overflow and give the wrong sign"], "answer": 3, "explain": "For starts such as -2,000,000,000 and 2,000,000,000 the true difference does not fit in an int. The stored value wraps to the opposite sign, so the sort places the larger start first. Integer.compare avoids the subtraction."}
```

```quiz
{"id": "iv-rev-touching", "q": "Two half-open intervals `[1,3)` and `[3,5)` are tested. Which result is correct?", "options": ["They overlap, because both contain 3", "They overlap, because they share an end value", "They do not overlap, because the first excludes 3", "The answer depends on which interval is listed first"], "answer": 2, "explain": "A half-open interval excludes its end, so no coordinate lies in both. The larger start 3 is not below the smaller end 3, so the strict test fails. Under the closed model the same numbers overlap at 3."}
```

```quiz
{"id": "iv-rev-active-end", "q": "A merge scan joins `[2,3]` to the active interval `[1,10]`. What must the active end become?", "options": ["3, the end of the newest interval", "10, the larger of the two ends", "13, the sum of the ends", "2, the start of the newest interval"], "answer": 1, "explain": "The active end is the largest end seen in the group. Setting it to 3 would shrink the interval and lose the coverage of 4 through 10, and a later interval such as `[4,5]` would be split off wrongly."}
```

```quiz
{"id": "iv-rev-cursor", "q": "Two sorted lists of disjoint intervals are intersected with two cursors. After a pair is recorded, which cursor advances?", "options": ["The one whose interval starts first", "Always the first list", "The one whose interval ends first", "Both cursors"], "answer": 2, "explain": "The interval with the smaller end cannot meet anything later in the other list, because later intervals there start after the other current interval ends. Advancing the one that starts first can skip an interval that still meets the next one."}
```

```quiz
{"id": "iv-rev-covered-tie", "q": "A scan removes covered intervals after sorting by start. Why must equal starts be ordered by larger end first?", "options": ["So that the container comes before the interval it holds", "So that the sort is stable", "So that the scan can stop early", "So that touching intervals merge"], "answer": 0, "explain": "With `[1,4)` and `[1,2)`, putting `[1,2)` first makes it look uncovered because no earlier end reaches 2. Putting `[1,4)` first lets the running maximum end 4 show that `[1,2)` is covered."}
```

```quiz
{"id": "iv-rev-tie-policy", "q": "Half-open sessions `[1,4)` and `[4,6)` are swept as events. In what order do the two events at coordinate 4 run?", "options": ["The start first, because starts raise the count", "The end first, because the first session no longer holds 4", "Either order gives the same peak", "The order of the input decides"], "answer": 1, "explain": "The half-open model excludes the end, so the first session frees its place at 4 before the second takes one. Running the start first reports a peak of 2, which never happens at any single coordinate."}
```

```quiz
{"id": "iv-rev-heap-wait", "q": "A problem asks which room each meeting uses, not only how many rooms are busy at once. What does a sweep lack for this?", "options": ["A sort key", "The identity of the interval that ends next", "A tie policy", "A model for ends"], "answer": 1, "explain": "A sweep counts active intervals but does not say which one finishes first. Chapter 17 adds a heap ordered by end time, which returns that interval and makes room assignment possible."}
```
