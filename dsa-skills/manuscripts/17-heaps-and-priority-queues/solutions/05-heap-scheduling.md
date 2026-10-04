<!-- solutions-for: 05-heap-scheduling -->
### Heap Scheduling

#### Solution: [Build] Released Shortest Job (Author exercise)
<!-- id: hp-released-shortest-job -->

**Approach.** Sort the jobs by release time and sweep a pointer along them. After each job ends, admit every job whose release time is at most the clock into a min-heap of durations, then poll the shortest and advance the clock by it. The guarantee that the machine never idles means the heap is never empty at a poll, and no jump is needed. Both examples are asserted. The random cases are filtered by a helper that proves the never-idle guarantee on each generated input, and the output is then compared with a scan-based simulation that looks at every job at every start.

**Complexity.** The sort and the heap operations give O(n log n) time, and the heap and the sorted copy need O(n) memory.

```java run
import java.util.Arrays;
import java.util.PriorityQueue;
import java.util.Random;

public final class ReleasedShortestJob {
    static int[] runOrder(int[][] jobs) {
        int n = jobs.length;
        int[][] byRelease = jobs.clone();
        Arrays.sort(byRelease, (x, y) -> Integer.compare(x[0], y[0]));
        PriorityQueue<Integer> shortest = new PriorityQueue<>();
        int[] out = new int[n];
        long clock = 0;
        int next = 0;
        for (int i = 0; i < n; i++) {
            while (next < n && byRelease[next][0] <= clock) shortest.offer(byRelease[next++][1]);
            int d = shortest.poll();
            out[i] = d;
            clock += d;
        }
        return out;
    }

    // returns null when the machine would have to wait, otherwise the scan-based order of durations
    static int[] scanOrder(int[][] jobs) {
        int n = jobs.length;
        boolean[] used = new boolean[n];
        int[] out = new int[n];
        long clock = 0;
        for (int step = 0; step < n; step++) {
            int best = -1;
            for (int i = 0; i < n; i++) {
                if (used[i] || jobs[i][0] > clock) continue;
                if (best < 0 || jobs[i][1] < jobs[best][1]) best = i;
            }
            if (best < 0) return null;
            used[best] = true;
            clock += jobs[best][1];
            out[step] = jobs[best][1];
        }
        return out;
    }

    public static void main(String[] args) {
        if (!Arrays.equals(runOrder(new int[][]{{0, 5}, {1, 2}, {2, 1}, {3, 3}}), new int[]{5, 1, 2, 3})) throw new AssertionError("example 1");
        if (!Arrays.equals(runOrder(new int[][]{{0, 2}}), new int[]{2})) throw new AssertionError("example 2");
        Random rnd = new Random(1751);
        int valid = 0;
        for (int t = 0; t < 8000; t++) {
            int n = 1 + rnd.nextInt(8);
            int[][] jobs = new int[n][2];
            for (int i = 0; i < n; i++) { jobs[i][0] = rnd.nextInt(10); jobs[i][1] = 1 + rnd.nextInt(4); }
            int[] expected = scanOrder(jobs);
            if (expected == null) continue;
            valid++;
            if (!Arrays.equals(runOrder(jobs), expected)) throw new AssertionError("wrong order for " + Arrays.deepToString(jobs));
        }
        if (valid < 500) throw new AssertionError("too few never-idle cases: " + valid);
    }
}
```

#### Solution: [Vary] Single-Threaded CPU (LeetCode 1834)
<!-- id: hp-cpu-wait-report -->

**Approach.** Keep the sweep and the ready heap, now ordered by processing time and then index, and track three facts while running. Whenever the heap is empty and the clock is behind the next enqueue time, the clock jumps and a counter goes up by one. The start time of each polled task gives its waiting time, which is the start minus the enqueue time, and a strictly greater wait replaces the current best, so among equal waits the first task found with that value in processing order is kept, and a final scan fixes the smallest index. The clock is a `long`. Both examples are asserted, a case with durations near 10^9 shows a finish time above the `int` range, and a slow simulation that scans every task at every start is the oracle on random inputs.

