<!-- lesson-kind: standard -->
<!-- lesson-id: common-subsequences -->
## Common Subsequences

<!-- stage: context -->
### Comparing Two Versions Of A Line

A version-control tool compares an old line of text, `bacd`, with a new line, `acdb`. The tool wants the longest run of characters that both lines keep in the same order, because everything else counts as an edit. The characters `a`, `c` and `d` appear in both lines in that order, so the shared length is 3. Only `b` moved.

A developer writes a quick scan. It reads the old line from left to right and, for each character, jumps to the next copy in the new line. The scan reports 1. It sees `b` first, jumps to the end of the new line, and has nothing left to read there.

Formally, the input is two strings `a` and `b`. A **subsequence** of a string keeps some of its characters, possibly none, in their original order and may skip characters between them. A **common subsequence** is a subsequence of both strings. The task is to return the length of the longest one. Neither string changes.

This lesson asks how to find that length when a single wrong early choice ruins a left-to-right scan.

<!-- stage: naive -->
### Scanning Left To Right With Early Choices

The quick idea is to take each character of `a` as soon as the new line can supply it. The scan keeps the position `p` in `b` after the last taken character.

```java
static int quickScan(String a, String b) {
    int p = 0;
    int taken = 0;
    for (int i = 0; i < a.length(); i++) {
        int q = b.indexOf(a.charAt(i), p);
        if (q >= 0) {
            taken++;
            p = q + 1;
        }
    }
    return taken;
}
```

The scan runs in O(a.length() * b.length()) time in the worst case and uses O(1) memory. It is fast, but each decision is final. Taking a character can push `p` so far right that better characters of `a` have no room left.

```predict
Run quickScan on a = "bacd" and b = "acdb". What does it return, and what is the true longest common subsequence length?

It returns 1. The scan takes b at the last position of the new line, so p moves past the end and a, c and d find nothing. The true length is 3, from the characters a, c and d.
```

<!-- stage: bottleneck -->
### One Early Choice Blocks Later Choices

The failure has a clear cause. Taking a character of `a` is not independent of the characters after it, because it fixes where the next search in `b` starts. A single choice made without looking ahead can cost the whole answer.

A correct but slow method lists every subsequence of `a` and checks whether it is also a subsequence of `b`. A string of length m has 2^m subsequences, and each check scans `b` in O(n) time. The total is O(2^m * n). For m = 40 that exceeds 10^13 steps.

The work repeats. Two different choices that stop at the same positions in both strings leave the same remaining problem, and the slow method solves that problem again for each choice. The number of distinct positions is only (m + 1) * (n + 1). If each position is solved once and stored, O(m * n) work suffices. The next section defines what to store and how one answer follows from smaller ones.

<!-- stage: insight -->
### Answer Each Pair Of Prefixes Once

Compare the two strings from their ends and let the answers for shorter strings decide the answer for longer ones. The table needs one entry for every pair of prefix lengths.

<!-- names: prefix pair, zero row, diagonal entry -->

#### One Entry For Each Prefix Pair

A **prefix pair** `(i, j)` is the first `i` characters of `a` together with the first `j` characters of `b`. Let `dp[i][j]` be the length of the longest common subsequence of that pair. The final answer is `dp[m][n]`, where m and n are the string lengths.

#### Equal Last Characters Join The Subsequence

Look at the last characters of the pair, `a[i - 1]` and `b[j - 1]`. If they are equal, some longest common subsequence ends with that character, and the rest of it lies inside the shorter pair `(i - 1, j - 1)`. The entry is therefore the **diagonal entry** `dp[i - 1][j - 1]` plus 1. Using the equal pair is never worse than skipping it, because skipping can only keep or shrink the remaining room.

#### Different Last Characters Drop One

If the last characters differ, they cannot both end the same common subsequence. At least one of them is unused. Dropping the last character of `a` gives the pair `(i - 1, j)`, and dropping the last character of `b` gives `(i, j - 1)`. The entry is the larger of `dp[i - 1][j]` and `dp[i][j - 1]`.

