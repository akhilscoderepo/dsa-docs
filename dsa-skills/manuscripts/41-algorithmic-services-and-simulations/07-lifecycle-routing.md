<!-- lesson-kind: standard -->
<!-- lesson-id: lifecycle-routing -->
## Track Status And Pick The Next Task

<!-- stage: context -->
### A Cancelled Job That Still Runs

A job runner accepts print jobs with a priority. A user cancels job 7 because the file was wrong. A minute later the printer starts job 7 anyway, because it was the highest priority job in the line and nobody told the line that it was cancelled. The paper is wasted, and the user sees the cancel screen say "done".

The opposite failure is just as common. A job finishes, but the line still lists it, so the next pick returns the same job twice. Both failures come from one cause. The program keeps two views of the same jobs, one that says what happened to each job and one that says which job is next, and the two views disagree.

This lesson asks how to keep the answer to "which job is next" correct while jobs are added, cancelled, finished and changed, and how to keep each call fast.

<!-- stage: naive -->
### Scanning Every Job On Every Pick

The direct design stores every job in one list with a flag for its state. A pick walks the whole list, skips jobs that are not waiting, and keeps the best one by priority, with the smaller id winning a tie.

```java
final class NaiveRunner {
    private static final class Job {
        final int id; final int priority; String state = "PENDING";
        Job(int id, int priority) { this.id = id; this.priority = priority; }
    }
    private final java.util.ArrayList<Job> jobs = new java.util.ArrayList<>();

    boolean add(int id, int priority) {
        for (Job j : jobs) if (j.id == id) return false;       // duplicate check scans every job
        jobs.add(new Job(id, priority));
        return true;
    }

    int next() {
        Job best = null;
        for (Job j : jobs) {                                    // visits finished and cancelled jobs too
            if (!j.state.equals("PENDING")) continue;
            if (best == null || j.priority > best.priority
                    || (j.priority == best.priority && j.id < best.id)) best = j;   // the smaller id wins a tie
        }
        return best == null ? -1 : best.id;
    }
}
```

The answers are right. The flag is the only record of what happened to a job, so a cancelled job can never be picked.

```predict
The runner holds n jobs. A loop calls next() and then marks the job it returned as done, until no job is waiting. About how many job visits do the next() calls make in total?

Each next() visits every stored job, because finished jobs stay in the list. There are n calls and each visits n jobs, so the total is about n squared visits. For n equal to 100000 that is ten billion visits.
```

<!-- stage: bottleneck -->
### Visiting Jobs That Cannot Win

The cost of one pick is O(n) for n stored jobs. The add call is also O(n) because of the duplicate check. A sequence of n calls therefore costs O(n^2), which is too slow for 10^5 calls.

Most visits are wasted. A job that is done or cancelled can never be the answer again, yet every later pick still reads it. The list grows with every job ever added, so the work per pick grows even when only a few jobs are waiting.

A structure ordered by priority would find the best job without a scan. That structure brings back the failure from the opening: it holds jobs, and a cancel call has to reach into it. Removing an arbitrary entry from a heap costs O(n) to find it. A design that ignores the cancel keeps returning dead jobs.

<!-- stage: insight -->
### Keep Status Apart From The Queue

Store the truth about each job in one place and let every other structure be a hint that the truth can overrule. The **status table** is a hash map from job id to its record, which holds the priority and the current state. Every call that changes what happened to a job writes this table first. A question such as "is job 7 done" is answered by the table and by nothing else.

#### The Ready Set

The **ready set** is a tree set or a heap that orders the waiting jobs by priority, then by smaller id. It exists only to answer the next-job question in O(log n). A job enters the ready set when it is added, and it leaves when it is picked, cancelled or finished. When the structure supports removal by key, as a tree set does, the call removes the job in O(log n) and the ready set never holds a dead job.

#### Entries That Go Stale

A heap cannot remove an arbitrary job quickly. So a cancel or a priority change only updates the status table and leaves the old heap entry in place. A **stale entry** is a heap entry whose job is no longer waiting, or whose priority or version no longer matches the table. A pick pops entries from the top and discards each stale one after comparing it with the table. The first entry that matches the table is the answer. Each entry is pushed once and popped once, so the discards cost O(log n) amortized per call.

