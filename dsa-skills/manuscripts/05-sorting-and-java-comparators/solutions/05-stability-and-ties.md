<!-- solutions-for: 05-stability-and-ties -->
### Stability And Ties

#### Solution: [Build] Stable Score Sort (Author exercise)
<!-- id: so-stable-score-sort -->

**Approach.** Sort a copy of the list with `Comparator.comparingInt(Entry::score)`. Entries with equal scores compare as zero, and `List.sort` on objects is documented to be stable, so equal scores keep their input order. The oracle processes the distinct scores in ascending order and, for each, copies matching entries in input order, which is a direct statement of the requirement and does not rely on any sorting property. The test uses long arrays with many repeated scores and distinct names so that any reordering inside a tie would be visible.

**Complexity.** O(n log n) comparisons and O(n) extra space for the copy.

```java run
import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import java.util.Random;
import java.util.TreeSet;

public final class StableScoreSort {
    record Entry(String name, int score) {}

    static List<Entry> sortByScore(List<Entry> in) {
        List<Entry> out = new ArrayList<>(in);
        out.sort(Comparator.comparingInt(Entry::score));
        return out;
    }
    static List<Entry> oracle(List<Entry> in) {
        TreeSet<Integer> scores = new TreeSet<>();
        for (Entry e : in) scores.add(e.score());
        List<Entry> out = new ArrayList<>();
        for (int s : scores) for (Entry e : in) if (e.score() == s) out.add(e);
        return out;
    }

    public static void main(String[] args) {
        List<Entry> ex1 = sortByScore(List.of(new Entry("ann", 3), new Entry("bob", 1), new Entry("cy", 3), new Entry("di", 1)));
        if (!ex1.equals(List.of(new Entry("bob", 1), new Entry("di", 1), new Entry("ann", 3), new Entry("cy", 3)))) throw new AssertionError("example 1");
        List<Entry> same = List.of(new Entry("x", 2), new Entry("y", 2), new Entry("z", 2));
        if (!sortByScore(same).equals(same)) throw new AssertionError("example 2");
        Random rnd = new Random(541);
        for (int t = 0; t < 2000; t++) {
            int n = rnd.nextInt(120);
            List<Entry> in = new ArrayList<>();
            for (int i = 0; i < n; i++) in.add(new Entry("p" + i, rnd.nextInt(4)));
            if (!sortByScore(in).equals(oracle(in))) throw new AssertionError("a tie was reordered for n = " + n);
        }
    }
}
```

#### Solution: [Vary] Explicit Index Tie (Author exercise)
<!-- id: so-explicit-index-tie -->

**Approach.** Box the positions 0 to n minus 1 into an `Integer[]` and sort them with a comparator that compares the values at those positions and, when the values are equal, compares the positions themselves. The last key means the result is the same whatever the sorting algorithm does with ties. The oracle repeatedly selects the unused position with the smallest value, preferring the smaller position, which uses only loops. The test includes extreme ints and many duplicates.

**Complexity.** O(n log n) comparisons, with O(n) extra space for the boxed indices.

```java run
import java.util.Arrays;
import java.util.Random;

public final class ExplicitIndexTie {
    static int[] positionsByValue(int[] values) {
        Integer[] pos = new Integer[values.length];
        for (int i = 0; i < pos.length; i++) pos[i] = i;
        Arrays.sort(pos, (i, j) -> values[i] != values[j] ? Integer.compare(values[i], values[j]) : Integer.compare(i, j));
        int[] out = new int[pos.length];
        for (int i = 0; i < out.length; i++) out[i] = pos[i];
        return out;
    }
    static int[] oracle(int[] values) {
        boolean[] used = new boolean[values.length];
        int[] out = new int[values.length];
        for (int k = 0; k < out.length; k++) {
            int best = -1;
            for (int i = 0; i < values.length; i++) {
                if (used[i]) continue;
                if (best == -1 || values[i] < values[best]) best = i;
            }
            used[best] = true;
            out[k] = best;
        }
        return out;
    }

    public static void main(String[] args) {
        if (!Arrays.equals(positionsByValue(new int[] {30, 10, 30, 20, 10}), new int[] {1, 4, 3, 0, 2})) throw new AssertionError("example 1");
        if (!Arrays.equals(positionsByValue(new int[] {7}), new int[] {0})) throw new AssertionError("example 2");
        if (positionsByValue(new int[0]).length != 0) throw new AssertionError("empty input");
        if (!Arrays.equals(positionsByValue(new int[] {Integer.MAX_VALUE, Integer.MIN_VALUE, Integer.MAX_VALUE}), new int[] {1, 0, 2})) throw new AssertionError("extremes");
        Random rnd = new Random(542);
        for (int t = 0; t < 4000; t++) {
            int n = rnd.nextInt(14);
            int[] v = new int[n];
            for (int i = 0; i < n; i++) v[i] = rnd.nextInt(4) == 0 ? Integer.MIN_VALUE : rnd.nextInt(4);
            if (!Arrays.equals(positionsByValue(v), oracle(v))) throw new AssertionError("differs from the selection oracle on " + Arrays.toString(v));
        }
    }
}
```

#### Solution: [Boundary] Comparator Equality (Author exercise)
<!-- id: so-comparator-equality -->

