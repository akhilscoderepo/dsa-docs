<!-- solutions-for: 02-shifts -->
### Solutions For Shifts

#### Solution: [Build] Extract Bit I (Author exercise)
<!-- id: bt02-extract-bit -->

**Approach.** One right shift brings position `i` to position 0, and one AND with 1 erases every other bit.

After the shift by `i`, the bit that started at position `i` sits at position 0. The other bits sit at higher positions or have left the number. The AND with 1 keeps only position 0, so the result is 0 or 1. The signed shift copies the sign into the high positions, but those positions are erased by the AND, so a negative `x` gives the same answer as the zero-fill shift. Position 31 is the sign bit, and the read returns 1 for every negative number at that position.

**Complexity.**

- **Time** is O(1), because the method does one shift and one AND.
- **Space** is O(1), as the method keeps no extra storage.

```java run
import java.util.Random;

public final class ExtractBit {
    /**
     * Returns the bit of x at position i, with position 0 as the lowest bit.
     * Time: O(1), one shift and one AND.
     * Space: O(1).
     * Invariant: after the shift, the wanted bit sits at position 0 and the AND keeps only that position.
     */
    static int bitAt(int x, int i) {
        // The signed shift is safe because the AND erases the copied sign bits.
        return (x >> i) & 1;
    }

    /** Oracle: reads the bit from the 32-character binary string. */
    static int oracle(int x, int i) {
        // toBinaryString drops leading zeros, so pad it to 32 characters.
        String s = String.format("%32s", Integer.toBinaryString(x)).replace(' ', '0');
        // Character 0 of the string is position 31.
        return s.charAt(31 - i) - '0';
    }

    public static void main(String[] args) {
        // Checks Example 1: 180 >> 2 is 45, whose lowest bit is 1.
        if ((180 >> 2) != 45 || bitAt(180, 2) != 1) throw new AssertionError("example 1");
        // Checks Example 2: position 31 of a negative int is 1.
        if (bitAt(Integer.MIN_VALUE + 5, 31) != 1) throw new AssertionError("example 2");
        // Checks that both right shifts give the same bit for a negative value.
        for (int i = 0; i < 32; i++) {
            if (((-16 >> i) & 1) != ((-16 >>> i) & 1)) throw new AssertionError("shift kinds " + i);
        }
        // Checks random values and positions against the string oracle with a fixed seed.
        Random rnd = new Random(3002);
        for (int round = 0; round < 1000; round++) {
            int x = rnd.nextInt();
            int i = rnd.nextInt(32);
            if (bitAt(x, i) != oracle(x, i)) throw new AssertionError("round " + round);
        }
    }
}
```

#### Solution: [Vary] Reverse Bits (LeetCode 190)
<!-- id: bt02-reverse-bits -->

**Approach.** The loop moves the lowest bit of `n` onto the right end of the result, 32 times.

In each round, the result moves up by one position with a left shift. This frees position 0 of the result, and OR writes the lowest bit of `n` there. Then `n` moves down by one position so the next bit becomes the lowest one. After round `k`, the result holds the lowest `k` bits of the input in reversed order. After 32 rounds, the first bit read, which was position 0 of `n`, has been pushed up to position 31. The loop uses a fixed count of 32 and the zero-fill shift, so a negative input never copies its sign into the bits still to be read.

**Complexity.**

- **Time** is O(1) for a fixed width of 32, because the loop runs 32 times with constant work per round.
- **Space** is O(1), as the method holds only the result and the shifted copy of `n`.

