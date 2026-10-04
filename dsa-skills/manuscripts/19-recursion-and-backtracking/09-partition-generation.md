<!-- lesson-kind: standard -->
<!-- lesson-id: partition-generation -->
## Partition Generation

<!-- stage: context -->
### The Ribbon Counter At Silverlake

The haberdashery at Silverlake sells ribbon from long reels, and each reel is printed along its length with a repeating row of letters so that the shop can tell one reel from another. Customers who order for a wedding ask for a whole length of reel to be cut into bows. Every centimetre is used, because the offcuts are not sold, and every bow must be one unbroken stretch of ribbon from the reel, cut in the order it lies.

The assistant wants to show a customer all the ways a given length could be cut into bows, with the counter's own rule deciding which bows are acceptable. A cut that leaves a scrap at the end is not allowed, and neither is a bow built from two stretches that were not next to each other on the reel.

<!-- stage: naive -->
### Try Every Pattern Of Cut Marks

A reel of n letters has n - 1 gaps between neighbouring letters, and each gap is either cut or left alone, which makes 2^(n-1) patterns. The direct method counts through the patterns, turns each into the bows it describes, and keeps the pattern only if every bow passes the rule.

```java
static List<List<String>> cutsByPattern(String reel, Predicate<String> ok) {
    int n = reel.length();
    List<List<String>> cuts = new ArrayList<>();
    for (int mask = 0; mask < (1 << (n - 1)); mask++) {
        List<String> bows = new ArrayList<>();
        int from = 0;
        for (int gap = 0; gap < n; gap++) {
            boolean cutHere = gap == n - 1 || (mask >> gap & 1) == 1;
            if (cutHere) { bows.add(reel.substring(from, gap + 1)); from = gap + 1; }
        }
        if (bows.stream().allMatch(ok)) cuts.add(bows);
    }
    return cuts;
}
```

The method covers each way to cut the reel exactly once and it judges every bow, so it is a dependable oracle for reels of at least one letter.

<!-- stage: bottleneck -->
### One Bad Bow Spoils Thousands

Each pattern is built in O(n) and judged afterwards, so the work is O(n * 2^n) and does not depend on how strict the rule is. The waste is plain when the rule is strict. If the first bow of a pattern is unacceptable, every one of the patterns that begins with that bow is spoiled, and there may be 2^(n-4) of them, but the loop makes and judges each one in turn. The shared start is built again for every pattern that has it.

The loop sees a pattern only as a finished number. A search that cut the reel from the left, one bow at a time, would meet a bad bow at the moment it was cut and could drop every continuation at once. It would also never need a pattern for the far end of the reel until the near end had passed inspection, so the work would follow the acceptable beginnings and not all 2^(n-1) patterns.

<!-- stage: insight -->
### Cut The Next Bow From The Front

Keep a number that says how much of the reel has been cut into accepted bows. Call it the **uncut start**: it is the first position that has not yet been assigned to a bow, and everything before it is covered exactly once by the bows on the path. The call chooses where the next bow ends, using the **ending choice**, a loop over every position from just after the start up to the end of the reel. The bow is the stretch from the start to that ending.

If the bow passes the rule, it joins the path and the call recurses from the ending, which becomes the new start. Because the next bow always begins exactly where the last one ended, the bows are contiguous and in reel order, and no stretch can be used twice or skipped. A rejected bow is dropped at once and so is every continuation that would have followed it.

The search finishes a partition when the start has reached the end of the reel. At that moment the **empty suffix** is all that remains, nothing is left to cut, and the path is a complete partition, so the call records a copy of it. A call may not record when the path merely looks long or when the loop ran out of endings, because a path that stops early has left a scrap uncut.

This makes the structure different from a subset search. A subset call may leave elements out, and a partition call must account for every position, so the recursion's shrinking measure is the length of the uncut part, which falls by the bow length each time and cannot go below zero.

The invariant is that the bows on the path tile the reel from position zero to the start without gaps or overlaps, and the call records only when the start equals the length.

<!-- names: uncut start, ending choice, empty suffix -->

<!-- stage: variables -->
### Start, End And Bows