**Complexity.** The time is O(n log n) and the memory is O(n).

```java run
import java.util.Arrays;
import java.util.PriorityQueue;
import java.util.Random;

public final class CpuWaitReport {
    static long[] report(int[][] tasks) {
        int n = tasks.length;
        long[][] sorted = new long[n][];
        for (int i = 0; i < n; i++) sorted[i] = new long[]{tasks[i][0], tasks[i][1], i};
        Arrays.sort(sorted, (x, y) -> Long.compare(x[0], y[0]));
        PriorityQueue<long[]> ready = new PriorityQueue<>(
            (x, y) -> x[1] != y[1] ? Long.compare(x[1], y[1]) : Long.compare(x[2], y[2]));
        long[] wait = new long[n];
        long clock = 0;
        long jumps = 0;
        int next = 0;
        for (int done = 0; done < n; done++) {
            if (ready.isEmpty() && clock < sorted[next][0]) { clock = sorted[next][0]; jumps++; }
            while (next < n && sorted[next][0] <= clock) ready.offer(sorted[next++]);
            long[] task = ready.poll();
            wait[(int) task[2]] = clock - task[0];
            clock += task[1];
        }
        int worst = 0;
        for (int i = 1; i < n; i++) if (wait[i] > wait[worst]) worst = i;
        return new long[]{clock, jumps, worst};
    }

    static long[] slow(int[][] tasks) {
        int n = tasks.length;
        boolean[] used = new boolean[n];
        long[] wait = new long[n];
        long clock = 0, jumps = 0;
        int started = 0;
        while (started < n) {
            int best = -1;
            long soonest = Long.MAX_VALUE;
            for (int i = 0; i < n; i++) {
                if (used[i]) continue;
                soonest = Math.min(soonest, tasks[i][0]);
                if (tasks[i][0] > clock) continue;
                if (best < 0 || tasks[i][1] < tasks[best][1]) best = i;
            }
            if (best < 0) { clock = soonest; jumps++; continue; }
            used[best] = true;
            wait[best] = clock - tasks[best][0];
            clock += tasks[best][1];
            started++;
        }
        int worst = 0;
        for (int i = 1; i < n; i++) if (wait[i] > wait[worst]) worst = i;
        return new long[]{clock, jumps, worst};
    }

    public static void main(String[] args) {
        if (!Arrays.equals(report(new int[][]{{1, 3}, {2, 2}, {2, 1}, {8, 2}, {20, 1}}), new long[]{21, 3, 1})) throw new AssertionError("example 1");
        if (!Arrays.equals(report(new int[][]{{1, 4}, {1, 4}}), new long[]{9, 1, 1})) throw new AssertionError("example 2");
        long[] big = report(new int[][]{{1_000_000_000, 1_000_000_000}, {1_000_000_000, 1_000_000_000}, {1_000_000_000, 1_000_000_000}});
        if (big[0] != 4_000_000_000L || big[0] <= Integer.MAX_VALUE) throw new AssertionError("finish time must exceed the int range, got " + big[0]);
        Random rnd = new Random(1752);
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(9);
            int[][] tasks = new int[n][2];
            for (int i = 0; i < n; i++) { tasks[i][0] = 1 + rnd.nextInt(12); tasks[i][1] = 1 + rnd.nextInt(4); }
            if (!Arrays.equals(report(tasks), slow(tasks))) throw new AssertionError("report differs on " + Arrays.deepToString(tasks));
        }
    }
}
```

#### Solution: [Boundary] Idle Gap And Simultaneous Releases (Author exercise)
<!-- id: hp-idle-gap-simultaneous -->

