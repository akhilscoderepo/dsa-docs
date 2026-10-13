# Lesson spec: Shifts

**Recognition cue.** Bits must move, extract, or assemble by position. **Invariant.** Shift meaning follows Java's signed `>>` versus zero-fill `>>>` contract.

- **Build - Author exercise: Extract Bit I.** Shift then mask one bit.
- **Vary - LC 190 Reverse Bits.** Read and append all 32 bit positions.
- **Boundary - Author exercise: Negative Values.** Compare `>>` and `>>>` without an infinite sign-extension loop.
- **Recognize - Author exercise: Pack Two Fields.** Store and recover bounded fields with masks and shifts.
