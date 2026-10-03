# Lesson spec: Constraint Signals

**Recognition cue.** The input limits rule out entire classes of solutions before code is written. **State.** Record the largest possible input size, value range, and required operation count. **Invariant.** A proposed approach must remain within its time and memory budget at the maximum legal input. **False friend.** Difficulty labels and familiar nouns such as “array” do not select an algorithm; the contract does.

- **Build - Author exercise: Budget Check.** Given `1 <= n <= 100_000`, classify a single scan, an `O(n log n)` sort, and an all-pairs `O(n^2)` comparison as plausible or implausible for an ordinary interview time limit. Hint: estimate growth at the maximum `n`, not at the sample input.
- **Vary - Author exercise: Small Domain.** Given `1 <= n <= 100_000` and `0 <= nums[i] <= 100`, explain why an auxiliary array of 101 counters may be reasonable even though an array indexed by arbitrary integer values would not be.
- **Boundary - Author exercise: Hidden Overflow.** Given `n = 100_000` and `|nums[i]| <= 1_000_000_000`, decide whether the total sum fits in Java `int`. The hostile case is one hundred thousand maximum positive values.
- **Recognize - Author exercise: Query Pressure.** Compare one range-sum query with one hundred thousand range-sum queries over unchanged data. State why the number of operations, rather than the word “array,” changes the acceptable design. The later Prefix Sum chapter owns the implementation.
