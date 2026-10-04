<!-- lesson-kind: combination -->
<!-- lesson-id: graph-and-union-find -->
## Graph And Union-Find

<!-- stage: context -->
### The Merrow Islands Radio Club

The Merrow Islands are a scatter of forty small islands, and the amateur radio club keeps a hand-lettered logbook in the harbour office. Every island has one hut with a transmitter. When the owners of two huts finish tuning a link between them, a club volunteer named Iselin writes the pair of island numbers on a new line of the log. A message can hop along any chain of links, so two islands are in touch when some chain of logged links joins them, however long.

Iselin is asked three things at the end of every season. How many separate networks exist, and how many islands does each hold? Which log lines were pointless, because the two islands could already reach each other through earlier lines? And on which line did the first pointless one appear? The log has grown to several thousand lines, and each season she is expected to answer after reading it only once from top to bottom.

<!-- stage: contributions -->
### What Edges And Roots Bring

The graph brings the events. Each line of the log is an edge, a statement that two vertices are now joined, and the lines arrive in a definite order. The graph also supplies the vocabulary of the questions: a component is a maximal set of mutually reachable vertices, a pointless line is an edge that closes a cycle, and the answers are counted from what each edge does when it is read.

Union-find brings the memory. It keeps exactly one representative per component, so one lookup tells which component a vertex is in, and one merge fuses two components when an edge joins them. It stores nothing about routes, only membership and size.

Neither half is enough alone. A graph with no representative has to search for a route before it can judge any edge, and representatives with no edges to read have nothing to merge. The cue for the combination is a stream of joining statements followed by questions about components, such as how many, how big, and which statement was already implied.

<!-- stage: naive -->
### Search The Log For Each Line

The direct method keeps an adjacency list of the lines read so far. When a new line names islands a and b, it first searches the list from a to see whether b can be reached. If it can, the line is pointless and is counted, and the first such index is remembered. Then the line is added. At the end, a final search from each unvisited island finds the networks and their sizes.

```java
static int[] audit(int n, int[][] log) {
    List<List<Integer>> adj = new ArrayList<>();
    for (int i = 0; i < n; i++) adj.add(new ArrayList<>());
    int pointless = 0, first = -1;
    for (int i = 0; i < log.length; i++) {
        int a = log[i][0], b = log[i][1];
        boolean[] seen = new boolean[n];
        Deque<Integer> stack = new ArrayDeque<>();
        stack.push(a);
        seen[a] = true;
        while (!stack.isEmpty()) {
            int v = stack.pop();
            for (int w : adj.get(v)) if (!seen[w]) { seen[w] = true; stack.push(w); }
        }
        if (seen[b]) {
            pointless++;
            if (first < 0) first = i;
        }
        adj.get(a).add(b);
        adj.get(b).add(a);
    }
    return new int[] {pointless, first};
}
```

It is correct for every log, including repeated lines, a line that names one island twice, and islands that never appear. Each judgement uses a fresh search over exactly the lines before it, so it never sees a link that has not been logged yet.

<!-- stage: bottleneck -->
### Every Line Triggers A Full Search

With V islands and E lines, the search before each line may touch every island and every earlier line, so the method costs O(E * (V + E)) in the worst case, and the final sweep for network sizes adds a further O(V + E). A season with 20,000 islands and 40,000 lines is about 40,000 searches of up to 60,000 steps, roughly 2.4 billion operations, only to answer a handful of numbers.

Most of that work is repeated. Two lines in a row that touch the same big network cause the search to walk the same huts again, and the answer to the search is always the same yes or no: do these two islands already belong together? The walk discovers routes, but nobody asked for a route. The three questions need only the identity of a network and its size at the moment each line is read, and that can be kept up to date with a few array writes per line, in roughly O(E * alpha(V)) overall.

<!-- stage: insight -->
### One Representative Per Evolving Component

Treat the log as a stream of **link events**. Each event names two vertices and is handled in three moves: look up the representative of each endpoint, compare the two, and act on the result. If the representatives are equal, the event is pointless, because the endpoints were already joined by earlier events. It changes no stored array, it only adds one to a redundant counter, and the first time this happens it records the line index. If the representatives differ, the event is a real merge: the smaller component is hung under the larger one, the counts change, and the number of components drops by one.

