<!-- section: review -->
## Review

Return to this page after the lessons and again after a few days. Each question describes a situation and hides the name of the lesson. Pick an answer before you open the explanation.

### Recognition Questions

```quiz
{"id": "sw-rev-running-sum", "q": "A window of fixed size `k` moves one index to the right. Which update keeps the running sum correct?", "options": ["Add the entering value and subtract the leaving value", "Add all `k` values again", "Subtract the entering value and add the leaving value", "Add the entering value and keep the leaving value"], "answer": 0, "explain": "Exactly one value enters and one leaves, so two operations update the sum. The leaving value is the one at index `right - k`, and it has to be subtracted or the sum describes more than `k` values."}
```

```quiz
{"id": "sw-rev-count-test", "q": "A scan must decide whether a window holds the same letters as `aab` in any order. Which test is correct?", "options": ["Every letter of `aab` occurs at least once in the window", "The window and the pattern contain the same set of letters", "The count of each letter in the window equals its count in the pattern", "The window read from left to right equals `aab`"], "answer": 2, "explain": "The pattern needs two copies of `a`, and a test of membership ignores that. Only equal counts, which count each letter, represent multiplicity. Reading the window in order fails, because `aba` and `baa` hold the same letters as `aab` and still differ from it."}
```

```quiz
{"id": "sw-rev-shrink-while", "q": "A new value breaks a window that holds no repeated character. Why does the shrink step use `while` and not `if`?", "options": ["Because `while` is faster", "Because `if` does not compile in a loop", "Because one removal may leave the repeated value inside", "Because the window must grow by one each step"], "answer": 2, "explain": "The repeated value can sit deep in the window, so the loop may have to remove several values before the window is valid again. A single removal can leave a duplicate and make the recorded length too large."}
```

```quiz
{"id": "sw-rev-cover-order", "q": "In a shortest-cover scan, when does the method record the length of the window?", "options": ["After a removal has broken the cover", "Only at the end of the loop", "Each time the right end moves", "Before the removal of the leftmost value, while the window still covers"], "answer": 3, "explain": "The window is a cover only while the missing count is 0. The method records the length at that moment and then removes the leftmost value. Recording after the removal could measure a window that no longer covers."}
```

```quiz
{"id": "sw-rev-zero-key", "q": "A count map keeps a key with count 0 after its last copy leaves. What goes wrong when the problem limits the distinct count?", "options": ["The counts become negative", "The window grows without limit", "Nothing, because the count is still correct", "`map.size()` overstates the number of distinct values"], "answer": 3, "explain": "The size of the map is used as the distinct count. A key with count 0 is not in the window, but it still adds to the size, so the window looks invalid and shrinks too far."}
```

```quiz
{"id": "sw-rev-exactly-k", "q": "Why does `atMost(k) - atMost(k - 1)` count the ranges with exactly `k` of something?", "options": ["Because the ranges with at most `k - 1` lie inside those with at most `k`, and the rest have exactly `k`", "Because the second count is always larger", "Because the window finds both counts in one pass", "Because `atMost(k)` already excludes smaller counts"], "answer": 0, "explain": "Each range has one count of the property. The set with count at most `k - 1` is a part of the set with count at most `k`, so the difference leaves the ranges with count exactly `k`."}
```

```quiz
{"id": "sw-rev-replacement-cost", "q": "A window of length 9 holds the letter `a` five times. What is its replacement cost?", "options": ["5", "9", "4", "14"], "answer": 2, "explain": "The cheapest plan keeps the most frequent letter and overwrites every other character. The cost is the length minus the dominant count, which is 9 - 5 = 4."}
```

```quiz
{"id": "sw-rev-valid-starts", "q": "After the shrink loop, `left = 4` and `right = 9`, and every value is positive. How many valid subarrays end at index 9?", "options": ["10", "6", "5", "1"], "answer": 1, "explain": "The starts 4 through 9 are all valid, because removing positive values from a valid window keeps it valid. That is `9 - 4 + 1 = 6` subarrays. The rule fails when negative values can raise the sum after a removal."}
```

```quiz
{"id": "sw-rev-while-if", "q": "Which statement about replacing `while` by `if` in a window loop is correct?", "options": ["It is always a safe optimization", "It is safe only for a problem with a separate proof, such as the replacement budget", "It is never safe", "It is safe whenever the window length is fixed"], "answer": 1, "explain": "The one removal form keeps a candidate length, and its window may be invalid. A proof must show that a longer answer needs a larger count than any seen. The duplicate-free problem has no such proof, and the form gives wrong answers there."}
```

```quiz
{"id": "sw-rev-status-counter", "q": "A status counter holds the number of letters whose window count breaks the rule. One letter enters. By how much can the counter change from that letter alone?", "options": ["By at most one", "By the window length", "By the alphabet size", "It cannot change"], "answer": 0, "explain": "Only the entering letter's count changes, so only its status can flip between fine and broken. The counter goes up or down by one, or stays the same."}
```
