<!-- solutions-for: 05-sorting-and-java-comparators -->
### Solutions For Sorted Runs

#### Solution: [Build] Contains Duplicate (LeetCode 217)
<!-- id: so-extra-copies -->

**Approach.**
The method sorts a copy and finds each run with an inner loop. A run of length `L` contributes `L - 1` extra copies, because exactly one position of the run must remain. The method adds `j - i - 1` for every run and returns the total. The invariant at the start of each outer step is that `extra` holds the extra copies of all runs left of `i`. The total equals `n` minus the number of distinct values.

**Complexity.**
- **Time** is O(n log n), because the sort dominates the linear scan of runs.
- **Space** is O(n), because of the sorted copy.

```java run
import java.util.*;

public final class ExtraCopies {
    /**
     * Returns the number of positions to delete so that all values are distinct.
     * Time: O(n log n). Space: O(n).
     * Invariant: at the start of each outer step, extra counts the extra copies left of i.
     */
    static int extraCopies(int[] nums) {
        int[] sorted = Arrays.copyOf(nums, nums.length);
        Arrays.sort(sorted);
        int extra = 0;
        int i = 0;
        // Each outer step handles one run, so the loops read each index once.
        while (i < sorted.length) {
            int j = i;
            while (j < sorted.length && sorted[j] == sorted[i]) j++;
            // All positions of the run except the first are extra.
            extra += j - i - 1;
            i = j;
        }
        return extra;
    }

    public static void main(String[] args) {
        // The statement examples and the empty input.
        if (extraCopies(new int[] {6, 2, 6, 6, 2, 9}) != 3) throw new AssertionError("example 1");
        if (extraCopies(new int[] {5, -5, 0}) != 0) throw new AssertionError("example 2");
        if (extraCopies(new int[0]) != 0) throw new AssertionError("empty");
        // Random arrays are checked against n minus the number of distinct values from a hash set.
        Random rnd = new Random(111);
        for (int t = 0; t < 500; t++) {
            int[] a = new int[rnd.nextInt(14)];
            for (int k = 0; k < a.length; k++) a[k] = rnd.nextInt(6) - 3;
            Set<Integer> distinct = new HashSet<>();
            for (int v : a) distinct.add(v);
            if (extraCopies(a) != a.length - distinct.size()) throw new AssertionError(Arrays.toString(a));
        }
    }
}
```

#### Solution: [Vary] Intersection Of Two Arrays (LeetCode 349)
<!-- id: so-common-values -->

**Approach.**
The method builds one array of `long` keys with the value doubled and the source tag added, so `2 * v` marks array `a` and `2 * v + 1` marks array `b`. The two keys of one value are adjacent after the sort, and keys of different values never interleave, because the doubled values differ by at least 2. The scan reads each run of equal values, using `Math.floorDiv(key, 2)` to recover the value, which is correct for negative values. A run is common when it holds both tags. The method emits one value per common run, and the runs come out in ascending order. The invariant is that every run left of the scan position was emitted once if and only if it held both tags.

**Complexity.**
- **Time** is O((n + m) log(n + m)), because the sort of the combined array dominates the linear scan.
- **Space** is O(n + m) for the combined keys and the answer.

