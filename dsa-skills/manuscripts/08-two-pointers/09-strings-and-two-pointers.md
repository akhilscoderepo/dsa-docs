<!-- lesson-kind: combination -->
<!-- lesson-id: strings-and-two-pointers -->
## Strings And Two Pointers

<!-- stage: context -->
### The Bracelet Engraver

A craft stall at a street market engraves names and short sayings on strips of metal that are bent into bracelets. Customers love sayings that read the same from the clasp end as from the other end, so the engraver is asked all day to check a customer's phrase before she starts cutting. The customer writes the phrase with capital letters, spaces, commas and exclamation marks, and she is happy to ignore all of those, because the metal only carries the letters and digits and nobody cares about capitals.

Her habit is to copy the phrase letter by letter onto a clean card, leaving out everything she ignores, and then to write the card out a second time backwards underneath it and compare the two lines. It works, but a queue forms. Some customers give her a saying with a single wrong letter and ask whether crossing out one letter would rescue it. Others only want to know if the little saying she can fit on a bracelet could be found, in order but with gaps, inside the long phrase on their t-shirt.

<!-- stage: contributions -->
### What Each Part Brings

Strings bring characters that can be compared one at a time and found by position. A `String` answers `charAt(i)` in constant time, so any two characters of a phrase can be set side by side without copying anything, and a `char[]` can also be changed in place, which a `String` never allows. A string alone offers no plan for which two positions to compare, and the natural plan of building a cleaned copy allocates memory and does the work even when the first and the last letters already disagree.

Two pointers bring the plan. One pointer stands at each end and walks inward, or both walk the same way at different speeds, and every step compares or moves exactly the characters that the question needs. Pointers alone have nothing to point at without positions in a sequence, and they cannot tell a letter that matters from a comma that does not. The characters supply the equality test and the skip test, and the pointers decide which pair meets next.

The recognition cue is a question about a text that is answered by comparing characters at positions chosen from the two ends or from two ranges: reads the same both ways, reverse it, becomes that after removing one, contains these in order. The decision to watch is which movement the question asks for, since the first three move in from the ends and the last moves along.

<!-- stage: naive -->
### Copy, Reverse, Compare Cards

The direct approach is the engraver's own habit: build a cleaned card of lowercase letters and digits, build a reversed copy of it, and compare the two cards.

```java
static boolean readsSameByCopying(String phrase) {
    StringBuilder card = new StringBuilder();
    for (int k = 0; k < phrase.length(); k++) {
        char c = phrase.charAt(k);
        if (Character.isLetterOrDigit(c)) card.append(Character.toLowerCase(c));
    }
    String forwards = card.toString();
    String backwards = card.reverse().toString();
    return forwards.equals(backwards);
}
```

It returns the right answer for every phrase, including a phrase made only of punctuation, whose card is empty and therefore reads the same both ways.

<!-- stage: bottleneck -->
### The Copies Cost Work And Memory

The cleaned card is O(n) extra memory, the reversed card is another O(n), and both are built completely before a single letter is compared. A phrase of a million characters whose first and last letters differ is still read and copied from start to end, although one comparison would have settled it. The comparison itself is a third full pass when the phrase is a palindrome. The running time stays O(n), but the constant is large and the memory is not O(1).

The one-letter repair makes it worse. Trying every letter as the one to cross out, then rebuilding and checking the whole card, repeats an O(n) test n times, which is O(n^2). The test for a second candidate begins by comparing exactly the letters that the first test already found equal. The copies hide the fact that the question is symmetric: the first letter must match the last, then the second must match the one before the last, and so on inward, so the first mismatch can be found by walking in from both ends without making a copy, in O(n) time and O(1) extra space.

<!-- stage: insight -->
### Walk In From Both Ends

For a palindrome the pointers `left` and `right` start at the two ends and each pair they compare is a **mirror pair**: the character at distance k from the front and the character at distance k from the back. Noise characters are skipped in place. Before comparing, `left` advances past anything that is not a letter or digit, and `right` retreats past the same, so the cleaned text is never built. After a match both pointers step inward. The invariant is that every mirror pair outside the window has been checked and matched, and when the pointers meet or cross, the remaining window has at most one character, which always matches itself.

