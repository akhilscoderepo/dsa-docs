<!-- solutions-for: 06-frequency-arrays -->
### Frequency Arrays

#### Solution: [Build] Digit Counts (Author exercise)
<!-- id: ar-digit-counts -->

**Approach.** Allocate ten slots, which Java zero-fills, and increment `count[d]` for every digit. After processing a prefix, each slot holds the number of times its digit occurred in that prefix. An empty input leaves all ten slots at zero, matching the second example. The assertions compare the table against a brute-force count for every digit on random inputs and check that the counts sum to the input length.

**Complexity.** O(n) time and O(1) space, since the table has a fixed ten slots.

```java run
import java.util.Arrays;
import java.util.Random;

public final class DigitCounts {
    static int[] digitCounts(int[] digits) {
        int[] count = new int[10];
        for (int d : digits) count[d]++;
        return count;
    }

    public static void main(String[] args) {
        if (!Arrays.equals(digitCounts(new int[] {2, 0, 2}), new int[] {1, 0, 2, 0, 0, 0, 0, 0, 0, 0})) throw new AssertionError("example 1");
        if (!Arrays.equals(digitCounts(new int[] {}), new int[10])) throw new AssertionError("example 2");
        Random rnd = new Random(21);
        for (int t = 0; t < 2000; t++) {
            int[] x = new int[rnd.nextInt(30)];
            for (int i = 0; i < x.length; i++) x[i] = rnd.nextInt(10);
            int[] got = digitCounts(x);
            int total = 0;
            for (int d = 0; d < 10; d++) {
                int expected = 0;
                for (int v : x) if (v == d) expected++;
                if (got[d] != expected) throw new AssertionError("digit " + d);
                total += got[d];
            }
            if (total != x.length) throw new AssertionError("counts must sum to the length");
        }
    }
}
```

#### Solution: [Vary] How Many Numbers Are Smaller Than the Current Number (LeetCode 1365)
<!-- id: ar-smaller-than-current -->

**Approach.** Count the occurrences of each value in a table of 101 slots, then build `below`, where `below[v]` is the sum of the counts of all values smaller than `v`. Each element's answer is then `below[nums[i]]`, a single lookup. Shifting `below` by one slot removes the special case at value zero, and equal values correctly contribute nothing to each other's answers because only strictly smaller slots are summed. The pair-loop brute force serves as the oracle.

**Complexity.** O(n + V) time with V = 101, and O(V) extra space plus the output.

```java run
import java.util.Arrays;
import java.util.Random;

public final class SmallerThanCurrent {
    static int[] smallerNumbers(int[] nums) {
        int[] count = new int[101];
        for (int v : nums) count[v]++;
        int[] below = new int[102];
        for (int v = 0; v <= 100; v++) below[v + 1] = below[v] + count[v];
        int[] out = new int[nums.length];
        for (int i = 0; i < nums.length; i++) out[i] = below[nums[i]];
        return out;
    }
    static int[] oracle(int[] nums) {
        int[] out = new int[nums.length];
        for (int i = 0; i < nums.length; i++) for (int j = 0; j < nums.length; j++) if (nums[j] < nums[i]) out[i]++;
        return out;
    }

    public static void main(String[] args) {
        if (!Arrays.equals(smallerNumbers(new int[] {6, 5, 4, 8}), new int[] {2, 1, 0, 3})) throw new AssertionError("example 1");
        if (!Arrays.equals(smallerNumbers(new int[] {7, 7, 7}), new int[] {0, 0, 0})) throw new AssertionError("example 2");
        if (!Arrays.equals(smallerNumbers(new int[] {0, 100}), new int[] {0, 1})) throw new AssertionError("range endpoints");
        Random rnd = new Random(22);
        for (int t = 0; t < 2000; t++) {
            int[] x = new int[2 + rnd.nextInt(20)];
            for (int i = 0; i < x.length; i++) x[i] = rnd.nextInt(101);
            if (!Arrays.equals(smallerNumbers(x), oracle(x))) throw new AssertionError("disagrees with the pair loop");
        }
    }
}
```

