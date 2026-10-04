<!-- solutions-for: 01-arrays-core-operations -->
### Solutions For Frequency Arrays

#### Solution: [Build] Digit Counts (Author exercise)
<!-- id: ar-digit-counts -->

**Approach.** The method allocates a count array with one slot for each digit 0 to 9. Java fills a new `int[]` with zeros, so every slot starts at 0. One scan then increments the slot at each value. The value is a valid index because the problem guarantees the range 0 to 9.

The invariant is that after a prefix of the input is processed, `count[d]` equals the number of occurrences of `d` in that prefix. No two readings are ever compared. The harness asserts the zero-fill behaviour and compares the method with a brute-force count.

**Complexity.**

- **Time** is O(n), because each reading triggers one increment.
- **Space** is O(1) beyond the output, because the output has a fixed length of 10.

```java run
import java.util.Arrays;
import java.util.Random;

public final class DigitCounts {
    /**
     * Counts how often each digit 0..9 appears in the input.
     * Time: O(n), because each value triggers one increment.
     * Space: O(1), because the result always has ten slots.
     * Invariant: after a prefix is processed, count[d] is the number of occurrences of d in it.
     */
    static int[] digitCounts(int[] digits) {
        // Java zero-fills a new int array, so every digit starts with count 0.
        int[] count = new int[10];
        // One scan reads each value exactly once, which gives the O(n) time.
        for (int x : digits) {
            // The value is the index, so one increment records the occurrence without any comparison.
            count[x]++;
        }
        // The array of ten counts is the answer.
        return count;
    }

    public static void main(String[] args) {
        // Checks the Java fact that a new int array starts with zeros.
        for (int v : new int[10]) if (v != 0) throw new AssertionError("new arrays are zero-filled");
        // Checks Example 1.
        if (!Arrays.equals(digitCounts(new int[] {2, 0, 2}), new int[] {1, 0, 2, 0, 0, 0, 0, 0, 0, 0})) throw new AssertionError("example 1");
        // Checks Example 2: an empty input gives ten zeros, and one repeated digit fills one slot.
        if (!Arrays.equals(digitCounts(new int[0]), new int[10])) throw new AssertionError("empty input");
        if (!Arrays.equals(digitCounts(new int[] {9, 9, 9, 9}), new int[] {0, 0, 0, 0, 0, 0, 0, 0, 0, 4})) throw new AssertionError("repeated digit");
        // Checks the method against a brute-force count on 3,000 random arrays.
        Random rnd = new Random(41);
        for (int t = 0; t < 3000; t++) {
            int[] x = new int[rnd.nextInt(30)];
            for (int i = 0; i < x.length; i++) x[i] = rnd.nextInt(10);
            int[] expected = new int[10];
            for (int d = 0; d < 10; d++) for (int v : x) if (v == d) expected[d]++;
            if (!Arrays.equals(digitCounts(x), expected)) throw new AssertionError("mismatch");
        }
    }
}
```

#### Solution: [Vary] Smaller Than Current Number (LeetCode 1365)
<!-- id: ar-smaller-than-current -->

**Approach.** The method builds a count array over the values 0 to 100. It then converts the counts into a table in which `smaller[v]` is the sum of `count[0..v-1]`, which is the number of readings strictly below `v`. A final scan answers each position with one table lookup.

The table comes from a running sum. Before adding `count[v]` to the running sum, the method stores the sum as `smaller[v]`. That order excludes the readings equal to `v`, which the strict comparison requires. The harness compares the method with an all-pairs oracle on random arrays that include repeated values.

**Complexity.**

- **Time** is O(n + D) with `D = 101`, because the method makes one counting pass, one pass over the slots and one answer pass.
- **Space** is O(D) for the count table, plus the output array of length `n`.

