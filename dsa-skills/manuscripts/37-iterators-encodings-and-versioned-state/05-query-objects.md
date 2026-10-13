<!-- lesson-kind: standard -->
<!-- lesson-id: query-objects -->
## Query Objects

<!-- stage: context -->
### Answering Thousands Of Questions About One Text

A documentation site loads one manual of 200 000 words when the server starts. A search feature then answers a stream of questions about it. How close do the words `error` and `timeout` come to each other? How many times does `retry` appear between word 5 000 and word 90 000? Does any other word on the site shorten to the same form `c3e` as the word `cache`? The manual never changes while the server runs, and a single day brings 50 000 such questions.

Each question is cheap to state and expensive to answer if the program rereads the manual every time. The data stays fixed and the questions keep coming. The program can therefore do some work once, at construction, and reuse the result for every later question.

This lesson asks one question. What should a constructor remember about stable data so that each later query avoids a full scan, and what can it safely forget?

<!-- stage: naive -->
### Scanning The Whole Input For Every Query

The direct method stores the words and answers each query by walking the whole array. For the shortest distance between two words, the walk remembers the latest index of each word and updates the best gap whenever it sees one of them.

```java
final class NaiveDistance {
    private final String[] words;

    NaiveDistance(String[] words) { this.words = words; }

    int shortest(String a, String b) {
        int lastA = -1, lastB = -1, best = Integer.MAX_VALUE;
        for (int i = 0; i < words.length; i++) {
            if (words[i].equals(a)) lastA = i;
            if (words[i].equals(b)) lastB = i;
            if (lastA >= 0 && lastB >= 0) best = Math.min(best, Math.abs(lastA - lastB));
        }
        return best == Integer.MAX_VALUE ? -1 : best;
    }
}
```

Each answer is correct. For a short text with two or three queries the class looks finished.

```predict
The text has 200 000 words and the service answers 50 000 queries. One of the two query words appears only 3 times in the text. How many words does the naive class examine, and how many of them can matter?

The naive class examines 200 000 times 50 000, which is 10 billion words. Only the 3 occurrences of the rare word and the occurrences of the other word can change the answer. Every other word is read and ignored.
```

<!-- stage: bottleneck -->
### Counting The Repeated Scans

The naive `shortest` costs O(n) time per query for a text of `n` words, so `q` queries cost O(n * q). The cost does not depend on how rare the query words are. The scan pays for the whole text even when a word occurs three times.

The repeated work has a clear cause. Every query rebuilds the same fact from scratch: where each word occurs. That fact belongs to the data, not to the query. The data does not change, so the program can compute it once and keep it. The next section shows what to keep and how a query reads it in time proportional to the matching occurrences, or less.

<!-- stage: insight -->
### Keep Positions And Search Inside Them

#### Store A Position List Per Word

A **position list** is the sorted array of indices at which one word occurs. The constructor makes one pass over the text and appends each index to the list of its word. The lists together hold exactly `n` numbers, so the memory is O(n), and a query touches only the lists of its own words. A word that occurs three times costs three entries.

<!-- names: position list, merge walk, lower bound -->

#### Compare Two Lists With A Merge Walk

The shortest distance between two words is the smallest difference between an index of the first list and an index of the second. A **merge walk** keeps one cursor in each sorted list and compares the two indices under the cursors. It records their gap, then advances the cursor that points to the smaller index. The smaller index cannot form a closer pair with any later index of the other list, because those later indices are larger, so moving it loses nothing. Each step advances one cursor. The walk ends when a list is exhausted. The cost is O(a + b) for lists of lengths `a` and `b`.

#### Count In A Range With A Lower Bound

A **lower bound** of a value `x` in a sorted array is the first index whose element is at least `x`. To count the occurrences of a value between two text positions, the constructor stores the position list of each value. A query takes the lower bound of `left` and the lower bound of `right + 1` in that list. The difference of the two indices is the number of positions in `[left, right]`. Each lower bound is one binary search, so a query costs O(log k) for `k` occurrences, and it never reads the text.

#### The Invariant Of The Constructor

The invariant says that preprocessing keeps exactly the information that the queries need and drops the rest. For distance queries that information is the positions of each word. For range counts it is the positions of each value. For a dot product of two sparse vectors it is the pairs of an index and a nonzero value. The test of a good constructor is that every query answer follows from the stored lists and that no query needs the original input again.

<!-- stage: variables -->
### What The Constructor Keeps

The constructor builds one map. Each query reads a few entries from it.

- **positions** maps a key, such as a word or a number, to its sorted array of indices.
- **pa** and **pb** are the position lists of the two query words in a distance query.
- **i** and **j** are the cursors into `pa` and `pb` during a merge walk.
- **gap** is the difference between `pa[i]` and `pb[j]` at one comparison.
- **best** is the smallest gap seen so far, or -1 when no pair exists.
- **lo, hi and mid** bound one binary search, and **target** is the value that the search looks for.
- **left** and **right** are the inclusive text positions of a range query, and the search looks for `left` and `right + 1`.

