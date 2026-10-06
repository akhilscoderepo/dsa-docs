<!-- section: orientation -->
## Orientation

A fire-spread simulator reports ten minutes for a forest that burns out in four. A word-game solver needs seconds to connect two short words. A lock solver answers that a reachable code has no route. A maze solver with limited wall breaks answers "no path" on a maze that has one. Each program runs an ordinary breadth-first search, and each failure comes from what the search treats as one vertex, one step or one minute. This chapter changes those three decisions one at a time.

### Prerequisites

You should know the queue-based search of chapter 21, including marking a vertex when it enters the queue and the shortest-path argument for unweighted edges. Grids as graphs come from chapter 21 lesson 05, and hash sets and maps come from chapter 04. Code samples assume `import java.util.*;` and a recent JDK.

### The Five Lessons

Each lesson changes one decision of the plain search.

- **Start From Many Sources** puts every source in the queue at distance 0 before the first removal.
- **Count By Whole Layers** adds one to the time after a whole group of equal-distance vertices, not after each vertex.
- **Search From Both Ends** grows two searches and joins their distances where they meet.
- **Search States You Generate** builds neighbors from rules and puts every fact that changes the moves into the visited key.
- **Keep The Best Resource Left** stores the largest remaining budget per cell and discards a state only when another state is at least as good.

### The Combination Lesson

- **Model The State Before Searching** joins all five lessons through four questions: what the start set is, what the state key holds, what the moves are and what one layer means.

### How To Work Through Each Lesson

A lesson opens with a program that returns a wrong answer on a realistic input. It then shows the first version and asks you to predict its result. The next parts name the rule, list the state, follow two traces, show the code and mark where the rule stops working. The exercises climb from a basic version to a pattern recognition problem, labeled Build, Vary, Boundary or Recognize. Read the hint only after a real attempt.

### What You Can Do After This Chapter

You can seed a queue with many sources and read the answer per cell. You can say what one layer means before you add one to a counter. You can decide when two searches meet and when a state counts as already seen. You can list the edge cases before coding: no source, every cell a source, start equal to target, and a blocked start.

### What Later Chapters Reuse

Two ideas carry forward. A complete state key returns in chapter 24, where edges have weights. The rule that discards a state only with a proof returns whenever a search keeps more than one state per vertex.
