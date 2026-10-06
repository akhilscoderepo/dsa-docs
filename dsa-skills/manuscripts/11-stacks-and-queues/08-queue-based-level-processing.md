<!-- lesson-kind: standard -->
<!-- lesson-id: queue-based-level-processing -->
## Group Queue Items By Level

<!-- stage: context -->
### A Crawl Report Without Boundaries

A link checker starts at one page and follows every link it finds. A plain queue visits the pages in a sensible order. The first page comes out, its links go in at the back, and the next page comes out from the front. The report that the team wants says more. It lists the pages that are one click from the start, then the pages that are two clicks away, and so on, so the team can see how deep a broken link sits.

The queue loop prints one long list. Nothing in that list marks where the pages of one click count end and the next ones begin. The lesson answers one question. How can one loop over a single queue stop exactly at the end of each level, without extra data stored on each item?

<!-- stage: naive -->
### Record Each Depth Then Regroup

The direct approach runs the usual queue loop and writes down the depth of every item as it is discovered. A child gets the depth of its parent plus one. After the loop ends, a second pass collects the items of each depth into a list.

```java
static List<List<Integer>> levelsBySweeping(int[] start, int[][] children) {
    ArrayDeque<Integer> queue = new ArrayDeque<>();
    int[] depth = new int[children.length];
    List<Integer> order = new ArrayList<>();
    for (int s : start) queue.offer(s);
    while (!queue.isEmpty()) {
        int id = queue.poll();
        order.add(id);
        for (int c : children[id]) {
            depth[c] = depth[id] + 1;
            queue.offer(c);
        }
    }
    int levelCount = 0;
    for (int id : order) levelCount = Math.max(levelCount, depth[id] + 1);
    List<List<Integer>> result = new ArrayList<>();
    for (int d = 0; d < levelCount; d++) {
        List<Integer> level = new ArrayList<>();
        for (int id : order) if (depth[id] == d) level.add(id);
        result.add(level);
    }
    return result;
}
```

The result is correct. The items of each level keep their discovery order, because the final pass reads `order` from front to back.

<!-- stage: bottleneck -->
### The Regrouping Pass Repeats Whole Scans

```predict
A crawl follows a chain of 100000 pages, where each page links to exactly one new page. How many depth comparisons does the regrouping pass make?

About 10^10 comparisons. The chain has 100000 levels, and the pass reads all 100000 entries of `order` once for every level.
```

The queue loop costs O(n) for `n` items. The regrouping pass costs O(n * L) for `L` levels, because it scans the whole `order` list once per level. A chain makes `L` equal to `n`, so the pass costs O(n^2). The loop also needs an array indexed by item id, so the method cannot handle items that have no small integer id.

The pass repeats work because the queue already holds the information it needs. The items of one level sit next to each other in the queue at the moment that level begins. The method throws that grouping away by polling everything into one flat list. It then rebuilds the grouping from stored depths with repeated scans.

<!-- stage: insight -->
### Drain Exactly One Level At A Time

The queue itself already separates the levels. The loop only needs to know how many items to take before it stops.

<!-- names: current batch, level size, level number -->

#### The Queue Holds Whole Levels

A queue returns items in the order they entered. Every item of level `d` is discovered while the loop processes level `d - 1`. So every item of level `d` enters the queue after all items of level `d - 1` and before all items of level `d + 1`. When the loop has finished level `d - 1`, the queue holds exactly the items of level `d`. This group is the **current batch**. The invariant is that, at the start of each outer iteration, the queue contains the current batch and nothing else.

#### Capture The Size Before Polling

The **level size** is the value of `queue.size()` read once at the start of the batch. The inner loop polls exactly that many items. Each polled item appends its children to the back of the queue. Those children belong to the next batch, and they sit behind all remaining items of the current batch. The loop must not read `queue.size()` again in the inner loop condition. The size grows with every append, so a second read would pull next-level items into the current batch.

#### Count Levels While Draining

