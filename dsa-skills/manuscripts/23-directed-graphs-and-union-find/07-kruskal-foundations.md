<!-- lesson-kind: standard -->
<!-- lesson-id: kruskal-foundations -->
## Kruskal Foundations

<!-- stage: context -->
### Pipes For The Marrowdale Villages

Ilse is the engineer of the Marrowdale Water Board, and the board has funds to bring a pipe supply to eleven hill villages that currently carry water from wells. Only a few routes between villages are even possible, because the ground has to be passable for a trench, and a surveyor has quoted a price for each possible route. Water entering any one village must be able to reach all the others, directly or through villages in between. Nobody cares which route a drop takes. The board only wants every village joined, and joined for the smallest total of quotes.

A pipe that is laid is paid for whether or not anyone needed it. Ilse has noticed that a hasty plan wastes money in two different ways. It can lay a pipe between two villages that already share water through some other path, which is pure waste, and it can lay so many cheap pipes in one valley that the money runs out before the far villages are reached. She wants a rule she can apply to a list of quotes, and she wants to know that the answer is truly the cheapest and not merely a decent one.

<!-- stage: naive -->
### Try Every Choice Of Pipes

A network that joins all V villages with the least money needs exactly V - 1 pipes. Fewer cannot reach everyone, and with prices that are never negative a spare pipe only adds cost. So the plain method tries every selection of V - 1 quoted routes, discards the selections that leave some village cut off, adds up the prices of the others and keeps the smallest total.

```java
static boolean linksAll(int n, int[][] routes, int mask) {
    int reached = 1;
    boolean grew = true;
    while (grew) {
        grew = false;
        for (int i = 0; i < routes.length; i++) {
            if ((mask >> i & 1) == 0) continue;
            boolean a = (reached >> routes[i][0] & 1) == 1;
            boolean b = (reached >> routes[i][1] & 1) == 1;
            if (a != b) { reached |= 1 << routes[i][0] | 1 << routes[i][1]; grew = true; }
        }
    }
    return reached == (1 << n) - 1;
}

static long cheapestBySelection(int n, int[][] routes) {
    long best = -1;
    for (int mask = 0; mask < (1 << routes.length); mask++) {
        if (Integer.bitCount(mask) != n - 1 || !linksAll(n, routes, mask)) continue;
        long cost = 0;
        for (int i = 0; i < routes.length; i++) if ((mask >> i & 1) == 1) cost += routes[i][2];
        if (best < 0 || cost < best) best = cost;
    }
    return best;
}
```

This is correct, because it looks at every candidate and the check for reaching all villages starts from village 0 and spreads along chosen pipes until nothing new is reached. It answers -1 when no selection links everyone. It also works for tiny valleys, which is all that Ilse's first sketch needed.

<!-- stage: bottleneck -->
### Too Many Selections To Inspect

The loop visits 2^E masks for E quoted routes, and the ones with exactly V - 1 bits set number C(E, V - 1), each checked in O(E * V) by the spreading test. The Marrowdale survey has 40 possible routes among 15 villages, and C(40, 14) is about 23 billion selections. A district with a hundred routes is far beyond any machine. The cost is exponential in the number of routes, so every added quote multiplies the work.

Nearly all of that work is wasted on selections that are obviously poor, such as ones that pick a route between two villages already linked by two other chosen routes. The search never learns anything from a bad selection. What is needed is a rule that decides about one route at a time, using only what has been laid so far, and never has to reconsider. The question is what fact about a single quote can justify laying it for good.

<!-- stage: insight -->
### The Cheapest Crossing Is Always Allowed

Pick any way of splitting the villages into two groups, and look at the pipes that cross from one group to the other. The **cut property** says that the cheapest crossing pipe belongs to some cheapest network. The reasoning is an exchange. Take a cheapest network that lacks this pipe. It must still cross the split somewhere, so adding the pipe closes a loop that passes over the split a second time, and removing the other crossing pipe on that loop restores a network. That pipe cost at least as much, so nothing got dearer. When two crossings tie, some cheapest network contains one of them, and a fixed tie rule picks which.

