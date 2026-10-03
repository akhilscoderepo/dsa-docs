<!-- lesson-kind: standard -->
<!-- lesson-id: ordering-contracts -->
## Ordering Contracts

<!-- stage: context -->
### A Ferry Master And The Loading Plan

A ferry master has forty trucks waiting at the dock and one rule for the deck: lighter trucks go on first, so the heavy ones end up near the ramp where the crew can unload them quickly. He has a clipboard with each truck's weight, and he can walk up to any two trucks and say which of them is lighter. That is all he is able to do. He cannot look at the whole queue at once and see the answer.

Two things make his job possible. Any two trucks can be told apart or declared equal, so no pair leaves him stuck. And his judgements agree with each other: if truck A is lighter than B and B is lighter than C, then A is lighter than C, and he never needs to be told so. A deck plan comes out of repeated pairwise judgements, and a plan that two supervisors can both reproduce depends on those two properties.

<!-- stage: naive -->
### Pick The Lightest Remaining Truck

The direct plan is to scan the queue for the lightest truck, put it on the deck, and repeat with whatever is left. In Java, with the weights in an `int[]`, it looks like this.

```java
static int[] loadingPlanBySelection(int[] weights) {
    int[] left = weights.clone();
    int[] plan = new int[left.length];
    for (int slot = 0; slot < plan.length; slot++) {
        int best = slot;
        for (int j = slot + 1; j < left.length; j++) {
            if (left[j] < left[best]) best = j;
        }
        int tmp = left[slot]; left[slot] = left[best]; left[best] = tmp;
        plan[slot] = left[slot];
    }
    return plan;
}
```

It works on every input, including an empty queue, and it never touches the caller's array because it sorts a clone.

<!-- stage: bottleneck -->
### Quadratic Scans And A Hidden Trap

The inner loop rescans the entire unplaced part of the queue for every slot, so the work is about n squared over two comparisons, which is O(n^2). With fifty thousand trucks that is over a billion comparisons, far too slow for a typical time limit. Library sorting needs O(n log n) comparisons, because each comparison is spent on a decision that later comparisons are allowed to reuse.

The second problem is quieter. The code above compares with `<`, which only works because the elements are primitives. The moment the order is something other than the natural numeric one, such as heaviest first or lightest by some derived key, the comparison has to be passed to the library as a function, and writing that function by hand is where bugs enter. The tempting version returns `a - b`, which is wrong whenever the difference does not fit in 32 bits. The cost is not speed but silently wrong output, with no exception and no warning.

<!-- stage: insight -->
### An Order Is A Promise You Make

Sorting is only allowed to be fast because the order you give it is a **total order**: any two elements can be compared, equal elements are interchangeable for the purpose of the answer, and the relation is transitive, so a verdict about A and B plus a verdict about B and C settles A against C without another look. Every fast sorting algorithm leans on that promise. If the promise is broken, the algorithm is not wrong, you are, and the result is whatever the algorithm happens to produce.

In Java the promise is carried by a **comparator**, an object whose `compare(a, b)` returns a negative number when `a` must come first, zero when the two are tied, and a positive number when `b` must come first. Only the sign matters. The arrays of primitives use the natural numeric order and need no comparator at all, which is why `Arrays.sort(int[])` has no overload that takes one. Objects, including boxed `Integer` values, accept a comparator, and that is how a descending order is written.

The one rule that matters on day one is to build the sign with a **overflow-safe compare**, which means calling `Integer.compare(a, b)` or `Long.compare(a, b)` and never subtracting. For `a = Integer.MIN_VALUE` and `b = Integer.MAX_VALUE`, the difference wraps around to 1, so the code claims the smallest int is larger than the largest.

<!-- names: total order, comparator, overflow-safe compare -->

A comparator can also be a decision that is not numeric at all. To glue numbers together into the largest possible number, you cannot compare 9 and 90 by value. You compare the two concatenations: `"990"` against `"909"`. That order is still a total order, and proving it is what makes the technique legal.

<!-- stage: variables -->
### The Pair, The Sign And The Result

Each comparison involves two elements, `a` and `b`, and returns a sign: negative keeps `a` ahead, positive puts `b` ahead, zero declares a tie. Nothing else about the call survives. The sorted output is the only state that matters, and what makes it correct is that every adjacent pair, read left to right, gets a non-positive sign. For a trace of the decisions we track an index `i`, the element being inserted, and the sorted prefix to its left, which grows by one element each step.

<!-- stage: trace -->
### Overflow And A Concatenation Order

