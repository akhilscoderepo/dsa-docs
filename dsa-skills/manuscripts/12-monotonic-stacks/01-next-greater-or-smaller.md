<!-- lesson-kind: standard -->
<!-- lesson-id: next-greater-or-smaller -->
## Next Greater Or Smaller

<!-- stage: context -->
### Who Blocks Your View

A choir stands in one long row facing the audience, and every singer wants to know the first person somewhere behind them who is taller. That person is the one who will hide them from the camera at the back of the hall. Some singers will never be hidden, because nobody behind them is taller, and for them the answer is "no one".

A stage manager walks down the row once, from the front to the back, holding a clipboard. On it she writes the names of singers who have not yet met a taller person, in the order they were met. Whenever she reaches a new singer, she looks at the last name on her list. If the newcomer is taller, that singer's question is answered, and she crosses the name off and looks at the new last name. She repeats this until the newcomer is no taller than the last name, and then she writes the newcomer at the bottom. She never walks back along the row.

<!-- stage: naive -->
### Look Ahead From Every Singer

The direct method takes each singer in turn and walks forward along the row until it finds a taller person.

```java
static int[] nextGreaterByScan(int[] heights) {
    int n = heights.length;
    int[] answer = new int[n];
    for (int i = 0; i < n; i++) {
        answer[i] = -1;
        for (int j = i + 1; j < n; j++) {
            if (heights[j] > heights[i]) { answer[i] = heights[j]; break; }
        }
    }
    return answer;
}
```

It states the question word for word, and it is correct: for `[2, 7, 3]` it returns `[7, -1, -1]`, since 7 is the first value larger than 2 and nobody is larger than 7 or than the final 3.

<!-- stage: bottleneck -->
### The Same Stretch Is Walked Again

When the heights fall steadily, as in `[9, 8, 7, 6, 5]`, nobody has a taller person behind them, so each inner loop runs to the end of the row. The singer at index `i` makes `n - 1 - i` comparisons, and the total is about `n * n / 2`. A row of 100,000 singers needs about five billion comparisons to report that nobody is hidden, so the method is O(n^2) time.

The repeated work is visible in that example. The walk that starts at index 0 passes over indices 1, 2, 3 and 4, and the walk that starts at index 1 passes over 2, 3 and 4 again, and so on. Each walk rediscovers facts about the same people. A person who is already shorter than someone seen on the way will never be the answer for anybody who stands before that someone, yet every earlier walk still pays to step over them. The method has no memory of what the previous walks learned.

<!-- stage: insight -->
### Keep Only Singers Still Waiting

The scan keeps an **unresolved stack** of indices, which holds every position that has not yet met a greater value. Scanning from left to right, the current index `j` looks at the top of the stack. While the top exists and `heights[j]` is strictly greater than `heights[top]`, the top is answered by `j`, so it is popped and its answer is recorded. This is **resolve on pop**: an index gets its answer at the moment it leaves the stack, and `j` is the first value that can answer it, because any earlier position that was greater than the top would have popped it before `j` was reached. After the loop, `j` itself is pushed.

The reason it works is the **monotonic order** of the stack. Read from bottom to top, the values never increase. Suppose the current value is not greater than the top. Everything below the top is at least as large as the top, so the current value is not greater than any of them either, and the loop may stop at once without looking deeper. Suppose instead the current value beats the top. Then the top is finished, and the next one down is tested the same way. A value is pushed on top of an entry that is at least as large, so the order is kept.

<!-- names: unresolved stack, resolve on pop, monotonic order -->

Each index enters the stack once and leaves it at most once, so the total work over the whole scan is O(n), although a single step may pop many entries. Indices still on the stack at the end never met a greater value, and their answer stays at the default of -1. The same loop finds the next smaller value if the comparison is flipped, and it finds the next greater value to the left if the scan runs from the right.

<!-- stage: variables -->
### The Stack, The Answers, The Index

The scan index `j` is the position being examined, and every position before `j` has been either answered or pushed. The stack holds indices and not values, because an answer is often a position or a distance, and because two equal values can be told apart only by their positions. The answer array starts filled with -1, meaning that no greater value has been found, and an entry is written exactly once, at the moment its index is popped. The value on top of the stack, `heights[stack.peekLast()]`, is the smallest value in the stack, and it is the only one a new value has to be compared with first. With `ArrayDeque`, the chosen end is the last one: push with `addLast`, pop with `removeLast`, and read with `peekLast`.

<!-- stage: trace -->
### Two Rows Through The Stack

Take the row `5, 3, 4, 1, 6`. Index 0 holds 5, and the stack is empty, so 0 is pushed. Index 1 holds 3, which is not greater than 5, so it is pushed on top. Index 2 holds 4. It is greater than 3, so index 1 is answered with 4 and popped. It is not greater than 5, so the loop stops and index 2 is pushed. Index 3 holds 1 and is pushed. Index 4 holds 6, which is greater than 1, then 4, then 5, so three entries are popped in one step and all three receive the answer 6. The stack ends up holding only index 4, whose answer stays -1.

