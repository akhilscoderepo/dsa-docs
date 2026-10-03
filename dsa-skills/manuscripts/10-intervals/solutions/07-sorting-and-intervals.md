<!-- solutions-for: 07-sorting-and-intervals -->
### Sorting And Intervals

#### Solution: [Build] Merge With Counts (LeetCode 56)
<!-- id: iv-sorting-merge-counts -->

**Approach.** Sort a copy by start. Keep the open block as a triple of start, furthest end and count. A session whose start is at most the block's end belongs to the block, so the block keeps whichever end reaches further and the count grows by one. Any other session opens a new block with count one. The closed contract is why equality joins a block. The assertions compare against a coverage oracle that doubles every coordinate, so that touching closed intervals share a cell and separated ones leave a gap, then count the originals lying inside each oracle block.

**Complexity.** O(n log n) time and O(n) space.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

public final class MergeWithCounts {
    static int[][] merge(int[][] sessions) {
        int[][] sorted = new int[sessions.length][];
        for (int i = 0; i < sorted.length; i++) sorted[i] = sessions[i].clone();
        Arrays.sort(sorted, (a, b) -> Integer.compare(a[0], b[0]));
        List<int[]> blocks = new ArrayList<>();
        for (int[] s : sorted) {
            int[] last = blocks.isEmpty() ? null : blocks.get(blocks.size() - 1);
            if (last != null && s[0] <= last[1]) { last[1] = Math.max(last[1], s[1]); last[2]++; }
            else blocks.add(new int[] {s[0], s[1], 1});
        }
        return blocks.toArray(new int[0][]);
    }
    static int[][] oracle(int[][] iv) {
        boolean[] cover = new boolean[100];
        for (int[] r : iv) for (int v = 2 * r[0]; v <= 2 * r[1]; v++) cover[v] = true;
        List<int[]> out = new ArrayList<>();
        int v = 0;
        while (v < cover.length) {
            if (!cover[v]) { v++; continue; }
            int s = v;
            while (v + 1 < cover.length && cover[v + 1]) v++;
            int count = 0;
            for (int[] r : iv) if (2 * r[0] >= s && 2 * r[1] <= v) count++;
            out.add(new int[] {s / 2, v / 2, count});
            v++;
        }
        return out.toArray(new int[0][]);
    }

