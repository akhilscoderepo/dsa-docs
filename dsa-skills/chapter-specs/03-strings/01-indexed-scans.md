# Lesson spec: Indexed Scans

**Recognition cue.** Each character can be inspected independently or folded into a small running answer. **State.** `i` is the next unexamined index. **False friend.** A reversed or paired comparison needs two pointers, not one scan.

- **Build - Author exercise: Count Digits.** Given `s`, return how many characters are decimal digits. `"a1b2" -> 2`; `"" -> 0`.
- **Vary - LC 58 Length of Last Word.** Scan characters while defining exactly when a word begins and ends.
- **Boundary - Author exercise: First Delimiter.** Return the first index of `':'`, or `-1`; test `":x"` and `"abc"`.
- **Recognize - LC 709 To Lower Case.** Each output character depends only on its input character.
