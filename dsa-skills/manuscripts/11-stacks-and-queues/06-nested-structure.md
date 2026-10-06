<!-- lesson-kind: standard -->
<!-- lesson-id: nested-structure -->
## Save State For Each Nesting Level

<!-- stage: context -->
### One Total For Two Arrays

A report tool reads the JSON array `[1, [2, 9], 4]` and prints the sum of the numbers that each array holds directly. The inner array holds 2 and 9, so its sum is 11. The outer array holds 1 and 4 directly, so its sum is 5. A tool that keeps one running total prints 16 for the outer array, because the 11 from the inner array leaks into it. The tool needs the 1 it had read before the inner array began, and it needs that 1 again after the inner array ends. How does the code carry unfinished work across a nested group?

<!-- stage: naive -->
### Find Each Group And Add Its Numbers

A direct method takes each opening symbol in turn. It scans forward to find the matching closing symbol, then adds the digits between them. When it meets an inner group on the way, it jumps to that group's closing symbol so the inner digits are skipped. The input here uses single digits and parentheses, so `[1, [2, 9], 4]` is written `(1(29)4)`.

```java
static int[] directSumsByRescan(String s) {
    List<int[]> groups = new ArrayList<>();
    for (int i = 0; i < s.length(); i++) {
        if (s.charAt(i) != '(') continue;
        int close = findClose(s, i);
        int sum = 0;
        for (int k = i + 1; k < close; k++) {
            if (s.charAt(k) == '(') k = findClose(s, k);
            else sum += s.charAt(k) - '0';
        }
        groups.add(new int[] {close, sum});
    }
    groups.sort((a, b) -> Integer.compare(a[0], b[0]));
    int[] out = new int[groups.size()];
    for (int g = 0; g < out.length; g++) out[g] = groups.get(g)[1];
    return out;
}

static int findClose(String s, int open) {
    int depth = 0;
    for (int k = open; k < s.length(); k++) {
        if (s.charAt(k) == '(') depth++;
        else if (s.charAt(k) == ')' && --depth == 0) return k;
    }
    return -1;
}
```

The method reports the sums in the order the groups close, so `(1(29)4)` gives `[11, 5]`.

<!-- stage: bottleneck -->
### Searching For The Same Closing Symbols Again

```predict
Take 50,000 nested empty groups, written as 50,000 `(` followed by 50,000 `)`. About how many characters do the calls to `findClose` read in total?

About 5 billion. The outer loop calls `findClose` once per group, and each call reads every character up to that group's closing symbol. The inner jump inside each group calls `findClose` again for the next group.
```

For the group that opens at index `i`, `findClose` reads every character from the opening to its closing symbol. Deeper groups sit inside shorter spans, but the outer groups are long, so the reads add up to about 2k² characters for `k` nested groups. The method therefore costs O(n^2) time for a text of `n` characters.

The repeated work is the search for a closing symbol. The scan already passed every one of those characters once. A method that remembers the unfinished groups while it reads can finish each group at the moment its closing symbol arrives, with no second search.

<!-- stage: insight -->
### Save Enclosing State While A Group Runs

#### Why One Total Fails

An inner group must finish before the group around it can finish. While the inner group runs, the outer group has partial work, such as the sum 1 in `(1(29)4)`. A single variable cannot hold both the outer partial sum and the inner partial sum.

<!-- names: frame, parent, restore -->

#### One Frame For Each Open Level

A **frame** is the record of one nesting level that is still open. In this lesson a frame holds one integer, the partial sum of its level. The scan keeps the frame of the innermost open level in the variable `cur`. Every frame of an outer level waits on a stack. The group around a level is its **parent**. When a `(` arrives, the scan pushes `cur` and starts a new frame with sum 0. At that moment the stack holds the frames of every parent, with the nearest parent on top.

#### Closing A Level

