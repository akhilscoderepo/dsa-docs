<!-- section: orientation -->
## Orientation

A monotonic stack is an ordinary stack with one added promise: the entries are kept in a single order, so that a new arrival can settle every entry it dominates and then stop. Questions that look as if each position must scan its neighbours, such as the next larger value, the length of a run of dominated days, or the widest region where a value is the smallest, are answered in one pass because each position enters the stack once and leaves it once. This chapter shows what the stack must hold, when an answer is written, and how ties between equal values are decided.

### What You Need Before Starting

Chapters 00 to 11 should be familiar, in particular contracts and complexity statements, loops over arrays, hash maps from Chapter 04, and the plain stack of Chapter 11 used through `ArrayDeque` with `addLast`, `removeLast` and `peekLast`. Prefix sums from Chapter 07 appear once, as an alternative viewpoint. Ordering that comes from a greedy exchange argument is named as a later destination, and no exercise here depends on it.

### The Eight Lessons

The first lesson finds the next greater or smaller value for every position and settles what happens on equality. The second lesson wraps the array into a ring and reads it twice without copying. The third answers a running question about a stream, how many days in a row were not higher, using compressed pairs. The fourth finds the nearest smaller position on each side of every element, and the fifth explains how to give every subarray exactly one owner when values repeat. The sixth turns those owners into sums by multiplying two distances, and the seventh uses the same walls to find the largest rectangle under a bar chart. The eighth lesson combines the stack with contribution counting and reports spreads and positions.

### How To Work Through A Lesson

Every lesson begins with a short scene and a plain method. Before you read the bottleneck, try to say which comparison the plain method repeats. The traces show the stack and the answers after every arrival, and the surrounding text points to the single step that is worth studying twice. Do the exercises in order. Before opening a hint, write down what the stack holds, which comparison removes an entry, and when the answer is written. Each solution contains Java that is compiled and run, and each program is checked against a slower method that tries everything.

### Leaving The Chapter

You should leave able to say in one sentence what the stack holds, why a failing comparison lets the loop stop, and why each position is handled a constant number of times. You should also be able to explain why a tie rule needs one strict side and one non-strict side, and why a width and a count of stretches are different numbers. The review at the end tests these points with short scenarios and is worth returning to after a few days.
