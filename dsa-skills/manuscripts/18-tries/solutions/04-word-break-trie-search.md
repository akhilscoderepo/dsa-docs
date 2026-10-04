<!-- solutions-for: 04-word-break-trie-search -->
### Word-Break Trie Search

#### Solution: [Build] Dictionary Ends From One Index (Author exercise)
<!-- id: tn-ends-from-index -->

**Approach.** Build a trie of the dictionary. For a start, move a cursor along the letters of `s` from that position. A missing edge stops the walk, and each flagged node adds its position plus one to the list. The walk reads at most as many letters as the longest word, because the trie has no deeper node, and a start equal to the length of the string reads nothing and returns an empty list. The oracle cuts every substring from the start and looks it up in a hash set. The assertions compare the two on random strings and dictionaries over a two-letter alphabet, which produce many words that begin inside each other.

**Complexity.** O(m) per start for m the longest word, and O(total dictionary letters) to build.

```java run
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Random;
import java.util.Set;

public final class EndsFromIndex {
    static final class Node {
        final Node[] next = new Node[26];
        boolean word;
    }

    static List<List<Integer>> solve(String s, List<String> words, List<Integer> starts) {
        Node root = new Node();
        for (String w : words) {
            Node cur = root;
            for (char c : w.toCharArray()) {
                if (cur.next[c - 'a'] == null) cur.next[c - 'a'] = new Node();
                cur = cur.next[c - 'a'];
            }
            cur.word = true;
        }
        List<List<Integer>> out = new ArrayList<>();
        for (int start : starts) {
            List<Integer> ends = new ArrayList<>();
            Node cur = root;
            for (int j = start; j < s.length(); j++) {
                cur = cur.next[s.charAt(j) - 'a'];
                if (cur == null) break;
                if (cur.word) ends.add(j + 1);
            }
            out.add(ends);
        }
        return out;
    }

    static List<List<Integer>> oracle(String s, List<String> words, List<Integer> starts) {
        Set<String> set = new HashSet<>(words);
        List<List<Integer>> out = new ArrayList<>();
        for (int start : starts) {
            List<Integer> ends = new ArrayList<>();
            for (int to = start + 1; to <= s.length(); to++) if (set.contains(s.substring(start, to))) ends.add(to);
            out.add(ends);
        }
        return out;
    }

    static String text(Random rnd, int len) {
        StringBuilder sb = new StringBuilder();
        for (int j = 0; j < len; j++) sb.append((char) ('a' + rnd.nextInt(2)));
        return sb.toString();
    }

    public static void main(String[] args) {
        List<String> dict = List.of("cat", "cats", "and", "sand", "dog");
        if (!solve("catsanddog", dict, List.of(0, 3, 4, 7, 9)).toString().equals("[[3, 4], [7], [7], [10], []]")) throw new AssertionError("example 1");
        if (!solve("aaa", List.of("a", "aa", "aaaa"), List.of(0, 1, 2, 3)).toString().equals("[[1, 2], [2, 3], [3], []]")) throw new AssertionError("example 2");
        Random rnd = new Random(18401);
        for (int t = 0; t < 5000; t++) {
            String s = text(rnd, 1 + rnd.nextInt(8));
            List<String> words = new ArrayList<>();
            int n = rnd.nextInt(6);
            for (int k = 0; k < n; k++) words.add(text(rnd, 1 + rnd.nextInt(4)));
            List<Integer> starts = new ArrayList<>();
            for (int i = 0; i <= s.length(); i++) starts.add(i);
            if (!solve(s, words, starts).equals(oracle(s, words, starts))) throw new AssertionError("differs on " + s + words);
        }
    }
}
```

#### Solution: [Vary] One Valid Segmentation On Short Input (Author exercise)
<!-- id: tn-one-segmentation -->

**Approach.** The recursion takes a start index and a shared list of the words chosen so far. At the end of the string it returns true. Otherwise it asks the trie walk for the ends of the start, tries them in increasing order, appends the piece before each call, and removes it after a failed call, so the list always holds the words chosen on the current route. The first route that reaches the end is the answer, joined with spaces. The oracle enumerates every segmentation by cutting substrings and checking a hash set, and takes the first in generation order. Since both try ends in increasing order, the two first answers must agree. The assertions also check that every returned answer rebuilds `s` and uses only dictionary words, and that the empty string is returned exactly when the enumeration finds nothing.

**Complexity.** Exponential in the worst case, O(2^n) calls, which is why the input is short.

