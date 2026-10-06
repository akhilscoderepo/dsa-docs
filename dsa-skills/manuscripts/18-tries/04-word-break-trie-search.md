<!-- lesson-kind: standard -->
<!-- lesson-id: word-break-trie-search -->
## Cut A String Into Dictionary Words

<!-- stage: context -->
### Why A Hashtag Splitter Builds Many Substrings

A social app splits hashtags such as `thecatsat` into words, so a search for `cat` finds the post. The splitter holds a dictionary of 100,000 words and must decide where the words begin and end. On a hashtag of 1,000 characters, the first version builds more than 500,000 substrings and checks each one in a hash set.

Most of those substrings cannot be words, and the program could have known this after a few characters. This lesson asks how a program lists the dictionary words that begin at one position without building any substring, and how it then uses that list to cut the whole string.

<!-- stage: naive -->
### Testing Every Substring Against A Set

The direct plan takes one start position and tries every end position. It builds the substring and asks a `HashSet<String>` whether the substring is a word.

```java
static List<Integer> endsBySubstring(Set<String> dict, String s, int from) {
    List<Integer> ends = new ArrayList<>();
    for (int to = from + 1; to <= s.length(); to++) {          // every possible end, up to the string end
        if (dict.contains(s.substring(from, to))) ends.add(to);   // builds a new string, then hashes it
    }
    return ends;
}
```

The method returns every end position `to` such that `s[from..to)` is a dictionary word. It is correct, and it does not use the fact that a word and the string must agree letter by letter.

<!-- stage: bottleneck -->
### Counting The Work After The First Mismatch

```predict
The string has n = 1,000 characters and no dictionary word starts with the letter at position 0. How many characters does the method above read for this one position, and how many does it need to read?

It builds substrings of length 1, 2, 3 and so on up to 1,000, and it hashes each one, so it reads about 500,000 characters. It needs to read one character, because no word starts with that letter and no longer substring can be a word.
```

For one start position the method costs O(n^2) time, because each of the `n` substrings has a length of O(n) and costs that much to build and hash. The cost does not depend on the dictionary, so it stays high even when the first letter already rules out every word.

The cheap fact is that a dictionary word and the text must agree on every letter from the first. A prefix tree stores those letters on edges. Walking it from the start position reads one letter at a time and stops at the first missing edge.

<!-- stage: insight -->
### Walking The Tree From One Position

The method keeps a **start index** `from` in the string. It begins at the root of the dictionary tree and reads `s[from]`, then `s[from + 1]`, and so on. After `k` letters the current node represents `s[from..from + k)`. No substring is built.

#### Ending At Terminal Nodes

A node with a true terminal flag means that the letters read so far form a dictionary word. The position `from + k` is then a **cut point**, which is an end position where a word that began at `from` can stop. The walk records the cut point and keeps reading, because a longer word may also start at `from`.

#### Stopping At A Dead End

When the next letter has no edge, the walk reached a **dead end**. No dictionary word extends the letters read so far, so no longer cut point can exist. The walk stops, and its list of cut points is exactly the list of dictionary words that begin at `from`. The cost is at most the length of the longest word, and not the length of the string.

#### Cutting The Whole String

To cut the string, the program recurses from each cut point. A call at `from` tries each cut point `e` and calls itself at `e`. A call at the string length succeeds. This search is correct, and the same start index can be reached by different sequences of cuts. The recursion then repeats work, and Chapter 26 shows how to remember results.

<!-- names: start index, cut point, dead end -->

<!-- stage: variables -->
### The Pieces Of State

The walk and the recursion share one tree and four pieces of state.

- **From** is the start index where the current search begins.
- **Node** is the tree node that represents the letters read since `from`.
- **Cut points** are the end positions that the walk recorded, in increasing order.
- **Path** is the list of words chosen by the recursion so far, and it is used only when the program must return a cutting.

The walk changes the node at every letter and appends a cut point at every terminal node. The recursion changes `from` to a cut point, and the path grows by one word.

<!-- stage: trace -->
### Following The Walk And The Recursion

#### Listing The Words From One Position

The first trace reads `catsand` from position 0. The dictionary holds `cat`, `cats`, `and`, `sand` and `dog`. The pointer `i` marks the letter under test, and `cuts` lists the cut points recorded so far.

The letters `c`, `a` and `t` follow edges, and the node after `t` is terminal, so the walk records the cut point 3. The letter `s` follows an edge to a second terminal node and records 4. The next letter `a` has no edge below `cats`, so the walk reaches a dead end and stops. The words that begin at position 0 are `cat` and `cats`.

#### Repeating A Start Index

The second trace cuts `aaab` with the dictionary `a` and `aa`. The recursion cannot succeed, because `b` is not a word. The pointer `from` marks the start index of each call, and `visits` counts how many calls so far began at that index.

