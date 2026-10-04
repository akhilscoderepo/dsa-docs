<!-- lesson-kind: standard -->
<!-- lesson-id: safe-construction -->
## Build Strings With StringBuilder

<!-- stage: context -->
### An Export That Slows As It Grows

A reporting tool writes one line of comma-separated values for every day in a month, then one for every day in a year. The month finishes in a blink. The year takes seconds, and a ten-year export takes minutes. The loop that builds the text has no nested loop and no expensive call, so the slowdown looks impossible.

The loop runs the line `result = result + piece` once per value. Java strings never change after creation, so every such line builds a brand new string. The question here is how a program builds a long output one piece at a time, so that each piece costs a constant amount of work and no stray comma ends the line.

<!-- stage: naive -->
### Adding Each Piece To The Result

The direct answer starts with an empty string and adds each number and a comma with the `+` operator.

```java
static String joinNumbers(int[] a) {
    String result = "";
    for (int i = 0; i < a.length; i++) {
        result = result + a[i] + ",";
    }
    return result;
}
```

On `{3, 1, 4}` the method returns `"3,1,4,"`. The text ends with a comma that the caller must cut off. On an empty array the method returns `""`, which is correct. The code is short, and every number lands in the right place.

<!-- stage: bottleneck -->
### Every Addition Copies The Whole Result

```predict
The loop adds a one-digit number and a comma to the result n times. After step k the result holds about 2k characters. Roughly how many characters does the loop copy in total, as a function of n?

Each addition creates a new string and copies all earlier characters into it. Step k copies about 2k characters, so the total is about 2 * (1 + 2 + ... + n), which is n squared plus n. The cost grows as O(n^2).
```

The loop looks linear, because it runs n times and each pass does one addition. The hidden cost sits inside the addition. A `String` cannot grow, so `result + a[i] + ","` allocates a new array, copies every old character into it and copies the new characters after them. The old string becomes garbage. For n numbers the total copying is O(n^2) characters, and the garbage grows in the same proportion. A long export slows down for exactly this reason. A correct method appends in amortized constant time per character, which gives O(n) in total. It also needs a rule that places the commas between the numbers and not after the last one.

<!-- stage: insight -->
### Keep One Buffer For The Finished Output

The class `StringBuilder` holds a growable array of characters. A call to `append` writes the new characters at the end of the same array, and the array grows by a multiplicative factor when it fills up. The array copies each character only a constant number of times on average, so appending n characters in total costs O(n) time.

#### The Builder Holds The Completed Prefix

The loop keeps one invariant. After the iteration for index `i`, the builder holds exactly the completed prefix of the output, which is the text for the elements before `i + 1`. Nothing in the builder is provisional, and the loop never edits earlier text. The call `out.toString()` runs once at the end and creates the final `String` with one copy.

<!-- names: StringBuilder, completed prefix, separator -->

#### Who Owns The Separator

A **separator** is a character placed between two pieces and never at either end. A simple rule keeps it correct. The piece at index `i` owns the separator in front of it, so the loop writes the separator when `i > 0` and then writes the piece. The first piece writes no separator, and the last piece leaves no trailing one. An empty input never enters the loop, so it produces the empty string without a special case.

#### Operations That Look Cheap And Are Not

The call `out.insert(0, text)` places text at the front. It shifts every existing character to the right, so it costs time proportional to the current length. Building a reversed string by inserting at index 0 repeats that shift n times and costs O(n^2) in total. The same result needs appends in reverse order, or one call to `out.reverse()`.

<!-- stage: variables -->
### Builder, Index And Separator Rule

Three values carry the whole loop, and the loop updates each at a set moment.

- **out** holds the completed prefix of the output and only grows at its end.
- **i** holds the index of the next element to write and grows by one per iteration.
- **separator rule** is the test `i > 0`, which decides whether a comma comes before the element at `i`.

<!-- stage: trace -->
### Joining Two Arrays Of Numbers

#### Three Numbers

