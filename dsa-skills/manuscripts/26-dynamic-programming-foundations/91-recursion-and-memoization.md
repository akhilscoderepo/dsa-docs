<!-- lesson-kind: combination -->
<!-- lesson-id: recursion-and-memoization -->
## Recursion And Memoization

<!-- stage: context -->
### A Map That Never Gets Reused

A level editor for a tile game shows designers how many monotone routes cross a board. A route starts at the top left tile, ends at the bottom right tile and moves only right or down. A developer writes a recursive method that adds the route counts of the two neighbors. The method answers a 3 by 3 board at once, but a 16 by 16 board takes a visible pause, and a 20 by 20 board does not finish during a code review.

The developer adds a `HashMap` that stores each finished answer, expecting a speedup. The pause stays the same, and the map grows to hundreds of thousands of entries. The code is not wrong, because every answer is still correct. Something in the way the map is used prevents it from helping.

This lesson asks what must be true about the values a recursive method receives, and about the map that stores its answers, so that each distinct question is computed once. The methods below read integers, return a `long` and change no input.

<!-- stage: contributions -->
### What Two Earlier Skills Add

#### What Recursion Supplies

A recursive method gives every subproblem a name, which is the list of arguments of one call. The call `routes(r, c)` asks for the count from tile `(r, c)` to the corner. Its base case answers the smallest questions directly, and its recursive case combines answers to smaller questions. Each call also occupies one stack frame until it returns. The longest chain of nested calls therefore decides how much stack the method uses.

#### What Memoization Supplies

Memoization adds a store that maps a finished question to its answer. The first call for a question computes the answer and writes it. Every later call for the same question reads the stored value and returns. A marker that no real answer can equal, such as -1 for a count, tells an empty slot from a stored result. The store bounds the total work by the number of distinct questions, no matter how often the recursion asks them.

#### What Both Add Together

Neither skill suffices alone. Recursion without a store repeats questions, and a store without a precise question name returns wrong or missing answers. The combination ties the two together through one rule: the store is indexed by exactly the arguments that the answer depends on. The next sections show how that rule fails when an argument is missing, when an argument is wrapped badly, and when the argument is correct and the work collapses from exponential to linear.

<!-- stage: naive -->
### Storing Answers Under Array Keys

The developer's first repair keeps the recursive method and wraps each pair of coordinates in a small array. The method looks up the array in a map before it computes anything, and it stores the result before it returns. The base case says that a tile in the last row or last column has exactly one route to the corner.

```java
static long routes(int rows, int cols) {
    Map<int[], Long> seen = new HashMap<>();
    return routes(0, 0, rows, cols, seen);
}

static long routes(int r, int c, int rows, int cols, Map<int[], Long> seen) {
    int[] state = {r, c};
    Long stored = seen.get(state);
    if (stored != null) return stored;
    long result;
    if (r == rows - 1 || c == cols - 1) {
        result = 1;
    } else {
        result = routes(r + 1, c, rows, cols, seen) + routes(r, c + 1, rows, cols, seen);
    }
    seen.put(state, result);
    return result;
}
```

The code compiles and returns correct counts. The plan reads sensibly: look up, compute, store.

```predict
For a 3 by 3 board, how many entries does seen hold when routes(0, 0, 3, 3, seen) returns, and how many lookups succeed?

The map holds 11 entries and no lookup succeeds. The method makes 11 calls, and each call creates a new array object. Java compares arrays by identity, so a new array never equals an earlier one that holds the same two numbers. The 11 calls reach only 8 distinct tiles, so 3 entries are duplicates that the map cannot recognize.
```

<!-- stage: bottleneck -->
### Why The Map Never Answers

#### The Lookup Fails Every Time

The method `get` on a `HashMap` finds a key through its `hashCode` and `equals` methods. An array inherits both methods from `Object`, so two arrays with equal contents are different keys. Every call creates a fresh array, misses the map, computes the answer again and adds one more entry. The map costs memory and time and saves nothing.

#### The Calls Grow With The Routes

