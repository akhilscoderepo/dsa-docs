<!-- solutions-for: 08-array-cycle-state -->
### Array Cycle State

#### Solution: [Build] Follow Links (Author exercise)
<!-- id: tp-follow-links -->

**Approach.** Because every value is between 1 and n, every read lands on an index between 0 and n, and index 0 can never be the target of a move, so the walk can never return to its own start. The loop marks the current index, reads the next one and counts the move, and stops when it reaches a marked index. The walk holds at most n + 1 distinct indices, so it makes at most n + 1 moves. The check recomputes both examples, runs a checked reader that rejects any index outside 0..n, confirms that index 0 is never revisited, compares with a brute force that stores the visited order in a list, and verifies the move bound.

**Complexity.** The loop performs between 2 and n + 1 moves, each one read, so time is O(n); the boolean array makes memory O(n), which this first rung allows.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

public final class FollowLinks {
    static int outOfRange = 0;

    static int read(int[] nums, int index) {
        if (index < 0 || index >= nums.length) { outOfRange++; throw new AssertionError("index out of range " + index); }
        return nums[index];
    }

    static int movesUntilRepeat(int[] nums) {
        boolean[] stood = new boolean[nums.length];
        int index = 0, moves = 0;
        while (!stood[index]) {
            stood[index] = true;
            index = read(nums, index);
            moves++;
        }
        return moves;
    }

    static int oracle(int[] nums) {
        List<Integer> order = new ArrayList<>();
        int index = 0;
        while (!order.contains(index)) { order.add(index); index = nums[index]; }
        return order.size();
    }

    public static void main(String[] args) {
        if (movesUntilRepeat(new int[] {2, 3, 1, 3}) != 4) throw new AssertionError("example 1");
        if (movesUntilRepeat(new int[] {1, 1}) != 2) throw new AssertionError("example 2");
        Random rnd = new Random(8071);
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(12);
            int[] nums = new int[n + 1];
            for (int i = 0; i <= n; i++) nums[i] = 1 + rnd.nextInt(n);
            int[] before = nums.clone();
            int moves = movesUntilRepeat(nums);
            if (moves != oracle(nums)) throw new AssertionError("differs on " + Arrays.toString(nums));
            if (moves < 2 || moves > n + 1) throw new AssertionError("move bound on " + Arrays.toString(nums));
            if (!Arrays.equals(before, nums)) throw new AssertionError("array changed");
            int index = 0;
            for (int s = 0; s < moves; s++) {
                index = nums[index];
                if (index == 0) throw new AssertionError("walk returned to start");
            }
        }
        if (outOfRange != 0) throw new AssertionError("out of range reads");
    }
}
```

#### Solution: [Vary] Find the Duplicate Number (LeetCode 287)
<!-- id: tp-find-duplicate-read-only -->

**Approach.** Phase one moves `slow` by one step and `fast` by two from index 0 until they are equal, which happens on the ring. Phase two leaves `slow` there, starts `finder` at index 0 and moves both one step per round until they are equal, and that index is the entry of the ring, which is the repeated value because it has two incoming arrows. The check recomputes both examples, enumerates every legal array for n up to 4 and many random arrays up to n = 40 including values repeated many times, compares with a counting oracle, confirms that the array is unchanged, and counts reads to show that the total never exceeds five times n + 1.

**Complexity.** Phase one needs at most n + 1 rounds of three reads and phase two at most n rounds of two reads, so time is linear, and only three integers are kept.

```java run
import java.util.Arrays;
import java.util.Random;

public final class FindDuplicateReadOnly {
    static long reads;

    static int at(int[] nums, int i) { reads++; return nums[i]; }

    static int findDuplicate(int[] nums) {
        int slow = 0, fast = 0;
        do {
            slow = at(nums, slow);
            fast = at(nums, at(nums, fast));
        } while (slow != fast);
        int finder = 0;
        while (finder != slow) {
            finder = at(nums, finder);
            slow = at(nums, slow);
        }
        return slow;
    }

    static int oracle(int[] nums) {
        int[] count = new int[nums.length + 1];
        for (int v : nums) if (++count[v] > 1) return v;
        return -1;
    }

    static boolean legal(int[] nums) {
        int n = nums.length - 1, repeated = 0;
        int[] count = new int[n + 1];
        for (int v : nums) {
            if (v < 1 || v > n) return false;
            count[v]++;
        }
        for (int v = 1; v <= n; v++) if (count[v] > 1) repeated++;
        return repeated == 1;
    }

    static void check(int[] nums) {
        int[] before = nums.clone();
        reads = 0;
        int got = findDuplicate(nums);
        if (got != oracle(nums)) throw new AssertionError("differs on " + Arrays.toString(nums));
        if (!Arrays.equals(before, nums)) throw new AssertionError("array changed");
        if (reads > 5L * nums.length) throw new AssertionError("too many reads " + reads + " for " + Arrays.toString(nums));
    }