The start index 2 is reached twice, once through `a`, `a` and once through `aa`. The start index 3 is reached three times, and the call at index 3 fails each time. The same suffix is searched again for every different way to reach it.

#### Stepping Through Both Searches

```trace
{"cells":["c","a","t","s","a","n","d"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"cuts":"[]"},"note":"The letter c has an edge, so the walk moves to the node for c."},{"at":{"i":1},"vars":{"cuts":"[]"},"note":"The letter a has an edge, so the walk moves to the node for ca."},{"at":{"i":2},"vars":{"cuts":"[3]"},"note":"The letter t has an edge, so the walk moves to the node for cat. The node is terminal, so the walk records the cut point 3."},{"at":{"i":3},"vars":{"cuts":"[3, 4]"},"note":"The letter s has an edge, so the walk moves to the node for cats. The node is terminal, so the walk records the cut point 4."},{"at":{"i":4},"vars":{"cuts":"[3, 4]"},"note":"The node for cats has no edge for a, so the walk reaches a dead end and stops."}]}
```

```trace
{"cells":["a","a","a","b"],"pointers":["from"],"steps":[{"at":{"from":0},"vars":{"visits":1},"note":"The call at index 0 finds the cut points [1, 2]."},{"at":{"from":1},"vars":{"visits":1},"note":"The call at index 1 finds the cut points [2, 3]."},{"at":{"from":2},"vars":{"visits":1},"note":"The call at index 2 finds the cut points [3]."},{"at":{"from":3},"vars":{"visits":1},"note":"The call at index 3 finds no cut point, so it fails."},{"at":{"from":3},"vars":{"visits":2},"note":"The call at index 3 finds no cut point, so it fails. This index was visited before, so the search repeats its work."},{"at":{"from":2},"vars":{"visits":2},"note":"The call at index 2 finds the cut points [3]. This index was visited before, so the search repeats its work."},{"at":{"from":3},"vars":{"visits":3},"note":"The call at index 3 finds no cut point, so it fails. This index was visited before, so the search repeats its work."}]}
```

<!-- stage: code -->
### Writing The Cuts In Java

#### Cut Points From One Position

The tree uses 26 slots in each node, so the dictionary and the string must hold lowercase letters only. The method `cuts` returns the cut points in increasing order, and the method `cut` at the end of the class uses it to cut the whole string.

```java
final class WordCutter {
    private static final class Node {
        final Node[] child = new Node[26];
        boolean terminal;
    }

    private final Node root = new Node();

    WordCutter(String[] dict) {
        for (String w : dict) {
            Node cur = root;
            for (int i = 0; i < w.length(); i++) {
                int s = w.charAt(i) - 'a';
                if (cur.child[s] == null) cur.child[s] = new Node();
                cur = cur.child[s];
            }
            cur.terminal = true;
        }
    }

    List<Integer> cuts(String s, int from) {
        List<Integer> out = new ArrayList<>();
        Node cur = root;
        for (int i = from; i < s.length(); i++) {          // read one letter at a time, no substring
            cur = cur.child[s.charAt(i) - 'a'];
            if (cur == null) break;                        // dead end: no word extends these letters
            if (cur.terminal) out.add(i + 1);              // a word ends after letter i
        }
        return out;
    }

    List<String> cut(String s, int from) {
        if (from == s.length()) return new ArrayList<>();   // the string ended exactly at a cut point
        for (int e : cuts(s, from)) {                       // each word that begins at from
            List<String> rest = cut(s, e);
            if (rest != null) { rest.add(0, s.substring(from, e)); return rest; }   // prepend the chosen word
        }
        return null;                                        // no cut point leads to the end
    }
}
```

#### Cutting The Whole String

The method `cut` returns one cutting, or null when none exists. It tries each cut point in increasing order, so the first word of the answer is the shortest possible.

#### Cost Of The Search

One call of `cuts` costs O(min(n, W)) time, where `W` is the length of the longest dictionary word. The recursion can call `cut` with the same `from` many times, so its running time grows exponentially with `n` on inputs such as `aaaa...ab`. It suits short strings.

<!-- stage: applicability -->
### Recognizing A String That Must Be Cut

#### Spotting The Pattern

The cue is a string that must be divided into dictionary words, where a walk can test every word at a position without building a substring. The invariant is that from a start index, the walk lists exactly the dictionary words that begin there.

#### Finding The False Friend

The false friend is plain recursion that repeats the same suffix. It looks like a finished solution, and its cost doubles when a string adds a letter. Memoization and dynamic programming fix it, and Chapter 26 owns that topic. Until then, the recursion in this lesson is limited to short inputs.

