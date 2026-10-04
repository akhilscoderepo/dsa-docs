# Lesson spec: Build Strings With StringBuilder

**Recognition cue.** The output is built incrementally. **State.** A `StringBuilder` contains exactly the completed output prefix. **Java hazard.** Repeated `+` in a loop creates repeated immutable strings. **False friend.** Do not use `StringBuilder.insert(0, ...)` for reversal; it turns linear work quadratic.

- **Build - Author exercise: Remove Spaces.** Return `s` without spaces using a `StringBuilder`.
- **Vary - LC 151 Reverse Words in a String.** Build the final words with explicit separator ownership.
- **Boundary - Author exercise: Empty Result.** `"   " -> ""`; never leave a trailing separator.
- **Recognize - LC 6 Zigzag Conversion.** Builders own the independently constructed rows.
