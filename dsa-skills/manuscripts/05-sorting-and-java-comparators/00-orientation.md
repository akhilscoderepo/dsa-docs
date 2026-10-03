<!-- section: orientation -->
## Orientation

Sorting is rarely the answer to a problem. It is a transformation that puts the data in an order from which a later, simpler decision becomes valid, and each lesson in this chapter names the order and the decision it unlocks. You will learn what it means for an ordering to be a contract, how `Arrays.sort` treats primitive arrays, how a `Comparator` is written and checked, how records with several fields are ordered, who owns the answer when two elements tie, and four ways to use a sorted sequence: sweeping over it, collapsing runs of equal values, and scanning it for a simple relation between neighbors. A final lesson joins strings, maps and sorting into canonical keys.

### What You Need Before Starting

You should have finished Chapters 00 to 04, or be comfortable with their content: reading a contract before coding, writing a single pass with an invariant, cloning an array so the caller's data survives, using a hash map to group items, and treating a string as a sequence of characters. You should know the difference between `int` and `Integer`, and that a record is a small class with named fields. Binary search, two pointers, intervals and greedy choices are named here only as later destinations. This chapter will not ask you to solve problems that need them.

### The Nine Lessons

The first lesson makes the ordering itself the subject, with the rule that a comparison must never be computed by subtracting. The second covers sorting primitives, including copies and sub-ranges. The third is about comparators as objects that must obey laws, and the fourth applies them to records with several fields. The fifth asks who owns a tie. The sixth, seventh and eighth lessons each use the sorted order to simplify a later question, by sweeping with a frontier, by closing runs of equal values, and by comparing each element with a neighbor or an index. The ninth lesson lets strings, maps and sorting meet, using sorted words as map keys.

### How To Work Through A Lesson

Read the small story first and try to predict where the plain approach will waste effort before the bottleneck section says so. The traces step through a concrete input, and it helps to pause on the step the text singles out. Attempt each exercise in order, write your answer in the notes box before opening the hint, and treat the solution as a last resort. Every solution carries Java that is compiled and run during the build, with assertions against an oracle that is slower but obviously correct, and several solutions include a deliberately wrong variant so you can see what the correct version protects against.

### Leaving The Chapter

By the end you should be able to say, for any problem that mentions an order, which pairs of elements the order must separate, what the comparator returns for ties, whether the original positions are still needed, and whether sorting is the right tool or only a convenient one. The review section checks these habits with scenarios and is worth repeating after a few days.
