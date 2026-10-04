<!-- lesson-kind: standard -->
<!-- lesson-id: state-space-bfs -->
## State-Space BFS

<!-- stage: context -->
### The Stiff Padlock On Locker 114

Ilse is a caretaker at Marlow Lane School, and over the holidays she has to open every locker whose owner left without a key. Locker 114 carries a cheap padlock with three number wheels, each showing a digit from 0 to 9. The wheels sit at 0 0 0. The sticker inside the cupboard door gives the code as 4 1 7. Turning one wheel by one click moves its digit up or down by one, and 9 rolls round to 0.

The trouble is that this padlock is old. A few wheel settings, such as 0 1 0 and 1 0 0, are worn so badly that the wheels will not move on from them, so Ilse must never pass through those settings. Each click costs her a few seconds and sore thumbs. She wants the smallest number of clicks that gets from 0 0 0 to 4 1 7 while avoiding every worn setting, and she wants a method that works for any lock, any code and any list of worn settings.

<!-- stage: naive -->
### Try Every Sequence Of Clicks

The direct approach is to try click sequences of length 1, then length 2, then length 3, and so on, stopping at the first length for which some sequence lands on the code. For a fixed length it explores every choice of wheel and direction, skips any setting on the worn list, and keeps going until the clicks run out.

```java
static boolean opensWithin(String setting, String code, Set<String> worn, int clicksLeft) {
    if (worn.contains(setting)) return false;
    if (setting.equals(code)) return true;
    if (clicksLeft == 0) return false;
    for (int wheel = 0; wheel < setting.length(); wheel++) {
        int digit = setting.charAt(wheel) - '0';
        for (int step : new int[] {9, 1}) {
            String next = setting.substring(0, wheel) + (char) ('0' + (digit + step) % 10)
                    + setting.substring(wheel + 1);
            if (opensWithin(next, code, worn, clicksLeft - 1)) return true;
        }
    }
    return false;
}

static int fewestClicks(String start, String code, Set<String> worn) {
    for (int limit = 0; limit <= 30; limit++)
        if (opensWithin(start, code, worn, limit)) return limit;
    return -1;
}
```

This is correct, since the smallest limit that succeeds is by definition the smallest number of clicks, and a sequence that revisits a setting only wastes clicks without breaking the answer. The cap of 30 is arbitrary and would be wrong for a lock whose real answer is longer.

<!-- stage: bottleneck -->
### The Same Setting Is Reached Again

With W wheels there are 2W moves from every setting, so a search of depth d visits about (2W)^d settings. For four wheels and a code that needs 12 clicks, that is 8^12, roughly seventy billion calls, and the iterative loop repeats all the shallower searches on top of it. The cost is O((2W)^d) per limit, which grows exponentially with the answer.

Almost all of that work is the same few settings seen again and again. The lock has only 10^W distinct settings, which is 10,000 for four wheels. Turning wheel one and then wheel two ends at exactly the same place as turning wheel two and then wheel one, and a click up followed by a click down returns to where it began. Each recursive call restarts from a setting that an earlier call already examined, without remembering that it did. A method that keeps a table of settings already reached would touch each of the 10,000 at most once, and BFS order would let the first arrival also be the shortest one.

<!-- stage: insight -->
### A Graph Nobody Wrote Down

Look at the lock as a graph whose vertices are the settings, even though no list of vertices or edges exists anywhere. Each vertex is described by a string of W digits, and that string is the **state encoding**: a compact value that names one situation completely and can be compared, hashed and stored in a seen set. The edges appear only when asked for. A small routine called the **move generator** takes one state and returns the states one legal click away, here two per wheel, one digit down and one digit up, each wrapping from 0 to 9 and back. BFS needs nothing else from the lock.

Worn settings are a third idea, the **dead state**: a state that may never be entered. The cleanest place to enforce that is the generator's caller. A neighbor is refused if it is dead, the same way a grid search refuses a wall. Because the start and the code are states too, either one can be dead, and that case must be decided before the first state goes on the queue.

