<!-- solutions-for: 04-deferred-transforms -->
### Solutions For Deferred Transforms

#### Solution: [Build] Global Add Sequence (Author exercise)
<!-- id: dq39-global-add-sequence -->

**Approach.** The structure keeps one number, `offset`, that records the sum of every `addAll` argument so far. Each stored raw value is the visible value minus the offset in force when it was appended. A read adds the current offset back to the raw value.

The invariant is that the true value of entry `i` equals `raw[i] + offset` after every call. An `addAll(d)` raises `offset` by `d`, so every existing entry rises by `d` at once. A value appended later subtracts the offset at its arrival, so it does not receive additions that happened before it existed. The harness compares every read with a brute-force list that applies each addition to each entry, and it asserts that a bad index returns -1.

**Complexity.**

- **Time** is O(1) per call, because each call reads or writes one list slot and one number.
- **Space** is O(n) for the `n` appended raw values plus one offset.

```java run
import java.util.ArrayList;
import java.util.Random;

public final class GlobalAddSequence {
    // The pending offset equals the sum of all addAll arguments received so far.
    private long offset = 0;
    // Raw values hold each appended value minus the offset at its arrival.
    private final ArrayList<Long> raw = new ArrayList<>();

    /**
     * Appends v so that it reads back as v right now.
     * Time: O(1) amortized. Space: O(1) extra per call.
     * Invariant: raw.get(i) + offset is the true value of entry i.
     */
    void append(long v) {
        // Subtract the offset so that the later read, which adds it back, returns v.
        raw.add(v - offset);
    }

    /**
     * Adds d to every current entry in constant time.
     * Time: O(1). Space: O(1).
     * Invariant: only offset changes, which shifts every stored entry equally.
     */
    void addAll(long d) {
        // One update replaces a loop over all entries; later appends are unaffected.
        offset += d;
    }

    /**
     * Returns the current value of entry i.
     * Time: O(1). Space: O(1).
     * Invariant: raw.get(i) + offset is the true value of entry i.
     */
    long get(int i) {
        // Return -1 for indices outside the sequence, as the contract requires.
        if (i < 0 || i >= raw.size()) return -1;
        // Add the offset back to the raw value to recover the visible value.
        return raw.get(i) + offset;
    }

    public static void main(String[] args) {
        // Check Example 1 and Example 2 from the exercise.
        GlobalAddSequence s = new GlobalAddSequence();
        s.append(5); s.addAll(3); s.append(10);
        if (s.get(0) != 8 || s.get(1) != 10) throw new AssertionError("example 1");
        s.addAll(-4);
        if (s.get(0) != 4 || s.get(1) != 6) throw new AssertionError("example 2");
        // Check that an invalid index returns -1, since the contract promises it.
        if (s.get(2) != -1 || s.get(-1) != -1) throw new AssertionError("bad index must return -1");
        // Compare against a brute-force list on random call sequences.
        Random rnd = new Random(1);
        for (int round = 0; round < 300; round++) {
            GlobalAddSequence fast = new GlobalAddSequence();
            ArrayList<Long> slow = new ArrayList<>();
            for (int step = 0; step < 60; step++) {
                int kind = rnd.nextInt(3);
                long x = rnd.nextInt(2_000_001) - 1_000_000;
                if (kind == 0) { fast.append(x); slow.add(x); }
                else if (kind == 1) { fast.addAll(x); for (int i = 0; i < slow.size(); i++) slow.set(i, slow.get(i) + x); }
                else if (!slow.isEmpty()) {
                    int i = rnd.nextInt(slow.size());
                    if (fast.get(i) != slow.get(i)) throw new AssertionError("round " + round + " step " + step);
                }
            }
        }
    }
}
```

#### Solution: [Vary] Fancy Sequence (LeetCode 1622)
<!-- id: dq39-fancy-sequence -->

**Approach.** The structure keeps a raw value per entry and one pending pair `(mul, add)`. The invariant is that the true value of entry `i` equals `raw[i] * mul + add` modulo `M` after every call. The call `addAll(d)` adds `d` to `add`. The call `multAll(m)` multiplies both `mul` and `add` by `m`, because the earlier additions must be scaled as well.

