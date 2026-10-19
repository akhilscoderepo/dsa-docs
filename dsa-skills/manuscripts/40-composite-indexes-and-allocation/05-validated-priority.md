<!-- lesson-kind: standard -->
<!-- lesson-id: validated-priority -->
## Validated Priority

<!-- stage: context -->
### Raising The Priority Of A Queued Job

A job scheduler keeps waiting jobs in a priority queue and always starts the job with the highest priority. Users can raise or lower the priority of a job that is still waiting. During a busy hour, the scheduler holds 100,000 waiting jobs and receives thousands of priority changes per second. The developer implements a change as "remove the job from the queue, then add it back with the new priority". Throughput collapses, and a profile shows that almost all the time goes into the removal step.

A priority queue answers "who is first?" very well. It answers "where is this job?" badly. The same pattern appears in task managers, auction pages, timers that can be rescheduled and shortest-path searches whose distances improve.

This lesson asks how to change priorities without ever searching the queue, and how to make sure that an outdated queue entry never decides an answer.

<!-- stage: naive -->
### Remove And Re-Add On Every Change

The direct design uses `java.util.PriorityQueue` and a change call that removes the old object before it adds the new one.

```java
final class NaiveScheduler {
    record Job(int priority, int id) {}
    private final java.util.PriorityQueue<Job> queue = new java.util.PriorityQueue<>(
            (a, b) -> a.priority() != b.priority() ? Integer.compare(b.priority(), a.priority()) : Integer.compare(a.id(), b.id()));
    private final java.util.Map<Integer, Job> jobOf = new java.util.HashMap<>();

    void set(int id, int priority) {
        Job old = jobOf.get(id);
        if (old != null) queue.remove(old);                  // linear search through the heap array
        Job now = new Job(priority, id);
        jobOf.put(id, now);
        queue.add(now);
    }

    int poll() {
        Job top = queue.poll();
        if (top == null) return -1;
        jobOf.remove(top.id());
        return top.id();
    }
}
```

The class gives correct answers. A set call costs O(n) when the job already exists, and a poll costs O(log n).

```predict
A heap holds 100,000 jobs, and the scheduler changes the priority of one job. How many entries can the removal step compare before it finds the job, and what could the scheduler do instead of removing it?

The heap array has no order that helps a search, so the removal can compare all 100,000 entries. The scheduler could leave the old entry in the heap and add a second entry with the new priority. It then has to recognize and ignore the old entry when that entry reaches the top.
```

<!-- stage: bottleneck -->
### The Search Inside The Heap

A heap keeps only one promise: the top entry is the best. The other entries sit in an order that supports sift operations and nothing else. `PriorityQueue.remove(Object)` therefore scans the array, which costs O(n) per priority change.

Skipping the removal looks cheap. The scheduler adds the new entry and leaves the old one in place, so a change costs O(log n). The old entry now competes for the top. Suppose a job had priority 5 and later received priority 1. The old entry with priority 5 reaches the top, the scheduler starts the job early, and the answer is wrong.

The queue needs a way to tell an old entry from a current one in O(1) time, using information that lives outside the heap.

<!-- stage: insight -->
### Trust The Record, Not The Queue

The map from job id to its current priority is the **authoritative record**. The heap is only a list of candidates. A candidate describes what the record said at the time of the call that created it.

#### Telling Candidates Apart

Each call that creates a candidate also tags it with a **version**, which is a counter value that grows with every call. The record stores the version of the newest candidate for each job. A candidate is current only when its version equals the stored version. Comparing priorities is not enough, because a job can be cancelled and added again with the same priority, and the old candidate would look correct while it is not.

#### Discarding At The Top

A candidate that fails the check is a **stale entry**. The class never searches for stale entries. It drops one only when it reaches the top, at the moment the answer depends on it. The top is checked in a loop: poll a candidate, compare its version with the record, and keep it only if the versions match. Each stale entry is dropped once, so the total drop work is bounded by the number of entries ever added.

