<!-- solutions-for: 09-in-place-sign-marking -->
### In-Place Sign Marking

#### Solution: [Build] Find All Numbers Disappeared in an Array (LeetCode 448)
<!-- id: ar-disappeared-numbers -->

**Approach.** For each element, take its magnitude, find slot `magnitude - 1`, and make that slot negative if it is not already. A second scan collects `index + 1` for every slot that is still positive. The marking step never flips a negative slot back, so repeated values are harmless. The assertions compare the result with a boolean-table oracle on random arrays, including arrays with heavy repetition.

**Complexity.** O(n) time and O(1) extra space apart from the output.

```java run
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public final class DisappearedNumbers {
    static List<Integer> disappeared(int[] nums) {
        for (int i = 0; i < nums.length; i++) {
            int slot = Math.abs(nums[i]) - 1;
            if (nums[slot] > 0) nums[slot] = -nums[slot];
        }
        List<Integer> missing = new ArrayList<>();
        for (int i = 0; i < nums.length; i++) if (nums[i] > 0) missing.add(i + 1);
        return missing;
    }
    static List<Integer> oracle(int[] nums) {
        boolean[] seen = new boolean[nums.length + 1];
        for (int v : nums) seen[v] = true;
        List<Integer> out = new ArrayList<>();
        for (int v = 1; v <= nums.length; v++) if (!seen[v]) out.add(v);
        return out;
    }

    public static void main(String[] args) {
        if (!disappeared(new int[] {2, 2, 5, 5, 1}).equals(List.of(3, 4))) throw new AssertionError("example 1");
        if (!disappeared(new int[] {1, 2, 3}).isEmpty()) throw new AssertionError("example 2");
        if (!disappeared(new int[] {1, 1}).equals(List.of(2))) throw new AssertionError("single repeat");
        Random rnd = new Random(51);
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(12);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = 1 + rnd.nextInt(n);
            List<Integer> expected = oracle(a);
            if (!disappeared(a.clone()).equals(expected)) throw new AssertionError("disagrees with the table oracle");
        }
    }
}
```

#### Solution: [Vary] Find All Duplicates in an Array (LeetCode 442)
<!-- id: ar-find-duplicates -->

**Approach.** Read the magnitude at each position and look at the slot it names. If that slot is already negative, the value was seen before, so it is a duplicate and is recorded. Otherwise the slot is marked. Each value is reported at the moment its second copy arrives, which is why the promise of at most two copies matters. The oracle counts occurrences with a table, and the result is compared as a list in order of second arrival.

**Complexity.** O(n) time and O(1) extra space apart from the output.

```java run
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public final class FindDuplicates {
    static List<Integer> duplicates(int[] nums) {
        List<Integer> dup = new ArrayList<>();
        for (int i = 0; i < nums.length; i++) {
            int slot = Math.abs(nums[i]) - 1;
            if (nums[slot] < 0) dup.add(slot + 1);
            else nums[slot] = -nums[slot];
        }
        return dup;
    }
    static List<Integer> oracle(int[] nums) {
        int[] count = new int[nums.length + 1];
        List<Integer> out = new ArrayList<>();
        for (int v : nums) if (++count[v] == 2) out.add(v);
        return out;
    }

    public static void main(String[] args) {
        if (!duplicates(new int[] {3, 1, 3, 2, 5, 5}).equals(List.of(3, 5))) throw new AssertionError("example 1");
        if (!duplicates(new int[] {1, 2, 3}).isEmpty()) throw new AssertionError("example 2");
        Random rnd = new Random(52);
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(12);
            int[] a = new int[n];
            int[] used = new int[n + 1];
            for (int i = 0; i < n; i++) {
                int v;
                do { v = 1 + rnd.nextInt(n); } while (used[v] == 2);
                used[v]++;
                a[i] = v;
            }
            if (!duplicates(a.clone()).equals(oracle(a))) throw new AssertionError("disagrees with the count oracle");
        }
    }
}
```

#### Solution: [Boundary] Re-read a Marked Value (Author exercise)
<!-- id: ar-reread-marked-value -->

**Approach.** A marked slot holds a negative number, and a negative number minus one is not a valid index, so reading a marked value directly fails. Taking `Math.abs` first recovers the original value, because marking only changed the sign. The marking step assigns `-Math.abs(slot)` so that a second visit cannot flip the slot back to positive. After the pass, taking the absolute value of every slot restores the original array. The assertions show the failing direct read, the successful repaired read, the exact marked array for `[2, 1]`, and the restoration.

