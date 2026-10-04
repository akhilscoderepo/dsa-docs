<!-- lesson-kind: standard -->
<!-- lesson-id: indexed-scans -->
## Scan A String By Index

<!-- stage: context -->
### A Word Counter That Says Three

A text editor shows a word count in its status bar. The first version counts the spaces in the text and adds one. It works on `"hello world"`, which shows 2 words. A user then types two spaces between the words. The status bar jumps to 3, although the text still holds two words.

The counter never looked at the characters around each space. It treated every space as the same event, and the text broke that belief. This lesson asks one question. How does a loop over the characters of a string define a word precisely, so that extra spaces, leading spaces and an empty string all give the right count?

<!-- stage: naive -->
### Splitting On Every Space

The shortest correct-looking answer asks Java to cut the text at each space and counts the pieces.

```java
static int countWords(String s) {
    return s.split(" ").length;
}
```

On `"hello world"` the call returns 2. On `"a  b"` the two spaces make an empty piece between them, so the call returns 3. On the empty string `""` the call returns 1, because splitting an empty string gives one empty piece. The method also allocates a new array and a new `String` for every piece before it counts anything.

<!-- stage: bottleneck -->
### Pieces Are Not Words

```predict
The split method cuts the text at every single space. What word count does it report for "a  b", what count should a correct method report, and how much extra memory does it use for a text of n characters?

It reports 3 pieces, because the two spaces cut out an empty piece. A correct method reports 2 words. The pieces together hold about n characters, so the method uses O(n) extra memory beyond the input.
```

The count is wrong because the method counts separators, and the question asks about words. Two separators in a row produce an empty piece that is not a word. The memory cost is a second problem. The method reads the text in O(n) time, which no method can beat. It also builds O(n) characters of new strings only to count them. A correct method needs to read each character once and keep one integer, so it runs in O(n) time with O(1) extra memory. That method first needs an exact definition of where a word begins.

<!-- stage: insight -->
### Count Where A Word Begins

A string stores its characters at the positions `0` through `s.length() - 1`. The call `s.charAt(i)` reads the character at position `i` in constant time. A loop with an index `i` can therefore visit every character once, left to right.

#### The Index Marks The Unexamined Part

During the loop, the index `i` is the position of the next unexamined character. Every character before `i` has been read, and its effect lives in a small running answer. The loop starts with `i = 0` and an answer for the empty prefix. It ends when `i` equals `s.length()`, so the loop reads every character exactly once.

<!-- names: unexamined, word start, charAt -->

#### A Word Start Is A Local Fact

A **word start** is a position `i` where `s.charAt(i)` is not a space and either `i` is `0` or `s.charAt(i - 1)` is a space. A word start depends only on the character at `i` and the one just before it. The loop can test it without remembering anything else. The number of words equals the number of word starts, because each word has exactly one first character. Repeated spaces, leading spaces and trailing spaces create no word start, so they cost nothing and change nothing.

#### Test The Position Before Reading Behind It

The test reads `s.charAt(i - 1)`, which is illegal when `i` is `0`. Java evaluates `&&` and `||` from left to right. It skips the right side once the left side decides the result. Writing `i == 0 ||` first means the call that reads behind the index runs only when `i` is at least 1.

<!-- stage: variables -->
### Index, Word Start Test And Count

The loop keeps three pieces of state, and each one changes at a known moment.

- **i** holds the index of the next unexamined character and grows by one on every iteration.
- **startsWord** holds true when the character at `i` begins a word and the loop recomputes it on every iteration.
- **words** holds the number of word starts found before or at `i` and grows only when `startsWord` is true.

<!-- stage: trace -->
### Counting Words In Two Strings

#### Extra Spaces In The Middle

Take `s = "to  be"`. The symbol `␣` in the trace below stands for one space. The pointer `i` marks the character that the current step examines. At `i = 0` the character `t` is not a space and `i` is `0`, so a word starts and the count becomes 1. At `i = 1` the character `o` follows `t`, so no word starts. Both spaces at `i = 2` and `i = 3` are spaces, so they never start a word. At `i = 4` the character `b` follows a space, so the second word starts. The final count is 2, and the loop ends when `i` reaches 6, which equals the length.

