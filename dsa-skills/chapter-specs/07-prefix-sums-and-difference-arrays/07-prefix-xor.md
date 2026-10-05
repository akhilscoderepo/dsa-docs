# Lesson spec: Use XOR As A Running Total

**Recognition cue.** A range XOR can be recovered because `x ^ x = 0`. **State.** `prefixXor[i]` summarizes values before `i`, so a range is the XOR of two prefix states.

- **Build - LC 1310 XOR Queries of a Subarray.** Answer immutable range XOR queries.
- **Vary - Author exercise: Count XOR K.** Use a frequency map and look up `prefixXor ^ k`.
- **Boundary - Author exercise: Empty Prefix.** Seed XOR zero for ranges starting at index zero.
- **Recognize - LC 1442 Count Triplets That Can Form Two Arrays of Equal XOR.** Repeated prefix XOR states identify zero-XOR ranges.
