<!-- lesson-kind: combination -->
<!-- lesson-id: merge-groups-as-edges-arrive -->
## Merge Groups As Edges Arrive

<!-- stage: context -->
### Why Rebuilding Groups Per Event Stalls

A device service receives pairing events. Each event says that two device records belong to the same customer. After every event the dashboard shows how many customer groups exist, and it flags an event that pairs two records already in one group. The first version searches the events seen so far each time a new one arrives. With a hundred events it feels instant. With a hundred thousand events, every refresh takes seconds and the dashboard stalls.

Four more requests follow in the same quarter. An administrator wants the size of the largest group. A data team wants every redundant event listed in arrival order. A billing team wants records that share an email address merged even when the letters of the address differ in case. A network team wants the cheapest set of links that joins every site. Each request looks like a separate algorithm.

This lesson asks one question. Which structure, updated one event at a time, answers all four requests without a new search per event?

<!-- stage: contributions -->
### What Each Earlier Lesson Adds

Five lessons of this chapter supply the pieces. Undirected Parent State contributes the cycle test for an undirected graph. An edge to a vertex that the search already reached, other than the parent, shows a cycle. That test lives inside one traversal and forgets everything afterward. Find Compression contributes `find`. It returns the representative of a group, the one vertex that stands for the whole group, and it shortens the route it walked. Union By Size contributes the merge rule that attaches the smaller group below the larger one and keeps a `size` entry for each representative.

Dynamic Connectivity contributes the view of edges as events that arrive over time. It also contributes a counter that falls by one for each merge that joins two groups. Kruskal Foundations contributes the habit of comparing the representatives of both endpoints before acting, and of processing edges in increasing weight.

The combination adds one rule. Compare the representatives of the endpoints before every merge, and let the outcome feed the question of the request. The invariant is that two vertices share a representative exactly when a path of already processed edges joins them. The nearest false friend is the `visited` array of a single traversal. It answers whether this search reached a vertex, and it cannot answer whether earlier edges joined two vertices.

<!-- stage: naive -->
### Searching The Earlier Events Each Time

The direct plan keeps an adjacency list of the events seen so far. For each new event, it searches from one endpoint to find out whether the other endpoint is reachable. A reachable endpoint marks the event as redundant, and an unreachable one lets the event enter the list.

```java
static int countRepeatLinks(int n, int[][] events) {
    List<List<Integer>> adj = new ArrayList<>();
    for (int i = 0; i < n; i++) adj.add(new ArrayList<>());
    int repeats = 0;
    for (int[] e : events) {
        if (reaches(adj, e[0], e[1])) repeats++;      // a full search over the earlier events
        else { adj.get(e[0]).add(e[1]); adj.get(e[1]).add(e[0]); }
    }
    return repeats;
}

static boolean reaches(List<List<Integer>> adj, int from, int to) {
    boolean[] seen = new boolean[adj.size()];
    ArrayDeque<Integer> queue = new ArrayDeque<>();
    seen[from] = true;
    queue.add(from);
    while (!queue.isEmpty()) {
        int cur = queue.poll();
        if (cur == to) return true;
        for (int nb : adj.get(cur)) {
            if (!seen[nb]) { seen[nb] = true; queue.add(nb); }
        }
    }
    return false;
}
```

```predict
Five vertices 0 to 4 receive the events 0-1, 1-2, 2-3 and 3-4 in this order. Every search starts at the first endpoint of the new event. How many vertices do the four searches take off the queue in total?

The searches take 10 vertices off the queue. The search for event 0-1 reaches 1 vertex, for 1-2 it reaches 2, for 2-3 it reaches 3 and for 3-4 it reaches 4. The target is never found, so each search walks its whole group, and the sum is 1 + 2 + 3 + 4.
```

<!-- stage: bottleneck -->
### Counting The Work Of Repeated Searches

The method answers correctly, but each event pays for a search over the whole structure. A search costs O(V + E) in the vertices and events seen so far, and the loop runs once per event. The total is O(E * (V + E)). A service with 100,000 records and 100,000 events then needs about 10^10 steps, which is minutes of work.

The loop also repeats the same question. Before each event, the search asks whether two vertices already share a group, and it rediscovers that group from scratch every time. A path of five vertices already shows the pattern, where each new event walks the group that the previous event grew.

