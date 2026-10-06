<!-- solutions-for: 04-expired-front-eviction -->
### Solutions For The Expiry Exercises

#### Solution: [Build] Expire One Window (Author exercise)
<!-- id: dq-expire-one -->

**Approach.**

The positions in the deque increase from the front to the back, so the oldest position is the first one. The method removes from the front while the front is smaller than the left bound, and it stops at the first position that is legal. Every later position is larger, so it is legal too. The invariant is that the returned deque is the longest suffix of the input that stays at or above the left bound. The assertions compare the result with a filter that keeps every position at or above the bound.

**Complexity.**

- **Time** is O(r) for r removed entries, plus O(1) for the final check.
- **Space** is O(n) for the copy of the deque that the method returns.

```java run
import java.util.*;

public final class ExpireOne {
    /**
     * Removes positions below leftBound from the front and returns the rest.
     * Time: O(r) for r removals. Space: O(n) for the returned copy.
     * Invariant: the result is the suffix of positions at or above leftBound.
     */
    static int[] expire(int[] positions, int leftBound) {
        Deque<Integer> d = new ArrayDeque<>();
        for (int p : positions) d.addLast(p);
        while (!d.isEmpty() && d.peekFirst() < leftBound) {   // the front is the oldest position
            d.pollFirst();                                    // an expired position leaves for good
        }
        int[] out = new int[d.size()];
        int i = 0;
        for (int p : d) out[i++] = p;
        return out;
    }

    public static void main(String[] args) {
        // Worked examples.
        if (!Arrays.equals(expire(new int[]{2, 4}, 3), new int[]{4})) throw new AssertionError("example 1");
        if (!Arrays.equals(expire(new int[]{3, 4, 5}, 3), new int[]{3, 4, 5})) throw new AssertionError("example 2");
        // Empty deque and a bound above every position.
        if (expire(new int[0], 5).length != 0) throw new AssertionError("empty");
        if (expire(new int[]{1, 2}, 9).length != 0) throw new AssertionError("all expired");
        // Random sorted position lists agree with a filter.
        Random rnd = new Random(10);
        for (int t = 0; t < 3000; t++) {
            int n = rnd.nextInt(12);
            int[] ps = new int[n];
            int cur = rnd.nextInt(3);
            for (int i = 0; i < n; i++) { ps[i] = cur; cur += 1 + rnd.nextInt(3); }
            int bound = rnd.nextInt(30);
            int[] want = Arrays.stream(ps).filter(p -> p >= bound).toArray();
            if (!Arrays.equals(expire(ps, bound), want)) throw new AssertionError("filter " + Arrays.toString(ps));
        }
    }
}
```

#### Solution: [Vary] Jumping Boundary (Author exercise)
<!-- id: dq-jumping-boundary -->

**Approach.**

The method appends position `r` on step `r`. It then removes from the front while the front is below the supplied bound for that step, and it records the new front. A loop is needed because the bound can jump over several stored positions at once. The invariant after each step is that the front is the oldest position at or above the bound. The assertions compare the recorded front with the bound itself, because with every position stored the oldest legal position is the bound.

**Complexity.**

- **Time** is O(n), because each position is appended once and expired at most once.
- **Space** is O(n), for the deque and the output array.

```java run
import java.util.*;

public final class JumpingBoundary {
    /**
     * Returns the oldest legal position after each step, given a non-decreasing bound per step.
     * Time: O(n) amortized. Space: O(n). Invariant: the front is at or above the bound.
     */
    static int[] oldestLegal(int[] bound) {
        Deque<Integer> d = new ArrayDeque<>();
        int[] out = new int[bound.length];
        for (int r = 0; r < bound.length; r++) {                  // one step per position
            d.addLast(r);                                         // the new position enters at the back
            while (d.peekFirst() < bound[r]) d.pollFirst();       // a loop, because a jump can expire many
            out[r] = d.peekFirst();                               // the position r itself is always legal
        }
        return out;
    }

    public static void main(String[] args) {
        // Worked examples.
        if (!Arrays.equals(oldestLegal(new int[]{0, 0, 1, 3, 3, 5}), new int[]{0, 0, 1, 3, 3, 5})) throw new AssertionError("example 1");
        if (!Arrays.equals(oldestLegal(new int[]{0, 0, 0}), new int[]{0, 0, 0})) throw new AssertionError("example 2");
        // Empty input.
        if (oldestLegal(new int[0]).length != 0) throw new AssertionError("empty");
        // Random non-decreasing bounds with bound[r] <= r: the oldest legal position is the bound.
        Random rnd = new Random(11);
        for (int t = 0; t < 3000; t++) {
            int n = rnd.nextInt(20);
            int[] b = new int[n];
            int cur = 0;
            for (int r = 0; r < n; r++) { cur = Math.min(r, cur + rnd.nextInt(3)); b[r] = cur; }
            if (!Arrays.equals(oldestLegal(b), b)) throw new AssertionError("random " + Arrays.toString(b));
        }
    }
}
```

