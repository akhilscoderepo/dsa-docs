<!-- solutions-for: 02-front-and-back-invariants -->
### Front And Back Invariants

#### Solution: [Build] Decreasing Candidate Values (Author exercise)
<!-- id: dq-decreasing-candidate-values -->

**Approach.** For each value, remove from the back while the back is strictly smaller, then append the value. The loop stops at the first back entry that is at least as large, which is what keeps the values non-increasing from front to back, and because equal values are not removed they stay in the list. The assertions check both examples, check after every step that the contents never increase from front to back, and compare the final front with a direct maximum scan, which is the claim that the front is the best survivor.

**Complexity.** O(n) time, since each value is appended once and removed at most once, and O(n) memory in the worst case.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

public final class DecreasingCandidateValues {
    static List<Integer> contents(int[] stream) {
        ArrayDeque<Integer> d = new ArrayDeque<>();
        int max = Integer.MIN_VALUE;
        for (int v : stream) {
            while (!d.isEmpty() && d.peekLast() < v) d.removeLast();
            d.addLast(v);
            max = Math.max(max, v);
            int prev = Integer.MAX_VALUE;
            for (int x : d) {
                if (x > prev) throw new AssertionError("values must not increase from front to back");
                prev = x;
            }
            if (d.peekFirst() != max) throw new AssertionError("the front must be the best survivor");
        }
        return new ArrayList<>(d);
    }

    public static void main(String[] args) {
        if (!contents(new int[]{4, 2, 7, 3, 3, 1, 6}).equals(Arrays.asList(7, 6))) throw new AssertionError("example 1");
        if (!contents(new int[]{5, 5, 5}).equals(Arrays.asList(5, 5, 5))) throw new AssertionError("example 2");
        if (!contents(new int[]{}).isEmpty()) throw new AssertionError("an empty stream gives an empty deque");
        Random rnd = new Random(1311);
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(16);
            int[] s = new int[n];
            for (int i = 0; i < n; i++) s[i] = rnd.nextInt(7) - 3;
            List<Integer> got = contents(s);
            List<Integer> expected = new ArrayList<>();
            for (int i = 0; i < n; i++) {
                boolean survives = true;
                for (int j = i + 1; j < n; j++) if (s[j] > s[i]) survives = false;
                if (survives) expected.add(s[i]);
            }
            if (!got.equals(expected)) throw new AssertionError("a value survives exactly when nothing later is larger: " + Arrays.toString(s));
        }
    }
}
```

#### Solution: [Vary] Increasing Candidate Values (Author exercise)
<!-- id: dq-increasing-candidate-values -->

**Approach.** Reverse the one comparison: remove from the back while the back is strictly larger than the new value, then append. The contents then never decrease from front to back, so the front is the smallest survivor. Nothing else changes, and the cost is the same. The assertions check both examples, check the order and the front after every step, and compare the final contents with the definition that a value survives exactly when no later value is smaller.

**Complexity.** O(n) time and O(n) memory in the worst case.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

public final class IncreasingCandidateValues {
    static List<Integer> contents(int[] stream) {
        ArrayDeque<Integer> d = new ArrayDeque<>();
        int min = Integer.MAX_VALUE;
        for (int v : stream) {
            while (!d.isEmpty() && d.peekLast() > v) d.removeLast();
            d.addLast(v);
            min = Math.min(min, v);
            int prev = Integer.MIN_VALUE;
            for (int x : d) {
                if (x < prev) throw new AssertionError("values must not decrease from front to back");
                prev = x;
            }
            if (d.peekFirst() != min) throw new AssertionError("the front must be the smallest survivor");
        }
        return new ArrayList<>(d);
    }

    public static void main(String[] args) {
        if (!contents(new int[]{4, 2, 7, 3, 3, 1, 6}).equals(Arrays.asList(1, 6))) throw new AssertionError("example 1");
        if (!contents(new int[]{9, 8, 7}).equals(Arrays.asList(7))) throw new AssertionError("example 2");
        Random rnd = new Random(1312);
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(16);
            int[] s = new int[n];
            for (int i = 0; i < n; i++) s[i] = rnd.nextInt(7) - 3;
            List<Integer> got = contents(s);
            List<Integer> expected = new ArrayList<>();
            for (int i = 0; i < n; i++) {
                boolean survives = true;
                for (int j = i + 1; j < n; j++) if (s[j] < s[i]) survives = false;
                if (survives) expected.add(s[i]);
            }
            if (!got.equals(expected)) throw new AssertionError("a value survives exactly when nothing later is smaller: " + Arrays.toString(s));
        }
    }
}
```

#### Solution: [Boundary] Equal Candidate Policy (Author exercise)
<!-- id: dq-equal-candidate-policy -->

**Approach.** Store indices and run the same loop twice with different back tests: strictly smaller values leave under keep equals, and smaller or equal values leave under replace equals. Both policies leave a front with the same value at every step, because a removed equal value is never needed while its newer copy is alive, but replace equals keeps only the newest of a tie, which is the one that expires last. The assertions check the examples, compare the front values of the two policies after every step, check that replace equals is a subsequence of keep equals, and for a value that appears several times, check that the newest copy is always present in both.

