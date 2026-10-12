<!-- solutions-for: 26-dynamic-programming-foundations -->
### Solutions For Caching And Tables

#### Solution: [Build] Memoized Fibonacci (Author exercise)
<!-- id: dp-memo-fib-cache -->

**Approach.**
The method allocates a `long[]` of length `n + 1` and fills it with `-1`, a value that no Fibonacci number equals. The recursive helper returns `k` directly for `k < 2`. For larger `k` it returns the cached value when the entry is not the marker. Otherwise it calls itself for `k - 1` and `k - 2`, stores the sum, and returns it. The store happens after both calls return, so a cache entry is never a partial result.

The invariant is that every entry is either the marker or the final value of `F(k)`. Each entry changes at most once, so each argument from 2 to `n` runs its sum a single time. The tests count the additions to confirm this, and they check that the marker `0` would have been wrong for `F(0)`.

**Complexity.**
- **Time** is O(n), because each argument from 2 to n computes one sum and every other call returns at once.
- **Space** is O(n) for the cache plus O(n) for the active calls.

```java run
import java.util.*;

public final class DpMemoFibCache {
    static int additions;

    /**
     * Returns F(n) using a cache of completed answers.
     * Time: O(n). Space: O(n) for the cache and O(n) for the call stack.
     * Invariant: memo[k] is -1 or the final value of F(k).
     */
    static long fibMemo(int n) {
        // The marker -1 cannot be a Fibonacci number, unlike the default 0.
        long[] memo = new long[n + 1];
        Arrays.fill(memo, -1);
        return fibFrom(n, memo);
    }

    private static long fibFrom(int k, long[] memo) {
        // Base values need no cache, and this check keeps the indexes below 2 out of the array logic.
        if (k < 2) return k;
        // A completed answer is returned without recursing.
        if (memo[k] != -1) return memo[k];
        // Both smaller answers are finished before the sum is stored.
        memo[k] = fibFrom(k - 1, memo) + fibFrom(k - 2, memo);
        additions++;
        return memo[k];
    }

    /** Oracle: two rolling values that never use a table. */
    static long oracle(int n) {
        long a = 0, b = 1;
        for (int i = 0; i < n; i++) {
            long next = a + b;
            a = b;
            b = next;
        }
        return a;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (fibMemo(50) != 12586269025L) throw new AssertionError("ex1");
        if (fibMemo(0) != 0) throw new AssertionError("ex2");
        // Boundary: n = 1 has a cache of two entries and no addition.
        additions = 0;
        if (fibMemo(1) != 1 || additions != 0) throw new AssertionError("one");
        // The cache limits the work: n - 1 additions for any n >= 2.
        additions = 0;
        if (fibMemo(90) != 2880067194370816120L) throw new AssertionError("largest");
        if (additions != 89) throw new AssertionError("additions " + additions);
        // Java fact: a new long array holds 0, which equals F(0), so 0 cannot mark an empty slot.
        long[] fresh = new long[2];
        if (fresh[0] != 0) throw new AssertionError("default");
        // Java fact: F(93) does not fit in a long and wraps to a negative number.
        if (oracle(93) >= 0) throw new AssertionError("wrap");
        // Every allowed index against the iterative oracle.
        for (int n = 0; n <= 90; n++) {
            if (fibMemo(n) != oracle(n)) throw new AssertionError("index " + n);
        }
    }
}
```

#### Solution: [Vary] Bottom-Up Fibonacci (Author exercise)
<!-- id: dp-memo-fib-table -->

**Approach.**
The method allocates a `long[]` of length `n + 1` and fills it with a loop in increasing index order. The base entries are `0 % m` and `1 % m`, so the value 1 reduces to 0 when `m` is 1. For an index `i >= 2` the sum of the two previous reduced entries is computed in `long` and reduced once. Each reduced entry is below `m`, so the sum stays below `4 * 10^9` and fits in a `long`. An `int` sum would overflow for large `m`.

