<!-- solutions-for: 26-dynamic-programming-foundations -->
### Solutions For Table Entry Definitions

#### Solution: [Build] Name The Subproblem (Author exercise)
<!-- id: dp-state-name-subproblem -->

**Approach.**
The sentence is that `dp[i]` is the number of chunk sequences whose sizes add up to exactly `i` bytes. The method sets `dp[0] = 1` for the empty sequence and leaves `dp[1] = 0` as the default. For each larger `i` it considers the last chunk. A last chunk of 2 leaves a sequence that adds up to `i - 2`, and a last chunk of 5 leaves one that adds up to `i - 5`. The two cases are disjoint, and each is read only when its index is not negative.

The invariant is that `dp[i]` matches its sentence for every index the loop has finished. Entries read by index `i` all have smaller indexes, so they are final before they are used. The tests check the empty message, a message of one byte that no chunk fits, and a random comparison with an exhaustive search.

**Complexity.**
- **Time** is O(n), because each of the n entries makes two reads.
- **Space** is O(n) for the array of n + 1 entries.

```java run
import java.util.*;

public final class DpNameSubproblem {
    /**
     * Counts ordered chunk sequences of sizes 2 and 5 that add up to exactly n.
     * Time: O(n). Space: O(n).
     * Invariant: dp[i] is the number of such sequences that add up to exactly i.
     */
    static long countSequences(int n) {
        // Indexes 0..n are all valid states, so the array has n + 1 entries.
        long[] dp = new long[n + 1];
        // The empty sequence is the only way to add up to 0.
        dp[0] = 1;
        // Increasing i guarantees that every smaller index is already final.
        for (int i = 1; i <= n; i++) {
            // The last chunk is 2 or 5, and the index guard avoids a negative read.
            if (i >= 2) dp[i] += dp[i - 2];
            if (i >= 5) dp[i] += dp[i - 5];
        }
        // The original question is the subproblem with i = n.
        return dp[n];
    }

    /** Oracle: exhaustive recursion that appends one chunk at a time. */
    static long oracle(int remaining) {
        if (remaining == 0) return 1;
        long total = 0;
        if (remaining >= 2) total += oracle(remaining - 2);
        if (remaining >= 5) total += oracle(remaining - 5);
        return total;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (countSequences(12) != 4) throw new AssertionError("ex1");
        if (countSequences(1) != 0) throw new AssertionError("ex2");
        // Boundary sizes: empty message, smallest chunk, and a size that mixes both chunks.
        if (countSequences(0) != 1) throw new AssertionError("zero");
        if (countSequences(2) != 1 || countSequences(5) != 1 || countSequences(7) != 2) throw new AssertionError("small");
        // Java fact: a negative index throws, which is why the guards exist.
        try {
            long[] probe = new long[3];
            long unused = probe[-1];
            throw new AssertionError("no exception " + unused);
        } catch (ArrayIndexOutOfBoundsException expected) {
            // The exception confirms the hazard the guards avoid.
        }
        // Every size up to 30 against the exhaustive search.
        for (int n = 0; n <= 30; n++) {
            if (countSequences(n) != oracle(n)) throw new AssertionError("size " + n);
        }
        // Random sizes up to 60 against a second, independent memo-free table built from the sentence.
        Random rnd = new Random(2601);
        for (int t = 0; t < 2000; t++) {
            int n = rnd.nextInt(61);
            long[] ref = new long[n + 6];
            ref[0] = 1;
            for (int i = 1; i <= n; i++) {
                long sum = 0;
                for (int c : new int[] {2, 5}) if (i - c >= 0) sum += ref[i - c];
                ref[i] = sum;
            }
            if (countSequences(n) != ref[n]) throw new AssertionError("random " + n);
        }
    }
}
```

#### Solution: [Vary] Add One Necessary Dimension (Author exercise)
<!-- id: dp-state-add-dimension -->

**Approach.**
The sentence is that `dp[i][u]` is the number of chunk sequences that add up to exactly `i` bytes and contain exactly `u` chunks of size 5. The second index is needed because two calls with the same `i` and different `u` have different futures once a cap exists. The method fills the table in increasing `i`. A last chunk of 2 reads `dp[i - 2][u]`, and a last chunk of 5 reads `dp[i - 5][u - 1]` when `u` is at least 1. The answer sums `dp[n][u]` for `u` from 0 to `k`.

The invariant is that each entry matches its sentence, and the cap is enforced only when the answer sums over `u <= k`. Using a single index of the form `dp[i]` would count sequences with more than `k` fives as valid, and the tests include a case that shows this error.

**Complexity.**
- **Time** is O(n * k), because each of the n + 1 rows computes k + 1 entries with two reads each.
- **Space** is O(n * k) for the table.

