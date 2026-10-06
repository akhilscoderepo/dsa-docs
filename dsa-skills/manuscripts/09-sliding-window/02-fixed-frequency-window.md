<!-- lesson-kind: standard -->
<!-- lesson-id: fixed-frequency-window -->
## Match Counts In A Fixed Window

<!-- stage: context -->
### A Scanner That Misses Scrambled Tokens

A log scanner looks for a six-character token inside a long line of text. The token can appear in any letter order, so `listen` also counts when the line contains `silent`. The scanner sorts the six characters of each block and compares the sorted text with the sorted token. It works on short lines. On a log line of two million characters, it takes seconds for one search, and the service runs hundreds of searches per minute.

Last lesson solved a similar slowness for sums. A sum updates with two operations when the block moves by one index. This lesson asks whether a test of the form "same characters in any order" can update just as cheaply.

<!-- stage: naive -->
### Sort Every Block And Compare

The direct method builds the sorted form of the pattern once. For each start index, it copies the block of the same length, sorts the copy, and compares it with the sorted pattern.

```java
static List<Integer> startsBySorting(String s, String p) {
    List<Integer> out = new ArrayList<>();
    char[] want = p.toCharArray();
    Arrays.sort(want);
    for (int start = 0; start + p.length() <= s.length(); start++) {
        char[] block = s.substring(start, start + p.length()).toCharArray();
        Arrays.sort(block);
        if (Arrays.equals(block, want)) out.add(start);
    }
    return out;
}
```

The method is correct for any characters. Each iteration creates a new string and a new array, and then sorts the array.

<!-- stage: bottleneck -->
### Counting The Work Per Block

```predict
Take the block that starts at index 0 and the block that starts at index 1. One character enters the block and one character leaves it. How many entries in a table of character counts change?

At most two entries change. The leaving character's count drops by one, and the entering character's count rises by one. If both characters are equal, no entry changes at all.
```

Let `n` be the length of `s` and `k` the length of the pattern. The method visits `n - k + 1` starts. Each start copies `k` characters, and sorting them costs O(k log k). The total is O(n * k log k). For `n = 2,000,000` and `k = 1,000`, the sort alone performs about 20 billion comparisons.

The method also allocates one string and one array per start, so it produces millions of short-lived objects. The sorted form of a block is rebuilt from nothing each time, although neighbouring blocks differ by one character. The order of characters inside a block carries no information for this test, so the sort throws away work that was never needed.

<!-- stage: insight -->
### Count Each Character And Update Two Entries

#### The Count Array Replaces The Sorted Block

Two blocks hold the same characters in different orders exactly when every character occurs the same number of times in both. A **count array** stores one integer per possible character, and entry `c` holds the number of occurrences of `c`. For lowercase English letters, the array has 26 entries and the character `c` maps to index `c - 'a'`.

#### The Letter Counts Of The Window

The **letter counts** of a window are the count array that describes `s[left..right]`. The method keeps two arrays. One holds the letter counts of the pattern, and it never changes. The other holds the letter counts of the window, and it changes by at most two entries per slide.

#### One Equality Test Per Window

The **equality test** compares the two arrays entry by entry. It costs 26 comparisons, which is a constant for this alphabet. A window is a hit exactly when the two arrays are equal. The invariant is this: when the window has length `k`, the window array equals the letter counts of `s[left..right]`. Equal arrays then mean equal characters in any order. The total time is O(n), because each index enters and leaves once, and each full window costs one constant comparison.

<!-- names: count array, letter counts, equality test -->

<!-- stage: variables -->
### What The Scan Keeps

The scan keeps two arrays and the usual window indexes.

- **need** is the count array of the pattern `p`, and it never changes after it is built.
- **have** is the count array of the current window, and it describes `s[left..right]`.
- **k** is the pattern length, and every window has this length once `right >= k - 1`.
- **right** is the index of the entering character, and the leaving index is `right - k`.
- **out** holds the start index of every window whose counts equal `need`.

<!-- stage: trace -->
### Tracing Two Scans

#### Finding Scrambled Copies Of abc

Take `s = "bacdcab"` and the pattern `p = "abc"`, so `k = 3`. In the trace below, the pointers `left` and `right` mark the window, and the variable `equal` shows the result of the equality test. The window is incomplete for the first two steps, so no test is made. Starting at `right = 2`, each step adds the entering character and removes the leaving one, and then tests the arrays.

