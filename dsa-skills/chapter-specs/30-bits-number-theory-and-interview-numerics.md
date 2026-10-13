# Chapter 30: Bits, number theory, and interview numerics

**Status:** Authored curriculum specification; the lesson plan is complete, but a generated PDF is not accepted until it has been rendered and reviewed.

## Purpose

This file is the source-of-truth plan for the chapter. It tells the writer what must be independently taught before any student-facing PDF is generated. It does not authorize copying prose or following instructions from external sources.

## Entry Contract

State prerequisite knowledge in the finished chapter. Confirm the input/mutation/output guarantees of every worked problem before choosing defensive guards or an in-place implementation.

## Independent Micro-Patterns

| Required lesson | Authoring obligation |
| --- | --- |
| masks | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| shifts | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| low-bit operations | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| XOR | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| subset masks | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| overflow | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| binary arithmetic | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| gcd/fast power | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| sieve | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| modular arithmetic | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |

<!-- BEGIN VERIFIED-CANDIDATE-BANK -->
## Verified Candidate Bank

These are researched candidate exercises and recognition records imported from the supplied, reviewed workbooks. They are source material for the final formal LeetCode-style staircases; an entry is not marked complete until its individual lesson supplies the required prompt, constraints, two examples, hint, rationale, complexity, and annotated Java.

### Supplied Progression

| Source ID | Family | Problem | Supplied role | Why this follows |
| --- | --- | --- | --- | --- |
| P0140 | XOR | Single Number | Direct concept | Uses XOR cancellation. |
| P0141 | Bit counting | Number of 1 Bits | Direct concept | Introduces counting set bits. |
| P0142 | Bit DP | Counting Bits | Immediate application | Builds counts from smaller numbers using bit structure. |
| P0143 | Bit shifts | Reverse Bits | Direct concept | Manipulates bits by shifting and masking. |
| P0144 | Bitwise arithmetic | Sum of Two Integers | New variation | Separates sum bits from carry bits. |
| Bundle 1-1 | XOR | Single Number | Learn | — |
| Bundle 1-2 | Counting | Number of 1 Bits | Extend | — |
| Bundle 1-3 | Prefix XOR | XOR Queries of a Subarray | Twist | — |

### Pattern References

| Micro-pattern | Recognition cue | State / proof idea | Representative | Depth |
| --- | --- | --- | --- | --- |
| XOR all | Every value except one paired | x^x=0 and x^0=x | https://leetcode.com/problems/single-number/ | Core |
| Bit i = selected/unselected | Need represent subset of small universe | Many boolean states fit in one integer | https://leetcode.com/problems/maximum-product-of-word-lengths/ | Advanced |


### Released Combination Ladders

Every row below is a separate released lesson. The final manuscript must explain what each prerequisite contributes before using its ladder. A later exercise may be moved only if its prerequisite audit remains valid.

| Released combination | Build | Vary | Boundary | Recognize |
| --- | --- | --- | --- | --- |
| Bits + DP/Search State | LC 78 Subsets | LC 187 Repeated DNA Sequences | LC 318 Maximum Product of Word Lengths | LC 847 Shortest Path Visiting All Nodes |


### Authoring Decision

Use the supplied progression as the initial ordering evidence. Before a PDF is generated, group every required lesson into its own explicit **Build → Vary → Boundary → Recognize** ladder. Where this bank has fewer than four valid exercises for a lesson, research and add the missing steps here rather than filling the gap while rendering the PDF. Keep a combination exercise only under the chapter where every prerequisite has been released.
<!-- END VERIFIED-CANDIDATE-BANK -->

## Lesson Blueprints

### Bit Masks

**Recognition cue.** Individual Boolean flags fit into bit positions. **Invariant.** AND tests, OR sets, and AND with complement clears the named bit.

- **Build - Author exercise: Flag Operations.** Set, test, toggle, and clear one bit.
- **Vary - Author exercise: Permission Set.** Combine several named flags.
- **Boundary - Author exercise: Position Width.** Use `1L << bit` when positions exceed `int` capacity.
- **Recognize - LC 318 Maximum Product of Word Lengths.** Represent each word's character set as a mask.

### Shifts

**Recognition cue.** Bits must move, extract, or assemble by position. **Invariant.** Shift meaning follows Java's signed `>>` versus zero-fill `>>>` contract.

