# Lesson spec: Kadane State

**Recognition cue.** The objective is the best contiguous sum with no fixed length. **State.** `bestEndingHere` is the best sum of a subarray forced to end at the current position; `bestOverall` is the best seen anywhere. This recurrence is **Kadane's algorithm**. **False friend.** Running minimum plus stock gain chooses two positions, not one contiguous subarray.

- **Build — LC 53 Maximum Subarray.** `[-2,1,-3,4,-1,2,1,-5,4] → 6`; `[-3] → -3`.
- **Vary — Author exercise: Minimum Subarray Sum.** Replace the maximum recurrence with the minimum recurrence; all-positive input must still return its smallest element.
- **Boundary — Author exercise: All Negative.** Return the largest value, not zero, for `[-8,-3,-6] → -3`; this protects the non-empty subarray contract.
- **Recognize — LC 1749 Maximum Absolute Sum of Any Subarray.** Track both maximum and minimum ending states because either can produce the largest magnitude.
