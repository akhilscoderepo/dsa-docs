<!-- solutions-for: 26-dynamic-programming-foundations -->
### Solutions For Recursion And Memoization

#### Solution: [Build] Stairs With A Hit Count (LeetCode 70)
<!-- id: dp-combo-stairs-hit-count -->

**Approach.**
The method allocates a `long[]` of `n + 1` slots filled with -1 and a one-element `int[]` that serves as the hit counter. The recursive helper returns 1 for `k < 2` without touching the array. For larger `k` it first checks the slot. A slot that is not -1 adds one to the counter and returns at once. Otherwise the helper computes the two smaller answers, writes their sum and returns it. The helper makes the call for `k - 1` first, so the slot for `k - 2` is already filled when the second call arrives.

The invariant is that a slot holds either -1 or the exact number of ways for its index, and each slot is written once. The recursion reaches indexes `n` down to 2 as misses, and every second call from index 4 and up is a hit. The counter therefore ends at `n - 3` when `n >= 4`, and at 0 for smaller `n`. The oracle does not use this formula. It walks a call tree that stops at any index requested earlier, and it computes the way count with a separate loop.

**Complexity.**
- **Time** is O(n), because each of the `n - 1` indexes from 2 to `n` is computed once and every call does constant work besides its two sub-calls.
- **Space** is O(n) for the array, and the stack holds at most `n` open calls.

```java run
import java.util.*;

public final class StairsHitCount {
    /**
     * Returns {ways, hits} for n steps, climbing 1 or 2 steps at a time.
     * Time: O(n). Space: O(n).
     * Invariant: a slot is either -1 or the exact way count for its index, written once.
     */
    static long[] solve(int n) {
        // One slot per index from 0 to n, all marked empty with -1.
        long[] memo = new long[n + 1];
        Arrays.fill(memo, -1);
        // The counter is an array so the recursive helper can change it.
        int[] hits = {0};
        long ways = waysUp(n, memo, hits);
        // Return the answer first and the counter second, as the contract states.
        return new long[] {ways, hits[0]};
    }

    /** Memoized recursion. Time: O(1) per call beyond sub-calls. Space: O(1) per frame. */
    static long waysUp(int k, long[] memo, int[] hits) {
        // Zero or one step left has exactly one way, and these calls are not counted as hits.
        if (k < 2) return 1;
        if (memo[k] != -1) {
            // A stored slot answers the call, so the counter rises and the recursion stops.
            hits[0]++;
            return memo[k];
        }
        // The call for k - 1 runs first, which fills the slot that the call for k - 2 reads.
        long first = waysUp(k - 1, memo, hits);
        long second = waysUp(k - 2, memo, hits);
        // Write once, after both branches returned.
        memo[k] = first + second;
        return memo[k];
    }

    /** Oracle: a call tree that stops at an index requested earlier; the answer comes from a loop. */
    static void tree(int k, Set<Integer> requested, int[] hits) {
        // Indexes below 2 are base cases and never count as hits.
        if (k < 2) return;
        // An index requested before counts as one hit and opens no subtree.
        if (!requested.add(k)) {
            hits[0]++;
            return;
        }
        tree(k - 1, requested, hits);
        tree(k - 2, requested, hits);
    }

    /** Oracle for the way count: a plain loop over the two previous values. */
    static long loopWays(int n) {
        long prev = 1, cur = 1;
        for (int k = 2; k <= n; k++) {
            long next = prev + cur;
            prev = cur;
            cur = next;
        }
        return cur;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!Arrays.equals(solve(5), new long[] {8, 2})) throw new AssertionError("example 1");
        if (!Arrays.equals(solve(2), new long[] {2, 0})) throw new AssertionError("example 2");
        // The smallest input has one way and no hits.
        if (!Arrays.equals(solve(1), new long[] {1, 0})) throw new AssertionError("n = 1");
        // The largest input stays inside long: the way count is the Fibonacci number 4660046610375530309.
        long[] big = solve(90);
        if (big[0] != 4660046610375530309L || big[1] != 87) throw new AssertionError("n = 90");
        if (big[0] <= 0) throw new AssertionError("overflow");
        // Every n up to 24 is compared with the plain recursion oracle.
        for (int n = 1; n <= 24; n++) {
            int[] oracleHits = {0};
            tree(n, new HashSet<>(), oracleHits);
            long oracleWays = loopWays(n);
            long[] got = solve(n);
            if (got[0] != oracleWays || got[1] != oracleHits[0]) throw new AssertionError("oracle n = " + n);
        }
        System.out.println("ok");
    }
}
```

