<!-- lesson-kind: standard -->
<!-- lesson-id: center-expansion -->
## Expand Palindromes From The Center

<!-- stage: context -->
### A Word Game That Freezes

A word-game helper highlights the longest palindrome inside a line of letters. A palindrome is a string that reads the same from left to right and from right to left, such as `racecar`. On a test line of 40 letters, the helper answers at once. On a line of 2000 letters, it freezes for several seconds.

The helper checks far more substrings than the line can hold distinct answers for. The question is how a program finds the longest palindromic substring without testing every substring from scratch, using only the characters around positions in the line.

<!-- stage: naive -->
### Test Every Substring

The direct method tries every substring. It builds the reverse of the substring with a `StringBuilder` and compares the two strings. It keeps the length of the longest match.

```java
static int longestPalindromeLength(String s) {
    int best = 0;
    for (int i = 0; i < s.length(); i++) {
        for (int j = i + 1; j <= s.length(); j++) {
            String part = s.substring(i, j);
            String reversed = new StringBuilder(part).reverse().toString();
            if (part.equals(reversed)) {
                best = Math.max(best, part.length());
            }
        }
    }
    return best;
}
```

On `"abba"` the method returns 4. On `"abc"` it returns 1, because every single character is a palindrome. On the empty string it returns 0.

<!-- stage: bottleneck -->
### Every Check Rebuilds What Was Already Known

```predict
A line holds n = 2000 letters. About how many substrings does the method test, and roughly how many character operations does it spend on them? Which fact about palindromes does it ignore?

The method tests n(n + 1) / 2, which is about 2 million, substrings. Copying and reversing a substring costs time proportional to its length, so the total is about n(n + 1)(n + 2) / 6, which is about 1.3 billion operations, and the cost grows as O(n^3). It ignores the fact that a palindrome contains a smaller palindrome in its middle, so each test repeats the work of the test for the inner part.
```

A palindrome such as `racecar` contains `aceca`, which contains `cec`, which contains `e`. The method rebuilds and rechecks each of these as an unrelated string. The relation between them is simple. A string is a palindrome exactly when its first and last characters match and the substring between them is a palindrome. A correct method uses this relation to grow a palindrome outward instead of testing from scratch. The worst case then drops to O(n^2) time with O(1) extra space.

<!-- stage: insight -->
### Grow A Palindrome Outward From Its Middle

Every palindrome has a middle. The characters on its two sides mirror each other, so the middle decides which pairs must match. A loop that fixes the middle first can check only the pairs that matter.

#### Two Kinds Of Middle

A palindrome of odd length has a **center**, which is one character, and its length is 1 more than twice the number of mirrored pairs. A palindrome of even length has a **gap** as its middle, which is the position between two neighbors. Both kinds exist, so a string of length `n` has `n` odd centers and `n - 1` gaps, which makes `2n - 1` middles in total.

<!-- names: center, expand, gap -->

#### Expand While The Ends Match

For one middle, the loop sets `left` and `right`. An odd center at index `c` starts at `left = c` and `right = c`. A gap between `c` and `c + 1` starts at `left = c` and `right = c + 1`. To **expand** means to compare `s.charAt(left)` with `s.charAt(right)`. When they match, the loop moves `left` down by one and `right` up by one. The middle stays fixed during the whole attempt, and only the two ends move.

#### Stop At The First Mismatch

The first mismatch, or a bound that `left` or `right` crosses, ends the attempt. No larger palindrome around this middle exists, because every larger one would need the failed pair to match. The attempt leaves `left` and `right` one step beyond the palindrome, so its length is `right - left - 1`. The invariant is that `s[left + 1 .. right - 1]` is a palindrome around the fixed middle whenever the loop tests a new pair.

<!-- stage: variables -->
### Left End, Right End And Best Length

Three values drive each attempt, and the loop updates them as described.

