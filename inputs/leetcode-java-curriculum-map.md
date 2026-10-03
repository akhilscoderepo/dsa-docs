# LeetCode Java Curriculum - Coverage Map

This map is the build contract for the PDF library. A chapter is not generated until its subtopics, prerequisites, exclusions, worked examples, and practice ladders are specified. Chapter size follows this coverage; it is never reduced to meet a page target.

## Curriculum outcome and micro-pattern standard

The outcome is not recognition of a few macro labels such as “arrays” or “graphs.” When the library is complete, the learner should be able to identify the smaller structural family inside a new interview problem, explain why its state is sufficient, implement it in Java without template dependence, and distinguish it from its nearest alternative. A macro chapter is therefore complete only when its independently recognizable micro-patterns are complete.

A micro-pattern receives a separate lesson and 4-7 problem ladder when it changes any of: the recognition cue, the maintained state, the invariant, the safe movement/discard rule, or the prerequisite set. For example, fixed-size windows, minimum-cover windows, and exactly-K windows are separate subtopics; so are lower-bound search, peak search, and answer-space search. They may share a chapter, but never share one vague explanation or one undifferentiated problem bank.

The original Java Pattern Handbook Sessions 1-3 and Java Cheat Sheet are mandatory coverage references. Before a replacement PDF is generated, its coverage map must crosswalk every relevant original micro-pattern to (a) an explicit lesson in this library, (b) a later composition chapter, or (c) a documented exclusion because it is redundant, non-interview-relevant, or requires a later prerequisite. The new library improves the prose, progression, examples, and practice depth; it must not silently lose the original taxonomy.

## Active build package

The active LeetCode-style specification contains Chapters 00-41. Chapters 00-35 cover foundations through advanced strings and randomized/search techniques. Chapters 36-41 form a curated Design-problem extension; their PDFs remain pending until the specifications are reviewed.

Each active chapter is rebuilt or created from its full coverage map, then text-checked, rendered, visually checked, and added to the ZIP only after it passes. The prior short Strings and Hash Maps/Sets PDFs are not package candidates; their replacements must meet the same gate as new chapters.

The per-chapter source specifications live in [`chapter-specs/`](chapter-specs/README.md). They are created before PDF authoring and hold the chapter's independent micro-pattern inventory, practice contract, Java integrity focus, reviewable **Unlocked Combinations Preview**, prerequisite/deferred-composition audit, publication gate, and research baseline. A PDF builder may refine a specification with verified representative problems, but may not silently narrow its scope.

## Chapter acceptance gate

A generated PDF is a draft, not a completed curriculum chapter. Do not mark it accepted, package it into the ZIP, or advance the build sequence until its owning row in this map has been crosswalked and every in-scope independent micro-pattern has all of the following:

- an explicit lesson that names the technique and explains its recognition cue, state or invariant, use case, and nearest confusing alternative;
- a Java implementation or deliberately justified deferral to the later composition chapter that owns the implementation;
- a staircase practice ladder: implementation, variation, boundary case, recognition problem, then relevant medium/hard extensions only after their prerequisites; and
- text extraction plus rendered visual QA confirming that the material is present and readable.

Do not substitute a broad topic label for its underlying micro-patterns. A chapter titled “Strings,” “Hash Maps and Sets,” or “Sorting” is incomplete if the PDF merely mentions a technique in prose, table, or scope paragraph without giving that technique its own teachable unit and practice ladder.

Current corrective rule: Chapters 03-05 must be rebuilt from the coverage map before Chapters 08 onward are treated as package work. In particular, Chapter 03 must separately cover normalization, fixed-alphabet counting, run-length construction, and center expansion; Chapter 04 must separately cover set membership, set-based sequence reasoning, frequency maps, key-to-index lookup, and grouping; Chapter 05 must separately cover ordering contracts, sort-and-sweep, sort-and-deduplicate, and Java comparator behavior. The currently generated Chapter 03-05 PDFs are drafts, not accepted package candidates.

## Composition discovery and release rule

Teach a topic's standalone primitives in its own chapter. Before generating every later chapter, run a **composition audit** across all earlier chapters and the new chapter's micro-patterns. The audit must discover, rather than rely on a manually remembered list of, combinations that have just become teachable.

For each candidate interview problem or pattern, identify its required primitives. A candidate becomes a composition lesson when it needs two or more independently taught primitives and its recognition cue, maintained state, invariant, safe movement rule, or failure mode is different from every standalone lesson. Its owner is the chapter that supplies the last missing prerequisite. Do not force a combination into an earlier chapter, and do not leave it implied after all prerequisites exist.

The audit for every chapter must use this procedure:

1. List the newly introduced micro-patterns and their state/invariant contracts.
2. Compare each one against every earlier micro-pattern and previously released composition, looking for a problem family that requires both.
3. Treat a candidate as newly unlocked only when the present chapter supplies the final required primitive. If it needs a later third primitive, leave it deferred until that chapter.
4. Reject false combinations: two labels appearing in the same problem are not enough. The combined problem must require both techniques to make a distinct decision; otherwise it remains an exercise under its single owning micro-pattern.
5. Add every accepted combination to the Deferred composition catalog and to a labelled **Unlocked Combinations** section in the owning PDF. Record participating topics, recognition cue, state contributed by each, invariant, nearest confusing pattern, prerequisites, representative problems, and a staircase practice ladder.

A composition lesson must name every participating technique, explain what each contributes, show why neither one alone is sufficient, and keep its practice ladder free of any still-untaught prerequisite. When a later chapter adds a third required primitive, create a new composition lesson with that complete prerequisite set; do not silently extend an older two-topic lesson.

