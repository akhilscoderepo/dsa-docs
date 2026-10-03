<!-- lesson-kind: standard -->
<!-- lesson-id: sequence-language -->
## Sequence Language

<!-- stage: context -->
### Best Days Or Best Streak

A product manager asks an analyst for the best stretch of days in a week of sales changes: `[2, -5, 3, 4]`. The analyst returns 9, reasoning that the good days are 2, 3 and 4. The manager looks at the calendar and says there is no stretch of days that adds up to 9. The most any unbroken run of days can give is 7, from the last two days, and the day with the loss of 5 sits in the middle of the only run that includes both the 2 and the 3.

The analyst answered a different question than the one asked. Both are reasonable questions, and the words that separate them are small. Problem statements use a handful of such words constantly, and a wrong reading of one of them produces a correct-looking answer to the wrong problem.

<!-- stage: naive -->
### Take The Good Parts

The quick reading of "best portion of the list" is to keep whatever helps. For a sum, that means adding up every positive value and ignoring the rest.

```java
static int bestPortionLoose(int[] nums) {
    int total = 0;
    for (int v : nums) {
        if (v > 0) total += v;
    }
    return total;
}
```

On `[2, -5, 3, 4]` this returns 9. It is fast, it is simple, and it matches the sample if the sample happens to be a pick-any-days question. It is a correct answer to that question and a wrong answer to the streak question.

<!-- stage: bottleneck -->
### Two Questions, Two Search Spaces

The difference is the size of what is being searched. A run of consecutive days is fixed by where it starts and where it ends, so a list of `n` values has `n * (n + 1) / 2` non-empty runs, which is O(n^2). For `n = 20` that is 210 candidates. Picking any days while keeping their order, or picking any days at all, gives `2^n - 1` non-empty choices. For `n = 20` that is 1,048,575 candidates, and at `n = 60` it is beyond what any machine can enumerate.

So the two readings do not only give different answers on one sample, they call for different algorithms with different costs. A method that quietly solves the larger space, as the greedy sum above does, can be fast because the larger space has an easy answer for sums, and it is still wrong for the smaller space, because the smaller space imposes a restriction the greedy sum ignores. The restriction is what the lesson names.

<!-- stage: insight -->
### Which Index Relationships Must Survive

Each of the three words describes a rule about the positions you may choose. Write the rule down before reading the examples.

A **subarray** is a block of consecutive positions, which means no position inside it is skipped. Its string counterpart is a substring. A **subsequence** is a selection of positions that keeps the original left-to-right order but may skip any of them. A **subset**, in the sense used by these problems, is any selection of positions at all, with no promise about adjacency or order.

<!-- names: subarray, subsequence, subset -->

Every subarray is also a subsequence, and every subsequence is also a subset, but the reverse never holds in general. That nesting is why a sample answer can satisfy two or three definitions at once while the underlying questions differ. `[2, 3]` taken from `[1, 2, 3, 4]` is all three, which proves nothing about which one the problem meant.

The invariant that decides a classification is positional. Write the positions of the candidate's values in the original array. If those positions are consecutive, the candidate is a subarray. If they strictly increase but have gaps, it is a subsequence and not a subarray. If they appear in any other order, it is only a subset. Two further words need the same care. A prefix is a subarray that starts at the first position, and a suffix is one that ends at the last position.

<!-- stage: variables -->
### Positions, Gaps And Order

Classification needs one list and two questions. The list is the positions of the chosen values in the original array, read in the order the candidate lists them. The first question is whether each position is exactly one more than the previous one, which tests for no gaps. The second is whether each position is larger than the previous one, which tests for preserved order. Repeated values make this slightly harder, because the same value may sit at several positions, so the question becomes whether some assignment of positions satisfies the rule.

<!-- stage: trace -->
### Classifying Two Candidates

