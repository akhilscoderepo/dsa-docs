<!-- lesson-kind: standard -->
<!-- lesson-id: lazy-deletion -->
## Delete From A Heap Lazily

<!-- stage: context -->
### Why Each Ticket Edit Takes Longer

A support tool keeps open tickets in a `PriorityQueue` ordered by urgency. Agents can raise or lower the urgency of a ticket. The first version handles an edit by removing the old ticket from the queue and adding it again with the new urgency. With 1,000 tickets the edits feel instant. With 100,000 tickets, each edit takes visibly longer than the previous batch, and a script that edits every ticket once runs for minutes.

The queue is fast for taking the smallest item, yet removing an arbitrary item is slow. This lesson asks how a program can change or delete items in a queue without paying for the removal at the time of the change.

<!-- stage: naive -->
### Removing The Old Ticket Immediately

The direct plan calls `remove(Object)` on the queue and then offers the new version.

```java
final class EagerBoard {
    record Ticket(int id, int urgency) {}

    private final PriorityQueue<Ticket> queue = new PriorityQueue<>(
        Comparator.comparingInt(Ticket::urgency).thenComparingInt(Ticket::id));
    private final Map<Integer, Ticket> current = new HashMap<>();

    void set(int id, int urgency) {
        Ticket old = current.get(id);
        if (old != null) queue.remove(old);          // finds the old ticket by scanning the array
        Ticket fresh = new Ticket(id, urgency);
        current.put(id, fresh);
        queue.offer(fresh);
    }

    Integer pollMostUrgent() {
        Ticket top = queue.poll();
        if (top == null) return null;
        current.remove(top.id());
        return top.id();
    }
}
```

The board is correct. Every edit of an existing ticket pays for the call to `remove(Object)`.

<!-- stage: bottleneck -->
### Measuring The Cost Of Each Edit

```predict
The queue holds n = 100,000 tickets, and the script edits every ticket once. How many items does remove(Object) examine over the whole script?

Each remove scans the array until it finds the item, so one call examines up to n items. The script makes n edits, which gives about n * n / 2 = 5 * 10^9 examinations, or O(n^2).
```

`PriorityQueue.remove(Object)` searches the array from the front with `equals` and then repairs the heap. The search costs O(n), and only the repair costs O(log n). The method looks cheap in code, because it is one call, yet it hides a linear scan. The same holds for `contains`.

Most of those removals are wasted. A ticket that was edited often will leave the queue by being polled long before the program needs its old entry gone. The program only needs to make sure that nobody ever acts on the old entry. It does not need to find the old entry at all.

<!-- stage: insight -->
### Marking Entries Instead Of Deleting Them

A **stale entry** is a queue entry that no longer describes the current state, for example an old version of an edited ticket. The program leaves stale entries inside the queue and skips them when they reach the root.

#### Recognizing Stale Entries By Version

Each `set` call creates a new entry with a **version number** from a global counter. The program stores the newest version of each ticket in a map. An entry is stale when its version differs from the map entry for its ticket, or when the map has no entry. The old entry stays in the array and costs nothing at edit time.

#### Recognizing Stale Entries By Count

When the program deletes a value, it adds one to a **deletion count** for that value in a map. A root whose value has a positive count is stale. The program polls it and subtracts one from the count. Equal values work, because each count removes exactly one copy.

#### Cleaning Before Every Read

Before `peek` or `poll`, the program runs a loop. While the root is stale, it polls the root and discards it. The loop ends at a live root or an empty queue. Each entry is inserted once and discarded at most once. The cleaning costs O(log n) per entry, so n entries cost O(n log n) in total.

<!-- names: stale entry, version number, deletion count -->

<!-- stage: variables -->
### What The Board Keeps

The lazy board stores the same entries as before and adds the state that identifies the stale ones.

- **Queue** holds every entry ever inserted that has not yet been polled, including stale ones.
- **Latest map** stores the newest version number of each ticket, and it has no entry for a ticket that left.
- **Version counter** increases by one for every new entry, so no two entries share a version.
- **Live size** counts the tickets that still exist, and it differs from the queue size while stale entries remain.

