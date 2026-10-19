<!-- lesson-kind: standard -->
<!-- lesson-id: dynamic-rankings -->
## Dynamic Rankings

<!-- stage: context -->
### A Scoreboard That Sorts On Every Refresh

A game server keeps a score for each of 200,000 players. Matches end every few milliseconds, and each match adds points to a handful of players. The lobby screen shows the top 10 players and refreshes after every match. A developer stores the scores in a hash map. Each refresh copies all entries into a list, sorts the list and reads the first ten.

The refresh costs a full sort even though the screen needs only ten rows. The server spends most of its time ordering players that the screen never shows.

The same question appears in task queues, auction pages and search results. Scores change, and callers ask for the best few entries. This lesson asks how to keep the ranking sorted between calls, and what must hold true about the order so that a changed score never leaves a stale row behind.

<!-- stage: naive -->
### Sorting All Scores For Each Query

The direct design keeps a hash map from player id to score. A top query copies the map entries, sorts them by score, and adds up the first `k` values.

```java
final class NaiveBoard {
    private final java.util.Map<Integer, Long> score = new java.util.HashMap<>();

    void addScore(int player, long points) {
        score.merge(player, points, Long::sum);          // one hash operation per update
    }

    long top(int k) {
        java.util.List<Long> all = new java.util.ArrayList<>(score.values());
        all.sort(java.util.Collections.reverseOrder());   // sorts every player on every query
        long sum = 0;
        for (int i = 0; i < k; i++) sum += all.get(i);
        return sum;
    }
}
```

An update costs O(1). A top query costs O(n log n) for n players, whatever the value of `k`.

```predict
Players 1, 2 and 3 hold 50, 30 and 40 points. A caller asks for top(2) one million times between updates. How much sorting work is repeated, and what does a sorted structure save?

Every call sorts all three scores again and returns 90, so the same ordering is rebuilt one million times. A structure that stays sorted between updates reads two entries per query. The sort cost moves into the update, which touches one player.
```

<!-- stage: bottleneck -->
### Re-Sorting Unchanged Data

A top query reads `k` entries, yet it pays for sorting all n. The sort repeats work whenever two queries arrive without an update between them, and even one update changes only one position in the order.

A tree set that stays sorted fixes the repeated work. An update then costs O(log n) and a top query costs O(k + log n). The tree set brings two new risks.

The first risk is a comparator that sees two players as equal. A tree set treats entries that compare equal as the same entry, so a second player with the same score silently disappears. The second risk is a score change. The old entry sits in the tree under its old score. A removal that uses the new score does not find it, and the old row stays in the ranking.

<!-- stage: insight -->
### A Strict Order And An Exact Removal

The ranking is a **total order** on entries. A total order compares any two different entries as unequal. A score alone is not a total order, because two players can share a score. Adding the player id as the last comparison field makes every pair of entries comparable and distinct.

#### Naming The Tie Rule

The **tie policy** says which of two entries with equal scores ranks first. It is part of the problem, not an implementation detail. A problem that says "smaller name first" states a tie policy. The comparator must follow that statement field by field, and it must end with the id so the order stays total.

#### Removing The Right Entry

An update has to delete the **exact old key**, which is the entry built from the old score and the same id. The class reads the old score from its map, removes the entry that carries that score, writes the new score and inserts the new entry. Entries are immutable, so no field changes while an entry sits inside the tree.

The invariant is that the tree holds one entry per live player, and each entry carries that player's current score.

<!-- names: total order, tie policy, exact old key -->

<!-- stage: variables -->
### What The Class Stores

Two structures and one record type carry the state.

- **scoreOf** maps each player id to the current total and changes in every addScore and reset call.
- **board** is a tree set of entries ordered by higher score first and then by smaller id, and it changes in step with scoreOf.
- **Entry** is an immutable pair of score and id, and a new object replaces it on every change.

The top query reads from `board` and never writes to either structure.

<!-- stage: trace -->
### Following Updates And Queries

#### Scores That Add Up

The first trace follows six calls. Here the pointer `call` names the latest call, and each step lists the board from best to worst as `score:id`.