#### Spaces At Both Ends

Now take `s = "␣x␣y␣"`. At `i = 0` the character is a space, so no word starts. At `i = 1` the character `x` follows a space, so a word starts. At `i = 3` the character `y` starts the second word. The final space at `i = 4` starts nothing. The count is 2, and the loop ends when `i` reaches 5, which equals the length.

#### Stepping Through Both Strings

```trace
{"cells":["t","o","␣","␣","b","e"],"pointers":["i"],"steps":[{"at":{"i":-1},"vars":{"words":0},"note":"Start: no character has been read, so words is 0."},{"at":{"i":0},"vars":{"startsWord":true,"words":1},"note":"Position 0 holds 't' and it is the first position, so a word starts. The count is 1."},{"at":{"i":1},"vars":{"startsWord":false,"words":1},"note":"Position 1 holds 'o' and the character before it is a letter, so no word starts. The count is 1."},{"at":{"i":2},"vars":{"startsWord":false,"words":1},"note":"Position 2 holds a space, so no word starts. The count is 1."},{"at":{"i":3},"vars":{"startsWord":false,"words":1},"note":"Position 3 holds a space, so no word starts. The count is 1."},{"at":{"i":4},"vars":{"startsWord":true,"words":2},"note":"Position 4 holds 'b' and the character before it is a space, so a word starts. The count is 2."},{"at":{"i":5},"vars":{"startsWord":false,"words":2},"note":"Position 5 holds 'e' and the character before it is a letter, so no word starts. The count is 2."}]}
```

```trace
{"cells":["\u2423","x","\u2423","y","\u2423"],"pointers":["i"],"steps":[{"at":{"i":-1},"vars":{"words":0},"note":"Start: no character has been read, so words is 0."},{"at":{"i":0},"vars":{"startsWord":false,"words":0},"note":"Position 0 holds a space, so no word starts. The count is 0."},{"at":{"i":1},"vars":{"startsWord":true,"words":1},"note":"Position 1 holds 'x' and the character before it is a space, so a word starts. The count is 1."},{"at":{"i":2},"vars":{"startsWord":false,"words":1},"note":"Position 2 holds a space, so no word starts. The count is 1."},{"at":{"i":3},"vars":{"startsWord":true,"words":2},"note":"Position 3 holds 'y' and the character before it is a space, so a word starts. The count is 2."},{"at":{"i":4},"vars":{"startsWord":false,"words":2},"note":"Position 4 holds a space, so no word starts. The count is 2."},{"at":{"i":5},"vars":{"words":2},"note":"The index equals the length, so the loop ends with 2 words."}]}
```

<!-- stage: code -->
### Scanning With An Index

#### A Loop That Counts Word Starts

```java
static int countWords(String s) {
    int words = 0;
    for (int i = 0; i < s.length(); i++) {
        boolean startsWord = s.charAt(i) != ' '
                && (i == 0 || s.charAt(i - 1) == ' ');
        if (startsWord) {
            words++;
        }
    }
    return words;
}
```

#### What The Loop Costs

The loop calls `charAt` at most twice per index and each call takes constant time, so the method runs in O(n) time for a string of length n. It stores two integers and one boolean, so it uses O(1) extra space. The empty string skips the loop and returns 0, which is correct without any special case.

<!-- stage: applicability -->
### When One Index Is Enough

#### Look For A Local Answer

Use a single index scan when each character contributes to the answer by itself, or together with a fixed amount of state about earlier characters. Counting characters of one kind, finding the first character that matches a test, and mapping each character to another character all qualify. The invariant of the scan is that the running answer always describes exactly the characters before `i`, and nothing else.

#### A Paired Comparison Is A False Friend

A false friend is a task that looks like a scan and breaks its rule. Checking whether a string reads the same backwards looks like a scan, but it compares the character at `i` with the character at `s.length() - 1 - i`. That second position moves in the opposite direction, so one index and a small running answer cannot describe the work. Tasks of that kind need two moving positions, which a later chapter teaches.

#### When Reading Behind Is Still Safe

The word start test reads one position behind `i`. This is still a single scan, because the position behind `i` is always `i - 1`, a fixed distance from the index. The scan stops being a single scan when the second position moves by its own rule.

