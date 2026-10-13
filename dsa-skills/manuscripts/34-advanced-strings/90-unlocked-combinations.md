<!-- section: unlocked-combinations -->
## Unlocked Combinations

An antivirus engine receives network bytes in small pieces and must flag a signature even when its first half arrived in one piece and its second half in the next. Matching a pattern with stored fallback state is one idea from this chapter. Holding that state between arrivals is another, and one lesson joins them. Other joins with strings wait for the chapters that own their rules.

### Pairing Taught In This Chapter

| Combination | Teach now | Representative problem |
| --- | --- | --- |
| Prefix Automata + Stream State | Yes | LeetCode 1032 Stream of Characters |

The lesson Stream Matching With Failure Links joins the prefix automaton from the pattern lessons with state kept between calls. The automaton supplies the failure links, and the stream owns one current state that survives from one query to the next. Each arriving character costs a short walk through links instead of a rescan of earlier text.

### Pairings That Wait

| Combination | Status | Owner of the rule |
| --- | --- | --- |
| Strings + DP compositions | Deferred | The owning DP chapter, chapters 26 to 29 |
| Strings + Trie compositions | Deferred | The trie chapter, chapter 18 |

Problems that mix strings with a table of subproblems depend on the state and order of that table, which the DP chapters teach. Problems that mix strings with prefix trees depend on trie ownership and deletion rules from the trie chapter. This chapter assigns no problems to either pairing.
