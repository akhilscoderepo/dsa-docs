<!-- lesson-kind: standard -->
<!-- lesson-id: mutation-contracts -->
## Mutation Contracts

<!-- stage: context -->
### The Report That Printed Garbage

A reporting tool keeps the day's sensor readings in one array and hands it to two helpers. The first helper strips out the readings flagged as faulty. The second prints the full day's readings for an audit. After the first helper runs, the audit page shows duplicates and missing values, and nobody has changed the audit code in months.

The helpers are not buggy in isolation. The first one rewrote the shared array to save memory, and the second one trusted that the array was untouched. Neither had been told what the other was allowed to do, because the interface never said whether the input could change. Every problem statement and every method signature carries an answer to that question, spoken or unspoken, and this lesson is about stating it out loud.

<!-- stage: naive -->
### Overwrite And Return The Same Array

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

Called on `[3, 2, 2, 3]` with target 3, it returns 2, and the array afterward reads `[2, 2, 2, 3]`. A caller who prints `nums.length` elements sees three twos and a three, and a caller who kept a second reference to the same array sees the damage too.

<!-- stage: bottleneck -->
### The Cost Is Surprise

The method runs in O(n) time with O(1) extra space, so no step is slow. The cost is that the data the caller still holds has been changed under them. The array has not become shorter, because a Java array's length is fixed when it is created. Only the first `write` slots are meaningful now, and the slots after that still hold old values that look real.

The safe alternative copies the input first. That copy costs O(n) extra space and O(n) extra time, which is cheap for one call and expensive for a million. So neither choice is free, and the right one depends on a promise that the code alone cannot reveal. When the statement says the input must be preserved, in-place rewriting is wrong however fast it is. When the statement asks for constant extra space, copying is wrong however clean it is.

<!-- stage: insight -->
### Separate The Container From The Answer

Two different things are easy to confuse here. The array is a physical container with a fixed length. The answer is a logical result that occupies some part of it. After an in-place filter, the logical result is the first `k` slots and nothing else, and the method's return value tells you `k`.

A **mutation contract** is the part of a problem's interface that says which inputs may be modified, what the caller may rely on afterward, and what storage the method may use. Writing it down takes one line, for example "input may be overwritten; positions `0..k-1` hold the result in original order; the rest is unspecified". The words "in place" are shorthand for such a contract, and they never mean the array got shorter.

<!-- names: mutation contract, logical result, auxiliary space -->

The cost counted against a solution is its **auxiliary space**, the extra working memory beyond the input and beyond the output the method is required to return. A method that must return a fresh array of `n` values uses O(n) space for the answer, and that is not auxiliary. Stating which convention you are using avoids an argument that is really about definitions.

The invariant that keeps an in-place rewrite safe is that every write must not destroy a value a later read still needs. The filter above is safe because `write` never passes `read`, so a slot is overwritten only after its original value has been read.

<!-- stage: variables -->
### Reference, Container And Boundary

Three things deserve names. The reference is the variable that points at the array, and two variables can point at the same one. The container is the array object itself with its fixed length. The boundary `k` is the count of meaningful slots, which in the filter equals `write` at the end. When a method may mutate, the contract must name `k` and say what the suffix holds, which is normally "unspecified", and the caller must never read it.

<!-- stage: trace -->
### Filtering The Four Readings

Run the filter on `[3, 2, 2, 3]` with target 3. The read index starts at slot 0, which holds a 3, so it is skipped and nothing is written. At slot 1 the value 2 is kept and copied to slot 0, which turns the array into `[2, 2, 2, 3]`. At slot 2 the next 2 is copied to slot 1, and the array does not visibly change because it was already a 2. At slot 3 the value 3 is skipped.

When the loop ends, `write` is 2, so the logical result is `[2, 2]`, the first two slots. The last two slots still hold `2` and `3`, and the 3 in slot 3 is a leftover from the original input, not a part of the answer. The step that teaches the most is the second one. It overwrote slot 0, destroying the first 3, which was safe only because that 3 had already been read and rejected. Anyone who held another reference to this array now sees `[2, 2, 2, 3]` and has lost the original.

```trace
{"cells":[3,2,2,3],"pointers":["read","write"],"steps":[{"at":{"read":0,"write":0},"vars":{"array":"[3,2,2,3]","k":0},"note":"Read slot 0, a 3: skip it. Nothing is written and write stays at 0."},{"at":{"read":1,"write":1},"vars":{"array":"[2,2,2,3]","k":1},"note":"Read slot 1, a 2: keep it and write it to slot 0. The array reads [2, 2, 2, 3]."},{"at":{"read":2,"write":2},"vars":{"array":"[2,2,2,3]","k":2},"note":"Read slot 2, a 2: keep it and write it to slot 1. The array reads [2, 2, 2, 3]."},{"at":{"read":3,"write":2},"vars":{"array":"[2,2,2,3]","k":2},"note":"Read slot 3, a 3: skip it. Nothing is written and write stays at 2."},{"at":{"read":4,"write":2},"vars":{"array":"[2,2,2,3]","k":2},"note":"Done. k = 2, so only the first 2 slots are the answer. The 3 left in the last slot is stale."}]}
```

