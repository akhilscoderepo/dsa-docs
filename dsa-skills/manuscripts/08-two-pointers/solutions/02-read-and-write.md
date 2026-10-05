<!-- solutions-for: 08-two-pointers -->
### Solutions For Reading Ahead And Writing Behind

#### Solution: [Build] Remove Element (LeetCode 27)
<!-- id: tp-remove-element -->

**Approach.**
The read index visits every slot once. A value that equals `val` is skipped while the count of removals is below `limit`, and the counter grows by one for each skip. Every other value is copied to the write index, and the write index advances. After the limit is reached, later copies of `val` are kept. The invariant is that the first `write` slots hold the kept values among the slots already read, in input order, and that `removed` equals the number of skipped values. The copy is safe because `write <= read`, so it never overwrites an unread value.

**Complexity.**
- **Time** is O(n), because the loop runs once per slot and each step does a constant number of operations.
- **Space** is O(1), because the method keeps three integers and edits the array in place.

```java run
import java.util.Arrays;
import java.util.Random;

public final class RemoveElement27 {
    /**
     * Removes the first limit occurrences of val in place and returns the new length.
     * Time: O(n), one pass.
     * Space: O(1).
     * Invariant: nums[0..write-1] holds the kept values among nums[0..read-1], in order.
     */
    static int removeFirst(int[] nums, int val, int limit) {
        // write is both the next free slot and the number of kept values.
        int write = 0;
        // removed counts the skipped occurrences of val.
        int removed = 0;
        // read visits each slot once, so the loop costs n steps.
        for (int read = 0; read < nums.length; read++) {
            // A value equal to val is skipped only while removals remain.
            if (nums[read] == val && removed < limit) {
                removed++;
            } else {
                // The slot write is at or behind read, so no unread value is lost.
                nums[write] = nums[read];
                write++;
            }
        }
        return write;
    }

    public static void main(String[] args) {
        // The statement examples.
        int[] a = {4, 1, 4, 2, 4, 3};
        int k = removeFirst(a, 4, 2);
        if (k != 4 || !Arrays.equals(Arrays.copyOf(a, k), new int[] {1, 2, 4, 3})) throw new AssertionError("example 1");
        int[] b = {7, 7};
        if (removeFirst(b, 7, 0) != 2 || !Arrays.equals(b, new int[] {7, 7})) throw new AssertionError("example 2");
        // The empty array returns zero.
        if (removeFirst(new int[0], 1, 3) != 0) throw new AssertionError("empty");
        // A limit above the number of occurrences removes them all.
        int[] c = {5, 5, 1};
        if (removeFirst(c, 5, 10) != 1 || c[0] != 1) throw new AssertionError("large limit");
        // Random arrays against a list that applies the same rule.
        Random rnd = new Random(21);
        for (int t = 0; t < 4000; t++) {
            int[] x = rnd.ints(rnd.nextInt(10), 0, 4).toArray();
            int val = rnd.nextInt(4), limit = rnd.nextInt(5);
            java.util.List<Integer> expect = new java.util.ArrayList<>();
            int seen = 0;
            for (int v : x) { if (v == val && seen < limit) seen++; else expect.add(v); }
            int[] y = x.clone();
            int got = removeFirst(y, val, limit);
            if (got != expect.size()) throw new AssertionError("length");
            for (int i = 0; i < got; i++) if (y[i] != expect.get(i)) throw new AssertionError("random");
        }
    }
}
```

#### Solution: [Vary] Move Zeroes (LeetCode 283)
<!-- id: tp-move-zeroes -->

**Approach.**
The kept values must end at the back, so both indexes run from the last slot toward the first. The read index starts at the last slot, and the write index also starts there. A nonzero value is copied to the write index, and the write index moves left. After the scan, the slots from index 0 to the write index hold stale values, so a second loop fills them with zeros. The invariant is that the slots after `write` hold the nonzero values read so far, in their original order. The copy is safe because `write >= read`.

