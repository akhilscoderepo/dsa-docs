<!-- lesson-kind: combination -->
<!-- lesson-id: strings-maps-and-sorting -->
## Strings, Maps, And Sorting

<!-- stage: context -->
### A Tile Club Sorting Its Racks

A word-game club meets every week, and each player brings a rack of tiles that spells one word. Players are always delighted when two racks use exactly the same tiles in different arrangements, so the organizer wants to seat such players together. For every word she needs a way to say, quickly, which table it belongs to, and the table should depend on the tiles alone, not on the order they happen to lie in.

Her trick is to ask each player to slide their tiles into alphabetical order on the rack before she looks. Two racks that held the same tiles now look identical, letter for letter, and a rack that differs by even one tile looks different. She writes the arranged tiles on a card and files the player's name under that card. When the same card comes up again, she adds the name to the same pile.

<!-- stage: contributions -->
### What Each Part Brings

The string supplies the letters of a word one by one, in a fixed order, and gives access to the individual characters, which can be copied into a character array. That array is the raw material: it has the right letters but in an arrangement that varies from word to word. The string alone cannot say which other words are rearrangements of it, because comparing two strings position by position sees only the arrangement.

Sorting contributes a canonical sequence. Putting the characters of any word in order produces the same result for every rearrangement of the word, so the arrangement is thrown away and only the multiset of letters remains. The map contributes the grouping: it takes that canonical sequence as a key and keeps, under each key, the list of words that produced it. The recognition cue for the combination is a question in which different strings belong together exactly when their characters, counted with repeats, agree.

<!-- stage: naive -->
### Compare Every Pair Of Words By Counting

Without a shared label for each set of tiles, the organizer compares each pair of racks directly, counting how many of each letter the two words contain.

```java
static boolean sameTilesByCounting(String a, String b) {
    if (a.length() != b.length()) return false;
    for (int i = 0; i < a.length(); i++) {
        char c = a.charAt(i);
        int inA = 0, inB = 0;
        for (int j = 0; j < a.length(); j++) {
            if (a.charAt(j) == c) inA++;
            if (b.charAt(j) == c) inB++;
        }
        if (inA != inB) return false;
    }
    return true;
}

static List<List<String>> groupByPairs(String[] words) {
    List<List<String>> groups = new ArrayList<>();
    for (String w : words) {
        boolean placed = false;
        for (List<String> g : groups) {
            if (sameTilesByCounting(g.get(0), w)) { g.add(w); placed = true; break; }
        }
        if (!placed) { List<String> g = new ArrayList<>(); g.add(w); groups.add(g); }
    }
    return groups;
}
```

It never mistakes a pair, it handles any characters, and it keeps the groups in order of first appearance.

<!-- stage: bottleneck -->
### Every Word Meets Every Group

Comparing one pair of words of length L costs O(L^2) here, since each letter is counted by a scan. Placing a word may compare it against every existing group, and with n words that need their own groups, the total grows to O(n^2 L^2). With ten thousand short words of length ten, that is billions of character comparisons, and nearly all of them confirm what a quick lookup could have told.

What is repeated is the question "do these two words use the same tiles?", asked again for every pair. The answer for a word does not depend on the other word, so it can be computed once per word and compared by equality of a single object. If a single object stood for the tiles, finding the right group would be one lookup, and the cost would be sorting each word, which is O(L log L), plus a hash of a string of length L.

<!-- stage: insight -->
### A Sorted Word Is The Group Name

The sorted arrangement of a word's characters is its **canonical form**: the same for every rearrangement, and different for any word with a different multiset of characters. Equal canonical forms mean equal tiles, and unequal canonical forms mean different tiles, so the question "do these two words belong together?" becomes "are these two strings equal?". Used as a map key, the canonical form turns grouping into one lookup per word: compute the form, find or create the group stored under it, add the word.

Two words are anagrams exactly when their canonical forms are equal, which gives a direct two-word test as well: sort both character arrays and compare them. The grouping version stores, under each canonical form, a list of the words that produced it. A linked map keeps the groups in order of first appearance, which makes the output deterministic.

A canonical form is one example of a **signature**, a value computed from a word that two words share exactly when they belong together. Another signature for lowercase English words is an array of 26 counts. It is valid only under that alphabet contract, and it is a different route to the same grouping, not the reason sorted keys work. The sorted key works for any characters, because sorting needs no alphabet at all.

<!-- names: canonical form, signature, frequency multiset -->

Sometimes the grouping relation is weaker than anagram equality. Two strings may be considered related if some allowed operations can turn one into the other, and then the sorted string is too strong, since two related strings can have different sorted forms. What does survive the operations is the **frequency multiset**, the collection of how often each character occurs, with the identity of the characters forgotten, together with the set of characters themselves. Deciding which parts of the information are preserved by the allowed operations is the real work of such problems.

<!-- stage: variables -->
### Key, Group List And Counts

