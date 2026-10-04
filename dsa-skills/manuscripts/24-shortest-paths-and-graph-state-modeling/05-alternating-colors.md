<!-- lesson-kind: standard -->
<!-- lesson-id: alternating-colors -->
## Alternating Colors

<!-- stage: context -->
### The Relay Box At Corran Valley

Tomasz keeps the layout for the Corran Valley Model Railway Club, a table-top system of six yards numbered 0 to 5. The yards are joined by one-way sections of track, and every section is painted either red or blue. Some yards have a short loop that leads back to the same yard, and a few yards are joined by two sections, one of each paint.

The old control box is the difficulty. Inside it sits a relay that clicks over each time the little shunter finishes a section, and the relay only accepts a section painted differently from the one just run. After a red section the shunter may enter only a blue one, and after a blue section only a red one, or the box jams and the whole table goes dark. On leaving yard 0 there is no earlier section, so either paint is allowed. For visiting children Tomasz wants to know, for each yard, the fewest sections the shunter must run to bring a wagon there from yard 0, or that the yard cannot be reached at all.

<!-- stage: naive -->
### Try Every Legal Route

The direct approach asks, for a limit of 0 sections, then 1, then 2 and so on, whether some legal route of at most that length ends at the wanted yard. The routine below walks every route in which each new section differs in paint from the previous one. The first limit that succeeds is the answer, and the cap of twice the number of yards is safe because a shortest route never arrives at the same yard with the same paint twice, and there are only 2n such arrivals.

```java
static boolean arrives(int[][] edges, int at, int lastPaint, int target, int left) {
    if (at == target) return true;
    if (left == 0) return false;
    for (int[] e : edges) {
        if (e[0] != at || e[2] == lastPaint) continue;
        if (arrives(edges, e[1], e[2], target, left - 1)) return true;
    }
    return false;
}

static int fewestSections(int[][] edges, int n, int target) {
    for (int limit = 0; limit <= 2 * n; limit++)
        if (arrives(edges, 0, -1, target, limit)) return limit;
    return -1;
}
```

Here `lastPaint` is -1 at the start so that either paint may leave yard 0, and red is 0 and blue is 1. This is correct on every layout, since it tries all legal routes in order of length, but it has to be run once for every yard Tomasz asks about.

<!-- stage: bottleneck -->
### Many Routes End In The Same Situation

If each yard has up to d sections leaving it, a search to depth L meets about d^L routes, and the loop over limits repeats every shallower search again. For six yards the cap is 12, so a layout with three sections out of every yard can cost around 3^12, more than half a million calls, per target yard. The cost is O(d^(2n)) per question, exponential in the number of yards.

Nearly all of that work is repeated. Two different routes may both finish at yard 3 after running a red section, and from that moment the same things are possible: only blue sections may leave, and they lead to the same places. The routes differ in how they got there, but the future depends on nothing except which yard the shunter is at and which paint it just ran. There are only 2n such situations, twelve in Tomasz's layout, yet the search treats each of its millions of routes as new. Whichever route reaches a situation first in order of length is the shortest, so every later route to it can be dropped the moment it is found.

<!-- stage: insight -->
### Pair The Yard With The Paint

The shunter's situation is not just a yard. Arriving at yard 3 over a red section and arriving over a blue one lead to different futures, so each is its own **state pair**: a yard together with the paint of the last section run. A layout with n yards therefore has 2n state pairs, and the search runs over those instead of over yards. The paint of a pair is simply the paint of the section just used to arrive. A state is written as yard times two plus paint, so it fits in one int and works as an array index.

From a state pair the **opposite-color rule** says which sections may leave: only those whose paint differs from the pair's paint, and each such section leads to the pair made of its far end and its own paint. All moves cost one section, so ordinary breadth-first order applies and the first time a pair is reached is its shortest distance. The answer for a yard is the smaller of its two pair distances, and a yard with neither reached is unreachable.

