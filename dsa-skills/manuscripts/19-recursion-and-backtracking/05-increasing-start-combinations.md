<!-- lesson-kind: standard -->
<!-- lesson-id: increasing-start-combinations -->
## Increasing-Start Combinations

<!-- stage: context -->
### The Tasting Panels Of Wexcombe Dairy

The Wexcombe Dairy Guild has twenty members and judges its cheeses with panels of five. Whoever organises the panels wants every possible panel written down once, so that over a season each combination of five judges can be given a turn. A panel of Ada, Bo and Cy is plainly the same panel as Cy, Ada and Bo, since a panel has no head of table and nobody sits in a seat that matters.

The organiser's first list was enormous, and when she looked at it closely she found that nearly every panel appeared many times, once for each way of reading out the same names. She would like a method that writes each panel only once, however many members there are.

<!-- stage: naive -->
### List The Ordered Draws Then Merge Repeats

The panel organiser knows how to list every ordered draw of k members, the way a seating is listed. A draw of Ada then Bo and a draw of Bo then Ada are the same panel, so the direct method sorts the members of each draw into rank order and keeps one copy of every sorted draw in a set.

```java
static Set<List<Integer>> panelsByDraws(int n, int k) {
    Set<List<Integer>> panels = new LinkedHashSet<>();
    draw(n, k, new boolean[n + 1], new ArrayList<>(), panels);
    return panels;
}

private static void draw(int n, int k, boolean[] taken, List<Integer> got, Set<List<Integer>> panels) {
    if (got.size() == k) {
        List<Integer> sorted = new ArrayList<>(got);
        Collections.sort(sorted);
        panels.add(sorted);
        return;
    }
    for (int m = 1; m <= n; m++) {
        if (taken[m]) continue;
        taken[m] = true; got.add(m);
        draw(n, k, taken, got, panels);
        got.remove(got.size() - 1); taken[m] = false;
    }
}
```

Every panel is found, since each one is the sorted form of some draw, and the set removes the repeats, so the method is a sound oracle.

<!-- stage: bottleneck -->
### Each Panel Is Found k Factorial Times

An ordered draw of k members can be read out in k! ways that give the same panel, so the search produces n! / (n - k)! draws to find only n! / (k! (n - k)!) panels. For twenty members and panels of ten that is about 6.7 * 10^11 draws against 184,756 panels, and the set needs O(k log k) sorting work at each of them. The repeats are not a small constant. They grow faster than anything else in the problem as the panel size rises.

The cause is that the search allows a member to be picked at any step, so it explores every order of every panel. A rule that fixed one reading order for each panel and never offered a member out of that order would meet each panel exactly once, with no set and no sorting, and the number of leaves would equal the number of panels.

<!-- stage: insight -->
### Only Look Forward In The Row

Put the members in a row and decide that a panel is always read from left to right in rank order. Then a panel is built by picking members in that order, and each pick is made from members that stand to the right of the previous pick. The **start index** passed to a call is the first position of the row that the call may still pick from, and after picking position i the next call receives i + 1. Nothing to the left of the last pick is ever offered again.

That single number replaces the table of used marks. Every panel has exactly one **increasing route** through the tree of calls, namely its members in rank order, and no other route can spell it, since a route that went backwards in the row is never generated. So there are no repeats, and no set is needed to collapse them.

A second observation concerns the end of the loop. A call that still needs `need` members cannot succeed unless at least `need` positions remain from the current one to the end of the row. The **room bound** is the largest start that still leaves room, which is n - need + 1 for values numbered from 1, and a loop that stops there never walks into a dead branch. Every call it makes can still be completed into a full panel.

The invariant is that each pick comes from positions at or after the start index, so every panel appears once, in increasing order, and the room bound guarantees that every call made lies on a path to at least one panel.

<!-- names: start index, increasing route, room bound -->

<!-- stage: variables -->
### Start, Need And Path

The `start` is the lowest member number a call may pick, one at the first call and one more than the last pick afterwards. The `path` holds the picked members in increasing order. The quantity `need` is `k` minus the length of the path, the number of members still to pick, and it falls by one with each call. The upper limit of the loop is `n - need + 1`, which depends on `need` as it was before the pick, so it is computed at the top of the call. The `panels` list stores a copy of the path each time `need` reaches zero.

<!-- stage: trace -->
### Panels Of Two From Four Members

