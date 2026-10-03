<!-- solutions-for: 05-sort-and-deduplicate -->
### Sort And Deduplicate

#### Solution: [Build] Contains Duplicate (LeetCode 217)
<!-- id: so-contains-duplicate-runs -->

**Approach.** Copy the argument, sort the copy, and walk it keeping the length of the current run. When a value equals its predecessor the run grows by one, and otherwise it restarts at one. The moment a run reaches two, a duplicate exists. The test compares with a hash-set oracle, confirms that the caller's array is unchanged, and covers the extremes of the `int` range.

**Complexity.** O(n log n) time and O(n) extra space for the copy.

```java run
import java.util.Arrays;
import java.util.HashSet;
import java.util.Random;
import java.util.Set;

public final class ContainsDuplicateRuns {
    static boolean containsDuplicate(int[] nums) {
        int[] a = nums.clone();
        Arrays.sort(a);
        int runLength = 0;
        for (int i = 0; i < a.length; i++) {
            runLength = (i > 0 && a[i] == a[i - 1]) ? runLength + 1 : 1;
            if (runLength >= 2) return true;
        }
        return false;
    }
    static boolean oracle(int[] nums) {
        Set<Integer> seen = new HashSet<>();
        for (int x : nums) if (!seen.add(x)) return true;
        return false;
    }

    public static void main(String[] args) {
        if (!containsDuplicate(new int[] {12, 5, 12})) throw new AssertionError("example 1");
        if (containsDuplicate(new int[] {8, 1, 6, 3})) throw new AssertionError("example 2");
        if (containsDuplicate(new int[] {Integer.MIN_VALUE, Integer.MAX_VALUE})) throw new AssertionError("extremes are distinct");
        if (!containsDuplicate(new int[] {Integer.MIN_VALUE, 3, Integer.MIN_VALUE})) throw new AssertionError("repeated extreme");
        Random rnd = new Random(561);
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(14);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(20) - 10;
            int[] keep = a.clone();
            if (containsDuplicate(a) != oracle(a)) throw new AssertionError("differs from the set oracle on " + Arrays.toString(keep));
            if (!Arrays.equals(a, keep)) throw new AssertionError("the argument must stay untouched");
        }
    }
}
```

#### Solution: [Vary] Intersection of Two Arrays (LeetCode 349)
<!-- id: so-intersection-sorted-runs -->

**Approach.** Reduce each array to its distinct values by sorting and keeping one representative per run. Join the two reduced lists and sort them. A value that came from both arrays now appears exactly twice, as an adjacent equal pair, and a value from one array appears once. Scanning for adjacent equal pairs therefore lists the common values in ascending order. The oracle checks membership of each candidate value directly by scanning both arrays, over every value in a small range.

**Complexity.** O((a + b) log(a + b)) time and O(a + b) extra space.

```java run
import java.util.Arrays;
import java.util.Random;

public final class IntersectionSortedRuns {
    static int[] distinctSorted(int[] values) {
        int[] a = values.clone();
        Arrays.sort(a);
        int[] out = new int[a.length];
        int size = 0;
        for (int i = 0; i < a.length; i++) if (i == 0 || a[i] != a[i - 1]) out[size++] = a[i];
        return Arrays.copyOf(out, size);
    }
    static int[] commonValues(int[] x, int[] y) {
        int[] ux = distinctSorted(x), uy = distinctSorted(y);
        int[] both = new int[ux.length + uy.length];
        System.arraycopy(ux, 0, both, 0, ux.length);
        System.arraycopy(uy, 0, both, ux.length, uy.length);
        Arrays.sort(both);
        int[] out = new int[Math.min(ux.length, uy.length)];
        int size = 0;
        for (int i = 1; i < both.length; i++) if (both[i] == both[i - 1]) out[size++] = both[i];
        return Arrays.copyOf(out, size);
    }
    static boolean has(int[] a, int v) { for (int x : a) if (x == v) return true; return false; }
    static int[] oracle(int[] x, int[] y, int range) {
        int[] out = new int[range];
        int size = 0;
        for (int v = 0; v < range; v++) if (has(x, v) && has(y, v)) out[size++] = v;
        return Arrays.copyOf(out, size);
    }

    public static void main(String[] args) {
        if (!Arrays.equals(commonValues(new int[] {4, 9, 5, 9}, new int[] {9, 4, 9, 8, 4}), new int[] {4, 9})) throw new AssertionError("example 1");
        if (commonValues(new int[] {1, 2}, new int[] {3, 4}).length != 0) throw new AssertionError("example 2");
        if (!Arrays.equals(commonValues(new int[] {7, 7, 7}, new int[] {7}), new int[] {7})) throw new AssertionError("a long run on one side");
        Random rnd = new Random(562);
        for (int t = 0; t < 4000; t++) {
            int[] x = new int[1 + rnd.nextInt(10)], y = new int[1 + rnd.nextInt(10)];
            for (int i = 0; i < x.length; i++) x[i] = rnd.nextInt(12);
            for (int i = 0; i < y.length; i++) y[i] = rnd.nextInt(12);
            if (!Arrays.equals(commonValues(x, y), oracle(x, y, 12))) throw new AssertionError("differs on " + Arrays.toString(x) + " and " + Arrays.toString(y));
        }
    }
}
```

