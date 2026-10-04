<!-- solutions-for: 20-greedy -->
### Farthest Frontier

#### Solution: [Build] Update Reachable Prefix (Author exercise)
<!-- id: gr-update-reachable-prefix -->

**Approach.** Keep the frontier `far` as a `long`, starting at index 0. Read towers in order while the index does not exceed `far`, and replace `far` by the larger of itself and `i + strength[i]`. The answer is the frontier capped at the last index. The assertions check both examples and show the overflow that the `long` prevents: `Integer.MAX_VALUE + 1` wraps to a negative int. Random arrays, with a pool that includes zeros and the largest int, are compared with a forward propagation that marks every reachable tower one jump at a time.

**Complexity.** The scan reads each tower at most once, so it takes O(n) time and O(1) extra memory; the oracle spends O(n²).

```java run
import java.util.Random;

public final class UpdateReachablePrefix {
    static int highestReachable(int[] strength) {
        long far = 0;
        for (int i = 0; i < strength.length; i++) {
            if (i > far) break;
            far = Math.max(far, (long) i + strength[i]);
        }
        return (int) Math.min(far, strength.length - 1);
    }

    static int oracle(int[] s) {
        int n = s.length;
        boolean[] reach = new boolean[n];
        reach[0] = true;
        int best = 0;
        for (int i = 0; i < n; i++) {
            if (!reach[i]) continue;
            best = i;
            long top = Math.min((long) n - 1, (long) i + s[i]);
            for (int j = i + 1; j <= top; j++) reach[j] = true;
        }
        return best;
    }

    public static void main(String[] args) {
        if (highestReachable(new int[]{3, 1, 0, 2, 0, 5}) != 5) throw new AssertionError("example 1");
        if (highestReachable(new int[]{1, 0, 9, 9}) != 1) throw new AssertionError("example 2");
        if (highestReachable(new int[]{0}) != 0) throw new AssertionError("a lone tower");
        if (highestReachable(new int[]{Integer.MAX_VALUE, 0, 0}) != 2) throw new AssertionError("a huge strength crosses the pass");
        int wrapped = Integer.MAX_VALUE + 1;
        if (wrapped >= 0) throw new AssertionError("the int sum must wrap negative");
        if (highestReachable(new int[]{0, Integer.MAX_VALUE}) != 0) throw new AssertionError("a dead first tower blocks everything");

        int[] pool = {0, 0, 0, 1, 2, 3, 5, Integer.MAX_VALUE};
        Random rnd = new Random(2201);
        for (int t = 0; t < 6000; t++) {
            int n = 1 + rnd.nextInt(12);
            int[] s = new int[n];
            for (int i = 0; i < n; i++) s[i] = pool[rnd.nextInt(pool.length)];
            if (highestReachable(s) != oracle(s)) throw new AssertionError("disagrees with the propagation oracle");
        }
    }
}
```

#### Solution: [Vary] Jump Game (LeetCode 55)
<!-- id: gr-jump-game-reach -->

**Approach.** The scan is the same, but it stops with `false` as soon as the index passes the frontier, and finishes with `true` otherwise. The last index is never read as a move, since reaching it is the goal. The oracle works backwards, which is a different method: it marks the last index as good and then, from the right, marks an index good when some index within its jump is good. The assertions cover both examples, a single element, and random arrays with small values where zeros occur often.

**Complexity.** One pass with a single running number gives linear time and constant extra memory, while the backward oracle needs O(n²) in the worst case.

```java run
import java.util.Random;

public final class JumpGameReach {
    static boolean canReach(int[] nums) {
        long far = 0;
        for (int i = 0; i < nums.length; i++) {
            if (i > far) return false;
            far = Math.max(far, (long) i + nums[i]);
        }
        return true;
    }

    static boolean backward(int[] nums) {
        int n = nums.length;
        boolean[] good = new boolean[n];
        good[n - 1] = true;
        for (int i = n - 2; i >= 0; i--) {
            for (int step = 1; step <= nums[i] && i + step < n; step++) {
                if (good[i + step]) { good[i] = true; break; }
            }
        }
        return good[0];
    }

    public static void main(String[] args) {
        if (canReach(new int[]{2, 0, 0, 1})) throw new AssertionError("example 1");
        if (!canReach(new int[]{1, 1, 1, 0})) throw new AssertionError("example 2");
        if (!canReach(new int[]{0})) throw new AssertionError("a single element is already at the end");
        if (canReach(new int[]{0, 1})) throw new AssertionError("a zero at the start blocks the move");
        if (!canReach(new int[]{5, 0, 0, 0})) throw new AssertionError("an early long jump crosses zeros");

        Random rnd = new Random(2202);
        for (int t = 0; t < 8000; t++) {
            int n = 1 + rnd.nextInt(12);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(4) == 0 ? rnd.nextInt(6) : rnd.nextInt(3);
            if (canReach(a) != backward(a)) throw new AssertionError("disagrees with the backward oracle");
        }
    }
}
```

#### Solution: [Boundary] Zero Before The Frontier (Author exercise)
<!-- id: gr-zero-before-frontier -->

