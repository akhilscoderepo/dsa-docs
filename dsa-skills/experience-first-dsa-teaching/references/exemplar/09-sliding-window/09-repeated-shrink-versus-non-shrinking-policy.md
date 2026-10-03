<!-- lesson-kind: standard -->
<!-- lesson-id: repeated-shrink-versus-non-shrinking-policy -->
## Repeated-Shrink Versus Non-Shrinking Policy

<!-- stage: context -->
### Two Versions Of The Same Solution

Two engineers post solutions to the same window problem. Hers has a `while` loop that pulls the left edge forward until the window is fine. His has an `if` in the same place, so the left edge moves by at most one step per new element, and the code is a few lines shorter. Both pass the examples in the problem statement. One of them is subtly wrong on some inputs, and which one it is depends on the problem.

This lesson is about that choice. Every window solution so far restored validity before it used the window. A second style exists, popular in published solutions, where the window never gets smaller and its length quietly stands for the best answer so far. Knowing when that second style is a proven shortcut and when it is a bug is a recognition skill, not a coding trick.

<!-- stage: naive -->
### Swap Every While For An If

The tempting rule is mechanical. Wherever a window solution repairs itself with a `while`, change it to an `if` and drop one line of work per step. Here is the longest substring without repeating characters, written that way.

```java
static int longestUniqueOneRemoval(String s) {
    int[] count = new int[128];
    int left = 0, best = 0;
    for (int right = 0; right < s.length(); right++) {
        char incoming = s.charAt(right);
        count[incoming]++;
        if (count[incoming] > 1) {            // `if`, not `while`
            count[s.charAt(left)]--;
            left++;
        }
        best = Math.max(best, right - left + 1);
    }
    return best;
}
```

On `abcabc` it returns 3, which is right, and on `dvdfkd` it returns 4, which is also right. The code looks like an optimization and survives the usual examples.

<!-- stage: bottleneck -->
### The Input That Breaks It

Run it on `abba`. The correct answer is 2, from `ab` or `ba`. The method returns 3. The reason is visible at the second `b`. The window is `abb`, which holds a repeat, and the `if` removes exactly one element, the leading `a`. The window is now `bb`, still holding a repeat, and the code moves on. When the final `a` arrives its own count is one, so the check sees nothing wrong, and the method measures the window `bba`, which holds two `b`s and is invalid.

This is not a performance issue at all. The `if` version has the same O(n) cost as the loop, and it gives a wrong answer. The check looked only at the arriving letter, a local symptom, while the real question was whether the whole window is valid. After one removal the window kept an old violation that the arriving letter could not reveal.

<!-- stage: insight -->
### Valid Window Or Candidate Length

There are two honest policies, and each carries a different promise. In the **repeated-shrink policy**, the repair loop runs until the window is valid, so after the loop the window is a real range, and anything computed from it, such as its boundaries, a count of ranges ending there, or its contents, can be trusted. Counting lessons, minimum-cover lessons and any question that needs the actual boundaries depend on this promise.

In the **non-shrinking policy**, the left edge moves at most one step per arrival, so the window length never decreases. The window is not promised to be valid. Its length is promised to equal a **candidate length**: the longest valid length found so far. The code can report the final length, never the boundaries, because the final window might not be a valid range.

<!-- names: repeated-shrink policy, non-shrinking policy, candidate length -->

Why can a length stand in for a window? Suppose the longest valid length so far is `L` and the window holds `L` elements ending just before `right`. When `right` arrives, the only window of length `L + 1` that ends there is the current one. If an exact test says it is valid, the length grows. If the test says it is invalid, then, because validity is monotone under shrinking, every longer window ending at `right` is invalid too, so the best length stays `L` and sliding by one keeps the size. Nothing is lost.

That argument needs three things. The objective is a maximum length and nothing else. Validity is monotone under shrinking. And the test after each arrival answers exactly whether the whole window is valid, using a global measure such as a counter of zeros, a count of distinct values, or a counter of letters that appear twice. A local symptom, such as the arriving letter's count, is not enough, as the failing input showed. The replacement-budget problem passes a different way: its test uses the stored maximum, which can only overstate validity, and the earlier argument showed that the reported length is still achievable.

So the question to ask is never whether an `if` is faster, since the cost is the same. It is whether the code is allowed to give up the valid window, and whether the test it uses is exact or proved safe.

