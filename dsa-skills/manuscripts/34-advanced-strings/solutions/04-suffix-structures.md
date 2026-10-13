<!-- solutions-for: 04-suffix-structures -->
### Solutions For Sorting And Comparing Suffixes

#### Solution: [Build] Sort Small Suffixes (Author exercise)
<!-- id: as-sort-small-suffixes -->

**Approach.**
The solution sorts the start indexes instead of copied suffixes. A rank array holds, for every start index, the order of its suffix by the first `k` characters, and the first rank is the character code. Each round sorts the indexes by the pair of `rank[i]` and `rank[i + k]`. The second value is -1 when `i + k` is past the end, so a suffix that ends early sorts first. The new ranks are assigned by walking the sorted order and adding 1 whenever the pair changes. The invariant is that after a round, equal ranks mean equal first `2k` characters and a smaller rank means a smaller `2k`-character prefix. Once all ranks are distinct, the sorted index order is the answer. The test compares every result with the copying method on random strings. It checks that the copied suffixes hold `n * (n + 1) / 2` characters. It also shows that `substring(1)` returns a new object on every call.

**Complexity.**
- **Time** is O(n log^2 n), because there are at most `ceil(log2 n) + 1` rounds and each round sorts `n` indexes with O(1) comparisons.
- **Space** is O(n), because the order, rank and next-rank arrays each hold `n` integers and no suffix is copied.

