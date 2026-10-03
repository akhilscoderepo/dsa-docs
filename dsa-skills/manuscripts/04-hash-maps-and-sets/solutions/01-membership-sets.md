<!-- solutions-for: 01-membership-sets -->
### Membership Sets

#### Solution: [Build] Contains Duplicate (LeetCode 217)
<!-- id: hm-contains-duplicate -->

**Approach.** Keep a set of the values already read. For each value, `add` returns false exactly when the value was already stored, which is the repeat that ends the scan. After a prefix has been read, the set equals the distinct values of that prefix. The assertions compare the result with an all-pairs check on random arrays, confirm that `add` reports presence, and show that a `HashSet<int[]>` treats two equal-content arrays as different values.

**Complexity.** Expected O(n) time and O(n) extra space.

```java run
import java.util.HashSet;
import java.util.Random;
import java.util.Set;

public final class ContainsDuplicate {
    static boolean hasDuplicate(int[] nums) {
        Set<Integer> seen = new HashSet<>();
        for (int x : nums) {
            if (!seen.add(x)) return true;
        }
        return false;
    }
    static boolean oracle(int[] nums) {
        for (int i = 0; i < nums.length; i++)
            for (int j = i + 1; j < nums.length; j++)
                if (nums[i] == nums[j]) return true;
        return false;
    }

    public static void main(String[] args) {
        if (!hasDuplicate(new int[] {3, 8, 5, 3})) throw new AssertionError("example 1");
        if (hasDuplicate(new int[] {})) throw new AssertionError("example 2");
        Set<Integer> s = new HashSet<>();
        if (!s.add(5) || s.add(5)) throw new AssertionError("add reports whether the value was new");
        Set<int[]> arrays = new HashSet<>();
        arrays.add(new int[] {1});
        arrays.add(new int[] {1});
        if (arrays.size() != 2) throw new AssertionError("arrays are compared by identity");
        Random rnd = new Random(41);
        for (int t = 0; t < 4000; t++) {
            int[] x = new int[rnd.nextInt(12)];
            for (int i = 0; i < x.length; i++) x[i] = rnd.nextInt(15) - 5;
            if (hasDuplicate(x) != oracle(x)) throw new AssertionError("disagrees with the pair check");
        }
    }
}
```

#### Solution: [Vary] Intersection of Two Arrays (LeetCode 349)
<!-- id: hm-intersection-arrays -->

**Approach.** Load the first array into a hash set, then scan the second and add each value found in that set to a tree set of answers, which both removes repeats and fixes the order. Repeats in either input cannot create repeats in the output, because both containers are sets. The oracle sorts and merges the two arrays with plain loops and builds the distinct common values, and the assertions require the same array on random inputs, including empty ones.

**Complexity.** Expected O(n + m) for the scans, plus O(k log k) for ordering the `k` answers, and O(n + k) extra space.

```java run
import java.util.Arrays;
import java.util.HashSet;
import java.util.Random;
import java.util.Set;
import java.util.TreeSet;

public final class IntersectionArrays {
    static int[] intersection(int[] a, int[] b) {
        Set<Integer> inA = new HashSet<>();
        for (int x : a) inA.add(x);
        Set<Integer> shared = new TreeSet<>();
        for (int y : b) if (inA.contains(y)) shared.add(y);
        int[] out = new int[shared.size()];
        int k = 0;
        for (int v : shared) out[k++] = v;
        return out;
    }
    static int[] oracle(int[] a, int[] b) {
        int[] sa = a.clone(), sb = b.clone();
        Arrays.sort(sa);
        Arrays.sort(sb);
        int[] tmp = new int[Math.min(sa.length, sb.length)];
        int n = 0, i = 0, j = 0;
        while (i < sa.length && j < sb.length) {
            if (sa[i] < sb[j]) i++;
            else if (sa[i] > sb[j]) j++;
            else {
                if (n == 0 || tmp[n - 1] != sa[i]) tmp[n++] = sa[i];
                i++; j++;
            }
        }
        return Arrays.copyOf(tmp, n);
    }

    public static void main(String[] args) {
        if (!Arrays.equals(intersection(new int[] {4, 9, 5, 9}, new int[] {9, 4, 9, 8, 4}), new int[] {4, 9})) throw new AssertionError("example 1");
        if (intersection(new int[] {}, new int[] {1}).length != 0) throw new AssertionError("example 2");
        Random rnd = new Random(42);
        for (int t = 0; t < 4000; t++) {
            int[] a = new int[rnd.nextInt(10)], b = new int[rnd.nextInt(10)];
            for (int i = 0; i < a.length; i++) a[i] = rnd.nextInt(8);
            for (int i = 0; i < b.length; i++) b[i] = rnd.nextInt(8);
            if (!Arrays.equals(intersection(a, b), oracle(a, b))) throw new AssertionError("disagrees with the merge oracle");
        }
    }
}
```

