<!-- section: review -->
## Review

Come back to this page after the lessons and again a few days later. Each question describes a situation and leaves out the lesson name. Choose an answer before you open the explanation.

### Recognition Questions

```quiz
{"id": "ms-rev-first-larger", "q": "The values 2, 7, 4, 9 arrive in order, and the stack removes every top value smaller than the arriving value. Which indices does the value 9 resolve?", "options": ["Indices 0, 1 and 2", "Indices 1 and 2", "Index 2 only", "Index 3 itself"], "answer": 1, "explain": "The value 7 already removed index 0 when it arrived. At that point the stack holds indices 1 and 2. The value 9 removes both of them, and index 3 stays because nothing larger follows."}
```

```quiz
{"id": "ms-rev-wrap-around", "q": "A circular array holds 3, 1, 2. Which value is the next greater value of the 2 at the last position?", "options": ["-1", "1", "3", "2"], "answer": 2, "explain": "The scan continues past the end and wraps to index 0. The value 3 there is larger than 2, so it is the answer. The value 2 has no larger value in a straight scan, which is why the wrap matters."}
```

```quiz
{"id": "ms-rev-span-last", "q": "Prices on seven days are 100, 80, 60, 70, 60, 75, 85. The span of a day counts that day and the days before it with a price at most as large. What is the span of the last day?", "options": ["7", "5", "4", "6"], "answer": 3, "explain": "The last price is 85. The days with prices 75, 60, 70, 60 and 80 are all at most 85, and the first price 100 is larger. The span counts those five days and the last day itself, which gives 6."}
```

```quiz
{"id": "ms-rev-both-sides", "q": "The values 4, 2, 5, 3 sit at indices 0 to 3. What are the previous smaller index and the next smaller index of the 5 at index 2?", "options": ["0 and 3", "-1 and 3", "1 and 3", "1 and 4"], "answer": 2, "explain": "The value to the left that is smaller than 5 and nearest is 2 at index 1. The nearest smaller value to the right is 3 at index 3. Both indices exist, so neither marker is needed."}
```

```quiz
{"id": "ms-rev-shared-ranges", "q": "The array holds 2 and 2, and the rightmost minimum owns each range that holds both values. How many ranges does the index 1 own?", "options": ["1", "2", "3", "0"], "answer": 1, "explain": "The array has three ranges: the first value, the second value and both values. The range that holds both goes to the rightmost minimum. Index 1 owns that range and its own single value, which makes 2."}
```

```quiz
{"id": "ms-rev-owned-count", "q": "An index 3 has its left boundary at index 1 and its right boundary at index 6. How many ranges does it own?", "options": ["12", "6", "5", "8"], "answer": 1, "explain": "A range picks a start from indices 2 and 3, which is `3 - 1` choices. It picks an end from indices 3, 4 and 5, which is `6 - 3` choices. The two choices are independent, so the count is 2 times 3."}
```

```quiz
{"id": "ms-rev-increasing-bars", "q": "The bar heights are 2, 4 and 6, and they never decrease. When does the bar of height 2 report its rectangle, and what is the area?", "options": ["When 4 arrives, with area 2", "At the closing step, with area 6", "At the closing step, with area 2", "When 6 arrives, with area 6"], "answer": 1, "explain": "No arriving bar is shorter, so nothing leaves the stack before the closing step. The closing bar removes the bars one by one. The bar of height 2 has no left boundary and the right boundary is the end, so its width is 3 and its area is 6."}
```

```quiz
{"id": "ms-rev-equal-boundaries", "q": "Boundaries for the sum of minimums of the array 4, 4 are found in two passes, and both passes stop at equal values. What total do they give?", "options": ["16", "12", "4", "8"], "answer": 3, "explain": "Each index sees the other as a boundary, so each owns only its single value. The range that holds both values has no owner. The total is 4 plus 4, which is 8, and the correct total is 12."}
```
