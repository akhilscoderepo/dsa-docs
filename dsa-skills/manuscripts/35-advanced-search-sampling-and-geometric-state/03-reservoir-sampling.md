<!-- lesson-kind: standard -->
<!-- lesson-id: reservoir-sampling -->
## Reservoir Sampling

<!-- stage: context -->
### One Random Line From A Pipe

A support dashboard shows one random request from today's traffic so engineers can spot odd cases. The traffic arrives as a log stream, one line at a time, and nobody knows in advance how many lines will come. By the evening the stream holds a billion lines of about 100 bytes each. A first version collects every line into a list and then picks a random position. It works on a developer laptop. On the real stream it needs about 100 GB of memory and the process dies before the dashboard refreshes.

Two facts make the task hard. The program sees each line once and cannot go back, and it cannot hold the stream. Yet the line on display must be fair. A line from the first minute and a line from the last minute must have exactly the same chance of being chosen. The question of this lesson is whether a program can keep one line, or a handful, while still being fair at every moment the stream stops.

<!-- stage: naive -->
### Store Everything, Then Pick

The direct design appends each item to a list and picks a random position when asked. A source of randomness is passed in as a `LongUnaryOperator` called `pick`, so tests can script it. A call `pick.applyAsLong(b)` returns an integer from 0 to `b - 1`.

```java
final class StoreAllSampler {
    private final java.util.ArrayList<Integer> all = new java.util.ArrayList<>();
    private final java.util.function.LongUnaryOperator pick;

    StoreAllSampler(java.util.function.LongUnaryOperator pick) { this.pick = pick; }

    void add(int value) { all.add(value); }              // every item stays in memory

    int sample() {
        if (all.isEmpty()) throw new java.util.NoSuchElementException();
        return all.get((int) pick.applyAsLong(all.size()));   // fair, because every position is equally likely
    }
}
```

The class is fair and short. Its cost grows with the stream. A second idea keeps only one item and flips a coin for each new item: with probability one half the new item replaces the held one. That uses constant memory, so it deserves a test.

```predict
The coin rule runs on a stream of 4 items. Each new item replaces the held item with probability 1/2. What is the probability that the first item is the one held at the end? What is that probability for the last item? Is the rule fair?

The first item stays only if the three later coins all come up "keep", which has probability (1/2)^3 = 1/8. The last item is held if its own coin says "replace", which has probability 1/2. The probabilities for the four items are 1/8, 1/8, 1/4 and 1/2. They are not equal, so the rule is not fair.
```

<!-- stage: bottleneck -->
### Memory Grows, Coins Skew

The store-all design takes O(n) space for a stream of `n` items, and `n` has no upper limit. The sampling step costs O(1) time, so the bottleneck is memory alone. For a billion lines the list does not fit, and a stream that never ends has no moment at which it is allowed to be picked from.

The coin rule shows what a repair has to fix. A fair rule treats every item that has arrived the same way, and a fixed coin cannot. The first item is exposed to many coins, one for each later item. The last item faces only its own. The more items have arrived, the less likely each newer item should be to replace the held one, because there are more earlier items that also deserve their fair share.

A fix therefore needs a replacement chance that depends on how many items have arrived. The chance for the third item must differ from the chance for the thousandth. The program needs a counter, one held item, and a rule that makes every item equally likely whenever the stream stops. Memory of one item and one counter is O(1) and does not depend on `n`.

<!-- stage: insight -->
### Replace With Chance One Over t

<!-- names: reservoir, inclusion probability, replacement draw -->

#### The Rule For One Item

The **reservoir** is the small array that holds the current sample. For a sample of one item, the reservoir has one slot. The first item always enters. When item number `t` arrives, with `t` counting from 1, the program makes a **replacement draw**: it asks for an integer from 0 to `t - 1`, and it replaces the held item with the new one only when the result is 0. The chance of replacement is `1 / t`, so item 2 replaces with chance one half, item 3 with chance one third, and item 1000 with chance one in a thousand.

#### Why The Chances Come Out Equal

