<!-- solutions-for: 01-arrays-core-operations -->
### Solutions For In-Place Sign Marking

#### Solution: [Build] Find Disappeared Numbers (LeetCode 448)
<!-- id: ar-disappeared-numbers -->

**Approach.** The method treats the sign of cell `v - 1` as the record that the value `v` appeared. A loop reads each element through `Math.abs`, computes `slot = value - 1`, and makes `nums[slot]` negative when it is still positive. The test before the negation prevents a repeated value from removing its own mark.

After the loop, every value that appeared has marked its cell. A cell that stayed positive at index `i` therefore means that the value `i + 1` never appeared, and a second loop collects those values in ascending order. The harness compares the method with a set-based oracle on random arrays.

**Complexity.**

- **Time** is O(n), because one loop marks `n` cells and a second loop reads `n` cells.
- **Space** is O(1) besides the result list, because the input array holds all marks.

```java run
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Random;
import java.util.Set;

public final class DisappearedNumbers {
    /**
     * Returns, in ascending order, the numbers in 1..n that do not appear in nums.
     * Time: O(n), because two loops each read n cells.
     * Space: O(1) besides the result, because the signs of nums hold the marks.
     * Invariant: cell v - 1 is negative exactly when value v appears in the prefix read so far.
     */
    static List<Integer> disappeared(int[] nums) {
        // Marking loop: one constant-cost step per element.
        for (int i = 0; i < nums.length; i++) {
            // The entry may already be negative, so the absolute value gives the original number.
            int slot = Math.abs(nums[i]) - 1;
            // Negate only a positive entry; negating again would erase the mark.
            if (nums[slot] > 0) nums[slot] = -nums[slot];
        }
        // Collection loop: positive cells name the numbers that never appeared.
        List<Integer> missing = new ArrayList<>();
        for (int i = 0; i < nums.length; i++) {
            // A cell that is still positive was never marked, so the number i + 1 is absent.
            if (nums[i] > 0) missing.add(i + 1);
        }
        return missing;
    }

    /**
     * Oracle: a hash set of the values, which uses O(n) space.
     * Time: O(n). Space: O(n).
     */
    static List<Integer> oracle(int[] nums) {
        // Store every value, then list the numbers 1..n that are absent from the set.
        Set<Integer> seen = new HashSet<>();
        for (int v : nums) seen.add(v);
        List<Integer> out = new ArrayList<>();
        for (int v = 1; v <= nums.length; v++) if (!seen.contains(v)) out.add(v);
        return out;
    }

    public static void main(String[] args) {
        // Checks Example 1 and Example 2.
        if (!disappeared(new int[] {5, 1, 5, 2, 2}).equals(List.of(3, 4))) throw new AssertionError("example 1");
        if (!disappeared(new int[] {1}).isEmpty()) throw new AssertionError("example 2");
        // Checks 5000 random arrays with values in 1..n against the oracle.
        Random rnd = new Random(19);
        for (int t = 0; t < 5000; t++) {
            int n = 1 + rnd.nextInt(10);
            int[] x = new int[n];
            for (int i = 0; i < n; i++) x[i] = 1 + rnd.nextInt(n);
            List<Integer> want = oracle(x);
            if (!disappeared(x).equals(want)) throw new AssertionError("mismatch on random input");
        }
    }
}
```

#### Solution: [Vary] Find All Duplicates (LeetCode 442)
<!-- id: ar-find-duplicates -->

**Approach.** The scan uses the same marks, and it reads the mark at the moment it writes. For each element, the method computes `value = Math.abs(nums[i])` and `slot = value - 1`. When `nums[slot]` is negative, an earlier occurrence already marked the cell, so the value is a second visit and joins the result. Otherwise the method makes the cell negative.

Each value appears at most twice, so each repeated value is reported exactly once, at the position of its second occurrence. That order matches the order in the exercise. The harness checks the method against a counting oracle that lists the values in the same order.

**Complexity.**

- **Time** is O(n), because the single loop does constant work for each of the `n` elements.
- **Space** is O(1) besides the result list, because the signs of the input hold the marks.

