<!-- section: review -->
## Review

A payout gives three tokens where two would do. A backup tool copies a file twice. A cashier screen shows nine breakdowns where four exist. Each failure matches a question below. Return to this page after the lessons and again after a few days. Each question describes a situation and hides the lesson name.

### Recognition Questions

```quiz
{"id": "cap-rev-unbounded-coin-change", "q": "A payout table stores the fewest tokens for each amount. When it fills amount 9 with a token of 3, which entry does it read, and why is that entry already correct?", "options": ["The entry for amount 6, which was finished earlier because amounts are visited in increasing order", "The entry for amount 12, which is finished first", "The entry for amount 3, which is the only one that exists", "No entry, because a token needs no earlier answer"], "answer": 0, "explain": "Every amount below 9 is final when the loop reaches 9. The entry for amount 6 may already contain the same token, which is why a token can repeat."}
```

```quiz
{"id": "cap-rev-unbounded-knapsack", "q": "In a table of best values by capacity, an item of weight 4 and value 5 is processed with the capacities in increasing order. Why can a capacity of 8 hold two copies of the item?", "options": ["The table adds the value twice by mistake", "Capacity 8 reads capacity 4 after the item already rewrote it, so that entry may hold one copy", "The item is copied into the table twice", "Capacity 8 is larger than the item"], "answer": 1, "explain": "The take case reads the current row. The entry for capacity 4 already holds one copy, so adding the value once more produces two copies."}
```

```quiz
{"id": "cap-rev-zero-one-knapsack", "q": "A one-array table for items that may be used once is updated with the capacities in increasing order. A single item of weight 3 and value 4 is tested with capacity 6. What does the table report?", "options": ["4, because the item fits once", "8, because the second capacity reads the entry the same item already rewrote", "0, because nothing fits", "6, because the capacity is full"], "answer": 1, "explain": "At capacity 6 the update reads capacity 3, which already holds the item. The table therefore counts the item twice and reports 8."}
```

```quiz
{"id": "cap-rev-partition-state", "q": "A subset-sum table has flags for sums up to half of the total. Which sum must be flagged for an equal split to exist, and what must the total be?", "options": ["The full total, and the total can be anything", "Half of the total, and the total must be even", "Zero, and the total must be odd", "Half of the total, and the total must be odd"], "answer": 1, "explain": "Two equal groups each sum to half of the total. An odd total has no whole half, so the answer is false before any table is built."}
```

```quiz
{"id": "cap-rev-target-sum", "q": "Numbers sum to 10 and each receives a plus or minus sign so that the signed sum is 4. What must the numbers with plus signs add up to?", "options": ["4", "6", "7", "3"], "answer": 2, "explain": "If the plus group sums to P, the minus group sums to 10 - P, and P - (10 - P) = 4 gives P = 7. The count of assignments equals the count of subsets with sum 7."}
```

```quiz
{"id": "cap-rev-combination-counts", "q": "A change counter lists the ways to pay 5 units with coins of 1, 2 and 5 and shows 9 breakdowns, where 4 exist. What kind of loop did it likely use?", "options": ["Coins on the outside and amounts inside", "A descending loop over the amounts", "Amounts on the outside with each coin tried as the last coin", "A loop that skips the seed"], "answer": 2, "explain": "Putting the amounts on the outside lets every coin come last, so each order of the same coins is counted. Putting the coins on the outside counts each combination once."}
```

```quiz
{"id": "cap-rev-permutation-counts", "q": "The number of ordered sequences of 1s and 2s that add up to 5 is built from smaller totals. Which two entries does the entry for total 5 add together?", "options": ["Totals 4 and 3", "Totals 5 and 0", "Totals 1 and 2", "Totals 4 and 1"], "answer": 0, "explain": "A sequence ends with a 1 or a 2. Removing the last element leaves a sequence for total 4 or total 3, so the entry adds those two counts."}
```

```quiz
{"id": "cap-rev-dp-and-capacity", "q": "A statement says that each voucher can be redeemed only once and that the order of redemption does not matter. Which loop structure fits?", "options": ["Totals on the outside and vouchers tried as the last element", "Items on the outside with the totals visited upward", "Items on the outside with the totals visited downward", "No table over totals can answer it"], "answer": 2, "explain": "Single use sets the direction downward, and order that does not matter puts the items on the outside. Totals on the outside would count sequences."}
```
