<!-- lesson-kind: standard -->
<!-- lesson-id: prefix-services -->
## Answer Prefix Queries With A Trie

<!-- stage: context -->
### A Search Box That Scans Every Word

A shop keeps 100,000 product names in memory. A search box sends a request after every keystroke, and each request asks for the total sales of all products whose name starts with the typed text. The code loops over every name and calls `startsWith`. Typing the word "apple" sends five requests, so the code scans the whole list five times.

The list also changes while people type. A product is renamed, a sales figure is overwritten with a corrected value, and a discontinued product is erased. The totals must follow each change at once, or the box shows a number that no longer matches the data.

This lesson asks how to answer a prefix question in time that depends on the length of the prefix and not on the number of stored words. It also asks how to keep that answer correct when words are overwritten, erased and ranked.

The contract is bounded. All words are lowercase English letters, all state lives in memory, and one thread makes every call in order.

<!-- stage: naive -->
### Scanning The Whole Map Per Query

The direct design keeps a map from word to value. A query loops over every entry and adds the value when the word starts with the prefix. An overwrite is a plain `put`, so the map always holds the newest value.

```java
final class NaivePrefixSum {
    private final java.util.Map<String, Integer> value = new java.util.HashMap<>();

    void insert(String key, int val) { value.put(key, val); }      // overwrite is a plain put

    long sum(String prefix) {
        long total = 0;
        for (java.util.Map.Entry<String, Integer> e : value.entrySet())   // visits every stored word
            if (e.getKey().startsWith(prefix)) total += e.getValue();
        return total;
    }
}
```

The answers are correct after every overwrite. The cost of one query does not depend on how many words match.

```predict
The map holds 100,000 words, and a client asks for the sum of the prefix "ap" 1,000 times without any insert in between. How many `startsWith` calls run, and how many words does each query actually need?

The code makes 100,000 times 1,000, which is 100 million calls to `startsWith`. Each query needs only the words that begin with "ap", and that can be a handful. The loop pays for every word, so the number of matches never reduces the work.
```

<!-- stage: bottleneck -->
### Repeated Work On Shared Prefixes

One query costs O(n * p) character comparisons for n stored words and a prefix of length p. The loop cannot skip a word before it reads that word. Ten queries on ten different prefixes cost ten full scans.

The scans also repeat work between words. The words "apple", "apply" and "applet" share the letters "appl". Each query compares those four letters three times, once per word, and every later query compares them again.

Rank queries make the cost worse. A request for the best three words by a score has to collect every matching word and sort them by score, so each keystroke pays a full scan plus a sort. The data has structure that the loop ignores: every prefix of a stored word is a shared starting point for many words.

<!-- stage: insight -->
### Store One Counter On Each Prefix

A **trie** is a tree in which every edge carries one character. The path from the root to a node spells a prefix, so every node stands for exactly one prefix. Words that share letters share the first nodes of their paths. A query for a prefix walks p edges and stops at one node, and that costs O(p) no matter how many words are stored.

#### Counters On The Path

The query needs a number that is ready when the walk ends. Each node stores that number for its prefix. The number is a sum of values, or a **pass count**, which is how many stored words go through the node. Insert walks the key once and adds to the number on every node of the path, so insert also costs O(p).

#### Changing A Value With A Delta

An overwrite must not add the new value on top of the old one. The call needs the **delta**, which is the new value minus the old value. Only the authoritative map from word to value knows the old value, so that map stays next to the trie. The trie holds derived numbers, and the map holds the truth. An erase uses the delta of minus the old value, and a node whose pass count falls to zero can be removed.

#### Branching And Ranking

A spelling checker needs to find stored words that differ from a typed word in exactly one letter. A search for words one letter away follows the query word and, at most once, leaves it to try every other child. A ranked search stores at each node only the words that pass through it. It reads the current counts from the authoritative map when it sorts, so a rank is never stale.

The invariant is that every node holds the exact aggregate of the live words under its prefix, and every public call applies all its node changes or none.

<!-- names: trie, delta, pass count -->

<!-- stage: variables -->
### State Behind A Prefix Service

Four pieces of state take part in each call, and each has one owner.

- **Word map** is the authoritative state, from each stored word to its value or count, and it changes first in every call.
- **Node** is derived state for one prefix, with up to 26 children and its sum or pass count.
- **Delta** is a local number, computed once from the word map and added to every node on the path.
- **Cursor** is the node reached after reading some characters, or a missing node when the prefix matches no word.

