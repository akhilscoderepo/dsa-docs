<!-- lesson-kind: standard -->
<!-- lesson-id: safe-construction -->
## Safe Construction

<!-- stage: context -->
### The Scribe Who Recopies The Letter

A scribe is hired to copy a long letter onto fresh paper, leaving out every space. He reads the original one character at a time, and whenever he finds a letter worth keeping, he takes a new sheet, copies everything he has written so far, and then adds the new letter at the end. By the time he reaches the end of a letter with ten thousand characters, he has recopied the growing text ten thousand times.

His employer watches the pile of discarded sheets grow taller than the letter itself and asks why he does not simply keep one long scroll and add each letter to the end of it. The scribe replies that paper never changes once written, which is true of his sheets, and does not apply to a scroll that has been left with room at the end.

<!-- stage: naive -->
### Glue Each Character Onto The Result

In Java the same behavior hides in the plain plus sign. Building the output by gluing one character at a time looks harmless.

```java
static String removeSpacesByConcatenation(String s) {
    String result = "";
    for (int i = 0; i < s.length(); i++) {
        char c = s.charAt(i);
        if (c != ' ') result += c;
    }
    return result;
}
```

On `"a b c"` it returns `"abc"`, and it is the shortest version that anyone would write. Strings are immutable in Java, so the compiler has to produce a new string at every `+=`.

<!-- stage: bottleneck -->
### Every Addition Copies Everything So Far

Each `result += c` builds a new string with the length of the old one plus one, so it copies every character already there. After `k` kept characters the step costs about `k` copies, and over `n` kept characters the total is about `n * n / 2`, which is O(n^2) time. For 200,000 characters that is twenty billion character copies, and the old strings pile up as garbage. The extra space at any moment is only O(n), so memory is not the main problem and time is.

The repeated copying is the waste. The output is only ever extended at its end, and all the earlier characters never change. A structure that can append at the end without copying the existing characters would make each step cost a constant amount, apart from occasional growth that is spread over many appends.

<!-- stage: insight -->
### One Builder, Growing At The End

A `StringBuilder` is a growable array of characters with spare room at its end. Appending a character writes into the spare room in constant time, and when the room runs out the builder allocates a larger array and copies once. Over a long run of appends the growth is paid back by many cheap steps, so appending is O(1) amortized. The **builder** therefore holds the output as it is being made, and a single `toString()` at the end creates the final string once.

The invariant is that the builder always contains exactly the **completed prefix** of the output: the part that is final and will not change. Each step either appends the next piece of output or does nothing, so the invariant holds after every step. If the output is built in the wrong order, for example reversed by inserting at the front, the builder must move all the characters already present at every insertion, and the cost is quadratic again. To reverse, append in reverse order of reading, or call `reverse()` once at the end.

<!-- names: builder, completed prefix, separator ownership -->

A recurring decision is **separator ownership**: which step is responsible for writing the space or comma between items. The reliable rule is that the loop writes a separator before every item except the first, which it can test with `builder.length() > 0`. Then no separator follows the last item and an empty list produces an empty result with no special case. The opposite rule, writing a separator after every item and removing the last one, fails when there are no items, because there is nothing to remove.

Some outputs are built in several places at once. A zigzag layout needs one builder per row, each owning its own completed prefix, and the rows are joined at the end. The same rule holds for each: append only, and read the result once at the end.

<!-- stage: variables -->
### Builder, Index And Separator Test

The builder `out` is created before the loop and holds the completed prefix. The index `i` reads the input. For word-based output, a pair of indices `start` and `end` marks the word that has just been found, and the word is appended in one call. The separator test is `out.length() > 0`, evaluated before appending the next item. After the loop, `out.toString()` gives the answer, and nothing else is read from the builder in between. For row-based output, an array of builders is indexed by the current row, and a direction variable moves down and then up.

<!-- stage: trace -->
### Building Without Spaces And Reversing Words

