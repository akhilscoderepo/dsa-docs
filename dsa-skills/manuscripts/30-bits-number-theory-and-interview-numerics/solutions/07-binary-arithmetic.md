<!-- solutions-for: 07-binary-arithmetic -->
### Solutions For Binary Arithmetic

#### Solution: [Build] One-Bit Half Adder (Author exercise)
<!-- id: bt07-half-adder -->

**Approach.** The two output bits come from two different gates on the same inputs.

The sum bit is 1 when the inputs differ, and XOR has exactly that truth table. The carry bit is 1 when both inputs are 1, and AND has that truth table. The pair therefore satisfies `sum + 2 * carry == a + b` for all four input combinations, which is the invariant that later lets the word loop add a carry word to a sum word without changing the total. The exercise needs no loop, since each of the four cases is decided by one operator.

**Complexity.**

- **Time** is O(1), because the method evaluates two operators and builds one two-element array.
- **Space** is O(1), because the output array has a fixed length of two.

```java run
public final class HalfAdder {
    /**
     * Returns {sumBit, carryBit} for two input bits.
     * Time: O(1), two operators.
     * Space: O(1), a two-element result.
     * Invariant: sumBit + 2 * carryBit equals a + b.
     */
    static int[] halfAdd(int a, int b) {
        // XOR is 1 exactly when the two input bits differ, which is the sum bit of one column.
        int sumBit = a ^ b;
        // AND is 1 exactly when both bits are 1, which produces a carry into the next column.
        int carryBit = a & b;
        // The pair is returned in the order the problem states.
        return new int[]{sumBit, carryBit};
    }

    public static void main(String[] args) {
        // Checks Example 1, the only case that produces a carry.
        int[] one = halfAdd(1, 1);
        if (one[0] != 0 || one[1] != 1) throw new AssertionError("example 1");
        // Checks Example 2, where one input bit is set.
        int[] two = halfAdd(1, 0);
        if (two[0] != 1 || two[1] != 0) throw new AssertionError("example 2");
        // Checks all four input pairs against the plain sum, which is the oracle.
        for (int a = 0; a <= 1; a++) {
            for (int b = 0; b <= 1; b++) {
                int[] r = halfAdd(a, b);
                if (r[0] + 2 * r[1] != a + b) throw new AssertionError("pair " + a + " " + b);
            }
        }
    }
}
```

#### Solution: [Vary] Sum With Round Count (LeetCode 371)
<!-- id: bt07-sum-rounds -->

**Approach.** The loop adds the sum word and the carry word until the carry word is zero, and a counter records the rounds.

Each round replaces `a` by `a ^ b` and `b` by `(a & b) << 1`. The sum `a + b` stays the same, because the XOR holds the columns without overlap and the shifted AND holds exactly the carries that those columns still owe. The carry word is saved in a temporary variable first, since the assignment to `a` would otherwise destroy the operand that the AND needs. The counter increases once per executed round, so an input with `b == 0` reports 0 rounds. For non-negative inputs the lowest set bit of the carry word rises by at least one column per round, so the loop stops after at most 31 rounds.

**Complexity.**

- **Time** is O(1) for an `int`, because the loop runs at most 32 rounds of three operators.
- **Space** is O(1), because the method keeps two words and one counter.

```java run
import java.util.Random;

public final class SumWithRounds {
    /**
     * Adds two non-negative ints with bitwise operators and reports the loop rounds.
     * Time: O(1), at most 32 rounds for an int.
     * Space: O(1), two words and a counter.
     * Invariant: a + b equals the original total before and after every round.
     */
    static int[] addCounting(int a, int b) {
        // The counter starts at zero, so an input with no carries reports zero rounds.
        int rounds = 0;
        // The loop continues while any carry bit is left to add.
        while (b != 0) {
            // Save the carry word first, because the next line overwrites a.
            int carryWord = (a & b) << 1;
            // XOR keeps the sum bit of every column without carries.
            a = a ^ b;
            // The carry word becomes the operand of the next round.
            b = carryWord;
            // One more round has finished.
            rounds++;
        }
        // The sum and the round count are returned together.
        return new int[]{a, rounds};
    }

    public static void main(String[] args) {
        // Checks Example 1 against the values in the lesson trace.
        int[] e1 = addCounting(13, 11);
        if (e1[0] != 24 || e1[1] != 4) throw new AssertionError("example 1");
        // Checks Example 2, where a run of nine set bits makes the carry travel far.
        int[] e2 = addCounting(999999999, 1);
        if (e2[0] != 1000000000 || e2[1] != 10) throw new AssertionError("example 2");
        // Checks that zero rounds run when the second operand is zero.
        if (addCounting(7, 0)[1] != 0) throw new AssertionError("zero operand");
        // Checks random inputs against the plus operator, which is the oracle, and bounds the rounds.
        Random rnd = new Random(3071);
        for (int round = 0; round < 5000; round++) {
            int a = rnd.nextInt(1_000_000_001);
            int b = rnd.nextInt(1_000_000_001);
            int[] r = addCounting(a, b);
            if (r[0] != a + b) throw new AssertionError("sum " + a + " " + b);
            if (r[1] > 31) throw new AssertionError("rounds " + a + " " + b);
        }
    }
}
```

