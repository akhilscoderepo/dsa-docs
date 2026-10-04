<!-- lesson-kind: combination -->
<!-- lesson-id: strings-and-maps -->
## Strings And Maps

<!-- stage: context -->
### A Renaming That Merges Two Letters

A data migration renames the letter codes of a product catalog. The old code `abca` becomes `zbxz`, and the new code uses one new letter for each old letter. A first check compares each old letter with its new letter and accepts the mapping `ab` to `cc`, although two different old letters now share one new letter. Records that were different before the migration become identical after it.

The check must look at characters of two strings together and remember what it has seen earlier. The question is what a program must remember while it scans two strings in step, so that it rejects a mapping that merges two letters or splits one letter.

<!-- stage: contributions -->
### What The String And Map Add

The string supplies characters in a fixed order. A scan with an index reads the same position of both strings together and never skips a character. The scan alone cannot compare a character with one that appeared much earlier, because it keeps no record of the past.

The map supplies that record. A frequency map or a 26-entry table remembers how often each character occurred. A map from one character to another remembers the partner that each source character received. The combined question compares, classifies or constrains characters across one or more strings. Neither part answers it alone. The scan fixes the order of the characters, and the map answers questions about characters that are far apart.

<!-- stage: naive -->
### Comparing Every Pair Of Positions

The direct method checks every pair of positions. Two positions of the source must hold equal letters exactly when the same two positions of the target hold equal letters.

```java
static boolean sameShape(String s, String t) {
    if (s.length() != t.length()) {
        return false;
    }
    for (int i = 0; i < s.length(); i++) {
        for (int j = i + 1; j < s.length(); j++) {
            boolean equalSource = s.charAt(i) == s.charAt(j);
            boolean equalTarget = t.charAt(i) == t.charAt(j);
            if (equalSource != equalTarget) {
                return false;
            }
        }
    }
    return true;
}
```

On `"abca"` and `"zbxz"` the method returns true. On `"ab"` and `"cc"` the pair of positions 0 and 1 gives different source letters and equal target letters, so the method returns false.

<!-- stage: bottleneck -->
### Every Pair Rechecks The Same Letters

```predict
Two strings of 100000 letters have the same shape. How many pair comparisons does the method make, and what single fact does each comparison look up again?

The method makes about n * (n - 1) / 2 comparisons, which is O(n^2). Each comparison re-reads whether two letters are equal, a fact that one remembered pairing per letter would already answer.
```

The method recomputes whether two letters match for every pair of positions. The information it needs is much smaller. Each source letter has to pair with one target letter for the whole string, and each target letter has to pair with one source letter. A program that records these pairings the first time it sees a letter can check each later position against the record in constant time. That reduces the work to one pass of O(n).

<!-- stage: insight -->
### Remember Each Pairing In Both Directions

#### Pair Each Source Letter Once

A **bijection** between two sets of letters pairs each letter of one set with exactly one letter of the other, and no letter is left over or used twice. The strings have the same shape exactly when the letter pairs read from the positions form a bijection.

<!-- names: bijection, forward map, reverse map -->

#### Keep Two Maps

The **forward map** sends a source letter to its target letter. The **reverse map** sends a target letter back to its source letter. At position `i`, the loop looks up `s[i]` in the forward map. If the map holds a different target, one source letter splits into two targets, so the answer is false. The loop also looks up `t[i]` in the reverse map. If it holds a different source, two source letters merge into one target, so the answer is false. If both lookups agree or find nothing, the loop stores the pairing.

#### Why One Direction Is Not Enough

The pair `"ab"` and `"cc"` passes the forward check, because `a` goes to `c` and `b` goes to `c` without a conflict. The reverse map catches it, since `c` already points back to `a` when `b` arrives. The reverse check is the part that blocks a merge, and the forward check blocks a split.

#### The Invariant

After position `i`, the forward map and the reverse map hold the same pairs, read in opposite directions, for all letters of `s[0..i]`, and the pairs form a bijection. The pass costs O(n) with O(1) work per position. The two maps hold at most one entry for each distinct letter, so the space is O(d).

<!-- stage: variables -->
### Two Maps And One Index

The scan uses three pieces of state.

- **forward** maps each source letter seen so far to its target letter.
- **reverse** maps each target letter seen so far to its source letter, and mirrors `forward`.
- **i** names the position of both strings that the loop compares, and it increases by one each time.

<!-- stage: trace -->
### Pairing Letters In Two String Pairs

#### A Consistent Renaming