This is a general dependency rule for the entire curriculum, including data-structure plus algorithm, algorithm plus algorithm, and three-or-more-topic compositions. Examples such as string-plus-map, heap-plus-intervals, graph-plus-heap, trie-plus-backtracking, and map-plus-linked-list are evidence that the audit is working, not an exhaustive hardcoded list.

## Coverage Audit Addendum

The following are high-frequency interview families that cannot be considered covered merely because a nearby macro chapter exists. They must be added to the named owner during rebuild planning, with their own recognition cue, state/invariant, and staircase ladder. This list is an audit result, not a replacement for the composition-discovery procedure above.

| Missing or weak family | Owner | Required distinction |
|---|---:|---|
| Running minimum plus best gain; running minimum plus best loss | 01 Arrays | A one-pass extremum-and-answer state, distinct from Kadane because the chosen pair is not a contiguous subarray. Include LC 121 / 122 sequencing only after the transaction contract is explicit. |
| Boyer-Moore majority vote | 01 Arrays | Candidate-cancellation state and its verification requirement. It is not a frequency map and not ordinary counting. |
| Pascal-style 2D construction | 02 Matrices | Build cells from already-computed neighbors; distinguish construction from grid DP and from matrix traversal. |
| Matrix plus set/map validation | 04 Hash maps and sets | Row/column/box membership state, for example Sudoku validation. It is released when hash-based membership becomes available. |
| Canonical string signature by sorting | 05 Sorting | String traversal supplies characters; sorting supplies the canonical key. Teach this as an unlocked composition, not as an aside. |
| Merge sort, partition/quicksort, and counting-sort tradeoffs | 05 Sorting | Divide-and-conquer merge state, partition invariant, and bounded-domain counting must be named. `Arrays.sort` familiarity is not sufficient coverage. |
| Monotone matrix search and partition-style binary search | 06 Binary search | Sorted matrix search and two-sorted-array partition search use different interval/partition invariants from exact search. Include LC 74 / 240 and LC 4 at the appropriate ladder depth. |
| Time-indexed key lookup | 06 Binary search | Map plus ordered timestamps plus binary search; released here because binary search is the final prerequisite. Include LC 981. |
| Prefix/suffix exclusion state | 07 Prefix sums and difference arrays | Product Except Self-style left/right accumulated state is neither a range-sum prefix nor a hashmap prefix-count pattern. Include LC 238. |
| Random-pointer cloning | 14 Linked lists | The existing composition catalog assigns this to Linked Lists; make that ownership explicit and do not leave it deferred indefinitely after HashMap is taught. Include LC 138. |
| Weighted interval scheduling | 26-29 Dynamic programming | Interval sorting alone is insufficient; predecessor lookup plus DP transition creates a separate family. |
| DAG dynamic programming | 26-29 Dynamic programming | Topological order supplies evaluation order, but path/count/minimize state is DP. Release only after both graph order and DP transitions are available. |

During each rebuild, re-audit this table along with the full composition audit. It is deliberately not a claim that every rare competitive-programming technique belongs in the package: additions must remain LeetCode/interview-relevant and satisfy the acceptance gate.

## Production Structure Gate

Coverage alone is not a usable learning system. Before a chapter is accepted, review its teaching structure with the following gate. A chapter that lists the right topics but fails this gate remains a draft.

### Chapter architecture

Each chapter must begin with a compact orientation that states: what prerequisite knowledge is assumed; which independently teachable micro-patterns will be learned; which nearby-looking patterns are intentionally deferred; and what new combinations become possible after the chapter. This prevents a learner from treating a macro label such as “Strings” or “Graphs” as one undifferentiated skill.

Every micro-pattern must be a self-contained lesson with this causal order: concrete context -> first plausible/brute-force idea -> bottleneck -> insight -> accepted technical name -> variable/state jobs -> narrative dry run -> readable Java -> complexity and boundary hazards -> challenge ladder. Do not compress two micro-patterns into one lesson when their recognition cue, state, invariant, or safe move differs.

### Java implementation integrity

Every chapter also receives a targeted Java implementation audit. This is not a repeated boilerplate page: teach a Java concern only when it changes the correctness, output contract, or asymptotic bound of a lesson in that chapter. The audit checks:

- the stated input guarantees versus any needed null, empty, singleton, rectangular, or ragged-shape guard;
- numeric range, including `long` accumulation, overflow-safe midpoint calculation, and comparator ordering with `Integer.compare` or `Long.compare` rather than subtraction;
- primitive/object boundaries and reference equality, including the fact that custom comparators require object arrays and that `.equals` compares object values;
- state extraction and output conversion, such as `entrySet()` traversal, consuming a heap deliberately, or returning `List<Integer>` state as an `int[]` when the signature requires it; and
- Java API costs that could silently break the claimed bound, including front operations on `ArrayList`, front insertion on `StringBuilder`, repeated string concatenation, linear `PriorityQueue.contains` / `remove(Object)`, and copying inside hot loops. Use `ArrayDeque` for ordinary stack/queue behavior.

Do not add guards merely from habit when a problem contract already rules out the condition. Do not state an API-cost rule without connecting it to the actual loop and supported Java behavior. The resulting code should look like interview-ready Java, not defensive boilerplate.

### Difficulty staircase review

Exercises are a progression, not a collection of titles. For each micro-pattern, the editor must identify the changed decision in every step:

