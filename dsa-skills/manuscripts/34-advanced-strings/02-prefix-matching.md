<!-- lesson-kind: standard -->
<!-- lesson-id: prefix-matching -->
## Match A Pattern Without Restarting

<!-- stage: context -->
### Why A Search Freezes On Repeated Text

A log viewer opens a two-megabyte export in which a faulty exporter padded every line with the letter `a`. An engineer searches for `aaaaaaaaab`, a pattern of nine letters `a` followed by one `b`. The search should finish at once, yet the viewer lags far behind what a single pass over the text would cost. The text holds about two million characters, and the viewer is comparing the pattern against almost every start position, nine characters deep each time, before the final `b` rejects it.

The same failure appears in any tool that scans text for a fixed pattern, such as a find command, a log filter or a file importer that looks for a marker line. The lesson asks one question. After a mismatch, what must the scan remember so that it never re-reads a text character it has already matched?

<!-- stage: naive -->
### Trying Every Start Position

The direct method tries each start position in the text. At a start `s` it compares the pattern with the text one character at a time. When a character differs, the method discards the progress and tries start `s + 1`.

```java
static int firstStart(String text, String pattern) {
    for (int s = 0; s + pattern.length() <= text.length(); s++) {
        int j = 0;
        while (j < pattern.length() && text.charAt(s + j) == pattern.charAt(j)) j++;
        if (j == pattern.length()) return s;
    }
    return -1;
}
```

On text `aaaaaaaaaaab` with pattern `aaab` the method matches three letters at the first start, fails on the fourth, and repeats that work at the next start. It is correct, and it uses no extra memory.

<!-- stage: bottleneck -->
### Counting The Repeated Comparisons

```predict
The text is 100 000 letters `a` and the pattern is 500 letters `a` followed by `b`. About how many character comparisons does the start-by-start method make, and which comparisons repeat?

About 50 million comparisons, because roughly 100 000 starts each match 500 letters before the `b` fails. Each text character is compared against up to 500 different pattern positions, and almost all of those comparisons were already implied by the previous start.
```

For a text of length `n` and a pattern of length `m`, the method makes up to `(n - m + 1) * m` comparisons, which is O(n * m). With `n = 2 000 000` and `m = 10` that is about 20 million comparisons, and with a 1 000-letter pattern it is about two billion.

The waste has a precise form. Suppose the scan matched the first five pattern characters at some start and then failed. Those five matched characters are the five text characters just read, so their content is known exactly. The restart reads them again, even though the pattern alone tells which shorter prefix of the pattern those same text characters already match.

The repeated work is therefore a re-comparison of text characters whose values the scan has already verified. A scan that moves the text index backward is the signal. The next section names the information that removes the backward move.

<!-- stage: insight -->
### Remembering The Longest Reusable Match

#### The Prefix Function

Take the prefix `p[0..i]`, which holds the first `i + 1` characters of the pattern. A **border** of `p[0..i]` is a non-empty string that is both a proper prefix of it and a suffix of it. A proper prefix is a prefix shorter than the whole string. The **prefix function** `pi` of the pattern stores, for each index `i`, the length of the longest border of `p[0..i]`, and 0 when no border exists.

<!-- names: prefix function, border, fallback -->

For the pattern `ababaca`, the prefix `ababa` has the borders `a` and `aba`, so `pi[4] = 3`.

#### Why A Mismatch Needs No Restart

Suppose `k` pattern characters currently match the end of the text read so far, and the next text character differs from `p[k]`. The matched characters equal `p[0..k-1]`. Any shorter match that could still be alive must be a prefix of the pattern that is also a suffix of `p[0..k-1]`, which is exactly a border of it. The longest such border has length `pi[k - 1]`.

The scan therefore sets `k` to `pi[k - 1]` and compares the same text character again. This step is a **fallback**. If the character still differs, another fallback uses the next shorter border, and the chain ends at `k = 0`. The text index never moves backward.

#### Why The Total Work Is Linear

