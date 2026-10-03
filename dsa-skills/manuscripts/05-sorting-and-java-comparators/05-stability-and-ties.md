<!-- lesson-kind: standard -->
<!-- lesson-id: stability-and-ties -->
## Stability And Ties

<!-- stage: context -->
### A Ticket Line With Priority Classes

A concert hall sells seats to three kinds of customers: members, students and the general public. Members are served before students and students before everyone else. The box office keeps a clipboard with customers listed in the order they walked up, and the manager's rule for each class is plain: whoever arrived first is served first. A member who walked up at nine o'clock must not wait behind a member who walked up at ten.

Moving a customer to a different class position is easy. The hard part is what happens to customers in the same class. If the clerk rearranges the clipboard carelessly, the members may come out in a scrambled order, each one still ahead of every student, so the class rule holds and the arrival rule is silently broken. Nobody complains until a member who was first in line finds out they were served last.

<!-- stage: naive -->
### One Pass Per Class

The direct approach is to handle one class at a time. For each class, in priority order, walk down the clipboard from the top and copy every customer of that class to the output.

```java
final class BoxOffice {
    record Customer(String name, int classRank) {}

    static List<Customer> serveByClass(List<Customer> arrivals, int classCount) {
        List<Customer> served = new ArrayList<>();
        for (int rank = 0; rank < classCount; rank++) {
            for (Customer c : arrivals) {
                if (c.classRank() == rank) served.add(c);
            }
        }
        return served;
    }
}
```

Because each pass walks the clipboard from the top, customers of one class come out in arrival order, which is exactly what the manager wants.

<!-- stage: bottleneck -->
### A Pass Per Class Does Not Scale

The clipboard is walked once for every class, so the cost is O(k n) for k classes and n customers. That is fine for three classes. If the priority is an arbitrary integer, there can be as many classes as customers and the cost grows to O(n^2). The method also has to be told the number of classes in advance, and it breaks if a customer has a rank outside the range it expected.

The library sort fixes the cost, at O(n log n), and takes the priority as a comparator. What it does not fix automatically is the second promise, arrival order within a class. Whether it holds depends on a property of the sort itself, and that property differs between sorting an array of objects and sorting an array of plain ints. A programmer who does not know which guarantee applies will write correct-looking code whose tie behavior is an accident of the library version.

<!-- stage: insight -->
### Ties Need An Owner

A **stable sort** keeps elements that compare as equal in the same relative order as in the input. Java's object sorts, `Arrays.sort(Object[])`, `Arrays.sort(T[], Comparator)`, `List.sort` and `Collections.sort`, promise exactly this. The sorting of primitive arrays, such as `Arrays.sort(int[])`, makes no such promise. That is harmless for plain numbers, since two equal ints cannot be told apart, but it matters as soon as the equal items carry something else, such as a name or a position.

The useful habit is to decide who owns each tie. If the problem says that equal keys keep their arrival order, the promise of a stable object sort is enough, and the comparator returns zero on equal keys. If the problem says anything stronger, or the sort used might not be stable, make the tie rule explicit by attaching the **arrival index** to each element and comparing it last. An order that mentions the index is deterministic whatever the algorithm does, and it can be read in the code instead of inferred from library documentation.

<!-- names: stable sort, arrival index, tie ownership -->

A second way to think about the same decision is **tie ownership**: the comparator, the input order, or an extra field must be named as the single thing that decides each tied pair. When no one owns a tie, the answer for that pair is left to chance. A comparator that returns zero is a statement that the two elements are interchangeable in the output, and that statement should be true. The same idea explains the old trick of sorting by the secondary key first and then by the primary key with a stable sort. It works only because of the stability promise, and it breaks silently if the second sort is ever replaced by a primitive one.

<!-- stage: variables -->
### Primary Key, Index And Final Rule

Each element carries a primary key, which the comparator reads, and optionally an original position, which is fixed when the elements are first listed and never changes afterwards. The final rule is the complete comparator: primary key first, then any further keys, then the index when the ties must follow arrival. Nothing in the sort needs to remember anything else. For the trace of a stable insertion, the state is the sorted prefix, and a new element is inserted after every element of an equal key.

<!-- stage: trace -->
### Equal Scores Keep Their Order

The first trace sorts five entries by a score alone, as an ascending order in which equal scores compare as zero. Each entry is inserted after all earlier entries with an equal score, which is what stability means. The step to study is the one for the third entry, which has the same score as the first one and lands right behind it rather than ahead of it.