**Approach.** When the heap is empty, assign the next release time to the clock in one statement, so a gap of a billion units costs one step. Then admit with a `while` loop every job whose release time is at most the clock, which includes all jobs that share the release time, and only then poll. The start time of each polled job is recorded. The harness asserts both examples and runs a flawed variant that admits a single job after a jump. That variant gives a different answer on the first example, which is why the loop must admit every tied release. A scan-based simulation checks random inputs with many equal release times, and a very large gap is run to show that the work does not depend on the length of the gap.

**Complexity.** The sort and the heap give O(n log n) time with O(n) memory, and a gap in the clock costs a constant number of steps.

```java run
import java.util.Arrays;
import java.util.PriorityQueue;
import java.util.Random;

public final class IdleGapSimultaneous {
    static long[] starts(int[][] jobs, boolean admitAllTies) {
        int n = jobs.length;
        Integer[] byRelease = new Integer[n];
        for (int i = 0; i < n; i++) byRelease[i] = i;
        Arrays.sort(byRelease, (x, y) -> Integer.compare(jobs[x][0], jobs[y][0]));
        PriorityQueue<Integer> ready = new PriorityQueue<>(
            (x, y) -> jobs[x][1] != jobs[y][1] ? Integer.compare(jobs[x][1], jobs[y][1]) : Integer.compare(x, y));
        long[] out = new long[n];
        long clock = 0;
        int next = 0;
        for (int k = 0; k < n; k++) {
            boolean jumped = false;
            if (ready.isEmpty()) {
                clock = Math.max(clock, jobs[byRelease[next]][0]);
                jumped = true;
            }
            if (jumped && !admitAllTies) ready.offer(byRelease[next++]);
            else while (next < n && jobs[byRelease[next]][0] <= clock) ready.offer(byRelease[next++]);
            int job = ready.poll();
            out[k] = clock;
            clock += jobs[job][1];
        }
        return out;
    }

    static long[] slow(int[][] jobs) {
        int n = jobs.length;
        boolean[] used = new boolean[n];
        long[] out = new long[n];
        long clock = 0;
        for (int k = 0; k < n; k++) {
            long soonest = Long.MAX_VALUE;
            for (int i = 0; i < n; i++) if (!used[i]) soonest = Math.min(soonest, jobs[i][0]);
            clock = Math.max(clock, soonest);
            int best = -1;
            for (int i = 0; i < n; i++) {
                if (used[i] || jobs[i][0] > clock) continue;
                if (best < 0 || jobs[i][1] < jobs[best][1]) best = i;
            }
            used[best] = true;
            out[k] = clock;
            clock += jobs[best][1];
        }
        return out;
    }

    public static void main(String[] args) {
        int[][] crowd = {{5, 4}, {5, 2}, {5, 2}, {5, 1}};
        if (!Arrays.equals(starts(crowd, true), new long[]{5, 6, 8, 10})) throw new AssertionError("example 1");
        if (Arrays.equals(starts(crowd, false), new long[]{5, 6, 8, 10})) throw new AssertionError("admitting one tied job must give a different schedule");
        if (!Arrays.equals(starts(new int[][]{{1, 1}, {1_000_000_000, 1}}, true), new long[]{1, 1_000_000_000})) throw new AssertionError("example 2");
        Random rnd = new Random(1753);
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(9);
            int[][] jobs = new int[n][2];
            for (int i = 0; i < n; i++) { jobs[i][0] = 1 + rnd.nextInt(6) * 3; jobs[i][1] = 1 + rnd.nextInt(4); }
            if (!Arrays.equals(starts(jobs, true), slow(jobs))) throw new AssertionError("start times differ on " + Arrays.deepToString(jobs));
        }
    }
}
```

#### Solution: [Recognize] Process Tasks Using Servers (LeetCode 1882)
<!-- id: hp-process-tasks-servers -->

