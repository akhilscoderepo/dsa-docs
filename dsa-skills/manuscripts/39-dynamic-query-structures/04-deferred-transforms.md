<!-- lesson-kind: standard -->
<!-- lesson-id: deferred-transforms -->
## Deferred Transforms

<!-- stage: context -->
### Why A Price Change Takes Seconds

A pricing service keeps a list of prices in memory. New prices arrive all day, and an operator sometimes applies a currency correction to every price already stored. The correction adds a fixed amount, or it multiplies every price by a rate. The list holds a million entries, so each correction visits a million slots, and a burst of corrections stalls the service.

The work looks wasteful because the correction is one decision about the whole list, yet the code pays for it once per entry. New prices make it harder. A price that arrives after a correction must not receive that correction, so the list cannot simply hold one global number. This lesson asks how to record a whole-list operation in constant time and still return the correct value of any single entry on demand.

<!-- stage: naive -->
### Updating Every Stored Entry

The direct design stores the values in an array list and applies each whole-list operation by looping over every entry. A new value is appended as it is. A read returns the stored value. Every operation keeps the invariant that each stored value is the current true value.

```java
final class NaiveSequence {
    private static final long MOD = 1_000_000_007L;
    private final java.util.ArrayList<Long> values = new java.util.ArrayList<>();

    void append(long v) { values.add(v % MOD); }

    void addAll(long d) {
        for (int i = 0; i < values.size(); i++)
            values.set(i, (values.get(i) + d) % MOD);
    }

    void multAll(long m) {
        for (int i = 0; i < values.size(); i++)
            values.set(i, values.get(i) * m % MOD);
    }

    long get(int i) { return i < values.size() ? values.get(i) : -1; }
}
```

The design is correct and easy to read. Its cost depends on how many entries exist when a whole-list operation arrives.

<!-- stage: bottleneck -->
### Every Whole List Call Costs Linear Time

```predict
A client appends 50,000 values and then calls addAll 50,000 times. About how many element updates does the naive class perform?

About 2.5 billion, because every addAll call sees all 50,000 entries. That is 50,000 calls times 50,000 entries.
```

Count the element updates. When the list holds `n` entries, each call to `addAll` or `multAll` performs `n` updates, so a single call costs O(n). A workload of `q` calls on a list of `n` entries therefore costs O(n * q). With `n = q = 100,000` that is ten billion updates, which exceeds any reasonable time limit.

The loop is also redundant. Every entry receives the same operation, so the loop repeats one decision `n` times. Reads and appends already cost O(1), so the whole-list calls are the only slow part. The workload here is update heavy, the calls arrive one at a time, and a later call may depend on an earlier answer, so no offline reordering is available. The state must absorb a whole-list operation without touching the entries.

<!-- stage: insight -->
### Store One Transform For All Entries

#### Keep The Operation Once

Instead of changing each entry, keep the operation in one place and apply it only when an entry is read. A pending operation that waits for a read is a **lazy tag**. Whole-list calls update only the tag, so each costs O(1). Reads pay the small price of applying the tag to a single entry.

#### Compose Operations Into A Pair

Adding `d` and multiplying by `m` are both functions of the form `x * mul + add`. A function of this form is an **affine pair** `(mul, add)`. Applying one more operation to a value already transformed by `(mul, add)` produces another pair of the same form. Adding `d` gives `(mul, add + d)`. Multiplying by `m` gives `(mul * m, add * m)`. The pair never grows, so a history of a million operations still fits in two numbers. The product of two operations is their composition, and its order matters because multiplication does not commute with addition.

#### Translate New Values Backwards

<!-- names: lazy tag, affine pair, modular inverse -->

A value `v` appended now must read back as exactly `v`, even though the tag already holds history. The design stores a raw value `x` such that `x * mul + add` equals `v`. Solving gives `x = (v - add) / mul`. Division modulo a prime `M` multiplies by the **modular inverse** of `mul`, which is the number whose product with `mul` leaves remainder 1. Fermat's little theorem gives it as `mul^(M-2) mod M`, computed by fast exponentiation in O(log M). The inverse exists only when `mul` is not a multiple of `M`. That condition is the one weak point of the design, and the Boundary exercise returns to it.

<!-- stage: variables -->
### Name The Stored And Pending Values

Four quantities describe the whole state, and every method reads or writes only these.

- **`M`** is the prime modulus 1,000,000,007, and every stored number lies in `[0, M)`.
- **`x[i]`** is the raw value stored for entry `i` at the moment it was appended.
- **`mul`** is the pending multiplier in the affine pair, and it starts at 1.
- **`add`** is the pending addend in the affine pair, and it starts at 0.