The first trace lists the panels of two from the four members 1 to 4. The pointer `start` is the first member the call may pick, and `i` is the member being picked now. The loop of the first call stops at the third member, and the loop of each later call stops at the fourth, so no call ever begins with fewer members to its right than it needs.

```trace
{"cells":["1","2","3","4"],"pointers":["start","i"],"steps":[{"at":{"start":0,"i":0},"vars":{"path":"[1]","need":1,"recorded":0},"note":"Member 1 is picked, so the path is [1] and the next call starts at member 2; this loop may run up to member 3."},{"at":{"start":1,"i":1},"vars":{"path":"[1, 2]","need":0,"recorded":0},"note":"Member 2 is picked, so the path is [1, 2] and the next call starts at member 3; this loop may run up to member 4."},{"at":{"start":2,"i":-1},"vars":{"path":"[1, 2]","need":0,"recorded":1},"note":"The path [1, 2] has k members, so a copy is recorded as panel 1."},{"at":{"start":1,"i":1},"vars":{"path":"[1]","need":1,"recorded":1},"note":"Member 2 is removed again, so the path is [1] and the loop tries the next member."},{"at":{"start":1,"i":2},"vars":{"path":"[1, 3]","need":0,"recorded":1},"note":"Member 3 is picked, so the path is [1, 3] and the next call starts at member 4; this loop may run up to member 4."},{"at":{"start":3,"i":-1},"vars":{"path":"[1, 3]","need":0,"recorded":2},"note":"The path [1, 3] has k members, so a copy is recorded as panel 2."},{"at":{"start":1,"i":2},"vars":{"path":"[1]","need":1,"recorded":2},"note":"Member 3 is removed again, so the path is [1] and the loop tries the next member."},{"at":{"start":1,"i":3},"vars":{"path":"[1, 4]","need":0,"recorded":2},"note":"Member 4 is picked, so the path is [1, 4] and the next call starts at member 5; this loop may run up to member 4."},{"at":{"start":4,"i":-1},"vars":{"path":"[1, 4]","need":0,"recorded":3},"note":"The path [1, 4] has k members, so a copy is recorded as panel 3."},{"at":{"start":1,"i":3},"vars":{"path":"[1]","need":1,"recorded":3},"note":"Member 4 is removed again, so the path is [1] and the loop tries the next member."},{"at":{"start":0,"i":0},"vars":{"path":"empty","need":2,"recorded":3},"note":"Member 1 is removed again, so the path is empty and the loop tries the next member."},{"at":{"start":0,"i":1},"vars":{"path":"[2]","need":1,"recorded":3},"note":"Member 2 is picked, so the path is [2] and the next call starts at member 3; this loop may run up to member 3."},{"at":{"start":2,"i":2},"vars":{"path":"[2, 3]","need":0,"recorded":3},"note":"Member 3 is picked, so the path is [2, 3] and the next call starts at member 4; this loop may run up to member 4."},{"at":{"start":3,"i":-1},"vars":{"path":"[2, 3]","need":0,"recorded":4},"note":"The path [2, 3] has k members, so a copy is recorded as panel 4."},{"at":{"start":2,"i":2},"vars":{"path":"[2]","need":1,"recorded":4},"note":"Member 3 is removed again, so the path is [2] and the loop tries the next member."},{"at":{"start":2,"i":3},"vars":{"path":"[2, 4]","need":0,"recorded":4},"note":"Member 4 is picked, so the path is [2, 4] and the next call starts at member 5; this loop may run up to member 4."},{"at":{"start":4,"i":-1},"vars":{"path":"[2, 4]","need":0,"recorded":5},"note":"The path [2, 4] has k members, so a copy is recorded as panel 5."},{"at":{"start":2,"i":3},"vars":{"path":"[2]","need":1,"recorded":5},"note":"Member 4 is removed again, so the path is [2] and the loop tries the next member."},{"at":{"start":0,"i":1},"vars":{"path":"empty","need":2,"recorded":5},"note":"Member 2 is removed again, so the path is empty and the loop tries the next member."},{"at":{"start":0,"i":2},"vars":{"path":"[3]","need":1,"recorded":5},"note":"Member 3 is picked, so the path is [3] and the next call starts at member 4; this loop may run up to member 3."},{"at":{"start":3,"i":3},"vars":{"path":"[3, 4]","need":0,"recorded":5},"note":"Member 4 is picked, so the path is [3, 4] and the next call starts at member 5; this loop may run up to member 4."},{"at":{"start":4,"i":-1},"vars":{"path":"[3, 4]","need":0,"recorded":6},"note":"The path [3, 4] has k members, so a copy is recorded as panel 6."},{"at":{"start":3,"i":3},"vars":{"path":"[3]","need":1,"recorded":6},"note":"Member 4 is removed again, so the path is [3] and the loop tries the next member."},{"at":{"start":0,"i":2},"vars":{"path":"empty","need":2,"recorded":6},"note":"Member 3 is removed again, so the path is empty and the loop tries the next member."}]}
```

