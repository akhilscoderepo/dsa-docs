# Lesson spec: Amortized Cost

**Recognition cue.** An operation is usually cheap but occasionally performs a large repair or resize whose cost is spread across many earlier/later operations. **State.** Track stored “credit” or a potential such as unused capacity. **Invariant.** Across a sequence of operations, the total charged cost pays for every actual operation. **False friend.** Amortized `O(1)` is not worst-case `O(1)` for each individual call.

- **Build - Author exercise: Doubling Array.** Start with capacity 1 and append eight values, doubling whenever full. List capacities `1,2,4,8` and count all element copies. Observe that the total copies remain proportional to the number of appends.
- **Vary - Author exercise: Grow By One.** Repeat the experiment when capacity increases by exactly one. Sum `1 + 2 + ... + (n-1)` and explain why append becomes `O(n)` amortized rather than `O(1)`.
- **Boundary - Author exercise: One Expensive Append.** Identify the append that triggers an `O(n)` copy and reconcile it with an `O(1)` amortized bound over the whole sequence.
- **Recognize - Author exercise: Potential Intuition.** Treat unused slots after doubling as prepaid capacity. Explain, without formal algebra, how this stored potential funds future cheap appends and the next resize.