| Step | Learner task | Permitted change |
|---|---|---|
| Build | Reproduce the newly taught state or operation | No new prerequisite or hidden second pattern |
| Vary | Adapt one rule | Output contract, local condition, or one state transition changes |
| Boundary | Protect the invariant | Empty input, duplicates, overflow, all-negative, endpoint, mutation, or similar hazard |
| Recognize | Identify the same pattern in an easy-side-medium prompt | Surface wording changes; state and prerequisites do not |
| Extend | Combine with an already taught prerequisite or add one justified state | The new contribution is explicitly taught before the problem |
| Medium / Hard | Solve an interview-grade composition | Every prerequisite is already owned; the new invariant is named |

Do not claim a staircase merely because problems are ordered by LeetCode difficulty. The progression is valid only when the learner can explain what changed from the preceding problem and why the previous state was insufficient.

### Unlocked-combination review

At the end of every chapter, add an **Unlocked Combinations** section. Generate it from the composition audit, not from a fixed list. For each newly released combination, show: participating prior and current micro-patterns; the contribution of each; the combined recognition cue; the new state/invariant; the nearest false friend; and the owner of any still-missing third prerequisite.

This section is mandatory in every PDF, including Chapters whose audit releases no new fully teachable composition. In that case, explicitly state `No new teach-now combinations` and list the nearest deferred combinations with their missing prerequisite and owning chapter. A passing chapter must never omit the section, hide it in an exercise hint, or substitute a generic transition paragraph.

For every **Teach now** entry, the current PDF must contain a dedicated combination lesson immediately before or within this section. The lesson must explain what each prerequisite contributes, the combined recognition cue, combined state/invariant, and the nearest single-topic false friend. It must then contain a separate staircase: Build, Vary, Boundary, Recognize, followed by relevant Extend/Medium/Hard problems only if every additional prerequisite is already taught. A deferred entry gets explanation and ownership only; it gets no premature exercises.

The section must distinguish three outcomes:

- **Teach now:** every prerequisite exists, so include a lesson and a staircase ladder in the current PDF.
- **Release later:** name the missing prerequisite and the chapter that will own the combination. This is a visible promise, not an omission.
- **Already covered:** link the combination to its existing owner; do not create duplicate explanations.

### Retention and confidence review

End each chapter with a short reconstruction and diagnostic loop: problems to reimplement from variable meanings, a small mixed recognition set drawn from previously learned chapters, and explicit “use this / do not use this” boundaries. At milestone chapters, add an integration lab that mixes only already taught topics and labels the prerequisites of every problem. This is where the learner practices choosing a pattern, rather than only following a chapter-local cue.

### Pre-publication audit

Before packaging a chapter, verify all of the following in the source and rendered PDF:

1. Every planned micro-pattern has exactly one owner and lesson.
2. Every exercise has a role in a valid staircase and names its changed decision.
3. Every newly unlocked combination is taught, visibly deferred, or linked to its existing owner.
4. No exercise depends on an untaught topic without an explicit deferral label.
5. The final decision map, reconstruction prompts, and integration material reflect the actual chapter content rather than generic boilerplate.
6. The rendered PDF contains a visible **Unlocked Combinations** heading. Its entries match the composition audit: every entry is classified as Teach now, Release later, or Already covered, and every Teach now entry has a named lesson or staircase owner in that PDF.
7. The chapter is not marked accepted when this checklist has not been completed against the rendered PDF. A generated file is a draft until the checklist is recorded as passed.
8. Every Teach now combination has its own explanation and staircase in the rendered PDF; a one-line reference, decision-table cell, or isolated representative problem does not pass this check.

## Build order and ownership