```java run
import java.util.Arrays;
import java.util.Random;

public final class SmallerThanCurrent {
    /**
     * Returns, for each position, how many values in the array are strictly smaller.
     * Time: O(n + D) with D = 101, because there are three linear passes.
     * Space: O(D) for the tables, plus the output.
     * Invariant: before slot v is added, running equals the number of values below v.
     */
    static int[] smallerNumbers(int[] nums) {
        // The domain 0..100 has 101 members, so the count array has 101 slots.
        int[] count = new int[101];
        // Pass 1: one increment per value, which costs O(n).
        for (int x : nums) count[x]++;
        // The smaller table maps each value to the number of readings below it.
        int[] smaller = new int[101];
        // The running sum holds the count of all values below the current slot.
        int running = 0;
        // Pass 2: walk the D slots once in increasing order.
        for (int v = 0; v <= 100; v++) {
            // Store the total before adding this slot, so equal values are excluded.
            smaller[v] = running;
            // Add this slot's readings, so the next slot sees them as smaller.
            running += count[v];
        }
        // The answer array has one entry per input position.
        int[] answer = new int[nums.length];
        // Pass 3: each answer is one table lookup, which costs O(n).
        for (int i = 0; i < nums.length; i++) answer[i] = smaller[nums[i]];
        // Return the lookups.
        return answer;
    }

    public static void main(String[] args) {
        // Checks Example 1: ties do not count as smaller.
        if (!Arrays.equals(smallerNumbers(new int[] {5, 0, 5, 2, 9}), new int[] {2, 0, 2, 1, 4})) throw new AssertionError("example 1");
        // Checks Example 2: equal values have nothing smaller.
        if (!Arrays.equals(smallerNumbers(new int[] {7, 7, 7}), new int[] {0, 0, 0})) throw new AssertionError("all equal");
        // Checks the domain edges 0 and 100 in one array.
        if (!Arrays.equals(smallerNumbers(new int[] {100, 0}), new int[] {1, 0})) throw new AssertionError("edges");
        // Checks the method against an all-pairs oracle on 3,000 random arrays with values in 0..100.
        Random rnd = new Random(43);
        for (int t = 0; t < 3000; t++) {
            int[] x = new int[1 + rnd.nextInt(15)];
            for (int i = 0; i < x.length; i++) x[i] = rnd.nextInt(2) == 0 ? rnd.nextInt(101) : rnd.nextInt(4) * 33;
            int[] expected = new int[x.length];
            for (int i = 0; i < x.length; i++) for (int j = 0; j < x.length; j++) if (x[j] < x[i]) expected[i]++;
            if (!Arrays.equals(smallerNumbers(x), expected)) throw new AssertionError("mismatch " + Arrays.toString(x));
        }
    }
}
```

#### Solution: [Boundary] Dice Validation (Author exercise)
<!-- id: ar-dice-validation -->

**Approach.** The method applies a range check before every index operation. Each roll `r` is compared with the limits 1 and 6. A roll outside that range ends the method at once with `null`, so the invalid value never reaches the array index. A valid roll increments `count[r - 1]`, and the offset of 1 maps face 1 to position 0.

Without the check, a roll of 0 computes the index `-1`, and a roll of 7 computes the index 6. Java throws `ArrayIndexOutOfBoundsException` in both cases. The harness asserts that behaviour and then checks the method against an oracle on random arrays that include invalid values.

**Complexity.**

- **Time** is O(n), because each roll costs one comparison pair and at most one increment.
- **Space** is O(1) beyond the output, because the output has six slots.

```java run
import java.util.Arrays;
import java.util.Random;

public final class DiceValidation {
    /**
     * Counts faces 1..6 and rejects the whole input when any roll is outside that range.
     * Time: O(n), because each roll is checked and counted once.
     * Space: O(1), because the result has six slots.
     * Invariant: count[f - 1] equals the number of valid rolls equal to f in the prefix processed so far.
     */
    static int[] countFaces(int[] rolls) {
        // Six slots cover the faces; Java zero-fills them.
        int[] count = new int[6];
        // One scan checks and counts each roll.
        for (int r : rolls) {
            // The range check runs first, so an invalid value never becomes an index.
            if (r < 1 || r > 6) return null;
            // The offset of 1 maps face 1 to slot 0 and face 6 to slot 5.
            count[r - 1]++;
        }
        // Return the counts after every roll has passed the check.
        return count;
    }

    public static void main(String[] args) {
        // Checks the Java facts that justify the range check: indexes -1 and 6 throw on a six-slot array.
        int[] probe = new int[6];
        boolean low = false, high = false;
        try { probe[-1]++; } catch (ArrayIndexOutOfBoundsException e) { low = true; }
        try { probe[6]++; } catch (ArrayIndexOutOfBoundsException e) { high = true; }
        if (!low || !high) throw new AssertionError("out-of-range indexes throw");
        // Checks Example 1.
        if (!Arrays.equals(countFaces(new int[] {1, 6, 6}), new int[] {1, 0, 0, 0, 0, 2})) throw new AssertionError("example 1");
        // Checks Example 2: the roll 0 is rejected, an empty input gives six zeros, and 7 is rejected.
        if (countFaces(new int[] {1, 6, 0}) != null) throw new AssertionError("zero rejected");
        if (!Arrays.equals(countFaces(new int[0]), new int[6])) throw new AssertionError("empty input");
        if (countFaces(new int[] {7}) != null) throw new AssertionError("seven rejected");
        // Checks the method against an oracle on 3,000 random arrays that sometimes contain invalid values.
        Random rnd = new Random(47);
        for (int t = 0; t < 3000; t++) {
            int[] x = new int[rnd.nextInt(10)];
            boolean valid = true;
            for (int i = 0; i < x.length; i++) {
                x[i] = rnd.nextInt(9) - 1;
                if (x[i] < 1 || x[i] > 6) valid = false;
            }
            int[] got = countFaces(x);
            if (!valid) {
                if (got != null) throw new AssertionError("invalid input must return null");
            } else {
                int[] expected = new int[6];
                for (int f = 1; f <= 6; f++) for (int v : x) if (v == f) expected[f - 1]++;
                if (!Arrays.equals(got, expected)) throw new AssertionError("count mismatch");
            }
        }
    }
}
```

