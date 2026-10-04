<!-- solutions-for: 05-sorting-and-java-comparators -->
### Solutions For Sorted Letter Groups

#### Solution: [Build] Valid Anagram (LeetCode 242)
<!-- id: so-anagram-normalized -->

**Approach.**
The method builds the canonical form of each string. It keeps only the letters, writes them in lowercase, and sorts the characters. Two strings are anagrams under this contract exactly when their canonical forms are equal. Letters are the only characters that count, so digits, spaces and punctuation do not enter the form. The invariant is that the canonical form depends only on the multiset of lowercase letters of the string.

**Complexity.**
- **Time** is O(n log n), because each form is sorted once, and the comparison costs O(n).
- **Space** is O(n) for the two character arrays.

```java run
import java.util.*;

public final class AnagramNormalized {
    /**
     * Returns the sorted lowercase letters of s, ignoring all other characters.
     * Time: O(n log n). Space: O(n).
     * Invariant: the result depends only on the multiset of lowercase letters in s.
     */
    static char[] form(String s) {
        StringBuilder sb = new StringBuilder();
        // Only letters enter the form, written in lowercase.
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            if (Character.isLetter(c)) sb.append(Character.toLowerCase(c));
        }
        char[] chars = sb.toString().toCharArray();
        Arrays.sort(chars);
        return chars;
    }

    static boolean isAnagram(String s, String t) {
        // Equal canonical forms mean equal multisets of letters.
        return Arrays.equals(form(s), form(t));
    }

    public static void main(String[] args) {
        // The statement examples and the empty strings.
        if (!isAnagram("Dormitory!", "dirty room")) throw new AssertionError("example 1");
        if (isAnagram("aab", "ab b")) throw new AssertionError("example 2");
        if (!isAnagram("", "123 !!")) throw new AssertionError("no letters");
        // Java fact from the lesson: toString of an array shows its identity, and equal arrays have different identities.
        char[] x = {'a'}, y = {'a'};
        if (x.toString().equals(y.toString())) throw new AssertionError("identity string");
        // Random strings are checked against a count-table oracle over 26 letters.
        Random rnd = new Random(131);
        String alphabet = "abAB c1!";
        for (int t = 0; t < 600; t++) {
            StringBuilder p = new StringBuilder(), q = new StringBuilder();
            for (int k = rnd.nextInt(8); k > 0; k--) p.append(alphabet.charAt(rnd.nextInt(alphabet.length())));
            for (int k = rnd.nextInt(8); k > 0; k--) q.append(alphabet.charAt(rnd.nextInt(alphabet.length())));
            int[] c1 = new int[26], c2 = new int[26];
            for (char c : p.toString().toCharArray()) if (Character.isLetter(c)) c1[Character.toLowerCase(c) - 'a']++;
            for (char c : q.toString().toCharArray()) if (Character.isLetter(c)) c2[Character.toLowerCase(c) - 'a']++;
            if (isAnagram(p.toString(), q.toString()) != Arrays.equals(c1, c2)) throw new AssertionError(p + " | " + q);
        }
    }
}
```

#### Solution: [Vary] Group Anagrams (LeetCode 49)
<!-- id: so-group-sorted-key -->

**Approach.**
The method computes the sorted-letter key of each word and appends the word to the list of that key in a `HashMap`. The words of a list therefore stay in input order. After the loop, the method copies the keys into a list, sorts the list, and reads the groups in that order. The sort gives a fixed output order, because `HashMap` iteration order is unspecified. The invariant after the loop is that each key owns exactly the words with that canonical form, in input order.

**Complexity.**
- **Time** is O(n * L log L + g log g * L), where g is the number of groups, because each word is sorted once and the keys are sorted once.
- **Space** is O(n * L) for the map and the output.

