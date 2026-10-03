<!-- lesson-kind: standard -->
<!-- lesson-id: frequency-maps -->
## Frequency Maps

<!-- stage: context -->
### Tallying Pastries By Name

A bakery sells forty kinds of pastry, and the owner wants to know at closing how many of each were sold. Customers buy in any order, and new specials appear without warning. She keeps a notebook with one page per pastry. When a croissant is sold she flips to the croissant page and adds a mark. When a pastry is sold for the first time she opens a fresh page for it with a single mark.

The notebook never lists pastries that were not sold, and it does not need a page for every pastry she could ever bake. A name leads straight to its page, the page holds a number, and the number is the answer to "how many of these". The same notebook answers a second question for free: whether two days of sales had the same mix, which is just comparing the two notebooks page by page.

<!-- stage: naive -->
### Recount The Log For Every Sale

Without the notebook, the owner could keep the sales log and, for every entry, count how many entries in the whole log have the same name.

```java
static int firstSoldOnceByRecount(String[] sales) {
    for (int i = 0; i < sales.length; i++) {
        int times = 0;
        for (int j = 0; j < sales.length; j++) {
            if (sales[j].equals(sales[i])) times++;
        }
        if (times == 1) return i;
    }
    return -1;
}
```

On `["bun", "tart", "bun", "scone"]` it returns 1, since `tart` is the first name that occurs exactly once. It works, and it reads almost like the question.

<!-- stage: bottleneck -->
### Every Entry Recounts The Whole Log

For each of the `n` entries the inner loop reads all `n` entries, so the time is O(n * n). With 100,000 sales that is ten billion string comparisons, and each comparison may read several characters. The answer for one pastry is recomputed every time that pastry appears, so the work is repeated as well as large.

Two facts point to the repair. First, the count for a name never depends on which entry asked for it, so it can be computed once. Second, the count has to be found from the name alone, without searching, which is what the notebook page gave the owner. A single pass can build all the counts, and a second pass can then ask each entry for its count in constant time.

<!-- stage: insight -->
### A Ledger Keyed By The Value Itself

A **frequency map** associates each distinct key with the number of times it has been seen. In Java it is a `HashMap<K, Integer>`, and the key leads to its count in expected constant time, the same way a ticket number led to a drawer. The map is a **ledger**, a record in which every entry is a key and the exact tally of that key over the part of the input already read. The invariant is that after reading a prefix, `count.get(key)` equals the number of occurrences of `key` in that prefix, for every key that has occurred.

<!-- names: frequency map, ledger, zero convention -->

Every ledger needs a **zero convention**, a rule for what an absent key means. The usual rule is that absent means zero. In Java, `get` on a missing key returns `null`, and unboxing that into an `int` throws, so the code uses `getOrDefault(key, 0)` or `merge(key, 1, Integer::sum)` to apply the rule safely. A second rule must be chosen whenever counts can fall: a key whose count returns to zero is either removed or kept, and mixing the two silently breaks the tests that ask whether a key is present.

Counting once and asking later is a pattern with two phases. The first pass builds the ledger. The second pass, or a comparison with a second ledger, makes the decision. First unique character uses the first pass to count and the second to walk the string in its original order. An anagram test builds two ledgers and compares them, because two strings are anagrams exactly when every key has the same count in both. A set cannot do either job, since it forgets multiplicity.

<!-- stage: variables -->
### Keys, Counts And The Absent Case

The map `count` has the characters, words or numbers as keys and `Integer` counts as values. Before the first read it is empty, which means every count is zero. Each read increases one count by one. When the problem also removes items, a decrement must either be allowed to go negative as a meaningful surplus, or it must delete the key at zero and ignore keys that were never added. Comparison of two ledgers uses `equals` on the maps, which compares keys and values and is not fooled by insertion order.

<!-- stage: trace -->
### Counting Then Asking

