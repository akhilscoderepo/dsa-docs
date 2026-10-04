<!-- lesson-kind: standard -->
<!-- lesson-id: sequence-language -->
## Defining Subarrays, Subsequences And Subsets

<!-- stage: context -->
### Ambiguity In Reading Range Requirements

A product manager asks an analyst for the best run of consecutive days in a week of daily sales changes: `[2, -5, 3, 4]`. The analyst returns 9, because the good days are 2, 3 and 4. The manager checks the data and finds no run of consecutive days that adds up to 9. No unbroken run of days gives more than 7, from the last two days. The day with the loss of 5 sits in the middle of the only run that includes both the 2 and the 3.

The analyst answered a different question than the one asked. Both are reasonable questions, and the words that separate them are small. Problem statements use a handful of such words constantly. A wrong reading of one word produces a correct-looking answer to the wrong problem.

<!-- stage: naive -->
### Summing Every Positive Element

The quick reading of "best portion of the list" is to keep every element that increases the sum. For a sum, that means adding every positive value and ignoring the rest.

```java
static int bestPortionLoose(int[] nums) {
    int total = 0;
    for (int v : nums) {
        if (v > 0) total += v;
    }
    return total;
}
```

On `[2, -5, 3, 4]` this returns 9. The method is fast and simple. It matches the sample if the sample is a pick-any-days question. It answers that question correctly and answers the consecutive-run question wrongly.

<!-- stage: bottleneck -->
### Search Space Sizes Of Subarrays And Subsets

The two questions have search spaces of different sizes. A run of consecutive days is fixed by where it starts and where it ends. A list of `n` values therefore has `n * (n + 1) / 2` non-empty runs, which is O(n^2). For `n = 20` that is 210 candidates. Picking any days while keeping their order, or picking any days at all, gives `2^n - 1` non-empty choices. For `n = 20` that is 1,048,575 candidates. At `n = 60` no machine can enumerate them.

So the two readings give different answers on one sample, and they also call for different algorithms with different costs. The greedy sum solves the larger space quickly, because sums have an easy answer there. It is still wrong for the smaller space, because the smaller space imposes a restriction that the greedy sum ignores. The lesson names that restriction.

<!-- stage: insight -->
### Index Relationships In Selections

Each of the three words defines a rule about the index positions you may choose. Write the rule down before reading the examples.

#### Definitions Of Subarray, Subsequence And Subset

A **subarray** is a block of consecutive positions, so no position inside it is skipped. Its string counterpart is a substring. A **subsequence** is a selection of positions that keeps the original left-to-right order but may skip any position. A **subset**, in the sense these problems use, is any selection of positions, with no promise about adjacency or order.

<!-- names: subarray, subsequence, subset -->

#### Nesting Of The Three Definitions

Every subarray is also a subsequence, and every subsequence is also a subset. The reverse does not hold in general. That nesting explains why a sample answer can satisfy two or three definitions while the questions differ. `[2, 3]` taken from `[1, 2, 3, 4]` is all three, so it proves nothing about which one the problem means.

#### Classification By Index Positions

The invariant that decides a classification is positional. Write the positions of the candidate's values in the original array. If those positions are consecutive, the candidate is a subarray. If they strictly increase but have gaps, it is a subsequence and not a subarray. If they appear in any other order, it is only a subset. Two further words need the same care. A prefix is a subarray that starts at the first position. A suffix is a subarray that ends at the last position.

<!-- stage: variables -->
### Position List And Two Index Tests

Classification needs one list and two tests.

- **Position list** holds the index in the original array of each chosen value, in candidate order.
- **Gap test** checks that each position equals the previous position plus 1.
- **Order test** checks that each position is larger than the previous position.
- **Repeated values** occupy several positions, so the test asks whether some assignment of positions satisfies the rule.

<!-- stage: trace -->
### Classifying Two Candidates By Positions

#### Classifying Candidate `[2, 4]`

Take the array `[1, 2, 3, 4]` and the candidate `[2, 4]`.

- **Positions** are 1 for the value 2 and 3 for the value 4.
- **Order test** passes, because the positions rise from 1 to 3.
- **Gap test** fails, because the difference is 2, not 1, so position 2 is skipped.
- **Verdict** is a subsequence and a subset, and not a subarray.

#### Classifying Candidate `[4, 2]`

