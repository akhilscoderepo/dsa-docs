<!-- section: orientation -->
## Orientation

A queue class passes every test that adds three items and removes three items. In production it treats a full queue as empty, because `head` and `tail` meet after a wraparound and equal indices cannot separate the two states. Class-shaped problems fail at the seams between calls, not inside one method. This chapter teaches how to keep one stored state valid across any legal sequence of public calls.

### Prerequisites

You should know arrays, lists, stacks, queues, deques, hash maps, linked lists, heaps and ordered sets, plus amortized cost. A **public call** is any method an outside caller may invoke. A **logical state** is what a caller can observe through those calls. The **fields** are the stored variables that together represent it.

### What Each Lesson Protects

Each lesson names one fact that every public call must leave true.

- **Trace A Sequence Of Method Calls** defines legal states and shows that a rejected call must leave every field unchanged.
- **Store Keys In Direct Slots** gives each key one slot or bucket, so update and removal keep that ownership.
- **Circular Buffers** reuse array positions with `head`, `size` and modular arithmetic, so no live slot is counted twice.
- **Split Containers** keep two halves within one element of each other, so the boundary marks the middle.
- **Cut Forward History After A Write** separates the stored pages from the cursor, so a new write drops the invalid future.
- **Reuse Freed Identifiers From A Pool** keeps each identifier in exactly one of the free or allocated states.
- **Containers And API State** joins a ring buffer with an index so every call restores both before it returns.
- **Multiple Collections Ownership** keeps a heap or ordered set and a membership set in agreement about each resource.

### Reading Order

Every lesson starts with a class that passes simple tests and then breaks on a longer call sequence. You predict the failure before the reasoning appears. Two traces follow the fields call by call, then Java code and the limits of the idea. The four exercises climb from a basic build to a variation, an edge case and a recognition problem. A LeetCode problem that appears twice carries a changed contract, and its text says what changed.

### What You Can Do After This Chapter

You can write down the fields of a class and the one fact they must satisfy after every call. You can choose between a direct array, a ring buffer, two halves, a cursor over stored history and a pool that hands out the smallest free id, and you can say what each call does when it must refuse. Cache designs belong to chapter 33, and concurrency belongs to the separate senior curriculum.
