# Lesson spec: Combine Totals From Both Sides

**Recognition cue.** Every output position needs an aggregate of all elements except itself. **State.** A left pass stores the aggregate before `i`; a right pass folds the aggregate after `i`. **False friend.** Division may be forbidden or invalid around zeros.

- **Build - Author exercise: Sum Except Self.** Return total-minus-current using `long` under an additive contract.
- **Vary - LC 238 Product of Array Except Self.** Build left products, then multiply by a rolling right product without division.
- **Boundary - LC 238 With Zeros.** Verify one zero and multiple zeros without special division cases.
- **Recognize - Author exercise: Prefix And Suffix Maximums.** Give every index the best value strictly to its left and right.
