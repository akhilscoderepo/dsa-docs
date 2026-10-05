# Lesson spec: Allow K Replacements In A Window

**Recognition cue.** A range can be made uniform by changing at most `k` values. **Invariant.** The required replacements are `windowLength - maxFrequency`; the window is usable when that value is at most `k`. **False friend.** Recomputing the maximum frequency on every move is unnecessary for the standard longest-length formulation.

- **Build - Author exercise: Replacement Cost Of One Window.** Given fixed boundaries, compute length minus its largest frequency.
- **Vary - Author exercise: Longest Binary Uniform Window.** Permit at most `k` flips and maintain the dominant count.
- **Boundary - Author exercise: Stale Maximum Trace.** Show why a historical `maxFrequency` may remain high without causing an impossible best length to be reported.
- **Recognize - LC 424 Longest Repeating Character Replacement.** Use the replacement budget to maintain the best achievable length.
