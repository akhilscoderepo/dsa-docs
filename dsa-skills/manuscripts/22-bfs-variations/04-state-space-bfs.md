<!-- lesson-kind: standard -->
<!-- lesson-id: search-generated-states -->
## Search States You Generate

<!-- stage: context -->
### Searching Without A Graph

A hardware device accepts a four-digit code. Its only command turns one digit up or down by one, and the digit 9 wraps to 0 in both directions. The firmware refuses a list of blocked codes. A technician needs the fewest commands that take the device from 0000 to a target code, and a wrong count wastes a real maintenance window.

Chapter 21 searched graphs that arrive as an adjacency list. Here nobody gives a list of vertices or edges. The input is a start code, a target code and a rule that says which codes one command can reach. There are 10,000 possible codes, and the rule produces the neighbors of any code on demand.

This lesson asks how breadth-first search runs when the graph exists only as a rule, and what the visited set must contain to give a correct answer.

<!-- stage: naive -->
### Building The Whole Graph First

The direct idea reuses the ordinary search from the earlier chapter. It builds the adjacency list for all 10,000 codes first, and then it runs breadth-first search on that list.

```java
static List<List<Integer>> buildGraph() {
    List<List<Integer>> adj = new ArrayList<>();
    for (int code = 0; code < 10_000; code++) {
        List<Integer> row = new ArrayList<>();
        for (int wheel = 1; wheel <= 1000; wheel *= 10) {
            int digit = code / wheel % 10;
            row.add(code - digit * wheel + (digit + 1) % 10 * wheel);
            row.add(code - digit * wheel + (digit + 9) % 10 * wheel);
        }
        adj.add(row);
    }
    return adj;
}
```

```predict
A device has eight wheels and the target is two commands away from the start. How many codes does the method above build, and how many codes does a search need to read?

The method builds 10^8 codes with 16 neighbors each, about 1.6 billion list entries, which does not fit in memory. A search that stops two commands from the start reads fewer than 300 codes: the start, its 16 neighbors, and at most 16 times 16 codes after that.
```

<!-- stage: bottleneck -->
### Paying For Codes The Search Never Reads

The method is correct, and the cost is the issue. For `w` wheels it creates 10^w vertices with 2w neighbors each, so building the list takes O(10^w * w) time and the same memory. At four wheels this is about 80,000 entries and still cheap. At eight wheels the list needs more memory than most machines have.

The search itself reads only the codes within the answer distance of the start, which is a tiny part of the list. Most of the work and memory goes to vertices that the search never touches.

The waste grows worse when a problem has more facts than the code. A grid with doors and keys has one vertex for every cell and every set of keys held. Most of those combinations can never occur. The fix is to skip the list, keep only the vertices the search reaches, and compute the neighbors of a vertex when the search takes it from the queue.

<!-- stage: insight -->
### Treating Each Situation As A State

A **state** is a complete description of one position in the search. The queue holds states, the visited set holds states, and every move maps one state to another. In the lock, the state is the four-digit code. The search stays an ordinary breadth-first search, and only one line changes: the call that read `adj.get(current)` becomes a call that generates the neighbors from the rule.

<!-- names: state, encoding, successor -->

#### Generating Neighbors From Rules

A **successor** of a state is a state that one legal move reaches. A method `successors(state)` applies every legal move to a copy of the state and returns the results. For a code, it turns each wheel up and then down by one, so a four-digit code has eight successors. The search discards a successor that is blocked or already visited, and it enqueues the others.

#### Choosing An Encoding

The **encoding** is the Java value that stands for a state, such as a `String`, an `int` or a record. Two states that mean the same position must produce equal values, because the visited set compares values. A `String` works in a `HashSet`, since it defines `equals` and `hashCode`. A `char[]` does not, because an array compares by identity and two arrays with the same digits count as different entries.

#### Including Every Fact That Matters

The encoding must contain every fact that changes which moves are legal later. Take a grid with two rows. Row 0 reads S, a free cell, a door D and the target T. Row 1 has a wall below S, a key K below the free cell, and walls below the door and the target. The door opens only for a walker who holds the key. A search that marks only the cell as visited reaches the free cell without the key and marks it. It then walks down to the key, but the free cell is already visited, so it never returns. That search reports -1. The true answer is 5 moves, found when the encoding is the triple of row, column and whether the key is held. The same cell with and without the key are two different states.

<!-- stage: variables -->
### What The Search Keeps

The search keeps a queue, a set of seen states and a counter. The code below uses these names, and each one has a fixed starting value.

- **queue** is an `ArrayDeque<String>` that holds generated codes waiting to be expanded; it starts with the start code.
- **seen** is a `HashSet<String>` that holds every code that is blocked or already generated; it starts with the blocked codes.
- **turns** is an `int` that counts commands; it is 0 for the start code and grows by one for each pass over the queue.
- **current** is the code that the search just took from the queue.
- **next** is one generated neighbor of `current`.

<!-- stage: trace -->
### Following Two Generated Searches

#### A Lock With Two Wheels

