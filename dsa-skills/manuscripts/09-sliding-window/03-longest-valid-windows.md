<!-- lesson-kind: standard -->
<!-- lesson-id: longest-valid-windows -->
## Longest-Valid Windows

<!-- stage: context -->
### A Street Of Shuttered Shops

A food street runs for a kilometre, and every stall is either open or closed on a given evening. A visitor wants the longest unbroken stroll along which she can eat at every stall, but she is a forgiving person: she will put up with one closed shutter along the way, and no more than that. She holds a sheet that lists the stalls in order, with a one for open and a zero for closed, and she wants to know how many stalls long her best stroll can be.

Pointing at the sheet, she can already see the difficulty. A long open stretch might be cut by a zero, but if she skips that zero she may join it to another long stretch beyond, and a second zero further on ruins the plan unless she lets go of the beginning. She keeps starting new strolls from different stalls, and each time she re-reads many stalls she has already looked at.

<!-- stage: naive -->
### Start Anywhere And Walk Until Stuck

The direct plan is to try every starting stall, walk forward counting closed ones, and stop when a second closed one appears. The longest walk over all starts is the answer.

```java
static int longestStrollFromEveryStart(int[] stalls) {
    int best = 0;
    for (int start = 0; start < stalls.length; start++) {
        int closed = 0;
        int end = start;
        while (end < stalls.length) {
            if (stalls[end] == 0) closed++;
            if (closed > 1) break;
            end++;
        }
        best = Math.max(best, end - start);
    }
    return best;
}
```

It is correct for every sheet, including an empty one, and it never counts a stall twice within one walk. It only counts the same stall again in a different walk.

<!-- stage: bottleneck -->
### Every Start Re-Reads The Same Stalls

Two neighbouring starts, say stall 10 and stall 11, walk almost exactly the same road. If the walk from stall 10 ran to stall 400, the walk from stall 11 reads stalls 11 to 400 again, and this repeats for every start. On a sheet that is all ones, every start runs to the end, so the method reads about n times n over two stalls in total, which is O(n^2). The sheet is long, but the information in it is tiny: what matters is only where the walk stopped, and the stopping point of one walk tells a lot about the next.

Here is the waste stated precisely. The walk from stall 10 stopped at stall 400 because a second zero sat there. The walk from stall 11 cannot stop earlier than stall 400, since it has fewer or equal zeros than the earlier one in the same range. It can only stop at the same place or later. The right end never has to go backwards, so the algorithm should keep it and move only the beginning, which brings the work down to O(n).

<!-- stage: insight -->
### Keep The Window Healthy Then Measure

Let two indices, `left` and `right`, mark a stretch of the sheet. The stretch is a **valid window** when it meets the rule of the problem, here that it contains at most one zero. The algorithm adds one stall at the right edge, which may break the rule. When it does, a **violation** has just been created, and the only repair that makes sense is to take stalls off the left edge until the rule holds again. That repair is the **shrink loop**, and it is a `while`, not an `if`, because one new stall can force the removal of many old ones.

<!-- names: valid window, violation, shrink loop -->

After the shrink loop finishes, the window is a valid window again, and its length is a candidate for the answer. The invariant is stronger than that. Every start that was thrown away is known to be useless for the current `right` and for every later one, because a start that fails now would still fail once the window grows to the right, since growing never removes a zero. So no start is skipped that could have produced a longer window. The best length seen across all values of `right` is the answer, and each index enters once and leaves once, which is why the scan is linear.

The rule only has to be repairable by removing from the left. Counting zeroes, counting repeated letters, and keeping a sum below a limit all qualify, because removing an element can only help. That is what separates this lesson from problems where the window must be equal to something exact.

<!-- stage: variables -->
### Edges, Ledger And Best Length

`left` and `right` are the inclusive edges of the window, and `right` moves every round. A ledger tells whether the rule holds: for the street it is the number of zeros inside, for repeated letters it is a table of counts, and for a limit it is a running sum, held in a `long` when the elements may be large. `best` starts at zero, which is also the right answer for an empty sheet, and is updated after the shrink loop so it only ever sees healthy windows. The length of the window is `right - left + 1`, and it can drop to zero when one element alone breaks the rule.

<!-- stage: trace -->
### One Zero Allowed On The Street

The first trace follows the sheet 1, 1, 0, 1, 1, 1, 0, 1 with at most one zero allowed. The window grows over the first six stalls, then at position 6 a second zero arrives. The step to study is the one at position 6: the window had the length 6 and held one zero, the new zero is a violation, and the shrink loop must move `left` past the first zero before the window is healthy again.