When a `)` arrives, the level is complete, and the scan records `cur` as its answer. The scan then pops the saved frame to **restore** the parent as the current level. The parent continues from the partial sum it had before the inner group began. The invariant is that `cur` is the partial sum of the innermost open level, and the stack holds the partial sums of all levels around it, in nesting order.

<!-- stage: variables -->
### The State Of The Scan

The scan keeps five pieces of state.

- **cur** is the partial sum of the innermost open level. A digit adds to it.
- **saved** is the stack of partial sums of the outer levels. A `(` pushes to it and a `)` pops from it.
- **out** is the list of finished sums, in the order the groups close.
- **i** is the position the scan reads now, and it grows by one per step.
- **c** is the character at index `i`, a digit, `(` or `)`.

<!-- stage: trace -->
### Two Inputs Through The Frames

#### Siblings Inside One Group

The first input is `(3(15)2(4))`. The outer group holds 3 and 2 directly. It also holds two inner groups, `(15)` and `(4)`. The scan pushes 0 at the first `(`, then adds 3. The second `(` pushes 3 and starts a new frame, and the digits 1 and 5 make it 6. The `)` records 6 and restores 3. The 2 makes the outer sum 5, and the group `(4)` records 4 in the same way. The last `)` records 5.

```trace
{"cells":["(","3","(","1","5",")","2","(","4",")",")"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"cur":0,"saved":"[0]","out":"[]"},"note":"( pushes the partial sum of the level around it and starts a new level at 0."},{"at":{"i":1},"vars":{"cur":3,"saved":"[0]","out":"[]"},"note":"The digit 3 adds to the current level, so the partial sum becomes 3."},{"at":{"i":2},"vars":{"cur":0,"saved":"[0, 3]","out":"[]"},"note":"( pushes the partial sum of the level around it and starts a new level at 0."},{"at":{"i":3},"vars":{"cur":1,"saved":"[0, 3]","out":"[]"},"note":"The digit 1 adds to the current level, so the partial sum becomes 1."},{"at":{"i":4},"vars":{"cur":6,"saved":"[0, 3]","out":"[]"},"note":"The digit 5 adds to the current level, so the partial sum becomes 6."},{"at":{"i":5},"vars":{"cur":3,"saved":"[0]","out":"[6]"},"note":") records 6 as the finished sum and restores the saved partial sum 3."},{"at":{"i":6},"vars":{"cur":5,"saved":"[0]","out":"[6]"},"note":"The digit 2 adds to the current level, so the partial sum becomes 5."},{"at":{"i":7},"vars":{"cur":0,"saved":"[0, 5]","out":"[6]"},"note":"( pushes the partial sum of the level around it and starts a new level at 0."},{"at":{"i":8},"vars":{"cur":4,"saved":"[0, 5]","out":"[6]"},"note":"The digit 4 adds to the current level, so the partial sum becomes 4."},{"at":{"i":9},"vars":{"cur":5,"saved":"[0]","out":"[6, 4]"},"note":") records 4 as the finished sum and restores the saved partial sum 5."},{"at":{"i":10},"vars":{"cur":0,"saved":"[]","out":"[6, 4, 5]"},"note":") records 5 as the finished sum and restores the saved partial sum 0."},{"at":{"i":11},"vars":{"cur":0,"saved":"[]","out":"[6, 4, 5]"},"note":"The text ends with an empty saved stack, and out holds the answer."}]}
```

#### A Chain Of Nested Groups

The second input is `(2(4(6))5)`. Every group has one inner group. The saved stack grows to three frames at the deepest point. Each `)` records the sum of its own level and restores the level around it. The outer level resumes with its 2 and adds the 5 after both inner groups are gone.

