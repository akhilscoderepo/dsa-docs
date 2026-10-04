<!-- solutions-for: 05-sorting-and-java-comparators -->
### Solutions For Scans After A Sort

#### Solution: [Build] Third Maximum Number (LeetCode 414)
<!-- id: so-third-maximum -->

**Approach.**
The method sorts a copy and scans it from the last index toward 0. The rank starts at 1 for the largest value and grows by 1 each time a value differs from its right neighbor. The method returns the value at the moment the rank reaches 3, and it returns the largest value if the loop ends first. The method keeps no sentinel, so the input value `Integer.MIN_VALUE` is a legal answer. The invariant after reading index `i` is that `rank` equals the number of distinct values in `sorted[i..n - 1]`.

**Complexity.**
- **Time** is O(n log n), because the sort dominates the linear scan.
- **Space** is O(n), because of the sorted copy.

```java run
import java.util.*;

public final class ThirdMaximum {
    /**
     * Returns the third largest distinct value, or the largest when fewer than three distinct values exist.
     * Time: O(n log n). Space: O(n).
     * Invariant: after index i, rank is the number of distinct values in sorted[i..n - 1].
     */
    static int thirdMax(int[] nums) {
        int[] sorted = Arrays.copyOf(nums, nums.length);
        Arrays.sort(sorted);
        int rank = 1;
        // The scan reads each neighbor pair once, from the top.
        for (int i = sorted.length - 2; i >= 0; i--) {
            // A change between neighbors starts a new distinct value.
            if (sorted[i] != sorted[i + 1]) {
                rank++;
                if (rank == 3) return sorted[i];
            }
        }
        // The loop ended with fewer than three distinct values, so the fallback is the largest value.
        return sorted[sorted.length - 1];
    }

    /** Oracle: collects the distinct values in a TreeSet and reads from the top. */
    static int brute(int[] nums) {
        TreeSet<Integer> set = new TreeSet<>();
        for (int v : nums) set.add(v);
        if (set.size() < 3) return set.last();
        Iterator<Integer> it = set.descendingIterator();
        it.next();
        it.next();
        return it.next();
    }

    public static void main(String[] args) {
        // The statement examples, including the sentinel trap.
        if (thirdMax(new int[] {10, -3, 10, 7, 7, 1}) != 1) throw new AssertionError("example 1");
        if (thirdMax(new int[] {1, 2, Integer.MIN_VALUE}) != Integer.MIN_VALUE) throw new AssertionError("example 2");
        if (thirdMax(new int[] {8, 8}) != 8 || thirdMax(new int[] {5}) != 5) throw new AssertionError("short inputs");
        // Java fact from the lesson: reading the third position from the end throws on a short array.
        boolean threw = false;
        try { int[] two = {8, 8}; int x = two[two.length - 3]; } catch (ArrayIndexOutOfBoundsException e) { threw = true; }
        if (!threw) throw new AssertionError("index");
        // Random arrays are checked against the TreeSet oracle.
        Random rnd = new Random(121);
        for (int t = 0; t < 500; t++) {
            int[] a = new int[1 + rnd.nextInt(10)];
            for (int k = 0; k < a.length; k++) a[k] = rnd.nextInt(6) == 0 ? Integer.MIN_VALUE : rnd.nextInt(6) - 2;
            if (thirdMax(a) != brute(a)) throw new AssertionError(Arrays.toString(a));
        }
    }
}
```

#### Solution: [Vary] Relative Ranks (LeetCode 506)
<!-- id: so-relative-ranks -->

**Approach.**
The method sorts the indexes of the scores by score in descending order, as in the lesson on stability. It then walks the sorted indexes with a position counter that starts at 1. For each index `idx`, it writes the medal or the decimal position into `ranks[idx]`, so the answer keeps the original positions of the scores. The scores are distinct, so the comparator never ties. The invariant after step `p` is that the `p` highest scores have their final rank strings in `ranks`.

