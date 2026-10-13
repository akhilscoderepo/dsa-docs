<!-- solutions-for: 03-online-prefixes -->
### Solutions For Online Prefixes

#### Solution: [Build] Product Prefix Stream (Author exercise)
<!-- id: st38-product-prefix-stream -->

**Approach.**
The class stores `p`, where `p[i]` is the product of the first `i` appended values and `p[0]` is 1. An append multiplies the newest stored product by the value and writes the result in the next slot. A query for the newest `k` values reads `p[n]` and `p[n - k]` and divides. The division is exact because `p[n]` equals `p[n - k]` times the wanted product, and it never divides by zero because every value is at least 1. The limits keep `p[n]` at most 9^18, which is below 2^63, so `long` holds every stored number.

The program replays the examples, then compares the class with a loop over the newest `k` values on random streams. It also checks that the largest allowed stored product fits in a `long`.

**Complexity.**
- **Time** is O(1) per append and per query, since each call performs one multiplication or one division.
- **Space** is O(n) for the `n` stored products.

```java run
import java.util.Random;

public final class ProductPrefixBuild {
    static final class ProductStream {
        private final long[] p = new long[19];   // p[i] is the product of the first i values
        private int n;                           // number of values appended

        ProductStream() {
            // The empty product is 1, so a query for all values needs no special case.
            p[0] = 1;
        }

        /**
         * Appends one value.
         * Time: O(1). Space: O(1) beyond the stored slot.
         * Invariant: p[n] equals the product of all appended values.
         */
        void append(int v) {
            // One multiplication extends the previous product by one step.
            p[n + 1] = p[n] * v;
            // The count moves only after the slot is written.
            n++;
        }

        /**
         * Returns the product of the newest k values.
         * Time: O(1). Space: O(1).
         * Invariant: p[n] = p[n - k] * answer, so the division has no remainder.
         */
        long last(int k) {
            // Both stored products come from one array, and the divisor is at least 1.
            return p[n] / p[n - k];
        }
    }

    /** Multiplies the newest k values by a loop, used as the oracle. */
    static long brute(int[] vals, int count, int k) {
        long r = 1;
        // Walks exactly the k newest positions.
        for (int i = count - k; i < count; i++) r *= vals[i];
        return r;
    }

    public static void main(String[] args) {
        // Example 1: values 2, 3, 4.
        ProductStream a = new ProductStream();
        a.append(2); a.append(3); a.append(4);
        if (a.last(2) != 12 || a.last(3) != 24) throw new AssertionError("example 1");
        // Example 2: values 5, 1, 7, 2.
        ProductStream b = new ProductStream();
        b.append(5); b.append(1); b.append(7); b.append(2);
        if (b.last(1) != 2 || b.last(4) != 70 || b.last(3) != 14) throw new AssertionError("example 2");
        // The largest allowed total, 18 nines, fits in a long.
        ProductStream big = new ProductStream();
        for (int i = 0; i < 18; i++) big.append(9);
        long nines = 1;
        for (int i = 0; i < 18; i++) nines *= 9;
        if (big.last(18) != nines || nines <= 0) throw new AssertionError("width");
        // Random streams compare every query with the loop oracle.
        Random rnd = new Random(3801L);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(18);
            int[] vals = new int[n];
            ProductStream s = new ProductStream();
            for (int i = 0; i < n; i++) {
                vals[i] = 1 + rnd.nextInt(9);
                s.append(vals[i]);
                int k = 1 + rnd.nextInt(i + 1);
                if (s.last(k) != brute(vals, i + 1, k)) throw new AssertionError("random query");
            }
        }
    }
}
```

#### Solution: [Vary] Product of the Last K Numbers (LeetCode 1352)
<!-- id: st38-product-last-k-reset -->

