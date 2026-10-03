<!-- lesson-kind: standard -->
<!-- lesson-id: fifo-simulation -->
## FIFO Simulation

<!-- stage: context -->
### The Print Shop Rota

A print shop has one machine and a stack of job slips pinned to a board in the order they were handed over the counter. The owner promises fairness: whoever came first is served first, and nobody who arrived later may jump ahead. Some jobs are tiny, such as a single poster, and some are huge, such as a whole thesis, so the owner adds a second promise. No job may hog the machine, so the operator prints one page of a job, and if the job still has pages left it goes behind everyone currently waiting.

The owner now wants a small program that predicts, for a given morning, the order in which the jobs will be finished. A job with nothing left to print finishes at once, and the line can run dry in the middle of the morning, so the program must also say what happens then.

<!-- stage: naive -->
### Sweep The Board Round After Round

The direct method keeps the remaining page count of every job in an array and sweeps the board from left to right. In each sweep every unfinished job receives one page, and a job is recorded as finished in the sweep where its count reaches zero.

```java
static int[] finishOrderBySweeps(int[] pages) {
    int n = pages.length;
    int[] left = pages.clone();
    int[] order = new int[n];
    int done = 0;
    boolean[] finished = new boolean[n];
    while (done < n) {
        for (int i = 0; i < n; i++) {
            if (finished[i]) continue;
            if (left[i] > 0) left[i]--;
            if (left[i] == 0) { finished[i] = true; order[done++] = i; }
        }
    }
    return order;
}
```

It is correct, since each sweep visits the jobs in arrival order, and a job that is passed over for being finished does not change the order of the others.

<!-- stage: bottleneck -->
### Finished Jobs Are Still Visited

Each sweep walks all n slots, including slots whose job is long finished, and the number of sweeps equals the largest page count W. The cost is therefore O(n W), even though the real work, one page printed, happens only P times, where P is the total of all page counts. If one thesis has a million pages and ninety thousand posters have one page each, the posters finish in the first sweep, and the remaining million sweeps still walk all ninety thousand empty slots, about ninety billion visits that print nothing.

The sweep forgets who is still waiting and re-derives it by looking at everyone each time. A line that holds only the jobs still waiting would never touch a finished job again, so each printed page would cost a constant amount of work, and the whole morning would cost O(n + P).

<!-- stage: insight -->
### A Line Holds Only Who Still Waits

Keep the waiting jobs in a queue. The **front item** is the next job the machine will serve, and everything else waits behind it in arrival order. A turn removes the front item, prints one page, and then decides its fate: if pages remain it joins the **back of the line**, behind every job that is already waiting, and if nothing remains it is recorded as finished and leaves for good. Because a returning job always goes to the back, the relative order of the waiting jobs is the order in which they will next be served, and no job can overtake another.

The invariant is that the front is the job to process next and every job waiting behind it is in the order of its next turn. Removing the front and appending at the back changes nothing about the order of the others, so the invariant survives every turn. A stack would break it, since the job just served would return to the very top and be served again immediately, which is the opposite of fairness.

Some questions ask whether the line can make progress at all. Suppose each waiting job needs a specific resource and only certain jobs can use the resource available right now. Then a **full rotation** is the signal: if the front item is rejected and moved to the back as many times as there are jobs in the line without any job being accepted, the arrangement is stuck forever, because another pass would repeat exactly the same rejections.

<!-- names: front item, back of the line, full rotation -->

The number of turns is bounded by the total work, and each turn is constant time, so the order of fairness costs nothing extra.

<!-- stage: variables -->
### Queue Of Indices And A Counter

The queue `line` stores job indices and not page counts, so a finished job can be reported by its original identity. The array `left` holds the remaining work for each index, and `order` collects indices in the sequence in which they finish. For the stuck detection, `spins` counts consecutive rejections, and it is reset to zero whenever a job is accepted. The stuck test compares `spins` with `line.size()`, evaluated after every rejection. When a job has zero remaining work on its first turn, it is recorded as finished at once and is never re-enqueued.

<!-- stage: trace -->
### One Page Per Turn, Then Stuck

The first trace has three jobs with 3, 1 and 2 pages, named by their positions 0, 1 and 2, and the machine prints one page per turn. The cells hold the starting page counts, and `front` points at the job being served. The job at position 0 is served first and goes to the back with two pages left. The job at position 1 finishes on its first turn, so it leaves for good and the line shrinks to two.

