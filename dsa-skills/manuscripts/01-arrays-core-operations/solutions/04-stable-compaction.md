<!-- solutions-for: 01-arrays-core-operations -->
### Solutions For Stable Compaction

#### Solution: [Build] Remove Element (LeetCode 27)
<!-- id: ar-remove-element -->

**Approach.** The method scans the array once with a read index and keeps a write index at the next free position of the accepted prefix. Each value that differs from `val` is copied to the write index, and the write index then advances. A value equal to `val` is skipped.

The invariant is that `nums[0..write-1]` holds the accepted values read so far, in order. The write index never exceeds the read index, so a copy never destroys an unread value. The return value is the write index. The harness compares the prefix against a list filter on 3,000 random arrays, and it checks that the array length stays unchanged.

**Complexity.**

- **Time** is O(n), because each position is read once and written at most once.
- **Space** is O(1), because the method stores only two indexes.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

public final class RemoveElement {
    /**
     * Overwrites the prefix of nums with every value not equal to val and returns its length.
     * Time: O(n), because each position is read once.
     * Space: O(1), because only two indexes are stored.
     * Invariant: nums[0..write-1] holds the accepted values read so far, in input order.
     */
    static int removeElement(int[] nums, int val) {
        // The write index is the next free position of the accepted prefix; it starts empty.
        int write = 0;
        // The read index visits every position once, which gives the O(n) time.
        for (int read = 0; read < nums.length; read++) {
            // A value different from val is accepted.
            if (nums[read] != val) {
                // Copy the accepted value to the free position; write <= read, so no unread value is lost.
                nums[write] = nums[read];
                // Grow the accepted prefix by one, which keeps the invariant true.
                write++;
            }
        }
        // The write index equals the count of accepted values, which is the contract's return value.
        return write;
    }

    /** Reference answer built with a list filter, used only to check the in-place method. */
    static List<Integer> oracle(int[] nums, int val) {
        // The list holds the expected kept values in order.
        List<Integer> kept = new ArrayList<>();
        // Visit every value and keep the ones that differ from val.
        for (int v : nums) if (v != val) kept.add(v);
        // Return the expected sequence.
        return kept;
    }