Each text character raises `k` by at most 1, and each fallback lowers `k` by at least 1. The value of `k` never goes below 0, so the total number of fallbacks over the whole scan cannot exceed the total number of increases, which is at most `n`. The same argument builds `pi` itself in O(m) time, because building `pi` is a match of the pattern against itself.

<!-- stage: variables -->
### State Kept During The Scan

The array construction and the search keep the same small state.

- **p** is the pattern, read by index and never copied.
- **pi** is the int array where `pi[i]` is the longest border length of `p[0..i]`.
- **k** is the matched length: the number of pattern characters that equal the end of the text read so far.
- **i** is the text index (or the pattern index while building `pi`) and only moves forward.
- **n** and **m** are the text length and the pattern length.

The state invariant is that `k` is the largest value less than `m` (or equal to `m` at a full match) for which `p[0..k-1]` is a suffix of the text read so far.

<!-- stage: trace -->
### Tracing The Fallbacks On ababaca

#### Building The Array For ababaca

The pattern `ababaca` is the case to study, because its mismatch at index 5 triggers two fallbacks in a row. In the trace below, the pointer `i` is the index being read and the pointer `k` is the matched length.

The scan reads `b` at index 1 and finds no match with `p[0] = a`, so `pi[1]` stays 0. Indexes 2, 3 and 4 match `a`, `b`, `a` against `p[0]`, `p[1]`, `p[2]`, so `k` grows to 3. At index 5 the character `c` differs from `p[3] = b`. The first fallback sets `k = pi[2] = 1`, and `c` still differs from `p[1] = b`. The second fallback sets `k = pi[0] = 0`, and `c` differs from `p[0] = a`, so `pi[5] = 0`. At index 6 the character `a` matches `p[0]`, so `pi[6] = 1`. The finished array is `0, 0, 1, 2, 3, 0, 1`. The two consecutive fallbacks at index 5 are the reason the pattern is a good test: one fallback is not enough there. After the first fallback the length is 1 and `c` still fails against `p[1]`. The chain must continue to length 0 before the scan can give up on `c`.

```trace
{"cells":["a","b","a","b","a","c","a"],"pointers":["i","k"],"steps":[{"at":{"i":0,"k":0},"vars":{"pi":"0"},"note":"pi[0] is 0 because a one-character prefix has no proper prefix. The matched length k starts at 0."},{"at":{"i":1,"k":0},"vars":{"pi":"0,0"},"note":"i = 1: no border is left to try. The character 'b' is not p[0], and pi[1] stays 0."},{"at":{"i":2,"k":1},"vars":{"pi":"0,0,1"},"note":"i = 2: the character 'a' matches p[0], the next expected pattern character, and k rises to 1, which is also the new border length."},{"at":{"i":3,"k":2},"vars":{"pi":"0,0,1,2"},"note":"i = 3: the character 'b' matches p[1], the next expected pattern character, and k rises to 2, which is also the new border length."},{"at":{"i":4,"k":3},"vars":{"pi":"0,0,1,2,3"},"note":"i = 4: the character 'a' matches p[2], the next expected pattern character, and k rises to 3, which is also the new border length."},{"at":{"i":5,"k":1},"vars":{"pi":"0,0,1,2,3"},"note":"i = 5: p[3] is 'b' and rejects 'c'. A fallback sets k to pi[2] = 1, the next shorter border, without moving i."},{"at":{"i":5,"k":0},"vars":{"pi":"0,0,1,2,3"},"note":"i = 5: p[1] is 'b' and rejects 'c'. A fallback sets k to pi[0] = 0, the next shorter border, without moving i."},{"at":{"i":5,"k":0},"vars":{"pi":"0,0,1,2,3,0"},"note":"i = 5: no border is left to try. The character 'c' is not p[0], and pi[5] stays 0."},{"at":{"i":6,"k":1},"vars":{"pi":"0,0,1,2,3,0,1"},"note":"i = 6: the character 'a' matches p[0], the next expected pattern character, and k rises to 1, which is also the new border length."}]}
```

