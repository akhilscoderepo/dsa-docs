<!-- lesson-kind: standard -->
<!-- lesson-id: run-construction -->
## Run Construction

<!-- stage: context -->
### Counting Beads On A Cord

A jeweller strings coloured beads on a cord and wants a short label for the pattern, so that a customer can order it by phone. Reading the cord from one end, she says "three red, one blue, two green" instead of naming all six beads. She never looks back along the cord. She holds in mind the colour she is currently counting and how many of it she has seen, and the moment the colour changes she speaks the tally and starts counting the new colour.

Notice what she does at the very end of the cord. There is no next bead to trigger the announcement, yet the last colour still has to be spoken. Many string construction problems are this cord wearing different clothes, and the end of the cord is where most mistakes happen.

<!-- stage: naive -->
### Count Each Colour Over The Whole Cord

A literal reading of "how many of each colour" is to take every distinct colour and count it across the entire cord.

```java
static String labelByTotals(String cord) {
    StringBuilder label = new StringBuilder();
    boolean[] done = new boolean[128];
    for (int i = 0; i < cord.length(); i++) {
        char c = cord.charAt(i);
        if (done[c]) continue;
        done[c] = true;
        int total = 0;
        for (int j = 0; j < cord.length(); j++) if (cord.charAt(j) == c) total++;
        label.append(total).append(c);
    }
    return label.toString();
}
```

On `rrrbgg` it gives `3r1b2g`, which is right. On `rrbrr` it gives `4r1b`.

<!-- stage: bottleneck -->
### Totals Are Not Streaks

The answer for `rrbrr` is wrong in kind, not in degree. The customer asked for the pattern along the cord, and `4r1b` throws away where the blue bead sits, so nobody could rebuild the cord from it. Totals answer a different question from streaks, and no amount of tuning will turn one into the other.

The cost is also poor. For every distinct colour the inner loop rescans the whole cord, so the time is O(n * k) for `n` beads and `k` distinct colours, which approaches O(n * n) when most beads differ. The streaks needed no such rescanning, because two beads belong to the same streak only when they are neighbours. Whether a bead extends the current streak depends on one comparison with the bead just before it, and everything further back is irrelevant to that decision.

<!-- stage: insight -->
### Speak A Streak When It Ends

Group equal neighbours, and the cord splits into pieces where each piece is as long as possible. Each such piece is a **maximal run**, a block of equal adjacent characters that cannot be extended on either side. The cord `rrbrr` has three maximal runs, `rr`, `b` and `rr`, even though only two colours appear. Adjacent equality is the only thing that joins characters into a run, so equal characters separated by anything else belong to different runs.

While scanning, you hold only the **pending run**, the character being counted and its length so far. The invariant is that everything before the pending run has already been written out as finished runs, and the pending run describes exactly the suffix not yet written. A new character either matches the pending character and lengthens it, or differs and ends it.

<!-- names: maximal run, pending run, flush -->

To **flush** is to write the pending run to the output and start a new one. A flush happens whenever the character changes, and it must happen once more after the loop ends, because the last run is never followed by a different character to trigger it. Forgetting that final flush silently loses the last run, which is the classic bug in this family. With the flush in place, each character is read once, each run is written once, and the output is built by appending to a buffer rather than rebuilding a string.

<!-- stage: variables -->
### The Current Character And Its Length

Three pieces of state matter. The character `cur` is the one being counted, and the length `len` says how many consecutive copies have been seen, starting at 1 once the first character is read. The index `i` points at the next unread character. The output buffer holds finished runs only, so it never contains a run that might still grow. A change of character writes `len` then `cur` and resets `len` to 1 for the new character, and the end of the input performs the same write once more. An empty input has no first character, so it is handled before `cur` is read.

<!-- stage: trace -->
### Reading A Cord Of Six Beads

