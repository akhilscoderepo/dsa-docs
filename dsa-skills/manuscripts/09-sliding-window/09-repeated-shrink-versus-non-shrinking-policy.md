<!-- lesson-kind: standard -->
<!-- lesson-id: repeated-shrink-versus-non-shrinking-policy -->
## Repeated-Shrink Versus Non-Shrinking Policy

<!-- stage: context -->
### A Painter And A Wooden Frame

A sign painter works along a long fence made of boards, and every board is painted one of twenty-six colours. She owns a small can of spare paint, enough to repaint at most k boards, and a customer wants to know the longest run of neighbouring boards that she could turn into a single colour with that can. To answer, she carries a wooden frame that lies over a run of boards and she walks it along the fence from left to right, pushing its right edge forward one board at a time.

The trouble starts when the right edge pulls in a board that makes the run too colourful to fix. She has two habits to choose from. She can pull the left edge in, one board after another, until the run is fixable again, and only then write down its width. Or she can slide the whole frame one board to the right, keeping its width, and trust that she has not lost anything. The second habit is faster, but she cannot tell whether it quietly lies to her about what is under the frame.

<!-- stage: naive -->
### Start Again At Every Board

The plain method gives every board its own attempt. For each starting board it lays a fresh tally of colours, extends the run to the right as far as the can allows, and remembers the widest run seen.

```java
static int longestByRestart(String fence, int repaints) {
    int best = 0;
    for (int start = 0; start < fence.length(); start++) {
        int[] seen = new int[26];
        int most = 0;
        for (int end = start; end < fence.length(); end++) {
            most = Math.max(most, ++seen[fence.charAt(end) - 'A']);
            if (end - start + 1 - most > repaints) break;
            best = Math.max(best, end - start + 1);
        }
    }
    return best;
}
```

For a fixed start the tally only grows, so the largest colour count is exact, and a run needs `width - most` repaints. The method returns the right width for every fence, including an empty one, which gives zero.

<!-- stage: bottleneck -->
### Each Attempt Rebuilds Its Neighbour's Tally

Two attempts that start one board apart cover almost the same boards, yet the second one builds its tally again from nothing. On a fence of n boards where one colour covers nearly everything, each attempt runs almost to the end, so the double loop does about n squared over two reads, which is O(n^2). With a hundred thousand boards that is five billion reads for a fence that could have been read once.

What the restart throws away is the run it just finished. When the right edge moves, the old run shares all but one board with the new one. So the tally should be kept, with one board added at the right and, when needed, boards taken off the left. That turns the double loop into a single pass, and the only open question is how many boards must come off the left, and whether the frame must always be a run the painter could really fix.

<!-- stage: insight -->
### Valid Window Or Length Bound

Keep one tally for the boards under the frame and move both edges only forward. The first policy keeps a **valid window** at all times: after every new board, the left edge moves in with a `while` loop until the rule holds again, and only a valid window is ever measured. The loop is needed because one new board can break the rule by more than one step. For a rule such as "no colour may repeat", a repeat of a board far on the left forces every board up to that repeat to leave, and a single removal would leave the run broken. Restoring validity is a loop, not a step.

The second policy is a trick for problems that ask only for a maximum length. The frame keeps its width unless it has just grown, so it holds a **length bound**, the widest fixable run seen so far, and not necessarily a run that is fixable now. It also keeps a **tracked maximum**, the highest count any single colour has ever reached under the frame, and it never lets that number fall when boards leave. After each new board, if `width - tracked maximum` exceeds the can, exactly one board leaves on the left. The frame then shifts instead of shrinking.

Why can the width never exceed the truth? Before the first shift, the frame holds the whole prefix and the tracked maximum is exact. A shift happens only when `width - tracked` goes one past the can, so afterwards the width equals the tracked maximum plus the can. The frame can then grow only when the new board raises the tracked maximum, which means the new board gave some colour a record count under the current frame, and that frame really needs just `width - record` repaints. So the width increases only through a genuinely fixable run, and a stale maximum can keep the width, never inflate it.

<!-- names: valid window, length bound, tracked maximum -->

