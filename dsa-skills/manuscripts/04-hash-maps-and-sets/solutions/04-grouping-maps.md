<!-- solutions-for: 04-grouping-maps -->
### Grouping Maps

#### Solution: [Build] Group by Remainder (Author exercise)
<!-- id: hm-group-by-remainder -->

**Approach.** Compute each key with `Math.floorMod`, which is never negative for a positive modulus, and append the number to the list for that key with `computeIfAbsent`. A `TreeMap` keeps the groups in increasing key order, and each list keeps input order because members are appended as they are read. With the `%` operator, `-1` and `3` would land in different groups for modulus 4, and the assertions show that. The oracle assigns each number to one of the `m` remainders by a nested loop over the possible remainders for small `m`, and the assertions compare the lists exactly.

**Complexity.** Expected O(n log g) for `g` distinct remainders because of the ordered map, and O(n) space.

```java run
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Random;
import java.util.TreeMap;

public final class GroupByRemainder {
    static List<List<Integer>> groupByRemainder(int[] nums, int m) {
        Map<Integer, List<Integer>> groups = new TreeMap<>();
        for (int x : nums) {
            groups.computeIfAbsent(Math.floorMod(x, m), k -> new ArrayList<>()).add(x);
        }
        return new ArrayList<>(groups.values());
    }
    static List<List<Integer>> oracle(int[] nums, int m) {
        List<List<Integer>> out = new ArrayList<>();
        for (int r = 0; r < m; r++) {
            List<Integer> g = new ArrayList<>();
            for (int x : nums) if (((x % m) + m) % m == r) g.add(x);
            if (!g.isEmpty()) out.add(g);
        }
        return out;
    }

    public static void main(String[] args) {
        if (!groupByRemainder(new int[] {8, 3, 5, 12, 9}, 4).equals(List.of(List.of(8, 12), List.of(5, 9), List.of(3)))) throw new AssertionError("example 1");
        if (!groupByRemainder(new int[] {-1, 3}, 4).equals(List.of(List.of(-1, 3)))) throw new AssertionError("example 2");
        if (-1 % 4 != -1 || Math.floorMod(-1, 4) != 3) throw new AssertionError("% is negative for a negative dividend and floorMod is not");
        if (!groupByRemainder(new int[] {}, 3).isEmpty()) throw new AssertionError("empty input");
        Random rnd = new Random(55);
        for (int t = 0; t < 4000; t++) {
            int[] x = new int[rnd.nextInt(12)];
            for (int i = 0; i < x.length; i++) x[i] = rnd.nextInt(30) - 12;
            int m = 1 + rnd.nextInt(6);
            if (!groupByRemainder(x, m).equals(oracle(x, m))) throw new AssertionError("disagrees with the remainder sweep");
        }
    }
}
```

#### Solution: [Vary] Group the People Given the Group Size They Belong To (LeetCode 1282)
<!-- id: hm-group-people-by-size -->

**Approach.** Use the required size as the key, with one waiting bucket per size. Append each person to the bucket for their size, and when the bucket reaches that size, add it to the result and remove it from the map, so the next person of that size starts a fresh bucket. The map therefore holds only unfinished buckets. The assertions check the exact outputs of the examples, and on random valid inputs they check that every person appears exactly once, that each emitted group has the size each member requires, and that no bucket is left waiting.

**Complexity.** Expected O(n) time and O(n) space.

```java run
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Random;

public final class GroupPeopleBySize {
    static List<List<Integer>> groupBySize(int[] size) {
        Map<Integer, List<Integer>> waiting = new HashMap<>();
        List<List<Integer>> done = new ArrayList<>();
        for (int person = 0; person < size.length; person++) {
            List<Integer> bucket = waiting.computeIfAbsent(size[person], k -> new ArrayList<>());
            bucket.add(person);
            if (bucket.size() == size[person]) {
                done.add(bucket);
                waiting.remove(size[person]);
            }
        }
        if (!waiting.isEmpty()) throw new IllegalStateException("input had no valid grouping");
        return done;
    }

    public static void main(String[] args) {
        if (!groupBySize(new int[] {2, 1, 3, 3, 2, 3}).equals(List.of(List.of(1), List.of(0, 4), List.of(2, 3, 5)))) throw new AssertionError("example 1");
        if (!groupBySize(new int[] {1, 1}).equals(List.of(List.of(0), List.of(1)))) throw new AssertionError("example 2");
        Random rnd = new Random(56);
        for (int t = 0; t < 3000; t++) {
            List<Integer> sizes = new ArrayList<>();
            int groups = 1 + rnd.nextInt(5);
            for (int g = 0; g < groups; g++) {
                int s = 1 + rnd.nextInt(4);
                for (int i = 0; i < s; i++) sizes.add(s);
            }
            java.util.Collections.shuffle(sizes, rnd);
            int[] input = sizes.stream().mapToInt(Integer::intValue).toArray();
            boolean[] seen = new boolean[input.length];
            for (List<Integer> g : groupBySize(input)) {
                for (int p : g) {
                    if (seen[p]) throw new AssertionError("person placed twice");
                    seen[p] = true;
                    if (input[p] != g.size()) throw new AssertionError("group size differs from the member's requirement");
                }
            }
            for (boolean b : seen) if (!b) throw new AssertionError("person missing");
        }
    }
}
```

#### Solution: [Boundary] Empty Buckets (Author exercise)
<!-- id: hm-empty-buckets -->

