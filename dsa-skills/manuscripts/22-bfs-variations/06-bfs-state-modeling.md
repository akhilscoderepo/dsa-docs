<!-- lesson-kind: combination -->
<!-- lesson-id: bfs-state-modeling -->
## BFS State Modeling

<!-- stage: context -->
### The Marlow Glasshouse

The Marlow Glasshouse is a long hall of potting benches laid out in rows, with glass partitions here and there that no mist can pass. When the humidity gets too low, the head gardener opens the valves on some of the benches, and the mist creeps from every open valve to the benches beside it, taking exactly one minute per step. Her notebook asks for three things after each opening: the minute at which the last reachable bench is misted, how many dry benches the mist never reached, and for every bench how many steps away the nearest valve is.

The glasshouse also has a seed room. Every cutting there carries a four-letter tag, and the registry allows a cutting to be re-tagged by changing one letter, but only to a tag that is already registered. A grafter wants to know in how many different ways one tag can be turned into another with the fewest re-taggings. The head gardener has worked out these numbers by hand for years, bench by bench, and each new season the hall grows.

<!-- stage: contributions -->
### What Each Idea Brings

Graph BFS brings time. The queue processes every place at distance d before any place at distance d + 1, so the first time a place is reached is the shortest time to it, and a whole layer of places can be treated as one minute, one step or one re-tagging.

State modeling brings identity. It decides which facts make two situations the same place, so that the search neither confuses two different situations nor counts one situation twice, and it decides what the visited record has to keep: a plain mark, a distance, or the list of ways in.

Neither is enough alone. A queue with a careless idea of a place revisits cells or walks off the edge of the hall, and a careful model with no layered queue has no way to say which ways in are shortest. The cue for the combination is a shortest-step question where the answer asks for more than one number, or where the moves wrap, are blocked, or leave the grid.

<!-- stage: naive -->
### One Fresh Search For Every Bench

The direct method treats every bench as its own question. For each bench in the hall it starts a separate search that spreads outward one ring at a time, with the hall closing round on itself at the ends of the rows, and stops when the ring first touches an open valve. The answer for that bench is the number of rings.

```java
static int[][] stepsToValve(int[][] hall) {
    int h = hall.length, w = hall[0].length;
    int[][] answer = new int[h][w];
    int[] dr = {1, -1, 0, 0}, dc = {0, 0, 1, -1};
    for (int r = 0; r < h; r++) {
        for (int c = 0; c < w; c++) {
            boolean[][] seen = new boolean[h][w];
            java.util.ArrayDeque<int[]> ring = new java.util.ArrayDeque<>();
            ring.add(new int[]{r, c});
            seen[r][c] = true;
            int steps = 0, found = -1;
            while (found < 0 && !ring.isEmpty()) {
                for (int k = ring.size(); k > 0; k--) {
                    int[] cur = ring.poll();
                    if (hall[cur[0]][cur[1]] == 0) { found = steps; break; }
                    for (int d = 0; d < 4; d++) {
                        int a = (cur[0] + dr[d] + h) % h, b = (cur[1] + dc[d] + w) % w;
                        if (!seen[a][b]) { seen[a][b] = true; ring.add(new int[]{a, b}); }
                    }
                }
                steps++;
            }
            answer[r][c] = found;
        }
    }
    return answer;
}
```

It is correct for any hall, with -1 for a bench that no valve can reach. For the tags, the matching direct method writes down every partial chain of re-taggings and extends each chain by every legal re-tagging, then counts the chains that end at the target tag in the fewest steps.

<!-- stage: bottleneck -->
### The Same Floor Is Searched Again

A hall of h rows and w columns has n = h * w benches, and the one-search-per-bench method costs O(n^2), since each of the n searches may sweep nearly the whole floor. For a hall of ten thousand benches that is a hundred million bench visits, and nearly all of them repeat what a neighbouring bench's search has already learned: the bench next door is one step further from the same valve.