The other requests make the cost worse. The size of the largest group needs a count per group after every event. A merge by shared email needs a way to turn each address into a vertex. A cheapest set of links needs the events sorted by weight and an immediate answer to the same question. The program needs a structure that remembers each group and merges two groups in almost constant time.

<!-- stage: insight -->
### One Structure Behind Four Requests

#### Keeping One Head Per Group

A **representative** is the one vertex that stands for a whole group. Union-find stores the representative of every group as the root of a tree, so `find(x)` returns the same vertex for every member of a group. Two vertices are connected exactly when their `find` results are equal. A merge of two groups changes only the root of one tree, so the cost of a merge does not depend on the group sizes. The count of groups starts at `V` and falls by one at each merge that joins two different groups.

#### Spotting A Closing Edge

A **closing edge** is an edge whose endpoints already share a representative at the moment it arrives. The redundant event of the opening scenario is a closing edge. It adds no connection, and it creates a cycle with the edges before it. The program detects it with one comparison, `find(u) == find(v)`, in near-constant time. The request decides what to do with the result. It can count the edge, store it in a list in arrival order, or skip it, as Kruskal does. A self-loop and a repeated pair both count as closing edges, because their endpoints share a representative immediately.

#### Reading Size From The Root

The **component size** is the number of vertices in one group, and union-find keeps it at the representative. When a merge attaches one root below another, the new size is the sum of both sizes. Keeping the running maximum of these sums gives the largest group at no extra cost. Identifiers that are not integers, such as email addresses, go through a map from key to integer id, after which the same operations apply. Edges that are not given, such as links between points, are generated first and then processed in sorted order.

<!-- names: representative, closing edge, component size -->

<!-- stage: variables -->
### What The Structure Keeps

The structure keeps these values, and the traces below use the same names.

- **parent** holds, for each vertex, the next vertex toward its root, and `parent[x] == x` marks a root.
- **size** holds the vertex count of a group and is read only at a root.
- **count** is the current number of groups, and it falls by one at each successful merge.
- **largest** is the maximum group size seen so far.
- **closing** lists the arrival positions of the events that join two vertices of one group.
- **owner** maps an identifier, such as an email address, to the first record that used it.

<!-- stage: trace -->
### Two Runs Of The Same Structure

#### Events On Six Vertices

The first trace reads six events on vertices 0 to 5. The cells are the vertex ids, and the pointers `u` and `v` mark the endpoints of the event under examination. The variable `closing` lists the positions of events whose endpoints already share a representative.

The first two events create the groups {0, 1} and {2, 3}. The third event joins them into one group of four. The fourth event pairs 0 and 2, which share a representative by then, so it closes a cycle and changes nothing. The fifth event creates {4, 5}. The sixth event repeats that pair, so it is a closing edge as well. The count of groups ends at 2 and the largest group has 4 vertices.

```trace
{"cells":[0,1,2,3,4,5],"pointers":["u","v"],"steps":[{"at":{"u":-1,"v":-1},"vars":{"count":"6","largest":"1","closing":"[]","parent":"[0, 1, 2, 3, 4, 5]"},"note":"Start: six groups of one vertex, so count = 6 and largest = 1."},{"at":{"u":0,"v":1},"vars":{"count":"5","largest":"2","closing":"[]","parent":"[0, 0, 2, 3, 4, 5]"},"note":"Event 0 pairs 0 and 1. The representatives 0 and 1 differ, so the groups merge and count becomes 5."},{"at":{"u":2,"v":3},"vars":{"count":"4","largest":"2","closing":"[]","parent":"[0, 0, 2, 2, 4, 5]"},"note":"Event 1 pairs 2 and 3. The representatives 2 and 3 differ, so the groups merge and count becomes 4."},{"at":{"u":1,"v":3},"vars":{"count":"3","largest":"4","closing":"[]","parent":"[0, 0, 0, 2, 4, 5]"},"note":"Event 2 pairs 1 and 3. The representatives 0 and 2 differ, so the groups merge and count becomes 3."},{"at":{"u":0,"v":2},"vars":{"count":"3","largest":"4","closing":"[3]","parent":"[0, 0, 0, 2, 4, 5]"},"note":"Event 3 pairs 0 and 2. Both have representative 0, so the event is a closing edge and nothing changes."},{"at":{"u":4,"v":5},"vars":{"count":"2","largest":"4","closing":"[3]","parent":"[0, 0, 0, 2, 4, 4]"},"note":"Event 4 pairs 4 and 5. The representatives 4 and 5 differ, so the groups merge and count becomes 2."},{"at":{"u":5,"v":4},"vars":{"count":"2","largest":"4","closing":"[3, 5]","parent":"[0, 0, 0, 2, 4, 4]"},"note":"Event 5 pairs 5 and 4. Both have representative 4, so the event is a closing edge and nothing changes."}]}
```

