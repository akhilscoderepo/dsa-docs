<!-- lesson-kind: standard -->
<!-- lesson-id: aho-corasick -->
## Match Many Patterns In One Pass

<!-- stage: context -->
### Why A Longer List Slows Every Scan

A moderation service checks each posted message against a blocklist. With 40 blocked words the check finishes instantly. Then the policy team imports a list of 20,000 entries, and the posting endpoint starts missing its latency budget. The code did not change. It still loops over the list and asks, for each entry, whether the message contains it. The work per message now grows with the size of the list, even when the message is a single short sentence.

The same shape appears in log scanners that look for known error signatures, in intrusion detection that checks packets against attack strings, and in editors that highlight many keywords at once. In every case the text arrives once, while the patterns are many and fixed. The question for this lesson is how to read each character of the text one time and still find every occurrence of every pattern, including occurrences that overlap or sit inside one another.

This lesson assumes you know the trie from chapter 18 and the level-order traversal with a queue from chapter 16. It adds one idea on top of them, a way to continue a match after a mismatch without rereading the text.

<!-- stage: naive -->
### Searching For Each Pattern Alone

The direct approach treats the patterns one at a time. For each pattern, try every start position in the text and compare characters until the pattern matches or a character differs. The code below counts every occurrence of every pattern, overlapping ones included.

```java
static int countAll(String text, String[] patterns) {
    int total = 0;
    // One full pass over the text for each pattern.
    for (String p : patterns) {
        for (int start = 0; start + p.length() <= text.length(); start++) {
            // startsWith compares in place and allocates no substring.
            if (text.startsWith(p, start)) total++;
        }
    }
    return total;
}
```

This code is correct, and for a handful of patterns it is fast enough. It also reports overlapping matches, because every start position is tested on its own.

```predict
A text has n characters and the pattern list has k patterns of length m each. In the worst case, how many character comparisons does this method make, and what happens when k grows from 40 to 20,000 while the text stays the same?

The worst case is about n * k * m comparisons, because every pattern tries every start and may compare m characters before a mismatch. Raising k by a factor of 500 raises the work by the same factor, even though the text did not change.
```

<!-- stage: bottleneck -->
### Counting The Repeated Reads

Let `n` be the text length, `k` the number of patterns and `m` the longest pattern. The method above makes up to `n * k * m` character comparisons, which is O(n * k * m). Take `n = 100,000`, `k = 20,000` and `m = 10`. That is 2 * 10^10 comparisons for one message-sized scan, far beyond what a request can afford. Even with `startsWith` and no substring allocation, the count of comparisons is the problem.

#### Two Kinds Of Repeated Work

The first repeated work is the loop over patterns. The text character at position `i` is read again for every pattern, so the text is read `k` times in total. Patterns that share a beginning, such as `she` and `shell`, compare the same first three characters twice at the same start.

The second repeated work is the restart after a mismatch. Take the patterns `hers` and `she` on the text `ushers`. The attempt for `she` reads `s`, `h`, `e` and succeeds at position 1. The attempt for `hers` starts at position 2 and reads `h`, `e`, `r`, `s`. Those characters `h` and `e` were already read as part of the match for `she`. Each attempt forgets what the previous attempts learned, so the same characters are read again.

#### What A Fix Must Provide

A better method must satisfy two conditions at once. It must share the reading of common prefixes across patterns, and it must keep, after each text character, enough knowledge to continue without going back. The trie from chapter 18 supplies the first condition. The second condition needs one extra piece of information for every trie node, and the next stage defines it.

<!-- stage: insight -->
### Sharing One Trie Across Patterns

Build one trie over all patterns, then read the text once while keeping a single current node. The current node stands for the longest part of the text just read that is still a prefix of some pattern. Three additions to the plain trie make this work.

<!-- names: failure link, output link, goto transition -->

#### A Failure Link Keeps The Longest Useful Suffix

Let `s` be the string spelled by the path from the root to a node `v`. The **failure link** of `v` points to the node for the longest proper suffix of `s` that is also a node in the trie, which means it is a prefix of some pattern. The root points to itself. A suffix is proper when it is shorter than `s`.

