<!-- lesson-kind: standard -->
<!-- lesson-id: longest-valid-windows -->
## Longest-Valid Windows

<!-- stage: context -->
### The Flaky Sensor

Picture a field engineer reading a strip of sensor logs, one reading per second. A 1 means the sensor reported normally and a 0 means it glitched. She will tolerate a single glitch inside a reported stretch, because one dropped reading is usually noise, but two in the same stretch suggest a real fault. Her question is easy to state: what is the longest unbroken stretch of readings that contains at most one glitch?

Look at the shape of that question. The answer is a contiguous range, the range has to satisfy a condition, and among all the ranges that do, we want the longest. The same shape shows up when you look for the longest piece of text with no repeated letter, the longest run of ones if you may flip a few zeros, or the longest subarray whose total stays inside a budget. Each asks for the longest valid contiguous range.

<!-- stage: naive -->
### The Obvious Scan

Caught off guard at a whiteboard, most of us would try every starting position. From each start, walk to the right while the stretch is still acceptable, remember how far we got, and then move on to the next start.

```java
static int longestRunBruteForce(int[] bits) {
    int best = 0;
    for (int start = 0; start < bits.length; start++) {
        int zeros = 0;
        for (int end = start; end < bits.length; end++) {
            if (bits[end] == 0) zeros++;
            if (zeros > 1) break;          // a second glitch ends this start
            best = Math.max(best, end - start + 1);
        }
    }
    return best;
}
```

The method is correct, and for a short log it is fine. The trouble only shows when the log gets long.

<!-- stage: bottleneck -->
### Where the Time Goes

Run it on `[1, 1, 0, 1, 1, 1, 0, 1]`. Starting at index 0, the inner loop reads six values, meets the second zero at index 6, and stops. Then the start moves to index 1, and the inner loop reads five of the same six values again, counting the same single zero it counted a moment ago. Start 2 does it again, and so on. Every start throws away what the previous start learned.

The damage is easiest to see on an input that never breaks, such as a log of all ones. The inner loop never hits its `break`, so start 0 reads n values, start 1 reads n - 1, and the total is n(n + 1) / 2. With n = 100,000 that is roughly five billion reads for an answer we can see at a glance. The method costs O(n^2) time and O(1) extra space, and the time is the part we cannot afford.

<!-- stage: insight -->
### Never Move Backward

Look at what start 1 had to rediscover. The range from index 0 through index 5 was already known to be valid, and moving the start from 0 to 1 removes exactly one reading. We did not need to recount anything. We needed to subtract the reading that left. So instead of restarting, keep one range alive, stretch its right edge forward to take in the next reading, and when the range becomes invalid, pull its left edge forward until it is valid again. Both edges only ever move forward.

Engineers call this technique a **sliding window**, and this particular flavor, where the length changes and the goal is the longest valid range, is a **variable-size window** or **longest-valid window**. The running count of zeros inside the window is its **violation counter**: a number that tells us at a glance whether the window is still valid.

<!-- names: sliding window, violation counter, longest-valid window -->

The left edge can safely never go backward because of one property, and it is the property to check whenever you consider this technique. Validity must be **monotone under shrinking**: if a range is valid, every smaller range inside it is valid too. Here, removing readings can never add a glitch, so the property holds. Now suppose the window from `left` to `right` is invalid. Any range that starts at or before `left` and ends at or after `right` contains that invalid window, so it is invalid as well. None of those starts can ever produce an answer again, and the left edge may leave them behind for good.

<!-- stage: variables -->
### Four Variables

The `left` index is the first position inside the window, and `right` is the last position we have taken in, so the window is the range from `left` through `right` inclusive. The variable `zeros` is the number of glitches currently inside that range. It is the violation counter, and the whole algorithm exists to keep it from exceeding one. Finally `best` remembers the longest window that was valid at the moment we measured it. Nothing else is needed, because the window never holds more than these four facts.

<!-- stage: trace -->
### One Run Through

