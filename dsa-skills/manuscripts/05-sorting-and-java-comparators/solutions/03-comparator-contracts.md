<!-- solutions-for: 05-sorting-and-java-comparators -->
### Solutions For Valid Comparators

#### Solution: [Build] Safe Integer Comparator (Author exercise)
<!-- id: so-distance-comparator -->

**Approach.**
The comparator converts each value to `long` before it subtracts the target, takes the absolute value, and passes the two distances to `Long.compare`. The cast comes first, so the difference of two 32-bit values is exact. The comparator reads one key per value, so it is antisymmetric and transitive, and equal distances return zero. The harness checks the examples, checks the sign for the extreme pair, and tests the mirror property on random pairs.

**Complexity.**
- **Time** is O(1) per comparison, because it reads two values and computes two distances.
- **Space** is O(1), because no object is allocated per call.

```java run
import java.util.*;

public final class DistanceComparator {
    /**
     * Ranks integers by their distance to target.
     * Time: O(1) per comparison. Space: O(1).
     * Invariant: the result has the sign of (distance of x) - (distance of y).
     */
    static Comparator<Integer> byDistance(int target) {
        // The cast to long happens before the subtraction, so the distance is exact.
        return (x, y) -> Long.compare(Math.abs((long) x - target), Math.abs((long) y - target));
    }

    public static void main(String[] args) {
        // The statement examples.
        if (byDistance(10).compare(7, 15) >= 0) throw new AssertionError("example 1");
        if (byDistance(0).compare(Integer.MIN_VALUE, Integer.MAX_VALUE) <= 0) throw new AssertionError("example 2");
        // Equal distances return zero.
        if (byDistance(5).compare(3, 7) != 0) throw new AssertionError("tie");
        // Random pairs are checked against distances computed with an exact oracle, including the mirror property.
        Random rnd = new Random(71);
        int[] pool = {Integer.MIN_VALUE, Integer.MAX_VALUE, 0, 5, -5, 100};
        for (int t = 0; t < 1000; t++) {
            int target = pool[rnd.nextInt(pool.length)], x = pool[rnd.nextInt(pool.length)], y = pool[rnd.nextInt(pool.length)];
            long dx = Math.abs((long) x - target), dy = Math.abs((long) y - target);
            int expect = dx < dy ? -1 : (dx > dy ? 1 : 0);
            Comparator<Integer> c = byDistance(target);
            if (Integer.signum(c.compare(x, y)) != expect) throw new AssertionError("sign");
            if (Integer.signum(c.compare(x, y)) != -Integer.signum(c.compare(y, x))) throw new AssertionError("mirror");
        }
    }
}
```

#### Solution: [Vary] Chained Keys (Author exercise)
<!-- id: so-chained-keys -->

**Approach.**
The comparator reads the length first and consults the alphabetical order only when the lengths tie. `Comparator.comparingInt(String::length)` compares the lengths without subtraction, and `thenComparing` runs only on a zero result. Strings of equal length and equal content are identical, so the combined rule leaves no pair that needs an arbitrary order. The harness compares the result with a sort by the single combined key `length` and then `content`, built from a padded string.

**Complexity.**
- **Time** is O(n log n * m), where m is the longest string, because each comparison reads at most m characters.
- **Space** is O(n) for the working buffer of the object sort.

```java run
import java.util.*;

public final class ChainedKeys {
    /**
     * Sorts names by length, then alphabetically.
     * Time: O(n log n * m). Space: O(n).
     * Invariant: after the sort, adjacent names are ordered by (length, text).
     */
    static void sortNames(String[] names) {
        // The second key runs only when the first key returns zero.
        Arrays.sort(names, Comparator.comparingInt(String::length).thenComparing(Comparator.naturalOrder()));
    }

    public static void main(String[] args) {
        // The statement examples.
        String[] e1 = {"bb", "a", "ab", "c"};
        sortNames(e1);
        if (!Arrays.equals(e1, new String[] {"a", "c", "ab", "bb"})) throw new AssertionError("example 1");
        String[] e2 = {"", "b", ""};
        sortNames(e2);
        if (!Arrays.equals(e2, new String[] {"", "", "b"})) throw new AssertionError("example 2");
        // Random lists are checked against an oracle that builds one combined string key.
        Random rnd = new Random(72);
        for (int t = 0; t < 500; t++) {
            String[] a = new String[rnd.nextInt(10)];
            for (int k = 0; k < a.length; k++) {
                StringBuilder sb = new StringBuilder();
                for (int len = rnd.nextInt(4); len > 0; len--) sb.append((char) ('a' + rnd.nextInt(3)));
                a[k] = sb.toString();
            }
            String[] expect = a.clone();
            // The key pads the length to two digits, so text order of keys equals (length, text) order.
            Arrays.sort(expect, Comparator.comparing(s -> String.format("%02d", s.length()) + s));
            sortNames(a);
            if (!Arrays.equals(a, expect)) throw new AssertionError(Arrays.toString(a));
        }
    }
}
```