The invariant is that the true value of entry `i` equals `(x[i] * mul + add) mod M` after every call. Indices are zero-based, and an index at or beyond the current size returns -1.

<!-- stage: trace -->
### Follow The Pair Through Updates

#### Trace The Small Example

Start with an empty sequence, so `mul = 1` and `add = 0`. The first append of 2 stores raw value 2, because the pair is the identity. The call addAll(3) changes only the addend to 3, and no entry is touched. The second append is 7. The design must store `x` with `x * 1 + 3 = 7`, so it stores `(7 - 3) * 1 = 4`. The call multAll(2) doubles both parts and leaves `mul = 2` and `add = 6`.

The first read of index 0 computes `2 * 2 + 6 = 10`, which equals `(2 + 3) * 2`. The read of index 1 computes `4 * 2 + 6 = 14`, which equals `(7 + 3) * 2`. No whole-list call ever visited either entry. The read of index 2 returns -1 because only two entries exist. The hardest step is the second append, because it writes a raw value that differs from the visible value.

```trace
{"cells":["0","1","2"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"mul":1,"add":0,"raw":"2","result":""},"note":"append(2) stores raw value (2 - 0) * inverse(1) = 2, so that 2 * 1 + 0 reads back as 2."},{"at":{"i":-1},"vars":{"mul":1,"add":3,"raw":"2","result":""},"note":"addAll(3) changes only the addend, which becomes 3. No entry is touched."},{"at":{"i":1},"vars":{"mul":1,"add":3,"raw":"2,4","result":""},"note":"append(7) stores raw value (7 - 3) * inverse(1) = 4, so that 4 * 1 + 3 reads back as 7."},{"at":{"i":-1},"vars":{"mul":2,"add":6,"raw":"2,4","result":""},"note":"multAll(2) multiplies both parts of the pair, so mul = 2 and add = 6. No entry is touched."},{"at":{"i":0},"vars":{"mul":2,"add":6,"raw":"2,4","result":"10"},"note":"get(0) computes 2 * 2 + 6 mod M = 10, which matches the naive loop."},{"at":{"i":1},"vars":{"mul":2,"add":6,"raw":"2,4","result":"14"},"note":"get(1) computes 4 * 2 + 6 mod M = 14, which matches the naive loop."},{"at":{"i":2},"vars":{"mul":2,"add":6,"raw":"2,4","result":"-1"},"note":"get(2) is at or beyond the size 2, so it returns -1."}]}
```

#### Trace The Modulus Wrap

The second run shows the modulus. Six calls to multAll(100) raise `mul` to 10^12, which wraps to 999993007 modulo `M`, and the later append of 9 needs a true inverse of that residue. The first entry reads 999965007 and the second reads 9, the same values that the naive loop produces.

```trace
{"cells":["0","1"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"mul":1,"add":0,"raw":"5","result":""},"note":"append(5) stores raw value (5 - 0) * inverse(1) = 5, so that 5 * 1 + 0 reads back as 5."},{"at":{"i":-1},"vars":{"mul":100,"add":0,"raw":"5","result":""},"note":"multAll(100) multiplies both parts of the pair, so mul = 100 and add = 0. No entry is touched."},{"at":{"i":-1},"vars":{"mul":10000,"add":0,"raw":"5","result":""},"note":"multAll(100) multiplies both parts of the pair, so mul = 10000 and add = 0. No entry is touched."},{"at":{"i":-1},"vars":{"mul":1000000,"add":0,"raw":"5","result":""},"note":"multAll(100) multiplies both parts of the pair, so mul = 1000000 and add = 0. No entry is touched."},{"at":{"i":-1},"vars":{"mul":100000000,"add":0,"raw":"5","result":""},"note":"multAll(100) multiplies both parts of the pair, so mul = 100000000 and add = 0. No entry is touched."},{"at":{"i":-1},"vars":{"mul":999999937,"add":0,"raw":"5","result":""},"note":"multAll(100) multiplies both parts of the pair, so mul = 999999937 and add = 0. No entry is touched."},{"at":{"i":-1},"vars":{"mul":999993007,"add":0,"raw":"5","result":""},"note":"multAll(100) multiplies both parts of the pair, so mul = 999993007 and add = 0. No entry is touched."},{"at":{"i":1},"vars":{"mul":999993007,"add":0,"raw":"5,326714288","result":""},"note":"append(9) stores raw value (9 - 0) * inverse(999993007) = 326714288, so that 326714288 * 999993007 + 0 reads back as 9."},{"at":{"i":0},"vars":{"mul":999993007,"add":0,"raw":"5,326714288","result":"999965007"},"note":"get(0) computes 5 * 999993007 + 0 mod M = 999965007, which matches the naive loop."},{"at":{"i":1},"vars":{"mul":999993007,"add":0,"raw":"5,326714288","result":"9"},"note":"get(1) computes 326714288 * 999993007 + 0 mod M = 9, which matches the naive loop."}]}
```

