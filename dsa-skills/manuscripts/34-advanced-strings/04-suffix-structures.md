<!-- lesson-kind: standard -->
<!-- lesson-id: suffix-structures -->
## Sort And Compare All Suffixes

<!-- stage: context -->
### Why Copying Every Suffix Fails

A code-review tool offers a feature that flags the longest passage repeated inside one generated source file. The first version lists every tail of the file as its own `String` and sorts the list, so that tails with a shared beginning sit side by side. It works on a 2,000-character test file. On a real 100,000-character file the JVM stops with `OutOfMemoryError: Java heap space`.

A suffix of a string `s` is the part from index `i` to the end, written `s[i..]`, and a string of length `n` has exactly `n` of them. The failed version copied all of them. Their total length is `n * (n + 1) / 2`, which is 5,000,050,000 characters for `n = 100,000`, about 5 GB of character data. The question for this lesson is how to put all suffixes of one text in order and read repeated substrings from that order without ever copying a suffix.

<!-- stage: naive -->
### Sorting Copied Suffixes

The direct method copies each suffix with `substring`, sorts the copies with the natural string order and recovers each start index from the copy length. Distinct suffixes of one string have distinct lengths, so the length identifies the start.

```java
static int[] sortCopiedSuffixes(String s) {
    int n = s.length();
    List<String> suffixes = new ArrayList<>();
    for (int i = 0; i < n; i++) {
        suffixes.add(s.substring(i)); // copies n - i characters
    }
    Collections.sort(suffixes);
    int[] start = new int[n];
    for (int j = 0; j < n; j++) {
        start[j] = n - suffixes.get(j).length();
    }
    return start;
}
```

For `banana` the sorted copies are `a`, `ana`, `anana`, `banana`, `na`, `nana`, and the method returns the starts `[5, 3, 1, 0, 4, 2]`. The answer is correct, and the memory cost is the problem.

<!-- stage: bottleneck -->
### Counting What The Sort Copies And Rescans

```predict
A string holds 100,000 copies of the letter a. How many characters does the copying method allocate, and how many characters can one comparison scan inside the sort?

The copies hold 5,000,050,000 characters in total. Every pair of suffixes shares a prefix as long as the shorter one, so one comparison can scan up to 100,000 characters.
```

The method has two separate costs. The first is memory. The `n` copies hold `n * (n + 1) / 2` characters, so space is O(n^2). The second is repeated scanning. A sort makes about `n log n` comparisons, and a comparison of two suffixes reads characters until they differ. On `aaaa...a` they never differ before the shorter suffix ends, so each comparison reads up to `n` characters and the total time is O(n^2 log n).

The named repeated work is rescanning shared beginnings. In `banana` the suffixes `ana` and `anana` share the beginning `ana`. Every comparison involving either of them reads those three characters again, although an earlier comparison already established that they match. Skipping the copies fixes the memory cost only, because a comparator that reads in place still rescans every shared beginning. The sort needs to reuse what earlier comparisons established.

<!-- stage: insight -->
### Ordering By Doubling Prefixes

The structure that fixes both costs is the **suffix array**: an `int[] sa` of length `n` holding the start indexes of all suffixes in increasing lexicographic order. It stores `n` integers and no characters.

#### Doubling The Compared Length

Give every suffix an integer **rank** that orders it by its first `k` characters only. Two suffixes get equal ranks when those `k` characters are equal, and a suffix shorter than `k` compares with its end treated as smaller than any character. If ranks for length `k` are known, ranks for length `2k` follow from one pair. The first `k` characters of `s[i..]` have rank `rank[i]`, and the next `k` characters are the first `k` of `s[i+k..]`, which have rank `rank[i+k]`. Sorting by the pair `(rank[i], rank[i+k])`, with `-1` when `i + k` is past the end, orders by `2k` characters without reading a single character again.

<!-- names: suffix array, rank, LCP array -->