#### Empty Prefixes Fill The Zero Row

A prefix of length 0 is the empty string, which shares only the empty subsequence with any text. Row 0 and column 0 are the **zero row** and the zero column, and every entry in them is 0. The invariant is that when the loop reaches `(i, j)`, the three entries it reads are already final, because each has a smaller `i`, a smaller `j`, or both.

<!-- stage: variables -->
### The Table And Its Two Indexes

Two strings come in unchanged, and these working values describe the table.

- **dp** is an `int[m + 1][n + 1]`; entry `dp[i][j]` is the longest common subsequence length of the first `i` characters of `a` and the first `j` characters of `b`.
- **i** counts the characters of `a` in the prefix, from 1 to m.
- **j** counts the characters of `b` in the prefix, from 1 to n.
- **diag**, **up** and **left** are `dp[i - 1][j - 1]`, `dp[i - 1][j]` and `dp[i][j - 1]`, the three entries that entry `(i, j)` can read.

The characters being compared are `a.charAt(i - 1)` and `b.charAt(j - 1)`, because a prefix of length `i` ends at index `i - 1`. Java fills a new `int` array with zeros, so row 0 and column 0 need no extra code.

<!-- stage: trace -->
### Two Runs Of The Table

#### Moving One Letter Out Of Place

The first run uses the lines from the opening, `a = "bacd"` and `b = "acdb"`. The table has 5 rows and 5 columns, and the cells below list them row by row, so cell 0 to 4 is row 0, cell 5 to 9 is row 1, and so on. The pointer `cell` marks the entry in progress. The variables `diag`, `up` and `left` are the three entries it may read, and `dp` is the value written.

Row 1 compares `b` with each character of the new line. Its entries stay 0 until the last column, where `b` meets `b` and writes 1. Row 2 compares `a`. It finds an equal pair at column 1 and writes the diagonal value 0 plus 1. Rows 3 and 4 extend that chain with `c` and `d`, which reaches 3 at cell 23. The last column then compares `d` with `b`, which differ, so the entry keeps the larger neighbour and the answer stays 3.

