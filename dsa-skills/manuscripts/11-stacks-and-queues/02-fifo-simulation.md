<!-- lesson-kind: standard -->
<!-- lesson-id: fifo-simulation -->
## Process Items In Arrival Order

<!-- stage: context -->
### A Job That Never Prints

A print service stores waiting jobs in a stack. Each new job goes on top, and the printer always takes the top job. Under steady load, a job that arrived early sits at the bottom while newer jobs keep printing first. Users see their document delayed without limit, although the printer is never idle.

The fault is in the order of service, not in the speed. The service must handle items in the order they arrived, and some items need several turns before they finish. The lesson answers one question. How does a queue simulate this process, including tasks that return for another turn, and how does the loop know when it can stop?

<!-- stage: naive -->
### Scan The Whole Array Each Pass

The direct approach keeps an array `remaining` with the work left per task. One pass visits every index from 0 to n - 1, gives each unfinished task one unit of work, and skips tasks with zero work left. The code repeats passes until every task is done and records the order in which tasks finish.

```java
static int[] finishOrderByScan(int[] remaining) {
    int n = remaining.length;
    int[] work = remaining.clone();
    int[] order = new int[n];
    int done = 0;
    while (done < n) {
        for (int i = 0; i < n; i++) {
            if (work[i] == 0) continue;
            work[i]--;
            if (work[i] == 0) order[done++] = i;
        }
    }
    return order;
}
```

For `[2,1,3]` the method returns `[1,0,2]`. The result is correct, and the method follows arrival order within each pass.

<!-- stage: bottleneck -->
### Visiting Tasks That Are Already Done

```predict
There are 1000 tasks. Nine hundred ninety-nine tasks need 1 unit of work, and the last task needs 1000 units. How many index visits does the scan make, and how many turns does the work itself require?

Each of the 1000 passes visits all 1000 indexes, so the scan makes 1,000,000 visits. The work itself needs 999 + 1000 = 1999 turns, because every unit of work is one turn. The scan spends almost all visits on finished tasks.
```

The scan costs O(n * m) time, where `m` is the largest amount of work, because each pass visits every task. The turns that matter total only the sum of all work, which is O(n + m) in the example. Every visit to a finished slot repeats a check that was already settled. The scan also loses the arrival order of tasks that return later, because it recovers that order from the array index and not from the order of returning.

The waste points to a different representation. The code should store only the tasks that still need a turn, in the order they will receive it.

<!-- stage: insight -->
### Keep Waiting Items In One Line

A queue holds exactly the waiting tasks in service order. The simulation removes one task at a time and decides whether it returns.

#### Where Items Enter And Leave

The **front** of the queue is the end that supplies the next task to process. The **back** is the end that receives every new or returning task. With `ArrayDeque`, the front is the first end read by `pollFirst`, and the back is the last end written by `addLast`. A task added at the back waits behind every task already present.

#### One Turn Of The Loop

The loop removes the front task and gives it one turn. It decrements the task's remaining work. When work remains, it adds the task at the back. When no work remains, the task is finished and leaves for good. The invariant is that the front is the next task to process and every task added to the queue appears behind all tasks already there. Items are therefore served in arrival order, and a stack, which serves the newest item first, reverses that order.

#### Detecting That No Progress Is Possible

Some simulations can stall. A **miss** is a turn where the removed item makes no progress and goes straight back to the queue. When the number of consecutive misses equals the queue length, every item has been tried against the same state and none made progress. Each further turn would repeat the same outcomes, so the loop stops.

<!-- names: front, back, miss -->

<!-- stage: variables -->
### Queue State And Counters

The simulation keeps three pieces of state.

- **queue** is the `ArrayDeque` of task ids that still need work, in service order, and it changes once per turn.
- **work** is the array of remaining units per task, and only the removed task's entry changes in a turn.
- **misses** is the count of consecutive misses; it resets to zero after progress and is compared with `queue.size()`.

<!-- stage: trace -->
### Two Simulations Step By Step

The first trace runs round-robin with one unit of work per turn on the work array `[2,1,3]`. The cells are the starting work, and the pointer `task` marks the task removed at each step. The variable `queue` shows task ids from front to back, and `finished` lists the finish order.

Task 0 loses one unit and returns to the back. Task 1 finishes on its first turn. Task 2 returns twice, because its work is the largest. The finish order is task 1, task 0, task 2, and the queue is empty after six turns.