Take `s = "egg"` and `t = "add"`. At position 0 the letter `e` is new, so the forward map stores `e` to `a` and the reverse map stores `a` to `e`. At position 1 the letter `g` is new, so both maps store the pairing `g` with `d`. At position 2 the letter `g` is known. Its stored target `d` matches `t[2]`, so nothing changes. The method returns true.

#### A Merge Caught By The Reverse Map

Now take `s = "badc"` and `t = "baba"`. The first two positions pair `b` with `b` and `a` with `a`. At position 2 the source letter `d` is new, but the reverse map says that the target letter `b` already comes from the source letter `b`. Two source letters would share one target, so the method returns false at position 2.

#### Stepping Through Both Pairs

```trace
{"cells":["e/a","g/d","g/d"],"pointers":["i"],"steps":[{"at":{"i":-1},"vars":{"forward":"{}","reverse":"{}"},"note":"Start: both maps are empty."},{"at":{"i":0},"vars":{"pair":"e/a","forward":"{e:a}","reverse":"{a:e}"},"note":"Both letters are new. Store e with a in both maps."},{"at":{"i":1},"vars":{"pair":"g/d","forward":"{e:a, g:d}","reverse":"{a:e, d:g}"},"note":"Both letters are new. Store g with d in both maps."},{"at":{"i":2},"vars":{"pair":"g/d","forward":"{e:a, g:d}","reverse":"{a:e, d:g}"},"note":"The stored pairing g with d matches. Nothing changes."},{"at":{"i":3},"vars":{"forward":"{e:a, g:d}","reverse":"{a:e, d:g}"},"note":"The scan ends with no conflict, so return true."}]}
```

```trace
{"cells":["b/b","a/a","d/b","c/a"],"pointers":["i"],"steps":[{"at":{"i":-1},"vars":{"forward":"{}","reverse":"{}"},"note":"Start: both maps are empty."},{"at":{"i":0},"vars":{"pair":"b/b","forward":"{b:b}","reverse":"{b:b}"},"note":"Both letters are new. Store b with b in both maps."},{"at":{"i":1},"vars":{"pair":"a/a","forward":"{b:b, a:a}","reverse":"{b:b, a:a}"},"note":"Both letters are new. Store a with a in both maps."},{"at":{"i":2},"vars":{"pair":"d/b","forward":"{b:b, a:a}","reverse":"{b:b, a:a}"},"note":"Target letter b already comes from b, not d. Two letters would merge, so return false."}]}
```

<!-- stage: code -->
### Two Maps In One Scan

#### Checking The Renaming

```java
static boolean isomorphic(String s, String t) {
    if (s.length() != t.length()) {
        return false;
    }
    Map<Character, Character> forward = new HashMap<>();
    Map<Character, Character> reverse = new HashMap<>();
    for (int i = 0; i < s.length(); i++) {
        char a = s.charAt(i);
        char b = t.charAt(i);
        Character mappedTo = forward.get(a);
        Character mappedFrom = reverse.get(b);
        if ((mappedTo != null && mappedTo != b) || (mappedFrom != null && mappedFrom != a)) {
            return false;
        }
        forward.put(a, b);
        reverse.put(b, a);
    }
    return true;
}
```

#### What The Method Costs

The loop runs n times and each iteration makes two lookups and two stores of expected constant time, so the expected time is O(n). Each map holds at most one entry for each distinct letter, so the space is O(d), at most O(n). The comparison `mappedTo != b` compares a `Character` with a `char`, which unboxes the first operand, and the null test comes first.

<!-- stage: applicability -->
### When Letters Must Match Across Strings

#### Look For Counts Or Pairings Across Strings

Use a string scan with a map when a question compares, classifies or constrains characters across one or more strings. Typical questions ask for the first letter with a given count, whether two strings use the same letters equally often, and whether a renaming is one to one. The invariant is that the map holds exactly the counts or pairings of the characters read so far. For a bounded alphabet such as lowercase letters, a 26-entry table replaces a map, as the previous lesson showed.

#### A Plain Scan Or A Sort Is A False Friend

A false friend here is a plain scan that compares only neighbors. A scan cannot remember a letter that appeared far earlier, so it misses a merge between positions 0 and 9. Sorting the letters of a string is another near miss. It supports the anagram question, but it loses the position of each letter, so it cannot test a renaming, and it costs O(n log n). Sorted signatures belong to a later chapter.

#### Java Details That Cause Failures

