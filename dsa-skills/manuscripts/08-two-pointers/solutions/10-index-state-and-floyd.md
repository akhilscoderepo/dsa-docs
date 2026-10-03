<!-- solutions-for: 08-index-state-and-floyd -->
### Index State And Floyd

#### Solution: [Build] Value-As-Next-Index (Author exercise)
<!-- id: tp-value-as-next-index -->

**Approach.** First validate: the length must be at least 2 and every value must be between 1 and n, where n is the length minus one. Only then walk, because a value of 0 would send the walk back to the start and a value above n would be an out-of-range read. The walk appends the current index to a list and moves along the link, and stops when the next index is already in the list. All indices are between 0 and n and each is added at most once, so the path has at most n + 1 entries. The check recomputes both examples, shows that an unvalidated walk on an illegal array either throws `ArrayIndexOutOfBoundsException` or comes back to index 0, compares with a brute force that rebuilds the path by repeated membership tests, and verifies that the array is unchanged.

**Complexity.** Validation reads each value once and the walk visits each index at most once, so O(n) time, and the returned path is the only memory used beyond a visited array of n + 1 booleans.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

public final class ValueAsNextIndex {
    static boolean legal(int[] nums) {
        if (nums.length < 2) return false;
        for (int v : nums) if (v < 1 || v > nums.length - 1) return false;
        return true;
    }

    static int[] pathFromZero(int[] nums) {
        if (!legal(nums)) return new int[0];
        boolean[] seen = new boolean[nums.length];
        int[] buffer = new int[nums.length];
        int size = 0, at = 0;
        while (!seen[at]) {
            seen[at] = true;
            buffer[size++] = at;
            at = nums[at];
        }
        return Arrays.copyOf(buffer, size);
    }

    static int[] oracle(int[] nums) {
        for (int v : nums) if (v < 1 || v > nums.length - 1) return new int[0];
        if (nums.length < 2) return new int[0];
        List<Integer> order = new ArrayList<>();
        int at = 0;
        while (!order.contains(at)) { order.add(at); at = nums[at]; }
        int[] out = new int[order.size()];
        for (int i = 0; i < out.length; i++) out[i] = order.get(i);
        return out;
    }

    public static void main(String[] args) {
        if (!Arrays.equals(pathFromZero(new int[] {3, 1, 4, 2, 1}), new int[] {0, 3, 2, 4, 1})) throw new AssertionError("example 1");
        if (pathFromZero(new int[] {2, 0, 1}).length != 0) throw new AssertionError("example 2");
        if (pathFromZero(new int[0]).length != 0 || pathFromZero(new int[] {1}).length != 0) throw new AssertionError("too short");
        int[] zeroValue = {2, 0, 1};
        int at = 0;
        for (int s = 0; s < 3; s++) at = zeroValue[at];
        boolean returned = false;
        int walk = 0;
        for (int s = 0; s < 3; s++) { walk = zeroValue[walk]; if (walk == 0) returned = true; }
        if (!returned) throw new AssertionError("a zero value should send the walk back to index 0");
        try {
            int[] pastEnd = {1, 5};
            int x = 0;
            for (int s = 0; s < 3; s++) x = pastEnd[x];
            throw new AssertionError("no exception for a value past the end");
        } catch (ArrayIndexOutOfBoundsException expected) {
            // an unvalidated walk fails here, which is why validation comes first
        }
        Random rnd = new Random(8101);
        int legalCount = 0, illegalCount = 0;
        for (int t = 0; t < 5000; t++) {
            int len = rnd.nextInt(9);
            int[] nums = new int[len];
            boolean wild = rnd.nextInt(4) == 0;
            for (int i = 0; i < len; i++) nums[i] = wild ? rnd.nextInt(len + 4) - 2 : 1 + rnd.nextInt(Math.max(1, len - 1));
            int[] before = nums.clone();
            int[] got = pathFromZero(nums);
            if (!Arrays.equals(got, oracle(nums))) throw new AssertionError("differs on " + Arrays.toString(nums));
            if (!Arrays.equals(before, nums)) throw new AssertionError("array changed");
            if (got.length > len) throw new AssertionError("path longer than n + 1");
            if (got.length == 0) illegalCount++; else legalCount++;
        }
        if (legalCount == 0 || illegalCount == 0) throw new AssertionError("both kinds of input must occur");
    }
}
```

#### Solution: [Vary] Find the Duplicate Number (LeetCode 287)
<!-- id: tp-duplicate-triple -->

**Approach.** The meeting phase moves `walker` one link and `runner` two links per round from index 0 until they coincide. The entry phase leaves the walker in place, restarts `returner` at 0 and moves both one link per round while counting rounds, and the count is the tail length because the returner needs exactly that many links to reach the first ring place. A last short walk from the entry counts the links until it is back on the entry, which is the ring size. The check recomputes both examples, enumerates every legal array for n up to 4 plus random ones with values repeated several times, and compares the triple with a first-visit table oracle. It also asserts that the number of meeting rounds is the smallest multiple of the ring size that is at least the tail, that this number differs from the tail whenever the ring is longer than the tail, that no loop runs for more than n + 1 rounds, and that the array is unchanged.

**Complexity.** The three loops together make O(n) rounds and use a few integers, so memory is O(1) beyond the input and nothing is written.

```java run
import java.util.Arrays;
import java.util.Random;