```java run
import java.util.*;

public final class DpAddDimension {
    /**
     * Counts chunk sequences of sizes 2 and 5 that add up to n with at most k chunks of size 5.
     * Time: O(n * k). Space: O(n * k).
     * Invariant: dp[i][u] counts sequences adding up to i with exactly u chunks of size 5.
     */
    static long countCapped(int n, int k) {
        // Row i holds the counts for i bytes, column u the number of 5-chunks used.
        long[][] dp = new long[n + 1][k + 1];
        // The empty sequence uses no 5-chunk.
        dp[0][0] = 1;
        // Each row reads only earlier rows.
        for (int i = 1; i <= n; i++) {
            for (int u = 0; u <= k; u++) {
                // A last chunk of 2 keeps the 5-chunk count unchanged.
                if (i >= 2) dp[i][u] += dp[i - 2][u];
                // A last chunk of 5 comes from a sequence with one fewer 5-chunk.
                if (i >= 5 && u >= 1) dp[i][u] += dp[i - 5][u - 1];
            }
        }
        // The cap allows any count of 5-chunks from 0 to k.
        long total = 0;
        for (int u = 0; u <= k; u++) total += dp[n][u];
        return total;
    }

    /** Oracle: exhaustive recursion that carries the number of 5-chunks still allowed. */
    static long oracle(int remaining, int fivesLeft) {
        if (remaining == 0) return 1;
        long total = 0;
        if (remaining >= 2) total += oracle(remaining - 2, fivesLeft);
        if (remaining >= 5 && fivesLeft > 0) total += oracle(remaining - 5, fivesLeft - 1);
        return total;
    }

    /** One-index table that ignores the cap, used to show that it gives a different answer. */
    static long uncapped(int n) {
        long[] dp = new long[n + 1];
        dp[0] = 1;
        for (int i = 1; i <= n; i++) {
            if (i >= 2) dp[i] += dp[i - 2];
            if (i >= 5) dp[i] += dp[i - 5];
        }
        return dp[n];
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (countCapped(12, 2) != 4) throw new AssertionError("ex1");
        if (countCapped(7, 0) != 0) throw new AssertionError("ex2");
        // The cap matters: 12 bytes with one 5-chunk allowed has fewer sequences than the uncapped count.
        if (countCapped(12, 1) != 1) throw new AssertionError("cap one");
        if (countCapped(12, 1) >= uncapped(12)) throw new AssertionError("cap must reduce the count");
        // Boundary: empty message with a zero cap.
        if (countCapped(0, 0) != 1) throw new AssertionError("empty");
        // Random pairs against the exhaustive search.
        Random rnd = new Random(2602);
        for (int t = 0; t < 2000; t++) {
            int n = rnd.nextInt(41);
            int k = rnd.nextInt(13);
            if (countCapped(n, k) != oracle(n, k)) throw new AssertionError("random " + n + " " + k);
        }
    }
}
```

#### Solution: [Boundary] Base-State Contract (Author exercise)
<!-- id: dp-state-base-contract -->

**Approach.**
The sentence is that `ways[i]` is the number of move sequences that start at cell `i` and end at cell `n - 1`. The base entry is `ways[n - 1] = 1`, the empty sequence. For a cell `i` before the end, the first move lands on some cell `i + s` with `s` from 1 to `jump[i]`. The method adds `ways[i + s]` only when `i + s` is at most `n - 1`, so a move past the end contributes 0. The table fills from the last cell down to cell 0, because each entry reads larger indexes.

The invariant is that every read index lies between `i + 1` and `n - 1`, so every transition ends at a defined entry. A track with one cell returns the base entry directly and never reads `jump` for a move.

**Complexity.**
- **Time** is O(n * J), where J is the largest jump value, because each cell tries at most J first moves.
- **Space** is O(n) for the array of n entries.

