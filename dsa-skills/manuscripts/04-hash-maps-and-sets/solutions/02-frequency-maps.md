<!-- solutions-for: 04-hash-maps-and-sets -->
### Solutions For Counting Values

#### Solution: [Build] First Unique Character (LeetCode 387)
<!-- id: hm-first-unique -->

**Approach.**
The first pass builds a frequency map from character to count. The second pass walks the string from index 0 and returns the first index whose character has count 1. The map cannot supply the order, because it stores counts and no positions, so the second pass reads the string. The invariant of the first pass is that after index `i`, every character of `s[0..i]` has an entry equal to its occurrences there. The harness also asserts three Java facts. Unboxing a missing key throws `NullPointerException`, `getOrDefault` returns the stated default, and `Integer` values from -128 to 127 share one object while `equals` compares values.

**Complexity.**
- **Time** is O(n) on average, because each of the two passes makes n map operations of expected constant time.
- **Space** is O(d) for d distinct characters, which is at most n.

```java run
import java.util.*;

public final class FirstUnique {
    /**
     * Returns the smallest index whose character occurs exactly once, or -1.
     * Time: O(n) expected. Space: O(d) for d distinct characters.
     * Invariant: after pass one, count.get(c) is the number of occurrences of c in s.
     */
    static int firstUniqueChar(String s) {
        Map<Character, Integer> count = new HashMap<>();
        // Pass one costs n map updates; an absent key counts as 0.
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            count.put(c, count.getOrDefault(c, 0) + 1);
        }
        // Pass two walks the string, because only the string knows the order.
        for (int i = 0; i < s.length(); i++) {
            if (count.get(s.charAt(i)) == 1) {
                return i;
            }
        }
        return -1;
    }

    /** Lesson code: the rescanning method, kept as the oracle. */
    static int naive(String s) {
        for (int i = 0; i < s.length(); i++) {
            int times = 0;
            for (int j = 0; j < s.length(); j++) if (s.charAt(j) == s.charAt(i)) times++;
            if (times == 1) return i;
        }
        return -1;
    }

    public static void main(String[] args) {
        // The statement examples and the empty string.
        if (firstUniqueChar("swiss") != 1) throw new AssertionError("example 1");
        if (firstUniqueChar("abab") != -1) throw new AssertionError("example 2");
        if (firstUniqueChar("") != -1) throw new AssertionError("empty");
        // The lesson's integer version on its two trace logs.
        if (lessonCodes(new int[] {4, 7, 4, 9, 7, 2}) != 3 || lessonCodes(new int[] {5, 5, 6, 6}) != -1) throw new AssertionError("lesson code");
        // Java facts from the lesson.
        Map<Integer, Integer> m = new HashMap<>();
        boolean threw = false;
        try { int c = m.get(7); } catch (NullPointerException e) { threw = true; }
        if (!threw) throw new AssertionError("unboxing null");
        if (m.getOrDefault(7, 0) != 0) throw new AssertionError("getOrDefault");
        if (Integer.valueOf(127) != Integer.valueOf(127)) throw new AssertionError("cached values");
        if (!Integer.valueOf(5000).equals(Integer.valueOf(5000))) throw new AssertionError("equals");
        // Random strings are checked against the rescanning oracle.
        Random rnd = new Random(44);
        for (int t = 0; t < 500; t++) {
            StringBuilder sb = new StringBuilder();
            int len = rnd.nextInt(10);
            for (int k = 0; k < len; k++) sb.append((char) ('a' + rnd.nextInt(5)));
            if (firstUniqueChar(sb.toString()) != naive(sb.toString())) throw new AssertionError(sb.toString());
        }
    }

    static int lessonCodes(int[] codes) {
        Map<Integer, Integer> count = new HashMap<>();
        for (int code : codes) count.put(code, count.getOrDefault(code, 0) + 1);
        for (int i = 0; i < codes.length; i++) if (count.get(codes[i]) == 1) return i;
        return -1;
    }
}
```

#### Solution: [Vary] Valid Anagram (LeetCode 242)
<!-- id: hm-valid-anagram -->

