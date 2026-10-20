<!-- lesson-kind: standard -->
<!-- lesson-id: palindrome-radii -->
## Find Palindromes Around Every Center

<!-- stage: context -->
### A Padding Line Freezes The Viewer

A log viewer has a feature that highlights the longest palindromic run in each line, meaning the longest stretch of characters that reads the same forward and backward. The feature works well on ordinary lines. Then a customer opens a file in which one line holds 100,000 copies of the same padding character, and the viewer freezes for many seconds. The feature tests every position as the middle of a possible palindrome, and on this line each test walks almost as far as the line allows.

One question drives this lesson. How can a program find the palindromes around every center in time proportional to the line length, so that the padding line costs no more than any other line of the same size? Centers come in two kinds. A character is the center of a palindrome with odd length, and the gap between two neighbouring characters is the center of a palindrome with even length. The answer must handle both kinds.

<!-- stage: naive -->
### Expanding Outward From Each Center

The direct method treats every position as a possible center and grows a window outward while the two end characters are equal. It runs once for odd lengths, where the window starts as a single character, and once for even lengths, where the window starts as an empty gap between two characters. It remembers the longest window found, and it replaces the answer only when a window is strictly longer, so the leftmost window wins a tie.

```java
static int[] longestByExpansion(String s) {
    int bestStart = 0, bestLen = 0;
    for (int center = 0; center < s.length(); center++) {
        for (int parity = 0; parity < 2; parity++) {
            // parity 0 starts a one-character window, parity 1 starts an empty gap window
            int lo = center, hi = center + parity;
            while (lo >= 0 && hi < s.length() && s.charAt(lo) == s.charAt(hi)) {
                lo--;
                hi++;
            }
            int len = hi - lo - 1; // number of characters between the failed ends
            if (len > bestLen) {
                bestLen = len;
                bestStart = lo + 1;
            }
        }
    }
    return new int[] {bestStart, bestLen};
}
```

On `abaab` the method finds `aba` around the first `b` and `baab` around the gap between the two `a` characters, and it returns start 1 with length 4. The method is correct, short, and fast on ordinary text, and it uses no memory beyond a few integers.

<!-- stage: bottleneck -->
### Counting The Repeated Comparisons

```predict
On a line of n identical characters, about how many character comparisons does the expansion method make, and which comparisons does it repeat?

Each center expands until it reaches the nearer end of the line, so the total is about n^2 / 2 comparisons, which is O(n^2). Center number k repeats the same equal pairs that center number k - 1 already compared, only shifted by one position.
```

#### Where The Cost Comes From

Every center scans on its own and forgets what earlier centers learned. On a line of `n` identical characters, the odd center at index `i` makes about `min(i, n - 1 - i)` successful comparisons, and the sum over all indexes is about `n^2 / 4`. The even centers add the same amount, so the total is O(n^2), about `n^2 / 2`. For `n = 100,000` that is about 5 * 10^9 comparisons, which explains the frozen viewer. A line of `n` distinct characters costs only O(n), so the method hides its worst case until the input is repetitive.

#### The Repeated Work

Once the method has found a long palindrome, the characters inside it are known to be symmetric. A center that sits inside that palindrome sees a left half that is the reversed right half of another center it has already finished. The method still compares those pairs again. The repeated work is the re-comparison of characters that a finished center already compared, and the lesson removes it.

<!-- stage: insight -->
### Reusing Matches Inside A Known Palindrome

Three ideas remove the repeated comparisons: one array that covers both kinds of center, a copy of an earlier answer for a position inside a known palindrome, and a limit on how much of that copy is trustworthy.

#### One Array For Both Parities

A palindrome of odd length has a character at its center, and a palindrome of even length has a gap at its center. Two kinds of center normally need two loops and two result arrays. Insert one **separator** character, written `#` here, before the first letter, between every pair of letters and after the last letter. The string `abab` becomes `#a#b#a#b#`, and the separator must not occur in the original string. Every palindrome of the new string has odd length and a single character as its center, and the gap between two letters has become an ordinary separator position.

