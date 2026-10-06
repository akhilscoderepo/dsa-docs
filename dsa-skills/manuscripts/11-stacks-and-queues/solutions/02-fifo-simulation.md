<!-- solutions-for: 11-stacks-and-queues -->
### Solutions For FIFO Simulation

#### Solution: [Build] Printer Queue (Author exercise)
<!-- id: sq-printer-queue -->

**Approach.**
The method keeps a clock `t` and a queue of arrived jobs. When the queue is empty and jobs remain, the clock jumps to the next arrival, because the printer is idle. Every job with `arrival <= t` then enters the queue in index order. The method removes the front job, advances the clock by its duration and records the finish time. The invariant is that the queue holds exactly the jobs that arrived by `t` and have not started, in arrival order.

**Complexity.**
- **Time** is O(n), because each job is added once and removed once.
- **Space** is O(n), because the queue can hold every job and the output has n entries.

```java run
import java.util.ArrayDeque;
import java.util.Arrays;
import java.util.Random;

public final class PrinterQueue {
    /**
     * Returns the finish time of each job on a single printer.
     * Time: O(n), each job is enqueued and dequeued once.
     * Space: O(n) for the queue and the output.
     * Invariant: the queue holds jobs that arrived by t and have not started, in arrival order.
     */
    static long[] finishTimes(int[] arrival, int[] duration) {
        int n = arrival.length;
        long[] finish = new long[n];
        ArrayDeque<Integer> queue = new ArrayDeque<>();
        long t = 0;
        int next = 0;
        // Continue while a job waits or a job has not yet arrived.
        while (next < n || !queue.isEmpty()) {
            // An idle printer jumps the clock to the next arrival.
            if (queue.isEmpty()) t = Math.max(t, arrival[next]);
            // Every job that has arrived by t joins behind the waiting jobs.
            while (next < n && arrival[next] <= t) queue.addLast(next++);
            // The queue is non-empty here, so the removal is safe.
            int job = queue.removeFirst();
            t += duration[job];
            finish[job] = t;
        }
        return finish;
    }

    /** Reference: the closed-form recurrence finish[i] = max(finish[i-1], arrival[i]) + duration[i]. */
    static long[] oracle(int[] arrival, int[] duration) {
        long[] f = new long[arrival.length];
        for (int i = 0; i < f.length; i++) f[i] = Math.max(i == 0 ? 0 : f[i - 1], arrival[i]) + duration[i];
        return f;
    }

    public static void main(String[] args) {
        // Example 1: the third job arrives after the printer is idle.
        if (!Arrays.equals(finishTimes(new int[] {0, 1, 10}, new int[] {3, 2, 1}), new long[] {3, 5, 11})) throw new AssertionError("example 1");
        // Example 2: three jobs arrive together and print in index order.
        if (!Arrays.equals(finishTimes(new int[] {0, 0, 0}, new int[] {2, 2, 2}), new long[] {2, 4, 6})) throw new AssertionError("example 2");
        // Empty input.
        if (finishTimes(new int[0], new int[0]).length != 0) throw new AssertionError("empty");
        // Random inputs agree with the recurrence.
        Random rnd = new Random(1111);
        for (int t = 0; t < 3000; t++) {
            int n = rnd.nextInt(10);
            int[] a = new int[n], d = new int[n];
            int at = 0;
            for (int i = 0; i < n; i++) { at += rnd.nextInt(5); a[i] = at; d[i] = 1 + rnd.nextInt(4); }
            if (!Arrays.equals(finishTimes(a, d), oracle(a, d))) throw new AssertionError("random");
        }
        // Large arrival times need long arithmetic because the sum can pass the int range.
        long big = finishTimes(new int[] {1_000_000_000, 1_000_000_000}, new int[] {10_000, 10_000})[1];
        if (big != 1_000_020_000L) throw new AssertionError("large");
    }
}
```

#### Solution: [Vary] Round-Robin Finish Order (Author exercise)
<!-- id: sq-round-robin-step -->

**Approach.**
The queue starts with every task id in index order. Each turn removes the front id, decrements its work and puts the id at the back only when work remains. A task that reaches zero is appended to the finish list. The invariant is that the queue holds exactly the unfinished tasks, in the order of their next turn. Total work is a decreasing measure, because every turn removes one unit, so the loop terminates.

**Complexity.**
- **Time** is O(n + W), because each unit of work is one turn at amortized O(1) and W is the sum of work.
- **Space** is O(n), because the queue and the output each hold at most n ids.

