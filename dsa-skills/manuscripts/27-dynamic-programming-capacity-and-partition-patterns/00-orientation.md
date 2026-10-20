<!-- section: orientation -->
## Orientation

A game shop pays out loyalty points in tokens and its change routine hands out three tokens where two would do. A backup tool copies a file onto a disk twice because its table lets the file be chosen again. A cashier screen lists nine ways to pay five units when only four exist. Each program has a table with a sound meaning and one wrong choice in its loops. This chapter adds a capacity to the table state and shows how the direction of a loop and the owner of the outer loop decide what the table counts.

### Prerequisites

You should know the foundations chapter before this one. That chapter explained how to say in one sentence what a table entry means, how to seed the base entry, and how to read only entries that are already final. This chapter uses arrays of `int` and `long`, and it assumes `import java.util.*;` in code samples.

### The Seven Lessons

Each lesson fixes one decision about a table that is indexed by a total or a capacity.

- **Unbounded Coin Change** finds the fewest items for an exact total when every item can repeat. The table walks the totals upward, so a finished entry may already contain the same item.
- **Unbounded Knapsack** keeps a value for each capacity when items repeat and leftover capacity is allowed. Each entry compares skipping an item with taking one more copy.
- **Zero-One Knapsack** lets each item appear once. A one-dimensional table works only when the capacities are visited downward.
- **Partition State** records which sums a subset can reach. A subset is any choice of positions, and the question is whether one reaches half of the total.
- **Target Sum** turns a plus or minus choice for each number into a count of subsets. The derived goal is `(total + target) / 2`.
- **Combination Counts** counts unordered ways to reach a total. A combination is a choice of how many times each item is used.
- **Permutation Counts** counts ordered ways to reach a total. A sequence is a list in which the order of the items matters.

### The Closing Lesson

- **DP And Capacity** joins the two loop decisions and the combine rule into one procedure, and it shows what each wrong setting returns.

### How To Work Through Each Lesson

A lesson opens with a small program that returns a wrong or slow answer on a realistic input. A first version comes next, and you predict the output it prints. Later parts name the rule, list the variables, follow two traces, show the code and say when the rule stops fitting. Each lesson ends with four exercises that move through Build, Vary, Boundary and Recognize. Look at a hint only once you have really tried.

### What You Can Do After This Chapter

You can read a statement and decide whether items repeat, whether order counts and what the table entry must hold. You can choose the loop direction and the loop owner from those answers, and you can say which neighboring question a wrong choice answers. You can reduce signed sums to a subset count, and you can use `long` counts when the numbers grow.

### What Later Chapters Reuse

Chapter 28 adds a small label to each table entry, such as holding or not holding an item, and it reuses the habit of reading only the previous layer. Chapter 29 keeps tables over ranges of positions and reuses the seed and combine choices from this chapter. Bit tricks and number theory belong to a later chapter.
