# Lesson spec: Matrix Rotation

**Recognition cue.** A square matrix must be transformed in place. **Invariant.** Transposition swaps each off-diagonal pair once; reversing each row then completes a clockwise rotation. **False friend.** A rectangular matrix cannot be rotated in place into the same dimensions.

- **Build - Author exercise: Transpose Square.** Swap `matrix[r][c]` with `matrix[c][r]` only for `c > r`.
- **Vary - LC 48 Rotate Image.** Transpose, then reverse each row.
- **Boundary - Author exercise: Odd Center.** Show why the center of a `3 x 3` matrix remains valid without special movement.
- **Recognize - Author exercise: Counterclockwise Rotation.** Transpose, then reverse columns; name the changed transformation.
