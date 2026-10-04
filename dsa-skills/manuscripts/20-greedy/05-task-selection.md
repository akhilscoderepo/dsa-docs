<!-- lesson-kind: standard -->
<!-- lesson-id: task-selection -->
## Task Selection

<!-- stage: context -->
### The Foreman At Bramble Wharf

The foreman at Bramble Wharf has two jobs that look different and feel alike. In the morning she loads a truck. The truck has room for a fixed number of boxes, and the stacks on the dock hold boxes of different kinds, each kind worth a different number of units per box. She wants the truck to leave carrying as many units as possible.

In the afternoon she plans the work of her small crew. A list of repair tasks is pinned to the board. Each one takes a known number of hours and must be finished by a stated hour, or the customer will not pay. The crew does one task at a time and she wants to complete as many tasks as possible before the deadlines pass. In both jobs she must decide which things to keep and which to leave behind.

<!-- stage: naive -->
### Try Every Subset Of Tasks

For the afternoon list the direct method decides, for each task in deadline order, whether to take it or to leave it, and keeps track of the hour at which the crew becomes free. A task may be taken only if it would finish by its deadline.

```java
static int most(int[][] tasks, int i, long free) {            // tasks[i] = {hours, deadline}, sorted by deadline
    if (i == tasks.length) return 0;
    int best = most(tasks, i + 1, free);                       // leave task i
    if (free + tasks[i][0] <= tasks[i][1])                     // task i would finish in time
        best = Math.max(best, 1 + most(tasks, i + 1, free + tasks[i][0]));
    return best;
}
```

The method is exact for any list, since it weighs both possibilities for every task. For the truck the same idea tries every number of boxes from every stack, and it is also exact. With a dozen tasks the answer arrives at once.

<!-- stage: bottleneck -->
### Every Task Doubles The Search

Two branches per task make O(2^n) calls for the afternoon list, and the truck search is no better. Most of the branches share a suffix of the list and differ only in the hour at which the crew becomes free, so the same questions are asked again and again.

A tempting shortcut is to walk through the tasks once in deadline order and take each one that still fits. It is fast, and it is wrong. With tasks of 5 hours due at hour 5, 4 hours due at hour 6, and 2 hours due at hour 6, the shortcut takes the five-hour task first, and then nothing else fits. The best plan takes the other two and completes both. A task that was accepted early can be the reason that several later tasks must be refused, and the shortcut never looks back.

<!-- stage: insight -->
### Keep The Cheapest Set That Still Fits

For the truck the answer is a plain choice. Every box occupies one place, so a box worth more units dominates a box worth fewer, and the foreman should fill the truck from the most valuable kind downwards. If an optimal load uses a lower-valued box while a higher-valued one stays on the dock, trading them keeps the count and raises the total.

For deadlines the safe order is by deadline, so that each task is judged against the time already spent on everything with an earlier deadline. Maintain a **retained set**, the tasks kept so far, which can all be finished by their deadlines. Add the next task, and if the total hours now run past its deadline, apply a **replacement rule**: discard the longest task in the set, whichever it is, newcomer included. The discard is called an **ejection**, and it can remove an old task in favour of a new one.

<!-- names: retained set, replacement rule, ejection -->

The rule is safe because the retained set always has two properties together. It is as large as any feasible set drawn from the tasks seen so far, and among sets of that size it has the least total time. An ejection removes the longest task, so the set keeps its size and its total shrinks, leaving the most room for later tasks. If the newcomer is itself the longest task, discarding it changes nothing, which is also correct. Small totals can only help the future, and a bigger set is never given up.

When every task takes exactly one slot, there is no longest task to prefer, so ejection never improves anything. Sorting by deadline and taking a task while the number taken so far is below its deadline is enough.

<!-- stage: variables -->
### The Total, The Heap And The Capacity

For the truck, `truck` is the number of box places still empty, `units` is the total loaded, and each stack is taken whole or partly, whichever the remaining places allow. For the tasks, `i` is the next task in deadline order, `time` is the sum of hours in the retained set, and the max-priority queue `kept` holds the hours of the retained tasks so that its top is the longest. The size of `kept` is the answer at any moment. Both `time` and `units` can pass the range of an `int`, so they are `long`. The tasks themselves are never modified.

<!-- stage: trace -->
### Loading A Truck And Keeping Tasks

The first trace loads the truck. Four kinds of box are listed from most to least valuable, and the truck has room for eight boxes. The two boxes at nine units each are taken whole. Then three boxes at seven units, which brings the total to thirty-nine with three places left. Four boxes at four units are available but only three places remain, so three are taken and the truck is full. Five more boxes at two units never get a place.

