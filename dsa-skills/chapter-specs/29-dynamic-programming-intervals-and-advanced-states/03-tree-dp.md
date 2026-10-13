# Lesson spec: Tree DP

**Recognition cue.** Each subtree returns several values because the parent decision changes what children may do. **Invariant.** Returned state summarizes the subtree completely for every parent-relevant mode.

- **Build - Author exercise: Take Or Skip Node.** Return two values from each subtree.
- **Vary - LC 337 House Robber III.** Taking a node forces both children into skip states.
- **Boundary - Author exercise: Null And Negative Values.** Define neutral returns and the empty-choice contract.
- **Recognize - Author exercise: Rerooted Distance Sums.** Use one subtree pass and one parent-contribution pass.
