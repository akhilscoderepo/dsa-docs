<!-- lesson-kind: standard -->
<!-- lesson-id: java-cost-habits -->
## Java Cost Habits

<!-- stage: context -->
### Why The Job Fails At Scale

An engineer builds an event processor. It takes events off the front of a list and handles them one at a time. For each event it appends a summary line to a growing report string. In testing, with a few hundred events, it finishes before she can switch windows. On the first real night, with a hundred thousand events, it is still running when the morning shift arrives.

She re-reads the code and finds no nested loops, so the usual quadratic suspects are absent. The slowness comes from two ordinary-looking library calls. Each call does a large piece of work behind the scenes every time it runs. A correct algorithm is only half of the job in Java. The other half is knowing what the convenient calls actually do.

<!-- stage: naive -->
### A Processor That Reads Well

The processor looks like this when you write it the way it first reads.

```java
static String processAll(List<Integer> events) {
    String report = "";
    while (!events.isEmpty()) {
        int event = events.remove(0);
        report = report + "handled " + event + "\n";
    }
    return report;
}
```

It is short and obviously correct. Each statement states its intent plainly. The call `remove(0)` takes the first event, and `+` builds text. A reviewer has no reason to object. The loop runs once per event, so it looks like O(n).

<!-- stage: bottleneck -->
### Two Calls That Each Cost O(n)

#### Front Removal Shifts Elements

Draining an `ArrayList` from the front is the first problem. Removing the element at index 0 shifts every later element one position to the left, as the class documents. So the first removal moves `n - 1` elements, and the next moves `n - 2`. Summed over all `n` removals, the shifts come to `n * (n - 1) / 2`, so the drain costs O(n^2). For 100,000 events that is about five billion element moves.

#### Concatenation Copies Characters

Building a string with `+` in a loop is the second problem. Strings are immutable, so each concatenation creates a brand-new string and copies every character of the old one. After `k` steps the string has about `k` times a constant number of characters. The total number of characters copied therefore also grows as O(n^2), and it reaches billions for a long report. Neither cost shows up as a loop in the source. The loop count said O(n), and each library call multiplied it by another factor of `n`.

<!-- stage: insight -->
### Every Call Has A Cost

#### Add Every Call To The Analysis

Treat every library call in a loop as an operation whose cost you must add to the analysis. The code you write is only part of the work. The call you do not see may be the dominant part.

A **hidden cost** is work that a library operation performs without appearing as a loop in your code. The repair is to replace each costly call with a structure that makes the same step cheap. For front removal, keep a read index and leave the list alone, so taking the next event is O(1). For text building, use `StringBuilder`. Its `append` writes into a buffer that grows geometrically, so the cost per character stays amortized constant, by the same argument as the doubling array in the previous lesson.

<!-- names: hidden cost, reference equality, value equality -->

#### Separate References From Values

Two more Java facts matter for correctness, not speed. **Reference equality**, written `==` on objects, asks whether two names point to the very same object. **Value equality**, written `.equals(...)`, asks whether two objects hold the same contents. Two `String` objects can have identical characters and still fail `==`. A third trap lives in the type system. `Arrays.asList` takes a varargs list of objects. When you pass it an `int[]`, it produces a list with one element, the array itself, instead of a list of the integers inside.

#### State The Invariant

The invariant is that you know the cost and meaning of every library call you rely on, and the claimed bound includes them. Convenience syntax never changes the specification you must satisfy.

<!-- stage: variables -->
### Ask Three Questions About Each Call

For each library call inside a loop, write three things beside it. First, write its cost per call as a function of the sizes involved, and say whether that cost is amortized. Second, say whether it mutates its input or returns something new. Third, say whether it compares by reference or by value, and whether it works on primitives or on boxed objects. If you cannot describe a call on those three lines, look it up before you rely on it.

<!-- stage: trace -->
### Draining Four Events From The Front

#### Drain With remove(0)

Take a list holding 10, 20, 30 and 40, and drain it with `remove(0)`. The first call removes 10 and shifts the other three values one place left, so three elements move. The second call removes 20, which is now at the front, and shifts the remaining two. The third call removes 30 and shifts the last one. The fourth call removes 40 and has nothing left to shift.

#### Compare With A Read Index

