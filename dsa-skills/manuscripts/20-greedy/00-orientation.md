<!-- section: orientation -->
## Orientation

A placement service puts a small job on its biggest server and then cannot place the next large job. A room booking system accepts one long meeting and turns away three short ones. A relay simulator tries every forwarding route and never finishes on a line of thirty stations. A batch runner keeps a long job that blocks two short jobs. Each program makes a decision, and a later decision pays for it. This chapter teaches how to make a decision once, never revisit it, and still get the best answer, together with the short argument that shows it is safe.

### Prerequisites

You should know arrays, sorting with a comparator and the two-pointer scan. Chapter 05 taught sorting with comparators, which every lesson uses to expose the next item. Chapter 08 taught pointers that move in one direction, which lesson 01 and lesson 03 reuse. Chapter 10 taught intervals, and lessons 02 and 04 build on the half-open model. Chapter 17 taught the heap, which lesson 05 uses to drop the longest retained task. Code samples assume `import java.util.*;` and a recent JDK.

### The Five Lessons

Each lesson adds one reason that a single committed choice is safe.

- **Local Choice** sorts both sides and gives the smallest sufficient resource to the smallest demand.
- **Interval Scheduling** orders requests by end time so that each accepted request leaves the most free time.
- **Farthest Frontier** replaces every forwarding route with one number, the farthest index that is reachable.
- **Exchange Reasoning** states the four parts of a proof and searches for an input that breaks a false rule.
- **Task Selection** keeps a set of tasks that can shrink, and drops the longest task when a deadline fails.

### The Combination Lesson

One lesson joins ordering with the proof.

- **Sort Then Commit Greedily** finds the one number that an exchange step compares, orders the items by it, and applies the same loop to cookies, gapped intervals, balloons and a log stream cut into parts.

### How To Work Through Each Lesson

A lesson opens with a program that fails on a realistic input, then shows the obvious version and asks you to predict its result. The next parts name the rule, list the state, follow two traces, show the code and mark where the rule stops working. The exercises climb from a basic version to a pattern recognition problem. A bracketed role labels each exercise: Build, Vary, Boundary or Recognize. Read the hint only after a real attempt.

### What You Can Do After This Chapter

You can say why a committed choice is safe in four sentences. You can pick the sort key by asking which attribute of the next item costs the others room. You can tell when a sort alone is enough and when a later item must push an earlier one out. You can list the edge cases before coding: empty input, equal keys, touching endpoints and sums that pass the `int` range.

### What Later Chapters Reuse

Three ideas carry forward.

- **State the invariant before the loop** returns wherever a loop commits and never looks back.
- **Compare by one key with `Integer.compare`** returns wherever a sort decides which item goes first.
- **Eject the worst retained item** returns wherever a heap keeps a bounded best set.
