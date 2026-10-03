<!-- solutions-for: 07-difference-arrays -->
### Difference Arrays

#### Solution: [Build] One Range Add (Author exercise)
<!-- id: ps-one-range-add -->

**Approach.** The array of totals steps up by the amount at `left` and steps back down just after `right`, so a difference array with `n + 1` slots records the update as `diff[left] += amount` and `diff[right + 1] -= amount`. A running sum over the first `n` slots rebuilds the totals: the running sum is the amount inside the stretch and zero outside it. The extra slot receives the cancelling note when the stretch ends at the last position and is never read. The oracle adds the amount to each position of the stretch directly.

**Complexity.** Two writes and one scan, so O(n) time and n + 1 slots of space.

```java run
import java.util.Arrays;
import java.util.Random;

public final class OneRangeAdd {
    static long[] rangeAdd(int n, int left, int right, long amount) {
        long[] diff = new long[n + 1];
        diff[left] += amount;
        diff[right + 1] -= amount;
        long[] out = new long[n];
        long running = 0;
        for (int p = 0; p < n; p++) {
            running += diff[p];
            out[p] = running;
        }
        return out;
    }
    static long[] oracle(int n, int left, int right, long amount) {
        long[] out = new long[n];
        for (int p = left; p <= right; p++) out[p] += amount;
        return out;
    }

    public static void main(String[] args) {
        if (!Arrays.equals(rangeAdd(5, 0, 2, 3), new long[] {3, 3, 3, 0, 0})) throw new AssertionError("example 1");
        if (!Arrays.equals(rangeAdd(6, 1, 3, 5), new long[] {0, 5, 5, 5, 0, 0})) throw new AssertionError("example 2");
        if (!Arrays.equals(rangeAdd(2, 0, 1, -4), new long[] {-4, -4})) throw new AssertionError("negative amount over everything");
        Random rnd = new Random(7801);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(10);
            int l = rnd.nextInt(n), r = l + rnd.nextInt(n - l);
            long v = rnd.nextInt(2000000001) - 1000000000;
            if (!Arrays.equals(rangeAdd(n, l, r, v), oracle(n, l, r, v))) throw new AssertionError("differs for " + l + "," + r);
        }
    }
}
```

#### Solution: [Vary] Corporate Flight Bookings (LeetCode 1109)
<!-- id: ps-flight-bookings -->

**Approach.** Each booking is a range update on the seats of the flights from `first` through `last`. Flights are numbered from one, so the start note goes to slot `first - 1` and the cancelling note, for the flight after `last`, goes to slot `last`, which is the zero-based index of that next flight and may equal `n`. A difference array of `n + 1` slots holds all the notes, and one running sum produces the seats of every flight. The oracle adds each booking to every flight it covers.

**Complexity.** O(bookings + n) time and n + 1 slots of space.

```java run
import java.util.Arrays;
import java.util.Random;

public final class FlightBookings {
    static int[] corpFlightBookings(int[][] bookings, int n) {
        int[] diff = new int[n + 1];
        for (int[] b : bookings) {
            diff[b[0] - 1] += b[2];
            diff[b[1]] -= b[2];
        }
        int[] seats = new int[n];
        int running = 0;
        for (int i = 0; i < n; i++) {
            running += diff[i];
            seats[i] = running;
        }
        return seats;
    }
    static int[] oracle(int[][] bookings, int n) {
        int[] seats = new int[n];
        for (int[] b : bookings)
            for (int f = b[0]; f <= b[1]; f++) seats[f - 1] += b[2];
        return seats;
    }

    public static void main(String[] args) {
        int[][] ex1 = {{1, 3, 5}, {2, 4, 3}, {3, 5, 2}};
        if (!Arrays.equals(corpFlightBookings(ex1, 5), new int[] {5, 8, 10, 5, 2})) throw new AssertionError("example 1");
        if (!Arrays.equals(corpFlightBookings(new int[][] {{1, 1, 7}}, 2), new int[] {7, 0})) throw new AssertionError("example 2");
        if (!Arrays.equals(corpFlightBookings(new int[][] {{1, 2, 4}}, 2), new int[] {4, 4})) throw new AssertionError("booking to the last flight");
        Random rnd = new Random(7802);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(10);
            int m = 1 + rnd.nextInt(6);
            int[][] bk = new int[m][3];
            for (int i = 0; i < m; i++) {
                int f = 1 + rnd.nextInt(n), l = f + rnd.nextInt(n - f + 1);
                bk[i] = new int[] {f, l, 1 + rnd.nextInt(20)};
            }
            if (!Arrays.equals(corpFlightBookings(bk, n), oracle(bk, n))) throw new AssertionError("differs for n=" + n);
        }
    }
}
```

#### Solution: [Boundary] Final Endpoint (Author exercise)
<!-- id: ps-final-endpoint -->

**Approach.** When a stretch ends at position `n - 1`, the cancelling note belongs to position `n`, one past the end of the data. A difference array of length `n` makes that write throw, while an array of length `n + 1` accepts it, and the extra slot is never read by the scan over the first `n` positions. A guard that skips the write when `right + 1` equals `n` is equally correct, since there is no position after the end to cancel the amount on. The program shows the throwing version, then both fixes, and compares them with an oracle on random updates, including ones that end at the last position and arrays of length one.

