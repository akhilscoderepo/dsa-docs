<!-- lesson-kind: combination -->
<!-- lesson-id: prefix-automata-state -->
## Stream Matching With Failure Links

<!-- stage: context -->
### Why A Stream Scanner Leaks Secrets

A log forwarder masks secrets before log lines leave a server. It watches the byte stream for 2,000 forbidden tokens, such as API key prefixes. Bytes arrive in network chunks of any size, so a token can start in one chunk and end in the next. The first version keeps every received character and, after each new character, compares all 2,000 tokens with the end of that buffer. In a load test its memory grows with the stream, and each character costs time proportional to the total length of all tokens. A second version drops its partial progress whenever a character fails to extend a match. That version misses the token `aab` inside the input `aaab`, so the secret reaches the log.

The question of this lesson is how a scanner can keep a small state for each stream, never store the stream, and still report every token that ends at the current character.

<!-- stage: contributions -->
### What The Earlier Lessons Contribute

The lesson Match A Pattern Without Restarting supplied the prefix function, which that lesson stored in an array named `pi`. This lesson calls the same array `fail`, to match the failure links of the trie. For one pattern `p`, the entry `fail[i]` is the length of the longest proper prefix of `p[0..i]` that is also a suffix of it. After a mismatch, the matched length moves to `fail[k - 1]` and the text index stays where it is. The lesson Match Many Patterns In One Pass supplied the trie. Each trie node stands for one prefix of some word, a failure link points to the longest proper suffix of that prefix that is also a node, and an output link reaches the nearest word that ends on that chain.

This lesson reads both ideas as one machine whose only memory is one state. The new step is to keep the machine running after a full match, so that overlapping occurrences are reported, and to keep the state alive between calls, so that the input never has to be stored.

<!-- stage: naive -->
### Comparing Every Word At Every Character

The direct design stores the stream in a `StringBuilder`. After each appended character, it compares every word with the end of the stream and counts the words that agree.

```java
final class NaiveStream {
    private final String[] words;
    private final StringBuilder stream = new StringBuilder();

    NaiveStream(String[] words) { this.words = words; }

    // Returns how many words end at the newest character of the stream.
    int query(char c) {
        stream.append(c);
        int count = 0;
        for (String w : words) {
            int start = stream.length() - w.length();
            if (start < 0) continue;                       // the stream is still shorter than this word
            int j = 0;
            while (j < w.length() && stream.charAt(start + j) == w.charAt(j)) j++;
            if (j == w.length()) count++;                  // every character agreed
        }
        return count;
    }
}
```

With the words `aab`, `ab` and `b`, the queries `a`, `a`, `b` return 0, 0 and 3, because all three words end at the third character. The answers are correct. Each call still reads the whole word list and the whole buffer end again.

```predict
A single word of 1,000 letters `a` followed by one `b` is stored, and the stream is 100,000 letters `a`. About how many character comparisons does the code above make, and how much memory does the stream take?

Every query compares the 1,000 letters `a` of the word against the end of the stream and fails only at the final letter `b`, so it makes about 1,001 comparisons. The run costs about 10^8 comparisons, which is O(n * m) for a stream of n characters and a word of m characters. The buffer holds all 100,000 characters, so memory grows with the stream and never shrinks.
```

<!-- stage: bottleneck -->
### Two Costs That Grow Without Limit

For q queries and words of total length L, the code above costs O(q * L) time. With L = 10^4 and q = 4 * 10^4, that is 4 * 10^8 character reads for a task that only needs one decision per character. The buffer adds O(q) memory, which is unacceptable for a stream that never ends.

The repeated work is easy to name. After the stream `aaaa`, the word `aaab` has matched three characters. At the next query the code reads those same three characters again, from the start of the word, and the query after that reads them again. Information gained at one character is discarded and rebuilt at the next. Restarting from the first character of the word on every mismatch removes some reads but breaks correctness, because the suffix `aa` of `aaa` is already a valid partial match for `aab`. Running a separate single-pattern matcher for each word keeps the reads linear in the stream, but still costs one step per word for every character, which is O(k) per character for k words.

