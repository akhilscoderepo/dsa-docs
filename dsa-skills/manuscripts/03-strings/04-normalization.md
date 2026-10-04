<!-- lesson-kind: standard -->
<!-- lesson-id: normalization -->
## Normalize Before Comparing

<!-- stage: context -->
### Two Spellings Of One Product Code

A warehouse system stores product codes. A picker types `ab-12` on one screen, and a label printer prints `AB 12` for the same item. The system compares the two strings, finds them different and reports a missing item. A person sees the same code in both cases at a glance.

The comparison treats a capital letter, a dash and a space as meaningful, although the business treats them as noise. The gap between what the strings say and what the people mean causes the false alarm. The question is how to compare two strings by what they mean, with a rule that a loop applies to every character.

<!-- stage: naive -->
### Lowercase Both And Compare

The obvious fix lowercases both strings and then compares them.

```java
static boolean sameCode(String a, String b) {
    return a.toLowerCase().equals(b.toLowerCase());
}
```

The method returns true for `"Ab12"` and `"aB12"`, so the capital letters stop causing false alarms. It returns false for `"ab-12"` and `"AB 12"`, because a dash and a space still differ. Each call to `toLowerCase` also allocates a full copy of its string.

<!-- stage: bottleneck -->
### One Rule Handles Only One Difference

```predict
The method lowercases both codes and compares them. What does it return for "ab-12" and "AB 12", what should it return, and which step is missing?

It returns false, but the business meaning says true. The missing step removes the characters that carry no meaning, which are the dash and the space. After both steps, each code holds only the letters and digits in lowercase, and the two strings become equal.
```

Lowercasing fixes one kind of difference. The codes differ in a second way, and no comparison method on the original strings can fix it. The program has to turn each input into a form where the unimportant differences are gone, and then compare those forms. Building the form costs one pass over each input, which is O(n + m) time for two codes of lengths n and m. The forms need O(n + m) extra space. The remaining question is how to choose the form so that no real difference disappears with the noise.

<!-- stage: insight -->
### Convert Both Inputs To One Standard Form

**Normalization** converts every input to a standard representation, so that inputs with the same meaning produce identical output. After normalization, a plain `equals` call answers the question.

#### Write The Equality Rule First

The rule says when two inputs are **equivalent**. For product codes, two codes are equivalent when they hold the same letters and digits in the same order, ignoring letter case and every other character. This sentence is the **contract** of the normalization. It decides which differences count as noise and which count as real. The loop is written only after the contract is clear.

<!-- names: canonical form, equivalent, contract -->

#### Build The Canonical Form In One Pass

The **canonical form** of an input is the one string that all equivalent inputs share. For product codes, the canonical form holds the lowercase letters and the digits, in order. A loop with an index `i` and a builder produces it. A letter from `'A'` to `'Z'` is lowercased and appended. A lowercase letter or a digit is appended unchanged. Every other character is skipped.

#### Normalize Both Sides The Same Way

The method must apply one function to both inputs. If the two inputs used slightly different rules, equivalent codes would produce different forms. The invariant is that the builder always holds the canonical form of the characters read so far. Two inputs are equivalent exactly when their canonical forms are equal.

#### An Empty Form Is A Legal Answer

An input made only of noise, such as `"?!"`, normalizes to the empty string. The empty string is a valid canonical form. Two noise-only inputs are equivalent under the contract, so the method must return true for them and must not reject empty results.

<!-- stage: variables -->
### Builder, Index And Character Class

Normalization needs three values, and each has a clear rule for when it changes.

- **out** holds the canonical form of the characters read so far and only grows at its end.
- **i** marks the position of the next character to classify and advances by one each round.
- **character class** is one of three cases: an uppercase letter, a kept character (a lowercase letter or a digit), or noise. Each iteration decides the class of the character at `i`.

<!-- stage: trace -->
### Normalizing Two Inputs

#### A Code With Capitals And A Dash

Take `s = "A-b 1"`. The pointer `i` marks the character under test. In the trace below, `␣` shows a space. At `i = 0` the capital `A` becomes `a`, so the builder holds `a`. At `i = 1` the dash is noise and the builder stays unchanged. At `i = 2` the lowercase `b` is appended as it is. At `i = 3` the space is noise. At `i = 4` the digit `1` is appended. The canonical form is `ab1`.