```java run
import java.util.*;

public final class SortSmallSuffixes {
    /**
     * Returns the start indexes of all suffixes in increasing lexicographic order.
     * Time: O(n log^2 n), because each doubling round sorts n indexes in O(n log n).
     * Space: O(n), because only integer arrays of length n are allocated.
     * Invariant: after the round with step k, equal rank means equal first 2k characters.
     */
    static int[] byDoubling(String s) {
        // n is read once; every loop below is bounded by it.
        int n = s.length();
        // order holds start indexes and is the array being sorted (boxed because the comparator needs Integer).
        Integer[] order = new Integer[n];
        // rank[i] orders suffix i by its first k characters; it starts as the character code.
        int[] rank = new int[n];
        // next receives the new ranks so the comparator keeps reading the old ones.
        int[] next = new int[n];
        // One pass seeds the identity order and the first-character ranks.
        for (int i = 0; i < n; i++) {
            // Every start index begins in its own slot.
            order[i] = i;
            // The character code orders suffixes by one character, matching String.compareTo.
            rank[i] = s.charAt(i);
        }
        // The step doubles each round; the break below ends the loop once all ranks differ.
        for (int k = 1; n > 0; k <<= 1) {
            // A lambda may capture only effectively final variables, so the step is copied.
            final int step = k;
            // The comparator reads two ranks per index and never touches a character.
            Comparator<Integer> byPair = (a, b) -> {
                // A different first half decides the order at once.
                if (rank[a] != rank[b]) return Integer.compare(rank[a], rank[b]);
                // A suffix with no second half uses -1, which sorts before every real rank.
                int ra = a + step < n ? rank[a + step] : -1;
                // The same rule applies to the other index.
                int rb = b + step < n ? rank[b + step] : -1;
                // Equal first halves are settled by the second halves.
                return Integer.compare(ra, rb);
            };
            // TimSort on n elements makes O(n log n) comparisons of O(1) each.
            Arrays.sort(order, byPair);
            // The smallest suffix gets rank 0.
            next[order[0]] = 0;
            // Walking the sorted order assigns ranks in a single pass.
            for (int t = 1; t < n; t++) {
                // The rank grows only when the pair differs from the previous pair.
                int bump = byPair.compare(order[t - 1], order[t]) < 0 ? 1 : 0;
                // Equal pairs share one rank, which is what keeps the invariant exact.
                next[order[t]] = next[order[t - 1]] + bump;
            }
            // Copying publishes the new ranks for the following round.
            System.arraycopy(next, 0, rank, 0, n);
            // Rank n - 1 at the end means no two suffixes tie, so the order is final.
            if (rank[order[n - 1]] == n - 1) break;
        }
        // The result unboxes the final order into the return array.
        int[] sa = new int[n];
        // One copy loop of n steps.
        for (int r = 0; r < n; r++) sa[r] = order[r];
        // Callers read the start of the r-th smallest suffix as sa[r].
        return sa;
    }

    /**
     * Brute-force oracle that copies and sorts every suffix.
     * Time: O(n^2 log n) comparisons of copied strings.
     * Space: O(n^2) characters.
     */
    static int[] oracle(String s) {
        // The list holds one copy per suffix, which is the cost the solution avoids.
        List<String> copies = new ArrayList<>();
        // Each substring call copies n - i characters.
        for (int i = 0; i < s.length(); i++) copies.add(s.substring(i));
        // Natural order of String is lexicographic by UTF-16 code unit.
        Collections.sort(copies);
        // The start of a suffix is the string length minus the copy length.
        int[] sa = new int[s.length()];
        // One recovery step per sorted copy.
        for (int r = 0; r < sa.length; r++) sa[r] = s.length() - copies.get(r).length();
        // The oracle answer is compared with the doubling answer in main.
        return sa;
    }

    public static void main(String[] args) {
        // Both examples from the problem text.
        if (!Arrays.equals(byDoubling("banana"), new int[] {5, 3, 1, 0, 4, 2})) throw new AssertionError("banana");
        if (!Arrays.equals(byDoubling("abab"), new int[] {2, 0, 3, 1})) throw new AssertionError("abab");
        // Empty and one-character inputs are the smallest boundaries.
        if (byDoubling("").length != 0) throw new AssertionError("empty");
        if (!Arrays.equals(byDoubling("q"), new int[] {0})) throw new AssertionError("single");
        // Seeded random strings over a tiny alphabet force long shared prefixes.
        Random rng = new Random(34_04_01L);
        for (int trial = 0; trial < 3000; trial++) {
            // Length 0 to 40 covers empty and repeated-letter shapes.
            int len = rng.nextInt(41);
            // The alphabet size varies from 1 to 3 letters.
            int alpha = 1 + rng.nextInt(3);
            StringBuilder sb = new StringBuilder();
            // Each position takes a random letter.
            for (int i = 0; i < len; i++) sb.append((char) ('a' + rng.nextInt(alpha)));
            String s = sb.toString();
            // The doubling result must equal the copying result.
            if (!Arrays.equals(byDoubling(s), oracle(s))) throw new AssertionError("mismatch " + s);
        }
        // The copies hold n(n+1)/2 characters in total, the memory claim in the Approach.
        String text = "mississippi";
        long copied = 0;
        for (int i = 0; i < text.length(); i++) copied += text.substring(i).length();
        if (copied != (long) text.length() * (text.length() + 1) / 2) throw new AssertionError("copy total");
        // substring(1) allocates a fresh String on each call, so the copies cannot share one object.
        if (text.substring(1) == text.substring(1)) throw new AssertionError("substring reuse");
        // String.compareTo orders by UTF-16 code unit, so a surrogate half sorts below U+FF21.
        String wide = "Ａ", half = "\uD83D";
        if (half.compareTo(wide) >= 0) throw new AssertionError("code unit order");
        // The doubling sort uses the same order, so it ranks the surrogate half first.
        if (!Arrays.equals(byDoubling(wide + half), new int[] {1, 0})) throw new AssertionError("surrogate order");
    }
}
```

#### Solution: [Vary] Longest Common Prefix Of Adjacent Suffixes (Author exercise)
<!-- id: as-adjacent-suffix-lcp -->

**Approach.**
The solution first sorts the start indexes with a comparator that reads characters in place, so no suffix is copied. It then fills the common prefix lengths in text order, which is Kasai's method. A rank array maps each start index to its sorted position. For text position `i` the predecessor is `sa[rank[i] - 1]`. The match length `h` starts from the previous value minus 1. Dropping the first character of two suffixes that matched for `h` characters leaves a match of at least `h - 1`. The invariant is that `h` at the start of position `i` is a proven lower bound on the true value, so the loop only extends it. Since `h` falls by at most 1 per step and never exceeds `n`, the extending loop runs at most `2n` times in total. The test counts those steps to confirm it. The oracle compares every adjacent pair from scratch.

**Complexity.**
- **Time** is O(n) for the Kasai pass, because the match counter rises at most `2n` times in total. The comparator sort that obtains `sa` costs O(n^2 log n) on a run of one letter, and the doubling method replaces it.
- **Space** is O(n), because the sorted indexes, the rank array and the result each hold `n` integers.

