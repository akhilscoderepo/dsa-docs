# Lesson spec: Compress Runs Of Characters

**Recognition cue.** Equal adjacent characters form one completed run. **State.** The current character and run length describe the suffix not yet emitted. **False friend.** Arbitrary duplicate grouping needs a map or sort.

- **Build - LC 443 String Compression.** Compress adjacent runs in place.
- **Vary - LC 38 Count and Say.** Read one run and construct the next string.
- **Boundary - Author exercise: Final Run.** Ensure `"aaab"` emits both `3a` and `1b`.
- **Recognize - Author exercise: Run-Length Encoding.** Convert a string such as `"aaabbc"` to `"3a2b1c"` by emitting each maximal run exactly once.
