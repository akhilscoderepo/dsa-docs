<!-- section: review -->
## Review

Come back to this section after the lessons and again after a few days. The scenarios avoid naming the method, so decide what the stack holds, which comparison removes an entry and when the answer is written before you read the options. They test prediction and recognition, which guided exercises cannot.

### Recognition Questions

```quiz
{"id":"ms-rev-resolve-on-pop","q":"In the next-greater scan, when is the answer of a waiting index written?","options":["When the index is pushed.","When a strictly greater value pops it.","After the loop ends, for every index.","When the stack becomes empty."],"answer":1,"explain":"An index is answered by the first strictly greater value, and that value arrives at the moment the index is popped."}
```

```quiz
{"id":"ms-rev-stop-rule","q":"Why may the removal loop stop at the first top that is not dominated?","options":["The remaining entries are already answered.","Entries beneath it are at least as large, so the arrival cannot dominate them either.","The array is sorted.","Stopping makes the scan faster but may skip answers."],"answer":1,"explain":"The stack keeps one order from bottom to top, so a value that fails against the top fails against everything under it."}
```

```quiz
{"id":"ms-rev-ring-lap","q":"Why does a circular next-greater scan push positions only during the first lap?","options":["The second lap is shorter.","Each position must be on the stack once; the second lap only resolves positions left waiting.","Pushing twice would make the scan quadratic.","The second lap has no comparisons."],"answer":1,"explain":"A second push would put a position on the stack twice and could answer it twice, while the second lap exists to resolve positions whose greater value stands before them."}
```

```quiz
{"id":"ms-rev-span-equal","q":"For a stock span defined as days with a price no higher than today's, what happens to an equal earlier price?","options":["It stays as a separate candidate.","It is removed and its span is absorbed into today's span.","It ends the run.","It is counted twice."],"answer":1,"explain":"An equal price is inside the run, so the removal test includes equality and the pair's span joins today's."}
```

```quiz
{"id":"ms-rev-sentinels","q":"For widths of the form right minus left minus one, what should a missing left wall and a missing right wall be?","options":["Both 0.","Left -1 and right n.","Left 0 and right n - 1.","Both -1."],"answer":1,"explain":"The sentinels -1 and n are the positions just outside the array, so the formula counts the elements strictly between the walls without special cases."}
```

```quiz
{"id":"ms-rev-tie-rule","q":"Two equal minimum values lie inside one subarray. Which pair of wall rules gives that subarray exactly one owner?","options":["Both walls stop at strictly smaller values.","Both walls stop at smaller or equal values.","One wall stops at strictly smaller values and the other at smaller or equal values.","Neither wall needs a rule."],"answer":2,"explain":"With both strict, both indices claim the subarray, and with both non-strict, neither does. The asymmetric rule gives it to exactly one."}
```

```quiz
{"id":"ms-rev-count-product","q":"An index owns subarrays starting after left and ending before right. How many does it own?","options":["right minus left minus one.","The product of i minus left and right minus i.","Right minus left.","The sum of the two distances."],"answer":1,"explain":"Every start in left plus one up to i combines with every end from i to right minus one, so the counts multiply."}
```

```quiz
{"id":"ms-rev-modulus","q":"In a sum of subarray minimums taken modulo a prime, where must the multiplication be widened to long?","options":["Only after the modulus is applied.","Before multiplying the two distances and before multiplying by the value.","It never needs widening.","Only for the final sum."],"answer":1,"explain":"A product of two int distances can wrap before any modulus is applied, so widening comes first."}
```

```quiz
{"id":"ms-rev-closing-zero","q":"Why does the histogram scan add a closing zero at index n?","options":["To make the array longer.","So every bar still waiting at the end is removed and priced.","To avoid negative heights.","Because zero is the smallest bar."],"answer":1,"explain":"Bars that never meet a shorter bar to their right have right wall n, and the closing zero removes them so each is priced once."}
```

```quiz
{"id":"ms-rev-width-vs-count","q":"A histogram uses right minus left minus one, and a total over subarrays uses a product. Why not use the width as the count?","options":["The width is always larger.","Only the widest run of a bar matters for a rectangle, while every sub-stretch containing the index matters for a count.","The product is faster.","There is no difference."],"answer":1,"explain":"A rectangle uses the one widest run, so a width suffices. A total over subarrays counts every start and end choice, which is a product."}
```