```trace
{"cells":[3,1,2],"pointers":["front"],"steps":[{"at":{"front":0},"vars":{"line":"[1:1,2:2,0:2]","finished":"[]"},"note":"The job at position 0 prints one page and goes to the back of the line with 2 left."},{"at":{"front":1},"vars":{"line":"[2:2,0:2]","finished":"[1]"},"note":"The job at position 1 prints its last page, so it finishes and leaves the line for good."},{"at":{"front":2},"vars":{"line":"[0:2,2:1]","finished":"[1]"},"note":"The job at position 2 prints one page and goes to the back of the line with 1 left."},{"at":{"front":0},"vars":{"line":"[2:1,0:1]","finished":"[1]"},"note":"The job at position 0 prints one page and goes to the back of the line with 1 left."},{"at":{"front":2},"vars":{"line":"[0:1]","finished":"[1,2]"},"note":"The job at position 2 prints its last page, so it finishes and leaves the line for good."},{"at":{"front":0},"vars":{"line":"[]","finished":"[1,2,0]"},"note":"The job at position 0 prints its last page, so it finishes and leaves the line for good."}]}
```

The second trace is a lunch queue. Students prefer sandwich type 1 or 0, and the sandwiches are a stack whose top is served first. A student takes the top sandwich only if it is the preferred type, and otherwise goes to the back. The cells hold the sandwiches, and `top` points at the one on offer. In the last steps all three remaining students prefer type 1, the top sandwich is type 0, and a full rotation of three rejections proves that nobody can ever eat again.

```trace
{"cells":[0,0,1,1],"pointers":["top"],"steps":[{"at":{"top":0},"vars":{"queue":"[1,1,0,1]","spins":1},"note":"The front student wants type 1, but the top sandwich is type 0, so the student goes to the back and the rejection count is 1."},{"at":{"top":0},"vars":{"queue":"[1,0,1,1]","spins":2},"note":"The front student wants type 1, but the top sandwich is type 0, so the student goes to the back and the rejection count is 2."},{"at":{"top":0},"vars":{"queue":"[0,1,1,1]","spins":3},"note":"The front student wants type 1, but the top sandwich is type 0, so the student goes to the back and the rejection count is 3."},{"at":{"top":0},"vars":{"queue":"[1,1,1]","spins":0},"note":"The front student wants type 0, which matches the top sandwich, so the student eats and the next sandwich is offered."},{"at":{"top":1},"vars":{"queue":"[1,1,1]","spins":1},"note":"The front student wants type 1, but the top sandwich is type 0, so the student goes to the back and the rejection count is 1."},{"at":{"top":1},"vars":{"queue":"[1,1,1]","spins":2},"note":"The front student wants type 1, but the top sandwich is type 0, so the student goes to the back and the rejection count is 2."},{"at":{"top":1},"vars":{"queue":"[1,1,1]","spins":3},"note":"The front student wants type 1, but the top sandwich is type 0, so the student goes to the back and the rejection count is 3. That equals the number of students waiting, so a full rotation made no progress and the line is stuck."}]}
```

<!-- stage: code -->
### Turns, Rotation, And Stuck Detection

```java
static int[] roundRobinFinishOrder(int[] pages) {
    ArrayDeque<Integer> line = new ArrayDeque<>();
    int[] left = pages.clone();
    for (int i = 0; i < pages.length; i++) line.addLast(i);
    int[] order = new int[pages.length];
    int done = 0;
    while (!line.isEmpty()) {
        int job = line.removeFirst();
        if (left[job] > 0) left[job]--;
        if (left[job] == 0) order[done++] = job;
        else line.addLast(job);
    }
    return order;
}

static int studentsUnableToEat(int[] students, int[] sandwiches) {
    ArrayDeque<Integer> line = new ArrayDeque<>();
    for (int s : students) line.addLast(s);
    int top = 0, spins = 0;
    while (!line.isEmpty() && top < sandwiches.length && spins < line.size()) {
        int want = line.removeFirst();
        if (want == sandwiches[top]) { top++; spins = 0; }
        else { line.addLast(want); spins++; }
    }
    return line.size();
}
```

Every turn removes one element and adds at most one, so the first method runs in O(n + P) time with O(n) space. In the second, each rejection is followed by at most a full rotation before a student is served or the loop stops, so it costs O(n^2) in the worst case by this argument, and a count of preferences brings it down to O(n).

<!-- stage: applicability -->
### When Arrival Order Is The Rule

Use a queue when items must be handled in the order they arrived and later arrivals wait behind earlier ones, as in printing, scheduling, buffering and rotation games. The invariant is that the front is the next item to process and every waiting item sits in the order of its next turn.

