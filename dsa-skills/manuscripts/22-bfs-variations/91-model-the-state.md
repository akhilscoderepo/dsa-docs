<!-- lesson-kind: combination -->
<!-- lesson-id: model-state-before-search -->
## Model The State Before Searching

<!-- stage: context -->
### Why One Search Per Source Runs Long

A warehouse routing service stores a floor plan as a table of cells. For every cell, it must report the distance to the nearest exit. The first version starts one search from each exit and keeps the smallest value for each cell. That version passes review on a plan with two exits. On a plan with five hundred exits, the service needs minutes.

Three more requests arrive in the same week. The first adds shelving cells that no cart can enter to the exit request. The second asks how many minutes pass until spoilage, which spreads one neighbor per minute, has rotted every crate it can reach. The third asks for the shortest chain of product codes where each code differs from the next in one character, and no table exists for that request. Each request looks like a new algorithm.

This lesson asks a different question. Before any loop is written, which things must the program decide so that one breadth-first search answers all three requests?

<!-- stage: contributions -->
### What Each Earlier Lesson Adds

Five earlier lessons in this chapter supply the pieces. Start From Many Sources contributes the seeding step: every source enters the queue at distance 0 before the first removal. Count By Whole Layers contributes the rule that a layer is the group of vertices at one distance, and that the program reads `queue.size()` before it processes a layer. Search From Both Ends contributes the habit of searching from the end that has the smaller frontier, or from the target when the target is the only fixed point. The Smallest Shortest Path exercise uses that second habit.

Search States You Generate contributes the complete encoding of a state and the generation of neighbors from rules instead of from a stored table. Keep The Best Resource Left contributes the test for when one state dominates another, which decides what the encoding must include. No exercise below spends a resource, so this contribution applies when a new contract adds one.

The combination adds one order of work. The program decides four things first and writes the loop second. The invariant is that every state key enters the queue once, marked before it enters, and the key holds everything that later moves depend on. The nearest false friend is the single-source grid search of the previous chapter. It passes every sample that has one source, no walls and no generated states.

<!-- stage: naive -->
### Searching Once From Every Source

The direct plan runs a complete search from each source cell and keeps the smallest distance seen for each cell. Each search owns a new distance array, so the searches never interfere with each other.

```java
static int[][] nearestZeroSlow(int[][] grid) {
    int rows = grid.length, cols = grid[0].length;
    int[][] best = new int[rows][cols];
    for (int[] row : best) Arrays.fill(row, Integer.MAX_VALUE);
    for (int s = 0; s < rows * cols; s++) {
        if (grid[s / cols][s % cols] != 0) continue;       // only a zero cell is a source
        int[] dist = new int[rows * cols];                 // a fresh array for every source
        Arrays.fill(dist, -1);
        ArrayDeque<Integer> queue = new ArrayDeque<>();
        dist[s] = 0;
        queue.add(s);
        while (!queue.isEmpty()) {
            int cur = queue.poll();
            int r = cur / cols, c = cur % cols;
            best[r][c] = Math.min(best[r][c], dist[cur]);  // keep the smaller of the two values
            int[][] around = {{r + 1, c}, {r - 1, c}, {r, c + 1}, {r, c - 1}};
            for (int[] a : around) {
                if (a[0] < 0 || a[0] >= rows || a[1] < 0 || a[1] >= cols) continue;
                int nid = a[0] * cols + a[1];
                if (dist[nid] == -1) { dist[nid] = dist[cur] + 1; queue.add(nid); }
            }
        }
    }
    return best;
}
```

```predict
A table has 3 rows and 4 columns. Three cells hold 0 and the other nine hold 1. The method returns the right distances. How many cells does it take off a queue in total?

It takes 36 cells off a queue. Each of the 3 sources runs a search that reaches all 12 cells. One shared search would take each cell off once, which is 12 removals.
```

<!-- stage: bottleneck -->
### Counting Repeated Searches