The link is safe because of one fact. After the text ends with `s`, any partial match that is still alive must be a suffix of `s` that is also a trie prefix. The longest such suffix is the failure link target. The shorter live ones are found by following failure links again from there.

#### The Goto Transition Removes The Retry Loop

The **goto transition** `go[v][c]` is the node reached from `v` after reading the character `c`. If `v` has a child on `c`, that child is the answer. Otherwise the answer is `go[fail[v]][c]`, which means the automaton falls back to the longest useful suffix and tries again there. At the root, a missing child leaves the state at the root.

Filling the full table in advance lets the scan do one array lookup per text character, with no retry loop. The fill runs in level order, the BFS from chapter 16. When the loop handles a node at depth `d`, the failure targets of all nodes at depth `d - 1` and above are known, and their table rows are complete. The failure link of a child `u` of `v` on character `c` is then `go[fail[v]][c]`, one lookup in a finished row.

#### An Output Link Reports Every Match

A node that ends a pattern is a terminal node. Reaching a terminal node means that pattern ends at the current text position. But shorter patterns that are suffixes of that node's string also end here. For the patterns `he` and `she`, reading `she` ends both of them.

The **output link** of `v` points to the nearest node on the failure chain of `v` that is terminal, or to the root when none exists. At each text position the scan reports `v` if it is terminal and then follows output links. The walk visits exactly the patterns that end at this position, so its length equals the number of matches reported.

The invariant ties these pieces together. After reading `text[0..i]`, the current node is the node for the longest suffix of `text[0..i]` that is a prefix of some pattern.

<!-- stage: variables -->
### Four Arrays And One State

The automaton keeps four arrays indexed by trie node, one current state, and the pattern list.

- **go** is a table with one row per node and one column per letter, holding the next node for every letter.
- **fail** holds, for each node, the node of its longest proper suffix that is also a trie prefix.
- **link** holds, for each node, the nearest terminal node on its failure chain, or 0 when none exists.
- **id** holds the index of the pattern that ends at a node, or -1 when no pattern ends there.
- **state** is the node reached after the text read so far, and it starts at the root, node 0.

The alphabet is the 26 lowercase letters, and a letter `c` selects the column `c - 'a'`. Any other character needs a different table, as the applicability stage explains.

<!-- stage: trace -->
### Following The Automaton On Two Texts

#### Failure Links For The First Pattern Set

Take the patterns `he`, `she`, `his` and `hers`. The trie has 10 nodes, numbered in creation order: 0 is the root, 1 is `h`, 2 is `he`, 3 is `s`, 4 is `sh`, 5 is `she`, 6 is `hi`, 7 is `his`, 8 is `her` and 9 is `hers`. The level-order fill gives these failure links for nodes 1 to 9: 0, 0, 0, 1, 2, 0, 3, 0 and 3.

Node 4 (`sh`) points to node 1 (`h`), because `h` is the longest proper suffix of `sh` that is a trie prefix. Node 5 (`she`) points to node 2 (`he`), which is also a terminal node. That single pair is why the output link of node 5 is node 2.

In the trace below, the pointer `i` marks the text position just read. The variable `state` names the string of the current node, and `reported` lists the patterns that end at this position.

#### Scanning The Text ushers

The state stays at the root for `u`, because no pattern starts with `u`. It moves down `s`, `sh` and `she` for the next three letters. At `she` the scan reports `she`, then follows the output link to `he` and reports it as well. The letter `r` has no child below `she`. The table sends the state to `her` through the failure link `he`, which has an `r` child. The final letter `s` reaches `hers`, which is reported.