The target costs are O(p) per insert, erase and query for a prefix of length p. Memory is O(total characters in the live words). Validation of an erase runs before the first node changes.

<!-- stage: trace -->
### Following Overwrites And Erases

#### Overwriting A Word

The first trace follows the sums stored on the nodes of the path to "apple". The pointer `call` sits on the latest call. Each step lists the nonzero prefix sums, and `delta` shows the number added to every node of the path.

```trace
{"cells":["insert(apple,3)","insert(app,2)","sum(ap)","insert(apple,5)","insert(app,2)","sum(ap)"],"pointers":["call"],"steps":[{"at":{"call":0},"vars":{"sums":"a:3 ap:3 app:3 appl:3 apple:3","delta":"3","result":"-1"},"note":"Call 0: the word is new, so the delta is 3 and every node on the path to apple gains 3."},{"at":{"call":1},"vars":{"sums":"a:5 ap:5 app:5 appl:3 apple:3","delta":"2","result":"-1"},"note":"Call 1: the word is new, so the delta is 2 and every node on the path to app gains 2."},{"at":{"call":2},"vars":{"sums":"a:5 ap:5 app:5 appl:3 apple:3","delta":"-","result":"5"},"note":"Call 2: the walk reads the node for ap and returns 5."},{"at":{"call":3},"vars":{"sums":"a:7 ap:7 app:7 appl:5 apple:5","delta":"2","result":"3"},"note":"Call 3: the old value is 3, so the delta is 2 and every node on the path to apple changes by 2."},{"at":{"call":4},"vars":{"sums":"a:7 ap:7 app:7 appl:5 apple:5","delta":"0","result":"2"},"note":"Call 4: the old value is 2 and the new value is the same, so the delta is 0 and no node changes."},{"at":{"call":5},"vars":{"sums":"a:7 ap:7 app:7 appl:5 apple:5","delta":"-","result":"7"},"note":"Call 5: the walk reads the node for ap and returns 7."}]}
```

Call 3 overwrites "apple" from 3 to 5, so the delta is 2 and the prefix "ap" rises from 5 to 7. The word map keeps app=2 while the sum on the app node rises to 7, because the path to apple passes through that node. Call 4 repeats the value 2 for "app", so the delta is 0 and no node changes.

#### Erasing A Word

The second trace follows pass counts, written as `prefix=pass/end`. The first number counts words that go through the prefix, and the second counts words that end exactly there. An erase of a missing word is checked before any node changes.

```trace
{"cells":["insert(app)","insert(apple)","insert(app)","erase(app)","erase(ap)","countPrefix(app)","erase(apple)","erase(app)","countPrefix(a)"],"pointers":["call"],"steps":[{"at":{"call":0},"vars":{"nodes":"a=1/0 ap=1/0 app=1/1","result":"-"},"note":"Call 0: the pass count rises by 1 on every node of the path to app, and the end count rises on the last node."},{"at":{"call":1},"vars":{"nodes":"a=2/0 ap=2/0 app=2/1 appl=1/0 apple=1/1","result":"-"},"note":"Call 1: the pass count rises by 1 on every node of the path to apple, and the end count rises on the last node."},{"at":{"call":2},"vars":{"nodes":"a=3/0 ap=3/0 app=3/2 appl=1/0 apple=1/1","result":"-"},"note":"Call 2: the pass count rises by 1 on every node of the path to app, and the end count rises on the last node."},{"at":{"call":3},"vars":{"nodes":"a=2/0 ap=2/0 app=2/1 appl=1/0 apple=1/1","result":"true"},"note":"Call 3: a copy of app exists, so every node on its path loses 1 from the pass count and the last node loses 1 from the end count."},{"at":{"call":4},"vars":{"nodes":"a=2/0 ap=2/0 app=2/1 appl=1/0 apple=1/1","result":"false"},"note":"Call 4: no copy of ap is stored, so the call returns false before it changes any node."},{"at":{"call":5},"vars":{"nodes":"a=2/0 ap=2/0 app=2/1 appl=1/0 apple=1/1","result":"2"},"note":"Call 5: the walk reads the pass count of app, which is 2."},{"at":{"call":6},"vars":{"nodes":"a=1/0 ap=1/0 app=1/1","result":"true"},"note":"Call 6: a copy of apple exists, so every node on its path loses 1 from the pass count and the last node loses 1 from the end count."},{"at":{"call":7},"vars":{"nodes":"empty","result":"true"},"note":"Call 7: a copy of app exists, so every node on its path loses 1 from the pass count and the last node loses 1 from the end count."},{"at":{"call":8},"vars":{"nodes":"empty","result":"0"},"note":"Call 8: the walk reads the pass count of a, which is 0."}]}
```

