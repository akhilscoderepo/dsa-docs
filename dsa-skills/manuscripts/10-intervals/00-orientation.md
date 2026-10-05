<!-- section: orientation -->
## Orientation

A booking service refuses a guest because one stay ends on the morning that the next stay begins. A maintenance report draws four separate bars where two windows share hours and one bar belongs. A capacity report claims a peak of two users when the sessions only touch. All three programs read the same pairs of numbers, and each one fails at the place where two ranges meet. This chapter answers one question: how does a program decide, from the order of the ranges and the rule for their ends, what to do with each range in a single pass?

### Prerequisites

You should know `int[][]` arrays, `List<int[]>`, `Arrays.sort` with a comparator, and the cost words of Chapter 00. Chapter 05 taught sorting with comparators, and Chapter 08 taught two indexes that move forward through sorted data. The chapter defines an interval, the closed and half-open models and each other term at the point where it first matters.

### The Six Lessons

Each lesson fixes one decision about a list of ranges and states what the scan keeps.

- **Choose How To Sort Intervals** compares sorting by start with sorting by end and shows why a subtraction comparator is unsafe.
- **Decide When Touching Intervals Overlap** derives the overlap test from a closed or half-open model.
- **Merge Intervals And Insert A New One** keeps one growing interval and splits an insert into three parts.
- **Intersect Two Lists Of Intervals** moves one cursor in each list and advances the one that ends first.
- **Keep The Most Intervals Without Overlap** sorts by end to keep requests, and by start to find covered ones.
- **Count Active Intervals With Events** turns ranges into ordered start and end events with an explicit tie policy.

### The Combination Lesson

One lesson joins the order from sorting with the test from the interval rule.

- **Sort Intervals Then Scan Once** pairs each question about a list with a sort key and one carried value.

### How To Work Through Each Lesson

Each lesson opens with a program that works but is slow or wrong, and it asks you to predict the cause before the answer appears. Two traces follow, with the data drawn above a moving pointer. Four exercises close the lesson, from the basic case to a problem you must recognize from its wording, with a hint hidden until you ask. Write down the closed or half-open rule before you open a hint.

### What You Can Do After This Chapter

You can state the model for ends before you write a comparison, and you can say which of `<` and `<=` it requires. You can choose the sort key from the decision a question makes, and you can name the one value that the scan carries. You can find the input that breaks each scan, such as equal starts, an interval that ends inside a longer one, or two ends that meet at one coordinate.