The method returns correct distances, but it repeats work. Each source runs a search that costs O(rows * cols), so a table with `S` sources costs O(S * rows * cols). When half of the cells are sources, `S` grows with the table and the cost becomes O((rows * cols)^2). A table of 1,000 by 1,000 cells then needs about 5 * 10^11 removals.

The loop also fixes the meaning of every part of the search in advance. The vertex is a cell, the neighbors are four table steps, and the answer is one distance per cell. A request for walls changes the neighbor test. A request for a chain of product codes has no table at all, so the loop has nothing to adapt. Each change forces a rewrite, because the code never separated the decisions from the loop.

The service needs one search that begins with every source together, and a way to state what a vertex, a neighbor and a distance mean for each request.

<!-- stage: insight -->
### Four Choices Before The Loop

#### Choosing The Start Set

The **start set** holds every vertex at which the answer is known before the search begins. The program marks each of them and adds them to the queue before the first removal. All of them sit in the first layer, which is the group of vertices at distance 0. The search then behaves like a single search from one imaginary vertex that touches every source. One pass replaces the search per source, and the cost drops from O(S * V) to O(V + E).

<!-- names: start set, state key, move rule, layer meaning -->

#### Choosing The State Key

The **state key** is the value that identifies one vertex, and the `visited` record stores it. A cell id `r * cols + c` is enough for a table with fixed rules. A word needs only its text. The key must contain everything that changes which moves are legal or what the answer means later. A key that leaves out such a fact merges two different situations and returns a wrong answer. A key that adds an unrelated fact splits one situation into many and wastes time and memory.

#### Choosing The Move Rule

The **move rule** lists the keys reachable from one key in one step. For a table, it applies the direction table, the bounds check and the eligibility test of the problem. For words, it replaces each letter in turn by every other letter and keeps the candidates that a hash set of the dictionary holds. The loop calls the rule and never learns how the keys are stored or produced.

#### Choosing The Layer Meaning

The **layer meaning** says what one layer costs in the units of the question. For nearest distance, one layer is one step. For rotting, one layer is one minute. The program reads `queue.size()` before it processes a layer, and it advances the counter once per layer. A counter that advances once per removed vertex counts vertices and not layers.

A changed contract touches exactly one choice. Walls change the move rule. A different report, such as the last cell or the whole sequence, changes only what the loop records, and the four choices stay as they were. An extra fact in the state changes the key. A different set of sources changes the start set.

<!-- stage: variables -->
### What One Search Keeps

One search keeps the following values. The traces show `key`, `layer`, `queue` and `parent`, and these mean the same as the code names below. In the first trace the pointer `key` marks the cell that left the queue.

- **startSet** holds the keys that enter the queue at distance 0.
- **key** is the state key of one vertex, such as a cell id or a word id.
- **dist** maps each key to its layer number, and -1 means the search has not reached it.
- **queue** is an `ArrayDeque` of keys waiting for expansion.
- **layerSize** is `queue.size()` read at the start of one layer.
- **layer** is the layer number of the keys that the current pass expands.
- **parent** maps a key to the key that discovered it, and -1 means no discoverer.

<!-- stage: trace -->
### Walking Two Different Inputs

#### Rotting From Two Sources

The first trace runs the rotting rule on a table with three rows and four columns, flattened into twelve cells. The value 2 marks a rotten cell, 1 a fresh cell and 0 an empty cell. The pointer `key` marks the cell that left the queue. The variable `layer` shows the layer number of that cell. A cell with layer `k` rots its fresh neighbors in minute `k + 1`.

Cells 0 and 11 form the start set, and both enter the queue at once as layer 0. They rot cells 1, 4, 7 and 10 in minute 1, and those four cells form layer 1. Cell 1 rots cell 2, cell 7 rots cell 6 and cell 10 rots cell 9. These cells rot in minute 2 and form layer 2. Cell 4 finds no fresh neighbor, because the cells next to it are empty or already rotten. The three cells of layer 2 find no fresh neighbor either, so the search ends without a third minute. The answer is the largest layer number, 2. The last cell to rot is cell 2, at row 0, column 2.

