<!-- solutions-for: 05-sorted-deduplication -->
### Sorted Deduplication

#### Solution: [Build] Remove Duplicates from Sorted Array (LeetCode 26)
<!-- id: ar-remove-duplicates -->

**Approach.** Admit the first element automatically, then admit each later element only if it differs from the last written value, which sorted order guarantees is the only place an equal value can be. The write index counts the admitted values, so it is the answer. An empty array returns 0 through the length check. The assertions include the unsorted failure, where adjacent comparison leaves a non-adjacent duplicate in place, and a randomized comparison with a `TreeSet` oracle.

**Complexity.** O(n) time and O(1) extra space.

```java run
import java.util.Arrays;
import java.util.Random;
import java.util.TreeSet;

public final class RemoveDuplicates {
    static int dedupe(int[] nums) {
        if (nums.length == 0) return 0;
        int write = 1;
        for (int read = 1; read < nums.length; read++) if (nums[read] != nums[write - 1]) nums[write++] = nums[read];
        return write;
    }

    public static void main(String[] args) {
        int[] a = {1, 1, 2, 3, 3, 3, 4};
        int k = dedupe(a);
        if (k != 4 || !Arrays.equals(Arrays.copyOf(a, k), new int[] {1, 2, 3, 4})) throw new AssertionError("example 1");
        if (dedupe(new int[] {}) != 0) throw new AssertionError("example 2");
        if (dedupe(new int[] {1, 2, 1}) != 3) throw new AssertionError("unsorted input keeps a non-adjacent duplicate");
        Random rnd = new Random(12);
        for (int t = 0; t < 3000; t++) {
            int[] x = new int[rnd.nextInt(12)];
            for (int i = 0; i < x.length; i++) x[i] = rnd.nextInt(5);
            Arrays.sort(x);
            TreeSet<Integer> expected = new TreeSet<>();
            for (int v : x) expected.add(v);
            int kk = dedupe(x);
            if (kk != expected.size()) throw new AssertionError("count");
            int i = 0;
            for (int v : expected) if (x[i++] != v) throw new AssertionError("order");
        }
    }
}
```

#### Solution: [Vary] Remove Duplicates from Sorted Array II (LeetCode 80)
<!-- id: ar-remove-duplicates-two -->

**Approach.** Admit an element when fewer than two slots are written, or when it differs from `nums[write - 2]`. If the current value equals the value two slots back in the written prefix, then, by sorted order, the two slots behind it both hold that value and a third copy must be skipped. Otherwise at most one copy is in the prefix and the element is admitted. The same method with the limit set to 1 reproduces the previous exercise, which the assertions check.

**Complexity.** O(n) time and O(1) extra space.

```java run
import java.util.Arrays;
import java.util.Random;

public final class RemoveDuplicatesTwo {
    static int keepAtMost(int[] nums, int limit) {
        int write = 0;
        for (int read = 0; read < nums.length; read++) {
            if (write < limit || nums[read] != nums[write - limit]) nums[write++] = nums[read];
        }
        return write;
    }

    static int oracle(int[] sorted, int limit) {
        int count = 0, run = 0;
        for (int i = 0; i < sorted.length; i++) {
            run = (i > 0 && sorted[i] == sorted[i - 1]) ? run + 1 : 1;
            if (run <= limit) count++;
        }
        return count;
    }

    public static void main(String[] args) {
        int[] a = {0, 0, 0, 1, 1, 1, 1, 2};
        int k = keepAtMost(a, 2);
        if (k != 5 || !Arrays.equals(Arrays.copyOf(a, k), new int[] {0, 0, 1, 1, 2})) throw new AssertionError("example 1");
        int[] b = {7, 7, 7};
        if (keepAtMost(b, 2) != 2) throw new AssertionError("example 2");
        int[] c = {1, 1, 2, 3, 3};
        if (keepAtMost(c, 1) != 3) throw new AssertionError("limit 1 matches plain deduplication");
        Random rnd = new Random(14);
        for (int t = 0; t < 3000; t++) {
            int[] x = new int[1 + rnd.nextInt(12)];
            for (int i = 0; i < x.length; i++) x[i] = rnd.nextInt(4);
            Arrays.sort(x);
            int limit = 1 + rnd.nextInt(3);
            int expected = oracle(x, limit);
            if (keepAtMost(x.clone(), limit) != expected) throw new AssertionError("limit " + limit);
        }
    }
}
```

