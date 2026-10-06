<!-- lesson-kind: standard -->
<!-- lesson-id: choose-explore-unchoose -->
## Undo Each Choice After Exploring It

<!-- stage: context -->
### Why The Test Plans Keep Growing

A test generator must run a program with every on and off setting of three flags. The developer keeps one shared list of settings and writes a method that adds `on`, calls itself for the next flag, adds `off` and calls itself again. The first plan prints `[on, on, on]`. The second plan prints `[on, on, on, off, off]`, which holds five settings for three flags. Every later plan is longer, and the generator never finishes with a correct plan.

The shared list carries the leftovers of one branch into the next branch. This lesson asks how a recursive method uses one shared list safely, and what it must do after each call returns.

<!-- stage: naive -->
### Passing A New List To Every Call

The direct plan avoids the shared list. Each call copies the list, adds one setting to the copy and passes the copy down.

```java
static void walkByCopy(int depth, int n, List<Integer> path, List<List<Integer>> out) {
    if (depth == n) { out.add(path); return; }                  // the copy already belongs to this branch only
    for (int v = 0; v <= 1; v++) {
        List<Integer> next = new ArrayList<>(path);             // a new list for each child call
        next.add(v);                                            // the copy gets one more setting
        walkByCopy(depth + 1, n, next, out);
    }
}
```

The method returns the right plans, because no two branches share a list. Each call allocates a new list as long as its depth.

<!-- stage: bottleneck -->
### Counting The Work Of Copying

```predict
A search makes 20 binary choices and only counts the leaves that pass a test, so it stores no list. About how many values do all the copies move?

The tree has 2^21 - 1, about 2 million calls. A call at depth d copies d - 1 values and adds one, so the copies move about 19 * 2^21, which is roughly 40 million values. A search that edits one list in place spends one append and one removal per call, so it moves about 4 million values.
```

The copies make the cost per call proportional to the depth, which is O(n) time and O(n) memory per call. The in-place search pays O(1) time per call, so the whole search costs O(2^n) and no longer carries a factor of n.

The shared list is therefore the better choice, and it only needs a rule that keeps the branches apart. The rule says that a call leaves the list exactly as it found it.

<!-- stage: insight -->
### Leaving The List As You Found It

#### Keeping One Working Path

The **working path** is one list that holds exactly the choices of the calls that are active at this moment. A call adds its choice, then calls itself, and the callee sees the choice at the end of the list. Every call on the stack has contributed one entry, in the order of the stack.

#### Taking Back The Choice

The **undo step** is the removal of the entry that the call added. It runs right after the recursive call returns. The next choice follows only after it. After the undo step, the list equals what it held when the call began, so the next sibling starts from the same state as the first one. A call that returns without the undo step breaks this equality, and the loss shows up in the siblings that follow.

#### Saving A Finished Path

A leaf stores its result by adding the working path to the output. The list keeps changing after the leaf returns, so the output must receive a **snapshot**, a new list with the same values. Without the copy, every stored result is the same list object, and it ends up empty after all undo steps have run.

<!-- names: working path, undo step, snapshot -->

<!-- stage: variables -->
### The Pieces Of State

Four pieces of state control the search.

- **Depth** is the number of choices that the working path holds, and it equals the position of the next decision.
- **Working path** is the one shared list that holds the choices of the active calls.
- **Output** is the list of snapshots that leaves have stored.
- **Candidate** is the value that the loop in the current call adds to the working path.

The depth grows by one in each call. The working path grows by one before the recursive call and shrinks by one after it.

<!-- stage: trace -->
### Following The Path Through Two Choices

#### Tracing Both Flags

The first trace runs the search with two binary choices. The pointer `d` shows the depth of the current call, and the cell labels name the two decisions. The variable `path` shows the working path after the step, and `stored` counts the snapshots in the output.

The search adds 0 at depth 0 and again at depth 1, which fills the path, so the leaf stores a snapshot and the undo step removes the last 0. The loop then adds 1 at depth 1, stores a second snapshot and removes it. The call at depth 0 now removes its own 0 and tries 1. At the end of the trace, the path is empty again and four snapshots sit in the output.

#### Tracing The Missing Undo Step

The second trace removes the undo step from the same search. The first leaf stores `[0, 0]`, and the path keeps both entries. The next loop step adds 1 to a path that already holds two values, so the call at depth 1 builds `[0, 0, 1]`. That path is longer than the number of decisions. The wrong plan from the opening appears at that step.

#### Stepping Through Both Runs

