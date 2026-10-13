<!-- lesson-kind: standard -->
<!-- lesson-id: edit-distance -->
## Edit Distance

<!-- stage: context -->
### A Diff Tool Reporting Extra Changes

A text diff tool compares the old line `abc` with the new line `bc`. The tool walks both lines from the left and compares the characters at the same position. Position 0 differs, so it reports a change. Position 1 differs, so it reports a second change. The old line has one extra character, so it reports a third change. The honest answer is a single deletion of the first character.

The same failure appears in a spell checker that ranks suggestions by how many characters differ. A word that lost its first letter looks as different as an unrelated word, because every later character shifts by one position.

Formally, the input is two strings `s` and `t`, and either may be empty. One edit is an insertion of one character, a deletion of one character, or a replacement of one character with another. The task is to return the smallest number of edits that turns `s` into `t`. The method never changes the strings.

This lesson asks how to count the fewest edits when characters shift position.

<!-- stage: naive -->
### Comparing Position By Position

The quick idea is to scan both strings at the same index. A mismatch costs one replacement, and any extra characters at the end cost one deletion or insertion each.

```java
static int samePositionCount(String s, String t) {
    int common = Math.min(s.length(), t.length());
    int edits = Math.abs(s.length() - t.length());
    for (int i = 0; i < common; i++) {
        if (s.charAt(i) != t.charAt(i)) edits++;
    }
    return edits;
}
```

The method runs in O(min(m, n)) time for strings of length m and n. It gives a correct count only when no insertion or deletion happens before the end. The open question is what the count means when a character is removed near the front.

```predict
Run samePositionCount on "abc" and "bc". What does it return, and what is the true minimum number of edits?

It returns 3. Positions 0 and 1 mismatch, and the length gap adds one more. The true minimum is 1, because deleting the first character of "abc" produces "bc". Position matching ignores that a deletion shifts every later character.
```

<!-- stage: bottleneck -->
### Every Edit Shifts The Alignment

An insertion or a deletion moves all later characters by one position. A fixed pairing of index `i` in `s` with index `i` in `t` is therefore wrong as soon as one such edit occurs. The method must try each choice at the current position and compare the totals.

A correct but slow method does exactly that with recursion. At the front of both strings, it either skips two equal characters or tries the three edits. Each edit shortens `s`, `t` or both by one character, so the recursion has depth up to m + n and branches three ways. The work is O(3^(m + n)). For two strings of length 15 that is already above 10^14 calls.

Most of those calls repeat. The recursion asks again and again for the cost of the same pair of remaining suffixes, and there are only (m + 1) * (n + 1) distinct pairs. Storing each answer once reduces the work to O(m * n) time and memory. The next section defines the stored answer and proves that three neighbors suffice.

<!-- stage: insight -->
### Each Cell Reads Three Neighbors

Define the answer for every pair of prefixes and fill the pairs from short to long. The final pair is the whole task.

<!-- names: prefix pair, last characters, diagonal neighbor -->

#### One Cell For Each Prefix Pair

A **prefix pair** is the first `i` characters of `s` together with the first `j` characters of `t`. Let `dp[i][j]` be the smallest number of edits that turns the first `i` characters of `s` into the first `j` characters of `t`. The table has `m + 1` rows and `n + 1` columns, and the answer is `dp[m][n]`.

#### Compare The Last Characters

Look at the **last characters** of the two prefixes, which are `s[i - 1]` and `t[j - 1]`. If they are equal, an optimal script can leave them paired, so `dp[i][j]` equals `dp[i - 1][j - 1]`, the **diagonal neighbor**. If they differ, the script must handle the last character of `s` in one of three ways. A replacement pairs the two characters and costs `dp[i - 1][j - 1] + 1`. A deletion removes `s[i - 1]` and costs `dp[i - 1][j] + 1`. An insertion appends `t[j - 1]` after the prefix of `s` and costs `dp[i][j - 1] + 1`. The cell holds the smallest of the three.

#### Edges Hold Plain Lengths

When `j` is 0, the target prefix is empty, so every character of the source prefix needs a deletion, and `dp[i][0]` equals `i`. When `i` is 0, every character of the target prefix needs an insertion, and `dp[0][j]` equals `j`. The invariant is that every cell is final before any cell that reads it, because each read points up, left or diagonally up-left. A row-by-row fill from the top row satisfies that order.

<!-- stage: variables -->
### The Table And The Three Reads

The method leaves both strings alone and keeps these working values.

- **dp** is an `int[m + 1][n + 1]`; entry `dp[i][j]` is the edit distance between the first `i` characters of `s` and the first `j` characters of `t`.
- **i** is the row, which counts the characters taken from `s`.
- **j** is the column, which counts the characters taken from `t`.
- **diag** is `dp[i - 1][j - 1]`, which the method reads for a match or a replacement.
- **up** is `dp[i - 1][j]`, which the method reads for a deletion.
- **left** is `dp[i][j - 1]`, which the method reads for an insertion.

