<!-- solutions-for: 08-java-cost-habits -->
### Java Cost Habits

#### Solution: [Build] Front Removal (Author exercise)
<!-- id: pc-front-removal -->

**Approach.** First, recall what `remove(0)` does. It shifts every later element one position left, as the `ArrayList` documentation states. Second, sum the moves. A list of size `s` moves `s - 1` elements, so draining `n` elements moves `(n - 1) + (n - 2) + ... + 0`, which is `n(n - 1) / 2`. That gives 10 moves for `n = 5` and about five billion for `n = 100,000`. Third, compare with the read index. It leaves the list unchanged, so each step costs one `get` and zero moves. The code models the shifting with a counting loop, so it computes the numbers. Then it checks that a real `ArrayList` drained both ways yields the same elements in the same order.

**Complexity.** Time: O(n^2) for draining with `remove(0)`, because the shift counts form the sum `n(n - 1) / 2`. The read-index version takes O(n) time, because it does one constant-time `get` per element. Space: O(1) extra for the counting model and for the read index, because each keeps only a few counters.

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

**Approach.** First, note that a `String` is immutable. The expression `result + ch` therefore creates a new string and copies every old character into it. Second, sum the copies. Step `k` copies the new string of length `k`, so `n` steps copy `1 + 2 + ... + n`, which is `n(n + 1) / 2`. That gives 15 for `n = 5` and about five billion for 100,000. Third, compare with `StringBuilder`. It appends into a buffer and grows its capacity geometrically, so most appends copy nothing. The code asserts three claims. Concatenation yields a new object. The old string stays unchanged. The builder's capacity changes only a few times over a million appends.

**Complexity.** Time: O(n^2) for concatenation in a loop, because the copy counts form the sum `n(n + 1) / 2`. The builder version takes O(n) time in total, because each append costs amortized O(1) when the capacity doubles. Space: O(n) for the final string in both versions, because the result holds `n` characters.

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

**Approach.** First, read the declaration. `Arrays.asList` has a varargs parameter of an object type. Second, apply the type rule. An `int[]` is not an `Object[]`, so the compiler passes the whole array as one argument. The list therefore holds a single element, the array itself, and its type is `List<int[]>`. Third, contrast with `Arrays.asList(1, 2, 3)`. Three separate boxed arguments form a three-element varargs array, so the list has three elements. Fourth, build a real `List<Integer>`. Loop over the array and add each value, which boxes it. Alternatively, stream the array and box the values. Both options visit every element once.

**Complexity.** Time: O(1) to wrap the single array, because `asList` stores one reference. Time: O(n) to build a real `List<Integer>`, because the loop or the stream visits each element once. Space: O(n) for the real list, because it holds `n` boxed values. The wrapper needs O(1) space.

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

**Approach.** First, apply the rule for `==` on objects. It compares references, so two strings created with `new String("abc")` are different objects and `==` is false. Second, apply the rule for `.equals`. It compares contents, so it returns true for the same characters. A solution that cares about contents must use `.equals`. Hash-based collections rely on it, along with `hashCode`, to find a matching key, and Chapter 04 builds on that. Third, compare a string with itself. Both names refer to one object, so `==` is true. Never rely on `==` between strings, because literals in the same class may be shared. As a result, the bug appears only sometimes.

**Complexity.** Time: `==` is O(1), because it compares two references. `.equals` is O(L) in the string length, because it may compare every character. Space: O(1) for both, because neither allocates memory.

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
