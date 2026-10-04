<!-- lesson-kind: standard -->
<!-- lesson-id: choose-explore-unchoose -->
## Choose Explore Unchoose

<!-- stage: context -->
### The Single Tray Of Marlow Inn

The kitchen of Marlow Inn plans its tasting menus on one wooden tray. For the first course the chef lays a dish on the tray, then thinks about what could follow it, then lays a second course beside the first, and so on until the tray holds a full menu, which she copies onto a card. Then she lifts the last dish off the tray and tries the next alternative for that course. When every alternative for the last course is spent, she lifts the dish before it and tries its alternatives. The tray is never emptied by hand between menus. It simply always shows the dishes of the menu she is working on, no more and no fewer.

One busy evening a new apprentice took over and, after finishing the menus that began with the soup, he moved on to the fish without lifting the soup off. Every later card carried a soup that nobody had ordered.

<!-- stage: naive -->
### Hand Every Course A Fresh Tray

The safest way to avoid leftovers is to give each course its own tray. A method that builds menus takes the current dishes as a list, makes a new list that holds those dishes plus the next one, and passes the new list down. Nothing is ever lifted off, because nothing is ever shared, and a finished menu is just the list that arrives at the last course.

```java
static void menus(List<String> options, int course, List<String> dishes, List<List<String>> cards) {
    if (course == options.size()) { cards.add(dishes); return; }
    for (char c : options.get(course).toCharArray()) {
        List<String> next = new ArrayList<>(dishes);
        next.add(String.valueOf(c));
        menus(options, course + 1, next, cards);
    }
}
```

This is correct for every input, since no call can disturb another call's list, and it is a good oracle for the version that follows.

<!-- stage: bottleneck -->
### Every Visit Pays For A Whole Copy

Each call copies the dishes it was given, so a call at depth d costs O(d) before it does anything else, and the search visits a number of calls that grows with every extra choice. When almost every visit ends in a finished menu, the copying roughly matches the cost of writing the cards and little is lost. Later lessons prune most branches, and then most visits end without producing a card, so the copying becomes the main cost: the search pays O(depth) at every visit to build lists that are thrown away within moments, and fills the memory with short-lived garbage.

The copying exists only because the method fears sharing. The real need is much smaller, namely that a sibling branch must see the same dishes the parent had. One shared list could serve that need, and a call would then cost O(1) to place or lift a dish, if the list were put back exactly as it was before each alternative is tried.

<!-- stage: insight -->
### Place It, Look Beyond It, Lift It

Keep one **working path**, a single mutable list that holds exactly the decisions made on the way from the first call to the current one. Each call takes a decision from its set of alternatives, appends it to the working path, makes the recursive call for the rest, and then runs the **unchoose step**, which removes precisely what was appended. The three moves are written in this order every time, with nothing between the recursive call and the removal that could skip it.

The removal is what makes sharing safe. When a call returns, the working path is identical to what it was when the call began, so the next alternative at the same depth starts from the same state as the previous one did. A call can therefore be understood alone: on entry, the path is the prefix it was promised, and on exit, the path is that same prefix again, whatever happened below.

A finished path must not be stored by reference. The list will keep changing as the search goes on, so a result must be a **snapshot copy** taken at the moment the path is complete. Copying only at that moment costs O(length of the path) once per result, while every other visit costs O(1).

The invariant is that on entry to every call the working path equals the decisions on the current route, and on exit it equals the same decisions again.

<!-- names: working path, unchoose step, snapshot copy -->

<!-- stage: variables -->
### Position, Path And Results

The `position` is the depth of the call, which is how many decisions are already fixed, and it grows by one on each recursive call. The `path` is the shared list of fixed decisions, and it changes twice around each recursive call: once to append and once to remove. The `results` list is the only place copies are stored, and it grows only when a call reaches the final position. The alternatives for a position, here the letters of one option string, never change during the run, so a loop over them is safe even though the path changes inside the loop.

