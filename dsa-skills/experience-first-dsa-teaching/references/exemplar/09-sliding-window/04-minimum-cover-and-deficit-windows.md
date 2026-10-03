<!-- lesson-kind: standard -->
<!-- lesson-id: minimum-cover-and-deficit-windows -->
## Minimum-Cover And Deficit Windows

<!-- stage: context -->
### The Shortest Errand Walk

You are new in town and need three errands done: a bakery, a pharmacy and a post office. Along the main street the shops appear in a long row, many of them irrelevant. You want to walk as little as possible, so you look for the shortest stretch of the street that contains at least one of each required shop. Extra shops inside the stretch are fine. They just make the walk longer than it needs to be.

Two things distinguish this from the earlier lessons. The length is no longer fixed, since a good stretch might be five shops or fifty. And the condition is not that the stretch matches a pattern exactly, it is that the stretch covers everything on a list, with surplus allowed. The goal is the smallest such stretch, so a shorter valid answer always beats a longer one.

<!-- stage: naive -->
### Grow From Every Start

The plain method picks each starting shop and walks to the right until every required shop has appeared, then notes the length and moves to the next start.

```java
static int shortestCoverBruteForce(String s, String need) {
    int best = -1;
    for (int start = 0; start < s.length(); start++) {
        int[] missing = new int[128];
        int stillMissing = need.length();
        for (char c : need.toCharArray()) missing[c]++;
        for (int end = start; end < s.length(); end++) {
            char c = s.charAt(end);
            if (missing[c] > 0) stillMissing--;
            missing[c]--;
            if (stillMissing == 0) {
                if (best == -1 || end - start + 1 < best) best = end - start + 1;
                break;
            }
        }
    }
    return best;
}
```

It finds the right answer and handles repeated required items, because the counter tracks every copy that is still owed.

<!-- stage: bottleneck -->
### Forgetting The Last Start's Work

Suppose the cover for start 0 ends at index 40. For start 1 the method begins again at index 1, re-counts the same 39 shops, and reaches nearly the same end. Each start throws away a ledger that its neighbor could have reused almost whole, because the stretch from start 1 to index 40 differs from the stretch from start 0 only by the first shop.

On a long street with a rare shop, many starts walk almost the whole way before finding a cover, or never find one. The method costs O(n^2) time in the worst case. On a string of 100,000 characters in which the last required letter appears only at the end, every start scans to the end, which is about five billion steps, plus a fresh 128-slot table allocated per start.

<!-- stage: insight -->
### Walk Forward, Then Tighten

The first start that works gives a hint. Once we have a stretch that covers everything, we do not restart. We keep the stretch and tighten it from the left, as long as it still covers, because every shop we can drop is a shop we do not need to walk past. As soon as dropping the leftmost shop would break the cover, we stop tightening and push the right edge forward again until the cover is restored.

The bookkeeping is a **deficit ledger**: for each required symbol, how many copies we still owe. A symbol that has arrived reduces what we owe. A symbol that is not required, or that we already have enough of, is surplus and is recorded as owing a negative amount, which is only a way of saying we hold extras. One number, the **outstanding count**, adds up everything still owed and tells us at a glance whether the window covers: it is zero exactly when it does. A window that covers every requirement and is shrunk as far as it can be is a **minimum-cover window**.

<!-- names: deficit ledger, outstanding count, minimum-cover window -->

The rhythm differs from the longest-valid lesson in one decisive way. There we shrank only when the window was invalid and measured afterward. Here the goal is the shortest valid window, so we shrink while the window is valid and measure at the top of the shrink loop, before each removal, because the loop may remove the very element that makes the window valid. The same two edges are used, and the same argument bounds the work, but the order of measuring and shrinking is reversed.

Why is it safe? Suppose the window from `left` to `right` covers, and the leftmost symbol is surplus. Any shorter cover that ends at `right` must start at `left` or later, so dropping that symbol loses nothing, and we repeat. When the leftmost symbol is needed, no cover ending at `right` can start later than `left`, which means this is the shortest cover ending at `right`.

<!-- stage: variables -->
### The Ledger And The Edges

The array `owed` has one slot per possible symbol. A slot starts at the number of copies required and moves down on arrival and up on departure. A positive slot means copies still owed, and a negative slot means surplus. The integer `outstanding` is the sum of the positive slots, starting at the length of the requirement. The two edges `left` and `right` bound the window. The pair `bestStart` and `bestLen` remember the best cover found so far, and remain unset if none exists. Notice that we store boundaries, not a substring.

<!-- stage: trace -->
### One Run Through

Take the street `ADOBECODEBANC` and the requirement `ABC`. The first five letters add up slowly: `A` and `B` reduce what we owe, while `D`, `O` and `E` are irrelevant. At index 5 the letter `C` arrives and the outstanding count reaches zero. The window `ADOBEC` covers, with length 6, and that is recorded.