The **radius** of position `i` is the largest `k` such that the characters from index `i - k` through `i + k` form a palindrome. The code stores it in an array named `rad`. Because separators are added in matching pairs, the radius at `i` equals the length of the longest palindrome of the original string that is centered there, and that palindrome starts at index `(i - radius) / 2` of the original string.

#### Copying From The Mirror Position

Suppose the scan has finished all positions before `i`. It remembers the finished palindrome whose right edge `right = center + rad[center]` lies farthest to the right. If `i` lies inside that palindrome, the **mirror** position of `i` is `j = 2 * center - i`, the position at the same distance from `center` on the other side. The big palindrome reads the same in both directions, so the text around `i` is the reversed text around `j`. A palindrome centered at `j` that fits entirely inside the big one therefore has a reflected twin centered at `i`, with the same radius. When `rad[j]` is smaller than `right - i`, the radius at `i` equals `rad[j]` exactly, and no comparison is needed.

#### Clamping At The Right Edge

The characters beyond `right` have not been compared with anything on the left side, so the reflection argument stops at that edge. When `rad[j]` is at least `right - i`, the code must **clamp** the copied value to `right - i`, which is the largest radius the big palindrome guarantees. Only after the clamp does it compare characters one pair at a time beyond `right`, and every successful comparison moves `right` farther to the right.

<!-- names: radius, separator, mirror, clamp -->

The invariant is that every position inside `rad[i]` of `i` is already known to match before an expansion starts. The value of `right` never decreases and never exceeds the last index, so successful comparisons happen at most once per index in total. Each position adds at most one failed comparison. The whole scan is therefore linear in the length of the separator string, which is `2n + 1` for an input of length `n`.

<!-- stage: variables -->
### Values The Scan Keeps

The scan keeps five values next to the current index `i`, and all of them describe the separator string `t` of length `m = 2n + 1`.

- **t** holds the input letters with one separator before, between and after them.
- **rad** holds one radius per index of `t`, and `rad[i]` is final once the scan leaves `i`.
- **center** is the index of the finished palindrome with the farthest right edge.
- **right** equals `center + rad[center]`, the last index known to match.
- **j** equals `2 * center - i`, the mirror of the current index `i`.

When `i` is greater than or equal to `right`, the scan copies nothing and starts with radius 0.

<!-- stage: trace -->
### Tracing Two Strings Step By Step

The pointer `i` marks the position being finished, the pointer `c` marks `center`, and the pointer `r` marks `right`. Each step shows the state after the scan finishes one position. The variable `copied` is the radius taken from the mirror before any comparison, and `expanded` is the number of extra matching pairs found by comparing. The final `rad` equals `copied` plus `expanded`.

#### Tracing abaab

The string `abaab` becomes `#a#b#a#a#b#`, which has 11 positions. Positions 0 to 3 start fresh, because `right` has not passed them. Position 3 is the letter `b`, and it expands to radius 3, so `center` moves to 3 and `right` moves to 6. Position 4 has mirror 2, whose radius is 0, so it copies 0. Position 5 has mirror 1 with radius 1, and that equals `right - i`, so the copy reaches the edge exactly and one more comparison is needed. That comparison fails, so the radius stays 1.

Position 6 is the gap between the two letters `a`. It is not inside any palindrome that extends past it, so it starts fresh and expands to radius 4, which is `baab`. Now `center` is 6 and `right` is 10. Positions 7 and 8 copy radii 1 and 0 from their mirrors. Position 9 has mirror 3 with radius 3, but `right - i` is only 1, so the clamp reduces the copy to 1. The scan keeps 1 because the comparison beyond the edge fails. Position 10 is at `right`, so it starts fresh with radius 0.

