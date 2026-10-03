<!-- lesson-kind: standard -->
<!-- lesson-id: nested-decoding -->
## Nested Decoding

<!-- stage: context -->
### The Knitting Pattern Shorthand

A knitting club writes its patterns in a shorthand to save paper. A number followed by a bracketed stretch means that the stretch is worked that many times, so `3[ab]` means plain, purl, plain, purl, plain, purl, written as `ababab`. Shorthand can be nested, because a motif that repeats can contain a smaller motif that repeats: `2[a3[b]]` is `abbbabbb`. Some repeat counts run past nine, such as a border that is worked twelve times, and several shorthand groups can sit side by side in a single row.

The club's newest member has a pattern book in shorthand and a machine that wants the long form. She needs a decoder that reads the shorthand once and produces the stitches, and she needs to trust it on a row like `2[a]3[b2[c]]`, where one group follows another and the second contains a third.

<!-- stage: naive -->
### Expand The Innermost Group, Again And Again

The direct method finds the first closing bracket, which must end an innermost group, walks back to its opening bracket and to the digits before it, replaces the whole group by its expansion, and repeats until no brackets remain.

```java
static String decodeByRewriting(String s) {
    String cur = s;
    while (cur.indexOf(']') >= 0) {
        int close = cur.indexOf(']');
        int open = cur.lastIndexOf('[', close);
        int digitsStart = open;
        while (digitsStart > 0 && Character.isDigit(cur.charAt(digitsStart - 1))) digitsStart--;
        int count = Integer.parseInt(cur.substring(digitsStart, open));
        String body = cur.substring(open + 1, close);
        cur = cur.substring(0, digitsStart) + body.repeat(count) + cur.substring(close + 1);
    }
    return cur;
}
```

It is correct, because the first closing bracket always ends a group with no brackets inside, and expanding it leaves a shorter nesting depth for the rest.

<!-- stage: bottleneck -->
### Every Expansion Copies The Whole Row

Each rewrite builds a new string out of the text before the group, the expansion, and the text after it, so it copies the entire current row. A row with g groups needs g rewrites, and each copy can be as long as the final output L, so the work is O(g L). With ten thousand small groups in a row whose final length is a hundred thousand stitches, that is a billion character copies, although the final row only has a hundred thousand characters, and each scan for the closing bracket also restarts at the left edge of the row.

The rewriting method also expands an inner group first and then repeats the already-expanded text when the outer group is expanded, which is right, but it stores the half-built row only as one long string, so every step touches all of it. A reader who keeps the unfinished row of each enclosing group separately only has to extend the row that is currently open, and the cost of the whole decode drops to O(n + L).

<!-- stage: insight -->
### Park The Parent Row And Its Count

Read the shorthand once. Keep a **digit accumulator**, a number that is updated as `count = count * 10 + digit` for each digit in a row of digits, so that a count such as 12 is read correctly instead of as 1 and then 2. Keep a builder for the row that is currently being worked. When an opening bracket arrives, the group is about to start, so park the state of the enclosing level: push the current builder together with the repeat count that was just read, which is the **frame pair**, and start a new empty builder and a count of zero.

Letters are appended to the builder of the innermost open group. When a closing bracket arrives, the **close-bracket expansion** happens: take the finished builder, repeat its text as many times as the parked count says, then pop the frame pair, append the repeated text to the parked builder, and continue with the parked builder as the current one. Nothing outside the group has been touched while it was open, so the parked row is exactly where it was.

The invariant is that each frame on the stack holds the unfinished row of one enclosing level and the repeat count that applies to the group directly inside it, and the current builder holds the innermost unfinished row. A decoder that repeats immediately at each digit fails on two counts: a multi-digit count is cut short, and the text to be repeated has not been read yet, so nothing can be repeated.

<!-- names: digit accumulator, frame pair, close-bracket expansion -->

Adjacent groups need no special care: when one group closes, the current builder is again the parent's, and the next digits start a new count.

<!-- stage: variables -->
### Count, Current Row, Parked Frames

The integer `count` accumulates digits and is reset to zero after being parked at an opening bracket. The builder `cur` is the row of the innermost open group, and it starts as the whole output row. Two stacks run in step, `counts` for parked integers and `rows` for parked builders, and they always have the same size. A letter is appended to `cur`. A closing bracket removes one entry from each stack. The final answer is `cur.toString()`, since after the last character every group has been closed and `cur` is the outermost row.

