<!-- lesson-kind: standard -->
<!-- lesson-id: fixed-alphabet-counts -->
## Count Letters In An Array

<!-- stage: context -->
### The Key A Typing Tutor Reports

A typing tutor shows each learner which letter they type most often, so the learner can practice that key. A lesson holds up to a hundred thousand lowercase letters. The first version of the report takes several seconds to appear on a long lesson. The next version, on the same machine and the same text, appears at once.

Both versions give the same answers. The slow one repeats work that the fast one never does. The question is which work repeats when a program asks about letters in a long text, and how a program that knows the set of possible letters avoids it.

<!-- stage: naive -->
### Counting Each Letter By Rescanning

The direct method takes every position in the text, scans the whole text again to see how often that letter occurs, and keeps the best letter. A tie goes to the smaller letter.

```java
static char mostFrequent(String s) {
    char best = s.charAt(0);
    int bestTimes = 0;
    for (int i = 0; i < s.length(); i++) {
        int times = 0;
        for (int j = 0; j < s.length(); j++) {
            if (s.charAt(j) == s.charAt(i)) {
                times++;
            }
        }
        if (times > bestTimes || (times == bestTimes && s.charAt(i) < best)) {
            best = s.charAt(i);
            bestTimes = times;
        }
    }
    return best;
}
```

On `"banana"` the method returns `'a'`, which occurs three times. On `"cabab"` the letters `a` and `b` tie with two each, and the method returns `'a'`.

<!-- stage: bottleneck -->
### The Same Letter Gets Counted Repeatedly

```predict
For a text of 100000 letters, roughly how many character comparisons does the double loop make, and why does the program count the same letter more than once?

The outer loop runs 100000 times and each pass runs the inner loop 100000 times, so the method makes about 10 billion comparisons, which is O(n^2). Every position of the letter a starts a full rescan, so the program counts a again for each a in the text.
```

The method asks the same question many times. A text with 40000 letters `a` triggers 40000 identical rescans, and each rescan returns the same number. The work scales with the square of the length, so doubling the text quadruples the time. The text itself carries a hint about a faster method. Only 26 different letters can occur, so at most 26 different questions exist. A correct method reads the text once, in O(n) time, and records an answer for each of the 26 letters as it goes.

<!-- stage: insight -->
### Give Each Letter One Array Slot

When the set of possible characters is small and known in advance, an array can replace the repeated scans. That set is the **alphabet**, and its size is a constant, which is 26 for the lowercase English letters.

#### Convert A Letter To An Array Index

The expression `c - 'a'` turns a lowercase letter into a number from 0 to 25. The letter `'a'` gives 0, the letter `'b'` gives 1, and the letter `'z'` gives 25. The number `'a'` is the **offset** that moves the letter codes down to start at 0. Java stores `char` values as numbers, so the subtraction needs no conversion call.

<!-- names: frequency table, alphabet, offset -->

#### The Table Holds The Processed Count

A **frequency table** is an `int[26]` where entry `k` records how often the letter `'a' + k` appears. The loop keeps one invariant. After the iteration for index `i`, every entry equals the number of times its letter occurs in `s[0..i]`. Each iteration does one increment, `table[s.charAt(i) - 'a']++`, which takes constant time.

#### Read The Answer From The Table

After the loop, the answer comes from the 26 entries, not from the text. A scan over `k = 0` to `25` finds the largest entry. Using a strict comparison keeps the first letter on a tie. The whole method costs O(n) for the text plus 26 steps for the table, so the time is O(n). The table has 26 entries whatever the text length, so the space is O(1).

<!-- stage: variables -->
### Table, Index And Best Slot

The method needs only three values, and the text below says when each one changes.

- **table** holds 26 counters and gains one increment per character.
- **i** walks over the text positions and moves right by one each round.
- **best** holds the table index of the largest counter found so far while the scan over the table, described above, reads it.

<!-- stage: trace -->
### Counting Letters In Two Texts

#### A Text With One Clear Winner

Take `s = "banana"`. The trace shows only the entries that are not zero. At `i = 0` the letter `b` raises its entry to 1. At `i = 1` the letter `a` raises its entry to 1. The letters `n`, `a`, `n` and `a` follow, so the final entries are `a` with 3, `b` with 1 and `n` with 2. The scan over the table picks `a`.