#### Scanning A Text With The Array

Now the same array drives a scan of the text `abababaca`. The pointer `i` is the text index, and the pointer `k` is the number of pattern characters matched.

The first five letters match the pattern prefix `ababa`, so `k` reaches 5. The sixth letter is `b`, but `p[5]` is `c`. One fallback sets `k = pi[4] = 3`, which says that the last three text characters `aba` still match the pattern start. The letter `b` then equals `p[3]`, so `k` grows to 4 without the text index moving. The scan continues, reaches `k = 7` at index 8, and reports the start 2. A restart-based scan would have returned to index 1 after the mismatch and read five letters again. The saving is visible in the count of reads: the text has nine characters, and the trace performs one read for each of them plus one extra comparison after the fallback, ten comparisons in total, whereas the start-by-start method repeats the five-letter partial match.

```trace
{"cells":["a","b","a","b","a","b","a","c","a"],"pointers":["i","k"],"steps":[{"at":{"i":0,"k":1},"vars":{"matched":1},"note":"i = 0: text character 'a' agrees with p[0], so the match is now 1 character long."},{"at":{"i":1,"k":2},"vars":{"matched":2},"note":"i = 1: text character 'b' agrees with p[1], so the match is now 2 characters long."},{"at":{"i":2,"k":3},"vars":{"matched":3},"note":"i = 2: text character 'a' agrees with p[2], so the match is now 3 characters long."},{"at":{"i":3,"k":4},"vars":{"matched":4},"note":"i = 3: text character 'b' agrees with p[3], so the match is now 4 characters long."},{"at":{"i":4,"k":5},"vars":{"matched":5},"note":"i = 4: text character 'a' agrees with p[4], so the match is now 5 characters long."},{"at":{"i":5,"k":3},"vars":{"matched":3},"note":"i = 5: p[5] is 'c' but the text holds 'b'. One fallback replaces 5 by pi[4] = 3, and the same text index is compared again."},{"at":{"i":5,"k":4},"vars":{"matched":4},"note":"i = 5: text character 'b' agrees with p[3], so the match is now 4 characters long."},{"at":{"i":6,"k":5},"vars":{"matched":5},"note":"i = 6: text character 'a' agrees with p[4], so the match is now 5 characters long."},{"at":{"i":7,"k":6},"vars":{"matched":6},"note":"i = 7: text character 'c' agrees with p[5], so the match is now 6 characters long."},{"at":{"i":8,"k":7},"vars":{"matched":7},"note":"i = 8: text character 'a' agrees with p[6], so the match is now 7 characters long. k equals the pattern length 7, so the first occurrence starts at 8 - 7 + 1 = 2."}]}
```

<!-- stage: code -->
### Building The Array And Searching

#### The Two Methods

Both methods use only index reads, so they allocate nothing except the array. The names `border` and `matched` in this code correspond to the border length and the matched length `k` of the trace.

```java
// Longest border length for every prefix of the pattern.
static int[] borderLengths(String pat) {
    int[] pi = new int[pat.length()];
    int border = 0;
    for (int i = 1; i < pat.length(); i++) {
        while (border > 0 && pat.charAt(i) != pat.charAt(border)) border = pi[border - 1];
        if (pat.charAt(i) == pat.charAt(border)) border++;
        pi[i] = border;
    }
    return pi;
}

// First start of pat inside text, or -1. An empty pattern returns 0.
static int scanForPattern(String text, String pat) {
    if (pat.isEmpty()) return 0;
    int[] pi = borderLengths(pat);
    int matched = 0;
    for (int i = 0; i < text.length(); i++) {
        while (matched > 0 && text.charAt(i) != pat.charAt(matched)) matched = pi[matched - 1];
        if (text.charAt(i) == pat.charAt(matched)) matched++;
        if (matched == pat.length()) return i - pat.length() + 1;
    }
    return -1;
}
```

#### Cost And Java Details

