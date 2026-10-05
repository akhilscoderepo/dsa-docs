<!-- solutions-for: 07-prefix-sums-and-difference-arrays -->
### Solutions For Range Updates

#### Solution: [Build] One Range Add (Author exercise)
<!-- id: ps-one-range-add -->

**Approach.**
The delta array has `n + 1` slots. The update writes `+value` at `left` and `-value` at `right + 1`. A running sum over the first `n` slots then gives `value` for the indexes `left` through `right` and 0 elsewhere. The second write cancels the first from `right + 1` onward. The invariant is that the total at index `i` equals the sum of the deltas at indexes 0 through `i`.

**Complexity.**
- **Time** is O(n), because the update costs O(1) and the final pass visits each index once.
- **Space** is O(n) for the delta array and the result.

```java run
import java.util.Arrays;
import java.util.Random;

public final class OneRangeAdd {
    /**
     * Returns the array with value on left..right and 0 elsewhere.
     * Time: O(n), two writes and one pass.
     * Space: O(n) for the deltas and the result.
     * Invariant: total[i] equals the sum of diff[0..i].
     */
    static long[] rangeAdd(int n, int left, int right, int value) {
        // The extra slot at index n absorbs the write when right is n - 1.
        long[] diff = new long[n + 1];
        // The value starts at left, and its cancellation starts after right.
        diff[left] += value;
        diff[right + 1] -= value;
        long[] total = new long[n];
        long cur = 0;
        for (int i = 0; i < n; i++) {
            // The running sum spreads each delta over all later indexes.
            cur += diff[i];
            total[i] = cur;
        }
        return total;
    }

    public static void main(String[] args) {
        // The statement examples.
        if (!Arrays.equals(rangeAdd(5, 1, 3, 7), new long[] {0, 7, 7, 7, 0})) throw new AssertionError("example 1");
        if (!Arrays.equals(rangeAdd(3, 0, 2, -4), new long[] {-4, -4, -4})) throw new AssertionError("example 2");
        // Random ranges against a direct loop.
        Random rnd = new Random(29);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(10);
            int l = rnd.nextInt(n), r = l + rnd.nextInt(n - l);
            int v = rnd.nextInt(2_000_000_001) - 1_000_000_000;
            long[] expect = new long[n];
            for (int i = l; i <= r; i++) expect[i] = v;
            if (!Arrays.equals(rangeAdd(n, l, r, v), expect)) throw new AssertionError("random");
        }
    }
}
```

#### Solution: [Vary] Corporate Flight Bookings (LeetCode 1109)
<!-- id: ps-flight-bookings-1109 -->

**Approach.**
Flights are numbered from 1, and the array index starts at 0. A booking `[first, last, seats]` therefore becomes the range `first - 1` through `last - 1`. Each booking writes `+seats` at `first - 1` and `-seats` at `last`, which is the cancelling index `(last - 1) + 1`. The delta array has `n + 1` slots, so the write for `last = n` is valid. One running sum then gives the seats on every flight, and overlapping bookings add up because every write uses `+=` and `-=`.

**Complexity.**
- **Time** is O(n + m) for `m` bookings, because each booking costs two writes and the final pass costs n additions.
- **Space** is O(n) for the delta array.

```java run
import java.util.Arrays;
import java.util.Random;

public final class FlightBookings1109 {
    /**
     * Returns the reserved seats on each of the n flights.
     * Time: O(n + m), two writes per booking and one pass.
     * Space: O(n) for the delta array.
     * Invariant: answer[i] equals the sum of diff[0..i].
     */
    static int[] corpFlightBookings(int[][] bookings, int n) {
        // The slot at index n takes the cancelling write of a booking that ends at flight n.
        int[] diff = new int[n + 1];
        for (int[] b : bookings) {
            // The flight number minus 1 is the array index.
            diff[b[0] - 1] += b[2];
            // The cancelling write sits at index last, which is (last - 1) + 1.
            diff[b[1]] -= b[2];
        }
        int[] answer = new int[n];
        int cur = 0;
        for (int i = 0; i < n; i++) {
            cur += diff[i];
            answer[i] = cur;
        }
        return answer;
    }

    public static void main(String[] args) {
        // The statement examples.
        if (!Arrays.equals(corpFlightBookings(new int[][] {{1, 3, 5}, {2, 4, 7}, {3, 3, 1}}, 4), new int[] {5, 12, 13, 7})) throw new AssertionError("example 1");
        if (!Arrays.equals(corpFlightBookings(new int[][] {{1, 1, 9}}, 1), new int[] {9})) throw new AssertionError("example 2");
        // Random bookings against a direct loop.
        Random rnd = new Random(30);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(10);
            int[][] bs = new int[rnd.nextInt(6)][];
            int[] expect = new int[n];
            for (int k = 0; k < bs.length; k++) {
                int f = 1 + rnd.nextInt(n), l = f + rnd.nextInt(n - f + 1), s = 1 + rnd.nextInt(10_000);
                bs[k] = new int[] {f, l, s};
                for (int i = f; i <= l; i++) expect[i - 1] += s;
            }
            if (!Arrays.equals(corpFlightBookings(bs, n), expect)) throw new AssertionError("random");
        }
    }
}
```

#### Solution: [Boundary] Final Endpoint (Author exercise)
<!-- id: ps-final-endpoint -->

**Approach.**
An update that ends at `n - 1` writes its cancelling delta to index `n`. The delta array has `n + 1` slots, so the write is valid and needs no guard. The final pass reads only the first `n` slots, so the extra slot never enters a total. The deltas are `long` values, because up to 10^5 updates of size 10^9 can overlap and the total reaches 10^14.