The first trace uses a lock with two wheels, so there are 100 codes and the search never builds them. The start is 00, the target is 11, and the blocked codes are 10 and 90. The cells hold the codes in the order the search takes them from the queue, and the pointer `cur` marks the code just taken. The code 00 has four neighbors, but two are blocked, so only 01 and 09 enter the queue. The code 01 generates 11, which is the target, and the search returns 2 when it takes 11.

```trace
{"cells":["00","01","09","11"],"pointers":["cur"],"steps":[{"at":{"cur":0},"vars":{"turns":0,"queued":2},"note":"The search takes 00 from the queue and generates 01, 09; each of them is 1 turn from the start."},{"at":{"cur":1},"vars":{"turns":1,"queued":4},"note":"The search takes 01 from the queue and generates 11, 91, 02; each of them is 2 turns from the start."},{"at":{"cur":2},"vars":{"turns":1,"queued":6},"note":"The search takes 09 from the queue and generates 19, 99, 08; each of them is 2 turns from the start."},{"at":{"cur":3},"vars":{"turns":2,"queued":5},"note":"The search takes 11 from the queue after 2 turns. It equals the target, so the method returns 2."}]}
```

#### A Grid With A Door And A Key

The second trace uses the grid from the insight stage. Each cell label is the triple row, column and key, with key 1 meaning the key is held. The search starts at (0,0,0) and reaches the key cell at (1,1,1). It then returns to cell (0,1) with the key, which is a new state (0,1,1), so the visited set allows it. The door cell (0,2) can now be entered, and the search reaches the target after 5 moves.

```trace
{"cells":["(0,0,0)","(0,1,0)","(1,1,1)","(0,1,1)","(0,2,1)","(0,0,1)","(0,3,1)"],"pointers":["cur"],"steps":[{"at":{"cur":0},"vars":{"moves":0,"queued":1},"note":"The search takes (0,0,0) and generates (0,1,0)."},{"at":{"cur":1},"vars":{"moves":1,"queued":1},"note":"The search takes (0,1,0) and generates (1,1,1)."},{"at":{"cur":2},"vars":{"moves":2,"queued":1},"note":"The search takes (1,1,1) and generates (0,1,1)."},{"at":{"cur":3},"vars":{"moves":3,"queued":2},"note":"The search takes (0,1,1) and generates (0,2,1), (0,0,1)."},{"at":{"cur":4},"vars":{"moves":4,"queued":2},"note":"The search takes (0,2,1) and generates (0,3,1)."},{"at":{"cur":5},"vars":{"moves":4,"queued":1},"note":"The search takes (0,0,1) and generates no new state."},{"at":{"cur":6},"vars":{"moves":5,"queued":0},"note":"The search takes (0,3,1), the target cell, after 5 moves, so it returns 5."}]}
```

<!-- stage: code -->
### Generating Neighbors In Java

The method returns the fewest commands, or -1 when the target cannot be reached.

```java
static int openLock(String[] deadends, String target) {
    Set<String> seen = new HashSet<>(Arrays.asList(deadends));
    ArrayDeque<String> queue = new ArrayDeque<>();
    if (!seen.add("0000")) return -1;
    queue.add("0000");
    for (int turns = 0; !queue.isEmpty(); turns++) {
        for (int count = queue.size(); count > 0; count--) {
            String current = queue.poll();
            if (current.equals(target)) return turns;
            for (String next : successors(current)) {
                if (seen.add(next)) queue.add(next);
            }
        }
    }
    return -1;
}

static List<String> successors(String code) {
    List<String> result = new ArrayList<>();
    char[] digits = code.toCharArray();
    for (int wheel = 0; wheel < digits.length; wheel++) {
        char original = digits[wheel];
        digits[wheel] = (char) ('0' + (original - '0' + 1) % 10);
        result.add(new String(digits));
        digits[wheel] = (char) ('0' + (original - '0' + 9) % 10);
        result.add(new String(digits));
        digits[wheel] = original;
    }
    return result;
}
```

The call `seen.add(next)` returns false when the set already holds the code, so one call both tests and marks it. Adding `+ 9` and taking the remainder by 10 turns a step down into a step up that wraps, because `%` in Java returns a negative value for a negative left operand. The time is O(R * w) for `R` reachable codes of `w` digits. The space is O(R * w) for the set and the queue.

<!-- stage: applicability -->
### Recognizing Searches Over Generated States

#### Reading The Cue

Use this method when the statement gives no graph, only a start, a goal and a rule for legal moves, and every move costs the same. Puzzle boards, number transformations and word edits fit this shape. A grid with extra rules, such as keys, fuel or a direction, fits it too. A grid with plain free and blocked cells fits it with the cell coordinates as the state.

#### Checking The Invariant

The invariant of the lesson is that the encoding holds every fact that affects future moves, and the visited set stores that complete encoding. Ask one question for each candidate state: if two situations share this encoding, will the same moves be legal from both? When the answer is no, add the missing fact to the encoding. Each fact multiplies the number of states, so add only facts that change the legal moves.

#### Avoiding The False Friend

