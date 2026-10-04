# Lesson spec: Path Enumeration

**Recognition cue.** The output needs every source-to-target path, not only reachability. **Invariant.** The working path contains exactly the current recursion chain and is restored after each neighbor. **False friend.** Global visited state can incorrectly forbid a vertex appearing in different valid paths of a DAG.

- **Build - Author exercise: Paths In A Tiny DAG.** Append a neighbor, recurse, then remove it.
- **Vary - LC 797 All Paths From Source to Target.** Copy the path whenever the target is reached.
- **Boundary - Author exercise: Dead End And Direct Edge.** Record only complete target paths.
- **Recognize - Author exercise: Enumerate Simple Paths.** Add path-local visited state when cycles are permitted.