**Complexity.** O(n) time and O(1) extra space.

```java run
import java.util.Arrays;

public final class RereadMarkedValue {
    static void markAll(int[] nums) {
        for (int i = 0; i < nums.length; i++) {
            int slot = Math.abs(nums[i]) - 1;
            nums[slot] = -Math.abs(nums[slot]);
        }
    }
    static void restore(int[] nums) {
        for (int i = 0; i < nums.length; i++) nums[i] = Math.abs(nums[i]);
    }

    public static void main(String[] args) {
        int[] a = {3, 1, 3};
        int[] b = a.clone();
        b[2] = -3;                                          // the state when the cursor reaches index 2
        boolean failed = false;
        try { int unused = b[b[2] - 1]; } catch (ArrayIndexOutOfBoundsException e) { failed = true; }
        if (!failed) throw new AssertionError("a negative value used as an index must fail");
        if (b[Math.abs(b[2]) - 1] != -3) throw new AssertionError("the magnitude must point back at the marked slot");
        int[] c = {2, 1};
        markAll(c);
        if (!Arrays.equals(c, new int[] {-2, -1})) throw new AssertionError("example 2 marked");
        restore(c);
        if (!Arrays.equals(c, new int[] {2, 1})) throw new AssertionError("example 2 restored");
        int[] d = {3, 1, 3};
        markAll(d);
        if (!Arrays.equals(d, new int[] {-3, 1, -3}) && !Arrays.equals(d, new int[] {-3, -1, -3})) throw new AssertionError("marks on [3,1,3]: " + Arrays.toString(d));
        restore(d);
        if (!Arrays.equals(d, new int[] {3, 1, 3})) throw new AssertionError("restore of [3,1,3]");
    }
}
```

#### Solution: [Recognize] Set Mismatch (LeetCode 645)
<!-- id: ar-set-mismatch -->

**Approach.** Run the mark pass. The value whose slot is already negative on arrival is the repeated one. After the pass, the one slot that is still positive names the missing value, which is its index plus one. Both answers come from a single marking pass followed by one scan, and the array is not needed afterwards. The oracle uses the sum and the sum of squares, which is independent of the marking idea.

**Complexity.** O(n) time and O(1) extra space.

```java run
import java.util.Arrays;
import java.util.Random;

public final class SetMismatch {
    static int[] findErrorNums(int[] nums) {
        int repeated = -1, missing = -1;
        for (int i = 0; i < nums.length; i++) {
            int slot = Math.abs(nums[i]) - 1;
            if (nums[slot] < 0) repeated = slot + 1;
            else nums[slot] = -nums[slot];
        }
        for (int i = 0; i < nums.length; i++) if (nums[i] > 0) missing = i + 1;
        return new int[] {repeated, missing};
    }
    static int[] oracle(int[] nums) {
        long n = nums.length, sum = 0, sq = 0;
        for (int v : nums) { sum += v; sq += (long) v * v; }
        long ds = sum - n * (n + 1) / 2;                       // repeated minus missing
        long dq = sq - n * (n + 1) * (2 * n + 1) / 6;          // repeated^2 minus missing^2
        long plus = dq / ds;                                   // repeated plus missing
        return new int[] {(int) ((plus + ds) / 2), (int) ((plus - ds) / 2)};
    }

    public static void main(String[] args) {
        if (!Arrays.equals(findErrorNums(new int[] {3, 1, 3, 4}), new int[] {3, 2})) throw new AssertionError("example 1");
        if (!Arrays.equals(findErrorNums(new int[] {2, 2}), new int[] {2, 1})) throw new AssertionError("example 2");
        Random rnd = new Random(53);
        for (int t = 0; t < 4000; t++) {
            int n = 2 + rnd.nextInt(12);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = i + 1;
            int from = rnd.nextInt(n), to;
            do { to = rnd.nextInt(n); } while (to == from);
            a[to] = a[from];                                    // value a[from] now repeats, old a[to] is missing
            for (int i = n - 1; i > 0; i--) { int j = rnd.nextInt(i + 1); int tmp = a[i]; a[i] = a[j]; a[j] = tmp; }
            if (!Arrays.equals(findErrorNums(a.clone()), oracle(a))) throw new AssertionError("disagrees with the sum oracle");
        }
    }
}
```