```trace
{"cells":["u","s","h","e","r","s"],"pointers":["i"],"steps":[{"at":{"i":-1},"vars":{"state":"(root)","reported":"-"},"note":"Before the first letter the state is the root."},{"at":{"i":0},"vars":{"state":"(root)","reported":"-"},"note":"i = 0: letter u. No pattern starts with this letter, so the state stays at the root. No pattern ends here."},{"at":{"i":1},"vars":{"state":"s","reported":"-"},"note":"i = 1: letter s. The state moves from (root) to s. No pattern ends here."},{"at":{"i":2},"vars":{"state":"sh","reported":"-"},"note":"i = 2: letter h. The state moves from s to sh. No pattern ends here."},{"at":{"i":3},"vars":{"state":"she","reported":"she, he"},"note":"i = 3: letter e. The state moves from sh to she. It reports she, he."},{"at":{"i":4},"vars":{"state":"her","reported":"-"},"note":"i = 4: letter r. The child is missing, so the table falls back through he and moves to her. No pattern ends here."},{"at":{"i":5},"vars":{"state":"hers","reported":"hers"},"note":"i = 5: letter s. The state moves from her to hers. It reports hers."}]}
```

#### Scanning The Text babcaa

The second trace uses the patterns `ab`, `bab`, `bc`, `bca`, `c` and `caa`. The text `babcaa` forces several fallbacks. After `bab` the scan reports `bab` and `ab`. The letter `c` has no child below `bab`, so the state falls back along the failure links to `b` and moves to `bc`, which reports `bc` and the pattern `c`. The text is never reread. Every step uses one table lookup and a short walk over output links.

```trace
{"cells":["b","a","b","c","a","a"],"pointers":["i"],"steps":[{"at":{"i":-1},"vars":{"state":"(root)","reported":"-"},"note":"Before the first letter the state is the root."},{"at":{"i":0},"vars":{"state":"b","reported":"-"},"note":"i = 0: letter b. The state moves from (root) to b. No pattern ends here."},{"at":{"i":1},"vars":{"state":"ba","reported":"-"},"note":"i = 1: letter a. The state moves from b to ba. No pattern ends here."},{"at":{"i":2},"vars":{"state":"bab","reported":"bab, ab"},"note":"i = 2: letter b. The state moves from ba to bab. It reports bab, ab."},{"at":{"i":3},"vars":{"state":"bc","reported":"bc, c"},"note":"i = 3: letter c. The child is missing, so the table falls back through ab, b and moves to bc. It reports bc, c."},{"at":{"i":4},"vars":{"state":"bca","reported":"bca"},"note":"i = 4: letter a. The state moves from bc to bca. It reports bca."},{"at":{"i":5},"vars":{"state":"caa","reported":"caa"},"note":"i = 5: letter a. The child is missing, so the table falls back through ca and moves to caa. It reports caa."}]}
```

<!-- stage: code -->
### Building And Scanning In Java

#### Building The Tables

The class below stores the automaton for lowercase letters. It inserts each pattern into a trie, then fills `fail`, `link` and the full `go` table in one level-order pass.

```java
final class Automaton {
    private static final int ALPHABET = 26;
    private final int[][] go;
    private final int[] fail, link, id;

    Automaton(String[] patterns) {
        int cap = 1;
        for (String p : patterns) cap += p.length();
        go = new int[cap][ALPHABET];
        for (int[] row : go) java.util.Arrays.fill(row, -1);
        fail = new int[cap];
        link = new int[cap];
        id = new int[cap];
        java.util.Arrays.fill(id, -1);
        int nodes = 1;
        for (int k = 0; k < patterns.length; k++) {
            int v = 0;
            for (int j = 0; j < patterns[k].length(); j++) {
                int c = patterns[k].charAt(j) - 'a';
                if (go[v][c] == -1) go[v][c] = nodes++;
                v = go[v][c];
            }
            id[v] = k;
        }
        int[] queue = new int[nodes];
        int head = 0, tail = 0;
        for (int c = 0; c < ALPHABET; c++) {
            int u = go[0][c];
            if (u == -1) go[0][c] = 0; else queue[tail++] = u;
        }
        while (head < tail) {
            int v = queue[head++];
            int f = fail[v];
            link[v] = id[f] >= 0 ? f : link[f];
            for (int c = 0; c < ALPHABET; c++) {
                int u = go[v][c];
                if (u == -1) go[v][c] = go[f][c];
                else { fail[u] = go[f][c]; queue[tail++] = u; }
            }
        }
    }

    // Calls handler(endIndex, patternIndex) for every occurrence.
    void scan(String text, java.util.function.BiConsumer<Integer, Integer> handler) {
        int v = 0;
        for (int i = 0; i < text.length(); i++) {
            int c = text.charAt(i) - 'a';
            if (c < 0 || c >= ALPHABET) throw new IllegalArgumentException("not a-z at " + i);
            v = go[v][c];
            for (int m = id[v] >= 0 ? v : link[v]; m != 0; m = link[m]) handler.accept(i, id[m]);
        }
    }
}
```

