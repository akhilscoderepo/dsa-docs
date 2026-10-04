<!-- lesson-kind: standard -->
<!-- lesson-id: mutation-contracts -->
## Whether A Method May Modify Its Input

<!-- stage: context -->
### Why A Shared Array Gets Corrupted

A reporting tool keeps the day's sensor readings in one array and passes it to two functions. The first function removes the readings flagged as faulty. The second prints the full day's readings in a daily report. After the first function runs, the report shows duplicates and missing values. Nobody has changed the report code in months.

Neither function is buggy in isolation. The first one rewrote the shared array to save memory. The second one assumed the array was unchanged. The interface never stated whether the input could change. Every problem statement and every method signature answers that question, stated or not. This lesson teaches you to state the answer explicitly.

<!-- stage: naive -->
### In-Place Removal By Overwriting

The tempting implementation reuses the input, because that costs no extra memory and looks efficient. The method below removes every occurrence of a value by overwriting from the front.

```java
static int removeValue(int[] nums, int target) {
    int write = 0;
    for (int read = 0; read < nums.length; read++) {
        if (nums[read] != target) {
            nums[write] = nums[read];
            write++;
        }
    }
    return write;
}
```

Called on `[3, 2, 2, 3]` with target 3, it returns 2, and the array afterward reads `[2, 2, 2, 3]`. A caller who prints `nums.length` elements sees three twos and a three. A caller who kept a second reference to the same array sees the damage too.

<!-- stage: bottleneck -->
### The Cost Of Changing Input Silently

```predict
After the overwriting method returns on `[3, 2, 2, 3]` with target 3, what does a caller who still holds the array see, and is the time cost the problem?

The caller sees `[2, 2, 2, 3]`, so the original data is gone even though the method ran in O(n) time. The cost is a silent change to the caller's data, not speed.
```

The method runs in O(n) time with O(1) extra space, so no step is slow. The cost is that the method silently changes the caller's data. The array does not become shorter, because a Java array's length is fixed when it is created. Only the first `write` slots are meaningful now. The slots after that still hold old values that look real.

The safe alternative copies the input first. That copy costs O(n) extra space and O(n) extra time. This is cheap for one call and expensive for a million calls. Neither choice is free, and the right one depends on a requirement that the code alone cannot reveal. When the statement says the input must be preserved, in-place rewriting is wrong however fast it is. When the statement asks for constant extra space, copying is wrong however clean it is.

<!-- stage: insight -->
### Separating The Array From The Result

#### Defining The Array And Its Meaningful Prefix

Two different things are easy to confuse. The array is a physical block of memory with a fixed length. The **meaningful prefix** is the part of that array that holds the answer. After an in-place filter, the meaningful prefix is the first `k` slots and nothing else. The return value gives `k`.

#### Stating What The Caller Can Rely On

A precondition states what the input must satisfy and whether the method may modify it. A **postcondition** states what the caller may rely on after the call, including which positions hold the result. Together they also state what extra storage the method may use. Write them in one line. For example: "precondition: input may be overwritten; postcondition: positions `0..k-1` hold the result in original order and the rest is unspecified". The words "in place" abbreviate such a specification. They never mean the array got shorter.

<!-- names: postcondition, meaningful prefix, auxiliary space -->

#### Counting Extra Memory And Safe Writes

The **auxiliary space** of a solution is its working memory beyond the input and beyond the required output. A returned array of `n` values therefore uses O(n) space that is not auxiliary. State which convention you use, so the argument stays about the algorithm and not about definitions.

A write is safe when it destroys no value that a later read still needs. That is the invariant of the filter, and the filter keeps it because the `write` index never passes the `read` index, and a slot is overwritten only after its original value has been read.

<!-- stage: variables -->
### Variables The Filter Uses

Four entities need names. When a method may modify its input, the specification must name `k` and state what the suffix holds.

- **Reference** is the variable that points at the array, and two variables can point at the same array.
- **Container** is the array object with its fixed length.
- **k** is the count of meaningful slots, which equals `write` at the end of the filter.
- **Suffix** is `nums[k..]`, which is normally "unspecified", and the caller must never read it.

<!-- stage: trace -->
### Tracing The Filter On Four Readings

#### Stepping Through The Loop

Run the filter on `[3, 2, 2, 3]` with target 3.

At `read = 0` the array holds a 3, so the loop skips it and writes nothing. At `read = 1` the array holds a 2, so the loop copies it to slot 0 and the array becomes `[2, 2, 2, 3]`.

At `read = 2` the array holds a 2, so the loop copies it to slot 1. The array looks unchanged because slot 1 already held a 2. At `read = 3` the array holds a 3, so the loop skips it.

#### Reading The Final State

