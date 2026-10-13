<!-- solutions-for: 04-xor-cancellation -->
### Solutions For XOR Cancellation

#### Solution: [Build] Single Number (LeetCode 136)
<!-- id: bt04-single-number -->

**Approach.** One fold with `^` erases every pair and leaves the single value.

The operator `^` is commutative and associative, so the fold equals the single value combined with every pair, in any grouping. Each pair gives `v ^ v = 0`, and `x ^ 0 = x` keeps the rest. The invariant is that `acc` after reading a prefix equals the exclusive or of the values that appear an odd number of times in that prefix. The accumulator starts at 0 because 0 changes nothing. Negative values work without special handling, since `^` acts on all 32 bits.

**Complexity.**

- **Time** is O(n), as the pass visits every element a single time.
- **Space** is O(1), as the fold keeps one integer and never writes to the input.

```java run
import java.util.HashMap;
import java.util.Random;

public final class XorSingle {
    /**
     * Returns the value that appears once when all other values appear twice.
     * Time: O(n), one pass.
     * Space: O(1), one accumulator.
     * Invariant: acc equals the exclusive or of values with an odd count in the prefix read so far.
     */
    static int singleNumber(int[] nums) {
        // Zero is the identity for ^, so the first element passes through unchanged.
        int acc = 0;
        // One pass reads each element exactly once.
        for (int v : nums) {
            // A value read twice cancels itself out of the accumulator.
            acc ^= v;
        }
        // Only the unpaired value remains.
        return acc;
    }

    /** Oracle: counts every value in a map and returns the value with count 1. */
    static int oracle(int[] nums) {
        HashMap<Integer, Integer> count = new HashMap<>();
        for (int v : nums) count.merge(v, 1, Integer::sum);
        for (var e : count.entrySet()) if (e.getValue() == 1) return e.getKey();
        throw new AssertionError("no single value");
    }

    public static void main(String[] args) {
        // Checks Example 1 and Example 2.
        if (singleNumber(new int[]{9, -3, 7, 9, 7}) != -3) throw new AssertionError("example 1");
        if (singleNumber(new int[]{42}) != 42) throw new AssertionError("example 2");
        // Checks the laws the approach relies on.
        int a = -123456, b = 987654, c = 31;
        if ((a ^ a) != 0 || (a ^ 0) != a) throw new AssertionError("identity laws");
        if (((a ^ b) ^ c) != (a ^ (b ^ c)) || (a ^ b) != (b ^ a)) throw new AssertionError("grouping laws");
        // Checks random shuffled arrays against the map oracle.
        Random rnd = new Random(3101);
        for (int round = 0; round < 2000; round++) {
            int pairs = rnd.nextInt(30);
            int[] nums = new int[2 * pairs + 1];
            java.util.HashSet<Integer> used = new java.util.HashSet<>();
            int idx = 0;
            for (int p = 0; p <= pairs; p++) {
                int v;
                do { v = rnd.nextInt(41) - 20; } while (!used.add(v));
                nums[idx++] = v;
                if (p < pairs) nums[idx++] = v;
            }
            for (int i = nums.length - 1; i > 0; i--) {
                int j = rnd.nextInt(i + 1);
                int t = nums[i]; nums[i] = nums[j]; nums[j] = t;
            }
            if (singleNumber(nums) != oracle(nums)) throw new AssertionError("round " + round);
        }
    }
}
```

#### Solution: [Vary] Missing Value By XOR (Author exercise)
<!-- id: bt04-missing-offset -->

**Approach.** The accumulator combines every number of the range with every element, so only the missing number survives.

The range `lo..lo+n` holds `n + 1` numbers. The elements of `a` and the index values `lo + i` for `i` in `0..n-1` together cover the range, except that the index values stop at `lo + n - 1`. Starting the accumulator at `lo + n` supplies the last range number once. Each number of the range except the missing one then enters once through an index value or the start value, and once through an element, so it cancels. The missing number enters only once. The invariant is that `acc` equals the exclusive or of the range numbers supplied so far and the elements read so far. Using `lo + i` and not `i` keeps the index values equal to the element values they should match.

**Complexity.**

- **Time** is O(n), because the loop body runs once per element of `a`.
- **Space** is O(1), because only the accumulator is stored.