The rest is ordinary BFS. The frontier holds states, a map from state to click count doubles as the seen set, and the first time a state is reached is the shortest way to reach it, because all clicks cost the same.

The one thing that can go wrong is the encoding itself. The invariant is that the encoding must contain every fact that changes which moves are legal later, and the seen set must be keyed by that whole encoding. For this padlock the digits alone suffice, since the rules of a click never depend on how the wheels got there.

<!-- names: state encoding, move generator, dead state -->

<!-- stage: variables -->
### Settings, Neighbors And Click Counts

The string `start` is where the wheels begin and `code` is the setting that opens the lock. The set `worn` holds the forbidden settings. The map `clicks` stores, for every state reached so far, the smallest number of clicks that gets there, so a missing key means unseen. The queue `frontier` holds states that have been reached but not yet expanded. Inside the loop, `cur` is the state just removed, and each string from the generator is a candidate `next`. The map entry for `next` is written only once, at the moment the candidate is accepted.

<!-- stage: trace -->
### Two Searches, One Over Strings

The first trace is a lock with two wheels, starting at 00 with code 21 and with the settings 10 and 11 worn. The cells are the settings in the exact order they are taken off the queue, and the pointer `cur` is the position of the one being expanded. The vars give its click count, how many states are waiting afterwards and how many it added. Because 10 is worn, the search cannot go straight up on the first wheel, so it leaves 00 only through 90, 09 and 01. Both 10 and 11 block the way to 21 from below, so the shortest route takes five clicks by way of 01, 02, 12 and 22. The search stops as soon as a generated neighbor equals the code, which is why the list of cells ends with 20.

