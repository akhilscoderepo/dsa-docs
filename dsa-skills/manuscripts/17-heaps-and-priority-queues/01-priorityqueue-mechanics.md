<!-- lesson-kind: standard -->
<!-- lesson-id: priorityqueue-mechanics -->
## Take The Smallest Item Repeatedly

<!-- stage: context -->
### Why The Timer Loop Gets Slower

A web server gives every connection an expiry time. On each tick the server closes the connection that expires first, then accepts new connections. The first version keeps the expiry times in a list and scans the whole list on every tick. With 1,000 connections nobody notices. With 200,000 connections the scans dominate the processor, and the tick that should take microseconds takes milliseconds.

The server needs only one fact from the list, the smallest value. The set of values changes between ticks, because connections arrive and leave. This lesson asks how a program takes the smallest value of a changing set without looking at every value each time.

<!-- stage: naive -->
### Scanning The List On Every Tick

The direct plan keeps the expiry times in an `ArrayList`. Each tick scans for the smallest value and removes it.

```java
static int removeEarliest(List<Integer> expiry) {
    int best = 0;
    for (int i = 1; i < expiry.size(); i++) {
        if (expiry.get(i) < expiry.get(best)) best = i;   // remember the position of the smallest value so far
    }
    return expiry.remove(best);                            // removes by position and shifts later values left
}
```

The method is correct on every input. Adding a new connection costs one `add` at the end of the list. Finding the earliest costs a full scan, and the removal shifts every later value one place left.

<!-- stage: bottleneck -->
### Counting The Comparisons

```predict
A list holds n = 200,000 expiry times. The server removes them one at a time with removeEarliest. About how many comparisons does the scan perform in total?

The scans compare n - 1, then n - 2, and so on down to 0 pairs. That sum is n(n - 1) / 2, about 2 * 10^10 comparisons, which is O(n^2).
```

One call costs O(n), because the scan reads every value and the removal shifts up to n values. Removing all n values costs O(n^2). The waste is repeated work. Each scan re-reads values that the previous scan already compared with each other, and it throws that knowledge away.

Sorting the list once does not fix the problem. A sorted list gives the smallest value in constant time. But every new connection must land in its sorted place, and inserting into the middle of an array costs O(n) because later values shift. The program needs a structure that keeps just enough order for the smallest value and costs less than a full sort to maintain.

<!-- stage: insight -->
### Keeping Only Partial Order

A **priority queue** is a collection with two core operations. The first adds an item. The second removes the item with the smallest key. Java's `PriorityQueue` implements it with a binary heap stored in a plain array. The key comes from the natural order of the items, or from a comparator that the next lesson covers.

#### What Heap Order Says

The array holds the items in positions 0 to `n - 1`. The item at position `i` has its parent at position `(i - 1) / 2`. Its children sit at positions `2 * i + 1` and `2 * i + 2`. **Heap order** is the rule that every item is less than or equal to its children. The smallest item then sits at position 0, so `peek` reads it in O(1) time.

Heap order is a partial order. A parent is no larger than its children. Two siblings have no required order. Items in different branches have no required relation either. The array is therefore not sorted.

#### Adding An Item

`offer` writes the new item at position `n`. The item may be smaller than its parent, so the queue runs **sift up**. It swaps the item with its parent while the item is smaller, and it stops at the first parent that is not larger. Each swap moves the item up one level. A binary tree of `n` items has about log2(n) levels, so `offer` costs O(log n).

#### Removing The Smallest Item

`poll` takes the item at position 0. The queue moves the last item of the array into position 0 and shrinks the array by one. That item may be larger than its children, so the queue runs **sift down**. It swaps the item with the smaller of its two children while that child is smaller than the item. Each swap moves the item one level down, so `poll` also costs O(log n).

<!-- names: priority queue, heap order, sift -->

<!-- stage: variables -->
### The State Behind One Queue

A queue is one array and one count, and the count is the only number the rules need.

- **Array position i** holds one item. Its parent sits at `(i - 1) / 2`, and its children sit at `2 * i + 1` and `2 * i + 2`.
- **Size n** counts the stored items. Positions at or beyond `n` hold no item.
- **Root** is position 0. It holds the smallest item whenever heap order holds.
- **Moving item** is the one value that sift up or sift down carries along a path, one swap at a time.

Every `offer` and every `poll` restores heap order before it returns, so the next call always starts from a valid queue.

<!-- stage: trace -->
### Watching Items Move Through The Array

#### Adding Five Values

Start with an empty queue and offer 5, 3, 8, 1 and 4 in that order. In the first trace the pointer `next` marks the value just offered, and the variable `array` shows the queue after sift up finishes.

The values 5, 3 and 8 take few steps. The value 3 swaps with its parent 5. The value 8 stays in place, because its parent 3 is smaller. The value 1 is the interesting case, because it swaps twice and travels from position 3 to position 0. The value 4 stops at once, because its parent 3 is smaller. The final array is not sorted, because 8 sits before 5 and 4.

