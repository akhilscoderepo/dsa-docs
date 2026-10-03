<!-- section: orientation -->
## Orientation

A sliding window is a stretch of a sequence whose two edges only ever move forward, together with a small summary of what the stretch currently holds. Because the summary is updated by one entering item and one leaving item, a problem that seems to ask about every possible stretch can be answered in a single pass. This chapter teaches when that trade is legal, and what the summary has to look like in each family of problems.

### What You Need Before Starting

You should have finished Chapters 00 to 08, or be comfortable with their content: stating a contract, keeping count arrays and hash maps of frequencies, building prefix sums, moving two pointers with an invariant, and remembering that `int` totals can wrap. Deques that keep the best candidate of each window are named only as a later destination, and no exercise here uses them.

### The Ten Lessons

The first two lessons fix the window length. One sums numbers or flags as the window slides, and the other compares letter counts. The third lesson lets the length vary and shrinks the window whenever a rule breaks. The fourth lesson finds the shortest stretch that covers a demand. The fifth and sixth lessons limit distinct values, and show how to count stretches with exactly k of something by subtracting two at-most answers. The seventh lesson spends a replacement budget, the eighth counts every valid stretch instead of the longest, and the ninth compares shrinking with a loop against a proved non-shrinking policy. The tenth lesson joins windows with frequency counts.

### How To Work Through A Lesson

Each lesson opens with a short story and a plain method. Before reading the bottleneck, guess which work the plain method repeats. The traces show both edges and the summary at every step, and the text names a step to study. Try the exercises in order, write down the window invariant before you open a hint, and decide in advance what makes a window valid and what removal can repair it. Every solution has Java that is compiled and run in the build against a slower oracle that checks every stretch.

### Leaving The Chapter

By the end you should be able to say what the summary of a window holds, what makes it valid, why moving the left edge can only repair and never ruin validity, and when the answer is recorded. You should also be able to tell when a window is the wrong tool, for example when values can be negative and shrinking no longer repairs a sum. The review section tests these habits with scenarios and is worth returning to after a few days.
