<!-- lesson-kind: standard -->
<!-- lesson-id: comparator-contracts -->
## Comparator Contracts

<!-- stage: context -->
### A Sports Day With Tied Finishers

At a school sports day, a volunteer has to publish the results of the sprint. Runners are listed by finishing time, fastest first. Several children crossed the line within the same hundredth of a second, so the list needs a second rule for them: the child in the lower lane number is listed first. The volunteer writes both rules at the top of the sheet, and anyone who follows them gets the same list.

Her first draft was careless. She wrote that a runner is listed before another "if the time is smaller", and said nothing about equal times. Two helpers reading that sheet disagreed about two tied runners, each saying the other should come first, and a third helper placed a runner above one they had both ranked below. A rule that does not answer every pair, or contradicts itself on a pair, makes a published list depend on who happens to read it.

<!-- stage: naive -->
### Hand-Written Selection With Nested Ifs

The first approach is to write the ordering inside a hand-made sort, with the rule spelled out as a yes-or-no question about two runners.

```java
final class SportsDay {
    record Run(int time, int lane) {}

    static boolean comesBefore(Run a, Run b) {
        if (a.time() != b.time()) return a.time() < b.time();
        return a.lane() < b.lane();
    }

    static Run[] publishBySelection(Run[] runs) {
        Run[] left = runs.clone();
        for (int slot = 0; slot < left.length; slot++) {
            int best = slot;
            for (int j = slot + 1; j < left.length; j++) {
                if (comesBefore(left[j], left[best])) best = j;
            }
            Run tmp = left[slot]; left[slot] = left[best]; left[best] = tmp;
        }
        return left;
    }
}
```

The rule is explicit, tied times fall through to lanes, and the output is the same for every input arrangement as long as no two runners share both time and lane.

<!-- stage: bottleneck -->
### One Rule Welded To One Slow Sort

This is O(n^2) comparisons, and the rule is welded into the loop. A new report, such as lane order first, needs another copy of the sort. The library already sorts in O(n log n) comparisons, and it accepts the rule as a separate object, so the ordering can be changed without touching the sorting.

Handing the rule over is the dangerous step. The library trusts the rule and does no checking beyond a rare exception. A rule that returns 1 for tied runners, or that subtracts two big numbers, produces a list that is wrong in a way no exception reports. For lists above a few dozen elements the library may notice the inconsistency and throw an error about a comparison method violating its general contract, but for small lists it will silently return something. The cost of an unchecked rule is a result nobody can trust, so the rule itself has to be tested the way code is tested.

<!-- stage: insight -->
### Three Laws A Rule Must Obey

A comparator is a function of two elements that returns a negative number, zero or a positive number. The library needs three promises from it. The comparator must be **antisymmetric**: swapping the arguments flips the sign, so `compare(a, b)` and `compare(b, a)` have opposite signs, and both are zero together. It must be **transitive**: if `a` goes before `b` and `b` goes before `c`, then `a` goes before `c`, and the same holds for ties. And a zero result must mean that the two elements are interchangeable for the ordering the problem asks for, so that neither one is better placed than the other.

Most useful orderings are built from a **key chain**: a list of keys examined in turn, where the first key that differs decides and later keys are consulted only for ties. The sports-day sheet is a chain of two keys, time and then lane. Java builds it with `Comparator.comparingInt(...)` for the first key and `.thenComparingInt(...)` for each next one, and `.reversed()` flips only the key it follows. Chained comparators of this kind inherit all three laws from their keys, which is why they are safer than hand-written conditionals.

<!-- names: antisymmetric, transitive, key chain -->

Some comparators are not a chain of ready-made keys, and for those the laws have to be argued. The concatenation rule for the biggest glued number says that string `x` goes before `y` when `x + y` is larger than `y + x`. The argument that it is transitive is that the rule is equivalent to comparing the numbers `x` divided by 10 to the length of `x` minus one, which is an ordinary numeric key in disguise. An ordering that is secretly a key comparison is automatically a total order.

<!-- stage: variables -->
### The Pair, The Keys And The Verdict

A comparison receives two elements and returns a sign. The key chain is an ordered list, and the position of the first key that differs is the only thing that decides the result. The comparator keeps no memory between calls, and it must not depend on anything outside its two arguments, such as a counter or the current time. In the trace, `a` and `b` are the two records, `decidedBy` names the key that settled the question, and the sorted prefix grows by one record at each step.

<!-- stage: trace -->
### Which Key Decided The Order

