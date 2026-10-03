<!-- lesson-kind: standard -->
<!-- lesson-id: center-expansion -->
## Center Expansion

<!-- stage: context -->
### A Mirror On A Row Of Tiles

A tiler lays a row of patterned tiles and wants to know where the pattern reads the same in both directions. She has a small hand mirror. She stands it upright on one tile, looks along the row, and compares the tile one step to the left with the tile one step to the right, then two steps either side, and so on. As long as each pair looks identical the reflection is perfect. The first mismatch ends that attempt, and she lifts the mirror and tries the next spot.

She also notices that the mirror does not have to stand on a tile. Set on the seam between two tiles, it can reflect a pattern like blue, red, red, blue, where nothing sits in the very middle. A symmetric stretch is defined by where the mirror stands, and everything else follows from comparing outward in pairs.

<!-- stage: naive -->
### Reverse Every Stretch And Compare

The direct method takes every stretch of tiles, reverses it and checks whether the reversal equals the stretch.

```java
static int countByReversing(String row) {
    int total = 0;
    for (int i = 0; i < row.length(); i++) {
        for (int j = i + 1; j <= row.length(); j++) {
            String piece = row.substring(i, j);
            if (piece.equals(new StringBuilder(piece).reverse().toString())) total++;
        }
    }
    return total;
}
```

On `aaa` it returns 6, which is right: three single tiles, two stretches of two and the whole row. It is easy to believe and easy to test on short rows.

<!-- stage: bottleneck -->
### Every Stretch Is Checked From Scratch

There are about `n * n / 2` stretches, and each reversal and comparison costs time proportional to its length, so the total is O(n * n * n). With `n = 2000` that is billions of character operations, and every substring also allocates two new strings. Worse, the checks share nothing. If `cabac` is symmetric, then `aba` inside it is symmetric for exactly the same reason, but the method compares both again from nothing.

The waste is that a symmetric stretch is symmetric because of its middle. If the stretch from `left` to `right` is symmetric and the characters just outside it match, the next larger stretch is symmetric too, and if they do not match, no larger stretch around the same middle can be. One mismatch ends everything around that middle, and the method does not use that fact at all.

<!-- stage: insight -->
### Grow Outward From Every Middle

Fix the middle and the whole family of symmetric stretches around it becomes a single walk. **Center expansion** places two boundaries at the middle and moves them apart one step at a time, left going down and right going up, while the two characters they point at are equal. Each successful step is one more symmetric stretch around that middle, and the first failed comparison, or either boundary leaving the string, ends the walk. The invariant is that before each comparison, the stretch strictly between `left` and `right` is symmetric.

<!-- names: center expansion, odd center, even center -->

There are two kinds of middle, and both must be tried. An **odd center** is a single character, so both boundaries start on the same index and the stretch has odd length. An **even center** is the gap between two neighbours, so the boundaries start at `i` and `i + 1` and the stretch has even length. A string of length `n` has `n` odd centers and `n - 1` even centers, so `2n - 1` walks in all, and each walk costs at most O(n). Skipping the even centers is the most common bug, because `abba` has no odd center that finds its full symmetry.

The total is O(n * n) in the worst case, for example `aaaa`, where every walk goes far, and it is much faster on typical text because most walks fail at once. Space is O(1), since a walk keeps two integers, and a count or a best interval is all that needs to be remembered.

<!-- stage: variables -->
### Two Boundaries Around One Middle

For one attempt, `left` and `right` are the only moving state. They start on the same index for an odd center and on adjacent indices for an even center, and the middle never changes during the attempt. The outer loop moves the middle across the string. A counting question adds one per successful step. A longest question compares the finished length, which is `right - left - 1` once the walk has stopped, because the stopping position is one step past the last matching pair on each side, and remembers the start index `left + 1`.

<!-- stage: trace -->
### Two Walks Around Two Middles

