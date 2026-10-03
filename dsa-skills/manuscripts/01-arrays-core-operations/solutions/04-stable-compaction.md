<!-- solutions-for: 04-stable-compaction -->
### Stable Compaction

#### Solution: [Build] Remove Element (LeetCode 27)
<!-- id: ar-remove-element -->

**Approach.** Read every element once and copy each one that is not `val` to the next free slot, counted by `kept`. Because `kept` never exceeds the read index, each write lands on a slot that has already been read. The return value is `kept`, and the prefix of that length holds the survivors in order. The suffix is left alone, and the assertions confirm both the prefix and the fact that the suffix still holds stale values. A randomized check compares against a list-based filter.

**Complexity.** O(n) time and O(1) extra space.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

public final class RemoveElement {
    static int removeElement(int[] nums, int val) {
        int kept = 0;
        for (int read = 0; read < nums.length; read++) if (nums[read] != val) nums[kept++] = nums[read];
        return kept;
    }

    public static void main(String[] args) {
        int[] a = {5, 1, 5, 5, 2};
        int k = removeElement(a, 5);
        if (k != 2 || !Arrays.equals(Arrays.copyOf(a, k), new int[] {1, 2})) throw new AssertionError("example 1");
        if (!Arrays.equals(a, new int[] {1, 2, 5, 5, 2})) throw new AssertionError("the suffix keeps stale values");
        int[] b = {4};
        if (removeElement(b, 4) != 0) throw new AssertionError("example 2");
        Random rnd = new Random(1);
        for (int t = 0; t < 3000; t++) {
            int[] x = new int[rnd.nextInt(10)];
            for (int i = 0; i < x.length; i++) x[i] = rnd.nextInt(4);
            int val = rnd.nextInt(4);
            List<Integer> expected = new ArrayList<>();
            for (int v : x) if (v != val) expected.add(v);
            int kk = removeElement(x, val);
            if (kk != expected.size()) throw new AssertionError("count");
            for (int i = 0; i < kk; i++) if (x[i] != expected.get(i)) throw new AssertionError("order");
        }
    }
}
```

#### Solution: [Vary] Move Zeroes (LeetCode 283)
<!-- id: ar-move-zeroes -->

**Approach.** Compact the non-zero values to the front with the same two indices, then fill the remaining slots with zeroes, since this contract specifies the whole array. A single-pass variant swaps each non-zero element with the slot at the write index, which also keeps the order and does fewer writes when zeroes are rare, and the assertions check that it agrees. The extra fill loop is needed here only because the contract fixes the suffix.

**Complexity.** O(n) time and O(1) extra space.

```java run
import java.util.Arrays;
import java.util.Random;

public final class MoveZeroes {
    static void moveZeroes(int[] nums) {
        int kept = 0;
        for (int read = 0; read < nums.length; read++) if (nums[read] != 0) nums[kept++] = nums[read];
        for (int i = kept; i < nums.length; i++) nums[i] = 0;
    }
    static void moveZeroesSwap(int[] nums) {
        int write = 0;
        for (int read = 0; read < nums.length; read++) {
            if (nums[read] != 0) { int t = nums[write]; nums[write] = nums[read]; nums[read] = t; write++; }
        }
    }

