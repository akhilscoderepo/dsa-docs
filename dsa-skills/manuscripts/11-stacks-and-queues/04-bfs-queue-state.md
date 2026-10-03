<!-- lesson-kind: standard -->
<!-- lesson-id: bfs-queue-state -->
## BFS Queue State

<!-- stage: context -->
### Beacons On The Coast Road

A coast has a chain of signal beacons, and each beacon can pass a message to a few neighbouring beacons by lighting its lamp in a certain colour. The coastguard drops a message at one beacon and wants to know the fewest relays needed to reach a particular distant beacon. Each relay takes about a minute, so fewer relays means a faster warning.

The wiring is not a neat line. Beacon 2 might pass to both 3 and 4, and beacon 1 might also pass to 3, so there are several routes to the same beacon, some long and some short. A few beacons even relay back to ones that have already lit. The coastguard has the wiring list for every beacon, but she needs a method that finds the shortest chain without trying every route, and that never gets stuck passing a message round a loop.

<!-- stage: naive -->
### Try Every Route With A Depth Limit

The direct approach follows every possible chain of relays from the start. To stop it going round loops, it gives up on a chain once it is longer than the number of beacons, and it keeps the shortest one that reaches the target.

```java
static int fewestRelaysByRoutes(int[][] next, int from, int to, int budget) {
    if (from == to) return 0;
    if (budget == 0) return Integer.MAX_VALUE;
    int best = Integer.MAX_VALUE;
    for (int neighbour : next[from]) {
        int sub = fewestRelaysByRoutes(next, neighbour, to, budget - 1);
        if (sub != Integer.MAX_VALUE) best = Math.min(best, sub + 1);
    }
    return best;
}
```

It is correct if the budget is at least the number of beacons, because the shortest chain never repeats a beacon and so always fits inside the budget.

<!-- stage: bottleneck -->
### Routes Multiply Faster Than Beacons

If every beacon relays to b others and the budget is d, the search follows about b^d chains, which is O(b^d) work. With two relays per beacon and a budget of forty, that is over a trillion chains, even though there are only forty beacons. Most of those chains are repeats: the search arrives at beacon 3 by a short route and by a long route and explores everything beyond it again each time, with no memory that beacon 3 was already reached sooner.

The shortest chain to a beacon is found the first time any chain reaches it, if chains are explored in order of increasing length. Everything after that first arrival is a longer chain to the same place and can be ignored. A method that explores by length and remembers each beacon it has already reached touches every beacon once and every wire once, so it costs O(V + E) for V beacons and E wires.

<!-- stage: insight -->
### Explore By Length And Mark On Arrival

Keep the beacons that have been reached but not yet processed in a **frontier queue**. Start with the first beacon alone. Repeatedly remove the beacon at the front, look at its neighbours, and add each neighbour that has not been reached before to the back. Because the queue is first in first out, every beacon at distance k is processed before any beacon at distance k + 1, and so the first time the target is reached, the number of relays is as small as possible.

When a beacon counts as reached matters. The **discovery mark** is set at the moment the beacon is added to the queue, not at the moment it is removed. If the mark waited until removal, a beacon with two incoming wires could be added twice before its first copy reached the front, and every later beacon behind it would be explored twice, which can multiply the work again. Setting the mark at insertion guarantees that each beacon enters the queue at most once.

The invariant is that the queue holds exactly the reached but unprocessed beacons in nondecreasing order of distance, and every marked beacon has its final shortest distance recorded. The queue can only differ in distance by one from front to back, and this is what the **distance layer** structure captures: the front layer is processed completely before the next one starts to be processed. A stack in place of the queue still visits every beacon but follows one chain as deep as it can first, and the distance it records on arrival need not be the shortest.

<!-- names: frontier queue, discovery mark, distance layer -->

Building such a wiring list from a raw problem statement is a modelling step, and full graph modelling arrives later in the curriculum, so every exercise here supplies its neighbours directly.

<!-- stage: variables -->
### Queue, Marks And Distances

The array `dist` has one entry per beacon, filled with minus one to mean not yet reached, and a nonnegative entry is both the discovery mark and the shortest known distance. The queue `frontier` holds beacon numbers. `next[b]` lists the beacons that beacon `b` can pass to. For a numeric search with no wiring list, the successors are computed on the fly, and the state is bounded by a limit so that the number of possible states stays finite. The answer is read from `dist[target]` when the target is reached, or minus one if the queue empties first.

<!-- stage: trace -->
### Layers Grow Outward From The Start