The invariant is that the status table alone decides which jobs are live, and every live job has at least one matching entry in the ready set, so a pick that skips stale entries returns the best live job.

<!-- names: status table, ready set, stale entry -->

<!-- stage: variables -->
### What The Service Stores

The service keeps five pieces of state, and each has one owner.

- **Status table** is the authoritative map from job id to priority, version and state, and every call reads and writes it first.
- **Ready set** is the derived order of waiting jobs, and it changes only after the status table accepts the call.
- **Entry** is an immutable record of priority, id and version, so no comparator field changes while it sits in the ready set.
- **Version** is a counter in the job record that increases on each priority change and marks older entries as stale.
- **Pending count** is a number kept in step with the status table, because the size of a heap also counts stale entries.

<!-- stage: trace -->
### Following Calls Through Both Structures

#### Tree Set With Exact Removal

The first trace uses a tree set, so each cancel and each completion removes the job from the ready set at once. The pointer `call` sits on the latest call. The ready set is shown from the best job to the worst, with each job written as `id1 p5` for id 1 with priority 5.

```trace
{"cells":["add(1,5)","add(2,9)","add(3,9)","cancel(2)","next()","complete(3)","cancel(3)","next()"],"pointers":["call"],"steps":[{"at":{"call":0},"vars":{"ready":"id1 p5","result":"true"},"note":"Call 0: job 1 with priority 5 enters the status table and the ready set."},{"at":{"call":1},"vars":{"ready":"id2 p9 id1 p5","result":"true"},"note":"Call 1: job 2 with priority 9 enters the status table and the ready set."},{"at":{"call":2},"vars":{"ready":"id2 p9 id3 p9 id1 p5","result":"true"},"note":"Call 2: job 3 with priority 9 enters the status table and the ready set."},{"at":{"call":3},"vars":{"ready":"id3 p9 id1 p5","result":"true"},"note":"Call 3: job 2 is PENDING, so the table records CANCELLED and the job leaves the ready set."},{"at":{"call":4},"vars":{"ready":"id3 p9 id1 p5","result":"3"},"note":"Call 4: the first job in the ready set is job 3, and the call writes nothing."},{"at":{"call":5},"vars":{"ready":"id1 p5","result":"true"},"note":"Call 5: job 3 is PENDING, so the table records DONE and the job leaves the ready set."},{"at":{"call":6},"vars":{"ready":"id1 p5","result":"false"},"note":"Call 6: job 3 is DONE, which cannot become CANCELLED, so the call returns false and writes nothing."},{"at":{"call":7},"vars":{"ready":"id1 p5","result":"1"},"note":"Call 7: the first job in the ready set is job 1, and the call writes nothing."}]}
```

Jobs 2 and 3 share priority 9, so the smaller id 2 comes first. After job 2 is cancelled, the pick returns job 3. The last cancel names job 3 after it is done, which is not a legal move, so the call returns false and the ready set stays unchanged.

#### Heap With Stale Entries

The second trace uses a heap, so the status table and the heap can disagree. Each heap entry is written as `id1 p5 v0` for id 1, priority 5 and the version it was pushed with. The pending count comes from the status table.

```trace
{"cells":["add(1,5)","add(2,9)","setPriority(2,1)","cancel(1)","add(3,4)","take()","take()"],"pointers":["call"],"steps":[{"at":{"call":0},"vars":{"heap":"id1 p5 v0","pending":"1","result":"true"},"note":"Call 0: job 1 enters the table and the heap gets the entry id1 p5 v0."},{"at":{"call":1},"vars":{"heap":"id2 p9 v0 id1 p5 v0","pending":"2","result":"true"},"note":"Call 1: job 2 enters the table and the heap gets the entry id2 p9 v0."},{"at":{"call":2},"vars":{"heap":"id2 p9 v0 id1 p5 v0 id2 p1 v1","pending":"2","result":"true"},"note":"Call 2: the table records priority 1 and version 1 for job 2, and the heap gets a second entry while the old one stays."},{"at":{"call":3},"vars":{"heap":"id2 p9 v0 id1 p5 v0 id2 p1 v1","pending":"1","result":"true"},"note":"Call 3: the table records CANCELLED for job 1, and its heap entry stays in place."},{"at":{"call":4},"vars":{"heap":"id2 p9 v0 id1 p5 v0 id3 p4 v0 id2 p1 v1","pending":"2","result":"true"},"note":"Call 4: job 3 enters the table and the heap gets the entry id3 p4 v0."},{"at":{"call":5},"vars":{"heap":"id2 p1 v1","pending":"1","result":"3"},"note":"Call 5: the take call discards the stale entries id2 p9 v0, id1 p5 v0 and returns job 3."},{"at":{"call":6},"vars":{"heap":"empty","pending":"0","result":"2"},"note":"Call 6: the take call finds the top entry matching the table and returns job 2."}]}
```

