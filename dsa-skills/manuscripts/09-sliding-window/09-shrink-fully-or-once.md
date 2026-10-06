<!-- lesson-kind: standard -->
<!-- lesson-id: shrink-fully-or-once -->
## Shrink Fully Or Shrink Once

<!-- stage: context -->
### A Scan At Every Step

A text tool must find the longest stretch that becomes one repeated character after at most `k` replacements. The text uses the full range of 16-bit characters, so the alphabet has 65,536 symbols. The tool keeps one count per symbol and scans all 65,536 counts to find the largest one whenever it tests the window. On a text of one million characters, that test alone costs about 65 billion steps.

A colleague suggests keeping the largest count seen so far and never recomputing it. Another colleague suggests a quick fix for slow window code in general: replace each `while` with an `if`. Keeping the largest count so far is safe for this problem. Replacing `while` with `if` breaks the duplicate-free problem. The question of this lesson is how to tell them apart.

<!-- stage: naive -->
### Scan All Counts At Every Test

The direct method follows the previous lesson. It keeps a count per symbol, and each time it tests the window, it scans the whole count array for the largest entry.

```java
static int longestWide(String s, int k) {
    int[] cnt = new int[65536];
    int left = 0, best = 0;
    for (int right = 0; right < s.length(); right++) {
        cnt[s.charAt(right)]++;
        while (right - left + 1 - maxOf(cnt) > k) {
            cnt[s.charAt(left)]--;
            left++;
        }
        best = Math.max(best, right - left + 1);
    }
    return best;
}

static int maxOf(int[] cnt) {
    int top = 0;
    for (int c : cnt) top = Math.max(top, c);
    return top;
}
```

The window is valid after every shrink, and the answer is exact.

<!-- stage: bottleneck -->
### Measuring The Cost Of The Scan

```predict
The best valid length found so far is 5 with k = 2, so some window had a dominant count of 3. Can a longer valid window exist without some letter reaching a count above 3?

No. A valid window of length 6 or more with k = 2 needs a dominant count of at least 4. So only a letter count above the old maximum can produce a longer answer, and the method needs just the largest count seen so far.
```

Let `A` be the alphabet size. Each loop test scans `A` counts, and the test runs at least once for each of the `n` indexes. The total is O(A * n). For `A = 65,536` and `n = 1,000,000`, that is about 65 billion steps. A heap or a sorted structure would lower the scan, but it adds a logarithm and a lot of code.

The prediction shows why a scan is more than the answer needs. A longer answer requires a count that is larger than any count seen before. The method does not need the exact dominant count of the current window. It needs to notice when a count exceeds the best one seen. That observation leads to a different window, one that keeps a length and does not always keep a valid block.

<!-- stage: insight -->
### Keep A Valid Window Or A Length

#### Full Shrink Keeps The Window Valid

A **full shrink** is the loop of the earlier lessons. After it, the window is valid, and every statement about the counts describes a legal block. The loop may remove several values for one new value. This form works for every window problem whose condition survives removal.

#### One Removal Keeps A Candidate Length

A **one removal** form lets `left` move at most once for each `right`. The window length never decreases. When the entering value keeps the cost within `k`, the window grows by one. Otherwise, the window slides by one, with `left` and `right` both moving forward. The window may be invalid at some steps. Its length is a **candidate length**: the best valid length found so far, and not the length of a valid block. The answer is the final window length.

#### When One Removal Is Safe

The one removal form needs a separate proof for each problem. For the replacement budget, three facts give the proof. First, until the first slide, the window only grows, so the largest count seen equals the exact dominant count.

Second, after a slide, the length equals the largest count seen plus `k`. The cost test then fails exactly when the length would grow without a larger count.

Third, the largest count grows only when the entering letter reaches a count above the old maximum. The current window then has cost exactly `k` and is valid. The invariant is that the window length equals the best valid length of the prefix.

The same form is wrong for the duplicate-free problem. There, one removal of a single value may leave the repeated value inside the window, and no counting argument rescues the length.

<!-- names: full shrink, one removal, candidate length -->

<!-- stage: variables -->
### What Each Form Keeps

The two forms keep different state, and the difference is the lesson.

- **left** and **right** are the boundaries of the window in both forms.
- **cnt** is the count array of the window, and it describes `s[left..right]` in both forms.
- **peak** is the largest count seen in any step of the one removal form, and it never decreases.
- **length** is `right - left + 1`, and the one removal form never lets it shrink.
- **best** is kept only by the full shrink form, since the one removal form returns the final length.

<!-- stage: trace -->
### Tracing Two Scans

#### One Removal On A Replacement Budget

Take `s = "AAABCD"` and `k = 1`. The trace below shows the window text, the variable `peak`, and whether the window is valid. The window grows to `AAAB` and stays valid. Then `C` enters, and the cost of `AAABC` is 2, so the window slides by one. The window `AABC` is invalid, because it has cost 2, but its length 4 equals the best valid length so far.