The wiring has seven beacons, with beacon 0 passing to 1 and 2, beacon 1 to 3, beacon 2 to 3 and 4, beacon 3 to 5, and beacon 4 to 5 and 6. The target is beacon 5. The cells list the beacons, and `at` points at the one just removed from the queue. When beacon 2 is processed, beacon 3 is already marked, so it is not added a second time, and only beacon 4 joins the queue.

```trace
{"cells":[0,1,2,3,4,5,6],"pointers":["at"],"steps":[{"at":{"at":0},"vars":{"queue":"[1,2]"},"note":"Beacon 0 is removed. It adds [1, 2]."},{"at":{"at":1},"vars":{"queue":"[2,3]"},"note":"Beacon 1 is removed. It adds [3]."},{"at":{"at":2},"vars":{"queue":"[3,4]"},"note":"Beacon 2 is removed. It adds [4]. The beacon(s) [3] are already marked, so they are not added again."},{"at":{"at":3},"vars":{"queue":"[4,5]"},"note":"Beacon 3 is removed. It adds [5]."},{"at":{"at":4},"vars":{"queue":"[5,6]"},"note":"Beacon 4 is removed. It adds [6]. The beacon(s) [5] are already marked, so they are not added again."},{"at":{"at":5},"vars":{"queue":"[6]"},"note":"Beacon 5 is the target, so the search stops with the shortest distance."}]}
```

The second trace runs the same wiring with the mark set at removal instead of at insertion. Watch the queue after beacon 2 is processed: beacon 3 now appears twice, since its first copy has not reached the front yet. The duplicate has to be skipped or processed twice, and every beacon beyond it is exposed to the same repeat.

```trace
{"cells":[0,1,2,3,4,5,6],"pointers":["at"],"steps":[{"at":{"at":0},"vars":{"queue":"[1,2]"},"note":"Beacon 0 is removed. It adds [1, 2]."},{"at":{"at":1},"vars":{"queue":"[2,3]"},"note":"Beacon 1 is removed. It adds [3]."},{"at":{"at":2},"vars":{"queue":"[3,3,4]"},"note":"Beacon 2 is removed. It adds [3, 4]."},{"at":{"at":3},"vars":{"queue":"[3,4,5]"},"note":"Beacon 3 is removed. It adds [5]."},{"at":{"at":3},"vars":{"queue":"[4,5]"},"note":"Beacon 3 is removed again, but it was already processed, so the duplicate is skipped."},{"at":{"at":4},"vars":{"queue":"[5,5,6]"},"note":"Beacon 4 is removed. It adds [5, 6]."},{"at":{"at":5},"vars":{"queue":"[5,6]"},"note":"Beacon 5 is the target, so the search stops with the shortest distance."}]}
```

<!-- stage: code -->
### Distances, Doubling And Early Exit

```java
static int fewestRelays(int[][] next, int start, int target) {
    int[] dist = new int[next.length];
    Arrays.fill(dist, -1);
    ArrayDeque<Integer> frontier = new ArrayDeque<>();
    dist[start] = 0;
    frontier.addLast(start);
    while (!frontier.isEmpty()) {
        int b = frontier.removeFirst();
        if (b == target) return dist[b];
        for (int nb : next[b]) {
            if (dist[nb] == -1) {
                dist[nb] = dist[b] + 1;
                frontier.addLast(nb);
            }
        }
    }
    return -1;
}

static int addOneOrDoubleSteps(int start, int target, int limit) {
    int[] dist = new int[limit + 1];
    Arrays.fill(dist, -1);
    ArrayDeque<Integer> frontier = new ArrayDeque<>();
    dist[start] = 0;
    frontier.addLast(start);
    while (!frontier.isEmpty()) {
        int x = frontier.removeFirst();
        if (x == target) return dist[x];
        int[] successors = {x + 1, x * 2};
        for (int y : successors) {
            if (y <= limit && dist[y] == -1) { dist[y] = dist[x] + 1; frontier.addLast(y); }
        }
    }
    return -1;
}
```

Each state enters the queue at most once and each wire is examined once, so the time is O(V + E) and the space is O(V). The target test sits at removal, which keeps the distance final, and the numeric version replaces the wiring list by two computed successors.

<!-- stage: applicability -->
### When Distance Means Fewest Moves

Use a queue-driven search when states are explored in nondecreasing number of transitions from a start and every transition costs the same. The invariant is that the queue holds the discovered but unprocessed states in order of distance, and each state is marked when it is added.

