<!-- lesson-kind: combination -->
<!-- lesson-id: rank-words-by-prefix -->
## Rank Words By Prefix

<!-- stage: context -->
### A Suggestion Box That Lags

A search box shows the three most popular searches that start with the text typed so far. The first version stores every search with its count. On each keystroke it keeps the searches that start with the typed text, sorts them and shows three. With a thousand stored searches nobody notices. With a million, every keystroke costs a full pass, and the suggestions arrive after the user typed the next letter.

A second failure is quieter. Two searches with the same count swap places between calls, because the sort has no rule for ties. The box flickers although no count changed.

This lesson combines prefix navigation with ranking. It asks how to answer "the best three words that start with this text" without touching words that do not start with it, and how to keep that answer exact while counts grow.

<!-- stage: contributions -->
### What The Earlier Lessons Contribute

#### A Walk That Costs One Step Per Letter

The lesson Answer Prefix Queries With A Trie supplied the trie walk. A query follows one child per letter, so its cost depends on the prefix length and not on the number of stored words. That lesson also stored an aggregate in every node on a word's path and repaired it from the record that decides. This lesson keeps the walk and the repair, and it changes what the aggregate is.

#### A Bound And A Tie Rule

The lesson Merge Feeds From Many Sources supplied the rule that a ranked answer keeps only a bounded number of candidates, and that the order of equal candidates is fixed before the bound cuts anything. A feed applies that rule to a merge of several sources. This lesson applies it to the words below one prefix.

#### The Choice This Lesson Adds

The new work is keeping a bounded ranked answer correct while the numbers behind the ranking change. A sum or a count can be repaired by adding a difference. A bounded ranking cannot always be repaired that way, and the lesson shows which changes keep it exact.

<!-- stage: naive -->
### Scanning Every Stored Word

The direct design keeps a map from each word to its count. A query walks the whole map, keeps the words that start with the prefix, sorts them by higher count and then by smaller word, and returns the first three.

```java
final class NaiveRanker {
    private final java.util.Map<String, Integer> count = new java.util.HashMap<>();

    void record(String word) { count.merge(word, 1, Integer::sum); }

    java.util.List<String> top(String prefix) {
        java.util.List<String> hits = new java.util.ArrayList<>();
        for (String w : count.keySet()) {
            if (w.startsWith(prefix)) hits.add(w);       // every stored word is examined
        }
        hits.sort((a, b) -> count.get(a).equals(count.get(b))
                ? a.compareTo(b) : Integer.compare(count.get(b), count.get(a)));
        return hits.size() > 3 ? hits.subList(0, 3) : hits;
    }
}
```

The answers are correct and the order of equal counts is fixed. The cost is the only problem.

```predict
A prefix matches only four of one million stored words. How many words does the query above examine, and how many does the answer need?

It examines all one million words and sorts the four matches. The answer needs only the three best of those four. Almost all of the work is spent on words that the prefix excludes.
```

<!-- stage: bottleneck -->
### Every Keystroke Pays For Every Word

Let n be the number of stored words and L the longest word length. The query tests each word against the prefix, which costs O(n * L) comparisons. It then sorts the matches, which costs O(m log m) for m matches. A prefix of one letter can match most of the words, so m is close to n.

The record call is cheap, but the query is the call that runs on every keystroke. The work that the answer needs is tiny, because it returns at most three words. The cost comes from rebuilding that answer from scratch each time.

A faster design must keep the answer for every prefix ready, and it must pay a small price when a count changes instead of a large price on every query.

<!-- stage: insight -->
### Keep The Best Three At Every Letter

Store the words in a trie. Every **prefix node** stands for one prefix, the text on the path from the root to that node. The root stands for the empty prefix.

#### What Each Node Keeps

Every prefix node keeps a **top list**: the words below it, at most three, in ranked order. A query walks one child per letter to the node of its prefix and returns a copy of that node's top list. The walk costs O(L), and the copy costs at most three entries.

The ranking is the **rank test**: a word comes before another word when its count is higher, and the smaller word comes first when the counts are equal. The test reads the counts from the map that decides. The lists store only words, never counts, so a list cannot hold a stale count.

#### Repairing On Every Record

A record call raises the count of one word by one. It then visits each prefix node on the word's path, from the root to the last letter. At each node it removes the word from the top list if the word is there, finds the word's place by the rank test and inserts it. It cuts the list back to three.

Only the recorded word moved up. Every other word kept its count, so the other entries of each list keep their relative order. A word that was cut from a list earlier cannot belong in it now, because the words in the list only moved up or stayed. The invariant is that every top list holds exactly the best three words below its prefix under the rank test.

<!-- names: prefix node, top list, rank test -->

<!-- stage: variables -->
### One Map And A Trie Of Lists