- **borderLengths** costs O(m) time and O(m) space for the array.
- **scanForPattern** costs O(n + m) time in total, because the text index advances once per iteration and fallbacks are paid for by earlier growth.

The empty-pattern guard matters, because the first comparison would otherwise read `pat.charAt(0)` on an empty string and throw. The methods compare UTF-16 code units from `charAt`, so the lesson assumes text in which each character is one code unit, such as lowercase English letters.

<!-- stage: applicability -->
### When The Prefix Function Applies

#### Recognizing The Pattern

Use this technique when one fixed pattern is matched against text that may contain long partial matches, or when a problem asks about the prefixes of a string that are also suffixes. The statement often reads as the longest prefix that is also a suffix, the period of a string, or a search that must run in linear time.

The invariant to state before coding is that `k` is the longest pattern prefix that is a suffix of the text read so far. Every fallback keeps that statement true, and every other move follows from it.

#### Two False Friends

The Z array looks like a close relative, because it is also an array of match lengths. It is a false friend of the prefix function. The **Z array** `z` stores, for each index `i`, the length of the longest common prefix of the whole string and the suffix that starts at `i`. The value `z[i]` looks forward from `i`. The value `pi[i]` looks backward and gives the longest border of `p[0..i]`. For `aabxaab` the Z array is `7,1,0,0,3,1,0` and the prefix function is `0,1,0,0,1,2,3`. At index 4 the suffix `aab` matches the prefix for 3 characters, so `z[4] = 3`, while the longest border of `aabxa` is only `a`, so `pi[4] = 1`.

A second false friend is the rolling hash from the previous lesson. It also avoids restarting, yet an equal hash does not prove an equal string, while the prefix function compares characters and is exact.

#### When Not To Use It

Do not use it when the pattern is short and the text is small, because the library `indexOf` is clear enough. Do not use it for many patterns at once, since a trie with failure links serves that case. Do not use it when the match allows wildcards or edits, because a border no longer describes the reusable part.

<!-- stage: exercises -->
### Exercises

#### [Build] Prefix Function (Author exercise)
<!-- id: as-prefix-function -->

**Prerequisites.** The border and prefix function definitions and the fallback step from this lesson.

**Problem.** A proper prefix of a string is a prefix whose length is less than the length of the string. A border of a string is a non-empty string that is both a proper prefix and a suffix of it. Given a string `p`, return an `int` array `pi` of the same length in which `pi[i]` is the length of the longest border of `p[0..i]`, and 0 when `p[0..i]` has no border.

**Constraints.** The limits are:
- **Length** is `0 <= p.length() <= 10^5`.
- **Characters** are lowercase English letters, each one UTF-16 code unit.
- **Empty input** returns an empty array.
- **Mutation** does not occur; `p` is immutable.

**Example 1.** Input `p = "aabaaab"`, output `[0,1,0,1,2,2,3]`.

**Example 2.** Input `p = "abcabcabd"`, output `[0,0,0,1,2,3,4,5,0]`. The border grows to 5 and collapses to 0 at the last character.

**Hint.** When `p[i]` differs from `p[k]`, which shorter border of the first `k` characters is the next to try, and where is its length stored?

**Changed decision.** Basic case: a mismatch replaces the current length by a stored shorter length and never restarts from 0.

#### [Vary] First Occurrence With KMP (LeetCode 28)
<!-- id: as-first-occurrence-kmp -->

**Prerequisites.** The Prefix Function exercise above.

**Problem.** Given strings `text` and `pattern`, return the smallest index `s` such that `text` has `pattern` as a substring starting at `s`, or -1 when no such index exists. In this lesson the pattern may be empty, and an empty pattern occurs at index 0. The text index must not move backward during the scan.

**Constraints.** The limits are:
- **Text length** is `0 <= text.length() <= 10^5`.
- **Pattern length** is `0 <= pattern.length() <= 10^5`.
- **Characters** are lowercase English letters, each one UTF-16 code unit.
- **Empty pattern** returns 0, even when the text is empty.
- **Mutation** does not occur; both strings are immutable.

