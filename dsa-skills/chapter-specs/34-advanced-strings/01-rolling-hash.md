# Lesson spec: Rolling Hash

**Recognition cue.** Many equal-length substrings need fast equality checks or repeated-pattern detection. **Invariant.** The maintained hash represents exactly the current substring under fixed base/modulus rules. **False friend.** Hash equality is not proof unless collisions are verified or bounded by policy.

- **Build - Author exercise: Fixed-Window Hash.** Remove the outgoing character and append the incoming one.
- **Vary - LC 187 Repeated DNA Sequences.** Record repeated fixed-length encodings.
- **Boundary - Author exercise: Negative Modular Difference.** Normalize after removing the outgoing contribution.
- **Recognize - LC 1044 Longest Duplicate Substring.** Combine rolling hash with binary search and collision verification.