Take `a b c`, with underscores standing for spaces so the cells are `a`, `_`, `b`, `_`, `c`. The builder starts empty. The `a` is kept, so the builder holds `a`. The space is skipped. The `b` is kept, giving `ab`. The next space is skipped, and the `c` gives `abc`. Each character was read once and appended at most once, and the builder never needed to copy its contents.

Now reverse the words of `go far now`, again with underscores for spaces. Scan from the end. The first word found is `now`. The builder is empty, so no separator is written, and `now` is appended. Moving left, the next word is `far`. The builder is not empty, so a space is appended and then `far`. The last word is `go`, again preceded by a space. The result is `now far go`. The step to study is the first, where the empty builder suppressed the separator.

```trace
{"cells":["a","_","b","_","c"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"builder":"a"},"note":"Read 'a' and append it. The builder holds 'a'."},{"at":{"i":1},"vars":{"builder":"a"},"note":"Read a space and skip it. The builder still holds 'a'."},{"at":{"i":2},"vars":{"builder":"ab"},"note":"Read 'b' and append it. The builder holds 'ab'."},{"at":{"i":3},"vars":{"builder":"ab"},"note":"Read a space and skip it. The builder still holds 'ab'."},{"at":{"i":4},"vars":{"builder":"abc"},"note":"Read 'c' and append it. The builder holds 'abc'."}]}
```

```trace
{"cells":["g","o","_","f","a","r","_","n","o","w"],"pointers":["i"],"steps":[{"at":{"i":7},"vars":{"word":"now","builder":"now"},"note":"Found the word 'now'. The builder was empty, so no separator is written. The builder holds 'now'."},{"at":{"i":3},"vars":{"word":"far","builder":"now far"},"note":"Found the word 'far'. The builder is not empty, so a separator comes first. The builder holds 'now far'."},{"at":{"i":0},"vars":{"word":"go","builder":"now far go"},"note":"Found the word 'go'. The builder is not empty, so a separator comes first. The builder holds 'now far go'."}]}
```

<!-- stage: code -->
### Append Only, Separator First

```java
static String removeSpaces(String s) {
    StringBuilder out = new StringBuilder(s.length());
    for (int i = 0; i < s.length(); i++) {
        char c = s.charAt(i);
        if (c != ' ') out.append(c);
    }
    return out.toString();
}

static String reverseWords(String s) {
    StringBuilder out = new StringBuilder();
    int i = s.length() - 1;
    while (i >= 0) {
        while (i >= 0 && s.charAt(i) == ' ') i--;             // skip spaces between words
        if (i < 0) break;
        int end = i;
        while (i >= 0 && s.charAt(i) != ' ') i--;
        if (out.length() > 0) out.append(' ');                // the loop owns the separator
        out.append(s, i + 1, end + 1);
    }
    return out.toString();
}

static String zigzag(String s, int numRows) {
    if (numRows == 1 || numRows >= s.length()) return s;
    StringBuilder[] rows = new StringBuilder[numRows];
    for (int r = 0; r < numRows; r++) rows[r] = new StringBuilder();
    int row = 0, step = 1;
    for (int i = 0; i < s.length(); i++) {
        rows[row].append(s.charAt(i));
        if (row == 0) step = 1;
        else if (row == numRows - 1) step = -1;
        row += step;
    }
    StringBuilder out = new StringBuilder(s.length());
    for (StringBuilder r : rows) out.append(r);
    return out.toString();
}
```

Each method appends each character a constant number of times, so the time is O(n), and the builders hold O(n) characters in total. The pitfalls are in the details. Appending an `int` appends its digits, so arithmetic on a `char` needs a cast before `append`. And `append(CharSequence, start, end)` takes an end that is exclusive, which the word copy uses.

<!-- stage: applicability -->
### When The Output Grows At Its End

Use a builder whenever the output is constructed piece by piece, and each piece goes at the end. The invariant is that the builder holds the completed prefix. Decide who writes the separator and write it before every item except the first. Create the final string once.