public final class DuplicateTriple {
    static int meetRounds, entryRounds, lapRounds;

    static int[] duplicateReport(int[] nums) {
        int walker = 0, runner = 0;
        meetRounds = 0;
        do {
            walker = nums[walker];
            runner = nums[nums[runner]];
            meetRounds++;
        } while (walker != runner);
        int returner = 0, tail = 0;
        while (returner != walker) {
            returner = nums[returner];
            walker = nums[walker];
            tail++;
        }
        entryRounds = tail;
        int entry = walker, cycle = 1;
        for (int probe = nums[entry]; probe != entry; probe = nums[probe]) cycle++;
        lapRounds = cycle;
        return new int[] {entry, tail, cycle};
    }

    static int[] oracle(int[] nums) {
        int[] first = new int[nums.length];
        Arrays.fill(first, -1);
        int at = 0, step = 0;
        while (first[at] < 0) { first[at] = step++; at = nums[at]; }
        return new int[] {at, first[at], step - first[at]};
    }

    static boolean legal(int[] nums) {
        int n = nums.length - 1, repeated = 0;
        int[] count = new int[n + 1];
        for (int v : nums) {
            if (v < 1 || v > n) return false;
            count[v]++;
        }
        for (int v = 1; v <= n; v++) if (count[v] > 1) repeated++;
        return repeated == 1;
    }

    static int longerRingCases = 0;

    static void check(int[] nums) {
        int[] before = nums.clone();
        int n = nums.length - 1;
        int[] got = duplicateReport(nums);
        int[] want = oracle(nums);
        if (!Arrays.equals(got, want)) throw new AssertionError("differs on " + Arrays.toString(nums));
        if (!Arrays.equals(before, nums)) throw new AssertionError("array changed");
        int tail = got[1], ring = got[2];
        int smallestMultiple = ((tail + ring - 1) / ring) * ring;
        if (meetRounds != smallestMultiple) throw new AssertionError("meeting rounds " + meetRounds + " on " + Arrays.toString(nums));
        if (ring > tail) {
            longerRingCases++;
            if (meetRounds == tail) throw new AssertionError("meeting rounds equal tail with a longer ring");
        }
        if (meetRounds > n + 1 || entryRounds > n + 1 || lapRounds > n + 1) throw new AssertionError("loop too long");
        int d = 0;
        for (int v : nums) { int c = 0; for (int w : nums) if (w == v) c++; if (c > 1) d = v; }
        if (got[0] != d) throw new AssertionError("entry is not the repeated value");
    }

    static void enumerate(int[] nums, int pos, int n) {
        if (pos == nums.length) { if (legal(nums)) check(nums); return; }
        for (int v = 1; v <= n; v++) { nums[pos] = v; enumerate(nums, pos + 1, n); }
    }

