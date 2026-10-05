# Lesson spec: Count Exactly K By Subtraction

**Recognition cue.** The task counts subarrays with exactly `k` occurrences or categories, while an at-most condition is monotone and easy to count. **Invariant.** `exactly(k) = atMost(k) - atMost(k - 1)` partitions all subarrays by property count. **False friend.** A direct exactly-`k` window does not usually give one stable boundary because removing a redundant left value can preserve exactness.

- **Build - Author exercise: Exactly One Odd Number.** Compute `atMost(1) - atMost(0)`.
- **Vary - LC 1248 Count Number of Nice Subarrays.** Count subarrays containing exactly `k` odd values.
- **Boundary - Author exercise: Empty At-Most Budget.** Define `atMost(-1)` as zero so the subtraction remains safe.
- **Recognize - LC 992 Subarrays with K Different Integers.** Apply the identity to distinct-value counts maintained by a map.
