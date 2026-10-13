<!-- solutions-for: 07-randomized-evolution -->
### Solutions For Randomized Evolution

#### Solution: [Build] Fisher-Yates One Step (Author exercise)
<!-- id: st38-fisher-yates-step -->

**Approach.**
The method computes the bound `a.length - i`, which is the number of values still waiting at and after the frontier. It asks `pick` for one offset `k` below that bound, checks the range, and swaps `a[i]` with `a[i + k]`. The offset 0 is legal and swaps a position with itself, so the value under the frontier keeps its own chance of staying. The check happens before the swap, so an out-of-range draw leaves the array unchanged. The invariant is that positions below `i` are never read or written, and the multiset of values never changes.

The program tries every legal offset for random arrays and frontiers, and it compares the result with a model that builds the expected array by copying and rotating a list. It also records the bound that `pick` receives and checks the error path.

**Complexity.**
- **Time** is O(1), because the method makes one draw and one swap.
- **Space** is O(1), because the method keeps three local integers.

```java run
import java.util.ArrayList;
import java.util.List;
import java.util.Random;
import java.util.function.IntUnaryOperator;

public final class FisherYatesStepBuild {
    /**
     * Performs one Fisher-Yates step at frontier i.
     * Time: O(1). Space: O(1).
     * Invariant: positions below i stay untouched and the multiset of values is preserved.
     */
    static int step(int[] a, int i, IntUnaryOperator pick) {
        // The unplaced suffix has a.length - i values, so the draw bound equals that size.
        int bound = a.length - i;
        // One draw per step: the offset selects a position inside the suffix.
        int k = pick.applyAsInt(bound);
        // A bad draw is rejected before any write, so the array stays unchanged.
        if (k < 0 || k >= bound) throw new IllegalStateException("draw out of range: " + k);
        // Offset k = 0 maps j to i and the swap changes nothing, which keeps fairness.
        int j = i + k;
        // Three assignments swap the two positions in place.
        int t = a[i]; a[i] = a[j]; a[j] = t;
        // The frontier position now holds its final value.
        return a[i];
    }

    public static void main(String[] args) {
        // Example 1: draw 1 at frontier 1 swaps positions 1 and 2.
        int[] a = {4, 7, 9};
        if (step(a, 1, b -> { if (b != 2) throw new AssertionError("bound"); return 1; }) != 9
                || !java.util.Arrays.equals(a, new int[]{4, 9, 7})) throw new AssertionError("example 1");
        // Example 2: draw 2 at frontier 0 swaps the ends.
        int[] c = {5, 5, 2};
        if (step(c, 0, b -> { if (b != 3) throw new AssertionError("bound"); return 2; }) != 2
                || !java.util.Arrays.equals(c, new int[]{2, 5, 5})) throw new AssertionError("example 2");
        // Out-of-range draws throw and leave the array unchanged.
        int[] d = {1, 2, 3};
        for (int bad : new int[]{-1, 3}) {
            boolean threw = false;
            try { step(d, 0, b -> bad); } catch (IllegalStateException e) { threw = true; }
            if (!threw || !java.util.Arrays.equals(d, new int[]{1, 2, 3})) throw new AssertionError("bad draw " + bad);
        }
        // Random arrays: every legal offset gives the model result, and pick is called once.
        Random rnd = new Random(3807L);
        for (int t = 0; t < 2000; t++) {
            int n = 1 + rnd.nextInt(8);
            int[] arr = new int[n];
            for (int x = 0; x < n; x++) arr[x] = rnd.nextInt(5) - 2;
            int i = rnd.nextInt(n);
            for (int k = 0; k < n - i; k++) {
                // The model removes the chosen value from the suffix list and appends the old frontier value in its slot.
                List<Integer> model = new ArrayList<>();
                for (int x : arr) model.add(x);
                int chosen = model.get(i + k);
                model.set(i + k, model.get(i));
                model.set(i, chosen);
                int[] work = arr.clone();
                int[] calls = {0};
                final int offset = k;
                final int expectBound = n - i;
                int got = step(work, i, b -> { calls[0]++; if (b != expectBound) throw new AssertionError("bound"); return offset; });
                if (calls[0] != 1 || got != chosen) throw new AssertionError("calls or value");
                for (int x = 0; x < n; x++) if (work[x] != model.get(x)) throw new AssertionError("array mismatch");
            }
        }
    }
}
```