**Complexity.**
- **Time** is O(n log n), because the sort of indexes dominates the linear walk.
- **Space** is O(n) for the boxed indexes and the answer.

```java run
import java.util.*;

public final class RelativeRanks {
    /**
     * Returns the rank string for each score, in the original order.
     * Time: O(n log n). Space: O(n).
     * Invariant: after step p, the p highest scores have their final rank strings.
     */
    static String[] ranks(int[] scores) {
        Integer[] order = new Integer[scores.length];
        for (int i = 0; i < order.length; i++) order[i] = i;
        // The comparator reads the scores through the indexes, largest score first.
        Arrays.sort(order, (a, b) -> Integer.compare(scores[b], scores[a]));
        String[] out = new String[scores.length];
        // One step per position in the descending order.
        for (int p = 0; p < order.length; p++) {
            String label = p == 0 ? "Gold Medal" : p == 1 ? "Silver Medal" : p == 2 ? "Bronze Medal" : String.valueOf(p + 1);
            // The answer goes to the original position of the score.
            out[order[p]] = label;
        }
        return out;
    }

    public static void main(String[] args) {
        // The statement examples and the empty input.
        if (!Arrays.equals(ranks(new int[] {40, 90, 10, 75}), new String[] {"Bronze Medal", "Gold Medal", "4", "Silver Medal"})) throw new AssertionError("example 1");
        if (!Arrays.equals(ranks(new int[] {7}), new String[] {"Gold Medal"})) throw new AssertionError("example 2");
        if (ranks(new int[0]).length != 0) throw new AssertionError("empty");
        // Random distinct scores are checked against a count of higher scores.
        Random rnd = new Random(122);
        for (int t = 0; t < 500; t++) {
            int n = rnd.nextInt(9);
            List<Integer> pool = new ArrayList<>();
            for (int v = 0; v < 30; v++) pool.add(v);
            Collections.shuffle(pool, rnd);
            int[] s = new int[n];
            for (int k = 0; k < n; k++) s[k] = pool.get(k);
            String[] got = ranks(s);
            for (int k = 0; k < n; k++) {
                int higher = 0;
                for (int v : s) if (v > s[k]) higher++;
                String expect = higher == 0 ? "Gold Medal" : higher == 1 ? "Silver Medal" : higher == 2 ? "Bronze Medal" : String.valueOf(higher + 1);
                if (!got[k].equals(expect)) throw new AssertionError(Arrays.toString(s));
            }
        }
    }
}
```

#### Solution: [Boundary] Fewer Than k Distinct Values (Author exercise)
<!-- id: so-kth-distinct -->

**Approach.**
The method sorts a copy and scans it from the smallest value. The rank starts at 1 for the smallest value and grows by 1 whenever a value differs from its left neighbor. The method returns the value at the moment the rank equals `k`. If the loop ends first, the array has fewer than `k` distinct values, and the method returns the largest value, which sits at the last index. The rank is an `int` compared with `k` up to 10^9, so the comparison needs no wider type. The invariant after index `i` is that `rank` is the number of distinct values in `sorted[0..i]`.

**Complexity.**
- **Time** is O(n log n), because the sort dominates the linear scan.
- **Space** is O(n), because of the sorted copy.

