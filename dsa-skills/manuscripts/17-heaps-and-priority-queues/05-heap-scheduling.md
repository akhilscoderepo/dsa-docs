<!-- lesson-kind: standard -->
<!-- lesson-id: heap-scheduling -->
## Heap Scheduling

<!-- stage: context -->
### The One-Machine Film Booth

A photo booth at a seaside market has one developing machine. Customers drop off their film rolls at various times of the day, and each roll needs a known number of minutes in the machine. When the machine becomes free, the attendant looks at the rolls that have already been dropped off and starts the one that takes the least time, because that keeps the average wait of the people at the counter down. If two rolls take equally long she starts the one with the lower ticket number.

Some mornings the machine is idle for an hour before the first customer arrives, and in the afternoon five people sometimes arrive in the same minute. The attendant handles those cases by instinct. The market's committee wants the same behaviour written down as a program, so that the day's order of work can be printed in advance from the list of drop-off times and processing times, with no mistakes about who goes first.

<!-- stage: naive -->
### Rescan The Counter At Every Start

The direct method simulates the machine. Whenever it is free, it scans all rolls, ignores those already done or not yet dropped off, and picks the best remaining one by the attendant's rule. If nothing is available it moves the clock to the earliest drop-off time that is still waiting.

```java
static int[] orderByScan(int[][] rolls) {          // rolls[i] = {dropOff, minutes}
    int n = rolls.length;
    boolean[] done = new boolean[n];
    int[] order = new int[n];
    long clock = 0;
    for (int step = 0; step < n; step++) {
        int pick = -1;
        long earliest = Long.MAX_VALUE;
        for (int i = 0; i < n; i++) {
            if (done[i]) continue;
            earliest = Math.min(earliest, rolls[i][0]);
            if (rolls[i][0] > clock) continue;
            if (pick < 0 || rolls[i][1] < rolls[pick][1]) pick = i;
        }
        if (pick < 0) { clock = earliest; step--; continue; }
        done[pick] = true;
        clock += rolls[pick][1];
        order[step] = pick;
    }
    return order;
}
```

It is correct. For the rolls `{1, 3}, {2, 2}, {2, 1}` it returns `[0, 2, 1]`.

<!-- stage: bottleneck -->
### Each Start Reads Every Roll

Every start scans all `n` rolls, so the cost is O(n^2) in total, and a day with a hundred thousand rolls needs ten billion looks. The scan also keeps testing rolls that have not yet arrived and rolls that are already finished, although those can never be chosen at this moment. Only the dropped-off and unfinished rolls matter, and they are exactly the ones for which the best must be found, again and again, while newcomers appear.

A single sort of all rolls cannot replace the scan. Sorting by minutes ignores whether a roll has arrived, and sorting by drop-off time ignores which roll is shortest. The two criteria apply at different moments: the arrival time decides who is a candidate, and the processing time decides who among the candidates goes first, and the set of candidates changes with the clock. Stepping the clock one minute at a time, to avoid reasoning about gaps, would cost time proportional to the length of the day, which could be 10^9 minutes.

<!-- stage: insight -->
### Admit First, Then Choose

Handle the two criteria with two structures. Sort the rolls once by drop-off time, which gives the **release sweep**: a pointer that moves along the sorted list and admits rolls as the clock reaches them. Admitted rolls go into the **ready heap**, a min-heap ordered by the selection rule, here the pair of minutes and ticket number. The root of the ready heap is always the roll to start next.

The loop is a fixed sequence. If the ready heap is empty and the next roll has not arrived, make the **clock jump** straight to its drop-off time, which skips the idle gap in one step. Then admit every roll whose drop-off time is at most the clock, all of them, including all that share one minute. Then poll the ready heap, start that roll, and add its minutes to the clock.

<!-- names: release sweep, ready heap, clock jump -->