<!-- stage: variables -->
### What Each Policy Keeps

Both policies keep `left`, `right` and the tallies. The repeated-shrink policy adds the promise that after the loop the tallies describe a valid window, so no further variable is needed. The non-shrinking policy adds a global violation measure that is exact for the current window, or a stored quantity such as `maxFreq` with its own proof, and treats the length `right - left + 1` as the candidate length, which equals the final answer after the last element is processed. A good habit is to write down, in one sentence next to the loop, which of the two promises the code is making.

<!-- stage: trace -->
### One Run Through

First the failing case. The string `abba` enters one letter at a time under the one-removal rule. The first two letters, `a` and `b`, are fine. The second `b` creates a repeat, and the rule removes the leading `a`. The window is now `bb`. The check has no further effect, because the policy allows only one removal, so the window stays at length 2 and still holds a repeat. The final `a` arrives with a count of one, so nothing triggers, and the window grows to `bba`, three letters with a repeated `b`. The reported length of 3 is wrong. With a global duplicate counter in place of the local check, the same string behaves: at the second `b` the counter is above zero and one letter leaves, and at the final `a` the counter is still above zero, so another letter leaves and the window ends as `ba`, length 2.

Now the proved case. Take `AABABBA` with a budget of one replacement and the non-shrinking rule. The window grows while its stored cost is within budget, reaching length 4 at index 3. At index 4 the cost exceeds the budget, so the left edge slides by one and the length stays at 4. The same slide happens at indices 5 and 6. The window never shrinks, and its length at the end, 4, is the answer.

Along the way some of those windows are not truly valid, since the stored maximum overstates the dominant count, as the previous lesson showed. That does not matter here, because the length is a candidate length, and a valid window of length 4 did exist earlier, namely `AABA`.

```trace
{"cells":["a","b","b","a"],"pointers":["left","right"],"steps":[{"at":{"left":0,"right":0},"vars":{"len":1,"duplicate":"no"},"note":"Take in index 0 (letter a)."},{"at":{"left":0,"right":1},"vars":{"len":2,"duplicate":"no"},"note":"Take in index 1 (letter b)."},{"at":{"left":0,"right":2},"vars":{"len":3,"duplicate":"yes"},"note":"Take in index 2 (letter b). A repeat is inside the window."},{"at":{"left":1,"right":2},"vars":{"len":2,"duplicate":"yes"},"note":"One removal only: drop index 0 (letter a). The window still holds a repeat."},{"at":{"left":1,"right":3},"vars":{"len":3,"duplicate":"yes"},"note":"Take in index 3 (letter a). A repeat is inside the window."}]}
```

```trace
{"cells":["A","A","B","A","B","B","A"],"pointers":["left","right"],"steps":[{"at":{"left":0,"right":0},"vars":{"len":1,"maxFreq":1},"note":"Take in index 0 (letter A). The window holds 1 letters and the stored maxFreq is 1."},{"at":{"left":0,"right":1},"vars":{"len":2,"maxFreq":2},"note":"Take in index 1 (letter A). The window holds 2 letters and the stored maxFreq is 2."},{"at":{"left":0,"right":2},"vars":{"len":3,"maxFreq":2},"note":"Take in index 2 (letter B). The window holds 3 letters and the stored maxFreq is 2."},{"at":{"left":0,"right":3},"vars":{"len":4,"maxFreq":3},"note":"Take in index 3 (letter A). The window holds 4 letters and the stored maxFreq is 3."},{"at":{"left":0,"right":4},"vars":{"len":5,"maxFreq":3},"note":"Take in index 4 (letter B). The window holds 5 letters and the stored maxFreq is 3."},{"at":{"left":1,"right":4},"vars":{"len":4,"maxFreq":3},"note":"The cost exceeds the budget, so slide: drop index 0 (letter A) and keep the length at 4."},{"at":{"left":1,"right":5},"vars":{"len":5,"maxFreq":3},"note":"Take in index 5 (letter B). The window holds 5 letters and the stored maxFreq is 3."},{"at":{"left":2,"right":5},"vars":{"len":4,"maxFreq":3},"note":"The cost exceeds the budget, so slide: drop index 1 (letter A) and keep the length at 4."},{"at":{"left":2,"right":6},"vars":{"len":5,"maxFreq":3},"note":"Take in index 6 (letter A). The window holds 5 letters and the stored maxFreq is 3."},{"at":{"left":3,"right":6},"vars":{"len":4,"maxFreq":3},"note":"The cost exceeds the budget, so slide: drop index 2 (letter B) and keep the length at 4."}]}
```