A false friend is the stack, which reverses arrival order and lets the most recent item starve the rest. A second false friend is a repeated sweep over a fixed array, which gives the same order but revisits finished items and costs the largest work times the number of items. A third is to stop a rotation game when the queue is empty only, and to forget that a line can be stuck while still full.

In Java, store indices when identity matters, and remove before re-adding so that the item never appears twice. Guard each removal with `isEmpty()` in the loop condition, and test the stuck condition against the size after a rejection. A job that already has no work must be finished before any decrement, because decrementing it would produce a negative count.

<!-- stage: exercises -->
### Exercises

#### [Build] Printer Queue (Author exercise)
<!-- id: sq-printer-queue -->

**Prerequisites.** The ArrayDeque Contracts lesson.

**Problem.** Jobs arrive at the printer in index order. Job `i` arrives at minute `arrival[i]` and takes `pages[i]` minutes. The printer serves the waiting jobs strictly in arrival order, and it never idles while a job has arrived. Return the finishing minute of every job, by index.

**Constraints.** 0 <= n <= 100000, 0 <= arrival[i] <= arrival[i + 1] <= 1000000000 and 1 <= pages[i] <= 1000000.

**Example 1.** Input `arrival = [0, 1, 10], pages = [4, 2, 3]`, output `[4, 6, 13]`.

**Example 2.** Input `arrival = [5, 5], pages = [1, 1]`, output `[6, 7]`.

**Hint.** Which job is the next one served after the printer becomes free? When can the printer start it?

**Changed decision.** First rung: the next job is whichever waits at the front, and the start time is the later of the printer becoming free and the job arriving.

#### [Vary] Round-Robin One Step (Author exercise)
<!-- id: sq-round-robin-one-step -->

**Prerequisites.** The Printer Queue rung.

**Problem.** Given the remaining page counts of waiting jobs in line order and a number of turns `t`, run `t` turns. Each turn removes the front job, prints one page of it, and puts it at the back only if pages remain. Stop early if the line becomes empty. Return the remaining page counts of the line from front to back.

**Constraints.** 0 <= n <= 100000, 1 <= left[i] <= 1000000 and 0 <= t <= 1000000000.

**Example 1.** Input `left = [3, 1, 2], t = 4`, output `[1, 1]`.

**Example 2.** Input `left = [1, 1], t = 5`, output `[]`.

**Hint.** What happens to a job that is served while it has exactly one page left? What is the line after the turns it would have taken?

**Changed decision.** A job is re-enqueued only when work remains, so the queue shrinks as tasks finish.

#### [Boundary] Queue Becomes Empty (Author exercise)
<!-- id: sq-queue-becomes-empty -->

**Prerequisites.** The Round-Robin One Step rung.

**Problem.** Run round-robin to the end with a quantum `q`: each turn removes the front job and prints up to `q` pages of it. A job finishes when its remaining pages reach zero, and a job that starts with zero pages finishes on its first turn. Return the job indices in the order they finish.

**Constraints.** 0 <= n <= 100000, 0 <= pages[i] <= 1000000 and 1 <= q <= 1000000.

**Example 1.** Input `pages = [5, 0, 2], q = 2`, output `[1, 2, 0]`.

**Example 2.** Input `pages = [], q = 3`, output `[]`.

**Hint.** Which check must come before any decrement? When is it safe to call `removeFirst`?

**Changed decision.** The loop must treat zero work as already done, and every removal sits behind an emptiness check in the loop condition.

#### [Recognize] Number of Students Unable to Eat Lunch (LeetCode 1700)
<!-- id: sq-students-unable-lunch -->

**Prerequisites.** The Queue Becomes Empty rung.

**Problem.** Students stand in a queue, and each prefers sandwich type 0 or 1. Sandwiches lie in a stack, with the one at index 0 on top. The front student takes the top sandwich if it matches the preference, and otherwise moves to the back. Return how many students never eat. Stop when a full rotation of the queue makes no progress.

**Constraints.** students.length == sandwiches.length, 1 <= students.length <= 100 and each value is 0 or 1.

**Example 1.** Input `students = [0, 1, 0, 1, 1], sandwiches = [1, 0, 1, 0, 1]`, output `0`.

**Example 2.** Input `students = [1, 1, 1, 1], sandwiches = [0, 1, 1, 1]`, output `4`.

**Hint.** How many consecutive rejections prove that nobody will ever be served? What resets that count?

**Changed decision.** The loop ends when a rejection count equals the queue length, since another pass would repeat the same rejections.