The **inclusion probability** of an item is the chance that it sits in the reservoir when the stream stops. The claim is that after `t` items every one of them has inclusion probability `1 / t`. The proof is by induction. After one item the claim holds, since the only item is held. Suppose it holds after `t - 1` items. Item `t` is held after its own draw with probability `1 / t`. An older item was held with probability `1 / (t - 1)`, and it stays when the new draw says "keep", which has probability `(t - 1) / t`. The product is `(1 / (t - 1)) * ((t - 1) / t) = 1 / t`. All `t` items now have the same inclusion probability.

#### A Reservoir Of k Items

For a sample of `k` items, the first `k` items fill the reservoir. When item `t` arrives with `t > k`, the replacement draw asks for an integer `j` from 0 to `t - 1`. If `j < k`, the new item overwrites slot `j`, and otherwise it is dropped. The new item enters with probability `k / t`. A specific held item is overwritten with probability `(k / t) * (1 / k) = 1 / t`. An older item with inclusion probability `k / (t - 1)` therefore keeps `k / (t - 1) * (1 - 1 / t) = k / t`. Every item has inclusion probability `k / t` after `t` items.

The invariant is that after every arrival, each item seen so far has inclusion probability `k / t`, and the reservoir stores at most `k` items.

<!-- stage: variables -->
### Counter, Slot And Draw Bound

The code for one item keeps three names, and the code for `k` items adds one.

- **seen** is the count `t` of items that have arrived, stored as a `long` because a stream can pass two billion items.
- **held** is the item currently in the reservoir. It changes only when the replacement draw returns 0.
- **pick** is the injected source of randomness. A call with bound `b` returns an integer from 0 to `b - 1`.
- **reservoir** is the array of at most `k` held items, used for the larger sample. Its slot `j` changes only when the draw `j` is below `k`.

The counter increases before the draw, so the draw bound is the new count. The first item makes no draw in the code, since its replacement chance is 1.

<!-- stage: trace -->
### Tracing Two Streams

#### A Sample Of One

The first trace feeds the stream `A B C D E` to the one-item rule with scripted draws. The pointer `t` marks the item that arrives. Item `A` enters without a draw. Item `B` draws from bound 2 and gets 1, so `A` stays. Item `C` draws from bound 3 and gets 0, so `C` replaces `A`. Item `D` draws from bound 4 and gets 2, so `C` stays. Item `E` draws from bound 5 and gets 0, so `E` replaces `C`. The final sample is `E`. The note of each step names the bound, the draw and the chance of replacement.

```trace
{"cells":["A","B","C","D","E"],"pointers":["t"],"steps":[{"at":{"t":0},"vars":{"bound":"none","draw":"none","held":"A"},"note":"Item A enters without a draw. The held item is A."},{"at":{"t":1},"vars":{"bound":2,"draw":1,"held":"A"},"note":"Bound 2, draw 1. The draw is not 0, so the held item stays."},{"at":{"t":2},"vars":{"bound":3,"draw":0,"held":"C"},"note":"Bound 3, draw 0. The draw is 0, so C replaces the held item."},{"at":{"t":3},"vars":{"bound":4,"draw":2,"held":"C"},"note":"Bound 4, draw 2. The draw is not 0, so the held item stays."},{"at":{"t":4},"vars":{"bound":5,"draw":0,"held":"E"},"note":"Bound 5, draw 0. The draw is 0, so E replaces the held item."}]}
```

#### A Sample Of Two

The second trace uses a reservoir of two slots on the stream `P Q R S T U`. The first two items fill slots 0 and 1. Item `R` draws from bound 3 and gets 2, which is not below 2, so `R` is dropped. Item `S` draws from bound 4 and gets 1, so `S` overwrites slot 1. Item `T` draws from bound 5 and gets 0, so `T` overwrites slot 0. Item `U` draws from bound 6 and gets 4, so `U` is dropped. The reservoir ends as `T S`.