**Approach.**
Two strings are anagrams exactly when every character has the same count in both. The method first returns false when the lengths differ, because equal counts imply equal lengths. It then adds one for each character of `s` and subtracts one for each character of `t` in a single map. A subtraction that brings an entry to 0 removes the entry, so the strings are anagrams exactly when the map is empty at the end. The invariant is that each entry equals the count in the processed part of `s` minus the count in the processed part of `t`, and no entry holds 0.

**Complexity.**
- **Time** is O(n + m) on average for lengths n and m, because each character causes one map update of expected constant time.
- **Space** is O(d) for d distinct characters.

```java run
import java.util.*;

public final class ValidAnagram {
    /**
     * Reports whether t is a rearrangement of s.
     * Time: O(n + m) expected. Space: O(d).
     * Invariant: each entry holds count in s minus count in t so far, and no entry holds 0.
     */
    static boolean isAnagram(String s, String t) {
        // Different lengths cannot give equal counts.
        if (s.length() != t.length()) return false;
        Map<Character, Integer> diff = new HashMap<>();
        // One update per character of s: the entry rises by one.
        for (int i = 0; i < s.length(); i++) {
            diff.merge(s.charAt(i), 1, Integer::sum);
        }
        // One update per character of t: the entry falls by one and disappears at 0.
        for (int i = 0; i < t.length(); i++) {
            char c = t.charAt(i);
            int now = diff.getOrDefault(c, 0) - 1;
            if (now == 0) diff.remove(c); else diff.put(c, now);
        }
        // An empty map means every count matched.
        return diff.isEmpty();
    }

    public static void main(String[] args) {
        // The statement examples and boundary lengths.
        if (!isAnagram("listen", "silent")) throw new AssertionError("example 1");
        if (isAnagram("aab", "abb")) throw new AssertionError("example 2");
        if (!isAnagram("", "") || isAnagram("a", "")) throw new AssertionError("empty");
        // Random strings are checked against a sort-based oracle.
        Random rnd = new Random(45);
        for (int k = 0; k < 600; k++) {
            String s = rand(rnd), t = rnd.nextBoolean() ? shuffle(s, rnd) : rand(rnd);
            char[] a = s.toCharArray(), b = t.toCharArray();
            Arrays.sort(a); Arrays.sort(b);
            if (isAnagram(s, t) != Arrays.equals(a, b)) throw new AssertionError(s + " " + t);
        }
    }

    static String rand(Random r) {
        StringBuilder sb = new StringBuilder();
        int len = r.nextInt(7);
        for (int i = 0; i < len; i++) sb.append((char) ('a' + r.nextInt(4)));
        return sb.toString();
    }

    static String shuffle(String s, Random r) {
        List<Character> l = new ArrayList<>();
        for (char c : s.toCharArray()) l.add(c);
        Collections.shuffle(l, r);
        StringBuilder sb = new StringBuilder();
        for (char c : l) sb.append(c);
        return sb.toString();
    }
}
```

#### Solution: [Boundary] Remove Zero Counts (Author exercise)
<!-- id: hm-remove-zero-counts -->

**Approach.**
Each pair changes one count. After the change, a count of 0 means the key is absent, so the method removes the entry at that moment. The invariant is that the map holds exactly the keys with a positive count, so `size()` equals the answer without a final scan. A map that kept zero entries would count a returned key as present, and `containsKey` would also disagree with the counts. The harness runs the zero-keeping variant on the second example to show the wrong size.

**Complexity.**
- **Time** is O(n) on average for n pairs, because each pair does one lookup and one update or removal of expected constant time.
- **Space** is O(d) for d distinct keys with a positive count at some moment.

