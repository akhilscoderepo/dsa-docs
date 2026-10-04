<!-- lesson-kind: standard -->
<!-- lesson-id: java-cost-habits -->
## Time Complexity Of Common Java Methods

<!-- stage: context -->
### Why Library Calls Dominate Running Time

An engineer builds an event processor. It takes events off the front of a list and handles them one at a time. For each event it appends a summary line to a growing report string. In testing, with a few hundred events, it finishes in milliseconds. On the first real night, with a hundred thousand events, it is still running hours later.

She re-reads the code and finds no nested loops, so no nested loop explains quadratic time. The slowness comes from two ordinary-looking library calls. Each call performs O(n) work internally every time it runs. A correct algorithm also needs the true cost of every library call it uses. In Java, that means knowing what each convenient call does.

<!-- stage: naive -->
### An Event Processor Built From Simple Calls

The processor below is the direct first implementation.

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
### Two Library Calls That Take Linear Time

```predict
The loop runs once per event. What does the whole processor cost for 100,000 events, given what `remove(0)` and `+` do on each call?

The cost is O(n^2), not O(n). Both calls do work proportional to the current size on every call, so the drain moves about five billion elements and the report building copies billions of characters.
```

#### Removing From The Front Shifts Elements

Draining an `ArrayList` from the front is the first problem. Removing the element at index 0 shifts every later element one position to the left, as the class documents. So the first removal moves `n - 1` elements, and the next moves `n - 2`. Summed over all `n` removals, the shifts come to `n * (n - 1) / 2`, so the drain costs O(n^2). For 100,000 events that is about five billion element moves.

#### Concatenating Strings Copies Every Character

Building a string with `+` in a loop is the second problem. Strings are immutable, so each concatenation creates a new string object and copies every character of the old one. After `k` steps the string has about `k` times a constant number of characters. The total number of characters copied therefore also grows as O(n^2), and it reaches billions for a long report. Neither cost shows up as a loop in the source. The loop count said O(n), and each library call multiplied it by another factor of `n`.

<!-- stage: insight -->
### Counting The Cost Of Each Library Call

#### Add Each Call's Cost To The Total

Treat every library call in a loop as an operation whose cost you must add to the analysis. The code you write is only part of the work. The call you do not see may be the dominant part.

The cost of a library call is the time and memory it uses internally, without appearing as a loop in your code. **Amortized** cost is the total cost of a sequence of calls divided by the number of calls. The repair is to replace each costly call with a structure that makes the same step cheap. For front removal, keep a read index and leave the list alone, so taking the next event is O(1). For text building, use `StringBuilder`. Its `append` writes into a buffer that grows by a constant factor each time it fills, so the cost per character stays amortized constant, by the same argument as the doubling array in the amortized cost lesson of this chapter.

<!-- names: amortized, reference equality, value equality -->

#### Comparing Objects By Reference Or Value

Two more Java facts matter for correctness, not speed. The first is how objects compare. **Reference equality**, written `==` on objects, asks whether two names point to the very same object. **Value equality**, written `.equals(...)`, asks whether two objects hold the same contents. Two `String` objects can have identical characters and still fail `==`. The second fact lives in the type system. `Arrays.asList` takes a varargs list of objects. When you pass it an `int[]`, it produces a list with one element, the array itself, instead of a list of the integers inside.

#### State What You Know About Each Call

Before you rely on a library call, find out what it costs and what it means, and include that cost in the bound you claim. Convenience syntax never changes the specification you must satisfy.

<!-- stage: variables -->
### Three Facts To Write Beside Each Call

Write three facts beside each library call inside a loop.

- **Cost per call** is a function of the sizes involved, and you state whether it is amortized.
- **Mutation** states whether the call changes its input or returns a new object.
- **Equality and types** state whether the call compares by reference or by value, and whether it works on primitives or boxed objects.

If you cannot describe a call by these three facts, read its documentation before you rely on it.

<!-- stage: trace -->
### Tracing A Drain With remove(0)

#### Counting Moves For Each remove(0) Call