```trace
{"cells":["z","a","b","a","z"],"pointers":["left","right"],"steps":[{"at":{"left":2,"right":2},"vars":{"center":"odd 2","found":1},"note":"Compare 'b' at 2 with 'b' at 2. They match, so found becomes 1. Move the boundaries outward."},{"at":{"left":1,"right":3},"vars":{"center":"odd 2","found":2},"note":"Compare 'a' at 1 with 'a' at 3. They match, so found becomes 2. Move the boundaries outward."},{"at":{"left":0,"right":4},"vars":{"center":"odd 2","found":3},"note":"Compare 'z' at 0 with 'z' at 4. They match, so found becomes 3. Move the boundaries outward."},{"at":{"left":-1,"right":5},"vars":{"center":"odd 2","found":3},"note":"Stop: a boundary is outside the string. The walk found 3 symmetric stretches."}]}
```

The first walk uses the odd center at index 2 of `zabaz`. Both boundaries start on the `b`, which matches itself and counts one stretch. The boundaries then move to the two `a` tiles, which match, and then to the two `z` tiles, which match. The next move would put `left` at -1, outside the string, so the walk stops with three symmetric stretches around that middle.

```trace
{"cells":["a","b","b","a"],"pointers":["left","right"],"steps":[{"at":{"left":1,"right":2},"vars":{"center":"even 1|2","found":1},"note":"Compare 'b' at 1 with 'b' at 2. They match, so found becomes 1. Move the boundaries outward."},{"at":{"left":0,"right":3},"vars":{"center":"even 1|2","found":2},"note":"Compare 'a' at 0 with 'a' at 3. They match, so found becomes 2. Move the boundaries outward."},{"at":{"left":-1,"right":4},"vars":{"center":"even 1|2","found":2},"note":"Stop: a boundary is outside the string. The walk found 2 symmetric stretches."}]}
```

The second walk uses the even center between the two `b` characters of `abba`. The boundaries start at indices 1 and 2, and they already match. They move to indices 0 and 3, where `a` matches `a`. The next move leaves the string and the walk stops with two stretches, `bb` and `abba`. No odd center would have discovered either of them.

<!-- stage: code -->
### Counting, Keeping The Best And Even Only

```java
static int expandCount(String s, int left, int right) {
    int found = 0;
    while (left >= 0 && right < s.length() && s.charAt(left) == s.charAt(right)) {
        found++;
        left--;
        right++;
    }
    return found;
}

static int countPalindromes(String s) {
    int total = 0;
    for (int c = 0; c < s.length(); c++) {
        total += expandCount(s, c, c);            // odd center
        total += expandCount(s, c, c + 1);        // even center, between c and c + 1
    }
    return total;
}

static int expandLength(String s, int left, int right) {
    while (left >= 0 && right < s.length() && s.charAt(left) == s.charAt(right)) {
        left--;
        right++;
    }
    return right - left - 1;                      // boundaries stopped one step past the last match
}

static String longestPalindrome(String s) {
    int bestStart = 0, bestLen = 0;
    for (int c = 0; c < s.length(); c++) {
        int odd = expandLength(s, c, c);
        int even = expandLength(s, c, c + 1);
        int len = Math.max(odd, even);
        if (len > bestLen) {
            bestLen = len;
            bestStart = c - (len - 1) / 2;
        }
    }
    return s.substring(bestStart, bestStart + bestLen);
}
```

The walks are O(n * n) in total and O(1) in extra space, apart from the single `substring` call at the end, which copies the answer once. Both boundaries are checked against the string limits before the characters are read, so an attempt that reaches an edge stops instead of throwing. For an empty string the outer loop does nothing and the method returns the empty string, since `bestLen` stays 0. The even walk at the last index starts with `right == s.length()` and stops immediately with length 0.

<!-- stage: applicability -->
### When Symmetry Has A Middle

Use center expansion when the question is about substrings that read the same in both directions, or any stretch defined by symmetry around a point. The invariant to say aloud is that the stretch strictly between the boundaries is symmetric, so one more matching pair extends it and one mismatch ends the walk. Always try both an odd and an even middle.