Without working lookups, every leaf of the call tree returns 1, so the number of calls is at least the number of routes. A board with `m` rows and `n` columns has C(m + n - 2, m - 1) routes, and the call count grows at the same rate, which is O(C(m + n - 2, m - 1)). A 10 by 10 board makes 97239 calls. A 20 by 20 board makes more than 10^10 calls. The board has only 400 distinct tiles.

#### A Plan That Names Each Question

The repair must make equal questions equal keys. Then the call count falls to the number of distinct tiles, and each tile does a constant amount of work. The stack depth stays at most `rows + cols`, because every call moves one step toward the corner.

<!-- stage: insight -->
### Make The Arguments The Key

A **cache key** is the value that identifies one question in the store. For a recursive method, the key must contain every argument that can change the answer, and it must compare by value. A pair of `int` values packed into one `long`, such as `(long) r * cols + c`, meets both needs. A two-dimensional `long[][]` array indexed by `r` and `c` meets them as well, with the indexes as the key.

A **cache hit** is a call that finds its key already stored and returns the stored value without recursing. The first call for a key is a miss. It recurses, computes and writes. The total number of misses therefore equals the number of distinct keys that the recursion reaches, and every other call is a hit. On the 3 by 3 board a working store reduces the 11 calls to 9: 8 misses and 1 hit.

The **recursion depth** is the number of nested calls that are open at one moment. Memoization keeps the depth unchanged, because a miss still recurses all the way to a base case before its first write. For the board, the depth is at most `rows + cols - 1`. For the row of houses in the first trace below, the depth is at most the number of houses. A depth beyond what the thread stack holds throws a `StackOverflowError`, and a table filled in a loop avoids that limit.

<!-- names: cache key, cache hit, recursion depth -->

The combined **invariant** has three parts. A stored value always equals the answer for its key. A slot is written at most once. A call that does not find its key stores the key before it returns. From the invariant, the time is the number of distinct keys times the work per miss.

<!-- stage: variables -->
### What The Memoized Method Keeps

Each method in this lesson keeps the same small set of names, and the traces and exercises use them with these meanings.

- **memo** is a `long[]`, a `long[][]` or a `HashMap<Long, Long>`, and the value -1 marks an empty slot in the array forms. The map form tests `containsKey` instead.
- **hits** is an `int` that counts the calls answered by reading `memo`.
- **misses** is an `int` that counts the calls that compute and write a value.
- **depth** is the number of calls that are open on the stack right now, and the deepest value seen is the stack cost.
- **state** is the tuple of arguments that names one question, such as the index `i` or the pair `r` and `c`.

Every answer in this lesson is a count or a sum that fits in a `long`. A count that can pass 9.2 * 10^18 needs a different type, so each exercise limits its input to stay under that bound.

<!-- stage: trace -->
### Two Memoized Runs Step By Step

#### House Values With A Hit Counter

The first run solves a row of five house values, `4 1 2 9 3`, with the rule that two neighboring houses cannot both be chosen. The method `best(i)` returns the largest sum available from houses `i` onward. Each cell is a house value, and the pointer `i` marks the call that just finished. The variable `memo` lists the stored answers by index, with a dot for an empty slot. The variable `hits` counts calls answered from `memo`. Calls with `i` past the last house return 0 and do not appear. The call `best(4)` is the first to finish, and `best(2)` later reads the stored value of `best(4)` without computing it.