Start from `k = 1`, where the rank is the character code itself. After at most `ceil(log2 n)` doublings, `2k` reaches `n`, all suffixes differ within `n` characters and every rank is distinct. Each round sorts `n` pairs in O(n log n), so construction is O(n log^2 n) time and O(n) space.

#### Reading Repeats From Neighbours

Once the suffix array exists, the **LCP array** (longest common prefix array) records one number per sorted position `r`. The number `lcp[r]` is the length of the longest common prefix of the suffixes `sa[r - 1]` and `sa[r]`, and `lcp[0] = 0`. Two suffixes that share a long beginning must sit next to each other in sorted order, because everything between them in the order shares that beginning too. A substring that occurs twice is therefore a common prefix of two neighbouring suffixes, and the longest repeated substring has length `max(lcp)`.

Computing each LCP value by comparing neighbours directly can cost O(n) per pair. Kasai's method processes suffixes in text order instead. If `s[i..]` shares `h` characters with its sorted predecessor, then `s[i+1..]` shares at least `h - 1` characters with its own predecessor. The variable `h` never drops by more than 1 per step and never exceeds `n`, so all increments together are at most `2n` and the whole LCP array costs O(n).

#### Counting Distinct Substrings

Every substring is a prefix of exactly one earliest suffix in sorted order. The suffix at `sa[r]` has `n - sa[r]` prefixes, and `lcp[r]` of them already belong to its predecessor. The number of distinct substrings is therefore `n * (n + 1) / 2 - sum(lcp)`.

#### Equal End Positions In An Automaton

A suffix automaton answers the same questions from the other direction. For a substring `t`, its end-position set lists every index where an occurrence of `t` ends. Substrings with the same end-position set form one state. In `banana` the substrings `na` and `ana` both end at indexes 3 and 5, so they share one state with lengths 2 and 3. The substring `a` ends at 1, 3 and 5 and has its own state. The automaton has at most `2n - 1` states for `n >= 2`. This lesson builds the suffix array, and the automaton stays an idea, because its construction needs a separate lesson.

<!-- stage: variables -->
### Arrays Kept During Construction

Construction and the LCP pass keep a short list of arrays and counters.

- **s** is the text, read by `charAt` and never copied.
- **sa** holds start indexes in sorted order, so `sa[r]` is the start of the suffix with sorted position `r`.
- **rank** holds one integer per start index; `rank[i]` orders suffix `i` by its first `k` characters, and after the last round it equals the sorted position of suffix `i`.
- **k** is the compared length, which starts at 1 and doubles each round.
- **lcp** holds `lcp[r]`, the common prefix length of the suffixes at sorted positions `r - 1` and `r`.
- **h** is the running match length in Kasai's loop, carried from one text position to the next.

<!-- stage: trace -->
### Building And Comparing Two Texts

#### Doubling Rounds On banana

The text is `banana`. The pointers `first` and `last` mark the start index of the smallest and the largest suffix after each round. Before any round, the rank is the character code: `b` is 98, `a` is 97 and `n` is 110.

The round with `k = 1` sorts by pairs of the first two characters and gives ranks `[2, 1, 3, 1, 3, 0]`. Two ties remain. The suffixes at 1 and 3 tie because both begin with `an`, and the suffixes at 2 and 4 tie because both begin with `na`. Sorted order so far is `[5, 1, 3, 0, 2, 4]`. The round with `k = 2` compares four characters, and the ties break because `ana` ends while `anana` continues. Ranks become `[3, 2, 5, 1, 4, 0]`, all distinct, and the array is `[5, 3, 1, 0, 4, 2]`. The loop stops after two rounds.

