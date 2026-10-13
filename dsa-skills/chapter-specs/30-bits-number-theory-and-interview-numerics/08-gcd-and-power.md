# Lesson spec: GCD And Power

**Recognition cue.** Divisibility repeats through remainders, or exponentiation repeats squared powers. **Invariant.** Euclid preserves the gcd; binary exponentiation preserves accumulated result times remaining power.

- **Build - Author exercise: Euclidean GCD.** Replace `(a,b)` with `(b,a%b)`.
- **Vary - LC 50 Pow(x, n).** Square the base while halving the exponent.
- **Boundary - Author exercise: Zero And MIN Exponent.** Define gcd sign and widen before exponent negation.
- **Recognize - Author exercise: LCM Safely.** Divide before multiplying to reduce overflow risk.
