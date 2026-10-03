<!-- lesson-kind: standard -->
<!-- lesson-id: grouping-maps -->
## Grouping Maps

<!-- stage: context -->
### Sorting Letters Into Pigeonholes

A mailroom receives a heap of letters, each stamped with a postal district number. The clerk has a wall of pigeonholes, but she does not label them in advance, because only some of the thousand districts appear on any given day. When a letter arrives for district 14 she looks for the pigeonhole marked 14. If it exists she drops the letter in, and if not she puts up a new label and starts the pile there.

At the end of the day each pigeonhole holds all the letters for one district, in the order they arrived, and there are no empty holes for districts that sent nothing. A counting tally would have told her how many letters each district received, but it could not have handed her the letters. The pigeonholes keep the members, which is what the delivery round needs.

<!-- stage: naive -->
### Search The Piles For A Matching Label

Without labelled pigeonholes the clerk could keep a list of piles and, for each new letter, walk along the piles looking for one with the same district on its first letter.

```java
static List<List<Integer>> groupByList(int[] districts) {
    List<List<Integer>> piles = new ArrayList<>();
    for (int d : districts) {
        List<Integer> home = null;
        for (List<Integer> pile : piles) {
            if (pile.get(0) == d) { home = pile; break; }
        }
        if (home == null) { home = new ArrayList<>(); piles.add(home); }
        home.add(d);
    }
    return piles;
}
```

For `[14, 3, 14, 9]` it returns `[[14, 14], [3], [9]]`, which is the right grouping with piles in order of first appearance.

<!-- stage: bottleneck -->
### A Walk Along All The Piles

For each of the `n` letters the code may walk through every existing pile, so with `g` different districts the time is O(n * g), and when most letters have a distinct district that approaches O(n * n). The comparison `pile.get(0) == d` is also a hazard in Java, because it compares `Integer` objects by identity once values leave the small cached range, so a large district number could create a second pile for the same district.

The waste is the walk. The pile for a district is determined by the district alone, and no letter needs to be compared with any other letter. What is missing is a way to go from a district straight to its pile, which is the same lookup that a count needed, except that the entry has to be a growing list of members and not a number.

<!-- stage: insight -->
### Let The Key Own A Growing List

A **grouping map** has a key for each class of equivalent inputs and, as the entry, the list of all inputs in that class. In Java it is a `Map<K, List<V>>`. The **key function** decides which class an input belongs to, for example the district of a letter, the remainder of a number, or a signature built from a word. Two inputs are in the same group exactly when their key function gives equal keys. The invariant is that after reading a prefix, `groups.get(key)` holds every processed input with that key, in arrival order.

Each **bucket** is created only when its first member arrives. In Java the call `computeIfAbsent(key, k -> new ArrayList<>()).add(value)` does both steps at once: it creates the list if the key is absent and then appends. This keeps the map free of empty buckets, and it matters when the key space is huge. Pre-creating one bucket for every possible key would cost memory proportional to the number of possible keys instead of the number of keys that occur.

<!-- names: grouping map, key function, bucket -->

Some problems add a rule about when a bucket is finished. If each key owns a bucket of a required size, the bucket is emitted and cleared when it becomes full, and the map then holds only buckets that are still waiting. The idea is the same, because a key still leads to one list, but the list is handed over and emptied instead of kept until the end. The cost is expected O(n) for the pass and O(n) space for the members stored.

<!-- stage: variables -->
### Keys, Lists And A Key Function

The map `groups` goes from key to list. The key function is a small pure computation applied to each input, and it must give equal keys for equivalent inputs and different keys otherwise. The output order comes from the map's iteration order, which is unspecified for `HashMap`, so use `LinkedHashMap` for order of first appearance or `TreeMap` for key order whenever the answer must be reproducible. Members appear within each list in the order they were read. A key that never occurs has no entry, so it cannot appear in the result.

<!-- stage: trace -->
### Filling Buckets, Then Emitting Them

```trace
{"cells":[7,4,9,2,10],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"value":7,"key":1,"buckets":"{1:[7]}"},"note":"Value 7 has key 1. A new bucket is created. Buckets: {1:[7]}."},{"at":{"i":1},"vars":{"value":4,"key":1,"buckets":"{1:[7, 4]}"},"note":"Value 4 has key 1. The bucket already exists. Buckets: {1:[7, 4]}."},{"at":{"i":2},"vars":{"value":9,"key":0,"buckets":"{1:[7, 4], 0:[9]}"},"note":"Value 9 has key 0. A new bucket is created. Buckets: {1:[7, 4], 0:[9]}."},{"at":{"i":3},"vars":{"value":2,"key":2,"buckets":"{1:[7, 4], 0:[9], 2:[2]}"},"note":"Value 2 has key 2. A new bucket is created. Buckets: {1:[7, 4], 0:[9], 2:[2]}."},{"at":{"i":4},"vars":{"value":10,"key":1,"buckets":"{1:[7, 4, 10], 0:[9], 2:[2]}"},"note":"Value 10 has key 1. The bucket already exists. Buckets: {1:[7, 4, 10], 0:[9], 2:[2]}."}]}
```

