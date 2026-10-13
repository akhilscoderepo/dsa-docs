# Lesson spec: Lazy Propagation

**Recognition cue.** Updates affect whole ranges and immediate descent would be too expensive. **Invariant.** A lazy tag records an update already applied to the node aggregate but not yet pushed to children.

- **Build - Author exercise: Range Add One Node.** Update aggregate by overlap length and store a pending delta.
- **Vary - Author exercise: Push Before Descent.** Transfer the tag to both children exactly once.
- **Boundary - Author exercise: Assignment Versus Addition Tags.** State composition order; they are not interchangeable.
- **Recognize - Author exercise: Range Add Range Sum.** Support both operations in logarithmic time.
