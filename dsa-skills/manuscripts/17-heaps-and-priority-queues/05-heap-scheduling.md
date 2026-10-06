<!-- lesson-kind: standard -->
<!-- lesson-id: heap-scheduling -->
## Run Tasks When They Become Ready

<!-- stage: context -->
### Why Builds Start Before They Exist

A build farm has one machine. Each build request has an arrival time and an estimated duration, and the farm runs the shortest waiting build next to keep the average wait low. The first version sorts all requests by duration once and runs them in that order.

The log then shows builds that start before anyone requested them. The shortest request in the file always runs first, even when it arrives an hour after a long request that the machine could have started. This lesson asks how a program picks the shortest build among those that have already arrived, while the clock moves and new requests keep arriving.

<!-- stage: naive -->
### Scanning All Requests At Every Step

The direct plan keeps a clock. At each step it scans every unfinished request, ignores those that have not arrived, and picks the shortest of the rest. When no request has arrived, it moves the clock to the earliest arrival.

```java
static int pickShortest(int[] release, int[] dur, boolean[] done, long time) {
    int pick = -1;
    for (int i = 0; i < release.length; i++) {
        if (done[i] || release[i] > time) continue;           // skip finished and not yet arrived
        if (pick == -1 || dur[i] < dur[pick]) pick = i;       // strict test keeps the smaller index on ties
    }
    return pick;
}

static int[] runOrderByScan(int[] release, int[] dur) {
    int n = release.length;
    boolean[] done = new boolean[n];
    int[] order = new int[n];
    long time = 0;
    for (int step = 0; step < n; step++) {
        int pick = pickShortest(release, dur, done, time);
        if (pick == -1) {                                     // nothing has arrived, so move the clock
            long earliest = Long.MAX_VALUE;
            for (int i = 0; i < n; i++) if (!done[i]) earliest = Math.min(earliest, release[i]);
            time = earliest;
            pick = pickShortest(release, dur, done, time);
        }
        done[pick] = true;
        order[step] = pick;
        time += dur[pick];                                    // the pick runs to completion
    }
    return order;
}
```

The method gives the right order on every input.

<!-- stage: bottleneck -->
### Counting The Scans

```predict
The farm receives n = 100,000 requests. How many request checks does the scan method perform in the worst case?

Each of the n steps scans all n requests, so it performs about n * n = 10^10 checks. That is O(n^2), and each scan rechecks requests whose state did not change.
```

Each step costs O(n), so the whole schedule costs O(n^2). The repeated work is clear. A request that has not arrived stays unarrived until the clock passes its release time, yet every scan tests it again. A request that has arrived stays arrived, yet every scan retests it and compares its duration with the others.

One global sort cannot replace the scan. Sorting by duration ignores arrival times, and sorting by arrival time ignores durations. The two orders interact, because the shortest request that is eligible depends on the clock. The program needs one structure for arrival order and one for the shortest eligible request.

<!-- stage: insight -->
### Releasing Tasks Into A Queue

The program sorts the request numbers once by arrival time, which gives the **release order**. It also keeps a `PriorityQueue` called the **eligible set**. The eligible set holds every request that has already arrived and has not yet run, ordered by duration and then by request number.

#### Advancing The Clock

Before each selection, the program adds every request from the release order whose arrival time is at most the clock. This includes all requests that share one arrival time, so the queue never picks a request while an equally early request waits outside it. After this step the eligible set holds exactly the requests that can run now.

#### Jumping Over Idle Time

When the eligible set is empty, the machine has nothing to run. The program does an **idle jump**. It sets the clock to the arrival time of the next request in the release order and then adds the arrivals. The clock never ticks one unit at a time, so a gap of a billion time units costs no extra steps.

#### Selecting And Running

The program polls the eligible set, runs that request to completion and adds its duration to the clock. Each request enters the queue once and leaves once, so the schedule costs O(n log n) for the sort and the queue operations.

<!-- names: release order, eligible set, idle jump -->

<!-- stage: variables -->
### The State Of One Schedule

The loop keeps four pieces of state, and each one changes in a known place.

- **Clock** is the current time, a `long` because durations add up beyond the `int` range.
- **Next position** is the index in the release order of the first request not yet added to the queue.
- **Eligible set** is the queue of arrived, unfinished requests, ordered by duration and then by request number.
- **Order** is the output array that records each request number when it runs.

The clock only moves forward, and the next position only moves forward. Both facts keep the total work bounded.

<!-- stage: trace -->
### Following A Schedule With A Gap

#### Choosing Among Arrived Requests

Take four requests as (arrival, duration) pairs. Request 0 is (5, 3), request 1 is (0, 4), and requests 2 and 3 are both (2, 2). The release order is 1, 2, 3, 0. In the first trace the pointer `next` marks the next request in release order, and the cells hold the durations in that order.