Now run through the quotes from cheapest to dearest, which is the **sorted sweep**, and keep a record of which villages are already joined by laid pipes. When the sweep reaches a quote whose two villages lie in different groups, take the group of one end and split it off from everything else. Any pipe crossing that split and cheaper than this quote would have been reached earlier, and it would have joined two groups already, so no such pipe crosses. This quote is the cheapest crossing, which makes it a **safe edge**: laying it can never rule out a cheapest network. A quote whose ends are already in one group is skipped, since it would only close a loop. The algorithm built on this is named after Kruskal.

The invariant is that the laid pipes form a loop-free set that sits inside some cheapest network. Each accepted quote keeps that true by the cut argument, and each skipped quote leaves it untouched. After V - 1 acceptances the set joins every village, so the sweep can stop. The group record is exactly what a union-find holds: a `find` for the two ends decides the quote, and a `union` records an acceptance.

<!-- names: cut property, sorted sweep, safe edge -->

<!-- stage: variables -->
### Order, Groups, Total And Count

The array `order` holds the quotes sorted by price, with the original order kept for equal prices. The group record is a `parent` array where `parent[v] == v` marks the leader of a group, and the pair `ra`, `rb` are the leaders found for the two ends of the current quote. The number `taken` counts accepted quotes and `total` adds up their prices in a `long`. The goal `need` is V - 1, and the loop stops the moment `taken` reaches it. If the loop ends with `taken` below `need`, some villages can never be joined.

<!-- stage: trace -->
### Two Sweeps Over Quotes

The first trace uses six villages and nine sorted quotes, each cell written as the two villages and the price. The pointer `i` is the quote under consideration. In the vars, `weight` is its price, `laid` is 1 when it was accepted and 0 when skipped, and `taken`, `total` and `parts` are the accepted count, the money so far and the number of separate groups after the decision. The fourth quote joins two villages that the first three pipes already connect, so it is skipped. The sweep stops once five pipes are laid, which leaves the last three quotes unread.

```trace
{"cells":["3-4:2","1-2:3","0-1:4","0-2:5","2-3:6","4-5:7","3-5:8","1-3:9","2-4:10"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"weight":2,"laid":1,"taken":1,"total":2,"parts":5},"note":"Villages 3 and 4 lie in different groups, so the pipe of 2 is laid; 5 groups remain."},{"at":{"i":1},"vars":{"weight":3,"laid":1,"taken":2,"total":5,"parts":4},"note":"Villages 1 and 2 lie in different groups, so the pipe of 3 is laid; 4 groups remain."},{"at":{"i":2},"vars":{"weight":4,"laid":1,"taken":3,"total":9,"parts":3},"note":"Villages 0 and 1 lie in different groups, so the pipe of 4 is laid; 3 groups remain."},{"at":{"i":3},"vars":{"weight":5,"laid":0,"taken":3,"total":9,"parts":3},"note":"Villages 0 and 2 already share a group, so the quote of 5 is skipped and nothing is paid."},{"at":{"i":4},"vars":{"weight":6,"laid":1,"taken":4,"total":15,"parts":2},"note":"Villages 2 and 3 lie in different groups, so the pipe of 6 is laid; 2 groups remain."},{"at":{"i":5},"vars":{"weight":7,"laid":1,"taken":5,"total":22,"parts":1},"note":"Villages 4 and 5 lie in different groups, so the pipe of 7 is laid; 1 group remain. Five pipes are laid, so the sweep stops with the remaining quotes unread."}]}
```

The second trace is the false friend. Five villages have six sorted quotes, and the cheapest quotes without any loop test pick the four cheapest and stop. The vars compare that rule with the sweep. The count `blindParts` is the number of groups after the blind picks, and `sweepParts` is the same for the sweep. The blind picks run into a triangle among villages 0, 1 and 2, spend a pipe on it, and leave two groups, while the sweep skips the loop edge and reaches everyone.