```java run
import java.util.*;

public final class GroupSortedKey {
    /**
     * Groups anagrams and orders the groups by their canonical form.
     * Time: O(n * L log L). Space: O(n * L).
     * Invariant: after the loop, each key owns exactly the words with that canonical form, in input order.
     */
    static List<List<String>> group(String[] words) {
        Map<String, List<String>> map = new HashMap<>();
        for (String w : words) {
            char[] c = w.toCharArray();
            Arrays.sort(c);
            // The key is built with new String, so equal contents give equal keys.
            map.computeIfAbsent(new String(c), k -> new ArrayList<>()).add(w);
        }
        // The key list is sorted because HashMap order is unspecified.
        List<String> keys = new ArrayList<>(map.keySet());
        Collections.sort(keys);
        List<List<String>> out = new ArrayList<>();
        for (String k : keys) out.add(map.get(k));
        return out;
    }

    public static void main(String[] args) {
        // The statement examples and the empty input.
        if (!group(new String[] {"rat", "tar", "tab", "art", "bat"}).equals(List.of(List.of("tab", "bat"), List.of("rat", "tar", "art")))) throw new AssertionError("example 1");
        if (!group(new String[] {"", "b", ""}).equals(List.of(List.of("", ""), List.of("b")))) throw new AssertionError("example 2");
        if (!group(new String[0]).isEmpty()) throw new AssertionError("empty");
        // Java fact from the lesson: a char array is not a usable key, but a String built from it is.
        Map<char[], Integer> bad = new HashMap<>();
        bad.put(new char[] {'a'}, 1);
        if (bad.containsKey(new char[] {'a'})) throw new AssertionError("array key");
        // Random words are checked against a pairwise oracle that compares sorted forms and orders groups by form.
        Random rnd = new Random(132);
        for (int t = 0; t < 500; t++) {
            String[] w = new String[rnd.nextInt(8)];
            for (int k = 0; k < w.length; k++) {
                StringBuilder sb = new StringBuilder();
                for (int len = rnd.nextInt(4); len > 0; len--) sb.append((char) ('a' + rnd.nextInt(3)));
                w[k] = sb.toString();
            }
            List<List<String>> expect = new ArrayList<>();
            List<String> formsSeen = new ArrayList<>();
            for (String s : w) {
                char[] c = s.toCharArray();
                Arrays.sort(c);
                String f = new String(c);
                int at = formsSeen.indexOf(f);
                if (at < 0) { formsSeen.add(f); expect.add(new ArrayList<>(List.of(s))); } else expect.get(at).add(s);
            }
            // The oracle orders groups by selection of the smallest remaining form.
            List<List<String>> ordered = new ArrayList<>();
            List<String> forms = new ArrayList<>(formsSeen);
            while (!forms.isEmpty()) {
                int best = 0;
                for (int k = 1; k < forms.size(); k++) if (forms.get(k).compareTo(forms.get(best)) < 0) best = k;
                ordered.add(expect.get(formsSeen.indexOf(forms.get(best))));
                forms.remove(best);
            }
            if (!group(w).equals(ordered)) throw new AssertionError(Arrays.toString(w));
        }
    }
}
```

#### Solution: [Boundary] Sort Characters By Frequency (LeetCode 451)
<!-- id: so-frequency-order -->

**Approach.**
The method counts each character code in an array of 128 entries. It collects the codes that occur and sorts them with a comparator that puts the larger count first and the smaller code first on a tie. The tie rule makes the answer unique. The method then writes each code as many times as its count. The key that groups equal characters is the character itself, and the frequency decides only the order of the groups. The invariant after the sort is that adjacent codes have a larger count on the left, or an equal count and a smaller code.

**Complexity.**
- **Time** is O(n + 128 log 128), which is O(n), because the counting pass reads each character once and the sort covers at most 128 codes.
- **Space** is O(n) for the output and O(1) for the count table.

```java run
import java.util.*;

public final class FrequencyOrder {
    /**
     * Returns the characters of s ordered by frequency, then by character code.
     * Time: O(n). Space: O(n).
     * Invariant: adjacent codes have a larger count on the left, or an equal count and a smaller code.
     */
    static String byFrequency(String s) {
        int[] count = new int[128];
        for (int i = 0; i < s.length(); i++) count[s.charAt(i)]++;
        List<Integer> codes = new ArrayList<>();
        for (int c = 0; c < 128; c++) if (count[c] > 0) codes.add(c);
        // The larger count comes first, and the smaller code wins a tie.
        codes.sort((a, b) -> count[a] != count[b] ? Integer.compare(count[b], count[a]) : Integer.compare(a, b));
        StringBuilder sb = new StringBuilder();
        for (int c : codes) for (int k = 0; k < count[c]; k++) sb.append((char) c);
        return sb.toString();
    }

    public static void main(String[] args) {
        // The statement examples and the empty input.
        if (!byFrequency("mississippi").equals("iiiissssppm")) throw new AssertionError("example 1");
        if (!byFrequency("bBaA").equals("ABab")) throw new AssertionError("example 2");
        if (!byFrequency("").equals("")) throw new AssertionError("empty");
        // Random strings are checked against an oracle that sorts all characters by a combined key.
        Random rnd = new Random(133);
        for (int t = 0; t < 500; t++) {
            StringBuilder sb = new StringBuilder();
            for (int k = rnd.nextInt(14); k > 0; k--) sb.append((char) ('a' + rnd.nextInt(4)));
            String s = sb.toString();
            Character[] all = new Character[s.length()];
            for (int k = 0; k < all.length; k++) all[k] = s.charAt(k);
            Arrays.sort(all, (x, y) -> {
                int cx = 0, cy = 0;
                for (int k = 0; k < s.length(); k++) { if (s.charAt(k) == x) cx++; if (s.charAt(k) == y) cy++; }
                return cx != cy ? Integer.compare(cy, cx) : Character.compare(x, y);
            });
            StringBuilder expect = new StringBuilder();
            for (char c : all) expect.append(c);
            if (!byFrequency(s).equals(expect.toString())) throw new AssertionError(s);
        }
    }
}
```