Row 0 and column 0 are filled before the loops, so the loops start at 1 and no read goes outside the table. In the trace, the cell index is `i * (n + 1) + j`, which numbers the table row by row.

<!-- stage: trace -->
### Two Runs Over Small Words

#### Turning spin Into pine

The first run turns `spin` into `pine`. The table has 5 rows and 5 columns, so cells 0 to 24 cover it row by row. The first row and first column are filled before the loops, so the trace starts at row 1. The pointer `cell` marks the entry in progress, and the variables show the three reads and the stored result.

Cell 6 compares `s` with `p`, which differ, and the best of the three reads is 0, so the cell holds 1. The first match appears at `p` against `p`, where the cell copies its diagonal neighbor. The pair `i` against `i` matches again one row later and extends the cheap path. The last cell holds 2, which means one deletion of `s` and one insertion of `e`.

```trace
{"cells":[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24],"pointers":["cell"],"steps":[{"at":{"cell":-1},"vars":{"i":0,"j":0,"diag":0,"up":0,"left":0,"dp":0},"note":"The first row and first column already hold plain lengths, because an empty prefix needs one edit per character."},{"at":{"cell":6},"vars":{"i":1,"j":1,"diag":0,"up":1,"left":1,"dp":1},"note":"Compare s with p for prefix lengths 1 and 1. The characters differ, so the cell adds one to the smallest read, which is 0."},{"at":{"cell":7},"vars":{"i":1,"j":2,"diag":1,"up":2,"left":1,"dp":2},"note":"Compare s with i for prefix lengths 1 and 2. The characters differ, so the cell adds one to the smallest read, which is 1."},{"at":{"cell":8},"vars":{"i":1,"j":3,"diag":2,"up":3,"left":2,"dp":3},"note":"Compare s with n for prefix lengths 1 and 3. The characters differ, so the cell adds one to the smallest read, which is 2."},{"at":{"cell":9},"vars":{"i":1,"j":4,"diag":3,"up":4,"left":3,"dp":4},"note":"Compare s with e for prefix lengths 1 and 4. The characters differ, so the cell adds one to the smallest read, which is 3."},{"at":{"cell":11},"vars":{"i":2,"j":1,"diag":1,"up":1,"left":2,"dp":1},"note":"Compare p with p for prefix lengths 2 and 1. The characters match, so the cell copies the diagonal value 1."},{"at":{"cell":12},"vars":{"i":2,"j":2,"diag":1,"up":2,"left":1,"dp":2},"note":"Compare p with i for prefix lengths 2 and 2. The characters differ, so the cell adds one to the smallest read, which is 1."},{"at":{"cell":13},"vars":{"i":2,"j":3,"diag":2,"up":3,"left":2,"dp":3},"note":"Compare p with n for prefix lengths 2 and 3. The characters differ, so the cell adds one to the smallest read, which is 2."},{"at":{"cell":14},"vars":{"i":2,"j":4,"diag":3,"up":4,"left":3,"dp":4},"note":"Compare p with e for prefix lengths 2 and 4. The characters differ, so the cell adds one to the smallest read, which is 3."},{"at":{"cell":16},"vars":{"i":3,"j":1,"diag":2,"up":1,"left":3,"dp":2},"note":"Compare i with p for prefix lengths 3 and 1. The characters differ, so the cell adds one to the smallest read, which is 1."},{"at":{"cell":17},"vars":{"i":3,"j":2,"diag":1,"up":2,"left":2,"dp":1},"note":"Compare i with i for prefix lengths 3 and 2. The characters match, so the cell copies the diagonal value 1."},{"at":{"cell":18},"vars":{"i":3,"j":3,"diag":2,"up":3,"left":1,"dp":2},"note":"Compare i with n for prefix lengths 3 and 3. The characters differ, so the cell adds one to the smallest read, which is 1."},{"at":{"cell":19},"vars":{"i":3,"j":4,"diag":3,"up":4,"left":2,"dp":3},"note":"Compare i with e for prefix lengths 3 and 4. The characters differ, so the cell adds one to the smallest read, which is 2."},{"at":{"cell":21},"vars":{"i":4,"j":1,"diag":3,"up":2,"left":4,"dp":3},"note":"Compare n with p for prefix lengths 4 and 1. The characters differ, so the cell adds one to the smallest read, which is 2."},{"at":{"cell":22},"vars":{"i":4,"j":2,"diag":2,"up":1,"left":3,"dp":2},"note":"Compare n with i for prefix lengths 4 and 2. The characters differ, so the cell adds one to the smallest read, which is 1."},{"at":{"cell":23},"vars":{"i":4,"j":3,"diag":1,"up":2,"left":2,"dp":1},"note":"Compare n with n for prefix lengths 4 and 3. The characters match, so the cell copies the diagonal value 1."},{"at":{"cell":24},"vars":{"i":4,"j":4,"diag":2,"up":3,"left":1,"dp":2},"note":"Compare n with e for prefix lengths 4 and 4. The characters differ, so the cell adds one to the smallest read, which is 1."}]}
```

