# Lesson spec: Version Histories

**Recognition cue.** Updates create versions and later queries name an earlier version or time. **Invariant.** Each index/key stores a monotone history; a query selects the latest change not after the requested version.

- **Build - Author exercise: Versioned Integer.** Append `(version,value)` changes.
- **Vary - LC 1146 Snapshot Array.** Store only changed indices per snapshot.
- **Boundary - Author exercise: Equal Versions Replace.** Coalesce writes with the same version.
- **Recognize - LC 981 Time Based Key-Value Store.** Binary-search per-key timestamp histories.