<!-- stage: trace -->
### Four Menus From One Tray

The first trace builds every menu from the option strings `ab`, `c` and `de`. The pointer `depth` is the course being decided, and the last step of each menu sits at the position one past the final course, where the copy is stored. Watch the line after each storing step: the removals peel the path back one dish at a time, and the next alternative starts from a shorter path.

```trace
{"cells":["ab","c","de"],"pointers":["depth"],"steps":[{"at":{"depth":0},"vars":{"path":"a","stored":0},"note":"The course at depth 0 puts a on the path, which now reads a."},{"at":{"depth":1},"vars":{"path":"ac","stored":0},"note":"The course at depth 1 puts c on the path, which now reads ac."},{"at":{"depth":2},"vars":{"path":"acd","stored":0},"note":"The course at depth 2 puts d on the path, which now reads acd."},{"at":{"depth":3},"vars":{"path":"acd","stored":1},"note":"Every course is decided, so a copy of the path is stored as menu 1, reading acd."},{"at":{"depth":2},"vars":{"path":"ac","stored":1},"note":"Everything below d is finished, so d is lifted and the path reads ac again."},{"at":{"depth":2},"vars":{"path":"ace","stored":1},"note":"The course at depth 2 puts e on the path, which now reads ace."},{"at":{"depth":3},"vars":{"path":"ace","stored":2},"note":"Every course is decided, so a copy of the path is stored as menu 2, reading ace."},{"at":{"depth":2},"vars":{"path":"ac","stored":2},"note":"Everything below e is finished, so e is lifted and the path reads ac again."},{"at":{"depth":1},"vars":{"path":"a","stored":2},"note":"Everything below c is finished, so c is lifted and the path reads a again."},{"at":{"depth":0},"vars":{"path":"empty","stored":2},"note":"Everything below a is finished, so a is lifted and the path reads nothing again."},{"at":{"depth":0},"vars":{"path":"b","stored":2},"note":"The course at depth 0 puts b on the path, which now reads b."},{"at":{"depth":1},"vars":{"path":"bc","stored":2},"note":"The course at depth 1 puts c on the path, which now reads bc."},{"at":{"depth":2},"vars":{"path":"bcd","stored":2},"note":"The course at depth 2 puts d on the path, which now reads bcd."},{"at":{"depth":3},"vars":{"path":"bcd","stored":3},"note":"Every course is decided, so a copy of the path is stored as menu 3, reading bcd."},{"at":{"depth":2},"vars":{"path":"bc","stored":3},"note":"Everything below d is finished, so d is lifted and the path reads bc again."},{"at":{"depth":2},"vars":{"path":"bce","stored":3},"note":"The course at depth 2 puts e on the path, which now reads bce."},{"at":{"depth":3},"vars":{"path":"bce","stored":4},"note":"Every course is decided, so a copy of the path is stored as menu 4, reading bce."},{"at":{"depth":2},"vars":{"path":"bc","stored":4},"note":"Everything below e is finished, so e is lifted and the path reads bc again."},{"at":{"depth":1},"vars":{"path":"b","stored":4},"note":"Everything below c is finished, so c is lifted and the path reads b again."},{"at":{"depth":0},"vars":{"path":"empty","stored":4},"note":"Everything below b is finished, so b is lifted and the path reads nothing again."}]}
```

The second trace shows what happens when a completed path is stored without a copy. It runs the search that lists every way to climb three stairs with steps of one or two, and it stores the working list itself. The pointer `pick` marks which step size is on the path, and the variable `stored` shows what the stored results read at that moment. The first result is correct for exactly one step.

