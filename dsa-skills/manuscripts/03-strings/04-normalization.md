<!-- lesson-kind: standard -->
<!-- lesson-id: normalization -->
## Normalization

<!-- stage: context -->
### Cards That Mean The Same Author

A small library keeps its catalog on index cards, and the cards were typed by many volunteers over many years. One card says `Smith, J.`, another says `smith j`, and a third says `SMITH J`. A patron asks whether the library holds two books by the same author, and the librarian has to decide which cards describe the same person.

She cannot compare the cards as they are, because the capital letters and commas differ although the author does not. So she decides what counts. The letters count and the case does not, and commas, periods and extra spaces are decoration. She mentally rewrites every card into the same plain form, and cards that look identical in that form belong to one author. Everything depends on deciding, once and clearly, which differences matter.

<!-- stage: naive -->
### Clean Both Cards Inside Every Comparison

A direct way to compare a stack of cards is to compare every pair, and to clean both cards each time they are compared.

```java
static boolean sameCard(String a, String b) {
    StringBuilder x = new StringBuilder(), y = new StringBuilder();
    for (char c : a.toCharArray()) if (Character.isLetter(c)) x.append(Character.toLowerCase(c));
    for (char c : b.toCharArray()) if (Character.isLetter(c)) y.append(Character.toLowerCase(c));
    return x.toString().equals(y.toString());
}

static int matchingPairs(String[] cards) {
    int pairs = 0;
    for (int i = 0; i < cards.length; i++)
        for (int j = i + 1; j < cards.length; j++)
            if (sameCard(cards[i], cards[j])) pairs++;
    return pairs;
}
```

It is correct. For `{"Smith, J.", "smith j", "Ng"}` it finds one matching pair, the first two cards.

<!-- stage: bottleneck -->
### Every Card Is Cleaned Repeatedly

With `k` cards of length about `L`, the nested loops make `k * (k - 1) / 2` comparisons, and each cleans two cards, so the cleaning work is O(k^2 * L). A card at position 0 is cleaned `k - 1` times, once for each partner. With 2,000 cards of 50 characters that is about 200 million character steps, and the number of comparisons alone grows with the square of the stack.

The cleaning of one card does not depend on which other card it is compared with. Its plain form is a property of the card itself. Computing that form once, per card, costs O(k * L) in total, and every later comparison then reads two finished strings. The expensive part was repeated work, not the comparison.

<!-- stage: insight -->
### Rewrite Each Input Into One Plain Form

A **canonical form** is a single chosen representation, such that two inputs are considered equivalent exactly when their canonical forms are equal. Normalization is the act of rewriting an input into it. The rules for the rewrite come from the problem's **equality contract**, the statement of which differences are meaningful. If case and punctuation do not matter, the canonical form is the letters in one case with the rest removed.

The invariant is that the rewrite changes only what the contract calls irrelevant and keeps everything it calls relevant, in the original order. Throwing away a relevant character merges inputs that should differ, and keeping an irrelevant one splits inputs that should match. The rewrite is a single scan with a builder, so one normalization costs O(L) time, and doing it once per input removes the repeated cleaning.

<!-- names: canonical form, equality contract, group size -->

Not every normalization removes characters. Some regroup them. A license key such as `x7-k-p-02-q9` has dashes in arbitrary places. The contract says the dashes are decoration, letters become uppercase, and the key is rewritten into groups of a fixed **group size** separated by dashes, where only the first group may be shorter. Because the short group is at the front, the rewrite should be built from the end, where the groups are full, and reversed once at the end. Starting from the front would need to know the total length first, or would insert at the front.

Some questions normalize into a shape and not into a string. To decide whether the capitals in a word follow one of three allowed patterns, count the capitals and note whether the first letter is one. The word is allowed if there are none, if all letters are capitals, or if there is exactly one and it comes first. The count is the normalized form.

<!-- stage: variables -->
### The Reader, The Builder And The Counter

The scan keeps an index `i` over the input and a `StringBuilder` for the canonical form, which holds the completed prefix. For case folding there is nothing else to remember. For regrouping, a counter `groupLen` counts characters in the group being built, and when it equals the group size the next character is preceded by a dash. For the capital pattern, a counter `upper` counts capitals and the first character is tested separately. Decide the character test from the contract, such as an ASCII letter range, before writing the loop.

<!-- stage: trace -->
### A Plain Form And A Regrouped Key

Take the card `A-b, C!`, with seven characters. The `A` is a letter, so `a` is appended. The dash is decoration and is skipped. The `b` is appended as it is. The comma and the space are skipped. The `C` becomes `c`. The exclamation mark is skipped. The canonical form is `abc`. Each character was read once and the builder never copied its contents.