#### Solution: [Vary] Houses Chosen By Index (LeetCode 198)
<!-- id: dp-combo-robber-chosen-houses -->

**Approach.**
The method defines `best(i)` as the largest sum that houses `i` to the end can give. A `HashMap<Integer, Integer>` keyed by `i` stores each answer. The value `best(i)` is the larger of `best(i + 1)`, which skips house `i`, and `nums[i] + best(i + 2)`, which takes it. An index past the end gives 0. The key is only `i`, because the answer for a suffix does not depend on what the earlier houses did.

The rebuild walks `i` from 0. All values are positive, so no best selection is a prefix of a different best selection. Therefore the lexicographically smallest list is found greedily. If `nums[i] + best(i + 2)` equals `best(i)`, some best selection of the suffix contains `i`, and it beats every selection that starts later. The walk adds `i` and jumps to `i + 2`. Otherwise it moves to `i + 1`.

**Complexity.**
- **Time** is O(n), because the map holds at most `n` entries and each miss does constant work, and the rebuild walk takes at most `n` steps.
- **Space** is O(n) for the map, the output list and at most `n` open calls.

```java run
import java.util.*;

public final class ChosenHouses {
    /**
     * Returns the lexicographically smallest index list among selections with the largest sum.
     * Time: O(n). Space: O(n).
     * Invariant: memo.get(i) is the best sum of houses i to the end, written once.
     */
    static List<Integer> choose(int[] nums) {
        Map<Integer, Integer> memo = new HashMap<>();
        List<Integer> picked = new ArrayList<>();
        int i = 0;
        // The walk visits each index at most once, so it costs O(n).
        while (i < nums.length) {
            int skip = best(i + 1, nums, memo);
            int take = nums[i] + best(i + 2, nums, memo);
            // Equality means some best selection of the suffix contains i, so take it.
            if (take == Math.max(skip, take)) {
                picked.add(i);
                // The next house is blocked, so the walk jumps by two.
                i += 2;
            } else {
                // Taking i is worse, so the walk moves to the next house.
                i += 1;
            }
        }
        return picked;
    }

    /** Memoized suffix value. Time: O(1) per call beyond sub-calls. Space: O(1) per frame. */
    static int best(int i, int[] nums, Map<Integer, Integer> memo) {
        // An index past the end has no houses and gives 0.
        if (i >= nums.length) return 0;
        // A stored suffix value answers the call.
        Integer stored = memo.get(i);
        if (stored != null) return stored;
        // Compute both branches before the single write.
        int value = Math.max(best(i + 1, nums, memo), nums[i] + best(i + 2, nums, memo));
        memo.put(i, value);
        return value;
    }

    /** Oracle: tries every subset, keeps the largest sum, and breaks ties by list order. */
    static List<Integer> oracle(int[] nums) {
        int n = nums.length;
        long bestSum = -1;
        List<Integer> bestList = null;
        for (int mask = 0; mask < (1 << n); mask++) {
            // Two neighboring bits would choose neighboring houses, so the subset is rejected.
            if ((mask & (mask >> 1)) != 0) continue;
            long sum = 0;
            List<Integer> list = new ArrayList<>();
            for (int k = 0; k < n; k++) {
                if ((mask >> k & 1) == 1) {
                    sum += nums[k];
                    list.add(k);
                }
            }
            if (sum > bestSum || (sum == bestSum && less(list, bestList))) {
                bestSum = sum;
                bestList = list;
            }
        }
        return bestList;
    }

    /** Lexicographic comparison where a proper prefix is smaller. */
    static boolean less(List<Integer> a, List<Integer> b) {
        for (int k = 0; k < Math.min(a.size(), b.size()); k++) {
            if (!a.get(k).equals(b.get(k))) return a.get(k) < b.get(k);
        }
        return a.size() < b.size();
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!choose(new int[] {2, 7, 9, 3, 1}).equals(List.of(0, 2, 4))) throw new AssertionError("example 1");
        if (!choose(new int[] {4, 4, 4, 4}).equals(List.of(0, 2))) throw new AssertionError("example 2");
        // One house is always chosen.
        if (!choose(new int[] {9}).equals(List.of(0))) throw new AssertionError("single house");
        // A tie between index 0 and index 1 goes to index 0.
        if (!choose(new int[] {5, 5}).equals(List.of(0))) throw new AssertionError("two equal houses");
        // The input stays unchanged.
        int[] keep = {3, 8, 3};
        choose(keep);
        if (!Arrays.equals(keep, new int[] {3, 8, 3})) throw new AssertionError("mutation");
        // Random arrays are checked against the subset oracle.
        Random rnd = new Random(11);
        for (int iter = 0; iter < 400; iter++) {
            int n = 1 + rnd.nextInt(12);
            int[] nums = new int[n];
            for (int k = 0; k < n; k++) nums[k] = 1 + rnd.nextInt(4);
            if (!choose(nums).equals(oracle(nums))) throw new AssertionError("oracle " + Arrays.toString(nums));
        }
        // The largest length of 100 houses completes with a recursion depth of about 100.
        int[] longRow = new int[100];
        Arrays.fill(longRow, 1000);
        if (choose(longRow).size() != 50) throw new AssertionError("long row");
        System.out.println("ok");
    }
}
```

