<!-- solutions-for: 07-index-expiry -->
### Solutions For The Recent Position Exercises

#### Solution: [Build] Best Of Last K Scores (Author exercise)
<!-- id: dq-best-of-last-k -->

**Approach.**

For each position the method first removes front positions below `i - k`, so every stored position is eligible. It then reads the front as the answer, because the new position must not see itself. After the read, it removes weaker scores from the back and appends `i`. The invariant at the read is that the stored positions are exactly the eligible positions that no newer eligible position beats. The assertions compare the output with a direct scan of the previous `k` scores on random arrays.

**Complexity.**

- **Time** is O(n), as the loop appends each position one time and removes it at most one time.
- **Space** is O(k) for the deque, and the output holds n entries.

```java run
import java.util.*;

public final class BestOfLastK {
    /**
     * Returns the best score among the previous k positions for every position, or -1.
     * Time: O(n). Space: O(k) plus the output.
     * Invariant at the read: stored positions are eligible and not beaten by a newer eligible position.
     */
    static int[] best(int[] scores, int k) {
        int[] out = new int[scores.length];
        Deque<Integer> d = new ArrayDeque<>();
        for (int i = 0; i < scores.length; i++) {                          // one query per position
            while (!d.isEmpty() && d.peekFirst() < i - k) d.pollFirst();   // 1: age test
            out[i] = d.isEmpty() ? -1 : scores[d.peekFirst()];             // 2: read before the append
            while (!d.isEmpty() && scores[d.peekLast()] < scores[i]) d.pollLast(); // 3: weaker scores leave
            d.addLast(i);                                                  // 4: append
        }
        return out;
    }

    public static void main(String[] args) {
        // Worked examples.
        if (!Arrays.equals(best(new int[]{5, 3, 6, 2, 4, 1, 7}, 3), new int[]{-1, 5, 5, 6, 6, 6, 4})) throw new AssertionError("example 1");
        if (!Arrays.equals(best(new int[]{9, 1, 1}, 1), new int[]{-1, 9, 1})) throw new AssertionError("example 2");
        // A single position has no eligible position.
        if (!Arrays.equals(best(new int[]{4}, 3), new int[]{-1})) throw new AssertionError("single");
        // Random arrays agree with a direct scan of the previous k scores.
        Random rnd = new Random(21);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(25), k = 1 + rnd.nextInt(8);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(8);
            int[] got = best(a, k);
            for (int i = 0; i < n; i++) {
                int want = -1;
                for (int j = Math.max(0, i - k); j < i; j++) want = Math.max(want, a[j]);
                if (got[i] != want) throw new AssertionError("position " + i);
            }
        }
    }
}
```

#### Solution: [Vary] Variable Legal Left Bound (Author exercise)
<!-- id: dq-variable-bound -->

**Approach.**

The age test compares the front with the supplied bound for the current position. A loop is needed, because a bound that jumps expires several positions at once. The read and the removals follow the same order as in the first exercise. The invariant is that every stored position is at least `bound[i]` at the read. The assertions compare the output with a direct scan between the bound and the previous position, and they include bounds that jump over several stored positions.

**Complexity.**

- **Time** is O(n), because each position is appended once and expires at most once.
- **Space** is O(n) when the bound never moves, since every position then stays eligible.

```java run
import java.util.*;

public final class VariableBound {
    /**
     * Returns the best eligible score for each position, using a supplied left bound.
     * Time: O(n). Space: O(n). Invariant at the read: every stored position is at least bound[i].
     */
    static int[] best(int[] scores, int[] bound) {
        int[] out = new int[scores.length];
        Deque<Integer> d = new ArrayDeque<>();
        for (int i = 0; i < scores.length; i++) {                           // one query per position
            while (!d.isEmpty() && d.peekFirst() < bound[i]) d.pollFirst(); // a loop, because a jump can expire many
            out[i] = d.isEmpty() ? -1 : scores[d.peekFirst()];              // read before the append
            while (!d.isEmpty() && scores[d.peekLast()] < scores[i]) d.pollLast();
            d.addLast(i);
        }
        return out;
    }

    public static void main(String[] args) {
        // Worked examples.
        if (!Arrays.equals(best(new int[]{4, 8, 2, 6}, new int[]{0, 0, 1, 2}), new int[]{-1, 4, 8, 2})) throw new AssertionError("example 1");
        if (!Arrays.equals(best(new int[]{3, 3, 3}, new int[]{0, 0, 1}), new int[]{-1, 3, 3})) throw new AssertionError("example 2");
        // A bound equal to the position leaves nothing eligible.
        if (!Arrays.equals(best(new int[]{5, 6}, new int[]{0, 1}), new int[]{-1, -1})) throw new AssertionError("bound at i - 1");
        // Random bounds agree with a direct scan.
        Random rnd = new Random(22);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(20);
            int[] a = new int[n], b = new int[n];
            int cur = 0;
            for (int i = 0; i < n; i++) { a[i] = rnd.nextInt(8); cur = Math.min(i, cur + rnd.nextInt(3)); b[i] = cur; }
            int[] got = best(a, b);
            for (int i = 0; i < n; i++) {
                int want = -1;
                for (int j = b[i]; j < i; j++) want = Math.max(want, a[j]);
                if (got[i] != want) throw new AssertionError("position " + i);
            }
        }
    }
}
```