The outer loop runs once per batch. The **level number** starts at 0 and increases by 1 after each inner loop finishes. A result list needs no stored depth per item, because the position of a batch in the result equals its level number. The total cost is O(n), because each item is polled once and each append happens once.

<!-- stage: variables -->
### What The Two Loops Keep

The method keeps four pieces of state.

- **queue** holds the items that are waiting, and at the start of each batch it holds one whole level.
- **levelSize** is the number of items in the current batch, read once before the inner loop and never changed during it.
- **level** is the list of ids polled in the current batch, in the order they left the queue.
- **result** is the list of finished levels, and its length equals the level number of the batch in progress.

The queue changes on every poll and every append. The `levelSize` value changes once per outer iteration.

<!-- stage: trace -->
### Walking Through Three Levels

#### Four Levels In A Small Tree

The first trace starts with item 0. Item 0 appends the children 1 and 2. Item 1 appends 3 and 4. Item 2 appends 5, and item 4 appends 6. The cells are the item ids, and the pointer `id` marks the item that was just polled. A step with the pointer past the last cell marks a point where no item was polled.

Each outer iteration begins with a step that shows the captured size. The queue lists the items from front to back. In the second iteration the size is 2, so the loop polls 1 and 2 only. By the time item 2 is polled, the queue already holds 3, 4 and 5, but they wait for the next iteration.

```trace
{"cells":[0,1,2,3,4,5,6],"pointers":["id"],"steps":[{"at":{"id":7},"vars":{"queue":"[0]","levelSize":1},"note":"A level begins. The captured size is 1."},{"at":{"id":0},"vars":{"queue":"[1, 2]","levelSize":1,"level":"[0]"},"note":"Poll 0 and append [1, 2]."},{"at":{"id":7},"vars":{"queue":"[1, 2]","levelSize":2},"note":"A level begins. The captured size is 2."},{"at":{"id":1},"vars":{"queue":"[2, 3, 4]","levelSize":2,"level":"[1]"},"note":"Poll 1 and append [3, 4]."},{"at":{"id":2},"vars":{"queue":"[3, 4, 5]","levelSize":2,"level":"[1, 2]"},"note":"Poll 2 and append [5]."},{"at":{"id":7},"vars":{"queue":"[3, 4, 5]","levelSize":3},"note":"A level begins. The captured size is 3."},{"at":{"id":3},"vars":{"queue":"[4, 5]","levelSize":3,"level":"[3]"},"note":"Poll 3 and append nothing."},{"at":{"id":4},"vars":{"queue":"[5, 6]","levelSize":3,"level":"[3, 4]"},"note":"Poll 4 and append [6]."},{"at":{"id":5},"vars":{"queue":"[6]","levelSize":3,"level":"[3, 4, 5]"},"note":"Poll 5 and append nothing."},{"at":{"id":7},"vars":{"queue":"[6]","levelSize":1},"note":"A level begins. The captured size is 1."},{"at":{"id":6},"vars":{"queue":"[]","levelSize":1,"level":"[6]"},"note":"Poll 6 and append nothing."}]}
```

#### Size Grows While A Level Drains

The second trace uses a larger fan-out. Item 0 appends 1, 2 and 3. Item 1 appends 4, and item 3 appends 5 and 6. The vars show both the captured size and the live value of `queue.size()`.

During the second level, the captured size stays 3. The live size is 3 after polling item 1, because item 4 joined the queue. A loop that compared against the live size would keep running past item 3. The captured size stops the inner loop after exactly three polls.

