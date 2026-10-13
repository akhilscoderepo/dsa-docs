# Lesson spec: Match A Pattern Without Restarting

**Recognition cue.** Pattern matching must reuse knowledge after a mismatch instead of restarting. **Invariant.** KMP's prefix function stores the longest proper prefix that is also a suffix; fallback preserves already matched structure.

- **Build - Author exercise: Prefix Function.** Compute fallback lengths for one pattern.
- **Vary - LC 28 Find the Index of the First Occurrence in a String.** Match text with KMP state.
- **Boundary - Author exercise: Repeated Prefixes.** Trace a pattern such as `ababaca` through multiple fallbacks.
- **Recognize - LC 1392 Longest Happy Prefix.** Read the final prefix-function value as the answer.
- **Extend - Author exercise: Z Array.** Compute, for every position, the length matching the string prefix and compare its reuse window with KMP fallback state.
