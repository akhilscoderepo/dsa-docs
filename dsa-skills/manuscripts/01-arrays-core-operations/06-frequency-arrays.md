<!-- lesson-kind: standard -->
<!-- lesson-id: frequency-arrays -->
## Frequency Arrays

<!-- stage: context -->
### Tallying Quiz Scores

A teacher grades a ten-point quiz for a class of two hundred students and wants to know how many students earned each score from 0 to 10. She does not need names or order, only a tally. In the old days she would draw eleven columns on the board and add a mark to the right column as each paper came off the pile.

The tally board has a property worth noticing. The number of columns is fixed by the grading scale and has nothing to do with the number of students. Each paper touches exactly one column, and the whole tally is finished when the pile is empty. When the possible values form a small known range, a board with one slot per value does the work of an entire search.

<!-- stage: naive -->
### Count One Score At A Time

A direct translation of the question is to go through each possible score and scan the whole pile to count it.

```java
static int[] tallyByRescanning(int[] scores, int maxScore) {
    int[] tally = new int[maxScore + 1];
    for (int s = 0; s <= maxScore; s++) {
        for (int i = 0; i < scores.length; i++) {
            if (scores[i] == s) tally[s]++;
        }
    }
    return tally;
}
```

For 200 papers and eleven scores it makes 2,200 comparisons, which is nothing. The structure mirrors the question word for word, one count per score, each computed independently.

<!-- stage: bottleneck -->
### One Full Scan Per Possible Value

With `n` elements and `V` possible values the loops perform `n * V` comparisons, so the cost is O(n * V). That is cheap for eleven scores. It becomes painful when the scale is wide. With `n = 100,000` readings that take values from 0 to 100,000, the method makes ten billion comparisons, while the answer could have been assembled from a single look at each reading.

The repeated scans are the waste. Each paper is examined `V` times, though it can contribute to exactly one count, and `V - 1` of those examinations return nothing. The memory use is O(V) for the tally, which is unavoidable if the answer is one count per value, so only the time can improve.

<!-- stage: insight -->
### Let The Value Choose Its Own Slot

If values are small non-negative integers, a value can serve directly as an index. Reading a paper with score 7 means incrementing slot 7, and nothing needs to be searched or compared.

A **frequency array** is an array whose index is a value and whose entry is how many times that value has appeared. It works when the values lie in a **bounded domain**, a small integer range stated by the problem, so that one slot per possible value is affordable. The invariant is that after processing a prefix of the input, `count[v]` equals the number of times `v` occurred in that prefix, for every `v` in the domain. One pass maintains it, and each element costs one increment.

<!-- names: frequency array, bounded domain -->

Everything downstream of the counts becomes cheap. To know how many values are smaller than `v`, add up the counts of all lower slots, which turns the table into a running total over values and answers each question in constant time. To produce the input in sorted order, write each value out as many times as its count says, which is a counting sort that runs in O(n + V) and beats comparison sorting when `V` is small. Both ideas appear in the exercises.

The technique has a clear price and a clear limit. The price is memory proportional to the size of the domain, so a domain of 101 slots is free and a domain of a billion is out of the question. The limit is that the problem must promise the domain. If values can be arbitrary integers or arbitrary identifiers, the index would be unbounded, and a hash map from a later chapter takes over.

<!-- stage: variables -->
### The Table And Its Range

The table `count` has one slot per value in the domain, so its length is the largest allowed value plus one when the domain starts at zero, or it needs an offset when values start elsewhere. Declare it before the loop, where Java fills it with zeros, which is the correct count for an empty prefix. Each input value is validated against the range before it is used as an index, because an out-of-range index throws an exception and a negative one fails in the same way.

<!-- stage: trace -->
### Tallying Five Digits

Take the digits `[2, 0, 2, 9, 2]` and a table of ten slots numbered 0 through 9, all starting at zero. Reading the first 2 raises slot 2 to 1. Reading 0 raises slot 0 to 1. Reading the second 2 raises slot 2 to 2, and reading 9 raises slot 9 to 1. Reading the third 2 raises slot 2 to 3.

The finished table has 1 in slot 0, 3 in slot 2, 1 in slot 9, and zeros elsewhere, and the counts add up to five, the number of digits read. The step that matters is the last one. Slot 2 climbed from 2 to 3 without any comparison against earlier digits, because the value itself pointed at its counter. Compare that with the rescanning method, which would have walked the whole list once for each of the ten slots.

```trace
{"cells":[2,0,2,9,2],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"digit":2,"count[digit]":1,"total":1},"note":"Read 2. Slot 2 rises to 1. No comparison with earlier digits is made; the value itself points at its counter."},{"at":{"i":1},"vars":{"digit":0,"count[digit]":1,"total":2},"note":"Read 0. Slot 0 rises to 1. No comparison with earlier digits is made; the value itself points at its counter."},{"at":{"i":2},"vars":{"digit":2,"count[digit]":2,"total":3},"note":"Read 2. Slot 2 rises to 2. No comparison with earlier digits is made; the value itself points at its counter."},{"at":{"i":3},"vars":{"digit":9,"count[digit]":1,"total":4},"note":"Read 9. Slot 9 rises to 1. No comparison with earlier digits is made; the value itself points at its counter."},{"at":{"i":4},"vars":{"digit":2,"count[digit]":3,"total":5},"note":"Read 2. Slot 2 rises to 3. No comparison with earlier digits is made; the value itself points at its counter."}]}
```

<!-- stage: code -->
### Counting, Validating And Accumulating

