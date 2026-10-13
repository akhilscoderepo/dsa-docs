# Lesson spec: Modular Arithmetic

**Recognition cue.** Counts or products must remain within a modulus. **Invariant.** Reduce after safe-width addition or multiplication while preserving congruence.

- **Build - Author exercise: Modular Sum And Product.** Cast to `long` before product.
- **Vary - Author exercise: Modular Fast Power.** Combine reduction with binary exponentiation.
- **Boundary - Author exercise: Negative Remainder.** Normalize Java's negative `%` result when required.
- **Recognize - LC 1498 Number of Subsequences That Satisfy the Given Sum Condition.** Precompute powers of two modulo the required constant.
