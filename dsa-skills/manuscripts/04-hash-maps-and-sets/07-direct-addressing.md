<!-- lesson-kind: standard -->
<!-- lesson-id: direct-addressing -->
## Choose An Array Or A Map

<!-- stage: context -->
### Two Counters That Need Different Storage

A text tool counts how often each lowercase letter occurs in a text of ten million characters. A profiler shows that the counting step spends most of its time on hashing and on creating `Integer` objects. A colleague replaces the map with an array and the tool becomes several times faster. The colleague then copies the same array idea into a tool that counts requests per user number, where user numbers reach one billion. That tool stops with an out-of-memory error at its first run.

Both tools count values, and both counters are correct in design. The first question is what makes an array the right storage for the first counter and the wrong storage for the second. The second question is how a program decides that before it writes the code.

<!-- stage: naive -->
### Counting Letters With A Map

The first version counts letters with a map from character to count. This version is correct for any characters, so it needs no assumption about the text.

```java
static Map<Character, Integer> letterCounts(String text) {
    Map<Character, Integer> counts = new HashMap<>();
    for (int i = 0; i < text.length(); i++) {
        counts.merge(text.charAt(i), 1, Integer::sum);
    }
    return counts;
}
```

On `"banana"` the method returns `a` with 3, `b` with 1 and `n` with 2. The map holds an entry only for letters that occur.

<!-- stage: bottleneck -->
### Every Update Pays For Hashing And Boxing

```predict
The text holds 10 million lowercase letters. How does the asymptotic cost of the map version compare with a version that keeps 26 counters, and what does the map still do for every letter?

Both versions cost O(n), so the profiler difference is a constant factor and not a different growth rate. For every letter the map computes a hash code, finds the entry, unboxes the old count, and boxes the new count into an `Integer` object. A plain counter performs one array increment.
```

The map is correct, but it does extra work in every iteration. It wraps the character into a `Character`, computes a hash code, finds the entry, and replaces the stored `Integer` with a new one. All of that work serves keys that could have any value. The text holds only 26 different keys, and the program knows the set in advance. A structure that uses the key itself as a position can skip the hashing and the object creation. Whether that is safe depends on the number of possible keys, and the second tool in the opening shows what happens when that number is a billion.

<!-- stage: insight -->
### Use The Key As An Array Index

#### Turn The Key Into A Position

**Direct addressing** stores the data for a key at the array position that the key computes. For lowercase letters the position is `c - 'a'`. For values in a known interval from `min` to `max`, the position is `value - min`. The subtraction shifts the interval to start at 0.

<!-- names: direct addressing, key range, sparse keys -->

#### Compare The Cost Of The Two Structures

The **key range** is the number of possible keys, which is `max - min + 1`. An array needs one slot for each possible key, so its space is O(key range) even if most slots stay empty. A hash map needs one entry for each key that occurs, so its space is O(d) for d distinct keys. Time per update is O(1) for both. The array's cost is certain, and the map's cost is expected.

#### Decide By Comparing Range With Input Size

An array is the better choice when the key range is small, either fixed by the contract such as 26 letters, or proportional to the input size n. A map is the better choice when the keys are **sparse keys**, which means the key range is far larger than the number of keys that occur. Two keys 2 and 1000000000 give a key range of one billion and only 2 occurring keys, so an array would reserve a billion slots for 2 entries.

#### Write The Contract Before The Code

The array version holds only under a stated contract, such as "the text holds lowercase English letters only". With that contract the index `c - 'a'` always lies in `0..25`. Without it, a character outside the range produces an index outside the array. The map version needs no contract, which is its advantage. The program should state which contract it relies on.

<!-- stage: variables -->
### Range, Offset And Slot

Three values describe a direct-addressed table.

- **min** is the smallest possible key, and it becomes the offset that the program subtracts from every key.
- **range** equals `max - min + 1` and fixes the array length.
- **slot** equals `key - min` and names the array position that stores the data of the key.

<!-- stage: trace -->
### Two Domains With One Idea

#### Letters From A To Z

Take the text `"dbdad"`. The position of `d` is 3, so the first letter increments slot 3. The letter `b` increments slot 1, then `d` increments slot 3 again. The letter `a` increments slot 0 and the last `d` increments slot 3. The final slots hold `a` with 1, `b` with 1 and `d` with 3. The array never changes its length.

#### Request Codes From 100 To 105

