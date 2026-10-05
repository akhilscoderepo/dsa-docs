<!-- lesson-kind: standard -->
<!-- lesson-id: replacement-budget-window -->
## Allow K Replacements In A Window

<!-- stage: context -->
### A Cleaner That May Overwrite Few Characters

A text normalizer receives a noisy sensor string such as `aababba`. It may overwrite at most `k` characters, and it wants the longest stretch that can be turned into one repeated character. A stretch of `aaba` becomes `aaaa` after one overwrite. The first version of the tool tries every stretch and counts its characters. It finds the most common one and checks whether the others number at most `k`. On a log of a few hundred thousand characters, it runs for hours.

The earlier windows tracked a count that the window must stay under, such as zeros or distinct values. This stretch is valid for a different reason. It is valid when the number of characters that differ from the most common one is small enough. The question of this lesson is how to state that rule as one number that a window can maintain.

<!-- stage: naive -->
### Count Every Stretch From Scratch

The direct method tries each start and end index. It counts the characters of the stretch, finds the largest count, and tests whether the remaining characters number at most `k`.

```java
static int longestByTrying(String s, int k) {
    int best = 0;
    for (int start = 0; start < s.length(); start++) {
        for (int end = start; end < s.length(); end++) {
            int[] cnt = new int[26];
            for (int i = start; i <= end; i++) cnt[s.charAt(i) - 'a']++;
            int top = 0;
            for (int c : cnt) top = Math.max(top, c);
            if (end - start + 1 - top <= k) best = Math.max(best, end - start + 1);
        }
    }
    return best;
}
```

The inner counting loop rebuilds the counts of a stretch although the previous stretch differs by one character.

<!-- stage: bottleneck -->
### Counting The Work Per Stretch

```predict
A stretch of length 7 holds the letter a four times, the letter b twice and the letter c once. How many overwrites turn it into one repeated letter, and which letter should it keep?

It needs 3 overwrites, and it should keep the letter a. Overwriting the other 3 characters with a costs 3, and keeping any other letter costs more.
```

The method visits about `n^2 / 2` stretches. Each stretch costs O(length) to count, so the total is O(n^3). A version that extends `end` and keeps one count array for each start costs O(26 * n^2). For `n = 300,000`, that is still about 1.2 * 10^12 steps.

The prediction shows the shape of the test. A stretch needs `length - top` overwrites, where `top` is the largest count of one letter. The test needs two numbers, the length and the largest count. The length comes from the indexes. The window can keep the counts of its letters as the earlier windows did, and read the largest one when needed. Both indexes then move only forward.

<!-- stage: insight -->
### Measure The Cost With The Dominant Count

#### The Replacement Cost Of A Window

The **dominant count** of a window is the largest number of copies of any one character inside it. The **replacement cost** of a window is its length minus its dominant count. The replacement cost is the smallest number of overwrites that make every character in the window equal, because the best choice keeps the most frequent character and overwrites all others.

#### A Window Is Valid When The Cost Is At Most K

The window is valid when its replacement cost is at most `k`. Validity survives removal. When one character leaves, the length drops by one, and the dominant count drops by at most one, so the cost does not rise. A sub-window of a valid window is valid, so the shrink loop of the longest-valid lesson applies. When the cost exceeds `k`, the method moves `left` forward until it does not.

#### The Dominant Count Can Fall

The dominant count is not a running total. It can fall when the dominant character leaves, and then another character becomes dominant. The method keeps a count per character and finds the dominant count by scanning the counts. For a fixed alphabet, the scan costs a constant. Some programs skip the scan and keep the largest dominant count seen so far, a **stale maximum**. That shortcut needs a separate argument, which the third exercise of this lesson explores and which a later lesson proves. This lesson uses the exact scan, so the invariant is simple: after the shrink loop, the window has replacement cost at most `k`.

<!-- names: dominant count, replacement cost, stale maximum -->

<!-- stage: variables -->
### What The Method Keeps

The method keeps the two indexes, a count per character and the best length.

