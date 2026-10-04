<!-- section: orientation -->
## Orientation

A method reports the highest temperature of a cold week as 0, although every reading is below zero. The loop started its maximum at 0, and no reading ever beat it. A second method removes the zeros from a 50,000-element array by shifting the tail left after each zero, and it runs for seconds. Both bugs live in the loop state, not in the idea. This chapter answers one question: what should a single pass over an array remember, and how does it keep that memory correct at every index?

### Prerequisites

You should know Java array syntax, the `for` loop and the cost vocabulary of Chapter 00. The chapter uses no other data structure.

### What The Twelve Lessons Cover

Each lesson adds one loop pattern and the invariant that makes it correct.

- **Direct Scans** answers a question with one pass and a value that marks absence.
- **Aggregation** keeps a running count, sum, maximum or streak.
- **Running Extremum And Best Gain** pairs each position with the best earlier position.
- **Stable Compaction** moves kept values forward with a second index.
- **Sorted Deduplication** keeps one value from each run of equal values.
- **Frequency Arrays** uses small values as indexes into a count array.
- **Majority Vote** cancels unlike pairs to find the one value that outnumbers the rest.
- **Cyclic Placement** swaps each value into the cell that matches it.
- **In-Place Sign Marking** records visits by changing the sign of stored numbers.
- **Kadane State** tracks the best subarray sum that ends at each index.
- **Product State** tracks the largest and smallest products at once.
- **Circular Kadane** handles subarrays that wrap past the last index.

### How To Work Through Each Lesson

Every part of a lesson carries a label, so you always know where you are. A lesson opens with a short failing case, and then a prediction prompt asks you to guess the cause before the answer appears. After that, a trace lets you step through the loop and watch one variable change. Each lesson closes with four exercises that have a hidden hint and a hidden solution. Write your own attempt before opening either one.

### What You Can Do After This Chapter

You can choose the state a loop must carry, write the invariant that describes it, and check the invariant on the first index, a middle index and the last index. You can pick between a second index, a count array, a swap and a sign change when a method must run in O(n) time with little extra memory. You can also name the inputs that break each pattern, such as an empty array, all-negative values, a single element and heavy duplication.
