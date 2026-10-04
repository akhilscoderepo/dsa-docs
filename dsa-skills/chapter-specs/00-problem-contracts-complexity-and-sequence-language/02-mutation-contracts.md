# Lesson spec: Specifying Preconditions, Postconditions And Mutation

**Recognition cue.** The prompt states whether the input may change and whether extra storage counts against the target. **State.** Separate the physical container from the logical result. **Invariant.** Every write preserves data still needed by a later read. **False friend.** “In place” does not mean “the Java array becomes shorter,” and output storage required by the return value is not always counted as auxiliary space.

- **Build - Author exercise: Meaningful Prefix.** Given `nums = [3,2,2,3]`, suppose a method returns `k = 2` after filtering `3`. State precisely what is guaranteed about `nums[0..k-1]` and what is unspecified about the suffix.
- **Vary - Author exercise: Preserve Input.** Given a contract that forbids mutation, choose between overwriting `nums` and allocating `result`. Explain why a correct value with a modified input still violates the API.
- **Boundary - Author exercise: Aliased Input.** Two variables refer to the same array. Trace why mutating through one reference is observable through the other. The exercise changes no algorithm; it changes the caller-visible contract.
- **Recognize - Author exercise: Output Space.** A method must return an array of length `n`. Distinguish the `O(n)` returned output from additional working memory, then state both conventions explicitly instead of hiding one.