- **cnt** is the array of counts, one entry per letter, and it describes `s[left..right]`.
- **dominant** is the largest entry of `cnt`, found by a scan of the 26 entries.
- **length** is `right - left + 1`, and it comes from the indexes alone.
- **k** is the number of overwrites allowed, and it satisfies `k >= 0`.
- **best** is the largest valid length recorded after a shrink loop.

<!-- stage: trace -->
### Tracing Two Scans

#### Four Letters In A Row After One Overwrite

Take `s = "aababba"` and `k = 1`. The trace below shows the window text, its dominant count and its cost. The window grows while the cost stays at most 1. At index 4, the window `aabab` has length 5 and dominant count 3, so the cost is 2. The shrink loop removes two characters before the cost is 1 again.

```trace
{"cells":["a","a","b","a","b","b","a"],"pointers":["left","right"],"steps":[{"at":{"left":0,"right":0},"vars":{"window":"a","dominant":"1","cost":"0","best":"1"},"note":"The letter 'a' enters. The window 'a' has dominant count 1 and cost 0, so best is 1."},{"at":{"left":0,"right":1},"vars":{"window":"aa","dominant":"2","cost":"0","best":"2"},"note":"The letter 'a' enters. The window 'aa' has dominant count 2 and cost 0, so best is 2."},{"at":{"left":0,"right":2},"vars":{"window":"aab","dominant":"2","cost":"1","best":"3"},"note":"The letter 'b' enters. The window 'aab' has dominant count 2 and cost 1, so best is 3."},{"at":{"left":0,"right":3},"vars":{"window":"aaba","dominant":"3","cost":"1","best":"4"},"note":"The letter 'a' enters. The window 'aaba' has dominant count 3 and cost 1, so best is 4."},{"at":{"left":2,"right":4},"vars":{"window":"bab","dominant":"2","cost":"1","best":"4"},"note":"The letter 'b' enters. The window 'aabab' has length 5 and dominant count 3, so the cost is 2, above 1. The letter 'a' leaves. The window 'abab' has length 4 and dominant count 2, so the cost is 2, above 1. The letter 'a' leaves. The window 'bab' has dominant count 2 and cost 1, so best is 4."},{"at":{"left":2,"right":5},"vars":{"window":"babb","dominant":"3","cost":"1","best":"4"},"note":"The letter 'b' enters. The window 'babb' has dominant count 3 and cost 1, so best is 4."},{"at":{"left":4,"right":6},"vars":{"window":"bba","dominant":"2","cost":"1","best":"4"},"note":"The letter 'a' enters. The window 'babba' has length 5 and dominant count 3, so the cost is 2, above 1. The letter 'b' leaves. The window 'abba' has length 4 and dominant count 2, so the cost is 2, above 1. The letter 'a' leaves. The window 'bba' has dominant count 2 and cost 1, so best is 4."}]}
```

The best length is 4. The window `aaba` needs one overwrite, and so does the window `babb`.

#### The Dominant Count Falls

Take `s = "abbbcxyz"` and `k = 1`. The window `abbb` has dominant count 3. The letter `c` enters, and one removal of `a` repairs the window. Then `x` enters, and the shrink loop removes `b` three times in a row. Each removal lowers the dominant count, and after the last removal the window `cx` has dominant count 1. A method that remembers the old value 3 would believe the window is much better than it is.