<!-- stage: code -->
### The Java Blueprint

```java
// Repeated-shrink policy: the window is valid after the loop, so boundaries can be trusted.
static int replaceShrink(String s, int k) {
    int[] tally = new int[26];
    int left = 0, maxFreq = 0, best = 0;
    for (int right = 0; right < s.length(); right++) {
        maxFreq = Math.max(maxFreq, ++tally[s.charAt(right) - 'A']);
        while (right - left + 1 - maxFreq > k) {
            tally[s.charAt(left) - 'A']--;
            left++;
        }
        best = Math.max(best, right - left + 1);
    }
    return best;
}

// Non-shrinking policy, stored-maximum test: length is a candidate length.
static int replaceSlide(String s, int k) {
    int[] tally = new int[26];
    int left = 0, maxFreq = 0;
    for (int right = 0; right < s.length(); right++) {
        maxFreq = Math.max(maxFreq, ++tally[s.charAt(right) - 'A']);
        if (right - left + 1 - maxFreq > k) {      // at most one step; the length never decreases
            tally[s.charAt(left) - 'A']--;
            left++;
        }
    }
    return s.length() - left;                       // the final window length is the candidate length
}

// Non-shrinking policy, exact global test: a counter of letters that appear more than once.
static int uniqueSlide(String s) {
    int[] count = new int[128];
    int repeats = 0, left = 0;
    for (int right = 0; right < s.length(); right++) {
        if (++count[s.charAt(right)] == 2) repeats++;
        if (repeats > 0) {                          // the whole window is tested, not only the new letter
            if (--count[s.charAt(left)] == 1) repeats--;
            left++;
        }
    }
    return s.length() - left;
}
```

The first two methods return the same number for every input, and the second one has no `best` variable. It does not need one, because the length never goes down, so the final length is also the largest length. The third method repairs the failing example from the bottleneck stage. Its counter `repeats` is exact for the window as it stands, so a violation left behind by an earlier one-step slide is noticed on the next arrival.

Each method states its promise. Only the first can answer a follow-up that asks for the start of the best stretch or the replaced string, because only its window is known to be valid at the moment of measurement.

All three loops run in O(n) time with a fixed-size table. The policies differ in what the code is allowed to claim, not in speed.

<!-- stage: applicability -->
### When It Applies

Reach for the non-shrinking policy only when four conditions hold together. The question asks for a maximum length and nothing else. Validity is monotone under shrinking. The test run after each arrival is exact for the whole window, or comes with a proof that it can only overstate validity in a harmless way. And no part of the answer needs the window boundaries. The invariant to state is that the window length equals the candidate length, the longest valid length found so far.

The first false friend is the blanket rule that an `if` is an optimization. It is not a rule, and the failing `abba` input shows what happens when the test is only a local symptom. The second false friend is using the non-shrinking form for a question it cannot answer. Counting windows, as in the exactly-K and count-all lessons, add a block of valid starts and so need the true `left`. Minimum-cover windows shrink while valid and need the true boundaries. Anything that returns the best stretch itself needs a valid window at the moment of recording.

When you are unsure, default to the repeated-shrink policy. It is correct whenever validity is monotone, and the only thing it gives up is one variable. When you do use the non-shrinking form, write the proof as a comment, and cross-check it against the repeated-shrink version on random short inputs, because the two must agree everywhere.

Check the usual setup items too. State the symbol domain, handle a budget of zero, and note in the contract whether the method promises boundaries.

<!-- stage: exercises -->
### Exercises

#### [Build] Restore Before Record (Author exercise)
<!-- id: sw-restore-before-record -->

**Prerequisites.** The longest-valid lesson; this lesson for the validity promise.

**Problem.** Given a string of lowercase letters, return the length of the longest substring in which every letter appears at most twice. Use a repair loop, and before every measurement, check that no letter in the window has a count above two. If the check ever fails, throw an `IllegalStateException`.

**Constraints.** 0 <= s.length <= 10^5 and `s` contains only lowercase English letters. Target O(n) time and O(1) extra space.

**Example 1.** Input `s = "aaabbb"`, output `4`, from the substring `"aabb"`.

**Example 2.** Input `s = "abcabc"`, output `6`, since every letter appears twice in the whole string.

