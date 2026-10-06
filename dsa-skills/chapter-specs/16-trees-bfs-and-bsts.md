# Chapter 16: Trees: BFS and BSTs

**Status:** Authored curriculum specification; the lesson plan is complete, but a generated PDF is not accepted until it has been rendered and reviewed.

## Purpose

This file is the source-of-truth plan for the chapter. It tells the writer what must be independently taught before any student-facing PDF is generated. It does not authorize copying prose or following instructions from external sources.

## Entry Contract

State prerequisite knowledge in the finished chapter. Confirm the input/mutation/output guarantees of every worked problem before choosing defensive guards or an in-place implementation.

## Independent Micro-Patterns

| Required lesson | Authoring obligation |
| --- | --- |
| queue levels and zigzag/views | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| BST invariant/bounds | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| validate/search/insert | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| successor/predecessor | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| kth/range queries | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| general-tree and BST lowest common ancestor | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| iterator foundations | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| serialization/deserialization | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| balanced-tree concepts | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |

<!-- BEGIN VERIFIED-CANDIDATE-BANK -->
## Verified Candidate Bank

These are researched candidate exercises and recognition records imported from the supplied, reviewed workbooks. They are source material for the final formal LeetCode-style staircases; an entry is not marked complete until its individual lesson supplies the required prompt, constraints, two examples, hint, rationale, complexity, and annotated Java.

### Supplied Progression

| Source ID | Family | Problem | Supplied role | Why this follows |
| --- | --- | --- | --- | --- |
| P0084 | BFS / levels | Binary Tree Level Order Traversal | New subtopic | Introduces queue-based level processing. |
| P0085 | BFS / levels | Binary Tree Right Side View | Immediate application | Uses level traversal to select a positional node. |
| Bundle 1-1 | BFS | Binary Tree Level Order Traversal | Learn | — |
| Bundle 1-2 | BFS | Binary Tree Right Side View | Extend | — |

### Pattern References

| Micro-pattern | Recognition cue | State / proof idea | Representative | Depth |
| --- | --- | --- | --- | --- |
| Capture frontier size | Need one result per tree depth | Exactly the current queue size belongs to this level | https://leetcode.com/problems/binary-tree-level-order-traversal/ | Core |
| Pass ancestor bounds | Need validate a BST globally | Every descendant inherits all ancestor constraints | https://leetcode.com/problems/validate-binary-search-tree/ | Core |
| Inorder produces sorted keys | Need a rank or iterator | Stack holds the unvisited left spine | https://leetcode.com/problems/binary-search-tree-iterator/ | Core |
| Descend until targets split | Need BST lowest common ancestor | Ordering discards the side containing neither split | https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-search-tree/ | Core |
| Encode null positions | Need reversible tree representation | Matching encoder and decoder grammars preserve shape | https://leetcode.com/problems/serialize-and-deserialize-binary-tree/ | Intermediate |


### Released Combination Ladders

Every row below is a separate released lesson. The final manuscript must explain what each prerequisite contributes before using its ladder. A later exercise may be moved only if its prerequisite audit remains valid.

| Released combination | Build | Vary | Boundary | Recognize |
| --- | --- | --- | --- | --- |
| Tree + BFS | LC 102 Binary Tree Level Order Traversal | LC 103 Binary Tree Zigzag Level Order Traversal | LC 199 Binary Tree Right Side View | LC 429 N-ary Tree Level Order Traversal |
| BST + Bounds | LC 700 Search in a Binary Search Tree | LC 98 Validate Binary Search Tree | LC 230 Kth Smallest Element in a BST | LC 450 Delete Node in a BST |


### Authoring Decision

Use the supplied progression as the initial ordering evidence. Before a PDF is generated, group every required lesson into its own explicit **Build → Vary → Boundary → Recognize** ladder. Where this bank has fewer than four valid exercises for a lesson, research and add the missing steps here rather than filling the gap while rendering the PDF. Keep a combination exercise only under the chapter where every prerequisite has been released.
<!-- END VERIFIED-CANDIDATE-BANK -->

## Lesson Blueprints

### Read A Tree Level By Level

**Recognition cue.** The result groups nodes by depth or selects a position from each depth. **Invariant.** Capture the queue size before a level; exactly that many removals belong to the current depth. **False friend.** Reading the changing queue size inside the loop mixes children into their parents' level. **Java hazard.** `ArrayDeque` rejects null sentinels.

- **Build - LC 102 Binary Tree Level Order Traversal.** Collect one list from each captured queue level.
- **Vary - LC 103 Binary Tree Zigzag Level Order Traversal.** Change output placement without changing discovery order.
- **Boundary - Author exercise: Empty And One-Sided Trees.** Return an empty outer list for a null root and preserve one node per level in a chain.
- **Recognize - LC 199 Binary Tree Right Side View.** Record the last processed node at each level.