```trace
{"cells":["a","b","b","b","c","x","y","z"],"pointers":["left","right"],"steps":[{"at":{"left":0,"right":0},"vars":{"window":"a","dominant":"1","cost":"0","best":"1"},"note":"The letter 'a' enters. The window 'a' has dominant count 1 and cost 0, so best is 1."},{"at":{"left":0,"right":1},"vars":{"window":"ab","dominant":"1","cost":"1","best":"2"},"note":"The letter 'b' enters. The window 'ab' has dominant count 1 and cost 1, so best is 2."},{"at":{"left":0,"right":2},"vars":{"window":"abb","dominant":"2","cost":"1","best":"3"},"note":"The letter 'b' enters. The window 'abb' has dominant count 2 and cost 1, so best is 3."},{"at":{"left":0,"right":3},"vars":{"window":"abbb","dominant":"3","cost":"1","best":"4"},"note":"The letter 'b' enters. The window 'abbb' has dominant count 3 and cost 1, so best is 4."},{"at":{"left":1,"right":4},"vars":{"window":"bbbc","dominant":"3","cost":"1","best":"4"},"note":"The letter 'c' enters. The window 'abbbc' has length 5 and dominant count 3, so the cost is 2, above 1. The letter 'a' leaves. The window 'bbbc' has dominant count 3 and cost 1, so best is 4."},{"at":{"left":4,"right":5},"vars":{"window":"cx","dominant":"1","cost":"1","best":"4"},"note":"The letter 'x' enters. The window 'bbbcx' has length 5 and dominant count 3, so the cost is 2, above 1. The letter 'b' leaves. The window 'bbcx' has length 4 and dominant count 2, so the cost is 2, above 1. The letter 'b' leaves. The window 'bcx' has length 3 and dominant count 1, so the cost is 2, above 1. The letter 'b' leaves. The window 'cx' has dominant count 1 and cost 1, so best is 4."},{"at":{"left":5,"right":6},"vars":{"window":"xy","dominant":"1","cost":"1","best":"4"},"note":"The letter 'y' enters. The window 'cxy' has length 3 and dominant count 1, so the cost is 2, above 1. The letter 'c' leaves. The window 'xy' has dominant count 1 and cost 1, so best is 4."},{"at":{"left":6,"right":7},"vars":{"window":"yz","dominant":"1","cost":"1","best":"4"},"note":"The letter 'z' enters. The window 'xyz' has length 3 and dominant count 1, so the cost is 2, above 1. The letter 'x' leaves. The window 'yz' has dominant count 1 and cost 1, so best is 4."}]}
```

<!-- stage: code -->
### Counting Replacements In Java

#### The Window With An Exact Dominant Count

```java
static int longestAfterReplacements(String s, int k) {
    int[] cnt = new int[26];
    int left = 0, best = 0;
    for (int right = 0; right < s.length(); right++) {
        cnt[s.charAt(right) - 'a']++;
        while (right - left + 1 - dominant(cnt) > k) {
            cnt[s.charAt(left) - 'a']--;
            left++;
        }
        best = Math.max(best, right - left + 1);
    }
    return best;
}

static int dominant(int[] cnt) {
    int top = 0;
    for (int c : cnt) top = Math.max(top, c);
    return top;
}
```

The loop condition uses the replacement cost directly. The method records the length after the loop, when the cost is at most `k`.

#### Cost Of The Scan

Each index enters once and leaves at most once. Each test of the loop condition scans 26 counts, so the time is O(26 * n), which is O(n) for this alphabet. The extra memory is the array of 26 counts. With a larger alphabet, the scan costs the alphabet size and needs a different structure, which a later chapter on heaps provides.

<!-- stage: applicability -->
### When The Cost Rule Applies

#### Spotting A Replacement Budget

Look for a request for the longest block that becomes uniform after at most `k` changes. The request may ask for the same character, the same bit or the same value. The cost of a block depends on its length and its most frequent value. That cost does not rise when the block loses an end.

#### The Invariant To State

After the shrink loop, the replacement cost of `s[left..right]` is at most `k`, and every discarded start is unusable for this `right` and later ones. The cost is computed from the counts of the window, and the counts describe exactly that window.

#### A Stale Maximum Is A False Friend

Some programs keep the largest dominant count seen so far and never lower it. That shortcut is correct for one specific form of the loop, and it needs a proof. The third exercise starts that proof, and a later lesson finishes it. The false friend is to apply the shortcut to every window problem. For a window that must be valid at every step, such as the minimum-cover problem, a stale value gives a wrong answer.

#### Java Habits For This Pattern

Use a count array indexed by `c - 'a'` when the contract names the alphabet. Keep the length as `right - left + 1` and never store it in a second variable that can drift. Scan the counts inside the loop condition, and do not cache the dominant count across a removal.

<!-- stage: exercises -->
### Exercises