- **left** is the index of the left end under test and moves down by one after a match.
- **right** is the index of the right end under test and moves up by one after a match.
- **best** keeps the longest length found for any middle so far and changes only after an attempt ends.

<!-- stage: trace -->
### Expanding From Every Middle

#### An Odd Palindrome

Take `s = "aba"`. The middle at index 0 compares `a` with itself and matches, and the next pair reaches outside the string, so the attempt ends with length 1. The gap after index 0 compares `a` with `b`, which fails at once. The middle at index 1 matches itself, then compares `a` with `a` and matches, and the next pair is outside the string. The attempt ends with length 3, so `best` becomes 3.

#### An Even Palindrome

Now take `s = "abba"`. The odd middles give length 1 each, and the first gap compares `a` with `b` and fails. The gap between indexes 1 and 2 compares `b` with `b` and matches, then `a` with `a` and matches, and the next pair is outside the string. The attempt ends with length 4. The last odd middle and the last gap add nothing new.

#### Stepping Through Both Strings

```trace
{"cells":["a","b","a"],"pointers":["left","right"],"steps":[{"at":{"left":-1,"right":0},"vars":{"best":0},"note":"Start: no middle has been tried, so best is 0."},{"at":{"left":0,"right":0},"vars":{"best":0},"note":"Odd center index 0: indexes 0 and 0 hold 'a' and 'a', which match, so both ends move outward."},{"at":{"left":-1,"right":1},"vars":{"best":1},"note":"Odd center index 0: at indexes -1 and 1, a bound is crossed, so the attempt ends with length 1. The best length is 1."},{"at":{"left":0,"right":1},"vars":{"best":1},"note":"Gap after index 0: at indexes 0 and 1, 'a' and 'b' differ, so the attempt ends with length 0. The best length is 1."},{"at":{"left":1,"right":1},"vars":{"best":1},"note":"Odd center index 1: indexes 1 and 1 hold 'b' and 'b', which match, so both ends move outward."},{"at":{"left":0,"right":2},"vars":{"best":1},"note":"Odd center index 1: indexes 0 and 2 hold 'a' and 'a', which match, so both ends move outward."},{"at":{"left":-1,"right":3},"vars":{"best":3},"note":"Odd center index 1: at indexes -1 and 3, a bound is crossed, so the attempt ends with length 3. The best length is 3."},{"at":{"left":1,"right":2},"vars":{"best":3},"note":"Gap after index 1: at indexes 1 and 2, 'b' and 'a' differ, so the attempt ends with length 0. The best length is 3."},{"at":{"left":2,"right":2},"vars":{"best":3},"note":"Odd center index 2: indexes 2 and 2 hold 'a' and 'a', which match, so both ends move outward."},{"at":{"left":1,"right":3},"vars":{"best":3},"note":"Odd center index 2: at indexes 1 and 3, a bound is crossed, so the attempt ends with length 1. The best length is 3."},{"at":{"left":2,"right":3},"vars":{"best":3},"note":"Gap after index 2: at indexes 2 and 3, a bound is crossed, so the attempt ends with length 0. The best length is 3."}]}
```