The false friend is `insert(0, ...)`, which looks like the natural way to reverse. It places the new character at the front and moves all of the existing ones, so a loop of insertions is quadratic. Another false friend is `String.join` or `split` for a small piece of work, which is fine for clarity when the input is short, but allocates arrays of intermediate strings that the explicit scan never needs. And `+` inside a loop is the most common cause of a slow string method.

In Java, `+` outside loops is fine, and the compiler turns a single expression into an efficient concatenation. Pre-size the builder when the output length is known. Use `char[]` when you know the exact size and want to fill positions directly. If several independent outputs are being built, give each its own builder instead of sharing one and trying to track offsets.

<!-- stage: exercises -->
### Exercises

#### [Build] Remove Spaces (Author exercise)
<!-- id: st-remove-spaces -->

**Prerequisites.** The indexed-scan lesson; the output contract from Chapter 00.

**Problem.** Given a string `s`, return the string obtained by deleting every space character. All other characters keep their order.

**Constraints.** 0 <= s.length() <= 2 * 10^5 and all characters are ASCII. Do not build the result with `+` in a loop.

**Example 1.** Input `s = "a b  c "`, output `"abc"`.

**Example 2.** Input `s = ""`, output `""`, since there is nothing to keep.

**Hint.** What holds the part of the output that is already final? Where is each new character placed?

**Changed decision.** First rung: a builder replaces repeated concatenation, so each kept character costs one append.

#### [Vary] Reverse Words in a String (LeetCode 151)
<!-- id: st-reverse-words -->

**Prerequisites.** The remove-spaces exercise above.

**Problem.** Given a string that may have leading, trailing and repeated spaces, return its words in reverse order, joined by single spaces, with no leading or trailing space.

**Constraints.** 1 <= s.length() <= 10^4 and `s` contains at least one word. Do not use `insert(0, ...)`.

**Example 1.** Input `s = "  the sky  is blue "`, output `"blue is sky the"`.

**Example 2.** Input `s = "solo"`, output `"solo"`, since a single word has nothing to reverse.

**Hint.** From which end do you read to get the words in the order you want? Which step writes the space between two words, and when does it stay silent?

**Changed decision.** The output is made of words, so the loop must own the separator and write it before every word except the first.

#### [Boundary] Empty Result (Author exercise)
<!-- id: st-empty-result -->

**Prerequisites.** The two exercises above.

**Problem.** Run the reverse-words method on a string made only of spaces and show that the result is the empty string, with no trailing separator. Also show why a version that writes a space after every word and removes the last one fails on that input.

**Constraints.** The input may contain no words at all. The method must not throw.

**Example 1.** Input `s = "   "`, output `""`.

**Example 2.** Input `s = " "`, output `""`, and the delete-the-last-separator version throws.

**Hint.** What does the delete-the-last-separator step try to remove when nothing was written? Which test makes the separator appear only after something exists?

**Changed decision.** The tests target the input with no items, where only the separator-first rule gives a legal empty result.

#### [Recognize] Zigzag Conversion (LeetCode 6)
<!-- id: st-zigzag -->

**Prerequisites.** All three exercises above.

**Problem.** Write a string in a zigzag pattern on a given number of rows, going down the rows and then diagonally back up, and then read it row by row. Return the string produced by reading the rows from top to bottom.

**Constraints.** 1 <= s.length() <= 1000, `s` has ASCII letters, and 1 <= numRows <= 1000. Use one builder per row.

**Example 1.** Input `s = "ABCDEFGHIJKLM", numRows = 3`, output `"AEIMBDFHJLCGK"`.

**Example 2.** Input `s = "ABC", numRows = 1`, output `"ABC"`, because one row reads the string as it is.

**Hint.** Which row does each character belong to, and when does the direction change? What happens to the direction when there is only one row?

**Changed decision.** The output is several independent prefixes, one per row, each owned by its own builder and joined at the end.