#### Solution: [Vary] Shuffle An Array (LeetCode 384)
<!-- id: st38-shuffle-array -->

**Approach.**
The constructor stores a private copy of `nums`. Each `shuffle()` call clones that copy into a fresh array and runs the frontier loop on the clone, and each `reset()` call returns another clone. No call writes into the stored copy and no caller receives it. The loop runs for `i` from 0 to `n - 2`, draws `i + pick.applyAsInt(n - i)` and swaps. The invariant is that the clone holds a permutation of the stored values, with positions below `i` final.

Fairness follows from counting: the draw sizes `n, n - 1, ..., 2` multiply to `n!`, and different draw sequences give different arrays when all values are distinct. The program checks this claim directly. For lengths 0 to 6 it feeds every draw sequence through a scripted source and requires that each of the `n!` orders of distinct values appears exactly once. It then runs random draws on arrays with repeated values, checks that each result is a rearrangement of the input, and checks that writes into returned arrays never change later calls.

**Complexity.**
- **Time** is O(n) per `shuffle()` and per `reset()`, because the loop and the clone each touch every position once.
- **Space** is O(n) for the stored copy and for each returned array, and the loop adds O(1) extra.

```java run
import java.util.Arrays;
import java.util.HashSet;
import java.util.Random;
import java.util.Set;
import java.util.function.IntUnaryOperator;

public final class ShuffleArrayVary {
    static final class ShuffleBox {
        private final int[] stored;
        private final IntUnaryOperator pick;

        ShuffleBox(int[] nums, IntUnaryOperator pick) {
            // A private copy protects the original order from later writes by the caller.
            this.stored = nums.clone();
            this.pick = pick;
        }

        /**
         * Returns a new array that holds the stored values in a random order.
         * Time: O(n). Space: O(n) for the returned array.
         * Invariant: the clone is always a permutation of the stored values, and positions below i are final.
         */
        int[] shuffle() {
            // The clone keeps the stored copy untouched, so reset stays possible.
            int[] out = stored.clone();
            int n = out.length;
            // Frontier i moves right; the last position needs no draw because one value is left.
            for (int i = 0; i + 1 < n; i++) {
                // The draw covers the n - i unplaced positions, including i itself.
                int j = i + pick.applyAsInt(n - i);
                // Swapping places the chosen value at the frontier, and that position is final.
                int t = out[i]; out[i] = out[j]; out[j] = t;
            }
            return out;
        }

        /**
         * Returns a new array equal to the construction-time input.
         * Time: O(n). Space: O(n).
         * Invariant: the stored copy is never written after construction.
         */
        int[] reset() {
            // A clone, not the stored array, so callers cannot write into the original.
            return stored.clone();
        }
    }

    /** Pick source that replays a fixed list of draws and checks each against its bound. */
    static IntUnaryOperator scripted(int... draws) {
        int[] pos = {0};
        return bound -> {
            int d = draws[pos[0]++];
            if (d < 0 || d >= bound) throw new AssertionError("draw " + d + " for bound " + bound);
            return d;
        };
    }

    public static void main(String[] args) {
        // Example 1: draws 2 then 0 turn [3,1,2] into [2,1,3], and reset restores the input.
        ShuffleBox b1 = new ShuffleBox(new int[]{3, 1, 2}, scripted(2, 0));
        if (!Arrays.equals(b1.shuffle(), new int[]{2, 1, 3})) throw new AssertionError("example 1 shuffle");
        if (!Arrays.equals(b1.reset(), new int[]{3, 1, 2})) throw new AssertionError("example 1 reset");
        // Example 2: duplicates stay legal and the draw sequence 1,2,0 gives [8,0,5,8].
        ShuffleBox b2 = new ShuffleBox(new int[]{8, 8, 5, 0}, scripted(1, 2, 0));
        if (!Arrays.equals(b2.shuffle(), new int[]{8, 0, 5, 8})) throw new AssertionError("example 2 shuffle");
        if (!Arrays.equals(b2.reset(), new int[]{8, 8, 5, 0})) throw new AssertionError("example 2 reset");
        // Exhaustive check: every draw sequence yields a different order, so all n! orders appear once.
        for (int n = 0; n <= 6; n++) {
            int[] input = new int[n];
            for (int i = 0; i < n; i++) input[i] = 10 + i;
            Set<String> seen = new HashSet<>();
            int[] draws = new int[Math.max(0, n - 1)];
            long total = 1;
            for (int i = 0; i < draws.length; i++) total *= (n - i);
            for (long code = 0; code < total || (n <= 1 && code == 0); code++) {
                // Decode the mixed-radix number into one draw per frontier.
                long rest = code;
                for (int i = 0; i < draws.length; i++) { draws[i] = (int) (rest % (n - i)); rest /= (n - i); }
                seen.add(Arrays.toString(new ShuffleBox(input, scripted(draws)).shuffle()));
                if (n <= 1) break;
            }
            long factorial = 1;
            for (int i = 2; i <= n; i++) factorial *= i;
            if (seen.size() != factorial) throw new AssertionError("orders for n=" + n + ": " + seen.size());
        }
        // Random draws on arrays with repeats: results are rearrangements and callers cannot corrupt the box.
        Random rnd = new Random(3808L);
        for (int t = 0; t < 2000; t++) {
            int n = rnd.nextInt(10);
            int[] nums = new int[n];
            for (int i = 0; i < n; i++) nums[i] = rnd.nextInt(4);
            int[] expected = nums.clone();
            ShuffleBox box = new ShuffleBox(nums, rnd::nextInt);
            // A caller write into the constructor argument must not reach the box.
            if (n > 0) nums[0] = 99;
            for (int round = 0; round < 4; round++) {
                int[] s = box.shuffle();
                int[] sortedS = s.clone(); Arrays.sort(sortedS);
                int[] sortedE = expected.clone(); Arrays.sort(sortedE);
                if (!Arrays.equals(sortedS, sortedE)) throw new AssertionError("not a rearrangement");
                // A caller write into a returned array must not reach the box.
                if (s.length > 0) s[0] = -7;
                int[] r = box.reset();
                if (!Arrays.equals(r, expected)) throw new AssertionError("reset changed");
                if (r.length > 0) r[0] = -8;
            }
        }
    }
}
```