```trace
{"cells":["b","a","n","a","n","a"],"pointers":["first","last"],"steps":[{"at":{"first":-1,"last":-1},"vars":{"k":0,"rank":"[98,97,110,97,110,97]"},"note":"Before any round the rank of each suffix is the code of its first character."},{"at":{"first":5,"last":4},"vars":{"k":1,"rank":"[2,1,3,1,3,0]","order":"[5,1,3,0,2,4]"},"note":"Round with k = 1 sorts by pairs of ranks, so it orders by 2 characters. Ties remain, so another round follows."},{"at":{"first":5,"last":2},"vars":{"k":2,"rank":"[3,2,5,1,4,0]","order":"[5,3,1,0,4,2]"},"note":"Round with k = 2 sorts by pairs of ranks, so it orders by 4 characters. All ranks are distinct, so the loop stops."}]}
```

#### Kasai Pass On banana

The pointer `i` marks the text position being compared, and `j` marks the start of its predecessor in sorted order, or -1 when none exists. The variable `h` carries over from one position to the next.

At `i = 0` the suffix `banana` sits at sorted position 3, and its predecessor `anana` begins with a different letter, so the match is 0. At `i = 1` the suffix `anana` has predecessor `ana`, which matches for 3 characters before it ends. Moving to `i = 2` lowers `h` from 3 to 2 without rescanning, and the next check finds the end of `na` at once, giving 2. The step from `i = 3` starts with `h = 1`, again reusing earlier work. The result is `lcp = [0, 1, 3, 0, 0, 2]`. Its maximum 3 gives the longest repeated substring `ana`, found at starts 1 and 3. The distinct count is `21 - 6 = 15`.

```trace
{"cells":["b","a","n","a","n","a"],"pointers":["i","j"],"steps":[{"at":{"i":0,"j":1},"vars":{"h":0,"lcp":"[0,0,0,0,0,0]"},"note":"i = 0: predecessor starts at 1. The match starts at h = 0 and ends at 0, so lcp[3] = 0."},{"at":{"i":1,"j":3},"vars":{"h":3,"lcp":"[0,0,3,0,0,0]"},"note":"i = 1: predecessor starts at 3. The match starts at h = 0 and ends at 3, so lcp[2] = 3."},{"at":{"i":2,"j":4},"vars":{"h":2,"lcp":"[0,0,3,0,0,2]"},"note":"i = 2: predecessor starts at 4. The match starts at h = 2 and ends at 2, so lcp[5] = 2."},{"at":{"i":3,"j":5},"vars":{"h":1,"lcp":"[0,1,3,0,0,2]"},"note":"i = 3: predecessor starts at 5. The match starts at h = 1 and ends at 1, so lcp[1] = 1."},{"at":{"i":4,"j":0},"vars":{"h":0,"lcp":"[0,1,3,0,0,2]"},"note":"i = 4: predecessor starts at 0. The match starts at h = 0 and ends at 0, so lcp[4] = 0."},{"at":{"i":5,"j":-1},"vars":{"h":0,"lcp":"[0,1,3,0,0,2]"},"note":"i = 5: the suffix is first in sorted order, so no predecessor exists and h resets to 0."}]}
```

<!-- stage: code -->
### Building Suffix Array And LCP

#### Construction Without Substrings

The first method builds the suffix array by doubling. It sorts boxed indexes with a comparator that reads only the `rank` array, so no suffix is ever copied.

```java
static int[] suffixArray(String s) {
    int n = s.length();
    Integer[] order = new Integer[n];
    int[] rank = new int[n];
    int[] next = new int[n];
    for (int i = 0; i < n; i++) {
        order[i] = i;
        rank[i] = s.charAt(i);
    }
    for (int k = 1; n > 0; k <<= 1) {
        final int step = k;
        Comparator<Integer> byPair = (a, b) -> {
            if (rank[a] != rank[b]) return Integer.compare(rank[a], rank[b]);
            int ra = a + step < n ? rank[a + step] : -1;
            int rb = b + step < n ? rank[b + step] : -1;
            return Integer.compare(ra, rb);
        };
        Arrays.sort(order, byPair);
        next[order[0]] = 0;
        for (int t = 1; t < n; t++) {
            int bump = byPair.compare(order[t - 1], order[t]) < 0 ? 1 : 0;
            next[order[t]] = next[order[t - 1]] + bump;
        }
        System.arraycopy(next, 0, rank, 0, n);
        if (rank[order[n - 1]] == n - 1) break; // all ranks distinct
    }
    int[] sa = new int[n];
    for (int r = 0; r < n; r++) sa[r] = order[r];
    return sa;
}
```

