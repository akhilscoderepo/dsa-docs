# Lesson spec: Track The Minimum In A Stack

**Recognition cue.** Ordinary stack operations must additionally return the current minimum in constant time. **Invariant.** Each depth stores enough information to recover the minimum for exactly that prefix of the stack. **False friend.** Scanning for the minimum on demand violates the operation contract.

- **Build - Author exercise: Value-Min Pairs.** Push each value with `min(value, previousMin)`.
- **Vary - Author exercise: Two-Stack Minimum.** Store a value on the minimum stack when it is no greater than the current minimum.
- **Boundary - Author exercise: Duplicate Minima.** Push the same minimum twice and ensure one pop does not lose it.
- **Recognize - LC 155 Min Stack.** Implement `push`, `pop`, `top`, and `getMin` with constant-time worst-case operations.
