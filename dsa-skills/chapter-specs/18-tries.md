# Chapter 18: Tries

**Status:** Authored curriculum specification; the lesson plan is complete, but a generated PDF is not accepted until it has been rendered and reviewed.

## Purpose

This file is the source-of-truth plan for the chapter. It tells the writer what must be independently taught before any student-facing PDF is generated. It does not authorize copying prose or following instructions from external sources.

## Entry Contract

State prerequisite knowledge in the finished chapter. Confirm the input/mutation/output guarantees of every worked problem before choosing defensive guards or an in-place implementation.

## Independent Micro-Patterns

| Required lesson | Authoring obligation |
| --- | --- |
| prefix nodes | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| insert/search | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| wildcard branching | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| word break/trie search | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| binary tries for maximum XOR | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |

<!-- BEGIN VERIFIED-CANDIDATE-BANK -->
## Verified Candidate Bank

These are researched candidate exercises and recognition records imported from the supplied, reviewed workbooks. They are source material for the final formal LeetCode-style staircases; an entry is not marked complete until its individual lesson supplies the required prompt, constraints, two examples, hint, rationale, complexity, and annotated Java.

### Supplied Progression

| Source ID | Family | Problem | Supplied role | Why this follows |
| --- | --- | --- | --- | --- |
| P0137 | Trie fundamentals | Implement Trie (Prefix Tree) | Direct concept | Builds the prefix data structure. |
| P0138 | Trie search | Design Add and Search Words Data Structure | Immediate application | Adds wildcard search through recursive branching. |
| P0139 | Trie + backtracking | Word Search II | Combination | Uses trie prefixes to prune a grid backtracking search. |
| Bundle 1-1 | Prefix | Implement Trie (Prefix Tree) | Learn | — |
| Bundle 1-2 | Wildcard Search | Design Add and Search Words Data Structure | Extend | — |
| Bundle 1-3 | Search | Word Search II | Twist | — |
| Bundle 2-10 | Search | Word Search II | Mixed | — |

### Pattern References

| Micro-pattern | Recognition cue | State / proof idea | Representative | Depth |
| --- | --- | --- | --- | --- |
| Follow character edges | Prefix existence/search | A prefix is literally a path | https://leetcode.com/problems/implement-trie-prefix-tree/ | Core |
| Branch only at wildcard | Wildcard character search | Only wildcard positions introduce branching | https://leetcode.com/problems/design-add-and-search-words-data-structure/ | Intermediate |
| Prune impossible prefixes | Many word searches share prefixes | All words sharing a prefix reuse the same prefix traversal | https://leetcode.com/problems/word-search-ii/ | Advanced |
| Choose bit branch greedily | Need binary values by bit prefix | Opposite bit maximizes the highest differing bit | https://leetcode.com/problems/maximum-xor-of-two-numbers-in-an-array/ | Advanced |


### Released Combination Ladders

Every row below is a separate released lesson. The final manuscript must explain what each prerequisite contributes before using its ladder. A later exercise may be moved only if its prerequisite audit remains valid.

| Released combination | Build | Vary | Boundary | Recognize |
| --- | --- | --- | --- | --- |
| Trie + String Search | LC 208 Implement Trie | LC 211 Design Add and Search Words | LC 648 Replace Words | LC 720 Longest Word in Dictionary |


### Authoring Decision

Use the supplied progression as the initial ordering evidence. Before a PDF is generated, group every required lesson into its own explicit **Build → Vary → Boundary → Recognize** ladder. Where this bank has fewer than four valid exercises for a lesson, research and add the missing steps here rather than filling the gap while rendering the PDF. Keep a combination exercise only under the chapter where every prerequisite has been released.
<!-- END VERIFIED-CANDIDATE-BANK -->

## Lesson Blueprints

### Store Words By Shared Prefix

**Recognition cue.** Many stored strings share prefixes and queries repeatedly ask whether a prefix exists. **Invariant.** The path from the root spells exactly one prefix; terminal state is separate from path existence. **False friend.** A hash set answers whole-word membership but cannot directly represent all prefixes.

- **Build - Author exercise: Store Shared Prefixes.** Insert `car` and `cat` and identify which nodes are shared.
- **Vary - Author exercise: Prefix Count.** Maintain how many inserted words pass through each node.
- **Boundary - Author exercise: Empty Word And Prefix-Only Node.** Distinguish the root terminal flag from a node that merely has children.
- **Recognize - LC 208 Implement Trie.** Support exact word and prefix queries from the same paths.

### Insert And Look Up Words

**Recognition cue.** Operations consume one character at a time and either create a missing edge or fail when an edge is absent. **Invariant.** After processing `i` characters, the current node represents `word[0..i]`. **Java hazard.** A 26-slot array is valid only for a lowercase-English contract; otherwise use a map.

- **Build - Author exercise: Insert Lowercase Words.** Create only missing child nodes.
- **Vary - Author exercise: Search Versus StartsWith.** Require a terminal marker only for exact search.
- **Boundary - Author exercise: Word Is Prefix Of Another.** Store `app` and `apple` without confusing their terminal states.
- **Recognize - LC 208 Implement Trie.** Implement the complete API under an explicit character-domain contract.

