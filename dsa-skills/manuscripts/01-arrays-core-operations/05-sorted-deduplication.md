<!-- lesson-kind: standard -->
<!-- lesson-id: sorted-deduplication -->
## Sorted Deduplication

<!-- stage: context -->
### The Guest List With Double Sign-Ins

An event desk keeps its sign-in sheet in alphabetical order by surname, and a few guests signed in twice, so their names appear on consecutive lines. The organizer wants a clean list with each guest once, still in alphabetical order, and wants it on the same sheet, since there is no spare paper.

The desk volunteer does not need to compare each name with the whole sheet. Because the sheet is alphabetical, a repeated name can only be sitting directly beneath its twin. A single glance at the previous kept line settles whether the current line is new. That shortcut depends entirely on the ordering, and losing it changes the problem.

<!-- stage: naive -->
### Compare With Everything Kept So Far

Without trusting the order, the safe method checks each element against every value already kept.

```java
static int dedupeByPrefixScan(int[] nums) {
    int kept = 0;
    for (int read = 0; read < nums.length; read++) {
        boolean seen = false;
        for (int j = 0; j < kept; j++) {
            if (nums[j] == nums[read]) { seen = true; break; }
        }
        if (!seen) nums[kept++] = nums[read];
    }
    return kept;
}
```

This works on any array, sorted or not, and it keeps the first copy of each value. For `[1, 1, 2, 3, 3]` it returns 3 with the prefix `[1, 2, 3]`.

<!-- stage: bottleneck -->
### The Inner Scan Ignores The Ordering

When every value is distinct the inner loop checks all the kept values each time, so the total is 0 + 1 + 2 + ... + (n - 1), which is O(n^2). With 100,000 distinct values that is nearly five billion comparisons, and the method is using none of the information it was given. The extra space is O(1).

The wasted effort is easy to see. In a sorted array, any earlier occurrence of the current value must sit immediately before it. All the other kept values are strictly smaller, so comparing against them can never match. Of the `kept` comparisons the inner loop performs, at most one can ever succeed, and it is always the most recently kept one.

<!-- stage: insight -->
### One Comparison Against The Last Kept Value

If equal values sit next to each other, then deciding whether the current element is new takes one comparison, with the last value written. If it differs from that value, it starts a fresh group, so it is kept. If it equals it, it repeats a value already represented, so it is skipped.

A maximal block of equal values is a **run**. In a sorted array every value occupies exactly one run, and runs appear in increasing order. The written prefix holds one **representative** for each run seen so far, and the invariant says exactly that: the written prefix contains one representative of every completed run, in order. Nothing is kept twice, and nothing is skipped without a representative already in place.

<!-- names: run, representative, admission rule -->

The comparison against the last written value is an **admission rule**. It decides whether an element may be written. Changing the rule changes the problem without changing the machinery. To allow each value up to two copies, compare with the value two slots back in the written prefix instead of the one directly behind it. If the current value differs from `nums[write - 2]`, then fewer than two copies of it are in the prefix, so it may be admitted. For any allowed count `k`, the rule is to compare with `nums[write - k]`, and the first `k` elements are always admitted because the prefix is too short to hold `k` earlier copies.

This is still the read and write pair from the previous lesson. What is new is that the admission rule looks at the written prefix rather than only at the current value, which is only legitimate because sorted order guarantees that equal values are adjacent.

<!-- stage: variables -->
### Read, Write And The Rule

The read index visits every element once. The write index is the count of admitted elements, and the slot `write - 1` holds the most recent representative. The first element is always admitted, since an empty prefix contains no copy of it, so the loop can start with `write = 1` and `read = 1`, provided the array is non-empty. The limit on copies, `k`, appears in the rule as the offset `write - k`.

<!-- stage: trace -->
### Collapsing Runs In A Sorted Sheet

Take `[1, 1, 2, 3, 3, 3, 4]` and keep one copy of each value. The first 1 is admitted automatically, so the prefix is `[1]` and the write index is 1. At read 1 the value 1 equals the last kept value, so it is skipped. At read 2 the value 2 differs from 1, so it is admitted, giving `[1, 2]`.

