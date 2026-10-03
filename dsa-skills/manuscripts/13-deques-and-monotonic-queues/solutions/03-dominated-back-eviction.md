<!-- solutions-for: 03-dominated-back-eviction -->
### Dominated-Back Eviction

#### Solution: [Build] Insert Maximum Candidate (Author exercise)
<!-- id: dq-insert-maximum-candidate -->

**Approach.** Keep a deque of indices. At step `i`, pop from the back while the value at the back index is strictly smaller than `a[i]`, count the pops, and append `i`. The count for the step is the answer entry. The assertions check both examples, compare the counts with a definition-based oracle that says index `j < i` is removed exactly at the first later step whose value strictly exceeds it, and confirm the amortized claim: the counts over the whole run add up to at most `n`, since each index is removed at most once.

**Complexity.** O(n) time overall and O(n) memory in the worst case.

```java run
import java.util.ArrayDeque;
import java.util.Arrays;
import java.util.Random;

public final class InsertMaximumCandidate {
    static int[] removedCounts(int[] a) {
        int[] out = new int[a.length];
        ArrayDeque<Integer> d = new ArrayDeque<>();
        for (int i = 0; i < a.length; i++) {
            while (!d.isEmpty() && a[d.peekLast()] < a[i]) { d.removeLast(); out[i]++; }
            d.addLast(i);
        }
        return out;
    }
    static int[] oracle(int[] a) {
        int[] out = new int[a.length];
        for (int j = 0; j < a.length; j++)
            for (int i = j + 1; i < a.length; i++)
                if (a[i] > a[j]) { out[i]++; break; }
        return out;
    }

    public static void main(String[] args) {
        if (!Arrays.equals(removedCounts(new int[]{6, 1, 3, 3, 8, 2, 5}), new int[]{0, 0, 1, 0, 3, 0, 1})) throw new AssertionError("example 1");
        if (!Arrays.equals(removedCounts(new int[]{4, 4, 4}), new int[]{0, 0, 0})) throw new AssertionError("example 2");
        Random rnd = new Random(1321);
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(16);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(6);
            int[] got = removedCounts(a);
            if (!Arrays.equals(got, oracle(a))) throw new AssertionError("disagrees with the definition on " + Arrays.toString(a));
            if (Arrays.stream(got).sum() > n) throw new AssertionError("each index is removed at most once");
        }
    }
}
```

#### Solution: [Vary] Insert Minimum Candidate (Author exercise)
<!-- id: dq-insert-minimum-candidate -->

**Approach.** Reverse the comparison: pop from the back while the back value is strictly larger than the new value, then append the new index. For minima it is the larger older values that a newcomer outlasts and beats, while a smaller older value is the better one and must stay. The assertions check both examples, compare the final contents with the definition that an index survives exactly when no later value is strictly smaller, and show that applying the maximum rule to a minimum question loses the answer on `[3, 1, 2]`.

**Complexity.** O(n) time and O(n) memory in the worst case.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

public final class InsertMinimumCandidate {
    static List<Integer> finalIndices(int[] a, boolean minimumRule) {
        ArrayDeque<Integer> d = new ArrayDeque<>();
        for (int i = 0; i < a.length; i++) {
            while (!d.isEmpty() && (minimumRule ? a[d.peekLast()] > a[i] : a[d.peekLast()] < a[i])) d.removeLast();
            d.addLast(i);
        }
        return new ArrayList<>(d);
    }
    static List<Integer> oracle(int[] a) {
        List<Integer> out = new ArrayList<>();
        for (int i = 0; i < a.length; i++) {
            boolean survives = true;
            for (int j = i + 1; j < a.length; j++) if (a[j] < a[i]) survives = false;
            if (survives) out.add(i);
        }
        return out;
    }

    public static void main(String[] args) {
        if (!finalIndices(new int[]{6, 1, 3, 3, 8, 2, 5}, true).equals(Arrays.asList(1, 5, 6))) throw new AssertionError("example 1");
        if (!finalIndices(new int[]{9, 8, 7}, true).equals(Arrays.asList(2))) throw new AssertionError("example 2");
        int[] w = {3, 1, 2};
        List<Integer> wrong = finalIndices(w, false);
        if (a0(w, wrong) == 1) throw new AssertionError("the maximum rule should not keep the minimum at the front");
        Random rnd = new Random(1322);
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(16);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(6);
            if (!finalIndices(a, true).equals(oracle(a))) throw new AssertionError("disagrees with the definition on " + Arrays.toString(a));
        }
    }
    static int a0(int[] a, List<Integer> deque) { return a[deque.get(0)]; }
}
```

#### Solution: [Boundary] Repeated Equal Values (Author exercise)
<!-- id: dq-repeated-equal-values -->

**Approach.** Run the same maximum loop twice, once popping strictly smaller values and once popping smaller or equal values, and record the largest size reached. A run of equal values is never popped under keep equals, so the deque grows to the length of the run, and under keep newest each arrival pops the previous equal value, so the size stays at 1. The answer of a window query does not depend on the policy, which the assertions check by running a sliding-window maximum with both policies against a brute force, with the front expired by index, so that either policy can be used when entries leave in arrival order.

**Complexity.** O(n) time and O(n) memory.

```java run
import java.util.ArrayDeque;
import java.util.Arrays;
import java.util.Random;

