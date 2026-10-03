<!-- lesson-kind: standard -->
<!-- lesson-id: fixed-alphabet-counts -->
## Fixed Alphabet Counts

<!-- stage: context -->
### Spelling Words From Tiles

A word game comes with a bag of lettered tiles, and a player wants to spell a word using only tiles from the bag, each tile used once. She tips the bag onto the table and sorts the tiles into twenty-six small trays labelled A to Z, one tray per letter. To spell the word she takes a tile from the tray for each of its letters, in order, and if a tray is ever empty when she needs it, the word cannot be spelled.

The trays make the question easy because the alphabet is small and fixed. She does not search through the pile for each letter. She goes straight to the tray with the right label. Twenty-six trays are the same for a bag of ten tiles and a bag of ten thousand.

<!-- stage: naive -->
### Hunt Through The Pile For Every Letter

Without trays, the direct method looks through the pile for an unused tile that matches each letter of the word.

```java
static boolean canSpellBySearch(String word, String bag) {
    char[] tiles = bag.toCharArray();
    for (int i = 0; i < word.length(); i++) {
        boolean found = false;
        for (int j = 0; j < tiles.length; j++) {
            if (tiles[j] == word.charAt(i)) { tiles[j] = '#'; found = true; break; }
        }
        if (!found) return false;
    }
    return true;
}
```

It is correct. It crosses off each tile it uses, so a letter needed twice needs two tiles. For the word `aabc` and the bag `cbaaaz` it finds all four tiles and returns true.

<!-- stage: bottleneck -->
### A Fresh Search Through The Whole Bag

For each of the `r` letters of the word, the inner loop may scan all `m` tiles, so the time is O(r * m). With 100,000 letters on each side, that is up to ten billion comparisons. The extra space is O(m) for the copy of the bag. Most of the effort is wasted on tiles that are not the wanted letter, and the same tile may be examined and rejected many times for different letters.

What matters about the bag is not the order of its tiles but how many of each letter it holds. That is twenty-six numbers. Counting them takes one pass over the bag, and each letter of the word then costs one lookup and one subtraction. The question turns from searching a pile into reading a small table.

<!-- stage: insight -->
### One Slot Per Letter, Found By Arithmetic

A **letter table** is an array of 26 integers, one per lowercase letter. The letter `c` has the slot `c - 'a'`, so `'a'` is slot 0 and `'z'` is slot 25. Reading a character and updating its counter is one subtraction and one array access, O(1), and the table has a fixed size that does not grow with the input. The invariant is that after a prefix of the input has been read, `count[c - 'a']` is the number of times `c` has occurred in that prefix.

All of this rests on the **alphabet contract**, the promise that every character is one of the 26 lowercase letters. Without that promise, the expression `c - 'a'` can be negative for an uppercase letter or larger than 25 for a digit or an accented letter, and indexing the table throws an exception. The contract must be stated, and either the code checks each character before using it as an index, or the problem guarantees it.

<!-- names: letter table, alphabet contract, net count -->

Two scans can share one table. To test whether a word can be spelled from a bag, count the bag, then walk through the word and subtract one for each letter. If any slot drops below zero, the bag ran out of that letter, and the scan can stop at once. To find the one letter that differs between two strings, add one for each letter of the first and subtract one for each letter of the second. The **net count** of each slot is the surplus in one string compared with the other, and the slot with a nonzero value is the odd letter out.

The table is not a hash map. It works because the keys are the integers 0 to 25 after one subtraction, so the key itself is the address. General characters, words or arbitrary keys have no such address and need the maps of Chapter 04.

<!-- stage: variables -->
### Twenty-Six Counters And An Index

The array `count` has length 26, and Java fills it with zeros, which is the right count for nothing read yet. The index `c - 'a'` is computed from the character `c`, and before using it, the code either checks that `c` lies between `'a'` and `'z'` or relies on the contract. For two-string questions the counter can go below zero, and its sign carries meaning: positive means a surplus from the first string, negative a surplus from the second. When the scan stops early, the table is left in a half-finished state and its contents mean nothing.

<!-- stage: trace -->
### Net Counts And An Early Stop

Take the strings `abc` and `cabd`. Reading the first string adds one to the slots of `a`, `b` and `c`. Reading the second subtracts one for each of `c`, `a`, `b` and `d`. After `c`, `a` and `b` the three slots are back to zero. Then `d` subtracts one from a slot that was zero, leaving `d` at minus one. The only nonzero slot is `d`, so `d` is the letter that the second string has extra.