#### Solution: [Boundary] Repeated Reset And Shuffle (Author exercise)
<!-- id: st38-reset-shuffle-cycles -->

**Approach.**
The class keeps two private arrays. The array `initial` is a copy of the constructor argument and never changes. The array `order` is the current order, and it starts as another copy. The method `shuffle()` runs the frontier loop on `order` in place, so the next shuffle continues from the new order, and it returns a clone. The method `current()` returns a clone of `order`. The method `reset()` copies `initial` back into `order` with `System.arraycopy` and returns a clone.

The invariant is that `order` is always a permutation of `initial`, and that no reference to either array leaves the class. Continuing from the current order is still fair. The counting argument does not depend on the starting order, because for distinct values different draw sequences still produce different results, so every order is reachable from every other with probability `1 / n!`. The lengths 0 and 1 make the loop run zero times, so they call `pick` zero times.

The program checks aliasing in both directions, runs the lengths 0 and 1, and compares against a model that keeps its own list. For starting orders other than the identity it enumerates every draw sequence and requires all `n!` results to be distinct.

**Complexity.**
- **Time** is O(n) per call, because each call runs one loop or one copy over `n` positions.
- **Space** is O(n) for the two private arrays, plus O(n) for each array returned.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.HashSet;
import java.util.List;
import java.util.Random;
import java.util.Set;
import java.util.function.IntUnaryOperator;

