<!-- solutions-for: 03-reservoir-sampling -->
### Solutions For Reservoir Sampling

#### Solution: [Build] Sample One Item (Author exercise)
<!-- id: rs35-sample-one -->

**Approach.**
The method stores the first item as the held item and starts the counter `t` at 1. For each later item it raises `t` by one and calls `pick` with the new `t`, so the bound grows from 2 up to `n`. A result of 0 replaces the held item. The chance that item `t` is held right after its own draw is `1 / t`. An older item that was held with chance `1 / (t - 1)` stays with chance `(t - 1) / t`, so every item holds with chance `1 / t`. The method checks the range of each draw before using it. The invariant is that after `t` items each of them is held with chance `1 / t`.

The program proves fairness by enumeration. For each stream length up to 6 it runs the method on every possible sequence of draws, which has `n!` members, and counts how often each position is the held one. Every position must appear exactly `(n - 1)!` times. A scripted source checks that the bounds are 2, 3 and so on.

**Complexity.**
- **Time** is O(n) for one pass with one draw per item.
- **Space** is O(1), because the method keeps the held item and the counter.

```java run
import java.util.NoSuchElementException;
import java.util.function.LongUnaryOperator;

public final class SampleOneBuild {
    /**
     * Returns the held item after one pass.
     * Time: O(n). Space: O(1).
     * Invariant: after t items each of them is held with chance 1/t.
     */
    static int sampleOne(int[] stream, LongUnaryOperator pick) {
        if (stream.length == 0) throw new NoSuchElementException(); // nothing to sample
        int held = stream[0]; // item 1 enters with chance 1
        long t = 1;
        for (int i = 1; i < stream.length; i++) {
            t++; // t is the number of items that have arrived
            long d = pick.applyAsLong(t); // replacement draw with bound t
            if (d < 0 || d >= t) throw new IllegalStateException("draw out of range");
            if (d == 0) held = stream[i]; // replace with chance 1/t
        }
        return held;
    }

    /** Feeds a fixed list of draws and checks every bound on the way. */
    static final class Script implements LongUnaryOperator {
        final long[] draws; int next = 0;
        Script(long... draws) { this.draws = draws; }
        public long applyAsLong(long bound) {
            long expected = next + 2; // the first draw has bound 2
            if (bound != expected) throw new AssertionError("bound " + bound + " expected " + expected);
            return draws[next++];
        }
    }

    public static void main(String[] args) {
        // the two examples from the problem text
        if (sampleOne(new int[]{5, 8, 3, 9}, new Script(1, 0, 2)) != 3) throw new AssertionError("ex1");
        if (sampleOne(new int[]{7}, new Script()) != 7) throw new AssertionError("ex2");
        // an empty stream throws
        boolean threw = false;
        try { sampleOne(new int[0], new Script()); } catch (NoSuchElementException e) { threw = true; }
        if (!threw) throw new AssertionError("empty");
        // exact fairness: enumerate every draw sequence and count how often each position is held
        for (int n = 1; n <= 6; n++) {
            int[] stream = new int[n];
            for (int i = 0; i < n; i++) stream[i] = i; // distinct values identify positions
            long[] counts = new long[n];
            long[] draws = new long[Math.max(0, n - 1)];
            while (true) {
                counts[sampleOne(stream, new Script(draws.clone()))]++;
                int pos = 0; // odometer: draw k has bound k + 2
                while (pos < draws.length && ++draws[pos] == pos + 2) draws[pos++] = 0;
                if (pos == draws.length) break;
            }
            long fact = 1;
            for (int i = 2; i < n; i++) fact *= i; // (n - 1)!
            for (long c : counts) if (c != fact) throw new AssertionError("unfair at n=" + n);
        }
        System.out.println("ok");
    }
}
```

#### Solution: [Vary] Linked List Random Node (LeetCode 382)
<!-- id: rs35-linked-list-random-node -->

