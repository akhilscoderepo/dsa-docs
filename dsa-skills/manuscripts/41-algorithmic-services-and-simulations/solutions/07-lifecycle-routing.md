<!-- solutions-for: 07-lifecycle-routing -->
### Solutions For Lifecycle Routing

#### Solution: [Build] In-Memory Task Lifecycle (Author exercise)
<!-- id: sv-life-task-lifecycle -->

**Approach.** A hash map from task id to an immutable record of priority and state is the authoritative table. A tree set of immutable keys holds the pending tasks. A key stores the priority and the id, and its comparator puts the larger priority first and the smaller id first among equals.

Every mutating call reads the table first. A cancel or a complete on a task that is not pending returns `false` before any write. Otherwise the call removes the key from the tree set, and then stores a new record with the new state. The key is removed with the same priority it was inserted with, because the table holds that priority and never changes it.

The invariant is that the tree set holds exactly the ids whose table state is `PENDING`, so the first key is always the answer to `next()`.

**Complexity.**

- **Time** is O(log n) per call, because each call does one hash lookup and at most one tree operation. The call `next()` reads the first key.
- **Space** is O(n), because each task owns one record and at most one key.

```java run
import java.util.*;

public final class TaskLifecycleSolution {
    static final class Tasks {
        private enum State { PENDING, DONE, CANCELLED }
        private record Rec(int priority, State state) {}
        private record Key(int priority, int id) {}
        private final Map<Integer, Rec> table = new HashMap<>();                 // id -> record, source of truth
        private final TreeSet<Key> ready = new TreeSet<>((a, b) ->
            a.priority() != b.priority() ? Integer.compare(b.priority(), a.priority()) : Integer.compare(a.id(), b.id()));

        /** Adds a pending task; O(log n) time, O(1) extra space; invariant: ready holds exactly the pending ids. */
        boolean add(int id, int priority) {
            // An id that was ever used is rejected, whatever its state.
            if (table.containsKey(id)) return false;
            table.put(id, new Rec(priority, State.PENDING));
            ready.add(new Key(priority, id));
            return true;
        }

        /** Moves a pending task to a new state; O(log n) time, O(1) space; invariant: the key leaves ready with the move. */
        private boolean leave(int id, State to) {
            Rec r = table.get(id);
            // Validate before any write: only a pending task can move.
            if (r == null || r.state() != State.PENDING) return false;
            ready.remove(new Key(r.priority(), id));
            table.put(id, new Rec(r.priority(), to));
            return true;
        }

        boolean cancel(int id) { return leave(id, State.CANCELLED); }

        boolean complete(int id) { return leave(id, State.DONE); }

        /** Returns the best pending id or -1; O(log n) time (first()), O(1) space; invariant: reads only. */
        int next() { return ready.isEmpty() ? -1 : ready.first().id(); }

        String state(int id) { Rec r = table.get(id); return r == null ? "NONE" : r.state().name(); }
    }

    public static void main(String[] args) {
        // Example 1 from the problem text.
        Tasks a = new Tasks();
        if (!a.add(1, 5) || !a.add(2, 9) || !a.add(3, 9) || a.next() != 2 || !a.cancel(2) || a.next() != 3) throw new AssertionError("e1");
        // Example 2 from the problem text.
        Tasks b = new Tasks();
        if (!b.add(4, 1) || !b.complete(4) || b.cancel(4) || b.next() != -1 || b.add(4, 7) || !b.state(4).equals("DONE")) throw new AssertionError("e2");
        // Random calls checked against a full scan of a plain map.
        Random rnd = new Random(7001);
        for (int round = 0; round < 400; round++) {
            Tasks s = new Tasks();
            Map<Integer, int[]> ref = new HashMap<>();                           // id -> {priority, state 0 pending 1 done 2 cancelled}
            for (int op = 0; op < 120; op++) {
                int id = rnd.nextInt(8), t = rnd.nextInt(5);
                if (t == 0) {
                    int p = rnd.nextInt(4);
                    boolean want = !ref.containsKey(id);
                    if (want) ref.put(id, new int[] {p, 0});
                    if (s.add(id, p) != want) throw new AssertionError("add");
                } else if (t == 1 || t == 2) {
                    boolean want = ref.containsKey(id) && ref.get(id)[1] == 0;
                    if (want) ref.get(id)[1] = t;
                    boolean got = t == 1 ? s.complete(id) : s.cancel(id);
                    if (got != want) throw new AssertionError("move");
                } else {
                    int best = -1;
                    for (int i : ref.keySet()) {
                        int[] v = ref.get(i);
                        if (v[1] != 0) continue;
                        if (best == -1 || v[0] > ref.get(best)[0] || (v[0] == ref.get(best)[0] && i < best)) best = i;
                    }
                    if (s.next() != best) throw new AssertionError("next");
                    String want = !ref.containsKey(id) ? "NONE" : new String[] {"PENDING", "DONE", "CANCELLED"}[ref.get(id)[1]];
                    if (!s.state(id).equals(want)) throw new AssertionError("state");
                }
            }
        }
    }
}
```

