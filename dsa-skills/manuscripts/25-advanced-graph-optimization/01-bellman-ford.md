<!-- lesson-kind: standard -->
<!-- lesson-id: bellman-ford -->
## Find Shortest Paths With Negative Edges

<!-- stage: context -->
### A Rebate Makes The Longer Route Cheaper

A payment platform moves money between accounts through partner banks. Every transfer charges a fee, but some transfers pay a rebate, which is a negative fee. Account 0 must reach account 1. The direct transfer charges 4. The route through account 2 charges 6 for the first transfer and then pays a rebate of 5 for the second, so its net fee is only 1. A planner that trusts the first fee it sees overpays by 3.

Treat the graph as directed. Each account is a vertex with a number from 0 to n - 1, and each transfer is an edge that carries a **weight**, the fee, which may be negative. The cost of a route is the sum of its weights. The task is to find the lowest total fee from one source account to every other account. The method also reports each account that no route reaches. The method reads the arrays it receives and never changes them.

This lesson asks how a search stays correct when a transfer that comes later can lower a fee that already looked final.

<!-- stage: naive -->
### Finishing The Cheapest Account First

The familiar tool for lowest-cost routes is the greedy search from the previous chapter. It repeatedly picks the unfinished account with the smallest known fee, marks that account finished, and updates the fees of the accounts it sends to. A finished account is never updated again.

```java
static long[] finishCheapest(int n, int[][] transfers, int src) {
    long[] fee = new long[n];
    Arrays.fill(fee, Long.MAX_VALUE);
    fee[src] = 0;
    boolean[] finished = new boolean[n];
    for (int pass = 0; pass < n; pass++) {
        int u = -1;
        for (int v = 0; v < n; v++) {
            if (!finished[v] && fee[v] != Long.MAX_VALUE && (u == -1 || fee[v] < fee[u])) u = v;
        }
        if (u == -1) break;
        finished[u] = true;
        for (int[] t : transfers) {
            if (t[0] == u && !finished[t[1]] && fee[u] + t[2] < fee[t[1]]) fee[t[1]] = fee[u] + t[2];
        }
    }
    return fee;
}
```

Each pass finishes one account and scans every transfer once, so the method does O(V * E) work. It reaches exactly the accounts that have a route. The open question is whether the stored fee of a finished account is the lowest one.

```predict
Use the transfers 0 to 1 with fee 4, 0 to 2 with fee 6, and 2 to 1 with fee -5. What fee does finishCheapest store for account 1?

It stores 4, which is wrong. Account 0 finishes first and sets account 1 to 4 and account 2 to 6. Account 1 has the smaller fee, so it finishes next. When account 2 finishes later, the rebate would give account 1 a fee of 1, but the check for finished accounts rejects the update. The true minimum is 1. The method treats the smallest known fee as final, and a rebate that arrives later breaks that belief.
```

<!-- stage: bottleneck -->
### Later Rebates Reach Finished Accounts

The greedy method works only when a longer route never costs less than the shorter route that it extends. A rebate removes that guarantee. An account with a small fee can still be improved by a route that first pays a large fee and then collects a larger rebate. The search has already stopped looking there.

Updating a finished account again does not fix the problem alone. Every account that depends on the changed fee needs another update too, and the update order decides how often the work repeats. With no bound on the repetition, a loop of transfers whose fees add up to less than zero keeps lowering the same fees forever, so the search never stops.

Listing every route that visits each account at most once gives correct answers, but the number of such routes grows like (V - 1)!, which is exponential. A usable method needs a fixed bound on the work, correct answers when a cheapest route exists, and a clear signal when none exists. The next section finds a bound of O(V * E) edge checks by organizing the work by the number of transfers in a route.

<!-- stage: insight -->
### Improving Fees One Layer At A Time

The method keeps a best known fee for every account and improves all fees together in passes. Pass `i` allows routes with one more transfer than pass `i - 1`.

<!-- names: snapshot, relax, negative cycle -->

#### A Cheapest Route Has Few Transfers