The priority change pushes a second entry for job 2 and leaves the old one. The cancel of job 1 leaves its entry too. The first take pops the entries `id2 p9 v0` and `id1 p5 v0`, finds both stale and discards them. The next entry, `id3 p4 v0`, matches the table, so the call returns job 3. The second take returns job 2 from the entry `id2 p1 v1`. The pending count stays correct throughout, even while the heap holds more entries than there are live jobs.

<!-- stage: code -->
### The Runner With Table And Heap

The class keeps the status table as the source of truth, pushes a new heap entry on each priority change, and skips stale entries in the pick.

```java
final class Runner {
    private record Entry(int priority, int id, int version) {}
    private static final class Job { int priority; int version; boolean pending = true; }

    private final java.util.Map<Integer, Job> table = new java.util.HashMap<>();
    private int pendingCount;                                   // live jobs only; the heap size also counts stale entries
    private final java.util.PriorityQueue<Entry> ready = new java.util.PriorityQueue<>(
        (a, b) -> a.priority() != b.priority() ? Integer.compare(b.priority(), a.priority())
                                                : Integer.compare(a.id(), b.id()));

    boolean add(int id, int priority) {
        if (table.containsKey(id)) return false;               // one hash lookup, no scan
        Job j = new Job(); j.priority = priority;
        table.put(id, j);
        ready.add(new Entry(priority, id, 0));                  // O(log n) push
        pendingCount++;
        return true;
    }

    boolean setPriority(int id, int priority) {
        Job j = table.get(id);
        if (j == null || !j.pending) return false;
        j.priority = priority; j.version++;                     // every older entry of this job is now stale
        ready.add(new Entry(priority, id, j.version));
        return true;
    }

    boolean cancel(int id) {
        Job j = table.get(id);
        if (j == null || !j.pending) return false;
        j.pending = false; pendingCount--;                      // the heap entry stays and goes stale
        return true;
    }

    int take() {
        int id = next();                                        // the top entry is live after next() returns
        if (id >= 0) { table.get(id).pending = false; pendingCount--; ready.poll(); }
        return id;
    }

    int pending() { return pendingCount; }

    int next() {
        while (!ready.isEmpty()) {
            Entry e = ready.peek();
            Job j = table.get(e.id());
            if (j.pending && j.version == e.version()) return e.id();   // matches the table: live
            ready.poll();                                       // stale: discard, each entry once
        }
        return -1;
    }
}
```

Each call costs O(log n) amortized, because an entry is pushed once and discarded at most once. The space is O(n + p) for n jobs and p priority changes.

<!-- stage: applicability -->
### Spotting Entities With A Lifecycle

#### Recognizing The Pattern

The cue is a set of entities that move through states while a query asks for the best live one under a rule. Name the authoritative record first, then list every derived view that depends on it. The invariant is that the record decides what is live and each view only narrows the search.

#### Choosing The Removal Style

Use exact removal when the index supports it in O(log n), as a tree set or a linked hash structure does. Use stale entries when the index is a heap or a plain queue and an entry in the middle cannot be reached. In both styles the record is written before the index, and a rejected call writes nothing.

#### False Friends

A boolean flag inside the queued object looks like a complete answer. It is a false friend when the object is also a key of a sorted structure, because changing a comparator field in place breaks the structure. Replace the entry instead. A heap size is another false friend, since it counts stale entries, so keep a separate counter for the number of live jobs. A plain queue with no status table cannot tell a cancelled job from a waiting one.