    public static void main(String[] args) {
        // Checks Example 1: three values stay, in order.
        int[] a = {4, 7, 4, 9, 4, 2};
        int k = removeElement(a, 4);
        if (k != 3 || !Arrays.equals(Arrays.copyOf(a, k), new int[] {7, 9, 2})) throw new AssertionError("example 1");
        // Checks Example 2: removing every value returns 0, and an empty array also returns 0.
        if (removeElement(new int[] {6, 6, 6}, 6) != 0) throw new AssertionError("all removed");
        if (removeElement(new int[0], 1) != 0) throw new AssertionError("empty input");
        // Checks the contract claim that the array length never changes.
        if (a.length != 6) throw new AssertionError("length is fixed");
        // Checks the method against the oracle on 3,000 random arrays with small values.
        Random rnd = new Random(11);
        for (int t = 0; t < 3000; t++) {
            int[] x = new int[rnd.nextInt(10)];
            for (int i = 0; i < x.length; i++) x[i] = rnd.nextInt(5);
            int val = rnd.nextInt(5);
            List<Integer> expected = oracle(x, val);
            int got = removeElement(x, val);
            if (got != expected.size()) throw new AssertionError("count mismatch");
            for (int i = 0; i < got; i++) if (x[i] != expected.get(i)) throw new AssertionError("prefix mismatch");
        }
    }
}
```

#### Solution: [Vary] Move Zeroes (LeetCode 283)
<!-- id: ar-move-zeroes -->

**Approach.** The method first compacts the non-zero values to the front with the read and write indexes. After that pass, the write index is the count of non-zero values, and the positions from `write` onward hold stale values. A second loop fills those positions with zeros.

Non-zero values keep their relative order because the first pass is a stable compaction. The second pass runs over `n - write` positions, so the total stays linear. The harness checks the result against a list-based oracle on random arrays and checks that a no-zero array stays unchanged.

**Complexity.**

- **Time** is O(n), because the compaction pass costs n reads and the fill pass costs at most n writes.
- **Space** is O(1), because the method stores two indexes.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

public final class MoveZeroes {
    /**
     * Moves every zero to the end while keeping non-zero values in their original order.
     * Time: O(n), because there is one compaction pass and one fill pass.
     * Space: O(1), because only two indexes are stored.
     * Invariant: after each read step, nums[0..write-1] holds the non-zero values read so far, in order.
     */
    static void moveZeroes(int[] nums) {
        // The write index marks the next free position of the non-zero prefix.
        int write = 0;
        // The read index visits each position once.
        for (int read = 0; read < nums.length; read++) {
            // Only non-zero values are accepted into the prefix.
            if (nums[read] != 0) {
                // Copy the value forward; write <= read, so the unread part is intact.
                nums[write] = nums[read];
                // Extend the prefix by one position.
                write++;
            }
        }
        // The positions from write onward hold stale values, so overwrite each one with zero.
        for (int i = write; i < nums.length; i++) nums[i] = 0;
    }

    /** Reference answer: non-zero values in order, then zeros, built in a new array. */
    static int[] oracle(int[] nums) {
        // Collect the non-zero values in order.
        List<Integer> out = new ArrayList<>();
        for (int v : nums) if (v != 0) out.add(v);
        // Pad with zeros until the original length is reached.
        while (out.size() < nums.length) out.add(0);
        // Convert the list to an array for comparison.
        return out.stream().mapToInt(Integer::intValue).toArray();
    }

    public static void main(String[] args) {
        // Checks Example 1: zeros move to the end and the other values keep their order.
        int[] a = {0, 0, 5, 0, -2, 7};
        moveZeroes(a);
        if (!Arrays.equals(a, new int[] {5, -2, 7, 0, 0, 0})) throw new AssertionError("example 1");
        // Checks Example 2: an all-zero array and a no-zero array stay as they are.
        int[] z = {0, 0, 0};
        moveZeroes(z);
        if (!Arrays.equals(z, new int[] {0, 0, 0})) throw new AssertionError("all zeros");
        int[] n = {3, 1};
        moveZeroes(n);
        if (!Arrays.equals(n, new int[] {3, 1})) throw new AssertionError("no zeros");
        // Checks the method against the oracle on 3,000 random arrays with values in -2..2.
        Random rnd = new Random(13);
        for (int t = 0; t < 3000; t++) {
            int[] x = new int[1 + rnd.nextInt(10)];
            for (int i = 0; i < x.length; i++) x[i] = rnd.nextInt(5) - 2;
            int[] expected = oracle(x);
            moveZeroes(x);
            if (!Arrays.equals(x, expected)) throw new AssertionError("mismatch " + Arrays.toString(expected));
        }
    }
}
```

#### Solution: [Boundary] Keep Evens (Author exercise)
<!-- id: ar-keep-evens -->

**Approach.** The method is the compaction loop with an evenness test. The test compares the remainder with zero, because Java gives a remainder with the sign of the dividend. The value `-3` has remainder `-1`, so a comparison with `1` would misclassify negative odd values, while a comparison with `0` is correct for every sign.

The loop keeps the prefix `nums[0..write-1]` holds the even values read so far, in order. The harness asserts the Java remainder facts that justify the test, and then checks the method against a list filter on random arrays with negative values.

**Complexity.**

- **Time** is O(n), because the loop reads every position once and writes each accepted value once.
- **Space** is O(1), because two index variables are the only extra storage.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

public final class KeepEvens {
    /**
     * Overwrites the prefix of nums with its even values and returns how many there are.
     * Time: O(n), because each position is read once.
     * Space: O(1), because only two indexes are stored.
     * Invariant: nums[0..write-1] holds the even values read so far, in input order.
     */
    static int keepEvens(int[] nums) {
        // The write index is the next free position of the accepted prefix.
        int write = 0;
        // The read index visits every position once.
        for (int read = 0; read < nums.length; read++) {
            // Compare the remainder with 0, which is correct for negative values too.
            if (nums[read] % 2 == 0) {
                // Copy the even value to the free position of the prefix.
                nums[write] = nums[read];
                // Extend the prefix by one position.
                write++;
            }
        }
        // The write index is the count of even values.
        return write;
    }

