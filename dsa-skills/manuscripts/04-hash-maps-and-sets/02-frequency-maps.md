<!-- lesson-kind: standard -->
<!-- lesson-id: frequency-maps -->
## Count Values With A Map

<!-- stage: context -->
### The First Error Code That Occurred Once

A monitoring page reads a log of up to 100000 numeric error codes. Most codes repeat many times, because one broken service raises the same code again and again. The page must show the first code that occurred exactly once, since a code that never repeats is often a new kind of fault. The first version of the page freezes while it reads a long log, and the second version, with the same output, finishes at once.

The two versions differ in how they learn how often a code occurred. A set can say that a code occurred, but this question needs the number of times. The question is what the program must store to learn all the counts in one pass, and how it then finds the first code with a count of one.

<!-- stage: naive -->
### Counting Each Code By Rescanning

The direct method visits each position in order. At each position it scans the whole log to count the code. It returns the first position whose code occurs once.

```java
static int firstUniqueIndex(int[] codes) {
    for (int i = 0; i < codes.length; i++) {
        int times = 0;
        for (int j = 0; j < codes.length; j++) {
            if (codes[j] == codes[i]) {
                times++;
            }
        }
        if (times == 1) {
            return i;
        }
    }
    return -1;
}
```

On `[4, 7, 4, 9, 7, 2]` the method returns 3, because the code 9 occurs once and the code 4 at index 0 occurs twice. On `[5, 5, 6, 6]` every code occurs twice, so the method returns -1.

<!-- stage: bottleneck -->
### One Code Gets Counted Again And Again

```predict
A log of 100000 codes holds the code 4 exactly 50000 times. How many times does the method compute the count of the code 4, and what does the whole method cost?

It computes the count of the code 4 once for each of its 50000 positions, and every computation returns the same number. The outer loop runs n times and each pass scans n codes, so the cost is O(n^2).
```

The count of a code does not change while the method runs. Still, the method recomputes it for every position that holds the code, and each computation scans the whole log. A log with few distinct codes makes the waste large, because the same few answers get computed thousands of times. The program needs each count once. A first pass that records all counts takes O(n) time, and a second pass that reads those counts can find the answer in O(n) time.

<!-- stage: insight -->
### Store One Count For Each Key

The first pass must store a number for each distinct code, and it must find that number quickly when the same code returns.

#### Map Each Key To A Count

A **map** stores pairs of a key and a value, and it finds the value for a key in expected constant time. Java's class is `HashMap`. Here the key is an error code and the value is how often the code occurred. A map used this way is a **frequency map**. Each pair is one **entry**. The set from the previous lesson is a map that keeps keys and drops values, so a frequency map adds exactly the fact that a set discards.

<!-- names: frequency map, entry, absent key -->

#### Decide What An Absent Key Means

The frequency map stores an entry only for a code that has occurred. A code with no entry is an **absent key**, and the convention is that an absent key has count 0. The call `count.getOrDefault(code, 0)` applies that convention in one expression. The update `count.put(code, count.getOrDefault(code, 0) + 1)` then adds one occurrence.

#### The Invariant Of The Counting Pass

After the iteration for index `i`, each entry equals the number of times its code occurs in `codes[0..i]`. A code that has not occurred has no entry. When the pass ends, the map holds the exact count of every code in the whole log.

#### Read The Answer In Original Order

The second pass walks `codes` from index 0 and returns the first index whose count is 1. The map answers each count in expected constant time. The pass walks the array and not the map, because the map stores counts and does not store positions, so only the array knows which code came first. The total time is O(n) on average, and the space is O(d), where d is the number of distinct codes.

<!-- stage: variables -->
### Map, Index And Count

Both passes use the same small set of values.

- **count** maps each code that occurred to its number of occurrences, and the first pass adds one per position.
- **i** names the position being read and moves right by one in each pass.
- **codes[i]** is the key that the first pass increments and the second pass looks up.

<!-- stage: trace -->
### Counting And Then Scanning

#### A Log With One Unique Code

Take `codes = [4, 7, 4, 9, 7, 2]`. The first pass reads all six positions. After it, the map holds 4 with count 2, 7 with count 2, 9 with count 1 and 2 with count 1. The second pass starts at index 0. The code 4 has count 2, and the code 7 has count 2, so the pass moves on. At index 3 the code 9 has count 1, so the method returns 3.

#### A Log Without A Unique Code

Take `codes = [5, 5, 6, 6]`. The first pass gives 5 with count 2 and 6 with count 2. The second pass reads all four positions, finds no count of 1, and returns -1.

#### Stepping Through Both Logs

