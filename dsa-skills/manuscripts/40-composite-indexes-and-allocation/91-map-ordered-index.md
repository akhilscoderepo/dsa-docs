<!-- lesson-kind: combination -->
<!-- lesson-id: map-ordered-index -->
## Look Up By ID And By Order

<!-- stage: context -->
### One Task Runs Twice

A task service keeps every pending task in two views. Operators open a user's page and run that user's most urgent task. A background worker runs the most urgent task of the whole system. Both views read the same tasks. On a quiet afternoon an operator runs a task from a user's page, and a minute later the worker runs the same task again. The customer receives two emails.

Neither view is slow, and neither holds a wrong priority. The operator's path removed the task from the user's view and forgot the system view. A task can leave the service through two doors, and only one door cleaned up behind it.

This lesson combines the record map, the sorted index and the all-or-nothing call from earlier lessons. It asks how to design a class where several calls can remove or change one record, and every call leaves every view agreeing.

<!-- stage: contributions -->
### What The Earlier Lessons Contribute

#### A Record That Decides

The lesson Multi-Index Records supplied the habit of naming one map as the record that decides, and of repairing every other structure from the old value that the record stores. This lesson keeps that map and adds one more view to repair.

#### Orders That Never Tie

The lesson Dynamic Rankings supplied the comparator rule. Every field that breaks a tie is compared in turn, the last field is unique, and an update removes the entry that carries the old fields. This lesson reuses that rule for two sorted sets that hold the same tasks.

#### Plans Before Writes

The lesson Transaction Lifecycles supplied the plan and commit split. This lesson uses it to make sure that a removal through any door reaches every sorted set.

#### The Choice This Lesson Adds

The new work is the number of exits. Each earlier lesson had one place where a record left the structure. Here a record leaves through the global exit, through the per-user exit and through an explicit remove call. All three must run the same repair.

<!-- stage: naive -->
### Two Sorted Sets Repaired By Hand

The direct design keeps a global tree set and a map from user to a tree set. Each method repairs the sets it remembers.

```java
final class NaiveDesk {
    record Task(int priority, int id, int user) {}
    private final java.util.Comparator<Task> order = (a, b) ->
            a.priority() != b.priority() ? Integer.compare(b.priority(), a.priority()) : Integer.compare(b.id(), a.id());
    private final java.util.TreeSet<Task> global = new java.util.TreeSet<>(order);
    private final java.util.Map<Integer, java.util.TreeSet<Task>> perUser = new java.util.HashMap<>();

    void add(int user, int id, int priority) {
        Task t = new Task(priority, id, user);
        global.add(t);
        perUser.computeIfAbsent(user, k -> new java.util.TreeSet<>(order)).add(t);
    }

    int execUser(int user) {
        java.util.TreeSet<Task> mine = perUser.get(user);
        if (mine == null || mine.isEmpty()) return -1;
        return mine.pollFirst().id();            // the global set still holds this task
    }

    int execGlobal() {
        Task t = global.pollFirst();
        return t == null ? -1 : t.id();          // the user's set still holds this task
    }
}
```

After `add(1, 7, 5)` and `execUser(1)`, the call `execGlobal()` returns 7 again.

```predict
A task has been run through the user's page. Which of the two calls can run it a second time, and which of the two calls can keep a task alive after the global call ran it?

Both can. The global call finds the task because the user path never touched the global set. The user call finds the task because the global path never touched the user's set. Each exit fixes one set and leaves the other with a task that no longer exists.
```

<!-- stage: bottleneck -->
### Every Exit Must Repair Every Set

The cost of the naive design is correctness, and it grows with the number of exits. A class with two sorted sets and three ways to remove a task has six repair decisions to make. A missed one produces a task that runs twice or a task that never runs.

Repairing by search does not help. A scan of the user's set for the task that the global set returned costs O(n), and a scan in the other direction costs the same. The class already knows the task, so it can build the exact old key and remove it in O(log n).

The design needs one place that removes a task from all three structures, and every public call has to pass through that place.

<!-- stage: insight -->
### One Removal Path For Every Exit

The class keeps three structures. The map from task id to task is the record that decides. The **global index** is a sorted set of all tasks. The **owner index** is a map from user to a sorted set of that user's tasks.