```trace
{"cells":["P","Q","R","S","T","U"],"pointers":["t"],"steps":[{"at":{"t":0},"vars":{"bound":"none","draw":"none","reservoir":"P"},"note":"Item P fills slot 0 without a draw."},{"at":{"t":1},"vars":{"bound":"none","draw":"none","reservoir":"P Q"},"note":"Item Q fills slot 1 without a draw."},{"at":{"t":2},"vars":{"bound":3,"draw":2,"reservoir":"P Q"},"note":"Bound 3, draw 2. The draw is not below 2, so R is dropped."},{"at":{"t":3},"vars":{"bound":4,"draw":1,"reservoir":"P S"},"note":"Bound 4, draw 1. The draw is below 2, so S overwrites slot 1."},{"at":{"t":4},"vars":{"bound":5,"draw":0,"reservoir":"T S"},"note":"Bound 5, draw 0. The draw is below 2, so T overwrites slot 0."},{"at":{"t":5},"vars":{"bound":6,"draw":4,"reservoir":"T S"},"note":"Bound 6, draw 4. The draw is not below 2, so U is dropped."}]}
```

<!-- stage: code -->
### One Pass With Constant Memory

#### The Two Samplers

The first method keeps one item and a counter. The second method keeps an array of `k` slots. Both read the input once and never store more than `k` items.

```java
final class Reservoir {
    static int sampleOne(int[] stream, java.util.function.LongUnaryOperator pick) {
        if (stream.length == 0) throw new java.util.NoSuchElementException();
        int held = stream[0];                                  // item 1 always enters
        long seen = 1;
        for (int i = 1; i < stream.length; i++) {
            seen++;                                            // seen is now t
            if (pick.applyAsLong(seen) == 0) held = stream[i]; // replace with chance 1/t
        }
        return held;
    }

    static int[] sampleK(int[] stream, int k, java.util.function.LongUnaryOperator pick) {
        int[] reservoir = new int[Math.min(k, stream.length)];
        long seen = 0;
        for (int x : stream) {
            seen++;
            if (seen <= k) { reservoir[(int) seen - 1] = x; continue; }  // the first k items fill the slots
            long j = pick.applyAsLong(seen);                   // 0 to t - 1
            if (j < k) reservoir[(int) j] = x;                 // enters with chance k/t, into a uniform slot
        }
        return reservoir;
    }
}
```

#### Cost

- **sampleOne** costs O(n) time for one pass and O(1) space.
- **sampleK** costs O(n) time and O(k) space.
- **Randomness** is one draw per item after the first `k`.

<!-- stage: applicability -->
### When One Pass Sampling Applies

#### Recognizing The Pattern

Use this method when items arrive one at a time, the total is unknown or too large to store, and each item must have the same chance of selection. The words "uniformly at random", "stream" and "do not store" are the cue. Before coding, decide the sample size `k` and what counts as an item, because the counter must count only eligible items. The invariant to protect is that after `t` eligible items, each has inclusion probability `k / t`.

#### False Friends

Picking a random position from a list is a false friend when the list already exists in memory, because direct indexing is simpler and costs O(1) after the length is known. Shuffling the stream is a second false friend: it needs the whole stream. The coin rule with a fixed probability is a third, since its chances skew toward recent items. When the stream length is known at the start, drawing `k` distinct positions without replacement does the same job.

#### When The Method Does Not Apply

If items carry different weights, the chance `1 / t` is wrong and the next lessons give the right rule. If the sample must be re-drawn many times from the same data, storing the data and sampling by index is faster per query. If the source of randomness is not uniform, the proof above no longer holds.

<!-- stage: exercises -->
### Exercises

#### [Build] Sample One Item (Author exercise)
<!-- id: rs35-sample-one -->

**Prerequisites.** The replacement chance `1 / t` from this lesson.

**Problem.** Write `int sampleOne(int[] stream, LongUnaryOperator pick)`. The method reads `stream` from left to right once. Item 1 becomes the held item without any draw. For each later item number `t`, the method calls `pick.applyAsLong(t)` exactly once and replaces the held item with the new item when the result is 0. The method returns the held item after the last item. An empty stream throws `NoSuchElementException`.

**Constraints.** The limits are:
- **Length** of `stream` is from 0 to 10^6.
- **Values** are `int` values that may repeat.
- **Draws** use the bound `t`, and a result outside 0 to `t - 1` throws `IllegalStateException`.
- **Memory** is O(1) beyond the input.

**Example 1.** Input `stream = [5, 8, 3, 9]` with scripted draws `1, 0, 2` for the bounds 2, 3 and 4, output `3`.

