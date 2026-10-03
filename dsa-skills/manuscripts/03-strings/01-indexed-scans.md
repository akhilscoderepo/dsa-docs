<!-- lesson-kind: standard -->
<!-- lesson-id: indexed-scans -->
## Indexed Scans

<!-- stage: context -->
### A Finger Moving Along A Line

A proofreader is given a long printed line, such as a serial number followed by a note, and asked a simple question: how many digits does it contain? She lays a finger under the first character, checks it, and moves the finger one place to the right. She never goes back and never looks ahead. When the finger passes the last character, she has seen everything once and the tally in her head is the answer.

The same finger can answer other questions about the line. Where does the first colon sit? How long is the last word? She only has to say, before she starts, what the finger is looking for and when the answer is decided. Everything to the left of the finger is settled, and everything to the right is still unread.

<!-- stage: naive -->
### Cut Off The Rest Each Step

Suppose the question is where the first colon is. A literal reading says that at each position, check whether the rest of the line starts with a colon.

```java
static int firstColonBySuffix(String s) {
    for (int i = 0; i < s.length(); i++) {
        if (s.substring(i).startsWith(":")) return i;
    }
    return -1;
}
```

It follows the sentence "does the rest of the text start with a colon" directly, and it returns the right answer: 1 for `"a:b"`, 0 for `":x"`, and -1 for `"abc"`.

<!-- stage: bottleneck -->
### Every Step Copies The Remainder

The call `s.substring(i)` builds a new string holding all characters from `i` to the end, so it copies `n - i` characters. Over the whole loop that adds up to about `n * n / 2` character copies, which makes the method O(n^2) time, and each step also leaves a temporary string for the garbage collector. A line of 100,000 characters without a colon performs about five billion character copies to learn that nothing matches.

The question at each position involves one character only. The position is already known, and the character at that position can be read in constant time. Everything else the substring copied, the whole rest of the line, is never inspected. The work grows with the square of the length although the question needs one look per character.

<!-- stage: insight -->
### Read One Character By Index

An **indexed scan** keeps one integer `i`, the index of the next unexamined character, and reads `s.charAt(i)` in constant time. The invariant is that every character before `i` has been examined and its effect on the answer has been recorded. Each step examines one character, moves `i` forward, and either updates a **running answer** or returns early because the answer is decided.

Every step applies a **character test** to the single character that was read: is it a digit, is it a colon, is it a space, is it an uppercase letter? The test is a comparison of one `char` against a constant or a range, which costs O(1). If the answer is a count, the running answer is a counter. If it is a position, the scan returns the first index where the test passes. If it is a length, the scan counts while the test passes, after skipping whatever the definition says to skip.

<!-- names: indexed scan, running answer, character test -->

The decision to make before writing the loop is when each answer is decided. A count is decided only at the end. A first position is decided at the first success, so the scan can stop early. The length of the last word is easiest to decide from the end of the line: skip trailing spaces, then count characters until the next space or the start. Choosing the direction and the stopping rule from the definition removes most off-by-one errors.

Two Java facts matter for the character test. A `char` is a 16-bit unit, and arithmetic on it produces an `int`, so a conversion back needs a cast. And `Character.isDigit` accepts digits from other scripts, so it can return true for characters that are not the ASCII digits a problem has in mind. When the statement says decimal digits, compare against `'0'` and `'9'` instead.

<!-- stage: variables -->
### The Index And The Running Answer

The index `i` is the next unexamined position, so before the loop it is 0 and after the loop it equals the length. The running answer is one variable whose meaning is fixed by the question: a count of matches so far, the length of the current word so far, or nothing at all when the scan returns the index itself. Keep the character in a local `char c`, so the test reads the string only once per step. For the backward scan of the last word, the index starts at the last position and moves down, and the same meaning holds mirrored: everything after `i` is settled.

<!-- stage: trace -->
### Counting Digits And Measuring A Last Word

Take the text `a1b2`. The index starts at 0. The character `a` is not a digit, so the count stays 0. The character `1` is a digit and the count becomes 1. The character `b` leaves it at 1, and the character `2` raises it to 2. The loop ends with the index equal to the length, and the answer is 2. No character was read twice.

Now take the last word of `hi  yo ` in a line where the underscore stands for a space, so the text is `h`, `i`, `_`, `_`, `y`, `o`, `_`. The backward scan starts at the last index. The final space is skipped because no word has begun. The `o` begins the word with length 1, and the `y` makes it 2. The space before `y` ends the word, so the answer is 2. The step to study is the first, where a space is skipped and not counted, since the definition says trailing spaces do not belong to the last word.

```trace
{"cells":["a","1","b","2"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"char":"a","count":0},"note":"Read 'a', which is not a digit. The count stays 0."},{"at":{"i":1},"vars":{"char":"1","count":1},"note":"Read '1', which is a digit. The count rises to 1."},{"at":{"i":2},"vars":{"char":"b","count":1},"note":"Read 'b', which is not a digit. The count stays 1."},{"at":{"i":3},"vars":{"char":"2","count":2},"note":"Read '2', which is a digit. The count rises to 2."}]}
```

```trace
{"cells":["h","i","_","_","y","o","_"],"pointers":["i"],"steps":[{"at":{"i":6},"vars":{"phase":"skip spaces","length":0},"note":"Index 6 holds a space and no word has begun, so skip it."},{"at":{"i":5},"vars":{"phase":"count letters","length":1},"note":"Index 5 holds 'o', part of the last word. The length is 1."},{"at":{"i":4},"vars":{"phase":"count letters","length":2},"note":"Index 4 holds 'y', part of the last word. The length is 2."},{"at":{"i":3},"vars":{"phase":"done","length":2},"note":"Index 3 holds a space, which ends the word. The answer is 2."}]}
```