| Order | PDF chapter | Independent subtopics | Explicitly deferred compositions |
|---:|---|---|---|
| 00 | Problem contracts, complexity, and sequence language | constraints as algorithm signals, mutation/space contracts, subarray versus subsequence, input guarantees, complexity tradeoffs, amortized analysis (accounting/potential intuition), adversarial dry-runs, Java API/code-quality habits | specific data structures and algorithms |
| 01 | Arrays: Core operations | direct scans and result contracts, aggregation, stable write-index compaction, sorted in-place deduplication, bounded-domain frequency arrays, cyclic placement, in-place sign marking, Kadane maximum/minimum state, maximum-product max/min state, circular-subarray reasoning after ordinary Kadane | opposite-end/three-way partition pointers, prefix sums, binary search, sorting |
| 02 | Matrices and 2D arrays | shape contracts, row/column/diagonal/boundary traversal, direction-state and layer-state simulation, neighbor enumeration, in-place transpose/rotation, row-column marker state, spiral traversal | graph traversal, dynamic programming, sorted-matrix binary search |
| 03 | Strings | indexing/scans, immutable-result construction and `StringBuilder`, parsing/validation state machines, normalization, fixed-alphabet counting, run-length construction, center-expansion palindromes | opposite-end palindrome checks, sliding window, hash/sort grouping |
| 04 | Hash maps and sets | membership, counts, key-to-index lookup, grouping, set-based sequence reasoning, custom-key equality/hash contracts, bounded-domain direct-address versus hash representation | heap top-k, sort-based grouping, two-pointer combinations |
| 05 | Sorting and Java comparators | ordering contracts, `Arrays.sort`, `Comparator`, custom objects, stability guarantees and tie ownership, sort-and-sweep, sort-and-deduplicate, sort-then-scan | intervals, greedy, binary-search-on-sorted-input, quickselect |
| 06 | Binary search | exact search, first/last occurrence, lower/upper bounds, first-true predicate search, peak/mountain search, rotated minimum, rotated-array target search, integer answer-space feasibility search, continuous answer-space feasibility search | two-pointers, heaps, dynamic programming |
| 07 | Prefix sums and difference arrays | one-dimensional prefix, range query, prefix/suffix exclusion state, prefix-count maps, earliest-index/balance maps, remainder-class maps, prefix XOR, difference/range updates, 2D prefix, 2D difference rectangle updates | sliding window, segment tree/Fenwick tree |
| 08 | Two pointers | opposite-end sorted-pair scans, same-direction read/write scans, partitioning, Dutch-national-flag three-way partition, duplicate skipping, 3Sum/k-sum foundations, index-as-storage plus Floyd fast/slow cycle detection | sliding window, greedy, linked-list pointer techniques |
| 09 | Sliding window | fixed-size aggregate windows, fixed-size frequency/permutation windows, longest-valid windows, minimum-cover/deficit windows, at-most-K distinct windows, exactly-K-by-subtraction windows, replacement-budget windows, count-all-valid-subarrays windows, repeated-shrink versus non-shrinking policy | prefix-sum alternatives, heap/window combinations |
| 10 | Intervals | endpoint ordering contracts, touching-boundary semantics, merge/insert, two-list intersection, overlap removal/coverage decisions, sweep events with explicit tie policy | greedy scheduling, heap rooms |
| 11 | Stacks and queues | Java APIs and `ArrayDeque` null contract, FIFO simulation, queue via two stacks/amortized transfer, BFS queue state, matching delimiters, nested structure, min stack, queue-based level processing, nested decoding, calculator/string parsing, infix/postfix evaluation | monotonic structures, histogram/contribution counting |
| 12 | Monotonic stacks | next greater/smaller, circular next-greater, stock span, boundary discovery, duplicate-attribution policy, contribution counting, histogram rectangles | greedy stack and DP stack variants |
| 13 | Deques and monotonic queues | `ArrayDeque`, front/back invariants, dominated-back eviction, expired-front eviction, sliding maximum, sliding minimum, index expiry, shortest-subarray deque state | graph BFS and sliding-window combinations |
| 14 | Linked lists | node invariants, reverse, partial/k-group reversal, merge, dummy heads, cycle entry, intersection, middle nodes, fixed-gap kth-from-end, multilevel flattening | random-pointer copying, cache design and multi-list structures |
| 15 | Trees: DFS | binary/N-ary tree representation, preorder/inorder/postorder recursion, iterative DFS, depth/height/path state, diameter and subtree return values, balance sentinels, tree reconstruction from traversals, Morris traversal, quadtree construction | BFS, BST-specific ordering |
| 16 | Trees: BFS and BSTs | queue levels and zigzag/views, BST invariant/bounds, validate/search/insert, successor/predecessor, kth/range queries, general-tree and BST lowest common ancestor, iterator foundations, serialization/deserialization, balanced-tree concepts | heap traversal |
| 17 | Heaps and priority queues | Java `PriorityQueue`, min/max heap orientation and comparators, top-k, k-way merge, scheduling, lazy deletion/stale entries, running median and dual-heap balancing | graph shortest path and interval-room scheduling |
| 18 | Tries | prefix nodes, insert/search, wildcard branching, word break/trie search, binary tries for maximum XOR | trie-guided board backtracking |
| 19 | Recursion and backtracking | call state, choose/explore/unchoose, subsets, permutations, increasing-start combinations, reusable-candidate combination sum, duplicate control, proof-based pruning, partition generation, board constraints | trie-guided search and memoized pruning |
| 20 | Greedy | local choice, interval scheduling, reachability/farthest frontier, exchange reasoning in interviews, task selection | heap scheduling and two-pointer greedy |
| 21 | Graph traversal: models, DFS, and ordinary BFS | adjacency lists/matrices, graph cloning, visited state, components, grid graphs, path enumeration, unweighted shortest paths, bipartite check, directed/undirected cycle detection | multi-source/bidirectional search, weighted paths, union-find |
| 22 | BFS variations | multi-source initialization, layered-state meaning, bidirectional frontiers, implicit/state-space BFS, resource-state dominance | Dijkstra and weighted state transitions |
| 23 | Directed graphs and union-find | Kahn indegree topological order, DFS postorder and three-color directed-cycle detection, parent-aware undirected cycle detection, disjoint-set find/path compression, union by size, connectivity, Kruskal foundations | weighted shortest paths and advanced graph state |
| 24 | Shortest paths and graph state modeling | Dijkstra, stale heap entries, `(node, state)` search, constrained flights, alternating colors, 0-1 BFS | negative-weight paths and all-pairs algorithms |
| 25 | Advanced graph optimization | Bellman-Ford, Floyd-Warshall, Prim, Kruskal, Eulerian trails/Hierholzer, strongly connected components, bridges/articulation points, minimum spanning-tree decisions | flow, matching, and specialized contest algorithms |
| 26 | Dynamic programming: foundations | state definition, memoization/tabulation, linear recurrence, take/skip state, rolling-state compression, feasibility/count/minimize objectives, grid DP, transition discipline | knapsack, state machines, interval/subsequence DP |
| 27 | Dynamic programming: capacity and partition patterns | unbounded coin change, unbounded knapsack, 0/1 knapsack, subset/partition state, target sum, order-irrelevant combination counts, order-sensitive permutation counts | state-machine and interval DP |
| 28 | Dynamic programming: state machines and sequences | stock buy/sell states, cooldown/fee/transaction-count transitions, LIS O(n^2) and patience/binary-search O(n log n), LCS, edit distance, palindromic sequence state | interval/partition DP and bitmask DP |
| 29 | Dynamic programming: intervals and advanced states | matrix-chain-style interval state, palindrome table/partition state, tree DP and rerooting, bitmask assignment/grid-profile DP, submask/SOS aggregation, digit DP (tight/started state), problem-specific optimizations | advanced optimizations |
| 30 | Bits, number theory, and interview numerics | masks, shifts, low-bit operations, XOR, subset masks, overflow, binary arithmetic, gcd/fast power, sieve, modular arithmetic | bitmask DP |
| 31 | Range-query structures and sweep processing | Fenwick tree, segment tree, lazy propagation, coordinate compression, sweep-line event state | interval and ordered-map compositions |
| 32 | Selection and ordered-data techniques | quickselect, partition invariants, ordered maps/sets, merge-based counting | streaming and range-query compositions |
| 33 | Design-data-structure problems | API contracts, invariant ownership, O(1) data-structure composition, iterators, randomized sets, caches | specialized services and concurrency |
| 34 | Advanced strings | rolling hash, KMP/Z algorithm, palindrome radii, suffix arrays/automata, Aho-Corasick multi-pattern matching | trie/DP/string compositions |
| 35 | Advanced search, sampling, and geometric state | meet-in-the-middle, A* search, reservoir sampling, weighted random selection, rejection sampling, randomized partitioning | bitmask DP, state-space graph search, quickselect |
| 36 | Stateful containers and histories | operation traces, direct-address stores, circular buffers, split containers, cursor/history state, reusable resource pools, deferred bulk mutation | concurrent containers |
| 37 | Iterators, encodings, and versioned state | iterator protocols, nested/multi-source iteration, structural codecs, snapshots, preprocessed query objects, incremental tree APIs | concurrent iteration and persistence |
| 38 | Streaming and temporal state | fixed windows, expiry, online prefix recurrences, order statistics, frequency/uniqueness, temporal indexes, randomized evolving state | concurrent streams and distributed event time |
| 39 | Dynamic query structures | mutable range queries, dynamic interval unions, explicit ordered structures, deferred algebraic transforms, query planning, dynamic graph/tree query APIs | persistent and distributed indexes |
| 40 | Composite indexes and allocation | multi-index consistency, dynamic rankings, availability allocation, frequency buckets, validated priority, transaction lifecycles | transactional storage and concurrency |
| 41 | Algorithmic services and simulations | board simulations, hierarchical namespaces, dependency formulas, feed aggregation, ledgers, prefix-search services, lifecycle routing | LLD, machine coding, persistence, concurrency, and HLD |