An appended value `v` needs a raw value `x` with `x * mul + add = v`. The code computes `x = (v - add) * inverse(mul)`, where the inverse is `mul^(M-2)` by Fermat's little theorem. The inverse exists because every `m` lies in `[1, 100]` and `M` is a prime larger than 100, so `mul` never becomes a multiple of `M`. The harness asserts that `%` returns a negative remainder for a negative left operand, which is why `append` adds `M` before the final reduction. It also checks the inverse identity and compares every read with a naive loop on random calls.

**Complexity.**

- **Time** is O(1) for `addAll`, `multAll` and `getIndex`, and O(log M) for `append`, because the inverse needs about 30 squarings.
- **Space** is O(n) for the raw values plus two numbers for the pair.

```java run
import java.util.ArrayList;
import java.util.Random;

public final class FancySequence {
    // M is prime, so every residue except 0 has a modular inverse.
    private static final long M = 1_000_000_007L;
    // Raw values hold each entry as it must be stored, given the pair at its arrival.
    private final ArrayList<Long> raw = new ArrayList<>();
    // Pending multiplier of the affine pair, never a multiple of M in this exercise.
    private long mul = 1;
    // Pending addend of the affine pair.
    private long add = 0;

    /**
     * Computes base^exp mod M by repeated squaring.
     * Time: O(log exp). Space: O(1).
     * Invariant: result * base^exp stays equal to the original power.
     */
    static long power(long base, long exp) {
        // Start with the multiplicative identity.
        long result = 1;
        // Reduce the base once so that products stay below M * M.
        base %= M;
        // Each pass handles one bit of the exponent, so there are about 30 passes.
        while (exp > 0) {
            // A set low bit multiplies the current square into the result.
            if ((exp & 1) == 1) result = result * base % M;
            // Squaring prepares the next bit.
            base = base * base % M;
            // Drop the bit that was just handled.
            exp >>= 1;
        }
        // The result equals base^exp mod M.
        return result;
    }

    /**
     * Appends v so that it reads back as v under the current pair.
     * Time: O(log M). Space: O(1) extra.
     * Invariant: raw * mul + add equals v modulo M for the new entry.
     */
    void append(long v) {
        // Reduce v - add into [0, M), because Java % can return a negative remainder.
        long shifted = ((v - add) % M + M) % M;
        // Multiply by the inverse of mul to undo the pending multiplier.
        raw.add(shifted * power(mul, M - 2) % M);
    }

    /**
     * Adds inc to every existing entry.
     * Time: O(1). Space: O(1).
     * Invariant: only add changes, which shifts every existing entry equally.
     */
    void addAll(long inc) {
        // Compose the new addition with the pending pair.
        add = (add + inc) % M;
    }

    /**
     * Multiplies every existing entry by m.
     * Time: O(1). Space: O(1).
     * Invariant: scaling both parts of the pair scales raw * mul + add.
     */
    void multAll(long m) {
        // The multiplier scales the multiplier part.
        mul = mul * m % M;
        // The addend also scales, because earlier additions are multiplied too.
        add = add * m % M;
    }

    /**
     * Returns the value at idx modulo M, or -1 when idx is out of range.
     * Time: O(1). Space: O(1).
     * Invariant: raw * mul + add is the true value of the entry.
     */
    long getIndex(int idx) {
        // An index at or beyond the size has no entry.
        if (idx >= raw.size()) return -1;
        // Apply the pending pair to the stored raw value.
        return (raw.get(idx) * mul + add) % M;
    }

    public static void main(String[] args) {
        // Check Example 1 and Example 2 from the exercise.
        FancySequence f = new FancySequence();
        f.append(2); f.addAll(3); f.append(7); f.multAll(2);
        if (f.getIndex(0) != 10 || f.getIndex(1) != 14 || f.getIndex(2) != -1) throw new AssertionError("example 1");
        FancySequence g = new FancySequence();
        g.append(5);
        for (int i = 0; i < 6; i++) g.multAll(100);
        g.append(9);
        if (g.getIndex(0) != 999965007L || g.getIndex(1) != 9) throw new AssertionError("example 2");
        // Check the Java claim that % keeps the sign of the left operand.
        if (-7 % 3 != -1) throw new AssertionError("remainder sign");
        // Check the Fermat inverse identity for several residues.
        for (long a : new long[] {1, 2, 100, 999_999_999L}) {
            if (a * power(a, M - 2) % M != 1) throw new AssertionError("inverse of " + a);
        }
        // Compare against a brute-force list on random calls with the exercise limits.
        Random rnd = new Random(2);
        for (int round = 0; round < 300; round++) {
            FancySequence fast = new FancySequence();
            ArrayList<Long> slow = new ArrayList<>();
            for (int step = 0; step < 80; step++) {
                int kind = rnd.nextInt(4);
                if (kind == 0) { long v = rnd.nextInt(101); fast.append(v); slow.add(v); }
                else if (kind == 1) { long d = rnd.nextInt(101); fast.addAll(d); for (int i = 0; i < slow.size(); i++) slow.set(i, (slow.get(i) + d) % M); }
                else if (kind == 2) { long m = 1 + rnd.nextInt(100); fast.multAll(m); for (int i = 0; i < slow.size(); i++) slow.set(i, slow.get(i) * m % M); }
                else {
                    int idx = rnd.nextInt(slow.size() + 2);
                    long want = idx < slow.size() ? slow.get(idx) : -1;
                    if (fast.getIndex(idx) != want) throw new AssertionError("round " + round + " step " + step);
                }
            }
        }
    }
}
```

