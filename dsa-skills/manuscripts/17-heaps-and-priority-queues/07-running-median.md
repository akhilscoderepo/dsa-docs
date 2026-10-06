<!-- lesson-kind: standard -->
<!-- lesson-id: running-median -->
## Track The Median As Numbers Arrive

<!-- stage: context -->
### Why The Latency Chart Lags

A monitoring dashboard shows the median response time of all requests so far. A mean hides slow outliers, and the median does not. Every second the dashboard receives a few thousand new response times, and the chart must show the current median after each batch. The first version stores every value in a sorted list. After a few hours the list holds tens of millions of values, and each new value takes longer to place than the one before.

The dashboard needs one number, the middle value, after every arrival. This lesson asks how a program reads the middle value of a growing collection without keeping the whole collection in sorted order.

<!-- stage: naive -->
### Inserting Into A Sorted List

The direct plan keeps an `ArrayList<Integer>` in sorted order. Each arrival finds its place with binary search and inserts there. The median is a read at the middle index.

```java
static final class SortedMedian {
    private final List<Integer> sorted = new ArrayList<>();

    void add(int v) {
        int pos = Collections.binarySearch(sorted, v);   // finds a matching position or the insertion point
        if (pos < 0) pos = -pos - 1;                     // convert the insertion point encoding
        sorted.add(pos, v);                              // shifts every later value one place right
    }

    double median() {
        int n = sorted.size();
        if (n % 2 == 1) return sorted.get(n / 2);
        return ((long) sorted.get(n / 2 - 1) + sorted.get(n / 2)) / 2.0;
    }
}
```

The class gives the right median after every arrival. Reading the median is a constant-time step, and the insertion is the expensive step.

<!-- stage: bottleneck -->
### Counting The Shifts

```predict
The list holds n = 10,000,000 values and receives one more. About how many values move during the insertion in the average case?

The insertion lands at a random position, so about half the values, 5,000,000, shift one place right. One insertion costs O(n), and n insertions cost O(n^2).
```

The binary search is cheap, O(log n), and the shift is not. The list moves every value after the insertion point. A linked list avoids the shift and loses the binary search, because finding the position then costs O(n).

The program does not need the full order. The median needs only the boundary between the smaller half of the values and the larger half. The order inside each half does not matter. A structure that keeps the two halves separate, and can read the boundary from each side, avoids both costs.

<!-- stage: insight -->
### Splitting The Values Into Two Halves

The program keeps two `PriorityQueue` objects. The **lower half** is a max-first queue that holds the smaller half of the values. The **upper half** is a min-first queue that holds the larger half. The root of each queue is the value nearest to the middle on its side.

#### Two Rules That Define The Halves

The first rule is about order. Every value in the lower half is less than or equal to every value in the upper half. That holds exactly when the root of the lower half is at most the root of the upper half. The second rule is about size. The lower half holds either the same number of values as the upper half or one more.

#### Reading The Median

With an odd count, the lower half holds one extra value, and its root is the median. With an even count, the two roots are the two middle values, and the median is their average. Both reads cost O(1).

#### Rebalancing After An Insertion

The first value goes into the lower half. Later, a new value goes into the lower half when it is at most the lower root, and into the upper half otherwise. This placement keeps the order rule. The size rule may break by one. If the lower half now holds two more values than the upper half, the program moves the lower root to the upper half. If the upper half holds more than the lower half, it moves the upper root to the lower half. This step is the **rebalance**. Moving a root keeps the order rule, because that root is the nearest value to the boundary. Each insertion costs O(log n).

<!-- names: lower half, upper half, rebalance -->

<!-- stage: variables -->
### The State Of The Two Queues

The tracker keeps two queues and relies on four pieces of state about them.

- **Lower half** is a queue with the largest value at the root, and it holds `ceil(n / 2)` values.
- **Upper half** is a queue with the smallest value at the root, and it holds `floor(n / 2)` values.
- **Boundary** is the pair of roots, and the order rule says the lower root is at most the upper root.
- **Count n** is the total number of values, and its parity says whether the median is one root or an average.

The sizes follow from the count, so the program never stores them separately.

<!-- stage: trace -->
### Watching The Halves Change

#### Adding Five Values

Add the values 5, 2, 8, 1 and 9 in that order. The first trace follows the value just added with the pointer `next`. The variables `lower` and `upper` list the contents of each half in sorted order, and `median` shows the result after the rebalance.

