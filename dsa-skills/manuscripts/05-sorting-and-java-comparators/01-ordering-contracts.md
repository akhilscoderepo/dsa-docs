<!-- lesson-kind: standard -->
<!-- lesson-id: ordering-contracts -->
## Compare Two Values Safely

<!-- stage: context -->
### A Ranking That Puts A Debtor First

A bank report ranks accounts from the lowest balance to the highest. The sort works on every test file, so the team ships it. A month later one account with a balance of 2000000000 appears above an account with a balance of -2000000000, and the whole ranking is out of order. The sorting call is correct and the data is valid. Only the rule that decides which of two balances comes first is wrong.

Every sort asks the same small question many times: given two values, which one goes first? This lesson answers two questions about that rule. What may the answer look like, and which Java call gives the right answer for every pair of `int` values?

<!-- stage: naive -->
### Deciding Order By Subtraction

The direct rule says that `a` goes first when `a - b` is negative, and that `b` goes first when `a - b` is positive. The rule needs no extra call, and it works on small numbers.

```java
static void sortAscending(Integer[] balances) {
    Arrays.sort(balances, (a, b) -> a - b);
}
```

The lambda is a **comparator**, a function that takes two values and returns a number. A negative result means the first value goes first, zero means neither goes first, and a positive result means the second value goes first. On `[40, -7, 12]` the rule gives the sorted order `[-7, 12, 40]`.

<!-- stage: bottleneck -->
### The Subtraction Leaves The int Range

```predict
The call compares a = 2000000000 with b = -2000000000. What sign does `a - b` have in Java, and which value does the sort place first?

The true difference is 4000000000, but an `int` holds at most 2147483647. The result wraps around to -294967296, which is negative, so the sort places 2000000000 first. The order is wrong for this pair.
```

A sort that uses comparisons makes O(n log n) of them, and one wrong answer can move a value to the wrong side of the array. The subtraction `a - b` is exact only when the true difference fits in 32 bits. For values near `Integer.MIN_VALUE` and `Integer.MAX_VALUE`, the difference wraps and the sign flips. The sort needs only the sign of the comparison, so the rule can ask for the sign without computing a difference at all.

<!-- stage: insight -->
### Return The Sign From A Comparison

The rule must return a correct sign for every pair, and no arithmetic on the values can promise that. A direct comparison of the two values can.

#### What A Comparison Result Means

The static method `Integer.compare(a, b)` returns a negative number when `a < b`, zero when `a == b`, and a positive number when `a > b`. It uses comparison operators and never subtracts, so it cannot overflow. `Long.compare` does the same for `long` values. Only the sign carries meaning, so code must not test for the exact values -1 and 1.

#### The Contract Behind The Sign

A **total order** is a rule that ranks every pair of values and never contradicts itself. Three properties define it. If `a` goes before `b`, then `b` never goes before `a`. If `a` goes before `b` and `b` goes before `c`, then `a` goes before `c`. Two values that tie are interchangeable for the ranking. A comparison function with these properties is the **compare contract**, and a sort gives a correct result only when the function obeys it.

<!-- names: Integer.compare, total order, compare contract -->

#### How A Sort Uses The Contract

A comparison sort never inspects the values themselves. It calls the comparison, reads the sign, and moves values. After the sort, every adjacent pair has a non-positive comparison result. That fact is the invariant that makes later scans valid. A comparison that breaks the contract breaks the invariant, and no later step can repair it.

<!-- stage: variables -->
### Two Values And One Sign

The comparison involves only three pieces, and each has a fixed meaning.

- **a** is the first value passed to the comparator.
- **b** is the second value passed to the comparator.
- **sign** is the number the comparator returns, and only its sign matters: negative puts `a` first, positive puts `b` first, zero means a tie.

The comparator keeps no state between calls, so the same pair always gives the same sign.

<!-- stage: trace -->
### One Sort Under Two Rules

#### The Subtraction Rule On Three Balances

Take `[2000000000, 5, -2000000000]` and sort it by insertion, which compares each new value with the values on its left. The subtraction rule compares 5 with 2000000000 and correctly moves 5 left. It then compares -2000000000 with 2000000000 and gets a wrapped positive result, so it believes that -2000000000 is already in the right place. The sort stops with the array `[5, 2000000000, -2000000000]`, which is not sorted.