```trace
{"cells":["A","A","A","B","C","D"],"pointers":["left","right"],"steps":[{"at":{"left":0,"right":0},"vars":{"window":"A","peak":"1","valid":"yes"},"note":"The letter 'A' enters, so peak is 1. The cost is within the budget, so the window grows. The window 'A' is valid."},{"at":{"left":0,"right":1},"vars":{"window":"AA","peak":"2","valid":"yes"},"note":"The letter 'A' enters, so peak is 2. The cost is within the budget, so the window grows. The window 'AA' is valid."},{"at":{"left":0,"right":2},"vars":{"window":"AAA","peak":"3","valid":"yes"},"note":"The letter 'A' enters, so peak is 3. The cost is within the budget, so the window grows. The window 'AAA' is valid."},{"at":{"left":0,"right":3},"vars":{"window":"AAAB","peak":"3","valid":"yes"},"note":"The letter 'B' enters, so peak is 3. The cost is within the budget, so the window grows. The window 'AAAB' is valid."},{"at":{"left":1,"right":4},"vars":{"window":"AABC","peak":"3","valid":"no"},"note":"The letter 'C' enters, so peak is 3. The length 5 minus peak 3 is 2, above 1, so the letter 'A' leaves and the window slides. The window 'AABC' is invalid, with exact cost 2."},{"at":{"left":2,"right":5},"vars":{"window":"ABCD","peak":"3","valid":"no"},"note":"The letter 'D' enters, so peak is 3. The length 5 minus peak 3 is 2, above 1, so the letter 'A' leaves and the window slides. The window 'ABCD' is invalid, with exact cost 3."}]}
```

The final length is 4, which is the correct answer. The invalid windows at the last two steps do not change the length.

#### One Removal On Duplicates

Take `s = "abcdbea"` and replace the `while` loop of the duplicate-free scan with an `if`. At index 4, the window `abcdb` holds two copies of `b`. One removal drops `a`, and `bcdb` still holds both copies. The scan treats the window as valid and records its length. The scan later reports 6, while the longest duplicate-free substring has length 5.

```trace
{"cells":["a","b","c","d","b","e","a"],"pointers":["left","right"],"steps":[{"at":{"left":0,"right":0},"vars":{"window":"a","repeat":"no","best":"1"},"note":"The character 'a' enters. The window 'a' has no repeat, and best is 1."},{"at":{"left":0,"right":1},"vars":{"window":"ab","repeat":"no","best":"2"},"note":"The character 'b' enters. The window 'ab' has no repeat, and best is 2."},{"at":{"left":0,"right":2},"vars":{"window":"abc","repeat":"no","best":"3"},"note":"The character 'c' enters. The window 'abc' has no repeat, and best is 3."},{"at":{"left":0,"right":3},"vars":{"window":"abcd","repeat":"no","best":"4"},"note":"The character 'd' enters. The window 'abcd' has no repeat, and best is 4."},{"at":{"left":1,"right":4},"vars":{"window":"bcdb","repeat":"yes","best":"4"},"note":"The character 'b' enters. The count of 'b' is 2, so one character leaves: 'a'. The window 'bcdb' has a repeated character, and best is 4."},{"at":{"left":1,"right":5},"vars":{"window":"bcdbe","repeat":"yes","best":"5"},"note":"The character 'e' enters. The window 'bcdbe' has a repeated character, and best is 5."},{"at":{"left":1,"right":6},"vars":{"window":"bcdbea","repeat":"yes","best":"6"},"note":"The character 'a' enters. The window 'bcdbea' has a repeated character, and best is 6."}]}
```

<!-- stage: code -->
### The One Removal Form In Java

#### Sliding Without A Scan

```java
static int longestWithBudget(String s, int k) {
    // 128 entries suffice for ASCII text; 16-bit text needs 65536 entries.
    int[] cnt = new int[128];
    int left = 0, peak = 0;
    for (int right = 0; right < s.length(); right++) {
        char c = s.charAt(right);
        cnt[c]++;
        peak = Math.max(peak, cnt[c]);
        if (right - left + 1 - peak > k) {
            cnt[s.charAt(left)]--;
            left++;
        }
    }
    return s.length() - left;
}
```

The `if` is safe here because of the proof in the insight. The method never scans the counts, and it returns the final window length, since `right + 1 == s.length()` after the loop.

#### Cost Of The Form

Each step does a constant amount of work, so the time is O(n), with no factor for the alphabet. The count array has 128 entries, which suffices for ASCII input. Text of 16-bit characters needs 65,536 entries, as in the first method of this lesson. The method does not record a best length, because the length never decreases.

<!-- stage: applicability -->
### Choosing The Shrink Policy

#### Which Policy Fits The Problem

Use a full shrink whenever the problem needs a valid window when it records. Examples are a count of ranges, a shortest cover and a duplicate-free length. Use one removal only when a separate argument shows that a window of the best length cannot hide a better answer. For the replacement budget, that argument is the three facts of the insight.

#### The Invariant To State