```java run
import java.util.ArrayDeque;
import java.util.Arrays;
import java.util.Random;

public final class RoundRobinStep {
    /**
     * Returns the task ids in the order in which tasks finish.
     * Time: O(n + W), one turn per unit of work.
     * Space: O(n) for the queue and the output.
     * Invariant: the queue holds the unfinished tasks in order of their next turn.
     */
    static int[] finishOrder(int[] remaining) {
        int[] work = remaining.clone();
        ArrayDeque<Integer> queue = new ArrayDeque<>();
        // All tasks start waiting in index order.
        for (int i = 0; i < work.length; i++) queue.addLast(i);
        int[] order = new int[work.length];
        int done = 0;
        // Each pass of the loop is one turn, and the loop test proves the removal is safe.
        while (!queue.isEmpty()) {
            int task = queue.removeFirst();
            // The turn removes one unit of work.
            work[task]--;
            // An unfinished task waits behind every other waiting task.
            if (work[task] > 0) queue.addLast(task);
            else order[done++] = task;
        }
        return order;
    }

    /** Reference: repeated full passes over the array, skipping finished tasks. */
    static int[] oracle(int[] remaining) {
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

    public static void main(String[] args) {
        // Examples 1 and 2 from the exercise.
        if (!Arrays.equals(finishOrder(new int[] {2, 1, 3}), new int[] {1, 0, 2})) throw new AssertionError("example 1");
        if (!Arrays.equals(finishOrder(new int[] {3, 3, 1}), new int[] {2, 0, 1})) throw new AssertionError("example 2");
        // Random inputs agree with the repeated-pass reference, and the input is unchanged.
        Random rnd = new Random(1112);
        for (int t = 0; t < 3000; t++) {
            int[] w = new int[rnd.nextInt(8)];
            for (int i = 0; i < w.length; i++) w[i] = 1 + rnd.nextInt(5);
            int[] copy = w.clone();
            if (!Arrays.equals(finishOrder(w), oracle(w)) || !Arrays.equals(w, copy)) throw new AssertionError("random");
        }
        // A stack serves the newest item first, so it reverses arrival order.
        java.util.ArrayDeque<Integer> stack = new java.util.ArrayDeque<>();
        stack.addLast(1); stack.addLast(2); stack.addLast(3);
        if (stack.removeLast() != 3) throw new AssertionError("stack reverses");
        // Boxed values outside the cache differ by reference but are equal by value.
        Integer a = Integer.valueOf(1000), b = Integer.valueOf(1000);
        if (a == b || !a.equals(b)) throw new AssertionError("boxed comparison");
        // Adding while iterating the same deque throws.
        boolean threw = false;
        ArrayDeque<Integer> dq = new ArrayDeque<>(java.util.List.of(1, 2));
        try { for (int x : dq) dq.addLast(x); } catch (java.util.ConcurrentModificationException e) { threw = true; }
        if (!threw) throw new AssertionError("ConcurrentModificationException expected");
    }
}
```

#### Solution: [Boundary] Queue Becomes Empty (Author exercise)
<!-- id: sq-queue-becomes-empty -->

**Approach.**
Only tasks with positive work enter the queue, so a task that starts complete keeps finish time 0 and never needs a removal. Each turn runs the front task for `min(q, work)` units and advances the clock by that amount. A task with work left goes to the back, and a finished task records the clock value. The loop condition `!queue.isEmpty()` proves every removal safe, including the case of an empty input. The invariant is that every queued task has positive work.

**Complexity.**
- **Time** is O(n + W/q), because each turn uses `q` units except the last turn of a task, and there are at most n of those.
- **Space** is O(n), because the queue and the output each hold at most n entries.

