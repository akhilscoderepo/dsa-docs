# Chapter 15: Trees: DFS

**Status:** Authored curriculum specification; the lesson plan is complete, but a generated PDF is not accepted until it has been rendered and reviewed.

## Purpose

This file is the source-of-truth plan for the chapter. It tells the writer what must be independently taught before any student-facing PDF is generated. It does not authorize copying prose or following instructions from external sources.

## Entry Contract

State prerequisite knowledge in the finished chapter. Confirm the input/mutation/output guarantees of every worked problem before choosing defensive guards or an in-place implementation.

## Independent Micro-Patterns

| Required lesson | Authoring obligation |
| --- | --- |
| binary/N-ary tree representation | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| preorder/inorder/postorder recursion | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| iterative DFS | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| depth/height/path state | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| diameter and subtree return values | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| balance sentinels | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| tree reconstruction from traversals | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| Morris traversal | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| quadtree construction | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |

<!-- BEGIN VERIFIED-CANDIDATE-BANK -->
## Verified Candidate Bank

These are researched candidate exercises and recognition records imported from the supplied, reviewed workbooks. They are source material for the final formal LeetCode-style staircases; an entry is not marked complete until its individual lesson supplies the required prompt, constraints, two examples, hint, rationale, complexity, and annotated Java.

### Supplied Progression

| Source ID | Family | Problem | Supplied role | Why this follows |
| --- | --- | --- | --- | --- |
| P0082 | DFS fundamentals | Maximum Depth of Binary Tree | Direct concept | Defines a recursive return value from children. |
| P0083 | DFS traversals | Binary Tree Preorder Traversal | Immediate application | Makes traversal order explicit. |
| P0086 | Tree state | Diameter of Binary Tree | New variation | Combines child-returned heights with a global answer. |
| P0087 | Path problems | Path Sum II | New variation | Carries path state down recursion and backtracks it. |
| P0088 | Path problems | Path Sum III | Combination | Combines tree traversal with prefix-sum reasoning. |
| P0089 | Lowest common ancestor | Lowest Common Ancestor of a Binary Tree | New subtopic | Combines subtree results to identify a shared ancestor. |
| P0090 | Construction | Construct Binary Tree from Preorder and Inorder Traversal | Combination | Uses traversal relationships plus recursive construction. |
| P0091 | Serialization | Serialize and Deserialize Binary Tree | Advanced application | Requires a reversible representation of recursive structure. |
| P0092 | Advanced path state | Binary Tree Maximum Path Sum | Deeper variation | Separates the value returned upward from the global path answer. |
| Bundle 1-1 | DFS | Maximum Depth of Binary Tree | Learn | — |
| Bundle 1-2 | DFS | Invert Binary Tree | Extend | — |
| Bundle 1-3 | DFS | Diameter of Binary Tree | Twist | — |
| Bundle 1-3 | Tree DP | Binary Tree Maximum Path Sum | Twist | — |
| Bundle 2-7 | Tree DP | House Robber III | Mixed | — |

### Pattern References

| Micro-pattern | Recognition cue | State / proof idea | Representative | Depth |
| --- | --- | --- | --- | --- |
| Children -> parent | Need subtree aggregate | Parent state depends on completed child states | https://leetcode.com/problems/maximum-depth-of-binary-tree/ | Core |
| Action position around child calls | Need preorder, inorder, or postorder | The action's position defines traversal order | https://leetcode.com/problems/binary-tree-inorder-traversal/ | Core |
| Downward path state + backtrack | Need root-to-leaf paths | Mutable path represents exactly the active recursion chain | https://leetcode.com/problems/path-sum-ii/ | Core |
| Map value -> inorder index | Need construct tree from traversals | Traversal orders uniquely partition subtrees | https://leetcode.com/problems/construct-binary-tree-from-preorder-and-inorder-traversal/ | Intermediate |
| Return best downward path | Need path may turn at a node | Parent can take only one branch, global path may take both | https://leetcode.com/problems/binary-tree-maximum-path-sum/ | Advanced |
| Height or failure sentinel | Need balance plus height | A failed descendant propagates without repeated height scans | https://leetcode.com/problems/balanced-binary-tree/ | Core |
| Temporary predecessor thread | Need traversal with constant auxiliary space | Every temporary link is detected and restored | https://leetcode.com/problems/binary-tree-inorder-traversal/ | Advanced |
| Uniform region or four children | Need recursive spatial compression | Each call represents exactly one square region | https://leetcode.com/problems/construct-quad-tree/ | Intermediate |


### Released Combination Ladders

Every row below is a separate released lesson. The final manuscript must explain what each prerequisite contributes before using its ladder. A later exercise may be moved only if its prerequisite audit remains valid.

| Released combination | Build | Vary | Boundary | Recognize |
| --- | --- | --- | --- | --- |
| Tree + DFS Return State | LC 104 Maximum Depth of Binary Tree | LC 543 Diameter of Binary Tree | LC 110 Balanced Binary Tree | LC 124 Binary Tree Maximum Path Sum |


