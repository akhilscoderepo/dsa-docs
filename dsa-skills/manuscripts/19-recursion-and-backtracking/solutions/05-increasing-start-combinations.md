<!-- solutions-for: 05-increasing-start-combinations -->
### Increasing-Start Combinations

#### Solution: [Build] Choose Two From Four (Author exercise)
<!-- id: bt-choose-two -->

**Approach.** The first pick takes any position, the second pick takes any position strictly after it, and a pair is recorded when the path holds two values. Values are read by position, so the pairs come out in array order whether or not the array is sorted. The oracle is a pair of nested loops over positions, which cannot repeat a pair or reorder one. Random arrays of length 2 to 6 feed both versions and their outputs must be equal, and the pair count must be n * (n - 1) / 2.

**Complexity.** The search visits n(n + 1)/2 calls at most, so it takes quadratic time in the array length, and the stack has depth two.

```java run
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Random;
import java.util.Set;

public final class ChooseTwo {
    static void pick(int[] nums, int start, List<Integer> path, List<List<Integer>> out) {
        if (path.size() == 2) {
            out.add(new ArrayList<>(path));
            return;
        }
        for (int i = start; i < nums.length; i++) {
            path.add(nums[i]);
            pick(nums, i + 1, path, out);
            path.remove(path.size() - 1);
        }
    }

    static List<List<Integer>> pairs(int[] nums) {
        List<List<Integer>> out = new ArrayList<>();
        pick(nums, 0, new ArrayList<>(), out);
        return out;
    }

    static List<List<Integer>> oracle(int[] nums) {
        List<List<Integer>> out = new ArrayList<>();
        for (int i = 0; i < nums.length; i++) for (int j = i + 1; j < nums.length; j++) out.add(List.of(nums[i], nums[j]));
        return out;
    }

    public static void main(String[] args) {
        List<List<Integer>> one = List.of(List.of(1, 2), List.of(1, 3), List.of(1, 4), List.of(2, 3), List.of(2, 4), List.of(3, 4));
        if (!pairs(new int[] {1, 2, 3, 4}).equals(one)) throw new AssertionError("example 1");
        if (!pairs(new int[] {5, -1, 0}).equals(List.of(List.of(5, -1), List.of(5, 0), List.of(-1, 0)))) throw new AssertionError("example 2");
        Random rnd = new Random(19501);
        for (int t = 0; t < 2000; t++) {
            int n = 2 + rnd.nextInt(5);
            Set<Integer> used = new HashSet<>();
            int[] a = new int[n];
            for (int i = 0; i < n; i++) {
                int v;
                do { v = rnd.nextInt(101) - 50; } while (!used.add(v));
                a[i] = v;
            }
            List<List<Integer>> got = pairs(a);
            if (!got.equals(oracle(a))) throw new AssertionError("differs on length " + n);
            if (got.size() != n * (n - 1) / 2) throw new AssertionError("pair count");
        }
    }
}
```

#### Solution: [Vary] Combinations From One To N (LeetCode 77)
<!-- id: bt-combinations-k -->

**Approach.** The call records the path when it holds `k` numbers and otherwise loops from `start` to `n - need + 1`, appending, recursing with `i + 1` and removing. The tight bound is a safe optimisation here, because a call with fewer than `need` numbers to its right cannot finish. The oracle enumerates every mask over 1 to n, keeps those with exactly k set bits, and sorts the lists lexicographically, which is the order of the search. The harness also confirms that each combination is strictly increasing and that the number of results matches the product formula for the binomial coefficient.

**Complexity.** C(n, k) results at O(k) per copy, plus the interior calls, which the room bound keeps within a factor of k of the results, and a stack k deep.