The invariant is that `table[i]` equals `F(i) % m` for every finished index. Reduction after each addition is valid because addition commutes with the remainder. The array length is `n + 1`, and the base entry for index 1 is written only when it exists.

**Complexity.**
- **Time** is O(n), because each index performs one addition and one remainder.
- **Space** is O(n) for the returned array.

```java run
import java.util.*;

public final class DpMemoFibTable {
    /**
     * Returns F(0..n) with every entry reduced modulo m.
     * Time: O(n). Space: O(n).
     * Invariant: table[i] equals F(i) modulo m for every index the loop has finished.
     */
    static long[] fibTable(int n, int m) {
        // One entry per index 0..n.
        long[] table = new long[n + 1];
        // F(0) = 0 is the array default; F(1) exists only when n >= 1, and it is reduced as well.
        if (n >= 1) table[1] = 1 % m;
        // The loop runs upward because index i reads indexes i - 1 and i - 2.
        for (int i = 2; i <= n; i++) {
            // Both operands are below m, so the long sum cannot overflow.
            table[i] = (table[i - 1] + table[i - 2]) % m;
        }
        return table;
    }

    /** Oracle: exact Fibonacci numbers from BigInteger, reduced afterwards. */
    static long[] oracle(int n, int m) {
        java.math.BigInteger a = java.math.BigInteger.ZERO, b = java.math.BigInteger.ONE;
        java.math.BigInteger mod = java.math.BigInteger.valueOf(m);
        long[] out = new long[n + 1];
        for (int i = 0; i <= n; i++) {
            out[i] = a.mod(mod).longValue();
            java.math.BigInteger next = a.add(b);
            a = b;
            b = next;
        }
        return out;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!Arrays.equals(fibTable(6, 10), new long[] {0, 1, 1, 2, 3, 5, 8})) throw new AssertionError("ex1");
        if (!Arrays.equals(fibTable(10, 7), new long[] {0, 1, 1, 2, 3, 5, 1, 6, 0, 6, 6})) throw new AssertionError("ex2");
        // Boundary: n = 0 gives one entry, and m = 1 reduces every entry to 0.
        if (!Arrays.equals(fibTable(0, 5), new long[] {0})) throw new AssertionError("n zero");
        if (!Arrays.equals(fibTable(5, 1), new long[6])) throw new AssertionError("m one");
        // Java fact: an int sum of two values near 1.2 * 10^9 overflows, while the long sum does not.
        int big = 1_200_000_000;
        if (big + big >= 0) throw new AssertionError("int overflow");
        if ((long) big + big != 2_400_000_000L) throw new AssertionError("long sum");
        // The largest modulus keeps all entries below it.
        for (long v : fibTable(1000, 2_000_000_000)) if (v < 0 || v >= 2_000_000_000L) throw new AssertionError("range");
        // Random sizes and moduli against the BigInteger oracle.
        Random rnd = new Random(2606);
        for (int t = 0; t < 1000; t++) {
            int n = rnd.nextInt(300);
            int m = 1 + rnd.nextInt(rnd.nextBoolean() ? 20 : 1_000_000_000);
            if (!Arrays.equals(fibTable(n, m), oracle(n, m))) throw new AssertionError("random " + n + " " + m);
        }
    }
}
```

#### Solution: [Boundary] Zero And One (Author exercise)
<!-- id: dp-memo-zero-one -->

**Approach.**
The table has length `Math.max(2, n + 1)`, so both base indexes exist even when `n` is 0. The method writes `table[0] = 2` and `table[1] = 1`, then fills indexes 2 through `n` in increasing order. For `n = 0` the loop does not run and the answer is the base value 2. Without the larger length, the write to index 1 would throw an exception for `n = 0`, and a table that assumes entry 0 is the default 0 would return the wrong value.

The invariant is that `table[i]` equals `L(i)` for every finished index, and the answer is read from index `n`, which always exists. The length rule is the only addition to the Fibonacci form.