### Authoring Decision

Use the supplied progression as the initial ordering evidence. Before a PDF is generated, group every required lesson into its own explicit **Build → Vary → Boundary → Recognize** ladder. Where this bank has fewer than four valid exercises for a lesson, research and add the missing steps here rather than filling the gap while rendering the PDF. Keep a combination exercise only under the chapter where every prerequisite has been released.
<!-- END VERIFIED-CANDIDATE-BANK -->

## Lesson Blueprints

### Tree Representation

**Recognition cue.** Data has one root and recursively nested children rather than one linear successor. **Invariant.** Each recursive call owns one node's subtree; `null` represents an empty binary subtree, while an N-ary node owns a child collection. **False friend.** A general graph may contain cycles or multiple parents; a tree traversal does not need visited state under the tree contract.

- **Build - Author exercise: Construct A Three-Node Tree.** Connect one root to left and right children and identify each empty subtree.
- **Vary - Author exercise: Count N-Ary Children.** Traverse a supplied child list without assuming two positions.
- **Boundary - Author exercise: Empty And Single-Node Trees.** Define the result of each operation at `null` before writing recursion.
- **Recognize - LC 559 Maximum Depth of N-ary Tree.** Generalize the child-to-parent depth recurrence.

### Recursive Traversal Orders

**Recognition cue.** Every node must be processed once, and the relative position of the node action and child calls determines meaning. **Invariant.** Preorder acts before children, inorder between binary children, and postorder after children. **False friend.** These are not interchangeable labels; reconstruction and sorted BST traversal depend on order.

- **Build - LC 144 Binary Tree Preorder Traversal.** Record node, then left and right subtrees.
- **Vary - LC 94 Binary Tree Inorder Traversal.** Move the action between the two child calls.
- **Boundary - Author exercise: Empty And One-Sided Trees.** Preserve order when one child is null.
- **Recognize - LC 145 Binary Tree Postorder Traversal.** Delay the node action until both subtree calls return.

### Iterative DFS

**Recognition cue.** Depth-first order is required without relying on the language call stack. **Invariant.** The explicit stack contains subtrees or frames still to be processed. **False friend.** Pushing left before right produces right-first preorder because the stack is LIFO.

- **Build - Author exercise: Iterative Preorder.** Push right before left so the left child is processed next.
- **Vary - Author exercise: Iterative Inorder.** Push the entire left spine, then visit and move right.
- **Boundary - Author exercise: Deep Skewed Tree.** Avoid recursive stack overflow and handle an initially null root.
- **Recognize - LC 145 Binary Tree Postorder Traversal.** Use explicit visit state or a controlled reverse-preorder construction.

### Depth And Path State

**Recognition cue.** A result depends on distance from the root, height below a node, or the values along the current root-to-node path. **Invariant.** Downward state is extended before a child call and restored afterward; upward state summarizes a completed subtree. **False friend.** A path list shared across recursion requires backtracking, while an integer depth passed by value does not.

- **Build - LC 104 Maximum Depth of Binary Tree.** Return one plus the larger child depth.
- **Vary - LC 112 Path Sum.** Pass the remaining target down one root-to-leaf path.
- **Boundary - Author exercise: Leaf Versus Internal Match.** Accept a target sum only where the problem requires a leaf.
- **Recognize - LC 113 Path Sum II.** Maintain a mutable path and remove the current node after both child calls.

### Diameter And Subtree Returns

**Recognition cue.** The best answer may pass through a node using both children, but the parent can continue through only one child. **Invariant.** Each call returns the best single branch usable by its parent and separately updates the best complete path seen. **False friend.** Returning the full two-branch path upward would fork and cease to be a path.

- **Build - Author exercise: Return Subtree Height.** Compute left and right heights before the parent result.
- **Vary - LC 543 Diameter of Binary Tree.** Update the global or wrapper answer with `leftHeight + rightHeight`.
- **Boundary - Author exercise: Nodes Versus Edges.** State which unit the return value and final diameter use.
- **Recognize - LC 124 Binary Tree Maximum Path Sum.** Return one nonnegative downward gain while allowing the complete answer to use both sides.

### Balance Sentinels

**Recognition cue.** Every subtree needs a normal summary unless a failure below should terminate or propagate immediately. **Invariant.** The helper returns height for a balanced subtree and a distinguished sentinel for an unbalanced one. **False friend.** Recomputing height separately at every node turns a linear solution into quadratic time on a skewed tree.

- **Build - Author exercise: Height Or Failure.** Return `-1` immediately when a child already failed.
- **Vary - Author exercise: Detect Local Imbalance.** Compare child heights only after both are valid.
- **Boundary - Author exercise: Empty Tree Height.** Choose a base height consistent with the balance difference formula.
- **Recognize - LC 110 Balanced Binary Tree.** Combine detection and height calculation in one postorder pass.

