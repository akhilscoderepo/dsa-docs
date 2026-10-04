# Lesson spec: Input Preconditions And Defensive Assumptions

**Recognition cue.** Correct initialization and guards depend on facts promised by the caller: non-empty input, sorted order, legal indices, rectangular shape, or bounded values. **State.** List guarantees separately from assumptions introduced by the solution. **Invariant.** Code may rely on a documented guarantee but must not invent one. **False friend.** Defensive branches added from habit can obscure the actual algorithm and may define behavior the problem never requested.

- **Build - Author exercise: Non-Empty Maximum.** Given a non-empty array contract, initialize a maximum from `nums[0]`. Explain why initializing from zero fails for `[-8,-3]` and why an empty-array guard is unnecessary under this exact contract.
- **Vary - Author exercise: Possibly Empty.** Change the contract to allow an empty array. Choose and document one response: sentinel, exception, or optional result. The method signature must agree with that choice.
- **Boundary - Author exercise: Rectangular Or Ragged.** For `int[][] grid`, distinguish a rectangular guarantee from a ragged array. Explain why `grid[0].length` is unsafe as the bound for every row when ragged input is legal.
- **Recognize - Author exercise: Sorted Promise.** Show which conclusion becomes valid when an array is guaranteed sorted: equal values form adjacent runs. Do not yet introduce binary search or two pointers.
