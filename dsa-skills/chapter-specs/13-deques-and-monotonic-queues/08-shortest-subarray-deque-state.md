# Lesson spec: Shortest-Subarray Deque State

**Recognition cue.** Negative values prevent an ordinary sum window, but prefix sums let the task ask for the shortest pair of indices whose difference is at least `k`. **Invariant.** Prefix-sum indices increase from front to back and their prefix values also strictly increase; the front supplies the earliest profitable start. **False friend.** A standard positive-number sliding window fails when extending can decrease the sum.

- **Build - Author exercise: Prefix-Pair Difference.** Given prefix sums, compute a subarray sum as `prefix[right] - prefix[left]`.
- **Vary - Author exercise: Remove Dominated Prefixes.** Discard a later-or-equal prefix value because the newer index is never a better start.
- **Boundary - Author exercise: Negative Values And Long Sums.** Use `long` prefix sums and trace a case where the window sum falls after expansion.
- **Recognize - LC 862 Shortest Subarray with Sum at Least K.** Pop valid starts from the front and dominated prefixes from the back.
