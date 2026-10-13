# Lesson spec: Weighted Selection

**Recognition cue.** Item probability is proportional to a positive weight. **Invariant.** Prefix sums partition `[1,totalWeight]` into intervals whose lengths equal weights.

- **Build - Author exercise: Prefix Weight Intervals.** Map a random ticket to one item.
- **Vary - LC 528 Random Pick with Weight.** Binary-search the first prefix reaching the ticket.
- **Boundary - Author exercise: Large Total And Zero Weight Policy.** Use `long` and state whether zero weights are legal.
- **Recognize - Author exercise: Mutable Weight Discussion.** Explain why updates would require a Fenwick tree rather than static prefixes.
