<!-- lesson-kind: standard -->
<!-- lesson-id: heap-orientation -->
## Heap Orientation

<!-- stage: context -->
### The Pharmacy Counter Rules

A small pharmacy fills prescriptions from a ticket rail. The pharmacist keeps two habits. On quiet mornings she takes the prescription that needs the fewest minutes to prepare, and if two of them need the same time, she takes the one whose ticket was handed out first, so that nobody who waited longer is passed by a later arrival with the same workload. On stock days she does the opposite with the delivery crates, and opens the heaviest crate first, because the heavy ones block the shelves.

Both habits are easy to say and easy to get slightly wrong. A new assistant has been told to build the rail in software, and the first version, which a colleague sketched in a few lines, already produces the right order on the sample tickets. The pharmacist wants to be sure it keeps producing the right order when the numbers are large, negative, or equal.

<!-- stage: naive -->
### Flip The Sign And Subtract

The usual shortcut is to store negated numbers in the default queue to get the largest first, and to write a comparator that subtracts one field from the other.

```java
static int heaviestCrateByNegation(int[] weights) {
    java.util.PriorityQueue<Integer> queue = new java.util.PriorityQueue<>();
    for (int w : weights) queue.offer(-w);
    return -queue.poll();
}

static java.util.PriorityQueue<int[]> ticketRail() {
    return new java.util.PriorityQueue<>((a, b) -> a[0] - b[0]);
}
```

For the weights `[4, 9, 2]` the first method returns 9, and the ticket rail orders `{minutes, ticket}` pairs by minutes on every ordinary example.

<!-- stage: bottleneck -->
### Arithmetic On Priorities Breaks

The shortcuts add no running cost, since each queue operation is still O(log n), so the problem is correctness. Negation maps every integer to its opposite except the smallest one, because there is no positive counterpart of `Integer.MIN_VALUE` in 32 bits, and its negation is itself. A crate with that weight would look like the lightest crate, and would be opened first by the max-first rule. Subtraction fails in the same way: the difference of a large positive number and a negative one does not fit in an `int`, wraps around to a negative value, and tells the queue that the larger number is the smaller one.

The second failure is about ties. A comparator that subtracts the minutes returns zero for two equal workloads, and the queue is then free to hand out either ticket first. The pharmacist's rule is a rule about the pair, and a queue that sees only one field of it cannot follow it. Repairing the order afterwards, by sorting the tied groups, would cost another O(n log n) pass and would defeat the point of the queue.

<!-- stage: insight -->
### Say The Order In Full

Give the queue an **explicit comparator** that spells out the whole order, and let the comparator compare, never calculate. The comparator is the only definition of what comes first, so it has to be written down for every queue, even for the default direction.

The comparator should rank the exact **priority tuple** that the algorithm uses: the fields in the order of importance, ending in a field that is unique, such as the original index, so that no two items are equal and the order is total. For the pharmacy that tuple is minutes, then ticket number. In Java it is built with `Comparator.comparingInt(...)` for the first field and `thenComparingInt(...)` for each following one, and a reverse direction on a single field is written `Comparator.reverseOrder()` or `(a, b) -> Integer.compare(b, a)`. Reversing a whole chain with `.reversed()` flips every field, including the tie-break, so a mixed direction must be built from separate parts.

<!-- names: explicit comparator, priority tuple, overflow-safe compare -->

Every numeric comparison goes through an **overflow-safe compare**, that is, `Integer.compare`, `Long.compare`, or a key extractor like `comparingInt`, which return a sign without ever forming a difference. They are correct on the full range of the type and have the same cost as the subtraction. With these three decisions made in the open, the queue's behaviour on equal priorities is determined by the data and not by accident, and the heap mechanics of the previous lesson work unchanged.

<!-- stage: variables -->
### Key Fields, Direction And Tie-Break

Each queued item carries its key fields and, usually, the original index, since the index identifies the item and breaks ties. The tuple's order of fields is fixed when the queue is built and never changes. The direction is chosen per field: ascending is the natural direction, and descending is requested by swapping the arguments of the compare call. The tie-break field is read only when all earlier fields are equal, so it changes the order of equal items and nothing else. If the algorithm needs an item to wait, such as a task that is not yet released, that condition is not part of the comparator, and the item is kept outside the queue until it is eligible.

<!-- stage: trace -->
### Equal Minutes Leave By Ticket

