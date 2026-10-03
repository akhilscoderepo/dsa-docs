<!-- solutions-for: 08-read-and-write -->
### Read And Write

#### Solution: [Build] Remove Element (LeetCode 27)
<!-- id: tp-remove-element -->

**Approach.** Scan with `read` over every slot. A survivor is copied to `write`, but only when the two indices differ, and each such copy is counted as a move, since a survivor that has not yet fallen behind a removed entry is already in its place. The returned pair is the survivor count and the move count. The check compares with a filter that builds a new list and counts the survivors whose index changed, asserts that `write <= read` at every step, shows that the array keeps its length with stale values after the prefix, shows that swapping with the last entry would reorder the survivors, and counts assignments of the shifting method from the lesson to support the quadratic claim.

**Complexity.** One pass with at most one assignment per slot, so the cost is proportional to n, and the working memory is two integers and a counter.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

public final class RemoveElement {
    static int[] removeElement(int[] nums, int val) {
        int write = 0, moves = 0;
        for (int read = 0; read < nums.length; read++) {
            if (write > read) throw new AssertionError("write passed read");
            if (nums[read] != val) {
                if (read != write) {
                    nums[write] = nums[read];
                    moves++;
                }
                write++;
            }
        }
        return new int[] {write, moves};
    }
    static int shiftingAssignments(int[] a, int val) {
        int size = a.length, count = 0, pos = 0;
        while (pos < size) {
            if (a[pos] == val) {
                for (int j = pos + 1; j < size; j++) { a[j - 1] = a[j]; count++; }
                size--;
            } else pos++;
        }
        return count;
    }
    static int swapWithLast(int[] a, int val) {
        int size = a.length, i = 0;
        while (i < size) {
            if (a[i] == val) a[i] = a[--size]; else i++;
        }
        return size;
    }

    public static void main(String[] args) {
        int[] one = {4, 9, 4, 6, 7};
        int[] r1 = removeElement(one, 4);
        if (!Arrays.equals(r1, new int[] {3, 3})) throw new AssertionError("example 1 " + Arrays.toString(r1));
        if (!Arrays.equals(Arrays.copyOf(one, 3), new int[] {9, 6, 7})) throw new AssertionError("example 1 prefix");
        if (one.length != 5 || one[3] != 6 || one[4] != 7) throw new AssertionError("the array keeps its length and stale slots");
        int[] two = {8, 8, 2, 3};
        if (!Arrays.equals(removeElement(two, 9), new int[] {4, 0})) throw new AssertionError("example 2");
        if (!Arrays.equals(two, new int[] {8, 8, 2, 3})) throw new AssertionError("example 2 array changed");
        int[] swapped = {4, 9, 4, 6, 7};
        int sk = swapWithLast(swapped, 4);
        if (sk != 3 || Arrays.equals(Arrays.copyOf(swapped, sk), new int[] {9, 6, 7})) throw new AssertionError("swap with last should reorder survivors");
        Random rnd = new Random(821);
        for (int t = 0; t < 5000; t++) {
            int n = rnd.nextInt(12);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = t % 6 == 0 ? 3 : rnd.nextInt(4) - 1;
            int val = rnd.nextInt(5) - 1;
            List<Integer> keep = new ArrayList<>();
            int expectMoves = 0;
            for (int i = 0; i < n; i++) if (a[i] != val) { if (i != keep.size()) expectMoves++; keep.add(a[i]); }
            int[] work = a.clone();
            int[] got = removeElement(work, val);
            if (got[0] != keep.size() || got[1] != expectMoves) throw new AssertionError("differs on " + Arrays.toString(a) + " val " + val);
            for (int i = 0; i < keep.size(); i++) if (work[i] != keep.get(i)) throw new AssertionError("prefix differs on " + Arrays.toString(a));
        }
        int n = 2000;
        int[] tray = new int[n];
        for (int i = 0; i < n; i++) tray[i] = i % 2;
        int shifts = shiftingAssignments(tray.clone(), 1);
        if (shifts < n * n / 8) throw new AssertionError("shifting should be quadratic: " + shifts);
        int[] pass = removeElement(tray.clone(), 1);
        if (pass[1] > n) throw new AssertionError("the single pass assigns at most once per slot");
    }
}
```

#### Solution: [Vary] Move Zeroes (LeetCode 283)
<!-- id: tp-move-zeroes -->

**Approach.** Scan with `read`. A token with a nonzero key is swapped into the slot at `write` when the two indices differ, and `write` advances. The swap carries the zero-key token that was sitting at `write` out to the read position, so no object is lost, and the nonzero tokens keep their order because they are accepted in scan order. A copy-then-fill version would replace the discarded tokens by new objects, which the check shows by comparing identities. The check compares with a stable partition built from lists, verifies by identity that the tokens form a permutation of the originals, and covers empty and all-zero arrays.

**Complexity.** One pass of n reads and at most n swaps, with constant extra memory.

```java run
import java.util.ArrayList;
import java.util.IdentityHashMap;
import java.util.List;
import java.util.Random;

