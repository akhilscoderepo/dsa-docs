<!-- lesson-kind: standard -->
<!-- lesson-id: run-construction -->
## Compress Runs Of Characters

<!-- stage: context -->
### A Password Rule About Repeated Characters

A sign-up form rejects any password that repeats one character more than twice in a row. A user types `Passsword1` and gets an error. The check must find the longest stretch of identical neighbors in the text. A first attempt works on every test password and still times out on one input, a pasted string of 100000 equal characters.

The stretch can start at any position, and the test input makes that fact expensive. The question is how a loop measures every stretch of identical neighbors, including the very last one. It should look at each character only a constant number of times.

<!-- stage: naive -->
### Extending From Every Position

The direct method takes each index as the start of a stretch and walks right while the characters stay equal. It keeps the longest length found.

```java
static int longestStretch(String s) {
    int best = 0;
    for (int i = 0; i < s.length(); i++) {
        int j = i;
        while (j < s.length() && s.charAt(j) == s.charAt(i)) {
            j++;
        }
        best = Math.max(best, j - i);
    }
    return best;
}
```

On `"aabbbc"` the method returns 3. On the empty string it returns 0. On `"abc"` it returns 1, because every stretch holds one character.

<!-- stage: bottleneck -->
### Every Position Walks The Same Stretch Again

```predict
The method starts a walk at every index. For a string of n equal characters, about how many comparisons does it make in total, and why does it repeat work?

The walk from index i covers the n - i characters to its right, so the total is about n + (n - 1) + ... + 1, which is n(n + 1) / 2 and grows as O(n^2). Every position inside a stretch starts a walk over the part of the stretch that lies ahead, and the earlier walk already measured that part.
```

The pasted password of 100000 equal characters makes about five billion comparisons, which explains the timeout. The repeated work has a clear cause. When the walk from index 0 reaches the end of a stretch, it already knows where the stretch ends. The walks from the next indexes inside the stretch rediscover the same end. A correct method keeps the start of the current stretch, moves one index forward, and acts only when the stretch ends. It reads each character a constant number of times, which gives O(n) time with O(1) extra space.

<!-- stage: insight -->
### Close Each Block At Its Boundary

A **maximal run** is a block of equal characters that cannot grow, because the character before it and the character after it differ or do not exist. The string `"aabbbc"` has three maximal runs: `aa`, `bbb` and `c`. Every character belongs to exactly one maximal run.

#### Keep The Start Of The Current Run

The loop keeps `start`, the index where the current run began. Its character is `s.charAt(start)`, and its length so far is `i - start`. These two facts describe the part of the string that the loop has read and not yet measured. The loop needs no other memory about the past.

<!-- names: maximal run, run boundary, final run -->

#### A Run Boundary Closes The Run

A **run boundary** is an index `i` where `s.charAt(i)` differs from `s.charAt(start)`. At that index the current run is complete, with length `i - start`. The loop uses that length, for example to update a best value, and then sets `start = i`. The run is closed exactly once, and no later step looks at it again.

#### The Last Run Has No Boundary After It

The **final run** reaches the end of the string, so no later character differs from it. A loop that closes runs only when it sees a different character leaves the final run unclosed. The loop therefore treats index `s.length()` as a boundary too. It runs `i` from 1 through `s.length()` and tests `i == s.length()` before it reads any character at `i`. The invariant is that every run that ends before index `i` is closed, and `start` marks the open run.

<!-- stage: variables -->
### Start Index, Current Index And Best Length

Three values describe the loop at every step, and the notes below say when each changes.

- **start** names the first index of the open run and changes only when a run closes.
- **i** is the index under test, from 1 up to and including `s.length()`.
- **best** keeps the longest closed run, and a closing run can raise it.

<!-- stage: trace -->
### Measuring Runs In Two Strings

#### A String With Three Runs