The array `go` has `cap` rows, which is the total pattern length plus one. That is an upper bound on the node count, because every inserted character creates at most one node.

#### Cost And Java Details

Building costs O(L * 26) time and space, where `L` is the total length of the patterns, because the table has `L + 1` rows of 26 entries. The scan costs O(n + z) time, where `z` is the number of reported matches. Each text character performs one lookup, and each output link followed reports one match.

Two Java details matter. The expression `charAt(j) - 'a'` is an `int`, so it can be used directly as a column index and a stray character produces a value outside 0 to 25, which the scan rejects instead of reading a wrong column. The code never calls `substring`, because index arithmetic is enough for every step.

<!-- stage: applicability -->
### When To Use The Automaton

#### Recognizing The Pattern

Reach for this method when a fixed set of patterns must be matched against one text or one stream, and the answer needs every occurrence, a count per pattern, or a yes or no after each character. The signal in a statement is the word "stream" or "any of these words", together with patterns that may overlap or contain one another. The invariant to state before coding is that the current node is the longest suffix of the text read so far that is a prefix of some pattern.

#### The Nearest False Friend

Running KMP once per pattern is the nearest false friend. KMP is the single-pattern case of the same idea, and it is correct, but `k` patterns need `k` passes and the cost returns to O(n * k). A second false friend is following only the failure link and testing only the current node for a terminal mark. That code finds `she` and misses `he`, because the nearest pattern end sits on the failure chain and not at the node itself. The output link or a precomputed count per node prevents the miss.

#### When Not To Use It

Do not use the table when the alphabet is large, such as arbitrary Unicode text. A table row per node then wastes memory, and a hash map per node is the better storage. Do not use it for a single pattern, where KMP needs less memory. Do not use it when patterns change between queries, because insertion invalidates the failure links and forces a rebuild. Patterns with wildcards or character classes also fall outside the method.

<!-- stage: exercises -->
### Exercises

#### [Build] Trie Failure Links (Author exercise)
<!-- id: as-trie-failure-links -->

**Prerequisites.** The trie from chapter 18, the level-order traversal from chapter 16 and the failure link definition in this lesson.

**Problem.** Given an array `patterns` of distinct non-empty strings over the letters `a` to `z`, insert the patterns in order into a trie. Number the root 0 and number every other node in the order it is created. For a node `v` whose path spells the string `s`, the failure link of `v` is the node whose string is the longest proper suffix of `s` that is also a trie node's string. The root's failure link is the root. Return an `int[]` whose entry `v` is the failure link of node `v`, with one entry per node.

**Constraints.** The limits are:
- **Patterns** satisfy `1 <= patterns.length <= 1000`, and all patterns are distinct.
- **Length** of each pattern is at least 1, and the total length is at most 10^4.
- **Letters** are lowercase `a` to `z` only.
- **Answer** is an `int[]` of length equal to the node count, and entry 0 is 0.
- **Mutation** does not occur; `patterns` does not change.

**Example 1.** Input `["he","she","his","hers"]`, output `[0,0,0,0,1,2,0,3,0,3]`.

**Example 2.** Input `["abab","baba"]`, output `[0,0,5,6,7,0,1,2,3]`, a chain in which each deep node falls back to a deep node.

**Hint.** Process the nodes in order of depth. When you handle node `v` and its child `u` on letter `c`, which already finished row gives the link of `u`?

**Changed decision.** Basic case: the fallback of a child comes from the finished row of its parent's fallback and not from a fresh search.

#### [Vary] Multi-Pattern Scan (Author exercise)
<!-- id: as-multi-pattern-scan -->

**Prerequisites.** The failure link exercise above and the output link in this lesson.

