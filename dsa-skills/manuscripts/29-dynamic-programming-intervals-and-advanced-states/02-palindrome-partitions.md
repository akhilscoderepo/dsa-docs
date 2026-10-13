<!-- lesson-kind: standard -->
<!-- lesson-id: palindrome-partitions -->
## Palindrome Partitions

<!-- stage: context -->
### Splitting A String Into Mirror Segments

A text-analysis tool reports how a string decomposes into segments that read the same forward and backward. The product rule says to report the fewest segments. For the input `aaba`, the best report has 2 segments, `a` and `aba`. The tool needs one cut between them.

A developer writes a quick rule. It repeatedly removes the longest segment at the front that reads the same in both directions. On `aaba` it removes `aa`, then `b`, then `a`. The rule reports 3 segments, one more than the best answer, because `aa` hides the longer segment `aba` that starts one character later.

Formally, the input is a string `s`. A **palindrome** is a string equal to its own reverse. A **partition** splits `s` into consecutive pieces, and every piece must be a palindrome. A **cut** is a boundary between two neighbouring pieces, so a partition with p pieces uses p - 1 cuts. The task is to return the fewest cuts over all partitions. The string never changes.

This lesson asks how to find that count when the choice at the front of the string changes what remains possible.

<!-- stage: naive -->
### Trying Every Set Of Cuts

The safe idea is to try every way to place cuts. A string of length n has n - 1 gaps between characters, and each gap either holds a cut or does not. The method below reads each subset of gaps from the bits of a number, checks every resulting piece, and keeps the smallest valid count.

```java
static int bruteCuts(String s) {
    int n = s.length();
    if (n == 0) return 0;
    int best = n - 1;
    for (int mask = 0; mask < (1 << (n - 1)); mask++) {
        int start = 0;
        int cuts = 0;
        boolean valid = true;
        for (int k = 0; k < n && valid; k++) {
            boolean pieceEnds = k == n - 1 || ((mask >> k) & 1) == 1;
            if (!pieceEnds) continue;
            int lo = start;
            int hi = k;
            while (lo < hi && s.charAt(lo) == s.charAt(hi)) { lo++; hi--; }
            if (lo < hi) valid = false;
            start = k + 1;
            if (k < n - 1) cuts++;
        }
        if (valid) best = Math.min(best, cuts);
    }
    return best;
}
```

There are 2^(n - 1) masks, and each one costs O(n) time to check its pieces. The total is O(2^n * n) time with O(1) extra memory. The method always returns the right answer, but the time doubles with every added character.

```predict
A string has 30 characters. How many different sets of cuts does the method above examine?

It examines 2^29, which is 536,870,912 sets. Each set also needs a scan of the whole string, so the work reaches about 1.6 * 10^10 character comparisons.
```

<!-- stage: bottleneck -->
### The Same Work Repeats Many Times

The method is slow because it repeats two kinds of work. Both repeats come from decisions that do not depend on each other.

#### Checking The Same Substring Again

Take the substring `s[2..5]`. Every mask that places cuts exactly before index 2 and after index 5 re-reads those four characters and decides again whether they form a palindrome. That count grows as 2^(n - 5) for a fixed substring. A string of length n has only n * (n + 1) / 2 substrings, so the same few answers are recomputed an enormous number of times. Checking each substring once costs O(n) per substring and O(n^3) in total, and a better order brings that down to O(n^2).

#### Solving The Same Remaining Text Again

Two different sets of cuts can agree on the first end characters of the string. Both then face the same question about the remaining text, and the method answers it from scratch each time. The number of distinct prefixes is only n + 1. If the best piece count for each prefix is stored, each prefix needs one pass over its possible starting points, which costs O(n) per prefix and O(n^2) in total.

The next section removes both repeats. It stores palindrome answers in a table and stores best piece counts for prefixes in an array.

<!-- stage: insight -->
### Store Palindromes, Then Count Pieces

Two small tables replace the search over cuts. The first table answers "is this substring a palindrome" in constant time. The second table uses the first one to count pieces for every prefix.

<!-- names: palindrome table, inner interval, last piece -->

#### One Entry For Each Substring

