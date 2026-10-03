# Lesson spec: Lower And Upper Bounds

**Recognition cue.** The output is an insertion boundary: first value `>= target` or first value `> target`. **Invariant.** One side is known to fail the predicate and the other contains the first possible success. **False friend.** Exact search may stop on equality; bounds may not.

- **Build - LC 35 Search Insert Position.** Find the first position whose value is at least `target`.
- **Vary - Author exercise: Upper Bound.** Find the first position whose value is strictly greater than `target`.
- **Boundary - Author exercise: Outside Range.** Test a target smaller than every value and larger than every value; insertion positions may be `0` or `n`.
- **Recognize - LC 744 Find Smallest Letter Greater Than Target.** Apply upper-bound logic plus the stated wraparound contract.
