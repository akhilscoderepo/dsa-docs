<!-- lesson-kind: combination -->
<!-- lesson-id: strings-and-maps -->
## Strings And Maps

<!-- stage: context -->
### A Cipher Club With A Codebook

A cipher club writes secret notes by replacing each symbol with a letter. The rule is strict: a symbol must always stand for the same letter, and two different symbols may never share a letter, or the note could not be read back. A new member shows a coded line next to its plain text and asks whether the code is a legal substitution.

The checker reads both lines together, one position at a time. She keeps a codebook with two columns, symbol to letter and letter to symbol. When a symbol appears that she has seen before, she looks it up and checks that the letter now written is the one in the book. When a new symbol appears, she checks that its letter is not already taken by another symbol, then writes both entries. She cannot decide by looking at neighbouring positions, because the symbol that matters may have appeared at the very start of the line.

<!-- stage: contributions -->
### What Each Part Brings

The string supplies the characters in a defined order, with a position for each one, and it can be read from left to right once. That order is what the problems ask about: the first character with some property, or the earliest violation of a rule. The string alone, though, can only look at the character in front of it and the few before it, and it forgets everything else.

The map supplies that memory. It remembers either how many times a character has appeared or which other character it was paired with, and it answers a question about any earlier character in expected constant time, wherever that character occurred. The recognition cue for the combination is a question that compares, classifies or constrains characters across one string or between two, including characters that are far apart. Used together, the string decides when to ask and the map decides what the answer is.

<!-- stage: naive -->
### Compare Every Pair Of Positions

The direct way to test a substitution is to check every pair of positions. Two positions in the plain text hold the same letter exactly when the two positions in the code hold the same symbol.

```java
static boolean isLegalBySearch(String plain, String coded) {
    if (plain.length() != coded.length()) return false;
    for (int i = 0; i < plain.length(); i++) {
        for (int j = i + 1; j < plain.length(); j++) {
            boolean samePlain = plain.charAt(i) == plain.charAt(j);
            boolean sameCoded = coded.charAt(i) == coded.charAt(j);
            if (samePlain != sameCoded) return false;
        }
    }
    return true;
}
```

For `abca` and `xyzx` it returns true, and for `abc` and `xyy` it returns false because positions 1 and 2 agree in the code but not in the plain text.

<!-- stage: bottleneck -->
### Positions Compared Again And Again

The nested loops compare about `n * n / 2` pairs, so the cost is O(n * n), and with 100,000 characters that is five billion comparisons. Each pair is checked on its own, though the answer for a pair follows from a fact about each character alone: which character it was first paired with.

A single left-to-right scan with no memory cannot replace the pair loop. Comparing a character only with its neighbour would accept `abca` and `xyzy`, since each adjacent step looks fine while the first and last positions disagree. What is needed is a record, per character, of the partner it was given the first time, so that a later occurrence can be checked against that one entry instead of against every earlier position.

<!-- stage: insight -->
### Two Notebooks For A Two-Way Rule

Counting questions need one ledger, as in the frequency lessons. Correspondence questions need maps that remember pairings. A **forward map** sends each character of the first string to the character of the second string it was paired with at the first occurrence. A **backward map** does the reverse. A step reads the pair `(a, b)` at position `i`. If the forward map already has an entry for `a`, it must equal `b`. If the backward map already has an entry for `b`, it must equal `a`. If a check fails, the rule is broken. If neither map has an entry, both entries are written.

<!-- names: forward map, backward map, bijection -->

The rule being checked is a **bijection** between the characters used, a pairing in which each character has exactly one partner in each direction. Keeping only the forward map checks that one symbol never means two letters, but it lets two symbols share a letter, which the club forbids. That is the boundary case of this lesson, and it is why both maps are needed. The invariant is that after position `i`, the two maps are exact inverses of each other and cover every character in the processed prefix.

The same machinery covers the counting questions. First unique character uses one frequency map for the counts and the string's own order for the answer. An anagram test builds a single signed ledger, adding for one string and subtracting for the other, and deleting keys that reach zero, so an empty map at the end means every count matched. A word pattern is the bijection check again, with words in place of characters, after splitting the sentence into tokens.

<!-- stage: variables -->
### One Or Two Maps And A Position

The scan index `i` moves through both strings at once, so their lengths are compared first and a mismatch ends the question. The forward map is keyed by characters of the first string and the backward map by characters of the second. For a counting question there is a single map from character to count, and a decision rule about deleting keys at zero. For a word pattern the second key type is a `String`, so equality uses `equals`, which map lookup already does. Nothing in these maps is read by position, only by key.

<!-- stage: trace -->
### A Legal Code And A Broken One