#### Solution: [Boundary] Negative Inputs (Author exercise)
<!-- id: bt07-negative-inputs -->

**Approach.** The same loop works on negative inputs, because two's complement addition is addition modulo 2^32.

The shift `<< 1` discards a bit that leaves column 31, and the plus operator discards the same bit when the sum overflows. So the loop computes the plus result for every pair of `int` values, wraparound included. Termination follows from the lowest set bit of the carry word. It moves up at least one column per round, and after 32 rounds no column is left, so the loop ends in at most 32 rounds. The pair `-1` and `1` needs all 32 rounds, because the carry travels through every column. The program also checks three Java facts that the lesson states: the shift discards the top bit, `a & b << 1` parses with the shift first, and a `long` loop does not wrap at 32 bits.

**Complexity.**

- **Time** is O(1), because the loop runs at most 32 rounds for any `int` pair.
- **Space** is O(1), because the method keeps two words and one temporary.

```java run
import java.util.Random;

public final class NegativeSum {
    /**
     * Adds two ints with bitwise operators, wrapping on overflow like the plus operator.
     * Time: O(1), at most 32 rounds.
     * Space: O(1), two words and a temporary.
     * Invariant: (a + b) modulo 2^32 never changes between rounds.
     */
    static int add(int a, int b) {
        // The loop ends when no carry bit remains.
        while (b != 0) {
            // The shift drops any bit that leaves column 31, which matches 32-bit overflow.
            int carryWord = (a & b) << 1;
            // The XOR holds the sum bit of each column without carries.
            a = a ^ b;
            // The carry word is the next operand.
            b = carryWord;
        }
        // The signed bit pattern of a is the final answer.
        return a;
    }

    /** Same loop in 64 bits, used only to show that widening changes the overflow behaviour. */
    static long addWide(long a, long b) {
        // The loop ends when the 64-bit carry word is zero.
        while (b != 0) {
            long carryWord = (a & b) << 1;
            a = a ^ b;
            b = carryWord;
        }
        return a;
    }

    /** Counts the rounds that add needs, to check the 32-round bound. */
    static int rounds(int a, int b) {
        int r = 0;
        // Each pass repeats one round of the same update.
        while (b != 0) {
            int carryWord = (a & b) << 1;
            a = a ^ b;
            b = carryWord;
            r++;
        }
        return r;
    }

    public static void main(String[] args) {
        // Checks Example 1 and Example 2.
        if (add(-5, 3) != -2) throw new AssertionError("example 1");
        if (add(Integer.MIN_VALUE, -1) != Integer.MAX_VALUE) throw new AssertionError("example 2");
        // Checks the worst case for rounds: the carry travels through all 32 columns.
        if (add(-1, 1) != 0) throw new AssertionError("minus one plus one");
        if (rounds(-1, 1) != 32) throw new AssertionError("32 rounds");
        // Checks the Java fact that a left shift discards the top bit.
        if ((Integer.MIN_VALUE << 1) != 0) throw new AssertionError("shift drops top bit");
        // Checks the precedence fact: the unparenthesized form shifts first and gives a different value.
        int p = 1, q = 1;
        if ((p & q << 1) != 0 || ((p & q) << 1) != 2) throw new AssertionError("precedence");
        // Checks that XOR alone drops carries and that a 64-bit loop does not wrap at 32 bits.
        if ((3 ^ 1) != 2) throw new AssertionError("xor alone");
        if (addWide(Integer.MAX_VALUE, 1) != 2147483648L) throw new AssertionError("wide loop");
        // Checks edge values and random pairs against the plus operator, which is the oracle.
        int[] edges = {0, 1, -1, 2, -2, Integer.MAX_VALUE, Integer.MIN_VALUE, 65535, -65536};
        for (int a : edges) {
            for (int b : edges) {
                if (add(a, b) != a + b) throw new AssertionError("edge " + a + " " + b);
                if (rounds(a, b) > 32) throw new AssertionError("edge rounds " + a + " " + b);
            }
        }
        Random rnd = new Random(3072);
        for (int round = 0; round < 20000; round++) {
            int a = rnd.nextInt();
            int b = rnd.nextInt();
            if (add(a, b) != a + b) throw new AssertionError("random " + a + " " + b);
        }
    }
}
```

