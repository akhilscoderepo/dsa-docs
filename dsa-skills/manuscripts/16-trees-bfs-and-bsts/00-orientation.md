<!-- section: orientation -->
## Orientation

A chat app lists people by the floor they sit on, and the list mixes floors. A phone-book lookup misses a name that is clearly stored. A help desk waits several seconds for the next ticket number. A saved game reloads with a branch on the wrong side. Each program keeps its data in a binary tree, and each failure comes from one wrong assumption about what the tree guarantees. This chapter shows how to read a tree row by row with a queue, how the order of a search tree lets one comparison skip half the data, and how to turn a tree into text and back.

### Prerequisites

You should know loops, recursion and the cost words from Chapter 00. Chapter 11 introduced queues and stacks, and the row loop and the stack walks of this chapter use both through `ArrayDeque`. Chapter 15 introduced the tree node with a left and a right reference and the three recursive walk orders. Each lesson defines its own terms the first time they matter. Code samples assume `import java.util.*;` and a recent JDK, and every tree node is a small class with a `val` field and two child references.

### The Nine Lessons

Each lesson adds one rule that turns a tree question into a short loop or a short recursion.

- **Read A Tree Level By Level** puts nodes in a queue and stores the row size before each row.
- **Carry Value Limits Down A Search Tree** checks every node against limits from all of its ancestors.
- **Search And Insert With One Path** follows one branch per comparison to find, add or remove a key.
- **Find The Next And Previous Key** finds the neighbors of a key in sorted order from one walk down the tree.
- **Answer Rank And Range Questions** reads keys in sorted order and skips subtrees that cannot matter.
- **Find The Lowest Common Ancestor** finds the deepest shared ancestor of two nodes, with and without key order.
- **Hand Out Tree Keys On Demand** keeps the unfinished path on a stack so each request costs little.
- **Turn A Tree Into Text And Back** writes empty slots as markers so one text rebuilds exactly one tree.
- **Keep A Search Tree Short** explains why height decides the cost and how a rotation keeps the order.

### The Combination Lessons

Two lessons join ideas that the chapter has already taught.

- **Group Nodes By Depth With A Queue** joins the tree with the queue, and it works for nodes with any number of children.
- **Search And Validate A Search Tree** joins the one-path search with the value limits, so one pass replaces a lookup for every node.

### How To Work Through Each Lesson

Each lesson begins with a program that fails or slows down on a real input, and then shows a plain version that works but costs too much. A prediction question follows, and you commit to an answer before the explanation opens. The remaining parts give the rule, the state, a step-by-step trace, the code and a check of when the method does not apply. The exercises climb from a basic version to a full interview problem. Each exercise has a role in brackets, either Build, Vary, Boundary or Recognize. Each exercise also lists a Changed decision, which names the one choice that differs from the exercise before it, and the tag Author exercise marks a problem written for this chapter. Try the hint before you read a solution.

### What You Can Do After This Chapter

You can say, for any tree question, whether it asks for rows, for sorted order, for a single key or for the whole structure, and you can pick the matching loop. You can state what a search tree promises about every descendant of a node, and you can name the check that proves it. You can read a tree problem and list its edge cases before you code: the empty tree, the chain, the equal keys and the keys at the extremes of `int`.

### What Later Chapters Reuse

Three ideas carry forward.

- **Store the row size first** returns whenever a later structure is read in rounds and each round must stay separate.
- **Pass the limits down** returns whenever a property must hold between a node and all of its ancestors.
- **Write the empty slots too** returns whenever a structure must be saved as a sequence and rebuilt without guessing.
