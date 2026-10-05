<!-- lesson-kind: standard -->
<!-- lesson-id: longest-valid-window -->
## Find The Longest Valid Window

<!-- stage: context -->
### A Report That Rereads The Same Minutes

An uptime report must name the longest stretch of consecutive minutes with at most one outage. The data holds one flag per minute, 1 for a healthy minute and 0 for an outage. A developer starts at each minute and walks forward until a second outage appears. For a month of data, 43,200 minutes, the report takes a noticeable time. For a year of per-second data, it never finishes.

The walks from neighbouring start minutes cover almost the same minutes. The walk from minute 0 already read minutes 1 to 5 on its way to the second outage. The walk from minute 1 reads them again. This lesson asks what the first walk already proves about the second.

<!-- stage: naive -->
### Walk Forward From Every Start

The direct method fixes a start index and extends the end index while the stretch stays valid. It remembers the longest stretch seen over all starts.

```java
static int longestFromEveryStart(int[] flags) {
    int best = 0;
    for (int start = 0; start < flags.length; start++) {
        int outages = 0;
        int end = start;
        while (end < flags.length && outages + (flags[end] == 0 ? 1 : 0) <= 1) {
            outages += flags[end] == 0 ? 1 : 0;
            end++;
        }
        best = Math.max(best, end - start);
    }
    return best;
}
```

The method stops a walk exactly when the next minute would add a second outage. The length of the walk is `end - start`.

<!-- stage: bottleneck -->
### Counting The Rereads

```predict
The walk from start 0 stops before index 5, so the stretch from index 0 to index 4 is valid. What does that tell you about the stretch from index 1 to index 4?

It is valid too. Removing the first minute from a valid stretch cannot add an outage. So the walk from start 1 can begin at index 5 and does not need to reread indexes 1 to 4.
```

If the array has no outage at all, every walk runs to the end of the array. The start at index `i` then reads `n - i` values, and the total is about `n * (n + 1) / 2`, which is O(n^2). For `n = 1,000,000` per-second flags, that is about 500 billion reads.

Each walk repeats the work of its neighbour. The stretch from start `i + 1` lies inside the valid stretch from start `i`. It is valid up to the same end index. The end index of the walk never needs to move backward. A method that moves both ends only forward costs O(n).

<!-- stage: insight -->
### Move Forward And Restore Validity

#### Expand By One And Check

The method **expands** the window by moving `right` forward one index, and the new value joins the window. If the window stays valid, the method records its length. If the new value makes the window invalid, the window has a **violation count** above the allowed limit. For the uptime report, the violation count is the number of outage minutes, and the limit is 1.

#### The Shrink Loop Restores Validity

A **shrink loop** moves `left` forward, one index per step, while the window is invalid. Each step removes `nums[left]` from the state. The loop stops as soon as the window is valid again, and it may run several times for one `right`. The loop is a `while`, because a single removal does not always repair the window.

#### Why Moving left Forward Is Safe

Validity here holds under removal: every block inside a valid block is also valid. After the shrink loop, `left` is therefore the smallest start that gives a valid window ending at `right`. Every start before `left` is unusable for this `right`. It stays unusable for every later `right`, because a longer block that contains an invalid block is also invalid. The invariant is that, after the loop, the window is valid and `left` never moves back. Both indexes only move forward, so the cost is O(n).

<!-- names: expand, violation count, shrink loop -->

<!-- stage: variables -->
### What The Method Keeps

The method keeps the two indexes and one summary of the window.

- **left** is the first index of the window, and it never moves backward.
- **right** is the index of the value that just entered, and it advances once per iteration.
- **violation count** is the number of outage values inside `flags[left..right]`.
- **best** is the largest length recorded after a shrink loop, and it starts at 0.

<!-- stage: trace -->
### Tracing Two Scans

#### Outages With A Limit Of One

Take `flags = [1, 1, 0, 1, 0, 1, 1]` and a limit of one outage. In the trace below, the variable `outages` is the violation count. The first outage at index 2 is allowed. The second outage at index 4 makes the window invalid. The shrink loop then moves `left` past the first outage, and only then does the method record a length.

