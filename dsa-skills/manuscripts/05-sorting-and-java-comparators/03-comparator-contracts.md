<!-- lesson-kind: standard -->
<!-- lesson-id: comparator-contracts -->
## Write A Valid Comparator

<!-- stage: context -->
### A Sort That Crashes On Large Files

A release tool lists file names from the shortest name to the longest. The comparator returns -1 when the first name is shorter and 1 in every other case. The tool works on test lists of ten names. On a production list of several thousand names, the sort sometimes stops with the message `Comparison method violates its general contract!`. The same code sorts other lists without any complaint.

The comparator gives a plausible answer for every pair, so the failure looks random. It is not random. This lesson answers one question. Which properties must a comparator have so that a sort gives one well-defined order for every input?

<!-- stage: naive -->
### Returning One Of Two Answers

The direct rule decides only whether the first name is shorter. It returns -1 for yes and 1 for no, so it never returns zero.

```java
static void sortByLength(String[] names) {
    Arrays.sort(names, (a, b) -> a.length() < b.length() ? -1 : 1);
}
```

On `["ccc", "a", "bb"]` the rule gives the order `["a", "bb", "ccc"]`. Every pair has different lengths, so every answer is clear. The rule seems to work whenever the test data has no two names of the same length.

<!-- stage: bottleneck -->
### Equal Names Each Claim To Go Second

```predict
The names `"ab"` and `"cd"` have the same length. What does the rule return for the pair in each order, and what does a sort conclude from the two answers?

The rule returns 1 for `compare("ab", "cd")` and 1 for `compare("cd", "ab")`. The first answer says that "cd" goes first, and the second says that "ab" goes first. The two answers contradict each other, so no order satisfies both.
```

A sort that makes O(n log n) comparisons relies on each answer being consistent with the others. When two names of equal length contradict each other, the sort can place them in either order, and chains of such pairs make the final array depend on the order of the input. The library may also detect the contradiction and throw `IllegalArgumentException`. Small lists rarely trigger the check, which explains the random failure. The rule needs a third answer for equal names, and it needs a check that its answers agree with one another.

<!-- stage: insight -->
### Make Every Answer Agree With The Others

A comparator is valid when its answers for all pairs describe one ranking. Three properties give that guarantee.

#### Mirror Answers For A Swapped Pair

A comparator is **antisymmetric** when `compare(a, b)` and `compare(b, a)` have opposite signs, and both are zero when the values tie. The naive rule fails here, because it returns 1 for both orders of an equal pair. Returning 0 for ties fixes this property.

#### Chains Of Answers Must Hold

A comparator is **transitive** when `a` before `b` and `b` before `c` always imply `a` before `c`. Ties must be transitive too. If `a` ties with `b`, then `a` and `b` must compare the same way against every third value `c`. Rules that compare by one fixed key are transitive automatically. Rules that mix keys, or that compare unrelated quantities, can break the chain.

#### Combine Keys In A Fixed Priority

Many orders use several keys, such as length first and then alphabetical order. The method `thenComparing` expresses this directly: the second key is consulted only when the first key returns zero. Each key on its own is a valid ranking, and the priority rule keeps the combination valid. The library builders `Comparator.comparingInt` and `Comparator.comparingLong` read a key from each object and compare the keys safely.

<!-- names: antisymmetric, transitive, thenComparing -->

#### When A Zero Is Allowed

A result of zero says that the pair is interchangeable for the ranking, and it does not say that the values are equal as objects. Return zero only when the problem accepts either order of the pair. If the problem needs one fixed order for such values, add another key that separates them.

<!-- stage: variables -->
### Two Values, A Key And A Result

The comparator uses a few named pieces with fixed meanings.

- **a** and **b** are the pair under comparison.
- **key** is the quantity that the comparator reads from a value, such as its length.
- **result** is negative, zero or positive, and it must change sign when `a` and `b` swap places.

The comparator holds no counters and no random numbers, so it returns the same result for the same pair every time.

<!-- stage: trace -->
### Checking Every Pair Under Two Rules

#### The Rule That Never Returns Zero

Take the names `["bb", "a", "cc"]` with lengths 2, 1 and 2. The check compares each pair in both orders. For the pair `"bb"` and `"cc"`, the naive rule returns 1 in both orders. Both answers say that the first name of the call goes second, which is a contradiction.

