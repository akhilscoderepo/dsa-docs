# Lesson spec: Array Cycle State

**Recognition cue.** Every array value is a legal next index, producing a functional graph, and the contract implies a cycle whose entry represents the duplicate. **Invariant.** Floyd’s fast/slow phase finds a meeting inside the cycle; resetting one pointer and moving both one step finds the entry. **False friend.** Sign marking and cyclic placement mutate the array; this method follows links without modification.

- **Build - Author exercise: Follow Links.** Starting at index zero, repeatedly move to `nums[index]` under a proven in-range contract.
- **Vary - LC 287 Find the Duplicate Number.** Interpret values as next indices and return the cycle entry.
- **Boundary - Author exercise: Immediate Cycle.** Trace the smallest legal input and prove every dereference remains in range.
- **Recognize - LC 287 Proof Exercise.** Explain why phase two’s equal-speed pointers meet at the entry, not merely somewhere in the cycle.