```trace
{"cells":["0-1:1","1-2:2","0-2:3","3-4:4","2-3:6","1-3:9"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"blindPicked":1,"blindParts":4,"sweepTaken":1,"sweepParts":4},"note":"Quote 0-1 of 1: the blind rule has picked 1 and leaves 4 groups. The sweep lays it."},{"at":{"i":1},"vars":{"blindPicked":2,"blindParts":3,"sweepTaken":2,"sweepParts":3},"note":"Quote 1-2 of 2: the blind rule has picked 2 and leaves 3 groups. The sweep lays it."},{"at":{"i":2},"vars":{"blindPicked":3,"blindParts":3,"sweepTaken":2,"sweepParts":3},"note":"Quote 0-2 of 3: the blind rule has picked 3 and leaves 3 groups. The sweep skips it."},{"at":{"i":3},"vars":{"blindPicked":4,"blindParts":2,"sweepTaken":3,"sweepParts":2},"note":"Quote 3-4 of 4: the blind rule has picked 4 and leaves 2 groups. The sweep lays it."},{"at":{"i":4},"vars":{"blindPicked":4,"blindParts":2,"sweepTaken":4,"sweepParts":1},"note":"Quote 2-3 of 6: the blind rule has picked 4 and leaves 2 groups. The sweep lays it."},{"at":{"i":5},"vars":{"blindPicked":4,"blindParts":2,"sweepTaken":4,"sweepParts":1},"note":"Quote 1-3 of 9: the blind rule has picked 4 and leaves 2 groups. The sweep has stopped."}]}
```

<!-- stage: code -->
### Sorted Sweep With Early Stop

```java
static long spanCost(int n, int[][] routes) {
    int[][] order = routes.clone();
    Arrays.sort(order, (p, q) -> Integer.compare(p[2], q[2]));
    int[] parent = new int[n];
    for (int v = 0; v < n; v++) parent[v] = v;
    long total = 0;
    int taken = 0;
    for (int[] r : order) {
        if (taken == n - 1) break;
        int ra = leader(parent, r[0]), rb = leader(parent, r[1]);
        if (ra == rb) continue;
        parent[ra] = rb;
        total += r[2];
        taken++;
    }
    return taken == n - 1 ? total : -1;
}

static int leader(int[] parent, int v) {
    while (parent[v] != v) {
        parent[v] = parent[parent[v]];
        v = parent[v];
    }
    return v;
}
```

The `clone` copies only the outer array, which is enough because sorting moves row references and never edits a row, so the caller's list is untouched. The sort is stable for objects, so equal prices keep their input order. The comparator uses `Integer.compare` rather than subtraction. Sorting costs O(E log E), the sweep does O(E) leader lookups that are nearly constant each, and memory is O(V) beyond the sorted copy.

<!-- stage: applicability -->
### When The Cheapest Join Wins

Use this when a weighted undirected graph must be connected through its cheapest set of edges, with the cue being words like connect all, minimum total cost, or fewest cables. The invariant to guard is that the accepted edges are loop-free and already inside some cheapest network, so a quote may be laid only when its two ends have different leaders. Stopping at V - 1 acceptances is an optimisation, and a count below V - 1 at the end is the signal that the graph was never connected.

The false friend is picking the cheapest edges and ignoring loops. Taking the V - 1 smallest prices looks like the cheapest network, yet a cluster of cheap quotes can form a triangle that wastes one pipe and strands a village. The rule also does not give shortest routes: the tree it builds can force a long detour between two particular villages, and that question belongs to weighted shortest paths, which come later. Do not use it for one-way pipes, where the directed problem is different. In Java, subtracting prices in a comparator overflows for large values and silently scrambles the sort, and summing int prices into an `int` wraps around, so keep the total in a `long`.

<!-- stage: exercises -->
### Exercises

#### [Build] Cheapest Safe Edge (Author exercise)
<!-- id: ug-cheapest-safe-edge -->

**Prerequisites.** The `find` and `union` pair from the two previous lessons on disjoint sets, and the cut argument from this lesson.

**Problem.** There are `n` villages numbered 0 to n-1, and `routes` lists possible pipes as `[a, b, price]`. Consider the routes in increasing price, with routes of equal price taken in their input order. Accept a route only when its two villages are not yet joined by accepted routes. Return the accepted routes, in the order they were accepted, as a new `int[][]` of copied rows. Do not stop early, and if the villages cannot all be joined, return the accepted routes of the groups that do form. Neither `routes` nor its rows are modified.

**Constraints.** Between 1 and 12 villages, at most 40 routes, and prices between 0 and 1000. A route may repeat another or join a village to itself.