#### Removing Two Smallest Values

Now start with the array from the first trace and poll twice. In the second trace the pointer `hole` marks where the moving item sits. The pointer `child` marks the smaller child that the item is compared with.

The first poll returns 1. The queue moves the last item 4 to the root and compares it with its smaller child 3. The item 4 swaps down once and stops, because its new child 5 is larger. The second poll returns 3, and the moving item 5 swaps with its smaller child 4. Each poll returns the current smallest value, so the two polls return 1 and then 3.

#### Stepping Through Both Runs

```trace
{"cells":[5,3,8,1,4],"pointers":["next"],"steps":[{"at":{"next":0},"vars":{"array":"[5]"},"note":"The value 5 enters at the end and swaps 0 time(s) during sift up. The array is now [5]."},{"at":{"next":1},"vars":{"array":"[3, 5]"},"note":"The value 3 enters at the end and swaps 1 time(s) during sift up. The array is now [3, 5]."},{"at":{"next":2},"vars":{"array":"[3, 5, 8]"},"note":"The value 8 enters at the end and swaps 0 time(s) during sift up. The array is now [3, 5, 8]."},{"at":{"next":3},"vars":{"array":"[1, 3, 8, 5]"},"note":"The value 1 enters at the end and swaps 2 time(s) during sift up. The array is now [1, 3, 8, 5]."},{"at":{"next":4},"vars":{"array":"[1, 3, 8, 5, 4]"},"note":"The value 4 enters at the end and swaps 0 time(s) during sift up. The array is now [1, 3, 8, 5, 4]."},{"at":{"next":5},"vars":{"array":"[1, 3, 8, 5, 4]"},"note":"All values are in. The root is 1, and the array [1, 3, 8, 5, 4] is not in sorted order."}]}
```

```trace
{"cells":[1,3,8,5,4],"pointers":["hole","child"],"steps":[{"at":{"hole":-1,"child":-1},"vars":{"array":"[1, 3, 8, 5, 4]","returned":"[]"},"note":"The queue holds [1, 3, 8, 5, 4] and no poll has run."},{"at":{"hole":0,"child":-1},"vars":{"array":"[4, 3, 8, 5]","returned":"[1]"},"note":"The poll takes 1 from the root. The last item 4 moves to the root, so the array is [4, 3, 8, 5]."},{"at":{"hole":1,"child":-1},"vars":{"array":"[3, 4, 8, 5]","returned":"[1]"},"note":"The item swaps with its smaller child. The moving item now sits at position 1, and the array is [3, 4, 8, 5]."},{"at":{"hole":1,"child":3},"vars":{"array":"[3, 4, 8, 5]","returned":"[1]"},"note":"The smaller child 5 is not smaller than 4, so sift down stops."},{"at":{"hole":0,"child":-1},"vars":{"array":"[5, 4, 8]","returned":"[1, 3]"},"note":"The poll takes 3 from the root. The last item 5 moves to the root, so the array is [5, 4, 8]."},{"at":{"hole":1,"child":-1},"vars":{"array":"[4, 5, 8]","returned":"[1, 3]"},"note":"The item swaps with its smaller child. The moving item now sits at position 1, and the array is [4, 5, 8]."}]}
```

<!-- stage: code -->
### Using PriorityQueue In Java

#### Sorting By Repeated Removal

The method below adds every value once and removes them all. The removal order is nondecreasing, so the loop sorts the input.

```java
static int[] sortWithQueue(int[] values) {
    PriorityQueue<Integer> queue = new PriorityQueue<>();   // smallest item first
    for (int v : values) queue.offer(v);                    // n offers, each O(log n)
    int[] sorted = new int[values.length];
    for (int i = 0; i < sorted.length; i++) {
        sorted[i] = queue.poll();                           // n polls, each O(log n)
    }
    return sorted;
}
```

#### Taking The Largest First

The default order puts the smallest item first. To take the largest item first, pass `Collections.reverseOrder()` to the constructor.

```java
static List<Integer> drainLargestFirst(int[] values) {
    PriorityQueue<Integer> queue = new PriorityQueue<>(Collections.reverseOrder());
    for (int v : values) queue.offer(v);
    List<Integer> out = new ArrayList<>();
    while (!queue.isEmpty()) out.add(queue.poll());         // the largest remaining item leaves first
    return out;
}
```

Both methods cost O(n log n), because n offers and n polls each cost O(log n). `peek` and `poll` return `null` on an empty queue, while `element` and `remove()` throw `NoSuchElementException`.

<!-- stage: applicability -->
### Deciding When A Priority Queue Fits

#### Spotting The Pattern

Use a priority queue when the algorithm repeatedly needs the smallest or largest eligible item and the set of candidates changes between requests. The invariant of the lesson is heap order. After every operation, the item at position 0 is the extreme under the queue's order. The rest of the array is only partly ordered.

