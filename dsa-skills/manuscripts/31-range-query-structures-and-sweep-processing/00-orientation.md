<!-- section: orientation -->
## Orientation

A leaderboard service updates one player's score and then reports the total score of ranks 1,000 to 5,000. Recomputing the total with a loop costs thousands of additions per request, and a stored prefix-sum array costs a full rebuild per update. A calendar service must report the most overlapping meetings at any minute while bookings arrive in any order. Both services need a structure that answers range questions while the data changes, or a pass that visits only the moments when something changes.

### Prerequisites

You should know prefix sums from the earlier chapter on prefix sums and difference arrays, sorting with comparators, binary search on a sorted array, and the heap from the chapter on priority queues. A half-open range `[a, b)` includes `a` and excludes `b`, and later lessons use it for intervals. You should read `i & -i` as the lowest set bit of `i`. Lesson 01 explains that expression again where it first matters. Recursive functions on a range, as in the tree chapters, appear from lesson 02 onward.

### The Five Lessons

Each lesson answers one question about how to avoid repeating work on a range of values or on a series of changes.

- **Fenwick Trees** store block sums in one array, so a prefix query and a point update each take O(log n) steps.
- **Segment Trees** store the aggregate of an exact interval in every node, so they handle operators such as minimum, which has no inverse operation and therefore does not fit a Fenwick tree.
- **Lazy Propagation** delays a range update inside a node until a later query needs the children.
- **Coordinate Compression** replaces huge or negative values by dense ranks that keep the order.
- **Sweep Events** sorts the moments at which state changes and updates the state once per moment.

### The Two Closing Lessons

Each closing lesson adds a part that names what the earlier lessons contribute.

- **Sweep And Ordered State** keeps an ordered structure of active values while events arrive in coordinate order. Its exercises cover a capacity check, a skyline, an equal-coordinate rule and a booking counter.
- **Compress Values Then Count Ranks** turns sparse keys into ranks and counts them with a Fenwick tree. Its exercises cover the ranking step, a sparse mutable sum, extreme values and an insertion cost.

### How To Work Through Each Lesson

A lesson opens with a realistic scenario that exposes a failure. A short direct program follows, and it is too slow or returns a wrong answer. You predict its cost before the explanation appears. The later parts name the stored quantity and list the variables, then follow two traces, show the code and state where the idea stops fitting. Range conventions differ by lesson: the Fenwick tree takes zero-based positions and stores them one-based, the segment tree uses inclusive ranges, and lazy propagation uses half-open ranges. Four exercises close each lesson, and each exercise has a hint and a solution that you can open after your own attempt.

### What You Can Do After This Chapter

You can choose between a Fenwick tree, a segment tree and a sorted event list from the update and query types in a problem statement. You can state what each stored number covers, and you can use `long` sums and one-based or zero-based indexes without off-by-one errors. You can also replace a sparse value range by ranks before counting.