```trace
{"cells":[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24],"pointers":["cell"],"steps":[{"at":{"cell":-1},"vars":{"i":0,"j":0,"diag":0,"up":0,"left":0,"dp":0},"note":"Row 0 and column 0 start at 0, because an empty prefix shares nothing with any other text."},{"at":{"cell":6},"vars":{"i":1,"j":1,"diag":0,"up":0,"left":0,"dp":0},"note":"Prefix lengths 1 and 1 end in 'b' and 'a'. The characters differ, so the entry is the larger of up 0 and left 0, which is 0."},{"at":{"cell":7},"vars":{"i":1,"j":2,"diag":0,"up":0,"left":0,"dp":0},"note":"Prefix lengths 1 and 2 end in 'b' and 'c'. The characters differ, so the entry is the larger of up 0 and left 0, which is 0."},{"at":{"cell":8},"vars":{"i":1,"j":3,"diag":0,"up":0,"left":0,"dp":0},"note":"Prefix lengths 1 and 3 end in 'b' and 'd'. The characters differ, so the entry is the larger of up 0 and left 0, which is 0."},{"at":{"cell":9},"vars":{"i":1,"j":4,"diag":0,"up":0,"left":0,"dp":1},"note":"Prefix lengths 1 and 4 end in 'b' on both sides. The characters are equal, so the entry is the diagonal value 0 plus 1, which is 1."},{"at":{"cell":11},"vars":{"i":2,"j":1,"diag":0,"up":0,"left":0,"dp":1},"note":"Prefix lengths 2 and 1 end in 'a' on both sides. The characters are equal, so the entry is the diagonal value 0 plus 1, which is 1."},{"at":{"cell":12},"vars":{"i":2,"j":2,"diag":0,"up":0,"left":1,"dp":1},"note":"Prefix lengths 2 and 2 end in 'a' and 'c'. The characters differ, so the entry is the larger of up 0 and left 1, which is 1."},{"at":{"cell":13},"vars":{"i":2,"j":3,"diag":0,"up":0,"left":1,"dp":1},"note":"Prefix lengths 2 and 3 end in 'a' and 'd'. The characters differ, so the entry is the larger of up 0 and left 1, which is 1."},{"at":{"cell":14},"vars":{"i":2,"j":4,"diag":0,"up":1,"left":1,"dp":1},"note":"Prefix lengths 2 and 4 end in 'a' and 'b'. The characters differ, so the entry is the larger of up 1 and left 1, which is 1."},{"at":{"cell":16},"vars":{"i":3,"j":1,"diag":0,"up":1,"left":0,"dp":1},"note":"Prefix lengths 3 and 1 end in 'c' and 'a'. The characters differ, so the entry is the larger of up 1 and left 0, which is 1."},{"at":{"cell":17},"vars":{"i":3,"j":2,"diag":1,"up":1,"left":1,"dp":2},"note":"Prefix lengths 3 and 2 end in 'c' on both sides. The characters are equal, so the entry is the diagonal value 1 plus 1, which is 2."},{"at":{"cell":18},"vars":{"i":3,"j":3,"diag":1,"up":1,"left":2,"dp":2},"note":"Prefix lengths 3 and 3 end in 'c' and 'd'. The characters differ, so the entry is the larger of up 1 and left 2, which is 2."},{"at":{"cell":19},"vars":{"i":3,"j":4,"diag":1,"up":1,"left":2,"dp":2},"note":"Prefix lengths 3 and 4 end in 'c' and 'b'. The characters differ, so the entry is the larger of up 1 and left 2, which is 2."},{"at":{"cell":21},"vars":{"i":4,"j":1,"diag":0,"up":1,"left":0,"dp":1},"note":"Prefix lengths 4 and 1 end in 'd' and 'a'. The characters differ, so the entry is the larger of up 1 and left 0, which is 1."},{"at":{"cell":22},"vars":{"i":4,"j":2,"diag":1,"up":2,"left":1,"dp":2},"note":"Prefix lengths 4 and 2 end in 'd' and 'c'. The characters differ, so the entry is the larger of up 2 and left 1, which is 2."},{"at":{"cell":23},"vars":{"i":4,"j":3,"diag":2,"up":2,"left":2,"dp":3},"note":"Prefix lengths 4 and 3 end in 'd' on both sides. The characters are equal, so the entry is the diagonal value 2 plus 1, which is 3."},{"at":{"cell":24},"vars":{"i":4,"j":4,"diag":2,"up":2,"left":3,"dp":3},"note":"Prefix lengths 4 and 4 end in 'd' and 'b'. The characters differ, so the entry is the larger of up 2 and left 3, which is 3."}]}
```

#### Two Different Ways To Reach 2

The second run uses `a = "cab"` and `b = "abc"`. The best length is 2, and it comes from `ab` in both strings. The row for `c` finds one equal pair at the last column and writes 1. The row for `a` finds an equal pair at column 1 and then carries that 1 to the right through differing pairs. The row for `b` finds an equal pair at column 2, reads the diagonal value 1 from that earlier equal pair, and writes 2. The last column then differs and keeps the larger neighbour, so the answer is 2.

