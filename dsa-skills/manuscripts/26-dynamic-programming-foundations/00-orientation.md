<!-- section: orientation -->
## Orientation

A shipping tool counts the ways to split a load into crates of 2 or 3 units. It answers for 12 units in a blink and then runs all night for 40. A route planner counts the paths a robot can take across a 20 by 20 floor and returns a number that is far too small. An inventory script that should save memory overwrites a value it still needs and reports a wrong total. Each program has a correct idea and a broken bookkeeping step. This chapter teaches dynamic programming, which is a way to answer a big question by storing the answers to smaller questions of the same kind, and it teaches how to keep that storage honest.

### Prerequisites

You should know recursion and arrays from the early chapters, and two-dimensional arrays for the grid lessons. Chapter 25 ended with distance tables whose entries become final after ordered rounds, and this chapter builds on that habit. Code samples assume `import java.util.*;` and a recent JDK.

### The Eight Lessons

Each lesson fixes one rule about the table that holds the answers.

- **Define What Each Table Entry Means** writes one sentence that says what `dp[i]` returns. A subproblem is a smaller question of the same kind, and the state is the smallest set of values that decides its answer.
- **Cache Results Or Fill A Table** removes repeated work in two ways. Memoization keeps the recursion and stores finished answers, and tabulation fills an array in dependency order.
- **Linear Recurrence** computes each entry from a fixed number of earlier entries. A recurrence is a rule that builds one entry from entries with smaller indexes.
- **Take Or Skip** compares leaving an item out with including it and giving up its neighbor. A prefix is the first `i` items of the input.
- **Rolling State** replaces the table with a few variables when the recurrence reads only recent entries. The window is the set of entries that later steps can still read.
- **Objective Types** keeps one table layout and changes the base value and the combine rule. The three questions are whether a goal is reachable, how many ways reach it, and the smallest cost to reach it.
- **Grid DP** stores one number for each cell and fills the cells in an order that finishes every predecessor first. A predecessor is a cell from which one allowed move reaches the current cell.
- **Transition Discipline** makes every read come from the previous layer. A layer is the full set of values for one step, such as one grid row.

### The Combination Lesson

- **Recursion And Memoization** turns the arguments of a recursive call into cache keys, so a recursion over stairs, houses and a grid computes each distinct question once.

### How To Work Through Each Lesson

A lesson opens with a program that gives a wrong or slow answer on a realistic input. It then shows a first version and asks you to predict its result. The next parts name the rule, list the variables, follow two traces, show the code and say when the rule stops fitting. Four exercises close each lesson, and they climb through Build, Vary, Boundary and Recognize. Read a hint only after a real attempt.

### What You Can Do After This Chapter

You can write the meaning of a table entry in one sentence before you write a formula. You can pick memoization or a loop, and you can shrink a table to a few variables when the window allows it. You can solve stairs, house and grid problems for counting, feasibility and minimum cost, and you can spot a loop that reads a value from the wrong layer.

### What Later Chapters Reuse

Chapter 27 adds a capacity to the state and decides, from the loop direction, whether an item can be used once or many times. That chapter reuses the sentence that defines an entry, the choice of base value and combine rule, and the layer rule from this one. Knapsack, state machines, interval problems and subsequence problems are not part of this chapter.