```java run
import java.util.*;

public final class CommonValues {
    /**
     * Returns the values present in both arrays, once each, in ascending order.
     * Time: O((n + m) log(n + m)). Space: O(n + m).
     * Invariant: every value left of the scan position was emitted once if both sources held it.
     */
    static int[] common(int[] a, int[] b) {
        long[] keys = new long[a.length + b.length];
        // The doubled value keeps different values apart, and the added tag names the source.
        for (int i = 0; i < a.length; i++) keys[i] = 2L * a[i];
        for (int i = 0; i < b.length; i++) keys[a.length + i] = 2L * b[i] + 1;
        Arrays.sort(keys);
        List<Integer> out = new ArrayList<>();
        int i = 0;
        // Each outer step reads one run of one value.
        while (i < keys.length) {
            long value = Math.floorDiv(keys[i], 2);
            boolean inA = false, inB = false;
            int j = i;
            while (j < keys.length && Math.floorDiv(keys[j], 2) == value) {
                if (Math.floorMod(keys[j], 2) == 0) inA = true; else inB = true;
                j++;
            }
            // A value is common when its run holds both tags.
            if (inA && inB) out.add((int) value);
            i = j;
        }
        int[] res = new int[out.size()];
        for (int k = 0; k < res.length; k++) res[k] = out.get(k);
        return res;
    }

    public static void main(String[] args) {
        // The statement examples and the empty inputs.
        if (!Arrays.equals(common(new int[] {8, 3, 8, -1}, new int[] {3, 8, 8, 0}), new int[] {3, 8})) throw new AssertionError("example 1");
        if (!Arrays.equals(common(new int[] {-2, -2}, new int[] {-2, 5}), new int[] {-2})) throw new AssertionError("example 2");
        if (common(new int[0], new int[] {1}).length != 0) throw new AssertionError("empty");
        // Java fact from the lesson: floorDiv and floorMod keep negative keys in the right run.
        if (Math.floorDiv(-3L, 2) != -2 || (-3L) / 2 != -1) throw new AssertionError("floorDiv");
        // Extreme values must not overflow the key.
        if (!Arrays.equals(common(new int[] {Integer.MIN_VALUE, Integer.MAX_VALUE}, new int[] {Integer.MAX_VALUE}), new int[] {Integer.MAX_VALUE})) throw new AssertionError("extreme");
        // Random arrays are checked against a hash-set oracle that is sorted afterward.
        Random rnd = new Random(112);
        for (int t = 0; t < 500; t++) {
            int[] a = new int[rnd.nextInt(8)], b = new int[rnd.nextInt(8)];
            for (int k = 0; k < a.length; k++) a[k] = rnd.nextInt(7) - 3;
            for (int k = 0; k < b.length; k++) b[k] = rnd.nextInt(7) - 3;
            TreeSet<Integer> expect = new TreeSet<>();
            Set<Integer> inB = new HashSet<>();
            for (int y : b) inB.add(y);
            for (int x : a) if (inB.contains(x)) expect.add(x);
            int[] want = new int[expect.size()];
            int p = 0;
            for (int v : expect) want[p++] = v;
            if (!Arrays.equals(common(a, b), want)) throw new AssertionError(Arrays.toString(a) + Arrays.toString(b));
        }
    }
}
```

#### Solution: [Boundary] All Equal (Author exercise)
<!-- id: so-distinct-ascending -->

**Approach.**
The method sorts a copy and reads it run by run. For each run, it appends the value at the first index of the run. The inner loop stops at the array boundary, so the last run ends there and needs no later value. The invariant at the start of each outer step is that the output holds the distinct values left of `i`, in ascending order, once each. The harness covers the empty array, one value, an all-equal array, and the extreme values.

**Complexity.**
- **Time** is O(n log n), because the sort dominates the linear scan.
- **Space** is O(n) for the sorted copy and the output.

```java run
import java.util.*;

public final class DistinctAscending {
    /**
     * Returns the distinct values of nums in ascending order.
     * Time: O(n log n). Space: O(n).
     * Invariant: at the start of each outer step, out holds the distinct values left of i.
     */
    static int[] distinctAscending(int[] nums) {
        int[] sorted = Arrays.copyOf(nums, nums.length);
        Arrays.sort(sorted);
        int[] out = new int[sorted.length];
        int size = 0;
        int i = 0;
        // Each outer step handles one run.
        while (i < sorted.length) {
            int j = i;
            // The boundary test comes first, so the last run ends at the array end.
            while (j < sorted.length && sorted[j] == sorted[i]) j++;
            // One representative stands for the run.
            out[size++] = sorted[i];
            i = j;
        }
        return Arrays.copyOf(out, size);
    }

    public static void main(String[] args) {
        // The statement examples and the small inputs.
        if (!Arrays.equals(distinctAscending(new int[] {4, 4, 4}), new int[] {4})) throw new AssertionError("example 1");
        if (!Arrays.equals(distinctAscending(new int[] {Integer.MAX_VALUE, Integer.MIN_VALUE, Integer.MAX_VALUE}), new int[] {Integer.MIN_VALUE, Integer.MAX_VALUE})) throw new AssertionError("example 2");
        if (distinctAscending(new int[0]).length != 0) throw new AssertionError("empty");
        if (!Arrays.equals(distinctAscending(new int[] {9}), new int[] {9})) throw new AssertionError("singleton");
        // Random arrays are checked against a TreeSet oracle.
        Random rnd = new Random(113);
        for (int t = 0; t < 500; t++) {
            int[] a = new int[rnd.nextInt(12)];
            for (int k = 0; k < a.length; k++) a[k] = rnd.nextInt(4) == 0 ? Integer.MIN_VALUE : rnd.nextInt(5) - 2;
            TreeSet<Integer> set = new TreeSet<>();
            for (int v : a) set.add(v);
            int[] want = new int[set.size()];
            int p = 0;
            for (int v : set) want[p++] = v;
            if (!Arrays.equals(distinctAscending(a), want)) throw new AssertionError(Arrays.toString(a));
        }
    }
}
```