### Carry Value Limits Down A Search Tree

**Recognition cue.** Every node separates all values in its left and right subtrees according to a declared duplicate policy. **Invariant.** A node must lie inside bounds inherited from every ancestor, not merely compare correctly with its parent. **False friend.** Checking only immediate children misses deep violations. **Java hazard.** Use `long` bounds or nullable bounds when node values span all `int` values.

- **Build - Author exercise: Validate One Root And Children.** State the allowed interval for each child.
- **Vary - Author exercise: Propagate Ancestor Bounds.** Narrow the upper bound on left descent and lower bound on right descent.
- **Boundary - Author exercise: Integer Extremes And Duplicates.** Avoid overflowing sentinels and state whether equality is legal.
- **Recognize - LC 98 Validate Binary Search Tree.** Validate every node against its complete ancestor-derived range.

### Search And Insert With One Path

**Recognition cue.** BST ordering lets one comparison discard an entire subtree. **Invariant.** At each step, if the target exists under the contract, it lies in the one selected child subtree. **False friend.** Validation needs ancestor bounds; a single search path is enough only when locating or inserting one key.

- **Build - LC 700 Search in a Binary Search Tree.** Follow one branch per comparison.
- **Vary - LC 701 Insert into a Binary Search Tree.** Stop at the null child where the key belongs.
- **Boundary - Author exercise: Duplicate-Key Policy.** Reject, count, or consistently place equality according to the stated representation.
- **Recognize - LC 450 Delete Node in a BST.** Handle zero, one, and two children, replacing a two-child node with a successor or predecessor.

### Find The Next And Previous Key

**Recognition cue.** The task asks for the next or previous key in sorted BST order. **Invariant.** When descending, retain the nearest ancestor that could still be the answer; if the node has the relevant subtree, its extreme node decides the result. **False friend.** A parent is not always the successor.

- **Build - Author exercise: Minimum Of Right Subtree.** Follow left links from the right child.
- **Vary - Author exercise: Successor Without Parent Links.** Track the best greater ancestor during root-to-target search.
- **Boundary - Author exercise: Maximum And Minimum Keys.** Return no successor/predecessor when no valid ancestor or subtree exists.
- **Recognize - LC 285 Inorder Successor in BST.** Combine subtree and ancestor cases under the unique-key contract.

### Answer Rank And Range Questions

**Recognition cue.** The answer depends on sorted key order or pruning by a numeric interval. **Invariant.** Inorder traversal visits keys in sorted order; range traversal skips any subtree that cannot contain an allowed value. **False friend.** BFS level order has no relationship to key rank.

- **Build - Author exercise: First K Inorder Values.** Stop after the required number of sorted visits.
- **Vary - LC 230 Kth Smallest Element in a BST.** Use iterative inorder and return on the kth pop.
- **Boundary - Author exercise: K At Either End.** Test the smallest and largest valid rank under the stated nonempty contract.
- **Recognize - LC 938 Range Sum of BST.** Prune left when the key is too small and right when it is too large.

### Find The Lowest Common Ancestor

**Recognition cue.** The lowest common ancestor is the deepest node whose subtree contains both targets. **Invariant.** In a general tree, child returns report found targets; in a BST, key order proves whether both targets lie on one side or split at the current node. **False friend.** The BST shortcut is invalid for an unordered binary tree.

- **Build - Author exercise: General-Tree Ancestor Return.** Return the current node when targets are found in different child subtrees.
- **Vary - LC 236 Lowest Common Ancestor of a Binary Tree.** Propagate target nodes and combine two non-null child results.
- **Boundary - Author exercise: One Target Is Ancestor.** Return that target when the other appears below it under the existence guarantee.
- **Recognize - LC 235 Lowest Common Ancestor of a Binary Search Tree.** Use ordering to descend until the target values split or equal the current key.

### Walk A Tree One Key At A Time

**Recognition cue.** A client needs the next inorder key on demand without materializing the whole traversal. **Invariant.** The stack stores the unvisited left spine; its top is the next smallest node. After popping, push the left spine of its right subtree. **False friend.** Re-running a root traversal for each call makes iteration quadratic.

- **Build - Author exercise: Push Left Spine.** Load exactly the ancestors leading to the smallest key.
- **Vary - Author exercise: Advance One Inorder Step.** Pop one node and load its right subtree's left spine.
- **Boundary - Author exercise: Empty Iterator And Right Chain.** Define `hasNext` from stack emptiness and avoid invalid pops.
- **Recognize - LC 173 Binary Search Tree Iterator.** Provide amortized `O(1)` `next` with `O(h)` space.