```trace
{"cells":["b","a","c","d","c","a","b"],"pointers":["left","right"],"steps":[{"at":{"left":0,"right":0},"vars":{},"note":"The character 'b' enters. The window is not full yet, so no test is made."},{"at":{"left":0,"right":1},"vars":{},"note":"The character 'a' enters. The window is not full yet, so no test is made."},{"at":{"left":0,"right":2},"vars":{"window":"bac","equal":"yes"},"note":"The character 'c' enters. The counts match, so the start 0 is recorded."},{"at":{"left":1,"right":3},"vars":{"window":"acd","equal":"no"},"note":"The character 'd' enters. The character 'b' leaves. The counts differ at 'b': the window holds 0 and the pattern needs 1."},{"at":{"left":2,"right":4},"vars":{"window":"cdc","equal":"no"},"note":"The character 'c' enters. The character 'a' leaves. The counts differ at 'a': the window holds 0 and the pattern needs 1."},{"at":{"left":3,"right":5},"vars":{"window":"dca","equal":"no"},"note":"The character 'a' enters. The character 'c' leaves. The counts differ at 'b': the window holds 0 and the pattern needs 1."},{"at":{"left":4,"right":6},"vars":{"window":"cab","equal":"yes"},"note":"The character 'b' enters. The character 'd' leaves. The counts match, so the start 4 is recorded."}]}
```

The windows `bac` and `cab` hit, and both start positions are recorded. The window `acd` fails, because the letter `d` has count 1 in `have` and count 0 in `need`.

#### A Pattern With A Repeated Letter

Take `s = "cabxaab"` and `p = "aab"`. The pattern needs the letter `a` twice. The first window `cab` contains one `a` and one `b`, and it also contains the letter `c`. A test that asks only whether each pattern letter occurs in the window would pass on windows such as `bxa`, which has one `a`. The count test fails there, because `have` holds 1 for `a` while `need` holds 2.

```trace
{"cells":["c","a","b","x","a","a","b"],"pointers":["left","right"],"steps":[{"at":{"left":0,"right":0},"vars":{},"note":"The character 'c' enters. The window is not full yet, so no test is made."},{"at":{"left":0,"right":1},"vars":{},"note":"The character 'a' enters. The window is not full yet, so no test is made."},{"at":{"left":0,"right":2},"vars":{"window":"cab","equal":"no"},"note":"The character 'b' enters. The counts differ at 'a': the window holds 1 and the pattern needs 2."},{"at":{"left":1,"right":3},"vars":{"window":"abx","equal":"no"},"note":"The character 'x' enters. The character 'c' leaves. The counts differ at 'a': the window holds 1 and the pattern needs 2."},{"at":{"left":2,"right":4},"vars":{"window":"bxa","equal":"no"},"note":"The character 'a' enters. The character 'a' leaves. The counts differ at 'a': the window holds 1 and the pattern needs 2."},{"at":{"left":3,"right":5},"vars":{"window":"xaa","equal":"no"},"note":"The character 'a' enters. The character 'b' leaves. The counts differ at 'b': the window holds 0 and the pattern needs 1."},{"at":{"left":4,"right":6},"vars":{"window":"aab","equal":"yes"},"note":"The character 'b' enters. The character 'x' leaves. The counts match, so the start 4 is recorded."}]}
```

Only the final window, `aab` at start 4, has equal counts.

<!-- stage: code -->
### Matching Counts In Java

#### The Scan With Two Count Arrays

```java
static List<Integer> anagramStarts(String s, String p) {
    List<Integer> out = new ArrayList<>();
    int k = p.length();
    if (k > s.length()) return out;
    int[] need = new int[26], have = new int[26];
    for (int i = 0; i < k; i++) need[p.charAt(i) - 'a']++;
    for (int right = 0; right < s.length(); right++) {
        have[s.charAt(right) - 'a']++;
        if (right >= k) have[s.charAt(right - k) - 'a']--;
        if (right >= k - 1 && Arrays.equals(have, need)) out.add(right - k + 1);
    }
    return out;
}
```

The method creates no substring and sorts nothing. The leaving character is `s.charAt(right - k)`, which is removed before the test, so the window has length `k` when the arrays are compared.

#### Cost And Alphabet Size

The time is O(n * 26), which is O(n) when the alphabet size is a constant. The extra memory is two arrays of 26 integers, which is O(1). If the alphabet changes, the cost of one test is the alphabet size, and the array size changes with it.

<!-- stage: applicability -->
### When The Count Test Applies

#### Spotting A Fixed Window With Counts

Look for a request about blocks of one fixed length where validity depends on which characters occur and how many times, not on a sum. The words "permutation of", "anagram of" and "same letters in any order" signal this lesson. Each block still has a fixed length, so the window slides exactly as in the sum lesson.

#### The Invariant To State

State what each array entry means before writing the loop. The window array holds the counts of `s[left..right]`, and it describes a full window only when `right - left + 1 == k`. Testing before the window is full gives hits on blocks that are too short.

