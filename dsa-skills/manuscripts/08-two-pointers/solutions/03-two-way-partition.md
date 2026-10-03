<!-- solutions-for: 08-two-way-partition -->
### Two-Way Partition

#### Solution: [Build] Sort Array By Parity (LeetCode 905)
<!-- id: tp-parity-split -->

**Approach.** Keep `lo` at the left end and `hi` at the right end, with everything before `lo` even and everything after `hi` odd. An even value under `lo` lets `lo` advance, an odd value under `hi` lets `hi` retreat, and otherwise the two values are a misplaced pair that trade places while both pointers advance. The loop runs while `lo <= hi`, so the last single position is classified too, and the returned `lo` is the number of even values. Evenness is tested with `% 2 == 0` and oddness with `% 2 != 0`, because a negative odd value has remainder minus one. The check confirms both examples, compares against a bit-test oracle on random arrays with negatives, and counts steps, trades, and writes per position to back the claims that each position is written at most once and the trades never exceed half the length.

**Complexity.** Linear time, since every step retires at least one position, and constant extra memory.

```java run
import java.util.Arrays;
import java.util.Random;

public final class ParitySplit {
    static int steps, trades;
    static int[] writes;

    static int sortByParity(int[] a) {
        int lo = 0, hi = a.length - 1;
        steps = 0;
        trades = 0;
        writes = new int[a.length];
        while (lo <= hi) {
            steps++;
            if (a[lo] % 2 == 0) lo++;
            else if (a[hi] % 2 != 0) hi--;
            else {
                int t = a[lo]; a[lo] = a[hi]; a[hi] = t;
                writes[lo]++; writes[hi]++; trades++;
                lo++; hi--;
            }
        }
        return lo;
    }

    static void check(int[] original) {
        int[] a = original.clone();
        int count = sortByParity(a);
        int evens = 0;
        for (int v : original) if ((v & 1) == 0) evens++;
        if (count != evens) throw new AssertionError("count " + count + " for " + Arrays.toString(original));
        for (int i = 0; i < a.length; i++) {
            boolean even = (a[i] & 1) == 0;
            if (even != (i < count)) throw new AssertionError("region wrong at " + i + " in " + Arrays.toString(a));
        }
        int[] x = a.clone(), y = original.clone();
        Arrays.sort(x);
        Arrays.sort(y);
        if (!Arrays.equals(x, y)) throw new AssertionError("values changed");
        if (trades > a.length / 2) throw new AssertionError("too many trades " + trades);
        if (steps > a.length) throw new AssertionError("too many steps " + steps);
        for (int w : writes) if (w > 1) throw new AssertionError("a position was written twice");
    }

    public static void main(String[] args) {
        int[] one = {3, 1, 4, 6, 7, 2};
        if (sortByParity(one) != 3 || !Arrays.equals(one, new int[] {2, 6, 4, 1, 7, 3})) throw new AssertionError("example 1 " + Arrays.toString(one));
        int[] two = {1, 1, 2};
        if (sortByParity(two) != 1 || !Arrays.equals(two, new int[] {2, 1, 1})) throw new AssertionError("example 2 " + Arrays.toString(two));
        if (-3 % 2 != -1 || (-3 % 2 == 1)) throw new AssertionError("negative odd remainder is minus one");
        int[] negatives = {-3, -4, 5, -8, Integer.MIN_VALUE, Integer.MAX_VALUE};
        check(negatives);
        check(new int[0]);
        check(new int[] {7});
        check(new int[] {8});
        check(new int[] {2, 2, 2, 2});
        check(new int[] {9, 9, 9});
        Random rnd = new Random(803);
        for (int t = 0; t < 4000; t++) {
            int n = rnd.nextInt(16);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(41) - 20;
            check(a);
        }
    }
}
```

#### Solution: [Vary] Partition Around Pivot (Author exercise)
<!-- id: tp-around-pivot -->

**Approach.** The loop is the parity loop with the front test replaced by `value < pivot`. A smaller value under `lo` stays, a value that is at least the pivot under `hi` stays, and a misplaced pair trades places. Values equal to the pivot belong to the back region, so they sit beside the larger ones. The comparison is written with `<` and never as a difference, since `Integer.MIN_VALUE - 1` wraps around to a large positive number and would flip the answer. The check confirms both examples, compares the count and the regions with a counting oracle on random arrays that include the extremes of `int`, demonstrates the subtraction bug on one concrete pair, and verifies that the pivot value is never moved into the front region.

**Complexity.** Linear time with one pass of the two pointers, and constant extra memory.

