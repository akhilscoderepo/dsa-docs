# Lesson spec: Continuous Answers

**Recognition cue.** Feasibility is monotone over real values and the problem accepts bounded numeric error. **State.** Maintain a real interval containing the answer and a documented convergence policy. **Java hazard.** A fixed iteration count bounds work; an epsilon loop must still make progress under `double` precision.

- **Build - Author exercise: Square Root.** Approximate `sqrt(x)` within the stated absolute error.
- **Vary - Author exercise: Maximum Minimum Distance.** Search a real separation value under a monotone placement check.
- **Boundary - Author exercise: Scale-Aware Error.** Compare absolute and relative error for very small and very large answers.
- **Recognize - Author exercise: Fixed Iterations.** Explain why 80 bisections are a convergence policy, not a claim of universal maximal precision.
