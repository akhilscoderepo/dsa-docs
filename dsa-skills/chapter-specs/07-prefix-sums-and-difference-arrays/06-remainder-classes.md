# Lesson spec: Group Prefixes By Remainder

**Recognition cue.** Divisibility of a range depends on two prefixes having the same normalized remainder. **State.** Store counts or earliest indices by `Math.floorMod(prefix, k)`. **Java hazard.** Java `%` may be negative.

- **Build - LC 974 Subarray Sums Divisible by K.** Count equal normalized remainder pairs.
- **Vary - LC 523 Continuous Subarray Sum.** Store earliest remainder indices and enforce length at least two.
- **Boundary - Author exercise: Negative Values.** Normalize negative prefix remainders with `Math.floorMod`.
- **Recognize - Author exercise: Longest Divisible Span.** Switch map meaning from count to earliest index.