**Complexity.**
- **Time** is O(n), because the first loop reads each slot once and the second loop writes at most `n` zeros.
- **Space** is O(1), because both loops edit the array in place.

```java run
import java.util.Arrays;
import java.util.Random;

public final class MoveZeroesFront {
    /**
     * Moves all zeros to the front and keeps the order of nonzero values.
     * Time: O(n), two passes.
     * Space: O(1).
     * Invariant: nums[write+1..n-1] holds the nonzero values read so far, in order.
     */
    static void zerosToFront(int[] nums) {
        int write = nums.length - 1;
        // The scan runs from the last slot, so the kept values build a suffix.
        for (int read = nums.length - 1; read >= 0; read--) {
            if (nums[read] != 0) {
                // A value already in its final slot needs no write.
                if (read != write) nums[write] = nums[read];
                write--;
            }
        }
        // Slots 0..write are stale, and they must become zeros.
        for (int i = write; i >= 0; i--) nums[i] = 0;
    }

    public static void main(String[] args) {
        // The statement examples.
        int[] a = {0, 3, 0, -2, 5};
        zerosToFront(a);
        if (!Arrays.equals(a, new int[] {0, 0, 3, -2, 5})) throw new AssertionError("example 1");
        int[] b = {1, 2};
        zerosToFront(b);
        if (!Arrays.equals(b, new int[] {1, 2})) throw new AssertionError("example 2");
        // The empty array and an all-zero array are valid.
        zerosToFront(new int[0]);
        int[] z = {0, 0, 0};
        zerosToFront(z);
        if (!Arrays.equals(z, new int[] {0, 0, 0})) throw new AssertionError("zeros");
        // Random arrays against a rebuild with zeros first.
        Random rnd = new Random(22);
        for (int t = 0; t < 4000; t++) {
            int[] x = rnd.ints(rnd.nextInt(9), -2, 3).toArray();
            int zeros = 0;
            for (int v : x) if (v == 0) zeros++;
            int[] expect = new int[x.length];
            int p = zeros;
            for (int v : x) if (v != 0) expect[p++] = v;
            int[] y = x.clone();
            zerosToFront(y);
            if (!Arrays.equals(y, expect)) throw new AssertionError("random");
        }
    }
}
```

#### Solution: [Boundary] Remove Duplicates From Sorted Array (LeetCode 26)
<!-- id: tp-dedup-sorted -->

**Approach.**
The array is not sorted, so only equal adjacent values collapse. A value is new exactly when it differs from the last kept value, because the last kept value is the last value of the previous block. The first value is admitted by the test `write == 0`, which also covers the empty array. A value in a block of length one differs from its predecessor and is admitted. Two equal values that are separated by a different value both stay. The invariant is that the kept prefix equals the input read so far with each block of equal adjacent values reduced to one copy.

**Complexity.**
- **Time** is O(n), because one pass makes one comparison per slot.
- **Space** is O(1), because the kept prefix lives inside the input array.

