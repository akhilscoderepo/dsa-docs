<!-- lesson-kind: combination -->
<!-- lesson-id: window-frequency-state -->
## Window Frequency State

<!-- stage: context -->
### One Skeleton Under Four Problems

Look back over this chapter. A fixed frequency window asked whether a block is a rearrangement of a probe. A longest-valid window asked for the longest stretch with no repeated letter. A replacement-budget window asked how long a stretch could be made uniform. A minimum-cover window asked for the shortest stretch containing every required letter. The stories differ, but each solution had the same parts: two edges, a table of counts, and some test that said whether the counts were acceptable.

Writing four separate solutions with four separate hand-made tests invites mistakes, because each test is a slightly different loop over the table and each is a chance for an off-by-one. This lesson pulls out the shared structure so that one idea, a single counter that answers the test, serves all four.

<!-- stage: contributions -->
### What Each Piece Contributes

The window boundaries contribute the rule of which elements are active. They say that an element enters when `right` reaches it, that it leaves when `left` passes it, and which policy decides how far `left` may move: a fixed distance, a repair loop that restores validity, or a shrink loop that continues while the window is still valid. They say nothing about what the elements mean.

The frequency state contributes the meaning. A table of counts says how many times each symbol occurs among the active elements, and a requirement table says how many times each symbol is wanted, allowed or budgeted. It says nothing about which elements are active. Neither piece answers the question alone. The combined invariant has to state both together: the table equals the counts of exactly the elements from `left` through `right`, and a single integer summarizes whether that table is acceptable.

<!-- stage: naive -->
### Rescan The Table At Every Step

The direct way to test a window is to loop over the whole table after each move and decide from scratch. Here is the permutation check written that way, over an alphabet of any 16-bit characters.

```java
static boolean containsPermutationRescan(String probe, String text) {
    int k = probe.length();
    if (k > text.length()) return false;
    int[] need = new int[65536], have = new int[65536];
    for (int i = 0; i < k; i++) need[probe.charAt(i)]++;
    for (int right = 0; right < text.length(); right++) {
        have[text.charAt(right)]++;
        if (right >= k) have[text.charAt(right - k)]--;
        if (right >= k - 1 && Arrays.equals(have, need)) return true;   // scans 65,536 slots
    }
    return false;
}
```

The answer is correct and the code is short.

<!-- stage: bottleneck -->
### A Big Table, A Big Test

Each step compares two tables of 65,536 integers, even though one step changed at most two slots. With a text of 100,000 characters that is about 6.5 billion slot reads, which is O(alphabet * n) time, to learn something that two slot updates already determine. Shrinking the table to 26 letters, as in the earlier lesson, hides the problem rather than removing it, because the test still scales with the alphabet instead of with the change.

There is a second cost, which is harder to see. Each of the four problems would carry its own loop over the table, with its own condition. A bug fixed in one copy is not fixed in the others, and the copies drift. The shared skeleton is not only faster, it is easier to get right.

<!-- stage: insight -->
### One Counter, Updated Where The Change Happened

When a symbol arrives or leaves, exactly one slot of the table changes. So the acceptability of the table can change only through that slot. If we keep an integer that counts how many slots are currently in the good state, then the update on a move is local: check whether that one slot was good before the change, apply the change, and check whether it is good afterward. Adjust the integer by the difference. The test for the whole window then reads one integer, in constant time, whatever the alphabet.

We call that integer the **status counter**, and the rule for how it is adjusted is the **local update**: subtract the slot's old contribution, change the slot, add the new contribution. What counts as good depends on the problem. For a permutation check a slot is good when its window count equals its required count, and the window passes when every required slot is good. For a no-repeat window a slot is bad when its count exceeds one, and the window passes when the number of bad slots is zero. For a cover, a slot is owed while its count is below its requirement, and the window passes when nothing is owed. For a replacement budget the counter is the stored dominant count.

<!-- names: status counter, local update -->

The four problems then differ only in three small choices: which policy moves `left`, how a slot is classified, and what the status counter must equal for the window to pass. The loop around them is identical.

The ordering inside the local update matters. The old contribution must be removed before the count changes, and the new one added after. Doing both after the change reads the wrong value and corrupts the counter silently. Every wrong answer from this technique that is not a boundary mistake traces back to the order of those three lines.

<!-- stage: variables -->
### The Combined State

The window is described by `left` and `right`. The table `have` holds the counts of exactly those elements, and the table `need` holds the requirements, which are fixed. The integer `status` summarizes `have` against `need` according to the problem's definition of good, and it is the only value the loop tests. The invariant ties them together: after every update, `status` equals what a full scan of the table would compute, `have` equals the counts of the elements from `left` through `right`, and the policy has moved `left` to the position it promises.

<!-- stage: trace -->
### One Run Through

Take the text `bcadabc` and the probe `abc`. The probe needs one of each of three letters, so the window passes when all three slots are good, and `status` counts the good slots. The first three letters enter one at a time. After `b` the status is 1, after `c` it is 2, and after `a` it is 3, so the window `bca` passes and start 0 is recorded.