### Match Words With Wildcards

**Recognition cue.** Most query characters select one trie edge, but a wildcard may match any child. **Invariant.** A recursive call represents all dictionary words consistent with the query prefix consumed so far. **False friend.** Branching at ordinary characters turns a narrow search into unnecessary exhaustive traversal.

- **Build - Author exercise: One Final Wildcard.** Check every child only at the wildcard position.
- **Vary - Author exercise: Multiple Wildcards.** Recurse independently through each viable child and short-circuit on success.
- **Boundary - Author exercise: Wildcard At Root And Missing Length.** Match exactly the query length and require terminal state at the end.
- **Recognize - LC 211 Design Add and Search Words Data Structure.** Combine trie insertion with selective wildcard DFS.

### Cut A String Into Dictionary Words

**Recognition cue.** A string must be segmented into dictionary words, and trie traversal can test every word beginning at a position without constructing substrings. **Invariant.** From a start index, advancing the trie enumerates exactly the dictionary prefixes of the remaining suffix. **False friend.** Plain recursion repeats the same suffix states exponentially; memoization/DP ownership is deferred to Chapter 26.

- **Build - Author exercise: Dictionary Ends From One Index.** Return every end position reachable by a trie word.
- **Vary - Author exercise: One Valid Segmentation On Short Input.** Recurse from terminal trie nodes while keeping the repeated-state risk visible.
- **Boundary - Author exercise: Prefix Exists But Word Does Not.** Branch only at terminal nodes, not every reachable prefix.
- **Recognize - Author exercise: Explain Trie-Based Word Break State.** Define the start-index state and identify why memoization is needed for scale, without introducing DP prematurely.

### Pick The Best XOR Partner

**Recognition cue.** The objective is to maximize XOR, so the highest differing bit dominates all lower bits. **Invariant.** At each bit, prefer the opposite branch when present; the chosen path is lexicographically best in XOR-bit order. **False friend.** A character trie and a binary trie share structure but not edge meaning.

- **Build - Author exercise: Insert Fixed-Width Bits.** Store each integer from the highest considered bit to the lowest.
- **Vary - Author exercise: Best XOR Partner.** Prefer the opposite bit and accumulate the resulting XOR value.
- **Boundary - Author exercise: Equal Values And Sign Policy.** State whether inputs are nonnegative and which bit width is traversed.
- **Recognize - LC 421 Maximum XOR of Two Numbers in an Array.** Query each number against previously inserted or fully stored values.

## Released Combination Lessons

### Look Up Prefixes In A Dictionary

String indexing supplies the next symbol; trie nodes preserve all dictionary candidates sharing the consumed prefix. The combination avoids rescanning unrelated words after the prefix has already ruled them out.

- **Build - LC 208 Implement Trie.** Establish exact and prefix path semantics.
- **Vary - LC 211 Design Add and Search Words Data Structure.** Branch only where the query contains a wildcard.
- **Boundary - LC 648 Replace Words.** Stop at the first terminal prefix and preserve words with no matching root.
- **Recognize - LC 720 Longest Word in Dictionary.** Traverse only words whose every shorter prefix is terminal and apply lexical tie-breaking.

### Deferred: Trie And Backtracking

A trie can prune many simultaneous board-word searches, but board path ownership and choose/explore/unchoose restoration arrive in Chapter 19. That chapter owns Word Search II.

## Practice Contract

Every independently recognizable micro-pattern receives its own staircase:

1. **Build:** implement only the newly introduced state or operation.
2. **Vary:** change one decision, output contract, or local condition.
3. **Boundary:** protect the invariant against the pattern's meaningful edge case.
4. **Recognize:** use the same state in an easy-side-medium LeetCode-style prompt.
5. Add Extend, Medium, or Hard only after every added prerequisite is already taught.

For each exercise record the source/ID, formal prompt, relevant constraints, two examples including one hostile case, diagnostic hint, solution rationale, complexity, and annotated Java.

## Java Integrity Focus

- State node-child representation and character-domain assumption.
- Backtracking through trie children must undo only traversal state, not shared trie structure.

## Unlocked Combinations Preview

Review this table before PDF authoring. It is deliberately visible here so a released composition cannot be discovered only after a chapter has already been rendered.

| Outcome | Combination | Review requirement |
| --- | --- | --- |
| Teach now | Trie + String Search | Prefix-node state narrows candidates; staircase: implement trie → wildcard → word break |
| Deferred | Trie + Backtracking | Chapter 19 supplies choose/explore/unchoose state |

For each `Teach now` row, the future PDF must include a named combination lesson and a separate staircase. For each `Deferred` row, the PDF must name the missing prerequisite and owner but must not assign its problems. `Already covered` rows link to the existing lesson rather than duplicating it.



## Composition Audit

At authoring time, compare this chapter's newly introduced micro-patterns with every completed earlier specification. A combination is released only if all of its prerequisites are already taught and its recognition cue or invariant is genuinely distinct.

**Currently deferred from this chapter:** trie-guided board backtracking.

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