    static void enumerate(int[] nums, int pos, int n) {
        if (pos == nums.length) { if (legal(nums)) check(nums); return; }
        for (int v = 1; v <= n; v++) { nums[pos] = v; enumerate(nums, pos + 1, n); }
    }

    public static void main(String[] args) {
        if (findDuplicate(new int[] {4, 2, 5, 3, 2, 1}) != 2) throw new AssertionError("example 1");
        if (findDuplicate(new int[] {3, 3, 3, 3}) != 3) throw new AssertionError("example 2");
        for (int n = 1; n <= 4; n++) enumerate(new int[n + 1], 0, n);
        Random rnd = new Random(8072);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(40);
            int d = 1 + rnd.nextInt(n);
            int k = 2 + rnd.nextInt(n);
            int[] nums = new int[n + 1];
            int[] pool = new int[n - 1];
            int p = 0;
            for (int v = 1; v <= n; v++) if (v != d) pool[p++] = v;
            for (int i = pool.length - 1; i > 0; i--) { int j = rnd.nextInt(i + 1); int tmp = pool[i]; pool[i] = pool[j]; pool[j] = tmp; }
            int filled = 0;
            for (int i = 0; i < k && filled < n + 1; i++) nums[filled++] = d;
            for (int i = 0; filled < n + 1; i++) nums[filled++] = pool[i];
            for (int i = nums.length - 1; i > 0; i--) { int j = rnd.nextInt(i + 1); int tmp = nums[i]; nums[i] = nums[j]; nums[j] = tmp; }
            if (!legal(nums)) throw new AssertionError("generator made an illegal array");
            check(nums);
        }
        int[] same = new int[101];
        Arrays.fill(same, 100);
        check(same);
    }
}
```

#### Solution: [Boundary] Immediate Cycle (Author exercise)
<!-- id: tp-immediate-cycle -->

**Approach.** For n = 1 the only legal array is `[1, 1]`: slow and fast both go to index 1 in one round and are equal, then phase two moves both from 0 and 1 to 1. For n = 2 the values 1 and 2 are the only legal indices, so no read can leave 0..2, and index 0 is never targeted. The test must come after the first move, which a do-while provides; a while loop with the test first would see two equal starting indices and wrongly return 0. The check runs every legal array of both sizes through a reader that throws on an illegal index, counts such failures, verifies the answers against a counting oracle, and confirms that the input is not written.

**Complexity.** For these sizes the work is a fixed handful of reads. In general the method keeps the linear bound of the previous exercise.

```java run
import java.util.Arrays;

public final class ImmediateCycle {
    static int illegalReads = 0;

    static int checked(int[] nums, int index) {
        if (index < 0 || index >= nums.length) { illegalReads++; throw new AssertionError("bad index " + index); }
        return nums[index];
    }

    static int duplicate(int[] nums) {
        int slow = 0, fast = 0;
        do {
            slow = checked(nums, slow);
            fast = checked(nums, checked(nums, fast));
        } while (slow != fast);
        int finder = 0;
        while (finder != slow) {
            finder = checked(nums, finder);
            slow = checked(nums, slow);
        }
        return slow;
    }

    static int wrongTestFirst(int[] nums) {
        int slow = 0, fast = 0;
        while (slow != fast) { slow = nums[slow]; fast = nums[nums[fast]]; }
        return slow;
    }

    static int oracle(int[] nums) {
        boolean[] seen = new boolean[nums.length];
        for (int v : nums) { if (seen[v]) return v; seen[v] = true; }
        return -1;
    }

