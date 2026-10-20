<!-- section: review -->
## Review

A cache hands back an evicted entry, a random pick returns a removed value and an iterator repeats an element. The questions below cover the six lessons and the three closing lessons. Read this page when the lessons are done and read it again several days later. Each question describes a situation, so reach an answer before the explanation opens.

### Recognition Questions

```quiz
{"id": "rq33-rev-contract-fields", "q": "A class has an operation `remove(x)`. Which item is missing from a complete contract if it states only the return value and the time cost?", "options": ["The memory layout", "The mutation and the failure behavior", "The name of the field", "The import list"], "answer": 1, "explain": "A contract states output, mutation, failure behavior and cost. A caller needs to know what changes in the state and what happens when the call is illegal."}
```

```quiz
{"id": "rq33-rev-failed-mutation", "q": "A bounded list rejects an insert when it is full. At which point should the operation detect this?", "options": ["After it has updated the size field", "After it has linked the new node", "Before it changes any field", "In a later call"], "answer": 2, "explain": "Checking before any write means a rejected call leaves every field unchanged, so the invariant holds without a repair step."}
```

```quiz
{"id": "rq33-rev-map-list", "q": "A cache stores a map from key to node and a doubly linked list of nodes. Which fact must hold after every operation?", "options": ["The map and the list hold the same set of nodes", "The map is sorted by key", "The list is sorted by key", "The list is shorter than the map"], "answer": 0, "explain": "Both structures refer to the same nodes. If one holds a node the other lacks, a lookup or an eviction touches a node that does not exist."}
```

```quiz
{"id": "rq33-rev-swap-last", "q": "An array holds values 4, 7, 9 and a map stores the slot of each value. Value 4 is removed by swapping with the last slot. What must change in the map?", "options": ["Nothing", "Value 4 maps to slot 2", "Value 9 maps to slot 0 and value 4 has no entry", "Value 7 maps to slot 0"], "answer": 2, "explain": "The value 9 moves into slot 0, so its entry changes. The removed value 4 loses its entry. The array then holds 9, 7."}
```

```quiz
{"id": "rq33-rev-last-slot", "q": "A swap-removal repairs the map entry of the moved value and deletes the map entry of the removed value. The removed value sits in the last slot, so both are the same value. Which order keeps the map correct?", "options": ["Delete the entry last, after the repair", "Repair the entry last, after the delete", "Either order gives the same map", "Skip both steps"], "answer": 0, "explain": "A repair that runs after the delete writes the entry back and revives the removed value. Deleting last removes the entry for good."}
```

```quiz
{"id": "rq33-rev-has-next", "q": "A caller calls `hasNext()` three times in a row on an iterator over 5 values. How many values does the iterator consume?", "options": ["Three", "One", "Five", "None"], "answer": 3, "explain": "hasNext reports availability and consumes nothing. Only next advances the iterator, and it advances exactly once."}
```

```quiz
{"id": "rq33-rev-peek", "q": "A peeking iterator caches one element from its source. Why does a second `peek()` not advance the source?", "options": ["The cache already holds the element, so the call returns it", "The source has no more elements", "peek always reads the last element", "The source is sorted"], "answer": 0, "explain": "The first peek moves one element from the source into the cache. Every later peek returns the cached element and leaves the source alone. Only next hands the element out and clears the cache."}
```

```quiz
{"id": "rq33-rev-lru-evict", "q": "An LRU cache of capacity 2 holds keys A then B, with B most recent. A `get(A)` runs, and then `put(C)`. Which key leaves the cache?", "options": ["A", "Both A and B", "Nothing", "B"], "answer": 3, "explain": "The get moves A to the front, so B is the least recent key. The put of C evicts B."}
```

```quiz
{"id": "rq33-rev-lfu-tie", "q": "An LFU cache must evict, and two keys share the lowest use count. Which key goes?", "options": ["The one with the larger key", "The one used least recently within that count", "Both", "The one added last"], "answer": 1, "explain": "Each count owns its own recency list. The tie breaks by recency inside the bucket of the minimum count."}
```
