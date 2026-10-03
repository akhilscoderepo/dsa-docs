<!-- solutions-for: 05-set-sequences -->
### Set Sequences

#### Solution: [Build] Longest Consecutive Sequence (LeetCode 128)
<!-- id: hm-longest-span -->

**Approach.** Load every value into a set. Loop over the set and skip any value whose predecessor is present, since it is inside a chain. For a start, walk upward with membership tests and measure the chain. Keep the longest chain, breaking ties toward the smaller start so the answer does not depend on hash iteration order. An empty set leaves the initial answer `[0, 0]`. The oracle sorts the distinct values, splits them into runs by adjacent differences and picks the longest with the smallest start, and the assertions require identical pairs on random arrays.

**Complexity.** Expected O(n) time and O(n) extra space.

```java run
import java.util.Arrays;
import java.util.HashSet;
import java.util.Random;
import java.util.Set;

public final class LongestSpan {
    static int[] longestRunSpan(int[] nums) {
        Set<Integer> all = new HashSet<>();
        for (int x : nums) all.add(x);
        int bestStart = 0, bestLen = 0;
        for (int x : all) {
            if (all.contains(x - 1)) continue;
            int len = 1;
            while (all.contains(x + len)) len++;
            if (len > bestLen || (len == bestLen && x < bestStart)) { bestLen = len; bestStart = x; }
        }
        return new int[] {bestStart, bestLen};
    }
    static int[] oracle(int[] nums) {
        int[] s = Arrays.stream(nums).distinct().sorted().toArray();
        int bestStart = 0, bestLen = 0;
        for (int i = 0; i < s.length; ) {
            int j = i;
            while (j + 1 < s.length && s[j + 1] == s[j] + 1) j++;
            int len = j - i + 1;
            if (len > bestLen) { bestLen = len; bestStart = s[i]; }
            i = j + 1;
        }
        return new int[] {bestStart, bestLen};
    }

    public static void main(String[] args) {
        if (!Arrays.equals(longestRunSpan(new int[] {50, 12, 13, 49, 11, 51, 52, 14}), new int[] {11, 4})) throw new AssertionError("example 1");
        if (!Arrays.equals(longestRunSpan(new int[] {-3, -2, -2}), new int[] {-3, 2})) throw new AssertionError("example 2");
        if (!Arrays.equals(longestRunSpan(new int[] {}), new int[] {0, 0})) throw new AssertionError("empty");
        Random rnd = new Random(81);
        for (int t = 0; t < 4000; t++) {
            int[] x = new int[rnd.nextInt(14)];
            for (int i = 0; i < x.length; i++) x[i] = rnd.nextInt(24) - 10;
            if (!Arrays.equals(longestRunSpan(x), oracle(x))) throw new AssertionError("disagrees with the sorted-run oracle on " + Arrays.toString(x));
        }
    }
}
```

#### Solution: [Vary] Intersection of Two Arrays (LeetCode 349)
<!-- id: hm-shared-in-order -->

**Approach.** Put the first array into a set of values still waiting to be reported. Scan the second array in order, and for each value call `remove`, which returns true only when the value was present, so a shared value is reported the first time it appears in the second array and never again. The set shrinks as answers are produced. The oracle scans the second array and keeps a value if it occurs in the first array and has not already been listed, using linear searches, and the assertions require the same list on random inputs.

**Complexity.** Expected O(n + m) time and O(n) extra space.

```java run
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Random;
import java.util.Set;

public final class SharedInOrder {
    static List<Integer> sharedOnce(int[] a, int[] b) {
        Set<Integer> pending = new HashSet<>();
        for (int x : a) pending.add(x);
        List<Integer> out = new ArrayList<>();
        for (int y : b) if (pending.remove(y)) out.add(y);
        return out;
    }
    static boolean has(int[] arr, int v) { for (int x : arr) if (x == v) return true; return false; }
    static List<Integer> oracle(int[] a, int[] b) {
        List<Integer> out = new ArrayList<>();
        for (int y : b) if (has(a, y) && !out.contains(y)) out.add(y);
        return out;
    }

    public static void main(String[] args) {
        if (!sharedOnce(new int[] {1, 3, 3, 7}, new int[] {7, 3, 3, 5, 1, 7}).equals(List.of(7, 3, 1))) throw new AssertionError("example 1");
        if (!sharedOnce(new int[] {2, 2}, new int[] {2, 2, 2}).equals(List.of(2))) throw new AssertionError("example 2");
        Set<Integer> s = new HashSet<>(List.of(4));
        if (!s.remove(4) || s.remove(4)) throw new AssertionError("remove is true only the first time");
        Random rnd = new Random(82);
        for (int t = 0; t < 4000; t++) {
            int[] a = new int[rnd.nextInt(10)], b = new int[rnd.nextInt(10)];
            for (int i = 0; i < a.length; i++) a[i] = rnd.nextInt(8);
            for (int i = 0; i < b.length; i++) b[i] = rnd.nextInt(8);
            if (!sharedOnce(a, b).equals(oracle(a, b))) throw new AssertionError("disagrees with the linear oracle");
        }
    }
}
```

