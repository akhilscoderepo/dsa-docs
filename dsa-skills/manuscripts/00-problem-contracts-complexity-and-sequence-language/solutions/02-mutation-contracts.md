<!-- solutions-for: 02-mutation-contracts -->
### Mutation Contracts

#### Solution: [Build] Meaningful Prefix (Author exercise)
<!-- id: pc-meaningful-prefix -->

**Approach.** The method keeps two indexes. `read` visits every position once. `write` marks the next free slot of the prefix. The invariant is that `nums[0..write-1]` holds the kept values seen so far, in their original order. When `nums[read]` differs from the target, the method copies it to `nums[write]` and advances `write`. When the loop ends, `write` equals `k`. The guarantee follows from the invariant: `nums[0..k-1]` holds the kept values in order. Nothing else is promised. The slots from `k` onward hold whatever the rewrite left behind, so they are unspecified and the caller must never read them as data. The array's own `length` stays 4 and says nothing about the answer. The returned `k` is the only boundary. When the method removes every element, `k = 0` and the entire array is unspecified.

**Complexity.** Time: O(n), because the loop visits each position once and does O(1) work per position. Space: O(1) auxiliary, because the method keeps two integer indexes and allocates no array.

```java run
import java.util.Arrays;

public final class MeaningfulPrefix {
    /**
     * Removes every occurrence of target by overwriting nums; returns the kept count k.
     * Time: O(n), one pass with O(1) work per position. Space: O(1), two indexes only.
     * Invariant: nums[0..write-1] holds the kept values seen so far, in original order.
     * Postcondition: nums[0..k-1] is the answer; nums[k..] is unspecified.
     */
    static int removeValue(int[] nums, int target) {
        // write is the next free slot of the prefix and the count of kept values.
        int write = 0;
        // Visit every position exactly once; this loop is the whole O(n) cost.
        for (int read = 0; read < nums.length; read++) {
            // Keep only non-target values; write <= read, so the copy never overwrites unread data.
            if (nums[read] != target) nums[write++] = nums[read];
        }
        // The count is the boundary of the meaningful prefix.
        return write;
    }

    public static void main(String[] args) {
        // The sample call returns k = 2 and a prefix of [2, 2].
        int[] a = {3, 2, 2, 3};
        int k = removeValue(a, 3);
        if (k != 2) throw new AssertionError("k");
        if (!Arrays.equals(Arrays.copyOf(a, k), new int[] {2, 2})) throw new AssertionError("meaningful prefix");
        // The array keeps its length, and the suffix keeps a stale value, so only k marks the answer.
        if (a.length != 4) throw new AssertionError("the array length never shrinks");
        if (a[3] != 3) throw new AssertionError("the suffix keeps a stale leftover value");
        // Removing every element gives k = 0.
        int[] b = {3, 3};
        if (removeValue(b, 3) != 0) throw new AssertionError("everything removed");
    }
}
```

#### Solution: [Vary] Preserve Input (Author exercise)
<!-- id: pc-preserve-input -->

**Approach.** Under a no-mutation specification, the method never writes into `nums`. First, one pass counts the kept values, so the method knows the exact length of the result. Second, the method allocates `out` with that length. Third, a second pass copies the kept values into `out` in order. The caller holds the original array and relies on it staying whole. Correct returned numbers are not enough, because any write to `nums` silently changes data the caller still owns. When the specification is permissive, rewriting in place is valid and saves O(n) memory. The design follows from the specification and not from habit.

**Complexity.** Time: O(n), because the method makes two passes and each pass does O(1) work per element. Space: O(n), because the returned array can hold up to n values. The in-place variant takes O(n) time and O(1) auxiliary space.

