<!-- section: orientation -->
## Orientation

A level meter lags on a ten-minute recording because every new sample rescans the last thousand samples. A dashboard keeps showing a latency spike that is an hour old. A fraud rule compares each payment with the best of the last five, and nobody can say why it drops the others. Each program stores recent items and needs the best one at once. This chapter shows how a deque answers that question in constant time per item, and why each of its two ends needs exactly one job.

### Prerequisites

You should know arrays, loops, the cost words from Chapter 00, and the idea of a window that moves along an array from Chapter 09. Prefix sums from Chapter 07 appear in the last lesson. Chapter 11 introduced `ArrayDeque`, and Chapter 12 showed how to remove weaker values from one end of a stack. Each lesson defines its own terms the first time they matter. Code samples assume `import java.util.*;` and a recent JDK.

### The Eight Lessons

Each lesson adds one rule about which end of the deque acts and when.

- **Use ArrayDeque From Both Ends** shows how a circular array gives constant-time calls at the front and the back, and what each call returns on an empty deque.
- **Give Each End One Job** keeps values in order so the front holds the best value and the back admits new ones.
- **Remove Weaker Values From The Back** explains why a newer, better value lets the deque drop older positions for good.
- **Remove Old Indices From The Front** tests the age of the front position before every read.
- **Find The Maximum Of Every Window** runs expiry, removal and append in one fixed order and reads the answer last.
- **Find The Minimum Of Every Window** flips one comparison and then lets the left end of the window move by a pointer.
- **Allow Only Recent Positions** reads the answer before the append, because a position must not see itself.
- **Find The Shortest Subarray With Negatives** stores prefix positions, and it removes a start from the front once that start has reached the target.

### The Combination Lesson

One lesson joins the deque lessons with the window lessons of Chapter 09.

- **Slide A Window With Two Deques** keeps the largest and the smallest value of a window up to date while its left end moves, and it counts every stretch that stays inside a limit.

### How To Work Through Each Lesson

Each lesson begins with a program that fails or slows down on a real input and then shows a plain version that works but costs too much. A prediction question follows, and you commit to an answer before the explanation opens. The remaining parts give the rule, the state, a step-by-step trace, the code and a check of when the method does not apply. The exercises climb from a basic version to a full interview problem. Each exercise has a role in brackets: Build, Vary, Boundary or Recognize. The line named Changed decision says what the exercise changes compared with the one before it.

### What You Can Do After This Chapter

You can name which end of a deque each step touches and what the call returns on an empty deque. You can explain why a removed position can never matter again, and you can run the steps in the right order for a window query. You can choose between one deque, two deques and a running total for a given question.

### What Later Chapters Reuse

Three ideas carry forward.

- **Expire before you read** returns whenever stored items stop counting after a distance or a boundary.
- **Store positions, not bare values** returns whenever equal values must expire at different times.
- **Fix the order of the steps** returns whenever a read, a removal and an append must not see each other's results.