    public static void main(String[] args) {
        if (!Arrays.equals(duplicateReport(new int[] {2, 4, 3, 1, 2}), new int[] {2, 1, 4})) throw new AssertionError("example 1");
        if (!Arrays.equals(duplicateReport(new int[] {5, 2, 6, 1, 3, 4, 2}), new int[] {2, 5, 2})) throw new AssertionError("example 2");
        for (int n = 1; n <= 4; n++) enumerate(new int[n + 1], 0, n);
        Random rnd = new Random(8102);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(30);
            int d = 1 + rnd.nextInt(n);
            int k = 2 + rnd.nextInt(Math.min(n, 4));
            int[] pool = new int[n - 1];
            int p = 0;
            for (int v = 1; v <= n; v++) if (v != d) pool[p++] = v;
            for (int i = pool.length - 1; i > 0; i--) { int j = rnd.nextInt(i + 1); int tmp = pool[i]; pool[i] = pool[j]; pool[j] = tmp; }
            int[] nums = new int[n + 1];
            int f = 0;
            for (int i = 0; i < k && f < n + 1; i++) nums[f++] = d;
            for (int i = 0; f < n + 1; i++) nums[f++] = pool[i];
            for (int i = nums.length - 1; i > 0; i--) { int j = rnd.nextInt(i + 1); int tmp = nums[i]; nums[i] = nums[j]; nums[j] = tmp; }
            check(nums);
        }
        if (longerRingCases == 0) throw new AssertionError("no case with a longer ring");
    }
}
```

#### Solution: [Boundary] Duplicate Near Start (Author exercise)
<!-- id: tp-duplicate-near-start -->

**Approach.** When `nums[0]` is the repeated value, the first link of the walk goes straight onto the ring, so the tail is one step, and the entry phase runs one round: the returner moves from 0 to the entry while the walker moves once around the ring, to a place that is one link before the entry modulo the ring size, which is the meeting place. The tail cannot be 0 because that would put index 0 on the ring, and some cell would then have to hold the value 0, which a legal array forbids. The same code path as for long tails works unchanged. The check recomputes both examples, enumerates every legal array for n up to 5 to confirm that the tail is at least 1, builds random arrays with `nums[0]` repeated and asserts a tail of 1 and a single entry round, compares with a first-visit oracle, and confirms that no cell was written.

**Complexity.** Linear time with at most n + 1 rounds in each phase, and constant memory beyond the input.

```java run
import java.util.Arrays;
import java.util.Random;

public final class DuplicateNearStart {
    static int entryRounds;

    static int[] report(int[] nums) {
        int a = 0, b = 0;
        do { a = nums[a]; b = nums[nums[b]]; } while (a != b);
        int c = 0, tail = 0;
        while (c != a) { c = nums[c]; a = nums[a]; tail++; }
        entryRounds = tail;
        int size = 1;
        for (int p = nums[a]; p != a; p = nums[p]) size++;
        return new int[] {a, tail, size};
    }

    static int[] oracle(int[] nums) {
        int[] first = new int[nums.length];
        Arrays.fill(first, -1);
        int at = 0, step = 0;
        while (first[at] < 0) { first[at] = step++; at = nums[at]; }
        return new int[] {at, first[at], step - first[at]};
    }

    static int minTail = Integer.MAX_VALUE;

    static void enumerate(int[] nums, int pos, int n) {
        if (pos == nums.length) {
            int[] count = new int[n + 1];
            int repeated = 0;
            for (int v : nums) count[v]++;
            for (int v = 1; v <= n; v++) if (count[v] > 1) repeated++;
            if (repeated == 1) minTail = Math.min(minTail, oracle(nums)[1]);
            return;
        }
        for (int v = 1; v <= n; v++) { nums[pos] = v; enumerate(nums, pos + 1, n); }
    }

    public static void main(String[] args) {
        if (!Arrays.equals(report(new int[] {1, 1}), new int[] {1, 1, 1})) throw new AssertionError("example 1");
        if (!Arrays.equals(report(new int[] {2, 3, 1, 2}), new int[] {2, 1, 3})) throw new AssertionError("example 2");
        for (int n = 1; n <= 5; n++) enumerate(new int[n + 1], 0, n);
        if (minTail != 1) throw new AssertionError("minimum tail should be 1 but was " + minTail);
        Random rnd = new Random(8103);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(25);
            int d = 1 + rnd.nextInt(n);
            int k = 2 + rnd.nextInt(Math.min(n, 3));
            int[] pool = new int[n - 1];
            int p = 0;
            for (int v = 1; v <= n; v++) if (v != d) pool[p++] = v;
            for (int i = pool.length - 1; i > 0; i--) { int j = rnd.nextInt(i + 1); int tmp = pool[i]; pool[i] = pool[j]; pool[j] = tmp; }
            int[] rest = new int[n];
            int f = 0;
            for (int i = 0; i < k - 1; i++) rest[f++] = d;
            for (int i = 0; f < n; i++) rest[f++] = pool[i];
            for (int i = rest.length - 1; i > 0; i--) { int j = rnd.nextInt(i + 1); int tmp = rest[i]; rest[i] = rest[j]; rest[j] = tmp; }
            int[] nums = new int[n + 1];
            nums[0] = d;
            System.arraycopy(rest, 0, nums, 1, n);
            int[] before = nums.clone();
            int[] got = report(nums);
            if (!Arrays.equals(got, oracle(nums))) throw new AssertionError("differs on " + Arrays.toString(nums));
            if (got[1] != 1 || entryRounds != 1) throw new AssertionError("tail should be 1 on " + Arrays.toString(nums));
            if (got[0] != nums[0]) throw new AssertionError("entry should be nums[0]");
            if (!Arrays.equals(before, nums)) throw new AssertionError("array changed");
        }
    }
}
```

#### Solution: [Recognize] Compare Alternatives (Author exercise)
<!-- id: tp-compare-alternatives -->

**Approach.** Floyd's two walks only read, so its count is always 0. Cyclic placement takes the value held in a cell, returns it if its own cell already holds it, and otherwise swaps it into that cell, which changes the array whenever a swap happens, and it can return before any swap when the duplicate is detected at once. Sign marking negates the cell named by each absolute value, so it always changes at least the first marked cell, and it returns when it meets an already negative cell. Each finder runs on its own copy, and the cell counts are compared with the original. The check recomputes both examples, verifies that all three methods return the duplicate that a counting oracle gives, that Floyd never writes, that sign marking always writes at least one cell, and that both zero and non-zero outcomes occur for placement.

**Complexity.** All three finders take O(n) time. Floyd uses O(1) extra space, while placement and sign marking also use O(1) extra space but write to the array, which is the reason they are excluded when the input is read-only.

```java run
import java.util.Arrays;
import java.util.Random;