The invariant is that after the jump and the admission, the ready heap contains exactly the rolls that are dropped off and not yet started, so its root is the best executable roll. Admitting only some of the rolls that are tied on the clock would break it, since a shorter roll could be left outside. Each roll is admitted once and polled once, the sort costs O(n log n), and each heap operation costs O(log n), so the whole schedule costs O(n log n) time with O(n) memory. The clock is a `long`, because a sum of many large durations may pass the range of an `int`.

<!-- stage: variables -->
### Clock, Pointer And Ready Heap

The `clock` is the time at which the machine next becomes free, and it changes in exactly two ways: it jumps forward to the next drop-off when the ready heap is empty, and it grows by the duration of each started roll. It never moves backward. The pointer `next` counts the rolls admitted so far in drop-off order, and it advances inside the admission loop only. The ready heap holds `{minutes, ticket}` pairs for admitted and unstarted rolls, so its size can rise and fall. The output position advances once per start. When the heap is empty at the start of an iteration, at least one roll has not been admitted yet, since otherwise the loop would already be over, and therefore the pointer can be read safely.

<!-- stage: trace -->
### A Jump, A Crowd And A Gap

The first run has five rolls. Their drop-off times, in sorted order, are `1, 2, 2, 8, 20`, and their minutes are 3, 2, 1, 2 and 1 for tickets 0 to 4. At the start the clock is 0, nothing has arrived, and the clock jumps to 1. Roll 0 is admitted and runs until the clock reads 4. By then rolls 1 and 2 have arrived, and the shorter roll 2 starts first. Roll 1 follows and ends at 7. The ready heap is empty again, and the clock jumps to 8 for roll 3, and then to 20 for roll 4.

The second run has four rolls that are all dropped off at minute 5, with minutes 4, 2, 2 and 1. The clock jumps to 5, all four are admitted before anything starts, and they leave in the order 3, 1, 2, 0. The step to study is the first start of the second run: the shortest roll is chosen only because the whole crowd was admitted first.

```trace
{"cells":[1,2,2,8,20],"pointers":["next"],"steps":[{"at":{"next":1},"vars":{"clock":4,"ready":"[]","order":"[0]"},"note":"The ready heap is empty, so the clock jumps from 0 to 1. Admitted: ticket 0. Ticket 0 has the least minutes (3) among the ready rolls and starts at 1. The clock is now 4."},{"at":{"next":3},"vars":{"clock":5,"ready":"[(2,t1)]","order":"[0,2]"},"note":"Admitted: tickets 1, 2. Ticket 2 has the least minutes (1) among the ready rolls and starts at 4. The clock is now 5."},{"at":{"next":3},"vars":{"clock":7,"ready":"[]","order":"[0,2,1]"},"note":"Ticket 1 has the least minutes (2) among the ready rolls and starts at 5. The clock is now 7."},{"at":{"next":4},"vars":{"clock":10,"ready":"[]","order":"[0,2,1,3]"},"note":"The ready heap is empty, so the clock jumps from 7 to 8. Admitted: ticket 3. Ticket 3 has the least minutes (2) among the ready rolls and starts at 8. The clock is now 10."},{"at":{"next":5},"vars":{"clock":21,"ready":"[]","order":"[0,2,1,3,4]"},"note":"The ready heap is empty, so the clock jumps from 10 to 20. Admitted: ticket 4. Ticket 4 has the least minutes (1) among the ready rolls and starts at 20. The clock is now 21."}]}
```

```trace
{"cells":[5,5,5,5],"pointers":["next"],"steps":[{"at":{"next":4},"vars":{"clock":6,"ready":"[(2,t1),(2,t2),(4,t0)]","order":"[3]"},"note":"The ready heap is empty, so the clock jumps from 0 to 5. Admitted: tickets 0, 1, 2, 3. Ticket 3 has the least minutes (1) among the ready rolls and starts at 5. The clock is now 6."},{"at":{"next":4},"vars":{"clock":8,"ready":"[(2,t2),(4,t0)]","order":"[3,1]"},"note":"Ticket 1 has the least minutes (2) among the ready rolls and starts at 6. The clock is now 8."},{"at":{"next":4},"vars":{"clock":10,"ready":"[(4,t0)]","order":"[3,1,2]"},"note":"Ticket 2 has the least minutes (2) among the ready rolls and starts at 8. The clock is now 10."},{"at":{"next":4},"vars":{"clock":14,"ready":"[]","order":"[3,1,2,0]"},"note":"Ticket 0 has the least minutes (4) among the ready rolls and starts at 10. The clock is now 14."}]}
```