The first trace inserts four runners, written as time over lane, into a growing sorted list, using the two-key chain. Look at the step where 52 over 1 meets 52 over 4: the times tie, so the first key says nothing and the second key puts lane 1 ahead of lane 4. The notes name the key that decided each comparison.

```trace
{"cells":["52/4","49/2","52/1","47/3"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"insert":"52/4","sortedPrefix":"52/4"},"note":"Insert 52/4. It is the first runner, so nothing is compared. The list is now 52/4."},{"at":{"i":1},"vars":{"insert":"49/2","sortedPrefix":"49/2, 52/4"},"note":"Insert 49/2. 49/2 against 52/4: the time decides, so it moves ahead. The list is now 49/2, 52/4."},{"at":{"i":2},"vars":{"insert":"52/1","sortedPrefix":"49/2, 52/1, 52/4"},"note":"Insert 52/1. 52/1 against 52/4: the lane decides, so it moves ahead; 52/1 against 49/2: the time decides, so it stays behind. The list is now 49/2, 52/1, 52/4."},{"at":{"i":3},"vars":{"insert":"47/3","sortedPrefix":"47/3, 49/2, 52/1, 52/4"},"note":"Insert 47/3. 47/3 against 52/4: the time decides, so it moves ahead; 47/3 against 52/1: the time decides, so it moves ahead; 47/3 against 49/2: the time decides, so it moves ahead. The list is now 47/3, 49/2, 52/1, 52/4."}]}
```

The second trace checks the concatenation comparator on the three strings 3, 30 and 34, one pair at a time. If the laws hold, the three verdicts must fit together into one order with no cycle. They do: 34 beats 3, 3 beats 30, and 34 beats 30, giving the sequence 34, 3, 30. The pair to study is the last one, because it is the one that would expose a cycle if the rule were not transitive.

```trace
{"cells":["3","30","34"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"pair":"3,30","glueXY":"330","glueYX":"303","first":"3"},"note":"Compare 3 with 30. Gluing 3 first gives 330 and gluing 30 first gives 303. The larger string wins, so 3 goes ahead of 30."},{"at":{"i":1},"vars":{"pair":"30,34","glueXY":"3034","glueYX":"3430","first":"34"},"note":"Compare 30 with 34. Gluing 30 first gives 3034 and gluing 34 first gives 3430. The larger string wins, so 34 goes ahead of 30."},{"at":{"i":2},"vars":{"pair":"3,34","glueXY":"334","glueYX":"343","first":"34"},"note":"Compare 3 with 34. Gluing 3 first gives 334 and gluing 34 first gives 343. The larger string wins, so 34 goes ahead of 3."}]}
```

<!-- stage: code -->
### Chains And A Law Checker

```java
final class ComparatorKit {
    record Run(int time, int lane) {}

    static final Comparator<Run> TIME_THEN_LANE =
        Comparator.comparingInt(Run::time).thenComparingInt(Run::lane);

    static final Comparator<String> GLUE_ORDER = (x, y) -> (y + x).compareTo(x + y);

    static <T> boolean obeysLaws(Comparator<T> c, List<T> sample) {
        for (T a : sample) {
            for (T b : sample) {
                if (Integer.signum(c.compare(a, b)) != -Integer.signum(c.compare(b, a))) return false;
                for (T d : sample) {
                    if (c.compare(a, b) <= 0 && c.compare(b, d) <= 0 && c.compare(a, d) > 0) return false;
                }
            }
        }
        return true;
    }
}
```

The chained comparator costs O(1) per comparison, so a sort with it is O(n log n). The checker is a test tool and costs O(m^3) for a sample of m elements, which is fine for a sample of a dozen. It tests antisymmetry for every pair and the no-cycle condition for every triple, and it treats a zero as "not after" in both directions, so ties are covered by the same test.

<!-- stage: applicability -->
### When A Rule Needs A Contract

Write an explicit comparator when the order is different from the natural one, or the elements are objects with several fields. State the invariant as three questions you can answer for any two elements: which comes first, whether swapping the arguments flips the answer, and whether a zero really means the two are interchangeable. Build chains from `comparingInt` and `thenComparing` wherever possible, since each piece has been checked by the library authors.

A false friend is a relation that reads like an order and is not one. "Interval A overlaps interval B" is true for A and B and for B and C while false for A and C, so it is not transitive and cannot be a comparator. Rock-paper-scissors fails the same way. A subtler false friend is a comparator that depends on state, such as a running counter, which can give different answers for the same pair on different calls.