The **palindrome table** is a boolean array `pal[i][j]` for `0 <= i <= j < n`. Entry `pal[i][j]` is true exactly when `s[i..j]` is a palindrome. A single character is always a palindrome, so every entry with `i == j` is true.

#### Equal Ends Depend On The Inner Interval

A substring with `i < j` is a palindrome when its two end characters are equal and the characters between them also form a palindrome. The characters between them are the **inner interval** `s[i + 1..j - 1]`. If the two ends are equal and the inner interval is empty, as for `aa`, the substring is a palindrome. If the inner interval holds one or more characters, the entry equals `pal[i + 1][j - 1]`. That entry has a larger `i` and a smaller `j`, so the loop must visit `i` from the end of the string down to 0 and `j` from `i` upward. Then the inner interval is final before the outer entry reads it.

#### Count Pieces For Each Prefix

Let `pieces[end]` be the fewest pieces in a partition of the first `end` characters. The empty prefix needs 0 pieces, so `pieces[0] = 0`. Consider any partition of the prefix and look at its **last piece**, which is `s[start..end - 1]` for some `start` from 0 to `end - 1`. The last piece must be a palindrome, and the characters before it form a partition of the shorter prefix of length `start`. The best choice is therefore `pieces[start] + 1`, minimized over every `start` with `pal[start][end - 1]` true.

#### Convert Pieces To Cuts

The answer for the whole string is `pieces[n] - 1`, because p pieces use p - 1 cuts. The invariant is that `pieces[start]` is final before `pieces[end]` reads it, since `start < end`, and that every entry of `pal` read here is final after the first loop. An empty string has no pieces and no cuts, so the method returns 0 for it in place of the value -1.

<!-- stage: variables -->
### Two Tables And Their Indexes

The string comes in unchanged, and these working values describe both tables.

- **pal** is a `boolean[n][n]`; entry `pal[i][j]` is true when `s[i..j]`, both ends included, is a palindrome.
- **pieces** is an `int[n + 1]`; entry `pieces[end]` is the fewest palindromic pieces that cover the first `end` characters.
- **i** and **j** are the first and last index of a substring while the palindrome table is filled.
- **start** is the first index of the last piece, so the piece is `s[start..end - 1]`.
- **end** is the prefix length, from 1 to n, and `end - 1` is the index of the last character of the prefix.

Java fills a new `boolean` array with `false`, so entries that the loop never sets stay false. The loop sets `pal[i][j]` only for `i <= j`. The second loop reads `pal[start][end - 1]` with `start <= end - 1`, which stays inside the filled part.

<!-- stage: trace -->
### Two Runs Of The Method

#### Filling The Palindrome Table

The first run uses `s = "aaba"` from the opening. The table has 4 rows and 4 columns, and the cells below list them row by row, so cell 0 to 3 is row 0, cell 4 to 7 is row 1, and so on. The pointer `cell` marks the entry in progress, and only the entries with `i <= j` are visited. The variable `ends` says whether the two end characters match, `inner` shows the entry for the inner interval, and `pal` is the value written.

Row 3 and row 2 hold single characters and the pair `ba`. Row 1 is the useful one. The pair `aa` has equal ends and an empty inner interval, so it is true. The substring `aba` has equal ends, and its inner interval is the single character `b`, which is true, so `aba` is true. Row 0 then finds that `aaba` has equal ends, but its inner interval `ab` is false, so the whole string is not a palindrome. The table holds 6 true entries.