The distinction also tells the two policies apart in other problems. A repeat-free run needs the first policy, because its rule has no budget that a stale number could stand for. A repainting budget lets the second policy work, because only the best length is reported.

<!-- stage: variables -->
### Edges, Tally And Two Maxima

`left` and `right` are the frame edges, both only moving forward, and `seen` holds the colour counts of the boards under the frame, decremented when a board leaves. `width` is `right - left + 1`. In the valid-window form the largest count is recomputed from `seen`, which is exact, or the rule is checked directly. In the length-bound form `tracked` is a separate variable that only goes up, and so it can exceed the exact largest count of the current frame. The answer of the second form is the final width, because the width never shrank, and it equals the number of boards minus the final `left`.

<!-- stage: trace -->
### Restoring A Run, Then Sliding It

The first trace uses the valid-window policy on the boards d, a, b, c, b, e, d, a with the rule that no letter may repeat. The step to study is the one where the second b arrives: the window d, a, b, c, b is broken, and the left edge has to move three times before it is valid again, so a single removal would have left the second b next to the first.

```trace
{"cells":["d","a","b","c","b","e","d","a"],"pointers":["l","r"],"steps":[{"at":{"l":0,"r":0},"vars":{"width":1,"best":1},"note":"Add d at position 0. No letter repeats, so the window is valid and its width 1 is recorded."},{"at":{"l":0,"r":1},"vars":{"width":2,"best":2},"note":"Add a at position 1. No letter repeats, so the window is valid and its width 2 is recorded."},{"at":{"l":0,"r":2},"vars":{"width":3,"best":3},"note":"Add b at position 2. No letter repeats, so the window is valid and its width 3 is recorded."},{"at":{"l":0,"r":3},"vars":{"width":4,"best":4},"note":"Add c at position 3. No letter repeats, so the window is valid and its width 4 is recorded."},{"at":{"l":0,"r":4},"vars":{"width":5,"best":4},"note":"Add b at position 4. It now appears twice, so the window is broken and must not be measured."},{"at":{"l":1,"r":4},"vars":{"width":4,"best":4},"note":"Remove d from the left, so l becomes 1. The repeat is still there."},{"at":{"l":2,"r":4},"vars":{"width":3,"best":4},"note":"Remove a from the left, so l becomes 2. The repeat is still there."},{"at":{"l":3,"r":4},"vars":{"width":2,"best":4},"note":"Remove b from the left, so l becomes 3. The repeat is gone, so the window is valid again."},{"at":{"l":3,"r":5},"vars":{"width":3,"best":4},"note":"Add e at position 5. No letter repeats, so the window is valid and its width 3 is recorded."},{"at":{"l":3,"r":6},"vars":{"width":4,"best":4},"note":"Add d at position 6. No letter repeats, so the window is valid and its width 4 is recorded."},{"at":{"l":3,"r":7},"vars":{"width":5,"best":5},"note":"Add a at position 7. No letter repeats, so the window is valid and its width 5 is recorded. Best width so far is 5."}]}
```

The second trace uses the length-bound policy on a fence of capital letters with a can of one repaint. The step to study is the first one where the frame stops growing and starts to shift. After that the width stays equal to the best run found so far, even though the tracked maximum can no longer be found among the boards that are currently under the frame.