The key is the sorted character sequence, built into a string, because arrays do not compare by content when used as hash keys. The map takes each key to a list of the words that produced it, and a linked map keeps the keys in order of first appearance. For frequency questions, a count per character is the state, and for the weaker relation two further facts are kept: the set of characters present, and the sorted list of counts. The words themselves are never changed.

<!-- stage: trace -->
### Words Filing Under Sorted Keys

The first trace files seven words into groups by their sorted key. The step to study is the fifth word, `tops`, whose key is the same as the earlier `stop` and `pots`, so it joins an existing pile and creates none.

```trace
{"cells":["stop","pots","opts","cat","act","dog","tops"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"word":"stop","key":"opst","piles":1},"note":"stop sorts to opst, a key not seen before, so a new pile starts. There are 1 piles."},{"at":{"i":1},"vars":{"word":"pots","key":"opst","piles":1},"note":"pots sorts to opst, which already names a pile, so it joins stop. There are 1 piles."},{"at":{"i":2},"vars":{"word":"opts","key":"opst","piles":1},"note":"opts sorts to opst, which already names a pile, so it joins stop pots. There are 1 piles."},{"at":{"i":3},"vars":{"word":"cat","key":"act","piles":2},"note":"cat sorts to act, a key not seen before, so a new pile starts. There are 2 piles."},{"at":{"i":4},"vars":{"word":"act","key":"act","piles":2},"note":"act sorts to act, which already names a pile, so it joins cat. There are 2 piles."},{"at":{"i":5},"vars":{"word":"dog","key":"dgo","piles":3},"note":"dog sorts to dgo, a key not seen before, so a new pile starts. There are 3 piles."},{"at":{"i":6},"vars":{"word":"tops","key":"opst","piles":3},"note":"tops sorts to opst, which already names a pile, so it joins stop pots opts. There are 3 piles."}]}
```

The second trace asks whether `cabbba` and `abbccc` are related by the allowed operations of swapping positions and exchanging two letters everywhere. It lists each letter's count in both words. The letter sets agree, and the sorted counts agree, one two three on both sides, even though the letters carrying those counts differ. A raw sorted string would call these two words different, and that is the step to notice.

```trace
{"cells":["a","b","c"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"letter":"a","countInFirst":2,"countInSecond":1},"note":"The letter a occurs 2 times in the first word and 1 times in the second. It is present in both."},{"at":{"i":1},"vars":{"letter":"b","countInFirst":3,"countInSecond":2},"note":"The letter b occurs 3 times in the first word and 2 times in the second. It is present in both."},{"at":{"i":2},"vars":{"letter":"c","countInFirst":1,"countInSecond":3},"note":"The letter c occurs 1 times in the first word and 3 times in the second. It is present in both."},{"at":{"i":3},"vars":{"sortedCountsFirst":"1,2,3","sortedCountsSecond":"1,2,3","verdict":"close"},"note":"The letter sets are equal and the sorted counts are 1, 2, 3 on both sides, so the strings are close even though no single letter has the same count in both."}]}
```

<!-- stage: code -->
### Sorted Keys, Counts And Closeness

```java
static boolean areAnagrams(String s, String t) {
    if (s.length() != t.length()) return false;
    char[] x = s.toCharArray(), y = t.toCharArray();
    Arrays.sort(x);
    Arrays.sort(y);
    return Arrays.equals(x, y);
}

static List<List<String>> groupAnagrams(String[] words) {
    Map<String, List<String>> piles = new LinkedHashMap<>();
    for (String w : words) {
        char[] letters = w.toCharArray();
        Arrays.sort(letters);
        piles.computeIfAbsent(new String(letters), k -> new ArrayList<>()).add(w);
    }
    return new ArrayList<>(piles.values());
}

static String sortByFrequency(String s) {
    Map<Character, Integer> count = new HashMap<>();
    for (char c : s.toCharArray()) count.merge(c, 1, Integer::sum);
    List<Character> keys = new ArrayList<>(count.keySet());
    keys.sort((a, b) -> count.get(a).equals(count.get(b)) ? Character.compare(a, b) : Integer.compare(count.get(b), count.get(a)));
    StringBuilder out = new StringBuilder();
    for (char c : keys) for (int i = 0; i < count.get(c); i++) out.append(c);
    return out.toString();
}

static boolean isClose(String a, String b) {
    if (a.length() != b.length()) return false;
    Map<Character, Integer> ca = new HashMap<>(), cb = new HashMap<>();
    for (char c : a.toCharArray()) ca.merge(c, 1, Integer::sum);
    for (char c : b.toCharArray()) cb.merge(c, 1, Integer::sum);
    if (!ca.keySet().equals(cb.keySet())) return false;
    List<Integer> fa = new ArrayList<>(ca.values()), fb = new ArrayList<>(cb.values());
    Collections.sort(fa);
    Collections.sort(fb);
    return fa.equals(fb);
}
```