```java run
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Random;
import java.util.Set;

public final class OneSegmentation {
    static final class Node {
        final Node[] next = new Node[26];
        boolean word;
    }

    static boolean split(Node root, String s, int start, List<String> chosen) {
        if (start == s.length()) return true;
        Node cur = root;
        for (int j = start; j < s.length(); j++) {
            cur = cur.next[s.charAt(j) - 'a'];
            if (cur == null) break;
            if (!cur.word) continue;
            chosen.add(s.substring(start, j + 1));
            if (split(root, s, j + 1, chosen)) return true;
            chosen.remove(chosen.size() - 1);
        }
        return false;
    }

    static String solve(String s, List<String> words) {
        Node root = new Node();
        for (String w : words) {
            Node cur = root;
            for (char c : w.toCharArray()) {
                if (cur.next[c - 'a'] == null) cur.next[c - 'a'] = new Node();
                cur = cur.next[c - 'a'];
            }
            cur.word = true;
        }
        List<String> chosen = new ArrayList<>();
        return split(root, s, 0, chosen) ? String.join(" ", chosen) : "";
    }

    static void all(String s, int start, Set<String> dict, List<String> path, List<String> found) {
        if (start == s.length()) { found.add(String.join(" ", path)); return; }
        for (int to = start + 1; to <= s.length(); to++) {
            String piece = s.substring(start, to);
            if (!dict.contains(piece)) continue;
            path.add(piece);
            all(s, to, dict, path, found);
            path.remove(path.size() - 1);
        }
    }

    static String text(Random rnd, int len) {
        StringBuilder sb = new StringBuilder();
        for (int j = 0; j < len; j++) sb.append((char) ('a' + rnd.nextInt(2)));
        return sb.toString();
    }

    public static void main(String[] args) {
        String a = solve("rainbowpath", List.of("rain", "bow", "rainbow", "path", "pa", "th"));
        if (!a.equals("rain bow pa th")) throw new AssertionError("example 1: " + a);
        if (!solve("abx", List.of("a", "ab", "b")).equals("")) throw new AssertionError("example 2");
        Random rnd = new Random(18402);
        for (int t = 0; t < 5000; t++) {
            String s = text(rnd, 1 + rnd.nextInt(9));
            List<String> words = new ArrayList<>();
            int n = rnd.nextInt(6);
            for (int k = 0; k < n; k++) words.add(text(rnd, 1 + rnd.nextInt(4)));
            List<String> found = new ArrayList<>();
            all(s, 0, new HashSet<>(words), new ArrayList<>(), found);
            String got = solve(s, words);
            String want = found.isEmpty() ? "" : found.get(0);
            if (!got.equals(want)) throw new AssertionError("differs on " + s + words + ": " + got + " vs " + want);
            if (!got.isEmpty() && !got.replace(" ", "").equals(s)) throw new AssertionError("pieces must rebuild the string");
        }
    }
}
```

#### Solution: [Boundary] Prefix Exists But Word Does Not (Author exercise)
<!-- id: tn-prefix-not-word -->

**Approach.** The recursion counts the splits of the suffix from a start index. At the end of the string it returns 1. Otherwise it walks the trie from the start and, at each flagged node only, adds the count of the suffix that begins after that node. An unflagged node on the route, such as the node for `abcd` when only `abcde` is stored, adds nothing, and a missing edge stops the walk. The oracle uses a different idea: it tries every set of cut positions as a bit mask over the gaps between letters and counts the masks whose pieces are all dictionary words. The assertions compare the two on random short inputs and check the hostile example.

**Complexity.** Exponential in the worst case, O(2^n) calls, so the input is short.

```java run
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Random;
import java.util.Set;

public final class PrefixNotWord {
    static final class Node {
        final Node[] next = new Node[26];
        boolean word;
    }

    static int count(Node root, String s, int start) {
        if (start == s.length()) return 1;
        int total = 0;
        Node cur = root;
        for (int j = start; j < s.length(); j++) {
            cur = cur.next[s.charAt(j) - 'a'];
            if (cur == null) break;
            if (cur.word) total += count(root, s, j + 1);
        }
        return total;
    }

    static int solve(String s, List<String> words) {
        Node root = new Node();
        for (String w : words) {
            Node cur = root;
            for (char c : w.toCharArray()) {
                if (cur.next[c - 'a'] == null) cur.next[c - 'a'] = new Node();
                cur = cur.next[c - 'a'];
            }
            cur.word = true;
        }
        return count(root, s, 0);
    }

    static int oracle(String s, List<String> words) {
        Set<String> dict = new HashSet<>(words);
        int gaps = s.length() - 1, ways = 0;
        for (int mask = 0; mask < (1 << gaps); mask++) {
            int from = 0;
            boolean ok = true;
            for (int g = 0; g <= gaps && ok; g++) {
                if (g == gaps || (mask >> g & 1) == 1) {
                    ok = dict.contains(s.substring(from, g + 1));
                    from = g + 1;
                }
            }
            if (ok) ways++;
        }
        return ways;
    }

    static String text(Random rnd, int len) {
        StringBuilder sb = new StringBuilder();
        for (int j = 0; j < len; j++) sb.append((char) ('a' + rnd.nextInt(2)));
        return sb.toString();
    }

    public static void main(String[] args) {
        if (solve("aaaa", List.of("a", "aa")) != 5) throw new AssertionError("example 1");
        if (solve("abcd", List.of("abcde", "bc", "a", "d")) != 1) throw new AssertionError("example 2");
        if (solve("ab", List.of("a")) != 0) throw new AssertionError("no split");
        Random rnd = new Random(18403);
        for (int t = 0; t < 5000; t++) {
            String s = text(rnd, 1 + rnd.nextInt(9));
            Set<String> pick = new HashSet<>();
            int n = rnd.nextInt(7);
            for (int k = 0; k < n; k++) pick.add(text(rnd, 1 + rnd.nextInt(4)));
            List<String> words = new ArrayList<>(pick);
            if (solve(s, words) != oracle(s, words)) throw new AssertionError("differs on " + s + words);
        }
    }
}
```