Only the live size answers questions about how many tickets exist. The queue size answers questions about memory.

<!-- stage: trace -->
### Following Stale Entries Through A Queue

#### Editing A Ticket Without Removal

Run the operations `set(A, 5)`, `set(B, 3)`, `set(A, 1)`, `poll`, `set(C, 2)`, `poll`, `poll` and `poll`. In the first trace the cells hold the four urgency values in the order of the `set` calls. The pointer `sets` marks how many `set` calls have run.

The call `set(A, 1)` adds a second entry for A and leaves the entry with urgency 5 inside the queue. The first poll returns A, because the root has urgency 1. The poll for C returns C with urgency 2, and the next poll returns B. The last poll finds the old A entry with urgency 5 at the root, sees that A has left, discards it and returns nothing.

#### Skipping Equal Values With Counts

The second trace adds the values 4, 2, 4, 7 and 4 and then deletes 4 twice. The queue still holds three entries with the value 4. The first poll returns 2. The second poll finds a 4 with count 2 at the root, discards it and lowers the count to 1. It discards a second 4 and lowers the count to 0, and then it returns the third 4.

#### Stepping Through Both Runs

```trace
{"cells":[5,3,1,2],"pointers":["sets"],"steps":[{"at":{"sets":1},"vars":{"queue entries":1,"live tasks":1},"note":"The call set(0, 5) adds the entry with version 1. The queue holds 1 entries, and 1 tasks are live."},{"at":{"sets":2},"vars":{"queue entries":2,"live tasks":2},"note":"The call set(1, 3) adds the entry with version 2. The queue holds 2 entries, and 2 tasks are live."},{"at":{"sets":3},"vars":{"queue entries":3,"live tasks":2},"note":"The call set(0, 1) adds the entry with version 3. The queue holds 3 entries, and 2 tasks are live."},{"at":{"sets":3},"vars":{"queue entries":2,"live tasks":1},"note":"The root is live, so the poll returns 0."},{"at":{"sets":4},"vars":{"queue entries":3,"live tasks":2},"note":"The call set(2, 2) adds the entry with version 4. The queue holds 3 entries, and 2 tasks are live."},{"at":{"sets":4},"vars":{"queue entries":2,"live tasks":1},"note":"The root is live, so the poll returns 2."},{"at":{"sets":4},"vars":{"queue entries":1,"live tasks":0},"note":"The root is live, so the poll returns 1."},{"at":{"sets":4},"vars":{"queue entries":0,"live tasks":0},"note":"The root is the old entry with urgency 5 for 0, and its version is out of date. It leaves the queue. The poll returns nothing."}]}
```

```trace
{"cells":[4,2,4,7,4],"pointers":["next"],"steps":[{"at":{"next":0},"vars":{"queue entries":1,"pending":"{}"},"note":"The value 4 enters the queue, which now holds 1 entries."},{"at":{"next":1},"vars":{"queue entries":2,"pending":"{}"},"note":"The value 2 enters the queue, which now holds 2 entries."},{"at":{"next":2},"vars":{"queue entries":3,"pending":"{}"},"note":"The value 4 enters the queue, which now holds 3 entries."},{"at":{"next":3},"vars":{"queue entries":4,"pending":"{}"},"note":"The value 7 enters the queue, which now holds 4 entries."},{"at":{"next":4},"vars":{"queue entries":5,"pending":"{}"},"note":"The value 4 enters the queue, which now holds 5 entries."},{"at":{"next":5},"vars":{"queue entries":5,"pending":"{4: 2}"},"note":"The program deletes 4 twice. It records the count 2 and leaves the queue unchanged."},{"at":{"next":5},"vars":{"queue entries":4,"pending":"{4: 2}"},"note":"The poll discards 0 stale root(s) and returns 2."},{"at":{"next":5},"vars":{"queue entries":1,"pending":"{}"},"note":"The poll discards 2 stale root(s) and returns 4."}]}
```