```java run
import java.util.Arrays;
import java.util.Random;

public final class CollapseAdjacent26 {
    /**
     * Collapses blocks of equal adjacent values in place and returns the new length.
     * Time: O(n).
     * Space: O(1).
     * Invariant: nums[0..write-1] is the input read so far with each adjacent block reduced to one value.
     */
    static int collapse(int[] nums) {
        int write = 0;
        for (int read = 0; read < nums.length; read++) {
            // The first value has no predecessor in the kept prefix, so it is always admitted.
            if (write == 0 || nums[read] != nums[write - 1]) {
                nums[write] = nums[read];
                write++;
            }
        }
        return write;
    }

    public static void main(String[] args) {
        // The statement examples.
        int[] a = {2, 2, 5, 2, 2, 2, 9};
        int k = collapse(a);
        if (k != 4 || !Arrays.equals(Arrays.copyOf(a, k), new int[] {2, 5, 2, 9})) throw new AssertionError("example 1");
        if (collapse(new int[0]) != 0) throw new AssertionError("example 2");
        // One value and all-equal values.
        if (collapse(new int[] {8}) != 1) throw new AssertionError("single");
        if (collapse(new int[] {4, 4, 4}) != 1) throw new AssertionError("all equal");
        // Random arrays against a list that adds a value when it differs from the list's last value.
        Random rnd = new Random(23);
        for (int t = 0; t < 4000; t++) {
            int[] x = rnd.ints(rnd.nextInt(10), -2, 3).toArray();
            java.util.List<Integer> expect = new java.util.ArrayList<>();
            for (int v : x) if (expect.isEmpty() || expect.get(expect.size() - 1) != v) expect.add(v);
            int[] y = x.clone();
            int got = collapse(y);
            if (got != expect.size()) throw new AssertionError("length");
            for (int i = 0; i < got; i++) if (y[i] != expect.get(i)) throw new AssertionError("random");
        }
    }
}
```

#### Solution: [Recognize] Remove Duplicates From Sorted Array II (LeetCode 80)
<!-- id: tp-dedup-twice -->

**Approach.**
The method keeps the first `k` values unconditionally. A later value is admitted when it differs from `nums[write - k]`, the value `k` slots behind the next free slot. In a sorted array, equality with that value means the kept prefix already ends with `k` copies of the candidate. The test reads the kept prefix and never `nums[read - k]`, because an earlier write may have overwritten that slot. With `k = 1` the rule becomes plain deduplication. The invariant is that no value appears more than `k` times in `nums[0..write-1]`.

**Complexity.**
- **Time** is O(n), because each slot gets one comparison and at most one copy.
- **Space** is O(1), because the result lives in the input array.

```java run
import java.util.Arrays;
import java.util.Random;

public final class DedupAtMostK80 {
    /**
     * Keeps at most k copies of each value of a sorted array and returns the new length.
     * Time: O(n).
     * Space: O(1).
     * Invariant: nums[0..write-1] is sorted and holds each value at most k times.
     */
    static int keepAtMost(int[] nums, int k) {
        int write = 0;
        for (int read = 0; read < nums.length; read++) {
            // The kept prefix is consulted, because slots behind read may be overwritten.
            if (write < k || nums[read] != nums[write - k]) {
                nums[write] = nums[read];
                write++;
            }
        }
        return write;
    }

    public static void main(String[] args) {
        // The statement examples.
        int[] a = {3, 3, 3, 3, 4, 4, 4};
        int m = keepAtMost(a, 3);
        if (m != 6 || !Arrays.equals(Arrays.copyOf(a, m), new int[] {3, 3, 3, 4, 4, 4})) throw new AssertionError("example 1");
        int[] b = {1, 2, 2, 2, 5};
        int q = keepAtMost(b, 1);
        if (q != 3 || !Arrays.equals(Arrays.copyOf(b, q), new int[] {1, 2, 5})) throw new AssertionError("example 2");
        // The empty array.
        if (keepAtMost(new int[0], 2) != 0) throw new AssertionError("empty");
        // Random sorted arrays against a count-based rebuild.
        Random rnd = new Random(24);
        for (int t = 0; t < 4000; t++) {
            int[] x = rnd.ints(rnd.nextInt(12), -2, 3).sorted().toArray();
            int k = 1 + rnd.nextInt(3);
            int[] expect = new int[x.length];
            int p = 0;
            for (int i = 0; i < x.length; i++) {
                int copies = 0;
                for (int j = 0; j < p; j++) if (expect[j] == x[i]) copies++;
                if (copies < k) expect[p++] = x[i];
            }
            int[] y = x.clone();
            int got = keepAtMost(y, k);
            if (got != p || !Arrays.equals(Arrays.copyOf(y, got), Arrays.copyOf(expect, p))) throw new AssertionError("random");
        }
    }
}
```
