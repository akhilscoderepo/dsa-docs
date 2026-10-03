# Exercise and solution records

## Exercise record

```
#### [Role] Title (LeetCode N)        or        #### [Role] Title (Author exercise)
<!-- id: permanent-slug -->

**Prerequisites.** What the learner must already know, with chapter references.

**Problem.** A complete statement in your own words: input, output, and what to return.

**Constraints.** Real limits and the target time and space.

**Example 1.** Input `...`, output `...`, with one sentence of why.

**Example 2.** A hostile case: boundary, empty, duplicate, extreme, or the trap this exercise targets.

**Hint.** A question that points at the decision without giving the answer. Two or more sentences are fine.

**Changed decision.** The one thing that differs from the previous rung of the ladder.
```

Roles, in ladder order: Build, Vary, Boundary, Recognize, then optionally Extend, Medium, Hard, Challenge. A lesson has at least one each of Build, Vary, Boundary and Recognize, between 4 and 7 exercises, and roles never go backward.

The `id` line sits directly under the heading. It is lowercase letters, digits and hyphens, unique across the chapter, and permanent: the learner's notes and status are stored under it, so a title can be edited freely but an id must never change. The matching solution record carries the same id.

Rules the audit enforces: every field above is present, the title ends with the source tag, each example states an input and an output, and no field is a stub (minimum words: Problem 15, Constraints 5, Hint 8, Changed decision 6, examples 3, Prerequisites 3).

## Rules for the content

- Author exercises are real problems with real constraints, not titles. If the spec only gives a title and a one-line goal, invent a specific, small, checkable task and a hostile second example.
- LeetCode exercises: restate the problem in your own words, give the actual constraints, and use examples you computed yourself, not the ones on the problem page. If you are not certain of the constraints, search to verify them. Never paste the original statement or its examples. When a combination lesson revisits a problem from earlier in the chapter, change the contract (a wider alphabet, a boundary report, a stricter complexity target) so that it is a new task and not a duplicate.
- The Build rung uses only this lesson's technique. Later rungs may use earlier lessons but never a technique that has not been taught yet.
- Each example's output must be correct. Compute it by running a brute-force program, not by hand, and keep example values inside the stated constraints.
- Never place the same sentence under more than one exercise.

## Solution record (in `solutions/<lesson file>`)

````
#### Solution: [Role] Title (LeetCode N)

**Approach.** The reasoning in two to five sentences, tied back to the lesson's invariant.

**Complexity.** Time and space, with the reason.

```java run
public final class Name {
    static int solve(...) { ... }
    public static void main(String[] args) {
        if (solve(...) != ...) throw new AssertionError("example 1");
        if (solve(...) != ...) throw new AssertionError("example 2");
    }
}
```
````

The heading after `Solution:` must match the exercise heading exactly, and the `<!-- id: -->` line under it must match the exercise's id. Where a cheap brute force exists, add a randomized cross-check to `main` (a few thousand small random inputs, a fixed seed); it catches wrong solutions and wrong claims that the two examples do not. Use `java run` with a `main` that checks both examples. The audit compiles the block and runs it with assertions enabled.