```trace
{"cells":["ann 3","bob 1","cy 3","di 1","eve 2"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"insert":"ann 3","list":"ann 3"},"note":"Insert ann with score 3. No earlier entry has the same score, so only the scores decide. The list reads ann 3."},{"at":{"i":1},"vars":{"insert":"bob 1","list":"bob 1, ann 3"},"note":"Insert bob with score 1. No earlier entry has the same score, so only the scores decide. The list reads bob 1, ann 3."},{"at":{"i":2},"vars":{"insert":"cy 3","list":"bob 1, ann 3, cy 3"},"note":"Insert cy with score 3. It has the same score as ann, so it goes right after it and arrival order is kept. The list reads bob 1, ann 3, cy 3."},{"at":{"i":3},"vars":{"insert":"di 1","list":"bob 1, di 1, ann 3, cy 3"},"note":"Insert di with score 1. It has the same score as bob, so it goes right after it and arrival order is kept. The list reads bob 1, di 1, ann 3, cy 3."},{"at":{"i":4},"vars":{"insert":"eve 2","list":"bob 1, di 1, eve 2, ann 3, cy 3"},"note":"Insert eve with score 2. No earlier entry has the same score, so only the scores decide. The list reads bob 1, di 1, eve 2, ann 3, cy 3."}]}
```

The second trace orders the numbers 5, 3, 8, 1, 6 by how many one-bits each has in binary, with equal counts ordered by value, written as bits over value. Here ties are owned by an explicit second key, the value, and stability plays no part. The step to study is the insertion of 6, which has two one-bits like 3 and 5 and therefore lands among them, behind 5 because 6 is larger.

```trace
{"cells":["5","3","8","1","6"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"insert":"2/5","order":"2/5"},"note":"Insert 5, which has 2 one-bits. The key is 2 over 5. The order reads 2/5."},{"at":{"i":1},"vars":{"insert":"2/3","order":"2/3, 2/5"},"note":"Insert 3, which has 2 one-bits. The key is 2 over 3. The order reads 2/3, 2/5."},{"at":{"i":2},"vars":{"insert":"1/8","order":"1/8, 2/3, 2/5"},"note":"Insert 8, which has 1 one-bits. The key is 1 over 8. The order reads 1/8, 2/3, 2/5."},{"at":{"i":3},"vars":{"insert":"1/1","order":"1/1, 1/8, 2/3, 2/5"},"note":"Insert 1, which has 1 one-bits. The key is 1 over 1. The order reads 1/1, 1/8, 2/3, 2/5."},{"at":{"i":4},"vars":{"insert":"2/6","order":"1/1, 1/8, 2/3, 2/5, 2/6"},"note":"Insert 6, which has 2 one-bits. The key is 2 over 6. The order reads 1/1, 1/8, 2/3, 2/5, 2/6."}]}
```

<!-- stage: code -->
### Stable Sort, Index Tie And Bit Order

```java
final class TieRules {
    record Entry(String name, int score) {}

    static List<Entry> byScoreKeepingArrival(List<Entry> entries) {
        List<Entry> out = new ArrayList<>(entries);
        out.sort(Comparator.comparingInt(Entry::score));   // zero on ties, stable by contract
        return out;
    }

    static int[] positionsByValue(int[] values) {
        Integer[] pos = new Integer[values.length];
        for (int i = 0; i < pos.length; i++) pos[i] = i;
        Arrays.sort(pos, (i, j) -> values[i] != values[j] ? Integer.compare(values[i], values[j]) : Integer.compare(i, j));
        int[] out = new int[pos.length];
        for (int i = 0; i < out.length; i++) out[i] = pos[i];
        return out;
    }

    static int[] byBitCount(int[] a) {
        Integer[] boxed = new Integer[a.length];
        for (int i = 0; i < a.length; i++) boxed[i] = a[i];
        Arrays.sort(boxed, Comparator.comparingInt(Integer::bitCount).thenComparingInt(x -> x));
        int[] out = new int[a.length];
        for (int i = 0; i < out.length; i++) out[i] = boxed[i];
        return out;
    }
}
```

All three sorts cost O(n log n) comparisons. The positions method needs O(n) extra space for the boxed indices, and the bit-count method boxes the values as well. `Integer.bitCount` is O(1) for a 32-bit value, so the comparator cost does not depend on the numbers.

<!-- stage: applicability -->
### When Equal Elements Are Not Identical

Think about stability whenever two elements can compare as equal while differing in something the output shows: a name, a timestamp, an original position. The invariant is that every tied pair has exactly one owner for its order, and you can name it. If the owner is the input order, use an object sort and write the comparator so that ties return zero. If the owner is a stated rule, put that rule in the comparator.