**Example 1.** Input `n = 4, routes = [[0,1,5],[1,2,3],[0,2,4],[2,3,6]]`, output `[[1,2,3],[0,2,4],[2,3,6]]`.

**Example 2.** Input `n = 5, routes = [[0,1,2],[2,3,2],[1,2,2],[3,4,1],[0,4,2],[1,3,9]]`, output `[[3,4,1],[0,1,2],[2,3,2],[1,2,2]]`.

**Hint.** If two routes cost the same, which one should the sort place first, and what does the leader test say about a route whose ends already share a leader?

**Changed decision.** A route is judged by the leaders of its ends at the moment it is reached, instead of being kept because it is one of the cheapest.

#### [Vary] Stop After V Minus One (Author exercise)
<!-- id: ug-stop-after-v-minus-one -->

**Prerequisites.** The Cheapest Safe Edge rung.

**Problem.** The same sweep now runs on a graph that is guaranteed to be connected, and it must end as soon as `n - 1` routes have been accepted. Return a `long[]` of two values: the total price of the accepted routes, and the number of routes that were examined, counting accepted and skipped ones, up to and including the route that completed the set. With one village the answer is `[0, 0]`. The `routes` array is not modified.

**Constraints.** 1 <= n <= 12, the routes join all villages, there are at most 40 routes, and every price is at most 1000.

**Example 1.** Input `n = 4, routes = [[0,1,1],[1,2,2],[2,3,3],[0,3,4],[0,2,5]]`, output `[6, 3]`.

**Example 2.** Input `n = 5, routes = [[0,1,1],[1,2,2],[0,2,3],[3,4,4],[2,3,6],[1,4,8]]`, output `[13, 5]`.

**Hint.** Should the test for having enough routes come before looking at the next one or after accepting one, and what number would an early check report for a single village?

**Changed decision.** The loop leaves once the accepted count reaches `n - 1`, instead of reading every remaining route to learn that none can be accepted.

#### [Boundary] Disconnected Weighted Graph (Author exercise)
<!-- id: ug-disconnected-weighted -->

**Prerequisites.** The Stop After V Minus One rung.

**Problem.** Given `n` villages and weighted `routes` that might not connect them all, return the least total price of a set of routes joining every village, as a `long`. If no such set exists, return -1. A single village needs no routes and costs 0. Prices can be large, so the total may exceed the range of an `int`. The input arrays are not modified.

**Constraints.** 1 <= n <= 60, at most 600 routes, and prices from 0 up to 2,000,000,000. Routes may be parallel, and a route may join a village to itself.

**Example 1.** Input `n = 4, routes = [[0,1,2],[1,2,3],[0,2,1]]`, output `-1`.

**Example 2.** Input `n = 5, routes = [[0,1,2000000000],[1,2,2000000000],[2,3,2000000000],[3,4,2000000000]]`, output `8000000000`.

**Hint.** After the sweep ends, what does the number of accepted routes tell you, and in which type must the running total be held?

**Changed decision.** The answer is reported only when exactly `n - 1` routes were accepted, instead of returning whatever total the sweep reached.

#### [Recognize] Min Cost To Connect All Points (LeetCode 1584)
<!-- id: ug-min-cost-connect-points -->

**Prerequisites.** The Disconnected Weighted Graph rung, and the idea that a list of points becomes a complete graph once every pair is priced.

**Problem.** Each `points[i] = [x, y]` is a distinct point on the plane. Connecting two points costs the Manhattan distance, `|x1 - x2| + |y1 - y2|`. Return the least total cost so that every pair of points is joined by a path of connections. The `points` array is not modified.

**Constraints.** 1 <= points.length <= 1000 and every coordinate lies between -1,000,000 and 1,000,000. All points are different.

**Example 1.** Input `points = [[0,0],[1,1],[1,0],[-1,1]]`, output `4`.

**Example 2.** Input `points = [[3,12],[-2,5],[-4,1]]`, output `18`.

**Hint.** How many candidate connections exist for n points, and which of the earlier rungs can run on that list once each pair has a price?

**Changed decision.** The routes are generated from the point pairs before the sweep, instead of being supplied as a list.
