<!-- lesson-kind: standard -->
<!-- lesson-id: replacement-budget-windows -->
## Replacement-Budget Windows

<!-- stage: context -->
### The Repainted Row

A sign painter has a long row of lettered tiles, each painted `A` or `B` or some other capital. A customer wants the longest possible stretch of identical tiles, and the painter has paint for at most `k` repaints. Which stretch should she choose, and how long can it be?

For any stretch, the cheapest plan is clear. She keeps the letter that already appears most often and repaints everything else to match. A stretch of seven tiles with four `A`s therefore costs three repaints. Her question becomes which stretch is the longest one whose repaint cost stays within the budget. Fixing a string so that it becomes uniform, and flipping a limited number of bits to make a long run of ones, are the same question.

<!-- stage: naive -->
### Price Every Stretch

Take every start and every end, tally the letters of that stretch, find the most common letter, and accept the stretch if its length minus that count is at most `k`.

```java
static int longestRepaintBruteForce(String tiles, int k) {
    int best = 0;
    for (int start = 0; start < tiles.length(); start++) {
        int[] tally = new int[26];
        int most = 0;
        for (int end = start; end < tiles.length(); end++) {
            most = Math.max(most, ++tally[tiles.charAt(end) - 'A']);
            if (end - start + 1 - most <= k) best = Math.max(best, end - start + 1);
        }
    }
    return best;
}
```

The inner loop keeps a running maximum, so each stretch is priced in constant time.

<!-- stage: bottleneck -->
### Pricing From Scratch Each Start

The pricing is cheap but the enumeration is not. Each start restarts the tally and the maximum, and there are about n^2 / 2 stretches to price. A row of 100,000 tiles gives five billion price checks, plus one new 26-slot array per start.

The cost is O(n^2) time. Neighboring stretches differ by one tile at the left or the right, and their prices differ by very little, yet each start prices its stretches without any memory of the previous start. The next section keeps a single stretch alive instead.

<!-- stage: insight -->
### Cost Is Length Minus The Leader

Define the **replacement cost** of a stretch as its length minus the number of times its most common letter appears. This is exactly the number of tiles the painter must change. A stretch is usable when its replacement cost is at most `k`, and it plays the role that "at most one zero" played in the first lesson of this kind.

Usability is monotone under shrinking. If a stretch can be made uniform with at most `k` repaints, any smaller stretch inside it can too, since removing a tile either removes a tile that needed repainting or removes one of the leader's copies, and in the second case the length drops by one as well. So we can keep one stretch, grow it on the right, and shrink it from the left whenever the cost exceeds the budget.

The expensive part appears to be the leader. The count of the most common letter changes as tiles enter and leave, and finding it needs a look at all 26 counts. We call that value the **dominant count**. The key observation is that we can avoid recomputing it on every departure. Keep a stored value `maxFreq` that only ever goes up, updated when a tile arrives and left alone when a tile leaves. It may now overstate the true dominant count of the stretch, and the next sections show why that cannot make the reported length wrong.

<!-- names: replacement cost, dominant count -->

Here is the reasoning in plain terms. The answer can only grow when a longer stretch becomes usable, and a stretch of length `L` is usable only if some letter appears at least `L - k` times in it. A stored value that has never been exceeded records the best dominant count seen so far, so a stretch longer than `maxFreq + k` would need a dominant count larger than any we have ever recorded. The shrink loop therefore holds the stretch at most `maxFreq + k` long, and a length of exactly `maxFreq + k` is reached only after a real stretch achieved that dominant count. The reported length always corresponds to some genuinely usable stretch, even when the current stretch is not itself usable.

<!-- stage: variables -->
### Five Variables

The array `tally` counts the letters in the current stretch. The indices `left` and `right` bound it. The integer `maxFreq` is the stored dominant count: the largest tally value observed at any arrival so far, and it never decreases. The value `best` is the longest length reported. The replacement cost used by the shrink test is `right - left + 1 - maxFreq`, computed from these and never stored. An honest variant would replace `maxFreq` by the true maximum of the 26 slots at every check, which costs 26 steps per iteration and gives identical answers.

<!-- stage: trace -->
### One Run Through

Take the row `AABABBA` with a budget of one repaint. The first two tiles are both `A`, so the stored maximum is 2 and the cost is zero. Tile `B` arrives, the cost is one, which is within budget, and the stretch `AAB` is usable. Another `A` makes `AABA` with three `A`s, cost one, and `best` reaches 4.

Index 4 brings a `B`. The stretch `AABAB` has cost two, over the budget, so the left edge removes the first `A`. The stored maximum stays at 3, because it never drops. The stretch is now `ABAB`, which holds two `A`s and two `B`s. Its true cost is two, yet the stored values say 4 minus 3, which is one, so the loop is satisfied. This stretch is not truly usable. The measurement still reports a length of 4, which is correct only because another stretch of length 4, namely `AABA`, was usable earlier.

