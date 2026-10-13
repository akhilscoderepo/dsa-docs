<!-- lesson-kind: standard -->
<!-- lesson-id: palindromic-sequences -->
## Palindromic Sequences

<!-- stage: context -->
### Scoring How Symmetric A String Is

A text tool scores how close a string is to reading the same in both directions. Its first version finds the longest palindromic substring, which is a block of adjacent characters that reads the same backward. For `bbbab` that block is `bbb`, so the tool reports 3. A reviewer points out that the characters at positions 0, 1, 2 and 4 spell `bbbb`, which is symmetric and has length 4. The tool undercounts because it requires the kept characters to touch each other.

A subsequence keeps characters in their original order but may skip any of them. A palindromic subsequence is a subsequence that reads the same forward and backward.

Formally, the input is a string `s` of lowercase letters, possibly empty. The task is to return the length of the longest palindromic subsequence of `s`. The method does not change `s`.

This lesson asks how a table can decide which characters to keep and which to skip.

<!-- stage: naive -->
### Trying Every Keep Or Skip Choice

The direct idea compares the first and last character and recurses on what remains. If the two characters match, both belong to the answer. If they differ, at least one of them must be skipped, and the code tries both.

```java
static int slow(String s, int left, int right) {
    if (left > right) return 0;
    if (left == right) return 1;
    if (s.charAt(left) == s.charAt(right)) {
        return 2 + slow(s, left + 1, right - 1);
    }
    return Math.max(slow(s, left + 1, right), slow(s, left, right - 1));
}
```

The answer for the whole string is `slow(s, 0, s.length() - 1)`. The code is correct, because every subsequence either uses the first character, uses the last one, or uses neither. The open question is how many calls it makes.

```predict
How many calls does slow make for the string "abcd", where no two characters match, counting the first call?

It makes 15 calls. A call on a range of m characters makes two calls on ranges of m - 1 characters, so the count for length m is twice the count for length m - 1, plus one. The counts are 1, 3, 7 and 15 for lengths 1 to 4.
```

<!-- stage: bottleneck -->
### The Same Ranges Appear Again And Again

When no characters match, each call on m characters makes two calls on m - 1 characters, so a string of n characters causes 2^n - 1 calls. The running time is O(2^n). A string of 40 characters needs more than 10^12 calls, which is far too slow.

The calls are not all different. The call `slow(s, 1, 3)` appears under both `slow(s, 0, 3)` and `slow(s, 1, 4)`. Each call is fully described by the pair `left` and `right`, and a string of n characters has only n * (n + 1) / 2 such pairs. The same pair is solved over and over, and each solve reads only two smaller pairs.

Storing the answer for each pair once cuts the work to O(n^2) pairs with O(1) work each. The question is in which order to fill the pairs, because a pair can be computed only after the smaller pairs it reads.

<!-- stage: insight -->
### One Table Entry For Each Range

Treat the range `left..right` as the state. Every call of the recursion depends on nothing else, so one stored number per range replaces the repeated calls.

<!-- names: closed interval, equal endpoints, increasing length -->

#### What One Entry Stores

A **closed interval** `[left, right]` contains the characters at positions `left` to `right`, including both ends. Let `dp[left][right]` be the length of the longest palindromic subsequence inside that closed interval. An interval with one character has `dp[left][left] = 1`. An empty range contributes 0.

#### Two Cases For Each Interval

Look at the characters `s[left]` and `s[right]`. When they are **equal endpoints**, some best subsequence uses both. Keeping both adds 2 to the best subsequence strictly inside, so `dp[left][right] = dp[left + 1][right - 1] + 2`. When `left + 1 > right - 1`, the inside is empty and its value is 0.

When the endpoints differ, no palindrome can use both of them as its outer pair. At least one endpoint is skipped, so `dp[left][right]` is the larger of `dp[left + 1][right]` and `dp[left][right - 1]`. Skipping an endpoint that a best subsequence does not use loses nothing, which is why trying both skips is enough.

#### Filling In Order Of Length

Every entry reads only intervals that are strictly shorter. The table is therefore filled by **increasing length**, from length 1 up to `n`, and by increasing `left` inside one length. The invariant is that when an interval of length L is computed, every interval of length less than L is already final. The answer is `dp[0][n - 1]`, or 0 for the empty string.

<!-- stage: variables -->
### The Table And The Two Ends

The method leaves `s` alone and keeps these working values.

- **dp** is an `int[n][n]`; entry `[left][right]` is the longest palindromic subsequence inside that interval, and entries with `left > right` stay 0.
- **length** is the number of characters in the interval that the outer loop fills, from 1 to `n`.
- **left** is the first position of the interval, from 0 to `n - length`.
- **right** is the last position, equal to `left + length - 1`.
- **inner** is `dp[left + 1][right - 1]`, which is 0 when the interval has length 2.

