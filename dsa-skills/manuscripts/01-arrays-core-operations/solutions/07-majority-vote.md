<!-- solutions-for: 07-majority-vote -->
### Majority Vote

#### Solution: [Build] Majority Element (LeetCode 169)
<!-- id: ar-majority-element -->

**Approach.** Keep a candidate and a vote count. When the count is zero, adopt the current element as the candidate, then add one vote if the element matches the candidate and subtract one if it does not. Each mismatch cancels a pair of distinct values, so a value occurring more than half the time cannot be cancelled away, and the candidate at the end is that value. The guarantee of a majority lets the second pass be skipped. The assertions compare the result with a counting oracle on random arrays that are built to contain a majority.

**Complexity.** O(n) time and O(1) extra space.

```java run
import java.util.Random;

public final class MajorityElement {
    static int majority(int[] nums) {
        int candidate = 0, votes = 0;
        for (int v : nums) {
            if (votes == 0) candidate = v;
            votes += (v == candidate) ? 1 : -1;
        }
        return candidate;
    }

    public static void main(String[] args) {
        if (majority(new int[] {4, 4, 7, 4, 1, 4, 4}) != 4) throw new AssertionError("example 1");
        if (majority(new int[] {3}) != 3) throw new AssertionError("example 2");
        Random rnd = new Random(31);
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(15);
            int m = rnd.nextInt(4);
            int need = n / 2 + 1;
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(4);
            for (int placed = 0; placed < need; ) { int p = rnd.nextInt(n); if (a[p] != m) { a[p] = m; } placed = 0; for (int v : a) if (v == m) placed++; }
            if (majority(a) != m) throw new AssertionError("guaranteed majority " + m + " missed");
        }
    }
}
```

#### Solution: [Vary] Verify The Candidate (Author exercise)
<!-- id: ar-verify-candidate -->

**Approach.** Run the vote to get a candidate, then count its occurrences in a second pass and return it only if `2 * count > n`. Without a guarantee, the candidate is merely the only value that could be a majority. The comparison avoids integer-division rounding for odd lengths. An empty array has no candidate worth returning, so the method returns `-1` before the passes. The assertions run against an exhaustive counting oracle over many small arrays.

**Complexity.** O(n) time and O(1) extra space.

```java run
import java.util.Random;

public final class VerifyCandidate {
    static int majorityOrNone(int[] nums) {
        if (nums.length == 0) return -1;
        int candidate = 0, votes = 0;
        for (int v : nums) {
            if (votes == 0) candidate = v;
            votes += (v == candidate) ? 1 : -1;
        }
        int count = 0;
        for (int v : nums) if (v == candidate) count++;
        return 2L * count > nums.length ? candidate : -1;
    }
    static int oracle(int[] nums) {
        for (int x : nums) {
            int c = 0;
            for (int y : nums) if (y == x) c++;
            if (2 * c > nums.length) return x;
        }
        return -1;
    }

    public static void main(String[] args) {
        if (majorityOrNone(new int[] {5, 5, 2, 5, 3}) != 5) throw new AssertionError("example 1");
        if (majorityOrNone(new int[] {1, 2, 1, 2}) != -1) throw new AssertionError("example 2");
        if (majorityOrNone(new int[] {}) != -1) throw new AssertionError("empty");
        Random rnd = new Random(32);
        for (int t = 0; t < 5000; t++) {
            int[] a = new int[rnd.nextInt(10)];
            for (int i = 0; i < a.length; i++) a[i] = rnd.nextInt(3);
            if (majorityOrNone(a) != oracle(a)) throw new AssertionError("disagrees with the oracle");
        }
    }
}
```

#### Solution: [Boundary] No Majority (Author exercise)
<!-- id: ar-no-majority -->

**Approach.** On `[1, 2, 3]` the first element becomes the candidate with one vote, the 2 cancels it to zero, and the 3 then becomes the candidate with one vote. The survivor is 3, but a count finds only one occurrence out of three, so there is no majority. On `[1, 2]` the 1 becomes the candidate and the 2 cancels it, leaving the votes at zero while the stored candidate is still 1. A count of 1 out of 2 is not more than half, so there is no majority there either. The ritual always ends with some candidate, and only the count turns it into an answer.

**Complexity.** O(n) time and O(1) extra space.

```java run
public final class NoMajority {
    static int[] vote(int[] nums) {                    // returns {candidate, votes}
        int candidate = 0, votes = 0;
        for (int v : nums) {
            if (votes == 0) candidate = v;
            votes += (v == candidate) ? 1 : -1;
        }
        return new int[] {candidate, votes};
    }
    static int count(int[] nums, int x) { int c = 0; for (int v : nums) if (v == x) c++; return c; }

    public static void main(String[] args) {
        int[] a = {1, 2, 3};
        int[] ra = vote(a);
        if (ra[0] != 3 || ra[1] != 1) throw new AssertionError("survivor of [1,2,3]");
        if (2 * count(a, ra[0]) > a.length) throw new AssertionError("3 is not a majority");
        int[] b = {1, 2};
        int[] rb = vote(b);
        if (rb[0] != 1 || rb[1] != 0) throw new AssertionError("survivor of [1,2] with votes 0");
        if (2 * count(b, rb[0]) > b.length) throw new AssertionError("1 is not a majority of two");
    }
}
```

