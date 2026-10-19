<!-- solutions-for: 02-dynamic-rankings -->
### Solutions For Dynamic Rankings

#### Solution: [Build] Design A Leaderboard (LeetCode 1244)
<!-- id: ci40-leaderboard -->

**Approach.** A hash map from player id to total is the source of truth. A tree set of immutable entries is the ranking. The comparator puts the higher total first and breaks ties by the smaller id, so no two entries compare equal.

An add call removes the entry built from the stored total, computes the new total, stores it and inserts the new entry. A reset call does the same with a new total of 0. A top call walks the first `K` entries of the set and sums their totals in a `long`.

The invariant is that the set holds one entry per player, and the entry carries the stored total. The removal precedes the insertion, so the set never holds two entries for one player.

**Complexity.**

- **Time** is O(log n) per update and O(K) per top query, because an update does one removal and one insertion, and the iterator starts at the first entry.
- **Space** is O(n), because each player owns one map slot and one entry.

```java run
import java.util.*;

public final class LeaderboardSolution {
    static final class Leaderboard {
        private record Entry(long score, int id) {}
        private final Map<Integer, Long> totalOf = new HashMap<>();   // id -> total, source of truth
        private final TreeSet<Entry> board = new TreeSet<>((a, b) -> {
            int c = Long.compare(b.score(), a.score());                // higher total first
            return c != 0 ? c : Integer.compare(a.id(), b.id());       // smaller id first among equals
        });

        /**
         * Replaces a player's total and repairs the ranking.
         * Time: O(log n), because it does one removal and one insertion.
         * Space: O(1) extra.
         * Invariant: board holds exactly one entry per player with the stored total.
         */
        private void set(int id, long total) {
            Long old = totalOf.get(id);
            // Remove the exact old key; a new player has none.
            if (old != null) board.remove(new Entry(old, id));
            totalOf.put(id, total);
            board.add(new Entry(total, id));
        }

        void addScore(int id, int score) {
            // Add to the stored total, or start from zero for a new player.
            set(id, totalOf.getOrDefault(id, 0L) + score);
        }

        /** Sums the first K entries in rank order; O(K) time, O(1) space; invariant: iteration order equals rank order. */
        long top(int k) {
            long sum = 0;
            for (Entry e : board) {
                if (k-- == 0) break;
                sum += e.score();
            }
            return sum;
        }

        void reset(int id) { set(id, 0); }
    }

    public static void main(String[] args) {
        // Example 1 and Example 2 from the problem text.
        Leaderboard lb = new Leaderboard();
        lb.addScore(1, 50); lb.addScore(2, 30); lb.addScore(3, 40);
        if (lb.top(2) != 90) throw new AssertionError("e1");
        lb.addScore(2, 25); lb.reset(1);
        if (lb.top(2) != 95) throw new AssertionError("e2");
        // Random calls checked against sorting a plain array each time.
        Random rnd = new Random(1244);
        for (int round = 0; round < 300; round++) {
            Leaderboard s = new Leaderboard();
            long[] ref = new long[9];
            boolean[] seen = new boolean[9];
            for (int op = 0; op < 100; op++) {
                int id = 1 + rnd.nextInt(8);
                int t = rnd.nextInt(3);
                if (t == 0) { int p = 1 + rnd.nextInt(5); ref[id] += p; seen[id] = true; s.addScore(id, p); }
                else if (t == 1 && seen[id]) { ref[id] = 0; s.reset(id); }
                else {
                    List<Long> all = new ArrayList<>();
                    for (int i = 1; i < 9; i++) if (seen[i]) all.add(ref[i]);
                    if (all.isEmpty()) continue;
                    all.sort(Collections.reverseOrder());
                    int k = 1 + rnd.nextInt(all.size());
                    long want = 0;
                    for (int i = 0; i < k; i++) want += all.get(i);
                    if (s.top(k) != want) throw new AssertionError("top");
                }
            }
        }
    }
}
```

#### Solution: [Vary] Sequentially Ordinal Rank Tracker (LeetCode 2102)
<!-- id: ci40-rank-tracker -->

**Approach.** Two tree sets share one comparator, which ranks the higher score first and the smaller name second. The set `returned` holds the entries at ranks 1 up to `i - 1`, where `i - 1` is the number of earlier get calls. The set `pending` holds every other entry.