Take `[1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1]` with a limit of one zero. The first four readings, 1, 0, 1, 1, slide in without trouble. The counter reaches 1 and the window covers indices 0 through 3, so `best` becomes 4.

At index 4 another zero arrives and the counter jumps to 2, which breaks the rule. The left edge starts to move. It passes index 0, a one, and the counter stays at 2. It passes index 1, the earlier zero, and the counter drops back to 1. The window is now indices 2 through 4, three readings long, and `best` stays at 4. Notice that one new reading forced two removals.

Indices 5, 6 and 7 are all ones, so the window quietly grows to indices 2 through 7, six readings, and `best` becomes 6. At index 8 a zero arrives and the counter hits 2 again. This time the left edge passes index 2, then 3, then 4, which is the older zero, and stops at 5. Three removals for one arrival.

Index 9 is another zero, and it is the hardest step. The counter is 2, and the only zero inside the window other than the new one sits at index 8, which is the last position the left edge can reach. So the left edge walks past 5, 6, 7 and 8 and lands on 9. The window has collapsed to the single reading at index 9. The final reading, a one at index 10, makes it two long. The answer is 6, the stretch from index 2 through index 7.

```trace
{"cells":[1,0,1,1,0,1,1,1,0,0,1],"pointers":["left","right"],"steps":[{"at":{"left":0,"right":0},"vars":{"zeros":0,"best":0},"note":"Take in index 0 (value 1)."},{"at":{"left":0,"right":0},"vars":{"zeros":0,"best":1},"note":"Measure: the window holds 1 readings, so best is 1."},{"at":{"left":0,"right":1},"vars":{"zeros":1,"best":1},"note":"Take in index 1 (value 0)."},{"at":{"left":0,"right":1},"vars":{"zeros":1,"best":2},"note":"Measure: the window holds 2 readings, so best is 2."},{"at":{"left":0,"right":2},"vars":{"zeros":1,"best":2},"note":"Take in index 2 (value 1)."},{"at":{"left":0,"right":2},"vars":{"zeros":1,"best":3},"note":"Measure: the window holds 3 readings, so best is 3."},{"at":{"left":0,"right":3},"vars":{"zeros":1,"best":3},"note":"Take in index 3 (value 1)."},{"at":{"left":0,"right":3},"vars":{"zeros":1,"best":4},"note":"Measure: the window holds 4 readings, so best is 4."},{"at":{"left":0,"right":4},"vars":{"zeros":2,"best":4},"note":"Take in index 4 (value 0). The counter now exceeds one, so the window must be repaired."},{"at":{"left":1,"right":4},"vars":{"zeros":2,"best":4},"note":"Remove index 0 (value 1) from the left."},{"at":{"left":2,"right":4},"vars":{"zeros":1,"best":4},"note":"Remove index 1 (value 0) from the left. The counter is back to one, so the window is valid."},{"at":{"left":2,"right":4},"vars":{"zeros":1,"best":4},"note":"Measure: the window holds 3 readings, so best is 4."},{"at":{"left":2,"right":5},"vars":{"zeros":1,"best":4},"note":"Take in index 5 (value 1)."},{"at":{"left":2,"right":5},"vars":{"zeros":1,"best":4},"note":"Measure: the window holds 4 readings, so best is 4."},{"at":{"left":2,"right":6},"vars":{"zeros":1,"best":4},"note":"Take in index 6 (value 1)."},{"at":{"left":2,"right":6},"vars":{"zeros":1,"best":5},"note":"Measure: the window holds 5 readings, so best is 5."},{"at":{"left":2,"right":7},"vars":{"zeros":1,"best":5},"note":"Take in index 7 (value 1)."},{"at":{"left":2,"right":7},"vars":{"zeros":1,"best":6},"note":"Measure: the window holds 6 readings, so best is 6."},{"at":{"left":2,"right":8},"vars":{"zeros":2,"best":6},"note":"Take in index 8 (value 0). The counter now exceeds one, so the window must be repaired."},{"at":{"left":3,"right":8},"vars":{"zeros":2,"best":6},"note":"Remove index 2 (value 1) from the left."},{"at":{"left":4,"right":8},"vars":{"zeros":2,"best":6},"note":"Remove index 3 (value 1) from the left."},{"at":{"left":5,"right":8},"vars":{"zeros":1,"best":6},"note":"Remove index 4 (value 0) from the left. The counter is back to one, so the window is valid."},{"at":{"left":5,"right":8},"vars":{"zeros":1,"best":6},"note":"Measure: the window holds 4 readings, so best is 6."},{"at":{"left":5,"right":9},"vars":{"zeros":2,"best":6},"note":"Take in index 9 (value 0). The counter now exceeds one, so the window must be repaired."},{"at":{"left":6,"right":9},"vars":{"zeros":2,"best":6},"note":"Remove index 5 (value 1) from the left."},{"at":{"left":7,"right":9},"vars":{"zeros":2,"best":6},"note":"Remove index 6 (value 1) from the left."},{"at":{"left":8,"right":9},"vars":{"zeros":2,"best":6},"note":"Remove index 7 (value 1) from the left."},{"at":{"left":9,"right":9},"vars":{"zeros":1,"best":6},"note":"Remove index 8 (value 0) from the left. The counter is back to one, so the window is valid."},{"at":{"left":9,"right":9},"vars":{"zeros":1,"best":6},"note":"Measure: the window holds 1 readings, so best is 6."},{"at":{"left":9,"right":10},"vars":{"zeros":1,"best":6},"note":"Take in index 10 (value 1)."},{"at":{"left":9,"right":10},"vars":{"zeros":1,"best":6},"note":"Measure: the window holds 2 readings, so best is 6."}]}
```

