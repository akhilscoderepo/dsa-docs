<!-- solutions-for: 08-two-pointers -->
### Solutions For Reading Ahead And Writing Behind

#### Solution: [Build] Remove Element (LeetCode 27)
<!-- id: tp-remove-element -->

**Approach.**
The read index visits every slot once. A value that differs from `val` is copied to the write index, and the write index advances. A value that equals `val` is skipped, so it never enters the output. The invariant is that the first `write` slots hold the values that differ from `val` among the slots already read, in input order. The copy is safe because `write <= read`, so it never overwrites an unread value.

**Complexity.**
- **Time** is O(n), because the loop runs once per slot and each step does one comparison and at most one copy.
- **Space** is O(1), because the method keeps two indexes and edits the array in place.

```java run
import java.util.Arrays;
import java.util.Random;

public final class RemoveElement27 {
    /**
     * Removes val in place and returns the count of kept values.
     * Time: O(n), one pass.
     * Space: O(1).
     * Invariant: nums[0..write-1] holds the kept values among nums[0..read-1], in order.
     */
    static int removeElement(int[] nums, int val) {
        // write is both the next free slot and the number of kept values.
        int write = 0;
        // read visits each slot once, so the loop costs n steps.
        for (int read = 0; read < nums.length; read++) {
            // Only a value that differs from val is admitted.
            if (nums[read] != val) {
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
        int k = removeElement(a, 4);
        if (k != 3 || !Arrays.equals(Arrays.copyOf(a, k), new int[] {1, 2, 3})) throw new AssertionError("example 1");
        if (removeElement(new int[] {7, 7}, 7) != 0) throw new AssertionError("example 2");
        // The empty array returns zero, and a value absent from the array changes nothing.
        if (removeElement(new int[0], 1) != 0) throw new AssertionError("empty");
        int[] same = {1, 2, 3};
        if (removeElement(same, 9) != 3 || !Arrays.equals(same, new int[] {1, 2, 3})) throw new AssertionError("absent");
        // Random arrays against a filter that builds a new list.
        Random rnd = new Random(21);
        for (int t = 0; t < 4000; t++) {
            int[] x = rnd.ints(rnd.nextInt(10), 0, 4).toArray();
            int val = rnd.nextInt(4);
            int[] expect = Arrays.stream(x).filter(v -> v != val).toArray();
            int[] y = x.clone();
            int got = removeElement(y, val);
            if (got != expect.length || !Arrays.equals(Arrays.copyOf(y, got), expect)) throw new AssertionError("random");
        }
    }
}
```

#### Solution: [Vary] Move Zeroes (LeetCode 283)
<!-- id: tp-move-zeroes -->

**Approach.**
The method first compacts the nonzero values to the front with the same read and write indexes. The slots from `write` to the end then hold stale values, so a second loop fills them with zeros. The result keeps the nonzero values in order and puts all zeros last. The invariant of the first loop is that `nums[0..write-1]` holds the nonzero values read so far. The method skips the copy when `read == write`, so a value that is already in place is not rewritten.

**Complexity.**
- **Time** is O(n), because the first loop reads each slot once and the second loop writes at most `n - write` zeros.
- **Space** is O(1), because both loops edit the array in place.

```java run
import java.util.Arrays;
import java.util.Random;

public final class MoveZeroes283 {
    /**
     * Moves all zeros to the end and keeps the order of nonzero values.
     * Time: O(n), two passes.
     * Space: O(1).
     * Invariant: after the first loop, nums[0..write-1] holds the nonzero values in order.
     */
    static void moveZeroes(int[] nums) {
        int write = 0;
        // The first pass compacts the nonzero values.
        for (int read = 0; read < nums.length; read++) {
            if (nums[read] != 0) {
                // A value already in its final slot needs no write.
                if (read != write) nums[write] = nums[read];
                write++;
            }
        }
        // The stale suffix holds old values, so it must become zeros.
        for (int i = write; i < nums.length; i++) nums[i] = 0;
    }

    public static void main(String[] args) {
        // The statement examples.
        int[] a = {0, 3, 0, -2, 5};
        moveZeroes(a);
        if (!Arrays.equals(a, new int[] {3, -2, 5, 0, 0})) throw new AssertionError("example 1");
        int[] b = {1, 2};
        moveZeroes(b);
        if (!Arrays.equals(b, new int[] {1, 2})) throw new AssertionError("example 2");
        // The empty array and an all-zero array are valid.
        moveZeroes(new int[0]);
        int[] z = {0, 0, 0};
        moveZeroes(z);
        if (!Arrays.equals(z, new int[] {0, 0, 0})) throw new AssertionError("zeros");
        // Random arrays against a stable two-list rebuild.
        Random rnd = new Random(22);
        for (int t = 0; t < 4000; t++) {
            int[] x = rnd.ints(rnd.nextInt(9), -2, 3).toArray();
            int[] expect = new int[x.length];
            int p = 0;
            for (int v : x) if (v != 0) expect[p++] = v;
            int[] y = x.clone();
            moveZeroes(y);
            if (!Arrays.equals(y, expect)) throw new AssertionError("random");
        }
    }
}
```