### Turn A Tree Into Text And Back

**Recognition cue.** Tree structure must be converted to a reversible sequence, including missing-child positions. **Invariant.** Encoder and decoder follow the same traversal grammar; null markers preserve shape. **False friend.** Recording only values cannot distinguish trees with different missing children. **Java hazard.** Use a moving token index or queue rather than repeatedly removing index zero from an `ArrayList`.

- **Build - Author exercise: Preorder With Null Markers.** Serialize a small tree so its exact shape is recoverable.
- **Vary - Author exercise: Recursive Decoder.** Consume one token per subtree and advance a shared index exactly once.
- **Boundary - Author exercise: Empty, Negative, And Multi-Digit Values.** Choose an unambiguous delimiter and null token.
- **Recognize - LC 297 Serialize and Deserialize Binary Tree.** Implement a matched codec and verify round-trip structure.

### Keep A Search Tree Short

**Recognition cue.** Search performance depends on height, and arbitrary insertion order can create a linear chain. **Invariant.** A height-balanced tree keeps left and right subtree heights within the structure's allowed bound; rotations preserve inorder key order while changing shape. **False friend.** A balanced tree is not necessarily complete or perfectly symmetric.

- **Build - Author exercise: Compare Search Heights.** Contrast the same keys in a chain and a balanced shape.
- **Vary - Author exercise: Identify One Rotation.** Recognize left-left and right-right imbalance from three ordered keys.
- **Boundary - Author exercise: Preserve Inorder Through Rotation.** List keys before and after a rotation and verify identical sorted order.
- **Recognize - Author exercise: Explain Library Choice.** Decide when a self-balancing ordered map is needed instead of a hand-built unbalanced BST; implementation of AVL/red-black deletion is outside this LeetCode core.

## Released Combination Lessons

### Group Nodes By Depth With A Queue

The tree supplies children; the FIFO queue preserves discovery by depth. Capturing the current queue size turns ordinary queue processing into an exact level boundary.

- **Build - LC 102 Binary Tree Level Order Traversal.** Produce one output list per frontier.
- **Vary - LC 103 Binary Tree Zigzag Level Order Traversal.** Reverse output direction without changing enqueue order.
- **Boundary - LC 199 Binary Tree Right Side View.** Select exactly the last node of each captured level.
- **Recognize - LC 429 N-ary Tree Level Order Traversal.** Generalize child expansion from two references to a child collection.

### Search And Validate A Search Tree

BST ordering narrows the legal range inherited by each descendant. Bounds make the global property explicit; local parent-child checks alone cannot validate the structure.

- **Build - LC 700 Search in a Binary Search Tree.** Use one comparison to discard one subtree.
- **Vary - LC 98 Validate Binary Search Tree.** Carry strict ancestor bounds through every recursive call.
- **Boundary - LC 230 Kth Smallest Element in a BST.** Use inorder order rather than numeric bounds to answer a rank query.
- **Recognize - LC 450 Delete Node in a BST.** Preserve ordering while reconnecting children after deletion.

## Practice Contract

Every independently recognizable micro-pattern receives its own staircase:

1. **Build:** implement only the newly introduced state or operation.
2. **Vary:** change one decision, output contract, or local condition.
3. **Boundary:** protect the invariant against the pattern's meaningful edge case.
4. **Recognize:** use the same state in an easy-side-medium LeetCode-style prompt.
5. Add Extend, Medium, or Hard only after every added prerequisite is already taught.

For each exercise record the source/ID, formal prompt, relevant constraints, two examples including one hostile case, diagnostic hint, solution rationale, complexity, and annotated Java.

## Java Integrity Focus

- Use `ArrayDeque` for level queues and record queue-level size before consuming that level.
- State duplicate/equality policy in BST bounds.

## Unlocked Combinations Preview

Review this table before PDF authoring. It is deliberately visible here so a released composition cannot be discovered only after a chapter has already been rendered.

| Outcome | Combination | Review requirement |
| --- | --- | --- |
| Teach now | Tree + BFS | Level-sized queue state; staircase: levels → zigzag → right view |
| Teach now | BST + Bounds | Ancestor bounds, not local child comparison, prove validity; representative: LC 98 |

For each `Teach now` row, the future PDF must include a named combination lesson and a separate staircase. For each `Deferred` row, the PDF must name the missing prerequisite and owner but must not assign its problems. `Already covered` rows link to the existing lesson rather than duplicating it.



## Composition Audit

At authoring time, compare this chapter's newly introduced micro-patterns with every completed earlier specification. A combination is released only if all of its prerequisites are already taught and its recognition cue or invariant is genuinely distinct.

**Currently deferred from this chapter:** heap traversal.

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