#### Solution: [Boundary] Dice Validation (Author exercise)
<!-- id: ar-dice-validation -->

**Approach.** Check `1 <= roll <= 6` before indexing and reject anything else. The method throws `IllegalArgumentException` with the offending value, and it validates the whole input before returning any counts, so a bad roll never produces a half-built table. Without the check, a roll of 0 would increment the unused slot 0 and silently disappear from the result, while a roll of 9 would throw an unrelated out-of-bounds exception. The assertions show both failure modes of the unchecked version.

**Complexity.** O(n) time and O(1) space, with a seven-slot table.

```java run
import java.util.Arrays;

public final class DiceValidation {
    static int[] diceCounts(int[] rolls) {
        int[] count = new int[7];
        for (int r : rolls) {
            if (r < 1 || r > 6) throw new IllegalArgumentException("not a die face: " + r);
            count[r]++;
        }
        return count;
    }
    static int[] unchecked(int[] rolls) {
        int[] count = new int[7];
        for (int r : rolls) count[r]++;
        return count;
    }

    public static void main(String[] args) {
        int[] ok = diceCounts(new int[] {1, 6, 6});
        if (ok[1] != 1 || ok[6] != 2 || ok[2] != 0) throw new AssertionError("valid rolls");
        boolean rejected = false;
        try { diceCounts(new int[] {1, 6, 0}); } catch (IllegalArgumentException e) { rejected = e.getMessage().endsWith("0"); }
        if (!rejected) throw new AssertionError("a roll of 0 must be rejected before indexing");
        int[] silent = unchecked(new int[] {1, 6, 0});
        if (silent[0] != 1) throw new AssertionError("the unchecked version hides the bad roll in the unused slot 0");
        boolean crashed = false;
        try { unchecked(new int[] {9}); } catch (ArrayIndexOutOfBoundsException e) { crashed = true; }
        if (!crashed) throw new AssertionError("the unchecked version fails with an unrelated exception on 9");
        if (!Arrays.equals(diceCounts(new int[] {}), new int[7])) throw new AssertionError("empty input");
    }
}
```

#### Solution: [Recognize] Height Checker (LeetCode 1051)
<!-- id: ar-height-checker -->

**Approach.** Count the heights in a table of 101 slots. Then walk the table in increasing order and, for each height `h`, consume its count while comparing against the input position that the sorted line would place there, advancing a position counter. A mismatch increments the answer. No sorted array is built and no comparison sort is used. The input array is read-only throughout, and the check against `Arrays.sort` on a copy confirms the sorted order is reproduced by the table walk.

**Complexity.** O(n + V) time with V = 101 and O(V) extra space.

```java run
import java.util.Arrays;
import java.util.Random;

public final class HeightChecker {
    static int mismatches(int[] heights) {
        int[] count = new int[101];
        for (int h : heights) count[h]++;
        int pos = 0, wrong = 0;
        for (int h = 1; h <= 100; h++) {
            while (count[h]-- > 0) {
                if (heights[pos] != h) wrong++;
                pos++;
            }
        }
        return wrong;
    }
    static int oracle(int[] heights) {
        int[] sorted = heights.clone();
        Arrays.sort(sorted);
        int wrong = 0;
        for (int i = 0; i < heights.length; i++) if (heights[i] != sorted[i]) wrong++;
        return wrong;
    }

    public static void main(String[] args) {
        int[] a = {2, 1, 3, 3, 4};
        int[] snapshot = a.clone();
        if (mismatches(a) != 2) throw new AssertionError("example 1");
        if (!Arrays.equals(a, snapshot)) throw new AssertionError("input untouched");
        if (mismatches(new int[] {1, 2, 3}) != 0) throw new AssertionError("example 2");
        Random rnd = new Random(23);
        for (int t = 0; t < 3000; t++) {
            int[] x = new int[1 + rnd.nextInt(15)];
            for (int i = 0; i < x.length; i++) x[i] = 1 + rnd.nextInt(100);
            if (mismatches(x) != oracle(x)) throw new AssertionError("disagrees with comparison sorting");
        }
    }
}
```