The second trace follows the afternoon list in deadline order, with each task written as hours then deadline. The first task, three hours due at four, fits. The second, five hours due at nine, brings the total to eight and fits. The third, four hours due at ten, makes twelve, which is too late, so the longest retained task, the five, is ejected and the total drops to seven. The fourth fits. The fifth, six hours due at twelve, would bring the total to fifteen. It is the longest, so it ejects itself, and the set keeps its three tasks.

```trace
{"cells":["2x9","3x7","4x4","5x2"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"placesLeft":6,"units":18},"note":"All 2 boxes at 9 units fit, so they are loaded whole and 6 places remain."},{"at":{"i":1},"vars":{"placesLeft":3,"units":39},"note":"All 3 boxes at 7 units fit, so they are loaded whole and 3 places remain."},{"at":{"i":2},"vars":{"placesLeft":0,"units":51},"note":"Only 3 of the 4 boxes at 4 units fit, so the truck becomes full."},{"at":{"i":3},"vars":{"placesLeft":0,"units":51},"note":"The truck is already full, so the 5 boxes at 2 units stay on the dock."}]}
```

```trace
{"cells":["3h-4","5h-9","4h-10","2h-11","6h-12"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"total":3,"kept":1,"longest":3},"note":"The task of 3 hours due at 4 ends at hour 3, in time, so it joins the set."},{"at":{"i":1},"vars":{"total":8,"kept":2,"longest":5},"note":"The task of 5 hours due at 9 ends at hour 8, in time, so it joins the set."},{"at":{"i":2},"vars":{"total":7,"kept":2,"longest":4},"note":"The task of 4 hours due at 10 would end at hour 12, too late. The longest kept task of 5 hours is ejected, so the total drops to 7."},{"at":{"i":3},"vars":{"total":9,"kept":3,"longest":4},"note":"The task of 2 hours due at 11 ends at hour 9, in time, so it joins the set."},{"at":{"i":4},"vars":{"total":9,"kept":3,"longest":4},"note":"The task of 6 hours due at 12 would end at hour 15, too late. It is the longest in the set, so it ejects itself and the total returns to 9."}]}
```

<!-- stage: code -->
### Fill By Value, Keep By Deadline

```java
static long maxUnits(long[][] types, long truck) {          // types[i] = {boxes, unitsPerBox}
    long[][] order = types.clone();
    Arrays.sort(order, (a, b) -> Long.compare(b[1], a[1]));   // most valuable first
    long units = 0;
    for (long[] t : order) {
        if (truck == 0) break;
        long take = Math.min(t[0], truck);
        units += take * t[1];
        truck -= take;
    }
    return units;
}

static int mostCourses(int[][] tasks) {                      // tasks[i] = {hours, deadline}
    int[][] order = tasks.clone();
    Arrays.sort(order, (a, b) -> Integer.compare(a[1], b[1]));
    PriorityQueue<Integer> kept = new PriorityQueue<>(Comparator.reverseOrder());
    long time = 0;
    for (int[] t : order) {
        kept.add(t[0]);
        time += t[0];
        if (time > t[1]) time -= kept.poll();               // drop the longest, maybe the newcomer
    }
    return kept.size();
}

static int mostUnitTasks(int[] deadlines) {
    int[] d = deadlines.clone();
    Arrays.sort(d);
    int done = 0;
    for (int x : d) if (done < x) done++;
    return done;
}
```

Sorting dominates all three methods. The truck loop and the unit-task loop are linear after it, and the deadline loop adds a heap operation per task, so the whole is O(n log n). The product `take * t[1]` is formed in `long` because both factors are stored as `long`, which is what prevents a wrapped total.

<!-- stage: applicability -->
### When Tasks Compete For One Budget

Use this pattern when items consume a shared budget, such as places, time before a deadline, or money, and the objective is a count or a total value. The invariant to state is that the retained items are feasible under every constraint processed so far and are the best under the proven replacement rule. For a pure capacity with values per unit, sort once and fill. For deadlines with durations, sort by deadline and keep a max-heap of durations.

The false friend is a single sort without a way to undo. Sorting by deadline and accepting whatever fits fails on the list from the bottleneck stage, and sorting by shortest duration ignores deadlines altogether, so a short task due far away can crowd out a long task that was about to expire. Another false friend is a value that is not per unit. If boxes differ in size as well as value, the filling is a knapsack problem, which needs dynamic programming from Chapter 27, and the greedy fill is wrong.