public final class RepeatedResetShuffleBoundary {
    static final class Deck {
        private final int[] initial;
        private final int[] order;
        private final IntUnaryOperator pick;

        Deck(int[] start, IntUnaryOperator pick) {
            // Two independent copies: one never changes, one evolves with each shuffle.
            this.initial = start.clone();
            this.order = start.clone();
            this.pick = pick;
        }

        /**
         * Applies one Fisher-Yates pass to the current order.
         * Time: O(n). Space: O(n) for the returned copy.
         * Invariant: order is a permutation of initial, and the pass never touches initial.
         */
        int[] shuffle() {
            int n = order.length;
            // Lengths 0 and 1 skip the loop, so pick is never called for them.
            for (int i = 0; i + 1 < n; i++) {
                // Draw over the unplaced suffix of size n - i.
                int j = i + pick.applyAsInt(n - i);
                // Swap in place; position i is final for this pass.
                int t = order[i]; order[i] = order[j]; order[j] = t;
            }
            // A clone keeps the caller away from the internal array.
            return order.clone();
        }

        /**
         * Returns a copy of the current order.
         * Time: O(n). Space: O(n).
         * Invariant: the call writes nothing.
         */
        int[] current() {
            // Clone so a write by the caller cannot change later shuffles.
            return order.clone();
        }

        /**
         * Restores the initial order and returns a copy of it.
         * Time: O(n). Space: O(n).
         * Invariant: afterwards order equals initial element by element.
         */
        int[] reset() {
            // Copy the values, never the reference, so the two arrays stay separate.
            System.arraycopy(initial, 0, order, 0, order.length);
            return order.clone();
        }
    }

    static IntUnaryOperator scripted(int... draws) {
        int[] pos = {0};
        return bound -> {
            int d = draws[pos[0]++];
            if (d < 0 || d >= bound) throw new AssertionError("draw " + d + " for bound " + bound);
            return d;
        };
    }

