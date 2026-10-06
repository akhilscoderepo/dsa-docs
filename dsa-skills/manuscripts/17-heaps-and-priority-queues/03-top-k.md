<!-- lesson-kind: standard -->
<!-- lesson-id: top-k -->
## Keep Only The Best K Items

<!-- stage: context -->
### Why The Leaderboard Runs Out Of Memory

A game server records one score event for every match and shows the ten highest scores of the day. On a quiet day the server stores all events in a list, sorts the list and prints the first ten. On a launch day the server receives 50 million events, and the list no longer fits in memory. Even when it fits, the server sorts all 50 million values to show ten of them.

The server needs only ten values and may forget the rest. This lesson asks which values the program must keep at any moment. It also asks how the program decides whether a new score belongs among the best.

<!-- stage: naive -->
### Sorting Every Value Before Taking Ten

The direct plan stores every value, sorts the whole array and copies the last `k` positions.

```java
static int[] kLargestBySort(int[] values, int k) {
    int[] copy = values.clone();                     // the full array stays in memory
    Arrays.sort(copy);                               // orders all n values, ascending
    int[] best = new int[k];
    for (int i = 0; i < k; i++) {
        best[i] = copy[copy.length - 1 - i];         // walk back from the largest
    }
    return best;
}
```

The method returns the right answer for any `k` from 0 to `n`. It needs memory for all `n` values and it orders values that the answer never uses.

<!-- stage: bottleneck -->
### Counting What The Sort Wastes

```predict
The server has n = 50,000,000 scores and keeps k = 10. How much work does the sort do, and how many values does the answer actually need?

The sort does about n log2(n), roughly 1.3 billion comparisons, and holds all n values. The answer needs only k = 10 values, so most of that work orders values that never appear.
```

Sorting costs O(n log n) time and O(n) memory. A value that is far below the tenth best never matters, yet the sort compares it with its neighbors many times. The work is spent on the order among the losers.

A queue that holds every value, with the largest at the root, has the same problem. Building it with n offers costs O(n log n) and it still needs O(n) memory. The queue must hold only the candidates that can still affect the answer, and the program must discard the others at once.

<!-- stage: insight -->
### Guarding The Boundary With A Small Queue

The program keeps a **size-k min-heap**, which is a `PriorityQueue` with the natural order that never holds more than `k` values. The `k` values it holds are the `k` largest values seen so far. The smallest of them sits at the root.

#### What The Root Means

The root is the **retention boundary**. Every kept value is at least as large as the root. Any new value smaller than the root has `k` kept values at least as large as itself. It can never be one of the `k` largest, so the program discards it.

#### Deciding For Each New Value

While the queue holds fewer than `k` values, every value goes in with `offer`. After that, the program compares each new value `v` with the root. If `v` is not larger than the root, the program discards `v`. If `v` is larger, the program does one step, named **replace the root**. It removes the root and inserts `v`. The old root is no longer among the `k` largest, because `k` larger values now exist.

#### Reading The Answer

After the scan, the queue holds the `k` largest values and the root is the kth largest value. Polling the queue returns the kept values in ascending order. Each of the `n` values costs O(log k) at most, so the scan costs O(n log k) time and O(k) memory.

<!-- names: size-k min-heap, retention boundary, replace the root -->

<!-- stage: variables -->
### The Four Pieces Of State

The scan needs one queue and one rule, and the queue never grows past a fixed size.

- **Capacity k** is the number of values to keep, and the queue size never exceeds it.
- **Root** is the smallest kept value, so it is the value a new candidate must beat.
- **Candidate v** is the next value from the input, compared once with the root.
- **Kept count** equals the queue size, and it is below `k` only during the first `k` values.

The root changes only when a candidate beats it, and then the new root is the smaller of the next kept value and the candidate.

<!-- stage: trace -->
### Following The Queue Through A Stream

#### Keeping The Three Largest

Take the stream 4, 9, 2, 7, 5, 8, 3 with `k = 3`. The first trace uses the pointer `next` for the candidate under test, and the variable `kept` lists the queue contents in ascending order.

The first three values 4, 9 and 2 fill the queue, so the root is 2. The candidate 7 beats the root 2, so 2 leaves and 7 enters. The candidate 5 beats the new root 4, and 4 leaves. The candidate 8 beats the root 5, so 5 leaves. The candidate 3 is below the root 7 and gets discarded. The queue ends with 7, 8 and 9, and the root 7 is the third largest value.