#### Finding The False Friend

The false friend is iteration. A `for` loop over a `PriorityQueue`, its `toString` and its stream all follow array order, and array order is not sorted order. The array `[1, 3, 8, 5, 4]` from the first trace shows this. To read items in order, the program must call `poll` repeatedly.

A second false friend is `contains` and `remove(Object)`. Both scan the array, so each costs O(n) and not O(log n).

#### Recognizing The No-Go Cases

A priority queue does not fit when the program needs the third smallest item without removing two others. It also does not fit when the program needs sorted order many times or access by rank. A single scan also beats the queue when the program reads the smallest value only once, because the scan and the build both cost O(n).

<!-- stage: exercises -->
### Exercises

#### [Build] Repeated Minimum (Author exercise)
<!-- id: hp-repeated-minimum -->

**Prerequisites.** The `offer` and `poll` operations of this lesson.

**Problem.** Given an array `values` of integers, return a new array that holds the same values in nondecreasing order. Add every value to a `PriorityQueue<Integer>` with `offer`, then fill the result by calling `poll` once for each value.

**Constraints.** The limits are:
- **Length** is `0 <= values.length <= 10^5`.
- **Values** are `int` values, and duplicates are allowed.
- **Mutation** does not occur; `values` keeps its order.

**Example 1.** Input `values = [7,2,9,2]`, output `[2,2,7,9]`.

**Example 2.** Input `values = []`, output `[]`.

**Hint.** What does the smallest remaining value look like after each `poll`? Does a duplicate leave the queue once or twice?

**Changed decision.** Basic case: the result comes from repeated removal and not from a comparison sort call.

#### [Vary] Last Stone Weight (LeetCode 1046)
<!-- id: hp-last-stone -->

**Prerequisites.** The previous exercise and `Collections.reverseOrder()` from the code stage.

**Problem.** Given an array `stones` of positive integer weights, repeat the following round while at least two stones remain. Take the two heaviest stones with weights `x <= y`. If `x == y`, discard both. Otherwise discard both and add a stone of weight `y - x`. Return the weight of the last stone, or 0 when no stone remains.

**Constraints.** The limits are:
- **Length** is `1 <= stones.length <= 30`.
- **Weights** satisfy `1 <= stones[i] <= 1000`.
- **Mutation** does not occur; `stones` keeps its order.

**Example 1.** Input `stones = [9,4,6,2]`, output 1.

**Example 2.** Input `stones = [5,5]`, output 0.

**Hint.** The decision that changes is the direction of the order. Which end of the queue must `poll` return in each round?

**Changed decision.** The queue returns the largest item first, and each round inserts a new value.

#### [Boundary] Empty And Singleton Heap (Author exercise)
<!-- id: hp-empty-singleton -->

**Prerequisites.** The `peek` and `poll` return rules in the code stage.

**Problem.** Given an array `values` of integers and an integer `m >= 0`, add every value to a `PriorityQueue<Integer>`. Call `poll` up to `m` times, and stop early when the queue becomes empty. Return the smallest remaining value without removing it, or `null` when no value remains.

**Constraints.** The limits are:
- **Length** is `0 <= values.length <= 10^5`.
- **Values** are `int` values, and any `int` can be a valid answer.
- **Count** satisfies `0 <= m <= 10^6`, and `m` may exceed the length.
- **Return** type is `Integer`, so `null` cannot be confused with a value.

**Example 1.** Input `values = [4,1,3]` and `m = 2`, output 4.

**Example 2.** Input `values = [4]` and `m = 1`, output `null`.

**Hint.** What do `poll` and `peek` return on an empty queue? Which loop condition prevents a call that throws?

**Changed decision.** The loop checks emptiness before each removal, so a count larger than the size is safe.

#### [Recognize] Kth Largest Element in a Stream (LeetCode 703)
<!-- id: hp-kth-largest-stream -->

**Prerequisites.** All three exercises above.

**Problem.** Design a class `KthLargest` with a constructor `KthLargest(int k, int[] nums)` and a method `int add(int val)`. After the constructor and after each `add`, the structure has seen a multiset of values. The method `add` inserts `val` and returns the kth largest value of that multiset, counting duplicates, so the largest value is the 1st largest.

**Constraints.** The limits are:
- **k** satisfies `1 <= k <= 10^4`.
- **Values** are `int` values, and the initial array may be empty.
- **Calls** number at most `10^4`, and every `add` call finds at least `k` values stored after inserting `val`.

**Example 1.** Input `k = 2`, `nums = [6,1,9]`, then `add(4)`, `add(10)`, `add(2)`, output `6, 9, 9`.

**Example 2.** Input `k = 1`, `nums = []`, then `add(3)`, `add(-2)`, output `3, 3`.

**Hint.** Which items can never be the kth largest again? What does the smallest item of a queue that holds only the k largest items represent?

**Changed decision.** The queue stays at size `k`, so its root is the answer and the other values leave.