```trace
{"cells":["add(1,30)","add(2,30)","add(1,15)","add(3,40)","top(2)","reset(1)","top(2)"],"pointers":["call"],"steps":[{"at":{"call":0},"vars":{"board":"30:1","result":"null"},"note":"Call 0: player 1 is new, so the board gains 30:1."},{"at":{"call":1},"vars":{"board":"30:1 30:2","result":"null"},"note":"Call 1: player 2 is new, so the board gains 30:2."},{"at":{"call":2},"vars":{"board":"45:1 30:2","result":"null"},"note":"Call 2: the board removes 30:1 and inserts 45:1."},{"at":{"call":3},"vars":{"board":"45:1 40:3 30:2","result":"null"},"note":"Call 3: player 3 is new, so the board gains 40:3."},{"at":{"call":4},"vars":{"board":"45:1 40:3 30:2","result":"85"},"note":"Call 4: top(2) adds the first 2 rows of the board and returns 85."},{"at":{"call":5},"vars":{"board":"40:3 30:2 0:1","result":"null"},"note":"Call 5: the board removes 45:1 and inserts 0:1."},{"at":{"call":6},"vars":{"board":"40:3 30:2 0:1","result":"70"},"note":"Call 6: top(2) adds the first 2 rows of the board and returns 70."}]}
```

The third call is the one that moves a player. Player 1 holds 30, so the class removes the entry `30:1` and then inserts `45:1`. Player 1 now outranks player 2.

#### Players With The Same Score

The second trace starts three players with equal scores. The id decides the order, and an update then separates one of them.

```trace
{"cells":["add(9,10)","add(4,10)","add(7,10)","top(3)","add(7,5)","top(1)"],"pointers":["call"],"steps":[{"at":{"call":0},"vars":{"board":"10:9","result":"null"},"note":"Call 0: player 9 is new, so the board gains 10:9."},{"at":{"call":1},"vars":{"board":"10:4 10:9","result":"null"},"note":"Call 1: player 4 is new, so the board gains 10:4."},{"at":{"call":2},"vars":{"board":"10:4 10:7 10:9","result":"null"},"note":"Call 2: player 7 is new, so the board gains 10:7."},{"at":{"call":3},"vars":{"board":"10:4 10:7 10:9","result":"30"},"note":"Call 3: top(3) adds the first 3 rows of the board and returns 30."},{"at":{"call":4},"vars":{"board":"15:7 10:4 10:9","result":"null"},"note":"Call 4: the board removes 10:7 and inserts 15:7."},{"at":{"call":5},"vars":{"board":"15:7 10:4 10:9","result":"15"},"note":"Call 5: top(1) adds the first 1 rows of the board and returns 15."}]}
```

The three entries sit in the board together, because the id makes them compare unequal. A comparator on score alone would keep only the first of the three.

<!-- stage: code -->
### The Board In Java

The class stores entries in a tree set and sums the first `k` entries of an iterator.

```java
final class Leaderboard {
    private record Entry(long score, int id) {}
    private final java.util.Map<Integer, Long> scoreOf = new java.util.HashMap<>();
    private final java.util.TreeSet<Entry> board = new java.util.TreeSet<>((a, b) -> {
        int c = Long.compare(b.score(), a.score());          // higher score first; compare never subtracts
        return c != 0 ? c : Integer.compare(a.id(), b.id()); // id breaks ties, so the order is total
    });

    void addScore(int id, long points) {
        Long old = scoreOf.get(id);
        if (old != null) board.remove(new Entry(old, id));    // exact old key first
        long now = (old == null ? 0 : old) + points;
        scoreOf.put(id, now);
        board.add(new Entry(now, id));                        // then the new key
    }

    long top(int k) {
        long sum = 0;
        for (Entry e : board) {                               // iterator walks in rank order
            if (k-- == 0) break;
            sum += e.score();
        }
        return sum;
    }
}
```

An update costs O(log n), because it does one removal and one insertion. A top query costs O(k), because the iterator starts at the first entry. The space is O(n).

<!-- stage: applicability -->
### Choosing A Sorted Set For Rankings

#### Checking The Comparator

Before you write the set, say the order aloud, one field at a time. The last field must be unique, and the comparison of every field must use `Integer.compare` or `Long.compare`. The invariant is that no two live entries compare equal, and every entry matches current state.

#### Rank Queries By Position

A top-`k` sum or a name list needs only the first `k` entries, so an iterator is enough. A query for the rank of one player is different. A tree set cannot report a position without a scan. That question needs a Fenwick tree or an order-statistic structure.

#### False Friends

A tree map keyed by score alone looks like a ranking, but it is a false friend, because it holds one player per score. A priority queue looks like a ranking too. It exposes only the best entry, and removing an arbitrary entry costs O(n). Skip the sorted set when only the single best entry matters and scores never decrease, because one variable is enough there.

<!-- stage: exercises -->
### Exercises

#### [Build] Design A Leaderboard (LeetCode 1244)
<!-- id: ci40-leaderboard -->

**Prerequisites.** The multi-index lesson and tree sets.

**Problem.** Design a class `Leaderboard`. The call `addScore(playerId, score)` adds `score` to the player's total and creates the player with that total if the player is new. The call `top(K)` returns the sum of the `K` highest totals. The call `reset(playerId)` sets that player's total to 0 and keeps the player on the board.