#### Sorting Every Window Is A False Friend

Sorting each block is correct and tempting, because sorted blocks compare with one call. It destroys the linear time, as the bottleneck showed. Comparing sets is a second false friend. A set records which characters occur, and it cannot record that `a` must occur twice.

#### The Java Hazard Of Small Arrays

A count array of size 26 works only when the contract promises lowercase English letters. A string with an uppercase letter or a digit makes `c - 'a'` negative or too large, and the code throws `ArrayIndexOutOfBoundsException`. For a wider alphabet, use an array of size 128 or 256 for ASCII or Latin-1, or use a `HashMap` for any character.

<!-- stage: exercises -->
### Exercises

#### [Build] Binary Window Counts (Author exercise)
<!-- id: sw-binary-counts -->

**Prerequisites.** The count array and the sum lesson.

**Problem.** Given a binary array `bits` and an integer `k`, return an array `out` of length `bits.length - k + 1`. For each start `i`, `out[i]` is the number of values equal to 1 in `bits[i..i + k - 1]`. Maintain a count array of size 2 and update it by the entering and the leaving value.

**Constraints.**
- **Length** satisfies `1 <= bits.length <= 10^5`.
- **Window size** satisfies `1 <= k <= bits.length`.
- **Values** are 0 or 1.
- **Return** type is `int[]`.
- **Mutation** does not occur; `bits` is unchanged.

**Example 1.** Input `bits = [1,0,1,1,0]`, `k = 3`. Output `[2,2,2]`.

**Example 2.** Input `bits = [0,0,0]`, `k = 3`. Output `[0]`.

**Hint.** Which entry of the count array changes when a 0 leaves? Which entry is the answer?

**Changed decision.** The state is a count array with two entries, in place of one sum.

#### [Vary] Find All Anagrams In A String (LeetCode 438)
<!-- id: sw-find-anagrams -->

**Prerequisites.** The binary counts exercise above.

**Problem.** Given strings `s` and `p`, return the start index of every substring of `s` that is an anagram of `p`. A string is an anagram of `p` when it has the same length as `p` and each character occurs the same number of times in both. Return the indexes in increasing order.

**Constraints.**
- **Lengths** satisfy `1 <= s.length, p.length <= 3 * 10^4`.
- **Characters** are lowercase English letters.
- **Return** type is a list of `Integer`, empty when no substring matches.
- **Mutation** does not occur; the strings are immutable.

**Example 1.** Input `s = "bacdcab"`, `p = "abc"`. Output `[0,4]`.

**Example 2.** Input `s = "ab"`, `p = "abc"`. Output `[]`, because the pattern is longer than the text.

**Hint.** When does the first full window end? What happens if the pattern is longer than `s`?

**Changed decision.** The method records every matching start, and it does not stop at the first.

#### [Boundary] Repeated Required Character (Author exercise)
<!-- id: sw-repeated-required -->

**Prerequisites.** The anagram exercise above.

**Problem.** Given strings `s` and `p`, return the smallest start index of a substring of `s` that has the same length as `p` and the same character counts as `p`. Return -1 if no such substring exists. A substring that contains each character of `p` at least once does not qualify when a count is too low.

**Constraints.**
- **Lengths** satisfy `1 <= s.length, p.length <= 10^5`.
- **Characters** are lowercase English letters.
- **Return** type is `int`.
- **Mutation** does not occur; the strings are immutable.

**Example 1.** Input `s = "cabxaab"`, `p = "aab"`. Output `4`.

**Example 2.** Input `s = "abcb"`, `p = "aab"`. Output `-1`.

**Hint.** What does the window array hold for `a` in the window `abc`, and what does the pattern array hold?

**Changed decision.** The test compares counts, and a plain test of membership would accept windows that lack a second copy.

#### [Recognize] Permutation In String (LeetCode 567)
<!-- id: sw-permutation-in-string -->

**Prerequisites.** All three exercises above.

**Problem.** Given strings `p` and `s`, return `true` if some substring of `s` is a permutation of `p`. A permutation of `p` has the same length as `p` and the same count of every character. The method may use the full equality test of two count arrays for each window.

**Constraints.**
- **Lengths** satisfy `1 <= p.length, s.length <= 10^4`.
- **Characters** are lowercase English letters.
- **Return** type is `boolean`.
- **Mutation** does not occur; the strings are immutable.

**Example 1.** Input `p = "ab"`, `s = "xbax"`. Output `true`, from the substring `ba`.

**Example 2.** Input `p = "aab"`, `s = "abba"`. Output `false`.

**Hint.** Which earlier exercise returns every start? How does a boolean answer change the end of the loop?

**Changed decision.** The method returns at the first hit, in place of collecting all starts.
