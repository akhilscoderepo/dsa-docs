<!-- lesson-kind: standard -->
<!-- lesson-id: dynamic-connectivity -->
## Dynamic Connectivity

<!-- stage: context -->
### The Switchboard At Pellam Bridge

Ines runs the switchboard in Pellam Bridge, a town of 2,000 houses numbered from 0. When the telephone company arrived, no house had a line. Since then a crew has laid one wire a day between two houses, and each wire carries a call in both directions. A call can pass through any chain of wires, so house 12 can ring house 90 whenever some path of wires joins them, however long.

All day, callers pick up and ask Ines the same thing: "Can I get through to number 90?" She must answer before she plugs anything in, and she must also be able to say, on request, how many separate islands of connected houses the town has. The wires keep arriving between questions. Ines wants an answer method that stays quick on the thousandth wire and the thousandth question, for any town size and any order of wires.

<!-- stage: naive -->
### Search The Wires Again Per Question

The direct way is to keep the wires as lists, one list of neighbours per house, and to treat every question as a fresh puzzle. Start at the caller's house, follow wires to any house not yet visited, and say yes if the search ever touches the requested house. Counting islands is the same search started from every house that is still unvisited.

```java
static void layWire(List<List<Integer>> wires, int a, int b) {
    wires.get(a).add(b);
    wires.get(b).add(a);
}

static boolean canReach(List<List<Integer>> wires, int from, int to) {
    boolean[] seen = new boolean[wires.size()];
    ArrayDeque<Integer> stack = new ArrayDeque<>();
    stack.push(from);
    seen[from] = true;
    while (!stack.isEmpty()) {
        int house = stack.pop();
        if (house == to) return true;
        for (int next : wires.get(house)) {
            if (!seen[next]) {
                seen[next] = true;
                stack.push(next);
            }
        }
    }
    return false;
}
```

Each answer is right for the wires laid so far, because a search over a snapshot reaches exactly the houses joined to the start. Laying a wire is cheap, and a wire between two houses that were already joined adds an edge but no new connection, which the search copes with since it never revisits a house.

<!-- stage: bottleneck -->
### Every Question Starts From Nothing

The search keeps no memory between questions. If the wires form one long street, 0 to 1 to 2 and on, then a question about house 0 and the newest house walks the whole street each time. With n houses and L wires one question costs O(n + L), and a day with Q questions costs O(Q * (n + L)).

Here is the actual count for the town above. Suppose the crew lays wire i to i+1 and Ines is asked, right after each wire, whether 0 can reach the new end. Every one of the 1,999 questions must walk the full street, and the searches touch 2,000,999 houses in total. Doubling the town roughly quadruples that total, since the work is about n squared over two. What the searches rediscover each time is that a handful of houses are joined. A better design would keep that fact, so that a new wire changes it a little, and a question reads it with almost no walking.

<!-- stage: insight -->
### Label Every House By Its Island

Give each island one **representative**: a single house chosen to stand for the whole island, so that every house in it can be traced to the same one. Two houses are connected exactly when tracing them leads to the same representative, which turns a graph question into the comparison of two numbers. Nothing is searched, because the wires themselves are no longer stored. Only the labels are.

The update rule is **merge on arrival**. When a wire appears between houses a and b, trace both to their representatives. If the two are equal, the wire joins houses that could already talk, so the structure is left exactly as it was, even though a wire was physically laid. If they differ, the islands are now one, so one representative is made to answer to the other, and that single write fixes the label of every house in both islands at once. Union by size and shortened tracing, from the two earlier lessons, keep each trace short.

The third piece is the **live count**: a number that starts at n and drops by one only on a merge that really joined two islands. A repeated wire never lowers it, so reading the number of islands costs nothing, however many wires have arrived.

The invariant is that two houses have the same representative exactly when some chain of wires laid so far joins them. Each rule above is chosen to keep that sentence true after every single wire.

<!-- names: representative, merge on arrival, live count -->

<!-- stage: variables -->
### Labels, Sizes And The Island Tally

The array `parent` stores for every house the one house it answers to, with `parent[h] == h` marking a representative. The array `size` is trusted only at representatives and starts at 1 everywhere. The integer `groups` is the live count and starts at n. For one wire, `a` and `b` are its houses, and `ra` and `rb` are their representatives found before anything is written. The boolean returned by `join` says whether the wire really merged two islands. A question never writes: it only calls `find` twice and compares the results.

<!-- stage: trace -->
### Wires And Questions In Order