```java run
import java.util.*;

public final class AdjacentSuffixLcp {
    // Counts every successful character match in the Kasai loop for the 2n bound.
    static long matchSteps;

    /**
     * Sorts start indexes by comparing suffixes character by character in place.
     * Time: O(n^2 log n) worst case, because a comparison may scan up to n characters.
     * Space: O(n), because only the index array is allocated.
     * Invariant: the comparator is a total order, since a proper prefix sorts first.
     */
    static int[] sortInPlace(String s) {
        // The index array is the only allocation of this method.
        Integer[] idx = new Integer[s.length()];
        // Seed each slot with its own start index.
        for (int i = 0; i < idx.length; i++) idx[i] = i;
        // The comparator walks both suffixes with two cursors and allocates nothing.
        Arrays.sort(idx, (a, b) -> {
            // Cursors start at the two suffix starts.
            int x = a, y = b;
            // Advance while both suffixes continue and agree.
            while (x < s.length() && y < s.length() && s.charAt(x) == s.charAt(y)) { x++; y++; }
            // The suffix that ended first is a proper prefix and sorts first.
            if (x == s.length() || y == s.length()) return Integer.compare(s.length() - a, s.length() - b);
            // Otherwise the first differing characters decide.
            return Character.compare(s.charAt(x), s.charAt(y));
        });
        // Unbox into the return array.
        int[] sa = new int[idx.length];
        // One pass of n copies.
        for (int r = 0; r < sa.length; r++) sa[r] = idx[r];
        // sa[r] is the start of the r-th smallest suffix.
        return sa;
    }

    /**
     * Kasai's method: lcp[r] is the common prefix length of the suffixes at sa[r - 1] and sa[r].
     * Time: O(n), because h rises at most 2n times in total.
     * Space: O(n), because rank and lcp each hold n integers.
     * Invariant: at the start of position i, h is a lower bound for the true match length.
     */
    static int[] kasai(String s, int[] sa) {
        // n is the text length and the length of every array.
        int n = s.length();
        // rank is the inverse permutation of sa.
        int[] rank = new int[n];
        // One pass builds the inverse.
        for (int r = 0; r < n; r++) rank[sa[r]] = r;
        // The answer array starts at all zeros, so lcp[0] stays 0.
        int[] lcp = new int[n];
        // h carries over from one text position to the next.
        int h = 0;
        // Text order is what makes the lower bound h - 1 valid.
        for (int i = 0; i < n; i++) {
            // The smallest suffix has no predecessor, so the carried bound is reset.
            if (rank[i] == 0) { h = 0; continue; }
            // j is the start of the predecessor in sorted order.
            int j = sa[rank[i] - 1];
            // Extend the lower bound only while characters agree and both suffixes continue.
            while (i + h < n && j + h < n && s.charAt(i + h) == s.charAt(j + h)) { h++; matchSteps++; }
            // The settled match length goes to the slot of suffix i.
            lcp[rank[i]] = h;
            // Dropping the first character costs one, never more.
            if (h > 0) h--;
        }
        // The caller reads the maximum for the longest repeat.
        return lcp;
    }

    /**
     * Brute-force oracle that compares each adjacent pair from the start.
     * Time: O(n^2), because each of n pairs may compare n characters.
     * Space: O(n), because the result holds n integers.
     */
    static int[] oracle(String s, int[] sa) {
        // One slot per sorted position.
        int[] lcp = new int[s.length()];
        // The first slot stays 0 by definition.
        for (int r = 1; r < sa.length; r++) {
            // Cursor h counts equal leading characters of the pair.
            int h = 0;
            // Plain comparison with no carried state.
            while (sa[r - 1] + h < s.length() && sa[r] + h < s.length()
                    && s.charAt(sa[r - 1] + h) == s.charAt(sa[r] + h)) h++;
            // Record the pair result.
            lcp[r] = h;
        }
        // The oracle answer is compared with Kasai in main.
        return lcp;
    }

    public static void main(String[] args) {
        // Both examples from the problem text.
        int[] b = kasai("banana", sortInPlace("banana"));
        if (!Arrays.equals(b, new int[] {0, 1, 3, 0, 0, 2})) throw new AssertionError("banana");
        int[] m = kasai("mississippi", sortInPlace("mississippi"));
        if (!Arrays.equals(m, new int[] {0, 1, 1, 4, 0, 0, 1, 0, 2, 1, 3})) throw new AssertionError("mississippi");
        // Empty input returns an empty array.
        if (kasai("", sortInPlace("")).length != 0) throw new AssertionError("empty");
        // Seeded random strings compare Kasai with the pairwise oracle and check the 2n bound.
        Random rng = new Random(34_04_02L);
        for (int trial = 0; trial < 3000; trial++) {
            // Length 0 to 60 with 1 to 3 letters gives long shared prefixes.
            int len = rng.nextInt(61), alpha = 1 + rng.nextInt(3);
            StringBuilder sb = new StringBuilder();
            // Random letters.
            for (int i = 0; i < len; i++) sb.append((char) ('a' + rng.nextInt(alpha)));
            String s = sb.toString();
            // Reset the counter before each run so the bound is per string.
            matchSteps = 0;
            int[] sa = sortInPlace(s);
            int[] fast = kasai(s, sa);
            // Kasai must equal the pairwise result.
            if (!Arrays.equals(fast, oracle(s, sa))) throw new AssertionError("mismatch " + s);
            // The total number of extensions is bounded by 2n.
            if (matchSteps > 2L * len) throw new AssertionError("steps " + s);
        }
    }
}
```