#### Solution: [Boundary] Exact Expiry Point (Author exercise)
<!-- id: dq-exact-expiry -->

**Approach.**

A range of length `k` ending at `right` holds the positions `right - k + 1` through `right`. The position `right - k` is the first one outside it, so the age test removes the front when it is at most `right - k`. The method stores every position, applies that test and records the front. The invariant is that the front equals `max(0, right - k + 1)`. The assertions check that formula on random sizes, and they check a range of length 1, where the test removes the previous position every step.

**Complexity.**

- **Time** is O(n), because each position is appended once and removed at most once.
- **Space** is O(k), because the deque never holds more than `k` positions after the age test.

```java run
import java.util.*;

public final class ExactExpiry {
    /**
     * Returns the oldest position still in the range ending at each right end.
     * Time: O(n) amortized. Space: O(k). Invariant: the front is max(0, right - k + 1).
     */
    static int[] oldest(int n, int k) {
        Deque<Integer> d = new ArrayDeque<>();
        int[] out = new int[n];
        for (int right = 0; right < n; right++) {          // one step per right end
            d.addLast(right);                              // the new position enters at the back
            if (d.peekFirst() <= right - k) d.pollFirst(); // position right - k is the first one outside
            out[right] = d.peekFirst();                    // the front is the oldest legal position
        }
        return out;
    }

    public static void main(String[] args) {
        // Worked examples.
        if (!Arrays.equals(oldest(5, 3), new int[]{0, 0, 0, 1, 2})) throw new AssertionError("example 1");
        if (!Arrays.equals(oldest(3, 1), new int[]{0, 1, 2})) throw new AssertionError("example 2");
        // Empty input.
        if (oldest(0, 4).length != 0) throw new AssertionError("empty");
        // Random sizes agree with the closed form.
        Random rnd = new Random(12);
        for (int t = 0; t < 2000; t++) {
            int n = rnd.nextInt(30), k = 1 + rnd.nextInt(8);
            int[] got = oldest(n, k);
            for (int r = 0; r < n; r++) if (got[r] != Math.max(0, r - k + 1)) throw new AssertionError("n=" + n + " k=" + k + " r=" + r);
        }
    }
}
```

#### Solution: [Recognize] Chronological Candidate Queue (Author exercise)
<!-- id: dq-chronological-queue -->

**Approach.**

A valid state has three properties. The positions strictly increase from the front to the back. Every position lies in the range from `right - k + 1` through `right`. The values at those positions never increase. The method checks each property in one pass and returns `false` at the first violation. The invariant is the full state rule of the sliding-range deque. The assertions try a valid state, an unordered state, an expired state, a state with a position beyond `right` and a state with rising values.

**Complexity.**

- **Time** is O(m) for m stored positions, because the pass reads each entry once.
- **Space** is O(1), because the pass keeps only the previous position.

```java run
public final class ChronologicalQueue {
    /**
     * Returns true when the stored positions form a legal deque state for the range ending at right.
     * Time: O(m). Space: O(1).
     * Invariant: positions increase, lie in the range, and the values never increase.
     */
    static boolean valid(int[] a, int k, int right, int[] stored) {
        for (int i = 0; i < stored.length; i++) {                       // one check per stored position
            if (stored[i] <= right - k || stored[i] > right) return false;   // outside the range
            if (i > 0 && stored[i] <= stored[i - 1]) return false;      // positions must increase
            if (i > 0 && a[stored[i]] > a[stored[i - 1]]) return false; // values must not increase
        }
        return true;
    }

    public static void main(String[] args) {
        int[] a = {4, 2, 12, 3, 8, 1};
        // Worked examples.
        if (!valid(a, 3, 4, new int[]{2, 4})) throw new AssertionError("example 1");
        if (valid(a, 3, 4, new int[]{1, 2})) throw new AssertionError("example 2");
        // Empty state is valid.
        if (!valid(a, 3, 4, new int[0])) throw new AssertionError("empty");
        // Expired position, unordered positions, a future position, rising values.
        if (valid(a, 3, 5, new int[]{2, 4})) throw new AssertionError("position 2 is expired at right 5");
        if (valid(a, 3, 4, new int[]{4, 2})) throw new AssertionError("positions must increase");
        if (valid(a, 3, 4, new int[]{4, 5})) throw new AssertionError("position 5 is beyond right");
        if (valid(a, 3, 3, new int[]{1, 2})) throw new AssertionError("values rise from 2 to 12");
    }
}
```