**Complexity.** O(n) time and O(n) memory.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

public final class EqualCandidatePolicy {
    static List<Integer> run(int[] s, boolean replaceEquals, int[] fronts) {
        ArrayDeque<Integer> d = new ArrayDeque<>();
        for (int i = 0; i < s.length; i++) {
            while (!d.isEmpty() && (replaceEquals ? s[d.peekLast()] <= s[i] : s[d.peekLast()] < s[i])) d.removeLast();
            d.addLast(i);
            if (fronts != null) fronts[i] = s[d.peekFirst()];
        }
        return new ArrayList<>(d);
    }

    public static void main(String[] args) {
        int[] ex1 = {2, 2, 1, 2};
        if (!run(ex1, false, null).equals(Arrays.asList(0, 1, 3)) || !run(ex1, true, null).equals(Arrays.asList(3))) throw new AssertionError("example 1");
        int[] ex2 = {5};
        if (!run(ex2, false, null).equals(Arrays.asList(0)) || !run(ex2, true, null).equals(Arrays.asList(0))) throw new AssertionError("example 2");
        Random rnd = new Random(1313);
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(14);
            int[] s = new int[n];
            for (int i = 0; i < n; i++) s[i] = rnd.nextInt(4);
            int[] fa = new int[n], fb = new int[n];
            List<Integer> keep = run(s, false, fa);
            List<Integer> replace = run(s, true, fb);
            if (!Arrays.equals(fa, fb)) throw new AssertionError("both policies give the same front value at every step");
            if (!keep.containsAll(replace)) throw new AssertionError("replace equals keeps a subset of keep equals");
            if (!keep.contains(n - 1) || !replace.contains(n - 1)) throw new AssertionError("the newest index is always present");
            int last = -1;
            for (int idx : replace) {
                if (idx <= last) throw new AssertionError("indices stay in chronological order");
                last = idx;
            }
        }
    }
}
```

#### Solution: [Recognize] Name Each End (Author exercise)
<!-- id: dq-name-each-end -->

**Approach.** Parse each entry. An entry whose index is at most `right - k` is old, so its reason is expiration, and expiration is only legitimate at the front. An entry with a larger index is still inside the window, so its reason is domination, and domination is only legitimate at the back. If the side does not match the reason, the label is `invalid`. The comparison is done in `long` arithmetic so that `right - k` cannot misbehave. The assertions check the examples and then generate logs from real sliding-window runs, confirming that every entry of a genuine run is labelled by the rule with no `invalid`, and that moving any entry to the wrong side produces `invalid`.

**Complexity.** O(m) time for `m` entries and O(m) memory for the labels.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

public final class NameEachEnd {
    static List<String> label(int k, String[] log) {
        List<String> out = new ArrayList<>();
        for (String entry : log) {
            String[] p = entry.split(" ");
            char side = p[0].charAt(0);
            long index = Long.parseLong(p[1]);
            long right = Long.parseLong(p[2]);
            boolean expired = index <= right - k;
            if (expired) out.add(side == 'F' ? "expired" : "invalid");
            else out.add(side == 'B' ? "dominated" : "invalid");
        }
        return out;
    }
    static List<String> genuineLog(int[] a, int k, List<String> expectedLabels) {
        ArrayDeque<Integer> d = new ArrayDeque<>();
        List<String> log = new ArrayList<>();
        for (int r = 0; r < a.length; r++) {
            while (!d.isEmpty() && d.peekFirst() <= r - k) { log.add("F " + d.removeFirst() + " " + r); expectedLabels.add("expired"); }
            while (!d.isEmpty() && a[d.peekLast()] < a[r]) { log.add("B " + d.removeLast() + " " + r); expectedLabels.add("dominated"); }
            d.addLast(r);
        }
        return log;
    }

    public static void main(String[] args) {
        if (!label(3, new String[]{"B 0 1", "F 1 4", "B 3 4", "B 2 4"}).equals(Arrays.asList("dominated", "expired", "dominated", "dominated"))) throw new AssertionError("example 1");
        if (!label(3, new String[]{"F 2 3"}).equals(Arrays.asList("invalid"))) throw new AssertionError("example 2");
        Random rnd = new Random(1314);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(14);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(6);
            int k = 1 + rnd.nextInt(5);
            List<String> expected = new ArrayList<>();
            List<String> log = genuineLog(a, k, expected);
            if (!label(k, log.toArray(new String[0])).equals(expected)) throw new AssertionError("a genuine run is labelled by the rule");
            for (int i = 0; i < log.size(); i++) {
                String[] flipped = log.toArray(new String[0]);
                flipped[i] = (flipped[i].charAt(0) == 'F' ? "B" : "F") + flipped[i].substring(1);
                if (!label(k, flipped).get(i).equals("invalid")) throw new AssertionError("a wrong side must be invalid");
            }
        }
    }
}
```
