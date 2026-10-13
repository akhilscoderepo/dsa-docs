# Lesson spec: Palindromic Sequences

**Recognition cue.** The state is a substring interval, but characters may be skipped. **Invariant.** `dp[left][right]` is the best palindromic subsequence within that closed interval.

- **Build - Author exercise: Length One And Two.** Establish interval base cases.
- **Vary - LC 516 Longest Palindromic Subsequence.** Match equal endpoints or skip one endpoint.
- **Boundary - Author exercise: Fill By Increasing Length.** Ensure inner intervals are ready first.
- **Recognize - LC 1312 Minimum Insertion Steps to Make a String Palindrome.** Relate insertions to the longest palindromic subsequence.
