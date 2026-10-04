<!-- lesson-kind: combination -->
<!-- lesson-id: sorted-letter-groups -->
## Group Strings By Sorted Letters

<!-- stage: context -->
### A Word Tool That Compares Every Pair

A word-game tool shows players all words that use the same letters, so `rat`, `tar` and `art` appear together. The first version takes each new word and compares it with every group found so far. On a list of 200 words it answers at once. On the full dictionary of 100000 words, it runs for hours, and the order of its groups depends on the order of the list.

The comparison itself is correct, but the tool repeats it for every pair of a word and a group. This lesson answers one question. What single value can the tool compute for each word, so that two words belong together exactly when their values are equal?

<!-- stage: contributions -->
### What Each Of The Three Parts Adds

Each earlier topic supplies one part of the answer, and none of them suffices alone.

The string supplies the characters in order. A loop over `toCharArray` reads every letter once, but the order of letters differs between words of the same group, so the raw string cannot serve as a group name.

The sort supplies a standard order. When two words contain the same letters, the same number of times, sorting their characters gives the same sequence. Two words with different letter counts give different sequences. The sorted sequence is therefore a name that depends only on the letters.

The map supplies the grouping. A `HashMap` from a name to a list of words puts every word into the right list in expected constant time. The map cannot decide what the name is, and the sort cannot collect the words. The combined question is how to name each word by its letters and collect the words that share a name.

<!-- stage: naive -->
### Comparing A Word With Every Group

The direct method keeps a list of groups. For each word, it sorts the letters of the word and of the first member of each group, and it compares the two results. A match adds the word to the group, and no match starts a new group.

```java
static List<List<String>> groupWords(String[] words) {
    List<List<String>> groups = new ArrayList<>();
    for (String w : words) {
        boolean placed = false;
        for (List<String> g : groups) {
            if (lettersSorted(g.get(0)).equals(lettersSorted(w))) {
                g.add(w);
                placed = true;
                break;
            }
        }
        if (!placed) {
            List<String> g = new ArrayList<>();
            g.add(w);
            groups.add(g);
        }
    }
    return groups;
}

static String lettersSorted(String s) {
    char[] c = s.toCharArray();
    Arrays.sort(c);
    return new String(c);
}
```

On `["rat", "tar", "tab"]` the method returns the groups `[rat, tar]` and `[tab]`.

<!-- stage: bottleneck -->
### Words Are Sorted Again And Again

```predict
The list holds 100000 words that all belong to different groups. About how many pairs of words does the method compare, and how often does it sort the letters of one given word?

Each word meets every earlier group, so the method makes about n * (n - 1) / 2 comparisons, which is roughly 5 billion and O(n^2). The first word of a group is sorted again for every later word, so one word can be sorted tens of thousands of times.
```

The method asks, for each pair of a word and a group, whether the two have the same letters. The answer for a group never changes, yet the method recomputes the sorted letters of the group's first word on every visit. Cost grows with the product of the number of words and the number of groups. A value computed once per word, and stored, would remove the repeated sorting. If that value were also the way to find the group, the search over groups would disappear as well.

<!-- stage: insight -->
### Name Each Word By Its Sorted Letters

The tool should compute a name for each word once and use the name to find the group directly.

#### The Name Depends Only On The Letters

The **canonical form** of a word is the sequence of its letters in sorted order. Two words have the same letters with the same counts exactly when their canonical forms are equal. Sorting removes the order of the letters and keeps their counts, which is the only information that anagrams share. The canonical form of `tar` is `art`, and so is the canonical form of `rat`.

#### Use The Name As A Map Key

A **signature key** is a canonical form that serves as the key of a map. The map sends each key to the list of words that have that key. Building the key for a word of length L costs O(L log L), and one map operation costs expected O(L) for hashing the key. A word is never compared with another word or with a group.

#### The Group Map And Its Invariant

The **group map** is the `HashMap<String, List<String>>` that holds every group. After the loop has read `i` words, the map holds one entry for each distinct canonical form among those words, and each list holds the words with that form in input order. A final pass over the map values yields the groups.

<!-- names: canonical form, signature key, group map -->

#### A Letter-Count Key Is A Variation

A table of letter counts, such as an `int[26]` array turned into a string, also names a group. That key is valid only when the problem fixes the alphabet, for example 26 lowercase letters. The sorted key needs no alphabet, because it sorts whatever characters appear. The count key is a variation of the idea, and it is not the reason the sorted key works.

<!-- stage: variables -->
### Word, Key And Map

The code uses four pieces of state.

- **word** is the string being read, and it never changes.
- **key** is the canonical form of the word, built once per word.
- **groups** is the group map from a key to the list of words with that key.
- **chars** is the character array that holds the word while it is sorted.

