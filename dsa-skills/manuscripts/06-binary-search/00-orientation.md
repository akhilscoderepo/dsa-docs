<!-- section: orientation -->
## Orientation

A login service scans a sorted list of one million banned addresses for every request, and the check takes longer than the rest of the request. A support tool returns "not found" for a value that sits in a rotated list. A shipping planner tests every capacity from 1 upward, and a single plan takes a minute. In each case the data or the answer space has order, and the program reads it one item at a time. This chapter answers one question: when does an ordered range let one comparison discard half of what remains, and how does the loop keep that claim true?

### Prerequisites

You should know Java loops and arrays, the cost words of Chapter 00, and the lookup methods of Chapter 04 for the map lesson. Chapter 05 helps, since every search here assumes sorted input and sorting comes from there. The chapter writes its own midpoint formula and does not call `Arrays.binarySearch` except to show where it misleads.

### The Nine Lessons

Each lesson fixes one meaning of the search interval and one rule for moving its ends.

- **Find A Value In Sorted Data** keeps a closed interval and discards each compared index.
- **Find The First Or Last Match** keeps a candidate when duplicates exist and moves toward one side.
- **Find Where A Value Belongs** returns a boundary index from zero to `n` and not a matching cell.
- **Find The First True Value** searches a monotone yes-or-no test and names the change point.
- **Find A Peak By Slope** reads the slope between neighbors to pick the side that holds a peak.
- **Find The Minimum After Rotation** compares the middle value with the right end to find the restart.
- **Find A Target After Rotation** names the sorted half first and tests the target against it.
- **Search Whole Number Answers** runs the search over candidate answers and not over input positions.
- **Search Real Number Answers** halves a real interval and stops by a fixed round count.

### The Two Combination Lessons

Two lessons join the search with earlier chapters, and each opens with a failure that the pairing fixes.

- **Look Up Values By Time** pairs a map from keys to lists with a search for the last entry at or before a time.
- **Search A Sorted Matrix** converts one number into a row and a column, and it contrasts that with a walk across sorted rows and columns.

### How To Work Through Each Lesson

Each lesson starts from a case where the simple approach breaks, and a short prediction asks you to guess the cost or the cause before the answer appears. A step-through trace shows the interval ends as they change. Four exercises close each lesson, and they grow from the plain case to a pattern you must recognize. Hints and solutions stay hidden until you open them, so make an attempt first. An exercise labeled Author exercise was written for this course. An exercise with a LeetCode number follows that problem, and its text states every rule that it changes.

### What You Can Do After This Chapter

You can state, before writing a loop, what the interval holds and which end each comparison moves. You can pick between a closed interval and a half-open one and defend the choice with the loop test. You can turn a question about a quantity into a yes-or-no test and check that the test never flips back. You can name the inputs that break a search: duplicates, an empty array, a missing answer, a midpoint that overflows, a rotated array with repeated values, and a real interval that stops shrinking.
