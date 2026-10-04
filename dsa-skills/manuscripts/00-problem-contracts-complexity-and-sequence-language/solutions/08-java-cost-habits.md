<!-- solutions-for: 08-java-cost-habits -->
### Java Library Call Time And Space Costs

#### Solution: [Build] Front Removal (Author exercise)
<!-- id: pc-front-removal -->

**Approach.**

- **`remove(0)`** shifts every later element one position left, as the `ArrayList` documentation states.
- **Moves** for a list of size `s` number `s - 1`, so draining `n` elements moves `(n - 1) + (n - 2) + ... + 0`, which is `n(n - 1) / 2`.
- **Totals** are 10 moves for `n = 5` and about five billion for `n = 100,000`.
- **Read index** leaves the list unchanged, so each step costs one `get` and zero moves.
- **Counting loop** in the code models the shifting and computes the numbers.
- **Real `ArrayList`** drained both ways yields the same elements in the same order, and the code checks it.

**Complexity.**

- **Time** is O(n^2) for draining with `remove(0)`, because the shift counts form the sum `n(n - 1) / 2`. The read-index version takes O(n), because it does one constant-time `get` per element.
- **Space** is O(1) extra for the counting model and for the read index, because each keeps only a few counters.

```java run
import java.util.ArrayList;
import java.util.List;

public final class FrontRemoval {
    /**
     * Counts the element moves made when draining a list of n elements with remove(0).
     * Time: O(n), one loop step per removal. Space: O(1), one counter.
     * Invariant: moves equals the shifts of all removals processed so far.
     */
    static long movesDrainingFront(int n) {
        // A long counter is required because the total is about 5 * 10^9 for n = 100,000.
        long moves = 0;
        // One iteration per removal; size is the list size before that removal.
        // Removing index 0 shifts size - 1 elements, so the sum grows quadratically in n.
        for (int size = n; size > 0; size--) moves += size - 1;   // removing index 0 shifts size - 1 elements
        // The total is n(n - 1) / 2.
        return moves;
    }

    public static void main(String[] args) {
        // Small case: n = 5 gives 4 + 3 + 2 + 1 + 0 = 10 moves.
        if (movesDrainingFront(5) != 10) throw new AssertionError("5 events");
        // Large case: n = 100,000 gives n(n - 1) / 2 moves, which needs a long.
        if (movesDrainingFront(100_000) != 4_999_950_000L) throw new AssertionError("100,000 events");
        List<Integer> a = new ArrayList<>(List.of(10, 20, 30, 40));
        List<Integer> viaRemove = new ArrayList<>();
        // Drain a real ArrayList from the front; each remove(0) shifts the rest left.
        while (!a.isEmpty()) viaRemove.add(a.remove(0));
        List<Integer> b = List.of(10, 20, 30, 40);
        List<Integer> viaIndex = new ArrayList<>();
        // Read the same elements with an index; nothing shifts.
        for (int read = 0; read < b.size(); read++) viaIndex.add(b.get(read));
        // Both methods produce the same elements in the same order; only the cost differs.
        if (!viaRemove.equals(viaIndex)) throw new AssertionError("same events, different cost");
    }
}
```

#### Solution: [Vary] String Construction (Author exercise)
<!-- id: pc-string-construction -->

**Approach.**

- **`String`** is immutable, so `result + ch` creates a new string and copies every old character into it.
- **Copies** at step `k` number `k`, so `n` steps copy `1 + 2 + ... + n`, which is `n(n + 1) / 2`.
- **Totals** are 15 for `n = 5` and about five billion for 100,000.
- **`StringBuilder`** appends into a buffer and grows its capacity geometrically, so most appends copy nothing.
- **Assertions** in the code check three claims: concatenation yields a new object, the old string stays unchanged, and the builder's capacity changes only a few times over a million appends.

**Complexity.**

- **Time** is O(n^2) for concatenation in a loop, because the copy counts form the sum `n(n + 1) / 2`. The builder version takes O(n) in total, because each append costs amortized O(1) when the capacity doubles.
- **Space** is O(n) for the final string in both versions, because the result holds `n` characters.