A get call moves the first entry of `pending` into `returned` and returns its name. That entry is the one at rank `i`, because `returned` holds exactly the better entries. An add call must keep every entry of `returned` better than every entry of `pending`. When the new entry beats the last entry of `returned`, the call inserts it into `returned` and moves the last entry of `returned` to `pending`. Otherwise the call inserts it into `pending`.

The invariant is that `returned` holds the best `i - 1` entries overall, and its size changes only in a get call.

**Complexity.**

- **Time** per call is O(log n). Each call performs at most three tree operations.
- **Space** is O(n), because each entry sits in exactly one of the two sets.

```java run
import java.util.*;

public final class RankTrackerSolution {
    static final class RankTracker {
        private record Place(int score, String name) {}
        private static final Comparator<Place> BETTER_FIRST = (a, b) -> {
            int c = Integer.compare(b.score(), a.score());
            return c != 0 ? c : a.name().compareTo(b.name());
        };
        private final TreeSet<Place> returned = new TreeSet<>(BETTER_FIRST);   // ranks 1 .. gets
        private final TreeSet<Place> pending = new TreeSet<>(BETTER_FIRST);    // all lower ranks

        /**
         * Inserts a place while keeping every returned place better than every pending place.
         * Time: O(log n).
         * Space: O(1) extra.
         * Invariant: returned holds the best |returned| places overall.
         */
        void add(String name, int score) {
            Place p = new Place(score, name);
            // A place that beats the weakest returned place takes its slot, and that place moves down.
            if (!returned.isEmpty() && BETTER_FIRST.compare(p, returned.last()) < 0) {
                returned.add(p);
                pending.add(returned.pollLast());
            } else {
                pending.add(p);
            }
        }

        /** Returns the place at the next rank; O(log n) time, O(1) extra space; invariant: the size of returned grows by one. */
        String get() {
            Place best = pending.pollFirst();   // best place not yet returned
            returned.add(best);
            return best.name();
        }
    }

    public static void main(String[] args) {
        // Examples from the problem text.
        RankTracker a = new RankTracker();
        a.add("a", 3); a.add("b", 5);
        if (!a.get().equals("b")) throw new AssertionError("e1 first");
        a.add("c", 4);
        if (!a.get().equals("c")) throw new AssertionError("e1 second");
        RankTracker b = new RankTracker();
        b.add("x", 1); b.add("y", 1);
        if (!b.get().equals("x") || !b.get().equals("y")) throw new AssertionError("e2");
        // Random calls checked by sorting all places and taking the i-th.
        Random rnd = new Random(2102);
        for (int round = 0; round < 300; round++) {
            RankTracker s = new RankTracker();
            List<int[]> all = new ArrayList<>();                  // {score, name number}
            int gets = 0, next = 0;
            for (int op = 0; op < 60; op++) {
                if (all.size() > gets && rnd.nextInt(3) == 0) {
                    gets++;
                    List<int[]> sorted = new ArrayList<>(all);
                    sorted.sort((x, y) -> x[0] != y[0] ? Integer.compare(y[0], x[0]) : Integer.compare(x[1], y[1]));
                    String want = "n" + (char) ('a' + sorted.get(gets - 1)[1] / 26) + (char) ('a' + sorted.get(gets - 1)[1] % 26);
                    if (!s.get().equals(want)) throw new AssertionError("rank " + gets);
                } else {
                    int score = 1 + rnd.nextInt(4);
                    String nm = "n" + (char) ('a' + next / 26) + (char) ('a' + next % 26);
                    all.add(new int[] {score, next++});
                    s.add(nm, score);
                }
            }
        }
    }
}
```

#### Solution: [Boundary] Equal Scores And Renames (Author exercise)
<!-- id: ci40-equal-renames -->

**Approach.** A map from id to a record of name and score is the source of truth. A tree set of immutable entries holds the ranking. The comparator compares the higher score first, then the smaller name, then the smaller id, so two players with equal names and scores stay distinct.

A rename call removes the entry built from the stored name and score, stores the new name and inserts the new entry. A top call collects the names of the first `k` entries.