The call `forward.get(a)` returns `null` for a new letter, so keep the result in a `Character` and test it for null before comparing. A comparison of two `Character` objects with `!=` compares references, so compare the unboxed `char` values.

<!-- stage: exercises -->
### Exercises

#### [Build] First Unique Character In A String (LeetCode 387)
<!-- id: hm-first-unique-outside -->

**Prerequisites.** The frequency map from the second lesson and the string scan from this lesson.

**Problem.** This variation of First Unique Character adds a second string. Let `s` and `t` be strings of lowercase letters. Return the smallest index `i` such that the letter `s.charAt(i)` occurs exactly once in `s` and does not occur in `t`. Return -1 when no index qualifies.

**Constraints.** The limits are:
- **Length** satisfies `0 <= s.length() <= 10^5`.
- **Characters** are lowercase letters `'a'` to `'z'`.
- **Second string** satisfies `0 <= t.length() <= 10^5` and may be empty.
- **Answer** is an index or -1.

**Example 1.** Input `s = "abcab"`, `t = "b"`, output 2, because `c` occurs once in `s` and is absent from `t`.

**Example 2.** Input `s = "xyz"`, `t = "x"`, output 1, because `x` occurs in `t` and `y` does not.

**Hint.** Which pass produces the counts for `s`, and what does the program check about `t` for each candidate?

**Changed decision.** A second string adds a condition to the original question, so the answer needs the counts of `s` and the letters of `t`.

#### [Vary] Letter Changes For An Anagram (LeetCode 242)
<!-- id: hm-letter-changes -->

**Prerequisites.** First Unique Character In A String above.

**Problem.** This variation of Valid Anagram counts the changes needed and does not only answer yes or no. Let `s` and `t` be strings of lowercase letters with equal length. In one step, replace any one character of `t` with any lowercase letter. Return the smallest number of steps that turn `t` into an anagram of `s`. The answer is 0 exactly when `t` is already an anagram of `s`.

**Constraints.** The limits are:
- **Length** satisfies `0 <= s.length() == t.length() <= 10^5`.
- **Characters** are lowercase letters.
- **Answer** is an `int` from 0 to `s.length()`.
- **Method** compares two letter tables.

**Example 1.** Input `s = "bab"`, `t = "aba"`, output 1.

**Example 2.** Input `s = "abc"`, `t = "cab"`, output 0.

**Hint.** For each letter, how many more copies does `s` hold than `t`?

**Changed decision.** The program compares two letter tables and sums the shortfalls instead of testing for equality.

#### [Boundary] Isomorphic Strings (LeetCode 205)
<!-- id: hm-isomorphic -->

**Prerequisites.** The two exercises above and the two maps from this lesson.

**Problem.** Let `s` and `t` be strings. They are isomorphic when a single mapping replaces each character of `s` by one character of `t` and turns `s` into `t`. The mapping must send different characters to different characters, and one character may map to itself. Return true when `s` and `t` are isomorphic.

**Constraints.** The limits are:
- **Length** satisfies `0 <= s.length() <= 5 * 10^4`.
- **Characters** are any Java `char` values.
- **Lengths** of `s` and `t` may differ, and then the answer is false.
- **Answer** is a boolean.

**Example 1.** Input `s = "abca"`, `t = "zbxz"`, output true.

**Example 2.** Input `s = "ab"`, `t = "cc"`, output false, because two characters would map to `c`.

**Hint.** Which map catches two source characters that share one target?

**Changed decision.** The mapping must hold in both directions, so one direction of memory lets a merge through.

#### [Recognize] Word Pattern (LeetCode 290)
<!-- id: hm-word-pattern -->

**Prerequisites.** All three exercises above.

**Problem.** Let `pattern` be a string of lowercase letters and `text` a string of words separated by single spaces. Return true when one word can be assigned to each letter of `pattern` so that the words of `text`, read in order, follow the pattern. Different letters need different words, and equal letters need equal words.

**Constraints.** The limits are:
- **Pattern** has `1 <= pattern.length() <= 300` letters.
- **Text** holds lowercase words with exactly one space between neighbors and no space at either end.
- **Count** of words may differ from the length of `pattern`, and then the answer is false.
- **Answer** is a boolean.

**Example 1.** Input `pattern = "xyx"`, `text = "red blue red"`, output true.

**Example 2.** Input `pattern = "ab"`, `text = "go go"`, output false, because two letters would share one word.

**Hint.** What does the program split first, and which two maps from this lesson carry over once the words are separate?

**Changed decision.** The targets are words and not characters, so the maps store `char` to `String` and `String` to `char`.