## Original handbook integration register

This register makes the supplied Pattern Handbook the coverage floor. A grouped row is not permission to merge its entries in teaching: every semicolon-separated micro-pattern retains an independent recognition cue and practice ladder when its state or invariant differs. The grouping only records ownership in the new library.

| Original handbook micro-patterns | New owner | Integration decision |
|---|---|---|
| Linear scan/running state; read/write filtering; sorted duplicate removal; partition; Kadane; circular Kadane | 01 Arrays and 08 Two Pointers | Keep read/write and sorted dedup distinct from opposite-end and three-way partition movement. |
| Prefix sum; difference array; sum-K map; earliest zero-balance index | 07 Prefix sums and difference arrays | Keep direct range sums, range updates, count maps, and earliest-index maps as separate subsections. |
| Membership set; frequency map; canonical key/grouping | 04 Hash maps and sets | Teach membership, multiplicity, index lookup, and grouping as separate map-state contracts. |
| Opposite-end sorted pair; same-direction fast/slow; 3Sum/kSum | 08 Two Pointers | Preserve direction and duplicate policy as the distinction; linked-list fast/slow remains in 14. |
| Fixed-size; longest-valid; shortest-valid; at-most-K; exactly-K; frequency-match; replacement budget; count-valid-subarrays windows | 09 Sliding window | Preserve all eight window states; exactly-K is taught through subtraction, not mixed with longest-window reasoning. |
| Exact search; lower bound; upper bound; answer-space search; rotated search/minimum | 06 Binary search | Separate interval invariant and monotone predicate lessons. |
| Sort+sweep; sort+deduplicate; quickselect | 05 Sorting and 32 Selection | Quickselect is deferred until partition invariants and selection, rather than treated as ordinary sorting. |
| Nested LIFO; next/previous greater-smaller; histogram | 11 Stacks and queues; 12 Monotonic stacks | Preserve ordinary stack frames, nearest-boundary stack state, and histogram/contribution state. |
| BFS-style queue; sliding maximum; sliding minimum | 11 Stacks and queues; 13 Deques and monotonic queues | FIFO traversal is distinct from value-monotone deque state. |
| Min/max heap; bounded top-K; two-heaps median | 17 Heaps and priority queues | Preserve heap orientation, bounded selection, merge/scheduling, lazy deletion, and balanced-half invariants. |
| Merge intervals; interval intersection; meeting rooms; earliest finish; furthest reach; minimum jumps; resource assignment | 10 Intervals; 17 Heaps; 20 Greedy | Keep endpoint sweep, two-list intersection, heap resource allocation, interval selection, and reachability frontier distinct. |
| Reverse list; dummy node; middle; kth from end | 14 Linked lists | Preserve link rewiring, sentinel ownership, fast/slow center, and fixed-gap pointer states. |
| Character frequency; center expansion; matrix boundary traversal; implicit-grid traversal | 03 Strings; 02 Matrices; 21 Graph traversal | Center expansion is a string-local symmetry state; grid connectivity moves to graph traversal. |
| Preorder/inorder/postorder; iterative DFS; level BFS; height; diameter; balance; LCA; root-to-leaf path; BST bounds; kth smallest | 15 Trees DFS; 16 Trees BFS and BSTs | Preserve traversal return contracts, level state, and BST ordering operations as independent lessons. |
| Subsets; combinations; permutations; duplicate combinations; reusable combination sum; pruning | 19 Recursion and backtracking | Keep choice representation, duplicate policy, reuse permission, and pruning proof separate. |
| Basic/prefix trie; trie-guided board search | 18 Tries; 19 Backtracking | Basic prefix ownership precedes the later trie-plus-board composition. |
| Graph representation/components; unweighted BFS; multi-source BFS; state-space BFS; Kahn/DFS topological order; DSU operations/cycle detection | 21 Graph traversal; 22 BFS variations; 23 Directed graphs and union-find | Preserve fixed-node, multi-source, and expanded-state BFS; preserve dependency and connectivity models. |
| Dijkstra; 0-1 BFS; Bellman-Ford; Kruskal; Prim | 24 Shortest paths; 25 Advanced graph optimization | Separate edge-weight assumptions and MST cut/cycle reasoning. |
| Deadline heap scheduling; remove-K-digits; stack-based string parsing; grid shortest path/grid multi-source BFS | 20 Greedy; 12 Monotonic stacks; 11 Stacks; 22 BFS variations | Retain these as explicit cross-topic compositions after both prerequisites are taught. |
| Take/skip; state compression; 0/1 and unbounded knapsack; subset sum; count combinations/permutations; grid DP; LCS; edit distance; LIS | 26-28 Dynamic programming | Preserve objective type, reuse rule, sequence relationship, and optimization level as distinct DP families. |
| Stock hold/cash; cooldown; bounded transactions; interval DP; palindrome DP; tree return states/rerooting; assignment bitmask; digit DP | 28-29 Dynamic programming | Preserve state-machine, interval, tree, subset-mask, and digit-prefix representations. |
| Floyd-Warshall; SCC Kosaraju/Tarjan; bridges; articulation points; Fenwick; segment/lazy tree | 25 Advanced graphs; 31 Range-query structures | Keep all-pairs, component, low-link, point-update, and range-update invariants separate. |
| KMP; Z; rolling hash; DP+monotonic deque; DP+binary search; DAG/SCC DP; meet-in-the-middle; SOS aggregation | 34 Advanced strings; 29 Advanced DP; 35 Advanced search | Preserve string reuse state, dominated-state optimization, condensed-graph DP, split enumeration, and submask aggregation. |
| LRU; Insert/Delete/GetRandom O(1) | 33 Design-data-structure problems | Preserve map-list ownership and map-array swap-with-last ownership as separate APIs. |

