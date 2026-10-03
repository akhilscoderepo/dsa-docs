# Lesson spec: Boundary Discovery

**Recognition cue.** Each element's valid region ends at the nearest smaller or greater element on both sides. **Invariant.** One scan determines a nearest boundary when an index is popped; a reverse scan or surviving top supplies the other boundary under the chosen comparison. **False friend.** The boundary value alone is insufficient when width or number of choices depends on distance.

- **Build - Author exercise: Previous Smaller Index.** Store indices in increasing value order and report the surviving top.
- **Vary - Author exercise: Next Smaller Index.** Resolve indices when a smaller current value arrives.
- **Boundary - Author exercise: No Boundary.** Use sentinels `-1` and `n` consistently when no smaller element exists.
- **Recognize - Author exercise: Widest Region Where Each Value Is Minimum.** Combine left and right boundaries into width `right - left - 1`.