```java run
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Random;

public final class FindAllDuplicates {
    /**
     * Returns the values that appear twice, in the order of their second occurrences.
     * Time: O(n), because one loop does constant work per element.
     * Space: O(1) besides the result, because the signs of nums hold the marks.
     * Invariant: cell v - 1 is negative exactly when value v appears in the prefix read so far.
     */
    static List<Integer> duplicates(int[] nums) {
        List<Integer> result = new ArrayList<>();
        // One pass; each element is read through its absolute value because earlier steps may have marked it.
        for (int i = 0; i < nums.length; i++) {
            int value = Math.abs(nums[i]);
            // The slot is the cell that records whether this value has been seen.
            int slot = value - 1;
            // A negative slot means an earlier occurrence marked it, so this is a second visit.
            if (nums[slot] < 0) result.add(value);
            // A positive slot means the value is new, so mark it.
            else nums[slot] = -nums[slot];
        }
        return result;
    }

    /**
     * Oracle: counts occurrences while scanning and reports the value at its second occurrence.
     * Time: O(n). Space: O(n).
     */
    static List<Integer> oracle(int[] nums) {
        // Count each value as it is read, and report it when the running count reaches two.
        Map<Integer, Integer> counts = new HashMap<>();
        List<Integer> out = new ArrayList<>();
        for (int v : nums) if (counts.merge(v, 1, Integer::sum) == 2) out.add(v);
        return out;
    }

    public static void main(String[] args) {
        // Checks Example 1 and Example 2.
        if (!duplicates(new int[] {3, 1, 3, 2, 1}).equals(List.of(3, 1))) throw new AssertionError("example 1");
        if (!duplicates(new int[] {1, 2, 3}).isEmpty()) throw new AssertionError("example 2");
        // Checks 5000 random arrays in which each value appears at most twice.
        Random rnd = new Random(29);
        for (int t = 0; t < 5000; t++) {
            int n = 1 + rnd.nextInt(10);
            // Build a pool with each value in 1..n at most twice, then draw n entries without replacement.
            List<Integer> pool = new ArrayList<>();
            for (int v = 1; v <= n; v++) { pool.add(v); pool.add(v); }
            java.util.Collections.shuffle(pool, rnd);
            int[] x = new int[n];
            for (int i = 0; i < n; i++) x[i] = pool.get(i);
            List<Integer> want = oracle(x);
            if (!duplicates(x).equals(want)) throw new AssertionError("mismatch on random input");
        }
    }
}
```

#### Solution: [Boundary] Re-read A Marked Value (Author exercise)
<!-- id: ar-reread-marked-value -->

**Approach.** A cell that an earlier step marked holds the negative of its original number. Using that negative number as an index fails, so every read of an element goes through `Math.abs`. The method counts a new distinct value each time it flips a positive target cell to negative, and it does not count a value whose target is already negative.

After the counting loop, many cells are negative. A final loop replaces each entry with its absolute value, which restores every original number, because marking changed only signs. The harness asserts that the array is equal to its snapshot afterward. It also asserts that a negative index throws `ArrayIndexOutOfBoundsException`, which is why the absolute value is required.

**Complexity.**

- **Time** is O(n), because the counting loop and the restoring loop each visit `n` cells once.
- **Space** is O(1), because the input array holds the marks and the method stores two integers.

```java run
import java.util.Arrays;
import java.util.HashSet;
import java.util.Random;
import java.util.Set;

public final class RereadMarkedValue {
    /**
     * Counts the distinct values in nums, then restores nums to its original contents.
     * Time: O(n), because two loops each visit n cells.
     * Space: O(1), because the signs of nums hold the marks.
     * Invariant: cell v - 1 is negative exactly when value v appears in the prefix read so far.
     */
    static int countDistinct(int[] nums) {
        int distinct = 0;
        // Marking loop: one constant-cost step per element.
        for (int i = 0; i < nums.length; i++) {
            // The entry may be a marked cell holding a negative number, so take the magnitude first.
            int slot = Math.abs(nums[i]) - 1;
            // A positive target means a new value, so count it and mark the target.
            if (nums[slot] > 0) {
                nums[slot] = -nums[slot];
                distinct++;
            }
        }
        // Restoring loop: marking changed only signs, so absolute values rebuild the original array.
        for (int i = 0; i < nums.length; i++) nums[i] = Math.abs(nums[i]);
        return distinct;
    }

    public static void main(String[] args) {
        // Checks Example 1 and Example 2, including that the array is unchanged afterward.
        int[] a = {2, 2, 2};
        if (countDistinct(a) != 1) throw new AssertionError("example 1");
        if (!Arrays.equals(a, new int[] {2, 2, 2})) throw new AssertionError("example 1 restored");
        int[] b = {1, 2, 3};
        if (countDistinct(b) != 3) throw new AssertionError("example 2");
        if (!Arrays.equals(b, new int[] {1, 2, 3})) throw new AssertionError("example 2 restored");
        // Checks the Java claim: a negative value used as an index throws an exception.
        int[] marked = {-2, 1};
        boolean thrown = false;
        try {
            int ignored = marked[marked[0] - 1];
        } catch (ArrayIndexOutOfBoundsException e) {
            thrown = true;
        }
        if (!thrown) throw new AssertionError("a negative index must throw");
        // Checks 5000 random arrays against a hash-set count, and that every array is restored.
        Random rnd = new Random(37);
        for (int t = 0; t < 5000; t++) {
            int n = 1 + rnd.nextInt(10);
            int[] x = new int[n];
            Set<Integer> set = new HashSet<>();
            for (int i = 0; i < n; i++) { x[i] = 1 + rnd.nextInt(n); set.add(x[i]); }
            int[] snapshot = x.clone();
            if (countDistinct(x) != set.size()) throw new AssertionError("count mismatch");
            if (!Arrays.equals(x, snapshot)) throw new AssertionError("array not restored");
        }
    }
}
```

