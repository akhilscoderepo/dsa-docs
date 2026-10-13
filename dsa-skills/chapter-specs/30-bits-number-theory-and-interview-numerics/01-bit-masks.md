# Lesson spec: Bit Masks

**Recognition cue.** Individual Boolean flags fit into bit positions. **Invariant.** AND tests, OR sets, and AND with complement clears the named bit.

- **Build - Author exercise: Flag Operations.** Set, test, toggle, and clear one bit.
- **Vary - Author exercise: Permission Set.** Combine several named flags.
- **Boundary - Author exercise: Position Width.** Use `1L << bit` when positions exceed `int` capacity.
- **Recognize - LC 318 Maximum Product of Word Lengths.** Represent each word's character set as a mask.
