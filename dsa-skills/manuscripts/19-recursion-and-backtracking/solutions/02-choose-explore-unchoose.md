<!-- solutions-for: 02-choose-explore-unchoose -->
### Solutions For Undoing Each Choice

#### Solution: [Build] Binary Choices (Author exercise)
<!-- id: bt-binary-choices -->

**Approach.**
One `StringBuilder` holds the working path. A call at depth `d` appends `'0'`, explores depth `d + 1`, shortens the builder by one character and then repeats with `'1'`. At depth `n`, the call stores `toString()`, which copies the characters, so later edits cannot change the stored string. Because the call tries `'0'` before `'1'` at every depth, the strings appear in increasing order. The length of the builder equals the depth on entry and on exit of every call, which is the invariant of the search.

**Complexity.**
- **Time** is O(n * 2^n), because each of the 2^n leaves copies n characters and the 2^(n+1) - 1 calls cost O(1) each.
- **Space** is O(n) for the builder and the stack, plus O(n * 2^n) for the output.

```java run
import java.util.*;

public final class BinaryChoices {
    /**
     * Returns all binary strings of length n in increasing order.
     * Time: O(n * 2^n). Space: O(n) besides the output.
     * Invariant: the builder length equals the depth on entry and on exit of every call.
     */
    static List<String> all(int n) {
        List<String> out = new ArrayList<>();
        go(0, n, new StringBuilder(), out);
        return out;
    }

    private static void go(int depth, int n, StringBuilder sb, List<String> out) {
        if (depth == n) { out.add(sb.toString()); return; }     // toString copies, so the stored string is final
        for (char c = '0'; c <= '1'; c++) {                      // two candidates, 0 before 1
            sb.append(c);                                        // choose the character for this position
            go(depth + 1, n, sb, out);                           // explore the later positions
            sb.setLength(sb.length() - 1);                       // undo: drop the character just added
        }
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!all(2).equals(List.of("00", "01", "10", "11"))) throw new AssertionError("ex1");
        if (!all(0).equals(List.of(""))) throw new AssertionError("ex2");
        // Every n up to 12 must match counting in binary with padding.
        for (int n = 0; n <= 12; n++) {
            List<String> got = all(n);
            if (got.size() != (1 << n)) throw new AssertionError("size " + n);
            for (int m = 0; m < got.size(); m++) {
                String want = n == 0 ? "" : String.format("%" + n + "s", Integer.toBinaryString(m)).replace(' ', '0');
                if (!got.get(m).equals(want)) throw new AssertionError("n=" + n + " m=" + m);
            }
        }
        // The Java claim: toString copies, so a stored string survives later edits of the builder.
        StringBuilder sb = new StringBuilder("ab"); String s = sb.toString(); sb.setLength(0);
        if (!s.equals("ab")) throw new AssertionError("toString copy");
        System.out.println("ok");
    }
}
```

#### Solution: [Vary] Variable Candidate Loop (Author exercise)
<!-- id: bt-variable-candidate-loop -->

**Approach.**
The working state is one number, the sum of the entries chosen so far, so the search needs no list. A call at depth `d` loops over every option, adds it to the sum, explores depth `d + 1` and subtracts the same option. At depth `k`, the call counts 1 when the sum equals `target` and 0 otherwise. The subtraction restores the sum, so every option at one depth starts from the same sum. The empty sequence arises at `k = 0`, where the sum is 0 and the answer is 1 only for `target = 0`.

**Complexity.**
- **Time** is O(m^k), where `m` is the number of options, because the tree has m^k leaves and each call costs O(1) per option.
- **Space** is O(k) for the stack, and the search stores no list.