The invariant is that every list is strictly increasing, so a cursor never needs to move backward.

<!-- stage: trace -->
### Tracing Two Searches On Positions

#### A Merge Walk On Two Position Lists

The first trace answers a distance query on the text `a c b c a c b b c a`. The word `a` occurs at positions 0, 4 and 9. The word `b` occurs at positions 2, 6 and 7. The position list of `a` is `pa` and that of `b` is `pb`. The pointers `pa[i]` and `pb[j]` mark the text positions under the two cursors `i` and `j` before the step moves one of them. The variable `best` shows the smallest gap so far.

The first comparison sets 0 against 2 with gap 2. The smaller position is 0, so the cursor of `a` moves to 4. Position 4 against 2 gives gap 2, and now the smaller position belongs to `b`, so that cursor moves to 6. Position 4 against 6 gives gap 2 again, and the cursor of `a` moves to 9. Position 9 against 6 gives gap 3, which does not improve the best value, so the cursor of `b` moves to 7. Position 9 against 7 gives gap 2. The cursor of `b` then moves past its last entry and the walk ends with the answer 2.

```trace
{"cells":["a","c","b","c","a","c","b","b","c","a"],"pointers":["pa[i]","pb[j]"],"steps":[{"at":{"pa[i]":0,"pb[j]":2},"vars":{"i":0,"j":0,"gap":2,"best":2},"note":"Compare 0 with 2. The gap is 2, so best is 2. pa[i] is the smaller position, so i moves forward."},{"at":{"pa[i]":4,"pb[j]":2},"vars":{"i":1,"j":0,"gap":2,"best":2},"note":"Compare 4 with 2. The gap is 2, so best is 2. pb[j] is the smaller position, so j moves forward."},{"at":{"pa[i]":4,"pb[j]":6},"vars":{"i":1,"j":1,"gap":2,"best":2},"note":"Compare 4 with 6. The gap is 2, so best is 2. pa[i] is the smaller position, so i moves forward."},{"at":{"pa[i]":9,"pb[j]":6},"vars":{"i":2,"j":1,"gap":3,"best":2},"note":"Compare 9 with 6. The gap is 3, so best is 2. pb[j] is the smaller position, so j moves forward."},{"at":{"pa[i]":9,"pb[j]":7},"vars":{"i":2,"j":2,"gap":2,"best":2},"note":"Compare 9 with 7. The gap is 2, so best is 2. pb[j] is the smaller position, so j moves forward."},{"at":{},"vars":{"i":2,"j":3,"best":2},"note":"A list is exhausted, so the walk ends and returns best, which is 2."}]}
```

#### Two Lower Bounds For A Range Count

The second trace counts how often the value 3 occurs in positions 2 to 6 of the array 1 3 2 3 3 1 3 2 3. The position list of the value 3 is 1, 3, 4, 6 and 8. The pointers `lo`, `hi` and `mid` bound each binary search, as in the earlier lesson.

The first search looks for the lower bound of 2. The middle entry 4 is at least 2, so the window shrinks to the left. The next middle entry 3 is also at least 2. The entry at index 0 is position 1, which is below 2, so the window closes at index 1. The second search looks for the lower bound of 7. The middle entry 4 is below 7, so the window moves right. Entry 8 is at least 7, and entry 6 is below 7, so the window closes at index 4. The count is 4 minus 1, which is 3. The positions 3, 4 and 6 lie in the range.

```trace
{"cells":["1","3","4","6","8"],"pointers":["lo","hi","mid"],"steps":[{"at":{"lo":0,"hi":5,"mid":-1},"vars":{"target":2},"note":"Search one: find the first position at least 2."},{"at":{"lo":0,"hi":5,"mid":2},"vars":{"target":2,"entry":4},"note":"Entry 4 is at least 2, so hi becomes 2."},{"at":{"lo":0,"hi":2,"mid":1},"vars":{"target":2,"entry":3},"note":"Entry 3 is at least 2, so hi becomes 1."},{"at":{"lo":0,"hi":1,"mid":0},"vars":{"target":2,"entry":1},"note":"Entry 1 is below 2, so lo becomes 1."},{"at":{"lo":1,"hi":1,"mid":1},"vars":{"target":2,"index":1},"note":"The window closes at index 1."},{"at":{"lo":0,"hi":5,"mid":-1},"vars":{"target":7},"note":"Search two: find the first position at least 7."},{"at":{"lo":0,"hi":5,"mid":2},"vars":{"target":7,"entry":4},"note":"Entry 4 is below 7, so lo becomes 3."},{"at":{"lo":3,"hi":5,"mid":4},"vars":{"target":7,"entry":8},"note":"Entry 8 is at least 7, so hi becomes 4."},{"at":{"lo":3,"hi":4,"mid":3},"vars":{"target":7,"entry":6},"note":"Entry 6 is below 7, so lo becomes 4."},{"at":{"lo":4,"hi":4,"mid":4},"vars":{"target":7,"index":4},"note":"The window closes at index 4."},{"at":{},"vars":{"count":3},"note":"The count is 4 minus 1, which is 3."}]}
```

