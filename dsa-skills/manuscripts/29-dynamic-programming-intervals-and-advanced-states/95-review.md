<!-- section: review -->
## Review

A greedy merge order overpays, a worker assignment misses the cheapest plan and a counter loops over every number up to a large bound. The questions below cover all seven lessons and the closing lesson. Return to this page after the lessons and again after a few days. Each question describes a situation and hides the lesson name.

### Recognition Questions

```quiz
{"id": "dp29-rev-interval-dp", "q": "A table entry dp[l][r] stores the best value for the range from l to r. Which entries may it read when it tries a split point k?", "options": ["dp[l][k] and dp[k+1][r], both shorter ranges", "Only dp[l+1][r]", "Any entry with a larger right end", "dp[r][l], the mirrored range"], "answer": 0, "explain": "Both halves are shorter than the whole range. Filling by increasing length finishes them first."}
```

```quiz
{"id": "dp29-rev-palindrome-partitions", "q": "A palindrome table says whether s[i..j] is a palindrome. Which condition must hold before the table marks it true when the ends match?", "options": ["The range is longer than 3", "The first letter appears twice", "The inner range s[i+1..j-1] is already marked true", "The whole prefix is a palindrome"], "answer": 2, "explain": "Equal ends make a palindrome only when the inside is one. A range of length one has no second end to match, and a range of length two has an empty inside."}
```

```quiz
{"id": "dp29-rev-tree-dp", "q": "A parent that takes its own value may not take the value of a child. What must each subtree return so the parent can choose?", "options": ["Only the best total", "Two values: the best total with the root taken and the best with it skipped", "The number of nodes", "The depth of the subtree"], "answer": 1, "explain": "The parent needs both modes, because taking itself forces children into skip mode while skipping lets each child choose."}
```

```quiz
{"id": "dp29-rev-bitmask-assignment", "q": "With n items and a used-set stored in an int mask, how many masks does the table need, and what is the full mask?", "options": ["n masks, and the full mask is n", "2^n masks, and the full mask is (1 << n) - 1", "n! masks, and the full mask is 0", "2^n masks, and the full mask is 1 << n"], "answer": 1, "explain": "Each item is one bit, so there are 2^n masks. All n bits set gives (1 << n) - 1."}
```

```quiz
{"id": "dp29-rev-submask-aggregation", "q": "What does sub = (sub - 1) & mask produce when sub is a nonempty submask of mask?", "options": ["Always sub - 1", "The complement of sub in mask", "A random submask", "The next smaller submask of mask in numeric order"], "answer": 3, "explain": "Subtracting one flips the lowest set bit and the bits below it. The AND with mask clears any bit that mask does not have."}
```

```quiz
{"id": "dp29-rev-digit-dp", "q": "Counting numbers up to a bound N digit by digit, what does the tight flag record?", "options": ["Whether the number is even", "Whether the number has started", "Whether the digits chosen so far equal the leading digits of N, so the next digit is capped", "Whether the digit sum is large"], "answer": 2, "explain": "While the prefix equals N's prefix, the next digit may not pass N's digit at that place. Once it is smaller, any digit is allowed."}
```

```quiz
{"id": "dp29-rev-optimization-proofs", "q": "A table row reads only the previous row. When can it be rolled into one array updated in place?", "options": ["Always", "When the update order guarantees each read sees the old value it needs", "Only when the table is square", "Never"], "answer": 1, "explain": "In-place updates overwrite entries. If a read needs an entry that was already overwritten, the answer changes, so the loop direction matters."}
```

```quiz
{"id": "dp29-rev-dp-advanced-state", "q": "A string problem asks about a contiguous range whose two ends are fixed, and a second problem asks about a set of used items. Which indexes fit?", "options": ["A mask for both", "A range of two ends for the first and a mask for the second", "A prefix length for both", "The value of the answer"], "answer": 1, "explain": "Subproblems that are contiguous pieces need two ends. Subproblems that are subsets of items need a mask."}
```