Call 4 asks to erase "ap". That prefix has a pass count of 2 but an end count of 0, so no stored word equals it. The call returns false and leaves every node as it was. Calls 6 and 7 bring the pass count of "a" to zero, and the nodes below it disappear.

<!-- stage: code -->
### A Prefix Sum Structure In Java

The class keeps the word map and the trie in step. It computes the delta from the map once and then walks the key.

```java
final class PrefixSums {
    private static final class Node {
        final Node[] next = new Node[26];
        long sum;                                   // sum of values of live words under this prefix
    }
    private final Node root = new Node();
    private final java.util.Map<String, Integer> value = new java.util.HashMap<>();

    void insert(String key, int val) {
        int old = value.getOrDefault(key, 0);       // the map knows the value being replaced
        value.put(key, val);
        long delta = (long) val - old;              // add only the difference to the path
        Node cur = root;
        for (int i = 0; i < key.length(); i++) {    // one step per character
            int c = key.charAt(i) - 'a';
            if (cur.next[c] == null) cur.next[c] = new Node();
            cur = cur.next[c];
            cur.sum += delta;
        }
    }

    long sum(String prefix) {
        Node cur = root;
        for (int i = 0; i < prefix.length() && cur != null; i++)
            cur = cur.next[prefix.charAt(i) - 'a'];  // a missing child ends the walk
        return cur == null ? 0 : cur.sum;
    }
}
```

An insert or a query costs O(p) time for a key or prefix of length p. The space is O(total characters in the live words) for the nodes plus O(n) for the word map.

<!-- stage: applicability -->
### When A Prefix Index Fits

#### Recognizing The Pattern

The cue is an API that inserts words and then asks about prefixes, wildcard patterns, counts or best matches. Write down what each node must store and which authoritative map can rebuild it. The invariant is that every node describes exactly the live words below it.

#### Choosing What A Node Stores

A sum or a pass count needs a delta on every path node. A one-letter-substitution search needs only the words and a flag for the end of a word. A ranked search needs the set of words under each node and reads the order from the word map. A suffix query needs a second trie built from reversed words.

#### False Friends

A sorted set with `ceiling` and `floor` looks like a prefix tool. It is a false friend when the question asks for a sum or a count, because the range scan still visits every match. A node that caches a rank is also a false friend, since a later count change leaves that cache stale. A plain hash map is the better choice when queries name whole words and never prefixes.

<!-- stage: exercises -->
### Exercises

#### [Build] Map Sum Pairs (LeetCode 677)
<!-- id: sv-prefix-map-sum -->

**Prerequisites.** Hash maps and the trie walk.

**Problem.** Design a class `MapSum`. The call `insert(key, val)` stores `val` for `key`, replaces any earlier value of that key, and returns the earlier value, or -1 when the key is new. The call `sum(prefix)` returns the total of the values of all stored keys that start with `prefix`, or 0 when none does. The rules are this chapter's own and differ from LeetCode, because `insert` returns a value.

**Constraints.** The limits are:
- **Keys and prefixes** are non-empty strings of 1 to 50 lowercase letters.
- **Values** are integers from 1 to 1000.
- **Calls** number at most 10^5, and totals fit in a `long`.
- **Return** of `insert` is an `int`, and of `sum` is a `long`.

**Example 1.** Input calls `insert(apple,3)`, `insert(app,2)`, `sum(ap)`, output -1, -1 and 5.

**Example 2.** Input calls `insert(apple,3)`, `insert(apple,5)`, `insert(app,2)`, `sum(app)`, output -1, 3, -1 and 7.

**Hint.** Which number does the second insert of the same key add to each node?

**Changed decision.** The trie stores sums, so an overwrite adds the difference between the new and old value and not the new value.

