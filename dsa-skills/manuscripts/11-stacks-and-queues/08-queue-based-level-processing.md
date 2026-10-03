<!-- lesson-kind: standard -->
<!-- lesson-id: queue-based-level-processing -->
## Queue-Based Level Processing

<!-- stage: context -->
### How Many Hear The Story Each Round

A village newsletter editor starts a rumour by telling one person. In each following round, everybody who heard the story in the previous round tells it to the people on their own list, and nobody is told twice. The editor wants a report that says who hears the story in round one, who hears it in round two, and so on, because the village council sends a reply team to each round in turn and needs the names of each group separately.

Some people tell many others and some tell no one, so the groups differ in size and the story can die out after a few rounds. The report must keep the rounds apart even though the whole village shares one list of who tells whom, and it must be produced without asking anybody twice.

<!-- stage: naive -->
### Sweep Everyone Once Per Round

The direct method records the round in which each person hears the story. For round r, it sweeps through the whole village, picks out everyone recorded as having heard it in round r, and marks their listeners for round r plus one.

```java
static int[] roundSizesBySweeps(int[][] tellsTo) {
    int n = tellsTo.length;
    int[] round = new int[n];
    Arrays.fill(round, -1);
    round[0] = 0;
    int last = 0;
    for (int r = 0; ; r++) {
        boolean any = false;
        for (int i = 0; i < n; i++) {
            if (round[i] != r) continue;
            for (int j : tellsTo[i]) if (round[j] == -1) { round[j] = r + 1; any = true; }
        }
        if (!any) break;
        last = r + 1;
    }
    int[] sizes = new int[last + 1];
    for (int i = 0; i < n; i++) if (round[i] >= 0) sizes[round[i]]++;
    return sizes;
}
```

It is correct, because a person is marked in the first round in which any teller reaches them, and the final tally counts each round separately.

<!-- stage: bottleneck -->
### One Full Sweep For Every Round

Each round sweeps all n people to find the few who heard it in that round, so a story that lasts d rounds costs d full sweeps, which is O(n d). In a village where the story passes along a chain, d is nearly n, so the cost is O(n^2), and a village of a hundred thousand people needs ten billion looks to find a few thousand tellers. Most of the sweep checks people who are not tellers in that round at all.

The method has no list of who is waiting to speak next. A queue that receives each newly told person as they are told already holds exactly those people, in the order they will speak. Because the queue is filled round by round, the people in it at the start of a round are exactly that round's group, and only the few people who are really speaking are ever touched. The total work becomes O(n + e) for n people and e entries on all the lists.

<!-- stage: insight -->
### Count Before You Drain

Run the queue as before, but process it one batch at a time. At the start of a round the queue holds precisely the people of that round and nobody else, since the people added during the previous round have been waiting at its back. Read the queue's size once, before removing anyone, and keep it as the **captured size**. Then remove exactly that many people. Everyone who is added while those people speak lands behind them, so the queue at the end of the round holds exactly the next group, and the loop can capture the new size and repeat.

The invariant is that at the start of every round the queue contains exactly the items of that round, and the captured size is their count. Capturing the size before the loop is what makes this true. A loop that asks the queue for its size at every step is wrong: each person who speaks adds new people, which raises the size, so the loop swallows the next round, and soon the groups blur into each other.

The **batch boundary** is therefore not stored in the queue but in a number. It is tempting to mark the end of a round with a special item pushed into the queue, but `ArrayDeque` refuses `null`, so a **null marker** throws `NullPointerException` the moment it is added. A real marker object would work but costs an extra check on every removal, and the captured size does the same job with no extra element at all.

<!-- names: captured size, batch boundary, null marker -->

The same structure computes the distance of every item from the start, because the round number of an item is exactly the number of steps it took to reach it. Tree level order is the application of this idea to trees and is taught later with the tree chapters.

<!-- stage: variables -->
### Queue, Size And Round Number

The queue holds item numbers, the integer `size` is read once at the start of a round, and the loop variable `k` counts removals within that round. The list `level` collects the items of the current round in the order they were removed, and `levels` collects those lists. The integer `round` counts completed rounds, and it is incremented only after the inner loop finishes. A boolean array `told` marks items when they are added to the queue, so that nobody is queued twice when the input lists overlap.