<!-- stage: code -->
### Writing The Index And The Search

#### Position Lists And The Merge Walk

The class below builds the lists in two passes. The first pass counts the occurrences of each word and the second pass fills arrays of exactly the right size. A query then runs the merge walk on two arrays.

```java
final class WordIndex {
    private final java.util.Map<String, int[]> positions = new java.util.HashMap<>();

    WordIndex(String[] words) {
        var counts = new java.util.HashMap<String, Integer>();
        for (String w : words) counts.merge(w, 1, Integer::sum);   // pass 1: occurrences per word
        var fill = new java.util.HashMap<String, Integer>();
        for (int i = 0; i < words.length; i++) {                    // pass 2: indices in increasing order
            int[] list = positions.computeIfAbsent(words[i], w -> new int[counts.get(w)]);
            list[fill.merge(words[i], 1, Integer::sum) - 1] = i;
        }
    }

    int shortest(String a, String b) {
        int[] pa = positions.get(a), pb = positions.get(b);
        if (pa == null || pb == null) return -1;                    // an absent word has no pair
        int i = 0, j = 0, best = Integer.MAX_VALUE;
        while (i < pa.length && j < pb.length) {
            best = Math.min(best, Math.abs(pa[i] - pb[j]));
            if (pa[i] < pb[j]) i++; else j++;                       // advance the smaller position
        }
        return best;
    }
}
```

#### The Lower Bound For Counting

The helper below returns the first index in a sorted array whose element is at least the target. The difference of two calls is a count of positions in a range.

```java
static int lowerBound(int[] sorted, int target) {
    int lo = 0, hi = sorted.length;          // the answer lies in [lo, hi]
    while (lo < hi) {
        int mid = (lo + hi) >>> 1;
        if (sorted[mid] < target) lo = mid + 1; else hi = mid;
    }
    return lo;                               // sorted.length when every element is smaller
}
```

#### Cost

- **Constructor** costs O(n) expected time and O(n) space for a text of `n` words.
- **shortest** costs O(a + b) time and O(1) space for lists of lengths `a` and `b`.
- **lowerBound** costs O(log k) time and O(1) space for a list of `k` entries.

<!-- stage: applicability -->
### When The Data Stays Fixed

#### Recognizing The Pattern

Use this method when a constructor receives stable data and many queries follow. The tell is a class whose constructor takes the whole input and whose methods only read. Write down what each query asks of the data, then decide which small structure answers it without the original input. Positions answer distance and range questions. A list of nonzero entries answers dot products. A map from a shortened form to a set of words answers questions about collisions.

#### A False Friend

Caching the answer of each query is a false friend of preprocessing. A cache helps when the same pair repeats, and it gives no help on a new pair. The preprocessed lists answer every pair from the first call. The invariant that every list is sorted also separates a merge walk from a nested loop. The nested loop checks all pairs and costs O(a * b).

#### Edge Cases To Check Every Time

An absent key must return the documented value and must not throw a null pointer error. A query whose two arguments are the same key needs its own rule, because the merge walk would pair every position with itself and report distance 0. A range that reaches outside the array needs a decision in the contract: clamp it, or reject it. A range with `left > right` is empty and counts zero. When products or sums can exceed the `int` range, accumulate in `long`.

<!-- stage: exercises -->
### Exercises

#### [Build] Shortest Word Distance II (LeetCode 244)
<!-- id: it37-query-objects-word-distance -->

**Prerequisites.** The position list and merge walk definitions from this lesson.

**Problem.** Design the class `WordIndex` built from an array of words. The call `shortest(a, b)` returns the smallest value of `|i - j|` over indices `i` and `j` with `i != j`, `words[i] = a` and `words[j] = b`. It returns -1 when no such pair exists, including the case that `a` or `b` is absent and the case `a = b` with fewer than two occurrences.

**Constraints.** The limits are:
- **Length** is `0 <= words.length <= 30000`.
- **Words** are lowercase strings of 1 to 10 letters.
- **Queries** number at most 50000, and the arguments are lowercase strings of 1 to 10 letters.
- **Mutation** does not occur after construction.