#### Solution: [Boundary] Happy Number (LeetCode 202)
<!-- id: hm-happy-number -->

**Approach.** Store each state before moving on. If the next state is already stored, the process has entered a loop that does not contain 1, so the answer is false. If 1 is reached first, the answer is true. Without the set, input 4 would loop forever. Digit-square sums shrink large numbers quickly, so only a few hundred states can ever occur, which bounds the set. The oracle runs the process for a fixed budget of 1000 steps and checks whether 1 appears, and the assertions compare both on every value from 1 to 3000 and on the largest `int`.

**Complexity.** Each step costs O(log n) for the digit sum, and the number of states is bounded by a small constant for 32-bit inputs, so the work and the space are effectively constant.

```java run
import java.util.HashSet;
import java.util.Set;

public final class HappyNumber {
    static int digitSquareSum(int n) {
        int sum = 0;
        for (; n > 0; n /= 10) sum += (n % 10) * (n % 10);
        return sum;
    }
    static boolean isHappy(int n) {
        Set<Integer> states = new HashSet<>();
        while (n != 1) {
            if (!states.add(n)) return false;
            n = digitSquareSum(n);
        }
        return true;
    }
    static boolean oracle(int n) {
        for (int step = 0; step < 1000; step++) {
            if (n == 1) return true;
            n = digitSquareSum(n);
        }
        return false;
    }

    public static void main(String[] args) {
        if (!isHappy(7)) throw new AssertionError("example 1");
        if (isHappy(4)) throw new AssertionError("example 2");
        if (!isHappy(1)) throw new AssertionError("1 is already happy");
        for (int n = 1; n <= 3000; n++)
            if (isHappy(n) != oracle(n)) throw new AssertionError("disagrees with the step budget at " + n);
        if (isHappy(Integer.MAX_VALUE) != oracle(Integer.MAX_VALUE)) throw new AssertionError("largest int");
    }
}
```

#### Solution: [Recognize] Longest Consecutive Sequence (LeetCode 128)
<!-- id: hm-longest-consecutive -->

**Approach.** Put every value in a hash set, which also removes repeats. Then, for each value `x` in the array, skip it when `x - 1` is in the set, because `x` is then in the middle of a run that is counted from its true start. When `x - 1` is absent, `x` is a run start, so count upward with membership tests of `x + 1`, `x + 2` and so on. Each run is counted exactly once from its start, and every value is walked over at most once in total, so the cost is linear. The oracle sorts the distinct values and scans for adjacent gaps, and the assertions agree on random arrays that include negatives and repeats.

**Complexity.** Expected O(n) time and O(n) extra space.

```java run
import java.util.Arrays;
import java.util.HashSet;
import java.util.Random;
import java.util.Set;

public final class LongestConsecutive {
    static int longestRun(int[] nums) {
        Set<Integer> all = new HashSet<>();
        for (int x : nums) all.add(x);
        int best = 0;
        for (int x : nums) {
            if (all.contains(x - 1)) continue;       // not a start of a run
            int len = 1;
            while (all.contains(x + len)) len++;
            best = Math.max(best, len);
        }
        return best;
    }
    static int oracle(int[] nums) {
        int[] s = Arrays.stream(nums).distinct().sorted().toArray();
        int best = 0, run = 0;
        for (int i = 0; i < s.length; i++) {
            run = (i > 0 && s[i] == s[i - 1] + 1) ? run + 1 : 1;
            best = Math.max(best, run);
        }
        return best;
    }

    public static void main(String[] args) {
        if (longestRun(new int[] {31, 8, 9, 30, 10, 32, 11}) != 4) throw new AssertionError("example 1");
        if (longestRun(new int[] {9, 9, 9}) != 1) throw new AssertionError("example 2");
        if (longestRun(new int[] {}) != 0) throw new AssertionError("empty");
        Random rnd = new Random(43);
        for (int t = 0; t < 4000; t++) {
            int[] x = new int[rnd.nextInt(14)];
            for (int i = 0; i < x.length; i++) x[i] = rnd.nextInt(20) - 8;
            if (longestRun(x) != oracle(x)) throw new AssertionError("disagrees with the sort oracle");
        }
    }
}
```