#### Solution: [Boundary] Zero Multiplier (Author exercise)
<!-- id: dq39-zero-multiplier -->

**Approach.** A multiplier of 0 makes the pending `mul` equal to 0 modulo the prime `M`. A zero has no inverse, because no `y` satisfies `0 * y = 1`, so the formula `x = (v - add) * inverse(mul)` breaks on the next append. The design avoids the division by resetting the pair whenever `m = 0` arrives.

On `multAll(0)` every existing entry becomes 0, whatever it held. The code sets `frozen` to the current size, resets the pair to `(1, 0)` and keeps the old raw values untouched. The invariant is that entry `i` below `frozen` has true value `add`, and entry `i` at or above `frozen` has true value `raw[i] * mul + add`. A frozen entry behaves as a raw value of 0 under the fresh pair, so later additions and nonzero multiplications still apply to it correctly. After a reset, `mul` is a product of nonzero residues of a prime, so it is nonzero and invertible until the next zero call, which resets again. The harness asserts that the power function returns 0 for base 0, so no inverse exists. It then compares every read with a naive loop on random calls that contain many zeros.

**Complexity.**

- **Time** is O(1) for `addAll`, `multAll` and `getIndex`, and O(log M) for `append`, because the reset replaces any scan of the entries.
- **Space** is O(n) for the raw values plus the pair and the `frozen` boundary.

