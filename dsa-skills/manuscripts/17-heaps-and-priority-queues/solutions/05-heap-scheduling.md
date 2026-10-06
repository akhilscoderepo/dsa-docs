<!-- solutions-for: 05-heap-scheduling -->
### Solutions For Scheduling By Release Time

#### Solution: [Build] Released Shortest Job (Author exercise)
<!-- id: hp-released-shortest-job -->

**Approach.**
The method sorts the job numbers by release time and keeps a queue ordered by duration. Before each selection, it adds every job whose release time is at most the clock. When the queue is empty, the clock jumps to the next release time. The job at the root runs to completion, and its waiting time is the clock at its start minus its release time. Equal durations do not change the total. Two tied jobs occupy the same pair of start slots in either order, so the sum of start times stays the same.

The invariant is that the queue holds exactly the jobs that have arrived and not run.

**Complexity.**
- **Time** is O(n log n), because the sort and the n queue insertions and removals each cost O(log n) per job.
- **Space** is O(n), because the sorted numbers and the queue hold up to n entries.

```java run
import java.util.*;

public final class ReleasedShortestJob {
    /**
     * Returns the sum of waiting times under shortest-arrived-job-first.
     * Time: O(n log n). Space: O(n).
     * Invariant: the queue holds exactly the arrived jobs that have not run.
     */
    static long totalWait(int[] release, int[] duration) {
        int n = release.length;
        Integer[] byRelease = new Integer[n];
        for (int i = 0; i < n; i++) byRelease[i] = i;
        Arrays.sort(byRelease, (a, b) -> Integer.compare(release[a], release[b]));
        // The queue orders by duration; the job number only keeps entries distinct.
        PriorityQueue<int[]> queue = new PriorityQueue<>((a, b) -> a[0] != b[0] ? Integer.compare(a[0], b[0]) : Integer.compare(a[1], b[1]));
        long time = 0, wait = 0;
        int next = 0;
        for (int done = 0; done < n; done++) {
            // An empty queue means the machine idles until the next arrival.
            if (queue.isEmpty() && time < release[byRelease[next]]) time = release[byRelease[next]];
            // Every job released by now joins before the selection.
            while (next < n && release[byRelease[next]] <= time) {
                int i = byRelease[next++];
                queue.offer(new int[] {duration[i], i});
            }
            int[] job = queue.poll();
            // Waiting time is the start time minus the release time.
            wait += time - release[job[1]];
            time += job[0];
        }
        return wait;
    }

    /** Oracle: scan all unfinished jobs at every step and move the clock when nothing has arrived. */
    static long oracle(int[] release, int[] duration) {
        int n = release.length;
        boolean[] done = new boolean[n];
        long time = 0, wait = 0;
        for (int step = 0; step < n; step++) {
            int pick = -1;
            for (int round = 0; round < 2 && pick == -1; round++) {
                for (int i = 0; i < n; i++) {
                    if (done[i] || release[i] > time) continue;
                    if (pick == -1 || duration[i] < duration[pick]) pick = i;
                }
                if (pick == -1) {
                    long earliest = Long.MAX_VALUE;
                    for (int i = 0; i < n; i++) if (!done[i]) earliest = Math.min(earliest, release[i]);
                    time = earliest;
                }
            }
            done[pick] = true;
            wait += time - release[pick];
            time += duration[pick];
        }
        return wait;
    }

    public static void main(String[] args) {
        // Examples from the exercise.
        if (totalWait(new int[] {0, 1, 2}, new int[] {5, 2, 1}) != 8) throw new AssertionError("ex1");
        if (totalWait(new int[] {3, 10}, new int[] {2, 1}) != 0) throw new AssertionError("ex2");
        if (totalWait(new int[0], new int[0]) != 0) throw new AssertionError("empty");
        // Random jobs, unsorted, with ties, must match the scan oracle.
        Random rnd = new Random(1741);
        for (int t = 0; t < 500; t++) {
            int n = rnd.nextInt(9);
            int[] r = new int[n], d = new int[n];
            for (int i = 0; i < n; i++) { r[i] = rnd.nextInt(15); d[i] = 1 + rnd.nextInt(4); }
            if (totalWait(r, d) != oracle(r, d)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Vary] Single-Threaded CPU (LeetCode 1834)
<!-- id: hp-cpu-release-times -->

**Approach.**
The method follows the same loop as the Build exercise and records the task index at each selection. The queue comparator reads the processing time first and the index second, so a tie always goes to the smaller index. When the queue is empty and the next task arrives later, the clock jumps straight to that arrival time. The clock is a `long`, because processing times up to 10^9 add up past the `int` range.

The invariant is that, after the arrivals are added, the queue holds exactly the tasks that can run now.

**Complexity.**
- **Time** is O(n log n), because the sort costs O(n log n) and each task enters and leaves the queue once.
- **Space** is O(n), because the sorted indexes and the queue hold up to n entries.

```java run
import java.util.*;

