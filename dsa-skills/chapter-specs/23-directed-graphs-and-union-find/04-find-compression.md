# Lesson spec: Find Compression

**Recognition cue.** Repeated operations ask which dynamically merged component contains an element. **Invariant.** Parent links lead to one representative root; path compression rewrites searched paths without changing membership. **False friend.** Union-find does not enumerate paths or support arbitrary edge deletion.

- **Build - Author exercise: Follow Parents To Root.** Implement `find` without compression.
- **Vary - Author exercise: Compress A Chain.** Point every visited node directly to the root.
- **Boundary - Author exercise: Singleton Components.** A node initially represents itself.
- **Recognize - LC 547 Number of Provinces.** Union connected cities and count remaining representatives.
