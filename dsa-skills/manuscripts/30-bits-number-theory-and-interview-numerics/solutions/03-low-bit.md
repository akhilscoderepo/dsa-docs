<!-- solutions-for: 03-low-bit -->
### Solutions For Low Bit

#### Solution: [Build] Clear One Set Bit (Author exercise)
<!-- id: bt03-clear-low-bits -->

**Approach.** The loop applies the clear step at most `k` times and stops at 0.

The expression `x & (x - 1)` copies every bit above the lowest set bit, because `x` and `x - 1` agree there. At the lowest set bit and below, the two operands hold complementary bits, so the AND gives 0. Each round therefore removes exactly one set bit and keeps the rest. The invariant is that after `r` rounds the value equals the original with its `r` lowest set bits removed. The guard `x != 0` ends the loop early, so a value with fewer than `k` set bits becomes 0 without extra work. For `x = 0` the guard is false at once, which avoids the case `0 - 1 = -1`.

**Complexity.**

- **Time** is O(min(k, b)), where `b` is the number of set bits in `x`, because each round removes one bit and the loop ends when either runs out.
- **Space** is O(1), since the loop needs a single integer.

```java run
import java.util.Random;

public final class LowBitClearK {
    /**
     * Applies the clear step to x up to k times and returns the result.
     * Time: O(min(k, set bits of x)), one round per removed bit.
     * Space: O(1), one working integer.
     * Invariant: after r rounds, x equals the input with its r lowest set bits removed.
     */
    static int clearLowestK(int x, int k) {
        // The guard stops at k rounds or when no set bit remains.
        for (int r = 0; r < k && x != 0; r++) {
            // Clearing the lowest set bit costs one operation and removes exactly one bit.
            x &= (x - 1);
        }
        // The remaining bits are the original bits above the removed ones.
        return x;
    }

    /** Oracle: scans positions from 0 upward and drops the first k set bits it meets. */
    static int oracle(int x, int k) {
        int removed = 0;
        int result = x;
        // The scan visits every position, which is the slow method the lesson replaces.
        for (int i = 0; i < 32 && removed < k; i++) {
            if (((x >>> i) & 1) == 1) {
                result &= ~(1 << i);
                removed++;
            }
        }
        return result;
    }

    public static void main(String[] args) {
        // Checks Example 1 and Example 2 from the exercise.
        if (clearLowestK(180, 2) != 160) throw new AssertionError("example 1");
        if (clearLowestK(7, 5) != 0) throw new AssertionError("example 2");
        // Checks the Java facts used in the explanation.
        if ((180 & 179) != 176) throw new AssertionError("clear step on 180");
        if ((0 & (0 - 1)) != 0) throw new AssertionError("zero stays zero");
        if (clearLowestK(0, 50) != 0) throw new AssertionError("zero input");
        // Checks the method against the scan oracle on random inputs with a fixed seed.
        Random rnd = new Random(3001);
        for (int round = 0; round < 5000; round++) {
            int x = rnd.nextInt() >>> 1;
            if (rnd.nextInt(4) == 0) x &= rnd.nextInt() & rnd.nextInt();
            int k = rnd.nextInt(40);
            if (clearLowestK(x, k) != oracle(x, k)) throw new AssertionError("round " + round);
        }
    }
}
```

#### Solution: [Vary] Number of 1 Bits (LeetCode 191)
<!-- id: bt03-count-set-bits -->

**Approach.** The answer equals the number of clear steps needed to reach 0.

Each clear step removes one set bit, so the loop count equals the number of set bits. The invariant is that `count` plus the set bits still in `n` stays equal to the original number of set bits. The loop ends because the number of set bits falls by one each round and cannot go below 0. A scan over all 31 value positions gives the same answer but always costs 31 rounds, while this loop costs one round per set bit.

**Complexity.**

- **Time** is O(b), where `b` is the number of set bits, because each round clears one bit.
- **Space** is O(1), since the loop needs two integers.

```java run
import java.util.Random;

public final class LowBitCount {
    /**
     * Returns the number of set bits of n, using one clear step per set bit.
     * Time: O(b) for b set bits.
     * Space: O(1).
     * Invariant: count + (set bits of n) equals the set bits of the original value.
     */
    static int countSetBits(int n) {
        // The counter records finished rounds.
        int count = 0;
        // The test is != 0 so the loop also works for negative patterns.
        while (n != 0) {
            // Remove the lowest set bit.
            n &= (n - 1);
            // One more bit has been removed.
            count++;
        }
        // The count equals the bits removed in total.
        return count;
    }

    /** Oracle: counts bits by testing all 32 positions. */
    static int oracle(int n) {
        int c = 0;
        for (int i = 0; i < 32; i++) c += (n >>> i) & 1;
        return c;
    }

    public static void main(String[] args) {
        // Checks Example 1 and Example 2.
        if (countSetBits(180) != 4) throw new AssertionError("example 1");
        if (countSetBits(2147483647) != 31) throw new AssertionError("example 2");
        // Checks the zero input and the library routine as a second oracle.
        if (countSetBits(0) != 0) throw new AssertionError("zero");
        if (countSetBits(1 << 30) != 1) throw new AssertionError("single high bit");
        // Checks random values, including sparse ones, against both oracles.
        Random rnd = new Random(3002);
        for (int round = 0; round < 5000; round++) {
            int n = rnd.nextInt() >>> 1;
            if (rnd.nextBoolean()) n &= rnd.nextInt() & rnd.nextInt() & rnd.nextInt();
            int got = countSetBits(n);
            if (got != oracle(n) || got != Integer.bitCount(n)) throw new AssertionError("round " + round);
        }
    }
}
```