The service stores one authoritative map and one derived trie.

- **count** maps each recorded word to its number of records and is the structure that decides.
- **Node** holds 26 child links and one list of at most three words.
- **K** is the list bound, fixed at 3.
- **before** applies the rank test to two words and reads both counts from `count`.
- **repair** removes a word from one node's list, reinserts it by `before` and cuts the list to `K`.

A query for a prefix that has no node returns an empty list. A query for the empty prefix reads the root.

<!-- stage: trace -->
### Following Counts And Lists

#### Words Moving Inside A List

The first trace records five words and then asks for the prefix `te`. The pointer `call` moves along the calls in order. The columns show every count, the list at the node for `t` and the list at the node for `te`.

```trace
{"cells":["record(tea)","record(ten)","record(tea)","record(team)","record(tent)","query(te)"],"pointers":["call"],"steps":[{"at":{"call":0},"vars":{"counts":"tea:1","list(t)":"[tea]","list(te)":"[tea]","result":"null"},"note":"Call 0: the count of tea becomes 1, and the call repairs the list of every prefix node on the path of tea."},{"at":{"call":1},"vars":{"counts":"tea:1 ten:1","list(t)":"[tea,ten]","list(te)":"[tea,ten]","result":"null"},"note":"Call 1: the count of ten becomes 1, and the call repairs the list of every prefix node on the path of ten."},{"at":{"call":2},"vars":{"counts":"tea:2 ten:1","list(t)":"[tea,ten]","list(te)":"[tea,ten]","result":"null"},"note":"Call 2: the count of tea becomes 2, and the call repairs the list of every prefix node on the path of tea."},{"at":{"call":3},"vars":{"counts":"tea:2 team:1 ten:1","list(t)":"[tea,team,ten]","list(te)":"[tea,team,ten]","result":"null"},"note":"Call 3: the count of team becomes 1, and the call repairs the list of every prefix node on the path of team."},{"at":{"call":4},"vars":{"counts":"tea:2 team:1 ten:1 tent:1","list(t)":"[tea,team,ten]","list(te)":"[tea,team,ten]","result":"null"},"note":"Call 4: the count of tent becomes 1, and the call repairs the list of every prefix node on the path of tent."},{"at":{"call":5},"vars":{"counts":"tea:2 team:1 ten:1 tent:1","list(t)":"[tea,team,ten]","list(te)":"[tea,team,ten]","result":"[tea,team,ten]"},"note":"Call 5: the query walks to the node for 'te'. The node exists, so the call copies its list."}]}
```

After `record(ten)` the words `tea` and `ten` both have a count of 1, so the smaller word `tea` leads the list of `t`. The second `record(tea)` lifts `tea` to a count of 2, and the call `record(team)` adds a word that starts with `tea`. The query for `te` copies the list of that node and returns it.

#### A Word Returning After A Cut

The second trace uses four words that share the prefix `b`. The list holds three, so the last word is cut when it arrives. The query for `be` ends at a missing child, and the query for the empty prefix reads the root.

```trace
{"cells":["record(ba)","record(bb)","record(bc)","record(bd)","record(bd)","query(b)","query(be)","query()"],"pointers":["call"],"steps":[{"at":{"call":0},"vars":{"counts":"ba:1","list(root)":"[ba]","list(b)":"[ba]","result":"null"},"note":"Call 0: the count of ba becomes 1, and the call repairs the root and the nodes on the path of ba."},{"at":{"call":1},"vars":{"counts":"ba:1 bb:1","list(root)":"[ba,bb]","list(b)":"[ba,bb]","result":"null"},"note":"Call 1: the count of bb becomes 1, and the call repairs the root and the nodes on the path of bb."},{"at":{"call":2},"vars":{"counts":"ba:1 bb:1 bc:1","list(root)":"[ba,bb,bc]","list(b)":"[ba,bb,bc]","result":"null"},"note":"Call 2: the count of bc becomes 1, and the call repairs the root and the nodes on the path of bc."},{"at":{"call":3},"vars":{"counts":"ba:1 bb:1 bc:1 bd:1","list(root)":"[ba,bb,bc]","list(b)":"[ba,bb,bc]","result":"null"},"note":"Call 3: the count of bd becomes 1, and the call repairs the root and the nodes on the path of bd."},{"at":{"call":4},"vars":{"counts":"ba:1 bb:1 bc:1 bd:2","list(root)":"[bd,ba,bb]","list(b)":"[bd,ba,bb]","result":"null"},"note":"Call 4: the count of bd becomes 2, and the call repairs the root and the nodes on the path of bd."},{"at":{"call":5},"vars":{"counts":"ba:1 bb:1 bc:1 bd:2","list(root)":"[bd,ba,bb]","list(b)":"[bd,ba,bb]","result":"[bd,ba,bb]"},"note":"Call 5: the query for 'b' reads the list of the node it reaches."},{"at":{"call":6},"vars":{"counts":"ba:1 bb:1 bc:1 bd:2","list(root)":"[bd,ba,bb]","list(b)":"[bd,ba,bb]","result":"empty"},"note":"Call 6: the query for 'be' ends at a missing child and returns an empty list."},{"at":{"call":7},"vars":{"counts":"ba:1 bb:1 bc:1 bd:2","list(root)":"[bd,ba,bb]","list(b)":"[bd,ba,bb]","result":"[bd,ba,bb]"},"note":"Call 7: the query for '' reads the list of the node it reaches."}]}
```

