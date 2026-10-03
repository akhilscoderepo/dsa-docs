<!-- solutions-for: 04-expired-front-eviction -->
### Expired-Front Eviction

#### Solution: [Build] Expire One Window (Author exercise)
<!-- id: dq-expire-one-window -->

**Approach.** Append index `r`, then test the front against `r - k`: if the front index is at most `r - k`, it is outside the window and is removed once. Because every index arrives exactly once and the window slides by one, at most one index can expire per arrival, so an `if` is enough, and the front afterward is `max(0, r - k + 1)`. The assertions check both examples against that closed form on random sizes, and show that the same single `if` fails as soon as the boundary can jump by two indices, which is why the next rung needs a loop.

**Complexity.** O(n) time, as each index is appended once and removed at most once, and O(k) memory.

```java run
import java.util.ArrayDeque;
import java.util.Arrays;
import java.util.Random;

public final class ExpireOneWindow {
    static int[] fronts(int n, int k) {
        int[] out = new int[n];
        ArrayDeque<Integer> d = new ArrayDeque<>();
        for (int r = 0; r < n; r++) {
            d.addLast(r);
            if (d.peekFirst() <= r - k) d.removeFirst();
            out[r] = d.peekFirst();
        }
        return out;
    }
    static boolean ifSufficesForJump(int[] legalLeft) {
        ArrayDeque<Integer> d = new ArrayDeque<>();
        for (int r = 0; r < legalLeft.length; r++) {
            d.addLast(r);
            if (!d.isEmpty() && d.peekFirst() < legalLeft[r]) d.removeFirst();
            if (d.peekFirst() < legalLeft[r]) return false;
        }
        return true;
    }

    public static void main(String[] args) {
        if (!Arrays.equals(fronts(6, 3), new int[]{0, 0, 0, 1, 2, 3})) throw new AssertionError("example 1");
        if (!Arrays.equals(fronts(2, 5), new int[]{0, 0})) throw new AssertionError("example 2");
        if (ifSufficesForJump(new int[]{0, 0, 1, 3, 3, 5})) throw new AssertionError("a single if cannot expire two indices at once");
        Random rnd = new Random(1331);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(30);
            int k = 1 + rnd.nextInt(10);
            int[] got = fronts(n, k);
            for (int r = 0; r < n; r++) if (got[r] != Math.max(0, r - k + 1)) throw new AssertionError("front is max(0, r-k+1) for n=" + n + " k=" + k);
        }
    }
}
```

#### Solution: [Vary] Jumping Boundary (Author exercise)
<!-- id: dq-jumping-boundary -->

**Approach.** After appending index `r`, loop while the front index is smaller than `legalLeft[r]`, removing it and counting the removals. The loop is needed because the bound can jump over several indices, and it stops at the first front that is legal, since indices increase toward the back. The assertions check the examples, compare the counts with a definition: the number of indices expired at step `r` is `legalLeft[r] - legalLeft[r-1]` for `r > 0`, with `legalLeft[0]` indices for the first step, and use random non-decreasing bounds with `legalLeft[r] <= r`.

**Complexity.** O(n) time overall and O(n) memory in the worst case of a bound that never moves.

```java run
import java.util.ArrayDeque;
import java.util.Arrays;
import java.util.Random;

public final class JumpingBoundary {
    static int[] expiredCounts(int[] legalLeft) {
        int n = legalLeft.length;
        int[] out = new int[n];
        ArrayDeque<Integer> d = new ArrayDeque<>();
        for (int r = 0; r < n; r++) {
            d.addLast(r);
            while (!d.isEmpty() && d.peekFirst() < legalLeft[r]) { d.removeFirst(); out[r]++; }
        }
        return out;
    }

    public static void main(String[] args) {
        if (!Arrays.equals(expiredCounts(new int[]{0, 0, 1, 3, 3, 5}), new int[]{0, 0, 1, 2, 0, 2})) throw new AssertionError("example 1");
        if (!Arrays.equals(expiredCounts(new int[]{0, 1, 2, 3}), new int[]{0, 1, 1, 1})) throw new AssertionError("example 2");
        Random rnd = new Random(1332);
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(20);
            int[] left = new int[n];
            int cur = 0;
            for (int r = 0; r < n; r++) {
                int next = cur + (rnd.nextInt(3) == 0 ? rnd.nextInt(3) : 0);
                cur = Math.min(next, r);
                left[r] = cur;
            }
            int[] got = expiredCounts(left);
            for (int r = 0; r < n; r++) {
                int expected = left[r] - (r == 0 ? 0 : left[r - 1]);
                if (got[r] != expected) throw new AssertionError("count at " + r + " for " + Arrays.toString(left));
            }
        }
    }
}
```