**Approach.**
The class keeps the stored products of the values after the latest zero, starting from the empty product 1. A nonzero value multiplies the newest stored product and appends the result. A zero has no inverse and also turns every later product into zero, so the class clears the list back to the single value 1. For `getProduct(k)`, the list holds `size - 1` values since the zero. When `k` is larger than that count, the range contains the zero and the answer is 0. Otherwise the answer is the newest stored product divided by the stored product `k` slots earlier, and the division is exact because both lie after the zero.

The program replays both examples and then compares the class with a loop over the whole stream on random sequences that contain many zeros.

**Complexity.**
- **Time** is O(1) amortized per call, because a clear discards stored values that each earlier add paid for once.
- **Space** is O(n) for the values since the latest zero.

```java run
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public final class ProductLastKVary {
    static final class ProductOfNumbers {
        private final List<Long> stored = new ArrayList<>();   // products of the values after the latest zero

        ProductOfNumbers() {
            // The empty product 1 anchors every division.
            stored.add(1L);
        }

        /**
         * Appends one number.
         * Time: O(1) amortized. Space: O(1) amortized.
         * Invariant: stored holds 1 followed by the running products since the latest zero.
         */
        void add(int num) {
            // A zero ends the useful history, so the list restarts from the empty product.
            if (num == 0) {
                stored.clear();
                stored.add(1L);
            } else {
                // A nonzero value extends the newest product by one step.
                stored.add(stored.get(stored.size() - 1) * num);
            }
        }

        /**
         * Returns the product of the newest k numbers.
         * Time: O(1). Space: O(1).
         * Invariant: the list has size - 1 entries after the latest zero.
         */
        long getProduct(int k) {
            int size = stored.size();
            // More entries requested than the list holds means the range includes the zero.
            if (k > size - 1) return 0;
            // Both stored products lie after the zero, so the quotient is exact.
            return stored.get(size - 1) / stored.get(size - 1 - k);
        }
    }

    public static void main(String[] args) {
        // Example 1: a zero sits inside the range of the second query.
        ProductOfNumbers a = new ProductOfNumbers();
        for (int v : new int[]{6, 2, 0, 5, 4}) a.add(v);
        if (a.getProduct(2) != 20 || a.getProduct(3) != 0 || a.getProduct(1) != 4) throw new AssertionError("example 1");
        // Example 2: queries before and after a zero.
        ProductOfNumbers b = new ProductOfNumbers();
        b.add(7); b.add(3); b.add(2);
        if (b.getProduct(3) != 42) throw new AssertionError("example 2 first");
        b.add(0); b.add(4);
        if (b.getProduct(2) != 0) throw new AssertionError("example 2 zero");
        b.add(5);
        if (b.getProduct(2) != 20 || b.getProduct(3) != 0) throw new AssertionError("example 2 end");
        // Random streams with frequent zeros compare with a full loop.
        Random rnd = new Random(3802L);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(14);
            int[] vals = new int[n];
            ProductOfNumbers s = new ProductOfNumbers();
            for (int i = 0; i < n; i++) {
                vals[i] = rnd.nextInt(4) == 0 ? 0 : 1 + rnd.nextInt(6);
                s.add(vals[i]);
                int k = 1 + rnd.nextInt(i + 1);
                long expect = 1;
                for (int j = i + 1 - k; j <= i; j++) expect *= vals[j];
                if (s.getProduct(k) != expect) throw new AssertionError("random query");
            }
        }
    }
}
```

#### Solution: [Boundary] Overflow Contract (Author exercise)
<!-- id: st38-overflow-contract -->

**Approach.**
The class stores two arrays. The array `pre[i]` holds the product of the first `i` values modulo `1000000007`, and `inv[i]` holds the modular inverse of `pre[i]`. Each append multiplies by the value for `pre` and by the inverse of the value for `inv`. The inverse of a single value comes from Fermat's little theorem, `v^(M - 2) mod M`, because `M` is prime and no value is a multiple of `M`. A query returns `pre[n] * inv[n - k] mod M`, which equals the product of the newest `k` values because `pre[n] = pre[n - k] * answer`.