```trace
{"cells":[0,1,2,3,4,5,6],"pointers":["id"],"steps":[{"at":{"id":7},"vars":{"queue":"[0]","levelSize":1,"queue.size()":1},"note":"A level begins. The captured size is 1."},{"at":{"id":0},"vars":{"queue":"[1, 2, 3]","levelSize":1,"level":"[0]","queue.size()":3},"note":"Poll 0 and append [1, 2, 3]."},{"at":{"id":7},"vars":{"queue":"[1, 2, 3]","levelSize":3,"queue.size()":3},"note":"A level begins. The captured size is 3."},{"at":{"id":1},"vars":{"queue":"[2, 3, 4]","levelSize":3,"level":"[1]","queue.size()":3},"note":"Poll 1 and append [4]."},{"at":{"id":2},"vars":{"queue":"[3, 4]","levelSize":3,"level":"[1, 2]","queue.size()":2},"note":"Poll 2 and append nothing."},{"at":{"id":3},"vars":{"queue":"[4, 5, 6]","levelSize":3,"level":"[1, 2, 3]","queue.size()":3},"note":"Poll 3 and append [5, 6]."},{"at":{"id":7},"vars":{"queue":"[4, 5, 6]","levelSize":3,"queue.size()":3},"note":"A level begins. The captured size is 3."},{"at":{"id":4},"vars":{"queue":"[5, 6]","levelSize":3,"level":"[4]","queue.size()":2},"note":"Poll 4 and append nothing."},{"at":{"id":5},"vars":{"queue":"[6]","levelSize":3,"level":"[4, 5]","queue.size()":1},"note":"Poll 5 and append nothing."},{"at":{"id":6},"vars":{"queue":"[]","levelSize":3,"level":"[4, 5, 6]","queue.size()":0},"note":"Poll 6 and append nothing."}]}
```

<!-- stage: code -->
### Writing The Two Loops

#### One Method For All Levels

The outer loop runs while the queue is non-empty. The inner loop runs a fixed number of times.

```java
static List<List<Integer>> levels(int[] start, int[][] children) {
    List<List<Integer>> result = new ArrayList<>();
    ArrayDeque<Integer> queue = new ArrayDeque<>();
    for (int s : start) queue.offer(s);
    while (!queue.isEmpty()) {
        int levelSize = queue.size();
        List<Integer> level = new ArrayList<>();
        for (int k = 0; k < levelSize; k++) {
            int id = queue.poll();
            level.add(id);
            for (int c : children[id]) queue.offer(c);
        }
        result.add(level);
    }
    return result;
}
```

#### A Marker Cannot Be Null

Some solutions append a marker after each level and detect the marker when it is polled. A `null` marker fails with an `ArrayDeque`, because `offer(null)` throws a `NullPointerException`. The size capture above needs no marker at all.

The method runs in O(n) time and O(w) extra space, where `w` is the widest level. The result lists add O(n) more for the output itself.

<!-- stage: applicability -->
### When Levels Matter To The Output

#### Recognize The Cue

Use the two loops when the answer must separate items by their distance from the start, or by the round in which they were produced. A report grouped by hops, a count of rounds until a target appears, and a per-level aggregate all fit. The invariant is that each outer iteration starts with exactly one level in the queue. A later chapter applies the same loops to trees.

#### Two False Friends

The first false friend is a loop `for (int k = 0; k < queue.size(); k++)`. It reads like the correct loop and gives wrong groups as soon as an item has a child. The second false friend is a level count taken from `queue.size()` at the end of the inner loop. That value includes the next batch.

#### When It Does Not Apply

The method counts hops. It does not measure weighted distance, so edges with different costs need a different structure. It also needs the graph to be traversed so that no item is added twice. A graph with cycles needs a visited check, which the earlier traversal lesson introduced. If the answer needs only the order of discovery and no grouping, the plain queue loop is enough and the extra size capture adds nothing.

<!-- stage: exercises -->
### Exercises

#### [Build] Process Queue In Batches (Author exercise)
<!-- id: sq-process-in-batches -->

**Prerequisites.** The two loops and the captured size in this lesson.

**Problem.** Items are identified by integers `0` to `n - 1`. The array `start` lists the items that are in the queue at the beginning, in queue order. The array `children[i]` lists the items that processing item `i` appends to the queue, in append order. Process items in first-in first-out order. Group the processed items into levels. Level 0 is the starting queue contents. Level `d + 1` is the set of items appended while level `d` is processed. Return the levels in order, and list the ids of each level in the order they were processed.