```trace
{"cells":["flag 0","flag 1"],"pointers":["d"],"steps":[{"at":{"d":0},"vars":{"path":"0","stored":0},"note":"The call at depth 0 adds 0, so the working path is [0]."},{"at":{"d":1},"vars":{"path":"0,0","stored":0},"note":"The call at depth 1 adds 0, so the working path is [0,0]."},{"at":{"d":2},"vars":{"path":"0,0","stored":1},"note":"The depth equals 2, so the leaf stores the snapshot [0,0]."},{"at":{"d":1},"vars":{"path":"0","stored":1},"note":"The undo step removes the 0 from depth 1, so the working path is [0]."},{"at":{"d":1},"vars":{"path":"0,1","stored":1},"note":"The call at depth 1 adds 1, so the working path is [0,1]."},{"at":{"d":2},"vars":{"path":"0,1","stored":2},"note":"The depth equals 2, so the leaf stores the snapshot [0,1]."},{"at":{"d":1},"vars":{"path":"0","stored":2},"note":"The undo step removes the 1 from depth 1, so the working path is [0]."},{"at":{"d":0},"vars":{"path":"empty","stored":2},"note":"The undo step removes the 0 from depth 0, so the working path is [empty]."},{"at":{"d":0},"vars":{"path":"1","stored":2},"note":"The call at depth 0 adds 1, so the working path is [1]."},{"at":{"d":1},"vars":{"path":"1,0","stored":2},"note":"The call at depth 1 adds 0, so the working path is [1,0]."},{"at":{"d":2},"vars":{"path":"1,0","stored":3},"note":"The depth equals 2, so the leaf stores the snapshot [1,0]."},{"at":{"d":1},"vars":{"path":"1","stored":3},"note":"The undo step removes the 0 from depth 1, so the working path is [1]."},{"at":{"d":1},"vars":{"path":"1,1","stored":3},"note":"The call at depth 1 adds 1, so the working path is [1,1]."},{"at":{"d":2},"vars":{"path":"1,1","stored":4},"note":"The depth equals 2, so the leaf stores the snapshot [1,1]."},{"at":{"d":1},"vars":{"path":"1","stored":4},"note":"The undo step removes the 1 from depth 1, so the working path is [1]."},{"at":{"d":0},"vars":{"path":"empty","stored":4},"note":"The undo step removes the 1 from depth 0, so the working path is [empty]."}]}
```

```trace
{"cells":["flag 0","flag 1"],"pointers":["d"],"steps":[{"at":{"d":0},"vars":{"path":"0","stored":0},"note":"The call at depth 0 adds 0, so the working path is [0]."},{"at":{"d":1},"vars":{"path":"0,0","stored":0},"note":"The call at depth 1 adds 0, so the working path is [0,0]."},{"at":{"d":2},"vars":{"path":"0,0","stored":1},"note":"The depth equals 2, so the leaf stores the snapshot [0,0]. No undo step follows."},{"at":{"d":1},"vars":{"path":"0,0,1","stored":1},"note":"The loop at depth 1 adds 1 to a path that still holds two entries, so the path is [0,0,1], longer than the two decisions."},{"at":{"d":2},"vars":{"path":"0,0,1","stored":2},"note":"The leaf stores the snapshot [0,0,1], a third entry for two flags. The output is already wrong."}]}
```

<!-- stage: code -->
### Writing The Search In Java

#### The Search With An Undo Step

The method below keeps one working path. The leaf stores a copy, and every `add` has a matching removal.

```java
static void walk(int depth, int n, List<Integer> path, List<List<Integer>> out) {
    if (depth == n) {                                   // every decision is made
        out.add(new ArrayList<>(path));                 // store a copy, because path keeps changing
        return;
    }
    for (int v = 0; v <= 1; v++) {                      // two candidates for this decision
        path.add(v);                                    // choose: the callee sees v at the end
        walk(depth + 1, n, path, out);                  // explore the rest of the decisions
        path.remove(path.size() - 1);                   // undo: remove by index, the last entry
    }
}
```

#### Removing By Index

The call `path.remove(path.size() - 1)` takes an `int`, so Java removes the entry at that index. The call `path.remove(v)` with an `int` variable `v` does the same and removes the entry at index `v`, which is a different entry. To remove a value, the call must pass an `Integer` object. The undo step always uses the index of the last entry.

#### Cost Of The Search

The search visits 2^(n+1) - 1 calls, and each call costs O(1) time outside the copies at the leaves. The 2^n snapshots cost O(n) each, so the search costs O(n * 2^n) time in total, and the output needs O(n * 2^n) memory. The working path and the stack together use O(n) memory.

<!-- stage: applicability -->
### Recognizing A Shared Path

#### Spotting The Pattern

The cue is a method that builds a candidate one choice at a time, explores what follows and then tries a sibling. The invariant is that on entry to each call the working path holds exactly the choices of the calls above it.

#### Finding The False Friend