In Java, keep totals in `long`, give the heap a reversed comparator for a max-heap, and clone arrays before sorting.

<!-- stage: exercises -->
### Exercises

#### [Build] Maximum Units on a Truck (LeetCode 1710)
<!-- id: gr-maximum-units -->

**Prerequisites.** The local-choice lesson of this chapter; sorting rows with a comparator from Chapter 05.

**Problem.** Each entry of `types` is `[boxes, unitsPerBox]`. The truck holds at most `truck` boxes, and any boxes may be left behind. Return the largest total number of units that the truck can carry.

**Constraints.** 0 <= types.length <= 1000, 0 <= boxes <= 1000000, 0 <= unitsPerBox <= 1000000 and 0 <= truck <= 2000000. Compute the total in `long`.

**Example 1.** Input `types = [[3, 7], [5, 2], [2, 9], [4, 4]]`, `truck = 8`, output 51.

**Example 2.** Input `types = [[1, 5], [2, 3]]`, `truck = 100`, output 11, since the truck is not filled.

**Hint.** If a box worth fewer units is on the truck while a better one is on the dock, what does swapping them do to the total? What happens when the truck is larger than the supply?

**Changed decision.** First rung: sort by value per box and fill greedily, taking each stack whole or only as much as the places allow.

#### [Vary] Deadline-Compatible Unit Tasks (Author exercise)
<!-- id: gr-unit-tasks-deadlines -->

**Prerequisites.** The truck exercise above.

**Problem.** Each task takes exactly one time slot, and slots are numbered 1, 2, 3 and so on. A task with deadline `d` must occupy one of the slots 1 to `d`, and a slot holds one task. Return the largest number of tasks that can be scheduled.

**Constraints.** 0 <= deadlines.length <= 100000 and 0 <= deadlines[i] <= 1000000000. A deadline of 0 can never be met.

**Example 1.** Input `deadlines = [3, 1, 1, 4, 3]`, output 4.

**Example 2.** Input `deadlines = [0, 5]`, output 1, since the task due at 0 is impossible.

**Hint.** After sorting, how many slots have been used when the next task is judged? What does the answer look like when all deadlines are the same?

**Changed decision.** The budget is now a deadline instead of a capacity, and with equal durations no earlier choice ever needs to be undone.

#### [Boundary] Equal Reward And Capacity Limit (Author exercise)
<!-- id: gr-equal-reward-capacity -->

**Prerequisites.** The two exercises above.

**Problem.** Each entry of `types` is `[boxes, unitsPerBox]`, and the truck holds at most `truck` boxes. Fill the truck from the highest `unitsPerBox` downwards. Among kinds with the same `unitsPerBox`, take the kind with the lower input index first. Return two `long` values: the total units loaded and the number of kinds from which at least one box was taken.

**Constraints.** 0 <= types.length <= 1000, 0 <= boxes <= 2000000000, 0 <= unitsPerBox <= 2147483647 and 0 <= truck <= 2000000000.

**Example 1.** Input `types = [[2, 5], [3, 5], [1, 5]]`, `truck = 4`, output `[20, 2]`.

**Example 2.** Input `types = [[2000000000, 2147483647]]`, `truck = 2000000000`, output `[4294967294000000000, 1]`.

**Hint.** What does the product of a box count and a value do in 32-bit arithmetic? Which kinds are reached when the truck fills up in the middle of a stack?

**Changed decision.** A deterministic tie rule is stated and the accumulated total is held in `long`, because the product exceeds the `int` range.

#### [Recognize] Course Schedule III (LeetCode 630)
<!-- id: gr-course-schedule-three -->

**Prerequisites.** All three exercises above; the heap of Chapter 17.

**Problem.** Each entry of `courses` is `[duration, lastDay]`. Courses are taken one after another starting on day 0, and a course must be finished on or before its last day. Return the largest number of courses that can be taken.

**Constraints.** 0 <= courses.length <= 100000 and 1 <= duration, lastDay <= 1000000000. The total duration may exceed the `int` range.

**Example 1.** Input `courses = [[5, 5], [4, 6], [2, 6]]`, output 2.

**Example 2.** Input `courses = [[1000000000, 1000000000], [1000000000, 2000000000], [1000000000, 2000000000]]`, output 2.

**Hint.** In which order should courses be considered? When the total passes the last day, which of the kept courses is the best one to give up?

**Changed decision.** An earlier acceptance can now be undone, so the retained durations sit in a max-heap and the longest is ejected when the deadline is broken.
