<!-- solutions-for: 05-query-objects -->
### Solutions For Query Objects

#### Solution: [Build] Shortest Word Distance II (LeetCode 244)
<!-- id: it37-query-objects-word-distance -->

**Approach.**
The constructor groups the indices of equal words into sorted arrays, one array per word. A query for two different words runs the merge walk. The walk compares the indices under two cursors, records their gap, and advances the cursor with the smaller index. The invariant is that every pair with both indices before the cursors was either compared or has a larger gap than a compared pair, because the skipped index could only meet larger indices of the other list.

A query for the same word cannot use the merge walk, because the walk would pair an index with itself and report 0. The two closest distinct occurrences of one word are adjacent in its sorted list, so the method returns the smallest difference between neighbors, or -1 for fewer than two entries. An absent word returns -1. The harness compares every answer with a double loop over the text on random texts drawn from a small alphabet, which produces repeated words and absent words.

**Complexity.**
- **Time** is O(n) expected for the constructor and O(a + b) per query for lists of lengths `a` and `b`, or O(a) for equal words.
- **Space** is O(n) for the lists, which together hold one index per input word.

```java run
import java.util.HashMap;
import java.util.Map;
import java.util.Random;

public final class WordIndexBuild {
    /** Position lists per word with a merge walk for pairs and a neighbor scan for equal words. */
    static final class WordIndex {
        private final Map<String, int[]> positions = new HashMap<>();

        /**
         * Builds the lists in two passes so each array has its exact size.
         * Time: O(n) expected. Space: O(n).
         * Invariant: each list holds the indices of one word in increasing order.
         */
        WordIndex(String[] words) {
            // The first pass counts the occurrences of each word.
            Map<String, Integer> counts = new HashMap<>();
            for (String w : words) counts.merge(w, 1, Integer::sum);
            // The second pass writes indices in increasing order into arrays of the exact size.
            Map<String, Integer> filled = new HashMap<>();
            for (int i = 0; i < words.length; i++) {
                int[] list = positions.computeIfAbsent(words[i], w -> new int[counts.get(w)]);
                int slot = filled.merge(words[i], 1, Integer::sum) - 1;
                list[slot] = i;
            }
        }

        /**
         * Returns the smallest gap between distinct indices holding the two words, or -1.
         * Time: O(a + b). Space: O(1).
         * Invariant: the cursor with the smaller index cannot form a closer pair with a later index of the other list.
         */
        int shortest(String a, String b) {
            int[] pa = positions.get(a), pb = positions.get(b);
            // An absent word has no occurrence to pair.
            if (pa == null || pb == null) return -1;
            int best = Integer.MAX_VALUE;
            if (a.equals(b)) {
                // Equal words: the closest distinct pair is a pair of neighbors in the single list.
                for (int i = 1; i < pa.length; i++) best = Math.min(best, pa[i] - pa[i - 1]);
                return best == Integer.MAX_VALUE ? -1 : best;
            }
            int i = 0, j = 0;
            // Each iteration advances one cursor, so the loop runs at most a + b times.
            while (i < pa.length && j < pb.length) {
                best = Math.min(best, Math.abs(pa[i] - pb[j]));
                // The smaller index moves, because the other cursor already gives its best partner.
                if (pa[i] < pb[j]) i++; else j++;
            }
            return best;
        }
    }

    /** Reference: checks every pair of indices. Time: O(n^2) per query. */
    static int oracle(String[] words, String a, String b) {
        int best = Integer.MAX_VALUE;
        // The double loop covers every ordered pair of distinct indices.
        for (int i = 0; i < words.length; i++)
            for (int j = 0; j < words.length; j++)
                if (i != j && words[i].equals(a) && words[j].equals(b)) best = Math.min(best, Math.abs(i - j));
        return best == Integer.MAX_VALUE ? -1 : best;
    }

    public static void main(String[] args) {
        // Example 1 from the exercise, including equal words and an absent word.
        String[] w1 = {"go", "to", "the", "store", "go", "to", "bed", "go"};
        WordIndex a = new WordIndex(w1);
        int[] got = {a.shortest("go", "to"), a.shortest("store", "bed"), a.shortest("go", "go"), a.shortest("bed", "bed"), a.shortest("go", "zoo")};
        if (!java.util.Arrays.equals(got, new int[] {1, 3, 3, -1, -1})) throw new AssertionError("example 1 " + java.util.Arrays.toString(got));
        // Example 2 and an empty input.
        WordIndex b = new WordIndex(new String[] {"x", "y"});
        if (b.shortest("y", "x") != 1 || b.shortest("x", "x") != -1) throw new AssertionError("example 2");
        WordIndex empty = new WordIndex(new String[0]);
        if (empty.shortest("a", "b") != -1) throw new AssertionError("empty");
        // Random texts over a four-letter alphabet are compared with the double loop for every pair of query words.
        Random rnd = new Random(3751L);
        String[] alphabet = {"a", "b", "c", "d", "e"};
        for (int t = 0; t < 2000; t++) {
            String[] words = new String[rnd.nextInt(14)];
            for (int i = 0; i < words.length; i++) words[i] = alphabet[rnd.nextInt(4)];
            WordIndex real = new WordIndex(words);
            for (String x : alphabet)
                for (String y : alphabet)
                    if (real.shortest(x, y) != oracle(words, x, y)) throw new AssertionError("pair " + x + y);
        }
    }
}
```

