# Chapter 19: Recursion and backtracking

**Status:** Authored curriculum specification; the lesson plan is complete, but a generated PDF is not accepted until it has been rendered and reviewed.

## Purpose

This file is the source-of-truth plan for the chapter. It tells the writer what must be independently taught before any student-facing PDF is generated. It does not authorize copying prose or following instructions from external sources.

## Entry Contract

State prerequisite knowledge in the finished chapter. Confirm the input/mutation/output guarantees of every worked problem before choosing defensive guards or an in-place implementation.

## Independent Micro-Patterns

| Required lesson | Authoring obligation |
| --- | --- |
| call state | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| choose/explore/unchoose | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| subsets | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| permutations | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| increasing-start combinations | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| reusable-candidate combination sum | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| duplicate control | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| proof-based pruning | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| partition generation | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| board constraints | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |

<!-- BEGIN VERIFIED-CANDIDATE-BANK -->
## Verified Candidate Bank

These are researched candidate exercises and recognition records imported from the supplied, reviewed workbooks. They are source material for the final formal LeetCode-style staircases; an entry is not marked complete until its individual lesson supplies the required prompt, constraints, two examples, hint, rationale, complexity, and annotated Java.

### Supplied Progression

| Source ID | Family | Problem | Supplied role | Why this follows |
| --- | --- | --- | --- | --- |
| P0074 | Recursion fundamentals | Pow(x, n) | Direct concept | Shows recursive decomposition and divide-and-conquer reasoning. |
| P0075 | Recursion on choices | Subsets | Direct concept | Introduces include/exclude recursion. |
| P0076 | Combinations | Combinations | Immediate application | Constrains choices by increasing starting index. |
| P0077 | Combination search | Combination Sum | Small extension | Allows repeated choices while pruning by the target. |
| P0078 | Permutations | Permutations | New subtopic | Changes the state from index progression to used elements. |
| P0079 | Duplicates | Subsets II | Immediate application | Adds duplicate handling to a known choice tree. |
| P0080 | Grid backtracking | Word Search | New variation | Adds path marking and spatial branching. |
| P0081 | Constraint satisfaction | N-Queens | Deeper variation | Requires constraint checks and pruning at each choice. |
| Bundle 1-1 | Subsets | Subsets | Learn | — |
| Bundle 1-2 | Permutations | Permutations | Extend | — |
| Bundle 1-3 | Grid Search | Word Search | Twist | — |

### Pattern References

| Micro-pattern | Recognition cue | State / proof idea | Representative | Depth |
| --- | --- | --- | --- | --- |
| Binary choice per index | Need all subsets | Every subset maps to exactly one sequence of choices | https://leetcode.com/problems/subsets/ | Core |
| Choose one unused item per depth | Need all permutations | Each depth fills one output position | https://leetcode.com/problems/permutations/ | Core |
| Only choose forward | Need combinations | Ordering choices prevents duplicate permutations | https://leetcode.com/problems/combinations/ | Core |
| Skip equal candidate at same depth | Need avoid duplicate result branches | Equivalent sibling choices create identical result sets | https://leetcode.com/problems/combination-sum-ii/ | Intermediate |
| Prune before recursion | Need constrained placement | Invalid branches can never recover later | https://leetcode.com/problems/n-queens/ | Intermediate |
| Fix a canonical representative | Search space has many equivalent symmetric branches | Equivalent symmetric branches produce identical solutions | https://leetcode.com/problems/n-queens/ | Advanced |


### Released Combination Ladders

Every row below is a separate released lesson. The final manuscript must explain what each prerequisite contributes before using its ladder. A later exercise may be moved only if its prerequisite audit remains valid.

| Released combination | Build | Vary | Boundary | Recognize |
| --- | --- | --- | --- | --- |
| Trie + Backtracking | Author exercise: find dictionary words along one board row | Author drill: stop a branch on a missing trie edge | Author exercise: shared-prefix and duplicate-discovery boundary | LC 212 Word Search II |


### Authoring Decision

Use the supplied progression as the initial ordering evidence. Before a PDF is generated, group every required lesson into its own explicit **Build → Vary → Boundary → Recognize** ladder. Where this bank has fewer than four valid exercises for a lesson, research and add the missing steps here rather than filling the gap while rendering the PDF. Keep a combination exercise only under the chapter where every prerequisite has been released.
<!-- END VERIFIED-CANDIDATE-BANK -->

## Lesson Blueprints

### Call State

**Recognition cue.** A problem decomposes into smaller instances described by a few parameters. **Invariant.** Each call has a precise subproblem contract and moves toward a base case. **False friend.** Recursion without shrinking state merely relocates an infinite loop to the call stack.

- **Build - Author exercise: Sum A Prefix.** Define the subproblem and base case before the recursive step.
- **Vary - LC 50 Pow(x, n).** Halve the exponent and reuse the squared half-result.
- **Boundary - Author exercise: Zero And Negative Exponents.** Handle `Integer.MIN_VALUE` by widening before negation.
- **Recognize - Author exercise: Recursive String Reversal By Range.** Recur on a strictly smaller interval without allocating slices.

