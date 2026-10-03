# Lesson spec: Integer Answers

**Recognition cue.** The answer is an integer value in a numeric range, and feasibility is monotone. **Invariant.** Every discarded candidate is proved infeasible or no better than an already feasible boundary. **False friend.** Binary search applies to the ordered answer space, not because the input happens to be an array.

- **Build - LC 875 Koko Eating Bananas.** Search the minimum eating speed that finishes on time.
- **Vary - LC 1011 Capacity To Ship Packages Within D Days.** Change the feasibility simulation while retaining minimum-feasible search.
- **Boundary - LC 1482 Minimum Number of Days to Make m Bouquets.** Detect impossible total demand before searching.
- **Recognize - LC 410 Split Array Largest Sum.** Search a maximum allowed part sum and greedily count required partitions.