#### A Text With A Tie

Now take `s = "cabab"`. The letters `c`, `a`, `b`, `a`, `b` give `a` with 2, `b` with 2 and `c` with 1. The scan reads the table from index 0, so it meets `a` first. Letter `b` has the same entry, and the strict comparison `>` leaves the choice on `a`.

#### Stepping Through Both Texts

```trace
{"cells":["b","a","n","a","n","a"],"pointers":["i"],"steps":[{"at":{"i":-1},"vars":{},"note":"Start: every entry of the table is 0."},{"at":{"i":0},"vars":{"b":1},"note":"Index 0 holds 'b', so the entry of b rises to 1."},{"at":{"i":1},"vars":{"a":1,"b":1},"note":"Index 1 holds 'a', so the entry of a rises to 1."},{"at":{"i":2},"vars":{"a":1,"b":1,"n":1},"note":"Index 2 holds 'n', so the entry of n rises to 1."},{"at":{"i":3},"vars":{"a":2,"b":1,"n":1},"note":"Index 3 holds 'a', so the entry of a rises to 2."},{"at":{"i":4},"vars":{"a":2,"b":1,"n":2},"note":"Index 4 holds 'n', so the entry of n rises to 2."},{"at":{"i":5},"vars":{"a":3,"b":1,"n":2},"note":"Index 5 holds 'a', so the entry of a rises to 3."},{"at":{"i":6},"vars":{"a":3,"b":1,"n":2},"note":"The loop ends. The scan over the table keeps the first largest entry, so the answer is 'a'."}]}
```

```trace
{"cells":["c","a","b","a","b"],"pointers":["i"],"steps":[{"at":{"i":-1},"vars":{},"note":"Start: every entry of the table is 0."},{"at":{"i":0},"vars":{"c":1},"note":"Index 0 holds 'c', so the entry of c rises to 1."},{"at":{"i":1},"vars":{"a":1,"c":1},"note":"Index 1 holds 'a', so the entry of a rises to 1."},{"at":{"i":2},"vars":{"a":1,"b":1,"c":1},"note":"Index 2 holds 'b', so the entry of b rises to 1."},{"at":{"i":3},"vars":{"a":2,"b":1,"c":1},"note":"Index 3 holds 'a', so the entry of a rises to 2."},{"at":{"i":4},"vars":{"a":2,"b":2,"c":1},"note":"Index 4 holds 'b', so the entry of b rises to 2."},{"at":{"i":5},"vars":{"a":2,"b":2,"c":1},"note":"The loop ends. The scan over the table keeps the first largest entry, so the answer is 'a'."}]}
```

<!-- stage: code -->
### A Table And One Pass

#### Finding The Most Frequent Letter

```java
static char mostFrequent(String s) {
    int[] table = new int[26];
    for (int i = 0; i < s.length(); i++) {
        table[s.charAt(i) - 'a']++;
    }
    int best = 0;
    for (int k = 1; k < 26; k++) {
        if (table[k] > table[best]) {
            best = k;
        }
    }
    return (char) ('a' + best);
}
```

#### What The Method Costs

The first loop reads each of the n characters once, and the second loop reads 26 entries. The time is O(n + 26), which is O(n). The table has 26 entries for every input, so the space is O(1). The cast to `char` in the last line is necessary, because `'a' + best` has type `int`.

<!-- stage: applicability -->
### When An Array Can Replace Scans

#### Look For A Small Declared Set

Use a frequency table when the statement names the set of characters and the set is small, such as the lowercase English letters or the ten digits. Questions about how often each character occurs, whether two texts use the same letters, and which letters are missing all fit. The invariant is that the table always holds the counts of exactly the characters processed so far. A table of size 26 costs the same for a text of ten characters and for a text of ten million.

#### Words And Arbitrary Characters Are A False Friend

A false friend here is a counting task whose set of possible values is not small. Counting how often each word appears has no 26-entry table, because the number of possible words is unbounded. A text with arbitrary Unicode characters has far too many possible values for a direct table. Such tasks need a map, which the next chapter teaches. The statement of a problem must name the alphabet before the table is a valid choice.

#### Java Details That Cause Failures

