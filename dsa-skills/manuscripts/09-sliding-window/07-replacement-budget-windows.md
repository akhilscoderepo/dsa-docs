<!-- lesson-kind: standard -->
<!-- lesson-id: replacement-budget-windows -->
## Replacement-Budget Windows

<!-- stage: context -->
### A Fence And A Few Paint Cans

A village fence is built from a long row of boards, and each board has been painted one of a handful of colours over the years. For the spring festival a volunteer wants one unbroken stretch of the fence to be a single colour, and she is free to choose the colour. She has paint for at most a fixed number of boards, say three, and every board she repaints turns into the colour she wants. She may leave the rest of the fence alone.

The question she brings to the committee is how long a stretch she can make uniform. A stretch that is already almost one colour needs only a few cans, but a stretch of ten boards in four colours needs far more than she owns. Each time she moves her attention one board along the fence, the colours inside her stretch change a little, and she has to decide again whether the stretch still fits her paint.

<!-- stage: naive -->
### Recount Every Stretch From Scratch

The direct plan is to try every starting board, grow the stretch one board at a time, and for each stretch count how many boards carry each colour. The commonest colour is kept, and the boards of every other colour have to be repainted. If that number fits the paint, the stretch is a candidate for the longest.

```java
static int longestByRecount(String fence, int cans) {
    int best = 0;
    for (int start = 0; start < fence.length(); start++) {
        int[] tally = new int[26];
        for (int end = start; end < fence.length(); end++) {
            tally[fence.charAt(end) - 'A']++;
            int mostCommon = 0;
            for (int t : tally) mostCommon = Math.max(mostCommon, t);
            int width = end - start + 1;
            if (width - mostCommon <= cans) best = Math.max(best, width);
        }
    }
    return best;
}
```

It is correct for any fence of capital letters. It tries every stretch exactly once, and for each one it scans all twenty-six colour counters to find the commonest colour.

<!-- stage: bottleneck -->
### Every Stretch Is Judged Alone

There are about n squared over two stretches, and the scan over twenty-six counters runs for each, so the whole method costs on the order of 26 times n squared, written O(n^2) once the alphabet is treated as a constant. A fence of one hundred thousand boards makes that billions of steps. The painful part is that a stretch and the stretch one board longer share nearly all of their boards, yet the code throws away its tallies at every new start and learns the same facts again.

Two pieces of work are repeated. The first is the tally itself, which could be carried along as the stretch moves, adding one board on the right and dropping one on the left. The second is the search for the commonest colour. Counting is cheap to maintain, but a maximum is not obviously so, because dropping a board from the left might lower it and nothing says which colour takes over. The question is whether the maximum has to be exact at all, or whether a cruder number is enough to decide the longest length.

<!-- stage: insight -->
### Cost Is Length Minus Commonest Count

A stretch needs one repaint for every board that is not of its favourite colour, so its **replacement cost** is the stretch length minus the **dominant count**, meaning the number of boards of the favourite colour. Paint on hand decides usability: the cost must be at most the number of cans. The volunteer does not need every usable stretch. She needs the widest one, and that lets the search drop a lot of bookkeeping.

Here is the classic trick. Let the frame around the stretch grow by one board whenever a new board arrives on the right. If the grown frame is unaffordable, push the left side forward by one board, so the frame travels along the fence at its current width instead of getting narrower. Its width at the end is the answer, since the width rises only when a genuinely affordable stretch of that width exists.

That is why the favourite colour's count can be a **stale maximum**. Remember the biggest such count any frame has ever held, and never lower it when boards leave on the left. After a slide it may exceed what the present frame really holds, so the frame it describes might not be affordable. That is harmless. Widening needs the remembered count to rise, and it rises only when a frame just extended truly holds that many boards of one colour. Without a rise, the extended frame costs one more than the budget allows, so the slide happens. The remembered count is therefore an upper bound reached only by real frames, and the width it pays for was real at some earlier moment.

<!-- names: replacement cost, dominant count, stale maximum -->

After each board is read, the frame width equals the widest affordable stretch inside the prefix read so far, and the remembered count equals the largest favourite-colour count among frames held. The width grows only together with that count, so the gap between them, which is the paint a frame may need, never exceeds the cans.

<!-- stage: variables -->
### Edges, Tally And Record Count

`left` and `right` are the edges of the window over the fence, and the window holds the boards from `left` up to `right`. `tally` is an array of twenty-six counters, one per capital letter, updated as boards enter on the right and leave on the left. `record` is the stale maximum: the largest single counter value seen so far, which is updated only at the moment a board enters and is never reduced. The answer is the window width at the end, which is the same as the number of boards minus the final value of `left`. For a string of two symbols, the tally is only two counters and the exact maximum is as cheap as the stale one.

<!-- stage: trace -->
### The Window Slides At Full Width

The first trace uses the fence A, A, A, B, C, D, E with one can of paint. The window grows to four boards by reading the first B, because three A boards plus one repainted board cost one can. The step to study is the fifth, where C arrives: the window would need two cans, so the left edge moves forward and the window slides at width four. From then on the record stays at 3 although the window no longer holds three boards of one colour.

