<!-- solutions-for: 03-farthest-frontier -->
### Solutions For Farthest Frontier

#### Solution: [Build] Update Reachable Prefix (Author exercise)
<!-- id: gr-update-reachable-prefix -->

**Approach.**
The method scans the indices from 0 and raises `farthest` to `i + power[i]` at each index that is inside the frontier. It stops at the first index that lies beyond `farthest`, because no scanned station can forward that far and later stations are not reachable either. The method returns `farthest`, capped at the last index, because a jump cannot leave the array.

After each step, every index up to `farthest` is reachable and no larger index is.

**Complexity.**
- **Time** is O(n), because each index is read once.
- **Space** is O(1), because the method keeps one integer.

```java run
import java.util.*;

public final class UpdateReachablePrefix {
    /**
     * Returns the largest index reachable from index 0.
     * Time: O(n). Space: O(1).
     * Invariant: every index up to farthest is reachable, and no larger index is.
     */
    static int frontier(int[] power) {
        int farthest = 0;                                             // index 0 is the start
        for (int i = 0; i < power.length; i++) {                      // one read per index
            if (i > farthest) break;                                  // beyond the frontier: nothing reaches it
            farthest = Math.min(power.length - 1, Math.max(farthest, i + power[i])); // extend, capped at the last index
        }
        return farthest;
    }

    static int brute(int[] p) {
        boolean[] seen = new boolean[p.length];
        Deque<Integer> q = new ArrayDeque<>();
        seen[0] = true; q.add(0);
        int best = 0;
        while (!q.isEmpty()) {                                        // breadth-first over every jump
            int i = q.poll();
            best = Math.max(best, i);
            for (int d = 0; d <= p[i] && i + d < p.length; d++) if (!seen[i + d]) { seen[i + d] = true; q.add(i + d); }
        }
        return best;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (frontier(new int[] {2, 3, 1, 1, 4}) != 4) throw new AssertionError("ex1");
        if (frontier(new int[] {3, 2, 1, 0, 4}) != 3) throw new AssertionError("ex2");
        // A single entry returns 0, and a huge power is capped at the last index.
        if (frontier(new int[] {0}) != 0 || frontier(new int[] {100000, 0, 0}) != 2) throw new AssertionError("edge");
        // Random arrays must match a breadth-first search over every jump.
        Random rnd = new Random(2021);
        for (int t = 0; t < 500; t++) {
            int[] p = new int[1 + rnd.nextInt(9)];
            for (int k = 0; k < p.length; k++) p[k] = rnd.nextInt(4);
            if (frontier(p) != brute(p)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Vary] Jump Game (LeetCode 55)
<!-- id: gr-jump-game -->

**Approach.**
The method runs the same scan and stops as soon as `farthest` reaches the last index, which means the answer is true. If the scan meets an index beyond `farthest` first, the answer is false. The frontier replaces every route, because each reachable index forwards to every closer index too, so the reachable indices form a prefix.

After each step, the reachable indices are exactly `0..farthest`.

**Complexity.**
- **Time** is O(n), because each index is tested once.
- **Space** is O(1), because the method keeps one integer.

```java run
import java.util.*;

public final class JumpGame {
    /**
     * Returns true when the last index is reachable.
     * Time: O(n). Space: O(1).
     * Invariant: the reachable indices are exactly 0..farthest.
     */
    static boolean canJump(int[] nums) {
        int farthest = 0;
        for (int i = 0; i < nums.length; i++) {                       // one test per index
            if (i > farthest) return false;                           // a gap: no jump lands on i
            farthest = Math.max(farthest, i + nums[i]);               // extend the frontier
            if (farthest >= nums.length - 1) return true;             // the last index is inside the frontier
        }
        return true;
    }

