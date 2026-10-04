<!-- section: orientation -->
## Orientation

A solution returns the right answer on every sample, then times out when the input holds 100,000 numbers. Another one passes the samples and then fails because it sorted the caller's array and moved every index. Neither bug is in the algorithm. Both come from facts in the problem statement that the author never read. This chapter answers one question: what must you know about a problem before you choose an approach?

### Prerequisites

You should be able to write a loop over an array in Java and read a simple Big-O bound. The chapter uses nothing beyond arrays and strings.

### What The Eight Lessons Cover

Each of the eight lessons trains one skill.

- **Reading Input Limits Before Choosing An Algorithm** turns the stated limits into a first filter on approaches.
- **Whether A Method May Modify Its Input** separates the stored array from the returned answer.
- **Subarrays, Subsequences And Subsets Compared** tells the three terms apart by the index positions they allow.
- **Input Preconditions And Edge Cases** separates what the caller guarantees from what your code assumes.
- **Comparing Time And Space Complexity Trade-Offs** counts how often the busiest statement runs.
- **Amortized Time Complexity** bounds the total cost of a call sequence in which expensive calls are rare.
- **Writing Edge-Case Tests** aims one small input at one kind of bug.
- **Time Complexity Of Common Java Methods** states the cost of the library calls inside your loops.

### How To Work Through Each Lesson

Every section of a lesson carries a part label, so you always know where you are. A lesson begins with a short scenario and a first version of the code, and then a prediction prompt asks you to decide what goes wrong before the explanation appears. Next, a walkthrough lets you step through the code and watch the moment the text points out. The lesson ends with four exercises, each with a hidden hint and a hidden solution. Try each exercise and write your own answer before you open either one.

### What You Can Do After This Chapter

After this chapter you can read a new prompt and state what the input guarantees, what a correct answer must contain, and which of subarray, subsequence or subset the problem asks for. You can pick time and space bounds that fit the input size and write one small test aimed at one kind of bug. You can also name the Java calls that change the cost of a loop.
