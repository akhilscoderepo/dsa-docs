<!-- solutions-for: 02-front-and-back-invariants -->
### Solutions For The Two-Ended Rules Exercises

#### Solution: [Build] Decreasing Candidate Values (Author exercise)
<!-- id: dq-decreasing-values -->

**Approach.**

The method appends each value at the back after it removes every strictly smaller value from the back. A removed value is older and smaller than the value that removed it, so it can never be the maximum again. The invariant is that the stored values never increase from front to back, and the front is the largest value seen. The assertions compare the front with a running maximum on random streams, and they compare the whole deque with a brute-force filter that keeps a value only when no strictly larger value follows it.

**Complexity.**

- **Time** is O(n) for n values, because each value is appended once and removed at most once.
- **Space** is O(n), because a strictly decreasing stream stores every value.

```java run
import java.util.*;

public final class DecreasingValues {
    /**
     * Returns the deque contents from front to back after all values are processed.
     * Time: O(n) amortized. Space: O(n). Invariant: values never increase from front to back.
     */
    static int[] build(int[] values) {
        Deque<Integer> d = new ArrayDeque<>();
        for (int x : values) {                              // one arrival per value
            while (!d.isEmpty() && d.peekLast() < x) d.pollLast();   // strictly smaller values lose
            d.addLast(x);                                   // the new value enters at the back
        }
        int[] out = new int[d.size()];
        int i = 0;
        for (int v : d) out[i++] = v;
        return out;
    }

    /** Brute force: keep a value only when no later value is strictly larger. */
    static int[] oracle(int[] values) {
        List<Integer> keep = new ArrayList<>();
        for (int i = 0; i < values.length; i++) {
            boolean beaten = false;
            for (int j = i + 1; j < values.length; j++) if (values[j] > values[i]) beaten = true;
            if (!beaten) keep.add(values[i]);
        }
        return keep.stream().mapToInt(Integer::intValue).toArray();
    }

    public static void main(String[] args) {
        // Worked examples.
        if (!Arrays.equals(build(new int[]{4, 2, 7, 3}), new int[]{7, 3})) throw new AssertionError("example 1");
        if (!Arrays.equals(build(new int[]{5, 5, 5}), new int[]{5, 5, 5})) throw new AssertionError("example 2");
        // Empty input.
        if (build(new int[0]).length != 0) throw new AssertionError("empty");
        // Random streams: the filter oracle agrees, and the front is the maximum.
        Random rnd = new Random(3);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(25);
            int[] a = new int[n];
            int max = Integer.MIN_VALUE;
            for (int i = 0; i < n; i++) { a[i] = rnd.nextInt(11) - 5; max = Math.max(max, a[i]); }
            int[] got = build(a);
            if (!Arrays.equals(got, oracle(a))) throw new AssertionError("oracle " + Arrays.toString(a));
            if (got[0] != max) throw new AssertionError("front is the maximum");
        }
    }
}
```

#### Solution: [Vary] Increasing Candidate Values (Author exercise)
<!-- id: dq-increasing-values -->

**Approach.**

The method flips the comparison, so it removes strictly larger values from the back before it appends. The stored values then never decrease from front to back, and the front is the smallest value seen. The method records the front after each append. The invariant is the mirror of the build exercise. The assertions compare each recorded front with a running minimum on random streams.

**Complexity.**

- **Time** is O(n), because each value is appended once and removed at most once.
- **Space** is O(n), for the deque and for the answer array.

```java run
import java.util.*;

public final class IncreasingValues {
    /**
     * Returns the smallest value seen after each arrival.
     * Time: O(n) amortized. Space: O(n). Invariant: values never decrease from front to back.
     */
    static int[] minAfterEach(int[] values) {
        Deque<Integer> d = new ArrayDeque<>();
        int[] out = new int[values.length];
        for (int i = 0; i < values.length; i++) {           // one arrival per value
            while (!d.isEmpty() && d.peekLast() > values[i]) d.pollLast();   // strictly larger values lose
            d.addLast(values[i]);                           // the new value enters at the back
            out[i] = d.peekFirst();                         // the front holds the smallest value
        }
        return out;
    }

    public static void main(String[] args) {
        // Worked examples.
        if (!Arrays.equals(minAfterEach(new int[]{5, 3, 8, 2}), new int[]{5, 3, 3, 2})) throw new AssertionError("example 1");
        if (!Arrays.equals(minAfterEach(new int[]{1, 2, 3}), new int[]{1, 1, 1})) throw new AssertionError("example 2");
        // Empty input.
        if (minAfterEach(new int[0]).length != 0) throw new AssertionError("empty");
        // Random streams agree with a running minimum.
        Random rnd = new Random(4);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(25);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(11) - 5;
            int[] got = minAfterEach(a);
            int min = Integer.MAX_VALUE;
            for (int i = 0; i < n; i++) {
                min = Math.min(min, a[i]);
                if (got[i] != min) throw new AssertionError("min at " + i);
            }
        }
    }
}
```