#### Solution: [Boundary] Duplicate Values, Different Ages (Author exercise)
<!-- id: dq-duplicate-ages -->

**Approach.**

Equal scores must keep their separate ages, so the deque stores positions. The back removes entries whose score is smaller or equal, so only the newest copy of an equal score stays. The newest copy expires last, so the front is the largest position among equal best scores. The invariant at the read is that the front holds the newest eligible position of the best score. The assertions compare the output with a scan that picks the largest position among the maxima, on arrays with many ties.

**Complexity.**

- **Time** is O(n), since each position enters the deque one time and leaves it at most one time.
- **Space** is O(k), since the age test keeps the deque inside one distance, plus n output entries.

```java run
import java.util.*;

public final class DuplicateAges {
    /**
     * Returns the largest position that holds the best eligible score, or -1.
     * Time: O(n). Space: O(k) plus the output.
     * Invariant at the read: the front is the newest eligible position of the best score.
     */
    static int[] bestPositions(int[] scores, int k) {
        int[] out = new int[scores.length];
        Deque<Integer> d = new ArrayDeque<>();
        for (int i = 0; i < scores.length; i++) {                           // one query per position
            while (!d.isEmpty() && d.peekFirst() < i - k) d.pollFirst();    // expire by position, not by value
            out[i] = d.isEmpty() ? -1 : d.peekFirst();                      // read before the append
            while (!d.isEmpty() && scores[d.peekLast()] <= scores[i]) d.pollLast(); // equal scores are replaced
            d.addLast(i);
        }
        return out;
    }

    public static void main(String[] args) {
        // Worked examples.
        if (!Arrays.equals(bestPositions(new int[]{4, 4, 1, 1}, 2), new int[]{-1, 0, 1, 1})) throw new AssertionError("example 1");
        if (!Arrays.equals(bestPositions(new int[]{2, 2, 2}, 1), new int[]{-1, 0, 1})) throw new AssertionError("example 2");
        // Random arrays with many ties agree with a scan for the largest maximum position.
        Random rnd = new Random(23);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(20), k = 1 + rnd.nextInt(6);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(3);
            int[] got = bestPositions(a, k);
            for (int i = 0; i < n; i++) {
                int want = -1;
                for (int j = Math.max(0, i - k); j < i; j++) if (want == -1 || a[j] >= a[want]) want = j;
                if (got[i] != want) throw new AssertionError("position " + i);
            }
        }
    }
}
```

#### Solution: [Recognize] LC 1696 Jump Game VI (LeetCode 1696)
<!-- id: dq-lc1696 -->

**Approach.**

Let the score of position `i` be the best sum of a walk that ends at `i`. That score is `nums[i]` plus the best score among positions `i - k` through `i - 1`. The deque stores positions ordered by score, and the front gives the best earlier score in constant time. The method expires positions below `i - k`, reads the front, computes the score and removes entries whose score is not larger. The invariant at the read is that the front holds the best score among eligible positions. The assertions compare the result with a quadratic version that checks every earlier position.

**Complexity.**

- **Time** is O(n), because every position is appended once and removed at most one time.
- **Space** is O(n), since the score array holds one entry per position.

```java run
import java.util.*;

public final class Lc1696 {
    /**
     * Returns the best score of a walk from position 0 to the last position.
     * Time: O(n). Space: O(n). Invariant at the read: the front is the best score among eligible positions.
     */
    static int maxResult(int[] nums, int k) {
        int n = nums.length;
        int[] score = new int[n];
        score[0] = nums[0];
        Deque<Integer> d = new ArrayDeque<>();
        d.addLast(0);
        for (int i = 1; i < n; i++) {                                      // one score per position
            while (d.peekFirst() < i - k) d.pollFirst();                   // the previous position keeps the deque non-empty
            score[i] = nums[i] + score[d.peekFirst()];                     // best earlier score plus the own value
            while (!d.isEmpty() && score[d.peekLast()] <= score[i]) d.pollLast(); // a better newer score outlasts it
            d.addLast(i);
        }
        return score[n - 1];
    }

    /** Quadratic oracle: check every earlier position within k. */
    static int oracle(int[] nums, int k) {
        int n = nums.length;
        int[] s = new int[n];
        s[0] = nums[0];
        for (int i = 1; i < n; i++) {
            int best = Integer.MIN_VALUE;
            for (int j = Math.max(0, i - k); j < i; j++) best = Math.max(best, s[j]);
            s[i] = nums[i] + best;
        }
        return s[n - 1];
    }

    public static void main(String[] args) {
        // Worked examples.
        if (maxResult(new int[]{3, -2, 4, -1, 2, -5, 6}, 3) != 15) throw new AssertionError("example 1");
        if (maxResult(new int[]{-5, -3, -1}, 1) != -9) throw new AssertionError("example 2");
        // A single position and a distance that covers everything.
        if (maxResult(new int[]{7}, 1) != 7) throw new AssertionError("single");
        if (maxResult(new int[]{1, -9, -9, 2}, 3) != 3) throw new AssertionError("long jump");
        // Random arrays agree with the oracle.
        Random rnd = new Random(24);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(20), k = 1 + rnd.nextInt(n);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(21) - 10;
            if (maxResult(a, k) != oracle(a, k)) throw new AssertionError(Arrays.toString(a) + " k=" + k);
        }
    }
}
```
