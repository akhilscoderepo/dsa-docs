<!-- solutions-for: 09-sieve -->
### Solutions For Sieve

#### Solution: [Build] Primes Through N (Author exercise)
<!-- id: bt09-primes-through-n -->

**Approach.** The solution keeps a flag per number and crosses out the multiples of each prime.

The outer loop visits `p` from 2 while `p * p <= n`. A flag that is still false at `p` means no smaller prime divides `p`, so `p` is prime. The inner loop then marks `p * p`, `p * p + p` and so on up to `n`. The invariant is that when the loop for `p` ends, every composite up to `n` whose smallest prime factor is at most `p` is marked. Multiples of `p` below `p * p` have a smaller prime factor and carry a mark already. A final scan from 2 collects the unmarked numbers in increasing order. An `n` below 2 gives an empty scan, so the empty array follows without a special case.

**Complexity.**

- **Time** is O(n log log n), because prime `p` writes about `n / p` flags and those counts add up to that bound.
- **Space** is O(n) for the flag array of `n + 1` booleans, plus the result array.

```java run
import java.util.Random;

public final class PrimesThroughN {
    /**
     * Returns all primes from 2 to n in increasing order.
     * Time: O(n log log n), one write per marked multiple plus one scan.
     * Space: O(n), one boolean per number.
     * Invariant: after the loop for p, every composite with smallest prime factor at most p is marked.
     */
    static int[] primesThrough(int n) {
        // Two slots at least, so indexes 0 and 1 exist even for tiny n.
        boolean[] composite = new boolean[Math.max(n + 1, 2)];
        // The square condition is computed in long, so p * p cannot wrap.
        for (int p = 2; (long) p * p <= n; p++) {
            // A marked number has a smaller prime factor, so it starts no loop.
            if (composite[p]) continue;
            // Multiples below p * p were marked by smaller primes.
            for (long m = (long) p * p; m <= n; m += p) {
                // This write is the only cost of the inner loop.
                composite[(int) m] = true;
            }
        }
        // First pass counts the unmarked numbers from 2 upward.
        int count = 0;
        for (int x = 2; x <= n; x++) if (!composite[x]) count++;
        // The result array has exactly one slot per prime.
        int[] out = new int[count];
        int k = 0;
        // Second pass copies the primes in increasing order.
        for (int x = 2; x <= n; x++) if (!composite[x]) out[k++] = x;
        return out;
    }

    /** Oracle that tests each number by trial division over every smaller value. */
    static int[] oracle(int n) {
        int count = 0;
        int[] buf = new int[Math.max(n + 1, 0)];
        for (int x = 2; x <= n; x++) {
            boolean prime = true;
            for (int d = 2; d < x; d++) if (x % d == 0) { prime = false; break; }
            if (prime) buf[count++] = x;
        }
        return java.util.Arrays.copyOf(buf, count);
    }

    public static void main(String[] args) {
        // Example 1 and Example 2 from the exercise text.
        if (!java.util.Arrays.equals(primesThrough(30), new int[]{2, 3, 5, 7, 11, 13, 17, 19, 23, 29})) throw new AssertionError("example 1");
        if (!java.util.Arrays.equals(primesThrough(2), new int[]{2})) throw new AssertionError("example 2a");
        if (primesThrough(1).length != 0 || primesThrough(0).length != 0) throw new AssertionError("example 2b");
        // The prime count up to one million is a known constant.
        if (primesThrough(1_000_000).length != 78498) throw new AssertionError("count to 10^6");
        // Every n from 0 to 300 matches the trial-division oracle.
        for (int n = 0; n <= 300; n++) {
            if (!java.util.Arrays.equals(primesThrough(n), oracle(n))) throw new AssertionError("n " + n);
        }
        // Random larger bounds with a fixed seed.
        Random rnd = new Random(3009);
        for (int round = 0; round < 40; round++) {
            int n = 300 + rnd.nextInt(3000);
            if (!java.util.Arrays.equals(primesThrough(n), oracle(n))) throw new AssertionError("random " + n);
        }
    }
}
```

#### Solution: [Vary] Count Primes (LeetCode 204)
<!-- id: bt09-count-primes-below -->

**Approach.** The solution runs the same marking loop for the bound `n - 1` and reads two values in the final scan.