**Approach.** Run the frontier scan and return the first index that exceeds the frontier. If the scan ends without that happening, every index is reachable and the answer is -1. A zero strictly inside the frontier changes nothing, so a first jump of at least the array length crosses any number of zeros. Sums are formed in `long`, since a strength of `Integer.MAX_VALUE` at a later index would wrap in 32-bit arithmetic. The oracle marks reachable indexes by propagating each reachable index forward, and then reports the smallest unmarked index.

**Complexity.** The scan is O(n) time with O(1) extra memory, against O(n²) for the propagation oracle.

```java run
import java.util.Random;

public final class ZeroBeforeFrontier {
    static int firstUnreachable(int[] nums) {
        long far = 0;
        for (int i = 0; i < nums.length; i++) {
            if (i > far) return i;
            far = Math.max(far, (long) i + nums[i]);
        }
        return -1;
    }

    static int oracle(int[] nums) {
        int n = nums.length;
        boolean[] reach = new boolean[n];
        reach[0] = true;
        for (int i = 0; i < n; i++) {
            if (!reach[i]) continue;
            long top = Math.min((long) n - 1, (long) i + nums[i]);
            for (int j = i + 1; j <= top; j++) reach[j] = true;
        }
        for (int i = 0; i < n; i++) if (!reach[i]) return i;
        return -1;
    }

    public static void main(String[] args) {
        if (firstUnreachable(new int[]{3, 0, 0, 0, 1}) != 4) throw new AssertionError("example 1");
        if (firstUnreachable(new int[]{4, 0, 0, 0, 0}) != -1) throw new AssertionError("example 2");
        if (firstUnreachable(new int[]{0}) != -1) throw new AssertionError("index zero is always reachable");
        if (firstUnreachable(new int[]{0, 7}) != 1) throw new AssertionError("a dead start leaves index one cut off");
        if (firstUnreachable(new int[]{2, 0, Integer.MAX_VALUE, 0, 0}) != -1) throw new AssertionError("large strength inside the frontier");
        if (firstUnreachable(new int[]{1, 0, Integer.MAX_VALUE}) != 2) throw new AssertionError("large strength beyond the frontier is unread");

        int[] pool = {0, 0, 0, 1, 2, 4, Integer.MAX_VALUE};
        Random rnd = new Random(2203);
        for (int t = 0; t < 6000; t++) {
            int n = 1 + rnd.nextInt(12);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = pool[rnd.nextInt(pool.length)];
            if (firstUnreachable(a) != oracle(a)) throw new AssertionError("disagrees with the propagation oracle");
        }
    }
}
```

#### Solution: [Recognize] Jump Game II (LeetCode 45)
<!-- id: gr-jump-layers -->

**Approach.** Walk the indices before the last one. At each index, update the record `far` of the best reach seen. When the index equals `curEnd`, the current layer is finished: if the record did not move past `curEnd`, nothing in the layer can forward the message and the answer is -1. Otherwise count one move, make the record the new layer end, and stop early once that end covers the last index. A one-element array leaves the loop body unexecuted and returns 0. The oracle is a breadth-first search over indexes, which returns the same counts and -1 for unreachable ends; the assertions also compare both examples.

**Complexity.** The layer walk visits each index once for O(n) time and O(1) extra memory; the breadth-first oracle costs O(n²).

```java run
import java.util.ArrayDeque;
import java.util.Random;

public final class JumpLayers {
    static int fewestMoves(int[] nums) {
        int n = nums.length;
        int jumps = 0;
        long curEnd = 0, far = 0;
        for (int i = 0; i < n - 1; i++) {
            far = Math.max(far, (long) i + nums[i]);
            if (i == curEnd) {
                if (far == curEnd) return -1;
                jumps++;
                curEnd = far;
                if (curEnd >= n - 1) break;
            }
        }
        return jumps;
    }

    static int bfs(int[] nums) {
        int n = nums.length;
        int[] dist = new int[n];
        java.util.Arrays.fill(dist, -1);
        dist[0] = 0;
        ArrayDeque<Integer> queue = new ArrayDeque<>();
        queue.add(0);
        while (!queue.isEmpty()) {
            int i = queue.poll();
            for (int j = i + 1; j <= Math.min(n - 1, i + nums[i]); j++) {
                if (dist[j] == -1) { dist[j] = dist[i] + 1; queue.add(j); }
            }
        }
        return dist[n - 1];
    }

    public static void main(String[] args) {
        if (fewestMoves(new int[]{4, 1, 1, 3, 1, 1, 1}) != 2) throw new AssertionError("example 1");
        if (fewestMoves(new int[]{2, 0, 0, 5}) != -1) throw new AssertionError("example 2");
        if (fewestMoves(new int[]{0}) != 0) throw new AssertionError("single element");
        if (fewestMoves(new int[]{1, 1, 1, 1}) != 3) throw new AssertionError("unit moves");
        if (fewestMoves(new int[]{9, 0, 0, 0}) != 1) throw new AssertionError("one long move");
        if (fewestMoves(new int[]{1, 0}) != 1) throw new AssertionError("a zero at the last index is not read");

        Random rnd = new Random(2204);
        for (int t = 0; t < 8000; t++) {
            int n = 1 + rnd.nextInt(12);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(5) == 0 ? 0 : 1 + rnd.nextInt(4);
            if (fewestMoves(a) != bfs(a)) throw new AssertionError("disagrees with the search oracle");
        }
    }
}
```
