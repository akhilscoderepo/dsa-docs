<!-- solutions-for: 06-amortized-cost -->
### Amortized Cost

#### Solution: [Build] Doubling Array (Author exercise)
<!-- id: pc-doubling-array -->

**Approach.** First, track `size`, `capacity` and a running copy count. Second, before each append, test whether `size == capacity`. If so, double the capacity, add `size` to the copy count, and record the new capacity. Third, write the value by increasing `size`. For eight appends the array is full on the second, third and fifth appends. Those resizes take the capacity from 1 to 2, 2 to 4 and 4 to 8. They copy 1, 2 and 4 elements, for a total of 7. Seven copies for eight appends is below one copy per append. The copy sizes double, so they form a geometric series that sums to less than twice the last term. The simulation records the capacities it passes through, so the code produces the list and nothing is counted by hand.

**Complexity.** Time: O(n) for the simulation, because the loop runs once per append and each iteration does constant work. The array itself performs O(n) total copies for `n` appends, so each append costs O(1) amortized. Space: O(log n) for the list of capacities, because the capacity doubles each time and the list holds one entry per doubling.

```java run
import java.util.ArrayList;
import java.util.List;

public final class DoublingArray {
    /**
     * Simulates appends into a doubling array and counts element copies.
     * Time: O(n), because the loop runs once per append with constant work.
     * Space: O(log n), because capacitiesSeen gains one entry per doubling.
     * Invariant: size <= capacity, and copies equals the sum of all earlier sizes at resize.
     */
    static long copies(int appends, List<Integer> capacitiesSeen) {
        // Capacity starts at 1 and size at 0, matching an empty array of one slot.
        int capacity = 1, size = 0;
        // The copy total is a long so that large append counts cannot overflow it.
        long copies = 0;
        // Record the initial capacity, because it is the first capacity that occurs.
        capacitiesSeen.add(capacity);
        // One iteration per append, so the loop itself costs O(n).
        for (int k = 0; k < appends; k++) {
            // A full array has no free slot, so a resize must happen before the write.
            if (size == capacity) {
                // Doubling makes room for as many further appends as there are stored values.
                capacity *= 2;
                // The resize moves every stored value once; this is the only source of copy cost.
                copies += size;
                // Record the new capacity; this is why extra memory grows with the number of doublings.
                capacitiesSeen.add(capacity);
            }
            // The write fills one slot; it is not counted as a copy.
            size++;
        }
        // Return the total copies so the caller can compare it with the number of appends.
        return copies;
    }

    public static void main(String[] args) {
        // Checks Example 1: capacities and total copies for 8 appends.
        List<Integer> caps = new ArrayList<>();
        if (copies(8, caps) != 7) throw new AssertionError("total copies for 8 appends");
        if (!caps.equals(List.of(1, 2, 4, 8))) throw new AssertionError("capacities " + caps);
        // Checks Example 2: the first append needs no resize.
        if (copies(1, new ArrayList<>()) != 0) throw new AssertionError("first append is free");
        // Checks a large run: 2^20 - 1 copies for a million appends is about one copy per append.
        if (copies(1_000_000, new ArrayList<>()) != 1_048_575L) throw new AssertionError("a million appends copy 2^20 - 1 elements, about one per append");
        // Checks the amortized bound: fewer than two copies per append.
        if (!(copies(1_000_000, new ArrayList<>()) < 2L * 1_000_000)) throw new AssertionError("always under two copies per append");
    }
}
```

#### Solution: [Vary] Grow By One (Author exercise)
<!-- id: pc-grow-by-one -->

**Approach.** First, notice that capacity grows by one slot, so the array is full on every append after the first. Second, note that an append that finds `s` stored values copies `s` elements. Third, add these costs over `n` appends: `1 + 2 + ... + (n - 1)`. The sum equals `n(n - 1) / 2`, so eight appends cost 28 copies against 7 for doubling. Fourth, divide by `n`. The cost per append averages about `n / 2`, which is O(n). The policy gives room for only one more append per resize, so no resize pays for later ones. Because of this, it loses the constant amortized bound.

**Complexity.** Time: O(n^2) total copies for `n` appends, because the copy costs form an arithmetic series. That is O(n) amortized per append. Space: O(1) extra for the simulation, because it keeps only integer counters.

```java run
public final class GrowByOne {
    /**
     * Counts element copies when capacity grows by one on each resize.
     * Time: O(n) to simulate, and the array performs O(n^2) copies in total.
     * Space: O(1), because only integer counters are stored.
     * Invariant: size <= capacity, and every append after the first triggers a resize.
     */
    static long copies(int appends) {
        // Capacity starts at 1 and size at 0, as in the doubling exercise.
        int capacity = 1, size = 0;
        // The copy total is a long because it reaches about 5 * 10^9 for 100,000 appends.
        long copies = 0;
        // One iteration per append, so the simulation loop costs O(n).
        for (int k = 0; k < appends; k++) {
            // The array is full, so a resize happens; growth by one makes this true on nearly every append.
            if (size == capacity) { capacity += 1; copies += size; }
            // Copying moves all stored values (size of them), which makes later resizes cost more and more.
            size++;
        }
        // Return the total, which the caller compares with n(n-1)/2.
        return copies;
    }

    public static void main(String[] args) {
        // Checks Example 1 and Example 2.
        if (copies(8) != 28) throw new AssertionError("8 appends");
        if (copies(1) != 0) throw new AssertionError("1 append");
        // Checks the closed formula n(n-1)/2 for every n from 1 to 200.
        for (int n = 1; n <= 200; n++) {
            if (copies(n) != (long) n * (n - 1) / 2) throw new AssertionError("formula at " + n);
        }
        // Checks the cost at scale: the quadratic total is far above the linear total of doubling.
        if (copies(100_000) != 4_999_950_000L) throw new AssertionError("100,000 appends cost about five billion copies");
    }
}
```