Now regroup the key `x7-k-p-02-q9` into groups of three. The scan goes from the end. The `9` and `Q` and the `2` fill the first group, so the builder holds `9Q2`. The next kept character, `0`, finds the group full, so a dash is appended first, giving `9Q2-0`. Then `P` and `K` complete the second group. The `7` finds that group full again, so another dash is written, then `7` and `X`. The builder holds `9Q2-0PK-7X`, and reversing it once gives `X7-KP0-2Q9`. The step to study is the one where a dash is written because the group is full and another character is waiting.

```trace
{"cells":["A","-","b",","," ","C","!"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"builder":"a"},"note":"Read 'A', a letter. Append 'a'. The builder holds 'a'."},{"at":{"i":1},"vars":{"builder":"a"},"note":"Read '-', which is decoration, and skip it. The builder holds 'a'."},{"at":{"i":2},"vars":{"builder":"ab"},"note":"Read 'b', a letter. Append 'b'. The builder holds 'ab'."},{"at":{"i":3},"vars":{"builder":"ab"},"note":"Read ',', which is decoration, and skip it. The builder holds 'ab'."},{"at":{"i":4},"vars":{"builder":"ab"},"note":"Read ' ', which is decoration, and skip it. The builder holds 'ab'."},{"at":{"i":5},"vars":{"builder":"abc"},"note":"Read 'C', a letter. Append 'c'. The builder holds 'abc'."},{"at":{"i":6},"vars":{"builder":"abc"},"note":"Read '!', which is decoration, and skip it. The builder holds 'abc'."}]}
```

```trace
{"cells":["x","7","-","k","-","p","-","0","2","-","q","9"],"pointers":["i"],"steps":[{"at":{"i":11},"vars":{"builder":"9","groupLen":1},"note":"Index 11 holds '9'. Append '9'. The builder holds '9'."},{"at":{"i":10},"vars":{"builder":"9Q","groupLen":2},"note":"Index 10 holds 'q'. Append 'Q'. The builder holds '9Q'."},{"at":{"i":9},"vars":{"builder":"9Q","groupLen":2},"note":"Index 9 holds a dash, which is decoration, so skip it."},{"at":{"i":8},"vars":{"builder":"9Q2","groupLen":3},"note":"Index 8 holds '2'. Append '2'. The builder holds '9Q2'."},{"at":{"i":7},"vars":{"builder":"9Q2-0","groupLen":1},"note":"Index 7 holds '0'. The group was full, so a dash is written first. Append '0'. The builder holds '9Q2-0'."},{"at":{"i":6},"vars":{"builder":"9Q2-0","groupLen":1},"note":"Index 6 holds a dash, which is decoration, so skip it."},{"at":{"i":5},"vars":{"builder":"9Q2-0P","groupLen":2},"note":"Index 5 holds 'p'. Append 'P'. The builder holds '9Q2-0P'."},{"at":{"i":4},"vars":{"builder":"9Q2-0P","groupLen":2},"note":"Index 4 holds a dash, which is decoration, so skip it."},{"at":{"i":3},"vars":{"builder":"9Q2-0PK","groupLen":3},"note":"Index 3 holds 'k'. Append 'K'. The builder holds '9Q2-0PK'."},{"at":{"i":2},"vars":{"builder":"9Q2-0PK","groupLen":3},"note":"Index 2 holds a dash, which is decoration, so skip it."},{"at":{"i":1},"vars":{"builder":"9Q2-0PK-7","groupLen":1},"note":"Index 1 holds '7'. The group was full, so a dash is written first. Append '7'. The builder holds '9Q2-0PK-7'."},{"at":{"i":0},"vars":{"builder":"9Q2-0PK-7X","groupLen":2},"note":"Index 0 holds 'x'. Append 'X'. The builder holds '9Q2-0PK-7X'. Reversing once gives 'X7-KP0-2Q9'."}]}
```

<!-- stage: code -->
### Fold, Count And Regroup

```java
static String lowercaseLetters(String s) {
    StringBuilder out = new StringBuilder();
    for (int i = 0; i < s.length(); i++) {
        char c = s.charAt(i);
        if (c >= 'A' && c <= 'Z') out.append((char) (c + ('a' - 'A')));
        else if (c >= 'a' && c <= 'z') out.append(c);
    }
    return out.toString();
}

static boolean detectCapital(String word) {
    int upper = 0;
    for (int i = 0; i < word.length(); i++) if (word.charAt(i) >= 'A' && word.charAt(i) <= 'Z') upper++;
    boolean firstUpper = word.length() > 0 && word.charAt(0) >= 'A' && word.charAt(0) <= 'Z';
    return upper == 0 || upper == word.length() || (upper == 1 && firstUpper);
}

static String licenseKey(String s, int k) {
    StringBuilder out = new StringBuilder();
    int groupLen = 0;
    for (int i = s.length() - 1; i >= 0; i--) {
        char c = s.charAt(i);
        if (c == '-') continue;
        if (groupLen == k) { out.append('-'); groupLen = 0; }
        out.append(Character.toUpperCase(c));
        groupLen++;
    }
    return out.reverse().toString();
}
```