Reversing a `char[]` is the same walk with a swap in place of a comparison. The invariant becomes that everything outside the window is already in reversed position, and the window holds the middle, still in original order. The swap is legal only because an array may be changed, which is why the Java contract says `char[]` and not `String`.

At the first mismatch of a mirror pair, a **single repair** may be allowed. All the pairs outside the window matched, so after removing one character the window's two end characters still stand at the ends of what is left, and they differ. Therefore the removed character must be one of the two ends. The repair then tries exactly two cases: drop the left character and check the rest of the window as a plain palindrome, or drop the right character and check the rest. If either is a palindrome, the answer is yes, and a third case never needs a look.

When the question is whether one text appears inside another in order, the pointers no longer face each other. A **left-to-right match** keeps one pointer on the long text that moves at every step and one on the short text that moves only on equal characters. The invariant is that the short text's first `i` characters occur, in order, within the part of the long text already passed, and taking the earliest occurrence of each never costs a later match.

<!-- names: mirror pair, single repair, left-to-right match -->

<!-- stage: variables -->
### Ends, Window And Repair Budget

`left` and `right` are positions in the string or the character array, and the loop runs while `left < right`, so a middle character is never compared with itself. In the subsequence problem the two pointers are `at` in the long text, which moves on every step, and `matched` in the short text, which moves only when the characters agree, and the answer is whether `matched` reaches the short text's length. The skip test is a method call on one character, and the compare is made on the lowercased characters so that capitals are treated as equal. The repair check is a separate helper that takes the two ends of a window, because the helper must not be allowed another repair. Swaps use a temporary `char`, and the number of swaps is half the length rounded down.

<!-- stage: trace -->
### One Clean Walk And One Repair

The first trace checks the phrase "Madam, I'm Adam" after noise is ignored. The cells are the characters of the phrase, spaces and punctuation included, and the pointers `left` and `right` stand on the characters being compared. The step to study is the seventh, where `left` sits on the comma at position 5 and is moved past it before any comparison is made. The walk ends when the pointers meet on the letter I at position 7, with every compared pair equal.

```trace
{"cells":["M","a","d","a","m",","," ","I","'","m"," ","A","d","a","m"],"pointers":["left","right"],"steps":[{"at":{"left":0,"right":14},"vars":{"pair":"mm"},"note":"'M' and 'm' are equal after lowercasing, so left becomes 1 and right becomes 13."},{"at":{"left":1,"right":13},"vars":{"pair":"aa"},"note":"'a' and 'a' are equal after lowercasing, so left becomes 2 and right becomes 12."},{"at":{"left":2,"right":12},"vars":{"pair":"dd"},"note":"'d' and 'd' are equal after lowercasing, so left becomes 3 and right becomes 11."},{"at":{"left":3,"right":11},"vars":{"pair":"aa"},"note":"'a' and 'A' are equal after lowercasing, so left becomes 4 and right becomes 10."},{"at":{"left":4,"right":10},"vars":{"skipped":"' '"},"note":"Position 10 holds ' ', which is noise, so right becomes 9 before any comparison."},{"at":{"left":4,"right":9},"vars":{"pair":"mm"},"note":"'m' and 'm' are equal after lowercasing, so left becomes 5 and right becomes 8."},{"at":{"left":5,"right":8},"vars":{"skipped":"','"},"note":"Position 5 holds ',', which is noise, so left becomes 6 before any comparison."},{"at":{"left":6,"right":8},"vars":{"skipped":"' '"},"note":"Position 6 holds ' ', which is noise, so left becomes 7 before any comparison."},{"at":{"left":7,"right":8},"vars":{"skipped":"\"'\""},"note":"Position 8 holds \"'\", which is noise, so right becomes 7 before any comparison."}]}
```

The second trace asks whether the text "abcxcbda" can become a palindrome by removing at most one character. The first mismatch appears between the b at position 1 and the d at position 6. The step to study is the first repair test, which drops the left end and fails inside the window, after which the second test drops the right end and succeeds. The notes name which test each step belongs to, and a positive answer needs only one test to pass.

