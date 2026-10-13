# Lesson spec: Cut Forward History After A Write

**Recognition cue.** The class supports navigation through past state while new writes invalidate part of the future. **Invariant.** Stored elements and the current cursor jointly define the visible state.

- **Build - Author exercise: Undoable String Cursor.** Move backward and append after undo.
- **Vary - LC 1472 Design Browser History.** Truncate forward history after visiting a new page.
- **Boundary - Author exercise: Oversized Navigation.** Clamp movement without corrupting history.
- **Recognize - LC 2296 Design a Text Editor.** Combine cursor-local insertion/deletion with bounded context output.