#### [Vary] Implement Magic Dictionary (LeetCode 676)
<!-- id: sv-prefix-magic-dictionary -->

**Prerequisites.** The map sum exercise above and recursion on a trie.

**Problem.** Design a class `MagicDictionary`. The call `buildDict(words)` discards any earlier dictionary and stores the given words. The call `search(word)` returns `true` when changing exactly one character of `word` to a different letter produces a stored word, and `false` otherwise. Changing no character does not count.

**Constraints.** The limits are:
- **Words and queries** are strings of 1 to 20 lowercase letters.
- **Dictionary** holds 0 to 100 words, and duplicates are allowed.
- **Calls** number at most 5000.
- **Return** of `search` is a `boolean`.

**Example 1.** Input `buildDict([hello,leetcode])`, then `search(hello)`, `search(hhllo)`, `search(hell)`, output `false`, `true`, `false`.

**Example 2.** Input `buildDict([abc,abd])`, then `search(abc)`, `search(xyz)`, then `buildDict([zzz])`, `search(abc)`, output `true`, `false`, `false`.

**Hint.** What does the walk carry besides the node, so that a second change is refused?

**Changed decision.** The walk follows the query word and may branch to a different child once, so it carries a flag that records whether the one change is used.

#### [Boundary] Implement Trie II (LeetCode 1804)
<!-- id: sv-prefix-trie-counts -->

**Prerequisites.** The two exercises above.

**Problem.** Design a class `TrieCounts`. The call `insert(word)` adds one copy of `word`. The call `countEqual(word)` returns how many copies of `word` are stored. The call `countPrefix(prefix)` returns how many stored copies start with `prefix`. The call `erase(word)` removes one copy and returns `true`, or returns `false` and changes nothing when no copy is stored.

**Constraints.** The limits are:
- **Words and prefixes** are strings of 1 to 50 lowercase letters.
- **Calls** number at most 10^5.
- **Copies** of one word are unlimited, and counts fit in an `int`.
- **Erase** of a word that is only a prefix of stored words returns `false`.

**Example 1.** Input calls `insert(apple)`, `insert(apple)`, `insert(app)`, `countEqual(apple)`, `countPrefix(app)`, `erase(apple)`, `countPrefix(app)`, output 2, 3, `true` and 2 for the last four.

**Example 2.** Input calls `insert(cat)`, `erase(car)`, `erase(ca)`, `countPrefix(ca)`, `erase(cat)`, `erase(cat)`, `countPrefix(c)`, output `false`, `false`, 1, `true`, `false` and 0.

**Hint.** Which check must pass before the first node count goes down?

**Changed decision.** An erase can fail, so the call first confirms that a copy exists and only then lowers the pass count along the path.

#### [Recognize] Design Search Autocomplete System (LeetCode 642)
<!-- id: sv-prefix-autocomplete -->

**Prerequisites.** All three exercises above.

**Problem.** LeetCode marks this problem as premium, so the contract below is the one this lesson checks and may differ in detail. Design a class `Autocomplete` built from arrays `sentences` and `times` that give each starting sentence and its count. The call `input(c)` receives one character. A letter or a space extends the typed text and returns the best three stored sentences that start with the typed text, ordered by larger count first and then by smaller `String.compareTo`. The character `#` ends the typed text, adds one to the count of that text, and returns an empty list. An empty typed text at `#` changes nothing.

**Constraints.** The limits are:
- **Characters** are lowercase letters, the space, and `#`.
- **Sentences** have 1 to 100 characters, and the start list has 0 to 100 sentences.
- **Calls** number at most 5000.
- **Return** is a list of at most three sentences.

**Example 1.** Input `["i love you","island","iroman","i love leetcode"]` with times `[5,3,2,2]`, then `input(i)`, `input( )`, `input(a)`, `input(#)`, output the lists `[i love you, island, i love leetcode]`, `[i love you, i love leetcode]`, `[]` and `[]`.

**Example 2.** Input the same start, then `input(i)`, `input( )`, `input(a)`, `input(#)`, `input(i)`, `input( )`, output the same four lists, then `[i love you, island, i love leetcode]` and `[i love you, i love leetcode, i a]`.

**Hint.** Where does the order of the matches come from when the counts change after a build?

**Changed decision.** Each node lists only the sentences under its prefix, and the sort reads current counts from the word map, so the order is never stale.