#### Solution: [Boundary] Keep One Per Run (Author exercise)
<!-- id: ar-keep-one-per-run -->

**Approach.** An all-equal array is a single run. The first element is admitted, every later element equals the last kept value, and the result is a count of 1. An already-unique array has one run per element, so every comparison finds a difference and every element is admitted, leaving the array unchanged with a count equal to its length. Neither case needs a special branch, because the loop bounds and the automatic admission of the first element already cover them. A single-element array is the intersection of both cases.

**Complexity.** O(n) time and O(1) extra space.

```java run
import java.util.Arrays;

public final class KeepOnePerRun {
    static int dedupe(int[] nums) {
        if (nums.length == 0) return 0;
        int write = 1;
        for (int read = 1; read < nums.length; read++) if (nums[read] != nums[write - 1]) nums[write++] = nums[read];
        return write;
    }

    public static void main(String[] args) {
        int[] allEqual = {5, 5, 5};
        if (dedupe(allEqual) != 1 || allEqual[0] != 5) throw new AssertionError("one run");
        int[] unique = {1, 2, 3};
        if (dedupe(unique) != 3 || !Arrays.equals(unique, new int[] {1, 2, 3})) throw new AssertionError("all runs");
        int[] single = {9};
        if (dedupe(single) != 1 || single[0] != 9) throw new AssertionError("one element is both extremes");
        int[] big = new int[100_000];
        if (dedupe(big) != 1) throw new AssertionError("a large all-equal array");
    }
}
```

#### Solution: [Recognize] String Compression (LeetCode 443)
<!-- id: ar-string-compression -->

**Approach.** Walk the array run by run. For each run, find its end with a scan, write the character at the write index, and, when the run length is greater than 1, write the digits of the length. The write index can never pass the read index, because a run of length `L` is replaced by at most `1 + digits(L)` characters, which is no longer than `L` when `L` is at least 2, and a run of length 1 is written as one character. So each write lands on a slot that has already been read. The digits of a number are produced by converting the length to characters, which is a small constant amount of work.

**Complexity.** O(n) time and O(1) extra space, since the digit conversion handles at most four digits for lengths up to 2000.

```java run
import java.util.Arrays;

public final class StringCompression {
    static int compress(char[] chars) {
        int write = 0, read = 0;
        while (read < chars.length) {
            char c = chars[read];
            int end = read;
            while (end < chars.length && chars[end] == c) end++;
            int runLength = end - read;
            chars[write++] = c;
            if (runLength > 1) for (char d : Integer.toString(runLength).toCharArray()) chars[write++] = d;
            read = end;
        }
        return write;
    }

    public static void main(String[] args) {
        char[] a = {'a', 'a', 'b', 'c', 'c', 'c'};
        int k = compress(a);
        if (k != 5 || !Arrays.equals(Arrays.copyOf(a, k), new char[] {'a', '2', 'b', 'c', '3'})) throw new AssertionError("example 1");
        char[] b = new char[12];
        Arrays.fill(b, 'x');
        int kb = compress(b);
        if (kb != 3 || !Arrays.equals(Arrays.copyOf(b, kb), new char[] {'x', '1', '2'})) throw new AssertionError("example 2");
        char[] c = {'z'};
        if (compress(c) != 1 || c[0] != 'z') throw new AssertionError("a single character has no count");
        char[] d = new char[2000];
        Arrays.fill(d, 'q');
        int kd = compress(d);
        if (kd != 5 || !new String(d, 0, kd).equals("q2000")) throw new AssertionError("a four-digit count");
    }
}
```
