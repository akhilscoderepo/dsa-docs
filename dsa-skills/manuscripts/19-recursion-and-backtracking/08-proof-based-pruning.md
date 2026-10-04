<!-- lesson-kind: standard -->
<!-- lesson-id: proof-based-pruning -->
## Proof-Based Pruning

<!-- stage: context -->
### The Handcart At Kestrel Dock

A porter at Kestrel Dock loads a handcart that will crack its axle under more than a fixed weight. A heap of crates sits on the quay, each with its weight stamped on the lid, and the harbour office wants a sheet listing every selection of crates that the cart can safely carry, since the crates that go on the morning cart are chosen from that sheet. The porter has lined the crates up from lightest to heaviest.

He started by writing out every selection of crates that could ever be put on the cart, one after another, and weighing each at the end. With thirty crates he was still writing at nightfall. Then an old hand told him that he had been weighing selections that were hopeless long before he finished writing them.

<!-- stage: naive -->
### Write Every Selection Then Weigh It

The direct method lists all 2^n selections of crates, adds up the weights of each one when it is complete, and keeps those whose total is within the limit.

```java
static List<List<Integer>> loadsByWeighing(int[] weights, int limit) {
    int n = weights.length;
    List<List<Integer>> loads = new ArrayList<>();
    for (int mask = 0; mask < (1 << n); mask++) {
        long total = 0;
        List<Integer> load = new ArrayList<>();
        for (int i = 0; i < n; i++) {
            if ((mask >> i & 1) == 1) { load.add(weights[i]); total += weights[i]; }
        }
        if (total <= limit) loads.add(load);
    }
    return loads;
}
```

It is correct for any weights, positive or not, and it is the oracle that the faster search is checked against.

<!-- stage: bottleneck -->
### Overloaded Prefixes Are Still Extended

The method touches all 2^n selections and spends O(n) on each, so it costs O(n * 2^n) whatever the limit. If the cart holds only a handful of crates out of thirty, nearly every selection is overloaded, and many of them were already overloaded when only their first few crates had been decided. A selection that begins with the three heaviest crates is over the limit before any other decision is made, yet the method goes on to write out every one of the 2^27 ways of finishing it and weighs each.

The loop cannot stop early because it does not build selections crate by crate. A search that does build them crate by crate has the chance to look at the partial load. The question is when looking at a partial load is enough to abandon all of its completions, and the answer has to be a proof, since a wrong abandonment silently removes real loads from the sheet.

<!-- stage: insight -->
### Prune Only What You Can Prove

A branch may be abandoned when something proves that no completion of it can be an answer. The cleanest proof rests on a **monotone constraint**: a condition that, once violated by a partial path, stays violated by every extension of it. With positive weights a load only gets heavier as crates are added, so a partial load over the limit makes all its completions overloaded, and the whole subtree can be skipped without being entered.

The second kind of proof is a **proven bound**. It does not say that the partial path already violates something. It says that the best the remaining decisions could achieve still falls short, or cannot beat the best answer found so far. For example, if every crate in the rest of the row is light and their total still cannot reach a required weight, the branch is hopeless, and the argument is arithmetic on the remaining items, not a hunch.

A branch that cannot lead to any answer is a **dead branch**, and the point of pruning is to refuse to enter dead branches. Because the crates are sorted lightest first, one more fact helps: if crate i does not fit in the room that is left, no later crate fits either, so the loop can stop and not merely skip. That exit is justified only by the order, which makes the order part of the proof.

Pruning has a limit that should be stated honestly. It removes work in practice, but the worst case stays exponential, since a limit that every selection satisfies prunes nothing. The invariant is that every pruned branch is covered by a stated monotone constraint or a stated bound, so the pruned search returns exactly what the unpruned search would.

<!-- names: monotone constraint, proven bound, dead branch -->

<!-- stage: variables -->
### Start, Room And Path

The `start` is the first crate the loop may take, as in the earlier lessons. The `room` is the weight the cart can still take, which equals the limit minus the weights on the path, and it is passed down by value, so no undo step is needed for it: the caller's copy is untouched when the call returns. The `path` holds the crates on the cart and does need its removal after each call. The values of `room` and of any sums are kept in `long`, so that large weights cannot wrap around. A call is recorded on arrival, because every call that is entered has already been shown to fit.

<!-- stage: trace -->
### Crates That Fit A Limit Of Eight