```trace
{"cells":["00","90","09","01","80","99","91","19","08","02","70","89","81","98","92","29","18","07","12","03","60","79","71","88","82","97","93","39","28","20"],"pointers":["cur"],"steps":[{"at":{"cur":0},"vars":{"clicks":0,"waiting":3,"added":3},"note":"State 00 is expanded at 0 clicks; it adds 90, 09, 01."},{"at":{"cur":1},"vars":{"clicks":1,"waiting":5,"added":3},"note":"State 90 is expanded at 1 click; it adds 80, 99, 91."},{"at":{"cur":2},"vars":{"clicks":1,"waiting":6,"added":2},"note":"State 09 is expanded at 1 click; it adds 19, 08."},{"at":{"cur":3},"vars":{"clicks":1,"waiting":6,"added":1},"note":"State 01 is expanded at 1 click; it adds 02."},{"at":{"cur":4},"vars":{"clicks":2,"waiting":8,"added":3},"note":"State 80 is expanded at 2 clicks; it adds 70, 89, 81."},{"at":{"cur":5},"vars":{"clicks":2,"waiting":8,"added":1},"note":"State 99 is expanded at 2 clicks; it adds 98."},{"at":{"cur":6},"vars":{"clicks":2,"waiting":8,"added":1},"note":"State 91 is expanded at 2 clicks; it adds 92."},{"at":{"cur":7},"vars":{"clicks":2,"waiting":9,"added":2},"note":"State 19 is expanded at 2 clicks; it adds 29, 18."},{"at":{"cur":8},"vars":{"clicks":2,"waiting":9,"added":1},"note":"State 08 is expanded at 2 clicks; it adds 07."},{"at":{"cur":9},"vars":{"clicks":2,"waiting":10,"added":2},"note":"State 02 is expanded at 2 clicks; it adds 12, 03."},{"at":{"cur":10},"vars":{"clicks":3,"waiting":12,"added":3},"note":"State 70 is expanded at 3 clicks; it adds 60, 79, 71."},{"at":{"cur":11},"vars":{"clicks":3,"waiting":12,"added":1},"note":"State 89 is expanded at 3 clicks; it adds 88."},{"at":{"cur":12},"vars":{"clicks":3,"waiting":12,"added":1},"note":"State 81 is expanded at 3 clicks; it adds 82."},{"at":{"cur":13},"vars":{"clicks":3,"waiting":12,"added":1},"note":"State 98 is expanded at 3 clicks; it adds 97."},{"at":{"cur":14},"vars":{"clicks":3,"waiting":12,"added":1},"note":"State 92 is expanded at 3 clicks; it adds 93."},{"at":{"cur":15},"vars":{"clicks":3,"waiting":14,"added":3},"note":"State 29 is expanded at 3 clicks; it adds 39, 28, 20."},{"at":{"cur":16},"vars":{"clicks":3,"waiting":14,"added":1},"note":"State 18 is expanded at 3 clicks; it adds 17."},{"at":{"cur":17},"vars":{"clicks":3,"waiting":14,"added":1},"note":"State 07 is expanded at 3 clicks; it adds 06."},{"at":{"cur":18},"vars":{"clicks":3,"waiting":15,"added":2},"note":"State 12 is expanded at 3 clicks; it adds 22, 13."},{"at":{"cur":19},"vars":{"clicks":3,"waiting":15,"added":1},"note":"State 03 is expanded at 3 clicks; it adds 04."},{"at":{"cur":20},"vars":{"clicks":4,"waiting":17,"added":3},"note":"State 60 is expanded at 4 clicks; it adds 50, 69, 61."},{"at":{"cur":21},"vars":{"clicks":4,"waiting":17,"added":1},"note":"State 79 is expanded at 4 clicks; it adds 78."},{"at":{"cur":22},"vars":{"clicks":4,"waiting":17,"added":1},"note":"State 71 is expanded at 4 clicks; it adds 72."},{"at":{"cur":23},"vars":{"clicks":4,"waiting":17,"added":1},"note":"State 88 is expanded at 4 clicks; it adds 87."},{"at":{"cur":24},"vars":{"clicks":4,"waiting":17,"added":1},"note":"State 82 is expanded at 4 clicks; it adds 83."},{"at":{"cur":25},"vars":{"clicks":4,"waiting":17,"added":1},"note":"State 97 is expanded at 4 clicks; it adds 96."},{"at":{"cur":26},"vars":{"clicks":4,"waiting":17,"added":1},"note":"State 93 is expanded at 4 clicks; it adds 94."},{"at":{"cur":27},"vars":{"clicks":4,"waiting":19,"added":3},"note":"State 39 is expanded at 4 clicks; it adds 49, 38, 30."},{"at":{"cur":28},"vars":{"clicks":4,"waiting":19,"added":1},"note":"State 28 is expanded at 4 clicks; it adds 27."},{"at":{"cur":29},"vars":{"clicks":4,"waiting":19,"added":1},"note":"State 20 is expanded at 4 clicks; it adds 21. The code 21 is generated here, so the answer is 5 clicks."}]}
```

The second trace changes the kind of state: the grid is a flat three by three board with a blocked centre, the pointer `cur` is a flat cell index, and moves go to all eight surrounding cells. Here the state is just a position, since nothing about the history changes the moves. Each step reports the shortest length in cells, counting both ends, and the number of distinct shortest paths into the cell being expanded. A cell can collect path counts from several parents in the same layer, which is why the count at the corner is 2 and not 1.

```trace
{"cells":[0,0,0,0,1,0,0,0,0],"pointers":["cur"],"steps":[{"at":{"cur":0},"vars":{"length":1,"paths":1,"waiting":2},"note":"Cell 0 is expanded with shortest length 1 and 1 shortest path into it; 2 cells now wait."},{"at":{"cur":1},"vars":{"length":2,"paths":1,"waiting":3},"note":"Cell 1 is expanded with shortest length 2 and 1 shortest path into it; 3 cells now wait."},{"at":{"cur":3},"vars":{"length":2,"paths":1,"waiting":4},"note":"Cell 3 is expanded with shortest length 2 and 1 shortest path into it; 4 cells now wait."},{"at":{"cur":2},"vars":{"length":3,"paths":1,"waiting":3},"note":"Cell 2 is expanded with shortest length 3 and 1 shortest path into it; 3 cells now wait."},{"at":{"cur":5},"vars":{"length":3,"paths":1,"waiting":3},"note":"Cell 5 is expanded with shortest length 3 and 1 shortest path into it; 3 cells now wait."},{"at":{"cur":6},"vars":{"length":3,"paths":1,"waiting":2},"note":"Cell 6 is expanded with shortest length 3 and 1 shortest path into it; 2 cells now wait."},{"at":{"cur":7},"vars":{"length":3,"paths":1,"waiting":1},"note":"Cell 7 is expanded with shortest length 3 and 1 shortest path into it; 1 cell now wait."},{"at":{"cur":8},"vars":{"length":4,"paths":2,"waiting":0},"note":"Cell 8 is expanded with shortest length 4 and 2 shortest paths into it; 0 cells now wait."}]}
```

