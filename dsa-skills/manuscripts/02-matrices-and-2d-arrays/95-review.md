<!-- section: review -->
## Review

Come back to this page after the lessons and again a few days later. Each question describes a situation and hides the lesson name. Commit to an answer before you read the options.

### Recognition Questions

```quiz
{"id":"mx-rev-row-length","q":"A method sums every cell of an `int[][]` named `t` whose rows may have different lengths. Which bound is safe for the inner loop over row `r`?","options":["t[0].length","t[r].length","t.length","t.length * t[0].length"],"answer":1,"explain":"Each row is its own array, so only `t[r].length` describes row `r`. The first row's length is wrong for any row of a different length."}
```

```quiz
{"id":"mx-rev-diagonal","q":"Which rule on the indexes `r` and `c` selects the cells of one line that runs down and to the right?","options":["r + c is constant","r - c is constant","r * c is constant","r is constant"],"answer":1,"explain":"Moving one step down and one step right raises both indexes by one, so their difference stays the same. The sum stays constant along a line that runs down and to the left."}
```

```quiz
{"id":"mx-rev-turn","q":"A cursor walks a matrix with offsets listed in the order right, down, left, up. Which update turns it clockwise?","options":["d = (d + 1) % 4","d = (d + 3) % 4","d = 4 - d","d = d * 2"],"answer":0,"explain":"The offsets are listed in clockwise order, so the next direction is the next entry, and the remainder wraps from the last entry back to the first."}
```

```quiz
{"id":"mx-rev-corner","q":"How many neighbors does a corner cell of a 5 by 5 board have when all eight surrounding cells count?","options":["8","5","3","4"],"answer":2,"explain":"A corner touches two cells along the sides and one diagonal cell inside the board. The other five positions lie outside, so the range test must reject them before any read."}
```

```quiz
{"id":"mx-rev-rotate","q":"Which two in-place steps rotate a square matrix a quarter turn clockwise?","options":["Reverse each row, then transpose","Transpose, then reverse each row","Reverse each column, then reverse each row","Transpose twice"],"answer":1,"explain":"The transpose sends (r, c) to (c, r), and reversing each row sends that cell to (c, n - 1 - r), which is the clockwise quarter turn. Transposing twice restores the input."}
```

```quiz
{"id":"mx-rev-markers","q":"A method clears the row and column of every zero. Why does it record the lines first and clear them afterward?","options":["Clearing is slower than recording.","Zeros written during the scan would look like zeros of the input.","Recording uses less time than reading.","Java forbids writing during a scan."],"answer":1,"explain":"The scan must see the input exactly as given. A zero written by the method would start a second round of clearing and wipe cells that should survive."}
```

```quiz
{"id":"mx-rev-guards","q":"In a spiral walk, the bottom pass runs only when `top <= bottom`. What would happen on a matrix with one row if the check were missing?","options":["The walk would skip the whole row.","The walk would emit the row a second time.","The walk would throw an exception at once.","The walk would stop after the first cell."],"answer":1,"explain":"The top pass already consumed the only row. Without the check, the bottom pass would walk that same row backward and emit its cells again."}
```
