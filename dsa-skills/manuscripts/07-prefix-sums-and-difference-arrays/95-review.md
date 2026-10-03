<!-- section: review -->
## Review

Come back to these scenarios after the lessons and again after a few days. None of them names the technique, so decide what table, key or sweep the situation needs before reading the options. They check recognition and prediction, which the guided exercises cannot.

### Recognition Questions

```quiz
{"id":"ps-rev-sentinel","q":"A prefix array for n values is allocated with n slots and prefix[i] is defined as the sum through position i. What breaks first?","options":["A query that starts at the first position, because there is no slot for the empty prefix.","Queries that end at the last position.","The type of the sum.","Nothing breaks."],"answer":0,"explain":"Without a slot for the empty prefix, a stretch beginning at index zero needs a special case or reads outside the array. One extra leading slot removes the case."}
```

```quiz
{"id":"ps-rev-range","q":"With prefix[i] holding the sum of the first i values, what is the sum of positions left through right, both included?","options":["prefix[right] - prefix[left]","prefix[right] - prefix[left - 1]","prefix[right + 1] + prefix[left]","prefix[right + 1] - prefix[left]"],"answer":3,"explain":"The slot after the last included position counts every value up to right, and the slot at left counts every value before left, so their difference is the stretch."}
```

```quiz
{"id":"ps-rev-overflow","q":"Values up to two billion are summed over a million positions to build a table. Which type should the table use?","options":["int, because each value fits in int.","float, to save space.","long, because a single sum can exceed what int holds.","short, because only differences matter."],"answer":2,"explain":"A sum of many values that each fit in int can still wrap. The table must be wide enough for the largest total, and the subtraction of two long slots is exact."}
```

```quiz
{"id":"ps-rev-division","q":"A product-except-self routine divides the grand product by each element. Which input exposes the flaw?","options":["An array of positive values.","An array of length one.","An array with repeated values.","An array containing a zero, since the division is by zero or hides which position is the only non-zero answer."],"answer":3,"explain":"A zero makes the grand product zero and divides by zero at its own position. Left and right passes avoid division and handle every number of zeros."}
```

```quiz
{"id":"ps-rev-count-order","q":"In a count of stretches with sum k, the current balance is recorded in the table before the complement is looked up. What goes wrong when k is zero?","options":["Every position pairs with itself, so empty stretches are counted.","Nothing, because the balance is the same.","The loop never ends.","Only the first position is counted."],"answer":0,"explain":"With k equal to zero the complement equals the balance just recorded, so the position matches itself. Looking up first keeps the stretch non-empty."}
```

```quiz
{"id":"ps-rev-first-index","q":"A solution to the longest stretch with equal numbers of two kinds overwrites the stored index of a balance on every visit. What does it compute?","options":["The longest stretch, as intended.","The number of stretches.","Nothing, because it always throws.","The shortest stretch for each repeated balance, not the longest."],"answer":3,"explain":"Storing the latest index pairs each position with the closest earlier match. The earliest index gives the widest span, so it must be kept."}
```

```quiz
{"id":"ps-rev-floormod","q":"A running total is -2 and the modulus is 3. Which expression gives the class used as a table index?","options":["Math.floorMod(-2, 3), which is 1","-2 % 3, which is -2","Math.abs(-2) % 3, which is 2","-2 / 3, which is 0"],"answer":0,"explain":"Java's % keeps the sign of the dividend and would be a negative index. floorMod returns a value from zero to the modulus minus one, so equal classes share one key."}
```

```quiz
{"id":"ps-rev-boxing","q":"A map of type Map<Long, Integer> is seeded with put(0L, 1) and then read with get(0). What is returned?","options":["1, because zero is zero.","null, because an Integer key does not equal a Long key.","0, as the default.","An exception is thrown."],"answer":1,"explain":"get takes an Object, so the int is boxed as an Integer, and an Integer is never equal to a Long. The lookup must use a long value so the boxed types match."}
```

```quiz
{"id":"ps-rev-xor","q":"Which statement about range XOR is true?","options":["Subtracting two prefix XOR values gives the range XOR.","XOR needs a long table.","Range XOR cannot be answered with a table.","XOR of two prefix values cancels the early part because each value appears twice and a ^ a is zero."],"answer":3,"explain":"XOR is its own inverse, so combining the prefix before the start with the prefix through the end leaves only the stretch. Subtraction is the wrong cancellation."}
```

```quiz
{"id":"ps-rev-difference","q":"A difference array is built for n positions and a range update ends at the last position. What is the safest way to store the cancelling note?","options":["Skip the note and hope.","Allocate n + 1 slots so that index n exists and is never read when rebuilding.","Use index minus one.","Shrink the range."],"answer":1,"explain":"The note belongs one past the end of the range. An extra slot makes the write valid, and a guard that skips the write is equally correct."}
```

```quiz
{"id":"ps-rev-2d","q":"Which four-term formula gives the sum of rows r1 to r2 and columns c1 to c2 from a padded table P?","options":["P[r2+1][c2+1] - P[r1][c2+1] - P[r2+1][c1] + P[r1][c1]","P[r2][c2] - P[r1][c1]","P[r2+1][c2+1] - P[r1][c1]","P[r2+1][c2+1] + P[r1][c1] - P[r1][c2+1] + P[r2+1][c1]"],"answer":0,"explain":"Two strips are removed and their overlap, removed twice, is added back once. The signs are plus, minus, minus, plus."}
```

```quiz
{"id":"ps-rev-2d-diff","q":"A rectangle update writes three corner notes and omits the one at the bottom-right just beyond the rectangle. What does the sweep produce?","options":["The correct grid.","Only the first row is wrong.","Tiles below and to the right of the rectangle receive a stray amount instead of zero.","An exception."],"answer":2,"explain":"The fourth note repairs the overlap of the two cancelling notes. Without it, every tile past both ends still carries the amount."}
```