**Complexity.** O(updates + n) time, with either one extra slot or a guard.

```java run
import java.util.Arrays;
import java.util.Random;

public final class FinalEndpoint {
    static long[] withSentinel(int n, int[][] updates) {
        long[] diff = new long[n + 1];
        for (int[] u : updates) { diff[u[0]] += u[2]; diff[u[1] + 1] -= u[2]; }
        return scan(diff, n);
    }
    static long[] withGuard(int n, int[][] updates) {
        long[] diff = new long[n];
        for (int[] u : updates) {
            diff[u[0]] += u[2];
            if (u[1] + 1 < n) diff[u[1] + 1] -= u[2];
        }
        return scan(diff, n);
    }
    static long[] tooShort(int n, int[][] updates) {
        long[] diff = new long[n];
        for (int[] u : updates) { diff[u[0]] += u[2]; diff[u[1] + 1] -= u[2]; }
        return scan(diff, n);
    }
    static long[] scan(long[] diff, int n) {
        long[] out = new long[n];
        long running = 0;
        for (int p = 0; p < n; p++) { running += diff[p]; out[p] = running; }
        return out;
    }
    static long[] oracle(int n, int[][] updates) {
        long[] out = new long[n];
        for (int[] u : updates) for (int p = u[0]; p <= u[1]; p++) out[p] += u[2];
        return out;
    }

    public static void main(String[] args) {
        int[][] one = {{0, 2, 2}};
        if (!Arrays.equals(withSentinel(3, one), new long[] {2, 2, 2})) throw new AssertionError("example 1 sentinel");
        if (!Arrays.equals(withGuard(3, one), new long[] {2, 2, 2})) throw new AssertionError("example 1 guard");
        int[][] two = {{0, 0, 9}};
        if (!Arrays.equals(withSentinel(1, two), new long[] {9}) || !Arrays.equals(withGuard(1, two), new long[] {9})) throw new AssertionError("example 2");
        boolean threw = false;
        try { tooShort(3, one); } catch (ArrayIndexOutOfBoundsException e) { threw = true; }
        if (!threw) throw new AssertionError("an array of length n should throw at index n");
        Random rnd = new Random(7803);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(8);
            int m = 1 + rnd.nextInt(5);
            int[][] up = new int[m][3];
            for (int i = 0; i < m; i++) {
                int l = rnd.nextInt(n), r = rnd.nextBoolean() ? n - 1 : l + rnd.nextInt(n - l);
                up[i] = new int[] {l, Math.max(l, r), rnd.nextInt(21) - 10};
            }
            long[] want = oracle(n, up);
            if (!Arrays.equals(withSentinel(n, up), want)) throw new AssertionError("sentinel differs");
            if (!Arrays.equals(withGuard(n, up), want)) throw new AssertionError("guard differs");
        }
    }
}
```

#### Solution: [Recognize] Car Pooling (LeetCode 1094)
<!-- id: ps-car-pooling -->

**Approach.** The number of passengers on board changes only at pick-up and drop-off positions. A difference array indexed by position records plus the passengers at `from` and minus them at `to`, and since people leave at `to` before the next boarding at the same position matters, the running sum at a position already reflects both. Scanning the positions in order with a running sum gives the load at each position, and the answer is false as soon as the load exceeds the capacity. Positions are bounded by 1000, so the array has 1002 slots. The oracle simulates the load at every position by adding each trip's passengers to the positions from `from` up to, but not including, `to`.

**Complexity.** O(trips + 1000) time and a constant-size array.

```java run
import java.util.Random;

public final class CarPooling {
    static boolean carPooling(int[][] trips, int capacity) {
        int[] diff = new int[1002];
        for (int[] t : trips) {
            diff[t[1]] += t[0];
            diff[t[2]] -= t[0];
        }
        int onBoard = 0;
        for (int d : diff) {
            onBoard += d;
            if (onBoard > capacity) return false;
        }
        return true;
    }
    static boolean oracle(int[][] trips, int capacity) {
        for (int pos = 0; pos <= 1000; pos++) {
            int load = 0;
            for (int[] t : trips) if (t[1] <= pos && pos < t[2]) load += t[0];
            if (load > capacity) return false;
        }
        return true;
    }

    public static void main(String[] args) {
        if (carPooling(new int[][] {{2, 1, 5}, {3, 3, 7}}, 4)) throw new AssertionError("example 1");
        if (!carPooling(new int[][] {{4, 0, 3}, {4, 3, 6}}, 4)) throw new AssertionError("example 2");
        if (!carPooling(new int[][] {{2, 1, 5}, {3, 3, 7}}, 5)) throw new AssertionError("exactly full is allowed");
        Random rnd = new Random(7804);
        for (int t = 0; t < 4000; t++) {
            int m = 1 + rnd.nextInt(5);
            int[][] trips = new int[m][3];
            for (int i = 0; i < m; i++) {
                int from = rnd.nextInt(20), to = from + 1 + rnd.nextInt(20);
                trips[i] = new int[] {1 + rnd.nextInt(5), from, to};
            }
            int cap = 1 + rnd.nextInt(12);
            if (carPooling(trips, cap) != oracle(trips, cap)) throw new AssertionError("differs for capacity " + cap);
        }
    }
}
```