The chain method for tags is worse. When a tag has k legal re-taggings at every step and the shortest route has s steps, the number of chains is O(k^s), and two chains that arrive at the same tag after the same number of steps are extended separately, although everything that happens after that point is identical. What is wanted is one sweep for all benches, O(n) in total, and one record per tag that remembers how many shortest ways lead to it, so that the work grows with the number of tags and not with the number of chains.

<!-- stage: insight -->
### One Vertex Is One Complete Fact Set

The modeling decision comes first: a vertex is the **fact set**, the smallest collection of facts that decides what can happen next. For a bench the fact set is its position, once the row and column have been brought into range. Whether the bench is a wall, a valve or a dry patch never changes during the search, so it is looked up in the input and is not part of the vertex. For a tag the fact set is the tag alone and not the chain that led to it, which is what lets two chains that meet at one tag be merged. If a move rule depended on something that does change, such as a key carried along, that fact would join the vertex, and the same position with and without it would be two different vertices.

The second decision is the **seed layer**. Every valve, or every rotting orange, goes into the queue before any step is taken, all at distance zero, so the queue behaves as if one extra source were joined to all of them. A single sweep then yields the distance to the nearest of them for every vertex, with no per-source search.

The third decision is the **layer clock**. Process the queue one layer at a time, and the layer number is the elapsed time. The minute at which spreading ends is the number of the last layer that reached anything new, and a vertex's layer is its shortest distance. For counting, the visited record keeps more than a mark. A vertex seen from two parents in the same layer has still one distance but two ways in, so marks are made final only when the layer ends, and the record keeps a count of ways or a distance table that a second sweep from the other end can be matched against.

The invariant is that every vertex in the queue carries its final distance, and its layer is complete before the next one begins.

<!-- names: fact set, seed layer, layer clock -->

<!-- stage: variables -->
### Queue, Distance And Ways

Each problem uses the same four pieces. The vertex is an index such as `r * w + c` for a bench, or a string for a tag, always in its normalized form. The queue holds vertices of the current layer, and `dist` is the table of final distances, with -1 for unreached. The counter `layer` is the clock and is raised only when a layer produced at least one new vertex. For counting ladders, `ways` maps each vertex to the number of shortest routes that reach it, and `fresh` is the map of vertices found in the layer being built, folded into `dist` and `ways` only after the layer is complete. For the walled spread, `left` is the count of fresh oranges not yet reached, reduced on each discovery.

<!-- stage: trace -->
### Misting And Counting Ladders

The first trace follows the spread through a small hall. The cells are in row order for a three by three hall, where `R` is an orange already rotten, `F` a fresh one, `.` an empty bench and `#` a wall. The pointer `cell` marks the vertex taken from the queue. The wall in the middle is never entered, and the bench in the lower left corner is empty, so it never joins the queue. The count `left` falls on each discovery, reaching zero at minute 5, which is the last layer.

```trace
{"cells":["R","F","F","F","#","F",".","F","F"],"pointers":["cell"],"steps":[{"at":{"cell":0},"vars":{"minute":0,"left":4},"note":"Cell 0 was rotten at minute 0. It rots cell(s) 3, 1 at minute 1, so left is now 4."},{"at":{"cell":3},"vars":{"minute":1,"left":4},"note":"Cell 3 was rotten at minute 1, and every side neighbour is a wall, an empty bench, outside the hall or already rotten, so nothing new is found."},{"at":{"cell":1},"vars":{"minute":1,"left":3},"note":"Cell 1 was rotten at minute 1. It rots cell(s) 2 at minute 2, so left is now 3."},{"at":{"cell":2},"vars":{"minute":2,"left":2},"note":"Cell 2 was rotten at minute 2. It rots cell(s) 5 at minute 3, so left is now 2."},{"at":{"cell":5},"vars":{"minute":3,"left":1},"note":"Cell 5 was rotten at minute 3. It rots cell(s) 8 at minute 4, so left is now 1."},{"at":{"cell":8},"vars":{"minute":4,"left":0},"note":"Cell 8 was rotten at minute 4. It rots cell(s) 7 at minute 5, so left is now 0."},{"at":{"cell":7},"vars":{"minute":5,"left":0},"note":"Cell 7 was rotten at minute 5, and every side neighbour is a wall, an empty bench, outside the hall or already rotten, so nothing new is found."}]}
```