The value 5 enters the lower half alone. The value 2 is at most the lower root 5, so it enters the lower half, which then holds two values. The program moves the root 5 to the upper half, and the median becomes 3.5. The value 8 goes to the upper half and forces the root 5 back to the lower half. The medians for the five values are 5, 3.5, 5, 3.5 and 5.

#### Adding Two Extreme Values

The second trace adds 2,147,483,647 and 2,147,483,646. After the second value the even count needs the average of the two roots. A sum in `int` arithmetic wraps to a negative number. Converting one operand to `long` before the addition gives the true sum, and the average is 2,147,483,646.5.

#### Stepping Through Both Runs

```trace
{"cells":[5,2,8,1,9],"pointers":["next"],"steps":[{"at":{"next":0},"vars":{"lower":"[5]","upper":"[]","median":5},"note":"The value 5 goes to the lower half. The sizes already follow the rule. The median is 5."},{"at":{"next":1},"vars":{"lower":"[2]","upper":"[5]","median":3.5},"note":"The value 2 goes to the lower half. The lower half is two ahead, so its root 5 moves to the upper half. The median is 3.5."},{"at":{"next":2},"vars":{"lower":"[2, 5]","upper":"[8]","median":5},"note":"The value 8 goes to the upper half. The upper half is ahead, so its root 5 moves to the lower half. The median is 5."},{"at":{"next":3},"vars":{"lower":"[1, 2]","upper":"[5, 8]","median":3.5},"note":"The value 1 goes to the lower half. The lower half is two ahead, so its root 5 moves to the upper half. The median is 3.5."},{"at":{"next":4},"vars":{"lower":"[1, 2, 5]","upper":"[8, 9]","median":5},"note":"The value 9 goes to the upper half. The upper half is ahead, so its root 5 moves to the lower half. The median is 5."}]}
```

```trace
{"cells":[2147483647,2147483646],"pointers":["next"],"steps":[{"at":{"next":-1},"vars":{"lower":"[]","upper":"[]","median":"none"},"note":"Both halves are empty, and no median exists yet."},{"at":{"next":0},"vars":{"lower":"[2147483647]","upper":"[]","median":2147483647},"note":"The value 2147483647 goes to the lower half. The sizes already follow the rule. The median is 2147483647."},{"at":{"next":1},"vars":{"lower":"[2147483646]","upper":"[2147483647]","median":2147483646.5},"note":"The value 2147483646 goes to the lower half, and the rebalance leaves one value in each half. In int arithmetic 2147483647 + 2147483646 wraps to -3. With a long sum, the average is 2147483646.5."}]}
```

<!-- stage: code -->
### Writing The Median Tracker

#### Insert And Read

The class below is a complete tracker. The call to `median` requires at least one inserted value.

```java
final class MedianTracker {
    private final PriorityQueue<Integer> lower = new PriorityQueue<>(Comparator.reverseOrder());
    private final PriorityQueue<Integer> upper = new PriorityQueue<>();

    void add(int v) {
        if (lower.isEmpty() || v <= lower.peek()) lower.offer(v);      // the order rule decides the side
        else upper.offer(v);
        if (lower.size() > upper.size() + 1) upper.offer(lower.poll()); // lower is two values ahead
        else if (upper.size() > lower.size()) lower.offer(upper.poll()); // upper is ahead
    }

    double median() {
        if (lower.size() > upper.size()) return lower.peek();           // odd count
        return ((long) lower.peek() + upper.peek()) / 2.0;             // even count, summed as long
    }
}
```

#### Cost Of The Tracker

Each `add` makes at most three queue operations, so it costs O(log n). The `median` method reads the roots in O(1). The two queues hold all n values, so the memory is O(n).

<!-- stage: applicability -->
### Recognizing A Running Median Question

#### Spotting The Pattern

The cue is a stream of values where each prefix needs its middle value. The invariant has two parts. The lower half holds the same count as the upper half or one more. Every lower value is at most every upper value.

#### Finding The False Friend

The false friend is one queue. A single queue exposes one extreme, the smallest or the largest value, and never the middle. A second false friend is the sorted list of the naive plan, which reads the median fast but pays O(n) to insert.

#### Recognizing The No-Go Cases

The two halves answer only the median. They do not answer a rank that changes with the question, such as the 90th percentile together with the median. For that, the program needs a structure that counts values by rank. The halves also do not support deleting an arbitrary value without the delayed deletion of the previous lesson.

<!-- stage: exercises -->
### Exercises