    public static void main(String[] args) {
        int[] a = {0, 0, 4, 0, 9, 2};
        moveZeroes(a);
        if (!Arrays.equals(a, new int[] {4, 9, 2, 0, 0, 0})) throw new AssertionError("example 1");
        int[] b = {0};
        moveZeroes(b);
        if (!Arrays.equals(b, new int[] {0})) throw new AssertionError("example 2");
        Random rnd = new Random(8);
        for (int t = 0; t < 3000; t++) {
            int[] x = new int[1 + rnd.nextInt(10)];
            for (int i = 0; i < x.length; i++) x[i] = rnd.nextInt(3);
            int[] y = x.clone();
            moveZeroes(x); moveZeroesSwap(y);
            if (!Arrays.equals(x, y)) throw new AssertionError("variants disagree");
        }
    }
}
```

#### Solution: [Boundary] Keep Evens (Author exercise)
<!-- id: ar-keep-evens -->

**Approach.** Use the same loop with the acceptance test `v % 2 == 0`. In Java the remainder takes the sign of the dividend, so `-3 % 2` is `-1`, and a test written as `v % 2 == 1` would treat negative odd numbers as even-like non-matches by accident. Testing evenness with `== 0` is correct for every sign, and testing oddness with `!= 0` is the matching safe form. The assertions show the pitfall directly and then check the filter against a list-based oracle.

**Complexity.** O(n) time and O(1) extra space.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

public final class KeepEvens {
    static int keepEvens(int[] nums) {
        int kept = 0;
        for (int read = 0; read < nums.length; read++) if (nums[read] % 2 == 0) nums[kept++] = nums[read];
        return kept;
    }

    public static void main(String[] args) {
        int[] a = {-2, 3, 4};
        int k = keepEvens(a);
        if (k != 2 || !Arrays.equals(Arrays.copyOf(a, k), new int[] {-2, 4})) throw new AssertionError("example 1");
        if (keepEvens(new int[] {1, 3}) != 0) throw new AssertionError("example 2");
        if (-3 % 2 != -1) throw new AssertionError("a negative odd remainder is -1, not 1");
        boolean wrongOddTest = (-3 % 2 == 1);
        if (wrongOddTest) throw new AssertionError("the == 1 odd test misses negative odd numbers");
        if (!((-3 % 2) != 0)) throw new AssertionError("the != 0 test treats it as odd");
        Random rnd = new Random(6);
        for (int t = 0; t < 3000; t++) {
            int[] x = new int[rnd.nextInt(10)];
            for (int i = 0; i < x.length; i++) x[i] = rnd.nextInt(21) - 10;
            List<Integer> expected = new ArrayList<>();
            for (int v : x) if (v % 2 == 0) expected.add(v);
            int kk = keepEvens(x);
            if (kk != expected.size()) throw new AssertionError("count");
            for (int i = 0; i < kk; i++) if (x[i] != expected.get(i)) throw new AssertionError("order");
        }
    }
}
```

#### Solution: [Recognize] Filter Positives (Author exercise)
<!-- id: ar-filter-positives -->

**Approach.** The loop is identical to the earlier ones and only the test changes to `nums[read] > 0`, which excludes zero. The bookkeeping, the write index counting the accepted values, stays the same. That is the point of the exercise: the pattern is the pair of indices and the invariant that `nums[0..write-1]` holds the accepted values read so far, and the filter is a plug-in condition. The assertions reuse one generic method with different predicates to show this.

**Complexity.** O(n) time and O(1) extra space.

```java run
import java.util.Arrays;
import java.util.function.IntPredicate;

public final class FilterPositives {
    static int compact(int[] nums, IntPredicate keep) {
        int write = 0;
        for (int read = 0; read < nums.length; read++) if (keep.test(nums[read])) nums[write++] = nums[read];
        return write;
    }

    public static void main(String[] args) {
        int[] a = {3, -1, 0, 5, -7, 2};
        int k = compact(a, v -> v > 0);
        if (k != 3 || !Arrays.equals(Arrays.copyOf(a, k), new int[] {3, 5, 2})) throw new AssertionError("example 1");
        if (compact(new int[] {-1, 0}, v -> v > 0) != 0) throw new AssertionError("example 2");
        int[] b = {5, 1, 5, 5, 2};
        if (compact(b, v -> v != 5) != 2) throw new AssertionError("the same method also removes a value");
        int[] c = {-2, 3, 4};
        if (compact(c, v -> v % 2 == 0) != 2) throw new AssertionError("and filters evens");
    }
}
```
