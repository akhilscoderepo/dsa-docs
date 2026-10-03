<!-- section: orientation -->
## Orientation

An interval is a stretch of a line with a beginning and an end, and many ordinary questions are about how such stretches relate: which ones clash, which ones can be fused into one, which ones can all be kept, and how many are in force at once. The answers are short loops once the stretches are in a good order, but nearly every mistake in this chapter comes from a decision made before the loop begins. Does a stretch that ends at hour 5 clash with one that starts at hour 5? Which end is the sort key? What does the loop carry from one stretch to the next? The chapter teaches those decisions first and the loops second.

### Before You Begin

You should be comfortable with arrays of arrays in Java, with sorting an array of pairs by a comparator, and with the sorting chapter's warning that a comparator must give a consistent total order. The earlier chapters on two pointers and prefix sums help, because the intersection of two lists reuses the idea of one cursor per sequence. Heaps are not needed, and the room-allocation problems that use them are left for the heap chapter.

### The Seven Lessons

The first lesson makes the comparator explicit: ordering by start or by end, how equal endpoints are broken, and why extreme values must never be compared by subtraction. The second fixes what a shared endpoint means under closed and half-open contracts, and shows that one wrong comparison sign changes a count. The third merges a list and inserts one new interval into a sorted list. The fourth intersects two sorted lists with a cursor in each. The fifth chooses which intervals to keep or to strike when overlap is the cost, and when one interval hides inside another. The sixth turns intervals into signed entries and sweeps them to count how many are active, with the order of equal coordinates stated as a rule. The seventh combines sorting with the overlap rules and answers four questions with the same sorted scan.

### How To Work Through A Lesson

Read the scene and predict what the clerk or the electrician should write on the paper before reading the plain method. When a trace opens, step through it once without the notes, and then check what you predicted against them. Try every exercise before its hint, and for each one write the contract in a single line, closed or half-open, before touching the code. The Java solutions are compiled and run, and each is compared with a slower method that checks every possible case.

### Leaving The Chapter

You should be able to say which sort key suits a union and which suits a selection, what single number a scan carries in each case, and how the code changes when a shared endpoint stops counting as overlap. You should also be able to explain why equal-coordinate entries need a stated order in a sweep, and why a comparison written as a subtraction is a bug waiting for large inputs. The review after the lessons poses short scenarios, and it is worth returning to after a few days.
