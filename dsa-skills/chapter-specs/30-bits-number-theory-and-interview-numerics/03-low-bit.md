# Lesson spec: Low Bit

**Recognition cue.** The algorithm repeatedly removes or isolates the least significant set bit. **Invariant.** `x & (x - 1)` clears exactly one set bit; `x & -x` isolates it under two's complement.

- **Build - Author exercise: Clear One Set Bit.** Trace a binary value.
- **Vary - LC 191 Number of 1 Bits.** Count iterations until zero.
- **Boundary - Author exercise: Zero And Negative Int.** Treat the value as a fixed 32-bit pattern.
- **Recognize - LC 338 Counting Bits.** Derive each count from a smaller value with one bit removed.
