<!-- section: orientation -->
## Orientation

This chapter teaches no algorithm. It teaches the vocabulary for reading a problem before you pick an approach. You learn what the input limits allow and what the input guarantees. You learn whether the code may change the input and which index positions an answer may use. You learn to count cost correctly and to spot Java calls that change how much work a loop does. Every later chapter assumes you do these things without effort. Most wrong answers in interviews come from skipping them.

### Prerequisites

You should be able to write a loop over an array in Java, read a simple Big-O bound, and run a small program to see its output. This chapter uses no data structure beyond arrays and strings. No lesson needs more than a few lines of code. The exercises stay small on purpose. Each one trains a single skill. In one exercise you read a problem statement and write down what the input guarantees and what the output must contain. In another you predict how many times a loop runs. In a third you write a small input that makes the code fail. You practice each skill alone, so no named algorithm distracts you.

### What The Eight Lessons Cover

The chapter has eight lessons. Each lesson trains one analysis skill.

- **Reading Input Limits Before Choosing An Algorithm** turns the limits in a problem statement into a first filter on approaches.
- **Whether A Method May Modify Its Input** separates the stored array from the returned answer and states what the code may change.
- **Subarrays, Subsequences And Subsets Compared** tells the three terms apart by the index positions each one allows.
- **Input Preconditions And Edge Cases** separates what the caller guarantees from what your code assumes.
- **Comparing Time And Space Complexity Trade-Offs** counts how often the statement that runs most often executes and compares solutions that use different resources.
- **Amortized Time Complexity** bounds the total cost of a sequence of calls in which expensive calls are rare.
- **Writing Edge-Case Tests** aims one small input at one kind of bug.
- **Time Complexity Of Common Java Methods** states the cost and meaning of the library calls inside your loops.

### How To Work Through Each Lesson

Work through each lesson in the same order.

The lesson starts with the context and the naive code. Read the short scenario and the first version of the code. Next comes the prediction, where you decide what is wrong before you reach the next section.

The trace follows, so step through it with the buttons and watch the step the text points out. After the trace, do the four exercises in order without opening the hint. Then write your own answer in the notes box before you read the solution.

The solution comes last, and every solution has Java that runs with assertions during the build. Finally, the build checks execute each numeric claim in the solutions, so no claim is only written down.

### What You Can Do After This Chapter

Before Chapter 01 you should be able to read a new prompt and state six things in a few lines.

- **Guarantees** are the input preconditions, and whether the code may modify the input.
- **Output** is what a correct answer must contain.
- **Sequence term** is the one the problem requests: subarray, subsequence or subset.
- **Complexity bounds** are the time and space limits that fit the input size.
- **Edge-case test** is one small input aimed at one kind of bug.
- **Library call** is any Java call that changes the claimed complexity.

The review section at the end checks these skills with recognition questions. You can retake them after a few days.
