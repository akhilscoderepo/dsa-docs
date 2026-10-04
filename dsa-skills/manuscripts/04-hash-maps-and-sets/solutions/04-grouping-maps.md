<!-- solutions-for: 04-hash-maps-and-sets -->
### Solutions For Grouping Values

#### Solution: [Build] Group By Remainder (Author exercise)
<!-- id: hm-group-by-remainder -->

**Approach.**
The key of a value is `Math.floorMod(value, m)`, which lies in `0..m-1` even for negative values. A `LinkedHashMap` from key to list receives each value through `computeIfAbsent(key, ...).add(value)`, so a list exists only after its first value arrives. The invariant is that after index `i`, each list holds exactly the values of `nums[0..i]` with that key, in input order. The map lists keys in order of first appearance. The harness asserts that `%` gives a negative key for a negative value, that `floorMod` does not, and that `computeIfAbsent` creates one list per key only.

**Complexity.**
- **Time** is O(n) on average, because each value costs one key computation, one map operation and one append.
- **Space** is O(n), because the lists together hold n values; the space does not depend on `m`.

```java run
import java.util.*;

public final class GroupByRemainder {
    /**
     * Groups values by floorMod(value, m); groups follow first appearance of their keys.
     * Time: O(n) expected. Space: O(n).
     * Invariant: after index i, each list holds the values of nums[0..i] with that key, in input order.
     */
    static List<List<Integer>> group(int[] nums, int m) {
        Map<Integer, List<Integer>> groups = new LinkedHashMap<>();
        // One iteration per value.
        for (int v : nums) {
            // floorMod keeps the key in 0..m-1 for negative values too.
            int key = Math.floorMod(v, m);
            // The list is created only when the key first appears, then the value joins it.
            groups.computeIfAbsent(key, k -> new ArrayList<>()).add(v);
        }
        return new ArrayList<>(groups.values());
    }

    /** Lesson code: one scan per worker number, kept as the oracle. */
    static List<List<Integer>> naive(int[] jobs, int m) {
        List<List<Integer>> result = new ArrayList<>();
        for (int worker = 0; worker < m; worker++) {
            List<Integer> mine = new ArrayList<>();
            for (int job : jobs) if (Math.floorMod(job, m) == worker) mine.add(job);
            if (!mine.isEmpty()) result.add(mine);
        }
        return result;
    }

    public static void main(String[] args) {
        // The statement examples.
        if (!group(new int[] {9, 4, 6, 1, -2}, 3).equals(List.of(List.of(9, 6), List.of(4, 1, -2)))) throw new AssertionError("example 1");
        if (!group(new int[0], 5).isEmpty()) throw new AssertionError("example 2");
        // The lesson traces.
        if (!group(new int[] {7, -1, 4, 2, 10, 5}, 3).equals(List.of(List.of(7, 4, 10), List.of(-1, 2, 5)))) throw new AssertionError("trace 1");
        if (!group(new int[] {8, 3, 12, 5, 4}, 4).equals(List.of(List.of(8, 12, 4), List.of(3), List.of(5)))) throw new AssertionError("trace 2");
        // Java facts from the lesson.
        if (-1 % 3 != -1 || Math.floorMod(-1, 3) != 2) throw new AssertionError("remainder of a negative value");
        Map<Integer, List<Integer>> probe = new HashMap<>();
        probe.computeIfAbsent(1, k -> new ArrayList<>()).add(5);
        probe.computeIfAbsent(1, k -> new ArrayList<>()).add(6);
        if (probe.size() != 1 || !probe.get(1).equals(List.of(5, 6))) throw new AssertionError("computeIfAbsent");
        // The modulus may be huge without extra cost.
        if (group(new int[] {5, 1_000_000_005}, 1_000_000_000).size() != 1) throw new AssertionError("large modulus");
        // Random arrays are checked against the one-scan-per-key oracle for key order by first appearance.
        Random rnd = new Random(52);
        for (int t = 0; t < 500; t++) {
            int[] a = new int[rnd.nextInt(10)];
            for (int k = 0; k < a.length; k++) a[k] = rnd.nextInt(21) - 10;
            int m = 1 + rnd.nextInt(5);
            List<List<Integer>> got = group(a, m), want = naive(a, m);
            // The oracle lists groups by key; compare as sets of groups.
            if (!new HashSet<>(got).equals(new HashSet<>(want)) || got.size() != want.size()) throw new AssertionError(Arrays.toString(a));
            // Order check: each group's first value appears in increasing index order of the input.
            int last = -1;
            for (List<Integer> g : got) {
                int idx = -1;
                for (int i = 0; i < a.length; i++) if (a[i] == g.get(0)) { idx = i; break; }
                if (idx <= last) throw new AssertionError("group order");
                last = idx;
            }
        }
    }
}
```