#### The Safe Rule On The Same Balances

The safe rule runs the same insertion. It compares -2000000000 with 2000000000 using `Integer.compare`, and the result is negative. The value moves left past 2000000000 and then past 5. The sort ends with `[-2000000000, 5, 2000000000]`.

#### Stepping Through Both Rules

```trace
{"cells":[2000000000,5,-2000000000],"pointers":["i","j"],"steps":[{"at":{"i":0,"j":-1},"vars":{"array":"[2000000000, 5, -2000000000]"},"note":"Start: the value at index 0 is a sorted prefix of length 1."},{"at":{"i":1,"j":0},"vars":{"compare":"5 vs 2000000000","sign":"negative","array":"[2000000000, 5, -2000000000]"},"note":"The sign is negative, so 5 goes before 2000000000. Swap them."},{"at":{"i":2,"j":1},"vars":{"compare":"-2000000000 vs 2000000000","sign":"positive","array":"[5, 2000000000, -2000000000]"},"note":"The sign is positive, so -2000000000 stays after 2000000000. Stop this insertion."},{"at":{"i":3,"j":-1},"vars":{"array":"[5, 2000000000, -2000000000]"},"note":"The sort ends with the array [5, 2000000000, -2000000000], which is not sorted."}]}
```

```trace
{"cells":[2000000000,5,-2000000000],"pointers":["i","j"],"steps":[{"at":{"i":0,"j":-1},"vars":{"array":"[2000000000, 5, -2000000000]"},"note":"Start: the value at index 0 is a sorted prefix of length 1."},{"at":{"i":1,"j":0},"vars":{"compare":"5 vs 2000000000","sign":"negative","array":"[2000000000, 5, -2000000000]"},"note":"The sign is negative, so 5 goes before 2000000000. Swap them."},{"at":{"i":2,"j":1},"vars":{"compare":"-2000000000 vs 2000000000","sign":"negative","array":"[5, 2000000000, -2000000000]"},"note":"The sign is negative, so -2000000000 goes before 2000000000. Swap them."},{"at":{"i":2,"j":0},"vars":{"compare":"-2000000000 vs 5","sign":"negative","array":"[5, -2000000000, 2000000000]"},"note":"The sign is negative, so -2000000000 goes before 5. Swap them."},{"at":{"i":3,"j":-1},"vars":{"array":"[-2000000000, 5, 2000000000]"},"note":"The sort ends with the array [-2000000000, 5, 2000000000], which is sorted."}]}
```

<!-- stage: code -->
### Two Calls To Fix The Rule

#### Ascending And Descending Order

```java
static void sortAscending(Integer[] balances) {
    Arrays.sort(balances, (a, b) -> Integer.compare(a, b));
}

static void sortDescending(Integer[] balances) {
    Arrays.sort(balances, (a, b) -> Integer.compare(b, a));
}
```

The descending rule swaps the arguments, which reverses the sign without negating it. Negating the result would fail for the one value `Integer.MIN_VALUE`, because `-Integer.MIN_VALUE` equals itself.

#### What The Calls Cost

The sort makes O(n log n) comparisons, and each comparison takes constant time. The comparator allocates nothing, so the extra space is the working space of the sort itself.

<!-- stage: applicability -->
### When A Comparison Rule Is Enough

#### Look For A Question About Order

Use an explicit comparison whenever the problem asks for a deterministic order before any scan can decide locally. The invariant is the contract above: the rule ranks every pair, never contradicts itself, and treats ties as interchangeable. Checking the contract on the extreme values and on equal values catches most faulty rules.

#### Where A Rule Looks Right And Is Not

A false friend here is a rule that passes ordinary tests and still breaks the contract. Subtraction is the common one. Another is a rule that returns -1 for every unequal pair and never compares in the other direction, which breaks the first property. A rule that reads a value that can change during the sort also fails, because the same pair then gets different signs.

#### Java Details That Cause Failures

A comparator works only on object types, so `Arrays.sort(int[], comparator)` does not exist, and the sort needs an `Integer[]`. A boxed array costs more memory than an `int[]`. When a problem needs only the natural ascending order of primitives, skip the comparator and call `Arrays.sort(int[])`, which the next lesson covers.

