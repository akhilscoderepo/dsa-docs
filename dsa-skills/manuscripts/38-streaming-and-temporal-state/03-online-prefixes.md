<!-- lesson-kind: standard -->
<!-- lesson-id: online-prefixes -->
## Online Prefixes

<!-- stage: context -->
### Why A Traffic Meter Falls Behind

A hosting company shows each customer a dashboard with the bytes served for the last `k` requests. The server appends one number per request, and the dashboard asks for the total of the newest `k` entries on every refresh. At launch the numbers look right. A year later two complaints arrive on the same day. Large customers see the dashboard freeze, because every refresh adds up 200000 numbers and 500 refreshes arrive each second. One customer sees a negative traffic total, because the sum was stored in a 32-bit `int` and wrapped past 2147483647.

The data has a property that the first design ignores. The stream is append-only: a recorded size never changes and never expires, and new entries only arrive at the end. Every query asks about the same kind of range, the newest `k` entries. This lesson asks how a program can answer such a query without touching those `k` entries again, and which kinds of values allow it.

<!-- stage: naive -->
### Adding Up The Newest Entries

The direct design stores every size in a list. A query walks the last `k` positions and adds them. The class below follows the dashboard exactly, including the 32-bit total.

```java
final class NaiveByteMeter {
    private final java.util.ArrayList<Integer> sizes = new java.util.ArrayList<>();

    void record(int bytes) { sizes.add(bytes); }

    int lastTotal(int k) {
        int total = 0;
        for (int i = sizes.size() - k; i < sizes.size(); i++) total += sizes.get(i);   // touches k entries
        return total;
    }
}
```

After the calls `record(5)`, `record(3)`, `record(8)`, the call `lastTotal(2)` returns 11. On small tests the class is correct and quick to write.

```predict
A meter records 200000 sizes of 100000 bytes each, and then lastTotal(200000) runs once for every one of 500 dashboard refreshes in a second. What does one call return, and how many additions does the second cost?

The true total is 20000000000, which does not fit in an int. The sum wraps and the call returns -1474836480. Each call performs 200000 additions, so 500 refreshes cost 10^8 additions in one second, and a customer with more history makes it worse. The class is slow and wrong for the same input.
```

<!-- stage: bottleneck -->
### Repeated Sums Over The Same Entries

A query for the newest `k` entries costs O(k) time. Two refreshes one second apart cover almost the same entries, yet the second refresh adds them from scratch. Of the 200000 entries in the window, only a handful are new since the previous refresh, and the program learns nothing from the first sum. For `q` queries over a stream of `n` entries, the total cost is O(q * k), which reaches 10^10 additions when `q` and `k` are both about 10^5.

The `int` total is a second weakness, and it hides inside the same loop. A stream of `n` entries with sizes up to `M` produces totals up to `n * M`. Storing that value in an `int` fails as soon as the product passes 2^31 - 1, which takes only 21475 entries of 100000 bytes.

A better design must therefore answer the query in time that does not depend on `k`. It must reuse the work from earlier appends instead of recomputing it. It must also use a number type wide enough for the largest total the constraints allow.

<!-- stage: insight -->
### Subtract Two Stored Totals

#### One Stored Total Per Position

<!-- names: prefix, inverse, reset -->

A **prefix** total is the sum of the first `i` entries, stored once at the moment entry `i` arrives. Each append computes the new prefix total from the previous one with a single addition, so an append costs O(1) time. The array `sums` holds `sums[0] = 0` for the empty stream and `sums[i]` for the first `i` entries. The newest `k` entries are the entries from position `n - k` up to `n - 1`, and their total is `sums[n] - sums[n - k]`. The query reads two numbers and subtracts, so it costs O(1) time no matter how large `k` is.

#### Why Subtraction Is Allowed

The subtraction works because addition has an **inverse**: subtracting `x` undoes adding `x`. The stored total `sums[n]` equals the wanted total plus `sums[n - k]`, and removing the second term leaves the first. Any operation with an inverse allows the same plan. A product has the inverse of division, so a stream of positive multipliers answers "product of the newest `k`" as `P[n] / P[n - k]`, where `P[i]` is the product of the first `i` entries. Division is exact here, because `P[n]` is `P[n - k]` times the wanted product.