#### Solution: [Boundary] Routes Through A Required Tile (LeetCode 62)
<!-- id: dp-combo-routes-through-tile -->

**Approach.**
The question for a call has three parts: the row, the column and a flag that records whether the route has already visited the required tile. The answer onward depends on all three, because a route that has not visited the tile must still visit it later. The method therefore uses a `long[m][n][2]` array filled with -1. On arrival at `(r, c)` the call raises the flag if the tile is the required one. At the last tile it returns the flag, which is 1 for a valid route and 0 otherwise. Elsewhere it adds the counts of the down and right neighbors that stay inside the board.

The invariant is that `memo[r][c][f]` is either -1 or the number of valid completions from `(r, c)` that start with flag value `f` before the arrival test. A key without the flag fails on this exercise, and the main method shows it with a one-line variant. The corner cases work without special code, since a required tile at the start raises the flag on the first call and a required tile at the end raises it on the last.

**Complexity.**
- **Time** is O(m * n), because there are at most `2 * m * n` keys and each miss does constant work.
- **Space** is O(m * n) for the array and O(m + n) for the stack.

```java run
import java.util.*;

public final class RoutesThroughTile {
    /**
     * Returns the number of right-or-down routes that visit tile (wr, wc).
     * Time: O(m * n). Space: O(m * n).
     * Invariant: memo[r][c][f] is -1 or the completion count from (r, c) with entry flag f.
     */
    static long routes(int m, int n, int wr, int wc) {
        long[][][] memo = new long[m][n][2];
        // Every slot starts at -1, which no count equals.
        for (long[][] plane : memo) for (long[] row : plane) Arrays.fill(row, -1);
        return walk(0, 0, 0, m, n, wr, wc, memo);
    }

    /** Memoized walk with the flag in the key. Time: O(1) per call. Space: O(1) per frame. */
    static long walk(int r, int c, int seen, int m, int n, int wr, int wc, long[][][] memo) {
        // The flag rises on the required tile and never falls.
        int flag = seen | ((r == wr && c == wc) ? 1 : 0);
        // A finished route counts as 1 only when the flag is raised.
        if (r == m - 1 && c == n - 1) return flag;
        // A stored count answers the call.
        if (memo[r][c][flag] != -1) return memo[r][c][flag];
        long total = 0;
        // Step down when a lower row exists.
        if (r + 1 < m) total += walk(r + 1, c, flag, m, n, wr, wc, memo);
        // Step right when a column to the right exists.
        if (c + 1 < n) total += walk(r, c + 1, flag, m, n, wr, wc, memo);
        memo[r][c][flag] = total;
        return total;
    }

    /** Wrong variant: the key drops the flag, so one slot serves two different questions. */
    static long routesWithoutFlag(int m, int n, int wr, int wc) {
        long[][] memo = new long[m][n];
        for (long[] row : memo) Arrays.fill(row, -1);
        return flawed(0, 0, 0, m, n, wr, wc, memo);
    }

    static long flawed(int r, int c, int seen, int m, int n, int wr, int wc, long[][] memo) {
        int flag = seen | ((r == wr && c == wc) ? 1 : 0);
        if (r == m - 1 && c == n - 1) return flag;
        if (memo[r][c] != -1) return memo[r][c];
        long total = 0;
        if (r + 1 < m) total += flawed(r + 1, c, flag, m, n, wr, wc, memo);
        if (c + 1 < n) total += flawed(r, c + 1, flag, m, n, wr, wc, memo);
        memo[r][c] = total;
        return total;
    }

    /** Oracle: follows every route with no storage and checks the tile on the way. */
    static long oracle(int r, int c, int m, int n, int wr, int wc, boolean seen) {
        boolean now = seen || (r == wr && c == wc);
        if (r == m - 1 && c == n - 1) return now ? 1 : 0;
        long total = 0;
        if (r + 1 < m) total += oracle(r + 1, c, m, n, wr, wc, now);
        if (c + 1 < n) total += oracle(r, c + 1, m, n, wr, wc, now);
        return total;
    }

    /** Helper for the Java behaviour claims: recursion that writes into the map it is computing in. */
    static final Map<Integer, Long> SHARED = new HashMap<>();

    static long fibInside(int k) {
        if (k < 2) return k;
        return SHARED.computeIfAbsent(k, x -> fibInside(x - 1) + fibInside(x - 2));
    }

    static int dive(int d) {
        return dive(d + 1) + 1;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (routes(3, 3, 1, 1) != 4) throw new AssertionError("example 1");
        if (routes(1, 1, 0, 0) != 1) throw new AssertionError("example 2");
        // A required corner leaves all routes of the board: C(4, 2) = 6 on a 3 by 3 board.
        if (routes(3, 3, 0, 0) != 6 || routes(3, 3, 2, 2) != 6) throw new AssertionError("corners");
        // A required tile on the top row narrows the board to one lane at the start.
        if (routes(3, 3, 0, 2) != 1) throw new AssertionError("top right");
        // The largest board stays inside long: C(38, 19) = 35345263800 routes pass through the start corner.
        if (routes(20, 20, 0, 0) != 35345263800L) throw new AssertionError("20 by 20");
        // Dropping the flag from the key gives a wrong answer on the 3 by 3 board.
        if (routesWithoutFlag(3, 3, 1, 1) == 4) throw new AssertionError("flagless key matched");
        // Random boards are checked against the plain enumeration.
        Random rnd = new Random(5);
        for (int iter = 0; iter < 300; iter++) {
            int m = 1 + rnd.nextInt(7), n = 1 + rnd.nextInt(7);
            int wr = rnd.nextInt(m), wc = rnd.nextInt(n);
            if (routes(m, n, wr, wc) != oracle(0, 0, m, n, wr, wc, false)) throw new AssertionError("oracle");
        }
        // Java claim: two arrays with equal contents are different map keys, while Arrays.equals compares contents.
        Map<int[], Long> byArray = new HashMap<>();
        byArray.put(new int[] {1, 2}, 5L);
        if (byArray.get(new int[] {1, 2}) != null) throw new AssertionError("array key matched");
        if (new int[] {1, 2}.equals(new int[] {1, 2})) throw new AssertionError("array equals");
        if (!Arrays.equals(new int[] {1, 2}, new int[] {1, 2})) throw new AssertionError("Arrays.equals");
        // Java claim: the packed long key is distinct for every pair of a 9 by 9 board.
        Set<Long> keys = new HashSet<>();
        for (int r = 0; r < 9; r++) for (int c = 0; c < 9; c++) keys.add((long) r * 9 + c);
        if (keys.size() != 81) throw new AssertionError("packed keys");
        // Java claim: computeIfAbsent that recurses into the same HashMap throws ConcurrentModificationException.
        boolean threw = false;
        try {
            fibInside(30);
        } catch (ConcurrentModificationException e) {
            threw = true;
        }
        if (!threw) throw new AssertionError("computeIfAbsent did not throw");
        // Java claim: unbounded recursion ends with StackOverflowError.
        boolean overflowed = false;
        try {
            dive(0);
        } catch (StackOverflowError e) {
            overflowed = true;
        }
        if (!overflowed) throw new AssertionError("no stack overflow");
        System.out.println("ok");
    }
}
```

