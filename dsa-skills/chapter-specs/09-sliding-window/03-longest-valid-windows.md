# Lesson spec: Find The Longest Valid Window

**Recognition cue.** The answer is the longest contiguous range satisfying a condition that can be restored by moving `left` forward. **Invariant.** After the shrink loop, the current window is valid; every discarded start is known to be unusable for the current `right`. **False friend.** A minimum-cover problem shrinks while valid and records before validity is lost.

- **Build - Author exercise: Longest Binary Run With One Zero.** Maintain the number of zeroes and shrink while it exceeds one.
- **Vary - LC 3 Longest Substring Without Repeating Characters.** Maintain character multiplicities and remove from the left until the duplicate is gone.
- **Boundary - Author exercise: Violation At Both Ends.** Trace repeated violations and verify the loop may remove several elements for one `right`.
- **Recognize - LC 1004 Max Consecutive Ones III.** Treat zeroes as violations with a budget of `k`.
