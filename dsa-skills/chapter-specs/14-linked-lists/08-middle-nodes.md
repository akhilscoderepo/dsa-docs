# Lesson spec: Middle Nodes

**Recognition cue.** A one-pass algorithm needs the midpoint without knowing length first. **Invariant.** Fast advances twice for each slow step; when fast reaches the end, slow has crossed half the nodes. **False friend.** Even-length lists have two middles, so the loop condition must match the requested one.

- **Build - Author exercise: Odd-Length Middle.** Trace slow and fast on five nodes.
- **Vary - LC 876 Middle of the Linked List.** Return the second middle for an even-length list.
- **Boundary - Author exercise: First Middle Contract.** Change the stopping condition to return the first of two middles.
- **Recognize - LC 234 Palindrome Linked List.** Find the midpoint before reversing and comparing the second half.
