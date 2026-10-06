<!-- section: orientation -->
## Orientation

A test that lists every ordering of four inputs prints the same list ten times. A subset generator returns lists that are all empty when it finishes. A puzzle app says that a word is missing from a grid, although the word is there. An invoice matcher runs for minutes on thirty invoices. Each program explores many branches while it shares one list, one array of flags or one grid of marks. This chapter shows how a program changes the shared state before a branch, restores it after the branch, and skips a branch when it can prove that the branch fails.

### Prerequisites

You should know loops, arrays and the `ArrayList` and `HashSet` classes. Chapter 03 introduced strings, `substring` and character arithmetic, which the cutting lesson and the board lesson use. Chapter 02 introduced grids and the four neighbours of a cell, which the last lesson uses. Chapter 15 introduced recursion on trees, so a call that makes calls is not new, although this chapter calls a method on arguments that describe a smaller task. Chapter 18 introduced the prefix tree, which the last lesson needs. Code samples assume `import java.util.*;` and a recent JDK.

### The Ten Lessons

Each lesson names one rule that keeps a search correct or keeps it small.

- **Shrink The Problem With Each Call** states what a call receives and promises, and why every call must move toward an answer it can return directly.
- **Undo Each Choice After Exploring It** shares one list between branches, removes each choice after its branch and stores a copy of every finished list.
- **List Every Subset** passes a start index to each call so that a set appears in one order and every call stores a result.
- **List Every Ordering** marks the indices that earlier positions hold and clears the mark when a branch ends.
- **Choose K Values Without Reordering** stops a path at a fixed size and ends each loop where too few indices remain.
- **Reuse A Value In A Sum** passes the same start to the child, so one value may repeat while the order stays fixed.
- **Skip Equal Values At One Level** compares a value with its left neighbour inside one loop, and keeps equal values at different depths.
- **Stop A Branch You Can Prove Fails** skips a branch only when a rule about the input shows that no extension can succeed.
- **Cut A String Into Pieces** chooses where the next piece ends and stores a result only when no letter remains.
- **Mark Cells On A Grid** marks the cells of one path, clears each mark on the way out and rejects a queen by its column and diagonals.

### The Board Lesson

One lesson joins this chapter with the chapter on prefix trees.

- **Search A Board With A Prefix Tree** carries a tree node along the marked cells of a path, stops at a missing edge and reports each word once.

### How To Work Through Each Lesson

Every lesson begins with a program that fails or crawls on a real input. A plain version follows, and then a prediction question asks for a number before the answer opens. The next parts name the rule, list the state, trace a small run, show the Java code and describe where the rule stops helping. Each lesson ends with four exercises. A role in brackets labels each exercise. Build writes the new idea, Vary changes one decision, Boundary protects an edge case and Recognize applies the idea to a problem that does not name it. The line Changed decision states what differs from the exercise above it. The tag Author exercise marks a problem written for this chapter. Read the hint before you open a solution.

### What You Can Do After This Chapter

You can write the contract of a recursive method before its body. You can tell whether a question asks for subsets, orderings, selections of a fixed size, sums with reuse, cuts of a string or paths on a grid. You can say which state each call changes and where the program restores it. You can list the edge cases before you code: the empty input, a path that is already full, a value larger than the remaining target, equal values at different depths and a mark that a return forgot to clear.

### What Later Chapters Reuse

Three ideas carry forward.

- **Change, explore, restore** returns wherever a search shares one structure between branches, such as the path marks of the graph chapters.
- **Name the call state** returns in the dynamic programming chapters, where equal states must have equal answers before a program may remember them.
- **Prove each skip** returns wherever a search stops early, including the shortest path and optimization chapters.