```trace
{"cells":["a","b","b","a"],"pointers":["left","right"],"steps":[{"at":{"left":-1,"right":0},"vars":{"best":0},"note":"Start: no middle has been tried, so best is 0."},{"at":{"left":0,"right":0},"vars":{"best":0},"note":"Odd center index 0: indexes 0 and 0 hold 'a' and 'a', which match, so both ends move outward."},{"at":{"left":-1,"right":1},"vars":{"best":1},"note":"Odd center index 0: at indexes -1 and 1, a bound is crossed, so the attempt ends with length 1. The best length is 1."},{"at":{"left":0,"right":1},"vars":{"best":1},"note":"Gap after index 0: at indexes 0 and 1, 'a' and 'b' differ, so the attempt ends with length 0. The best length is 1."},{"at":{"left":1,"right":1},"vars":{"best":1},"note":"Odd center index 1: indexes 1 and 1 hold 'b' and 'b', which match, so both ends move outward."},{"at":{"left":0,"right":2},"vars":{"best":1},"note":"Odd center index 1: at indexes 0 and 2, 'a' and 'b' differ, so the attempt ends with length 1. The best length is 1."},{"at":{"left":1,"right":2},"vars":{"best":1},"note":"Gap after index 1: indexes 1 and 2 hold 'b' and 'b', which match, so both ends move outward."},{"at":{"left":0,"right":3},"vars":{"best":1},"note":"Gap after index 1: indexes 0 and 3 hold 'a' and 'a', which match, so both ends move outward."},{"at":{"left":-1,"right":4},"vars":{"best":4},"note":"Gap after index 1: at indexes -1 and 4, a bound is crossed, so the attempt ends with length 4. The best length is 4."},{"at":{"left":2,"right":2},"vars":{"best":4},"note":"Odd center index 2: indexes 2 and 2 hold 'b' and 'b', which match, so both ends move outward."},{"at":{"left":1,"right":3},"vars":{"best":4},"note":"Odd center index 2: at indexes 1 and 3, 'b' and 'a' differ, so the attempt ends with length 1. The best length is 4."},{"at":{"left":2,"right":3},"vars":{"best":4},"note":"Gap after index 2: at indexes 2 and 3, 'b' and 'a' differ, so the attempt ends with length 0. The best length is 4."},{"at":{"left":3,"right":3},"vars":{"best":4},"note":"Odd center index 3: indexes 3 and 3 hold 'a' and 'a', which match, so both ends move outward."},{"at":{"left":2,"right":4},"vars":{"best":4},"note":"Odd center index 3: at indexes 2 and 4, a bound is crossed, so the attempt ends with length 1. The best length is 4."},{"at":{"left":3,"right":4},"vars":{"best":4},"note":"Gap after index 3: at indexes 3 and 4, a bound is crossed, so the attempt ends with length 0. The best length is 4."}]}
```

<!-- stage: code -->
### One Expansion Method And One Loop

#### Expanding And Measuring

```java
static int expand(String s, int left, int right) {
    while (left >= 0 && right < s.length() && s.charAt(left) == s.charAt(right)) {
        left--;
        right++;
    }
    return right - left - 1;
}

static int longestPalindromeLength(String s) {
    int best = 0;
    for (int c = 0; c < s.length(); c++) {
        best = Math.max(best, expand(s, c, c));
        best = Math.max(best, expand(s, c, c + 1));
    }
    return best;
}
```

#### What The Methods Cost

Each call to `expand` runs at most about `n / 2` rounds, because each round moves both ends outward. The main loop makes `2n` calls, so the time is O(n^2) in the worst case, which happens for a string of equal letters. The methods keep a few integers, so the space is O(1). The condition tests the bounds before it calls `charAt`, so no index outside the string is ever read. The last call, with `right = n`, returns 0 at once.

<!-- stage: applicability -->
### When Symmetry Defines The Answer

#### Look For A Mirror Around A Point

Use center expansion when the answer is a substring defined by symmetry around a point. Counting palindromic substrings, finding the longest one, and finding the longest even-length one all qualify. The invariant is that each attempt fixes its middle and widens only while the new pair matches. The two start rules, one for an odd center and one for a gap, cover every palindrome exactly once.

#### Checking One Whole String Is A False Friend

A false friend is a task that mentions palindromes and has a different structure. The question of whether a whole string reads the same backward compares the first character with the last, then the second with the second to last, and so on. That check starts at both ends and moves inward, which the later chapter on two pointers teaches. Center expansion starts in the middle and moves outward over many different middles.

#### Java Details That Cause Failures

The test `left >= 0 && right < s.length()` must come before `s.charAt(left)`, because `&&` stops at the first false operand and the call would throw on an index outside the string. A call to `s.substring(a, b)` includes index `a` and excludes index `b`. After `expand` returns length `L` for the middle that started at `(left, right)`, the start of the palindrome is not `left`, because the loop already moved `left`. The start comes from the starting middle, as the solutions show.

