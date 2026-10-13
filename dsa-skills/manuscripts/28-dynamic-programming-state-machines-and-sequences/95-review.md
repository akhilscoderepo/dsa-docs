<!-- section: review -->
## Review

A report sells before it buys, a diff lists extra changes and a checker misreads a word. The questions below cover all six lessons and the closing lesson. Return to this page after the lessons and again after a few days. Each question describes a situation and hides the lesson name.

### Recognition Questions

```quiz
{"id": "seq-rev-stock-states", "q": "A report tracks the best cash on each day while holding a share and while holding none. Which pair of values moves to the next day when the share is sold?", "options": ["The no-share value plus the price goes to the holding value", "Both values add 3", "Holding value plus the price goes to the no-share value, if that beats the old no-share value", "Both values reset to zero"], "answer": 2, "explain": "Selling moves value from the holding label to the no-share label. The new no-share value is the larger of its old value and the holding value plus the price."}
```

```quiz
{"id": "seq-rev-transaction-variants", "q": "A trade needs one idle day after each sale. A table keeps only holding and no-share values. What does it allow that the rule forbids?", "options": ["Buying on the day right after a sale", "Selling twice in a row", "Holding two shares", "Ending with no share"], "answer": 0, "explain": "Two labels cannot tell a fresh sale from an older one. A third label for the day after a sale restores the rule."}
```

```quiz
{"id": "seq-rev-increasing-subsequences", "q": "In the tails array for a strictly increasing subsequence, an element equal to an existing tail arrives. What should the search do?", "options": ["Append it to the array", "Replace the last tail", "Ignore the array and restart", "Replace the first tail that is greater than or equal to it"], "answer": 3, "explain": "A lower bound search finds the first tail at least as large as the element. Replacing it keeps the length the same, because equal values must not extend a strict run."}
```

```quiz
{"id": "seq-rev-common-subsequences", "q": "Two strings are compared with a prefix table. When the last characters differ, which entries does the table read?", "options": ["The entry that drops both characters", "The entry that drops the last character of the first prefix and the one that drops the last of the second", "Only the entry above", "No entries, the cell becomes zero"], "answer": 1, "explain": "A mismatch means at most one of the two characters joins a match. The cell takes the larger of the two entries that drop one character."}
```

```quiz
{"id": "seq-rev-edit-distance", "q": "The table for turning an empty prefix into a prefix of length 5 holds what value in the first row?", "options": ["0, because the empty string matches", "1, because only one rule applies", "5, one insertion for each character", "The length of the shorter string plus one"], "answer": 2, "explain": "Each character of the target needs one insertion, so the entry for empty against length j is j."}
```

```quiz
{"id": "seq-rev-palindromic-sequences", "q": "A range table is indexed by left and right. In what order must the cells be filled so the inner range is ready?", "options": ["By increasing left only", "By increasing range length", "By decreasing right only, ignoring length", "In any order"], "answer": 1, "explain": "The cell for left and right reads the cell for left plus one and right minus one. That cell has a shorter length, so filling by length finishes it first."}
```

```quiz
{"id": "seq-rev-dp-state-machines", "q": "A table must allow at most two trades. Which pair is a complete state?", "options": ["The mode (holding or not) and the number of trades completed so far", "The day and the price", "Only the best profit", "The mode alone"], "answer": 0, "explain": "The mode decides which moves are legal and the count decides how many trades remain. Together they name every situation."}
```
