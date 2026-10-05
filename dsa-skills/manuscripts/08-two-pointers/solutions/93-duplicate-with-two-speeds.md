<!-- solutions-for: 08-two-pointers -->
### Solutions For Duplicates With Two Speeds

#### Solution: [Build] Value-As-Next-Index (Author exercise)
<!-- id: tp-contract-check -->

**Approach.**
The table has `n + 1` slots, so the legal values are the integers from 1 to `n`. A value above `n` makes a read leave the array when the walk follows it. A value of 0 or below makes the walk return to slot 0 or leave the array, which breaks the claim that the first loop slot is a repeated value. The method scans the slots in order and returns the first index whose value falls outside the range. The invariant is that every slot before the current index holds a legal value.

**Complexity.**
- **Time** is O(n), because the scan reads each slot at most once.
- **Space** is O(1), because the method keeps one index.

```java run
import java.util.Random;

public final class ContractCheck {
    /**
     * Returns the first index whose value is not in 1..n, or -1 when the table is legal.
     * Time: O(n).
     * Space: O(1).
     * Invariant: every slot before i holds a value in 1..n.
     */
    static int firstIllegal(int[] nums) {
        // n is one less than the number of slots, because the table has n + 1 slots.
        int n = nums.length - 1;
        for (int i = 0; i < nums.length; i++) {
            // A value outside 1..n would leave the array or point back to slot 0.
            if (nums[i] < 1 || nums[i] > n) return i;
        }
        return -1;
    }

    public static void main(String[] args) {
        // The statement examples.
        if (firstIllegal(new int[] {3, 1, 3, 4, 2}) != -1) throw new AssertionError("example 1");
        if (firstIllegal(new int[] {1, 3, 2}) != 1) throw new AssertionError("example 2");
        // A value of 0 is illegal even though it is a valid index.
        if (firstIllegal(new int[] {1, 0, 1}) != 1) throw new AssertionError("zero");
        // A legal table never reads outside the array when followed for n + 1 links.
        Random rnd = new Random(101);
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(8);
            int[] a = rnd.ints(n + 1, 0, n + 3).toArray();
            int bad = -1;
            for (int i = 0; i < a.length && bad < 0; i++) if (a[i] < 1 || a[i] > n) bad = i;
            if (firstIllegal(a) != bad) throw new AssertionError("random");
            if (bad < 0) {
                int x = 0;
                for (int step = 0; step <= n + 1; step++) {
                    if (x < 0 || x >= a.length) throw new AssertionError("walk left the array");
                    x = a[x];
                    if (x == 0) throw new AssertionError("walk returned to slot 0");
                }
            }
        }
    }
}
```

#### Solution: [Vary] Find the Duplicate Number (LeetCode 287)
<!-- id: tp-duplicate-count -->

**Approach.**
Phase one runs the slow pointer by one link and the fast pointer by two links until they meet inside the loop. Phase two restarts the slow pointer at slot 0 and moves both pointers one link per round until they meet at the entry point, which is the repeated value `d`. A second pass over the table counts the slots that hold `d`. The pass reads the table and writes nothing. With exactly one repeated value, the count is at least 2. Phase two keeps both pointers at the same distance, counted in links, from the entry point.

**Complexity.**
- **Time** is O(n), because the two phases and the counting pass each read a number of slots that is linear in `n`.
- **Space** is O(1), because the method keeps two slot numbers and one counter.

