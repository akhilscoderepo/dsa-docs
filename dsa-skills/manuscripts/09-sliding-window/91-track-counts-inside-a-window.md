<!-- lesson-kind: combination -->
<!-- lesson-id: track-counts-inside-a-window -->
## Track Counts Inside A Window

<!-- stage: context -->
### Counts That Describe The Wrong Text

A scanner looks for rearrangements of a short signature inside a data stream. Its author keeps the two boundaries correct, with a left index and a right index that always bound the last few characters. The scanner updates its character counts when a character enters, and it forgets to update them when a character leaves. After a few thousand characters, the counts describe the whole stream and not the window. The scanner then reports matches that do not exist, and it misses real ones.

The boundaries alone cannot answer a question about the contents of the window, and the counts alone do not know which characters are inside. This lesson asks what must stay true about both together, so that one small test per step answers questions of four different kinds.

<!-- stage: contributions -->
### What Boundaries And Counts Each Add

The boundaries name the active range. Two indexes `left` and `right` fix which positions are inside the window, and each move of an index adds or removes exactly one position. The boundaries do not know what the positions hold. They give a length, and they give the order in which positions leave, which is the order of arrival.

The counts record what the active range holds. An array or a map stores how many copies of each character are inside. The counts know the contents, but they do not know which positions to remove next. They need the boundaries to say which character leaves. The same boundaries say which characters no longer belong to the answer.

Only the pair answers the question. A move of `right` adds `s[right]` to the counts, and a move of `left` removes `s[left]` from the counts. The combined statement is that the counts describe exactly the characters at positions `left` through `right`. If one update is missing, the statement breaks, and every later test reads the wrong window.

<!-- stage: naive -->
### Recount The Active Range Each Step

The direct method keeps the two boundaries and rebuilds the counts from the active range at every step. It then tests the rule on the fresh counts.

```java
static int firstMatchByRecount(String s, String p) {
    int k = p.length();
    for (int right = k - 1; right < s.length(); right++) {
        int[] fresh = new int[26];
        for (int i = right - k + 1; i <= right; i++) fresh[s.charAt(i) - 'a']++;
        int[] want = new int[26];
        for (int i = 0; i < k; i++) want[p.charAt(i) - 'a']++;
        if (java.util.Arrays.equals(fresh, want)) return right - k + 1;
    }
    return -1;
}
```

The method is correct, and it never lets the counts drift away from the boundaries.

<!-- stage: bottleneck -->
### Counting The Work Of Each Test

```predict
A status counter holds the number of letters whose window count differs from the pattern count. One letter enters the window. How many letters can change between "matching" and "not matching"?

At most one. Only the entering letter's count changes, so only that letter can change its status, and the status counter changes by at most one.
```

Each step of the recount costs O(k) to rebuild the counts, so the method costs O(n * k). Even with maintained counts, a full comparison costs O(A) per step for alphabet size `A`, and a scan for a dominant count costs the same. The four problems of this lesson ask four different questions about the counts. Do they match exactly? Does any count exceed a limit? Does every count reach a minimum? Does the length minus the largest count fit a budget?

The prediction points to a cheaper test. Each step changes the count of at most two letters, the one that enters and the one that leaves. A single integer can summarise the answer to the rule, and each step can adjust that integer by looking at those two letters only.

<!-- stage: insight -->
### One Counter Answers The Rule

#### The Status Counter

A **status counter** is one integer that says how many letters currently break the rule. The rule differs by problem. An exact match breaks the rule for a letter whose window count differs from its pattern count. A repeat limit breaks the rule for a letter whose count exceeds the limit. A cover breaks the rule for a letter whose count is below its required count. The window is valid exactly when the status counter is 0.

#### The Entering And Leaving Updates

The **entering update** changes the count of one letter and then checks that letter's status again. If the letter was fine and is now broken, the counter rises by one. If it was broken and is now fine, the counter falls by one. The **leaving update** does the same for the letter at `left`. Both updates cost O(1), and each step makes one of each at most.

#### The Combined Invariant

The invariant has two parts. The counts describe exactly `s[left..right]`, and the status counter equals the number of letters that break the rule for those counts. Every test then reads the counter and never scans an array. The budget problem fits the same plan with one change. Its rule is about the whole window and not about each letter. The counter becomes the expression `length - largest count`, and the same two updates keep the counts correct.

<!-- names: status counter, entering update, leaving update -->

<!-- stage: variables -->
### What The Combination Keeps

The combined method keeps four pieces of state, and each has one meaning.

- **left** and **right** bound the active range, and the length is `right - left + 1`.
- **cnt** holds the number of copies of each character inside `s[left..right]`.
- **need** holds the rule for each character: an exact count, a limit, or a minimum.
- **bad** is the status counter, the number of characters whose count breaks the rule.

<!-- stage: trace -->
### Tracing Two Combined Scans

#### A Status Counter For An Exact Match

Take `s = "eidbaooo"` and the pattern `p = "ab"`. The pattern needs one `a` and one `b`. The counter `bad` starts at 2, because both letters have window count 0 and need 1. In the trace below, the pointers `left` and `right` mark the window of length 2, and the variable `bad` shows the counter after each step.