```java run
import java.util.*;

public final class KthDistinct {
    /**
     * Returns the k-th smallest distinct value, or the largest value when fewer than k distinct values exist.
     * Time: O(n log n). Space: O(n).
     * Invariant: after index i, rank is the number of distinct values in sorted[0..i].
     */
    static int kthDistinct(int[] nums, int k) {
        int[] sorted = Arrays.copyOf(nums, nums.length);
        Arrays.sort(sorted);
        // The smallest value has rank 1, so k = 1 returns it without a loop step.
        if (k == 1) return sorted[0];
        int rank = 1;
        for (int i = 1; i < sorted.length; i++) {
            // A change between neighbors starts a new distinct value.
            if (sorted[i] != sorted[i - 1]) {
                rank++;
                if (rank == k) return sorted[i];
            }
        }
        // The loop ended before the rank reached k, so the stated fallback applies.
        return sorted[sorted.length - 1];
    }

    public static void main(String[] args) {
        // The statement examples and the edge values of k.
        if (kthDistinct(new int[] {5, 1, 5, 3}, 2) != 3) throw new AssertionError("example 1");
        if (kthDistinct(new int[] {4, 4}, 3) != 4) throw new AssertionError("example 2");
        if (kthDistinct(new int[] {9, 2, 2}, 1) != 2) throw new AssertionError("k = 1");
        if (kthDistinct(new int[] {7}, 1000000000) != 7) throw new AssertionError("huge k");
        // Random arrays are checked against a TreeSet oracle.
        Random rnd = new Random(123);
        for (int t = 0; t < 500; t++) {
            int[] a = new int[1 + rnd.nextInt(10)];
            for (int x = 0; x < a.length; x++) a[x] = rnd.nextInt(6) - 2;
            int k = 1 + rnd.nextInt(7);
            TreeSet<Integer> set = new TreeSet<>();
            for (int v : a) set.add(v);
            int expect;
            if (set.size() < k) expect = set.last();
            else {
                Iterator<Integer> it = set.iterator();
                expect = it.next();
                for (int c = 1; c < k; c++) expect = it.next();
            }
            if (kthDistinct(a, k) != expect) throw new AssertionError(Arrays.toString(a) + " k=" + k);
        }
    }
}
```

#### Solution: [Recognize] Missing Number (LeetCode 268)
<!-- id: so-missing-number -->

**Approach.**
The method sorts a copy. The values are distinct and lie in the range 0 to `n`, so in the sorted copy the value at index `i` equals `i` for every index before the missing value and exceeds `i` from the missing value onward. The scan returns the first index whose value differs from the index. If every index matches, the missing value is `n`. The invariant before index `i` is that `sorted[0..i - 1]` equals `0..i - 1`, so the missing value is at least `i`.

**Complexity.**
- **Time** is O(n log n), because the sort dominates the linear scan.
- **Space** is O(n), because of the sorted copy.

```java run
import java.util.*;

public final class MissingNumber {
    /**
     * Returns the value of 0..n that is absent from nums.
     * Time: O(n log n). Space: O(n).
     * Invariant: before index i, sorted[0..i - 1] equals 0..i - 1.
     */
    static int missing(int[] nums) {
        int[] sorted = Arrays.copyOf(nums, nums.length);
        Arrays.sort(sorted);
        // The scan checks one index per step.
        for (int i = 0; i < sorted.length; i++) {
            // The first mismatch shows that the value i is absent.
            if (sorted[i] != i) return i;
        }
        // Every index matched, so the absent value is n.
        return sorted.length;
    }

    public static void main(String[] args) {
        // The statement examples and the empty input.
        if (missing(new int[] {5, 2, 0, 1, 4}) != 3) throw new AssertionError("example 1");
        if (missing(new int[] {0, 1, 2}) != 3) throw new AssertionError("example 2");
        if (missing(new int[0]) != 0) throw new AssertionError("empty");
        // Random arrays are built by removing one value from a shuffled range and checked against the removed value.
        Random rnd = new Random(124);
        for (int t = 0; t < 500; t++) {
            int n = rnd.nextInt(10);
            List<Integer> all = new ArrayList<>();
            for (int v = 0; v <= n; v++) all.add(v);
            Collections.shuffle(all, rnd);
            int removed = all.remove(all.size() - 1);
            int[] a = new int[n];
            for (int k = 0; k < n; k++) a[k] = all.get(k);
            if (missing(a) != removed) throw new AssertionError(Arrays.toString(a));
        }
    }
}
```