```trace
{"cells":["#","a","#","b","#","a","#","a","#","b","#"],"pointers":["i","c","r"],"steps":[{"at":{"i":0,"c":0,"r":0},"vars":{"rad":"0","copied":"0","expanded":"0"},"note":"i = 0: No known palindrome covers this index, so the radius starts at 0. Expansion adds 0, so rad[0] = 0."},{"at":{"i":1,"c":1,"r":2},"vars":{"rad":"1","copied":"0","expanded":"1"},"note":"i = 1: No known palindrome covers this index, so the radius starts at 0. Expansion adds 1, so rad[1] = 1."},{"at":{"i":2,"c":1,"r":2},"vars":{"rad":"0","copied":"0","expanded":"0"},"note":"i = 2: No known palindrome covers this index, so the radius starts at 0. Expansion adds 0, so rad[2] = 0."},{"at":{"i":3,"c":3,"r":6},"vars":{"rad":"3","copied":"0","expanded":"3"},"note":"i = 3: No known palindrome covers this index, so the radius starts at 0. Expansion adds 3, so rad[3] = 3."},{"at":{"i":4,"c":3,"r":6},"vars":{"rad":"0","copied":"0","expanded":"0"},"note":"i = 4: Mirror 2 has radius 0, below the edge distance 2, so the copy 0 is exact. Expansion adds 0, so rad[4] = 0."},{"at":{"i":5,"c":3,"r":6},"vars":{"rad":"1","copied":"1","expanded":"0"},"note":"i = 5: Mirror 1 has radius 1, equal to the edge distance 1, so the copy 1 reaches the edge and expansion must test beyond it. Expansion adds 0, so rad[5] = 1."},{"at":{"i":6,"c":6,"r":10},"vars":{"rad":"4","copied":"0","expanded":"4"},"note":"i = 6: No known palindrome covers this index, so the radius starts at 0. Expansion adds 4, so rad[6] = 4."},{"at":{"i":7,"c":6,"r":10},"vars":{"rad":"1","copied":"1","expanded":"0"},"note":"i = 7: Mirror 5 has radius 1, below the edge distance 3, so the copy 1 is exact. Expansion adds 0, so rad[7] = 1."},{"at":{"i":8,"c":6,"r":10},"vars":{"rad":"0","copied":"0","expanded":"0"},"note":"i = 8: Mirror 4 has radius 0, below the edge distance 2, so the copy 0 is exact. Expansion adds 0, so rad[8] = 0."},{"at":{"i":9,"c":6,"r":10},"vars":{"rad":"1","copied":"1","expanded":"0"},"note":"i = 9: Mirror 3 has radius 3, above the edge distance 1, so the clamp reduces the copy to 1. Expansion adds 0, so rad[9] = 1."},{"at":{"i":10,"c":6,"r":10},"vars":{"rad":"0","copied":"0","expanded":"0"},"note":"i = 10: No known palindrome covers this index, so the radius starts at 0. Expansion adds 0, so rad[10] = 0."}]}
```

#### Tracing abab With A Clamp

The string `abab` becomes `#a#b#a#b#`, with 9 positions. Position 3 expands to radius 3 and moves `right` to 6. Position 5 expands to radius 3, so `center` is 5 and `right` is 8. Position 7 is the letter `b`, and its mirror is 3, whose radius is 3. The value `right - i` is 1, because index 8 is the last position. The clamp gives 1, and an unclamped copy would claim radius 3 for a position that has only one character to its right.

The final radii are `0 1 0 3 0 3 0 1 0`. The largest value is 3, first reached at index 3, so the longest palindrome is `aba` and it starts at original index `(3 - 3) / 2 = 0`.