#### Solution: [Vary] Design a Todo List (LeetCode 2590)
<!-- id: sv-life-todo-list -->

**Approach.** Three arrays indexed by task id hold the authoritative facts: the owner, the due date and a done flag, and a set of tags per task. Three derived views depend on them. A map from user to a tree set holds that user's pending tasks. A map from the pair of user and tag to a tree set holds the pending tasks that carry the tag. A map from the same pair to an integer counts the done tasks.

A tree set stores `due * 2^20 + id` as one `long`. Because the due date and the id never change after creation, the key never changes while it sits in a set. Sorting by this key orders tasks by due date and then by id.

A complete call checks that the task exists, belongs to the user and is not done. Only then does it set the flag, remove the key from the user set and from each tag set, and raise each tag counter. Duplicate tags are removed when the task is added, so each tag index and counter is touched once per task.

The invariant is that each pending task has its key in the user set and in every tag set it carries, and no done task has a key anywhere.

**Complexity.**

- **Time** is O((t + 1) log n) per add or complete call for t tags per task, and O(k) per list call for k returned ids.
- **Space** is O(n * (t + 1)), because each task owns one key per index it appears in.

```java run
import java.util.*;

public final class TodoListSolution {
    static final class Todo {
        private final List<Integer> owner = new ArrayList<>();                       // index id -> user (id 0 unused)
        private final List<Integer> dueOf = new ArrayList<>();
        private final List<Boolean> done = new ArrayList<>();
        private final List<Set<String>> tagsOf = new ArrayList<>();
        private final Map<Integer, TreeSet<Long>> byUser = new HashMap<>();          // derived: pending keys per user
        private final Map<String, TreeSet<Long>> byTag = new HashMap<>();            // derived: pending keys per user and tag
        private final Map<String, Integer> doneCount = new HashMap<>();              // derived: done tasks per user and tag

        Todo() { owner.add(0); dueOf.add(0); done.add(false); tagsOf.add(Set.of()); }

        private static long key(int due, int id) { return ((long) due << 20) | id; }

        private static String slot(int user, String tag) { return user + "#" + tag; }

        /** Creates a pending task and indexes it; O((t+1) log n) time, O(t) space; invariant: every index sees the new key. */
        int addTask(int user, int due, String[] tags) {
            int id = owner.size();
            Set<String> set = new TreeSet<>(Arrays.asList(tags));                    // repeated tags count once
            owner.add(user); dueOf.add(due); done.add(false); tagsOf.add(set);
            long k = key(due, id);
            byUser.computeIfAbsent(user, x -> new TreeSet<>()).add(k);
            for (String t : set) byTag.computeIfAbsent(slot(user, t), x -> new TreeSet<>()).add(k);
            return id;
        }

        /** Completes a task; O((t+1) log n) time, O(1) space; invariant: validation precedes every write. */
        boolean complete(int user, int taskId) {
            // Validate existence, ownership and state before any write.
            if (taskId < 1 || taskId >= owner.size() || owner.get(taskId) != user || done.get(taskId)) return false;
            done.set(taskId, true);
            long k = key(dueOf.get(taskId), taskId);
            byUser.get(user).remove(k);
            for (String t : tagsOf.get(taskId)) {
                byTag.get(slot(user, t)).remove(k);
                doneCount.merge(slot(user, t), 1, Integer::sum);
            }
            return true;
        }

        private static List<Integer> ids(TreeSet<Long> keys) {
            List<Integer> out = new ArrayList<>();
            if (keys != null) for (long k : keys) out.add((int) (k & ((1 << 20) - 1)));
            return out;
        }

        List<Integer> pending(int user) { return ids(byUser.get(user)); }

        List<Integer> pendingWithTag(int user, String tag) { return ids(byTag.get(slot(user, tag))); }

        int doneWithTag(int user, String tag) { return doneCount.getOrDefault(slot(user, tag), 0); }
    }

    public static void main(String[] args) {
        // Example 1 from the problem text.
        Todo a = new Todo();
        if (a.addTask(1, 10, new String[] {"a", "b"}) != 1 || a.addTask(1, 5, new String[] {"b"}) != 2 || a.addTask(2, 7, new String[] {"a"}) != 3) throw new AssertionError("e1 ids");
        if (!a.pending(1).equals(List.of(2, 1)) || !a.pendingWithTag(1, "a").equals(List.of(1))) throw new AssertionError("e1 lists");
        if (a.complete(2, 2) || !a.complete(1, 1) || !a.pending(1).equals(List.of(2))) throw new AssertionError("e1 complete");
        // Example 2 from the problem text.
        Todo b = new Todo();
        if (b.addTask(3, 4, new String[] {"x", "x"}) != 1 || !b.complete(3, 1) || b.doneWithTag(3, "x") != 1) throw new AssertionError("e2 a");
        if (b.complete(3, 1) || !b.pendingWithTag(3, "x").isEmpty()) throw new AssertionError("e2 b");
        // Random calls checked against a scan of every task.
        Random rnd = new Random(2590);
        String[] pool = {"a", "b", "c"};
        for (int round = 0; round < 300; round++) {
            Todo s = new Todo();
            List<int[]> ref = new ArrayList<>();                                     // {user, due, done}
            List<Set<String>> refTags = new ArrayList<>();
            for (int op = 0; op < 80; op++) {
                int t = rnd.nextInt(5), user = 1 + rnd.nextInt(3);
                if (t == 0 || ref.isEmpty()) {
                    int due = 1 + rnd.nextInt(5), n = rnd.nextInt(4);
                    String[] tags = new String[n];
                    for (int i = 0; i < n; i++) tags[i] = pool[rnd.nextInt(3)];
                    int id = s.addTask(user, due, tags);
                    ref.add(new int[] {user, due, 0});
                    refTags.add(new TreeSet<>(Arrays.asList(tags)));
                    if (id != ref.size()) throw new AssertionError("id");
                } else if (t == 1) {
                    int id = 1 + rnd.nextInt(ref.size() + 1);
                    boolean want = id <= ref.size() && ref.get(id - 1)[0] == user && ref.get(id - 1)[2] == 0;
                    if (want) ref.get(id - 1)[2] = 1;
                    if (s.complete(user, id) != want) throw new AssertionError("complete");
                } else {
                    String tag = pool[rnd.nextInt(3)];
                    List<Integer> all = new ArrayList<>(), withTag = new ArrayList<>();
                    int doneN = 0;
                    for (int i = 0; i < ref.size(); i++) {
                        int[] v = ref.get(i);
                        if (v[0] != user) continue;
                        if (v[2] == 0) { all.add(i); if (refTags.get(i).contains(tag)) withTag.add(i); }
                        else if (refTags.get(i).contains(tag)) doneN++;
                    }
                    Comparator<Integer> byDue = (x, y) -> ref.get(x)[1] != ref.get(y)[1] ? Integer.compare(ref.get(x)[1], ref.get(y)[1]) : Integer.compare(x, y);
                    all.sort(byDue); withTag.sort(byDue);
                    List<Integer> wantAll = new ArrayList<>(), wantTag = new ArrayList<>();
                    for (int i : all) wantAll.add(i + 1);
                    for (int i : withTag) wantTag.add(i + 1);
                    if (!s.pending(user).equals(wantAll)) throw new AssertionError("pending");
                    if (!s.pendingWithTag(user, tag).equals(wantTag)) throw new AssertionError("tagged");
                    if (s.doneWithTag(user, tag) != doneN) throw new AssertionError("done count");
                }
            }
        }
    }
}
```

