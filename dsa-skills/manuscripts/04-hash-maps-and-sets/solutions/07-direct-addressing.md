<!-- solutions-for: 04-hash-maps-and-sets -->
### Solutions For Arrays Versus Maps

#### Solution: [Build] Words Containing Each Letter (Author exercise)
<!-- id: hm-words-per-letter -->

**Approach.**
The alphabet is the 26 lowercase letters, so the table has 26 slots and the index is `c - 'a'`. A letter must count once per word, so the method needs to know whether the current word has already counted that letter. A second array `lastWord` stores, for each letter, the index of the last word that counted it, starting at -1. A letter increments its table slot only when `lastWord[slot]` differs from the current word index, and then records the word index. This avoids clearing a marker array for every word. The invariant is that after word `w`, `table[k]` equals the number of words among `0..w` that contain the letter `'a' + k`. The harness also asserts the failures from the lesson: an out-of-range character, an interval that wraps in `int`, and a huge array request.

**Complexity.**
- **Time** is O(L), where L is the total number of letters over all words, because each letter does constant work.
- **Space** is O(1), because the two arrays hold 26 entries each, whatever the input.

```java run
import java.util.*;

public final class WordsPerLetter {
    /**
     * Counts, for each letter, the words that contain it at least once.
     * Time: O(L) for L total letters. Space: O(1), two 26-entry arrays.
     * Invariant: after word w, table[k] is the number of words in 0..w that contain letter 'a' + k.
     */
    static int[] wordsPerLetter(String[] words) {
        int[] table = new int[26];
        int[] lastWord = new int[26];
        Arrays.fill(lastWord, -1);
        // One pass over the words.
        for (int w = 0; w < words.length; w++) {
            // One pass over the letters of the word.
            for (int i = 0; i < words[w].length(); i++) {
                int slot = words[w].charAt(i) - 'a';
                // The letter counts for this word only the first time it appears in the word.
                if (lastWord[slot] != w) {
                    lastWord[slot] = w;
                    table[slot]++;
                }
            }
        }
        return table;
    }

    public static void main(String[] args) {
        // The statement examples.
        int[] want = new int[26];
        want['m' - 'a'] = 2; want['n' - 'a'] = 2; want['o' - 'a'] = 3;
        if (!Arrays.equals(wordsPerLetter(new String[] {"moon", "mom", "no"}), want)) throw new AssertionError("example 1");
        if (!Arrays.equals(wordsPerLetter(new String[] {""}), new int[26])) throw new AssertionError("example 2");
        if (!Arrays.equals(wordsPerLetter(new String[0]), new int[26])) throw new AssertionError("no words");
        // Failures from the lesson: a character outside the alphabet, a wrapped range and a huge request.
        boolean threw = false;
        try { wordsPerLetter(new String[] {"a1"}); } catch (ArrayIndexOutOfBoundsException e) { threw = true; }
        if (!threw) throw new AssertionError("character outside the alphabet");
        if (Integer.MAX_VALUE - Integer.MIN_VALUE + 1 != 0) throw new AssertionError("full range wraps to 0");
        int wrapped = 2_000_000_000 - (-2_000_000_000) + 1;
        threw = false;
        try { int[] bad = new int[wrapped]; } catch (NegativeArraySizeException e) { threw = true; }
        if (!threw) throw new AssertionError("negative size");
        threw = false;
        try { int[] huge = new int[Integer.MAX_VALUE]; } catch (OutOfMemoryError e) { threw = true; }
        if (!threw) throw new AssertionError("huge array request");
        // Random words are checked against a set-based oracle.
        Random rnd = new Random(63);
        for (int t = 0; t < 500; t++) {
            String[] ws = new String[rnd.nextInt(6)];
            for (int k = 0; k < ws.length; k++) {
                StringBuilder sb = new StringBuilder();
                int len = rnd.nextInt(6);
                for (int j = 0; j < len; j++) sb.append((char) ('a' + rnd.nextInt(4)));
                ws[k] = sb.toString();
            }
            int[] expect = new int[26];
            for (String w : ws) {
                Set<Character> s = new HashSet<>();
                for (char c : w.toCharArray()) s.add(c);
                for (char c : s) expect[c - 'a']++;
            }
            if (!Arrays.equals(wordsPerLetter(ws), expect)) throw new AssertionError(Arrays.toString(ws));
        }
    }
}
```

