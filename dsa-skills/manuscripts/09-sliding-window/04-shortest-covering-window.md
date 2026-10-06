<!-- lesson-kind: standard -->
<!-- lesson-id: shortest-covering-window -->
## Find The Shortest Covering Window

<!-- stage: context -->
### A Snippet That Shows Too Much

A search page shows a snippet of each document: the shortest passage that contains every word of the query. A developer builds it by trying every start word and reading forward until all query words have appeared. On a document of 50,000 words, the snippet takes noticeable time. On a book of five million words, the page times out.

The longest-valid lesson shrank the window only while it was invalid. This lesson asks for the opposite goal. The answer is the shortest block that satisfies a requirement. To keep the code short, the lesson maps each word of the query to one letter, so a document becomes a string of letters. A block that already satisfies the requirement may still be too long, and the method must trim it without losing the requirement.

<!-- stage: naive -->
### Read Forward From Every Start

Each start index begins a separate search that reads forward until every required word has appeared. The first end index that works gives the shortest cover for that start. The method keeps the best result over all starts.

```java
static int shortestFromEveryStart(String s, String need) {
    int best = Integer.MAX_VALUE;
    for (int start = 0; start < s.length(); start++) {
        int[] have = new int[26];
        for (int end = start; end < s.length(); end++) {
            have[s.charAt(end) - 'a']++;
            if (covers(have, need)) {
                best = Math.min(best, end - start + 1);
                break;
            }
        }
    }
    return best == Integer.MAX_VALUE ? -1 : best;
}

static boolean covers(int[] have, String need) {
    int[] want = new int[26];
    for (int i = 0; i < need.length(); i++) want[need.charAt(i) - 'a']++;
    for (int c = 0; c < 26; c++) if (have[c] < want[c]) return false;
    return true;
}
```

The helper `covers` returns true when no letter of `need` is short in `have`. It recounts `need` on every call, which adds cost to every test.

<!-- stage: bottleneck -->
### Counting The Rereads Again

```predict
Suppose the walk from start 0 first covers the requirement at an index `e`. Could the walk from start 1 find a cover that ends before index `e`?

No. A cover from start 1 that ended before index 6 would also be a cover from start 0, because start 0 only adds one more value. Then the walk from start 0 would have stopped earlier. So the walk from start 1 ends at index `e` or later.
```

If the requirement never holds, every start reads to the end of the text. The sum of the read lengths is quadratic, O(n^2), and each test with `covers` adds the alphabet size. For `n = 5,000,000` words, the method reads about 12 trillion positions.

The end index of the shortest cover never moves back as the start moves forward. The method only needs to move both ends forward and keep the counts of the current block. The remaining question is how to know that the block covers the requirement without comparing every count each time.

<!-- stage: insight -->
### Expand Until Covered And Then Trim

#### The Missing Count Tells Whether The Block Covers

Let `need[c]` be the number of copies of character `c` that the requirement asks for. The **missing count** is the total number of required copies that the block does not yet provide. A block covers the requirement exactly when the missing count is 0. When a character `c` enters and the block holds fewer than `need[c]` copies of it, the missing count drops by one. When a character leaves and the block drops below `need[c]`, the missing count rises by one. Both updates cost O(1).

#### The Surplus Can Leave Without Harm

A character is a **surplus** when the block holds more copies of it than `need` asks for. A character that `need` never mentions is a surplus too. Removing a surplus character does not raise the missing count. A cover can therefore contain many surplus characters, and the leftmost character of a cover is often a surplus.

#### The Minimum Window Records Before It Breaks

The method expands `right` until the missing count is 0. Then it moves `left` forward while the missing count stays 0. At every such step, the block still covers the requirement, so the method records its length. The shortest block recorded is the **minimum window**. The method records first and removes second, because the removal that breaks the cover must not be counted. The invariant is that the block `[left..right]` covers the requirement whenever the method records, and no earlier start gives a shorter cover for this `right`.

<!-- names: missing count, surplus, minimum window -->

<!-- stage: variables -->
### What The Method Keeps

The method keeps the two indexes, the requirement and a ledger of what the block holds.

- **need** is the count array of the requirement, and it never changes.
- **have** is the count array of the block `s[left..right]`.
- **missing** is the number of required copies the block lacks, and it starts at the total size of the requirement.
- **best** is the length of the shortest cover found, and it starts above any possible length. The code of this lesson keeps only this length, and the Boundary exercise adds `bestStart` for the position.

<!-- stage: trace -->
### Tracing Two Scans

#### Trimming Surplus From A Cover

Take `s = "bccbbacc"` and a requirement of one `a` and one `b`. The trace below shows `missing` and the best length. The block first covers the requirement at index 5, but it holds two surplus `b` characters, because the requirement needs only one `b`, and two `c` characters that the requirement does not need at all. The method records each cover and then removes the leftmost character while the cover holds.