The invariant is that the set holds one entry per id, and the entry carries the stored name. A comparator that stops at the name would treat two players called `sam` with equal scores as one entry, and the second add would vanish.

**Complexity.**

- **Time** is O(log n) per add and rename, and O(k) per query, because the iterator starts at the first entry.
- **Space** is O(n), because each id owns one record and one entry.

```java run
import java.util.*;

public final class EqualRenamesSolution {
    static final class NameBoard {
        private record Row(int score, String name, int id) {}
        private final Map<Integer, Row> rowOf = new HashMap<>();     // id -> current row, source of truth
        private final TreeSet<Row> ranking = new TreeSet<>((a, b) -> {
            int c = Integer.compare(b.score(), a.score());
            if (c != 0) return c;
            c = a.name().compareTo(b.name());
            return c != 0 ? c : Integer.compare(a.id(), b.id());     // id keeps the order total
        });

        /** Registers a player; O(log n) time, O(1) extra space; invariant: one row per id in both structures. */
        void add(int id, String name, int score) {
            Row r = new Row(score, name, id);
            rowOf.put(id, r);
            ranking.add(r);
        }

        /**
         * Changes a name and repairs the ranking.
         * Time: O(log n).
         * Space: O(1) extra.
         * Invariant: the removed row equals the stored row field by field.
         */
        void rename(int id, String newName) {
            Row old = rowOf.get(id);
            // The removal needs the old name, because the comparator reads it.
            ranking.remove(old);
            Row now = new Row(old.score(), newName, id);
            rowOf.put(id, now);
            ranking.add(now);
        }

        /** Returns the names of the first k rows; O(k) time, O(k) space for the result. */
        List<String> topNames(int k) {
            List<String> out = new ArrayList<>();
            for (Row r : ranking) {
                if (out.size() == k) break;
                out.add(r.name());
            }
            return out;
        }
    }

    public static void main(String[] args) {
        // Example 1: two players called sam with the same score both appear.
        NameBoard a = new NameBoard();
        a.add(1, "sam", 10); a.add(2, "sam", 10);
        if (!a.topNames(2).equals(List.of("sam", "sam"))) throw new AssertionError("e1");
        // Example 2: a rename moves a player ahead of an equal score.
        NameBoard b = new NameBoard();
        b.add(1, "zed", 5); b.add(2, "amy", 5); b.rename(1, "abe");
        if (!b.topNames(2).equals(List.of("abe", "amy"))) throw new AssertionError("e2");
        // Random calls checked against sorting all rows.
        Random rnd = new Random(40);
        String[] pool = {"amy", "abe", "sam", "zed"};
        for (int round = 0; round < 300; round++) {
            NameBoard s = new NameBoard();
            int n = 1 + rnd.nextInt(8);
            String[] nm = new String[n];
            int[] sc = new int[n];
            for (int i = 0; i < n; i++) { nm[i] = pool[rnd.nextInt(4)]; sc[i] = rnd.nextInt(3); s.add(i + 1, nm[i], sc[i]); }
            for (int op = 0; op < 40; op++) {
                if (rnd.nextBoolean()) { int i = rnd.nextInt(n); nm[i] = pool[rnd.nextInt(4)]; s.rename(i + 1, nm[i]); }
                else {
                    Integer[] order = new Integer[n];
                    for (int i = 0; i < n; i++) order[i] = i;
                    Arrays.sort(order, (x, y) -> sc[x] != sc[y] ? Integer.compare(sc[y], sc[x]) : !nm[x].equals(nm[y]) ? nm[x].compareTo(nm[y]) : Integer.compare(x, y));
                    int k = 1 + rnd.nextInt(n);
                    List<String> want = new ArrayList<>();
                    for (int i = 0; i < k; i++) want.add(nm[order[i]]);
                    if (!s.topNames(k).equals(want)) throw new AssertionError("topNames");
                }
            }
        }
    }
}
```

#### Solution: [Recognize] Design Task Manager (LeetCode 3408)
<!-- id: ci40-task-manager -->

**Approach.** A map from task id to an immutable task is the source of truth. A tree set of the same tasks is the ranking. The comparator puts the higher priority first and the larger task id second, which matches the required tie rule and keeps the order total.