The invariant is that every live job has exactly one current candidate in the heap, and a candidate leaves the loop only if it matches the record.

<!-- names: authoritative record, version, stale entry -->

<!-- stage: variables -->
### Record Fields And Heap Fields

The scheduler keeps a record map, a heap and a counter.

- **current** maps each live job id to its priority and its newest version, and a set call overwrites that entry.
- **heap** holds entries of priority, id and version, and a set call adds one entry without removing any.
- **clock** is the counter that hands out the next version, and it only grows.

A cancel call removes the job from `current` and leaves its heap entries in place. Those entries fail the version check later, because the job is missing from the record.

<!-- stage: trace -->
### Following Entries Through The Heap

#### A Job That Changes Priority

The first trace starts with two jobs and raises the priority of job 1 before the first poll. In each step the pointer `call` marks the call just run. The heap column lists entries as `priority:id@version` in pop order.

```trace
{"cells":["set(1,5)","set(2,9)","set(1,12)","poll()","poll()","poll()"],"pointers":["call"],"steps":[{"at":{"call":0},"vars":{"heap":"5:1@1","result":"null"},"note":"Call 0: the record for job 1 becomes priority 5 with version 1, and the heap gains an entry. Older entries for job 1 stay in the heap."},{"at":{"call":1},"vars":{"heap":"9:2@2 5:1@1","result":"null"},"note":"Call 1: the record for job 2 becomes priority 9 with version 2, and the heap gains an entry. Older entries for job 2 stay in the heap."},{"at":{"call":2},"vars":{"heap":"12:1@3 9:2@2 5:1@1","result":"null"},"note":"Call 2: the record for job 1 becomes priority 12 with version 3, and the heap gains an entry. Older entries for job 1 stay in the heap."},{"at":{"call":3},"vars":{"heap":"9:2@2 5:1@1","result":"1"},"note":"Call 3: entry 12:1@3 matches the record, so poll returns job 1."},{"at":{"call":4},"vars":{"heap":"5:1@1","result":"2"},"note":"Call 4: entry 9:2@2 matches the record, so poll returns job 2."},{"at":{"call":5},"vars":{"heap":"empty","result":"-1"},"note":"Call 5: entry 5:1@1 fails the version check, so poll drops it; then the heap is empty, so poll returns -1."}]}
```

The first poll pops the entry `12:1@3`, which matches the record, and returns job 1. The second poll pops `9:2@2`. The entry `5:1@1` reaches the top only in the last poll, and the record no longer holds job 1, so the scheduler drops it.

#### A Job That Returns With The Same Priority

The second trace cancels a job and adds it again with the same priority.

```trace
{"cells":["set(3,7)","cancel(3)","set(3,7)","poll()","poll()"],"pointers":["call"],"steps":[{"at":{"call":0},"vars":{"heap":"7:3@1","result":"null"},"note":"Call 0: the record for job 3 becomes priority 7 with version 1, and the heap gains an entry. Older entries for job 3 stay in the heap."},{"at":{"call":1},"vars":{"heap":"7:3@1","result":"null"},"note":"Call 1: job 3 leaves the record. Its heap entries stay and now fail the version check."},{"at":{"call":2},"vars":{"heap":"7:3@1 7:3@2","result":"null"},"note":"Call 2: the record for job 3 becomes priority 7 with version 2, and the heap gains an entry. Older entries for job 3 stay in the heap."},{"at":{"call":3},"vars":{"heap":"empty","result":"3"},"note":"Call 3: entry 7:3@1 fails the version check, so poll drops it; then entry 7:3@2 matches the record, so poll returns job 3."},{"at":{"call":4},"vars":{"heap":"empty","result":"-1"},"note":"Call 4: the heap is empty, so poll returns -1."}]}
```

Both entries for job 3 show priority 7. The first one has version 1, and the record holds version 3. The version check separates them, and a priority check would not.

<!-- stage: code -->
### A Job Queue With Version Checks