Take `a = {3, 1, 4}`. The pointer `i` marks the element being written. At `i = 0` the loop writes `3` and no comma, so the builder holds `3`. At `i = 1` the loop writes a comma and then `1`, so the builder holds `3,1`. At `i = 2` it writes a comma and then `4`, so the builder holds `3,1,4`. The loop ends with no trailing comma.

#### A Number With Two Digits

Now take `a = {9, 15}`. At `i = 0` the builder receives `9`. At `i = 1` it receives a comma and then the two characters of `15`, so the builder holds `9,15`. One element can add several characters in one step, and the separator rule does not change.

#### Stepping Through Both Arrays

```trace
{"cells":["3","1","4"],"pointers":["i"],"steps":[{"at":{"i":-1},"vars":{"out":""},"note":"Start: the builder is empty."},{"at":{"i":0},"vars":{"out":"3"},"note":"Index 0 writes 3 and no comma, because it is the first element. The builder holds 3."},{"at":{"i":1},"vars":{"out":"3,1"},"note":"Index 1 writes a comma and then 1. The builder holds 3,1."},{"at":{"i":2},"vars":{"out":"3,1,4"},"note":"Index 2 writes a comma and then 4. The builder holds 3,1,4."},{"at":{"i":3},"vars":{"out":"3,1,4"},"note":"The index equals the length, so the loop ends with 3,1,4 and no trailing comma."}]}
```

```trace
{"cells":["9","15"],"pointers":["i"],"steps":[{"at":{"i":-1},"vars":{"out":""},"note":"Start: the builder is empty."},{"at":{"i":0},"vars":{"out":"9"},"note":"Index 0 writes 9 and no comma, because it is the first element. The builder holds 9."},{"at":{"i":1},"vars":{"out":"9,15"},"note":"Index 1 writes a comma and then 15. The builder holds 9,15."},{"at":{"i":2},"vars":{"out":"9,15"},"note":"The index equals the length, so the loop ends with 9,15 and no trailing comma."}]}
```

<!-- stage: code -->
### Appending Into One Buffer

#### The Join Loop And The Reverse Case

```java
static String joinNumbers(int[] a) {
    StringBuilder out = new StringBuilder();
    for (int i = 0; i < a.length; i++) {
        if (i > 0) {
            out.append(',');
        }
        out.append(a[i]);
    }
    return out.toString();
}

static String reverseText(String s) {
    StringBuilder out = new StringBuilder(s.length());
    for (int i = s.length() - 1; i >= 0; i--) {
        out.append(s.charAt(i));
    }
    return out.toString();
}
```

#### What Each Method Costs

Both methods run in O(n) time for n output characters and use O(n) space for the builder. The constructor argument `s.length()` in the second method reserves the final capacity once, so the array never grows. Reading the loop from the last index down to 0 gives the reversed order without any insert at the front.

<!-- stage: applicability -->
### Choosing A Builder

#### Look For Repeated Construction

Use a builder when a loop produces the output a piece at a time and the number of pieces depends on the input. Joining values, filtering characters, formatting lines and constructing rows all fit. The invariant of the pattern is that the builder always holds the completed prefix of the output and the loop only appends to it. A single addition of two or three strings outside a loop needs no builder.

#### Insert At The Front Is A False Friend

A false friend is a call that looks like the right tool and breaks the cost rule. The call `insert(0, ...)` looks like the natural way to prepend pieces, so a reversal written with it appears correct and passes small tests. It shifts the whole buffer on every call, so n calls cost O(n^2). Delete operations at the front behave the same way. A loop that needs the output in reverse order should either append in reverse order or append forward and call `reverse()` once.

#### Java Details That Cause Failures

The call `out.append('a' + 1)` appends the text `98`, because `'a' + 1` is an `int` and `append(int)` writes its decimal digits. A cast such as `(char) ('a' + 1)` appends `b`. A builder is not thread-safe and has no `equals` that compares text, so compare builders with `toString()` or `compareTo`. The constructor `new StringBuilder(n)` sets the capacity to n and the length to 0.