Take a list holding 10, 20, 30 and 40, and drain it with `remove(0)`.

The first call removes 10 and shifts the other 3 values one place left. The second call removes 20, now at the front, and shifts the remaining 2. The third call removes 30 and shifts the last 1. The fourth call removes 40 and shifts 0.

#### Comparing The Total With A Read Index

The total moves are 3 + 2 + 1 + 0 = 6. The formula `n * (n - 1) / 2` agrees, because 4 * 3 / 2 = 6. A read index goes from 0 to 3, reads each event in place and moves 0 elements.

The first call moves the most elements: 3 for four events and 99,999 for 100,000 events.

The cost grows quadratically with size, so it stays invisible on small tests.

```trace
{"cells":[10,20,30,40],"pointers":["removed"],"steps":[{"at":{"removed":0},"vars":{"movedThisCall":3,"totalMoved":3,"readIndexMoves":0},"note":"remove(0) takes 10 and shifts 3 later elements left. Total moved: 3. A read index would have moved nothing."},{"at":{"removed":1},"vars":{"movedThisCall":2,"totalMoved":5,"readIndexMoves":0},"note":"remove(0) takes 20 and shifts 2 later elements left. Total moved: 5. A read index would have moved nothing."},{"at":{"removed":2},"vars":{"movedThisCall":1,"totalMoved":6,"readIndexMoves":0},"note":"remove(0) takes 30 and shifts 1 later element left. Total moved: 6. A read index would have moved nothing."},{"at":{"removed":3},"vars":{"movedThisCall":0,"totalMoved":6,"readIndexMoves":0},"note":"remove(0) takes 40 and shifts 0 later elements left. Total moved: 6. A read index would have moved nothing."}]}
```

<!-- stage: code -->
### The Fixed Processor And Two remove Methods

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

- **Time** is O(n), because the loop makes one pass and each append costs amortized O(1).
- **Space** is O(n) extra, because the report string holds every line.
- **`remove(int)`** removes by position.
- **`remove(Object)`** removes by value, so a `List<Integer>` needs `Integer.valueOf(7)` to remove the value 7.

In the code, the variable `read` is the read index from the previous stages. The two `remove` calls at the end of the code show the trap in the last two bullets.

<!-- stage: applicability -->
### Checking Library Calls Inside Loops

Apply this checklist to every loop body.

First, list the library calls in the loop body, and give each one the three facts. Next, check the documented cost of any unfamiliar method name before the analysis. Throughout, the invariant holds that you know the cost and meaning of each call you rely on, and the stated bound includes them.

Familiar syntax is the false friend here, because code that looks like a safe pattern often is not. A call that looks like a single step is not automatically constant time, primitive-friendly or value-based. The calls `list.remove(0)` and `string + char` look like `list.get(0)` and `builder.append(char)`, but they cost far more.

Two more Java hazards belong on the same list.

A `List<Integer>` costs several times the memory of an `int[]` and adds one pointer dereference per element, which matters when inputs reach a million elements. The call `Arrays.asList(new int[]{1,2,3})` has size 1, not 3, because the array is a single object.

The exercises below practice these checks.

<!-- stage: exercises -->
### Exercises

#### [Build] Front Removal (Author exercise)
<!-- id: pc-front-removal -->

**Prerequisites.** The three facts about library calls from this lesson.

**Problem.** An `ArrayList` holds `n` elements. Method A removes every element by calling `remove(0)` until the list is empty. Method B reads the elements in order with an index that runs from 0 to `n - 1`, and it does not change the list. A move is one element copied one position to the left inside the list. Compute the total number of moves for each method when `n = 5`. Then explain why the total for Method A grows with the square of `n`.

**Constraints.** The limits are:
- **`n`** satisfies `1 <= n <= 10^5`, and the list holds `n` elements at the start.
- **`remove(0)`** on a list of size `s` moves `s - 1` elements.
- **Index read** counts as zero moves.
- **Total** fits in a `long`, because the largest total is about 5 * 10^9, which exceeds the `int` range.