<!-- stage: code -->
### Four Small Scans

```java
static int countDigits(String s) {
    int count = 0;
    for (int i = 0; i < s.length(); i++) {
        char c = s.charAt(i);
        if (c >= '0' && c <= '9') count++;
    }
    return count;
}

static int lengthOfLastWord(String s) {
    int i = s.length() - 1;
    while (i >= 0 && s.charAt(i) == ' ') i--;         // skip trailing spaces
    int length = 0;
    while (i >= 0 && s.charAt(i) != ' ') { length++; i--; }
    return length;
}

static int firstDelimiter(String s) {
    for (int i = 0; i < s.length(); i++) if (s.charAt(i) == ':') return i;
    return -1;
}

static String toLowerAscii(String s) {
    char[] out = new char[s.length()];
    for (int i = 0; i < out.length; i++) {
        char c = s.charAt(i);
        out[i] = (c >= 'A' && c <= 'Z') ? (char) (c + ('a' - 'A')) : c;
    }
    return new String(out);
}
```

Each method reads a character in constant time and makes one pass, so the time is O(n), and only `toLowerAscii` allocates extra space, one `char` array of length `n`. The conversion in the last method needs the cast to `char`. The ASCII range test is deliberate: `Character.isDigit` and `Character.toLowerCase` accept far more than ASCII, and the problem contract decides which behavior is wanted.

<!-- stage: applicability -->
### When One Pass Settles The Question

Use an indexed scan when each character can be judged on its own, or folded into a small running answer, and the characters are examined in one direction. The invariant is that the characters before the index are settled. Decide the stopping rule from the definition: end of input for a count, first success for a position, a space after letters for a word.

The false friend is a question that compares characters with each other, such as whether the text reads the same backward. That pairs a character near the start with one near the end, and a single moving index cannot hold both, so it needs two pointers, which Chapter 08 teaches. A second false friend is `substring`, `split` or `toCharArray` in a loop where only one character is needed. Each copies text and turns a linear scan into extra work and extra garbage.

In Java, strings are immutable, indexed by UTF-16 code units, and `charAt` runs in constant time. A character outside the basic range occupies two units, so counting visible characters can differ from counting `char` values. The problems here use ASCII, and the contract should say so. Also write `i < s.length()` and not a stored length that might go stale if the loop variable is changed inside the body.

<!-- stage: exercises -->
### Exercises

#### [Build] Count Digits (Author exercise)
<!-- id: st-count-digits -->

**Prerequisites.** Loops over arrays; the contract sheet from Chapter 00.

**Problem.** Given a string `s`, return how many of its characters are decimal digits, meaning the characters `'0'` through `'9'`. Every other character, including letters and punctuation, is not a digit.

**Constraints.** 0 <= s.length() <= 10^5 and all characters are ASCII. Use one pass and constant extra space.

**Example 1.** Input `s = "a1b2"`, output 2.

**Example 2.** Input `s = ""`, output 0, since an empty string has no characters at all.

**Hint.** What does the index mean at the start of the loop? Which comparison on a single character decides whether it is a digit?

**Changed decision.** First rung: a single character test is applied once per position, with a counter as the running answer.

#### [Vary] Length of Last Word (LeetCode 58)
<!-- id: st-length-last-word -->

**Prerequisites.** The count-digits exercise above.

**Problem.** Given a string made of letters and spaces, return the length of its last word. A word is a maximal run of non-space characters, and the string may begin or end with spaces.

**Constraints.** 1 <= s.length() <= 10^4 and `s` contains at least one word. Use one backward scan and constant extra space.

**Example 1.** Input `s = "  moon rise  "`, output 4.

**Example 2.** Input `s = "a"`, output 1, since the only word is the whole string.

**Hint.** From which end is the answer easiest to decide? What must you skip first, and when exactly does the word end?

**Changed decision.** The scan runs backward and has two phases, skipping spaces and then counting letters, so the definition of a word becomes explicit.

#### [Boundary] First Delimiter (Author exercise)
<!-- id: st-first-delimiter -->

**Prerequisites.** The two exercises above.

**Problem.** Return the index of the first `':'` in a string, or -1 if there is none. Check that a colon at index 0 and a string with no colon both come out right.

**Constraints.** 0 <= s.length() <= 10^5. Do not call `substring` inside the loop.

**Example 1.** Input `s = ":x"`, output 0.

**Example 2.** Input `s = "abc"`, output -1.

**Hint.** Which value does the loop return when it finishes without a match? Why is a colon at the very first position not a special case?

**Changed decision.** The answer is decided at the first success and the scan returns early, with -1 meaning that the whole string has been settled.

#### [Recognize] To Lower Case (LeetCode 709)
<!-- id: st-to-lower-case -->

**Prerequisites.** All three exercises above.

**Problem.** Given a string of printable ASCII characters, return the string with every uppercase letter replaced by the matching lowercase letter, and every other character unchanged.

**Constraints.** 1 <= s.length() <= 100 and every character is printable ASCII. Build the result without repeated string concatenation.

**Example 1.** Input `s = "JavaOne 21!"`, output `"javaone 21!"`.

**Example 2.** Input `s = "already lower"`, output `"already lower"`.

**Hint.** Does any output character depend on a different input position? How do you turn an uppercase `char` into a lowercase one by arithmetic?

**Changed decision.** Each output character depends only on the input character at the same index, so a scan with a character array suffices.
