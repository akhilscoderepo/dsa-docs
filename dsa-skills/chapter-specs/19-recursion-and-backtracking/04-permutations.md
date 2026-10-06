# Lesson spec: List Every Ordering

**Recognition cue.** Every output uses all elements, but their positions may differ. **Invariant.** Depth equals the next output position; used state prevents one input occurrence from filling two positions. **False friend.** Increasing-start indices generate combinations, not permutations.

- **Build - Author exercise: Permute Three Distinct Values.** Mark one unused index per depth.
- **Vary - LC 46 Permutations.** Generate all arrangements with a used array or in-place swaps.
- **Boundary - Author exercise: Restore Used State.** Verify every recursive return clears exactly the selected index.
- **Recognize - LC 47 Permutations II.** Sort and skip equal unused siblings while allowing equal values at different depths.