#### Solution: [Boundary] Repeated Cancel Or Complete (Author exercise)
<!-- id: sv-life-repeat-cancel -->

**Approach.** A hash map holds one mutable job record with a priority, a version and a state. The heap holds immutable entries of priority, id and version. A set of live entries is not kept, so the heap may hold several entries for one job, and only one of them matches the record.

A `setPriority` call changes the record, raises the version and pushes a new entry. The old entry stays in the heap and becomes stale. A `cancel` or a `complete` call changes only the record. A `take` call pops from the top until it meets an entry whose job is pending and whose version equals the record version. It marks that job done and returns the id. A separate counter changes with each pending-to-other move and each add, so `pending()` never reads the heap size.

A repeated terminal call is handled before any write. A cancel on a cancelled job and a complete on a done job return `true` and change nothing, so the counter cannot drop twice. A conflicting terminal call returns `false`.

The invariant is that the record alone decides which jobs are live, every pending job has exactly one matching entry in the heap, and the counter equals the number of pending records.

**Complexity.**

- **Time** is O(log n) amortized per call, because each entry is pushed once and popped at most once.
- **Space** is O(n + p) for n jobs and p priority changes, because stale entries stay until a `take` reaches them.

```java run
import java.util.*;

public final class RepeatCancelSolution {
    static final class Jobs {
        private enum State { PENDING, DONE, CANCELLED }
        private record Entry(int priority, int id, int version) {}
        private static final class Job { int priority; int version; State state = State.PENDING; }
        private final Map<Integer, Job> table = new HashMap<>();                     // source of truth
        private final PriorityQueue<Entry> heap = new PriorityQueue<>((a, b) ->
            a.priority() != b.priority() ? Integer.compare(b.priority(), a.priority()) : Integer.compare(a.id(), b.id()));
        private int pendingCount;                                                    // derived, never read from heap.size()

        /** Adds a pending job; O(log n) time, O(1) space; invariant: one matching entry per pending job. */
        boolean add(int id, int priority) {
            if (table.containsKey(id)) return false;
            Job j = new Job(); j.priority = priority;
            table.put(id, j);
            heap.add(new Entry(priority, id, 0));
            pendingCount++;
            return true;
        }

        /** Changes the priority of a pending job; O(log n) time, O(1) space; invariant: the old entry becomes stale. */
        boolean setPriority(int id, int priority) {
            Job j = table.get(id);
            if (j == null || j.state != State.PENDING) return false;
            j.priority = priority;
            j.version++;                                                             // raising the version marks older entries stale
            heap.add(new Entry(priority, id, j.version));
            return true;
        }

        /** Cancels a job; O(1) time and space; invariant: a repeat changes nothing and the counter drops once. */
        boolean cancel(int id) {
            Job j = table.get(id);
            if (j == null || j.state == State.DONE) return false;
            if (j.state == State.CANCELLED) return true;                             // idempotent repeat
            j.state = State.CANCELLED;
            pendingCount--;
            return true;
        }

        /** Completes a job; O(1) time and space; invariant: a repeat changes nothing and the counter drops once. */
        boolean complete(int id) {
            Job j = table.get(id);
            if (j == null || j.state == State.CANCELLED) return false;
            if (j.state == State.DONE) return true;                                  // idempotent repeat
            j.state = State.DONE;
            pendingCount--;
            return true;
        }

        /** Takes the best pending job; O(log n) amortized time, O(1) space; invariant: stale entries are discarded once. */
        int take() {
            while (!heap.isEmpty()) {
                Entry e = heap.poll();
                Job j = table.get(e.id());
                // An entry is live only when the record is pending and carries the same version.
                if (j.state == State.PENDING && j.version == e.version()) {
                    j.state = State.DONE;
                    pendingCount--;
                    return e.id();
                }
            }
            return -1;
        }

        int pending() { return pendingCount; }
    }

    public static void main(String[] args) {
        // Example 1 from the problem text.
        Jobs a = new Jobs();
        if (!a.add(1, 5) || !a.add(2, 9) || !a.setPriority(2, 1) || a.take() != 1 || a.take() != 2 || a.take() != -1 || !a.complete(2) || a.cancel(2)) throw new AssertionError("e1");
        // Example 2 from the problem text.
        Jobs b = new Jobs();
        if (!b.add(3, 4) || !b.cancel(3) || !b.cancel(3) || b.complete(3) || b.setPriority(3, 8) || b.take() != -1 || b.pending() != 0) throw new AssertionError("e2");
        // Random calls checked against a scan of a plain map with no heap.
        Random rnd = new Random(7003);
        for (int round = 0; round < 400; round++) {
            Jobs s = new Jobs();
            Map<Integer, int[]> ref = new HashMap<>();                               // id -> {priority, state 0 pending 1 done 2 cancelled}
            for (int op = 0; op < 150; op++) {
                int id = rnd.nextInt(6), t = rnd.nextInt(6), p = rnd.nextInt(4);
                int[] v = ref.get(id);
                if (t == 0) {
                    boolean want = v == null;
                    if (want) ref.put(id, new int[] {p, 0});
                    if (s.add(id, p) != want) throw new AssertionError("add");
                } else if (t == 1) {
                    boolean want = v != null && v[1] == 0;
                    if (want) v[0] = p;
                    if (s.setPriority(id, p) != want) throw new AssertionError("setPriority");
                } else if (t == 2) {
                    boolean want = v != null && v[1] != 1;
                    if (want) v[1] = 2;
                    if (s.cancel(id) != want) throw new AssertionError("cancel");
                } else if (t == 3) {
                    boolean want = v != null && v[1] != 2;
                    if (want) v[1] = 1;
                    if (s.complete(id) != want) throw new AssertionError("complete");
                } else {
                    int best = -1;
                    for (int i : ref.keySet()) {
                        int[] w = ref.get(i);
                        if (w[1] != 0) continue;
                        if (best == -1 || w[0] > ref.get(best)[0] || (w[0] == ref.get(best)[0] && i < best)) best = i;
                    }
                    if (best != -1) ref.get(best)[1] = 1;
                    if (s.take() != best) throw new AssertionError("take");
                }
                int count = 0;
                for (int[] w : ref.values()) if (w[1] == 0) count++;
                if (s.pending() != count) throw new AssertionError("pending count");
            }
        }
    }
}
```

