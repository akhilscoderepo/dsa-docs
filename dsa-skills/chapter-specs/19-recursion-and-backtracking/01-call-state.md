# Lesson spec: Shrink The Problem With Each Call

**Recognition cue.** A problem decomposes into smaller instances described by a few parameters. **Invariant.** Each call has a precise subproblem contract and moves toward a base case. **False friend.** Recursion without shrinking state merely relocates an infinite loop to the call stack.

- **Build - Author exercise: Sum A Prefix.** Define the subproblem and base case before the recursive step.
- **Vary - LC 50 Pow(x, n).** Halve the exponent and reuse the squared half-result.
- **Boundary - Author exercise: Zero And Negative Exponents.** Handle `Integer.MIN_VALUE` by widening before negation.
- **Recognize - Author exercise: Recursive String Reversal By Range.** Recur on a strictly smaller interval without allocating slices.