    public static void main(String[] args) {
        // Checks the Java remainder facts: a negative odd value has remainder -1, and a negative even value has 0.
        if (-3 % 2 != -1) throw new AssertionError("remainder of -3");
        if (-4 % 2 != 0) throw new AssertionError("remainder of -4");
        // Checks Example 1.
        int[] a = {-2, 3, 4};
        int k = keepEvens(a);
        if (k != 2 || !Arrays.equals(Arrays.copyOf(a, k), new int[] {-2, 4})) throw new AssertionError("example 1");
        // Checks Example 2 and the empty input.
        if (keepEvens(new int[] {-3, 1, 5}) != 0) throw new AssertionError("only odd values");
        if (keepEvens(new int[0]) != 0) throw new AssertionError("empty input");
        // Checks the method against a list filter on 3,000 random arrays with values in -6..6.
        Random rnd = new Random(17);
        for (int t = 0; t < 3000; t++) {
            int[] x = new int[rnd.nextInt(10)];
            List<Integer> expected = new ArrayList<>();
            for (int i = 0; i < x.length; i++) {
                x[i] = rnd.nextInt(13) - 6;
                if (Math.floorMod(x[i], 2) == 0) expected.add(x[i]);
            }
            int got = keepEvens(x);
            if (got != expected.size()) throw new AssertionError("count mismatch");
            for (int i = 0; i < got; i++) if (x[i] != expected.get(i)) throw new AssertionError("prefix mismatch");
        }
    }
}
```

#### Solution: [Recognize] Filter Positives (Author exercise)
<!-- id: ar-filter-positives -->

**Approach.** The method keeps the same read index and write index. Only the acceptance test changes, and it becomes `nums[read] > 0`. The comparison with zero excludes zero itself and excludes `Integer.MIN_VALUE`, so no arithmetic runs on the values and no overflow can occur.

The invariant is the same as in the earlier exercises: `nums[0..write-1]` holds the accepted values read so far, in order. The harness checks the method against a list filter on random arrays that include the extreme value.

**Complexity.**

- **Time** is linear, because one pass reads each position and every write follows a read.
- **Space** is constant, because the method adds no array.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

public final class FilterPositives {
    /**
     * Overwrites the prefix of nums with its strictly positive values and returns how many there are.
     * Time: O(n), because each position is read once.
     * Space: O(1), because only two indexes are stored.
     * Invariant: nums[0..write-1] holds the positive values read so far, in input order.
     */
    static int filterPositives(int[] nums) {
        // The write index is the next free position of the accepted prefix.
        int write = 0;
        // The read index visits every position once.
        for (int read = 0; read < nums.length; read++) {
            // A plain comparison rejects zero and every negative value without any arithmetic.
            if (nums[read] > 0) {
                // Copy the positive value to the free position of the prefix.
                nums[write] = nums[read];
                // Extend the prefix by one position.
                write++;
            }
        }
        // The write index is the count of positive values.
        return write;
    }

    public static void main(String[] args) {
        // Checks Example 1.
        int[] a = {3, -1, 0, 5, -7, 2};
        int k = filterPositives(a);
        if (k != 3 || !Arrays.equals(Arrays.copyOf(a, k), new int[] {3, 5, 2})) throw new AssertionError("example 1");
        // Checks Example 2: zero and the smallest int are both rejected.
        if (filterPositives(new int[] {0, -4, Integer.MIN_VALUE}) != 0) throw new AssertionError("no positives");
        // Checks that the largest int is accepted and the empty input returns 0.
        int[] b = {Integer.MAX_VALUE, 0};
        if (filterPositives(b) != 1 || b[0] != Integer.MAX_VALUE) throw new AssertionError("maximum value");
        if (filterPositives(new int[0]) != 0) throw new AssertionError("empty input");
        // Checks the method against a list filter on 3,000 random arrays that include extreme values.
        Random rnd = new Random(19);
        int[] pool = {Integer.MIN_VALUE, -3, -1, 0, 1, 4, Integer.MAX_VALUE};
        for (int t = 0; t < 3000; t++) {
            int[] x = new int[rnd.nextInt(10)];
            List<Integer> expected = new ArrayList<>();
            for (int i = 0; i < x.length; i++) {
                x[i] = pool[rnd.nextInt(pool.length)];
                if (x[i] > 0) expected.add(x[i]);
            }
            int got = filterPositives(x);
            if (got != expected.size()) throw new AssertionError("count mismatch");
            for (int i = 0; i < got; i++) if (x[i] != expected.get(i)) throw new AssertionError("prefix mismatch");
        }
    }
}
```