## Deferred composition catalog

These problems are deliberately not used as early-topic filler. Each belongs to the chapter that introduces the last required prerequisite, where the combination itself is explained and practiced.

| Composition | Owning chapter | Representative problems | What the learner must combine |
|---|---|---|---|
| Hash map + prefix state | Prefix sums and difference arrays | LC 560 Subarray Sum Equals K; LC 525 Contiguous Array | A prefix value becomes a map key whose earliest/count occurrence has a defined meaning. |
| Array value + index state | Arrays: Core operations | LC 41 First Missing Positive; LC 442 Find All Duplicates in an Array; LC 448 Find All Numbers Disappeared in an Array | A bounded value domain lets an element's value name an array position; cyclic placement and sign marking have different mutation invariants. |
| Array local product state | Arrays: Core operations | LC 152 Maximum Product Subarray | A negative value swaps the useful maximum-ending and minimum-ending products, so one Kadane sum state is insufficient. |
| Prefix remainder/XOR state | Prefix sums and difference arrays | LC 523 Continuous Subarray Sum; LC 974 Subarray Sums Divisible by K; LC 1310 XOR Queries of a Subarray | Equivalent remainder or XOR prefix states encode a range property; the map key is not necessarily the raw numeric prefix. |
| Sorting + two pointers | Two pointers | LC 15 3Sum; LC 16 3Sum Closest | Sorting creates the monotone relationship that makes safe pointer movement possible. |
| Sliding window + frequency state | Sliding window | LC 3 Longest Substring Without Repeating Characters; LC 76 Minimum Window Substring | A map/count array describes the window while both boundaries move. |
| Sliding window + exact-count transformation | Sliding window | LC 930 Binary Subarrays With Sum; LC 992 Subarrays with K Different Integers; LC 1248 Count Number of Nice Subarrays | When “at most K” is tractable, exactly K is the difference of two at-most counts; it is not the same state as a longest-valid window. |
| Deque + sliding window | Deques and monotonic queues | LC 239 Sliding Window Maximum; LC 1438 Longest Continuous Subarray With Absolute Diff | The deque stores candidate indices in value order and expires indices outside the window. |
| Stack + histogram / contribution counting | Monotonic stacks | LC 84 Largest Rectangle in Histogram; LC 907 Sum of Subarray Minimums | Monotone boundaries determine the range for which an element is decisive. |
| Greedy + monotonic stack | Greedy | LC 402 Remove K Digits | Removing a larger preceding digit is safe only while a smaller current digit makes the numerical prefix lexicographically better. |
| Stack + expression state | Stacks and queues | LC 150 Evaluate Reverse Polish Notation; LC 394 Decode String; LC 224 Basic Calculator | The stack retains unresolved operands, operators, or nested parse frames. |
| Stack + parsing state | Stacks and queues | LC 71 Simplify Path; LC 224 Basic Calculator; LC 227 Basic Calculator II | Tokens and nested frames are consumed only when their local grammar is complete; whitespace, unary signs, and precedence are explicit input contracts. |
| Hash map + linked list | Design-data-structure problems | LC 146 LRU Cache; LC 460 LFU Cache | A map finds a node while a doubly linked list changes recency/frequency order in O(1). |
| Hash map + random-pointer graph | Linked lists | LC 138 Copy List with Random Pointer | The map preserves the identity mapping from each original node to its clone before random links are connected. |
| Hash map + dynamic array | Design-data-structure problems | LC 380 Insert Delete GetRandom O(1); LC 381 Insert Delete GetRandom O(1) - Duplicates Allowed | The map repairs an index after swap-with-last; the array enables random selection. |
| Iterator/design API state | Design-data-structure problems | LC 173 BST Iterator; LC 284 Peeking Iterator; LC 341 Flatten Nested List Iterator | The class invariant carries deferred traversal state across API calls. |
| Heap + intervals | Heaps and priority queues | LC 253 Meeting Rooms II; LC 2406 Divide Intervals Into Minimum Number of Groups | Sorted starts expose the next event; a min-heap tracks the earliest resource release. |
| Greedy + deadline heap | Greedy | LC 630 Course Schedule III | Sorting exposes deadline order; a max-heap ejects the longest selected duration when feasibility is violated. |
| Heap + two balanced halves | Heaps and priority queues | LC 295 Find Median from Data Stream; LC 480 Sliding Window Median | A max-heap and min-heap partition the stream around the current median. |
| Heap + delayed deletion | Heaps and priority queues | LC 480 Sliding Window Median; LC 1675 Minimize Deviation in Array | A heap may contain stale entries when arbitrary removal is unavailable; a validity map or version check controls when a root is usable. |
| Trie + backtracking | Recursion and backtracking | LC 212 Word Search II | Trie prefix failure prunes DFS branches over the board. |
| Trie + bitwise prefixes | Tries | LC 421 Maximum XOR of Two Numbers in an Array; LC 1707 Maximum XOR With an Element From Array | A binary trie selects the opposite bit whenever that preserves a higher XOR bit. |
| Tree traversal + structural encoding | Trees: BFS and BSTs | LC 297 Serialize and Deserialize Binary Tree; LC 100 Same Tree | Null markers preserve tree shape; decoding consumes tokens under the same contract. |
| Tree traversal-pair reconstruction | Trees: DFS | LC 105 Construct Binary Tree from Preorder and Inorder Traversal; LC 106 Construct Binary Tree from Inorder and Postorder Traversal | The traversal order fixes a root while the inorder position splits the remaining values into structural subproblems. |
| Graph BFS + multiple sources | BFS variations | LC 994 Rotting Oranges; LC 542 01 Matrix | Every source starts at distance zero; first visit fixes the nearest-source distance. |
| Graph BFS + two frontiers | BFS variations | LC 127 Word Ladder; LC 752 Open the Lock | Expand the smaller frontier; an intersection joins two shortest partial paths. |
| Graph + heap | Shortest paths and graph state modeling | LC 743 Network Delay Time; LC 1631 Path With Minimum Effort | The heap selects the unsettled state with smallest current cost. |
| Graph + expanded state | Shortest paths and graph state modeling | LC 787 Cheapest Flights Within K Stops; LC 1129 Shortest Path with Alternating Colors | The visited/distance key is `(node, state)`, not just the node. |
| Graph + union-find + maps | Directed graphs and union-find | LC 721 Accounts Merge; LC 1202 Smallest String With Swaps | Map external labels to components; union-find supplies connectivity. |
| Graph DFS + edge-use state | Advanced graph optimization | LC 332 Reconstruct Itinerary; LC 753 Cracking the Safe | Hierholzer consumes each directed edge once, then appends vertices on backtracking. |
| Graph DFS + low-link state | Advanced graph optimization | LC 1192 Critical Connections in a Network | Discovery and low-link times distinguish a bridge from an ordinary back edge. |
| DP: unbounded capacity | DP capacity and partition patterns | LC 322 Coin Change; LC 518 Coin Change II | A state may reuse the same item; loop order distinguishes reuse from 0/1 choice. |
| DP: partition/subset | DP capacity and partition patterns | LC 416 Partition Equal Subset Sum; LC 494 Target Sum | Boolean/count state represents reachable totals under a bounded choice rule. |
| DP: stock/state machine | DP state machines and sequences | LC 121 Best Time to Buy and Sell Stock; LC 309 Best Time to Buy and Sell Stock with Cooldown; LC 714 Best Time to Buy and Sell Stock with Transaction Fee | Each state states whether a stock is held and what transaction restrictions remain. |
| DP: interval/partition | DP intervals and advanced states | LC 312 Burst Balloons; LC 132 Palindrome Partitioning II | Choose the final action within an interval, then combine independent subintervals. |
| Bitmask + DP/backtracking | DP intervals and advanced states | LC 698 Partition to K Equal Sum Subsets; LC 847 Shortest Path Visiting All Nodes | A mask precisely represents which choices or vertices have been used. |
| Digit construction + DP state | DP intervals and advanced states | LC 902 Numbers At Most N Given Digit Set; LC 600 Non-negative Integers without Consecutive Ones | The state records digit position, prefix tightness, and the constraint-relevant prior digit/state. |
| Row profile + DP state | DP intervals and advanced states | LC 1240 Tiling a Rectangle with the Fewest Squares | A mask/profile records the unfinished boundary of the partially filled grid. |
| Meet-in-the-middle + subset state | Advanced search, sampling, and geometric state | LC 1755 Closest Subsequence Sum; LC 2035 Partition Array Into Two Arrays to Minimize Sum Difference | Split an exponential choice set into two halves, then combine compatible summaries. |
| Graph heuristic + heap | Advanced search, sampling, and geometric state | LC 1293 Shortest Path in a Grid with Obstacles Elimination; LC 1091 Shortest Path in Binary Matrix | A state includes location and resource; A* is contrasted with ordinary BFS/Dijkstra when a valid heuristic exists. |
| Randomization + index state | Advanced search, sampling, and geometric state | LC 398 Random Pick Index; LC 528 Random Pick with Weight | The maintained state makes each eligible outcome receive its required probability. |
| Randomization + acceptance region | Advanced search, sampling, and geometric state | LC 478 Generate Random Point in a Circle; LC 497 Random Point in Non-overlapping Rectangles | Candidate generation and acceptance/weighting must preserve the requested distribution. |
| Trie automaton + stream state | Advanced strings | LC 1032 Stream of Characters | Automaton/trie state summarizes all active pattern prefixes while text arrives. |
| Circular containers + API state | Stateful containers and histories | LC 622 Design Circular Queue; LC 641 Design Circular Deque; LC 3508 Implement Router | Modular storage, full/empty semantics, and every secondary index survive arbitrary call sequences. |
| Iterator + traversal state | Iterators, encodings, and versioned state | LC 284 Peeking Iterator; LC 341 Flatten Nested List Iterator; LC 1586 BST Iterator II | Traversal state persists across calls while observation and consumption remain distinct. |
| Queue + temporal window | Streaming and temporal state | LC 933 Number of Recent Calls; LC 362 Design Hit Counter; LC 1797 Authentication Manager | Expiry boundaries and lazy cleanup preserve the observable active window. |
| Ordered set + interval state | Dynamic query structures | LC 352 Data Stream as Disjoint Intervals; LC 715 Range Module; LC 2276 Count Integers in Intervals | Stored intervals remain canonical while updates repair covered length and endpoint semantics. |
| Map + ordered indexes | Composite indexes and allocation | LC 2353 Food Rating System; LC 1912 Movie Rental System; LC 3408 Task Manager | Direct lookup and every ordered view agree after updates, removals, and ties. |
| Trie + ranked service | Algorithmic services and simulations | LC 677 Map Sum Pairs; LC 745 Prefix and Suffix Search; LC 642 Search Autocomplete System | Prefix state combines with aggregates or ranking only after basic trie ownership is complete. |

