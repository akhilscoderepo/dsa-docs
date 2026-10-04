<!-- lesson-kind: standard -->
<!-- lesson-id: permutations -->
## Permutations

<!-- stage: context -->
### The Seating Cards Of Dunmore Hall

The steward of Dunmore Hall seats a small dinner party along one side of a long table, and the host likes to see every possible seating before choosing. Each guest has a name card. To try a seating, the steward takes a card from the pile, sets it at the first chair, then takes another card for the second chair, and so on until every chair has a guest. A card that is already at the table is turned face down on the pile, so that he cannot hand the same guest two chairs.

Two seatings that differ only in who sits where count as different, because the host cares that the duke sits beside the vicar in one of them and not in the other. The steward wants to be certain that every arrangement turns up exactly once, and that no guest is ever seated twice in the same arrangement.

<!-- stage: naive -->
### Try Every Sequence And Throw Out Repeats

The steward can ignore the idea of face-down cards and just fill each chair with any guest at all. For n guests that gives n choices per chair, which can be written as an odometer of n digits, each digit running over the guests. A finished sequence is kept only if it contains no guest twice.

```java
static List<List<Integer>> seatingsByFilter(int[] guests) {
    int n = guests.length;
    List<List<Integer>> kept = new ArrayList<>();
    int[] pick = new int[n];                       // pick[c] = guest index at chair c
    while (true) {
        boolean[] seen = new boolean[n];
        boolean ok = true;
        for (int c = 0; c < n && ok; c++) {
            if (seen[pick[c]]) ok = false; else seen[pick[c]] = true;
        }
        if (ok) {
            List<Integer> seating = new ArrayList<>();
            for (int c = 0; c < n; c++) seating.add(guests[pick[c]]);
            kept.add(seating);
        }
        int c = n - 1;
        while (c >= 0 && pick[c] == n - 1) pick[c--] = 0;
        if (c < 0) break;
        pick[c]++;
    }
    return kept;
}
```

The method is correct for any input, and its output order is a convenient reference for the faster search.

<!-- stage: bottleneck -->
### Most Sequences Seat Someone Twice

The odometer walks through n^n sequences, and only n! of them are real seatings. For four guests that is 256 sequences against 24 answers, but for ten guests it is ten billion sequences against about 3.6 million answers, and the check of each rejected sequence costs O(n) more. The loop spends nearly all its life on sequences that were doomed by their first two chairs, since a guest repeated at the second chair makes every continuation worthless, and yet the odometer still counts through all of those continuations one by one.

The cost is the failure to look at the sequence while it is still being built. A search that never offers a guest who is already seated would reach only valid prefixes, so every partial sequence it extends is a prefix of at least one real seating, and the work shrinks from n^n to the n! leaves plus the internal nodes above them.

<!-- stage: insight -->
### Depth Is The Chair Being Filled

Let the depth of the call be the chair being filled, so that depth d means chairs 0 to d - 1 already hold guests. The call loops over every guest index. Each guest who is already at the table is skipped, and every other guest is seated, the call recurses to fill the next chair, and the guest is taken off again. The **next position** is simply the depth, so the state of a call is one number plus the shared path.

A boolean array of **used marks** is what keeps a guest out of two chairs. Index i is marked as the guest is seated and the same index i is cleared as the guest is removed, so on return the marks equal what they were on entry. The marks are indexed by input position, not by value, which is the reason an input occurrence cannot fill two chairs even when two guests share a name.

The tree has n choices at the root, n - 1 at the next level, and so on down, so it has n! leaves, and an arrangement is recorded when the depth equals n. There is a second way to hold the same state without any marks. An **in-place swap** exchanges the guest at the current chair with a guest further along the array, so the array's prefix is the seated part and its suffix is the remaining pile, and a second swap undoes the first on the way back.

The invariant is that the depth equals the number of filled positions, and each input occurrence is either on the path exactly once or unmarked and available.

<!-- names: next position, used marks, in-place swap -->

<!-- stage: variables -->
### Depth, Path, Used And Results

The `depth` is the number of filled chairs and grows by one with each call. The `path` holds the guests seated so far in chair order and is changed by one guest per move. The array `used` has one flag per input index, false at the start, set to true at the moment a guest is seated and set to false again at the moment the guest leaves. In the swapping form, `pos` replaces both depth and the marks, because the array prefix before `pos` is the path. The `results` list receives a copy of the path at depth n.

