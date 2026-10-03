# Lesson spec: Product State

**Recognition cue.** The objective is a contiguous product and negative values can reverse the useful order. **State.** Keep both the maximum and minimum product ending at the current index; a negative swaps their roles. **False friend.** Sum Kadane needs one ending state because addition does not reverse order.

- **Build — LC 152 Maximum Product Subarray.** `[2,3,-2,4] → 6`; `[-2,0,-1] → 0`.
- **Vary — Author exercise: Product Ending Here.** Return the best product forced to include the final item; this removes `bestOverall` but retains max/min state.
- **Boundary — LC 152 zero-and-negative trace.** Dry-run `[-2,3,-4] → 24` and `[0,-2] → 0`.
- **Recognize — LC 1567 Maximum Length of Subarray With Positive Product.** The representation changes from products to sign/length state, but a negative still swaps the favorable and unfavorable histories.