With words of length L, sorting each key costs O(L log L), so grouping n words costs O(n L log L) time and O(n L) space. The closeness check needs O(L) time for the counts, plus a sort of at most one count per distinct character. The sorted key is turned into a `String` because a `char[]` used as a key would be compared by identity, not by content.

<!-- stage: applicability -->
### When Rearrangements Count As Equal

Use a sorted signature when the question is about the multiset of characters: anagrams, groups of anagrams, whether one word can be rearranged into another. The invariant is that two strings share a canonical form exactly when they share the same characters with the same repeat counts. State what is allowed to change, the arrangement only, and check that the signature does not throw away anything the problem still cares about.

A false friend is a frequency-array signature presented as the cause of the technique. A 26-slot array is a valid and faster signature when the alphabet is guaranteed to be lowercase English, and it is wrong for other characters. It is an alternative representation, and sorting works without any alphabet contract. A second false friend is the problem where the allowed operations merge or relabel letters. There the sorted string is not preserved, only the character set and the frequency multiset are, and using the raw sorted key reports differently labeled strings as unrelated.

In Java, build a `String` from the sorted array before using it as a key, because arrays use identity equality. A map from `Character` to `Integer` or a plain array of counts are the usual counting tools, and a linked map keeps group order stable. When ordering the output by frequency, add an explicit tie rule, since the order of equal-frequency characters is otherwise left to chance.

<!-- stage: exercises -->
### Exercises

#### [Build] Valid Anagram (LeetCode 242)
<!-- id: so-valid-anagram-sorted -->

**Prerequisites.** The arrays-sort lesson and string traversal from Chapter 03.

**Problem.** Return true if the second string uses exactly the same characters as the first, with the same repeat counts, in any arrangement. Decide it by putting the characters of each word in order and comparing the two results.

**Constraints.** 1 <= s.length(), t.length() <= 50000 and the strings may contain any `char` values. Do not assume a 26-letter alphabet.

**Example 1.** Input `s = "listen", t = "silent"`, output true.

**Example 2.** Input `s = "aab", t = "abb"`, output false, since the repeat counts differ.

**Hint.** What does a word look like after its characters are sorted? Which check can reject two words immediately before any sorting?

**Changed decision.** First rung: the anagram question is answered by comparing canonical forms, not by counting with an assumed alphabet.

#### [Vary] Group Anagrams (LeetCode 49)
<!-- id: so-group-anagrams-sorted -->

**Prerequisites.** The valid-anagram exercise above.

**Problem.** Partition the words into groups of mutual anagrams. Report the groups in order of the first appearance of each group, and the words inside a group in input order. Use the sorted string of each word as the key of a map from keys to lists.

**Constraints.** 1 <= words.length <= 10000 and 0 <= each length <= 100. An empty string is a valid word, and words may repeat.

**Example 1.** Input `["stop", "pots", "opts", "cat", "act", "dog", "tops"]`, output `[["stop","pots","opts","tops"],["cat","act"],["dog"]]`.

**Example 2.** Input `[""]`, a single empty word, output `[[""]]`.

**Hint.** Why must the key be a `String` and not a `char[]`? Which kind of map keeps groups in order of first appearance?

**Changed decision.** The pair test becomes a map key, so each word costs one sort and one lookup in place of a comparison with every group.

#### [Boundary] Sort Characters by Frequency (LeetCode 451)
<!-- id: so-sort-characters-by-frequency -->

**Prerequisites.** The two exercises above.

**Problem.** Rearrange a string so that characters appear in decreasing order of how often they occur, with each character's copies together. Break ties between characters of equal count by the smaller character code. Keep this output ordering apart from the canonical key, which sorts by character and ignores counts.

**Constraints.** 1 <= s.length() <= 50000, and the string may contain letters of both cases and digits. Compare counts with `Integer.compare`, and treat the tie rule as part of the contract.

**Example 1.** Input `s = "tree"`, output `"eert"`.

**Example 2.** Input `s = "Aabb"`, output `"bbAa"`, since the uppercase letter has the smaller code.

**Hint.** What does a canonical key throw away that this problem needs? Which two quantities decide where a character goes?

**Changed decision.** The ordering key changes from the character to its count, so the canonical sorted form is no longer the right output.

#### [Recognize] Determine if Two Strings Are Close (LeetCode 1657)
<!-- id: so-two-strings-close -->

**Prerequisites.** All three exercises above.

**Problem.** Two strings are close if one can become the other using any number of these operations: swap any two characters of the string, or choose two characters that both occur in the string and exchange them everywhere. Decide whether two given strings are close. A raw sorted string is not enough.

**Constraints.** 1 <= a.length(), b.length() <= 100000 and both strings consist of lowercase English letters.

**Example 1.** Input `a = "cabbba", b = "abbccc"`, output true.

**Example 2.** Input `a = "aabbc", b = "abbcd"`, output false, since the letter sets differ.

**Hint.** Which facts about the two strings survive both operations? What can the second operation change about which letter owns which count?

**Changed decision.** The signature must forget the identity of the characters while keeping the set of characters and the multiset of counts.
