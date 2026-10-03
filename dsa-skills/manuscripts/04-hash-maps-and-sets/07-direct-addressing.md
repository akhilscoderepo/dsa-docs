<!-- lesson-kind: standard -->
<!-- lesson-id: direct-addressing -->
## Direct Addressing

<!-- stage: context -->
### Mailboxes Numbered By Room

A small hotel has forty rooms, and the front desk has a wall of forty mailboxes, one labelled for each room number. When a letter arrives for room 23, the clerk reaches for the twenty-third box and drops it in. There is no directory to consult and no filing rule to compute. The number on the envelope is the position on the wall.

Contrast that with a city post office, where addresses are street names that no wall could hold boxes for, and clerks use a directory to find the right bag. The hotel wall is faster and simpler, but it works only because the set of possible addresses is small, known in advance and fully numbered. If a guest insisted on mail addressed to room 1,000,000,000, the wall would have nowhere to put it.

<!-- stage: naive -->
### Use A General Map Anyway

A programmer who has just learned about frequency maps might count the letters of a lowercase word with one.

```java
static Map<Character, Integer> countsWithMap(String word) {
    Map<Character, Integer> count = new HashMap<>();
    for (char c : word.toCharArray()) {
        count.merge(c, 1, Integer::sum);
    }
    return count;
}
```

For `banana` it produces a map with a 3, b 1 and n 2. It is correct, it works for any characters, and it needs no knowledge of the alphabet.

<!-- stage: bottleneck -->
### Generality Has A Price

Both the map and the table are O(n) for a word of length `n`, so the difference is the constant factor, and it is large. Each `merge` boxes the character into a `Character` and the count into an `Integer`, computes a hash code, finds a bucket, compares keys and may allocate a node. A node holds references to the key and the value, so each distinct letter costs tens of bytes instead of four. For a few thousand words this is invisible, and for hundreds of millions of characters it is the difference between a fast loop and a slow one.

The map pays for a flexibility that this problem has not asked for. The statement promises that every character is a lowercase English letter. With that promise there are exactly 26 possible keys, and a key can be turned into a position by plain arithmetic. No hashing, no collisions and no nodes are needed if the keys can simply be used as indices.

<!-- stage: insight -->
### When The Key Is Already An Address

A **direct-address table** is an array in which the key itself, after a fixed adjustment, is the index of its slot. A lowercase letter `c` lives in slot `c - 'a'`, and a score between 40 and 100 lives in slot `score - 40`. The adjustment is the **offset**, the smallest allowed key, which moves the first possible key to slot 0. The table needs one slot for every key in the range, so its length is the largest key minus the smallest plus one.

None of this is safe without a **domain contract**, a promise from the problem about which keys can occur. The contract is what makes the array correct, because a key outside the range would index outside the table or land in the wrong slot. State the contract as a sentence, such as "every character is a lowercase English letter", and either check it, as the code below does, or rely on the problem's guarantee. The invariant is the one from the frequency lessons: `count[key - offset]` equals the number of occurrences of `key` in the processed prefix, with untouched slots meaning zero.

<!-- names: direct-address table, offset, domain contract -->

The choice between table and map is about the size of the promised range compared with the number of keys that occur. A range of 26 or 101 slots is always affordable. A range of a million slots is affordable if memory allows, and it pays off when many keys occur. A range of four billion, such as all 32-bit integers, is not affordable. Even a narrow range is a poor fit if only two keys occur and they are far apart, such as 2 and 1,000,000,000. In those cases the map stores only the keys that appear, which is why hash tables exist.

Direct addressing is not a rival of hashing in the rest of this chapter. It is the special case in which the hash function is the identity and nothing can collide. A general hash map also starts with an array of buckets, and it uses a hash function to squeeze the key space into that array. Writing a small one at the end of the exercises shows how that squeeze works.

<!-- stage: variables -->
### A Table, An Offset And A Check

The table `count` has one slot per allowed key and is created before the loop, with Java filling it with zeros. The offset is a constant derived from the contract, such as `'a'` or the minimum score. For each input key the code first checks that it lies within the contract, then computes `key - offset` and updates that slot. When the range is chosen at run time from the data, as in the sparse case, the minimum and maximum are computed first and the span is compared with a memory budget before an array is allocated.

<!-- stage: trace -->
### Counting With An Offset