```trace
{"cells":[4,7,4,9,7,2],"pointers":["i"],"steps":[{"at":{"i":-1},"vars":{"count":"{}"},"note":"Start of the counting pass: the map is empty."},{"at":{"i":0},"vars":{"code":4,"count":"{4:1}"},"note":"Counting pass: code 4 now has count 1."},{"at":{"i":1},"vars":{"code":7,"count":"{4:1, 7:1}"},"note":"Counting pass: code 7 now has count 1."},{"at":{"i":2},"vars":{"code":4,"count":"{4:2, 7:1}"},"note":"Counting pass: code 4 now has count 2."},{"at":{"i":3},"vars":{"code":9,"count":"{4:2, 7:1, 9:1}"},"note":"Counting pass: code 9 now has count 1."},{"at":{"i":4},"vars":{"code":7,"count":"{4:2, 7:2, 9:1}"},"note":"Counting pass: code 7 now has count 2."},{"at":{"i":5},"vars":{"code":2,"count":"{4:2, 7:2, 9:1, 2:1}"},"note":"Counting pass: code 2 now has count 1."},{"at":{"i":0},"vars":{"code":4,"count":"{4:2, 7:2, 9:1, 2:1}"},"note":"Scan pass: code 4 has count 2, so move on."},{"at":{"i":1},"vars":{"code":7,"count":"{4:2, 7:2, 9:1, 2:1}"},"note":"Scan pass: code 7 has count 2, so move on."},{"at":{"i":2},"vars":{"code":4,"count":"{4:2, 7:2, 9:1, 2:1}"},"note":"Scan pass: code 4 has count 2, so move on."},{"at":{"i":3},"vars":{"code":9,"count":"{4:2, 7:2, 9:1, 2:1}"},"note":"Scan pass: code 9 has count 1, so the method returns 3."}]}
```

```trace
{"cells":[5,5,6,6],"pointers":["i"],"steps":[{"at":{"i":-1},"vars":{"count":"{}"},"note":"Start of the counting pass: the map is empty."},{"at":{"i":0},"vars":{"code":5,"count":"{5:1}"},"note":"Counting pass: code 5 now has count 1."},{"at":{"i":1},"vars":{"code":5,"count":"{5:2}"},"note":"Counting pass: code 5 now has count 2."},{"at":{"i":2},"vars":{"code":6,"count":"{5:2, 6:1}"},"note":"Counting pass: code 6 now has count 1."},{"at":{"i":3},"vars":{"code":6,"count":"{5:2, 6:2}"},"note":"Counting pass: code 6 now has count 2."},{"at":{"i":0},"vars":{"code":5,"count":"{5:2, 6:2}"},"note":"Scan pass: code 5 has count 2, so move on."},{"at":{"i":1},"vars":{"code":5,"count":"{5:2, 6:2}"},"note":"Scan pass: code 5 has count 2, so move on."},{"at":{"i":2},"vars":{"code":6,"count":"{5:2, 6:2}"},"note":"Scan pass: code 6 has count 2, so move on."},{"at":{"i":3},"vars":{"code":6,"count":"{5:2, 6:2}"},"note":"Scan pass: code 6 has count 2, so move on."},{"at":{"i":4},"vars":{"count":"{5:2, 6:2}"},"note":"The scan ends with no count of 1, so the method returns -1."}]}
```

<!-- stage: code -->
### A Counting Pass And A Scan

#### Finding The First Code With Count One

```java
static int firstUniqueIndex(int[] codes) {
    Map<Integer, Integer> count = new HashMap<>();
    for (int code : codes) {
        count.put(code, count.getOrDefault(code, 0) + 1);
    }
    for (int i = 0; i < codes.length; i++) {
        if (count.get(codes[i]) == 1) {
            return i;
        }
    }
    return -1;
}
```

#### What The Method Costs

Each pass makes n map operations of expected constant time, so the time is O(n) on average. The map holds one entry per distinct code, so the space is O(d), which is at most O(n). The expression `count.get(codes[i]) == 1` is safe here, because every code of the array has an entry after the first pass.

<!-- stage: applicability -->
### When A Map Of Counts Fits

#### Look For The Number Of Times

Use a frequency map when the answer depends on how often a value occurs, for example the first unique value or the most common value. Another case asks whether two collections hold the same values with the same multiplicities. The invariant is that `count.get(key)` equals the exact frequency of the key in the processed part of the input, with absent keys read as 0. A removal that brings a count to 0 must delete the entry, so that the map size and `containsKey` still describe the values that are present.

#### A Set Is A False Friend

