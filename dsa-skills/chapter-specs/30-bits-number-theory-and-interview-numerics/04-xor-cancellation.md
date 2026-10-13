# Lesson spec: XOR Cancellation

**Recognition cue.** Equal values pair off, or differing bits must be isolated without carries. **Invariant.** XOR is associative, commutative, and cancels `x ^ x` to zero.

- **Build - LC 136 Single Number.** Cancel every paired value.
- **Vary - Author exercise: Missing Value By XOR.** XOR indices and values.
- **Boundary - Author exercise: Zero And Negative Values.** Cancellation is bitwise and independent of sign.
- **Recognize - LC 260 Single Number III.** Split values by one differing set bit.