```trace
{"cells":[4,1,2,9,3],"pointers":["i"],"steps":[{"at":{"i":-1},"vars":{"memo":". . . . .","hits":0},"note":"No call has finished. All five slots are empty."},{"at":{"i":4},"vars":{"memo":". . . . 3","hits":0},"note":"best(4) skips for 0 or takes for 3, and it stores 3."},{"at":{"i":3},"vars":{"memo":". . . 9 3","hits":0},"note":"best(3) skips for 3 or takes for 9, and it stores 9."},{"at":{"i":4},"vars":{"memo":". . . 9 3","hits":1},"note":"best(4) finds the stored value 3 and returns without recursing. This is hit 1."},{"at":{"i":2},"vars":{"memo":". . 9 9 3","hits":1},"note":"best(2) skips for 9 or takes for 5, and it stores 9."},{"at":{"i":3},"vars":{"memo":". . 9 9 3","hits":2},"note":"best(3) finds the stored value 9 and returns without recursing. This is hit 2."},{"at":{"i":1},"vars":{"memo":". 10 9 9 3","hits":2},"note":"best(1) skips for 9 or takes for 10, and it stores 10."},{"at":{"i":2},"vars":{"memo":". 10 9 9 3","hits":3},"note":"best(2) finds the stored value 9 and returns without recursing. This is hit 3."},{"at":{"i":0},"vars":{"memo":"13 10 9 9 3","hits":3},"note":"best(0) skips for 10 or takes for 13, and it stores 13."}]}
```

The final answer is 13, which comes from houses 0 and 3. Notice that the run makes exactly five misses, one per index, and three hits.

#### Board Routes With A Pair Key

The second run counts routes on a 3 by 3 board. Each cell is a tile in row-major order, written `r,c`. The pointer `tile` marks the call that just finished. The variable `memo` shows the stored counts in the same row-major order, with a dot for an empty slot. The variable `hits` counts reads from `memo`. The tile `1,1` computes once under the call for `1,0`, and the call for `0,1` later reads that stored count.

```trace
{"cells":["0,0","0,1","0,2","1,0","1,1","1,2","2,0","2,1","2,2"],"pointers":["tile"],"steps":[{"at":{"tile":-1},"vars":{"memo":". . . . . . . . .","hits":0},"note":"No call has finished. All nine slots are empty."},{"at":{"tile":6},"vars":{"memo":". . . . . . 1 . .","hits":0},"note":"Tile 2,0 stores 1. It lies in the last row or column, so it has one route."},{"at":{"tile":7},"vars":{"memo":". . . . . . 1 1 .","hits":0},"note":"Tile 2,1 stores 1. It lies in the last row or column, so it has one route."},{"at":{"tile":5},"vars":{"memo":". . . . . 1 1 1 .","hits":0},"note":"Tile 1,2 stores 1. It lies in the last row or column, so it has one route."},{"at":{"tile":4},"vars":{"memo":". . . . 2 1 1 1 .","hits":0},"note":"Tile 1,1 stores 2. It adds the counts of tiles 2,1 and 1,2."},{"at":{"tile":3},"vars":{"memo":". . . 3 2 1 1 1 .","hits":0},"note":"Tile 1,0 stores 3. It adds the counts of tiles 2,0 and 1,1."},{"at":{"tile":4},"vars":{"memo":". . . 3 2 1 1 1 .","hits":1},"note":"Tile 1,1 is already stored as 2, so the call returns it. This is the hit."},{"at":{"tile":2},"vars":{"memo":". . 1 3 2 1 1 1 .","hits":1},"note":"Tile 0,2 stores 1. It lies in the last row or column, so it has one route."},{"at":{"tile":1},"vars":{"memo":". 3 1 3 2 1 1 1 .","hits":1},"note":"Tile 0,1 stores 3. It adds the counts of tiles 1,1 and 0,2."},{"at":{"tile":0},"vars":{"memo":"6 3 1 3 2 1 1 1 .","hits":1},"note":"Tile 0,0 stores 6. It adds the counts of tiles 1,0 and 0,1."}]}
```

The answer is 6, and the run makes 9 calls: 8 misses and 1 hit. Notice that the only hit is the second arrival at tile `1,1`. The corner tile `2,2` is never visited.

<!-- stage: code -->
### Three Memoized Forms In Java

#### Array Memo For A Single Index

The first form uses a `long[]` when the argument is one index in a known range. The sentinel -1 is safe because a count of ways is never negative. The array has `n + 1` slots, so the index `n` is valid.