```trace
{"cells":["bun","tart","bun","scone","tart","bun"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"name":"bun","ledger":"bun 1"},"note":"Read bun. Its count becomes 1. Ledger: bun 1."},{"at":{"i":1},"vars":{"name":"tart","ledger":"bun 1, tart 1"},"note":"Read tart. Its count becomes 1. Ledger: bun 1, tart 1."},{"at":{"i":2},"vars":{"name":"bun","ledger":"bun 2, tart 1"},"note":"Read bun. Its count becomes 2. Ledger: bun 2, tart 1."},{"at":{"i":3},"vars":{"name":"scone","ledger":"bun 2, tart 1, scone 1"},"note":"Read scone. Its count becomes 1. Ledger: bun 2, tart 1, scone 1."},{"at":{"i":4},"vars":{"name":"tart","ledger":"bun 2, tart 2, scone 1"},"note":"Read tart. Its count becomes 2. Ledger: bun 2, tart 2, scone 1."},{"at":{"i":5},"vars":{"name":"bun","ledger":"bun 3, tart 2, scone 1"},"note":"Read bun. Its count becomes 3. Ledger: bun 3, tart 2, scone 1."}]}
```

Take the sales `["bun", "tart", "bun", "scone", "tart", "bun"]`. The first pass reads each name and raises its count, so after six reads the ledger holds bun 3, tart 2 and scone 1. The pass costs one map update per entry.

```trace
{"cells":["bun","tart","bun","scone","tart","bun"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"name":"bun","count":3,"answer":"none yet"},"note":"Ask the ledger about bun: count 3. Not unique, keep walking."},{"at":{"i":1},"vars":{"name":"tart","count":2,"answer":"none yet"},"note":"Ask the ledger about tart: count 2. Not unique, keep walking."},{"at":{"i":2},"vars":{"name":"bun","count":3,"answer":"none yet"},"note":"Ask the ledger about bun: count 3. Not unique, keep walking."},{"at":{"i":3},"vars":{"name":"scone","count":1,"answer":3},"note":"Ask the ledger about scone: count 1. This is the first name with count 1, so the answer is index 3."}]}
```

The second pass walks the sales in their original order and asks the ledger for each name's count. The first entry, `bun`, has count 3 and the next, `tart`, has count 2, so neither qualifies. The third entry, `scone`, has count 1, so the answer is index 3 and the walk stops. The order comes from the array, not from the map, which is why the map never needs to remember positions.

<!-- stage: code -->
### Counting, Asking And Comparing

```java
static Map<Character, Integer> counts(String s) {
    Map<Character, Integer> count = new HashMap<>();
    for (char c : s.toCharArray()) {
        count.merge(c, 1, Integer::sum);                 // absent means zero, so merge starts at 1
    }
    return count;
}

static int firstUnique(String s) {
    Map<Character, Integer> count = counts(s);
    for (int i = 0; i < s.length(); i++) {
        if (count.get(s.charAt(i)) == 1) return i;       // safe: every character of s is a key
    }
    return -1;
}

static boolean sameLetters(String a, String b) {
    return counts(a).equals(counts(b));
}

static void remove(Map<String, Integer> ledger, String key) {
    Integer now = ledger.get(key);
    if (now == null) return;                             // never added, nothing to remove
    if (now == 1) ledger.remove(key);                    // delete at zero, so absence still means zero
    else ledger.put(key, now - 1);
}
```

All counting is expected O(n) time and O(k) space for `k` distinct keys. `firstUnique` compares an unboxed `Integer` with 1, which is safe because every character it asks about is already a key. `sameLetters` uses `Map.equals`, which compares contents regardless of insertion order. The helper `remove` deletes a key when its count would fall to zero, so a later `containsKey` answers correctly.

<!-- stage: applicability -->
### When The Number Matters

Use a frequency map when the decision depends on how many times something occurred, or when two collections must have the same multiplicities. The invariant that should hold at every step is that the count of each key equals its occurrences in the processed prefix, with absent meaning zero. Decide the zero convention before writing the first line.

The false friend is a set. A set tells whether a value appeared and silently loses how often, so an anagram test or a most-frequent question built on a set gives wrong answers on inputs like `aab` against `abb`. The other false friend runs the opposite way: a frequency map is wasteful when the question only asks whether something appeared at least once.