```java run
import java.util.*;

public final class VariableCandidateLoop {
    private static int sum;                                   // the working state: the sum of the chosen entries

    /**
     * Counts sequences of length k over options whose entries add up to target.
     * Time: O(m^k). Space: O(k) stack frames.
     * Invariant: on entry to each call, sum equals the sum of the choices of the calls above.
     */
    static int count(int[] options, int k, int target) {
        sum = 0;
        return go(0, options, k, target);
    }

    private static int go(int depth, int[] options, int k, int target) {
        if (depth == k) return sum == target ? 1 : 0;         // a full sequence counts when it reaches the target
        int total = 0;
        for (int v : options) {                              // several candidates at one depth
            sum += v;                                        // choose v
            total += go(depth + 1, options, k, target);      // explore the remaining positions
            sum -= v;                                        // undo: restore the sum for the next candidate
        }
        return total;
    }

    static int brute(int[] options, int k, int target) {
        int m = options.length, total = 0;
        long limit = 1;
        for (int i = 0; i < k; i++) limit *= m;
        for (long code = 0; code < limit; code++) {          // read the code as a base-m number
            long c = code; int s = 0;
            for (int i = 0; i < k; i++) { s += options[(int) (c % m)]; c /= m; }
            if (s == target) total++;
        }
        return total;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (count(new int[] {1, 2}, 3, 5) != 3) throw new AssertionError("ex1");
        if (count(new int[] {4}, 0, 4) != 0) throw new AssertionError("ex2");
        if (count(new int[] {4}, 0, 0) != 1) throw new AssertionError("empty sequence");
        // Random inputs must match the base-m enumeration.
        Random rnd = new Random(1912);
        for (int t = 0; t < 300; t++) {
            int m = 1 + rnd.nextInt(5);
            Set<Integer> set = new LinkedHashSet<>();
            while (set.size() < m) set.add(rnd.nextInt(19) - 9);
            int[] o = set.stream().mapToInt(Integer::intValue).toArray();
            int k = rnd.nextInt(6), target = rnd.nextInt(21) - 10;
            if (count(o, k, target) != brute(o, k, target)) throw new AssertionError("random " + t);
        }
        // After a search the shared sum is back at zero, which shows that every choice was undone.
        count(new int[] {3, 4}, 5, 17);
        if (sum != 0) throw new AssertionError("sum not restored");
        System.out.println("ok");
    }
}
```

#### Solution: [Boundary] Store A Completed Path (Author exercise)
<!-- id: bt-store-completed-path -->

**Approach.**
The search keeps one working list and a running sum. At depth `k`, a leaf with the right sum adds `new ArrayList<>(path)` to the result. The copy matters because `List.add` stores the reference. If the leaf stored `path` itself, the undo steps would empty that same list, and every stored entry would end as an empty list. For `k = 0`, the empty path is a leaf at once, so the result holds one empty list when `target` is 0. The undo step removes the last index, and the sum shrinks by the removed value.

**Complexity.**
- **Time** is O(k * m^k), where `m` is the number of options, because each leaf may copy k values.
- **Space** is O(k) for the path and the stack, plus the output.

```java run
import java.util.*;

public final class StoreCompletedPath {
    /**
     * Returns every sequence of length k over options that adds up to target, in search order.
     * Time: O(k * m^k). Space: O(k) besides the output.
     * Invariant: the path holds exactly the choices of the active calls, and sum is their total.
     */
    static List<List<Integer>> collect(int[] options, int k, int target) {
        List<List<Integer>> out = new ArrayList<>();
        go(0, 0, options, k, target, new ArrayList<>(), out);
        return out;
    }

    private static void go(int depth, int sum, int[] options, int k, int target, List<Integer> path, List<List<Integer>> out) {
        if (depth == k) {
            if (sum == target) out.add(new ArrayList<>(path));   // copy: the path keeps changing after this call
            return;
        }
        for (int v : options) {                                  // options are tried from left to right
            path.add(v);                                         // choose v
            go(depth + 1, sum + v, options, k, target, path, out);   // explore with the larger sum
            path.remove(path.size() - 1);                        // undo: remove the last index, not a value
        }
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!collect(new int[] {1, 2}, 2, 3).equals(List.of(List.of(1, 2), List.of(2, 1)))) throw new AssertionError("ex1");
        if (!collect(new int[] {5}, 0, 0).equals(List.of(List.of()))) throw new AssertionError("ex2");
        if (!collect(new int[] {5}, 0, 1).isEmpty()) throw new AssertionError("empty result");
        // Random inputs must match a base-m enumeration in the same order.
        Random rnd = new Random(1913);
        for (int t = 0; t < 300; t++) {
            int m = 1 + rnd.nextInt(4);
            Set<Integer> set = new LinkedHashSet<>();
            while (set.size() < m) set.add(rnd.nextInt(19) - 9);
            int[] o = set.stream().mapToInt(Integer::intValue).toArray();
            int k = rnd.nextInt(5), target = rnd.nextInt(21) - 10;
            List<List<Integer>> want = new ArrayList<>();
            long limit = 1; for (int i = 0; i < k; i++) limit *= m;
            for (long code = 0; code < limit; code++) {          // the most significant digit is the first position
                int[] digit = new int[k]; long c = code;
                for (int i = k - 1; i >= 0; i--) { digit[i] = (int) (c % m); c /= m; }
                List<Integer> seq = new ArrayList<>(); int s = 0;
                for (int i = 0; i < k; i++) { seq.add(o[digit[i]]); s += o[digit[i]]; }
                if (s == target) want.add(seq);
            }
            if (!collect(o, k, target).equals(want)) throw new AssertionError("random " + t);
        }
        // The Java claim: List.add stores the reference, so a stored path changes with the original.
        List<Integer> p = new ArrayList<>(List.of(1)); List<List<Integer>> store = new ArrayList<>();
        store.add(p); p.clear();
        if (!store.get(0).isEmpty()) throw new AssertionError("alias");
        // The Java claim: remove(int) removes an index and remove(Object) removes a value.
        List<Integer> q = new ArrayList<>(List.of(7, 8, 9)); q.remove(1);
        if (!q.equals(List.of(7, 9))) throw new AssertionError("remove index");
        q.remove(Integer.valueOf(9));
        if (!q.equals(List.of(7))) throw new AssertionError("remove value");
        System.out.println("ok");
    }
}
```