#### The Rule With A Tie Answer

The repaired rule uses `Integer.compare` on the lengths. For the same pair it returns 0 in both orders, which says that the two names are interchangeable by length. For the other pairs it returns -1 in one order and 1 in the other order, so the answers mirror each other.

#### Stepping Through Both Rules

```trace
{"cells":["bb","a","cc"],"pointers":["i","j"],"steps":[{"at":{"i":0,"j":1},"vars":{"first":"compare(\"bb\", \"a\") = 1","second":"compare(\"a\", \"bb\") = -1"},"note":"The answers 1 and -1 mirror each other, so the order is clear."},{"at":{"i":0,"j":2},"vars":{"first":"compare(\"bb\", \"cc\") = 1","second":"compare(\"cc\", \"bb\") = 1"},"note":"Both orders return 1. Each name claims to go second, which is a contradiction."},{"at":{"i":1,"j":2},"vars":{"first":"compare(\"a\", \"cc\") = -1","second":"compare(\"cc\", \"a\") = 1"},"note":"The answers -1 and 1 mirror each other, so the order is clear."},{"at":{"i":3,"j":-1},"vars":{},"note":"One pair contradicts itself, so the rule is not a valid comparator."}]}
```

```trace
{"cells":["bb","a","cc"],"pointers":["i","j"],"steps":[{"at":{"i":0,"j":1},"vars":{"first":"compare(\"bb\", \"a\") = 1","second":"compare(\"a\", \"bb\") = -1"},"note":"The answers 1 and -1 mirror each other, so the order is clear."},{"at":{"i":0,"j":2},"vars":{"first":"compare(\"bb\", \"cc\") = 0","second":"compare(\"cc\", \"bb\") = 0"},"note":"Both orders return 0. The two names are interchangeable by length."},{"at":{"i":1,"j":2},"vars":{"first":"compare(\"a\", \"cc\") = -1","second":"compare(\"cc\", \"a\") = 1"},"note":"The answers -1 and 1 mirror each other, so the order is clear."},{"at":{"i":3,"j":-1},"vars":{},"note":"Every pair mirrors or ties, so the rule is a valid comparator."}]}
```

<!-- stage: code -->
### Compare By Key Then By Tie Key

#### A Valid Rule For Names

```java
static void sortByLength(String[] names) {
    Arrays.sort(names, (a, b) -> Integer.compare(a.length(), b.length()));
}

static void sortByLengthThenAlphabet(String[] names) {
    Arrays.sort(names, Comparator.comparingInt(String::length)
            .thenComparing(Comparator.naturalOrder()));
}
```

#### What The Rules Cost

Each comparison reads two lengths or two strings, so it takes constant time for the length rule and time proportional to the shorter name for the alphabet rule. The sort makes O(n log n) comparisons. The comparator allocates no memory per call, so the space is that of the library sort.

<!-- stage: applicability -->
### When To Check The Contract

#### Check Every Rule You Write

Test any comparator that you write with three kinds of inputs: a pair that ties, a pair of extreme values, and a triple that checks the chain. The invariant is that all answers agree with one ranking. Run the pair in both orders, because a mirror failure appears only when the order of arguments flips.

#### Where Rules Look Valid And Are Not

A false friend is a rule that gives sensible answers for most pairs. A rule that returns 1 for every pair that is not smaller breaks the mirror property, as the naive rule did. A rule that compares by a key that differs between calls, such as a random number, breaks the chain. A rule that compares two different measures depending on a condition can break the chain as well. If the answers cannot be written as one key per value, check the chain of three values by hand.

#### Java Details That Cause Failures

The library may throw `IllegalArgumentException` for an invalid comparator, but it is not required to. A sort can therefore finish with a wrong order and raise no error. The result of `compare` has no fixed values, so test its sign and not equality with 1 or -1. A `compare` method that returns the difference of two `int` fields repeats the overflow failure from the first lesson of this chapter.

<!-- stage: exercises -->
### Exercises

#### [Build] Safe Integer Comparator (Author exercise)
<!-- id: so-distance-comparator -->

**Prerequisites.** The three properties of a valid comparator from this lesson.