**Complexity.**
- **Time** is O(n + m) for `m` updates, because each update costs two writes and the pass costs n additions.
- **Space** is O(n) for the delta array and the result.

```java run
import java.util.Arrays;
import java.util.Random;

public final class FinalEndpoint {
    /**
     * Returns the totals after all range additions.
     * Time: O(n + m), two writes per update and one pass.
     * Space: O(n) for the deltas and the result.
     * Invariant: total[i] equals the sum of diff[0..i].
     */
    static long[] apply(int n, int[][] updates) {
        // One slot beyond the last index holds the cancelling write of an update that reaches the end.
        long[] diff = new long[n + 1];
        for (int[] u : updates) {
            diff[u[0]] += u[2];
            diff[u[1] + 1] -= u[2];
        }
        long[] total = new long[n];
        long cur = 0;
        // The pass stops before the extra slot.
        for (int i = 0; i < n; i++) {
            cur += diff[i];
            total[i] = cur;
        }
        return total;
    }

    public static void main(String[] args) {
        // The statement examples.
        if (!Arrays.equals(apply(4, new int[][] {{1, 3, 4}}), new long[] {0, 4, 4, 4})) throw new AssertionError("example 1");
        if (!Arrays.equals(apply(4, new int[][] {{0, 0, 3}, {0, 3, 2}}), new long[] {5, 2, 2, 2})) throw new AssertionError("example 2");
        // An array of length n would throw on the cancelling write.
        try {
            int[] tooShort = new int[4];
            tooShort[3 + 1] -= 4;
            throw new AssertionError("expected an out of range write");
        } catch (ArrayIndexOutOfBoundsException expected) {
            // This is the failure that the extra slot prevents.
        }
        // Many large overlapping updates stay exact in long.
        int[][] many = new int[1000][];
        for (int i = 0; i < many.length; i++) many[i] = new int[] {0, 0, 1_000_000_000};
        if (apply(1, many)[0] != 1_000_000_000_000L) throw new AssertionError("long total");
        // Random updates, many of them ending at the last index, against a direct loop.
        Random rnd = new Random(31);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(8);
            int[][] ups = new int[rnd.nextInt(6)][];
            long[] expect = new long[n];
            for (int k = 0; k < ups.length; k++) {
                int l = rnd.nextInt(n), r = rnd.nextBoolean() ? n - 1 : l + rnd.nextInt(n - l);
                int v = rnd.nextInt(2_000_001) - 1_000_000;
                ups[k] = new int[] {l, r, v};
                for (int i = l; i <= r; i++) expect[i] += v;
            }
            if (!Arrays.equals(apply(n, ups), expect)) throw new AssertionError("random");
        }
    }
}
```

#### Solution: [Recognize] Car Pooling (LeetCode 1094)
<!-- id: ps-car-pooling-1094 -->

**Approach.**
A trip occupies seats from position `from` up to but not including position `to`, because the drop at `to` happens before a pickup at the same position. The method writes `+passengers` at `from` and `-passengers` at `to`. A running sum over the positions then gives the number of people in the car after all pickups and drops at each position. A pickup and a drop at one position combine into a single delta, which orders the drop before the pickup. The answer is false as soon as the running sum passes the capacity. Positions go up to 1000, so the delta array has 1001 slots and the index `to` is always valid.

**Complexity.**
- **Time** is O(P + m) for `m` trips and `P = 1001` positions, because each trip costs two writes and the pass visits each position once.
- **Space** is O(P) for the delta array.

```java run
import java.util.Random;

public final class CarPooling1094 {
    /**
     * Returns true when the number of people in the car never exceeds capacity.
     * Time: O(P + m), two writes per trip and one pass over the positions.
     * Space: O(P) for the delta array.
     * Invariant: after reading diff[0..p], cur is the number of people in the car at position p.
     */
    static boolean carPooling(int[][] trips, int capacity) {
        // Positions are at most 1000, so index to is always valid.
        int[] diff = new int[1001];
        for (int[] t : trips) {
            // Passengers board at from and leave at to.
            diff[t[1]] += t[0];
            diff[t[2]] -= t[0];
        }
        int cur = 0;
        for (int p = 0; p < diff.length; p++) {
            // The delta at p already holds the drops that precede the pickups at p.
            cur += diff[p];
            if (cur > capacity) return false;
        }
        return true;
    }

    public static void main(String[] args) {
        // The statement examples.
        if (carPooling(new int[][] {{2, 1, 5}, {3, 3, 7}}, 4)) throw new AssertionError("example 1");
        if (!carPooling(new int[][] {{3, 2, 4}, {3, 4, 6}}, 3)) throw new AssertionError("example 2");
        // A larger capacity makes the first example feasible.
        if (!carPooling(new int[][] {{2, 1, 5}, {3, 3, 7}}, 5)) throw new AssertionError("capacity 5");
        // Random trips against a direct count at every position.
        Random rnd = new Random(32);
        for (int t = 0; t < 3000; t++) {
            int[][] trips = new int[1 + rnd.nextInt(5)][];
            for (int k = 0; k < trips.length; k++) {
                int from = rnd.nextInt(10), to = from + 1 + rnd.nextInt(10);
                trips[k] = new int[] {1 + rnd.nextInt(5), from, to};
            }
            int cap = 1 + rnd.nextInt(10);
            boolean expect = true;
            for (int p = 0; p <= 20; p++) {
                int load = 0;
                for (int[] tr : trips) if (tr[1] <= p && p < tr[2]) load += tr[0];
                if (load > cap) expect = false;
            }
            if (carPooling(trips, cap) != expect) throw new AssertionError("random");
        }
    }
}
```