#### Keeping Two Equal Values

The second trace uses the stream 5, 5, 5, 1 with `k = 2`. The candidate 5 equals the root, so the rule "larger than the root" discards it. The queue keeps 5 and 5, and the candidate 1 is discarded as well. Equal values cause no wrong answer, because replacing an equal value would change nothing.

#### Stepping Through Both Streams

```trace
{"cells":[4,9,2,7,5,8,3],"pointers":["next"],"steps":[{"at":{"next":0},"vars":{"kept":"[4]","root":4},"note":"The queue holds fewer than 3 values, so 4 enters. The kept values are [4]."},{"at":{"next":1},"vars":{"kept":"[4, 9]","root":4},"note":"The queue holds fewer than 3 values, so 9 enters. The kept values are [4, 9]."},{"at":{"next":2},"vars":{"kept":"[2, 4, 9]","root":2},"note":"The queue holds fewer than 3 values, so 2 enters. The kept values are [2, 4, 9]."},{"at":{"next":3},"vars":{"kept":"[4, 7, 9]","root":4},"note":"The candidate 7 beats the root 2. The value 2 leaves and 7 enters. The kept values are [4, 7, 9]."},{"at":{"next":4},"vars":{"kept":"[5, 7, 9]","root":5},"note":"The candidate 5 beats the root 4. The value 4 leaves and 5 enters. The kept values are [5, 7, 9]."},{"at":{"next":5},"vars":{"kept":"[7, 8, 9]","root":7},"note":"The candidate 8 beats the root 5. The value 5 leaves and 8 enters. The kept values are [7, 8, 9]."},{"at":{"next":6},"vars":{"kept":"[7, 8, 9]","root":7},"note":"The candidate 3 does not beat the root 7, so the program discards it. The kept values are [7, 8, 9]."}]}
```

```trace
{"cells":[5,5,5,1],"pointers":["next"],"steps":[{"at":{"next":0},"vars":{"kept":"[5]","root":5},"note":"The queue holds fewer than 2 values, so 5 enters. The kept values are [5]."},{"at":{"next":1},"vars":{"kept":"[5, 5]","root":5},"note":"The queue holds fewer than 2 values, so 5 enters. The kept values are [5, 5]."},{"at":{"next":2},"vars":{"kept":"[5, 5]","root":5},"note":"The candidate 5 does not beat the root 5, so the program discards it. The kept values are [5, 5]."},{"at":{"next":3},"vars":{"kept":"[5, 5]","root":5},"note":"The candidate 1 does not beat the root 5, so the program discards it. The kept values are [5, 5]."}]}
```

<!-- stage: code -->
### Writing The Scan In Java

#### Keeping The K Largest

The method returns the kept values in nonincreasing order. It fills the result from the last position, because each poll returns the smallest kept value.

```java
static int[] kLargest(int[] values, int k) {
    PriorityQueue<Integer> kept = new PriorityQueue<>();      // natural order, smallest value at the root
    for (int v : values) {
        if (kept.size() < k) {
            kept.offer(v);                                    // the first k values always stay
        } else if (k > 0 && v > kept.peek()) {
            kept.poll();                                      // the old root leaves
            kept.offer(v);                                    // the candidate takes its place
        }
    }
    int[] best = new int[kept.size()];
    for (int i = best.length - 1; i >= 0; i--) best[i] = kept.poll();  // smallest kept value goes last
    return best;
}
```

#### Cost And Direction

Each of the `n` values costs one `peek` in O(1) and at most one `poll` and one `offer` in O(log k). The scan runs in O(n log k) time with O(k) memory. The direction matters. A queue of `k` values with the largest at the root keeps the `k` smallest values, which is the opposite question.

<!-- stage: applicability -->
### Recognizing A Top K Question

#### Spotting The Pattern

The cue is a question that asks for only the best `k` items of a large or growing input. The invariant is that the queue holds the `k` best items seen so far and its root is the retention boundary. A kth largest question uses the same state and returns the root.

#### Finding The False Friend

The false friend is a max-heap that holds every item. It answers the question, because `k` polls return the `k` largest values. It keeps O(n) memory when `k` is small, and it adds O(n) build time before the first poll.

A second false friend is the opposite direction. A max-oriented queue that is trimmed to `k` values keeps the `k` smallest values.