```java
static int[] digitCounts(int[] digits) {
    int[] count = new int[10];
    for (int d : digits) count[d]++;
    return count;
}

static int[] diceCounts(int[] rolls) {
    int[] count = new int[7];                     // slots 1..6 are used; slot 0 stays unused
    for (int r : rolls) {
        if (r < 1 || r > 6) throw new IllegalArgumentException("not a die face: " + r);
        count[r]++;
    }
    return count;
}

static int[] smallerThanEach(int[] nums, int maxValue) {
    int[] count = new int[maxValue + 1];
    for (int v : nums) count[v]++;
    int[] below = new int[maxValue + 2];          // below[v] = how many values are < v
    for (int v = 0; v <= maxValue; v++) below[v + 1] = below[v] + count[v];
    int[] out = new int[nums.length];
    for (int i = 0; i < nums.length; i++) out[i] = below[nums[i]];
    return out;
}
```

Each method makes a constant number of passes over the input and one pass over the table, so the time is O(n + V) and the space is O(V) plus the output. `diceCounts` checks the range first, since an unchecked `count[0]` increment would hide a bad roll in a slot that nobody reads. In `smallerThanEach` the array `below` is shifted by one so that `below[v]` counts strictly smaller values without any special case at zero.

<!-- stage: applicability -->
### When The Domain Is Small And Promised

Use a frequency array when values are integers in a small range that the problem states, and you need counts, sortedness, or comparisons between values. The invariant is that `count[v]` always equals the number of processed elements equal to `v`. Check the size of the table against the memory budget before allocating it.

The false friend is an array indexed by arbitrary identifiers. A user id up to a billion would need a four-gigabyte table, and a negative value cannot index at all without an offset. Chapter 04 owns hash maps, which count arbitrary keys at a modest memory cost. If the statement does not promise a bounded range, assume the domain is not bounded.

Java supplies the zero-filled table for free, and it also supplies the exceptions. Index validation is the part to remember. For a character alphabet, subtract `'a'` to land in 0..25 only after confirming the input is lowercase, and for signed values add an offset equal to the smallest allowed value. Prefer `int[]` over a boxed collection here, because the memory per slot is smaller and there is no pointer chase.

<!-- stage: exercises -->
### Exercises

#### [Build] Digit Counts (Author exercise)
<!-- id: ar-digit-counts -->

**Prerequisites.** Chapter 00 constraint signals; the frequency table in this lesson.

**Problem.** Given an array `digits` whose values are all in `0..9`, return an array of ten counts where entry `d` is the number of times `d` occurs.

**Constraints.** 0 <= digits.length <= 10^5 and 0 <= digits[i] <= 9. Aim for one pass over the input and a ten-slot table.

**Example 1.** Input `digits = [2, 0, 2]`, output `[1, 0, 2, 0, 0, 0, 0, 0, 0, 0]`.

**Example 2.** Input `digits = []`, output ten zeroes, since the empty prefix has no occurrences.

**Hint.** What can a digit's own value serve as? What should the table hold before any digit has been read?

**Changed decision.** First rung: the value becomes the index, which removes all searching.

#### [Vary] How Many Numbers Are Smaller Than the Current Number (LeetCode 1365)
<!-- id: ar-smaller-than-current -->

**Prerequisites.** The digit-counts exercise above.

**Problem.** Given an array `nums`, return an array in which each entry is the count of values in `nums` that are strictly smaller than the value at that position. The small value range allows counting instead of comparing every pair.

**Constraints.** 2 <= nums.length <= 500 and 0 <= nums[i] <= 100. Aim for time proportional to `n` plus the range size.

**Example 1.** Input `nums = [6, 5, 4, 8]`, output `[2, 1, 0, 3]`.

**Example 2.** Input `nums = [7, 7, 7]`, output `[0, 0, 0]`, because equal values are not smaller.

**Hint.** If you know how many times each value occurs, how can you obtain the number of values below `v` without scanning the input? What must you add up?

**Changed decision.** The counts are turned into running totals over values, so each query is a single table lookup.

#### [Boundary] Dice Validation (Author exercise)
<!-- id: ar-dice-validation -->

**Prerequisites.** The two exercises above.

**Problem.** Count how many times each face of a six-sided die appears in an array of rolls, but reject any value outside `1..6` before using it as an index. Decide what the method does on a bad roll and document it.

**Constraints.** 0 <= rolls.length <= 10^5. The table has seven slots and slot 0 is unused. A bad roll must not corrupt a count or throw an unrelated exception.

**Example 1.** Input `rolls = [1, 6, 6]`, output counts of 1 for face 1 and 2 for face 6, with all other faces at 0.

**Example 2.** Input `rolls = [1, 6, 0]`, output a rejection of the roll 0 before any index is used.

**Hint.** Which index would an unchecked roll of 0 increment, and would anyone ever notice? What should the method promise about the input?

**Changed decision.** The question moves from counting to protecting the index, since the table's range is a contract that must be enforced.

#### [Recognize] Height Checker (LeetCode 1051)
<!-- id: ar-height-checker -->

**Prerequisites.** All three exercises above.

**Problem.** Students line up by height, and the expected line is the heights in non-decreasing order. Given the current heights, return the number of positions where the current height differs from the expected height. Use the small range to build the sorted order by counting instead of comparison sorting.

**Constraints.** 1 <= heights.length <= 100 and 1 <= heights[i] <= 100. The input must not be modified.

**Example 1.** Input `heights = [2, 1, 3, 3, 4]`, output 2, since positions 0 and 1 differ from `[1, 2, 3, 3, 4]`.

**Example 2.** Input `heights = [1, 2, 3]`, output 0, because the line is already ordered.

**Hint.** How do you list the values in sorted order if you know how many times each occurs? Do you need to build the sorted array first, or can you compare as you walk the table?

**Changed decision.** A compact known range makes counting preferable to comparison sorting, and the table is used to generate order.