```trace
{"cells":["#","a","#","b","#","a","#","b","#"],"pointers":["i","c","r"],"steps":[{"at":{"i":0,"c":0,"r":0},"vars":{"rad":"0","copied":"0","expanded":"0"},"note":"i = 0: No known palindrome covers this index, so the radius starts at 0. Expansion adds 0, so rad[0] = 0."},{"at":{"i":1,"c":1,"r":2},"vars":{"rad":"1","copied":"0","expanded":"1"},"note":"i = 1: No known palindrome covers this index, so the radius starts at 0. Expansion adds 1, so rad[1] = 1."},{"at":{"i":2,"c":1,"r":2},"vars":{"rad":"0","copied":"0","expanded":"0"},"note":"i = 2: No known palindrome covers this index, so the radius starts at 0. Expansion adds 0, so rad[2] = 0."},{"at":{"i":3,"c":3,"r":6},"vars":{"rad":"3","copied":"0","expanded":"3"},"note":"i = 3: No known palindrome covers this index, so the radius starts at 0. Expansion adds 3, so rad[3] = 3."},{"at":{"i":4,"c":3,"r":6},"vars":{"rad":"0","copied":"0","expanded":"0"},"note":"i = 4: Mirror 2 has radius 0, below the edge distance 2, so the copy 0 is exact. Expansion adds 0, so rad[4] = 0."},{"at":{"i":5,"c":5,"r":8},"vars":{"rad":"3","copied":"1","expanded":"2"},"note":"i = 5: Mirror 1 has radius 1, equal to the edge distance 1, so the copy 1 reaches the edge and expansion must test beyond it. Expansion adds 2, so rad[5] = 3."},{"at":{"i":6,"c":5,"r":8},"vars":{"rad":"0","copied":"0","expanded":"0"},"note":"i = 6: Mirror 4 has radius 0, below the edge distance 2, so the copy 0 is exact. Expansion adds 0, so rad[6] = 0."},{"at":{"i":7,"c":5,"r":8},"vars":{"rad":"1","copied":"1","expanded":"0"},"note":"i = 7: Mirror 3 has radius 3, above the edge distance 1, so the clamp reduces the copy to 1. Expansion adds 0, so rad[7] = 1."},{"at":{"i":8,"c":5,"r":8},"vars":{"rad":"0","copied":"0","expanded":"0"},"note":"i = 8: No known palindrome covers this index, so the radius starts at 0. Expansion adds 0, so rad[8] = 0."}]}
```

<!-- stage: code -->
### Manacher's Scan In Java

#### Building The Padded Array

The first method builds the separator string as a `char` array, so later code reads characters by index and never allocates a substring.

```java
static char[] withSeparators(String s) {
    char[] t = new char[2 * s.length() + 1];
    for (int i = 0; i < t.length; i++) t[i] = '#'; // every position starts as a separator
    for (int k = 0; k < s.length(); k++) t[2 * k + 1] = s.charAt(k); // letters sit at odd indexes
    return t;
}
```

#### Computing Every Radius

The second method is the scan. The condition `i < right` decides whether a mirror exists, and the `while` loop is the only place that moves `right`.

```java
static int[] radii(char[] t) {
    int m = t.length;
    int[] rad = new int[m];
    int center = 0, right = 0;
    for (int i = 0; i < m; i++) {
        if (i < right) rad[i] = Math.min(right - i, rad[2 * center - i]); // copy, clamped at the edge
        while (i - rad[i] - 1 >= 0 && i + rad[i] + 1 < m
                && t[i - rad[i] - 1] == t[i + rad[i] + 1]) {
            rad[i]++; // one more matching pair around i
        }
        if (i + rad[i] > right) { // this palindrome reaches farther right than any before
            center = i;
            right = i + rad[i];
        }
    }
    return rad;
}
```

#### Reading Off The Longest Palindrome

The third method takes the finished radius array, scans it once and keeps the first maximum. The strict comparison keeps the leftmost center on a tie, and a smaller center index gives a smaller start index in the original string.

```java
static int[] longestFromRadii(int[] rad) {
    int bestCenter = 0;
    for (int i = 1; i < rad.length; i++) {
        if (rad[i] > rad[bestCenter]) bestCenter = i; // strictly larger keeps the leftmost on ties
    }
    return new int[] {(bestCenter - rad[bestCenter]) / 2, rad[bestCenter]};
}
```