```java run
import java.util.ArrayList;
import java.util.List;

public final class CombinationsK {
    static void pick(int n, int k, int start, List<Integer> path, List<List<Integer>> out) {
        int need = k - path.size();
        if (need == 0) {
            out.add(new ArrayList<>(path));
            return;
        }
        for (int i = start; i <= n - need + 1; i++) {
            path.add(i);
            pick(n, k, i + 1, path, out);
            path.remove(path.size() - 1);
        }
    }

    static List<List<Integer>> combine(int n, int k) {
        List<List<Integer>> out = new ArrayList<>();
        pick(n, k, 1, new ArrayList<>(), out);
        return out;
    }

    static List<List<Integer>> oracle(int n, int k) {
        List<List<Integer>> out = new ArrayList<>();
        for (int m = 0; m < (1 << n); m++) {
            if (Integer.bitCount(m) != k) continue;
            List<Integer> s = new ArrayList<>();
            for (int i = 0; i < n; i++) if ((m >> i & 1) == 1) s.add(i + 1);
            out.add(s);
        }
        out.sort((a, b) -> {
            for (int i = 0; i < a.size(); i++) if (!a.get(i).equals(b.get(i))) return a.get(i) - b.get(i);
            return 0;
        });
        return out;
    }

    public static void main(String[] args) {
        if (!combine(4, 3).equals(List.of(List.of(1, 2, 3), List.of(1, 2, 4), List.of(1, 3, 4), List.of(2, 3, 4)))) throw new AssertionError("example 1");
        if (!combine(1, 1).equals(List.of(List.of(1)))) throw new AssertionError("example 2");
        for (int n = 1; n <= 12; n++) {
            for (int k = 1; k <= n; k++) {
                List<List<Integer>> got = combine(n, k);
                if (!got.equals(oracle(n, k))) throw new AssertionError("differs at n=" + n + ", k=" + k);
                long c = 1;
                for (int j = 1; j <= k; j++) c = c * (n - k + j) / j;
                if (got.size() != c) throw new AssertionError("count at n=" + n + ", k=" + k);
                for (List<Integer> s : got) for (int j = 1; j < s.size(); j++) if (s.get(j) <= s.get(j - 1)) throw new AssertionError("not increasing");
            }
        }
    }
}
```

#### Solution: [Boundary] Insufficient Remaining Values (Author exercise)
<!-- id: bt-room-bound -->

**Approach.** The search counts its own invocations in a field while the loop stops at `n - need + 1`. When `k` exceeds `n` the bound at the first call is below the start, the loop never runs, and the answer is zero combinations after exactly one call. When `k` is zero the first call already has no need left and records one empty combination. The harness checks the call count against a closed form that shares nothing with the recursion: every call is a prefix of some combination, and the prefixes of length j that can still be completed number C(n - k + j, j), so the total is the sum of those over j from 0 to k. It also shows that a loop bounded by the end of the row makes at least as many calls, with strictly more on four numbers and two picks, and that a bound one too small drops every combination that ends with the largest number.

**Complexity.** The number of calls is the sum above, and each combination costs an O(k) copy.