#### Solution: [Boundary] Exact Expiry Point (Author exercise)
<!-- id: dq-exact-expiry-point -->

**Approach.** Remove from the front while the index is at most `r - k`. The index exactly `k` steps behind the right edge is already outside a window of length `k`, because the window covers `r - k + 1` through `r`. The resulting size is `min(r + 1, k)`. The assertions check the examples, compare with that formula on random inputs, and show that the off-by-one test `index < r - k` leaves `k + 1` indices, one stale entry too many, and in particular a window of length 2 for `k = 1`.

**Complexity.** O(n) time and O(k) memory.

```java run
import java.util.ArrayDeque;
import java.util.Arrays;
import java.util.Random;

public final class ExactExpiryPoint {
    static int[] sizes(int n, int k, boolean strictTest) {
        int[] out = new int[n];
        ArrayDeque<Integer> d = new ArrayDeque<>();
        for (int r = 0; r < n; r++) {
            d.addLast(r);
            while (!d.isEmpty() && (strictTest ? d.peekFirst() < r - k : d.peekFirst() <= r - k)) d.removeFirst();
            out[r] = d.size();
        }
        return out;
    }

    public static void main(String[] args) {
        if (!Arrays.equals(sizes(5, 3, false), new int[]{1, 2, 3, 3, 3})) throw new AssertionError("example 1");
        if (!Arrays.equals(sizes(4, 1, false), new int[]{1, 1, 1, 1})) throw new AssertionError("example 2");
        if (!Arrays.equals(sizes(4, 1, true), new int[]{1, 2, 2, 2})) throw new AssertionError("the strict test keeps a stale index");
        Random rnd = new Random(1333);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(30);
            int k = 1 + rnd.nextInt(12);
            int[] got = sizes(n, k, false);
            int[] wrong = sizes(n, k, true);
            for (int r = 0; r < n; r++) {
                if (got[r] != Math.min(r + 1, k)) throw new AssertionError("size must be min(r+1, k)");
                if (wrong[r] != Math.min(r + 1, k + 1)) throw new AssertionError("the strict test gives min(r+1, k+1)");
            }
        }
    }
}
```

#### Solution: [Recognize] Chronological Candidate Queue (Author exercise)
<!-- id: dq-chronological-candidate-queue -->

**Approach.** At each right edge `r`, do three things in order: remove from the front while the index is at most `r - k`, remove from the back while the value is strictly smaller than `a[r]`, and append `r`. The first two moves keep, respectively, the age rule and the order rule. The indices stay increasing because only `r` is ever appended, and the values stay non-increasing because the back loop stops at the first entry that is not smaller. After the last step the deque holds the indices in the last window that no later value in that window strictly exceeds. The assertions check the examples, check both orders after every step, and compare the final deque with that definition.

**Complexity.** O(n) time and O(k) memory.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

public final class ChronologicalCandidateQueue {
    static List<Integer> finalDeque(int[] a, int k) {
        ArrayDeque<Integer> d = new ArrayDeque<>();
        for (int r = 0; r < a.length; r++) {
            while (!d.isEmpty() && d.peekFirst() <= r - k) d.removeFirst();
            while (!d.isEmpty() && a[d.peekLast()] < a[r]) d.removeLast();
            d.addLast(r);
            int prevIndex = -1, prevValue = Integer.MAX_VALUE;
            for (int idx : d) {
                if (idx <= prevIndex) throw new AssertionError("indices must increase from front to back");
                if (a[idx] > prevValue) throw new AssertionError("values must not increase from front to back");
                if (idx <= r - k) throw new AssertionError("every stored index must be inside the window");
                prevIndex = idx;
                prevValue = a[idx];
            }
        }
        return new ArrayList<>(d);
    }
    static List<Integer> oracle(int[] a, int k) {
        List<Integer> out = new ArrayList<>();
        int n = a.length;
        for (int i = Math.max(0, n - k); i < n; i++) {
            boolean survives = true;
            for (int j = i + 1; j < n; j++) if (a[j] > a[i]) survives = false;
            if (survives) out.add(i);
        }
        return out;
    }

    public static void main(String[] args) {
        if (!finalDeque(new int[]{4, 2, 12, 3, 8, 1}, 3).equals(Arrays.asList(4, 5))) throw new AssertionError("example 1");
        if (!finalDeque(new int[]{5, 4, 3, 2, 1}, 2).equals(Arrays.asList(3, 4))) throw new AssertionError("example 2");
        Random rnd = new Random(1334);
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(14);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(6);
            int k = 1 + rnd.nextInt(n);
            if (!finalDeque(a, k).equals(oracle(a, k))) throw new AssertionError("disagrees with the definition on " + Arrays.toString(a) + " k=" + k);
        }
    }
}
```