    public static void main(String[] args) {
        if (!Arrays.deepEquals(merge(new int[][] {{15, 18}, {1, 3}, {8, 10}, {2, 6}}), new int[][] {{1, 6, 2}, {8, 10, 1}, {15, 18, 1}})) throw new AssertionError("example 1");
        if (!Arrays.deepEquals(merge(new int[][] {{4, 5}, {1, 4}}), new int[][] {{1, 5, 2}})) throw new AssertionError("example 2");
        int[][] original = {{9, 10}, {1, 2}};
        merge(original);
        if (original[0][0] != 9) throw new AssertionError("the input order survives");
        Random rnd = new Random(10701);
        for (int t = 0; t < 5000; t++) {
            int n = 1 + rnd.nextInt(8);
            int[][] a = new int[n][2];
            for (int i = 0; i < n; i++) { a[i][0] = rnd.nextInt(20); a[i][1] = a[i][0] + rnd.nextInt(6); }
            if (!Arrays.deepEquals(merge(a), oracle(a))) throw new AssertionError("differs on " + Arrays.deepToString(a));
        }
    }
}
```

#### Solution: [Vary] Insert Position And Absorbed Count (LeetCode 57)
<!-- id: iv-sorting-insert-position -->

**Approach.** The list is already sorted and disjoint, so one pass counts three regions without any sort. List intervals that end at or before the new start lie entirely before it, and their number is the position. The next intervals, while they start strictly before the new end, share a point with it under the half-open contract and are absorbed. The rest lie after. A touching list interval ends exactly at the new start, or starts exactly at the new end, and falls in a free region. The assertions compare with an oracle that expands every interval into its integer cells, absorbs those that share a cell, rebuilds the result list and finds where the grown interval sits in it.

**Complexity.** O(n) time and O(1) extra space.

```java run
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public final class InsertPosition {
    static int[] insert(int[][] list, int[] extra) {
        int i = 0;
        while (i < list.length && list[i][1] <= extra[0]) i++;
        int position = i, absorbed = 0;
        while (i < list.length && list[i][0] < extra[1]) { absorbed++; i++; }
        return new int[] {position, absorbed};
    }
    static int[] oracle(int[][] list, int[] extra) {
        int lo = extra[0], hi = extra[1];
        int absorbed = 0;
        for (int[] r : list) {
            boolean shares = false;
            for (int c = r[0]; c < r[1]; c++) if (c >= extra[0] && c < extra[1]) shares = true;
            if (shares) { absorbed++; lo = Math.min(lo, r[0]); hi = Math.max(hi, r[1]); }
        }
        List<int[]> result = new ArrayList<>();
        boolean placed = false;
        int position = -1;
        for (int[] r : list) {
            boolean shares = false;
            for (int c = r[0]; c < r[1]; c++) if (c >= extra[0] && c < extra[1]) shares = true;
            if (shares) continue;
            if (!placed && r[0] >= hi) { position = result.size(); result.add(new int[] {lo, hi}); placed = true; }
            result.add(r);
        }
        if (!placed) position = result.size();
        return new int[] {position, absorbed};
    }

    public static void main(String[] args) {
        int[] e1 = insert(new int[][] {{1, 3}, {6, 9}}, new int[] {2, 5});
        if (e1[0] != 0 || e1[1] != 1) throw new AssertionError("example 1");
        int[] e2 = insert(new int[][] {{1, 2}, {3, 4}}, new int[] {2, 3});
        if (e2[0] != 1 || e2[1] != 0) throw new AssertionError("example 2");
        int[] e3 = insert(new int[0][], new int[] {2, 3});
        if (e3[0] != 0 || e3[1] != 0) throw new AssertionError("empty list");
        Random rnd = new Random(10702);
        for (int t = 0; t < 6000; t++) {
            int n = rnd.nextInt(7);
            int[][] list = new int[n][2];
            int cur = rnd.nextInt(3);
            for (int i = 0; i < n; i++) {
                list[i][0] = cur;
                list[i][1] = cur + 1 + rnd.nextInt(4);
                cur = list[i][1] + rnd.nextInt(3);
            }
            int s = rnd.nextInt(25);
            int[] extra = {s, s + 1 + rnd.nextInt(8)};
            int[] got = insert(list, extra), want = oracle(list, extra);
            if (got[0] != want[0] || got[1] != want[1]) throw new AssertionError("differs: got " + got[0] + "," + got[1] + " want " + want[0] + "," + want[1]);
        }
    }
}
```

#### Solution: [Boundary] Kept Indices With A Tie Rule (LeetCode 435)
<!-- id: iv-sorting-kept-indices -->

**Approach.** Sort an array of indices, not copies of the intervals, by end and then by the smaller index, so equal ends have a fixed winner. Keep an index when its start is at or after the last kept end, then sort the kept indices ascending for the report. The comparator uses `Integer.compare` on both keys. The assertions check the stated rule against a selection loop that repeatedly picks the lowest-ending unprocessed interval, check that the kept set is conflict-free, and compare its size with an exhaustive search over all subsets.

**Complexity.** O(n log n) time and O(n) space for the index array.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.Random;

public final class KeptIndices {
    static int[] kept(int[][] iv) {
        Integer[] order = new Integer[iv.length];
        for (int i = 0; i < order.length; i++) order[i] = i;
        Arrays.sort(order, (x, y) -> iv[x][1] != iv[y][1] ? Integer.compare(iv[x][1], iv[y][1]) : Integer.compare(x, y));
        List<Integer> keep = new ArrayList<>();
        long lastEnd = Long.MIN_VALUE;
        for (int idx : order) if (iv[idx][0] >= lastEnd) { keep.add(idx); lastEnd = iv[idx][1]; }
        Collections.sort(keep);
        return keep.stream().mapToInt(Integer::intValue).toArray();
    }
    static int[] selectionLoop(int[][] iv) {
        boolean[] used = new boolean[iv.length];
        List<Integer> keep = new ArrayList<>();
        long lastEnd = Long.MIN_VALUE;
        for (int round = 0; round < iv.length; round++) {
            int pick = -1;
            for (int i = 0; i < iv.length; i++) {
                if (used[i]) continue;
                if (pick < 0 || iv[i][1] < iv[pick][1]) pick = i;
            }
            used[pick] = true;
            if (iv[pick][0] >= lastEnd) { keep.add(pick); lastEnd = iv[pick][1]; }
        }
        Collections.sort(keep);
        return keep.stream().mapToInt(Integer::intValue).toArray();
    }
    static int bestSize(int[][] iv) {
        int n = iv.length, best = 0;
        for (int mask = 0; mask < (1 << n); mask++) {
            boolean ok = true;
            for (int a = 0; a < n && ok; a++) {
                if ((mask >> a & 1) == 0) continue;
                for (int b = a + 1; b < n && ok; b++) {
                    if ((mask >> b & 1) == 0) continue;
                    if (iv[a][0] < iv[b][1] && iv[b][0] < iv[a][1]) ok = false;
                }
            }
            if (ok) best = Math.max(best, Integer.bitCount(mask));
        }
        return best;
    }

    public static void main(String[] args) {
        if (!Arrays.equals(kept(new int[][] {{2, 5}, {0, 3}, {3, 6}, {1, 4}, {6, 9}}), new int[] {1, 2, 4})) throw new AssertionError("example 1");
        if (!Arrays.equals(kept(new int[][] {{1, 2}, {1, 2}}), new int[] {0})) throw new AssertionError("example 2");
        Random rnd = new Random(10703);
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(8);
            int[][] a = new int[n][2];
            for (int i = 0; i < n; i++) { a[i][0] = rnd.nextInt(10); a[i][1] = a[i][0] + 1 + rnd.nextInt(5); }
            int[] got = kept(a);
            if (!Arrays.equals(got, selectionLoop(a))) throw new AssertionError("tie rule differs on " + Arrays.deepToString(a));
            for (int x = 0; x < got.length; x++) for (int y = x + 1; y < got.length; y++)
                if (a[got[x]][0] < a[got[y]][1] && a[got[y]][0] < a[got[x]][1]) throw new AssertionError("kept set clashes");
            if (got.length != bestSize(a)) throw new AssertionError("kept set is not maximum on " + Arrays.deepToString(a));
        }
    }
}
```