A fix must give four things. It must use constant extra memory per stream, apart from a structure built once from the words. It must do work that does not grow with the number of words. It must keep every partial match that can still succeed. It must report every word that ends at the current character, including words nested inside longer ones.

<!-- stage: insight -->
### One State Summarizes The Whole Stream

#### The Match State

<!-- names: match state, fallback transition, period -->

Read the stream one character at a time and ask one question after each character. What is the longest suffix of the characters read so far that is also a prefix of some stored word? The answer is the **match state**. For one pattern it is a length `k` between 0 and `m`. For many words it is a trie node.

The match state is enough to predict everything that follows. Any word occurrence that is still alive, meaning its first characters are already in the stream, begins at some suffix of the stream. That suffix is a prefix of the word, so it is no longer than the longest one. It is also a suffix of the longest one, because both end at the same character. Therefore every alive partial match is a border of the match state string, and the failure links list those borders from longest to shortest. Nothing before the match state needs to be kept.

#### The Fallback Transition

When the next character `c` does not extend the current state, the machine follows a **fallback transition**. It moves to the failure target and tries `c` again at that shorter state, repeating until `c` extends a state or the root is reached. No text index moves, so no character is read twice. Each character raises the matched length by at most 1, and each fallback lowers it by at least 1, so all fallbacks together cost at most as much as all the growth. The work over a stream of n characters is O(n) in total.

A full match is not a stopping point. At state `m` there is no next pattern character, so the machine treats the state as a mismatch and falls back to `fail[m - 1]`. The longest border of a found word is exactly the longest overlap with the next occurrence. In a trie the same rule is carried by the failure link, and a count stored at each node adds the words that end along its failure chain.

#### One Array Answers Three Questions

The array `fail` of one string `s` of length `n` also answers questions about `s` alone. The value `fail[n - 1]` is the length of the longest proper prefix that is also a suffix. The smallest **period** of `s` is the smallest `p` such that `s[i] == s[i + p]` wherever both indexes exist, and it equals `n - fail[n - 1]`. When this `p` divides `n` and is less than `n`, the string is `n / p` copies of its first `p` characters. When it does not divide `n`, the whole string is the only repeating unit.

<!-- stage: variables -->
### State Kept By The Machine

One pattern and a set of words use the same pieces with different shapes.

- **fail** for one pattern is an int array where `fail[i]` is the longest proper border length of `p[0..i]`.
- **k** is the match state for one pattern, the number of pattern characters that end the stream read so far, from 0 to `m`.
- **go** for many words is a table with one row per trie node and one column per letter, holding the next node for every letter.
- **fail** for many words is indexed by node, and holds the node of the longest proper suffix that is also a node. Node `k` of a one-word trie has the target `fail[k - 1]` of the array above.
- **hits** holds, for each node, how many stored words end at that node or along its failure chain.
- **state** is the current trie node and starts at the root, node 0. It is the only value kept between calls.

Words and stream use only lowercase `a` to `z`, so the letter `c` selects column `c - 'a'`.

<!-- stage: trace -->
### Following The State Through Two Inputs

#### One Pattern With A Match State

The pattern is `aabaa`, so `fail` is `0, 1, 0, 1, 2`. The text is `aabaaabaa`. In the trace below, the pointer `i` is the text index and the pointer `k` is the match state.

The first five characters extend the state from 0 to 5, which is a full match that starts at index 0. The machine does not stop. It falls back from state 5 to `fail[4] = 2`, because the last two characters `aa` already begin the next occurrence. At index 5 the character is `a`, but the pattern expects `b` after two matched characters. One fallback moves the state to `fail[1] = 1`, where `a` matches and the state becomes 2. Indexes 6, 7 and 8 raise the state to 5 again, so the second match starts at index 4. The text index moved forward on every step, and the result is the array `0, 4`.

