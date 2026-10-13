<!-- section: orientation -->
## Orientation

A moderation service watches a chat feed for 5,000 banned phrases. The first version tests every phrase at every position of every message, and the feed falls behind within minutes. A second version checks each position with a built-in substring search and still rereads the same characters again and again after each near miss. Advanced string algorithms remove that rereading by remembering what the text already proved.

### Prerequisites

You should know arrays and strings, the two-pointer and sliding-window habits, hash maps, tries from the trie chapter, and sorting with a comparator. A **prefix** of a string is its first characters, and a **suffix** is its last characters. A **border** is a piece that is both a proper prefix and a suffix of the same string.

### What Each Lesson Reuses

Each lesson answers one question about reusing work on text. The prefix-matching lesson also ends with an extension exercise on the Z array.

- **Rolling Hash** gives every window of a fixed length a number that updates in constant time, and it compares characters whenever two numbers agree.
- **Match A Pattern Without Restarting** stores the longest border of every pattern prefix, so a mismatch falls back instead of rewinding the text.
- **Find Palindromes Around Every Center** pads the string, copies radii from a mirror position and expands only past the known edge.
- **Sort And Compare All Suffixes** orders every suffix by doubling the compared length, then reads shared prefixes between neighbors.
- **Match Many Patterns In One Pass** builds one trie of the patterns and adds failure links so a single scan finds all of them.
- **Stream Matching With Failure Links** keeps one automaton state between arriving characters, so a late character is answered without rescanning old ones.

### Reading Order

Every lesson begins with a text task that fails at scale. A direct method follows, and you predict where its cost comes from before the reasoning appears. The remaining parts name the reused fact, list the variables, follow two traces, give Java code and state where the idea stops fitting. The exercises climb from a basic build to a variation, an edge case and a recognition problem. A LeetCode problem that appears twice carries a changed contract, and its text says what changed.

### What You Can Do After This Chapter

You can pick the tool whose stored fact fits a text task: a hash for equal windows, a border table for one pattern, radii for palindromes, a suffix order for many substring questions, and an automaton for many patterns or a stream. You can state what each one stores and when a hash match still needs a character check. Compositions of strings with dynamic programming or tries are left to the chapters that own those invariants.
