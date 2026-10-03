<!-- lesson-kind: standard -->
<!-- lesson-id: majority-vote -->
## Majority Vote

<!-- stage: context -->
### A Ballot Box Without A Tally Sheet

A village holds a vote with a single question, and the ballots arrive in a long stream, one name per ballot. The clerk wants to know whether any name was written on more than half of all ballots. There is no table to keep tallies on and the clerk can only hold two things in mind at once: one name and one small number.

A clever clerk invents a ritual. She keeps a name in mind and a count. A ballot matching the name raises the count, and a ballot with a different name lowers it. When the count would go below zero she drops the old name and adopts the one on the current ballot. When the box is empty, she holds a single name, and the surprising claim is that if any name had more than half the ballots, it must be that one.

<!-- stage: naive -->
### Count Every Name Against The Whole Box

The direct way to answer the question is to check each ballot's name by counting how many ballots carry it.

```java
static int majorityByCounting(int[] ballots) {
    for (int i = 0; i < ballots.length; i++) {
        int count = 0;
        for (int j = 0; j < ballots.length; j++) {
            if (ballots[j] == ballots[i]) count++;
        }
        if (2 * count > ballots.length) return ballots[i];
    }
    return -1;
}
```

It returns the name held by more than half the ballots, or `-1` if none. It is easy to trust, because it literally follows the definition.

<!-- stage: bottleneck -->
### A Full Recount For Every Ballot

For each ballot the method rescans the whole array, so the cost is `n * n`, which is O(n^2). With 50,000 ballots that is 2.5 billion comparisons. The extra space is O(1), so memory is not the problem, and the time is. Most of the effort repeats, since every copy of the same name triggers the same recount of the same number.

A sort fixes the repetition. After sorting, the majority name must occupy the middle position, so reading the middle gives a candidate in O(n log n) time, but that costs time and either mutates the input or needs a copy. A table of counts keyed by name is linear in time and costs memory proportional to the number of distinct names. The clerk's ritual needs neither the sort nor the table, which is what makes it worth understanding.

<!-- stage: insight -->
### Different Names Cancel In Pairs

Imagine pairing ballots with different names and tossing each pair out. A name that holds more than half the ballots cannot be eliminated by this process, because each tossed pair removes at most one ballot carrying that name, and there are not enough pairs to remove them all. Whatever remains after all possible pairs are tossed must consist of ballots with a single name, and the majority name, if it exists, must be that name.

The vote counter performs the pairing without storing anything. The held name is the **candidate**, and the count of unmatched ballots for it is the **votes**. A ballot with the same name adds a vote. A ballot with a different name cancels one vote, which is the pair being tossed. When the votes are zero, no unmatched ballots remain, so the next ballot starts a new candidate. This is **cancellation**, and the algorithm built on it is the Boyer-Moore majority vote.

<!-- names: candidate, votes, cancellation, verification pass -->

The invariant is that the ballots read so far consist of discarded pairs of distinct names plus exactly `votes` copies of the candidate. The proof of the claim follows. Suppose a name `m` appears more than `n / 2` times. Each discarded pair contains at most one copy of `m`, and there are at most `n / 2` pairs, so at least one copy of `m` survives, and the survivors all carry the candidate's name. Therefore the candidate is `m`.

The conclusion holds only when a majority exists. If nothing has a majority, the process still ends with some candidate, and nothing about it says the name is frequent. A **verification pass**, a second scan that counts the candidate, turns the candidate into an answer. If the problem guarantees a majority, the pass can be skipped, and otherwise it is mandatory.

<!-- stage: variables -->
### One Name And One Count

Keep `candidate`, the name currently held, and `votes`, the number of unmatched ballots for it. At the start `votes` is zero and `candidate` holds nothing meaningful. For each ballot, when `votes` is zero the ballot becomes the candidate with one vote, and otherwise the ballot either adds a vote when it matches or removes one when it does not. The verification pass uses one more counter, which counts occurrences of the final candidate.

<!-- stage: trace -->
### Two Boxes, Two Outcomes

First box: `[4, 4, 7, 4, 1, 4, 4]`. The first ballot makes 4 the candidate with one vote, and the second raises it to two. The 7 cancels one vote, leaving one. The next 4 restores two votes, and the 1 cancels one again. The last two 4s bring the votes to three. The survivor is 4, and a count confirms it holds five of seven ballots, which beats half.