#### The Single Place That Writes

A **removal helper** takes one task, removes it from the record, from the global index and from the owner index, and deletes an owner set that becomes empty. A matching insert helper does the reverse. No public call touches a structure directly. Add calls insert, edit calls remove and insert, a remove call removes, and both execute calls pick a task from one index and then call the helper.

#### Why The Order Of Steps Matters

An execute call reads the task from one index first and removes it second. The removal uses the full task object, because both sorted sets find entries by their fields. An edit builds the new task as a copy and runs remove-then-insert in the helper, so the old fields leave every set before the new fields enter.

The invariant is that the record, the global index and the owner index hold the same tasks, with the same fields, after every call.

<!-- names: global index, owner index, removal helper -->

<!-- stage: variables -->
### Three Views And Two Helpers

The class stores one record and two indexes, and two helpers write them.

- **byId** maps each task id to its immutable task and is the record that decides.
- **global** is a tree set of all tasks, ordered by higher priority and then by larger id.
- **perUser** maps each user to a tree set of that user's tasks, with the same order.
- **insert** and **drop** are the only methods that write the three structures.

An owner set that becomes empty is removed from `perUser`, so a query for an unknown user and for a user with no tasks gives the same answer.

<!-- stage: trace -->
### Following Tasks Through Three Views

#### Running A Task From A User's Page

The first trace adds three tasks and runs one through each door. The pointer `call` marks the call that just ran. The columns show the task ids in the global order, then the ids of each user.

```trace
{"cells":["add(1,101,5)","add(1,102,7)","add(2,103,7)","execUser(1)","execGlobal()","execGlobal()"],"pointers":["call"],"steps":[{"at":{"call":0},"vars":{"global":"101","users":"u1:[101]","result":"null"},"note":"Call 0: task 101 enters the record, the global index and the list of user 1."},{"at":{"call":1},"vars":{"global":"102 101","users":"u1:[102,101]","result":"null"},"note":"Call 1: task 102 enters the record, the global index and the list of user 1."},{"at":{"call":2},"vars":{"global":"103 102 101","users":"u1:[102,101] u2:[103]","result":"null"},"note":"Call 2: task 103 enters the record, the global index and the list of user 2."},{"at":{"call":3},"vars":{"global":"103 101","users":"u1:[101] u2:[103]","result":"102"},"note":"Call 3: the best task of user 1 is 102. The helper removes it from all three structures."},{"at":{"call":4},"vars":{"global":"101","users":"u1:[101]","result":"103"},"note":"Call 4: the best task overall is 103. The helper removes it from all three structures."},{"at":{"call":5},"vars":{"global":"empty","users":"empty","result":"101"},"note":"Call 5: the best task overall is 101. The helper removes it from all three structures."}]}
```

The fourth call runs task 102 through the user door. The helper removes it from the global index in the same step, so the later global call does not see it.

#### Editing And Then Running

The second trace edits a priority and runs a task through the global door.

```trace
{"cells":["add(4,301,2)","add(4,302,9)","add(5,303,4)","edit(301,10)","execGlobal()","execUser(4)","execGlobal()"],"pointers":["call"],"steps":[{"at":{"call":0},"vars":{"global":"301","users":"u4:[301]","result":"null"},"note":"Call 0: task 301 enters the record, the global index and the list of user 4."},{"at":{"call":1},"vars":{"global":"302 301","users":"u4:[302,301]","result":"null"},"note":"Call 1: task 302 enters the record, the global index and the list of user 4."},{"at":{"call":2},"vars":{"global":"302 303 301","users":"u4:[302,301] u5:[303]","result":"null"},"note":"Call 2: task 303 enters the record, the global index and the list of user 5."},{"at":{"call":3},"vars":{"global":"301 302 303","users":"u4:[301,302] u5:[303]","result":"null"},"note":"Call 3: the helper removes the old entry of task 301 everywhere, then inserts it with priority 10."},{"at":{"call":4},"vars":{"global":"302 303","users":"u4:[302] u5:[303]","result":"301"},"note":"Call 4: the best task overall is 301. The helper removes it from all three structures."},{"at":{"call":5},"vars":{"global":"303","users":"u5:[303]","result":"302"},"note":"Call 5: the best task of user 4 is 302. The helper removes it from all three structures."},{"at":{"call":6},"vars":{"global":"empty","users":"empty","result":"303"},"note":"Call 6: the best task overall is 303. The helper removes it from all three structures."}]}
```

