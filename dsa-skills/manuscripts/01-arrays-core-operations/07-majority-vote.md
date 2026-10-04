<!-- lesson-kind: standard -->
<!-- lesson-id: majority-vote -->
## Majority Vote

<!-- stage: context -->
### Finding The Value Behind Half The Records

A billing service receives a batch of ten million order lines. Each line carries a product id. The team wants to know whether one product accounts for more than half of the batch. The service runs on a small worker with a strict memory limit, so it cannot store a table with one entry for each distinct product id. The usual answer, a map from id to count, needs memory that grows with the number of distinct ids.

The question has a special shape. The team does not ask for the frequency of every id. It asks about one value that may occupy more than half of all positions, and such a value is called a **majority element**. An array of `n` elements has a majority element only when some value occurs more than `n / 2` times. At most one value can satisfy that condition. This lesson shows how to find the only possible holder of that role with one pass and a fixed amount of memory.

<!-- stage: naive -->
### Counting Every Value With A Map

The direct method counts how often each value occurs. It stores one counter per distinct value in a `HashMap`, then returns the value whose counter exceeds `n / 2`.

```java
static int majorityByMap(int[] nums) {
    java.util.Map<Integer, Integer> counts = new java.util.HashMap<>();
    for (int v : nums) {
        counts.merge(v, 1, Integer::sum);
        if (counts.get(v) > nums.length / 2) return v;
    }
    return -1;
}
```

This method is correct for every input. It reads each element once and updates one counter, so the time is O(n). The map holds one entry for each distinct value, so the extra space is O(n) in the worst case. A batch with millions of distinct ids needs millions of entries. A different direct method sorts a copy and reads the middle element, which takes O(n log n) time and still needs O(n) space for the copy.

<!-- stage: bottleneck -->
### Storing Counts That Only One Value Needs

```predict
A batch has 1,000,000 elements and a map counter for each of its distinct values. Suppose one value occupies 600,000 positions. How many of the map counters are needed to decide who holds more than half?

At most one counter matters, the one for the value that holds more than half. All other counters describe values that cannot exceed half of the batch once that value does, so the map keeps almost all of its entries for nothing.
```

The map spends memory on every distinct value, but the question concerns at most one of them. Two values cannot both occur more than `n / 2` times, because their counts would add up to more than `n`. Therefore the work of tracking all the other values is repeated effort that never changes the answer. The memory cost is O(k) for `k` distinct values, which reaches O(n) when most values differ. Sorting also does not remove the cost, since it needs a copy of the data and an O(n log n) step.

The task needs a method that keeps a fixed number of variables and still cannot lose a true majority. The next stage shows what such a method must preserve.

<!-- stage: insight -->
### Pairing Different Values To Remove Them

#### Discard Pairs Of Different Values

Take any two elements with different values and remove both from the array. A majority element can lose at most one occurrence in this step, because the removed pair holds at most one copy of it. The array shrinks by two elements, and the majority value loses at most one. Before the step, it occurred more than half the time. After the step, it still occurs more than half the time. Repeating the step keeps that property until only equal values remain, and those equal values must be the majority element.

#### Track One Survivor Of The Pairing

The scan performs this pairing without storing the removed elements. It keeps one **candidate**, the value that currently has unpaired copies, and a count of those copies. When the next element differs from the candidate, one copy of the candidate and the new element form a pair that is discarded. This event is a **cancellation**. When the next element equals the candidate, it joins the unpaired copies, and the count grows by one. When the count is zero, no unpaired copies remain, so the next element becomes the new candidate.

<!-- names: candidate, cancellation, verification pass -->

#### Confirm The Survivor With A Second Count

The scan guarantees only one direction. If a majority element exists, it is the candidate at the end. If no majority exists, the scan still ends with some candidate, and that value may occur only once. A **verification pass** counts the candidate in a second loop over the array and accepts it only when its count is greater than `n / 2`. The pass is required unless the problem promises that a majority element exists. Both loops together still take O(n) time and O(1) extra space.

<!-- stage: variables -->
### Meaning Of The Two Running Variables

The scan keeps two variables, and each has a precise meaning at every index.

- **`candidate`** is the value that owns the unpaired copies in the prefix read so far, and it changes only when `votes` is zero.
- **`votes`** is the number of unpaired copies of `candidate` in that prefix, and it is never negative.

When `nums[i]` equals `candidate`, `votes` grows by one. When `nums[i]` differs, `votes` shrinks by one, which is one cancellation. When `votes` is zero before reading `nums[i]`, the element replaces `candidate` and `votes` becomes one. The value in `votes` is a bound on unpaired copies. It is not the number of times the candidate occurs in the array, and a later stage uses a separate counter for that number.

<!-- stage: trace -->
### Tracing A Majority And A Missing Majority

The first trace reads `[3, 1, 3, 2, 3, 3, 1]`, where the value 3 occurs four times out of seven. At index 0 the votes are zero, so 3 becomes the candidate with one vote. The value 1 at index 1 differs, so it cancels one vote and `votes` drops to zero. At index 2 the votes are zero again, so 3 returns as the candidate. The value 2 cancels it, the next 3 restores it, and the following 3 raises the votes to two. The last element is 1, which cancels one vote and leaves 3 with one vote. The scan ends with candidate 3, and the second count finds four copies, which is more than three.