The moves are 3, then 2, then 1, then 0, which is 6 in all. The formula `n * (n - 1) / 2` gives 4 * 3 / 2, which is also 6. With a read index, the code never touches the list. The index goes from 0 to 3, each event is read in place, and zero elements move. Watch the first call, because it moves the most elements. With four events it moves three. With 100,000 events it moves 99,999. That is why the cost explodes with size and stays invisible on small tests.

```trace
{"cells":[10,20,30,40],"pointers":["removed"],"steps":[{"at":{"removed":0},"vars":{"movedThisCall":3,"totalMoved":3,"readIndexMoves":0},"note":"remove(0) takes 10 and shifts 3 later elements left. Total moved: 3. A read index would have moved nothing."},{"at":{"removed":1},"vars":{"movedThisCall":2,"totalMoved":5,"readIndexMoves":0},"note":"remove(0) takes 20 and shifts 2 later elements left. Total moved: 5. A read index would have moved nothing."},{"at":{"removed":2},"vars":{"movedThisCall":1,"totalMoved":6,"readIndexMoves":0},"note":"remove(0) takes 30 and shifts 1 later element left. Total moved: 6. A read index would have moved nothing."},{"at":{"removed":3},"vars":{"movedThisCall":0,"totalMoved":6,"readIndexMoves":0},"note":"remove(0) takes 40 and shifts 0 later elements left. Total moved: 6. A read index would have moved nothing."}]}
```

<!-- stage: code -->
### Faster Code And Overload Checks

```java
import java.util.*;

public final class JavaCosts {
    // O(n): a read index replaces repeated front removal. The list itself is never changed.
    static String processAll(List<Integer> events) {
        StringBuilder report = new StringBuilder();
        for (int read = 0; read < events.size(); read++) {
            report.append("handled ").append(events.get(read)).append('\n');
        }
        return report.toString();
    }

    public static void main(String[] args) {
        List<Integer> events = new ArrayList<>(List.of(10, 20, 30));
        if (!processAll(events).equals("handled 10\nhandled 20\nhandled 30\n")) throw new AssertionError("report text");
        if (events.size() != 3) throw new AssertionError("the input list is untouched");
        List<Integer> list = new ArrayList<>(List.of(5, 1, 7));
        list.remove(1);                              // an int argument removes by index
        if (!list.equals(List.of(5, 7))) throw new AssertionError("remove(int) removes an index");
        list.remove(Integer.valueOf(7));             // an object argument removes by value
        if (!list.equals(List.of(5))) throw new AssertionError("remove(Object) removes a value");
    }
}
```

The loop makes one pass. The time is O(n) for the loop plus amortized O(1) per append, so O(n) in total. The extra space is the report itself. The two `remove` calls at the end show the overload trap. An `int` argument removes by position, and an object argument removes by value. A `List<Integer>` needs `Integer.valueOf(7)` to remove the value 7, which is easy to get wrong in a hurry.

<!-- stage: applicability -->
### Checking The Calls You Did Not Write

Scan every loop body for library calls and ask the three questions. The invariant is that you know the cost and meaning of each call you rely on, and the bound you state includes them. When a method name in a loop is unfamiliar, check its documented cost before you write the analysis.

The false friend is familiar syntax. A call that looks like a single step is not automatically constant time, primitive-friendly or value-based. The calls `list.remove(0)` and `string + char` look like their cheap cousins, `list.get(0)` and `builder.append(char)`, but they cost far more.

Two more Java hazards belong on the same list. Boxed collections such as `List<Integer>` cost several times the memory of an `int[]` and add a pointer chase per element, which matters near the million-element limits. Also, `Arrays.asList(new int[]{1,2,3})` has size 1, not 3, because the array is a single object. The exercises below take each of these in turn.

<!-- stage: exercises -->
### Exercises

#### [Build] Front Removal (Author exercise)
<!-- id: pc-front-removal -->

**Prerequisites.** The hidden-cost questions from this lesson.

**Problem.** An `ArrayList` holds `n` elements. Method A removes every element by calling `remove(0)` until the list is empty. Method B reads the elements in order with an index that runs from 0 to `n - 1`, and it does not change the list. A move is one element copied one position to the left inside the list. Compute the total number of moves for each method when `n = 5`. Then explain why the total for Method A grows with the square of `n`.