```trace
{"cells":["1","2"],"pointers":["pick"],"steps":[{"at":{"pick":0},"vars":{"path":"[1]","stored":"[]"},"note":"A step of 1 goes on the path, leaving 2 stairs."},{"at":{"pick":0},"vars":{"path":"[1, 1]","stored":"[]"},"note":"A step of 1 goes on the path, leaving 1 stairs."},{"at":{"pick":0},"vars":{"path":"[1, 1, 1]","stored":"[]"},"note":"A step of 1 goes on the path, leaving 0 stairs."},{"at":{"pick":-1},"vars":{"path":"[1, 1, 1]","stored":"[[1, 1, 1]]"},"note":"The stairs are used up, and the working list itself is stored, with no copy, as result 1."},{"at":{"pick":0},"vars":{"path":"[1, 1]","stored":"[[1, 1]]"},"note":"The step of 1 is lifted, and every stored result that is this same list changes with it."},{"at":{"pick":0},"vars":{"path":"[1]","stored":"[[1]]"},"note":"The step of 1 is lifted, and every stored result that is this same list changes with it."},{"at":{"pick":1},"vars":{"path":"[1, 2]","stored":"[[1, 2]]"},"note":"A step of 2 goes on the path, leaving 0 stairs."},{"at":{"pick":-1},"vars":{"path":"[1, 2]","stored":"[[1, 2], [1, 2]]"},"note":"The stairs are used up, and the working list itself is stored, with no copy, as result 2."},{"at":{"pick":1},"vars":{"path":"[1]","stored":"[[1], [1]]"},"note":"The step of 2 is lifted, and every stored result that is this same list changes with it."},{"at":{"pick":0},"vars":{"path":"[]","stored":"[[], []]"},"note":"The step of 1 is lifted, and every stored result that is this same list changes with it."},{"at":{"pick":1},"vars":{"path":"[2]","stored":"[[2], [2]]"},"note":"A step of 2 goes on the path, leaving 1 stairs."},{"at":{"pick":0},"vars":{"path":"[2, 1]","stored":"[[2, 1], [2, 1]]"},"note":"A step of 1 goes on the path, leaving 0 stairs."},{"at":{"pick":-1},"vars":{"path":"[2, 1]","stored":"[[2, 1], [2, 1], [2, 1]]"},"note":"The stairs are used up, and the working list itself is stored, with no copy, as result 3."},{"at":{"pick":0},"vars":{"path":"[2]","stored":"[[2], [2], [2]]"},"note":"The step of 1 is lifted, and every stored result that is this same list changes with it."},{"at":{"pick":1},"vars":{"path":"[]","stored":"[[], [], []]"},"note":"The step of 2 is lifted, and every stored result that is this same list changes with it."},{"at":{"pick":-1},"vars":{"path":"[]","stored":"[[], [], []]"},"note":"The search is over and the path is empty, so all three stored results are the same empty list."}]}
```

<!-- stage: code -->
### The Three Moves In Order

```java
static List<List<Character>> allMenus(List<String> options) {
    List<List<Character>> results = new ArrayList<>();
    build(options, 0, new ArrayList<>(), results);
    return results;
}

private static void build(List<String> options, int position,
                          List<Character> path, List<List<Character>> results) {
    if (position == options.size()) {
        results.add(new ArrayList<>(path));            // snapshot copy
        return;
    }
    for (char c : options.get(position).toCharArray()) {
        path.add(c);                                   // place the decision
        build(options, position + 1, path, results);   // look beyond it
        path.remove(path.size() - 1);                  // lift it, by index
    }
}
```

The removal is by index on purpose. For a list of `Integer` values, a call such as `path.remove(x)` with an `int` argument removes the element at position x, not the value x, and the working path then loses the wrong item. The search visits each node of the decision tree once, at O(1) cost beyond the stored copies, and the stack is as deep as the number of positions.

<!-- stage: applicability -->
### Shared State Needs An Exact Undo

Use the three moves when one candidate is grown a decision at a time, and the search must come back and try a sibling from the same starting point. Menus, schedules, arrangements and every generator in the remaining lessons of this chapter fit. What must stay true, as the invariant of every call, is that the working path on exit equals the working path on entry, so any extra state that a call changes, such as a counter or a mark, has its own undo step.