The word `bd` arrives with a count of 1 and loses the tie to three smaller words, so it is cut. Its second record gives it a count of 2. The call repairs the root, the node for `b` and the node for `bd`. In the first two lists, `bd` now ranks first and pushes `bc` out.

<!-- stage: code -->
### The Word Ranker In Java

The class keeps the map that decides, and each record repairs the lists on one path.

```java
final class WordRanker {
    private static final int K = 3;

    private static final class Node {
        final Node[] next = new Node[26];
        final java.util.ArrayList<String> top = new java.util.ArrayList<>();
    }

    private final java.util.Map<String, Integer> count = new java.util.HashMap<>();
    private final Node root = new Node();

    private boolean before(String a, String b) {
        int ca = count.get(a), cb = count.get(b);
        return ca != cb ? ca > cb : a.compareTo(b) < 0;
    }

    private void repair(Node node, String word) {
        node.top.remove(word);                              // drop the old place of the word
        int at = 0;
        while (at < node.top.size() && before(node.top.get(at), word)) at++;
        if (at < K) {
            node.top.add(at, word);
            if (node.top.size() > K) node.top.remove(K);    // cut the list back to the bound
        }
    }

    void record(String word) {
        count.merge(word, 1, Integer::sum);                 // the map changes first
        Node cur = root;
        repair(cur, word);
        for (int i = 0; i < word.length(); i++) {
            int c = word.charAt(i) - 'a';
            if (cur.next[c] == null) cur.next[c] = new Node();
            cur = cur.next[c];
            repair(cur, word);
        }
    }

    java.util.List<String> top(String prefix) {
        Node cur = root;
        for (int i = 0; i < prefix.length() && cur != null; i++) cur = cur.next[prefix.charAt(i) - 'a'];
        return cur == null ? java.util.List.of() : new java.util.ArrayList<>(cur.top);
    }
}
```

A record call costs O(L * K), because it repairs L + 1 lists of at most K entries. A query costs O(L + K). The space is O(S * K), where S is the number of trie nodes.

<!-- stage: applicability -->
### Bounded Answers Under Change

#### When A Short List Is Enough

A short list per node stays exact only when every change moves a word up the ranking. Counts that only grow, and indexes that only grow, both qualify. A word that falls out of a list cannot return unless it is recorded again, and a record call visits that list. The invariant is that each list equals the best K words below its prefix after every call.

#### False Friends And Limits

A call that lowers a count or deletes a word breaks the shortcut. A word that was cut earlier may now deserve a place, and the three stored words give no way to find it. The fix is to keep every word below the prefix in an ordered set per node and read its first three entries. The set holds immutable entries that carry the count, so a change removes the old entry and inserts a new one. A tree set must never contain an entry whose counted fields change in place.

Skip the lists when queries are rare and writes are frequent, because the repair cost then outweighs the saved scans. A sorted array of all words with binary search is also a valid design for a fixed dictionary that never changes counts.

<!-- stage: exercises -->
### Exercises

#### [Build] Prefix Maximum Under Overwrite (LeetCode 677)
<!-- id: sv-rank-prefix-max -->

**Prerequisites.** The trie walk and the repair from the record that decides.

**Problem.** Design a class `PrefixMax`. The call `put(key, value)` stores `value` for `key` and replaces any earlier value of that key. The call `max(prefix)` returns the largest value among all stored keys that start with `prefix`, or -1 if no stored key starts with it.

**Constraints.** The limits are:
- **Keys** and **prefixes** are lowercase strings of length 1 to 50.
- **Values** are integers from 0 to 10^6, so -1 never collides with a stored value.
- **Calls** number at most `5 * 10^4`.
- **Overwrite** may lower a value.

**Example 1.** Input calls `put(apple,3)`, `put(app,5)`, `max(ap)`, `put(app,2)`, `max(ap)`, `max(b)`, output 5, then 3, then -1.