#### Solution: [Boundary] Repeated Character String (Author exercise)
<!-- id: as-repeated-character-string -->

**Approach.**
Every distinct substring is a prefix of exactly one suffix when suffixes are taken in sorted order and a prefix already shared with the predecessor is skipped. The suffix at `sa[r]` has `n - sa[r]` prefixes, and `lcp[r]` of them belong to the predecessor. The count is therefore the sum of `n - sa[r] - lcp[r]`, which equals `n * (n + 1) / 2` minus the sum of `lcp`. The boundary is a string of one repeated letter. All its suffixes start at different indexes yet share the longest possible prefixes, so the sum of `lcp` is `n * (n - 1) / 2` and the answer is `n`. The arithmetic runs in `long`, because `100000 * 100001 / 2` overflows `int`. This version builds `sa` by packing the pair of ranks and the index into one `long` and sorting a primitive array, which avoids boxing. The invariant is that sorting the packed values orders by pair first and by index only on equal pairs.

**Complexity.**
- **Time** is O(n log^2 n), because there are O(log n) rounds, each sorting `n` packed longs in O(n log n), plus an O(n) Kasai pass.
- **Space** is O(n), because the packed array, the ranks and the lcp array hold `n` numbers each and no suffix is copied.

```java run
import java.util.*;

public final class RepeatedCharacterString {
    /**
     * Counts distinct non-empty substrings from the sorted suffixes and their adjacent prefix lengths.
     * Time: O(n log^2 n), because construction dominates the O(n) lcp pass.
     * Space: O(n), because all arrays hold n numbers.
     * Invariant: sa[r] contributes n - sa[r] - lcp[r] new substrings, each counted once.
     */
    static long distinct(String s) {
        // n is the text length.
        int n = s.length();
        // An empty text has no substrings.
        if (n == 0) return 0;
        // The sorted start indexes come from packed-key doubling.
        int[] sa = packedDoubling(s);
        // The adjacent prefix lengths come from the carried-match pass.
        int[] lcp = adjacent(s, sa);
        // The total is accumulated in long to survive n near 100000.
        long total = 0;
        // Each sorted position adds its new prefixes only.
        for (int r = 0; r < n; r++) total += n - sa[r] - lcp[r];
        // The count of distinct substrings.
        return total;
    }

    /**
     * Builds the suffix array by sorting packed long keys, with no boxing.
     * Time: O(n log^2 n), because each round sorts n primitives in O(n log n).
     * Space: O(n), because the packed array and two int arrays hold n values.
     * Invariant: key(i) = rank[i] * M + (rank[i + k] + 1) orders suffixes by 2k characters.
     */
    static int[] packedDoubling(String s) {
        // n is the text length, at least 1 here.
        int n = s.length();
        // M exceeds every rank value, including character codes up to 65535.
        long m = Math.max(n, 65536) + 1;
        // rank starts as the character code.
        int[] rank = new int[n];
        // Seed the first-character ranks.
        for (int i = 0; i < n; i++) rank[i] = s.charAt(i);
        // packed[t] holds key * n + index, so a numeric sort sorts by key then index.
        long[] packed = new long[n];
        // The sorted index list that each round leaves behind.
        int[] sa = new int[n];
        // The step doubles until all ranks differ.
        for (int k = 1; ; k <<= 1) {
            // Build one packed value per start index.
            for (int i = 0; i < n; i++) {
                // A suffix with no second half uses 0, below every real second rank + 1.
                long second = i + k < n ? rank[i + k] + 1 : 0;
                // The first rank is the more significant part.
                long key = rank[i] * m + second;
                // The index sits in the low part, so equal keys sort by index.
                packed[i] = key * n + i;
            }
            // A primitive sort needs no comparator and no boxing.
            Arrays.sort(packed);
            // The new rank of the smallest key is 0.
            int[] fresh = new int[n];
            // Previous key is tracked to detect ties.
            long prevKey = -1;
            // The running new rank value.
            int cur = -1;
            // Walk the sorted packed values.
            for (int t = 0; t < n; t++) {
                // Low part is the index, high part is the key.
                int idx = (int) (packed[t] % n);
                long key = packed[t] / n;
                // A new key means a new rank value.
                if (key != prevKey) { cur++; prevKey = key; }
                // Equal keys share one rank.
                fresh[idx] = cur;
                // The sorted order is stored for the final answer.
                sa[t] = idx;
            }
            // The new ranks replace the old ones for the following round.
            rank = fresh;
            // Rank n - 1 for the last suffix means all keys differ.
            if (cur == n - 1) return sa;
        }
    }

    /**
     * Computes adjacent common prefix lengths by carrying the match length across text positions.
     * Time: O(n), because the carried length rises at most 2n times.
     * Space: O(n), because the inverse array and result hold n integers.
     * Invariant: the carried length never exceeds the true match of the next text position.
     */
    static int[] adjacent(String s, int[] sa) {
        // n is the text length.
        int n = s.length();
        // where[i] is the sorted position of the suffix starting at i.
        int[] where = new int[n];
        // Invert the permutation.
        for (int r = 0; r < n; r++) where[sa[r]] = r;
        // Result array, zero at position 0.
        int[] lcp = new int[n];
        // Carried match length.
        int carried = 0;
        // Visit starts in text order.
        for (int i = 0; i < n; i++) {
            // The smallest suffix has no predecessor.
            if (where[i] == 0) { carried = 0; continue; }
            // Predecessor start.
            int j = sa[where[i] - 1];
            // Extend while both suffixes continue and agree.
            while (i + carried < n && j + carried < n && s.charAt(i + carried) == s.charAt(j + carried)) carried++;
            // Store for the sorted position of i.
            lcp[where[i]] = carried;
            // Moving to i + 1 loses at most one character of the match.
            if (carried > 0) carried--;
        }
        // Return the full array.
        return lcp;
    }

    /**
     * Oracle that stores every substring in a set.
     * Time: O(n^3) because each of O(n^2) substrings is built and hashed.
     * Space: O(n^3) characters in the worst case.
     */
    static long oracle(String s) {
        // The set removes duplicate substrings by value.
        Set<String> all = new HashSet<>();
        // Every start and every end gives one substring.
        for (int i = 0; i < s.length(); i++) for (int j = i + 1; j <= s.length(); j++) all.add(s.substring(i, j));
        // The set size is the count.
        return all.size();
    }

    public static void main(String[] args) {
        // Both examples from the problem text.
        if (distinct("abab") != 7) throw new AssertionError("abab");
        if (distinct("zzzzzzz") != 7) throw new AssertionError("zzzzzzz");
        // Empty and single-letter boundaries.
        if (distinct("") != 0 || distinct("a") != 1) throw new AssertionError("tiny");
        // Seeded random strings compare with the set oracle.
        Random rng = new Random(34_04_03L);
        for (int trial = 0; trial < 2000; trial++) {
            // Length 0 to 30 over 1 to 3 letters.
            int len = rng.nextInt(31), alpha = 1 + rng.nextInt(3);
            StringBuilder sb = new StringBuilder();
            // Random letters.
            for (int i = 0; i < len; i++) sb.append((char) ('a' + rng.nextInt(alpha)));
            String s = sb.toString();
            // The suffix-based count must equal the set size.
            if (distinct(s) != oracle(s)) throw new AssertionError("mismatch " + s);
        }
        // A repeated letter of every length from 1 to 40 has exactly n distinct substrings.
        for (int n = 1; n <= 40; n++) if (distinct("c".repeat(n)) != n) throw new AssertionError("repeat " + n);
        // The largest allowed input runs the same code and returns n.
        String big = "a".repeat(100_000);
        if (distinct(big) != 100_000L) throw new AssertionError("big");
        // int arithmetic overflows for n = 100000, which is why the total uses long.
        int wrong = 100_000 * 100_001 / 2;
        if (wrong == 5_000_050_000L) throw new AssertionError("int did not overflow");
        if ((long) 100_000 * 100_001 / 2 != 5_000_050_000L) throw new AssertionError("long total");
    }
}
```