```trace
{"cells":[1,1,0,1,1,1,0,1],"pointers":["left","right"],"steps":[{"at":{"left":0,"right":0},"vars":{"zeros":0,"best":1},"note":"Position 0 is open. The window grows to length 1."},{"at":{"left":0,"right":1},"vars":{"zeros":0,"best":2},"note":"Position 1 is open. The window grows to length 2."},{"at":{"left":0,"right":2},"vars":{"zeros":1,"best":3},"note":"Position 2 is the first zero in the window. It is allowed, so the window grows to length 3."},{"at":{"left":0,"right":3},"vars":{"zeros":1,"best":4},"note":"Position 3 is open. The window grows to length 4."},{"at":{"left":0,"right":4},"vars":{"zeros":1,"best":5},"note":"Position 4 is open. The window grows to length 5."},{"at":{"left":0,"right":5},"vars":{"zeros":1,"best":6},"note":"Position 5 is open. The window grows to length 6."},{"at":{"left":3,"right":6},"vars":{"zeros":1,"best":6},"note":"Position 6 is a second zero, a violation, so 3 stalls leave from the left and left becomes 3. The window is healthy at length 4."},{"at":{"left":3,"right":7},"vars":{"zeros":1,"best":6},"note":"Position 7 is open. The window grows to length 5."}]}
```

The second trace uses letters, where the rule is that no letter may repeat inside the window. The sheet is k, q, n, n, k, r, s, q. The step to study is the arrival of the second n at position 3: the window k, q, n, n has a repeat, and the shrink loop removes three letters in a row, because the old n sits at the far end of the window. After that the window is just the single new n.

```trace
{"cells":["k","q","n","n","k","r","s","q"],"pointers":["left","right"],"steps":[{"at":{"left":0,"right":0},"vars":{"removed":0,"best":1},"note":"Letter k at position 0 is new to the window, so it grows to length 1."},{"at":{"left":0,"right":1},"vars":{"removed":0,"best":2},"note":"Letter q at position 1 is new to the window, so it grows to length 2."},{"at":{"left":0,"right":2},"vars":{"removed":0,"best":3},"note":"Letter n at position 2 is new to the window, so it grows to length 3."},{"at":{"left":3,"right":3},"vars":{"removed":3,"best":3},"note":"Letter n at position 3 repeats, so 3 letters leave from the left and left becomes 3. The window has length 1."},{"at":{"left":3,"right":4},"vars":{"removed":0,"best":3},"note":"Letter k at position 4 is new to the window, so it grows to length 2."},{"at":{"left":3,"right":5},"vars":{"removed":0,"best":3},"note":"Letter r at position 5 is new to the window, so it grows to length 3."},{"at":{"left":3,"right":6},"vars":{"removed":0,"best":4},"note":"Letter s at position 6 is new to the window, so it grows to length 4."},{"at":{"left":3,"right":7},"vars":{"removed":0,"best":5},"note":"Letter q at position 7 is new to the window, so it grows to length 5."}]}
```

<!-- stage: code -->
### Zero Budget And Repeated Letters

```java
static int longestWithBudget(int[] sheet, int budget) {
    int left = 0, zeros = 0, best = 0;
    for (int right = 0; right < sheet.length; right++) {
        if (sheet[right] == 0) zeros++;
        while (zeros > budget) {
            if (sheet[left] == 0) zeros--;
            left++;
        }
        best = Math.max(best, right - left + 1);
    }
    return best;
}

static int longestWithoutRepeat(String text) {
    int[] seen = new int[256];
    int left = 0, best = 0;
    for (int right = 0; right < text.length(); right++) {
        seen[text.charAt(right)]++;
        while (seen[text.charAt(right)] > 1) {
            seen[text.charAt(left)]--;
            left++;
        }
        best = Math.max(best, right - left + 1);
    }
    return best;
}

static long longestUnderLimit(int[] weights, long limit) {
    long sum = 0;
    int left = 0, best = 0;
    for (int right = 0; right < weights.length; right++) {
        sum += weights[right];
        while (left <= right && sum > limit) sum -= weights[left++];
        best = Math.max(best, right - left + 1);
    }
    return best;
}
```

Each index is added once and removed at most once, so the work is O(n) across the whole scan, with O(1) extra space apart from the 256-slot table. The letter version assumes characters below 256 and keeps the count of the new letter as the only one that can be wrong. In the limit version the guard `left <= right` is what allows an element that is too heavy on its own to empty the window.

<!-- stage: applicability -->
### Spotting A Repairable Rule

Reach for this pattern when the question asks for the longest contiguous stretch obeying a rule that gets easier to satisfy as elements leave from the front. The invariant to state aloud before coding is that the window is healthy right after the shrink loop and that every discarded start is hopeless for all later right ends. Then decide the ledger, write the add line, the while line with its removal, and finally the update of `best`, always in that order.