```java run
import java.util.Random;

public final class XorMissingOffset {
    /**
     * Returns the number in lo..lo+n that is absent from a.
     * Time: O(n), one pass.
     * Space: O(1), one accumulator.
     * Invariant: acc is the exclusive or of the supplied range numbers and the elements read so far.
     */
    static int missing(int[] a, int lo) {
        // The top of the range has no index, so the start value supplies it.
        int acc = lo + a.length;
        // Each step supplies one range number and reads one element.
        for (int i = 0; i < a.length; i++) {
            // Equal numbers cancel, so only the absent number survives.
            acc ^= (lo + i) ^ a[i];
        }
        // The accumulator is the missing number.
        return acc;
    }

    /** Oracle: marks present values in a boolean table over the range. */
    static int oracle(int[] a, int lo) {
        boolean[] seen = new boolean[a.length + 1];
        for (int v : a) seen[v - lo] = true;
        for (int i = 0; i < seen.length; i++) if (!seen[i]) return lo + i;
        throw new AssertionError("nothing missing");
    }

    public static void main(String[] args) {
        // Checks Example 1 and Example 2.
        if (missing(new int[]{7, 5, 8, 6}, 5) != 9) throw new AssertionError("example 1");
        if (missing(new int[]{-2, 0, 2, 1}, -2) != -1) throw new AssertionError("example 2");
        // Checks the empty array, where the range holds only lo.
        if (missing(new int[0], -77) != -77) throw new AssertionError("empty array");
        // Checks random ranges with a random start, including negative starts and a missing first value.
        Random rnd = new Random(3102);
        for (int round = 0; round < 3000; round++) {
            int n = rnd.nextInt(40);
            int lo = rnd.nextInt(2001) - 1000;
            int gap = rnd.nextInt(n + 1);
            int[] a = new int[n];
            int k = 0;
            for (int v = lo; v <= lo + n; v++) if (v != lo + gap) a[k++] = v;
            for (int i = n - 1; i > 0; i--) {
                int j = rnd.nextInt(i + 1);
                int t = a[i]; a[i] = a[j]; a[j] = t;
            }
            if (missing(a, lo) != lo + gap || oracle(a, lo) != lo + gap) throw new AssertionError("round " + round);
        }
    }
}
```

#### Solution: [Boundary] Zero And Negative Values (Author exercise)
<!-- id: bt04-odd-count-signed -->

**Approach.** The fold works on the 32-bit pattern, so sign and zero need no special case.

An even count of copies of a value gives `v ^ v ^ ... ^ v = 0`, and an odd count gives one copy of `v`. The fold therefore equals the exclusive or of one copy of every odd-count value, which is the single answer. The operator `^` treats the sign bit like any other bit, so `Integer.MIN_VALUE` cancels with itself. The answer 0 is not confused with "nothing found", because the problem guarantees that an odd-count value exists, and the fold returns 0 when that value is 0. A solution that starts with `-1` or `0` as a "none" marker would fail here. The invariant is that `acc` equals the exclusive or of the odd-count values in the prefix.

**Complexity.**

- **Time** is O(n), since a single scan combines each of the `n` values.
- **Space** is O(1), since the accumulator is the only state.

```java run
import java.util.HashMap;
import java.util.Random;

public final class XorOddCount {
    /**
     * Returns the one value with an odd count, for any int values.
     * Time: O(n), one pass.
     * Space: O(1), one accumulator.
     * Invariant: acc is the exclusive or of the values that have an odd count in the prefix.
     */
    static int oddOne(int[] nums) {
        // The identity element for ^ is 0, and no sentinel is needed.
        int acc = 0;
        // Each element is combined once, whatever its sign.
        for (int v : nums) {
            // Pairs of equal values cancel, and the sign bit follows the same rule.
            acc ^= v;
        }
        // The result may be 0 or negative.
        return acc;
    }

    /** Oracle: counts every value and returns the one with an odd count. */
    static int oracle(int[] nums) {
        HashMap<Integer, Integer> count = new HashMap<>();
        for (int v : nums) count.merge(v, 1, Integer::sum);
        for (var e : count.entrySet()) if ((e.getValue() & 1) == 1) return e.getKey();
        throw new AssertionError("no odd count");
    }

    public static void main(String[] args) {
        // Checks Example 1 and Example 2.
        if (oddOne(new int[]{0, 0, 0}) != 0) throw new AssertionError("example 1");
        if (oddOne(new int[]{-5, 3, -5, 3, -5}) != -5) throw new AssertionError("example 2");
        // Checks the sign bit and the extreme value under ^.
        if ((Integer.MIN_VALUE ^ Integer.MIN_VALUE) != 0) throw new AssertionError("min cancels");
        if (oddOne(new int[]{Integer.MIN_VALUE, 7, Integer.MIN_VALUE, 7, Integer.MIN_VALUE}) != Integer.MIN_VALUE) throw new AssertionError("min survives");
        if ((-1 ^ 0) != -1 || (-1 ^ -1) != 0) throw new AssertionError("minus one");
        // Checks random arrays with odd and even counts against the map oracle.
        Random rnd = new Random(3103);
        int[] pool = {0, -1, 1, Integer.MIN_VALUE, Integer.MAX_VALUE, -7, 12, 255, -256, 65536};
        for (int round = 0; round < 3000; round++) {
            java.util.ArrayList<Integer> list = new java.util.ArrayList<>();
            int odd = rnd.nextInt(pool.length);
            for (int p = 0; p < pool.length; p++) {
                int copies = 2 * rnd.nextInt(4) + (p == odd ? 1 : 0);
                for (int c = 0; c < copies; c++) list.add(pool[p]);
            }
            java.util.Collections.shuffle(list, rnd);
            int[] nums = list.stream().mapToInt(Integer::intValue).toArray();
            if (oddOne(nums) != oracle(nums)) throw new AssertionError("round " + round);
        }
    }
}
```