#### Merging Accounts By Shared Email

The second trace reads four accounts. The cells are the account positions 0 to 3, and the pointer `acct` marks the account being read. The variable `owner` maps each lowercase email address to the first account that used it. When a later account uses an address that has an owner, the structure merges the two accounts.

Account 1 uses an address that account 0 owns, once the letters are lowercased, so the two merge. Account 3 uses an address that account 1 owns, so it merges as well, and account 0 stays the first-seen account of the group. Account 2 shares nothing and stays alone. The groups by final root are {0, 1, 3} and {2}.

```trace
{"cells":[0,1,2,3],"pointers":["acct"],"steps":[{"at":{"acct":-1},"vars":{"owner":"{}","parent":"[0, 1, 2, 3]"},"note":"Start: four accounts, each its own group, and no address has an owner."},{"at":{"acct":0},"vars":{"owner":"{a@x.io:0, b@x.io:0}","parent":"[0, 1, 2, 3]"},"note":"Account 0: a@x.io gets owner 0; b@x.io gets owner 0."},{"at":{"acct":1},"vars":{"owner":"{a@x.io:0, b@x.io:0, c@x.io:1}","parent":"[1, 1, 2, 3]"},"note":"Account 1: b@x.io is owned by account 0, so accounts 1 and 0 merge; c@x.io gets owner 1."},{"at":{"acct":2},"vars":{"owner":"{a@x.io:0, b@x.io:0, c@x.io:1, d@x.io:2}","parent":"[1, 1, 2, 3]"},"note":"Account 2: d@x.io gets owner 2."},{"at":{"acct":3},"vars":{"owner":"{a@x.io:0, b@x.io:0, c@x.io:1, d@x.io:2, e@x.io:3}","parent":"[1, 1, 2, 1]"},"note":"Account 3: c@x.io is owned by account 1, so accounts 3 and 1 merge; e@x.io gets owner 3."},{"at":{"acct":3},"vars":{"owner":"{a@x.io:0, b@x.io:0, c@x.io:1, d@x.io:2, e@x.io:3}","parent":"[1, 1, 2, 1]"},"note":"Grouping by final root gives {0, 1, 3} and {2}. The name of each group comes from its smallest account position, so the groups are named Ana and Cy."}]}
```

<!-- stage: code -->
### A Group Structure For Every Request

#### The Structure

The class `Groups` keeps the arrays and the counters. The method `find` compresses the route by halving. The method `union` returns true only when it merges two different groups, so the caller learns whether the event was a closing edge. The class compiles on its own.

```java
import java.util.Arrays;

final class Groups {
    private final int[] parent;
    private final int[] size;
    private int count;
    private int largest = 1;

    Groups(int n) {
        parent = new int[n];
        size = new int[n];
        for (int i = 0; i < n; i++) { parent[i] = i; size[i] = 1; }
        count = n;                                   // every vertex starts as a group of one
    }

    int find(int x) {
        while (parent[x] != x) {
            parent[x] = parent[parent[x]];           // halve the route so later calls are shorter
            x = parent[x];
        }
        return x;
    }

    boolean union(int a, int b) {
        int ra = find(a), rb = find(b);
        if (ra == rb) return false;                  // same representative, so this is a closing edge
        if (size[ra] < size[rb]) { int t = ra; ra = rb; rb = t; }
        parent[rb] = ra;                             // the smaller group goes below the larger one
        size[ra] += size[rb];                        // size stays in step with parent
        largest = Math.max(largest, size[ra]);
        count--;                                     // two groups became one
        return true;
    }

    int count() { return count; }
    int largest() { return largest; }

    static int[] groupsAfterEach(int n, int[][] events) {
        Groups groups = new Groups(n);
        int[] result = new int[events.length];
        for (int i = 0; i < events.length; i++) {
            groups.union(events[i][0], events[i][1]);    // a closing edge leaves the count unchanged
            result[i] = groups.count();                  // one number per event, read in O(1)
        }
        return result;
    }
}
```