**Approach.** `String.compareToIgnoreCase` returns zero for `"Bob"` and `"bob"`, which are different strings. A stable sort keeps their input order, so two orderings of the same words give two outputs, and a `TreeSet` treats a zero as "already present" and keeps only one. Adding `thenComparing(Comparator.naturalOrder())` makes the comparator return zero only for equal strings, which restores determinism and keeps both words in the set. The program checks all permutations of a small word list for the number of distinct outputs and checks the set sizes.

**Complexity.** The comparator costs time proportional to the word length, and a sort is O(n log n) comparisons; the permutation check is exponential and only for tiny tests.

```java run
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import java.util.TreeSet;

public final class ComparatorEquality {
    static final Comparator<String> LOOSE = String::compareToIgnoreCase;
    static final Comparator<String> REPAIRED = LOOSE.thenComparing(Comparator.naturalOrder());

    static void permute(List<String> a, int k, List<List<String>> out) {
        if (k == a.size()) { out.add(new ArrayList<>(a)); return; }
        for (int i = k; i < a.size(); i++) {
            Collections.swap(a, k, i);
            permute(a, k + 1, out);
            Collections.swap(a, k, i);
        }
    }
    static int distinctOutputs(List<String> words, Comparator<String> c) {
        List<List<String>> perms = new ArrayList<>();
        permute(new ArrayList<>(words), 0, perms);
        Set<List<String>> outs = new HashSet<>();
        for (List<String> p : perms) { List<String> s = new ArrayList<>(p); s.sort(c); outs.add(s); }
        return outs.size();
    }

    public static void main(String[] args) {
        if (LOOSE.compare("bob", "Bob") != 0) throw new AssertionError("the loose comparator ties different strings");
        if (REPAIRED.compare("bob", "Bob") == 0) throw new AssertionError("the repaired comparator separates them");
        List<String> words = List.of("bob", "Bob", "amy");
        if (distinctOutputs(words, LOOSE) < 2) throw new AssertionError("example 1: the loose output depends on input order");
        if (distinctOutputs(words, REPAIRED) != 1) throw new AssertionError("the repaired output is unique");
        TreeSet<String> loose = new TreeSet<>(LOOSE), repaired = new TreeSet<>(REPAIRED);
        loose.add("bob"); loose.add("Bob");
        repaired.add("bob"); repaired.add("Bob");
        if (loose.size() != 1) throw new AssertionError("example 2: the loose set drops a word");
        if (repaired.size() != 2) throw new AssertionError("the repaired set keeps both words");
        if (REPAIRED.compare("amy", "amy") != 0) throw new AssertionError("identical words still tie");
        List<String> sorted = new ArrayList<>(words);
        sorted.sort(REPAIRED);
        if (!sorted.equals(List.of("amy", "Bob", "bob"))) throw new AssertionError("uppercase sorts before lowercase in natural order");
    }
}
```

#### Solution: [Recognize] Sort Integers by The Number of 1 Bits (LeetCode 1356)
<!-- id: so-sort-by-bits -->

**Approach.** Box the values and sort them with `comparingInt(Integer::bitCount)` followed by `thenComparingInt` on the value itself, so the tie between two numbers with the same bit count is decided by an explicit second key. Because equal numbers are identical, no further tie rule is needed. The oracle counts bits with a shifting loop and picks the minimum of the remaining numbers under the pair (bits, value) at each round, so it uses neither the comparator nor `bitCount`.

**Complexity.** O(n log n) comparisons, each in O(1) for a 32-bit value; O(n) extra space for the boxed array.

```java run
import java.util.Arrays;
import java.util.Comparator;
import java.util.Random;

public final class SortByBits {
    static int[] byBitCount(int[] a) {
        Integer[] boxed = new Integer[a.length];
        for (int i = 0; i < a.length; i++) boxed[i] = a[i];
        Arrays.sort(boxed, Comparator.comparingInt(Integer::bitCount).thenComparingInt(x -> x));
        int[] out = new int[a.length];
        for (int i = 0; i < out.length; i++) out[i] = boxed[i];
        return out;
    }
    static int bits(int x) { int c = 0; while (x != 0) { c += x & 1; x >>>= 1; } return c; }
    static int[] oracle(int[] a) {
        boolean[] used = new boolean[a.length];
        int[] out = new int[a.length];
        for (int k = 0; k < out.length; k++) {
            int best = -1;
            for (int i = 0; i < a.length; i++) {
                if (used[i]) continue;
                if (best == -1 || bits(a[i]) < bits(a[best]) || (bits(a[i]) == bits(a[best]) && a[i] < a[best])) best = i;
            }
            used[best] = true;
            out[k] = a[best];
        }
        return out;
    }

    public static void main(String[] args) {
        if (!Arrays.equals(byBitCount(new int[] {5, 3, 8, 1, 6}), new int[] {1, 8, 3, 5, 6})) throw new AssertionError("example 1");
        if (!Arrays.equals(byBitCount(new int[] {0, 16, 15}), new int[] {0, 16, 15})) throw new AssertionError("example 2");
        if (Integer.bitCount(10000) != bits(10000)) throw new AssertionError("bit counters agree");
        Random rnd = new Random(543);
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(14);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(40);
            if (!Arrays.equals(byBitCount(a), oracle(a))) throw new AssertionError("differs from the oracle on " + Arrays.toString(a));
        }
    }
}
```