#### Solution: [Vary] Anagram Over ASCII (Author exercise)
<!-- id: hm-anagram-ascii -->

**Approach.**
The statement bounds every code below 128, so a table of 128 counters covers the alphabet and the character code is the index. The method returns false for different lengths, adds one for each character of `s`, subtracts one for each character of `t`, and returns false at the first count below 0. Because the lengths are equal, no negative count means that all counts are 0 at the end. The invariant is that `table[c]` equals the occurrences of `c` in the processed part of `s` minus those in the processed part of `t`. Case matters, because `b` and `B` have different codes.

**Complexity.**
- **Time** is O(n + m) for the lengths n and m, with no hashing and no boxing.
- **Space** is O(1), because the table has 128 entries.

```java run
import java.util.*;

public final class AnagramAscii {
    /**
     * Reports whether t is a rearrangement of s, for strings of ASCII characters.
     * Time: O(n + m). Space: O(1), a 128-entry table.
     * Invariant: table[c] is the count of c in the processed part of s minus its count in the processed part of t.
     */
    static boolean isAnagram(String s, String t) {
        // Different lengths cannot give equal counts.
        if (s.length() != t.length()) return false;
        int[] table = new int[128];
        // The character code is the index, which direct addressing allows under the ASCII contract.
        for (int i = 0; i < s.length(); i++) table[s.charAt(i)]++;
        for (int i = 0; i < t.length(); i++) {
            // A count below 0 means t holds a character more often than s does.
            if (--table[t.charAt(i)] < 0) return false;
        }
        // Equal lengths and no negative count force every count to be 0.
        return true;
    }

    /** The map version from the frequency lesson, kept as the oracle. */
    static boolean viaMap(String s, String t) {
        Map<Character, Integer> m = new HashMap<>();
        for (char c : s.toCharArray()) m.merge(c, 1, Integer::sum);
        for (char c : t.toCharArray()) m.merge(c, -1, Integer::sum);
        for (int v : m.values()) if (v != 0) return false;
        return true;
    }

    public static void main(String[] args) {
        // The statement examples.
        if (!isAnagram("Ab 1", "1 bA")) throw new AssertionError("example 1");
        if (isAnagram("aab", "aBb")) throw new AssertionError("example 2");
        if (!isAnagram("", "")) throw new AssertionError("empty");
        // The largest ASCII code stays inside the table; a code of 128 would not.
        if (!isAnagram("\u007f", "\u007f")) throw new AssertionError("code 127");
        boolean threw = false;
        try { isAnagram("\u0080", "\u0080"); } catch (ArrayIndexOutOfBoundsException e) { threw = true; }
        if (!threw) throw new AssertionError("code 128 breaks the contract");
        // Random ASCII strings are checked against the map version.
        Random rnd = new Random(64);
        for (int t = 0; t < 600; t++) {
            String s = rand(rnd);
            String u = rnd.nextBoolean() ? shuffle(s, rnd) : rand(rnd);
            if (isAnagram(s, u) != viaMap(s, u)) throw new AssertionError(s + " | " + u);
        }
    }

    static String rand(Random r) {
        StringBuilder sb = new StringBuilder();
        int len = r.nextInt(7);
        for (int i = 0; i < len; i++) sb.append((char) (r.nextInt(4) == 0 ? r.nextInt(128) : 'a' + r.nextInt(3)));
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

#### Solution: [Boundary] Sparse IDs (Author exercise)
<!-- id: hm-sparse-ids -->

**Approach.**
The method finds the minimum and the maximum in one pass, computes the key range as `(long) max - min + 1`, and compares it with `4L * ids.length`. The cast comes before the subtraction, because in `int` arithmetic the range of `[Integer.MIN_VALUE, Integer.MAX_VALUE]` wraps to 0 and would pass the test. The decision depends on the range and not on how many ids occur, so two ids 2 and one billion give false. The invariant is that after index `i`, `min` and `max` are the extremes of `ids[0..i]`.

**Complexity.**
- **Time** is O(n), because one pass finds both extremes.
- **Space** is O(1), because the method keeps two numbers.

```java run
import java.util.*;