```trace
{"cells":[2,1,1,0,1,0,1,1,0,1,1,2],"pointers":["key"],"steps":[{"at":{"key":-1},"vars":{"layer":"0","queue":"[0, 11]"},"note":"Both rotten cells, [0, 11], enter the queue before any removal. They form layer 0."},{"at":{"key":0},"vars":{"layer":"0","queue":"[11, 4, 1]"},"note":"Cell 0 rots [4, 1]."},{"at":{"key":11},"vars":{"layer":"0","queue":"[4, 1, 7, 10]"},"note":"Cell 11 rots [7, 10]."},{"at":{"key":-1},"vars":{"layer":"0","queue":"[4, 1, 7, 10]"},"note":"Layer 0 is fully expanded. The cells it rotted form layer 1 in minute 1, and the smallest is 1."},{"at":{"key":4},"vars":{"layer":"1","queue":"[1, 7, 10]"},"note":"Cell 4 finds no fresh neighbor."},{"at":{"key":1},"vars":{"layer":"1","queue":"[7, 10, 2]"},"note":"Cell 1 rots [2]."},{"at":{"key":7},"vars":{"layer":"1","queue":"[10, 2, 6]"},"note":"Cell 7 rots [6]."},{"at":{"key":10},"vars":{"layer":"1","queue":"[2, 6, 9]"},"note":"Cell 10 rots [9]."},{"at":{"key":-1},"vars":{"layer":"1","queue":"[2, 6, 9]"},"note":"Layer 1 is fully expanded. The cells it rotted form layer 2 in minute 2, and the smallest is 2."},{"at":{"key":2},"vars":{"layer":"2","queue":"[6, 9]"},"note":"Cell 2 finds no fresh neighbor."},{"at":{"key":6},"vars":{"layer":"2","queue":"[9]"},"note":"Cell 6 finds no fresh neighbor."},{"at":{"key":9},"vars":{"layer":"2","queue":"[]"},"note":"Cell 9 finds no fresh neighbor."},{"at":{"key":-1},"vars":{"layer":"2","queue":"[]"},"note":"The queue is empty. The largest layer number is 2, so the answer is 2 minutes, and the last cell is row 0, column 2."}]}
```

#### Building A Word Sequence

The second trace searches for a shortest sequence from lead to gold. The list of seven words has these ids, from 0 to 6, and the cells of the trace are these ids. The id 0 is lead, 1 is load, 2 is goad, 3 is gold, 4 is lend, 5 is mend and 6 is loan. The pointer `key` marks the word that left the queue. No table exists, so the move rule generates each next word by replacing one letter and looking the result up. The variable `parent` records which word discovered each reached word.

The word lead generates load and lend. Load then generates goad and loan, and lend generates mend. Loan and mend open no new route, but the search still marks them, because it cannot know that in advance. Goad generates gold, and the search stops. Following the parents from gold gives a sequence of four words.

```trace
{"cells":[0,1,2,3,4,5,6],"pointers":["key"],"steps":[{"at":{"key":-1},"vars":{"queue":"[lead]","parent":"{}"},"note":"The begin word lead has id 0. It is marked as reached and enters the queue."},{"at":{"key":0},"vars":{"queue":"[load, lend]","parent":"{load:lead, lend:lead}"},"note":"lead leaves the queue and generates [load, lend], each with parent lead."},{"at":{"key":1},"vars":{"queue":"[lend, goad, loan]","parent":"{load:lead, lend:lead, goad:load, loan:load}"},"note":"load leaves the queue and generates [goad, loan], each with parent load."},{"at":{"key":4},"vars":{"queue":"[goad, loan, mend]","parent":"{load:lead, lend:lead, goad:load, loan:load, mend:lend}"},"note":"lend leaves the queue and generates [mend], each with parent lend."},{"at":{"key":2},"vars":{"queue":"[loan, mend, gold]","parent":"{load:lead, lend:lead, goad:load, loan:load, mend:lend, gold:goad}"},"note":"goad leaves the queue and generates [gold], each with parent goad. The end word is reached, so the search stops."},{"at":{"key":3},"vars":{"queue":"[loan, mend, gold]","parent":"followed"},"note":"Following the parents from gold back to lead and reversing gives lead, load, goad, gold."}]}
```

