<!-- solutions-for: 04-hash-maps-and-sets -->
### Solutions For Membership Sets

#### Solution: [Build] Contains Duplicate (LeetCode 217)
<!-- id: hm-contains-duplicate -->

**Approach.**
One pass keeps a set of the values read so far. For each value, the call `add` stores it and reports whether it was new, so a `false` result proves that an earlier index holds the same value. The invariant is that after index `i`, the set holds exactly the distinct values of `nums[0..i]`. If the loop finishes, no index repeated a value. The harness also asserts three Java facts from the lesson. The call `add` returns false for a stored value. The call `contains` finds a value that another `Integer` object boxed. The class `LinkedHashSet` keeps insertion order.

**Complexity.**
- **Time** is O(n) on average, because the loop makes n calls to `add` that each take expected constant time.
- **Space** is O(n), because a file of distinct values stores every value in the set.

```java run
import java.util.*;

public final class ContainsDuplicate {
    /**
     * Reports whether any value occurs twice.
     * Time: O(n) expected. Space: O(n).
     * Invariant: after index i, seen holds the distinct values of nums[0..i].
     */
    static boolean containsDuplicate(int[] nums) {
        Set<Integer> seen = new HashSet<>();
        // The loop runs once per element, which gives n iterations.
        for (int i = 0; i < nums.length; i++) {
            // add returns false when the value is stored already, which proves a repeat.
            if (!seen.add(nums[i])) {
                return true;
            }
        }
        // Every value was new, so no value repeats.
        return false;
    }

    /** Lesson code: the pairwise method, kept as the oracle. */
    static boolean naive(int[] nums) {
        for (int i = 0; i < nums.length; i++) {
            for (int j = i + 1; j < nums.length; j++) {
                if (nums[i] == nums[j]) return true;
            }
        }
        return false;
    }

    public static void main(String[] args) {
        // The statement examples and the empty array.
        if (!containsDuplicate(new int[] {8, 3, 5, 3})) throw new AssertionError("example 1");
        if (containsDuplicate(new int[] {-2, 0, 2})) throw new AssertionError("example 2");
        if (containsDuplicate(new int[0])) throw new AssertionError("empty");
        if (!containsDuplicate(new int[] {4, 7, 1, 7, 9}) || containsDuplicate(new int[] {3, 1, 4, 2})) throw new AssertionError("trace inputs");
        // Java facts from the lesson.
        Set<Integer> s = new HashSet<>();
        if (!s.add(1000) || s.add(1000)) throw new AssertionError("add return value");
        if (!s.contains(Integer.valueOf(500 + 500))) throw new AssertionError("lookup uses equals");
        if (!Integer.valueOf(127).equals(Integer.valueOf(127))) throw new AssertionError("equals");
        Set<Integer> ordered = new LinkedHashSet<>(List.of(9, 4, 8));
        if (!new ArrayList<>(ordered).equals(List.of(9, 4, 8))) throw new AssertionError("insertion order");
        // Random arrays are checked against the pairwise oracle.
        Random rnd = new Random(41);
        for (int t = 0; t < 500; t++) {
            int[] a = new int[rnd.nextInt(10)];
            for (int k = 0; k < a.length; k++) a[k] = rnd.nextInt(14) - 4;
            if (containsDuplicate(a) != naive(a)) throw new AssertionError(Arrays.toString(a));
        }
    }
}
```

#### Solution: [Vary] Intersection Of Two Arrays (LeetCode 349)
<!-- id: hm-intersection -->

**Approach.**
The method puts every value of `b` into a set, then reads `a` from left to right. A value of `a` joins the answer when the set of `b` holds it and the answer has not reported it yet. A second set, `reported`, enforces that each shared value appears once, and the left-to-right scan gives the order of first occurrence in `a`. The invariant is that after index `i`, the answer holds the shared values of `a[0..i]` once each, in order of first occurrence.

**Complexity.**
- **Time** is O(n + m) on average for arrays of lengths n and m, because each array is read once with expected constant-time set operations.
- **Space** is O(n + m), because the set of `b`, the set `reported` and the answer together hold at most n + m values.