**Constraints.** The limits are:
- **Players** have integer ids from 1 to 10^4.
- **Scores** satisfy `1 <= score <= 100`, and totals fit in a `long`.
- **K** satisfies `1 <= K <=` the number of players, and `reset` names an existing player.
- **Calls** number at most 1000.

**Example 1.** Input calls `addScore(1,50)`, `addScore(2,30)`, `addScore(3,40)`, `top(2)`, output 90.

**Example 2.** Input the same calls, then `addScore(2,25)`, `reset(1)`, `top(2)`, output 95, from totals 55 and 40.

**Hint.** Which entry must leave the set before a total changes?

**Changed decision.** A changing total forces the old entry out of the set, so the set must locate it by the old total.

#### [Vary] Sequentially Ordinal Rank Tracker (LeetCode 2102)
<!-- id: ci40-rank-tracker -->

**Prerequisites.** The leaderboard exercise above.

**Problem.** Design a class `RankTracker`. The call `add(name, score)` inserts a location with a unique name. The call `get()` returns the name of the location at rank `i`, where `i` is the number of `get` calls so far including this one. Rank 1 is the highest score, and equal scores rank by the smaller name first.

**Constraints.** The limits are:
- **Names** are distinct lowercase strings of length 1 to 10.
- **Scores** satisfy `1 <= score <= 10^5`.
- **Calls** number at most `10^5`, and every `get` has at least `i` locations.
- **Return** of `get` is a name.

**Example 1.** Input calls `add(a,3)`, `add(b,5)`, `get()`, `add(c,4)`, `get()`, output `b` and then `c`.

**Example 2.** Input calls `add(x,1)`, `add(y,1)`, `get()`, `get()`, output `x` and then `y`.

**Hint.** Split the entries into the ones already returned and the rest. What must hold between the two halves?

**Changed decision.** The query position grows with each call, so one half only gains entries and the other half hands over its best.

#### [Boundary] Equal Scores And Renames (Author exercise)
<!-- id: ci40-equal-renames -->

**Prerequisites.** The two exercises above.

**Problem.** Design a class `NameBoard`. The call `add(id, name, score)` registers a player with a unique id. Names are not unique. The call `rename(id, newName)` changes the name of a registered player. The call `topNames(k)` returns the names of the `k` best players, ordered by higher score, then smaller name, then smaller id.

**Constraints.** The limits are:
- **Ids** are distinct integers from 1 to 10^5.
- **Names** are lowercase strings of length 1 to 8, and two players may share a name.
- **Scores** satisfy `0 <= score <= 100`, and many players may share a score.
- **k** satisfies `1 <= k <=` the number of players.

**Example 1.** Input calls `add(1,sam,10)`, `add(2,sam,10)`, `topNames(2)`, output `sam`, `sam`.

**Example 2.** Input calls `add(1,zed,5)`, `add(2,amy,5)`, `rename(1,abe)`, `topNames(2)`, output `abe`, `amy`.

**Hint.** What does a comparator that stops after the name do with two players called `sam`?

**Changed decision.** Equal names and scores must stay distinct entries, so the id joins the comparator.

#### [Recognize] Design Task Manager (LeetCode 3408)
<!-- id: ci40-task-manager -->

**Prerequisites.** All three exercises above.

**Problem.** The contract below belongs to this chapter and can differ from the LeetCode text in detail. Design a class `TaskManager` built from tasks `{userId, taskId, priority}`. The call `add(userId, taskId, priority)` adds a task with a new `taskId`. The call `edit(taskId, newPriority)` changes the priority of an existing task. The call `rmv(taskId)` deletes a task. The call `execTop()` removes the task with the highest priority, breaking ties by the larger `taskId`, and returns its `userId`, or -1 when no task exists.

**Constraints.** The limits are:
- **Tasks** number at most `10^5` at any time, and each `taskId` is unique among live tasks.
- **Priority** satisfies `0 <= priority <= 10^9`.
- **Calls** number at most `2 * 10^5`, and `edit` and `rmv` name live tasks.
- **Return** of `execTop` is an `int`.

**Example 1.** Input tasks `{1,101,5}`, `{2,102,9}`, `{3,103,9}` and two `execTop()` calls, output 3 and then 2.

**Example 2.** Input tasks `{1,101,5}`, `{2,102,9}` and the calls `edit(101,12)`, `execTop()`, `rmv(102)`, `execTop()`, output 1 and then -1.

**Hint.** Which fields form the comparator, and which structure reads the old priority?

**Changed decision.** Execution removes the best entry, so it also removes the record from the map.