Everything the questions ask is a by-product of that comparison. The component count is n minus the real merges. The pointless lines are those where the comparison said equal, and the line index of the first one is read at that moment. The sizes of the networks are the values kept at the surviving representatives, so they can be listed at the end without any search.

The invariant is that the arrays change in **lockstep**: the parent array and the size array are written together, only after both representatives are known and different, so the size stored at a representative is always the true number of vertices that lead to it. A write to one array without the other leaves the picture inconsistent, and so does comparing the endpoints themselves instead of their representatives.

<!-- names: link events, representative, lockstep -->

<!-- stage: variables -->
### Parent, Size And The Running Tallies

The array `parent` holds, for each island, the one island it answers to, with `parent[i] == i` marking a representative. The array `size` is meaningful only at representatives and starts at 1 everywhere. For the line being read, `ra` and `rb` are the two representatives. Three tallies change with the lines: `components` starts at n and falls by one on each real merge, `pointless` starts at 0 and rises on every line where `ra == rb`, and `first` starts at -1 and is written once, on the first pointless line, using the line's index `i`. The largest network is read from `size` at the end, or kept in a running `biggest` that is updated after each real merge with the keeper's new size.

<!-- stage: trace -->
### Two Logs Read Line By Line

The first trace reads a season of six lines over seven islands, listed as the cells in the order they were logged. The pointer `i` is the line being read. The vars show the two representatives found, how many networks remain, how many pointless lines have been counted and the index of the first one. The line at index 3 joins two islands that the first three lines already tied together, and the line at index 5 names a single island twice, so both are counted and neither changes any array.

```trace
{"cells":["0-1","2-3","1-3","3-0","4-5","6-6"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"ra":0,"rb":1,"networks":6,"pointless":0,"first":-1},"note":"Representatives 0 and 1 differ, so the two networks merge and 6 remain."},{"at":{"i":1},"vars":{"ra":2,"rb":3,"networks":5,"pointless":0,"first":-1},"note":"Representatives 2 and 3 differ, so the two networks merge and 5 remain."},{"at":{"i":2},"vars":{"ra":0,"rb":2,"networks":4,"pointless":0,"first":-1},"note":"Representatives 0 and 2 differ, so the two networks merge and 4 remain."},{"at":{"i":3},"vars":{"ra":0,"rb":0,"networks":4,"pointless":1,"first":3},"note":"Both endpoints lead to representative 0, so the line is pointless; it is counted and nothing is written. It is the first one, at index 3."},{"at":{"i":4},"vars":{"ra":4,"rb":5,"networks":3,"pointless":1,"first":3},"note":"Representatives 4 and 5 differ, so the two networks merge and 3 remain."},{"at":{"i":5},"vars":{"ra":6,"rb":6,"networks":3,"pointless":2,"first":3},"note":"Both endpoints lead to representative 6, so the line is pointless; it is counted and nothing is written."}]}
```

The second trace follows the two arrays themselves on a log of six lines over six islands. The vars `parent` and `size` show both arrays after the line has been handled, written as lists with one entry per island. Each real merge changes one slot of `parent` and one slot of `size` in the same step, and the size slot that changes always belongs to the keeper. The line at index 4 touches only islands that already share a representative, so both lists stay exactly as they were, and the last line merges the two remaining networks.

```trace
{"cells":["4-5","3-4","0-1","1-2","2-0","2-5"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"parent":"012344","size":"111121","networks":5},"note":"Representatives 4 and 5 differ, so one slot of parent and one slot of size change together."},{"at":{"i":1},"vars":{"parent":"012444","size":"111131","networks":4},"note":"Representatives 3 and 4 differ, so one slot of parent and one slot of size change together."},{"at":{"i":2},"vars":{"parent":"002444","size":"211131","networks":3},"note":"Representatives 0 and 1 differ, so one slot of parent and one slot of size change together."},{"at":{"i":3},"vars":{"parent":"000444","size":"311131","networks":2},"note":"Representatives 0 and 2 differ, so one slot of parent and one slot of size change together."},{"at":{"i":4},"vars":{"parent":"000444","size":"311131","networks":2},"note":"Representatives are both 0, so neither array is written."},{"at":{"i":5},"vars":{"parent":"000404","size":"611131","networks":1},"note":"Representatives 0 and 4 differ, so one slot of parent and one slot of size change together."}]}
```