The target primes are strictly smaller than `n`, so the flag array covers the numbers up to `n - 1`. The scan counts the unmarked numbers from 2 up to `n - 1`, and it remembers the last unmarked one. That last number is the largest prime below `n`. When no prime exists, which happens for `n <= 2`, the count stays 0 and the remembered value keeps its start value -1. The array is sized for at least two slots, so a bound of 0 or 1 never indexes outside it.

**Complexity.**

- **Time** is O(n log log n), as in the previous exercise, because only the bound changes by one.
- **Space** is O(n), for one boolean per number below `n`.

```java run
import java.util.Random;

public final class CountPrimesBelow {
    /**
     * Returns {count, largest} for the primes strictly below n, with largest = -1 when none exist.
     * Time: O(n log log n), marking plus one scan.
     * Space: O(n), one boolean per number.
     * Invariant: after the loop for p, every composite below n with smallest prime factor at most p is marked.
     */
    static int[] countBelow(int n) {
        // The last candidate is n - 1, and two slots at least keep tiny bounds safe.
        int top = n - 1;
        boolean[] composite = new boolean[Math.max(top + 1, 2)];
        // Loop for p while the square stays inside the range, using long for the product.
        for (int p = 2; (long) p * p <= top; p++) {
            // A marked p is composite and starts no loop.
            if (composite[p]) continue;
            // Start at the square, because smaller multiples were marked already.
            for (long m = (long) p * p; m <= top; m += p) composite[(int) m] = true;
        }
        int count = 0, largest = -1;
        // One scan counts primes and keeps the latest one, which is the largest.
        for (int x = 2; x <= top; x++) {
            if (!composite[x]) { count++; largest = x; }
        }
        return new int[]{count, largest};
    }

    /** Oracle that trial-divides every candidate below n. */
    static int[] oracle(int n) {
        int count = 0, largest = -1;
        for (int x = 2; x < n; x++) {
            boolean prime = true;
            for (int d = 2; d * d <= x; d++) if (x % d == 0) { prime = false; break; }
            if (prime) { count++; largest = x; }
        }
        return new int[]{count, largest};
    }

    public static void main(String[] args) {
        // Example 1 and Example 2 from the exercise text.
        if (!java.util.Arrays.equals(countBelow(10), new int[]{4, 7})) throw new AssertionError("example 1");
        if (!java.util.Arrays.equals(countBelow(2), new int[]{0, -1})) throw new AssertionError("example 2");
        // Bounds 0 and 1 have no primes.
        if (!java.util.Arrays.equals(countBelow(0), new int[]{0, -1})) throw new AssertionError("zero");
        if (!java.util.Arrays.equals(countBelow(1), new int[]{0, -1})) throw new AssertionError("one");
        // A prime bound itself must stay out of the count.
        if (!java.util.Arrays.equals(countBelow(13), new int[]{5, 11})) throw new AssertionError("prime bound");
        // Every bound from 0 to 400 matches the oracle.
        for (int n = 0; n <= 400; n++) {
            if (!java.util.Arrays.equals(countBelow(n), oracle(n))) throw new AssertionError("n " + n);
        }
        // Random larger bounds with a fixed seed.
        Random rnd = new Random(3010);
        for (int round = 0; round < 50; round++) {
            int n = rnd.nextInt(200_000);
            if (!java.util.Arrays.equals(countBelow(n), oracle(n))) throw new AssertionError("random " + n);
        }
    }
}
```

#### Solution: [Boundary] Zero One And p-Squared Overflow (Author exercise)
<!-- id: bt09-square-overflow -->

**Approach.** The solution marks composites only inside the window, using marker primes up to the square root of `hi`.

A first sieve finds the primes up to 46,341, which is enough for every `hi` that fits in an `int`. For each marker prime `p` with `p * p <= hi`, the window loop starts at the larger of `p * p` and the first multiple of `p` that is at least `lo`. Starting at `p * p` keeps `p` itself unmarked when `p` lies in the window. All arithmetic on squares and starts uses `long`. With `int`, the product `46341 * 46341` wraps to a negative number, the test `p * p <= hi` succeeds again, and a loop that should stop keeps running. The final scan counts unmarked numbers from `max(lo, 2)`, so 0 and 1 never count. The invariant is that after the loop for `p`, every composite in the window with a prime factor at most `p` is marked.