```trace
{"cells":[1,1,0,1,0,1,1],"pointers":["left","right"],"steps":[{"at":{"left":0,"right":0},"vars":{"outages":"0","best":"1"},"note":"The value 1 enters. The window length 1 is valid, and best is 1."},{"at":{"left":0,"right":1},"vars":{"outages":"0","best":"2"},"note":"The value 1 enters. The window length 2 is valid, and best is 2."},{"at":{"left":0,"right":2},"vars":{"outages":"1","best":"3"},"note":"The value 0 enters. It is an outage, so outages is 1. The window length 3 is valid, and best is 3."},{"at":{"left":0,"right":3},"vars":{"outages":"1","best":"4"},"note":"The value 1 enters. The window length 4 is valid, and best is 4."},{"at":{"left":3,"right":4},"vars":{"outages":"1","best":"4"},"note":"The value 0 enters. It is an outage, so outages is 2. The value at index 0 leaves. The value at index 1 leaves. The outage at index 2 leaves, so outages is 1. The window length 2 is valid, and best is 4."},{"at":{"left":3,"right":5},"vars":{"outages":"1","best":"4"},"note":"The value 1 enters. The window length 3 is valid, and best is 4."},{"at":{"left":3,"right":6},"vars":{"outages":"1","best":"4"},"note":"The value 1 enters. The window length 4 is valid, and best is 4."}]}
```

The best length is 4, reached twice. The right index never moves back, and the left index only moves in the shrink loop.

#### One New Value Forces Several Removals

Take `s = "abcdbea"` and ask for the longest substring with no repeated character. The window `abcd` is valid. The next character `b` repeats a character that sits at the second position of the window. One removal of `a` does not fix it, because the first `b` is still inside. The loop removes `a` and then `b`, and so it runs twice for one `right`. A single `if` here would leave a duplicate inside the window.

```trace
{"cells":["a","b","c","d","b","e","a"],"pointers":["left","right"],"steps":[{"at":{"left":0,"right":0},"vars":{"window":"a","best":"1"},"note":"The character 'a' enters. The window 'a' has no repeat, and best is 1."},{"at":{"left":0,"right":1},"vars":{"window":"ab","best":"2"},"note":"The character 'b' enters. The window 'ab' has no repeat, and best is 2."},{"at":{"left":0,"right":2},"vars":{"window":"abc","best":"3"},"note":"The character 'c' enters. The window 'abc' has no repeat, and best is 3."},{"at":{"left":0,"right":3},"vars":{"window":"abcd","best":"4"},"note":"The character 'd' enters. The window 'abcd' has no repeat, and best is 4."},{"at":{"left":2,"right":4},"vars":{"window":"cdb","best":"4"},"note":"The character 'b' enters. The character 'a' leaves. The character 'b' leaves. The loop ran 2 times for this index. The window 'cdb' has no repeat, and best is 4."},{"at":{"left":2,"right":5},"vars":{"window":"cdbe","best":"4"},"note":"The character 'e' enters. The window 'cdbe' has no repeat, and best is 4."},{"at":{"left":2,"right":6},"vars":{"window":"cdbea","best":"5"},"note":"The character 'a' enters. The window 'cdbea' has no repeat, and best is 5."}]}
```

<!-- stage: code -->
### The Expand And Shrink Pattern In Java

#### The Loop With One Allowed Outage

```java
static int longestAtMostOneZero(int[] flags) {
    int left = 0, zeros = 0, best = 0;
    for (int right = 0; right < flags.length; right++) {
        if (flags[right] == 0) zeros++;
        while (zeros > 1) {
            if (flags[left] == 0) zeros--;
            left++;
        }
        best = Math.max(best, right - left + 1);
    }
    return best;
}
```

The `for` loop expands, the `while` loop restores validity, and the line after the `while` records the length. The `while` always ends with `left <= right`, because a window with at most one zero exists for every `right`. The length `right - left + 1` is valid at that line.

#### Cost Of Both Loops

The `for` loop runs `n` times. The `while` loop moves `left` forward, and `left` never exceeds `n`, so the `while` loop runs at most `n` times over the whole call. The time is O(n) and the extra memory is O(1).

<!-- stage: applicability -->
### When The Pattern Applies

#### Spotting A Longest-Valid Request

Look for a request for the longest contiguous range that satisfies a condition, where moving `left` forward can restore the condition. Phrases such as "at most", "no repeated" and "at most `k` changes" fit. The condition must survive removal: if a block is valid, every block inside it is valid.

#### The Invariant To State

After the shrink loop, the window is valid, and every discarded start is unusable for the current `right` and for every later one. State this before the loop. It tells the reader that recording the length after the loop is safe, and that the loop need not look back.

#### A Minimum-Cover Request Is A False Friend