```trace
{"cells":[3,1,3,2,3,3,1],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"candidate":3,"votes":1},"note":"The votes are zero, so 3 becomes the candidate with one vote."},{"at":{"i":1},"vars":{"candidate":3,"votes":0},"note":"1 differs from the candidate 3, so one cancellation leaves 0 votes."},{"at":{"i":2},"vars":{"candidate":3,"votes":1},"note":"The votes are zero, so 3 becomes the candidate with one vote."},{"at":{"i":3},"vars":{"candidate":3,"votes":0},"note":"2 differs from the candidate 3, so one cancellation leaves 0 votes."},{"at":{"i":4},"vars":{"candidate":3,"votes":1},"note":"The votes are zero, so 3 becomes the candidate with one vote."},{"at":{"i":5},"vars":{"candidate":3,"votes":2},"note":"3 equals the candidate, so the votes grow to 2."},{"at":{"i":6},"vars":{"candidate":3,"votes":1},"note":"1 differs from the candidate 3, so one cancellation leaves 1 votes."},{"at":{"i":7},"vars":{"candidate":3,"votes":1,"occurrences":4},"note":"The scan ends with candidate 3. The second count finds 4 occurrences, which is more than 3."}]}
```

The second trace reads `[4, 5, 6]`, where every value is different. The candidate is 4, then 5 cancels it, then the zero votes make 6 the candidate. The scan ends with candidate 6 and one vote, but the value 6 occurs once out of three elements. The hardest step is the last one. It shows that the survivor of the scan is only a candidate until the verification pass counts it.

```trace
{"cells":[4,5,6],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"candidate":4,"votes":1},"note":"The votes are zero, so 4 becomes the candidate with one vote."},{"at":{"i":1},"vars":{"candidate":4,"votes":0},"note":"5 differs from the candidate 4, so one cancellation leaves 0 votes."},{"at":{"i":2},"vars":{"candidate":6,"votes":1},"note":"The votes are zero, so 6 becomes the candidate with one vote."},{"at":{"i":3},"vars":{"candidate":6,"votes":1,"occurrences":1},"note":"The scan ends with candidate 6. The second count finds 1 occurrences, which is not more than 1."}]}
```

<!-- stage: code -->
### Write The Scan And The Second Count

```java
static int majorityCandidate(int[] nums) {
    int candidate = nums[0];
    int votes = 0;
    for (int v : nums) {
        if (votes == 0) candidate = v;   // no unpaired copies, so v starts a new group
        votes += (v == candidate) ? 1 : -1;
    }
    return candidate;
}

static int majorityOrMinusOne(int[] nums) {
    int candidate = majorityCandidate(nums);
    int occurrences = 0;
    for (int v : nums) if (v == candidate) occurrences++;
    return occurrences > nums.length / 2 ? candidate : -1;
}
```

The method `majorityCandidate` replaces the candidate whenever the votes are zero, and then the same line of arithmetic handles equal and different values. The method `majorityOrMinusOne` adds the second loop. Both loops read the array once each, so the time is O(n) and the extra space is O(1). The comparison `v == candidate` is correct for `int` values. For boxed `Integer` or `String` values it compares object references, so use `equals` there.

<!-- stage: applicability -->
### Check The Majority Condition Before Using It

#### Conditions That Allow The Method

Use this scan when the question asks about a value that occurs more than half the time, and when memory must stay constant.

- **Invariant** is that the unpaired copies in the prefix all equal `candidate`, and every discarded pair holds one value that differs from the other.
- **Precondition** is a strict majority, meaning more than `n / 2` occurrences, and not merely the most frequent value.
- **Verification** is mandatory when the input does not promise a majority.
- **Streams** work when the data can be read twice, since the second count needs a second reading.

#### False Friends And No-Go Cases

A frequency count is a false friend, because it looks like the same task but asks a different question. It answers how often each value occurs, and the vote scan cannot answer that. The scan also does not find the most frequent value when no value passes `n / 2`, because the survivor may be rare. Reading the middle element of a sorted copy looks like another shortcut, but it needs the sort. The threshold `n / 3` or any other fraction needs more than one candidate, so a single `candidate` and `votes` pair is not enough there.

Do not use the scan when the data can be read only once and the contract gives no promised majority, because the confirming count then has nothing to read.

<!-- stage: exercises -->
### Exercises

#### [Build] Majority Element (LeetCode 169)
<!-- id: ar-majority-element -->

**Prerequisites.** The vote scan with `candidate` and `votes` from this lesson.

**Problem.** Given an integer array `nums`, return the majority element, which is the value that occurs more than `n / 2` times, where `n = nums.length`. The input guarantees that such a value exists.