```java run
import java.util.Random;

public final class ReverseBits {
    /**
     * Reverses the 32-bit pattern of n.
     * Time: O(1), exactly 32 rounds.
     * Space: O(1).
     * Invariant: after k rounds, result holds the lowest k bits of the input in reversed order.
     */
    static int reverse(int n) {
        // The result starts empty.
        int result = 0;
        // A fixed count of 32 ends the loop for every input, including negative ones.
        for (int i = 0; i < 32; i++) {
            // Move earlier bits up one position, then write the lowest bit of n at position 0.
            result = (result << 1) | (n & 1);
            // The zero-fill shift drops the used bit and brings the next one down.
            n >>>= 1;
        }
        // The last bit written started at position 31 of the input and now sits at position 0.
        return result;
    }

    /** Oracle: reverses the 32-character binary string. */
    static int oracle(int n) {
        // Pad the binary string to 32 characters, reverse it and parse it as unsigned.
        String s = String.format("%32s", Integer.toBinaryString(n)).replace(' ', '0');
        String r = new StringBuilder(s).reverse().toString();
        return (int) Long.parseLong(r, 2);
    }

    public static void main(String[] args) {
        // Checks Example 1 and Example 2.
        if (reverse(43261596) != 964176192) throw new AssertionError("example 1");
        if (reverse(-3) != -1073741825) throw new AssertionError("example 2");
        // Checks the two extremes: zero and the pattern with only the sign bit.
        if (reverse(0) != 0 || reverse(Integer.MIN_VALUE) != 1 || reverse(1) != Integer.MIN_VALUE) throw new AssertionError("extremes");
        // Checks the library result as a second reference for random values with a fixed seed.
        Random rnd = new Random(3012);
        for (int round = 0; round < 1000; round++) {
            int n = rnd.nextInt();
            if (reverse(n) != oracle(n) || reverse(n) != Integer.reverse(n)) throw new AssertionError("round " + round);
        }
        // Checks that reversing twice returns the input.
        if (reverse(reverse(123456789)) != 123456789) throw new AssertionError("involution");
    }
}
```

#### Solution: [Boundary] Negative Values (Author exercise)
<!-- id: bt02-negative-values -->

**Approach.** The loop reads the lowest bit, adds it, and shifts with zero fill until the value is 0.

The zero-fill shift puts a 0 into the top position in every round. After at most 32 rounds, every bit of the original pattern has left, and the value is 0, so the loop always ends. The signed shift fails here. For a negative `x`, it copies the sign bit into the top position, the value settles at -1, and the test `x != 0` never turns false. The count adds `x & 1` before each shift, so every bit equal to 1 is counted exactly once. The invariant is that `ones` equals the number of 1 bits already shifted out.

**Complexity.**

- **Time** is O(1) for a fixed width of 32, because the loop runs at most 32 rounds.
- **Space** is O(1), as the method holds just one counter and the shifted value.

```java run
import java.util.Random;

public final class NegativeValues {
    /**
     * Counts the bits equal to 1 in the 32-bit pattern of x.
     * Time: O(1), at most 32 rounds.
     * Space: O(1).
     * Invariant: ones equals the number of 1 bits that have already left x.
     */
    static int countOnes(int x) {
        // The counter starts at 0.
        int ones = 0;
        // The zero-fill shift guarantees x reaches 0 after at most 32 rounds.
        while (x != 0) {
            // The lowest bit is 0 or 1, so the AND adds it directly.
            ones += x & 1;
            // Shift in a 0 at the top, so the sign bit never repeats.
            x >>>= 1;
        }
        return ones;
    }

    /** Oracle: counts the 1 characters of the binary string. */
    static int oracle(int x) {
        // toBinaryString shows the 32-bit pattern of a negative int.
        int count = 0;
        for (char c : Integer.toBinaryString(x).toCharArray()) if (c == '1') count++;
        return count;
    }

    public static void main(String[] args) {
        // Checks Example 1 and Example 2.
        if (countOnes(-8) != 29) throw new AssertionError("example 1");
        if (countOnes(Integer.MIN_VALUE) != 1) throw new AssertionError("example 2");
        // Checks the lesson claims about the two right shifts on -1.
        if ((-1 >> 1) != -1 || (-1 >>> 1) != Integer.MAX_VALUE) throw new AssertionError("shift kinds");
        // Checks that the signed shift never reaches 0 within 100 rounds for a negative value.
        int stuck = -8;
        for (int i = 0; i < 100; i++) stuck >>= 1;
        if (stuck != -1) throw new AssertionError("signed shift stays at -1");
        // Checks zero and the extremes.
        if (countOnes(0) != 0 || countOnes(-1) != 32 || countOnes(Integer.MAX_VALUE) != 31) throw new AssertionError("extremes");
        // Checks random values against the string oracle and the library with a fixed seed.
        Random rnd = new Random(3022);
        for (int round = 0; round < 1000; round++) {
            int x = rnd.nextInt();
            if (countOnes(x) != oracle(x) || countOnes(x) != Integer.bitCount(x)) throw new AssertionError("round " + round);
        }
    }
}
```