Now the window slides, with each move changing two slots. Letter `d` enters and `b` leaves. The slot for `d` is not required, so it is ignored, and the slot for `b` goes from good to bad, so the status falls to 2 and start 1 is skipped. Next `a` enters and `c` leaves. The window `ada` holds two `a`s, so the `a` slot flips from good to bad because its count overshoots the requirement of one, and the `c` slot goes bad as well. The status drops to 0.

Then `b` enters and `a` leaves. The `a` slot, with a count of one, is good again, and the `b` slot becomes good, so the status climbs to 2. The last move brings `c` in and removes `d`, the `c` slot becomes good, and the status reaches 3. The window `abc` passes at start 4. The answer is starts 0 and 4, found with no table scan at all.

```trace
{"cells":["b","c","a","d","a","b","c"],"pointers":["left","right"],"steps":[{"at":{"left":0,"right":0},"vars":{"matched":1,"found":0},"note":"Take in index 0 (letter b). The window is not full yet."},{"at":{"left":0,"right":1},"vars":{"matched":2,"found":0},"note":"Take in index 1 (letter c). The window is not full yet."},{"at":{"left":0,"right":2},"vars":{"matched":3,"found":1},"note":"Take in index 2 (letter a). Every needed letter matches its count (3 of 3), so start 0 is recorded."},{"at":{"left":1,"right":3},"vars":{"matched":2,"found":1},"note":"Add d, remove b. Only 2 of 3 needed letters match, so start 1 is skipped."},{"at":{"left":2,"right":4},"vars":{"matched":0,"found":1},"note":"Add a, remove c. Only 0 of 3 needed letters match, so start 2 is skipped."},{"at":{"left":3,"right":5},"vars":{"matched":2,"found":1},"note":"Add b, remove a. Only 2 of 3 needed letters match, so start 3 is skipped."},{"at":{"left":4,"right":6},"vars":{"matched":3,"found":2},"note":"Add c, remove d. Every needed letter matches its count (3 of 3), so start 4 is recorded."}]}
```

<!-- stage: code -->
### The Java Blueprint

```java
static boolean containsPermutation(String probe, String text) {
    int k = probe.length();
    if (k > text.length()) return false;
    int[] need = new int[65536], have = new int[65536];
    int distinct = 0;
    for (int i = 0; i < k; i++) if (need[probe.charAt(i)]++ == 0) distinct++;
    int status = 0;                                   // number of required slots whose count equals the need
    for (int right = 0; right < text.length(); right++) {
        char in = text.charAt(right);
        if (need[in] > 0) {
            if (have[in] == need[in]) status--;       // old contribution out
            have[in]++;
            if (have[in] == need[in]) status++;       // new contribution in
        }
        if (right >= k) {
            char out = text.charAt(right - k);
            if (need[out] > 0) {
                if (have[out] == need[out]) status--;
                have[out]--;
                if (have[out] == need[out]) status++;
            }
        }
        if (right >= k - 1 && status == distinct) return true;
    }
    return false;
}
```

Letters that the probe does not need are skipped entirely. That is safe here because the window length equals the probe length: if every needed slot matches its count exactly, the counts already add up to `k`, so there is no room left for an unneeded letter.

The same shape carries the other three problems with a different classification. For the no-repeat window, `status` counts letters whose count exceeds one, it rises when a count moves from one to two, falls when it moves from two to one, and the window passes when it is zero. For the cover, `status` counts copies still owed and falls when an arriving letter was owed, which is the outstanding counter of the minimum-cover lesson. For the replacement budget, `status` is replaced by the stored dominant count, with the justification from that lesson.

The cost is O(n + m) time with no dependence on the alphabet in the loop, plus O(alphabet) to allocate the tables once. When the alphabet is large and the text short, a `HashMap` for the tables avoids the allocation, with the same updates.

<!-- stage: applicability -->
### When It Applies

Use a window with frequency state when the validity of a range depends on how many times symbols occur in it, and the boundaries obey one of the policies already taught. The invariant to say aloud is that the table equals the counts of the active elements and the status counter equals the result of a full classification of that table.

The first false friend is classifying with the wrong comparison. A permutation requires equality, so a count that overshoots is bad. A cover requires at least, so a count that overshoots is fine. Copying the permutation counter into a cover problem rejects windows that are correct, and copying the cover counter into a permutation problem accepts windows that are wrong, and neither fails loudly. The second false friend is doing the local update in the wrong order, which corrupts the counter in a way that only some inputs reveal.

A related limit is worth naming. The table answers questions about counts and presence. It cannot answer which symbol is the largest or the smallest inside the window, because a count table has no order. A question like the maximum value in every window needs a different structure, which a later chapter on deques teaches.

When you build any of these, check the symbol domain, decide which comparison is the right one, write the three lines of the local update in order, and test the status counter against a full scan on small random inputs.

<!-- stage: exercises -->
### Exercises

#### [Build] Permutation in String With A Matched Counter (LeetCode 567)
<!-- id: sw-permutation-matched -->

**Prerequisites.** The fixed frequency lesson; this lesson for the status counter.