The second trace counts shortest ladders from `rat` to `pen` through a registry of eight tags. The cells are the tags, and the pointer `w` marks the tag being expanded. Each expansion adds its own count of ways to every tag found one layer later. The tag `pet` is reached from `pat` and from `ret`, so it holds two ways, and the final tag `pen` collects ways from both `pet` and `ren`.

```trace
{"cells":["rat","pat","pet","pot","rot","ret","ren","pen","ten"],"pointers":["w"],"steps":[{"at":{"w":0},"vars":{"layer":0,"ways":1},"note":"rat holds 1 way(s) and passes them to pat (now 1), ret (now 1), rot (now 1)."},{"at":{"w":1},"vars":{"layer":1,"ways":1},"note":"pat holds 1 way(s) and passes them to pet (now 1), pot (now 1)."},{"at":{"w":5},"vars":{"layer":1,"ways":1},"note":"ret holds 1 way(s) and passes them to pet (now 2), ren (now 1)."},{"at":{"w":4},"vars":{"layer":1,"ways":1},"note":"rot holds 1 way(s) and passes them to pot (now 2)."},{"at":{"w":2},"vars":{"layer":2,"ways":2},"note":"pet holds 2 way(s) and passes them to pen (now 2)."},{"at":{"w":3},"vars":{"layer":2,"ways":2},"note":"pot holds 2 way(s), and none of its one-letter neighbours is new."},{"at":{"w":6},"vars":{"layer":2,"ways":1},"note":"ren holds 1 way(s) and passes them to pen (now 3), ten (now 1)."}]}
```

<!-- stage: code -->
### Three Sweeps With Different Records

```java
final class GlasshouseSweeps {
    // Walled spread: returns {minutes, fresh left}. 1 fresh, 2 rotten, 3 wall, 0 empty.
    static int[] spread(int[][] g) {
        int h = g.length, w = g[0].length, left = 0, minutes = 0;
        int[] queue = new int[h * w];
        int head = 0, tail = 0;
        boolean[] done = new boolean[h * w];
        for (int i = 0; i < h * w; i++) {
            int v = g[i / w][i % w];
            if (v == 1) left++;
            if (v == 2) { queue[tail++] = i; done[i] = true; }
        }
        int[] step = {w, -w, 1, -1};
        while (head < tail) {
            int layerEnd = tail;
            boolean grew = false;
            for (; head < layerEnd; head++) {
                int cur = queue[head], c = cur % w;
                for (int d = 0; d < 4; d++) {
                    if (d == 2 && c == w - 1 || d == 3 && c == 0) continue;
                    int nxt = cur + step[d];
                    if (nxt < 0 || nxt >= h * w || done[nxt] || g[nxt / w][nxt % w] != 1) continue;
                    done[nxt] = true; queue[tail++] = nxt; left--; grew = true;
                }
            }
            if (grew) minutes++;
        }
        return new int[]{minutes, left};
    }

    // Wrapping distances to the nearest zero, -1 when the grid has none.
    static int[][] wrap(int[][] g) {
        int h = g.length, w = g[0].length;
        int[][] dist = new int[h][w];
        java.util.ArrayDeque<int[]> q = new java.util.ArrayDeque<>();
        for (int r = 0; r < h; r++)
            for (int c = 0; c < w; c++) {
                dist[r][c] = g[r][c] == 0 ? 0 : -1;
                if (g[r][c] == 0) q.add(new int[]{r, c});
            }
        int[][] move = {{1, 0}, {-1, 0}, {0, 1}, {0, -1}};
        while (!q.isEmpty()) {
            int[] cur = q.poll();
            for (int[] m : move) {
                int a = Math.floorMod(cur[0] + m[0], h), b = Math.floorMod(cur[1] + m[1], w);
                if (dist[a][b] == -1) { dist[a][b] = dist[cur[0]][cur[1]] + 1; q.add(new int[]{a, b}); }
            }
        }
        return dist;
    }

    // Number of shortest ladders: layer-final marks, ways summed per layer.
    static long ladders(String from, String to, java.util.List<String> registry) {
        java.util.Set<String> known = new java.util.HashSet<>(registry);
        if (!known.contains(to)) return 0;
        java.util.Map<String, Long> ways = new java.util.HashMap<>();
        java.util.Set<String> final_ = new java.util.HashSet<>();
        ways.put(from, 1L); final_.add(from);
        java.util.List<String> layer = java.util.List.of(from);
        while (!layer.isEmpty() && !ways.containsKey(to)) {
            java.util.Map<String, Long> fresh = new java.util.LinkedHashMap<>();
            for (String s : layer) {
                char[] t = s.toCharArray();
                for (int i = 0; i < t.length; i++) {
                    char keep = t[i];
                    for (char x = 'a'; x <= 'z'; x++) {
                        t[i] = x;
                        String n = new String(t);
                        if (known.contains(n) && !final_.contains(n)) fresh.merge(n, ways.get(s), Long::sum);
                    }
                    t[i] = keep;
                }
            }
            final_.addAll(fresh.keySet());
            ways.putAll(fresh);
            layer = new java.util.ArrayList<>(fresh.keySet());
        }
        return ways.getOrDefault(to, 0L);
    }
}
```

