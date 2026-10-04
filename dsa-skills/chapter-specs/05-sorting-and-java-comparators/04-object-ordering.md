# Lesson spec: Sort Objects By Several Fields

**Recognition cue.** The thing being ordered has several fields and a stated priority. **State.** The comparator encodes the contract, including tie ownership. **Java hazard.** `Comparator` applies to objects such as `int[][]`, not `int[]` elements directly.

- **Build - Author exercise: Sort Scores.** Sort `Student(name, score)` by score, then name.
- **Vary - LC 937 Reorder Data in Log Files.** Compare identifier only after content ties.
- **Boundary - Author exercise: Equal Primary Keys.** State the secondary tie rule rather than relying on current order.
- **Recognize - LC 406 Queue Reconstruction by Height.** The first sort key makes insertion-by-position meaningful.
