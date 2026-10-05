# Lesson spec: Slide A Window Of Fixed Size

**Recognition cue.** The problem asks for every contiguous block of exactly `k` elements and the block can be updated when one value leaves and one enters. **Invariant.** Before recording a result, the maintained aggregate equals the contents of `nums[left..right]`, whose length is `k`. **False friend.** A prefix sum is often better when many unrelated range queries follow; a window is natural for one left-to-right pass.

- **Build - Author exercise: Sums of Every K-Block.** Return the sum of each length-`k` subarray by adding the entering value and removing the leaving value.
- **Vary - LC 643 Maximum Average Subarray I.** Track the maximum fixed-window sum and divide only once at the end.
- **Boundary - Author exercise: Whole-Array Window.** Handle `k == nums.length` and state the contract for illegal `k` rather than silently inventing a result.
- **Recognize - LC 1456 Maximum Number of Vowels in a Substring of Given Length.** Replace numeric sum with a Boolean contribution per character.
