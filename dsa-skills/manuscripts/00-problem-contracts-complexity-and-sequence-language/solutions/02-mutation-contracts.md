<!-- solutions-for: 02-mutation-contracts -->
### Mutation Contracts

#### Solution: [Build] Meaningful Prefix (Author exercise)
<!-- id: pc-meaningful-prefix -->

**Approach.** The guarantee is that `nums[0..k-1]` holds the kept values in their original order. Nothing else is promised. The slots from `k` onward hold whatever the rewrite left behind. They are unspecified, and the caller must never read them as data. The array's own `length` stays 4, which says nothing about the answer. The returned `k` is the only boundary. When the method removes every element, `k = 0` and the entire array is unspecified.

**Complexity.** O(n) time, O(1) auxiliary space.

```java run
import java.util.Arrays;

public final class MeaningfulPrefix {
    static int removeValue(int[] nums, int target) {
        int write = 0;
        for (int read = 0; read < nums.length; read++) {
            if (nums[read] != target) nums[write++] = nums[read];
        }
        return write;
    }

    public static void main(String[] args) {
        int[] a = {3, 2, 2, 3};
        int k = removeValue(a, 3);
        if (k != 2) throw new AssertionError("k");
        if (!Arrays.equals(Arrays.copyOf(a, k), new int[] {2, 2})) throw new AssertionError("meaningful prefix");
        if (a.length != 4) throw new AssertionError("the array length never shrinks");
        if (a[3] != 3) throw new AssertionError("the suffix keeps a stale leftover value");
        int[] b = {3, 3};
        if (removeValue(b, 3) != 0) throw new AssertionError("everything removed");
    }
}
```

#### Solution: [Vary] Preserve Input (Author exercise)
<!-- id: pc-preserve-input -->

**Approach.** Under a no-mutation contract, build a fresh array of the kept values and never write into `nums`. Correct returned numbers are not enough, because the caller holds the original array and relies on it staying whole. Any other design silently changes data the caller still owns. When the contract is permissive, rewriting in place is valid and saves O(n) memory. The design follows from the contract and not from habit.

**Complexity.** The copying method takes O(n) time and O(n) space for the returned array. The in-place variant takes O(n) time and O(1) auxiliary space.

```java run
import java.util.Arrays;

public final class PreserveInput {
    static int[] withoutValue(int[] nums, int target) {
        int kept = 0;
        for (int v : nums) if (v != target) kept++;
        int[] out = new int[kept];
        int at = 0;
        for (int v : nums) if (v != target) out[at++] = v;
        return out;
    }

    public static void main(String[] args) {
        int[] nums = {4, 1, 4, 2};
        int[] snapshot = nums.clone();
        int[] result = withoutValue(nums, 4);
        if (!Arrays.equals(result, new int[] {1, 2})) throw new AssertionError("result");
        if (!Arrays.equals(nums, snapshot)) throw new AssertionError("input must be untouched");
        if (withoutValue(new int[] {}, 4).length != 0) throw new AssertionError("empty input");
    }
}
```

#### Solution: [Boundary] Aliased Input (Author exercise)
<!-- id: pc-aliased-input -->

**Approach.** The assignment `b = a` copies the reference, not the array, so there is one array object with two names. A write through either name is visible through the other. If the two views must stay independent, take a copy before the call, for example `int[] b = a.clone()`. That call allocates a second array and copies the elements. For an array of primitives the copy is complete. An array of arrays needs a deeper copy.

**Complexity.** Cloning takes O(n) time and O(n) space. Reading or writing through a reference takes O(1) time.

```java run
import java.util.Arrays;

public final class AliasedInput {
    static void setFirst(int[] arr, int value) { arr[0] = value; }

    public static void main(String[] args) {
        int[] a = {1, 2, 3};
        int[] b = a;
        setFirst(a, 9);
        if (b[0] != 9) throw new AssertionError("aliases share one array");
        if (a != b) throw new AssertionError("same object");
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

**Approach.** A method that must hand back `n` values needs at least O(n) memory of any kind, because the result itself has that size. Convention one counts everything, so the total is O(n). Convention two charges only auxiliary space, the working memory beyond the input and the required output. Under it the same method uses O(1), because it adds only a few scalars. A solution description should say which convention it uses. An interviewer who asks for O(1) space almost always means the second.

**Complexity.** O(n) time, O(n) total space counting the result, and O(1) auxiliary space when the result is excluded.

```java run
public final class OutputSpace {
    static int[] doubled(int[] nums) {
        int[] out = new int[nums.length];   // required output: O(n), not auxiliary
        for (int i = 0; i < nums.length; i++) out[i] = nums[i] * 2;   // only scalar working state
        return out;
    }

    public static void main(String[] args) {
        int[] in = {1, 2, 3, 4, 5};
        int[] out = doubled(in);
        if (out.length != in.length) throw new AssertionError("output length is forced to n");
        if (out == in) throw new AssertionError("output is a separate array");
        if (out[4] != 10 || in[4] != 5) throw new AssertionError("values and untouched input");
    }
}
```
