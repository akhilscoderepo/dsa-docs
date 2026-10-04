# Lesson spec: Heap Scheduling

**Recognition cue.** Items become eligible over time, and the best eligible item must be selected by a second priority. **Invariant.** After advancing time and adding all released tasks, the heap contains exactly the executable tasks. **False friend.** One global sort cannot generally express both release time and dynamic selection priority.

- **Build - Author exercise: Released Shortest Job.** Sort by release time and heap-select the shortest available job.
- **Vary - LC 1834 Single-Threaded CPU.** Add index tie-breaking and jump time when no task is available.
- **Boundary - Author exercise: Idle Gap And Simultaneous Releases.** Advance directly to the next release and enqueue every tie before selecting.
- **Recognize - LC 1882 Process Tasks Using Servers.** Coordinate available-resource and busy-resource heaps.
