<!-- lesson-kind: standard -->
<!-- lesson-id: dfs-topological-state -->
## DFS Topological State

<!-- stage: context -->
### Twelve Rooms In The Clock Museum

Odile Brandt guides school groups through the Fennel Street Clock Museum, and next month she has to lead a class of eleven-year-olds through all twelve rooms in one sensible sweep. The building is a tangle of corridors, but every doorway has a small brass plate, and each plate names the rooms that build on the room you are standing in. The Springs room's plate names the Escapement room, because you cannot appreciate how a clock ticks until you have seen what drives it. The Escapement plate names the Pendulum Hall and the Watch Bench, and so on across the floor.

Her rule is simple. No room may be shown before a room it builds on has been shown. She wants a list of all twelve rooms in an order that obeys every plate, and she wants a clear answer if the plates contradict each other, because a previous curator once wrote one that sent visitors round in a circle. She has a stub of blue chalk in her pocket for marking doorframes while she walks the building with a clipboard, though she has not yet decided what the marks should mean.

<!-- stage: naive -->
### Keep Picking Any Ready Room

The first idea is to build the tour one room at a time. Look through the rooms that are not yet on the list, find one whose every predecessor is already on it, append that room, and start the search again. When a full search finds no ready room, stop.

```java
static int[] tourByRescanning(int n, int[][] plates) {
    boolean[] placed = new boolean[n];
    int[] tour = new int[n];
    int count = 0;
    while (count < n) {
        int pick = -1;
        for (int room = 0; room < n && pick < 0; room++) {
            if (placed[room]) continue;
            boolean ready = true;
            for (int[] plate : plates)
                if (plate[1] == room && !placed[plate[0]]) { ready = false; break; }
            if (ready) pick = room;
        }
        if (pick < 0) return new int[0];
        placed[pick] = true;
        tour[count++] = pick;
    }
    return tour;
}
```

This is correct. A room enters the list only when everything it builds on is already there, so the list obeys every plate. If no room is ready, every remaining room is waiting on another remaining room, and following those waits must eventually repeat, which is a loop, so the empty answer is honest.

<!-- stage: bottleneck -->
### Every Pick Rereads Every Plate

Testing one room against the plates costs a pass over all m plates, the search tests up to n rooms, and the list needs n picks. That makes O(n^2 * m) in the worst case. With two thousand rooms and six thousand plates, that is about 2.4 * 10^10 comparisons, far too many for a museum database, and a real exhibition hall network has more doors than that.

Almost all of that rereading finds out what an earlier pick already knew. Whether the Pendulum Hall is ready is settled the instant the Escapement room is placed, yet each later search asks every plate again from scratch. The method also forgets where it is in the building. It jumps to whichever room happens to pass the test, so it never follows a corridor to its end, and when the plates do contradict each other it can only say that nothing is ready, with no hint of which rooms form the circle. A better method should walk the corridors themselves, touch each room and plate a fixed number of times, and let the walk itself reveal both a valid order and a loop.

<!-- stage: insight -->
### Chalk On The Way In And Out

Walk depth first from any room and chalk each doorframe twice. A slash when you walk in turns the room **gray**, which means it is open: you are somewhere beneath it and have not finished its plate. A second slash when you leave makes an X, so the room is **black**, which means finished. Rooms you have never entered carry no chalk. The moment a room turns black is the key event, because a room only turns black after every room it leads to has itself been entered and finished. At that instant all of its followers are already sitting on the list you are building.

That suggests writing the rooms down in the order they finish, which is called the **postorder**. The first finisher has nothing after it, the next has only that room, and each room joins the list behind everything it must precede. Read the finishing sequence backwards and every plate is obeyed, which is the **reversal** of the postorder. Filling the answer array from its last slot toward its first does the reversal for free.

Every door you test lands on one of three colors. A white room is a new corridor, so walk in. A gray room means you are still inside it and just found a door leading back, so the rooms between it and here form a circle, and no order exists. A black room is the quiet case: you reached a room that another branch already finished, a **cross edge** in the usual vocabulary, and it changes nothing because that room is already on the list. The invariant is that the gray rooms always form one unbroken corridor from the start of this walk to the current room.