Now take the candidate `[4, 2]` on the same array.

- **Positions** are 3 for the value 4, then 1 for the value 2.
- **Order test** fails, because the positions fall.
- **Gap test** fails, because the difference is -2, not 1.
- **Verdict** is a subset only, because a subset makes no promise about order.

Both candidates hold the same two values, so they look like the same answer. Only the positions show that one candidate respects the original order and the other does not. The order test is the step most often missed on this second candidate.

#### Step Trace Of Both Classifications

```trace
{"cells":[1,2,3,4],"pointers":["first","second"],"steps":[{"at":{"first":1,"second":-1},"vars":{"candidate":"[2,4]","gap":"-","order":"-"},"note":"Candidate [2,4]. The value 2 sits at position 1."},{"at":{"first":1,"second":3},"vars":{"candidate":"[2,4]","gap":"2","order":"rises"},"note":"The value 4 sits at position 3. The step is 2, so position 2 was skipped, and the positions rise."},{"at":{"first":1,"second":3},"vars":{"candidate":"[2,4]","gap":"2","order":"rises","verdict":"subsequence and subset, not subarray"},"note":"Verdict: a gap means no subarray, rising positions mean a subsequence, and any selection is a subset."},{"at":{"first":3,"second":-1},"vars":{"candidate":"[4,2]","gap":"-","order":"-"},"note":"Candidate [4,2]. The value 4 sits at position 3."},{"at":{"first":3,"second":1},"vars":{"candidate":"[4,2]","gap":"-2","order":"falls"},"note":"The value 2 sits at position 1. The positions fall, so the original order was reversed."},{"at":{"first":3,"second":1},"vars":{"candidate":"[4,2]","gap":"-2","order":"falls","verdict":"subset only"},"note":"Verdict: falling positions rule out both a subarray and a subsequence. Only the subset rule remains."}]}
```

<!-- stage: code -->
### Position-Based Classifier Implementation

#### Contiguous And Ordered Match Methods

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

#### Time Complexity Of Both Methods

- **isContiguousBlock** costs O(n * m) for a candidate of length `m`, because it tries every start position and compares a block.
- **isInOrder** costs O(n), because it is a single left-to-right scan.
- **Earliest match** is a safe greedy choice, because taking an earlier position never makes a later match harder.
- **Subset test** ignores order and compares counts of values, and a later chapter on hash maps makes it cheap.

The two methods differ by exactly the rule the lesson stated, a block versus an ordered selection.

<!-- stage: applicability -->
### Applying The Index Rule To Problem Statements

#### Restating The Index Rule

Whenever a statement says subarray, substring, subsequence, subset, prefix or suffix, restate its index rule in one line before looking at the examples.

- **Invariant** is that the answer satisfies the stated position rule exactly, and does not merely resemble a sample.
- **Typical failure** is a fast greedy that passes the samples but answers a larger search space than the one asked.

#### Confusing Substring With Subsequence

The false friend in this lesson is a pair of terms that look interchangeable but have different position rules. Here it is the pair of everyday words "substring" and "subsequence", which many people use interchangeably. The same goes for "subarray" and "subset". They are not interchangeable, even when a sample answer satisfies several definitions. Problem statements often choose samples that do.

#### Java Support For Contiguous Selections

Java supports the contiguous case only.

- **String.substring** returns a block.
- **Arrays.copyOfRange** returns a block and excludes its end index.
- **Subsequence** has no library call, so you code it as a scan.
- **"Contiguous" or "consecutive"** in a statement gives the subarray rule even without the word.

<!-- stage: exercises -->
### Exercises

#### [Build] Classify [2,4] (Author exercise)
<!-- id: pc-classify-2-4 -->

**Prerequisites.** The position rules for subarray, subsequence and subset in this lesson.

**Problem.** Let `nums` be an array of distinct integers, and let `cand` be a list of values taken from `nums`. Define three terms by the positions (0-based indexes) of the values of `cand` in `nums`. `cand` is a subarray if its values occupy consecutive positions in increasing order, each one greater by exactly 1 than the previous position. `cand` is a subsequence if its positions strictly increase, with gaps allowed. `cand` is a subset if every value of `cand` occurs in `nums`, in any order. For `nums = [1,2,3,4]` and `cand = [2,4]`, decide for each of the three terms whether it holds. Base every answer on the positions of the values, not on how the values look.