<!-- stage: exercises -->
### Exercises

#### [Build] In-Memory Task Lifecycle (Author exercise)
<!-- id: sv-life-task-lifecycle -->

**Prerequisites.** Hash maps and tree sets.

**Problem.** Design a class `Tasks`. The call `add(id, priority)` creates a task in state `PENDING` and returns `true`, or returns `false` if the id was ever used. The call `cancel(id)` moves a `PENDING` task to `CANCELLED` and returns `true`, or returns `false` for any other case. The call `complete(id)` moves a `PENDING` task to `DONE` and returns `true`, or returns `false` for any other case. The call `next()` returns the id of the `PENDING` task with the highest priority, breaking ties by the smaller id, or returns -1 if none exists. It changes nothing. The call `state(id)` returns the state name, or `NONE` for an unknown id.

**Constraints.** The limits are:
- **Ids** are integers from 1 to 10^5, and priorities are integers from 0 to 10^9.
- **Calls** number at most 2 * 10^5.
- **States** are the strings `PENDING`, `DONE`, `CANCELLED` and `NONE`.
- **Return** types are `boolean` for `add`, `cancel` and `complete`, `int` for `next`, and `String` for `state`.

**Example 1.** Input calls `add(1,5)`, `add(2,9)`, `add(3,9)`, `next()`, `cancel(2)`, `next()`, output `true`, `true`, `true`, 2, `true` and 3.

**Example 2.** Input calls `add(4,1)`, `complete(4)`, `cancel(4)`, `next()`, `add(4,7)`, `state(4)`, output `true`, `true`, `false`, -1, `false` and `DONE`.

**Hint.** Which structure answers "what happened to task 4", and which structure answers "who is next"?

**Changed decision.** A move out of `PENDING` removes the task from the ordered set in the same call that writes the table.

#### [Vary] Design a Todo List (LeetCode 2590)
<!-- id: sv-life-todo-list -->

**Prerequisites.** The task exercise above and tree sets.

**Problem.** Design a class `Todo`. The call `addTask(user, due, tags)` creates a pending task for the user, where `tags` is an array of strings, and returns the task id. Ids start at 1 and increase by 1 across all users. Repeated tags in one call count once. The call `complete(user, taskId)` marks the task done and returns `true` when the task exists, belongs to that user and is pending, and otherwise returns `false`. The call `pending(user)` returns the user's pending task ids ordered by `due`, then by id. The call `pendingWithTag(user, tag)` returns the same order, limited to tasks that carry the tag. The call `doneWithTag(user, tag)` returns how many of the user's done tasks carry the tag.

**Constraints.** The limits are:
- **Users** are integers from 1 to 10^4, and `due` is an integer from 1 to 10^9.
- **Tags** are lowercase strings, with 0 to 5 per task.
- **Calls** number at most 10^5, and a call may name an unknown task or user.
- **Return** of the two list calls is a list of ids, and `doneWithTag` returns an `int`.

**Example 1.** Input calls `addTask(1,10,[a,b])`, `addTask(1,5,[b])`, `addTask(2,7,[a])`, `pending(1)`, `pendingWithTag(1,a)`, `complete(2,2)`, `complete(1,1)`, `pending(1)`, output 1, 2, 3, the list 2, 1, the list 1, `false`, `true` and the list 2.

**Example 2.** Input calls `addTask(3,4,[x,x])`, `complete(3,1)`, `doneWithTag(3,x)`, `complete(3,1)`, `pendingWithTag(3,x)`, output 1, `true`, 1, `false` and the empty list.

**Hint.** Which indexes must lose a task when it is completed, and which count must gain it?

**Changed decision.** The user's index and every tag index lose the task in one step, while a done counter per user and tag gains it. The ordered key never changes after creation.

#### [Boundary] Repeated Cancel Or Complete (Author exercise)
<!-- id: sv-life-repeat-cancel -->

**Prerequisites.** The two exercises above and priority queues.