#### LCP, Repeats And Distinct Count

The remaining methods use `sa` and the Kasai pass. Characters are compared as UTF-16 code units, which is the order `String.compareTo` uses.

```java
static int[] adjacentLcp(String s, int[] sa) {
    int n = s.length();
    int[] rank = new int[n];
    for (int r = 0; r < n; r++) rank[sa[r]] = r;
    int[] lcp = new int[n];
    int h = 0;
    for (int i = 0; i < n; i++) {
        if (rank[i] == 0) { h = 0; continue; }
        int j = sa[rank[i] - 1];
        while (i + h < n && j + h < n && s.charAt(i + h) == s.charAt(j + h)) h++;
        lcp[rank[i]] = h;
        if (h > 0) h--;
    }
    return lcp;
}

static long distinctSubstrings(int n, int[] lcp) {
    long total = (long) n * (n + 1) / 2;
    for (int v : lcp) total -= v;
    return total;
}
```

The count uses `long`, because `n * (n + 1) / 2` exceeds the `int` range once `n` passes 65,535.

<!-- stage: applicability -->
### When Suffix Order Answers The Question

#### Recognizing The Pattern

Reach for sorted suffixes when one fixed text is queried for repeated substrings, for the longest repeat, for distinct substring counts or for the order of its suffixes. The invariant to protect is that after every doubling round, equal ranks mean equal first `k` characters, and after the last round the ranks equal the sorted positions. A comparator that breaks this, for example by treating a missing character as equal to a real one, silently merges `ana` with `anana`.

#### False Friends And Limits

The rolling hash is a false friend of the suffix array. It also finds repeated substrings, but it answers one length per pass, relies on collision handling and needs a binary search over the length. The suffix array is deterministic and answers every length at once, at the price of O(n log^2 n) construction and O(n) integers of memory. A second false friend is `String.indexOf` in a loop, which finds one pattern per call and cannot order suffixes.

The method does not apply when the text changes between queries, because every edit invalidates the order. It also does not apply when only a single pattern is searched once, where a linear scan is cheaper. Characters are compared as UTF-16 code units, so supplementary characters sort by their surrogate halves and not by code point, which can differ from the order a person expects.

<!-- stage: exercises -->
### Exercises

#### [Build] Sort Small Suffixes (Author exercise)
<!-- id: as-sort-small-suffixes -->

**Prerequisites.** The doubling rounds and the rank array from this lesson.

**Problem.** Given a string `s` of lowercase English letters, return the int array `sa` of length `s.length()` in which `sa[r]` is the start index of the suffix of rank `r` when all suffixes are sorted by character code. A suffix that is a proper prefix of another suffix sorts before it. The suffix starting at index `i` is the characters from `i` to the last index.

**Constraints.** The limits are:
- **Length** satisfies `0 <= s.length() <= 100000`.
- **Characters** are the letters `a` to `z` only.
- **Empty input** returns an empty array.
- **Ties** do not occur, since distinct start indexes give distinct suffixes.
- **Mutation** does not occur; `s` is read only.

**Example 1.** Input `s = "banana"`, output `[5, 3, 1, 0, 4, 2]`.

**Example 2.** Input `s = "abab"`, output `[2, 0, 3, 1]`, because `ab` is a proper prefix of `abab` and sorts first.

**Hint.** Sort the indexes, not the substrings. Which two numbers decide the order of two suffixes once the first `k` characters are ranked?

**Changed decision.** The sort key changes from a copied string to a pair of integers read from a rank array.

#### [Vary] Longest Common Prefix Of Adjacent Suffixes (Author exercise)
<!-- id: as-adjacent-suffix-lcp -->

**Prerequisites.** The suffix array exercise above and the Kasai pass.