Suppose a route visits some account twice. The part between the two visits is a loop that returns to the same account. If the fees of the loop add up to zero or more, cutting the loop out does not raise the cost of the route. So when no loop has a total below zero, some cheapest route visits every account at most once. A route over n accounts that never repeats an account uses at most n - 1 transfers.

#### Fees Grouped By Transfer Count

The array `dist` holds the lowest known fee from the source to each account, with `Long.MAX_VALUE` for an account that has no known route. Before any pass, only the source has a fee, which is 0. After pass `i`, `dist[v]` is the lowest fee over all routes to `v` that use at most `i` transfers. This sentence carries the entire method, because every later pass merely extends the allowed transfer count by one.

#### Relaxing Every Transfer Once

To **relax** a transfer from `u` to `v` with weight `w`, the method computes `dist[u] + w` and compares it with `dist[v]`. When the sum is smaller, the method stores it in `dist[v]`. One pass relaxes every transfer in the list exactly once, in list order. Since a cheapest route needs at most n - 1 transfers, n - 1 passes are enough.

#### Reading A Snapshot Of The Previous Pass

A **snapshot** is a copy of `dist` taken at the start of a pass. Every relaxation in that pass reads the fee of `u` from the snapshot and writes only into `dist`. Skipping the snapshot lets an improvement written early feed a later transfer within the same pass. A pass could then chain two or three transfers, which breaks the transfer-count statement above. Final answers survive that shortcut, but any problem with a cap on transfers does not.

#### Detecting A Negative Cycle

A **negative cycle** is a loop of transfers whose fees add up to less than zero. When the source reaches such a loop, every extra lap lowers the fee again, so no lowest fee exists. In that case n - 1 passes are not enough, and pass n still finds an improvement. Without a reachable negative cycle, pass n finds none. So the method runs one extra pass and reports a negative cycle when that pass improves any fee.

#### Why Infinity Needs A Guard

An unknown fee is `Long.MAX_VALUE`. Adding a positive weight to it wraps around to a large negative number. Adding a negative weight gives a value just below the maximum, which looks like a real fee and would spread through the array. So the method skips every transfer whose source account is still unknown.

<!-- stage: variables -->
### Fee Array, Snapshot, And Change Flag

The method reads `n`, the list `edges` of triples `[from, to, weight]`, and the source `src`. It changes none of them. It keeps three working values.

- **dist** is a `long[]` of length `n`; `Long.MAX_VALUE` marks an account with no known route.
- **prev** is a copy of `dist` taken at the start of the pass; relaxations read only from it.
- **changed** is a `boolean` that records whether the pass lowered any entry of `dist`.

When a pass leaves `changed` false, no later pass can improve anything, because the next pass would read the same values. The method then stops early.

<!-- stage: trace -->
### Two Runs On Small Transfer Maps

#### Six Accounts With Rebates

The first map lists eight transfers in a fixed order. Account 0 charges 6, 5 and 5 to reach accounts 1, 2 and 3. Account 1 pays a rebate of 1 toward account 4. Account 2 pays a rebate of 2 toward account 1 and charges 1 toward account 4. Account 3 pays rebates of 2 and 1 toward accounts 2 and 5. Each cell shows the table after one pass, and the pointer `pass` selects it. The variable `improved` counts entries that dropped, and `reached` counts entries with a known fee.

The early passes discover accounts and lower fees in bulk. Account 4 needs the longest route, which follows accounts 3, 2 and 1 and uses four transfers, so its final fee of 0 appears only in pass 4. Pass 5 changes nothing, which lets the method stop. The final fees are 0, 1, 3, 5, 0 and 4.

