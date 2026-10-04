<!-- section: orientation -->
## Orientation

This chapter teaches no algorithm. It teaches the vocabulary for reading a problem before you pick an approach. You learn what the input limits allow and what the input guarantees. You learn whether the code may change the input and which index positions an answer may use. You learn to count cost correctly and to spot Java calls that change the operation count. Every later chapter assumes you do these things without effort. Most wrong answers in interviews come from skipping them.

### Prerequisites

You should be able to write a loop over an array in Java, read a simple Big-O bound, and run a small program to see its output. This chapter uses no data structure beyond arrays and strings. No lesson needs more than a few lines of code. The exercises stay small on purpose. Each one trains a single skill. In one exercise you read a problem statement and write down what the input guarantees and what the output must contain. In another you predict how many times a loop runs. In a third you write a small input that makes the code fail. You practice each skill alone, so no named algorithm distracts you.

### Chapter Scope And Lesson Overview

The chapter has eight lessons. Each lesson trains one analysis skill.

- **Analyzing Input Limits And Operation Budgets** converts the limits in a statement into a first filter on approaches.
- **Specifying Preconditions, Postconditions And Mutation** separates the physical array from the logical answer and states what the code may change.
- **Defining Subarrays, Subsequences And Subsets** distinguishes the three terms by the index positions each one allows.
- **Input Preconditions And Defensive Assumptions** separates what the caller guarantees from what your code assumes.
- **Comparing Time And Space Complexity Trade-Offs** counts executions of the dominant statement and compares solutions that use different resources.
- **Amortized Analysis Of Operation Sequences** bounds the total cost of a sequence in which expensive calls are rare.
- **Designing Adversarial Test Inputs** aims one small input at one failure mode.
- **Java Library Call Time And Space Costs** states the complexity and meaning of the library calls inside your loops.

### Procedure For Each Lesson

Work through each lesson in the same order.

- **Context and naive code** come first. Read the short scenario and the first version of the code.
- **Prediction** comes next. Decide what is wrong before you reach the next section.
- **Trace** follows. Step through it with the buttons and watch the step the text points out.
- **Exercises** come after the trace. Do the four exercises in order without opening the hint.
- **Notes box** holds your own answer. Write it before you read the solution.
- **Solution** comes last. Every solution has Java that runs with assertions during the build.
- **Build checks** execute each numeric claim in the solutions, so no claim is only written down.

### Chapter Completion Criteria

Before Chapter 01 you should be able to read a new prompt and state seven things in a few lines.

- **Guarantees** are the meaningful input preconditions, and whether mutation is allowed.
- **Output validity** is the part of the output that is valid.
- **Sequence relationship** is the one the problem requests: subarray, subsequence or subset.
- **Complexity bounds** are the plausible time and space limits for the input size.
- **Adversarial test** is one input that targets a failure mode.
- **Library cost** is any Java call that changes the claimed complexity.

The review section at the end checks these skills with recognition questions. You can retake them after a few days.
