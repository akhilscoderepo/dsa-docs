<!-- solutions-for: 07-direct-addressing -->
### Direct Addressing

#### Solution: [Build] Lowercase Character Counts (Author exercise)
<!-- id: hm-lowercase-counts -->

**Approach.** Allocate 26 slots and, for each character, check that it lies between `'a'` and `'z'` before computing the slot `c - 'a'`. A character outside the range is rejected with an `IllegalArgumentException` and no slot is touched for it. Without the check, `'1' - 'a'` is negative and would throw an unrelated index exception, while an uppercase letter would do the same. The assertions compare the table with a map version on random lowercase strings, confirm that rejections happen, and show that a `char` outside the basic plane occupies two `char` values, which is why the contract matters.

**Complexity.** O(n) time and O(1) extra space, since the table has a fixed 26 slots.

```java run
import java.util.HashMap;
import java.util.Map;
import java.util.Random;

public final class LowercaseCounts {
    static int[] lowercaseCounts(String s) {
        int[] count = new int[26];
        for (char c : s.toCharArray()) {
            if (c < 'a' || c > 'z') throw new IllegalArgumentException("outside the contract: " + c);
            count[c - 'a']++;
        }
        return count;
    }
    static Map<Character, Integer> viaMap(String s) {
        Map<Character, Integer> count = new HashMap<>();
        for (char c : s.toCharArray()) count.merge(c, 1, Integer::sum);
        return count;
    }

    public static void main(String[] args) {
        int[] b = lowercaseCounts("banana");
        if (b[0] != 3 || b[1] != 1 || b[13] != 2) throw new AssertionError("example 1");
        int total = 0;
        for (int v : b) total += v;
        if (total != 6) throw new AssertionError("counts sum to the length");
        boolean rejected = false;
        try { lowercaseCounts("ab1"); } catch (IllegalArgumentException e) { rejected = true; }
        if (!rejected) throw new AssertionError("example 2");
        if ('1' - 'a' >= 0) throw new AssertionError("a digit would index a negative slot");
        if ("😀".length() != 2) throw new AssertionError("a supplementary character is two char values");
        Random rnd = new Random(101);
        for (int t = 0; t < 3000; t++) {
            StringBuilder sb = new StringBuilder();
            int n = rnd.nextInt(20);
            for (int i = 0; i < n; i++) sb.append((char) ('a' + rnd.nextInt(26)));
            String s = sb.toString();
            int[] table = lowercaseCounts(s);
            Map<Character, Integer> map = viaMap(s);
            for (int k = 0; k < 26; k++)
                if (table[k] != map.getOrDefault((char) ('a' + k), 0)) throw new AssertionError("table and map disagree for " + (char) ('a' + k));
        }
    }
}
```

#### Solution: [Vary] Valid Anagram (LeetCode 242)
<!-- id: hm-anagram-array -->

**Approach.** Use one table of 26 balances. For each position, add one to the slot of the first string's character and subtract one from the slot of the second string's character. The strings are anagrams exactly when every slot ends at zero, because each slot then holds the difference between the two counts. Different lengths are rejected first. The assertions check the examples, including the slots that end at 1 and -1 for the second example, and compare the result with a sort-based oracle on random strings.

**Complexity.** O(n) time and O(1) extra space.