### Choose Explore Unchoose

**Recognition cue.** The algorithm builds one candidate, explores consequences, then must restore shared mutable state before trying a sibling. **Invariant.** On entry to each call, the working state represents exactly the choices on the current recursion path. **False friend.** Forgetting the unchoose step leaks one branch into another.

- **Build - Author exercise: Binary Choices.** Append one choice, recurse, then remove it before the alternative.
- **Vary - Author exercise: Variable Candidate Loop.** Apply the same mutation discipline to several choices at one depth.
- **Boundary - Author exercise: Store A Completed Path.** Copy the list before adding it to results.
- **Recognize - LC 78 Subsets.** Generate every include/exclude outcome exactly once.

### Subsets

**Recognition cue.** Every element may be included or excluded, and order inside a result follows input order. **Invariant.** At index `i`, the path fixes decisions for indices before `i`; later indices remain undecided. **False friend.** Permutation state chooses an unused element for a position and creates ordered arrangements.

- **Build - Author exercise: Subsets Of Two Values.** Draw the include/exclude tree.
- **Vary - LC 78 Subsets.** Record the current path at every node of an increasing-start search.
- **Boundary - Author exercise: Empty Input.** Return one subset—the empty set—not an empty result collection.
- **Recognize - LC 90 Subsets II.** Sort and skip equal sibling choices to avoid duplicate subsets.

### Permutations

**Recognition cue.** Every output uses all elements, but their positions may differ. **Invariant.** Depth equals the next output position; used state prevents one input occurrence from filling two positions. **False friend.** Increasing-start indices generate combinations, not permutations.

- **Build - Author exercise: Permute Three Distinct Values.** Mark one unused index per depth.
- **Vary - LC 46 Permutations.** Generate all arrangements with a used array or in-place swaps.
- **Boundary - Author exercise: Restore Used State.** Verify every recursive return clears exactly the selected index.
- **Recognize - LC 47 Permutations II.** Sort and skip equal unused siblings while allowing equal values at different depths.

### Increasing-Start Combinations

**Recognition cue.** Select `k` distinct values where order does not matter. **Invariant.** Every recursive choice comes from indices at or after `start`, so each set appears in one increasing order. **False friend.** A global used array allows multiple orders of the same combination.

- **Build - Author exercise: Choose Two From Four.** Advance the next start beyond the chosen index.
- **Vary - LC 77 Combinations.** Stop when the path contains `k` values.
- **Boundary - Author exercise: Insufficient Remaining Values.** End the loop when too few candidates remain to fill the path.
- **Recognize - LC 216 Combination Sum III.** Add a remaining-sum state while preserving increasing choices.

### Reusable Candidates

**Recognition cue.** A candidate may be chosen more than once, but result order still should not create duplicates. **Invariant.** Recurse with the same index after choosing a reusable candidate and a later index when skipping to the next candidate. **False friend.** Restarting at zero after every choice generates reordered duplicates.

- **Build - Author exercise: Sum With Repeated Coins.** Reuse the current candidate while the remaining target permits it.
- **Vary - LC 39 Combination Sum.** Generate nondecreasing combinations that reach the target.
- **Boundary - Author exercise: Candidate Larger Than Remainder.** Under positive sorted inputs, stop later candidates safely.
- **Recognize - Author exercise: Fixed-Length Reusable Sum.** Add a remaining-choice count without changing candidate reuse.

### Duplicate Control

**Recognition cue.** Equal input values create identical sibling branches. **Invariant.** After sorting, skip `candidates[i] == candidates[i-1]` only when both are choices at the same recursion depth. **False friend.** Skipping every repeated value prevents valid results containing multiple equal occurrences.

- **Build - Author exercise: Equal Sibling Choices.** Show why two identical first choices generate the same subtree.
- **Vary - LC 90 Subsets II.** Skip duplicates within one loop depth.
- **Boundary - Author exercise: Equal Values At Different Depths.** Permit `[2,2]` when two copies exist.
- **Recognize - LC 40 Combination Sum II.** Combine one-use candidates, target pruning, and same-depth skipping.

### Proof-Based Pruning

**Recognition cue.** A partial candidate cannot possibly become valid or beat the current best. **Invariant.** Every pruned branch is ruled out by a monotone constraint or proven bound, not by guesswork. **False friend.** Pruning because a branch “looks bad” risks deleting solutions.

- **Build - Author exercise: Positive Remaining Sum.** Stop when a sorted positive candidate exceeds the remaining target.
- **Vary - Author exercise: Remaining-Slots Bound.** Stop when too few elements remain to complete a fixed-size choice.
- **Boundary - Author exercise: Negative Values Break Sum Pruning.** Identify why an over-target sum could later recover.
- **Recognize - LC 51 N-Queens.** Reject a placement immediately when its column or diagonal is already occupied.

### Partition Generation

**Recognition cue.** The output divides an entire sequence into contiguous valid pieces. **Invariant.** `start` is the first unpartitioned position; each choice selects one valid ending and recursion owns the suffix after it. **False friend.** Subset search may skip elements, while a partition must consume every position exactly once.