    public static void main(String[] args) {
        if (duplicate(new int[] {1, 1}) != 1) throw new AssertionError("example 1");
        if (duplicate(new int[] {2, 2, 1}) != 2) throw new AssertionError("example 2");
        if (wrongTestFirst(new int[] {1, 1}) != 0) throw new AssertionError("test-first loop should return 0 here");
        int legalCount = 0;
        for (int a = 1; a <= 1; a++) for (int b = 1; b <= 1; b++) {
            int[] nums = {a, b};
            if (oracle(nums) != a || a != b) throw new AssertionError("n = 1 shape");
            if (duplicate(nums) != 1) throw new AssertionError("n=1");
            legalCount++;
        }
        for (int a = 1; a <= 2; a++) for (int b = 1; b <= 2; b++) for (int c = 1; c <= 2; c++) {
            int[] nums = {a, b, c};
            int[] before = nums.clone();
            int ones = 0, twos = 0;
            for (int v : nums) { if (v == 1) ones++; else twos++; }
            if (ones == 0 || twos == 0) {
                // all three equal: exactly one repeated value, still legal
            }
            if (duplicate(nums) != oracle(nums)) throw new AssertionError("differs on " + Arrays.toString(nums));
            if (!Arrays.equals(before, nums)) throw new AssertionError("array changed");
            legalCount++;
        }
        if (legalCount != 9) throw new AssertionError("expected 9 arrays");
        if (illegalReads != 0) throw new AssertionError("illegal reads happened");
    }
}
```

#### Solution: [Recognize] Phase Two Proof (LeetCode 287)
<!-- id: tp-phase-two-proof -->

**Approach.** Run phase one and remember where it stopped, then run phase two and return both indices. After phase one the slow walker has taken a multiple of the ring length in steps, so it stands at a place that is `mu` steps short of the entry measured around the ring, modulo the ring length. The walker from index 0 needs exactly `mu` steps to reach the entry, and the ring walker needs `mu` steps plus whole laps, so the two agree after `mu` rounds, and not earlier because the first one is still on the tail. The meeting place of phase one is at a position that depends on how many laps the walkers made, so it is the entry only when `mu` is a multiple of the ring length. The check recomputes both examples, compares the duplicate with a counting oracle, derives `mu` and the ring length by an independent walk, and asserts that phase two runs exactly `mu` rounds, that the stopping index is on the ring, and that the stopping index equals the duplicate exactly when `mu` is a multiple of the ring length. It also verifies that both outcomes occur in the random trials.

**Complexity.** Linear time, since each phase takes at most n + 1 rounds, and constant extra space with no write to the array.

```java run
import java.util.Arrays;
import java.util.Random;

public final class PhaseTwoProof {
    static int phaseTwoRounds;

    static int[] stopAndDuplicate(int[] nums) {
        int slow = 0, fast = 0;
        do {
            slow = nums[slow];
            fast = nums[nums[fast]];
        } while (slow != fast);
        int stop = slow;
        int finder = 0;
        phaseTwoRounds = 0;
        while (finder != slow) {
            finder = nums[finder];
            slow = nums[slow];
            phaseTwoRounds++;
        }
        return new int[] {stop, slow};
    }

    static int oracleDuplicate(int[] nums) {
        int[] count = new int[nums.length + 1];
        for (int v : nums) if (++count[v] > 1) return v;
        return -1;
    }

    public static void main(String[] args) {
        if (!Arrays.equals(stopAndDuplicate(new int[] {4, 2, 5, 3, 2, 1}), new int[] {5, 2})) throw new AssertionError("example 1");
        if (!Arrays.equals(stopAndDuplicate(new int[] {3, 3, 3, 3}), new int[] {3, 3})) throw new AssertionError("example 2");
        Random rnd = new Random(8074);
        int sameCount = 0, differentCount = 0;
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(25);
            int d = 1 + rnd.nextInt(n);
            int k = 2 + rnd.nextInt(Math.min(n, 3));
            int[] pool = new int[n - 1];
            int p = 0;
            for (int v = 1; v <= n; v++) if (v != d) pool[p++] = v;
            for (int i = pool.length - 1; i > 0; i--) { int j = rnd.nextInt(i + 1); int tmp = pool[i]; pool[i] = pool[j]; pool[j] = tmp; }
            int[] nums = new int[n + 1];
            int filled = 0;
            for (int i = 0; i < k && filled < n + 1; i++) nums[filled++] = d;
            for (int i = 0; filled < n + 1; i++) nums[filled++] = pool[i];
            for (int i = nums.length - 1; i > 0; i--) { int j = rnd.nextInt(i + 1); int tmp = nums[i]; nums[i] = nums[j]; nums[j] = tmp; }
            int[] before = nums.clone();
            int[] got = stopAndDuplicate(nums);
            if (got[1] != oracleDuplicate(nums)) throw new AssertionError("duplicate differs on " + Arrays.toString(nums));
            if (!Arrays.equals(before, nums)) throw new AssertionError("array changed");
            int[] firstVisit = new int[n + 1];
            Arrays.fill(firstVisit, -1);
            int index = 0, step = 0;
            while (firstVisit[index] < 0) { firstVisit[index] = step++; index = nums[index]; }
            int mu = firstVisit[index], lambda = step - mu;
            if (index != got[1]) throw new AssertionError("entry is not the duplicate");
            if (phaseTwoRounds != mu) throw new AssertionError("phase two rounds " + phaseTwoRounds + " vs mu " + mu);
            if (firstVisit[got[0]] < mu) throw new AssertionError("stop is not on the ring");
            boolean same = got[0] == got[1];
            if (same != (mu % lambda == 0)) throw new AssertionError("stop equals entry rule on " + Arrays.toString(nums));
            if (same) sameCount++; else differentCount++;
        }
        if (sameCount == 0 || differentCount == 0) throw new AssertionError("both outcomes must occur");
    }
}
```