#### Solution: [Vary] Dot Product of Two Sparse Vectors (LeetCode 1570)
<!-- id: it37-query-objects-sparse-dot -->

**Approach.**
The constructor keeps two parallel arrays, the indices of the nonzero entries and their values, in increasing index order. A zero entry contributes nothing to any dot product, so dropping it loses no information the query needs. The method `dot` walks the two index arrays with one cursor each. Equal indices contribute the product, and the cursor with the smaller index moves. An index that exists in only one vector never meets an equal index. It contributes nothing, which matches the rule that missing entries count as zero.

Each product widens one factor to `long` first. Two values near 10^6 give a product near 10^12, which overflows `int`. The harness compares the result with a dense loop over the shorter length on random vectors with many zeros and different lengths.

**Complexity.**
- **Time** is O(n) for the constructor and O(p + q) per `dot` for `p` and `q` nonzero entries, which can be far below the vector lengths.
- **Space** is O(p) for a vector with `p` nonzero entries.

```java run
import java.util.Random;

public final class SparseVecVary {
    /** Vector that stores only the nonzero entries as parallel index and value arrays. */
    static final class SparseVec {
        private final int[] idx;
        private final int[] val;

        /**
         * Keeps the nonzero entries of nums.
         * Time: O(n). Space: O(p) for p nonzero entries.
         * Invariant: idx is strictly increasing and val[k] is the entry at idx[k].
         */
        SparseVec(int[] nums) {
            // The first pass counts the nonzero entries so the arrays have the exact size.
            int p = 0;
            for (int x : nums) if (x != 0) p++;
            idx = new int[p];
            val = new int[p];
            // The second pass copies each nonzero entry in index order.
            int k = 0;
            for (int i = 0; i < nums.length; i++) {
                if (nums[i] != 0) { idx[k] = i; val[k] = nums[i]; k++; }
            }
        }

        /**
         * Returns the dot product with another vector, treating missing entries as zero.
         * Time: O(p + q). Space: O(1).
         * Invariant: every common index below the cursors has already been added to the sum.
         */
        long dot(SparseVec other) {
            long sum = 0;
            int i = 0, j = 0;
            // Each iteration advances at least one cursor, so the loop runs at most p + q times.
            while (i < idx.length && j < other.idx.length) {
                if (idx[i] == other.idx[j]) {
                    // Widening one factor first keeps the product in long.
                    sum += (long) val[i] * other.val[j];
                    i++;
                    j++;
                } else if (idx[i] < other.idx[j]) {
                    // This index has no partner in the other vector.
                    i++;
                } else {
                    j++;
                }
            }
            return sum;
        }
    }

    /** Reference: multiplies dense arrays over the shorter length. Time: O(min(n, m)). */
    static long oracle(int[] a, int[] b) {
        long sum = 0;
        // Indices beyond the shorter array contribute zero, so the loop stops there.
        for (int i = 0; i < Math.min(a.length, b.length); i++) sum += (long) a[i] * b[i];
        return sum;
    }

    public static void main(String[] args) {
        // Example 1 and Example 2 from the exercise.
        if (new SparseVec(new int[] {1, 0, 0, 2, 3}).dot(new SparseVec(new int[] {0, 3, 0, 4, 0})) != 8) throw new AssertionError("example 1");
        if (new SparseVec(new int[] {2, 0, -5}).dot(new SparseVec(new int[] {4, 7})) != 8) throw new AssertionError("example 2");
        // Empty vectors and an all-zero vector give 0.
        if (new SparseVec(new int[0]).dot(new SparseVec(new int[] {1, 2})) != 0) throw new AssertionError("empty");
        if (new SparseVec(new int[] {0, 0}).dot(new SparseVec(new int[] {5, 5})) != 0) throw new AssertionError("zeros");
        // Two entries of 10^6 give 10^12, which does not fit in an int.
        if (new SparseVec(new int[] {1_000_000}).dot(new SparseVec(new int[] {1_000_000})) != 1_000_000_000_000L) throw new AssertionError("long product");
        // Random sparse vectors of different lengths are compared with the dense loop.
        Random rnd = new Random(3752L);
        for (int t = 0; t < 4000; t++) {
            int[] a = new int[rnd.nextInt(12)];
            int[] b = new int[rnd.nextInt(12)];
            for (int i = 0; i < a.length; i++) a[i] = rnd.nextInt(3) == 0 ? rnd.nextInt(2_000_001) - 1_000_000 : 0;
            for (int i = 0; i < b.length; i++) b[i] = rnd.nextInt(3) == 0 ? rnd.nextInt(2_000_001) - 1_000_000 : 0;
            if (new SparseVec(a).dot(new SparseVec(b)) != oracle(a, b)) throw new AssertionError("random");
        }
    }
}
```