#### Solution: [Boundary] Zero And Negative Int (Author exercise)
<!-- id: bt03-lowest-bit-signed -->

**Approach.** The expression `x & -x` isolates the bit, and a widening mask removes the sign.

In two's complement, `-x` equals `~x + 1`, which is the complement of `x - 1`. So `x & -x` keeps exactly the lowest set bit for every `int` pattern, negative values included. The one surprise is `Integer.MIN_VALUE`, where `-x` wraps back to `x`. The AND then returns `Integer.MIN_VALUE`, which is a negative `int` although the true bit value is 2^31. The expression `& 0xFFFFFFFFL` promotes the `int` to a `long` first and then keeps the low 32 bits, which turns the negative result into 2147483648. The invariant is that the returned value is a power of two or 0, and 0 appears only for the zero pattern.

**Complexity.**

- **Time** is O(1), because the method performs a fixed number of operations.
- **Space** is O(1), because no extra storage grows with the input.

```java run
import java.util.Random;

public final class LowBitIsolateSigned {
    /**
     * Returns the lowest set bit of the 32-bit pattern of x as a non-negative long.
     * Time: O(1).
     * Space: O(1).
     * Invariant: the result is 0 or a power of two, and it is the smallest power of two present in the pattern.
     */
    static long lowestBit(int x) {
        // Negation then AND isolates one bit; the mask widens the int without sign extension.
        return (x & -x) & 0xFFFFFFFFL;
    }

    /** Oracle: scans positions from 0 and returns the first set position as a power of two. */
    static long oracle(int x) {
        for (int i = 0; i < 32; i++) {
            if (((x >>> i) & 1) == 1) return 1L << i;
        }
        return 0L;
    }

    public static void main(String[] args) {
        // Checks Example 1 and Example 2.
        if (lowestBit(-8) != 8L) throw new AssertionError("example 1");
        if (lowestBit(Integer.MIN_VALUE) != 2147483648L) throw new AssertionError("example 2");
        // Checks the Java facts behind the approach.
        if (-Integer.MIN_VALUE != Integer.MIN_VALUE) throw new AssertionError("negation wraps");
        if ((Integer.MIN_VALUE & -Integer.MIN_VALUE) >= 0) throw new AssertionError("int result is negative");
        if (lowestBit(0) != 0L) throw new AssertionError("zero");
        if (lowestBit(-1) != 1L) throw new AssertionError("all ones");
        if (lowestBit(12) != 4L) throw new AssertionError("positive");
        // Checks every position as the only set bit.
        for (int i = 0; i < 32; i++) {
            if (lowestBit(1 << i) != (1L << i)) throw new AssertionError("position " + i);
        }
        // Checks random patterns against the scan oracle.
        Random rnd = new Random(3003);
        for (int round = 0; round < 5000; round++) {
            int x = rnd.nextInt();
            if (rnd.nextBoolean()) x &= rnd.nextInt();
            if (lowestBit(x) != oracle(x)) throw new AssertionError("round " + round);
        }
    }
}
```

#### Solution: [Recognize] Counting Bits (LeetCode 338)
<!-- id: bt03-count-bits-table -->

**Approach.** Each entry equals the entry for the number with its lowest set bit cleared, plus one.

For `i > 0` the value `i & (i - 1)` is strictly smaller than `i`, so its entry is already filled when the pass reaches `i`. That value has exactly one set bit fewer than `i`, which gives `ans[i] = ans[i & (i - 1)] + 1`. The invariant is that `ans[0..i-1]` hold correct counts before the pass writes `ans[i]`. Entry 0 is the base case and stays 0. The pass does one array read and one write per index, so no inner loop is needed.

**Complexity.**

- **Time** is O(n), because each of the `n` entries needs one constant-time update.
- **Space** is O(n) for the returned array, and no other storage is needed.

```java run
import java.util.Random;

public final class LowBitTable {
    /**
     * Returns ans where ans[i] is the number of set bits in i, for 0 <= i <= n.
     * Time: O(n), one constant-time update per index.
     * Space: O(n), the result array.
     * Invariant: before step i, ans[0..i-1] are correct.
     */
    static int[] countBits(int n) {
        // ans[0] is 0 by default and serves as the base case.
        int[] ans = new int[n + 1];
        // The loop runs once per index from 1 to n.
        for (int i = 1; i <= n; i++) {
            // Clearing the lowest set bit gives a smaller index whose entry is already known.
            ans[i] = ans[i & (i - 1)] + 1;
        }
        // Every entry now holds its set bit count.
        return ans;
    }

    public static void main(String[] args) {
        // Checks Example 1 and Example 2.
        int[] e1 = countBits(8);
        int[] want1 = {0, 1, 1, 2, 1, 2, 2, 3, 1};
        if (!java.util.Arrays.equals(e1, want1)) throw new AssertionError("example 1");
        if (!java.util.Arrays.equals(countBits(0), new int[]{0})) throw new AssertionError("example 2");
        // Checks that the cleared value is smaller, which makes the single pass valid.
        for (int i = 1; i < 5000; i++) {
            if ((i & (i - 1)) >= i) throw new AssertionError("not smaller at " + i);
        }
        // Checks random sizes against an independent bit-by-bit count.
        Random rnd = new Random(3004);
        for (int round = 0; round < 200; round++) {
            int n = rnd.nextInt(3000);
            int[] got = countBits(n);
            if (got.length != n + 1) throw new AssertionError("length");
            for (int i = 0; i <= n; i++) {
                int c = 0;
                for (int v = i; v > 0; v >>= 1) c += v & 1;
                if (got[i] != c) throw new AssertionError("round " + round + " i " + i);
            }
        }
    }
}
```