```trace
{"cells":[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15],"pointers":["cell"],"steps":[{"at":{"cell":-1},"vars":{"i":0,"j":0,"diag":0,"up":0,"left":0,"dp":0},"note":"Row 0 and column 0 start at 0, because an empty prefix shares nothing with any other text."},{"at":{"cell":5},"vars":{"i":1,"j":1,"diag":0,"up":0,"left":0,"dp":0},"note":"Prefix lengths 1 and 1 end in 'c' and 'a'. The characters differ, so the entry is the larger of up 0 and left 0, which is 0."},{"at":{"cell":6},"vars":{"i":1,"j":2,"diag":0,"up":0,"left":0,"dp":0},"note":"Prefix lengths 1 and 2 end in 'c' and 'b'. The characters differ, so the entry is the larger of up 0 and left 0, which is 0."},{"at":{"cell":7},"vars":{"i":1,"j":3,"diag":0,"up":0,"left":0,"dp":1},"note":"Prefix lengths 1 and 3 end in 'c' on both sides. The characters are equal, so the entry is the diagonal value 0 plus 1, which is 1."},{"at":{"cell":9},"vars":{"i":2,"j":1,"diag":0,"up":0,"left":0,"dp":1},"note":"Prefix lengths 2 and 1 end in 'a' on both sides. The characters are equal, so the entry is the diagonal value 0 plus 1, which is 1."},{"at":{"cell":10},"vars":{"i":2,"j":2,"diag":0,"up":0,"left":1,"dp":1},"note":"Prefix lengths 2 and 2 end in 'a' and 'b'. The characters differ, so the entry is the larger of up 0 and left 1, which is 1."},{"at":{"cell":11},"vars":{"i":2,"j":3,"diag":0,"up":1,"left":1,"dp":1},"note":"Prefix lengths 2 and 3 end in 'a' and 'c'. The characters differ, so the entry is the larger of up 1 and left 1, which is 1."},{"at":{"cell":13},"vars":{"i":3,"j":1,"diag":0,"up":1,"left":0,"dp":1},"note":"Prefix lengths 3 and 1 end in 'b' and 'a'. The characters differ, so the entry is the larger of up 1 and left 0, which is 1."},{"at":{"cell":14},"vars":{"i":3,"j":2,"diag":1,"up":1,"left":1,"dp":2},"note":"Prefix lengths 3 and 2 end in 'b' on both sides. The characters are equal, so the entry is the diagonal value 1 plus 1, which is 2."},{"at":{"cell":15},"vars":{"i":3,"j":3,"diag":1,"up":1,"left":2,"dp":2},"note":"Prefix lengths 3 and 3 end in 'b' and 'c'. The characters differ, so the entry is the larger of up 1 and left 2, which is 2."}]}
```

<!-- stage: code -->
### Filling The Table Row By Row

The method returns the length of the longest common subsequence. It fills the table with a row for each prefix length of `a`.

```java
static int commonLength(String a, String b) {
    int m = a.length();
    int n = b.length();
    int[][] dp = new int[m + 1][n + 1];
    for (int i = 1; i <= m; i++) {
        for (int j = 1; j <= n; j++) {
            if (a.charAt(i - 1) == b.charAt(j - 1)) {
                dp[i][j] = dp[i - 1][j - 1] + 1;
            } else {
                dp[i][j] = Math.max(dp[i - 1][j], dp[i][j - 1]);
            }
        }
    }
    return dp[m][n];
}
```

Time grows as O(m * n) and the table needs O(m * n) memory. When only the length matters, two rows suffice, which cuts memory to O(n) but removes the ability to rebuild the subsequence itself. If either string is empty, a loop runs zero times and the method returns 0. The exercises below build the table step by step.

<!-- stage: applicability -->
### Recognizing Order-Preserving Matches

#### Reading The Cue

Use this method when two sequences may skip elements but must keep relative order. Phrases such as "in the same order, not necessarily next to each other" and "shared by both" point here. The state is a pair of prefix lengths, and each entry depends on three neighbours that have smaller indexes.

#### Checking The Invariant

The invariant says that each entry is final before any entry reads it, and that it describes exactly its own prefix pair. Test two equal strings, which must return their length. Test two strings with no shared character, which must return 0. Test one empty string. Test strings where the equal characters appear in reversed order, such as `ab` and `ba`, which must return 1.

#### Avoiding The False Friend

The first false friend is the quick left-to-right scan, which passes any test where the first available copy is also the best. The second is the longest common substring, which needs the characters to touch and resets an entry to 0 on a difference. The third is a table that sets the entry to the larger neighbour even when the characters are equal, which drops the matched character. The method does not apply when the pieces must be adjacent or when the order may change, because the prefix pair no longer captures the remaining problem.