<!-- stage: code -->
### A Relay Log Reader

```java
final class RelayLog {
    private final int[] parent;
    private final int[] size;
    private int components;
    private int pointless;
    private int first = -1;
    private int lines;

    RelayLog(int n) {
        parent = new int[n];
        size = new int[n];
        for (int i = 0; i < n; i++) {
            parent[i] = i;
            size[i] = 1;
        }
        components = n;
    }

    private int find(int x) {
        while (parent[x] != x) {
            parent[x] = parent[parent[x]];
            x = parent[x];
        }
        return x;
    }

    void read(int a, int b) {
        int ra = find(a), rb = find(b);
        if (ra == rb) {
            if (pointless++ == 0) first = lines;
        } else {
            int big = size[ra] >= size[rb] ? ra : rb;
            int small = big == ra ? rb : ra;
            parent[small] = big;
            size[big] += size[small];
            components--;
        }
        lines++;
    }

    int[] report() { return new int[] {components, pointless, first}; }

    int[] networkSizes() {
        int[] out = new int[components];
        int k = 0;
        for (int i = 0; i < parent.length; i++) if (parent[i] == i) out[k++] = size[i];
        java.util.Arrays.sort(out);
        return out;
    }
}
```

Each `read` costs O(alpha(n)) amortised with halving in `find`, and the whole log is O(E alpha(n)) with O(n) memory. The counter `lines` advances on every line, pointless or not, so `first` is an index into the log and not a count of merges. The method `networkSizes` scans the parent array once and reads `size` only where a vertex is its own representative.

<!-- stage: applicability -->
### When The Log Only Grows

Use this combination when joining statements keep arriving and the questions are about membership: how many groups, how large, which statement added nothing, or which statement is the cheapest that still joins two groups. The same loop serves a friendship list, a set of shared identifiers, and a list of candidate edges sorted by cost. The invariant to defend is that both arrays move in lockstep at the representatives, and that every judgement is made on representatives, never on the raw endpoints.

The false friend is the edge-count shortcut. Subtracting the number of lines from the number of islands gives the number of networks only for a forest, and the moment one pointless line appears, the answer is too small by exactly the number of pointless lines. Do not use this method when links can be removed, because a merge cannot be undone from the arrays alone. It also cannot list the paths between two islands, and it cannot give the cheapest route when links have costs; weighted shortest paths belong to Chapter 24. In Java, ids kept in a `Map<String, Integer>` come back as boxed `Integer` objects, and comparing two of them with `==` works for small values and fails past 127, so compare with `.equals` or unbox into an `int` first.

<!-- stage: exercises -->
### Exercises

#### [Build] Number of Provinces (LeetCode 547)
<!-- id: uc-province-sizes -->

**Prerequisites.** Union by size, and the idea that each friendship edge merges two components.

**Problem.** There are `n` cities numbered 0 to n-1. The input `pairs` is a list of friendships, each `[a, b]` meaning that cities a and b are directly connected, and the connection works in both directions. A province is a maximal set of cities joined by chains of friendships. Return the sizes of all provinces as a new `int[]` sorted in ascending order. A pair may repeat or name one city twice, and a city that appears in no pair is a province of size 1. The input is not modified.

**Constraints.** 1 <= n <= 1000 and 0 <= pairs.length <= 3000, with every city between 0 and n-1.

**Example 1.** Input `n = 7, pairs = [[0,1],[1,2],[3,4],[5,5]]`, output `[1,1,2,3]`.

**Example 2.** Input `n = 6, pairs = [[5,0],[0,5],[2,3],[3,4],[4,2]]`, output `[1,2,3]`.