#### Solution: [Recognize] Single Number III (LeetCode 260)
<!-- id: bt04-two-singles -->

**Approach.** The first fold gives `p ^ q`, and one differing bit then separates the two values.

The fold over the whole array cancels all pairs and leaves `diff = p ^ q`. The values `p` and `q` are distinct, so `diff` has at least one set bit. The expression `diff & -diff` picks the lowest such bit as `split`. At that bit exactly one of `p` and `q` has a 1. The second pass folds only the elements whose bit is set. The two copies of any paired value share the same bit, so a pair lands in one group together and cancels there. Each group then holds exactly one single value, and the fold of the group returns it. The other value is `diff ^ p`. The method returns the smaller value first. For `diff = Integer.MIN_VALUE`, `diff & -diff` is also `Integer.MIN_VALUE`, which is nonzero, so the test `(v & split) != 0` still works.

**Complexity.**

- **Time** is O(n), because the method makes two passes.
- **Space** is O(1), because it keeps a few integers and the result array.

```java run
import java.util.Arrays;
import java.util.HashMap;
import java.util.Random;

public final class XorTwoSingles {
    /**
     * Returns the two values that appear once, smaller first.
     * Time: O(n), two passes.
     * Space: O(1), a few integers and the result.
     * Invariant: the group with the split bit set contains exactly one single value and complete pairs.
     */
    static int[] twoSingles(int[] nums) {
        // The first fold cancels all pairs and leaves p ^ q.
        int diff = 0;
        for (int v : nums) diff ^= v;
        // The lowest set bit of diff is a bit where p and q differ.
        int split = diff & -diff;
        // The second fold covers one group only.
        int p = 0;
        for (int v : nums) {
            // Elements in the group with the split bit set include p and complete pairs.
            if ((v & split) != 0) p ^= v;
        }
        // The other single value is what remains of diff after removing p.
        int q = diff ^ p;
        // The contract asks for ascending order.
        return new int[]{Math.min(p, q), Math.max(p, q)};
    }

    /** Oracle: counts values in a map and collects those with count 1. */
    static int[] oracle(int[] nums) {
        HashMap<Integer, Integer> count = new HashMap<>();
        for (int v : nums) count.merge(v, 1, Integer::sum);
        int[] out = count.entrySet().stream().filter(e -> e.getValue() == 1).mapToInt(java.util.Map.Entry::getKey).sorted().toArray();
        return out;
    }

    public static void main(String[] args) {
        // Checks Example 1 and Example 2.
        if (!Arrays.equals(twoSingles(new int[]{6, 2, 9, 6, 4, 2}), new int[]{4, 9})) throw new AssertionError("example 1");
        if (!Arrays.equals(twoSingles(new int[]{-1, 5, -1, 0}), new int[]{0, 5})) throw new AssertionError("example 2");
        // Checks the case where the two values differ only in the sign bit.
        int[] edge = {Integer.MIN_VALUE, 0, 3, 3};
        if ((Integer.MIN_VALUE & -Integer.MIN_VALUE) == 0) throw new AssertionError("split is nonzero");
        if (!Arrays.equals(twoSingles(edge), new int[]{Integer.MIN_VALUE, 0})) throw new AssertionError("sign bit split");
        // Checks random inputs against the map oracle.
        Random rnd = new Random(3104);
        for (int round = 0; round < 3000; round++) {
            int pairs = rnd.nextInt(20);
            java.util.HashSet<Integer> used = new java.util.HashSet<>();
            java.util.ArrayList<Integer> list = new java.util.ArrayList<>();
            for (int s = 0; s < 2; s++) {
                int v;
                do { v = rnd.nextInt(61) - 30; } while (!used.add(v));
                list.add(v);
            }
            for (int p = 0; p < pairs; p++) {
                int v;
                do { v = rnd.nextInt(61) - 30; } while (!used.add(v));
                list.add(v);
                list.add(v);
            }
            java.util.Collections.shuffle(list, rnd);
            int[] nums = list.stream().mapToInt(Integer::intValue).toArray();
            if (!Arrays.equals(twoSingles(nums), oracle(nums))) throw new AssertionError("round " + round);
        }
    }
}
```