Second box: `[1, 2, 3]`, where no name is a majority. The 1 becomes the candidate with one vote. The 2 cancels it, so the votes are zero. The 3 arrives with no votes held, so it becomes the new candidate with one vote. The ritual ends holding 3, a name with a single ballot out of three. Nothing in the process warned that the survivor is not a majority, and only the counting pass reveals it. That last step is the one to remember: the candidate is a suspect, and the verification pass is the trial.

```trace
{"cells":[4,4,7,4,1,4,4],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"candidate":4,"votes":1},"note":"Read 4. Votes were zero, so 4 becomes the candidate with one vote."},{"at":{"i":1},"vars":{"candidate":4,"votes":2},"note":"Read 4. It matches the candidate 4, so votes rise to 2."},{"at":{"i":2},"vars":{"candidate":4,"votes":1},"note":"Read 7. It differs from the candidate 4, so one pair cancels and votes fall to 1."},{"at":{"i":3},"vars":{"candidate":4,"votes":2},"note":"Read 4. It matches the candidate 4, so votes rise to 2."},{"at":{"i":4},"vars":{"candidate":4,"votes":1},"note":"Read 1. It differs from the candidate 4, so one pair cancels and votes fall to 1."},{"at":{"i":5},"vars":{"candidate":4,"votes":2},"note":"Read 4. It matches the candidate 4, so votes rise to 2."},{"at":{"i":6},"vars":{"candidate":4,"votes":3},"note":"Read 4. It matches the candidate 4, so votes rise to 3."}]}
```

```trace
{"cells":[1,2,3],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"candidate":1,"votes":1},"note":"Read 1. Votes were zero, so 1 becomes the candidate with one vote."},{"at":{"i":1},"vars":{"candidate":1,"votes":0},"note":"Read 2. It differs from the candidate 1, so one pair cancels and votes fall to 0."},{"at":{"i":2},"vars":{"candidate":3,"votes":1},"note":"Read 3. Votes were zero, so 3 becomes the candidate with one vote."}]}
```

<!-- stage: code -->
### The Vote With An Optional Check

```java
static int majorityGuaranteed(int[] ballots) {        // contract: a majority name exists
    int candidate = 0, votes = 0;
    for (int b : ballots) {
        if (votes == 0) candidate = b;
        votes += (b == candidate) ? 1 : -1;
    }
    return candidate;
}

static int majorityOrNone(int[] ballots) {            // contract: a majority may not exist
    int candidate = majorityGuaranteed(ballots);
    int count = 0;
    for (int b : ballots) if (b == candidate) count++;
    return 2L * count > ballots.length ? candidate : -1;
}
```

Both methods make one or two linear passes and keep a constant number of variables, so the time is linear and the extra space is constant. The first is correct only under its stated guarantee. The second adds the verification pass and compares `2 * count` with the length instead of dividing, which avoids a rounding mistake for odd lengths. The sentinel `-1` is acceptable only if ballot names can never be `-1`, so pick the signal from the contract.

<!-- stage: applicability -->
### When More Than Half Is The Question

Use the majority vote when one value may occur more than half the time and you must use constant extra space, or when you want one linear pass without a table. The invariant is that the elements read are discarded distinct pairs plus `votes` copies of the candidate, so a true majority cannot be cancelled away. If the problem does not guarantee that a majority exists, follow the pass with a verification count.

The false friend is the frequency map. A map counts every name and answers the same question with O(n) memory, and it generalizes to any frequency threshold, which the vote does not. The vote is also not ordinary counting, because the votes counter is not the number of occurrences of the candidate. It is the surplus of the candidate over the names that cancelled it. A related trap is to read the candidate as the most frequent value. When no majority exists, the survivor can be a rare name.

Java notes are small but real. Compare with `2L * count > n` and not with `count > n / 2`, which has an off-by-one for odd lengths when written carelessly. And a sentinel return such as `-1` must be a value the input cannot contain, otherwise an optional wrapper or an exception is the honest design.

<!-- stage: exercises -->
### Exercises

#### [Build] Majority Element (LeetCode 169)
<!-- id: ar-majority-element -->

**Prerequisites.** The candidate and votes ritual from this lesson; the aggregation lesson.

