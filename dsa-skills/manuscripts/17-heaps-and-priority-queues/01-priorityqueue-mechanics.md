<!-- lesson-kind: standard -->
<!-- lesson-id: priorityqueue-mechanics -->
## PriorityQueue Mechanics

<!-- stage: context -->
### The Watch Repair Bench

A watchmaker's bench takes in work all day. Every ticket carries a due day, and whenever she finishes a job she reaches for the ticket with the earliest due day, whatever order the tickets arrived in. Customers walk in at any hour, and some of them bring a watch that is due tomorrow while the pile still holds work due next month, so the next job to pick up can change at any moment.

She never needs the whole pile in order. She needs exactly one fact, which ticket comes next, and she needs to drop a new ticket onto the bench without disturbing the rest. Her apprentice currently sorts the pile again every morning, and on busy weeks the bench holds thousands of tickets, so the morning sort has started to take longer than the repairs themselves.

<!-- stage: naive -->
### Search The Whole Pile Each Time

The direct method keeps the due days in an `ArrayList` and, whenever a job is finished, searches the list for the smallest value and removes it.

```java
static int takeMostUrgentByScan(java.util.ArrayList<Integer> pile) {
    int best = 0;
    for (int i = 1; i < pile.size(); i++) {
        if (pile.get(i) < pile.get(best)) best = i;
    }
    return pile.remove(best);
}
```

It is correct. From the pile `[7, 3, 9, 1, 5]` it returns 1, and a new ticket is added with a plain `add` at the end, which costs nothing.

<!-- stage: bottleneck -->
### Every Pickup Searches Everything

Adding is cheap, but each pickup reads every ticket in the pile and then shifts the tail of the list to close the gap, so one pickup costs O(n). Emptying a pile of `n` tickets costs about n times n over two, which is O(n^2). With a hundred thousand tickets that is several billion comparisons, and it all comes from rediscovering the minimum of nearly the same pile again and again. A sorted list reverses the trade and does not help: a pickup becomes cheap, but every insertion must shift a part of the list to keep the order, and again costs O(n).

Both versions pay for more than the bench needs. A fully sorted pile answers a question nobody asked, namely where the fifth most urgent ticket is. The bench only ever asks for the single most urgent ticket. A structure that keeps just enough order to name the minimum, and that repairs itself cheaply when a ticket enters or leaves, would give logarithmic work for both operations.

<!-- stage: insight -->
### A Tree In An Array

The structure is the **heap order**, stored in the Java class `PriorityQueue`. Picture a binary tree filled level by level from left to right, laid out in one array, where the rule is that every parent is no larger than either of its children. Then the smallest item is always at index 0, and `peek` reads it in constant time. The rule says nothing about the relation between two siblings, or between cousins, so the array is only partly ordered, and that is exactly why keeping it is cheap.

Each change restores the rule along a single path. To `offer` an item, append it at the end of the array and run **sift-up**: while the item is smaller than its parent, swap them. To `poll`, take the root away, move the last item of the array into the empty root, and run **sift-down**: while the item is larger than its smaller child, swap it with that child. A path in a tree with `n` nodes has about log2(n) steps, so `offer` and `poll` each cost O(log n), and `peek` costs O(1).

<!-- names: heap order, sift-up, sift-down -->

The word "smaller" always means smaller under the queue's comparator, which is the natural order of the elements unless one is supplied. The root is therefore the extreme in that order, and everything below it is only known to be no better than its parent. Taking all items out by repeated `poll` produces them in order, but the array itself is not in order at any moment, so reading it directly, or iterating over the queue, shows the heap's internal arrangement and not a sorted list.

<!-- stage: variables -->
### Array, Size And Comparator

The array holds the items, and its length used in the heap is the `size`. The item at index `i` has its parent at `(i - 1) / 2` with integer division, and its children at `2i + 1` and `2i + 2` when those indices are below `size`. The root index 0 changes only when an offered item climbs all the way to it, or when a poll replaces it. The comparator, either supplied at construction or taken from the elements, decides what smaller means, and it must not change while items are inside the queue. The size grows by one on each `offer` and shrinks by one on each `poll`. When the queue is empty, `peek` and `poll` return `null`, while `element` and `remove` throw an exception.

<!-- stage: trace -->
### Two Tickets Climb And One Root Sinks

