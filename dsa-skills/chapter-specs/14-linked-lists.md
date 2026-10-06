# Chapter 14: Linked lists

**Status:** Authored curriculum specification; the lesson plan is complete, but a generated PDF is not accepted until it has been rendered and reviewed.

## Purpose

This file is the source-of-truth plan for the chapter. It tells the writer what must be independently taught before any student-facing PDF is generated. It does not authorize copying prose or following instructions from external sources.

## Entry Contract

State prerequisite knowledge in the finished chapter. Confirm the input/mutation/output guarantees of every worked problem before choosing defensive guards or an in-place implementation.

## Independent Micro-Patterns

| Required lesson | Authoring obligation |
| --- | --- |
| node invariants | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| reverse | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| partial/k-group reversal | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| merge | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| dummy heads | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| cycle entry | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| intersection | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| middle nodes | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| fixed-gap kth-from-end | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| multilevel flattening | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |

<!-- BEGIN VERIFIED-CANDIDATE-BANK -->
## Verified Candidate Bank

These are researched candidate exercises and recognition records imported from the supplied, reviewed workbooks. They are source material for the final formal LeetCode-style staircases; an entry is not marked complete until its individual lesson supplies the required prompt, constraints, two examples, hint, rationale, complexity, and annotated Java.

### Supplied Progression

| Source ID | Family | Problem | Supplied role | Why this follows |
| --- | --- | --- | --- | --- |
| P0044 | Pointer fundamentals | Reverse Linked List | Direct concept | Establishes safe pointer rewiring. |
| P0045 | Merge ordered lists | Merge Two Sorted Lists | Immediate application | Reuses pointer movement while exploiting sorted order. |
| P0046 | Fast and slow pointers | Middle of the Linked List | Direct concept | Introduces two speeds for relative-position discovery. |
| P0047 | Fast and slow pointers | Linked List Cycle | Immediate application | Uses the same speed relationship to detect a cycle. |
| P0048 | Fast and slow pointers | Linked List Cycle II | Immediate application | Extends cycle detection to locate the entry. |
| P0049 | Pointer gap | Remove Nth Node From End of List | New variation | Maintains a fixed distance between two pointers. |
| P0050 | Reordering | Reorder List | Combination | Combines midpoint, reversal, and merging. |
| P0051 | Merge sort | Sort List | Combination | Combines linked-list splitting, recursion, and merging. |
| P0052 | Random pointers | Copy List with Random Pointer | New variation | Adds arbitrary references and mapping. |

### Pattern References

| Micro-pattern | Recognition cue | State / proof idea | Representative | Depth |
| --- | --- | --- | --- | --- |
| Save next before redirect | Reverse links | Each original link is redirected exactly once | https://leetcode.com/problems/reverse-linked-list/ | Core |
| 2:1 speed ratio | Find middle | When fast reaches end, slow is midpoint | https://leetcode.com/problems/middle-of-the-linked-list/ | Core |
| Fast catches slow | Cycle detection | Relative speed guarantees collision inside a finite cycle | https://leetcode.com/problems/linked-list-cycle/ | Core |
| Advance fast k steps first | Kth from end | Gap remains k throughout | https://leetcode.com/problems/remove-nth-node-from-end-of-list/ | Core |
| Consume smaller head | Merge sorted lists | Remaining nodes remain sorted | https://leetcode.com/problems/merge-two-sorted-lists/ | Core |
| Transform into two compatible halves | Reorder alternating ends | Reversal converts tail order into required alternating order | https://leetcode.com/problems/reorder-list/ | Intermediate |


### Released Combination Ladders

Every row below is a separate released lesson. The final manuscript must explain what each prerequisite contributes before using its ladder. A later exercise may be moved only if its prerequisite audit remains valid.

| Released combination | Build | Vary | Boundary | Recognize |
| --- | --- | --- | --- | --- |
| Linked List + Hash Map | Author drill: build an original-to-clone map | LC 138 Copy List with Random Pointer | LC 138 null/self/shared-random boundary | Author exercise: clone nodes with two arbitrary reference fields |


### Authoring Decision

Use the supplied progression as the initial ordering evidence. Before a PDF is generated, group every required lesson into its own explicit **Build → Vary → Boundary → Recognize** ladder. Where this bank has fewer than four valid exercises for a lesson, research and add the missing steps here rather than filling the gap while rendering the PDF. Keep a combination exercise only under the chapter where every prerequisite has been released.
<!-- END VERIFIED-CANDIDATE-BANK -->

## Lesson Blueprints

### Follow References Through A List

**Recognition cue.** The structure is defined by references rather than contiguous indices, so mutation changes reachability. **Invariant.** Every unreached node remains reachable from a saved reference, and the returned head owns the intended chain. **False friend.** Array-style random access does not exist; reaching position `i` costs a traversal.

