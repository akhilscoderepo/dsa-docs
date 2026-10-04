# Lesson spec: Choose An Array Or A Map

**Recognition cue.** A compact, known domain makes an array a more direct representation than a map. **State.** `count[value - min]` maps the declared range to slots; a `HashMap` remains the general representation for sparse or open-ended keys. **False friend.** Do not claim `int[26]` works for arbitrary Unicode text.

- **Build - Author exercise: Lowercase Character Counts.** Count `a` through `z` with `int[26]` under an explicit lowercase-English contract.
- **Vary - LC 242 Valid Anagram.** Replace a map with a frequency array only after the alphabet contract is stated.
- **Boundary - Author exercise: Sparse IDs.** Explain why values `{2, 1_000_000_000}` reject direct addressing even though both are integers.
- **Recognize - LC 706 Design HashMap.** The prompt removes the compact-domain guarantee; a general hash representation is now justified.
