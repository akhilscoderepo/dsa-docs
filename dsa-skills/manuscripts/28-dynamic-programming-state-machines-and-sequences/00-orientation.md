<!-- section: orientation -->
## Orientation

A trading report sells a share on the day before it buys it. A diff tool lists three changes where one would turn "abc" into "bc". A spell checker rates a word as far from its correction because it counts only matching letters in the same positions. Each program leaves out one fact: what situation a table entry describes. This chapter labels every table entry with that situation, such as holding a share or having used one of two trades, and then fills tables over two strings or over the ends of one string.

### Prerequisites

You should know the two previous dynamic programming chapters. They explained how to state in one sentence what a table entry means, how to seed the base entry, and how to read only entries that are already final. The code uses arrays of `int` and `String`, and it assumes `import java.util.*;` in samples.

### The Six Lessons

Each lesson fixes one question about what an entry remembers.

- **Stock States** keeps two values per day, the best cash while holding a share and the best cash while holding none. A mode is a named situation that limits the next move.
- **Transaction Variants** adds a waiting day, a fee or a trade count to the mode, so the rule becomes part of the state.
- **Increasing Subsequences** finds the longest strictly rising choice of elements, first with a quadratic table and then with a short array of smallest tails.
- **Common Subsequences** compares two strings with a table indexed by two prefix lengths.
- **Edit Distance** counts the fewest insertions, deletions and replacements that turn one string into another, using the same two-prefix table.
- **Palindromic Sequences** moves to a table indexed by the two ends of one string and fills it by growing range length.

### The Closing Lesson

- **DP State Machines** joins the mode idea and the trade count into one table of labeled states and shows why one number per day loses the answer.

### How To Work Through Each Lesson

A lesson opens with a small program that returns a wrong or slow answer on a realistic input. It shows a first version and asks you to predict its output. Later parts name the rule, list the variables, follow two traces, show the code and say when the rule stops fitting. Four exercises close each lesson, and they climb through Build, Vary, Boundary and Recognize. Read a hint only after a real attempt.

### What You Can Do After This Chapter

You can list the legal moves of a problem and turn them into a table whose entries carry a label. You can choose between a prefix table, a range table and a tails array from the shape of the question. You can fill a two-index table in an order that finishes every needed entry first, and you can recover one optimal answer from it.

### What Later Chapters Reuse

Chapter 29 reuses the range table from the last lesson and adds states such as ranges of positions, digits and bit masks. Every later table problem reuses the habit of writing the meaning of an entry before writing a loop.