#### Solution: [Boundary] Equal Candidate Policy (Author exercise)
<!-- id: dq-equal-policy -->

**Approach.**

The two policies differ in one comparison. The keep policy removes strictly smaller back values, so an equal value stays. The replace policy removes back values that are smaller or equal, so the newer equal value replaces the older one. Both policies keep the front equal to the maximum, because an equal value gives the same answer. The keep policy stores more values and the replace policy stores fewer. The invariant of the keep policy is non-increasing order. The invariant of the replace policy is strictly decreasing order. The assertions check that both policies give the same front after every arrival and that the replace deque never exceeds the keep deque in size.

**Complexity.**

- **Time** is O(n) for either policy, because each value is appended once and removed at most once.
- **Space** is O(n) in the worst case, and the replace policy never stores more than the keep policy.

```java run
import java.util.*;

public final class EqualPolicy {
    /**
     * Returns the deque from front to back after all values, under the chosen policy.
     * Time: O(n) amortized. Space: O(n).
     * Invariant: non-increasing when keepEqual, strictly decreasing otherwise.
     */
    static int[] run(int[] values, boolean keepEqual) {
        Deque<Integer> d = new ArrayDeque<>();
        for (int x : values) {                                       // one arrival per value
            while (!d.isEmpty() && (keepEqual ? d.peekLast() < x : d.peekLast() <= x)) d.pollLast();
            d.addLast(x);                                            // the new value enters at the back
        }
        int[] out = new int[d.size()];
        int i = 0;
        for (int v : d) out[i++] = v;
        return out;
    }

    public static void main(String[] args) {
        // Worked examples.
        if (!Arrays.equals(run(new int[]{4, 4, 2}, true), new int[]{4, 4, 2})) throw new AssertionError("example 1");
        if (!Arrays.equals(run(new int[]{4, 4, 2}, false), new int[]{4, 2})) throw new AssertionError("example 2");
        // Empty input under both policies.
        if (run(new int[0], true).length != 0 || run(new int[0], false).length != 0) throw new AssertionError("empty");
        // Random streams: the front agrees after every prefix, and replace is never larger.
        Random rnd = new Random(5);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(20);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(5);
            for (int len = 1; len <= n; len++) {
                int[] p = Arrays.copyOf(a, len);
                int[] keep = run(p, true), repl = run(p, false);
                if (keep[0] != repl[0]) throw new AssertionError("fronts differ");
                if (repl.length > keep.length) throw new AssertionError("replace stores more");
            }
        }
    }
}
```

#### Solution: [Recognize] Name Each End (Author exercise)
<!-- id: dq-name-each-end -->

**Approach.**

A removal for age belongs at the front, because the oldest value sits there. A removal for value belongs at the back, because the newest and weakest value sits there. The method scans the records and returns the position of the first record whose end does not match its cause, or `-1` when every record matches. The invariant is that the front serves age and the back serves value. The assertions try matching records, one wrong end of each kind, and a mismatch late in a long list.

**Complexity.**

- **Time** is O(r) for r records, because the scan reads each record once.
- **Space** is O(1), because the scan keeps one index.

```java run
public final class NameEachEnd {
    /**
     * Returns the first record whose end does not match its cause, or -1.
     * Time: O(r). Space: O(1). Invariant: age removes at the front, value removes at the back.
     */
    static int firstMismatch(String[][] records) {
        for (int i = 0; i < records.length; i++) {                   // one check per record
            boolean frontForAge = records[i][0].equals("front") == records[i][1].equals("age");
            if (!frontForAge) return i;                              // the end and the cause disagree
        }
        return -1;
    }

    public static void main(String[] args) {
        // Worked examples.
        if (firstMismatch(new String[][]{{"front", "age"}, {"back", "value"}}) != -1) throw new AssertionError("example 1");
        if (firstMismatch(new String[][]{{"back", "age"}}) != 0) throw new AssertionError("example 2");
        // Empty record list.
        if (firstMismatch(new String[0][]) != -1) throw new AssertionError("empty");
        // The other wrong pairing and a late mismatch.
        if (firstMismatch(new String[][]{{"front", "value"}}) != 0) throw new AssertionError("front for value");
        if (firstMismatch(new String[][]{{"front", "age"}, {"back", "value"}, {"front", "age"}, {"front", "value"}}) != 3) throw new AssertionError("late mismatch");
    }
}
```