Take `s = "aabbbc"`. The loop starts with `start = 0` and `best = 0`. At `i = 1` the character `a` equals the run character, so nothing closes. At `i = 2` the character `b` differs, so the run `aa` closes with length 2, and `start` moves to 2. The characters at `i = 3` and `i = 4` extend the run `bbb`. At `i = 5` the character `c` closes `bbb` with length 3, which becomes the best. At `i = 6`, which equals the length, the final run `c` closes with length 1.

#### A Last Run That Wins

Now take `s = "xyyy"`. The run `x` closes at `i = 1` with length 1. The characters at `i = 2` and `i = 3` extend the run `yyy`. Only the boundary at `i = 4`, the end of the string, closes it with length 3, so the answer depends on handling the final run.

#### Stepping Through Both Strings

```trace
{"cells":["a","a","b","b","b","c"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"start":0,"best":0},"note":"Start: the open run begins at index 0 and best is 0."},{"at":{"i":1},"vars":{"start":0,"best":0},"note":"Index 1 holds 'a', which matches the open run, so the run grows."},{"at":{"i":2},"vars":{"start":2,"best":2},"note":"At index 2, 'b' differs from 'a', so the run closes, with length 2. The best length is 2."},{"at":{"i":3},"vars":{"start":2,"best":2},"note":"Index 3 holds 'b', which matches the open run, so the run grows."},{"at":{"i":4},"vars":{"start":2,"best":2},"note":"Index 4 holds 'b', which matches the open run, so the run grows."},{"at":{"i":5},"vars":{"start":5,"best":3},"note":"At index 5, 'c' differs from 'b', so the run closes, with length 3. The best length is 3."},{"at":{"i":6},"vars":{"start":6,"best":3},"note":"At index 6, the index equals the length, so the end of the string closes the final run, with length 1. The best length is 3."}]}
```

```trace
{"cells":["x","y","y","y"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"start":0,"best":0},"note":"Start: the open run begins at index 0 and best is 0."},{"at":{"i":1},"vars":{"start":1,"best":1},"note":"At index 1, 'y' differs from 'x', so the run closes, with length 1. The best length is 1."},{"at":{"i":2},"vars":{"start":1,"best":1},"note":"Index 2 holds 'y', which matches the open run, so the run grows."},{"at":{"i":3},"vars":{"start":1,"best":1},"note":"Index 3 holds 'y', which matches the open run, so the run grows."},{"at":{"i":4},"vars":{"start":4,"best":3},"note":"At index 4, the index equals the length, so the end of the string closes the final run, with length 3. The best length is 3."}]}
```

<!-- stage: code -->
### One Pass With A Start Index

#### Measuring The Longest Run

```java
static int longestRun(String s) {
    int best = 0;
    int start = 0;
    for (int i = 1; i <= s.length(); i++) {
        if (i == s.length() || s.charAt(i) != s.charAt(start)) {
            best = Math.max(best, i - start);
            start = i;
        }
    }
    return best;
}
```

#### What The Method Costs

The loop makes at most n iterations, and each iteration does a constant amount of work, so the time is O(n). The method keeps a constant number of integers beyond the input, so the space is O(1). The empty string never enters the loop, because `i` starts at 1 and the bound is 0, so the method returns 0 without a special case.

<!-- stage: applicability -->
### Telling Runs From Duplicates

#### Look For Adjacent Equal Characters

Use this pattern when the problem talks about neighbors that are equal. Compression, run lengths, stuck keys and repeated-character limits all qualify. The invariant is that all runs before the open run are closed, and the open run starts at `start`. A loop that closes each run at its boundary and handles the end of the string reads each character once.

#### Equal Characters Far Apart Are A False Friend

A false friend is a problem that mentions repeated characters and does not mean adjacent ones. In `"aabaa"` the letter `a` appears four times, but it forms two runs of 2, and the run structure says nothing about the total of 4. Grouping equal characters wherever they sit needs a table or a sort. Letters from a small alphabet can use the table from the previous lesson. General grouping belongs to the next chapters.

#### Java Details That Cause Failures

