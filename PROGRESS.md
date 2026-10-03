# Progress

Statuses: done | claimed NN <UTC time> | todo. Update on every chapter.

| Chapter | Status |
|---|---|
| 00-problem-contracts-complexity-and-sequence-language | done |
| 01-arrays-core-operations | done |
| 02-matrices-and-2d-arrays | done |
| 03-strings | done |
| 04-hash-maps-and-sets | done |
| 05-sorting-and-java-comparators | done |
| 06-binary-search | done |
| 07-prefix-sums-and-difference-arrays | done |
| 08-two-pointers | done |
| 09-sliding-window | done |
| 10-intervals | claimed 10 2026-10-03T15:33Z |
| 11-stacks-and-queues | claimed 11 2026-10-03T15:39Z |
| 12-monotonic-stacks | done |
| 13-deques-and-monotonic-queues | todo |
| 14-linked-lists | todo |
| 15-trees-dfs | todo |
| 16-trees-bfs-and-bsts | todo |
| 17-heaps-and-priority-queues | todo |
| 18-tries | todo |
| 19-recursion-and-backtracking | todo |
| 20-greedy | todo |
| 21-graph-traversal-models-dfs-and-ordinary-bfs | todo |
| 22-bfs-variations | todo |
| 23-directed-graphs-and-union-find | todo |
| 24-shortest-paths-and-graph-state-modeling | todo |
| 25-advanced-graph-optimization | todo |
| 26-dynamic-programming-foundations | todo |
| 27-dynamic-programming-capacity-and-partition-patterns | todo |
| 28-dynamic-programming-state-machines-and-sequences | todo |
| 29-dynamic-programming-intervals-and-advanced-states | todo |
| 30-bits-number-theory-and-interview-numerics | todo |
| 31-range-query-structures-and-sweep-processing | todo |
| 32-selection-and-ordered-data-techniques | todo |
| 33-design-data-structure-problems | todo |
| 34-advanced-strings | todo |
| 35-advanced-search-sampling-and-geometric-state | todo |
| 36-stateful-containers-and-histories | todo |
| 37-iterators-encodings-and-versioned-state | todo |
| 38-streaming-and-temporal-state | todo |
| 39-dynamic-query-structures | todo |
| 40-composite-indexes-and-allocation | todo |
| 41-algorithmic-services-and-simulations | todo |

## Notes
- 05 (2026-10-03): Spec LC reuse inside the chapter was resolved by changing the contract/invariant, with the LC number kept so spec parity holds. Largest Number (179): lesson 01 builds the glue order; lesson 03 re-asks it as a comparator-law proof. Queue Reconstruction (406): lesson 04 sorts tallest-first and inserts at index; lesson 06 sorts shortest-first and fills the k-th empty slot. Contains Duplicate (217): lesson 02 sorts in place; lesson 07 sorts a copy and measures run length. Intersection (349) is answered by sorting concatenated distinct lists, since two pointers belong to Chapter 08. Missing Number (268) uses sorted index mismatch.
- 06 (2026-10-03): LC 74 appears in lesson 01 as a virtual-array recognition exercise and in lesson 11 as a row-first Build (first-column bound, then in-row search); the solution also cross-checks the virtual-index form. LC 981 appears twice in lesson 10 (Vary: the store; Boundary: early query and missing key, guarded step back), which leaves one expected spec-role WARN. LC 278 appears in lessons 02 (candidate kept on a hit) and 04 (half-open first-true). LC 911 is added as an Extend exercise because the ladder table lists it. LC 1146 is the Recognize exercise. Lesson 09 uses a fixed 100-round bisection policy and shows the epsilon-loop non-termination under a capped loop. Remaining WARNs: the spec-role WARN above and a 3-file template-phrase WARN on the "linear scan" oracle sentence in the solutions.
- 08 (2026-10-03): content complete, human review pending. Repeated problems changed contract: LC 167 classic in 01, unsorted original indices in 08. LC 15 lists triplets in 05, existence with a long target in 06, count on a cloned input in 08. LC 18 lists quadruplets in 05, counts near int limits in 06, pruned listing in 08. LC 16 closest value in 06, smaller-sum tie rule in 08. LC 287 standard in 07, [duplicate, tail, cycle] in 10; the 07 proof rung returns [phase-one stop, duplicate]. LC 27 returns [k, moves]; LC 283 uses Token objects; LC 26 keeps the last of each run; LC 80 takes a limit L. Earlier chapters contained none of LC 125, 344, 680, 392, so standard contracts are used. Remaining WARNs: 07 low-diversity (insight vocabulary) and 07 spec-role (proof rung is tagged LC 287 twice).
- 07 (2026-10-03): LC reuse inside the chapter was resolved by changing the contract. 560: lesson 04 uses int keys; lesson 11 re-asks it with `long` keys and the `get(0)` boxing hazard. 525: lesson 05 returns the length; lesson 11 returns the span `[start, end]` with strict-longer tie rule. 974: lesson 06 uses an array of `k` counters; lesson 11 uses a map with k up to 1e9 and a `long` answer. 523: lesson 06 returns existence; lesson 11 returns the earliest-ending pair. 1310: lesson 02 is the offline table; lesson 07 is an append-only XOR log. 238: lesson 03 Vary is the two-pass version; the zeros Boundary uses a zero-count method cross-checked against the passes, which gives one expected spec-role WARN. Remaining WARNs: that spec-role WARN and a 3-file template-phrase WARN on the 560 and 974 problem-statement wording.
- 09 (2026-10-03): content complete, human review pending. LC 567: boolean in 02, first start with a matches counter in 10. LC 3: length in 03, [start, length, shrinkSteps] in 10. LC 424: stale-max length in 07, both policies compared in 09, exact-max [start, length] in 10. LC 76: classic in 04, [count of shortest starts, leftmost] in 10. Remaining WARN: 03 template-phrase ('left and right are the inclusive edges of' recurs in 3 files).
- 12 (2026-10-03): content complete, human review pending. Chapters 10 and 11 were claimed by other sessions inside the 6-hour window, so this run took 12; the add_repo and register_repo_root tools were not available in this session, and the existing clone with push access was used. LC 907 appears in lessons 05, 06 and 08 with a different contract each time: 05 returns [sum mod, owned-subarray count] to verify the tie rule, 06 prices each index at removal in one pass with no wall arrays and values up to 1e9, and 08 changes it to a sum of subarray ranges (max minus min) with two ownership passes. LC 496 appears in lesson 01 (value-keyed map over distinct values) and in 08 (queries are positions into an array with repeated values, so answers are keyed by position). LC 739 in 01 returns distances, and in 08 returns [sum of waits, longest wait]. LC 84 in 07 is the standard problem, and in 08 it returns [area, start, end] with a smallest-start tie rule. The extra LC repeats leave expected spec-role WARNs. Lesson 08 is the released combination lesson. Remaining WARNs: eight low-diversity trace-vocabulary warnings (generated trace notes reuse words by design), one low-diversity insight warning in 05, and a template-phrase WARN in solutions ('scan left to right with a stack of' recurs in 3 files).