```trace
{"cells":["a","a","b","a","a","a","b","a","a"],"pointers":["i","k"],"steps":[{"at":{"i":-1,"k":0},"vars":{"starts":"[]"},"note":"Start: the match state is 0 and nothing is read yet."},{"at":{"i":0,"k":1},"vars":{"starts":"[]"},"note":"i = 0: 'a' equals p[0], so the state rises to 1."},{"at":{"i":1,"k":2},"vars":{"starts":"[]"},"note":"i = 1: 'a' equals p[1], so the state rises to 2."},{"at":{"i":2,"k":3},"vars":{"starts":"[]"},"note":"i = 2: 'b' equals p[2], so the state rises to 3."},{"at":{"i":3,"k":4},"vars":{"starts":"[]"},"note":"i = 3: 'a' equals p[3], so the state rises to 4."},{"at":{"i":4,"k":5},"vars":{"starts":"[0]"},"note":"i = 4: 'a' equals p[4], so the state rises to 5. The state equals the pattern length, so a match starts at 0."},{"at":{"i":4,"k":2},"vars":{"starts":"[0]"},"note":"i = 4: the match state has no next pattern character, so it falls back to fail[4] = 2 and keeps scanning."},{"at":{"i":5,"k":1},"vars":{"starts":"[0]"},"note":"i = 5: p[2] is 'b' and rejects 'a'. The fallback moves the state from 2 to fail[1] = 1 and the same text index is tried again."},{"at":{"i":5,"k":2},"vars":{"starts":"[0]"},"note":"i = 5: 'a' equals p[1], so the state rises to 2."},{"at":{"i":6,"k":3},"vars":{"starts":"[0]"},"note":"i = 6: 'b' equals p[2], so the state rises to 3."},{"at":{"i":7,"k":4},"vars":{"starts":"[0]"},"note":"i = 7: 'a' equals p[3], so the state rises to 4."},{"at":{"i":8,"k":5},"vars":{"starts":"[0,4]"},"note":"i = 8: 'a' equals p[4], so the state rises to 5. The state equals the pattern length, so a match starts at 4."},{"at":{"i":8,"k":2},"vars":{"starts":"[0,4]"},"note":"i = 8: the match state has no next pattern character, so it falls back to fail[4] = 2 and keeps scanning."}]}
```

#### Three Words With Failure Links

The words are `ab`, `bab` and `b`. Their trie has nodes 1 and 2 for `ab`, nodes 3, 4 and 5 for `bab`, and the word `b` ends at node 3. The failure targets are `fail[2] = 3`, `fail[4] = 1` and `fail[5] = 2`, and the others point to the root. The stored counts are `hits[2] = 2`, `hits[3] = 1` and `hits[5] = 3`, because node 5 inherits `ab` through node 2 and `b` through node 3. The stream is `ababbab`, and the pointer `v` is the current node.

The first `b` reaches node 2 and reports two words, `ab` and `b`. The next `a` has no child under node 2, so the transition goes through the failure target, node 3, and lands on node 4. The second `b` reaches node 5 and reports three words in one lookup. The following `b` finds no child under node 5. The transitions follow the failure chain to node 3 and report only `b`. The counts for the whole stream are `0, 2, 0, 3, 1, 0, 3`, and no query looked at an earlier character.

```trace
{"cells":["a","b","a","b","b","a","b"],"pointers":["v"],"steps":[{"at":{"v":0},"vars":{"count":0},"note":"Start: the state is the root, node 0."},{"at":{"v":1},"vars":{"letter":"a","count":0},"note":"Letter 'a': the node has a child for this letter, so the state moves from node 0 to node 1. Exactly 0 stored word(s) end here."},{"at":{"v":2},"vars":{"letter":"b","count":2},"note":"Letter 'b': the node has a child for this letter, so the state moves from node 1 to node 2. Exactly 2 stored word(s) end here."},{"at":{"v":4},"vars":{"letter":"a","count":0},"note":"Letter 'a': the transition follows the failure chain, so the state moves from node 2 to node 4. Exactly 0 stored word(s) end here."},{"at":{"v":5},"vars":{"letter":"b","count":3},"note":"Letter 'b': the node has a child for this letter, so the state moves from node 4 to node 5. Exactly 3 stored word(s) end here."},{"at":{"v":3},"vars":{"letter":"b","count":1},"note":"Letter 'b': the transition follows the failure chain, so the state moves from node 5 to node 3. Exactly 1 stored word(s) end here."},{"at":{"v":4},"vars":{"letter":"a","count":0},"note":"Letter 'a': the node has a child for this letter, so the state moves from node 3 to node 4. Exactly 0 stored word(s) end here."},{"at":{"v":5},"vars":{"letter":"b","count":3},"note":"Letter 'b': the node has a child for this letter, so the state moves from node 4 to node 5. Exactly 3 stored word(s) end here."}]}
```