<!-- names: postorder, reversal, cross edge -->

<!-- stage: variables -->
### Chalk, Doors And The Slot

The array `chalk` holds 0 for a room never entered, 1 for a gray room and 2 for a black one. The list `doors` stores, for every room, the rooms named on its plate, sorted ascending so that the walk is the same every time. The variable `room` is the room being walked and `next` is the plate entry under test. The array `tour` is the answer, and the integer `slot` is the next position to fill, starting at n and counting down. The flag `loop` turns true the first time a door lands on a gray room, and from then on every call returns at once.

<!-- stage: trace -->
### One Clean Walk And One Loop

The first trace walks a museum of six rooms with plates 0 to 1, 0 to 2, 1 to 3, 2 to 3, 2 to 4, 3 to 5 and 4 to 3. The cells are the rooms and the pointer `room` marks where the walk currently stands. Each step is an event: a room turning gray, a room turning black and landing in a slot, or a door that leads to a room already black. Watch the door from 2 to 3. Room 3 was finished on the way down from room 1, so the walk simply notes it and moves on, and the count of open rooms shows that nothing went wrong. The final list is the finishing sequence read backwards.

```trace
{"cells":[0,1,2,3,4,5],"pointers":["room"],"steps":[{"at":{"room":0},"vars":{"open":1,"listed":0},"note":"Room 0 turns gray: the walk enters it."},{"at":{"room":1},"vars":{"open":2,"listed":0},"note":"Room 1 turns gray: the walk enters it."},{"at":{"room":3},"vars":{"open":3,"listed":0},"note":"Room 3 turns gray: the walk enters it."},{"at":{"room":5},"vars":{"open":4,"listed":0},"note":"Room 5 turns gray: the walk enters it."},{"at":{"room":5},"vars":{"open":3,"listed":1},"note":"Room 5 turns black and is listed in slot 5."},{"at":{"room":3},"vars":{"open":2,"listed":2},"note":"Room 3 turns black and is listed in slot 4."},{"at":{"room":1},"vars":{"open":1,"listed":3},"note":"Room 1 turns black and is listed in slot 3."},{"at":{"room":2},"vars":{"open":2,"listed":3},"note":"Room 2 turns gray: the walk enters it."},{"at":{"room":2},"vars":{"open":2,"listed":3},"note":"The door from 2 to 3 leads to black room 3, already finished by another branch; it is accepted and ignored."},{"at":{"room":4},"vars":{"open":3,"listed":3},"note":"Room 4 turns gray: the walk enters it."},{"at":{"room":4},"vars":{"open":3,"listed":3},"note":"The door from 4 to 3 leads to black room 3, already finished by another branch; it is accepted and ignored."},{"at":{"room":4},"vars":{"open":2,"listed":4},"note":"Room 4 turns black and is listed in slot 2."},{"at":{"room":2},"vars":{"open":1,"listed":5},"note":"Room 2 turns black and is listed in slot 1."},{"at":{"room":0},"vars":{"open":0,"listed":6},"note":"Room 0 turns black and is listed in slot 0. The tour is [0, 2, 4, 1, 3, 5]."}]}
```

The second trace uses five rooms with plates 0 to 1, 1 to 2, 2 to 3, 3 to 1 and 0 to 4. The walk goes down the corridor 0, 1, 2, 3 and then tries the door from 3 back to 1. Room 1 is gray at that moment, so the corridor 1, 2, 3 and this door close a circle. The walk stops there, room 4 is never entered, and the answer is the empty list.

```trace
{"cells":[0,1,2,3,4],"pointers":["room"],"steps":[{"at":{"room":0},"vars":{"open":1,"listed":0},"note":"Room 0 turns gray: the walk enters it."},{"at":{"room":1},"vars":{"open":2,"listed":0},"note":"Room 1 turns gray: the walk enters it."},{"at":{"room":2},"vars":{"open":3,"listed":0},"note":"Room 2 turns gray: the walk enters it."},{"at":{"room":3},"vars":{"open":4,"listed":0},"note":"Room 3 turns gray: the walk enters it."},{"at":{"room":3},"vars":{"open":4,"listed":0},"note":"The door from 3 to 1 leads to gray room 1, so the gray corridor plus this door is a circle; no order exists. The answer is the empty list."}]}
```

