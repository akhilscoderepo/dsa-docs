<!-- solutions-for: 01-arrays-core-operations -->
### Solutions For Direct Scans

#### Solution: [Build] First Match (Author exercise)
<!-- id: ar-first-match -->

**Approach.** The method examines positions from left to right and returns at the first position that holds `target`. Before each comparison, every earlier position has been examined and none matched, so the first match found is the smallest matching index. If the loop ends, every position was examined without a match, so -1 is correct. An empty array skips the loop and returns -1 directly.

The sorted-copy plan from the lesson fails for a reason the harness shows: `Arrays.binarySearch` on the sorted copy `[4, 7, 7]` returns position 1, while the first 7 in the original array sits at index 0. The harness also compares the scan with `List.indexOf` on 2,000 random arrays.

**Complexity.**

- **Time** is O(n), because the loop performs at most `n` comparisons and stops earlier on a match.
- **Space** is O(1), since the only variable that outlives a comparison is the index `i`.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

public final class FirstMatch {
    /**
     * Returns the smallest index holding target, or -1 when target is absent.
     * Time: O(n), because each position is compared at most once.
     * Space: O(1), because only the loop index is stored.
     * Invariant: before reading nums[i], no position in 0..i-1 holds target.
     */
    static int firstIndex(int[] nums, int target) {
        // Visit each position once from the left; the loop header bounds the cost at n comparisons.
        for (int i = 0; i < nums.length; i++) {
            // On a match the invariant makes i the smallest matching index, so the method may leave now.
            if (nums[i] == target) return i;
        }
        // The loop ended, so every position was examined and none matched; -1 is outside the legal indexes.
        return -1;
    }

    /** The plan from the lesson: sort a copy, then binary search it. It answers a position in the copy. */
    static int firstIndexSorted(int[] nums, int target) {
        int[] sorted = nums.clone();
        Arrays.sort(sorted);
        return Arrays.binarySearch(sorted, target);
    }

    public static void main(String[] args) {
        // Checks both examples, including the empty array that skips the loop.
        if (firstIndex(new int[] {6, 2, 8, 2}, 2) != 1) throw new AssertionError("example 1");
        if (firstIndex(new int[] {}, 3) != -1) throw new AssertionError("example 2");
        // Checks the lesson claim: the sorted-copy plan returns 1 for [7, 4, 7], but the first 7 is at index 0.
        if (firstIndexSorted(new int[] {7, 4, 7}, 7) != 1) throw new AssertionError("sorted copy position");
        if (firstIndex(new int[] {7, 4, 7}, 7) != 0) throw new AssertionError("original position");
        // Checks the equality claim: Integer.valueOf(1000) objects are equal by equals but not by reference here.
        Integer p = Integer.valueOf(1000), q = Integer.valueOf(1000);
        if (!p.equals(q)) throw new AssertionError("equals compares values");
        if (p == q) throw new AssertionError("== compares references outside the small cache");
        // Checks the scan against List.indexOf on 2,000 random arrays with a small value range.
        Random rnd = new Random(11);
        for (int t = 0; t < 2000; t++) {
            int[] x = new int[rnd.nextInt(9)];
            List<Integer> boxed = new ArrayList<>();
            for (int i = 0; i < x.length; i++) { x[i] = rnd.nextInt(6) - 2; boxed.add(x[i]); }
            int target = rnd.nextInt(8) - 3;
            if (firstIndex(x, target) != boxed.indexOf(target)) throw new AssertionError("mismatch on " + Arrays.toString(x));
        }
    }
}
```

#### Solution: [Vary] Last Match (Author exercise)
<!-- id: ar-last-match -->

**Approach.** The method keeps the variable `found`, which starts at -1 and takes the value of `i` on every match. A match at index `i` does not rule out a later match, so the loop must continue to the end. After the loop, `found` holds the largest matching index, or -1 when no position matched.

A second correct method scans from the right and returns at the first match it sees. That method is the first-match scan run in reverse, and it stops early on average. The harness checks that both methods agree with `List.lastIndexOf` on 2,000 random arrays.

**Complexity.**

- **Time** is O(n), because the forward method always performs exactly `n` comparisons.
- **Space** is O(1), since `found` and the loop index are the whole state.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

public final class LastMatch {
    /**
     * Returns the largest index holding target, or -1 when target is absent.
     * Time: O(n), because every position is compared exactly once.
     * Space: O(1), because only found and the index are stored.
     * Invariant: before reading nums[i], found is the largest matching index in 0..i-1, or -1.
     */
    static int lastIndex(int[] nums, int target) {
        // The sentinel -1 states that nothing has matched before the first position.
        int found = -1;
        // Visit every position; a match cannot end the loop because a later match would be larger.
        for (int i = 0; i < nums.length; i++) {
            // Record the latest match, which keeps the invariant for the next position.
            if (nums[i] == target) found = i;
        }
        // Return the latest match, or -1 when the loop never matched.
        return found;
    }

    /**
     * Scans from the right and leaves at the first match, which is the last match from the left.
     * Time: O(n) in the worst case, and fewer steps when the match sits near the end.
     * Space: O(1), because only the index is stored.
     */
    static int lastIndexFromRight(int[] nums, int target) {
        // Start at the final position and move left.
        for (int i = nums.length - 1; i >= 0; i--) {
            // The first match met from the right has the largest index, so return at once.
            if (nums[i] == target) return i;
        }
        // No position matched.
        return -1;
    }

    public static void main(String[] args) {
        // Checks both examples.
        if (lastIndex(new int[] {5, 1, 5, 5, 2}, 5) != 3) throw new AssertionError("example 1");
        if (lastIndex(new int[] {4}, 9) != -1) throw new AssertionError("example 2");
        // Checks the empty array.
        if (lastIndex(new int[] {}, 1) != -1) throw new AssertionError("empty");
        // Checks both methods against List.lastIndexOf on 2,000 random arrays.
        Random rnd = new Random(23);
        for (int t = 0; t < 2000; t++) {
            int[] x = new int[rnd.nextInt(9)];
            List<Integer> boxed = new ArrayList<>();
            for (int i = 0; i < x.length; i++) { x[i] = rnd.nextInt(5); boxed.add(x[i]); }
            int target = rnd.nextInt(6);
            int expected = boxed.lastIndexOf(target);
            if (lastIndex(x, target) != expected) throw new AssertionError("forward mismatch on " + Arrays.toString(x));
            if (lastIndexFromRight(x, target) != expected) throw new AssertionError("reverse mismatch on " + Arrays.toString(x));
        }
    }
}
```

