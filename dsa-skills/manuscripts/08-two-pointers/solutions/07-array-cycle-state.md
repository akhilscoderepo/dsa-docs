<!-- solutions-for: 08-two-pointers -->
### Solutions For Following Values As Indexes

#### Solution: [Build] Follow Links (Author exercise)
<!-- id: tp-follow-links -->

**Approach.**
Every value is a legal index from 0 to `n - 1`, so the read `nums[index]` never leaves the array. The method keeps a `boolean` array of visited indexes and starts at index 0. It marks the current index, moves to `nums[index]`, and counts the marked indexes. The walk stops at the first index that is already marked. The walk has at most `n` distinct indexes, so it must stop. The invariant is that `visited[i]` is true exactly for the indexes already counted.

**Complexity.**
- **Time** is O(n), because each index is visited at most once before the walk stops.
- **Space** is O(n) for the visited array, which this exercise allows.

```java run
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public final class FollowLinks {
    /**
     * Returns the number of distinct indexes visited from index 0 before a repeat.
     * Time: O(n).
     * Space: O(n) for the visited array.
     * Invariant: visited[i] is true exactly for the indexes already counted.
     */
    static int walkLength(int[] nums) {
        boolean[] visited = new boolean[nums.length];
        int index = 0, count = 0;
        // The walk ends at the first marked index, so the loop runs at most n times.
        while (!visited[index]) {
            visited[index] = true;
            count++;
            // Every value is a legal index, so this read stays in range.
            index = nums[index];
        }
        return count;
    }

    public static void main(String[] args) {
        // The statement examples.
        if (walkLength(new int[] {1, 2, 0}) != 3) throw new AssertionError("example 1");
        if (walkLength(new int[] {0}) != 1) throw new AssertionError("example 2");
        // Random legal arrays against a path list built step by step.
        Random rnd = new Random(71);
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(9);
            int[] a = rnd.ints(n, 0, n).toArray();
            List<Integer> path = new ArrayList<>();
            int x = 0;
            while (!path.contains(x)) { path.add(x); x = a[x]; }
            if (walkLength(a) != path.size()) throw new AssertionError("random");
        }
    }
}
```

#### Solution: [Vary] Find the Duplicate Number (LeetCode 287)
<!-- id: tp-find-duplicate -->

**Approach.**
The table has `n + 1` slots and the values lie between 1 and `n`, so reading `nums[i]` as the next index keeps every step in range and never returns to index 0. In phase one, `slow` moves one step and `fast` moves two steps per round, and they meet inside the cycle. In phase two, `slow` returns to index 0, and both pointers move one step per round. They meet at the first index of the cycle. Two different indexes point to that index, so its value is repeated. The invariant of phase two is that both pointers are the same number of steps from the entry.

**Complexity.**
- **Time** is O(n), because each phase makes at most a few times `n` steps.
- **Space** is O(1), because the method keeps two indexes and never writes to the table.

```java run
import java.util.Arrays;
import java.util.Random;

public final class FindDuplicate287 {
    /**
     * Returns a repeated value of a table with n + 1 values in 1..n, without writing to it.
     * Time: O(n).
     * Space: O(1).
     * Invariant of phase two: both pointers are equally far from the entry.
     */
    static int findDuplicate(int[] nums) {
        int slow = 0, fast = 0;
        // Phase one: the fast pointer gains one step per round, so they meet inside the cycle.
        do {
            slow = nums[slow];
            fast = nums[nums[fast]];
        } while (slow != fast);
        // Phase two: restart one pointer; equal speeds meet at the entry.
        slow = 0;
        while (slow != fast) {
            slow = nums[slow];
            fast = nums[fast];
        }
        return slow;
    }

    public static void main(String[] args) {
        // The statement examples.
        if (findDuplicate(new int[] {3, 1, 3, 4, 2}) != 3) throw new AssertionError("example 1");
        if (findDuplicate(new int[] {2, 2, 2, 2, 2}) != 2) throw new AssertionError("example 2");
        // The smallest legal input.
        if (findDuplicate(new int[] {1, 1}) != 1) throw new AssertionError("smallest");
        // Random legal tables: the answer repeats, and the table is unchanged.
        Random rnd = new Random(72);
        for (int t = 0; t < 5000; t++) {
            int n = 1 + rnd.nextInt(9);
            int[] a = rnd.ints(n + 1, 1, n + 1).toArray();
            int[] copy = a.clone();
            int d = findDuplicate(a);
            int count = 0;
            for (int v : a) if (v == d) count++;
            if (count < 2) throw new AssertionError("not a repeat " + Arrays.toString(a));
            if (!Arrays.equals(a, copy)) throw new AssertionError("table was written");
        }
    }
}
```

#### Solution: [Boundary] Immediate Cycle (Author exercise)
<!-- id: tp-immediate-cycle -->

**Approach.**
The method runs phase one and records the index where the pointers meet, then runs phase two and records the index of the second meeting. For `[1, 1]` the first round moves `slow` to index 1 and `fast` to `nums[nums[0]]`, which is `nums[1]`, which is 1, so they meet at once. Every read uses a value between 1 and `n`, and the table has `n + 1` slots, so no read leaves the array. The invariant is that the meeting index of phase one lies on the cycle, and the meeting index of phase two is the entry.