#### Using It On A Stream Of Events

The static method `groupsAfterEach` in the same class answers the dashboard request: the number of groups after each event. Every other request of the lesson reads the result of `union`, the value `largest()` or the result of `find`.

The other requests differ only in the surrounding code. A matrix request calls `union` for every pair with a 1 in the upper triangle. A request for closing edges stores each event whose `union` returns false. A request with identifiers calls `union` on the record numbers after a map lookup. A cheapest-links request sorts the pairs by weight first and adds a weight only when `union` returns true.

- **Time** is O(E * alpha(V)) for E calls, plus O(E log E) when the program sorts, where alpha is the inverse Ackermann function.
- **Space** is O(V) for the two arrays, plus whatever the request itself stores, such as a map of identifiers.

<!-- stage: applicability -->
### Telling When Merging Groups Fits

#### Reading The Cue

Use the structure when edges, links or shared identifiers arrive and the question concerns which items end up together. Counts of groups, the size of the largest group, the first closing edge and a final grouping all qualify. The structure only merges. A request that removes edges or asks for a route between two vertices needs a different tool, such as a search over the stored edges.

#### Choosing What The Union Result Feeds

Read the contract and ask what the program does with the comparison of the representatives. A count of groups subtracts one per merge. A largest-group request keeps a running maximum at each merge. A request for closing edges stores the event whenever the comparison finds equal representatives. A request about shared identifiers adds a map from identifier to record, and a request about points generates the edges first.

#### Keeping The Invariant

The invariant is that two vertices share a representative exactly when the processed events join them. It breaks when `size` is read at a vertex that is not a root, or when `parent` changes without a matching update of `size`. In Java, `toLowerCase()` without a locale depends on the machine. Merging by email therefore needs a fixed locale. The false friend is the `visited` array of one traversal, which answers a different question.

<!-- stage: exercises -->
### Exercises

#### [Build] Count Provinces And Find The Largest (LeetCode 547)
<!-- id: dgc-components-and-largest -->

**Prerequisites.** The Union By Size and Dynamic Connectivity lessons.

**Problem.** This changes the Number of Provinces contract: the method also returns the size of the largest province. A square table `isConnected` of 0 and 1 describes `n` cities, where `isConnected[i][j] == 1` means that city `i` and city `j` are directly connected. A province is a maximal set of cities in which every two cities are joined by a chain of direct connections. Return `{count, largest}`, the number of provinces and the number of cities in the largest province.

**Constraints.** The limits are:
- **Size** is `1 <= n <= 200`, and the table has `n` rows of `n` entries.
- **Entries** are 0 or 1, and `isConnected[i][i]` equals 1.
- **Symmetry** holds, so `isConnected[i][j]` equals `isConnected[j][i]`.
- **Result** is an `int` array of length 2.
- **Mutation** does not occur; the method leaves the table unchanged.

**Example 1.** Input `isConnected = [[1,1,0,0],[1,1,0,0],[0,0,1,0],[0,0,0,1]]`, output `{3, 2}`.

**Example 2.** Input `isConnected = [[1,1,0,0],[1,1,1,0],[0,1,1,0],[0,0,0,1]]`, output `{2, 3}`, because cities 0 and 2 connect only through city 1.

**Hint.** Which value holds the size of a group after a merge? When does the maximum change, and what is its value for `n = 1`?

**Changed decision.** The structure also keeps a running maximum of the merged sizes.

#### [Vary] List Every Edge That Closes A Cycle (LeetCode 684)
<!-- id: dgc-edges-closing-cycles -->

**Prerequisites.** Undirected Parent State and the first exercise above.

**Problem.** This changes the Redundant Connection contract: the method returns every closing edge, not one. Vertices are numbered 1 to `n`. Process the edges in input order. An edge is closing when a chain of earlier edges already joins its two endpoints, and a self-loop is closing. Return all closing edges in input order, each as it appears in the input.