**Approach.**
A linked list gives no length and no index, so the counter `t` counts the nodes read so far. The method sets the held value to the head value and walks the remaining nodes. At each node it raises `t` and draws from bound `t`. A result of 0 replaces the held value. The walk reads each node once and writes nothing into the list, so the list stays unchanged. The proof is the same as for an array: after `t` nodes, each has chance `1 / t`. The invariant is that `held` is the value of a node chosen uniformly among the first `t` nodes.

The program builds lists of length 1 to 6 and enumerates all draw sequences. Each node must be returned in exactly `(n - 1)!` sequences. It also checks that the list is unchanged after the walk and that the examples match.

**Complexity.**
- **Time** is O(n) for one walk.
- **Space** is O(1), because the walk keeps a node reference, the counter and the held value.

```java run
import java.util.function.LongUnaryOperator;

public final class LinkedListRandomNodeVary {
    static final class ListNode {
        int val; ListNode next;
        ListNode(int val, ListNode next) { this.val = val; this.next = next; }
    }

    /**
     * Returns the value of a uniformly chosen node.
     * Time: O(n). Space: O(1).
     * Invariant: held is the value of a node chosen uniformly among the t nodes read so far.
     */
    static int randomNode(ListNode head, LongUnaryOperator pick) {
        int held = head.val; // the first node is the sample so far
        long t = 1;
        for (ListNode cur = head.next; cur != null; cur = cur.next) {
            t++; // one more node has been read
            if (pick.applyAsLong(t) == 0) held = cur.val; // chance 1/t to take this node
        }
        return held;
    }

    static ListNode build(int... vals) {
        ListNode head = null;
        for (int i = vals.length - 1; i >= 0; i--) head = new ListNode(vals[i], head);
        return head;
    }

    public static void main(String[] args) {
        // the two examples from the problem text
        long[] d1 = {0, 0};
        int[] at1 = {0};
        if (randomNode(build(1, 2, 3), b -> d1[at1[0]++]) != 3) throw new AssertionError("ex1");
        if (randomNode(build(4, 5), b -> 1) != 4) throw new AssertionError("ex2");
        // exact fairness: every node is returned in exactly (n - 1)! of the n! draw sequences
        for (int n = 1; n <= 6; n++) {
            int[] vals = new int[n];
            for (int i = 0; i < n; i++) vals[i] = 100 + i;
            ListNode head = build(vals);
            long[] counts = new long[n];
            long[] draws = new long[Math.max(0, n - 1)];
            while (true) {
                final long[] copy = draws.clone();
                final int[] at = {0};
                counts[randomNode(head, b -> copy[at[0]++]) - 100]++;
                int pos = 0;
                while (pos < draws.length && ++draws[pos] == pos + 2) draws[pos++] = 0; // odometer with bound pos + 2
                if (pos == draws.length) break;
            }
            long fact = 1;
            for (int i = 2; i < n; i++) fact *= i;
            for (long c : counts) if (c != fact) throw new AssertionError("unfair at n=" + n);
            // the walk must leave the list unchanged
            ListNode cur = head;
            for (int i = 0; i < n; i++, cur = cur.next) if (cur.val != 100 + i) throw new AssertionError("list changed");
        }
        System.out.println("ok");
    }
}
```

#### Solution: [Boundary] First K Items And Short Stream (Author exercise)
<!-- id: rs35-first-k-short-stream -->

**Approach.**
The result array has length `min(k, n)`, which covers a stream shorter than `k` without a special case. The first `min(k, n)` items go into slots 0 onward in arrival order. For each later item number `t` the method draws `j` from bound `t`. When `j < k` the item overwrites slot `j`. The new item is kept with chance `k / t`. A specific held item is overwritten with chance `(k / t) * (1 / k) = 1 / t`, so an item held with chance `k / (t - 1)` keeps `k / t`. The invariant is that after `t` items every item seen is in the reservoir with chance `k / t` (or with chance 1 when `t <= k`).