The beginning needs care, and this is **start seeding**. Before the first section there is no previous paint. When either paint may start, both pairs of yard 0 are placed in the queue at distance zero, which lets every section out of yard 0 be taken. When the first paint is fixed, only the pair that allows that paint is placed. The invariant is that the table entry for a pair holds the fewest sections of a legal route ending there with that paint, and no pair is ever queued twice.

<!-- names: state pair, opposite-color rule, start seeding -->

<!-- stage: variables -->
### Pairs, Distances And The Queue

The array `edges` holds sections as `{from, to, paint}` with 0 for red and 1 for blue. The array `dist` has 2n slots, where slot `2 * yard + paint` is the fewest sections for a route that ends at that yard with that paint, and -1 means not yet reached. The queue `frontier` holds encoded states that have a distance but have not been expanded. Inside the loop, `cur` is the state just removed, `cur / 2` is its yard and `cur % 2` its paint. A section is skipped when its paint equals `cur % 2`. A slot of `dist` is written exactly once, when the state is first discovered.

<!-- stage: trace -->
### Two Layouts, Two Start Rules

The first trace uses the contract of this lesson's last exercise: for each yard report the distance of a route that ends with a red section and of one that ends with a blue section. The layout has six yards, and the cells are the states in the order they leave the queue, written as the yard followed by r or b. The queue begins with 1r and 1b, the two sections out of yard 0, so yard 0 itself is not in it and no zero is ever recorded for it. The pointer `cur` is the position being expanded, and the vars give its distance, the number waiting and the number added. The search ends with yard 0 reached only by blue, after three sections.

```trace
{"cells":["1r","1b","2r","0b"],"pointers":["cur"],"steps":[{"at":{"cur":0},"vars":{"dist":1,"waiting":1,"added":0},"note":"State 1r is expanded at 1 section; no blue section leaves node 1 to an unreached state."},{"at":{"cur":1},"vars":{"dist":1,"waiting":1,"added":1},"note":"State 1b is expanded at 1 section; only red sections may leave it, and they add 2r."},{"at":{"cur":2},"vars":{"dist":2,"waiting":1,"added":1},"note":"State 2r is expanded at 2 sections; only blue sections may leave it, and they add 0b."},{"at":{"cur":3},"vars":{"dist":3,"waiting":0,"added":0},"note":"State 0b is expanded at 3 sections; no red section leaves node 0 to an unreached state."}]}
```

The second trace changes the start rule and the picture. Here the cells are the three yards themselves, the pointer `node` is the yard of the state being expanded, and both states of yard 0 begin in the queue at distance zero, as when either paint may start. The layout has a red loop on yard 0 and a blue loop on yard 1, plus two sections between yards 0 and 1 with different paint. The state 1b is created once, from 0r, and the blue loop on yard 1 later leads from 1r back to that known state, so it adds nothing.

```trace
{"cells":[0,1,2],"pointers":["node"],"steps":[{"at":{"node":0},"vars":{"state":"0r","dist":0,"waiting":2},"note":"State 0r is expanded at 0 sections; it adds 1b."},{"at":{"node":0},"vars":{"state":"0b","dist":0,"waiting":2},"note":"State 0b is expanded at 0 sections; it adds 1r."},{"at":{"node":1},"vars":{"state":"1b","dist":1,"waiting":2},"note":"State 1b is expanded at 1 section; it adds 2r."},{"at":{"node":1},"vars":{"state":"1r","dist":1,"waiting":1},"note":"State 1r is expanded at 1 section; nothing new can be reached from it."},{"at":{"node":2},"vars":{"state":"2r","dist":2,"waiting":0},"note":"State 2r is expanded at 2 sections; nothing new can be reached from it."}]}
```

<!-- stage: code -->
### Breadth-First Over Yard And Paint