#### Solution: [Boundary] Target Absent (Author exercise)
<!-- id: ar-target-absent -->

**Approach.** The method is the first-match scan, and the exercise tests the cases around it. The loop returns an index only from inside the body, and it returns -1 only after the loop ends. Because the two returns sit in different places, a value of -1 stored in the array cannot produce the sentinel. For `nums = [4, -1, 9]` and `target = -1`, the loop matches at index 1 and returns 1. An absent target needs the loop to examine every position first, so the method returns -1 only after `nums.length` comparisons.

The harness counts the comparisons on an absent target and expects exactly `nums.length`. It also checks 2,000 random arrays with negative values against `List.indexOf`.

**Complexity.**

- **Time** is O(n), because an absent target forces all `n` comparisons.
- **Space** is O(1), since the scan keeps only its loop index.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

public final class TargetAbsent {
    /** Records how many positions the last call examined, so the harness can check the full scan. */
    static int examined;

    /**
     * Returns the first index of target, or -1 after a complete scan finds nothing.
     * Time: O(n), because an absent target makes the loop examine all n positions.
     * Space: O(1), because only the index and the harness counter exist.
     * Invariant: before reading nums[i], positions 0..i-1 were examined and none held target.
     */
    static int firstIndexOrAbsent(int[] nums, int target) {
        // The counter belongs to the harness only and does not change the result.
        examined = 0;
        // Visit positions left to right.
        for (int i = 0; i < nums.length; i++) {
            // Count one examined position.
            examined++;
            // A match returns a real index, even when the stored value is -1.
            if (nums[i] == target) return i;
        }
        // Reached only after every position was examined, so absence is proven.
        return -1;
    }

