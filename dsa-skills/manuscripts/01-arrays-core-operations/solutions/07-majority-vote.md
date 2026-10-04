<!-- solutions-for: 01-arrays-core-operations -->
### Solutions For Majority Vote

#### Solution: [Build] Majority Element (LeetCode 169)
<!-- id: ar-majority-element -->

**Approach.** The method keeps one `candidate` and one `votes` while it reads the array from left to right. When `votes` is zero, the current element becomes the candidate. Then an element equal to the candidate adds one vote, and a different element removes one vote. A removed vote pairs one copy of the candidate with one different element, and the pair leaves the game. A pair holds at most one copy of the majority value, so a value with more than half of the positions always has unpaired copies at the end. All unpaired copies equal the candidate, so the candidate is the majority value.

The input promises a majority, so the method returns the candidate without a second count. The harness compares the result with a count-based oracle on random arrays that are built to contain a majority.

**Complexity.**

- **Time** is O(n), because one loop reads each element once and does constant work.
- **Space** is O(1), because the method stores only `candidate` and `votes`.

```java run
import java.util.Random;

public final class MajorityElement {
    /**
     * Returns the majority element of an array that is promised to have one.
     * Time: O(n), because the loop reads each element once.
     * Space: O(1), because only candidate and votes are stored.
     * Invariant: the unpaired copies in the prefix all equal candidate, and votes counts them.
     */
    static int majorityElement(int[] nums) {
        // The candidate starts as the first element; votes is zero, so the first loop pass replaces it anyway.
        int candidate = nums[0];
        // votes counts the unpaired copies of the candidate in the prefix read so far.
        int votes = 0;
        // One pass over the array: n iterations with constant work each, which is the O(n) cost.
        for (int v : nums) {
            // Zero votes means no unpaired copies remain, so v starts a new group.
            if (votes == 0) candidate = v;
            // An equal value adds an unpaired copy, and a different value pairs with one and removes it.
            votes += (v == candidate) ? 1 : -1;
        }
        // The promised majority cannot be fully paired, so the candidate is that majority.
        return candidate;
    }

    /**
     * Oracle: counts every value and returns the one above n / 2.
     * Time: O(n^2) here, which is acceptable for small test arrays.
     * Space: O(1).
     */
    static int oracle(int[] nums) {
        // Try every value as the possible majority.
        for (int a : nums) {
            // Count the occurrences of a with a full scan.
            int c = 0;
            for (int b : nums) if (a == b) c++;
            // A count above n / 2 identifies the majority.
            if (c > nums.length / 2) return a;
        }
        // The caller only passes arrays with a majority, so this line is never reached.
        throw new AssertionError("no majority in oracle input");
    }

    public static void main(String[] args) {
        // Checks Example 1 and Example 2.
        if (majorityElement(new int[] {5, 5, 8, 8, 5}) != 5) throw new AssertionError("example 1");
        if (majorityElement(new int[] {7}) != 7) throw new AssertionError("example 2");
        // Checks a majority at the end and a majority at the start.
        if (majorityElement(new int[] {1, 2, 3, 3, 3}) != 3) throw new AssertionError("majority at the end");
        if (majorityElement(new int[] {4, 4, 4, 1, 2}) != 4) throw new AssertionError("majority at the start");
        // Checks 3000 random arrays that contain a forced majority, against the oracle.
        Random rnd = new Random(11);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(15);
            int major = rnd.nextInt(5);
            int[] x = new int[n];
            // Fill more than half of the positions with the majority value, the rest with random values.
            int need = n / 2 + 1;
            for (int i = 0; i < n; i++) x[i] = i < need ? major : rnd.nextInt(5);
            // Shuffle so the majority lands in random positions.
            for (int i = n - 1; i > 0; i--) { int j = rnd.nextInt(i + 1); int tmp = x[i]; x[i] = x[j]; x[j] = tmp; }
            if (majorityElement(x) != oracle(x)) throw new AssertionError("mismatch on random input");
        }
    }
}
```

#### Solution: [Vary] Verify The Candidate (Author exercise)
<!-- id: ar-verify-candidate -->

**Approach.** The method runs the same vote scan, but the result is only a candidate now. A second loop counts how many times the candidate occurs in the array. The method returns the candidate when that count is greater than `n / 2` and returns `-1` otherwise.

The second loop is needed because the scan guarantees only one direction. A true majority always survives, but a survivor of an array without a majority can be a rare value. The harness compares the method with a count-based oracle on random arrays that include many without a majority.

**Complexity.**

- **Time** is O(n), because the vote scan and the counting loop each read the array once.
- **Space** is O(1), because the method stores `candidate`, `votes` and one counter.