<!-- stage: exercises -->
### Exercises

#### [Build] Sort An Array (LeetCode 912)
<!-- id: so-sort-array -->

**Prerequisites.** The compare contract and `Integer.compare` from this lesson.

**Problem.** Let `nums` be an array of integers. Return a new array that holds the values of `nums` in nondecreasing order. The input array keeps its original contents.

**Constraints.** The limits are:
- **Length** satisfies `0 <= nums.length <= 5 * 10^4`; the empty array is legal.
- **Values** are 32-bit integers, including `Integer.MIN_VALUE` and `Integer.MAX_VALUE`.
- **Mutation** of `nums` is not allowed.
- **Answer** is an `int[]` of the same length.

**Example 1.** Input `nums = [5, -3, 9, -3, 0]`, output `[-3, -3, 0, 5, 9]`.

**Example 2.** Input `nums = [2147483647, -2147483648, 0]`, output `[-2147483648, 0, 2147483647]`.

**Hint.** When the method merges two sorted halves, which call decides whether the left or the right value moves first?

**Changed decision.** The method writes its own sort, so the comparison decision is visible in the code.

#### [Vary] Sort Boxed Integers In Descending Order (Author exercise)
<!-- id: so-descending-boxed -->

**Prerequisites.** Sort An Array above.

**Problem.** Let `values` be an `Integer[]`. Sort `values` in place so that the largest value comes first and equal values stay adjacent. Use a comparator, and do not negate or subtract.

**Constraints.** The limits are:
- **Length** satisfies `0 <= values.length <= 10^4`.
- **Elements** are non-null `Integer` objects in the full 32-bit range.
- **Mutation** of `values` in place is required.
- **Answer** is the same array, sorted.

**Example 1.** Input `values = [3, 9, 1, 9]`, output `[9, 9, 3, 1]`.

**Example 2.** Input `values = [-2147483648, 2147483647]`, output `[2147483647, -2147483648]`.

**Hint.** Which argument order of `Integer.compare` reverses the ranking, and which `Arrays.sort` overload takes a comparator?

**Changed decision.** The ranking reverses, and the element type changes from `int` to `Integer` so that a comparator is allowed.

#### [Boundary] Extreme Comparator (Author exercise)
<!-- id: so-extreme-comparator -->

**Prerequisites.** The two exercises above.

**Problem.** Let `a` and `b` be `int` values. Return the sign of `a` compared with `b` as exactly -1, 0 or 1. The result must agree with the mathematical order for every pair, including pairs of `Integer.MIN_VALUE` and `Integer.MAX_VALUE`.

**Constraints.** The limits are:
- **Inputs** are any two 32-bit integers.
- **Result** is -1, 0 or 1 and no other number.
- **Arithmetic** on `a` and `b` is not allowed.
- **Pairs** include equal values and values of opposite sign.

**Example 1.** Input `a = -2147483648`, `b = 2147483647`, output -1.

**Example 2.** Input `a = 2147483647`, `b = 2147483647`, output 0.

**Hint.** Which comparison operators answer the question without producing a number that can wrap?

**Changed decision.** The method must normalize the sign, because the library result is negative, zero or positive and not -1, 0 or 1.

#### [Recognize] Largest Number (LeetCode 179)
<!-- id: so-largest-number -->

**Prerequisites.** All three exercises above.

**Problem.** Let `nums` be an array of non-negative integers. Arrange the values so that, written one after another as decimal strings, they form the largest possible number. Return that number as a string.

**Constraints.** The limits are:
- **Length** satisfies `1 <= nums.length <= 100`.
- **Values** satisfy `0 <= nums[i] <= 10^9`.
- **Leading zeros** do not appear in the answer, so an array of zeros returns `"0"`.
- **Answer** is a string and can exceed the `long` range.

**Example 1.** Input `nums = [3, 30, 34, 5, 9]`, output `"9534330"`.

**Example 2.** Input `nums = [0, 0]`, output `"0"`.

**Hint.** For two values `x` and `y`, which of the strings `x + y` and `y + x` is larger, and does that answer depend on any third value?

**Changed decision.** The order is not numeric order. The comparison compares two concatenations of the same pair.