The map grows by one list whenever a new key appears, and each list grows by one word per matching input word.

<!-- stage: trace -->
### Building The Groups And The Key

#### Reading Five Words

Take the words `rat`, `tar`, `tab`, `art` and `bat`. The key of `rat` is `art`, so the map gets a new list with `rat`. The key of `tar` is `art`, so `tar` joins the list of `art`. The key of `tab` is `abt` and starts a second list. The word `art` joins the first list, and `bat` joins the second. The map ends with two keys, and the lists are `[rat, tar, art]` and `[tab, bat]`.

#### Building One Key

The key of a word is the result of sorting its characters. Take `tea` and an insertion sort over its characters. The character `e` is smaller than `t`, so it moves left. The character `a` is smaller than both, so it moves to the front. The result `aet` is the key of `tea`, `eat` and `ate`.

#### Stepping Through The Words And The Key

```trace
{"cells":["rat","tar","tab","art","bat"],"pointers":["i"],"steps":[{"at":{"i":-1},"vars":{"groups":"{}"},"note":"Start: the group map is empty."},{"at":{"i":0},"vars":{"word":"rat","key":"art","groups":"{art=[rat]}"},"note":"The key art is new, so the map gets a list with rat."},{"at":{"i":1},"vars":{"word":"tar","key":"art","groups":"{art=[rat, tar]}"},"note":"The key art exists, so tar joins its list."},{"at":{"i":2},"vars":{"word":"tab","key":"abt","groups":"{art=[rat, tar], abt=[tab]}"},"note":"The key abt is new, so the map gets a list with tab."},{"at":{"i":3},"vars":{"word":"art","key":"art","groups":"{art=[rat, tar, art], abt=[tab]}"},"note":"The key art exists, so art joins its list."},{"at":{"i":4},"vars":{"word":"bat","key":"abt","groups":"{art=[rat, tar, art], abt=[tab, bat]}"},"note":"The key abt exists, so bat joins its list."},{"at":{"i":5},"vars":{"groups":"{art=[rat, tar, art], abt=[tab, bat]}"},"note":"The loop ends. The map holds two keys and five words."}]}
```

```trace
{"cells":["t","e","a"],"pointers":["i","j"],"steps":[{"at":{"i":0,"j":-1},"vars":{"chars":"tea"},"note":"Start: the character at index 0 is a sorted prefix of length 1."},{"at":{"i":1,"j":0},"vars":{"chars":"tea"},"note":"The character e is smaller than t. Swap them."},{"at":{"i":2,"j":1},"vars":{"chars":"eta"},"note":"The character a is smaller than t. Swap them."},{"at":{"i":2,"j":0},"vars":{"chars":"eat"},"note":"The character a is smaller than e. Swap them."},{"at":{"i":3,"j":-1},"vars":{"key":"aet"},"note":"The characters are sorted, so the key of tea is aet."}]}
```

<!-- stage: code -->
### One Pass With A Map

#### Grouping By Sorted Letters

```java
static List<List<String>> groupWords(String[] words) {
    Map<String, List<String>> groups = new HashMap<>();
    for (String word : words) {
        char[] chars = word.toCharArray();
        Arrays.sort(chars);
        String key = new String(chars);
        groups.computeIfAbsent(key, k -> new ArrayList<>()).add(word);
    }
    return new ArrayList<>(groups.values());
}
```

The call `computeIfAbsent(key, ...)` returns the list stored under `key`, and it first creates an empty list when the key is missing. The line therefore replaces a `get` followed by a null check and a `put`.

#### What The Method Costs

Let n be the number of words and L the length of the longest word. Each word costs O(L log L) to sort and expected O(L) to hash. The total time is O(n * L log L). The map and its lists hold every word once, so the space is O(n * L). The iteration order of `groups.values()` is not specified, so a caller that needs a fixed order of groups must sort the keys.

<!-- stage: applicability -->
### When Sorted Letters Name A Group

#### Look For Equal Letters With Equal Counts

Use a sorted key when two items belong together exactly when they hold the same elements the same number of times, and the elements can be sorted. The invariant is that the key depends only on the multiset of elements, and that equal multisets give equal keys. The same idea names groups of numbers by the digits they hold.

#### Where The Key Is Wrong

A false friend is a raw sorted string used when the problem allows a different kind of equivalence. Two strings are close when one becomes the other by swapping any two characters or by exchanging two letters everywhere. Their letters differ, so their sorted strings differ, although the strings are equivalent. The right name there combines the set of letters with the sorted list of counts. A count table is another false friend when the alphabet is not fixed, since a table of 26 entries fails for other characters.

