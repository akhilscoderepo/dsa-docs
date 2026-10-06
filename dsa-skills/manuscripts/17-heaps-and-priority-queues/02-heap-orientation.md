<!-- lesson-kind: standard -->
<!-- lesson-id: heap-orientation -->
## Choose The Order With A Comparator

<!-- stage: context -->
### Why The Wrong Job Runs First

A job scheduler stores each job's priority as an `int` and runs the highest priority first. The team's queue returns the smallest value first, so a developer stores the negative of each priority. The scheduler passes every test with priorities from 1 to 100.

In production, a job with priority `Integer.MIN_VALUE`, which is meant to run last, runs first. At the same time, jobs with equal priority run in a different order whenever they arrive in a different order, and support cannot reproduce the complaints. This lesson asks how a program states exactly which item leaves the queue first, including ties and extreme values.

<!-- stage: naive -->
### Storing The Negative Of Each Priority

The direct plan keeps one `PriorityQueue<Integer>` and stores `-p` for each priority `p`. The smallest stored value is then the largest priority.

```java
static List<Integer> runOrder(int[] priorities) {
    PriorityQueue<Integer> queue = new PriorityQueue<>();
    for (int p : priorities) queue.offer(-p);          // the smallest stored value is the largest priority
    List<Integer> order = new ArrayList<>();
    while (!queue.isEmpty()) order.add(-queue.poll()); // undo the negation on the way out
    return order;
}
```

The method works for every priority from -1,000,000 to 1,000,000. Two jobs with equal priority are indistinguishable here, because the queue stores only the number and not which job it belongs to.

<!-- stage: bottleneck -->
### Finding Where Negation Breaks

```predict
In Java, what does -Integer.MIN_VALUE evaluate to, and where does a job with that priority leave the queue?

The expression evaluates to Integer.MIN_VALUE, because +2^31 does not fit in an int. The stored value is the smallest int, so the job leaves first although its priority is the smallest.
```

The `int` range is asymmetric. The value `Integer.MIN_VALUE` is -2,147,483,648, and `Integer.MAX_VALUE` is 2,147,483,647. Negating the minimum wraps around to itself. Any trick that does arithmetic on priorities, such as `a - b`, wraps in the same way when the difference exceeds 2^31 - 1.

Ties cause the second failure. Equal priorities have no required order in a heap, so the leaving order depends on array layout. Repairing this by polling every equal item and re-sorting the group costs O(g log g) per poll for a group of size g. The repair also needs each item to carry more than a number. The program needs a rule that compares whole items and never does arithmetic on the keys.

<!-- stage: insight -->
### Letting A Comparator Define The Order

A **comparator** is an object with one method, `compare(a, b)`. It returns a negative number when `a` must leave the queue before `b`. It returns zero for a tie and a positive number when `b` must leave first. A `PriorityQueue` built with a comparator places the item that is smallest under that rule at the root. Heap order from the previous lesson then holds under the comparator and not under the natural order.

#### Reversing The Direction

A max-first queue needs the reverse rule. `Comparator.reverseOrder()` provides it for natural orders, and `Collections.reverseOrder()` from the previous lesson is the same rule. For a custom rule, the program swaps the two arguments, as in `(a, b) -> Integer.compare(b, a)`. No stored value changes, so no value can overflow.

#### Comparing Without Arithmetic

`Integer.compare(a, b)` returns -1, 0 or 1 by comparing the two values directly. It never subtracts them, so it gives the right answer for every pair of `int` values. The subtraction `a - b` is wrong whenever the true difference lies outside the `int` range, for example `Integer.MAX_VALUE - (-1)`.

#### Ordering By A Tuple With A Tie-Break

A priority often has several fields, such as a duration and an original index. The comparator compares the first field, and only a tie moves it to the next field. The second field is the **tie-break**. A tie-break on a unique field, such as the index, makes the order total, so two runs on the same input give the same output. `Comparator.comparingInt(Task::duration).thenComparingInt(Task::index)` builds this rule.

<!-- names: comparator, tie-break, Integer.compare -->

<!-- stage: variables -->
### The Fields Of One Ordering Rule

An ordering rule has four parts, and each one is a decision the code makes explicit.

- **Key field** is the value the first comparison reads, such as the duration of a task.
- **Direction** says whether a smaller or a larger key leaves first.
- **Tie-break field** is the next field read when two key fields are equal, such as the original index.
- **Comparator result** is the sign of the answer, negative, zero or positive, and never its size.

The queue calls the comparator only to decide which of two items sits higher in the array.