<!-- stage: code -->
### The Java Blueprint

```java
static int longestRunAtMostOneZero(int[] bits) {
    int left = 0, zeros = 0, best = 0;
    for (int right = 0; right < bits.length; right++) {
        if (bits[right] == 0) zeros++;
        while (zeros > 1) {                // `while`, not `if`: one arrival may force several removals
            if (bits[left] == 0) zeros--;
            left++;
        }
        best = Math.max(best, right - left + 1);   // measured only after the window is repaired
    }
    return best;
}
```

The `while` is what the trace on index 9 demanded: a single arrival can require many removals, so one `if` would leave the window invalid. The measurement comes after the repair for the same reason, since measuring earlier could record a window that violates the rule.

A nested loop usually signals quadratic time, but not here. Each index enters the window once, when `right` reaches it, and leaves at most once, when `left` passes it. Together the two edges move at most 2n steps, so the total work is O(n) with O(1) extra space. This is the amortized argument from Chapter 00: the inner loop is occasionally long, but its total across the whole run is bounded by n.

One more detail matters for later. If the allowed number of zeros were 0 instead of 1, the left edge could pass the right edge, leaving an empty window of length `right - left + 1 = 0`. That is correct and requires no special case, which is why the loop condition tests the violation counter and never compares `left` with `right`.

<!-- stage: applicability -->
### When It Applies

Reach for a longest-valid window when the answer is the longest contiguous range, the validity condition can be summarized by a small running value, and the condition is monotone under shrinking. The invariant to state aloud is this: after the repair loop, the window from `left` through `right` is valid, and every start before `left` is known to be unusable for the current `right` and for every later one.

The closest false friend is the minimum-cover window, which is the next lesson. It looks almost identical, with two edges and a counter, but it shrinks while the window is still valid and records the answer inside the shrink loop, because it wants the shortest valid range. Here we shrink only after validity breaks and record afterward. Mixing the two policies is a common source of off-by-one answers.