The first trace has eight houses and ten events in the order they happen. A cell such as `L 0-1` is a wire being laid, and `Q 1-2` is a caller asking whether the two houses connect. The pointer `i` marks the current event. The vars show the two representatives found, the number of islands afterwards and a `result` flag: for a wire it is 1 when the wire merged two islands, and for a question it is 1 when the answer is yes. The wire 3-0 arrives after the island of 0, 1, 2 and 3 is already complete, so its result is 0 and the count stays put. The question about houses 5 and 6 is asked once before the wire 5-6 exists and gets a no, and the later question about 5 and 7 gets a yes.

```trace
{"cells":["L 0-1","L 2-3","Q 1-2","L 1-3","Q 0-2","L 3-0","L 6-7","Q 5-6","L 5-6","Q 5-7"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"ra":0,"rb":1,"groups":7,"result":1},"note":"Line 0-1 is laid. Their labels 0 and 1 differ, so the groups fuse and 7 remain."},{"at":{"i":1},"vars":{"ra":2,"rb":3,"groups":6,"result":1},"note":"Line 2-3 is laid. Their labels 2 and 3 differ, so the groups fuse and 6 remain."},{"at":{"i":2},"vars":{"ra":0,"rb":2,"groups":6,"result":0},"note":"Houses 1 and 2 carry labels 0 and 2, so the operator answers no."},{"at":{"i":3},"vars":{"ra":0,"rb":2,"groups":5,"result":1},"note":"Line 1-3 is laid. Their labels 0 and 2 differ, so the groups fuse and 5 remain."},{"at":{"i":4},"vars":{"ra":0,"rb":0,"groups":5,"result":1},"note":"Houses 0 and 2 both carry label 0, so the operator answers yes."},{"at":{"i":5},"vars":{"ra":0,"rb":0,"groups":5,"result":0},"note":"Line 3-0 is laid, but both houses already carry label 0, so the group count stays 5."},{"at":{"i":6},"vars":{"ra":6,"rb":7,"groups":4,"result":1},"note":"Line 6-7 is laid. Their labels 6 and 7 differ, so the groups fuse and 4 remain."},{"at":{"i":7},"vars":{"ra":5,"rb":6,"groups":4,"result":0},"note":"Houses 5 and 6 carry labels 5 and 6, so the operator answers no."},{"at":{"i":8},"vars":{"ra":5,"rb":6,"groups":3,"result":1},"note":"Line 5-6 is laid. Their labels 5 and 6 differ, so the groups fuse and 3 remain."},{"at":{"i":9},"vars":{"ra":6,"rb":6,"groups":3,"result":1},"note":"Houses 5 and 7 both carry label 6, so the operator answers yes."}]}
```

The second trace puts the two methods side by side on a small version of the street. Nine houses get wires 0-1, 1-2 and so on, and after each wire the caller asks whether house 0 reaches the newest house. The vars hold two running totals. The value `dfsWork` is the number of houses a fresh search touches, summed over all questions so far, and `ufWork` is the number of parent hops the label structure has made on all of its traces. The first total climbs faster with every row, which is what the quadratic cost looks like at small scale.

```trace
{"cells":["L 0-1","Q 0-1","L 1-2","Q 0-2","L 2-3","Q 0-3","L 3-4","Q 0-4","L 4-5","Q 0-5","L 5-6","Q 0-6","L 6-7","Q 0-7","L 7-8","Q 0-8"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"dfsWork":0,"ufWork":0},"note":"Line 0-1 is laid. Union-find does its finds; the DFS side stores the line and does no work yet."},{"at":{"i":1},"vars":{"dfsWork":2,"ufWork":1},"note":"The query 0 to 1 is asked. A fresh DFS touches 2 houses, and the running DFS total is 2."},{"at":{"i":2},"vars":{"dfsWork":2,"ufWork":2},"note":"Line 1-2 is laid. Union-find does its finds; the DFS side stores the line and does no work yet."},{"at":{"i":3},"vars":{"dfsWork":5,"ufWork":3},"note":"The query 0 to 2 is asked. A fresh DFS touches 3 houses, and the running DFS total is 5."},{"at":{"i":4},"vars":{"dfsWork":5,"ufWork":4},"note":"Line 2-3 is laid. Union-find does its finds; the DFS side stores the line and does no work yet."},{"at":{"i":5},"vars":{"dfsWork":9,"ufWork":5},"note":"The query 0 to 3 is asked. A fresh DFS touches 4 houses, and the running DFS total is 9."},{"at":{"i":6},"vars":{"dfsWork":9,"ufWork":6},"note":"Line 3-4 is laid. Union-find does its finds; the DFS side stores the line and does no work yet."},{"at":{"i":7},"vars":{"dfsWork":14,"ufWork":7},"note":"The query 0 to 4 is asked. A fresh DFS touches 5 houses, and the running DFS total is 14."},{"at":{"i":8},"vars":{"dfsWork":14,"ufWork":8},"note":"Line 4-5 is laid. Union-find does its finds; the DFS side stores the line and does no work yet."},{"at":{"i":9},"vars":{"dfsWork":20,"ufWork":9},"note":"The query 0 to 5 is asked. A fresh DFS touches 6 houses, and the running DFS total is 20."},{"at":{"i":10},"vars":{"dfsWork":20,"ufWork":10},"note":"Line 5-6 is laid. Union-find does its finds; the DFS side stores the line and does no work yet."},{"at":{"i":11},"vars":{"dfsWork":27,"ufWork":11},"note":"The query 0 to 6 is asked. A fresh DFS touches 7 houses, and the running DFS total is 27."},{"at":{"i":12},"vars":{"dfsWork":27,"ufWork":12},"note":"Line 6-7 is laid. Union-find does its finds; the DFS side stores the line and does no work yet."},{"at":{"i":13},"vars":{"dfsWork":35,"ufWork":13},"note":"The query 0 to 7 is asked. A fresh DFS touches 8 houses, and the running DFS total is 35."},{"at":{"i":14},"vars":{"dfsWork":35,"ufWork":14},"note":"Line 7-8 is laid. Union-find does its finds; the DFS side stores the line and does no work yet."},{"at":{"i":15},"vars":{"dfsWork":44,"ufWork":15},"note":"The query 0 to 8 is asked. A fresh DFS touches 9 houses, and the running DFS total is 44."}]}
```