**Constraints.** `nums` holds distinct `int` values, so each value has exactly one position. Here `nums = [1,2,3,4]`, and every value of `cand` occurs in `nums`. `cand` is non-empty: the empty selection is out of scope. The answer is three boolean verdicts, one per term. Neither input changes.

**Example 1.** Input `nums = [1,2,3,4]` and candidate `[2,4]`, output not a subarray, yes a subsequence and yes a subset.

**Example 2.** Input `nums = [1,2,3,4]` and candidate `[2,3]`, output yes for all three, because positions 1 and 2 are consecutive.

**Hint.** Write down the position of each candidate value. Are the positions consecutive, merely increasing, or neither?

**Changed decision.** Basic case: a test on positions replaces an impression of similarity.

#### [Vary] Order Matters (Author exercise)
<!-- id: pc-order-matters -->

**Prerequisites.** The classification exercise above.

**Problem.** Use the definitions of subarray, subsequence and subset from the previous exercise. Let `nums = [1,2,3,4]` and `cand = [4,2]`. Decide for each of the three terms whether it holds. Then name the one decision that differs from the candidate `[2,4]`. That decision is whether the candidate must keep the relative order of the values in `nums`.

**Constraints.** `nums` holds distinct `int` values, and every value of `cand` occurs in `nums`. `cand` is non-empty. A subset is judged by membership alone and makes no promise about order. The answer is three boolean verdicts plus the name of the changed decision. Neither input changes.

**Example 1.** Input `nums = [1,2,3,4]` and candidate `[4,2]`, output not a subarray, not a subsequence, yes a subset.

**Example 2.** Input `nums = [1,2,3,4]` and candidate `[1,2,3,4]`, output yes for all three, since the candidate is the whole array.

**Hint.** What happens to the positions when you list 4 before 2? Which of the three rules cares about the direction of the positions?

**Changed decision.** The candidate's order flips, so the test moves from checking gaps to checking direction.

#### [Boundary] Empty Choice (Author exercise)
<!-- id: pc-empty-choice -->

**Prerequisites.** The two exercises above.

**Problem.** Given an array `nums`, a subarray is a contiguous run of positions, and its sum is the sum of its values. The empty subarray has no positions and has sum 0. Compute the maximum subarray sum of `nums = [-8,-3,-6]` under two specifications. In the first, the subarray must be non-empty. In the second, the empty subarray is allowed. Return both answers and state why they differ.

**Constraints.** `1 <= nums.length <= 10^5` and `-10^4 <= nums[i] <= 10^4`, with `nums[i]` of type `int`. A specification must say whether the empty subarray is legal, and you must not assume a convention. The maximum is a single `int`. If several subarrays reach it, the value is the same. `nums` does not change.

**Example 1.** Input `nums = [-8,-3,-6]` with a non-empty requirement, output -3, the best single reading.

**Example 2.** Input `nums = [-8,-3,-6]` with the empty choice allowed, output 0, the sum of choosing nothing.

**Hint.** What is the sum of an empty block, and does the specification say such a block counts? Which answer would an all-negative array expose if you guessed wrongly?

**Changed decision.** The legal set of candidates changes by one element, the empty selection. That one element flips the answer.

#### [Recognize] Contiguous Maximum (Author exercise)
<!-- id: pc-contiguous-maximum -->

**Prerequisites.** All three exercises above.

**Problem.** Given an array `nums`, a subarray is a contiguous run of positions. A subsequence is any selection of positions in increasing order, and gaps are allowed. Both must be non-empty here. For `nums = [5,-10,4]`, compute the maximum sum over all non-empty subarrays and the maximum sum over all non-empty subsequences. Explain why a subarray that contains both 5 and 4 must also contain -10, while a subsequence may skip it. The efficient algorithm for the contiguous case belongs to Chapter 01.

**Constraints.** `1 <= nums.length <= 20`, with `int` values. The size allows a brute force over every candidate. Each answer is a single `int`. `nums` does not change.

**Example 1.** Input `nums = [5,-10,4]` as a subarray question, output 5.

**Example 2.** Input `nums = [5,-10,4]` as a subsequence question, output 9, from positions 0 and 2.

**Hint.** Which blocks of consecutive positions contain both the 5 and the 4? What else do they contain?

**Changed decision.** The same data and the same sum objective give two answers because the position rule changes.