#### Java Details That Cause Failures

The call `s.charAt(i)` returns a `char`, which Java compares as a number, so `c == ' '` is a correct test. A call with an index below 0 or at least `s.length()` throws `StringIndexOutOfBoundsException`. A `char` holds one UTF-16 code unit, so a character outside the basic range occupies two positions. The exercises in this chapter use text made of single-unit characters only.

<!-- stage: exercises -->
### Exercises

#### [Build] Count Digits (Author exercise)
<!-- id: st-count-digits -->

**Prerequisites.** The index loop and the meaning of `i` from this lesson.

**Problem.** Let `s` be a string. A decimal digit is one of the characters `'0'` through `'9'`. Return the number of positions of `s` that hold a decimal digit.

**Constraints.** The limits are:
- **Length** satisfies `0 <= s.length() <= 10^5`; the empty string is legal.
- **Characters** are any Java `char` values, so the method tests the range `'0'` to `'9'` and no other digit.
- **Answer** is an `int`.
- **Mutation** does not occur.

**Example 1.** Input `s = "r2d2!"`, output 2.

**Example 2.** Input `s = ""`, output 0, because the loop never runs.

**Hint.** Which comparison accepts exactly the ten characters `'0'` to `'9'`, and which library call accepts more than that?

**Changed decision.** Basic case: the running answer is one integer that grows when a test succeeds.

#### [Vary] Length Of The Last Word (LeetCode 58)
<!-- id: st-last-word -->

**Prerequisites.** The count of word starts from this lesson and the digit counter above.

**Problem.** Let `s` be a string made of letters and spaces. A word is a maximal run of consecutive letters. Return the length of the last word of `s`.

**Constraints.** The limits are:
- **Length** satisfies `1 <= s.length() <= 10^4`.
- **Characters** are English letters and the space character `' '`.
- **Words** exist, so `s` contains at least one letter.
- **Spaces** may appear at the start, at the end and between words.

**Example 1.** Input `s = "go home  "`, output 4, because trailing spaces belong to no word.

**Example 2.** Input `s = "a"`, output 1.

**Hint.** What must the running length do when a letter starts a word, and what must it do when a space appears after a word?

**Changed decision.** The running answer changes meaning: it holds the length of the latest word, and a space leaves it untouched.

#### [Boundary] First Delimiter (Author exercise)
<!-- id: st-first-delim -->

**Prerequisites.** The index loop from this lesson.

**Problem.** Let `s` be a string. Return the smallest index `i` such that `s.charAt(i)` equals `':'`. Return `-1` when `s` holds no colon.

**Constraints.** The limits are:
- **Length** satisfies `0 <= s.length() <= 10^5`.
- **Characters** are any Java `char` values.
- **Answer** is an `int` in the range `-1` to `s.length() - 1`.
- **Mutation** does not occur.

**Example 1.** Input `s = ":x"`, output 0, because the colon sits at the first position.

**Example 2.** Input `s = "abc"`, output -1, because the loop ends without a match.

**Hint.** Which statement leaves the loop at the first match, and what does the method return when the loop finds none?

**Changed decision.** The scan stops early on the first success, and the method must choose a return value for no match.

#### [Recognize] To Lower Case (LeetCode 709)
<!-- id: st-to-lower -->

**Prerequisites.** All three exercises above.

**Problem.** Let `s` be a string of printable ASCII characters. Return a string of the same length where each character from `'A'` to `'Z'` becomes the matching character from `'a'` to `'z'`. Every other character stays unchanged.

**Constraints.** The limits are:
- **Length** satisfies `0 <= s.length() <= 10^5`.
- **Characters** are printable ASCII, with code values 32 through 126.
- **Answer** is a new string; `s` does not change.
- **Method** is a loop over the characters, with no call to `toLowerCase`.

**Example 1.** Input `s = "Ab-C9"`, output `"ab-c9"`.

**Example 2.** Input `s = ""`, output `""`.

**Hint.** Each output character depends on one input character at the same index. What is the numeric distance between `'A'` and `'a'`?

**Changed decision.** The scan produces a new character at each index and not a single running number.