<!-- stage: code -->
### A Switchboard That Remembers Islands

```java
final class Switchboard {
    private final int[] parent;
    private final int[] size;
    private int groups;

    Switchboard(int houses) {
        parent = new int[houses];
        size = new int[houses];
        for (int h = 0; h < houses; h++) {
            parent[h] = h;
            size[h] = 1;
        }
        groups = houses;
    }

    private int find(int h) {
        while (parent[h] != h) {
            parent[h] = parent[parent[h]];
            h = parent[h];
        }
        return h;
    }

    boolean join(int a, int b) {
        int ra = find(a), rb = find(b);
        if (ra == rb) return false;
        if (size[ra] < size[rb]) {
            int swap = ra;
            ra = rb;
            rb = swap;
        }
        parent[rb] = ra;
        size[ra] += size[rb];
        groups--;
        return true;
    }

    boolean linked(int a, int b) { return find(a) == find(b); }

    int islands() { return groups; }
}
```

The `find` rewrites each visited slot to its grandparent as it climbs, so it needs one loop and no recursion. The method `join` returns false for a wire inside an island, and that early exit is the whole defence against double counting. Asking `linked` never changes `groups`. Time per call is close to constant on average, and memory is two integers per house.

<!-- stage: applicability -->
### When The Question Keeps Changing

Reach for this when facts arrive one at a time and the question after each is "are these two in the same group?" or "how many groups now?". Typical cues are cables added to a network, friend links in a feed, pixels turned on in an image, or records that share an identifier and so must be treated as one thing. The invariant to defend is that equal representatives mean joined by something already added, so every addition must go through the two-representatives step and nothing may write a label from anywhere else.

The false friend is a depth-first search that is correct on one snapshot. It answers a single question well, but it keeps nothing between questions, so alternating wires and questions makes it redo the whole walk each time. The operation count above, about two million touches against 3,997 parent hops for the same 2,000 wires and questions, is the price. Do not use this structure when links can also be removed, because a representative cannot be unpicked once two islands share it, or when the answer needs the actual route between two houses, since labels record membership and nothing else. In Java, `new int[n]` is zero-filled, so skipping the loop that sets `parent[h] = h` makes every house answer to house 0 and every question return yes.

<!-- stage: exercises -->
### Exercises

#### [Build] Online Connect And Query (Author exercise)
<!-- id: ug-online-connect-query -->

**Prerequisites.** The size-aware union and the `find` routine from the two previous lessons.

**Problem.** There are `n` houses numbered 0 to n-1 and no wires. The array `ops` is a list of events applied strictly in order, and each event is `{kind, a, b}`. Kind 0 lays a wire between houses `a` and `b`. Kind 1 asks whether `a` and `b` are joined by a chain of wires laid before this event. Return a `boolean[]` with one entry per question, in the order the questions appear. A house is always joined to itself, and a question never changes anything. The `ops` array is not modified.

**Constraints.** 1 <= n <= 10000, and 0 <= ops.length <= 20000. Every house number is between 0 and n-1, and `kind` is 0 or 1.

**Example 1.** Input `n = 5, ops = [[1,0,4],[0,0,1],[0,3,4],[1,0,4],[0,1,3],[1,0,4]]`, output `[false, false, true]`.

