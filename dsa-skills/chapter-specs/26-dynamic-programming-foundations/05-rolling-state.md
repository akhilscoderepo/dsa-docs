# Lesson spec: Rolling State

**Recognition cue.** A transition reads only a fixed recent window of DP values. **Invariant.** Each scalar retains the exact prior state named by the recurrence before update.

- **Build - Author exercise: Two-State Fibonacci.** Keep previous-two and previous-one.
- **Vary - LC 198 House Robber.** Roll skip/take prefix values.
- **Boundary - Author exercise: Update Order.** Save old values before overwriting a needed dependency.
- **Recognize - LC 746 Min Cost Climbing Stairs.** Compress the table to constant auxiliary space.
