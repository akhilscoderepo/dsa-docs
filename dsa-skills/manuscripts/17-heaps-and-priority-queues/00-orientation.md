<!-- section: orientation -->
## Orientation

A support tool serves tickets in the wrong order after an edit. A build farm starts a job before anyone requested it. A dashboard chart of the median response time slows down every hour. A timer loop spends most of its processor time looking for the earliest expiry. Each program keeps a changing set of items and needs the smallest, the largest or the middle one again and again. This chapter shows how a priority queue answers that question in O(log n) time per change, and how to keep it correct when ties, extreme integers, release times and deletions enter the picture.

### Prerequisites

You should know loops, arrays, the cost words from Chapter 00, and sorting with comparators from Chapter 05. Chapter 04 introduced hash maps, which two lessons use for counts and versions. Chapter 10 introduced intervals and the choice between a half-open and a closed interval, and the combination lesson builds on both. Chapter 14 introduced linked list nodes, which the merge exercise uses. Each lesson defines its own terms the first time they matter. Code samples assume `import java.util.*;` and a recent JDK.

### The Seven Lessons

Each lesson adds one rule that turns a repeated search for an extreme item into a short loop on a queue.

- **Take The Smallest Item Repeatedly** shows how `PriorityQueue` stores items in an array and why iteration does not give sorted order.
- **Choose The Order With A Comparator** states exactly which item leaves first, including ties and the extremes of `int`.
- **Keep Only The Best K Items** holds a queue of fixed size, whose root guards the boundary.
- **Merge Sorted Lists With A Heap** keeps one value from each sorted source and refills it after every removal.
- **Run Tasks When They Become Ready** separates the order of arrival from the order of selection.
- **Delete From A Heap Lazily** skips outdated entries when they reach the root, so no removal needs a scan.
- **Track The Median As Numbers Arrive** splits the values into two halves that always bracket the middle.

### The Combination Lesson

One lesson joins this chapter with an earlier one.

- **Reuse Meeting Rooms With A Heap** joins sorted intervals with a queue of end times, so one pass counts rooms or groups.

### How To Work Through Each Lesson

Each lesson begins with a program that fails or slows down on a real input, and then shows a plain version that works but costs too much. A prediction question follows, and you commit to an answer before the explanation opens. The remaining parts give the rule, the state, a step-by-step trace, the code and a check of when the method does not apply. The exercises climb from a basic version to an interview problem. Each exercise has a role in brackets, either Build, Vary, Boundary or Recognize. Each exercise also lists a Changed decision, which names the one choice that differs from the exercise before it, and the tag Author exercise marks a problem written for this chapter. Try the hint before you read a solution.

### What You Can Do After This Chapter

You can tell, for a given problem, whether it needs the smallest item, the best k items, the next item from several sorted sources, the best available item at a given time, or the middle item. You can write the comparator for a tuple of fields and say what happens on ties. You can list the edge cases before you code: an empty queue, equal priorities, `Integer.MIN_VALUE` and `Integer.MAX_VALUE`, and a count that exceeds the size.

### What Later Chapters Reuse

Three ideas carry forward.

- **Guard the boundary with a small queue** returns whenever only the best few items matter.
- **Skip stale entries at the root** returns whenever a queue holds entries that may no longer be true, for example distances in a graph search.
- **Add released items before selecting** returns whenever the choice depends on a clock.
