<!-- solutions-for: 20-greedy -->
### Greedy And Ordering

#### Solution: [Build] Assign Cookies (LeetCode 455)
<!-- id: gc-cookie-owners -->

**Approach.** Sort the child indexes by greed and the cookie indexes by size, in both cases with the lower index first on a tie. Walk the cookies in order with a cursor `k` over the children. A cookie that is at least as large as the greed of the child at `k` goes to that child and the cursor advances, and a smaller cookie cannot satisfy that child or any later one, so it stays unused. The assertions check both examples. Random small cases are compared with an exhaustive matching for the number served, and also checked for legality, for serving exactly the least greedy children, and for giving the cookies to those children in increasing order.

**Complexity.** The two sorts cost O(n log n + m log m) and the walk takes m steps.

```java run
import java.util.Arrays;
import java.util.Random;

public final class CookieOwners {
    static int[] owners(int[] greed, int[] sizes) {
        Integer[] kids = new Integer[greed.length], cookies = new Integer[sizes.length];
        for (int i = 0; i < kids.length; i++) kids[i] = i;
        for (int i = 0; i < cookies.length; i++) cookies[i] = i;
        Arrays.sort(kids, (a, b) -> greed[a] != greed[b] ? Integer.compare(greed[a], greed[b]) : Integer.compare(a, b));
        Arrays.sort(cookies, (a, b) -> sizes[a] != sizes[b] ? Integer.compare(sizes[a], sizes[b]) : Integer.compare(a, b));
        int[] owner = new int[sizes.length];
        Arrays.fill(owner, -1);
        int k = 0;
        for (int c : cookies) {
            if (k < kids.length && sizes[c] >= greed[kids[k]]) owner[c] = kids[k++];
        }
        return owner;
    }

    static int oracle(int[] g, int[] s, int idx, boolean[] taken) {
        if (idx == g.length) return 0;
        int best = oracle(g, s, idx + 1, taken);
        for (int c = 0; c < s.length; c++) {
            if (!taken[c] && s[c] >= g[idx]) {
                taken[c] = true;
                best = Math.max(best, 1 + oracle(g, s, idx + 1, taken));
                taken[c] = false;
            }
        }
        return best;
    }

    public static void main(String[] args) {
        if (!Arrays.equals(owners(new int[]{7, 2, 5}, new int[]{5, 1, 3, 9}), new int[]{2, -1, 1, 0})) throw new AssertionError("example 1");
        if (!Arrays.equals(owners(new int[]{2, 2}, new int[]{2, 2, 2}), new int[]{0, 1, -1})) throw new AssertionError("example 2");
        if (owners(new int[0], new int[]{4, 4}).length != 2 || owners(new int[0], new int[]{4, 4})[0] != -1) throw new AssertionError("no children");
        if (owners(new int[]{3}, new int[0]).length != 0) throw new AssertionError("no cookies");
        if (owners(new int[]{Integer.MAX_VALUE}, new int[]{Integer.MAX_VALUE})[0] != 0) throw new AssertionError("values at the int limit");

        Random rnd = new Random(2601);
        for (int t = 0; t < 5000; t++) {
            int n = rnd.nextInt(7), m = rnd.nextInt(7);
            int[] g = new int[n], s = new int[m];
            for (int i = 0; i < n; i++) g[i] = 1 + rnd.nextInt(6);
            for (int i = 0; i < m; i++) s[i] = 1 + rnd.nextInt(6);
            int[] own = owners(g, s);
            boolean[] served = new boolean[n];
            int count = 0, lastChild = -1;
            Integer[] byCookie = new Integer[m];
            for (int i = 0; i < m; i++) byCookie[i] = i;
            Arrays.sort(byCookie, (a, b) -> s[a] != s[b] ? Integer.compare(s[a], s[b]) : Integer.compare(a, b));
            int prevRankGreed = -1, prevRankIdx = -1;
            for (int c : byCookie) {
                if (own[c] == -1) continue;
                int child = own[c];
                if (served[child] || s[c] < g[child]) throw new AssertionError("illegal match");
                served[child] = true;
                count++;
                if (g[child] < prevRankGreed || (g[child] == prevRankGreed && child < prevRankIdx)) throw new AssertionError("children must be served in greed order");
                prevRankGreed = g[child]; prevRankIdx = child;
            }
            if (count != oracle(g, s, 0, new boolean[m])) throw new AssertionError("not the maximum number served");
            int maxServedGreed = -1;
            for (int i = 0; i < n; i++) if (served[i]) maxServedGreed = Math.max(maxServedGreed, g[i]);
            for (int i = 0; i < n; i++) if (!served[i] && g[i] < maxServedGreed) throw new AssertionError("a less greedy child was skipped");
        }
    }
}
```