**Constraints.** The limits are:
- **Vertices** number `1 <= n <= 1000`.
- **Edges** number `0 <= m <= 2000`, and every endpoint lies in `[1, n]`.
- **Repeats** are allowed, so an edge may appear more than once and a self-loop may occur.
- **Result** is an array of `{a, b}` pairs, empty when no edge closes a cycle.
- **Mutation** does not occur; the method leaves `edges` unchanged.

**Example 1.** Input `n = 5`, `edges = [[1,2],[2,3],[3,1],[1,2],[4,4],[3,5]]`, output `[[3,1],[1,2],[4,4]]`.

**Example 2.** Input `n = 4`, `edges = [[1,2],[2,3],[1,3],[3,4],[4,1]]`, output `[[1,3],[4,1]]`, because the last edge closes a cycle only through the earlier edges 3-4, 2-3 and 1-2.

**Hint.** What must the program do with an edge whose endpoints share a representative? Does the answer change if the closing edge is also merged?

**Changed decision.** The method stores every closing edge and continues after the first one.

#### [Boundary] Merge Accounts Ignoring Letter Case (LeetCode 721)
<!-- id: dgc-accounts-case-insensitive -->

**Prerequisites.** Dynamic Connectivity and the two exercises above.

**Problem.** This changes the Accounts Merge contract: email comparison ignores letter case, and a merged group keeps the name of its first account. Each account is a list whose first entry is a name and whose other entries are email addresses. Two accounts belong to one group when a chain of accounts links them, where consecutive accounts share an email address after both addresses are lowercased. Return one list per group. Each list holds the name of the group's earliest account in input order, followed by the distinct lowercase addresses of the group in ascending string order. Order the groups by the earliest input position of their accounts.

**Constraints.** The limits are:
- **Accounts** number `1 <= n <= 200`, and each holds a name of 1 to 10 letters and 1 to 8 addresses.
- **Addresses** have 3 to 30 characters from letters, digits, `@` and `.`.
- **Names** may differ between accounts of one group, and an address may repeat inside one account.
- **Comparison** ignores case, and the output uses lowercase only.
- **Mutation** does not occur; the method leaves `accounts` unchanged.

**Example 1.** Input `accounts = [[Ana,A@x.io,b@x.io],[Bo,B@X.io,c@x.io],[Cy,d@x.io]]`, output `[[Ana,a@x.io,b@x.io,c@x.io],[Cy,d@x.io]]`.

**Example 2.** Input `accounts = [[Dee,k@m.org],[Eli,K@m.org,z@m.org],[Fay,Z@M.ORG],[Gus,q@m.org]]`, output `[[Dee,k@m.org,z@m.org],[Gus,q@m.org]]`, because Dee, Eli and Fay link through a chain and the earliest name is kept.

**Hint.** What is one vertex here, and which structure turns an address into a vertex? Which locale does the lowercase conversion need?

**Changed decision.** The method lowercases every address with a fixed locale, and the name comes from the earliest account of the group.

#### [Recognize] Connect Points That May Repeat (LeetCode 1584)
<!-- id: dgc-connect-repeated-points -->

**Prerequisites.** Kruskal Foundations and the three exercises above.

**Problem.** This changes the Min Cost to Connect All Points contract: points may repeat. An array holds `n` points `{x, y}`, and two entries may be equal. The cost of a link between two entries is the Manhattan distance of their points, which is 0 for equal points. Return the lowest total cost of links that make every entry reachable from every other entry.

**Constraints.** The limits are:
- **Points** number `1 <= n <= 1000`, and equal points may occur.
- **Coordinates** are `int` values with `-10^6 <= x, y <= 10^6`.
- **Cost** of one link is at most 4 * 10^6.
- **Result** has type `long` and is `0` when `n` is 1 or when all points are equal.
- **Mutation** does not occur; the method leaves `points` unchanged.

**Example 1.** Input `points = [[1,1],[1,1],[4,5],[0,6]]`, output `11`.

**Example 2.** Input `points = [[2,2],[9,9],[2,2],[9,9]]`, output `14`, because both equal pairs join at cost 0 and one link of length 14 joins the two pairs.

**Hint.** The sorted list now starts with zero-cost links. Does the loop count an accepted link by its cost or by its comparison of representatives?

**Changed decision.** A link of cost 0 is a real link that the loop accepts, and the stop rule counts accepted links.
