<!-- solutions-for: 91-sort-then-commit-greedily -->
### Solutions For Sort Then Commit Greedily

#### Solution: [Build] Assign Cookies (LeetCode 455)
<!-- id: gr-sort-satisfied-children -->

**Approach.**
The method sorts the child positions by greed, with ties broken by smaller position, and sorts a copy of the cookies. It walks the cookies from the smallest. A cookie goes to the first child in the sorted order who is still unsatisfied when it is large enough, and a cookie that is too small for that child is useless for every later child, so the walk discards it. The method records the position of every satisfied child and sorts the positions at the end. The swap argument of lesson 01 shows the count is the largest possible, and the tie rule makes the listed positions deterministic.

After each cookie, the satisfied children are the first `k` of the sorted order, and the cookies read so far are used or discarded.

**Complexity.**
- **Time** is O(n log n + m log m), because the two sorts dominate the single walk.
- **Space** is O(n + m) for the sorted copies and the answer.

```java run
import java.util.*;

public final class SortSatisfiedChildren {
    /**
     * Returns the positions of the satisfied children in increasing order.
     * Time: O(n log n + m log m). Space: O(n + m).
     * Invariant: the children served so far are the first k children in greed order, and k is largest for the cookies read.
     */
    static List<Integer> satisfied(int[] g, int[] s) {
        Integer[] order = new Integer[g.length];
        for (int i = 0; i < order.length; i++) order[i] = i;
        Arrays.sort(order, (a, b) -> g[a] != g[b] ? Integer.compare(g[a], g[b]) : Integer.compare(a, b)); // greed, then position
        int[] cookies = s.clone();                                     // keep the caller's order
        Arrays.sort(cookies);
        List<Integer> out = new ArrayList<>();
        int k = 0;                                                     // next child in greed order
        for (int c : cookies) {                                        // smallest cookie first
            if (k < order.length && c >= g[order[k]]) out.add(order[k++]); // serve the next child
        }
        Collections.sort(out);                                         // report positions in increasing order
        return out;
    }

    static int brute(int[] g, int[] s, int gi, boolean[] used) {
        if (gi == g.length) return 0;
        int best = brute(g, s, gi + 1, used);
        for (int k = 0; k < s.length; k++) {
            if (!used[k] && s[k] >= g[gi]) {
                used[k] = true;
                best = Math.max(best, 1 + brute(g, s, gi + 1, used));
                used[k] = false;
            }
        }
        return best;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!satisfied(new int[] {3, 1, 2}, new int[] {2, 3}).equals(List.of(1, 2))) throw new AssertionError("ex1");
        if (!satisfied(new int[] {2, 2, 2}, new int[] {1, 2}).equals(List.of(0))) throw new AssertionError("ex2");
        // Large values compare without overflow, and the input arrays keep their order.
        int[] cookies = {5, 1};
        satisfied(new int[] {Integer.MAX_VALUE}, cookies);
        if (cookies[0] != 5) throw new AssertionError("mutation");
        if (satisfied(new int[] {Integer.MAX_VALUE}, new int[] {Integer.MAX_VALUE}).size() != 1) throw new AssertionError("max");
        // Random inputs: the count must be optimal, and the satisfied children must be feasible together.
        Random rnd = new Random(2091);
        for (int t = 0; t < 500; t++) {
            int[] g = new int[rnd.nextInt(6)], s = new int[rnd.nextInt(6)];
            for (int k = 0; k < g.length; k++) g[k] = 1 + rnd.nextInt(7);
            for (int k = 0; k < s.length; k++) s[k] = 1 + rnd.nextInt(7);
            List<Integer> got = satisfied(g, s);
            if (got.size() != brute(g, s, 0, new boolean[s.length])) throw new AssertionError("count " + t);
            int[] need = new int[got.size()];
            for (int k = 0; k < need.length; k++) need[k] = g[got.get(k)];
            Arrays.sort(need);
            int[] have = s.clone();
            Arrays.sort(have);
            int p = 0;
            for (int h : have) if (p < need.length && h >= need[p]) p++;
            if (p != need.length) throw new AssertionError("feasible " + t);
        }
    }
}
```

#### Solution: [Vary] Non-overlapping Intervals (LeetCode 435)
<!-- id: gr-intervals-with-gap -->

**Approach.**
The method sorts the intervals by end and keeps an interval when its start is at least the previous kept end plus `gap`. The sum uses `long`, because an end near 2^31 plus a gap near 10^9 passes the `int` range. The exchange argument still holds. An interval with an earlier end leaves a bound `end + gap` that is no larger, so every later interval that fits after the later end also fits after the earlier end. The method returns the number of intervals that it does not keep.

After each interval, `bound` is the smallest start that a later kept interval may have, for a largest kept set of the intervals read.