The edit removes the old entry first. The global call then finds the new priority at the front, and the helper removes that task from the list of user 4 as well.

<!-- stage: code -->
### The Task Desk In Java

The class routes every change through two helpers.

```java
final class TaskDesk {
    private record Task(int priority, int id, int user) {}
    private static final java.util.Comparator<Task> ORDER = (a, b) ->
            a.priority() != b.priority() ? Integer.compare(b.priority(), a.priority()) : Integer.compare(b.id(), a.id());
    private final java.util.Map<Integer, Task> byId = new java.util.HashMap<>();
    private final java.util.TreeSet<Task> global = new java.util.TreeSet<>(ORDER);
    private final java.util.Map<Integer, java.util.TreeSet<Task>> perUser = new java.util.HashMap<>();

    private void insert(Task t) {
        byId.put(t.id(), t);
        global.add(t);
        perUser.computeIfAbsent(t.user(), k -> new java.util.TreeSet<>(ORDER)).add(t);
    }

    private void drop(Task t) {
        byId.remove(t.id());
        global.remove(t);                                   // the exact object removes the exact entry
        java.util.TreeSet<Task> mine = perUser.get(t.user());
        mine.remove(t);
        if (mine.isEmpty()) perUser.remove(t.user());
    }

    int execGlobal() {
        if (global.isEmpty()) return -1;
        Task t = global.first();
        drop(t);
        return t.id();
    }
}
```

Every call costs O(log n), because the helpers do a constant number of hash and tree operations. The space is O(n), because each task sits in three structures.

<!-- stage: applicability -->
### Several Exits From One Record

#### Counting The Doors

List every public call that creates, changes or removes a record. Mark which indexes each call must touch. If two calls remove the same record, they must share a helper. The invariant is that the record and every index hold the same tasks after each call.

#### Order Fields And Copies

A sorted set compares the fields of its entries, so an edit must remove the old entry before the new fields exist anywhere in the set. Store immutable entries and build a new entry per edit. The comparator must end with a unique field, so removing an entry cannot remove a different one.

#### False Friends And Limits

A lazy heap with version checks looks like a way to avoid the helper. It is a false friend when two heaps exist for the same records, because a version number in one heap says nothing about the other heap. Skip the owner index when no call asks about one user, because the second index then costs memory and gives nothing back.

<!-- stage: exercises -->
### Exercises

#### [Build] Number Container With Floor (LeetCode 2349)
<!-- id: ci40-nc-floor -->

**Prerequisites.** The multi-index lesson and the helper idea above.

**Problem.** Design a class `FloorContainers` with an unbounded array of slots, all empty. The call `change(index, number)` stores `number` in a slot and replaces any earlier value. The call `clear(index)` empties a slot. The call `find(number, floor)` returns the smallest index that is at least `floor` and holds `number`, or -1 if none exists.

**Constraints.** The limits are:
- **Indexes** satisfy `0 <= index <= 10^9`, and **numbers** satisfy `1 <= number <= 10^9`.
- **Floor** satisfies `0 <= floor <= 10^9`.
- **Calls** number at most `10^5`, and `clear` may name an empty slot.
- **Return** of `find` is an `int`.

**Example 1.** Input calls `change(1,10)`, `change(5,10)`, `change(9,10)`, `find(10,2)`, `clear(5)`, `find(10,2)`, output 5 and then 9.

**Example 2.** Input calls `find(10,10)`, `find(7,0)` on an empty container, output -1 and -1.

**Hint.** Which method of a tree set answers "smallest element at least x"?

**Changed decision.** The query adds a lower bound and a clear call adds a second exit, so both go through the same removal helper.

#### [Vary] Food Ratings With Retirement (LeetCode 2353)
<!-- id: ci40-food-retire -->

**Prerequisites.** The Build exercise above.