```java run
import java.util.ArrayList;
import java.util.List;

public final class RoomBound {
    static long calls;

    static void pick(int n, int k, int start, int slack, List<Integer> path, List<List<Integer>> out) {
        calls++;
        int need = k - path.size();
        if (need == 0) {
            out.add(new ArrayList<>(path));
            return;
        }
        int hi = n - need + 1 + slack;
        for (int i = start; i <= Math.min(hi, n); i++) {
            path.add(i);
            pick(n, k, i + 1, slack, path, out);
            path.remove(path.size() - 1);
        }
    }

    static long[] run(int n, int k, int slack) {
        calls = 0;
        List<List<Integer>> out = new ArrayList<>();
        pick(n, k, 1, slack, new ArrayList<>(), out);
        return new long[] {out.size(), calls};
    }

    static long choose(int a, int b) {
        long[][] c = new long[a + 2][a + 2];
        for (int i = 0; i <= a; i++) {
            c[i][0] = 1;
            for (int j = 1; j <= i; j++) c[i][j] = c[i - 1][j - 1] + (j <= i - 1 ? c[i - 1][j] : 0);
        }
        return c[a][b];
    }

    public static void main(String[] args) {
        long[] one = run(4, 2, 0);
        if (one[0] != 6 || one[1] != 10) throw new AssertionError("example 1: " + one[0] + "," + one[1]);
        long[] two = run(3, 5, 0);
        if (two[0] != 0 || two[1] != 1) throw new AssertionError("example 2");
        long[] zero = run(5, 0, 0);
        if (zero[0] != 1 || zero[1] != 1) throw new AssertionError("k = 0");
        for (int n = 1; n <= 14; n++) {
            for (int k = 0; k <= 16; k++) {
                long[] tight = run(n, k, 0);
                long want = 1;
                long count = 0;
                if (k <= n) {
                    want = 0;
                    for (int j = 0; j <= k; j++) want += choose(n - k + j, j);
                    count = choose(n, k);
                }
                if (tight[0] != count || tight[1] != want) throw new AssertionError("differs at n=" + n + ", k=" + k);
                long[] loose = run(n, k, 1000);
                if (loose[0] != tight[0] || loose[1] < tight[1]) throw new AssertionError("a loose bound finds the same panels with no fewer calls");
                if (k >= 1 && k <= n) {
                    long[] tooSmall = run(n, k, -1);
                    if (tooSmall[0] >= tight[0]) throw new AssertionError("a bound that is one too small loses panels, n=" + n + ", k=" + k);
                }
            }
        }
        if (run(4, 2, 1000)[1] <= run(4, 2, 0)[1]) throw new AssertionError("the loose bound makes more calls on 4 and 2");
    }
}
```

#### Solution: [Recognize] Combination Sum III (LeetCode 216)
<!-- id: bt-sum-three -->

**Approach.** The state is the start digit, the remaining sum, and the path. A call with `k` digits on the path records it when the remaining sum is exactly zero, and otherwise the loop runs from `start` to 9, skipping out of the loop when the digit exceeds the remaining sum, which is safe because all digits are positive and the loop is in increasing order. The room bound is applied as in the previous rung. The oracle takes every mask over the digits 1 to 9, keeps masks with k bits and sum n, and sorts the lists. The harness compares the two over every k from 1 to 9 and every n up to 60.

**Complexity.** At most C(9, k) leaves, so a constant bound for this alphabet, and in general the same form as the combinations search.

```java run
import java.util.ArrayList;
import java.util.List;

public final class SumThree {
    static void pick(int k, int remaining, int start, List<Integer> path, List<List<Integer>> out) {
        int need = k - path.size();
        if (need == 0) {
            if (remaining == 0) out.add(new ArrayList<>(path));
            return;
        }
        for (int d = start; d <= 9 - need + 1; d++) {
            if (d > remaining) break;
            path.add(d);
            pick(k, remaining - d, d + 1, path, out);
            path.remove(path.size() - 1);
        }
    }

    static List<List<Integer>> sets(int k, int n) {
        List<List<Integer>> out = new ArrayList<>();
        pick(k, n, 1, new ArrayList<>(), out);
        return out;
    }

    static List<List<Integer>> oracle(int k, int n) {
        List<List<Integer>> out = new ArrayList<>();
        for (int m = 0; m < (1 << 9); m++) {
            if (Integer.bitCount(m) != k) continue;
            List<Integer> s = new ArrayList<>();
            int sum = 0;
            for (int i = 0; i < 9; i++) if ((m >> i & 1) == 1) { s.add(i + 1); sum += i + 1; }
            if (sum == n) out.add(s);
        }
        out.sort((a, b) -> {
            for (int i = 0; i < a.size(); i++) if (!a.get(i).equals(b.get(i))) return a.get(i) - b.get(i);
            return 0;
        });
        return out;
    }

    public static void main(String[] args) {
        if (!sets(3, 9).equals(List.of(List.of(1, 2, 6), List.of(1, 3, 5), List.of(2, 3, 4)))) throw new AssertionError("example 1");
        if (!sets(4, 1).isEmpty()) throw new AssertionError("example 2");
        for (int k = 1; k <= 9; k++) {
            for (int n = 1; n <= 60; n++) {
                if (!sets(k, n).equals(oracle(k, n))) throw new AssertionError("differs at k=" + k + ", n=" + n);
            }
        }
    }
}
```