The width is the contract. Each stored residue is below `M`, which fits in an `int`, but the product of two residues reaches about 10^18, which needs a `long`. An `int` product would wrap. The program shows the wrap on 10^9 times 10^9 and then compares the class with a `BigInteger` oracle on random streams of large values.

**Complexity.**
- **Time** is O(log M) per append for the modular power and O(1) per query, where `M` is the modulus.
- **Space** is O(n) for the two stored arrays.

```java run
import java.math.BigInteger;
import java.util.Random;

public final class OverflowContractBoundary {
    static final long MOD = 1_000_000_007L;

    static final class ModProductStream {
        private final long[] pre = new long[100_001];   // pre[i] is the product of the first i values modulo MOD
        private final long[] inv = new long[100_001];   // inv[i] is the modular inverse of pre[i]
        private int n;                                  // number of values appended

        ModProductStream() {
            // The empty product and its inverse are both 1.
            pre[0] = 1;
            inv[0] = 1;
        }

        /**
         * Computes base^exp modulo MOD by repeated squaring.
         * Time: O(log exp). Space: O(1).
         * Invariant: result * base^exp stays equal to the original power.
         */
        private static long power(long base, long exp) {
            long result = 1;
            base %= MOD;
            // Each pass handles one bit of the exponent.
            while (exp > 0) {
                // A set bit multiplies the result; both factors are below MOD, so the product fits in a long.
                if ((exp & 1) == 1) result = result * base % MOD;
                // Squaring moves to the next bit.
                base = base * base % MOD;
                exp >>= 1;
            }
            return result;
        }

        /**
         * Appends one value.
         * Time: O(log MOD). Space: O(1) beyond the stored slots.
         * Invariant: pre[i] * inv[i] % MOD == 1 for every i up to n.
         */
        void append(int v) {
            // The widening to long happens before the multiplication.
            pre[n + 1] = pre[n] * v % MOD;
            // The inverse of v is v^(MOD - 2) by Fermat's little theorem.
            inv[n + 1] = inv[n] * power(v, MOD - 2) % MOD;
            n++;
        }

        /**
         * Returns the product of the newest k values modulo MOD.
         * Time: O(1). Space: O(1).
         * Invariant: pre[n] = pre[n - k] * answer modulo MOD.
         */
        int product(int k) {
            // Multiplying by the stored inverse plays the role of division.
            return (int) (pre[n] * inv[n - k] % MOD);
        }
    }

    public static void main(String[] args) {
        // Example 1: 10^9 and 999999999 are -7 and -8 modulo MOD.
        ModProductStream a = new ModProductStream();
        a.append(1_000_000_000); a.append(999_999_999); a.append(3);
        if (a.product(2) != 999_999_983 || a.product(3) != 168 || a.product(1) != 3) throw new AssertionError("example 1");
        // Example 2: the newest two values are 10^9 and 5.
        ModProductStream b = new ModProductStream();
        b.append(7); b.append(1_000_000_000); b.append(1_000_000_000); b.append(5);
        if (b.product(2) != 999_999_972 || b.product(3) != 245 || b.product(4) != 1715) throw new AssertionError("example 2");
        // An int product of two large values wraps, while the long product keeps the true value.
        int wrapped = 1_000_000_000 * 1_000_000_000;
        long exact = 1_000_000_000L * 1_000_000_000L;
        if (wrapped == exact || exact != 1_000_000_000_000_000_000L || wrapped >= 0) throw new AssertionError("width demonstration");
        // Random streams of large values compare with a BigInteger product of the newest k values.
        Random rnd = new Random(3803L);
        BigInteger mod = BigInteger.valueOf(MOD);
        for (int t = 0; t < 400; t++) {
            int n = 1 + rnd.nextInt(12);
            int[] vals = new int[n];
            ModProductStream s = new ModProductStream();
            for (int i = 0; i < n; i++) {
                vals[i] = rnd.nextInt(3) == 0 ? 1 + rnd.nextInt(5) : 1_000_000_000 - rnd.nextInt(1000);
                s.append(vals[i]);
                int k = 1 + rnd.nextInt(i + 1);
                BigInteger expect = BigInteger.ONE;
                for (int j = i + 1 - k; j <= i; j++) expect = expect.multiply(BigInteger.valueOf(vals[j]));
                if (s.product(k) != expect.mod(mod).intValueExact()) throw new AssertionError("random query");
            }
        }
    }
}
```