```java run
import java.util.Random;

public final class VerifyCandidate {
    /**
     * Returns the majority value, or -1 when no value occurs more than n / 2 times.
     * Time: O(n), because two loops read each element once.
     * Space: O(1), because only three scalars are stored.
     * Invariant: after the scan, a true majority is the candidate; the count loop confirms it.
     */
    static int majorityOrMinusOne(int[] nums) {
        // The candidate and the unpaired-copy count start empty.
        int candidate = nums[0];
        int votes = 0;
        // Vote scan: one pass, constant work per element.
        for (int v : nums) {
            // With no unpaired copies, the current element becomes the candidate.
            if (votes == 0) candidate = v;
            // Equal values add a vote; different values cancel one.
            votes += (v == candidate) ? 1 : -1;
        }
        // Count how often the candidate really occurs, which is the verification pass.
        int occurrences = 0;
        // Second pass: reads each element once, so it adds O(n) time and no memory.
        for (int v : nums) if (v == candidate) occurrences++;
        // Accept the candidate only when it occurs more than half the time.
        return occurrences > nums.length / 2 ? candidate : -1;
    }

    /**
     * Oracle: tries each value with a full count.
     * Time: O(n^2). Space: O(1).
     */
    static int oracle(int[] nums) {
        // Try every value as the majority and count it with a full scan.
        for (int a : nums) {
            int c = 0;
            for (int b : nums) if (a == b) c++;
            // A count above n / 2 is the majority.
            if (c > nums.length / 2) return a;
        }
        // No value passed the threshold.
        return -1;
    }

    public static void main(String[] args) {
        // Checks Example 1 and Example 2.
        if (majorityOrMinusOne(new int[] {9, 4, 9, 9, 2}) != 9) throw new AssertionError("example 1");
        if (majorityOrMinusOne(new int[] {9, 4, 9, 4}) != -1) throw new AssertionError("example 2");
        // Checks that the survivor alone would be wrong: the scan ends on 3 for [1, 2, 3], yet no majority exists.
        if (majorityOrMinusOne(new int[] {1, 2, 3}) != -1) throw new AssertionError("no majority in 1 2 3");
        // Checks 5000 random arrays, most of them without a majority, against the oracle.
        Random rnd = new Random(23);
        for (int t = 0; t < 5000; t++) {
            int[] x = new int[1 + rnd.nextInt(12)];
            for (int i = 0; i < x.length; i++) x[i] = rnd.nextInt(4);
            if (majorityOrMinusOne(x) != oracle(x)) throw new AssertionError("mismatch on random input");
        }
    }
}
```

#### Solution: [Boundary] No Majority (Author exercise)
<!-- id: ar-no-majority -->

**Approach.** The method runs the vote scan and keeps its final `candidate` and `votes`. Then it counts the true occurrences of the candidate with a second loop and returns the three numbers.

For `[1, 2, 3]` the candidate 1 is cancelled by 2, and the zero votes let 3 take over with one vote. The survivor 3 occurs once out of three elements, so the survivor is not a majority. For `[1, 2]` the two values cancel and `votes` ends at zero. Zero final votes means no unpaired copies remain, so the survivor cannot be a majority. A positive final `votes` is also not enough, as the first case shows. Only the count in the second loop proves a majority.

**Complexity.**

- **Time** is O(n), because the scan and the count each read the array once.
- **Space** is O(1), because the method stores three integers and the fixed-size result.

```java run
import java.util.Arrays;
import java.util.Random;

public final class NoMajority {
    /**
     * Returns {candidate, votes, occurrences of candidate} after one vote scan.
     * Time: O(n), because two loops read each element once.
     * Space: O(1), because only the three result numbers are stored.
     * Invariant: votes never goes below zero, and it counts the unpaired copies of candidate.
     */
    static int[] voteState(int[] nums) {
        // Both variables start empty; the first element replaces the candidate.
        int candidate = nums[0];
        int votes = 0;
        // Scan: one constant-cost step per element.
        for (int v : nums) {
            // Zero votes means the element starts a new group.
            if (votes == 0) candidate = v;
            // Add one vote for an equal value, remove one vote for a different value.
            votes += (v == candidate) ? 1 : -1;
        }
        // Count the true occurrences of the survivor in a separate loop.
        int occurrences = 0;
        for (int v : nums) if (v == candidate) occurrences++;
        // Return the three numbers in the order the exercise defines.
        return new int[] {candidate, votes, occurrences};
    }

    public static void main(String[] args) {
        // Checks Example 1: the survivor 3 occurs once, so it is not a majority of three elements.
        if (!Arrays.equals(voteState(new int[] {1, 2, 3}), new int[] {3, 1, 1})) throw new AssertionError("example 1");
        // Checks Example 2: the votes cancel to zero.
        if (!Arrays.equals(voteState(new int[] {1, 2}), new int[] {1, 0, 1})) throw new AssertionError("example 2");
        // Checks the claims on 5000 random arrays: votes is not negative, and zero votes never comes with a majority.
        Random rnd = new Random(5);
        for (int t = 0; t < 5000; t++) {
            int[] x = new int[1 + rnd.nextInt(10)];
            for (int i = 0; i < x.length; i++) x[i] = rnd.nextInt(4);
            int[] r = voteState(x);
            if (r[1] < 0) throw new AssertionError("votes is negative");
            // A true majority forces positive final votes.
            if (r[2] > x.length / 2 && r[1] <= 0) throw new AssertionError("a majority needs positive votes");
            // The final votes never exceed the true occurrences of the survivor.
            if (r[1] > r[2]) throw new AssertionError("votes exceeds occurrences");
        }
    }
}
```

