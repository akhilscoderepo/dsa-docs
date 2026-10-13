<!-- section: review -->
## Review

A circular queue cannot tell full from empty, a browser history keeps pages that should be gone, and an ID pool hands out the same number twice. The questions below cover the six lessons and the two closing lessons. Try them after the lessons and again after a few days, and commit to an answer before opening the explanation.

### Recognition Questions

```quiz
{"id": "rq36-rev-rejected-call", "q": "A bounded counter rejects an increment that would pass its limit. Which fields may that rejected call change?", "options": ["Only the call counter.", "None of them.", "The limit, lowered by one.", "The value, reset to zero."], "answer": 1, "explain": "A rejected call leaves every field unchanged, so the next legal call sees the same state it would have seen without the rejected one."}
```

```quiz
{"id": "rq36-rev-bucket-owner", "q": "A hash set uses `key % 769` as the bucket index. Two keys share a bucket. What must remove(key) do?", "options": ["Clear the whole bucket.", "Delete only the node that holds that key.", "Move the other key to a new bucket.", "Do nothing, because the keys collide."], "answer": 1, "explain": "The bucket owns every key that hashes to it, so removal deletes only the matching entry and leaves the colliding keys in place."}
```

```quiz
{"id": "rq36-rev-full-empty", "q": "A ring buffer stores only `head` and `tail`. Both equal 3. What does that tell you?", "options": ["The buffer is empty.", "The buffer is full.", "The buffer holds one item.", "Nothing, because both states give equal indices."], "answer": 3, "explain": "A full buffer and an empty buffer can have equal indices after wraparound. An explicit `size` field separates the two states."}
```

```quiz
{"id": "rq36-rev-modular-tail", "q": "A ring buffer has capacity 5, `head = 3` and `size = 4`. Which slot holds the newest item?", "options": ["Slot 2", "Slot 0", "Slot 1", "Slot 7"], "answer": 2, "explain": "The newest item sits at `(head + size - 1) % capacity`, which is `(3 + 4 - 1) % 5 = 1`. Slot 1 holds it, and slot 2 is the next free slot."}
```

```quiz
{"id": "rq36-rev-split-middle", "q": "Two halves hold 3 and 3 elements and the rule removes the front middle. After one remove from the middle, what keeps the halves within one element?", "options": ["Nothing; the sizes still differ by at most one.", "A rebalance that moves one element between halves.", "Always clearing the back half.", "Rebuilding both halves from scratch."], "answer": 0, "explain": "Removing the front middle of 3 and 3 takes the last element of the left half, leaving 2 and 3. The right half exceeds the left by one, which the rule allows, so no element moves."}
```

```quiz
{"id": "rq36-rev-history-cut", "q": "A browser sits on page 2 of pages 0 to 4 and visits a new page. What happens to pages 3 and 4?", "options": ["They stay and the new page goes after them.", "They are hidden from the visible history, and the new page follows page 2.", "They move before page 2.", "They are kept until back is called."], "answer": 1, "explain": "A new visit invalidates the forward history, so the visible pages end at the cursor plus the new page, whether or not the old slots are physically cleared."}
```

```quiz
{"id": "rq36-rev-pool-states", "q": "An ID pool uses a heap of returned ids. A caller returns id 4 twice. What goes wrong without a membership check?", "options": ["Nothing; the heap ignores duplicates.", "Id 4 can be allocated twice to two owners.", "The frontier counter falls.", "The heap loses its order."], "answer": 1, "explain": "A heap orders entries but does not reject duplicates. A set of returned ids refuses the second return, so each id is free at most once."}
```

```quiz
{"id": "rq36-rev-stale-entry", "q": "A writable-stacks set holds stale index 3 after stack 3 filled up. What must the allocator do when it reads index 3?", "options": ["Write into stack 3 anyway.", "Remove the stale entry and read the next one.", "Report that the pool is full.", "Rebuild every stack."], "answer": 1, "explain": "The stated stale-entry policy discards an entry that no longer matches the stack state when the allocator reaches it, then continues."}
```