A request for the shortest range that covers some requirement looks similar, because it also uses two indexes. It shrinks while the window is still valid, and it records the length before validity is lost. The longest-valid pattern shrinks only while the window is invalid, and it records after validity returns. Copying one pattern into the other gives a wrong answer that passes small samples.

#### Java Habits For This Pattern

Use `while` for the shrink step. Use a count array or a `HashMap` for the window state, and decrement the count of the leaving value before moving `left`. Do not create a substring in the loop. Keep only `left`, `right` and the best length, and build the result once at the end if the problem asks for text.

<!-- stage: exercises -->
### Exercises

#### [Build] Longest Binary Run With One Zero (Author exercise)
<!-- id: sw-one-zero -->

**Prerequisites.** The expand and shrink pattern of this lesson.

**Problem.** Given a binary array `bits`, return the length of the longest contiguous block of `bits` that contains at most one value equal to 0. A block of length 0 is not allowed unless `bits` is empty.

**Constraints.**
- **Length** satisfies `0 <= bits.length <= 10^5`.
- **Values** are 0 or 1.
- **Return** type is `int`, and the empty array gives 0.
- **Mutation** does not occur; `bits` is unchanged.

**Example 1.** Input `bits = [1,1,0,1,0,1,1]`. Output `4`.

**Example 2.** Input `bits = [0,0,0]`. Output `1`, because two zeros are not allowed.

**Hint.** What does the method subtract from the zero count when `left` passes a 0?

**Changed decision.** The method shrinks while the zero count exceeds one, and then records the length.

#### [Vary] Longest Substring Without Repeating Characters (LeetCode 3)
<!-- id: sw-longest-no-repeat -->

**Prerequisites.** The one-zero exercise above.

**Problem.** Given a string `s`, return the length of the longest substring in which every character occurs at most once.

**Constraints.**
- **Length** satisfies `0 <= s.length <= 5 * 10^4`.
- **Characters** are any ASCII characters, codes 0 to 127.
- **Return** type is `int`.
- **Mutation** does not occur; `s` is immutable.

**Example 1.** Input `s = "abcdbea"`. Output `5`, from `cdbea`.

**Example 2.** Input `s = "aaaa"`. Output `1`.

**Hint.** What must the method decrement while `left` moves? When is the window valid again?

**Changed decision.** The state changes from one zero count to a count per character, and the check becomes "no count above one".

#### [Boundary] Violation At Both Ends (Author exercise)
<!-- id: sw-many-removals -->

**Prerequisites.** The two exercises above.

**Problem.** Given a string `s`, define `first(r)` as the smallest index `l` such that `s[l..r]` has no repeated character, for each `r` from 0 to `s.length - 1`. Let `first(-1)` be 0. Return the largest value of `first(r) - first(r - 1)` over all `r`. This number is the largest forward jump of the left index at a single `r`.

**Constraints.**
- **Length** satisfies `0 <= s.length <= 5 * 10^4`.
- **Characters** are lowercase English letters.
- **Return** type is `int`, and the empty string gives 0.
- **Mutation** does not occur; `s` is immutable.

**Example 1.** Input `s = "abcdbea"`. Output `2`, at the second `b`.

**Example 2.** Input `s = "abc"`. Output `0`, because `left` never moves.

**Hint.** What is the new value of `left` when the entering character repeats one inside the window?

**Changed decision.** The answer measures the jump of `left`, so the loop must allow several removals, and an `if` cannot give the right value.

#### [Recognize] Max Consecutive Ones III (LeetCode 1004)
<!-- id: sw-max-ones-k -->

**Prerequisites.** All three exercises above.

**Problem.** Given a binary array `nums` and an integer `k`, return the length of the longest contiguous block that contains at most `k` zeros. A block of this kind becomes all ones if you flip its zeros.

**Constraints.**
- **Length** satisfies `1 <= nums.length <= 10^5`.
- **Values** are 0 or 1.
- **Limit** satisfies `0 <= k <= nums.length`.
- **Return** type is `int`.
- **Mutation** does not occur; `nums` is unchanged.

**Example 1.** Input `nums = [1,0,0,1,1,0,1]`, `k = 2`. Output `5`, from indexes 0 to 4 or from indexes 2 to 6.

**Example 2.** Input `nums = [0,0,0]`, `k = 0`. Output `0`.

**Hint.** Which earlier exercise has the same loop with a limit of one? What changes when the limit is `k`?

**Changed decision.** The limit of the zero count is a parameter, and it can be 0.