<!-- stage: trace -->
### Rounds Of A Seven-Person Village

The village has seven people numbered 0 to 6. Person 0 tells 1 and 2, person 1 tells 3 and 4, person 2 tells 5, and person 4 tells 6. The cells hold the people, and `item` points at the person being processed. The first round holds only person 0. At the start of the second round the queue holds 1 and 2, so the captured size is 2, and the people added while they speak, 3, 4 and 5, wait behind them for the third round.

```trace
{"cells":[0,1,2,3,4,5,6],"pointers":["item"],"steps":[{"at":{"item":0},"vars":{"round":0,"size":1,"queue":"[1,2]"},"note":"Round 1 has captured size 1. Person 0 speaks and adds [1, 2], who wait behind the current group."},{"at":{"item":1},"vars":{"round":1,"size":2,"queue":"[2,3,4]"},"note":"Round 2 has captured size 2. Person 1 speaks and adds [3, 4], who wait behind the current group."},{"at":{"item":2},"vars":{"round":1,"size":2,"queue":"[3,4,5]"},"note":"Round 2 has captured size 2. Person 2 speaks and adds [5], who wait behind the current group."},{"at":{"item":3},"vars":{"round":2,"size":3,"queue":"[4,5]"},"note":"Round 3 has captured size 3. Person 3 speaks and adds nobody."},{"at":{"item":4},"vars":{"round":2,"size":3,"queue":"[5,6]"},"note":"Round 3 has captured size 3. Person 4 speaks and adds [6], who wait behind the current group."},{"at":{"item":5},"vars":{"round":2,"size":3,"queue":"[6]"},"note":"Round 3 has captured size 3. Person 5 speaks and adds nobody."},{"at":{"item":6},"vars":{"round":3,"size":1,"queue":"[]"},"note":"Round 4 has captured size 1. Person 6 speaks and adds nobody."}]}
```

The second trace runs a faulty loop that asks the queue for its size at every step. Watch how the first batch grows: person 0 adds two people, which raises the size, so the loop keeps going and removes 1 and 2 in the same batch. Then the counter catches up with the live size and the loop stops, after one batch that mixes the first two rounds together.

```trace
{"cells":[0,1,2,3,4,5,6],"pointers":["item"],"steps":[{"at":{"item":0},"vars":{"i":0,"liveSize":2,"batch":"[0]"},"note":"Step 0: person 0 is removed and adds [1, 2], so the live size is now 2 and the counter moves to 1."},{"at":{"item":1},"vars":{"i":1,"liveSize":3,"batch":"[0,1]"},"note":"Step 1: person 1 is removed and adds [3, 4], so the live size is now 3 and the counter moves to 2."},{"at":{"item":2},"vars":{"i":2,"liveSize":3,"batch":"[0,1,2]"},"note":"Step 2: person 2 is removed and adds [5], so the live size is now 3 and the counter moves to 3. The counter now equals the live size, so the loop stops with the first batch holding 0, 1 and 2."}]}
```

<!-- stage: code -->
### Batches, Distance And Zigzag

```java
static List<List<Integer>> levels(int[][] children) {
    List<List<Integer>> levels = new ArrayList<>();
    ArrayDeque<Integer> queue = new ArrayDeque<>();
    queue.addLast(0);
    while (!queue.isEmpty()) {
        int size = queue.size();
        List<Integer> level = new ArrayList<>();
        for (int k = 0; k < size; k++) {
            int item = queue.removeFirst();
            level.add(item);
            for (int child : children[item]) queue.addLast(child);
        }
        levels.add(level);
    }
    return levels;
}

static int levelsToTarget(int[][] children, int target) {
    ArrayDeque<Integer> queue = new ArrayDeque<>();
    queue.addLast(0);
    int round = 0;
    while (!queue.isEmpty()) {
        int size = queue.size();
        for (int k = 0; k < size; k++) {
            int item = queue.removeFirst();
            if (item == target) return round;
            for (int child : children[item]) queue.addLast(child);
        }
        round++;
    }
    return -1;
}
```

Every item enters and leaves the queue once, so both methods run in O(n + e) time and use O(width) extra space for the queue, where the width is the size of the largest round.

<!-- stage: applicability -->
### When The Answer Comes In Rounds