**Approach.** Create a bucket only when a value arrives, by using `computeIfAbsent` inside a `TreeMap`, and report the size of each bucket in key order. A key that never occurs has no entry, so no empty bucket appears and memory depends on the number of distinct remainders, not on `m`. Reading a missing key with `get` returns null and creates nothing, which the assertions confirm, while `computeIfAbsent` creates exactly one entry. The oracle counts each value's remainder with a sorted list of remainders and compares the run lengths, and the assertions use a modulus of one billion to show that nothing proportional to `m` is built.

**Complexity.** Expected O(n log g) time for `g` distinct remainders, and O(n) space.

```java run
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Map;
import java.util.Random;
import java.util.TreeMap;

public final class EmptyBuckets {
    static List<Integer> bucketSizes(int[] nums, int m) {
        Map<Integer, List<Integer>> groups = new TreeMap<>();
        for (int x : nums) groups.computeIfAbsent(x % m, k -> new ArrayList<>()).add(x);
        List<Integer> sizes = new ArrayList<>();
        for (List<Integer> g : groups.values()) sizes.add(g.size());
        return sizes;
    }
    static List<Integer> oracle(int[] nums, int m) {
        List<Integer> rems = new ArrayList<>();
        for (int x : nums) rems.add(x % m);
        Collections.sort(rems);
        List<Integer> sizes = new ArrayList<>();
        for (int i = 0; i < rems.size(); ) {
            int j = i;
            while (j < rems.size() && rems.get(j).equals(rems.get(i))) j++;
            sizes.add(j - i);
            i = j;
        }
        return sizes;
    }

    public static void main(String[] args) {
        if (!bucketSizes(new int[] {10, 20, 30}, 1_000_000_000).equals(List.of(1, 1, 1))) throw new AssertionError("example 1");
        if (!bucketSizes(new int[] {}, 5).isEmpty()) throw new AssertionError("example 2");
        Map<Integer, List<Integer>> probe = new TreeMap<>();
        if (probe.get(7) != null || !probe.isEmpty()) throw new AssertionError("reading a missing key creates nothing");
        probe.computeIfAbsent(7, k -> new ArrayList<>());
        if (probe.size() != 1) throw new AssertionError("computeIfAbsent creates exactly one bucket");
        Random rnd = new Random(57);
        for (int t = 0; t < 4000; t++) {
            int[] x = new int[rnd.nextInt(14)];
            for (int i = 0; i < x.length; i++) x[i] = rnd.nextInt(40);
            int m = 1 + rnd.nextInt(8);
            if (!bucketSizes(x, m).equals(oracle(x, m))) throw new AssertionError("disagrees with the sorted-run count");
        }
    }
}
```

#### Solution: [Recognize] Group Anagrams (LeetCode 49)
<!-- id: hm-group-anagrams -->

**Approach.** Build the key from the 26 letter counts, writing a comma after each count, and use a `LinkedHashMap` from key to list of words so groups appear in order of first appearance. Two words are anagrams exactly when their count arrays are equal, so the key is canonical. Without the separator, `aaaaaaaaaaab` and `abbbbbbbbbbb` would both produce the same text of digits, and the assertions demonstrate that collision. The oracle groups by the sorted letters of each word, which is an independent key, and the assertions require the same groups in the same order.

**Complexity.** Expected O(n * L) time for `n` words of length at most `L`, and O(n * L) space for the keys and the lists.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Random;

public final class GroupAnagrams {
    static String key(String w, boolean separator) {
        int[] count = new int[26];
        for (char c : w.toCharArray()) count[c - 'a']++;
        StringBuilder sb = new StringBuilder();
        for (int c : count) { sb.append(c); if (separator) sb.append(','); }
        return sb.toString();
    }
    static List<List<String>> groupAnagrams(String[] words) {
        Map<String, List<String>> groups = new LinkedHashMap<>();
        for (String w : words) groups.computeIfAbsent(key(w, true), k -> new ArrayList<>()).add(w);
        return new ArrayList<>(groups.values());
    }
    static List<List<String>> oracle(String[] words) {
        Map<String, List<String>> groups = new LinkedHashMap<>();
        for (String w : words) {
            char[] c = w.toCharArray();
            Arrays.sort(c);
            groups.computeIfAbsent(new String(c), k -> new ArrayList<>()).add(w);
        }
        return new ArrayList<>(groups.values());
    }

    public static void main(String[] args) {
        String[] w1 = {"listen", "silent", "enlist", "google", "gogole", "cat"};
        if (!groupAnagrams(w1).equals(List.of(List.of("listen", "silent", "enlist"), List.of("google", "gogole"), List.of("cat")))) throw new AssertionError("example 1");
        if (!groupAnagrams(new String[] {""}).equals(List.of(List.of("")))) throw new AssertionError("example 2");
        String a = "aaaaaaaaaaab", b = "abbbbbbbbbbb";
        if (!key(a, false).equals(key(b, false))) throw new AssertionError("without a separator these two words collide");
        if (key(a, true).equals(key(b, true))) throw new AssertionError("with a separator they stay apart");
        Random rnd = new Random(58);
        for (int t = 0; t < 3000; t++) {
            String[] words = new String[1 + rnd.nextInt(10)];
            for (int i = 0; i < words.length; i++) {
                StringBuilder sb = new StringBuilder();
                int n = rnd.nextInt(5);
                for (int k = 0; k < n; k++) sb.append((char) ('a' + rnd.nextInt(3)));
                words[i] = sb.toString();
            }
            if (!groupAnagrams(words).equals(oracle(words))) throw new AssertionError("disagrees with the sorted-letters grouping");
        }
    }
}
```