<!-- stage: code -->
### Writing Lazy Boards In Java

#### Versions For Edited Entries

The class stores `{id, urgency, version}` triples and checks the version at the root.

```java
final class LazyBoard {
    private final PriorityQueue<int[]> queue = new PriorityQueue<>((a, b) ->
        a[1] != b[1] ? Integer.compare(a[1], b[1]) : Integer.compare(a[0], b[0]));
    private final Map<Integer, Integer> latest = new HashMap<>();   // id to newest version
    private int version = 0;

    void set(int id, int urgency) {
        version++;                                                   // a global counter never repeats a version
        latest.put(id, version);
        queue.offer(new int[] {id, urgency, version});               // the old entry stays in the queue
    }

    private void dropStale() {
        while (!queue.isEmpty()) {
            int[] top = queue.peek();
            Integer v = latest.get(top[0]);
            if (v != null && v == top[2]) return;                    // a live root ends the cleaning
            queue.poll();                                            // a stale root leaves the queue
        }
    }

    Integer pollMostUrgent() {
        dropStale();
        if (queue.isEmpty()) return null;
        int id = queue.poll()[0];
        latest.remove(id);                                           // any older entry of this id is now stale
        return id;
    }

    int size() { return latest.size(); }                             // live size, not the queue size
}
```

#### Counts For Equal Values

The class stores plain values and a map of pending deletions.

```java
final class LazyValues {
    private final PriorityQueue<Integer> queue = new PriorityQueue<>();
    private final Map<Integer, Integer> pending = new HashMap<>();   // value to number of deleted copies
    private int live = 0;

    void add(int v) { queue.offer(v); live++; }

    void remove(int v) { pending.merge(v, 1, Integer::sum); live--; } // the caller guarantees v is present

    Integer min() {
        while (!queue.isEmpty()) {
            Integer c = pending.get(queue.peek());
            if (c == null) break;                                    // no pending deletion, so the root is live
            int top = queue.poll();
            if (c == 1) pending.remove(top); else pending.put(top, c - 1);
        }
        return queue.peek();
    }

    Integer poll() {
        Integer m = min();                                           // cleans first, so m is live
        if (m != null) { queue.poll(); live--; }
        return m;
    }

    int size() { return live; }
}
```

Both classes cost O(log n) per call, amortized over the entries they discard.

<!-- stage: applicability -->
### Recognizing A Delayed Deletion Question

#### Spotting The Pattern

The cue is a queue where items change, expire or get deleted, while the program still needs the best live item. The invariant is that, before the program reads the root, it discards every entry whose version, count or eligibility no longer matches the companion state. After that loop, the root is live.

#### Finding The False Friend

The false friend is `PriorityQueue.remove(Object)`, together with `contains`. Each of them walks the array with `equals`, so the cost grows linearly with the queue size. The call looks like one logarithmic step in code, and only a profiler shows the true cost.

A second false friend is the queue size. With stale entries inside, `queue.size()` over-counts the live items, so any rule that depends on the number of live items must use its own counter.

#### Recognizing The No-Go Cases

The counting form assumes that every deleted value is present. Deleting a value that never entered leaves a pending count that later removes an unrelated copy. If many entries go stale, memory grows with the number of edits and not with the number of live items. A design with a position map or a sorted structure then fits better.

<!-- stage: exercises -->
### Exercises

#### [Build] Versioned Priorities (Author exercise)
<!-- id: hp-versioned-priorities -->

**Prerequisites.** The version map and the cleaning loop of this lesson.

**Problem.** Design a class `TaskBoard` with a method `void set(int id, int priority)` and a method `int poll()`. The call `set` inserts task `id` or replaces its priority. The call `poll` removes and returns the id of the task with the smallest priority, and a tie goes to the smaller id. It returns -1 when no task exists. A task that was polled no longer exists until a new `set` adds it.