Take the array `[1, 2, 3, 4]` and the candidate `[2, 4]`. The value 2 lives at position 1 and the value 4 at position 3. The positions rise, from 1 to 3, so the original order is preserved. The gap between them is 2, not 1, so position 2 was skipped. That makes the candidate a subsequence and a subset and rules out a subarray.

Now take the candidate `[4, 2]` on the same array. The value 4 lives at position 3 and then the value 2 at position 1. The positions fall, so the order was reversed, and the candidate is neither a subarray nor a subsequence. It is still a subset, because a subset makes no promise about order. The step that students miss is the second candidate's order test. Holding the same two values makes it feel like the same answer, and only the positions reveal that one candidate respects the original order and the other does not.

```trace
{"cells":[1,2,3,4],"pointers":["first","second"],"steps":[{"at":{"first":1,"second":-1},"vars":{"candidate":"[2,4]","gap":"-","order":"-"},"note":"Candidate [2,4]. The value 2 sits at position 1."},{"at":{"first":1,"second":3},"vars":{"candidate":"[2,4]","gap":"2","order":"rises"},"note":"The value 4 sits at position 3. The step is 2, so position 2 was skipped, and the positions rise."},{"at":{"first":1,"second":3},"vars":{"candidate":"[2,4]","gap":"2","order":"rises","verdict":"subsequence and subset, not subarray"},"note":"Verdict: a gap means no subarray, rising positions mean a subsequence, and any selection is a subset."},{"at":{"first":3,"second":-1},"vars":{"candidate":"[4,2]","gap":"-","order":"-"},"note":"Candidate [4,2]. The value 4 sits at position 3."},{"at":{"first":3,"second":1},"vars":{"candidate":"[4,2]","gap":"-2","order":"falls"},"note":"The value 2 sits at position 1. The positions fall, so the original order was reversed."},{"at":{"first":3,"second":1},"vars":{"candidate":"[4,2]","gap":"-2","order":"falls","verdict":"subset only"},"note":"Verdict: falling positions rule out both a subarray and a subsequence. Only the subset rule remains."}]}
```

<!-- stage: code -->
### A Classifier From Positions

```java
// True when cand appears in nums as one unbroken block.
static boolean isContiguousBlock(int[] nums, int[] cand) {
    for (int start = 0; start + cand.length <= nums.length; start++) {
        int j = 0;
        while (j < cand.length && nums[start + j] == cand[j]) j++;
        if (j == cand.length) return true;
    }
    return cand.length == 0;
}

// True when cand appears in order, gaps allowed (greedy earliest match).
static boolean isInOrder(int[] nums, int[] cand) {
    int j = 0;
    for (int i = 0; i < nums.length && j < cand.length; i++) {
        if (nums[i] == cand[j]) j++;
    }
    return j == cand.length;
}
```

The first method tries every start position and compares a block, so it costs O(n * m) for a candidate of length `m`. The second is a single left-to-right scan, which is O(n), and its greedy choice of the earliest match is safe because taking an earlier position never makes a later match harder. The two methods differ by exactly the rule the lesson stated, a block versus an ordered selection. A subset test would ignore order and compare counts of values, which a later chapter on hash maps makes cheap.

<!-- stage: applicability -->
### Reading The Word Before The Example

Whenever a statement says subarray, substring, subsequence, subset, prefix or suffix, restate its index rule in one line before looking at the examples. The invariant is that the answer must satisfy the stated position rule exactly, not merely resemble a sample. A fast greedy that passes the samples but answers a larger search space than the one asked is the typical failure.

The false friend is the pair of everyday words "substring" and "subsequence", which many people use interchangeably. The same goes for "subarray" and "subset". They are not interchangeable even when a sample answer satisfies several definitions, and the samples in problem statements are often chosen so that they do.

Java gives mild support for the contiguous case and none for the others. `String.substring` and `Arrays.copyOfRange` both produce blocks, and the second one excludes its end index. Neither can express a subsequence, which has to be coded as a scan. When a statement says "contiguous" or "consecutive", it is telling you the subarray rule even if it avoids the word.

