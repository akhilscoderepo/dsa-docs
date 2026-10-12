# Lesson spec: Transition Discipline

**Recognition cue.** A recurrence is known, but in-place loop order can accidentally reuse current-iteration state. **Invariant.** Every read comes from the intended logical layer.

- **Build - Author exercise: Separate Previous Row.** Compute a new layer from an immutable old layer.
- **Vary - Author exercise: Update One Row In Place.** Explain which neighbor is current-row and which is prior-row.
- **Boundary - Author exercise: Aliased Arrays.** Show why assigning `next = current` destroys layer separation.
- **Recognize - LC 931 Minimum Falling Path Sum.** Use explicit prior-row ownership or safe update storage.