```java run
import java.util.*;

public final class DpBaseContract {
    /**
     * Counts move sequences from cell 0 to cell n - 1 on a forward track.
     * Time: O(n * J) for the largest jump J. Space: O(n).
     * Invariant: ways[i] is the number of sequences from cell i that end exactly at cell n - 1.
     */
    static long countRoutes(int[] jump) {
        int n = jump.length;
        // One entry per cell, and the default 0 means no route is known yet.
        long[] ways = new long[n];
        // The empty sequence is the only route that starts on the last cell.
        ways[n - 1] = 1;
        // Going backward ensures that every larger index is final before it is read.
        for (int i = n - 2; i >= 0; i--) {
            // The first move has length s, and the loop bound keeps it inside the allowed range.
            for (int s = 1; s <= jump[i]; s++) {
                // A move past the last cell is not allowed, so it adds nothing.
                if (i + s <= n - 1) ways[i] += ways[i + s];
            }
        }
        // The original question starts at cell 0.
        return ways[0];
    }

    /** Oracle: exhaustive recursion over first moves, with an explicit end check. */
    static long oracle(int[] jump, int cell) {
        if (cell == jump.length - 1) return 1;
        long total = 0;
        for (int s = 1; s <= jump[cell]; s++) {
            if (cell + s < jump.length) total += oracle(jump, cell + s);
        }
        return total;
    }

    public static void main(String[] args) {
        // The two examples of the exercise, and a mutation check on the input.
        int[] a = {2, 1, 3, 1, 1};
        int[] aCopy = a.clone();
        if (countRoutes(a) != 4) throw new AssertionError("ex1");
        if (!Arrays.equals(a, aCopy)) throw new AssertionError("input changed");
        if (countRoutes(new int[] {3}) != 1) throw new AssertionError("ex2");
        // Hostile: large jumps near the end must not read past the array.
        if (countRoutes(new int[] {3, 3, 3, 3, 3}) != 7) throw new AssertionError("overshoot");
        if (countRoutes(new int[] {3, 3}) != 1) throw new AssertionError("two cells");
        // Random tracks against the exhaustive search.
        Random rnd = new Random(2603);
        for (int t = 0; t < 2000; t++) {
            int n = 1 + rnd.nextInt(14);
            int[] jump = new int[n];
            for (int i = 0; i < n; i++) jump[i] = 1 + rnd.nextInt(3);
            if (countRoutes(jump) != oracle(jump, 0)) throw new AssertionError("random " + Arrays.toString(jump));
        }
    }
}
```

#### Solution: [Recognize] Climbing With Steps Of One Or Three (LeetCode 70)
<!-- id: dp-state-stairs-one-three -->

**Approach.**
The sentence is that `dp[i]` is the number of move sequences that climb from the ground to step `i`, landing exactly on step `i`. The ground is step 0 and has one way, the empty sequence. The last move of any way to step `i` is a 1-step from `i - 1` or a 3-step from `i - 3`. The two cases are disjoint, so `dp[i] = dp[i - 1] + dp[i - 3]`, and each term is read only when its index is not negative. The answer sits at index `n`.

The invariant is that `dp[i]` matches its sentence for each finished `i`. The sentence chooses the direction on purpose: it says reach and not leave, so index 0 is the base and index `n` is the answer. Mixing the two directions is the usual error here.

**Complexity.**
- **Time** is O(n), because every step makes at most two reads.
- **Space** is O(n) for the array of n + 1 entries.

```java run
import java.util.*;

public final class DpStairsOneThree {
    /**
     * Counts ordered climbs with moves of 1 or 3 steps that land exactly on step n.
     * Time: O(n). Space: O(n).
     * Invariant: dp[i] is the number of move sequences that land exactly on step i.
     */
    static long climbs(int n) {
        // Steps 0..n are all states, so the array has n + 1 entries.
        long[] dp = new long[n + 1];
        // Making no move is the single way to stand on the ground.
        dp[0] = 1;
        // Increasing i keeps every smaller index final.
        for (int i = 1; i <= n; i++) {
            // The last move is a 1-step from i - 1, which always exists for i >= 1.
            dp[i] += dp[i - 1];
            // The last move is a 3-step from i - 3, which exists only for i >= 3.
            if (i >= 3) dp[i] += dp[i - 3];
        }
        // Reaching step n is the original question.
        return dp[n];
    }

    /** Oracle: exhaustive recursion on the steps still to climb. */
    static long oracle(int remaining) {
        if (remaining == 0) return 1;
        long total = oracle(remaining - 1);
        if (remaining >= 3) total += oracle(remaining - 3);
        return total;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (climbs(6) != 6) throw new AssertionError("ex1");
        if (climbs(2) != 1) throw new AssertionError("ex2");
        // Boundary: zero steps, and the first size where the 3-step appears.
        if (climbs(0) != 1) throw new AssertionError("zero");
        if (climbs(3) != 2) throw new AssertionError("three");
        // The result stays inside long for the largest allowed size.
        if (climbs(60) <= 0) throw new AssertionError("overflow");
        // Every size up to 30 against the exhaustive search.
        for (int n = 0; n <= 30; n++) {
            if (climbs(n) != oracle(n)) throw new AssertionError("size " + n);
        }
        // Random sizes against a table built in the opposite direction, from step n down to the ground.
        Random rnd = new Random(2604);
        for (int t = 0; t < 1000; t++) {
            int n = rnd.nextInt(61);
            long[] leave = new long[n + 1];
            leave[n] = 1;
            for (int i = n - 1; i >= 0; i--) {
                leave[i] = leave[i + 1] + (i + 3 <= n ? leave[i + 3] : 0);
            }
            if (climbs(n) != leave[0]) throw new AssertionError("direction " + n);
        }
    }
}
```
