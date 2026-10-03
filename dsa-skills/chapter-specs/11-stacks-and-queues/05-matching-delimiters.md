# Lesson spec: Matching Delimiters

**Recognition cue.** Every closing symbol must match the most recent unresolved compatible opening symbol. **Invariant.** The stack stores exactly the openings not yet matched, in nesting order. **False friend.** Equal counts do not prove correct order.

- **Build - Author exercise: One Bracket Type.** Validate parentheses by pushing openings and resolving closings.
- **Vary - LC 20 Valid Parentheses.** Match three delimiter types against the stack top.
- **Boundary - Author exercise: Premature Close And Leftover Open.** Reject both an empty-stack close and a nonempty stack after the scan.
- **Recognize - LC 1021 Remove Outermost Parentheses.** Use nesting depth to omit the first opening and final closing of each primitive group.