At index 5 the stretch `ABABB` has cost two, so one more removal gives `BABB`, and now the true dominant count really is 3. Index 6 gives `BABBA`, cost two, and the removal of a `B` leaves `ABBA`, whose true dominant count is 2 against a stored 3. The answer stays at 4. The stored maximum was never exceeded after index 3, so no longer stretch was ever claimed.

```trace
{"cells":["A","A","B","A","B","B","A"],"pointers":["left","right"],"steps":[{"at":{"left":0,"right":0},"vars":{"maxFreq":1,"cost":0,"best":0},"note":"Take in index 0 (letter A). The stored maxFreq is 1, so the cost is 0."},{"at":{"left":0,"right":0},"vars":{"maxFreq":1,"cost":0,"best":1},"note":"Measure: the window holds 1 letters, so best is 1."},{"at":{"left":0,"right":1},"vars":{"maxFreq":2,"cost":0,"best":1},"note":"Take in index 1 (letter A). The stored maxFreq is 2, so the cost is 0."},{"at":{"left":0,"right":1},"vars":{"maxFreq":2,"cost":0,"best":2},"note":"Measure: the window holds 2 letters, so best is 2."},{"at":{"left":0,"right":2},"vars":{"maxFreq":2,"cost":1,"best":2},"note":"Take in index 2 (letter B). The stored maxFreq is 2, so the cost is 1."},{"at":{"left":0,"right":2},"vars":{"maxFreq":2,"cost":1,"best":3},"note":"Measure: the window holds 3 letters, so best is 3."},{"at":{"left":0,"right":3},"vars":{"maxFreq":3,"cost":1,"best":3},"note":"Take in index 3 (letter A). The stored maxFreq is 3, so the cost is 1."},{"at":{"left":0,"right":3},"vars":{"maxFreq":3,"cost":1,"best":4},"note":"Measure: the window holds 4 letters, so best is 4."},{"at":{"left":0,"right":4},"vars":{"maxFreq":3,"cost":2,"best":4},"note":"Take in index 4 (letter B). The stored maxFreq is 3, so the cost is 2. That is over the budget."},{"at":{"left":1,"right":4},"vars":{"maxFreq":3,"cost":1,"best":4},"note":"Remove index 0 (letter A) from the left. The window now has 2 of its most common letter; the stored maxFreq stays 3."},{"at":{"left":1,"right":4},"vars":{"maxFreq":3,"cost":1,"best":4},"note":"Measure: the window holds 4 letters, so best is 4. The true dominant count is only 2, below the stored 3."},{"at":{"left":1,"right":5},"vars":{"maxFreq":3,"cost":2,"best":4},"note":"Take in index 5 (letter B). The stored maxFreq is 3, so the cost is 2. That is over the budget."},{"at":{"left":2,"right":5},"vars":{"maxFreq":3,"cost":1,"best":4},"note":"Remove index 1 (letter A) from the left. The window now has 3 of its most common letter; the stored maxFreq stays 3."},{"at":{"left":2,"right":5},"vars":{"maxFreq":3,"cost":1,"best":4},"note":"Measure: the window holds 4 letters, so best is 4."},{"at":{"left":2,"right":6},"vars":{"maxFreq":3,"cost":2,"best":4},"note":"Take in index 6 (letter A). The stored maxFreq is 3, so the cost is 2. That is over the budget."},{"at":{"left":3,"right":6},"vars":{"maxFreq":3,"cost":1,"best":4},"note":"Remove index 2 (letter B) from the left. The window now has 2 of its most common letter; the stored maxFreq stays 3."},{"at":{"left":3,"right":6},"vars":{"maxFreq":3,"cost":1,"best":4},"note":"Measure: the window holds 4 letters, so best is 4. The true dominant count is only 2, below the stored 3."}]}
```

<!-- stage: code -->
### The Java Blueprint

```java
static int longestRepaint(String tiles, int k) {
    int[] tally = new int[26];
    int left = 0, maxFreq = 0, best = 0;
    for (int right = 0; right < tiles.length(); right++) {
        int arrived = ++tally[tiles.charAt(right) - 'A'];
        maxFreq = Math.max(maxFreq, arrived);            // raised on arrival, never lowered on departure
        while (right - left + 1 - maxFreq > k) {         // cost over budget
            tally[tiles.charAt(left) - 'A']--;
            left++;
        }
        best = Math.max(best, right - left + 1);
    }
    return best;
}
```

Notice what is missing: there is no line that lowers `maxFreq` when a tile leaves. That omission is deliberate, and it is the part to check in review. A loop that tried to recompute the true maximum after each departure would work, only with 26 reads per step, and the stored version is justified by the argument above.

The loop does not shrink the stretch to a truly usable one. It shrinks it until the stored values accept it. If you need the actual best stretch, with its boundaries and not just its length, this code cannot supply them, because the final stretch may not be usable. For the length alone, the answer is correct.

The left edge trails the right edge without ever turning back, which gives O(n) time, and the extra space is the 26-slot table. The tallies only cover capital letters. A different domain needs a different table size, and the contract should say so.

<!-- stage: applicability -->
### When It Applies