#### Solution: [Recognize] Dominant Product Id (Author exercise)
<!-- id: ar-dominant-product-id -->

**Approach.** A majority is not guaranteed in this story, so run the vote and then verify with a second counting pass over the same array. Both passes read the stream sequentially and neither needs a table keyed by id, which is why constant extra space is possible. For `[204, 17, 204, 204, 9, 204]` the vote ends on 204 and the count of four exceeds half of six. For `[1, 2, 3, 4]` the survivor is 4 with one occurrence, which fails the check. The result matches an all-pairs counting oracle on random inputs.

**Complexity.** O(n) time and O(1) extra space.

```java run
import java.util.Random;

public final class DominantProductId {
    static int dominant(int[] lines) {
        int candidate = 0, votes = 0;
        for (int id : lines) {
            if (votes == 0) candidate = id;
            votes += (id == candidate) ? 1 : -1;
        }
        int count = 0;
        for (int id : lines) if (id == candidate) count++;
        return lines.length > 0 && 2L * count > lines.length ? candidate : -1;
    }
    static int oracle(int[] lines) {
        for (int x : lines) { int c = 0; for (int y : lines) if (x == y) c++; if (2 * c > lines.length) return x; }
        return -1;
    }

    public static void main(String[] args) {
        if (dominant(new int[] {204, 17, 204, 204, 9, 204}) != 204) throw new AssertionError("example 1");
        if (dominant(new int[] {1, 2, 3, 4}) != -1) throw new AssertionError("example 2");
        if (dominant(new int[] {}) != -1) throw new AssertionError("no lines");
        Random rnd = new Random(33);
        for (int t = 0; t < 4000; t++) {
            int[] a = new int[rnd.nextInt(12)];
            for (int i = 0; i < a.length; i++) a[i] = rnd.nextInt(3);
            if (dominant(a) != oracle(a)) throw new AssertionError("disagrees with the oracle");
        }
    }
}
```

#### Solution: [Extend] Majority Element II (LeetCode 229)
<!-- id: ar-majority-element-two -->

**Approach.** Generalize cancellation to triples of three distinct values. Keep two candidates and two vote counters. A matching element adds a vote to its candidate. Otherwise, if a counter is zero, the element takes over that candidate slot with one vote, and if both counters are positive, one vote is removed from each, which is the triple of three distinct values being discarded. A value above `n / 3` occurrences survives, because each discarded triple removes at most one copy of it and there are fewer than `n / 3` triples. At most two values can exceed one third, so two slots suffice. A second pass verifies both candidates, since the survivors need not qualify, and the candidates must be distinct before they are counted.

**Complexity.** O(n) time and O(1) extra space.

```java run
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Random;

public final class MajorityElementTwo {
    static List<Integer> majorityThird(int[] nums) {
        int c1 = 0, c2 = 1, v1 = 0, v2 = 0;           // c2 starts different from c1 so a match is never double counted
        for (int x : nums) {
            if (x == c1) v1++;
            else if (x == c2) v2++;
            else if (v1 == 0) { c1 = x; v1 = 1; }
            else if (v2 == 0) { c2 = x; v2 = 1; }
            else { v1--; v2--; }
        }
        int n1 = 0, n2 = 0;
        for (int x : nums) { if (x == c1) n1++; else if (x == c2) n2++; }
        List<Integer> out = new ArrayList<>();
        if (3L * n1 > nums.length) out.add(c1);
        if (3L * n2 > nums.length) out.add(c2);
        return out;
    }
    static List<Integer> oracle(int[] nums) {
        List<Integer> out = new ArrayList<>();
        for (int x : nums) {
            int c = 0;
            for (int y : nums) if (y == x) c++;
            if (3 * c > nums.length && !out.contains(x)) out.add(x);
        }
        Collections.sort(out);
        return out;
    }

    public static void main(String[] args) {
        List<Integer> r1 = majorityThird(new int[] {1, 1, 1, 3, 3, 2, 2, 2});
        Collections.sort(r1);
        if (!r1.equals(List.of(1, 2))) throw new AssertionError("example 1: " + r1);
        if (!majorityThird(new int[] {5}).equals(List.of(5))) throw new AssertionError("example 2");
        Random rnd = new Random(34);
        for (int t = 0; t < 8000; t++) {
            int[] a = new int[1 + rnd.nextInt(12)];
            for (int i = 0; i < a.length; i++) a[i] = rnd.nextInt(4) - 1;      // includes 0 and -1 to stress the initial candidates
            List<Integer> got = majorityThird(a);
            Collections.sort(got);
            if (!got.equals(oracle(a))) throw new AssertionError("disagrees with the oracle on " + java.util.Arrays.toString(a));
        }
    }
}
```
