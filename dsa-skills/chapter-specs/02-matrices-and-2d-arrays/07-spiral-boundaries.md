# Lesson spec: Walking A Matrix In Spiral Order

**Recognition cue.** Output consumes a rectangle layer by layer. **Invariant.** `top`, `bottom`, `left`, and `right` enclose exactly the unvisited rectangle. **False friend.** Direction-state simulation and shrinking-boundary traversal can produce similar output, but their state and failure modes differ.

- **Build - Author exercise: One Ring.** Emit the perimeter of a rectangular matrix without repeating corners.
- **Vary - LC 54 Spiral Matrix.** Repeatedly consume top row, right column, bottom row, and left column.
- **Boundary - LC 54 Thin Remainder.** Guard the bottom and left passes when only one row or one column remains.
- **Recognize - LC 59 Spiral Matrix II.** Reverse the data flow: generate values into the same shrinking layers.