**Complexity.**
- **Time** is O(n), because each phase moves along the walk a bounded number of rounds.
- **Space** is O(1), because the method keeps two indexes and returns two numbers.

```java run
import java.util.Arrays;
import java.util.Random;

public final class ImmediateCycle {
    /**
     * Returns {meeting index of phase one, meeting index of phase two}.
     * Time: O(n).
     * Space: O(1).
     * Invariant: the first index lies on the cycle and the second is the cycle entry.
     */
    static int[] meetings(int[] nums) {
        int slow = 0, fast = 0;
        do {
            slow = nums[slow];
            fast = nums[nums[fast]];
        } while (slow != fast);
        int m = slow;
        slow = 0;
        // The restarted pointer and the stored pointer move one step per round.
        while (slow != fast) {
            slow = nums[slow];
            fast = nums[fast];
        }
        return new int[] {m, slow};
    }

    public static void main(String[] args) {
        // The statement examples.
        if (!Arrays.equals(meetings(new int[] {1, 1}), new int[] {1, 1})) throw new AssertionError("example 1");
        if (!Arrays.equals(meetings(new int[] {1, 3, 4, 2, 2}), new int[] {4, 2})) throw new AssertionError("example 2");
        // Random legal tables: the entry is the first repeated index of the walk, and m lies on the cycle.
        Random rnd = new Random(73);
        for (int t = 0; t < 5000; t++) {
            int n = 1 + rnd.nextInt(9);
            int[] a = rnd.ints(n + 1, 1, n + 1).toArray();
            // The walk's first repeated index, found with a visited array.
            boolean[] seen = new boolean[n + 1];
            int x = 0;
            while (!seen[x]) { seen[x] = true; x = a[x]; }
            int[] got = meetings(a);
            if (got[1] != x) throw new AssertionError("entry");
            // Walking from m must return to m, which proves that m is on the cycle.
            int y = a[got[0]], steps = 1;
            while (y != got[0] && steps <= n + 2) { y = a[y]; steps++; }
            if (y != got[0]) throw new AssertionError("m is not on the cycle");
        }
    }
}
```

#### Solution: [Recognize] Tail And Cycle Lengths (Author exercise)
<!-- id: tp-tail-cycle-lengths -->

**Approach.**
Phase one ends with both pointers on the cycle. Walking from that index until it returns counts the cycle length `c`. In phase two the restarted pointer takes exactly as many steps as the tail has indexes before the entry, so counting those rounds gives `t`. The proof is that the pointers meet after `k` rounds with `k` a multiple of `c`, and the slow pointer is then `k - t` steps into the cycle. After `t` more steps it stands at the entry, and so does a pointer that restarts at index 0. The invariant of the count is that the number of phase-two rounds equals the distance from index 0 to the entry.

**Complexity.**
- **Time** is O(n), because phase one, the cycle count and phase two each take at most a few times `n` steps.
- **Space** is O(1), because the method keeps a few indexes and counters.

```java run
import java.util.Arrays;
import java.util.Random;

public final class TailCycleLengths {
    /**
     * Returns {tail length, cycle length} of the walk from index 0.
     * Time: O(n).
     * Space: O(1).
     * Invariant: phase-two rounds equal the distance from index 0 to the entry.
     */
    static int[] lengths(int[] nums) {
        int slow = 0, fast = 0;
        // Phase one finds an index on the cycle.
        do {
            slow = nums[slow];
            fast = nums[nums[fast]];
        } while (slow != fast);
        // Count the cycle by walking once around it.
        int cycle = 1;
        for (int x = nums[fast]; x != fast; x = nums[x]) cycle++;
        // Phase two counts the steps from index 0 to the entry.
        slow = 0;
        int tail = 0;
        while (slow != fast) {
            slow = nums[slow];
            fast = nums[fast];
            tail++;
        }
        return new int[] {tail, cycle};
    }

    public static void main(String[] args) {
        // The statement examples.
        if (!Arrays.equals(lengths(new int[] {3, 1, 3, 4, 2}), new int[] {1, 3})) throw new AssertionError("example 1");
        if (!Arrays.equals(lengths(new int[] {1, 1}), new int[] {1, 1})) throw new AssertionError("example 2");
        // Random legal tables against a position map of the walk.
        Random rnd = new Random(74);
        for (int t = 0; t < 5000; t++) {
            int n = 1 + rnd.nextInt(9);
            int[] a = rnd.ints(n + 1, 1, n + 1).toArray();
            int[] position = new int[n + 1];
            Arrays.fill(position, -1);
            int x = 0, step = 0;
            while (position[x] < 0) { position[x] = step++; x = a[x]; }
            int[] expect = {position[x], step - position[x]};
            if (!Arrays.equals(lengths(a), expect)) throw new AssertionError("random " + Arrays.toString(a));
        }
    }
}
```