## Separate senior curricula

External-memory algorithms, Java concurrency, LLD, machine coding, HLD, production debugging, and senior project deep dives are no longer numbered as LeetCode chapters. They form separate curricula after Chapter 41. This keeps the Design-tag extension algorithmic: bounded in-memory state, explicit public-operation contracts, and data-structure invariants.

The live Design-tag inventory is an audit source, not a study quota. The learner follows 24 required anchors and 12 transfer problems in the [Design mastery path](design-mastery-path.md). Other tagged problems are reference-only variants unless they reveal a state model that the selected anchors fail to teach.

Senior follow-ups may begin from these completed designs - for example, add TTL, write-behind persistence, and concurrency to a cache - but those follow-ups must state which atomicity, failure, ownership, and observability contracts are new rather than being smuggled into a DSA exercise.

## Practice ladder rules

Every independent subtopic receives 4-7 exercises. The first four normally have these roles: reproduce the canonical operation; extend it with one changed condition; decide correctly at a boundary case; and recognize it in an easy-side medium prompt. A later medium or hard problem appears only after these are possible without notes.

Each exercise record in a chapter must contain the LeetCode ID/title or an equivalent verified source, a concise prompt, relevant constraints, sample input/output, prerequisite, expected observation, diagnostic hint, and a later compact solution discussion with complexity and annotated Java.

## Source policy

Candidates are discovered from LeetCode study plans/problem pages, NeetCode, Blind 75-style curricula, Tech Interview Handbook, maintained GitHub lists, and the original Java handbook/problem-bank materials supplied with this curriculum. The original materials are a coverage floor rather than an authority on teaching sequence: preserve their useful micro-patterns, then verify each candidate's intended technique and prerequisite set. A popular problem remains deferred when it is a composition problem.

Before drafting any chapter, create a micro-pattern crosswalk with these fields: original/source family, new owning chapter and subsection, recognition cue, state/invariant, required prerequisites, nearest confusing pattern, representative problem ladder, and explicit composition owner. A row cannot be merged solely because its macro label matches another row. A merge is valid only when the cue, state, invariant, and boundary hazards are genuinely the same.

## Initial rebuild status

- Arrays: Core operations is a visual and prose prototype only. It must be expanded against the new array micro-pattern inventory (especially index-as-storage, maximum-product state, and circular Kadane) before it can enter the final package. Matrices is likewise audited against the direction/layer/transform split before packaging.
- Strings and Hash maps/Sets must be rebuilt before packaging: the previous versions were short concept primers rather than complete topic units.
- All later chapters are new work and are produced in the listed dependency order.