<!-- stage: code -->
### One Search For Cells And Words

#### Writing The Search Once

The method `layers` takes the number of keys, the start set, a move rule and a `parent` array. The move rule is an `IntFunction<int[]>` that maps a key to the keys one step away. The method fills `parent` and returns `dist`, where -1 marks a key that the search never reached. The same array serves as the `visited` record, so no second structure exists. The final pass expands the last layer and finds nothing, so `layer` ends one higher than the largest distance. Callers read the largest value in `dist`. The imports and the wrapper class make the block compile on its own.

```java
import java.util.ArrayDeque;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;
import java.util.function.IntFunction;
import java.util.function.IntPredicate;

final class StateWalk {
    static int[] layers(int keyCount, int[] startSet, IntFunction<int[]> moves, int[] parent) {
        int[] dist = new int[keyCount];
        Arrays.fill(dist, -1);                               // -1 means not reached yet
        Arrays.fill(parent, -1);                             // -1 means no discoverer yet
        ArrayDeque<Integer> queue = new ArrayDeque<>();
        for (int s : startSet) {
            if (dist[s] == -1) { dist[s] = 0; queue.add(s); } // every source enters before any removal
        }
        int layer = 0;                                       // layer number of the keys in this pass
        while (!queue.isEmpty()) {
            int layerSize = queue.size();                    // the size of this layer, fixed now
            for (int i = 0; i < layerSize; i++) {
                int key = queue.poll();
                for (int nb : moves.apply(key)) {            // the move rule lists each neighbor key
                    if (dist[nb] == -1) { dist[nb] = layer + 1; parent[nb] = key; queue.add(nb); }
                }
            }
            layer++;                                         // one increment per layer
        }
        return dist;
    }
}
```

#### Plugging In Two Move Rules

The two methods below belong in the same class. The first reads a table and the second generates words from the lowercase letters. Both return an `IntFunction<int[]>` that maps a key to the keys one step away, so `layers` runs unchanged.

```java
static IntFunction<int[]> gridMoves(int[][] grid, int[][] dirs, IntPredicate open) {
    int rows = grid.length, cols = grid[0].length;
    return key -> {
        int[] found = new int[dirs.length];
        int n = 0;
        for (int[] d : dirs) {                               // each allowed step of the table
            int nr = key / cols + d[0], nc = key % cols + d[1];
            if (nr < 0 || nr >= rows || nc < 0 || nc >= cols) continue;
            if (open.test(grid[nr][nc])) found[n++] = nr * cols + nc;
        }
        return Arrays.copyOf(found, n);
    };
}

static IntFunction<int[]> wordMoves(String[] words) {
    Map<String, Integer> idOf = new HashMap<>();
    for (int i = 0; i < words.length; i++) idOf.put(words[i], i);
    return key -> {
        char[] chars = words[key].toCharArray();
        int[] found = new int[chars.length * 25];
        int n = 0;
        for (int p = 0; p < chars.length; p++) {              // generate by changing one position
            char keep = chars[p];
            for (char c = 'a'; c <= 'z'; c++) {
                if (c == keep) continue;
                chars[p] = c;
                Integer id = idOf.get(new String(chars));    // a hash lookup decides membership
                if (id != null) found[n++] = id;
            }
            chars[p] = keep;                                 // restore the letter before the next position
        }
        return Arrays.copyOf(found, n);
    };
}
```

#### Calling It For Three Requests

For nearest distance with walls, pass every zero cell as the start set and `gridMoves` with `v -> v == 1`, and use `dist` as the answer table. For rotting, pass every cell holding 2 with the same test and read the largest value in `dist`. A fresh cell that keeps -1 never rots. For the chain of codes, pass the id of the begin word and `wordMoves`, then follow `parent` from the end word id until -1 and reverse the result. The three calls differ only in the start set, the move rule and what the caller reads afterward.