```trace
{"cells":["b","c","c","b","b","a","c","c"],"pointers":["left","right"],"steps":[{"at":{"left":0,"right":0},"vars":{"missing":"1","best":"none"},"note":"The character 'b' enters. It fills a required copy."},{"at":{"left":0,"right":1},"vars":{"missing":"1","best":"none"},"note":"The character 'c' enters. It is a surplus."},{"at":{"left":0,"right":2},"vars":{"missing":"1","best":"none"},"note":"The character 'c' enters. It is a surplus."},{"at":{"left":0,"right":3},"vars":{"missing":"1","best":"none"},"note":"The character 'b' enters. It is a surplus."},{"at":{"left":0,"right":4},"vars":{"missing":"1","best":"none"},"note":"The character 'b' enters. It is a surplus."},{"at":{"left":5,"right":5},"vars":{"missing":"1","best":"2"},"note":"The character 'a' enters. It fills a required copy. The block 'bccbba' covers the requirement and is the shortest so far, with length 6. The surplus 'b' leaves, and the cover holds. The block 'ccbba' covers the requirement and is the shortest so far, with length 5. The surplus 'c' leaves, and the cover holds. The block 'cbba' covers the requirement and is the shortest so far, with length 4. The surplus 'c' leaves, and the cover holds. The block 'bba' covers the requirement and is the shortest so far, with length 3. The surplus 'b' leaves, and the cover holds. The block 'ba' covers the requirement and is the shortest so far, with length 2. The character 'b' leaves and breaks the cover."},{"at":{"left":5,"right":6},"vars":{"missing":"1","best":"2"},"note":"The character 'c' enters. It is a surplus."},{"at":{"left":5,"right":7},"vars":{"missing":"1","best":"2"},"note":"The character 'c' enters. It is a surplus."}]}
```

The best length is 2, from the block `ba` at indexes 4 and 5. The first cover found had length 6, so the trim saved four positions.

#### A Requirement With Two Copies

Take `s = "abcabca"` and a requirement of two `a` characters and one `b`. The missing count starts at 3. The first `a` and the first `b` bring it to 1, and the second `a` at index 3 brings it to 0. One `a` does not meet a requirement of two copies. A test that only asks whether each letter appears would stop one `a` too early.

```trace
{"cells":["a","b","c","a","b","c","a"],"pointers":["left","right"],"steps":[{"at":{"left":0,"right":0},"vars":{"missing":"2","best":"none"},"note":"The character 'a' enters. It fills a required copy."},{"at":{"left":0,"right":1},"vars":{"missing":"1","best":"none"},"note":"The character 'b' enters. It fills a required copy."},{"at":{"left":0,"right":2},"vars":{"missing":"1","best":"none"},"note":"The character 'c' enters. It is a surplus."},{"at":{"left":1,"right":3},"vars":{"missing":"1","best":"4"},"note":"The character 'a' enters. It fills a required copy. The block 'abca' covers the requirement and is the shortest so far, with length 4. The character 'a' leaves and breaks the cover."},{"at":{"left":1,"right":4},"vars":{"missing":"1","best":"4"},"note":"The character 'b' enters. It is a surplus."},{"at":{"left":1,"right":5},"vars":{"missing":"1","best":"4"},"note":"The character 'c' enters. It is a surplus."},{"at":{"left":4,"right":6},"vars":{"missing":"1","best":"4"},"note":"The character 'a' enters. It fills a required copy. The block 'bcabca' covers the requirement, with length 6. The surplus 'b' leaves, and the cover holds. The block 'cabca' covers the requirement, with length 5. The surplus 'c' leaves, and the cover holds. The block 'abca' covers the requirement, with length 4. The character 'a' leaves and breaks the cover."}]}
```

<!-- stage: code -->
### The Trimming Scan In Java

#### Counting Missing Copies

```java
static int shortestCover(String s, String t) {
    int[] need = new int[26], have = new int[26];
    for (int i = 0; i < t.length(); i++) need[t.charAt(i) - 'a']++;
    int missing = t.length(), left = 0, best = Integer.MAX_VALUE;
    for (int right = 0; right < s.length(); right++) {
        int c = s.charAt(right) - 'a';
        if (have[c] < need[c]) missing--;
        have[c]++;
        while (missing == 0) {
            best = Math.min(best, right - left + 1);
            int d = s.charAt(left) - 'a';
            have[d]--;
            if (have[d] < need[d]) missing++;
            left++;
        }
    }
    return best == Integer.MAX_VALUE ? -1 : best;
}
```

The comparison `have[c] < need[c]` runs before the increment, so it tests whether the entering character fills a gap. The loop records before it removes, and the removal may break the cover and end the loop.

#### Cost Of The Scan

The time is O(n + m), where `m = t.length()`, because `right` advances `n` times and `left` advances at most `n` times. The memory is two arrays with one entry per letter. The method creates no substring. If the problem asks for the text, the method stores `bestStart` and `bestLength` and builds one substring at the end.

<!-- stage: applicability -->
### When The Trimming Scan Applies

#### Spotting A Shortest-Cover Request