```java run
import java.util.Arrays;
import java.util.Random;

public final class AnagramArray {
    static int[] balance(String s, String t) {
        int[] b = new int[26];
        for (int i = 0; i < s.length(); i++) {
            b[s.charAt(i) - 'a']++;
            b[t.charAt(i) - 'a']--;
        }
        return b;
    }
    static boolean isAnagram(String s, String t) {
        if (s.length() != t.length()) return false;
        for (int v : balance(s, t)) if (v != 0) return false;
        return true;
    }
    static boolean oracle(String s, String t) {
        char[] a = s.toCharArray(), b = t.toCharArray();
        Arrays.sort(a);
        Arrays.sort(b);
        return Arrays.equals(a, b);
    }

    public static void main(String[] args) {
        if (!isAnagram("triangle", "integral")) throw new AssertionError("example 1");
        if (isAnagram("aabc", "abcc")) throw new AssertionError("example 2");
        int[] b = balance("aabc", "abcc");
        if (b[0] != 1 || b[2] != -1) throw new AssertionError("slots a and c end at 1 and -1");
        if (isAnagram("ab", "abc")) throw new AssertionError("different lengths");
        Random rnd = new Random(102);
        for (int t = 0; t < 4000; t++) {
            StringBuilder x = new StringBuilder(), y = new StringBuilder();
            int n = rnd.nextInt(8);
            for (int i = 0; i < n; i++) x.append((char) ('a' + rnd.nextInt(3)));
            int m = rnd.nextInt(4) == 0 ? rnd.nextInt(8) : n;
            for (int i = 0; i < m; i++) y.append((char) ('a' + rnd.nextInt(3)));
            if (isAnagram(x.toString(), y.toString()) != oracle(x.toString(), y.toString())) throw new AssertionError("disagrees with the sort oracle");
        }
    }
}
```

#### Solution: [Boundary] Sparse IDs (Author exercise)
<!-- id: hm-sparse-ids -->

**Approach.** Compute the minimum and maximum identifier and the span `max - min + 1` as a `long`. If the span is at most `4 * n + 64`, allocate a table of that many slots and index it with `id - min`. Otherwise use a hash map, which stores only the identifiers that occur. Both paths maintain the same invariant, so the answer is the same, and memory is proportional to the input size either way. The assertions run the examples through the intended paths, compare both paths against each other on random data, and check the oracle on identifiers near a billion where a table would be unaffordable.

**Complexity.** Expected O(n) time and O(n) extra space in both branches.

```java run
import java.util.HashMap;
import java.util.Map;
import java.util.Random;

public final class SparseIds {
    static boolean lastUsedTable;

    static int mostCommonId(int[] ids) {
        if (ids.length == 0) return 0;
        int lo = Integer.MAX_VALUE, hi = Integer.MIN_VALUE;
        for (int id : ids) { lo = Math.min(lo, id); hi = Math.max(hi, id); }
        long span = (long) hi - lo + 1;
        int best = 0;
        if (span <= 4L * ids.length + 64) {
            lastUsedTable = true;
            int[] count = new int[(int) span];
            for (int id : ids) best = Math.max(best, ++count[id - lo]);
        } else {
            lastUsedTable = false;
            Map<Integer, Integer> count = new HashMap<>();
            for (int id : ids) best = Math.max(best, count.merge(id, 1, Integer::sum));
        }
        return best;
    }
    static int oracle(int[] ids) {
        int best = 0;
        for (int a : ids) {
            int c = 0;
            for (int b : ids) if (a == b) c++;
            best = Math.max(best, c);
        }
        return best;
    }

    public static void main(String[] args) {
        if (mostCommonId(new int[] {2, 1_000_000_000, 2}) != 2 || lastUsedTable) throw new AssertionError("example 1 must use the map");
        if (mostCommonId(new int[] {5, 6, 7, 5, 6, 5}) != 3 || !lastUsedTable) throw new AssertionError("example 2 must use the table");
        if (mostCommonId(new int[] {}) != 0) throw new AssertionError("empty input");
        Random rnd = new Random(103);
        for (int t = 0; t < 3000; t++) {
            int[] x = new int[rnd.nextInt(14)];
            int base = rnd.nextBoolean() ? 0 : 999_999_900;
            int spread = rnd.nextBoolean() ? 10 : 1_000_000_000 - base;
            for (int i = 0; i < x.length; i++) x[i] = base + rnd.nextInt(spread);
            if (mostCommonId(x) != oracle(x)) throw new AssertionError("disagrees with the pair count");
        }
    }
}
```