Use a replacement-budget window when the task allows up to `k` edits to make a range uniform, and the objective is the longest such range. The invariant to state aloud is that the cost of the stretch equals its length minus its dominant count, the stretch is usable when the cost is at most `k`, and the stored maximum never falls below the dominant count of the current stretch.

The first false friend is the habit of recomputing the maximum on every move. It is correct and wasteful, and it hides the fact that the length formulation does not need it. The second false friend is the frequency-signature window, which demands exact counts. A replacement budget accepts any stretch where one letter is frequent enough, and the letter may change from one stretch to the next.

The stored maximum must not be used to report the actual stretch. If a problem asks for the replaced string, the start of the best stretch, or the number of edits actually used, compute the true dominant count for the winning stretch after the fact. The shortcut is justified for the length only.

Two binary versions are worth recognizing. Flipping at most `k` zeros to make a run of ones is the first lesson's exercise, and making a run of either symbol uniform is the same problem with an alphabet of two. When the alphabet has two symbols, the dominant count is simply the larger of two counters.

<!-- stage: exercises -->
### Exercises

#### [Build] Replacement Cost Of One Window (Author exercise)
<!-- id: sw-replacement-cost -->

**Prerequisites.** The fixed frequency lesson for tallies; this lesson for the cost formula.

**Problem.** Given a string of capital letters and two indices `left` and `right`, inclusive, return the minimum number of letters that must be changed so that every letter in that range is the same.

**Constraints.** 1 <= s.length <= 10^5, `s` contains only `A` to `Z`, and 0 <= left <= right < s.length. Target O(right - left) time.

**Example 1.** Input `s = "AABAB"`, `left = 0`, `right = 4`, output `2`, since the letter `A` appears three times in five tiles.

**Example 2.** Input `s = "ZZZ"`, `left = 0`, `right = 2`, output `0`.

**Hint.** If you keep the most common letter and change the rest, how many letters change, and which two numbers does that depend on?

**Changed decision.** First rung of the ladder: there is no sliding yet, only the cost formula of one fixed range.

#### [Vary] Longest Binary Uniform Window (Author exercise)
<!-- id: sw-binary-uniform -->

**Prerequisites.** The exercise above, and the longest-valid lesson.

**Problem.** Given a binary array `bits` and an integer `k`, you may flip at most `k` values. Return the length of the longest contiguous segment that can be made all zeros or all ones.

**Constraints.** 1 <= bits.length <= 10^5, each value is 0 or 1, and 0 <= k <= bits.length. Target O(n) time and O(1) extra space.

**Example 1.** Input `bits = [1, 0, 1, 1, 0, 0, 1]`, `k = 1`, output `4`, from `[1, 0, 1, 1]` with one flip.

**Example 2.** Input `bits = [0, 1, 0, 1]`, `k = 0`, output `1`. No flip is allowed, so each segment must already be uniform.

**Hint.** With only two symbols, what is the dominant count of a segment, and do you need the stored-maximum idea at all?

**Changed decision.** The alphabet shrinks to two symbols, so the dominant count becomes the larger of two counters and can be computed exactly at every step.

#### [Boundary] Stale Maximum Trace (Author exercise)
<!-- id: sw-stale-maximum -->

**Prerequisites.** The two exercises above.

**Problem.** Run the replacement-budget algorithm with a stored maximum that never decreases. Return a two-element array: the reported best length, and the number of positions `right` at which, after the shrink loop, the stored maximum was strictly larger than the true maximum letter count inside the current stretch.

**Constraints.** 1 <= s.length <= 10^5, `s` contains only `A` to `Z`, and 0 <= k <= s.length. Target O(26 * n) time.

**Example 1.** Input `s = "AABABBA"`, `k = 1`, output `[4, 2]`. The stored maximum overstates the stretch after indices 4 and 6.

**Example 2.** Input `s = "AAAA"`, `k = 0`, output `[4, 0]`. The stretch never loses a copy of its leader, so the stored maximum never drifts.

**Hint.** The stored maximum only changes on arrival. At which moment can the true count of the leading letter fall below it, and how do you read the true count without disturbing the algorithm?

**Changed decision.** The algorithm is observed rather than used, so the staleness the lesson argues is harmless becomes a number you can see.

#### [Recognize] Longest Repeating Character Replacement (LeetCode 424)
<!-- id: sw-character-replacement -->

**Prerequisites.** The three exercises above.

**Problem.** You may overwrite at most `k` characters of the string `s` with any uppercase letter. Return the length of the longest run of one repeated letter that you can end up with.

**Constraints.** 1 <= s.length <= 10^5, `s` consists of only uppercase English letters, and 0 <= k <= s.length. Target O(n) time.

**Example 1.** Input `s = "BBABCBB"`, `k = 1`, output `4`, for instance from `"BBAB"` after changing the `A`.

**Example 2.** Input `s = "QQRQQ"`, `k = 0`, output `2`. With no edits allowed, the `R` splits the run.

**Hint.** The alphabet has 26 letters and the budget is a limit, so which value must the stretch compare against, and what happens to that value when a tile leaves?

**Changed decision.** The leader is chosen among 26 letters, so the stored dominant count carries the argument and the loop never rescans the table.