The cell `dp[left + 1][right - 1]` is read only when the endpoints match. For length 2 that index pair has `left + 1 > right - 1`, so the code reads it as 0 without touching the array.

<!-- stage: trace -->
### Two Strings Filled By Length

#### A Run With Many Matching Letters

The first run uses `bbbab`. The cells are the five characters. The pointers `left` and `right` mark the ends of the interval in progress, and the variable `length` is their span. The variable `inner` is the value strictly inside, `skip` is the better of the two skip cases, and `dp` is the stored entry.

The five intervals of length 1 each store 1. At length 2 the pairs `bb` match and store 2, while `ba` and `ab` differ and store 1. At length 3 the interval `bbb` has equal endpoints and an inner value of 1, so it stores 3. The final interval `0..4` has endpoints `b` and `b`, and the inner interval `1..3` holds 2, so the answer is 2 + 2, which is 4.

```trace
{"cells":["b","b","b","a","b"],"pointers":["left","right"],"steps":[{"at":{"left":0,"right":0},"vars":{"length":1,"inner":0,"skip":0,"dp":1},"note":"Length 1, interval 0..0. A single character is a palindrome, so the entry is 1."},{"at":{"left":1,"right":1},"vars":{"length":1,"inner":0,"skip":0,"dp":1},"note":"Length 1, interval 1..1. A single character is a palindrome, so the entry is 1."},{"at":{"left":2,"right":2},"vars":{"length":1,"inner":0,"skip":0,"dp":1},"note":"Length 1, interval 2..2. A single character is a palindrome, so the entry is 1."},{"at":{"left":3,"right":3},"vars":{"length":1,"inner":0,"skip":0,"dp":1},"note":"Length 1, interval 3..3. A single character is a palindrome, so the entry is 1."},{"at":{"left":4,"right":4},"vars":{"length":1,"inner":0,"skip":0,"dp":1},"note":"Length 1, interval 4..4. A single character is a palindrome, so the entry is 1."},{"at":{"left":0,"right":1},"vars":{"length":2,"inner":0,"skip":1,"dp":2},"note":"Length 2, interval 0..1. The endpoints b and b match, the inner value is 0, so the entry is 0+2=2."},{"at":{"left":1,"right":2},"vars":{"length":2,"inner":0,"skip":1,"dp":2},"note":"Length 2, interval 1..2. The endpoints b and b match, the inner value is 0, so the entry is 0+2=2."},{"at":{"left":2,"right":3},"vars":{"length":2,"inner":0,"skip":1,"dp":1},"note":"Length 2, interval 2..3. The endpoints b and a differ. Skipping the left end gives 1, skipping the right end gives 1, so the entry is 1."},{"at":{"left":3,"right":4},"vars":{"length":2,"inner":0,"skip":1,"dp":1},"note":"Length 2, interval 3..4. The endpoints a and b differ. Skipping the left end gives 1, skipping the right end gives 1, so the entry is 1."},{"at":{"left":0,"right":2},"vars":{"length":3,"inner":1,"skip":2,"dp":3},"note":"Length 3, interval 0..2. The endpoints b and b match, the inner value is 1, so the entry is 1+2=3."},{"at":{"left":1,"right":3},"vars":{"length":3,"inner":1,"skip":2,"dp":2},"note":"Length 3, interval 1..3. The endpoints b and a differ. Skipping the left end gives 1, skipping the right end gives 2, so the entry is 2."},{"at":{"left":2,"right":4},"vars":{"length":3,"inner":1,"skip":1,"dp":3},"note":"Length 3, interval 2..4. The endpoints b and b match, the inner value is 1, so the entry is 1+2=3."},{"at":{"left":0,"right":3},"vars":{"length":4,"inner":2,"skip":3,"dp":3},"note":"Length 4, interval 0..3. The endpoints b and a differ. Skipping the left end gives 2, skipping the right end gives 3, so the entry is 3."},{"at":{"left":1,"right":4},"vars":{"length":4,"inner":1,"skip":3,"dp":3},"note":"Length 4, interval 1..4. The endpoints b and b match, the inner value is 1, so the entry is 1+2=3."},{"at":{"left":0,"right":4},"vars":{"length":5,"inner":2,"skip":3,"dp":4},"note":"Length 5, interval 0..4. The endpoints b and b match, the inner value is 2, so the entry is 2+2=4."}]}
```

#### A Run With Few Matches

The second run uses `abcda`, where only the first and last characters match. Every shorter interval has distinct endpoints, so each entry copies the larger neighbor. The interval `0..4` has equal endpoints, and its inner interval `1..3` holds 1, so it stores 3. This is the only place in the run where the table adds 2.