<!-- stage: exercises -->
### Exercises

#### [Build] Palindromic Substrings (LeetCode 647)
<!-- id: st-palindromic-substrings -->

**Prerequisites.** The expansion method and the two kinds of middle from this lesson.

**Problem.** Let `s` be a string. A palindromic substring is a contiguous block of `s` that reads the same forward and backward. Return the number of palindromic substrings of `s`. Count blocks at different positions separately, even when their text is equal.

**Constraints.** The limits are:
- **Length** satisfies `1 <= s.length() <= 1000`.
- **Characters** are lowercase English letters.
- **Answer** is an `int`.
- **Mutation** does not occur.

**Example 1.** Input `s = "level"`, output 7, from five single letters, `eve` and `level`.

**Example 2.** Input `s = "ab"`, output 2.

**Hint.** Each successful expansion step from a middle adds one palindromic substring, so what does the loop add after every match?

**Changed decision.** Basic case: the loop counts every successful step and does not keep the longest length.

#### [Vary] Longest Palindromic Substring (LeetCode 5)
<!-- id: st-longest-palindrome -->

**Prerequisites.** The substring counter above.

**Problem.** Let `s` be a string. Return a longest palindromic substring of `s`. When several have the longest length, return the one with the smallest start index.

**Constraints.** The limits are:
- **Length** satisfies `1 <= s.length() <= 1000`.
- **Characters** are English letters and digits.
- **Answer** is a substring of `s`, which is never empty.
- **Mutation** does not occur.

**Example 1.** Input `s = "xabacd"`, output `"aba"`.

**Example 2.** Input `s = "ac"`, output `"a"`, because both single letters tie and `"a"` starts first.

**Hint.** Which start index belongs to a palindrome of length `L` around the middle that began at `(left, right)`, and when should the best interval change?

**Changed decision.** The method keeps the interval of the best palindrome and not only its length, and a strict comparison keeps the leftmost tie.

#### [Boundary] Even Center (Author exercise)
<!-- id: st-even-center -->

**Prerequisites.** The two exercises above and the two kinds of middle from this lesson.

**Problem.** Given a string `s`, count the palindromic substrings of `s` that have even length. Substrings at different positions count separately.

**Constraints.** The limits are:
- **Length** satisfies `0 <= s.length() <= 1000`.
- **Characters** are lowercase English letters.
- **Equal text** at different positions still counts once for each position.
- **Answer** is 0 when `s` has no even-length palindromic substring.

**Example 1.** Input `s = "abba"`, output 2, from `bb` and `abba`.

**Example 2.** Input `s = "aaaa"`, output 4, from three copies of `aa` and one `aaaa`.

**Hint.** Which pair of indexes starts the first comparison for the gap after index `c`, and why does no odd center belong here?

**Changed decision.** Only the gap start rule applies, and the first pair compares two neighbors before any expansion happens.

#### [Recognize] Longest Even-Length Palindrome (Author exercise)
<!-- id: st-longest-even-palindrome -->

**Prerequisites.** All three exercises above.

**Problem.** Let `s` be a string. Return the longest palindromic substring of `s` whose length is even. Return the empty string when no such substring exists. Among equally long candidates, return the one that starts first.

**Constraints.** The limits are:
- **Length** satisfies `0 <= s.length() <= 1000`.
- **Characters** are lowercase English letters.
- **Answer** has even length, and the empty string counts as even.
- **Mutation** does not occur.

**Example 1.** Input `s = "xabbay"`, output `"abba"`.

**Example 2.** Input `s = "abc"`, output `""`, because no two neighbors match.

**Hint.** Which middles can produce an even-length answer, and what start index does a gap at `c` give for a length `L`?

**Changed decision.** The expansion invariant stays the same, and the start rule keeps only gaps and records the interval.
