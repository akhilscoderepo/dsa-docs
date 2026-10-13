<!-- solutions-for: 01-bit-masks -->
### Solutions For Bit Masks

#### Solution: [Build] Flag Operations (Author exercise)
<!-- id: bt01-flag-ops -->

**Approach.** Every operation builds the single-bit value `1 << p` and combines it with the flags in one step.

The test ANDs the flags with the single-bit value and counts a nonzero result. The set operation ORs the value in, the clear operation ANDs with its complement, and the toggle operation XORs it. Each of the three updates changes position `p` and leaves the other 30 positions as they were, which is the invariant of the loop. The loop applies the operations in the given order and counts tests as it goes. A clear on a clear bit and a set on a set bit both leave the flags unchanged, so repeated operations need no special case.

**Complexity.**

- **Time** is O(m) for `m` operations, because each operation does a constant number of bit operations.
- **Space** is O(1) beyond the two-slot result array.

```java run
import java.util.Random;

public final class FlagOps {
    /**
     * Applies set, clear, toggle and test operations to a flags value.
     * Time: O(m), constant work per operation.
     * Space: O(1) beyond the result array.
     * Invariant: after each operation, only the bit named by that operation can differ from before.
     */
    static int[] apply(int flags, int[][] ops) {
        // The counter holds the number of tests that found their bit set.
        int found = 0;
        // One iteration per operation, so the loop costs O(m).
        for (int[] op : ops) {
            // The single-bit value shared by all four operations.
            int bit = 1 << op[1];
            if (op[0] == 0) {
                // A nonzero AND means the bit is set; the comparison avoids == 1.
                if ((flags & bit) != 0) found++;
            } else if (op[0] == 1) {
                // OR writes a 1 at the position and keeps the rest.
                flags |= bit;
            } else if (op[0] == 2) {
                // AND with the complement erases only that position.
                flags &= ~bit;
            } else {
                // XOR flips only that position.
                flags ^= bit;
            }
        }
        // Slot 0 is the final flags, slot 1 is the number of positive tests.
        return new int[]{flags, found};
    }

    /** Oracle: simulates the flags with a boolean array of 31 positions. */
    static int[] oracle(int flags, int[][] ops) {
        // Unpack the starting flags into one boolean per position.
        boolean[] bits = new boolean[31];
        for (int i = 0; i < 31; i++) bits[i] = ((flags >> i) & 1) == 1;
        int found = 0;
        // Apply each operation on the array.
        for (int[] op : ops) {
            if (op[0] == 0) { if (bits[op[1]]) found++; }
            else if (op[0] == 1) bits[op[1]] = true;
            else if (op[0] == 2) bits[op[1]] = false;
            else bits[op[1]] = !bits[op[1]];
        }
        // Pack the array back into an int.
        int out = 0;
        for (int i = 0; i < 31; i++) if (bits[i]) out += 1 << i;
        return new int[]{out, found};
    }

    public static void main(String[] args) {
        // Checks Example 1 from the problem text.
        int[][] ex1 = {{1, 3}, {2, 0}, {3, 2}, {0, 3}};
        if (!java.util.Arrays.equals(apply(5, ex1), new int[]{8, 1})) throw new AssertionError("example 1");
        // Checks Example 2, where clearing a clear bit and a double toggle change nothing.
        int[][] ex2 = {{2, 5}, {0, 5}, {3, 30}, {3, 30}, {0, 30}};
        if (!java.util.Arrays.equals(apply(0, ex2), new int[]{0, 0})) throw new AssertionError("example 2");
        // Checks the lesson claim that the shift 1 << 32 wraps to 1 for an int.
        int thirtyTwo = 32;
        if ((1 << thirtyTwo) != 1) throw new AssertionError("int shift wraps");
        // Checks random operation lists against the boolean-array oracle with a fixed seed.
        Random rnd = new Random(3001);
        for (int round = 0; round < 500; round++) {
            int flags = rnd.nextInt() & Integer.MAX_VALUE;
            int[][] ops = new int[rnd.nextInt(15)][];
            for (int i = 0; i < ops.length; i++) ops[i] = new int[]{rnd.nextInt(4), rnd.nextInt(31)};
            if (!java.util.Arrays.equals(apply(flags, ops), oracle(flags, ops))) throw new AssertionError("round " + round);
        }
    }
}
```

#### Solution: [Vary] Permission Set (Author exercise)
<!-- id: bt01-permission-set -->

**Approach.** Each list becomes one mask, and the final test compares a whole set at once.

The grants mask collects every granted position with OR. The revokes mask is cleared out of it with AND and the complement, so a name that appears in both lists ends as not granted. The required mask collects the needed positions in the same way. The user holds every required permission exactly when ANDing the effective mask with the required mask returns the required mask unchanged. The test `!= 0` would only prove that one required bit is present, so the equality is the point of the exercise. An empty required list gives a required mask of 0, and the equality holds trivially.

**Complexity.**

- **Time** is O(g + r + q) for the three list lengths, because each name costs one switch and one bit operation.
- **Space** is O(1), because the program keeps three integers and no copy of the lists.