```java run
import java.util.*;

public final class RemoveZeroCounts {
    /**
     * Applies signed count changes and returns the number of keys with a positive count.
     * Time: O(n) expected. Space: O(d).
     * Invariant: the map holds exactly the keys whose count is positive.
     */
    static int presentKeys(int[][] ops) {
        Map<Integer, Integer> count = new HashMap<>();
        // One iteration per pair, so n iterations.
        for (int[] op : ops) {
            int now = count.getOrDefault(op[0], 0) + op[1];
            // A count of 0 means absent, so the entry must go.
            if (now == 0) count.remove(op[0]); else count.put(op[0], now);
        }
        return count.size();
    }

    /** The mistake: zero entries stay in the map. */
    static int keepsZeros(int[][] ops) {
        Map<Integer, Integer> count = new HashMap<>();
        for (int[] op : ops) count.merge(op[0], op[1], Integer::sum);
        return count.size();
    }

    public static void main(String[] args) {
        // The statement examples.
        if (presentKeys(new int[][] {{3, 2}, {5, 1}, {3, -2}}) != 1) throw new AssertionError("example 1");
        if (presentKeys(new int[][] {{1, 4}, {1, -4}, {1, 4}}) != 1) throw new AssertionError("example 2");
        if (presentKeys(new int[0][]) != 0) throw new AssertionError("empty");
        // The variant that keeps zeros reports a larger size on the first example.
        if (keepsZeros(new int[][] {{3, 2}, {5, 1}, {3, -2}}) != 2) throw new AssertionError("zero entries inflate size");
        // Random valid sequences are checked against a full recount at the end.
        Random rnd = new Random(46);
        for (int t = 0; t < 500; t++) {
            int n = rnd.nextInt(12);
            int[] truth = new int[5];
            int[][] ops = new int[n][];
            for (int k = 0; k < n; k++) {
                int key = rnd.nextInt(5);
                int delta = rnd.nextInt(7) - 3;
                if (truth[key] + delta < 0) delta = -truth[key];
                truth[key] += delta;
                ops[k] = new int[] {key, delta};
            }
            int expect = 0;
            for (int v : truth) if (v > 0) expect++;
            if (presentKeys(ops) != expect) throw new AssertionError("trial " + t);
        }
    }
}
```

#### Solution: [Recognize] Unique Number Of Occurrences (LeetCode 1207)
<!-- id: hm-unique-occurrences -->

**Approach.**
A first map counts each value. The counts become the elements of a set, and the method adds them one by one with `add`. If `add` returns false, two distinct values share a count, so the answer is false. The loop over the map uses `values()`, because only the counts matter. The invariant is that the set holds the counts of the entries read so far, and all of them are different.

**Complexity.**
- **Time** is O(n) on average, because counting takes n updates and the second step reads at most n entries.
- **Space** is O(d) for d distinct values, since the map and the set each hold at most d items.

```java run
import java.util.*;

public final class UniqueOccurrences {
    /**
     * Reports whether all distinct values of arr occur a different number of times.
     * Time: O(n) expected. Space: O(d).
     * Invariant: seenCounts holds the counts of the entries read so far, all different.
     */
    static boolean uniqueOccurrences(int[] arr) {
        Map<Integer, Integer> count = new HashMap<>();
        // Counting pass: n updates.
        for (int x : arr) count.merge(x, 1, Integer::sum);
        Set<Integer> seenCounts = new HashSet<>();
        // Each count goes into a set; a repeated count fails at once.
        for (int c : count.values()) {
            if (!seenCounts.add(c)) return false;
        }
        return true;
    }

    public static void main(String[] args) {
        // The statement examples and a single value.
        if (!uniqueOccurrences(new int[] {4, 4, 9, 2, 9, 9})) throw new AssertionError("example 1");
        if (uniqueOccurrences(new int[] {1, 2})) throw new AssertionError("example 2");
        if (!uniqueOccurrences(new int[] {7})) throw new AssertionError("single");
        // Random arrays are checked against a quadratic oracle.
        Random rnd = new Random(47);
        for (int t = 0; t < 500; t++) {
            int[] a = new int[1 + rnd.nextInt(10)];
            for (int k = 0; k < a.length; k++) a[k] = rnd.nextInt(6) - 2;
            List<Integer> counts = new ArrayList<>();
            for (int i = 0; i < a.length; i++) {
                boolean first = true;
                int c = 0;
                for (int j = 0; j < a.length; j++) {
                    if (a[j] == a[i]) { c++; if (j < i) first = false; }
                }
                if (first) counts.add(c);
            }
            boolean expect = new HashSet<>(counts).size() == counts.size();
            if (uniqueOccurrences(a) != expect) throw new AssertionError(Arrays.toString(a));
        }
    }
}
```