public final class MoveZeroes {
    static final class Token {
        final int key;
        Token(int key) { this.key = key; }
    }

    static void moveZeroes(Token[] tokens) {
        int write = 0;
        for (int read = 0; read < tokens.length; read++) {
            if (tokens[read].key != 0) {
                if (read != write) {
                    Token held = tokens[write];
                    tokens[write] = tokens[read];
                    tokens[read] = held;
                }
                write++;
            }
        }
    }
    static void copyThenFill(Token[] tokens) {
        int write = 0;
        for (int read = 0; read < tokens.length; read++) if (tokens[read].key != 0) tokens[write++] = tokens[read];
        while (write < tokens.length) tokens[write++] = new Token(0);
    }
    static Token[] make(int... keys) {
        Token[] t = new Token[keys.length];
        for (int i = 0; i < keys.length; i++) t[i] = new Token(keys[i]);
        return t;
    }
    static boolean samePopulation(Token[] before, Token[] after) {
        IdentityHashMap<Token, Integer> seen = new IdentityHashMap<>();
        for (Token x : before) seen.merge(x, 1, Integer::sum);
        for (Token x : after) seen.merge(x, -1, Integer::sum);
        for (int v : seen.values()) if (v != 0) return false;
        return true;
    }
    static String keys(Token[] t) {
        StringBuilder sb = new StringBuilder();
        for (Token x : t) sb.append(x.key).append(' ');
        return sb.toString().trim();
    }