The first run offers the due days `7, 3, 9, 1, 5, 2` in that order. The 7 is alone and is the root. The 3 is appended under the 7, is smaller than its parent, and swaps up. The 9 stays where it lands. The 1 is appended at index 3, swaps with the 7 at index 1, and then swaps with the 3 at the root, so it climbs two levels. The 5 stays. The 2 is appended at index 5, swaps with the 9 at index 2, and stops below the root 1. The final array `[1, 3, 2, 7, 5, 9]` is a valid heap and is clearly not sorted, since the 2 sits after the 3.

The second run polls the root of a heap built from `4, 8, 6, 9, 12, 7, 10`. The root 4 leaves, the last item 10 is moved to index 0, and the trace follows the node that holds the 10 as it sinks. The step to study is the first one after the move, where the node has two children, 8 and 6, and the 10 must swap with the smaller of them and not with the left one by habit.

```trace
{"cells":[7,3,9,1,5,2],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"heap":"[7]","root":7},"note":"Value 7 is appended at index 0. Its parent is not larger, so it stays. The root is 7."},{"at":{"i":1},"vars":{"heap":"[3,7]","root":3},"note":"Value 3 is appended at index 1. Sift-up moves it up 1 level, to index 0. The root is 3."},{"at":{"i":2},"vars":{"heap":"[3,7,9]","root":3},"note":"Value 9 is appended at index 2. Its parent is not larger, so it stays. The root is 3."},{"at":{"i":3},"vars":{"heap":"[1,3,9,7]","root":1},"note":"Value 1 is appended at index 3. Sift-up moves it up 2 levels, to index 0. The root is 1."},{"at":{"i":4},"vars":{"heap":"[1,3,9,7,5]","root":1},"note":"Value 5 is appended at index 4. Its parent is not larger, so it stays. The root is 1."},{"at":{"i":5},"vars":{"heap":"[1,3,2,7,5,9]","root":1},"note":"Value 2 is appended at index 5. Sift-up moves it up 1 level, to index 2. The root is 1."}]}
```

```trace
{"cells":[10,8,6,9,12,7],"pointers":["node"],"steps":[{"at":{"node":0},"vars":{"heap":"[10,8,6,9,12,7]","removed":4},"note":"The root 4 is polled and the last item 10 is moved to index 0. The array is shown after that move, and the value 10 must now sink to its place."},{"at":{"node":2},"vars":{"heap":"[6,8,10,9,12,7]","removed":4},"note":"The children of index 0 hold 8 and 6. The smaller child 6 is less than 10, so it moves up and 10 sinks to index 2."},{"at":{"node":5},"vars":{"heap":"[6,8,7,9,12,10]","removed":4},"note":"The children of index 2 hold 7. The smaller child 7 is less than 10, so it moves up and 10 sinks to index 5."},{"at":{"node":5},"vars":{"heap":"[6,8,7,9,12,10]","removed":4},"note":"Index 5 has no children, so the sink stops. The heap order is restored."}]}
```

<!-- stage: code -->
### Queue Operations In Java

```java
static int[] drainInOrder(int[] values) {
    java.util.PriorityQueue<Integer> queue = new java.util.PriorityQueue<>();
    for (int v : values) queue.offer(v);         // append, then sift-up
    int[] out = new int[values.length];
    for (int i = 0; i < out.length; i++) {
        out[i] = queue.poll();                   // root leaves, last item sinks
    }
    return out;
}
```

Each of the two loops makes `n` operations that cost O(log n) apiece, so the method runs in O(n log n) time with O(n) memory for the queue, and this is the same bound as sorting, with the difference that it can be stopped after any number of polls. The unboxing in `queue.poll()` is safe here because the queue holds exactly `n` items when the second loop starts. On a possibly empty queue the result is `null`, and unboxing it to an `int` would throw a `NullPointerException`. For a maximum-first queue a comparator is passed to the constructor, a topic that the next lesson treats in detail.

<!-- stage: applicability -->
### When The Next Item Keeps Changing

Reach for a `PriorityQueue` when a loop keeps asking for the smallest or largest item among candidates that come and go. The invariant to say aloud is that `peek` is the extreme under the comparator and that every parent in the array is no better than its children, which is a statement about the root only. Offer when a candidate becomes eligible, and poll when you commit to it.

The false friend is the iteration order. A `for` loop over the queue, `toString`, and the stream of its elements all walk the array from index 0 and show a partly ordered arrangement, so they must never be used to read a sorted list. Another false friend is a `TreeSet`, which keeps everything sorted at a logarithmic cost and supports removal of any item, but silently drops equal elements, and a heap keeps duplicates. A plain sort is simpler and faster when all items are known at the start and every one of them is wanted in order.

