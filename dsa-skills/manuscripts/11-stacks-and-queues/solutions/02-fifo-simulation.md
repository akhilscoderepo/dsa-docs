<!-- solutions-for: 02-fifo-simulation -->
### FIFO Simulation

#### Solution: [Build] Printer Queue (Author exercise)
<!-- id: sq-printer-queue -->

**Approach.** Put the job indices in a queue in arrival order. Keep a clock for the minute at which the printer becomes free. Remove the front job, start it at the later of the clock and its arrival minute, and add its page count to get the finishing minute, which becomes the new clock. No job can be served out of order because the queue only ever gives the oldest waiting job. The assertions compare against a minute-by-minute simulation that uses its own waiting list, on random small inputs.

**Complexity.** O(n) time and O(n) space.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

public final class PrinterQueue {
    static long[] finish(int[] arrival, int[] pages) {
        ArrayDeque<Integer> line = new ArrayDeque<>();
        for (int i = 0; i < arrival.length; i++) line.addLast(i);
        long[] done = new long[arrival.length];
        long clock = 0;
        while (!line.isEmpty()) {
            int job = line.removeFirst();
            clock = Math.max(clock, arrival[job]) + pages[job];
            done[job] = clock;
        }
        return done;
    }
    static long[] oracle(int[] arrival, int[] pages) {
        int n = arrival.length;
        long[] done = new long[n];
        List<Integer> waiting = new ArrayList<>();
        int next = 0, current = -1, left = 0;
        for (int minute = 0; next < n || !waiting.isEmpty() || current >= 0; minute++) {
            while (next < n && arrival[next] == minute) waiting.add(next++);
            if (current < 0 && !waiting.isEmpty()) { current = waiting.remove(0); left = pages[current]; }
            if (current >= 0) {
                left--;
                if (left == 0) { done[current] = minute + 1; current = -1; }
            }
        }
        return done;
    }

    public static void main(String[] args) {
        if (!Arrays.equals(finish(new int[] {0, 1, 10}, new int[] {4, 2, 3}), new long[] {4, 6, 13})) throw new AssertionError("example 1");
        if (!Arrays.equals(finish(new int[] {5, 5}, new int[] {1, 1}), new long[] {6, 7})) throw new AssertionError("example 2");
        if (finish(new int[0], new int[0]).length != 0) throw new AssertionError("no jobs");
        Random rnd = new Random(11201);
        for (int t = 0; t < 3000; t++) {
            int n = rnd.nextInt(8);
            int[] arrival = new int[n], pages = new int[n];
            int at = 0;
            for (int i = 0; i < n; i++) { at += rnd.nextInt(5); arrival[i] = at; pages[i] = 1 + rnd.nextInt(6); }
            if (!Arrays.equals(finish(arrival, pages), oracle(arrival, pages))) throw new AssertionError("differs on " + Arrays.toString(arrival) + " " + Arrays.toString(pages));
        }
    }
}
```

#### Solution: [Vary] Round-Robin One Step (Author exercise)
<!-- id: sq-round-robin-one-step -->

**Approach.** Load the counts into a queue and run turns while turns remain and the line is nonempty. Each turn removes the front count, subtracts one, and re-enqueues the result only when it is still positive, so finished jobs leave. After the turns, copy the queue from front to back. The number of turns can be a billion, but the loop stops as soon as the line is empty, and each turn is constant time, so the loop is bounded by the total work. The assertions compare with a simulation on a plain list that removes at index zero, and check the example where the line empties before the turns are used.

**Complexity.** O(min(t, P)) time for total work P, and O(n) space.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

public final class RoundRobinOneStep {
    static int[] run(int[] left, int turns) {
        ArrayDeque<Integer> line = new ArrayDeque<>();
        for (int v : left) line.addLast(v);
        for (int t = 0; t < turns && !line.isEmpty(); t++) {
            int job = line.removeFirst() - 1;
            if (job > 0) line.addLast(job);
        }
        int[] out = new int[line.size()];
        int i = 0;
        for (int v : line) out[i++] = v;
        return out;
    }
    static int[] oracle(int[] left, int turns) {
        List<Integer> list = new ArrayList<>();
        for (int v : left) list.add(v);
        for (int t = 0; t < turns; t++) {
            if (list.isEmpty()) break;
            int v = list.remove(0) - 1;
            if (v > 0) list.add(v);
        }
        return list.stream().mapToInt(Integer::intValue).toArray();
    }

    public static void main(String[] args) {
        if (!Arrays.equals(run(new int[] {3, 1, 2}, 4), new int[] {1, 1})) throw new AssertionError("example 1");
        if (run(new int[] {1, 1}, 5).length != 0) throw new AssertionError("example 2");
        if (!Arrays.equals(run(new int[] {2, 2}, 0), new int[] {2, 2})) throw new AssertionError("zero turns change nothing");
        if (run(new int[] {1}, 1000000000).length != 0) throw new AssertionError("a huge turn count stops when the line is empty");
        Random rnd = new Random(11202);
        for (int t = 0; t < 4000; t++) {
            int n = rnd.nextInt(8);
            int[] left = new int[n];
            for (int i = 0; i < n; i++) left[i] = 1 + rnd.nextInt(5);
            int turns = rnd.nextInt(30);
            if (!Arrays.equals(run(left, turns), oracle(left, turns))) throw new AssertionError("differs on " + Arrays.toString(left) + " t=" + turns);
        }
    }
}
```

