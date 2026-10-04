<!-- lesson-kind: standard -->
<!-- lesson-id: word-break-trie-search -->
## Word-Break Trie Search

<!-- stage: context -->
### The Banner Painter Of Wick Lane

Old Wick, the sign painter, receives orders from shopkeepers who write their slogans with no spaces at all, because the paper they use is narrow. An order reads `catsanddog`, and Wick must paint it on a banner with gaps between the words. The town council has given him a short list of approved words, and a banner is only valid if every piece between gaps is on that list.

Wick works from the left. At the first letter he asks which approved words begin there, and for each one he sets a gap after it and carries on from the next letter. Some words that begin at a given letter are short and some are long, and a long approved word can swallow a short one, as `cats` does with `cat`. He wants a quick way to list every approved word that begins at the current letter.

<!-- stage: naive -->
### Cut Every Piece And Look It Up

The direct method keeps the approved words in a hash set. From a given position, it cuts a piece of every possible length, from one letter to the end of the banner, and looks each piece up in the set. Every piece found is an approved word that begins at that position.

```java
static List<Integer> endsFrom(String banner, int from, Set<String> approved) {
    List<Integer> ends = new ArrayList<>();
    for (int to = from + 1; to <= banner.length(); to++) {
        if (approved.contains(banner.substring(from, to))) ends.add(to);
    }
    return ends;
}
```

The method returns the right ends for any list of words, in increasing order, and it is the natural first attempt.

<!-- stage: bottleneck -->
### Pieces Are Cut After Hope Is Gone

Each call cuts banner.length() - from pieces, and every piece is a fresh string whose hashing reads all of its letters. For a banner of n letters, one call costs O(n^2) letter reads, and a search that calls it from every position costs O(n^3). A banner of two thousand letters means billions of reads.

Most of that work is hopeless. Once the piece `qx` is not the beginning of any approved word, longer pieces such as `qxa` and `qxab` cannot be approved either, yet the method still cuts and hashes them. The longest approved word may have ten letters and the banner two thousand. What is needed is a way to keep reading letters one at a time and to stop at the first letter that leaves every approved word behind, so a call costs at most the length of the longest approved word and cuts no string at all.

<!-- stage: insight -->
### Let One Walk List All The Ends

Put the approved words into a trie. From a **start index** i, set a cursor at the root and feed it the banner letters i, i + 1, i + 2 and so on. After each letter, the cursor stands on the node for the piece read so far. Whenever that node is flagged, the piece is an approved word, and its end is the next position, so this is a **terminal stop**. The walk then continues, because a longer approved word may still follow, and cats continues past cat.

The walk ends at a **dead end**: the first letter for which the cursor's node has no edge. At that moment no approved word is a beginning of the remaining text, so nothing further along can be a word either. One walk from one start index therefore reports exactly the approved words that are beginnings of the suffix, and it reads at most as many letters as the longest approved word, since the trie has no deeper node.

A segmentation continues only from terminal stops. A node that merely lies on the route to a longer word, such as the node for `ca` inside `cat`, is not a place to put a gap, and treating it as one would accept `ca` as a piece.

The invariant is that a walk from start index i, after reading k letters, stands on the node for the first k letters of the suffix, and the flagged nodes met on the way are exactly the approved words that begin at i.

<!-- names: start index, terminal stop, dead end -->

<!-- stage: variables -->
### Start, Cursor And Position

The variable `start` is the first letter of the suffix under study, and it is the whole state of a segmentation attempt: what remains to be split is fully determined by it. A cursor `node` begins at the root for each walk. The position `j` runs from `start` up to the first missing edge or the end of the banner. When `node.word` is true, the position `j + 1` is a valid end and is added to the list. Nothing in the trie is modified by a search, so a recursive attempt may reuse the same trie for every call.

<!-- stage: trace -->
### One Walk And Many Calls

The first trace walks the trie of `cat`, `cats`, `and`, `sand` and `dog` from start index 0 of the banner `catsanddog`. The pointer `i` marks the start and `j` the letter being read. The walk reports a word at `cat` and again at `cats`, and then meets a dead end when the letter `a` has no edge below `cats`, so the remaining letters of the banner are never read.