- **Build - Author exercise: Extract Bit I.** Shift then mask one bit.
- **Vary - LC 190 Reverse Bits.** Read and append all 32 bit positions.
- **Boundary - Author exercise: Negative Values.** Compare `>>` and `>>>` without an infinite sign-extension loop.
- **Recognize - Author exercise: Pack Two Fields.** Store and recover bounded fields with masks and shifts.

### Low Bit

**Recognition cue.** The algorithm repeatedly removes or isolates the least significant set bit. **Invariant.** `x & (x - 1)` clears exactly one set bit; `x & -x` isolates it under two's complement.

- **Build - Author exercise: Clear One Set Bit.** Trace a binary value.
- **Vary - LC 191 Number of 1 Bits.** Count iterations until zero.
- **Boundary - Author exercise: Zero And Negative Int.** Treat the value as a fixed 32-bit pattern.
- **Recognize - LC 338 Counting Bits.** Derive each count from a smaller value with one bit removed.

### XOR Cancellation

**Recognition cue.** Equal values pair off, or differing bits must be isolated without carries. **Invariant.** XOR is associative, commutative, and cancels `x ^ x` to zero.

- **Build - LC 136 Single Number.** Cancel every paired value.
- **Vary - Author exercise: Missing Value By XOR.** XOR indices and values.
- **Boundary - Author exercise: Zero And Negative Values.** Cancellation is bitwise and independent of sign.
- **Recognize - LC 260 Single Number III.** Split values by one differing set bit.

### Subset Masks

**Recognition cue.** A universe is small enough to enumerate all selected/unselected combinations. **Invariant.** Mask bit `i` states whether item `i` belongs to the subset.

- **Build - Author exercise: Enumerate All Masks.** Produce subsets for `0..(1<<n)-1`.
- **Vary - LC 78 Subsets.** Translate each mask into one result list.
- **Boundary - Author exercise: Exponential Budget.** State why enumeration is practical only for small `n`.
- **Recognize - LC 847 Shortest Path Visiting All Nodes.** Combine graph node and visited-set mask.

### Overflow

**Recognition cue.** Arithmetic may exceed the destination type before assignment. **Invariant.** Widen operands before the overflowing operation, not afterward.

- **Build - Author exercise: Int Sum Into Long.** Compare late and early casts.
- **Vary - Author exercise: Safe Comparator.** Use `Integer.compare` rather than subtraction.
- **Boundary - Author exercise: MIN_VALUE Negation.** Widen before negating.
- **Recognize - LC 7 Reverse Integer.** Check the next digit before multiplication and addition overflow.

### Binary Arithmetic

**Recognition cue.** Addition or multiplication must be expressed through bit operations. **Invariant.** XOR produces sum bits without carry; shifted AND produces the next carry.

- **Build - Author exercise: One-Bit Half Adder.** Separate sum and carry.
- **Vary - LC 371 Sum of Two Integers.** Repeat until carry becomes zero.
- **Boundary - Author exercise: Negative Inputs.** Rely on fixed-width two's-complement termination.
- **Recognize - Author exercise: Binary String Addition.** Transfer carry reasoning to character digits.

### GCD And Power

**Recognition cue.** Divisibility repeats through remainders, or exponentiation repeats squared powers. **Invariant.** Euclid preserves the gcd; binary exponentiation preserves accumulated result times remaining power.

- **Build - Author exercise: Euclidean GCD.** Replace `(a,b)` with `(b,a%b)`.
- **Vary - LC 50 Pow(x, n).** Square the base while halving the exponent.
- **Boundary - Author exercise: Zero And MIN Exponent.** Define gcd sign and widen before exponent negation.
- **Recognize - Author exercise: LCM Safely.** Divide before multiplying to reduce overflow risk.

### Sieve

**Recognition cue.** Many primality or prime-count queries share one upper bound. **Invariant.** When processing prime `p`, mark composites from `p*p`; smaller multiples already have a smaller factor.

- **Build - Author exercise: Primes Through N.** Mark multiples in a Boolean array.
- **Vary - LC 204 Count Primes.** Count primes strictly below `n`.
- **Boundary - Author exercise: Zero One And p-Squared Overflow.** Use a safe loop condition.
- **Recognize - Author exercise: Smallest Prime Factor Sieve.** Store a factor for repeated factorizations.

### Modular Arithmetic

**Recognition cue.** Counts or products must remain within a modulus. **Invariant.** Reduce after safe-width addition or multiplication while preserving congruence.