A false friend is the shortest-cover problem of the next lesson, which also has a window, but there the shrinking happens while the window is good and the record is taken before the rule breaks. Copying the update of `best` to the wrong side of the loop gives an answer that is off by one in a very consistent way. Another false friend is any rule that can also be broken by removing elements, such as a window that must contain a certain value; shrinking does not repair that.

In Java, count with arrays when the alphabet is small and known, and watch the type of a sum: two `int` elements near the limit overflow before the comparison runs, so declare the sum as a `long`. Do not change the input, since the window needs nothing but reads. A `while` loop with an unguarded `left` can run past `right` when a single element violates the rule, so guard it or let the ledger fall to zero first.

<!-- stage: exercises -->
### Exercises

#### [Build] Longest Binary Run With One Zero (Author exercise)
<!-- id: sw-one-zero-run -->

**Prerequisites.** The longest-valid pattern from this lesson, and a counter of zeros inside a window.

**Problem.** Given an array of zeros and ones, return the length of the longest contiguous stretch that contains at most one zero. Keep a count of zeros, and while it exceeds one, move `left` forward. The array must not be modified.

**Constraints.** 0 <= bits.length <= 200000 and every value is 0 or 1. One pass, O(1) extra space.

**Example 1.** Input `bits = [1, 0, 1, 1, 0, 1, 1, 1]`, output 6.

**Example 2.** Input `bits = [0, 0, 0]`, output 1.

**Hint.** When a second zero enters, which end of the window must give up elements, and how many of them? What should be recorded after that repair?

**Changed decision.** First rung: the window is allowed to be broken for a moment, and the answer is recorded only after repair.

#### [Vary] Longest Substring Without Repeating Characters (LeetCode 3)
<!-- id: sw-no-repeat-substring -->

**Prerequisites.** The one-zero exercise above, and a table of letter counts.

**Problem.** Given a string, return the length of its longest substring in which no character occurs twice. Keep multiplicities for the window and remove characters from the left, in a `while` loop, until the character that just arrived appears only once.

**Constraints.** 0 <= s.length() <= 50000 and every character has a code below 128. Linear time with at most one table of 128 counters.

**Example 1.** Input `s = "qrsqtuvr"`, output 6.

**Example 2.** Input `s = "zzzz"`, output 1.

**Hint.** What does a count of two for the new character say about which old element must leave first? Is it enough to remove just one element?

**Changed decision.** The rule is no longer a single number but a table of multiplicities, and the repair stops exactly when the newcomer's own count is back to one.

#### [Boundary] Violation At Both Ends (Author exercise)
<!-- id: sw-violation-both-ends -->

**Prerequisites.** The two exercises above, and the idea that one arriving element can force many removals.

**Problem.** Given an array of positive integers and a `long` limit, find the longest contiguous stretch whose sum does not exceed the limit. Return two numbers: the best length, and the largest number of elements removed from the left while processing a single new right element (the too-heavy element itself counts as removed). An element that is too large on its own must leave an empty window, and the sum must not overflow.

**Constraints.** 0 <= values.length <= 100000, each value is between 1 and 2147483647, and the limit is between 0 and 4000000000000. Each element enters and leaves at most once.

**Example 1.** Input `values = [2, 3, 1, 9, 2, 2], limit = 6`, output `[3, 4]`.

**Example 2.** Input `values = [7, 1, 1], limit = 5`, output `[2, 1]`.

**Hint.** What happens when the first element alone exceeds the limit? Can the loop that removes elements ever pass the right edge, and what stops it?

**Changed decision.** The violation can come at the start (an element too heavy alone, which empties the window) and at the far end (one arrival removing several), so the shrink must be a guarded loop and the sum a `long`.

#### [Recognize] Max Consecutive Ones III (LeetCode 1004)
<!-- id: sw-max-consecutive-ones-iii -->

**Prerequisites.** All three exercises above.

**Problem.** Given a binary array and an integer `k`, return the length of the longest stretch that becomes all ones if at most `k` zeros are flipped. Treat each zero as a violation with a budget of `k`, and do not actually change the array.

**Constraints.** 1 <= nums.length <= 100000, every value is 0 or 1, and 0 <= k <= nums.length. The input is read-only.

**Example 1.** Input `nums = [0, 1, 1, 0, 0, 1, 0, 1], k = 2`, output 5.

**Example 2.** Input `nums = [1, 1, 1], k = 0`, output 3.

**Hint.** What is the same as "at most k zeros inside the window"? What does the budget look like when you count it down instead of counting zeros up?

**Changed decision.** The tolerance of one zero becomes a budget parameter, which may be zero (no flips at all) or at least the number of zeros (the whole array).