The nearest false friend is the version that forgets the undo and keeps going. It looks almost identical and often produces correct first results, which is what makes the bug hard to see, and then every later branch inherits decisions that belong to a finished branch. A second false friend is the copy-per-call method from the naive stage, which is right but pays for a whole copy at every visit, and it is a sensible choice only when the depth is tiny or the search is not pruned.

Do not reach for a shared working path when the state is a single number or an immutable value that is naturally passed down by value, because the undo is then automatic and nothing can leak. In Java, remember the two traps of the shared list: store a copy and not the list itself, and remove by index and not by value when the elements are integers.

<!-- stage: exercises -->
### Exercises

#### [Build] Binary Choices (Author exercise)
<!-- id: bt-binary-choices -->

**Prerequisites.** The idea of a working path, and a call that makes one decision per position.

**Problem.** Given a length `n`, return every string of `n` characters, each `0` or `1`, in increasing order. Use one shared list or builder for the working path, append a digit, recurse, then remove it before the other digit is tried.

**Constraints.** 0 <= n <= 12, so at most 4096 strings are returned.

**Example 1.** Input `n = 2`, output `["00", "01", "10", "11"]`.

**Example 2.** Input `n = 0`, output `[""]`.

**Hint.** What must the path look like at the moment the alternative digit is appended, and which line makes that true?

**Changed decision.** Two alternatives at every depth, with the path shortened by exactly one character before the second alternative is tried.

#### [Vary] Variable Candidate Loop (Author exercise)
<!-- id: bt-variable-loop -->

**Prerequisites.** The Binary Choices rung.

**Problem.** Given a list `options` of strings, pick exactly one letter from each string, in order, and return every string formed this way. Results appear in the order the search finds them when the letters of each option are tried left to right. If any option string is empty, no word can be formed.

**Constraints.** 0 <= options.length <= 8, each option has 0 to 4 lowercase letters.

**Example 1.** Input `options = ["ab", "c", "de"]`, output `["acd", "ace", "bcd", "bce"]`.

**Example 2.** Input `options = ["xy", "", "z"]`, output `[]`.

**Hint.** What does a loop over zero alternatives do to the recursive call, and what does the list of results contain afterwards?

**Changed decision.** The number of alternatives differs at each depth, so the loop bound comes from the option at that position, while the append and remove stay the same.

#### [Boundary] Store A Completed Path (Author exercise)
<!-- id: bt-store-completed -->

**Prerequisites.** The Variable Candidate Loop rung.

**Problem.** Return every way to climb `n` stairs using steps of 1 or 2, each way written as the list of step sizes taken in order. Ways are listed in the order found when the step of 1 is tried before the step of 2. Climbing zero stairs has exactly one way, which is the empty list.

**Constraints.** 0 <= n <= 14, so every count of ways fits easily in an int.

**Example 1.** Input `n = 3`, output `[[1, 1, 1], [1, 2], [2, 1]]`.

**Example 2.** Input `n = 0`, output `[[]]`.

**Hint.** If the results held the working list itself rather than a copy, what would every stored entry look like once the search has finished?

**Changed decision.** The completed path is copied at the moment it is stored, so later removals cannot reach into the results.

#### [Recognize] Subsets (LeetCode 78)
<!-- id: bt-subsets-include-first -->

**Prerequisites.** The Store A Completed Path rung.

**Problem.** Take an array of distinct integers and produce every subset, each written in the original order of the array. Decide each element in turn as include or exclude, trying include first, and record a subset only when every element has been decided.

**Constraints.** 0 <= nums.length <= 10, and the values are distinct integers between -10 and 10.

**Example 1.** Input `nums = [1, 2, 3]`, output `[[1, 2, 3], [1, 2], [1, 3], [1], [2, 3], [2], [3], []]`.

**Example 2.** Input `nums = [5]`, output `[[5], []]`.

**Hint.** Which of the two choices at an element needs an undo step, and which does not?

**Changed decision.** The decision at each position is whether to place the element at all, so the exclude branch leaves the path untouched.