#### Solution: [Recognize] Announcement Coordinates (LeetCode 452)
<!-- id: iv-sorting-arrow-positions -->

**Approach.** Sort a copy by end. The first session gets an announcement at its own end, which is the furthest right coordinate that still reaches it. Every later session whose start is not past that coordinate has already heard it, because the spans are closed. The first session starting strictly after it needs a new announcement at its own end, and the coordinate is added to the answer list. The assertions check three things on random inputs: every session contains some reported coordinate, the count equals the exhaustive minimum over subsets of end coordinates, and the list is strictly increasing.

**Complexity.** O(n log n) time and O(n) space.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

public final class AnnouncementCoordinates {
    static int[] announce(int[][] points) {
        int[][] sorted = new int[points.length][];
        for (int i = 0; i < sorted.length; i++) sorted[i] = points[i].clone();
        Arrays.sort(sorted, (a, b) -> Integer.compare(a[1], b[1]));
        List<Integer> shots = new ArrayList<>();
        long shot = Long.MIN_VALUE;
        for (int[] s : sorted) if (shots.isEmpty() || s[0] > shot) { shot = s[1]; shots.add(s[1]); }
        return shots.stream().mapToInt(Integer::intValue).toArray();
    }
    static int minimum(int[][] pts) {
        int n = pts.length;
        for (int k = 1; k <= n; k++) {
            for (int mask = 0; mask < (1 << n); mask++) {
                if (Integer.bitCount(mask) != k) continue;
                boolean all = true;
                for (int[] p : pts) {
                    boolean hit = false;
                    for (int c = 0; c < n; c++) if ((mask >> c & 1) == 1 && p[0] <= pts[c][1] && pts[c][1] <= p[1]) hit = true;
                    if (!hit) { all = false; break; }
                }
                if (all) return k;
            }
        }
        return n;
    }

    public static void main(String[] args) {
        if (!Arrays.equals(announce(new int[][] {{4, 12}, {1, 5}, {6, 8}, {2, 4}, {9, 14}}), new int[] {4, 8, 14})) throw new AssertionError("example 1");
        if (!Arrays.equals(announce(new int[][] {{1, 1}}), new int[] {1})) throw new AssertionError("example 2");
        if (announce(new int[][] {{Integer.MIN_VALUE, Integer.MAX_VALUE}, {Integer.MAX_VALUE, Integer.MAX_VALUE}}).length != 1) throw new AssertionError("extreme closed spans");
        Random rnd = new Random(10704);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(7);
            int[][] a = new int[n][2];
            for (int i = 0; i < n; i++) { a[i][0] = rnd.nextInt(10); a[i][1] = a[i][0] + rnd.nextInt(5); }
            int[] got = announce(a);
            for (int[] p : a) {
                boolean hit = false;
                for (int c : got) if (p[0] <= c && c <= p[1]) hit = true;
                if (!hit) throw new AssertionError("a session heard nothing: " + Arrays.deepToString(a));
            }
            for (int i = 1; i < got.length; i++) if (got[i] <= got[i - 1]) throw new AssertionError("not increasing");
            if (got.length != minimum(a)) throw new AssertionError("not minimal on " + Arrays.deepToString(a));
        }
    }
}
```