#### Solution: [Recognize] Cheapest Entry Cost Across A Board (LeetCode 64)
<!-- id: dp-combo-entry-cost-board -->

**Approach.**
The statement asks for a smallest total over right-or-down routes, and two routes that reach the same tile share the same future. The question for a call is therefore only the pair `(r, c)`. The method defines `cheapest(r, c)` as the least charge to pay after standing on `(r, c)`, which excludes the charge of that tile itself. At the last tile it returns 0. Elsewhere it takes the smaller of the down option, `cost[r + 1][c] + cheapest(r + 1, c)`, and the right option, with the same shape. A `long[][]` memo filled with -1 stores the answers, and -1 is safe because every answer is at least 0.

The invariant is that `memo[r][c]` is -1 or the exact least onward charge from `(r, c)`. The start tile never enters the sum, which matches the contract. The result type is `long`, since twenty-three charges of 10^9 already pass the `int` range.

**Complexity.**
- **Time** is O(m * n), because each tile computes once and does constant work.
- **Space** is O(m * n) for the memo and O(m + n) for the stack.

```java run
import java.util.*;

public final class EntryCostBoard {
    /**
     * Returns the least total entry charge from the top left to the bottom right tile.
     * Time: O(m * n). Space: O(m * n).
     * Invariant: memo[r][c] is -1 or the least charge still to pay after standing on (r, c).
     */
    static long cheapestRoute(int[][] cost) {
        int m = cost.length, n = cost[0].length;
        long[][] memo = new long[m][n];
        // -1 marks an empty slot, since every real answer is at least 0.
        for (long[] row : memo) Arrays.fill(row, -1);
        return cheapest(0, 0, cost, memo);
    }

    /** Memoized recursion on the tile pair. Time: O(1) per call. Space: O(1) per frame. */
    static long cheapest(int r, int c, int[][] cost, long[][] memo) {
        int m = cost.length, n = cost[0].length;
        // The last tile has nothing left to pay.
        if (r == m - 1 && c == n - 1) return 0;
        // A stored slot answers the call.
        if (memo[r][c] != -1) return memo[r][c];
        // Start with a value larger than any real total, so the first option always wins.
        long best = Long.MAX_VALUE;
        // The down option pays the entry charge of the tile below.
        if (r + 1 < m) best = Math.min(best, cost[r + 1][c] + cheapest(r + 1, c, cost, memo));
        // The right option pays the entry charge of the tile to the right.
        if (c + 1 < n) best = Math.min(best, cost[r][c + 1] + cheapest(r, c + 1, cost, memo));
        memo[r][c] = best;
        return best;
    }

    /** Oracle: enumerates every route with no storage. */
    static long oracle(int r, int c, int[][] cost) {
        int m = cost.length, n = cost[0].length;
        if (r == m - 1 && c == n - 1) return 0;
        long best = Long.MAX_VALUE;
        if (r + 1 < m) best = Math.min(best, cost[r + 1][c] + oracle(r + 1, c, cost));
        if (c + 1 < n) best = Math.min(best, cost[r][c + 1] + oracle(r, c + 1, cost));
        return best;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (cheapestRoute(new int[][] {{5, 2, 8}, {1, 9, 3}, {4, 1, 2}}) != 8) throw new AssertionError("example 1");
        if (cheapestRoute(new int[][] {{0, 7, 2, 6}, {3, 1, 9, 4}}) != 17) throw new AssertionError("example 2");
        // A single tile costs nothing, whatever its charge is.
        if (cheapestRoute(new int[][] {{777}}) != 0) throw new AssertionError("single tile");
        // One row pays every entered tile, and one column does the same.
        if (cheapestRoute(new int[][] {{9, 1, 2, 3}}) != 6) throw new AssertionError("one row");
        if (cheapestRoute(new int[][] {{9}, {4}, {5}}) != 9) throw new AssertionError("one column");
        // The largest board with maximum charges needs long: 22 entries of 10^9 exceed the int range.
        int[][] heavy = new int[12][12];
        for (int[] row : heavy) Arrays.fill(row, 1_000_000_000);
        if (cheapestRoute(heavy) != 22_000_000_000L) throw new AssertionError("heavy board");
        // Random boards are checked against the plain enumeration.
        Random rnd = new Random(3);
        for (int iter = 0; iter < 400; iter++) {
            int m = 1 + rnd.nextInt(6), n = 1 + rnd.nextInt(6);
            int[][] cost = new int[m][n];
            for (int[] row : cost) for (int c = 0; c < n; c++) row[c] = rnd.nextInt(20);
            if (cheapestRoute(cost) != oracle(0, 0, cost)) throw new AssertionError("oracle");
        }
        System.out.println("ok");
    }
}
```