```trace
{"cells":["start","pass 1","pass 2","pass 3","pass 4","pass 5"],"pointers":["pass"],"steps":[{"at":{"pass":0},"vars":{"improved":0,"reached":1},"note":"Before pass 1, the table holds only the source fee: [0, unknown, unknown, unknown, unknown, unknown]."},{"at":{"pass":1},"vars":{"improved":3,"reached":4},"note":"Pass 1 reads the start values and improves 3 entries; the table now reads [0, 6, 5, 5, unknown, unknown]."},{"at":{"pass":2},"vars":{"improved":4,"reached":6},"note":"Reading the previous table, pass 2 writes 4 cheaper entries, giving [0, 3, 3, 5, 5, 4]."},{"at":{"pass":3},"vars":{"improved":2,"reached":6},"note":"In pass 3, 2 entries drop below the stored value, leaving [0, 1, 3, 5, 2, 4]."},{"at":{"pass":4},"vars":{"improved":1,"reached":6},"note":"Pass 4 still finds 1 cheaper entry, and the table becomes [0, 1, 3, 5, 0, 4]."},{"at":{"pass":5},"vars":{"improved":0,"reached":6},"note":"Pass 5 finds nothing cheaper, so the table stays [0, 1, 3, 5, 0, 4] and the method stops."}]}
```

#### A Loop With A Negative Total

The second map lists four transfers. Account 0 charges 2 toward account 1. Account 1 pays a rebate of 3 toward account 2, while account 2 charges 1 to return, so that loop totals -2. Account 2 also charges 4 toward account 3. Because account 0 reaches the loop, no lowest fees exist. Four accounts allow three ordinary passes, and the variable `limit` holds that number.

Pass 4 is the extra pass, and it still improves. It lowers account 2 from -1 to -3. That drop proves a reachable negative cycle, so the method reports failure.

```trace
{"cells":["start","pass 1","pass 2","pass 3","pass 4"],"pointers":["pass"],"steps":[{"at":{"pass":0},"vars":{"improved":0,"reached":1,"limit":3},"note":"Before pass 1, the table holds only the source fee: [0, unknown, unknown, unknown]."},{"at":{"pass":1},"vars":{"improved":1,"reached":2,"limit":3},"note":"Pass 1 reads the start values and improves 1 entry; the table now reads [0, 2, unknown, unknown]."},{"at":{"pass":2},"vars":{"improved":1,"reached":3,"limit":3},"note":"Reading the previous table, pass 2 writes 1 cheaper entry, giving [0, 2, -1, unknown]."},{"at":{"pass":3},"vars":{"improved":2,"reached":4,"limit":3},"note":"In pass 3, 2 entries drop below the stored value, leaving [0, 0, -1, 3]."},{"at":{"pass":4},"vars":{"improved":1,"reached":4,"limit":3},"note":"Pass 4 still finds 1 cheaper entry, and the table becomes [0, 0, -3, 3]. This pass is the extra one, so a negative cycle is reachable."}]}
```

<!-- stage: code -->
### Bellman-Ford With A Snapshot Per Pass

The method returns a `long[]` in which `Long.MAX_VALUE` marks an unreachable account. It returns `null` when a negative cycle is reachable from the source. The snapshot uses `clone`, which copies the whole array in O(V) time.

```java
static long[] bellmanFord(int n, int[][] edges, int src) {
    long[] dist = new long[n];
    Arrays.fill(dist, Long.MAX_VALUE);
    dist[src] = 0;
    for (int pass = 1; pass <= n - 1; pass++) {
        long[] prev = dist.clone();
        boolean changed = false;
        for (int[] e : edges) {
            if (prev[e[0]] == Long.MAX_VALUE) continue;
            long next = prev[e[0]] + e[2];
            if (next < dist[e[1]]) {
                dist[e[1]] = next;
                changed = true;
            }
        }
        if (!changed) return dist;
    }
    for (int[] e : edges) {
        if (dist[e[0]] != Long.MAX_VALUE && dist[e[0]] + e[2] < dist[e[1]]) return null;
    }
    return dist;
}
```

The skip of unknown sources must come before the sum, so the sum never starts from the marker. The early return inside the loop is valid because every later pass would repeat an unchanged pass unchanged. The final loop is the extra pass, and it only reads, since a single improvement is enough to answer. The method runs in O(V * (V + E)) time, because each of at most n - 1 passes copies the array and scans every edge. It uses O(V) memory for `dist` and `prev`, not counting the input.