**Example 1.** Input `words = ["go","to","the","store","go","to","bed","go"]` and queries `shortest("go","to")`, `shortest("store","bed")`, `shortest("go","go")`, `shortest("bed","bed")`, `shortest("go","zoo")`, output `[1,3,3,-1,-1]`.

**Example 2.** Input `words = ["x","y"]` and queries `shortest("y","x")`, `shortest("x","x")`, output `[1,-1]`.

**Hint.** What does the merge walk do when both arguments name the same list, and which neighbors in that one list can give the smallest gap?

**Changed decision.** The contract now allows equal arguments and absent words, so the answer for equal words comes from adjacent entries of one list and not from a merge of two lists.

#### [Vary] Dot Product of Two Sparse Vectors (LeetCode 1570)
<!-- id: it37-query-objects-sparse-dot -->

**Prerequisites.** The Shortest Word Distance II exercise above.

**Problem.** Design the class `SparseVec` built from an integer array `nums`. The call `dot(other)` returns the sum of `nums[i] * other.nums[i]` over all indices `i` that exist in both arrays, as a `long`. The two vectors can have different lengths. Indices beyond the shorter vector contribute nothing.

**Constraints.** The limits are:
- **Length** is `0 <= nums.length <= 100000` for each vector.
- **Values** are `int` numbers with `-10^6 <= nums[i] <= 10^6`.
- **Zeros** are common, but the input promises no bound on their count.
- **Result** fits in a `long`, and neither vector changes after construction.

**Example 1.** Input `a = [1,0,0,2,3]` and `b = [0,3,0,4,0]`, output 8.

**Example 2.** Input `a = [2,0,-5]` and `b = [4,7]`, output 8.

**Hint.** Which entries of each vector can make a product nonzero, and which type must hold the product of two values near one million?

**Changed decision.** The stored list keeps only the nonzero pairs of an index and a value, and the product is computed in `long` instead of `int`.

#### [Boundary] Unique Word Abbreviation (LeetCode 288)
<!-- id: it37-query-objects-abbreviation -->

**Prerequisites.** The previous two exercises above.

**Problem.** Define the abbreviation of a word as the word itself when it has at most 2 letters, and otherwise its first letter, the count of letters between the first and last letter written in decimal, and its last letter. Design the class `AbbrDictionary` built from an array of words that can contain repeats. The call `conflicts(word)` returns the number of distinct dictionary words that have the same abbreviation as `word` and differ from `word`.

**Constraints.** The limits are:
- **Dictionary** has `0 <= length <= 30000` words, with repeats allowed.
- **Words** are lowercase strings of 1 to 20 letters, and queries use the same alphabet.
- **Queries** number at most 50000, and the dictionary does not change.
- **Distinct** means two words are equal only when all letters match.

**Example 1.** Input `dictionary = ["deer","door","cake","card"]` and queries `conflicts("dear")`, `conflicts("deer")`, `conflicts("cart")`, `conflicts("cake")`, output `[2,1,0,0]`.

**Example 2.** Input `dictionary = ["abc","adc","abc"]` and queries `conflicts("abc")`, `conflicts("ac")`, `conflicts("axc")`, output `[1,0,2]`.

**Hint.** Which word in the group does not count as a conflict, and how can the stored group tell that the query word is in it?

**Changed decision.** The stored group holds distinct words per abbreviation, so a repeated dictionary word counts once and the query word subtracts itself.

#### [Recognize] Range Frequency Queries (LeetCode 2080)
<!-- id: it37-query-objects-range-frequency -->

**Prerequisites.** All exercises above.

**Problem.** Design the class `RangeFreq` built from an integer array `arr`. The call `query(left, right, value)` returns how many indices `i` satisfy `left <= i <= right`, `0 <= i < arr.length` and `arr[i] = value`. The bounds `left` and `right` are any integers, so a range can reach outside the array or be empty.

**Constraints.** The limits are:
- **Length** is `1 <= arr.length <= 100000`.
- **Values** are `int` numbers with `-10^9 <= arr[i] <= 10^9`.
- **Queries** number at most 100000, with `left`, `right` and `value` as `int` numbers.
- **Empty range** means `left > right` after the range is cut to the array, and the answer is 0.

**Example 1.** Input `arr = [12,33,4,56,22,2,34,33,22,12,34,56]` and queries `query(1,2,4)`, `query(0,11,33)`, `query(-5,3,12)`, `query(8,100,22)`, `query(5,2,33)`, output `[1,2,1,1,0]`.

**Example 2.** Input `arr = [7,7,7]` and queries `query(0,2,7)`, `query(1,1,7)`, `query(3,5,7)`, output `[3,1,0]`.

**Hint.** Which two lower bounds in the position list of `value` give the count, and what does the constructor store for a value that never occurs?

**Changed decision.** The query never reads `arr`. It cuts the range to the array, then subtracts two lower bounds in one position list, and an absent value gives 0.