**Example 2.** Input `stream = [7]`, no draw, output `7`.

**Hint.** What is the draw bound at the second item, and how many draws does a stream of `n` items cause?

**Changed decision.** Basic case: one slot, one counter, and the replacement chance changes with the count.

#### [Vary] Linked List Random Node (LeetCode 382)
<!-- id: rs35-linked-list-random-node -->

**Prerequisites.** The Sample One Item exercise above. This exercise changes the container: the items sit in a singly linked list whose length is unknown.

**Problem.** A node has an `int val` and a reference `next`. Write `int randomNode(ListNode head, LongUnaryOperator pick)`. The method walks the list once from `head` and returns the value of one node, chosen so that each node has the same probability. The method does not copy the list, does not count the nodes in a first pass, and uses the replacement rule of the previous exercise.

**Constraints.** The limits are:
- **Nodes** number from 1 to 10^4, and values are `int` values that may repeat.
- **Walks** are single: the list is read once and is not changed.
- **Draws** use the bound equal to the number of nodes read so far.
- **Memory** is O(1) beyond the list.

**Example 1.** Input list `1 -> 2 -> 3` with scripted draws `0, 0` for the bounds 2 and 3, output `3`.

**Example 2.** Input list `4 -> 5` with scripted draw `1` for the bound 2, output `4`.

**Hint.** Which variable plays the role of the array index in the previous exercise?

**Changed decision.** The input is a linked list, so the length is never known and the counter replaces the index.

#### [Boundary] First K Items And Short Stream (Author exercise)
<!-- id: rs35-first-k-short-stream -->

**Prerequisites.** The Linked List Random Node exercise above. This exercise grows the sample from one item to `k` items.

**Problem.** Write `int[] sampleK(int[] stream, int k, LongUnaryOperator pick)`. The first `min(k, n)` items fill slots 0 onward in arrival order. For each item `t` with `t > k`, the method calls `pick.applyAsLong(t)` once. If the result `j` is below `k`, the method stores the new item in slot `j`. The method returns the slots as an array whose length is `min(k, n)`.

**Constraints.** The limits are:
- **Length** `n` of `stream` is from 0 to 10^5.
- **Sample size** `k` is from 1 to 10^5, and `k` may exceed `n`.
- **Draws** happen only for items with `t > k`, with the bound `t`.
- **Result** is a new array, and an empty stream returns an empty array.

**Example 1.** Input `stream = [10, 20, 30, 40, 50]`, `k = 2`, scripted draws `0, 3, 1` for the bounds 3, 4 and 5, output `[30, 50]`.

**Example 2.** Input `stream = [9, 8]`, `k = 5`, no draws, output `[9, 8]`.

**Hint.** What should the result contain when the stream ends before the reservoir is full?

**Changed decision.** The reservoir holds `k` items, and the code must handle the fill phase and a stream shorter than `k`.

#### [Recognize] Random Pick Index (LeetCode 398)
<!-- id: rs35-random-pick-index -->

**Prerequisites.** The First K Items And Short Stream exercise above. This exercise hides the stream inside an array and filters it by a target value.

**Problem.** Write `int pickIndex(int[] nums, int target, LongUnaryOperator pick)`. The method returns an index `i` with `nums[i] == target`, chosen so that every such index has the same probability. The array may contain `target` several times, and it contains it at least once. The method stores no list of indices. Whenever it meets the `m`-th matching position, it calls `pick.applyAsLong(m)` once and keeps the new index only when the result is 0. The first matching position needs no draw.

**Constraints.** The limits are:
- **Length** of `nums` is from 1 to 2 * 10^4, and values are `int` values.
- **Target** occurs at least once in `nums`.
- **Draw bound** equals the count of matches so far, not the position in the array.
- **Memory** is O(1) beyond the input.

**Example 1.** Input `nums = [1, 2, 3, 3, 3]`, `target = 3`, scripted draws `1, 0` for the bounds 2 and 3, output `4`.

**Example 2.** Input `nums = [5, 5]`, `target = 5`, scripted draw `0` for the bound 2, output `1`.

**Hint.** What count should the replacement chance use when only some positions are eligible?

**Changed decision.** Only matching positions count as items, so the counter increments on matches and not on every position.