A false friend is a stack, which reaches the target by some chain and need not reach it by the shortest one. A second false friend is the exhaustive route search, which is correct and exponential, because it forgets that a state was already reached sooner. A third is marking a state when it is removed, which allows duplicates into the queue and restores much of the repeated work.

In Java, store the mark in the distance array, so that a single comparison against minus one answers whether a state was reached. Check whether the start is the target before generating any successor. Bound numeric states with an explicit limit so the arrays have a finite size, and never put `null` into the deque to separate layers.

<!-- stage: exercises -->
### Exercises

#### [Build] Process A Supplied Frontier (Author exercise)
<!-- id: sq-supplied-frontier -->

**Prerequisites.** The Two-Stack Queue lesson.

**Problem.** States are numbered 0 to n - 1 and `next[s]` lists the successors of state `s`. Starting from `start`, repeatedly remove the state at the front of a queue and append its successors that have not been marked. Mark a state when it is appended. Return the states in the order they are removed.

**Constraints.** 1 <= n <= 100000, 0 <= start < n, every successor is between 0 and n - 1, and the total length of all successor lists is at most 200000.

**Example 1.** Input `next = [[1, 2], [3], [3], []], start = 0`, output `[0, 1, 2, 3]`.

**Example 2.** Input `next = [[0, 0]], start = 0`, output `[0]`.

**Hint.** When is a state marked, and what does a self-loop do to the queue?

**Changed decision.** First rung: the successors are given, so the only decision is to mark each state as it is appended and never again.

#### [Vary] Minimum Add-One Or Double Steps (Author exercise)
<!-- id: sq-add-one-or-double -->

**Prerequisites.** The Process A Supplied Frontier rung.

**Problem.** From a number `x` one step may produce `x + 1` or `2 * x`. Return the fewest steps from `start` to `target` when no number may exceed `limit`, or -1 if it cannot be reached.

**Constraints.** 0 <= start <= limit <= 1000000, 0 <= target <= limit.

**Example 1.** Input `start = 3, target = 10, limit = 100`, output `3`.

**Example 2.** Input `start = 5, target = 3, limit = 100`, output `-1`.

**Hint.** What are the states, and how many of them are there? Why is the limit needed?

**Changed decision.** The successors are computed from the state itself, and a bound on the state values keeps the search finite.

#### [Boundary] Start Is Target (Author exercise)
<!-- id: sq-start-is-target -->

**Prerequisites.** The Minimum Add-One Or Double Steps rung.

**Problem.** States are the numbers 0 to n - 1, and the successors of `x` are `(x + 2) % n` and `(x + 3) % n`. Search from `start` with a queue and stop at the moment `target` is removed from the queue. Return `[distance, enqueues]`, where `enqueues` counts every state ever appended, including the start, up to that moment. If `start` equals `target` return `[0, 1]` without generating successors. Return `[-1, e]` with the number `e` of states appended when the queue runs empty.

**Constraints.** 1 <= n <= 100000, 0 <= start < n and 0 <= target < n.

**Example 1.** Input `n = 7, start = 0, target = 4`, output `[2, 6]`.

**Example 2.** Input `n = 6, start = 2, target = 2`, output `[0, 1]`.

**Hint.** Is the target tested when a state is appended or when it is removed? What does a mark at insertion do to the count?

**Changed decision.** The target test happens before successors are generated, and the mark at insertion keeps the count of appended states at most n.

#### [Recognize] Shortest Word Transform From Supplied Neighbors (Author exercise)
<!-- id: sq-word-transform-neighbors -->

**Prerequisites.** The Start Is Target rung.

**Problem.** Words are numbered 0 to n - 1, and `neighbours[w]` lists the words that differ from word `w` by one letter, supplied for you. Return the number of words in the shortest chain from `begin` to `end`, counting both ends, or 0 if no chain exists.

**Constraints.** 1 <= n <= 5000, every neighbour index is between 0 and n - 1, and neighbour lists are symmetric.

**Example 1.** Input `neighbours = [[1], [0, 2, 4], [1, 3], [2], [1]], begin = 0, end = 3`, output `4`.

**Example 2.** Input `neighbours = [[1], [0], []], begin = 0, end = 2`, output `0`.

**Hint.** What is the distance from `begin` to `end` in transitions, and how does it relate to the number of words in the chain?

**Changed decision.** The queue invariant is used on a supplied neighbour list, and the answer counts words, which is the distance plus one.