The first trace compares three extreme integers, the way a buggy subtraction comparator would see them. Comparing the minimum with the maximum by subtraction produces a wrapped result of positive 1, so it would say the minimum belongs after the maximum. The safe compare returns a negative number, and the true order is minimum, zero, maximum. Watch the vars of each step: `bySubtraction` and `byCompare` disagree on the first pair, and agree on the others.

```trace
{"cells":["MIN","0","MAX"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"pair":"MIN,MAX","bySubtraction":1,"byCompare":-1},"note":"Compare MIN with MAX. Subtraction gives sign +1 and Integer.compare gives -1. They disagree: the difference wrapped around, so the subtraction comparator would put them in the wrong order."},{"at":{"i":1},"vars":{"pair":"MIN,0","bySubtraction":-1,"byCompare":-1},"note":"Compare MIN with 0. Subtraction gives sign -1 and Integer.compare gives -1. They agree, since this difference fits in 32 bits."},{"at":{"i":2},"vars":{"pair":"0,MAX","bySubtraction":-1,"byCompare":-1},"note":"Compare 0 with MAX. Subtraction gives sign -1 and Integer.compare gives -1. They agree, since this difference fits in 32 bits."}]}
```

The second trace sorts the digit strings 3, 30, 34, 5 and 9 so that their concatenation is as large as possible. It uses insertion, and each new element slides left past neighbors whose concatenation is smaller. The step to study is the one for 34: it must go ahead of 3, because 343 is larger than 334, even though 3 is the smaller number. The sorted prefix at the end reads 9, 5, 34, 3, 30, and gluing it together gives 9534330.

```trace
{"cells":["3","30","34","5","9"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"insert":"3","sortedPrefix":"3"},"note":"Insert 3. It is the first element, so the prefix is just itself. The prefix is now 3."},{"at":{"i":1},"vars":{"insert":"30","sortedPrefix":"3,30"},"note":"Insert 30. 330 = 330 is at least 303 = 303, so 30 stays behind 3. The prefix is now 3, 30."},{"at":{"i":2},"vars":{"insert":"34","sortedPrefix":"34,3,30"},"note":"Insert 34. 3430 = 3430 beats 3034 = 3034, so 34 moves ahead of 30; 343 = 343 beats 334 = 334, so 34 moves ahead of 3. The prefix is now 34, 3, 30."},{"at":{"i":3},"vars":{"insert":"5","sortedPrefix":"5,34,3,30"},"note":"Insert 5. 530 = 530 beats 305 = 305, so 5 moves ahead of 30; 53 = 53 beats 35 = 35, so 5 moves ahead of 3; 534 = 534 beats 345 = 345, so 5 moves ahead of 34. The prefix is now 5, 34, 3, 30."},{"at":{"i":4},"vars":{"insert":"9","sortedPrefix":"9,5,34,3,30"},"note":"Insert 9. 930 = 930 beats 309 = 309, so 9 moves ahead of 30; 93 = 93 beats 39 = 39, so 9 moves ahead of 3; 934 = 934 beats 349 = 349, so 9 moves ahead of 34; 95 = 95 beats 59 = 59, so 9 moves ahead of 5. The prefix is now 9, 5, 34, 3, 30."}]}
```

<!-- stage: code -->
### Safe Compare And Concatenation Order

```java
static int[] sortedCopy(int[] a) {
    int[] copy = a.clone();
    Arrays.sort(copy);
    return copy;
}

static Integer[] descending(int[] a) {
    Integer[] boxed = new Integer[a.length];
    for (int i = 0; i < a.length; i++) boxed[i] = a[i];
    Arrays.sort(boxed, (x, y) -> Integer.compare(y, x));
    return boxed;
}

static String largestNumber(int[] nums) {
    String[] parts = new String[nums.length];
    for (int i = 0; i < nums.length; i++) parts[i] = Integer.toString(nums[i]);
    Arrays.sort(parts, (x, y) -> (y + x).compareTo(x + y));
    if (parts.length > 0 && parts[0].equals("0")) return "0";
    return String.join("", parts);
}
```

The primitive sort takes O(n log n) time; the boxed variant adds O(n) extra memory for the wrapper objects. In `largestNumber` the comparison builds two strings of length up to twenty, so each comparison costs O(1) for the bounded sizes of this problem. The all-zero case is caught after sorting, since a leading `"0"` in the largest-first order means every piece was zero.

<!-- stage: applicability -->
### When The Order Is The Decision

Reach for an explicit ordering contract when a scan, a merge or a grouping step can only decide something locally once the data is in a known sequence, and the sequence is not simply ascending numbers. The invariant to state before coding is the sentence that finishes "x goes before y exactly when". If you cannot complete it for every pair, including equal pairs, the order is not ready.