#### Solution: [Recognize] Design Ride Sharing System (LeetCode 3829)
<!-- id: sv-life-ride-matching -->

**Approach.** Two hash maps hold the authoritative state of riders and drivers. Each maps an id to its state. A rider is `WAITING`, `MATCHED` or `CANCELLED`. A driver is `AVAILABLE`, `BUSY` or `OFFLINE`. Two live counters follow those states.

The available drivers live in a tree set of ids, so a driver leaves it by key in O(log n), and the first element is the smallest id. The waiting riders live in a FIFO queue in arrival order. A queue cannot remove a rider from the middle, so `cancelRider` only writes the state. The queued id becomes a stale entry, and `match` discards stale entries from the front.

A `match` call first discards stale riders from the front of the queue, and then checks that the queue and the driver set are both non-empty. If either is empty it returns `[-1, -1]` and has written nothing apart from the discards, which change no state. Otherwise it removes both fronts, writes both new states and moves both counters. Because both checks come before the first status write, a match with no driver cannot consume a rider.

The invariant is that the state maps alone decide who is live, the driver set holds exactly the `AVAILABLE` drivers, and every `WAITING` rider has exactly one queue entry in arrival order.

**Complexity.**

- **Time** is O(log n) amortized per call, because the driver set costs O(log n) per change and each rider entry is queued once and discarded at most once.
- **Space** is O(r + d) for r riders and d drivers, because every id owns one state and at most one entry.