<!-- stage: trace -->
### Seating Three Guests In Turn

The first trace uses the marks and stops after the third arrangement, which is enough to show a deep return and a shallow return. The pointer `depth` is the chair being filled and `i` is the guest being offered, and the variable `used` shows the marks of the three guests in order. Notice that a guest at a marked index is never offered, and that the marks are cleared as the search climbs back.

```trace
{"cells":["1","2","3"],"pointers":["depth","i"],"steps":[{"at":{"depth":0,"i":0},"vars":{"path":"[1]","used":"TFF"},"note":"Guest 1 is offered for chair 0, so index 0 is marked and the path is [1]."},{"at":{"depth":1,"i":1},"vars":{"path":"[1, 2]","used":"TTF"},"note":"Guest 2 is offered for chair 1, so index 1 is marked and the path is [1, 2]."},{"at":{"depth":2,"i":2},"vars":{"path":"[1, 2, 3]","used":"TTT"},"note":"Guest 3 is offered for chair 2, so index 2 is marked and the path is [1, 2, 3]."},{"at":{"depth":3,"i":-1},"vars":{"path":"[1, 2, 3]","used":"TTT"},"note":"All three chairs are filled, so a copy of [1, 2, 3] is recorded as arrangement 1."},{"at":{"depth":2,"i":2},"vars":{"path":"[1, 2]","used":"TTF"},"note":"Guest 3 leaves chair 2, so index 2 is cleared and the path is [1, 2]."},{"at":{"depth":1,"i":1},"vars":{"path":"[1]","used":"TFF"},"note":"Guest 2 leaves chair 1, so index 1 is cleared and the path is [1]."},{"at":{"depth":1,"i":2},"vars":{"path":"[1, 3]","used":"TFT"},"note":"Guest 3 is offered for chair 1, so index 2 is marked and the path is [1, 3]."},{"at":{"depth":2,"i":1},"vars":{"path":"[1, 3, 2]","used":"TTT"},"note":"Guest 2 is offered for chair 2, so index 1 is marked and the path is [1, 3, 2]."},{"at":{"depth":3,"i":-1},"vars":{"path":"[1, 3, 2]","used":"TTT"},"note":"All three chairs are filled, so a copy of [1, 3, 2] is recorded as arrangement 2."},{"at":{"depth":2,"i":1},"vars":{"path":"[1, 3]","used":"TFT"},"note":"Guest 2 leaves chair 2, so index 1 is cleared and the path is [1, 3]."},{"at":{"depth":1,"i":2},"vars":{"path":"[1]","used":"TFF"},"note":"Guest 3 leaves chair 1, so index 2 is cleared and the path is [1]."},{"at":{"depth":0,"i":0},"vars":{"path":"[]","used":"FFF"},"note":"Guest 1 leaves chair 0, so index 0 is cleared and the path is empty."},{"at":{"depth":0,"i":1},"vars":{"path":"[2]","used":"FTF"},"note":"Guest 2 is offered for chair 0, so index 1 is marked and the path is [2]."},{"at":{"depth":1,"i":0},"vars":{"path":"[2, 1]","used":"TTF"},"note":"Guest 1 is offered for chair 1, so index 0 is marked and the path is [2, 1]."},{"at":{"depth":2,"i":2},"vars":{"path":"[2, 1, 3]","used":"TTT"},"note":"Guest 3 is offered for chair 2, so index 2 is marked and the path is [2, 1, 3]."},{"at":{"depth":3,"i":-1},"vars":{"path":"[2, 1, 3]","used":"TTT"},"note":"All three chairs are filled, so a copy of [2, 1, 3] is recorded as arrangement 3."}]}
```

The second trace holds the same search in a single array with swaps. The pointer `pos` is the chair being filled and `j` is the position that is swapped into it, so `j` equal to `pos` is a swap of a guest with themselves. The variable `array` shows the whole array after each move, with the seated prefix at the front.

