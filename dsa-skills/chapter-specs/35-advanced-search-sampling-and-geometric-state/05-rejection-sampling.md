# Lesson spec: Rejection Sampling

**Recognition cue.** Uniform samples are easy in a bounding domain, and rejecting outside points leaves the desired uniform conditional distribution. **Invariant.** Every accepted point comes from the same uniform proposal density.

- **Build - Author exercise: Point In Unit Circle.** Sample a square and reject points outside the circle.
- **Vary - LC 478 Generate Random Point in a Circle.** Translate and scale accepted points.
- **Boundary - Author exercise: Boundary And Expected Trials.** State inclusion policy and analyze acceptance probability.
- **Recognize - LC 470 Implement Rand10() Using Rand7().** Reject biased overflow outcomes from a uniform larger range.