Now take the values `[103, 101, 103, 105, 101, 103]`, which a contract limits to the interval 100 to 105. The offset is `min = 100`, and the range is 6. The value 103 maps to slot 3, the value 101 to slot 1 and the value 105 to slot 5. The final slots hold 101 with 2, 103 with 3 and 105 with 1.

#### Stepping Through Both Inputs

```trace
{"cells":["d","b","d","a","d"],"pointers":["i"],"steps":[{"at":{"i":-1},"vars":{"slots":"{}"},"note":"Start: every slot holds 0."},{"at":{"i":0},"vars":{"key":"d","slot":3,"slots":"{3: 1}"},"note":"Key d maps to slot 3, which now holds 1."},{"at":{"i":1},"vars":{"key":"b","slot":1,"slots":"{1: 1, 3: 1}"},"note":"Key b maps to slot 1, which now holds 1."},{"at":{"i":2},"vars":{"key":"d","slot":3,"slots":"{1: 1, 3: 2}"},"note":"Key d maps to slot 3, which now holds 2."},{"at":{"i":3},"vars":{"key":"a","slot":0,"slots":"{0: 1, 1: 1, 3: 2}"},"note":"Key a maps to slot 0, which now holds 1."},{"at":{"i":4},"vars":{"key":"d","slot":3,"slots":"{0: 1, 1: 1, 3: 3}"},"note":"Key d maps to slot 3, which now holds 3."}]}
```

```trace
{"cells":[103,101,103,105,101,103],"pointers":["i"],"steps":[{"at":{"i":-1},"vars":{"slots":"{}"},"note":"Start: every slot holds 0."},{"at":{"i":0},"vars":{"key":103,"slot":3,"slots":"{3: 1}"},"note":"Key 103 maps to slot 3, which now holds 1."},{"at":{"i":1},"vars":{"key":101,"slot":1,"slots":"{1: 1, 3: 1}"},"note":"Key 101 maps to slot 1, which now holds 1."},{"at":{"i":2},"vars":{"key":103,"slot":3,"slots":"{1: 1, 3: 2}"},"note":"Key 103 maps to slot 3, which now holds 2."},{"at":{"i":3},"vars":{"key":105,"slot":5,"slots":"{1: 1, 3: 2, 5: 1}"},"note":"Key 105 maps to slot 5, which now holds 1."},{"at":{"i":4},"vars":{"key":101,"slot":1,"slots":"{1: 2, 3: 2, 5: 1}"},"note":"Key 101 maps to slot 1, which now holds 2."},{"at":{"i":5},"vars":{"key":103,"slot":3,"slots":"{1: 2, 3: 3, 5: 1}"},"note":"Key 103 maps to slot 3, which now holds 3."}]}
```

<!-- stage: code -->
### A Table Indexed By The Key

#### Counting Values In A Known Interval

```java
static int[] countInRange(int[] values, int min, int max) {
    int[] table = new int[max - min + 1];
    for (int v : values) {
        table[v - min]++;
    }
    return table;
}
```

#### What The Method Costs

The loop makes one array increment for each value, so the time is O(n) with a very small constant. The table holds `max - min + 1` slots, so the space is O(key range), which does not depend on n. The method is correct only when every value lies in the interval from `min` to `max`. A value outside the interval throws `ArrayIndexOutOfBoundsException`, or writes into the wrong slot if `min` is wrong.

<!-- stage: applicability -->
### When The Key Range Is Small

#### Look For A Bounded Domain

Use an array when the statement bounds the keys and the bound is small. Examples are lowercase letters, decimal digits, ASCII codes below 128, scores from 0 to 100, and days of a year. The invariant is that `table[key - min]` holds the data of `key` for every key in the declared interval, and no key outside the interval ever arrives. Use a map when the keys are words, objects, coordinates, or integers with no useful bound.

#### Unicode Text Is A False Friend

A false friend here is a text in which characters are not limited. A table of 26 entries does not fit arbitrary Unicode text, because a Java `char` has 65536 possible values and a character outside the alphabet breaks the index. A table with 65536 entries works but costs memory for every counter, so a map or a validated alphabet is the usual choice. The same caution applies to integers. The type `int` has four billion values, so a bounded domain must come from the problem and not from the type.

#### Java Details That Cause Failures

The expression `max - min + 1` wraps around in `int` when the interval spans the whole range, so compute the range with `long` before it sizes an array. A request for a huge array throws `OutOfMemoryError` or `NegativeArraySizeException`, and the failure appears at run time. The array `new int[26]` starts with all counts at 0, but a table reused between inputs must be reset first.

<!-- stage: exercises -->
### Exercises