Use a batch loop when work must be grouped by its distance from the start, or by arrival batch, and every item in the queue at the start of a round belongs to that round. The invariant is that the captured size equals the number of items of the current round and the queue behind them holds the next round.

A false friend is the plain drain loop `while (!queue.isEmpty())`, which gives the right visiting order and no rounds. A second false friend is a loop bounded by the live `queue.size()`, which changes as the loop adds items. A third is a sentinel inserted into the queue, which is impossible with `null` and wasteful with any other object.

In Java, assign `int size = queue.size()` once per round, outside the inner loop, and never reuse it after the loop adds items. Do not add `null` to an `ArrayDeque`. Increase the round counter after the inner loop, so that the answer for an item found during the loop is the number of completed rounds before it.

<!-- stage: exercises -->
### Exercises

#### [Build] Process Queue In Batches (Author exercise)
<!-- id: sq-process-in-batches -->

**Prerequisites.** The Min Stack lesson.

**Problem.** Items are numbered 0 to n - 1, and `children[i]` lists the items that processing item `i` appends to the queue. Start with item 0 alone. Return the items processed in each batch, with each batch holding exactly the items that were waiting when it began.

**Constraints.** 1 <= n <= 100000, every item other than 0 appears in at most one list, and no list contains item 0.

**Example 1.** Input `children = [[1, 2], [3], [], []]`, output `[[0], [1, 2], [3]]`.

**Example 2.** Input `children = [[]]`, output `[[0]]`.

**Hint.** When must the size of the queue be read? What does the queue contain right after a batch ends?

**Changed decision.** First rung: the queue is drained in batches, so the size is captured before each batch begins.

#### [Vary] Count Levels To First Target (Author exercise)
<!-- id: sq-levels-to-target -->

**Prerequisites.** The Process Queue In Batches rung.

**Problem.** With the same lists, return the number of batches that finish before the batch containing `target` begins, which is the distance of `target` from item 0. Return -1 if the target never appears. Item 0 is at distance zero.

**Constraints.** 1 <= n <= 100000, 0 <= target < n, every item other than 0 appears in at most one list, and some items may not be reachable from item 0.

**Example 1.** Input `children = [[1, 2], [3], [], []], target = 3`, output `2`.

**Example 2.** Input `children = [[1], [], []], target = 2`, output `-1`.

**Hint.** When should the counter of batches be incremented? What does the counter mean when the target is found in the middle of a batch?

**Changed decision.** The round counter is incremented after each captured batch is fully processed, so it counts completed batches.

#### [Boundary] Expanding Queue (Author exercise)
<!-- id: sq-expanding-queue -->

**Prerequisites.** The Count Levels To First Target rung.

**Problem.** Items are numbered 0 to n - 1, and processing item `x` appends the items `2x + 1` and `2x + 2` when they are smaller than n. Starting from item 0, return the size of every batch in order. The queue grows during each batch, but the new items must not be part of the current batch.

**Constraints.** 0 <= n <= 1000000, and the answer is empty when n is zero.

**Example 1.** Input `n = 7`, output `[1, 2, 4]`.

**Example 2.** Input `n = 10`, output `[1, 2, 4, 3]`.

**Hint.** Which value of `queue.size()` is correct to use as the loop bound, and when is it read?

**Changed decision.** The batch size is a captured number and not the live queue size, which grows while the batch runs.

#### [Recognize] Alternate Level Output (Author exercise)
<!-- id: sq-alternate-level-output -->

**Prerequisites.** The Expanding Queue rung.

**Problem.** With lists `children` as before, return the batches in order, but reverse the reported order of every batch whose index is odd, counting the first batch as index 0. Items must still be dequeued in the usual first-in-first-out order, so the reversal only affects what is reported.

**Constraints.** 1 <= n <= 100000, every item other than 0 appears in at most one list, and no list contains item 0.

**Example 1.** Input `children = [[1, 2], [3, 4], [5], [], [], []]`, output `[[0], [2, 1], [3, 4, 5]]`.

**Example 2.** Input `children = [[]]`, output `[[0]]`.

**Hint.** Should the queue discovery order change, or only the order in which a finished batch is reported?

**Changed decision.** The queue keeps its first-in-first-out discovery, and the reporting order of alternate batches is reversed after each batch is complete.
