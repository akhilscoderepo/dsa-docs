<!-- solutions-for: 05-sort-then-scan -->
### Sort Then Scan

#### Solution: [Build] Third Maximum Number (LeetCode 414)
<!-- id: so-third-maximum -->

**Approach.** Sort a copy and walk from the large end. A new place begins whenever a value differs from the one just above it, and the walk returns the value at which the place count reaches three. If the loop ends first, fewer than three distinct values exist and the largest value is returned. No sentinel is used, so `Integer.MIN_VALUE` in the input is handled like any other value. The oracle places the values in a `TreeSet`, which holds each distinct value once, and reads the third from the top.

**Complexity.** O(n log n) time and O(n) extra space for the copy.

```java run
import java.util.Arrays;
import java.util.Random;
import java.util.TreeSet;

public final class ThirdMaximum {
    static int thirdMax(int[] nums) {
        int[] a = nums.clone();
        Arrays.sort(a);
        int place = 1;
        for (int i = a.length - 1; i >= 0; i--) {
            if (i < a.length - 1 && a[i] != a[i + 1]) place++;
            if (place == 3) return a[i];
        }
        return a[a.length - 1];
    }
    static int oracle(int[] nums) {
        TreeSet<Integer> set = new TreeSet<>();
        for (int x : nums) set.add(x);
        if (set.size() < 3) return set.last();
        return set.descendingSet().stream().skip(2).findFirst().get();
    }

    public static void main(String[] args) {
        if (thirdMax(new int[] {2, 2, 3, 1, 5, 5}) != 2) throw new AssertionError("example 1");
        if (thirdMax(new int[] {8, 8, 4}) != 8) throw new AssertionError("example 2");
        if (thirdMax(new int[] {Integer.MIN_VALUE, 1, 2}) != Integer.MIN_VALUE) throw new AssertionError("the minimum is a legal third value");
        if (thirdMax(new int[] {Integer.MIN_VALUE, Integer.MIN_VALUE}) != Integer.MIN_VALUE) throw new AssertionError("fallback with the minimum");
        Random rnd = new Random(571);
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(10);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(6) == 0 ? Integer.MIN_VALUE : rnd.nextInt(6) - 2;
            int[] keep = a.clone();
            if (thirdMax(a) != oracle(a)) throw new AssertionError("differs from the TreeSet oracle on " + Arrays.toString(keep));
        }
    }
}
```

#### Solution: [Vary] Relative Ranks (LeetCode 506)
<!-- id: so-relative-ranks -->

**Approach.** Sort the positions `0 .. n-1`, not the scores, using a comparator that reads the score array so that the highest score comes first. The position at sorted rank `r` receives the medal for ranks 0 to 2 and the string `r + 1` otherwise, written into the answer at its original index. The comparator uses `Integer.compare`. The oracle computes each athlete's place directly as one more than the number of strictly higher scores, which needs no sorting.

**Complexity.** O(n log n) time and O(n) extra space for the boxed positions and the answer.

```java run
import java.util.Arrays;
import java.util.HashSet;
import java.util.Random;
import java.util.Set;

public final class RelativeRanks {
    static String[] relativeRanks(int[] score) {
        Integer[] by = new Integer[score.length];
        for (int i = 0; i < by.length; i++) by[i] = i;
        Arrays.sort(by, (i, j) -> Integer.compare(score[j], score[i]));
        String[] medal = {"Gold Medal", "Silver Medal", "Bronze Medal"};
        String[] out = new String[score.length];
        for (int rank = 0; rank < by.length; rank++) out[by[rank]] = rank < 3 ? medal[rank] : String.valueOf(rank + 1);
        return out;
    }
    static String[] oracle(int[] score) {
        String[] medal = {"Gold Medal", "Silver Medal", "Bronze Medal"};
        String[] out = new String[score.length];
        for (int i = 0; i < score.length; i++) {
            int place = 1;
            for (int s : score) if (s > score[i]) place++;
            out[i] = place <= 3 ? medal[place - 1] : String.valueOf(place);
        }
        return out;
    }

    public static void main(String[] args) {
        if (!Arrays.equals(relativeRanks(new int[] {40, 90, 70, 55}), new String[] {"4", "Gold Medal", "Silver Medal", "Bronze Medal"})) throw new AssertionError("example 1");
        if (!Arrays.equals(relativeRanks(new int[] {10}), new String[] {"Gold Medal"})) throw new AssertionError("example 2");
        Random rnd = new Random(572);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(10);
            Set<Integer> used = new HashSet<>();
            int[] score = new int[n];
            for (int i = 0; i < n; i++) {
                int v;
                do { v = rnd.nextInt(1000001); } while (!used.add(v));
                score[i] = v;
            }
            if (!Arrays.equals(relativeRanks(score), oracle(score))) throw new AssertionError("differs from the counting oracle on " + Arrays.toString(score));
        }
    }
}
```