**Problem.** Given an array of size `n`, return the majority element, the value that appears more than `n / 2` times. The input guarantees that such an element always exists.

**Constraints.** 1 <= n <= 5 * 10^4 and -10^9 <= nums[i] <= 10^9. Use a single pass and a constant number of variables.

**Example 1.** Input `nums = [4, 4, 7, 4, 1, 4, 4]`, output 4.

**Example 2.** Input `nums = [3]`, output 3, since a single element is trivially a majority.

**Hint.** When a different value arrives, what happens to your held candidate's lead? What do you do when the lead reaches zero?

**Changed decision.** First rung: a two-variable cancellation replaces counting every value.

#### [Vary] Verify The Candidate (Author exercise)
<!-- id: ar-verify-candidate -->

**Prerequisites.** The majority-element exercise above.

**Problem.** Now no majority is guaranteed. Run the vote, then count the survivor in a second pass and return it only when it occurs more than `n / 2` times. Otherwise return `-1`.

**Constraints.** 0 <= n <= 5 * 10^4 and 0 <= nums[i] <= 10^9, so `-1` can never be a legal element. Use constant extra space.

**Example 1.** Input `nums = [5, 5, 2, 5, 3]`, output 5, which occurs three times out of five.

**Example 2.** Input `nums = [1, 2, 1, 2]`, output -1, because neither value exceeds half.

**Hint.** What does the vote guarantee when a majority exists, and what does it say when none does? What one extra pass settles it?

**Changed decision.** The guarantee is removed, so a verification pass becomes mandatory.

#### [Boundary] No Majority (Author exercise)
<!-- id: ar-no-majority -->

**Prerequisites.** The two exercises above.

**Problem.** Trace the vote on `[1, 2, 3]` and show that the survivor is not a majority, which is why verification is mandatory. Then trace `[1, 2]` and show how the votes cancel to zero. State what the survivor is in each case and what the count check returns.

**Constraints.** Use the standard rule: when the votes are zero, the current element becomes the candidate before it is compared. Arrays contain distinct small positive values.

**Example 1.** Input `nums = [1, 2, 3]`, output survivor 3 with a verified count of 1, so no majority.

**Example 2.** Input `nums = [1, 2]`, output survivor 1 with votes 0 after the pair cancels, and a verified count of 1, so no majority.

**Hint.** After a cancellation to zero, which element becomes the next candidate? What does the final votes value tell you about frequency, and what does it not tell you?

**Changed decision.** The tests target the guarantee itself, showing the ritual's output is meaningless without the count.

#### [Recognize] Dominant Product Id (Author exercise)
<!-- id: ar-dominant-product-id -->

**Prerequisites.** All three exercises above.

**Problem.** A stream of order lines each carries a product id. Decide whether any single id accounts for more than half of the lines, using constant extra space, and return that id or `-1` if none does. The stream is given as an array here.

**Constraints.** 0 <= lines.length <= 10^5 and 0 <= lines[i] <= 10^9. Do not use a table of counts.

**Example 1.** Input `lines = [204, 17, 204, 204, 9, 204]`, output 204, from four of six lines.

**Example 2.** Input `lines = [1, 2, 3, 4]`, output -1, since no id has more than two lines.

**Hint.** Is a majority guaranteed here? Which pass is therefore required, and why can a table of counts be avoided?

**Changed decision.** The same two-pass pattern appears in a business story with an unguaranteed majority.

#### [Extend] Majority Element II (LeetCode 229)
<!-- id: ar-majority-element-two -->

**Prerequisites.** All four exercises above.

**Problem.** Given an integer array, return all values that appear more than `n / 3` times. At most two such values can exist, so keep two candidates with two vote counters, and verify both with a second pass.

**Constraints.** 1 <= nums.length <= 5 * 10^4 and -10^9 <= nums[i] <= 10^9. Use constant extra space. The result may be in any order.

**Example 1.** Input `nums = [1, 1, 1, 3, 3, 2, 2, 2]`, output `[1, 2]`, since each appears three times and `n / 3` is 2.

**Example 2.** Input `nums = [5]`, output `[5]`, because one occurrence exceeds `1 / 3`.

**Hint.** If three different values cancel together as a triple, how many triples can there be, and how many copies of a value above `n / 3` must survive?

**Changed decision.** The threshold moves from one half to one third, so cancellation removes triples and two candidates are kept.
