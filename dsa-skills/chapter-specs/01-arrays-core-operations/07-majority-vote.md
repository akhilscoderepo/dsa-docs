# Lesson spec: Majority Vote

**Recognition cue.** One value may occur more than half the time, and constant extra space is requested. **State.** `candidate` and `votes`; a different value cancels one vote, and the same value adds one. **Invariant.** After reading a prefix, every value other than `candidate` that was cancelled was cancelled against a distinct occurrence, so a true majority of the whole array cannot be eliminated. **Verification requirement.** The survivor is only a candidate unless the contract guarantees a majority; a second counting pass confirms it. **False friend.** It is not a frequency map and not ordinary counting. Added by the coverage audit addendum (Boyer-Moore majority vote).

- **Build — LC 169 Majority Element.** `[2,2,1,1,2] → 2`; `[3] → 3`. A majority is guaranteed.
- **Vary — Author exercise: Verify The Candidate.** No majority is guaranteed. Run the vote, then count the survivor in a second pass and return it only when it occurs more than `n/2` times, otherwise `-1`.
- **Boundary — Author exercise: No Majority.** `[1,2,3]` leaves a survivor that is not a majority; show why verification is mandatory. Also trace `[1,2]`, where the votes cancel to zero.
- **Recognize — Author exercise: Dominant Product Id.** A stream of order lines each carry a product id; decide whether any single id accounts for more than half the lines, using O(1) extra space.
- **Extend — LC 229 Majority Element II.** Elements occurring more than `n/3` times: two candidates and two vote counters, with a mandatory verification pass.