<!-- stage: applicability -->
### Recognizing Negative Fee Problems

#### Reading The Cue

Use this method when the statement gives weighted edges that may be negative, or when it limits the number of edges a route may use. Refunds and price adjustments both produce negative weights. A cap such as at most k transfers asks for the same pass structure. The answer is usually a distance array, one distance to a target, or a report that the distances do not exist.

#### Checking The Invariant

An **invariant** is a statement about the state that holds before and after every step. Here, after pass `i`, each finite `dist[v]` is the lowest fee over routes with at most `i` transfers, and every finite entry is the cost of a real route. The snapshot protects the first half, and the skip of unknown sources protects the second half. Test an unreachable account, which must keep the marker. Test a graph whose negative cycle cannot be reached from the source, which must not stop the answer. Test one account alone, where zero passes run and the extra pass only checks self loops.

#### Avoiding The False Friend

A **false friend** is a well-known technique that seems to apply but returns wrong answers on some inputs. Here the false friend is the greedy search that finishes the smallest fee first. It is correct for nonnegative weights, and the first example of this lesson shows how a rebate breaks it. A second false friend is adding a constant to every weight to remove the negatives. A route with more transfers gains more of the constant, so the cheapest route can change. A third is reading the answer after a fixed number of passes without the extra pass, which silently returns wrong fees when a reachable negative cycle exists.

<!-- stage: exercises -->
### Exercises

#### [Build] One Relaxation Pass (Author exercise)
<!-- id: ga-bf-one-pass -->

**Prerequisites.** The relaxation and snapshot steps of this lesson.

**Problem.** An array `dist` of type `long[]` holds a fee for each account, and `Long.MAX_VALUE` means that no route is known. Each triple `[u, v, w]` in `edges` is a transfer from `u` to `v` with fee `w`. Return a new `long[]` that results from one pass. For every transfer in which `dist[u]` is known, propose `dist[u] + w` for account `v`. Each account keeps the smallest of its old fee and all proposals. Proposals read only the old array.

**Constraints.** The limits are:
- **Accounts** satisfy `1 <= dist.length <= 1000`, and `u` and `v` are valid indices.
- **Transfers** satisfy `0 <= edges.length <= 5000`, and repeats and self loops may occur.
- **Weight** satisfies `-1000000 <= w <= 1000000`.
- **Distances** are `Long.MAX_VALUE` or lie in `-10^12..10^12`.
- **Mutation** is not allowed, because the input array stays unchanged.

**Example 1.** Input `dist = [0,9223372036854775807,9223372036854775807,9223372036854775807]`, `edges = [[0,1,4],[1,2,-2],[2,3,1]]`, output `[0,4,9223372036854775807,9223372036854775807]`.

**Example 2.** Input `dist = [0,5,9223372036854775807]`, `edges = [[0,1,7],[1,2,-3],[0,2,9]]`, output `[0,5,2]`.

**Hint.** If the method wrote account 1 first and then read it for the next transfer, how many transfers would one pass use in the first example?

**Changed decision.** The method reads each proposal from the old array and writes into a copy. It also skips unknown sources, so no sum starts from the marker.

#### [Vary] Cheapest Flights Within K Stops (LeetCode 787)
<!-- id: ga-bf-flights-by-limit -->

**Prerequisites.** The exercise above.

**Problem.** There are `n` cities numbered from 0. Each entry `[a, b, p]` of `flights` is a one-way flight from `a` to `b` with price `p`, which may be negative to model a credit. A route from `src` to `dst` is a sequence of flights in which each flight starts where the previous one ends. Its stops are the cities between the first and last flight. Return an `int[]` of length `k + 1`. Entry `j` is the lowest total price over routes from `src` to `dst` with at most `j` stops, or `Integer.MAX_VALUE` when no such route exists.

