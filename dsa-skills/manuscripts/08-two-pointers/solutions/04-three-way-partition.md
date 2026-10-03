<!-- solutions-for: 08-three-way-partition -->
### Three-Way Partition

#### Solution: [Build] Partition 0,1,2 (Author exercise)
<!-- id: tp-flag-012 -->

**Approach.** Three markers cut the array into four regions: zeros before `zeroEnd`, ones from `zeroEnd` to before `scan`, an unscanned stretch from `scan` to `twoStart - 1`, and twos from `twoStart` on. Each step reads the value under `scan`. A zero trades with the value at `zeroEnd` and both `zeroEnd` and `scan` advance. A one only advances `scan`. A two trades with the value at `twoStart - 1`, the end of the unscanned stretch, and the end retreats while `scan` stays. When the loop ends the answer is the pair `zeroEnd` and `scan`, which are the start of the ones and the start of the twos. The check confirms both examples, compares the final array and both boundaries with a counting oracle on random arrays, counts the iterations to confirm there are at most n of them, and runs the same loop on tagged objects to show that objects carrying a category keep their identity, which a counting rewrite would lose.

**Complexity.** Linear time, since each iteration advances `scan` or retreats the end, and constant extra memory.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

public final class FlagZeroOneTwo {
    static int iterations;

    static int[] flag(int[] a) {
        int zeroEnd = 0, scan = 0, twoStart = a.length;
        iterations = 0;
        while (scan < twoStart) {
            iterations++;
            int v = a[scan];
            if (v == 0) {
                a[scan] = a[zeroEnd];
                a[zeroEnd] = 0;
                zeroEnd++;
                scan++;
            } else if (v == 1) {
                scan++;
            } else {
                twoStart--;
                a[scan] = a[twoStart];
                a[twoStart] = 2;
            }
        }
        return new int[] {zeroEnd, scan};
    }

    record Towel(int code, String id) {}

    static void flagTowels(List<Towel> rail) {
        int low = 0, mid = 0, high = rail.size() - 1;
        while (mid <= high) {
            int code = rail.get(mid).code();
            if (code == 0) { Towel t = rail.get(low); rail.set(low, rail.get(mid)); rail.set(mid, t); low++; mid++; }
            else if (code == 1) mid++;
            else { Towel t = rail.get(high); rail.set(high, rail.get(mid)); rail.set(mid, t); high--; }
        }
    }

    public static void main(String[] args) {
        int[] one = {2, 1, 0, 1, 2, 0};
        if (!Arrays.equals(flag(one), new int[] {2, 4}) || !Arrays.equals(one, new int[] {0, 0, 1, 1, 2, 2})) throw new AssertionError("example 1 " + Arrays.toString(one));
        int[] two = {1, 1, 1};
        if (!Arrays.equals(flag(two), new int[] {0, 3}) || !Arrays.equals(two, new int[] {1, 1, 1})) throw new AssertionError("example 2");
        if (!Arrays.equals(flag(new int[0]), new int[] {0, 0})) throw new AssertionError("empty");
        Random rnd = new Random(814);
        for (int t = 0; t < 4000; t++) {
            int n = rnd.nextInt(15);
            int[] a = new int[n];
            int[] counts = new int[3];
            for (int i = 0; i < n; i++) { a[i] = rnd.nextInt(3); counts[a[i]]++; }
            int[] expected = a.clone();
            Arrays.sort(expected);
            int[] got = flag(a);
            if (!Arrays.equals(a, expected)) throw new AssertionError("not sorted " + Arrays.toString(a));
            if (got[0] != counts[0] || got[1] != counts[0] + counts[1]) throw new AssertionError("boundaries " + Arrays.toString(got));
            if (iterations > n) throw new AssertionError("iterations " + iterations + " above " + n);
        }
        List<Towel> rail = new ArrayList<>();
        int[] codes = {2, 0, 1, 2, 0, 1, 1, 0};
        for (int i = 0; i < codes.length; i++) rail.add(new Towel(codes[i], "t" + i));
        List<Towel> before = new ArrayList<>(rail);
        flagTowels(rail);
        for (int i = 1; i < rail.size(); i++) if (rail.get(i - 1).code() > rail.get(i).code()) throw new AssertionError("objects not ordered");
        for (Towel t : before) if (!rail.contains(t)) throw new AssertionError("an object was lost: " + t);
        if (rail.size() != before.size()) throw new AssertionError("size changed");
    }
}
```

#### Solution: [Vary] Sort Colors (LeetCode 75)
<!-- id: tp-sort-colors -->

**Approach.** The same four-region invariant is written here with a `switch` on the value under the scanning marker. Red goes to the front region by a trade with the first white position, white advances the marker, and blue goes to the back by a trade with the last unscanned position, with the marker staying in place so the arrived value gets scanned. The contract is that nothing is returned, so the check reads the array itself after the call, confirms the loop ran at most n iterations, and compares with `Arrays.sort` on a copy for random inputs. It also confirms that the array object is the same object with the sorted contents, and that the extra memory is three integer markers by never allocating another array in the method.

**Complexity.** Linear time with one pass, and constant extra memory.

```java run
import java.util.Arrays;
import java.util.Random;