```java run
import java.util.ArrayDeque;
import java.util.Arrays;
import java.util.Random;

public final class QueueBecomesEmpty {
    /**
     * Returns the clock value at which each task completes.
     * Time: O(n + W/q) turns, each at amortized O(1).
     * Space: O(n) for the queue and the output.
     * Invariant: every task in the queue has positive remaining work.
     */
    static int[] completion(int[] workIn, int q) {
        int[] work = workIn.clone();
        int[] finish = new int[work.length];
        ArrayDeque<Integer> queue = new ArrayDeque<>();
        // A task with zero work is already complete and never enters the queue.
        for (int i = 0; i < work.length; i++) if (work[i] > 0) queue.addLast(i);
        int clock = 0;
        // The loop test guarantees the queue is non-empty before each removal.
        while (!queue.isEmpty()) {
            int task = queue.removeFirst();
            // A turn uses the quantum or what is left, whichever is smaller.
            int used = Math.min(q, work[task]);
            clock += used;
            work[task] -= used;
            // Unfinished tasks wait behind the others; finished tasks record the clock.
            if (work[task] > 0) queue.addLast(task);
            else finish[task] = clock;
        }
        return finish;
    }

    /** Reference: full passes over the array with the same clock rule. */
    static int[] oracle(int[] workIn, int q) {
        int n = workIn.length;
        int[] work = workIn.clone();
        int[] finish = new int[n];
        int clock = 0;
        boolean any = true;
        while (any) {
            any = false;
            for (int i = 0; i < n; i++) {
                if (work[i] == 0) continue;
                int used = Math.min(q, work[i]);
                clock += used;
                work[i] -= used;
                if (work[i] == 0) finish[i] = clock; else any = true;
            }
        }
        return finish;
    }

    public static void main(String[] args) {
        // Example 1: the zero-work task keeps time 0.
        if (!Arrays.equals(completion(new int[] {3, 0, 2}, 2), new int[] {5, 0, 4})) throw new AssertionError("example 1");
        // Example 2: every task finishes on its first turn.
        if (!Arrays.equals(completion(new int[] {1, 1, 1}, 5), new int[] {1, 2, 3})) throw new AssertionError("example 2");
        // Empty input removes nothing.
        if (completion(new int[0], 3).length != 0) throw new AssertionError("empty");
        // Random inputs agree with the repeated-pass reference.
        Random rnd = new Random(1113);
        for (int t = 0; t < 3000; t++) {
            int[] w = new int[rnd.nextInt(8)];
            for (int i = 0; i < w.length; i++) w[i] = rnd.nextInt(7);
            int q = 1 + rnd.nextInt(4);
            if (!Arrays.equals(completion(w, q), oracle(w, q))) throw new AssertionError("random " + Arrays.toString(w) + q);
        }
        // Removing from an empty deque throws, which the loop test prevents.
        boolean threw = false;
        try { new ArrayDeque<Integer>().removeFirst(); } catch (java.util.NoSuchElementException e) { threw = true; }
        if (!threw) throw new AssertionError("removeFirst on empty throws");
    }
}
```

#### Solution: [Recognize] Students Unable To Eat Lunch (LeetCode 1700)
<!-- id: sq-students-lunch -->

**Approach.**
The method queues the students and tracks the index `sandwichAt` of the top sandwich. The front student takes the sandwich when the preferences match, which advances `sandwichAt` and resets `misses`. Otherwise the student goes to the back and `misses` grows. When `misses` equals the queue size, every remaining student has been tested against the same top sandwich and none wants it, so no later turn can succeed. The method returns the queue size. The invariant is that `misses` counts consecutive misses since the last success.

**Complexity.**
- **Time** is O(n^2) in the worst case, because each of at most n successes can follow up to n misses.
- **Space** is O(n), because the queue holds the students.

```java run
import java.util.ArrayDeque;
import java.util.Random;

public final class StudentsLunch {
    /**
     * Returns the number of students who never get a sandwich.
     * Time: O(n^2) worst case, up to n misses per success.
     * Space: O(n) for the queue.
     * Invariant: misses is the number of consecutive misses since the last success.
     */
    static int unableToEat(int[] students, int[] sandwiches) {
        ArrayDeque<Integer> queue = new ArrayDeque<>();
        for (int s : students) queue.addLast(s);
        int sandwichAt = 0, misses = 0;
        // Stop on an empty queue or after as many consecutive misses as the queue length.
        while (!queue.isEmpty() && misses < queue.size()) {
            int s = queue.removeFirst();
            if (s == sandwiches[sandwichAt]) {
                // A match takes the sandwich and resets the stall counter.
                sandwichAt++;
                misses = 0;
            } else {
                // A mismatch sends the student to the back and counts one failed turn.
                queue.addLast(s);
                misses++;
            }
        }
        return queue.size();
    }

    /** Reference: count preferences, then serve sandwiches until one has no taker. */
    static int oracle(int[] students, int[] sandwiches) {
        int[] count = new int[2];
        for (int s : students) count[s]++;
        int served = 0;
        for (int sw : sandwiches) {
            if (count[sw] == 0) break;
            count[sw]--;
            served++;
        }
        return students.length - served;
    }

    public static void main(String[] args) {
        // Example 1: three students want 1 while the top sandwich is 0.
        if (unableToEat(new int[] {1, 1, 1, 0}, new int[] {0, 0, 1, 1}) != 3) throw new AssertionError("example 1");
        // Example 2: one student remains at the end.
        if (unableToEat(new int[] {0, 1, 0, 1, 1}, new int[] {1, 0, 0, 1, 0}) != 1) throw new AssertionError("example 2");
        // The trace case from the lesson.
        if (unableToEat(new int[] {1, 0, 0, 1, 1}, new int[] {0, 0, 1, 0, 1}) != 2) throw new AssertionError("trace case");
        // Random inputs agree with the counting reference.
        Random rnd = new Random(1114);
        for (int t = 0; t < 5000; t++) {
            int n = 1 + rnd.nextInt(9);
            int[] st = new int[n], sw = new int[n];
            for (int i = 0; i < n; i++) { st[i] = rnd.nextInt(2); sw[i] = rnd.nextInt(2); }
            if (unableToEat(st, sw) != oracle(st, sw)) throw new AssertionError("random");
        }
    }
}
```
