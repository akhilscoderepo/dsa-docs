# Lesson spec: Build A Spanning Tree With Kruskal

**Recognition cue.** All weighted edges can be sorted and union-find is available. **Invariant.** Accepted edges form an acyclic forest; the next cheapest edge joining two components is safe.

- **Build - Author exercise: Sorted Safe Edges.** Union endpoints only when their roots differ.
- **Vary - Author exercise: Stop At V Minus One.** Finish when the forest becomes one tree.
- **Boundary - Author exercise: Equal Weights And Disconnection.** Allow any safe tie and report failure when components remain.
- **Recognize - LC 1584 Min Cost to Connect All Points.** Implement the Kruskal alternative and compare its edge-storage cost with Prim.