#### Solution: [Recognize] Design HashMap (LeetCode 706)
<!-- id: hm-design-hashmap -->

**Approach.** Keep an array of 769 buckets, each a singly linked list of key and value nodes. A key is mapped to a bucket by `Math.floorMod(key, 769)`, which is never negative even for negative keys, and a prime size spreads common patterns. `put` walks the bucket and replaces the value if the key is present, otherwise it adds a node at the front. `get` walks the bucket and returns -1 when the key is absent. `remove` unlinks the node. A table with one slot for each `int` would need 2^32 slots, which the assertions compute. They also run random operations against `java.util.HashMap` as an oracle and compare every `get`.

**Complexity.** Expected O(1) per operation for well-spread keys, and O(n) in the worst case if every key lands in one bucket, with O(n + buckets) space.

```java run
import java.util.HashMap;
import java.util.Map;
import java.util.Random;

public final class DesignHashMap {
    static final class MyHashMap {
        private static final int SIZE = 769;
        private static final class Node {
            final int key; int value; Node next;
            Node(int key, int value, Node next) { this.key = key; this.value = value; this.next = next; }
        }
        private final Node[] buckets = new Node[SIZE];

        private int slot(int key) { return Math.floorMod(key, SIZE); }

        void put(int key, int value) {
            int s = slot(key);
            for (Node n = buckets[s]; n != null; n = n.next) {
                if (n.key == key) { n.value = value; return; }
            }
            buckets[s] = new Node(key, value, buckets[s]);
        }
        int get(int key) {
            for (Node n = buckets[slot(key)]; n != null; n = n.next) {
                if (n.key == key) return n.value;
            }
            return -1;
        }
        void remove(int key) {
            int s = slot(key);
            Node prev = null;
            for (Node n = buckets[s]; n != null; prev = n, n = n.next) {
                if (n.key == key) {
                    if (prev == null) buckets[s] = n.next; else prev.next = n.next;
                    return;
                }
            }
        }
    }

    public static void main(String[] args) {
        MyHashMap m = new MyHashMap();
        m.put(7, 70);
        m.put(-3, 30);
        if (m.get(7) != 70 || m.get(5) != -1) throw new AssertionError("example 1");
        MyHashMap n = new MyHashMap();
        n.put(7, 70);
        n.put(7, 71);
        if (n.get(7) != 71) throw new AssertionError("the second put replaces");
        n.remove(7);
        if (n.get(7) != -1) throw new AssertionError("example 2");
        if (((long) Integer.MAX_VALUE - Integer.MIN_VALUE + 1) != (1L << 32)) throw new AssertionError("one slot per int needs 2^32 slots");
        MyHashMap c = new MyHashMap();
        c.put(1, 10);
        c.put(1 + 769, 20);
        c.put(1 - 769, 30);
        if (c.get(1) != 10 || c.get(770) != 20 || c.get(-768) != 30) throw new AssertionError("colliding keys stay apart");
        c.remove(770);
        if (c.get(1) != 10 || c.get(770) != -1 || c.get(-768) != 30) throw new AssertionError("removing one colliding key leaves the others");
        Random rnd = new Random(104);
        for (int t = 0; t < 300; t++) {
            MyHashMap mine = new MyHashMap();
            Map<Integer, Integer> real = new HashMap<>();
            for (int op = 0; op < 200; op++) {
                int key = rnd.nextInt(5) == 0 ? rnd.nextInt() : rnd.nextInt(40) - 20;
                int kind = rnd.nextInt(3);
                if (kind == 0) { int v = rnd.nextInt(1000); mine.put(key, v); real.put(key, v); }
                else if (kind == 1) { mine.remove(key); real.remove(key); }
                if (mine.get(key) != real.getOrDefault(key, -1)) throw new AssertionError("disagrees with HashMap");
            }
        }
    }
}
```
