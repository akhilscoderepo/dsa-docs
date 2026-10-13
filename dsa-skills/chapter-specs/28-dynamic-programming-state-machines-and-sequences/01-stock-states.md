# Lesson spec: Stock States

**Recognition cue.** Each day ends in a small mode such as holding or not holding. **Invariant.** `hold` and `cash` are the best values after processing the current prefix under their exact ownership states.

- **Build - LC 121 Best Time to Buy and Sell Stock.** Track one buy followed by one sell.
- **Vary - LC 122 Best Time to Buy and Sell Stock II.** Transition between hold and cash repeatedly.
- **Boundary - Author exercise: One Day And Falling Prices.** Respect the no-transaction result.
- **Recognize - Author exercise: State Diagram.** Derive transitions before compressing them to scalars.
