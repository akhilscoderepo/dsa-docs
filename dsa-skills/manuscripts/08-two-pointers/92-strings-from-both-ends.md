<!-- lesson-kind: combination -->
<!-- lesson-id: strings-from-both-ends -->
## Check Strings From Both Ends

<!-- stage: context -->
### A Sign-Up Form That Rejects Good Names

A sign-up form offers a bonus feature: it detects whether a phrase reads the same backward and forward, such as a motto or a nickname. The first version compares the text with its reverse. Users type phrases such as `Madam, I'm Adam`. The form says no, because the comma, the apostrophe, the space and the capital letters all count in a plain comparison.

The fix has to ignore punctuation and letter case. The question is how a program can compare the letters at the two ends of the text, skip what does not count, and avoid building new strings.

<!-- stage: contributions -->
### What Strings And Pointers Each Add

A Java `String` gives indexed access to its characters with `charAt`, and each access costs O(1). The class `Character` classifies a character with methods such as `isLetterOrDigit` and changes its case with `toLowerCase`. These two facilities decide which characters count and when two characters are equal. A `String` is also immutable, so no method can swap two of its characters. Reversal needs a `char[]` or a new string.

Two pointers supply the movement. One pointer starts at each end, and the pair of characters under the pointers is a symmetric pair. The pointers do not know what a letter is, and the string does not know where to look next. Together they compare the right pairs in one pass over the text. A second movement pattern appears too: both pointers can also move in the same direction at different rates, which is a different problem.

<!-- stage: naive -->
### Cleaning The Text And Reversing A Copy

The direct method builds a clean copy that keeps only letters and digits in lowercase. It reverses the copy and compares the two strings.

```java
static boolean isPalindromeSlow(String s) {
    StringBuilder clean = new StringBuilder();
    for (int i = 0; i < s.length(); i++) {
        char c = s.charAt(i);
        if (Character.isLetterOrDigit(c)) clean.append(Character.toLowerCase(c));
    }
    String forward = clean.toString();
    String backward = clean.reverse().toString();
    return forward.equals(backward);
}
```

For `Madam, I'm Adam` the clean copy is `madamimadam`, and both strings are equal, so the method returns true. The method is correct, and it handles any text.

```predict
The text holds 10 million characters, and its first letter differs from its last letter. How many characters does `isPalindromeSlow` process before it answers, and how many characters must a comparison of the two ends inspect?

The slow method cleans all 10 million characters and reverses them, so it processes the whole text and holds two extra strings. A comparison of the two ends can answer after one pair. The slow method is O(n) in time and O(n) in extra space.
```

<!-- stage: bottleneck -->
### The Copies Answer Questions Nobody Asked

The method builds two strings of length up to `n` before it compares a single pair. It spends O(n) time and O(n) memory even when the first pair already differs. The clean copy keeps a second copy of the text, and the reversed copy keeps a third.

The answer depends on pairs of characters at mirrored positions, and each pair can be read straight from the original text. The only work that is not obvious is the skipping of characters that do not count, and that skipping can be done by moving the pointer, with no copy.

<!-- stage: insight -->
### Compare Mirrored Characters In Place

#### The Mirrored Pair

A **symmetric pair** is the pair of characters at positions `left` and `right`, with `left` starting at 0 and `right` starting at `n - 1`. A text is a palindrome when every symmetric pair holds equal characters. The scan compares one pair, then moves both pointers inward by one, until the pointers meet.

#### Skipping Characters That Do Not Count

The **skip rule** moves a pointer past a character that the problem ignores, before the pair is compared. Under the rule, `left` moves right while the character at `left` is not a letter or digit. The pointer `right` moves left under the same test. Each skip is one pointer step, so the total number of steps over the whole scan is at most `n`. The characters are then compared in lowercase.

<!-- names: symmetric pair, skip rule -->

#### Reversing And One Repair

Reversal swaps each symmetric pair, so it needs a mutable `char[]`, and it takes `n / 2` swaps. A near-palindrome that allows one deletion adds one **repair**: at the first mismatch, the scan tries two cases, with the left character removed and with the right character removed. Each case checks the remaining range as a plain palindrome, so the total cost stays O(n).

#### Pointers That Move The Same Way

A subsequence test starts both pointers at the beginning. The pointer over the long text moves every round, and the pointer over the pattern moves only when its character matches. This movement is not symmetric, and it needs no elimination argument.