Now take `3, 3, 2, 5` with a strict comparison. Index 1 holds 3 and is equal to the top, so it does not resolve it, and the stack holds two 3s. The 2 is pushed. The 5 pops the 2, and then both 3s. The step to study in the first row is the last one, where a single value answers three indices, because it shows why the total work is linear even though one step is long.

```trace
{"cells":[5,3,4,1,6],"pointers":["j"],"steps":[{"at":{"j":0},"vars":{"stack":"[0]","answer":"[-1,-1,-1,-1,-1]"},"note":"The stack is empty, so index 0 (value 5) is pushed with nothing to resolve."},{"at":{"j":1},"vars":{"stack":"[0,1]","answer":"[-1,-1,-1,-1,-1]"},"note":"The value 3 is not greater than 5 on top, so nothing is resolved and index 1 is pushed."},{"at":{"j":2},"vars":{"stack":"[0,2]","answer":"[-1,4,-1,-1,-1]"},"note":"The value 4 is greater than the waiting value(s) at index 1, so each gets the answer 4 and leaves. Index 2 is then pushed."},{"at":{"j":3},"vars":{"stack":"[0,2,3]","answer":"[-1,4,-1,-1,-1]"},"note":"The value 1 is not greater than 4 on top, so nothing is resolved and index 3 is pushed."},{"at":{"j":4},"vars":{"stack":"[4]","answer":"[6,4,6,6,-1]"},"note":"The value 6 is greater than the waiting value(s) at index 3, 2, 0, so each gets the answer 6 and leaves. Index 4 is then pushed."}]}
```

```trace
{"cells":[3,3,2,5],"pointers":["j"],"steps":[{"at":{"j":0},"vars":{"stack":"[0]","answer":"[-1,-1,-1,-1]"},"note":"The stack is empty, so index 0 (value 3) is pushed with nothing to resolve."},{"at":{"j":1},"vars":{"stack":"[0,1]","answer":"[-1,-1,-1,-1]"},"note":"The value 3 is not greater than 3 on top, so nothing is resolved and index 1 is pushed."},{"at":{"j":2},"vars":{"stack":"[0,1,2]","answer":"[-1,-1,-1,-1]"},"note":"The value 2 is not greater than 3 on top, so nothing is resolved and index 2 is pushed."},{"at":{"j":3},"vars":{"stack":"[3]","answer":"[5,5,5,-1]"},"note":"The value 5 is greater than the waiting value(s) at index 2, 1, 0, so each gets the answer 5 and leaves. Index 3 is then pushed."}]}
```

<!-- stage: code -->
### Greater, Smaller, And By Position

```java
static int[] nextGreaterValue(int[] a) {
    int n = a.length;
    int[] answer = new int[n];
    java.util.Arrays.fill(answer, -1);
    java.util.ArrayDeque<Integer> stack = new java.util.ArrayDeque<>();
    for (int j = 0; j < n; j++) {
        while (!stack.isEmpty() && a[j] > a[stack.peekLast()]) {
            answer[stack.removeLast()] = a[j];     // j is the first strictly greater value
        }
        stack.addLast(j);
    }
    return answer;
}

static int[] nextSmallerValue(int[] a) {
    int n = a.length;
    int[] answer = new int[n];
    java.util.Arrays.fill(answer, -1);
    java.util.ArrayDeque<Integer> stack = new java.util.ArrayDeque<>();
    for (int j = 0; j < n; j++) {
        while (!stack.isEmpty() && a[j] < a[stack.peekLast()]) {
            answer[stack.removeLast()] = a[j];     // only the comparison changed
        }
        stack.addLast(j);
    }
    return answer;
}
```

Both methods make one left-to-right pass, and every index is pushed once and popped at most once, so the time is O(n) and the extra space is O(n) for the stack in the worst case of a row that never resolves. The comparison is strict, so a value equal to the top stays unresolved. `answer[stack.removeLast()]` unboxes the `Integer` into an index, and the stack holds positions, which is what lets the same loop return a distance `j - top` in the next lesson's exercise with no change to the structure.

<!-- stage: applicability -->
### When A Stack Of Waiters Fits

Use this scan when each position asks for the nearest later value that crosses a threshold relative to its own value, and the first such value ends its question. The invariant is that the stack holds exactly the positions that have not met a crossing value yet, with values that never increase from bottom to top, and the current value settles every top it strictly dominates. Decide the comparison before coding: strict for "greater", and flip it for "smaller".