```trace
{"cells":["(","2","(","4","(","6",")",")","5",")"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"cur":0,"saved":"[0]","out":"[]"},"note":"( pushes the partial sum of the level around it and starts a new level at 0."},{"at":{"i":1},"vars":{"cur":2,"saved":"[0]","out":"[]"},"note":"The digit 2 adds to the current level, so the partial sum becomes 2."},{"at":{"i":2},"vars":{"cur":0,"saved":"[0, 2]","out":"[]"},"note":"( pushes the partial sum of the level around it and starts a new level at 0."},{"at":{"i":3},"vars":{"cur":4,"saved":"[0, 2]","out":"[]"},"note":"The digit 4 adds to the current level, so the partial sum becomes 4."},{"at":{"i":4},"vars":{"cur":0,"saved":"[0, 2, 4]","out":"[]"},"note":"( pushes the partial sum of the level around it and starts a new level at 0."},{"at":{"i":5},"vars":{"cur":6,"saved":"[0, 2, 4]","out":"[]"},"note":"The digit 6 adds to the current level, so the partial sum becomes 6."},{"at":{"i":6},"vars":{"cur":4,"saved":"[0, 2]","out":"[6]"},"note":") records 6 as the finished sum and restores the saved partial sum 4."},{"at":{"i":7},"vars":{"cur":2,"saved":"[0]","out":"[6, 4]"},"note":") records 4 as the finished sum and restores the saved partial sum 2."},{"at":{"i":8},"vars":{"cur":7,"saved":"[0]","out":"[6, 4]"},"note":"The digit 5 adds to the current level, so the partial sum becomes 7."},{"at":{"i":9},"vars":{"cur":0,"saved":"[]","out":"[6, 4, 7]"},"note":") records 7 as the finished sum and restores the saved partial sum 0."},{"at":{"i":10},"vars":{"cur":0,"saved":"[]","out":"[6, 4, 7]"},"note":"The text ends with an empty saved stack, and out holds the answer."}]}
```

<!-- stage: code -->
### Writing The Scan In Java

#### The Scan Method

The method assumes a balanced text, which the problem contract guarantees. It stores the saved sums in an `ArrayDeque<Integer>` and pushes `cur` when a group opens.

```java
static int[] directSums(String s) {
    ArrayDeque<Integer> saved = new ArrayDeque<>();
    List<Integer> out = new ArrayList<>();
    int cur = 0;
    for (int i = 0; i < s.length(); i++) {
        char c = s.charAt(i);
        if (c == '(') {
            saved.push(cur);
            cur = 0;
        } else if (c == ')') {
            out.add(cur);
            cur = saved.pop();
        } else {
            cur += c - '0';
        }
    }
    int[] result = new int[out.size()];
    for (int g = 0; g < result.length; g++) result[g] = out.get(g);
    return result;
}
```

#### Cost Of The Scan

Each character causes at most one push, one pop or one addition. The method runs in O(n) time. The stack holds one integer per open level, so the space is O(d) for nesting depth `d`, plus O(g) for the `g` recorded sums. Digits outside every group go into the starting value of `cur` and appear in no answer.

<!-- stage: applicability -->
### When Each Level Needs Its Own State

#### Recognize The Cue

Use saved frames when an inner structure must finish before the structure around it can finish. The invariant is that the current variables describe the innermost open level and the stack describes every level around it. Nested arrays, nested function calls and nested markup all have this shape. The cue is a computation at each level that depends on a result from the levels inside it.

#### One Accumulator Is A False Friend

A single global total looks like enough, because the sum of all digits is easy to keep. It is a false friend whenever a level needs its own answer. It cannot give the sum of the outer level after an inner group has added digits to the same variable. A reset at each `(` has the opposite fault, because it loses the partial sum that the outer level had before the inner group began.

#### When No Frame Is Needed

Skip the frames when the answer depends only on how deep the scan is, such as the maximum nesting depth. A depth counter or the stack size is enough there. Skip them as well for questions about the whole text, such as the total of all digits. The frames pay off only when each level carries a value that the scan must come back to.

<!-- stage: exercises -->
### Exercises

#### [Build] Maximum Parenthesis Depth (Author exercise)
<!-- id: sq-max-nesting-depth -->