Now ask whether the word `bab` can be spelled from the bag `abc`. Counting the bag gives one `a`, one `b` and one `c`. The first `b` in the word takes the `b` count to zero. The `a` takes the `a` count to zero. The second `b` would take the `b` count to minus one, so the word cannot be spelled, and the scan stops there without reading anything else. The step to study is the last one, where a negative count is a verdict that no later letter can reverse.

```trace
{"cells":["a","b","c","c","a","b","d"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"phase":"add from first","nonzero":"a:1"},"note":"Read 'a' from the first string and add one to its slot. Nonzero slots: a:1."},{"at":{"i":1},"vars":{"phase":"add from first","nonzero":"a:1,b:1"},"note":"Read 'b' from the first string and add one to its slot. Nonzero slots: a:1,b:1."},{"at":{"i":2},"vars":{"phase":"add from first","nonzero":"a:1,b:1,c:1"},"note":"Read 'c' from the first string and add one to its slot. Nonzero slots: a:1,b:1,c:1."},{"at":{"i":3},"vars":{"phase":"subtract from second","nonzero":"a:1,b:1"},"note":"Read 'c' from the second string and subtract one from its slot. Nonzero slots: a:1,b:1."},{"at":{"i":4},"vars":{"phase":"subtract from second","nonzero":"b:1"},"note":"Read 'a' from the second string and subtract one from its slot. Nonzero slots: b:1."},{"at":{"i":5},"vars":{"phase":"subtract from second","nonzero":"none"},"note":"Read 'b' from the second string and subtract one from its slot. Nonzero slots: none."},{"at":{"i":6},"vars":{"phase":"subtract from second","nonzero":"d:-1"},"note":"Read 'd' from the second string and subtract one from its slot. Nonzero slots: d:-1."}]}
```

```trace
{"cells":["a","b","c","b","a","b"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"phase":"count the bag","counts":"a:1"},"note":"Read 'a' from the bag. Counts: a:1."},{"at":{"i":1},"vars":{"phase":"count the bag","counts":"a:1,b:1"},"note":"Read 'b' from the bag. Counts: a:1,b:1."},{"at":{"i":2},"vars":{"phase":"count the bag","counts":"a:1,b:1,c:1"},"note":"Read 'c' from the bag. Counts: a:1,b:1,c:1."},{"at":{"i":3},"vars":{"phase":"spell the word","counts":"a:1,c:1"},"note":"Read 'b' from the word and take one tile. Counts: a:1,c:1."},{"at":{"i":4},"vars":{"phase":"spell the word","counts":"c:1"},"note":"Read 'a' from the word and take one tile. Counts: c:1."},{"at":{"i":5},"vars":{"phase":"spell the word","counts":"b:-1,c:1"},"note":"Read 'b' from the word and take one tile. Counts: b:-1,c:1. The count is negative, so the word cannot be spelled. Stop."}]}
```

<!-- stage: code -->
### Counting With A Letter Table

```java
static int[] vowelCounts(String s) {                       // a, e, i, o, u in that order
    int[] count = new int[26];
    for (int i = 0; i < s.length(); i++) count[s.charAt(i) - 'a']++;
    String vowels = "aeiou";
    int[] out = new int[5];
    for (int v = 0; v < 5; v++) out[v] = count[vowels.charAt(v) - 'a'];
    return out;
}

static char findDifference(String s, String t) {
    int[] net = new int[26];
    for (int i = 0; i < s.length(); i++) net[s.charAt(i) - 'a']++;
    for (int i = 0; i < t.length(); i++) net[t.charAt(i) - 'a']--;
    for (int c = 0; c < 26; c++) if (net[c] != 0) return (char) ('a' + c);
    return '?';
}

static boolean canConstruct(String note, String magazine) {
    int[] count = new int[26];
    for (int i = 0; i < magazine.length(); i++) count[magazine.charAt(i) - 'a']++;
    for (int i = 0; i < note.length(); i++) if (--count[note.charAt(i) - 'a'] < 0) return false;
    return true;
}
```

Each method makes one pass over each string and a pass over 26 slots at most, so the time is O(n + m) and the space is O(1) with a fixed 26-element table. These methods trust the alphabet contract and throw an `ArrayIndexOutOfBoundsException` for a character outside `'a'` to `'z'`. The conversion back to a character needs the cast, since `'a' + c` is an `int`.

<!-- stage: applicability -->
### When The Alphabet Is Small And Promised