```trace
{"cells":["a","b","c","d","a"],"pointers":["left","right"],"steps":[{"at":{"left":0,"right":0},"vars":{"length":1,"inner":0,"skip":0,"dp":1},"note":"Length 1, interval 0..0. A single character is a palindrome, so the entry is 1."},{"at":{"left":1,"right":1},"vars":{"length":1,"inner":0,"skip":0,"dp":1},"note":"Length 1, interval 1..1. A single character is a palindrome, so the entry is 1."},{"at":{"left":2,"right":2},"vars":{"length":1,"inner":0,"skip":0,"dp":1},"note":"Length 1, interval 2..2. A single character is a palindrome, so the entry is 1."},{"at":{"left":3,"right":3},"vars":{"length":1,"inner":0,"skip":0,"dp":1},"note":"Length 1, interval 3..3. A single character is a palindrome, so the entry is 1."},{"at":{"left":4,"right":4},"vars":{"length":1,"inner":0,"skip":0,"dp":1},"note":"Length 1, interval 4..4. A single character is a palindrome, so the entry is 1."},{"at":{"left":0,"right":1},"vars":{"length":2,"inner":0,"skip":1,"dp":1},"note":"Length 2, interval 0..1. The endpoints a and b differ. Skipping the left end gives 1, skipping the right end gives 1, so the entry is 1."},{"at":{"left":1,"right":2},"vars":{"length":2,"inner":0,"skip":1,"dp":1},"note":"Length 2, interval 1..2. The endpoints b and c differ. Skipping the left end gives 1, skipping the right end gives 1, so the entry is 1."},{"at":{"left":2,"right":3},"vars":{"length":2,"inner":0,"skip":1,"dp":1},"note":"Length 2, interval 2..3. The endpoints c and d differ. Skipping the left end gives 1, skipping the right end gives 1, so the entry is 1."},{"at":{"left":3,"right":4},"vars":{"length":2,"inner":0,"skip":1,"dp":1},"note":"Length 2, interval 3..4. The endpoints d and a differ. Skipping the left end gives 1, skipping the right end gives 1, so the entry is 1."},{"at":{"left":0,"right":2},"vars":{"length":3,"inner":1,"skip":1,"dp":1},"note":"Length 3, interval 0..2. The endpoints a and c differ. Skipping the left end gives 1, skipping the right end gives 1, so the entry is 1."},{"at":{"left":1,"right":3},"vars":{"length":3,"inner":1,"skip":1,"dp":1},"note":"Length 3, interval 1..3. The endpoints b and d differ. Skipping the left end gives 1, skipping the right end gives 1, so the entry is 1."},{"at":{"left":2,"right":4},"vars":{"length":3,"inner":1,"skip":1,"dp":1},"note":"Length 3, interval 2..4. The endpoints c and a differ. Skipping the left end gives 1, skipping the right end gives 1, so the entry is 1."},{"at":{"left":0,"right":3},"vars":{"length":4,"inner":1,"skip":1,"dp":1},"note":"Length 4, interval 0..3. The endpoints a and d differ. Skipping the left end gives 1, skipping the right end gives 1, so the entry is 1."},{"at":{"left":1,"right":4},"vars":{"length":4,"inner":1,"skip":1,"dp":1},"note":"Length 4, interval 1..4. The endpoints b and a differ. Skipping the left end gives 1, skipping the right end gives 1, so the entry is 1."},{"at":{"left":0,"right":4},"vars":{"length":5,"inner":1,"skip":1,"dp":3},"note":"Length 5, interval 0..4. The endpoints a and a match, the inner value is 1, so the entry is 1+2=3."}]}
```

<!-- stage: code -->
### Filling The Table By Length

The method returns the length of the longest palindromic subsequence. It fills intervals from short to long.

```java
static int longestPalindromicSubsequence(String s) {
    int n = s.length();
    int[][] dp = new int[n][n];
    for (int length = 1; length <= n; length++) {
        for (int left = 0; left + length - 1 < n; left++) {
            int right = left + length - 1;
            if (length == 1) {
                dp[left][right] = 1;
            } else if (s.charAt(left) == s.charAt(right)) {
                int inner = length == 2 ? 0 : dp[left + 1][right - 1];
                dp[left][right] = inner + 2;
            } else {
                dp[left][right] = Math.max(dp[left + 1][right], dp[left][right - 1]);
            }
        }
    }
    return n == 0 ? 0 : dp[0][n - 1];
}
```

The cost is O(n^2) time for the pairs and O(n^2) memory for the table. The empty string never enters the loops, so the final line returns 0 for it. The first exercise below fills only the entries of length 1 and 2.

<!-- stage: applicability -->
### Recognizing Skippable Characters In A Range

#### Reading The Cue

Use this method when the state is a range of the input, the chosen characters keep their order, and some characters may be skipped. Words such as "subsequence", "delete characters" and "insert characters to make symmetric" point here. The table indexes two ends, and each entry depends on shorter ranges.