<!-- stage: exercises -->
### Exercises

#### [Build] LCS Of Short Prefixes (Author exercise)
<!-- id: cs-short-prefixes -->

**Prerequisites.** The prefix-pair table from this lesson.

**Problem.** Strings `a` and `b` and integers `i` and `j` are given. Return the length of the longest common subsequence of the first `i` characters of `a` and the first `j` characters of `b`.

**Constraints.** The limits are:
- **Length** satisfies `0 <= a.length(), b.length() <= 500`.
- **Prefix lengths** satisfy `0 <= i <= a.length()` and `0 <= j <= b.length()`.
- **Characters** are lowercase English letters.
- **Mutation** is not allowed, because strings are immutable.

**Example 1.** Input `a = "bacd"`, `b = "acdb"`, `i = 3`, `j = 4`, output `2`.

**Example 2.** Input `a = "bacd"`, `b = "acdb"`, `i = 1`, `j = 2`, output `0`.

**Hint.** For one entry, which entry does an equal pair of last characters read, and which two entries does a different pair read?

**Changed decision.** The table stops at row `i` and column `j` in place of the full strings. Each entry still reads only entries with smaller indexes.

#### [Vary] Longest Common Subsequence (LeetCode 1143)
<!-- id: cs-longest-common-subsequence -->

**Prerequisites.** The exercise above.

**Problem.** Two strings `text1` and `text2` are given. Return the length of the longest string that is a subsequence of both. Return 0 if they share no character.

**Constraints.** The limits are:
- **Length** satisfies `1 <= text1.length(), text2.length() <= 1000`.
- **Characters** are lowercase English letters.
- **Result** is an `int`.
- **Mutation** is not allowed, because strings are immutable.

**Example 1.** Input `text1 = "abcd"`, `text2 = "xaybzc"`, output `3`.

**Example 2.** Input `text1 = "programming"`, `text2 = "gaming"`, output `6`.

**Hint.** Fill the whole table with two loops, and read the answer from the corner entry.

**Changed decision.** The prefix lengths now reach the full strings, so the answer is the last entry of the last row.

#### [Boundary] Empty Prefix (Author exercise)
<!-- id: cs-empty-prefix -->

**Prerequisites.** The two exercises above.

**Problem.** Strings `a` and `b` are given. Count the prefix pairs `(i, j)` with `0 <= i <= a.length()` and `0 <= j <= b.length()` whose longest common subsequence has length 0.

**Constraints.** The limits are:
- **Length** satisfies `0 <= a.length(), b.length() <= 300`, and either string may be empty.
- **Characters** are lowercase English letters.
- **Result** is an `int`.
- **Mutation** is not allowed, because strings are immutable.

**Example 1.** Input `a = ""`, `b = "abc"`, output `4`.

**Example 2.** Input `a = "ab"`, `b = "ba"`, output `6`.

**Hint.** Which entries are 0 before any character is compared, and does the loop need to visit them?

**Changed decision.** The method counts zeros in the whole table, including row 0 and column 0. With an empty string, every entry is one of those.

#### [Recognize] Delete Operation For Two Strings (LeetCode 583)
<!-- id: cs-delete-operation -->

**Prerequisites.** All three exercises above.

**Problem.** Two strings `word1` and `word2` are given. One step deletes one character from either string. Return the smallest number of steps that makes the strings equal.

**Constraints.** The limits are:
- **Length** satisfies `0 <= word1.length(), word2.length() <= 500`, and either string may be empty.
- **Characters** are lowercase English letters.
- **Result** is an `int`.
- **Mutation** is not allowed, because strings are immutable.

**Example 1.** Input `word1 = "bacd"`, `word2 = "acdb"`, output `2`.

**Example 2.** Input `word1 = "kitten"`, `word2 = "sitting"`, output `5`.

**Hint.** The characters that survive form a common subsequence of both strings. How long can that survivor string be?

**Changed decision.** The answer counts the removed characters, so the method returns the two lengths added together minus twice the common subsequence length.