At read 3 the value 3 differs from 2 and is admitted, giving `[1, 2, 3]`. Reads 4 and 5 are further 3s that equal the last kept value, so both are skipped. At read 6 the value 4 differs from 3 and is admitted. The loop ends with the prefix `[1, 2, 3, 4]` and a write index of 4. The step that deserves attention is read 5, the last of the repeated 3s. By then three comparisons in a row against the single last kept value have been enough, and no earlier value was ever consulted.

```trace
{"cells":[1,1,2,3,3,3,4],"pointers":["read","write"],"steps":[{"at":{"read":0,"write":1},"vars":{"kept":1,"prefix":"[1]"},"note":"Read 0: the first value is always admitted. The prefix is [1] and write is 1."},{"at":{"read":1,"write":1},"vars":{"kept":1,"prefix":"[1]"},"note":"Read 1: 1 equals the last kept value, so it is skipped. The prefix stays [1]."},{"at":{"read":2,"write":2},"vars":{"kept":2,"prefix":"[1,2]"},"note":"Read 2: 2 differs from the last kept value 1, so it is admitted. The prefix grows to [1, 2]."},{"at":{"read":3,"write":3},"vars":{"kept":3,"prefix":"[1,2,3]"},"note":"Read 3: 3 differs from the last kept value 2, so it is admitted. The prefix grows to [1, 2, 3]."},{"at":{"read":4,"write":3},"vars":{"kept":3,"prefix":"[1,2,3]"},"note":"Read 4: 3 equals the last kept value, so it is skipped. The prefix stays [1, 2, 3]."},{"at":{"read":5,"write":3},"vars":{"kept":3,"prefix":"[1,2,3]"},"note":"Read 5: 3 equals the last kept value, so it is skipped. The prefix stays [1, 2, 3]."},{"at":{"read":6,"write":4},"vars":{"kept":4,"prefix":"[1,2,3,4]"},"note":"Read 6: 4 differs from the last kept value 3, so it is admitted. The prefix grows to [1, 2, 3, 4]."}]}
```

<!-- stage: code -->
### One Rule, Any Copy Limit

```java
static int dedupe(int[] nums) {
    if (nums.length == 0) return 0;
    int write = 1;                                  // nums[0] is always admitted
    for (int read = 1; read < nums.length; read++) {
        if (nums[read] != nums[write - 1]) nums[write++] = nums[read];
    }
    return write;
}

static int keepAtMost(int[] nums, int limit) {
    int write = 0;
    for (int read = 0; read < nums.length; read++) {
        if (write < limit || nums[read] != nums[write - limit]) nums[write++] = nums[read];
    }
    return write;
}
```

The first method compares only with the last written value, and the second generalizes the rule to a limit of `limit` copies per value. Both run in O(n) time and O(1) extra space, and both require the input to be sorted, which is a guarantee they rely on and never check. If `limit` is 1, the second reduces to the first. Note that `write - limit` is only evaluated when `write >= limit`, because the short-circuit `||` stops earlier.

<!-- stage: applicability -->
### When Equal Values Are Neighbors

Use sorted deduplication when the input is sorted, so equal values form adjacent runs, and you want to keep one or a few representatives per run in place. The invariant is that the written prefix contains the right number of representatives of every completed run, in order. Admission is a single comparison against a slot of the written prefix.

The false friend is unsorted data. On `[1, 2, 1]` the comparison against the last kept value sees 2 and then 1 and keeps all three, because the two 1s are not adjacent. The method then reports success while leaving duplicates. For unsorted data you need a set from Chapter 04 or a sort from Chapter 05 first. Another look-alike is compaction by a value test, which keeps or drops each element independently, whereas here an element's fate depends on the previous kept element.

Java details matter for the generalization. Compare primitive `int` values with `==` and `!=`, but if the array held boxed `Integer` objects, `!=` would compare references and misbehave for larger values. And when the same technique is applied to a `char[]`, as in the last exercise, completed runs must be counted before they are written, because the output for a run can be longer or shorter than the run itself.