```java run
import java.util.Arrays;
import java.util.Random;

public final class AroundPivot {
    static int partition(int[] a, int pivot) {
        int lo = 0, hi = a.length - 1;
        while (lo <= hi) {
            if (a[lo] < pivot) lo++;
            else if (a[hi] >= pivot) hi--;
            else {
                int t = a[lo]; a[lo] = a[hi]; a[hi] = t;
                lo++; hi--;
            }
        }
        return lo;
    }

    static void check(int[] original, int pivot) {
        int[] a = original.clone();
        int count = partition(a, pivot);
        int smaller = 0;
        for (int v : original) if (Integer.compare(v, pivot) < 0) smaller++;
        if (count != smaller) throw new AssertionError("count for " + Arrays.toString(original) + " pivot " + pivot);
        for (int i = 0; i < a.length; i++) {
            if ((a[i] < pivot) != (i < count)) throw new AssertionError("region wrong at " + i + " in " + Arrays.toString(a));
        }
        int[] x = a.clone(), y = original.clone();
        Arrays.sort(x);
        Arrays.sort(y);
        if (!Arrays.equals(x, y)) throw new AssertionError("values changed");
    }

    public static void main(String[] args) {
        int[] one = {9, 2, 7, 4, 5, 1};
        if (partition(one, 5) != 3 || !Arrays.equals(one, new int[] {1, 2, 4, 7, 5, 9})) throw new AssertionError("example 1 " + Arrays.toString(one));
        int[] two = {4, 6, 5};
        if (partition(two, 4) != 0 || !Arrays.equals(two, new int[] {4, 6, 5})) throw new AssertionError("example 2 " + Arrays.toString(two));
        if (Integer.MIN_VALUE - 1 < 0) throw new AssertionError("a difference of MIN_VALUE and 1 wraps to a positive value");
        if (!(Integer.MIN_VALUE < 1)) throw new AssertionError("direct comparison is correct");
        int[] extremes = {Integer.MAX_VALUE, Integer.MIN_VALUE, 0, -1, 1};
        check(extremes, 0);
        check(extremes, Integer.MIN_VALUE);
        check(extremes, Integer.MAX_VALUE);
        check(new int[0], 3);
        check(new int[] {5}, 5);
        check(new int[] {5, 5, 5}, 5);
        Random rnd = new Random(804);
        for (int t = 0; t < 4000; t++) {
            int n = rnd.nextInt(14);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(11) - 5;
            check(a, rnd.nextInt(13) - 6);
        }
    }
}
```

#### Solution: [Boundary] One Empty Region (Author exercise)
<!-- id: tp-one-empty-region -->

**Approach.** Use the parity loop and count the trades. In an array of only even values the left pointer walks the whole array and is stopped by the loop condition once it passes `hi`, not by an element, so the boundary is the length and no trade happens. In an array of only odd values the right pointer walks all the way to the front and the boundary is zero. The result is the pair of the boundary and the trade count. The check confirms both examples, runs the empty and one-element cases, confirms that an already partitioned array is left unchanged with zero trades, and compares the trade count with the number of odd values that sit inside the first stretch of the final even region, which is the number of misplaced pairs.

**Complexity.** Linear time in the worst case, and a trade count of at most half the length, with constant extra memory.