The false friend is a missing undo step. The code compiles, and the first branch works, so a quick test with one leaf passes. A second false friend is the stored reference without a copy. Both bugs show up only when a test has several results, and the output then holds identical or overlong lists.

#### Recognizing The No-Go Cases

The shared path does not fit when two threads run the search at the same time, because both would edit one list. It does not fit when each call must keep its own history, which happens when a result needs a persistent version of every prefix. A copy per call suits those cases.

<!-- stage: exercises -->
### Exercises

#### [Build] Binary Choices (Author exercise)
<!-- id: bt-binary-choices -->

**Prerequisites.** The working path and the undo step of this lesson.

**Problem.** Given an integer `n`, return every string of length `n` that holds only the characters `0` and `1`. Build each string in one shared `StringBuilder` by appending a character, calling the method for the next position and removing the character before the alternative. The result lists the strings in increasing order, and the character `0` comes before `1` at each position.

**Constraints.** The limits are:
- **Length** is `0 <= n <= 12`.
- **Characters** are `0` and `1` only.
- **Order** is increasing lexicographic order.
- **Empty case** `n = 0` returns one empty string.

**Example 1.** Input `n = 2`, output `["00","01","10","11"]`.

**Example 2.** Input `n = 0`, output `[""]`.

**Hint.** What is the length of the builder before and after each recursive call? Which method of `StringBuilder` shortens it by one?

**Changed decision.** The working path is a `StringBuilder` and the undo step is one shortening, and the stored result is a `String`, which is already a copy.

#### [Vary] Variable Candidate Loop (Author exercise)
<!-- id: bt-variable-candidate-loop -->

**Prerequisites.** The previous exercise.

**Problem.** Given an integer array `options` with distinct values, an integer `k` and an integer `target`, count the sequences of length `k` that add up to `target`. Every entry of a sequence comes from `options`. An option may appear several times in one sequence. Two sequences with the same values in a different order count as different sequences.

**Constraints.** The limits are:
- **Options** satisfy `1 <= options.length <= 5` and `-9 <= options[i] <= 9`.
- **Length** is `0 <= k <= 8`.
- **Target** is `-100 <= target <= 100`.
- **Empty sequence** has the sum 0.

**Example 1.** Input `options = [1,2]`, `k = 3`, `target = 5`, output 3.

**Example 2.** Input `options = [4]`, `k = 0`, `target = 4`, output 0.

**Hint.** Which value replaces the list as the working state? How many candidates does the loop try at each depth?

**Changed decision.** The loop tries several candidates at one depth, and the undo step reverses a running sum and not a list.

#### [Boundary] Store A Completed Path (Author exercise)
<!-- id: bt-store-completed-path -->

**Prerequisites.** The two exercises above.

**Problem.** Use the input of the previous exercise and return the sequences themselves instead of their count. Each sequence is a list of integers. The result lists the sequences in the order in which a search that tries `options` from left to right at each depth finds them. A sequence stored in the result must not change when the search continues.

**Constraints.** The limits are:
- **Options** satisfy `1 <= options.length <= 5` and `-9 <= options[i] <= 9`.
- **Length** is `0 <= k <= 6`.
- **Target** is `-100 <= target <= 100`.
- **Empty result** is an empty list when no sequence reaches `target`.

**Example 1.** Input `options = [1,2]`, `k = 2`, `target = 3`, output `[[1,2],[2,1]]`.

**Example 2.** Input `options = [5]`, `k = 0`, `target = 0`, output `[[]]`.

**Hint.** What does `out.add(path)` store in the output? What does the output hold after the last undo step?

**Changed decision.** The leaf stores a copy of the working path, and the empty path is a valid stored result.

#### [Recognize] Subsets (LeetCode 78)
<!-- id: bt-subsets-include-exclude -->

**Prerequisites.** The previous three exercises.

**Problem.** Given an array `nums` of distinct integers, return every subset of `nums`, including the empty subset and `nums` itself. Decide each position in order and try excluding the value before including it. Each subset keeps the order of its values in `nums`, and the result lists the subsets in the order in which that search reaches them.

**Constraints.** The limits are:
- **Length** is `0 <= nums.length <= 10`.
- **Values** are distinct integers with `-10 <= nums[i] <= 10`.
- **Count** of subsets is exactly `2^nums.length`.
- **Mutation** does not occur; `nums` keeps its order.

**Example 1.** Input `nums = [1,2]`, output `[[],[2],[1],[1,2]]`.

**Example 2.** Input `nums = []`, output `[[]]`.

**Hint.** How many decisions does each subset need? Which working state does the call at index `i` hold?

**Changed decision.** The two candidates at each depth are to exclude and to include the value at that index, and the depth counts positions of the input.
