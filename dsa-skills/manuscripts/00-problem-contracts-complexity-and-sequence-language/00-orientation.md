<!-- section: orientation -->
## Orientation

This chapter teaches no algorithm. It teaches the language you use to read a problem before you pick an approach. You learn what the limits allow and what the input promises. You learn whether the code may change the input and which positions an answer may use. You learn to count cost honestly and to spot Java calls that quietly change the count. Every later chapter assumes you do these things without effort. Most wrong answers in interviews come from skipping them.

### What You Need Before Starting

You should be able to write a loop over an array in Java, read a simple Big-O bound, and run a small program to see its output. This chapter uses no data structure beyond arrays and strings, and no lesson needs more than a few lines of code. The exercises stay small on purpose. Each one trains a single skill. In one exercise you read a problem statement and write down what the input guarantees and what the output must contain. In another you predict how many times a loop runs. In a third you write a tiny input that makes the code fail. You practice each skill alone, so no named algorithm distracts you.

### The Eight Habits

The lessons cover eight habits. Constraint signals turn the limits in a statement into a first filter on approaches. Mutation contracts separate the physical array from the logical answer and say what the code may change. Sequence language defines subarray, subsequence and subset by the positions each one allows. Input guarantees separate what the caller promised from what your code assumes. Complexity tradeoffs count executions of the dominant statement and compare solutions that spend different resources. Amortized cost prices a sequence of operations in which expensive calls are rare. Hostile Dry Runs, which covers adversarial testing, aims one tiny input at one failure mode. Java cost habits cover the price and meaning of the library calls inside your loops.

### How To Work Through A Lesson

Read the short story and the first, plain version of the code. Predict what is wrong before you reach the next section. Step through the trace with the buttons. In each lesson, watch the hardest step, the one the text points out. Then do the four exercises in order without opening the hint. Write your own answer in the notes box, and only then read the solution. Every solution has Java that runs with assertions during the build. The build executes each numeric claim in the solutions, so none is only written down.

### Leaving The Chapter

Before Chapter 01 you should be able to read a new prompt and state seven things in a few lines. State the meaningful guarantees and whether mutation is allowed. State which part of the output is valid and which sequence relationship the problem requests. State the plausible time and space budget, one adversarial test, and any Java call that changes the claimed cost. The review section at the end checks exactly that with recognition questions. You can retake them after a few days.