```trace
{"cells":["e","i","d","b","a","o","o","o"],"pointers":["left","right"],"steps":[{"at":{"left":0,"right":0},"vars":{"bad":"3"},"note":"The letter 'e' enters. Its count stops matching, so bad is 3."},{"at":{"left":0,"right":1},"vars":{"bad":"4"},"note":"The letter 'i' enters. Its count stops matching, so bad is 4."},{"at":{"left":1,"right":2},"vars":{"bad":"4"},"note":"The letter 'd' enters. Its count stops matching, so bad is 5. The letter 'e' leaves. Its count now matches, so bad is 4."},{"at":{"left":2,"right":3},"vars":{"bad":"2"},"note":"The letter 'b' enters. Its count now matches, so bad is 3. The letter 'i' leaves. Its count now matches, so bad is 2."},{"at":{"left":3,"right":4},"vars":{"bad":"0"},"note":"The letter 'a' enters. Its count now matches, so bad is 1. The letter 'd' leaves. Its count now matches, so bad is 0. The counter is 0, so the scan returns the start 3."}]}
```

The counter reaches 0 at the window `ba` and the scan returns its start, 3. At no step does the scan compare two arrays.

#### A Status Counter For A Cover

Take `s = "abcabc"` and the requirement of one each of `a`, `b` and `c`. Here the counter `bad` is the number of letters whose count is below the requirement. The trace records every window that covers the requirement after trimming, and it counts how many shortest windows exist. The variable `best` is the shortest length found and `ways` is the number of windows with that length.

```trace
{"cells":["a","b","c","a","b","c"],"pointers":["left","right"],"steps":[{"at":{"left":0,"right":0},"vars":{"bad":"2","best":"none","ways":"0"},"note":"The letter 'a' enters, so bad is 2."},{"at":{"left":0,"right":1},"vars":{"bad":"1","best":"none","ways":"0"},"note":"The letter 'b' enters, so bad is 1."},{"at":{"left":1,"right":2},"vars":{"bad":"1","best":"3","ways":"1"},"note":"The letter 'c' enters, so bad is 0. The window 'abc' covers the requirement and is the shortest so far, so best is 3 and ways is 1. The letter 'a' leaves, so bad is 1."},{"at":{"left":2,"right":3},"vars":{"bad":"1","best":"3","ways":"2"},"note":"The letter 'a' enters, so bad is 0. The window 'bca' covers the requirement with the shortest length, so ways is 2. The letter 'b' leaves, so bad is 1."},{"at":{"left":3,"right":4},"vars":{"bad":"1","best":"3","ways":"3"},"note":"The letter 'b' enters, so bad is 0. The window 'cab' covers the requirement with the shortest length, so ways is 3. The letter 'c' leaves, so bad is 1."},{"at":{"left":4,"right":5},"vars":{"bad":"1","best":"3","ways":"4"},"note":"The letter 'c' enters, so bad is 0. The window 'abc' covers the requirement with the shortest length, so ways is 4. The letter 'a' leaves, so bad is 1."}]}
```

Four windows of length 3 cover the requirement, and no window of length 2 does.

<!-- stage: code -->
### The Counter In Java

#### Exact Match With A Status Counter

```java
static int firstMatchStart(String s, String p) {
    int k = p.length();
    if (k > s.length()) return -1;
    int[] need = new int[26], cnt = new int[26];
    for (int i = 0; i < k; i++) need[p.charAt(i) - 'a']++;
    int bad = 0;
    for (int x = 0; x < 26; x++) if (need[x] != 0) bad++;
    for (int right = 0; right < s.length(); right++) {
        int in = s.charAt(right) - 'a';
        boolean wasOk = cnt[in] == need[in];
        cnt[in]++;
        boolean isOk = cnt[in] == need[in];
        if (wasOk && !isOk) bad++; else if (!wasOk && isOk) bad--;
        if (right >= k) {
            int out = s.charAt(right - k) - 'a';
            wasOk = cnt[out] == need[out];
            cnt[out]--;
            isOk = cnt[out] == need[out];
            if (wasOk && !isOk) bad++; else if (!wasOk && isOk) bad--;
        }
        if (right >= k - 1 && bad == 0) return right - k + 1;
    }
    return -1;
}
```

The initial value of `bad` counts the letters of the pattern, because every window count starts at 0. Each update compares the status of one letter before and after the count changes.

#### Cost Of The Counter

Each step makes two constant updates, so the time is O(n) with no factor for the alphabet. The working memory is two small arrays, one entry per letter. A map replaces the arrays for a larger alphabet, with the same logic.

<!-- stage: applicability -->
### When The Combination Applies

#### Spotting A Rule Over Counts

Look for a window problem where validity is a rule over counts. Typical rules are an exact match, a limit on repeats, a minimum for each required character, or a budget for replacements. The window may have a fixed length or a variable one, and the counts and the boundaries must change together at every step.

#### The Invariant To State

