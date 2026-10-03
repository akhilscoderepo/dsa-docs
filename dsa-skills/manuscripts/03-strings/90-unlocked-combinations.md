<!-- section: unlocked-combinations -->
## Unlocked Combinations

This chapter introduces no teach-now combination. The arrays chapter already supplied one-pass state, compaction and counting on a single sequence, and strings are that sequence with characters as elements and an immutable wrapper around them. A combination is released only when every prerequisite has been taught, and the ones below still miss one.

### Deferred

Strings with hash maps are deferred to Chapter 04, which supplies arbitrary-key state. That is why this chapter counts only over a fixed lowercase alphabet with an array, and why grouping equal characters wherever they sit is left alone. Strings with two pointers are deferred to Chapter 08, which supplies opposite-end movement, so checking a whole string as a palindrome from both ends waits there. Strings with sliding windows are deferred to Chapter 09, which supplies moving-window state, so longest substring questions with a changing condition wait there. Nothing assigned in this chapter calls for those techniques.

### Already Covered

The write position from the arrays chapter returns as in-place compression of a character array, now driven by a pending run. The frequency array from the arrays chapter returns as the letter table, now indexed by a character minus `'a'`. Neither is a new combination, and each lesson names the earlier idea it builds on.