- **Build - Author exercise: Traverse And Count.** Follow `next` references without modifying the list.
- **Vary - Author exercise: Insert After A Node.** Save the old successor before linking the new node.
- **Boundary - Author exercise: Empty And Singleton Lists.** State which references may be null under each operation.
- **Recognize - LC 203 Remove Linked List Elements.** Maintain a valid retained chain while removing matching nodes.

### Reverse A List In One Pass

**Recognition cue.** Every `next` edge must point to the previous node. **Invariant.** `prev` heads the fully reversed prefix, `curr` heads the untouched suffix, and no node is lost between them. **False friend.** Reassigning `curr.next` before saving its old successor disconnects the remaining list.

- **Build - Author exercise: Reverse Three Nodes By Hand.** Record `next`, redirect the edge, then advance both references.
- **Vary - LC 206 Reverse Linked List.** Apply the invariant until the untouched suffix is empty.
- **Boundary - Author exercise: Empty And One Node.** Return the correct head without special pointer rewiring.
- **Recognize - LC 92 Reverse Linked List II.** Reverse only a specified segment and reconnect both boundaries.

### Reverse Blocks Inside A List

**Recognition cue.** Only complete blocks or a bounded sublist should have their edges reversed. **Invariant.** Before reversing, identify the block predecessor, first node, successor after the block, and whether a full block exists. **False friend.** Reversing first and discovering a short final group later makes restoration unnecessarily difficult.

- **Build - Author exercise: Reverse Exactly Two Nodes.** Reconnect a supplied predecessor and successor.
- **Vary - LC 92 Reverse Linked List II.** Locate one range, reverse it, and preserve the surrounding chain.
- **Boundary - Author exercise: Incomplete Final Group.** Look ahead `k` nodes and leave a short suffix unchanged.
- **Recognize - LC 25 Reverse Nodes in k-Group.** Repeat the bounded reversal while full groups remain.

### Merge Two Sorted Lists

**Recognition cue.** Two sorted linked chains must become one sorted chain without allocating replacement nodes. **Invariant.** The result tail ends a sorted finalized prefix; both remaining heads begin sorted suffixes. **False friend.** Copying values into an array avoids the pointer problem but violates the intended space and node-reuse contract.

- **Build - Author exercise: Merge Two One-Node Lists.** Attach the smaller head and then the remainder.
- **Vary - LC 21 Merge Two Sorted Lists.** Repeatedly consume the smaller current node.
- **Boundary - Author exercise: One Empty Or Exhausted List.** Attach the entire remaining suffix in one step.
- **Recognize - LC 148 Sort List.** Split, recursively sort, and reuse the merge invariant in linked-list merge sort.

### Use A Dummy Node At The Head

**Recognition cue.** The real head may be inserted, removed, or replaced, creating a special first-node case. **Invariant.** `dummy.next` always identifies the current result head while `tail` or `prev` owns the last finalized link. **False friend.** A dummy node is not automatically useful when the head never changes.

- **Build - Author exercise: Prepend Without A Special Case.** Insert through `dummy.next` and return that reference.
- **Vary - LC 21 Merge Two Sorted Lists.** Build the result behind a stable dummy tail.
- **Boundary - LC 203 Remove Linked List Elements.** Remove one or many matching original head nodes uniformly.
- **Recognize - LC 19 Remove Nth Node From End of List.** Let a dummy predecessor make deletion of the original head ordinary.

### Find Where A Cycle Starts

**Recognition cue.** Following `next` may revisit nodes, and the task asks whether a cycle exists or where it begins. **Invariant.** Floyd's slow and fast pointers collide inside a cycle; after resetting one pointer to the head, equal-speed movement meets at the entry. **False friend.** A value duplicate does not imply a node cycle—identity matters.

- **Build - LC 141 Linked List Cycle.** Detect a collision with one-step and two-step movement.
- **Vary - Author exercise: Measure Cycle Length.** Walk once around from the collision point.
- **Boundary - Author exercise: Self-Loop And Two-Node Cycle.** Guard fast-pointer dereferences correctly.
- **Recognize - LC 142 Linked List Cycle II.** Reset one pointer and locate the cycle entry without extra storage.

### Find Where Two Lists Meet

**Recognition cue.** Two acyclic lists may share the same tail nodes by reference. **Invariant.** Switching each pointer to the other head makes both traverse equal total distance before meeting or reaching null. **False friend.** Equal node values are not an intersection.

- **Build - Author exercise: Compare Node Identity.** Distinguish two separate nodes holding the same value.
- **Vary - Author exercise: Align By Length.** Advance the longer list by the length difference, then move together.
- **Boundary - Author exercise: No Intersection And Shared Head.** Verify both null meeting and immediate identity.
- **Recognize - LC 160 Intersection of Two Linked Lists.** Use head switching for constant-space alignment.

### Find The Middle Node