<!-- stage: trace -->
### Two Levels, Then A Two-Digit Count

The first trace decodes `2[a3[b]]`. The row of cells spells the input, with `i` at the character being processed. The first opening bracket parks the empty outer row with the count 2, and the second parks the row `a` with the count 3. Look at the first closing bracket: the open row `b` is repeated three times to give `bbb`, and the parked row `a` receives it, so the current row becomes `abbb`.

```trace
{"cells":["2","[","a","3","[","b","]","]"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"count":2,"row":"","parked":"[]"},"note":"The digit 2 is read, so the count becomes 2."},{"at":{"i":1},"vars":{"count":0,"row":"","parked":"[]"},"note":"An opening bracket parks the row '' with the count 2, then starts an empty row and a zero count."},{"at":{"i":2},"vars":{"count":0,"row":"a","parked":"[]"},"note":"The letter a is appended to the current row, which becomes 'a'."},{"at":{"i":3},"vars":{"count":3,"row":"a","parked":"[]"},"note":"The digit 3 is read, so the count becomes 3."},{"at":{"i":4},"vars":{"count":0,"row":"","parked":"[,a]"},"note":"An opening bracket parks the row 'a' with the count 3, then starts an empty row and a zero count."},{"at":{"i":5},"vars":{"count":0,"row":"b","parked":"[,a]"},"note":"The letter b is appended to the current row, which becomes 'b'."},{"at":{"i":6},"vars":{"count":0,"row":"abbb","parked":"[]"},"note":"A closing bracket repeats 'b' 3 times and appends it to the parked row, so the current row becomes 'abbb'."},{"at":{"i":7},"vars":{"count":0,"row":"abbbabbb","parked":"[]"},"note":"A closing bracket repeats 'abbb' 2 times and appends it to the parked row, so the current row becomes 'abbbabbb'."}]}
```

The second trace decodes `12[ab]c`. The digit 1 is read, and then the digit 2 turns the count into 12 by multiplying by ten and adding. If the decoder had acted at the first digit it would have used the count 1 and left a stray 2.

```trace
{"cells":["1","2","[","a","b","]","c"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"count":1,"row":"","parked":"[]"},"note":"The digit 1 is read, so the count becomes 1."},{"at":{"i":1},"vars":{"count":12,"row":"","parked":"[]"},"note":"The digit 2 is read, so the count becomes 12."},{"at":{"i":2},"vars":{"count":0,"row":"","parked":"[]"},"note":"An opening bracket parks the row '' with the count 12, then starts an empty row and a zero count."},{"at":{"i":3},"vars":{"count":0,"row":"a","parked":"[]"},"note":"The letter a is appended to the current row, which becomes 'a'."},{"at":{"i":4},"vars":{"count":0,"row":"ab","parked":"[]"},"note":"The letter b is appended to the current row, which becomes 'ab'."},{"at":{"i":5},"vars":{"count":0,"row":"abababababababababababab","parked":"[]"},"note":"A closing bracket repeats 'ab' 12 times and appends it to the parked row, so the current row becomes 'abababababababababababab'."},{"at":{"i":6},"vars":{"count":0,"row":"ababababababababababababc","parked":"[]"},"note":"The letter c is appended to the current row, which becomes 'ababababababababababababc'."}]}
```

<!-- stage: code -->
### Decode With Two Parallel Stacks

```java
static String decode(String s) {
    ArrayDeque<Integer> counts = new ArrayDeque<>();
    ArrayDeque<StringBuilder> rows = new ArrayDeque<>();
    StringBuilder cur = new StringBuilder();
    int count = 0;
    for (int i = 0; i < s.length(); i++) {
        char c = s.charAt(i);
        if (c >= '0' && c <= '9') {
            count = count * 10 + (c - '0');
        } else if (c == '[') {
            counts.addLast(count);
            rows.addLast(cur);
            cur = new StringBuilder();
            count = 0;
        } else if (c == ']') {
            String body = cur.toString();
            cur = rows.removeLast();
            cur.append(body.repeat(counts.removeLast()));
        } else {
            cur.append(c);
        }
    }
    return cur.toString();
}
```

Each input character causes constant work apart from the append of repeated text, and every output character is written a small number of times, once for each level it is copied through, so the time is O(n + L * d) for output length L and nesting depth d, and the space is O(n + L).

