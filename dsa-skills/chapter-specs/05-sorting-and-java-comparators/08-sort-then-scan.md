# Lesson spec: Scan The Sorted Array

**Recognition cue.** Sorting exposes a simple adjacent relation but does not itself compute the answer. **State.** A scan retains the best local candidate under the new order. **False friend.** Binary search needs a monotone query contract, not merely sorted input.

- **Build - LC 414 Third Maximum Number.** Sort then select under duplicate rules.
- **Vary - LC 506 Relative Ranks.** Preserve original positions while scanning sorted values.
- **Boundary - Author exercise: Fewer Than k Distinct Values.** Return the stated fallback rather than indexing past the deduplicated run count.
- **Recognize - LC 268 Missing Number.** Sort the values, then return the first index whose value differs from the expected value; return `n` if every earlier position matches.