#### Solution: [Vary] Non-overlapping Intervals (LeetCode 435)
<!-- id: gc-removals-and-boundary -->

**Approach.** Sort a copy by end and sweep with a boundary that starts at -1, which is below every legal start. A span whose start is at or after the boundary is kept and moves the boundary to its end, and the removed count is the total minus the kept count. The final boundary is the end of the last kept span. The assertions check both examples and the empty input. Random small calendars are compared with an enumeration of every conflict-free subset, which gives the largest size and, among the subsets of that size, the smallest possible end of the last span. That second comparison confirms that the greedy plan stays ahead.

**Complexity.** One sort and one sweep give O(n log n) time, and the clone holds n row references.

```java run
import java.util.Arrays;
import java.util.Random;

public final class RemovalsAndBoundary {
    static long[] removalsAndBoundary(int[][] acts) {
        int[][] s = acts.clone();
        Arrays.sort(s, (a, b) -> Integer.compare(a[1], b[1]));
        int kept = 0;
        long boundary = -1;
        for (int[] r : s) if (r[0] >= boundary) { kept++; boundary = r[1]; }
        return new long[]{acts.length - kept, boundary};
    }

    static long[] oracle(int[][] a) {
        int n = a.length, bestSize = 0;
        long bestEnd = -1;
        for (int mask = 0; mask < (1 << n); mask++) {
            boolean ok = true;
            long lastEnd = -1;
            for (int i = 0; i < n && ok; i++) {
                if ((mask >> i & 1) == 0) continue;
                lastEnd = Math.max(lastEnd, a[i][1]);
                for (int j = i + 1; j < n && ok; j++)
                    if ((mask >> j & 1) == 1 && a[i][0] < a[j][1] && a[j][0] < a[i][1]) ok = false;
            }
            if (!ok) continue;
            int size = Integer.bitCount(mask);
            if (size > bestSize || (size == bestSize && lastEnd < bestEnd)) { bestSize = size; bestEnd = lastEnd; }
        }
        return new long[]{n - bestSize, bestSize == 0 ? -1 : bestEnd};
    }

    public static void main(String[] args) {
        if (!Arrays.equals(removalsAndBoundary(new int[][]{{1, 4}, {2, 3}, {3, 6}, {5, 7}, {4, 5}}), new long[]{2, 7})) throw new AssertionError("example 1");
        if (!Arrays.equals(removalsAndBoundary(new int[][]{{0, 5}, {0, 5}, {5, 10}}), new long[]{1, 10})) throw new AssertionError("example 2");
        if (!Arrays.equals(removalsAndBoundary(new int[0][]), new long[]{0, -1})) throw new AssertionError("empty input");
        if (!Arrays.equals(removalsAndBoundary(new int[][]{{0, 1}}), new long[]{0, 1})) throw new AssertionError("a single span starting at zero is kept");

        Random rnd = new Random(2602);
        for (int t = 0; t < 4000; t++) {
            int n = rnd.nextInt(9);
            int[][] a = new int[n][];
            for (int i = 0; i < n; i++) {
                int s = rnd.nextInt(10);
                a[i] = new int[]{s, s + 1 + rnd.nextInt(5)};
            }
            if (!Arrays.equals(removalsAndBoundary(a), oracle(a))) throw new AssertionError("disagrees with the subset search on " + Arrays.deepToString(a));
        }
    }
}
```