#### [Build] Words Containing Each Letter (Author exercise)
<!-- id: hm-words-per-letter -->

**Prerequisites.** The letter table and the offset `c - 'a'` from this lesson.

**Problem.** Let `words` be an array of strings of lowercase English letters. Return an `int[26]` where entry `k` is the number of words that contain the letter `'a' + k` at least once. A word counts once for a letter, however often the letter occurs in it.

**Constraints.** The limits are:
- **Length** satisfies `0 <= words.length <= 10^4`, and each word has at most 100 letters.
- **Characters** are the lowercase letters `'a'` to `'z'` only.
- **Words** may be empty.
- **Answer** has exactly 26 entries.

**Example 1.** Input `words = ["moon", "mom", "no"]`, output has 2 at index 12 for `m`, 2 at index 13 for `n`, 3 at index 14 for `o`, and 0 elsewhere.

**Example 2.** Input `words = [""]`, output is 26 zeros.

**Hint.** What must the program reset for each word, so that a repeated letter inside one word counts once?

**Changed decision.** Basic case: a table over a declared alphabet, with a per-word marker so that each letter counts once for each word.

#### [Vary] Anagram Over ASCII (Author exercise)
<!-- id: hm-anagram-ascii -->

**Prerequisites.** Words Containing Each Letter above and the anagram exercise from the frequency map lesson.

**Problem.** Let `s` and `t` be strings in which every character has a code below 128. Return true when `t` is a rearrangement of `s`.

**Constraints.** The limits are:
- **Length** satisfies `0 <= s.length(), t.length() <= 10^5`.
- **Characters** have codes in `0..127`, so a table of 128 slots covers the alphabet.
- **Answer** is a boolean.
- **Mutation** of the inputs is not allowed.

**Example 1.** Input `s = "Ab 1"`, `t = "1 bA"`, output true.

**Example 2.** Input `s = "aab"`, `t = "aBb"`, output false, because `b` and `B` are different characters.

**Hint.** Which statement of the problem lets the program use an array in place of the map from the earlier lesson?

**Changed decision.** The stated alphabet bound replaces the map with a table of 128 counters.

#### [Boundary] Sparse IDs (Author exercise)
<!-- id: hm-sparse-ids -->

**Prerequisites.** The two exercises above and the cost comparison from this lesson.

**Problem.** Let `ids` be a non-empty array of integers. Direct addressing is acceptable when the key range `max - min + 1` is at most `4 * ids.length`. Return true when it is acceptable and false otherwise.

**Constraints.** The limits are:
- **Length** satisfies `1 <= ids.length <= 10^5`.
- **Values** are any 32-bit integers, including `Integer.MIN_VALUE` and `Integer.MAX_VALUE`.
- **Arithmetic** must not overflow, so the range uses `long`.
- **Answer** is a boolean.

**Example 1.** Input `ids = [5, 7, 6, 9]`, output true, because the range 5 is at most 16.

**Example 2.** Input `ids = [2, 1000000000]`, output false, although both values are integers.

**Hint.** What value does `max - min + 1` take in `int` when `min` is `Integer.MIN_VALUE` and `max` is `Integer.MAX_VALUE`?

**Changed decision.** The decision depends on the key range and not on the number of keys, and the range needs wider arithmetic.

#### [Recognize] Design HashMap (LeetCode 706)
<!-- id: hm-design-hashmap -->

**Prerequisites.** All three exercises above.

**Problem.** Implement a class `MyHashMap` without `java.util.HashMap` and without any array indexed by the key. The class supports `put(int key, int value)`, which stores or replaces the value, `get(int key)`, which returns the value or -1 when the key is absent, and `remove(int key)`, which deletes the key if present.

**Constraints.** The limits are:
- **Keys** are any 32-bit integers, so the key range is 2^32.
- **Values** satisfy `0 <= value <= 10^9`.
- **Calls** number at most `10^5` in total.
- **Method** stores entries in an array of buckets chosen by `Math.floorMod(Integer.hashCode(key), buckets.length)`.

**Example 1.** Input: `put(7, 70)`, `put(-3, 5)`, `get(7)`, `get(8)`; output `70`, then `-1`.

**Example 2.** Input: `put(7, 70)`, `put(7, 71)`, `remove(7)`, `get(7)`; output `-1`.

**Hint.** Which statement of the problem rules out an array with one slot per key, and what replaces the key as the array index?

**Changed decision.** The key range is far too large for direct addressing, so a hash of the key picks a bucket and the bucket holds a short list.