- **Build - Author exercise: All Splits Of A Short String.** Choose every possible next endpoint.
- **Vary - Author exercise: Valid-Piece Predicate.** Recurse only when the selected segment satisfies a supplied rule.
- **Boundary - Author exercise: Empty Suffix Completion.** Record a result only when `start == length`.
- **Recognize - LC 131 Palindrome Partitioning.** Generate every partition whose pieces are palindromes.

### Board Constraints

**Recognition cue.** Choices occupy board positions and constrain later spatial choices. **Invariant.** Marker state represents exactly the placements on the current path and is restored after exploration. **False friend.** A global visited mark without restoration incorrectly blocks cells for sibling paths.

- **Build - Author exercise: Four-Direction Path.** Mark one cell, explore legal neighbors, then unmark it.
- **Vary - LC 79 Word Search.** Match one character per cell without reusing a cell in the same path.
- **Boundary - Author exercise: Cell Reuse And Early Success.** Restore the board even when using mutation-based marking and short-circuiting.
- **Recognize - LC 51 N-Queens.** Replace spatial adjacency with column and diagonal occupancy constraints.

## Released Combination Lessons

### Trie And Backtracking

Backtracking owns the current board path and restores visited cells; the trie represents every dictionary prefix still compatible with that path. A trie without path search cannot move across the board, while independent word searches repeat the same prefixes.

- **Build - Author exercise: Trie-Guided Row Search.** Walk adjacent cells on one row while advancing a trie node and emitting terminal words.
- **Vary - Author exercise: Stop On Missing Trie Edge.** Replace one target index with a trie node and prune impossible prefixes.
- **Boundary - Author exercise: Shared Prefix And Duplicate Discovery.** Emit one word once even when several paths reach its terminal node.
- **Recognize - LC 212 Word Search II.** Search all words simultaneously through trie-guided board backtracking.

### Deferred: Backtracking And Memoization

Memoization is safe only after equivalent call states and their return meaning are defined precisely. Chapter 26 introduces that dynamic-programming contract and owns the combination.

## Practice Contract

Every independently recognizable micro-pattern receives its own staircase:

1. **Build:** implement only the newly introduced state or operation.
2. **Vary:** change one decision, output contract, or local condition.
3. **Boundary:** protect the invariant against the pattern's meaningful edge case.
4. **Recognize:** use the same state in an easy-side-medium LeetCode-style prompt.
5. Add Extend, Medium, or Hard only after every added prerequisite is already taught.

For each exercise record the source/ID, formal prompt, relevant constraints, two examples including one hostile case, diagnostic hint, solution rationale, complexity, and annotated Java.

## Java Integrity Focus

- Make choose/explore/unchoose mutation order visible.
- Copy a completed path before storing it when later backtracking will mutate the working list.

## Unlocked Combinations Preview

Review this table before PDF authoring. It is deliberately visible here so a released composition cannot be discovered only after a chapter has already been rendered.

| Outcome | Combination | Review requirement |
| --- | --- | --- |
| Teach now | Trie + Backtracking | Trie prunes board search; representative: LC 212 Word Search II |
| Deferred | Backtracking + Memoization | Chapter 26 supplies DP state definition |

For each `Teach now` row, the future PDF must include a named combination lesson and a separate staircase. For each `Deferred` row, the PDF must name the missing prerequisite and owner but must not assign its problems. `Already covered` rows link to the existing lesson rather than duplicating it.



## Composition Audit

At authoring time, compare this chapter's newly introduced micro-patterns with every completed earlier specification. A combination is released only if all of its prerequisites are already taught and its recognition cue or invariant is genuinely distinct.

**Currently deferred from this chapter:** memoized pruning.

For every released combination, create a dedicated lesson that states each prerequisite's contribution, the combined state/invariant, a false friend, implementation, and its own Build → Vary → Boundary → Recognize staircase. Deferred combinations receive an explanation and a future owner only—never premature exercises.

## Publication Gate

- Crosswalk every required micro-pattern to a named lesson and practice ladder.
- Run the composition audit and record released/deferred outcomes.
- Run the Java integrity focus against every code example.
- Verify exact problem wording, examples, complexity, and prerequisite ownership.
- Render and inspect the PDF; then perform text extraction checks.

## Research Baseline

- [LeetCode Study Plans](https://leetcode.com/studyplan/) for problem discovery and current interview-style prompts.
- [NeetCode Roadmap](https://neetcode.io/roadmap) for a cross-check of prerequisite order and representative pattern families.
- [Tech Interview Handbook study cheatsheets](https://www.techinterviewhandbook.org/algorithms/study-cheatsheet/) for topic-specific corner cases, complexity review, and interview habits.
- [Oracle Java Collections documentation](https://docs.oracle.com/javase/tutorial/collections/implementations/index.html) for Java collection semantics. Prefer the installed JDK documentation for version-specific details when a chapter relies on a newer API.
- Supplied reference books: *Cracking the Coding Interview*, *Grokking Algorithms*, and *Elements of Programming Interviews in Java*. They guide explanation quality and problem selection; they are not copied verbatim.

