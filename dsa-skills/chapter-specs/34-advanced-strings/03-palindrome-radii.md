# Lesson spec: Find Palindromes Around Every Center

**Recognition cue.** Palindromes centered at every position must be found in linear time. **Invariant.** Manacher's algorithm maintains the rightmost known palindrome and mirrors a radius within it, then expands only beyond known coverage.

- **Build - Author exercise: Expand Odd Centers.** Compute radii by direct expansion.
- **Vary - Author exercise: Unified Separators.** Transform the string so odd and even palindromes share one representation.
- **Boundary - Author exercise: Mirror Beyond Boundary.** Clamp the copied radius to the current right edge.
- **Recognize - LC 5 Longest Palindromic Substring.** Use radii to recover the longest substring boundaries.