**Hint.** The check before the measurement is only worth having if the loop above it truly restores validity. Which loop construct guarantees that after one arrival with a count of three?

**Changed decision.** First rung of the ladder: the validity promise is turned into a runtime check, so a loop that fails to repair is caught immediately.

#### [Vary] One-Removal Maximum-Length Trace (Author exercise)
<!-- id: sw-one-removal-trace -->

**Prerequisites.** The exercise above, and the replacement-budget lesson.

**Problem.** Given a string `s` of capital letters and a budget `k`, run the non-shrinking replacement algorithm, which moves `left` at most once per arrival. Return an array where entry `i` is the window length after processing index `i`.

**Constraints.** 1 <= s.length <= 10^5, `s` contains only capital letters, and 0 <= k <= s.length. Target O(n) time.

**Example 1.** Input `s = "AABABBA"`, `k = 1`, output `[1, 2, 3, 4, 4, 4, 4]`.

**Example 2.** Input `s = "ABCD"`, `k = 0`, output `[1, 1, 1, 1]`. With no budget, the window slides by one for every new letter after the first.

**Hint.** The entries never decrease. What does each entry represent, given that the window itself may not be valid, and how does it relate to the longest valid length of the prefix?

**Changed decision.** The length trace is observed instead of used, which shows that each entry is the best length for its prefix and not the size of a valid window.

#### [Boundary] Multiple Left Removals Needed (Author exercise)
<!-- id: sw-multiple-removals -->

**Prerequisites.** The two exercises above.

**Problem.** For a string `s` of lowercase letters, return a two-element array. The first entry is the length of the longest substring without repeating characters, computed with a repair loop. The second is the value returned by the one-removal variant, which uses an `if` that fires only when the arriving letter's count exceeds one, and reports the largest window length it ever measured.

**Constraints.** 0 <= s.length <= 10^5 and `s` contains only lowercase English letters. Target O(n) time.

**Example 1.** Input `s = "abba"`, output `[2, 3]`. One removal leaves `bb` invalid, so the variant overstates.

**Example 2.** Input `s = "abcabc"`, output `[3, 3]`. Every repeat needs only one removal, so the two agree.

**Hint.** What property of the input makes one removal insufficient, and why can a check that looks only at the arriving letter fail to notice the leftover repeat?

**Changed decision.** The input is chosen so that one arrival forces several removals, which is the only case where the two policies diverge.

#### [Recognize] Longest Repeating Character Replacement, Both Policies (LeetCode 424)
<!-- id: sw-replacement-both-policies -->

**Prerequisites.** The three exercises above.

**Problem.** Solve the replacement problem from the previous lesson twice for an uppercase string `s` and a budget `k`: once with the repeated-shrink policy and once with the non-shrinking policy. Return the common answer, and have your code throw an `IllegalStateException` if the two policies ever disagree.

**Constraints.** 1 <= s.length <= 10^5, `s` contains only capital letters, and 0 <= k <= s.length. Target O(n) time.

**Example 1.** Input `s = "XYXXY"`, `k = 1`, output `4`.

**Example 2.** Input `s = "BBABCBB"`, `k = 1`, output `4`.

**Hint.** Which of the two promises, a valid window or a candidate length, does each version make, and which stored quantity must never decrease for the second one to be safe?

**Changed decision.** Both policies must be written for one problem and checked against each other, which forces the invariant of each to be stated.

#### [Extend] Non-Shrinking Without Repeats (Author exercise)
<!-- id: sw-unique-non-shrinking -->

**Prerequisites.** The four exercises above.

**Problem.** Return the length of the longest substring without repeating characters, but use the non-shrinking policy: the left edge moves at most one step per arrival and the result is the final window length. Your test must be exact for the whole window, so keep a counter of letters that currently appear more than once.

**Constraints.** 0 <= s.length <= 10^5 and `s` contains only lowercase English letters. Target O(n) time and O(1) extra space.

**Example 1.** Input `s = "abba"`, output `2`, which the local-check variant gets wrong.

**Example 2.** Input `s = "qrrstq"`, output `4`, from `"rstq"`. The local-check variant reports 5 here.

**Hint.** Which counter must change when a count moves from one to two, and from two back to one, so that it is exact after every arrival and every departure?

**Changed decision.** The test changes from a local symptom to an exact global counter, which is what makes the non-shrinking policy safe for this problem.
