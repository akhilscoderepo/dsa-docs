<!-- section: review -->
## Review

A count finishes for 12 and never finishes for 100. A memory-saving rewrite returns a wrong total. A grid count ignores the walls. A question below fits each failure. Take a second look at this page after the lessons and a third look after a few days. Each question depicts a situation and omits the lesson name.

### Recognition Questions

```quiz
{"id": "dp-rev-state-definition", "q": "A recursive counter passes the list of chunks chosen so far, and two calls with different lists but the same number of bytes left return the same count. What does this show about the list?", "options": ["It belongs in the state, because it differs between calls", "It does not belong in the state, because it does not change the answer", "The counter must be iterative", "The answer is wrong"], "answer": 1, "explain": "The state holds only the values that decide the answer. Calls with equal remaining bytes return equal answers, so the list can be dropped and the calls can share one stored result."}
```

```quiz
{"id": "dp-rev-memo-and-table", "q": "A cache is a new long array, and the code treats the value 0 as 'not computed'. Why does this fail for a sequence whose first answer is 0?", "options": ["Arrays cannot hold zero", "The recursion becomes infinite", "A real answer of 0 looks empty, so the method recomputes it on every call", "The loop runs backward"], "answer": 2, "explain": "A marker for an empty slot must differ from every real answer. With 0 as the marker, a stored answer of 0 is never recognized as stored."}
```

```quiz
{"id": "dp-rev-linear-recurrence", "q": "The count for size i adds the counts for i - 1 and i - 2. Before the loop computes entry i, what must already be true?", "options": ["Both entries i - 1 and i - 2 are final", "Entry i holds a guess", "The array is sorted", "Entry n is final"], "answer": 0, "explain": "The window is the set of earlier entries that one entry reads. The loop order guarantees that every entry in the window is final before it is read."}
```

```quiz
{"id": "dp-rev-take-or-skip", "q": "In a row of values where two neighbors cannot both be chosen, a best selection uses the last value. What does it do with the value just before the last?", "options": ["It uses it too", "It leaves it out, and the rest comes from the prefix that ends two positions earlier", "It doubles the last value", "It restarts from the beginning"], "answer": 1, "explain": "Taking the last value forbids its neighbor. The remaining choices lie in the prefix two shorter, which has no index next to the taken one."}
```

```quiz
{"id": "dp-rev-rolling-state", "q": "A loop keeps two variables for the last two entries. After computing the new value, which assignment must run first?", "options": ["The newer variable takes the new value", "Both assignments at once in any order", "The older variable takes the newer variable's value", "The table is rebuilt"], "answer": 2, "explain": "The oldest variable is written first, because it reads the newer variable before that variable is overwritten. The other order leaves both variables with the same number."}
```

```quiz
{"id": "dp-rev-objective-types", "q": "A jump table counts routes with the base value 0 for the start cell instead of 1. What do the later entries become?", "options": ["Twice as large", "Correct", "All 0", "Negative"], "answer": 2, "explain": "The empty sequence of jumps is one way to stand on the start cell. With a base value of 0, every sum built from it stays 0."}
```

```quiz
{"id": "dp-rev-grid-dp", "q": "A robot moves only right or down, and the loops visit the cells row by row, left to right. Why is every predecessor final when a cell is computed?", "options": ["Every predecessor lies in an earlier row or earlier in the same row", "The grid is square", "Cells are computed twice", "Predecessors are never read"], "answer": 0, "explain": "The cell above and the cell to the left both come earlier in reading order. The fill order is safe because the move set only points that way."}
```

```quiz
{"id": "dp-rev-transition-discipline", "q": "A loop writes the new row into the array that it also reads, and the results look like they include the current row. What went wrong?", "options": ["The row is too short", "A read touched a value of the current layer instead of the previous layer", "The grid is empty", "The loop ran too few times"], "answer": 1, "explain": "A transition must read only the previous layer. Writing into the array being read mixes two layers, so a later cell reads a value that belongs to the current row."}
```

```quiz
{"id": "dp-rev-recursion-and-memoization", "q": "A memoized board recursion stores results by the row alone, and different columns in the same row get the same stored result. What is missing?", "options": ["A larger stack", "A faster loop", "A sorted board", "The column in the cache key"], "answer": 3, "explain": "The key must contain every argument that changes the answer. Leaving out the column makes different questions share one slot, so the stored value is wrong for most of them."}
```