#### Solution: [Recognize] Longest Duplicate Substring (LeetCode 1044)
<!-- id: as-longest-duplicate-contract -->

**Approach.**
This contract returns the start index and length of the longest repeated substring, with the smallest start on ties, and it differs from the rolling-hash version of the same LeetCode number. The solution builds the suffix array, computes the adjacent common prefix lengths and reads the answer from them. Two occurrences of a repeated substring of length `L` are two suffixes sharing an `L`-character prefix. Every suffix between them in sorted order shares it too, so the maximum value of `lcp` is the longest repeat length. Every start index of a maximum-length repeat belongs to some adjacent pair with `lcp` equal to that maximum, so the smallest start is the minimum of `min(sa[r - 1], sa[r])` over those pairs. The invariant is that no pair outside the maximum can name a longer repeat, and no maximum pair is skipped. The hashing approach binary searches on the length, hashes every window of that length and needs a collision check. The suffix method is deterministic, handles ties by construction and costs O(n log^2 n) with this construction. Rolling hash costs O(n log n) expected time and O(n) space, with a small chance of a wrong candidate unless every hit is verified. The test checks both against an `indexOf` oracle.

**Complexity.**
- **Time** is O(n log^2 n), because construction sorts `n` indexes in each of O(log n) rounds, while the lcp pass and the final scan cost O(n) each.
- **Space** is O(n), because the order, rank and lcp arrays hold `n` integers and the answer is two integers.

