<!-- section: review -->
## Review

A chat filter misses a phrase split across two messages, a duplicate finder reports two different strings as equal, and a palindrome search takes minutes on a long line of identical letters. The questions below cover the five lessons and the closing lesson. Try them after the lessons and again after a few days, and commit to an answer before opening the explanation.

### Recognition Questions

```quiz
{"id": "rq34-rev-hash-equal", "q": "Two windows of a text have the same rolling hash value. What may you conclude?", "options": ["Both windows hold the same characters.", "The windows may differ, so compare their characters before accepting.", "The windows must differ.", "The hash base was too small, so rebuild it."], "answer": 1, "explain": "Different windows can share a hash value because many strings map to fewer numbers. Equal hashes are a signal to verify, and only a character comparison proves equality."}
```

```quiz
{"id": "rq34-rev-prefix-fallback", "q": "A pattern `ababaca` has `pi[4] = 3`. The matcher has matched `ababa` and the next text character is `b`, but the pattern expects `c`. What happens next?", "options": ["The matcher restarts at the pattern start and rereads the text.", "The matched length becomes 4 after falling back to 3 and matching `b`.", "The matcher stops and reports no match.", "The text pointer moves back by 5."], "answer": 1, "explain": "The longest border of `ababa` is `aba`, so the matched length falls to 3 with the text pointer unchanged. Pattern index 3 is `b`, which equals the text character, so the length grows to 4."}
```

```quiz
{"id": "rq34-rev-radius-meaning", "q": "In the padded string `#a#b#a#b#` (indexes 0 to 8) the radius at index 3 is 3. Which palindrome of `abab` does this describe?", "options": ["The string `bab`.", "The string `abab`.", "The string `b` alone.", "The string `aba`, starting at index 0."], "answer": 3, "explain": "The window from index 0 to 6 reads `#a#b#a#`, and the radius 3 equals the length of `aba`. It starts at original index (3 - 3) / 2 = 0."}
```

```quiz
{"id": "rq34-rev-suffix-order", "q": "What is the suffix array of `banana`, listing start indexes in lexicographic order of the suffixes?", "options": ["[0, 1, 2, 3, 4, 5]", "[5, 3, 1, 0, 4, 2]", "[5, 1, 3, 0, 2, 4]", "[0, 5, 3, 1, 4, 2]"], "answer": 1, "explain": "The sorted suffixes are `a`, `ana`, `anana`, `banana`, `na`, `nana`, which begin at 5, 3, 1, 0, 4 and 2."}
```

```quiz
{"id": "rq34-rev-failure-link", "q": "A trie holds the patterns `he`, `she`, `his` and `hers`. Where does the failure link of the node for `she` point?", "options": ["The root", "The node for `s`", "The node for `sh`", "The node for `he`"], "answer": 3, "explain": "The proper suffixes of `she` are `he` and `e`. The string `he` is a prefix of a pattern and `e` is not, so the longest one that is a trie node is `he`."}
```

```quiz
{"id": "rq34-rev-stream-invariant", "q": "In a stream matcher, what is true of the current state after each character is read?", "options": ["It stands for the longest stored prefix that is a suffix of the text read so far.", "It stands for the first character of the text.", "It counts how many characters have arrived.", "It stores the last pattern that matched."], "answer": 0, "explain": "Failure links let the matcher keep the longest stored prefix that is a suffix of the text read so far. This one fact decides both which patterns end here and where to continue after the next character."}
```
