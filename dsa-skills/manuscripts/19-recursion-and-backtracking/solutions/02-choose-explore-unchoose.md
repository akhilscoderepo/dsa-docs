<!-- solutions-for: 02-choose-explore-unchoose -->
### Choose Explore Unchoose

#### Solution: [Build] Binary Choices (Author exercise)
<!-- id: bt-binary-choices -->

**Approach.** One `StringBuilder` is the working path. At each position the call appends `0`, recurses, deletes the last character, then appends `1`, recurses and deletes again, and a finished path is stored with `toString`, which makes a copy. The oracle counts from 0 to 2^n - 1 and pads the binary form with zeros, so it shares no code with the search. The harness compares both for every length up to 12 and checks that the builder is empty after the search, which is the exit half of the invariant.

**Complexity.** The 2^n results are written at O(n) each, giving O(n * 2^n) time overall, with a stack of depth n.

```java run
import java.util.ArrayList;
import java.util.List;

public final class BinaryChoices {
    static void build(int n, StringBuilder path, List<String> out) {
        if (path.length() == n) {
            out.add(path.toString());
            return;
        }
        for (char c = '0'; c <= '1'; c++) {
            path.append(c);
            build(n, path, out);
            path.deleteCharAt(path.length() - 1);
        }
    }

    static List<String> strings(int n, StringBuilder path) {
        List<String> out = new ArrayList<>();
        build(n, path, out);
        return out;
    }

    static List<String> oracle(int n) {
        List<String> out = new ArrayList<>();
        for (int m = 0; m < (1 << n); m++) {
            StringBuilder sb = new StringBuilder(Integer.toBinaryString(m));
            while (sb.length() < n) sb.insert(0, '0');
            out.add(n == 0 ? "" : sb.toString());
        }
        return out;
    }

    public static void main(String[] args) {
        if (!strings(2, new StringBuilder()).equals(List.of("00", "01", "10", "11"))) throw new AssertionError("example 1");
        if (!strings(0, new StringBuilder()).equals(List.of(""))) throw new AssertionError("example 2");
        for (int n = 0; n <= 12; n++) {
            StringBuilder path = new StringBuilder();
            List<String> got = strings(n, path);
            if (!got.equals(oracle(n))) throw new AssertionError("differs at n=" + n);
            if (path.length() != 0) throw new AssertionError("path must be empty on exit, n=" + n);
        }
    }
}
```

#### Solution: [Vary] Variable Candidate Loop (Author exercise)
<!-- id: bt-variable-loop -->

**Approach.** The loop at each position runs over the letters of that position's option string, so a position with no letters never recurses and nothing is stored. The path is a `char` buffer written by index, with the undo being the next write at the same depth, and the alternative is also tested with the `ArrayList<Character>` form from the lesson, whose `remove(size - 1)` removes by index. The oracle builds the product iteratively, extending a list of words one option at a time. The harness compares them on random option lists, empty strings included, and checks that an empty option gives no words.

**Complexity.** Output size times length, so at most 4^8 words of length 8, with a stack of depth equal to the number of options.

```java run
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public final class VariableLoop {
    static void build(List<String> options, int position, List<Character> path, List<String> out) {
        if (position == options.size()) {
            StringBuilder sb = new StringBuilder();
            for (char c : path) sb.append(c);
            out.add(sb.toString());
            return;
        }
        for (char c : options.get(position).toCharArray()) {
            path.add(c);
            build(options, position + 1, path, out);
            path.remove(path.size() - 1);
        }
    }

    static List<String> words(List<String> options) {
        List<String> out = new ArrayList<>();
        List<Character> path = new ArrayList<>();
        build(options, 0, path, out);
        if (!path.isEmpty()) throw new AssertionError("path must be empty on exit");
        return out;
    }

    static List<String> oracle(List<String> options) {
        List<String> acc = new ArrayList<>();
        acc.add("");
        for (String opt : options) {
            List<String> next = new ArrayList<>();
            for (String prefix : acc) for (char c : opt.toCharArray()) next.add(prefix + c);
            acc = next;
        }
        return acc;
    }

    public static void main(String[] args) {
        if (!words(List.of("ab", "c", "de")).equals(List.of("acd", "ace", "bcd", "bce"))) throw new AssertionError("example 1");
        if (!words(List.of("xy", "", "z")).isEmpty()) throw new AssertionError("example 2");
        if (!words(List.of()).equals(List.of(""))) throw new AssertionError("no options gives the empty word");
        List<Integer> nums = new ArrayList<>(List.of(10, 20, 30));
        nums.remove(1);
        if (!nums.equals(List.of(10, 30))) throw new AssertionError("remove(int) removes by index");
        List<Integer> big = new ArrayList<>(List.of(10, 1, 3));
        big.remove(Integer.valueOf(1));
        if (!big.equals(List.of(10, 3))) throw new AssertionError("remove(Object) removes by value");
        Random rnd = new Random(19201);
        for (int t = 0; t < 3000; t++) {
            int k = rnd.nextInt(6);
            List<String> options = new ArrayList<>();
            for (int i = 0; i < k; i++) {
                StringBuilder sb = new StringBuilder();
                int len = rnd.nextInt(5);
                for (int j = 0; j < len; j++) sb.append((char) ('a' + rnd.nextInt(26)));
                options.add(sb.toString());
            }
            if (!words(options).equals(oracle(options))) throw new AssertionError("differs on " + options);
        }
    }
}
```

#### Solution: [Boundary] Store A Completed Path (Author exercise)
<!-- id: bt-store-completed -->

