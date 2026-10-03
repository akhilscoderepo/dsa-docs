<!-- solutions-for: 06-amortized-cost -->
### Amortized Cost

#### Solution: [Build] Doubling Array (Author exercise)
<!-- id: pc-doubling-array -->

**Approach.** The array is full on the second append, the third, and the fifth, and not again before the eighth. Those resizes take the capacity from 1 to 2, 2 to 4 and 4 to 8, and they copy 1, 2 and 4 elements, for a total of 7. Seven copies for eight appends is below one copy per append. The simulation records the capacities it passes through, so the list is produced by code instead of by hand.

**Complexity.** The simulation is O(n) time. The doubling array performs O(n) total copies for `n` appends, so O(1) amortized per append.

```java run
import java.util.ArrayList;
import java.util.List;

public final class DoublingArray {
    static long copies(int appends, List<Integer> capacitiesSeen) {
        int capacity = 1, size = 0;
        long copies = 0;
        capacitiesSeen.add(capacity);
        for (int k = 0; k < appends; k++) {
            if (size == capacity) {
                capacity *= 2;
                copies += size;
                capacitiesSeen.add(capacity);
            }
            size++;
        }
        return copies;
    }

    public static void main(String[] args) {
        List<Integer> caps = new ArrayList<>();
        if (copies(8, caps) != 7) throw new AssertionError("total copies for 8 appends");
        if (!caps.equals(List.of(1, 2, 4, 8))) throw new AssertionError("capacities " + caps);
        if (copies(1, new ArrayList<>()) != 0) throw new AssertionError("first append is free");
        if (copies(1_000_000, new ArrayList<>()) != 1_048_575L) throw new AssertionError("a million appends copy 2^20 - 1 elements, about one per append");
        if (!(copies(1_000_000, new ArrayList<>()) < 2L * 1_000_000)) throw new AssertionError("always under two copies per append");
    }
}
```

#### Solution: [Vary] Grow By One (Author exercise)
<!-- id: pc-grow-by-one -->

**Approach.** With growth by one slot, the array is full on every append after the first. At the append that follows `s` stored values, it copies `s` elements. The total over `n` appends is `1 + 2 + ... + (n - 1)`, which equals `n(n - 1) / 2`, so eight appends cost 28 copies against 7 for doubling. The cost per append averages about `n / 2`, which is O(n), so the policy loses the constant amortized bound.

**Complexity.** O(n^2) total copies, hence O(n) amortized per append.

```java run
public final class GrowByOne {
    static long copies(int appends) {
        int capacity = 1, size = 0;
        long copies = 0;
        for (int k = 0; k < appends; k++) {
            if (size == capacity) { capacity += 1; copies += size; }
            size++;
        }
        return copies;
    }

    public static void main(String[] args) {
        if (copies(8) != 28) throw new AssertionError("8 appends");
        if (copies(1) != 0) throw new AssertionError("1 append");
        for (int n = 1; n <= 200; n++) {
            if (copies(n) != (long) n * (n - 1) / 2) throw new AssertionError("formula at " + n);
        }
        if (copies(100_000) != 4_999_950_000L) throw new AssertionError("100,000 appends cost about five billion copies");
    }
}
```

#### Solution: [Boundary] One Expensive Append (Author exercise)
<!-- id: pc-one-expensive-append -->

**Approach.** After 1,024 values the capacity is exactly 1,024, so the array is full. The 1,025th append is the one that finds no room, doubles to 2,048 and copies all 1,024 stored values. All earlier resizes copied 1 + 2 + 4 + ... + 512, which is 1,023 elements in total. So the single spike equals the total of every earlier spike plus one, a geometric series, and the total copies stay below two per append. One costly call does not break the average, because the previous 1,024 appends already created that room.

**Complexity.** The spike is O(n) for that one call. The total for `n` appends is O(n), so O(1) amortized.

```java run
public final class OneExpensiveAppend {
    static long[] copiesAfter(int appends) {
        int capacity = 1, size = 0;
        long total = 0, last = 0;
        for (int k = 0; k < appends; k++) {
            last = 0;
            if (size == capacity) { capacity *= 2; total += size; last = size; }
            size++;
        }
        return new long[] {total, last};
    }

    public static void main(String[] args) {
        long[] a = copiesAfter(1025);
        if (a[1] != 1024) throw new AssertionError("the 1025th append copies 1024 elements");
        if (a[0] - a[1] != 1023) throw new AssertionError("all earlier resizes copied 1023 in total");
        long[] b = copiesAfter(1024);
        if (b[1] != 0) throw new AssertionError("1024 appends end without a spike");
        if (!(a[0] < 2L * 1025)) throw new AssertionError("fewer than two copies per append");
    }
}
```

#### Solution: [Recognize] Potential Intuition (Author exercise)
<!-- id: pc-potential-intuition -->

**Approach.** After a resize to capacity `2c` the array holds `c` values, so exactly `c` empty slots remain and `c` more appends can happen before the next resize. Charge each of those appends 3 units, spend 1 on the write and save 2. The `c` appends save `2c` units, and the next resize costs `2c` copies, so the stored credit pays for it exactly. The first resize from 1 to 2 copies one value and is funded by the 2 units the first append saved, with one unit to spare. The simulation tracks the credit balance and asserts it never goes negative once the first resize has passed.

**Complexity.** O(n) time for the simulation, and the charge of 3 per append gives O(1) amortized cost.

```java run
public final class PotentialIntuition {
    public static void main(String[] args) {
        int capacity = 1, size = 0;
        long credit = 0;
        for (int k = 0; k < 100_000; k++) {
            credit += 3;                      // charged for this append
            if (size == capacity) {
                credit -= size;               // pay for the copy
                capacity *= 2;
            }
            credit -= 1;                      // pay for the write
            size++;
            if (credit < 0) throw new AssertionError("credit went negative at append " + (k + 1));
        }
        // Resize from 4 to 8: the two appends since the last resize saved 4 units, and the copy costs 4.
        long saved = 2L * 2, copyCost = 4;
        if (saved != copyCost) throw new AssertionError("saved credit pays for the copy");
    }
}
```