#### Solution: [Boundary] Unique Word Abbreviation (LeetCode 288)
<!-- id: it37-query-objects-abbreviation -->

**Approach.**
The constructor maps each abbreviation to the set of distinct dictionary words that produce it. Because the group is a set, a word repeated in the dictionary appears once. The method `conflicts` computes the abbreviation of the query word and looks up its group. The answer is the group size, minus one when the group contains the query word itself, because a word never conflicts with itself. An abbreviation with no group gives 0.

The invariant is that the group of an abbreviation holds exactly the distinct dictionary words with that abbreviation. Words of one or two letters abbreviate to themselves, so their group holds only that same word, and the conflict count is always 0. The harness compares the result with a scan over the distinct dictionary words on random dictionaries with many shared first and last letters.

**Complexity.**
- **Time** is O(total letters) expected for the constructor and O(L) expected per query, because one abbreviation and one set lookup cost O(L).
- **Space** is O(total letters) for the stored distinct words.

```java run
import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Random;
import java.util.Set;

public final class AbbrDictionaryBoundary {
    /** Maps each abbreviation to the distinct dictionary words that share it. */
    static final class AbbrDictionary {
        private final Map<String, Set<String>> groups = new HashMap<>();

        static String abbr(String w) {
            // Words of at most two letters keep their own spelling.
            if (w.length() <= 2) return w;
            // Longer words keep the outer letters and the count of letters between them.
            return w.charAt(0) + String.valueOf(w.length() - 2) + w.charAt(w.length() - 1);
        }

        /**
         * Groups the dictionary words by abbreviation.
         * Time: O(total letters) expected. Space: O(total letters).
         * Invariant: each set holds the distinct words of one abbreviation.
         */
        AbbrDictionary(String[] dictionary) {
            // A set per abbreviation drops repeated dictionary words.
            for (String w : dictionary) groups.computeIfAbsent(abbr(w), k -> new HashSet<>()).add(w);
        }

        /**
         * Counts the distinct dictionary words with the same abbreviation that differ from the query word.
         * Time: O(L) expected. Space: O(1).
         * Invariant: the query word is subtracted once, and only when the group contains it.
         */
        int conflicts(String word) {
            Set<String> group = groups.get(abbr(word));
            // No word has this abbreviation.
            if (group == null) return 0;
            // The query word is part of the group when the dictionary contains it, and it is not a conflict.
            return group.size() - (group.contains(word) ? 1 : 0);
        }
    }

    /** Reference: scans the distinct words of the dictionary. Time: O(n) per query. */
    static int oracle(String[] dictionary, String word) {
        Set<String> distinct = new HashSet<>(java.util.Arrays.asList(dictionary));
        int count = 0;
        // Every distinct word is tested against the query word.
        for (String d : distinct) if (!d.equals(word) && AbbrDictionary.abbr(d).equals(AbbrDictionary.abbr(word))) count++;
        return count;
    }

    public static void main(String[] args) {
        // Example 1 from the exercise.
        AbbrDictionary a = new AbbrDictionary(new String[] {"deer", "door", "cake", "card"});
        int[] got = {a.conflicts("dear"), a.conflicts("deer"), a.conflicts("cart"), a.conflicts("cake")};
        if (!java.util.Arrays.equals(got, new int[] {2, 1, 0, 0})) throw new AssertionError("example 1 " + java.util.Arrays.toString(got));
        // Example 2: a repeated dictionary word counts once.
        AbbrDictionary b = new AbbrDictionary(new String[] {"abc", "adc", "abc"});
        int[] got2 = {b.conflicts("abc"), b.conflicts("ac"), b.conflicts("axc")};
        if (!java.util.Arrays.equals(got2, new int[] {1, 0, 2})) throw new AssertionError("example 2 " + java.util.Arrays.toString(got2));
        // An empty dictionary and short words never conflict.
        if (new AbbrDictionary(new String[0]).conflicts("hello") != 0) throw new AssertionError("empty");
        if (new AbbrDictionary(new String[] {"it", "it", "aa"}).conflicts("it") != 0) throw new AssertionError("short words");
        // Random dictionaries over a three-letter alphabet are compared with the scan.
        Random rnd = new Random(3753L);
        String letters = "abc";
        for (int t = 0; t < 3000; t++) {
            String[] dict = new String[rnd.nextInt(8)];
            for (int i = 0; i < dict.length; i++) dict[i] = randomWord(rnd, letters);
            AbbrDictionary real = new AbbrDictionary(dict);
            for (int q = 0; q < 10; q++) {
                String w = randomWord(rnd, letters);
                if (real.conflicts(w) != oracle(dict, w)) throw new AssertionError("conflicts " + w);
            }
        }
    }

    static String randomWord(Random rnd, String letters) {
        // Lengths 1 to 5 cover words that abbreviate to themselves and words that do not.
        StringBuilder sb = new StringBuilder();
        for (int n = 1 + rnd.nextInt(5); n > 0; n--) sb.append(letters.charAt(rnd.nextInt(letters.length())));
        return sb.toString();
    }
}
```