    public static void main(String[] args) {
        // Example 1: shuffle, caller write, current, reset, then a second shuffle after reset.
        int[] start = {1, 2, 3};
        Deck d = new Deck(start, scripted(1, 1, 2, 1));
        int[] s = d.shuffle();
        if (!Arrays.equals(s, new int[]{2, 3, 1})) throw new AssertionError("example 1 first shuffle");
        s[0] = 99;
        if (!Arrays.equals(d.current(), new int[]{2, 3, 1})) throw new AssertionError("returned array aliased");
        if (!Arrays.equals(d.reset(), new int[]{1, 2, 3})) throw new AssertionError("example 1 reset");
        if (!Arrays.equals(d.shuffle(), new int[]{3, 1, 2})) throw new AssertionError("example 1 second shuffle");
        // Example 2: a write to the constructor argument does not reach the deck.
        int[] arg = {4, 4};
        Deck e = new Deck(arg, scripted());
        arg[0] = 9;
        if (!Arrays.equals(e.reset(), new int[]{4, 4})) throw new AssertionError("constructor aliasing");
        // Lengths 1 and 0 call pick zero times; the scripted source with no draws would fail on a call.
        if (!Arrays.equals(new Deck(new int[]{6}, scripted()).shuffle(), new int[]{6})) throw new AssertionError("length 1");
        if (new Deck(new int[0], scripted()).shuffle().length != 0) throw new AssertionError("length 0");
        // Exhaustive fairness from a non-identity starting order of distinct values.
        int[] weird = {30, 10, 40, 20, 50};
        int n = weird.length;
        Set<String> seen = new HashSet<>();
        long total = 1;
        for (int i = 0; i < n - 1; i++) total *= (n - i);
        int[] draws = new int[n - 1];
        for (long code = 0; code < total; code++) {
            long rest = code;
            for (int i = 0; i < draws.length; i++) { draws[i] = (int) (rest % (n - i)); rest /= (n - i); }
            seen.add(Arrays.toString(new Deck(weird, scripted(draws)).shuffle()));
        }
        if (seen.size() != 120) throw new AssertionError("expected 120 distinct orders, got " + seen.size());
        // Random cycles against a model that keeps its own copy of the initial order.
        Random rnd = new Random(3809L);
        for (int t = 0; t < 2000; t++) {
            int len = rnd.nextInt(9);
            int[] src = new int[len];
            List<Integer> modelInitial = new ArrayList<>();
            for (int i = 0; i < len; i++) { src[i] = rnd.nextInt(5); modelInitial.add(src[i]); }
            Deck deck = new Deck(src, rnd::nextInt);
            List<Integer> modelCurrent = new ArrayList<>(modelInitial);
            for (int op = 0; op < 12; op++) {
                int kind = rnd.nextInt(3);
                int[] got;
                if (kind == 0) {
                    got = deck.shuffle();
                    // The shuffle keeps the multiset; the model adopts the observed order.
                    List<Integer> a = new ArrayList<>(); for (int x : got) a.add(x);
                    List<Integer> b1 = new ArrayList<>(modelCurrent), b2 = new ArrayList<>(a);
                    Collections.sort(b1); Collections.sort(b2);
                    if (!b1.equals(b2)) throw new AssertionError("shuffle changed the multiset");
                    modelCurrent = a;
                } else if (kind == 1) {
                    got = deck.current();
                    if (!Arrays.equals(got, modelCurrent.stream().mapToInt(Integer::intValue).toArray())) throw new AssertionError("current");
                } else {
                    got = deck.reset();
                    modelCurrent = new ArrayList<>(modelInitial);
                    if (!Arrays.equals(got, modelInitial.stream().mapToInt(Integer::intValue).toArray())) throw new AssertionError("reset");
                }
                // Hostile caller: scribble on the returned array and on the original argument.
                if (got.length > 0) got[0] = -5;
                if (len > 0) src[0] = -6;
            }
        }
    }
}
```

#### Solution: [Recognize] Streaming Sample Review (Author exercise)
<!-- id: st38-streaming-sample-review -->

**Approach.**
The class stores one held value and a `long` count `seen`. Each `add` increments the count to `t`, draws from the bound `t`, and replaces the held value when the draw is 0. The probability that value number `t` replaces the held one is `1 / t`. A value that arrived earlier survives each later step `s` with probability `(s - 1) / s`. These factors telescope, so after `m` additions every value is held with probability `1 / m`. The invariant is that, given `m` values added, the held value is each of them with probability `1 / m`, and the count equals `m`.

The program verifies the claim by enumeration, as in the shuffle exercises. For stream lengths 1 to 7 it feeds every combination of draws to a scripted source. A combination is one draw below `t` for each step `t`, which gives `m!` combinations. It requires that every position of the stream is held in exactly `(m - 1)!` combinations, and that the held value matches a model that records the last step whose draw was 0. It also checks the empty case and a count beyond the `int` range.

**Complexity.**
- **Time** is O(1) per call, because `add` makes one draw and `pick` reads one field.
- **Space** is O(1), because the class stores one value and one `long`, whatever the stream length.

```java run
import java.util.NoSuchElementException;
import java.util.Random;
import java.util.function.IntUnaryOperator;

public final class StreamingSampleReviewRecognize {
    static final class StreamPicker {
        private final IntUnaryOperator pick;
        private int held;
        private long seen;

        StreamPicker(IntUnaryOperator pick) { this.pick = pick; }

        /**
         * Records one value and decides whether it replaces the held value.
         * Time: O(1). Space: O(1).
         * Invariant: after m calls, each of the m values is held with probability 1/m.
         */
        void add(int value) {
            // The count includes the new value, so t is the stream length after this call.
            seen++;
            // Draw 0 out of t outcomes happens with probability 1/t, the share the newcomer needs.
            if (pick.applyAsInt((int) Math.min(seen, Integer.MAX_VALUE)) == 0) held = value;
        }

