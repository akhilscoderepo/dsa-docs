<!-- section: unlocked-combinations -->
## Unlocked Combinations

A network router keeps the last 10,000 packets and answers how many packets went to one destination. The ring buffer alone cannot answer that question, and the destination index alone cannot forget old packets. One class needs both, and each call must update both before it returns. The same shape appears when a resource pool needs an ordered structure and a membership check.

### Pairings Taught In This Chapter

| Combination | Teach now | Representative problem |
| --- | --- | --- |
| Containers + API State | Yes | LeetCode 3508 Implement Router |
| Multiple Collections + Ownership | Yes | LeetCode 1172 Dinner Plate Stacks |

The lesson Containers And API State joins modular storage with an index and a call log, so a rejected call changes nothing. The lesson Multiple Collections Ownership places each resource in one of three states and keeps every index in agreement about it.

### Pairings Already Covered

| Combination | Status | Owner of the rule |
| --- | --- | --- |
| Cache composition | Covered | Chapter 33 owns LRU, LFU and randomized sets |

Chapter 33 teaches eviction order across a map and a list. This chapter assigns no cache problem, and it reuses the ownership idea only for identifiers and stack slots.