    public static void main(String[] args) {
        // Checks Example 1 and confirms the absent target examines all four positions.
        if (firstIndexOrAbsent(new int[] {3, 2, 2, 3}, 5) != -1) throw new AssertionError("example 1");
        if (examined != 4) throw new AssertionError("an absent target needs the full scan");
        // Checks Example 2: the value -1 at index 1 is a match and returns index 1.
        if (firstIndexOrAbsent(new int[] {4, -1, 9}, -1) != 1) throw new AssertionError("example 2");
        if (examined != 2) throw new AssertionError("the scan stops at the match");
        // Checks the empty array: no position is examined.
        if (firstIndexOrAbsent(new int[] {}, 3) != -1 || examined != 0) throw new AssertionError("empty");
        // Checks 2,000 random arrays that include negative values against List.indexOf.
        Random rnd = new Random(31);
        for (int t = 0; t < 2000; t++) {
            int[] x = new int[rnd.nextInt(9)];
            List<Integer> boxed = new ArrayList<>();
            for (int i = 0; i < x.length; i++) { x[i] = rnd.nextInt(5) - 3; boxed.add(x[i]); }
            int target = rnd.nextInt(7) - 4;
            int expected = boxed.indexOf(target);
            if (firstIndexOrAbsent(x, target) != expected) throw new AssertionError("mismatch on " + Arrays.toString(x));
            if (expected == -1 && examined != x.length) throw new AssertionError("absent needs a full scan");
        }
    }
}
```

#### Solution: [Recognize] Build Array from Permutation (LeetCode 1920)
<!-- id: ar-build-permutation -->

**Approach.** The contract gives every index, so each answer is one direct read and no search happens. For each `i`, the method reads `nums[i]`, uses it as an index into `nums`, and stores the result at position `i` of a new array. The new array is required, because an in-place write at position `i` would replace a value that a later position still needs to read. The harness shows the difference: the in-place version returns a wrong array for `[3, 0, 2, 1]`.

The harness compares the method with a stream-based oracle on 2,000 random permutations.

**Complexity.**

- **Time** is O(n), because each of the `n` positions costs two array reads and one write.
- **Space** is O(n), because the answer is a new array of length `n`, and the contract forbids overwriting the input.

```java run
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.ArrayList;
import java.util.Random;
import java.util.stream.IntStream;

public final class BuildFromPermutation {
    /**
     * Builds ans where ans[i] = nums[nums[i]], without changing nums.
     * Time: O(n), because each position costs a constant number of reads and one write.
     * Space: O(n), because the answer is a separate array.
     * Invariant: while the loop runs, nums still holds its original values.
     */
    static int[] buildArray(int[] nums) {
        // Allocate the answer separately so reads of nums never see overwritten values.
        int[] ans = new int[nums.length];
        // One pass over all positions gives O(n) time.
        for (int i = 0; i < nums.length; i++) {
            // Read the stored value, use it as an index, and write to the same position of ans.
            ans[i] = nums[nums[i]];
        }
        // Return the new array.
        return ans;
    }

    /** The wrong variant: writes into the input while reading it. */
    static int[] buildInPlace(int[] nums) {
        int[] copy = nums.clone();
        for (int i = 0; i < copy.length; i++) copy[i] = copy[copy[i]];
        return copy;
    }

    public static void main(String[] args) {
        // Checks both examples.
        if (!Arrays.equals(buildArray(new int[] {3, 0, 2, 1}), new int[] {1, 3, 2, 0})) throw new AssertionError("example 1");
        if (!Arrays.equals(buildArray(new int[] {1, 2, 0}), new int[] {2, 0, 1})) throw new AssertionError("example 2");
        // Checks the lesson claim: reading and writing the same array gives a different, wrong result.
        if (Arrays.equals(buildInPlace(new int[] {3, 0, 2, 1}), new int[] {1, 3, 2, 0})) throw new AssertionError("in-place differs");
        // Checks that the input stays unchanged after the call.
        int[] input = {3, 0, 2, 1};
        buildArray(input);
        if (!Arrays.equals(input, new int[] {3, 0, 2, 1})) throw new AssertionError("input must not change");
        // Checks a single element, the smallest permutation.
        if (!Arrays.equals(buildArray(new int[] {0}), new int[] {0})) throw new AssertionError("single element");
        // Checks 2,000 random permutations against a stream-based oracle.
        Random rnd = new Random(41);
        for (int t = 0; t < 2000; t++) {
            int n = 1 + rnd.nextInt(8);
            List<Integer> list = new ArrayList<>();
            for (int i = 0; i < n; i++) list.add(i);
            Collections.shuffle(list, rnd);
            int[] x = list.stream().mapToInt(Integer::intValue).toArray();
            int[] expected = IntStream.range(0, n).map(i -> x[x[i]]).toArray();
            if (!Arrays.equals(buildArray(x), expected)) throw new AssertionError("mismatch on " + Arrays.toString(x));
        }
    }
}
```