<!-- stage: code -->
### Breadth-First Over Lock Settings

```java
final class Lock {
    static List<String> neighbors(String state) {
        List<String> out = new ArrayList<>(2 * state.length());
        char[] wheels = state.toCharArray();
        for (int i = 0; i < wheels.length; i++) {
            char keep = wheels[i];
            wheels[i] = (char) ('0' + (keep - '0' + 9) % 10);
            out.add(new String(wheels));
            wheels[i] = (char) ('0' + (keep - '0' + 1) % 10);
            out.add(new String(wheels));
            wheels[i] = keep;
        }
        return out;
    }

    static int fewestClicks(String start, String code, Set<String> worn) {
        if (worn.contains(start) || worn.contains(code)) return -1;
        Map<String, Integer> clicks = new HashMap<>();
        ArrayDeque<String> frontier = new ArrayDeque<>();
        clicks.put(start, 0);
        frontier.add(start);
        while (!frontier.isEmpty()) {
            String cur = frontier.poll();
            if (cur.equals(code)) return clicks.get(cur);
            for (String next : neighbors(cur)) {
                if (worn.contains(next) || clicks.containsKey(next)) continue;
                clicks.put(next, clicks.get(cur) + 1);
                frontier.add(next);
            }
        }
        return -1;
    }
}
```

The generator restores each wheel after producing its two strings, so one `char[]` serves all the moves. Time is O(S * W) for S reachable states and W wheels, at most 10^W states, and space is O(S * W) for the map and queue. The start check up front is the dead-state rule applied before anything is queued.

<!-- stage: applicability -->
### When The Graph Is Implied

Reach for this model when a puzzle says "fewest moves" and the situation is described by a configuration instead of a drawn graph: lock dials, sliding tiles, a word changing one letter at a time, a robot with a battery level, a cube with a few rotations. The recognition cue is that you can write a function from one configuration to the list of configurations one move away. The invariant to defend is completeness: the encoding must record every fact that can change a future move, and the visited check must use all of it.

The false friend is encoding only the part you can see. A maze where doors need keys looks like a plain grid, yet standing on cell (3, 4) with the red key and standing there without it have different futures. Marking only the cell as visited would refuse the second arrival and miss a real route, so the state must be the cell and the set of keys held. The opposite mistake, adding facts that never change a move, is safe but wastes memory.

Do not use it when the number of reachable states is astronomically large, such as ten wheels with long answers, where a bidirectional search or a smarter model is needed, or when clicks have unequal costs, which needs a weighted shortest path method. In Java, `state.charAt(i) + 1` is an `int`, not a `char`, so it must be cast back before it is appended, and two equal strings compare equal only with `equals`, since `==` tests identity and a seen set keyed by identity never matches.

<!-- stage: exercises -->
### Exercises

#### [Build] Combination-Lock States (Author exercise)
<!-- id: bv-lock-neighbors -->

**Prerequisites.** The move generator from this lesson, and the idea of a digit string as a state.

**Problem.** The `state` is a string of 1 to 6 characters, each a digit from `'0'` to `'9'`, and it names the wheel settings of a lock, left to right. Return every state that is exactly one click away as a `List<String>`, in this order: for each wheel from left to right, first the state with that digit decreased by one, then the state with it increased by one, where 0 minus one is 9 and 9 plus one is 0. The input string is not modified, and the result always has twice as many entries as the string has wheels.

