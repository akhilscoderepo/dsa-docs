<!-- solutions-for: 08-java-cost-habits -->
### Java Cost Habits

#### Solution: [Build] Front Removal (Author exercise)
<!-- id: pc-front-removal -->

**Approach.** Removing the element at index 0 shifts every later element one position left, which the `ArrayList` documentation states. Draining `n` elements this way moves `(n - 1) + (n - 2) + ... + 0`, which is `n(n - 1) / 2`, so 10 moves for `n = 5` and about five billion for `n = 100,000`. A read index leaves the list unchanged and costs nothing per step. The code models the shifting with a counting list, so it computes the numbers. Then it checks that a real `ArrayList` drained both ways processes the same elements.

**Complexity.** Front removal is O(n^2) time in total. The read-index version is O(n) time and O(1) extra space.

```java run
import java.util.ArrayList;
import java.util.List;

public final class FrontRemoval {
    static long movesDrainingFront(int n) {
        long moves = 0;
        for (int size = n; size > 0; size--) moves += size - 1;   // removing index 0 shifts size - 1 elements
        return moves;
    }

    public static void main(String[] args) {
        if (movesDrainingFront(5) != 10) throw new AssertionError("5 events");
        if (movesDrainingFront(100_000) != 4_999_950_000L) throw new AssertionError("100,000 events");
        List<Integer> a = new ArrayList<>(List.of(10, 20, 30, 40));
        List<Integer> viaRemove = new ArrayList<>();
        while (!a.isEmpty()) viaRemove.add(a.remove(0));
        List<Integer> b = List.of(10, 20, 30, 40);
        List<Integer> viaIndex = new ArrayList<>();
        for (int read = 0; read < b.size(); read++) viaIndex.add(b.get(read));
        if (!viaRemove.equals(viaIndex)) throw new AssertionError("same events, different cost");
    }
}
```

#### Solution: [Vary] String Construction (Author exercise)
<!-- id: pc-string-construction -->

**Approach.** A `String` is immutable, so `result + ch` creates a new string and copies every old character into it. The copies for `n` steps are `1 + 2 + ... + n`, which is `n(n + 1) / 2`, so 15 for `n = 5` and about five billion for 100,000. A `StringBuilder` appends into a buffer and grows its capacity geometrically, so most appends copy nothing. The code asserts three claims. Concatenation yields a new object. The old string stays unchanged. The builder's capacity changes only a few times over a million appends.

**Complexity.** Concatenation in a loop is O(n^2) time. The builder version is O(n) time with amortized O(1) per append, and O(n) space for the result.

```java run
public final class StringConstruction {
    static long charsCopiedByConcat(int n) { long c = 0; for (int len = 1; len <= n; len++) c += len; return c; }

    public static void main(String[] args) {
        if (charsCopiedByConcat(5) != 15) throw new AssertionError("5 characters");
        if (charsCopiedByConcat(100_000) != 5_000_050_000L) throw new AssertionError("100,000 characters");
        String s = "abc";
        String t = s + "d";
        if (t == s || !s.equals("abc") || !t.equals("abcd")) throw new AssertionError("concatenation builds a new string and leaves the old one alone");
        StringBuilder sb = new StringBuilder();
        int capacityChanges = 0, last = sb.capacity();
        for (int i = 0; i < 1_000_000; i++) {
            sb.append('x');
            if (sb.capacity() != last) { capacityChanges++; last = sb.capacity(); }
        }
        if (sb.length() != 1_000_000) throw new AssertionError("length");
        if (capacityChanges > 40) throw new AssertionError("capacity should grow geometrically, saw " + capacityChanges + " changes");
    }
}
```

#### Solution: [Boundary] Primitive Arrays (Author exercise)
<!-- id: pc-primitive-arrays -->

**Approach.** `Arrays.asList` is declared with a varargs parameter of an object type. An `int[]` is not an `Object[]`, so the compiler treats the whole array as one argument and the list holds a single element, the array. Three separate boxed arguments, as in `Arrays.asList(1, 2, 3)`, form a three-element varargs array and give a three-element list. To turn the primitives in an array into a list, loop over it and add each value, which boxes each one. Alternatively, stream the array and box the values.

**Complexity.** O(1) to wrap the single array. O(n) time and O(n) space to build a real `List<Integer>`.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.IntStream;

public final class PrimitiveArrays {
    public static void main(String[] args) {
        int[] raw = {1, 2, 3};
        List<int[]> wrapped = Arrays.asList(raw);
        if (wrapped.size() != 1) throw new AssertionError("one element: the array itself");
        if (wrapped.get(0) != raw) throw new AssertionError("the element is the same array object");
        if (Arrays.asList(1, 2, 3).size() != 3) throw new AssertionError("three boxed arguments");
        List<Integer> viaLoop = new ArrayList<>();
        for (int v : raw) viaLoop.add(v);
        List<Integer> viaStream = IntStream.of(raw).boxed().collect(Collectors.toList());
        if (!viaLoop.equals(List.of(1, 2, 3)) || !viaStream.equals(viaLoop)) throw new AssertionError("a real list of integers");
    }
}
```

#### Solution: [Recognize] Value Equality (Author exercise)
<!-- id: pc-value-equality -->

**Approach.** `==` on objects compares references, so two strings created with `new String("abc")` are different objects and `==` is false. `.equals` compares contents and returns true. A solution that cares about contents must use `.equals`. Hash-based collections rely on it, along with `hashCode`, to find a matching key, and Chapter 04 builds on that. A string compared with itself is the same object, so `==` is true there. Never rely on `==` between strings, because literals in the same class may be shared, so the bug appears only sometimes.

**Complexity.** `==` is O(1). `.equals` is O(L) in the string length, because it may compare every character.

```java run
public final class ValueEquality {
    public static void main(String[] args) {
        String a = new String("abc");
        String b = new String("abc");
        if (a == b) throw new AssertionError("two new objects are never ==");
        if (!a.equals(b)) throw new AssertionError("the contents match");
        if (a != a) throw new AssertionError("one object is == to itself");
        Integer small1 = Integer.valueOf(127), small2 = Integer.valueOf(127);
        if (small1 != small2) throw new AssertionError("the language guarantees a cache for -128..127");
        if (!Integer.valueOf(1000).equals(Integer.valueOf(1000))) throw new AssertionError("equals compares boxed values");
    }
}
```
