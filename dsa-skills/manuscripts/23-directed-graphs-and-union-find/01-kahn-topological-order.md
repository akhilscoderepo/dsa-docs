<!-- lesson-kind: standard -->
<!-- lesson-id: kahn-topological-order -->
## Kahn Topological Order

<!-- stage: context -->
### Seven Steps For The Wardrobe

Tomasz has bought a flat-pack wardrobe for his daughter's room, and the instruction sheet is a poster of seven numbered boxes joined by arrows. Sort the screws and washers. Fit the four feet to the base. Join the two side panels to the base, which needs both the sorted screws and the fitted feet. Slide in the back panel and hang the rail for the shelves, each of which needs the joined sides. Hang the doors, which need the back panel and the rail. The seventh box, peeling the foam corners off the packed parts, has no arrows at all.

Tomasz is happy to follow any sequence that never starts a box before the boxes pointing at it are finished, but he wants to write it as one list on the back of the poster. His sister has a sheet for a bigger cabinet with forty boxes, and she suspects one of its arrows has been printed backwards. They would like a method that produces a working sequence for any poster, and says plainly when none exists.

<!-- stage: naive -->
### Rescan The Poster After Each Pick

The direct plan is to build the list one slot at a time. For each slot, go through every arrow on the poster and note which boxes still have an unfinished box pointing at them, then pick any unplaced box that is not noted, place it and move on. If no box is free while some are still unplaced, the poster has a loop and the answer is empty.

```java
static int[] orderByScanning(int n, int[][] edges) {
    int[] order = new int[n];
    boolean[] placed = new boolean[n];
    for (int slot = 0; slot < n; slot++) {
        boolean[] blocked = new boolean[n];
        for (int[] e : edges) {
            if (!placed[e[0]]) blocked[e[1]] = true;
        }
        int pick = -1;
        for (int v = 0; v < n && pick < 0; v++) {
            if (!placed[v] && !blocked[v]) pick = v;
        }
        if (pick < 0) return new int[0];
        placed[pick] = true;
        order[slot] = pick;
    }
    return order;
}
```

This is correct, because a box is placed only when every arrow into it comes from a placed box, and the scan fails only when every unplaced box has an unplaced predecessor, which means a loop. It is just slow on a big poster.

<!-- stage: bottleneck -->
### Every Pick Reads The Whole Poster

Each of the n slots reads all m arrows to rebuild the blocked marks, then walks all n boxes to find a free one, so the total is O(n * (n + m)). A poster with 100,000 boxes and 200,000 arrows needs about thirty billion steps, far past a few seconds, and a sheet that long is realistic for a build graph or a course catalogue.

The waste is plain. Placing one box can only change the situation for the boxes it points at, a handful of them, yet the method re-derives the status of every box from scratch. Most of the blocked marks it computes are identical to the ones it computed a moment ago. A method that kept a running count of unfinished predecessors for each box, and touched only the few counts that a placement changes, would read each arrow once in total and look at each box once, which is O(n + m).

<!-- stage: insight -->
### Count What Still Blocks Each Box

Keep, for every box, one number: how many arrows into it still come from boxes not yet placed. That number is the **indegree**, here the count of unresolved prerequisites. Computing it takes one pass over the arrows, adding one to the target of each. A box whose indegree is zero is free right now, so it may go into the list at once.

All the free boxes wait in the **ready queue**, a plain first-in first-out line. Seed it with every box of indegree zero, in ascending order, including boxes that have no arrows at all. Then repeat one move. Take the front box, write it into the list, and for each arrow leaving it subtract one from the target's indegree. When a target reaches zero, all its prerequisites are in the list, so it joins the back of the queue. Nothing else ever touches a count.

When the queue is empty the process ends, and there are two outcomes. If every box was written, the list is a valid order. If fewer were written, the boxes that never reached zero form the **stuck set**: each of them waits on another member of the set, directly or through a chain, so a loop sits inside it, and no order exists.

The invariant is that the indegree of each box equals its arrows from boxes not yet written, and the queue holds exactly the unwritten boxes whose count is zero. A box can enter the queue only once, because its count falls to zero only once.

<!-- names: indegree, ready queue, stuck set -->

<!-- stage: variables -->
### Counts, Queue And List

The int `n` is the number of boxes, numbered 0 to n-1, and `edges` holds one pair `{before, after}` for each arrow. The array `indegree` has one slot per box and is rebuilt inside the method, never taken from the caller. The list `after`, indexed by box, holds the targets of the arrows leaving it, so the loop does not search the whole poster. The queue `ready` holds boxes that are free but not yet written. The array `order` receives the boxes in the sequence they are removed, `done` is how many have been written, and `cur` is the box just taken from the front.

<!-- stage: trace -->
### One Clean Poster, One With A Loop

The first trace is the wardrobe poster with boxes 0 to 6 and arrows 0 to 2, 1 to 2, 2 to 3, 2 to 4, 3 to 5 and 4 to 5, with box 6 alone. The cells are the boxes in the order they are taken off the queue, and the pointer `cur` is the position of the one being removed. The vars show every box's indegree after that removal, written as seven numbers, and the queue as it stands. Box 2 enters the queue only after both 0 and 1 are gone, and box 5 waits for 3 and 4, so the order is 0, 1, 6, 2, 3, 4, 5.