**Complexity.**
- **Time** is O(n), because each index from 2 to n performs one addition.
- **Space** is O(n) for the table, with a minimum of two entries.

```java run
import java.util.*;

public final class DpMemoZeroOne {
    /**
     * Returns the Lucas number L(n) from a table filled in increasing index order.
     * Time: O(n). Space: O(n).
     * Invariant: table[i] equals L(i) for every index the loop has finished.
     */
    static long lucas(int n) {
        // The table keeps room for both base indexes, even when n is 0.
        long[] table = new long[Math.max(2, n + 1)];
        // The base entries are not 0 and 1, so the defaults are wrong for index 0.
        table[0] = 2;
        table[1] = 1;
        // Index i reads two smaller indexes, so the loop runs upward.
        for (int i = 2; i <= n; i++) table[i] = table[i - 1] + table[i - 2];
        // The answer sits at index n, which always exists.
        return table[n];
    }

    /** Oracle: plain recursion on the recurrence, valid for small n only. */
    static long oracle(int n) {
        if (n == 0) return 2;
        if (n == 1) return 1;
        return oracle(n - 1) + oracle(n - 2);
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (lucas(0) != 2) throw new AssertionError("ex1");
        if (lucas(5) != 11) throw new AssertionError("ex2");
        // Boundary: the second base value, and the largest allowed index.
        if (lucas(1) != 1) throw new AssertionError("one");
        if (lucas(80) != 52361396397820127L) throw new AssertionError("largest");
        // Java fact: writing index 1 of a one-entry array throws, which is why the length has a floor.
        try {
            long[] tooSmall = new long[1];
            tooSmall[1] = 1;
            throw new AssertionError("no exception");
        } catch (ArrayIndexOutOfBoundsException expected) {
            // The exception confirms the hazard the floor avoids.
        }
        // Every small index against the recursive oracle.
        for (int n = 0; n <= 25; n++) {
            if (lucas(n) != oracle(n)) throw new AssertionError("index " + n);
        }
        // Random larger indexes against the identity L(n) = F(n - 1) + F(n + 1).
        Random rnd = new Random(2607);
        for (int t = 0; t < 500; t++) {
            int n = 1 + rnd.nextInt(79);
            long a = 0, b = 1;
            for (int i = 0; i < n - 1; i++) {
                long next = a + b;
                a = b;
                b = next;
            }
            // After the loop a = F(n - 1) and b = F(n), so F(n + 1) = a + b.
            if (lucas(n) != a + (a + b)) throw new AssertionError("identity " + n);
        }
    }
}
```

#### Solution: [Recognize] Stairs With Broken Steps (LeetCode 70)
<!-- id: dp-memo-stairs-broken -->

**Approach.**
The sentence is that `ways[i]` is the number of move sequences of 1 or 2 steps that land exactly on step `i` without landing on any broken step. A marker array records the broken steps. The memoized form is a recursion on the step index. It returns 1 for step 0, returns 0 for a broken step, and otherwise caches the sum of the answers for `i - 1` and `i - 2`, where the second term is read only when `i >= 2`. The tabulated form fills the same entries in increasing index order. Both forms return the answer for step `n`.

The invariant is that every finished entry matches its sentence, and a broken step always holds 0, so no way passes through it. The memoized form keeps up to `n + 1` calls active on the call stack, and the tabulated form keeps none, so both use O(n) memory but only the memoized form depends on the stack size. The test records the deepest recursion and compares it with `n + 1` when nothing is broken.

**Complexity.**
- **Time** is O(n + b), where b is the length of `broken`, because marking costs b and each step performs one addition.
- **Space** is O(n) for the cache or table, plus O(n) for the call stack in the memoized form.