**Complexity.**

- **Time** is O(sqrt(hi) log log hi + w log log w), where `w = hi - lo + 1`, because the marker sieve and the window marking each follow the sieve cost.
- **Space** is O(sqrt(hi) + w), for the marker flags and the window flags.

```java run
import java.util.Random;

public final class SquareOverflow {
    /**
     * Counts primes in the closed window lo..hi, where hi may equal Integer.MAX_VALUE.
     * Time: O(sqrt(hi) log log hi + w log log w) for window size w.
     * Space: O(sqrt(hi) + w).
     * Invariant: after the loop for p, every composite in the window with a prime factor at most p is marked.
     */
    static int countWindow(int lo, int hi) {
        // The window has hi - lo + 1 numbers, computed in long to stay safe.
        int size = (int) ((long) hi - lo + 1);
        boolean[] gone = new boolean[size];
        // Marker primes must reach 46,341 because 46,341 squared exceeds Integer.MAX_VALUE.
        int limit = 46_341;
        boolean[] composite = new boolean[limit + 1];
        // Each marker p is processed in increasing order, with the square held in long.
        for (int p = 2; p <= limit; p++) {
            if (composite[p]) continue;
            // Mark composites among the markers themselves with the usual loop.
            for (long m = (long) p * p; m <= limit; m += p) composite[(int) m] = true;
            long square = (long) p * p;
            // A square above hi ends the work, and the wrapped int value would not.
            if (square > hi) continue;
            // First multiple of p that is at least lo, then lifted to the square if smaller.
            long start = ((lo + (long) p - 1) / p) * p;
            if (start < square) start = square;
            // Marking cost is about size / p writes for this marker.
            for (long m = start; m <= hi; m += p) gone[(int) (m - lo)] = true;
        }
        int count = 0;
        // Numbers 0 and 1 are skipped, so a window that begins at 0 stays correct.
        for (long x = Math.max(lo, 2); x <= hi; x++) if (!gone[(int) (x - lo)]) count++;
        return count;
    }

    /** Oracle that trial-divides each window number with long arithmetic. */
    static int oracle(int lo, int hi) {
        int count = 0;
        for (long x = Math.max(lo, 2); x <= hi; x++) {
            boolean prime = true;
            for (long d = 2; d * d <= x; d++) if (x % d == 0) { prime = false; break; }
            if (prime) count++;
        }
        return count;
    }

    public static void main(String[] args) {
        // Example 1: zero and one are not prime.
        if (countWindow(0, 1) != 0) throw new AssertionError("example 1");
        // Example 2: the window ending at Integer.MAX_VALUE, checked against the oracle and the known count.
        if (countWindow(2147483600, 2147483647) != 2) throw new AssertionError("example 2");
        if (countWindow(2147483600, 2147483647) != oracle(2147483600, 2147483647)) throw new AssertionError("example 2 oracle");
        // A single-number window on the largest int, which is prime.
        if (countWindow(Integer.MAX_VALUE, Integer.MAX_VALUE) != 1) throw new AssertionError("max value");
        // Small windows including 0, 1 and 2 as the first values.
        if (countWindow(2, 2) != 1 || countWindow(1, 1) != 0 || countWindow(0, 2) != 1) throw new AssertionError("small");
        // Random windows with a fixed seed, near zero and near the top of the range.
        Random rnd = new Random(3011);
        for (int round = 0; round < 300; round++) {
            int lo = rnd.nextInt(400);
            int hi = lo + rnd.nextInt(400);
            if (countWindow(lo, hi) != oracle(lo, hi)) throw new AssertionError("low " + lo + " " + hi);
        }
        for (int round = 0; round < 12; round++) {
            int hi = Integer.MAX_VALUE - rnd.nextInt(5000);
            int lo = hi - rnd.nextInt(3000);
            if (countWindow(lo, hi) != oracle(lo, hi)) throw new AssertionError("high " + lo + " " + hi);
        }
    }
}
```

#### Solution: [Recognize] Smallest Prime Factor Sieve (Author exercise)
<!-- id: bt09-prime-factor-queries -->

**Approach.** The solution builds the smallest-prime-factor table once and splits each query by repeated division.

