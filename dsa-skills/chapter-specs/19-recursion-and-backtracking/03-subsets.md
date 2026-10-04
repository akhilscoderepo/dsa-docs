# Lesson spec: Subsets

**Recognition cue.** Every element may be included or excluded, and order inside a result follows input order. **Invariant.** At index `i`, the path fixes decisions for indices before `i`; later indices remain undecided. **False friend.** Permutation state chooses an unused element for a position and creates ordered arrangements.

- **Build - Author exercise: Subsets Of Two Values.** Draw the include/exclude tree.
- **Vary - LC 78 Subsets.** Record the current path at every node of an increasing-start search.
- **Boundary - Author exercise: Empty Input.** Return one subset—the empty set—not an empty result collection.
- **Recognize - LC 90 Subsets II.** Sort and skip equal sibling choices to avoid duplicate subsets.