Code that writes the result into the same `char[]` it reads must never let the write index pass the read index. A run of length `L` writes one character and, when `L >= 2`, the digits of `L`, and that is never more than `L` characters. A count above 9 needs several digit characters, so `(char) ('0' + count)` is wrong for a count of 10 or more. A builder call `append(count)` writes the digits of an `int` correctly.

<!-- stage: exercises -->
### Exercises

#### [Build] String Compression (LeetCode 443)
<!-- id: st-string-compression -->

**Prerequisites.** The start index and the boundary test from this lesson.

**Problem.** Let `chars` be a `char[]`. Rewrite its prefix in place. For each maximal run of equal characters, write the character, and when the run length is at least 2, write the decimal digits of the length after it. Return the number `k` of characters written. The first `k` entries of `chars` hold the result, and the entries after `k` are unspecified.

**Constraints.** The limits are:
- **Length** satisfies `1 <= chars.length <= 2000`.
- **Characters** are letters, digits and symbols from the ASCII range.
- **Counts** above 9 write each digit as its own character.
- **Space** is O(1) extra, with no second array.

**Example 1.** Input `chars = "xxxyzz"`, output `k = 5` with prefix `"x3yz2"`.

**Example 2.** Input `chars = "kkkkkkkkkkkk"` (twelve letters), output `k = 3` with prefix `"k12"`.

**Hint.** When a run closes, how many characters does the write side add, and why can the write index never pass the start of the next run?

**Changed decision.** The method closes runs as in this lesson, and a write index replaces the best length.

#### [Vary] Count And Say (LeetCode 38)
<!-- id: st-count-and-say -->

**Prerequisites.** The compression exercise above.

**Problem.** Define term 1 as the string `"1"`. Define term `k + 1` by reading term `k` from left to right and describing each maximal run as its length followed by its digit. Return term `n`.

**Constraints.** The limits are:
- **Input** satisfies `1 <= n <= 30`.
- **Terms** hold only the digits 1, 2 and 3.
- **Answer** is a string.
- **Method** builds each term with a `StringBuilder`.

**Example 1.** Input `n = 5`, output `"111221"`.

**Example 2.** Input `n = 2`, output `"11"`.

**Hint.** Which loop turns one term into the next, and what does the run closing at the end of the term write?

**Changed decision.** One run reader produces the next string, and the result of each round becomes the input of the next.

#### [Boundary] Final Run (Author exercise)
<!-- id: st-final-run -->

**Prerequisites.** The two exercises above and the final run from this lesson.

**Problem.** Given a string `s`, return an `int[]` that holds the lengths of the maximal runs of `s`, in order from left to right.

**Constraints.** The limits are:
- **Length** satisfies `0 <= s.length() <= 10^5`.
- **Characters** are lowercase English letters.
- **Empty input** gives an array of length 0.
- **Answer** holds one entry per maximal run, so its entries add up to `s.length()`.

**Example 1.** Input `s = "aaab"`, output `[3, 1]`.

**Example 2.** Input `s = ""`, output `[]`.

**Hint.** Which step records the length of the last run, and what does the loop see at that moment?

**Changed decision.** The answer lists every run, so the final run must be recorded as well as the runs that a later character closes.

#### [Recognize] Run-Length Encoding (Author exercise)
<!-- id: st-run-length-encoding -->

**Prerequisites.** All three exercises above.

**Problem.** Let `s` be a string. Return the encoding of `s`. The encoding writes, for each maximal run from left to right, the decimal length of the run followed by the run character. Runs of length 1 also write their length.

**Constraints.** The limits are:
- **Length** satisfies `0 <= s.length() <= 10^5`.
- **Characters** are lowercase English letters.
- **Lengths** may have several digits, such as 12.
- **Answer** for the empty string is the empty string.

**Example 1.** Input `s = "xxxxxxxxxxxxy"` (twelve letters `x`), output `"12x1y"`.

**Example 2.** Input `s = ""`, output `""`.

**Hint.** What does the loop write at each boundary, and what must it write after the loop ends or at index `s.length()`?

**Changed decision.** The result is a new string with a length for every run, and each run is emitted exactly once.