```java run
import java.util.*;

public final class IntersectionOfTwo {
    /**
     * Returns the values present in both arrays, once each, in the order of first occurrence in a.
     * Time: O(n + m) expected. Space: O(n + m).
     * Invariant: after index i, out holds the shared values of a[0..i], each once, in first-occurrence order.
     */
    static int[] intersection(int[] a, int[] b) {
        // The set of b answers "does b hold this value" in expected constant time.
        Set<Integer> inB = new HashSet<>();
        for (int y : b) inB.add(y);
        Set<Integer> reported = new HashSet<>();
        List<Integer> out = new ArrayList<>();
        // The scan of a costs n iterations.
        for (int x : a) {
            // A value joins the answer only if b holds it and it is new to the answer.
            if (inB.contains(x) && reported.add(x)) {
                out.add(x);
            }
        }
        int[] res = new int[out.size()];
        for (int k = 0; k < res.length; k++) res[k] = out.get(k);
        return res;
    }

    public static void main(String[] args) {
        // The statement examples.
        if (!Arrays.equals(intersection(new int[] {9, 4, 9, 8, 4}, new int[] {4, 9, 5}), new int[] {9, 4})) throw new AssertionError("example 1");
        if (intersection(new int[0], new int[] {1}).length != 0) throw new AssertionError("example 2");
        // Random arrays are checked against a quadratic oracle.
        Random rnd = new Random(42);
        for (int t = 0; t < 500; t++) {
            int[] a = new int[rnd.nextInt(9)], b = new int[rnd.nextInt(9)];
            for (int k = 0; k < a.length; k++) a[k] = rnd.nextInt(8) - 3;
            for (int k = 0; k < b.length; k++) b[k] = rnd.nextInt(8) - 3;
            List<Integer> expect = new ArrayList<>();
            for (int x : a) {
                boolean inb = false;
                for (int y : b) if (x == y) inb = true;
                if (inb && !expect.contains(x)) expect.add(x);
            }
            int[] got = intersection(a, b);
            if (got.length != expect.size()) throw new AssertionError("size");
            for (int k = 0; k < got.length; k++) if (got[k] != expect.get(k)) throw new AssertionError("order");
        }
    }
}
```

#### Solution: [Boundary] Happy Number (LeetCode 202)
<!-- id: hm-happy-number -->

**Approach.**
The digit-square sum is a function of the current value alone, so the sequence of values repeats forever once any value occurs twice. A set of produced values detects that repeat. The loop stops with true when the value is 1, and with false when `add` reports a value that the set already holds. The invariant is that the set holds every value produced before the current one, so a value inside the set proves a cycle that never reaches 1. For `n` up to 2^31 - 1, the first sum is at most 9 * 81 = 729 and every later value stays below 1000, so the set stays small.

**Complexity.**
- **Time** is O(log n) for the first digit sum plus O(1) steps, because every later value is below 1000 and so at most 1000 distinct values occur before a repeat.
- **Space** is O(1) in n, because the set holds at most 1000 values.

```java run
import java.util.*;

public final class HappyNumber {
    /**
     * Reports whether repeated digit-square sums reach 1.
     * Time: O(log n) for the first sum plus at most about 1000 steps. Space: O(1) in n.
     * Invariant: seen holds every value produced before the current one.
     */
    static boolean isHappy(int n) {
        Set<Integer> seen = new HashSet<>();
        int cur = n;
        // The loop ends at 1, or when a value repeats; add returns false for a repeat.
        while (cur != 1) {
            if (!seen.add(cur)) {
                return false;
            }
            cur = digitSquareSum(cur);
        }
        return true;
    }

    static int digitSquareSum(int v) {
        int sum = 0;
        // Each pass removes the last decimal digit, so the loop runs once per digit.
        while (v > 0) {
            int d = v % 10;
            sum += d * d;
            v /= 10;
        }
        return sum;
    }

    public static void main(String[] args) {
        // The statement examples, with the exact chain of the second one.
        if (!isHappy(19)) throw new AssertionError("example 1");
        if (isHappy(2)) throw new AssertionError("example 2");
        int[] chain = {2, 4, 16, 37, 58, 89, 145, 42, 20, 4};
        for (int k = 0; k + 1 < chain.length; k++) if (digitSquareSum(chain[k]) != chain[k + 1]) throw new AssertionError("chain " + k);
        int[] happy = {19, 82, 68, 100, 1};
        for (int k = 0; k + 1 < happy.length; k++) if (digitSquareSum(happy[k]) != happy[k + 1]) throw new AssertionError("happy chain " + k);
        // The largest input still ends, and every later value is below 1000.
        if (digitSquareSum(Integer.MAX_VALUE) > 729 + 0) throw new AssertionError("bound");
        isHappy(Integer.MAX_VALUE);
        // A step-limited oracle checks every value up to 3000: after 1000 steps a value is either 1 or in a cycle.
        for (int n = 1; n <= 3000; n++) {
            int v = n;
            for (int s = 0; s < 1000 && v != 1; s++) v = digitSquareSum(v);
            if (isHappy(n) != (v == 1)) throw new AssertionError("n=" + n);
        }
    }
}
```