```java run
import java.util.Arrays;
import java.util.Random;

public final class DuplicateCount287 {
    /**
     * Returns {d, c}: the repeated value and the number of slots that hold it.
     * Time: O(n).
     * Space: O(1).
     * Invariant of phase two: both pointers are equally far from the entry point.
     */
    static int[] duplicateAndCount(int[] nums) {
        int slow = 0, fast = 0;
        // Phase one: the gap grows by one link per round until it is a multiple of the loop length.
        do {
            slow = nums[slow];
            fast = nums[nums[fast]];
        } while (slow != fast);
        // Phase two: equal speeds from slot 0 and from the meeting point meet at the entry point.
        slow = 0;
        while (slow != fast) {
            slow = nums[slow];
            fast = nums[fast];
        }
        // One read-only pass counts the slots that hold the repeated value.
        int count = 0;
        for (int v : nums) if (v == slow) count++;
        return new int[] {slow, count};
    }

    public static void main(String[] args) {
        // The statement examples.
        if (!Arrays.equals(duplicateAndCount(new int[] {3, 1, 3, 4, 2}), new int[] {3, 2})) throw new AssertionError("example 1");
        if (!Arrays.equals(duplicateAndCount(new int[] {2, 2, 2, 2, 2}), new int[] {2, 5})) throw new AssertionError("example 2");
        // Random legal tables with exactly one repeated value, built from a permutation.
        Random rnd = new Random(102);
        for (int t = 0; t < 5000; t++) {
            int n = 1 + rnd.nextInt(9);
            int d = 1 + rnd.nextInt(n);
            int c = 2 + rnd.nextInt(n);
            // The other n + 1 - c slots hold distinct values from the n - 1 values other than d.
            int[] others = new int[n - 1];
            int p = 0;
            for (int v = 1; v <= n; v++) if (v != d) others[p++] = v;
            for (int i = others.length - 1; i > 0; i--) { int j = rnd.nextInt(i + 1); int tmp = others[i]; others[i] = others[j]; others[j] = tmp; }
            int rest = n + 1 - c;
            if (rest > others.length) continue;
            int[] a = new int[n + 1];
            for (int i = 0; i < c; i++) a[i] = d;
            for (int i = 0; i < rest; i++) a[c + i] = others[i];
            for (int i = a.length - 1; i > 0; i--) { int j = rnd.nextInt(i + 1); int tmp = a[i]; a[i] = a[j]; a[j] = tmp; }
            int[] copy = a.clone();
            int[] got = duplicateAndCount(a);
            if (got[0] != d || got[1] != c) throw new AssertionError("random " + Arrays.toString(copy));
            if (!Arrays.equals(a, copy)) throw new AssertionError("table was written");
        }
    }
}
```

#### Solution: [Boundary] Duplicate Near Start (Author exercise)
<!-- id: tp-duplicate-near-start -->

**Approach.**
The two phases find the repeated value `d` with no writes. A short forward scan then looks for the first two slots that hold `d` and returns them in increasing order. A duplicate near the start leaves a walk with a very short tail. For `[1, 1]` the tail is slot 0 alone and the loop is slot 1 with a link to itself, and the entry point is 1. The invariant of the scan is that it has found fewer than two slots holding `d` before it reaches the returned index.

**Complexity.**
- **Time** is O(n), because the two phases and the scan are each linear.
- **Space** is O(1), because the method keeps two slot numbers, a counter and one result slot.