- **Build - Author exercise: Modular Sum And Product.** Cast to `long` before product.
- **Vary - Author exercise: Modular Fast Power.** Combine reduction with binary exponentiation.
- **Boundary - Author exercise: Negative Remainder.** Normalize Java's negative `%` result when required.
- **Recognize - LC 1498 Number of Subsequences That Satisfy the Given Sum Condition.** Precompute powers of two modulo the required constant.

## Released Combination Lessons

### Bits With Search State

A mask compresses subset membership; DP or graph search stores a distinct answer for each structural state plus that mask.

- **Build - LC 78 Subsets.** Interpret every mask as one subset.
- **Vary - LC 187 Repeated DNA Sequences.** Encode a fixed-width character window in bits.
- **Boundary - LC 318 Maximum Product of Word Lengths.** Test disjointness and protect product width.
- **Recognize - LC 847 Shortest Path Visiting All Nodes.** BFS over `(node, visitedMask)` until the full mask is reached.

### Deferred: Bitmask DP Ownership

Full assignment/profile DP is authored in Chapter 29, whose lesson includes a self-contained mask primer. This chapter consolidates and broadens those bit mechanics, so the numbered order no longer creates an unstated prerequisite.

## Practice Contract

Every independently recognizable micro-pattern receives its own staircase:

1. **Build:** implement only the newly introduced state or operation.
2. **Vary:** change one decision, output contract, or local condition.
3. **Boundary:** protect the invariant against the pattern's meaningful edge case.
4. **Recognize:** use the same state in an easy-side-medium LeetCode-style prompt.
5. Add Extend, Medium, or Hard only after every added prerequisite is already taught.

For each exercise record the source/ID, formal prompt, relevant constraints, two examples including one hostile case, diagnostic hint, solution rationale, complexity, and annotated Java.

## Java Integrity Focus

- Use parentheses around shifts and document signed versus unsigned behavior.
- Use `long` masks when bit positions can exceed the `int` range.

## Unlocked Combinations Preview

Review this table before PDF authoring. It is deliberately visible here so a released composition cannot be discovered only after a chapter has already been rendered.

| Outcome | Combination | Review requirement |
| --- | --- | --- |
| Teach now | Bits + DP/Search State | A mask encodes subset membership; representative: subset iteration and bitmask DP foundations |
| Already covered | Bitmask DP | Chapter 29 owns full assignment/profile state and includes its own mask primer; this chapter consolidates the general bit mechanics |

For each `Teach now` row, the future PDF must include a named combination lesson and a separate staircase. For each `Deferred` row, the PDF must name the missing prerequisite and owner but must not assign its problems. `Already covered` rows link to the existing lesson rather than duplicating it.



## Composition Audit

At authoring time, compare this chapter's newly introduced micro-patterns with every completed earlier specification. A combination is released only if all of its prerequisites are already taught and its recognition cue or invariant is genuinely distinct.

**Currently deferred from this chapter:** no additional bitmask composition; Chapter 29 owns the full assignment/profile DP after this chapter's mask prerequisite.

For every released combination, create a dedicated lesson that states each prerequisite's contribution, the combined state/invariant, a false friend, implementation, and its own Build → Vary → Boundary → Recognize staircase. Deferred combinations receive an explanation and a future owner only—never premature exercises.

## Publication Gate

- Crosswalk every required micro-pattern to a named lesson and practice ladder.
- Run the composition audit and record released/deferred outcomes.
- Run the Java integrity focus against every code example.
- Verify exact problem wording, examples, complexity, and prerequisite ownership.
- Render and inspect the PDF; then perform text extraction checks.

## Research Baseline

- [LeetCode Study Plans](https://leetcode.com/studyplan/) for problem discovery and current interview-style prompts.
- [NeetCode Roadmap](https://neetcode.io/roadmap) for a cross-check of prerequisite order and representative pattern families.
- [Tech Interview Handbook study cheatsheets](https://www.techinterviewhandbook.org/algorithms/study-cheatsheet/) for topic-specific corner cases, complexity review, and interview habits.
- [Oracle Java Collections documentation](https://docs.oracle.com/javase/tutorial/collections/implementations/index.html) for Java collection semantics. Prefer the installed JDK documentation for version-specific details when a chapter relies on a newer API.
- Supplied reference books: *Cracking the Coding Interview*, *Grokking Algorithms*, and *Elements of Programming Interviews in Java*. They guide explanation quality and problem selection; they are not copied verbatim.