When the loop ends, the state has these facts.

The value of `write` is 2, so the meaningful prefix is `[2, 2]`, the first two slots. The last two slots still hold `2` and `3`, and the 3 in slot 3 is a leftover from the input, not part of the answer.

The overwrite at slot 0 destroyed the first 3, which was safe because the loop had already read and rejected it. As a result, other references to this array now see `[2, 2, 2, 3]` and have lost the original.

```trace
{"cells":[3,2,2,3],"pointers":["read","write"],"steps":[{"at":{"read":0,"write":0},"vars":{"array":"[3,2,2,3]","k":0},"note":"Read slot 0, a 3: skip it. Nothing is written and write stays at 0."},{"at":{"read":1,"write":1},"vars":{"array":"[2,2,2,3]","k":1},"note":"Read slot 1, a 2: keep it and write it to slot 0. The array reads [2, 2, 2, 3]."},{"at":{"read":2,"write":2},"vars":{"array":"[2,2,2,3]","k":2},"note":"Read slot 2, a 2: keep it and write it to slot 1. The array reads [2, 2, 2, 3]."},{"at":{"read":3,"write":2},"vars":{"array":"[2,2,2,3]","k":2},"note":"Read slot 3, a 3: skip it. Nothing is written and write stays at 2."},{"at":{"read":4,"write":2},"vars":{"array":"[2,2,2,3]","k":2},"note":"Done. k = 2, so only the first 2 slots are the answer. The 3 left in the last slot is stale."}]}
```

<!-- stage: code -->
### Implementing In-Place And Copying Variants

```java
// Contract A: input may be overwritten. Meaningful result is nums[0..k-1], suffix unspecified.
static int removeValueInPlace(int[] nums, int target) {
    int write = 0;
    for (int read = 0; read < nums.length; read++) {
        if (nums[read] != target) nums[write++] = nums[read];   // write <= read, so unread data is never clobbered
    }
    return write;
}

// Contract B: input must be preserved. Return a fresh array of exactly the kept values.
static int[] removeValueCopy(int[] nums, int target) {
    int kept = 0;
    for (int v : nums) if (v != target) kept++;
    int[] result = new int[kept];
    int at = 0;
    for (int v : nums) if (v != target) result[at++] = v;
    return result;
}
```

The method `removeValueInPlace` is the same loop as `removeValue` shown first in this lesson. The two variants differ in cost and in the data they keep.

- **removeValueInPlace** takes O(n) time and O(1) auxiliary space, and it gives up the original data.
- **removeValueCopy** takes O(n) time, because it makes two passes so the result has the exact length.
- **removeValueCopy** uses O(n) space for the answer it must return.

Each variant fits only its own specification. Picking the wrong variant for the stated specification is a correctness error, not a style choice.

<!-- stage: applicability -->
### Checking The Specification Before Coding

#### Applying The Invariant

Check the precondition and the postcondition on the input array before you write any array or string solution.

Every write must preserve the data that a later read still needs. That condition is the invariant of the filter. The caller then reads only the stated meaningful prefix. When the statement has no rule about changing the input, you ask or you state your assumption. The default is to leave the input intact when the copy cost is small.

#### Finding Cases That Break The Precondition

An in-place method can look as if it follows the specification and still break its precondition about who may overwrite the input. Such a method is a false friend. Two cases qualify.

The phrase "in place" does not mean the array shrank, because a Java array never changes length. A loop to `nums.length` after an in-place removal reads stale slots, so the method returns a count instead. A returned reference to the same array does not prove the data is unchanged, because the caller's other references see every write.

#### Passing Arrays To Java Methods

Java passes an `int[]` parameter as a reference value.

A `String` is immutable, so a method that appears to modify one builds a new one. Assignment to the parameter variable does not affect the caller. Writes through the parameter do affect the caller.

Chapter 01 applies these specifications to every in-place exercise.

<!-- stage: exercises -->
### Exercises

#### [Build] Meaningful Prefix (Author exercise)
<!-- id: pc-meaningful-prefix -->

**Prerequisites.** The filter method in this lesson.

**Problem.** A method `removeValue(int[] nums, int target)` overwrites `nums` so that the elements not equal to `target` occupy the first positions in their original order. It returns `k`, the count of those elements. The meaningful prefix is the run of positions `0` through `k - 1`. Take `nums = [3,2,2,3]` and `target = 3`, so the method returns `k = 2`. State which values the method guarantees in `nums[0..k-1]`. State what the method specifies about `nums[k..]`. State what the caller must never do with the positions from `k` onward.

