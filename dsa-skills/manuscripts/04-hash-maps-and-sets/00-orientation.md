<!-- section: orientation -->
## Orientation

This chapter teaches seven ways to use hash sets and hash maps, and then two combinations that use them with earlier chapters. You will learn to ask whether a value has appeared, to keep an exact count per key, to remember where a value was seen, to keep the members of each group, to reason about runs of numbers by membership alone, to build keys from several fields, and to recognise when a plain array is the better table. The point is never to reach for a `HashMap` by habit. Each structure earns its place by storing exactly the information the next decision needs, and each lesson names what the key means, what the value means, and why order does not matter.

### What You Need Before Starting

You should have finished Chapters 00 to 03 or be comfortable with their contents. That means reading a contract, writing a one-pass loop with an invariant, using a frequency array over a small alphabet, and scanning strings and matrices by index. You should know the basic Java collections interfaces, that `Integer` and `int` are different types, and that a `char` can be subtracted from another. Sorting, two pointers, sliding windows and binary search appear in later chapters, and this chapter leaves them out on purpose.

### The Nine Lessons

Membership sets come first, since the simplest question is whether something has appeared. Frequency maps add the count, and key-to-index maps add the position. Grouping maps keep the members of each class and not just their number. Set sequences use membership of neighbouring values to find runs without sorting. Key equality shows how to build compound keys safely in Java, including the hazards of arrays and mutable fields. Direct addressing shows when an array is the simpler and faster table. The two combination lessons then join strings with maps, for counting and for two-way pairings, and matrices with sets, for uniqueness inside overlapping scopes.

### How To Work Through A Lesson

Take in the story and the plain first version, and work out what is wasteful before the bottleneck section confirms it. Traces show the contents of the set or map after every step, which lets you check a prediction. Halt the stepper at the step that the text highlights. Do the four exercises in order, type your own answer into the notes box before opening the hint, and look at the solution last. Every solution has Java that runs during the build with assertions against a slow but obviously correct oracle, and many add a deliberately wrong variant to show what the right version protects against.

### Leaving The Chapter

When the chapter is done you should be able to look at a problem and say what the key is, what the value is, which index or count convention applies, and whether a set, a map or a plain array is the smallest structure that works, as well as which lookalike misleads. The review section probes this with scenario questions that are best retaken after a few days.
