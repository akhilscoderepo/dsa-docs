# Lesson spec: Fixed Frequency Windows

**Recognition cue.** Every candidate has a fixed length, but validity depends on its multiset rather than its aggregate. **Invariant.** The frequency state describes exactly the current length-`k` window. **False friend.** Sorting every window destroys linear time. **Java hazard.** A small count array is valid only when the character domain is stated.

- **Build - Author exercise: Binary Window Counts.** For every length-`k` block, report its number of ones.
- **Vary - LC 438 Find All Anagrams in a String.** Record every start whose counts match the pattern.
- **Boundary - Author exercise: Repeated Required Character.** Test a pattern such as `aab`; set membership cannot represent multiplicity.
- **Recognize - LC 567 Permutation in String.** Return whether any fixed window has the pattern's frequency signature.