```java run
import java.util.*;

public final class DpMemoStairsBroken {
    static int deepest;

    /**
     * Counts climbs to step n by memoized recursion.
     * Time: O(n + b). Space: O(n) cache plus O(n) call stack.
     * Invariant: memo[i] is -1 or the number of ways to land exactly on step i.
     */
    static long waysMemo(int n, int[] broken) {
        // The marker array turns the broken list into constant-time lookups.
        boolean[] isBroken = new boolean[n + 1];
        for (int b : broken) isBroken[b] = true;
        // The marker -1 separates "not computed" from a real answer of 0.
        long[] memo = new long[n + 1];
        Arrays.fill(memo, -1);
        deepest = 0;
        return from(n, 1, isBroken, memo);
    }

    private static long from(int i, int depth, boolean[] isBroken, long[] memo) {
        // The depth is recorded to compare the stack against the table.
        deepest = Math.max(deepest, depth);
        // A broken step cannot be landed on, so no sequence ends there.
        if (isBroken[i]) return 0;
        // The ground has exactly one way, the empty sequence.
        if (i == 0) return 1;
        // A completed answer is reused.
        if (memo[i] != -1) return memo[i];
        // The last move is a 1-step, and a 2-step exists only from step i - 2 >= 0.
        long total = from(i - 1, depth + 1, isBroken, memo);
        if (i >= 2) total += from(i - 2, depth + 1, isBroken, memo);
        memo[i] = total;
        return total;
    }

    /**
     * Counts climbs to step n by filling a table upward.
     * Time: O(n + b). Space: O(n).
     * Invariant: ways[i] is the number of ways to land exactly on step i.
     */
    static long waysTable(int n, int[] broken) {
        boolean[] isBroken = new boolean[n + 1];
        for (int b : broken) isBroken[b] = true;
        long[] ways = new long[n + 1];
        // The ground has one way, and step 0 is never broken.
        ways[0] = 1;
        // Index i reads smaller indexes only, so the loop runs upward.
        for (int i = 1; i <= n; i++) {
            // A broken step keeps the default 0.
            if (isBroken[i]) continue;
            ways[i] = ways[i - 1] + (i >= 2 ? ways[i - 2] : 0);
        }
        return ways[n];
    }

    /** Oracle: exhaustive enumeration of move sequences, with the broken set checked at every landing. */
    static long oracle(int n, Set<Integer> broken, int at) {
        if (at == n) return 1;
        long total = 0;
        for (int move = 1; move <= 2; move++) {
            int next = at + move;
            if (next <= n && !broken.contains(next)) total += oracle(n, broken, next);
        }
        return total;
    }

    public static void main(String[] args) {
        // The two examples of the exercise, with a mutation check on the input.
        int[] b1 = {3};
        int[] b1Copy = b1.clone();
        if (waysMemo(5, b1) != 2 || waysTable(5, b1) != 2) throw new AssertionError("ex1");
        if (!Arrays.equals(b1, b1Copy)) throw new AssertionError("input changed");
        if (waysMemo(3, new int[] {3}) != 0 || waysTable(3, new int[] {3}) != 0) throw new AssertionError("ex2");
        // Boundary: zero steps, and the largest allowed size without any broken step.
        if (waysMemo(0, new int[0]) != 1 || waysTable(0, new int[0]) != 1) throw new AssertionError("zero");
        if (waysMemo(60, new int[0]) != 2504730781961L) throw new AssertionError("largest");
        // The memoized recursion holds n + 1 calls at once when nothing is broken, while the table holds none.
        if (deepest != 61) throw new AssertionError("depth " + deepest);
        // Random staircases: both forms match each other and the exhaustive search.
        Random rnd = new Random(2608);
        for (int t = 0; t < 3000; t++) {
            int n = rnd.nextInt(16);
            List<Integer> list = new ArrayList<>();
            for (int s = 1; s <= n; s++) if (rnd.nextInt(4) == 0) list.add(s);
            int[] broken = list.stream().mapToInt(Integer::intValue).toArray();
            long expected = oracle(n, new HashSet<>(list), 0);
            if (waysMemo(n, broken) != expected) throw new AssertionError("memo " + n + " " + list);
            if (waysTable(n, broken) != expected) throw new AssertionError("table " + n + " " + list);
        }
    }
}
```