Each method makes one pass and keeps a constant number of counters beside its output, so the time is O(n) and the extra space is the builder. The ASCII range tests are chosen on purpose. `Character.isLetter` accepts letters of every script, and `String.toLowerCase()` without a locale argument uses the default locale, which changes the result for some languages. Using `Locale.ROOT` or explicit ranges makes the result the same everywhere.

<!-- stage: applicability -->
### When Equivalent Inputs Look Different

Use normalization when inputs that should be treated as equal differ only in case, separators or layout, and the contract says exactly which differences are irrelevant. The invariant is that the canonical form keeps every relevant character in order and removes or rewrites only the irrelevant ones. Normalize each input once, then compare or count.

The false friend is a canonical form made by sorting the characters, which also puts anagrams together but changes the equality contract from "same text" to "same multiset of letters". That signature belongs to a later chapter once sorting is taught. A second false friend is a normalization that is too eager, such as removing digits from a license key, which merges keys that should differ. A third is normalizing in the wrong direction: a regrouping that starts from the front leaves the short group at the wrong end.

In Java, give case conversion a locale or avoid it: `toLowerCase(Locale.ROOT)` or explicit ASCII arithmetic. Decide whether an empty canonical form is legal and what it means. Two inputs with nothing relevant normalize to the same empty string, so the contract should say whether they count as equal.

<!-- stage: exercises -->
### Exercises

#### [Build] Lowercase Letters Only (Author exercise)
<!-- id: st-lowercase-letters -->

**Prerequisites.** The safe-construction lesson; the character test from the first lesson of this chapter.

**Problem.** Given a string, return a string containing only its ASCII letters, each converted to lowercase and kept in the original order. Digits, spaces and punctuation are dropped.

**Constraints.** 0 <= s.length() <= 10^5 and all characters are ASCII. Use a builder and no regular expression.

**Example 1.** Input `s = "A-b, C!"`, output `"abc"`.

**Example 2.** Input `s = "x9 Y"`, output `"xy"`.

**Hint.** Which characters are relevant under this contract, and which differences are decoration? Where do the kept characters go?

**Changed decision.** First rung: one pass rewrites the input into a canonical form that keeps only the relevant characters.

#### [Vary] Detect Capital (LeetCode 520)
<!-- id: st-detect-capital -->

**Prerequisites.** The lowercase-letters exercise above.

**Problem.** A word uses capitals correctly if all its letters are capitals, or none is a capital, or only its first letter is a capital. Given a word of ASCII letters, return whether it uses capitals correctly.

**Constraints.** 1 <= word.length() <= 100 and `word` has only ASCII letters. Do not build a second string.

**Example 1.** Input `word = "Zebra"`, output true.

**Example 2.** Input `word = "zEbra"`, output false.

**Hint.** What two facts about the capitals are enough to decide? Which three values of the count allow the word?

**Changed decision.** The normal form is a shape, the count of capitals and the position of the first, and not a rewritten string.

#### [Boundary] Punctuation Only (Author exercise)
<!-- id: st-punctuation-only -->

**Prerequisites.** The two exercises above.

**Problem.** Run the lowercase-letters normalization on strings with no letters and show that the result is the empty string, which is a legal canonical form. Then decide whether two such cards count as equal, and state the contract that makes your answer correct.

**Constraints.** The input may contain no letters at all. The method must not throw and must not return null.

**Example 1.** Input `s = "?!"`, output `""`.

**Example 2.** Input `s = " ,.- "`, output `""`, and two such strings have equal canonical forms.

**Hint.** What does the builder hold if nothing is appended? Is an empty canonical form a mistake or a consequence of the contract?

**Changed decision.** The tests target the input with nothing relevant, where the empty result is the correct normal form and the contract decides equality.

#### [Recognize] License Key Formatting (LeetCode 482)
<!-- id: st-license-key -->

**Prerequisites.** All three exercises above.

**Problem.** A license key is a string of letters, digits and dashes. Rewrite it so that dashes are removed, every letter is uppercase, and the characters are grouped by `k` with a single dash between groups. Only the first group may be shorter than `k`, and it must contain at least one character unless the key is empty.

**Constraints.** 1 <= s.length() <= 10^5, 1 <= k <= 10^4, and `s` consists of letters, digits and dashes. Do not insert at the front of a builder.

**Example 1.** Input `s = "x7-k-p-02-q9", k = 3`, output `"X7-KP0-2Q9"`.

**Example 2.** Input `s = "---", k = 2`, output `""`, since no character remains.

**Hint.** Which end of the string tells you where the full groups are? How can you build in that direction without inserting at the front?

**Changed decision.** The normalization regroups characters, and the group boundaries are counted from the end of the key.
