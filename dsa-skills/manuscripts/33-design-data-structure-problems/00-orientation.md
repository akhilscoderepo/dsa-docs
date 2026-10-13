<!-- section: orientation -->
## Orientation

A cache returns a stale value after an eviction. A random-pick service returns a deleted item. An iterator skips one element after a second call to `hasNext`. In each case every method looks correct alone, and the failure appears only after a particular sequence of calls. Design problems ask for a class whose operations stay correct and fast across any such sequence.

### Prerequisites

You should know hash maps and sets from the chapter on hash maps and sets, dynamic arrays and doubly linked lists from the chapters on arrays and linked lists, stacks from the stack chapter, and the in-order walk of a binary search tree. A **contract** is the promise an operation makes about its legal input, its output, its mutation of state, its failure behavior and its cost. An **invariant** is a fact about the stored fields that holds again at the end of each operation.

### The Six Lessons

Each lesson answers one question about keeping state correct across public calls.

- **Write The Contract Before The Code** states output, mutation, failure and cost for each operation before any field is chosen.
- **One Method Repairs Each Link** gives every cross-field repair to exactly one method, so a rejected call leaves all fields unchanged.
- **Pair A Map With Ordered Storage** uses a hash map for lookup and a list or array for position, with cross references that stay synchronized.
- **Keep Traversal State Between Calls** caches one element so that `hasNext` and `peek` consume nothing.
- **Pick A Random Value In Constant Time** removes by swapping with the last slot and repairs the moved value's index.
- **Evict The Least Recent Entry** builds recency caches, first by last use and then by use count.

### The Three Closing Lessons

Each closing lesson joins earlier parts into one structure and names what each part contributes.

- **Locate By Key And Order By Recency** joins a map and a linked list, with exercises on relinking, resizing, capacity one and an eviction log.
- **Find A Slot And Pick From Array** joins a map and a dynamic array, with exercises on swap removal, an exclusion pick, the last slot and duplicate values.
- **Traversal State Across Public Calls** joins iterators with trees, wrappers and nested sources, with exercises on a node pool, a source that cannot restart, a depth limit and rotation among sources.

### How To Work Through Each Lesson

A lesson opens with a failing sequence of calls. A direct implementation follows, and you predict where it breaks before the explanation appears. Later parts name the invariant, list the state, follow two traces, show the code and say when the idea stops fitting. Each exercise set runs from the basic structure through a variation and an edge case to a recognition problem. Several LeetCode problems return with a changed contract, and the problem text says what changed.

### What You Can Do After This Chapter

You can write the contract of a class before coding it. You can name the invariant that links its fields and the one method that repairs each link. You can pick the pair of structures that gives constant-time lookup together with the ordering or position a problem needs. Concurrent designs are outside this chapter and wait for a later chapter on specialized services.