```java run
import java.util.*;

public final class DuplicateSubstringContract {
    /**
     * Returns {start, length} of the longest substring occurring at two or more starts, smallest start on ties.
     * Time: O(n log^2 n), because suffix array construction dominates.
     * Space: O(n), because every working array holds n integers.
     * Invariant: every start of a maximum-length repeat belongs to an adjacent pair whose lcp equals the maximum.
     */
    static int[] longestDuplicate(String s) {
        // n is the text length.
        int n = s.length();
        // Sorted starts and adjacent prefix lengths feed the scan.
        int[] sa = suffixArray(s);
        int[] lcp = phiLcp(s, sa);
        // best is the longest repeat length so far; -1 start means none yet.
        int bestLen = 0, bestStart = -1;
        // Pair r compares sorted positions r - 1 and r.
        for (int r = 1; r < n; r++) {
            // The earlier text position is the smaller start of the pair.
            int start = Math.min(sa[r - 1], sa[r]);
            // A strictly longer prefix replaces the answer.
            if (lcp[r] > bestLen) { bestLen = lcp[r]; bestStart = start; }
            // An equal length keeps the smaller start, which is the tie rule.
            else if (lcp[r] == bestLen && bestLen > 0 && start < bestStart) bestStart = start;
        }
        // No repeat leaves {-1, 0}, as the contract says.
        return new int[] {bestStart, bestLen};
    }

    /**
     * Builds the suffix array by doubling with a precomputed second-half array.
     * Time: O(n log^2 n), because each round sorts n indexes.
     * Space: O(n), because all arrays hold n integers.
     * Invariant: equal rank means equal first 2k characters after each round.
     */
    static int[] suffixArray(String s) {
        // n is the text length.
        int n = s.length();
        // Boxed indexes for the comparator sort.
        Integer[] order = new Integer[n];
        // Current ranks and the second-half ranks of the current round.
        final int[] rank = new int[n], second = new int[n];
        // Seed identity order and character-code ranks.
        for (int i = 0; i < n; i++) { order[i] = i; rank[i] = s.charAt(i); }
        // Doubling stops when all ranks differ.
        for (int k = 1; n > 1; k <<= 1) {
            // Precompute the second half so the comparator has two array reads.
            for (int i = 0; i < n; i++) second[i] = i + k < n ? rank[i + k] : -1;
            // Sort by the pair of first and second half.
            Arrays.sort(order, (a, b) -> rank[a] != rank[b] ? Integer.compare(rank[a], rank[b]) : Integer.compare(second[a], second[b]));
            // New ranks are built apart from the old ones.
            int[] fresh = new int[n];
            // Walk the sorted order and bump on each changed pair.
            for (int t = 1; t < n; t++) {
                int p = order[t - 1], q = order[t];
                boolean same = rank[p] == rank[q] && second[p] == second[q];
                fresh[q] = fresh[p] + (same ? 0 : 1);
            }
            // Publish the new ranks by copying, because the comparator holds the rank array.
            System.arraycopy(fresh, 0, rank, 0, n);
            // The last sorted suffix has rank n - 1 only when no ties remain.
            if (rank[order[n - 1]] == n - 1) break;
        }
        // Unbox the final order.
        int[] sa = new int[n];
        for (int r = 0; r < n; r++) sa[r] = order[r];
        // The array of sorted starts.
        return sa;
    }

    /**
     * Computes adjacent prefix lengths through the permuted array indexed by text position.
     * Time: O(n), because the match length rises at most 2n times.
     * Space: O(n), because two arrays of n integers are allocated.
     * Invariant: plcp[i] >= plcp[i - 1] - 1, so the match never restarts from zero.
     */
    static int[] phiLcp(String s, int[] sa) {
        // n is the text length.
        int n = s.length();
        // phi[i] is the start of the suffix just before suffix i in sorted order, or -1.
        int[] phi = new int[n];
        // Fill phi from consecutive sorted starts.
        for (int r = 0; r < n; r++) phi[sa[r]] = r == 0 ? -1 : sa[r - 1];
        // plcp[i] is the prefix length of suffix i and its predecessor.
        int[] plcp = new int[n];
        // Carried match length.
        int h = 0;
        // Text order.
        for (int i = 0; i < n; i++) {
            // No predecessor means no match and a reset.
            if (phi[i] < 0) { h = 0; continue; }
            // Extend while both suffixes continue and agree.
            while (i + h < n && phi[i] + h < n && s.charAt(i + h) == s.charAt(phi[i] + h)) h++;
            plcp[i] = h;
            // One character is lost when both suffixes advance.
            if (h > 0) h--;
        }
        // Convert to sorted order: lcp[r] belongs to the suffix at sa[r].
        int[] lcp = new int[n];
        for (int r = 0; r < n; r++) lcp[r] = plcp[sa[r]];
        // The array read by the scan.
        return lcp;
    }

    /**
     * Oracle that tests every length from longest to shortest with indexOf.
     * Time: O(n^3) worst case.
     * Space: O(n) per substring.
     */
    static int[] oracle(String s) {
        // Longest lengths first, so the first hit is maximal.
        for (int len = s.length() - 1; len >= 1; len--) {
            // Smallest start first, so the first hit is the tie winner.
            for (int p = 0; p + len <= s.length(); p++) {
                // A later occurrence of the same text at a different start proves a repeat.
                if (s.indexOf(s.substring(p, p + len), p + 1) >= 0) return new int[] {p, len};
            }
        }
        // No repeat.
        return new int[] {-1, 0};
    }

    public static void main(String[] args) {
        // Both examples from the problem text.
        if (!Arrays.equals(longestDuplicate("banana"), new int[] {1, 3})) throw new AssertionError("banana");
        if (!Arrays.equals(longestDuplicate("xyxyxy"), new int[] {0, 4})) throw new AssertionError("xyxyxy");
        // No repeat, empty and single-letter inputs return {-1, 0}.
        for (String t : new String[] {"abcd", "", "a"}) {
            if (!Arrays.equals(longestDuplicate(t), new int[] {-1, 0})) throw new AssertionError("none " + t);
        }
        // Two repeats of length 3 tie, and the smaller start 0 wins.
        if (!Arrays.equals(longestDuplicate("xyzabcabcxyz"), new int[] {0, 3})) throw new AssertionError("tie");
        // Seeded random strings compare with the indexOf oracle.
        Random rng = new Random(34_04_04L);
        for (int trial = 0; trial < 3000; trial++) {
            // Length 0 to 40 over 1 to 3 letters.
            int len = rng.nextInt(41), alpha = 1 + rng.nextInt(3);
            StringBuilder sb = new StringBuilder();
            for (int i = 0; i < len; i++) sb.append((char) ('a' + rng.nextInt(alpha)));
            String s = sb.toString();
            // Start and length must both match, including the tie rule.
            if (!Arrays.equals(longestDuplicate(s), oracle(s))) throw new AssertionError("mismatch " + s);
        }
    }
}
```
