<!-- section: orientation -->
## Orientation

Two pointers is the habit of keeping two positions in one sequence and letting each comparison retire a whole group of possibilities, so that a scan which looks quadratic needs a single pass. The chapter shows that the habit comes in several different shapes. Two ends walk toward each other over sorted data, one reader runs ahead of one writer, a boundary sweeps a pivot across an array, three regions share one array, a fixed value is combined with a pair scan, and a slow and a fast walker chase each other through links hidden in an array. Each shape is safe only because of a specific promise about the data.

### What You Need Before Starting

You should have finished Chapters 00 to 07, or be comfortable with their content: stating a contract before coding, naming a loop invariant, working with arrays and strings in place, sorting with Java comparators, halving an interval with a proof, and remembering that `int` sums can wrap. Sliding windows, greedy choice and linked-list pointer tricks are named only as later destinations, and no exercise here depends on them.

### The Ten Lessons

The first lesson scans a sorted array from both ends and shows why one comparison discards one endpoint for good. The second lesson separates a reader from a writer to compact an array. The third and fourth lessons split an array into two regions and then three, trading order for fewer moves. The fifth lesson governs how equal values are skipped, and the sixth lesson uses that rule to fix one, two or more leading values before a pair scan. The seventh lesson follows array values as links to find where a walk enters a cycle. The last three lessons join pairs of ideas: sorting with pointers, strings with pointers, and index storage with the cycle walk.

### How To Work Through A Lesson

Each lesson opens with a small story and a plain method. Before reading the bottleneck, guess which work the plain method repeats. The traces show every pointer position of a concrete input, and the text names one step worth studying. Try the exercises in order, write the invariant on paper before opening a hint, and note whether the exercise allows you to change the input. Every solution comes with Java that is compiled and run in the build against a slower, obviously correct oracle on many random inputs.

### Leaving The Chapter

By the end you should be able to look at a problem and say which two positions you keep, what the region between or behind them promises, which move is safe and why the data makes it safe, and what happens when the pointers meet, cross or run out of input. You should also recognize the cases where the data offers no such promise, so that moving a pointer would only be a guess. The review section checks these habits with short scenarios and is worth revisiting after a few days.
