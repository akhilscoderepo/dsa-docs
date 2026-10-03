<!-- lesson-kind: standard -->
<!-- lesson-id: java-cost-habits -->
## Java Cost Habits

<!-- stage: context -->
### The Job That Only Failed In Production

An engineer builds an event processor that takes events off the front of a list and handles them one at a time, then writes a summary line for each event by appending text to a growing report string. In testing, with a few hundred events, it finishes before she can switch windows. On the first real night, with a hundred thousand events, it is still running when the morning shift arrives.

She re-reads the code and finds no nested loops, so the usual quadratic suspects are absent. The slowness comes from two ordinary-looking library calls, each of which does a large hidden piece of work every time it is called. Writing a correct algorithm is only half of the job in Java, because the other half is knowing what the convenient calls actually do.

<!-- stage: naive -->
### Use Whatever Reads Nicely

The processor, written the way it first reads, looks like this.

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

It is short and obviously correct. Each statement states its intent plainly, `remove(0)` takes the first event and `+` builds text, and a reviewer would have no reason to object. The loop runs once per event, which looks like O(n).

<!-- stage: bottleneck -->
### Two Calls, Each Doing O(n) Work

Draining an `ArrayList` from the front is the first problem. Removing the element at index 0 shifts every later element one position to the left, which the class documents. So the first removal moves `n - 1` elements, the next moves `n - 2`, and the total is `n * (n - 1) / 2`, which is O(n^2). For 100,000 events that is about five billion element moves.

Building a string with `+` in a loop is the second problem. Strings are immutable, so each concatenation creates a brand-new string and copies every character of the old one. After `k` steps the string has about `k` times a constant number of characters, so the total number of characters copied also grows as O(n^2) and reaches billions for a long report. Both costs are invisible in the source, because neither shows up as a loop. The loop count said O(n), and the library calls multiplied it by another factor of `n` each.

<!-- stage: insight -->
### Every Call Has A Cost

Treat every library call in a loop as an operation whose cost must be added to the analysis. The code you write is only part of the work, and the call you do not see may be the dominant part.

A **hidden cost** is work performed by a library operation that does not appear as a loop in your code. The repair here is to replace each costly call with a structure that makes the same step cheap. For front removal, keep a read index and leave the list alone, so taking the next event is O(1). For text building, use `StringBuilder`, whose `append` writes into a buffer that grows geometrically, so the cost per character is amortized constant, by the same argument as the doubling array in the previous lesson.

<!-- names: hidden cost, reference equality, value equality -->

Two more Java facts matter for correctness, not speed. **Reference equality**, written `==` on objects, asks whether two names point to the very same object. **Value equality**, written `.equals(...)`, asks whether two objects hold the same contents. Two `String` objects can have identical characters and still fail `==`. A third trap lives in the type system. `Arrays.asList` takes a varargs list of objects, so handing it an `int[]` produces a list with one element, the array itself, instead of a list of the integers inside.

The invariant is that the cost and meaning of every library call you rely on must be known and included in the claimed bound. Convenience syntax never changes the contract you are supposed to satisfy.

<!-- stage: variables -->
### What To Ask About Each Call

For each library call inside a loop, write three things beside it. First, its cost per call as a function of the sizes involved, and whether that cost is amortized. Second, whether it mutates its input or returns something new. Third, whether it compares by reference or by value, and whether it works on primitives or on boxed objects. A call you cannot describe on those three lines is a call you should look up before relying on it.

<!-- stage: trace -->
### Draining Four Events From The Front

Take a list holding 10, 20, 30 and 40, and drain it with `remove(0)`. The first call removes 10 and shifts the other three values one place left, so three elements move. The second call removes what is now at the front, 20, and shifts the remaining two, so two elements move. The third call removes 30 and shifts the last one. The fourth call removes 40 and has nothing left to shift.

The totals are 3, then 2, then 1, then 0, which is 6 moves in all, and the formula `n * (n - 1) / 2` gives 4 * 3 / 2, which is also 6. With a read index instead, the list is never touched. The index goes from 0 to 3, each event is read in place, and zero elements move. The step to watch is the first call, which moves the most elements. With four events it moves three, and with 100,000 events it moves 99,999, which is why the cost explodes with size and stays invisible on small tests.

```trace
{"cells":[10,20,30,40],"pointers":["removed"],"steps":[{"at":{"removed":0},"vars":{"movedThisCall":3,"totalMoved":3,"readIndexMoves":0},"note":"remove(0) takes 10 and shifts 3 later elements left. Total moved: 3. A read index would have moved nothing."},{"at":{"removed":1},"vars":{"movedThisCall":2,"totalMoved":5,"readIndexMoves":0},"note":"remove(0) takes 20 and shifts 2 later elements left. Total moved: 5. A read index would have moved nothing."},{"at":{"removed":2},"vars":{"movedThisCall":1,"totalMoved":6,"readIndexMoves":0},"note":"remove(0) takes 30 and shifts 1 later element left. Total moved: 6. A read index would have moved nothing."},{"at":{"removed":3},"vars":{"movedThisCall":0,"totalMoved":6,"readIndexMoves":0},"note":"remove(0) takes 40 and shifts 0 later elements left. Total moved: 6. A read index would have moved nothing."}]}
```