The clock starts at 0 and the queue holds request 1 only, so request 1 runs and the clock moves to 4. By then requests 2 and 3 have arrived. They tie on duration, and the smaller number 2 runs first, so the clock moves to 6. Request 0 arrived at 5, so the queue holds requests 3 and 0. Request 3 has duration 2 and runs before request 0 with duration 3.

#### Jumping Over An Idle Gap

The second trace uses requests (4, 2), (4, 1) and (0, 1). The release order is 2, 0, 1. Request 2 runs from time 0 to 1, and then the queue is empty. The clock jumps from 1 to 4, and requests 0 and 1 enter the queue together. Request 1 has the shorter duration and runs first.

#### Stepping Through Both Schedules

```trace
{"cells":[4,2,2,3],"pointers":["next"],"steps":[{"at":{"next":1},"vars":{"start":0,"clock":4,"queue":"[]","order":"[1]"},"note":"The requests [1] have arrived and join the queue. The request 1 has the smallest duration 4 among the arrived requests. It starts at 0 and ends at 4."},{"at":{"next":3},"vars":{"start":4,"clock":6,"queue":"[3]","order":"[1, 2]"},"note":"The requests [2, 3] have arrived and join the queue. The request 2 has the smallest duration 2 among the arrived requests. It starts at 4 and ends at 6."},{"at":{"next":4},"vars":{"start":6,"clock":8,"queue":"[0]","order":"[1, 2, 3]"},"note":"The requests [0] have arrived and join the queue. The request 3 has the smallest duration 2 among the arrived requests. It starts at 6 and ends at 8."},{"at":{"next":4},"vars":{"start":8,"clock":11,"queue":"[]","order":"[1, 2, 3, 0]"},"note":"The request 0 has the smallest duration 3 among the arrived requests. It starts at 8 and ends at 11."}]}
```

```trace
{"cells":[1,2,1],"pointers":["next"],"steps":[{"at":{"next":1},"vars":{"start":0,"clock":1,"queue":"[]","order":"[2]"},"note":"The requests [2] have arrived and join the queue. The request 2 has the smallest duration 1 among the arrived requests. It starts at 0 and ends at 1."},{"at":{"next":3},"vars":{"start":4,"clock":5,"queue":"[0]","order":"[2, 1]"},"note":"The queue is empty, so the clock jumps from 1 to 4. The requests [0, 1] have arrived and join the queue. The request 1 has the smallest duration 1 among the arrived requests. It starts at 4 and ends at 5."},{"at":{"next":3},"vars":{"start":5,"clock":7,"queue":"[]","order":"[2, 1, 0]"},"note":"The request 0 has the smallest duration 2 among the arrived requests. It starts at 5 and ends at 7."}]}
```

<!-- stage: code -->
### Writing The Scheduler In Java

#### One Loop For All Requests

Each request is a pair `{arrival, duration}`. The method returns request numbers in the order the machine runs them.

```java
static int[] runOrder(int[][] tasks) {
    int n = tasks.length;
    Integer[] byRelease = new Integer[n];
    for (int i = 0; i < n; i++) byRelease[i] = i;
    Arrays.sort(byRelease, (a, b) -> Integer.compare(tasks[a][0], tasks[b][0]));    // release order

    PriorityQueue<int[]> eligible = new PriorityQueue<>((a, b) ->
        a[0] != b[0] ? Integer.compare(a[0], b[0]) : Integer.compare(a[1], b[1]));  // duration, then number
    int[] order = new int[n];
    int next = 0;
    long time = 0;
    for (int done = 0; done < n; done++) {
        if (eligible.isEmpty() && time < tasks[byRelease[next]][0]) {
            time = tasks[byRelease[next]][0];                                       // idle jump
        }
        while (next < n && tasks[byRelease[next]][0] <= time) {                     // add every arrival, ties included
            int i = byRelease[next++];
            eligible.offer(new int[] {tasks[i][1], i});
        }
        int[] best = eligible.poll();
        order[done] = best[1];
        time += best[0];                                                            // run to completion
    }
    return order;
}
```

#### Cost Of The Scheduler

The sort costs O(n log n). Each request enters and leaves the queue once, so the loop costs O(n log n) in total. The extra memory is O(n) for the sorted numbers and the queue.

<!-- stage: applicability -->
### Recognizing A Release Time Question

#### Spotting The Pattern

The cue is items that become available over time, with a second priority that chooses among the available ones. The invariant is that, after the clock moves and every released task joins the queue, the queue holds exactly the tasks that can run now.

#### Finding The False Friend

The false friend is one global sort. It looks sufficient, because sorting by duration gives the shortest request first. It ignores arrival times, so it starts requests before they exist. Sorting by arrival and then scanning for the shortest brings back the O(n^2) cost.

A second false friend is a loop that advances the clock one unit at a time. It works for small times and stalls when arrival times reach 10^9.

#### Recognizing The No-Go Cases

This pattern assumes that a started task runs to completion. If a new short task may interrupt a running one, the program needs the remaining duration in the entry and a different event loop. The pattern also needs a fixed rule for equal priorities, or the output differs between runs.