**Constraints.** The limits are:
- **`nums`** is an `int[]` with `1 <= n <= 5 * 10^4`.
- **Values** are any `int` values.
- **Majority** exists in every input, so no verification is needed.
- **Mutation** of `nums` is not allowed.
- **Extra space** is O(1).

**Example 1.** Input `[5, 5, 8, 8, 5]`, output 5, because 5 occurs three times out of five.

**Example 2.** Input `[7]`, output 7, because a single element is its own majority.

**Hint.** What does `votes` hold after each element, and why does a value that is more than half of the array survive every cancellation?

**Changed decision.** Baseline case: replace the map of counts with one `candidate` and one `votes`.

#### [Vary] Verify The Candidate (Author exercise)
<!-- id: ar-verify-candidate -->

**Prerequisites.** The Majority Element exercise above.

**Problem.** Given an integer array `nums`, return the value that occurs more than `n / 2` times, where `n = nums.length`. Return `-1` when no value occurs that often.

**Constraints.** The limits are:
- **`nums`** is an `int[]` with `1 <= n <= 5 * 10^4`.
- **Values** are `int` values in the range `0` to `10^9`, so `-1` never collides with a real answer.
- **Majority** may not exist.
- **Mutation** of `nums` is not allowed.
- **Extra space** is O(1).

**Example 1.** Input `[9, 4, 9, 9, 2]`, output 9, because 9 occurs three times out of five.

**Example 2.** Input `[9, 4, 9, 4]`, output -1, because the best value occurs two times and `n / 2` is 2.

**Hint.** After the scan ends, how can you tell whether the survivor is a true majority?

**Changed decision.** The majority is no longer promised, so the output contract adds a verification pass and a failure value.

#### [Boundary] No Majority (Author exercise)
<!-- id: ar-no-majority -->

**Prerequisites.** The two exercises above.

**Problem.** Given an integer array `nums`, run the vote scan from this lesson. Replace the candidate with the current element whenever `votes` is zero before the element is read. Return an `int[]` that holds the final candidate, the final `votes` and the number of times the candidate occurs in `nums`.

**Constraints.** The limits are:
- **`nums`** is an `int[]` with `1 <= n <= 1000`.
- **Values** are `int` values in the range `0` to `100`.
- **Result** has length three, in the order candidate, votes, occurrences.
- **Mutation** of `nums` is not allowed.

**Example 1.** Input `[1, 2, 3]`, output `[3, 1, 1]`, because the survivor 3 occurs once and is not a majority of three elements.

**Example 2.** Input `[1, 2]`, output `[1, 0, 1]`, because the two elements cancel and the votes end at zero.

**Hint.** If the final `votes` is zero, can the candidate still be a majority?

**Changed decision.** The tests target arrays without a majority, so the survivor and its true count disagree with the claim that it dominates.

#### [Recognize] Dominant Product Id (Author exercise)
<!-- id: ar-dominant-product-id -->

**Prerequisites.** The Verify The Candidate exercise above.

**Problem.** Each element of the array `lines` is the product id of one order line, and ids are non-empty strings. Return the id that appears in more than half of the lines. Return `null` when no id does.

**Constraints.** The limits are:
- **`lines`** is a `String[]` with `1 <= n <= 10^5` and no `null` elements.
- **Ids** are non-empty strings of at most 12 lowercase letters or digits.
- **Comparison** uses string equality and not reference identity.
- **Mutation** of `lines` is not allowed, and the array may be read twice.
- **Extra space** is O(1).

**Example 1.** Input `["a7", "k2", "a7", "a7", "m5"]`, output `"a7"`, because it occurs three times out of five.

**Example 2.** Input `["a7", "k2", "k2", "a7"]`, output `null`, because the best id occurs two times and `n / 2` is 2.

**Hint.** Which cue in the statement asks for one value that holds more than half, and which operator compares two strings correctly?

**Changed decision.** The values are objects, so the same scan needs `equals`, and a memory limit rules out a map from ids to counts.

#### [Extend] Majority Element II (LeetCode 229)
<!-- id: ar-majority-element-ii -->

**Prerequisites.** The Verify The Candidate exercise above.

**Problem.** Given an integer array `nums` with `n` elements, return every value that occurs more than `n / 3` times, using integer division. Return the values in ascending order. Return an empty list when no value qualifies.

**Constraints.** The limits are:
- **`nums`** is an `int[]` with `1 <= n <= 5 * 10^4`.
- **Values** are any `int` values.
- **Result** holds at most two entries, since a third entry would push the total above `n` elements.
- **Mutation** of `nums` is not allowed.
- **Extra space** is O(1) apart from the result list.

**Example 1.** Input `[4, 4, 4, 1, 2, 2, 2, 7]`, output `[2, 4]`, because `n / 3` is 2 and both 4 and 2 occur three times.

**Example 2.** Input `[1, 2, 3, 4]`, output `[]`, because `n / 3` is 1 and every value occurs once.

**Hint.** If a cancellation now removes one copy each of three distinct numbers, how many candidates and how many vote counters does the scan need, and what must you do before you return them?

**Changed decision.** The threshold falls from one half to one third, so the scan keeps two candidates with two vote counters and always verifies both.