```java
static long waysUp(int step, long[] memo) {
    if (step < 2) return 1;                       // zero or one step left has exactly one way
    if (memo[step] != -1) return memo[step];      // stored answer: return without recursing
    memo[step] = waysUp(step - 1, memo) + waysUp(step - 2, memo);
    return memo[step];
}
```

#### Packed Key For Two Indexes

The second form packs `r` and `c` into one `long`, so the key compares by value. The multiplier is the column count, and each pair `(r, c)` gives a different key while `0 <= c < cols`. The method uses `containsKey` and `get` in separate steps and writes only after both recursive calls return.

```java
static long routes(int r, int c, int rows, int cols, Map<Long, Long> memo) {
    long key = (long) r * cols + c;                     // distinct for every pair in range
    if (memo.containsKey(key)) return memo.get(key);    // stored answer
    long result = 1;                                    // last row or column has one route
    if (r < rows - 1 && c < cols - 1) {
        long down = routes(r + 1, c, rows, cols, memo); // finish both branches before writing
        long right = routes(r, c + 1, rows, cols, memo);
        result = down + right;
    }
    memo.put(key, result);                              // write once, after the recursion returns
    return result;
}
```

#### Extra Argument In The Key

The third form adds a flag to the question. The answer for a tile depends on whether the route has passed a required tile, so the table has a third index. The flag is part of the key because dropping it gives one slot two different answers.

```java
static long viaTile(int r, int c, int seen, int[] size, int[] must, long[][][] memo) {
    int flag = seen | (r == must[0] && c == must[1] ? 1 : 0);   // flag becomes 1 on the required tile
    if (r == size[0] - 1 && c == size[1] - 1) return flag;       // a finished route counts only with flag 1
    if (memo[r][c][flag] != -1) return memo[r][c][flag];
    long total = 0;
    if (r + 1 < size[0]) total += viaTile(r + 1, c, flag, size, must, memo);   // step down
    if (c + 1 < size[1]) total += viaTile(r, c + 1, flag, size, must, memo);   // step right
    memo[r][c][flag] = total;
    return total;
}
```

<!-- stage: applicability -->
### Choosing Memoized Recursion

#### Reading The Cue

Look for a recursive definition whose calls repeat the same arguments. A counting or optimizing question over indexes or coordinates usually fits. The test is to draw the calls for a small input and mark any argument list that appears twice. When the number of distinct argument lists is small, add a store keyed by the whole list. When the stack depth could reach several thousand, fill a table in dependency order instead.

#### Checking The Invariant

The invariant says that the stored value for a key equals the answer to that key, and that no slot is written twice. Test it on the smallest input, on an input with one row or one element, and on an input where the optional argument takes both values. Count the misses and compare them with the number of distinct argument lists. A difference points to a missing or extra part of the key.

#### Avoiding The False Friend

A **false friend** is a technique that looks right and breaks quietly. Three appear here. An `int[]` or a `List` of changing contents used as a map key never hits, or it hits with stale contents. A key that drops an argument stores one answer for two different questions, and the output is wrong without any exception. Calling `computeIfAbsent` with a function that recurses into the same `HashMap` throws a `ConcurrentModificationException` in current Java versions. The packed `long` and the array indexed by every argument avoid all three.

<!-- stage: exercises -->
### Exercises

#### [Build] Stairs With A Hit Count (LeetCode 70)
<!-- id: dp-combo-stairs-hit-count -->

**Prerequisites.** The memoization and linear recurrence lessons in this chapter.

**Problem.** A staircase has `n` steps, and a climber moves 1 or 2 steps at a time. The method `ways(k)` returns 1 when `k < 2`. Otherwise it reads `memo[k]` if that slot is not -1, and it counts that read as one hit. When the slot is -1, it stores `ways(k - 1) + ways(k - 2)` in `memo[k]`. All slots start at -1. Return a `long[]` of length 2 that holds the value of `ways(n)` and the number of hits made during that one call.