An edit call removes the task built from the stored fields, stores a copy with the new priority and inserts it. A remove call deletes the task from the set and the map. An execute call takes the first task of the set, deletes it from the map as well, and returns its user id.

The invariant is that the map and the set hold the same tasks. Execute updates both structures, so a task never stays in one after it leaves the other.

**Complexity.**

- **Time** per call is O(log n). A call costs one hash operation plus two tree operations at most.
- **Space** is O(n), because each live task owns one map slot and one tree entry.

```java run
import java.util.*;

public final class TaskManagerSolution {
    static final class TaskManager {
        private record Task(int priority, int taskId, int userId) {}
        private final Map<Integer, Task> byId = new HashMap<>();       // taskId -> task, source of truth
        private final TreeSet<Task> ranking = new TreeSet<>((a, b) -> {
            int c = Integer.compare(b.priority(), a.priority());        // higher priority first
            return c != 0 ? c : Integer.compare(b.taskId(), a.taskId()); // larger task id first on ties
        });

        /** Adds a task; O(log n) time, O(1) space; invariant: the task enters both structures. */
        void add(int userId, int taskId, int priority) {
            Task t = new Task(priority, taskId, userId);
            byId.put(taskId, t);
            ranking.add(t);
        }

        /** Changes a priority; O(log n) time, O(1) space; invariant: the old entry leaves before the new one enters. */
        void edit(int taskId, int newPriority) {
            Task old = byId.get(taskId);
            ranking.remove(old);
            Task now = new Task(newPriority, taskId, old.userId());
            byId.put(taskId, now);
            ranking.add(now);
        }

        /** Deletes a task; O(log n) time, O(1) space; invariant: the task leaves both structures. */
        void rmv(int taskId) {
            ranking.remove(byId.remove(taskId));
        }

        /**
         * Removes and reports the best task.
         * Time: O(log n).
         * Space: O(1).
         * Invariant: the executed task leaves the map and the set together.
         */
        int execTop() {
            // pollFirst removes the best entry from the set in one step.
            Task best = ranking.pollFirst();
            if (best == null) return -1;
            byId.remove(best.taskId());
            return best.userId();
        }
    }

    public static void main(String[] args) {
        // Example 1: ties go to the larger task id.
        TaskManager a = new TaskManager();
        a.add(1, 101, 5); a.add(2, 102, 9); a.add(3, 103, 9);
        if (a.execTop() != 3 || a.execTop() != 2) throw new AssertionError("e1");
        // Example 2: edit then remove.
        TaskManager b = new TaskManager();
        b.add(1, 101, 5); b.add(2, 102, 9); b.edit(101, 12);
        if (b.execTop() != 1) throw new AssertionError("e2 first");
        b.rmv(102);
        if (b.execTop() != -1) throw new AssertionError("e2 last");
        // Random calls checked against a scan of a plain map.
        Random rnd = new Random(3408);
        for (int round = 0; round < 300; round++) {
            TaskManager s = new TaskManager();
            Map<Integer, int[]> ref = new HashMap<>();              // taskId -> {user, priority}
            int next = 0;
            for (int op = 0; op < 100; op++) {
                int t = rnd.nextInt(4);
                if (t == 0) { int u = rnd.nextInt(5), p = rnd.nextInt(4); ref.put(next, new int[] {u, p}); s.add(u, next++, p); }
                else if (t == 1 && !ref.isEmpty()) { int id = new ArrayList<>(ref.keySet()).get(rnd.nextInt(ref.size())); int p = rnd.nextInt(4); ref.get(id)[1] = p; s.edit(id, p); }
                else if (t == 2 && !ref.isEmpty()) { int id = new ArrayList<>(ref.keySet()).get(rnd.nextInt(ref.size())); ref.remove(id); s.rmv(id); }
                else if (t == 3) {
                    int best = -1;
                    for (int id : ref.keySet())
                        if (best == -1 || ref.get(id)[1] > ref.get(best)[1] || (ref.get(id)[1] == ref.get(best)[1] && id > best)) best = id;
                    int want = best == -1 ? -1 : ref.get(best)[0];
                    if (best != -1) ref.remove(best);
                    if (s.execTop() != want) throw new AssertionError("execTop");
                }
            }
        }
    }
}
```