```trace
{"cells":[2,1,3],"pointers":["task"],"steps":[{"at":{"task":0},"vars":{"queue":"[1, 2, 0]","finished":"[]"},"note":"Task 0 loses one unit, has 1 left and returns to the back."},{"at":{"task":1},"vars":{"queue":"[2, 0]","finished":"[1]"},"note":"Task 1 loses its last unit and finishes."},{"at":{"task":2},"vars":{"queue":"[0, 2]","finished":"[1]"},"note":"Task 2 loses one unit, has 2 left and returns to the back."},{"at":{"task":0},"vars":{"queue":"[2]","finished":"[1, 0]"},"note":"Task 0 loses its last unit and finishes."},{"at":{"task":2},"vars":{"queue":"[2]","finished":"[1, 0]"},"note":"Task 2 loses one unit, has 1 left and returns to the back."},{"at":{"task":2},"vars":{"queue":"[]","finished":"[1, 0, 2]"},"note":"Task 2 loses its last unit and finishes."}]}
```

The second trace uses a school lunch case. The students array is `[1,0,0,1,1]` and the sandwiches array is `[0,0,1,0,1]`. Each student prefers sandwich type 0 or 1, and the sandwiches lie in a fixed order. The student at the front eats when the preference equals the top sandwich. Otherwise the student moves to the back. The cells are the sandwiches, and the pointer `top` is the index of the top sandwich, which moves one place right each time a student eats. The variable `misses` counts consecutive moves to the back.

The last two students both want sandwich 1 while the top sandwich is 0. Two consecutive misses equal the queue length, so the loop stops and reports two students left.

```trace
{"cells":[0,0,1,0,1],"pointers":["top"],"steps":[{"at":{"top":0},"vars":{"queue":"[0, 0, 1, 1, 1]","misses":1},"note":"A student who wants 1 does not match sandwich 0 and moves to the back, so misses is 1."},{"at":{"top":1},"vars":{"queue":"[0, 1, 1, 1]","misses":0},"note":"A student who wants 0 takes sandwich 0, and misses resets to 0."},{"at":{"top":2},"vars":{"queue":"[1, 1, 1]","misses":0},"note":"A student who wants 0 takes sandwich 0, and misses resets to 0."},{"at":{"top":3},"vars":{"queue":"[1, 1]","misses":0},"note":"A student who wants 1 takes sandwich 1, and misses resets to 0."},{"at":{"top":3},"vars":{"queue":"[1, 1]","misses":1},"note":"A student who wants 1 does not match sandwich 0 and moves to the back, so misses is 1."},{"at":{"top":3},"vars":{"queue":"[1, 1]","misses":2},"note":"A student who wants 1 does not match sandwich 0 and moves to the back, so misses is 2."},{"at":{"top":3},"vars":{"queue":"[1, 1]","misses":2},"note":"The queue size equals misses, so the loop stops with 2 students left."}]}
```

<!-- stage: code -->
### Round-Robin And Stalled Queue

#### Round-Robin With A Queue

The queue holds only unfinished tasks, so every turn does useful work.

```java
static int[] finishOrder(int[] remaining) {
    int[] work = remaining.clone();
    java.util.ArrayDeque<Integer> queue = new java.util.ArrayDeque<>();
    for (int i = 0; i < work.length; i++) queue.addLast(i);
    int[] order = new int[work.length];
    int done = 0;
    while (!queue.isEmpty()) {
        int task = queue.removeFirst();
        work[task]--;
        if (work[task] > 0) queue.addLast(task);
        else order[done++] = task;
    }
    return order;
}
```

#### Stopping After A Run Of Misses

The second method keeps `misses` and stops when it equals the queue size.

```java
static int unableToEat(int[] students, int[] sandwiches) {
    java.util.ArrayDeque<Integer> queue = new java.util.ArrayDeque<>();
    for (int s : students) queue.addLast(s);
    int top = 0, misses = 0;
    while (!queue.isEmpty() && misses < queue.size()) {
        int s = queue.removeFirst();
        if (s == sandwiches[top]) { top++; misses = 0; }
        else { queue.addLast(s); misses++; }
    }
    return queue.size();
}
```

The first method runs in O(n + W) time, where `W` is the total work, and uses O(n) space. The second runs in O(n^2) time in the worst case, because each of n successes can follow up to n misses, and it uses O(n) space.

<!-- stage: applicability -->
### Deciding Whether A Queue Fits

#### Recognizing Arrival-Order Processing

Use a queue when items must be handled in arrival order and later arrivals wait behind earlier ones. Task schedulers, print spoolers and request handlers have this shape. The invariant to state in code comments is that one end supplies the next item and the other end receives every addition. Prove each removal safe with a size check, or choose the form that reports empty.

#### Stack And Priority Order Are False Friends

A stack looks similar, because both structures add and remove items one at a time. That is the false friend. A stack serves the newest item first and reverses arrival order. A task that must return for another turn also tempts code to put it back at the front, which gives it a second turn before every waiting task. Return it to the back. If a task has a priority that overrides arrival order, a plain queue does not fit.

#### Java Hazards In The Loop