<!-- stage: exercises -->
### Exercises

#### [Build] Remove Duplicates from Sorted Array (LeetCode 26)
<!-- id: ar-remove-duplicates -->

**Prerequisites.** The read and write indices from stable compaction; this lesson.

**Problem.** Given an integer array sorted in non-decreasing order, remove duplicates in place so that each distinct value appears once, keeping the relative order. Return the number `k` of distinct values, with the first `k` slots holding them.

**Constraints.** 0 <= nums.length <= 3 * 10^4 and -100 <= nums[i] <= 100, with `nums` sorted non-decreasing. Use O(1) extra space.

**Example 1.** Input `nums = [1, 1, 2, 3, 3, 3, 4]`, output `k = 4` with prefix `[1, 2, 3, 4]`.

**Example 2.** Input `nums = []`, output `k = 0`, so the empty array needs no special branch beyond the length check.

**Hint.** Which value does the current element have to differ from to count as new? Where does that value live?

**Changed decision.** First rung: the admission test looks at the written prefix and relies on sorted order.

#### [Vary] Remove Duplicates from Sorted Array II (LeetCode 80)
<!-- id: ar-remove-duplicates-two -->

**Prerequisites.** The remove-duplicates exercise above.

**Problem.** Given a sorted array, remove duplicates in place so that each distinct value appears at most twice, keeping the relative order. Return the new length `k`, with the first `k` slots holding the result.

**Constraints.** 1 <= nums.length <= 3 * 10^4 and -10^4 <= nums[i] <= 10^4, with `nums` sorted non-decreasing. Use O(1) extra space.

**Example 1.** Input `nums = [0, 0, 0, 1, 1, 1, 1, 2]`, output `k = 5` with prefix `[0, 0, 1, 1, 2]`.

**Example 2.** Input `nums = [7, 7, 7]`, output `k = 2` with prefix `[7, 7]`.

**Hint.** To allow two copies, which slot of the written prefix must the current value differ from? What happens for the first two elements?

**Changed decision.** The admission rule now reads `nums[write - 2]` instead of `nums[write - 1]`.

#### [Boundary] Keep One Per Run (Author exercise)
<!-- id: ar-keep-one-per-run -->

**Prerequisites.** The two exercises above.

**Problem.** Verify your deduplication on the two extreme shapes: an array in which every value is equal and an array that is already free of duplicates. State the returned count and the resulting prefix for each, and explain why neither needs a special case.

**Constraints.** 1 <= nums.length <= 10^5, sorted non-decreasing. The all-equal array is a single run, and the already-unique array is one run per element.

**Example 1.** Input `nums = [5, 5, 5]`, output `k = 1` with prefix `[5]`.

**Example 2.** Input `nums = [1, 2, 3]`, output `k = 3` with the array unchanged.

**Hint.** How many runs does each array contain? What does the admission rule do when every element differs from the last kept one?

**Changed decision.** The two extremes of run structure, one run and all runs, test whether the loop bounds and the first-element rule are right.

#### [Recognize] String Compression (LeetCode 443)
<!-- id: ar-string-compression -->

**Prerequisites.** All three exercises above.

**Problem.** Given a `char[]`, compress it in place by replacing each run of identical characters with the character followed by the run length, but only when the run length is greater than 1. Lengths of ten or more are written as separate digit characters. Return the new length of the array.

**Constraints.** 1 <= chars.length <= 2000 and each character is a lowercase letter, an uppercase letter or a digit. Use O(1) extra space.

**Example 1.** Input `chars = ['a','a','b','c','c','c']`, output length 5 with prefix `['a','2','b','c','3']`.

**Example 2.** Input `chars = ['x','x','x','x','x','x','x','x','x','x','x','x']`, output length 3 with prefix `['x','1','2']`.

**Hint.** When does a run end, and what must you know before writing its output? Can the output for a run ever overtake the read position?

**Changed decision.** The representation is characters and each completed run owns a variable-length write decision.