```trace
{"cells":["M","M","M","M","N","P","Q","R"],"pointers":["l","r"],"steps":[{"at":{"l":0,"r":0},"vars":{"width":1,"tracked":1,"exact":1},"note":"Add M at position 0. Width minus tracked maximum 1 is at most 1, so nothing leaves and the width grows to 1."},{"at":{"l":0,"r":1},"vars":{"width":2,"tracked":2,"exact":2},"note":"Add M at position 1. Width minus tracked maximum 2 is at most 1, so nothing leaves and the width grows to 2."},{"at":{"l":0,"r":2},"vars":{"width":3,"tracked":3,"exact":3},"note":"Add M at position 2. Width minus tracked maximum 3 is at most 1, so nothing leaves and the width grows to 3."},{"at":{"l":0,"r":3},"vars":{"width":4,"tracked":4,"exact":4},"note":"Add M at position 3. Width minus tracked maximum 4 is at most 1, so nothing leaves and the width grows to 4."},{"at":{"l":0,"r":4},"vars":{"width":5,"tracked":4,"exact":4},"note":"Add N at position 4. Width minus tracked maximum 4 is at most 1, so nothing leaves and the width grows to 5."},{"at":{"l":1,"r":5},"vars":{"width":5,"tracked":4,"exact":3},"note":"Add P at position 5. Width minus tracked maximum 4 is more than 1, so one letter (M) leaves and the frame shifts. Width stays 5."},{"at":{"l":2,"r":6},"vars":{"width":5,"tracked":4,"exact":2},"note":"Add Q at position 6. Width minus tracked maximum 4 is more than 1, so one letter (M) leaves and the frame shifts. Width stays 5."},{"at":{"l":3,"r":7},"vars":{"width":5,"tracked":4,"exact":1},"note":"Add R at position 7. Width minus tracked maximum 4 is more than 1, so one letter (M) leaves and the frame shifts. Width stays 5."}]}
```

<!-- stage: code -->
### Three Forms Of The Same Pass

```java
static int longestDistinctRun(int[] nums) {
    Map<Integer, Integer> inside = new HashMap<>();
    int left = 0, best = 0;
    for (int right = 0; right < nums.length; right++) {
        inside.merge(nums[right], 1, Integer::sum);
        while (inside.get(nums[right]) > 1) {          // restore before recording
            inside.merge(nums[left++], -1, Integer::sum);
        }
        best = Math.max(best, right - left + 1);
    }
    return best;
}

static int repaintAlwaysValid(String fence, int repaints) {
    int[] seen = new int[26];
    int left = 0, best = 0;
    for (int right = 0; right < fence.length(); right++) {
        seen[fence.charAt(right) - 'A']++;
        while (right - left + 1 - Arrays.stream(seen).max().getAsInt() > repaints) {
            seen[fence.charAt(left++) - 'A']--;
        }
        best = Math.max(best, right - left + 1);
    }
    return best;
}

static int repaintOneRemoval(String fence, int repaints) {
    int[] seen = new int[26];
    int left = 0, tracked = 0;
    for (int right = 0; right < fence.length(); right++) {
        tracked = Math.max(tracked, ++seen[fence.charAt(right) - 'A']);
        if (right - left + 1 - tracked > repaints) seen[fence.charAt(left++) - 'A']--;
    }
    return fence.length() - left;
}
```

The first two forms move each edge at most n times, so the pass is linear in moves, and the second pays a scan of 26 counts for each check, which is O(26 n) and still linear for a fixed alphabet. The third needs only constant work per board, O(n) time and O(1) space, and it returns the number of boards minus `left` rather than a measured best.

<!-- stage: applicability -->
### Deciding Which Policy Is Safe

Reach for the always-valid form whenever the rule is about the content of the window, such as no repeats or every value at most a limit. State the invariant before writing the loop: after the loop body finishes, the window satisfies the rule, and it is measured only then. Write the removal as a `while`, because a single added element may need several removed ones. The one-removal form is a special licence, not a style: it needs a proof that the reported length can never exceed a length that a valid window achieves, and a tracked number that is allowed to go stale.

The nearest false friend is the habit of replacing every `while` with an `if` to save a loop. In the repeat-free problem this leaves a broken window, and the next measurement reads it. Another is trusting the width of the shifted frame as a description of the current boards, when it describes the best run seen. A third is returning the final window's contents when the question asks only for a length.

In Java, decide in advance whether the input may be modified, and here nothing is written back to the array or string. Keep the tracked maximum in an `int` that never decreases, and do not recompute it from the counts in the one-removal form, because the stale value is the whole point. If the problem asks for the window itself, use the valid-window form, since the shifted frame may contain a run that cannot be fixed.

<!-- stage: exercises -->
### Exercises

#### [Build] Restore Before Record (Author exercise)
<!-- id: sw-restore-before-record -->