Take the numbers `[7, 4, 9, 2, 10]` grouped by the remainder after dividing by 3. The 7 has remainder 1, so a bucket for 1 is created and holds 7. The 4 also has remainder 1 and joins it. The 9 has remainder 0 and starts a bucket, the 2 has remainder 2 and starts another, and the 10 joins bucket 1. At the end bucket 1 holds `[7, 4, 10]`, bucket 0 holds `[9]` and bucket 2 holds `[2]`.

```trace
{"cells":[2,1,3,3,2,3],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"size":2,"waiting":"{2:[0]}","emitted":"[]"},"note":"Person 0 needs size 2. The bucket holds [0] and is not full yet."},{"at":{"i":1},"vars":{"size":1,"waiting":"{2:[0]}","emitted":"[[1]]"},"note":"Person 1 needs size 1. The bucket is full, so emit [1] and remove it. Emitted: [[1]]."},{"at":{"i":2},"vars":{"size":3,"waiting":"{2:[0], 3:[2]}","emitted":"[[1]]"},"note":"Person 2 needs size 3. The bucket holds [2] and is not full yet."},{"at":{"i":3},"vars":{"size":3,"waiting":"{2:[0], 3:[2, 3]}","emitted":"[[1]]"},"note":"Person 3 needs size 3. The bucket holds [2, 3] and is not full yet."},{"at":{"i":4},"vars":{"size":2,"waiting":"{3:[2, 3]}","emitted":"[[1], [0, 4]]"},"note":"Person 4 needs size 2. The bucket is full, so emit [0, 4] and remove it. Emitted: [[1], [0, 4]]."},{"at":{"i":5},"vars":{"size":3,"waiting":"{}","emitted":"[[1], [0, 4], [2, 3, 5]]"},"note":"Person 5 needs size 3. The bucket is full, so emit [2, 3, 5] and remove it. Emitted: [[1], [0, 4], [2, 3, 5]]."}]}
```

The second trace uses the group-size rule. Each cell is the size of the group that person must belong to. Person 0 wants a group of 2, so a bucket for size 2 opens. Person 1 wants size 1, and the bucket is full at once, so `[1]` is emitted. Persons 2 and 3 fill part of a bucket for size 3, person 4 completes the size-2 bucket as `[0, 4]`, and person 5 completes the size-3 bucket as `[2, 3, 5]`.

<!-- stage: code -->
### Grouping, Emitting And Signatures

```java
static List<List<Integer>> groupByRemainder(int[] nums, int m) {
    Map<Integer, List<Integer>> groups = new TreeMap<>();
    for (int x : nums) {
        groups.computeIfAbsent(Math.floorMod(x, m), k -> new ArrayList<>()).add(x);
    }
    return new ArrayList<>(groups.values());
}

static List<List<Integer>> groupBySize(int[] size) {
    Map<Integer, List<Integer>> waiting = new HashMap<>();
    List<List<Integer>> done = new ArrayList<>();
    for (int person = 0; person < size.length; person++) {
        List<Integer> bucket = waiting.computeIfAbsent(size[person], k -> new ArrayList<>());
        bucket.add(person);
        if (bucket.size() == size[person]) {
            done.add(bucket);                          // full: hand it over
            waiting.remove(size[person]);              // and start a fresh one next time
        }
    }
    return done;
}

static List<List<String>> groupAnagrams(String[] words) {
    Map<String, List<String>> groups = new LinkedHashMap<>();
    for (String w : words) {
        int[] count = new int[26];
        for (char c : w.toCharArray()) count[c - 'a']++;
        StringBuilder key = new StringBuilder();
        for (int c : count) key.append(c).append(',');     // separator keeps 1,11 apart from 11,1
        groups.computeIfAbsent(key.toString(), k -> new ArrayList<>()).add(w);
    }
    return new ArrayList<>(groups.values());
}
```

Each method makes one pass with expected constant map work per input, and the anagram key costs O(26) per word, so the grouping is expected O(n) for a fixed alphabet. `Math.floorMod` is used because `%` can be negative in Java, which would put `-1` and `3` in different groups for a modulus of 4. `LinkedHashMap` keeps groups in order of first appearance and `TreeMap` keeps them in key order, so the output is reproducible.

<!-- stage: applicability -->
### When Members Must Be Kept

Use a grouping map when the answer is a collection of lists, one per equivalence class, and each list must contain the members and not only their number. The invariant worth stating is that each key owns exactly the processed inputs whose key function equals it. Decide the key function first, and check that equivalent inputs always produce equal keys.