**Constraints.** The limits are:
- **Steps** satisfy `1 <= n <= 90`.
- **Result** holds the way count at index 0 and the hit count at index 1.
- **Hits** count only reads of a stored slot with `k >= 2`.
- **Overflow** cannot occur, since the count for `n = 90` is below 9.2 * 10^18.

**Example 1.** Input `n = 5`, output `[8, 2]`.

**Example 2.** Input `n = 2`, output `[2, 0]`.

**Hint.** Which call reads a slot that an earlier branch has already filled?

**Changed decision.** The recursion now returns two numbers because a counter travels with the memo. The counter must change only on a read of a stored slot.

#### [Vary] Houses Chosen By Index (LeetCode 198)
<!-- id: dp-combo-robber-chosen-houses -->

**Prerequisites.** The exercise above and the take-or-skip lesson.

**Problem.** The array `nums` holds the positive value of each house. A selection is a set of indexes with no two neighboring indexes. Among all selections with the largest sum, return the one whose sorted index list is smallest in lexicographic order. Return that list in increasing order.

**Constraints.** The limits are:
- **Length** satisfies `1 <= nums.length <= 100`.
- **Values** satisfy `1 <= nums[i] <= 1000`.
- **Result** is an increasing list of indexes.
- **Ties** go to the list that holds the smaller index at the first position where lists differ.
- **Input** stays unchanged.

**Example 1.** Input `nums = [2,7,9,3,1]`, output `[0,2,4]`.

**Example 2.** Input `nums = [4,4,4,4]`, output `[0,2]`.

**Hint.** After the stored best sums are known, which test at index `i` shows whether some best selection contains `i`?

**Changed decision.** The method reads the stored sums to rebuild the selection, and it prefers taking index `i` whenever taking it still reaches the best sum.

#### [Boundary] Routes Through A Required Tile (LeetCode 62)
<!-- id: dp-combo-routes-through-tile -->

**Prerequisites.** The grid lesson and the exercises above.

**Problem.** A board has `m` rows and `n` columns. A route starts at row 0, column 0, ends at row `m - 1`, column `n - 1`, and moves one tile right or one tile down per step. Given a required tile `(wr, wc)`, return the number of routes that visit that tile. The start tile and the end tile count as visited.

**Constraints.** The limits are:
- **Board** satisfies `1 <= m, n <= 20`.
- **Required tile** satisfies `0 <= wr < m` and `0 <= wc < n`.
- **Result** is a `long`.
- **Corners** are allowed as the required tile.

**Example 1.** Input `m = 3`, `n = 3`, `wr = 1`, `wc = 1`, output `4`.

**Example 2.** Input `m = 1`, `n = 1`, `wr = 0`, `wc = 0`, output `1`.

**Hint.** Does the count from a tile onward depend only on the tile, or also on what the route visited before?

**Changed decision.** The key gains a flag that records whether the required tile has been visited. Two arrivals at the same tile with different flags have different futures.

#### [Recognize] Cheapest Entry Cost Across A Board (LeetCode 64)
<!-- id: dp-combo-entry-cost-board -->

**Prerequisites.** The grid lesson and the exercises above.

**Problem.** The matrix `cost` holds a non-negative charge for entering each tile. A route starts at row 0, column 0, ends at the last row and last column, and moves one tile right or one tile down per step. The route pays the charge of every tile it enters, and it pays nothing for the start tile. Return the smallest total charge over all routes.

**Constraints.** The limits are:
- **Rows and columns** satisfy `1 <= m, n <= 12`.
- **Charges** satisfy `0 <= cost[r][c] <= 1000000000`.
- **Result** is a `long`, and a 1 by 1 board gives 0.
- **Input** stays unchanged.

**Example 1.** Input `cost = [[5,2,8],[1,9,3],[4,1,2]]`, output `8`.

**Example 2.** Input `cost = [[0,7,2,6],[3,1,9,4]]`, output `17`.

**Hint.** Which arguments of a call to `cheapest(r, c)` change its answer?

**Changed decision.** The objective becomes a minimum, and the start tile is free. The key stays the pair `(r, c)`, because the best cost onward depends only on the tile.