The table uses the sieve loop with one change. A write at multiple `m` stores `p` only if `spf[m]` is still 0, so the first prime that reaches `m` keeps it, and that prime is the smallest. A prime `p` has `spf[p] = p`, set when the outer scan finds `spf[p]` still 0. For a query `x`, the loop appends `spf[x]` and replaces `x` by `x / spf[x]` until `x` is 1. The factors come out in nondecreasing order, because dividing out the smallest prime leaves a number whose smallest prime factor is at least as large. The invariant is that the product of the collected factors times the current `x` always equals the original query.

**Complexity.**

- **Time** is O(n log log n + q log n), because the table build follows the sieve cost and each query takes at most log2(n) divisions.
- **Space** is O(n) for the `spf` table, plus the output rows.

```java run
import java.util.Random;

public final class PrimeFactorQueries {
    /**
     * Returns the prime factorization of every query in nondecreasing order.
     * Time: O(n log log n + q log n) for table build and q queries.
     * Space: O(n) for the table plus the output.
     * Invariant: product of collected factors times x equals the original query.
     */
    static int[][] factorAll(int n, int[] queries) {
        // spf[x] holds the smallest prime factor of x, or 0 while unvisited.
        int[] spf = new int[n + 1];
        for (int p = 2; p <= n; p++) {
            // A written value means a smaller prime reached p, so p is composite.
            if (spf[p] != 0) continue;
            spf[p] = p;
            // Square start with a long counter so the product cannot wrap.
            for (long m = (long) p * p; m <= n; m += p) {
                // Only the first writer stays, and that is the smallest prime.
                if (spf[(int) m] == 0) spf[(int) m] = p;
            }
        }
        int[][] out = new int[queries.length][];
        // One row per query, filled by repeated division.
        for (int i = 0; i < queries.length; i++) {
            int x = queries[i];
            // At most log2(x) factors exist, so a scratch array of 31 slots is enough.
            int[] scratch = new int[31];
            int size = 0;
            // Each division removes one prime factor and keeps the invariant.
            while (x > 1) {
                scratch[size++] = spf[x];
                x /= spf[x];
            }
            out[i] = java.util.Arrays.copyOf(scratch, size);
        }
        return out;
    }

    /** Oracle that factors by trial division. */
    static int[] oracleOne(int x) {
        int[] scratch = new int[31];
        int size = 0;
        for (int d = 2; x > 1; d++) {
            while (x % d == 0) { scratch[size++] = d; x /= d; }
        }
        return java.util.Arrays.copyOf(scratch, size);
    }

    public static void main(String[] args) {
        // Example 1: a composite, a prime and a number with four factors.
        int[][] r1 = factorAll(100, new int[]{12, 97, 84});
        if (!java.util.Arrays.deepEquals(r1, new int[][]{{2, 2, 3}, {97}, {2, 2, 3, 7}})) throw new AssertionError("example 1");
        // Example 2: a power of two and the smallest prime.
        int[][] r2 = factorAll(100, new int[]{64, 2});
        if (!java.util.Arrays.deepEquals(r2, new int[][]{{2, 2, 2, 2, 2, 2}, {2}})) throw new AssertionError("example 2");
        // Every number up to 2000 matches trial division.
        int[] all = new int[1999];
        for (int i = 0; i < all.length; i++) all[i] = i + 2;
        int[][] got = factorAll(2000, all);
        for (int i = 0; i < all.length; i++) {
            if (!java.util.Arrays.equals(got[i], oracleOne(all[i]))) throw new AssertionError("x " + all[i]);
        }
        // Random bounds and queries with a fixed seed, including a large power of two.
        Random rnd = new Random(3012);
        for (int round = 0; round < 60; round++) {
            int n = 2 + rnd.nextInt(100_000);
            int[] q = new int[20];
            for (int i = 0; i < q.length; i++) q[i] = 2 + rnd.nextInt(n - 1);
            int[][] res = factorAll(n, q);
            for (int i = 0; i < q.length; i++) {
                if (!java.util.Arrays.equals(res[i], oracleOne(q[i]))) throw new AssertionError("random " + q[i]);
            }
        }
        if (factorAll(1_000_000, new int[]{524_288})[0].length != 19) throw new AssertionError("power of two");
    }
}
```