#### Solution: [Boundary] Equal Keys And Extreme Values (Author exercise)
<!-- id: so-check-contract -->

**Approach.**
The method tries every ordered triple of positions, including repeated positions, and tests the three rules. The mirror rule compares the signs of both argument orders, the chain rule tests `c(x, z) <= 0` whenever both earlier results are nonpositive, and the tie rule compares the signs against a third value. The loop returns false at the first violated rule. The invariant is that no triple checked so far broke a rule. The harness applies the method to comparators with known behavior.

**Complexity.**
- **Time** is O(n^3), because the loops try every triple of the n sample values.
- **Space** is O(1), because the method keeps no data beyond the loop indexes.

```java run
import java.util.*;

public final class CheckContract {
    /**
     * Returns true when c is antisymmetric, transitive and tie-consistent on sample.
     * Time: O(n^3). Space: O(1).
     * Invariant: no earlier triple broke a rule.
     */
    static boolean isValid(Integer[] sample, Comparator<Integer> c) {
        // The three loops try every ordered triple, including repeated positions.
        for (Integer x : sample) {
            for (Integer y : sample) {
                // Mirror rule: swapping the arguments flips the sign.
                if (Integer.signum(c.compare(x, y)) != -Integer.signum(c.compare(y, x))) return false;
                for (Integer z : sample) {
                    // Chain rule: x before y and y before z force x before z.
                    if (c.compare(x, y) <= 0 && c.compare(y, z) <= 0 && c.compare(x, z) > 0) return false;
                    // Tie rule: values that tie compare alike against every third value.
                    if (c.compare(x, y) == 0 && Integer.signum(c.compare(x, z)) != Integer.signum(c.compare(y, z))) return false;
                }
            }
        }
        return true;
    }

    public static void main(String[] args) {
        // The statement examples.
        Integer[] extremes = {Integer.MIN_VALUE, 0, Integer.MAX_VALUE};
        if (isValid(extremes, (a, b) -> a - b)) throw new AssertionError("example 1");
        if (!isValid(new Integer[] {3, 3, 8}, Integer::compare)) throw new AssertionError("example 2");
        // Edge cases: the empty sample, the safe rule on extremes, and the never-zero rule on a tie.
        if (!isValid(new Integer[0], (a, b) -> a - b)) throw new AssertionError("empty");
        if (!isValid(extremes, Integer::compare)) throw new AssertionError("safe on extremes");
        Comparator<Integer> neverZero = (a, b) -> a < b ? -1 : 1;
        if (isValid(new Integer[] {3, 3}, neverZero)) throw new AssertionError("never zero with a tie");
        // The rule also fails on distinct values, because it returns 1 when a value meets itself.
        if (isValid(new Integer[] {1, 2, 3}, neverZero)) throw new AssertionError("never zero, distinct values");
        // A cyclic rule on 0, 1, 2 (each value beats the next) breaks the chain rule.
        Comparator<Integer> cyclic = (a, b) -> a.equals(b) ? 0 : ((b - a + 3) % 3 == 1 ? -1 : 1);
        if (isValid(new Integer[] {0, 1, 2}, cyclic)) throw new AssertionError("cyclic");
        // Random samples: Integer::compare must always pass on the full range.
        Random rnd = new Random(73);
        int[] pool = {Integer.MIN_VALUE, Integer.MAX_VALUE, 0, 1, -1};
        for (int t = 0; t < 300; t++) {
            Integer[] s = new Integer[rnd.nextInt(6)];
            for (int k = 0; k < s.length; k++) s[k] = pool[rnd.nextInt(pool.length)];
            if (!isValid(s, Integer::compare)) throw new AssertionError("compare must pass");
        }
    }
}
```

#### Solution: [Recognize] Largest Number (LeetCode 179)
<!-- id: so-order-for-largest -->