#### Solution: [Recognize] Longest Word In Dictionary (LeetCode 720)
<!-- id: so-buildable-word -->

**Approach.**
The method sorts a copy of the words alphabetically. In that order, every prefix of a word comes before the word, so one pass can decide buildability. A hash set holds the buildable words found so far. A word is buildable when it has one letter, or when its prefix without the last letter is in that set. The scan keeps the best word and replaces it only when a buildable word is strictly longer, so among equal lengths the alphabetically first word stays. The invariant after each word is that the set holds exactly the buildable words among the words read so far, and `best` is the longest of them, with the alphabetically first word on ties.

**Complexity.**
- **Time** is O(n log n * m + n * m), where m is the longest word, because the sort compares words of length up to m and each prefix lookup hashes up to m characters.
- **Space** is O(n * m) for the sorted copy and the set.

```java run
import java.util.*;

public final class BuildableWord {
    /**
     * Returns the longest buildable word, the alphabetically first on a tie, or "" when there are no words.
     * Time: O(n log n * m). Space: O(n * m).
     * Invariant: built holds the buildable words read so far, and best is the longest of them.
     */
    static String longestWord(String[] words) {
        String[] sorted = words.clone();
        Arrays.sort(sorted);
        Set<String> built = new HashSet<>();
        String best = "";
        // Prefixes sort before their words, so each prefix is decided before the word that needs it.
        for (String w : sorted) {
            if (w.length() == 1 || built.contains(w.substring(0, w.length() - 1))) {
                built.add(w);
                // Strict comparison keeps the alphabetically first word among equal lengths.
                if (w.length() > best.length()) best = w;
            }
        }
        return best;
    }

    /** Oracle: checks every prefix of every word directly. */
    static String brute(String[] words) {
        Set<String> all = new HashSet<>(Arrays.asList(words));
        String best = "";
        for (String w : words) {
            boolean ok = true;
            for (int len = 1; len < w.length(); len++) if (!all.contains(w.substring(0, len))) ok = false;
            if (ok && (w.length() > best.length() || (w.length() == best.length() && w.compareTo(best) < 0))) best = w;
        }
        return best;
    }

    public static void main(String[] args) {
        // The statement examples and the empty input.
        if (!longestWord(new String[] {"t", "ta", "tan", "tank", "tab", "x", "xyz"}).equals("tank")) throw new AssertionError("example 1");
        if (!longestWord(new String[] {"m", "mo", "ma", "mop"}).equals("mop")) throw new AssertionError("example 2");
        if (!longestWord(new String[0]).equals("")) throw new AssertionError("empty");
        // Random dictionaries over two letters are checked against the prefix-checking oracle.
        Random rnd = new Random(114);
        for (int t = 0; t < 600; t++) {
            String[] w = new String[rnd.nextInt(9)];
            for (int k = 0; k < w.length; k++) {
                StringBuilder sb = new StringBuilder();
                for (int len = 1 + rnd.nextInt(4); len > 0; len--) sb.append((char) ('a' + rnd.nextInt(2)));
                w[k] = sb.toString();
            }
            if (!longestWord(w).equals(brute(w))) throw new AssertionError(Arrays.toString(w));
        }
    }
}
```