The second trace is the false friend. It lists panels of two from three members with a table of used marks and no start index. The pointer `i` is the member being picked, and the variable `repeat` says whether the sorted panel was already recorded. The trace stops after four draws, which already includes a panel found for the second time.

```trace
{"cells":["1","2","3"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"path":"[1]","repeat":"no"},"note":"Member 1 is picked from anywhere in the row that is not marked, so the path is [1]."},{"at":{"i":1},"vars":{"path":"[1, 2]","repeat":"no"},"note":"Member 2 is picked from anywhere in the row that is not marked, so the path is [1, 2]."},{"at":{"i":1},"vars":{"path":"[1, 2]","repeat":"no"},"note":"The draw [1, 2] is complete as the panel [1, 2], which is new, so it is kept."},{"at":{"i":1},"vars":{"path":"[1]","repeat":"no"},"note":"Member 2 is removed and unmarked, so the path is [1]."},{"at":{"i":2},"vars":{"path":"[1, 3]","repeat":"no"},"note":"Member 3 is picked from anywhere in the row that is not marked, so the path is [1, 3]."},{"at":{"i":2},"vars":{"path":"[1, 3]","repeat":"no"},"note":"The draw [1, 3] is complete as the panel [1, 3], which is new, so it is kept."},{"at":{"i":2},"vars":{"path":"[1]","repeat":"no"},"note":"Member 3 is removed and unmarked, so the path is [1]."},{"at":{"i":0},"vars":{"path":"empty","repeat":"no"},"note":"Member 1 is removed and unmarked, so the path is empty."},{"at":{"i":1},"vars":{"path":"[2]","repeat":"no"},"note":"Member 2 is picked from anywhere in the row that is not marked, so the path is [2]."},{"at":{"i":0},"vars":{"path":"[2, 1]","repeat":"no"},"note":"Member 1 is picked from anywhere in the row that is not marked, so the path is [2, 1]."},{"at":{"i":0},"vars":{"path":"[2, 1]","repeat":"yes"},"note":"The draw [2, 1] is complete as the panel [1, 2], which was already recorded, so it is a repeat."},{"at":{"i":0},"vars":{"path":"[2]","repeat":"no"},"note":"Member 1 is removed and unmarked, so the path is [2]."},{"at":{"i":2},"vars":{"path":"[2, 3]","repeat":"no"},"note":"Member 3 is picked from anywhere in the row that is not marked, so the path is [2, 3]."},{"at":{"i":2},"vars":{"path":"[2, 3]","repeat":"no"},"note":"The draw [2, 3] is complete as the panel [2, 3], which is new, so it is kept."}]}
```

<!-- stage: code -->
### Start Index And Room Bound

```java
static List<List<Integer>> combine(int n, int k) {
    List<List<Integer>> panels = new ArrayList<>();
    pick(n, k, 1, new ArrayList<>(), panels);
    return panels;
}

private static void pick(int n, int k, int start, List<Integer> path, List<List<Integer>> panels) {
    int need = k - path.size();
    if (need == 0) {
        panels.add(new ArrayList<>(path));
        return;
    }
    for (int i = start; i <= n - need + 1; i++) {   // room bound
        path.add(i);
        pick(n, k, i + 1, path, panels);            // only members to the right
        path.remove(path.size() - 1);
    }
}
```

The bound uses `need` as it stands at the top of the call. A bound that is one too small cuts the loop short and silently drops every panel that ends with the last member. The number of calls equals the number of prefixes of panels, and the stack is k deep, so the time is within O(k) per panel plus the cost of the copy.

<!-- stage: applicability -->
### Unordered Selections Of Fixed Size

Use the increasing start when a result is a set of k items and the order inside it carries no meaning: teams, committees, hands of cards, subsets of fixed size, and every problem that asks for combinations. The invariant to rely on is that the picks form an increasing sequence of positions, so each set has exactly one spelling and a call can bound its loop using only its own need.

