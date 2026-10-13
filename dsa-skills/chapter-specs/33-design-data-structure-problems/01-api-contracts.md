# Lesson spec: Write The Contract Before The Code

**Recognition cue.** Correctness spans a sequence of public calls rather than one function invocation. **Invariant.** Every operation states output, mutation, failure behavior, and promised complexity.

- **Build - Author exercise: Specify A Counter API.** Define legal calls and observable state.
- **Vary - Author exercise: Empty Removal Policy.** Choose exception, sentinel, or precondition consistently.
- **Boundary - Author exercise: Repeated Calls.** Trace state across duplicate inserts and removals.
- **Recognize - LC 155 Min Stack.** Express constant-time operation contracts before implementation.