#### Solution: [Recognize] Subsets (LeetCode 78)
<!-- id: bt-subsets-include-exclude -->

**Approach.**
Each subset corresponds to one decision per index, so the depth equals the index of the next value to decide. A call at index `i` first explores the branch that excludes `nums[i]`, which changes no state. It then adds `nums[i]` to the working list, explores the branch that includes it and removes the value. At index `n`, the call stores a copy of the working list. Because the exclude branch runs first, the result lists the empty subset first and the full set last. The working list holds the included values among the first `i` positions.

**Complexity.**
- **Time** is O(n * 2^n), because there are 2^n leaves and each copies up to n values.
- **Space** is O(n) for the list and the stack, plus the output.

```java run
import java.util.*;

public final class SubsetsIncludeExclude {
    /**
     * Returns all subsets of nums, trying exclusion before inclusion at each index.
     * Time: O(n * 2^n). Space: O(n) besides the output.
     * Invariant: at index i, the path holds the included values among nums[0..i).
     */
    static List<List<Integer>> subsets(int[] nums) {
        List<List<Integer>> out = new ArrayList<>();
        go(0, nums, new ArrayList<>(), out);
        return out;
    }

    private static void go(int i, int[] nums, List<Integer> path, List<List<Integer>> out) {
        if (i == nums.length) { out.add(new ArrayList<>(path)); return; }   // all decisions made: store a copy
        go(i + 1, nums, path, out);                          // exclude nums[i]: the path stays as it is
        path.add(nums[i]);                                   // choose to include nums[i]
        go(i + 1, nums, path, out);                          // explore the later indices
        path.remove(path.size() - 1);                        // undo: remove the last entry by index
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!subsets(new int[] {1, 2}).equals(List.of(List.of(), List.of(2), List.of(1), List.of(1, 2)))) throw new AssertionError("ex1");
        if (!subsets(new int[] {}).equals(List.of(List.of()))) throw new AssertionError("ex2");
        // Random inputs must match a bitmask enumeration whose first index is the highest bit.
        Random rnd = new Random(1914);
        for (int t = 0; t < 300; t++) {
            int n = rnd.nextInt(9);
            Set<Integer> set = new LinkedHashSet<>();
            while (set.size() < n) set.add(rnd.nextInt(21) - 10);
            int[] a = set.stream().mapToInt(Integer::intValue).toArray();
            List<List<Integer>> want = new ArrayList<>();
            for (int mask = 0; mask < (1 << n); mask++) {
                List<Integer> s = new ArrayList<>();
                for (int i = 0; i < n; i++) if ((mask >> (n - 1 - i) & 1) == 1) s.add(a[i]);
                want.add(s);
            }
            if (!subsets(a).equals(want)) throw new AssertionError("random " + t);
        }
        // The input must stay unchanged.
        int[] keep = {3, 1, 2}; subsets(keep);
        if (!Arrays.equals(keep, new int[] {3, 1, 2})) throw new AssertionError("mutation");
        System.out.println("ok");
    }
}
```