**Constraints.** The limits are:
- **Calls** number at most `10^5`.
- **Ids** satisfy `0 <= id <= 10^9`, and priorities are `int` values.
- **Return** is -1 when the board is empty.

**Example 1.** Input `set(1,5)`, `set(2,3)`, `set(1,1)`, `poll()`, `poll()`, `poll()`, output `1, 2, -1`.

**Example 2.** Input `set(7,2)`, `set(7,9)`, `set(8,5)`, `poll()`, `poll()`, output `8, 7`.

**Hint.** Which entry of task 7 does the first `poll` meet at the root in the second example? What tells the program that an entry is out of date?

**Changed decision.** An edit inserts a new entry and records its version, and the old entry stays in the queue.

#### [Vary] Delayed Removal Counts (Author exercise)
<!-- id: hp-delayed-removal-counts -->

**Prerequisites.** The previous exercise and the count map in the code stage.

**Problem.** Design a class `ValueBag` with methods `void add(int v)`, `void remove(int v)` and `Integer min()`. The call `remove` deletes one copy of `v` and is called only when at least one copy exists. The call `min` returns the smallest value that is still present, or `null` when the bag is empty. Do not call `PriorityQueue.remove`.

**Constraints.** The limits are:
- **Calls** number at most `10^5`.
- **Values** are `int` values, and duplicates are allowed.
- **Remove** is called only for a value that is present.

**Example 1.** Input `add(4)`, `add(2)`, `add(4)`, `remove(2)`, `min()`, `remove(4)`, `min()`, `remove(4)`, `min()`, output `4, 4, null`.

**Example 2.** Input `add(3)`, `add(1)`, `remove(1)`, `min()`, output `3`.

**Hint.** What does the program record at `remove` time? Where does it look at that record?

**Changed decision.** The record is a count of deleted copies for each value, and the root check happens at `min` time.

#### [Boundary] Several Stale Roots (Author exercise)
<!-- id: hp-several-stale-roots -->

**Prerequisites.** The two exercises above.

**Problem.** Given an array `adds` of values added to a bag, and an array `removes` of values deleted afterward, return the smallest remaining value. Return `null` when none remains. Every value in `removes` has a copy that is still present when its turn comes. Clean the root in a loop, because several stale entries can sit at the root in a row, and equal values can have several outstanding deletions.

**Constraints.** The limits are:
- **Lengths** satisfy `0 <= adds.length <= 10^5` and `0 <= removes.length <= adds.length`.
- **Values** are `int` values, and duplicates are allowed.
- **Validity** means that each removal matches a present copy.

**Example 1.** Input `adds = [5,5,5,5,9]` and `removes = [5,5,5]`, output 5.

**Example 2.** Input `adds = [2,2,2,9]` and `removes = [2,2,2]`, output 9.

**Hint.** What happens if the cleaning code uses an `if` where a `while` is needed? How many copies of the root value does a count of 3 discard?

**Changed decision.** The cleaning step repeats until the root is live.

#### [Recognize] Sliding Window Median (LeetCode 480)
<!-- id: hp-sliding-window-median -->

**Prerequisites.** All three exercises above.

**Problem.** Given an array `nums` and a window size `k`, return the maximum of each window of `k` consecutive values, from left to right. Use one queue ordered by value, largest first, and discard expired entries only when they reach the root. The median version of this window question needs the two halves taught in the next lesson, so this version asks for the maximum.

**Constraints.** The limits are:
- **Length** is `1 <= nums.length <= 10^5`.
- **Window** satisfies `1 <= k <= nums.length`.
- **Values** are `int` values, and duplicates are allowed.
- **Answer** has `nums.length - k + 1` values.

**Example 1.** Input `nums = [4,2,12,3,8,1]` and `k = 3`, output `[12,12,12,8]`.

**Example 2.** Input `nums = [5]` and `k = 1`, output `[5]`.

**Hint.** What does the program store next to each value so that it can tell when the entry has left the window? When does the program check that?

**Changed decision.** An entry is stale when its position falls before the window start, and the check happens only at the root.