The false friend is a frequency map. It gives the size of each class and discards the members, so it cannot produce grouped output. The reverse mistake wastes memory, because lists of members are heavier than counts when only sizes are needed. Another false friend is a key that is not canonical, such as an anagram key that depends on letter order, which splits one class into several buckets.

Java hazards are specific. Keys must have a correct `equals` and `hashCode`, which `String` and the boxed numbers have and arrays do not, so never use an `int[]` as a key and convert it to a string or a record instead. Negative numbers need `Math.floorMod`. Build keys with a separator when concatenating numbers, since `"1" + "11"` equals `"11" + "1"`. Iteration order of `HashMap` is unspecified, so choose `LinkedHashMap` or `TreeMap` before the answer must be stable.

<!-- stage: exercises -->
### Exercises

#### [Build] Group by Remainder (Author exercise)
<!-- id: hm-group-by-remainder -->

**Prerequisites.** Lesson on frequency maps; the grouping map in this lesson.

**Problem.** Given an integer array `nums` and a positive integer `m`, return the numbers grouped by `Math.floorMod(value, m)`. The groups come in increasing order of remainder, and the numbers inside a group keep their input order.

**Constraints.** 0 <= nums.length <= 10^4, 1 <= m <= 10^9, and values lie in -10^9..10^9. Negative values are allowed.

**Example 1.** Input `nums = [8, 3, 5, 12, 9]`, `m = 4`, output `[[8, 12], [5, 9], [3]]`.

**Example 2.** Input `nums = [-1, 3]`, `m = 4`, output `[[-1, 3]]`, because the floor remainder of -1 is 3.

**Hint.** What does `-1 % 4` give in Java, and which method gives the remainder you want? What should the map's value be?

**Changed decision.** First rung: the entry is a list of members, so the map owns the group and not just a number.

#### [Vary] Group the People Given the Group Size They Belong To (LeetCode 1282)
<!-- id: hm-group-people-by-size -->

**Prerequisites.** The build exercise above.

**Problem.** Person `i` must be in a group of exactly `groupSizes[i]` people. Return a list of groups of person indices such that every person appears exactly once and every group has the size its members require. Emit a group as soon as it is full.

**Constraints.** 1 <= n <= 500, 1 <= groupSizes[i] <= n, and at least one valid grouping exists. Any valid grouping that follows the emit rule is accepted.

**Example 1.** Input `groupSizes = [2, 1, 3, 3, 2, 3]`, output `[[1], [0, 4], [2, 3, 5]]`.

**Example 2.** Input `groupSizes = [1, 1]`, output `[[0], [1]]`, since each person forms a group alone.

**Hint.** What should happen to a bucket in the map after it is handed over? Which key should represent the group a person is waiting in?

**Changed decision.** A bucket now has a completion rule, so full buckets are emitted and removed from the map.

#### [Boundary] Empty Buckets (Author exercise)
<!-- id: hm-empty-buckets -->

**Prerequisites.** The two exercises above.

**Problem.** Given `nums` and a modulus `m`, return the sizes of the non-empty remainder groups in increasing order of remainder. Do not create a bucket for any remainder that received no value, and do not allocate memory proportional to `m`.

**Constraints.** 0 <= nums.length <= 10^4 and 1 <= m <= 10^9. The values are non-negative. Memory must depend only on the values that occur.

**Example 1.** Input `nums = [10, 20, 30]`, `m = 1000000000`, output `[1, 1, 1]`.

**Example 2.** Input `nums = []`, `m = 5`, output `[]`, because no bucket was ever created.

**Hint.** What would an array with one slot per remainder cost when `m` is a billion? Which map call creates a bucket only on demand?

**Changed decision.** Buckets must be created only when a member arrives, which is what keeps memory proportional to the keys that occur.

#### [Recognize] Group Anagrams (LeetCode 49)
<!-- id: hm-group-anagrams -->

**Prerequisites.** All three exercises above.

**Problem.** Given an array of lowercase words, group the words that are anagrams of each other. Groups are listed in order of the first word of each group, and words keep their input order inside a group. Build the key from a count of each letter, with a separator between counts.

**Constraints.** 1 <= words.length <= 10^4 and each word has 0 to 100 lowercase letters. An empty word is a valid word.

**Example 1.** Input `words = ["listen", "silent", "enlist", "google", "gogole", "cat"]`, output `[["listen", "silent", "enlist"], ["google", "gogole"], ["cat"]]`.

**Example 2.** Input `words = [""]`, output `[[""]]`, since the empty word forms one group.

**Hint.** Which key is the same for any two anagrams and different for any two non-anagrams? What could go wrong if the counts are joined with no separator?

**Changed decision.** The key function is now a computed signature, so correctness depends on the signature being canonical and unambiguous.