Now we tighten. The leftmost letter is `A`, which we still owe once we remove it, so removing it breaks the cover. The outstanding count goes back to 1 and tightening stops. The right edge moves on through `O`, `D`, `E` and `B`, which changes nothing, and reaches the `A` at index 10. The cover is back, but it is long: `DOBECODEBA` has length 10.

This time tightening goes a long way. `D`, `O` and `E` are irrelevant and drop out for free. The first `B` also drops out for free, because a second `B` arrived later and covers the requirement. The window shrinks to `CODEBA`, length 6, which ties the best. Removing the `C` breaks the cover, so we stop.

The edge goes on to take in `N` and `C`, giving `ODEBANC` with length 7. Tightening removes `O` and `D`, and records `EBANC` at length 5, a new best. Dropping `E` gives `BANC` with length 4, the best of all. Dropping `B` breaks the cover. The answer is `BANC`.

```trace
{"cells":["A","D","O","B","E","C","O","D","E","B","A","N","C"],"pointers":["left","right"],"steps":[{"at":{"left":0,"right":0},"vars":{"remaining":2,"bestLen":0},"note":"Take in index 0 (letter A); it fills a requirement."},{"at":{"left":0,"right":1},"vars":{"remaining":2,"bestLen":0},"note":"Take in index 1 (letter D); it is surplus or irrelevant."},{"at":{"left":0,"right":2},"vars":{"remaining":2,"bestLen":0},"note":"Take in index 2 (letter O); it is surplus or irrelevant."},{"at":{"left":0,"right":3},"vars":{"remaining":1,"bestLen":0},"note":"Take in index 3 (letter B); it fills a requirement."},{"at":{"left":0,"right":4},"vars":{"remaining":1,"bestLen":0},"note":"Take in index 4 (letter E); it is surplus or irrelevant."},{"at":{"left":0,"right":5},"vars":{"remaining":0,"bestLen":0},"note":"Take in index 5 (letter C); it fills a requirement."},{"at":{"left":0,"right":5},"vars":{"remaining":0,"bestLen":6},"note":"Every requirement is met by 'ADOBEC', length 6, a new best."},{"at":{"left":1,"right":5},"vars":{"remaining":1,"bestLen":6},"note":"Remove index 0 (letter A) from the left. That letter was still required, so the cover is broken."},{"at":{"left":1,"right":6},"vars":{"remaining":1,"bestLen":6},"note":"Take in index 6 (letter O); it is surplus or irrelevant."},{"at":{"left":1,"right":7},"vars":{"remaining":1,"bestLen":6},"note":"Take in index 7 (letter D); it is surplus or irrelevant."},{"at":{"left":1,"right":8},"vars":{"remaining":1,"bestLen":6},"note":"Take in index 8 (letter E); it is surplus or irrelevant."},{"at":{"left":1,"right":9},"vars":{"remaining":1,"bestLen":6},"note":"Take in index 9 (letter B); it is surplus or irrelevant."},{"at":{"left":1,"right":10},"vars":{"remaining":0,"bestLen":6},"note":"Take in index 10 (letter A); it fills a requirement."},{"at":{"left":1,"right":10},"vars":{"remaining":0,"bestLen":6},"note":"Every requirement is met by 'DOBECODEBA', length 10, no better than the best."},{"at":{"left":2,"right":10},"vars":{"remaining":0,"bestLen":6},"note":"Remove index 1 (letter D) from the left. That letter was surplus, so the window still covers."},{"at":{"left":2,"right":10},"vars":{"remaining":0,"bestLen":6},"note":"Every requirement is met by 'OBECODEBA', length 9, no better than the best."},{"at":{"left":3,"right":10},"vars":{"remaining":0,"bestLen":6},"note":"Remove index 2 (letter O) from the left. That letter was surplus, so the window still covers."},{"at":{"left":3,"right":10},"vars":{"remaining":0,"bestLen":6},"note":"Every requirement is met by 'BECODEBA', length 8, no better than the best."},{"at":{"left":4,"right":10},"vars":{"remaining":0,"bestLen":6},"note":"Remove index 3 (letter B) from the left. That letter was surplus, so the window still covers."},{"at":{"left":4,"right":10},"vars":{"remaining":0,"bestLen":6},"note":"Every requirement is met by 'ECODEBA', length 7, no better than the best."},{"at":{"left":5,"right":10},"vars":{"remaining":0,"bestLen":6},"note":"Remove index 4 (letter E) from the left. That letter was surplus, so the window still covers."},{"at":{"left":5,"right":10},"vars":{"remaining":0,"bestLen":6},"note":"Every requirement is met by 'CODEBA', length 6, no better than the best."},{"at":{"left":6,"right":10},"vars":{"remaining":1,"bestLen":6},"note":"Remove index 5 (letter C) from the left. That letter was still required, so the cover is broken."},{"at":{"left":6,"right":11},"vars":{"remaining":1,"bestLen":6},"note":"Take in index 11 (letter N); it is surplus or irrelevant."},{"at":{"left":6,"right":12},"vars":{"remaining":0,"bestLen":6},"note":"Take in index 12 (letter C); it fills a requirement."},{"at":{"left":6,"right":12},"vars":{"remaining":0,"bestLen":6},"note":"Every requirement is met by 'ODEBANC', length 7, no better than the best."},{"at":{"left":7,"right":12},"vars":{"remaining":0,"bestLen":6},"note":"Remove index 6 (letter O) from the left. That letter was surplus, so the window still covers."},{"at":{"left":7,"right":12},"vars":{"remaining":0,"bestLen":6},"note":"Every requirement is met by 'DEBANC', length 6, no better than the best."},{"at":{"left":8,"right":12},"vars":{"remaining":0,"bestLen":6},"note":"Remove index 7 (letter D) from the left. That letter was surplus, so the window still covers."},{"at":{"left":8,"right":12},"vars":{"remaining":0,"bestLen":5},"note":"Every requirement is met by 'EBANC', length 5, a new best."},{"at":{"left":9,"right":12},"vars":{"remaining":0,"bestLen":5},"note":"Remove index 8 (letter E) from the left. That letter was surplus, so the window still covers."},{"at":{"left":9,"right":12},"vars":{"remaining":0,"bestLen":4},"note":"Every requirement is met by 'BANC', length 4, a new best."},{"at":{"left":10,"right":12},"vars":{"remaining":1,"bestLen":4},"note":"Remove index 9 (letter B) from the left. That letter was still required, so the cover is broken."}]}
```