**Problem.** Design a class `Jobs` on a heap. The call `add(id, priority)` creates a `PENDING` job and returns `true`, or returns `false` if the id was ever used. The call `setPriority(id, priority)` changes the priority of a `PENDING` job and returns `true`, or returns `false` otherwise. The call `cancel(id)` returns `true` when the job is `PENDING` or already `CANCELLED`, and returns `false` when it is `DONE` or unknown. The call `complete(id)` returns `true` when the job is `PENDING` or already `DONE`, and returns `false` when it is `CANCELLED` or unknown. The call `take()` marks the highest priority `PENDING` job `DONE`, breaking ties by the smaller id, and returns its id, or returns -1 if none exists. The call `pending()` returns the number of `PENDING` jobs.

**Constraints.** The limits are:
- **Ids** are integers from 1 to 10^5, and priorities are integers from 0 to 10^9.
- **Calls** number at most 3 * 10^5, and any call may repeat.
- **Repeats** of an accepted terminal call change nothing and still return `true`.
- **Return** types are `boolean` for the four state calls and `int` for `take` and `pending`.

**Example 1.** Input calls `add(1,5)`, `add(2,9)`, `setPriority(2,1)`, `take()`, `take()`, `take()`, `complete(2)`, `cancel(2)`, output `true`, `true`, `true`, 1, 2, -1, `true` and `false`.

**Example 2.** Input calls `add(3,4)`, `cancel(3)`, `cancel(3)`, `complete(3)`, `setPriority(3,8)`, `take()`, `pending()`, output `true`, `true`, `true`, `false`, `false`, -1 and 0.

**Hint.** What does a heap entry need to carry so that `take()` can tell it is out of date?

**Changed decision.** A repeated terminal call is accepted without any write, and `pending()` reads a counter because the heap size includes stale entries.

#### [Recognize] Design Ride Sharing System (LeetCode 3829)
<!-- id: sv-life-ride-matching -->

**Prerequisites.** All three exercises above.

**Problem.** This contract is written for the chapter, so the LeetCode statement may differ in detail. Design a class `Rides` with separate id spaces for riders and drivers. The call `addRider(riderId)` puts a rider in state `WAITING`, and `addDriver(driverId)` puts a driver in state `AVAILABLE`. Each returns `false` if that id was ever used.

The call `cancelRider(riderId)` moves a `WAITING` rider to `CANCELLED`. The call `removeDriver(driverId)` moves an `AVAILABLE` driver to `OFFLINE`. The call `finishTrip(driverId)` moves a `BUSY` driver back to `AVAILABLE`. Each of these three returns `true` when the move is legal and `false` otherwise.

The call `match()` pairs the rider who has waited longest with the `AVAILABLE` driver of smallest id, marks the rider `MATCHED` and the driver `BUSY`, and returns `[driverId, riderId]`. If either side has nobody, it returns `[-1, -1]` and changes nothing. The calls `waiting()` and `available()` return the two live counts.

**Constraints.** The limits are:
- **Ids** are integers from 1 to 10^5 in each id space.
- **Calls** number at most 3 * 10^5.
- **Order** of riders is the order of their successful `addRider` calls.
- **Return** types are `boolean` for the state calls, `int[]` of length 2 for `match`, and `int` for the counts.

**Example 1.** Input calls `addRider(10)`, `addRider(11)`, `addDriver(5)`, `addDriver(3)`, `match()`, `cancelRider(11)`, `match()`, `waiting()`, `available()`, output `true`, `true`, `true`, `true`, `[3,10]`, `true`, `[-1,-1]`, 0 and 1.

**Example 2.** Input calls `addDriver(2)`, `addRider(7)`, `cancelRider(7)`, `addRider(8)`, `match()`, `removeDriver(2)`, `finishTrip(2)`, `removeDriver(2)`, `addDriver(2)`, output `true`, `true`, `true`, `true`, `[2,8]`, `false`, `true`, `true` and `false`.

**Hint.** Which side can remove an entry by key, and which side needs stale entries to be skipped?

**Changed decision.** Both sides are checked for a live candidate before either status changes, so a match with no driver leaves the waiting rider in place. This contract uses a longest-waiting rider and a smallest-id driver, and it may differ from the LeetCode statement.