**Constraints.** 1 <= length <= 6, and every character is a digit. No dead states exist in this exercise.

**Example 1.** Input `"042"`, output `["942","142","032","052","041","043"]`.

**Example 2.** Input `"90"`, output `["80","00","99","91"]`.

**Hint.** Which wheel's digit changes in each entry, and what must happen to the copy after both of its neighbors have been written?

**Changed decision.** The neighbors are built from the encoding by changing one position at a time, instead of being read from a stored list of edges.

#### [Vary] Open The Lock (LeetCode 752)
<!-- id: bv-open-lock -->

**Prerequisites.** The Combination-Lock States rung and the click-count map from the code stage.

**Problem.** A lock has four wheels, each with digits 0 to 9 that wrap around, and starts at `"0000"`. The array `deadends` lists settings that jam the lock: once the wheels show one, they cannot be turned again. Given `target`, return the smallest number of clicks, one wheel one step at a time, that reaches it, or -1 when it is unreachable. A route may not pass through a listed setting, and the start counts as passed. The `deadends` array is not modified.

**Constraints.** 1 <= deadends.length <= 500, every string has exactly four digits, and `target` is not equal to `"0000"`.

**Example 1.** Input `deadends = ["0100","1000","0010"], target = "1230"`, output `8`.

**Example 2.** Input `deadends = ["1000","9000","2000"], target = "3000"`, output `5`.

**Hint.** The generator stays the same. What are the two extra gates a neighbor must pass before it is queued?

**Changed decision.** A neighbor is refused when it is a listed setting, so the dead set joins the seen set as a reason to skip a state.

#### [Boundary] Forbidden Start And Target (Author exercise)
<!-- id: bv-forbidden-ends -->

**Prerequisites.** The Open The Lock rung.

**Problem.** The lock has `start.length()` wheels and begins at the setting `start`, which need not be all zeros. The `forbidden` array lists settings that may never be shown, at any moment, including the first and the last. Return the fewest clicks from `start` to `target`, or -1 if no legal route exists. The contract for the edges is exact: if `start` is forbidden the answer is -1 even when `start` equals `target`, if `target` is forbidden the answer is -1, and if `start` equals `target` and is not forbidden the answer is 0. Neither array is modified.

**Constraints.** 1 <= wheels <= 6, `start` and `target` have the same length, every string is made of digits, and `forbidden` has at most 1000 entries.

**Example 1.** Input `start = "55", target = "55", forbidden = ["55"]`, output `-1`.

**Example 2.** Input `start = "7", target = "3", forbidden = ["4","6"]`, output `6`.

**Hint.** Which two checks can be answered without generating a single neighbor, and in which order must they run?

**Changed decision.** The forbidden list is applied to the start and the target before anything is enqueued, instead of only to neighbors.

#### [Recognize] Shortest Path In Binary Matrix (LeetCode 1091)
<!-- id: bv-binary-matrix-count -->

**Prerequisites.** The Forbidden Start And Target rung, and the shortest-path model of lesson 07 in the previous chapter.

**Problem.** The `grid` is an n by n `int[][]` of 0 (open) and 1 (blocked), and a move goes to any of the eight surrounding cells that is open. A path runs from the top-left cell to the bottom-right cell and may not repeat a cell. Return a `long[]` of two values: the length of the shortest path in cells, counting both ends, and the number of distinct shortest paths. If either end cell is blocked, or no path exists, return `[-1, 0]`. The grid is not modified.

**Constraints.** 1 <= n <= 8, and every entry is 0 or 1. The count fits in a `long`.

**Example 1.** Input `grid = [[0,0,0],[0,1,0],[0,0,0]]`, output `[4, 2]`.

**Example 2.** Input `grid = [[0,0,1,0],[0,0,0,0],[1,0,1,0],[0,0,0,0]]`, output `[5, 4]`.

**Hint.** When a cell is reached a second time from a cell in the previous layer, is the state new, and is the way of reaching it new?

**Changed decision.** The first arrival still fixes the length, but every later arrival from the preceding layer adds its path count, instead of being ignored.