The program enumerates every sequence of draws for stream lengths up to 6 and every `k` up to 7. For each case, every position must appear in the final reservoir in exactly `k * n! / (k! * n)` sequences when `n >= k`, and in every sequence when `n < k`. It also checks the two examples and the empty stream.

**Complexity.**
- **Time** is O(n) for one pass.
- **Space** is O(k) for the reservoir, and O(1) beyond it.

```java run
import java.util.Arrays;
import java.util.function.LongUnaryOperator;

public final class FirstKShortStreamBoundary {
    /**
     * Returns the reservoir after one pass.
     * Time: O(n). Space: O(min(k, n)).
     * Invariant: after t items each item is in the reservoir with chance min(1, k/t).
     */
    static int[] sampleK(int[] stream, int k, LongUnaryOperator pick) {
        int[] slots = new int[Math.min(k, stream.length)]; // a short stream gives a short result
        for (int i = 0; i < stream.length; i++) {
            long t = i + 1L; // number of items that have arrived
            if (t <= k) { slots[i] = stream[i]; continue; } // fill phase: no draw
            long j = pick.applyAsLong(t); // 0 to t - 1
            if (j < k) slots[(int) j] = stream[i]; // enters with chance k/t into slot j
        }
        return slots;
    }

    public static void main(String[] args) {
        // the two examples from the problem text
        long[] d = {0, 3, 1};
        int[] at = {0};
        if (!Arrays.equals(sampleK(new int[]{10, 20, 30, 40, 50}, 2, b -> d[at[0]++]), new int[]{30, 50})) throw new AssertionError("ex1");
        if (!Arrays.equals(sampleK(new int[]{9, 8}, 5, b -> { throw new AssertionError("no draw"); }), new int[]{9, 8})) throw new AssertionError("ex2");
        // an empty stream gives an empty array
        if (sampleK(new int[0], 3, b -> 0).length != 0) throw new AssertionError("empty");
        // exact fairness over every draw sequence: counts per position are equal
        for (int n = 1; n <= 6; n++) for (int kk = 1; kk <= 7; kk++) {
            final int k = kk; // effectively final copy for the lambda
            int[] stream = new int[n];
            for (int i = 0; i < n; i++) stream[i] = i;
            int draws = Math.max(0, n - k); // draws exist for items k + 1 .. n
            long[] seq = new long[draws];
            long[] counts = new long[n];
            long total = 0;
            while (true) {
                final long[] copy = seq.clone();
                final int[] cursor = {0};
                int[] res = sampleK(stream, k, b -> {
                    long expectedBound = k + 1 + cursor[0];
                    if (b != expectedBound) throw new AssertionError("bound");
                    return copy[cursor[0]++];
                });
                for (int v : res) counts[v]++;
                total++;
                int pos = 0; // odometer: draw index p has bound k + 1 + p
                while (pos < draws && ++seq[pos] == k + 1 + pos) seq[pos++] = 0;
                if (pos == draws) break;
            }
            // each position must be present in k/n of the sequences (all of them when n <= k)
            long expected = n <= k ? total : total * k / n;
            if (n > k && (total * k) % n != 0) throw new AssertionError("not divisible");
            for (long c : counts) if (c != expected) throw new AssertionError("unfair n=" + n + " k=" + k);
        }
        System.out.println("ok");
    }
}
```

#### Solution: [Recognize] Random Pick Index (LeetCode 398)
<!-- id: rs35-random-pick-index -->

**Approach.**
Only positions with `nums[i] == target` count as items, so the counter `m` counts matches. The first match is taken without a draw. For the `m`-th match, the method calls `pick` with bound `m` and replaces the stored index when the result is 0. A draw bound based on the array position would give early matches too little weight, because the position grows even when no match arrives. The method stores one index and one counter, so it needs no list of indices. The proof is the reservoir proof applied to the subsequence of matches. The invariant is that after `m` matches, each of them is the stored index with chance `1 / m`.