#### Solution: [Recognize] Set Mismatch (LeetCode 645)
<!-- id: ar-set-mismatch -->

**Approach.** The cue is a range of 1 to `n` with a mutable input and a question about which values appeared. The method marks cell `value - 1` for each element, using `Math.abs` at every read. When the target cell is already negative, the value is the repeated number, and the method records it. The repeated value occurs exactly twice, so the record is written once.

After the pass, exactly one cell stays positive. One value is absent, and all other values marked their cells. The index `i` of the positive cell gives the absent value `i + 1`. The method returns the repeated value and the absent value in that order. The harness builds inputs from a permutation, applies the error, and compares the method with the known answer and with a counting oracle.

**Complexity.**

- **Time** is O(n), because the marking loop and the search for the positive cell each visit at most `n` cells.
- **Space** is O(1), because the signs of the input hold the marks and the method stores two integers.

```java run
import java.util.Arrays;
import java.util.Random;

public final class SetMismatch {
    /**
     * Returns {repeated number, absent number} for an array that started as 1..n and has one error.
     * Time: O(n), because two loops each visit at most n cells.
     * Space: O(1), because the signs of nums hold the marks.
     * Invariant: cell v - 1 is negative exactly when value v appears in the prefix read so far.
     */
    static int[] findErrorNums(int[] nums) {
        int repeated = -1;
        // Marking loop: one constant-cost step per element.
        for (int i = 0; i < nums.length; i++) {
            // Read the entry through its absolute value, since earlier steps may have marked it.
            int value = Math.abs(nums[i]);
            int slot = value - 1;
            // A negative target is a second visit, so this value is the repeated one.
            if (nums[slot] < 0) repeated = value;
            // A positive target means a new value, so mark it.
            else nums[slot] = -nums[slot];
        }
        // Search loop: the only positive cell names the absent value.
        int absent = -1;
        for (int i = 0; i < nums.length; i++) if (nums[i] > 0) absent = i + 1;
        return new int[] {repeated, absent};
    }

    /**
     * Oracle: counts every value with a count array, which uses O(n) space.
     * Time: O(n). Space: O(n).
     */
    static int[] oracle(int[] nums) {
        // Count each value, then find the value counted twice and the value counted zero times.
        int[] count = new int[nums.length + 1];
        for (int v : nums) count[v]++;
        int repeated = -1, absent = -1;
        for (int v = 1; v <= nums.length; v++) {
            if (count[v] == 2) repeated = v;
            if (count[v] == 0) absent = v;
        }
        return new int[] {repeated, absent};
    }

    public static void main(String[] args) {
        // Checks Example 1 and Example 2.
        if (!Arrays.equals(findErrorNums(new int[] {2, 3, 3, 4, 5}), new int[] {3, 1})) throw new AssertionError("example 1");
        if (!Arrays.equals(findErrorNums(new int[] {2, 2}), new int[] {2, 1})) throw new AssertionError("example 2");
        // Checks 5000 random arrays: start from 1..n, copy one value over another, and shuffle.
        Random rnd = new Random(43);
        for (int t = 0; t < 5000; t++) {
            int n = 2 + rnd.nextInt(10);
            int[] x = new int[n];
            for (int i = 0; i < n; i++) x[i] = i + 1;
            // Overwrite one position with the value of another position, creating the single error.
            int a = rnd.nextInt(n), b = rnd.nextInt(n);
            while (b == a) b = rnd.nextInt(n);
            int absent = x[a];
            int repeated = x[b];
            x[a] = repeated;
            // Shuffle so the repeated copies land in random positions.
            for (int i = n - 1; i > 0; i--) { int j = rnd.nextInt(i + 1); int tmp = x[i]; x[i] = x[j]; x[j] = tmp; }
            int[] want = oracle(x);
            if (want[0] != repeated || want[1] != absent) throw new AssertionError("oracle disagrees with construction");
            if (!Arrays.equals(findErrorNums(x), want)) throw new AssertionError("mismatch on random input");
        }
    }
}
```