<!-- stage: code -->
### Scheduling With A Ready Heap

```java
static int[] scheduleOrder(int[][] jobs) {          // jobs[i] = {release, duration}
    int n = jobs.length;
    int[][] sorted = new int[n][];
    for (int i = 0; i < n; i++) sorted[i] = new int[]{jobs[i][0], jobs[i][1], i};
    java.util.Arrays.sort(sorted, (x, y) -> Integer.compare(x[0], y[0]));
    java.util.PriorityQueue<int[]> ready = new java.util.PriorityQueue<>(
        (x, y) -> x[1] != y[1] ? Integer.compare(x[1], y[1]) : Integer.compare(x[2], y[2]));
    int[] order = new int[n];
    long clock = 0;
    int next = 0;
    for (int done = 0; done < n; done++) {
        if (ready.isEmpty() && clock < sorted[next][0]) clock = sorted[next][0];   // jump
        while (next < n && sorted[next][0] <= clock) ready.offer(sorted[next++]);  // admit all
        int[] job = ready.poll();
        clock += job[1];
        order[done] = job[2];
    }
    return order;
}
```

The sort costs O(n log n), and the loop performs `n` polls and `n` offers of logarithmic cost, so the method runs in O(n log n) time and O(n) memory. The read of `sorted[next]` in the jump line is safe because the heap is empty only while some job is still waiting to be admitted. The comparisons use `Integer.compare` on every field, and the clock is a `long`, so an `int` overflow cannot occur through the accumulating durations.

<!-- stage: applicability -->
### When Eligibility Changes With Time

Use a sorted release list and a ready heap when each item has an availability time, and the next item to run is the best one under a second criterion among those already available. The invariant to state is that, after advancing the clock and admitting every released item, the heap holds exactly the executable items. The same loop appears in job schedulers, in simulations of servers, and in problems that say an item cannot be used before a given moment.

The false friend is a single sort. A sort by availability alone loses the second criterion, and a sort by the second criterion alone ignores who has arrived, so one global order cannot express a rule that depends on the clock. Another false friend is a greedy pick among all items that ignores the clock, which may choose an item that is not yet allowed to start. A third is a loop that advances the clock by one unit, which is correct but costs time in proportion to the span of the clock and not to the number of items.

Do not use it when items can be interrupted and resumed by a newcomer with higher priority, because the remaining time then changes and the ordering key goes stale. In that case the chosen item is pushed back with its updated remainder at each arrival. In Java, keep clock values in `long`, admit all tied releases before polling, and read the next release only when an unadmitted item is known to exist.

<!-- stage: exercises -->
### Exercises

#### [Build] Released Shortest Job (Author exercise)
<!-- id: hp-released-shortest-job -->

**Prerequisites.** The release sweep, the ready heap and the admission loop of this lesson.

**Problem.** Each job has a release time and a duration. One machine starts at time 0 and runs one job at a time without stopping. Whenever it is free it starts the shortest released and unstarted job. Return the durations in the order the jobs are run. It is guaranteed that when the machine finishes a job, some unstarted job has already been released, so it never waits.

**Constraints.** 1 <= jobs.length <= 10^5, 0 <= release <= 10^9, 1 <= duration <= 10^4, and the machine never idles. Jobs with equal durations are interchangeable in the answer.

**Example 1.** Input `jobs = [[0, 5], [1, 2], [2, 1], [3, 3]]`, output `[5, 1, 2, 3]`.

