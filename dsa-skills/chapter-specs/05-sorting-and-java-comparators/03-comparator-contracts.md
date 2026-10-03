# Lesson spec: Comparator Contracts

**Recognition cue.** Objects or boxed values require an order different from their natural order. **Invariant.** The comparator is antisymmetric, transitive, and returns zero only when elements are interchangeable for the required ordering.

- **Build - Author exercise: Safe Integer Comparator.** Use `Integer.compare` instead of subtraction.
- **Vary - Author exercise: Chained Keys.** Compare a primary field, then a deterministic secondary field.
- **Boundary - Author exercise: Equal Keys And Extreme Values.** Test comparator consistency and overflow safety.
- **Recognize - LC 179 Largest Number.** Order strings by `b+a` versus `a+b` to maximize concatenation.