public final class SparseIds {
    /**
     * Reports whether the key range is at most four slots per id.
     * Time: O(n). Space: O(1).
     * Invariant: after index i, min and max are the extremes of ids[0..i].
     */
    static boolean directAddressingOk(int[] ids) {
        int min = ids[0], max = ids[0];
        // One pass finds both extremes.
        for (int v : ids) {
            min = Math.min(min, v);
            max = Math.max(max, v);
        }
        // The cast to long comes first, so the subtraction cannot wrap.
        long range = (long) max - min + 1;
        return range <= 4L * ids.length;
    }

    /** The mistake: the range is computed in int. */
    static boolean overflowing(int[] ids) {
        int min = ids[0], max = ids[0];
        for (int v : ids) { min = Math.min(min, v); max = Math.max(max, v); }
        int range = max - min + 1;
        return range <= 4 * ids.length;
    }

    public static void main(String[] args) {
        // The statement examples.
        if (!directAddressingOk(new int[] {5, 7, 6, 9})) throw new AssertionError("example 1");
        if (directAddressingOk(new int[] {2, 1_000_000_000})) throw new AssertionError("example 2");
        // The full int range: the correct method says no, and the int version wraps and says yes.
        int[] ends = {Integer.MIN_VALUE, Integer.MAX_VALUE};
        if (directAddressingOk(ends)) throw new AssertionError("full range");
        if (!overflowing(ends)) throw new AssertionError("int arithmetic wraps");
        // A single id has range 1.
        if (!directAddressingOk(new int[] {Integer.MIN_VALUE})) throw new AssertionError("single id");
        // The bound is inclusive: range 8 with 2 ids is acceptable, range 9 is not.
        if (!directAddressingOk(new int[] {10, 17}) || directAddressingOk(new int[] {10, 18})) throw new AssertionError("threshold");
        // Random arrays are checked against a BigInteger-free oracle that uses double.
        Random rnd = new Random(65);
        for (int t = 0; t < 600; t++) {
            int[] a = new int[1 + rnd.nextInt(6)];
            for (int k = 0; k < a.length; k++) a[k] = rnd.nextBoolean() ? rnd.nextInt(30) : (rnd.nextBoolean() ? Integer.MAX_VALUE - rnd.nextInt(5) : Integer.MIN_VALUE + rnd.nextInt(5));
            double lo = Double.MAX_VALUE, hi = -Double.MAX_VALUE;
            for (int v : a) { lo = Math.min(lo, v); hi = Math.max(hi, v); }
            boolean expect = hi - lo + 1 <= 4.0 * a.length;
            if (directAddressingOk(a) != expect) throw new AssertionError(Arrays.toString(a));
        }
    }
}
```

#### Solution: [Recognize] Design HashMap (LeetCode 706)
<!-- id: hm-design-hashmap -->

**Approach.**
The key range is 2^32, so no array with one slot per key is possible. The class keeps an array of buckets, and each bucket is a singly linked list of nodes with a key and a value. The index of a key is `Math.floorMod(Integer.hashCode(key), buckets.length)`, which lies in `0..length-1` even for a negative key. `put` walks the chain of its bucket and replaces the value of an equal key, or adds a new node at the front. `get` walks the chain and returns the value or -1. `remove` unlinks the node. The array doubles when the number of entries exceeds the number of buckets, and every node moves to its new bucket, so chains stay short. The invariant is that every node sits in the bucket that its key computes, and no key appears twice.

**Complexity.**
- **Time** is expected O(1) per call, amortized, because the load factor stays at most 1 and a doubling costs O(size) once per doubling.
- **Space** is O(size + buckets), which is O(size) because the bucket count stays within a constant factor of the size.

```java run
import java.util.*;