```trace
{"cells":["A","A","A","B","C","D","E"],"pointers":["left","right"],"steps":[{"at":{"left":0,"right":0},"vars":{"record":1,"true max":1,"width":1},"note":"Read A at position 0: The record rises from 0 to 1. The window of width 1 costs 0, which fits 1, so it grows."},{"at":{"left":0,"right":1},"vars":{"record":2,"true max":2,"width":2},"note":"Read A at position 1: The record rises from 1 to 2. The window of width 2 costs 0, which fits 1, so it grows."},{"at":{"left":0,"right":2},"vars":{"record":3,"true max":3,"width":3},"note":"Read A at position 2: The record rises from 2 to 3. The window of width 3 costs 0, which fits 1, so it grows."},{"at":{"left":0,"right":3},"vars":{"record":3,"true max":3,"width":4},"note":"Read B at position 3: The record stays 3. The window of width 4 costs 1, which fits 1, so it grows."},{"at":{"left":1,"right":4},"vars":{"record":3,"true max":2,"width":4},"note":"Read C at position 4: the record is 3 and the window of width 5 would cost 2, more than 1. Drop A; left becomes 1 and the window slides at width 4."},{"at":{"left":2,"right":5},"vars":{"record":3,"true max":1,"width":4},"note":"Read D at position 5: the record is 3 and the window of width 5 would cost 2, more than 1. Drop A; left becomes 2 and the window slides at width 4."},{"at":{"left":3,"right":6},"vars":{"record":3,"true max":1,"width":4},"note":"Read E at position 6: the record is 3 and the window of width 5 would cost 2, more than 1. Drop A; left becomes 3 and the window slides at width 4."}]}
```

The second trace uses a longer fence with two cans, and it ends with a record that is higher than the commonest count of the final window. Look hardest at the final step, where the window holds five boards with at most two of any colour, yet the record is still 3, and the answer of width 5 is correct because a window with three boards of one colour and two repainted ones was seen earlier.

```trace
{"cells":["Q","R","R","Q","S","Q","Q","T","U"],"pointers":["left","right"],"steps":[{"at":{"left":0,"right":0},"vars":{"record":1,"true max":1,"width":1},"note":"Read Q at position 0: The record rises from 0 to 1. The window of width 1 costs 0, which fits 2, so it grows."},{"at":{"left":0,"right":1},"vars":{"record":1,"true max":1,"width":2},"note":"Read R at position 1: The record stays 1. The window of width 2 costs 1, which fits 2, so it grows."},{"at":{"left":0,"right":2},"vars":{"record":2,"true max":2,"width":3},"note":"Read R at position 2: The record rises from 1 to 2. The window of width 3 costs 1, which fits 2, so it grows."},{"at":{"left":0,"right":3},"vars":{"record":2,"true max":2,"width":4},"note":"Read Q at position 3: The record stays 2. The window of width 4 costs 2, which fits 2, so it grows."},{"at":{"left":1,"right":4},"vars":{"record":2,"true max":2,"width":4},"note":"Read S at position 4: the record is 2 and the window of width 5 would cost 3, more than 2. Drop Q; left becomes 1 and the window slides at width 4."},{"at":{"left":2,"right":5},"vars":{"record":2,"true max":2,"width":4},"note":"Read Q at position 5: the record is 2 and the window of width 5 would cost 3, more than 2. Drop R; left becomes 2 and the window slides at width 4."},{"at":{"left":2,"right":6},"vars":{"record":3,"true max":3,"width":5},"note":"Read Q at position 6: The record rises from 2 to 3. The window of width 5 costs 2, which fits 2, so it grows."},{"at":{"left":3,"right":7},"vars":{"record":3,"true max":3,"width":5},"note":"Read T at position 7: the record is 3 and the window of width 6 would cost 3, more than 2. Drop R; left becomes 3 and the window slides at width 5."},{"at":{"left":4,"right":8},"vars":{"record":3,"true max":2,"width":5},"note":"Read U at position 8: the record is 3 and the window of width 6 would cost 3, more than 2. Drop Q; left becomes 4 and the window slides at width 5."}]}
```

<!-- stage: code -->
### One Pass With A Sliding Window

```java
static int longestPaintable(String fence, int cans) {
    int[] tally = new int[26];
    int record = 0, left = 0;
    for (int right = 0; right < fence.length(); right++) {
        int now = ++tally[fence.charAt(right) - 'A'];
        record = Math.max(record, now);
        boolean tooCostly = (right - left + 1) - record > cans;
        if (tooCostly) {
            tally[fence.charAt(left) - 'A']--;
            left++;
        }
    }
    return fence.length() - left;
}

static int windowCost(String fence, int left, int right) {
    int[] tally = new int[26];
    int top = 0;
    for (int i = left; i <= right; i++) top = Math.max(top, ++tally[fence.charAt(i) - 'A']);
    return (right - left + 1) - top;
}

static int longestFlippable(int[] bits, int flips) {
    int[] seen = new int[2];
    int record = 0, left = 0;
    for (int right = 0; right < bits.length; right++) {
        record = Math.max(record, ++seen[bits[right]]);
        if ((right - left + 1) - record > flips) seen[bits[left++]]--;
    }
    return bits.length - left;
}
```