#### An Input With No Letters Or Digits

Now take `s = "?!"`. Both characters are noise, so the builder stays empty. The loop ends with the empty string as the canonical form. Two such inputs both produce the empty string, so the comparison reports them as equivalent.

#### Stepping Through Both Inputs

```trace
{"cells":["A","-","b","\u2423","1"],"pointers":["i"],"steps":[{"at":{"i":-1},"vars":{"out":""},"note":"Start: the builder is empty."},{"at":{"i":0},"vars":{"out":"a"},"note":"Index 0 holds the capital A, so the loop appends a. The builder holds a."},{"at":{"i":1},"vars":{"out":"a"},"note":"Index 1 holds '-', which is noise, so the builder stays unchanged. The builder holds a."},{"at":{"i":2},"vars":{"out":"ab"},"note":"Index 2 holds 'b', so the loop appends it unchanged. The builder holds ab."},{"at":{"i":3},"vars":{"out":"ab"},"note":"Index 3 holds the space, which is noise, so the builder stays unchanged. The builder holds ab."},{"at":{"i":4},"vars":{"out":"ab1"},"note":"Index 4 holds '1', so the loop appends it unchanged. The builder holds ab1."},{"at":{"i":5},"vars":{"out":"ab1"},"note":"The index equals the length, so the canonical form is ab1."}]}
```

```trace
{"cells":["?","!"],"pointers":["i"],"steps":[{"at":{"i":-1},"vars":{"out":""},"note":"Start: the builder is empty."},{"at":{"i":0},"vars":{"out":""},"note":"Index 0 holds '?', which is noise, so the builder stays unchanged. The builder is empty."},{"at":{"i":1},"vars":{"out":""},"note":"Index 1 holds '!', which is noise, so the builder stays unchanged. The builder is empty."},{"at":{"i":2},"vars":{"out":""},"note":"The index equals the length, so the canonical form is the empty string."}]}
```

<!-- stage: code -->
### Normalize Then Compare

#### A Normalizer And A Comparison

```java
static String normalize(String s) {
    StringBuilder out = new StringBuilder(s.length());
    for (int i = 0; i < s.length(); i++) {
        char c = s.charAt(i);
        if (c >= 'A' && c <= 'Z') {
            out.append((char) (c + ('a' - 'A')));
        } else if ((c >= 'a' && c <= 'z') || (c >= '0' && c <= '9')) {
            out.append(c);
        }
    }
    return out.toString();
}

static boolean sameCode(String a, String b) {
    return normalize(a).equals(normalize(b));
}
```

#### What The Methods Cost

The normalizer reads each character once and appends at most once, so it runs in O(n) time and uses O(n) space for the output. The comparison normalizes both inputs and then compares them, so it runs in O(n + m) time and uses O(n + m) space. The range tests keep the contract to ASCII letters and digits, so no locale changes the result.

<!-- stage: applicability -->
### Choosing What To Keep Or Drop

#### Look For A Meaning Gap

Use normalization when two strings differ in ways that the problem calls irrelevant, such as capital letters, separators or padding. Write down the contract, then write the loop. The invariant is that the normalized output of any prefix is the canonical form of that prefix. A good normalizer maps equivalent inputs to one form and keeps every difference that the problem still treats as real.

#### Dropping Too Much Is A Risk

A normalizer that removes too much merges inputs that should stay different. A rule that also drops digits turns `"A1"` and `"A2"` into the same form, and the system reports two different items as one. Check each dropped character class against the contract before writing the loop.

#### Sorting As A Signature Is A False Friend

A false friend is a technique that looks like normalization and needs tools that the reader does not have yet. Sorting the characters of a string produces a form that is shared by all rearrangements, which looks like a canonical form for anagrams. That form depends on sorting, which a later chapter teaches. This chapter normalizes only with one pass that keeps the order.

#### Java Details That Cause Failures

The call `toLowerCase()` without an argument depends on the default locale of the machine. Case mapping outside ASCII can also change the length of a string, because `"ß".toUpperCase()` produces two characters. The operator `==` on two strings compares references, so `new String("a") == "a"` is false. Always compare normalized strings with `equals`.