<!-- stage: applicability -->
### When A Count Governs A Group

Use two parked values per level when a repeat count applies to a bracketed stretch that may itself contain counted groups, as in compressed text, run-length notations and repeated templates. The invariant is that every frame holds the unfinished row of an enclosing level and the count for the group directly inside it.

A false friend is expanding at each digit, which breaks on counts above nine and on nesting. A second false friend is a single global builder, which merges inner and outer rows once a group has been entered. A third is the repeated rewriting of one string, which is correct and copies the whole row for every group.

In Java, convert a digit with `c - '0'` and never with a cast, which would give the character code. Reset the count to zero after parking it, or the count leaks into the next group. Remember that `String.repeat` returns the empty string for zero and throws `IllegalArgumentException` for a negative count, so decide what a count of zero means before reading input.

<!-- stage: exercises -->
### Exercises

#### [Build] Decode One Flat Group (Author exercise)
<!-- id: sq-decode-flat-group -->

**Prerequisites.** The Queue-Based Level Processing lesson.

**Problem.** The input is letters, then one group of the form `k[letters]` with a single-digit `k`, then letters. Return the decoded text, where the group's letters are repeated `k` times in place. The input has no nested group.

**Constraints.** 1 <= s.length <= 100, `k` is a digit from 1 to 9, and every other character in the group is a lowercase letter.

**Example 1.** Input `s = "3[ab]"`, output `"ababab"`.

**Example 2.** Input `s = "x2[yz]w"`, output `"xyzyzw"`.

**Hint.** What must be remembered between the opening bracket and the closing bracket? Where does the repeated text go?

**Changed decision.** First rung: one level is enough, so a count and a buffer for the group suffice, with no stack of parked rows.

#### [Vary] Multi-Digit Repeat Count (Author exercise)
<!-- id: sq-multi-digit-count -->

**Prerequisites.** The Decode One Flat Group rung.

**Problem.** The input is letters and flat groups of the form `k[letters]`, where `k` may have several digits and several groups may follow each other. Return the decoded text. A group never contains another group.

**Constraints.** 1 <= s.length <= 100, every count is at most 300, and the decoded text has at most 100000 characters.

**Example 1.** Input `s = "12[a]"`, output `"aaaaaaaaaaaa"`.

**Example 2.** Input `s = "10[ab]c"`, output `"ababababababababababc"`.

**Hint.** How is the number 12 built from the digits 1 and 2? When is the count reset?

**Changed decision.** The count is accumulated as `count * 10 + digit`, and it is reset when the group opens, so that multi-digit counts read correctly.

#### [Boundary] Adjacent And Nested Groups (Author exercise)
<!-- id: sq-adjacent-nested-groups -->

**Prerequisites.** The Multi-Digit Repeat Count rung.

**Problem.** The input is letters, counts and brackets, with groups that follow each other and groups that contain other groups. Return the decoded text. Every bracket is balanced and every count is at most 20.

**Constraints.** 1 <= s.length <= 100, the nesting depth is at most 5, and the decoded text has at most 100000 characters.

**Example 1.** Input `s = "2[a]3[b2[c]]"`, output `"aabccbccbcc"`.

**Example 2.** Input `s = "2[2[2[a]]]"`, output `"aaaaaaaa"`.

**Hint.** After one group closes, which builder is current? What happens to the count when the next group starts?

**Changed decision.** Frames are parked and restored in pairs, so adjacent groups reuse the parent row and nested groups never mix with their parents.

#### [Recognize] Decode String (LeetCode 394)
<!-- id: sq-decode-string -->

**Prerequisites.** The Adjacent And Nested Groups rung.

**Problem.** Given an encoded string, return its decoded form. The encoding rule is `k[encoded_string]`, which means the text inside the brackets is repeated exactly `k` times. The input is always well formed, and digits appear only as repeat counts.

**Constraints.** 1 <= s.length <= 30, every count is between 1 and 300, and the decoded text has at most 100000 characters.

**Example 1.** Input `s = "2[x3[y]z]"`, output `"xyyyzxyyyz"`.

**Example 2.** Input `s = "ab2[c]"`, output `"abcc"`.

**Hint.** What is parked when a bracket opens, and what is combined when it closes?

**Changed decision.** The complete nested grammar is decoded with saved counts and parent builders, in a single pass.