    public static void main(String[] args) {
        Token[] one = make(3, 0, 0, 5, 0, 8);
        Token[] oneBefore = one.clone();
        moveZeroes(one);
        if (!keys(one).equals("3 5 8 0 0 0")) throw new AssertionError("example 1 " + keys(one));
        if (one[0] != oneBefore[0] || one[1] != oneBefore[3] || one[2] != oneBefore[5]) throw new AssertionError("nonzero tokens must be the same objects");
        Token[] two = make(6, 7);
        Token[] twoBefore = two.clone();
        moveZeroes(two);
        if (!keys(two).equals("6 7") || two[0] != twoBefore[0] || two[1] != twoBefore[1]) throw new AssertionError("example 2");
        Token[] lossy = make(3, 0, 0, 5, 0, 8);
        Token[] lossyBefore = lossy.clone();
        copyThenFill(lossy);
        if (samePopulation(lossyBefore, lossy)) throw new AssertionError("copy then fill should replace objects");
        moveZeroes(new Token[0]);
        Random rnd = new Random(822);
        for (int t = 0; t < 5000; t++) {
            int n = rnd.nextInt(12);
            int[] ks = new int[n];
            for (int i = 0; i < n; i++) ks[i] = t % 5 == 0 ? 0 : (rnd.nextInt(3) == 0 ? rnd.nextInt(5) + 1 : 0);
            Token[] arr = make(ks);
            Token[] before = arr.clone();
            moveZeroes(arr);
            List<Token> expected = new ArrayList<>();
            for (Token x : before) if (x.key != 0) expected.add(x);
            int nonzero = expected.size();
            for (int i = 0; i < nonzero; i++) if (arr[i] != expected.get(i)) throw new AssertionError("nonzero order broke");
            for (int i = nonzero; i < n; i++) if (arr[i].key != 0) throw new AssertionError("zero tail broke");
            if (!samePopulation(before, arr)) throw new AssertionError("a token was lost or duplicated");
        }
    }
}
```

#### Solution: [Boundary] Remove Duplicates from Sorted Array (LeetCode 26)
<!-- id: tp-keep-last-of-run -->

**Approach.** An item is accepted when it ends its run, meaning it is the final item or the next item has a different key. Accepted items are copied to `write` in scan order, and the count is returned. An empty array never enters the loop, a run of one item ends itself, and a run of equal keys contributes exactly its last item. The usual test against the newest accepted item would keep the first of each run instead, and the check shows that the two rules pick different tags. The check compares with a list built by scanning from the right, using object identity on random sorted arrays with all-equal and one-element cases.

**Complexity.** The scan visits each slot once and looks one slot ahead, so the work is linear with constant extra memory.

```java run
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public final class KeepLastOfRun {
    record Item(int key, char tag) {}

    static int keepLast(Item[] items) {
        int write = 0;
        for (int read = 0; read < items.length; read++) {
            boolean endsRun = read + 1 == items.length || items[read + 1].key() != items[read].key();
            if (endsRun) items[write++] = items[read];
        }
        return write;
    }
    static int keepFirst(Item[] items) {
        int write = 0;
        for (int read = 0; read < items.length; read++) {
            if (write == 0 || items[read].key() != items[write - 1].key()) items[write++] = items[read];
        }
        return write;
    }
    static Item[] parse(String s) {
        if (s.isBlank()) return new Item[0];
        String[] parts = s.trim().split(" ");
        Item[] out = new Item[parts.length];
        for (int i = 0; i < parts.length; i++) out[i] = new Item(Integer.parseInt(parts[i].substring(0, parts[i].indexOf(':'))), parts[i].charAt(parts[i].length() - 1));
        return out;
    }
    static String show(Item[] a, int k) {
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < k; i++) sb.append(a[i].key()).append(':').append(a[i].tag()).append(' ');
        return sb.toString().trim();
    }

    public static void main(String[] args) {
        Item[] one = parse("1:a 1:b 2:c 3:d 3:e 3:f");
        int k1 = keepLast(one);
        if (k1 != 3 || !show(one, k1).equals("1:b 2:c 3:f")) throw new AssertionError("example 1 " + show(one, k1));
        Item[] none = parse("");
        if (keepLast(none) != 0) throw new AssertionError("example 2");
        Item[] single = parse("7:z");
        if (keepLast(single) != 1 || single[0].tag() != 'z') throw new AssertionError("one element");
        Item[] firsts = parse("1:a 1:b 2:c 3:d 3:e 3:f");
        int kf = keepFirst(firsts);
        if (kf != 3 || !show(firsts, kf).equals("1:a 2:c 3:d")) throw new AssertionError("the first-of-run rule keeps different tags");
        Random rnd = new Random(823);
        for (int t = 0; t < 5000; t++) {
            int n = rnd.nextInt(12);
            Item[] arr = new Item[n];
            int key = rnd.nextInt(5) - 2;
            for (int i = 0; i < n; i++) {
                if (t % 7 != 0 && rnd.nextInt(3) == 0) key += 1 + rnd.nextInt(2);
                arr[i] = new Item(key, (char) ('a' + i));
            }
            Item[] before = arr.clone();
            List<Item> expected = new ArrayList<>();
            for (int i = n - 1; i >= 0; i--) if (expected.isEmpty() || before[i].key() != expected.get(0).key()) expected.add(0, before[i]);
            int k = keepLast(arr);
            if (k != expected.size()) throw new AssertionError("count differs");
            for (int i = 0; i < k; i++) if (arr[i] != expected.get(i)) throw new AssertionError("survivor differs at " + i);
        }
    }
}
```

#### Solution: [Recognize] Remove Duplicates from Sorted Array II (LeetCode 80)
<!-- id: tp-at-most-limit -->

**Approach.** The read index advances over every slot, and a value is admitted when fewer than `L` slots are kept so far, or when it differs from the kept entry exactly `L` places behind the write index. Because the array is sorted, that kept entry equals the current value only if `L` copies are already in the prefix. A limit of zero is answered with 0 before the loop, and the check shows that without that guard the look-behind would accept values wrongly. The check also counts the reads, which equal the length, compares with a counting oracle on random sorted arrays and all limits from 0 to the length, and confirms that limit 1 matches the one-per-run loop from the lesson, including on the empty array.

**Complexity.** One read per slot and at most one write per slot, so the work is linear in the length with constant extra memory.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

public final class AtMostLimit {
    static int reads;

    static int keepAtMost(int[] nums, int limit) {
        if (limit == 0) return 0;
        int write = 0;
        for (int read = 0; read < nums.length; read++) {
            reads++;
            int v = nums[read];
            if (write < limit || nums[write - limit] != v) nums[write++] = v;
        }
        return write;
    }
    static int unguarded(int[] nums, int limit) {
        int write = 0;
        for (int read = 0; read < nums.length; read++) {
            int v = nums[read];
            if (write < limit || nums[write - limit] != v) nums[write++] = v;
        }
        return write;
    }
    static int onePerRun(int[] sorted) {
        int write = 0;
        for (int read = 0; read < sorted.length; read++) {
            if (write == 0 || sorted[read] != sorted[write - 1]) sorted[write++] = sorted[read];
        }
        return write;
    }

    public static void main(String[] args) {
        int[] one = {2, 2, 2, 2, 5, 5, 9};
        int k1 = keepAtMost(one, 3);
        if (k1 != 6 || !Arrays.equals(Arrays.copyOf(one, k1), new int[] {2, 2, 2, 5, 5, 9})) throw new AssertionError("example 1");
        if (keepAtMost(new int[] {4, 4}, 0) != 0) throw new AssertionError("example 2");
        if (unguarded(new int[] {4, 4, 5}, 0) == 0) throw new AssertionError("the zero limit needs its guard");
        if (keepAtMost(new int[0], 0) != 0 || keepAtMost(new int[0], 1) != 0) throw new AssertionError("empty array");
        Random rnd = new Random(824);
        for (int t = 0; t < 4000; t++) {
            int n = rnd.nextInt(12);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = t % 6 == 0 ? 2 : rnd.nextInt(5) - 2;
            Arrays.sort(a);
            for (int limit = 0; limit <= n; limit++) {
                List<Integer> expected = new ArrayList<>();
                int run = 0;
                for (int i = 0; i < n; i++) {
                    run = i > 0 && a[i] == a[i - 1] ? run + 1 : 1;
                    if (run <= limit) expected.add(a[i]);
                }
                int[] work = a.clone();
                reads = 0;
                int k = keepAtMost(work, limit);
                if (reads != (limit == 0 ? 0 : n)) throw new AssertionError("reads " + reads);
                if (k != expected.size()) throw new AssertionError("count differs on " + Arrays.toString(a) + " limit " + limit);
                for (int i = 0; i < k; i++) if (work[i] != expected.get(i)) throw new AssertionError("prefix differs on " + Arrays.toString(a));
            }
            int[] x = a.clone(), y = a.clone();
            int kx = keepAtMost(x, 1), ky = onePerRun(y);
            if (kx != ky || !Arrays.equals(Arrays.copyOf(x, kx), Arrays.copyOf(y, ky))) throw new AssertionError("limit 1 differs from the lesson loop on " + Arrays.toString(a) + " " + kx + " " + ky);
        }
    }
}
```