<!-- stage: variables -->
### What The Scan Remembers

The scan keeps these names.

- **left** and **right** are the indexes of the current symmetric pair, and they move toward each other.
- **s** is the text, which the scan reads and never changes in the comparison problems.
- **chars** is a `char[]` copy, used only by the reversal problem, where the scan writes.

The comparison loop runs while `left < right`. When the pointers meet or cross, no pair is left, and the text has passed.

<!-- stage: trace -->
### Comparing Pairs And Repairing One Mismatch

#### A Phrase With Punctuation

The text is `Madam, I'm Adam`. The pointers skip the comma, the space and the apostrophe, and they compare the letters in lowercase. Each skip is one step of one pointer, and each comparison moves both pointers. Every compared pair matches, so the answer is true.

```trace
{"cells":["M","a","d","a","m",","," ","I","'","m"," ","A","d","a","m"],"pointers":["left","right"],"steps":[{"at":{"left":0,"right":14},"vars":{"pair":"m and m"},"note":"The letters m and m match, so both pointers move inward."},{"at":{"left":1,"right":13},"vars":{"pair":"a and a"},"note":"The letters a and a match, so both pointers move inward."},{"at":{"left":2,"right":12},"vars":{"pair":"d and d"},"note":"The letters d and d match, so both pointers move inward."},{"at":{"left":3,"right":11},"vars":{"pair":"a and a"},"note":"The letters a and a match, so both pointers move inward."},{"at":{"left":4,"right":10},"vars":{},"note":"The character ' ' at right is ignored, so right moves left."},{"at":{"left":4,"right":9},"vars":{"pair":"m and m"},"note":"The letters m and m match, so both pointers move inward."},{"at":{"left":5,"right":8},"vars":{},"note":"The character ',' at left is ignored, so left moves right."},{"at":{"left":6,"right":8},"vars":{},"note":"The character ' ' at left is ignored, so left moves right."},{"at":{"left":7,"right":8},"vars":{},"note":"The character \"'\" at right is ignored, so right moves left."},{"at":{"left":7,"right":7},"vars":{},"note":"The pointers have met, so every counted pair matched and the answer is true."}]}
```

#### One Deletion Allowed

The text is `abcddcbea`. The first pair matches, and the second pair at positions 1 and 7 holds `b` and `e`. The scan then tests the range without the left character and the range without the right character. The first range is `cddcbe`, and it is not a palindrome. The second range is `bcddcb`, and it is a palindrome. The answer is therefore true.

```trace
{"cells":["a","b","c","d","d","c","b","e","a"],"pointers":["left","right"],"steps":[{"at":{"left":0,"right":8},"vars":{"pair":"a and a"},"note":"The characters a and a match, so both pointers move inward."},{"at":{"left":1,"right":7},"vars":{"pair":"b and e"},"note":"The characters b and e differ. The scan now tests two ranges."},{"at":{"left":2,"right":7},"vars":{"range":"cddcbe"},"note":"Without the left character, the range cddcbe is not a palindrome."},{"at":{"left":1,"right":6},"vars":{"range":"bcddcb"},"note":"Without the right character, the range bcddcb is a palindrome, so the answer is true."}]}
```

<!-- stage: code -->
### The Scan In Java

```java
static boolean isPalindrome(String s) {
    int left = 0, right = s.length() - 1;
    while (left < right) {
        while (left < right && !Character.isLetterOrDigit(s.charAt(left))) left++;
        while (left < right && !Character.isLetterOrDigit(s.charAt(right))) right--;
        if (Character.toLowerCase(s.charAt(left)) != Character.toLowerCase(s.charAt(right))) return false;
        left++;
        right--;
    }
    return true;
}
```

The inner loops keep the guard `left < right`, so a text of only punctuation ends without reading outside the string. An empty text and a text with no letters or digits return true, because no pair is compared. The method reads the string and allocates nothing. The class `Character` works on UTF-16 units, so a character outside the Basic Multilingual Plane counts as two units here.

<!-- stage: applicability -->
### When The Two Ends Fit

#### The Invariant

The invariant is that every symmetric pair outside the range from `left` to `right` has already been compared and matched. The skip rule keeps the invariant true, because an ignored character belongs to no pair. When the pointers meet, the remaining range has at most one counted character, and that character is its own mirror.

#### The False Friend