#### Java Details That Cause Failures

Use `new String(chars)` or `String.valueOf(chars)` to build the key, because `chars.toString()` returns the identity of the array object. Two arrays with equal contents have different identities, so a map keyed by arrays never groups anything. Strings are immutable and safe as keys. The order of `HashMap` values is unspecified, so sort the keys when the output order matters.

<!-- stage: exercises -->
### Exercises

#### [Build] Valid Anagram (LeetCode 242)
<!-- id: so-anagram-normalized -->

**Prerequisites.** The canonical form from this lesson.

**Problem.** Let `s` and `t` be strings. Ignore every character that is not a letter, and ignore letter case. Return true when the remaining letters of `s` can be rearranged into the remaining letters of `t`. This version normalizes case and spaces, which the original problem does not.

**Constraints.** The limits are:
- **Length** satisfies `0 <= s.length, t.length <= 10^5`.
- **Characters** are ASCII letters, digits, spaces and punctuation.
- **Letters** `A` and `a` count as the same letter.
- **Answer** is a boolean, and two strings without letters are anagrams of each other.

**Example 1.** Input `s = "Dormitory!"`, `t = "dirty room"`, output true.

**Example 2.** Input `s = "aab"`, `t = "ab b"`, output false.

**Hint.** Which characters enter the canonical form, and in which case are they written before sorting?

**Changed decision.** Basic case: the key keeps only normalized letters, so two strings are compared through their canonical forms.

#### [Vary] Group Anagrams (LeetCode 49)
<!-- id: so-group-sorted-key -->

**Prerequisites.** Valid Anagram above.

**Problem.** Let `words` be an array of strings. Group the words whose letters are rearrangements of each other. Return the groups ordered by their canonical form in ascending order. List the words of each group in their input order. This version fixes the order of the output, and it uses the sorted key and not a count table.

**Constraints.** The limits are:
- **Length** satisfies `0 <= words.length <= 10^4`.
- **Words** have length from 0 to 100 and may contain any character.
- **Empty word** has the canonical form of the empty string and forms its own group.
- **Answer** is a list of lists, and every word appears in exactly one group.

**Example 1.** Input `words = ["rat", "tar", "tab", "art", "bat"]`, output `[["tab", "bat"], ["rat", "tar", "art"]]`, because `abt` sorts before `art`.

**Example 2.** Input `words = ["", "b", ""]`, output `[["", ""], ["b"]]`.

**Hint.** After the map is built, which collection must be sorted so that the groups come out in a fixed order?

**Changed decision.** The output order is part of the contract, so the keys are sorted after the grouping.

#### [Boundary] Sort Characters By Frequency (LeetCode 451)
<!-- id: so-frequency-order -->

**Prerequisites.** The two exercises above.

**Problem.** Let `s` be a string of ASCII characters. Return a string with the same characters, ordered by how often each character occurs, from most often to least often. Characters with equal frequency appear in ascending order of their character code. Equal characters stay together.

**Constraints.** The limits are:
- **Length** satisfies `0 <= s.length <= 10^5`.
- **Characters** have codes from 0 to 127, and case matters.
- **Ties** are resolved by character code, so the answer is unique.
- **Answer** has the same length as `s`.

**Example 1.** Input `s = "mississippi"`, output `"iiiissssppm"`.

**Example 2.** Input `s = "bBaA"`, output `"ABab"`.

**Hint.** Which key groups equal characters, and which second key makes the order of equal frequencies unique?

**Changed decision.** The ordering key is a count and not a canonical form, and equal counts need an explicit tie rule.

#### [Recognize] Determine If Two Strings Are Close (LeetCode 1657)
<!-- id: so-strings-close -->

**Prerequisites.** All three exercises above.

**Problem.** Let `a` and `b` be strings of lowercase letters. Two operations are allowed on `a`. The first swaps any two characters of the string. The second takes two letters that both occur in the string and exchanges them everywhere, so every occurrence of the first becomes the second and every occurrence of the second becomes the first. Return true when some sequence of operations turns `a` into `b`.

**Constraints.** The limits are:
- **Length** satisfies `0 <= a.length, b.length <= 10^5`.
- **Letters** are lowercase English letters only.
- **Different lengths** make the answer false.
- **Answer** is a boolean, and two empty strings are close.

**Example 1.** Input `a = "aabbbc"`, `b = "bccaaa"`, output true.

**Example 2.** Input `a = "aabb"`, `b = "abbb"`, output false.

**Hint.** What must the two strings share about their letters, and what must their lists of counts share after sorting?

**Changed decision.** The raw sorted string is not enough. The key combines the set of letters with the sorted list of counts.