#### Solution: [Recognize] Dominant Product Id (Author exercise)
<!-- id: ar-dominant-product-id -->

**Approach.** The cue is one value that may hold more than half of all positions, together with a request for constant extra space. Both point to the vote scan. The scan keeps one candidate id and a vote count, and it compares ids with `equals`. A second loop counts the candidate and the method returns it only when the count exceeds `n / 2`, otherwise `null`.

Reference comparison with `==` is wrong for strings that are equal but stored as separate objects, so every comparison uses `equals`. The harness asserts this behaviour and compares the method with a map-based oracle on random arrays.

**Complexity.**

- **Time** is O(n), because two loops each read every line once and `equals` on a bounded-length id costs constant time.
- **Space** is O(1), because the method stores one reference, two counters and no map.

```java run
import java.util.HashMap;
import java.util.Map;
import java.util.Random;

public final class DominantProductId {
    /**
     * Returns the id that occurs in more than half of the lines, or null.
     * Time: O(n), because two loops read each line once and ids have bounded length.
     * Space: O(1), because only a candidate reference and two counters are stored.
     * Invariant: the unpaired copies in the prefix all equal candidate, and votes counts them.
     */
    static String dominantId(String[] lines) {
        // The candidate starts empty and votes is zero, so the first line replaces it.
        String candidate = null;
        int votes = 0;
        // Vote scan: one pass with constant work per line.
        for (String id : lines) {
            // Zero votes means no unpaired copies remain, so this id becomes the candidate.
            if (votes == 0) candidate = id;
            // equals compares the characters; == would compare object references.
            votes += id.equals(candidate) ? 1 : -1;
        }
        // Count the candidate in a second pass, because the survivor may not be a majority.
        int occurrences = 0;
        for (String id : lines) if (id.equals(candidate)) occurrences++;
        // Return the id only when it appears in more than half of the lines.
        return occurrences > lines.length / 2 ? candidate : null;
    }

    /**
     * Oracle: a map of counts, which uses O(n) space.
     * Time: O(n). Space: O(n).
     */
    static String oracle(String[] lines) {
        // Count every id in a map.
        Map<String, Integer> counts = new HashMap<>();
        for (String id : lines) counts.merge(id, 1, Integer::sum);
        // Return the id whose count exceeds half of the lines.
        for (Map.Entry<String, Integer> e : counts.entrySet()) if (e.getValue() > lines.length / 2) return e.getKey();
        return null;
    }

    public static void main(String[] args) {
        // Checks the Java claim: equal strings in different objects fail == and pass equals.
        String a = "a7";
        String b = new String("a7");
        if (a == b) throw new AssertionError("separate objects must differ by reference");
        if (!a.equals(b)) throw new AssertionError("equal characters must pass equals");
        // Checks that the method treats separate objects with equal text as the same id.
        String[] objects = {new String("a7"), new String("k2"), new String("a7"), new String("a7"), new String("m5")};
        if (!"a7".equals(dominantId(objects))) throw new AssertionError("separate objects");
        // Checks Example 1 and Example 2.
        if (!"a7".equals(dominantId(new String[] {"a7", "k2", "a7", "a7", "m5"}))) throw new AssertionError("example 1");
        if (dominantId(new String[] {"a7", "k2", "k2", "a7"}) != null) throw new AssertionError("example 2");
        // Checks 5000 random arrays against the map oracle, with ids built as new objects.
        Random rnd = new Random(31);
        for (int t = 0; t < 5000; t++) {
            String[] x = new String[1 + rnd.nextInt(12)];
            for (int i = 0; i < x.length; i++) x[i] = new String("p" + rnd.nextInt(3));
            String got = dominantId(x), want = oracle(x);
            if (got == null ? want != null : !got.equals(want)) throw new AssertionError("mismatch on random input");
        }
    }
}
```

