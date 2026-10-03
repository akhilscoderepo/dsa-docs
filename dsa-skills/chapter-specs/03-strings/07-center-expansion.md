# Lesson spec: Center Expansion

**Recognition cue.** A substring is defined by symmetry around one character or one gap. **State.** `left` and `right` expand only while characters match; the center remains fixed for one attempt. **False friend.** This is not opposite-end validation of the whole string.

- **Build - LC 647 Palindromic Substrings.** Expand around every odd and even center.
- **Vary - LC 5 Longest Palindromic Substring.** Preserve the best interval rather than only a count.
- **Boundary - Author exercise: Even Center.** `"abba"` must discover a palindrome centered between the middle characters.
- **Recognize - Author exercise: Longest Even-Length Palindrome.** Return the longest palindromic substring whose center lies between two characters, using the same expansion invariant with different initial boundaries.