```java run
import java.util.ArrayList;
import java.util.Random;

public final class ZeroMultiplierSequence {
    // M is prime, so a residue has an inverse exactly when it is not 0.
    private static final long M = 1_000_000_007L;
    // Raw values of entries appended since the last reset keep their meaning under the pair.
    private final ArrayList<Long> raw = new ArrayList<>();
    // Entries with index below frozen were zeroed by a multiplier of 0 and read as add.
    private int frozen = 0;
    // Pending multiplier, always a nonzero residue so that it stays invertible.
    private long mul = 1;
    // Pending addend.
    private long add = 0;

    /**
     * Computes base^exp mod M by repeated squaring.
     * Time: O(log exp). Space: O(1).
     * Invariant: result * base^exp stays equal to the original power.
     */
    static long power(long base, long exp) {
        // Start with the multiplicative identity.
        long result = 1;
        // Reduce the base once so that products stay below M * M.
        base %= M;
        // Each pass handles one bit of the exponent.
        while (exp > 0) {
            // A set low bit multiplies the current square into the result.
            if ((exp & 1) == 1) result = result * base % M;
            // Squaring prepares the next bit.
            base = base * base % M;
            // Drop the handled bit.
            exp >>= 1;
        }
        // The result equals base^exp mod M.
        return result;
    }

    /**
     * Appends v so that it reads back as v under the current pair.
     * Time: O(log M). Space: O(1) extra.
     * Invariant: mul is nonzero, so its inverse exists and raw * mul + add equals v.
     */
    void append(long v) {
        // Reduce v - add into [0, M), because Java % can return a negative remainder.
        long shifted = ((v - add) % M + M) % M;
        // Divide by mul using its Fermat inverse, which is safe because mul is nonzero.
        raw.add(shifted * power(mul, M - 2) % M);
    }

    /**
     * Adds inc to every existing entry.
     * Time: O(1). Space: O(1).
     * Invariant: only add changes, which shifts every existing entry equally.
     */
    void addAll(long inc) {
        // Compose the addition with the pending pair.
        add = (add + inc) % M;
    }

    /**
     * Multiplies every existing entry by m, where m may be 0.
     * Time: O(1). Space: O(1).
     * Invariant: after the call, mul is nonzero and frozen entries read as add.
     */
    void multAll(long m) {
        // A zero multiplier cannot be stored in mul, so it triggers a reset.
        if (m == 0) {
            // Every entry that exists now becomes 0 and is marked by the frozen boundary.
            frozen = raw.size();
            // The fresh pair is the identity, so a frozen entry reads as 0 * 1 + 0 = 0.
            mul = 1;
            add = 0;
            // Nothing else changes, so no scan of the entries is needed.
            return;
        }
        // A nonzero multiplier scales the multiplier part, and a product of nonzero residues stays nonzero.
        mul = mul * m % M;
        // The addend scales too, because earlier additions are multiplied.
        add = add * m % M;
    }

    /**
     * Returns the value at idx modulo M, or -1 when idx is out of range.
     * Time: O(1). Space: O(1).
     * Invariant: frozen entries read as add, others as raw * mul + add.
     */
    long getIndex(int idx) {
        // An index at or beyond the size has no entry.
        if (idx >= raw.size()) return -1;
        // A frozen entry was zeroed, so only the addend since the reset remains.
        if (idx < frozen) return add;
        // Other entries apply the full pair to the stored raw value.
        return (raw.get(idx) * mul + add) % M;
    }

    public static void main(String[] args) {
        // Check Example 1 and Example 2 from the exercise.
        ZeroMultiplierSequence a = new ZeroMultiplierSequence();
        a.append(4); a.multAll(0); a.addAll(6); a.append(9);
        if (a.getIndex(0) != 6 || a.getIndex(1) != 9) throw new AssertionError("example 1");
        ZeroMultiplierSequence b = new ZeroMultiplierSequence();
        b.append(7); b.append(1); b.multAll(0); b.addAll(4); b.append(3); b.multAll(5);
        if (b.getIndex(0) != 20 || b.getIndex(2) != 15) throw new AssertionError("example 2");
        // Check that zero has no inverse: the power function returns 0, and 0 never multiplies to 1.
        if (power(0, M - 2) != 0) throw new AssertionError("zero power");
        if (0L * power(0, M - 2) % M == 1) throw new AssertionError("zero inverse");
        // Compare against a brute-force list on random calls with frequent zero multipliers.
        Random rnd = new Random(3);
        for (int round = 0; round < 400; round++) {
            ZeroMultiplierSequence fast = new ZeroMultiplierSequence();
            ArrayList<Long> slow = new ArrayList<>();
            for (int step = 0; step < 80; step++) {
                int kind = rnd.nextInt(4);
                if (kind == 0) { long v = rnd.nextInt(5) == 0 ? M - 1 : (long) rnd.nextInt(1_000_000_000); fast.append(v); slow.add(v); }
                else if (kind == 1) { long d = rnd.nextInt(1_000_000_000); fast.addAll(d); for (int i = 0; i < slow.size(); i++) slow.set(i, (slow.get(i) + d) % M); }
                else if (kind == 2) {
                    long m = rnd.nextInt(3) == 0 ? 0 : (long) rnd.nextInt(1_000_000_000) + 1;
                    fast.multAll(m);
                    for (int i = 0; i < slow.size(); i++) slow.set(i, slow.get(i) * m % M);
                } else {
                    int idx = rnd.nextInt(slow.size() + 2);
                    long want = idx < slow.size() ? slow.get(idx) : -1;
                    if (fast.getIndex(idx) != want) throw new AssertionError("round " + round + " step " + step);
                }
            }
        }
    }
}
```