```java run
import java.util.Arrays;
import java.util.Random;

public final class OneEmptyRegion {
    static int[] split(int[] a) {
        int lo = 0, hi = a.length - 1, trades = 0;
        while (lo <= hi) {
            if (a[lo] % 2 == 0) lo++;
            else if (a[hi] % 2 != 0) hi--;
            else {
                int t = a[lo]; a[lo] = a[hi]; a[hi] = t;
                trades++; lo++; hi--;
            }
        }
        return new int[] {lo, trades};
    }

    static int[] oracle(int[] original) {
        int evens = 0;
        for (int v : original) if ((v & 1) == 0) evens++;
        int misplaced = 0;
        for (int i = 0; i < evens; i++) if ((original[i] & 1) != 0) misplaced++;
        return new int[] {evens, misplaced};
    }

    public static void main(String[] args) {
        int[] one = {2, 4, 6, 8};
        if (!Arrays.equals(split(one), new int[] {4, 0}) || !Arrays.equals(one, new int[] {2, 4, 6, 8})) throw new AssertionError("example 1");
        int[] two = {7, 5, 3};
        if (!Arrays.equals(split(two), new int[] {0, 0}) || !Arrays.equals(two, new int[] {7, 5, 3})) throw new AssertionError("example 2");
        if (!Arrays.equals(split(new int[0]), new int[] {0, 0})) throw new AssertionError("empty");
        if (!Arrays.equals(split(new int[] {5}), new int[] {0, 0})) throw new AssertionError("one odd");
        if (!Arrays.equals(split(new int[] {6}), new int[] {1, 0})) throw new AssertionError("one even");
        int[] sorted = {-2, 0, 4, 3, 5, -7};
        int[] copy = sorted.clone();
        if (!Arrays.equals(split(sorted), new int[] {3, 0}) || !Arrays.equals(sorted, copy)) throw new AssertionError("already partitioned");
        Random rnd = new Random(805);
        for (int t = 0; t < 4000; t++) {
            int n = rnd.nextInt(16);
            int[] a = new int[n];
            int mode = rnd.nextInt(4);
            for (int i = 0; i < n; i++) {
                int v = rnd.nextInt(41) - 20;
                if (mode == 0) v = v * 2;
                if (mode == 1) v = v * 2 + 1;
                a[i] = v;
            }
            int[] expected = oracle(a);
            int[] got = split(a);
            if (!Arrays.equals(got, expected)) throw new AssertionError(Arrays.toString(got) + " versus " + Arrays.toString(expected));
            if (got[1] > n / 2) throw new AssertionError("trades above half the length");
            if (mode == 0 && (got[0] != n || got[1] != 0)) throw new AssertionError("all even");
            if (mode == 1 && (got[0] != 0 || got[1] != 0)) throw new AssertionError("all odd");
        }
    }
}
```

#### Solution: [Recognize] Sort Array By Parity II (LeetCode 922)
<!-- id: tp-alternating-parity -->

**Approach.** Two pointers start at the front, `e` on even indexes and `o` on odd indexes, and each moves in steps of two. If the value under `e` is even, that slot is already right and `e` advances by two. If the value under `o` is odd, `o` advances by two. Otherwise the slot at `e` holds an odd value and the slot at `o` holds an even value, which is a misplaced pair of values that belong in each other's slots, so they trade places and both pointers advance. Because the counts of evens and odds are equal, whenever one slot class has a wrong value the other class has one too, which is why the trade always exists. The check confirms both examples, builds random arrays with equal counts of evens and odds including negatives, and verifies the slot classes, the multiset, and the trade count.

**Complexity.** Linear time with each pointer visiting its own half of the indexes once, and constant extra memory.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.Random;

public final class AlternatingParity {
    static int trades;

    static void arrange(int[] a) {
        int e = 0, o = 1;
        trades = 0;
        while (e < a.length && o < a.length) {
            if (a[e] % 2 == 0) e += 2;
            else if (a[o] % 2 != 0) o += 2;
            else {
                int t = a[e]; a[e] = a[o]; a[o] = t;
                trades++; e += 2; o += 2;
            }
        }
    }

    static void check(int[] original) {
        int[] a = original.clone();
        arrange(a);
        for (int i = 0; i < a.length; i++) {
            boolean even = (a[i] & 1) == 0;
            if (even != (i % 2 == 0)) throw new AssertionError("slot " + i + " wrong in " + Arrays.toString(a) + " from " + Arrays.toString(original));
        }
        int[] x = a.clone(), y = original.clone();
        Arrays.sort(x);
        Arrays.sort(y);
        if (!Arrays.equals(x, y)) throw new AssertionError("values changed");
        if (trades > a.length / 2) throw new AssertionError("too many trades");
    }

    public static void main(String[] args) {
        int[] one = {4, 2, 5, 7};
        arrange(one);
        if (!Arrays.equals(one, new int[] {4, 5, 2, 7})) throw new AssertionError("example 1 " + Arrays.toString(one));
        int[] two = {3, 0, 1, 6};
        arrange(two);
        if (!Arrays.equals(two, new int[] {0, 3, 6, 1})) throw new AssertionError("example 2 " + Arrays.toString(two));
        check(new int[0]);
        check(new int[] {1, 2});
        check(new int[] {1, 3, 2, 4});
        check(new int[] {-3, -2, Integer.MIN_VALUE, Integer.MAX_VALUE});
        Random rnd = new Random(806);
        for (int t = 0; t < 4000; t++) {
            int pairs = rnd.nextInt(8);
            List<Integer> values = new ArrayList<>();
            for (int i = 0; i < pairs; i++) {
                values.add((rnd.nextInt(31) - 15) * 2);
                values.add((rnd.nextInt(31) - 15) * 2 + 1);
            }
            Collections.shuffle(values, rnd);
            int[] a = new int[values.size()];
            for (int i = 0; i < a.length; i++) a[i] = values.get(i);
            check(a);
        }
    }
}
```