```trace
{"cells":["a","b","c","a"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"pair":"ax","forward":"a->x","backward":"x->a"},"note":"Pair 'a' with 'x': new in both maps, so store it. Forward: a->x."},{"at":{"i":1},"vars":{"pair":"by","forward":"a->x, b->y","backward":"x->a, y->b"},"note":"Pair 'b' with 'y': new in both maps, so store it. Forward: a->x, b->y."},{"at":{"i":2},"vars":{"pair":"cz","forward":"a->x, b->y, c->z","backward":"x->a, y->b, z->c"},"note":"Pair 'c' with 'z': new in both maps, so store it. Forward: a->x, b->y, c->z."},{"at":{"i":3},"vars":{"pair":"ax","forward":"a->x, b->y, c->z","backward":"x->a, y->b, z->c"},"note":"Pair 'a' with 'x': already stored and consistent. Forward: a->x, b->y, c->z."}]}
```

Take the plain text `abca` and the code `xyzx`. The first three positions pair a with x, b with y and c with z, and each pairing is new in both directions, so both maps gain an entry. At position 3 the letter a is already in the forward map with partner x, and the code symbol is x again, so the check passes and the line is legal.

```trace
{"cells":["a","b","c"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"pair":"ax","forward":"a->x","backward":"x->a"},"note":"Pair 'a' with 'x': new in both maps, so store it. Forward: a->x."},{"at":{"i":1},"vars":{"pair":"by","forward":"a->x, b->y","backward":"x->a, y->b"},"note":"Pair 'b' with 'y': new in both maps, so store it. Forward: a->x, b->y."},{"at":{"i":2},"vars":{"pair":"cy","forward":"a->x, b->y","backward":"x->a, y->b"},"note":"Symbol 'y' is already paired with 'b', not 'c'. Fail."}]}
```

Now take `abc` and `xyy`. The first two positions are fine. At position 2 the letter c is new in the forward map, but the symbol y is already in the backward map as the partner of b, not of c. The backward check fails and the answer is false. A forward map alone would have accepted this input, which is the reason for the second notebook.

<!-- stage: code -->
### Counting, Balancing And Pairing

```java
static char firstUniqueChar(String s) {
    Map<Character, Integer> count = new LinkedHashMap<>();
    for (char c : s.toCharArray()) count.merge(c, 1, Integer::sum);
    for (Map.Entry<Character, Integer> e : count.entrySet()) {
        if (e.getValue() == 1) return e.getKey();       // LinkedHashMap iterates in first-seen order
    }
    return '_';
}

static boolean sameLetters(String a, String b) {
    if (a.length() != b.length()) return false;
    Map<Character, Integer> ledger = new HashMap<>();
    for (int i = 0; i < a.length(); i++) {
        bump(ledger, a.charAt(i), 1);
        bump(ledger, b.charAt(i), -1);
    }
    return ledger.isEmpty();                            // every key was deleted when it reached zero
}

static void bump(Map<Character, Integer> ledger, char c, int delta) {
    int now = ledger.getOrDefault(c, 0) + delta;
    if (now == 0) ledger.remove(c); else ledger.put(c, now);
}

static boolean isIsomorphic(String s, String t) {
    if (s.length() != t.length()) return false;
    Map<Character, Character> forward = new HashMap<>(), backward = new HashMap<>();
    for (int i = 0; i < s.length(); i++) {
        char a = s.charAt(i), b = t.charAt(i);
        Character f = forward.get(a), g = backward.get(b);
        if (f != null && f != b) return false;
        if (g != null && g != a) return false;
        forward.put(a, b);
        backward.put(b, a);
    }
    return true;
}

static boolean wordPattern(String pattern, String sentence) {
    String[] words = sentence.split(" ");
    if (pattern.length() != words.length) return false;
    Map<Character, String> forward = new HashMap<>();
    Map<String, Character> backward = new HashMap<>();
    for (int i = 0; i < words.length; i++) {
        char p = pattern.charAt(i);
        String w = words[i];
        String f = forward.get(p);
        Character g = backward.get(w);
        if (f != null && !f.equals(w)) return false;
        if (g != null && g != p) return false;
        forward.put(p, w);
        backward.put(w, p);
    }
    return true;
}
```

Every method makes one pass with expected constant map work per position, and the running cost is expected O(n) time with O(k) space for `k` distinct characters or words. The `Character` values are compared after unboxing, because `f != b` mixes a boxed value with a primitive, which unboxes the box and compares numbers. For two boxed values, `equals` is used. The `LinkedHashMap` gives the first-seen order that the first-unique question needs without a second pass over the string.

<!-- stage: applicability -->
### When The Question Spans Far Apart Characters