#### Solution: [Boundary] Remove Duplicates From Sorted Array (LeetCode 26)
<!-- id: tp-dedup-sorted -->

**Approach.**
In a sorted array equal values are adjacent, so a value is new exactly when it differs from the last kept value. The method admits the first value without a comparison, which handles the empty array by a guard. Each later value is compared with `nums[write - 1]`, the last slot of the kept prefix. A value in a run of length one differs from its predecessor and is admitted. The invariant is that the kept prefix holds each distinct value read so far once, in sorted order.

**Complexity.**
- **Time** is O(n), because one pass makes one comparison per slot.
- **Space** is O(1), because the kept prefix lives inside the input array.

```java run
import java.util.Arrays;
import java.util.Random;

public final class DedupSorted26 {
    /**
     * Keeps one copy of each distinct value of a sorted array and returns the count.
     * Time: O(n).
     * Space: O(1).
     * Invariant: nums[0..write-1] lists the distinct values read so far, sorted.
     */
    static int dedup(int[] nums) {
        // An empty array has no distinct values, and the guard protects nums[write - 1].
        if (nums.length == 0) return 0;
        // The first value is always kept, so the prefix starts with length one.
        int write = 1;
        for (int read = 1; read < nums.length; read++) {
            // A value that differs from the last kept value starts a new run.
            if (nums[read] != nums[write - 1]) {
                nums[write] = nums[read];
                write++;
            }
        }
        return write;
    }

    public static void main(String[] args) {
        // The statement examples.
        int[] a = {2, 2, 5, 7, 7, 7, 9};
        int k = dedup(a);
        if (k != 4 || !Arrays.equals(Arrays.copyOf(a, k), new int[] {2, 5, 7, 9})) throw new AssertionError("example 1");
        if (dedup(new int[0]) != 0) throw new AssertionError("example 2");
        // One value and all-equal values.
        if (dedup(new int[] {8}) != 1) throw new AssertionError("single");
        if (dedup(new int[] {4, 4, 4}) != 1) throw new AssertionError("all equal");
        // Random sorted arrays against a TreeSet rebuild.
        Random rnd = new Random(23);
        for (int t = 0; t < 4000; t++) {
            int[] x = rnd.ints(rnd.nextInt(10), -3, 4).sorted().toArray();
            int[] expect = Arrays.stream(x).distinct().toArray();
            int[] y = x.clone();
            int got = dedup(y);
            if (got != expect.length || !Arrays.equals(Arrays.copyOf(y, got), expect)) throw new AssertionError("random");
        }
    }
}
```

#### Solution: [Recognize] Remove Duplicates From Sorted Array II (LeetCode 80)
<!-- id: tp-dedup-twice -->

**Approach.**
The method keeps the first two values unconditionally. A later value is admitted when it differs from `nums[write - 2]`, the value two slots behind the next free slot. In a sorted array, equality with that value means the kept prefix already ends with two copies. The test reads the kept prefix and never `nums[read - 2]`, because an earlier write may have overwritten that slot. The invariant is that no value appears three times in `nums[0..write-1]`.

**Complexity.**
- **Time** is O(n), because each slot gets one comparison and at most one copy.
- **Space** is O(1), because the result lives in the input array.

```java run
import java.util.Arrays;
import java.util.Random;

public final class DedupTwice80 {
    /**
     * Keeps at most two copies of each value of a sorted array and returns the new length.
     * Time: O(n).
     * Space: O(1).
     * Invariant: nums[0..write-1] is sorted and holds each value at most twice.
     */
    static int dedupTwice(int[] nums) {
        int write = 0;
        for (int read = 0; read < nums.length; read++) {
            // The kept prefix is consulted, because slots behind read may be overwritten.
            if (write < 2 || nums[read] != nums[write - 2]) {
                nums[write] = nums[read];
                write++;
            }
        }
        return write;
    }

    public static void main(String[] args) {
        // The statement examples.
        int[] a = {3, 3, 3, 3, 4, 4, 4};
        int k = dedupTwice(a);
        if (k != 4 || !Arrays.equals(Arrays.copyOf(a, k), new int[] {3, 3, 4, 4})) throw new AssertionError("example 1");
        int[] b = {1, 2, 2, 2, 5};
        int m = dedupTwice(b);
        if (m != 4 || !Arrays.equals(Arrays.copyOf(b, m), new int[] {1, 2, 2, 5})) throw new AssertionError("example 2");
        // The empty array.
        if (dedupTwice(new int[0]) != 0) throw new AssertionError("empty");
        // Random sorted arrays against a count-based rebuild.
        Random rnd = new Random(24);
        for (int t = 0; t < 4000; t++) {
            int[] x = rnd.ints(rnd.nextInt(12), -2, 3).sorted().toArray();
            int[] expect = new int[x.length];
            int p = 0;
            for (int i = 0; i < x.length; i++) {
                int copies = 0;
                for (int j = 0; j < p; j++) if (expect[j] == x[i]) copies++;
                if (copies < 2) expect[p++] = x[i];
            }
            int[] y = x.clone();
            int got = dedupTwice(y);
            if (got != p || !Arrays.equals(Arrays.copyOf(y, got), Arrays.copyOf(expect, p))) throw new AssertionError("random");
        }
    }
}
```