**Complexity.**
- **Time** is O(n log n), because the sort dominates the scan.
- **Space** is O(n) for the sorted copy.

```java run
import java.util.*;

public final class IntervalsWithGap {
    /**
     * Returns the smallest number of removals so kept intervals are at least gap apart.
     * Time: O(n log n). Space: O(n).
     * Invariant: bound is the least start allowed for the next kept interval of a largest kept set.
     */
    static int removals(int[][] intervals, long gap) {
        int[][] byEnd = intervals.clone();
        Arrays.sort(byEnd, (a, b) -> Integer.compare(a[1], b[1]));    // earliest end first
        int kept = 0;
        long bound = Long.MIN_VALUE;                                   // below every start
        for (int[] m : byEnd) {                                        // one test per interval
            if (m[0] >= bound) {                                       // the gap rule allows this interval
                kept++;
                bound = (long) m[1] + gap;                             // widened sum: no int overflow
            }
        }
        return intervals.length - kept;
    }

    static int brute(int[][] m, long gap) {
        int best = 0;
        for (int mask = 0; mask < (1 << m.length); mask++) {
            List<int[]> pick = new ArrayList<>();
            for (int k = 0; k < m.length; k++) if ((mask >> k & 1) != 0) pick.add(m[k]);
            pick.sort((a, b) -> Integer.compare(a[1], b[1]));
            boolean ok = true;
            for (int k = 1; k < pick.size(); k++) {
                for (int j = 0; j < k; j++) {                          // every pair must be separated by the gap
                    boolean apart = pick.get(k)[0] >= pick.get(j)[1] + gap || pick.get(j)[0] >= pick.get(k)[1] + gap;
                    if (!apart) ok = false;
                }
            }
            if (ok) best = Math.max(best, pick.size());
        }
        return m.length - best;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (removals(new int[][] {{1, 3}, {2, 4}, {4, 6}, {5, 8}, {7, 9}}, 1) != 2) throw new AssertionError("ex1");
        if (removals(new int[][] {{1, 3}, {3, 5}, {5, 7}}, 1) != 1) throw new AssertionError("ex2");
        // Large ends plus a large gap pass the int range and stay correct.
        if (removals(new int[][] {{0, Integer.MAX_VALUE}, {Integer.MAX_VALUE - 1, Integer.MAX_VALUE}}, 1_000_000_000) != 1) throw new AssertionError("overflow");
        if (removals(new int[0][], 5) != 0) throw new AssertionError("empty");
        // Random inputs must match exhaustive search with a pairwise gap test.
        Random rnd = new Random(2092);
        for (int t = 0; t < 500; t++) {
            int[][] m = new int[rnd.nextInt(8)][];
            for (int k = 0; k < m.length; k++) { int s = rnd.nextInt(12); m[k] = new int[] {s, s + 1 + rnd.nextInt(4)}; }
            int gap = rnd.nextInt(3);
            if (removals(m, gap) != brute(m, gap)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Boundary] Minimum Number of Arrows to Burst Balloons (LeetCode 452)
<!-- id: gr-half-open-balloons -->

**Approach.**
The method sorts the balloons by end. The first arrow of a group goes at the last integer inside the first balloon, which is `end - 1`. That arrow bursts a later balloon exactly when the later start is at most `end - 1`, so a balloon that begins at the end of the first one needs a new arrow. The method keeps the arrow coordinate as a `long`, so every comparison with a start uses one wide type. An arrow at the last point of the earliest-ending balloon reaches every later balloon that any earlier arrow could reach.

After each balloon, `arrow` is the coordinate of the current group's arrow, and `arrows` counts the groups opened so far.

**Complexity.**
- **Time** is O(n log n), because sorting the ends dominates the scan.
- **Space** is O(n) for the sorted copy.

```java run
import java.util.*;

public final class HalfOpenBalloons {
    /**
     * Returns the fewest arrows for half-open integer balloons.
     * Time: O(n log n). Space: O(n).
     * Invariant: arrow is the last integer of the earliest-ending balloon in the current group.
     */
    static int arrows(int[][] balloons) {
        int[][] byEnd = balloons.clone();
        Arrays.sort(byEnd, (a, b) -> Integer.compare(a[1], b[1]));    // earliest end first, no subtraction
        int count = 0;
        long arrow = Long.MIN_VALUE;
        for (int[] b : byEnd) {                                        // one test per balloon
            if (count == 0 || b[0] > arrow) {                          // start passes the arrow: a new group
                count++;
                arrow = (long) b[1] - 1;                               // last integer inside the half-open range
            }
        }
        return count;
    }