The first trace loads crates of weights 2, 3, 5 and 6 under a limit of 8. The pointer `start` is the first crate a call may take, and `i` is the crate under consideration, which reads -1 when a call has just arrived and recorded its load. At some loops the next crate is too heavy and the loop stops at once, which the notes call a stop, and the crates after it are never looked at.

```trace
{"cells":["2","3","5","6"],"pointers":["start","i"],"steps":[{"at":{"start":0,"i":-1},"vars":{"path":"[]","room":8,"calls":1},"note":"The call arrives with the load [], and 8 of weight can still be added, so the load fits and is recorded."},{"at":{"start":0,"i":0},"vars":{"path":"[2]","room":6,"calls":1},"note":"The crate of weight 2 fits, so it goes on the cart and 6 of room remains."},{"at":{"start":1,"i":-1},"vars":{"path":"[2]","room":6,"calls":2},"note":"The call arrives with the load [2], and 6 of weight can still be added, so the load fits and is recorded."},{"at":{"start":1,"i":1},"vars":{"path":"[2, 3]","room":3,"calls":2},"note":"The crate of weight 3 fits, so it goes on the cart and 3 of room remains."},{"at":{"start":2,"i":-1},"vars":{"path":"[2, 3]","room":3,"calls":3},"note":"The call arrives with the load [2, 3], and 3 of weight can still be added, so the load fits and is recorded."},{"at":{"start":2,"i":2},"vars":{"path":"[2, 3]","room":3,"calls":3},"note":"The crate of weight 5 is more than the 3 left, and every later crate is heavier, so the loop stops here."},{"at":{"start":1,"i":1},"vars":{"path":"[2]","room":6,"calls":3},"note":"The crate of weight 3 comes off again, so the path is [2] and 6 of room is back."},{"at":{"start":1,"i":2},"vars":{"path":"[2, 5]","room":1,"calls":3},"note":"The crate of weight 5 fits, so it goes on the cart and 1 of room remains."},{"at":{"start":3,"i":-1},"vars":{"path":"[2, 5]","room":1,"calls":4},"note":"The call arrives with the load [2, 5], and 1 of weight can still be added, so the load fits and is recorded."},{"at":{"start":3,"i":3},"vars":{"path":"[2, 5]","room":1,"calls":4},"note":"The crate of weight 6 is more than the 1 left, and every later crate is heavier, so the loop stops here."},{"at":{"start":1,"i":2},"vars":{"path":"[2]","room":6,"calls":4},"note":"The crate of weight 5 comes off again, so the path is [2] and 6 of room is back."},{"at":{"start":1,"i":3},"vars":{"path":"[2, 6]","room":0,"calls":4},"note":"The crate of weight 6 fits, so it goes on the cart and 0 of room remains."},{"at":{"start":4,"i":-1},"vars":{"path":"[2, 6]","room":0,"calls":5},"note":"The call arrives with the load [2, 6], and 0 of weight can still be added, so the load fits and is recorded."},{"at":{"start":1,"i":3},"vars":{"path":"[2]","room":6,"calls":5},"note":"The crate of weight 6 comes off again, so the path is [2] and 6 of room is back."},{"at":{"start":0,"i":0},"vars":{"path":"empty","room":8,"calls":5},"note":"The crate of weight 2 comes off again, so the path is empty and 8 of room is back."},{"at":{"start":0,"i":1},"vars":{"path":"[3]","room":5,"calls":5},"note":"The crate of weight 3 fits, so it goes on the cart and 5 of room remains."},{"at":{"start":2,"i":-1},"vars":{"path":"[3]","room":5,"calls":6},"note":"The call arrives with the load [3], and 5 of weight can still be added, so the load fits and is recorded."},{"at":{"start":2,"i":2},"vars":{"path":"[3, 5]","room":0,"calls":6},"note":"The crate of weight 5 fits, so it goes on the cart and 0 of room remains."},{"at":{"start":3,"i":-1},"vars":{"path":"[3, 5]","room":0,"calls":7},"note":"The call arrives with the load [3, 5], and 0 of weight can still be added, so the load fits and is recorded."},{"at":{"start":3,"i":3},"vars":{"path":"[3, 5]","room":0,"calls":7},"note":"The crate of weight 6 is more than the 0 left, and every later crate is heavier, so the loop stops here."},{"at":{"start":2,"i":2},"vars":{"path":"[3]","room":5,"calls":7},"note":"The crate of weight 5 comes off again, so the path is [3] and 5 of room is back."},{"at":{"start":2,"i":3},"vars":{"path":"[3]","room":5,"calls":7},"note":"The crate of weight 6 is more than the 5 left, and every later crate is heavier, so the loop stops here."},{"at":{"start":0,"i":1},"vars":{"path":"empty","room":8,"calls":7},"note":"The crate of weight 3 comes off again, so the path is empty and 8 of room is back."},{"at":{"start":0,"i":2},"vars":{"path":"[5]","room":3,"calls":7},"note":"The crate of weight 5 fits, so it goes on the cart and 3 of room remains."},{"at":{"start":3,"i":-1},"vars":{"path":"[5]","room":3,"calls":8},"note":"The call arrives with the load [5], and 3 of weight can still be added, so the load fits and is recorded."},{"at":{"start":3,"i":3},"vars":{"path":"[5]","room":3,"calls":8},"note":"The crate of weight 6 is more than the 3 left, and every later crate is heavier, so the loop stops here."},{"at":{"start":0,"i":2},"vars":{"path":"empty","room":8,"calls":8},"note":"The crate of weight 5 comes off again, so the path is empty and 8 of room is back."},{"at":{"start":0,"i":3},"vars":{"path":"[6]","room":2,"calls":8},"note":"The crate of weight 6 fits, so it goes on the cart and 2 of room remains."},{"at":{"start":4,"i":-1},"vars":{"path":"[6]","room":2,"calls":9},"note":"The call arrives with the load [6], and 2 of weight can still be added, so the load fits and is recorded."},{"at":{"start":0,"i":3},"vars":{"path":"empty","room":8,"calls":9},"note":"The crate of weight 6 comes off again, so the path is empty and 8 of room is back."}]}
```

