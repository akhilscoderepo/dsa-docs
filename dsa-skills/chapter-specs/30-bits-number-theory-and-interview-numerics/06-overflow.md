# Lesson spec: Overflow

**Recognition cue.** Arithmetic may exceed the destination type before assignment. **Invariant.** Widen operands before the overflowing operation, not afterward.

- **Build - Author exercise: Int Sum Into Long.** Compare late and early casts.
- **Vary - Author exercise: Safe Comparator.** Use `Integer.compare` rather than subtraction.
- **Boundary - Author exercise: MIN_VALUE Negation.** Widen before negating.
- **Recognize - LC 7 Reverse Integer.** Check the next digit before multiplication and addition overflow.