The class stores the record in a map and the candidates in a heap.

```java
final class JobQueue {
    private record Entry(int priority, int id, int version) {}
    private final java.util.PriorityQueue<Entry> heap = new java.util.PriorityQueue<>((a, b) ->
            a.priority() != b.priority() ? Integer.compare(b.priority(), a.priority()) : Integer.compare(a.id(), b.id()));
    private final java.util.Map<Integer, int[]> current = new java.util.HashMap<>();   // id -> {priority, version}
    private int clock = 0;

    void set(int id, int priority) {
        int v = ++clock;
        current.put(id, new int[] {priority, v});            // the record changes first
        heap.add(new Entry(priority, id, v));                // the old entry stays in the heap
    }

    void cancel(int id) { current.remove(id); }

    int poll() {
        while (!heap.isEmpty()) {
            Entry e = heap.poll();
            int[] cur = current.get(e.id());
            if (cur != null && cur[1] == e.version()) {      // only the newest entry of a live job passes
                current.remove(e.id());
                return e.id();
            }
        }
        return -1;
    }
}
```

A set call costs O(log n). A poll call costs O(log n) per entry it drops and per entry it returns. Each entry is dropped at most once, so the cost of dropping is O(log n) amortized per set call. The space is O(total set calls) until the heap is rebuilt.

<!-- stage: applicability -->
### When Stale Entries Are Cheaper Than Removal

#### Checking The Conditions

Use versioned candidates when callers change or cancel items far more often than they ask for the best item, and when the heap offers no handle to an arbitrary entry. The invariant is that the record decides, and a heap entry is exposed only if it still matches the record.

#### Memory And Rebuilding

Stale entries accumulate in the heap between polls. If the workload makes millions of changes and few polls, the heap grows far beyond the number of live jobs. A rebuild fixes this. When the heap size exceeds about twice the live count, copy the current entries into a new heap and drop the rest.

#### False Friends

A sorted set with an exact removal is a false friend of this design when the entries are small and immutable. It supports removal in O(log n), and it needs no versions, so it is the simpler choice. A second false friend is a priority change that only ever raises a priority in a minimum heap, as in shortest paths, where a duplicate entry is harmless and a plain distance check is enough. Skip versions when the heap must also answer "what is the k-th best" for large `k`, because stale entries distort that answer.

<!-- stage: exercises -->
### Exercises

#### [Build] Versioned Heap Entry (Author exercise)
<!-- id: ci40-versioned-heap -->

**Prerequisites.** Priority queues and the multi-index lesson.

**Problem.** Design a class `JobBoard`. The call `set(id, priority)` adds a job with a new id or changes the priority of an existing job. The call `cancel(id)` deletes a live job. The call `poll()` removes the live job with the highest priority and returns its id, or returns -1 if no job is live. Equal priorities go to the smaller id. The call `size()` returns the number of live jobs.

**Constraints.** The limits are:
- **Ids** are integers from 1 to 10^5.
- **Priorities** satisfy `0 <= priority <= 10^9`.
- **Calls** number at most `2 * 10^5`, and `cancel` names a live job.
- **Return** of `poll` and `size` is an `int`.

**Example 1.** Input calls `set(1,5)`, `set(2,9)`, `set(1,12)`, `poll()`, `poll()`, `poll()`, output 1, 2 and -1.

**Example 2.** Input calls `set(4,3)`, `cancel(4)`, `size()`, `poll()`, output 0 and -1.

**Hint.** Which value tells a heap entry that a newer entry for the same job exists?

**Changed decision.** A change adds an entry instead of removing one, so the check moves from the update to the poll.

#### [Vary] Design Movie Rental System (LeetCode 1912)
<!-- id: ci40-rental-report -->

**Prerequisites.** The versioned heap exercise above.