#### Checking Cost And Java Details

- **radii** costs O(n) time, because `right` only moves forward and each position adds at most one failed comparison.
- **radii** uses O(n) space, because `rad` and `t` each hold `2n + 1` values.
- **longestFromRadii** costs one more O(n) pass and no extra array.

The separator `#` must be a character that cannot occur in the input, so the code assumes an alphabet of letters and digits. A Java `char` is one UTF-16 code unit, so a character outside the Basic Multilingual Plane occupies two units and the scan would treat its halves as separate characters. A caller with such text should first convert it to an array of code points.

<!-- stage: applicability -->
### Deciding When Radii Fit

#### Reading The Recognition Cue

Use the technique when a problem asks about palindromic substrings at every center, such as the longest one, the count of all of them, or whether a given range is a palindrome after a lookup. A hint is a statement that needs both odd and even lengths and gives a length limit of tens of thousands or more, where a quadratic expansion would time out. The invariant to hold in mind is that the radii left of `i` are final and that `right` is the farthest known matching index.

#### Naming The False Friend

The nearest false friend is the longest palindromic subsequence, which allows skipped characters. It looks like the same question, but the position rule differs and the radii do not apply, because a subsequence has no center to expand around. That problem belongs to dynamic programming over two indexes. A second false friend is the prefix function from the previous lesson. It also reuses earlier work after a mismatch, but it measures prefixes that are suffixes, and a palindrome has no such relation to the start of the string.

#### Knowing When Not To Use It

Do not use radii when palindromes may contain mismatches, because the mirror argument needs exact equality. Do not use them for short inputs with limits near 1,000, where center expansion is simpler and fast enough. Do not forget the separator assumption: a string that already contains `#` breaks the transform, so choose a character outside the alphabet or compare original indexes without building the padded array.

<!-- stage: exercises -->
### Exercises

#### [Build] Expand Odd Centers (Author exercise)
<!-- id: as-expand-odd-centers -->

**Prerequisites.** The direct expansion method from this lesson.

**Problem.** Let `s` be a string. For each index `c` of `s`, the odd radius of `c` is the largest integer `k >= 0` such that `c - k >= 0`, `c + k < s.length()`, and the characters from index `c - k` through index `c + k` form a palindrome, meaning they equal their own reverse. Return an array `odd` of length `s.length()` where `odd[c]` is the odd radius of `c`. Compute each value by expanding outward from `c` one pair of characters at a time.

**Constraints.** The limits are:
- **Length** satisfies `1 <= s.length() <= 1000`.
- **Characters** are lowercase English letters.
- **Answer** is an `int[]` of the same length as `s`.
- **Mutation** does not occur.

**Example 1.** Input `s = "abaab"`, output `[0, 1, 0, 0, 0]`.

**Example 2.** Input `s = "aaaaa"`, output `[0, 1, 2, 1, 0]`, because the radius at each index is limited by the nearer end of the string.

**Hint.** Compare `s[c - k - 1]` with `s[c + k + 1]` before you increase `k`. What stops the loop at the ends of the string?

**Changed decision.** Basic case: each center expands alone, and no result from a neighbouring center is reused.

#### [Vary] Unified Separators (Author exercise)
<!-- id: as-unified-separators -->

**Prerequisites.** The odd radius exercise above.

**Problem.** Let `s` be a string of lowercase letters, and let `t` be the string formed by writing `#` before the first letter, between every pair of neighbouring letters, and after the last letter, so `t.length() == 2 * s.length() + 1`. The radius of index `i` in `t` is the largest `k >= 0` such that `i - k >= 0`, `i + k < t.length()`, and `t[i - k .. i + k]` is a palindrome. Return the array `rad` of length `t.length()` that holds the radius of every index of `t`. This version changes one decision from the previous exercise: odd and even palindromes of `s` are now both read as odd palindromes of `t`.