<!-- stage: trace -->
### Tracing Ties And Overflow

#### Polling Tasks With Equal Durations

Take four tasks with durations 3, 1, 3 and 1 at indexes 0 to 3. The rule orders by duration and breaks ties by the smaller index. In the first trace the pointer `pick` marks the task that `poll` returns.

The two tasks with duration 1 leave first. Their durations are tied, so the tie-break compares indexes 1 and 3, and index 1 leaves first. The tasks with duration 3 follow the same way, with index 0 before index 2. The leaving order is therefore 1, 3, 0, 2 on every run.

#### Comparing Two Extreme Values

The second trace compares `a = Integer.MAX_VALUE` with `b = -1`. The pointers `a` and `b` mark the two values. The true difference is 2,147,483,648, which exceeds the largest `int`, so `a - b` wraps to -2,147,483,648. The subtraction rule reads that negative sign as "a is smaller" and puts `a` first in a smallest-first queue, which is wrong. `Integer.compare(a, b)` returns 1, so `b` leaves first.

#### Stepping Through Both Runs

```trace
{"cells":[3,1,3,1],"pointers":["pick"],"steps":[{"at":{"pick":-1},"vars":{"left":"[0, 1, 2, 3]","order":"[]"},"note":"Four tasks wait. The rule is the smaller duration first and, for a tie, the smaller index."},{"at":{"pick":1},"vars":{"left":"[0, 2, 3]","order":"[1]"},"note":"The task 1 with duration 1 leaves. Task 3 has the same duration, and the tie-break picks the smaller index 1."},{"at":{"pick":3},"vars":{"left":"[0, 2]","order":"[1, 3]"},"note":"The task 3 with duration 1 leaves."},{"at":{"pick":0},"vars":{"left":"[2]","order":"[1, 3, 0]"},"note":"The task 0 with duration 3 leaves. Task 2 has the same duration, and the tie-break picks the smaller index 0."},{"at":{"pick":2},"vars":{"left":"[]","order":"[1, 3, 0, 2]"},"note":"The task 2 with duration 3 leaves."}]}
```

```trace
{"cells":[2147483647,-1],"pointers":["a","b"],"steps":[{"at":{"a":0,"b":1},"vars":{"a":2147483647,"b":-1,"true a - b":2147483648},"note":"The values are Integer.MAX_VALUE and -1. The true difference is 2147483648, which is larger than the largest int."},{"at":{"a":0,"b":1},"vars":{"a - b in int":-2147483648,"sign":"negative"},"note":"The subtraction wraps to -2147483648. A negative sign says that a leaves first in a smallest-first queue."},{"at":{"a":0,"b":1},"vars":{"Integer.compare":1,"leaves first":"b"},"note":"Integer.compare reads the two values directly and returns 1, so b leaves first, which is the correct answer."}]}
```

<!-- stage: code -->
### Building Queues With Comparators

#### Three Queues With Three Rules

The wrapper class holds a small `record` for the task, and each factory method returns a queue with one rule.

```java
final class Orders {
    record Task(int duration, int index) {}

    static PriorityQueue<Task> shortestFirst() {
        return new PriorityQueue<>(
            Comparator.comparingInt(Task::duration)   // first field decides
                      .thenComparingInt(Task::index)); // equal durations fall back to the index
    }

    static PriorityQueue<Integer> largestFirst() {
        return new PriorityQueue<>(Comparator.reverseOrder());
    }

    static PriorityQueue<Integer> largestFirstByHand() {
        return new PriorityQueue<>((a, b) -> Integer.compare(b, a)); // arguments swapped, no subtraction
    }
}
```

#### Costs Of The Comparator

Every `offer` and `poll` calls the comparator O(log n) times. A comparator that runs in constant time keeps both operations at O(log n). A comparator that sorts or scans inside `compare` multiplies that cost.

<!-- stage: applicability -->
### Checking The Order Before Using It

#### Stating The Tuple First

Write the exact tuple of fields that decides the order before writing any code. The invariant of the lesson is that the comparator orders that exact tuple, so the root is always the item the algorithm wants next. A missing tie-break shows up only when two items share the first field, so the tuple must list the tie-break.

#### Finding The False Friend

The false friend is a negation or subtraction trick. It looks like a cheap way to reverse or combine orders, and it passes every test without extreme values. It fails at `Integer.MIN_VALUE` and for any difference larger than the `int` range.

A second false friend is a mutable key. If code changes a field that the comparator reads after the item is in the queue, the queue does not move the item. The root may then no longer be the smallest item.

#### Recognizing The No-Go Cases

