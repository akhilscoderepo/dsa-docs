<!-- lesson-kind: standard -->
<!-- lesson-id: task-selection -->
## Task Selection

<!-- stage: context -->
### Why A Nightly Runner Misses Its Deadlines

A nightly runner executes batch jobs on one worker. Each job has a duration and a deadline, both in minutes after midnight. The worker runs one job at a time and never pauses a job. A job counts only if it finishes by its deadline. The operator wants as many jobs as possible to count.

On one night a five-minute job with a deadline of minute 5 arrives first. Two two-minute jobs with a deadline of minute 6 follow it. A runner that starts the five-minute job finishes it on time, and then both short jobs miss their deadline. A runner that skips the long job finishes both short jobs on time. This lesson asks which jobs to keep, and how a program changes its mind about a job it already accepted.

<!-- stage: naive -->
### Accepting Jobs In Deadline Order

The direct plan sorts the jobs by deadline. It keeps a running total of accepted durations and accepts a job when the total still fits inside the deadline of that job.

```java
static int acceptInDeadlineOrder(int[][] jobs) {
    int[][] order = jobs.clone();
    Arrays.sort(order, (a, b) -> Integer.compare(a[1], b[1]));   // earlier deadline first
    long total = 0;
    int accepted = 0;
    for (int[] job : order) {                                    // job = {duration, deadline}
        if (total + job[0] <= job[1]) {
            total += job[0];
            accepted++;
        }
    }
    return accepted;
}
```

```predict
Run the method on `[[5,5],[2,6],[2,6]]`, where each pair is duration and deadline. What does it return, and how many jobs can the worker finish on time at best?

It returns 1. The job `[5,5]` comes first and fits, so the method accepts it. Each two-minute job then needs a total of 7, which passes its deadline of 6, so the method rejects both. The worker can finish the two short jobs on time, which gives 2.
```

<!-- stage: bottleneck -->
### Counting The Cost Of A Fixed Decision

The sorted scan runs in O(n log n) time, so cost is not the problem. The method decides each job once and never revisits it. The first accepted job keeps its place even after later jobs show that a smaller choice would have served better.

Trying every subset would find the best answer, but it needs O(2^n) time. A middle road exists. The program keeps the order by deadline, but it lets an accepted job leave the set later. The open question is which accepted job to drop, so that the set stays as good as possible.

<!-- stage: insight -->
### Keeping A Set That Can Always Shrink

#### One Capacity And A Value Per Unit

Start with the simpler case that has no deadlines. A truck holds a fixed number of boxes, and each box type has a count and a number of units per box. Take the box type with the most units per box first, and continue down the list until the truck is full. Swapping a box of fewer units for a box of more units never lowers the total and never changes the number of boxes, so the sorted order is safe.

#### Processing By Deadline

Now add deadlines. The **deadline order** sorts the jobs by deadline. When the scan reaches a job, every job processed before it has an earlier or equal deadline. The scan keeps a **retained set**, the jobs that are currently accepted and finish on time if they run in deadline order.

Add the new job to the retained set. If the total duration still fits inside the deadline of the new job, every retained job still finishes on time, because the new job has the latest deadline. If the total no longer fits, the set must lose one job.

#### The Replacement Rule

The **replacement rule** says to drop the retained job with the longest duration. That job may be the new one. Dropping the longest job lowers the total by the largest amount, and it removes exactly one job, so the count is as large as it can be. Any other drop leaves a larger total, and a larger total can only hurt later jobs. A max-heap of the retained durations finds the longest job in O(log n).

<!-- names: deadline order, retained set, replacement rule -->

<!-- stage: variables -->
### What The Scan Remembers

The scan needs a sorted array, a heap, and a sum. Four items describe the state.

- **courses** is the array of pairs `{duration, deadline}`, sorted by deadline.
- **kept** is a max-heap holding the durations of the retained set.
- **total** is the sum of the durations in `kept`, held in a `long`.
- **c** is the job under test, and the test is `total > c[1]` after the job joins the set.

The size of `kept` is the answer at every moment, and the last size is the result.

<!-- stage: trace -->
### Two Scans With Replacement

#### Rejecting The New Job