The false friend is checking one whole string from its two ends. Testing whether a given string is a palindrome is a two-pointer walk inward from the opposite ends and needs no middle, because there is a single candidate. Counting or finding symmetric substrings has many candidates, and walking inward from the ends of each one is the slow method of the naive section.

Java points are small but real. Reading with `charAt` avoids allocating substrings, and one `substring` at the end copies the answer once. Compare characters with `==` and whole strings with `equals`. Use `right - left - 1` after the loop, not the loop counter, to get the length, because the boundaries have already moved one step too far. For very long strings, the O(n * n) worst case is acceptable at a few thousand characters, and a different technique is needed beyond that.

<!-- stage: exercises -->
### Exercises

#### [Build] Palindromic Substrings (LeetCode 647)
<!-- id: st-palindromic-substrings -->

**Prerequisites.** Chapter 00 contract reading; center expansion from this lesson.

**Problem.** Given a string `s`, return the number of substrings that read the same forwards and backwards. Substrings at different positions count separately even if their text is equal. A single character is a palindrome.

**Constraints.** 1 <= s.length() <= 1000, lowercase letters only. Aim for quadratic time and constant extra space.

**Example 1.** Input `s = "abc"`, output 3, from the three single characters.

**Example 2.** Input `s = "aaa"`, output 6, from three single characters, two pairs and the whole string.

**Hint.** How many middles does a string of length `n` have, counting both kinds? What does each successful step of an expansion contribute?

**Changed decision.** First rung: a symmetric stretch is found from its middle outward instead of being checked from scratch.

#### [Vary] Longest Palindromic Substring (LeetCode 5)
<!-- id: st-longest-palindromic -->

**Prerequisites.** The build exercise above.

**Problem.** Return the longest substring of `s` that reads the same in both directions. If several have the maximum length, return the one that starts first.

**Constraints.** 1 <= s.length() <= 1000, letters and digits. Strict improvement is needed to replace the best, so ties keep the earlier one.

**Example 1.** Input `s = "dcbabcx"`, output `"cbabc"`.

**Example 2.** Input `s = "ac"`, output `"a"`, since both single characters tie and the first wins.

**Hint.** What must you remember besides the length to cut the answer out at the end? How do you compute the start from a middle and a length?

**Changed decision.** The walk's result is an interval to keep, not a count to add.

#### [Boundary] Even Center (Author exercise)
<!-- id: st-even-center -->

**Prerequisites.** The two exercises above.

**Problem.** Count only the palindromic substrings of even length. Each one is centered between two adjacent characters, so only gap centers are tried. Explain why walks that start on a single character can never find them.

**Constraints.** 0 <= s.length() <= 10^4. A gap center exists only between two characters, so a string of length 1 has none.

**Example 1.** Input `s = "abba"`, output 2, from `bb` and `abba`.

**Example 2.** Input `s = "abc"`, output 0, because no two neighbours are equal.

**Hint.** Where do the two boundaries start for a gap center? What happens at the last index, where there is no neighbour on the right?

**Changed decision.** The starting positions of the boundaries change from equal to adjacent, with the same stopping rule.

#### [Recognize] Longest Even-Length Palindrome (Author exercise)
<!-- id: st-longest-even-palindrome -->

**Prerequisites.** All three exercises above.

**Problem.** Return the longest palindromic substring whose length is even, or the empty string if none exists. If several have the same length, return the earliest. Use the same expansion invariant with the boundaries starting on adjacent indices.

**Constraints.** 0 <= s.length() <= 5000, lowercase letters only. Only even middles are tried.

**Example 1.** Input `s = "xabbay"`, output `"abba"`.

**Example 2.** Input `s = "abcd"`, output `""`, since no two neighbours match.

**Hint.** What is the length of the stretch after an expansion that stops, and how do you tell that no even palindrome exists at all?

**Changed decision.** Only one kind of middle is allowed, so the answer can be empty and must be handled as a normal result.