#### Solution: [Vary] Group The People By Group Size (LeetCode 1282)
<!-- id: hm-group-people -->

**Approach.**
The key of a person is the required size. The map holds, for each size, the one group that is still filling. A person joins the bucket of their size. When the bucket reaches that size, the method appends it to the answer and removes the key. The next person of that size then starts a new bucket. The invariant is that every bucket in the map holds fewer members than its key, and every emitted group holds exactly its size. A valid partition exists, so the map is empty when the loop ends.

**Complexity.**
- **Time** is O(n) on average, because each person causes one map operation and one append. Each emitted group enters the answer once.
- **Space** is O(n), because the buckets and the answer hold at most n person numbers.

```java run
import java.util.*;

public final class GroupPeople {
    /**
     * Partitions persons into groups of the size each person demands, in order of completion.
     * Time: O(n) expected. Space: O(n).
     * Invariant: each bucket in filling holds fewer members than its key.
     */
    static List<List<Integer>> groupThePeople(int[] sizes) {
        Map<Integer, List<Integer>> filling = new HashMap<>();
        List<List<Integer>> done = new ArrayList<>();
        // One iteration per person.
        for (int p = 0; p < sizes.length; p++) {
            List<Integer> bucket = filling.computeIfAbsent(sizes[p], k -> new ArrayList<>());
            bucket.add(p);
            // A full bucket leaves the map, so the next person of this size starts a fresh one.
            if (bucket.size() == sizes[p]) {
                done.add(bucket);
                filling.remove(sizes[p]);
            }
        }
        return done;
    }

    public static void main(String[] args) {
        // The statement examples.
        if (!groupThePeople(new int[] {2, 1, 2, 3, 3, 3}).equals(List.of(List.of(1), List.of(0, 2), List.of(3, 4, 5)))) throw new AssertionError("example 1");
        if (!groupThePeople(new int[] {1, 1}).equals(List.of(List.of(0), List.of(1)))) throw new AssertionError("example 2");
        // Random valid inputs: build sizes from random groups, shuffle the persons, then verify the contract.
        Random rnd = new Random(53);
        for (int t = 0; t < 500; t++) {
            List<Integer> sizeList = new ArrayList<>();
            int groups = 1 + rnd.nextInt(4);
            for (int g = 0; g < groups; g++) {
                int s = 1 + rnd.nextInt(4);
                for (int k = 0; k < s; k++) sizeList.add(s);
            }
            Collections.shuffle(sizeList, rnd);
            int[] sizes = new int[sizeList.size()];
            for (int i = 0; i < sizes.length; i++) sizes[i] = sizeList.get(i);
            boolean[] used = new boolean[sizes.length];
            for (List<Integer> g : groupThePeople(sizes)) {
                for (int member : g) {
                    if (used[member] || sizes[member] != g.size()) throw new AssertionError("bad group");
                    used[member] = true;
                }
                for (int i = 1; i < g.size(); i++) if (g.get(i) <= g.get(i - 1)) throw new AssertionError("member order");
            }
            for (boolean u : used) if (!u) throw new AssertionError("person left out");
        }
    }
}
```

#### Solution: [Boundary] Empty Buckets (Author exercise)
<!-- id: hm-empty-buckets -->

**Approach.**
A key exists in the map only after a value with that key arrives, so the map never holds an empty bucket. The method counts values per key in a `LinkedHashMap`, which gives the sizes of the non-empty groups in order of first appearance. Allocating one bucket per possible key would cost `m` units of time and memory, and `m` can reach one billion. The invariant is that every key in the map has a count of at least 1. The harness also runs a modulus of one billion with three values and checks that the answer holds three entries at most.

**Complexity.**
- **Time** is O(n) on average, whatever the value of `m`.
- **Space** is O(d) for d distinct keys that received a value, at most n.