The first run sets the pharmacy's rule on five tickets with preparation times `5, 2, 5, 1, 2`, numbered 0 to 4. All five are offered, and then they are polled one at a time under the tuple minutes then ticket. The lone 1 at ticket 3 leaves first. The two tickets that need 2 minutes follow, and ticket 1 goes before ticket 4 because its number is smaller. The 5-minute tickets leave last in the order 0 and 2. A queue that compared minutes only would be free to open ticket 4 before ticket 1, and the step to study is the second poll, where the tie-break decides.

The second run shows the extreme values on a max-first queue built with `Integer.compare`. The weights are `2147483647, -2147483648, 0, 7`, and the order that leaves is the largest weight first, then 7, then 0, and the smallest integer last. A queue built on negated values would have treated the smallest integer as the heaviest and opened it first.

```trace
{"cells":[5,2,5,1,2],"pointers":["picked"],"steps":[{"at":{"picked":3},"vars":{"left":"[(2,1),(2,4),(5,0),(5,2)]","order":"[3]"},"note":"Ticket 3 needs 1 minutes and leaves."},{"at":{"picked":1},"vars":{"left":"[(2,4),(5,0),(5,2)]","order":"[3,1]"},"note":"Ticket 1 needs 2 minutes and leaves. Another ticket needs 2 minutes as well, and the smaller ticket number decided."},{"at":{"picked":4},"vars":{"left":"[(5,0),(5,2)]","order":"[3,1,4]"},"note":"Ticket 4 needs 2 minutes and leaves."},{"at":{"picked":0},"vars":{"left":"[(5,2)]","order":"[3,1,4,0]"},"note":"Ticket 0 needs 5 minutes and leaves. Another ticket needs 5 minutes as well, and the smaller ticket number decided."},{"at":{"picked":2},"vars":{"left":"[]","order":"[3,1,4,0,2]"},"note":"Ticket 2 needs 5 minutes and leaves."}]}
```

```trace
{"cells":[2147483647,-2147483648,0,7],"pointers":["picked"],"steps":[{"at":{"picked":0},"vars":{"order":"[2147483647]","left":3},"note":"Weight 2147483647 is the largest that remains, so it leaves."},{"at":{"picked":3},"vars":{"order":"[2147483647,7]","left":2},"note":"Weight 7 is the largest that remains, so it leaves."},{"at":{"picked":2},"vars":{"order":"[2147483647,7,0]","left":1},"note":"Weight 0 is the largest that remains, so it leaves."},{"at":{"picked":1},"vars":{"order":"[2147483647,7,0,-2147483648]","left":0},"note":"Weight -2147483648 is the largest that remains, so it leaves. Under negation this weight would have looked like the lightest crate and left first."}]}
```

<!-- stage: code -->
### Comparators For Both Habits

```java
static int[] orderByMinutesThenTicket(int[] minutes) {
    java.util.PriorityQueue<int[]> rail = new java.util.PriorityQueue<>(
        java.util.Comparator.<int[]>comparingInt(t -> t[0]).thenComparingInt(t -> t[1]));
    for (int i = 0; i < minutes.length; i++) rail.offer(new int[]{minutes[i], i});
    int[] order = new int[minutes.length];
    for (int k = 0; k < order.length; k++) order[k] = rail.poll()[1];
    return order;
}

static java.util.PriorityQueue<Integer> heaviestFirst() {
    return new java.util.PriorityQueue<>(java.util.Comparator.reverseOrder());
}
```

The first method makes `n` offers and `n` polls of logarithmic cost, so it takes O(n log n) time, and the array pairs are plain objects, so the extra memory is linear. The explicit type witness `Comparator.<int[]>comparingInt` tells the compiler the element type, which is what lets `t[0]` compile inside the lambda. The second method returns a queue whose natural order is reversed by the comparator and works for every `int`, including the extremes.

<!-- stage: applicability -->
### When Ties And Extremes Matter

Use an explicit tuple comparator whenever the problem names more than one criterion, whenever it says how ties are resolved, or whenever the numbers can reach the limits of their type. The invariant is that the comparator ranks exactly the tuple the algorithm needs, with a unique last field, and that the queue's root is the first item in that order. State the tuple in words before writing the comparator, and test it on equal and extreme values.