The `start` is the uncut start, and a call records its path exactly when `start == s.length()`. The loop variable `end` is the ending choice, with the bow being `s.substring(start, end)`; it runs from `start + 1` to `s.length()` so the bow is never empty and never reaches past the string. The `rule` is a supplied test that a bow must pass and does not change during the run. The `path` holds the accepted bows in reel order and changes by one bow per move.

<!-- stage: trace -->
### Every Way To Cut Three Letters

The first trace cuts the reel `abc` with a rule that accepts every bow. The pointer `start` is the uncut start, and `end` is the position where the bow under consideration stops, so the bow is the letters from `start` up to but not including `end`. A partition is recorded when `start` has reached 3.

```trace
{"cells":["a","b","c"],"pointers":["start","end"],"steps":[{"at":{"start":0,"end":1},"vars":{"path":"['a']","recorded":0},"note":"The bow a runs from 0 to 1 and is accepted, so the path is ['a'] and the next call starts at 1."},{"at":{"start":1,"end":2},"vars":{"path":"['a', 'b']","recorded":0},"note":"The bow b runs from 1 to 2 and is accepted, so the path is ['a', 'b'] and the next call starts at 2."},{"at":{"start":2,"end":3},"vars":{"path":"['a', 'b', 'c']","recorded":0},"note":"The bow c runs from 2 to 3 and is accepted, so the path is ['a', 'b', 'c'] and the next call starts at 3."},{"at":{"start":3,"end":-1},"vars":{"path":"['a', 'b', 'c']","recorded":1},"note":"The start has reached 3, so nothing is left uncut and a copy of ['a', 'b', 'c'] is recorded as partition 1."},{"at":{"start":2,"end":3},"vars":{"path":"['a', 'b']","recorded":1},"note":"The bow c is taken off again, so the path is ['a', 'b']."},{"at":{"start":1,"end":2},"vars":{"path":"['a']","recorded":1},"note":"The bow b is taken off again, so the path is ['a']."},{"at":{"start":1,"end":3},"vars":{"path":"['a', 'bc']","recorded":1},"note":"The bow bc runs from 1 to 3 and is accepted, so the path is ['a', 'bc'] and the next call starts at 3."},{"at":{"start":3,"end":-1},"vars":{"path":"['a', 'bc']","recorded":2},"note":"The start has reached 3, so nothing is left uncut and a copy of ['a', 'bc'] is recorded as partition 2."},{"at":{"start":1,"end":3},"vars":{"path":"['a']","recorded":2},"note":"The bow bc is taken off again, so the path is ['a']."},{"at":{"start":0,"end":1},"vars":{"path":"empty","recorded":2},"note":"The bow a is taken off again, so the path is empty."},{"at":{"start":0,"end":2},"vars":{"path":"['ab']","recorded":2},"note":"The bow ab runs from 0 to 2 and is accepted, so the path is ['ab'] and the next call starts at 2."},{"at":{"start":2,"end":3},"vars":{"path":"['ab', 'c']","recorded":2},"note":"The bow c runs from 2 to 3 and is accepted, so the path is ['ab', 'c'] and the next call starts at 3."},{"at":{"start":3,"end":-1},"vars":{"path":"['ab', 'c']","recorded":3},"note":"The start has reached 3, so nothing is left uncut and a copy of ['ab', 'c'] is recorded as partition 3."},{"at":{"start":2,"end":3},"vars":{"path":"['ab']","recorded":3},"note":"The bow c is taken off again, so the path is ['ab']."},{"at":{"start":0,"end":2},"vars":{"path":"empty","recorded":3},"note":"The bow ab is taken off again, so the path is empty."},{"at":{"start":0,"end":3},"vars":{"path":"['abc']","recorded":3},"note":"The bow abc runs from 0 to 3 and is accepted, so the path is ['abc'] and the next call starts at 3."},{"at":{"start":3,"end":-1},"vars":{"path":"['abc']","recorded":4},"note":"The start has reached 3, so nothing is left uncut and a copy of ['abc'] is recorded as partition 4."},{"at":{"start":0,"end":3},"vars":{"path":"empty","recorded":4},"note":"The bow abc is taken off again, so the path is empty."}]}
```

The second trace uses the reel `abcde` with a rule that accepts only bows of two or three letters. Watch the path `ab`, `cd`: it leaves one letter and no acceptable bow can be cut from it, so the call returns without recording anything, because the start never reaches 5 on that route.