**Example 1.** Input `n = 5` drained with `remove(0)`, output 10 element moves in total.

**Example 2.** Input `n = 5` drained with a read index, output 0 element moves, since nothing is shifted.

**Hint.** When the first element is removed, which other elements must change position? What is the sum of the shifts across all `n` removals?

**Changed decision.** An index replaces a convenient call, so the cost per step becomes constant.

#### [Vary] String Construction (Author exercise)
<!-- id: pc-string-construction -->

**Prerequisites.** The front-removal exercise above.

**Problem.** Method A builds a string of `n` characters. It starts with an empty `String` and runs `result = result + ch` once for each character. Method B appends the same `n` characters to a `StringBuilder`. A copy is one character written into a newly created string. Compute the total number of copies made by Method A when `n = 5`. Then explain at which step Method A copies old characters, and why Method B avoids most copies.

**Constraints.** The limits are:
- **`n`** satisfies `1 <= n <= 10^5`.
- **Step** adds exactly one `char`.
- **Total** for Method A fits in a `long`.

**Example 1.** Input `n = 5` using `+` in a loop, output 15 characters copied in total (1 + 2 + 3 + 4 + 5).

**Example 2.** Input `n = 5` using a `StringBuilder` with enough capacity, output 0 repeated copies.

**Hint.** Each time the string is extended, how many old characters are copied into the new string? What does `StringBuilder` do differently when it runs out of room?

**Changed decision.** The costly call moves from list shifting to string copying, and the cure becomes a buffer that grows by a constant factor.

#### [Boundary] Primitive Arrays (Author exercise)
<!-- id: pc-primitive-arrays -->

**Prerequisites.** The two exercises above.

**Problem.** Consider the call `Arrays.asList(new int[]{1,2,3})`. Determine the size and the element type of the list it returns. Explain why the result is a `List<int[]>` with one element and not a `List<Integer>` with three elements. Then give a way to build a `List<Integer>` that holds the integers 1, 2 and 3. Building the `List<Integer>` from an array of length `n` takes O(n) time and O(n) space.

**Constraints.** The limits are:
- **`Arrays.asList`** takes a varargs parameter of an object type.
- **`int[]`** is a single object and is not an `Object[]`, because `int` is a primitive type.
- **`List<Integer>`** stores boxed values, and boxing converts each `int` to an `Integer`.

**Example 1.** Input `Arrays.asList(new int[]{1,2,3})`, output a list of size 1 whose only element is the `int[]`.

**Example 2.** Input `Arrays.asList(1, 2, 3)`, output a list of size 3, because three boxed arguments form the varargs array.

**Hint.** Could an `int[]` be treated as an `Object[]`? What does the compiler pass to the varargs parameter when you hand it one array of primitives?

**Changed decision.** The question moves from running time to meaning, because the call compiles and runs but means something other than intended.

#### [Recognize] Value Equality (Author exercise)
<!-- id: pc-value-equality -->

**Prerequisites.** All three exercises above.

**Problem.** Two `String` objects hold the same characters, and they are separate objects in memory. Value equality means the two strings contain the same characters in the same order. Reference equality means both names refer to one object. Determine the result of `==` and of `.equals` for the two strings. State which operator tests value equality. Then determine the result of `==` when a string is compared with itself. The operator `==` takes O(1) time, and `.equals` takes O(L) time for strings of length L.

**Constraints.** The limits are:
- **Creation** uses `new String("abc")`, which always returns a new object.
- **Length** is 3 for each string.
- **`==`** on two object references returns true only if they refer to the same object.
- **`.equals`** on two `String` values returns true if and only if their characters match.

**Example 1.** Input two separate strings holding "abc", output `==` is false and `.equals` is true.

**Example 2.** Input one string compared with itself, output `==` is true, since both names point to one object.

**Hint.** Does `==` look inside the objects or at where they live? Which operator would a map or a set rely on to find a matching key?

**Changed decision.** The question changes from cost to identity, and the same two characters give two different answers depending on the operator.