<!-- stage: code -->
### Matching One Pattern And Many Words

#### One Pattern As A Machine

The method `advance` is the single transition. It is used while building `fail` and while scanning, and it never reads a character twice. The names `fail` and `state` here match the variables stage.

```java
final class StreamMatching {
    // Longest proper border length for every prefix of pat; pat must not be null.
    static int[] failArray(String pat) {
        int[] fail = new int[pat.length()];
        int state = 0;
        for (int i = 1; i < pat.length(); i++) {
            state = advance(fail, pat, state, pat.charAt(i));
            fail[i] = state;
        }
        return fail;
    }

    // One transition: from a match state, read c and return the next match state.
    static int advance(int[] fail, String pat, int state, char c) {
        if (state == pat.length()) state = fail[state - 1];          // a full match falls back instead of stopping
        while (state > 0 && pat.charAt(state) != c) state = fail[state - 1];
        return pat.charAt(state) == c ? state + 1 : state;
    }

    // Every start index of pat in text, overlaps included, in increasing order. pat is non-empty.
    static int[] allStarts(String text, String pat) {
        int[] fail = failArray(pat);
        int[] starts = new int[text.length()];
        int found = 0, state = 0;
        for (int i = 0; i < text.length(); i++) {
            state = advance(fail, pat, state, text.charAt(i));
            if (state == pat.length()) starts[found++] = i - pat.length() + 1;
        }
        return java.util.Arrays.copyOf(starts, found);
    }

    // Smallest length u so that s is s[0..u-1] repeated; returns s.length() when no shorter unit exists.
    static int smallestUnit(String s) {
        int n = s.length();
        int p = n - failArray(s)[n - 1];
        return n % p == 0 ? p : n;
    }
}
```

The call `failArray(pat)` relies on `advance` reading `fail[state - 1]` only for indexes already filled. In `failArray` the state is always less than `i`, so the entry it reads has been written.

#### Many Words With A Persistent State

The class below builds the trie once, fills `go`, `fail` and `hits` in one level-order pass, and keeps one `state` between calls. The array `made` marks which `go` entries are real trie edges, because the fill later writes fallback results into the same table and a plain `0` cannot tell the two apart.

```java
final class WordStream {
    private static final int ALPHABET = 26;
    private final int[][] go;
    private final int[] hits;
    private int state = 0;

    WordStream(String[] words) {
        int cap = 1;
        for (String w : words) cap += w.length();                  // each character adds at most one node
        go = new int[cap][ALPHABET];
        hits = new int[cap];
        int[] fail = new int[cap];
        boolean[] made = new boolean[cap * ALPHABET];              // marks real trie edges, node * 26 + letter
        int nodes = 1;
        for (String w : words) {
            int v = 0;
            for (int j = 0; j < w.length(); j++) {
                int c = w.charAt(j) - 'a';
                if (!made[v * ALPHABET + c]) { made[v * ALPHABET + c] = true; go[v][c] = nodes++; }
                v = go[v][c];
            }
            hits[v]++;                                             // one more word ends at this node
        }
        int[] queue = new int[nodes];
        int head = 0, tail = 0;
        for (int c = 0; c < ALPHABET; c++) if (made[c]) queue[tail++] = go[0][c];
        while (head < tail) {
            int v = queue[head++];
            hits[v] += hits[fail[v]];                              // the failure target is shallower, so its count is final
            for (int c = 0; c < ALPHABET; c++) {
                int u = go[v][c];
                if (made[v * ALPHABET + c]) { fail[u] = go[fail[v]][c]; queue[tail++] = u; }
                else go[v][c] = go[fail[v]][c];                    // missing edge becomes the fallback result
            }
        }
    }

    // Consumes one letter and returns how many words end at it.
    int query(char letter) {
        state = go[state][letter - 'a'];
        return hits[state];
    }
}
```