```java run
import java.util.Arrays;
import java.util.Random;

public final class DuplicateNearStart {
    /**
     * Returns {i, j} with i < j: the two smallest slots that hold the repeated value.
     * Time: O(n).
     * Space: O(1).
     * Invariant: before the returned index, fewer than two slots hold the repeated value.
     */
    static int[] firstTwoPositions(int[] nums) {
        int slow = 0, fast = 0;
        do {
            slow = nums[slow];
            fast = nums[nums[fast]];
        } while (slow != fast);
        slow = 0;
        while (slow != fast) {
            slow = nums[slow];
            fast = nums[fast];
        }
        // The entry point is the repeated value; scan for its first two slots.
        int[] out = {-1, -1};
        int found = 0;
        for (int i = 0; i < nums.length && found < 2; i++) {
            if (nums[i] == slow) out[found++] = i;
        }
        return out;
    }

    public static void main(String[] args) {
        // The statement examples.
        if (!Arrays.equals(firstTwoPositions(new int[] {1, 1}), new int[] {0, 1})) throw new AssertionError("example 1");
        if (!Arrays.equals(firstTwoPositions(new int[] {1, 3, 4, 2, 2}), new int[] {3, 4})) throw new AssertionError("example 2");
        // A table where one value fills every slot.
        if (!Arrays.equals(firstTwoPositions(new int[] {2, 2, 2}), new int[] {0, 1})) throw new AssertionError("all equal");
        // Random legal tables against a position map built with a set.
        Random rnd = new Random(103);
        for (int t = 0; t < 5000; t++) {
            int n = 1 + rnd.nextInt(8);
            int d = 1 + rnd.nextInt(n);
            int c = 2 + rnd.nextInt(n);
            int[] others = new int[n - 1];
            int p = 0;
            for (int v = 1; v <= n; v++) if (v != d) others[p++] = v;
            for (int i = others.length - 1; i > 0; i--) { int j = rnd.nextInt(i + 1); int tmp = others[i]; others[i] = others[j]; others[j] = tmp; }
            int rest = n + 1 - c;
            if (rest > others.length) continue;
            int[] a = new int[n + 1];
            for (int i = 0; i < c; i++) a[i] = d;
            for (int i = 0; i < rest; i++) a[c + i] = others[i];
            for (int i = a.length - 1; i > 0; i--) { int j = rnd.nextInt(i + 1); int tmp = a[i]; a[i] = a[j]; a[j] = tmp; }
            int first = -1, second = -1;
            for (int i = 0; i < a.length; i++) if (a[i] == d) { if (first < 0) first = i; else if (second < 0) second = i; }
            if (!Arrays.equals(firstTwoPositions(a), new int[] {first, second})) throw new AssertionError("random " + Arrays.toString(a));
        }
    }
}
```

#### Solution: [Recognize] Compare Alternatives (Author exercise)
<!-- id: tp-read-only-view -->

**Approach.**
The input is an `IntUnaryOperator`, which offers a read and no write, so sign marking and cyclic placement cannot be written against it. A set would need O(n) space and a sorted copy would need to read every slot into an array. The two-speed walk needs only reads and two slot numbers. The method runs phase one with slow and fast pointers, restarts the slow pointer at slot 0, and moves both pointers one link per round until they meet. The meeting slot is the repeated value. The test harness counts the reads and checks that their number stays linear in `n`. During phase two, the number of links from each pointer to the entry point stays equal.

**Complexity.**
- **Time** is O(n) reads, because phase one takes at most `t + c` rounds with three reads each and phase two takes `t` rounds with two reads each.
- **Space** is O(1), because the method keeps two slot numbers.

```java run
import java.util.Random;
import java.util.function.IntUnaryOperator;

public final class ReadOnlyView {
    /**
     * Returns the repeated value of a table that can only be read through a view.
     * Time: O(n) reads.
     * Space: O(1).
     * Invariant of phase two: both pointers are equally far from the entry point.
     */
    static int repeatedValue(IntUnaryOperator view) {
        int slow = 0, fast = 0;
        // Phase one: every read goes through the view, so no write is possible.
        do {
            slow = view.applyAsInt(slow);
            fast = view.applyAsInt(view.applyAsInt(fast));
        } while (slow != fast);
        // Phase two: equal speeds meet at the entry point.
        slow = 0;
        while (slow != fast) {
            slow = view.applyAsInt(slow);
            fast = view.applyAsInt(fast);
        }
        return slow;
    }

    public static void main(String[] args) {
        // The statement examples.
        int[] a = {3, 1, 3, 4, 2};
        if (repeatedValue(i -> a[i]) != 3) throw new AssertionError("example 1");
        int[] b = {1, 1};
        if (repeatedValue(i -> b[i]) != 1) throw new AssertionError("example 2");
        // Random legal tables: the answer repeats, and the number of reads stays linear in n.
        Random rnd = new Random(104);
        for (int t = 0; t < 5000; t++) {
            int n = 1 + rnd.nextInt(9);
            int[] x = rnd.ints(n + 1, 1, n + 1).toArray();
            int[] reads = {0};
            int d = repeatedValue(i -> { reads[0]++; return x[i]; });
            int count = 0;
            for (int v : x) if (v == d) count++;
            if (count < 2) throw new AssertionError("not a repeat");
            if (reads[0] > 6 * (n + 1)) throw new AssertionError("too many reads: " + reads[0]);
        }
    }
}
```