#### Recognizing The No-Go Cases

The size-`k` queue does not fit when `k` is close to `n`, because sorting costs about the same and is simpler. It does not fit either when the program must answer many different values of `k` over the same data. Then one sort answers every question.

<!-- stage: exercises -->
### Exercises

#### [Build] K Largest Values (Author exercise)
<!-- id: hp-k-largest-values -->

**Prerequisites.** The size-`k` queue and the root rule of this lesson.

**Problem.** Given an array `values` of integers and an integer `k`, return the `k` largest values in nonincreasing order. Duplicates count separately. Keep a `PriorityQueue<Integer>` with the natural order that never holds more than `k` values.

**Constraints.** The limits are:
- **Length** is `0 <= values.length <= 10^5`.
- **Values** are `int` values, and duplicates are allowed.
- **k** satisfies `0 <= k <= values.length`.
- **Mutation** does not occur; `values` keeps its order.

**Example 1.** Input `values = [5,1,9,3,7]` and `k = 3`, output `[9,7,5]`.

**Example 2.** Input `values = [2,2,2,1]` and `k = 2`, output `[2,2]`.

**Hint.** Which value does a new candidate compete with? What does the root say about every value that has already left the queue?

**Changed decision.** The queue size stays at `k`, and the root replaces itself only when a larger value arrives.

#### [Vary] Kth Largest Element in an Array (LeetCode 215)
<!-- id: hp-kth-largest-array -->

**Prerequisites.** The previous exercise.

**Problem.** Given an array `values` and an integer `k`, return the kth largest value of the array in sorted order, counting duplicates. The largest value is the 1st largest. Return the root of the size-`k` queue after one scan.

**Constraints.** The limits are:
- **Length** is `1 <= values.length <= 10^5`.
- **Values** are `int` values, and duplicates are allowed.
- **k** satisfies `1 <= k <= values.length`.
- **Mutation** does not occur; `values` keeps its order.

**Example 1.** Input `values = [8,3,8,1,6,6]` and `k = 3`, output 6.

**Example 2.** Input `values = [4]` and `k = 1`, output 4.

**Hint.** After the scan, what does the smallest of the `k` kept values mean for the whole array?

**Changed decision.** The method returns one value, the root, and not the whole queue.

#### [Boundary] K Equals One Or N (Author exercise)
<!-- id: hp-k-one-or-n -->

**Prerequisites.** The two exercises above.

**Problem.** Given an array `values` and an integer `k` with `1 <= k <= n`, return the sum of the `k` largest values as a `long`. The queue must keep the same rule at `k = 1`, where it holds one value, and at `k = n`, where it holds every value.

**Constraints.** The limits are:
- **Length** is `1 <= values.length <= 10^5`.
- **Values** are any `int` values, including `Integer.MAX_VALUE`.
- **Sum** needs the type `long`, because `int` addition can wrap.
- **Mutation** does not occur; `values` keeps its order.

**Example 1.** Input `values = [4,9,2]` and `k = 1`, output 9.

**Example 2.** Input `values = [2147483647,2147483647]` and `k = 2`, output 4294967294.

**Hint.** What does the queue hold when `k = n`? Where does an `int` sum of two large values go wrong?

**Changed decision.** The queue never evicts at `k = n`, and the sum type changes to `long`.

#### [Recognize] Top K Frequent Elements (LeetCode 347)
<!-- id: hp-top-k-frequent -->

**Prerequisites.** The previous three exercises and the hash map counting from Chapter 04.

**Problem.** Given an array `nums` and an integer `k`, return the `k` values that occur most often, in any order. The frequency of a value is the number of positions that hold it. The input guarantees that the set of `k` most frequent values is unique.

**Constraints.** The limits are:
- **Length** is `1 <= nums.length <= 10^5`.
- **Values** are `int` values.
- **k** satisfies `1 <= k <=` the number of distinct values.
- **Uniqueness** means no value outside the answer ties with the least frequent value inside it.

**Example 1.** Input `nums = [4,1,1,2,2,2,4,4,4]` and `k = 2`, output `[4,2]` in any order.

**Example 2.** Input `nums = [9]` and `k = 1`, output `[9]`.

**Hint.** Which number does the queue compare, the value or its frequency? What does the root hold after the scan?

**Changed decision.** The queue stores value and frequency pairs, ordered by frequency.