<!-- stage: code -->
### Implement The Pair With Fermat Inverse

```java
final class DeferredSequence {
    private static final long M = 1_000_000_007L;
    private final java.util.ArrayList<Long> raw = new java.util.ArrayList<>();
    private long mul = 1;
    private long add = 0;

    private static long power(long base, long exp) {
        long result = 1;
        base %= M;
        while (exp > 0) {
            if ((exp & 1) == 1) result = result * base % M;
            base = base * base % M;
            exp >>= 1;
        }
        return result;
    }

    void append(long v) {
        long shifted = ((v - add) % M + M) % M;
        raw.add(shifted * power(mul, M - 2) % M);
    }

    void addAll(long d) { add = (add + d) % M; }

    void multAll(long m) {
        mul = mul * m % M;
        add = add * m % M;
    }

    long get(int i) {
        if (i >= raw.size()) return -1;
        return (raw.get(i) * mul + add) % M;
    }
}
```

The method `append` first reduces `v - add` into `[0, M)`, because Java `%` keeps the sign of its left operand. It then multiplies by the inverse of `mul`. Every product stays below `M * M`, which is under `2^63`, so `long` never overflows. The class never loops over the list in `addAll` or `multAll`, so those calls cost O(1), while `append` costs O(log M) and `get` costs O(1).

<!-- stage: applicability -->
### Check The Cue And The Limits

#### Spot The Cue

Use this design when new values are appended and some operations affect every value that already exists. The cue is a mix of cheap appends and sweeping updates. The invariant to protect is that each stored raw value and the single pending pair together reproduce the true value of every entry, in the order the operations arrived.

#### Watch The Order And The False Friend

A plain running total of additions looks like enough, and for addition alone it is. Adding multiplication turns that total into a false friend, because a later multiplier must also scale the additions that came before it. The pair handles this by multiplying the addend as well. Order matters, so composing the same two operations in the other order gives a different pair.

#### Know When It Stops Working

The design needs a prime modulus and a nonzero multiplier, since division is replaced by the inverse. It also needs every operation to hit all entries. An operation that affects only a range of entries cannot live in one global pair. That case needs a tag per segment, which the last exercise develops.

<!-- stage: exercises -->
### Exercises

#### [Build] Global Add Sequence (Author exercise)
<!-- id: dq39-global-add-sequence -->

**Prerequisites.** The affine pair of this lesson, used with `mul` fixed at 1.

**Problem.** Design a sequence of `long` values with three operations. `append(v)` adds `v` at the end. `addAll(d)` adds `d` to every value currently in the sequence and does not change values appended later. `get(i)` returns the current value at zero-based index `i`. Use exact `long` arithmetic and no modulus. Each call must run in O(1) time.

**Constraints.** The limits are:
- **Calls** number at most `10^5` in total, and they arrive online one at a time.
- **Update/query ratio** is about 2 to 1, with appends and `addAll` calls outnumbering `get` calls.
- **`v` and `d`** are `long` values with absolute value at most `10^9`.
- **`i`** satisfies `0 <= i < size()`, otherwise `get` throws `IndexOutOfBoundsException`.
- **Sums** stay below `10^15` in absolute value, so `long` is enough.

**Example 1.** Input the calls `append(5)`, `addAll(3)`, `append(10)`, get(0), get(1), output `8, 10`.

**Example 2.** Input the calls of Example 1 followed by `addAll(-4)`, get(0), get(1), output `4, 6`.

**Hint.** What single number records how much was added since the sequence was created? What must a new value subtract so that it reads back unchanged?

**Changed decision.** The loop over entries becomes one stored offset, and new values subtract the offset in force when they arrive.

#### [Vary] Fancy Sequence (LeetCode 1622)
<!-- id: dq39-fancy-sequence -->

**Prerequisites.** The Global Add Sequence exercise above and the modular inverse of this lesson.

**Problem.** Implement a sequence with `append(val)`, `addAll(inc)`, `multAll(m)` and `getIndex(idx)`. `multAll(m)` multiplies every value currently stored by `m`. `getIndex(idx)` returns the value at zero-based index `idx` modulo `1_000_000_007`, or -1 when `idx` is not less than the current size. The three updates apply only to values that exist at the time of the call.