#### Solution: [Recognize] Online Stock Span (LeetCode 901)
<!-- id: st38-stock-span-stream -->

**Approach.**
Subtraction cannot produce a span, because "the nearest earlier price above this one" has no inverse. The class keeps a stack of pairs, a price and the number of days it covers. The stack holds prices in strictly decreasing order from bottom to top, and the spans of its entries add up to the number of days so far. A new price starts with span 1. While the top entry has a price at most the new price, the class pops it and adds its span to the new span, because every day that top entry covered also has a price at most the new one. The class then pushes the new pair. The invariant is that the stack order stays strictly decreasing, so the entry below the new top is the nearest earlier price strictly above it.

Each price is pushed once and popped at most once, so a sequence of `m` calls does O(m) work in total. The program replays both examples and compares with a backward scan on random price streams with many ties.

**Complexity.**
- **Time** is O(1) amortized per call, because the total number of pops over `m` calls is at most `m`.
- **Space** is O(m) in the worst case of strictly decreasing prices, since nothing is popped.

```java run
import java.util.Random;

public final class StockSpanRecognize {
    static final class StockSpanner {
        private final int[] prices = new int[10_001];   // stack of prices, strictly decreasing from bottom to top
        private final int[] spans = new int[10_001];    // days covered by each stacked price
        private int size;                               // number of stacked pairs

        /**
         * Appends a price and returns its span.
         * Time: O(1) amortized. Space: O(1) amortized.
         * Invariant: stacked prices strictly decrease, and the spans add up to the days seen.
         */
        int next(int price) {
            int span = 1;
            // Pops every older price that is at most the new price.
            while (size > 0 && prices[size - 1] <= price) {
                // The popped entry covers days whose prices are also at most the new price.
                span += spans[size - 1];
                size--;
            }
            // The new pair keeps the stack strictly decreasing.
            prices[size] = price;
            spans[size] = span;
            size++;
            return span;
        }
    }

    public static void main(String[] args) {
        // Example 1: ties and a drop in the sequence.
        StockSpanner a = new StockSpanner();
        int[] in1 = {31, 41, 41, 26, 59, 53};
        int[] out1 = {1, 2, 3, 1, 5, 1};
        for (int i = 0; i < in1.length; i++) if (a.next(in1[i]) != out1[i]) throw new AssertionError("example 1 at " + i);
        // Example 2: a long rising tail.
        StockSpanner b = new StockSpanner();
        int[] in2 = {8, 6, 6, 7, 9, 3, 10};
        int[] out2 = {1, 1, 2, 3, 5, 1, 7};
        for (int i = 0; i < in2.length; i++) if (b.next(in2[i]) != out2[i]) throw new AssertionError("example 2 at " + i);
        // Random streams with a small price range create many ties and compare with a backward scan.
        Random rnd = new Random(3804L);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(20);
            int[] vals = new int[n];
            StockSpanner s = new StockSpanner();
            for (int i = 0; i < n; i++) {
                vals[i] = 1 + rnd.nextInt(6);
                int expect = 1;
                for (int j = i - 1; j >= 0 && vals[j] <= vals[i]; j--) expect++;
                if (s.next(vals[i]) != expect) throw new AssertionError("random span");
            }
        }
    }
}
```