#### Solution: [Recognize] Determine If Two Strings Are Close (LeetCode 1657)
<!-- id: so-strings-close -->

**Approach.**
The two operations keep the length, keep the set of letters that occur, and permute the list of counts among those letters. Swapping positions rearranges the string freely. Exchanging two letters everywhere exchanges their counts. Two strings are therefore close exactly when they have the same length, the same set of letters, and the same multiset of counts. The method counts letters in two tables of 26 entries, compares which entries are nonzero, and compares the two count tables after sorting. The pair `abbccc` and `aaabbc` is close, although their sorted strings differ, so a raw sorted string is not a valid key. The invariant is that the sorted counts are the multiset of letter counts of the string.

**Complexity.**
- **Time** is O(n + 26 log 26), which is O(n), because the counting pass dominates and the sorts cover 26 entries.
- **Space** is O(1), because both tables have 26 entries.

```java run
import java.util.*;

public final class StringsClose {
    /**
     * Returns true when one string becomes the other by the two allowed operations.
     * Time: O(n). Space: O(1).
     * Invariant: the sorted counts are the multiset of letter counts of the string.
     */
    static boolean close(String a, String b) {
        // Different lengths cannot match, because both operations keep the length.
        if (a.length() != b.length()) return false;
        int[] ca = new int[26], cb = new int[26];
        for (int i = 0; i < a.length(); i++) { ca[a.charAt(i) - 'a']++; cb[b.charAt(i) - 'a']++; }
        // The same letters must occur in both strings, because the operations never create a new letter.
        for (int i = 0; i < 26; i++) if ((ca[i] == 0) != (cb[i] == 0)) return false;
        Arrays.sort(ca);
        Arrays.sort(cb);
        // Equal sorted counts mean that one count list is a permutation of the other.
        return Arrays.equals(ca, cb);
    }

    /** Oracle: searches every string reachable by the two operations, for short strings. */
    static boolean brute(String a, String b) {
        Set<String> seen = new HashSet<>();
        Deque<String> queue = new ArrayDeque<>();
        seen.add(a);
        queue.add(a);
        while (!queue.isEmpty()) {
            String s = queue.poll();
            if (s.equals(b)) return true;
            for (int i = 0; i < s.length(); i++) {
                for (int j = i + 1; j < s.length(); j++) {
                    char[] c = s.toCharArray();
                    char tmp = c[i]; c[i] = c[j]; c[j] = tmp;
                    String next = new String(c);
                    if (seen.add(next)) queue.add(next);
                }
            }
            for (char x = 'a'; x <= 'c'; x++) {
                for (char y = (char) (x + 1); y <= 'c'; y++) {
                    if (s.indexOf(x) < 0 || s.indexOf(y) < 0) continue;
                    StringBuilder sb = new StringBuilder();
                    for (char ch : s.toCharArray()) sb.append(ch == x ? y : ch == y ? x : ch);
                    String next = sb.toString();
                    if (seen.add(next)) queue.add(next);
                }
            }
        }
        return false;
    }

    public static void main(String[] args) {
        // The statement examples and the empty strings.
        if (!close("aabbbc", "bccaaa")) throw new AssertionError("example 1");
        if (close("aabb", "abbb")) throw new AssertionError("example 2");
        if (!close("", "")) throw new AssertionError("empty");
        // Different letter sets with equal counts must fail.
        if (close("aabb", "ccdd")) throw new AssertionError("letter sets");
        // Random short strings over three letters are checked against the breadth-first oracle.
        Random rnd = new Random(134);
        for (int t = 0; t < 400; t++) {
            int n = rnd.nextInt(6);
            StringBuilder p = new StringBuilder(), q = new StringBuilder();
            for (int k = 0; k < n; k++) { p.append((char) ('a' + rnd.nextInt(3))); q.append((char) ('a' + rnd.nextInt(3))); }
            if (close(p.toString(), q.toString()) != brute(p.toString(), q.toString())) throw new AssertionError(p + " | " + q);
        }
    }
}
```