**Problem.** Given distinct non-empty patterns over `a` to `z` and a text over `a` to `z`, count for every pattern how many times it occurs in the text. An occurrence is a start index at which the pattern equals the text characters for its whole length. Occurrences may overlap. Return an `int[]` whose entry `k` is the number of occurrences of `patterns[k]`. This changes the previous task by consuming a text and reporting all terminal outputs at each position.

**Constraints.** The limits are:
- **Patterns** satisfy `1 <= patterns.length <= 1000`, all distinct, with total length at most 10^4.
- **Text** has length `0 <= text.length() <= 10^5`.
- **Letters** are lowercase `a` to `z` only, in patterns and text.
- **Answer** is an `int[]` of length `patterns.length`, and every count fits in an `int`.
- **Mutation** does not occur; neither input changes.

**Example 1.** Input patterns `["he","she","his","hers"]` and text `"ushers"`, output `[1,1,0,1]`.

**Example 2.** Input patterns `["a","aa"]` and text `"aaaa"`, output `[4,3]`, because overlapping occurrences all count.

**Hint.** After each text character, which patterns end here? Think of the current node and then of the nodes reachable from it by output links.

**Changed decision.** The automaton now walks a text, and every position can report several patterns instead of at most one.

#### [Boundary] Suffix Pattern Matches (Author exercise)
<!-- id: as-suffix-pattern-matches -->

**Prerequisites.** The multi-pattern scan above.

**Problem.** Given distinct non-empty patterns over `a` to `z` and a text over `a` to `z`, return an `int[]` `ends` of length `text.length()`, where `ends[i]` is the number of patterns that occur in the text and finish at index `i`. A pattern finishes at `i` when it equals the text characters from `i - length + 1` through `i`. Some patterns are suffixes of other patterns, so one text position can end several patterns, and a count that reads only the current node misses the shorter ones.

**Constraints.** The limits are:
- **Patterns** satisfy `1 <= patterns.length <= 1000`, all distinct, with total length at most 10^4.
- **Text** has length `0 <= text.length() <= 10^5`.
- **Letters** are lowercase `a` to `z` only.
- **Answer** is an `int[]` of length `text.length()`, and each entry is at most `patterns.length`.
- **Mutation** does not occur; neither input changes.

**Example 1.** Input patterns `["he","she","hers"]` and text `"ushers"`, output `[0,0,0,2,0,1]`.

**Example 2.** Input patterns `["a","aa","aaa"]` and text `"aaaa"`, output `[1,2,3,3]`, where every shorter pattern is a suffix of the longer ones.

**Hint.** If the current node is `aaa`, which other patterns end at the same position? Which link leads to each of them?

**Changed decision.** A node carries the matches inherited from its failure chain as well as its own, so the count at a node includes its fallback's count.

#### [Recognize] Stream of Characters (LeetCode 1032)
<!-- id: as-stream-of-characters -->

**Prerequisites.** The multi-pattern scan and suffix matches above.

**Problem.** Design a class `StreamChecker`. Its constructor takes an array `words` of distinct non-empty strings over `a` to `z`. Its method `query(char letter)` appends `letter` to the end of an internal stream, which starts empty and is never cleared. It returns `true` exactly when some word in `words` is a suffix of the whole stream so far, and `false` otherwise. The method returns one boolean and does not say which word matched or how many did. The automaton state must persist between calls to `query`.

**Constraints.** The limits are:
- **Words** satisfy `1 <= words.length <= 2000`, all distinct, with total length at most 10^4.
- **Calls** to `query` number at most 4 * 10^4.
- **Letters** are lowercase `a` to `z` only, in words and queries.
- **Answer** of each call is a `boolean`.
- **Mutation** does not occur on `words`; the stream is only appended to.

**Example 1.** Input words `["rat","at","tea"]` and queries `r,a,t,e,a`, output `false,false,true,false,true`.

**Example 2.** Input words `["abcd","bc"]` and queries `a,b,c,d,c`, output `false,false,true,true,false`; the third query is true only because `bc` is inherited through a failure link.

**Hint.** The state must survive between calls. Can the answer for a node be decided once, when the automaton is built, so that each query is one lookup?

**Changed decision.** The text is no longer a finished string, so the scan loop becomes a single step that keeps the node between calls.