The second trace is the failure that this lesson guards against. The values are 5 and -5, the target sum is 0, and the search prunes whenever the running sum exceeds the target. The pruning rule is valid for positive values only, so with a negative value present it cuts off a path that would have come back down to the target.

```trace
{"cells":["5","-5"],"pointers":["start","i"],"steps":[{"at":{"start":0,"i":-1},"vars":{"path":"[]","sum":0,"lost":"no"},"note":"The call arrives with the path [] summing to 0, which is the target, so it is counted."},{"at":{"start":0,"i":0},"vars":{"path":"[5]","sum":5,"lost":"yes"},"note":"The sum 5 is above the target, so the careless rule abandons the branch, but the value -5 is still to come and would bring the sum back to 0, so a real answer is lost."},{"at":{"start":0,"i":1},"vars":{"path":"[-5]","sum":-5,"lost":"no"},"note":"The value -5 is taken, so the sum is -5."},{"at":{"start":2,"i":-1},"vars":{"path":"[-5]","sum":-5,"lost":"no"},"note":"The call arrives with the path [-5] summing to -5, which is not the target."},{"at":{"start":0,"i":1},"vars":{"path":"empty","sum":0,"lost":"no"},"note":"The value -5 is removed, so the sum is 0 again."}]}
```

<!-- stage: code -->
### Loop That Stops At The First Misfit

```java
static List<List<Integer>> loads(int[] weights, long limit) {
    List<List<Integer>> out = new ArrayList<>();
    load(weights, 0, limit, new ArrayList<>(), out);
    return out;
}

// weights are positive and ascending; room is what the cart can still carry
private static void load(int[] weights, int start, long room, List<Integer> path, List<List<Integer>> out) {
    out.add(new ArrayList<>(path));                 // every call entered fits
    for (int i = start; i < weights.length; i++) {
        if (weights[i] > room) break;               // monotone: later crates are heavier
        path.add(weights[i]);
        load(weights, i + 1, room - weights[i], path, out);
        path.remove(path.size() - 1);
    }
}
```

Both parts of the stop rest on stated facts: the weights are positive, so a load never gets lighter, and the weights ascend, so the first misfit ends the loop. Remove either fact and the `break` is wrong. Because only fitting crates are ever entered, the number of calls equals the number of loads that fit, and each costs a copy for its record.

<!-- stage: applicability -->
### Constraints That Only Get Worse

Use proof-based pruning when partial paths have a property that can only get worse as they grow: a total that rises with positive terms, a count of conflicts that never falls, or a cost that has a known floor for the rest of the path. It also applies when the remaining items give a bound strong enough to rule out reaching the goal. The invariant to hold on to is that each skipped branch has a written reason, and the reason is a fact about all its completions.