public final class CompareAlternatives {
    static int floyd(int[] a) {
        int w = 0, r = 0;
        do { w = a[w]; r = a[a[r]]; } while (w != r);
        int s = 0;
        while (s != w) { s = a[s]; w = a[w]; }
        return w;
    }

    static int placement(int[] a) {
        for (int i = 0; i < a.length; i++) {
            while (a[i] != i) {
                int v = a[i];
                if (a[v] == v) return v;
                a[i] = a[v];
                a[v] = v;
            }
        }
        return -1;
    }

    static int signMarking(int[] a) {
        for (int i = 0; i < a.length; i++) {
            int v = Math.abs(a[i]);
            if (a[v] < 0) return v;
            a[v] = -a[v];
        }
        return -1;
    }

    static int changed(int[] before, int[] after) {
        int c = 0;
        for (int i = 0; i < before.length; i++) if (before[i] != after[i]) c++;
        return c;
    }

    static int[] compare(int[] nums) {
        int[] a = nums.clone(), b = nums.clone(), c = nums.clone();
        int d1 = floyd(a), d2 = placement(b), d3 = signMarking(c);
        if (d1 != d2 || d2 != d3) throw new AssertionError("finders disagree on " + Arrays.toString(nums));
        return new int[] {changed(nums, a), changed(nums, b), changed(nums, c)};
    }

    static int oracle(int[] nums) {
        int[] count = new int[nums.length + 1];
        for (int v : nums) if (++count[v] > 1) return v;
        return -1;
    }

    public static void main(String[] args) {
        if (!Arrays.equals(compare(new int[] {3, 1, 4, 2, 1}), new int[] {0, 4, 4})) throw new AssertionError("example 1");
        if (!Arrays.equals(compare(new int[] {1, 1}), new int[] {0, 0, 1})) throw new AssertionError("example 2");
        Random rnd = new Random(8104);
        int placementZero = 0, placementWrote = 0;
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(20);
            int d = 1 + rnd.nextInt(n);
            int k = 2 + rnd.nextInt(Math.min(n, 3));
            int[] pool = new int[n - 1];
            int p = 0;
            for (int v = 1; v <= n; v++) if (v != d) pool[p++] = v;
            for (int i = pool.length - 1; i > 0; i--) { int j = rnd.nextInt(i + 1); int tmp = pool[i]; pool[i] = pool[j]; pool[j] = tmp; }
            int[] nums = new int[n + 1];
            int f = 0;
            for (int i = 0; i < k && f < n + 1; i++) nums[f++] = d;
            for (int i = 0; f < n + 1; i++) nums[f++] = pool[i];
            for (int i = nums.length - 1; i > 0; i--) { int j = rnd.nextInt(i + 1); int tmp = nums[i]; nums[i] = nums[j]; nums[j] = tmp; }
            int[] before = nums.clone();
            int[] counts = compare(nums);
            if (!Arrays.equals(before, nums)) throw new AssertionError("compare must work on copies");
            if (floyd(nums.clone()) != oracle(nums)) throw new AssertionError("floyd differs");
            if (counts[0] != 0) throw new AssertionError("floyd wrote");
            if (counts[2] < 1) throw new AssertionError("sign marking wrote nothing");
            if (counts[1] == 0) placementZero++; else placementWrote++;
        }
        if (placementZero == 0 || placementWrote == 0) throw new AssertionError("both placement outcomes must occur");
    }
}
```