**Problem.** Let `target` be an integer. Write a `Comparator<Integer>` that ranks an integer by its distance `|x - target|`. The comparator returns a negative number when the first value is closer, zero when the distances are equal, and a positive number otherwise.

**Constraints.** The limits are:
- **Values** and `target` are 32-bit integers.
- **Distance** is computed exactly and can reach `2^32 - 1`.
- **Result** is the sign that the contract requires, and its exact size does not matter.
- **Equal distances** return zero.

**Example 1.** Input `target = 10`, compare 7 with 15, output a negative number, because the distances are 3 and 5.

**Example 2.** Input `target = 0`, compare `-2147483648` with `2147483647`, output a positive number, because the distances are 2147483648 and 2147483647.

**Hint.** In which type must the difference be computed, and which compare method reads the two distances?

**Changed decision.** Basic case: the key is a computed distance, and the comparison reads keys and never subtracts them.

#### [Vary] Chained Keys (Author exercise)
<!-- id: so-chained-keys -->

**Prerequisites.** Safe Integer Comparator above.

**Problem.** Let `names` be an array of strings. Sort the array in place so that shorter strings come first. Order strings of equal length alphabetically by `compareTo`.

**Constraints.** The limits are:
- **Length** satisfies `0 <= names.length <= 10^4`.
- **Strings** are non-null and have lengths from 0 to 100.
- **Ties** are resolved by the second key, so no two different strings compare as equal.
- **Mutation** of the array in place is required.

**Example 1.** Input `names = ["bb", "a", "ab", "c"]`, output `["a", "c", "ab", "bb"]`.

**Example 2.** Input `names = ["", "b", ""]`, output `["", "", "b"]`.

**Hint.** When is the second key consulted, and which builder method chains it after the first key?

**Changed decision.** A second key joins the first, and the second key is consulted only on a tie.

#### [Boundary] Equal Keys And Extreme Values (Author exercise)
<!-- id: so-check-contract -->

**Prerequisites.** The two exercises above.

**Problem.** Let `sample` be an array of integers and let `c` be a `Comparator<Integer>`. Return true when `c` satisfies three rules for every `x`, `y` and `z` taken from `sample`. The first rule is that `sign(c(x, y))` equals `-sign(c(y, x))`. The second rule is that `c(x, y) <= 0` and `c(y, z) <= 0` imply `c(x, z) <= 0`. The third rule is that `c(x, y) == 0` implies `sign(c(x, z)) == sign(c(y, z))`. Return false otherwise.

**Constraints.** The limits are:
- **Length** satisfies `0 <= sample.length <= 40`; the empty sample returns true.
- **Values** are 32-bit integers and may repeat.
- **Triples** include repeated positions, so `x`, `y` and `z` can be the same element.
- **Comparator** is deterministic.

**Example 1.** Input `sample = [-2147483648, 0, 2147483647]` and `c = (a, b) -> a - b`, output false.

**Example 2.** Input `sample = [3, 3, 8]` and `c = Integer::compare`, output true.

**Hint.** Which rule fails for the pair of the smallest and the largest value under subtraction?

**Changed decision.** The method checks a comparator and does not sort, so the contract becomes the thing under test.

#### [Recognize] Largest Number (LeetCode 179)
<!-- id: so-order-for-largest -->

**Prerequisites.** All three exercises above.

**Problem.** Let `nums` hold non-negative integers. Return an `int[]` that holds the same values in an order whose decimal strings, written one after another, form the largest possible number. This version returns the order of the values, and it changes the contract of the original problem, which returns the number as a string. When two orders give the same number, either is accepted.

**Constraints.** The limits are:
- **Length** satisfies `0 <= nums.length <= 100`; the empty array returns an empty array.
- **Values** satisfy `0 <= nums[i] <= 10^9`.
- **Comparison** of two values uses their two concatenations and no numeric subtraction.
- **Answer** holds exactly the values of `nums`.

**Example 1.** Input `nums = [824, 8247]`, output `[824, 8247]`, because 8248247 is larger than 8247824.

**Example 2.** Input `nums = [0, 10, 2]`, output `[2, 10, 0]`.

**Hint.** Does the answer for two values depend on a third value, and what makes the comparison a valid ranking?

**Changed decision.** The comparator must be a valid ranking on its own, since the method returns the order and no later step repairs it.