```trace
{"cells":[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15],"pointers":["cell"],"steps":[{"at":{"cell":15},"vars":{"i":3,"j":3,"ends":"match","inner":"empty","pal":1},"note":"Substring 'a' spans indexes 3 to 3. The end characters 'a' and 'a' match and nothing lies between them, so the entry is true."},{"at":{"cell":10},"vars":{"i":2,"j":2,"ends":"match","inner":"empty","pal":1},"note":"Substring 'b' spans indexes 2 to 2. The end characters 'b' and 'b' match and nothing lies between them, so the entry is true."},{"at":{"cell":11},"vars":{"i":2,"j":3,"ends":"differ","inner":"empty","pal":0},"note":"Substring 'ba' spans indexes 2 to 3. The end characters 'b' and 'a' differ, so the entry is false."},{"at":{"cell":5},"vars":{"i":1,"j":1,"ends":"match","inner":"empty","pal":1},"note":"Substring 'a' spans indexes 1 to 1. The end characters 'a' and 'a' match and nothing lies between them, so the entry is true."},{"at":{"cell":6},"vars":{"i":1,"j":2,"ends":"differ","inner":"empty","pal":0},"note":"Substring 'ab' spans indexes 1 to 2. The end characters 'a' and 'b' differ, so the entry is false."},{"at":{"cell":7},"vars":{"i":1,"j":3,"ends":"match","inner":"true","pal":1},"note":"Substring 'aba' spans indexes 1 to 3. The end characters match and the inner interval 2 to 2 is true, so the entry is true."},{"at":{"cell":0},"vars":{"i":0,"j":0,"ends":"match","inner":"empty","pal":1},"note":"Substring 'a' spans indexes 0 to 0. The end characters 'a' and 'a' match and nothing lies between them, so the entry is true."},{"at":{"cell":1},"vars":{"i":0,"j":1,"ends":"match","inner":"empty","pal":1},"note":"Substring 'aa' spans indexes 0 to 1. The end characters 'a' and 'a' match and nothing lies between them, so the entry is true."},{"at":{"cell":2},"vars":{"i":0,"j":2,"ends":"differ","inner":"true","pal":0},"note":"Substring 'aab' spans indexes 0 to 2. The end characters 'a' and 'b' differ, so the entry is false."},{"at":{"cell":3},"vars":{"i":0,"j":3,"ends":"match","inner":"false","pal":0},"note":"Substring 'aaba' spans indexes 0 to 3. The end characters match, but the inner interval 1 to 2 is false, so the entry is false."}]}
```

#### Counting Pieces For Each Prefix

The second run reads the table from the first run and fills `pieces` for the same string. Two pointers mark the characters. The pointer `start` marks the first character of the candidate last piece, and the pointer `end` marks the last character of the prefix. Each step tests one candidate piece. A palindromic piece proposes `pieces[start] + 1`, and the array keeps the smaller value.

Prefix length 2 shows the choice. The piece `aa` starts at 0 and gives 1 piece. The piece `a` starts at 1 and would give 2, so the array keeps 1. Prefix length 4 tests `aaba`, `aba`, `ba` and `a`. The piece `aba` starts at 1, where `pieces[1]` is 1, so it gives 2. The piece `a` gives 3, which loses. The final value is 2 pieces, so the method returns 1 cut.