Use a letter table when the characters come from a small fixed alphabet that the problem states, such as lowercase English letters, and the question is about counts, balance or availability. The invariant is that each slot holds the count for its letter over the part already read. Check the alphabet contract against the statement before choosing this table.

The false friend is a general character set. Text that may contain uppercase letters, digits, punctuation or other scripts either needs a larger table whose size is stated, such as 128 for ASCII, or a map. Even then the table only counts single characters. Counting words or arbitrary keys is the job of the maps in Chapter 04. Another false friend is using a table to answer an ordering question. The counts forget the order, so they cannot tell which of two strings comes first or whether one is a subsequence of the other.

In Java, subtracting `'a'` from a `char` gives an `int`, so no cast is needed for the index, but one is needed to convert back. Allocate the table at the declared size and check each character if the input is not guaranteed. A pre-decrement such as `--count[i] < 0` both updates and tests in one step. If the alphabet is larger than a few hundred characters, a table stops being cheap, and a map becomes the better choice.

<!-- stage: exercises -->
### Exercises

#### [Build] Vowel Counts (Author exercise)
<!-- id: st-vowel-counts -->

**Prerequisites.** The frequency-array lesson from Chapter 01; the indexed scan from the first lesson of this chapter.

**Problem.** Given a string of lowercase letters, return an array of five counts, giving how many times each of `a`, `e`, `i`, `o` and `u` appears, in that order.

**Constraints.** 0 <= s.length() <= 10^5 and `s` contains only the letters `a` to `z`. Use a 26-slot table.

**Example 1.** Input `s = "education"`, output `[1, 1, 1, 1, 1]`.

**Example 2.** Input `s = "banana"`, output `[3, 0, 0, 0, 0]`.

**Hint.** What index does a letter get, and what does the table hold before any letter is read? How do you get from the table to the five answers?

**Changed decision.** First rung: each letter picks its own counter by arithmetic, so there is no search.

#### [Vary] Find the Difference (LeetCode 389)
<!-- id: st-find-difference -->

**Prerequisites.** The vowel-counts exercise above.

**Problem.** String `t` is made by shuffling string `s` and adding one extra lowercase letter at a random position. Return that extra letter.

**Constraints.** 0 <= s.length() <= 1000, `t.length() == s.length() + 1`, and both contain only lowercase letters.

**Example 1.** Input `s = "abcd", t = "dbcea"`, output `'e'`.

**Example 2.** Input `s = "aab", t = "abaa"`, output `'a'`, because `t` has three copies and `s` has two.

**Hint.** What happens to a letter's counter if you add for one string and subtract for the other? Which slot ends nonzero?

**Changed decision.** One table is shared by two strings, with additions from one and subtractions from the other, and the answer is the slot with a nonzero net count.

#### [Boundary] Invalid Alphabet (Author exercise)
<!-- id: st-invalid-alphabet -->

**Prerequisites.** The two exercises above.

**Problem.** Write a method that counts the lowercase letters of a string, and reject any character outside `'a'` to `'z'` before it is used as an index. Decide what the method does on a bad character, and document it. Show what the unchecked version does with `'B'`, `'{'` and `'é'`.

**Constraints.** 0 <= s.length() <= 10^5. A bad character must not corrupt any count and must not cause an unrelated exception.

**Example 1.** Input `s = "ab"`, output counts of 1 for `a` and 1 for `b`.

**Example 2.** Input `s = "aB"`, output a rejection that names the character `'B'` and its index 1.

**Hint.** Which index would `'B' - 'a'` produce? Why is checking the range before indexing better than catching the exception afterwards?

**Changed decision.** The question moves from counting to protecting the index, since the alphabet is a contract that has to be enforced.

#### [Recognize] Ransom Note (LeetCode 383)
<!-- id: st-ransom-note -->

**Prerequisites.** All three exercises above.

**Problem.** Given a note and a magazine, both strings of lowercase letters, return whether the note can be spelled using letters from the magazine, where each magazine letter can be used once.

**Constraints.** 1 <= note.length(), magazine.length() <= 10^5 and both contain only lowercase letters. Stop as soon as a needed letter runs out.

**Example 1.** Input `note = "aabc", magazine = "cbaaaz"`, output true.

**Example 2.** Input `note = "xyy", magazine = "yxz"`, output false, since two `y` are needed and one is available.

**Hint.** What do you count first, and what do you do for each letter of the note? When can you stop early?

**Changed decision.** The counts are consumed while scanning the second string, and a negative count ends the scan with a definite no.