#### Cost And Java Details

- **failArray** costs O(m) time and O(m) space, because the state rises at most once per character.
- **allStarts** costs O(n + m) time and O(m + z) space for z matches, because the text index never moves back.
- **WordStream** builds in O(L * 26) time and space for total word length L, and each `query` costs O(1) time with no growth in memory.

The expression `letter - 'a'` has type `int`, so it indexes the table directly, and a letter outside `a` to `z` would throw an `ArrayIndexOutOfBoundsException` instead of reading a wrong column. The code never calls `substring`, because every comparison uses an index.

<!-- stage: applicability -->
### When The Machine Applies

#### Recognizing The Pattern

Look for input that arrives as a sequence and a question asked after each element about the end of what has arrived: does any stored word end here, how many, or where did a pattern start. A second cue is a question about a single string's own structure, such as the longest border or the shortest repeating unit. Both cue types are answered by the same state. The invariant is that the match state always names the longest suffix of the characters read that is a prefix of some stored word, so the whole stream collapses into one number or node.

#### The Nearest False Friend

The false friend is to restart matching from scratch on a mismatch. It looks natural, and it passes inputs such as `abc` in `abxabc`, yet it fails on `aab` in `aaab`, because the characters already matched may begin the next attempt. A second false friend is to run KMP on each word separately. It is correct for one pattern, and for k words it costs k steps for every character, so a pattern list of 2,000 words keeps the cost of the naive scan. The trie with failure links merges all words into one state.

#### When Not To Use It

Do not use the table version when the word list changes while the stream runs, because adding one word can change failure targets across the trie and forces a rebuild. Do not use it when the alphabet is large, such as full Unicode, because a table of L * |alphabet| ints is too big and a map per node is needed. A single search of a stored text with one pattern is better served by `String.indexOf`, which needs no preparation. Patterns with wildcards or character classes break the border argument and need a different method.

<!-- stage: exercises -->
### Exercises

#### [Build] Every Start Of A Pattern (LeetCode 28)
<!-- id: as-all-starts-automaton -->

**Prerequisites.** The Prefix Function and First Occurrence With KMP exercises of the lesson Match A Pattern Without Restarting. This exercise changes the contract of LeetCode 28: it returns all start indices, not the first one.

**Problem.** Given strings `text` and `pattern`, return an `int[]` of every index `s` such that `text` has `pattern` as a substring starting at `s`. The occurrences may overlap. The indices are in increasing order, and the array is empty when there is no occurrence. Run the pattern as an automaton with states `0` to `m`, where state `m` is the match state and it falls back to `fail[m - 1]` instead of stopping the scan.

**Constraints.** The limits are:
- **Text length** is `0 <= text.length() <= 10^5`.
- **Pattern length** is `1 <= pattern.length() <= 10^5`.
- **Characters** are lowercase English letters.
- **Return** value is a new `int[]`, which may have length 0.
- **Mutation** does not occur; both strings are immutable.

**Example 1.** Input `text = "abababa"`, `pattern = "aba"`, output `[0, 2, 4]`.

**Example 2.** Input `text = "aaaaaa"`, `pattern = "aaa"`, output `[0, 1, 2, 3]`. Every position after the third continues the previous match.

**Hint.** After the machine reaches state `m`, which earlier state describes the longest end of the text that still begins the pattern?

**Changed decision.** The scan no longer returns at the first full match, and the match state falls back to `fail[m - 1]` so overlapping occurrences are found.

#### [Vary] Smallest Repeating Unit (LeetCode 459)
<!-- id: as-smallest-repeating-unit -->

**Prerequisites.** The first exercise above. This exercise changes the contract of LeetCode 459: it returns a length, not a boolean.

**Problem.** Given a non-empty string `s` of length `n`, return the smallest positive integer `u` such that `u` divides `n` and `s` equals the first `u` characters repeated `n / u` times. Return `n` when no smaller `u` has this property. Compute the answer from `n - fail[n - 1]`, where `fail[n - 1]` is the length of the longest proper prefix of `s` that is also a suffix.