public final class SortColorsPass {
    static int loops;

    static void sortColors(int[] nums) {
        int redEnd = 0, cursor = 0, blueStart = nums.length - 1;
        loops = 0;
        while (cursor <= blueStart) {
            loops++;
            switch (nums[cursor]) {
                case 0 -> {
                    int keep = nums[redEnd];
                    nums[redEnd] = nums[cursor];
                    nums[cursor] = keep;
                    redEnd++;
                    cursor++;
                }
                case 1 -> cursor++;
                default -> {
                    int arrived = nums[blueStart];
                    nums[blueStart] = nums[cursor];
                    nums[cursor] = arrived;
                    blueStart--;
                }
            }
        }
    }

    public static void main(String[] args) {
        int[] one = {2, 0, 2, 1, 1, 0};
        sortColors(one);
        if (!Arrays.equals(one, new int[] {0, 0, 1, 1, 2, 2})) throw new AssertionError("example 1 " + Arrays.toString(one));
        int[] two = {1, 0};
        sortColors(two);
        if (!Arrays.equals(two, new int[] {0, 1})) throw new AssertionError("example 2");
        int[] empty = new int[0];
        sortColors(empty);
        if (loops != 0) throw new AssertionError("empty array must cost no loops");
        Random rnd = new Random(815);
        for (int t = 0; t < 4000; t++) {
            int n = rnd.nextInt(16);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(3);
            int[] expected = a.clone();
            Arrays.sort(expected);
            int[] same = a;
            sortColors(a);
            if (same != a || !Arrays.equals(a, expected)) throw new AssertionError("wrong result " + Arrays.toString(a));
            if (loops > n) throw new AssertionError("loops " + loops + " above " + n);
        }
        int[] allBlue = {2, 2, 2, 2, 2};
        sortColors(allBlue);
        if (loops != 5 || !Arrays.equals(allBlue, new int[] {2, 2, 2, 2, 2})) throw new AssertionError("all blue");
        int[] allRed = {0, 0, 0};
        sortColors(allRed);
        if (loops != 3) throw new AssertionError("all red");
    }
}
```

#### Solution: [Boundary] Reinspect Swapped High (Author exercise)
<!-- id: tp-reinspect-high -->

**Approach.** Run the one-pass sort and count each iteration in which the value under `mid` is 2, because that is the iteration that trades with `high` and leaves `mid` where it is. Every two is moved into the high region by exactly one such iteration, and `high` retreats once for each, so the count must equal the number of twos in the input, which is the oracle used here. The branch must not advance `mid` since the value that arrives from the far end has not been scanned. The check includes a deliberately wrong version that advances `mid` after the trade, and shows that it leaves the array `[1, 0, 2]` for the input `[1, 2, 0]` while the correct version sorts it. It also confirms both examples and compares with a sorted copy and the count of twos on random arrays.

**Complexity.** Linear time, at most n loop iterations in total, with constant extra memory.

```java run
import java.util.Arrays;
import java.util.Random;

public final class ReinspectHigh {
    static int sortAndCount(int[] a) {
        int low = 0, mid = 0, high = a.length - 1, stays = 0;
        while (mid <= high) {
            if (a[mid] == 0) {
                int t = a[low]; a[low] = a[mid]; a[mid] = t;
                low++; mid++;
            } else if (a[mid] == 1) {
                mid++;
            } else {
                int t = a[high]; a[high] = a[mid]; a[mid] = t;
                high--;
                stays++;
            }
        }
        return stays;
    }

    static void wrongAdvance(int[] a) {
        int low = 0, mid = 0, high = a.length - 1;
        while (mid <= high) {
            if (a[mid] == 0) {
                int t = a[low]; a[low] = a[mid]; a[mid] = t;
                low++; mid++;
            } else if (a[mid] == 1) {
                mid++;
            } else {
                int t = a[high]; a[high] = a[mid]; a[mid] = t;
                high--;
                mid++;
            }
        }
    }