```trace
{"cells":[0,1,6,2,3,4,5],"pointers":["cur"],"steps":[{"at":{"cur":0},"vars":{"indegree":"0 0 1 1 1 2 0","queue":"1 6"},"note":"Box 0 is removed and written to the list. It frees no new box."},{"at":{"cur":1},"vars":{"indegree":"0 0 0 1 1 2 0","queue":"6 2"},"note":"Box 1 is removed and written to the list. It frees box 2."},{"at":{"cur":2},"vars":{"indegree":"0 0 0 1 1 2 0","queue":"2"},"note":"Box 6 is removed and written to the list. It frees no new box."},{"at":{"cur":3},"vars":{"indegree":"0 0 0 0 0 2 0","queue":"3 4"},"note":"Box 2 is removed and written to the list. It frees box 3, 4."},{"at":{"cur":4},"vars":{"indegree":"0 0 0 0 0 1 0","queue":"4"},"note":"Box 3 is removed and written to the list. It frees no new box."},{"at":{"cur":5},"vars":{"indegree":"0 0 0 0 0 0 0","queue":"5"},"note":"Box 4 is removed and written to the list. It frees box 5."},{"at":{"cur":6},"vars":{"indegree":"0 0 0 0 0 0 0","queue":"empty"},"note":"Box 5 is removed and written to the list. It frees no new box."}]}
```

The second trace is a six-box sheet with arrows 0 to 1, 1 to 2, 2 to 3, 3 to 1, 0 to 4 and 4 to 5, where the arrows among 1, 2 and 3 form a loop. The cells are again the removal order, and the final step moves the pointer one past the last cell to mark the point where the queue ran dry. Boxes 1, 2 and 3 never reach zero, because each waits on the next in the loop, and the vars show their counts stuck at 1, so the process writes only three boxes and the answer is empty.

```trace
{"cells":[0,4,5],"pointers":["cur"],"steps":[{"at":{"cur":0},"vars":{"indegree":"0 1 1 1 0 1","queue":"4"},"note":"Box 0 is removed and written to the list. It frees box 4."},{"at":{"cur":1},"vars":{"indegree":"0 1 1 1 0 0","queue":"5"},"note":"Box 4 is removed and written to the list. It frees box 5."},{"at":{"cur":2},"vars":{"indegree":"0 1 1 1 0 0","queue":"empty"},"note":"Box 5 is removed and written to the list. It frees no new box."},{"at":{"cur":3},"vars":{"indegree":"0 1 1 1 0 0","queue":"empty"},"note":"The queue is empty with only 3 of 6 boxes written. Boxes 1, 2 and 3 still have indegree 1, so they form the stuck set and the answer is empty."}]}
```

<!-- stage: code -->
### Kahn's Method On Boxes And Arrows

```java
final class Planner {
    static int[] kahn(int n, int[][] edges) {
        int[] indegree = new int[n];
        List<List<Integer>> after = new ArrayList<>();
        for (int i = 0; i < n; i++) after.add(new ArrayList<>());
        for (int[] e : edges) {
            after.get(e[0]).add(e[1]);
            indegree[e[1]]++;
        }
        ArrayDeque<Integer> ready = new ArrayDeque<>();
        for (int v = 0; v < n; v++) {
            if (indegree[v] == 0) ready.add(v);
        }
        int[] order = new int[n];
        int done = 0;
        while (!ready.isEmpty()) {
            int cur = ready.poll();
            order[done++] = cur;
            for (int next : after.get(cur)) {
                if (--indegree[next] == 0) ready.add(next);
            }
        }
        return done == n ? order : new int[0];
    }
}
```

Each arrow is read once while building and once when its source is removed, and each box is queued and removed at most once, so the time is O(n + m) and the extra space is O(n + m) for the lists, the counts and the queue. The caller's `edges` is only read. Replacing the final test with a count of `done` gives the number of boxes that can be finished, which is what a feasibility question needs.

<!-- stage: applicability -->
### Orders From Prerequisites

Use this method whenever the input says that some things must come before others and the question asks for a valid sequence, how many items can be completed, or whether a sequence exists. Typical cases are course prerequisites, build targets, spreadsheet cells that read other cells and set-up steps for a machine. The recognition cue is a directed relation where an item may start only when everything pointing at it is done. The invariant to defend is that each count equals the unfinished predecessors, and the queue holds precisely the unwritten items with count zero.

The false friend is a sort of the labels. Writing the boxes in ascending number order looks like an order and often passes small tests, but an arrow from box 5 to box 2 puts 2 before one of its own prerequisites. Labels carry no information about the arrows, so only the counts can say what is free. A second trap is to seed the queue with only the first box of indegree zero, or to skip boxes without arrows, which loses whole parts of the poster.