A second false friend is a recursion that branches at every reachable prefix node and not only at terminal nodes. A prefix that is not a word is not a cut point, and the string may also end in the middle of a word.

#### Recognizing The No-Go Cases

The search does not fit when the program needs to count every cutting of a long string or to decide quickly on a long string, because the repeated starts make it too slow. It does not fit either when the dictionary has few short words, and a plain set test of each short substring is simpler.

<!-- stage: exercises -->
### Exercises

#### [Build] Dictionary Ends From One Index (Author exercise)
<!-- id: tr-dictionary-ends-from-index -->

**Prerequisites.** The prefix tree of the previous lessons.

**Problem.** Given an array `dict` of nonempty lowercase words, a lowercase string `s` and an index `from` with `0 <= from <= s.length()`, return the array of all positions `e` with `from < e <= s.length()` such that `s[from..e)` equals an entry of `dict`. List the positions in increasing order.

**Constraints.** The limits are:
- **Count** is `0 <= dict.length <= 10^4`.
- **Length** of each word is `1 <= length <= 20`, and `s.length()` is at most 1000.
- **Characters** are lowercase English letters.
- **Mutation** does not occur; the inputs keep their contents.

**Example 1.** Input `dict = ["cat","cats","and","sand"]`, `s = "catsand"` and `from = 0`, output `[3,4]`.

**Example 2.** Input the same dictionary and `s`, with `from = 5`, output `[]`.

**Hint.** When does the walk record a position? What makes the walk stop before the end of the string?

**Changed decision.** The method lists the words at one position and does no recursion.

#### [Vary] One Valid Segmentation On Short Input (Author exercise)
<!-- id: tr-one-valid-segmentation -->

**Prerequisites.** The previous exercise.

**Problem.** Given an array `dict` of nonempty lowercase words and a lowercase string `s`, return one array of dictionary words whose concatenation equals `s`. Among all valid cuttings, return the one whose first word is the shortest, and apply the same rule to the rest. Return `null` when no cutting exists.

**Constraints.** The limits are:
- **Count** is `0 <= dict.length <= 100`.
- **Length** of each word is `1 <= length <= 10`, and `1 <= s.length() <= 20`.
- **Characters** are lowercase English letters.
- **Mutation** does not occur; the inputs keep their contents.

**Example 1.** Input `dict = ["cat","cats","and","sand","dog"]` and `s = "catsanddog"`, output `["cat","sand","dog"]`.

**Example 2.** Input `dict = ["a","aa"]` and `s = "aaab"`, output `null`.

**Hint.** Which cut point does the recursion try first? What does the recursion return when no cut point leads to the end?

**Changed decision.** The recursion starts a new walk at every cut point, and a failed branch returns null.

#### [Boundary] Prefix Exists But Word Does Not (Author exercise)
<!-- id: tr-prefix-exists-no-word -->

**Prerequisites.** The two exercises above.

**Problem.** Given an array `dict` of nonempty lowercase words and a lowercase string `s`, return the number of positions `i` in `0..s.length()-1` where the walk from `i` reads at least one letter and records no cut point. The walk stops at a dead end or at the end of the string.

**Constraints.** The limits are:
- **Count** is `0 <= dict.length <= 100`.
- **Length** of each word is `1 <= length <= 10`, and `0 <= s.length() <= 100`.
- **Characters** are lowercase English letters.
- **Mutation** does not occur; the inputs keep their contents.

**Example 1.** Input `dict = ["cats"]` and `s = "catcat"`, output 2.

**Example 2.** Input `dict = ["apple","pen"]` and `s = "applepen"`, output 2.

**Hint.** What does the walk do when the string ends before a word ends? When does the walk read zero letters?

**Changed decision.** The method counts positions where a prefix of a word matches but no word does.

#### [Recognize] Explain Trie-Based Word Break State (Author exercise)
<!-- id: tr-word-break-state-count -->

**Prerequisites.** The previous three exercises.

**Problem.** Given an array `dict` of nonempty lowercase words and a lowercase string `s`, run the plain recursion that calls itself once for every cut point of the current start index and never stops early. The call at the string length counts as a call. Return an array of two numbers: the total number of calls and the number of different start indices among those calls.

**Constraints.** The limits are:
- **Count** is `0 <= dict.length <= 100`.
- **Length** of each word is `1 <= length <= 10`, and `1 <= s.length() <= 20`.
- **Characters** are lowercase English letters.
- **Mutation** does not occur; the inputs keep their contents.

**Example 1.** Input `dict = ["a","aa"]` and `s = "aaab"`, output `[7,4]`.

**Example 2.** Input `dict = ["ab"]` and `s = "abab"`, output `[3,3]`.

**Hint.** What does the state of one call consist of? When can two calls have the same state?

**Changed decision.** The method measures the repeated states and builds no cutting.
