# Lesson spec: Digit DP

**Recognition cue.** Count numbers up to a bound under digit constraints without enumerating every number. **Invariant.** State includes position, whether the prefix is tight to the bound, and whether a nonleading digit has started the number.

- **Build - Author exercise: Count Fixed-Length Digit Strings.** Start without tightness.
- **Vary - Author exercise: Add Tight State.** Restrict the next digit by the bound prefix.
- **Boundary - Author exercise: Leading Zero And Number Zero.** Define when the constructed number has started.
- **Recognize - LC 902 Numbers At Most N Given Digit Set.** Count valid numbers under a decimal upper bound.