```trace
{"cells":["b","a","n","a","n","a"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"char":"b","slot":1,"count":1},"note":"Read 'b'. Its slot is 98 - 97 = 1, and the count there becomes 1. Nonzero slots: b 1."},{"at":{"i":1},"vars":{"char":"a","slot":0,"count":1},"note":"Read 'a'. Its slot is 97 - 97 = 0, and the count there becomes 1. Nonzero slots: a 1, b 1."},{"at":{"i":2},"vars":{"char":"n","slot":13,"count":1},"note":"Read 'n'. Its slot is 110 - 97 = 13, and the count there becomes 1. Nonzero slots: a 1, b 1, n 1."},{"at":{"i":3},"vars":{"char":"a","slot":0,"count":2},"note":"Read 'a'. Its slot is 97 - 97 = 0, and the count there becomes 2. Nonzero slots: a 2, b 1, n 1."},{"at":{"i":4},"vars":{"char":"n","slot":13,"count":2},"note":"Read 'n'. Its slot is 110 - 97 = 13, and the count there becomes 2. Nonzero slots: a 2, b 1, n 2."},{"at":{"i":5},"vars":{"char":"a","slot":0,"count":3},"note":"Read 'a'. Its slot is 97 - 97 = 0, and the count there becomes 3. Nonzero slots: a 3, b 1, n 2."}]}
```

Take the word `banana` and a table of 26 slots numbered from 0. The `b` has index 1, the `a` index 0 and the `n` index 13. The three `a` letters raise slot 0 to 3, the `b` raises slot 1 to 1, and the two `n` letters raise slot 13 to 2. Every step is one subtraction and one array update, and the table never grows.

```trace
{"cells":[5,6,7,5,6,5],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"id":5,"slot":0,"table":"[1, 0, 0]"},"note":"Read id 5. Slot 5 - 5 = 0 rises to 1. Table: [1, 0, 0]."},{"at":{"i":1},"vars":{"id":6,"slot":1,"table":"[1, 1, 0]"},"note":"Read id 6. Slot 6 - 5 = 1 rises to 1. Table: [1, 1, 0]."},{"at":{"i":2},"vars":{"id":7,"slot":2,"table":"[1, 1, 1]"},"note":"Read id 7. Slot 7 - 5 = 2 rises to 1. Table: [1, 1, 1]."},{"at":{"i":3},"vars":{"id":5,"slot":0,"table":"[2, 1, 1]"},"note":"Read id 5. Slot 5 - 5 = 0 rises to 2. Table: [2, 1, 1]."},{"at":{"i":4},"vars":{"id":6,"slot":1,"table":"[2, 2, 1]"},"note":"Read id 6. Slot 6 - 5 = 1 rises to 2. Table: [2, 2, 1]."},{"at":{"i":5},"vars":{"id":5,"slot":0,"table":"[3, 2, 1]"},"note":"Read id 5. Slot 5 - 5 = 0 rises to 3. Table: [3, 2, 1]."}]}
```

The second trace counts identifiers 5, 6 and 7 with an offset of 5, so a table of three slots is enough. The identifier 5 maps to slot 0, 6 to slot 1 and 7 to slot 2. After six identifiers the slots hold 3, 2 and 1. Without the offset, the table would need eight slots with five of them wasted, and with identifiers near a billion the waste would be fatal.

<!-- stage: code -->
### Tables, Anagrams And A Chosen Representation

```java
static int[] lowercaseCounts(String s) {
    int[] count = new int[26];
    for (char c : s.toCharArray()) {
        if (c < 'a' || c > 'z') throw new IllegalArgumentException("outside the contract: " + c);
        count[c - 'a']++;
    }
    return count;
}

static boolean isAnagram(String s, String t) {
    if (s.length() != t.length()) return false;
    int[] balance = new int[26];
    for (int i = 0; i < s.length(); i++) {
        balance[s.charAt(i) - 'a']++;
        balance[t.charAt(i) - 'a']--;
    }
    for (int b : balance) if (b != 0) return false;
    return true;
}

static int mostCommonId(int[] ids) {
    if (ids.length == 0) return 0;
    int lo = Integer.MAX_VALUE, hi = Integer.MIN_VALUE;
    for (int id : ids) { lo = Math.min(lo, id); hi = Math.max(hi, id); }
    long span = (long) hi - lo + 1;
    int best = 0;
    if (span <= 4L * ids.length + 64) {                 // compact enough: direct address with an offset
        int[] count = new int[(int) span];
        for (int id : ids) best = Math.max(best, ++count[id - lo]);
    } else {                                            // sparse: a hash map stores only what occurs
        Map<Integer, Integer> count = new HashMap<>();
        for (int id : ids) best = Math.max(best, count.merge(id, 1, Integer::sum));
    }
    return best;
}
```

The table methods are O(n) with a tiny constant and O(1) extra space for the 26-letter versions. `isAnagram` uses one table with an increment for the first string and a decrement for the second, so the strings are anagrams exactly when every slot ends at zero. `mostCommonId` computes the span in `long` to avoid overflow, and it picks the table only when the span is within a small multiple of the input size, which keeps memory proportional to the data in both branches.

<!-- stage: applicability -->
### When A Range Is Promised And Small

Use a direct-address table when the problem promises a compact integer range, or an alphabet that maps cleanly onto one, and the memory for one slot per possible key is affordable. The invariant is that slot `key - offset` equals the count of that key in the processed prefix. Read the constraints for the range before choosing, and write the contract in a comment.