<!-- stage: code -->
### The Java Blueprint

```java
static String minWindow(String s, String t) {
    int[] owed = new int[128];
    for (int i = 0; i < t.length(); i++) owed[t.charAt(i)]++;
    int outstanding = t.length();
    int left = 0, bestStart = 0, bestLen = Integer.MAX_VALUE;
    for (int right = 0; right < s.length(); right++) {
        char in = s.charAt(right);
        if (owed[in] > 0) outstanding--;       // a copy we still owed has arrived
        owed[in]--;                            // negative means surplus
        while (outstanding == 0) {             // covered: measure first, then try to tighten
            if (right - left + 1 < bestLen) {
                bestLen = right - left + 1;
                bestStart = left;
            }
            char out = s.charAt(left);
            owed[out]++;
            if (owed[out] > 0) outstanding++;  // we dropped a copy that was needed
            left++;
        }
    }
    return bestLen == Integer.MAX_VALUE ? "" : s.substring(bestStart, bestStart + bestLen);
}
```

Every change to `owed` is paired. An arrival decreases a slot and a departure increases the same slot, so the ledger stays correct whatever the window holds. The test `owed[in] > 0` before the decrement asks whether the arriving letter was still owed, and the matching test `owed[out] > 0` after the increment asks whether the departing letter leaves us owing something again. Writing those two tests the other way round is the usual source of off-by-one answers here.

The window is built only by integer boundaries. The single call to `substring` happens once at the end, so the loop allocates nothing. Both edges only move forward, so together they travel at most 2n positions and the time is O(n + m), where `m` is the length of the requirement, and the extra space is O(1) for a fixed character table. If the requirement is longer than the text, or asks for a letter the text never supplies, the outstanding count never reaches zero and the method returns the empty string without special handling.

<!-- stage: applicability -->
### When It Applies

Reach for a minimum-cover window when the task asks for the shortest contiguous range that covers a list of requirements, with surplus allowed. The invariant to say aloud is this: the outstanding count is zero exactly when the window from `left` to `right` contains every required symbol at least as many times as required, and after the shrink loop no earlier `left` yields a cover for this `right`.

Three false friends are worth separating. A fixed frequency window demands equality with a signature, and a cover allows extras, so a window with surplus letters is rejected by one and accepted by the other. A longest-valid window shrinks only on violation, while this one shrinks on success. And a problem that sounds similar but asks for the shortest range with a sum of at least a target is a cover whose requirement is a number, which is the extension exercise below.

The technique relies on monotonicity in the other direction: adding more symbols to a covering window keeps it covering. That is true for counts that are required at least, and it stops being true as soon as extras are forbidden. Also notice that with the sum version, negative numbers break the property, because adding an element could reduce the total.

Check these before coding. Decide the symbol domain and the table size. Decide what to return when no cover exists and apply the same rule in the code and in the tests. Do not build substrings inside the loop, and remember that the requirement may contain repeats.

<!-- stage: exercises -->
### Exercises