```java run
import java.util.HashSet;
import java.util.Random;
import java.util.Set;

public final class PermissionSet {
    /** Returns the bit position of a permission name; the five names are fixed by the problem. */
    static int bitOf(String name) {
        // A switch maps each name to its position in constant time.
        return switch (name) {
            case "READ" -> 0;
            case "WRITE" -> 1;
            case "EXECUTE" -> 2;
            case "DELETE" -> 3;
            default -> 4;
        };
    }

    /**
     * Returns true when the user ends with every required permission.
     * Time: O(g + r + q), one bit operation per name.
     * Space: O(1), three integers.
     * Invariant: bit p of each mask is 1 exactly when its list names the permission at p.
     */
    static boolean allowed(String[] grants, String[] revokes, String[] required) {
        // The effective mask starts empty.
        int effective = 0;
        // OR sets each granted position; a repeated name changes nothing.
        for (String g : grants) effective |= 1 << bitOf(g);
        // AND with the complement removes each revoked position, even if it was never granted.
        for (String r : revokes) effective &= ~(1 << bitOf(r));
        // The need mask collects the required positions.
        int need = 0;
        for (String q : required) need |= 1 << bitOf(q);
        // Equality with need means every required bit is present; an empty need passes.
        return (effective & need) == need;
    }

    /** Oracle: uses string sets. */
    static boolean oracle(String[] grants, String[] revokes, String[] required) {
        // Build the set of granted names, then remove the revoked names.
        Set<String> have = new HashSet<>(java.util.List.of(grants));
        for (String r : revokes) have.remove(r);
        // Every required name must be in the remaining set.
        for (String q : required) if (!have.contains(q)) return false;
        return true;
    }

    public static void main(String[] args) {
        // Checks Example 1 and its variant that requires a revoked permission.
        String[] g1 = {"READ", "WRITE", "DELETE"};
        String[] r1 = {"DELETE"};
        if (!allowed(g1, r1, new String[]{"READ", "WRITE"})) throw new AssertionError("example 1a");
        if (allowed(g1, r1, new String[]{"READ", "DELETE"})) throw new AssertionError("example 1b");
        // Checks Example 2, where the weaker any-bit test would give the wrong answer.
        String[] g2 = {"READ"};
        if (allowed(g2, new String[0], new String[]{"READ", "WRITE"})) throw new AssertionError("example 2");
        if (((1 & 3) != 0) != true) throw new AssertionError("any-bit test is true here");
        // Checks the empty required list.
        if (!allowed(new String[0], new String[0], new String[0])) throw new AssertionError("empty required");
        // Checks random lists against the string-set oracle with a fixed seed.
        String[] names = {"READ", "WRITE", "EXECUTE", "DELETE", "ADMIN"};
        Random rnd = new Random(3011);
        for (int round = 0; round < 500; round++) {
            String[] g = pick(rnd, names, 7);
            String[] r = pick(rnd, names, 5);
            String[] q = pick(rnd, names, 4);
            if (allowed(g, r, q) != oracle(g, r, q)) throw new AssertionError("round " + round);
        }
    }

    /** Returns a random list of up to max names, which may repeat. */
    static String[] pick(Random rnd, String[] names, int max) {
        // The length may be 0, so empty lists are covered.
        String[] out = new String[rnd.nextInt(max)];
        for (int i = 0; i < out.length; i++) out[i] = names[rnd.nextInt(names.length)];
        return out;
    }
}
```

#### Solution: [Boundary] Position Width (Author exercise)
<!-- id: bt01-position-width -->

**Approach.** The single-bit value is a `long`, so positions 32 to 63 stay valid.

The expression `1L << p` starts from a `long` operand, and Java reduces its shift distance to the low 6 bits, so every `p` from 0 to 63 names its own digit. The expression `1 << p` starts from an `int` and reduces the distance to the low 5 bits, so position 32 would collide with position 0. OR accumulates the single-bit values, which makes duplicates harmless, because a second OR of the same bit changes nothing. Position 63 is the sign digit, so the result is negative whenever the list contains 63, and the program returns it unchanged.

**Complexity.**

- **Time** is O(m) for `m` positions, because each position costs one shift and one OR.
- **Space** is O(1), because the program keeps one `long`.

