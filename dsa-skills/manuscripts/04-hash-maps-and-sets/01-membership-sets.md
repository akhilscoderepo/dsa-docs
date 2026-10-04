<!-- lesson-kind: standard -->
<!-- lesson-id: membership-sets -->
## Check Membership With A Set

<!-- stage: context -->
### Duplicate Order Numbers In An Import

A warehouse system imports a file of up to 100000 order numbers. Two rows with the same number would ship one order twice, so the import must reject the file when any number repeats. The first version of the check passes on a small test file. On the real file it runs for minutes, although the code is correct.

The check gives the right answer and still wastes time. The question is which question the program asks again and again while it reads the file, and what it must remember so that it asks each question once.

<!-- stage: naive -->
### Comparing Every Pair Of Numbers

The direct method compares each number with every number that comes after it. If any pair is equal, the file has a duplicate.

```java
static boolean containsDuplicate(int[] nums) {
    for (int i = 0; i < nums.length; i++) {
        for (int j = i + 1; j < nums.length; j++) {
            if (nums[i] == nums[j]) {
                return true;
            }
        }
    }
    return false;
}
```

On `[4, 7, 1, 7, 9]` the method returns true when `i = 1` and `j = 3`. On `[3, 1, 4, 2]` it checks all six pairs and returns false.

<!-- stage: bottleneck -->
### The Same Question Repeats For Every Number

```predict
The file holds 100000 distinct order numbers, so no pair is equal. Roughly how many comparisons does the double loop make, and what question does each comparison answer?

The loop makes about n * (n - 1) / 2 comparisons, which is about 5 billion and O(n^2). Each comparison asks whether one earlier number equals the current number. The loop asks that question again for every later number, scanning all earlier numbers each time.
```

When the file has no duplicate, the method never stops early. For each position `j`, it looks back over every earlier number to answer one question: did this value appear before? The answer to that question does not depend on the order of the earlier numbers. It depends only on which values occurred. A program that keeps the values it has already read can answer the question without scanning them, so the total work can drop from O(n^2) to O(n).

<!-- stage: insight -->
### Keep Read Values In A Hash Set

The program needs a container that stores values and answers "is this value stored?" quickly. The answer to that question is the whole state that later numbers need.

#### Store Only What The Question Needs

A **hash set** stores distinct values. Adding a value takes expected constant time, and so does asking whether a value is stored. Expected constant time means O(1) on average over typical input. Java provides it as `HashSet`. The set keeps no count and no position for a value, because this question never asks for either.

<!-- names: hash set, membership test, seen set -->

#### Test Before Adding

A **membership test** asks whether a value is already in the set. In Java, `contains(x)` runs the test, and `add(x)` stores `x` and returns `false` when `x` was already there. The loop reads `nums[i]`, runs the test, and either returns true or stores the value. The set that holds the values read so far is the **seen set**.

#### The Invariant That Keeps The Loop Correct

After the iteration for index `i`, the seen set holds exactly the distinct values of `nums[0..i]`, and no two of those values are equal. If the loop reaches index `i + 1` with a value that the seen set already holds, two positions share one value, so the loop returns true. If the loop ends, every position was new, so the answer is false.

#### What The Set Costs

Each of the n iterations does one expected O(1) operation, so the time is O(n) on average. The seen set can hold all n values when no duplicate exists, so the space is O(n). The method spends memory to remove the repeated scans.

<!-- stage: variables -->
### Set, Index And Value

The loop needs two pieces of state, and the list says when each one changes.

- **seen** holds the distinct values read so far and gains one value per iteration that does not return.
- **i** names the position being read and moves right by one each iteration.

The value `nums[i]` is the one the test checks before the loop stores it.

<!-- stage: trace -->
### Reading Two Files Of Numbers

#### A File That Repeats A Number

Take `nums = [4, 7, 1, 7, 9]`. At `i = 0` the set is empty, so the loop stores 4. At `i = 1` it stores 7, and at `i = 2` it stores 1. At `i = 3` the value 7 is already in the set, so the test succeeds and the method returns true without reading 9.

#### A File With Distinct Numbers

Now take `nums = [3, 1, 4, 2]`. Every test fails, so the loop stores 3, 1, 4 and 2 in turn. The loop ends with four values in the set and returns false. This case shows that a false answer needs the full pass, while a true answer can stop at the first repeat.

#### Stepping Through Both Files

```trace
{"cells":[4,7,1,7,9],"pointers":["i"],"steps":[{"at":{"i":-1},"vars":{"seen":"{}"},"note":"Start: the seen set is empty."},{"at":{"i":0},"vars":{"value":4,"seen":"{4}"},"note":"Value 4 is not in the seen set. Store it."},{"at":{"i":1},"vars":{"value":7,"seen":"{4, 7}"},"note":"Value 7 is not in the seen set. Store it."},{"at":{"i":2},"vars":{"value":1,"seen":"{4, 7, 1}"},"note":"Value 1 is not in the seen set. Store it."},{"at":{"i":3},"vars":{"value":7,"seen":"{4, 7, 1}"},"note":"Value 7 is already in the seen set, so the method returns true."}]}
```

```trace
{"cells":[3,1,4,2],"pointers":["i"],"steps":[{"at":{"i":-1},"vars":{"seen":"{}"},"note":"Start: the seen set is empty."},{"at":{"i":0},"vars":{"value":3,"seen":"{3}"},"note":"Value 3 is not in the seen set. Store it."},{"at":{"i":1},"vars":{"value":1,"seen":"{3, 1}"},"note":"Value 1 is not in the seen set. Store it."},{"at":{"i":2},"vars":{"value":4,"seen":"{3, 1, 4}"},"note":"Value 4 is not in the seen set. Store it."},{"at":{"i":3},"vars":{"value":2,"seen":"{3, 1, 4, 2}"},"note":"Value 2 is not in the seen set. Store it."},{"at":{"i":4},"vars":{"seen":"{3, 1, 4, 2}"},"note":"The loop ends with no repeat, so the method returns false."}]}
```

