# Lesson spec: Randomized Evolution

**Recognition cue.** Public calls mutate a collection and later return randomized output. **Invariant.** Each valid arrangement or element has the promised probability under the current state.

- **Build - Author exercise: Fisher-Yates One Step.** Choose uniformly from the remaining suffix.
- **Vary - LC 384 Shuffle an Array.** Produce a uniform permutation and preserve reset state.
- **Boundary - Author exercise: Repeated Reset And Shuffle.** Avoid aliasing the original array.
- **Recognize - Author exercise: Streaming Sample Review.** Connect evolving state to Chapter 35 reservoir sampling.
