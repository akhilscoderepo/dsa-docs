# Lesson spec: Multi-Index Records

**Recognition cue.** The same entity must support lookup by ID and ordered/filter views by mutable attributes. **Invariant.** Authoritative record state and every secondary index describe exactly the same live entities.

- **Build - LC 2349 Design a Number Container System.** Map index to number and number to ordered indices.
- **Vary - LC 2353 Design a Food Rating System.** Order by rating with deterministic name tie-breaking.
- **Boundary - Author exercise: Update To Same Value.** Avoid duplicate index entries and unnecessary removal.
- **Recognize - LC 1912 Design Movie Rental System.** Maintain available and rented views over shared records.