<!-- stage: code -->
### A Set And One Pass

#### Finding A Repeated Number

```java
static boolean containsDuplicate(int[] nums) {
    Set<Integer> seen = new HashSet<>();
    for (int i = 0; i < nums.length; i++) {
        if (!seen.add(nums[i])) {
            return true;
        }
    }
    return false;
}
```

#### What The Method Costs

The loop runs n times and each `add` takes expected constant time, so the time is O(n) on average. The set holds up to n values, so the space is O(n). The call `seen.add(nums[i])` both tests and stores, so the loop never searches the set twice for one value.

<!-- stage: applicability -->
### When A Set Answers The Question

#### Look For Appeared Or Forbidden

Use a set when the question asks whether a value has appeared, exists in another collection, or is forbidden. The question must ignore how often the value occurred and where it occurred. The invariant is that the set holds exactly the relevant values processed so far. Common cases include rejecting duplicate identifiers, finding the values two arrays share, and stopping a process that revisits a state.

#### A Map Is A False Friend

A false friend here is a task that needs more than existence. If the answer depends on how many times a value occurred, the set discards the count and gives wrong answers. A map from value to count is needed instead. If the answer needs the position of an earlier value, the set has no position to return. The next two lessons teach those cases. A set stays correct whenever the question asks only whether a value is present.

#### Java Details That Cause Failures

A `Set<Integer>` stores `Integer` objects, and the `==` operator compares object references for them. Use `equals`, or let the set compare the values, as `contains` does. A `HashSet` keeps no insertion order. When the output must follow the order of first appearance, `LinkedHashSet` keeps that order, or the program can collect results in a list while the set only answers the test.

<!-- stage: exercises -->
### Exercises

#### [Build] Contains Duplicate (LeetCode 217)
<!-- id: hm-contains-duplicate -->

**Prerequisites.** The seen set and the test before adding from this lesson.

**Problem.** Let `nums` be an array of integers. Return true when some value occurs at least twice in `nums`. Return false when every value is distinct.

**Constraints.** The limits are:
- **Length** satisfies `0 <= nums.length <= 10^5`; the empty array is legal.
- **Values** are 32-bit integers, and negative values and zero are legal.
- **Mutation** of `nums` is not allowed.
- **Answer** is a boolean.

**Example 1.** Input `nums = [8, 3, 5, 3]`, output true.

**Example 2.** Input `nums = [-2, 0, 2]`, output false.

**Hint.** After each value, which one fact must the program remember about it?

**Changed decision.** Basic case: one set and one pass replace the pair of loops.

#### [Vary] Intersection Of Two Arrays (LeetCode 349)
<!-- id: hm-intersection -->

**Prerequisites.** Contains Duplicate above.

**Problem.** Let `a` and `b` be integer arrays. Return an `int[]` that holds every value present in both arrays exactly once. List the values in the order of their first occurrence in `a`.

**Constraints.** The limits are:
- **Length** satisfies `0 <= a.length, b.length <= 10^4`.
- **Values** are 32-bit integers.
- **Duplicates** may occur inside either array.
- **Answer** may be empty and holds no repeated value.

**Example 1.** Input `a = [9, 4, 9, 8, 4]`, `b = [4, 9, 5]`, output `[9, 4]`.

**Example 2.** Input `a = []`, `b = [1]`, output `[]`.

**Hint.** Which array should go into a set, and which structure prevents a shared value from appearing twice in the answer?

**Changed decision.** Two collections take part, and the answer must report each shared value once.

#### [Boundary] Happy Number (LeetCode 202)
<!-- id: hm-happy-number -->

**Prerequisites.** The two exercises above.

**Problem.** Let `n` be a positive integer. Replace `n` by the sum of the squares of its decimal digits, and repeat. Return true when the repeated replacement reaches 1. Return false when it reaches a value that occurred earlier.

**Constraints.** The limits are:
- **Input** satisfies `1 <= n <= 2^31 - 1`.
- **Digit sum** of squares fits in `int` for every input in range.
- **Termination** relies on detecting a repeated value, not on a step limit.
- **Answer** is a boolean.

**Example 1.** Input `n = 19`, output true, because the values are 19, 82, 68, 100 and then 1.

**Example 2.** Input `n = 2`, output false, because the values `4, 16, 37, 58, 89, 145, 42, 20, 4` repeat the value 4.

**Hint.** What does the program need to remember about each value it has produced, and what ends the loop if the value 1 never appears?

**Changed decision.** The items stored in the set are states of a process, not elements of an array.

#### [Recognize] Longest Consecutive Sequence (LeetCode 128)
<!-- id: hm-longest-consecutive -->

**Prerequisites.** All three exercises above.

**Problem.** Let `nums` be an unsorted integer array. A run is a set of values `x, x + 1, ..., x + k - 1`, each present in `nums`. Return the length of the longest run.

**Constraints.** The limits are:
- **Length** satisfies `0 <= nums.length <= 10^5`.
- **Values** are 32-bit integers, and duplicates may occur.
- **Answer** is 0 for the empty array.
- **Time** target is O(n) on average, so sorting is not the intended method.

**Example 1.** Input `nums = [100, 4, 200, 1, 3, 2]`, output 4, for the run `1, 2, 3, 4`.

**Example 2.** Input `nums = [7, 7, 7]`, output 1.

**Hint.** If the set holds every value, which values can the program recognize as the first value of a run by one membership test?

**Changed decision.** Membership tests on neighbors `x - 1` and `x + 1` replace sorting.