The first trace uses the jobs `[4,4]`, `[3,9]`, `[2,10]` and `[9,11]` in deadline order. The pointer `i` marks the job under test.

The first three jobs fit, and the total reaches 9. The fourth job raises the total to 18, which passes its deadline of 11. The longest job in the set is the new job with duration 9, so the scan drops it, and the total returns to 9. The scan keeps three jobs.

```trace
{"cells":["4/4","3/9","2/10","9/11"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"total":4,"kept":1},"note":"The job 4 due 4 joins the set, so the total becomes 4. The total fits inside 4, so the job stays."},{"at":{"i":1},"vars":{"total":7,"kept":2},"note":"The job 3 due 9 joins the set, so the total becomes 7. The total fits inside 9, so the job stays."},{"at":{"i":2},"vars":{"total":9,"kept":3},"note":"The job 2 due 10 joins the set, so the total becomes 9. The total fits inside 10, so the job stays."},{"at":{"i":3},"vars":{"total":9,"kept":3},"note":"The job 9 due 11 joins the set, so the total becomes 18. The total passes 11, so the scan drops the longest duration 9, and the total becomes 9."}]}
```

#### Replacing An Older Job

The second trace uses `[5,5]`, `[2,6]` and `[2,6]`, the input that broke the sorted scan. The first job fits. The second job raises the total to 7, which passes its deadline of 6. The longest job is the retained job with duration 5, so the scan drops that one and keeps the new job. The third job then fits, and the scan keeps two jobs.

```trace
{"cells":["5/5","2/6","2/6"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"total":5,"kept":1},"note":"The job 5 due 5 joins the set, so the total becomes 5. The total fits inside 5, so the job stays."},{"at":{"i":1},"vars":{"total":2,"kept":1},"note":"The job 2 due 6 joins the set, so the total becomes 7. The total passes 6, so the scan drops the longest duration 5, and the total becomes 2."},{"at":{"i":2},"vars":{"total":4,"kept":2},"note":"The job 2 due 6 joins the set, so the total becomes 4. The total fits inside 6, so the job stays."}]}
```

<!-- stage: code -->
### Keeping Durations In A Max-Heap

```java
static int maxCourses(int[][] courses) {
    int[][] order = courses.clone();
    Arrays.sort(order, (a, b) -> Integer.compare(a[1], b[1]));
    PriorityQueue<Integer> kept = new PriorityQueue<>(Collections.reverseOrder());
    long total = 0;
    for (int[] c : order) {
        kept.add(c[0]);
        total += c[0];
        if (total > c[1]) total -= kept.poll();   // drop the longest retained duration
    }
    return kept.size();
}
```

The scan adds the new duration before it tests the deadline, so the new job competes for removal with the older jobs. The heap uses `Collections.reverseOrder()`, which compares without subtraction. The total is a `long`, so a sum of many large durations does not overflow.

- **Time** is O(n log n), because the sort and the heap operations each cost that much.
- **Space** is O(n) for the heap and the sorted copy.

<!-- stage: applicability -->
### Choosing Which Tasks To Keep

#### Applying The Invariant

Use this method when each task has a cost against a limit, and the goal is to keep as many tasks as possible. The invariant is that the retained tasks are feasible under the constraint processed so far, and no feasible set of the processed tasks has more tasks or a smaller total. State it before you code, and name the replacement rule that keeps it true.

#### Finding Cases That Break The Precondition

A false friend is sorting once and never undoing a choice. That works when every item takes capacity and no deadline interacts with the order, as with the truck. It fails when a later item can only fit if an earlier accepted item leaves. A second false friend is choosing by deadline alone, since a job with the earliest deadline may take far more time than it is worth.

#### Avoiding Java Pitfalls

Use a `long` for the running total of durations or rewards. Use `Collections.reverseOrder()` for a max-heap and never `(a, b) -> b - a`, which overflows for values with opposite signs. State the tie rule whenever equal values change the returned arrangement, because a heap does not return equal elements in insertion order.

<!-- stage: exercises -->
### Exercises

#### [Build] Maximum Units on a Truck (LeetCode 1710)
<!-- id: gr-maximum-units-truck -->

