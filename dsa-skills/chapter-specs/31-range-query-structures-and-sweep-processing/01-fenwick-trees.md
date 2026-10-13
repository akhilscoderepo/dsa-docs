# Lesson spec: Fenwick Trees

**Recognition cue.** Point updates and prefix/range sums must both be logarithmic. **Invariant.** Tree index `i` stores the block ending at `i` whose length is `i & -i`; implementation uses one-based indexing.

- **Build - Author exercise: Prefix Query.** Repeatedly subtract the low bit.
- **Vary - Author exercise: Point Update.** Add a delta while repeatedly adding the low bit.
- **Boundary - Author exercise: Index Conversion.** Map external zero-based positions to internal one-based positions.
- **Recognize - LC 307 Range Sum Query - Mutable.** Compute range sums as two prefixes and update by delta.