```trace
{"cells":["p","p","q","r","r","r"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"cur":"p","len":1,"output":"empty"},"note":"Read 'p'. It starts the pending run with length 1."},{"at":{"i":1},"vars":{"cur":"p","len":2,"output":"empty"},"note":"'p' matches the pending character, so the length rises to 2."},{"at":{"i":2},"vars":{"cur":"q","len":1,"output":"2p"},"note":"'q' differs from 'p'. Flush 2p to the output and start a new pending run of 'q'."},{"at":{"i":3},"vars":{"cur":"r","len":1,"output":"2p1q"},"note":"'r' differs from 'q'. Flush 1q to the output and start a new pending run of 'r'."},{"at":{"i":4},"vars":{"cur":"r","len":2,"output":"2p1q"},"note":"'r' matches the pending character, so the length rises to 2."},{"at":{"i":5},"vars":{"cur":"r","len":3,"output":"2p1q"},"note":"'r' matches the pending character, so the length rises to 3."},{"at":{"i":6},"vars":{"cur":"r","len":3,"output":"2p1q3r"},"note":"The input has ended. Flush the final run 3r. The output is 2p1q3r."}]}
```

Follow the cord `ppqrrr`. The first `p` starts the pending run with length 1, and the second `p` lengthens it to 2. The `q` differs, so the run `2p` is flushed to the output and `q` becomes the pending run. The `r` that follows differs from `q`, so `1q` is flushed, and two more `r` beads then raise the length to 3. When the index reaches the end, the final flush writes `3r`, and the output is `2p1q3r`.

The step to study is the last one. Nothing in the cord changed there, yet a write happened, because the end of the input ends the final run just as a new character would.

```trace
{"cells":["z","z","z","z","y","y","x"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"cur":"z","len":1,"write":0},"note":"Read 'z'. The pending run starts with length 1 and nothing has been written."},{"at":{"i":1},"vars":{"cur":"z","len":2,"write":0},"note":"'z' matches, so the length rises to 2."},{"at":{"i":2},"vars":{"cur":"z","len":3,"write":0},"note":"'z' matches, so the length rises to 3."},{"at":{"i":3},"vars":{"cur":"z","len":4,"write":0},"note":"'z' matches, so the length rises to 4."},{"at":{"i":4},"vars":{"cur":"y","len":1,"write":2},"note":"'y' differs. Write z4 at the write position, which is now 2, and start a new pending run."},{"at":{"i":5},"vars":{"cur":"y","len":2,"write":2},"note":"'y' matches, so the length rises to 2."},{"at":{"i":6},"vars":{"cur":"x","len":1,"write":4},"note":"'x' differs. Write y2 at the write position, which is now 4, and start a new pending run."},{"at":{"i":7},"vars":{"cur":"x","len":1,"write":5},"note":"The input has ended. Write the final run x. The compressed length is 5."}]}
```

The second trace compresses the characters `zzzzyyx` in place. The write position never overtakes the read position, because each run of length 1 produces one character, each run of length 2 produces two and longer runs produce fewer than they consume. That fact is what lets the compressed form overwrite the array it is reading.

<!-- stage: code -->
### Encoding, Compressing And Saying

```java
static String encode(String s) {
    if (s.isEmpty()) return "";
    StringBuilder out = new StringBuilder();
    char cur = s.charAt(0);
    int len = 1;
    for (int i = 1; i < s.length(); i++) {
        if (s.charAt(i) == cur) {
            len++;
        } else {
            out.append(len).append(cur);          // flush the finished run
            cur = s.charAt(i);
            len = 1;
        }
    }
    out.append(len).append(cur);                  // flush the last run
    return out.toString();
}

static int compress(char[] chars) {
    if (chars.length == 0) return 0;
    int write = 0;
    char cur = chars[0];
    int len = 1;
    for (int i = 1; i <= chars.length; i++) {
        if (i < chars.length && chars[i] == cur) { len++; continue; }
        chars[write++] = cur;                     // flush: the character, then its count if above 1
        if (len > 1) for (char d : Integer.toString(len).toCharArray()) chars[write++] = d;
        if (i < chars.length) { cur = chars[i]; len = 1; }
    }
    return write;
}

static String countAndSay(int n) {
    String term = "1";
    for (int step = 1; step < n; step++) term = encode(term);
    return term;
}
```

All three are O(n) in the length they read, with the `StringBuilder` giving amortized constant-time appends. The in-place version uses O(1) extra space and treats the position `i == chars.length` as the moment of the final flush, so the same code path handles the end. Concatenating with `+=` inside the loop would copy the growing output on every flush and cost O(n * n) in the worst case, which is why the buffer is used. Count and Say applies the encoder repeatedly, and each term is read as runs of the previous one.

<!-- stage: applicability -->
### When Neighbours Define The Group