**Problem.** A chain has shops that each own at most one copy of a movie at a fixed price. Design a class `RentalReport` built from entries `{shop, movie, price}`, with all copies unrented. The call `rent(shop, movie)` marks a copy rented. The call `drop(shop, movie)` marks it unrented. The call `report()` lists the 5 cheapest rented copies as `{shop, movie}`, or all of them when fewer exist, with ties broken by shop and then movie. A copy may be rented, dropped and rented again.

**Constraints.** The limits are:
- **Entries** number at most `10^5`, each `{shop, movie}` pair appears once, and prices are `int` values from 1 to 10^4.
- **Calls** number at most `10^5`.
- **Rent** names an unrented copy, and **drop** names a rented copy.
- **Report** must not list a copy twice.

**Example 1.** Input entries `{0,1,5}`, `{0,2,6}`, `{1,1,4}` and calls `rent(0,1)`, `rent(1,1)`, `report()`, output `{1,1}` and `{0,1}`.

**Example 2.** Input the same entries and calls `rent(1,1)`, `drop(1,1)`, `rent(1,1)`, `rent(0,2)`, `report()`, output `{1,1}` and `{0,2}`.

**Hint.** What does the heap hold for a copy that was rented twice, and how does the report avoid listing it twice?

**Changed decision.** The report reads five entries and puts the valid ones back, so a version check runs on every popped entry.

#### [Boundary] Repeated Corrections (Author exercise)
<!-- id: ci40-repeated-corrections -->

**Prerequisites.** The two exercises above.

**Problem.** Design a class `Desk` with the calls `set(id, priority)`, `cancel(id)`, `poll()` and `size()` of the versioned heap exercise, and a call `peek()`. The call `peek()` returns the id that `poll()` would return, but removes nothing. Calling `peek()` any number of times must not change any later answer. Equal priorities go to the smaller id.

**Constraints.** The limits are:
- **Ids** are integers from 1 to 10^5, and priorities satisfy `0 <= priority <= 10^9`.
- **Calls** number at most `2 * 10^5`, and one id may receive thousands of `set` calls.
- **Cancel** names a live job.
- **Return** of `peek` and `poll` is -1 when no job is live.

**Example 1.** Input calls `set(1,5)`, `set(1,9)`, `set(1,5)`, `peek()`, `poll()`, `peek()`, output 1, 1 and -1.

**Example 2.** Input calls `set(2,4)`, `set(3,4)`, `cancel(2)`, `set(2,4)`, `peek()`, `poll()`, `poll()`, output 2, 2 and 3.

**Hint.** May a peek call discard a stale entry, and may it discard a live one?

**Changed decision.** A read-only call may drop stale entries but never a live entry, and repeated corrections must not change any answer.

#### [Recognize] Design Auction System (LeetCode 3815)
<!-- id: ci40-auction -->

**Prerequisites.** All three exercises above.

**Problem.** The contract here is the chapter's own and can differ in detail from LeetCode. Design a class `Auction`. The call `addBid(userId, itemId, amount)` records a bid, and a new bid by the same user on the same item replaces that user's earlier bid. The call `removeBid(userId, itemId)` withdraws the user's current bid on the item. The call `getHighestBidder(itemId)` returns the user with the highest current bid on the item, breaking ties by the larger user id, or -1 if the item has no bid.

**Constraints.** The limits are:
- **Users** and **items** are integers from 1 to 10^5.
- **Amounts** satisfy `1 <= amount <= 10^9`.
- **Calls** number at most `2 * 10^5`, and `removeBid` names a user with a current bid on that item.
- **Return** of `getHighestBidder` is an `int`.

**Example 1.** Input calls `addBid(1,10,50)`, `addBid(2,10,70)`, `addBid(1,10,80)`, `getHighestBidder(10)`, output 1.

**Example 2.** Input calls `addBid(1,10,50)`, `addBid(2,10,50)`, `getHighestBidder(10)`, `removeBid(2,10)`, `getHighestBidder(10)`, output 2 and then 1.

**Hint.** Which key identifies one bid in the record, and how many heaps does the system need?

**Changed decision.** The record is keyed by user and item, and each item owns its own heap of candidates.