The false friend is marking only the visible location. It looks like the ordinary grid search from the earlier chapter, and it gives the wrong answer as soon as a key, a mask or a mode changes the moves available from a cell. The door and key grid in the insight stage shows -1 where the true answer is 5. The opposite mistake also costs: an encoding with unused facts makes the search visit duplicates of the same situation.

<!-- stage: exercises -->
### Exercises

#### [Build] Combination-Lock States (Author exercise)
<!-- id: bv4-lock-neighbors -->

**Prerequisites.** The generated neighbors of this lesson.

**Problem.** A lock shows `w` wheels, and each wheel holds one decimal digit. One turn moves a single wheel to the next digit up or down, and the digit 9 wraps to 0 while the digit 0 wraps to 9. Given a code as a string of `w` digits, return every code that one turn can produce. List the wheels from left to right, and for each wheel put the turn up before the turn down.

**Constraints.** The limits are:
- **Wheels** satisfy `1 <= w <= 8`.
- **Code** contains only the characters `0` to `9`.
- **Result** is a list of exactly `2 * w` strings, and the input is not modified.

**Example 1.** Input `code = "1209"`, output `["2209","0209","1309","1109","1219","1299","1200","1208"]`.

**Example 2.** Input `code = "9"`, output `["0","8"]`.

**Hint.** Which character changes in each result, and what happens at the ends of the digit range?

**Changed decision.** The method builds each neighbor from a copy of the code and restores the changed digit before the next wheel.

#### [Vary] Open The Lock (LeetCode 752)
<!-- id: bv4-open-the-lock -->

**Prerequisites.** The first exercise above.

**Problem.** A lock has four wheels with digits 0 to 9 that start at `"0000"`. One turn moves one wheel up or down by one digit, with wrap-around. A list of dead codes is given, and the lock stops working if it shows a dead code. Return the minimum number of turns to show `target`, or -1 when no sequence of turns avoids every dead code.

**Constraints.** The limits are:
- **Dead codes** number `0 <= deadends.length <= 500`, each a string of four digits.
- **Target** is a string of four digits.
- **Start** may be a dead code, and then the result is -1.
- **Result** is one `int`.

**Example 1.** Input `deadends = ["0010","0001","1100"]`, `target = "0021"`, output `5`.

**Example 2.** Input `deadends = ["1000","9000","0100","0900","0010","0090","0001","0009"]`, `target = "5555"`, output `-1`.

**Hint.** Where can the dead codes be stored so that they are skipped like visited codes?

**Changed decision.** The method puts dead codes into the seen set before the search, so the check is the same as a visited check.

#### [Boundary] Forbidden Start And Target (Author exercise)
<!-- id: bv4-forbidden-endpoints -->

**Prerequisites.** The two exercises above.

**Problem.** A lock has `w` wheels with digits 0 to 9 and the same turn rule as before. Given a `start` code, a `target` code and a list of forbidden codes, return the minimum number of turns from `start` to `target` without ever showing a forbidden code. A forbidden `start` or a forbidden `target` makes the answer -1, even when the two codes are equal. Equal codes that are not forbidden give 0.

**Constraints.** The limits are:
- **Wheels** satisfy `1 <= w <= 5`, and `start`, `target` and every forbidden code have `w` digits.
- **Forbidden list** has `0 <= length <= 1000` codes, possibly with repeats.
- **Result** is one `int`, with -1 for an unreachable target.

**Example 1.** Input `start = "5"`, `target = "5"`, `forbidden = ["5"]`, output `-1`.

**Example 2.** Input `start = "3"`, `target = "3"`, `forbidden = ["2","4"]`, output `0`.

**Hint.** Which two checks must run before the first code enters the queue?

**Changed decision.** The method applies the forbidden rule to the start and the target before it enqueues anything, so equality of the two codes does not bypass it.

#### [Recognize] Shortest Path in Binary Matrix (LeetCode 1091)
<!-- id: bv4-shortest-path-binary-matrix -->

**Prerequisites.** All three exercises above.

**Problem.** A square grid `grid` of size `n` by `n` holds 0 for a free cell and 1 for a blocked cell. A clear path starts at `(0,0)`, ends at `(n-1,n-1)`, and uses only free cells. Consecutive cells of the path differ by at most 1 in each coordinate, so a cell has up to eight neighbors. Return the number of cells on the shortest clear path, or -1 when no clear path exists.

**Constraints.** The limits are:
- **Size** satisfies `1 <= n <= 100`.
- **Cells** are 0 or 1.
- **Endpoints** may be blocked, and then the result is -1.
- **Length** counts cells, so a single free cell gives 1.

**Example 1.** Input `grid = [[0,0,1,0],[1,0,1,0],[1,1,0,0],[0,0,1,0]]`, output `4`.

**Example 2.** Input `grid = [[1,0],[0,0]]`, output `-1`.

**Hint.** What is the state, and which rule generates its neighbors?

**Changed decision.** The state is the pair of coordinates, because no other fact changes the legal moves, and the successor rule has eight directions.