public final class RepeatedEqualValues {
    static int[] peakSizes(int[] a) {
        int[] peak = new int[2];
        for (int policy = 0; policy < 2; policy++) {
            ArrayDeque<Integer> d = new ArrayDeque<>();
            for (int i = 0; i < a.length; i++) {
                while (!d.isEmpty() && (policy == 0 ? a[d.peekLast()] < a[i] : a[d.peekLast()] <= a[i])) d.removeLast();
                d.addLast(i);
                peak[policy] = Math.max(peak[policy], d.size());
            }
        }
        return peak;
    }
    static int[] windowMax(int[] a, int k, boolean replaceEquals) {
        int[] out = new int[a.length - k + 1];
        ArrayDeque<Integer> d = new ArrayDeque<>();
        for (int i = 0; i < a.length; i++) {
            while (!d.isEmpty() && d.peekFirst() <= i - k) d.removeFirst();
            while (!d.isEmpty() && (replaceEquals ? a[d.peekLast()] <= a[i] : a[d.peekLast()] < a[i])) d.removeLast();
            d.addLast(i);
            if (i >= k - 1) out[i - k + 1] = a[d.peekFirst()];
        }
        return out;
    }
    static int[] brute(int[] a, int k) {
        int[] out = new int[a.length - k + 1];
        for (int s = 0; s + k <= a.length; s++) {
            int m = Integer.MIN_VALUE;
            for (int j = s; j < s + k; j++) m = Math.max(m, a[j]);
            out[s] = m;
        }
        return out;
    }

    public static void main(String[] args) {
        if (!Arrays.equals(peakSizes(new int[]{7, 7, 7, 7, 7}), new int[]{5, 1})) throw new AssertionError("example 1");
        if (!Arrays.equals(peakSizes(new int[]{1, 2, 3}), new int[]{1, 1})) throw new AssertionError("example 2");
        Random rnd = new Random(1323);
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(16);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(3);
            int[] p = peakSizes(a);
            if (p[1] > p[0]) throw new AssertionError("keeping only the newest never needs more room");
            int k = 1 + rnd.nextInt(n);
            if (!Arrays.equals(windowMax(a, k, false), brute(a, k)) || !Arrays.equals(windowMax(a, k, true), brute(a, k)))
                throw new AssertionError("both policies must give the window maxima on " + Arrays.toString(a) + " k=" + k);
        }
    }
}
```

#### Solution: [Recognize] Online Suffix Maximum Candidates (Author exercise)
<!-- id: dq-online-suffix-maximum -->

**Approach.** Maintain a deque of indices with the strictly smaller removal. After each arrival the front holds the largest value so far and the size is the number of candidates, which are the indices that no later value so far strictly exceeds. Both numbers are read in constant time after the insertion. The assertions compare each pair with a direct computation on the prefix, where the maximum is a scan and the candidate count is the number of indices with no strictly larger value after them, and check both examples.

**Complexity.** O(1) amortized per arrival and O(n) memory in the worst case.

```java run
import java.util.ArrayDeque;
import java.util.Arrays;
import java.util.Random;

public final class OnlineSuffixMaximum {
    static int[][] report(int[] a) {
        int[][] out = new int[a.length][2];
        ArrayDeque<Integer> d = new ArrayDeque<>();
        for (int i = 0; i < a.length; i++) {
            while (!d.isEmpty() && a[d.peekLast()] < a[i]) d.removeLast();
            d.addLast(i);
            out[i][0] = a[d.peekFirst()];
            out[i][1] = d.size();
        }
        return out;
    }
    static int[][] oracle(int[] a) {
        int[][] out = new int[a.length][2];
        for (int i = 0; i < a.length; i++) {
            int max = Integer.MIN_VALUE, count = 0;
            for (int j = 0; j <= i; j++) {
                max = Math.max(max, a[j]);
                boolean candidate = true;
                for (int k = j + 1; k <= i; k++) if (a[k] > a[j]) candidate = false;
                if (candidate) count++;
            }
            out[i][0] = max;
            out[i][1] = count;
        }
        return out;
    }

    public static void main(String[] args) {
        int[][] want1 = {{2, 1}, {8, 1}, {8, 2}, {8, 3}, {8, 4}, {9, 1}, {9, 2}};
        if (!Arrays.deepEquals(report(new int[]{2, 8, 3, 3, 1, 9, 4}), want1)) throw new AssertionError("example 1");
        int[][] want2 = {{7, 1}, {7, 2}, {7, 3}};
        if (!Arrays.deepEquals(report(new int[]{7, 5, 5}), want2)) throw new AssertionError("example 2");
        Random rnd = new Random(1324);
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(14);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(6) - 2;
            if (!Arrays.deepEquals(report(a), oracle(a))) throw new AssertionError("disagrees with the prefix definition on " + Arrays.toString(a));
        }
    }
}
```