```trace
{"cells":["c","a","t","s","a","n","d","d","o","g"],"pointers":["i","j"],"steps":[{"at":{"i":0,"j":0},"vars":{"node":"c","ends":""},"note":"The node for c is not flagged, so only the cursor moves."},{"at":{"i":0,"j":1},"vars":{"node":"ca","ends":""},"note":"The node for ca is not flagged, so only the cursor moves."},{"at":{"i":0,"j":2},"vars":{"node":"cat","ends":"3"},"note":"The node for cat is flagged, so 3 is recorded as an end and the walk continues."},{"at":{"i":0,"j":3},"vars":{"node":"cats","ends":"3 4"},"note":"The node for cats is flagged, so 4 is recorded as an end and the walk continues."},{"at":{"i":0,"j":4},"vars":{"node":"cats","ends":"3 4"},"note":"The letter a has no edge below the node for cats, so this is the dead end and the walk stops with the ends found so far."}]}
```

The second trace shows the risk that the lesson leaves open. The banner is `aaab` and the approved words are `a` and `aa`. The recursion tries to split from each terminal stop and fails, because `b` is not approved. The pointer `start` marks the suffix of each call, and `calls` counts all calls so far. Notice that start 2 and start 3 are entered several times, always with the same outcome, so the same question is answered again and again.

```trace
{"cells":["a","a","a","b"],"pointers":["start"],"steps":[{"at":{"start":0},"vars":{"calls":1},"note":"The call for start 0 finds the ends 1, 2 and tries them in order."},{"at":{"start":1},"vars":{"calls":2},"note":"The call for start 1 finds the ends 2, 3 and tries them in order."},{"at":{"start":2},"vars":{"calls":3},"note":"The call for start 2 finds the ends 3 and tries them in order."},{"at":{"start":3},"vars":{"calls":4},"note":"The call for start 3 finds no approved word beginning here, so it answers no."},{"at":{"start":3},"vars":{"calls":5},"note":"The call for start 3 finds no approved word beginning here, so it answers no."},{"at":{"start":2},"vars":{"calls":6},"note":"The call for start 2 finds the ends 3 and tries them in order."},{"at":{"start":3},"vars":{"calls":7},"note":"The call for start 3 finds no approved word beginning here, so it answers no."}]}
```

<!-- stage: code -->
### Ends From An Index And Plain Splitting

```java
final class BannerTrie {
    private static final class Node {
        final Node[] next = new Node[26];
        boolean word;
    }

    private final Node root = new Node();

    void add(String word) {
        Node cur = root;
        for (char c : word.toCharArray()) {
            if (cur.next[c - 'a'] == null) cur.next[c - 'a'] = new Node();
            cur = cur.next[c - 'a'];
        }
        cur.word = true;
    }

    List<Integer> endsFrom(String banner, int start) {
        List<Integer> ends = new ArrayList<>();
        Node cur = root;
        for (int j = start; j < banner.length(); j++) {
            cur = cur.next[banner.charAt(j) - 'a'];
            if (cur == null) break;
            if (cur.word) ends.add(j + 1);
        }
        return ends;
    }

    boolean canSplit(String banner, int start) {
        if (start == banner.length()) return true;
        for (int end : endsFrom(banner, start)) {
            if (canSplit(banner, end)) return true;
        }
        return false;
    }
}
```

One call of `endsFrom` costs O(m), where m is the length of the longest stored word, and cuts no strings. The plain recursion `canSplit` is correct but can repeat a start index many times, so its time can grow exponentially with the banner length.

<!-- stage: applicability -->
### Segmenting With A Word List

Use a trie walk when a string must be broken into dictionary words and every word that begins at a position has to be found quickly: segmenting text without spaces, validating that a code is a concatenation of allowed tokens, and tokenizers with a fixed vocabulary. The invariant is that a walk from a start index visits exactly the stored words that begin there, and it never needs to read past the first dead end.

One false friend is the plain recursion over terminal stops. It looks complete, and on short banners it is, yet the same start index is reached by many routes, so a banner such as many letters `a` followed by `b` takes exponentially many calls to fail. The state of the problem is only the start index, so there are at most n + 1 distinct questions, and remembering answers to them is the cure. The ownership of that technique, memoization and the dynamic programming built from it, is deferred to Chapter 26. A second false friend is gapping at every node on the route, which accepts pieces such as `ca` that are only beginnings.

If the dictionary is tiny and the banner short, the substring and set method is simpler and fast enough. In Java, build no substrings inside the walk, and read letters with `charAt`. Recursion depth equals the number of words in the split, which can be the banner length when single letters are approved.

