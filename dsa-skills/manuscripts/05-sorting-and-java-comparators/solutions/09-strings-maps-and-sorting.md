<!-- solutions-for: 05-strings-maps-and-sorting -->
### Strings, Maps, And Sorting

#### Solution: [Build] Valid Anagram (LeetCode 242)
<!-- id: so-valid-anagram-sorted -->

**Approach.** Reject immediately when the lengths differ, then copy both strings into character arrays, sort them, and compare the arrays by content. Sorting discards the arrangement and leaves only the multiset of characters, so equal sorted arrays mean equal tiles. The method uses no alphabet assumption, and the test draws characters from a mixed set including digits, punctuation and a non-ASCII character. The oracle compares counts held in a `HashMap`.

**Complexity.** O(n log n) time and O(n) extra space for the two arrays.

```java run
import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;
import java.util.Random;

public final class ValidAnagramSorted {
    static boolean areAnagrams(String s, String t) {
        if (s.length() != t.length()) return false;
        char[] x = s.toCharArray(), y = t.toCharArray();
        Arrays.sort(x);
        Arrays.sort(y);
        return Arrays.equals(x, y);
    }
    static boolean oracle(String s, String t) {
        Map<Character, Integer> m = new HashMap<>();
        for (char c : s.toCharArray()) m.merge(c, 1, Integer::sum);
        for (char c : t.toCharArray()) m.merge(c, -1, Integer::sum);
        for (int v : m.values()) if (v != 0) return false;
        return true;
    }

    public static void main(String[] args) {
        if (!areAnagrams("listen", "silent")) throw new AssertionError("example 1");
        if (areAnagrams("aab", "abb")) throw new AssertionError("example 2");
        if (areAnagrams("ab", "abc")) throw new AssertionError("different lengths");
        if (!areAnagrams("a1!é", "é!1a")) throw new AssertionError("no alphabet assumption");
        Random rnd = new Random(581);
        String alphabet = "abcA1!é";
        for (int t = 0; t < 5000; t++) {
            StringBuilder a = new StringBuilder(), b = new StringBuilder();
            int n = 1 + rnd.nextInt(8);
            for (int i = 0; i < n; i++) a.append(alphabet.charAt(rnd.nextInt(alphabet.length())));
            if (rnd.nextBoolean()) {
                char[] c = a.toString().toCharArray();
                for (int i = c.length - 1; i > 0; i--) { int j = rnd.nextInt(i + 1); char tmp = c[i]; c[i] = c[j]; c[j] = tmp; }
                b.append(c);
                if (rnd.nextInt(3) == 0) b.setCharAt(0, alphabet.charAt(rnd.nextInt(alphabet.length())));
            } else {
                int m = 1 + rnd.nextInt(8);
                for (int i = 0; i < m; i++) b.append(alphabet.charAt(rnd.nextInt(alphabet.length())));
            }
            if (areAnagrams(a.toString(), b.toString()) != oracle(a.toString(), b.toString())) throw new AssertionError("differs on " + a + " and " + b);
        }
    }
}
```

#### Solution: [Vary] Group Anagrams (LeetCode 49)
<!-- id: so-group-anagrams-sorted -->

**Approach.** For each word, sort its characters, turn the result into a `String`, and use it as the key in a `LinkedHashMap` from keys to lists. The linked map keeps keys in order of first appearance, and each list receives words in input order, so the output is deterministic. A `char[]` key would be compared by identity and every word would form its own group, so the conversion to `String` is essential. The oracle never builds a key: it keeps the groups in a list and decides membership of a word by comparing letter counts against the first word of each group.

**Complexity.** O(n L log L) time for n words of length at most L, and O(n L) space.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Random;