    static boolean brute(int[] a, int i, boolean[] dead) {
        if (i >= a.length - 1) return true;
        if (dead[i]) return false;
        for (int d = 1; d <= a[i]; d++) if (brute(a, i + d, dead)) return true;
        dead[i] = true;
        return false;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!canJump(new int[] {2, 3, 1, 1, 4})) throw new AssertionError("ex1");
        if (canJump(new int[] {3, 2, 1, 0, 4})) throw new AssertionError("ex2");
        // One entry is always true, even with value 0.
        if (!canJump(new int[] {0})) throw new AssertionError("single");
        // Random arrays must match a memoized search over every distance.
        Random rnd = new Random(2022);
        for (int t = 0; t < 600; t++) {
            int[] a = new int[1 + rnd.nextInt(10)];
            for (int k = 0; k < a.length; k++) a[k] = rnd.nextInt(4);
            if (canJump(a) != brute(a, 0, new boolean[a.length])) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Boundary] Zero Before The Frontier (Author exercise)
<!-- id: gr-zero-before-the-frontier -->

**Approach.**
The method scans with the same frontier. A zero at index `i` is harmless when `farthest > i`, because an earlier station already forwards past it. A zero blocks when `farthest == i`, `power[i] == 0` and `i < n - 1`, because no station forwards beyond it and the zero cannot either. The method returns the first such index. Indices after a block are not examined, because they are unreachable. The last index never blocks, since nothing lies beyond it.

After each step, `farthest` is the largest reachable index of the scanned prefix.

**Complexity.**
- **Time** is O(n), because each index is tested once.
- **Space** is O(1), because the method keeps one integer.

```java run
import java.util.*;

public final class ZeroBeforeTheFrontier {
    /**
     * Returns the smallest index of a blocking zero, or -1 when none blocks.
     * Time: O(n). Space: O(1).
     * Invariant: farthest is the largest reachable index of the scanned prefix.
     */
    static int firstBlock(int[] power) {
        int farthest = 0;
        for (int i = 0; i < power.length - 1; i++) {                  // the last index never blocks
            if (power[i] == 0 && farthest == i) return i;             // nothing crosses this zero
            farthest = Math.max(farthest, i + power[i]);              // extend the frontier
        }
        return -1;
    }

    static int brute(int[] p) {
        int n = p.length;
        for (int z = 0; z < n - 1; z++) {                             // test each zero by definition
            if (p[z] != 0) continue;
            boolean reach = z == 0;
            if (!reach) {
                boolean[] seen = new boolean[n];
                Deque<Integer> q = new ArrayDeque<>();
                seen[0] = true; q.add(0);
                while (!q.isEmpty()) {
                    int i = q.poll();
                    if (i == z) reach = true;
                    for (int d = 1; d <= p[i] && i + d < n; d++) if (!seen[i + d]) { seen[i + d] = true; q.add(i + d); }
                }
            }
            boolean crossed = false;                                  // does an earlier station forward beyond z?
            for (int j = 0; j < z; j++) {
                boolean r = j == 0;
                if (!r) {
                    boolean[] seen = new boolean[n];
                    Deque<Integer> q = new ArrayDeque<>();
                    seen[0] = true; q.add(0);
                    while (!q.isEmpty()) {
                        int i = q.poll();
                        if (i == j) r = true;
                        for (int d = 1; d <= p[i] && i + d < n; d++) if (!seen[i + d]) { seen[i + d] = true; q.add(i + d); }
                    }
                }
                if (r && j + p[j] > z) crossed = true;
            }
            if (reach && !crossed) return z;
        }
        return -1;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (firstBlock(new int[] {3, 2, 1, 0, 4}) != 3) throw new AssertionError("ex1");
        if (firstBlock(new int[] {2, 0, 2, 0, 4}) != -1) throw new AssertionError("ex2");
        // A zero last never blocks, and a zero at index 0 of a longer line blocks.
        if (firstBlock(new int[] {1, 0}) != -1 || firstBlock(new int[] {0, 5}) != 0) throw new AssertionError("edge");
        // Random arrays must match a definition-based check with breadth-first reachability.
        Random rnd = new Random(2023);
        for (int t = 0; t < 600; t++) {
            int[] p = new int[1 + rnd.nextInt(9)];
            for (int k = 0; k < p.length; k++) p[k] = rnd.nextInt(3);
            if (firstBlock(p) != brute(p)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Recognize] Jump Game II (LeetCode 45)
<!-- id: gr-jump-game-ii -->

**Approach.**
The method treats the indices that need the same number of jumps as one jump layer. The variable `layerEnd` is the right edge of the current layer, and `next` is the farthest index that any index of the current layer can reach. The scan reads the indices in order and raises `next`. When the scan reaches `layerEnd`, the current layer is complete, so the method counts one jump and moves `layerEnd` to `next`. The scan stops before the last index, because the guarantee says the last index lies inside some layer. Every index of the next layer needs one jump more than the current layer, and every index inside the frontier is reached by one jump from some index of the current layer, so the count is the smallest.

After each step, `jumps` is the number of completed layers, and `next` is the frontier after one more jump.

**Complexity.**
- **Time** is O(n), because each index is read once.
- **Space** is O(1), because the method keeps three integers.

```java run
import java.util.*;

public final class JumpGameII {
    /**
     * Returns the smallest number of jumps to the last index.
     * Time: O(n). Space: O(1).
     * Invariant: layerEnd is the right edge of indices reachable in jumps, and next is the edge after one more jump.
     */
    static int jump(int[] nums) {
        int jumps = 0, layerEnd = 0, next = 0;
        for (int i = 0; i < nums.length - 1; i++) {                   // the last index needs no jump from it
            next = Math.max(next, i + nums[i]);                       // best reach of the current layer
            if (i == layerEnd) { jumps++; layerEnd = next; }          // layer done: one more jump
        }
        return jumps;
    }

    static int brute(int[] a) {
        int n = a.length;
        int[] dist = new int[n];
        Arrays.fill(dist, Integer.MAX_VALUE);
        dist[0] = 0;
        for (int i = 0; i < n; i++) {                                 // dynamic programming over every distance
            if (dist[i] == Integer.MAX_VALUE) continue;
            for (int d = 1; d <= a[i] && i + d < n; d++) dist[i + d] = Math.min(dist[i + d], dist[i] + 1);
        }
        return dist[n - 1];
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (jump(new int[] {2, 3, 1, 1, 4}) != 2) throw new AssertionError("ex1");
        if (jump(new int[] {1, 2, 0, 1}) != 2) throw new AssertionError("ex2");
        // One entry needs no jump.
        if (jump(new int[] {0}) != 0) throw new AssertionError("single");
        // Random reachable arrays must match dynamic programming.
        Random rnd = new Random(2024);
        int checked = 0;
        for (int t = 0; t < 2000 && checked < 500; t++) {
            int[] a = new int[1 + rnd.nextInt(10)];
            for (int k = 0; k < a.length; k++) a[k] = rnd.nextInt(4);
            if (brute(a) == Integer.MAX_VALUE) continue;              // the exercise guarantees reachability
            checked++;
            if (jump(a) != brute(a)) throw new AssertionError("random " + t);
        }
        if (checked < 100) throw new AssertionError("too few reachable samples");
    }
}
```