#### A Reset Restores The Inverse

The inverse fails when the value has no inverse. Division by zero is undefined, and a zero entry also makes every later stored product zero, so the stored numbers no longer carry information about earlier entries. A **reset** repairs this. When a zero arrives, the stream discards all stored products and starts again from the empty product 1. A query that asks for more entries than the stream holds since the last reset includes the zero, so its answer is 0.

#### Append-Only Is The Condition

This plan needs the stream to be append-only. A stored total includes every earlier entry, so changing or expiring entry `j` would change every `sums[i]` with `i > j`. The stored numbers would cost O(n) to repair. The invariant of this method is that `sums[i]` always equals the fold of the first `i` entries, and each new entry extends that fold by exactly one step.

<!-- stage: variables -->
### Fields Behind Both Streams

The lesson uses two small classes. The trace follows the first fields of each.

- **sums** is the `long` array of stored totals, with `sums[0] = 0`.
- **n** is the number of entries recorded so far, and `sums[n]` is the total of all of them.
- **k** is the number of newest entries a query asks for, from 1 to `n`.
- **products** is the `long` array of stored products, where the empty product 1 sits in slot `base`.
- **base** is the slot that holds the empty product after the latest zero.
- **last** is the index of the newest entry in the traces, so it equals `n - 1` and is -1 before any entry.
- **top** is the slot of the product of every entry since that zero, so `top - base` counts those entries.

The invariant for sums is `sums[i] = entry 0 + ... + entry i - 1` for every `i` from 0 to `n`. The invariant for products is the same statement with multiplication, restricted to the entries after the last zero.

<!-- stage: trace -->
### Following Totals And Products

#### Stored Totals Answer Two Queries

The first trace records the sizes 5, 3, 8, 2 and 6. The pointer `last` marks the index of the newest recorded entry. After the first three appends, the stored totals are 0, 5, 8 and 16. The query for the newest 2 entries computes `sums[3] - sums[1]`, which is 16 - 5 = 11, and that equals 3 + 8. Two more appends bring the stored total to 24. The query for the newest 4 entries computes `sums[5] - sums[1]`, which is 24 - 5 = 19. The query for all 5 entries uses `sums[0] = 0` and returns 24. Every answer takes one subtraction, and the appends never revisit earlier entries.

```trace
{"cells":["5","3","8","2","6"],"pointers":["last"],"steps":[{"at":{"last":-1},"vars":{"sums":"[0]","call":"new","result":"none"},"note":"Start: no entry is recorded, so sums holds only the empty total 0."},{"at":{"last":0},"vars":{"sums":"[0, 5]","call":"record(5)","result":"none"},"note":"record adds 5 to the last stored total and stores 5."},{"at":{"last":1},"vars":{"sums":"[0, 5, 8]","call":"record(3)","result":"none"},"note":"record adds 3 to the last stored total and stores 8."},{"at":{"last":2},"vars":{"sums":"[0, 5, 8, 16]","call":"record(8)","result":"none"},"note":"record adds 8 to the last stored total and stores 16."},{"at":{"last":2},"vars":{"sums":"[0, 5, 8, 16]","call":"lastTotal(2)","result":"11"},"note":"lastTotal(2) computes sums[3] - sums[1] = 16 - 5 = 11, which equals 3 + 8."},{"at":{"last":3},"vars":{"sums":"[0, 5, 8, 16, 18]","call":"record(2)","result":"none"},"note":"record adds 2 to the last stored total and stores 18."},{"at":{"last":4},"vars":{"sums":"[0, 5, 8, 16, 18, 24]","call":"record(6)","result":"none"},"note":"record adds 6 to the last stored total and stores 24."},{"at":{"last":4},"vars":{"sums":"[0, 5, 8, 16, 18, 24]","call":"lastTotal(4)","result":"19"},"note":"lastTotal(4) computes sums[5] - sums[1] = 24 - 5 = 19."},{"at":{"last":4},"vars":{"sums":"[0, 5, 8, 16, 18, 24]","call":"lastTotal(5)","result":"24"},"note":"lastTotal(5) computes sums[5] - sums[0] = 24 - 0 = 24, the total of all entries."}]}
```