A false friend here is a set, which can say that a value occurred but not how often. A set reports `[1, 1, 2]` and `[1, 2, 2]` as the same collection of values, although their frequencies differ. Sorting both arrays and comparing them also works for such questions, but it costs O(n log n) and reorders the data, so the original positions are lost.

#### Java Details That Cause Failures

The call `count.get(key)` returns `null` for an absent key, and unboxing the result in `int c = count.get(key)` throws `NullPointerException`. Use `getOrDefault(key, 0)` when the key may be absent. A comparison `count.get(a) == count.get(b)` compares `Integer` objects by reference, and it can pass for small counts, because Java caches the values from -128 to 127. It can then fail for larger counts. Use `equals`. When the program needs both key and value from a map, iterate over `entrySet()` and do not call `get` inside a loop over `keySet()`.

<!-- stage: exercises -->
### Exercises

#### [Build] First Unique Character (LeetCode 387)
<!-- id: hm-first-unique -->

**Prerequisites.** The frequency map and the second pass over the original order from this lesson.

**Problem.** Let `s` be a string. Return the smallest index `i` such that the character `s.charAt(i)` occurs exactly once in `s`. Return -1 when no character occurs exactly once.

**Constraints.** The limits are:
- **Length** satisfies `0 <= s.length() <= 10^5`; the empty string is legal.
- **Characters** are any Java `char` values.
- **Answer** is an index in `0..s.length() - 1`, or -1.
- **Order** of the answer follows the string, not the iteration order of the map.

**Example 1.** Input `s = "swiss"`, output 1, because `w` occurs once and `s` occurs three times.

**Example 2.** Input `s = "abab"`, output -1.

**Hint.** What does the first pass store, and which structure supplies the order for the second pass?

**Changed decision.** Basic case: one pass counts, and a second pass over the string finds the first count of one.

#### [Vary] Valid Anagram (LeetCode 242)
<!-- id: hm-valid-anagram -->

**Prerequisites.** First Unique Character above.

**Problem.** Let `s` and `t` be strings. They are anagrams when `t` is a rearrangement of the characters of `s`, with each character used the same number of times in both. Return true when they are anagrams.

**Constraints.** The limits are:
- **Length** satisfies `0 <= s.length(), t.length() <= 10^5`; the lengths may differ.
- **Characters** are any Java `char` values, so the method uses a map.
- **Answer** is a boolean.
- **Mutation** of the inputs is not allowed.

**Example 1.** Input `s = "listen"`, `t = "silent"`, output true.

**Example 2.** Input `s = "aab"`, `t = "abb"`, output false, because the counts of `a` differ.

**Hint.** If one string adds to the ledger and the other subtracts from it, what must every count be at the end?

**Changed decision.** The output compares two ledgers for equality and has no positions.

#### [Boundary] Remove Zero Counts (Author exercise)
<!-- id: hm-remove-zero-counts -->

**Prerequisites.** The two exercises above and the removal rule from the applicability stage.

**Problem.** Let `ops` be an array of pairs `{key, delta}`. Process the pairs in order, and add `delta` to the count of `key`. Return the number of keys whose count is greater than 0 after all pairs.

**Constraints.** The limits are:
- **Length** satisfies `0 <= ops.length <= 10^5`.
- **Values** `key` and `delta` are integers with `|delta| <= 100`.
- **Validity** guarantees that no count ever becomes negative.
- **Method** deletes an entry when its count returns to 0, so that the map size is the answer.

**Example 1.** Input `ops = [[3, 2], [5, 1], [3, -2]]`, output 1, because key 3 returns to 0 and key 5 holds 1.

**Example 2.** Input `ops = [[1, 4], [1, -4], [1, 4]]`, output 1.

**Hint.** What does `map.size()` count if a key keeps an entry with value 0?

**Changed decision.** A count can fall as well as rise, and an entry with count 0 must stop counting as present.

#### [Recognize] Unique Number Of Occurrences (LeetCode 1207)
<!-- id: hm-unique-occurrences -->

**Prerequisites.** All three exercises above and the set from the previous lesson.

**Problem.** Let `arr` be an integer array. Return true when no two distinct values of `arr` occur the same number of times.

**Constraints.** The limits are:
- **Length** satisfies `1 <= arr.length <= 1000`.
- **Values** satisfy `-1000 <= arr[i] <= 1000`.
- **Answer** is a boolean.
- **Method** may combine a map of counts with a set of counts.

**Example 1.** Input `arr = [4, 4, 9, 2, 9, 9]`, output true, because the counts are 2, 3 and 1.

**Example 2.** Input `arr = [1, 2]`, output false, because both values occur once.

**Hint.** After counting, what are the items of a second collection, and what does a repeated item mean?

**Changed decision.** The counts of the first map become the elements of a set.