#### [Build] Shortest Segment Containing A And B (Author exercise)
<!-- id: sw-shortest-a-and-b -->

**Prerequisites.** The longest-valid lesson for the two-edge loop; this lesson for the shrink-while-valid rhythm.

**Problem.** Given a string made of lowercase letters, return the length of the shortest contiguous segment that contains at least one `a` and at least one `b`. Return -1 if no such segment exists.

**Constraints.** 0 <= s.length <= 10^5. Target O(n) time and O(1) extra space.

**Example 1.** Input `s = "ccabcb"`, output `2`, from the segment `"ab"`.

**Example 2.** Input `s = "aaaa"`, output `-1`, because no `b` exists anywhere.

**Hint.** Once a segment holds both letters, which end can you trim without losing the guarantee, and when do you record its length?

**Changed decision.** First rung of the ladder: the window shrinks while valid, and its length is recorded inside the shrink loop.

#### [Vary] Required Multiplicities (Author exercise)
<!-- id: sw-required-multiplicities -->

**Prerequisites.** The exercise above.

**Problem.** Given a string made of lowercase letters, return the length of the shortest contiguous segment that contains at least two `a` characters and at least one `b`. Return -1 if no such segment exists.

**Constraints.** 0 <= s.length <= 10^5. Target O(n) time and O(1) extra space.

**Example 1.** Input `s = "abcaab"`, output `3`, from `"aab"`. A check that only asks whether each letter appears would stop at `"ab"`, which has length 2 and is wrong.

**Example 2.** Input `s = "bcc"`, output `-1`.

**Hint.** What number tells you how many copies of each letter are still owed, and when does one arrival stop reducing the debt?

**Changed decision.** One letter must appear twice, so the ledger counts copies and distinct membership is no longer enough.

#### [Boundary] No Cover Exists (Author exercise)
<!-- id: sw-no-cover-exists -->

**Prerequisites.** The two exercises above.

**Problem.** Given strings `s` and `t`, return a two-element array `[start, length]` describing the shortest segment of `s` that contains every character of `t` with its full multiplicity. If there is none, return `[-1, 0]`. Do not create any substring.

**Constraints.** 0 <= s.length, t.length <= 10^5, and both strings contain only ASCII characters. If `t` is empty, return `[0, 0]`. Target O(n + m) time.

**Example 1.** Input `s = "xyz"`, `t = "xz"`, output `[0, 3]`.

**Example 2.** Input `s = "a"`, `t = "aa"`, output `[-1, 0]`. The letter exists, but only once, so the requirement can never be met.

**Hint.** What does the outstanding count look like at the end of the scan when a requirement can never be met, and what should the variables hold in that case?

**Changed decision.** The result may not exist, so a sentinel is returned, and the answer is reported as boundaries rather than as text.

#### [Recognize] Minimum Window Substring (LeetCode 76)
<!-- id: sw-minimum-window-substring -->

**Prerequisites.** The three exercises above.

**Problem.** Find the shortest piece of `s` that contains every character of `t`, counting repeats, so a `t` with two `a`s needs a piece with two `a`s. Return that piece, or the empty string when no piece qualifies.

**Constraints.** m == s.length, n == t.length, 1 <= m, n <= 10^5, and `s` and `t` consist of uppercase and lowercase English letters. Target O(m + n) time. The answer is unique whenever it exists.

**Example 1.** Input `s = "bbaacb"`, `t = "abc"`, output `"acb"`.

**Example 2.** Input `s = "bba"`, `t = "baa"`, output `""`, because `s` holds only one `a`.

**Hint.** The ledger and the shrink loop are the same as before. What must you remember at the moment a cover is found, so that the substring can be built once after the scan?

**Changed decision.** The requirement is read from a second string and the answer is text, so the boundaries are stored and the substring is created once.

#### [Extend] Minimum Size Subarray Sum (LeetCode 209)
<!-- id: sw-minimum-size-subarray-sum -->

**Prerequisites.** The four exercises above.

**Problem.** Given positive integers `nums` and a positive integer `target`, return the length of the shortest contiguous block whose total is at least `target`, or 0 when no block reaches it.

**Constraints.** 1 <= target <= 10^9, 1 <= nums.length <= 10^5, and 1 <= nums[i] <= 10^4. Target O(n) time and O(1) extra space.

**Example 1.** Input `target = 9`, `nums = [3, 1, 4, 1, 5, 2]`, output `3`, from `[4, 1, 5]`.

**Example 2.** Input `target = 20`, `nums = [3, 1, 4]`, output `0`, since the whole array totals only 8.

**Hint.** What plays the part of the outstanding count when the requirement is a number, and why does positivity make shrinking safe?

**Changed decision.** The requirement is a numeric threshold instead of a list of symbols, and the cover is monotone only because every value is positive.