**Example 1.** Input `text = "abababaca"`, `pattern = "ababaca"`, output 2.

**Example 2.** Input `text = "aaaaab"`, `pattern = "aab"`, output 3. The scan matches `aa` at several starts before the real occurrence.

**Hint.** What does the matched length become when `text[i]` differs from `pattern[k]`, and does the text index change?

**Changed decision.** The output changes from an array of lengths to the first start index, which is computed as `i - m + 1` when `k` reaches `m`.

#### [Boundary] Repeated Prefixes (Author exercise)
<!-- id: as-repeated-prefixes -->

**Prerequisites.** The Prefix Function exercise above.

**Problem.** Let `p` be a string and let `k` satisfy `1 <= k <= p.length()`. A border length of the first `k` characters is an integer `L` with `0 < L < k` such that `p[0..L)` equals `p[k-L..k)`. Return all border lengths of the first `k` characters in decreasing order. The pattern `ababaca` with `k = 5` needs two fallbacks to list all of them.

**Constraints.** The limits are:
- **Length** is `1 <= p.length() <= 10^5`.
- **Prefix length** `k` satisfies `1 <= k <= p.length()`.
- **Characters** are lowercase English letters.
- **Empty answer** is an empty array, returned when no border exists.
- **Mutation** does not occur; `p` is immutable.

**Example 1.** Input `p = "ababaca"`, `k = 5`, output `[3,1]`.

**Example 2.** Input `p = "aaaa"`, `k = 1`, output `[]`, because the whole prefix is excluded and no shorter length exists.

**Hint.** Start from `pi[k - 1]`. Is every shorter border also a border of that longest border?

**Changed decision.** The output changes from one length to the full chain of lengths reached by repeated fallback.

#### [Recognize] Longest Happy Prefix (LeetCode 1392)
<!-- id: as-longest-happy-prefix -->

**Prerequisites.** The Prefix Function and Repeated Prefixes exercises above.

**Problem.** A happy prefix of a string `s` is a non-empty string that is a proper prefix of `s` and also a suffix of `s`. Return the longest happy prefix of `s` as a `String`, or the empty string when none exists. The prefix and the suffix may overlap inside `s`.

**Constraints.** The limits are:
- **Length** is `1 <= s.length() <= 10^5`.
- **Characters** are lowercase English letters.
- **Empty answer** is the empty string `""`, never `null`.
- **Mutation** does not occur; `s` is immutable.

**Example 1.** Input `s = "level"`, output `"l"`.

**Example 2.** Input `s = "ababab"`, output `"abab"`. The prefix and the suffix overlap.

**Hint.** Which single entry of the prefix function already holds the length of the answer?

**Changed decision.** The array is no longer the output; only its last entry is read, and the answer is cut from the string at that length.

#### [Extend] Z Array (Author exercise)
<!-- id: as-z-array -->

**Prerequisites.** All four exercises above.

**Problem.** For a string `s` of length `n`, define `z[i]` as the length of the longest common prefix of `s` and the suffix `s[i..]`. Define `z[0] = n` by convention. Return the array `z`. Then explain how the window `[l, r)` of the rightmost match found so far plays the role that the matched length `k` plays in the prefix function.

**Constraints.** The limits are:
- **Length** is `0 <= s.length() <= 10^5`.
- **Characters** are lowercase English letters, each one UTF-16 code unit.
- **Empty input** returns an empty array.
- **Convention** `z[0] = n` for every non-empty string.
- **Mutation** does not occur; `s` is immutable.

**Example 1.** Input `s = "aabxaab"`, output `[7,1,0,0,3,1,0]`.

**Example 2.** Input `s = "aaaaa"`, output `[5,4,3,2,1]`. Each position reuses the entry to its left.

**Hint.** If position `i` lies inside the window that starts at `l`, which earlier entry already describes the same characters, and how far may it be trusted?

**Changed decision.** The state changes from one length `k` of the text read so far to a window of text already compared with the prefix.
