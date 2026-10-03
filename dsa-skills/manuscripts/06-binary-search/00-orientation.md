<!-- section: orientation -->
## Orientation

Binary search is the habit of throwing away half of the possibilities with one question, and the whole chapter is about learning which questions allow that. The array is only the first place where it works. You will see it find an exact value, the first or last copy of a value, an insertion point, the first position where a yes-or-no question turns true, the top of a hill, the lowest value of a rotated array, and the answer to an optimization problem when only a test of one candidate is available. Two final lessons join the search with a hash map and with a grid.

### What You Need Before Starting

You should have finished Chapters 00 to 05, or be comfortable with their content: stating a contract before coding, writing a loop whose invariant you can say aloud, using arrays and strings with their edge cases, keeping a hash map of lists, and sorting data so that a later decision becomes legal. You should know that `int` arithmetic wraps without warning, and that an array index must lie between zero and the length minus one. Two pointers, heaps and dynamic programming are named only as later destinations, and no exercise here needs them.

### The Eleven Lessons

The first lesson searches for one exact value and fixes the vocabulary of interval, midpoint and invariant. The second and third lessons handle duplicates and insertion points, and the fourth generalizes them to any monotone yes-or-no question. The fifth finds a peak without a sorted array, and the sixth and seventh cut through a rotated array to find its minimum and a target. The eighth and ninth lessons search a range of answers, whole numbers first and then real ones. The tenth lesson pairs the search with a map for lookups by key and time, and the eleventh pairs it with the shape of a matrix.

### How To Work Through A Lesson

Each lesson opens with a small story and a plain method. Before reading the bottleneck, guess how many times the plain method repeats work. The traces list every probe of a concrete input, with the discarded part in view, and the text names one step to study. Try each exercise in order and write your invariant on paper before opening the hint. Every solution comes with Java that is compiled and run in the build against an oracle that is slower and obviously right, and some include a wrong version so you can see exactly what the correct code prevents.

### Leaving The Chapter

By the end you should be able to take any search problem and say which interval convention you use, what the loop keeps true, what the condition on the midpoint means, what remains when the loop ends, and what the return value is for the empty and the one-element cases. You should also be able to tell when binary search is not allowed, because nothing is monotone. The review section checks these habits with short scenarios, and it is worth returning to after a few days.
