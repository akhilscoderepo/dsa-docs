<!-- section: orientation -->
## Orientation

A dashboard needs the total of every 10,000-minute block of a million readings, and the job adds up each block from scratch and never finishes. A cache study needs the longest run of requests that touches at most two different items, and the code collects items into a new set for every start index. A search page needs the shortest passage that contains every query word, and it reads the document forward from every word. Each program repeats work that the next block already did, because two neighbouring blocks share almost every element. This chapter answers one question: when two neighbouring blocks overlap, how does the answer for the second reuse the answer for the first?

### Prerequisites

You should know Java arrays, `String` methods such as `charAt`, `HashMap` with `merge` and `remove`, and the cost words of Chapter 00. Two earlier chapters help. Chapter 04 introduced counts kept in a map, and Chapter 08 introduced two indexes that move in one direction. This chapter explains the window, the running sum and each other term at the point where it first matters.

### The Nine Lessons

Each lesson fixes one rule for moving the two ends of a window and states what the window keeps true.

- **Slide A Window Of Fixed Size** updates a running sum with one entering and one leaving value.
- **Match Counts In A Fixed Window** keeps a count per character and compares counts.
- **Find The Longest Valid Window** moves the left end forward until the window is valid again.
- **Find The Shortest Covering Window** trims a window that already covers a requirement.
- **Limit A Window To K Distinct Values** keeps a map of counts and removes empty keys.
- **Count Exactly K By Subtraction** builds an exact count from two counts of at most.
- **Allow K Replacements In A Window** measures the cost of making a window uniform.
- **Count Every Valid Subarray** adds the number of valid starts for each end.
- **Shrink Fully Or Shrink Once** decides when the left end may move only once per step.

### The Combination Lesson

One lesson joins the boundaries of a window with a count of its contents.

- **Track Counts Inside A Window** separates what the boundaries add from what the counts add, and it keeps one counter that answers most rules in constant time.

### How To Work Through Each Lesson

Each lesson opens with a slow program and asks you to predict its cost before the answer appears. Two traces follow, with the window drawn above the data. Four exercises close the lesson, from the basic case to a problem that you must recognize from its wording, with a hint hidden until you ask. Try the hint only after you have written the state that the window keeps.

Each exercise carries one of four tags. Build asks you to write the basic loop of the lesson. Vary changes one rule of that loop and asks for the new loop. Boundary feeds the loop an input at its edge, such as an empty array or a limit of zero. Recognize hides the method behind the wording of a real problem. Each exercise also names a changed decision, which is the one choice that differs from the lesson loop. Lessons also call the window a block, a span, a range or a run. A false friend is a tempting method that fails or wastes effort, and every lesson names one in a heading of its own.

### What You Can Do After This Chapter

You can state, before you write the loop, what the window holds and what each stored number means. You can choose between a fixed window, a longest window, a shortest window and a counting window from the wording of a problem. You can name the input that breaks each rule, such as a negative value in a sum, a window that must stay valid when it records, or a count of zero that stays in a map. You can explain why `while` is not replaceable by `if` in general, and for which problem the replacement is proved safe.
