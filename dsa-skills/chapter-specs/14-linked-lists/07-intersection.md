# Lesson spec: Find Where Two Lists Meet

**Recognition cue.** Two acyclic lists may share the same tail nodes by reference. **Invariant.** Switching each pointer to the other head makes both traverse equal total distance before meeting or reaching null. **False friend.** Equal node values are not an intersection.

- **Build - Author exercise: Compare Node Identity.** Distinguish two separate nodes holding the same value.
- **Vary - Author exercise: Align By Length.** Advance the longer list by the length difference, then move together.
- **Boundary - Author exercise: No Intersection And Shared Head.** Verify both null meeting and immediate identity.
- **Recognize - LC 160 Intersection of Two Linked Lists.** Use head switching for constant-space alignment.