**Constraints.** The limits are:
- **Length** is `1 <= s.length() <= 10^5`.
- **Characters** are lowercase English letters.
- **Return** value is an `int` from 1 to `n`.
- **Ties** do not occur because the smallest valid `u` is unique.
- **Mutation** does not occur; the string is immutable.

**Example 1.** Input `s = "abcabcabc"`, output `3`.

**Example 2.** Input `s = "ababa"`, output `5`. The border length is 3 and the gap 2 does not divide 5, so no proper unit exists.

**Hint.** If the gap `n - fail[n - 1]` does not divide `n`, can any other length work?

**Changed decision.** The output changes from a yes-or-no answer to the exact unit length. The test `n % p == 0` still decides between `p` and `n`, where `p = n - fail[n - 1]`.

#### [Boundary] Borders And Repeats Of Every Prefix (LeetCode 1392)
<!-- id: as-prefix-border-lengths -->

**Prerequisites.** The second exercise above. This exercise changes the contract of LeetCode 1392: it reports every prefix, and it adds a repeat flag for each one.

**Problem.** Given a non-empty string `s` of length `n`, return an `int[][]` with two rows of length `n`. In row 0, entry `i` is the length of the longest proper prefix of `s[0..i]` that is also a suffix of `s[0..i]`, or 0 when none exists. In row 1, entry `i` is 1 when `s[0..i]` consists of two or more equal copies of a shorter string, and 0 otherwise.

**Constraints.** The limits are:
- **Length** is `1 <= s.length() <= 10^5`.
- **Characters** are lowercase English letters.
- **Return** value is a new `int[2][n]`, and row 1 holds only 0 and 1.
- **Length one** gives `[[0], [0]]`, because a single character has no shorter string to repeat.
- **Mutation** does not occur; the string is immutable.

**Example 1.** Input `s = "ababab"`, output `[[0, 0, 1, 2, 3, 4], [0, 0, 0, 1, 0, 1]]`. The prefixes `abab` and `ababab` are repeats.

**Example 2.** Input `s = "abcab"`, output `[[0, 0, 0, 1, 2], [0, 0, 0, 0, 0]]`. The last prefix has a border of length 2, yet its gap 3 does not divide 5, so it is not a repeat.

**Hint.** For a prefix of length `len` with border `b > 0`, which length is the only candidate for the repeating unit, and what test confirms it?

**Changed decision.** The border row is the same as before. The repeat row applies the divisibility test to every prefix, so a border that exists is no longer enough to report a repeat.

#### [Recognize] Count Words Ending Here (LeetCode 1032)
<!-- id: as-count-words-ending-here -->

**Prerequisites.** The multi-pattern scan and suffix matches of the lesson Match Many Patterns In One Pass. This exercise changes the contract of LeetCode 1032: each call returns a count and not a boolean.

**Problem.** Design a class `WordCounter`. Its constructor takes an array `words` of distinct non-empty strings. Its method `query(char letter)` appends `letter` to an internal stream that starts empty and is never cleared. It returns the number of words in `words` that are a suffix of the whole stream so far. The state must persist between calls, and the class must not store the stream.

**Constraints.** The limits are:
- **Words** satisfy `1 <= words.length <= 2000`, all distinct.
- **Word length** is at least 1, and the total length is at most 10^4.
- **Calls** to `query` number at most 4 * 10^4.
- **Letters** are lowercase `a` to `z` in words and queries.
- **Answer** of each call is an `int` from 0 to `words.length`.

**Example 1.** Input words `["cd","abc","bc","c"]` and queries `a,b,c,d`, output `0,0,3,1`.

**Example 2.** Input words `["a","aa","aaa"]` and queries `a,a,a,a`, output `1,2,3,3`. Every shorter word is a suffix of a longer one.

**Hint.** If the count at a node already includes the count at its failure target, how many nodes does one query have to look at?

**Changed decision.** The answer is a number of words and not a flag, so the count of the failure target is added to each node at build time and a query reads one value.