A character outside `'a'` to `'z'` produces an index below 0 or above 25, and Java throws `ArrayIndexOutOfBoundsException` at the increment. A new `int[26]` starts with every entry at 0, so no initialization loop is needed. The expression `c - 'a'` has type `int`, and the expression `'a' + k` also has type `int`, so a conversion back to a letter needs the cast `(char)`.

<!-- stage: exercises -->
### Exercises

#### [Build] Vowel Counts (Author exercise)
<!-- id: st-vowel-counts -->

**Prerequisites.** The frequency table and the index `c - 'a'` from this lesson.

**Problem.** Let `s` be a string of lowercase English letters. Return an `int[]` of length 5. Entry 0 holds the number of `'a'` in `s`, and entries 1 to 4 hold the numbers of `'e'`, `'i'`, `'o'` and `'u'` in that order.

**Constraints.** The limits are:
- **Length** satisfies `0 <= s.length() <= 10^5`; the empty string is legal.
- **Characters** are the lowercase letters `'a'` to `'z'` only.
- **Answer** has exactly 5 entries, all of type `int`.
- **Method** fills a 26-entry table and reads the five vowels from it.

**Example 1.** Input `s = "mississippi"`, output `[0, 0, 4, 0, 0]`.

**Example 2.** Input `s = ""`, output `[0, 0, 0, 0, 0]`.

**Hint.** Which table indexes belong to the five vowels, and when does the program read them?

**Changed decision.** Basic case: one pass fills the table, and a fixed list of indexes reads the answer.

#### [Vary] Find The Difference (LeetCode 389)
<!-- id: st-find-difference -->

**Prerequisites.** The vowel counter above.

**Problem.** Let `s` and `t` be strings of lowercase letters. The string `t` holds the same letters as `s`, in any order, plus exactly one extra letter at any position. Return the extra letter.

**Constraints.** The limits are:
- **Length** satisfies `0 <= s.length() <= 1000` and `t.length() == s.length() + 1`.
- **Characters** are the lowercase letters `'a'` to `'z'`.
- **Extra letter** may equal a letter that already occurs in `s`.
- **Answer** is a `char`.

**Example 1.** Input `s = "xyz"`, `t = "zqyx"`, output `'q'`.

**Example 2.** Input `s = ""`, `t = "m"`, output `'m'`.

**Hint.** If one pass adds each letter of `s` and another pass subtracts each letter of `t`, which entry ends up different from 0?

**Changed decision.** Two strings share one table, and the answer is the one entry that the increments and decrements leave nonzero.

#### [Boundary] Invalid Alphabet (Author exercise)
<!-- id: st-invalid-alphabet -->

**Prerequisites.** The two exercises above and the Java details from this lesson.

**Problem.** Let `s` be a string. Return `-1` when `s` holds any character outside `'a'` to `'z'`. Otherwise return the number of distinct letters in `s`.

**Constraints.** The limits are:
- **Length** satisfies `0 <= s.length() <= 10^5`.
- **Characters** are any Java `char` values.
- **Answer** is an `int` from `-1` to `26`.
- **Order** of checks guarantees that no table index lies outside 0 to 25.

**Example 1.** Input `s = "abca"`, output 3.

**Example 2.** Input `s = "ab1"`, output -1, because the digit lies outside the alphabet.

**Hint.** Which comparison must run before the table is indexed, and which index does the digit `'1'` give?

**Changed decision.** The method validates each character before it uses the character as an index.

#### [Recognize] Ransom Note (LeetCode 383)
<!-- id: st-ransom-note -->

**Prerequisites.** All three exercises above.

**Problem.** Let `note` and `magazine` be strings. The note can be built from the magazine when every letter of `note` can be matched to its own distinct position of `magazine` that holds the same letter. Return true when the note can be built.

**Constraints.** The limits are:
- **Length** satisfies `0 <= note.length(), magazine.length() <= 10^5`.
- **Characters** are the lowercase letters `'a'` to `'z'`.
- **Use** of a magazine position happens at most once.
- **Method** counts the magazine first and fails as soon as a needed count drops below 0.

**Example 1.** Input `note = "deed"`, `magazine = "eddxe"`, output true.

**Example 2.** Input `note = "noon"`, `magazine = "onn"`, output false, because the magazine holds one `o` only.

**Hint.** What does the table hold after the magazine pass, and what does each letter of the note do to it?

**Changed decision.** The first string fills the table with supply, and the second string consumes it and may fail early.