#### Solution: [Boundary] Queue Becomes Empty (Author exercise)
<!-- id: sq-queue-becomes-empty -->

**Approach.** Queue the indices. While the queue is nonempty, remove the front index, subtract up to `q` pages from its count (never going below zero), and record the index as finished if its count is now zero, otherwise append it. A job that starts at zero is recorded on its first turn because the subtraction is a no-op and the zero test follows it. Every removal is protected by the loop condition `!line.isEmpty()`. The assertions compare with a sweep model that gives every unfinished job up to `q` pages per round in index order, which has the same finish order as the queue, and show the empty input and the all-zero input.

**Complexity.** O(n + P / q) turns in time, each constant, so O(n + P / q) overall, and O(n) space.

```java run
import java.util.ArrayDeque;
import java.util.Arrays;
import java.util.Random;

public final class QueueBecomesEmpty {
    static int[] finishOrder(int[] pages, int q) {
        ArrayDeque<Integer> line = new ArrayDeque<>();
        int[] left = pages.clone();
        for (int i = 0; i < pages.length; i++) line.addLast(i);
        int[] order = new int[pages.length];
        int done = 0;
        while (!line.isEmpty()) {
            int job = line.removeFirst();
            left[job] -= Math.min(q, left[job]);
            if (left[job] == 0) order[done++] = job;
            else line.addLast(job);
        }
        return order;
    }
    static int[] sweeps(int[] pages, int q) {
        int n = pages.length, done = 0;
        int[] left = pages.clone(), order = new int[n];
        boolean[] finished = new boolean[n];
        while (done < n) {
            for (int i = 0; i < n; i++) {
                if (finished[i]) continue;
                left[i] -= Math.min(q, left[i]);
                if (left[i] == 0) { finished[i] = true; order[done++] = i; }
            }
        }
        return order;
    }

    public static void main(String[] args) {
        if (!Arrays.equals(finishOrder(new int[] {5, 0, 2}, 2), new int[] {1, 2, 0})) throw new AssertionError("example 1");
        if (finishOrder(new int[0], 3).length != 0) throw new AssertionError("example 2");
        if (!Arrays.equals(finishOrder(new int[] {0, 0, 0}, 1), new int[] {0, 1, 2})) throw new AssertionError("all zero jobs finish in line order");
        if (!Arrays.equals(finishOrder(new int[] {5, 2, 0}, 2), new int[] {1, 2, 0})) throw new AssertionError("a zero job finishes on its own turn, not before the others");
        Random rnd = new Random(11203);
        for (int t = 0; t < 4000; t++) {
            int n = rnd.nextInt(9);
            int[] pages = new int[n];
            for (int i = 0; i < n; i++) pages[i] = rnd.nextInt(8);
            int q = 1 + rnd.nextInt(4);
            if (!Arrays.equals(finishOrder(pages, q), sweeps(pages, q))) throw new AssertionError("differs on " + Arrays.toString(pages) + " q=" + q);
        }
    }
}
```

#### Solution: [Recognize] Number of Students Unable to Eat Lunch (LeetCode 1700)
<!-- id: sq-students-unable-lunch -->

**Approach.** Put the preferences in a queue and walk the sandwiches from the top. The front student either takes the top sandwich, which resets the rejection counter and offers the next sandwich, or goes to the back, which increments the counter. When the counter equals the queue size, a whole rotation produced no meal, and the same rotation would repeat forever, so the loop stops. The students left in the queue are the answer. The assertions compare with a counting method: count the preferences, walk the sandwiches, and stop at the first sandwich whose type nobody left wants.

**Complexity.** O(n^2) time in the worst case for the rotation, and O(n) space. The counting check runs in O(n).

```java run
import java.util.ArrayDeque;
import java.util.Random;

public final class StudentsUnableToEat {
    static int unable(int[] students, int[] sandwiches) {
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
    static int counting(int[] students, int[] sandwiches) {
        int[] want = new int[2];
        for (int s : students) want[s]++;
        int served = 0;
        for (int type : sandwiches) {
            if (want[type] == 0) break;
            want[type]--;
            served++;
        }
        return students.length - served;
    }

    public static void main(String[] args) {
        if (unable(new int[] {0, 1, 0, 1, 1}, new int[] {1, 0, 1, 0, 1}) != 0) throw new AssertionError("example 1");
        if (unable(new int[] {1, 1, 1, 1}, new int[] {0, 1, 1, 1}) != 4) throw new AssertionError("example 2");
        if (unable(new int[] {1, 1, 1, 0}, new int[] {0, 0, 1, 1}) != 3) throw new AssertionError("a stuck line with students still waiting");
        Random rnd = new Random(11204);
        for (int t = 0; t < 5000; t++) {
            int n = 1 + rnd.nextInt(10);
            int[] students = new int[n], sandwiches = new int[n];
            for (int i = 0; i < n; i++) { students[i] = rnd.nextInt(2); sandwiches[i] = rnd.nextInt(2); }
            if (unable(students, sandwiches) != counting(students, sandwiches)) throw new AssertionError("differs");
        }
    }
}
```