#### Solution: [Recognize] Pack Two Fields (Author exercise)
<!-- id: bt02-pack-fields -->

**Approach.** The left shift moves `x` into the top 12 positions, OR joins it with `y`, and two reads split them again.

To store a record, shift `x` left by 20 and OR the result with `y`. The field `y` is below 2^20, so it occupies only positions 0 to 19 and cannot touch the shifted `x`. To read `y`, AND the stored value with a run of 20 ones, which erases the top 12 positions. To read `x`, shift the stored value right by 20 with zero fill. When `x` is 2048 or more, position 31 is 1, and the stored `int` is negative. The signed shift would copy that sign into the field and return a negative number, so the read must use the zero-fill shift. The invariant is that the two fields use disjoint positions, so neither write disturbs the other.

**Complexity.**

- **Time** is O(r + q) for `r` records and `q` queries, because each record and each query costs a constant number of shifts.
- **Space** is O(r) for the array of stored `int` values, which is half the size of two arrays.

```java run
import java.util.Random;

public final class PackFields {
    /** Returns the packed int: x in positions 20 to 31 and y in positions 0 to 19. */
    static int pack(int x, int y) {
        // y stays below 2^20, so the OR cannot disturb the shifted x.
        return (x << 20) | y;
    }

    /**
     * Stores every record in one int, then answers each query from the stored values.
     * Time: O(r + q), constant work per record and per query.
     * Space: O(r), one int per record and the answer array.
     * Invariant: the two fields use disjoint positions, so a read of one field never sees the other.
     */
    static int[] answers(int[][] records, int[][] queries) {
        // One int per record is the whole table.
        int[] stored = new int[records.length];
        for (int i = 0; i < records.length; i++) stored[i] = pack(records[i][0], records[i][1]);
        // One answer per query.
        int[] out = new int[queries.length];
        for (int k = 0; k < queries.length; k++) {
            int p = stored[queries[k][0]];
            if (queries[k][1] == 0) {
                // Zero fill makes the field correct even when the top bit is 1.
                out[k] = p >>> 20;
            } else {
                // The run of 20 ones keeps positions 0 to 19 and erases the field x.
                out[k] = p & ((1 << 20) - 1);
            }
        }
        return out;
    }

    /** Oracle: reads the fields straight from the records. */
    static int[] oracle(int[][] records, int[][] queries) {
        int[] out = new int[queries.length];
        // The answer is the original field, with no packing at all.
        for (int k = 0; k < queries.length; k++) out[k] = records[queries[k][0]][queries[k][1]];
        return out;
    }

    public static void main(String[] args) {
        // Checks Example 1, where the stored int is negative.
        int[][] r1 = {{4095, 7}, {1, 1048575}, {0, 0}};
        int[][] q1 = {{0, 0}, {0, 1}, {1, 1}};
        if (!java.util.Arrays.equals(answers(r1, q1), new int[]{4095, 7, 1048575})) throw new AssertionError("example 1");
        if (pack(4095, 7) >= 0) throw new AssertionError("negative stored value");
        // Checks that the signed shift would return a negative field for that stored value.
        if ((pack(4095, 7) >> 20) != -1) throw new AssertionError("signed shift copies the sign");
        // Checks Example 2.
        if (!java.util.Arrays.equals(answers(new int[][]{{2, 5}}, new int[][]{{0, 0}, {0, 1}}), new int[]{2, 5})) throw new AssertionError("example 2");
        // Checks random records and queries against the direct oracle with a fixed seed.
        Random rnd = new Random(3032);
        for (int round = 0; round < 500; round++) {
            int[][] recs = new int[1 + rnd.nextInt(5)][];
            for (int i = 0; i < recs.length; i++) recs[i] = new int[]{rnd.nextInt(4096), rnd.nextInt(1 << 20)};
            int[][] qs = new int[6][];
            for (int k = 0; k < qs.length; k++) qs[k] = new int[]{rnd.nextInt(recs.length), rnd.nextInt(2)};
            if (!java.util.Arrays.equals(answers(recs, qs), oracle(recs, qs))) throw new AssertionError("round " + round);
        }
    }
}
```