public final class GroupAnagramsSorted {
    static List<List<String>> group(String[] words) {
        Map<String, List<String>> piles = new LinkedHashMap<>();
        for (String w : words) {
            char[] letters = w.toCharArray();
            Arrays.sort(letters);
            piles.computeIfAbsent(new String(letters), k -> new ArrayList<>()).add(w);
        }
        return new ArrayList<>(piles.values());
    }
    static boolean sameCounts(String a, String b) {
        int[] c = new int[128];
        for (char ch : a.toCharArray()) c[ch]++;
        for (char ch : b.toCharArray()) c[ch]--;
        for (int v : c) if (v != 0) return false;
        return true;
    }
    static List<List<String>> oracle(String[] words) {
        List<List<String>> groups = new ArrayList<>();
        for (String w : words) {
            boolean placed = false;
            for (List<String> g : groups) if (sameCounts(g.get(0), w)) { g.add(w); placed = true; break; }
            if (!placed) { List<String> g = new ArrayList<>(); g.add(w); groups.add(g); }
        }
        return groups;
    }

    public static void main(String[] args) {
        List<List<String>> ex1 = group(new String[] {"stop", "pots", "opts", "cat", "act", "dog", "tops"});
        if (!ex1.equals(List.of(List.of("stop", "pots", "opts", "tops"), List.of("cat", "act"), List.of("dog")))) throw new AssertionError("example 1");
        if (!group(new String[] {""}).equals(List.of(List.of("")))) throw new AssertionError("example 2");
        if (group(new String[] {"ab", "ab"}).size() != 1) throw new AssertionError("repeated words share a group");
        Random rnd = new Random(582);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(9);
            String[] words = new String[n];
            for (int i = 0; i < n; i++) {
                StringBuilder sb = new StringBuilder();
                int len = rnd.nextInt(4);
                for (int j = 0; j < len; j++) sb.append("abc".charAt(rnd.nextInt(3)));
                words[i] = sb.toString();
            }
            if (!group(words).equals(oracle(words))) throw new AssertionError("differs from the count oracle on " + Arrays.toString(words));
        }
    }
}
```

#### Solution: [Boundary] Sort Characters by Frequency (LeetCode 451)
<!-- id: so-sort-characters-by-frequency -->

**Approach.** Count each character in a `HashMap`, put the distinct characters in a list, and order that list by count descending with the smaller character code first on equal counts. Then write each character as many times as its count. The canonical sorted form would put every character in code order, ignoring counts, so it cannot be the output; it only tells which characters are present. The oracle repeatedly takes the remaining character with the highest count, preferring the smaller code, using plain arrays.

**Complexity.** O(n + d log d) time for n characters of which d are distinct, and O(n) space for the output.

```java run
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Random;

public final class SortCharactersByFrequency {
    static String sortByFrequency(String s) {
        Map<Character, Integer> count = new HashMap<>();
        for (char c : s.toCharArray()) count.merge(c, 1, Integer::sum);
        List<Character> keys = new ArrayList<>(count.keySet());
        keys.sort((a, b) -> count.get(a).equals(count.get(b)) ? Character.compare(a, b) : Integer.compare(count.get(b), count.get(a)));
        StringBuilder out = new StringBuilder();
        for (char c : keys) for (int i = 0; i < count.get(c); i++) out.append(c);
        return out.toString();
    }
    static String oracle(String s) {
        int[] c = new int[128];
        for (char ch : s.toCharArray()) c[ch]++;
        StringBuilder out = new StringBuilder();
        while (true) {
            int best = -1;
            for (int ch = 0; ch < 128; ch++) if (c[ch] > 0 && (best == -1 || c[ch] > c[best])) best = ch;
            if (best == -1) break;
            for (int i = 0; i < c[best]; i++) out.append((char) best);
            c[best] = 0;
        }
        return out.toString();
    }