**Constraints.** The limits are:
- **Items** count `0 <= n <= 10^5`, and `children.length == n`.
- **Ids** appear once in total across `start` and all `children` arrays, so no item is added twice.
- **Start** may be empty.
- **Return** is an `int[][]` with one row per level, and it is empty when `start` is empty.

**Example 1.** Input `start = [0,1]` and `children = [[2],[3,4],[],[5],[],[]]`, output `[[0,1],[2,3,4],[5]]`.

**Example 2.** Input `start = []` and `children = [[]]`, output `[]`.

**Hint.** Read the queue size once at the start of each level. How many items belong to that level?

**Changed decision.** The captured size replaces any stored depth.

#### [Vary] Count Levels To First Target (Author exercise)
<!-- id: sq-levels-to-target -->

**Prerequisites.** The exercise above.

**Problem.** Use the same item model, with `start`, `children` and first-in first-out processing. Given a target item `t`, return the number of complete levels processed before the level that contains `t`. Return 0 when `t` is in the starting queue. Return -1 when no processed item equals `t`.

**Constraints.** The limits are:
- **Items** count `1 <= n <= 10^5`, and `children.length == n`.
- **Ids** appear at most once in total across `start` and all `children` arrays.
- **Target** is an id with `0 <= t < n`, and it may be unreachable.
- **Return** is an `int`.

**Example 1.** Input `start = [0]`, `children = [[1,2],[3],[],[4],[]]` and `t = 4`, output 3.

**Example 2.** Input `start = [0]`, `children = [[1],[],[]]` and `t = 2`, output -1.

**Hint.** Where does the distance counter change, and where does it stay unchanged? Stop as soon as the target leaves the queue.

**Changed decision.** The distance increases once after each captured batch, not once per item.

#### [Boundary] Expanding Queue (Author exercise)
<!-- id: sq-expanding-queue -->

**Prerequisites.** The two exercises above.

**Problem.** Use the same item model. Return the number of items processed in each level, in level order. During a level, each processed item may append many children. The count of a level must include only the items that were in the queue when that level began.

**Constraints.** The limits are:
- **Items** count `0 <= n <= 10^5`, and `children.length == n`.
- **Fan-out** of one item may be up to `10^5`, so the queue can grow far beyond the starting level.
- **Ids** appear at most once in total across `start` and all `children` arrays.
- **Return** is an `int[]`, empty when `start` is empty.

**Example 1.** Input `start = [0]` and `children = [[1,2,3,4],[5],[],[6,7],[],[],[],[]]`, output `[1,4,3]`.

**Example 2.** Input `start = [0,1]` and `children = [[],[]]`, output `[2]`.

**Hint.** The live queue size changes during the inner loop. Which value must the loop bound use?

**Changed decision.** New appends increase `queue.size()`, and the level size ignores them.

#### [Recognize] Alternate Level Output (Author exercise)
<!-- id: sq-alternate-levels -->

**Prerequisites.** All three exercises above.

**Problem.** Use the same item model. Return the levels as in the first exercise, with one change in the report. Levels numbered 1, 3, 5 and so on are listed in reverse processing order. Levels numbered 0, 2, 4 and so on keep processing order. The queue must still process items in plain first-in first-out order, so reversing a level in the report must not change the order of later appends.

**Constraints.** The limits are:
- **Items** count `0 <= n <= 10^5`, and `children.length == n`.
- **Ids** appear at most once in total across `start` and all `children` arrays.
- **Order** of processing is first-in first-out for every level.
- **Return** is an `int[][]`, empty when `start` is empty.

**Example 1.** Input `start = [0]` and `children = [[1,2],[3,4],[5],[6,7],[8],[],[],[],[]]`, output `[[0],[2,1],[3,4,5],[8,7,6]]`.

**Example 2.** Input `start = [0,1]` and `children = [[2,3],[4],[],[5],[],[]]`, output `[[0,1],[4,3,2],[5]]`.

**Hint.** Build each level in processing order first. Reverse only the finished list before adding it to the result.

**Changed decision.** The reversal changes the report of a level and leaves the discovery order untouched.