#### A Zero Resets The Stored Products

The second trace records the multipliers 4, 3, 0, 5, 2 and 6. The pointer `last` marks the index of the newest entry, and the pointer `zero` marks the position of the latest zero, or -1 before any zero. The first two entries store the products 1, 4 and 12, and the query for 2 entries returns 12 / 1 = 12. The zero arrives, the stored list shrinks back to the single value 1, and `zero` moves to position 2. The entries 5, 2 and 6 rebuild the list as 1, 5, 10 and 60. A query for 3 entries returns 60 / 1 = 60. A query for 2 entries returns 60 / 5 = 12. A query for 4 entries asks for more than the three entries since the zero, so it returns 0 without any division.

```trace
{"cells":["4","3","0","5","2","6"],"pointers":["last","zero"],"steps":[{"at":{"last":-1,"zero":-1},"vars":{"products":"[1]","call":"new","result":"none"},"note":"Start: no entry is recorded and the list holds the empty product 1."},{"at":{"last":0,"zero":-1},"vars":{"products":"[1, 4]","call":"record(4)","result":"none"},"note":"record multiplies the last stored product by 4 and stores 4."},{"at":{"last":1,"zero":-1},"vars":{"products":"[1, 4, 12]","call":"record(3)","result":"none"},"note":"record multiplies the last stored product by 3 and stores 12."},{"at":{"last":1,"zero":-1},"vars":{"products":"[1, 4, 12]","call":"lastProduct(2)","result":"12"},"note":"lastProduct(2) computes 12 / 1 = 12, which equals 4 * 3."},{"at":{"last":2,"zero":2},"vars":{"products":"[1]","call":"record(0)","result":"none"},"note":"A zero has no inverse, so record discards the list and keeps only the empty product 1. The pointer zero moves here."},{"at":{"last":3,"zero":2},"vars":{"products":"[1, 5]","call":"record(5)","result":"none"},"note":"record multiplies the last stored product by 5 and stores 5."},{"at":{"last":4,"zero":2},"vars":{"products":"[1, 5, 10]","call":"record(2)","result":"none"},"note":"record multiplies the last stored product by 2 and stores 10."},{"at":{"last":5,"zero":2},"vars":{"products":"[1, 5, 10, 60]","call":"record(6)","result":"none"},"note":"record multiplies the last stored product by 6 and stores 60."},{"at":{"last":5,"zero":2},"vars":{"products":"[1, 5, 10, 60]","call":"lastProduct(3)","result":"60"},"note":"lastProduct(3) computes 60 / 1 = 60, which equals 5 * 2 * 6."},{"at":{"last":5,"zero":2},"vars":{"products":"[1, 5, 10, 60]","call":"lastProduct(2)","result":"12"},"note":"lastProduct(2) computes 60 / 5 = 12, which equals 2 * 6."},{"at":{"last":5,"zero":2},"vars":{"products":"[1, 5, 10, 60]","call":"lastProduct(4)","result":"0"},"note":"Four entries reach back to the zero, since only three entries follow it, so the answer is 0 without any division."}]}
```

<!-- stage: code -->
### Two Streams With Stored Totals

#### The Byte Meter

The meter keeps a growing `long` array and the count `n`. The array doubles when it fills, so appends cost O(1) amortized time.

```java
final class ByteMeter {
    private long[] sums = new long[8];     // sums[i] is the total of the first i sizes
    private int n;                         // number of sizes recorded

    void record(long bytes) {
        if (n + 1 == sums.length) sums = java.util.Arrays.copyOf(sums, sums.length * 2);   // grow, amortized O(1)
        sums[n + 1] = sums[n] + bytes;                                                    // extend the total by one step
        n++;
    }

    long lastTotal(int k) {
        if (k < 1 || k > n) throw new IllegalArgumentException("k out of range");
        return sums[n] - sums[n - k];                                                     // two reads and one subtraction
    }
}
```

#### The Growth Factor With A Reset

The growth tracker stores multipliers as `long` values. The field `base` is the array slot that holds the empty product after the latest zero, so a reset moves one index and copies nothing.