**Recognition cue.** A one-pass algorithm needs the midpoint without knowing length first. **Invariant.** Fast advances twice for each slow step; when fast reaches the end, slow has crossed half the nodes. **False friend.** Even-length lists have two middles, so the loop condition must match the requested one.

- **Build - Author exercise: Odd-Length Middle.** Trace slow and fast on five nodes.
- **Vary - LC 876 Middle of the Linked List.** Return the second middle for an even-length list.
- **Boundary - Author exercise: First Middle Contract.** Change the stopping condition to return the first of two middles.
- **Recognize - LC 234 Palindrome Linked List.** Find the midpoint before reversing and comparing the second half.

### Find The Kth Node From The End

**Recognition cue.** A node's position is defined relative to the end, but only one traversal is desired. **Invariant.** After advancing `fast` by the prescribed gap, moving both pointers preserves that distance until fast reaches the terminal position. **False friend.** Fast/slow ratio finds a fraction such as the middle; a fixed gap finds an offset from the end.

- **Build - Author exercise: Kth Node From End.** Create a gap of `k` and return the slow node.
- **Vary - Author exercise: Predecessor Of Kth From End.** Start behind a dummy node so slow stops before the target.
- **Boundary - Author exercise: K Equals Length.** Confirm the target is the original head and validate the input contract.
- **Recognize - LC 19 Remove Nth Node From End of List.** Preserve the gap, then bypass the target through its predecessor.

### Flatten Child Lists Into One List

**Recognition cue.** Nodes form a main doubly linked chain plus child chains that must be spliced into depth-first order. **Invariant.** Each splice preserves `prev`/`next` symmetry and retains the old successor so traversal can resume after the child chain. **False friend.** Updating only forward links creates a list that looks correct in one direction but is structurally broken.

- **Build - Author exercise: Splice One Child Chain.** Connect parent, child head, child tail, and saved successor in a safe order.
- **Vary - Author exercise: Stack Of Deferred Successors.** Push the old `next` when descending and restore it after a child chain ends.
- **Boundary - Author exercise: Child At Tail And Nested Child.** Handle a null saved successor and more than one nesting level.
- **Recognize - LC 430 Flatten a Multilevel Doubly Linked List.** Produce preorder flattening while clearing every child pointer.

## Released Combination Lessons

### Copy A List With Random Links

The linked list supplies node identity and outgoing references; the map records which clone corresponds to each original node. Values alone cannot reconstruct arbitrary `random` edges, and pointer traversal alone cannot find a clone by original identity in constant time.

- **Build - Author exercise: Original-To-Clone Map.** Create one clone for every original node and store the identity mapping.
- **Vary - LC 138 Copy List with Random Pointer.** Use a second pass to wire `next` and `random` through the map.
- **Boundary - Author exercise: Null, Self, And Shared Random Targets.** Preserve all three reference cases without cloning a target twice.
- **Recognize - Author exercise: Two Arbitrary References.** Clone nodes containing `next`, `randomA`, and `randomB` by reusing the same identity-map invariant.

### Deferred: LRU Cache Composition

An LRU cache needs a map for direct lookup plus a doubly linked recency list with strict ownership around sentinels. Chapter 33 introduces the design API and owns that combination staircase.

## Practice Contract

Every independently recognizable micro-pattern receives its own staircase:

1. **Build:** implement only the newly introduced state or operation.
2. **Vary:** change one decision, output contract, or local condition.
3. **Boundary:** protect the invariant against the pattern's meaningful edge case.
4. **Recognize:** use the same state in an easy-side-medium LeetCode-style prompt.
5. Add Extend, Medium, or Hard only after every added prerequisite is already taught.

For each exercise record the source/ID, formal prompt, relevant constraints, two examples including one hostile case, diagnostic hint, solution rationale, complexity, and annotated Java.

## Java Integrity Focus

- Use a dummy node only when its ownership simplifies the returned head contract.
- Guard pointer rewiring order so the unreached suffix is never lost.

## Unlocked Combinations Preview

Review this table before PDF authoring. It is deliberately visible here so a released composition cannot be discovered only after a chapter has already been rendered.

| Outcome | Combination | Review requirement |
| --- | --- | --- |
| Teach now | Linked List + Hash Map | Original-to-clone identity mapping; representative: LC 138 |
| Deferred | Hash Map + Linked List Cache | Chapter 33 adds API and recency-list ownership |

For each `Teach now` row, the future PDF must include a named combination lesson and a separate staircase. For each `Deferred` row, the PDF must name the missing prerequisite and owner but must not assign its problems. `Already covered` rows link to the existing lesson rather than duplicating it.



## Composition Audit

At authoring time, compare this chapter's newly introduced micro-patterns with every completed earlier specification. A combination is released only if all of its prerequisites are already taught and its recognition cue or invariant is genuinely distinct.

**Currently deferred from this chapter:** cache design and multi-list design structures beyond the released random-pointer copy.

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

