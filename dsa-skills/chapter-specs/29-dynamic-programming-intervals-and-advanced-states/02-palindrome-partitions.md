# Lesson spec: Palindrome Partitions

**Recognition cue.** Partition cost depends on whether each substring is a palindrome. **Invariant.** A precomputed palindrome table answers validity while a prefix DP minimizes cuts.

- **Build - Author exercise: Palindrome Table.** Fill equal endpoints after the inner interval is known.
- **Vary - Author exercise: Minimum Valid Prefix Pieces.** Transition from every earlier cut whose suffix is valid.
- **Boundary - Author exercise: Empty Prefix And Whole Palindrome.** Avoid an off-by-one extra cut.
- **Recognize - LC 132 Palindrome Partitioning II.** Combine substring validity with minimum partition cuts.