#### Solution: [Recognize] Range Frequency Queries (LeetCode 2080)
<!-- id: it37-query-objects-range-frequency -->

**Approach.**
The constructor stores, for each value, the sorted array of indices where it occurs. A query first cuts the range to the array, so `left` becomes `max(left, 0)` and `right` becomes `min(right, n - 1)`. An empty range after the cut returns 0. Otherwise the answer is the lower bound of `right + 1` minus the lower bound of `left` in the position list of the value. The lower bound of `left` counts the positions before the range. The lower bound of `right + 1` counts the positions up to the end of the range. The difference counts the positions inside. An absent value has no list and returns 0.

The invariant is that every list is strictly increasing, so a lower bound splits it into the positions below the target and the positions at or above it. The cut also prevents overflow, because after it `right + 1` is at most `n`. The harness compares the class with a linear count on random arrays and on ranges that start below 0, end beyond the array or have `left > right`.

**Complexity.**
- **Time** is O(n) expected for the constructor and O(log k) per query for `k` occurrences of the value.
- **Space** is O(n), because the lists together hold one index per array element.

```java run
import java.util.HashMap;
import java.util.Map;
import java.util.Random;

public final class RangeFreqRecognize {
    /** Position lists per value with two lower-bound searches per query. */
    static final class RangeFreq {
        private final Map<Integer, int[]> positions = new HashMap<>();
        private final int n;

        /**
         * Builds the sorted position list of every value.
         * Time: O(n) expected. Space: O(n).
         * Invariant: each list holds the indices of one value in increasing order.
         */
        RangeFreq(int[] arr) {
            n = arr.length;
            // The first pass counts how many times each value occurs.
            Map<Integer, Integer> counts = new HashMap<>();
            for (int x : arr) counts.merge(x, 1, Integer::sum);
            // The second pass fills arrays of the exact size in increasing index order.
            Map<Integer, Integer> filled = new HashMap<>();
            for (int i = 0; i < n; i++) {
                int[] list = positions.computeIfAbsent(arr[i], v -> new int[counts.get(v)]);
                list[filled.merge(arr[i], 1, Integer::sum) - 1] = i;
            }
        }

        /** First index of sorted whose element is at least target. Time: O(log k). Space: O(1). */
        private static int lowerBound(int[] sorted, int target) {
            int lo = 0, hi = sorted.length;
            // The answer stays inside [lo, hi] and the window halves each iteration.
            while (lo < hi) {
                int mid = (lo + hi) >>> 1;
                if (sorted[mid] < target) lo = mid + 1; else hi = mid;
            }
            return lo;
        }

        /**
         * Counts the indices in the cut range that hold the value.
         * Time: O(log k). Space: O(1).
         * Invariant: lowerBound(right + 1) - lowerBound(left) is the number of positions in [left, right].
         */
        int query(int left, int right, int value) {
            // Cutting the range to the array also keeps right + 1 from overflowing.
            int l = Math.max(left, 0), r = Math.min(right, n - 1);
            if (l > r) return 0;
            int[] list = positions.get(value);
            // A value that never occurs has no list.
            if (list == null) return 0;
            // Two lower bounds bracket the positions inside the range.
            return lowerBound(list, r + 1) - lowerBound(list, l);
        }
    }

    /** Reference: counts matching elements inside the cut range. Time: O(n) per query. */
    static int oracle(int[] arr, int left, int right, int value) {
        int c = 0;
        // Only indices that are both in the array and in the range are counted.
        for (int i = 0; i < arr.length; i++) if (i >= left && i <= right && arr[i] == value) c++;
        return c;
    }

    public static void main(String[] args) {
        // Example 1 from the exercise, with ranges that leave the array and an empty range.
        int[] arr = {12, 33, 4, 56, 22, 2, 34, 33, 22, 12, 34, 56};
        RangeFreq a = new RangeFreq(arr);
        int[] got = {a.query(1, 2, 4), a.query(0, 11, 33), a.query(-5, 3, 12), a.query(8, 100, 22), a.query(5, 2, 33)};
        if (!java.util.Arrays.equals(got, new int[] {1, 2, 1, 1, 0})) throw new AssertionError("example 1 " + java.util.Arrays.toString(got));
        // Example 2: a range wholly beyond the array is empty after the cut.
        RangeFreq b = new RangeFreq(new int[] {7, 7, 7});
        if (b.query(0, 2, 7) != 3 || b.query(1, 1, 7) != 1 || b.query(3, 5, 7) != 0) throw new AssertionError("example 2");
        // Extreme bounds do not overflow.
        if (b.query(Integer.MIN_VALUE, Integer.MAX_VALUE, 7) != 3) throw new AssertionError("extreme bounds");
        // Random arrays with few distinct values are compared with the linear count.
        Random rnd = new Random(3754L);
        for (int t = 0; t < 3000; t++) {
            int[] x = new int[1 + rnd.nextInt(12)];
            for (int i = 0; i < x.length; i++) x[i] = rnd.nextInt(4) - 1;
            RangeFreq real = new RangeFreq(x);
            for (int q = 0; q < 25; q++) {
                int l = rnd.nextInt(18) - 3, r = rnd.nextInt(18) - 3, v = rnd.nextInt(6) - 2;
                if (real.query(l, r, v) != oracle(x, l, r, v)) throw new AssertionError("query " + l + " " + r + " " + v);
            }
        }
    }
}
```