**Problem.** Design a class `FoodMenu` built from arrays `foods`, `cuisines` and `ratings`. The call `changeRating(food, rating)` sets a rating. The call `retire(food)` removes a food from the menu for good. The call `topTwo(cuisine)` returns the names of up to two foods of that cuisine, in order of higher rating first and smaller name second.

**Constraints.** The limits are:
- **Foods** are distinct lowercase strings, and the arrays hold `1` to `10^4` entries.
- **Ratings** satisfy `1 <= rating <= 10^8`.
- **Calls** number at most `10^4`, and `changeRating` and `retire` name foods that are still on the menu.
- **Return** of `topTwo` is a list of at most two names.

**Example 1.** Input foods `a` (x, 5), `b` (x, 9), `c` (x, 9), `d` (y, 4) and the calls `topTwo(x)`, `retire(b)`, `topTwo(x)`, output `b`, `c` and then `c`, `a`.

**Example 2.** Input the same calls, then `changeRating(a,9)`, `topTwo(x)`, output `a`, `c`.

**Hint.** Which two structures must forget a retired food?

**Changed decision.** A retire call is a second exit for a record, so it shares the removal path with a rating change.

#### [Boundary] Movie Desk With Strict Moves (LeetCode 1912)
<!-- id: ci40-movie-desk -->

**Prerequisites.** The two exercises above.

**Problem.** A chain has shops with at most one copy of each movie at a fixed price. Design a class `MovieDesk` built from entries `{shop, movie, price}`, all unrented. The call `rent(shop, movie)` returns `true` and marks the copy rented if the copy exists and is unrented, and returns `false` otherwise. The call `drop(shop, movie)` returns `true` and marks it unrented if the copy is rented, and returns `false` otherwise. The call `search(movie)` returns up to 3 shops with an unrented copy, ordered by price and then shop. The call `rentedCount()` returns the number of rented copies.

**Constraints.** The limits are:
- **Entries** number at most `10^5`, with one copy per pair of shop and movie.
- **Prices** are integers from 1 to 10^4, and **shops** and **movies** are integers from 0 to 10^5.
- **Calls** number at most `10^5`, and `rent` and `drop` may name a pair that has no copy.
- **Rejected** calls change nothing.

**Example 1.** Input entries `{0,1,5}`, `{1,1,4}`, `{2,1,4}` and the calls `search(1)`, `rent(1,1)`, `rent(1,1)`, `search(1)`, output shops 1, 2, 0, then `true`, `false` and shops 2, 0.

**Example 2.** Input the same entries and the calls `drop(0,1)`, `rent(9,9)`, `rent(0,1)`, `rentedCount()`, output `false`, `false`, `true` and 1.

**Hint.** What does a state field on each copy replace, and which check runs before a move?

**Changed decision.** Each copy carries a state, and one move helper changes the state and both views.

#### [Recognize] Task Desk With Two Exits (LeetCode 3408)
<!-- id: ci40-task-desk -->

**Prerequisites.** All three exercises above.

**Problem.** This chapter writes the contract below itself, and it can differ in detail from LeetCode. Design a class `TaskDesk`. The call `add(userId, taskId, priority)` adds a task with a new id. The call `edit(taskId, priority)` changes a priority. The call `rmv(taskId)` deletes a task. The call `execGlobal()` runs and removes the task with the highest priority overall, with the larger task id winning ties, and returns its id, or -1 if no task exists. The call `execUser(userId)` does the same for one user's tasks.

**Constraints.** The limits are:
- **Tasks** number at most `10^5` at any time, and **priorities** satisfy `0 <= priority <= 10^9`.
- **Calls** number at most `2 * 10^5`, and `edit` and `rmv` name live tasks.
- **Users** are integers from 1 to 10^5.
- **Return** of both execute calls is an `int`.

**Example 1.** Input tasks `{1,101,5}`, `{1,102,7}`, `{2,103,7}` and the calls `execUser(1)`, `execGlobal()`, `execGlobal()`, output 102, 103 and 101.

**Example 2.** Input the calls `execUser(3)`, `add(3,200,1)`, `execGlobal()`, `execUser(3)`, output -1, then 200, then -1.

**Hint.** Which calls remove a task, and which structures must each of them reach?

**Changed decision.** Both execute calls and the remove call are exits, so all three go through one helper and no exit repairs a set by hand.
