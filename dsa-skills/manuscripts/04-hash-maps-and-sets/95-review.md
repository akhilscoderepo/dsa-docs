<!-- section: review -->
## Review

Return to this page after the lessons and again a few days later. Each question describes a situation and hides the lesson name. Commit to an answer before you open the explanation.

### Recognition Questions

```quiz
{"id": "hm-rev-duplicate-batch", "q": "A loop must reject a batch of order numbers as soon as any number repeats. Which remembered state is enough?", "options": ["The set of numbers read so far", "A map from each number to its count", "A sorted copy of all numbers", "A list of the position of each number"], "answer": 0, "explain": "The question asks only whether a number has appeared, so a set suffices. A count or a position stores more than the question needs, and a sorted copy costs O(n log n)."}
```

```quiz
{"id": "hm-rev-absent-key", "q": "The program runs `int c = count.get(key)` for a key that never occurred in the map. What happens?", "options": ["The call returns 0", "The call returns -1", "The call throws a `NullPointerException` when it unboxes the result", "The call stores the key with count 0"], "answer": 2, "explain": "The method `get` returns `null` for an absent key, and unboxing `null` into an `int` throws. The call `getOrDefault(key, 0)` applies the convention that an absent key counts 0."}
```

```quiz
{"id": "hm-rev-store-first", "q": "Two Sum runs on `[5, 5]` with target 10. The loop stores `nums[i]` in the map before it looks up the complement. What does it return?", "options": ["`[0, 1]`", "`[0, 0]`", "`[-1, -1]`", "It throws an exception"], "answer": 1, "explain": "At index 0 the loop stores 5 at position 0 and then finds the complement 5 at position 0, the same cell. Looking up before storing finds the second 5 at index 1."}
```

```quiz
{"id": "hm-rev-negative-remainder", "q": "A scheduler uses `job % m` as the worker number with `m = 3`. What does it get for the job -7?", "options": ["2", "1", "-2", "-1"], "answer": 3, "explain": "The operator `%` keeps the sign of the left operand, so -7 % 3 is -1 and the index falls outside the range 0 to 2. `Math.floorMod(-7, 3)` returns 2."}
```

```quiz
{"id": "hm-rev-run-start", "q": "In the method for the longest run of consecutive numbers, which values start a walk upward?", "options": ["Every value in the set", "Values whose successor is absent", "Values whose predecessor is absent", "Only the smallest value"], "answer": 2, "explain": "A value without `x - 1` in the set is the first value of its run. A value with a predecessor lies inside a run that an earlier start already walks, so walking from it repeats work."}
```

```quiz
{"id": "hm-rev-array-key", "q": "A program counts equal pairs `{row, col}` with a `Map<int[], Integer>`, using each input array as the key. Why does every pair end with count 1?", "options": ["An array compares by identity, so equal contents still give different keys", "An `int[]` has no `hashCode` method", "A map refuses arrays and ignores the inserts", "The map boxes each pair into one shared `Integer`"], "answer": 0, "explain": "The method `equals` of an array compares object identity, so two arrays with the same numbers are two keys. A record or a `List` compares contents."}
```

```quiz
{"id": "hm-rev-sparse", "q": "A table must count 1000 user ids, and the ids lie between 1 and 2000000000. Which storage fits?", "options": ["An `int[]` indexed by `id - 1`", "A `HashMap` from id to count", "A `boolean[]` of the same length", "Any of the three, since the cost is the same"], "answer": 1, "explain": "The key range is two billion while only 1000 keys occur, so the keys are sparse. An array needs one slot for each possible key, and a map needs one entry for each key that occurs."}
```

```quiz
{"id": "hm-rev-forward-only", "q": "A check for a one-to-one renaming keeps only the forward map from source letter to target letter. Which pair does it wrongly accept?", "options": ["`\"ab\"` and `\"ba\"`", "`\"aa\"` and `\"bb\"`", "`\"ab\"` and `\"cc\"`", "`\"ab\"` and `\"ab\"`"], "answer": 2, "explain": "The forward map sends `a` to `c` and `b` to `c` without a conflict, so two source letters merge. The reverse map from target to source catches the merge."}
```

```quiz
{"id": "hm-rev-box-index", "q": "On a 9 by 9 board the box index of a cell is `(r / 3) * 3 + c / 3`. Which box does the cell in row 4 and column 7 belong to?", "options": ["Box 4", "Box 6", "Box 5", "Box 3"], "answer": 2, "explain": "Row 4 gives `4 / 3 = 1`, so `1 * 3 = 3`. Column 7 gives `7 / 3 = 2`. The sum is 5."}
```

### Questions To Ask Before Writing Code

Before you declare a map or a set, answer three questions in your own words. What does the key mean, and what does the value mean? Does the question need existence, a count, a position or the full list of members? Is the number of possible keys small enough for an array, or does the problem leave the keys open? The invariant that you write for the loop then names what the structure holds after each element, and most exercises in this chapter change one of the three answers.
