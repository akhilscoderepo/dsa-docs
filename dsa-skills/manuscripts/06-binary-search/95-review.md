<!-- section: review -->
## Review

Return to this page after the lessons and again a few days later. Each question describes a situation and hides the lesson name. Commit to an answer before you open the explanation.

### Recognition Questions

```quiz
{"id": "bs-rev-closed-update", "q": "A closed-interval search on `[5]` for the target 2 uses `while (lo <= hi)` and sets `hi = mid` when `nums[mid]` is larger than the target. What happens?", "options": ["It returns -1 after one step", "The loop never ends", "It returns 0", "It throws an `ArrayIndexOutOfBoundsException`"], "answer": 1, "explain": "The values are `lo = 0`, `hi = 0` and `mid = 0`. The update `hi = mid` leaves the interval unchanged, so the same state repeats. A closed interval must drop the compared index with `hi = mid - 1`."}
```

```quiz
{"id": "bs-rev-last-match", "q": "The array `[1, 2, 2, 2, 3]` is searched for the last index of 2. At `mid = 2` the value equals 2. Which move keeps the search correct?", "options": ["Return 2 at once", "Set `hi = mid - 1`", "Save 2 as a candidate and set `lo = mid + 1`", "Set `lo = mid` and keep `hi`"], "answer": 2, "explain": "A found value is a candidate and not the answer when duplicates exist. Moving right keeps looking for a later 2. Returning at once gives index 2, but the last 2 is at index 3."}
```

```quiz
{"id": "bs-rev-insert-position", "q": "What index does the first-at-least search return for the target 4 in `[1, 3, 3, 5]`?", "options": ["2", "1", "4", "3"], "answer": 3, "explain": "The first value at least 4 is 5 at index 3, and that index is where 4 belongs. The value 4 is absent, but the search still returns a boundary and not -1."}
```

```quiz
{"id": "bs-rev-monotone-test", "q": "Which yes-or-no test over the numbers 2 to 20 is unsafe to search with a first-true loop?", "options": ["The number is at least 7", "The number squared is at least 50", "The number is prime", "The number is above 15"], "answer": 2, "explain": "A test must change once from false to true. The primality test flips several times, so a middle result says nothing about either side."}
```

```quiz
{"id": "bs-rev-peak-move", "q": "Peak search runs on `[1, 3, 5, 4, 2]` with `lo = 0` and `hi = 4`. At `mid = 2` the loop compares `nums[mid]` with `nums[mid + 1]`. What does it do?", "options": ["Sets `lo = 3`", "Sets `lo = 2`", "Returns 5 at once", "Sets `hi = 2`"], "answer": 3, "explain": "The value 5 is larger than 4, so the slope falls to the right and a peak lies at `mid` or to its left. The update `hi = mid` keeps `mid` as a candidate."}
```

```quiz
{"id": "bs-rev-rotated-min", "q": "The array is `[3, 4, 5, 1, 2]` with `lo = 0`, `hi = 4` and `mid = 2`. Which comparison and move find the minimum?", "options": ["`nums[mid] > nums[hi]` sets `lo = mid + 1`", "`nums[mid] > nums[lo]` sets `hi = mid`", "`nums[mid] < nums[hi]` sets `lo = mid + 1`", "`nums[mid] == nums[hi]` returns `mid`"], "answer": 0, "explain": "The value 5 is larger than the right end 2, so the restart lies to the right of `mid`. The comparison with the right end is always safe for distinct values."}
```

```quiz
{"id": "bs-rev-rotated-plain", "q": "A plain binary search from the first lesson runs on `[6, 7, 9, 1, 2, 3, 4]` for the target 7. What does it return?", "options": ["1", "-1", "0", "3"], "answer": 1, "explain": "The first middle value is 1, which is smaller than 7, so the search moves right and never reads index 1. The array is sorted only inside its two runs."}
```

```quiz
{"id": "bs-rev-speed-check", "q": "Piles `[5, 9, 14, 20]` must be finished in 9 hours. Speed 6 needs 1 + 2 + 3 + 4 = 10 hours. How does the answer search move?", "options": ["Sets `hi = 6`", "Returns 6", "Sets `lo = 7`", "Sets `lo = 6`"], "answer": 2, "explain": "Speed 6 fails, and every lower speed fails too, so the answer is above 6. The update `lo = mid + 1` drops the failing candidate."}
```

```quiz
{"id": "bs-rev-epsilon-loop", "q": "A search on the interval `[1, 2]` uses `while (hi - lo > 1e-20)`. Why can the loop run forever?", "options": ["The midpoint always equals `hi`", "Two neighboring `double` values near 1 differ by more than 1e-20, so the width stops shrinking", "The condition compares a `double` with an `int`", "Bisection never reaches a width below 1e-10"], "answer": 1, "explain": "The spacing of `double` values near 1 is about 2.2e-16. After about 52 halvings the midpoint equals `lo` or `hi`, and the width never falls below that spacing."}
```

```quiz
{"id": "bs-rev-time-floor", "q": "One key has changes at the times `[2, 5, 9, 14, 20]`. A query asks for time 14. Which change answers it?", "options": ["The change at time 9", "The change at time 20", "The change at time 14", "No change, because 14 is not strictly earlier"], "answer": 2, "explain": "The contract asks for the last change at or before the query. A change at exactly 14 qualifies, so the floor search steps back from the first time above 14."}
```

```quiz
{"id": "bs-rev-sorted-columns", "q": "The matrix `[[1, 4], [2, 5]]` has sorted rows and sorted columns. A virtual index search runs for the target 2. What does it return?", "options": ["`true`", "`true` after three comparisons", "`false`, although 2 is present", "It throws an exception"], "answer": 2, "explain": "Read row after row, the values are 1, 4, 2, 5, which is not ascending. The first middle value is 4, so the search moves left and ends without reading 2."}
```

### Questions To Ask Before Writing The Loop

Before the first line of a search, write down three facts in your own words. What does the interval `[lo, hi]` hold, and does it include `hi`? Which comparison decides a side, and what does each outcome prove about the discarded part? What does the loop return when the interval becomes empty? If any answer is vague, the loop is not ready. If the test over the answers can flip back, the search does not apply.
