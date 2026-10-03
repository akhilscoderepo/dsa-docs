# Lesson spec: Earliest Balance

**Recognition cue.** The goal is the longest span between two equal balance states. **State.** Store the earliest index for each balance because the earliest occurrence creates the longest later span. **False friend.** Frequency counts answer how many spans; earliest indices answer the longest span.

- **Build - LC 525 Contiguous Array.** Treat `0` as `-1`; equal balances enclose equal counts.
- **Vary - Author exercise: Equal A And B.** Add `+1` for `A`, `-1` for `B`, and `0` for irrelevant values.
- **Boundary - Author exercise: Prefix From Zero.** Seed balance zero at index `-1` so a valid span can start at index zero.
- **Recognize - LC 1371 Find the Longest Substring Containing Vowels in Even Counts.** The repeated state is a parity mask rather than one integer balance.