    public static void main(String[] args) {
        if (!sortByFrequency("tree").equals("eert")) throw new AssertionError("example 1");
        if (!sortByFrequency("Aabb").equals("bbAa")) throw new AssertionError("example 2");
        if (!sortByFrequency("z").equals("z")) throw new AssertionError("single character");
        Random rnd = new Random(583);
        String alphabet = "abAB019";
        for (int t = 0; t < 4000; t++) {
            StringBuilder sb = new StringBuilder();
            int n = 1 + rnd.nextInt(14);
            for (int i = 0; i < n; i++) sb.append(alphabet.charAt(rnd.nextInt(alphabet.length())));
            String s = sb.toString();
            String got = sortByFrequency(s);
            if (!got.equals(oracle(s))) throw new AssertionError("differs from the oracle on " + s);
            if (got.length() != s.length()) throw new AssertionError("length changed");
        }
    }
}
```

#### Solution: [Recognize] Determine if Two Strings Are Close (LeetCode 1657)
<!-- id: so-two-strings-close -->

**Approach.** Swapping positions can rearrange the characters freely, so arrangement is irrelevant. Exchanging two letters everywhere can move a count from one letter to another, but only between letters that already occur, so the set of letters is unchanged and the multiset of counts is unchanged. Hence two strings are close exactly when they have equal length, the same set of characters, and equal sorted lists of counts. A raw sorted string fails here: `abbccc` and `cabbba` have different sorted strings but are close. The oracle searches the space of strings reachable by both operations, on tiny strings over three letters, and the two answers must agree on every pair.

**Complexity.** O(n) time for counting plus O(d log d) for d distinct letters, with O(d) space.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;

public final class TwoStringsClose {
    static boolean isClose(String a, String b) {
        if (a.length() != b.length()) return false;
        Map<Character, Integer> ca = new HashMap<>(), cb = new HashMap<>();
        for (char c : a.toCharArray()) ca.merge(c, 1, Integer::sum);
        for (char c : b.toCharArray()) cb.merge(c, 1, Integer::sum);
        if (!ca.keySet().equals(cb.keySet())) return false;
        List<Integer> fa = new ArrayList<>(ca.values()), fb = new ArrayList<>(cb.values());
        Collections.sort(fa);
        Collections.sort(fb);
        return fa.equals(fb);
    }
    static boolean reachable(String from, String to) {
        Set<String> seen = new HashSet<>();
        ArrayDeque<String> queue = new ArrayDeque<>();
        seen.add(from);
        queue.add(from);
        while (!queue.isEmpty()) {
            String cur = queue.poll();
            if (cur.equals(to)) return true;
            List<String> next = new ArrayList<>();
            char[] c = cur.toCharArray();
            for (int i = 0; i < c.length; i++) for (int j = i + 1; j < c.length; j++) {
                char[] d = c.clone();
                char t = d[i]; d[i] = d[j]; d[j] = t;
                next.add(new String(d));
            }
            for (char x = 'a'; x <= 'c'; x++) for (char y = (char) (x + 1); y <= 'c'; y++) {
                if (cur.indexOf(x) < 0 || cur.indexOf(y) < 0) continue;
                StringBuilder sb = new StringBuilder();
                for (char ch : c) sb.append(ch == x ? y : ch == y ? x : ch);
                next.add(sb.toString());
            }
            for (String n : next) if (seen.add(n)) queue.add(n);
        }
        return false;
    }
    static void all(int len, String prefix, List<String> out) {
        if (prefix.length() == len) { out.add(prefix); return; }
        for (char c = 'a'; c <= 'c'; c++) all(len, prefix + c, out);
    }

    public static void main(String[] args) {
        if (!isClose("cabbba", "abbccc")) throw new AssertionError("example 1");
        if (isClose("aabbc", "abbcd")) throw new AssertionError("example 2");
        char[] x = "cabbba".toCharArray(), y = "abbccc".toCharArray();
        java.util.Arrays.sort(x);
        java.util.Arrays.sort(y);
        if (java.util.Arrays.equals(x, y)) throw new AssertionError("the raw sorted strings differ for close strings");
        for (int len = 1; len <= 5; len++) {
            List<String> words = new ArrayList<>();
            all(len, "", words);
            for (String a : words) for (String b : words) {
                if (isClose(a, b) != reachable(a, b)) throw new AssertionError("differs from the search oracle on " + a + " and " + b);
            }
        }
    }
}
```