In Java, a comparator that returns a fixed 1 for "not smaller" is wrong for equal elements even when it appears to work. Do not rely on the library throwing; the check for inconsistency happens only in some code paths and only when the lists are long enough. Test your comparator on ties and on extreme values before you trust it.

<!-- stage: exercises -->
### Exercises

#### [Build] Safe Integer Comparator (Author exercise)
<!-- id: so-safe-integer-comparator -->

**Prerequisites.** The ordering-contracts lesson; lists from Chapter 01.

**Problem.** Write a `Comparator<Integer>` that orders integers ascending by calling `Integer.compare`, and use it to sort a `List<Integer>` that holds extreme values. Confirm that the result matches the natural order of the numbers.

**Constraints.** 0 <= list.size() <= 200 and any `int` is allowed. Subtraction is not allowed anywhere in the comparator.

**Example 1.** Input `list = [5, -3, 5, 0]`, output `[-3, 0, 5, 5]`.

**Example 2.** Input `list = [Integer.MAX_VALUE, Integer.MIN_VALUE, -1]`, output `[Integer.MIN_VALUE, -1, Integer.MAX_VALUE]`.

**Hint.** What does `Integer.compare(x, y)` return when `x` is the larger value? Which `List` method accepts a comparator?

**Changed decision.** The comparator becomes a named object that a list can use, in place of the built-in order of a primitive array.

#### [Vary] Chained Keys (Author exercise)
<!-- id: so-chained-keys -->

**Prerequisites.** The safe-comparator exercise above.

**Problem.** A support desk has tickets with a priority and an opening time. Sort them so that the higher priority comes first, and among equal priorities the earlier opening time comes first. Build the order as a chain of two keys rather than with nested conditionals.

**Constraints.** 0 <= tickets.length <= 500, with priority between 1 and 5 and opening times between 0 and 1000000. Two tickets with equal priority and equal time are interchangeable.

**Example 1.** Input tickets `(p=2,t=10), (p=5,t=30), (p=5,t=20)`, output `(5,20), (5,30), (2,10)`.

**Example 2.** Input tickets `(p=3,t=7), (p=3,t=7)`, output both in either order, since they are interchangeable.

**Hint.** Which key is consulted only when the first one ties? Which one of the two keys must be reversed, and which must not?

**Changed decision.** The order now has two keys with opposite directions, so the second key is reached only after a tie on the first.

#### [Boundary] Equal Keys And Extreme Values (Author exercise)
<!-- id: so-equal-keys-extreme -->

**Prerequisites.** The two exercises above.

**Problem.** Write a checker that tests whether a comparator is antisymmetric and transitive on every pair and triple of a sample list, and apply it to a correct comparator and to a comparator that returns 1 for tied values. Include the extreme ints in the sample, and show that a subtraction comparator also fails the checker.

**Constraints.** The sample holds at most 10 integers, including `Integer.MIN_VALUE`, `Integer.MAX_VALUE`, 0 and at least one repeated value.

**Example 1.** Input comparator `Integer::compare`, output: the checker passes.

**Example 2.** Input comparator `(a, b) -> a < b ? -1 : 1`, output: the checker fails, since two equal values each come before the other.

**Hint.** What must `compare(a, a)` return, and what must the signs of `compare(a, b)` and `compare(b, a)` be for a tied pair? Which extreme pair makes subtraction lie?

**Changed decision.** The tests now target ties and the ends of the type, the places where a plausible comparator breaks.

#### [Recognize] Largest Number (LeetCode 179)
<!-- id: so-largest-number-laws -->

**Prerequisites.** All three exercises above, and the earlier largest-number exercise.

**Problem.** Revisit the largest glued number, with the question changed. Implement the glue order as a named `Comparator<String>`, return the largest number as a string, and also prove on the input's own pieces that the comparator is antisymmetric and transitive, by running the checker from the previous exercise on them.

**Constraints.** 1 <= nums.length <= 8 and 0 <= nums[i] <= 100000. Pieces may repeat, and some pairs of different pieces glue to the same string in both orders.

**Example 1.** Input `nums = [12, 121]`, output `"12121"`, and the checker passes.

**Example 2.** Input `nums = [2, 22, 222]`, output `"222222"`, and the three pieces tie with each other.

**Hint.** What does the comparator return for two pieces whose two concatenations are equal? Why does that case matter for the zero rule?

**Changed decision.** The invariant has moved from "find the right order" to "show the order is a valid total order", ties included.
