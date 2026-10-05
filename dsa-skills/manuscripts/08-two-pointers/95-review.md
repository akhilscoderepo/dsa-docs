<!-- section: review -->
## Review

Return to this page after the lessons and again after a few days. Each question describes a situation and hides the name of the lesson. Pick an answer before you open the explanation.

### Recognition Questions

```quiz
{"id": "tp-rev-which-pointer", "q": "A sorted array is scanned from both ends. The sum of the two end values is below the target. Which move is safe?", "options": ["Move `right` one step to the left", "Move `left` one step to the right", "Move both pointers inward", "Restart the scan with a larger target"], "answer": 1, "explain": "Every pair that uses the left value and any value at or before `right` has a sum no larger than the current sum, so the left index cannot be part of an answer. Moving `right` would discard an index that could still help."}
```

```quiz
{"id": "tp-rev-unsorted-scan", "q": "Why does the opposite-end scan fail on `[12, 3, 5, 8]` with target 13?", "options": ["The array has an even length", "The sum overflows `int`", "The order does not support the elimination, so the scan drops the index of 5 or 8 too early", "The target is too small"], "answer": 2, "explain": "The claim that a smaller left value gives smaller sums needs sorted order. In this array the scan sees sums that are all too large and discards the values that form the pair `5 + 8`."}
```

```quiz
{"id": "tp-rev-write-count", "q": "A read and write scan ends with `write = 4`. What does `write` mean?", "options": ["The index of the last unread value", "The number of values kept, which equals the length of the kept prefix", "The number of values removed", "The number of swaps performed"], "answer": 1, "explain": "The write index is the next free slot of the output, so it equals the number of kept values. The values after it are stale and must not be read as part of the answer."}
```

```quiz
{"id": "tp-rev-negative-parity", "q": "Which Java test decides that an `int` x is odd for every value, including negative ones?", "options": ["`x % 2 == 1`", "`x % 2 != 0`", "`x / 2 == 0`", "`x > 0 && x % 2 == 1`"], "answer": 1, "explain": "A negative odd value gives `-3 % 2 == -1`, so the test `== 1` misses it. The test `x % 2 != 0` is true for odd values of either sign."}
```

```quiz
{"id": "tp-rev-mid-wait", "q": "In the three-way scan, `nums[mid]` belongs to the third group and swaps with `nums[high]`. What happens to `mid`?", "options": ["It advances, because the slot is settled", "It moves back by one", "It stays, because the value that arrived from `high` is unread", "It jumps to `high`"], "answer": 2, "explain": "The value that arrives from the far end has not been inspected. It can belong to any of the three groups, so the scan must look at it in the next iteration."}
```

```quiz
{"id": "tp-rev-mid-bound", "q": "Which loop condition lets the three-way scan inspect the slot at `high`?", "options": ["`mid < high`", "`mid <= high`", "`mid != low`", "`low < high`"], "answer": 1, "explain": "The slot at `high` is still unresolved when `mid == high`. The condition `mid < high` stops one slot early and can leave a value in the wrong group."}
```

```quiz
{"id": "tp-rev-skip-order", "q": "In the pair scan with skipping, when does the scan skip equal values after a match?", "options": ["Before the match is recorded", "Only at the start of the loop", "After the match is recorded", "Never, because a set removes repeats"], "answer": 2, "explain": "A skip before the evaluation can discard the only representative of a run. For `[2, 2]` with target 4, skipping first loses the pair."}
```

```quiz
{"id": "tp-rev-four-cost", "q": "A reduction fixes two values and then runs one pair scan on a sorted array of `n` values. What is the time cost, ignoring the sort?", "options": ["O(n)", "O(n^2)", "O(n^3)", "O(n^4)"], "answer": 2, "explain": "Each fixed value adds one loop of up to `n` iterations, and the pair scan costs O(n). Two fixed loops and one scan give O(n^3)."}
```

```quiz
{"id": "tp-rev-long-sum", "q": "Three `int` values near 2,147,483,647 are added in an `int` variable. What happens?", "options": ["Java throws an exception", "The sum wraps to a wrong value without an error", "The sum saturates at the maximum", "The compiler rejects the addition"], "answer": 1, "explain": "Integer addition in Java wraps silently. The sum 2,147,483,647 + 2,147,483,647 + 2 becomes 0 in `int`, which is why the sums in these lessons use `long`."}
```

```quiz
{"id": "tp-rev-packed-key", "q": "A packed key is `((long) value << 32) | row`. After sorting the keys, how do you read the row?", "options": ["`(int) (key >> 32)`", "`(int) key`", "`key % 32`", "`key / 32`"], "answer": 1, "explain": "The low 32 bits hold the row, and the cast `(int) key` keeps exactly those bits. The shift by 32 recovers the value instead."}
```

```quiz
{"id": "tp-rev-phase-two", "q": "After the two pointers meet in phase one, `slow` restarts at slot 0. How does each pointer move in phase two?", "options": ["Both move one link per round", "`slow` moves one link and `fast` moves two", "Both move two links per round", "Only `fast` moves"], "answer": 0, "explain": "Equal speeds keep the two pointers the same number of links from the entry point, so they meet exactly at the entry point, which is the repeated value."}
```