<!-- stage: exercises -->
### Exercises

#### [Build] Classify [2,4] (Author exercise)
<!-- id: pc-classify-2-4 -->

**Prerequisites.** The position rules for subarray, subsequence and subset in this lesson.

**Problem.** For `nums = [1,2,3,4]`, decide whether `[2,4]` is a subarray, a subsequence and a subset. Justify each answer from the positions of the values in the original array, and not from how the values look.

**Constraints.** The array holds distinct values, so each value has one position. Treat the empty selection as out of scope for this exercise.

**Example 1.** Input `nums = [1,2,3,4]` and candidate `[2,4]`, output not a subarray, yes a subsequence and yes a subset.

**Example 2.** Input `nums = [1,2,3,4]` and candidate `[2,3]`, output yes for all three, because positions 1 and 2 are consecutive.

**Hint.** Write down the position of each candidate value. Are the positions consecutive, merely increasing, or neither?

**Changed decision.** First rung: replaces an impression of similarity with a test on positions.

#### [Vary] Order Matters (Author exercise)
<!-- id: pc-order-matters -->

**Prerequisites.** The classification exercise above.

**Problem.** For the same input `nums = [1,2,3,4]`, classify the candidate `[4,2]`. State the single changed decision compared with `[2,4]`, which is whether the original relative order must be preserved.

**Constraints.** The values are distinct. A subset is judged by membership alone, with no promise about order.

**Example 1.** Input `nums = [1,2,3,4]` and candidate `[4,2]`, output not a subarray, not a subsequence, yes a subset.

**Example 2.** Input `nums = [1,2,3,4]` and candidate `[1,2,3,4]`, output yes for all three, since the candidate is the whole array.

**Hint.** What happens to the positions when you list 4 before 2? Which of the three rules cares about the direction of the positions?

**Changed decision.** The candidate's order flips, so the test moves from checking gaps to checking direction.

#### [Boundary] Empty Choice (Author exercise)
<!-- id: pc-empty-choice -->

**Prerequisites.** The two exercises above.

**Problem.** A statement asks for the maximum sum of a subarray of `nums = [-8,-3,-6]`. Decide whether the empty subarray is legal only after reading the contract, and show how the answer differs when the empty choice is allowed and when it is forbidden.

**Constraints.** `1 <= nums.length <= 10^5` and `-10^4 <= nums[i] <= 10^4`. The statement must say whether the result may be empty. Do not assume a convention.

**Example 1.** Input `nums = [-8,-3,-6]` with a non-empty requirement, output -3, the best single reading.

**Example 2.** Input `nums = [-8,-3,-6]` with the empty choice allowed, output 0, the sum of choosing nothing.

**Hint.** What is the sum of an empty block, and does the contract say such a block counts? Which answer would an all-negative array expose if you guessed wrongly?

**Changed decision.** The legal set of candidates changes by one element, the empty selection, and that one element flips the answer.

#### [Recognize] Contiguous Maximum (Author exercise)
<!-- id: pc-contiguous-maximum -->

**Prerequisites.** All three exercises above.

**Problem.** For `nums = [5,-10,4]`, compute the maximum sum of a non-empty subarray and the maximum sum of a non-empty subsequence. Explain why a subarray cannot skip a negative middle value while a subsequence can. The algorithm for the contiguous case belongs to Chapter 01.

**Constraints.** `1 <= nums.length <= 20`, small enough to enumerate every candidate by brute force.

**Example 1.** Input `nums = [5,-10,4]` as a subarray question, output 5.

**Example 2.** Input `nums = [5,-10,4]` as a subsequence question, output 9, from positions 0 and 2.

**Hint.** Which blocks of consecutive positions contain both the 5 and the 4? What do they also contain?

**Changed decision.** The same data and the same sum objective give two answers because the position rule changes.