Write down which statement the loop maintains. A full shrink keeps the statement "the window is valid". A one removal form keeps the statement "the window length equals the best valid length so far", and the window may be invalid. Mixing the two statements leads to measuring an invalid window as if it were valid.

#### Replacing While With If Is A False Friend

A loop that looks slow tempts a reader to change `while` to `if`. The change is not an optimization rule. It gives the right answer only for problems with a proof like the one above. For the duplicate-free problem, it returns 6 for `abcdbea`, and the true answer is 5.

#### Java Habits For This Pattern

Write the invariant as a comment above the loop. Name the variable `peak` and not `max`, so a reader sees that it is a historical value. Return `s.length() - left` only for the one removal form. Test the shortcut against the full shrink form on random inputs before you trust it.

<!-- stage: exercises -->
### Exercises

#### [Build] Restore Before Record (Author exercise)
<!-- id: sw-restore-before-record -->

**Prerequisites.** The full shrink form of this lesson and of the longest-valid lesson.

**Problem.** Given a string `s`, return an `int[]` of two entries, `{start, length}`, for the leftmost longest substring in which no character occurs twice. The method restores validity with a `while` loop before it measures the window. An assertion confirms that the window is valid at that moment.

**Constraints.**
- **Length** satisfies `0 <= s.length <= 10^5`.
- **Characters** are ASCII characters, codes 0 to 127.
- **Ties** go to the smallest start.
- **Empty input** returns `{0, 0}`.
- **Mutation** does not occur; `s` is immutable.

**Example 1.** Input `s = "abcdbea"`. Output `{2, 5}`.

**Example 2.** Input `s = "bbbbb"`. Output `{0, 1}`.

**Hint.** Which comparison keeps the leftmost start when two windows have the same length?

**Changed decision.** The method reports a position and a length, and it asserts validity before each measurement.

#### [Vary] One-Removal Maximum-Length Trace (Author exercise)
<!-- id: sw-one-removal-trace -->

**Prerequisites.** The exercise above.

**Problem.** Given a string `s` of uppercase letters and an integer `k`, run the one removal form of this lesson. After the step for each index `r`, call the window `s[left..r]` invalid when its length minus its exact dominant count exceeds `k`. Return an `int[]` of two entries: the final window length, and the number of indexes `r` after which the window is invalid.

**Constraints.**
- **Length** satisfies `1 <= s.length <= 10^5`.
- **Characters** are uppercase English letters.
- **Budget** satisfies `0 <= k <= s.length`.
- **Return** type is `int[]` with two entries.
- **Mutation** does not occur; `s` is immutable.

**Example 1.** Input `s = "AAABCD"`, `k = 1`. Output `{4, 2}`.

**Example 2.** Input `s = "ABAB"`, `k = 2`. Output `{4, 0}`.

**Hint.** The final length is `s.length - left`. What does the exact dominant count of the window require?

**Changed decision.** The window length is a candidate length, and the exercise counts the steps where the window is not a valid block.

#### [Boundary] Multiple Left Removals Needed (Author exercise)
<!-- id: sw-multiple-removals -->

**Prerequisites.** The two exercises above.

**Problem.** Given a string `s`, return the best length that a duplicate-free scan reports when it replaces the `while` loop with an `if`. The scan adds the entering character to the counts and, if its count exceeds 1, removes one character at `left`. After every step it records `right - left + 1` in `best`. The exercise returns `best`, which may exceed the true answer.

**Constraints.**
- **Length** satisfies `0 <= s.length <= 10^5`.
- **Characters** are lowercase English letters.
- **Return** type is `int`.
- **Mutation** does not occur; `s` is immutable.

**Example 1.** Input `s = "abcdbea"`. Output `6`, and the true answer is 5.

**Example 2.** Input `s = "abcabc"`. Output `3`, and the true answer is 3.

**Hint.** After one removal at index 4 of `abcdbea`, is the repeated `b` still inside the window?

**Changed decision.** The method makes one removal where several are needed, and the window keeps a duplicate.

#### [Recognize] Longest Repeating Character Replacement (LeetCode 424)
<!-- id: sw-wide-replacement -->

**Prerequisites.** All three exercises above.

**Problem.** Given a string `s` of arbitrary 16-bit characters and an integer `k`, return the length of the longest substring that becomes one repeated character after at most `k` replacements. The method must run in O(n) time and must not scan the count array inside the loop. You met this problem in lesson 07; now the alphabet has 65,536 symbols, so a scan of the counts costs too much.

**Constraints.**
- **Length** satisfies `1 <= s.length <= 10^6`.
- **Characters** are any 16-bit `char` values, codes 0 to 65535.
- **Budget** satisfies `0 <= k <= s.length`.
- **Return** type is `int`.
- **Mutation** does not occur; `s` is immutable.

**Example 1.** Input `s = "AABABBA"`, `k = 1`. Output `4`.

**Example 2.** Input `s = "ABCDE"`, `k = 0`. Output `1`.

**Hint.** Which value replaces the scan, and why can it be stale without harm?

**Changed decision.** The alphabet is too large to scan, so the method keeps the largest count seen and slides without shrinking fully.