The technique also fails silently when monotonicity fails. Ask for the longest subarray whose sum is at most a limit, and allow negative numbers, and removing an element from the left can increase the sum. A window that is invalid may become valid after growing, so discarding left positions is no longer safe. The code still runs and still returns a number, which is exactly why the monotone check has to be conscious. When the input is a string, also avoid building substrings inside the window loop; keep the two indices and construct the result once at the end if the problem asks for the text itself.

<!-- stage: exercises -->
### Exercises

#### [Build] Longest Binary Run With One Zero (Author exercise)
<!-- id: sw-run-one-zero -->

**Prerequisites.** Chapter 01 array scans; this lesson.

**Problem.** You are given an array of bits. Return the length of the longest contiguous stretch that contains at most one 0. The input must not be modified.

**Constraints.** 1 <= bits.length <= 10^5 and each value is 0 or 1. Target O(n) time and O(1) extra space.

**Example 1.** Input `[1, 1, 0, 1, 1, 1, 0, 1]`, output `6`, from indices 0 through 5.

**Example 2.** Input `[0, 0, 0]`, output `1`, because the best stretch is a single zero.

**Hint.** When the count of zeros reaches two, which end of the window must give something up, and how will you know it has given up enough?

**Changed decision.** First rung of the ladder: introduces the violation counter and the repair loop.

#### [Vary] Longest Substring Without Repeating Characters (LeetCode 3)
<!-- id: sw-distinct-substring -->

**Prerequisites.** Frequency arrays from Chapter 03; this lesson.

**Problem.** Given a string, return the length of its longest substring in which no character appears more than once.

**Constraints.** 0 <= s.length <= 5 * 10^4. The string contains English letters, digits, symbols and spaces. Target O(n) time.

**Example 1.** Input `"dvdfkd"`, output `4`, from the substring `"vdfk"`.

**Example 2.** Input `"tmmzuxt"`, output `5`, from `"mzuxt"`. The left edge must never move backward when the second `t` arrives.

**Hint.** A window with a repeated character is invalid. How many characters might have to leave before it is valid again, and which counter tells you when to stop?

**Changed decision.** The violation changes from a count of zeros to a repeated character, so one integer becomes a table of multiplicities.

#### [Boundary] Violation At Both Ends (Author exercise)
<!-- id: sw-left-boundaries -->

**Prerequisites.** The two exercises above.

**Problem.** Use the same rule of at most one zero, but instead of the answer, return an array where entry `right` holds the value of `left` after the window has been repaired for that `right`.

**Constraints.** 1 <= bits.length <= 10^5 and each value is 0 or 1. Return an array of the same length in O(n) time.

**Example 1.** Input `[1, 1, 1, 0, 1, 0]`, output `[0, 0, 0, 0, 0, 4]`. The last reading forces the left edge to jump four positions at once.

**Example 2.** Input `[0, 0, 0]`, output `[0, 1, 2]`. Every arrival after the first forces exactly one removal.

**Hint.** Which line of your repair loop lets `left` jump by more than one position in a single step, and what stops it?

**Changed decision.** The same loop is observed instead of used: the output is the left boundary, which exposes repairs that remove several elements.

#### [Recognize] Max Consecutive Ones III (LeetCode 1004)
<!-- id: sw-flip-k-zeros -->

**Prerequisites.** The three exercises above.

**Problem.** Given a binary array and an integer k, you may flip at most k zeros to ones. Return the length of the longest run of ones you can obtain.

**Constraints.** 1 <= nums.length <= 10^5, each value is 0 or 1, and 0 <= k <= nums.length. Target O(n) time and O(1) extra space.

**Example 1.** Input `nums = [1, 0, 1, 0, 0, 1, 1]`, `k = 2`, output `5`, from indices 2 through 6 after flipping the two zeros.

**Example 2.** Input `nums = [0, 0, 0]`, `k = 0`, output `0`. The window becomes empty after every arrival.

**Hint.** What does "flip at most k zeros" say about the number of zeros the final run is allowed to contain?

**Changed decision.** The limit changes from the constant one to a parameter k, including k = 0, where the window can become empty.