<!-- stage: code -->
### Two Contracts, Two Methods

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

The first method is O(n) time and O(1) auxiliary space and gives up the original data. The second is O(n) time, makes two passes so the result has the exact length, and uses O(n) space for the answer it was required to return. Neither performs extra work for the other's contract, and picking the wrong one for the stated promise is a correctness error, not a style choice.

<!-- stage: applicability -->
### Reading The Promise

Check the mutation contract before writing a single line of an array or string solution. The invariant to keep in mind is that every write preserves the data a later read still needs, and that nothing outside the stated meaningful range is ever read by the caller. If the statement says nothing about mutation, ask or state your assumption, and prefer to leave the input intact when the cost is small.

The false friend is "in place" taken to mean the array shrank. In Java the length of an array never changes, so an in-place removal always comes with a returned count, and code that loops to `nums.length` afterward reads stale slots. A second false friend is believing that returning the same reference proves nothing changed. The caller's other references to that array see every write.

One more hazard sits in the language. Strings are immutable, so a method that appears to "modify" one has really built a new one, and `int[]` parameters are passed by reference value, so assignments to the parameter variable do not affect the caller while writes through it do. Chapter 01 uses these contracts on every in-place exercise.

<!-- stage: exercises -->
### Exercises

#### [Build] Meaningful Prefix (Author exercise)
<!-- id: pc-meaningful-prefix -->

**Prerequisites.** The filter method in this lesson.

**Problem.** Given `nums = [3,2,2,3]`, suppose a method removes the value 3 in place and returns `k = 2`. State exactly what is guaranteed about `nums[0..k-1]`, what is unspecified about `nums[k..]`, and what the caller must never do with the suffix.

**Constraints.** Java array length is fixed at creation. The method returns an `int` and may overwrite the input.

**Example 1.** Input `nums = [3,2,2,3]` and target 3, output `k = 2` and a meaningful prefix of `[2,2]`.

**Example 2.** Input `nums = [3,3]` and target 3, output `k = 0`, so there is no meaningful prefix at all and the whole array is unspecified.

**Hint.** The return value is the only thing that says how much of the array counts as the answer. What does the array's own `length` tell you after the call?

**Changed decision.** First rung: separates the physical array from the logical result and names the boundary `k`.

#### [Vary] Preserve Input (Author exercise)
<!-- id: pc-preserve-input -->

**Prerequisites.** The meaningful-prefix exercise above.

**Problem.** A contract forbids modifying the input array. Choose between overwriting `nums` and allocating a new `result`, and explain why a method that returns correct values but leaves the input modified still violates the interface.

**Constraints.** `1 <= nums.length <= 10^5`. Assume callers may keep using the original array after the call.

**Example 1.** Input `nums = [4,1,4,2]` and target 4 under a no-mutation contract, output `[1,2]` with `nums` still equal to `[4,1,4,2]`.

**Example 2.** Input the same call under a permissive contract, output that either design is valid, and the in-place one saves O(n) memory.

**Hint.** Who else may hold a reference to the array? Which part of the interface does a hidden write break even when the returned numbers are right?

**Changed decision.** The contract flips from permissive to restrictive, which flips the correct design from overwriting to allocating.

#### [Boundary] Aliased Input (Author exercise)
<!-- id: pc-aliased-input -->

**Prerequisites.** The two exercises above.

**Problem.** Two variables `a` and `b` refer to the same `int[]`. A method receives `a` and rewrites its contents in place. Trace why the change is visible through `b`, and state what a caller must do first if both views must remain independent.

**Constraints.** `a` and `b` reference one array object. The method assigns into elements and never reassigns the parameter variable itself.

**Example 1.** Input `a = b = [1,2,3]` and a method that sets `a[0] = 9`, output that `b[0]` also reads 9.

**Example 2.** Input `b = a.clone()` taken before the call, output that `b` still reads `[1,2,3]` after `a` changes.

**Hint.** Is there one array or two? What does the assignment `b = a` copy, the contents or the reference?

**Changed decision.** No algorithm changes. Only the caller-visible contract changes, from a private array to one shared with another reference.

#### [Recognize] Output Space (Author exercise)
<!-- id: pc-output-space -->

**Prerequisites.** All three exercises above.

**Problem.** A method must return an array of length `n` built from its input. Distinguish the O(n) returned output from additional working memory, and state both conventions explicitly: one in which the output counts as space and one in which only auxiliary space counts.

**Constraints.** `1 <= n <= 10^5`. The method may allocate one result array and a constant number of scalar variables.

**Example 1.** Input an array of length 5 and a method that fills a new array of length 5, output auxiliary space O(1) under the convention that the result is excluded.

**Example 2.** Input the same method counted under the convention that includes the result, output total space O(n).

**Hint.** If a method had to return `n` values, could it return them with less than O(n) memory of any kind? Which part of the O(n) did the problem statement demand?

**Changed decision.** The question moves from whether the input may change to which storage is charged against the solution.