**Prerequisites.** Sliding windows from the earlier lessons of this chapter, and a hash map of counts from Chapter 04.

**Problem.** Given an `int` array of ticket numbers, return the length of the longest run of neighbouring entries in which no number repeats. Use a `while` loop to restore the window after each new entry, and measure the window only when it is valid. Do not modify the array.

**Constraints.** 0 <= nums.length <= 100000, and any `int` values, including the extremes of the type. Each index may enter the window once and leave it at most once.

**Example 1.** Input `nums = [4, 7, 4, 9, 7, 1]`, output 4.

**Example 2.** Input `nums = [5, 5, 5]`, output 1.

**Hint.** After a new entry arrives, which entries must leave before the window can be trusted again? Is it always exactly one?

**Changed decision.** The measurement moves behind the loop. The window is checked for validity before it is read, so recording a broken run becomes impossible.

#### [Vary] One-Removal Maximum-Length Trace (Author exercise)
<!-- id: sw-one-removal-trace -->

**Prerequisites.** The exercise above, and the idea of a repaint budget as width minus the largest count.

**Problem.** Given a string of capital letters and a budget k, run the one-removal formulation, where the largest count is tracked and never lowered and at most one letter leaves per step. Return an `int` array holding the window width after each character. Then say what the final width represents.

**Constraints.** 0 <= s.length() <= 100000, only the letters A to Z, and 0 <= k <= s.length(). The result has the same length as the string, and the input is not changed.

**Example 1.** Input `s = "QQQRSTQ", k = 2`, output `[1, 2, 3, 4, 5, 5, 5]`.

**Example 2.** Input `s = "ABAB", k = 0`, output `[1, 1, 1, 1]`.

**Hint.** Compare each width with the best fixable run inside the part of the string read so far. Could the boards under the final window need more than k repaints?

**Changed decision.** The output is the whole sequence of widths instead of one answer, so the width is read as the best length so far and not as a statement about the current window.

#### [Boundary] Multiple Left Removals Needed (Author exercise)
<!-- id: sw-multiple-left-removals -->

**Prerequisites.** The two exercises above.

**Problem.** Given an `int` array and a limit c, find the longest run in which no value appears more than c times. Return a two-element array: that length, and the largest number of left removals that any single new entry forced. Use the input as given, and use a `while` loop.

**Constraints.** 0 <= nums.length <= 100000, 1 <= c <= 100000, any `int` values. A single step may remove many entries, and all removals together stay below the array length.

**Example 1.** Input `nums = [9, 8, 7, 1, 1, 2, 1], c = 2`, output `[6, 4]`.

**Example 2.** Input `nums = [3, 3, 3, 3], c = 1`, output `[1, 1]`.

**Hint.** When the third copy of a value arrives, how far left is the copy that has to go? What is left of the run if only one entry is removed?

**Changed decision.** The input is chosen so that one removal leaves the window invalid, and the answer exposes the longest burst of removals, which a single `if` would never perform.

#### [Recognize] Longest Repeating Character Replacement (LeetCode 424)
<!-- id: sw-replacement-both-forms -->

**Prerequisites.** All three exercises above.

**Problem.** For a string of capital letters and a budget k, compute the longest run that can be made into one letter with at most k replacements by two methods: the always-valid form that takes the exact largest count and shrinks with a `while`, and the non-shrinking form with a tracked maximum. Return four numbers: the length from the first form, the length from the second, the final tracked maximum, and the exact largest count of the final window.

**Constraints.** 0 <= s.length() <= 100000, only A to Z, 0 <= k <= s.length(). The two lengths must agree for every input, and the string is only read.

**Example 1.** Input `s = "AAAABCDE", k = 1`, output `[5, 5, 4, 1]`.

**Example 2.** Input `s = "ABAB", k = 2`, output `[4, 4, 2, 2]`.

**Hint.** In which example does the tracked maximum describe letters that are no longer under the final window? What property of that value keeps the length honest?

**Changed decision.** Earlier problems report only a length. This one reports both forms and the gap between the tracked and exact maximum, so the policy and the invariant each form needs become visible.
