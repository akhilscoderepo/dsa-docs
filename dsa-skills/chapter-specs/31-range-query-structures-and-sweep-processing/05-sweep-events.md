# Lesson spec: Sweep Events

**Recognition cue.** State changes only at sorted coordinates or times. **Invariant.** After applying events under the stated tie policy, active state represents exactly the interval between this coordinate and the next.

- **Build - LC 1094 Car Pooling.** Add passenger deltas at pickup and drop-off coordinates.
- **Vary - Author exercise: Group Equal Coordinates.** Apply all same-position deltas before evaluating the next span.
- **Boundary - Author exercise: Start-End Tie.** Choose event order from closed or half-open semantics.
- **Recognize - LC 218 The Skyline Problem.** Maintain active heights while sweeping building boundaries.