**Hint.** After all pairs are read, where is each province's size stored, and which vertices hold it?

**Changed decision.** The input is a list of pairs and the answer is the sorted list of component sizes, instead of a matrix and a single count.

#### [Vary] Redundant Connection (LeetCode 684)
<!-- id: uc-redundant-count -->

**Prerequisites.** The Build rung, and the idea that an edge inside one component adds nothing.

**Problem.** Consider `n` vertices labelled 0 through n-1 with a list `edges` of undirected edges read in order. The graph is general: it may be disconnected, may repeat an edge, and may contain an edge from a vertex to itself. An edge is redundant when its two endpoints are already in one component at the moment it is read. Return `[count, firstIndex]` as a new `int[]`, where `count` is the number of redundant edges and `firstIndex` is the 0-based position in `edges` of the first one, or -1 when there is none. The input is not modified.

**Constraints.** 1 <= n <= 1000 and 0 <= edges.length <= 3000, with every endpoint between 0 and n-1.

**Example 1.** Input `n = 4, edges = [[0,1],[1,2],[2,0],[2,0],[3,3]]`, output `[3,2]`.

**Example 2.** Input `n = 6, edges = [[0,1],[2,3]]`, output `[0,-1]`.

**Hint.** What must be true of the two representatives, found before any write, for an edge to count?

**Changed decision.** The scan counts every redundant edge and reports the first one, instead of returning the last edge that closes a cycle in a graph that has exactly one.

#### [Boundary] Accounts Merge (LeetCode 721)
<!-- id: uc-merged-accounts -->

**Prerequisites.** The Vary rung, and mapping each shared identifier to the first account that owned it.

**Problem.** Each account is a list whose first entry is a name and whose remaining entries are one or more emails. Two accounts belong to the same person exactly when a chain of accounts joins them through shared emails, and an equal name alone proves nothing. Return `[groups, largest]` as a new `int[]`, where `groups` is the number of merged account groups and `largest` is the number of distinct emails in the group that has the most. An email repeated inside one account counts once. The input is not modified.

**Constraints.** 1 <= accounts.length <= 500, every account has between 1 and 10 emails after its name, and names and emails are non-empty strings.

**Example 1.** Input `accounts = [["Ana","a@x","b@x"],["Ben","c@x"],["Ana","b@x","d@x"],["Ana","e@x"]]`, output `[3,3]`.

**Example 2.** Input `accounts = [["Sam","s@y","s@y","t@y"],["Sam","u@y"],["Sam","t@y"]]`, output `[2,2]`.

**Hint.** Which accounts should be united when an email is met for the second time, and what is stored in the map for each email?

**Changed decision.** Emails are mapped to their first owner and only the number of groups and the largest email set are returned, instead of rebuilding every merged account.

#### [Recognize] Min Cost to Connect All Points (LeetCode 1584)
<!-- id: uc-chebyshev-spanning -->

**Prerequisites.** The Boundary rung, and the rule that a sorted edge is accepted only when it joins two components.

**Problem.** Each point is a pair `[x, y]` of integers. Connecting two points costs `max(|x1 - x2|, |y1 - y2|)`, the Chebyshev distance, and any two points may be connected. Choose connections so that every point can reach every other and the total cost is as small as possible. Return `[total, largest]` as a new `int[]`, where `total` is the minimum total cost and `largest` is the cost of the most expensive connection that the sorted-edge method accepts, or 0 when there is only one point. Duplicate points are allowed and cost 0 to join.

**Constraints.** 1 <= points.length <= 300 and coordinates between -10000 and 10000.

**Example 1.** Input `points = [[0,0],[2,2],[3,10],[5,2],[7,0]]`, output `[15,8]`.

**Example 2.** Input `points = [[1,1],[1,1],[4,5]]`, output `[4,4]`.

**Hint.** Which edge list must be sorted, and how many accepted edges mean that no further edge can matter?

**Changed decision.** The distance is the larger coordinate gap and the answer also reports the largest accepted edge, instead of the Manhattan sum with only a total.