<!-- stage: code -->
### A Depth-First Tour Planner

```java
final class MuseumTour {
    private static final int WHITE = 0, GRAY = 1, BLACK = 2;
    private final List<List<Integer>> doors = new ArrayList<>();
    private final int[] chalk;
    private final int[] tour;
    private int slot;
    private boolean loop;

    MuseumTour(int n, int[][] plates) {
        for (int i = 0; i < n; i++) doors.add(new ArrayList<>());
        for (int[] p : plates) doors.get(p[0]).add(p[1]);
        for (List<Integer> d : doors) Collections.sort(d);
        chalk = new int[n];
        tour = new int[n];
        slot = n;
    }

    private void visit(int room) {
        chalk[room] = GRAY;
        for (int next : doors.get(room)) {
            if (chalk[next] == GRAY) { loop = true; return; }
            if (chalk[next] == WHITE) {
                visit(next);
                if (loop) return;
            }
        }
        chalk[room] = BLACK;
        tour[--slot] = room;
    }

    int[] plan() {
        for (int r = 0; r < chalk.length && !loop; r++)
            if (chalk[r] == WHITE) visit(r);
        return loop ? new int[0] : tour;
    }
}
```

The loop that starts walks in ascending order of room number and the sorted plates make the answer reproducible. Each room is entered once and each plate is looked at once, so the time is O(n + m) plus the sort of the plates, and the space is O(n + m) for the lists, with the recursion adding up to n frames on top.

<!-- stage: applicability -->
### When Finishing Order Is The Answer

Reach for this walk when the input is a directed graph and the question is about order or loops: build orders, course plans, spreadsheet cells that read other cells, import statements, anything where a thing must wait for the things it depends on. The recognition cue is the pair of words "before" and "directed". The invariant to defend is that gray rooms are exactly the current corridor, so only a door into gray proves a loop, and a room is listed only at the moment it turns black.

The nearest false friend is the visited flag from undirected cycle detection. With a single boolean, a diamond of rooms, where two corridors meet at a shared final room, looks like a loop the moment the second corridor arrives, and a perfectly good plan is rejected. A second false friend is listing rooms on entry instead of on exit. For plates 0 to 1, 0 to 2 and 2 to 1, entry order gives 0, 1, 2, which puts room 1 before room 2 even though room 2 must come first.

Do not use it when the graph is undirected, where the parent edge matters instead, or when the task asks for the smallest order alphabetically or a layer-by-layer schedule, which the queue method of the previous lesson gives directly. In Java the hazard is the call stack. A recursive walk down a chain of one hundred thousand rooms throws `StackOverflowError`, since the default stack holds only some thousands of frames. Use an explicit stack with a per-room position, or run the walk in a thread created with a larger stack size.

<!-- stage: exercises -->
### Exercises

#### [Build] Three-Color Trace (Author exercise)
<!-- id: ug-three-color-trace -->

**Prerequisites.** The chalk marks from this lesson, and an adjacency list with sorted neighbours.

**Problem.** A directed acyclic graph has `n` vertices labelled 0 to n - 1, and `edges` holds pairs `[from, to]`. Run a depth-first search that starts new walks from vertices 0, 1, 2, and so on, taking only those still unvisited, and follows the out-neighbours of each vertex in ascending order of label. A clock starts at 0. Every time a vertex turns gray it receives the clock value as its entry time, and every time it turns black it receives the clock value as its exit time, and the clock goes up by one after each of those two events. Return an `int[2][n]`, with entry times in row 0 and exit times in row 1. The input is not modified.

**Constraints.** 1 <= n <= 1000, 0 <= edges.length <= 3000, the graph has no directed cycle, and parallel edges may appear.

**Example 1.** Input `n = 5, edges = [[0,1],[0,2],[1,3],[2,3],[3,4]]`, output `[[0,1,7,2,3],[9,6,8,5,4]]`.

**Example 2.** Input `n = 6, edges = [[4,1],[4,0],[0,3],[1,3],[2,5]]`, output `[[0,4,6,1,10,7],[3,5,9,2,11,8]]`.

