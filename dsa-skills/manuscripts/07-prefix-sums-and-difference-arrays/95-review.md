<!-- section: review -->
## Review

Return to this page after the lessons and again after a few days. Each question describes a situation and hides the name of the lesson. Pick an answer before you open the explanation.

### Recognition Questions

```quiz
{"id": "ps-rev-first-entry", "q": "A stored array `prefix` has length `nums.length + 1` and holds sums. What does `prefix[0]` hold?", "options": ["The value `nums[0]`", "The value 0", "The value -1", "The value `nums.length`"], "answer": 1, "explain": "The entry `prefix[0]` is the sum of zero values, which is 0. It lets every window formula read a valid entry, even when the window starts at index 0."}
```

```quiz
{"id": "ps-rev-window-formula", "q": "Which expression gives the sum of `nums[left]` through `nums[right]`, both included, when `prefix[i]` is the sum of the first `i` values?", "options": ["`prefix[right] - prefix[left]`", "`prefix[right + 1] - prefix[left + 1]`", "`prefix[right + 1] - prefix[left]`", "`prefix[right] - prefix[left - 1]`"], "answer": 2, "explain": "The entry `prefix[right + 1]` includes `nums[right]`, and `prefix[left]` stops just before `nums[left]`. The last option reads index -1 when `left` is 0."}
```

```quiz
{"id": "ps-rev-product-zero", "q": "An `int` array holds `[1, 0, 3]`. A program computes the product of all values and then divides by `nums[1]` to get the product of the others. What happens?", "options": ["It returns 0", "It returns 3", "It returns 4", "It throws an `ArithmeticException`"], "answer": 3, "explain": "Integer division by zero throws in Java. The two-pass method with a left product and a right product never divides, so the zero causes no error."}
```

```quiz
{"id": "ps-rev-missing-seed", "q": "A loop counts windows with sum `k` using a frequency map of earlier totals. The map starts empty and has no entry for the total 0. Which windows does the loop miss?", "options": ["Windows of length 1 in the middle", "Windows that start at index 0", "Windows that contain a negative value", "Windows that end at the last index"], "answer": 1, "explain": "A window that starts at index 0 pairs its end with boundary 0, whose total is 0. Without the entry for that boundary, the lookup finds nothing for these windows."}
```

```quiz
{"id": "ps-rev-earliest-balance", "q": "A balance of 2 first appears at index 1 and again at indexes 4 and 7. What is the length of the longest balanced span that ends at index 7 with that balance?", "options": ["3", "7", "6", "2"], "answer": 2, "explain": "The span starts right after the earliest index 1 and ends at index 7, so its length is 7 - 1 = 6. The later index 4 would give 3, which is shorter."}
```

```quiz
{"id": "ps-rev-floor-mod", "q": "What does `Math.floorMod(-7, 5)` return?", "options": ["-2", "2", "3", "-3"], "answer": 2, "explain": "The number -7 equals -2 * 5 + 3, so the remainder from 0 to 4 is 3. The operator `-7 % 5` gives -2 in Java, and that is why a map keyed by `%` splits one class in two."}
```

```quiz
{"id": "ps-rev-xor-window", "q": "A prefix XOR array for `[5, 1, 7, 2, 6]` is `[0, 5, 4, 3, 1, 7]`. What is the XOR of the values at indexes 2 through 4?", "options": ["4", "3", "11", "7"], "answer": 1, "explain": "The query reads `px[5] ^ px[2]`, which is `7 ^ 4 = 3`. The values 5 and 1 appear in both entries and cancel."}
```

```quiz
{"id": "ps-rev-extra-slot", "q": "A range update adds to indexes `left` through `right` of an array of length `n`, and it may end at index `n - 1`. How long must the difference array be so that the cancelling write never leaves the array?", "options": ["`n - 1`", "`n`", "`2 * n`", "`n + 1`"], "answer": 3, "explain": "The cancelling write goes to index `right + 1`, which is `n` when the update reaches the last index. The array needs the slot `n`, so its length is `n + 1`."}
```

```quiz
{"id": "ps-rev-rectangle-formula", "q": "A prefix matrix `P` has `P[r][c]` as the sum of rows `0..r-1` and columns `0..c-1`. Which expression sums the rectangle from `(r1, c1)` to `(r2, c2)`?", "options": ["`P[r2][c2] - P[r1][c2] - P[r2][c1] + P[r1][c1]`", "`P[r2 + 1][c2 + 1] - P[r1][c2 + 1] - P[r2 + 1][c1]`", "`P[r2 + 1][c2 + 1] - P[r1][c2 + 1] - P[r2 + 1][c1] + P[r1][c1]`", "`P[r2 + 1][c2 + 1] - P[r1][c1]`"], "answer": 2, "explain": "The two subtractions remove the rows above and the columns to the left. Both removals take away the corner region, so the formula adds `P[r1][c1]` back once."}
```

```quiz
{"id": "ps-rev-corner-writes", "q": "Which four writes add `v` to the rectangle from `(r1, c1)` to `(r2, c2)` in a difference matrix `D`?", "options": ["`+v` at `(r1, c1)`, `-v` at `(r1, c2 + 1)`, `-v` at `(r2 + 1, c1)`, `+v` at `(r2 + 1, c2 + 1)`", "`+v` at `(r1, c1)` and `-v` at `(r2 + 1, c2 + 1)`", "`+v` at all four corners of the rectangle", "`+v` at `(r1, c1)`, `-v` at `(r1, c2 + 1)`, `-v` at `(r2 + 1, c1)`, `-v` at `(r2 + 1, c2 + 1)`"], "answer": 0, "explain": "The two cancelling writes remove the value to the right and below the rectangle. The cells below and to the right lost the value twice, so the last write restores it with `+v`."}
```

```quiz
{"id": "ps-rev-map-value", "q": "A solution must report the length of the longest window whose two boundaries share a state. What must the map store for each state?", "options": ["The number of earlier boundaries with that state", "The first index at which the state occurred", "The last index at which the state occurred", "The sum of the indexes with that state"], "answer": 1, "explain": "The earliest boundary with the state gives the longest window for the current end. A count answers how many windows exist, and it cannot give a length."}
```