The nearest wrong idea is to use the same two pointers for a subsequence test. A palindrome check moves both pointers inward and compares mirrored positions. A subsequence test moves both pointers to the right at different rates and never compares mirrored positions. Reusing the inward movement on the subsequence problem compares the first pattern character with the last text character and gives wrong answers.

#### Conditions That Break The Fit

The method needs a rule that tells which characters count, and it needs equality that does not depend on neighbors. A check for a palindrome of words needs a tokenizer first. For text that holds characters outside the Basic Multilingual Plane, the scan compares pieces of a character, and the code must walk by code point instead.

<!-- stage: exercises -->
### Exercises

#### [Build] Valid Palindrome (LeetCode 125)
<!-- id: tp-valid-palindrome -->

**Prerequisites.** The scan of this lesson.

**Problem.** Given a string `s`, return `true` when the string reads the same forward and backward after every uppercase letter becomes lowercase and every character that is not a letter or digit is removed. The empty result counts as a palindrome.

**Constraints.** The limits are:
- **Length** is `0 <= s.length() <= 2 * 10^5`; the empty string is valid.
- **Characters** are printable ASCII characters.
- **Counted characters** are letters and digits only, and `_` is not counted.
- **Extra space** is O(1), and the method does not build a new string.

**Example 1.** Input `s = "Madam, I'm Adam"`, output `true`.

**Example 2.** Input `s = "Ab, 9a"`, output `false`.

**Hint.** Move each pointer past ignored characters before you compare. What stops the inner loops from running off the string?

**Changed decision.** Basic case: skipping happens before the comparison, and the guard keeps the pointers in range.

#### [Vary] Reverse String (LeetCode 344)
<!-- id: tp-reverse-chars -->

**Prerequisites.** The first exercise above and the reversal remark in the insight.

**Problem.** Given a `char[]` named `chars`, reverse its elements in place so that the first element becomes the last. The method returns nothing.

**Constraints.** The limits are:
- **Length** is `0 <= chars.length <= 10^5`; the empty array is valid.
- **Elements** are `char` values.
- **Mutation** is required, and the extra space is O(1).
- **Pairs** are swapped once, so a middle element of an odd length stays.

**Example 1.** Input `chars = ['d','o','g','s']`, output `['s','g','o','d']`.

**Example 2.** Input `chars = ['x']`, output `['x']`.

**Hint.** A `String` cannot be edited. Which pairs do you swap, and when do the pointers stop?

**Changed decision.** The pointers write instead of read, so the loop swaps the pair at each step.

#### [Boundary] Valid Palindrome II (LeetCode 680)
<!-- id: tp-palindrome-one-delete -->

**Prerequisites.** The first exercise and the repair rule of this lesson.

**Problem.** Given a string `s` of lowercase letters, return `true` when `s` can become a palindrome after deleting at most one character. Characters are not skipped or normalized.

**Constraints.** The limits are:
- **Length** is `1 <= s.length() <= 10^5`.
- **Characters** are lowercase English letters.
- **Deletion** removes zero or one character, at any position.
- **Extra space** is O(1).

**Example 1.** Input `s = "abcddcbea"`, output `true`.

**Example 2.** Input `s = "abc"`, output `false`.

**Hint.** At the first mismatch, test exactly two cases. Why is it enough to test only the first mismatch?

**Changed decision.** The first mismatch opens two branches, and each branch needs a plain palindrome check on the rest.

#### [Recognize] Is Subsequence (LeetCode 392)
<!-- id: tp-is-subsequence -->

**Prerequisites.** All exercises above and the false friend of this lesson.

**Problem.** Given two strings `s` and `t`, return `true` when `s` is a subsequence of `t`. A subsequence keeps the relative order of its characters and may skip characters of `t`.

**Constraints.** The limits are:
- **Length** of `s` is `0 <= s.length() <= 100`; the empty string is a subsequence of every string.
- **Length** of `t` is `0 <= t.length() <= 10^4`.
- **Characters** are lowercase English letters.
- **Extra space** is O(1).

**Example 1.** Input `s = "ace"` and `t = "abcde"`, output `true`.

**Example 2.** Input `s = "aec"` and `t = "abcde"`, output `false`.

**Hint.** Both pointers move right. Which pointer moves every round, and which moves only on a match?

**Changed decision.** The pointers move in the same direction at different rates, so no pair is mirrored.