```java
final class GrowthTracker {
    private long[] products = new long[8];
    private int base;           // slot of the empty product after the latest zero
    private int top;            // slot of the product of every entry since that zero

    GrowthTracker() { products[0] = 1; }

    void record(int factor) {
        if (factor == 0) {                                  // a zero has no inverse, so history ends here
            base = top + 1;
            top = base;
            ensure(top);
            products[top] = 1;                              // the empty product starts the new history
            return;
        }
        top++;
        ensure(top);
        products[top] = products[top - 1] * factor;         // extend the product by one step
    }

    long lastProduct(int k) {
        if (k > top - base) return 0;                       // the range reaches back to a zero
        return products[top] / products[top - k];           // exact division, because both slots lie after the zero
    }

    private void ensure(int slot) {
        if (slot >= products.length) products = java.util.Arrays.copyOf(products, products.length * 2);   // amortized O(1)
    }
}
```

#### Cost

- **ByteMeter** costs O(1) amortized time per record, O(1) time per query and O(n) space for the stored totals.
- **GrowthTracker** costs O(1) amortized time per record, O(1) time per query and O(n) space, including slots from before a zero.

<!-- stage: applicability -->
### When Stored Totals Answer Queries

#### Recognizing The Pattern

Use this method when entries only arrive and never change, and each query asks for a fold over the newest `k` entries or over any range. Before coding, name the fold, check that it has an inverse, and decide what happens at a zero or another value that destroys the inverse. Then choose the number type from the largest stored total, not from the largest single entry. The invariant to keep is that every stored number equals the fold of everything before its position, and an append extends it by one step.

#### A False Friend

The maximum of the newest `k` entries looks like the same query, and it is a false friend of stored totals. A maximum has no inverse, because knowing the maximum of the first `n` entries and of the first `n - k` entries does not reveal the maximum of the last `k`. That query needs a structure that keeps only candidates, which the stock span exercise below builds. A second false friend is a stored product over values that may be zero, if the code divides without a reset.

#### When The Method Does Not Apply

If entries change after they arrive, every stored number after the changed position is wrong, and a binary indexed tree, covered in chapter 31, fits better. If entries expire by timestamp and the question concerns the live ones, the expiry lessons of this chapter apply. If the totals can exceed the widest primitive type and no modulus is stated, the stored numbers need arbitrary-precision arithmetic, which changes the cost of each step.

<!-- stage: exercises -->
### Exercises

#### [Build] Product Prefix Stream (Author exercise)
<!-- id: st38-product-prefix-stream -->

**Prerequisites.** The stored totals and the division rule from this lesson. The stream is append-only and every value is positive.

**Problem.** Design the class `ProductStream` with a no-argument constructor. The method `append(v)` adds the integer `v` to the end of the stream. The method `last(k)` returns the product of the newest `k` appended integers as a `long`. The class never loops over `k` entries when `last` runs.

**Constraints.** The limits are:
- **Values** `v` are integers from 1 to 9.
- **Appends** number at most 18 per object.
- **Query** `k` satisfies 1 <= k <= the number of values appended so far.
- **Result** of `last` fits in a `long` for every allowed call.

**Example 1.** Input calls `["ProductStream","append","append","append","last","last"]` with arguments `[[],[2],[3],[4],[2],[3]]`, output `[null,null,null,null,12,24]`.

**Example 2.** Input calls `["ProductStream","append","append","append","append","last","last","last"]` with arguments `[[],[5],[1],[7],[2],[1],[4],[3]]`, output `[null,null,null,null,null,2,70,14]`.

**Hint.** Which value does the stored list start with, so that a query for all entries needs no special case?

**Changed decision.** Basic case: the stored fold is a product, division replaces subtraction, and positivity guarantees that every division is exact and safe.

#### [Vary] Product of the Last K Numbers (LeetCode 1352)
<!-- id: st38-product-last-k-reset -->

**Prerequisites.** The Product Prefix Stream exercise above. This exercise changes the values: zero is now allowed.

**Problem.** Design the class `ProductOfNumbers` with a no-argument constructor. The method `add(num)` appends the integer `num`. The method `getProduct(k)` returns the product of the newest `k` appended integers. The class must answer `getProduct` without a loop over `k` entries.