Do not use it when the relation is undirected, since an edge then has no before and after, or when a unique answer is demanded without a tie-break rule, because the queue order decides which valid sequence comes out. In Java, `Collections.nCopies(n, new ArrayList<>())` fills the outer list with n references to a single inner list, so every box would share one set of targets. Build each inner list in a loop, and remember that `--indegree[next]` changes the value before the comparison with zero.

<!-- stage: exercises -->
### Exercises

#### [Build] Compute Indegrees (Author exercise)
<!-- id: ug-compute-indegrees -->

**Prerequisites.** The indegree array from this lesson, and the idea that an arrow points from before to after.

**Problem.** There are `n` vertices numbered 0 to n-1, and each row `edges[i] = {from, to}` is one directed arrow. Return an `int[]` of length n whose entry v is the number of arrows that end at v. A repeated arrow counts each time it appears, and an arrow from a vertex to itself counts once at that vertex. The `edges` array is not modified.

**Constraints.** 1 <= n <= 1000, at most 5000 arrows, and both ends of every arrow are valid vertices. Parallel arrows and self-loops are allowed.

**Example 1.** Input `n = 5, edges = [[0,1],[0,2],[3,2],[1,2],[0,1]]`, output `[0,2,3,0,0]`.

**Example 2.** Input `n = 4, edges = [[2,2],[1,3]]`, output `[0,0,1,1]`.

**Hint.** Which end of the pair is the one that gains a count, and what should a vertex with no incoming arrow show?

**Changed decision.** Only the target of an arrow is counted, instead of both ends as an undirected degree would do.

#### [Vary] Courses Finishable In Order (LeetCode 207)
<!-- id: ug-courses-completable -->

**Prerequisites.** The Compute Indegrees rung and the queue loop from the code stage.

**Problem.** There are `numCourses` courses numbered 0 to numCourses-1, and `prerequisites[i] = {a, b}` means course b must be taken before course a. Return the number of courses that can be completed one after another, each only after all its prerequisites are completed. That is the number of vertices removed by the zero-indegree process, so the answer equals numCourses exactly when no cycle exists. The `prerequisites` array is not modified.

**Constraints.** 1 <= numCourses <= 2000, up to 5000 pairs, and a pair may repeat. A pair `{a, a}` is allowed and blocks course a for good.

**Example 1.** Input `numCourses = 4, prerequisites = [[1,0],[2,1],[3,2]]`, output `4`.

**Example 2.** Input `numCourses = 5, prerequisites = [[1,0],[2,1],[1,2],[3,2],[4,3]]`, output `1`.

**Hint.** The pairs are written the other way round from the poster arrows, so which course is the source of the arrow? And what does the loop's final count say when the queue runs dry early?

**Changed decision.** The answer is the number of vertices removed, instead of a yes or no on whether all were removed.

#### [Boundary] Several Initial Sources (Author exercise)
<!-- id: ug-several-sources -->

**Prerequisites.** The Courses Finishable In Order rung.

**Problem.** Work proceeds in rounds. In each round, every vertex that has indegree zero at the start of the round is removed together, and the arrows leaving them are then subtracted. Return the number of rounds needed to remove all `n` vertices, or -1 if some vertex can never be removed. Isolated vertices and vertices with no incoming arrow all go in round one. Each row `edges[i] = {from, to}` is one arrow, and the array is not modified.

**Constraints.** 1 <= n <= 1000, at most 3000 arrows, and both ends are valid vertices. Arrows may repeat and may be self-loops.

**Example 1.** Input `n = 6, edges = [[0,1],[2,1],[1,3]]`, output `3`.

**Example 2.** Input `n = 4, edges = [[1,2],[2,1]]`, output `-1`.

**Hint.** Which vertices must be in the queue before the first removal, and how can you tell where one round ends and the next begins?

**Changed decision.** Every zero-indegree vertex is queued at the start and removed as one round, instead of being handled one at a time with no notion of rounds.

#### [Recognize] Course Order From Prerequisites (LeetCode 210)
<!-- id: ug-course-order -->

**Prerequisites.** The Several Initial Sources rung and the full Kahn loop from the code stage.

**Problem.** There are `numCourses` courses numbered 0 to numCourses-1, and `prerequisites[i] = {a, b}` means course b must come before course a. Return an `int[]` listing every course in an order that respects all pairs, or an empty array when no such order exists. Use a first-in first-out queue seeded with the zero-indegree courses in ascending order, so the result is deterministic. The `prerequisites` array is not modified.

**Constraints.** 1 <= numCourses <= 2000 and up to 5000 pairs, which may repeat. Courses with no pair at all must still appear in the result.

**Example 1.** Input `numCourses = 5, prerequisites = [[1,3],[4,1]]`, output `[0,2,3,1,4]`.

**Example 2.** Input `numCourses = 4, prerequisites = [[1,0],[2,1],[1,2],[3,0]]`, output `[]`.

**Hint.** For each pair, which course gains an indegree, and which list receives the other?

**Changed decision.** The removal order itself is returned, and an unfinished count means an empty result, instead of only counting the removed vertices.