**Example 2.** Input `jobs = [[0, 2]]`, output `[2]`.

**Hint.** Which jobs are candidates at the moment a job ends? What is the clock after you start a job of duration `d`?

**Changed decision.** First rung: only the sweep and the heap, with no idle gap and no ties to resolve by index.

#### [Vary] Single-Threaded CPU (LeetCode 1834)
<!-- id: hp-cpu-wait-report -->

**Prerequisites.** Released Shortest Job above, and the tuple comparator from the orientation lesson.

**Problem.** Task `i` is `tasks[i] = [enqueueTime, processingTime]`. A single processor, free at time 0, starts the available task with the smallest processing time and, for equal times, the smaller index, and it waits for the next enqueue time when nothing is available. The waiting time of a task is its start time minus its enqueue time. Return `[finish time of the last task, number of times the clock jumped over an idle gap, counting the wait before the first task, index of the task with the longest waiting time]`, with the smallest index chosen among equal waits.

**Constraints.** 1 <= tasks.length <= 10^5 and 1 <= enqueueTime, processingTime <= 10^9, so every time value needs a `long`.

**Example 1.** Input `tasks = [[1, 3], [2, 2], [2, 1], [8, 2], [20, 1]]`, output `[21, 3, 1]`.

**Example 2.** Input `tasks = [[1, 4], [1, 4]]`, output `[9, 1, 1]`.

**Hint.** Which moment is a jump, and which is simply the next start? What decides which of two tasks with equal waiting times is reported?

**Changed decision.** Index tie-breaking and idle jumps both enter the loop, and the answer reports facts about the schedule and not the order itself.

#### [Boundary] Idle Gap And Simultaneous Releases (Author exercise)
<!-- id: hp-idle-gap-simultaneous -->

**Prerequisites.** The two exercises above.

**Problem.** Given jobs as `[release, duration]` pairs, schedule them with the shortest-duration rule and index tie-break, and return the start time of each job in the order they are run.

**Constraints.** 1 <= jobs.length <= 10^5, 1 <= release <= 10^9, 1 <= duration <= 10^9, so start times need a `long`. Several jobs may share a release time.

**Example 1.** Input `jobs = [[5, 4], [5, 2], [5, 2], [5, 1]]`, output `[5, 6, 8, 10]`.

**Example 2.** Input `jobs = [[1, 1], [1000000000, 1]]`, output `[1, 1000000000]`.

**Hint.** When the heap is empty, to what value should the clock be set, and how many jobs must be admitted at that value before the first poll?

**Changed decision.** The empty heap must trigger a direct jump over a very long gap, and every tied release must be admitted before one job is chosen.

#### [Recognize] Process Tasks Using Servers (LeetCode 1882)
<!-- id: hp-process-tasks-servers -->

**Prerequisites.** All three exercises above.

**Problem.** There are servers with weights `servers[i]` and tasks `tasks[j]`, where task `j` arrives at second `j` and needs `tasks[j]` seconds. Tasks wait in arrival order. At any second, a waiting task is given the free server with the smallest weight, with the smaller index for equal weights, and that server is busy for the task's duration and is free again at the end of it. If no server is free, the first waiting task starts when the earliest server frees up. Return, for each task, the index of the server that runs it.

**Constraints.** 1 <= servers.length, tasks.length <= 2 * 10^5 and 1 <= servers[i], tasks[j] <= 2 * 10^5.

**Example 1.** Input `servers = [5, 1, 1, 4]`, `tasks = [3, 1, 2, 2, 1, 4, 1]`, output `[1, 2, 2, 1, 2, 1, 2]`.

**Example 2.** Input `servers = [2]`, `tasks = [1, 1]`, output `[0, 0]`.

**Hint.** One queue holds the free servers and another holds the busy ones. By which key is the busy queue ordered, and when do its entries move back?

**Changed decision.** Two heaps now exchange items: servers leave the free heap when they start a task and return from the busy heap when their finish time is reached.