```trace
{"cells":["1","2","3"],"pointers":["pos","j"],"steps":[{"at":{"pos":0,"j":0},"vars":{"array":"[1, 2, 3]"},"note":"Position 0 swaps with position 0, so the seated front of the array is now [1]."},{"at":{"pos":1,"j":1},"vars":{"array":"[1, 2, 3]"},"note":"Position 1 swaps with position 1, so the seated front of the array is now [1, 2]."},{"at":{"pos":2,"j":2},"vars":{"array":"[1, 2, 3]"},"note":"Position 2 swaps with position 2, so the seated front of the array is now [1, 2, 3]."},{"at":{"pos":3,"j":-1},"vars":{"array":"[1, 2, 3]"},"note":"Every chair is filled, so a copy of [1, 2, 3] is recorded as arrangement 1."},{"at":{"pos":2,"j":2},"vars":{"array":"[1, 2, 3]"},"note":"The swap of positions 2 and 2 is reversed, so the array reads [1, 2, 3] again."},{"at":{"pos":1,"j":1},"vars":{"array":"[1, 2, 3]"},"note":"The swap of positions 1 and 1 is reversed, so the array reads [1, 2, 3] again."},{"at":{"pos":1,"j":2},"vars":{"array":"[1, 3, 2]"},"note":"Position 1 swaps with position 2, so the seated front of the array is now [1, 3]."},{"at":{"pos":2,"j":2},"vars":{"array":"[1, 3, 2]"},"note":"Position 2 swaps with position 2, so the seated front of the array is now [1, 3, 2]."},{"at":{"pos":3,"j":-1},"vars":{"array":"[1, 3, 2]"},"note":"Every chair is filled, so a copy of [1, 3, 2] is recorded as arrangement 2."},{"at":{"pos":2,"j":2},"vars":{"array":"[1, 3, 2]"},"note":"The swap of positions 2 and 2 is reversed, so the array reads [1, 3, 2] again."},{"at":{"pos":1,"j":2},"vars":{"array":"[1, 2, 3]"},"note":"The swap of positions 1 and 2 is reversed, so the array reads [1, 2, 3] again."},{"at":{"pos":0,"j":0},"vars":{"array":"[1, 2, 3]"},"note":"The swap of positions 0 and 0 is reversed, so the array reads [1, 2, 3] again."},{"at":{"pos":0,"j":1},"vars":{"array":"[2, 1, 3]"},"note":"Position 0 swaps with position 1, so the seated front of the array is now [2]."},{"at":{"pos":1,"j":1},"vars":{"array":"[2, 1, 3]"},"note":"Position 1 swaps with position 1, so the seated front of the array is now [2, 1]."},{"at":{"pos":2,"j":2},"vars":{"array":"[2, 1, 3]"},"note":"Position 2 swaps with position 2, so the seated front of the array is now [2, 1, 3]."},{"at":{"pos":3,"j":-1},"vars":{"array":"[2, 1, 3]"},"note":"Every chair is filled, so a copy of [2, 1, 3] is recorded as arrangement 3."}]}
```

<!-- stage: code -->
### Marks In An Array

```java
static List<List<Integer>> seatings(int[] guests) {
    List<List<Integer>> results = new ArrayList<>();
    place(guests, new boolean[guests.length], new ArrayList<>(), results);
    return results;
}

private static void place(int[] guests, boolean[] used, List<Integer> path, List<List<Integer>> results) {
    if (path.size() == guests.length) {            // depth equals n
        results.add(new ArrayList<>(path));
        return;
    }
    for (int i = 0; i < guests.length; i++) {
        if (used[i]) continue;                     // already seated
        used[i] = true;
        path.add(guests[i]);
        place(guests, used, path, results);
        path.remove(path.size() - 1);
        used[i] = false;                           // clear the same index
    }
}
```

When the guests are stored in an `int[]`, copying a finished arrangement needs a loop, since `Arrays.asList` applied to an `int[]` returns a list with one element, which is the whole array. The search makes O(n) work at every node beyond the copies and has n! leaves, so it takes O(n * n!) time, with a stack n deep.

<!-- stage: applicability -->
### Every Element Used, Order Counts

Use the used-marks search when every element must appear in the output and the order of the elements is part of the answer: schedules of tasks, seatings, orders of visiting stops, and all the words that can be made from a set of letters. What the search relies on is an invariant, that the depth is the number of filled positions and that a mark is set exactly for the occurrences on the path.

The nearest false friend is the increasing-start loop of the last lesson. That loop never looks backward, so it produces each set of elements once in rank order, which is a combination, and using it where order matters misses every arrangement that is not increasing. The reverse mistake is also a false friend: a used-marks search where order does not matter returns each selection n! times over. A second false friend is a global mark that is never cleared, which blocks guests for every later branch, as in the earlier lesson.