**Constraints.** `1 <= n <= 10^5`. The list holds `n` elements at the start. Calling `remove(0)` on a list of size `s` moves `s - 1` elements. Reading an element by index counts as zero moves. The total fits in a `long`, because the largest total is about 5 * 10^9, which exceeds the `int` range.

**Example 1.** Input `n = 5` drained with `remove(0)`, output 10 element moves in total.

**Example 2.** Input `n = 5` drained with a read index, output 0 element moves, since nothing is shifted.

**Hint.** When the first element is removed, which other elements must change position? What is the sum of the shifts across all `n` removals?

**Changed decision.** An index replaces a convenient call, so the cost per step becomes constant.

#### [Vary] String Construction (Author exercise)
<!-- id: pc-string-construction -->

**Prerequisites.** The front-removal exercise above.

**Problem.** Method A builds a string of `n` characters. It starts with an empty `String` and runs `result = result + ch` once for each character. Method B appends the same `n` characters to a `StringBuilder`. A copy is one character written into a newly created string. Compute the total number of copies made by Method A when `n = 5`. Then explain at which step Method A copies old characters, and why Method B avoids most copies.

**Constraints.** `1 <= n <= 10^5`. Each step adds exactly one `char`. A `String` is immutable, so each `+` creates a new string and copies every old character into it. Appending to a `StringBuilder` with spare capacity copies nothing. The total for Method A fits in a `long`.

**Example 1.** Input `n = 5` using `+` in a loop, output 15 characters copied in total (1 + 2 + 3 + 4 + 5).

**Example 2.** Input `n = 5` using a `StringBuilder` with enough capacity, output 0 repeated copies.

**Hint.** Each time the string is extended, how many old characters are copied into the new string? What does `StringBuilder` do differently when it runs out of room?

**Changed decision.** The costly call moves from list shifting to string copying, and the cure becomes a buffer that grows geometrically.

#### [Boundary] Primitive Arrays (Author exercise)
<!-- id: pc-primitive-arrays -->

**Prerequisites.** The two exercises above.

**Problem.** Consider the call `Arrays.asList(new int[]{1,2,3})`. Determine the size and the element type of the list it returns. Explain why the result is a `List<int[]>` with one element and not a `List<Integer>` with three elements. Then give a way to build a `List<Integer>` that holds the integers 1, 2 and 3.

**Constraints.** `Arrays.asList` takes a varargs parameter of an object type. An `int[]` is a single object, and it is not an `Object[]`, because `int` is a primitive type. A `List<Integer>` stores boxed values. Boxing converts each `int` to an `Integer`. Building the `List<Integer>` from an array of length `n` takes O(n) time and O(n) space.

**Example 1.** Input `Arrays.asList(new int[]{1,2,3})`, output a list of size 1 whose only element is the `int[]`.

**Example 2.** Input `Arrays.asList(1, 2, 3)`, output a list of size 3, because three boxed arguments form the varargs array.

**Hint.** Could an `int[]` be treated as an `Object[]`? What does the compiler pass to the varargs parameter when you hand it one array of primitives?

**Changed decision.** The question moves from running time to meaning, because the call compiles and runs but means something other than intended.

#### [Recognize] Value Equality (Author exercise)
<!-- id: pc-value-equality -->

**Prerequisites.** All three exercises above.

**Problem.** Two `String` objects hold the same characters, and they are separate objects in memory. Value equality means the two strings contain the same characters in the same order. Reference identity means both names refer to one object. Determine the result of `==` and of `.equals` for the two strings. State which operator tests value equality. Then determine the result of `==` when a string is compared with itself.

**Constraints.** Create each string with `new String("abc")`, which always returns a new object. Each string has length 3. `==` on two object references returns true only if they refer to the same object. `.equals` on two `String` values returns true if and only if their characters match. Use `.equals` to compare contents. `==` takes O(1) time. `.equals` takes O(L) time for strings of length L.

**Example 1.** Input two separate strings holding "abc", output `==` is false and `.equals` is true.

**Example 2.** Input one string compared with itself, output `==` is true, since both names point to one object.

**Hint.** Does `==` look inside the objects or at where they live? Which operator would a map or a set rely on to find a matching key?

**Changed decision.** The question changes from cost to identity, and the same two characters give two different answers depending on the operator.