<!-- stage: exercises -->
### Exercises

#### [Build] Dictionary Ends From One Index (Author exercise)
<!-- id: tn-ends-from-index -->

**Prerequisites.** The insert and search lesson, and the flag at a node.

**Problem.** Given a lowercase string `s`, a list of lowercase dictionary words and a list of start positions, return for each start the list of all positions `e` greater than the start such that `s[start..e)` is a dictionary word, in increasing order. A start equal to the length of `s` gives an empty list.

**Constraints.** 1 <= s.length <= 200, 0 <= words.length <= 100, each word has 1 to 20 letters, and every start is between 0 and s.length inclusive.

**Example 1.** Input `s = "catsanddog"`, `words = ["cat", "cats", "and", "sand", "dog"]`, `starts = [0, 3, 4, 7, 9]`, output `[[3, 4], [7], [7], [10], []]`.

**Example 2.** Input `s = "aaa"`, `words = ["a", "aa", "aaaa"]`, `starts = [0, 1, 2, 3]`, output `[[1, 2], [2, 3], [3], []]`.

**Hint.** When must the walk stop reading letters, and when is an end recorded?

**Changed decision.** An end is recorded at every flagged node while the walk continues, and the walk stops only at a missing edge or the end of the string.

#### [Vary] One Valid Segmentation On Short Input (Author exercise)
<!-- id: tn-one-segmentation -->

**Prerequisites.** The Dictionary Ends From One Index rung.

**Problem.** For a short lowercase string `s` and a list of dictionary words, return one segmentation as the words joined by single spaces, or the empty string if none exists. Try the ends of each start in increasing order, so shorter words are tried first, and stop at the first complete segmentation. Plain recursion is expected.

**Constraints.** 1 <= s.length <= 20, 0 <= words.length <= 30, and each word has 1 to 20 lowercase letters.

**Example 1.** Input `s = "rainbowpath"`, `words = ["rain", "bow", "rainbow", "path", "pa", "th"]`, output `"rain bow pa th"`.

**Example 2.** Input `s = "abx"`, `words = ["a", "ab", "b"]`, output `""`.

**Hint.** From which positions is the recursion allowed to continue, and what ends it successfully?

**Changed decision.** The call returns the path of words instead of a flag, and it continues only from the ends reported by the walk.

#### [Boundary] Prefix Exists But Word Does Not (Author exercise)
<!-- id: tn-prefix-not-word -->

**Prerequisites.** The One Valid Segmentation rung and the terminal stop.

**Problem.** For a short lowercase string `s` and a list of distinct dictionary words, return the number of different ways to split `s` into a sequence of dictionary words. Two splits are different if their cut positions differ. Count by plain recursion that branches only at flagged nodes, so that a route that is merely the beginning of a longer word is never used as a piece.

**Constraints.** 1 <= s.length <= 22, 0 <= words.length <= 30, and each word has 1 to 22 letters.

**Example 1.** Input `s = "aaaa"`, `words = ["a", "aa"]`, output `5`.

**Example 2.** Input `s = "abcd"`, `words = ["abcde", "bc", "a", "d"]`, output `1`.

**Hint.** The node for `abcd` exists in the trie because of `abcde`, so what exactly separates a node that exists from a node that ends a word?

**Changed decision.** The call adds the counts of the continuations from every flagged node, and a node without the flag contributes nothing.

#### [Recognize] Explain Trie-Based Word Break State (Author exercise)
<!-- id: tn-word-break-state -->

**Prerequisites.** The Prefix Exists But Word Does Not rung.

**Problem.** Run the plain recursion that asks whether the suffix from a start index can be split, trying the ends of the start in increasing order and stopping at the first success. Return `[calls, distinctStarts]`, where `calls` is the number of times the recursion was entered, counting the first call, and `distinctStarts` is the number of different start indices among them. The gap between the two numbers is the repeated work.

**Constraints.** 1 <= s.length <= 18, 0 <= words.length <= 20, and each word has 1 to 18 lowercase letters.

**Example 1.** Input `s = "aaaab"`, `words = ["a", "aa"]`, output `[12, 5]`.

**Example 2.** Input `s = "abc"`, `words = ["abc", "ab", "c"]`, output `[3, 3]`.

**Hint.** What do two calls with the same start index have in common, and how many different start indices can exist at most?

**Changed decision.** The question is no longer whether a split exists but how many calls the repeated states cost, which makes the state a single start index visible.