**Example 2.** Input `n = 4, ops = [[0,2,2],[1,2,2],[1,0,3],[0,0,3],[0,3,0],[1,3,0]]`, output `[true, false, true]`.

**Hint.** Which of the two event kinds is allowed to write to the arrays, and how many entries must the result array have before the loop starts?

**Changed decision.** Answers come from comparing two stored labels at the moment of the question, instead of searching the wires laid so far.

#### [Vary] Number Of Provinces (LeetCode 547)
<!-- id: ug-provinces-by-row -->

**Prerequisites.** The Online Connect And Query rung.

**Problem.** The matrix `isConnected` is n by n, symmetric, with `isConnected[i][j] == 1` when cities `i` and `j` are directly linked and 1 on the diagonal. Process the rows in order, and for each row `i` merge city `i` with every city `j` that the row marks as linked. Return an `int[]` of length n, where entry `i` is the number of provinces among all n cities after rows 0 to i have been merged. Cities start out as n separate provinces, so the entries never increase, and the last one is the ordinary province count. The matrix is not modified.

**Constraints.** 1 <= n <= 200, every entry is 0 or 1, `isConnected[i][i] == 1`, and `isConnected[i][j] == isConnected[j][i]`.

**Example 1.** Input `isConnected = [[1,1,0,0],[1,1,0,0],[0,0,1,1],[0,0,1,1]]`, output `[3, 3, 2, 2]`.

**Example 2.** Input `isConnected = [[1,1,1,0,0],[1,1,0,0,0],[1,0,1,1,0],[0,0,1,1,1],[0,0,0,1,1]]`, output `[3, 3, 2, 1, 1]`.

**Hint.** When is the tally allowed to go down, and at which point inside the row loop should an entry be recorded?

**Changed decision.** The structure is built row by row and read after every row, instead of being built completely and read once at the end.

#### [Boundary] Duplicate Union (Author exercise)
<!-- id: ug-duplicate-union -->

**Prerequisites.** The Provinces rung, and the rule that a merge inside one group writes nothing.

**Problem.** There are `n` vertices and a list `edges` that may contain the same edge many times, in either direction, and may contain self-loops. Add the edges one by one. Return a `long[]` of two values: the number of connected components after all edges, and the number of unordered pairs of distinct vertices that lie in the same component. A repeated edge, a reversed copy and a self-loop must leave both numbers exactly as they were before it. The `edges` array is not modified.

**Constraints.** 1 <= n <= 100000 and 0 <= edges.length <= 200000. Every endpoint is between 0 and n-1, and the pair count can exceed the range of `int`.

**Example 1.** Input `n = 5, edges = [[0,1],[1,0],[0,1],[2,3]]`, output `[3, 2]`.

**Example 2.** Input `n = 4, edges = [[0,1],[1,2],[2,0],[3,3]]`, output `[2, 3]`.

**Hint.** What would happen to a component's size if a merge of a group into itself were allowed to run, and which type holds the pair total?

**Changed decision.** An edge whose endpoints already share a representative exits before any write, instead of being merged again.

#### [Recognize] Accounts Merge (LeetCode 721)
<!-- id: ug-accounts-merge -->

**Prerequisites.** The Duplicate Union rung, and a hash map from a string to the first index that used it.

**Problem.** Each `accounts[i]` is a `String[]` whose first entry is a person's name and whose remaining entries are email addresses. Two accounts belong to the same person if they share at least one email, directly or through a chain of other accounts, and every account of one person carries the same name. Two accounts with the same name but no shared email, directly or through a chain, are different people. Return a `List<List<String>>` with one list per person: the name first, then that person's distinct emails in natural `String` order. Sort the outer list by comparing the lists element by element in natural `String` order, shorter first on a tie. The input is not modified.

**Constraints.** 1 <= accounts.length <= 1000, every account has at least one email, and an email may repeat inside one account. Accounts that share an email have the same name.

**Example 1.** Input `accounts = [["Ada","a@x","b@x"],["Bo","c@x"],["Ada","b@x","d@x"],["Ada","e@x"]]`, output `[["Ada","a@x","b@x","d@x"],["Ada","e@x"],["Bo","c@x"]]`.

**Example 2.** Input `accounts = [["Eve","x1","x2"],["Eve","x3"],["Eve","x2","x3"],["Fay","y1"],["Fay","y1","y2"]]`, output `[["Eve","x1","x2","x3"],["Fay","y1","y2"]]`.

**Hint.** What are the elements being merged, what links two of them, and which label is read when the emails are finally grouped?

**Changed decision.** The structure runs over account indices and is driven by a shared email, instead of running over the emails or over the names.