public final class DesignHashMap {
    static final class MyHashMap {
        private static final class Node {
            final int key;
            int value;
            Node next;
            Node(int key, int value, Node next) { this.key = key; this.value = value; this.next = next; }
        }

        private Node[] buckets = new Node[16];
        private int size;

        private int index(int key, int length) {
            // floorMod keeps the index in range for negative hash codes.
            return Math.floorMod(Integer.hashCode(key), length);
        }

        /** Stores or replaces the value of key. Expected O(1) amortized. */
        void put(int key, int value) {
            int b = index(key, buckets.length);
            // The chain walk is short because the load factor stays at most 1.
            for (Node n = buckets[b]; n != null; n = n.next) {
                if (n.key == key) {
                    n.value = value;
                    return;
                }
            }
            buckets[b] = new Node(key, value, buckets[b]);
            size++;
            if (size > buckets.length) resize();
        }

        /** Returns the value of key, or -1 when the key is absent. Expected O(1). */
        int get(int key) {
            for (Node n = buckets[index(key, buckets.length)]; n != null; n = n.next) {
                if (n.key == key) return n.value;
            }
            return -1;
        }

        /** Deletes key if present. Expected O(1). */
        void remove(int key) {
            int b = index(key, buckets.length);
            Node prev = null;
            for (Node n = buckets[b]; n != null; prev = n, n = n.next) {
                if (n.key == key) {
                    // Unlink the node from its chain.
                    if (prev == null) buckets[b] = n.next; else prev.next = n.next;
                    size--;
                    return;
                }
            }
        }

        private void resize() {
            Node[] bigger = new Node[buckets.length * 2];
            // Every node moves to the bucket that the longer array computes.
            for (Node head : buckets) {
                for (Node n = head; n != null; ) {
                    Node next = n.next;
                    int b = index(n.key, bigger.length);
                    n.next = bigger[b];
                    bigger[b] = n;
                    n = next;
                }
            }
            buckets = bigger;
        }

        int bucketCount() { return buckets.length; }
    }

    public static void main(String[] args) {
        // The statement examples.
        MyHashMap m = new MyHashMap();
        m.put(7, 70); m.put(-3, 5);
        if (m.get(7) != 70 || m.get(8) != -1) throw new AssertionError("example 1");
        MyHashMap m2 = new MyHashMap();
        m2.put(7, 70); m2.put(7, 71); m2.remove(7);
        if (m2.get(7) != -1) throw new AssertionError("example 2");
        // Java facts used by the index: the hash of an Integer is its value, and floorMod stays in range.
        if (Integer.hashCode(-3) != -3 || Math.floorMod(-3, 16) != 13) throw new AssertionError("index of a negative key");
        // The extreme keys work.
        m.put(Integer.MIN_VALUE, 1); m.put(Integer.MAX_VALUE, 2);
        if (m.get(Integer.MIN_VALUE) != 1 || m.get(Integer.MAX_VALUE) != 2) throw new AssertionError("extreme keys");
        // Growth: 1000 keys end in more than 16 buckets and stay readable.
        MyHashMap big = new MyHashMap();
        for (int k = 0; k < 1000; k++) big.put(k * 7919, k);
        if (big.bucketCount() <= 16) throw new AssertionError("no growth");
        for (int k = 0; k < 1000; k++) if (big.get(k * 7919) != k) throw new AssertionError("lost key " + k);
        // Random operations are checked against java.util.HashMap.
        Random rnd = new Random(66);
        for (int t = 0; t < 200; t++) {
            MyHashMap mine = new MyHashMap();
            Map<Integer, Integer> ref = new HashMap<>();
            for (int step = 0; step < 300; step++) {
                int key = rnd.nextInt(40) - 20;
                int op = rnd.nextInt(3);
                if (op == 0) { int v = rnd.nextInt(1000); mine.put(key, v); ref.put(key, v); }
                else if (op == 1) { mine.remove(key); ref.remove(key); }
                else if (mine.get(key) != ref.getOrDefault(key, -1)) throw new AssertionError("trial " + t + " step " + step);
            }
        }
    }
}
```