**Approach.** Keep every server in exactly one of two heaps. The free heap is ordered by weight and then index, and the busy heap is ordered by finish time, then weight, then index. For task `j`, set the time to the larger of the current time and `j`, and move every busy server whose finish time is at most that time back to the free heap. If the free heap is still empty, set the time to the earliest finish time and release again. Poll the best free server, record its index, and push it to the busy heap with finish time `time + tasks[j]`. Both examples are asserted, and a second-by-second simulation with a plain arrival queue is the oracle on random small inputs, including inputs where several servers finish at the same second.

**Complexity.** Each task moves at most one server out of the free heap and each server move back costs one busy poll, so the time is O((m + n) log n) for n servers and m tasks, with O(n) memory.

```java run
import java.util.ArrayDeque;
import java.util.Arrays;
import java.util.PriorityQueue;
import java.util.Random;

public final class ProcessTasksServers {
    static int[] assign(int[] servers, int[] tasks) {
        PriorityQueue<int[]> free = new PriorityQueue<>(
            (x, y) -> x[0] != y[0] ? Integer.compare(x[0], y[0]) : Integer.compare(x[1], y[1]));
        PriorityQueue<long[]> busy = new PriorityQueue<>((x, y) -> {
            if (x[0] != y[0]) return Long.compare(x[0], y[0]);
            if (x[1] != y[1]) return Long.compare(x[1], y[1]);
            return Long.compare(x[2], y[2]);
        });
        for (int s = 0; s < servers.length; s++) free.offer(new int[]{servers[s], s});
        int[] out = new int[tasks.length];
        long time = 0;
        for (int j = 0; j < tasks.length; j++) {
            time = Math.max(time, j);
            while (!busy.isEmpty() && busy.peek()[0] <= time) {
                long[] b = busy.poll();
                free.offer(new int[]{(int) b[1], (int) b[2]});
            }
            if (free.isEmpty()) {
                time = busy.peek()[0];
                while (!busy.isEmpty() && busy.peek()[0] <= time) {
                    long[] b = busy.poll();
                    free.offer(new int[]{(int) b[1], (int) b[2]});
                }
            }
            int[] s = free.poll();
            out[j] = s[1];
            busy.offer(new long[]{time + tasks[j], s[0], s[1]});
        }
        return out;
    }

    static int[] bySeconds(int[] servers, int[] tasks) {
        long[] busyUntil = new long[servers.length];
        ArrayDeque<Integer> waiting = new ArrayDeque<>();
        int[] out = new int[tasks.length];
        int assigned = 0;
        for (long t = 0; assigned < tasks.length; t++) {
            if (t < tasks.length) waiting.add((int) t);
            while (!waiting.isEmpty()) {
                int best = -1;
                for (int s = 0; s < servers.length; s++) {
                    if (busyUntil[s] > t) continue;
                    if (best < 0 || servers[s] < servers[best]) best = s;
                }
                if (best < 0) break;
                int j = waiting.poll();
                out[j] = best;
                busyUntil[best] = t + tasks[j];
                assigned++;
            }
        }
        return out;
    }

    public static void main(String[] args) {
        if (!Arrays.equals(assign(new int[]{5, 1, 1, 4}, new int[]{3, 1, 2, 2, 1, 4, 1}), new int[]{1, 2, 2, 1, 2, 1, 2})) throw new AssertionError("example 1");
        if (!Arrays.equals(assign(new int[]{2}, new int[]{1, 1}), new int[]{0, 0})) throw new AssertionError("example 2");
        Random rnd = new Random(1754);
        for (int t = 0; t < 5000; t++) {
            int[] servers = new int[1 + rnd.nextInt(5)];
            int[] tasks = new int[1 + rnd.nextInt(9)];
            for (int i = 0; i < servers.length; i++) servers[i] = 1 + rnd.nextInt(4);
            for (int i = 0; i < tasks.length; i++) tasks[i] = 1 + rnd.nextInt(5);
            if (!Arrays.equals(assign(servers, tasks), bySeconds(servers, tasks))) throw new AssertionError("assignment differs for " + Arrays.toString(servers) + " " + Arrays.toString(tasks));
        }
    }
}
```