A false friend is the habit of sorting an array of primitive values together with a parallel array of labels. The two arrays cannot be sorted together by the library, and any attempt to do it by hand tends to lose the tie behavior. Another false friend is trusting a comparator that returns zero for elements that are visibly different. `Comparator.comparing(String::toLowerCase)` treats "Bob" and "bob" as the same, and a sorted set built with it will silently throw one of them away.

In Java, do not infer the tie rule from the current behavior of a particular JDK. Read the API promise, which for object sorts is stability and for primitive sorts is nothing at all, and when the promise is too weak, carry the index. Never use an unstable method on elements with identity.

<!-- stage: exercises -->
### Exercises

#### [Build] Stable Score Sort (Author exercise)
<!-- id: so-stable-score-sort -->

**Prerequisites.** The object-ordering lesson above; lists and records from earlier chapters.

**Problem.** Given entries with a name and a score listed in arrival order, return them ordered by score from lowest to highest, so that entries with equal scores stay in arrival order. Use a comparator that looks at the score only, and explain why the ties come out right.

**Constraints.** 0 <= entries.size() <= 1000 and scores between 0 and 100. Names need not be distinct.

**Example 1.** Input `(ann,3), (bob,1), (cy,3), (di,1)`, output `(bob,1), (di,1), (ann,3), (cy,3)`.

**Example 2.** Input `(x,2), (y,2), (z,2)`, output `(x,2), (y,2), (z,2)`, since all scores tie.

**Hint.** What does the sort of an object list promise about elements the comparator calls equal? What must the comparator return on a tie?

**Changed decision.** First rung: the tie rule is delegated to a documented property of the sort and not written in the comparator.

#### [Vary] Explicit Index Tie (Author exercise)
<!-- id: so-explicit-index-tie -->

**Prerequisites.** The stable-score exercise above.

**Problem.** Given an `int[]` of values, return the original positions of the values in order of increasing value, with ties broken by the smaller position. A plain `int[]` sort cannot give positions, so sort boxed indices with a comparator that mentions the position itself.

**Constraints.** 0 <= values.length <= 1000 and any `int` values. The result must not depend on how stable the sorting method is.

**Example 1.** Input `values = [30, 10, 30, 20, 10]`, output `[1, 4, 3, 0, 2]`.

**Example 2.** Input `values = [7]`, output `[0]`.

**Hint.** What should the comparator look at when two values are equal? Why does sorting the values themselves lose the positions?

**Changed decision.** The tie rule moves from the library's promise into the comparator, by adding the original position as the last key.

#### [Boundary] Comparator Equality (Author exercise)
<!-- id: so-comparator-equality -->

**Prerequisites.** The two exercises above.

**Problem.** Sort words with a comparator that ignores case, and show that it returns zero for words that differ in the output, such as `"Bob"` and `"bob"`. Show that a `TreeSet` built with it drops one of the two, then repair the comparator so that it returns zero only for identical words.

**Constraints.** Words consist of English letters, 1 to 6 characters, and at most 5 words per test. Compare with `String.compareToIgnoreCase` and a final natural-order tie rule.

**Example 1.** Input `["bob", "Bob", "amy"]`, output with the loose comparator: `"Bob"` and `"bob"` may appear in either order depending on the input order.

**Example 2.** Input `["bob", "Bob"]` placed in a `TreeSet` with the loose comparator, output a set of size 1; with the repaired comparator, size 2.

**Hint.** What does the set do when two elements compare as zero? What extra key makes any two different strings compare as nonzero?

**Changed decision.** The comparator is judged by what its zeros mean, so the final key is added until a zero implies identical output.

#### [Recognize] Sort Integers by The Number of 1 Bits (LeetCode 1356)
<!-- id: so-sort-by-bits -->

**Prerequisites.** All three exercises above.

**Problem.** Sort an array of non-negative integers by the number of one-bits in their binary form, ascending. Integers with the same number of one-bits are sorted by their numeric value, ascending.

**Constraints.** 1 <= arr.length <= 500 and 0 <= arr[i] <= 10000. A custom comparator needs boxed values.

**Example 1.** Input `arr = [5, 3, 8, 1, 6]`, output `[1, 8, 3, 5, 6]`.

**Example 2.** Input `arr = [0, 16, 15]`, output `[0, 16, 15]`.

**Hint.** What is the secondary key, and who owns a tie between two equal numbers? Which `Integer` method counts one-bits?

**Changed decision.** The tie rule is part of the specification, so it appears as an explicit second key in the comparator.