**Prerequisites.** The one-capacity case in the insight of this lesson.

**Problem.** Array `boxTypes` holds pairs `{count, unitsPerBox}`. A truck holds at most `truckSize` boxes. Return the largest total number of units that the truck can carry.

**Constraints.** The limits are:
- **Count** is `1 <= boxTypes.length <= 1000`.
- **Values** are integers in `1 <= count, unitsPerBox <= 1000`.
- **Capacity** is `1 <= truckSize <= 10^6`.
- **Mutation** of `boxTypes` is allowed.

**Example 1.** Input `boxTypes = [[1,3],[2,2],[3,1]]` and `truckSize = 4`, output 8.

**Example 2.** Input `boxTypes = [[2,4],[3,6],[1,9]]` and `truckSize = 5`, output 31.

**Hint.** Which box type should leave the sorted list first?

**Changed decision.** The method sorts by units per box and fills the truck.

#### [Vary] Deadline-Compatible Unit Tasks (Author exercise)
<!-- id: gr-deadline-unit-tasks -->

**Prerequisites.** The retained set of this lesson.

**Problem.** Each task takes exactly one time unit. Array `deadlines` holds one deadline per task. A task with deadline `d` must run in one of the slots `1, 2, ..., d`. Each slot runs at most one task. Return the largest number of tasks that run.

**Constraints.** The limits are:
- **Count** is `0 <= deadlines.length <= 10^5`.
- **Values** are integers in `1 <= d <= 10^9`.
- **Slots** are numbered from 1 and cannot hold two tasks.
- **Mutation** of the array is allowed.

**Example 1.** Input `deadlines = [2,1,2]`, output 2.

**Example 2.** Input `deadlines = [1,1,1]`, output 1.

**Hint.** After sorting, how many tasks have been accepted when a new deadline arrives?

**Changed decision.** Every duration is one, so no task needs to leave the set.

#### [Boundary] Equal Reward And Capacity Limit (Author exercise)
<!-- id: gr-equal-reward-capacity -->

**Prerequisites.** The first exercise and the Java notes of this lesson.

**Problem.** Arrays `counts` and `rewards` describe `n` item types. Type `i` has `counts[i]` units, and each unit earns `rewards[i]`. A bag holds at most `capacity` units. Take units from the type with the largest reward first, and break equal rewards by the smaller type index. Return a `long` array of length `n + 1`. Entry `i` is the number of units taken from type `i`, and the last entry is the total reward.

**Constraints.** The limits are:
- **Count** is `1 <= n <= 10^5`.
- **Values** are integers in `1 <= counts[i], rewards[i], capacity <= 10^9`.
- **Total** reward can reach 10^18, so it needs `long`.
- **Mutation** of the input arrays does not occur.

**Example 1.** Input `counts = [3,2]`, `rewards = [5,5]` and `capacity = 4`, output `[3,1,20]`.

**Example 2.** Input `counts = [1000000000]`, `rewards = [1000000000]` and `capacity = 1000000000`, output `[1000000000,1000000000000000000]`.

**Hint.** What type must the product of a count and a reward use?

**Changed decision.** A tie rule fixes the returned amounts, and the reward needs a wider type.

#### [Recognize] Course Schedule III (LeetCode 630)
<!-- id: gr-course-schedule-iii -->

**Prerequisites.** The replacement rule of this lesson.

**Problem.** Array `courses` holds pairs `{duration, lastDay}`. The student takes one course at a time, starts on day 1 and never pauses a course. A course finishes by its last day or it does not count. Return the largest number of courses that can finish on time.

**Constraints.** The limits are:
- **Count** is `0 <= courses.length <= 10^4`.
- **Values** are integers in `1 <= duration, lastDay <= 10^4`.
- **Order** of the input is arbitrary.
- **Return** is 0 for empty input.

**Example 1.** Input `courses = [[3,6],[4,8],[2,5],[7,20]]`, output 3.

**Example 2.** Input `courses = [[5,5],[2,6],[2,6]]`, output 2.

**Hint.** When the total passes a deadline, which accepted course frees the most time?

**Changed decision.** An accepted course may leave the set when a better choice appears.