**Constraints.** The limits are:
- **Length** satisfies `1 <= s.length() <= 1000`.
- **Characters** are lowercase English letters, so `#` never occurs in `s`.
- **Answer** is an `int[]` of length `2 * s.length() + 1`.
- **Mutation** does not occur.

**Example 1.** Input `s = "abba"`, output `[0, 1, 0, 1, 4, 1, 0, 1, 0]`, where the value 4 at index 4 stands for the even palindrome `abba`.

**Example 2.** Input `s = "aa"`, output `[0, 1, 2, 1, 0]`, where the value 2 at index 2 is the gap between the two letters.

**Hint.** Which index of `t` holds the gap between `s[0]` and `s[1]`, and what is the radius there when both letters are equal?

**Changed decision.** Both parities share one array, so the same loop that handled odd centers now handles gaps.

#### [Boundary] Mirror Beyond Boundary (Author exercise)
<!-- id: as-mirror-beyond-boundary -->

**Prerequisites.** The radius array of the previous exercise and the copy rule from this lesson.

**Problem.** Let `s` be a string of lowercase letters and let `t` and the radius of every index of `t` be defined as in the previous exercise. Return the radius array `rad` of `t` by scanning `t` once from left to right. The scan keeps the finished palindrome whose right edge `right = center + rad[center]` is farthest right. For an index `i < right`, it starts `rad[i]` at the smaller of `right - i` and `rad[2 * center - i]`, and then it expands. For `s = "abab"` an unbounded copy of `rad[2 * center - i]` would give a wrong radius, so the bound `right - i` is the point of this exercise.

**Constraints.** The limits are:
- **Length** satisfies `1 <= s.length() <= 100000`.
- **Characters** are lowercase English letters.
- **Answer** is an `int[]` of length `2 * s.length() + 1`.
- **Mutation** does not occur.

**Example 1.** Input `s = "abab"`, output `[0, 1, 0, 3, 0, 3, 0, 1, 0]`, where index 7 holds 1 and not 3.

**Example 2.** Input `s = "aaabaa"`, output `[0, 1, 2, 3, 2, 1, 0, 5, 0, 1, 2, 1, 0]`, where an unbounded copy would leave 3 at index 11.

**Hint.** At index 7 of `abab`, how many positions remain between `i` and the right edge of the palindrome centered at index 5?

**Changed decision.** The copied radius is limited by the distance to the known right edge before any further comparison.

#### [Recognize] Longest Palindromic Substring (LeetCode 5)
<!-- id: as-longest-palindrome-radii -->

**Prerequisites.** All three exercises above.

**Problem.** Let `s` be a string. A palindromic substring is a contiguous block of `s` that equals its own reverse. Return an array `{start, length}` for a longest palindromic substring of `s`, where `start` is the 0-based index of its first character. When several have the longest length, return the one with the smallest `start`. This repeats LeetCode 5, which the strings chapter solved by center expansion, and the contract here differs in two ways: the length limit is 100,000, and the answer is a start index with a length and not the substring itself.

**Constraints.** The limits are:
- **Length** satisfies `1 <= s.length() <= 100000`.
- **Characters** are English letters and digits.
- **Answer** is an `int[]` of two values, and the length is at least 1.
- **Ties** go to the smallest start index.
- **Mutation** does not occur.

**Example 1.** Input `s = "babad"`, output `[0, 3]`, because `bab` and `aba` both have length 3 and `bab` starts first.

**Example 2.** Input `s = "abcbaxdefed"`, output `[0, 5]`, because `abcba` and `defed` both have length 5 and `abcba` starts first.

**Hint.** Which center index of the separator string holds the largest radius, and how does the start index of the original string follow from that center and radius?

**Changed decision.** The radii of every center are computed once, and the answer is read from them instead of being tracked during expansion.
