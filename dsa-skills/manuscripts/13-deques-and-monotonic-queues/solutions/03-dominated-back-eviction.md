<!-- solutions-for: 03-dominated-back-eviction -->
### Solutions For The Domination Exercises

#### Solution: [Build] Insert Maximum Candidate (Author exercise)
<!-- id: dq-insert-max -->

**Approach.**

The method walks the positions in order. For each position it pops every back entry whose value is strictly smaller, then appends the new position. A popped position has a newer position with at least its value, so it cannot be a future maximum. The invariant is that the stored values never increase from front to back. The assertions compare the result with a quadratic filter that keeps a position when no later value is strictly larger. They also check the boxed-integer claim from the lesson.

**Complexity.**

- **Time** is O(n), since the loop appends position `i` once and the inner loop pops each position at most one time.
- **Space** is O(n), for a strictly decreasing array that keeps every position.

```java run
import java.util.*;

public final class InsertMax {
    /**
     * Returns the stored positions, front to back, after all values are processed.
     * Time: O(n) amortized. Space: O(n). Invariant: stored values never increase toward the back.
     */
    static int[] positions(int[] a) {
        Deque<Integer> d = new ArrayDeque<>();
        for (int i = 0; i < a.length; i++) {                         // one arrival per position
            while (!d.isEmpty() && a[d.peekLast()] < a[i]) d.pollLast();   // strictly smaller values are dominated
            d.addLast(i);                                            // the newest position enters at the back
        }
        int[] out = new int[d.size()];
        int k = 0;
        for (int p : d) out[k++] = p;
        return out;
    }

    /** Brute force: keep a position when no later value is strictly larger. */
    static int[] oracle(int[] a) {
        List<Integer> keep = new ArrayList<>();
        for (int i = 0; i < a.length; i++) {
            boolean beaten = false;
            for (int j = i + 1; j < a.length; j++) if (a[j] > a[i]) beaten = true;
            if (!beaten) keep.add(i);
        }
        return keep.stream().mapToInt(Integer::intValue).toArray();
    }

    public static void main(String[] args) {
        // Worked examples.
        if (!Arrays.equals(positions(new int[]{5, 3, 4, 4, 2, 6}), new int[]{5})) throw new AssertionError("example 1");
        if (!Arrays.equals(positions(new int[]{3, 3, 1}), new int[]{0, 1, 2})) throw new AssertionError("example 2");
        // Empty input.
        if (positions(new int[0]).length != 0) throw new AssertionError("empty");
        // Random arrays agree with the oracle.
        Random rnd = new Random(6);
        for (int t = 0; t < 3000; t++) {
            int n = rnd.nextInt(25);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(7) - 3;
            if (!Arrays.equals(positions(a), oracle(a))) throw new AssertionError("oracle " + Arrays.toString(a));
        }
        // Boxed integers in -128..127 are cached, so == hides the bug; equals is always correct.
        if (Integer.valueOf(127) != Integer.valueOf(127)) throw new AssertionError("cache up to 127");
        if (!Integer.valueOf(1000).equals(Integer.valueOf(1000))) throw new AssertionError("equals works above 127");
    }
}
```

#### Solution: [Vary] Insert Minimum Candidate (Author exercise)
<!-- id: dq-insert-min -->

**Approach.**

The method flips the comparison, so the back entries with strictly larger values leave first. A larger older value cannot be a future minimum when a newer value is at least as small. The invariant is that stored values never decrease from front to back, so the front holds the smallest value. The assertions compare the result with a quadratic filter on random arrays and check that the front value is the minimum of the array.

**Complexity.**

- **Time** is O(n), because the pops across all arrivals never exceed the n appends.
- **Space** is O(n), for a strictly increasing array that keeps every position.

```java run
import java.util.*;

public final class InsertMin {
    /**
     * Returns the stored positions, front to back, for the minimum rule.
     * Time: O(n) amortized. Space: O(n). Invariant: stored values never decrease toward the back.
     */
    static int[] positions(int[] a) {
        Deque<Integer> d = new ArrayDeque<>();
        for (int i = 0; i < a.length; i++) {                         // one arrival per position
            while (!d.isEmpty() && a[d.peekLast()] > a[i]) d.pollLast();   // strictly larger values are dominated
            d.addLast(i);                                            // the newest position enters at the back
        }
        int[] out = new int[d.size()];
        int k = 0;
        for (int p : d) out[k++] = p;
        return out;
    }

    public static void main(String[] args) {
        // Worked examples.
        if (!Arrays.equals(positions(new int[]{4, 6, 2, 5, 5, 1}), new int[]{5})) throw new AssertionError("example 1");
        if (!Arrays.equals(positions(new int[]{1, 2, 3}), new int[]{0, 1, 2})) throw new AssertionError("example 2");
        // Empty input.
        if (positions(new int[0]).length != 0) throw new AssertionError("empty");
        // Random arrays: keep a position when no later value is strictly smaller.
        Random rnd = new Random(7);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(25);
            int[] a = new int[n];
            int min = Integer.MAX_VALUE;
            for (int i = 0; i < n; i++) { a[i] = rnd.nextInt(7) - 3; min = Math.min(min, a[i]); }
            List<Integer> want = new ArrayList<>();
            for (int i = 0; i < n; i++) {
                boolean beaten = false;
                for (int j = i + 1; j < n; j++) if (a[j] < a[i]) beaten = true;
                if (!beaten) want.add(i);
            }
            int[] got = positions(a);
            if (!Arrays.equals(got, want.stream().mapToInt(Integer::intValue).toArray())) throw new AssertionError("oracle");
            if (a[got[0]] != min) throw new AssertionError("front is the minimum");
        }
    }
}
```