A false friend is sorting primitive values and expecting to carry extra information along. Once `int[]` is sorted, the original positions are gone, and a tie between two equal ints is not distinguishable. If equal elements must keep a role, the elements have to become objects or indexes first. The no-go condition is a relation that is not transitive, such as "these two intervals overlap", which can hold for A and B and for B and C without holding for A and C. Sorting with such a relation can fail in the middle of the sort with an exception or, worse, complete with a wrong order.

In Java, the primitive overload `Arrays.sort(int[])` has no comparator argument, so descending order on `int[]` means sorting ascending and reading backwards, or boxing. Never compute a sign by subtraction, and never return a hard-coded 1 for "not less", since that breaks the contract when the two elements are equal.

<!-- stage: exercises -->
### Exercises

#### [Build] Sort an Array (LeetCode 912)
<!-- id: so-sort-an-array -->

**Prerequisites.** Chapter 01 array loops; the idea of a contract from Chapter 00.

**Problem.** Given an integer array, return a new array containing the same values in nondecreasing order. The caller's array must be left exactly as it was. State the order in a comment before writing any code.

**Constraints.** 1 <= nums.length <= 50000 and -50000 <= nums[i] <= 50000. Aim for O(n log n) time.

**Example 1.** Input `nums = [5, 2, 3, 1]`, output `[1, 2, 3, 5]`.

**Example 2.** Input `nums = [4, -1, 4, 0, -1]`, output `[-1, -1, 0, 4, 4]`, so duplicates stay in the result.

**Hint.** Which standard method sorts a primitive array in place, and what must happen first so the input is not mutated? What is the order of two equal values?

**Changed decision.** First rung: you commit to an explicit output order and to not mutating the argument.

#### [Vary] Sort Boxed Integers in Descending Order (Author exercise)
<!-- id: so-boxed-descending -->

**Prerequisites.** The sort-an-array exercise above.

**Problem.** Given an `Integer[]`, sort it so the largest value comes first, using a comparator you write yourself. Then explain, with a check in code, why the comparator form of `Arrays.sort` has no overload for `int[]`.

**Constraints.** 0 <= values.length <= 1000, and values may be any `int`, including both extremes. Use a safe compare, not subtraction.

**Example 1.** Input `values = [3, 9, 1, 9]`, output `[9, 9, 3, 1]`.

**Example 2.** Input `values = [-5, 0, 7]`, output `[7, 0, -5]`.

**Hint.** What does the comparator return when its arguments are swapped relative to the natural order? Which parameter types does each overload of `Arrays.sort` accept?

**Changed decision.** The order is reversed, so the sign of the comparison flips and the element type must be an object.

#### [Boundary] Extreme Comparator (Author exercise)
<!-- id: so-extreme-comparator -->

**Prerequisites.** The two exercises above.

**Problem.** Order the three values `Integer.MIN_VALUE`, `0` and `Integer.MAX_VALUE` in every starting arrangement, ascending, without subtraction. Then exhibit the exact pair for which a subtraction-based comparator gives the wrong sign.

**Constraints.** Exactly three distinct values, in any of the six permutations. The comparator must return the correct sign for every pair of ints.

**Example 1.** Input `[MAX, MIN, 0]`, output `[MIN, 0, MAX]`.

**Example 2.** Input `[0, MAX, MIN]`, output `[MIN, 0, MAX]`, and the pair (MIN, MAX) is the one subtraction gets wrong.

**Hint.** What is the value of `Integer.MIN_VALUE - Integer.MAX_VALUE` in 32-bit arithmetic? Which pairs of ints can overflow when subtracted?

**Changed decision.** The data is chosen to sit at the edge of the type, so the safe compare is the only correct version.

#### [Recognize] Largest Number (LeetCode 179)
<!-- id: so-largest-number -->

**Prerequisites.** All three exercises above.

**Problem.** Given a list of non-negative integers, arrange them so that the number formed by gluing their decimal digits together is as large as possible, and return it as a string. If the result would be a run of zeros, return a single `"0"`.

**Constraints.** 1 <= nums.length <= 100 and 0 <= nums[i] <= 1000000000. The result may exceed any numeric type.

**Example 1.** Input `nums = [8, 81, 80]`, output `"88180"`.

**Example 2.** Input `nums = [0, 0, 0]`, output `"0"`.

**Hint.** Compare two candidates by the two strings you get when each goes first. Why is numeric order the wrong question for 8 against 81?

**Changed decision.** The comparator is no longer numeric: it is the concatenation order, and the zero case needs its own guard.