#### Solution: [Extend] Majority Element II (LeetCode 229)
<!-- id: ar-majority-element-ii -->

**Approach.** A value above `n / 3` occurrences can be one of at most two values, so the scan keeps two candidates with two vote counters. An element equal to either candidate adds a vote to that candidate. Otherwise, a candidate with zero votes takes the element and starts with one vote. When both counters are positive and the element matches neither candidate, one copy of each candidate and the new element form a triple of three different values, so both counters drop by one. A triple holds at most one copy of any value, so a value above one third cannot be fully removed by triples, and it survives as one of the two candidates.

The survivors are only candidates, so a second loop counts both. The method returns, in ascending order, every candidate whose count exceeds `n / 3`. The two candidates always differ, and the harness asserts that the result has no duplicate. It compares the method with a map-based oracle on random arrays.

**Complexity.**

- **Time** is O(n), because the scan and the count each read the array once with constant work per element.
- **Space** is O(1) besides the result list, because the method stores two candidates, two counters and two occurrence counters.

```java run
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Random;

public final class MajorityElementTwo {
    /**
     * Returns, in ascending order, every value that occurs more than n / 3 times.
     * Time: O(n), because two loops read each element once.
     * Space: O(1) besides the result, because only four scalars and two counts are stored.
     * Invariant: the unpaired copies in the prefix belong to at most two values, held in c1 and c2.
     */
    static List<Integer> overThird(int[] nums) {
        // Two candidates start as different values with zero votes each.
        int c1 = 0, c2 = 1, v1 = 0, v2 = 0;
        // Vote scan: one pass with constant work per element.
        for (int v : nums) {
            // A match with the first candidate adds one vote to it.
            if (v == c1) v1++;
            // A match with the second candidate adds one vote to it.
            else if (v == c2) v2++;
            // A free first slot takes the element, so the candidates stay different.
            else if (v1 == 0) { c1 = v; v1 = 1; }
            // A free second slot takes the element.
            else if (v2 == 0) { c2 = v; v2 = 1; }
            // Both slots are busy, so one copy of each plus this element forms a triple that is discarded.
            else { v1--; v2--; }
        }
        // Count both survivors in a second pass, because the scan only proposes them.
        int n1 = 0, n2 = 0;
        for (int v : nums) { if (v == c1) n1++; else if (v == c2) n2++; }
        // Keep each survivor whose true count passes n / 3.
        List<Integer> result = new ArrayList<>();
        if (n1 > nums.length / 3) result.add(c1);
        if (n2 > nums.length / 3) result.add(c2);
        // Sort the at most two values so the output order is ascending.
        result.sort(null);
        return result;
    }

    /**
     * Oracle: a map of counts, which uses O(n) space.
     * Time: O(n log n). Space: O(n).
     */
    static List<Integer> oracle(int[] nums) {
        // Count every value in a map.
        Map<Integer, Integer> counts = new HashMap<>();
        for (int v : nums) counts.merge(v, 1, Integer::sum);
        // Collect the values above n / 3 and sort them.
        List<Integer> out = new ArrayList<>();
        for (Map.Entry<Integer, Integer> e : counts.entrySet()) if (e.getValue() > nums.length / 3) out.add(e.getKey());
        out.sort(null);
        return out;
    }

    public static void main(String[] args) {
        // Checks Example 1 and Example 2.
        if (!overThird(new int[] {4, 4, 4, 1, 2, 2, 2, 7}).equals(List.of(2, 4))) throw new AssertionError("example 1");
        if (!overThird(new int[] {1, 2, 3, 4}).isEmpty()) throw new AssertionError("example 2");
        // Checks that a value equal to the starting candidate guess 0 is handled when the array holds only 0.
        if (!overThird(new int[] {0, 0, 0}).equals(List.of(0))) throw new AssertionError("all zeros");
        // Checks 8000 random arrays against the oracle, and that the result never holds a duplicate.
        Random rnd = new Random(41);
        for (int t = 0; t < 8000; t++) {
            int[] x = new int[1 + rnd.nextInt(14)];
            for (int i = 0; i < x.length; i++) x[i] = rnd.nextInt(5);
            List<Integer> got = overThird(x);
            if (!got.equals(oracle(x))) throw new AssertionError("mismatch on random input");
            if (got.size() == 2 && got.get(0).equals(got.get(1))) throw new AssertionError("duplicate in result");
        }
    }
}
```