The false friend is an array used on text that the contract does not cover. An `int[26]` works for lowercase English letters and for nothing else. A Java `char` has 65,536 possible values, so a table of that size is feasible, but a character outside the basic plane takes two `char` values, so counting `char` values counts code units and not what a reader sees as characters. Arbitrary integers, identifiers and strings should go to a hash map.

In Java, validate each key before indexing, because a negative or oversized index throws `ArrayIndexOutOfBoundsException`, and an index that is valid but wrong silently corrupts a count. Compute spans in `long`, since `hi - lo + 1` can overflow `int`. Prefer `int[]` to `Integer[]` or `List<Integer>` for tables, because primitives avoid boxing. When the range is large, compare it with the number of inputs before allocating.

<!-- stage: exercises -->
### Exercises

#### [Build] Lowercase Character Counts (Author exercise)
<!-- id: hm-lowercase-counts -->

**Prerequisites.** Chapter 03 letter table; the direct-address table in this lesson. This is a deliberate revisit that treats the table as a choice of representation and checks it against the map version.

**Problem.** Count the occurrences of each letter `a` to `z` in a string and return an array of 26 counts. Under the contract every character is a lowercase English letter, so any other character must be rejected with an `IllegalArgumentException` before it is used as an index.

**Constraints.** 0 <= s.length() <= 10^5. The result array has length 26 and slot 0 is the letter `a`. Rejection must happen before any slot is touched for that character.

**Example 1.** Input `s = "banana"`, output counts of 3 for `a`, 1 for `b` and 2 for `n`, with every other slot zero.

**Example 2.** Input `s = "ab1"`, output a rejection of the character `1`, since it lies outside the contract.

**Hint.** What would `'1' - 'a'` evaluate to, and what would happen to the table if it were used as an index?

**Changed decision.** First rung: the key becomes an array index under a stated contract, replacing hashing with subtraction.

#### [Vary] Valid Anagram (LeetCode 242)
<!-- id: hm-anagram-array -->

**Prerequisites.** The build exercise above; the map version in the frequency lesson.

**Problem.** Decide whether two lowercase strings are anagrams using a single table of 26 integers. Increment for each character of the first string and decrement for the matching position of the second, and answer true only when every slot returns to zero.

**Constraints.** 0 <= s.length(), t.length() <= 5 * 10^4 and both strings contain lowercase English letters only. Strings of different lengths are never anagrams.

**Example 1.** Input `s = "triangle"`, `t = "integral"`, output true.

**Example 2.** Input `s = "aabc"`, `t = "abcc"`, output false, since slot `a` ends at 1 and slot `c` at -1.

**Hint.** Why is one table enough when two ledgers were needed before? What must every slot hold at the end?

**Changed decision.** The alphabet contract replaces the map, and a signed balance replaces two separate counts.

#### [Boundary] Sparse IDs (Author exercise)
<!-- id: hm-sparse-ids -->

**Prerequisites.** The two exercises above.

**Problem.** Given identifiers that are non-negative integers, return the largest number of times any identifier occurs. The method must work for identifiers such as 2 and 1,000,000,000 without allocating memory proportional to the largest value. Use a direct table when the identifier span is compact and a hash map when it is sparse.

**Constraints.** 0 <= ids.length <= 10^5 and 0 <= ids[i] <= 10^9. Memory must stay proportional to the input size in both cases.

**Example 1.** Input `ids = [2, 1000000000, 2]`, output 2, using the map path.

**Example 2.** Input `ids = [5, 6, 7, 5, 6, 5]`, output 3, where a three-slot table with an offset of 5 is enough.

**Hint.** What does the span `max - min + 1` tell you about the table size? What happens to the answer if you switch representation?

**Changed decision.** The representation is chosen from the data, and the answer must not depend on which one was chosen.

#### [Recognize] Design HashMap (LeetCode 706)
<!-- id: hm-design-hashmap -->

**Prerequisites.** All three exercises above.

**Problem.** Implement a map from `int` keys to `int` values with `put(key, value)`, `get(key)` which returns -1 for a missing key, and `remove(key)`, without using any built-in hash table class. In this version keys may be any `int`, including negative ones, which removes the compact-range promise of the original statement.

**Constraints.** Keys and values lie in `int` range and at most 10^4 operations are performed. A table with one slot for every possible key is not allowed.

**Example 1.** Input operations `put(7, 70)`, `put(-3, 30)`, `get(7)`, `get(5)`, output 70 and -1.

**Example 2.** Input operations `put(7, 70)`, `put(7, 71)`, `remove(7)`, `get(7)`, output -1, since the second put replaces and the remove deletes.

**Hint.** If you cannot afford one slot per key, how can many keys share a small array? What must each slot store so that keys that share it stay apart?

**Changed decision.** The compact-domain guarantee is gone, so keys are squeezed into a small array by a hash function and collisions are handled in the slot.
