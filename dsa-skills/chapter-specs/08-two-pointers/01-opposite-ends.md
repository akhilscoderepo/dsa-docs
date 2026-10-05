# Lesson spec: Scan From Both Ends

**Recognition cue.** Ordered input lets one comparison eliminate every pair using one endpoint. **Invariant.** Any valid pair not yet ruled out lies between `left` and `right`. **False friend.** Without order or another monotone property, moving an endpoint is a guess.

- **Build - LC 167 Two Sum II.** Move left when the sum is too small and right when it is too large.
- **Vary - Author exercise: Closest Pair Sum.** Preserve the best distance while the same elimination rule shrinks the interval.
- **Boundary - Author exercise: Two Values.** Trace one comparison with equal values and an absent target.
- **Recognize - LC 11 Container With Most Water.** Move the shorter wall because moving the taller wall cannot improve the limiting height.
