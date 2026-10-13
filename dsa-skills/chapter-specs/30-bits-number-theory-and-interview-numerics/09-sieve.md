# Lesson spec: Sieve

**Recognition cue.** Many primality or prime-count queries share one upper bound. **Invariant.** When processing prime `p`, mark composites from `p*p`; smaller multiples already have a smaller factor.

- **Build - Author exercise: Primes Through N.** Mark multiples in a Boolean array.
- **Vary - LC 204 Count Primes.** Count primes strictly below `n`.
- **Boundary - Author exercise: p-Squared Overflow.** Use a safe loop condition.
- **Recognize - Author exercise: Smallest Prime Factor Sieve.** Store a factor for repeated factorizations.