```java run
import java.util.*;

public final class EmptyBuckets {
    /**
     * Returns the sizes of the non-empty remainder groups, in order of first appearance of the key.
     * Time: O(n) expected. Space: O(d).
     * Invariant: every key in sizes has a count of at least 1.
     */
    static int[] groupSizes(int[] nums, int m) {
        Map<Integer, Integer> sizes = new LinkedHashMap<>();
        // One iteration per value; no work depends on m.
        for (int v : nums) {
            sizes.merge(Math.floorMod(v, m), 1, Integer::sum);
        }
        int[] out = new int[sizes.size()];
        int k = 0;
        // entrySet gives key and value together; only the value matters here, so values() would also work.
        for (Map.Entry<Integer, Integer> e : sizes.entrySet()) {
            out[k++] = e.getValue();
        }
        return out;
    }

    public static void main(String[] args) {
        // The statement examples.
        if (!Arrays.equals(groupSizes(new int[] {10, 20, 31, 41, 51}, 10), new int[] {2, 3})) throw new AssertionError("example 1");
        if (groupSizes(new int[0], 7).length != 0) throw new AssertionError("example 2");
        // A huge modulus with few values answers at once.
        if (groupSizes(new int[] {1, 2, 3}, 1_000_000_000).length != 3) throw new AssertionError("large modulus");
        if (groupSizes(new int[] {-1, 999_999_999}, 1_000_000_000).length != 1) throw new AssertionError("negative key joins");
        // Random arrays are checked against a per-key count that visits every possible key.
        Random rnd = new Random(54);
        for (int t = 0; t < 500; t++) {
            int[] a = new int[rnd.nextInt(10)];
            for (int k = 0; k < a.length; k++) a[k] = rnd.nextInt(30) - 10;
            int m = 1 + rnd.nextInt(6);
            List<Integer> want = new ArrayList<>();
            List<Integer> order = new ArrayList<>();
            for (int v : a) if (!order.contains(Math.floorMod(v, m))) order.add(Math.floorMod(v, m));
            for (int key : order) {
                int c = 0;
                for (int v : a) if (Math.floorMod(v, m) == key) c++;
                want.add(c);
            }
            int[] got = groupSizes(a, m);
            if (got.length != want.size()) throw new AssertionError("length");
            for (int i = 0; i < got.length; i++) if (got[i] != want.get(i)) throw new AssertionError("value");
        }
    }
}
```

#### Solution: [Recognize] Group Anagrams (LeetCode 49)
<!-- id: hm-group-anagrams -->

**Approach.**
Two words are anagrams exactly when their 26 letter counts are equal. The method builds a string from the 26 counts, separated by commas so that the counts 1 and 11 cannot merge into one digit run. That string is the group key, and a `LinkedHashMap` from key to list owns one bucket per signature. The invariant is that after word `i`, each bucket holds the words of `words[0..i]` with that signature, in input order. Building a key costs the word length plus 26, which is cheaper than sorting the word.

**Complexity.**
- **Time** is O(n * (L + 26)) on average for n words of length at most L. Each word needs one counting pass, one key build and one map operation.
- **Space** is O(n * L) for the buckets, plus a key of about 26 numbers for each distinct signature.

```java run
import java.util.*;

public final class GroupAnagrams {
    /**
     * Groups words that are rearrangements of each other.
     * Time: O(n * (L + 26)) expected. Space: O(n * L).
     * Invariant: after word i, each bucket holds the words of words[0..i] with that letter-count signature.
     */
    static List<List<String>> groupAnagrams(String[] words) {
        Map<String, List<String>> groups = new LinkedHashMap<>();
        // One iteration per word.
        for (String w : words) {
            int[] counts = new int[26];
            // The counting pass reads each letter once.
            for (int i = 0; i < w.length(); i++) counts[w.charAt(i) - 'a']++;
            StringBuilder key = new StringBuilder();
            // The commas keep the counts 1,11 distinct from 11,1.
            for (int c : counts) key.append(c).append(',');
            groups.computeIfAbsent(key.toString(), k -> new ArrayList<>()).add(w);
        }
        return new ArrayList<>(groups.values());
    }

    public static void main(String[] args) {
        // The statement examples.
        List<List<String>> g1 = groupAnagrams(new String[] {"stop", "pots", "cat", "tops", "act", "dog"});
        if (!g1.equals(List.of(List.of("stop", "pots", "tops"), List.of("cat", "act"), List.of("dog")))) throw new AssertionError("example 1");
        if (!groupAnagrams(new String[] {""}).equals(List.of(List.of("")))) throw new AssertionError("example 2");
        if (!groupAnagrams(new String[0]).isEmpty()) throw new AssertionError("empty");
        // Random words are checked against a sorted-letters key, with the same bucket order.
        Random rnd = new Random(55);
        for (int t = 0; t < 400; t++) {
            String[] words = new String[rnd.nextInt(8)];
            for (int k = 0; k < words.length; k++) {
                StringBuilder sb = new StringBuilder();
                int len = rnd.nextInt(4);
                for (int j = 0; j < len; j++) sb.append((char) ('a' + rnd.nextInt(3)));
                words[k] = sb.toString();
            }
            Map<String, List<String>> oracle = new LinkedHashMap<>();
            for (String w : words) {
                char[] cs = w.toCharArray();
                Arrays.sort(cs);
                oracle.computeIfAbsent(new String(cs), k -> new ArrayList<>()).add(w);
            }
            if (!groupAnagrams(words).equals(new ArrayList<>(oracle.values()))) throw new AssertionError(Arrays.toString(words));
        }
    }
}
```