**Constraints.** The limits are:
- **Cities** satisfy `2 <= n <= 60`, and `src != dst` with both in `0..n-1`.
- **Flights** satisfy `0 <= flights.length <= 300`, and parallel flights and loops may occur.
- **Prices** satisfy `-100 <= p <= 1000`, and a loop with a negative total may exist.
- **Limit** satisfies `0 <= k <= n`.

**Example 1.** Input `n = 4`, `flights = [[0,1,100],[1,2,100],[2,3,100],[0,3,500]]`, `src = 0`, `dst = 3`, `k = 2`, output `[500,500,300]`.

**Example 2.** Input `n = 3`, `flights = [[0,1,50],[1,2,-20],[0,2,40]]`, `src = 0`, `dst = 2`, `k = 1`, output `[40,30]`.

**Hint.** After which pass does a route with j stops first appear in the fee array, and why does a negative loop stay harmless with a fixed pass count?

**Changed decision.** The method reads the destination after every pass and stores it, instead of reading it once at the end. It never checks for a negative cycle, because the pass count is fixed by the limit.

#### [Boundary] Unreachable And Negative Cycle (Author exercise)
<!-- id: ga-bf-unreachable-cycle -->

**Prerequisites.** The two exercises above.

**Problem.** Consider `n` accounts numbered from 0 and the one-way transfers in `edges`, where each triple `[a, b, w]` has fee `w`. Return a `long[]` `d` of length `n`. Entry `d[v]` is the lowest total fee from account 0 to account `v`, or `Long.MAX_VALUE` when no route exists. If a loop with a negative total fee is reachable from account 0, return an empty array. A negative loop that account 0 cannot reach does not change the result.

**Constraints.** The limits are:
- **Accounts** satisfy `1 <= n <= 500`.
- **Transfers** satisfy `0 <= edges.length <= 3000`, and repeats and self loops may occur.
- **Weight** satisfies `-1000000000 <= w <= 1000000000`.
- **Sums** may exceed the range of `int`, and the result uses `long`.

**Example 1.** Input `n = 3`, `edges = [[0,1,5],[1,2,-3],[2,1,1]]`, output `[]`.

**Example 2.** Input `n = 5`, `edges = [[0,1,3],[1,2,-2],[3,4,-5],[4,3,1]]`, output `[0,3,1,9223372036854775807,9223372036854775807]`.

**Hint.** What happens to the sum when the source fee is `Long.MAX_VALUE` and the weight is negative, and which pass proves the cycle?

**Changed decision.** The method skips unknown sources before any sum, and it runs one more pass after n - 1 passes. An improvement in that pass means the answer is the empty array.

#### [Recognize] Negative-Edge Shortest Paths (Author exercise)
<!-- id: ga-bf-negative-edge-paths -->

**Prerequisites.** All three exercises above.

**Problem.** A settlement system has accounts numbered from 0. Each triple `[a, b, w]` in `transfers` moves funds from `a` to `b` with net fee `w`, which is negative for a rebate. No loop with a negative total fee is reachable from account 0. Among the accounts other than 0 that account 0 can reach, find the one with the lowest net fee, taking the smallest index on a tie. Return a `long[]` of length 2 with that account and its fee, or `{-1, 0}` when account 0 reaches no other account.

**Constraints.** The limits are:
- **Accounts** satisfy `1 <= n <= 400`.
- **Transfers** satisfy `0 <= transfers.length <= 2500`, and repeats and self loops may occur.
- **Fee** satisfies `-100000 <= w <= 100000`.
- **Guarantee** states that no negative loop is reachable from account 0.

**Example 1.** Input `n = 4`, `transfers = [[0,1,4],[0,2,6],[2,1,-5],[1,3,3]]`, output `[1,1]`.

**Example 2.** Input `n = 4`, `transfers = [[0,1,2],[2,3,-4],[3,2,1]]`, output `[1,2]`.

**Hint.** Which accounts may enter the comparison for the lowest fee, and why does the loop on accounts 2 and 3 not matter in the second example?

**Changed decision.** The method computes all fees with early stopping and then scans only reachable accounts other than 0. The usual statement asks for one target and does not ask for a minimum over accounts.