#### Solution: [Recognize] Explain Trie-Based Word Break State (Author exercise)
<!-- id: tn-word-break-state -->

**Approach.** The state of the question is one number, the start index, because the unsplit suffix is fully determined by it. The recursion is entered once per route, so the same start index can be entered many times, and the answer from a start index never depends on how it was reached. The solution runs the plain recursion with a call counter and a set of start indices seen, and returns the two numbers. The oracle does the same with substrings and a hash set of words, which is a different way to find the ends, so the counts must agree. The assertions also show the lesson's claim: the number of distinct start indices never exceeds n + 1, while the call count for a failing banner of letters `a` followed by `b` grows past every bound that is linear in n.

**Complexity.** Exponential in the number of calls, with at most n + 1 distinct states. Remembering the answer of each start index would bound the calls by the number of states, and that technique is the subject of Chapter 26.

```java run
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Random;
import java.util.Set;

public final class WordBreakState {
    static final class Node {
        final Node[] next = new Node[26];
        boolean word;
    }

    static int calls;
    static Set<Integer> seen;

    static boolean can(Node root, String s, int start) {
        calls++;
        seen.add(start);
        if (start == s.length()) return true;
        Node cur = root;
        for (int j = start; j < s.length(); j++) {
            cur = cur.next[s.charAt(j) - 'a'];
            if (cur == null) break;
            if (cur.word && can(root, s, j + 1)) return true;
        }
        return false;
    }

    static int[] solve(String s, List<String> words) {
        Node root = new Node();
        for (String w : words) {
            Node cur = root;
            for (char c : w.toCharArray()) {
                if (cur.next[c - 'a'] == null) cur.next[c - 'a'] = new Node();
                cur = cur.next[c - 'a'];
            }
            cur.word = true;
        }
        calls = 0;
        seen = new HashSet<>();
        can(root, s, 0);
        return new int[] {calls, seen.size()};
    }

    static int oCalls;
    static Set<Integer> oSeen;

    static boolean oracleCan(String s, int start, Set<String> dict) {
        oCalls++;
        oSeen.add(start);
        if (start == s.length()) return true;
        for (int to = start + 1; to <= s.length(); to++) {
            if (dict.contains(s.substring(start, to)) && oracleCan(s, to, dict)) return true;
        }
        return false;
    }

    static int[] oracle(String s, List<String> words) {
        oCalls = 0;
        oSeen = new HashSet<>();
        oracleCan(s, 0, new HashSet<>(words));
        return new int[] {oCalls, oSeen.size()};
    }

    static String text(Random rnd, int len) {
        StringBuilder sb = new StringBuilder();
        for (int j = 0; j < len; j++) sb.append((char) ('a' + rnd.nextInt(2)));
        return sb.toString();
    }

    static void same(int[] a, int[] b, String what) {
        if (a[0] != b[0] || a[1] != b[1]) throw new AssertionError(what + ": " + a[0] + "," + a[1] + " vs " + b[0] + "," + b[1]);
    }

    public static void main(String[] args) {
        same(solve("aaaab", List.of("a", "aa")), new int[] {12, 5}, "example 1");
        same(solve("abc", List.of("abc", "ab", "c")), new int[] {3, 3}, "example 2");
        int previous = 0;
        for (int k = 4; k <= 16; k += 4) {
            String banner = "a".repeat(k) + "b";
            int[] r = solve(banner, List.of("a", "aa"));
            if (r[1] != k + 1) throw new AssertionError("start indices 0.." + k + " are the only states");
            if (r[0] <= 3 * previous && previous > 0) throw new AssertionError("calls must grow faster than linearly");
            previous = r[0];
        }
        Random rnd = new Random(18404);
        for (int t = 0; t < 5000; t++) {
            String s = text(rnd, 1 + rnd.nextInt(9));
            List<String> words = new ArrayList<>();
            int n = rnd.nextInt(6);
            for (int k = 0; k < n; k++) words.add(text(rnd, 1 + rnd.nextInt(4)));
            int[] got = solve(s, words);
            same(got, oracle(s, words), "random " + s + words);
            if (got[1] > s.length() + 1 || got[0] < got[1]) throw new AssertionError("state count bound");
        }
    }
}
```