The loop reads each board once on entering and at most once on leaving, so it takes O(n) time, and the tally is a fixed array, so the extra space is O(1). The `if` instead of a `while` is deliberate: the window loses one board at most per step, and that is what keeps its width from ever shrinking.

<!-- stage: applicability -->
### Reading A Problem As A Budget

Reach for this when a question asks for the longest range that can be made all the same, or all sorted into one group, by changing at most k elements. The signal is a cost that is length minus the count of the best group, and a budget that the cost must not exceed. Before coding, write the invariant in words: the window width is the best achievable width seen so far, and a slide never lowers it.

A false friend is the exact-maximum habit. Rescanning the counters at every move gives the same answer for the longest length, so it is not wrong, but it costs twenty-six reads per step and hides why the stale value is safe. Another is the shrinking form with a `while`, which is also correct but must keep the maximum exact, and a problem that asks for the best window itself, not only its length, needs that exactness. A third is a question about the fewest changes for a fixed length, where no window grows and the plain cost formula is enough.

In Java, remember that `char` arithmetic gives an `int`, so the index is `ch - 'A'`, and that an empty string must give zero without touching the array. Test the stale maximum on a case where it exceeds the true value of the final window, because that is the case a naive rewrite breaks.

<!-- stage: exercises -->
### Exercises

#### [Build] Replacement Cost Of One Window (Author exercise)
<!-- id: sw-window-cost -->

**Prerequisites.** Counting letters in an array of twenty-six counters.

**Problem.** Given a string of capital letters and two positions `left` and `right` with `left <= right`, return the number of letters in `s[left..right]` that would have to change to make the stretch one letter. That is the stretch length minus the count of its commonest letter. Do not change the string.

**Constraints.** 1 <= s.length() <= 200000 and 0 <= left <= right < s.length(). One call may scan the stretch once, and must use a fixed amount of extra memory.

**Example 1.** Input `s = "KKLMKLKN", left = 1, right = 5`, output 3.

**Example 2.** Input `s = "ZZZZ", left = 0, right = 3`, output 0.

**Hint.** What is the cost when every letter of the stretch is the same? Which single count decides the answer, and why do the other letters not matter individually?

**Changed decision.** First rung: nothing slides yet, only the formula length minus the dominant count is proven on fixed boundaries.

#### [Vary] Longest Binary Uniform Window (Author exercise)
<!-- id: sw-binary-flips -->

**Prerequisites.** The cost exercise above.

**Problem.** Given an array of zeros and ones and an integer `flips`, return the length of the longest stretch that becomes all zeros or all ones after flipping at most `flips` of its entries. The array may not be changed.

**Constraints.** 0 <= bits.length <= 100000 and 0 <= flips <= bits.length. Each entry is 0 or 1. Run in one pass over the array.

**Example 1.** Input `bits = [1, 0, 0, 1, 0, 1, 1], flips = 1`, output 4.

**Example 2.** Input `bits = [0, 1, 0, 1, 1, 1], flips = 0`, output 3.

**Hint.** With two symbols, how many counters are there? Which of them is the dominant count after a step, and what happens when the window becomes too costly?

**Changed decision.** The alphabet shrinks to two values, so either symbol may be the one that wins, and the stretch may end up all zeros or all ones.

#### [Boundary] Stale Maximum Trace (Author exercise)
<!-- id: sw-stale-maximum -->

**Prerequisites.** The two exercises above.

**Problem.** Run the sliding window with the stale maximum on a string of capital letters and a budget `k`. Return a pair: the longest length the window reaches and the number of positions at which the stale maximum is strictly greater than the true commonest count of the current window. The window must never shrink in width.

**Constraints.** 0 <= s.length() <= 100000 and 0 <= k <= s.length(). The reported length must also equal the best usable stretch for every prefix of the string.

**Example 1.** Input `s = "MMMNOPQ", k = 1`, output `[4, 3]`.

**Example 2.** Input `s = "ABCD", k = 0`, output `[1, 0]`.

**Hint.** When does the left edge move? At that moment compare the stale value with a recount of the current window. Why does the length stay correct even if they differ?

**Changed decision.** The maximum is allowed to be wrong about the current window, and the exercise is to show that the length it supports is still right.

#### [Recognize] Longest Repeating Character Replacement (LeetCode 424)
<!-- id: sw-char-replacement -->

**Prerequisites.** All three exercises above.

**Problem.** Given a string of capital English letters and an integer `k`, you may replace any character with any other at most `k` times in total. Return the length of the longest substring that can become all one letter.

**Constraints.** 0 <= s.length() <= 100000 and 0 <= k <= s.length(). The string is not modified. Return the length only.

**Example 1.** Input `s = "PQQPRPPS", k = 2`, output 5.

**Example 2.** Input `s = "XYZ", k = 0`, output 1.

**Hint.** What is the cost of a window in terms of its width and one count? Which single value must never decrease so that the window can only slide or grow?

**Changed decision.** The answer is only the length, so the maximum count does not have to be exact, and the window grows or slides but never shrinks.