- **Time** is O(V + E) for the search plus the cost of the move rule calls, where `E` counts the pairs that the rule reports. A table rule costs O(1) per key. The word rule tries 25 letters at each of `L` positions and hashes a word of length `L`, so it costs O(L^2) per key and the whole word search costs O(V * L^2).
- **Space** is O(V), because `dist`, `parent` and the queue hold at most one entry per key, and the word rule adds a map of V words.

<!-- stage: applicability -->
### Telling Which Choice A Contract Changes

#### Mapping A Changed Contract To One Choice

Read a changed contract and ask which of the four choices it touches. More than one source changes the start set. A new obstacle or a new kind of step changes the move rule. An extra fact that the answer depends on, such as a remaining resource, changes the state key. A different unit of cost, such as minutes in place of steps, changes the layer meaning. A different report, such as the last cell or the whole sequence, changes none of the four. The exercises below change the report in two cases, the move rule in one and the start set in one, and the other choices stay as they were.

#### Keeping The Invariant

The invariant of the whole lesson is that every state key enters the queue once and is marked before it enters. It also says that the queue holds the keys of one layer followed by the keys of the next. A rule that marks a key only when it leaves the queue lets the same key enter several times. A counter that increases per removed key breaks the second part.

#### Avoiding The Familiar Single-Source Search

The single-source grid search is the false friend of this lesson. It passes every sample that has one source and no walls. It fails when a contract adds sources, walls, or states that no table stores. In Java, a `-1` that serves as both the unreached marker and a legal answer is a second hazard, so a contract that allows -1 as a result needs its own check for unreached keys.

<!-- stage: exercises -->
### Exercises

#### [Build] Rot Everything And Name The Last Cell (LeetCode 994)
<!-- id: bv9-rot-last-cell -->

**Prerequisites.** The Start From Many Sources and Count By Whole Layers lessons.

**Problem.** This changes the Rotting Oranges contract: the method returns the last cell to rot together with the minute count. A table holds 0 for an empty cell, 1 for a fresh orange and 2 for a rotten orange. In each minute, every fresh orange that shares a side with a rotten orange becomes rotten. The last cell is the cell with the smallest row, then the smallest column, among the oranges that rot in the last minute in which at least one orange rots. Return `{minutes, row, col}`. Return `{-1, -1, -1}` when some fresh orange never rots. Return `{0, -1, -1}` when the table holds no fresh orange.

**Constraints.** The limits are:
- **Size** is `1 <= rows, cols <= 10`, and every row has the same length.
- **Cells** are the `int` values 0, 1 and 2 only.
- **Neighbors** use the four side directions only.
- **Ties** go to the smaller row, then the smaller column.
- **Mutation** does not occur; the method leaves `grid` unchanged.

**Example 1.** Input `grid = [[2,1,1],[1,1,0],[0,1,1]]`, output `{4, 2, 2}`.

**Example 2.** Input `grid = [[2,1,0,1],[1,1,0,1],[0,1,1,2]]`, output `{2, 0, 3}`, because two sources start together and three cells rot in minute 2, so the row-major first one is the answer.

**Hint.** When does the minute counter advance, and what happens to the counter when a layer rots nothing?

**Changed decision.** The method reports a cell of the last layer and not only the number of layers.

#### [Vary] Distance To The Nearest Zero Around Walls (LeetCode 542)
<!-- id: bv9-nearest-zero-walls -->

**Prerequisites.** The Start From Many Sources lesson and the first exercise above.

**Problem.** This changes the 01 Matrix contract: cells marked 2 are walls. A table holds 0, 1 or 2. A route moves between side neighbors and never enters a wall. The distance of a cell is the number of steps of a shortest route from that cell to a cell holding 0. Return a table of the same size. Each cell holds its distance, or -1 when the cell is a wall or when no route reaches a zero.

**Constraints.** The limits are:
- **Size** is `1 <= rows, cols <= 50`, and every row has the same length.
- **Cells** are the `int` values 0, 1 and 2 only.
- **Neighbors** use the four side directions only.
- **Result** is a new table; the method leaves `grid` unchanged.
- **Sources** may be absent, and then every cell holds -1.