**Example 2.** Input calls `put(ab,4)`, `put(ab,9)`, `put(ab,1)`, `max(a)`, `put(ac,6)`, `max(a)`, `max(ab)`, output 1, then 6, then 1.

**Hint.** After an overwrite lowers the value of the key that held the maximum, which value is the maximum now?

**Changed decision.** LeetCode sums the values below a prefix. This contract takes the maximum, so a lowered value cannot be repaired by a subtraction and each node keeps all values it covers.

#### [Vary] Count Near Words Within A Budget (LeetCode 676)
<!-- id: sv-rank-near-words -->

**Prerequisites.** The exercise above and the trie walk.

**Problem.** Design a class `NearDictionary` built from an array of words. The call `countWithin(query, d)` returns the number of distinct dictionary words that have the same length as `query` and differ from it in at most `d` positions.

**Constraints.** The limits are:
- **Words** and **queries** are lowercase strings of length 1 to 20.
- **Dictionary** holds at most `10^4` words and may repeat a word.
- **Budget** d is an integer from 0 to 2.
- **Calls** number at most `10^4`.

**Example 1.** Input words `hello`, `hallo`, `hullo`, `help`, `hello` and the calls `countWithin(hello,0)`, `countWithin(hello,1)`, `countWithin(hxllo,1)`, output 1, 3 and 3.

**Example 2.** Input words `abc`, `abd`, `xyz` and the calls `countWithin(abz,1)`, `countWithin(abz,2)`, output 2 and 3.

**Hint.** What should a step do when the letter on the trie edge differs from the query letter?

**Changed decision.** LeetCode asks for exactly one substituted letter and returns a boolean. This contract counts words and spends a branch budget, so a mismatch costs one unit and a repeated word counts once.

#### [Boundary] Prefix And Suffix Filter (LeetCode 745)
<!-- id: sv-rank-affix-filter -->

**Prerequisites.** The two exercises above.

**Problem.** Design a class `WordFilter` built from an array of words. The call `f(prefix, suffix)` returns the largest index `i` such that `words[i]` starts with `prefix` and ends with `suffix`, or -1 if no word does.

**Constraints.** The limits are:
- **Words** are lowercase strings of length 1 to 7, and the array holds at most `10^4` entries.
- **Prefixes** and **suffixes** are lowercase strings of length 0 to 7, and an empty one matches every word.
- **Duplicates** may appear, and the larger index wins.
- **Calls** number at most `10^4`.

**Example 1.** Input words `apple`, `ample`, `maple` and the calls `f(a,e)`, `f(ap,le)`, `f(m,e)`, `f(z,e)`, output 1, 0, 2 and -1.

**Example 2.** Input words `bob`, `bob`, `bo` and the calls `f(bo,b)`, `f(bo,o)`, `f(,b)`, output 1, 2 and 1.

**Hint.** Which single string can encode both the suffix and the prefix of a word so that one walk checks both?

**Changed decision.** One walk must satisfy two constraints at the end of a word and at its start. Each word is inserted once per suffix, and each node stores the largest index, which a later word always overwrites.

#### [Recognize] Autocomplete With Recency Ties (LeetCode 642)
<!-- id: sv-rank-autocomplete -->

**Prerequisites.** All three exercises above.

**Problem.** This chapter writes the contract below itself, and it can differ in detail from LeetCode. Design a class `Autocomplete`. The call `type(c)` appends the character `c` to the current text and returns up to 3 stored sentences that start with that text. The character `#` instead commits the current text as one use of that sentence, clears the text and returns an empty list. The call `retract(sentence)` removes one use of a stored sentence and returns `true`, or returns `false` if the sentence is not stored. Sentences rank by higher use count, then by more recent last use, then by smaller text.

**Constraints.** The limits are:
- **Sentences** hold lowercase letters and spaces, with length 1 to 30, and `#` follows at least one character.
- **Last use** is the order of commits, and `retract` leaves it unchanged.
- **Calls** number at most `10^4`.
- **Count** of uses reaches zero when a sentence is removed.

**Example 1.** Input calls `go#`, `gone#`, `go#`, `ga#` typed one character at a time, then `type(g)`, `type(o)`, `type(#)`, output `[go, ga, gone]`, then `[go, gone]`, then `[]`.

**Example 2.** Input the commits `ab#`, `ab#`, `ac#`, then `retract(ab)`, `type(a)`, `retract(ab)`, `retract(zz)`, `type(c)`, output `true`, `[ac, ab]`, `true`, `false` and `[ac]`.

**Hint.** The counts can fall, so which structure per node can still find the next best sentence after a removal?

**Changed decision.** The tie rule is recency, uses can be retracted and the answer is not bounded by growth. Each node keeps every sentence below it in an ordered set of immutable entries, and a change swaps the old entry for a new one on the whole path.