The false friend is a globally greater value. The maximum of everything to the right is easy to compute, but it is rarely the first greater value, and for the row `2, 7, 3, 9` the answer for 2 is 7 and not 9. A second false friend is a heap of waiting values, which also gives the biggest or smallest waiting item but has no notion of position order, so it would cost logarithmic time per operation for no benefit. A third trap is storing values on the stack and then needing the position, because two equal values then cannot be told apart.

Do not use the pattern when the answer requires looking at the position of a threshold that is not tied to the element's own value, such as the first later value larger than a number that was given in advance, since there each position compares against a different threshold. Also keep the contract in view: a missing answer is reported as -1 only if -1 cannot be a real value, so a row that may hold -1 needs another marker.

<!-- stage: exercises -->
### Exercises

#### [Build] Next Greater Value (Author exercise)
<!-- id: ms-next-greater-value -->

**Prerequisites.** Arrays and loops; stack operations on `ArrayDeque`.

**Problem.** Given an integer array `a`, return an array `r` of the same length where `r[i]` is the first value after position `i` that is strictly greater than `a[i]`. If no such value exists, `r[i]` is -1.

**Constraints.** 1 <= a.length <= 10^5 and 0 <= a[i] <= 10^9, so -1 is never a real value. Aim for linear time and do not mutate `a`.

**Example 1.** Input `a = [2, 7, 3, 5, 4, 6, 8]`, output `[7, 8, 5, 6, 6, 8, -1]`.

**Example 2.** Input `a = [5, 4, 3]`, output `[-1, -1, -1]`, because a row that only falls resolves nobody.

**Hint.** What does the stack contain after the scan has handled position `j`? Which entries can the current value answer, and when must the loop stop?

**Changed decision.** First rung: the stack holds waiting positions, and an answer is written at the moment of a pop.

#### [Vary] Daily Temperatures (LeetCode 739)
<!-- id: ms-daily-temperatures -->

**Prerequisites.** The Next Greater Value exercise above.

**Problem.** Given an array `temperatures` of daily readings, return an array `r` where `r[i]` is the number of days after day `i` until a strictly warmer day arrives. If no warmer day ever arrives, `r[i]` is 0.

**Constraints.** 1 <= temperatures.length <= 10^5 and 30 <= temperatures[i] <= 100. Linear time is expected.

**Example 1.** Input `temperatures = [71, 69, 72, 65, 80, 75, 70]`, output `[2, 1, 2, 1, 0, 0, 0]`.

**Example 2.** Input `temperatures = [90, 80, 70, 85]`, output `[0, 2, 1, 0]`, so one warm day at the end answers two earlier days at different distances.

**Hint.** The answer is a distance, not a value. What must the stack store so that `j - top` can be computed when an entry is popped?

**Changed decision.** The output changes from the resolving value to the distance to the resolving position, so the stack must keep positions.

#### [Boundary] Equal Values Stay Unresolved (Author exercise)
<!-- id: ms-equal-stays-unresolved -->

**Prerequisites.** The two exercises above.

**Problem.** Given an integer array `a`, return for each position the index of the first later position whose value is strictly greater, or -1 if none exists. Equal values never answer each other.

**Constraints.** 1 <= a.length <= 10^5 and -10^9 <= a[i] <= 10^9, so values and indices are different kinds of numbers and -1 is safe as a position marker only.

**Example 1.** Input `a = [4, 4, 5, 4]`, output `[2, 2, -1, -1]`.

**Example 2.** Input `a = [3, 3, 3]`, output `[-1, -1, -1]`, since an equal value is not a greater one.

**Hint.** What would change in the output if the loop popped on `>=`? Which of the two examples would expose that mistake?

**Changed decision.** The comparison is strict, so a tie leaves the earlier index on the stack, which keeps the non-increasing order.

#### [Recognize] Next Greater Element I (LeetCode 496)
<!-- id: ms-next-greater-element-i -->

**Prerequisites.** All three exercises above, and hash maps from Chapter 04.

**Problem.** Two arrays of distinct integers are given, `queries` and `reference`, and every value of `queries` also appears in `reference`. For each value in `queries`, find its position in `reference` and return the first value to its right in `reference` that is greater than it, or -1 if there is none.

**Constraints.** 1 <= queries.length <= reference.length <= 1000, all values are distinct within each array, and 0 <= value <= 10^4. Linear time in the two lengths combined is expected.

**Example 1.** Input `queries = [4, 1, 2]`, `reference = [1, 3, 4, 2]`, output `[-1, 3, -1]`.

**Example 2.** Input `queries = [2, 4]`, `reference = [1, 2, 3, 4]`, output `[3, -1]`.

**Hint.** The scan only needs to run once, over `reference`. What would you store so that each query is a lookup, and what does a missing entry mean?

**Changed decision.** The scan is the same, but its results are stored under their values in a map, and the queries become lookups.