#### Solution: [Boundary] Repeated Equal Values (Author exercise)
<!-- id: dq-repeated-equal -->

**Approach.**

The two policies give the same front value and different front positions. The keep policy leaves an equal back value, so the front stays at the oldest position of the maximum. The replace policy removes an equal back value, so the front moves to the newest position of the maximum. The newest position outlasts the older one when positions later expire, which is why the replace policy is the usual choice. The invariant is that the front holds a position of the current maximum. The assertions check that both policies report the same front value after every arrival and that the replace front is never older than the keep front.

**Complexity.**

- **Time** is O(n), as the work per arrival is one append plus pops that earlier arrivals paid for.
- **Space** is O(n), because the deque and the array of recorded fronts each hold up to n entries.

```java run
import java.util.*;

public final class RepeatedEqual {
    /**
     * Returns the front position after each arrival under the chosen tie policy.
     * Time: O(n) amortized. Space: O(n). Invariant: the front is a position of the current maximum.
     */
    static int[] fronts(int[] a, boolean keepEqual) {
        Deque<Integer> d = new ArrayDeque<>();
        int[] out = new int[a.length];
        for (int i = 0; i < a.length; i++) {                         // one arrival per position
            while (!d.isEmpty() && (keepEqual ? a[d.peekLast()] < a[i] : a[d.peekLast()] <= a[i])) d.pollLast();
            d.addLast(i);                                            // the newest position enters at the back
            out[i] = d.peekFirst();                                  // report the front position
        }
        return out;
    }

    public static void main(String[] args) {
        // Worked examples.
        if (!Arrays.equals(fronts(new int[]{4, 4, 2}, true), new int[]{0, 0, 0})) throw new AssertionError("example 1");
        if (!Arrays.equals(fronts(new int[]{4, 4, 2}, false), new int[]{0, 1, 1})) throw new AssertionError("example 2");
        // Empty input.
        if (fronts(new int[0], true).length != 0) throw new AssertionError("empty");
        // Random arrays with many ties.
        Random rnd = new Random(8);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(20);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(4);
            int[] keep = fronts(a, true), repl = fronts(a, false);
            for (int i = 0; i < n; i++) {
                if (a[keep[i]] != a[repl[i]]) throw new AssertionError("values differ");
                if (repl[i] < keep[i]) throw new AssertionError("replace front is older");
            }
        }
    }
}
```

#### Solution: [Recognize] Online Suffix Maximum Candidates (Author exercise)
<!-- id: dq-suffix-maxima -->

**Approach.**

A position is a suffix maximum when no later value is strictly larger. The final deque of the keep policy holds exactly those positions. A popped position had a later strictly larger value, and a position that was never popped has none. The method builds the deque and returns it. The invariant is the one from the lesson: the stored positions are exactly the positions that no later value beats. The assertions compare the result with a right-to-left scan that tracks the running maximum.

**Complexity.**

- **Time** is O(n), because the inner loop only removes entries and no entry returns after a removal.
- **Space** is O(n), because a non-increasing array keeps every position.

```java run
import java.util.*;

public final class SuffixMaxima {
    /**
     * Returns every position whose value is at least every later value, in increasing order.
     * Time: O(n) amortized. Space: O(n). Invariant: the deque holds the positions no later value beats.
     */
    static int[] suffixMaxima(int[] a) {
        Deque<Integer> d = new ArrayDeque<>();
        for (int i = 0; i < a.length; i++) {                         // one arrival per position
            while (!d.isEmpty() && a[d.peekLast()] < a[i]) d.pollLast();   // a strictly larger later value beats it
            d.addLast(i);
        }
        int[] out = new int[d.size()];
        int k = 0;
        for (int p : d) out[k++] = p;
        return out;
    }

    /** Oracle: scan right to left with a running maximum. */
    static int[] scan(int[] a) {
        LinkedList<Integer> res = new LinkedList<>();
        int best = Integer.MIN_VALUE;
        for (int i = a.length - 1; i >= 0; i--) {
            if (a[i] >= best) res.addFirst(i);
            best = Math.max(best, a[i]);
        }
        return res.stream().mapToInt(Integer::intValue).toArray();
    }

    public static void main(String[] args) {
        // Worked examples.
        if (!Arrays.equals(suffixMaxima(new int[]{4, 2, 7, 3}), new int[]{2, 3})) throw new AssertionError("example 1");
        if (!Arrays.equals(suffixMaxima(new int[]{5, 5, 1}), new int[]{0, 1, 2})) throw new AssertionError("example 2");
        // Empty input.
        if (suffixMaxima(new int[0]).length != 0) throw new AssertionError("empty");
        // Random arrays agree with the scan.
        Random rnd = new Random(9);
        for (int t = 0; t < 3000; t++) {
            int n = rnd.nextInt(25);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(6) - 2;
            if (!Arrays.equals(suffixMaxima(a), scan(a))) throw new AssertionError("scan " + Arrays.toString(a));
        }
    }
}
```
