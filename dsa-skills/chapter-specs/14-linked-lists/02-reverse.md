# Lesson spec: Reverse

**Recognition cue.** Every `next` edge must point to the previous node. **Invariant.** `prev` heads the fully reversed prefix, `curr` heads the untouched suffix, and no node is lost between them. **False friend.** Reassigning `curr.next` before saving its old successor disconnects the remaining list.

- **Build - Author exercise: Reverse Three Nodes By Hand.** Record `next`, redirect the edge, then advance both references.
- **Vary - LC 206 Reverse Linked List.** Apply the invariant until the untouched suffix is empty.
- **Boundary - Author exercise: Empty And One Node.** Return the correct head without special pointer rewiring.
- **Recognize - LC 92 Reverse Linked List II.** Reverse only a specified segment and reconnect both boundaries.