```trace
{"cells":["a","b","c","x","c","b","d","a"],"pointers":["left","right"],"steps":[{"at":{"left":0,"right":7},"vars":{"test":"scan"},"note":"'a' and 'a' match, so both pointers move inward."},{"at":{"left":1,"right":6},"vars":{"test":"first mismatch"},"note":"'b' at 1 and 'd' at 6 differ. Only these two characters can be the one removed, so two windows are tested."},{"at":{"left":2,"right":6},"vars":{"test":"drop left"},"note":"drop left: 'c' and 'd' differ, so this window is not a palindrome and the test fails."},{"at":{"left":1,"right":5},"vars":{"test":"drop right"},"note":"drop right: 'b' and 'b' match, so both pointers move inward."},{"at":{"left":2,"right":4},"vars":{"test":"drop right"},"note":"drop right: 'c' and 'c' match, so both pointers move inward."},{"at":{"left":3,"right":3},"vars":{"test":"drop right"},"note":"drop right: the pointers met with every pair equal, so this window is a palindrome."}]}
```

<!-- stage: code -->
### Palindrome, Reversal, Repair And Matching

```java
static boolean readsSameIgnoringNoise(String phrase) {
    int left = 0, right = phrase.length() - 1;
    while (left < right) {
        if (!Character.isLetterOrDigit(phrase.charAt(left))) { left++; continue; }
        if (!Character.isLetterOrDigit(phrase.charAt(right))) { right--; continue; }
        if (Character.toLowerCase(phrase.charAt(left)) != Character.toLowerCase(phrase.charAt(right))) return false;
        left++;
        right--;
    }
    return true;
}

static void reverseInPlace(char[] chars) {
    for (int left = 0, right = chars.length - 1; left < right; left++, right--) {
        char keep = chars[left];
        chars[left] = chars[right];
        chars[right] = keep;
    }
}

static boolean plainWindow(String s, int left, int right) {
    while (left < right) {
        if (s.charAt(left++) != s.charAt(right--)) return false;
    }
    return true;
}

static boolean almostPalindrome(String s) {
    int left = 0, right = s.length() - 1;
    while (left < right) {
        if (s.charAt(left) != s.charAt(right)) {
            return plainWindow(s, left + 1, right) || plainWindow(s, left, right - 1);
        }
        left++;
        right--;
    }
    return true;
}

static boolean appearsInOrder(String small, String large) {
    int matched = 0;
    for (int at = 0; at < large.length() && matched < small.length(); at++) {
        if (large.charAt(at) == small.charAt(matched)) matched++;
    }
    return matched == small.length();
}
```

Every method touches each position a constant number of times, so the walks cost O(n) time and O(1) extra memory, and the repair adds at most two more O(n) window checks after the single mismatch, so it is still O(n). The subsequence walk is O(n) in the length of the long text. The skip loop moves one pointer per iteration and never both, which keeps the comparison between two letters only.

<!-- stage: applicability -->
### Telling The Four Movements Apart

Whenever a text question asks whether something reads the same both ways, reverses, or becomes so after a bounded number of removals, the pointers start at the two ends, and each step finalizes one mirror pair. A text that must contain another in order is different: both pointers go forward, at unequal speeds. State the invariant before coding, and name which of the two motions the problem has, since the code looks similar but the proofs differ. Also decide whether noise characters are skipped, which characters count as noise, and whether capitals match.

The nearest false friend is using the opposite-end walk for the subsequence problem, because "check two things from both sides" sounds right. It compares the wrong characters, since the matching characters of a subsequence need not sit symmetrically. A second false friend is center expansion from the strings chapter: it finds the longest palindromic piece inside a text, while these walks test one given text from outside in. A third is the repair that tries deleting every character in turn, which is correct but O(n^2).