public final class CpuReleaseTimes {
    /**
     * Returns task indexes in execution order.
     * Time: O(n log n). Space: O(n).
     * Invariant: after arrivals are added, the queue holds exactly the runnable tasks.
     */
    static int[] getOrder(int[][] tasks) {
        int n = tasks.length;
        Integer[] byRelease = new Integer[n];
        for (int i = 0; i < n; i++) byRelease[i] = i;
        Arrays.sort(byRelease, (a, b) -> Integer.compare(tasks[a][0], tasks[b][0]));
        PriorityQueue<int[]> eligible = new PriorityQueue<>((a, b) ->
            a[0] != b[0] ? Integer.compare(a[0], b[0]) : Integer.compare(a[1], b[1]));
        int[] order = new int[n];
        int next = 0;
        long time = 0;
        for (int done = 0; done < n; done++) {
            // Idle jump: nothing can run, so the clock moves to the next arrival.
            if (eligible.isEmpty() && time < tasks[byRelease[next]][0]) time = tasks[byRelease[next]][0];
            // Add every task that has arrived, including all ties on one arrival time.
            while (next < n && tasks[byRelease[next]][0] <= time) {
                int i = byRelease[next++];
                eligible.offer(new int[] {tasks[i][1], i});
            }
            int[] best = eligible.poll();
            order[done] = best[1];
            // The task runs to completion.
            time += best[0];
        }
        return order;
    }

    /** Oracle: advance the clock one unit at a time and scan every task. */
    static int[] oracle(int[][] tasks) {
        int n = tasks.length;
        boolean[] done = new boolean[n];
        int[] order = new int[n];
        long time = 0;
        for (int step = 0; step < n; step++) {
            int pick = -1;
            while (pick == -1) {
                for (int i = 0; i < n; i++) {
                    if (done[i] || tasks[i][0] > time) continue;
                    if (pick == -1 || tasks[i][1] < tasks[pick][1]) pick = i;
                }
                if (pick == -1) time++;
            }
            done[pick] = true;
            order[step] = pick;
            time += tasks[pick][1];
        }
        return order;
    }

