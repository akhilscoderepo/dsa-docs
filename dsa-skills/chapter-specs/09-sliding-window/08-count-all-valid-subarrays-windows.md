# Lesson spec: Count-All-Valid-Subarrays Windows

**Recognition cue.** The problem asks for the number of contiguous ranges and, once the left boundary is restored, every suffix ending at `right` is valid. **Invariant.** After shrinking, starts `left..right` produce exactly `right - left + 1` valid subarrays ending at `right`. **False friend.** This addition is invalid when validity is not monotone under removing a prefix. **Java hazard.** Use `long` when the number of subarrays can exceed `int`.

- **Build - Author exercise: Count Subarrays With At Most One Zero.** Add the number of valid starts for each right endpoint.
- **Vary - Author exercise: Count Subarrays With Sum Below K For Positive Values.** Use positivity to justify that removing from the left cannot increase the sum.
- **Boundary - Author exercise: K At The Minimum.** Verify that a window may shrink to empty and contributes zero.
- **Recognize - LC 713 Subarray Product Less Than K.** Maintain a positive-product window and count all valid suffixes.