**Problem.** Given two strings `s1` and `s2`, return whether `s2` contains a rearrangement of `s1` as a substring. The characters may be any 16-bit values, so do not compare two tables inside the loop. Maintain a counter of required characters whose window count equals their requirement.

**Constraints.** 1 <= s1.length, s2.length <= 10^5 and every character is a UTF-16 code unit. Target O(n + m) time.

**Example 1.** Input `s1 = "aab"`, `s2 = "zbaaz"`, output `true`, from the block `"baa"`.

**Example 2.** Input `s1 = "aab"`, `s2 = "abbab"`, output `false`. Every window of length three has the right letters but never two `a`s.

**Hint.** When one required character's count changes, which two checks around the change tell you whether the counter goes up, goes down, or stays?

**Changed decision.** First rung of the ladder: the comparison of two tables is replaced by a counter updated at the one slot that changed.

#### [Vary] Longest Unique Substring With A Status Counter (LeetCode 3)
<!-- id: sw-unique-status-counter -->

**Prerequisites.** The exercise above, and the longest-valid lesson.

**Problem.** Given a string `s`, return a two-element array holding the start index and the length of the leftmost longest substring that has no repeated character. For an empty string return `[0, 0]`. Keep a counter of characters whose count exceeds one, and allow the window to be tested in constant time.

**Constraints.** 0 <= s.length <= 5 * 10^4 and every character is a UTF-16 code unit. Target O(n) time.

**Example 1.** Input `s = "dvdfkd"`, output `[1, 4]`, from `"vdfk"`.

**Example 2.** Input `s = "abccdefgcd"`, output `[3, 5]`, from `"cdefg"`. A later stretch `"defgc"` ties but starts further right.

**Hint.** The length may vary now. Which transitions of a count should change the counter, and why does the repair loop have to be a `while` here?

**Changed decision.** The status counter counts violations instead of matches, and the answer reports boundaries, so the window must be valid when it is measured.

#### [Boundary] Longest Repeating Character Replacement, Mixed Case (LeetCode 424)
<!-- id: sw-replacement-mixed-case -->

**Prerequisites.** The two exercises above, and the replacement-budget lesson.

**Problem.** This is the replacement problem with a wider alphabet. Given a string `s` of uppercase and lowercase English letters, where `A` and `a` are different symbols, and an integer `k`, return the length of the longest substring that can be made to contain a single symbol with at most `k` replacements. Use a stored dominant count and state in a comment why it may overstate the current window.

**Constraints.** 1 <= s.length <= 10^5, `s` contains only English letters of either case, and 0 <= k <= s.length. Target O(n) time.

**Example 1.** Input `s = "aAaA"`, `k = 1`, output `3`.

**Example 2.** Input `s = "AAaa"`, `k = 0`, output `2`. The two cases are separate symbols, so no window of length three is uniform.

**Hint.** The table now has 52 slots. Where does a lowercase letter's slot sit, and what part of the stored-maximum argument depends on the size of the alphabet?

**Changed decision.** The alphabet doubles, which tests the slot mapping, while the stored-maximum argument has to be restated rather than copied.

#### [Recognize] Minimum Window Substring Over Any Characters (LeetCode 76)
<!-- id: sw-minimum-window-any-chars -->

**Prerequisites.** The three exercises above, and the minimum-cover lesson.

**Problem.** The strings `s` and `t` may contain any 16-bit characters. Return the leftmost shortest substring of `s` that contains every character of `t` with its full multiplicity, or the empty string when none exists. Keep a single counter of copies still owed.

**Constraints.** 1 <= s.length, t.length <= 10^5 and every character is a UTF-16 code unit. Target O(n + m) time and one call to `substring`.

**Example 1.** Input `s = "zzxyzxyyz"`, `t = "xyz"`, output `"zxy"`.

**Example 2.** Input `s = "aa"`, `t = "aaa"`, output `""`. Only two copies of `a` exist.

**Hint.** Which comparison does a cover need, equality or at-least, and in what order do the three lines of the local update run when the departing character was owed?

**Changed decision.** The classification becomes at-least instead of equal, and the counter tracks copies owed, which makes the window pass at zero.

#### [Extend] Longest Substring with At Least K Repeating Characters (LeetCode 395)
<!-- id: sw-at-least-k-repeating -->

**Prerequisites.** The four exercises above, and the at-most-K distinct lesson.

**Problem.** Return the length of the longest substring of `s` in which every letter that occurs does so at least `k` times.

**Constraints.** 1 <= s.length <= 10^4, `s` consists of lowercase English letters, and 1 <= k <= 10^5. Target O(26 * n) time.

**Example 1.** Input `s = "xxyyyzzzzw"`, `k = 3`, output `7`, from `"yyyzzzz"`.

**Example 2.** Input `s = "aabbbcccd"`, `k = 3`, output `6`, from `"bbbccc"`.

**Hint.** A window with an unknown number of distinct letters has no monotone rule. If you fix the number of distinct letters allowed at `t`, what two counters make the window testable, and how many values of `t` must you try?

**Changed decision.** Validity is not monotone on its own, so the window is run once per allowed number of distinct letters, with two status counters per run.
