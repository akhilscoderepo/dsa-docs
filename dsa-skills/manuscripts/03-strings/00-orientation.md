<!-- section: orientation -->
## Orientation

This chapter teaches seven techniques for strings in Java. You will learn to scan a string by index and stop at the right moment, to build a result without copying it over and over, to carry a small amount of state through a parse, to normalize before comparing, to count over a fixed alphabet, to write each run of equal characters once, and to find symmetric substrings by growing outward from a middle. Every technique comes with an invariant, a lookalike that fails, and a four-step practice ladder.

### What You Need Before Starting

You should have finished Chapters 00, 01 and 02 or be comfortable with their contents. That means reading a contract, writing a one-pass loop with a clear invariant, and using a write position that never passes a read position. You should know that a Java `String` is immutable, that `charAt` reads one `char`, and that a `char[]` can be changed in place. Hash maps, sliding windows and opposite-end pointer walks appear later in the course, and this chapter keeps them out on purpose.

### The Seven Lessons

Indexed scans come first because every other lesson reads characters by position. Safe construction shows why building a string by repeated concatenation is expensive and how a buffer fixes it. Parsing state carries a sign, a number or a depth across characters. Normalization cleans a string before comparing it. Fixed alphabet counts replace searching with a table of twenty-six counters. Run construction writes each block of equal neighbours once. Center expansion finds symmetric substrings from every middle.

### How To Work Through A Lesson

Begin with the story and the plain first version, and decide what is wasteful before the bottleneck section names it. String traces list the characters as cells, with index pointers marking where each step reads. Stop the stepper at the step that the text points to. Take the four exercises in order, write your own answer in the notes box before opening a hint, and read the solution last. Each solution contains Java that runs during the build with assertions against a slow but obviously correct oracle.

### Leaving The Chapter

After this chapter you should be able to read a string problem and say what is being scanned, what state summarises the part already read, what the output buffer holds, and what alphabet or symmetry promise is in force, together with the lookalike that fails. The review section turns that into recognition questions that are worth retaking after a few days.