The nearest false friend is the table of used marks from the previous lesson. It looks like a safe way to stop a member being picked twice, and it does stop that, yet it allows every order of every set, so the output has k! copies of each panel. A second false friend is a search that stops at size k but starts every loop at the first member, which also repeats sets in different orders. The remedy in both cases is the same number, the start index.

Do not use it when the problem is about arrangements, where positions matter. When equal values appear in the input the start index alone is not enough, and the skip rule of a later lesson applies. In Java, compute the room bound from the need before the pick, copy the path at the leaf, and keep the combinations of n up to about twenty in mind, because the count of results is a binomial coefficient and grows quickly.

<!-- stage: exercises -->
### Exercises

#### [Build] Choose Two From Four (Author exercise)
<!-- id: bt-choose-two -->

**Prerequisites.** The working path with its undo step, and the permutation lesson as a contrast.

**Problem.** Given an array of between 2 and 6 distinct integers, return every pair of two elements, written in array order, with the pairs listed as found when each pick may use only positions after the previous pick.

**Constraints.** 2 <= nums.length <= 6, and the values are distinct integers between -50 and 50.

**Example 1.** Input `nums = [1, 2, 3, 4]`, output `[[1, 2], [1, 3], [1, 4], [2, 3], [2, 4], [3, 4]]`.

**Example 2.** Input `nums = [5, -1, 0]`, output `[[5, -1], [5, 0], [-1, 0]]`.

**Hint.** What number does the call for the second pick receive after the first pick sits at position i?

**Changed decision.** The next start moves just beyond the position picked, and values are compared by position, so the order of the input decides the order of each pair.

#### [Vary] Combinations From One To N (LeetCode 77)
<!-- id: bt-combinations-k -->

**Prerequisites.** The Choose Two From Four rung.

**Problem.** Given two integers `n` and `k`, return every combination of `k` numbers chosen from 1 to `n`, each written in increasing order, and the combinations in the order found by the increasing-start search. The call stops adding once the path has `k` numbers.

**Constraints.** 1 <= n <= 12 and 1 <= k <= n.

**Example 1.** Input `n = 4`, `k = 3`, output `[[1, 2, 3], [1, 2, 4], [1, 3, 4], [2, 3, 4]]`.

**Example 2.** Input `n = 1`, `k = 1`, output `[[1]]`.

**Hint.** At what path length does a call record a combination, and at what length does it loop?

**Changed decision.** The recursion stops on a size of k instead of on an index at the end of the row, so the leaves sit at one depth.

#### [Boundary] Insufficient Remaining Values (Author exercise)
<!-- id: bt-room-bound -->

**Prerequisites.** The Combinations From One To N rung.

**Problem.** Given `n` and `k` with 0 <= k, return a pair `[count, calls]`. Here `count` is the number of combinations of `k` numbers from 1 to `n`, and `calls` is how many times the recursive method runs, including the first call, when its loop stops as soon as too few numbers remain to fill the path. A `k` larger than `n` is allowed and has no combinations.

**Constraints.** 1 <= n <= 14 and 0 <= k <= 16.

**Example 1.** Input `n = 4`, `k = 2`, output `[6, 10]`.

**Example 2.** Input `n = 3`, `k = 5`, output `[0, 1]`.

**Hint.** If the loop bound is the end of the row, which calls can never reach a full path, and what does the bound need to know to remove them?

**Changed decision.** The upper limit of the loop now depends on how many picks are still needed, so dead branches are never entered at all.

#### [Recognize] Combination Sum III (LeetCode 216)
<!-- id: bt-sum-three -->

**Prerequisites.** The Insufficient Remaining Values rung.

**Problem.** Given `k` and `n`, return all sets of exactly `k` different digits from 1 to 9 that add up to `n`, each in increasing order and in the order found. Carry the remaining sum as one more parameter of the call, next to the start index.

**Constraints.** 1 <= k <= 9 and 1 <= n <= 60.

**Example 1.** Input `k = 3`, `n = 9`, output `[[1, 2, 6], [1, 3, 5], [2, 3, 4]]`.

**Example 2.** Input `k = 4`, `n = 1`, output `[]`.

**Hint.** What value must the remaining sum have when the path reaches length k, and which part of the state is unchanged from the combinations problem?

**Changed decision.** A second number joins the call state and shrinks with each pick, and a path is recorded only when both the length and the sum are exact.