#### Checking The Invariant

The invariant says that every shorter interval is final before a longer one is read. Test a string of length 1, a string of length 2 with equal characters, and a string of length 2 with different characters, because those cases exercise the rule for empty inner ranges. Test a string of one repeated letter, where the answer equals the length.

#### Avoiding The False Friend

The first false friend is the longest palindromic substring, which requires adjacent characters and returns 3 for `bbbab`. The second is a loop over `left` from small to large with `right` from `left` to `n - 1`, which reads `dp[left + 1][right]` before it exists. The third is a greedy rule that drops a mismatched endpoint without trying the other one. Do not use this table when the input needs more than a few thousand characters, since O(n^2) memory then dominates.

<!-- stage: exercises -->
### Exercises

#### [Build] Length One And Two (Author exercise)
<!-- id: ps-length-one-and-two -->

**Prerequisites.** The interval definition and the two cases from this lesson.

**Problem.** Given a string `s` of length `n`, return an `int[n][n]` table. Entry `[left][right]` holds the length of the longest palindromic subsequence inside the interval from `left` to `right` when `right - left + 1` is 1 or 2. Every other entry is 0.

**Constraints.** The limits are:
- **Length** satisfies `0 <= s.length() <= 1000`.
- **Characters** are lowercase English letters.
- **Result** is a new array, and an empty string returns an empty array.
- **Mutation** is not allowed, because `s` is immutable.

**Example 1.** Input `s = "aab"`, output `[[1,2,0],[0,1,1],[0,0,1]]`.

**Example 2.** Input `s = "z"`, output `[[1]]`.

**Hint.** An interval of two characters stores 2 when its characters match. What does it store when they differ, and which two single-character entries explain that value?

**Changed decision.** The method stops after length 2 and never reads an inner interval. These entries are the base cases that every longer interval relies on.

#### [Vary] Longest Palindromic Subsequence (LeetCode 516)
<!-- id: ps-longest-palindromic-subsequence -->

**Prerequisites.** The exercise above.

**Problem.** Given a string `s`, return the length of its longest palindromic subsequence. A subsequence keeps the original order and may skip any characters.

**Constraints.** The limits are:
- **Length** satisfies `1 <= s.length() <= 1000`.
- **Characters** are lowercase English letters.
- **Result** is an `int`.
- **Mutation** is not allowed, because `s` is immutable.

**Example 1.** Input `s = "bbbab"`, output `4`.

**Example 2.** Input `s = "cbbd"`, output `2`.

**Hint.** When the endpoints match, which inner interval gives the rest? When they differ, which two intervals does the larger value come from?

**Changed decision.** Equal endpoints add 2 to the inner interval, and different endpoints skip one endpoint. The two cases replace the keep-or-skip choice of the capacity tables.

#### [Boundary] Fill By Increasing Length (Author exercise)
<!-- id: ps-fill-by-increasing-length -->

**Prerequisites.** The two exercises above.

**Problem.** A string of length `n` has intervals `(left, right)` with `0 <= left <= right < n`. List them by increasing length, and by increasing `left` among equal lengths. Given `n`, `left` and `right`, return the zero-based position of that interval in the list.

**Constraints.** The limits are:
- **Length** satisfies `1 <= n <= 1000`.
- **Interval** satisfies `0 <= left <= right < n`.
- **Result** is an `int`, and the first interval has position 0.
- **Mutation** is not allowed, because the inputs are plain integers.

**Example 1.** Input `n = 5`, `left = 1`, `right = 2`, output `6`.

**Example 2.** Input `n = 5`, `left = 0`, `right = 4`, output `14`.

**Hint.** How many intervals of each shorter length come before the first interval of the target length?

**Changed decision.** The method counts positions in the fill order. In that order, every interval that an entry reads has a smaller position, so inner intervals are always ready first.

#### [Recognize] Minimum Insertion Steps To Make A String Palindrome (LeetCode 1312)
<!-- id: ps-minimum-insertions-palindrome -->

**Prerequisites.** All three exercises above.

**Problem.** Given a string `s`, an insertion adds one character at any position. Return the smallest number of insertions that turns `s` into a palindrome.

**Constraints.** The limits are:
- **Length** satisfies `1 <= s.length() <= 500`.
- **Characters** are lowercase English letters.
- **Result** is an `int`.
- **Mutation** is not allowed, because `s` is immutable.

**Example 1.** Input `s = "zzazz"`, output `0`.

**Example 2.** Input `s = "mbadm"`, output `2`.

**Hint.** Characters that stay in place form a subsequence. Which subsequence must be a palindrome, and how many characters remain without a partner?

**Changed decision.** The answer is `n` minus the longest palindromic subsequence, so the lesson table supplies the number. Each character outside that subsequence needs one inserted partner.