#### Solution: [Boundary] Duplicate Starts (Author exercise)
<!-- id: hm-duplicate-starts -->

**Approach.** Insert every value into a set, which collapses repeated values, then count the values whose predecessor is absent. Counting starts while looping over the array would count a repeated start once per copy, so the example `[4, 4, 5, 9, 9, 9, 2]` would report 6 starts, from the 4s, the 9s and the 2, and not the 3 runs. Looping over the set makes each start appear once. The oracle sorts the distinct values and counts the places where the gap to the previous value is not exactly one, and the assertions show the array-loop variant overcounting and the set version matching the oracle.

**Complexity.** Expected O(n) time and O(n) extra space.

```java run
import java.util.Arrays;
import java.util.HashSet;
import java.util.Random;
import java.util.Set;

public final class DuplicateStarts {
    static int countRuns(int[] nums) {
        Set<Integer> all = new HashSet<>();
        for (int x : nums) all.add(x);
        int starts = 0;
        for (int x : all) if (!all.contains(x - 1)) starts++;
        return starts;
    }
    static int countOverArray(int[] nums) {
        Set<Integer> all = new HashSet<>();
        for (int x : nums) all.add(x);
        int starts = 0;
        for (int x : nums) if (!all.contains(x - 1)) starts++;
        return starts;
    }
    static int oracle(int[] nums) {
        int[] s = Arrays.stream(nums).distinct().sorted().toArray();
        int runs = 0;
        for (int i = 0; i < s.length; i++) if (i == 0 || s[i] != s[i - 1] + 1) runs++;
        return runs;
    }

    public static void main(String[] args) {
        if (countRuns(new int[] {4, 4, 5, 9, 9, 9, 2}) != 3) throw new AssertionError("example 1");
        if (countRuns(new int[] {}) != 0) throw new AssertionError("example 2");
        if (countOverArray(new int[] {4, 4, 5, 9, 9, 9, 2}) != 6) throw new AssertionError("counting over the array repeats starts");
        Random rnd = new Random(83);
        for (int t = 0; t < 4000; t++) {
            int[] x = new int[rnd.nextInt(14)];
            for (int i = 0; i < x.length; i++) x[i] = rnd.nextInt(16) - 6;
            if (countRuns(x) != oracle(x)) throw new AssertionError("disagrees with the sorted gaps");
        }
    }
}
```

#### Solution: [Recognize] Happy Number (LeetCode 202)
<!-- id: hm-happy-steps -->

**Approach.** Keep the visited states in a set. Before each replacement, `add` the current number. If the add fails, the state has repeated and the loop never reaches 1, so return -1. Otherwise compute the next state and count one replacement. When the current number is already 1 the loop does not run and the answer is 0. The oracle follows the process with a fixed budget of 1000 replacements and reports the step count at which 1 first appears, or -1, and the assertions compare on every value from 1 to 3000.

**Complexity.** Each replacement costs O(log n) for the digits, and only a small constant number of states can occur for 32-bit inputs, so the work and the space are effectively constant.

```java run
import java.util.HashSet;
import java.util.Set;

public final class HappySteps {
    static int next(int n) {
        int sum = 0;
        for (int m = n; m > 0; m /= 10) sum += (m % 10) * (m % 10);
        return sum;
    }
    static int happySteps(int n) {
        Set<Integer> states = new HashSet<>();
        int steps = 0;
        while (n != 1) {
            if (!states.add(n)) return -1;
            n = next(n);
            steps++;
        }
        return steps;
    }
    static int oracle(int n) {
        for (int step = 0; step <= 1000; step++) {
            if (n == 1) return step;
            n = next(n);
        }
        return -1;
    }

    public static void main(String[] args) {
        if (happySteps(13) != 2) throw new AssertionError("example 1");
        if (happySteps(20) != -1) throw new AssertionError("example 2");
        if (happySteps(1) != 0) throw new AssertionError("1 needs no replacement");
        for (int n = 1; n <= 3000; n++)
            if (happySteps(n) != oracle(n)) throw new AssertionError("disagrees with the step budget at " + n);
    }
}
```