    public static void main(String[] args) {
        int[] one = {2, 0, 1};
        if (sortAndCount(one) != 1 || !Arrays.equals(one, new int[] {0, 1, 2})) throw new AssertionError("example 1 " + Arrays.toString(one));
        int[] two = {2, 2, 0};
        if (sortAndCount(two) != 2 || !Arrays.equals(two, new int[] {0, 2, 2})) throw new AssertionError("example 2 " + Arrays.toString(two));
        int[] bad = {1, 2, 0};
        wrongAdvance(bad);
        if (!Arrays.equals(bad, new int[] {1, 0, 2})) throw new AssertionError("the wrong version should leave 1,0,2 but gave " + Arrays.toString(bad));
        int[] good = {1, 2, 0};
        sortAndCount(good);
        if (!Arrays.equals(good, new int[] {0, 1, 2})) throw new AssertionError("correct version failed");
        if (sortAndCount(new int[0]) != 0) throw new AssertionError("empty");
        if (sortAndCount(new int[] {2}) != 1) throw new AssertionError("single two");
        Random rnd = new Random(816);
        for (int t = 0; t < 4000; t++) {
            int n = rnd.nextInt(16);
            int[] a = new int[n];
            int twos = 0;
            for (int i = 0; i < n; i++) { a[i] = rnd.nextInt(3); if (a[i] == 2) twos++; }
            int[] expected = a.clone();
            Arrays.sort(expected);
            int stays = sortAndCount(a);
            if (!Arrays.equals(a, expected)) throw new AssertionError("not sorted " + Arrays.toString(a));
            if (stays != twos) throw new AssertionError("stays " + stays + " versus twos " + twos);
        }
    }
}
```

#### Solution: [Recognize] Three-Way Pivot Partition (Author exercise)
<!-- id: tp-pivot-three-way -->

**Approach.** The codes 0, 1 and 2 become the outcomes of `Integer.compare(value, pivot)`: negative sends the value to the front by a trade with the start of the equal region, zero only advances the scanning marker, and positive sends it to the back by a trade with the end of the unscanned stretch, with the marker staying. The returned pair holds the index where the equal region starts and the index where the greater region starts. Subtraction is never used, because `Integer.MAX_VALUE - Integer.MIN_VALUE` wraps to minus one and would call the largest value smaller than the smallest. The check confirms both examples, includes arrays with both extremes of `int`, and compares the region sizes and contents with a counting oracle on random arrays.

**Complexity.** Linear time with one read per loop step, and constant extra memory.

```java run
import java.util.Arrays;
import java.util.Random;

public final class PivotThreeWay {
    static int[] split(int[] a, int pivot) {
        int equalStart = 0, scan = 0, greaterStart = a.length;
        while (scan < greaterStart) {
            int c = Integer.compare(a[scan], pivot);
            if (c < 0) {
                int t = a[equalStart]; a[equalStart] = a[scan]; a[scan] = t;
                equalStart++;
                scan++;
            } else if (c > 0) {
                greaterStart--;
                int t = a[greaterStart]; a[greaterStart] = a[scan]; a[scan] = t;
            } else {
                scan++;
            }
        }
        return new int[] {equalStart, greaterStart};
    }

    static void check(int[] original, int pivot) {
        int[] a = original.clone();
        int[] got = split(a, pivot);
        int less = 0, equal = 0;
        for (int v : original) { if (v < pivot) less++; else if (v == pivot) equal++; }
        if (got[0] != less || got[1] != less + equal) throw new AssertionError("boundaries " + Arrays.toString(got) + " for " + Arrays.toString(original) + " pivot " + pivot);
        for (int i = 0; i < a.length; i++) {
            int expectedSign = i < less ? -1 : (i < less + equal ? 0 : 1);
            if (Integer.signum(Integer.compare(a[i], pivot)) != expectedSign) throw new AssertionError("region wrong at " + i + " in " + Arrays.toString(a));
        }
        int[] x = a.clone(), y = original.clone();
        Arrays.sort(x);
        Arrays.sort(y);
        if (!Arrays.equals(x, y)) throw new AssertionError("values changed");
    }

    public static void main(String[] args) {
        int[] one = {5, 9, 5, 1, 7, 5, 2};
        if (!Arrays.equals(split(one, 5), new int[] {2, 5}) || !Arrays.equals(one, new int[] {2, 1, 5, 5, 5, 7, 9})) throw new AssertionError("example 1 " + Arrays.toString(one));
        int[] two = {3, 3, 3};
        if (!Arrays.equals(split(two, 8), new int[] {3, 3}) || !Arrays.equals(two, new int[] {3, 3, 3})) throw new AssertionError("example 2");
        if (Integer.MAX_VALUE - Integer.MIN_VALUE != -1) throw new AssertionError("the difference of the extremes wraps to minus one");
        check(new int[] {Integer.MAX_VALUE, Integer.MIN_VALUE, 0, Integer.MAX_VALUE, Integer.MIN_VALUE}, 0);
        check(new int[] {Integer.MAX_VALUE, Integer.MIN_VALUE, 7}, Integer.MAX_VALUE);
        check(new int[] {Integer.MAX_VALUE, Integer.MIN_VALUE, 7}, Integer.MIN_VALUE);
        check(new int[0], 4);
        check(new int[] {4}, 4);
        check(new int[] {6, 6, 6, 6}, 6);
        Random rnd = new Random(817);
        for (int t = 0; t < 4000; t++) {
            int n = rnd.nextInt(15);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(9) - 4;
            check(a, rnd.nextInt(11) - 5);
        }
    }
}
```