#### Turning act Into cat

The second run turns `act` into `cat`. The table has 4 rows and 4 columns, so cells 0 to 15 cover it. Only the last pair, `t` against `t`, matches at equal positions, and the answer is 2. The path uses two replacements, which turn `a` into `c` and `c` into `a`. A deletion of the leading `a` and an insertion of a second `a` also costs 2, so the cell ties between two scripts. The table stores only the count, which is why the exercises recover a script by walking back through it.

```trace
{"cells":[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15],"pointers":["cell"],"steps":[{"at":{"cell":-1},"vars":{"i":0,"j":0,"diag":0,"up":0,"left":0,"dp":0},"note":"The first row and first column already hold plain lengths, because an empty prefix needs one edit per character."},{"at":{"cell":5},"vars":{"i":1,"j":1,"diag":0,"up":1,"left":1,"dp":1},"note":"Compare a with c for prefix lengths 1 and 1. The characters differ, so the cell adds one to the smallest read, which is 0."},{"at":{"cell":6},"vars":{"i":1,"j":2,"diag":1,"up":2,"left":1,"dp":1},"note":"Compare a with a for prefix lengths 1 and 2. The characters match, so the cell copies the diagonal value 1."},{"at":{"cell":7},"vars":{"i":1,"j":3,"diag":2,"up":3,"left":1,"dp":2},"note":"Compare a with t for prefix lengths 1 and 3. The characters differ, so the cell adds one to the smallest read, which is 1."},{"at":{"cell":9},"vars":{"i":2,"j":1,"diag":1,"up":1,"left":2,"dp":1},"note":"Compare c with c for prefix lengths 2 and 1. The characters match, so the cell copies the diagonal value 1."},{"at":{"cell":10},"vars":{"i":2,"j":2,"diag":1,"up":1,"left":1,"dp":2},"note":"Compare c with a for prefix lengths 2 and 2. The characters differ, so the cell adds one to the smallest read, which is 1."},{"at":{"cell":11},"vars":{"i":2,"j":3,"diag":1,"up":2,"left":2,"dp":2},"note":"Compare c with t for prefix lengths 2 and 3. The characters differ, so the cell adds one to the smallest read, which is 1."},{"at":{"cell":13},"vars":{"i":3,"j":1,"diag":2,"up":1,"left":3,"dp":2},"note":"Compare t with c for prefix lengths 3 and 1. The characters differ, so the cell adds one to the smallest read, which is 1."},{"at":{"cell":14},"vars":{"i":3,"j":2,"diag":1,"up":2,"left":2,"dp":2},"note":"Compare t with a for prefix lengths 3 and 2. The characters differ, so the cell adds one to the smallest read, which is 1."},{"at":{"cell":15},"vars":{"i":3,"j":3,"diag":2,"up":2,"left":2,"dp":2},"note":"Compare t with t for prefix lengths 3 and 3. The characters match, so the cell copies the diagonal value 2."}]}
```

<!-- stage: code -->
### Filling The Table Row By Row

The method returns the edit distance. It fills the edges first and then each interior cell from its three neighbors.

```java
static int editDistance(String s, String t) {
    int m = s.length(), n = t.length();
    int[][] dp = new int[m + 1][n + 1];
    for (int i = 0; i <= m; i++) dp[i][0] = i;
    for (int j = 0; j <= n; j++) dp[0][j] = j;
    for (int i = 1; i <= m; i++) {
        for (int j = 1; j <= n; j++) {
            if (s.charAt(i - 1) == t.charAt(j - 1)) {
                dp[i][j] = dp[i - 1][j - 1];
            } else {
                dp[i][j] = 1 + Math.min(dp[i - 1][j - 1],
                        Math.min(dp[i - 1][j], dp[i][j - 1]));
            }
        }
    }
    return dp[m][n];
}
```

The cost is O(m * n) time and O(m * n) memory. Two empty strings give a 1 by 1 table with answer 0. Row `i` reads only row `i - 1` and itself, so two arrays of length `n + 1` are enough when no script is needed. The exercises below build the table in four forms.

<!-- stage: applicability -->
### Recognizing Strings That Become Each Other

#### Reading The Cue

Use this method when one sequence must become another by local changes and the goal is the fewest changes or the cheapest total cost. Words such as "minimum number of operations to convert" and "insert, delete or replace a character" point here. Each prefix pair has one answer, and each answer depends on three smaller prefix pairs.