    public static void main(String[] args) {
        // Examples from the exercise.
        if (!Arrays.equals(getOrder(new int[][] {{5, 3}, {0, 4}, {2, 2}, {2, 2}}), new int[] {1, 2, 3, 0})) throw new AssertionError("ex1");
        if (!Arrays.equals(getOrder(new int[][] {{7, 1}}), new int[] {0})) throw new AssertionError("ex2");
        // Huge times need a long clock: two tasks of 10^9 after a gap do not overflow.
        int[][] big = {{1_000_000_000, 1_000_000_000}, {1_000_000_000, 1_000_000_000}, {1_000_000_000, 1}};
        if (!Arrays.equals(getOrder(big), new int[] {2, 0, 1})) throw new AssertionError("long clock");
        // Random tasks with ties and gaps must match the unit-step oracle.
        Random rnd = new Random(1742);
        for (int t = 0; t < 500; t++) {
            int[][] a = new int[1 + rnd.nextInt(8)][2];
            for (int[] x : a) { x[0] = rnd.nextInt(12); x[1] = 1 + rnd.nextInt(4); }
            if (!Arrays.equals(getOrder(a), oracle(a))) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Boundary] Idle Gap And Simultaneous Releases (Author exercise)
<!-- id: hp-idle-gap-ties -->

**Approach.**
The loop is the same as in the Vary exercise, and it stores the start time of each job instead of the order. After an idle gap, the clock equals the next release time. The inner loop then adds every job with a release time at most the clock, so jobs that share that time all enter before the first selection. The queue picks the shortest duration among them, and the smaller index breaks a tie. If the loop added only one job at a time, it could start a longer job while a shorter job with the same release time waited outside.

The invariant is that the clock never decreases and that every job released by the clock is in the queue or has run.

**Complexity.**
- **Time** is O(n log n), because the sort and the queue operations cost O(log n) per job.
- **Space** is O(n), because the queue and the start array hold up to n entries.

```java run
import java.util.*;

public final class IdleGapTies {
    /**
     * Returns the start time of each job, shortest duration first, ties by smaller index.
     * Time: O(n log n). Space: O(n).
     * Invariant: every job released by the clock is queued or finished.
     */
    static long[] startTimes(int[][] tasks) {
        int n = tasks.length;
        Integer[] byRelease = new Integer[n];
        for (int i = 0; i < n; i++) byRelease[i] = i;
        Arrays.sort(byRelease, (a, b) -> Integer.compare(tasks[a][0], tasks[b][0]));
        PriorityQueue<int[]> queue = new PriorityQueue<>((a, b) ->
            a[0] != b[0] ? Integer.compare(a[0], b[0]) : Integer.compare(a[1], b[1]));
        long[] start = new long[n];
        int next = 0;
        long time = 0;
        for (int done = 0; done < n; done++) {
            // After an idle gap the clock equals the next release time.
            if (queue.isEmpty() && time < tasks[byRelease[next]][0]) time = tasks[byRelease[next]][0];
            // The loop admits every job that shares this release time before any selection.
            while (next < n && tasks[byRelease[next]][0] <= time) {
                int i = byRelease[next++];
                queue.offer(new int[] {tasks[i][1], i});
            }
            int[] job = queue.poll();
            start[job[1]] = time;
            time += job[0];
        }
        return start;
    }

    /** Oracle: advance the clock one unit at a time and scan every job. */
    static long[] oracle(int[][] tasks) {
        int n = tasks.length;
        boolean[] done = new boolean[n];
        long[] start = new long[n];
        long time = 0;
        for (int step = 0; step < n; step++) {
            int pick = -1;
            while (pick == -1) {
                for (int i = 0; i < n; i++) {
                    if (done[i] || tasks[i][0] > time) continue;
                    if (pick == -1 || tasks[i][1] < tasks[pick][1]) pick = i;
                }
                if (pick == -1) time++;
            }
            done[pick] = true;
            start[pick] = time;
            time += tasks[pick][1];
        }
        return start;
    }

    public static void main(String[] args) {
        // Examples from the exercise.
        if (!Arrays.equals(startTimes(new int[][] {{4, 2}, {4, 1}, {0, 1}}), new long[] {5, 4, 0})) throw new AssertionError("ex1");
        if (!Arrays.equals(startTimes(new int[][] {{3, 2}}), new long[] {3})) throw new AssertionError("ex2");
        if (startTimes(new int[0][]).length != 0) throw new AssertionError("empty");
        // Several jobs on one release time with equal durations resolve by index.
        if (!Arrays.equals(startTimes(new int[][] {{2, 3}, {2, 3}, {2, 3}}), new long[] {2, 5, 8})) throw new AssertionError("ties");
        // Random jobs with gaps and shared release times must match the unit-step oracle.
        Random rnd = new Random(1743);
        for (int t = 0; t < 500; t++) {
            int[][] a = new int[rnd.nextInt(8)][2];
            for (int[] x : a) { x[0] = rnd.nextInt(10); x[1] = 1 + rnd.nextInt(3); }
            if (!Arrays.equals(startTimes(a), oracle(a))) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Recognize] Process Tasks Using Servers (LeetCode 1882)
<!-- id: hp-process-tasks-servers -->

**Approach.**
The method keeps two queues. The free queue orders idle servers by weight and then by index. The busy queue orders running servers by finish time, then weight, then index. For task `j`, the clock becomes the larger of its current value and `j`. If no server is free, the clock jumps to the earliest finish time. The method then moves every busy server whose finish time is at most the clock back to the free queue. The root of the free queue takes the task and enters the busy queue with finish time clock plus duration. The clock never decreases, because a waiting task starts no earlier than the previous task.

The invariant is that every server is in exactly one queue, and the free queue holds exactly the servers idle at the clock.

**Complexity.**
- **Time** is O((n + m) log n) for `n` servers and `m` tasks, because the code makes n initial insertions and at most m moves in each direction, and each move costs O(log n).
- **Space** is O(n), because the two queues together hold each server once.

```java run
import java.util.*;

public final class ProcessTasksServers {
    /**
     * Returns the server index assigned to each task.
     * Time: O((n + m) log n). Space: O(n).
     * Invariant: each server sits in exactly one queue, and the free queue holds the idle servers.
     */
    static int[] assign(int[] servers, int[] tasks) {
        // Free servers: smaller weight first, then smaller index.
        PriorityQueue<int[]> free = new PriorityQueue<>((a, b) ->
            a[0] != b[0] ? Integer.compare(a[0], b[0]) : Integer.compare(a[1], b[1]));
        // Busy servers: finish time {0}, weight {1}, index {2}.
        PriorityQueue<long[]> busy = new PriorityQueue<>((a, b) ->
            a[0] != b[0] ? Long.compare(a[0], b[0]) : a[1] != b[1] ? Long.compare(a[1], b[1]) : Long.compare(a[2], b[2]));
        for (int s = 0; s < servers.length; s++) free.offer(new int[] {servers[s], s});
        int[] result = new int[tasks.length];
        long time = 0;
        for (int j = 0; j < tasks.length; j++) {
            // Task j cannot start before second j.
            time = Math.max(time, j);
            // With no free server, the clock jumps to the earliest finish time.
            if (free.isEmpty()) time = Math.max(time, busy.peek()[0]);
            // Servers that finished by now return to the free queue.
            while (!busy.isEmpty() && busy.peek()[0] <= time) {
                long[] b = busy.poll();
                free.offer(new int[] {(int) b[1], (int) b[2]});
            }
            int[] server = free.poll();
            result[j] = server[1];
            busy.offer(new long[] {time + tasks[j], server[0], server[1]});
        }
        return result;
    }

    /** Oracle: simulate second by second with a waiting list. */
    static int[] oracle(int[] servers, int[] tasks) {
        int n = servers.length, m = tasks.length;
        long[] freeAt = new long[n];
        int[] result = new int[m];
        int assigned = 0;
        for (long sec = 0; assigned < m; sec++) {
            // At second sec, task assigned is waiting if assigned <= sec; serve tasks in index order.
            while (assigned < m && assigned <= sec) {
                int best = -1;
                for (int s = 0; s < n; s++) {
                    if (freeAt[s] > sec) continue;
                    if (best == -1 || servers[s] < servers[best]) best = s;
                }
                if (best == -1) break;
                result[assigned] = best;
                freeAt[best] = sec + tasks[assigned];
                assigned++;
            }
        }
        return result;
    }

    public static void main(String[] args) {
        // Examples from the exercise.
        if (!Arrays.equals(assign(new int[] {3, 1, 1, 2}, new int[] {2, 2, 1, 3, 1}), new int[] {1, 2, 1, 1, 2})) throw new AssertionError("ex1");
        if (!Arrays.equals(assign(new int[] {5}, new int[] {4, 1}), new int[] {0, 0})) throw new AssertionError("ex2");
        // Random inputs must match the second-by-second simulation.
        Random rnd = new Random(1744);
        for (int t = 0; t < 500; t++) {
            int[] sv = new int[1 + rnd.nextInt(4)];
            for (int i = 0; i < sv.length; i++) sv[i] = 1 + rnd.nextInt(3);
            int[] tk = new int[1 + rnd.nextInt(8)];
            for (int i = 0; i < tk.length; i++) tk[i] = 1 + rnd.nextInt(6);
            if (!Arrays.equals(assign(sv, tk), oracle(sv, tk))) throw new AssertionError("random " + t);
        }
    }
}
```