Do not list all arrangements when n is much beyond ten, since the count has already passed three million, and ask whether a count or a best value can be computed without listing. In Java, mark and clear the same index, copy the result when the path is a list or an array, and remember that equal values need the skip rule of a later lesson, because the marks alone treat two equal guests as different people.

<!-- stage: exercises -->
### Exercises

#### [Build] Permute Three Distinct Values (Author exercise)
<!-- id: bt-permute-three -->

**Prerequisites.** The working path with its undo step, and the idea that the depth is the position being filled.

**Problem.** Given an array of exactly three distinct integers, return all six arrangements. A call fills one position, offers the values from the lowest index to the highest, and skips any index that is marked as used. Return the arrangements in the order they are found.

**Constraints.** The array has length 3, and its values are distinct integers between -50 and 50.

**Example 1.** Input `nums = [1, 2, 3]`, output `[[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]`.

**Example 2.** Input `nums = [9, -4, 0]`, output `[[9, -4, 0], [9, 0, -4], [-4, 9, 0], [-4, 0, 9], [0, 9, -4], [0, -4, 9]]`.

**Hint.** If the mark were set but never cleared, how many arrangements could the search ever finish?

**Changed decision.** A mark on an index replaces the start index of earlier lessons, and every call scans all indexes from zero.

#### [Vary] Permutations By Swapping (LeetCode 46)
<!-- id: bt-permute-swaps -->

**Prerequisites.** The Permute Three Distinct Values rung.

**Problem.** For an array of distinct integers, list every arrangement using a single array and no marks. The call for position `pos` swaps the element at `pos` with each element at index `j >= pos` in turn, recurses on `pos + 1`, and swaps back. Results appear in discovery order.

**Constraints.** 0 <= nums.length <= 8, and the values are distinct integers between -20 and 20.

**Example 1.** Input `nums = [1, 2, 3]`, output `[[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 2, 1], [3, 1, 2]]`.

**Example 2.** Input `nums = [8]`, output `[[8]]`.

**Hint.** After the recursive call returns, what does the suffix of the array look like if the swap is not reversed?

**Changed decision.** The state moves into the array itself, so the used marks disappear and the undo step becomes a second swap.

#### [Boundary] Restore Used State (Author exercise)
<!-- id: bt-restore-used -->

**Prerequisites.** The Permutations By Swapping rung.

**Problem.** Given an array of distinct integers and a length `r`, return every ordered selection of `r` of them, using a used-marks search that stops at depth `r`. Selections are returned in the order found when indexes are offered from low to high. When `r` is 0 the answer is one empty selection, and when `r` exceeds the array length there are none.

**Constraints.** 0 <= nums.length <= 7, 0 <= r <= 9, and the values are distinct integers between -20 and 20.

**Example 1.** Input `nums = [1, 2, 3]`, `r = 2`, output `[[1, 2], [1, 3], [2, 1], [2, 3], [3, 1], [3, 2]]`.

**Example 2.** Input `nums = [7, 8]`, `r = 3`, output `[]`.

**Hint.** When a call returns from a selection that stopped early, which single flag must it clear, and which flags must it leave alone?

**Changed decision.** The search stops at depth r and not at depth n, so most calls return without using every mark, and each must clear exactly its own.

#### [Recognize] Permutations With Equal Values (LeetCode 47)
<!-- id: bt-permutations-equal -->

**Prerequisites.** The Restore Used State rung. The skip rule is previewed here and explained fully in the Duplicate Control lesson.

**Problem.** Given an array of integers that may repeat, return every distinct arrangement. Sort a copy, then skip an index when its value equals the value before it and that earlier index is not currently marked. Arrangements are returned in the order found.

**Constraints.** 0 <= nums.length <= 8, and the values are integers between -10 and 10.

**Example 1.** Input `nums = [1, 1, 2]`, output `[[1, 1, 2], [1, 2, 1], [2, 1, 1]]`.

**Example 2.** Input `nums = [2, 2, 1, 2]`, output `[[1, 2, 2, 2], [2, 1, 2, 2], [2, 2, 1, 2], [2, 2, 2, 1]]`.

**Hint.** Among equal values at one depth, which one is offered first, and why is it wrong to forbid an equal value at a deeper depth?

**Changed decision.** Equal values are offered once per depth, but each of them can still fill a later position, so the rule looks at the mark of the previous index.
