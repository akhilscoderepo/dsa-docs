<!-- section: unlocked-combinations -->
## Unlocked Combinations

A product team needs a session cache that drops the oldest idle session, a raffle that draws a uniform winner and lets entrants withdraw, and a reader that pages through a nested menu one item at a time. Each need pairs two structures from this chapter. Three pairings are taught below, and one waits for a later chapter.

### Pairings Taught In This Chapter

The lesson Locate By Key And Order By Recency joins the hash map with the doubly linked list. The map finds a node by key, and the list owns the recency order and removes a node in constant time. Its four exercises relink a node, resize a cache, check capacity one and log the evicted keys of a frequency cache.

The lesson Find A Slot And Pick From Array joins the hash map with the dynamic array. The map stores the slot of each value, and the array gives uniform selection and last-slot repair. Its four exercises remove by swap, pick a value different from a given one, remove from the last slot and hold duplicate values.

The lesson Traversal State Across Public Calls joins iterators with the tree walk, wrappers and nested lists. The next-element invariant has to hold across every call. Its four exercises iterate a tree stored in a node pool, wrap a source that cannot restart, flatten nested lists under a depth limit and rotate among several sources.

### Pairings That Wait For A Later Chapter

Thread-safe designs change which operations are atomic and which lock owns each field. A later chapter on specialized services takes them, and this chapter assigns no problems to them.