#### Solution: [Recognize] Longest Consecutive Sequence (LeetCode 128)
<!-- id: hm-longest-consecutive -->

**Approach.**
The set holds every value, so one test answers whether `x - 1` exists. A value without a predecessor starts a run, and the method walks upward from it with tests on `x + 1`, `x + 2` and so on. A value with a predecessor lies inside a run that an earlier start already measures, so the loop skips it. The invariant is that every run is walked once, from its first value. The walks together take one step per distinct value. The loop reads values from the set, so duplicates in `nums` cause no repeated walk. Plain `int` arithmetic needs one guard. The walk stops when `x + len` wraps past `Integer.MAX_VALUE`, and the test on `x - 1` skips the wrap at `Integer.MIN_VALUE`. The harness checks a run at each end.

**Complexity.**
- **Time** is O(n) on average, because n insertions build the set and the walks visit each distinct value once.
- **Space** is O(n), because the set holds up to n distinct values.

```java run
import java.util.*;

public final class LongestConsecutive {
    /**
     * Returns the length of the longest run of consecutive values.
     * Time: O(n) expected. Space: O(n).
     * Invariant: each run is walked once, from its smallest value.
     */
    static int longestConsecutive(int[] nums) {
        Set<Integer> all = new HashSet<>();
        for (int x : nums) all.add(x);
        int best = 0;
        // The loop visits each distinct value once.
        for (int x : all) {
            // A stored predecessor means a walk from an earlier start covers x.
            if (all.contains(x - 1) && x != Integer.MIN_VALUE) continue;
            int len = 1;
            // The inner walk runs only from run starts, so all walks total at most the distinct values.
            while (x + len > x && all.contains(x + len)) len++;
            best = Math.max(best, len);
        }
        return best;
    }

    public static void main(String[] args) {
        // The statement examples.
        if (longestConsecutive(new int[] {100, 4, 200, 1, 3, 2}) != 4) throw new AssertionError("example 1");
        if (longestConsecutive(new int[] {7, 7, 7}) != 1) throw new AssertionError("example 2");
        if (longestConsecutive(new int[0]) != 0) throw new AssertionError("empty");
        // A run that ends at the largest int and one that starts at the smallest int.
        if (longestConsecutive(new int[] {Integer.MAX_VALUE - 1, Integer.MAX_VALUE}) != 2) throw new AssertionError("max edge");
        if (longestConsecutive(new int[] {Integer.MIN_VALUE, Integer.MIN_VALUE + 1}) != 2) throw new AssertionError("min edge");
        // Random arrays are checked against a sort-based oracle.
        Random rnd = new Random(43);
        for (int t = 0; t < 500; t++) {
            int[] a = new int[rnd.nextInt(12)];
            for (int k = 0; k < a.length; k++) a[k] = rnd.nextInt(16) - 5;
            int[] s = a.clone();
            Arrays.sort(s);
            int expect = 0, run = 0;
            for (int k = 0; k < s.length; k++) {
                if (k == 0 || s[k] == s[k - 1] + 1) run++;
                else if (s[k] != s[k - 1]) run = 1;
                expect = Math.max(expect, run);
            }
            if (longestConsecutive(a) != expect) throw new AssertionError(Arrays.toString(a));
        }
    }
}
```