```java run
import java.util.Arrays;

public final class PreserveInput {
    /**
     * Returns the values of nums that differ from target, in order, without writing to nums.
     * Time: O(n), two passes with O(1) work per element. Space: O(n), for the returned array.
     * Postcondition: nums holds the same values as before the call.
     */
    static int[] withoutValue(int[] nums, int target) {
        // First pass counts the kept values so the result array has the exact size.
        int kept = 0;
        for (int v : nums) if (v != target) kept++;
        // Allocate the result; this is the O(n) space that protects the input.
        int[] out = new int[kept];
        // at is the next free slot of out.
        int at = 0;
        // Second pass copies the kept values in order; it only reads nums.
        for (int v : nums) if (v != target) out[at++] = v;
        return out;
    }

    public static void main(String[] args) {
        // The result is correct, and the input equals its snapshot, so nothing was written to it.
        int[] nums = {4, 1, 4, 2};
        int[] snapshot = nums.clone();
        int[] result = withoutValue(nums, 4);
        if (!Arrays.equals(result, new int[] {1, 2})) throw new AssertionError("result");
        if (!Arrays.equals(nums, snapshot)) throw new AssertionError("input must be untouched");
        // Empty input gives an empty result.
        if (withoutValue(new int[] {}, 4).length != 0) throw new AssertionError("empty input");
    }
}
```

#### Solution: [Boundary] Aliased Input (Author exercise)
<!-- id: pc-aliased-input -->

**Approach.** The assignment `b = a` copies the reference, not the array, so one array object has two names. A write through either name is visible through the other, because both names point to the same elements. If the two views must stay independent, the caller takes a copy before the call, for example `int[] b = a.clone()`. That call allocates a second array and copies the elements. For an array of primitives the copy is complete. An array of arrays needs a deeper copy, because `clone()` copies only the outer references.

**Complexity.** Time: O(n) for the clone, because it copies n elements, and O(1) to read or write one element through a reference. Space: O(n) for the clone, because it allocates a second array of n elements. The assignment `b = a` costs O(1) space, because it copies one reference.

```java run
import java.util.Arrays;

public final class AliasedInput {
    /**
     * Writes value into the first slot of arr.
     * Time: O(1), one element write. Space: O(1), no allocation.
     * The write changes the shared array object, so every alias sees it.
     */
    static void setFirst(int[] arr, int value) { arr[0] = value; }

    public static void main(String[] args) {
        // Aliases: b copies the reference, so a write through a shows through b.
        int[] a = {1, 2, 3};
        int[] b = a;
        setFirst(a, 9);
        if (b[0] != 9) throw new AssertionError("aliases share one array");
        if (a != b) throw new AssertionError("same object");
        // Clone: d is a separate array, so a write through c leaves d unchanged.
        int[] c = {1, 2, 3};
        int[] d = c.clone();
        setFirst(c, 9);
        if (!Arrays.equals(d, new int[] {1, 2, 3})) throw new AssertionError("clone is independent");
        if (c == d) throw new AssertionError("clone is a different object");
    }
}
```

#### Solution: [Recognize] Output Space (Author exercise)
<!-- id: pc-output-space -->

**Approach.** A method that must hand back `n` values needs at least O(n) memory of any kind, because the result itself has that size. Convention one counts everything, so the total is O(n). Convention two charges only auxiliary space, the working memory beyond the input and the required output. Under it the same method uses O(1), because it adds only a few scalars. The two answers describe the same code, so a solution description should say which convention it uses. An interviewer who asks for O(1) space almost always means the second.

**Complexity.** Time: O(n), because the loop writes each of the n result slots once. Space: O(n) total counting the result, because the result array has n slots. Auxiliary space: O(1) when the result is excluded, because the method adds only the loop index.

```java run
public final class OutputSpace {
    /**
     * Returns a new array whose elements are the doubled input values.
     * Time: O(n), one write per result slot. Space: O(n) total, O(1) auxiliary.
     * The result array is required output; only the loop index is working memory.
     */
    static int[] doubled(int[] nums) {
        int[] out = new int[nums.length];   // required output: O(n), not auxiliary
        // One iteration per element; this loop is the whole O(n) time cost.
        for (int i = 0; i < nums.length; i++) out[i] = nums[i] * 2;   // only scalar working state
        return out;
    }

    public static void main(String[] args) {
        // The output has length n and is a separate array, and the input stays unchanged.
        int[] in = {1, 2, 3, 4, 5};
        int[] out = doubled(in);
        if (out.length != in.length) throw new AssertionError("output length is forced to n");
        if (out == in) throw new AssertionError("output is a separate array");
        if (out[4] != 10 || in[4] != 5) throw new AssertionError("values and untouched input");
    }
}
```