Each sweep visits a vertex once and looks at its moves once, so the walled spread and the wrapping distances cost O(n) for n benches, and the ladder count costs O(V * L * 26) for V tags of length L, plus the time to hash each candidate tag. The queue arrays and tables take O(n) or O(V) memory.

<!-- stage: applicability -->
### Choosing What A Vertex Remembers

Reach for this combination when a shortest-step question has a twist that a plain queue does not cover: spreading from many places at once, a grid that wraps around, moves that go diagonally, blocked starts, or an answer that asks how many shortest routes or cells there are and not only how long. The invariant is that every vertex in the queue holds its final distance, so a vertex can be marked, counted or matched against a second sweep without being reopened.

The first false friend is the model that puts the whole route into the state, as the chain method does. It is correct and it makes every route a separate vertex, so the work grows with the number of routes. A second false friend is a visited mark placed on discovery when the question asks how many ways there are, since the second parent in the same layer is then thrown away and the count comes out too low.

The no-go condition is a move with a cost. If stepping onto one bench takes two minutes and another takes five, a layer is no longer a unit of time and the first arrival may not be the cheapest, so the problem belongs to Chapter 24 and its weighted frontiers. This chapter assigns no problem whose frontier is ordered by a heap or by a double-ended queue.

Java adds one hazard to the wrapping grid. The remainder operator keeps the sign of the dividend, so `(r - 1) % h` is -1 for r = 0 and indexes the array out of range, while `Math.floorMod(r - 1, h)` gives h - 1. Counts of ladders also grow fast, so the sum belongs in a `long`.

<!-- stage: exercises -->
### Exercises

#### [Build] Rotting Oranges (LeetCode 994)
<!-- id: bs-rot-walls-untouched -->

**Prerequisites.** The seed layer from multi-source BFS and the layer clock from the layer-meaning lesson.

**Problem.** A grid holds 0 for an empty cell, 1 for a fresh orange, 2 for a rotten orange and 3 for a wall. Each minute, every fresh orange that shares a side with a rotten orange becomes rotten. Rot never crosses a wall or an empty cell, and it does not move diagonally. Return `[minutes, left]`, where `minutes` is the number of minutes until no more oranges can rot, which is 0 when nothing ever rots, and `left` is the number of fresh oranges that are still fresh at that time.

**Constraints.** 1 <= rows, columns <= 12, and every cell is 0, 1, 2 or 3.