The false friend is the pair of tricks in the naive method. Negation looks like a harmless max-heap, and subtraction looks like a harmless compare, and both are correct on every example that a person writes by hand. Another false friend is a comparator that returns only the first field of a tuple while the problem sorts by two, which gives results that depend on the insertion order and that pass the small samples by luck.

Do not put a changing key inside the comparator. A comparator that reads a field which is modified while the item is in the queue leaves the array in an order that the heap no longer matches, and the queue does not notice. If a key can change, remove the item and insert a new one, or use the stale-entry technique from a later lesson. In Java, prefer `Integer.compare` and `Long.compare` over subtraction, and wrap an `int` in `long` before any arithmetic on priorities.

<!-- stage: exercises -->
### Exercises

#### [Build] Safe Max-Heap (Author exercise)
<!-- id: hp-safe-max-heap -->

**Prerequisites.** The comparator rules of this lesson and the offer and poll moves of the previous one.

**Problem.** Given an integer array `values`, return its values in descending order by offering them to a `PriorityQueue` with a reverse comparator, with no negation and no subtraction of values.

**Constraints.** 0 <= values.length <= 10^5, and each value is any `int`, including `-2147483648` and `2147483647`.

**Example 1.** Input `values = [3, -7, 10, 3]`, output `[10, 3, 3, -7]`.

**Example 2.** Input `values = [-2147483648, 2147483647, 0]`, output `[2147483647, 0, -2147483648]`.

**Hint.** What does `-Integer.MIN_VALUE` evaluate to? Which library call compares two ints without forming a difference?

**Changed decision.** The direction is reversed on purpose, and the whole `int` range must be safe, so the comparator may only compare.

#### [Vary] Pair Priority (Author exercise)
<!-- id: hp-pair-priority -->

**Prerequisites.** Safe Max-Heap above.

**Problem.** Given an array `duration` of task durations, return the original indices of the tasks in the order they leave a queue that prefers the shorter duration and, for equal durations, the smaller index.

**Constraints.** 1 <= duration.length <= 10^5 and 1 <= duration[i] <= 10^9.

**Example 1.** Input `duration = [4, 1, 4, 1, 3]`, output `[1, 3, 4, 0, 2]`.

**Example 2.** Input `duration = [2, 2, 2]`, output `[0, 1, 2]`.

**Hint.** Which fields form the tuple, and in which order? Why must the index be stored in the queue next to the duration?

**Changed decision.** The queue ranks a pair and not a single number, and the second field decides every tie.

#### [Boundary] Equal Priorities And Extreme Integers (Author exercise)
<!-- id: hp-equal-priorities-extremes -->

**Prerequisites.** The two exercises above.

**Problem.** Given an array `priority` of arbitrary integers, return the indices in the order they leave a queue that prefers the larger priority and, for equal priorities, the smaller index.

**Constraints.** 1 <= priority.length <= 10^5, and each priority is any `int`.

**Example 1.** Input `priority = [5, 2147483647, 5, -2147483648, 2147483647]`, output `[1, 4, 0, 2, 3]`.

**Example 2.** Input `priority = [0, 0]`, output `[0, 1]`.

**Hint.** Which of the two fields is reversed and which is not? What goes wrong if the whole comparator chain is reversed at the end?

**Changed decision.** The two fields now run in opposite directions, and the extreme values forbid any arithmetic in the comparator.

#### [Recognize] Single-Threaded CPU (LeetCode 1834)
<!-- id: hp-single-threaded-cpu -->

**Prerequisites.** All three exercises above.

**Problem.** Task `i` is given as `tasks[i] = [enqueueTime, processingTime]` and becomes available at its enqueue time. One processor works without interruption. When it is idle and tasks are available it takes the one with the smallest processing time, and the smaller index among equals. If it is idle and no task is available, it waits for the next one. Return the indices of the tasks in the order they are processed.

**Constraints.** 1 <= tasks.length <= 10^5 and 1 <= enqueueTime, processingTime <= 10^9, so clock values need a `long`.

**Example 1.** Input `tasks = [[2, 3], [0, 6], [3, 1], [3, 1], [20, 2]]`, output `[1, 2, 3, 0, 4]`.

**Example 2.** Input `tasks = [[1, 2], [1, 2], [1, 2]]`, output `[0, 1, 2]`.

**Hint.** Which tasks may enter the queue at a given clock value, and in what order should they be examined? What should the clock do when the queue is empty?

**Changed decision.** The tuple comparator now sits inside a time loop, where only tasks that have already been released may be queued.