<!-- stage: exercises -->
### Exercises

#### [Build] Lowercase Letters Only (Author exercise)
<!-- id: st-letters-only -->

**Prerequisites.** The normalizer loop and the character classes from this lesson.

**Problem.** Let `s` be a string. Return a string that holds, in their original order, the ASCII letters of `s` converted to lowercase. Every other character is dropped.

**Constraints.** The limits are:
- **Length** satisfies `0 <= s.length() <= 10^5`.
- **Letters** are the characters `'A'` to `'Z'` and `'a'` to `'z'` only.
- **Answer** is a new string; `s` does not change.
- **Method** is a loop that appends to a `StringBuilder`.

**Example 1.** Input `s = "A-b c!"`, output `"abc"`.

**Example 2.** Input `s = "2024"`, output `""`, because no letter exists.

**Hint.** Which characters does the loop lowercase, which does it keep as they are, and which does it skip?

**Changed decision.** Basic case: the loop keeps one character class and converts a second class on the way in.

#### [Vary] Detect Capital (LeetCode 520)
<!-- id: st-detect-capital -->

**Prerequisites.** The normalizer above.

**Problem.** Let `word` be a string of English letters. The capital usage of `word` is correct when one of three forms holds. In the first form, every letter is lowercase. In the second form, every letter is uppercase. In the third form, only the first letter is uppercase. Return true when the capital usage is correct.

**Constraints.** The limits are:
- **Length** satisfies `1 <= word.length() <= 100`.
- **Characters** are the letters `'A'` to `'Z'` and `'a'` to `'z'`.
- **Single letter** is correct in either case.
- **Method** builds each of the three allowed forms from the letters of `word` and compares `word` with them.

**Example 1.** Input `word = "gRaph"`, output false.

**Example 2.** Input `word = "Graph"`, output true.

**Hint.** Which three strings can `word` equal when its capitals are correct, and how does the loop build each one from the same letters?

**Changed decision.** Normalization produces three allowed forms, and the answer is whether the input equals any one of them.

#### [Boundary] Punctuation Only (Author exercise)
<!-- id: st-punctuation-only -->

**Prerequisites.** The two exercises above and the empty canonical form from this lesson.

**Problem.** Let `a` and `b` be strings. Return true when the lowercase letters of `a` in order equal the lowercase letters of `b` in order. Uppercase letters count as their lowercase forms, and every other character is ignored.

**Constraints.** The limits are:
- **Length** satisfies `0 <= a.length(), b.length() <= 10^5`.
- **Letters** are the characters `'A'` to `'Z'` and `'a'` to `'z'`.
- **Empty form** is legal, so two strings with no letters are equal.
- **Mutation** does not occur.

**Example 1.** Input `a = "Ab,c"`, `b = "a BC"`, output true.

**Example 2.** Input `a = "?!"`, `b = ""`, output true, because both strings normalize to the empty string.

**Hint.** What does the normalizer return for an input with no letters, and does the comparison need a special case for it?

**Changed decision.** The normalized result may be empty, and the empty result must count as a valid form.

#### [Recognize] License Key Formatting (LeetCode 482)
<!-- id: st-license-key -->

**Prerequisites.** All three exercises above and the reverse-by-append habit from the StringBuilder lesson.

**Problem.** Let `s` be a string of letters, digits and dashes, and let `k` be a positive integer. Remove the dashes and convert the letters to uppercase. Then split the remaining characters into groups separated by single dashes. Every group holds exactly `k` characters, except that the first group may hold fewer, and it holds at least one character. Return the formatted key, or the empty string when no character remains.

**Constraints.** The limits are:
- **Length** satisfies `1 <= s.length() <= 10^5`.
- **Characters** are English letters, digits and `'-'`.
- **Group size** satisfies `1 <= k <= 10^4`.
- **Dashes** in the output appear only between groups.

**Example 1.** Input `s = "x1-k9"`, `k = 3`, output `"X-1K9"`.

**Example 2.** Input `s = "--"`, `k = 2`, output `""`, because no character remains.

**Hint.** Groups fill from the right end, so which direction should the loop read, and how does the builder end up in the right order?

**Changed decision.** The output contract groups the normalized characters from the right, so the loop reads backward and reverses once at the end.