```trace
{"cells":["a","b","c","d","e"],"pointers":["start","end"],"steps":[{"at":{"start":0,"end":2},"vars":{"path":"['ab']","recorded":0},"note":"The bow ab runs from 0 to 2 and is accepted, so the path is ['ab'] and the next call starts at 2."},{"at":{"start":2,"end":4},"vars":{"path":"['ab', 'cd']","recorded":0},"note":"The bow cd runs from 2 to 4 and is accepted, so the path is ['ab', 'cd'] and the next call starts at 4."},{"at":{"start":4,"end":-1},"vars":{"path":"['ab', 'cd']","recorded":0},"note":"The start is 4 with 1 letters left and no acceptable bow can be cut from them, so the call returns without recording anything."},{"at":{"start":2,"end":4},"vars":{"path":"['ab']","recorded":0},"note":"The bow cd is taken off again, so the path is ['ab']."},{"at":{"start":2,"end":5},"vars":{"path":"['ab', 'cde']","recorded":0},"note":"The bow cde runs from 2 to 5 and is accepted, so the path is ['ab', 'cde'] and the next call starts at 5."},{"at":{"start":5,"end":-1},"vars":{"path":"['ab', 'cde']","recorded":1},"note":"The start has reached 5, so nothing is left uncut and a copy of ['ab', 'cde'] is recorded as partition 1."},{"at":{"start":2,"end":5},"vars":{"path":"['ab']","recorded":1},"note":"The bow cde is taken off again, so the path is ['ab']."},{"at":{"start":0,"end":2},"vars":{"path":"empty","recorded":1},"note":"The bow ab is taken off again, so the path is empty."},{"at":{"start":0,"end":3},"vars":{"path":"['abc']","recorded":1},"note":"The bow abc runs from 0 to 3 and is accepted, so the path is ['abc'] and the next call starts at 3."},{"at":{"start":3,"end":5},"vars":{"path":"['abc', 'de']","recorded":1},"note":"The bow de runs from 3 to 5 and is accepted, so the path is ['abc', 'de'] and the next call starts at 5."},{"at":{"start":5,"end":-1},"vars":{"path":"['abc', 'de']","recorded":2},"note":"The start has reached 5, so nothing is left uncut and a copy of ['abc', 'de'] is recorded as partition 2."},{"at":{"start":3,"end":5},"vars":{"path":"['abc']","recorded":2},"note":"The bow de is taken off again, so the path is ['abc']."},{"at":{"start":0,"end":3},"vars":{"path":"empty","recorded":2},"note":"The bow abc is taken off again, so the path is empty."}]}
```

<!-- stage: code -->
### Recording At The End Of The Reel

```java
static List<List<String>> partitions(String s, Predicate<String> rule) {
    List<List<String>> out = new ArrayList<>();
    cut(s, 0, rule, new ArrayList<>(), out);
    return out;
}

private static void cut(String s, int start, Predicate<String> rule,
                        List<String> path, List<List<String>> out) {
    if (start == s.length()) {                      // nothing is left uncut
        out.add(new ArrayList<>(path));
        return;
    }
    for (int end = start + 1; end <= s.length(); end++) {
        String bow = s.substring(start, end);
        if (!rule.test(bow)) continue;              // a rejected bow ends this route
        path.add(bow);
        cut(s, end, rule, path, out);
        path.remove(path.size() - 1);
    }
}
```

The loop bound `end <= s.length()` matters, because `substring` throws a `StringIndexOutOfBoundsException` when its end is beyond the string. For an empty string the first call is already at the end and records one empty partition. The number of partitions can reach 2^(n-1), and each costs a copy, so the time is O(n * 2^n) in the worst case, with a stack no deeper than n.

<!-- stage: applicability -->
### Cutting A Whole Sequence

Use partition generation when the output divides an entire sequence into consecutive pieces and each piece has its own validity test: words in a dictionary, numbers without leading zeros, palindromic parts, and equal-sized chunks. The invariant to maintain is that the pieces on the path cover the prefix up to the start exactly, so a record is legal only when that prefix is the whole sequence.

The nearest false friend is the subset search. It also walks forward with an index, which makes the two look alike, yet a subset call may skip positions, and a skipped letter in a partition means a scrap of reel has been dropped. Using subset-style recursion here produces selections of letters instead of covers of the reel. A second false friend is a loop that records when it runs out of endings, which lets a path that stopped early count as complete.