<!-- stage: code -->
### Cheaper Versions And A Few Facts

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

The loop makes one pass, so the time is O(n) for the loop plus amortized O(1) per append, which is O(n) in total, and the extra space is the report itself. The two `remove` calls at the end show the overload trap, where an `int` argument removes by position and an object argument removes by value. A `List<Integer>` needs `Integer.valueOf(7)` to remove the value 7, which is easy to get wrong in a hurry.

<!-- stage: applicability -->
### Checking The Calls You Did Not Write

Scan every loop body for library calls and ask the three questions. The invariant is that the cost and meaning of each call you rely on are known and included in the bound you state. Whenever a method name is unfamiliar in a loop, check its documented cost before writing the analysis.

The false friend is familiar syntax. A call that looks like a single step is not automatically constant time, primitive-friendly or value-based. `list.remove(0)` and `string + char` look the same as their cheap cousins, `list.get(0)` and `builder.append(char)`, and they are not.

Two more Java hazards belong on the same list. Boxed collections such as `List<Integer>` cost several times the memory of an `int[]` and add a pointer chase per element, which matters near the million-element limits. And `Arrays.asList(new int[]{1,2,3})` has size 1, not 3, because the array is a single object. The exercises below take each of these in turn.

<!-- stage: exercises -->
### Exercises

#### [Build] Front Removal (Author exercise)
<!-- id: pc-front-removal -->

**Prerequisites.** The hidden-cost questions from this lesson.

**Problem.** Explain why repeatedly calling `ArrayList.remove(0)` to drain `n` elements performs quadratic shifting. Contrast it with maintaining a read index, and state the move counts of both for `n = 5`.

**Constraints.** `1 <= n <= 10^5`. Count one move for each element shifted left. Reading an element by index counts as zero moves.

**Example 1.** Input `n = 5` drained with `remove(0)`, output 10 element moves in total.

**Example 2.** Input `n = 5` drained with a read index, output 0 element moves, since nothing is shifted.

**Hint.** When the first element is removed, which other elements must change position? What is the sum of the shifts across all `n` removals?

**Changed decision.** First rung: replaces a convenient call with an index so that the per-step cost becomes constant.

#### [Vary] String Construction (Author exercise)
<!-- id: pc-string-construction -->

**Prerequisites.** The front-removal exercise above.

**Problem.** Compare `result = result + ch` in a loop with `StringBuilder.append(ch)` for building a string of `n` characters. Explain where the repeated copying occurs and count the characters copied by the concatenation version for `n = 5`.

**Constraints.** `1 <= n <= 10^5`. Count one copy per character moved into a new string. Appending to a builder with spare capacity copies nothing.

**Example 1.** Input `n = 5` using `+` in a loop, output 15 characters copied in total (1 + 2 + 3 + 4 + 5).

**Example 2.** Input `n = 5` using a `StringBuilder` with enough capacity, output 0 repeated copies.

**Hint.** Each time the string is extended, how many old characters are copied into the new string? What does `StringBuilder` do differently when it runs out of room?

**Changed decision.** The costly call moves from list shifting to string copying, and the cure becomes a buffer that grows geometrically.

#### [Boundary] Primitive Arrays (Author exercise)
<!-- id: pc-primitive-arrays -->

**Prerequisites.** The two exercises above.

**Problem.** Evaluate `Arrays.asList(new int[]{1,2,3})`. State why the result is a one-element `List<int[]>` and not a `List<Integer>`, and show a way to get a list of the three integers.

**Constraints.** `Arrays.asList` takes a varargs array of objects. An `int[]` is itself a single object, not an array of objects.

**Example 1.** Input `Arrays.asList(new int[]{1,2,3})`, output a list of size 1 whose only element is the `int[]`.

**Example 2.** Input `Arrays.asList(1, 2, 3)`, output a list of size 3, because three boxed arguments form the varargs array.

**Hint.** Could an `int[]` be treated as an `Object[]`? What does the compiler pass to the varargs parameter when you hand it one array of primitives?

**Changed decision.** The question moves from running time to meaning, because the call compiles and runs and still means something other than intended.

#### [Recognize] Value Equality (Author exercise)
<!-- id: pc-value-equality -->

**Prerequisites.** All three exercises above.

**Problem.** Compare two distinct `String` objects that contain the same characters. Explain why `.equals` expresses value equality while `==` tests reference identity, and say which one a solution should use for contents.

**Constraints.** Create each string with `new String("abc")` so that the two objects are guaranteed to be separate. Use `.equals` for contents.

**Example 1.** Input two separate strings holding "abc", output `==` is false and `.equals` is true.

**Example 2.** Input one string compared with itself, output `==` is true, since both names point to one object.

**Hint.** Does `==` look inside the objects or at where they live? Which operator would a map or a set rely on to find a matching key?

**Changed decision.** The question changes from cost to identity, and the same two characters give two different answers depending on the operator.