Two Java hazards appear in these loops. Comparing boxed `Integer` values with `==` compares references and fails for values outside the small cached range, so call `equals` or unbox to `int` first. Adding to a collection inside a for-each loop over the same collection throws `ConcurrentModificationException`, so use a `while` loop that removes the front. A simulation also never terminates when no turn removes work, so every loop needs a measure that strictly decreases or a stalled-state test.

<!-- stage: exercises -->
### Exercises

#### [Build] Printer Queue (Author exercise)
<!-- id: sq-printer-queue -->

**Prerequisites.** The queue loop in this lesson.

**Problem.** Job `i` arrives at time `arrival[i]` and needs `duration[i]` time units on a printer. The printer handles one job at a time, starts the earliest arrived waiting job as soon as it is free, and never interrupts a job. Return an array whose entry `i` is the time at which job `i` finishes.

**Constraints.** The limits are:
- **Length** is `0 <= n <= 10^5` for both arrays.
- **Arrival** values are non-decreasing integers in `[0, 10^9]`.
- **Duration** values are integers in `[1, 10^4]`.
- **Return** is a new `long[]`; the inputs do not change.

**Example 1.** Input `arrival = [0,1,10]` and `duration = [3,2,1]`, output `[3,5,11]`.

**Example 2.** Input `arrival = [0,0,0]` and `duration = [2,2,2]`, output `[2,4,6]`.

**Hint.** Jobs that arrive while the printer is busy wait in the queue. When the queue is empty, which time should the clock jump to?

**Changed decision.** Basic case: every job enters the queue once and leaves once, in arrival order.

#### [Vary] Round-Robin One Step (Author exercise)
<!-- id: sq-round-robin-step -->

**Prerequisites.** The exercise above.

**Problem.** Task `i` needs `work[i]` units. Each turn takes the first task in the queue, removes one unit of its work and puts it at the end of the queue only when work remains. Initially the queue holds tasks `0` to `n - 1` in index order. Return the task ids in the order in which tasks finish.

**Constraints.** The limits are:
- **Length** is `0 <= n <= 1000`.
- **Work** values are integers in `[1, 1000]`.
- **Return** is a new `int[]` of length `n`; the input does not change.

**Example 1.** Input `[2,1,3]`, output `[1,0,2]`.

**Example 2.** Input `[3,3,1]`, output `[2,0,1]`.

**Hint.** The queue should hold only unfinished tasks. Which test decides between re-adding and recording a finish?

**Changed decision.** A task re-enters the queue only when work remains, and the loop ends when the queue is empty.

#### [Boundary] Queue Becomes Empty (Author exercise)
<!-- id: sq-queue-becomes-empty -->

**Prerequisites.** The two exercises above.

**Problem.** Task `i` needs `work[i]` units, where zero means the task is already complete. A turn runs the first queued task for at most `q` units, and the clock advances by the units used. A task with work left goes to the end of the queue. Initially the queue holds every task with positive work in index order. Return the clock value at which each task completes, and `0` for a task that starts complete.

**Constraints.** The limits are:
- **Length** is `0 <= n <= 1000`, and an empty array is legal.
- **Work** values are integers in `[0, 1000]`.
- **Quantum** `q` is an integer in `[1, 1000]`.
- **Return** is a new `int[]` of length `n`; the input does not change.

**Example 1.** Input `work = [3,0,2]` and `q = 2`, output `[5,0,4]`.

**Example 2.** Input `work = [1,1,1]` and `q = 5`, output `[1,2,3]`.

**Hint.** Never remove from the queue unless the loop condition proves it is non-empty. What happens to a task that finishes on its first turn?

**Changed decision.** A task may finish on its first turn and never return, and the queue may be empty before the first removal.

#### [Recognize] Students Unable To Eat Lunch (LeetCode 1700)
<!-- id: sq-students-lunch -->

**Prerequisites.** All three exercises above.

**Problem.** Each student prefers sandwich type 0 or 1. Sandwiches lie in a stack, with `sandwiches[0]` on top. The student at the front of the queue takes the top sandwich if it matches the preference. Otherwise the student moves to the back of the queue. Return the number of students who never take a sandwich.

**Constraints.** The limits are:
- **Length** is `1 <= students.length == sandwiches.length <= 100`.
- **Values** are `0` or `1` in both arrays.
- **Return** is an `int` between `0` and the number of students.

**Example 1.** Input `students = [1,1,1,0]` and `sandwiches = [0,0,1,1]`, output `3`.

**Example 2.** Input `students = [0,1,0,1,1]` and `sandwiches = [1,0,0,1,0]`, output `1`.

**Hint.** When does another trip around the queue stop being able to change anything?

**Changed decision.** The loop stops after as many consecutive misses as the queue length, and no student returns once the top sandwich has no taker.