**Problem.** Given a string `s` of lowercase English letters, let `sa` be its suffix array. Return the int array `lcp` of length `s.length()` where `lcp[0] = 0` and, for `r >= 1`, `lcp[r]` is the length of the longest common prefix of the suffixes starting at `sa[r - 1]` and `sa[r]`.

**Constraints.** The limits are:
- **Length** satisfies `0 <= s.length() <= 100000`.
- **Characters** are the letters `a` to `z` only.
- **Empty input** returns an empty array.
- **Values** in `lcp` are non-negative `int` values below `s.length()`.
- **Mutation** does not occur; `s` is read only.

**Example 1.** Input `s = "banana"`, output `[0, 1, 3, 0, 0, 2]`, so the longest repeat has length 3.

**Example 2.** Input `s = "mississippi"`, output `[0, 1, 1, 4, 0, 0, 1, 0, 2, 1, 3]`, where the value 4 is the repeat `issi`.

**Hint.** If suffix `i` matches its predecessor for `h` characters, how many characters must suffix `i + 1` match its own predecessor?

**Changed decision.** The question moves from the order of suffixes to the match length between neighbours, and the running value `h` replaces a fresh comparison for each pair.

#### [Boundary] Repeated Character String (Author exercise)
<!-- id: as-repeated-character-string -->

**Prerequisites.** The adjacent LCP exercise above and the distinct substring count.

**Problem.** Given a string `s` of lowercase English letters, return the number of distinct non-empty substrings of `s`, where two substrings are equal when they have the same characters in the same order. Equal prefixes of different suffixes must not be counted twice, and the suffixes of a string made of one repeated letter all start at different indexes while sharing long prefixes.

**Constraints.** The limits are:
- **Length** satisfies `0 <= s.length() <= 100000`.
- **Characters** are the letters `a` to `z` only.
- **Return type** is `long`, because the number of substrings can exceed the `int` range.
- **Empty input** returns 0.
- **Mutation** does not occur; `s` is read only.

**Example 1.** Input `s = "abab"`, output 7: `a`, `b`, `ab`, `ba`, `aba`, `bab`, `abab`.

**Example 2.** Input `s = "zzzzzzz"`, output 7, because only the lengths 1 to 7 of the repeated letter exist.

**Hint.** How many prefixes does the suffix at `sa[r]` contribute, and how many of those did its sorted predecessor already contribute?

**Changed decision.** The count subtracts shared prefix lengths, so equal prefixes of distinct suffix starts are counted once.

#### [Recognize] Longest Duplicate Substring (LeetCode 1044)
<!-- id: as-longest-duplicate-contract -->

**Prerequisites.** The adjacent LCP exercise above and the rolling-hash lesson of this chapter.

**Problem.** This lesson uses LeetCode 1044 with a different contract from the rolling-hash lesson, which asks for a duplicate found by hashing. Here, given a string `s` of lowercase English letters, return the pair `(start, length)` of the longest substring that occurs at two or more different start indexes. Occurrences may overlap. Among all substrings of the maximum length that occur twice, return the smallest start index of any occurrence. If no substring occurs twice, return `(-1, 0)`.

**Constraints.** The limits are:
- **Length** satisfies `0 <= s.length() <= 100000`.
- **Characters** are the letters `a` to `z` only.
- **Answer** is an `int[]` of two values, start then length.
- **Ties** between equal lengths resolve to the smallest start index.
- **Mutation** does not occur; `s` is read only.

**Example 1.** Input `s = "banana"`, output `(1, 3)`, the substring `ana`.

**Example 2.** Input `s = "xyxyxy"`, output `(0, 4)`, because `xyxy` occurs at starts 0 and 2 and the occurrences overlap.

**Hint.** Where must two occurrences of the longest repeat sit in sorted suffix order? Which neighbour pairs reach the maximum common prefix length?

**Changed decision.** The answer is read from neighbouring suffixes and ties are settled by the smallest start, in place of a binary search over the length.