**Prerequisites.** The stack of open levels in this lesson.

**Problem.** The depth of a character in a balanced string of `(` and `)` is the number of groups that are open and contain it. The depth of a `(` counts its own group. Given a balanced string `s`, return the largest depth of any character, or 0 for the empty string.

**Constraints.** The limits are:
- **Length** is `0 <= s.length() <= 10^5`.
- **Characters** are only `(` and `)`, and `s` is balanced.
- **Return** is an `int`.
- **Mutation** is not allowed; the string does not change.

**Example 1.** Input `(()(()))`, output 3.

**Example 2.** Input `()()()`, output 1, because no group contains another.

**Hint.** Push a marker at each `(` and pop one at each `)`. Which value of the stack size do you record after each push?

**Changed decision.** Basic case: the stack stores only that a level is open, and the answer is the largest stack size.

#### [Vary] Sum Values By Nested Group (Author exercise)
<!-- id: sq-inclusive-group-totals -->

**Prerequisites.** The exercise above and the frames of this lesson.

**Problem.** A string `s` holds digits and balanced parentheses. A group's total is the sum of every digit between its `(` and its matching `)`, including digits inside nested groups. Return the totals of all groups in the order their closing parentheses appear. Digits outside every group appear in no total.

**Constraints.** The limits are:
- **Length** is `0 <= s.length() <= 10^5`.
- **Characters** are the digits `0` to `9`, `(` and `)`, and the parentheses are balanced.
- **Totals** fit in an `int`, because each digit is at most 9.
- **Return** is an `int[]`, empty when `s` holds no group.

**Example 1.** Input `(1(29)4)`, output `[11, 16]`.

**Example 2.** Input `7(3)(48)2`, output `[3, 12]`.

**Hint.** The lesson restores the parent's partial sum when a level closes. What must the parent receive from the level that just closed?

**Changed decision.** The contract counts nested digits, so a closing level adds its total to the restored parent.

#### [Boundary] Deep Single Chain (Author exercise)
<!-- id: sq-deep-single-chain -->

**Prerequisites.** The two exercises above.

**Problem.** The height of a balanced string of `(` and `)` is the largest number of groups that contain one another, counting empty groups, and 0 for the empty string. A string that is not balanced has no height. Return the height of `s`, or -1 when `s` is not balanced.

**Constraints.** The limits are:
- **Length** is `0 <= s.length() <= 10^5`.
- **Characters** are only `(` and `)`.
- **Return** is an `int`, and -1 marks any string that is not balanced.
- **Mutation** is not allowed; the string does not change.

**Example 1.** Input `((((()))))`, output 5, a chain of five empty-bodied groups.

**Example 2.** Input `)(`, output -1, because the first character closes a group that was never opened.

**Hint.** Store in each frame the greatest height of the inner groups already closed. What does a level return to its parent when it closes?

**Changed decision.** The scan must detect an invalid text, so a `)` on an empty stack and a nonempty final stack both return -1.

#### [Recognize] Score Of Parentheses (LeetCode 856)
<!-- id: sq-score-of-parentheses -->

**Prerequisites.** All three exercises above.

**Problem.** The score of a balanced string is defined by three rules. The string `()` scores 1. A concatenation `AB` of two balanced strings scores `score(A) + score(B)`. A string `(A)` around a balanced string `A` scores `2 * score(A)`. Given a balanced string `s`, return its score.

**Constraints.** The limits are:
- **Length** is `2 <= s.length() <= 50`.
- **Characters** are only `(` and `)`, and `s` is balanced.
- **Return** is an `int`.
- **Mutation** is not allowed; the string does not change.

**Example 1.** Input `((()()))`, output 8.

**Example 2.** Input `()(())()`, output 4.

**Hint.** Give each frame the score of the siblings closed so far. What does a `)` add to the restored parent when the closed level held nothing?

**Changed decision.** A closed level contributes `max(2 * inner, 1)` to its parent, so an empty level adds 1.