```java run
import java.math.BigInteger;
import java.util.Random;

public final class PositionWidth {
    /**
     * Returns the long with a 1 at every listed position.
     * Time: O(m), one shift and one OR per position.
     * Space: O(1), one long.
     * Invariant: after each step, bit p of the result is 1 exactly when p appeared so far.
     */
    static long maskOf(int[] positions) {
        // The result starts empty.
        long mask = 0L;
        // One iteration per position.
        for (int p : positions) {
            // 1L keeps the shift in 64-bit arithmetic, so positions 32 to 63 stay distinct.
            mask |= 1L << p;
        }
        // The sign digit may be set, so the value can be negative.
        return mask;
    }

    /** Oracle: builds the value with BigInteger and keeps the low 64 bits. */
    static long oracle(int[] positions) {
        // A BigInteger has no width limit, so no position can wrap.
        BigInteger big = BigInteger.ZERO;
        for (int p : positions) big = big.setBit(p);
        // longValue keeps the low 64 bits in two's complement.
        return big.longValue();
    }

    public static void main(String[] args) {
        // Checks Example 2 and the int-shift trap named in the lesson.
        if (maskOf(new int[]{32, 32}) != 4294967296L) throw new AssertionError("example 2");
        int thirtyTwo = 32;
        if ((1 << thirtyTwo) != 1) throw new AssertionError("int shift wraps to 1");
        // Checks that position 63 gives a negative long and that Example 1 matches the oracle.
        if ((1L << 63) != Long.MIN_VALUE) throw new AssertionError("sign digit");
        int[] ex1 = {0, 40, 63};
        if (maskOf(ex1) >= 0 || maskOf(ex1) != oracle(ex1)) throw new AssertionError("example 1");
        // Checks the empty list.
        if (maskOf(new int[0]) != 0L) throw new AssertionError("empty");
        // Checks random lists against the BigInteger oracle with a fixed seed.
        Random rnd = new Random(3021);
        for (int round = 0; round < 500; round++) {
            int[] ps = new int[rnd.nextInt(10)];
            for (int i = 0; i < ps.length; i++) ps[i] = rnd.nextInt(64);
            if (maskOf(ps) != oracle(ps)) throw new AssertionError("round " + round);
        }
    }
}
```

#### Solution: [Recognize] Disjoint Word Pairs (LeetCode 318)
<!-- id: bt01-disjoint-word-pairs -->

**Approach.** One mask per word reduces every pair test to a single AND.

The first pass reads each word once and sets bit `c - 'a'` for each letter, so the mask records which of the 26 letters occur and ignores repeats. A zero result from ANDing two masks proves that the two words have no letter in common. The second pass visits every index pair `i < j` and counts the pairs with a zero AND. Because the exercise asks for a count and not a maximum product, no pair can be skipped, and the answer needs no `long` arithmetic: at most 499,500 pairs fit in an `int`.

**Complexity.**

- **Time** is O(S + n * n), where `S` is the total number of letters, because the mask pass reads each letter once and the pair pass does one AND per pair.
- **Space** is O(n) for the array of masks.

```java run
import java.util.HashSet;
import java.util.Random;
import java.util.Set;

public final class DisjointWordPairs {
    /**
     * Counts index pairs i < j whose words share no letter.
     * Time: O(S + n * n), S is the total letter count.
     * Space: O(n), one mask per word.
     * Invariant: masks[i] has bit c set exactly when word i contains the letter at position c.
     */
    static int countPairs(String[] words) {
        // One int per word is enough because the alphabet has 26 letters.
        int[] masks = new int[words.length];
        // Pass one reads every letter once.
        for (int i = 0; i < words.length; i++) {
            for (int k = 0; k < words[i].length(); k++) {
                // OR sets the letter's bit and ignores repeated letters.
                masks[i] |= 1 << (words[i].charAt(k) - 'a');
            }
        }
        // The count starts at 0 and only grows.
        int count = 0;
        // Pass two visits each pair once.
        for (int i = 0; i < words.length; i++) {
            for (int j = i + 1; j < words.length; j++) {
                // A zero AND proves that the two letter sets are disjoint.
                if ((masks[i] & masks[j]) == 0) count++;
            }
        }
        return count;
    }

    /** Oracle: compares character sets directly. */
    static int oracle(String[] words) {
        int count = 0;
        for (int i = 0; i < words.length; i++) {
            for (int j = i + 1; j < words.length; j++) {
                // Collect the letters of word i, then look for any letter of word j.
                Set<Character> seen = new HashSet<>();
                for (char c : words[i].toCharArray()) seen.add(c);
                boolean shared = false;
                for (char c : words[j].toCharArray()) if (seen.contains(c)) shared = true;
                if (!shared) count++;
            }
        }
        return count;
    }

    public static void main(String[] args) {
        // Checks Example 1 and Example 2.
        if (countPairs(new String[]{"abc", "de", "cf", "ghi"}) != 5) throw new AssertionError("example 1");
        if (countPairs(new String[]{"aa", "aa", "b"}) != 2) throw new AssertionError("example 2");
        // Checks the empty list and the single word.
        if (countPairs(new String[0]) != 0 || countPairs(new String[]{"z"}) != 0) throw new AssertionError("small");
        // Checks the full alphabet in one word, which sets bit 25 and every bit below it.
        if (countPairs(new String[]{"abcdefghijklmnopqrstuvwxyz", "a"}) != 0) throw new AssertionError("alphabet");
        // Checks random lists against the set oracle with a fixed seed.
        Random rnd = new Random(3031);
        for (int round = 0; round < 400; round++) {
            String[] ws = new String[rnd.nextInt(8)];
            for (int i = 0; i < ws.length; i++) {
                StringBuilder sb = new StringBuilder();
                int len = 1 + rnd.nextInt(4);
                for (int k = 0; k < len; k++) sb.append((char) ('a' + rnd.nextInt(8)));
                ws[i] = sb.toString();
            }
            if (countPairs(ws) != oracle(ws)) throw new AssertionError("round " + round);
        }
    }
}
```
