<!-- section: orientation -->
## Orientation

A weather report lists a temperature for every day and asks how many days pass until a warmer one. A loop that scans forward from each day answers a year of data at once, but its cost grows with the square of the log length, so a decade of hourly readings is already slow. A bar chart asks for the largest rectangle that fits under its bars, and the same loop fails the same way. This chapter shows how one scan with a stack answers both questions, and why each value is looked at only a constant number of times.

### Prerequisites

You should know arrays, loops, the cost words from Chapter 00, and the stack from Chapter 11, including what `push`, `pop` and `peek` return. Each lesson defines its own terms the first time they matter. Code samples assume `import java.util.*;` and a recent JDK.

### The Seven Lessons

Each lesson adds one decision about when an index leaves the stack and what the method records at that moment.

- **Find The Next Greater Value** keeps indices whose answer is still unknown and removes the top when a larger value arrives.
- **Find The Next Greater In A Circle** scans the array twice by index arithmetic, so the last values can find answers at the front.
- **Compute The Stock Span** reads the same stack from the other side and measures how far back a price stays the largest.
- **Find Both Boundaries Of A Value** gets the nearest smaller index on each side from two scans, with a marker for a missing side.
- **Break Ties Between Equal Values** decides which of two equal values owns a shared range, so no range is counted twice or lost.
- **Count Subarrays By Their Minimum** turns the two boundaries into a count of ranges and adds up the minimum of every range.
- **Find The Largest Rectangle** turns the same boundaries into a width, and it adds a closing bar that empties the stack.

### The Combination Lesson

One lesson joins the stack with the counting lessons.

- **Count Subarrays From Stack Boundaries** computes the count and the contribution of each index at the moment it leaves, and it uses one loop for sums of minimums and of maximums, and its exercises add the rectangle.

### How To Work Through Each Lesson

Each lesson starts with a task that is easy to state and slow to run. A plain version follows, and a prediction question asks you to commit to an answer before the explanation opens. The remaining parts give the rule, the state, two traces, the code and a check of when the method does not apply. The exercises climb through four roles: Build, Vary, Boundary and Recognize. The line named Changed decision says what an exercise changes compared with the one before it.

### What You Can Do After This Chapter

You can tell from the wording of a problem whether it needs the next larger value, the next smaller value or both. You can choose which comparison removes equal values and explain the result for an array of equal values. You can compute widths and counts at the moment an index leaves, and you can add the closing step so that no index stays unresolved.

### What Later Chapters Reuse

Three ideas carry forward.

- **Resolve on removal** returns whenever an answer for an old item becomes known only when a newer item arrives.
- **One strict side and one non-strict side** returns whenever equal values must have exactly one owner.
- **A closing step that empties the structure** returns whenever pending items need a final answer after the input ends.
