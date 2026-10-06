# Lesson spec: Search States You Generate

**Recognition cue.** Vertices are not listed explicitly; legal operations generate neighboring states. **Invariant.** The state encoding contains every fact that affects future moves, and visited uses that complete encoding. **False friend.** Marking only a visible location is wrong when inventory, mask, or mode changes future options.

- **Build - Author exercise: Combination-Lock States.** Generate one-wheel turns from a string state.
- **Vary - LC 752 Open the Lock.** Avoid deadends and return minimum turns.
- **Boundary - Author exercise: Forbidden Start And Target.** Apply the problem's dead-state contract before enqueueing.
- **Recognize - LC 1091 Shortest Path in Binary Matrix.** Recognize coordinates as an implicit state space with uniform moves.