Use strings with maps when the rule compares, classifies or constrains characters that may be far apart, whether within one string or across two. The invariant is that the map or maps summarise exactly the processed prefix, and for a pairing rule that the two directions stay inverse to each other. Name what the key means and what the value means before writing a line.

The false friend is a plain scan that remembers only the previous character. It handles runs and adjacent comparisons, as in Chapter 03, but it cannot remember a character that appeared long ago. A second false friend is sorting. Sorting canonicalises strings and is a good tool for some comparisons, and it belongs to Chapter 05, but it is not required here and it destroys the positions that some questions need.

Java details are many. Use `equals` for string tokens and never `==`. Boxed `Character` values from a map are objects, so compare them with `equals` or unbox them first. Choose `LinkedHashMap` when the first-seen order matters. `split(" ")` on an empty string returns an array holding one empty string, so a pattern of length 1 would match an empty sentence unless the lengths and tokens are checked. When the alphabet is a small known range, the table from the direct-addressing lesson replaces the map.

<!-- stage: exercises -->
### Exercises

#### [Build] First Unique Character in a String (LeetCode 387)
<!-- id: hm-first-unique-letter -->

**Prerequisites.** Frequency maps; this lesson's reading of a string as order plus a map as memory. This is a deliberate revisit that returns the character itself and relies on first-seen order of the map.

**Problem.** Return the first character of the string that occurs exactly once, or the underscore character if every character repeats. Use an insertion-ordered map so that the order of the answer comes from the map's own iteration.

**Constraints.** 0 <= s.length() <= 10^5 and the string holds any characters other than the underscore. Return the character, not an index.

**Example 1.** Input `s = "level"`, output `'v'`.

**Example 2.** Input `s = "noon"`, output `'_'`, because both characters occur twice.

**Hint.** Which map type iterates in the order keys were first inserted, and does later counting change that order?

**Changed decision.** The answer is read from an ordered map instead of by rescanning the string.

#### [Vary] Valid Anagram (LeetCode 242)
<!-- id: hm-anagram-ledger -->

**Prerequisites.** The build exercise above; two-map comparison in the frequency lesson and the table version in the direct-addressing lesson.

**Problem.** Decide whether two strings, which may contain any characters, are anagrams, using one map as a signed ledger. Add one for each character of the first string and subtract one for each character of the second, deleting a key when its count reaches zero. The strings are anagrams when the map is empty at the end.

**Constraints.** 0 <= a.length(), b.length() <= 5 * 10^4. Characters are arbitrary, so a fixed 26-slot table is not allowed.

**Example 1.** Input `a = "dusty"`, `b = "study"`, output true.

**Example 2.** Input `a = "abca"`, `b = "abcc"`, output false, with the ledger left holding `a` and `c`.

**Hint.** Why must a key whose count returns to zero be removed before testing for an empty map?

**Changed decision.** Two ledgers become one signed ledger, so the final test is emptiness and not map equality.

#### [Boundary] Isomorphic Strings (LeetCode 205)
<!-- id: hm-isomorphic-strings -->

**Prerequisites.** The two exercises above.

**Problem.** Two strings of equal length are isomorphic if the characters of the first can be replaced to give the second, where each character always maps to the same replacement and no two different characters map to the same replacement. Return whether the strings are isomorphic.

**Constraints.** 0 <= s.length() == t.length() <= 5 * 10^4, and characters are arbitrary. Both directions of the pairing must be checked.

**Example 1.** Input `s = "gaga"`, `t = "xyxy"`, output true.

**Example 2.** Input `s = "ab"`, `t = "cc"`, output false, because two different characters would share the replacement `c`.

**Hint.** What does a forward map alone accept in the second example? What must you also record?

**Changed decision.** A one-way consistency check is replaced by a two-way one, which is the boundary of the bijection rule.

#### [Recognize] Word Pattern (LeetCode 290)
<!-- id: hm-word-pattern -->

**Prerequisites.** All three exercises above.

**Problem.** Given a pattern of lowercase letters and a sentence of words separated by single spaces, return whether the sentence follows the pattern, meaning there is a bijection between pattern letters and words, so equal letters match equal words and different letters match different words.

**Constraints.** 1 <= pattern.length() <= 300 and the sentence has single spaces and no leading or trailing spaces. The number of words must equal the pattern length.

**Example 1.** Input `pattern = "xyx"`, `sentence = "up down up"`, output true.

**Example 2.** Input `pattern = "ab"`, `sentence = "hot hot"`, output false, since two letters would share one word.

**Hint.** Which key types do the two maps have now, and which comparison must be used for the string values?

**Changed decision.** The second side of the pairing is a token, not a character, but the invariant and the two maps are the same.