#### Solution: [Recognize] Affine Lazy Segment Tree (Author exercise)
<!-- id: dq39-affine-lazy-segment-tree -->

**Approach.** A range update touches only some entries, so one global pair cannot describe it. Two entries that differ in range membership need different transforms. The fix is a segment tree. Every node stores the sum of its half-open segment `[lo, hi)`. It also stores a pending pair `(mul, add)` that applies to the whole segment but not yet to its children.

The invariant is that a node's sum already includes every update that reached it, and its pending pair still has to reach its children. Applying `(b, c)` to a node of length `len` sets the sum to `b * sum + c * len`, because each of the `len` entries gains `c` after scaling. It also composes the tag, so the new pair is `(b * mul, b * add + c)`, which applies the older pair first and the new one second. Before descending, a node pushes its pair to both children and resets to the identity `(1, 0)`. The pair `b = 0` needs no inverse, because the tree composes and never divides. The harness compares both calls with a naive array on random ranges, including empty ranges and `b = 0`.

**Complexity.**

- **Time** is O(log n) per `apply` and per `sum`, because each call visits at most about four nodes per level and pushes down one pair per visited node.
- **Space** is O(n) for the arrays of sums and tags, with 4n slots each.

```java run
import java.util.Random;

public final class AffineLazySegmentTree {
    // M is the prime modulus of every stored sum.
    private static final long M = 1_000_000_007L;
    // sum[o] is the sum of the half-open segment of node o, including all updates that reached o.
    private final long[] sum;
    // mulTag[o] and addTag[o] hold the pending pair that children of o have not received yet.
    private final long[] mulTag, addTag;
    // n is the number of array entries.
    private final int n;

    AffineLazySegmentTree(long[] a) {
        // Allocate four slots per entry, which suffices for a recursive tree.
        n = a.length;
        sum = new long[4 * n];
        mulTag = new long[4 * n];
        addTag = new long[4 * n];
        // Build the tree over the half-open range [0, n).
        build(1, 0, n, a);
    }

    /**
     * Builds node o for the half-open segment [lo, hi).
     * Time: O(n) over the whole build. Space: O(log n) recursion.
     * Invariant: sum[o] is the segment sum and the tag is the identity.
     */
    private void build(int o, int lo, int hi, long[] a) {
        // Every node starts with the identity pair.
        mulTag[o] = 1;
        addTag[o] = 0;
        // A leaf holds one entry.
        if (hi - lo == 1) { sum[o] = a[lo] % M; return; }
        // Split the segment at mid, so the children are [lo, mid) and [mid, hi).
        int mid = (lo + hi) >>> 1;
        build(2 * o, lo, mid, a);
        build(2 * o + 1, mid, hi, a);
        // The parent sum is the sum of the two children.
        sum[o] = (sum[2 * o] + sum[2 * o + 1]) % M;
    }

    /**
     * Applies the map x to b * x + c to the whole segment of node o, which has len entries.
     * Time: O(1). Space: O(1).
     * Invariant: sum[o] is updated and the tag records what children still need.
     */
    private void applyNode(int o, int len, long b, long c) {
        // Each of the len entries becomes b * x + c, so the sum becomes b * sum + c * len.
        sum[o] = (b * sum[o] + c * len) % M;
        // The new tag applies the old tag first and the new pair second.
        addTag[o] = (b * addTag[o] + c) % M;
        mulTag[o] = b * mulTag[o] % M;
    }

    /**
     * Moves the pending pair of node o to both children and resets it.
     * Time: O(1). Space: O(1).
     * Invariant: after the call, o has the identity tag and children hold the full history.
     */
    private void push(int o, int lo, int hi) {
        // Skip the work when the tag is already the identity.
        if (mulTag[o] == 1 && addTag[o] == 0) return;
        // Children cover [lo, mid) and [mid, hi).
        int mid = (lo + hi) >>> 1;
        applyNode(2 * o, mid - lo, mulTag[o], addTag[o]);
        applyNode(2 * o + 1, hi - mid, mulTag[o], addTag[o]);
        // The parent no longer owes anything to its children.
        mulTag[o] = 1;
        addTag[o] = 0;
    }

    /**
     * Applies the map x to b * x + c to every entry in the half-open range [l, r).
     * Time: O(log n). Space: O(log n) recursion.
     * Invariant: sums of visited nodes stay equal to the sums of the true entries.
     */
    void apply(int l, int r, long b, long c) {
        // An empty range changes nothing.
        if (l >= r) return;
        update(1, 0, n, l, r, b, c);
    }

    private void update(int o, int lo, int hi, int l, int r, long b, long c) {
        // A segment fully inside the range takes the pair as a tag and stops.
        if (l <= lo && hi <= r) { applyNode(o, hi - lo, b, c); return; }
        // A partly covered segment pushes first so that children see the older history.
        push(o, lo, hi);
        int mid = (lo + hi) >>> 1;
        // Recurse only into children that overlap [l, r).
        if (l < mid) update(2 * o, lo, mid, l, r, b, c);
        if (r > mid) update(2 * o + 1, mid, hi, l, r, b, c);
        // Rebuild the parent sum from the updated children.
        sum[o] = (sum[2 * o] + sum[2 * o + 1]) % M;
    }

    /**
     * Returns the sum of entries in the half-open range [l, r) modulo M.
     * Time: O(log n). Space: O(log n) recursion.
     * Invariant: pushing before descent keeps children exact for the queried part.
     */
    long sum(int l, int r) {
        // An empty range sums to 0.
        if (l >= r) return 0;
        return query(1, 0, n, l, r);
    }

    private long query(int o, int lo, int hi, int l, int r) {
        // A segment fully inside the range contributes its stored sum.
        if (l <= lo && hi <= r) return sum[o];
        // Push the pending pair so that the children are exact.
        push(o, lo, hi);
        int mid = (lo + hi) >>> 1;
        long total = 0;
        // Add the contribution of each overlapping child.
        if (l < mid) total += query(2 * o, lo, mid, l, r);
        if (r > mid) total += query(2 * o + 1, mid, hi, l, r);
        // Each child result is below M, so the total is reduced once.
        return total % M;
    }

    public static void main(String[] args) {
        // Check Example 1 and Example 2 from the exercise.
        AffineLazySegmentTree t = new AffineLazySegmentTree(new long[] {1, 2, 3, 4});
        t.apply(1, 3, 2, 1);
        if (t.sum(0, 4) != 17) throw new AssertionError("example 1");
        t.apply(0, 4, 0, 9);
        if (t.sum(1, 3) != 18) throw new AssertionError("example 2");
        // Compare against a naive array on random ranges, including empty ranges and b = 0.
        Random rnd = new Random(4);
        for (int round = 0; round < 300; round++) {
            int n = 1 + rnd.nextInt(20);
            long[] naive = new long[n];
            for (int i = 0; i < n; i++) naive[i] = rnd.nextInt(1_000_000_000);
            AffineLazySegmentTree fast = new AffineLazySegmentTree(naive.clone());
            for (int step = 0; step < 60; step++) {
                int l = rnd.nextInt(n + 1), r = rnd.nextInt(n + 1);
                if (l > r) { int tmp = l; l = r; r = tmp; }
                if (rnd.nextBoolean()) {
                    long b = rnd.nextInt(4) == 0 ? 0 : (long) rnd.nextInt(1_000_000_000);
                    long c = rnd.nextInt(1_000_000_000);
                    fast.apply(l, r, b, c);
                    for (int i = l; i < r; i++) naive[i] = (b * naive[i] + c) % M;
                } else {
                    long want = 0;
                    for (int i = l; i < r; i++) want = (want + naive[i]) % M;
                    if (fast.sum(l, r) != want) throw new AssertionError("round " + round + " step " + step);
                }
            }
        }
    }
}
```