#### Solution: [Boundary] All Equal (Author exercise)
<!-- id: so-all-equal -->

**Approach.** Emit the first element of the sorted array unconditionally, and for every later element emit it only when it differs from its predecessor. The test `i == 0` replaces any fabricated predecessor. A version that starts with a previous value of 0 fails on `[0, 0, 0]`, since the first zero looks like a repeat of the made-up start and the result is empty. The program checks the faulty version really fails, then checks that the correct version returns exactly one value for a run of any length from 1 to 20, for several values including the extremes, and that the empty array gives an empty result.

**Complexity.** O(n log n) time for the sort plus O(n) for the scan, with O(n) extra space.

```java run
import java.util.Arrays;

public final class AllEqual {
    static int[] distinct(int[] values) {
        int[] a = values.clone();
        Arrays.sort(a);
        int[] out = new int[a.length];
        int size = 0;
        for (int i = 0; i < a.length; i++) if (i == 0 || a[i] != a[i - 1]) out[size++] = a[i];
        return Arrays.copyOf(out, size);
    }
    static int[] faultySentinel(int[] values) {
        int[] a = values.clone();
        Arrays.sort(a);
        int[] out = new int[a.length];
        int size = 0, previous = 0;
        for (int x : a) {
            if (x != previous) out[size++] = x;
            previous = x;
        }
        return Arrays.copyOf(out, size);
    }

    public static void main(String[] args) {
        if (!Arrays.equals(distinct(new int[] {4, 4, 4}), new int[] {4})) throw new AssertionError("example 1");
        if (!Arrays.equals(distinct(new int[] {0, 0, 0}), new int[] {0})) throw new AssertionError("example 2");
        if (faultySentinel(new int[] {0, 0, 0}).length != 0) throw new AssertionError("the sentinel version loses the zeros");
        if (distinct(new int[0]).length != 0) throw new AssertionError("empty input");
        int[] samples = {0, 1, -1, Integer.MIN_VALUE, Integer.MAX_VALUE};
        for (int v : samples) {
            for (int k = 1; k <= 20; k++) {
                int[] run = new int[k];
                Arrays.fill(run, v);
                if (!Arrays.equals(distinct(run), new int[] {v})) throw new AssertionError("run of " + k + " copies of " + v);
            }
        }
        if (!Arrays.equals(distinct(new int[] {2, 0, 2, 0, 1}), new int[] {0, 1, 2})) throw new AssertionError("mixed values");
    }
}
```

#### Solution: [Recognize] Longest Word in Dictionary (LeetCode 720)
<!-- id: so-longest-buildable-word -->

**Approach.** Sort the words alphabetically. A word's prefix of one letter shorter sorts before it, so when a word is read, that prefix has already been judged. Keep a set of buildable words: a one-letter word is buildable, and a longer word is buildable when its prefix without the last letter is in the set. Track the best word, replacing it only when a buildable word is strictly longer, so among equal lengths the first one met in sorted order, the alphabetically smallest, is kept. The oracle checks every prefix of every word against the full word list, without sorting, and picks the longest and then the smallest.

**Complexity.** O(n log n) comparisons for the sort, each costing up to the word length L, plus O(n L) for the prefix checks; O(n L) extra space for the set.

```java run
import java.util.Arrays;
import java.util.HashSet;
import java.util.Random;
import java.util.Set;

public final class LongestBuildableWord {
    static String longestWord(String[] words) {
        String[] w = words.clone();
        Arrays.sort(w);
        Set<String> ok = new HashSet<>();
        String best = "";
        for (String s : w) {
            if (s.length() == 1 || ok.contains(s.substring(0, s.length() - 1))) {
                ok.add(s);
                if (s.length() > best.length()) best = s;
            }
        }
        return best;
    }
    static String oracle(String[] words) {
        Set<String> all = new HashSet<>(Arrays.asList(words));
        String best = "";
        for (String s : words) {
            boolean built = true;
            for (int len = 1; len < s.length() && built; len++) built = all.contains(s.substring(0, len));
            if (!built) continue;
            if (s.length() > best.length() || (s.length() == best.length() && s.compareTo(best) < 0)) best = s;
        }
        return best;
    }

    public static void main(String[] args) {
        if (!longestWord(new String[] {"cat", "c", "ca", "dog", "do", "d", "dot"}).equals("cat")) throw new AssertionError("example 1");
        if (!longestWord(new String[] {"xy", "xyz"}).isEmpty()) throw new AssertionError("example 2");
        Random rnd = new Random(563);
        String letters = "abc";
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(10);
            String[] w = new String[n];
            for (int i = 0; i < n; i++) {
                int len = 1 + rnd.nextInt(4);
                StringBuilder sb = new StringBuilder();
                for (int j = 0; j < len; j++) sb.append(letters.charAt(rnd.nextInt(letters.length())));
                w[i] = sb.toString();
            }
            if (!longestWord(w).equals(oracle(w))) throw new AssertionError("differs from the prefix oracle on " + Arrays.toString(w));
        }
    }
}
```