        /**
         * Returns the held value.
         * Time: O(1). Space: O(1).
         * Invariant: the call writes nothing.
         */
        int pick() {
            // An empty stream has no value to return.
            if (seen == 0) throw new NoSuchElementException();
            return held;
        }

        long count() { return seen; }
    }

    public static void main(String[] args) {
        // Example 1: draws 0,1,0 keep 5, ignore 8, then replace by 3.
        int[] script = {0, 1, 0};
        int[] at = {0};
        StreamPicker p = new StreamPicker(b -> script[at[0]++]);
        p.add(5); p.add(8); p.add(3);
        if (p.pick() != 3) throw new AssertionError("example 1");
        // Example 2: an empty picker throws, and the first value is always kept because the bound is 1.
        StreamPicker q = new StreamPicker(b -> { if (b != 1) throw new AssertionError("bound"); return 0; });
        boolean threw = false;
        try { q.pick(); } catch (NoSuchElementException e) { threw = true; }
        if (!threw) throw new AssertionError("empty must throw");
        q.add(7);
        if (q.pick() != 7) throw new AssertionError("example 2");
        // Exhaustive fairness: every position is held in exactly (m-1)! of the m! draw combinations.
        for (int m = 1; m <= 7; m++) {
            long total = 1;
            for (int t = 2; t <= m; t++) total *= t;
            long[] heldCount = new long[m];
            for (long code = 0; code < total; code++) {
                // Decode the mixed-radix number: step t uses a digit in [0, t).
                int[] draws = new int[m];
                long rest = code;
                for (int t = 1; t <= m; t++) { draws[t - 1] = (int) (rest % t); rest /= t; }
                int[] pos = {0};
                StreamPicker sp = new StreamPicker(b -> {
                    int d = draws[pos[0]++];
                    if (b != pos[0]) throw new AssertionError("bound must equal the step number");
                    return d;
                });
                for (int i = 0; i < m; i++) sp.add(100 + i);
                // The model: the held value is the one added at the last step whose draw was 0.
                int last = -1;
                for (int t = 1; t <= m; t++) if (draws[t - 1] == 0) last = t - 1;
                if (sp.pick() != 100 + last) throw new AssertionError("model mismatch");
                heldCount[last]++;
            }
            long expected = total / m;
            for (int i = 0; i < m; i++) if (heldCount[i] != expected) throw new AssertionError("m=" + m + " position " + i);
        }
        // The count is a long: it passes the int range without overflow.
        StreamPicker big = new StreamPicker(b -> 1);
        big.add(1);
        java.lang.reflect.Field f;
        try {
            f = StreamPicker.class.getDeclaredField("seen");
            f.setAccessible(true);
            f.setLong(big, (long) Integer.MAX_VALUE + 5);
        } catch (ReflectiveOperationException ex) { throw new AssertionError(ex); }
        big.add(2);
        if (big.count() != (long) Integer.MAX_VALUE + 6) throw new AssertionError("count width");
        // Random streams against a model with the same scripted draws.
        Random rnd = new Random(3810L);
        for (int t = 0; t < 2000; t++) {
            int len = 1 + rnd.nextInt(30);
            int[] vals = new int[len], dr = new int[len];
            int[] ix = {0};
            StreamPicker sp = new StreamPicker(b -> dr[ix[0]++]);
            int expectedHeld = 0;
            for (int i = 0; i < len; i++) {
                vals[i] = rnd.nextInt(6);
                dr[i] = rnd.nextInt(i + 1);
                if (dr[i] == 0) expectedHeld = vals[i];
                sp.add(vals[i]);
            }
            if (sp.pick() != expectedHeld || sp.count() != len) throw new AssertionError("random stream");
        }
    }
}
```