Do not use a heap when you need the k-th item from the middle, a search for an arbitrary item, or the removal of an arbitrary item, because `contains` and `remove(Object)` walk the whole array. In Java, the queue rejects `null`, throws a `ClassCastException` for elements that are not comparable when no comparator is given, and is not safe for use by several threads at once.

<!-- stage: exercises -->
### Exercises

#### [Build] Repeated Minimum (Author exercise)
<!-- id: hp-repeated-minimum -->

**Prerequisites.** The array layout and the offer and poll moves of this lesson.

**Problem.** Given an integer array `values`, put every value into a `PriorityQueue`, then poll until the queue is empty, and return the polled values in the order they came out.

**Constraints.** 0 <= values.length <= 10^5 and -10^9 <= values[i] <= 10^9. Duplicates are allowed.

**Example 1.** Input `values = [9, 4, 7, 4, 1]`, output `[1, 4, 4, 7, 9]`.

**Example 2.** Input `values = [-3, 8, -3, 0]`, output `[-3, -3, 0, 8]`, which shows that equal values are kept and not merged.

**Hint.** Which end of the queue does `poll` read? Does the output order depend on the order in which the values were offered?

**Changed decision.** First rung: only offer and poll, with the natural order, and the full sequence of polls is read as a sorted list.

#### [Vary] Last Stone Weight (LeetCode 1046)
<!-- id: hp-last-stone-weight -->

**Prerequisites.** Repeated Minimum above, and the idea that a comparator can reverse the order.

**Problem.** Given an array `stones` of positive weights, repeat the following while at least two stones remain: take the two heaviest stones, and if their weights differ, put back one stone with the difference. Return the weight of the last remaining stone, or 0 if none remains.

**Constraints.** 1 <= stones.length <= 30 and 1 <= stones[i] <= 1000.

**Example 1.** Input `stones = [9, 3, 6, 6, 2]`, output 2.

**Example 2.** Input `stones = [5, 5]`, output 0.

**Hint.** The default queue gives the smallest item first. What must change so that the heaviest comes first, and does the new remainder go back into the same queue?

**Changed decision.** The queue must now hand out the largest item, and the loop offers a new item after each pair of polls.

#### [Boundary] Empty And Singleton Heap (Author exercise)
<!-- id: hp-empty-and-singleton -->

**Prerequisites.** The two exercises above.

**Problem.** Process the integer array `ops` against one natural-order `PriorityQueue`. A positive value `x` means offer `x`, the value 0 means poll, and the value -1 means peek. For every poll and every peek append the item returned, or 0 if the queue was empty, to the result. After the last operation append the number of items still in the queue.

**Constraints.** 1 <= ops.length <= 10^5, and each operation is -1, 0, or a value from 1 to 10^9. The queue is never asked for a value through a method that throws.

**Example 1.** Input `ops = [0, -1, 5, -1, 0, 0]`, output `[0, 0, 5, 5, 0, 0]`.

**Example 2.** Input `ops = [4, 4, 0, -1]`, output `[4, 4, 1]`, where the one remaining item is both the peek and the next poll.

**Hint.** Which of `peek`, `poll`, `element` and `remove` return a marker on an empty queue, and which throw? What does a queue with a single item return for both peek and poll?

**Changed decision.** The queue may be empty or hold a single item, so each read must be legal there, and the final size is reported to expose what was left.

#### [Recognize] Kth Largest Element in a Stream (LeetCode 703)
<!-- id: hp-kth-largest-stream -->

**Prerequisites.** All three exercises above.

**Problem.** Given an integer `k` and an initial array `initial`, process each value of the array `adds` in turn, adding it to the collection, and after each addition report the k-th largest value in the collection, counting duplicates separately.

**Constraints.** 1 <= k <= 10^4, 0 <= initial.length <= 10^4, 1 <= adds.length <= 10^4, values within -10^4 and 10^4, and after every addition the collection holds at least k values.

**Example 1.** Input `k = 2`, `initial = [6, 1, 9]`, `adds = [4, 10, 7, 2]`, output `[6, 9, 9, 9]`.

**Example 2.** Input `k = 1`, `initial = []`, `adds = [3, 1, 5]`, output `[3, 3, 5]`.

**Hint.** Only the k best values can ever matter. Which of them is the weakest, and where in a heap does it sit?

**Changed decision.** The queue now holds a bounded number of items, and its root is read as an answer after every addition and not only at the end.