```java run
public final class StringConstruction {
    /**
     * Counts the characters copied when building a string of n characters with "+" in a loop.
     * Time: O(n), one loop step per appended character. Space: O(1), one counter.
     * Invariant: c equals the copies made by all steps up to and including length len.
     */
    // Step len creates a string of length len and copies all len characters, so c is 1 + 2 + ... + n.
    static long charsCopiedByConcat(int n) { long c = 0; for (int len = 1; len <= n; len++) c += len; return c; }

    public static void main(String[] args) {
        // Small case: 1 + 2 + 3 + 4 + 5 = 15 copies.
        if (charsCopiedByConcat(5) != 15) throw new AssertionError("5 characters");
        // Large case: n(n + 1) / 2 copies, which needs a long.
        if (charsCopiedByConcat(100_000) != 5_000_050_000L) throw new AssertionError("100,000 characters");
        String s = "abc";
        String t = s + "d";
        // Concatenation builds a new object and leaves the old string unchanged.
        if (t == s || !s.equals("abc") || !t.equals("abcd")) throw new AssertionError("concatenation builds a new string and leaves the old one alone");
        StringBuilder sb = new StringBuilder();
        // Track capacity to count how often the buffer grows.
        int capacityChanges = 0, last = sb.capacity();
        // One million appends; each is amortized O(1), and the copying happens only at a resize.
        for (int i = 0; i < 1_000_000; i++) {
            sb.append('x');
            // A capacity change marks a resize, the only moment the builder copies old characters.
            if (sb.capacity() != last) { capacityChanges++; last = sb.capacity(); }
        }
        // All appended characters are present.
        if (sb.length() != 1_000_000) throw new AssertionError("length");
        // Geometric growth keeps the number of resizes small, far below the append count.
        if (capacityChanges > 40) throw new AssertionError("capacity should grow geometrically, saw " + capacityChanges + " changes");
    }
}
```

#### Solution: [Boundary] Primitive Arrays (Author exercise)
<!-- id: pc-primitive-arrays -->

**Approach.**

- **Declaration** of `Arrays.asList` has a varargs parameter of an object type.
- **Type rule** says an `int[]` is not an `Object[]`, so the compiler passes the whole array as one argument.
- **Result** is a list with a single element, the array itself, of type `List<int[]>`.
- **`Arrays.asList(1, 2, 3)`** passes three separate boxed arguments, which form a three-element varargs array, so the list has three elements.
- **Loop** over the array adds each value to a `List<Integer>`, which boxes it.
- **Stream** over the array boxes the values as an alternative, and both options visit every element once.

**Complexity.**

- **Time** is O(1) to wrap the single array, because `asList` stores one reference. Building a real `List<Integer>` takes O(n), because the loop or the stream visits each element once.
- **Space** is O(n) for the real list, because it holds `n` boxed values. The wrapper needs O(1) space.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.IntStream;

public final class PrimitiveArrays {
    public static void main(String[] args) {
        int[] raw = {1, 2, 3};
        // Wrapping an int[] yields a list of one element, because int[] is not an Object[].
        List<int[]> wrapped = Arrays.asList(raw);
        if (wrapped.size() != 1) throw new AssertionError("one element: the array itself");
        // The single element is the very same array object; no copy happens (O(1) wrap).
        if (wrapped.get(0) != raw) throw new AssertionError("the element is the same array object");
        // Three boxed arguments form the varargs array, so the list has three elements.
        if (Arrays.asList(1, 2, 3).size() != 3) throw new AssertionError("three boxed arguments");
        List<Integer> viaLoop = new ArrayList<>();
        // The loop boxes each int once: O(n) time and O(n) space for the new list.
        for (int v : raw) viaLoop.add(v);
        // The stream does the same work: it boxes each int and collects n values.
        List<Integer> viaStream = IntStream.of(raw).boxed().collect(Collectors.toList());
        // Both ways give a real list of the integers 1, 2 and 3.
        if (!viaLoop.equals(List.of(1, 2, 3)) || !viaStream.equals(viaLoop)) throw new AssertionError("a real list of integers");
    }
}
```

#### Solution: [Recognize] Value Equality (Author exercise)
<!-- id: pc-value-equality -->

**Approach.**

- **`==`** on objects compares references, so two strings created with `new String("abc")` are different objects and the result is false.
- **`.equals`** compares contents, so it returns true for the same characters.
- **Content comparison** must use `.equals`, and hash-based collections rely on it, along with `hashCode`, to find a matching key. Chapter 04 builds on that.
- **Self-comparison** with `==` is true, because both names refer to one object.
- **`==` between strings** is unreliable, because literals in the same class may be shared, so the bug appears only sometimes.

**Complexity.**

- **Time** is O(1) for `==`, because it compares two references, and O(L) for `.equals` in the string length, because it may compare every character.
- **Space** is O(1) for both, because neither allocates memory.

```java run
public final class ValueEquality {
    public static void main(String[] args) {
        // new String always allocates a separate object, even for equal contents.
        String a = new String("abc");
        String b = new String("abc");
        // Reference comparison: two separate objects are never ==.
        if (a == b) throw new AssertionError("two new objects are never ==");
        // Value comparison: equals walks the characters (O(L)) and finds a match.
        if (!a.equals(b)) throw new AssertionError("the contents match");
        // Identity of an object with itself: always true, in O(1).
        if (a != a) throw new AssertionError("one object is == to itself");
        // Boxed Integers: the language caches values from -128 to 127, so == works only there.
        Integer small1 = Integer.valueOf(127), small2 = Integer.valueOf(127);
        if (small1 != small2) throw new AssertionError("the language guarantees a cache for -128..127");
        // Outside the cache, equals compares the boxed values, which is the correct test.
        if (!Integer.valueOf(1000).equals(Integer.valueOf(1000))) throw new AssertionError("equals compares boxed values");
    }
}
```