```java
final class Shunting {
    static int[][] arrivals(int n, int[][] edges) {
        List<List<int[]>> out = new ArrayList<>();
        for (int i = 0; i < n; i++) out.add(new ArrayList<>());
        for (int[] e : edges) out.get(e[0]).add(new int[] {e[1], e[2]});
        int[] dist = new int[2 * n];
        Arrays.fill(dist, -1);
        ArrayDeque<Integer> frontier = new ArrayDeque<>();
        for (int[] s : out.get(0)) {
            int id = s[0] * 2 + s[1];
            if (dist[id] < 0) {
                dist[id] = 1;
                frontier.add(id);
            }
        }
        while (!frontier.isEmpty()) {
            int cur = frontier.poll();
            for (int[] s : out.get(cur / 2)) {
                if (s[1] == cur % 2) continue;
                int id = s[0] * 2 + s[1];
                if (dist[id] >= 0) continue;
                dist[id] = dist[cur] + 1;
                frontier.add(id);
            }
        }
        int[][] answer = new int[n][2];
        for (int v = 0; v < n; v++) {
            answer[v][0] = dist[2 * v];
            answer[v][1] = dist[2 * v + 1];
        }
        return answer;
    }
}
```

This version starts from the sections that leave yard 0 at distance one instead of queuing yard 0 at distance zero, because the answer is asked per last paint and a route with no section has none. Each section is examined once per paint of its start yard, so time is O(n + m) for m sections, and the two arrays and the queue take O(n + m) space.

<!-- stage: applicability -->
### When The Last Move Limits The Next

Look for a rule that ties the next move to the kind of the previous one: lanes that must alternate, a tool that must be swapped after each job, a bus that may not take two express legs in a row. The recognition cue is a graph whose edges carry a label, with a restriction that compares the label of the next edge to the label of the last. The invariant to keep is that the visited table is indexed by the whole situation, here yard and last paint, and that a state is marked only when it is first queued.

The false friend is the plain shortest-path BFS with one visited flag per yard. It looks right because the layout is an ordinary graph, but marking a yard from its first, red arrival can suppress a later blue arrival that is the only one allowed to continue, and a reachable yard is then reported as unreachable. The exercises build such a layout concretely.

Do not use this model when the restriction needs more history than the last label, for example no more than two red sections in a row, since the state must then also count the run length, or when the sections have unequal costs, which calls for a heap in place of a queue. In Java, `new int[n][2]` is filled with zeros, which read as distance zero, so every slot must be set to -1 first. An `int[]` placed in a `HashSet` is found only by identity, so equal contents are not matched; pack the state into one int instead.

<!-- stage: exercises -->
### Exercises

#### [Build] Alternate Red And Blue (Author exercise)
<!-- id: sp-alt-moves -->

**Prerequisites.** The move generator idea from the state-space BFS lesson, and the color-coded section list `{from, to, paint}` used in this lesson.

**Problem.** A model layout has sections stored in `edges`, where `edges[i] = {from, to, paint}` is a one-way section and paint is 0 for red or 1 for blue. The shunter stands at yard `v` and has just run a section of paint `last`, which is 0 or 1. Return an `int[][]` holding `{to, paint}` for each section that leaves `v` and whose paint differs from `last`, in the order the sections appear in `edges`. The input is not modified, and the result is empty when nothing may leave.

**Constraints.** 1 <= n <= 1000 yards numbered from 0, at most 5000 sections, and loops and parallel sections are allowed.

**Example 1.** Input `edges = [[0,1,0],[0,2,1],[0,3,0],[1,0,1],[0,0,1]], v = 0, last = 0`, output `[[2,1],[0,1]]`. With `last = 1` the output is `[[1,0],[3,0]]`.

**Example 2.** Input `edges = [[2,2,0],[2,2,1],[2,4,0],[3,2,1]], v = 2, last = 1`, output `[[2,0],[4,0]]`.

**Hint.** Which two conditions must a section satisfy, and what do the other sections of the layout contribute to the answer?

**Changed decision.** The allowed moves are chosen by comparing the paint of each section to the last paint, instead of by looking only at where the section leads.

#### [Vary] Two Start Modes (Author exercise)
<!-- id: sp-alt-start-modes -->

**Prerequisites.** The Alternate Red And Blue rung and breadth-first order over encoded states.