#### Solution: [Boundary] One Expensive Append (Author exercise)
<!-- id: pc-one-expensive-append -->

**Approach.** First, observe that after 1,024 values the capacity is exactly 1,024, so the array is full. Second, follow the 1,025th append. It finds no room, doubles the capacity to 2,048 and copies all 1,024 stored values. Third, add the earlier resizes. They copied 1 + 2 + 4 + ... + 512, which is 1,023 elements in total. So the single spike equals the total of every earlier spike plus one. This is a geometric series, so the total copies stay below two per append. One costly call does not break the average, because the previous 1,024 appends already created the room that this resize uses. The code returns both the total and the copies of the last append.

**Complexity.** Time: the spike is O(n) for that one call, and the simulation is O(n) overall, because its loop runs once per append. The total for `n` appends is O(n) copies, so each append costs O(1) amortized. Space: O(1), because the code keeps a few counters.

```java run
public final class OneExpensiveAppend {
    /**
     * Simulates doubling appends and returns {total copies, copies of the last append}.
     * Time: O(n), because the loop runs once per append with constant work.
     * Space: O(1), because only integer counters and a two-element result are stored.
     * Invariant: total equals the sum of all spikes so far, and last is the latest append's cost.
     */
    static long[] copiesAfter(int appends) {
        // Capacity starts at 1 and size at 0; total sums all copies and last tracks the latest append.
        int capacity = 1, size = 0;
        long total = 0, last = 0;
        // One iteration per append, so the loop costs O(n).
        for (int k = 0; k < appends; k++) {
            // Reset the per-append cost so that a cheap append reports 0 copies.
            last = 0;
            // A full array forces a resize; this is the only append that pays a copy cost.
            if (size == capacity) { capacity *= 2; total += size; last = size; }
            // The write itself fills one slot and is not counted as a copy.
            size++;
        }
        // Return both numbers so the caller can compare the spike with the earlier total.
        return new long[] {total, last};
    }

    public static void main(String[] args) {
        // Checks Example 1: the 1,025th append copies 1,024 elements.
        long[] a = copiesAfter(1025);
        if (a[1] != 1024) throw new AssertionError("the 1025th append copies 1024 elements");
        // Checks that all earlier resizes together copied 1,023 elements.
        if (a[0] - a[1] != 1023) throw new AssertionError("all earlier resizes copied 1023 in total");
        // Checks Example 2: after 1,024 appends the last append is cheap, so there is no spike.
        long[] b = copiesAfter(1024);
        if (b[1] != 0) throw new AssertionError("1024 appends end without a spike");
        // Checks the amortized bound: fewer than two copies per append.
        if (!(a[0] < 2L * 1025)) throw new AssertionError("fewer than two copies per append");
    }
}
```

#### Solution: [Recognize] Potential Intuition (Author exercise)
<!-- id: pc-potential-intuition -->

**Approach.** First, look at the array right after a resize to capacity `2c`. It holds `c` values, so exactly `c` slots are empty. That means `c` more appends can happen before the next resize. Second, charge each of those appends 3 units. Spend 1 unit on the write and save 2 units. Third, add the savings. The `c` appends save `2c` units, and the next resize from `2c` to `4c` copies `2c` values. So the saved credit pays for the resize exactly. The first resize from 1 to 2 copies one value. The 2 units saved by the first append fund it, with one unit to spare. The simulation tracks the credit balance and asserts that it never goes negative.

**Complexity.** Time: O(n) for the simulation, because the loop runs once per append. Space: O(1), because the code keeps only `capacity`, `size` and `credit`. The charge of 3 units per append shows that the cost is O(1) amortized.

```java run
public final class PotentialIntuition {
    /**
     * Checks that a charge of 3 units per append always covers writes and copies.
     * Time: O(n), because the loop runs once per append with constant work.
     * Space: O(1), because only three integer variables are stored.
     * Invariant: credit >= 0 after every append.
     */
    public static void main(String[] args) {
        // Capacity starts at 1; credit is the saved balance and starts at 0.
        int capacity = 1, size = 0;
        long credit = 0;
        // Simulate 100,000 appends; one iteration per append gives the O(n) time.
        for (int k = 0; k < 100_000; k++) {
            // Every append is charged 3 units up front.
            credit += 3;                      // charged for this append
            // A full array must resize before the write.
            if (size == capacity) {
                // The resize costs one unit per stored value, paid from the saved credit.
                credit -= size;               // pay for the copy
                // Doubling makes room for as many appends as the array now holds.
                capacity *= 2;
            }
            // The write costs 1 unit; the remaining 2 units of the charge stay saved.
            credit -= 1;                      // pay for the write
            size++;
            // A negative balance would show that 3 units per append is not enough.
            if (credit < 0) throw new AssertionError("credit went negative at append " + (k + 1));
        }
        // Resize from 4 to 8: the two appends since the last resize saved 4 units, and the copy costs 4.
        // Checks the hand calculation from Example 1: saved credit equals the copy cost.
        long saved = 2L * 2, copyCost = 4;
        if (saved != copyCost) throw new AssertionError("saved credit pays for the copy");
    }
}
```