#### [Build] Replacement Cost Of One Window (Author exercise)
<!-- id: sw-window-cost -->

**Prerequisites.** The replacement cost of this lesson.

**Problem.** Given a string `s` and two indexes `l` and `r` with `0 <= l <= r < s.length`, return the replacement cost of the substring `s[l..r]`. The cost is its length minus the largest number of copies of any one character in it.

**Constraints.**
- **Length** satisfies `1 <= s.length <= 10^5`.
- **Indexes** satisfy `0 <= l <= r < s.length`.
- **Characters** are lowercase English letters.
- **Return** type is `int`.
- **Mutation** does not occur; `s` is immutable.

**Example 1.** Input `s = "aabbbcc"`, `l = 1`, `r = 5`. Output `2`, for the window `abbbc`.

**Example 2.** Input `s = "aabbbcc"`, `l = 2`, `r = 4`. Output `0`.

**Hint.** Which count do you subtract from the length?

**Changed decision.** The method reads the counts of one fixed window, and it moves no boundary.

#### [Vary] Longest Binary Uniform Window (Author exercise)
<!-- id: sw-binary-uniform -->

**Prerequisites.** The cost exercise above.

**Problem.** Given a binary array `bits` and an integer `k`, return the length of the longest contiguous block that becomes all zeros or all ones after at most `k` flips of single values. The dominant count of a block is the larger of its number of zeros and its number of ones.

**Constraints.**
- **Length** satisfies `1 <= bits.length <= 10^5`.
- **Values** are 0 or 1.
- **Budget** satisfies `0 <= k <= bits.length`.
- **Return** type is `int`.
- **Mutation** does not occur; `bits` is unchanged.

**Example 1.** Input `bits = [1,1,0,0,1,0,0,0,1,0]`, `k = 2`. Output `8`.

**Example 2.** Input `bits = [1,0,1,0]`, `k = 1`. Output `3`.

**Hint.** The alphabet has two values. How does that change the scan for the dominant count?

**Changed decision.** The method flips toward whichever value dominates, so it tracks both counts.

#### [Boundary] Stale Maximum Trace (Author exercise)
<!-- id: sw-stale-maximum -->

**Prerequisites.** The two exercises above.

**Problem.** Given a string `s` and an integer `k`, run the longest-window scan of this lesson with an exact dominant count. After the shrink loop at each index `r`, let `exact(r)` be the dominant count of the current window. Let `seen(r)` be the largest `exact(i)` for `i <= r`. Return the number of indexes `r` where `seen(r) > exact(r)`.

**Constraints.**
- **Length** satisfies `1 <= s.length <= 10^5`.
- **Characters** are lowercase English letters.
- **Budget** satisfies `0 <= k <= s.length`.
- **Return** type is `int`.
- **Mutation** does not occur; `s` is immutable.

**Example 1.** Input `s = "aababba"`, `k = 1`. Output `2`, at indexes 4 and 6.

**Example 2.** Input `s = "abc"`, `k = 0`. Output `0`.

**Hint.** When does the exact dominant count of the window fall below its earlier peak?

**Changed decision.** The method compares a historical value with the exact one, and it reports where they differ.

#### [Recognize] Longest Repeating Character Replacement (LeetCode 424)
<!-- id: sw-char-replacement -->

**Prerequisites.** All three exercises above.

**Problem.** Given a string `s` of uppercase English letters and an integer `k`, return the length of the longest substring that becomes one repeated letter after at most `k` replacements of single characters.

**Constraints.**
- **Length** satisfies `1 <= s.length <= 10^5`.
- **Characters** are uppercase English letters.
- **Budget** satisfies `0 <= k <= s.length`.
- **Return** type is `int`.
- **Mutation** does not occur; `s` is immutable.

**Example 1.** Input `s = "AABABBA"`, `k = 1`. Output `4`.

**Example 2.** Input `s = "ABAB"`, `k = 2`. Output `4`.

**Hint.** Which earlier exercise has the same loop? Which array index maps `A` to 0?

**Changed decision.** The alphabet is uppercase, and the budget decides the loop condition.