**Approach.**
The method boxes the values and sorts them with a comparator that puts `x` before `y` when the string `x + y` is larger than `y + x`. Both strings have the same length, so their text order equals their numeric order. The comparator reads the number formed by a pair, so it is antisymmetric and ties only when both orders give the same number. It is transitive because it equals the order of a fixed key relation that the harness verifies on random triples. After the sort, no adjacent pair gains from a swap. The harness compares the concatenated answer with a permutation oracle.

**Complexity.**
- **Time** is O(n log n * L), where L is the longest decimal length, because each comparison builds strings of length at most 2L.
- **Space** is O(n) for the boxed array and the answer.

```java run
import java.util.*;

public final class OrderForLargest {
    static int cmp(int x, int y) {
        // The larger concatenation decides the order, and equal concatenations tie.
        return (Integer.toString(y) + x).compareTo(Integer.toString(x) + y);
    }

    /**
     * Returns the values arranged for the largest concatenation.
     * Time: O(n log n * L). Space: O(n).
     * Invariant: after the sort, for every adjacent pair x, y the text x + y >= y + x.
     */
    static int[] order(int[] nums) {
        Integer[] boxed = new Integer[nums.length];
        for (int i = 0; i < nums.length; i++) boxed[i] = nums[i];
        Arrays.sort(boxed, (x, y) -> cmp(x, y));
        int[] out = new int[nums.length];
        for (int i = 0; i < out.length; i++) out[i] = boxed[i];
        return out;
    }

    static String join(int[] a) {
        StringBuilder sb = new StringBuilder();
        for (int v : a) sb.append(v);
        return sb.toString();
    }

    static String best(int[] a, int k, String cur) {
        if (k == a.length) return cur;
        String bestSoFar = cur;
        for (int i = k; i < a.length; i++) {
            int tmp = a[k]; a[k] = a[i]; a[i] = tmp;
            String r = best(a, k + 1, cur);
            tmp = a[k]; a[k] = a[i]; a[i] = tmp;
            if (r.compareTo(bestSoFar) > 0) bestSoFar = r;
        }
        return bestSoFar;
    }

    static String brute(int[] nums) {
        String[] best = {""};
        permute(nums.clone(), 0, best);
        return best[0];
    }

    static void permute(int[] a, int k, String[] best) {
        if (k == a.length) {
            String t = join(a);
            if (best[0].isEmpty() || t.compareTo(best[0]) > 0) best[0] = t;
            return;
        }
        for (int i = k; i < a.length; i++) {
            int tmp = a[k]; a[k] = a[i]; a[i] = tmp;
            permute(a, k + 1, best);
            tmp = a[k]; a[k] = a[i]; a[i] = tmp;
        }
    }

    public static void main(String[] args) {
        // The statement examples and the empty array.
        if (!Arrays.equals(order(new int[] {824, 8247}), new int[] {824, 8247})) throw new AssertionError("example 1");
        if (!Arrays.equals(order(new int[] {0, 10, 2}), new int[] {2, 10, 0})) throw new AssertionError("example 2");
        if (order(new int[0]).length != 0) throw new AssertionError("empty");
        Random rnd = new Random(74);
        int[] pool = {0, 1, 3, 12, 121, 30, 34, 5, 9, 824, 8247, 1000000000};
        // The comparator obeys the contract on random triples.
        for (int t = 0; t < 2000; t++) {
            int x = pool[rnd.nextInt(pool.length)], y = pool[rnd.nextInt(pool.length)], z = pool[rnd.nextInt(pool.length)];
            if (Integer.signum(cmp(x, y)) != -Integer.signum(cmp(y, x))) throw new AssertionError("mirror");
            if (cmp(x, y) <= 0 && cmp(y, z) <= 0 && cmp(x, z) > 0) throw new AssertionError("chain");
        }
        // Random arrays are checked against the permutation oracle.
        for (int t = 0; t < 300; t++) {
            int[] a = new int[rnd.nextInt(6)];
            for (int k = 0; k < a.length; k++) a[k] = pool[rnd.nextInt(pool.length)];
            int[] r = order(a);
            int[] sortedIn = a.clone(), sortedOut = r.clone();
            Arrays.sort(sortedIn);
            Arrays.sort(sortedOut);
            if (!Arrays.equals(sortedIn, sortedOut)) throw new AssertionError("values changed");
            if (a.length > 0 && !join(r).equals(brute(a))) throw new AssertionError(Arrays.toString(a));
        }
    }
}
```