**Problem.** For a layout of `n` yards and sections `edges` as before, the shunter starts at yard 0 and must run alternating paints. The argument `first` is -1 when either paint may leave yard 0, 0 when the first section must be red and 1 when it must be blue. Return an `int[]` of length n whose entry for each yard is the fewest sections of a legal route that ends there, or -1 if there is none. Yard 0 always has 0, since the empty route is allowed. The input is not modified.

**Constraints.** 1 <= n <= 500, up to 4000 sections, and `first` is one of -1, 0, 1.

**Example 1.** Input `n = 6, edges = [[0,1,0],[1,2,0],[0,3,1],[3,2,1],[2,4,1],[4,1,0],[1,5,1]], first = -1`, output `[0,1,-1,1,-1,2]`.

**Example 2.** Input is the same layout with `first = 1`, output `[0,-1,-1,1,-1,-1]`.

**Hint.** Before the first section there is no last paint. Which states of yard 0 should the queue hold for each value of `first`, and at what distance?

**Changed decision.** The queue starts with the states that allow the permitted first paint, instead of with a single start state.

#### [Boundary] Self-Loop And Parallel Colors (Author exercise)
<!-- id: sp-alt-loops-parallel -->

**Prerequisites.** The Two Start Modes rung.

**Problem.** A club layout has `n` yards and sections `edges` of the form `{from, to, paint}`; a section may start and end at the same yard, and two sections may join the same two yards with the same or different paint. Given a start yard `s` and a target yard `t`, return the fewest sections in a non-empty route from `s` to `t` in which consecutive sections differ in paint, with either paint allowed first, or -1 if none exists. The yards `s` and `t` may be equal, and then the empty route does not count. The input is not modified.

**Constraints.** 1 <= n <= 200, up to 2000 sections, 0 <= s, t < n, and all entries valid.

**Example 1.** Input `n = 3, edges = [[0,0,0],[0,1,0],[0,1,1],[1,1,1],[1,2,0],[2,0,1]], s = 2, t = 2`, output `4`.

**Example 2.** Input is the same layout with `s = 0, t = 0`, output `1`.

**Hint.** Is a second section between the same two yards a duplicate when its paint differs, and what distance should a start state have if the empty route is forbidden?

**Changed decision.** Sections of different paint between the same yards are kept as separate moves, and the start yard is given no distance of its own.

#### [Recognize] Shortest Path with Alternating Colors (LeetCode 1129)
<!-- id: sp-alt-color-pairs -->

**Prerequisites.** The Self-Loop And Parallel Colors rung and the node-and-state search lesson. The input form follows the LeetCode statement, with separate red and blue arrays.

**Problem.** Yards are numbered 0 to n-1, and `redEdges` and `blueEdges` list one-way sections as `{from, to}`, which may include loops and repeats. A legal route starts at yard 0 and alternates paint between consecutive sections. This version changes the output: return an `int[n][2]` in which entry `v` is `{fewest sections of a legal route ending at v with a red section, fewest sections of one ending with a blue section}`, using -1 where no such route exists. Routes must contain at least one section, so yard 0 does not get a 0 unless a legal cycle exists. The arrays are not modified.

**Constraints.** 1 <= n <= 100, at most 400 sections of each paint, and all yard numbers are valid.

**Example 1.** Input `n = 5, redEdges = [[0,1],[2,3],[3,3]], blueEdges = [[1,2],[3,4],[2,0]]`, output `[[-1,-1],[1,-1],[-1,2],[3,-1],[-1,4]]`.

**Example 2.** Input `n = 6, redEdges = [[0,1],[1,2],[3,4],[2,3]], blueEdges = [[0,1],[2,0],[4,5],[3,3]]`, output `[[-1,3],[1,1],[2,-1],[-1,-1],[-1,-1],[-1,-1]]`.

**Hint.** If you place both states of yard 0 in the queue at distance zero, what does that claim about a route that uses no section, and which first layer avoids it?

**Changed decision.** Both distances of every yard are reported separately, and the search starts from the first layer of sections instead of from a zero-distance start state.