The nearest false friend is pruning because a branch looks poor, such as skipping the heaviest crates since they seem wasteful, or stopping a search once it has produced enough answers that look good. Such rules may be fast, and they remove real answers without anyone noticing. A second false friend is a valid rule moved into a setting where its premise fails, as when a prune on a running sum meets negative values, or an early exit relies on an order that the input does not have.

Do not prune when the data can break the premise, and test any pruned search against the unpruned one on small random inputs, which is the safest guard. Pruning also does not change the worst case, so a problem whose every path is valid still takes exponential time. Keep sums in `long` when weights can be large, and pass shrinking numbers by value so that they restore themselves.

<!-- stage: exercises -->
### Exercises

#### [Build] Positive Remaining Sum (Author exercise)
<!-- id: bt-positive-budget -->

**Prerequisites.** The increasing-start search for subsets, and the exit from a loop at the first value that is too large.

**Problem.** Given positive integers in ascending order and a budget, count the subsets, empty one included, whose sum is at most the budget, where each position is used at most once. Return a pair `[count, calls]`, where `calls` is the number of times the recursive method runs when its loop stops at the first value larger than the remaining budget.

**Constraints.** 0 <= nums.length <= 14, the values are positive, ascending and at most 30, and 0 <= budget <= 60.

**Example 1.** Input `nums = [2, 3, 4]`, `budget = 6`, output `[6, 6]`.

**Example 2.** Input `nums = [5, 6]`, `budget = 4`, output `[1, 1]`.

**Hint.** What does it say about the number of calls if the method is entered only when the load already fits?

**Changed decision.** The method is entered only for loads that already fit, so every call stands for one counted subset and none is wasted.

#### [Vary] Remaining-Slots Bound (Author exercise)
<!-- id: bt-nonadjacent-slots -->

**Prerequisites.** The Positive Remaining Sum rung, and the room bound of the combinations lesson.

**Problem.** Given `n` and `k`, return every increasing list of `k` positions from 0 to `n - 1` in which no two positions are neighbours, in the order the search finds them. A call that still needs `need` positions must stop its loop at the largest position that leaves room for those picks and the gaps between them.

**Constraints.** 1 <= n <= 12 and 0 <= k <= 8.

**Example 1.** Input `n = 5`, `k = 2`, output `[[0, 2], [0, 3], [0, 4], [1, 3], [1, 4], [2, 4]]`.

**Example 2.** Input `n = 4`, `k = 3`, output `[]`.

**Hint.** How many positions do `need` picks occupy, counting the empty position that must separate each pair?

**Changed decision.** Each remaining pick needs two positions of room, one for itself and one for its gap, so the loop bound is stricter than in the plain combinations search.

#### [Boundary] Negative Values Break Sum Pruning (Author exercise)
<!-- id: bt-negative-breaks-prune -->

**Prerequisites.** The Remaining-Slots Bound rung.

**Problem.** Given integers that may be negative or zero and a target, count the subsets, empty one included, whose sum equals the target, each position used at most once. Prune only on a proven bound: abandon a branch when the sum still needed is below the lowest sum, or above the highest sum, that the unused positions can produce.

**Constraints.** 0 <= nums.length <= 14, the values are integers between -9 and 9, and the target is between -30 and 30.

**Example 1.** Input `nums = [5, -5]`, `target = 0`, output `2`.

**Example 2.** Input `nums = [3, -2, 4, -1]`, `target = 2`, output `2`.

**Hint.** If a partial sum is already above the target and a negative value is still to come, can the sum come back?

**Changed decision.** The rule changes from stopping when the partial sum exceeds the target to comparing the need with the lowest and highest sums of what remains.

#### [Recognize] N-Queens Rejections (LeetCode 51)
<!-- id: bt-queens-rejected -->

**Prerequisites.** The Negative Values Break Sum Pruning rung.

**Problem.** Place one queen in each row of an `n` by `n` board so that no two share a column or a diagonal. Fill rows from the top, trying columns from left to right, and refuse a square at once if its column or either diagonal is occupied. Return `[solutions, rejected]`, where `rejected` is the number of squares refused for that reason during the whole search.

**Constraints.** 1 <= n <= 8, a board small enough to search in full.

**Example 1.** Input `n = 4`, output `[2, 44]`.

**Example 2.** Input `n = 3`, output `[0, 13]`.

**Hint.** Once two queens attack each other, can any later placement repair the conflict?

**Changed decision.** The answer is a count of solutions and refusals and not the boards, and a refusal is justified by a conflict that no later row can undo.