#### [Build] Rebalance Two Halves (Author exercise)
<!-- id: hp-rebalance-halves -->

**Prerequisites.** The two halves and the rebalance rule of this lesson.

**Problem.** Given an array `values`, insert the values one by one into a lower half and an upper half that follow the two rules of this lesson. After each insertion, record the root of the lower half. After `i` values, that root sits at sorted position `ceil(i / 2)`. It is the smaller middle value when `i` is even. Return the array of recorded roots.

**Constraints.** The limits are:
- **Length** is `0 <= values.length <= 10^5`.
- **Values** are `int` values, and duplicates are allowed.
- **Answer** has one entry per input value.
- **Mutation** does not occur; `values` keeps its order.

**Example 1.** Input `values = [5,2,8,1]`, output `[5,2,5,2]`.

**Example 2.** Input `values = []`, output `[]`.

**Hint.** Which half receives a value that equals the lower root? After the move of one root, which rule does the program check next?

**Changed decision.** The program moves one root across the boundary whenever the sizes differ by more than the size rule allows.

#### [Vary] Find Median from Data Stream (LeetCode 295)
<!-- id: hp-find-median-stream -->

**Prerequisites.** The previous exercise.

**Problem.** Design a class `MedianFinder` with `void addNum(int num)` and `double findMedian()`. The call `findMedian` returns the middle value of all numbers added so far when the count is odd. For an even count, it returns the average of the two middle values. It is called only after at least one `addNum`.

**Constraints.** The limits are:
- **Calls** number at most `10^5`.
- **Values** are `int` values from `-10^5` to `10^5`.
- **Return** is a `double`, and an answer within `10^-5` of the exact value is accepted.

**Example 1.** Input `addNum(6)`, `addNum(10)`, `addNum(2)`, with `findMedian()` after each, output `6.0, 8.0, 6.0`.

**Example 2.** Input `addNum(3)`, `addNum(3)`, then `findMedian()`, output `3.0`.

**Hint.** Which roots does the program read when the count is even? What does the sign of `lower.size() - upper.size()` tell it?

**Changed decision.** The method reads one root for an odd count and averages two roots for an even count.

#### [Boundary] Overflow-Safe Even Median (Author exercise)
<!-- id: hp-overflow-safe-median -->

**Prerequisites.** The two exercises above.

**Problem.** Given a non-empty array `values` of `int` values, return the median of all values as a `double`. For an even count, the median is the average of the two middle values. Every `int` is a legal value, so the sum of the two middle values can exceed the range of `int`.

**Constraints.** The limits are:
- **Length** is `1 <= values.length <= 10^5`.
- **Values** are any `int` values, including `Integer.MIN_VALUE` and `Integer.MAX_VALUE`.
- **Return** is a `double` that is exact for the average of two `int` values.

**Example 1.** Input `values = [2147483647,2147483646]`, output 2147483646.5.

**Example 2.** Input `values = [-2147483648,-2147483648]`, output -2147483648.0.

**Hint.** What does `a + b` return when both values are near `Integer.MAX_VALUE`? Which operand needs the cast, and when must the cast happen?

**Changed decision.** The program widens one operand to `long` before the addition, so the sum cannot wrap.

#### [Recognize] Sliding Window Median (LeetCode 480)
<!-- id: hp-window-median-full -->

**Prerequisites.** All three exercises above and the delayed deletion lesson.

**Problem.** Given an array `nums` and a window size `k`, return the median of each window of `k` consecutive values, from left to right. For an even `k`, the median is the average of the two middle values. Keep two halves. When a value leaves the window, delete it lazily, and keep a separate count of the live values in each half.

**Constraints.** The limits are:
- **Length** is `1 <= nums.length <= 10^5`.
- **Window** satisfies `1 <= k <= nums.length`.
- **Values** are any `int` values, including `Integer.MIN_VALUE` and `Integer.MAX_VALUE`.
- **Answer** has `nums.length - k + 1` entries of type `double`.

**Example 1.** Input `nums = [4,2,12,3,8,1]` and `k = 3`, output `[4.0,3.0,8.0,3.0]`.

**Example 2.** Input `nums = [1,5,2,2]` and `k = 2`, output `[3.0,3.5,2.0]`.

**Hint.** Which size decides whether the program rebalances, the queue size or the live count? What must hold about each root before the program reads it?

**Changed decision.** Expiry marks an entry as stale and lowers a live count, and the rebalance reads the live counts.