**Hint.** Where in the visit does the clock tick for gray, and where for black, and does a vertex that is already black tick it again?

**Changed decision.** Time is recorded at two moments of each visit, entry and exit, instead of only when a vertex is first discovered.

#### [Vary] Postorder Topological List (Author exercise)
<!-- id: ug-postorder-list -->

**Prerequisites.** The Three-Color Trace rung.

**Problem.** The graph is acyclic and given as `n` and `edges` of pairs `[from, to]`, where `from` must appear before `to`. Return an `int[]` holding every vertex exactly once so that every edge's source comes earlier than its target. To make the answer unique, start walks from 0 upward, follow out-neighbours in ascending order, append a vertex to a list only after all its out-neighbours are done, and return that list reversed. The inputs are not modified.

**Constraints.** 1 <= n <= 50000, 0 <= edges.length <= 100000, there is no directed cycle, and a chain of vertices can be n long.

**Example 1.** Input `n = 6, edges = [[5,2],[5,0],[4,0],[4,1],[2,3],[3,1]]`, output `[5,4,2,3,1,0]`.

**Example 2.** Input `n = 5, edges = [[3,1],[3,1],[1,0],[4,2]]`, output `[4,3,2,1,0]`.

**Hint.** The answer is built backwards. What must be true of every out-neighbour of a vertex at the moment that vertex is appended, and what does a chain of 50000 vertices do to the call stack?

**Changed decision.** The output records only the finishing order, reversed, instead of both entry and exit times.

#### [Boundary] Cross Edge To Black (Author exercise)
<!-- id: ug-cross-edge-black -->

**Prerequisites.** The Postorder Topological List rung.

**Problem.** The directed graph may contain cycles, self loops and parallel edges. Run the same walk as before, with walks started from 0 upward and out-neighbours taken in ascending order, and classify each entry of `edges` at the moment the walk tests it by the colour of its target: white, gray or black. A test that finds a white target counts as a white edge and then walks into it. Return an `int[3]` holding the number of white, gray and black tests, in that order. The walk does not stop at the first loop, and a gray test is a loop, which includes a self loop. The input is not modified.

**Constraints.** 1 <= n <= 1000, 0 <= edges.length <= 5000, and parallel edges and self loops are allowed, each counted as its own test.

**Example 1.** Input `n = 4, edges = [[0,1],[0,2],[1,3],[2,3]]`, output `[3,0,1]`.

**Example 2.** Input `n = 5, edges = [[0,1],[1,2],[2,1],[2,2],[0,3],[3,4],[0,4],[0,1]]`, output `[4,2,2]`.

**Hint.** When the second path reaches the shared vertex, has the walk come back to a vertex it is still inside, or to one it has already left?

**Changed decision.** A door into a black vertex is accepted and counted, instead of being treated as a sign of a loop.

#### [Recognize] Course Schedule II (LeetCode 210)
<!-- id: ug-course-schedule-dfs -->

**Prerequisites.** The Cross Edge To Black rung.

**Problem.** There are `numCourses` courses labelled 0 to numCourses - 1, and each entry `[a, b]` of `prerequisites` means course `b` must be taken before course `a`. Return an `int[]` order that takes every course exactly once and respects every entry, or an empty array when no such order exists. Use a depth-first search that starts walks from course 0 upward and follows the courses that depend on the current one in ascending order, so the reference answer is the reverse of the finishing sequence. Stop and return the empty array the moment a door leads into a gray course. The input is not modified.

**Constraints.** 1 <= numCourses <= 2000, 0 <= prerequisites.length <= 5000, all pairs are distinct, and a course never lists itself.

**Example 1.** Input `numCourses = 5, prerequisites = [[1,4],[2,4],[3,1],[3,2],[0,3]]`, output `[4,2,1,3,0]`.

**Example 2.** Input `numCourses = 4, prerequisites = [[1,0],[2,1],[1,2],[3,0]]`, output `[]`.

**Hint.** An entry lists the dependent course first. Which way must the door between the two courses point for the finishing order to come out with prerequisites first after reversing?

**Changed decision.** The edge direction is read from the pair as prerequisite to dependent, and a gray target ends the whole search with an empty answer instead of continuing.
