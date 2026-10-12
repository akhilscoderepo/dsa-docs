# Lesson spec: Partition State

**Recognition cue.** Values must split into groups with equal or constrained sums. **Invariant.** Reachable sums summarize all one-use choices processed so far.

- **Build - Author exercise: Reachable Subset Sums.** Update Boolean capacity states descending.
- **Vary - LC 416 Partition Equal Subset Sum.** Reduce equal partition to target `total/2`.
- **Boundary - Author exercise: Odd Total And Large Target.** Reject parity immediately and budget memory by target.
- **Recognize - LC 1049 Last Stone Weight II.** Find the reachable sum closest to half.