**Constraints.** The limits are:
- **Calls** number at most `10^5`, they arrive online, and no call is known in advance.
- **Update/query ratio** is mixed with no fixed split, so each of the four calls must stay cheap.
- **`val` and `inc`** are integers in `[0, 100]`.
- **`m`** is an integer in `[1, 100]`, so it is never a multiple of the modulus.
- **Return value** is a `long` in `[0, M)` or -1.

**Example 1.** Input the calls `append(2)`, `addAll(3)`, `append(7)`, `multAll(2)`, getIndex(0), getIndex(1), getIndex(2), output `10, 14, -1`.

**Example 2.** Input the calls `append(5)`, `multAll(100)` six times, `append(9)`, getIndex(0), getIndex(1), output `999965007, 9`.

**Hint.** What pair of numbers composes both operations into one? How does a new value find the raw number that reads back as itself?

**Changed decision.** Multiplication joins addition, so the stored state grows from one offset to a pair and appends need a modular inverse.

#### [Boundary] Zero Multiplier (Author exercise)
<!-- id: dq39-zero-multiplier -->

**Prerequisites.** The Fancy Sequence exercise above.

**Problem.** Use the same four calls as Fancy Sequence, but allow `multAll(m)` with `m = 0`. After such a call every value currently stored equals 0 before any later addition. A pending multiplier equal to 0 modulo `1_000_000_007` has no modular inverse, so a design that divides by the running multiplier fails on the next `append`. Design the structure so it never divides by zero, and explain how it resets the pending pair.

**Constraints.** The limits are:
- **Calls** number at most `10^5` and arrive online, with no advance knowledge.
- **Update/query ratio** is about 1 to 1, and every call must stay cheap.
- **`val`, `inc` and `m`** are integers in `[0, M - 1]`, where `M = 1_000_000_007`.
- **Zero multiplier** `m = 0` may occur any number of times and anywhere.
- **Return value** is a `long` in `[0, M)` or -1 for an index at or beyond the size.

**Example 1.** Input the calls `append(4)`, `multAll(0)`, `addAll(6)`, `append(9)`, getIndex(0), getIndex(1), output `6, 9`.

**Example 2.** Input the calls `append(7)`, `append(1)`, `multAll(0)`, `addAll(4)`, `append(3)`, `multAll(5)`, getIndex(0), getIndex(2), output `20, 15`.

**Hint.** After a multiplication by zero, what is the value of every earlier entry, whatever it held before? Could you forget their raw values and restart the pair at the identity?

**Changed decision.** The nonzero guarantee disappears, so a zero multiplier must reset the pair and mark every earlier entry as zero.

#### [Recognize] Affine Lazy Segment Tree (Author exercise)
<!-- id: dq39-affine-lazy-segment-tree -->

**Prerequisites.** The Zero Multiplier exercise above and a segment tree with range sum queries.

**Problem.** Maintain an array `a` of `n` integers modulo `M = 1_000_000_007`. The call `apply(l, r, b, c)` replaces `a[i]` by `(b * a[i] + c) mod M` for every `i` with `l <= i < r`. The call `sum(l, r)` returns the sum of `a[i]` for `l <= i < r`, modulo `M`. Both ranges are half-open, so `r` is excluded and an empty range with `l = r` is allowed. State which fact breaks the single global pair of this lesson and which structure replaces it.

**Constraints.** The limits are:
- **`n`** satisfies `1 <= n <= 10^5`, and the initial values lie in `[0, M)`.
- **Calls** number at most `10^5`, and they arrive online in any order.
- **Update/query ratio** is about 1 to 1, so both calls must cost O(log n).
- **`b` and `c`** are integers in `[0, M - 1]`, and `b = 0` is allowed.
- **Ranges** satisfy `0 <= l <= r <= n`, and sums use `long` arithmetic.

**Example 1.** Input `a = [1, 2, 3, 4]` and the calls `apply(1, 3, 2, 1)`, sum(0, 4), output `17`, because the array becomes `[1, 5, 7, 4]`.

**Example 2.** Input the calls of Example 1 followed by `apply(0, 4, 0, 9)`, sum(1, 3), output `18`, because every entry becomes 9.

**Hint.** A range update leaves some entries unchanged. How can a node store a pending pair for its whole segment and push it down only when a query needs the children?

**Changed decision.** Updates now cover only a range, so one tag per segment replaces the single global pair and tags compose when pushed down.