**Constraints.** The limits are:
- **Length** is fixed, so `nums.length` does not change after the call.
- **Return value** is an `int` in the range `0` to `nums.length`.
- **Mutation** is allowed; the method may overwrite any position of the input.
- **Empty input** is allowed, and then `k = 0`.
- **All equal to `target`** gives `k = 0` and no position holds a guaranteed value.
- **Suffix** values in `nums[k..]` are unspecified, and the caller must not read them as results.

**Example 1.** Input `nums = [3,2,2,3]` and target 3, output `k = 2` and a meaningful prefix of `[2,2]`.

**Example 2.** Input `nums = [3,3]` and target 3, output `k = 0`, so there is no meaningful prefix at all and the whole array is unspecified.

**Hint.** The return value is the only thing that says how much of the array counts as the answer. What does the array's own `length` tell you after the call?

**Changed decision.** First exercise in the sequence: separates the physical array from the meaningful prefix and names the boundary `k`.

#### [Vary] Preserve Input (Author exercise)
<!-- id: pc-preserve-input -->

**Prerequisites.** The meaningful-prefix exercise above.

**Problem.** Given an array `nums` and an integer `target`, produce the elements of `nums` that are not equal to `target`, in their original order. Two designs exist. The in-place design overwrites `nums`. The copying design allocates a new array `result` and leaves `nums` unchanged. A no-mutation specification states that after the call every position of `nums` holds the same value as before the call. Under a no-mutation specification, choose a design and return `result`. Explain why a method that returns the correct values but modifies `nums` still violates the specification.

**Constraints.** The limits are:
- **Length** is `1 <= nums.length <= 10^5`.
- **Values** of elements and `target` are `int`.
- **Result** has exactly as many elements as `nums` has values different from `target`, and may have length 0.
- **Caller** may keep using the original array after the call.
- **No-mutation specification** allows no write to `nums`.
- **Permissive specification** accepts either design.

**Example 1.** Input `nums = [4,1,4,2]` and target 4 under a no-mutation contract, output `[1,2]` with `nums` still equal to `[4,1,4,2]`.

**Example 2.** Input the same call under a permissive contract, output that either design is valid, and the in-place one saves O(n) memory.

**Hint.** Who else may hold a reference to the array? Which part of the interface does a hidden write break even when the returned numbers are right?

**Changed decision.** The specification changes from permissive to restrictive, which changes the correct design from overwriting to allocating.

#### [Boundary] Aliased Input (Author exercise)
<!-- id: pc-aliased-input -->

**Prerequisites.** The two exercises above.

**Problem.** In Java, an array variable holds a reference, which is the address of an array object. Two variables are aliases when they hold the same reference. Let `a` and `b` be two `int[]` variables that are aliases. A method receives `a` and assigns new values to its elements. Explain why a reader of `b` sees the new values. Then state the step a caller must take before the call so that `b` keeps the old contents.

**Constraints.** The limits are:
- **Aliases** `a` and `b` refer to one array object, so exactly one array exists in memory.
- **Writes** go to elements, as in `arr[0] = value`; the method never assigns to the parameter variable itself.
- **Elements** are `int` values, so a shallow copy is a complete copy.
- **Copy** made with `clone()` before the call is a separate array object.
- **Return value** does not exist.

**Example 1.** Input `a = b = [1,2,3]` and a method that sets `a[0] = 9`, output that `b[0]` also reads 9.

**Example 2.** Input `b = a.clone()` taken before the call, output that `b` still reads `[1,2,3]` after `a` changes.

**Hint.** Is there one array or two? What does the assignment `b = a` copy, the contents or the reference?

**Changed decision.** No algorithm changes. Only the caller-visible specification changes, from a private array to one shared with another reference.

#### [Recognize] Output Space (Author exercise)
<!-- id: pc-output-space -->

**Prerequisites.** All three exercises above.

**Problem.** A method receives an array of length `n` and must return a new array of length `n`. Total space is all memory the method allocates, including the returned array. Auxiliary space is the memory the method allocates beyond the input and the returned output. Compute both quantities for a method that fills one new result array. State the total space under the convention that counts the output. State the auxiliary space under the convention that excludes it. The output alone needs `n` slots under any plan.

**Constraints.** The limits are:
- **Size** is `1 <= n <= 10^5`.
- **Allocation** is exactly one result array of length `n` plus a constant number of scalar variables.
- **Input** is never modified.
- **Units** are `O(...)` notation as a function of `n`.

**Example 1.** Input an array of length 5 and a method that fills a new array of length 5, output auxiliary space O(1) under the convention that the result is excluded.

**Example 2.** Input the same method counted under the convention that includes the result, output total space O(n).

**Hint.** If a method had to return `n` values, could it return them with less than O(n) memory of any kind? Which part of the O(n) did the problem statement demand?

**Changed decision.** The question moves from whether the input may change to which storage is charged against the solution.