#### Solution: [Recognize] Height Checker (LeetCode 1051)
<!-- id: ar-height-checker -->

**Approach.** The method counts the heights in an array of 101 slots, with the offset equal to 0 because the values are at most 100. The sorted sequence is the walk over the slots from low to high, where slot `v` contributes `count[v]` copies of `v`. The method does not store that sequence. A position index `idx` advances with the walk, and each copy of `v` is compared with `heights[idx]`. A mismatch adds one to the answer.

The invariant is that after the walk handles all copies of the values below `v`, `idx` equals the number of those copies, and `idx` is the position of the next expected value. The input array is never modified. The harness compares the method with a comparison sort on a clone.

**Complexity.**

- **Time** is O(n + D) with `D = 100`, because the method counts once and then walks the slots and positions once.
- **Space** is O(D), because only the count array is allocated, and no sorted copy exists.

```java run
import java.util.Arrays;
import java.util.Random;

public final class HeightChecker {
    /**
     * Counts positions whose value differs from the sorted order, using counting sort logic.
     * Time: O(n + D) with D = 100, because counting and the slot walk are both linear.
     * Space: O(D), because only the count array is stored.
     * Invariant: idx equals the number of expected values already compared.
     */
    static int heightChecker(int[] heights) {
        // Slots 1..100 hold the counts; slot 0 stays unused.
        int[] count = new int[101];
        // Counting pass: one increment per height, which costs O(n).
        for (int h : heights) count[h]++;
        // The position index follows the sorted sequence without storing it.
        int idx = 0;
        // The mismatch counter is the answer.
        int mismatches = 0;
        // Walk the slots in increasing order, which produces the values in sorted order.
        for (int v = 1; v <= 100; v++) {
            // Each slot contributes count[v] copies of v to the sorted sequence.
            for (int c = 0; c < count[v]; c++) {
                // Compare the expected value v with the original value at this position.
                if (heights[idx] != v) mismatches++;
                // Move to the next expected position.
                idx++;
            }
        }
        // Return the number of positions that differ from the sorted order.
        return mismatches;
    }

    public static void main(String[] args) {
        // Checks Example 1: positions 0, 1 and 3 differ from [1, 2, 2, 3, 3].
        if (heightChecker(new int[] {3, 1, 2, 2, 3}) != 3) throw new AssertionError("example 1");
        // Checks Example 2: an input already in order and a single element give 0.
        if (heightChecker(new int[] {4, 4, 9}) != 0) throw new AssertionError("already sorted");
        if (heightChecker(new int[] {100}) != 0) throw new AssertionError("single element at the top of the range");
        // Checks that the input is not modified.
        int[] a = {5, 2, 5};
        int[] snapshot = a.clone();
        heightChecker(a);
        if (!Arrays.equals(a, snapshot)) throw new AssertionError("input must stay unchanged");
        // Checks the method against a comparison sort on 3,000 random arrays with values in 1..100.
        Random rnd = new Random(53);
        for (int t = 0; t < 3000; t++) {
            int[] x = new int[1 + rnd.nextInt(15)];
            for (int i = 0; i < x.length; i++) x[i] = rnd.nextInt(2) == 0 ? 1 + rnd.nextInt(100) : 1 + rnd.nextInt(3);
            int[] sorted = x.clone();
            Arrays.sort(sorted);
            int expected = 0;
            for (int i = 0; i < x.length; i++) if (x[i] != sorted[i]) expected++;
            if (heightChecker(x) != expected) throw new AssertionError("mismatch " + Arrays.toString(x));
        }
    }
}
```