#### Solution: [Boundary] Minimum Number of Arrows to Burst Balloons (LeetCode 452)
<!-- id: gc-launch-points -->

**Approach.** Convert each balloon to the span from `c - r` to `c + r` in `long`, sort by the upper end, and sweep. A balloon whose lower end is strictly greater than the current shot position needs a new shot, placed at that balloon's upper end, which is the earliest end of the group it begins. A balloon whose lower end equals the shot position is already burst, because the spans are closed. The assertions check both examples, show that the same sum in `int` wraps to -2, and then compare random cases, including extreme centres and radii, with a search over every set of candidate points taken from the span ends. The returned shots are also checked to burst every balloon.

**Complexity.** The sort dominates at O(n log n), and the sweep is linear.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

public final class LaunchPoints {
    static List<Long> shots(long[][] balloons) {
        long[][] w = new long[balloons.length][];
        for (int i = 0; i < w.length; i++) w[i] = new long[]{balloons[i][0] - balloons[i][1], balloons[i][0] + balloons[i][1]};
        Arrays.sort(w, (a, b) -> Long.compare(a[1], b[1]));
        List<Long> out = new ArrayList<>();
        for (long[] x : w) if (out.isEmpty() || x[0] > out.get(out.size() - 1)) out.add(x[1]);
        return out;
    }

    static long[] summary(long[][] balloons) {
        List<Long> s = shots(balloons);
        return new long[]{s.size(), s.isEmpty() ? 0 : s.get(s.size() - 1)};
    }

    static int oracle(long[][] b) {
        int n = b.length;
        if (n == 0) return 0;
        long[] cand = new long[n];
        for (int i = 0; i < n; i++) cand[i] = b[i][0] + b[i][1];
        int best = n;
        for (int mask = 1; mask < (1 << n); mask++) {
            boolean all = true;
            for (int k = 0; k < n && all; k++) {
                boolean hit = false;
                for (int c = 0; c < n && !hit; c++)
                    if ((mask >> c & 1) == 1 && b[k][0] - b[k][1] <= cand[c] && cand[c] <= b[k][0] + b[k][1]) hit = true;
                all = hit;
            }
            if (all) best = Math.min(best, Integer.bitCount(mask));
        }
        return best;
    }