#### Checking The Invariant

The invariant says that `dp[i][j]` is the exact distance between two fixed prefixes, and each operation moves to the matching smaller pair. Check it with an empty string on each side, which must return the other length. Check two equal strings, which must return 0. Check strings of different lengths with no shared letter, which must return the longer length.

#### Avoiding The False Friend

The first false friend is position-by-position comparison, which breaks after one deletion. The second is the longest common subsequence length, which ignores replacement and counts a replacement as one deletion and one insertion. The third is a greedy rule that matches the first equal letters, which fails when an early match blocks a cheaper alignment.

The method does not apply when edit costs depend on the position or on a moved block of text. Moving a whole block is not one edit here, and the table cannot price it.

<!-- stage: exercises -->
### Exercises

#### [Build] Insert Or Delete Only (Author exercise)
<!-- id: ed-insert-delete-only -->

**Prerequisites.** The prefix table of the previous lesson and the three reads from this lesson.

**Problem.** Given strings `s` and `t`, one operation inserts one character at any position or deletes one character from any position. Return the smallest number of operations that turns `s` into `t`.

**Constraints.** The limits are:
- **Length** satisfies `0 <= s.length(), t.length() <= 500`.
- **Alphabet** is lowercase English letters.
- **Result** is an `int`.
- **Mutation** is not allowed, because strings are immutable.

**Example 1.** Input `s = "sea"`, `t = "eat"`, output `2`.

**Example 2.** Input `s = "abc"`, `t = "xyz"`, output `6`.

**Hint.** When the last characters differ, which two neighbors remain once replacement is not allowed?

**Changed decision.** The replacement read is removed, and only the match, deletion and insertion reads remain. A mismatch costs one more than the smaller of `up` and `left`.

#### [Vary] Edit Distance (LeetCode 72)
<!-- id: ed-edit-distance -->

**Prerequisites.** The exercise above.

**Problem.** Given strings `word1` and `word2`, one operation inserts one character, deletes one character or replaces one character with another. Return the smallest number of operations that turns `word1` into `word2`.

**Constraints.** The limits are:
- **Length** satisfies `0 <= word1.length(), word2.length() <= 500`.
- **Alphabet** is lowercase English letters.
- **Result** is an `int`.
- **Mutation** is not allowed, because strings are immutable.

**Example 1.** Input `word1 = "kitten"`, `word2 = "sitting"`, output `3`.

**Example 2.** Input `word1 = "monday"`, `word2 = "mundane"`, output `3`.

**Hint.** Which cell gives the cost of a replacement, and when is that cost zero?

**Changed decision.** A replacement read and a free match are added to the two operations of the previous exercise. Equal last characters copy the diagonal neighbor without adding one.

#### [Boundary] Empty String (Author exercise)
<!-- id: ed-empty-string -->

**Prerequisites.** The two exercises above.

**Problem.** Given strings `s` and `t`, either of which may be empty, return the smallest number of insertions, deletions and replacements that turns `s` into `t`.

**Constraints.** The limits are:
- **Length** satisfies `0 <= s.length(), t.length() <= 300`.
- **Alphabet** is lowercase English letters.
- **Empty input** is legal for either string or both.
- **Result** is an `int`.

**Example 1.** Input `s = ""`, `t = "abc"`, output `3`.

**Example 2.** Input `s = "abcd"`, `t = ""`, output `4`.

**Hint.** What does `dp[i][0]` mean when the target prefix has no characters?

**Changed decision.** The first row and first column come from lengths and not from the three reads. When one string is empty, the loops never run and the table edge is the answer.

#### [Recognize] Reconstruct Operations (Author exercise)
<!-- id: ed-reconstruct-operations -->

**Prerequisites.** All three exercises above.

**Problem.** Given strings `s` and `t`, return a script as a `String` with one letter for each aligned step, read from left to right. The letter `M` keeps a matching character, `R` replaces a character, `D` deletes a character of `s`, and `I` inserts a character of `t`. The script has the fewest letters other than `M`. When several moves are optimal at the end of a prefix pair, prefer the diagonal move, then `D`, then `I`.

**Constraints.** The limits are:
- **Length** satisfies `0 <= s.length(), t.length() <= 300`.
- **Alphabet** is lowercase English letters.
- **Result** has length at least `max(s.length(), t.length())`.
- **Mutation** is not allowed, because strings are immutable.

**Example 1.** Input `s = "cat"`, `t = "cut"`, output `"MRM"`.

**Example 2.** Input `s = "ab"`, `t = "b"`, output `"DM"`.

**Hint.** Starting from `dp[m][n]`, which neighbor cell explains the stored value?

**Changed decision.** The same table is built, and then the method walks from the last cell back to cell `(0, 0)`. Each step emits one letter, and the letters are reversed at the end.