The program enumerates all draw sequences for arrays of length up to 7 over a small value range and checks that every matching index appears equally often. It also confirms the examples and that a wrong bound, the array position, produces unequal counts.

**Complexity.**
- **Time** is O(n) for one pass.
- **Space** is O(1), because the method stores one index and one counter.

```java run
import java.util.ArrayList;
import java.util.List;
import java.util.function.LongUnaryOperator;

public final class RandomPickIndexRecognize {
    /**
     * Returns a uniformly chosen index among the positions equal to target.
     * Time: O(n). Space: O(1).
     * Invariant: after m matches the stored index is each of them with chance 1/m.
     */
    static int pickIndex(int[] nums, int target, LongUnaryOperator pick) {
        int chosen = -1;
        long m = 0; // count of matches so far
        for (int i = 0; i < nums.length; i++) {
            if (nums[i] != target) continue; // only matches are items
            m++;
            if (m == 1 || pick.applyAsLong(m) == 0) chosen = i; // first match enters, later ones with chance 1/m
        }
        return chosen;
    }

    /** The biased variant that uses the array position as the bound. */
    static int biased(int[] nums, int target, LongUnaryOperator pick) {
        int chosen = -1;
        for (int i = 0; i < nums.length; i++) {
            if (nums[i] != target) continue;
            if (chosen == -1 || pick.applyAsLong(i + 1) == 0) chosen = i;
        }
        return chosen;
    }

    interface Picker { int run(int[] nums, int target, LongUnaryOperator p); }

    /** Counts results over all draw sequences, where the sequence length is the number of draws used. */
    static long[] histogram(Picker f, int[] nums, int target, long[] bounds) {
        long[] counts = new long[nums.length];
        long[] seq = new long[bounds.length];
        while (true) {
            final long[] copy = seq.clone();
            final int[] at = {0};
            counts[f.run(nums, target, b -> copy[at[0]++])]++;
            int pos = 0;
            while (pos < seq.length && ++seq[pos] == bounds[pos]) seq[pos++] = 0;
            if (pos == seq.length) break;
        }
        return counts;
    }

    public static void main(String[] args) {
        // the two examples from the problem text
        long[] d = {1, 0};
        int[] at = {0};
        if (pickIndex(new int[]{1, 2, 3, 3, 3}, 3, b -> d[at[0]++]) != 4) throw new AssertionError("ex1");
        if (pickIndex(new int[]{5, 5}, 5, b -> 0) != 1) throw new AssertionError("ex2");
        // exact fairness on arrays with gaps between matches
        int[][] cases = {{3, 1, 3, 2, 3}, {2, 3, 3, 1, 3, 3, 0}, {4, 4, 4, 4}, {1, 7, 2}};
        for (int[] nums : cases) {
            int target = nums[0] == 4 ? 4 : (nums.length == 3 ? 7 : 3);
            List<Integer> matches = new ArrayList<>();
            for (int i = 0; i < nums.length; i++) if (nums[i] == target) matches.add(i);
            long[] bounds = new long[matches.size() - 1];
            for (int i = 0; i < bounds.length; i++) bounds[i] = i + 2; // the m-th match draws from bound m
            long[] counts = histogram(RandomPickIndexRecognize::pickIndex, nums, target, bounds);
            long expected = -1;
            for (int i : matches) { if (expected == -1) expected = counts[i]; if (counts[i] != expected) throw new AssertionError("unfair " + i); }
        }
        // the position-based bound is not fair on {3,1,3,2,3}: matches at 0, 2, 4 draw from bounds 3 and 5
        long[] bad = histogram(RandomPickIndexRecognize::biased, new int[]{3, 1, 3, 2, 3}, 3, new long[]{3, 5});
        if (bad[0] == bad[2] && bad[2] == bad[4]) throw new AssertionError("biased variant looks fair");
        System.out.println("ok");
    }
}
```