Do not generate all partitions when only their number or the fewest pieces is wanted, because the number of partitions can be exponential while a table over start positions gives the answer in polynomial time. That table needs the memoization contract of a later chapter. In Java, keep the loop bound at the string length, copy the path when it is stored, and expect that a rule which is cheap to apply early removes most of the tree.

<!-- stage: exercises -->
### Exercises

#### [Build] All Splits Of A Short String (Author exercise)
<!-- id: bt-short-splits -->

**Prerequisites.** The working path with its undo step, and the increasing-start loop as a contrast.

**Problem.** Given a short string, return every way to cut it into consecutive nonempty pieces that together form the whole string. Pieces are tried from the shortest ending to the longest, and partitions are listed in the order found.

**Constraints.** 1 <= s.length() <= 8, and s has lowercase letters only.

**Example 1.** Input `s = "abc"`, output `[["a", "b", "c"], ["a", "bc"], ["ab", "c"], ["abc"]]`.

**Example 2.** Input `s = "a"`, output `[["a"]]`.

**Hint.** What number of partitions does a string of n letters have, and at what start is a partition complete?

**Changed decision.** The loop picks where a piece ends and not whether a letter is taken, so every position is covered exactly once.

#### [Vary] Valid-Piece Predicate (Author exercise)
<!-- id: bt-valid-pieces -->

**Prerequisites.** The All Splits Of A Short String rung.

**Problem.** Given a string of digits and a cap, cut it into consecutive pieces so that every piece is a number with no leading zero, where the single digit zero is allowed, and every piece has a value at most the cap. Return the partitions in the order found, with shorter pieces tried first.

**Constraints.** 1 <= s.length() <= 8, s has digits only, and 0 <= cap <= 1000.

**Example 1.** Input `s = "1234"`, `cap = 34`, output `[["1", "2", "3", "4"], ["1", "2", "34"], ["1", "23", "4"], ["12", "3", "4"], ["12", "34"]]`.

**Example 2.** Input `s = "1001"`, `cap = 100`, output `[["1", "0", "0", "1"], ["10", "0", "1"], ["100", "1"]]`.

**Hint.** When a piece fails the test, should the search try longer pieces from the same start, and why can a leading zero never be repaired by extending the piece?

**Changed decision.** A rule is applied to each piece before recursion, so a failing piece removes its whole continuation but not the longer pieces from the same start.

#### [Boundary] Empty Suffix Completion (Author exercise)
<!-- id: bt-empty-suffix -->

**Prerequisites.** The Valid-Piece Predicate rung.

**Problem.** Given a string, cut it into consecutive pieces whose lengths are each 2 or 3, using all of the string, and return the partitions in the order found with shorter pieces tried first. The empty string has exactly one partition, the empty one, and a string that cannot be covered has none.

**Constraints.** 0 <= s.length() <= 12, and s has lowercase letters only.

**Example 1.** Input `s = "abcde"`, output `[["ab", "cde"], ["abc", "de"]]`.

**Example 2.** Input `s = "a"`, output `[]`.

**Hint.** What is true of the start when a path is complete, and what happens if a piece of three letters is requested with two letters left?

**Changed decision.** A path is recorded only at an empty suffix, so partial covers that run out of acceptable pieces are silently dropped.

#### [Recognize] Palindrome Partitioning (LeetCode 131)
<!-- id: bt-palindrome-partition -->

**Prerequisites.** The Empty Suffix Completion rung.

**Problem.** Given a string, return every way to cut it into consecutive pieces that each read the same forwards and backwards, using all of the string. List partitions in the order found when shorter pieces are tried first.

**Constraints.** 1 <= s.length() <= 12, and s has lowercase letters only.

**Example 1.** Input `s = "aab"`, output `[["a", "a", "b"], ["aa", "b"]]`.

**Example 2.** Input `s = "abba"`, output `[["a", "b", "b", "a"], ["a", "bb", "a"], ["abba"]]`.

**Hint.** Which supplied rule from the earlier rungs does the palindrome test replace, and does the rest of the search change at all?

**Changed decision.** The rule becomes a palindrome test on the piece, while the structure of the search stays exactly that of the predicate rung.