The counts describe exactly the characters from `left` to `right`, and the status counter equals the number of characters that break the rule. Say this before the loop. A reader can then check each of the two updates against the statement, and a missing leaving update shows up at once.

#### Counts Without Boundaries Are A False Friend

A method that adds each character to a count but never removes any describes the whole prefix and not the window. The counts look correct on short inputs, because the prefix and the window coincide at the start. They also look correct when the entering update is right and the leaving update is wrong by one position. Only a check against a recount from the boundaries exposes the drift.

#### Java Habits For This Pattern

Update the counts and the status counter in the same method, so one cannot change without the other. Compare the status of the letter before and after the change, and never recompute the whole counter in the loop. Use arrays when the contract fixes the alphabet and maps otherwise. Build the answer text once, from stored boundaries.

<!-- stage: exercises -->
### Exercises

#### [Build] Permutation In String (LeetCode 567)
<!-- id: sw-comb-permutation -->

**Prerequisites.** The status counter, and the fixed windows of the earlier lesson on counts.

**Problem.** Given strings `p` and `s`, return the smallest start index of a substring of `s` that is a permutation of `p`, or -1 if none exists. The method keeps a status counter of the letters whose window count differs from their count in `p`. It does constant work per step and never compares two arrays.

**Constraints.**
- **Lengths** satisfy `1 <= p.length, s.length <= 10^5`.
- **Characters** are lowercase English letters.
- **Return** type is `int`.
- **Mutation** does not occur; the strings are immutable.

**Example 1.** Input `p = "ab"`, `s = "eidbaooo"`. Output `3`.

**Example 2.** Input `p = "aab"`, `s = "abbaz"`. Output `-1`.

**Hint.** What is the value of the counter before any character enters?

**Changed decision.** A counter replaces the comparison of two arrays, and the method returns a position and not a boolean.

#### [Vary] Longest Substring Without Repeating Characters (LeetCode 3)
<!-- id: sw-comb-repeat-limit -->

**Prerequisites.** The exercise above.

**Problem.** Given a string `s` and an integer `limit >= 1`, return the length of the longest substring in which every character occurs at most `limit` times. With `limit = 1`, this is the problem of the longest substring without repeating characters. The status counter holds the number of characters whose count exceeds `limit`.

**Constraints.**
- **Length** satisfies `0 <= s.length <= 10^5`.
- **Characters** are ASCII characters, codes 0 to 127.
- **Limit** satisfies `1 <= limit <= s.length + 1`.
- **Return** type is `int`.
- **Mutation** does not occur; `s` is immutable.

**Example 1.** Input `s = "aaabbcaaa"`, `limit = 2`. Output `5`.

**Example 2.** Input `s = "pwwkew"`, `limit = 1`. Output `3`.

**Hint.** When does the entering letter raise the counter? When does a leaving letter lower it?

**Changed decision.** The rule is a limit instead of a ban on repeats, and the counter tracks the letters over the limit.

#### [Boundary] Longest Repeating Character Replacement (LeetCode 424)
<!-- id: sw-comb-leftmost-replacement -->

**Prerequisites.** The two exercises above.

**Problem.** Given a string `s` of uppercase letters and an integer `k`, return an `int[]` of two entries, `{start, length}`, for the leftmost longest substring that becomes one repeated letter after at most `k` replacements. The start must name a valid substring.

**Constraints.**
- **Length** satisfies `1 <= s.length <= 10^5`.
- **Characters** are uppercase English letters.
- **Budget** satisfies `0 <= k <= s.length`.
- **Ties** go to the smallest start.
- **Mutation** does not occur; `s` is immutable.

**Example 1.** Input `s = "AABABBA"`, `k = 1`. Output `{0, 4}`.

**Example 2.** Input `s = "ABCDE"`, `k = 0`. Output `{0, 1}`.

**Hint.** The one removal form keeps an invalid window. Does its `left` index name a valid substring?

**Changed decision.** The answer includes a position. The window must be valid when it is recorded, so the method uses a full shrink.

#### [Recognize] Minimum Window Substring (LeetCode 76)
<!-- id: sw-comb-count-minimum -->

**Prerequisites.** All three exercises above.

**Problem.** Given lowercase strings `s` and `t`, return an `int[]` of two entries: the length of the shortest substring of `s` that contains every character of `t` with its multiplicity, and the number of substrings of that length that do so. Return `{-1, 0}` when no substring qualifies.

**Constraints.**
- **Lengths** satisfy `1 <= s.length, t.length <= 10^5`.
- **Characters** are lowercase English letters.
- **Return** type is `int[]` with two entries.
- **Mutation** does not occur; the strings are immutable.

**Example 1.** Input `s = "abcabc"`, `t = "abc"`. Output `{3, 4}`.

**Example 2.** Input `s = "aa"`, `t = "aaa"`. Output `{-1, 0}`.

**Hint.** Which recorded windows have the shortest length, and can the same window be recorded twice?

**Changed decision.** The method counts the shortest windows as well as measuring them, so it must record every cover that the trimming loop reaches.