In Java, a `String` cannot be reversed in place, so convert once with `toCharArray` and work on that copy. `Character.isLetterOrDigit` also accepts letters outside ASCII, so a contract that promises only ASCII needs no extra test, and one that does not must say what counts. Compare lowercased characters, never the original ones, and never call `charAt` on an index the loop has not first checked against both ends.

<!-- stage: exercises -->
### Exercises

#### [Build] Valid Palindrome (LeetCode 125)
<!-- id: tp-clean-palindrome -->

**Prerequisites.** Opposite-end pointers from the first lesson of this chapter, and `Character.isLetterOrDigit` from the strings chapter.

**Problem.** Given a string `s`, decide whether it reads the same forwards and backwards after every character that is not a letter or a digit is ignored and capital letters are treated as lowercase. Build no cleaned copy: walk two pointers inward over `s` itself, and skip noise at each pointer before comparing.

**Constraints.** 0 <= s.length() <= 200000 and every character is printable ASCII. Use O(1) extra memory.

**Example 1.** Input `s = "Step on no pets!"`, output `true`.

**Example 2.** Input `s = " . , "`, output `true`.

**Hint.** Which pointer should move first when a character is noise? What does the loop condition guarantee about the two pointers at the moment of the comparison?

**Changed decision.** First rung: the comparison is on normalized characters, and the normalization is done in place by skipping at the pointers instead of by building a second string.

#### [Vary] Reverse String (LeetCode 344)
<!-- id: tp-reverse-chars -->

**Prerequisites.** The Build exercise above, and the difference between `String` and `char[]`.

**Problem.** Reverse the character array `chars` in place by swapping the two pointers' characters and moving both inward. Return nothing, make no second array, and report how many swaps were performed.

**Constraints.** 0 <= chars.length <= 100000 and any `char` values. The method returns the number of swaps.

**Example 1.** Input `chars = ['p', 'o', 'l', 'e', 's']`, output array `['s', 'e', 'l', 'o', 'p']` with 2 swaps.

**Example 2.** Input `chars = ['x']`, output array `['x']` with 0 swaps.

**Hint.** What condition stops the loop so that the middle character of an odd length is left alone? How many swaps does a length of ten need?

**Changed decision.** The pointers meet the same way, but the step is a swap instead of a comparison, and the contract is that the same array object ends up reversed.

#### [Boundary] Valid Palindrome II (LeetCode 680)
<!-- id: tp-palindrome-one-skip -->

**Prerequisites.** The two exercises above.

**Problem.** Given a string `s` of lowercase letters with no noise, decide whether it can become a palindrome by removing at most one character. Walk in from both ends, and at the first mismatch test exactly the two windows that skip the left character or the right one. Do not allow a second repair inside either window.

**Constraints.** 0 <= s.length() <= 100000 and every character is a lowercase letter a to z. Aim for at most about 3n character comparisons.

**Example 1.** Input `s = "abcxcbda"`, output `true`.

**Example 2.** Input `s = "abcdefa"`, output `false`.

**Hint.** Why can the removed character only be one of the two characters that just disagreed? What would go wrong if the helper window were allowed to repair again?

**Changed decision.** The pointers now meet one mismatch, and the invariant gets a budget of one repair, spent at the first disagreement and no later.

#### [Recognize] Is Subsequence (LeetCode 392)
<!-- id: tp-subsequence-rates -->

**Prerequisites.** The previous exercises, and the idea of a subsequence from Chapter 00.

**Problem.** Given strings `small` and `large`, decide whether `small` can be obtained from `large` by deleting some characters without changing the order of the rest. The pointers are not mirrored: one runs over `large` at every step and the other advances only when the characters are equal.

**Constraints.** 0 <= small.length() <= 5000, 0 <= large.length() <= 100000, lowercase letters only. The scan must stop as soon as `small` is fully matched.

**Example 1.** Input `small = "ace", large = "abcde"`, output `true`.

**Example 2.** Input `small = "aec", large = "abcde"`, output `false`.

**Hint.** Which pointer advances on every step? Why is taking the earliest match of each character never harmful?

**Changed decision.** Both pointers now move from left to right at different speeds, so the opposite-end invariant of the first three exercises does not apply.