#### Solution: [Recognize] Binary String Addition (Author exercise)
<!-- id: bt07-binary-string-sum -->

**Approach.** The method adds the digits column by column from the right and passes a carry from each column to the next.

A result array of length `max(x, y) + 1` leaves room for a final carry. Each column adds the digit of `x`, the digit of `y` and the incoming carry. The low bit of that total is the output digit, and the total shifted right by one is the next carry. The invariant is that the digits written so far, together with the carry, equal the sum of the processed suffixes of both inputs. After the leftmost column the carry occupies the extra slot. The method then skips leading zeros and keeps one digit when the whole sum is zero, which also handles inputs with leading zeros.

**Complexity.**

- **Time** is O(L), where L is the longer input length, because the method visits each column once and then scans the result once.
- **Space** is O(L), for the result array of length L + 1.

```java run
import java.math.BigInteger;
import java.util.Random;

public final class BinaryStringSum {
    /**
     * Adds two binary strings and returns the sum without leading zeros.
     * Time: O(L) for the longer length L.
     * Space: O(L) for the result array.
     * Invariant: the written digits plus the carry equal the sum of the suffixes read so far.
     */
    static String add(String x, String y) {
        // One extra slot holds a final carry.
        int len = Math.max(x.length(), y.length()) + 1;
        char[] out = new char[len];
        // The carry starts at zero before the rightmost column.
        int carry = 0;
        // Each pass handles one column, counted from the right end.
        for (int k = 0; k < len; k++) {
            // The incoming carry joins the two digits of this column.
            int total = carry;
            // A shorter input contributes zero in the columns it does not reach.
            if (k < x.length()) total += x.charAt(x.length() - 1 - k) - '0';
            if (k < y.length()) total += y.charAt(y.length() - 1 - k) - '0';
            // The low bit is the output digit, written from the right end of the array.
            out[len - 1 - k] = (char) ('0' + (total & 1));
            // The high bit becomes the carry into the next column.
            carry = total >> 1;
        }
        // Skip leading zeros, but stop before the last character so zero keeps one digit.
        int start = 0;
        while (start < len - 1 && out[start] == '0') start++;
        return new String(out, start, len - start);
    }

    public static void main(String[] args) {
        // Checks Example 1, where the carry runs through every column.
        if (!add("111", "1").equals("1000")) throw new AssertionError("example 1");
        // Checks Example 2, where leading zeros must not survive.
        if (!add("0", "000").equals("0")) throw new AssertionError("example 2");
        // Checks the trace case and a long carry chain.
        if (!add("1011", "110").equals("10001")) throw new AssertionError("trace case");
        String ones = "1".repeat(200);
        if (!add(ones, "1").equals("1" + "0".repeat(200))) throw new AssertionError("long chain");
        // Checks random strings, including leading zeros, against BigInteger, which is the oracle.
        Random rnd = new Random(3074);
        for (int round = 0; round < 3000; round++) {
            StringBuilder a = new StringBuilder();
            StringBuilder b = new StringBuilder();
            for (int i = 1 + rnd.nextInt(70); i > 0; i--) a.append(rnd.nextBoolean() ? '1' : '0');
            for (int i = 1 + rnd.nextInt(70); i > 0; i--) b.append(rnd.nextBoolean() ? '1' : '0');
            String expected = new BigInteger(a.toString(), 2).add(new BigInteger(b.toString(), 2)).toString(2);
            if (!add(a.toString(), b.toString()).equals(expected)) throw new AssertionError(a + " " + b);
        }
    }
}
```