### Traversal Reconstruction

**Recognition cue.** Two traversal orders describe one tree with unique values, and one order identifies the root while the other partitions subtrees. **Invariant.** Each recursive call owns matching traversal ranges for exactly one subtree. **False friend.** Preorder alone does not uniquely determine an arbitrary binary tree. **Java hazard.** Map inorder values to indices to avoid repeated linear searches.

- **Build - Author exercise: Split One Root.** Locate the preorder root in inorder and identify left/right sizes.
- **Vary - Author exercise: Reconstruct By Index Ranges.** Pass boundaries instead of copying slices.
- **Boundary - Author exercise: Empty Range And Skewed Tree.** Stop exactly when the owned range is empty.
- **Recognize - LC 105 Construct Binary Tree from Preorder and Inorder Traversal.** Combine the index map with a moving preorder position.

### Morris Traversal

**Recognition cue.** Inorder or preorder traversal is required with `O(1)` auxiliary space and temporary reversible threading is allowed. **Invariant.** A predecessor's null right link temporarily points back to the current node and is restored on the second encounter. **False friend.** Forgetting restoration corrupts the input tree and can create a cycle.

- **Build - Author exercise: Find Inorder Predecessor.** Walk to the rightmost node of the left subtree.
- **Vary - Author exercise: Create And Remove One Thread.** Distinguish first and second arrival at the same node.
- **Boundary - Author exercise: No Left Child And Existing Thread.** Visit directly in the first case and restore in the second.
- **Recognize - LC 94 Binary Tree Inorder Traversal.** Implement Morris inorder and verify the tree is unchanged afterward.

### Quadtree Construction

**Recognition cue.** A square grid region becomes one leaf when uniform; otherwise it divides into four equal quadrants. **Invariant.** Each call owns a precise row/column region and returns the node representing exactly that region. **False friend.** Creating four children before testing uniformity produces unnecessary structure.

- **Build - Author exercise: Uniform Region Test.** Decide whether every cell in one supplied square matches its first cell.
- **Vary - Author exercise: Split Four Quadrants.** Calculate non-overlapping child bounds for an even side length.
- **Boundary - Author exercise: One Cell.** Return a leaf without further subdivision.
- **Recognize - LC 427 Construct Quad Tree.** Recursively compress uniform regions and build internal nodes only when needed.

## Released Combination Lessons

### Tree DFS Returns

The tree supplies recursive subproblems; DFS return state compresses each completed subtree into the fact its parent needs. The central design decision is separating the value returned upward from any complete answer formed at the current node.

- **Build - LC 104 Maximum Depth of Binary Tree.** Return one height from two completed child heights.
- **Vary - LC 543 Diameter of Binary Tree.** Return one branch but evaluate a two-branch answer locally.
- **Boundary - LC 110 Balanced Binary Tree.** Propagate a failure sentinel without recomputing heights.
- **Recognize - LC 124 Binary Tree Maximum Path Sum.** Separate upward gain from a path that may turn through the current node.

### Deferred: Tree And BFS

DFS does not preserve distance layers. Chapter 16 adds the level-sized queue frontier and owns level order, zigzag output, and tree views.

## Practice Contract

Every independently recognizable micro-pattern receives its own staircase:

1. **Build:** implement only the newly introduced state or operation.
2. **Vary:** change one decision, output contract, or local condition.
3. **Boundary:** protect the invariant against the pattern's meaningful edge case.
4. **Recognize:** use the same state in an easy-side-medium LeetCode-style prompt.
5. Add Extend, Medium, or Hard only after every added prerequisite is already taught.

For each exercise record the source/ID, formal prompt, relevant constraints, two examples including one hostile case, diagnostic hint, solution rationale, complexity, and annotated Java.

## Java Integrity Focus

- Return recursion state rather than relying on mutable globals when possible.
- Define the `null`-node base case as part of the traversal contract.

## Unlocked Combinations Preview

Review this table before PDF authoring. It is deliberately visible here so a released composition cannot be discovered only after a chapter has already been rendered.

| Outcome | Combination | Review requirement |
| --- | --- | --- |
| Teach now | Tree + DFS Return State | Subtree facts returned to parent; staircase: depth → diameter → balanced tree |
| Deferred | Tree + BFS | Chapter 16 supplies level-frontier state |

For each `Teach now` row, the future PDF must include a named combination lesson and a separate staircase. For each `Deferred` row, the PDF must name the missing prerequisite and owner but must not assign its problems. `Already covered` rows link to the existing lesson rather than duplicating it.



## Composition Audit

At authoring time, compare this chapter's newly introduced micro-patterns with every completed earlier specification. A combination is released only if all of its prerequisites are already taught and its recognition cue or invariant is genuinely distinct.

**Currently deferred from this chapter:** BFS, BST-specific ordering.

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