    static int brute(int[][] b) {
        if (b.length == 0) return 0;
        int lo = Integer.MAX_VALUE, hi = Integer.MIN_VALUE;
        for (int[] x : b) { lo = Math.min(lo, x[0]); hi = Math.max(hi, x[1]); }
        List<Integer> pts = new ArrayList<>();
        for (int x = lo; x < hi; x++) pts.add(x);                      // every integer coordinate
        int best = Integer.MAX_VALUE;
        for (int mask = 0; mask < (1 << pts.size()); mask++) {
            boolean all = true;
            for (int[] x : b) {
                boolean hit = false;
                for (int k = 0; k < pts.size(); k++) if ((mask >> k & 1) != 0 && x[0] <= pts.get(k) && pts.get(k) < x[1]) hit = true;
                if (!hit) { all = false; break; }
            }
            if (all) best = Math.min(best, Integer.bitCount(mask));
        }
        return best;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (arrows(new int[][] {{1, 3}, {3, 5}, {2, 4}}) != 2) throw new AssertionError("ex1");
        if (arrows(new int[][] {{1, 4}, {2, 5}, {3, 6}}) != 1) throw new AssertionError("ex2");
        // Extreme coordinates and empty input.
        if (arrows(new int[][] {{Integer.MIN_VALUE, Integer.MIN_VALUE + 1}, {Integer.MAX_VALUE - 1, Integer.MAX_VALUE}}) != 2) throw new AssertionError("extreme");
        if (arrows(new int[0][]) != 0) throw new AssertionError("empty");
        // Random inputs must match an exhaustive search over integer arrow positions.
        Random rnd = new Random(2093);
        for (int t = 0; t < 400; t++) {
            int[][] b = new int[rnd.nextInt(6)][];
            for (int k = 0; k < b.length; k++) { int s = rnd.nextInt(8); b[k] = new int[] {s, s + 1 + rnd.nextInt(4)}; }
            if (arrows(b) != brute(b)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Recognize] Partition Labels (LeetCode 763)
<!-- id: gr-partition-labels -->

**Approach.**
The method records the last index of every letter in one pass. A second pass keeps `end`, the largest last index among the letters read since the current part began. A part may close at position `i` exactly when `i == end`, because then every letter inside the part has its last occurrence inside the part. The method closes the part at the first such position. An optimal cut cannot lie later than the first legal position without losing a part, and cutting at the first legal position still leaves a legal remainder, so the number of parts is the largest possible.

After each position, the closed parts are legal, and `end` covers every letter of the open part.

**Complexity.**
- **Time** is O(n) for two passes over the string.
- **Space** is O(1) for the array of 26 entries, plus the output list.

```java run
import java.util.*;

public final class PartitionLabels {
    /**
     * Returns the lengths of the parts of a cut with the most parts.
     * Time: O(n). Space: O(1) plus output.
     * Invariant: end is the largest last index of the letters in the open part, and closed parts share no letter.
     */
    static List<Integer> partition(String s) {
        int[] last = new int[26];
        for (int i = 0; i < s.length(); i++) last[s.charAt(i) - 'a'] = i;   // final write wins
        List<Integer> parts = new ArrayList<>();
        int start = 0, end = 0;
        for (int i = 0; i < s.length(); i++) {                         // one pass
            end = Math.max(end, last[s.charAt(i) - 'a']);               // the part must reach the last copy
            if (i == end) {                                             // every letter in the part ends here
                parts.add(i - start + 1);
                start = i + 1;
            }
        }
        return parts;
    }

    static int brute(String s) {
        int n = s.length(), best = 0;
        for (int mask = 0; mask < (1 << Math.max(0, n - 1)); mask++) {  // every set of cut positions
            int[] owner = new int[26];
            Arrays.fill(owner, -1);
            int chunk = 0;
            boolean legal = true;
            for (int i = 0; i < n && legal; i++) {
                int c = s.charAt(i) - 'a';
                if (owner[c] != -1 && owner[c] != chunk) legal = false;
                owner[c] = chunk;
                if (i < n - 1 && (mask >> i & 1) != 0) chunk++;
            }
            if (legal && n > 0) best = Math.max(best, chunk + 1);
        }
        return best;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!partition("abacbdeffed").equals(List.of(5, 6))) throw new AssertionError("ex1");
        if (!partition("aabbcc").equals(List.of(2, 2, 2))) throw new AssertionError("ex2");
        if (!partition("").isEmpty() || !partition("a").equals(List.of(1))) throw new AssertionError("small");
        // Random strings: the part count must be the maximum, and the sizes must sum to the length.
        Random rnd = new Random(2094);
        for (int t = 0; t < 500; t++) {
            StringBuilder sb = new StringBuilder();
            for (int k = rnd.nextInt(10); k > 0; k--) sb.append((char) ('a' + rnd.nextInt(4)));
            String s = sb.toString();
            List<Integer> p = partition(s);
            int sum = 0;
            for (int x : p) sum += x;
            if (sum != s.length() || p.size() != brute(s)) throw new AssertionError("random " + t);
        }
    }
}
```