**Example 1.** Input `grid = [[1,1,1],[1,2,1],[1,1,0]]`, output `[[4,3,2],[3,-1,1],[2,1,0]]`.

**Example 2.** Input `grid = [[1,2,0],[2,1,2],[1,1,2]]`, output `[[-1,-1,0],[-1,-1,-1],[-1,-1,-1]]`, because walls cut off the only zero.

**Hint.** Which one of the four choices does a wall touch? Can the result table also mark unreached cells?

**Changed decision.** The move rule rejects walls, and a cell that no route reaches keeps -1.

#### [Boundary] One Shortest Word Sequence (LeetCode 127)
<!-- id: bv9-word-sequence -->

**Prerequisites.** The Search States You Generate lesson and the two exercises above.

**Problem.** This changes the Word Ladder contract: the method returns one shortest sequence and not its length. Given a begin word, an end word and a list of words of equal length, a sequence starts with the begin word and ends with the end word. Each next word appears in the list, and each word differs from the one before it in exactly one position. Return one sequence with the fewest words as a list. Any shortest sequence is accepted. Return an empty list when the end word is not in the list or when no sequence exists.

**Constraints.** The limits are:
- **Words** have the same length from 1 to 10 and use the lowercase letters `a` to `z`.
- **List** holds `1 <= n <= 5000` words, and duplicates may occur.
- **Begin** differs from the end word and need not appear in the list.
- **Result** includes the begin word and the end word.
- **Mutation** does not occur; the method leaves the list unchanged.

**Example 1.** Input `begin = "cold"`, `end = "warm"`, `words = [cord, card, ward, warm, wore]`, output `[cold, cord, card, ward, warm]`.

**Example 2.** Input `begin = "hat"`, `end = "cog"`, `words = [hot, dot, cog]`, output `[]`, because the end word is in the list but no chain of one-letter changes reaches it.

**Hint.** What is one vertex here, and how does the program find its neighbors without a stored table? What must the search store to rebuild a sequence?

**Changed decision.** The search stores the discovering word for each reached word, and the answer comes from following those parents.
#### [Recognize] Smallest Shortest Path In A Binary Matrix (LeetCode 1091)
<!-- id: bv9-smallest-shortest-path -->

**Prerequisites.** The Search From Both Ends lesson and the three exercises above.

**Problem.** This changes the Shortest Path in Binary Matrix contract: the method returns the cells of one specific shortest path. A table holds 0 for an open cell and 1 for a blocked cell. A path starts at the top left cell, ends at the bottom right cell, and moves between open cells through the eight steps `(-1,-1)`, `(-1,0)`, `(-1,1)`, `(0,-1)`, `(0,1)`, `(1,-1)`, `(1,0)`, `(1,1)` in this fixed order. Among all shortest paths, return the one whose sequence of steps is smallest when two paths are compared at the first position where their steps differ, using the fixed order. Return the cells as `{row, col}` pairs, or an empty array when no path exists.

**Constraints.** The limits are:
- **Size** is `1 <= rows, cols <= 100`, and every row has the same length.
- **Cells** are the `int` values 0 and 1 only.
- **Endpoints** may be blocked, and then the result is empty.
- **Single cell** is an open table of one cell, and then the result holds that one cell.
- **Mutation** does not occur; the method leaves `grid` unchanged.

**Example 1.** Input `grid = [[0,0,1,0],[1,1,0,0],[0,0,1,1],[1,0,0,0]]`, output `[[0,0],[0,1],[1,2],[2,1],[3,2],[3,3]]`.

**Example 2.** Input `grid = [[0,0,0],[0,1,0],[0,0,0]]`, output `[[0,0],[0,1],[1,2],[2,2]]`, because several shortest paths tie and the fixed order prefers the step to the right over the steps down.

**Hint.** A forward search finds the length but does not tell which first step is smallest. From which cell should the distances be measured?

**Changed decision.** The search runs from the target, and a forward walk then chooses the earliest step that lowers the remaining distance.
