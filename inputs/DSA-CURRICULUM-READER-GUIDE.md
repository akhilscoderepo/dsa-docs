# Java DSA Interview Curriculum

This collection contains Chapters 00 through 41. It is arranged as a dependency sequence, not as a challenge to finish every page as quickly as possible. Work through one chapter until you can recognize its core states and solve the early staircase problems without notes. Then move forward.

## How To Study

Read the chapter explanation before opening LeetCode. For each micro-pattern, implement the Build problem first. The Vary problem changes one decision, the Boundary problem tests the condition most likely to break the invariant, and Recognize asks you to identify the same structure inside a normal interview prompt.

Do not measure progress by pages read or questions submitted. A chapter is usable when you can explain the recognition cue, name the maintained state, justify the complexity, implement the central method, and distinguish it from the nearest false friend.

If a later problem combines several techniques, return to the owning chapter's unlocked-combination lesson. Combination problems are placed after the final prerequisite rather than scattered through early chapters.

## Phase 1 - Sequence Foundations

### Chapters 00-05

- 00 Problem contracts, complexity, and sequence language
- 01 Arrays: core operations
- 02 Matrices and two-dimensional arrays
- 03 Strings
- 04 Hash maps and sets
- 05 Sorting and Java comparators

This phase establishes the vocabulary used everywhere else: input and output contracts, mutation boundaries, traversal state, equality, ordering, canonical representations, and the cost of Java collection operations. Do not skip Chapter 00 merely because the individual ideas look familiar. It teaches how to state the contract before selecting an algorithm.

## Phase 2 - Boundaries And Ranges

### Chapters 06-13

- 06 Binary search
- 07 Prefix sums and difference arrays
- 08 Two pointers
- 09 Sliding window
- 10 Intervals
- 11 Stacks and queues
- 12 Monotonic stacks
- 13 Deques and monotonic queues

These chapters are easy to confuse because several techniques move boundaries through a sequence. The decisive question is what state makes movement safe. Binary search maintains a feasible search region. Two pointers rely on an ordering or partition relationship. Sliding windows maintain a property of one contiguous range. Monotonic structures keep only candidates that can still matter.

Chapter 13 is intentionally demanding. Return to it after Chapters 09 and 12 if the deque invariants do not yet feel natural.

## Phase 3 - Linked And Hierarchical State

### Chapters 14-20

- 14 Linked lists
- 15 Tree depth-first search
- 16 Tree breadth-first search and binary search trees
- 17 Heaps and priority queues
- 18 Tries
- 19 Recursion and backtracking
- 20 Greedy algorithms

This phase shifts from index boundaries to structural ownership and choice. State may live in links, recursive return values, a search path, a heap frontier, or a proof that one local decision cannot damage the best global result.

Tree DFS and backtracking both use recursion, but their contracts differ. A tree traversal usually receives a fixed structure and returns information about it. Backtracking constructs a partial choice, explores it, and undoes the mutation before trying the next choice.

## Phase 4 - Graph Models

### Chapters 21-25

- 21 Graph traversal with DFS and BFS
- 22 Multi-source, bidirectional, and state-space BFS
- 23 Directed graphs and union-find
- 24 Shortest paths and graph state modeling
- 25 Advanced graph optimization

The hardest graph decision is often the model rather than the traversal. State the vertices, edges, edge costs, and complete visited key before selecting BFS, Dijkstra, topological processing, union-find, or a low-link algorithm. When the same node can be reached with different resources or modes, the state is a pair such as `(node, remaining resource)`, not merely the node.

## Phase 5 - Dynamic Programming

### Chapters 26-29

- 26 Dynamic programming foundations
- 27 Capacity and partition patterns
- 28 State machines and sequence DP
- 29 Interval and advanced-state DP

Do not begin by drawing a table. Define what one state means, what decision changes it, which smaller states it depends on, and the order in which those dependencies become available. Memoization and tabulation are implementations of that recurrence, not substitutes for it.

Finish Chapter 26 before separating 0/1 choices from reusable choices, stock states, subsequence relationships, interval states, tree DP, bitmask state, or digit-prefix state.

## Phase 6 - Advanced Interview Tools

### Chapters 30-35

- 30 Bits, number theory, and interview numerics
- 31 Range-query structures and sweep processing
- 32 Selection and ordered-data techniques
- 33 Design-data-structure problems
- 34 Advanced strings
- 35 Advanced search, sampling, and geometric state

These chapters are part of the complete collection, but their priority depends on the companies and roles you target. They cover interview-relevant techniques that appear less frequently than arrays, trees, graphs, and foundational DP, while remaining important for stronger loops and specialized teams.

Chapter 33 is the bridge from DSA into design. It teaches API state and composite invariants for caches, randomized sets, and iterators. Concurrent caches, expiry, persistence, and distributed ownership belong to the later concurrency, machine-coding, and system-design curricula.

## Phase 7 - Design Problems

### Chapters 36-41

- 36 Stateful containers and histories
- 37 Iterators, encodings, and versioned state
- 38 Streaming and temporal state
- 39 Dynamic query structures
- 40 Composite indexes and allocation
- 41 Algorithmic services and simulations

LeetCode's Design tag does not mean low-level or high-level system design. These problems still ask for bounded in-memory algorithms, but the input arrives as a constructor followed by public method calls. Correctness therefore lives across a history of operations. The important questions are which fields form the state, which method owns each mutation, which indexes must agree, and what complexity every call promises.

These chapters come last because they deliberately combine the earlier curriculum. A movie-rental system needs maps, ordered sets, and cross-index repair. A hit counter needs queues and temporal windows. A dynamic graph calculator needs shortest paths plus an update/query contract. A search autocomplete system needs tries, ranking, and mutable frequency state.

Do not attempt to solve the entire Design tag. Follow the [Design mastery path](design-mastery-path.md): 24 required anchors teach the reusable state models, and 12 transfer problems test whether you can recognize those models behind a different API. The rest of the tag is an author reference inventory, not assigned work.

Finish the Design extension before moving to LLD or machine coding. The later curricula will change the scale and engineering contract by adding extensibility, persistence, concurrency, failures, testing, and deployment concerns.

## The Review Loop

After every three or four chapters, choose unfamiliar problems rather than replaying memorized solutions. For each attempt, record the recognition cue you missed, the invariant you failed to maintain, or the implementation boundary that caused the bug. Review the decision, not just the final code.

A productive review session contains one fresh problem, one previously failed problem, and one verbal explanation without an editor. This tests recognition, repair, and communication separately.

## Completion Standard

You do not need instant recall of every hard problem. You should be able to identify the main family, propose a direct solution, explain why it is insufficient, derive the relevant state or invariant, implement the standard form, and test hostile boundaries.

Once those actions are reliable across Chapters 00-41, move to low-level design, concurrency, machine coding, and high-level system design. Keep DSA alive with mixed review rather than restarting the curriculum from Chapter 00.