#### Solution: [Boundary] Fewer Than k Distinct Values (Author exercise)
<!-- id: so-fewer-than-k-distinct -->

**Approach.** Walk the sorted copy from the large end, counting a new place whenever the value changes, and return the value when the count equals `k`. When the loop ends without reaching `k`, return the largest value, which is the stated fallback. The method never computes `length - k`, so a `k` beyond the array size is harmless. The test checks the examples, a value of `k` above the number of distinct values, `k` equal to one, arrays of equal values, and compares with a `TreeSet` oracle for every `k` from one to the array length plus two.

**Complexity.** O(n log n) time and O(n) extra space.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;
import java.util.TreeSet;

public final class FewerThanKDistinct {
    static int kthDistinctOrBest(int[] nums, int k) {
        int[] a = nums.clone();
        Arrays.sort(a);
        int place = 1;
        for (int i = a.length - 1; i >= 0; i--) {
            if (i < a.length - 1 && a[i] != a[i + 1]) place++;
            if (place == k) return a[i];
        }
        return a[a.length - 1];
    }
    static int oracle(int[] nums, int k) {
        TreeSet<Integer> set = new TreeSet<>();
        for (int x : nums) set.add(x);
        List<Integer> desc = new ArrayList<>(set.descendingSet());
        return k <= desc.size() ? desc.get(k - 1) : desc.get(0);
    }

    public static void main(String[] args) {
        if (kthDistinctOrBest(new int[] {4, 4, 4}, 2) != 4) throw new AssertionError("example 1");
        if (kthDistinctOrBest(new int[] {7, 1, 9, 9}, 3) != 1) throw new AssertionError("example 2");
        if (kthDistinctOrBest(new int[] {5, 9, 2}, 1) != 9) throw new AssertionError("k = 1 is the maximum");
        if (kthDistinctOrBest(new int[] {3}, 1000) != 3) throw new AssertionError("k far beyond the array");
        Random rnd = new Random(573);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(8);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(5) - 2;
            for (int k = 1; k <= n + 2; k++) {
                if (kthDistinctOrBest(a, k) != oracle(a, k)) throw new AssertionError("differs on " + Arrays.toString(a) + " k=" + k);
            }
        }
    }
}
```

#### Solution: [Recognize] Missing Number (LeetCode 268)
<!-- id: so-missing-number-sorted -->

**Approach.** Sort a copy. If nothing is missing before position `i`, the sorted array holds exactly the value `i` there, because the values are distinct and start at 0. The first position where the value is larger than the index shows that the number equal to the index is absent. If no position disagrees, the numbers 0 through n minus 1 are all present and the missing number is `n`. The oracle uses the difference between the sum 0 + ... + n, computed in a `long`, and the sum of the array, which does not sort.

**Complexity.** O(n log n) time and O(n) extra space for the copy.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.Random;

public final class MissingNumberSorted {
    static int missingNumber(int[] nums) {
        int[] a = nums.clone();
        Arrays.sort(a);
        for (int i = 0; i < a.length; i++) if (a[i] != i) return i;
        return a.length;
    }
    static int oracle(int[] nums) {
        long n = nums.length, expected = n * (n + 1) / 2, actual = 0;
        for (int x : nums) actual += x;
        return (int) (expected - actual);
    }

    public static void main(String[] args) {
        if (missingNumber(new int[] {3, 0, 1, 4}) != 2) throw new AssertionError("example 1");
        if (missingNumber(new int[] {0, 1, 2}) != 3) throw new AssertionError("example 2");
        if (missingNumber(new int[] {1}) != 0) throw new AssertionError("zero is missing");
        Random rnd = new Random(574);
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(12);
            List<Integer> pool = new ArrayList<>();
            for (int i = 0; i <= n; i++) pool.add(i);
            Collections.shuffle(pool, rnd);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = pool.get(i);
            int[] keep = a.clone();
            if (missingNumber(a) != oracle(a)) throw new AssertionError("differs from the sum oracle on " + Arrays.toString(keep));
            if (!Arrays.equals(a, keep)) throw new AssertionError("the argument must not change");
        }
    }
}
```