**Example 1.** Input `grid = [[2,1,1],[1,3,1],[0,1,1]]`, output `[5, 0]`.

**Example 2.** Input `grid = [[2,3,1],[3,3,1],[0,1,1]]`, output `[0, 4]`.

**Hint.** Which cells go into the queue before the first minute, and in which situations should the minute counter not be raised?

**Changed decision.** Walls and empty cells both stop the spread, and the answer carries the count of fresh oranges left over instead of a single -1.

#### [Vary] 01 Matrix (LeetCode 542)
<!-- id: bs-torus-nearest-zero -->

**Prerequisites.** The Build rung and the idea that a vertex is a normalized position.

**Problem.** A grid of 0 and 1 is given in which the left edge continues on the right edge and the top edge continues on the bottom edge, so the grid wraps in both directions. Return a grid of the same size in which each cell holds the number of steps to the nearest 0, moving one step up, down, left or right with wrapping. If the grid contains no 0, every cell of the result is -1.

**Constraints.** 1 <= rows, columns <= 10, and every cell is 0 or 1.

**Example 1.** Input `grid = [[1,1,1,1],[0,1,1,1],[1,1,1,1]]`, output `[[1,2,3,2],[0,1,2,1],[1,2,3,2]]`.

**Example 2.** Input `grid = [[1,1],[1,1]]`, output `[[-1,-1],[-1,-1]]`.

**Hint.** What does the position one step left of column 0 normalize to, and what happens when the grid has only one row?

**Changed decision.** Neighbours are computed with a wrapping remainder instead of a bounds test, and a grid with no source ends with a table of -1 and not an error.

#### [Boundary] Shortest Path in Binary Matrix (LeetCode 1091)
<!-- id: bs-diagonal-cells-on-shortest -->

**Prerequisites.** The Vary rung and the idea that visited may store a distance.

**Problem.** An n by n grid holds 0 for an open cell and 1 for a blocked cell. A path starts at the top-left cell and ends at the bottom-right cell, moves between open cells in any of the eight directions, and counts the cells it visits, both ends included. Return `[length, cells]`, where `length` is the number of cells on a shortest path and `cells` is the number of distinct cells that lie on at least one shortest path. If either end is blocked or no path exists, return `[-1, 0]`.

**Constraints.** 1 <= n <= 10, and every cell is 0 or 1.

**Example 1.** Input `grid = [[0,0,0,0],[0,1,1,0],[0,1,1,0],[0,0,0,0]]`, output `[6, 10]`.

**Example 2.** Input `grid = [[0,0],[0,1]]`, output `[-1, 0]`.

**Hint.** What distances would a sweep from the far corner give, and which cells satisfy the two distances adding up to the shortest length?

**Changed decision.** The answer asks about all shortest paths at once, so two distance tables are kept and matched instead of a single path being traced back.

#### [Recognize] Word Ladder (LeetCode 127)
<!-- id: bs-ladder-count -->

**Prerequisites.** The Boundary rung and the state-space lesson.

**Problem.** A start word, a target word and a list of distinct lowercase words of equal length are given. A ladder is a sequence of words that begins with the start word, ends with the target word, changes exactly one letter at each step, and uses only words from the list after the first, where the start word itself need not be in the list. Return the number of different ladders that have the fewest steps, or 0 if there is none, including the case when the target is not in the list.

**Constraints.** 1 <= word length <= 5, 0 <= list length <= 200, and the start and target words are different.

**Example 1.** Input `start = "rat"`, `target = "pen"`, `list = ["pat","pet","pot","rot","ret","ren","pen","ten"]`, output `3`.

**Example 2.** Input `start = "aa"`, `target = "bb"`, `list = ["ab","ba","bb"]`, output `2`.

**Hint.** What must be remembered about a tag found in the current layer before its neighbours are finalized, and when may it be marked as done?

**Changed decision.** The search keeps a count of shortest ways for every tag and marks tags final only at the end of a layer, instead of stopping at the first arrival of the target.
