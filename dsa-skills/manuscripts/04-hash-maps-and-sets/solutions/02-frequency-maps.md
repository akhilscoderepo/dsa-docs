<!-- solutions-for: 02-frequency-maps -->
### Frequency Maps

#### Solution: [Build] First Unique Character in a String (LeetCode 387)
<!-- id: hm-first-unique-char -->

**Approach.** The first pass builds a ledger with `merge`, which treats an absent key as zero. The second pass walks the string in its original order and returns the first index whose character has count 1. Because every character of the string is a key by then, the lookup never returns `null`. The oracle for each index counts the matching characters with a nested loop, and the assertions require equal answers on random strings over a small alphabet, plus the examples and the boxed-comparison hazard the lesson mentions.

**Complexity.** Expected O(n) time and O(k) extra space for `k` distinct characters.

```java run
import java.util.HashMap;
import java.util.Map;
import java.util.Random;

public final class FirstUniqueChar {
    static int firstUnique(String s) {
        Map<Character, Integer> count = new HashMap<>();
        for (char c : s.toCharArray()) count.merge(c, 1, Integer::sum);
        for (int i = 0; i < s.length(); i++) {
            if (count.get(s.charAt(i)) == 1) return i;
        }
        return -1;
    }
    static int oracle(String s) {
        for (int i = 0; i < s.length(); i++) {
            int times = 0;
            for (int j = 0; j < s.length(); j++) if (s.charAt(j) == s.charAt(i)) times++;
            if (times == 1) return i;
        }
        return -1;
    }

    public static void main(String[] args) {
        if (firstUnique("swiss") != 1) throw new AssertionError("example 1");
        if (firstUnique("abab") != -1) throw new AssertionError("example 2");
        if (firstUnique("z") != 0) throw new AssertionError("single character");
        Map<Character, Integer> m = new HashMap<>();
        if (m.get('q') != null) throw new AssertionError("a missing key returns null");
        if (Integer.valueOf(1000) == Integer.valueOf(1000)) throw new AssertionError("boxed values above 127 are distinct objects");
        if (!Integer.valueOf(1000).equals(Integer.valueOf(1000))) throw new AssertionError("equals compares values");
        Random rnd = new Random(44);
        for (int t = 0; t < 4000; t++) {
            StringBuilder sb = new StringBuilder();
            int n = 1 + rnd.nextInt(12);
            for (int i = 0; i < n; i++) sb.append((char) ('a' + rnd.nextInt(5)));
            String s = sb.toString();
            if (firstUnique(s) != oracle(s)) throw new AssertionError("disagrees with the recount on " + s);
        }
    }
}
```

#### Solution: [Vary] Valid Anagram (LeetCode 242)
<!-- id: hm-valid-anagram -->

**Approach.** Build one ledger per string and compare them with `Map.equals`, which checks that the key sets and every count agree and ignores insertion order. A set of letters would call `aab` and `abb` equal, so the counts are what carry the answer. Strings of different lengths cannot be anagrams, and the map comparison already rejects them, but the length check is cheaper and runs first. The oracle sorts both character arrays and compares them, and the assertions require agreement on random strings.

**Complexity.** Expected O(n + m) time and O(k) extra space.

```java run
import java.util.Arrays;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Random;
import java.util.Set;

public final class ValidAnagram {
    static Map<Character, Integer> counts(String s) {
        Map<Character, Integer> count = new HashMap<>();
        for (char c : s.toCharArray()) count.merge(c, 1, Integer::sum);
        return count;
    }
    static boolean isAnagram(String s, String t) {
        if (s.length() != t.length()) return false;
        return counts(s).equals(counts(t));
    }
    static boolean oracle(String s, String t) {
        char[] a = s.toCharArray(), b = t.toCharArray();
        Arrays.sort(a);
        Arrays.sort(b);
        return Arrays.equals(a, b);
    }
    static Set<Character> letters(String s) {
        Set<Character> set = new HashSet<>();
        for (char c : s.toCharArray()) set.add(c);
        return set;
    }

    public static void main(String[] args) {
        if (!isAnagram("stone", "notes")) throw new AssertionError("example 1");
        if (isAnagram("aab", "abb")) throw new AssertionError("example 2");
        if (!letters("aab").equals(letters("abb"))) throw new AssertionError("the letter sets of the two examples are equal, so a set cannot decide");
        if (!isAnagram("", "")) throw new AssertionError("empty strings");
        Random rnd = new Random(45);
        for (int t = 0; t < 4000; t++) {
            StringBuilder x = new StringBuilder(), y = new StringBuilder();
            int n = rnd.nextInt(8), m = rnd.nextInt(8);
            for (int i = 0; i < n; i++) x.append((char) ('a' + rnd.nextInt(3)));
            for (int i = 0; i < m; i++) y.append((char) ('a' + rnd.nextInt(3)));
            if (isAnagram(x.toString(), y.toString()) != oracle(x.toString(), y.toString())) throw new AssertionError("disagrees with the sort oracle");
        }
    }
}
```