```java run
import java.util.*;

public final class RideMatchingSolution {
    static final class Rides {
        private enum R { WAITING, MATCHED, CANCELLED }
        private enum D { AVAILABLE, BUSY, OFFLINE }
        private final Map<Integer, R> rider = new HashMap<>();                       // source of truth for riders
        private final Map<Integer, D> driver = new HashMap<>();                      // source of truth for drivers
        private final ArrayDeque<Integer> queue = new ArrayDeque<>();                // derived: rider ids in arrival order, may hold stale ids
        private final TreeSet<Integer> free = new TreeSet<>();                       // derived: exactly the AVAILABLE drivers
        private int waiting;                                                         // derived live counter

        /** Registers a waiting rider; O(1) time and space; invariant: one queue entry per waiting rider. */
        boolean addRider(int id) {
            if (rider.containsKey(id)) return false;
            rider.put(id, R.WAITING);
            queue.addLast(id);
            waiting++;
            return true;
        }

        /** Registers an available driver; O(log n) time, O(1) space; invariant: free holds exactly the available ids. */
        boolean addDriver(int id) {
            if (driver.containsKey(id)) return false;
            driver.put(id, D.AVAILABLE);
            free.add(id);
            return true;
        }

        /** Cancels a waiting rider; O(1) time and space; invariant: the queue entry becomes stale and the counter drops once. */
        boolean cancelRider(int id) {
            if (rider.get(id) != R.WAITING) return false;
            rider.put(id, R.CANCELLED);
            waiting--;
            return true;
        }

        /** Takes an available driver offline; O(log n) time, O(1) space; invariant: the id leaves free in the same call. */
        boolean removeDriver(int id) {
            if (driver.get(id) != D.AVAILABLE) return false;
            driver.put(id, D.OFFLINE);
            free.remove(id);
            return true;
        }

        /** Returns a busy driver to the available set; O(log n) time, O(1) space; invariant: free gains the id. */
        boolean finishTrip(int id) {
            if (driver.get(id) != D.BUSY) return false;
            driver.put(id, D.AVAILABLE);
            free.add(id);
            return true;
        }

        /** Pairs the longest waiting rider with the smallest free driver; O(log n) amortized time, O(1) space; invariant: both checks precede both writes. */
        int[] match() {
            // Discard stale riders at the front; this changes no state.
            while (!queue.isEmpty() && rider.get(queue.peekFirst()) != R.WAITING) queue.pollFirst();
            if (queue.isEmpty() || free.isEmpty()) return new int[] {-1, -1};
            int r = queue.pollFirst();
            int d = free.pollFirst();
            rider.put(r, R.MATCHED);
            driver.put(d, D.BUSY);
            waiting--;
            return new int[] {d, r};
        }

        int waiting() { return waiting; }

        int available() { return free.size(); }
    }

    public static void main(String[] args) {
        // Example 1 from the problem text.
        Rides a = new Rides();
        a.addRider(10); a.addRider(11); a.addDriver(5); a.addDriver(3);
        if (!Arrays.equals(a.match(), new int[] {3, 10}) || !a.cancelRider(11) || !Arrays.equals(a.match(), new int[] {-1, -1}) || a.waiting() != 0 || a.available() != 1) throw new AssertionError("e1");
        // Example 2 from the problem text.
        Rides b = new Rides();
        if (!b.addDriver(2) || !b.addRider(7) || !b.cancelRider(7) || !b.addRider(8)) throw new AssertionError("e2 setup");
        if (!Arrays.equals(b.match(), new int[] {2, 8}) || b.removeDriver(2) || !b.finishTrip(2) || !b.removeDriver(2) || b.addDriver(2)) throw new AssertionError("e2");
        // Random calls checked against scans of plain state maps.
        Random rnd = new Random(3829);
        for (int round = 0; round < 400; round++) {
            Rides s = new Rides();
            Map<Integer, Integer> rs = new HashMap<>();                              // rider -> 0 waiting 1 matched 2 cancelled
            Map<Integer, Integer> ds = new HashMap<>();                              // driver -> 0 available 1 busy 2 offline
            List<Integer> order = new ArrayList<>();
            for (int op = 0; op < 150; op++) {
                int id = rnd.nextInt(6), t = rnd.nextInt(6);
                if (t == 0) {
                    boolean want = !rs.containsKey(id);
                    if (want) { rs.put(id, 0); order.add(id); }
                    if (s.addRider(id) != want) throw new AssertionError("addRider");
                } else if (t == 1) {
                    boolean want = !ds.containsKey(id);
                    if (want) ds.put(id, 0);
                    if (s.addDriver(id) != want) throw new AssertionError("addDriver");
                } else if (t == 2) {
                    boolean want = Integer.valueOf(0).equals(rs.get(id));
                    if (want) rs.put(id, 2);
                    if (s.cancelRider(id) != want) throw new AssertionError("cancelRider");
                } else if (t == 3) {
                    boolean want = Integer.valueOf(0).equals(ds.get(id));
                    if (want) ds.put(id, 2);
                    if (s.removeDriver(id) != want) throw new AssertionError("removeDriver");
                } else if (t == 4) {
                    boolean want = Integer.valueOf(1).equals(ds.get(id));
                    if (want) ds.put(id, 0);
                    if (s.finishTrip(id) != want) throw new AssertionError("finishTrip");
                } else {
                    int r = -1, d = -1;
                    for (int x : order) if (rs.get(x) == 0) { r = x; break; }
                    for (int x : new TreeSet<>(ds.keySet())) if (ds.get(x) == 0) { d = x; break; }
                    int[] want = r == -1 || d == -1 ? new int[] {-1, -1} : new int[] {d, r};
                    if (want[0] != -1) { rs.put(r, 1); ds.put(d, 1); }
                    if (!Arrays.equals(s.match(), want)) throw new AssertionError("match");
                }
                int w = 0, f = 0;
                for (int v : rs.values()) if (v == 0) w++;
                for (int v : ds.values()) if (v == 0) f++;
                if (s.waiting() != w || s.available() != f) throw new AssertionError("counts");
            }
        }
    }
}
```