```trace
{"cells":["a","a","b","a"],"pointers":["start","end"],"steps":[{"at":{"start":0,"end":0},"vars":{"end":1,"start":0,"piece":"a","pal":1,"pieces":"[0, 1, -, -, -]"},"note":"Prefix length 1, last piece starts at 0. The piece 'a' is a palindrome, so pieces[1] becomes pieces[0] + 1 = 1."},{"at":{"start":0,"end":1},"vars":{"end":2,"start":0,"piece":"aa","pal":1,"pieces":"[0, 1, 1, -, -]"},"note":"Prefix length 2, last piece starts at 0. The piece 'aa' is a palindrome, so pieces[2] becomes pieces[0] + 1 = 1."},{"at":{"start":1,"end":1},"vars":{"end":2,"start":1,"piece":"a","pal":1,"pieces":"[0, 1, 1, -, -]"},"note":"Prefix length 2, last piece starts at 1. The piece 'a' is a palindrome, but pieces[1] + 1 = 2 does not beat 1."},{"at":{"start":0,"end":2},"vars":{"end":3,"start":0,"piece":"aab","pal":0,"pieces":"[0, 1, 1, -, -]"},"note":"Prefix length 3, last piece starts at 0. The piece 'aab' is not a palindrome, so this start is skipped."},{"at":{"start":1,"end":2},"vars":{"end":3,"start":1,"piece":"ab","pal":0,"pieces":"[0, 1, 1, -, -]"},"note":"Prefix length 3, last piece starts at 1. The piece 'ab' is not a palindrome, so this start is skipped."},{"at":{"start":2,"end":2},"vars":{"end":3,"start":2,"piece":"b","pal":1,"pieces":"[0, 1, 1, 2, -]"},"note":"Prefix length 3, last piece starts at 2. The piece 'b' is a palindrome, so pieces[3] becomes pieces[2] + 1 = 2."},{"at":{"start":0,"end":3},"vars":{"end":4,"start":0,"piece":"aaba","pal":0,"pieces":"[0, 1, 1, 2, -]"},"note":"Prefix length 4, last piece starts at 0. The piece 'aaba' is not a palindrome, so this start is skipped."},{"at":{"start":1,"end":3},"vars":{"end":4,"start":1,"piece":"aba","pal":1,"pieces":"[0, 1, 1, 2, 2]"},"note":"Prefix length 4, last piece starts at 1. The piece 'aba' is a palindrome, so pieces[4] becomes pieces[1] + 1 = 2."},{"at":{"start":2,"end":3},"vars":{"end":4,"start":2,"piece":"ba","pal":0,"pieces":"[0, 1, 1, 2, 2]"},"note":"Prefix length 4, last piece starts at 2. The piece 'ba' is not a palindrome, so this start is skipped."},{"at":{"start":3,"end":3},"vars":{"end":4,"start":3,"piece":"a","pal":1,"pieces":"[0, 1, 1, 2, 2]"},"note":"Prefix length 4, last piece starts at 3. The piece 'a' is a palindrome, but pieces[3] + 1 = 3 does not beat 2."}]}
```

<!-- stage: code -->
### Table First, Then Prefix Counts

The method returns the fewest cuts. The first pair of loops fills `pal` from the last row upward. The second pair fills `pieces` from short prefixes to long ones.

```java
static int minCuts(String s) {
    int n = s.length();
    if (n == 0) return 0;
    boolean[][] pal = new boolean[n][n];
    for (int i = n - 1; i >= 0; i--) {
        for (int j = i; j < n; j++) {
            boolean innerOk = j - i < 2 || pal[i + 1][j - 1];
            pal[i][j] = s.charAt(i) == s.charAt(j) && innerOk;
        }
    }
    int[] pieces = new int[n + 1];
    for (int end = 1; end <= n; end++) {
        pieces[end] = Integer.MAX_VALUE;
        for (int start = 0; start < end; start++) {
            if (pal[start][end - 1] && pieces[start] + 1 < pieces[end]) {
                pieces[end] = pieces[start] + 1;
            }
        }
    }
    return pieces[n] - 1;
}
```

Both parts take O(n^2) time, and the two tables need O(n^2) memory. The sentinel `Integer.MAX_VALUE` is safe, because `start = end - 1` always finds a one-character palindrome and `pieces[start]` is already finite. For an empty string the early return gives 0 in place of -1. The exercises below change the rule for a valid piece, the value stored per prefix and the memory used.

<!-- stage: applicability -->
### Recognizing Cost Tied To Valid Substrings

#### Reading The Cue

Use this method when a string splits into consecutive pieces, a yes-or-no rule judges each piece by its own characters, and the goal counts or minimizes the pieces. Phrases such as "every piece must be" and "fewest cuts" point here. The rule must depend only on the piece and not on its neighbours.

#### Checking The Invariant

The invariant says that `pal` is final before the prefix loop starts, and that `pieces[start]` is final before `pieces[end]` reads it. Test a single character, which needs 0 cuts. Test a whole-string palindrome, which also needs 0 cuts. Test a string with no repeated neighbours, such as `abcd`, which needs n - 1 cuts. Test the empty string, which must return 0.

#### Avoiding The False Friend

The first false friend is the longest-prefix rule from the opening, which passes any input where the longest palindrome at the front is also part of a best partition. The second false friend is a longest palindromic substring search, which finds one piece and says nothing about how the rest splits. The third is a table fill that visits `i` upward, so `pal[i + 1][j - 1]` is still false when read. The method does not apply when the validity of a piece depends on the pieces next to it, because `pieces[start]` then no longer summarizes the earlier text.

