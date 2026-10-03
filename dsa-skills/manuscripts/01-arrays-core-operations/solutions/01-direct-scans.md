<!-- solutions-for: 01-direct-scans -->
### Direct Scans

#### Solution: [Build] First Match (Author exercise)
<!-- id: ar-first-match -->

**Approach.** Walk the indices from 0 upward and return the first one whose value equals the target. Before each look, everything earlier is known not to match, so the first match is the earliest. If the loop ends, the invariant covers the whole array and `-1` is proven correct. An empty array runs the loop zero times and returns `-1` with no special branch. The assertions also check that sorting a copy gives a different, wrong index for the same input.

**Complexity.** O(n) time and O(1) extra space.

```java run
import java.util.Arrays;

public final class FirstMatch {
    static int firstIndex(int[] nums, int target) {
        for (int i = 0; i < nums.length; i++) if (nums[i] == target) return i;
        return -1;
    }
    static int firstIndexViaSort(int[] nums, int target) {
        int[] sorted = nums.clone();
        Arrays.sort(sorted);
        for (int i = 0; i < sorted.length; i++) if (sorted[i] == target) return i;
        return -1;
    }

    public static void main(String[] args) {
        if (firstIndex(new int[] {7, 4, 7}, 7) != 0) throw new AssertionError("example 1");
        if (firstIndex(new int[] {}, 3) != -1) throw new AssertionError("example 2");
        if (firstIndex(new int[] {4, 1, 7, 7}, 7) != 2) throw new AssertionError("trace run");
        if (firstIndexViaSort(new int[] {7, 4, 7}, 7) == 0) throw new AssertionError("the sorted copy reports a rearranged position");
        int[] original = {9, 3, 9};
        int[] snapshot = original.clone();
        firstIndex(original, 3);
        if (!Arrays.equals(original, snapshot)) throw new AssertionError("input untouched");
    }
}
```

#### Solution: [Vary] Last Match (Author exercise)
<!-- id: ar-last-match -->

**Approach.** Scan from the back, so the first match met is the last occurrence, and return it. An early exit at the first match from the front would be wrong, because a later match could exist. Scanning from the back keeps the early exit legitimate. An alternative is to scan forward and overwrite an `answer` variable on every match, which also touches every element once. Both versions return `-1` when no element matches.

**Complexity.** O(n) time and O(1) extra space.

```java run
public final class LastMatch {
    static int lastIndex(int[] nums, int target) {
        for (int i = nums.length - 1; i >= 0; i--) if (nums[i] == target) return i;
        return -1;
    }
    static int lastIndexForward(int[] nums, int target) {
        int answer = -1;
        for (int i = 0; i < nums.length; i++) if (nums[i] == target) answer = i;
        return answer;
    }

    public static void main(String[] args) {
        if (lastIndex(new int[] {7, 4, 7}, 7) != 2) throw new AssertionError("example 1");
        if (lastIndex(new int[] {1}, 9) != -1) throw new AssertionError("example 2");
        java.util.Random rnd = new java.util.Random(11);
        for (int t = 0; t < 2000; t++) {
            int[] a = new int[rnd.nextInt(9)];
            for (int i = 0; i < a.length; i++) a[i] = rnd.nextInt(4);
            int target = rnd.nextInt(5);
            if (lastIndex(a, target) != lastIndexForward(a, target)) throw new AssertionError("two directions disagree");
        }
    }
}
```

#### Solution: [Boundary] Target Absent (Author exercise)
<!-- id: ar-target-absent -->

**Approach.** Return `-1` only after the loop finishes, because only then does the invariant cover every element. A return after one or two failures would be a guess. For an empty array the loop condition is false immediately, so the method falls through to `-1` and the contract is satisfied without a special case. Duplicates and ordering play no role, since the scan examines one element at a time.

**Complexity.** O(n) time and O(1) extra space, with every element examined exactly once in the absent case.

```java run
public final class TargetAbsent {
    static int firstIndex(int[] nums, int target, int[] examined) {
        for (int i = 0; i < nums.length; i++) {
            examined[0]++;
            if (nums[i] == target) return i;
        }
        return -1;
    }

    public static void main(String[] args) {
        int[] counter = new int[1];
        if (firstIndex(new int[] {3, 2, 2, 3}, 5, counter) != -1) throw new AssertionError("absent target");
        if (counter[0] != 4) throw new AssertionError("all four elements are examined before -1 is justified");
        counter[0] = 0;
        if (firstIndex(new int[] {}, 3, counter) != -1 || counter[0] != 0) throw new AssertionError("empty array");
        counter[0] = 0;
        if (firstIndex(new int[] {3, 2, 2, 3}, 2, counter) != 1 || counter[0] != 2) throw new AssertionError("early exit on a match");
    }
}
```

#### Solution: [Recognize] Build Array From Permutation (LeetCode 1920)
<!-- id: ar-build-permutation -->

**Approach.** Each value of `nums` is a valid index, because the input is a permutation of `0..n-1`. For every position `i`, read `nums[i]`, use it as an index, and write the value found there into `ans[i]`. Nothing is searched. The allocation of `ans` is the output required by the problem, so under the usual convention the extra working space is O(1). The checks verify the examples and a property: building the array twice with the inverse relationship round-trips on a small permutation.

**Complexity.** O(n) time and O(n) space for the required output, O(1) auxiliary.

```java run
import java.util.Arrays;

public final class BuildPermutation {
    static int[] build(int[] nums) {
        int[] ans = new int[nums.length];
        for (int i = 0; i < nums.length; i++) ans[i] = nums[nums[i]];
        return ans;
    }

    public static void main(String[] args) {
        if (!Arrays.equals(build(new int[] {2, 0, 1}), new int[] {1, 2, 0})) throw new AssertionError("example 1");
        if (!Arrays.equals(build(new int[] {0}), new int[] {0})) throw new AssertionError("example 2");
        int[] identity = {0, 1, 2, 3};
        if (!Arrays.equals(build(identity), identity)) throw new AssertionError("identity maps to itself");
        int[] p = {1, 2, 0};
        int[] twice = build(build(p));
        if (!Arrays.equals(twice, new int[] {1, 2, 0})) throw new AssertionError("this permutation returns to itself after two builds");
        int[] sorted = build(p).clone();
        Arrays.sort(sorted);
        if (!Arrays.equals(sorted, new int[] {0, 1, 2})) throw new AssertionError("the result is again a permutation of 0..n-1");
    }
}
```
