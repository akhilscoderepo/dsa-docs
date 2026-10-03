<!-- section: orientation -->
## Orientation

This chapter teaches no algorithm. It teaches the language you use to read a problem before you pick one: what the limits allow, what the input promises, whether it may be changed, which positions an answer may use, how to count cost honestly, and which Java calls quietly change the count. Every later chapter assumes you can do these things without effort, and most wrong answers in interviews come from skipping them.

### What You Need Before Starting

You should be able to write a loop over an array in Java, read a simple Big-O bound, and run a small program to see its output. No data structure beyond arrays and strings appears here, and no lesson needs more than a few lines of code. The exercises are deliberately small, because the aim is to practice reading a contract, predicting a cost and designing a hostile test, one at a time, before any named algorithm competes for your attention.

### The Eight Habits

The lessons cover eight habits. Constraint signals turn the limits in a statement into a first filter on approaches. Mutation contracts separate the physical array from the logical answer and say what may be changed. Sequence language fixes the meaning of subarray, subsequence and subset by the positions they allow. Input guarantees separate what the caller promised from what your code assumes. Complexity tradeoffs count executions of the dominant statement and compare solutions that spend different resources. Amortized cost prices a sequence of operations whose expensive calls are rare. Hostile dry runs aim one tiny input at one failure mode. Java cost habits add the price and meaning of the library calls that live inside your loops.

### How To Work Through A Lesson

Read the short story and the first, plain version of the code, and try to predict what is wrong before you reach the next section. Step through the trace with the buttons, and in each lesson watch the hardest step, the one the text points out. Then do the four exercises in order without opening the hint, write your own answer in the notes box, and only then read the solution. Every solution has Java that runs with assertions during the build, so each numeric claim in the solutions was executed and not only written down.

### Leaving The Chapter

Before Chapter 01 you should be able to read a new prompt and state, in a few lines, the meaningful guarantees, whether mutation is allowed, which part of the output is valid, which sequence relationship is requested, the plausible time and space budget, one adversarial test, and any Java call that changes the claimed cost. The review section at the end checks exactly that with recognition questions you can retake after a few days.