<!-- stage: exercises -->
### Exercises

#### [Build] Palindrome Table (Author exercise)
<!-- id: dp29-pp-palindrome-table -->

**Prerequisites.** The palindrome table from this lesson.

**Problem.** A string `s` is given. Count the pairs `(i, j)` with `0 <= i <= j < s.length()` for which the substring from index `i` to index `j`, both included, is a palindrome.

**Constraints.** The limits are:
- **Length** satisfies `0 <= s.length() <= 500`, and the string may be empty.
- **Characters** are lowercase English letters.
- **Result** is an `int`.
- **Mutation** is not allowed, because strings are immutable.

**Example 1.** Input `s = "aaba"`, output `6`.

**Example 2.** Input `s = "abcba"`, output `7`.

**Hint.** An entry reads the entry for the inner interval. Which loop order makes that entry final first?

**Changed decision.** The method counts true entries in place of using them to split the string. The fill rule stays the same.

#### [Vary] Minimum Valid Prefix Pieces (Author exercise)
<!-- id: dp29-pp-valid-prefix-pieces -->

**Prerequisites.** The exercise above.

**Problem.** A string `s` and an integer `k` are given. A piece is valid when it is a palindrome and has at least `k` characters. Split `s` into consecutive valid pieces and return the smallest number of pieces. Return -1 if no such split exists.

**Constraints.** The limits are:
- **Length** satisfies `1 <= s.length() <= 500`.
- **Minimum piece length** satisfies `1 <= k <= s.length()`.
- **Characters** are lowercase English letters.
- **Result** is an `int`, and -1 marks an impossible split.

**Example 1.** Input `s = "aabbcc"`, `k = 2`, output `3`.

**Example 2.** Input `s = "racecarbob"`, `k = 3`, output `2`.

**Hint.** For each prefix, try every earlier cut. Which cuts are allowed, and what value marks a prefix that no split reaches?

**Changed decision.** The validity rule gains a length limit, so some prefixes have no split. The array needs an explicit value for unreachable prefixes, and the transition must skip them.

#### [Boundary] Empty Prefix And Whole Palindrome (Author exercise)
<!-- id: dp29-pp-empty-prefix -->

**Prerequisites.** The two exercises above.

**Problem.** A string `s` is given. Return an `int` array `r` of length `s.length() + 1`. Entry `r[e]` is the fewest cuts in a palindrome partition of the first `e` characters of `s`.

**Constraints.** The limits are:
- **Length** satisfies `0 <= s.length() <= 500`, and the string may be empty.
- **Characters** are lowercase English letters.
- **Entry zero** equals 0, because the empty prefix needs no cuts.
- **Mutation** is not allowed, because strings are immutable.

**Example 1.** Input `s = ""`, output `[0]`.

**Example 2.** Input `s = "abcba"`, output `[0, 0, 1, 2, 1, 0]`.

**Hint.** Piece counts and cut counts differ by one. Which prefix would give -1 if the method subtracted blindly?

**Changed decision.** The method reports every prefix, not only the whole string. The empty prefix and every palindromic prefix must give 0, so the subtraction needs a guard.

#### [Recognize] Palindrome Partitioning II (LeetCode 132)
<!-- id: dp29-pp-min-cuts -->

**Prerequisites.** All three exercises above.

**Problem.** A string `s` is given. Split `s` into substrings so that each substring is a palindrome. Return the smallest number of cuts that makes this possible.

**Constraints.** The limits are:
- **Length** satisfies `1 <= s.length() <= 2000`.
- **Characters** are lowercase English letters.
- **Result** is an `int`, and 0 means `s` is already a palindrome.
- **Mutation** is not allowed, because strings are immutable.

**Example 1.** Input `s = "abbab"`, output `1`.

**Example 2.** Input `s = "cabbad"`, output `2`.

**Hint.** The cost of a piece depends on whether it is a palindrome. Can a second loop produce the validity answers while the cut counts fill?

**Changed decision.** The length limit of 2000 makes a full boolean table expensive. The solution keeps only an array of cut counts and finds palindromes by growing them from each center.