**Constraints.** The limits are:
- **Values** `num` are integers from 0 to 100.
- **Calls** number at most 4 * 10^4 per object.
- **Query** `k` satisfies 1 <= k <= the number of values added so far.
- **Result** of every `getProduct` call fits in a 32-bit signed integer.

**Example 1.** Input calls `["ProductOfNumbers","add","add","add","add","add","getProduct","getProduct","getProduct"]` with arguments `[[],[6],[2],[0],[5],[4],[2],[3],[1]]`, output `[null,null,null,null,null,null,20,0,4]`.

**Example 2.** Input calls `["ProductOfNumbers","add","add","add","getProduct","add","add","getProduct","add","getProduct","getProduct"]` with arguments `[[],[7],[3],[2],[3],[0],[4],[2],[5],[2],[3]]`, output `[null,null,null,null,42,null,null,0,null,20,0]`.

**Hint.** After a zero arrives, which stored numbers still help, and which query sizes can reach back to the zero?

**Changed decision.** A zero has no inverse, so the stored list is discarded when a zero arrives and a query that reaches back to that zero returns 0 directly.

#### [Boundary] Overflow Contract (Author exercise)
<!-- id: st38-overflow-contract -->

**Prerequisites.** The Product of the Last K Numbers exercise above. This exercise changes the answer to a remainder and fixes the number width.

**Problem.** Design the class `ModProductStream` with a no-argument constructor. The method `append(v)` adds the integer `v`. The method `product(k)` returns the product of the newest `k` appended integers, taken modulo `1000000007`. The result is an `int` between 0 and 1000000006. The class answers `product` without a loop over `k` entries.

**Constraints.** The limits are:
- **Values** `v` are integers from 1 to 10^9.
- **Calls** number at most 10^5 per object.
- **Query** `k` satisfies 1 <= k <= the number of values appended so far.
- **Modulus** is the prime 1000000007, and no value is a multiple of it.

**Example 1.** Input calls `["ModProductStream","append","append","append","product","product","product"]` with arguments `[[],[1000000000],[999999999],[3],[2],[3],[1]]`, output `[null,null,null,null,999999983,168,3]`.

**Example 2.** Input calls `["ModProductStream","append","append","append","append","product","product","product"]` with arguments `[[],[7],[1000000000],[1000000000],[5],[2],[3],[4]]`, output `[null,null,null,null,null,999999972,245,1715]`.

**Hint.** Which intermediate value is the largest, the answer or a product of two stored numbers, and what primitive type must hold it? A **modular inverse** of `a` is a number `b` with `a * b` leaving remainder 1 after division by the modulus. For the prime 1000000007, Fermat's little theorem gives `b = a^(1000000005) mod 1000000007`, which fast exponentiation computes in about 30 steps.

**Changed decision.** Division is no longer exact integer division. The stored list divides by multiplying with a modular inverse, and every product of two residues needs a `long` even though each residue fits in an `int`.

#### [Recognize] Online Stock Span (LeetCode 901)
<!-- id: st38-stock-span-stream -->

**Prerequisites.** The Overflow Contract exercise above. This exercise has no inverse operation, so stored totals do not apply.

**Problem.** Design the class `StockSpanner` with a no-argument constructor. The method `next(price)` appends the integer `price` as the newest daily price. It returns the span of that day: the number of consecutive days that end on the newest day and whose prices are all less than or equal to `price`. The newest day counts, so the span is at least 1.

**Constraints.** The limits are:
- **Prices** are integers from 1 to 10^5.
- **Calls** number at most 10^4 per object.
- **Ties** are included: an earlier price equal to the newest price belongs to the span.

**Example 1.** Input calls `["StockSpanner","next","next","next","next","next","next"]` with arguments `[[],[31],[41],[41],[26],[59],[53]]`, output `[null,1,2,3,1,5,1]`.

**Example 2.** Input calls `["StockSpanner","next","next","next","next","next","next","next"]` with arguments `[[],[8],[6],[6],[7],[9],[3],[10]]`, output `[null,1,1,2,3,5,1,7]`.

**Hint.** When a new price is at least as large as an older price, can the older price ever matter to a later span on its own?

**Changed decision.** The answer is a distance back to the nearest strictly greater price, which no inverse can produce. A stack of price and span pairs replaces the stored array, and each price enters and leaves the stack once.