Java has its own traps here. `map.get(key)` returns `null` for a missing key, and unboxing it throws a `NullPointerException`, so use `getOrDefault` or `merge`. Compare `Integer` values with `equals` or unbox them first, because `==` on boxed values above 127 compares object identity and can be false for equal numbers. Never compare a map's entries by position, since `HashMap` has no stable order. When both key and value are needed, loop over `entrySet()` instead of calling `get` for every key.

<!-- stage: exercises -->
### Exercises

#### [Build] First Unique Character in a String (LeetCode 387)
<!-- id: hm-first-unique-char -->

**Prerequisites.** Chapter 03 character scans; the ledger in this lesson.

**Problem.** Given a string `s`, return the index of the first character that occurs exactly once in the whole string, or -1 if every character repeats. Positions are those of the original string.

**Constraints.** 1 <= s.length() <= 10^5 and `s` holds lowercase letters. A single pass to count and a single pass to ask are enough.

**Example 1.** Input `s = "swiss"`, output 1, since `w` is the first character with count one.

**Example 2.** Input `s = "abab"`, output -1, because every character occurs twice.

**Hint.** Why can the first pass not answer the question by itself? What order must the second pass follow?

**Changed decision.** First rung: a count replaces the existence test, so the ledger records how many and the string supplies the order.

#### [Vary] Valid Anagram (LeetCode 242)
<!-- id: hm-valid-anagram -->

**Prerequisites.** The build exercise above.

**Problem.** Return true if the second string can be formed by rearranging all the characters of the first one, and false otherwise. Compare the two ledgers, not the strings themselves.

**Constraints.** 0 <= s.length(), t.length() <= 5 * 10^4. Characters may be any `char`, so a map is used and not a fixed table.

**Example 1.** Input `s = "stone"`, `t = "notes"`, output true.

**Example 2.** Input `s = "aab"`, `t = "abb"`, output false, though both strings use the same set of letters.

**Hint.** Does a set of letters distinguish these two examples? What equality between ledgers is enough?

**Changed decision.** The question becomes equality of two multiplicity records instead of a search through one.

#### [Boundary] Remove Zero Counts (Author exercise)
<!-- id: hm-remove-zero-counts -->

**Prerequisites.** The two exercises above.

**Problem.** An array of operations adds or removes items, each written as `"+x"` or `"-x"` for an item name `x`. Return the number of distinct items whose count is positive after all operations. A removal of an item that is not present is ignored, and a key must be deleted exactly when its count returns to zero.

**Constraints.** 0 <= ops.length <= 10^5. Item names are short non-empty strings. Absence must keep meaning a count of zero throughout.

**Example 1.** Input `ops = ["+a", "+b", "+a", "-a", "-b"]`, output 1, since `a` is left with one.

**Example 2.** Input `ops = ["-z", "+z", "-z"]`, output 0, because the first removal is ignored and the last one empties `z`.

**Hint.** If a key stays in the map with value zero, what will a presence test claim? Which operation must be ignored instead of creating a negative count?

**Changed decision.** Counts now fall as well as rise, so the zero convention has to be enforced by deleting keys, not just by reading defaults.

#### [Recognize] Unique Number of Occurrences (LeetCode 1207)
<!-- id: hm-unique-occurrences -->

**Prerequisites.** All three exercises above.

**Problem.** Given an integer array, return true if the number of occurrences of every distinct value is different from that of every other value. Count each value with a map first, then test the counts for repeats with a set.

**Constraints.** 1 <= arr.length <= 1000 and -1000 <= arr[i] <= 1000. Two containers are expected, one map and one set.

**Example 1.** Input `arr = [3, 3, 5, 5, 5, 1]`, output true, because the counts are 2, 3 and 1.

**Example 2.** Input `arr = [7, 7, 8, 8]`, output false, since both values occur twice.

**Hint.** What are the values of the first map, and which structure answers whether a list of numbers has a repeat?

**Changed decision.** The output of one counting pass becomes the input of a membership question, so the two lessons combine.