The comparator must give the same answer for the same pair every time and must stay consistent when two comparisons chain together. A comparator that depends on the clock or on random numbers breaks heap order. If the algorithm needs two different orders at once, it needs two queues.

<!-- stage: exercises -->
### Exercises

#### [Build] Safe Max-Heap (Author exercise)
<!-- id: hp-safe-max-heap -->

**Prerequisites.** The reverse comparator and `Integer.compare` from this lesson.

**Problem.** Given an array `values` of integers, return a new array with the same values in nonincreasing order. Use one `PriorityQueue<Integer>` whose comparator reverses the natural order. The comparator must not subtract or negate any value.

**Constraints.** The limits are:
- **Length** is `0 <= values.length <= 10^5`.
- **Values** are any `int` values, including `Integer.MIN_VALUE` and `Integer.MAX_VALUE`.
- **Mutation** does not occur; `values` keeps its order.

**Example 1.** Input `values = [4,-9,4,0]`, output `[4,4,0,-9]`.

**Example 2.** Input `values = [-2147483648, 2147483647, 0]`, output `[2147483647, 0, -2147483648]`.

**Hint.** Which two arguments does `Integer.compare` need so that the larger value counts as smaller? Which stored value breaks if the code negates it?

**Changed decision.** The direction changes by swapping arguments, and no stored value changes.

#### [Vary] Pair Priority (Author exercise)
<!-- id: hp-pair-priority -->

**Prerequisites.** The previous exercise and the tuple comparator in the code stage.

**Problem.** Given an array `durations`, task `i` has duration `durations[i]`. Return the task indexes in the order a queue removes them when the rule is the smaller duration first and, for equal durations, the smaller index first.

**Constraints.** The limits are:
- **Length** is `0 <= durations.length <= 10^5`.
- **Durations** are `int` values from `1` to `10^9`.
- **Answer** is a permutation of `0` to `n - 1`.
- **Mutation** does not occur; `durations` keeps its order.

**Example 1.** Input `durations = [3,1,3,1]`, output `[1,3,0,2]`.

**Example 2.** Input `durations = [5,5,5]`, output `[0,1,2]`.

**Hint.** What does the queue store for each task? Which field breaks a tie, and why does it never tie itself?

**Changed decision.** The queue stores a pair, and a second field breaks ties.

#### [Boundary] Equal Priorities And Extreme Integers (Author exercise)
<!-- id: hp-equal-extreme -->

**Prerequisites.** The two exercises above.

**Problem.** Given an array `priorities`, job `i` has priority `priorities[i]`. Return the job indexes in the order a queue removes them when the larger priority leaves first and, for equal priorities, the smaller index leaves first. Every `int` value is a legal priority.

**Constraints.** The limits are:
- **Length** is `0 <= priorities.length <= 10^5`.
- **Priorities** are any `int` values, including `Integer.MIN_VALUE` and `Integer.MAX_VALUE`.
- **Ties** always resolve by the smaller index.
- **Mutation** does not occur; `priorities` keeps its order.

**Example 1.** Input `priorities = [-2147483648, 2147483647, -2147483648, 0]`, output `[1,3,0,2]`.

**Example 2.** Input `priorities = [7,7,7]`, output `[0,1,2]`.

**Hint.** Which comparison overflows when one priority is `Integer.MAX_VALUE` and the other is negative? Does the tie-break also need to avoid subtraction?

**Changed decision.** Comparison uses `Integer.compare` on both fields, so no difference can overflow.

#### [Recognize] Single-Threaded CPU (LeetCode 1834)
<!-- id: hp-single-threaded-cpu -->

**Prerequisites.** All three exercises above.

**Problem.** Given an array `processing`, task `i` needs `processing[i]` time units. All tasks are available at time 0, and one processor runs one task at a time without interruption. When the processor is free, it starts the available task with the smallest processing time, and a tie goes to the smaller index. Return the indexes in execution order.

**Constraints.** The limits are:
- **Length** is `0 <= processing.length <= 10^5`.
- **Processing times** are `int` values from `1` to `10^9`.
- **Answer** is a permutation of `0` to `n - 1`.
- **Mutation** does not occur; `processing` keeps its order.

**Example 1.** Input `processing = [4,2,4,1]`, output `[3,1,0,2]`.

**Example 2.** Input `processing = [6]`, output `[0]`.

**Hint.** Which pair of fields decides the next task? Does the order of the output depend on the running clock when every task is released at time 0?

**Changed decision.** The same tuple rule applies, and the release times are all zero in this version.
