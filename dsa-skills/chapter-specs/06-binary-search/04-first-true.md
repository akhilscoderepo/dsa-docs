# Lesson spec: First True

**Recognition cue.** A monotone predicate changes once from false to true. **Invariant.** `hi` remains a possible first true answer while discarded positions are proved false or cannot improve it. **False friend.** A non-monotone predicate cannot justify discarding half.

- **Build - Author exercise: First True Boolean.** Find the first `true` in `[false,false,true,true]`.
- **Vary - LC 278 First Bad Version.** Replace stored booleans with an oracle call.
- **Boundary - Author exercise: No True Value.** Define and return sentinel `n` when the contract permits all false.
- **Recognize - LC 1539 Kth Missing Positive Number.** The count of missing values by index is monotone and becomes a searchable predicate.