    public static void main(String[] args) {
        if (!Arrays.equals(summary(new long[][]{{5, 3}, {1, 1}, {9, 2}, {12, 0}}), new long[]{3, 12})) throw new AssertionError("example 1");
        if (!Arrays.equals(summary(new long[][]{{2147483647L, 2147483647L}, {0, 0}}), new long[]{1, 0})) throw new AssertionError("example 2");
        int wrapped = 2147483647 + 2147483647;
        if (wrapped != -2) throw new AssertionError("the int sum must wrap to -2");
        if (!Arrays.equals(summary(new long[0][]), new long[]{0, 0})) throw new AssertionError("no balloons");
        if (shots(new long[][]{{3, 0}, {3, 0}}).size() != 1) throw new AssertionError("two point balloons at the same place share a shot");
        if (shots(new long[][]{{0, 2}, {4, 2}}).size() != 1) throw new AssertionError("spans touching at a point share a shot");

        long[] pool = {-2147483648L, -4, -1, 0, 1, 3, 2147483647L};
        long[] radii = {0, 0, 1, 2, 3, 2147483647L};
        Random rnd = new Random(2603);
        for (int t = 0; t < 5000; t++) {
            int n = rnd.nextInt(8);
            long[][] b = new long[n][];
            for (int i = 0; i < n; i++) {
                if (rnd.nextInt(3) == 0) b[i] = new long[]{pool[rnd.nextInt(pool.length)], radii[rnd.nextInt(radii.length)]};
                else b[i] = new long[]{rnd.nextInt(9) - 4, rnd.nextInt(4)};
            }
            List<Long> s = shots(b);
            if (s.size() != oracle(b)) throw new AssertionError("not the fewest shots on " + Arrays.deepToString(b));
            for (long[] x : b) {
                boolean hit = false;
                for (long p : s) if (x[0] - x[1] <= p && p <= x[0] + x[1]) hit = true;
                if (!hit) throw new AssertionError("a balloon was missed");
            }
        }
    }
}
```

#### Solution: [Recognize] Partition Labels (LeetCode 763)
<!-- id: gc-section-sizes -->

**Approach.** Record the last position of every letter. Scan with a `start` and an `end`, where `end` is the farthest last position among the letters seen since `start`. When the index reaches `end`, every letter inside the piece has its last occurrence inside the piece, so the piece closes and the next one starts after it. Closing at the first such moment is the earliest legal cut. The oracle computes every legal cut position independently, by checking that the letters before the cut and the letters after it are disjoint, and cuts at all of them. The assertions check both examples, the empty string, and agreement with an exhaustive search over all cut sets on random short strings.

**Complexity.** Two passes over the text and a 26-entry table give O(n) time and O(1) extra memory beyond the output.

```java run
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public final class SectionSizes {
    static List<Integer> sectionSizes(String s) {
        int[] last = new int[26];
        for (int i = 0; i < s.length(); i++) last[s.charAt(i) - 'a'] = i;
        List<Integer> out = new ArrayList<>();
        int start = 0, end = 0;
        for (int i = 0; i < s.length(); i++) {
            end = Math.max(end, last[s.charAt(i) - 'a']);
            if (i == end) { out.add(i - start + 1); start = i + 1; }
        }
        return out;
    }

    static boolean disjoint(String left, String right) {
        for (char c : left.toCharArray()) if (right.indexOf(c) >= 0) return false;
        return true;
    }

    static List<Integer> finest(String s) {
        List<Integer> out = new ArrayList<>();
        int start = 0;
        for (int p = 0; p < s.length(); p++) {
            if (p == s.length() - 1 || disjoint(s.substring(0, p + 1), s.substring(p + 1))) { out.add(p - start + 1); start = p + 1; }
        }
        return out;
    }

    static int bestByCuts(String s) {
        int n = s.length(), best = 1;
        if (n == 0) return 0;
        for (int mask = 0; mask < (1 << Math.max(0, n - 1)); mask++) {
            boolean ok = true;
            int[] piece = new int[26];
            java.util.Arrays.fill(piece, -1);
            int id = 0;
            for (int i = 0; i < n && ok; i++) {
                int c = s.charAt(i) - 'a';
                if (piece[c] != -1 && piece[c] != id) ok = false;
                piece[c] = id;
                if (i < n - 1 && (mask >> i & 1) == 1) id++;
            }
            if (ok) best = Math.max(best, Integer.bitCount(mask) + 1);
        }
        return best;
    }

    public static void main(String[] args) {
        if (!sectionSizes("xyxzzwvwvu").equals(List.of(3, 2, 4, 1))) throw new AssertionError("example 1");
        if (!sectionSizes("mnopqmrst").equals(List.of(6, 1, 1, 1))) throw new AssertionError("example 2");
        if (!sectionSizes("").isEmpty()) throw new AssertionError("empty string");
        if (!sectionSizes("aaaa").equals(List.of(4))) throw new AssertionError("one repeated letter is one piece");
        if (!sectionSizes("abcabc").equals(List.of(6))) throw new AssertionError("interleaved letters cannot be cut");

        Random rnd = new Random(2604);
        for (int t = 0; t < 4000; t++) {
            int n = rnd.nextInt(11);
            StringBuilder sb = new StringBuilder();
            int alpha = 1 + rnd.nextInt(5);
            for (int i = 0; i < n; i++) sb.append((char) ('a' + rnd.nextInt(alpha)));
            String s = sb.toString();
            List<Integer> got = sectionSizes(s);
            if (!got.equals(finest(s))) throw new AssertionError("differs from the independent cuts on " + s);
            if (got.size() != bestByCuts(s)) throw new AssertionError("not the most pieces on " + s);
            int sum = 0;
            for (int v : got) sum += v;
            if (sum != n) throw new AssertionError("pieces must cover the string");
        }
    }
}
```