Look for a request for the shortest contiguous block that contains required values, possibly with required copies. Phrases such as "shortest segment containing", "minimum window" and "smallest range that includes" fit. The requirement must survive adding values to the block, so a longer block never loses a cover.

#### The Invariant To State

The block covers the requirement exactly when the missing count is 0, and the method records only at such moments. A reader who states this before the loop avoids the common bug of recording after a removal has already broken the cover.

#### Exact Equality Is A False Friend

A fixed-size window test asks whether the counts of the block equal the counts of the pattern. A cover allows surplus characters, so equality is the wrong test here. The two problems look alike, because both use a pattern and a window, and they need different tests and different loops.

#### Java Habits For This Pattern

Compare the count before the increment on entry and after the decrement on exit, or the missing count drifts by one. Use `Integer.MAX_VALUE` as the initial best length and test for it at the end, so an input with no cover returns -1, or the empty string when the problem asks for text. Create the answer substring once, after the loop.

<!-- stage: exercises -->
### Exercises

#### [Build] Shortest Segment Containing A And B (Author exercise)
<!-- id: sw-shortest-ab -->

**Prerequisites.** The missing count and the trimming scan of this lesson.

**Problem.** Given a string `s` over the letters `a`, `b` and `c`, return the length of the shortest substring that contains at least one `a` and at least one `b`. Return -1 if no such substring exists.

**Constraints.**
- **Length** satisfies `0 <= s.length <= 10^5`.
- **Characters** are `a`, `b` or `c`.
- **Return** type is `int`, and -1 means no such substring.
- **Mutation** does not occur; `s` is immutable.

**Example 1.** Input `s = "bccbbacc"`. Output `2`, from `ba`.

**Example 2.** Input `s = "cccab"`. Output `2`, from `ab`.

**Hint.** The requirement has two symbols with one copy each. What is the missing count at the start?

**Changed decision.** The method records at every cover and trims, in place of stopping at the first cover.

#### [Vary] Required Multiplicities (Author exercise)
<!-- id: sw-required-multiplicities -->

**Prerequisites.** The exercise above.

**Problem.** Given a string `s` over the letters `a`, `b` and `c`, return the length of the shortest substring that contains at least two `a` characters and at least one `b`. Return -1 if no such substring exists.

**Constraints.**
- **Length** satisfies `0 <= s.length <= 10^5`.
- **Characters** are `a`, `b` or `c`.
- **Return** type is `int`, and -1 means no such substring.
- **Mutation** does not occur; `s` is immutable.

**Example 1.** Input `s = "abcabca"`. Output `4`.

**Example 2.** Input `s = "abc"`. Output `-1`, because `a` occurs once.

**Hint.** Which comparison decides whether an entering `a` lowers the missing count?

**Changed decision.** The requirement for `a` is 2, so the method tracks filled copies, not whether a letter appeared.

#### [Boundary] No Cover Exists (Author exercise)
<!-- id: sw-no-cover -->

**Prerequisites.** The two exercises above.

**Problem.** Given lowercase strings `s` and `t`, return an `int[]` of two entries, `{start, length}`, for the leftmost shortest substring of `s` that contains every character of `t` with its multiplicity. If `t` is empty, return `{0, 0}`. If no such substring exists, return `{-1, 0}`. The method must not build any substring.

**Constraints.**
- **Lengths** satisfy `0 <= s.length, t.length <= 10^5`.
- **Characters** are lowercase English letters.
- **Ties** go to the smallest start index.
- **Mutation** does not occur; the strings are immutable.

**Example 1.** Input `s = "xaybz"`, `t = "ab"`. Output `{1, 3}`.

**Example 2.** Input `s = "aab"`, `t = "abc"`. Output `{-1, 0}`.

**Hint.** What value does `missing` have at the start when `t` is empty? Which comparison keeps the leftmost start on a tie?

**Changed decision.** The empty result is a defined value, and the method reports positions in place of text.

#### [Recognize] Minimum Window Substring (LeetCode 76)
<!-- id: sw-minimum-window -->

**Prerequisites.** All three exercises above.

**Problem.** Given strings `s` and `t`, return the shortest substring of `s` that contains every character of `t`, including duplicates. If no such substring exists, return the empty string. When several substrings share the shortest length, return the leftmost.

The index of a letter in a count array of size 52 is 0 to 25 for `a` to `z` and 26 to 51 for `A` to `Z`.

**Constraints.**
- **Lengths** satisfy `1 <= s.length, t.length <= 10^5`.
- **Characters** are uppercase or lowercase English letters.
- **Return** type is `String`.
- **Mutation** does not occur; the strings are immutable.

**Example 1.** Input `s = "ADOBECODEBANC"`, `t = "ABC"`. Output `"BANC"`.

**Example 2.** Input `s = "aa"`, `t = "aaa"`. Output `""`.

**Hint.** The alphabet has 52 letters now. How does that change the array size and the index of a character?

**Changed decision.** The alphabet is larger, and the method builds the answer string once from stored boundaries.