#### Solution: [Boundary] Remove Zero Counts (Author exercise)
<!-- id: hm-remove-zero-counts -->

**Approach.** Parse each operation into a sign and a name. An addition uses `merge` to start at 1 or add one. A removal first checks that the key is present, ignores it if not, and otherwise either deletes the key when its count is 1 or decrements it. Deleting at zero keeps the invariant that a key is in the map exactly when its count is positive, so the answer is the map size. The assertions run a leaky variant that keeps zero entries and show that its `containsKey` lies, then compare the correct method with a brute-force simulation on an `int` array of counts over random operation lists.

**Complexity.** Expected O(m) time for `m` operations and O(k) extra space for `k` distinct items.

```java run
import java.util.HashMap;
import java.util.Map;
import java.util.Random;

public final class RemoveZeroCounts {
    static int positiveItems(String[] ops) {
        Map<String, Integer> ledger = new HashMap<>();
        for (String op : ops) {
            String name = op.substring(1);
            if (op.charAt(0) == '+') {
                ledger.merge(name, 1, Integer::sum);
            } else {
                Integer now = ledger.get(name);
                if (now == null) continue;
                if (now == 1) ledger.remove(name);
                else ledger.put(name, now - 1);
            }
        }
        return ledger.size();
    }
    static Map<String, Integer> leaky(String[] ops) {
        Map<String, Integer> ledger = new HashMap<>();
        for (String op : ops) {
            String name = op.substring(1);
            if (op.charAt(0) == '+') ledger.merge(name, 1, Integer::sum);
            else if (ledger.containsKey(name) && ledger.get(name) > 0) ledger.merge(name, -1, Integer::sum);
        }
        return ledger;
    }
    static int oracle(String[] ops) {
        int[] c = new int[4];
        for (String op : ops) {
            int k = op.charAt(1) - 'a';
            if (op.charAt(0) == '+') c[k]++;
            else if (c[k] > 0) c[k]--;
        }
        int n = 0;
        for (int v : c) if (v > 0) n++;
        return n;
    }

    public static void main(String[] args) {
        if (positiveItems(new String[] {"+a", "+b", "+a", "-a", "-b"}) != 1) throw new AssertionError("example 1");
        if (positiveItems(new String[] {"-z", "+z", "-z"}) != 0) throw new AssertionError("example 2");
        Map<String, Integer> l = leaky(new String[] {"+b", "-b"});
        if (!l.containsKey("b") || l.get("b") != 0) throw new AssertionError("the leaky ledger keeps b with count zero");
        if (positiveItems(new String[] {"+b", "-b"}) != 0) throw new AssertionError("the correct ledger forgets b");
        Random rnd = new Random(46);
        for (int t = 0; t < 4000; t++) {
            String[] ops = new String[rnd.nextInt(12)];
            for (int i = 0; i < ops.length; i++) ops[i] = (rnd.nextBoolean() ? "+" : "-") + (char) ('a' + rnd.nextInt(4));
            if (positiveItems(ops) != oracle(ops)) throw new AssertionError("disagrees with the array simulation");
        }
    }
}
```

#### Solution: [Recognize] Unique Number of Occurrences (LeetCode 1207)
<!-- id: hm-unique-occurrences -->

**Approach.** Count each value in a map, then loop over `entrySet()` and add each count to a set. A failed `add` means two values share a count, so the answer is false. If the loop finishes, all counts are different. Equivalently, the set of counts has the same size as the map. The oracle compares every pair of values with a direct count by scanning the array, and the assertions require the same verdict on random arrays.

**Complexity.** Expected O(n) time and O(k) extra space for `k` distinct values.

```java run
import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Random;
import java.util.Set;

public final class UniqueOccurrences {
    static boolean uniqueOccurrences(int[] arr) {
        Map<Integer, Integer> count = new HashMap<>();
        for (int v : arr) count.merge(v, 1, Integer::sum);
        Set<Integer> counts = new HashSet<>();
        for (Map.Entry<Integer, Integer> e : count.entrySet()) {
            if (!counts.add(e.getValue())) return false;
        }
        return true;
    }
    static int times(int[] arr, int v) { int c = 0; for (int x : arr) if (x == v) c++; return c; }
    static boolean oracle(int[] arr) {
        for (int a : arr)
            for (int b : arr)
                if (a != b && times(arr, a) == times(arr, b)) return false;
        return true;
    }

    public static void main(String[] args) {
        if (!uniqueOccurrences(new int[] {3, 3, 5, 5, 5, 1})) throw new AssertionError("example 1");
        if (uniqueOccurrences(new int[] {7, 7, 8, 8})) throw new AssertionError("example 2");
        if (!uniqueOccurrences(new int[] {4})) throw new AssertionError("a single value is trivially unique");
        Random rnd = new Random(47);
        for (int t = 0; t < 4000; t++) {
            int[] x = new int[1 + rnd.nextInt(12)];
            for (int i = 0; i < x.length; i++) x[i] = rnd.nextInt(5) - 2;
            if (uniqueOccurrences(x) != oracle(x)) throw new AssertionError("disagrees with the pair check");
        }
    }
}
```