**Approach.** The search keeps one list of step sizes. When the remaining stairs reach zero it stores `new ArrayList<>(path)`, so the stored entry is cut loose from the list that the next removal will change. The harness also runs the careless variant that stores `path` itself and asserts what the lesson claims: at the end every stored entry is the same object and reads empty, so the results look like `n`-many empty lists. The oracle enumerates the sequences by growing lists of partial sums iteratively, and a zero-stair climb must return one empty list.

**Complexity.** The number of ways is a Fibonacci number, so the time is proportional to that count times the path length, with a stack of depth at most n.

```java run
import java.util.ArrayList;
import java.util.List;

public final class StoreCompleted {
    static void climb(int left, List<Integer> path, List<List<Integer>> out, boolean copy) {
        if (left == 0) {
            out.add(copy ? new ArrayList<>(path) : path);
            return;
        }
        for (int s = 1; s <= 2; s++) {
            if (s > left) break;
            path.add(s);
            climb(left - s, path, out, copy);
            path.remove(path.size() - 1);
        }
    }

    static List<List<Integer>> ways(int n, boolean copy) {
        List<List<Integer>> out = new ArrayList<>();
        climb(n, new ArrayList<>(), out, copy);
        return out;
    }

    static List<List<Integer>> oracle(int n) {
        List<List<Integer>> done = new ArrayList<>();
        List<List<Integer>> open = new ArrayList<>();
        open.add(new ArrayList<>());
        while (!open.isEmpty()) {
            List<List<Integer>> next = new ArrayList<>();
            for (List<Integer> p : open) {
                int sum = 0;
                for (int v : p) sum += v;
                if (sum == n) { done.add(p); continue; }
                for (int s = 1; s <= 2; s++) {
                    if (sum + s <= n) { List<Integer> q = new ArrayList<>(p); q.add(s); next.add(q); }
                }
            }
            open = next;
        }
        return done;
    }

    static void sortLex(List<List<Integer>> l) {
        l.sort((a, b) -> {
            for (int i = 0; i < Math.min(a.size(), b.size()); i++) if (!a.get(i).equals(b.get(i))) return a.get(i) - b.get(i);
            return a.size() - b.size();
        });
    }

    public static void main(String[] args) {
        if (!ways(3, true).equals(List.of(List.of(1, 1, 1), List.of(1, 2), List.of(2, 1)))) throw new AssertionError("example 1");
        List<List<Integer>> zero = ways(0, true);
        if (zero.size() != 1 || !zero.get(0).isEmpty()) throw new AssertionError("example 2");
        for (int n = 0; n <= 14; n++) {
            List<List<Integer>> got = ways(n, true), want = oracle(n);
            sortLex(want);
            if (!got.equals(want)) throw new AssertionError("differs at n=" + n);
            List<List<Integer>> bad = ways(n, false);
            if (bad.size() != got.size()) throw new AssertionError("same count at n=" + n);
            for (List<Integer> entry : bad) if (!entry.isEmpty()) throw new AssertionError("an uncopied entry should read empty at n=" + n);
            if (n > 0 && bad.get(0) != bad.get(bad.size() - 1)) throw new AssertionError("uncopied entries share one object");
        }
    }
}
```

#### Solution: [Recognize] Subsets (LeetCode 78)
<!-- id: bt-subsets-include-first -->

**Approach.** At index `i` the call either places `nums[i]` on the path, recurses and removes it, or recurses with the path unchanged, with include tried first. A subset is stored, as a copy, when the index reaches the length of the array. The oracle runs over the masks from 2^n - 1 down to 0, reading the highest bit as the first element, which is the same order without any recursion. The harness compares them for random arrays of distinct values and checks that the path is empty at the end of the search.

**Complexity.** Writing 2^n subsets of average length n / 2 costs O(n * 2^n), and the stack is n frames deep.

```java run
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Random;
import java.util.Set;

public final class SubsetsIncludeFirst {
    static void go(int[] nums, int i, List<Integer> path, List<List<Integer>> out) {
        if (i == nums.length) {
            out.add(new ArrayList<>(path));
            return;
        }
        path.add(nums[i]);
        go(nums, i + 1, path, out);
        path.remove(path.size() - 1);
        go(nums, i + 1, path, out);
    }

    static List<List<Integer>> subsets(int[] nums) {
        List<List<Integer>> out = new ArrayList<>();
        List<Integer> path = new ArrayList<>();
        go(nums, 0, path, out);
        if (!path.isEmpty()) throw new AssertionError("path must be empty on exit");
        return out;
    }

    static List<List<Integer>> oracle(int[] nums) {
        int n = nums.length;
        List<List<Integer>> out = new ArrayList<>();
        for (int m = (1 << n) - 1; m >= 0; m--) {
            List<Integer> s = new ArrayList<>();
            for (int i = 0; i < n; i++) if ((m >> (n - 1 - i) & 1) == 1) s.add(nums[i]);
            out.add(s);
        }
        return out;
    }

    public static void main(String[] args) {
        List<List<Integer>> want = List.of(List.of(1, 2, 3), List.of(1, 2), List.of(1, 3), List.of(1), List.of(2, 3), List.of(2), List.of(3), List.of());
        if (!subsets(new int[] {1, 2, 3}).equals(want)) throw new AssertionError("example 1");
        if (!subsets(new int[] {5}).equals(List.of(List.of(5), List.of()))) throw new AssertionError("example 2");
        Random rnd = new Random(19202);
        for (int t = 0; t < 2000; t++) {
            int n = rnd.nextInt(9);
            Set<Integer> used = new HashSet<>();
            int[] a = new int[n];
            for (int i = 0; i < n; i++) {
                int v;
                do { v = rnd.nextInt(21) - 10; } while (!used.add(v));
                a[i] = v;
            }
            if (!subsets(a).equals(oracle(a))) throw new AssertionError("differs on n=" + n);
        }
    }
}
```