Use run construction when equal adjacent characters form one unit and the output or answer is built left to right from those units. The invariant to say aloud is that everything before the pending run is finished and the pending run covers the unwritten suffix. Check the end of input explicitly, since that is where the last run waits.

The false friend is grouping all equal characters wherever they sit. Anagram grouping, duplicate counting and frequency questions look like run questions, but `abab` has no equal neighbours at all, and merging its two `a` characters needs a table or a sort. A fixed-alphabet table or the maps of Chapter 04 own those problems, and they are wrong tools for adjacency.

Java adds some points. Build output with a `StringBuilder`, and append an `int` directly so that multi-digit counts like 12 are written correctly, because adding `'0' + len` as a single character breaks at 10. In-place work on a `char[]` is safe only because compressed output never outruns the input being read, so confirm that before overwriting. Counts above 9 occupy several characters, and the compressed length must be measured in characters, not in runs.

<!-- stage: exercises -->
### Exercises

#### [Build] String Compression (LeetCode 443)
<!-- id: st-string-compression -->

**Prerequisites.** Chapter 01's write-index lens; the pending run in this lesson. This is a deliberate revisit, now driven by the pending run and its flush.

**Problem.** Given a character array `chars`, compress it in place so that each maximal run is written as its character followed by the decimal length of the run when the length exceeds 1. Return the new length of the array. Extra space must be constant, and lengths of 10 or more are written as several characters.

**Constraints.** 1 <= chars.length <= 2000 and every element is a letter, a digit or a symbol. Constant extra space is required.

**Example 1.** Input `chars = ['z','z','z','z','y','y','x']`, output 5, and the first five characters are `z4y2x`.

**Example 2.** Input `chars = ['q']`, output 1, and the array still starts with `q`.

**Hint.** When must the write happen for the final run, and why can the write position never get ahead of the read position?

**Changed decision.** The output now overwrites the input, so safety depends on the output never being longer than what has been read.

#### [Vary] Count and Say (LeetCode 38)
<!-- id: st-count-and-say -->

**Prerequisites.** The build exercise above.

**Problem.** The first term of the sequence is `"1"`. Each later term describes the previous term by reading its runs aloud, as a count followed by the digit. Return the `n`-th term as a string.

**Constraints.** 1 <= n <= 30. Terms grow quickly, so build each one with a buffer.

**Example 1.** Input `n = 4`, output `"1211"`, since the third term is `21`, which reads as one 2 and one 1.

**Example 2.** Input `n = 1`, output `"1"`, with no encoding step performed.

**Hint.** Each term is the encoding of the one before it. What would you have to change in the encoder to reuse it as it is?

**Changed decision.** The output of one pass becomes the input of the next, so the same run reader is applied repeatedly.

#### [Boundary] Final Run (Author exercise)
<!-- id: st-final-run -->

**Prerequisites.** The two exercises above.

**Problem.** Encode a string as count-then-character for each maximal run, and make sure the last run is written even though no character follows it. Show that a loop which only writes on a change of character drops the last run.

**Constraints.** 0 <= s.length() <= 10^5, any characters. A string with a single run must still produce one block.

**Example 1.** Input `s = "aaab"`, output `"3a1b"`, with both `3a` and `1b` present.

**Example 2.** Input `s = "zz"`, output `"2z"`, because the only run is also the last one.

**Hint.** What event ends the final run, given that no different character ever arrives? What should happen for the empty string?

**Changed decision.** The end of the input becomes a trigger equal in importance to a change of character.

#### [Recognize] Run-Length Encoding (Author exercise)
<!-- id: st-run-length-encoding -->

**Prerequisites.** All three exercises above.

**Problem.** Convert a string to its run-length encoding by writing each maximal run exactly once as its length followed by its character. Equal characters that are not adjacent form separate runs and must stay separate.

**Constraints.** 0 <= s.length() <= 10^5. Characters may repeat anywhere in the string. Output must be built with a buffer.

**Example 1.** Input `s = "aaabbc"`, output `"3a2b1c"`.

**Example 2.** Input `s = "abab"`, output `"1a1b1a1b"`, because no two equal characters are neighbours.

**Hint.** What single comparison decides whether a new character extends the pending run? Would a table of totals preserve the answer for `abab`?

**Changed decision.** The tempting grouping of equal characters anywhere is replaced by adjacency, which is what keeps the output reversible.