<!-- stage: exercises -->
### Exercises

#### [Build] Remove Spaces (Author exercise)
<!-- id: st-remove-spaces -->

**Prerequisites.** The builder loop and the completed prefix from this lesson.

**Problem.** Let `s` be a string. Return a string that holds the characters of `s` in their original order with every space character `' '` removed.

**Constraints.** The limits are:
- **Length** satisfies `0 <= s.length() <= 10^5`; the empty string is legal.
- **Characters** are any Java `char` values, and only `' '` is removed.
- **Method** uses a `StringBuilder` and no `+` inside the loop.
- **Mutation** does not occur; the method returns a new string.

**Example 1.** Input `s = "a b  c"`, output `"abc"`.

**Example 2.** Input `s = ""`, output `""`.

**Hint.** Which characters does the builder append, and which does the loop skip?

**Changed decision.** Basic case: the loop appends a character only when a test succeeds.

#### [Vary] Reverse Words In A String (LeetCode 151)
<!-- id: st-reverse-words -->

**Prerequisites.** The separator rule and the word start test from the previous lesson.

**Problem.** Let `s` be a string of letters, digits and spaces. A word is a maximal run of non-space characters. Return the words of `s` in reverse order, joined by exactly one space, with no space at the start or the end.

**Constraints.** The limits are:
- **Length** satisfies `1 <= s.length() <= 10^4`.
- **Characters** are English letters, digits and `' '`.
- **Words** exist, so `s` holds at least one non-space character.
- **Spaces** may repeat and may appear at both ends of `s`.

**Example 1.** Input `s = "  one  two three "`, output `"three two one"`.

**Example 2.** Input `s = "word"`, output `"word"`.

**Hint.** Which piece owns the single space in the output, and in which order does the loop append the stored words?

**Changed decision.** The loop collects whole words first and then writes them in reverse order with one owner for each separator.

#### [Boundary] Empty Result (Author exercise)
<!-- id: st-empty-result -->

**Prerequisites.** The two exercises above.

**Problem.** Let `s` be a string of lowercase letters and commas. A field is a maximal run of letters. Return the fields of `s` in their original order, joined by the character `'|'`. When `s` holds no field, return the empty string.

**Constraints.** The limits are:
- **Length** satisfies `0 <= s.length() <= 10^5`.
- **Characters** are lowercase English letters and `','`.
- **Commas** may repeat and may appear at both ends.
- **Output** has no `'|'` at the start or at the end.

**Example 1.** Input `s = "ab,,c"`, output `"ab|c"`.

**Example 2.** Input `s = ",,,"`, output `""`, because no field exists.

**Hint.** When does the loop know that a bar belongs in front of a letter, and what does the builder hold at that moment?

**Changed decision.** The separator depends on the builder content, so an input with no field produces no separator at all.

#### [Recognize] Zigzag Conversion (LeetCode 6)
<!-- id: st-zigzag -->

**Prerequisites.** All three exercises above.

**Problem.** Let `s` be a string and `numRows` a positive integer. Write the characters of `s` in order into `numRows` rows. Start at the top row, move down one row per character until the bottom row, then move up one row per character until the top row, and repeat. Return the characters of row 0, then row 1, and so on up to the last row, as one string.

**Constraints.** The limits are:
- **Length** satisfies `1 <= s.length() <= 1000`.
- **Characters** are English letters.
- **Rows** satisfy `1 <= numRows <= 1000`.
- **Single row** returns `s` unchanged when `numRows == 1`.

**Example 1.** Input `s = "ABCDEFGHIJ"`, `numRows = 4`, output `"AGBFHCEIDJ"`.

**Example 2.** Input `s = "ABC"`, `numRows = 5`, output `"ABC"`, because each row holds at most one character.

**Hint.** Which builder receives the character at index `i`, and when does the direction flip?

**Changed decision.** One builder per row replaces one builder for the whole output, and the direction changes at the first and last rows.