<!-- stage: exercises -->
### Exercises

#### [Build] Released Shortest Job (Author exercise)
<!-- id: hp-released-shortest-job -->

**Prerequisites.** The release order and the eligible set of this lesson.

**Problem.** Given arrays `release` and `duration`, job `i` arrives at time `release[i]` and needs `duration[i]` time units. One machine runs one job at a time without interruption. When the machine is free, it starts the arrived job with the smallest duration. If no job has arrived, it waits for the next arrival. The waiting time of a job is its start time minus its release time. Return the sum of all waiting times.

**Constraints.** The limits are:
- **Length** is `0 <= n <= 10^5`, and the arrays have equal length.
- **Release times** satisfy `0 <= release[i] <= 10^9`, in any order.
- **Durations** satisfy `1 <= duration[i] <= 10^4`.
- **Answer** is a `long`.

**Example 1.** Input `release = [0,1,2]` and `duration = [5,2,1]`, output 8.

**Example 2.** Input `release = [3,10]` and `duration = [2,1]`, output 0.

**Hint.** Which jobs may the queue hold when the clock reads 5? What does the machine do when the queue is empty?

**Changed decision.** The queue admits a job only after its release time passes.

#### [Vary] Single-Threaded CPU (LeetCode 1834)
<!-- id: hp-cpu-release-times -->

**Prerequisites.** The previous exercise and the tuple comparator from the second lesson.

**Problem.** Given a 2D array `tasks`, task `i` has enqueue time `tasks[i][0]` and processing time `tasks[i][1]`. One processor runs one task at a time without interruption. When the processor is idle and no task has arrived, it waits for the next enqueue time. Otherwise it starts the arrived task with the smallest processing time, and a tie goes to the smaller index. Return the task indexes in execution order.

**Constraints.** The limits are:
- **Length** is `1 <= tasks.length <= 10^5`.
- **Enqueue times** satisfy `0 <= tasks[i][0] <= 10^9`.
- **Processing times** satisfy `1 <= tasks[i][1] <= 10^9`.
- **Clock** needs the type `long`, because times add up.

**Example 1.** Input `tasks = [[5,3],[0,4],[2,2],[2,2]]`, output `[1,2,3,0]`.

**Example 2.** Input `tasks = [[7,1]]`, output `[0]`.

**Hint.** What must the program do when the queue is empty and the next task arrives later? Which field breaks a tie among equal processing times?

**Changed decision.** The comparator adds the index as a tie-break, and the clock jumps over idle gaps.

#### [Boundary] Idle Gap And Simultaneous Releases (Author exercise)
<!-- id: hp-idle-gap-ties -->

**Prerequisites.** The two exercises above.

**Problem.** Use the machine of the previous exercise. The arrived job with the smallest duration starts first, and a tie goes to the smaller index. Given `tasks` as `{release, duration}` pairs, return the start time of each job, indexed by job number. All jobs that share one release time must enter the queue before the machine selects.

**Constraints.** The limits are:
- **Length** is `0 <= tasks.length <= 10^5`.
- **Release times** satisfy `0 <= tasks[i][0] <= 10^9`, and several jobs may share one value.
- **Durations** satisfy `1 <= tasks[i][1] <= 10^9`.
- **Answer** is a `long[]` of start times.

**Example 1.** Input `tasks = [[4,2],[4,1],[0,1]]`, output `[5,4,0]`.

**Example 2.** Input `tasks = [[3,2]]`, output `[3]`.

**Hint.** If the program adds only one job per clock value, which job could it pick wrongly? What is the clock after the idle gap?

**Changed decision.** The program adds every job with an arrival at or below the clock before it selects.

#### [Recognize] Process Tasks Using Servers (LeetCode 1882)
<!-- id: hp-process-tasks-servers -->

**Prerequisites.** All three exercises above.

**Problem.** Given an array `servers` of weights and an array `tasks` of durations, task `j` enters a queue at second `j`. Tasks are assigned in order. A task goes to a free server with the smallest weight, and a tie goes to the smaller server index. If no server is free, the task waits until one is free. A server that starts a task at second `t` is free again at second `t + tasks[j]`, and tasks that wait are served in index order. Return the server index of each task.

**Constraints.** The limits are:
- **Servers** number `1 <= servers.length <= 2 * 10^5`, with weights from `1` to `10^5`.
- **Tasks** number `1 <= tasks.length <= 2 * 10^5`, with durations from `1` to `10^5`.
- **Times** need the type `long`.

**Example 1.** Input `servers = [3,1,1,2]` and `tasks = [2,2,1,3,1]`, output `[1,2,1,1,2]`.

**Example 2.** Input `servers = [5]` and `tasks = [4,1]`, output `[0,0]`.

**Hint.** Which two groups of servers does the program need to track? What event moves a server from one group to the other?

**Changed decision.** A second queue holds busy servers ordered by finish time, and servers move back when their finish time passes.
